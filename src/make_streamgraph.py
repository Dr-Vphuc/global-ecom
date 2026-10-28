# -*- coding: utf-8 -*-
"""Dòng chảy cơ cấu xuất khẩu Việt Nam 1995–2023, 10 ngành (T21).

Hình này trả lời "Việt Nam BÁN GÌ, và cái đó đổi thế nào trong 28 năm". Nó là
nhịp mở của mạch chuyện: rổ hàng đã được xây lại gần như từ đầu, và chính chỗ
xây lại ấy dẫn tới đề xuất ở T31.

Vì sao KHÔNG vẽ streamgraph đường nền lượn theo kiểu ThemeRiver
---------------------------------------------------------------
Đã thử và bỏ, vì một lý do đo được chứ không phải vì thẩm mỹ: tổng xuất khẩu
1995 là 5,1 tỷ USD còn 2023 là 385,5 tỷ, gấp **75 lần**. Trên bất kỳ trục tuyến
tính nào — đường nền lượn hay không — bề dày năm 1995 chỉ còn khoảng 1,3% chiều
cao khung, tức mỏng hơn một nét bút. Cơ cấu của đầu kỳ, thứ mà hình này sinh ra
để kể, sẽ không nhìn thấy gì cả.

Nên chia làm hai tầng, mỗi tầng trả lời đúng một câu:

* **Tầng trên** — tổng xuất khẩu theo giá trị tuyệt đối. Trả lời "lớn lên bao
  nhiêu", và chỉ cần một dải mỏng là đủ.
* **Tầng dưới** — cùng dữ liệu nhưng chuẩn hóa về 100%. Trả lời "đổi cơ cấu thế
  nào", và vì đã bỏ quy mô đi nên năm 1995 đọc được ngang năm 2023.

Mất gì khi tách: không đọc được trực tiếp giá trị tuyệt đối của từng ngành. Đổi
lại là thứ quan trọng hơn ở đây — hai câu hỏi không còn giẫm lên nhau.

Nhãn ngành dán thẳng lên dải, không dùng chú giải: mắt khỏi phải nhảy đi nhảy
lại giữa dải và bảng màu. Dải nào mỏng quá không dán được thì kể tên ở ghi chú.

Chạy
----
    python src/make_streamgraph.py
    python src/make_streamgraph.py --from-year 2005
"""

from __future__ import print_function

import argparse
import os
import sys

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_data as R  # noqa: E402

DATA = os.path.join("data", "processed")
OUTDIR = "output"
FOCUS = "VNM"

PT_PER_INCH = 72.0
CANVAS_PT = R.FIG_WIDTH_FULL * PT_PER_INCH
CANVAS_H = 390.0
MARGIN_X = 10.0
MARGIN_L = 34.0
TEXT_PAD = 6.0
LINE_H = 1.33
LABEL_FLOOR_PT = 7.0

LABEL_MIN_SHARE = 6.0     # dải mỏng hơn mức này thì không dán nhãn lên được
GRID = "#E6E6E6"
TEXT_DIM = "#555555"

SOURCE_TEXT = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab), "
               "xuất khẩu theo nhóm HS92 gộp lên 10 ngành cấp 1.")


def load(from_year, to_year):
    tree = pd.read_csv(os.path.join(DATA, "tree.csv"))
    cp = pd.read_csv(os.path.join(DATA, "country_product.csv"))
    cp = cp[(cp["country_iso3"] == FOCUS) & (cp["year"] >= from_year)
            & (cp["year"] <= to_year)].copy()
    cp["sector_id"] = cp["product_id"].map(
        tree.set_index("product_id")["sector_id"])
    wide = cp.pivot_table(index="year", columns="sector_id",
                          values="export_value", aggfunc="sum").fillna(0.0)
    wide = wide.sort_index()
    return wide


def biggest_moves(share):
    """Ngành lên nhiều nhất và xuống nhiều nhất, tính bằng điểm phần trăm."""
    d = share.iloc[-1] - share.iloc[0]
    return int(d.idxmax()), float(d.max()), int(d.idxmin()), float(d.min())


def headline(wide, share):
    y0, y1 = int(share.index[0]), int(share.index[-1])
    up, dup, dn, ddn = biggest_moves(share)
    tot0, tot1 = float(wide.iloc[0].sum()), float(wide.iloc[-1].sum())
    up_vi = R.SECTOR_NAME_VI.get(up, str(up))
    dn_vi = R.SECTOR_NAME_VI.get(dn, str(dn))
    title = ("Rổ hàng được xây lại: %s từ %s lên %s, %s từ %s xuống %s"
             % (up_vi, R.fmt_pct(share.iloc[0][up]),
                R.fmt_pct(share.iloc[-1][up]), dn_vi,
                R.fmt_pct(share.iloc[0][dn]), R.fmt_pct(share.iloc[-1][dn])))
    sub = ("Việt Nam %d–%d: tổng xuất khẩu %s → %s, gấp %s lần. Tầng trên là "
           "quy mô, tầng dưới là cùng dữ liệu chuẩn hóa về 100%% — phải tách "
           "ra vì ở thang tuyến tính, cơ cấu năm %d chỉ còn dày %s khung."
           % (y0, y1, R.fmt_usd(tot0), R.fmt_usd(tot1),
              R.fmt_vn(tot1 / tot0, 0), y0, R.fmt_pct(tot0 / tot1 * 100.0)))
    return title, sub


def build(wide, share, thin_names):
    title, sub = headline(wide, share)
    t_w = CANVAS_PT - MARGIN_L - MARGIN_X - 2 * TEXT_PAD
    title_w = R.wrap_pt(title, R.FONT_SIZES["title"], t_w)
    sub_w = R.wrap_pt(sub, R.FONT_SIZES["subtitle"], t_w)
    note = ("Màu là ngành hàng, cùng bảng màu với mọi hình khác của đồ án. "
            "Dải quá mỏng nên không dán được nhãn: %s. Tỷ trọng tính trên giá "
            "trị xuất khẩu, không phải số mặt hàng." % thin_names)
    note_w = R.wrap_pt(note, R.FONT_SIZES["annotation"], t_w)
    src_w = R.wrap_pt(SOURCE_TEXT, R.FONT_SIZES["footnote"], t_w)

    m_t = (TEXT_PAD + R.n_lines(title_w) * R.FONT_SIZES["title"] * LINE_H
           + R.n_lines(sub_w) * R.FONT_SIZES["subtitle"] * LINE_H
           + 2 * TEXT_PAD)
    m_b = (22.0 + R.n_lines(note_w) * R.FONT_SIZES["annotation"] * LINE_H
           + R.n_lines(src_w) * R.FONT_SIZES["footnote"] * LINE_H + TEXT_PAD)
    plot_h = CANVAS_H - m_t - m_b

    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.24, 0.76], vertical_spacing=0.05)

    years = [int(y) for y in wide.index]
    total = (wide.sum(axis=1) / 1e9).tolist()
    fig.add_trace(go.Scatter(
        x=years, y=total, mode="lines", fill="tozeroy",
        line=dict(color="#4A4A4A", width=1.0), fillcolor="#D9D9D9",
        hovertemplate="%{x}<br>%{y:.1f} tỷ USD<extra></extra>",
        showlegend=False), row=1, col=1)

    # Thứ tự xếp chồng: ngành giảm mạnh nhất nằm dưới cùng, tăng mạnh nhất trên
    # cùng. Nhờ vậy chỗ giao nhau của hai xu thế nằm giữa khung, đúng chỗ mắt
    # nhìn vào đầu tiên, thay vì bị đẩy ra rìa.
    order = (share.iloc[-1] - share.iloc[0]).sort_values().index.tolist()
    for sid in order:
        fig.add_trace(go.Scatter(
            x=years, y=share[sid].tolist(), mode="lines",
            stackgroup="one", line=dict(width=0.4, color="#FFFFFF"),
            fillcolor=R.SECTOR_PALETTE[int(sid)],
            name=R.SECTOR_NAME_VI.get(int(sid), str(sid)),
            hovertemplate=("%{x}<br>" + R.SECTOR_NAME_VI.get(int(sid), str(sid))
                           + " %{y:.1f}%<extra></extra>"),
            showlegend=False), row=2, col=1)

    # nhãn dán thẳng lên dải, ở năm dải đó dày nhất
    cum = share[order].cumsum(axis=1)
    for sid in order:
        s = share[sid]
        if s.max() < LABEL_MIN_SHARE:
            continue
        yr = s.idxmax()
        mid = cum.loc[yr, sid] - s.loc[yr] / 2.0
        # Dải dày nhất ở ngay mép khung thì nhãn căn giữa sẽ bị cắt mất nửa:
        # "Nông sản, gỗ và giấy" dày nhất đúng năm 1995 nên chỉ còn "gỗ và giấy".
        if int(yr) == years[0]:
            xa = "left"
        elif int(yr) == years[-1]:
            xa = "right"
        else:
            xa = "center"
        fig.add_annotation(
            x=int(yr), y=mid, xref="x2", yref="y2",
            text=R.SECTOR_NAME_VI.get(int(sid), str(sid)),
            showarrow=False, xanchor=xa, yanchor="middle",
            xshift=2 if xa == "left" else (-2 if xa == "right" else 0),
            font=dict(size=LABEL_FLOOR_PT,
                      color=R.SECTOR_TEXT_ON_FILL.get(int(sid), "#000000")))

    tick_years = [y for y in R.MILESTONE_YEARS if y in years]
    fig.update_xaxes(tickmode="array", tickvals=tick_years,
                     ticktext=[str(y) for y in tick_years],
                     tickfont=dict(size=R.FONT_SIZES["tick"]),
                     gridcolor=GRID, zeroline=False, row=2, col=1)
    fig.update_xaxes(showticklabels=False, gridcolor=GRID, row=1, col=1)
    fig.update_yaxes(title=dict(text="tỷ USD",
                                font=dict(size=R.FONT_SIZES["axis"])),
                     tickfont=dict(size=R.FONT_SIZES["tick"]),
                     gridcolor=GRID, zeroline=False, row=1, col=1)
    fig.update_yaxes(title=dict(text="phần trăm rổ hàng",
                                font=dict(size=R.FONT_SIZES["axis"])),
                     range=[0, 100], tickmode="array",
                     tickvals=[0, 25, 50, 75, 100],
                     ticktext=[R.fmt_pct(v, 0) for v in (0, 25, 50, 75, 100)],
                     tickfont=dict(size=R.FONT_SIZES["tick"]),
                     gridcolor=GRID, zeroline=False, row=2, col=1)
    fig.update_layout(
        font=dict(family=", ".join(R.FONT_STACK),
                  size=R.FONT_SIZES["annotation"]),
        separators=",.",
        margin=dict(l=MARGIN_L, r=MARGIN_X, t=m_t, b=m_b),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        hovermode="x unified", showlegend=False)

    def block(txt, y_from_top, size, color=None):
        fig.add_annotation(text=txt, showarrow=False, xref="paper",
                           yref="paper", x=0,
                           y=1 + (m_t - y_from_top) / plot_h,
                           xshift=-(MARGIN_L - TEXT_PAD), xanchor="left",
                           yanchor="top", align="left",
                           font=dict(size=size, color=color))

    block(title_w, TEXT_PAD, R.FONT_SIZES["title"])
    block(sub_w, TEXT_PAD + R.n_lines(title_w) * R.FONT_SIZES["title"] * LINE_H,
          R.FONT_SIZES["subtitle"], TEXT_DIM)

    def bottom(txt, y_from_plot, size, color):
        fig.add_annotation(text=txt, showarrow=False, xref="paper",
                           yref="paper", x=0, y=-(y_from_plot / plot_h),
                           xshift=-(MARGIN_L - TEXT_PAD), xanchor="left",
                           yanchor="top", align="left",
                           font=dict(size=size, color=color))

    bottom(note_w, 22.0, R.FONT_SIZES["annotation"], TEXT_DIM)
    bottom(src_w, 22.0 + R.n_lines(note_w) * R.FONT_SIZES["annotation"] * LINE_H,
           R.FONT_SIZES["footnote"], "#777777")
    return fig


def save(fig, name):
    os.makedirs(OUTDIR, exist_ok=True)
    html = os.path.join(OUTDIR, name + ".html")
    fig.write_html(html, include_plotlyjs="cdn",
                   config={"displayModeBar": False})
    print("  %s" % html)
    try:
        png = os.path.join(OUTDIR, name + ".png")
        fig.write_image(png, width=int(round(CANVAS_PT)),
                        height=int(round(CANVAS_H)),
                        scale=(R.FIG_WIDTH_FULL * R.FIG_DPI_PRINT)
                              / round(CANVAS_PT))
        print("  %s" % png)
    except Exception as exc:
        print("  (không xuất được PNG: %s)" % exc)


def report(wide, share):
    print("\n" + "=" * 70)
    print("KIỂM CHỨNG — dòng chảy cơ cấu xuất khẩu Việt Nam")
    print("=" * 70)
    y0, y1 = int(share.index[0]), int(share.index[-1])
    tot0, tot1 = float(wide.iloc[0].sum()), float(wide.iloc[-1].sum())
    print("  %d–%d, %s năm liên tục, %s ngành cấp 1"
          % (y0, y1, R.fmt_vn(len(share), 0), R.fmt_vn(share.shape[1], 0)))
    print("  Tổng xuất khẩu %s → %s, gấp %s lần"
          % (R.fmt_usd(tot0, 2), R.fmt_usd(tot1, 2),
             R.fmt_vn(tot1 / tot0, 1)))
    print("  Cơ cấu năm %d chiếm %s chiều cao nếu vẽ chung thang tuyến tính "
          "— lý do tách hai tầng" % (y0, R.fmt_pct(tot0 / tot1 * 100.0)))

    print("\n  Tỷ trọng theo ngành ở các năm mốc:")
    cols = [y for y in R.MILESTONE_YEARS if y in share.index]
    hdr = "    %-26s" % "ngành" + "".join("%9s" % y for y in cols) + "   đổi"
    print(hdr)
    for sid in (share.iloc[-1] - share.iloc[0]).sort_values(
            ascending=False).index:
        nm = R.SECTOR_NAME_VI.get(int(sid), str(sid))
        row = "    %-26s" % nm[:26]
        for y in cols:
            row += "%9s" % R.fmt_pct(share.loc[y, sid])
        d = share.iloc[-1][sid] - share.iloc[0][sid]
        row += "  %+6.1f đ%%" % d
        print(row)

    bad = share.sum(axis=1)
    print("\n  Mỗi năm tỷ trọng có cộng đủ 100%% không? lệch lớn nhất %s"
          % R.fmt_vn(float((bad - 100.0).abs().max()), 6))
    assert float((bad - 100.0).abs().max()) < 1e-6, "tỷ trọng không khớp 100%"
    up, dup, dn, ddn = biggest_moves(share)
    print("  Lên nhiều nhất: %s %+.1f điểm %%  ·  xuống nhiều nhất: %s %+.1f điểm %%"
          % (R.SECTOR_NAME_VI.get(up, up), dup,
             R.SECTOR_NAME_VI.get(dn, dn), ddn))
    thin = [R.SECTOR_NAME_VI.get(int(s), str(s)) for s in share.columns
            if share[s].max() < LABEL_MIN_SHARE]
    print("  Dải quá mỏng không dán nhãn (%s): %s"
          % (R.fmt_vn(len(thin), 0), ", ".join(thin) if thin else "không có"))
    return thin


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from-year", type=int, default=1995)
    ap.add_argument("--to-year", type=int, default=R.REFERENCE_YEAR)
    a = ap.parse_args()

    wide = load(a.from_year, a.to_year)
    share = wide.div(wide.sum(axis=1), axis=0) * 100.0
    thin = report(wide, share)
    fig = build(wide, share, ", ".join(thin) if thin else "không có")
    print("\nĐã dựng dòng chảy cơ cấu %d–%d:" % (a.from_year, a.to_year))
    save(fig, "stream_sectors_%d_%d" % (a.from_year, a.to_year))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Phần giá trị xuất khẩu làm ra trong nước, theo ngành hàng (A19, B27, B28).

Hình này trả lời câu hỏi mà ECI không trả lời được: hàng *đi qua* Việt Nam thì
thấy rồi, nhưng bao nhiêu trong đó *ở lại*? Mỗi thanh là một trong chín ngành, dài
bằng phần trăm giá trị của hàng xuất khẩu được tạo ra bên trong lãnh thổ (còn lại
là linh kiện, nguyên liệu nhập về). Số lấy từ OECD TiVA 2025, ghép sang ngành của
Atlas qua nhóm HS2 (xem ``map_sector_isic.py``).

Vì sao xếp theo PCI chứ không theo độ dài thanh
-----------------------------------------------
Câu hỏi của đồ án là *hàng càng khó thì có càng ít ở lại không*. Xếp từ ngành khó
nhất (PCI cao) xuống ngành dễ nhất thì câu trả lời hiện ra như một dốc: bốn thanh
đầu cùng ngắn. Xếp theo độ dài thì dốc ấy biến mất và hình chỉ còn là một bảng
xếp hạng. Mất gì: không thấy ngay ngành nào giữ nhiều nhất; đổi lại là cột PCI
nằm ngay cạnh để đối chiếu.

Hai thứ nhỏ cần đọc cho đúng
----------------------------
* Vạch mảnh trên thanh là khoảng giữa hai cách ghép HS2 → ISIC (cột ``lo``, ``hi``).
  Máy móc chỉ dao động 46,2–47,5%, nên chênh 3 điểm so với điện tử nằm trong sai số.
* Ngành "Khác" (HS99, HS97) không ghép được nên không có thanh.

Chạy
----
    python src/map_sector_isic.py          # tạo data/processed/sector_dva_2022.csv
    python src/make_dva_sector.py
    python src/make_dva_sector.py --year 2015   # năm đối chứng (cần map_sector_isic --year 2015)
"""

from __future__ import print_function

import argparse
import os
import sys

import pandas as pd
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_data as R  # noqa: E402

DATA = os.path.join("data", "processed")
OUTDIR = "output"

PT_PER_INCH = 72.0
CANVAS_PT = R.FIG_WIDTH_FULL * PT_PER_INCH
ROW_PT = 24.0                 # chiều cao một hàng thanh
MARGIN_L = 128.0              # chỗ cho tên ngành
MARGIN_R = 96.0               # chỗ cho hai cột chữ bên phải: phần giữ lại và PCI
MARGIN_X = 10.0
TEXT_PAD = 6.0
LINE_H = 1.33
LABEL_FLOOR_PT = 7.0
TOP_N = 4                     # "hàng khó" = bốn ngành PCI cao nhất (khớp báo cáo §6.2)

TEXT = "#1A1A1A"
TEXT_DIM = "#555555"
REF_LINE = "#555555"
WHISKER = "#333333"

SOURCE_TEXT = ("Nguồn: OECD TiVA 2025 (EXGR_DVA) ghép sang ngành Atlas qua HS2 "
               "(data/reference/hs2_to_isic4.csv); PCI từ Atlas of Economic "
               "Complexity.")


def signed(x, nd=2):
    return "%s%s" % ("+" if x >= 0 else "−", R.fmt_vn(abs(x), nd))


def load(year):
    path = os.path.join(DATA, "sector_dva_%d.csv" % year)
    hp = os.path.join(DATA, "tiva_headline_%d.csv" % year)
    for p in (path, hp):
        if not os.path.exists(p):
            raise SystemExit("thiếu %s — chạy: python src/map_sector_isic.py --year %d"
                             % (p, year))
    s = pd.read_csv(path)
    h = pd.read_csv(hp).set_index("key")["value"]
    return s.sort_values("pci", ascending=False).reset_index(drop=True), h


def headline(s, h):
    """Tiêu đề dựng từ dữ liệu: bốn ngành khó nhất so với mức bình quân cả rổ."""
    top = s.head(TOP_N)
    lo, hi = top["dva_pct"].min(), top["dva_pct"].max()
    avg = float(h["dva_rb"])
    if hi < avg:
        so = "đều thấp hơn mức bình quân %s của cả rổ hàng" % R.fmt_pct(avg)
    elif lo > avg:
        so = "đều cao hơn mức bình quân %s của cả rổ hàng" % R.fmt_pct(avg)
    else:
        so = "so với mức bình quân %s của cả rổ hàng" % R.fmt_pct(avg)
    return ("Bốn ngành hàng khó nhất giữ lại %s–%s giá trị xuất khẩu, %s"
            % (R.fmt_vn(lo, 1), R.fmt_pct(hi), so)), lo, hi, avg


def build(s, h, year):
    title, lo4, hi4, avg = headline(s, h)
    sub = ("Phần giá trị của hàng xuất khẩu được làm ra trong lãnh thổ Việt Nam, "
           "theo ngành, năm %d. Xếp từ ngành khó nhất (PCI cao) xuống ngành dễ "
           "nhất; mỗi ngành tính trên xuất khẩu gộp của nó." % year)
    note = ("Vạch mảnh là khoảng giữa hai cách ghép sang ngành ISIC của OECD. Chưa "
            "tính ngành Khác (%s xuất khẩu: HS99 và HS97 không ghép được). TiVA "
            "dừng ở %d nên hình lấy %d, không phải năm tham chiếu %d."
            % (R.fmt_pct(float(h["khac_pct"])), year, year, R.REFERENCE_YEAR))

    t_w = CANVAS_PT - MARGIN_X - MARGIN_X - 2 * TEXT_PAD
    title_w = R.wrap_pt(title, R.FONT_SIZES["title"], t_w)
    sub_w = R.wrap_pt(sub, R.FONT_SIZES["subtitle"], t_w)
    note_w = R.wrap_pt(note, R.FONT_SIZES["annotation"], t_w)
    src_w = R.wrap_pt(SOURCE_TEXT, R.FONT_SIZES["footnote"], t_w)

    m_t = (TEXT_PAD + R.n_lines(title_w) * R.FONT_SIZES["title"] * LINE_H
           + R.n_lines(sub_w) * R.FONT_SIZES["subtitle"] * LINE_H
           + 2 * TEXT_PAD + 22.0)               # 22: chỗ cho nhãn vạch bình quân
    m_b = (22.0 + R.n_lines(note_w) * R.FONT_SIZES["annotation"] * LINE_H
           + R.n_lines(src_w) * R.FONT_SIZES["footnote"] * LINE_H + TEXT_PAD)
    plot_h = ROW_PT * len(s)
    canvas_h = m_t + plot_h + m_b

    names = list(s["ten"])
    dva = list(s["dva_pct"])
    err_up = [max(0.0, hi - v) for hi, v in zip(s["hi"], dva)]
    err_dn = [max(0.0, v - lo) for lo, v in zip(s["lo"], dva)]
    fig = go.Figure(go.Bar(
        x=dva, y=names, orientation="h",
        marker=dict(color=[R.SECTOR_PALETTE[int(i)] for i in s["sector_id"]],
                    line=dict(color="#FFFFFF", width=1)),
        error_x=dict(type="data", symmetric=False, array=err_up, arrayminus=err_dn,
                     color=WHISKER, thickness=1, width=3),
        customdata=[[R.fmt_vn(lo, 1), R.fmt_pct(hi), signed(p), R.fmt_pct(sh),
                     R.fmt_pct(v)]
                    for lo, hi, p, sh, v in zip(s["lo"], s["hi"], s["pci"],
                                                s["share_of_mapped_pct"], dva)],
        hovertemplate=("<b>%{y}</b><br>Giữ lại trong nước: %{customdata[4]}<br>"
                       "Khoảng theo hai cách ghép: %{customdata[0]}–%{customdata[1]}"
                       "<br>PCI %{customdata[2]} · %{customdata[3]} xuất khẩu"
                       "<extra></extra>"),
        showlegend=False))

    fig.update_xaxes(range=[0, 100], tickvals=[0, 25, 50, 75, 100],
                     ticktext=[R.fmt_vn(v, 0) + "%" for v in (0, 25, 50, 75, 100)],
                     tickfont=dict(size=R.FONT_SIZES["tick"], color=TEXT_DIM),
                     showgrid=False, zeroline=False, ticks="", fixedrange=True)
    fig.update_yaxes(autorange="reversed", tickfont=dict(size=R.FONT_SIZES["annotation"],
                                                         color=TEXT),
                     showgrid=False, zeroline=False, ticks="", ticklabelstandoff=4,
                     fixedrange=True)
    fig.update_layout(
        font=dict(family=", ".join(R.FONT_STACK), size=R.FONT_SIZES["annotation"]),
        separators=",.", bargap=0.34,
        margin=dict(l=MARGIN_L, r=MARGIN_R, t=m_t, b=m_b),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", showlegend=False,
        shapes=[dict(type="line", xref="x", yref="paper", x0=avg, x1=avg, y0=0, y1=1,
                     line=dict(color=REF_LINE, width=1, dash="dash"))])

    # vạch bình quân + cột PCI
    fig.add_annotation(text="Bình quân cả rổ <b>%s</b>" % R.fmt_pct(avg),
                       xref="x", yref="paper", x=avg, y=1, yshift=4, showarrow=False,
                       xanchor="center", yanchor="bottom",
                       font=dict(size=R.FONT_SIZES["annotation"], color=REF_LINE))
    # Hai cột chữ bên phải thay cho nhãn đầu thanh: nhãn đầu thanh va vào vạch
    # khoảng và vạch bình quân, còn cột thì không đè lên gì.
    for dich, tieu in ((6, "Giữ lại"), (58, "PCI")):
        fig.add_annotation(text=tieu, xref="paper", yref="paper", x=1, y=1,
                           xshift=dich, yshift=4, showarrow=False, xanchor="left",
                           yanchor="bottom",
                           font=dict(size=R.FONT_SIZES["annotation"], color=TEXT_DIM))
    for ten, v, p in zip(names, dva, s["pci"]):
        fig.add_annotation(text="<b>%s</b>" % R.fmt_pct(v), xref="paper", yref="y",
                           x=1, y=ten, xshift=6, showarrow=False, xanchor="left",
                           font=dict(size=R.FONT_SIZES["annotation"], color=TEXT))
        fig.add_annotation(text=signed(p), xref="paper", yref="y", x=1, y=ten,
                           xshift=58, showarrow=False, xanchor="left",
                           font=dict(size=R.FONT_SIZES["annotation"], color=TEXT_DIM))

    def block(txt, y_from_top, size, color=None):
        fig.add_annotation(text=txt, showarrow=False, xref="paper", yref="paper",
                           x=0, y=1 + (m_t - y_from_top) / plot_h,
                           xshift=-(MARGIN_L - TEXT_PAD), xanchor="left",
                           yanchor="top", align="left",
                           font=dict(size=size, color=color))

    block(title_w, TEXT_PAD, R.FONT_SIZES["title"])
    block(sub_w, TEXT_PAD + R.n_lines(title_w) * R.FONT_SIZES["title"] * LINE_H,
          R.FONT_SIZES["subtitle"], TEXT_DIM)

    def bottom(txt, y_from_plot, size, color):
        fig.add_annotation(text=txt, showarrow=False, xref="paper", yref="paper",
                           x=0, y=-(y_from_plot / plot_h),
                           xshift=-(MARGIN_L - TEXT_PAD), xanchor="left",
                           yanchor="top", align="left",
                           font=dict(size=size, color=color))

    bottom(note_w, 22.0, R.FONT_SIZES["annotation"], TEXT_DIM)
    bottom(src_w, 22.0 + R.n_lines(note_w) * R.FONT_SIZES["annotation"] * LINE_H,
           R.FONT_SIZES["footnote"], "#777777")
    return fig, title, canvas_h


def save(fig, name, canvas_h):
    os.makedirs(OUTDIR, exist_ok=True)
    html = os.path.join(OUTDIR, name + ".html")
    fig.write_html(html, include_plotlyjs="cdn", config={"displayModeBar": False})
    print("  %s" % html)
    try:
        png = os.path.join(OUTDIR, name + ".png")
        fig.write_image(png, width=int(round(CANVAS_PT)), height=int(round(canvas_h)),
                        scale=(R.FIG_WIDTH_FULL * R.FIG_DPI_PRINT) / round(CANVAS_PT))
        print("  %s" % png)
    except Exception as exc:
        print("  (không xuất được PNG: %s)" % exc)


def report(s, h, year, title):
    print("\n" + "=" * 72)
    print("KIỂM CHỨNG — phần giá trị làm ra trong nước theo ngành, %d" % year)
    print("=" * 72)
    print("  Tiêu đề: %s" % title)
    print("\n  %-30s %8s %-13s %6s %8s" % ("Ngành (xếp theo PCI)", "Trong nước",
                                          "Khoảng", "PCI", "Xuất khẩu"))
    for _, r in s.iterrows():
        print("  %-30s %8s %6s–%-6s %6s %8s" % (
            r["ten"], R.fmt_pct(r["dva_pct"]), R.fmt_vn(r["lo"], 1), R.fmt_pct(r["hi"]),
            signed(r["pci"]), R.fmt_pct(r["share_of_mapped_pct"])))

    # tái tính bình quân cả rổ từ chính các thanh, đối chiếu file tiêu đề
    avg = (s["dva_pct"] * s["export_usd"]).sum() / s["export_usd"].sum()
    top = s.head(TOP_N)
    print("\n  Bình quân gia quyền chín ngành: %s (file tiêu đề: %s) → %s"
          % (R.fmt_pct(avg), R.fmt_pct(float(h["dva_rb"])),
             "khớp" if abs(avg - float(h["dva_rb"])) < 0.05 else "LỆCH"))
    print("  %d ngành PCI cao nhất: %s; chiếm %s xuất khẩu ghép được; %s–%s"
          % (TOP_N, ", ".join(top["ten"]), R.fmt_pct(top["share_of_mapped_pct"].sum()),
             R.fmt_vn(top["dva_pct"].min(), 1), R.fmt_pct(top["dva_pct"].max())))
    print("  Spearman PCI × tỷ lệ trong nước (mức ISIC, n=%d): %s, p=%s"
          % (int(h["n_isic"]), signed(float(h["rho"])), R.fmt_vn(float(h["p"]), 3)))
    assert ((s["dva_pct"] >= 0) & (s["dva_pct"] <= 100)).all()
    assert (s["lo"] <= s["dva_pct"] + 1e-9).all() and (s["dva_pct"] <= s["hi"] + 1e-9).all()
    print("  Mọi thanh trong [0; 100] và nằm trong khoảng của chính nó: đạt")
    print("=" * 72)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--year", type=int, default=2022)
    a = ap.parse_args()
    s, h = load(a.year)
    fig, title, canvas_h = build(s, h, a.year)
    print("Đã dựng hình phần giá trị trong nước theo ngành:")
    save(fig, "dva_sectors_%d" % a.year, canvas_h)
    report(s, h, a.year, title)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Mặt phẳng quyết định: nên dồn sức vào nhóm hàng nào (T31).

Đây là hình mang **đề xuất** của báo cáo. Mọi hình trước mô tả cấu trúc; hình này
phải chỉ ra một việc nên làm, và chỉ ra bằng số đo được chứ không bằng cảm tính.

Hai trục, cả hai đều lấy thẳng từ Atlas, không tự chế:

* **RCA** (*revealed comparative advantage* — lợi thế so sánh hiện hữu): tỷ trọng
  một mặt hàng trong rổ xuất khẩu của Việt Nam, chia cho tỷ trọng của chính mặt
  hàng đó trong rổ xuất khẩu thế giới. Lớn hơn 1 nghĩa là Việt Nam bán mặt hàng
  đó **đậm hơn mức trung bình thế giới**. Trục ngang để thang log vì 1 là mốc
  trung tính, nửa dưới và nửa trên phải cân nhau về thị giác.
* **PCI** (*product complexity index* — độ phức tạp của mặt hàng): đo mặt hàng đó
  thường do những nước có rổ hàng đa dạng và hiếm làm ra hay không. Cao nghĩa là
  làm được nó cần nhiều năng lực tích luỹ. Mốc 0 là mức trung bình thế giới.

Giao của hai mốc chia mặt phẳng làm bốn góc, và bốn góc có nghĩa rất khác nhau:

===============  ==========================================================
Góc              Đọc là gì
===============  ==========================================================
phải–trên        đã thắng: vừa bán đậm vừa là hàng khó
trái–trên        **cơ hội**: hàng khó, nhưng chưa bán đậm bằng thế giới
phải–dưới        đang kẹt: bán rất đậm nhưng là hàng dễ, ai cũng làm được
trái–dưới        không phải chỗ của mình
===============  ==========================================================

Quy tắc chọn nhóm để đề xuất được viết thành code (``candidates``), không chọn
tay: hàng xuất trên 1 tỷ USD, PCI dương, RCA đang trong dải sát ngưỡng
``[RCA_LO, RCA_HI)`` và RCA **tăng** so với năm so sánh. Trong số đó lấy hai nhóm
PCI cao nhất. Viết thành quy tắc nên chạy năm khác sẽ ra nhóm khác, và hình không
bao giờ in ra một đề xuất mà dữ liệu năm đó không đỡ.

Nhóm ``Other`` bị loại khỏi danh sách đề xuất dù nó rất to: đó là ô gom mã
``XXXX`` chưa phân loại của Atlas, không phải một ngành hàng có thật để mà đầu tư
vào. Nó vẫn được vẽ, vì 11,8% rổ hàng thì không giấu đi được. Xem hạn chế **D4**.

Chạy
----
    python src/make_decision_plane.py
    python src/make_decision_plane.py --year 2015 --since 2007
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
FOCUS = "VNM"

PT_PER_INCH = 72.0
CANVAS_PT = R.FIG_WIDTH_FULL * PT_PER_INCH
CANVAS_H = 470.0
MARGIN_X = 10.0
TEXT_PAD = 6.0
LINE_H = 1.33
LABEL_FLOOR_PT = 7.0

# Quy tắc chọn nhóm đề xuất — đổi ở đây thì đổi cả hình lẫn câu tiêu đề.
MIN_EXPORT = 1e9
RCA_LO, RCA_HI = 0.5, 1.5
N_PICK = 2
N_LABEL = 9
AXIS_BAND = 28.0      # nhãn tick + tên trục
LEG_BAND = 74.0       # chú giải ngành, xếp ngang nên cao 3 hàng
MARGIN_L = 38.0
UNCLASSIFIED = "Other"           # tên NGÀNH cấp 1 trong tree.csv
UNCLASSIFIED_VI = "Chưa phân loại"

GRID = "#E6E6E6"
RULE = "#8A8A8A"
TEXT_DIM = "#555555"
QUAD = "#B4B4B4"
LEADER = "#9A9A9A"

SOURCE_TEXT = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab). "
               "RCA và PCI lấy nguyên từ Atlas, không tự tính lại.")


def load(year, since):
    tree = pd.read_csv(os.path.join(DATA, "tree.csv"))
    cp = pd.read_csv(os.path.join(DATA, "country_product.csv"))
    cp = cp[cp["country_iso3"] == FOCUS]
    meta = tree.set_index("product_id")
    cur = cp[cp["year"] == year].set_index("product_id").copy()
    old = cp[cp["year"] == since].set_index("product_id")
    cur["name"] = meta["name_short"].map(R.ten_nhom)
    cur["sector_id"] = meta["sector_id"]
    cur["sector"] = cur["sector_id"].map(
        tree[tree["level"] == 1].set_index("sector_id")["name_short"])
    cur["rca_old"] = old["rca"]
    cur["exp_old"] = old["export_value"]
    cur = cur[cur["export_value"] > 0].copy()
    cur["share"] = cur["export_value"] / cur["export_value"].sum() * 100.0
    cur["d_rca"] = cur["rca"] - cur["rca_old"]
    return cur.dropna(subset=["rca", "pci"])


def candidates(df):
    """Nhóm đáng dồn sức, theo quy tắc chứ không theo ý thích.

    Sát ngưỡng lợi thế mà chưa vượt là chỗ đáng bỏ tiền nhất: vượt được mốc 1 là
    một thắng lợi nhìn thấy được, trong khi nhóm đã ở RCA 2,2 thì thêm một đồng
    nữa chỉ làm dày thêm chỗ vốn đã dày.
    """
    c = df[(df["export_value"] >= MIN_EXPORT)
           & (df["pci"] > 0)
           & (df["rca"] >= RCA_LO) & (df["rca"] < RCA_HI)
           & (df["d_rca"] > 0)
           & (df["sector"] != UNCLASSIFIED)]
    return c.nlargest(N_PICK, "pci")


def stuck(df):
    """Nhóm bán rất đậm nhưng là hàng dễ — chỗ KHÔNG nên dồn thêm."""
    c = df[(df["export_value"] >= MIN_EXPORT) & (df["rca"] >= 1.0)
           & (df["pci"] < 0) & (df["sector"] != UNCLASSIFIED)]
    return c.nsmallest(3, "pci")


def headline(year, since, df, pick, stk):
    tot = df["export_value"].sum()
    if len(pick) >= 2:
        a, b = pick.iloc[0], pick.iloc[1]
        title = ("Nên dồn sức vào %s và %s: hàng khó nhất trong rổ, và đang sát "
                 "ngưỡng lợi thế" % (a["name"], b["name"]))
    elif len(pick) == 1:
        a = pick.iloc[0]
        title = ("Nên dồn sức vào %s: hàng khó, và đang sát ngưỡng lợi thế"
                 % a["name"])
    else:
        title = ("Năm %d không nhóm nào thoả cả bốn điều kiện đề xuất" % year)

    parts = []
    for _, r in pick.iterrows():
        parts.append("%s (RCA %s → %s, PCI %s)"
                     % (r["name"], R.fmt_vn(r["rca_old"], 2),
                        R.fmt_vn(r["rca"], 2), R.fmt_vn(r["pci"], 2)))
    big = df.nlargest(1, "export_value").iloc[0]
    sub = ("Năm %d: %s. Để so, nhóm lớn nhất là %s — %s rổ hàng, RCA đã %s nên "
           "thêm một đồng vào đó chỉ làm dày chỗ vốn dày."
           % (year, "; ".join(parts) if parts else "không có nhóm nào",
              big["name"], R.fmt_pct(big["share"]), R.fmt_vn(big["rca"], 2)))

    nm = ", ".join(stk["name"].tolist())
    note = ("RCA > 1 là bán đậm hơn mức trung bình thế giới; PCI > 0 là hàng khó "
            "hơn mức trung bình thế giới. Diện tích hình tròn là giá trị xuất "
            "khẩu. Góc phải–dưới là chỗ đang kẹt — %s — bán rất đậm nhưng là "
            "hàng dễ, và tỷ trọng của chúng đang giảm. Ô %s là mã chưa phân loại "
            "của Atlas, không phải một ngành để đầu tư (hạn chế D4)."
            % (nm, UNCLASSIFIED_VI))
    return title, sub, note


def build(year, since, df, pick, stk):
    title, sub, note = headline(year, since, df, pick, stk)
    t_w = CANVAS_PT - 2 * MARGIN_X - 2 * TEXT_PAD
    title_w = R.wrap_pt(title, R.FONT_SIZES["title"], t_w)
    sub_w = R.wrap_pt(sub, R.FONT_SIZES["subtitle"], t_w)
    note_w = R.wrap_pt(note, R.FONT_SIZES["annotation"], t_w)
    src_w = R.wrap_pt(SOURCE_TEXT, R.FONT_SIZES["footnote"], t_w)

    m_t = (TEXT_PAD + R.n_lines(title_w) * R.FONT_SIZES["title"] * LINE_H
           + R.n_lines(sub_w) * R.FONT_SIZES["subtitle"] * LINE_H
           + 2 * TEXT_PAD)
    m_b = (AXIS_BAND + LEG_BAND
           + R.n_lines(note_w) * R.FONT_SIZES["annotation"] * LINE_H
           + R.n_lines(src_w) * R.FONT_SIZES["footnote"] * LINE_H + TEXT_PAD)
    plot_h = CANVAS_H - m_t - m_b

    picked = set(pick.index)
    stuck_ix = set(stk.index)
    fig = go.Figure()

    # một vệt cho mỗi ngành: màu = ngành, đúng quy ước §3.1, không mở bảng mới
    sizeref = 2.0 * df["export_value"].max() / (28.0 ** 2)
    for sid, grp in df.groupby("sector_id"):
        name_vi = R.SECTOR_NAME_VI.get(int(sid), grp["sector"].iloc[0])
        fig.add_trace(go.Scatter(
            x=grp["rca"], y=grp["pci"], mode="markers",
            name=name_vi, legendgroup=str(sid),
            marker=dict(size=grp["export_value"], sizemode="area",
                        sizeref=sizeref, sizemin=1.6,
                        color=R.SECTOR_PALETTE[int(sid)],
                        line=dict(color="#FFFFFF", width=0.6)),
            customdata=grp[["name", "share", "rca", "pci"]].values,
            hovertemplate=("<b>%{customdata[0]}</b><br>"
                           "tỷ trọng %{customdata[1]:.1f}%<br>"
                           "RCA %{customdata[2]:.2f} · PCI %{customdata[3]:.2f}"
                           "<extra></extra>")))

    # đường mốc: RCA = 1 và PCI = 0
    fig.add_vline(x=1.0, line=dict(color=RULE, width=0.9, dash="dash"))
    fig.add_hline(y=0.0, line=dict(color=RULE, width=0.9, dash="dash"))

    # quỹ đạo của hai nhóm được đề xuất: chấm rỗng là năm so sánh
    for _, r in pick.iterrows():
        if pd.notna(r["rca_old"]) and r["rca_old"] > 0:
            fig.add_trace(go.Scatter(
                x=[r["rca_old"], r["rca"]], y=[r["pci"], r["pci"]],
                mode="lines", line=dict(color="#000000", width=0.9),
                hoverinfo="skip", showlegend=False))
            fig.add_trace(go.Scatter(
                x=[r["rca_old"]], y=[r["pci"]], mode="markers",
                marker=dict(size=5, color="#FFFFFF",
                            line=dict(color="#000000", width=0.9)),
                hoverinfo="skip", showlegend=False))

    # vòng đen làm nổi hai nhóm đề xuất — B12, nổi bằng hình chứ không bằng màu
    if len(pick):
        fig.add_trace(go.Scatter(
            x=pick["rca"], y=pick["pci"], mode="markers",
            marker=dict(size=14, color="rgba(0,0,0,0)",
                        line=dict(color=R.HIGHLIGHT_STROKE,
                                  width=R.HIGHLIGHT_STROKE_WIDTH)),
            hoverinfo="skip", showlegend=False))

    xs = [0.04, 12.0]
    ys = [min(-2.3, df["pci"].min() - 0.15), max(1.5, df["pci"].max() + 0.25)]

    # chữ góc: đọc hình trước khi đọc chú thích
    corners = [
        (xs[0], ys[1], "left", "top",
         "hàng khó, chưa bán đậm<br>— CHỖ ĐÁNG ĐẦU TƯ"),
        (xs[1], ys[1], "right", "top", "hàng khó, đã bán đậm<br>— đã thắng"),
        (xs[1], ys[0], "right", "bottom", "hàng dễ, bán rất đậm<br>— đang kẹt"),
        (xs[0], ys[0], "left", "bottom", "hàng dễ, không bán đậm")]
    for x, y, xa, ya, txt in corners:
        fig.add_annotation(x=_lg(x), y=y, xref="x", yref="y", text=txt,
                           showarrow=False, xanchor=xa, yanchor=ya,
                           align=xa, font=dict(size=LABEL_FLOOR_PT, color=QUAD))

    # Nhãn mặt hàng: nhóm to nhất, cộng hai nhóm đề xuất và ba nhóm đang kẹt.
    #
    # Phải tự giải va chạm. Ở đây các chấm đáng dán nhãn lại chụm vào đúng một
    # chỗ — quanh RCA = 1, PCI ≈ 0,9 — nên để plotly đặt thì ba nhãn quan trọng
    # nhất chồng lên nhau. Quy đổi toạ độ dữ liệu ra point, thử lần lượt vài mức
    # xê dịch, nhãn nào không tìm được chỗ trống thì BỎ chứ không chồng; riêng
    # hai nhóm đề xuất luôn được xếp trước nên chắc chắn có chỗ.
    plot_w = CANVAS_PT - MARGIN_L - MARGIN_X
    lx0, lx1 = _lg(xs[0]), _lg(xs[1])

    def to_pt(rca, pci):
        return ((_lg(rca) - lx0) / (lx1 - lx0) * plot_w,
                (ys[1] - pci) / (ys[1] - ys[0]) * plot_h)

    show = list(pick.index) + [i for i in
                               df.nlargest(N_LABEL, "export_value").index
                               if i not in picked]
    show += [i for i in stuck_ix if i not in show]
    lab_h = LABEL_FLOOR_PT * LINE_H

    # Chữ bốn góc và hai vòng đen làm nổi cũng chiếm chỗ. Nạp sẵn chúng vào danh
    # sách ô đã dùng, nếu không nhãn mặt hàng sẽ đè lên đúng hai thứ dùng để
    # dẫn mắt người đọc.
    placed = []
    for x, y, xa, ya, txt in corners:
        lines = txt.split("<br>")
        w = max(len(t) for t in lines) * LABEL_FLOOR_PT * 0.52
        h = len(lines) * lab_h
        cx = 0.0 if xa == "left" else plot_w - w
        cy = 0.0 if ya == "top" else plot_h - h
        placed.append((cx, cy, cx + w, cy + h))
    for ix in pick.index:
        r = df.loc[ix]
        px, py = to_pt(r["rca"], r["pci"])
        placed.append((px - 9.0, py - 9.0, px + 9.0, py + 9.0))

    for ix in show:
        r = df.loc[ix]
        em = ix in picked
        txt = r["name"]
        w = max(12.0, len(txt) * LABEL_FLOOR_PT * 0.52)
        px, py = to_pt(r["rca"], r["pci"])
        spot = None
        for d in (0.0, -11.0, 20.0, -22.0, 31.0, -33.0, 42.0):
            top = py - 7.0 - lab_h + d
            box = (px - w / 2.0, top, px + w / 2.0, top + lab_h)
            if box[1] < 0 or box[3] > plot_h:
                continue
            if any(box[0] < q[2] and q[0] < box[2]
                   and box[1] < q[3] and q[1] < box[3] for q in placed):
                continue
            spot = (box, d)
            break
        if spot is None:
            continue
        placed.append(spot[0])
        # Nhãn bị đẩy xa thì phải có nét dẫn. Không có nét dẫn, nhãn "Nội thất"
        # bị đẩy lên 33 pt rơi đúng vào quả bóng Điện tử ở trên — người đọc sẽ
        # gán tên sai cho chấm, tệ hơn hẳn là không dán nhãn.
        shift = 7.0 - spot[1]
        if abs(spot[1]) > 12.0:
            # Nét dẫn vẽ bằng một annotation chỉ có mũi tên, không có chữ: shape
            # đặt theo pixel lấy `xanchor` ở thang tuyến tính còn annotation lấy
            # ở thang log, nên trên trục log shape rơi lệch hẳn sang chỗ khác.
            fig.add_annotation(x=_lg(r["rca"]), y=r["pci"], text="",
                               showarrow=True, ax=0, ay=-shift,
                               arrowhead=0, arrowwidth=0.5, arrowcolor=LEADER,
                               standoff=4)
        fig.add_annotation(
            x=_lg(r["rca"]), y=r["pci"], xref="x", yref="y",
            text=("<b>%s</b>" % txt) if em else txt,
            showarrow=False, xanchor="center", yanchor="bottom",
            yshift=shift,
            font=dict(size=LABEL_FLOOR_PT,
                      color="#000000" if em else TEXT_DIM))

    tickv = [0.05, 0.1, 0.25, 0.5, 1, 2, 4, 8]
    fig.update_xaxes(
        type="log", range=[_lg(xs[0]), _lg(xs[1])],
        tickmode="array", tickvals=tickv,
        ticktext=[R.fmt_vn(v, 0 if v >= 1 else 2) for v in tickv],
        title=dict(text="RCA — bán đậm hơn (phải) hay nhạt hơn (trái) thế giới",
                   font=dict(size=R.FONT_SIZES["axis"])),
        tickfont=dict(size=R.FONT_SIZES["tick"]),
        gridcolor=GRID, zeroline=False, showline=True, linecolor=RULE,
        linewidth=0.8)
    fig.update_yaxes(
        range=ys,
        title=dict(text="PCI — độ phức tạp của mặt hàng",
                   font=dict(size=R.FONT_SIZES["axis"])),
        tickfont=dict(size=R.FONT_SIZES["tick"]),
        gridcolor=GRID, zeroline=False, showline=True, linecolor=RULE,
        linewidth=0.8)
    fig.update_layout(
        font=dict(family=", ".join(R.FONT_STACK),
                  size=R.FONT_SIZES["annotation"]),
        separators=",.",
        margin=dict(l=MARGIN_L, r=MARGIN_X, t=m_t, b=m_b),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        hovermode="closest",
        legend=dict(orientation="h", yanchor="top",
                    y=-((AXIS_BAND + 4.0) / plot_h),
                    xanchor="left", x=0, font=dict(size=LABEL_FLOOR_PT),
                    itemsizing="constant", tracegroupgap=2,
                    bgcolor="rgba(0,0,0,0)"))

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

    bottom(note_w, AXIS_BAND + LEG_BAND, R.FONT_SIZES["annotation"], TEXT_DIM)
    bottom(src_w, AXIS_BAND + LEG_BAND
           + R.n_lines(note_w) * R.FONT_SIZES["annotation"] * LINE_H,
           R.FONT_SIZES["footnote"], "#777777")
    return fig


def _lg(v):
    import math
    return math.log10(v)


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


def report(year, since, df, pick, stk):
    print("\n" + "=" * 70)
    print("KIỂM CHỨNG — mặt phẳng quyết định, năm %d (so với %d)" % (year, since))
    print("=" * 70)
    tot = df["export_value"].sum()
    print("  %s nhóm hàng cấp 2 có số liệu, tổng xuất %s"
          % (R.fmt_vn(len(df), 0), R.fmt_usd(tot, 2)))
    print("  Quy tắc chọn: xuất ≥ %s · PCI > 0 · %s ≤ RCA < %s · RCA tăng từ %d"
          % (R.fmt_usd(MIN_EXPORT, 0), R.fmt_vn(RCA_LO, 1),
             R.fmt_vn(RCA_HI, 1), since))

    pool = df[(df["export_value"] >= MIN_EXPORT) & (df["pci"] > 0)
              & (df["rca"] >= RCA_LO) & (df["rca"] < RCA_HI)
              & (df["d_rca"] > 0) & (df["sector"] != UNCLASSIFIED)]
    print("\n  Lọt vào vòng chọn (%s nhóm), xếp theo PCI:" % R.fmt_vn(len(pool), 0))
    for _, r in pool.sort_values("pci", ascending=False).iterrows():
        mark = "  ←ĐỀ XUẤT" if r.name in set(pick.index) else ""
        print("    %-30s RCA %s → %s  PCI %s  xuất %s%s"
              % (r["name"][:30], R.fmt_vn(r["rca_old"], 2),
                 R.fmt_vn(r["rca"], 2), R.fmt_vn(r["pci"], 2),
                 R.fmt_usd(r["export_value"], 1), mark))

    print("\n  Bốn góc có bao nhiêu nhóm, và bao nhiêu tiền:")
    for lab, m in [
            ("phải–trên  đã thắng", (df["rca"] >= 1) & (df["pci"] >= 0)),
            ("trái–trên  cơ hội", (df["rca"] < 1) & (df["pci"] >= 0)),
            ("phải–dưới  đang kẹt", (df["rca"] >= 1) & (df["pci"] < 0)),
            ("trái–dưới  ngoài cuộc", (df["rca"] < 1) & (df["pci"] < 0))]:
        g = df[m]
        print("    %-22s %3s nhóm · %12s · %6s rổ hàng"
              % (lab, R.fmt_vn(len(g), 0), R.fmt_usd(g["export_value"].sum(), 1),
                 R.fmt_pct(g["export_value"].sum() / tot * 100.0)))

    print("\n  Chỗ đang kẹt, PCI thấp nhất trong nhóm xuất ≥ 1 tỷ:")
    for _, r in stk.iterrows():
        print("    %-30s RCA %s  PCI %s  %s rổ hàng"
              % (r["name"][:30], R.fmt_vn(r["rca"], 2), R.fmt_vn(r["pci"], 2),
                 R.fmt_pct(r["share"])))

    unc = df[df["sector"] == UNCLASSIFIED]
    if len(unc):
        print("\n  Ô chưa phân loại: %s rổ hàng — đã loại khỏi danh sách đề xuất"
              % R.fmt_pct(unc["share"].sum()))
    print("  Nhãn nhỏ nhất %.1f pt · khung %.1f × %.1f pt · PNG %d dpi"
          % (LABEL_FLOOR_PT, CANVAS_PT, CANVAS_H, R.FIG_DPI_PRINT))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--since", type=int, default=2015,
                    help="năm so sánh để biết RCA đang tăng hay giảm")
    a = ap.parse_args()

    df = load(a.year, a.since)
    pick = candidates(df)
    stk = stuck(df)
    fig = build(a.year, a.since, df, pick, stk)
    print("Đã dựng mặt phẳng quyết định năm %d:" % a.year)
    save(fig, "decision_plane_%d" % a.year)
    report(a.year, a.since, df, pick, stk)
    return 0


if __name__ == "__main__":
    sys.exit(main())

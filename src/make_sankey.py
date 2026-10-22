# -*- coding: utf-8 -*-
"""Sankey nhập → Việt Nam → xuất: kiểm giả thuyết trung chuyển (T19).

Đây là hình DUY NHẤT của đồ án còn giữ chiều của luồng. T15 (node-link) và T17
(chord) đều gộp hai chiều vào một dải theo **B13**, nên câu hỏi "hàng vào từ đâu,
hàng ra đi đâu" không thể trả lời bằng hai hình đó. Sankey là chỗ trả lời.

Bốn quyết định thiết kế, mỗi cái có lý do đo được:

1. **Dùng đồ thị ĐẦY ĐỦ, không lọc ngưỡng B4.** Các hình mạng (T15–T17) lọc cạnh
   để 27.535 cạnh xuống còn 416 cho mắt đọc được. Nhưng hình này chỉ xét 1 nước,
   số cạnh của riêng Việt Nam vốn đã nhỏ, mà lọc thì tổng xuất khẩu không còn
   khớp con số chính thức 385,5 tỷ USD ở `country_year.csv`. Nên ở đây lấy hết.
   *Hệ quả phải nói ra:* số của hình này KHÔNG so trực tiếp được với T17 — đúng
   cái bẫy đã ghi ở **A5**.

2. **Hai cột dùng CHUNG một thang giá trị trên mỗi point.** Nhờ vậy cột cao hơn
   là cột nhiều tiền hơn, và phần chênh lệch chiều cao giữa hai cột *chính là*
   cán cân thương mại — đọc được bằng mắt, không cần chú thích.

3. **Không có nút "giá trị tăng thêm".** Rất muốn vẽ thêm một nút như vậy cho
   dòng vào bằng dòng ra, nhưng tách được bao nhiêu giá trị ở lại Việt Nam thì
   cần bảng vào–ra (input–output), dữ liệu Atlas không có. Phần chênh chỉ được
   gọi đúng tên số học của nó: **xuất trừ nhập**. Xem hạn chế **D2**, **D5**.

4. **Màu: chỉ có xám.** Màu đã dành hết cho ngành hàng (style guide §3.1) và
   **B17** đã đo được là không còn chỗ cho bảng màu thứ ba. Hai cột phân biệt
   bằng VỊ TRÍ (trái = mua vào, phải = bán ra), dải lớn nhất mỗi bên đậm hơn, và
   Việt Nam nổi bằng viền đen theo **B12**.

Chạy
----
    python src/make_sankey.py                 # năm tham chiếu 2023
    python src/make_sankey.py --year 1995     # năm đối chứng
    python src/make_sankey.py --topk 9
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
CANVAS_PT = R.FIG_WIDTH_FULL * PT_PER_INCH      # 453,6
CANVAS_H = 356.0
MARGIN_X = 10.0
TEXT_PAD = 6.0
LINE_H = 1.33
LABEL_FLOOR_PT = 7.0

HEAD_PT = 16.0        # chỗ cho nhãn ba cột
LAB_W = 94.0        # chỗ để nhãn nước, mỗi bên
BAR_W = 10.0        # bề dày thanh
GAP_PT = 2.6        # khe giữa hai thanh liền nhau

BAR_FILL = "#6E6E6E"
VN_FILL = "#2E2E2E"
BAL_FILL = "#E4E4E4"      # phần chênh xuất − nhập, không phải giá trị tăng thêm
RIB_FILL = "#CFCFCF"
RIB_FOCUS = "#8E8E8E"
LEADER = "#9A9A9A"
TEXT_DIM = "#555555"

SOURCE_TEXT = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab), "
               "dữ liệu HS92 theo cặp nước. Đồ thị đầy đủ, không lọc ngưỡng.")


# ---------------------------------------------------------------------------
# Dữ liệu
# ---------------------------------------------------------------------------

def load_nodes():
    n = pd.read_csv(os.path.join(DATA, "nodes.csv"))
    name = {}
    for iso, vi in zip(n["country_iso3"], n["country_name_vi"]):
        name[iso] = vi if isinstance(vi, str) and vi.strip() else iso
    region = dict(zip(n["country_iso3"], n["region"]))
    return name, region


def load_flows(year):
    """Trả về hai Series: mua vào (nguồn → VN) và bán ra (VN → đích).

    Mỗi dòng của ``edges.csv`` là một luồng CÓ HƯỚNG, cột ``export_value`` là
    giá trị chảy từ ``source_iso3`` sang ``target_iso3``. Nên:
      - hàng Việt Nam mua vào  = các dòng có target_iso3 == VNM
      - hàng Việt Nam bán ra   = các dòng có source_iso3 == VNM
    """
    e = pd.read_csv(os.path.join(DATA, "edges.csv"))
    e = e[e["year"] == year]
    buy = (e[e["target_iso3"] == FOCUS]
           .groupby("source_iso3")["export_value"].sum())
    sell = (e[e["source_iso3"] == FOCUS]
            .groupby("target_iso3")["export_value"].sum())
    buy = buy[buy > 0].sort_values(ascending=False)
    sell = sell[sell > 0].sort_values(ascending=False)
    return buy, sell


def topk_group(s, k):
    """Giữ k nước lớn nhất, gộp phần đuôi thành một mục ``Khác``.

    Trả về danh sách ``(khoá, giá trị, số_nước_gộp)``; khoá là iso3, trừ mục gộp
    có khoá ``None``.
    """
    head = s.head(k)
    tail = s.iloc[k:]
    items = [(iso, float(v), 1) for iso, v in head.items()]
    if len(tail):
        items.append((None, float(tail.sum()), int(len(tail))))
    return items


# ---------------------------------------------------------------------------
# Hình học — mọi toạ độ tính bằng point, trục đặt đúng khoảng point
# ---------------------------------------------------------------------------

def biggest_named(rows):
    """Giá trị của ĐỐI TÁC lớn nhất, bỏ qua cụm gộp ``Khác``.

    Cần hàm riêng vì cụm gộp thường lớn hơn mọi nước đứng riêng — bên bán ra năm
    2023, ``Khác`` là 132,2 tỷ còn Hoa Kỳ chỉ 95,2 tỷ. Lấy "lớn nhất" theo nghĩa
    thường thì hình sẽ tô đậm đúng cái ô duy nhất không phải một đối tác nào.
    """
    v = [r[1] for r in rows if r[0] is not None]
    return max(v) if v else 0.0


def stack(items, ppv, y_top):
    """Xếp các thanh từ trên xuống, cao theo giá trị. Trả về (khoá, v, n, y0, y1)."""
    out = []
    y = y_top
    for key, v, n in items:
        h = v * ppv
        out.append((key, v, n, y, y + h))
        y += h + GAP_PT
    return out


def ribbon(xa, ya0, ya1, xb, yb0, yb1):
    """Dải nối hai đoạn thẳng đứng bằng hai đường Bézier bậc ba.

    Điểm điều khiển đặt ở giữa khoảng ngang nên dải đi ra khỏi thanh theo phương
    ngang — mắt đọc được là "cùng một dòng hàng", không bị tưởng là mũi nhọn.
    """
    cx = (xa + xb) / 2.0
    return ("M %.2f,%.2f C %.2f,%.2f %.2f,%.2f %.2f,%.2f "
            "L %.2f,%.2f C %.2f,%.2f %.2f,%.2f %.2f,%.2f Z"
            % (xa, ya0, cx, ya0, cx, yb0, xb, yb0,
               xb, yb1, cx, yb1, cx, ya1, xa, ya1))


def place_labels(rows, block_h, y_lo, y_hi):
    """Đẩy nhãn cho khỏi chồng nhau: một lượt xuống, rồi một lượt lên.

    Trả về danh sách y tâm nhãn, cùng thứ tự với ``rows``. Lượt xuống giải quyết
    chồng lấn, lượt lên xử lý trường hợp lượt xuống đẩy quá đáy khung.
    """
    ys = [(r[3] + r[4]) / 2.0 for r in rows]
    for i in range(len(ys)):
        lo = y_lo + block_h / 2.0 if i == 0 else ys[i - 1] + block_h
        if ys[i] < lo:
            ys[i] = lo
    for i in range(len(ys) - 1, -1, -1):
        hi = y_hi - block_h / 2.0 if i == len(ys) - 1 else ys[i + 1] - block_h
        if ys[i] > hi:
            ys[i] = hi
    return ys


# ---------------------------------------------------------------------------
# Câu chữ — suy từ dữ liệu, không viết sẵn
# ---------------------------------------------------------------------------

def headline(year, buy, sell, name, region):
    """Tiêu đề + phụ đề + ghi chú, mọi con số tính lại trong chính lần chạy này."""
    bt, st = float(buy.sum()), float(sell.sum())
    top_b, top_s = buy.index[0], sell.index[0]
    nb, ns = name.get(top_b, top_b), name.get(top_s, top_s)

    # vùng nào cấp nhiều hàng nhất, vùng nào mua nhiều hàng nhất
    rb = buy.groupby(buy.index.map(lambda i: region.get(i, "Other"))).sum()
    rs = sell.groupby(sell.index.map(lambda i: region.get(i, "Other"))).sum()
    rb = rb.sort_values(ascending=False)
    rs = rs.sort_values(ascending=False)
    rb_name = R.REGION_VI.get(rb.index[0], rb.index[0])
    rs_name = R.REGION_VI.get(rs.index[0], rs.index[0])

    # cán cân với hai đối tác đầu mỗi bên: đây là bằng chứng của "hành lang"
    bal_b = float(sell.get(top_b, 0.0)) - float(buy.get(top_b, 0.0))
    bal_s = float(sell.get(top_s, 0.0)) - float(buy.get(top_s, 0.0))

    # Chỉ được gọi là "hành lang" khi hai đầu NGƯỢC DẤU: mua ròng ở đầu này, bán
    # ròng ở đầu kia. Hai đối tác khác tên nhau thôi thì chưa đủ — một nước có
    # thể vừa mua vừa bán nhiều mà chẳng có chiều nào. Phép kiểm này chạy lại mỗi
    # năm nên tiêu đề không bao giờ in ra một khẳng định mà dữ liệu năm đó bác.
    corridor = (top_b != top_s) and bal_b < 0 and bal_s > 0
    if corridor:
        title = ("Hàng vào từ %s, hàng ra sang %s — hai đầu của một hành lang"
                 % (nb, ns))
    elif top_b != top_s:
        title = ("Việt Nam mua nhiều nhất từ %s, bán nhiều nhất sang %s" % (nb, ns))
    else:
        title = ("%s vừa là nơi Việt Nam mua nhiều nhất vừa là nơi bán nhiều nhất"
                 % nb)

    # Hai vùng đứng đầu MỖI BÊN, không phải một. Năm 2023 vùng đứng đầu hai bên
    # đều là Đông Á, nên chỉ nêu một vùng thì giấu mất chỗ bất đối xứng: hàng vào
    # dồn vào một vùng, hàng ra thì chia đôi.
    def two(sr, tot):
        parts = []
        for k, v in sr.head(2).items():
            parts.append("%s %s" % (R.REGION_VI.get(k, k),
                                    R.fmt_pct(v / tot * 100.0)))
        return " và ".join(parts)

    sub = ("Năm %d Việt Nam mua %s và bán %s. Hàng vào dồn vào %s; hàng ra chia "
           "cho %s. Ba nguồn mua lớn nhất giữ %s tổng hàng vào, ba nơi bán lớn "
           "nhất giữ %s tổng hàng ra."
           % (year, R.fmt_usd(bt), R.fmt_usd(st), two(rb, bt), two(rs, st),
              R.fmt_pct(buy.head(3).sum() / bt * 100.0),
              R.fmt_pct(sell.head(3).sum() / st * 100.0)))

    def ten(x):
        return "thặng dư" if x >= 0 else "thâm hụt"

    note = ("Chênh lệch với từng đối tác là bằng chứng của chiều: %s %s với %s, "
            "%s %s với %s. Phần nhạt trên thanh Việt Nam là xuất trừ nhập (%s), "
            "KHÔNG phải giá trị tăng thêm trong nước — tách được phần đó cần "
            "bảng vào–ra mà dữ liệu Atlas không có (hạn chế D2, D5)."
            % (ten(bal_b), R.fmt_usd(abs(bal_b)), nb,
               ten(bal_s), R.fmt_usd(abs(bal_s)), ns,
               R.fmt_usd(st - bt)))
    return title, sub, note, rb, rs, bal_b, bal_s


# ---------------------------------------------------------------------------
# Dựng hình
# ---------------------------------------------------------------------------

def build(year, buy, sell, name, region, topk):
    title, sub, note, rb, rs, bal_b, bal_s = headline(year, buy, sell, name,
                                                      region)
    t_w = CANVAS_PT - 2 * MARGIN_X - 2 * TEXT_PAD
    title_w = R.wrap_pt(title, R.FONT_SIZES["title"], t_w)
    sub_w = R.wrap_pt(sub, R.FONT_SIZES["subtitle"], t_w)
    note_w = R.wrap_pt(note, R.FONT_SIZES["annotation"], t_w)
    src_w = R.wrap_pt(SOURCE_TEXT, R.FONT_SIZES["footnote"], t_w)

    m_t = (TEXT_PAD
           + R.n_lines(title_w) * R.FONT_SIZES["title"] * LINE_H
           + R.n_lines(sub_w) * R.FONT_SIZES["subtitle"] * LINE_H
           + TEXT_PAD)
    m_b = (10.0
           + R.n_lines(note_w) * R.FONT_SIZES["annotation"] * LINE_H
           + R.n_lines(src_w) * R.FONT_SIZES["footnote"] * LINE_H
           + TEXT_PAD)
    plot_w = CANVAS_PT - 2 * MARGIN_X
    plot_h = CANVAS_H - m_t - m_b

    b_items = topk_group(buy, topk)
    s_items = topk_group(sell, topk)
    bt, st = float(buy.sum()), float(sell.sum())

    # Một thang chung cho cả hai cột: bên nào nhiều tiền hơn thì cao hơn, và
    # chênh lệch chiều cao đọc ra ngay là cán cân thương mại.
    head_room = HEAD_PT
    avail_b = plot_h - head_room - (len(b_items) - 1) * GAP_PT
    avail_s = plot_h - head_room - (len(s_items) - 1) * GAP_PT
    ppv = min(avail_b / bt, avail_s / st)

    rows_b = stack(b_items, ppv, head_room)
    rows_s = stack(s_items, ppv, head_room)

    x_b1 = LAB_W + BAR_W
    cx = plot_w / 2.0
    x_v0, x_v1 = cx - BAR_W / 2.0, cx + BAR_W / 2.0
    x_s0 = plot_w - LAB_W - BAR_W

    shapes, ann, hov_x, hov_y, hov_t = [], [], [], [], []

    # thanh Việt Nam: cao bằng bên lớn hơn; phần không có hàng vào là phần chênh
    vn_h = max(bt, st) * ppv
    vn_top = head_room
    shapes.append(dict(type="rect", x0=x_v0, y0=vn_top, x1=x_v1,
                       y1=vn_top + vn_h, fillcolor=VN_FILL,
                       line=dict(color=R.HIGHLIGHT_STROKE,
                                 width=R.HIGHLIGHT_STROKE_WIDTH),
                       layer="above"))
    if abs(st - bt) * ppv > 1.0:
        lo = vn_top + min(bt, st) * ppv
        shapes.append(dict(type="rect", x0=x_v0, y0=lo, x1=x_v1,
                           y1=vn_top + vn_h, fillcolor=BAL_FILL,
                           line=dict(color=R.HIGHLIGHT_STROKE,
                                     width=R.HIGHLIGHT_STROKE_WIDTH),
                           layer="above"))

    # dải hàng vào: xếp trên thanh Việt Nam theo đúng thứ tự cột trái
    y = vn_top
    big_b = biggest_named(rows_b)
    for key, v, n, y0, y1 in rows_b:
        h = v * ppv
        shapes.append(dict(type="path",
                           path=ribbon(x_b1, y0, y1, x_v0, y, y + h),
                           fillcolor=(RIB_FOCUS if v == big_b else RIB_FILL),
                           line=dict(width=0), layer="below",
                           opacity=0.95))
        y += h
    y = vn_top
    big_s = biggest_named(rows_s)
    for key, v, n, y0, y1 in rows_s:
        h = v * ppv
        shapes.append(dict(type="path",
                           path=ribbon(x_v1, y, y + h, x_s0, y0, y1),
                           fillcolor=(RIB_FOCUS if v == big_s else RIB_FILL),
                           line=dict(width=0), layer="below",
                           opacity=0.95))
        y += h

    block_h = 2 * LABEL_FLOOR_PT * LINE_H

    def side(rows, total, x_bar0, x_bar1, x_text, anchor, leader_from):
        ys = place_labels(rows, block_h, 0.0, plot_h)
        for (key, v, n, y0, y1), ly in zip(rows, ys):
            shapes.append(dict(type="rect", x0=x_bar0, y0=y0, x1=x_bar1, y1=y1,
                               fillcolor=BAR_FILL, line=dict(width=0),
                               layer="above"))
            if key is None:
                l1 = "Khác (%s nước)" % R.fmt_vn(n, 0)
            else:
                l1 = name.get(key, key)
            l2 = "%s · %s" % (R.fmt_usd(v), R.fmt_pct(v / total * 100.0))
            mid = (y0 + y1) / 2.0
            if abs(ly - mid) > 1.0:
                shapes.append(dict(type="line", x0=leader_from, y0=mid,
                                   x1=x_text, y1=ly,
                                   line=dict(color=LEADER, width=0.5),
                                   layer="below"))
            focus = (key is not None and v == biggest_named(rows))
            body = ("<b>%s</b><br>%s" % (l1, l2)) if focus else ("%s<br>%s"
                                                                 % (l1, l2))
            ann.append(dict(x=x_text, y=ly, xref="x", yref="y",
                            showarrow=False, xanchor=anchor, yanchor="middle",
                            align=anchor, text=body,
                            font=dict(size=LABEL_FLOOR_PT,
                                      color="#000000" if focus else TEXT_DIM)))
            hov_x.append((x_bar0 + x_bar1) / 2.0)
            hov_y.append(mid)
            hov_t.append("%s<br>%s · %s" % (l1, R.fmt_usd(v, 2),
                                            R.fmt_pct(v / total * 100.0)))

    side(rows_b, bt, LAB_W, x_b1, LAB_W - TEXT_PAD, "right", LAB_W)
    side(rows_s, st, x_s0, x_s0 + BAR_W, x_s0 + BAR_W + TEXT_PAD, "left",
         x_s0 + BAR_W)

    # nhãn ba cột: mua vào — Việt Nam — bán ra
    ann.append(dict(x=LAB_W + BAR_W / 2.0, y=head_room - 3.0,
                    xref="x", yref="y", showarrow=False, xanchor="center",
                    yanchor="bottom", text="<b>MUA VÀO</b>",
                    font=dict(size=LABEL_FLOOR_PT, color=TEXT_DIM)))
    ann.append(dict(x=x_s0 + BAR_W / 2.0, y=head_room - 3.0,
                    xref="x", yref="y", showarrow=False, xanchor="center",
                    yanchor="bottom", text="<b>BÁN RA</b>",
                    font=dict(size=LABEL_FLOOR_PT, color=TEXT_DIM)))
    ann.append(dict(x=cx, y=head_room - 3.0, xref="x", yref="y",
                    showarrow=False, xanchor="center", yanchor="bottom",
                    text="<b>VIỆT NAM</b>",
                    font=dict(size=LABEL_FLOOR_PT, color="#000000")))
    # nhãn phần chênh, đặt ngay cạnh đoạn nhạt
    if abs(st - bt) * ppv > 6.0:
        lo = vn_top + min(bt, st) * ppv
        ann.append(dict(x=x_v1 + 2.0, y=(lo + vn_top + vn_h) / 2.0,
                        xref="x", yref="y", showarrow=False, xanchor="left",
                        yanchor="middle",
                        text="xuất − nhập<br>%s" % R.fmt_usd(st - bt),
                        font=dict(size=LABEL_FLOOR_PT, color=TEXT_DIM)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hov_x, y=hov_y, mode="markers",
                             hoverinfo="text", hovertext=hov_t,
                             marker=dict(size=9, color="rgba(0,0,0,0)"),
                             showlegend=False))
    fig.update_layout(
        shapes=shapes, annotations=ann,
        font=dict(family=", ".join(R.FONT_STACK),
                  size=R.FONT_SIZES["annotation"]),
        separators=",.",
        margin=dict(l=MARGIN_X, r=MARGIN_X, t=m_t, b=m_b),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        hovermode="closest", showlegend=False)
    fig.update_xaxes(visible=False, range=[0, plot_w], constrain="domain")
    # trục y đảo chiều: y = 0 ở trên, tính xuống như đọc chữ
    fig.update_yaxes(visible=False, range=[plot_h, 0], constrain="domain")

    def block(txt, y_from_top, size, color=None):
        fig.add_annotation(text=txt, showarrow=False, xref="paper",
                           yref="paper", x=0,
                           y=1 + (m_t - y_from_top) / plot_h,
                           xshift=-(MARGIN_X - TEXT_PAD), xanchor="left",
                           yanchor="top", align="left",
                           font=dict(size=size, color=color))

    block(title_w, TEXT_PAD, R.FONT_SIZES["title"])
    block(sub_w, TEXT_PAD + R.n_lines(title_w) * R.FONT_SIZES["title"] * LINE_H,
          R.FONT_SIZES["subtitle"], TEXT_DIM)

    def bottom(txt, y_from_plot, size, color):
        fig.add_annotation(text=txt, showarrow=False, xref="paper",
                           yref="paper", x=0, y=-(y_from_plot / plot_h),
                           xshift=-(MARGIN_X - TEXT_PAD), xanchor="left",
                           yanchor="top", align="left",
                           font=dict(size=size, color=color))

    bottom(note_w, 10.0, R.FONT_SIZES["annotation"], TEXT_DIM)
    bottom(src_w, 10.0 + R.n_lines(note_w) * R.FONT_SIZES["annotation"] * LINE_H,
           R.FONT_SIZES["footnote"], "#777777")
    return fig, rb, rs, bal_b, bal_s, rows_b, rows_s, ppv


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
        print("  (không xuất được PNG: %s — bản .html vẫn dùng được)" % exc)


# ---------------------------------------------------------------------------
# Khối kiểm chứng
# ---------------------------------------------------------------------------

def report(year, buy, sell, name, region, rb, rs, bal_b, bal_s, rows_b, rows_s,
           ppv):
    print("\n" + "=" * 70)
    print("KIỂM CHỨNG — Sankey nhập → Việt Nam → xuất, năm %d" % year)
    print("=" * 70)
    bt, st = float(buy.sum()), float(sell.sum())
    print("  Đối tác: mua vào từ %s nước, bán ra %s nước"
          % (R.fmt_vn(len(buy), 0), R.fmt_vn(len(sell), 0)))
    print("  Tổng mua vào %s · tổng bán ra %s · xuất trừ nhập %s"
          % (R.fmt_usd(bt, 2), R.fmt_usd(st, 2), R.fmt_usd(st - bt, 2)))

    cy = pd.read_csv(os.path.join(DATA, "country_year.csv"))
    row = cy[(cy["country_iso3"] == FOCUS) & (cy["year"] == year)]
    if len(row):
        ex_off = float(row["export_value"].iloc[0])
        im_off = float(row["import_value"].iloc[0])
        print("  Khớp với country_year.csv: xuất %s (lệch %s) · nhập %s (lệch %s)"
              % (R.fmt_usd(ex_off, 2), R.fmt_usd(st - ex_off, 2),
                 R.fmt_usd(im_off, 2), R.fmt_usd(bt - im_off, 2)))

    print("\n  Cột trái — mua vào (%s thanh, đã gộp đuôi):" % len(rows_b))
    for key, v, n, y0, y1 in rows_b:
        lab = ("Khác (%d nước)" % n) if key is None else name.get(key, key)
        print("    %-24s %12s  %6s  cao %5.1f pt"
              % (lab[:24], R.fmt_usd(v, 2), R.fmt_pct(v / bt * 100.0),
                 v * ppv))
    print("  Cột phải — bán ra (%s thanh):" % len(rows_s))
    for key, v, n, y0, y1 in rows_s:
        lab = ("Khác (%d nước)" % n) if key is None else name.get(key, key)
        print("    %-24s %12s  %6s  cao %5.1f pt"
              % (lab[:24], R.fmt_usd(v, 2), R.fmt_pct(v / st * 100.0),
                 v * ppv))

    s_b = sum(r[1] for r in rows_b)
    s_s = sum(r[1] for r in rows_s)
    print("\n  Dải cộng lại có bằng tổng không? mua vào lệch %s · bán ra lệch %s"
          % (R.fmt_usd(s_b - bt, 2), R.fmt_usd(s_s - st, 2)))
    assert abs(s_b - bt) < 1.0 and abs(s_s - st) < 1.0, "dải không khớp tổng"

    print("\n  Theo vùng — mua vào:")
    for k, v in rb.head(4).items():
        print("    %-22s %6s" % (R.REGION_VI.get(k, k),
                                 R.fmt_pct(v / bt * 100.0)))
    print("  Theo vùng — bán ra:")
    for k, v in rs.head(4).items():
        print("    %-22s %6s" % (R.REGION_VI.get(k, k),
                                 R.fmt_pct(v / st * 100.0)))

    top_b, top_s = buy.index[0], sell.index[0]
    print("\n  Bằng chứng chiều (cán cân với từng đối tác):")
    print("    %-22s mua %12s · bán %12s · chênh %12s"
          % (name.get(top_b, top_b), R.fmt_usd(buy.get(top_b, 0.0), 2),
             R.fmt_usd(sell.get(top_b, 0.0), 2), R.fmt_usd(bal_b, 2)))
    print("    %-22s mua %12s · bán %12s · chênh %12s"
          % (name.get(top_s, top_s), R.fmt_usd(buy.get(top_s, 0.0), 2),
             R.fmt_usd(sell.get(top_s, 0.0), 2), R.fmt_usd(bal_s, 2)))
    if bal_b < 0 and bal_s > 0:
        print("    → hai đầu ngược dấu: mua ở một đầu, bán ở đầu kia. Đây là"
              " dấu hiệu hành lang mà giả thuyết trung chuyển cần.")
    else:
        print("    → hai đầu KHÔNG ngược dấu, không đọc ra hành lang ở năm này.")

    print("\n  Nhãn nhỏ nhất trên hình: %.1f pt (sàn %.1f pt của style guide §7)"
          % (LABEL_FLOOR_PT, LABEL_FLOOR_PT))
    print("  Khung %.1f × %.1f pt, xuất PNG %d × %d px = %d dpi"
          % (CANVAS_PT, CANVAS_H,
             round(R.FIG_WIDTH_FULL * R.FIG_DPI_PRINT),
             round(CANVAS_H / PT_PER_INCH * R.FIG_DPI_PRINT),
             R.FIG_DPI_PRINT))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--topk", type=int, default=7,
                    help="số nước đứng riêng mỗi bên, phần còn lại gộp")
    a = ap.parse_args()

    name, region = load_nodes()
    buy, sell = load_flows(a.year)
    if not len(buy) or not len(sell):
        print("Không có luồng nào của %s ở năm %d." % (FOCUS, a.year))
        return 1

    fig, rb, rs, bal_b, bal_s, rows_b, rows_s, ppv = build(
        a.year, buy, sell, name, region, a.topk)
    print("Đã dựng Sankey năm %d:" % a.year)
    save(fig, "sankey_vietnam_%d" % a.year)
    report(a.year, buy, sell, name, region, rb, rs, bal_b, bal_s, rows_b,
           rows_s, ppv)
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
"""Small multiples theo thời gian: Việt Nam bán cho ai, 1995·2005·2015·2023 (T20).

T21 trả lời "bán GÌ". Hình này trả lời "bán CHO AI", và nó là hình dựng sẵn cho
phát hiện **A9**: từ 2015 đến 2023 tiền xuất khẩu gấp 2,28 lần mà **số bạn hàng
giảm 15 nước**, trong khi trung vị thế giới là +1. Nhiều tiền hơn, qua ít kênh
hơn — một câu mà bốn ô lưới nói hộ được.

Vì sao small multiples chứ không phải một hình động hay một hình chồng
----------------------------------------------------------------------
Bốn năm mốc, mỗi năm một thứ hạng bạn hàng KHÁC NHAU — Nhật Bản đứng đầu năm
1995, Hoa Kỳ đứng đầu năm 2023. Vẽ chồng lên nhau thì phải chọn một thứ tự
chung, mà thứ tự nào cũng sai cho ba năm còn lại. Small multiples cho mỗi ô tự
xếp hạng của nó, và vì **trục ngang dùng chung một thang**, mắt vẫn so được bề
dài giữa các ô. Đó đúng là phép đổi mà small multiples sinh ra để làm.

Hai điều buộc phải thống nhất giữa bốn ô, nếu không thì so sánh là giả:

1. **Chung thang trục ngang** — tính một lần trên cả bốn năm rồi áp cho cả bốn.
2. **Chung quy tắc gộp đuôi** — cùng lấy ``TOPK`` nước đầu, phần còn lại gộp
   thành một thanh ``Khác`` kèm số nước, để không ô nào trông thưa giả tạo.

Tiêu đề từng ô ghi tổng giá trị và **số bạn hàng** của năm đó; chính cặp số này
là bằng chứng của A9, nên nó phải nằm trên hình chứ không nằm trong lời kể.

Chạy
----
    python src/make_time_multiples.py
    python src/make_time_multiples.py --direction nhap
    python src/make_time_multiples.py --topk 5
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
CANVAS_H = 344.0
MARGIN_X = 10.0
MARGIN_L = 64.0            # chỗ cho tên nước ở cột trái của mỗi ô
TEXT_PAD = 6.0
LINE_H = 1.33
LABEL_FLOOR_PT = 7.0

BAR = "#B4B4B4"
BAR_TOP = "#5A5A5A"        # thanh lớn nhất của từng ô
BAR_REST = "#DCDCDC"       # cụm gộp "Khác"
GRID = "#E6E6E6"
TEXT_DIM = "#555555"

SOURCE_TEXT = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab). "
               "Đồ thị đầy đủ, không lọc ngưỡng — xem T19.")


def load(years, direction):
    """Với mỗi năm, trả về Series bạn hàng → giá trị, đã sắp giảm dần."""
    e = pd.read_csv(os.path.join(DATA, "edges.csv"))
    n = pd.read_csv(os.path.join(DATA, "nodes.csv"))
    name = {}
    for iso, vi in zip(n["country_iso3"], n["country_name_vi"]):
        name[iso] = vi if isinstance(vi, str) and vi.strip() else iso
    out = {}
    for y in years:
        ey = e[e["year"] == y]
        if direction == "xuat":
            s = ey[ey["source_iso3"] == FOCUS].groupby(
                "target_iso3")["export_value"].sum()
        else:
            s = ey[ey["target_iso3"] == FOCUS].groupby(
                "source_iso3")["export_value"].sum()
        s = s[s > 0].sort_values(ascending=False)
        out[y] = s
    return out, name


def panel_rows(s, topk, name):
    """TOPK nước đầu cộng một thanh gộp — cùng quy tắc cho cả bốn ô."""
    tot = float(s.sum())
    rows = []
    for iso, v in s.head(topk).items():
        rows.append((name.get(iso, iso), float(v) / tot * 100.0, False))
    tail = s.iloc[topk:]
    if len(tail):
        rows.append(("Khác (%s nước)" % R.fmt_vn(len(tail), 0),
                     float(tail.sum()) / tot * 100.0, True))
    return rows, tot


def headline(data, years, direction):
    y0, y1 = years[0], years[-1]
    t0, t1 = float(data[y0].sum()), float(data[y1].sum())
    n0, n1 = len(data[y0]), len(data[y1])
    verb = "bán cho" if direction == "xuat" else "mua từ"
    # A9 so 2015 với 2023 và thấy số bạn hàng giảm 15. Nhưng vẽ đủ bốn mốc thì
    # hình dạng thật không phải một đường giảm: số bạn hàng ĐẠT ĐỈNH rồi mới
    # quay đầu. Nên tìm năm đỉnh thay vì chỉ so hai đầu — so hai đầu ở đây sẽ ra
    # "tăng 68 nước", đúng số nhưng che mất chỗ quan trọng.
    counts = [(y, len(data[y])) for y in years]
    peak_y, peak_n = max(counts, key=lambda t: t[1])
    if peak_y != y1 and peak_n > n1:
        kenh = ("tiền gấp %s lần, nhưng số bạn hàng đã đạt đỉnh %s nước năm %d "
                "rồi lùi về %s" % (R.fmt_vn(t1 / t0, 1), R.fmt_vn(peak_n, 0),
                                   peak_y, R.fmt_vn(n1, 0)))
    elif n1 < n0:
        kenh = ("tiền gấp %s lần mà số bạn hàng GIẢM %s nước"
                % (R.fmt_vn(t1 / t0, 1), R.fmt_vn(n0 - n1, 0)))
    else:
        kenh = ("tiền gấp %s lần, số bạn hàng %s nước → %s"
                % (R.fmt_vn(t1 / t0, 1), R.fmt_vn(n0, 0), R.fmt_vn(n1, 0)))
    top0 = data[y0].index[0]
    top1 = data[y1].index[0]
    title = ("Việt Nam %s ai: %s" % (verb, kenh))
    sub = ("Bốn năm mốc, chung một thang trục ngang nên bề dài so được giữa các "
           "ô. Bạn hàng lớn nhất đổi từ %%s năm %d sang %%s năm %d, và tỷ trọng "
           "của nó %%s." % (y0, y1))
    return title, sub, top0, top1


def build(data, years, name, topk, direction):
    title, sub_t, top0, top1 = headline(data, years, direction)
    panels = {}
    for y in years:
        panels[y] = panel_rows(data[y], topk, name)
    xmax = max(max(r[1] for r in panels[y][0]) for y in years)
    xmax = min(100.0, xmax * 1.18)

    s0 = panels[years[0]][0][0][1]
    s1 = panels[years[-1]][0][0][1]
    trend = ("tăng từ %s lên %s" % (R.fmt_pct(s0), R.fmt_pct(s1))
             if s1 >= s0 else
             "giảm từ %s xuống %s" % (R.fmt_pct(s0), R.fmt_pct(s1)))
    sub = sub_t % (name.get(top0, top0), name.get(top1, top1), trend)

    t_w = CANVAS_PT - MARGIN_L - MARGIN_X - 2 * TEXT_PAD
    title_w = R.wrap_pt(title, R.FONT_SIZES["title"], t_w)
    sub_w = R.wrap_pt(sub, R.FONT_SIZES["subtitle"], t_w)
    note = ("Thanh là tỷ trọng trong tổng %s của chính năm đó, nên bốn ô so "
            "được CƠ CẤU; quy mô tuyệt đối nằm ở tiêu đề từng ô. Thanh nhạt "
            "nhất là phần gộp các nước còn lại."
            % ("xuất khẩu" if direction == "xuat" else "nhập khẩu"))
    note_w = R.wrap_pt(note, R.FONT_SIZES["annotation"], t_w)
    src_w = R.wrap_pt(SOURCE_TEXT, R.FONT_SIZES["footnote"], t_w)

    m_t = (TEXT_PAD + R.n_lines(title_w) * R.FONT_SIZES["title"] * LINE_H
           + R.n_lines(sub_w) * R.FONT_SIZES["subtitle"] * LINE_H
           + 2 * TEXT_PAD)
    m_b = (20.0 + R.n_lines(note_w) * R.FONT_SIZES["annotation"] * LINE_H
           + R.n_lines(src_w) * R.FONT_SIZES["footnote"] * LINE_H + TEXT_PAD)
    plot_h = CANVAS_H - m_t - m_b

    subtitles = []
    for y in years:
        rows, tot = panels[y]
        subtitles.append("<b>%d</b> · %s · %s bạn hàng"
                         % (y, R.fmt_usd(tot), R.fmt_vn(len(data[y]), 0)))

    fig = make_subplots(rows=2, cols=2, subplot_titles=subtitles,
                        horizontal_spacing=0.17, vertical_spacing=0.13,
                        shared_xaxes=False)

    for i, y in enumerate(years):
        r, c = i // 2 + 1, i % 2 + 1
        rows, tot = panels[y]
        labels = [x[0] for x in rows][::-1]
        vals = [x[1] for x in rows][::-1]
        rest = [x[2] for x in rows][::-1]
        top = max(v for v, g in zip(vals, rest) if not g)
        colors = [BAR_REST if g else (BAR_TOP if v == top else BAR)
                  for v, g in zip(vals, rest)]
        fig.add_trace(go.Bar(
            x=vals, y=labels, orientation="h",
            marker=dict(color=colors, line=dict(width=0)),
            text=[R.fmt_pct(v) for v in vals], textposition="outside",
            textfont=dict(size=LABEL_FLOOR_PT, color=TEXT_DIM),
            cliponaxis=False,
            hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
            showlegend=False), row=r, col=c)
        fig.update_xaxes(range=[0, xmax], showticklabels=False,
                         showgrid=False, zeroline=False, row=r, col=c)
        fig.update_yaxes(tickfont=dict(size=LABEL_FLOOR_PT),
                         showgrid=False, zeroline=False,
                         ticklabelstandoff=2, row=r, col=c)

    # Tiêu đề ô căn trái theo mép trái của chính ô đó. Đẩy sang trái thêm nữa
    # thì tiêu đề hai ô cột phải tràn khỏi khung và bị cắt mất đuôi.
    for a, (r, c) in zip(fig.layout.annotations,
                         [(1, 1), (1, 2), (2, 1), (2, 2)]):
        a.font.size = R.FONT_SIZES["annotation"]
        a.xanchor = "left"
        a.x = fig.get_subplot(r, c).xaxis.domain[0]

    fig.update_layout(
        font=dict(family=", ".join(R.FONT_STACK),
                  size=R.FONT_SIZES["annotation"]),
        separators=",.", bargap=0.28,
        margin=dict(l=MARGIN_L, r=MARGIN_X, t=m_t, b=m_b),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        showlegend=False)

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

    bottom(note_w, 20.0, R.FONT_SIZES["annotation"], TEXT_DIM)
    bottom(src_w, 20.0 + R.n_lines(note_w) * R.FONT_SIZES["annotation"] * LINE_H,
           R.FONT_SIZES["footnote"], "#777777")
    return fig, panels, xmax


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


def report(data, years, panels, name, xmax, direction):
    print("\n" + "=" * 70)
    print("KIỂM CHỨNG — small multiples theo thời gian (%s)"
          % ("xuất khẩu" if direction == "xuat" else "nhập khẩu"))
    print("=" * 70)
    print("  Chung một thang trục ngang cho cả bốn ô: 0 → %s"
          % R.fmt_pct(xmax))
    print("\n  %-6s %14s %10s %10s %10s" % ("năm", "tổng", "bạn hàng",
                                            "top 1", "top 3"))
    for y in years:
        s = data[y]
        tot = float(s.sum())
        print("  %-6d %14s %10s %10s %10s"
              % (y, R.fmt_usd(tot, 1), R.fmt_vn(len(s), 0),
                 R.fmt_pct(s.iloc[0] / tot * 100.0),
                 R.fmt_pct(s.head(3).sum() / tot * 100.0)))

    y0, y1 = years[0], years[-1]
    t0, t1 = float(data[y0].sum()), float(data[y1].sum())
    n0, n1 = len(data[y0]), len(data[y1])
    print("\n  %d → %d: tiền gấp %s lần, bạn hàng %+d nước"
          % (y0, y1, R.fmt_vn(t1 / t0, 2), n1 - n0))
    counts = [(y, len(data[y])) for y in years]
    peak_y, peak_n = max(counts, key=lambda t: t[1])
    print("  Đỉnh số bạn hàng: %s nước năm %d — từ đó %s"
          % (R.fmt_vn(peak_n, 0), peak_y,
             "giảm liên tục" if all(
                 counts[i][1] >= counts[i + 1][1]
                 for i in range(len(counts) - 1)
                 if counts[i][0] >= peak_y) else "không giảm đều"))
    if 2015 in data and 2023 in data:
        a, b = len(data[2015]), len(data[2023])
        print("  Khớp A9 (2015→2023): %d → %d bạn hàng, chênh %+d"
              % (a, b, b - a))

    print("\n  Thứ hạng đầu bảng từng năm — lý do không vẽ chồng được:")
    for y in years:
        top3 = [name.get(i, i) for i in data[y].head(3).index]
        print("    %d: %s" % (y, " · ".join(top3)))

    for y in years:
        rows, tot = panels[y]
        tong = sum(x[1] for x in rows)
        assert abs(tong - 100.0) < 1e-6, "ô %d không cộng đủ 100%%" % y
    print("\n  Mỗi ô có cộng đủ 100%% không? có, cả %s ô"
          % R.fmt_vn(len(years), 0))
    print("  Nhãn nhỏ nhất %.1f pt · khung %.1f × %.1f pt"
          % (LABEL_FLOOR_PT, CANVAS_PT, CANVAS_H))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--years", type=str,
                    default=",".join(str(y) for y in R.MILESTONE_YEARS))
    ap.add_argument("--topk", type=int, default=6)
    ap.add_argument("--direction", choices=["xuat", "nhap"], default="xuat")
    a = ap.parse_args()
    years = [int(x) for x in a.years.split(",")]

    data, name = load(years, a.direction)
    fig, panels, xmax = build(data, years, name, a.topk, a.direction)
    print("Đã dựng small multiples %s:" % a.direction)
    save(fig, "time_multiples_%s" % a.direction)
    report(data, years, panels, name, xmax, a.direction)
    return 0


if __name__ == "__main__":
    sys.exit(main())

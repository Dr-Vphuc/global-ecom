"""Lưới small multiples: cơ cấu xuất khẩu Việt Nam so với các nước ASEAN (T14).

Small multiples là cách so sánh nhiều cây cùng lúc mà vẫn giữ được phép đọc của
treemap: mỗi ô lưới là một nước, dùng CHUNG một bảng màu và CHUNG một cách mã
hóa, nên mắt chỉ phải học bảng màu một lần rồi quét ngang.

Hai quyết định thiết kế, cả hai đều có lý do:

1. **Chỉ vẽ tới tầng 1 (10 ngành), không xuống tầng 2.** Ở kích thước một phần
   tư màn hình, 97 ô nhóm hàng thành những vệt không đọc được. Small multiples
   đổi chiều sâu lấy chiều rộng so sánh — đó là bản chất của nó.

2. **Mỗi ô lưới tự chuẩn hóa về 100%.** Treemap so SÁNH CƠ CẤU, không so quy mô.
   Nếu vẽ theo quy mô tuyệt đối thì ô của Việt Nam (385,5 tỷ) sẽ nuốt ô của
   Philippines và không ai đọc được cơ cấu nữa. Quy mô tuyệt đối không bị mất —
   nó nằm ở tiêu đề từng ô lưới.

Việt Nam được làm nổi bằng viền đậm chứ không bằng màu, theo quy ước ở
``docs/style-guide.md``: màu đã dành hết cho ngành, không còn dư để đánh dấu nước.

Chạy
----
    python src/make_small_multiples.py
    python src/make_small_multiples.py --year 1995
    python src/make_small_multiples.py --countries VNM,THA,MYS,SGP
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reference_data as R  # noqa: E402
from make_hierarchy_charts import OUTDIR, load_exports, load_tree, sector_index  # noqa: E402

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    sys.exit("Thiếu plotly. Chạy: python -m pip install plotly kaleido")

# Mặc định: Việt Nam cùng ba nước ASEAN có quy mô xuất khẩu gần nhất năm 2023.
# Singapore bị để ngoài vì phần lớn kim ngạch của họ là tái xuất, cơ cấu không
# so sánh trực tiếp được — ghi lại ở đây để khỏi ai hỏi lại.
DEFAULT_COUNTRIES = ["VNM", "THA", "MYS", "IDN"]

TILE_BORDER = dict(color="#FFFFFF", width=1)

# Khung tính bằng POINT theo B16 — xem reference_data.xuat_png.
FIG_H_INCH = 5.70
MARGIN_X = 8.0
TEXT_PAD = 6.0
LINE_H = 1.33
LABEL_FLOOR_PT = 7.0
TILE_TITLE_BAND = 32.0   # tên nước + giá trị, hai dòng, trên mỗi ô lưới
FOCUS_ISO = "VNM"


def sector_shares(tree, exports):
    """Gộp xuất khẩu lên 10 ngành cấp 1. Trả về (danh sách ngành, tổng)."""
    index = sector_index(tree)
    total = sum(exports.values())
    acc = {}
    for pid, v in exports.items():
        hit = index.get(pid)
        if hit is None:
            continue
        acc[hit] = acc.get(hit, 0.0) + v
    out = []
    for (sid, no), v in sorted(acc.items(), key=lambda kv: -kv[1]):
        out.append({
            "no": no,
            "name": R.SECTOR_NAME_VI[no],
            "value": v,
            "share": v / total * 100,
            "color": R.SECTOR_PALETTE[no],
        })
    return out, total


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--countries", default=",".join(DEFAULT_COUNTRIES),
                    help="danh sách ISO3 cách nhau bởi dấu phẩy")
    args = ap.parse_args()

    countries = [c.strip().upper() for c in args.countries.split(",") if c.strip()]
    if len(countries) not in (3, 4):
        sys.exit("Cần 3 hoặc 4 nước để lưới cân đối, đang có %d" % len(countries))

    print("Đọc cây HS92...")
    tree = load_tree()

    panels = []
    for iso in countries:
        print("Đọc xuất khẩu %s năm %d..." % (iso, args.year))
        rows, total = sector_shares(tree, load_exports(iso, args.year))
        panels.append((iso, rows, total))

    cols = 2
    rows_n = (len(panels) + 1) // 2
    titles = []
    for iso, _, total in panels:
        name = R.COUNTRY_VI.get(iso, (iso,))[0]
        mark = "  ◆" if iso == "VNM" else ""
        titles.append("<b>%s</b>%s<br><span style='font-size:%dpx;color:#666'>"
                      "%s</span>"
                      % (name, mark, R.FONT_SIZES["footnote"], R.fmt_usd(total)))

    fig = make_subplots(
        rows=rows_n, cols=cols,
        specs=[[{"type": "domain"}] * cols for _ in range(rows_n)],
        subplot_titles=titles,
        horizontal_spacing=0.03, vertical_spacing=0.10,
    )

    for i, (iso, rows, total) in enumerate(panels):
        r, c = i // cols + 1, i % cols + 1
        is_focus = iso == "VNM"
        fig.add_trace(go.Treemap(
            labels=[x["name"] for x in rows],
            parents=[""] * len(rows),
            values=[x["value"] for x in rows],
            marker=dict(
                colors=[x["color"] for x in rows],
                line=(dict(color=R.HIGHLIGHT_STROKE, width=R.HIGHLIGHT_STROKE_WIDTH)
                      if is_focus else TILE_BORDER),
            ),
            # Nhãn chỉ hiện khi ngành chiếm từ 6% trở lên: ở kích thước một phần
            # tư màn hình, dưới ngưỡng đó chữ không còn đọc được.
            text=["<b>%s</b><br>%s" % (x["name"], R.fmt_pct(x["share"], 0))
                  if x["share"] >= 6 else "" for x in rows],
            texttemplate="%{text}",
            textposition="middle center",
            # Hover dựng sẵn từng ô, không để plotly tự định dạng: %{value:.3s}
            # ra "18.4G USD" — sai dấu thập phân, và dùng tiền tố SI mà mục 6.4
            # của style guide không cho dùng.
            hovertemplate=["<b>%s</b><br>%s — %s tổng xuất khẩu<extra></extra>"
                           % (x["name"], R.fmt_usd(x["value"]), R.fmt_pct(x["share"]))
                           for x in rows],
            tiling=dict(packing="squarify"),
            sort=True,
        ), row=r, col=c)

    year_note = "" if args.year == R.REFERENCE_YEAR else " (năm %d)" % args.year
    # --- khối chữ đặt tay theo B16 (khung point) ---------------------------
    # Tiêu đề cũ viết sẵn câu "Việt Nam là nước duy nhất còn dựa mạnh vào dệt
    # may, giày dép" — một khẳng định không được tính lại, tức đúng thứ quy tắc
    # 2 của CLAUDE.md cấm. Giờ đi tìm ngành mà Việt Nam vượt nước cao thứ nhì
    # nhiều nhất, rồi nói đúng khoảng cách đo được.
    share_of = {}
    for iso, rws, _tot in panels:
        for x in rws:
            share_of.setdefault(x["name"], {})[iso] = x["share"]
    vn_gap = []
    for nganh, per in share_of.items():
        if FOCUS_ISO not in per:
            continue
        khac = [v for k, v in per.items() if k != FOCUS_ISO]
        if not khac:
            continue
        vn_gap.append((per[FOCUS_ISO] - max(khac), nganh, per[FOCUS_ISO],
                       max(khac)))
    vn_gap.sort(reverse=True)
    if vn_gap and vn_gap[0][0] > 0:
        _d, nganh, vn_s, nhi_s = vn_gap[0]
        title = ("Việt Nam dựa vào %s nặng hơn hẳn: %s rổ hàng, nước cao thứ "
                 "nhì chỉ %s%s"
                 % (nganh.lower(), R.fmt_pct(vn_s), R.fmt_pct(nhi_s), year_note))
    else:
        title = ("Không ngành nào Việt Nam vượt cả ba nước còn lại%s" % year_note)
    sub = ("Cơ cấu xuất khẩu theo 10 ngành cấp 1 của hệ HS92, năm %d. Mỗi ô "
           "lưới tự chuẩn hóa về 100%% nên so được cơ cấu; quy mô tuyệt đối "
           "ghi dưới tên nước. Việt Nam viền đậm." % args.year)
    src = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab), phân "
           "loại HS92. Giá trị xuất khẩu, USD hiện hành.")
    w_pt, h_pt = R.khung_pt(R.FIG_WIDTH_FULL), R.khung_pt(FIG_H_INCH)
    t_w = w_pt - 2 * MARGIN_X - 2 * TEXT_PAD
    tw = R.wrap_pt(title, R.FONT_SIZES["title"], t_w)
    sw = R.wrap_pt(sub, R.FONT_SIZES["subtitle"], t_w)
    cw = R.wrap_pt(src, R.FONT_SIZES["footnote"], t_w)
    h_title = R.n_lines(tw) * R.FONT_SIZES["title"] * LINE_H
    h_sub = R.n_lines(sw) * R.FONT_SIZES["subtitle"] * LINE_H
    m_t = TEXT_PAD + h_title + h_sub + TILE_TITLE_BAND
    m_b = 8.0 + R.n_lines(cw) * R.FONT_SIZES["footnote"] * LINE_H + TEXT_PAD
    plot_h = h_pt - m_t - m_b

    fig.update_layout(
        font=dict(family=", ".join(R.FONT_STACK), size=R.FONT_SIZES["legend"]),
        separators=",.",
        margin=dict(t=m_t, l=MARGIN_X, r=MARGIN_X, b=m_b),
        paper_bgcolor="#FFFFFF",
        # Chữ trong ô tự co cho vừa; chặn sàn 7 pt của §7, thà giấu còn hơn in
        # ra chữ 2–3 pt như bản trước khi sửa lỗi đơn vị B16.
        uniformtext=dict(minsize=LABEL_FLOOR_PT, mode="hide"),
    )
    # Co chữ tiêu đề từng ô lưới (subplot_titles nằm trong layout.annotations).
    # Phải làm TRƯỚC khi thêm tiêu đề chính, nếu không tiêu đề chính cũng bị co.
    fig.update_annotations(font_size=R.FONT_SIZES["annotation"])

    def ann(text, y, size, color):
        fig.add_annotation(text=text, showarrow=False, xref="paper",
                           yref="paper", x=0, y=y,
                           xshift=-(MARGIN_X - TEXT_PAD), xanchor="left",
                           yanchor="top", align="left",
                           font=dict(size=size, color=color))

    ann(tw, 1 + (m_t - TEXT_PAD) / plot_h, R.FONT_SIZES["title"], None)
    ann(sw, 1 + (m_t - TEXT_PAD - h_title) / plot_h,
        R.FONT_SIZES["subtitle"], "#555555")
    ann(cw, -(8.0 / plot_h), R.FONT_SIZES["footnote"], "#777777")

    os.makedirs(OUTDIR, exist_ok=True)
    stem = "small_multiples_%s_%d" % ("-".join(c.lower() for c in countries), args.year)
    html = os.path.join(OUTDIR, stem + ".html")
    fig.write_html(html, include_plotlyjs="cdn", config={"displayModeBar": False})
    print("  %s" % html)
    try:
        png = os.path.join(OUTDIR, stem + ".png")
        R.xuat_png(fig, png, R.FIG_WIDTH_FULL, FIG_H_INCH)
        print("  %s" % png)
    except Exception as exc:
        print("  (không xuất được PNG: %s — bản .html vẫn dùng được)" % exc)

    print("\nCơ cấu theo ngành, %d:" % args.year)
    for iso, rows, total in panels:
        top = rows[0]
        print("  %-4s %14s  — lớn nhất: %-28s %6s"
              % (iso, R.fmt_usd(total), top["name"], R.fmt_pct(top["share"])))

    # Hai con số đỡ cho tiêu đề. In ra để bất kỳ ai cũng kiểm lại được bằng
    # chính script này, thay vì phải tin vào câu tiêu đề.
    TEXTILE, MANUF = 1, (1, 7, 8, 9)
    share_of = {iso: {r["no"]: r["share"] for r in rows} for iso, rows, _ in panels}

    print("\nNgành 1 (dệt may, giày dép, nội thất) — cơ sở của tiêu đề:")
    rank = sorted(share_of, key=lambda c: -share_of[c].get(TEXTILE, 0))
    for iso in rank:
        print("  %-4s %6s" % (iso, R.fmt_pct(share_of[iso].get(TEXTILE, 0))))
    if len(rank) >= 2:
        a, b = share_of[rank[0]].get(TEXTILE, 0), share_of[rank[1]].get(TEXTILE, 0)
        if b > 0:
            print("  -> %s gấp %s lần %s" % (rank[0], R.fmt_vn(a / b), rank[1]))

    print("\nTổng bốn ngành chế tạo (dệt may, vận tải, máy móc, điện tử):")
    for iso in sorted(share_of, key=lambda c: -sum(share_of[c].get(n, 0) for n in MANUF)):
        print("  %-4s %6s"
              % (iso, R.fmt_pct(sum(share_of[iso].get(n, 0) for n in MANUF))))


if __name__ == "__main__":
    main()

"""Hai ma trận kề: thứ tự alphabet so với thứ tự theo cụm (T16).

Đây là nửa thứ hai của phép so sánh mà checklist nộp bài mục 5 yêu cầu. Node-link
ở T15 và hai ma trận ở đây vẽ CÙNG MỘT đồ thị — 73 nút, 416 cạnh, năm 2023 —
nên mọi khác biệt giữa ba hình là khác biệt của CÁCH BIỂU DIỄN, không phải của
dữ liệu.

Điều hình này chứng minh
------------------------
Sắp thứ tự hàng/cột KHÔNG làm đổi một bit dữ liệu nào. Hai ma trận chứa đúng
cùng 416 ô có giá trị. Vậy mà bản alphabet trông như nhiễu rắc đều, còn bản sắp
theo cụm hiện ra ba khối vuông đặc nằm trên đường chéo. Toàn bộ cấu trúc nằm ở
THỨ TỰ, không nằm ở dữ liệu.

Đó là bài học của mục 9.1 giáo trình: với ma trận kề, thuật toán sắp lại hàng
cột (matrix reordering / seriation) chính là thuật toán trực quan hóa. Ở đây
thứ tự lấy từ cộng đồng Louvain đã tính ở T18, không phải sắp bằng tay.

Vì sao đặt hai ma trận cạnh nhau chứ không chỉ vẽ bản đẹp
---------------------------------------------------------
Nếu chỉ đưa bản đã sắp, người xem không có cách nào biết cấu trúc đó là thật hay
do mình sắp ra. Đặt cạnh bản alphabet thì phép so sánh tự nó là bằng chứng.

So với node-link
----------------
    ma trận    — tra một cặp nước bất kỳ là tức thì, không ô nào bị che, đọc
                 được mật độ trong từng khối. Nhưng mất hoàn toàn cảm giác về
                 hình dáng và về đường đi.
    node-link  — thấy hình dáng và nước nào nằm giữa, nhưng không tra nổi một
                 cặp cụ thể vì cạnh chồng lên nhau.

Chạy
----
    python src/make_adjacency.py
    python src/make_adjacency.py --year 2015
"""

from __future__ import annotations

import argparse
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import graph_common as GC  # noqa: E402
import reference_data as R  # noqa: E402

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    sys.exit("Thiếu plotly. Chạy: python -m pip install plotly kaleido")


def log(msg):
    print(msg)
    sys.stdout.flush()


def matrix(order, g):
    """Ma trận log10(giá trị xuất khẩu) theo thứ tự nút đã cho.

    Ô trống để None chứ không để 0: plotly bỏ qua None nên ô trống giữ đúng màu
    nền, còn để 0 thì nó bị tô bằng nấc thấp nhất của thang màu và cả ma trận
    biến thành một tấm kín đặc — không còn phân biệt được "không buôn" với
    "buôn rất ít".
    """
    idx = {n: i for i, n in enumerate(order)}
    m = [[None] * len(order) for _ in order]
    for s, t, d in g.edges(data=True):
        if s in idx and t in idx:
            m[idx[s]][idx[t]] = math.log10(max(d["weight"], 1.0))
    return m


def block_shapes(order, comm, axis_ref, color="#000000"):
    """Khung viền quanh mỗi khối cụm trên đường chéo — chỉ cho bản đã sắp.

    Vẽ khung để người xem thấy ranh giới khối là do cụm Louvain quyết định,
    không phải do mắt tự gom.
    """
    shapes = []
    start = 0
    for i in range(1, len(order) + 1):
        at_end = i == len(order)
        if at_end or comm.get(order[i]) != comm.get(order[start]):
            shapes.append(dict(
                type="rect", xref=axis_ref[0], yref=axis_ref[1],
                x0=start - 0.5, x1=i - 0.5, y0=start - 0.5, y1=i - 0.5,
                line=dict(color=color, width=1.4), fillcolor="rgba(0,0,0,0)",
                layer="above",
            ))
            start = i
    return shapes


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--seed", type=int, default=GC.DEFAULT_SEED)
    args = ap.parse_args()

    log("Dựng đồ thị đã lọc năm %d..." % args.year)
    gd = GC.load_graph(args.year, args.seed)
    g, comm, meta = gd["g"], gd["comm"], gd["meta"]
    log("  %d nút, %d cạnh" % (g.number_of_nodes(), g.number_of_edges()))

    orders = [("Thứ tự alphabet", GC.alpha_order(gd)),
              ("Thứ tự theo cụm Louvain", GC.community_order(gd))]

    fig = make_subplots(
        rows=1, cols=2, horizontal_spacing=0.085,
        subplot_titles=["<b>%s</b>" % t for t, _ in orders],
    )

    vals = [math.log10(max(d["weight"], 1.0)) for _, _, d in g.edges(data=True)]
    zmin, zmax = min(vals), max(vals)

    for k, (title, order) in enumerate(orders):
        m = matrix(order, g)
        labels = [n for n in order]           # mã ISO3: 73 nhãn thì tên đầy đủ
        names = [GC.name_vi(n, meta) for n in order]   # tên đầy đủ để hover
        fig.add_trace(go.Heatmap(
            z=m, x=labels, y=labels,
            colorscale=[[i / (len(R.SEQUENTIAL_SCALE) - 1), c]
                        for i, c in enumerate(R.SEQUENTIAL_SCALE)],
            zmin=zmin, zmax=zmax,
            showscale=(k == 1),
            colorbar=dict(
                title=dict(text="log₁₀ giá trị<br>xuất khẩu (USD)", side="right",
                           font=dict(size=R.FONT_SIZES["footnote"])),
                thickness=12, len=0.62, y=0.44,
                tickfont=dict(size=R.FONT_SIZES["footnote"]),
            ),
            hovertemplate=("<b>%{customdata[0]} → %{customdata[1]}</b>"
                           "<br>log₁₀ = %{z:.2f}<extra></extra>"),
            customdata=[[[names[i], names[j]] for j in range(len(order))]
                        for i in range(len(order))],
            xgap=0.4, ygap=0.4,
        ), row=1, col=k + 1)

    # Khung khối chỉ vẽ cho bản ĐÃ SẮP — đó mới là chỗ khối tồn tại.
    shapes = block_shapes(orders[1][1], comm, ("x2", "y2"))

    # Đánh dấu hàng và cột của Việt Nam trên CẢ HAI bản, để người xem bám theo
    # một nước cụ thể khi mắt chuyển từ hình trái sang hình phải.
    for k, (_, order) in enumerate(orders):
        if "VNM" not in order:
            continue
        i = order.index("VNM")
        xr = "x" if k == 0 else "x2"
        yr = "y" if k == 0 else "y2"
        n = len(order)
        shapes.append(dict(type="rect", xref=xr, yref=yr,
                           x0=-0.5, x1=n - 0.5, y0=i - 0.5, y1=i + 0.5,
                           line=dict(color=R.HIGHLIGHT_STROKE, width=0.9),
                           fillcolor="rgba(0,0,0,0)", layer="above"))
        shapes.append(dict(type="rect", xref=xr, yref=yr,
                           x0=i - 0.5, x1=i + 0.5, y0=-0.5, y1=n - 0.5,
                           line=dict(color=R.HIGHLIGHT_STROKE, width=0.9),
                           fillcolor="rgba(0,0,0,0)", layer="above"))

    n = len(orders[0][1])
    fig.update_layout(**GC.base_layout(
        title="Cùng một mạng lưới, chỉ đổi thứ tự hàng cột — và cấu trúc hiện ra",
        subtitle="Ma trận kề %d×%d, năm %d. Hai hình chứa ĐÚNG cùng %d luồng. "
                 "Bản trái sắp theo tên nước, bản phải sắp theo cụm Louvain. "
                 "Hàng và cột Việt Nam được kẻ đen trên cả hai bản."
                 % (n, n, args.year, g.number_of_edges()),
        note=GC.source_note(
            args.year,
            "Ô trống = hai nước này không có luồng nào qua ngưỡng, không phải "
            "giá trị 0. Thang màu là log₁₀ vì giá trị lệch 5 bậc độ lớn. "
            "Hàng = nước xuất, cột = nước nhập."),
        shapes=shapes,
        margin=dict(t=120, l=56, r=96, b=66),
        showlegend=False,
    ))

    tick = dict(tickfont=dict(size=5.4), tickangle=90, showgrid=False,
                ticks="", constrain="domain")
    fig.update_xaxes(**tick)
    fig.update_yaxes(tickfont=dict(size=5.4), showgrid=False, ticks="",
                     autorange="reversed", scaleanchor=None)
    fig.update_annotations(font_size=R.FONT_SIZES["legend"] + 2)

    GC.save(fig, "adjacency_%d" % args.year, width=1800, height=1000, log=log)

    # --- Bằng chứng: khối đặc hơn phần ngoài khối bao nhiêu lần? ----------
    log("")
    log("Mật độ trong khối so với ngoài khối — cơ sở của tiêu đề:")
    inside = outside = 0
    n_in = n_out = 0
    nodes = list(g.nodes())
    for a in nodes:
        for b in nodes:
            if a == b:
                continue
            same = comm.get(a) == comm.get(b)
            has = g.has_edge(a, b)
            if same:
                n_in += 1
                inside += 1 if has else 0
            else:
                n_out += 1
                outside += 1 if has else 0
    d_in = inside / n_in * 100 if n_in else 0
    d_out = outside / n_out * 100 if n_out else 0
    log("  trong cùng một khối : %4d/%5d cặp có luồng = %s"
        % (inside, n_in, R.fmt_pct(d_in)))
    log("  khác khối           : %4d/%5d cặp có luồng = %s"
        % (outside, n_out, R.fmt_pct(d_out)))
    if d_out > 0:
        log("  -> trong khối đặc gấp %s lần ngoài khối."
            % R.fmt_vn(d_in / d_out))
        log("     Đây là thứ mà bản sắp theo cụm cho thấy và bản alphabet giấu đi.")

    log("")
    log("Việt Nam trong ma trận:")
    vn_out = sorted(g.out_edges("VNM", data=True), key=lambda e: -e[2]["weight"])
    vn_in = sorted(g.in_edges("VNM", data=True), key=lambda e: -e[2]["weight"])
    log("  %d ô trên hàng (thị trường xuất), %d ô trên cột (nguồn nhập)"
        % (len(vn_out), len(vn_in)))
    for _, t, d in vn_out[:5]:
        log("    xuất sang %-14s %s" % (GC.name_vi(t, meta), R.fmt_usd(d["weight"])))


if __name__ == "__main__":
    main()

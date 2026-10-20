"""Node-link mạng thương mại đã lọc — bố cục force-directed (T15).

Hình này và ma trận kề ở T16 vẽ CÙNG MỘT đồ thị: 73 nút, 416 cạnh, năm 2023.
Cố ý như vậy, vì checklist nộp bài mục 5 yêu cầu so sánh trực tiếp hai họ biểu
diễn trên cùng dữ liệu. Đặt cạnh nhau thì thấy ngay mỗi họ mạnh ở đâu:

    node-link  — thấy được HÌNH DÁNG tổng thể và nước nào nằm giữa, nhưng
                 không tra được một cặp nước cụ thể vì cạnh chồng nhau.
    ma trận kề — tra một cặp là tức thì và không bao giờ bị che, nhưng mất
                 hoàn toàn cảm giác về hình dáng.

Ba quyết định thiết kế
----------------------
1. **Không có mũi tên** — quyết định B5. Đối ứng của mạng là 0,84, nghĩa là
   84% các cặp buôn cả hai chiều. Vẽ mũi tên hai đầu cho 84% số cạnh chỉ thêm
   mực mà không thêm thông tin. Chiều của dòng hàng nằm ở hover.

2. **Cộng đồng mã hóa bằng ĐỘ SÁNG và HÌNH DẠNG, không bằng màu** — lý do đo
   được, ghi ở ``reference_data.py`` mục COMMUNITY_FILL: bảng 10 màu ngành đã
   chiếm hết gam an toàn cho người mù màu, không còn chỗ cho ba màu nữa. Ba nấc
   xám giữ ΔE 20,1 với CẢ BA dạng mù màu, và còn đọc được với người đơn sắc.

3. **Kích thước nút theo CĂN BẬC HAI của độ mạnh** — vì mắt người đọc DIỆN
   TÍCH của hình tròn, không đọc bán kính. Lấy bán kính tỷ lệ thuận với giá trị
   thì nước lớn nhất sẽ trông lớn gấp bình phương lần thực tế.

Chạy
----
    python src/make_node_link.py
    python src/make_node_link.py --year 2015
    python src/make_node_link.py --seed 7       # đổi bố cục, không đổi cấu trúc
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import graph_common as GC  # noqa: E402
import reference_data as R  # noqa: E402

try:
    import networkx as nx
    import plotly.graph_objects as go
except ImportError:
    sys.exit("Thiếu networkx hoặc plotly. Chạy: python -m pip install networkx plotly kaleido")

# Nút nhỏ nhất và lớn nhất, tính theo pixel đường kính. Dưới 8px thì không
# bấm được bằng chuột, trên 46px thì nút che mất cạnh quanh nó.
SIZE_MIN, SIZE_MAX = 8.0, 46.0

# Cạnh chia thành ba nhóm độ dày. Plotly không cho mỗi đoạn một độ dày trong
# cùng một trace, nên muốn phân biệt thì phải tách trace — ba nhóm là đủ để
# thấy khác biệt mà vẫn chỉ thêm ba trace.
EDGE_TIERS = [
    # (phân vị dưới, phân vị trên, độ dày, độ mờ)
    (0.00, 0.60, 0.6, 0.18),
    (0.60, 0.90, 1.3, 0.30),
    (0.90, 1.00, 2.6, 0.48),
]

# Chỉ ghi nhãn cho nước đủ lớn hoặc nước trọng tâm. 73 nhãn cùng lúc thì chữ
# đè lên nhau thành một vệt đen — checklist mục 11.
LABEL_TOP_N = 14


def log(msg):
    print(msg)
    sys.stdout.flush()


def layout_positions(u, comm, seed):
    """Bố cục force-directed có GIEO MẦM THEO CỤM. Trả về {iso3: (x, y)}.

    Hai điều chỉnh so với spring_layout chạy trần, cả hai đều vì hình đầu tiên
    vẽ ra không đọc được:

    1. **Trọng số lấy log.** Giá trị thương mại lệch tới 5 bậc độ lớn. Đưa
       thẳng vào thì luồng Mexico–Hoa Kỳ kéo hai nút đó dính chặt vào nhau và
       đẩy 71 nút còn lại ra một vòng vô nghĩa ở ngoài.

    2. **Gieo mầm quanh ba tâm cụm thay vì gieo ngẫu nhiên.** spring_layout
       chạy trần cho ra một quả cầu đặc ở giữa, ba khối trộn lẫn — đúng thứ mà
       hình này đang muốn phân biệt. Đặt sẵn mỗi cụm quanh một đỉnh tam giác
       rồi mới chạy lực, thì lực nội cụm giữ khối lại với nhau còn lực giữa cụm
       chỉ kéo chúng xích vào. Bố cục force-directed là phương pháp lặp từ một
       điểm xuất phát: đổi điểm xuất phát là một tham số hợp lệ của phương
       pháp, không phải sắp đặt kết quả. Cấu trúc cụm do Louvain quyết định ở
       bước trước, hình chỉ hiển thị lại.
    """
    h = nx.Graph()
    for a, b, d in u.edges(data=True):
        h.add_edge(a, b, weight=math.log10(max(d["weight"], 1.0)))
    h.add_nodes_from(u.nodes())

    groups = sorted(set(comm.get(n, 0) for n in h.nodes()))
    rng = random.Random(seed)
    anchors = {}
    for i, c in enumerate(groups):
        ang = 2 * math.pi * i / max(1, len(groups)) - math.pi / 2
        anchors[c] = (math.cos(ang), math.sin(ang))

    init = {}
    for n in h.nodes():
        ax, ay = anchors.get(comm.get(n, groups[0]), (0.0, 0.0))
        init[n] = (ax + rng.uniform(-0.28, 0.28), ay + rng.uniform(-0.28, 0.28))

    return nx.spring_layout(h, pos=init, weight="weight", seed=seed,
                            iterations=250, k=0.9)


def label_position(x, y, cx, cy):
    """Đẩy nhãn ra PHÍA NGOÀI tâm hình, để nhãn tỏa ra thay vì chồng lên nhau.

    Plotly không có thuật toán tránh va chạm nhãn. Nhưng trong một hình mạng,
    nhãn gần như luôn va nhau ở vùng đặc ở giữa, còn phía ngoài thì trống. Đẩy
    mỗi nhãn ra hướng xa tâm là cách rẻ nhất giải quyết phần lớn va chạm: bốn
    hướng đủ để tách các nhãn kề nhau ra bốn phía khác nhau.
    """
    dx, dy = x - cx, y - cy
    if abs(dx) > abs(dy):
        return "middle right" if dx > 0 else "middle left"
    return "top center" if dy > 0 else "bottom center"


def percentile(vals, q):
    s = sorted(vals)
    if not s:
        return 0.0
    pos = (len(s) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(s) - 1)
    return s[lo] * (1 - (pos - lo)) + s[hi] * (pos - lo)


def _emit(fig, members, pos, comm, c, meta, u, strength, labelled, node_size,
          textposition, show_legend, legend_label):
    """Vẽ một nhóm nút cùng cụm VÀ cùng hướng nhãn thành một trace.

    Phải tách theo hướng nhãn vì plotly chỉ nhận MỘT ``textposition`` cho cả
    trace. Chỉ trace đầu của mỗi cụm hiện trong chú giải, các trace sau ẩn đi,
    nếu không chú giải sẽ có ba bốn dòng trùng tên cho cùng một cụm.
    """
    texts, hovers, widths, colors = [], [], [], []
    for n in members:
        nm = GC.name_vi(n, meta)
        texts.append(("<b>%s</b>" % nm) if n == "VNM"
                     else (nm if n in labelled else ""))
        hovers.append(
            "<b>%s</b><br>%s qua lại trong đồ thị đã lọc"
            "<br>%d đối tác ở đây · %s<extra></extra>"
            % (nm, R.fmt_usd(strength.get(n, 0)), u.degree(n),
               R.COMMUNITY_NAME_VI.get(c, "cụm %d" % c)))
        # Việt Nam: viền đen dày, theo quyết định B12.
        is_vn = n == "VNM"
        widths.append(R.HIGHLIGHT_STROKE_WIDTH + 1.0 if is_vn else 1.0)
        colors.append(R.HIGHLIGHT_STROKE if is_vn
                      else R.COMMUNITY_STROKE.get(c, "#FFFFFF"))
    fig.add_trace(go.Scatter(
        x=[pos[n][0] for n in members], y=[pos[n][1] for n in members],
        mode="markers+text",
        name=legend_label, showlegend=show_legend, legendgroup="cum%d" % c,
        marker=dict(
            size=[node_size(strength.get(n, 0)) for n in members],
            color=R.COMMUNITY_FILL.get(c, "#9A9A9A"),
            symbol=R.COMMUNITY_SYMBOL.get(c, "circle"),
            line=dict(color=colors, width=widths),
        ),
        text=texts, textposition=textposition,
        textfont=dict(size=R.FONT_SIZES["footnote"] + 1, color="#222222"),
        hovertemplate=hovers,
    ))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--seed", type=int, default=GC.DEFAULT_SEED)
    args = ap.parse_args()

    log("Dựng đồ thị đã lọc năm %d..." % args.year)
    gd = GC.load_graph(args.year, args.seed)
    g, u, comm, meta, strength = (gd["g"], gd["u"], gd["comm"], gd["meta"],
                                  gd["strength"])
    log("  %d nút, %d cạnh, %d cụm"
        % (g.number_of_nodes(), g.number_of_edges(), len(set(comm.values()))))

    log("Tính bố cục force-directed (seed=%d)..." % args.seed)
    pos = layout_positions(u, comm, args.seed)

    fig = go.Figure()

    # --- Cạnh, chia ba nhóm độ dày ----------------------------------------
    weights = [d["weight"] for _, _, d in u.edges(data=True)]
    cuts = [(percentile(weights, lo), percentile(weights, hi), w, op)
            for lo, hi, w, op in EDGE_TIERS]
    for i, (vlo, vhi, width, opacity) in enumerate(cuts):
        xs, ys = [], []
        for a, b, d in u.edges(data=True):
            w = d["weight"]
            # Nhóm cuối phải lấy cả biên trên, nếu không cạnh lớn nhất bị rơi
            # ra ngoài mọi nhóm và không được vẽ.
            inside = (vlo <= w < vhi) if i < len(cuts) - 1 else (vlo <= w <= vhi)
            if not inside:
                continue
            xs += [pos[a][0], pos[b][0], None]
            ys += [pos[a][1], pos[b][1], None]
        if not xs:
            continue
        fig.add_trace(go.Scatter(
            x=xs, y=ys, mode="lines", hoverinfo="skip", showlegend=False,
            line=dict(color="rgba(70,70,70,%.2f)" % opacity, width=width),
        ))

    # --- Nút, một trace cho mỗi cụm để chú giải tự sinh --------------------
    smax = max(strength.values()) or 1.0
    smin = min(strength.values())

    def node_size(v):
        # Căn bậc hai: mắt đọc diện tích, không đọc bán kính.
        t = (math.sqrt(v) - math.sqrt(smin)) / (math.sqrt(smax) - math.sqrt(smin))
        return SIZE_MIN + t * (SIZE_MAX - SIZE_MIN)

    ranked = sorted(g.nodes(), key=lambda n: -strength.get(n, 0))
    labelled = set(ranked[:LABEL_TOP_N]) | (set(R.FOCUS_ISO3) & set(g.nodes()))

    cx = sum(p[0] for p in pos.values()) / len(pos)
    cy = sum(p[1] for p in pos.values()) / len(pos)

    for c in sorted(set(comm.values())):
        members = [n for n in g.nodes() if comm.get(n) == c]
        members.sort(key=lambda n: -strength.get(n, 0))
        if not members:
            continue
        # Moi huong nhan la mot trace rieng: plotly chi nhan MOT textposition
        # cho ca trace, nen muon moi nhan mot huong thi phai tach ra.
        by_dir = {}
        for n in members:
            d = label_position(pos[n][0], pos[n][1], cx, cy) if n in labelled else "top center"
            by_dir.setdefault(d, []).append(n)
        first_of_community = True
        for tpos, group in by_dir.items():
            members_g = group
            _emit(fig, members_g, pos, comm, c, meta, u, strength, labelled,
                  node_size, tpos, show_legend=first_of_community,
                  legend_label="%s (%d nước)" % (
                      R.COMMUNITY_NAME_VI.get(c, "cụm %d" % c), len(members)))
            first_of_community = False
    vn_comm = comm.get("VNM")
    vn_members = sum(1 for v in comm.values() if v == vn_comm)

    fig.update_layout(**GC.base_layout(
        title="Việt Nam nằm trong khối châu Á do Trung Quốc dẫn đầu — "
              "không có khối ASEAN riêng",
        subtitle="Mạng thương mại %d sau khi lọc ngưỡng: %d nước, %d luồng. "
                 "Cỡ nút = tổng kim ngạch qua lại (theo diện tích). "
                 "Cụm mã hóa bằng độ sáng và hình dạng, không bằng màu. "
                 "Việt Nam viền đen. Thuật toán Louvain gom Việt Nam cùng %d "
                 "nước khác vào một khối."
                 % (args.year, g.number_of_nodes(), g.number_of_edges(),
                    vn_members - 1),
        note=GC.source_note(args.year,
                            "Không vẽ mũi tên: đối ứng 0,84 nên 84%% các cặp "
                            "buôn cả hai chiều (quyết định B5). Bố cục "
                            "force-directed, seed=%d — đổi seed thì hình xoay "
                            "nhưng cấu trúc cụm không đổi." % args.seed),
        xaxis=dict(visible=False, showgrid=False, zeroline=False),
        yaxis=dict(visible=False, showgrid=False, zeroline=False,
                   scaleanchor="x", scaleratio=1),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.0,
                    bgcolor="rgba(255,255,255,0.88)", bordercolor="#DDDDDD",
                    borderwidth=1, font=dict(size=R.FONT_SIZES["legend"])),
        margin=dict(t=110, l=10, r=10, b=56),
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="#888888"),
    ))

    GC.save(fig, "node_link_%d" % args.year, log=log)

    # --- Bằng chứng in ra, để không ai phải tin tiêu đề -------------------
    log("")
    log("Thành phần từng khối (cơ sở của tiêu đề):")
    for c in sorted(set(comm.values())):
        members = sorted((n for n in g.nodes() if comm.get(n) == c),
                         key=lambda n: -strength.get(n, 0))
        log("  %-38s %2d nước — lớn nhất: %s"
            % (R.COMMUNITY_NAME_VI.get(c, "cụm %d" % c), len(members),
               ", ".join(members[:6])))
    log("")
    asean = sorted(set(R.FOCUS_ISO3) & set(g.nodes()))
    log("10 nước ASEAN rơi vào khối nào:")
    for iso in asean:
        log("  %-4s %-14s khối %d — %s"
            % (iso, GC.name_vi(iso, meta), comm.get(iso, -1),
               R.COMMUNITY_SHORT_VI.get(comm.get(iso), "?")))
    same = len({comm.get(i) for i in asean})
    log("")
    if same == 1:
        log("  -> Cả %d nước ASEAN nằm CÙNG một khối, nhưng khối đó có %d nước"
            % (len(asean), vn_members))
        log("     và do Trung Quốc dẫn đầu. ASEAN KHÔNG hiện ra như một khối")
        log("     riêng — đây là phát hiện A8, và nó đi ngược trực giác.")
    else:
        log("  -> ASEAN bị chia ra %d khối khác nhau." % same)


if __name__ == "__main__":
    main()

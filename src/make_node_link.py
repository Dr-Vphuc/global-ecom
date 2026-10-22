"""Node-link của mạng thương mại đã lọc — T15.

Vẽ 73 nút và 416 cạnh còn lại sau quy tắc lọc của T10 (B4). Không vẽ đồ thị đầy
đủ: 27.535 cạnh trên 231 nút là mật độ 51,8%, vẽ ra chỉ còn một vệt đặc —
phát hiện A3 nói thẳng điều đó.

Năm quyết định, kèm lý do:

1. **Không mũi tên** — quyết định B5. Đối ứng của mạng là 0,84: hai nước đã mua
   của nhau thì gần như luôn bán cho nhau, nên chiều của cạnh gần như không
   thêm thông tin, trong khi 416 đầu mũi tên thì đủ sức làm hỏng hình.

2. **Gộp hai chiều thành MỘT cạnh.** 416 cạnh có hướng rút lại còn 271 cặp
   nước. Độ dày cạnh là **tổng giá trị hai chiều của những luồng vượt ngưỡng** —
   phải nói rõ vì có cặp chỉ một chiều lọt ngưỡng (Việt Nam bán sang Hoa Kỳ lọt,
   chiều ngược lại không), nên độ dày không phải "tổng thương mại hai nước".

3. **Kích thước nút theo bậc, DIỆN TÍCH tỉ lệ với bậc** (bán kính theo căn bậc
   hai). Bậc ở đây là bậc trong đồ thị đã lọc, từ 1 đến 92, chứ không phải số
   bạn hàng thật — Việt Nam có 166 bạn hàng nhưng chỉ 12 cặp vượt ngưỡng.

4. **Màu nút theo cụm Louvain, dùng bảng màu RIÊNG.** Quy tắc §3.1 của style
   guide: 10 màu ngành không được mượn sang chỉ cụm. Ba màu dưới đây đã đo bằng
   `src/check_palette.py`: ΔE2000 nhỏ nhất 24,7 ở mắt thường, 13,5 qua cả ba
   dạng mù màu, và cách mọi màu ngành ít nhất 20,0 — tức không ai nhầm cụm
   với ngành.

5. **Việt Nam nổi bằng hình, không bằng màu** — B12: viền đen 1,5px, nhãn in
   đậm, và 12 cạnh của Việt Nam vẽ đậm hơn phần còn lại.

Và một điều phải nói trước khi ai đó kỳ vọng nhầm: **tô màu theo cụm sẽ KHÔNG
làm ASEAN nổi lên.** Cả 10 nước ASEAN rơi vào cùng một cụm với Trung Quốc, Nhật,
Hàn, Ấn và vùng Vịnh — phát hiện A8. Đó là lý do Việt Nam phải dựa vào viền đậm.

Chạy
----
    python src/make_node_link.py
    python src/make_node_link.py --year 2015 --seed 7
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reference_data as R  # noqa: E402

try:
    import networkx as nx
except ImportError:
    sys.exit("Thiếu networkx. Chạy: python -m pip install -r requirements.txt")

try:
    import plotly.graph_objects as go
except ImportError:
    sys.exit("Thiếu plotly. Chạy: python -m pip install plotly kaleido")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "output")
EDGES_CSV = os.path.join(ROOT, "data", "processed", "edges.csv")
METRICS_CSV = os.path.join(ROOT, "data", "processed", "metrics.csv")

# Màu cụm nằm ở reference_data (cùng chỗ với màu ngành, và cùng đi qua
# src/check_palette.py). Gán theo CỠ cụm, không theo số hiệu Louvain.
COMMUNITY_PALETTE = R.COMMUNITY_PALETTE
COMMUNITY_FALLBACK = R.COMMUNITY_COLOR_FALLBACK

NODE_BORDER = "#FFFFFF"
EDGE_BINS = [
    # (phần trăm giá trị cặp, màu, độ dày) — cạnh càng lớn càng đậm và dày.
    (0.50, "rgba(176,176,176,0.40)", 0.5),
    (0.80, "rgba(150,150,150,0.55)", 0.9),
    (0.95, "rgba(110,110,110,0.70)", 1.6),
    (1.01, "rgba(70,70,70,0.85)", 2.6),
]
FOCUS_EDGE_COLOR = "rgba(0,0,0,0.75)"


# ---------------------------------------------------------------------------
# Dữ liệu
# ---------------------------------------------------------------------------
def load_nodes(year):
    """Các dòng `filtered` của metrics.csv, theo mã nước."""
    if not os.path.exists(METRICS_CSV):
        sys.exit("Chưa có %s.\nChạy trước: python src/compute_metrics.py" % METRICS_CSV)
    nodes = {}
    with open(METRICS_CSV, "r", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["graph"] == "filtered" and int(row["year"]) == year:
                nodes[row["country_iso3"]] = row
    if not nodes:
        sys.exit("metrics.csv không có dòng `filtered` cho năm %d.\n"
                 "Chạy: python src/compute_metrics.py --year %d" % (year, year))
    return nodes


def load_pairs(year, nodes):
    """Gộp cạnh có hướng thành cặp không hướng: {(a, b): tổng giá trị}.

    Chỉ giữ cạnh `above_threshold` và chỉ giữ cặp mà cả hai đầu đều nằm trong
    danh sách nút đã lọc — để hình và `metrics.csv` nói cùng một đồ thị.
    """
    pairs, n_directed = {}, 0
    with open(EDGES_CSV, "r", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if int(row["year"]) != year:
                continue
            if row["above_threshold"] not in ("True", "TRUE", "1"):
                continue
            a, b = row["source_iso3"], row["target_iso3"]
            if a not in nodes or b not in nodes:
                continue
            key = (a, b) if a < b else (b, a)
            pairs[key] = pairs.get(key, 0.0) + float(row["export_value"])
            n_directed += 1
    return pairs, n_directed


def community_order(nodes):
    """{số hiệu cụm: (thứ hạng cỡ, màu, nhãn tiếng Việt)}."""
    members = {}
    for iso, row in nodes.items():
        members.setdefault(row["community"], []).append(row)
    order = sorted(members, key=lambda c: -len(members[c]))
    out = {}
    for rank, cid in enumerate(order):
        top = sorted(members[cid], key=lambda r: -float(r["strength_total"]))[:3]
        label = "%s (%s nước)" % (
            ", ".join(t["country_name_vi"] for t in top),
            R.fmt_vn(len(members[cid]), 0))
        color = COMMUNITY_PALETTE.get(rank, COMMUNITY_FALLBACK)
        out[cid] = (rank, color, label)
    return out


# ---------------------------------------------------------------------------
# Bố cục
# ---------------------------------------------------------------------------
def layout(pairs, nodes, seed, kind="kamada"):
    """Xếp chỗ cho 73 nút. Hai cách, cùng một nguyên tắc: KHÔNG dùng trọng số.

    Có trọng số thì ba bốn cặp khổng lồ (Hoa Kỳ–Mexico, Hoa Kỳ–Canada,
    Trung Quốc–Hoa Kỳ) kéo mọi thứ về một điểm và phần còn lại dính thành vành
    ngoài không đọc được. Bố cục ở đây trả lời câu hỏi "ai nối với ai", còn độ
    lớn của luồng đã nằm ở độ dày cạnh rồi.

    `seed` cố định để chạy lại ra đúng hình cũ — không có nó thì mỗi lần render
    báo cáo lại ra một hình khác, và không ai đối chiếu được với bản đã in.
    """
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(pairs)
    if kind == "kamada":
        return nx.kamada_kawai_layout(g)
    return nx.spring_layout(g, seed=seed, k=1.9 / math.sqrt(len(nodes)),
                            iterations=400)


# ---------------------------------------------------------------------------
# Hình
# ---------------------------------------------------------------------------
def edge_traces(pairs, pos, focus):
    """Một trace cho mỗi nhóm độ dày, cộng một trace riêng cho cạnh Việt Nam."""
    vals = sorted(pairs.values())
    cuts = [vals[min(len(vals) - 1, int(q * len(vals)))] for q, _, _ in EDGE_BINS]

    buckets = [([], []) for _ in EDGE_BINS]
    focus_xy = ([], [])
    for (a, b), v in pairs.items():
        xs, ys = (focus_xy if focus in (a, b)
                  else buckets[next(i for i, c in enumerate(cuts) if v <= c)])
        xs += [pos[a][0], pos[b][0], None]
        ys += [pos[a][1], pos[b][1], None]

    traces = []
    for (xs, ys), (_, color, width) in zip(buckets, EDGE_BINS):
        if not xs:
            continue
        traces.append(go.Scatter(
            x=xs, y=ys, mode="lines", hoverinfo="skip", showlegend=False,
            line=dict(color=color, width=width),
        ))
    if focus_xy[0]:
        traces.append(go.Scatter(
            x=focus_xy[0], y=focus_xy[1], mode="lines", hoverinfo="skip",
            showlegend=False,
            line=dict(color=FOCUS_EDGE_COLOR, width=R.HIGHLIGHT_LINE_WIDTH),
        ))
    return traces


def edge_hover_trace(pairs, pos, nodes):
    """Chấm trong suốt ở giữa mỗi cạnh, chỉ để rê chuột đọc được giá trị.

    Bản PNG không có hover nên chấm này vô hình ở đó; bản HTML thì nhờ nó mà
    271 cạnh tra được giá trị, thay vì phải mở lại edges.csv.
    """
    xs, ys, texts = [], [], []
    for (a, b), v in pairs.items():
        xs.append((pos[a][0] + pos[b][0]) / 2)
        ys.append((pos[a][1] + pos[b][1]) / 2)
        texts.append("<b>%s ↔ %s</b><br>%s (tổng hai chiều, phần vượt ngưỡng)"
                     "<extra></extra>"
                     % (nodes[a]["country_name_vi"], nodes[b]["country_name_vi"],
                        R.fmt_usd(v)))
    return go.Scatter(x=xs, y=ys, mode="markers", showlegend=False,
                      marker=dict(size=7, color="rgba(0,0,0,0)"),
                      hovertemplate=texts)


def node_traces(nodes, pos, comm, focus, n_named):
    """Một trace cho mỗi cụm (để có chú giải), cộng một trace cho Việt Nam."""
    ranked = sorted(nodes.values(), key=lambda r: -float(r["strength_total"]))
    named = {r["country_iso3"] for r in ranked[:n_named]}

    def size_of(row):
        # Diện tích tỉ lệ với bậc -> bán kính theo căn bậc hai. Nếu lấy đường
        # kính tỉ lệ thẳng với bậc thì nút Trung Quốc (bậc 92) sẽ rộng gấp 92
        # lần nút nhỏ nhất và nuốt cả hình.
        return 7.0 + 3.1 * math.sqrt(int(row["degree_total"]))

    def label_of(row):
        iso = row["country_iso3"]
        if iso == focus:
            return "<b>%s</b>" % row["country_name_vi"]
        if iso in named:
            return row["country_name_vi"]
        if row["is_focus"] in ("TRUE", "True", "1"):
            return iso          # 9 nước ASEAN còn lại: nhãn ngắn, khỏi che hình
        return ""

    cx = sum(p[0] for p in pos.values()) / len(pos)
    cy = sum(p[1] for p in pos.values()) / len(pos)

    def textpos_of(row):
        """Đẩy nhãn ra PHÍA NGOÀI tâm hình.

        Để mặc định "top center" thì ở giữa — chỗ đông nút nhất — nhãn chồng
        lên nhau và lên cạnh. Đẩy theo hướng xuyên tâm thì mỗi nhãn tự tránh
        phần rậm rạp mà không cần thuật toán né nhãn nào.
        """
        x, y = pos[row["country_iso3"]]
        dx, dy = x - cx, y - cy
        if abs(dx) > abs(dy):
            return "middle right" if dx > 0 else "middle left"
        return "top center" if dy > 0 else "bottom center"

    def hover_of(row):
        return ("<b>%s</b><br>%s<br>%s cạnh (%s vào · %s ra)<br>"
                "Tổng luồng vượt ngưỡng: %s<extra></extra>"
                % (row["country_name_vi"], comm[row["community"]][2],
                   R.fmt_vn(int(row["degree_total"]), 0),
                   R.fmt_vn(int(row["degree_in"]), 0),
                   R.fmt_vn(int(row["degree_out"]), 0),
                   R.fmt_usd(float(row["strength_total"]))))

    traces = []
    for cid in sorted(comm, key=lambda c: comm[c][0]):
        rows = [r for r in ranked
                if r["community"] == cid and r["country_iso3"] != focus]
        traces.append(go.Scatter(
            x=[pos[r["country_iso3"]][0] for r in rows],
            y=[pos[r["country_iso3"]][1] for r in rows],
            mode="markers+text", name=comm[cid][2],
            marker=dict(size=[size_of(r) for r in rows], color=comm[cid][1],
                        line=dict(color=NODE_BORDER, width=1)),
            text=[label_of(r) for r in rows],
            textposition=[textpos_of(r) for r in rows],
            textfont=dict(size=R.FONT_SIZES["annotation"], color="#333333"),
            hovertemplate=[hover_of(r) for r in rows],
        ))

    row = nodes.get(focus)
    if row:
        traces.append(go.Scatter(
            x=[pos[focus][0]], y=[pos[focus][1]], mode="markers+text",
            name="%s — viền đen theo B12" % row["country_name_vi"],
            marker=dict(size=size_of(row), color=comm[row["community"]][1],
                        line=dict(color=R.HIGHLIGHT_STROKE,
                                  width=R.HIGHLIGHT_STROKE_WIDTH)),
            text=[label_of(row)], textposition=textpos_of(row),
            textfont=dict(size=R.FONT_SIZES["annotation"] + 1, color="#000000"),
            hovertemplate=[hover_of(row)],
        ))
    return traces


# Khung tính bằng POINT theo B16 — xem reference_data.xuat_png.
FIG_H_INCH = 6.60
MARGIN_X = 8.0
TEXT_PAD = 6.0
LINE_H = 1.33
LEG_BAND = 48.0        # chú giải cụm, xếp ngang, cuộn thành hai hàng


def _go_nhan_chong(fig, x_rng, y_rng, plot_w, plot_h):
    """Bỏ bớt nhãn nút cho đến khi không còn nhãn nào chồng nhãn nào.

    Đặt nhãn theo hướng xuyên tâm là đủ khi chữ còn in ra ~3 pt như trước khi
    sửa lỗi đơn vị B16. Ở cỡ chữ ĐÚNG, chữ to gấp 2,78 lần nên vùng giữa — chỗ
    đông nút nhất — chồng chéo hẳn: "Trung Quốc" đè "Nhật Bản", "Hoa Kỳ" đè
    "Đài Loan". Nên xếp nhãn theo thứ tự ưu tiên (Việt Nam trước, rồi nút to
    dần xuống) và nhãn nào không còn chỗ trống thì BỎ, chứ không chồng.

    Trục đã khoá tỉ lệ 1:1 (scaleanchor) nên hai chiều dùng chung một hệ số.
    """
    sx = (x_rng[1] - x_rng[0]) or 1.0
    sy = (y_rng[1] - y_rng[0]) or 1.0
    k = min(plot_w / sx, plot_h / sy)
    ds = []
    for ti, tr in enumerate(fig.data):
        if not getattr(tr, "text", None) or "text" not in (tr.mode or ""):
            continue
        sizes = tr.marker.size
        if not isinstance(sizes, (list, tuple)):
            sizes = [sizes] * len(tr.text)
        pos = tr.textposition
        if not isinstance(pos, (list, tuple)):
            pos = [pos] * len(tr.text)
        fs = tr.textfont.size or R.FONT_SIZES["annotation"]
        for pi, lab in enumerate(tr.text):
            if not lab:
                continue
            ds.append(dict(ti=ti, pi=pi, lab=lab, fs=fs,
                           r=(sizes[pi] or 8) / 2.0,
                           px=(tr.x[pi] - x_rng[0]) * k,
                           py=(y_rng[1] - tr.y[pi]) * k,
                           pos=pos[pi] or "top center"))
    # Việt Nam (nhãn in đậm) đứng trước, rồi nút to dần xuống.
    ds.sort(key=lambda d: (0 if "<b>" in d["lab"] else 1, -d["r"]))

    placed, bo = [], {}
    for d in ds:
        n = len(d["lab"].replace("<b>", "").replace("</b>", ""))
        w = n * d["fs"] * 0.52
        h = d["fs"] * 1.33
        pad = d["r"] + 2.0
        if d["pos"] == "middle right":
            x0, y0 = d["px"] + pad, d["py"] - h / 2.0
        elif d["pos"] == "middle left":
            x0, y0 = d["px"] - pad - w, d["py"] - h / 2.0
        elif d["pos"] == "bottom center":
            x0, y0 = d["px"] - w / 2.0, d["py"] + pad
        else:
            x0, y0 = d["px"] - w / 2.0, d["py"] - pad - h
        box = (x0, y0, x0 + w, y0 + h)
        if any(box[0] < q[2] and q[0] < box[2]
               and box[1] < q[3] and q[1] < box[3] for q in placed):
            bo.setdefault(d["ti"], []).append(d["pi"])
            continue
        placed.append(box)
    n_bo = 0
    for ti, idx in bo.items():
        txt = list(fig.data[ti].text)
        for pi in idx:
            txt[pi] = ""
            n_bo += 1
        fig.data[ti].text = txt
    print("  Nhãn nút: giữ %s, bỏ %s vì không còn chỗ trống"
          % (R.fmt_vn(len(placed), 0), R.fmt_vn(n_bo, 0)))


def _span(vals, pad=0.09):
    """Khoảng trục bám sát dữ liệu, chừa lề cho nhãn nút khỏi bị cắt."""
    lo, hi = min(vals), max(vals)
    m = (hi - lo) * pad
    return [lo - m, hi + m]


def make_figure(nodes, pairs, pos, comm, year, focus, n_directed, n_named):
    fig = go.Figure()
    for t in edge_traces(pairs, pos, focus):
        fig.add_trace(t)
    fig.add_trace(edge_hover_trace(pairs, pos, nodes))
    for t in node_traces(nodes, pos, comm, focus, n_named):
        fig.add_trace(t)

    frow = nodes.get(focus)
    fpairs = sorted(((v, k) for k, v in pairs.items() if focus in k), reverse=True)
    biggest = ""
    if fpairs:
        v, k = fpairs[0]
        other = k[0] if k[1] == focus else k[1]
        biggest = (" Cạnh dày nhất của %s là %s — %s."
                   % (nodes[focus]["country_name_vi"],
                      nodes[other]["country_name_vi"], R.fmt_usd(v)))

    # Tiêu đề dựng từ dữ liệu, không viết cứng: mỗi cụm gọi theo nước mạnh nhất
    # trong cụm đó, xếp theo cỡ cụm. Chạy năm khác ra cụm khác thì câu tiêu đề
    # tự đổi theo, không bị nói sai.
    heads = []
    for cid in sorted(comm, key=lambda c: comm[c][0]):
        top = max((r for r in nodes.values() if r["community"] == cid),
                  key=lambda r: float(r["strength_total"]))
        heads.append(top["country_name_vi"])
    if frow and len(heads) == 3:
        title = ("<b>Mạng chia thành ba cực — quanh %s, quanh %s và quanh %s — "
                 "và %s nằm trong cực %s</b>"
                 % (heads[0], heads[1], heads[2], frow["country_name_vi"],
                    heads[comm[frow["community"]][0]]))
    elif frow:
        title = ("<b>%s cực trong mạng lưới đã lọc — %s nằm trong cực %s</b>"
                 % (R.fmt_vn(len(heads), 0), frow["country_name_vi"],
                    heads[comm[frow["community"]][0]]))
    else:
        title = "<b>Mạng lưới thương mại đã lọc, năm %d</b>" % year

    # --- khối chữ đặt tay theo B16 (khung point) ---------------------------
    # layout.title không tự ngắt dòng; ở khung point câu tiêu đề dài sẽ tràn
    # khỏi mép khung. Và thẻ <b> trong `title` phải bóc ra vì khối chữ bây giờ
    # tự đặt cỡ, không nhờ plotly.
    tit = title.replace("<b>", "").replace("</b>", "")
    sub = ("Năm %d · %s nút, %s cạnh có hướng gộp thành %s cặp nước. Cỡ nút "
           "theo bậc (diện tích tỉ lệ với bậc), độ dày cạnh theo tổng giá trị "
           "hai chiều của phần vượt ngưỡng, màu theo cụm Louvain. Không mũi "
           "tên — quyết định B5.%s"
           % (year, R.fmt_vn(len(nodes), 0), R.fmt_vn(n_directed, 0),
              R.fmt_vn(len(pairs), 0), biggest))
    note = ("Cụm Louvain KHÔNG tách được ASEAN: cả 10 nước ASEAN nằm chung một "
            "cụm với Trung Quốc, Nhật, Hàn, Ấn và vùng Vịnh (phát hiện A8) — "
            "nên Việt Nam nhận viền đen, không nhận màu riêng.")
    src = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab). Đồ thị "
           "đã lọc theo quy tắc T10: giữ cạnh ≥ 0,046% tổng xuất khẩu thế "
           "giới, cộng top 3 luồng xuất và nhập của mỗi nước ASEAN.")

    w_pt, h_pt = R.khung_pt(R.FIG_WIDTH_FULL), R.khung_pt(FIG_H_INCH)
    t_w = w_pt - 2 * MARGIN_X - 2 * TEXT_PAD
    tw = R.wrap_pt(tit, R.FONT_SIZES["title"], t_w)
    sw = R.wrap_pt(sub, R.FONT_SIZES["subtitle"], t_w)
    nw = R.wrap_pt(note, R.FONT_SIZES["annotation"], t_w)
    cw = R.wrap_pt(src, R.FONT_SIZES["footnote"], t_w)
    h_title = R.n_lines(tw) * R.FONT_SIZES["title"] * LINE_H
    h_sub = R.n_lines(sw) * R.FONT_SIZES["subtitle"] * LINE_H
    h_note = R.n_lines(nw) * R.FONT_SIZES["annotation"] * LINE_H
    h_src = R.n_lines(cw) * R.FONT_SIZES["footnote"] * LINE_H
    m_t = TEXT_PAD + h_title + h_sub + TEXT_PAD
    m_b = LEG_BAND + h_note + h_src + 2 * TEXT_PAD
    plot_h = h_pt - m_t - m_b

    fig.update_layout(
        font=dict(family=", ".join(R.FONT_STACK), size=R.FONT_SIZES["legend"]),
        separators=",.",
        margin=dict(t=m_t, l=MARGIN_X, r=MARGIN_X, b=m_b),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        legend=dict(orientation="h", y=-(4.0 / plot_h), x=0, xanchor="left",
                    yanchor="top", font=dict(size=R.FONT_SIZES["footnote"])),
        hovermode="closest",
        xaxis=dict(visible=False, showgrid=False, zeroline=False,
                   range=_span([p[0] for p in pos.values()])),
        yaxis=dict(visible=False, showgrid=False, zeroline=False,
                   scaleanchor="x", scaleratio=1,
                   range=_span([p[1] for p in pos.values()])),
    )

    def ann(text, y, size, color):
        fig.add_annotation(text=text, showarrow=False, xref="paper",
                           yref="paper", x=0, y=y,
                           xshift=-(MARGIN_X - TEXT_PAD), xanchor="left",
                           yanchor="top", align="left",
                           font=dict(size=size, color=color))

    ann(tw, 1 + (m_t - TEXT_PAD) / plot_h, R.FONT_SIZES["title"], None)
    ann(sw, 1 + (m_t - TEXT_PAD - h_title) / plot_h,
        R.FONT_SIZES["subtitle"], "#555555")
    ann(nw, -(LEG_BAND / plot_h), R.FONT_SIZES["annotation"], "#444444")
    ann(cw, -((LEG_BAND + h_note) / plot_h), R.FONT_SIZES["footnote"], "#777777")

    _go_nhan_chong(fig, _span([p[0] for p in pos.values()]),
                   _span([p[1] for p in pos.values()]),
                   w_pt - 2 * MARGIN_X, plot_h)
    return fig


def save(fig, name):
    os.makedirs(OUTDIR, exist_ok=True)
    html = os.path.join(OUTDIR, name + ".html")
    fig.write_html(html, include_plotlyjs="cdn", config={"displayModeBar": False})
    print("  %s" % html)
    try:
        png = os.path.join(OUTDIR, name + ".png")
        R.xuat_png(fig, png, R.FIG_WIDTH_FULL, FIG_H_INCH)
        print("  %s" % png)
    except Exception as exc:
        print("  (không xuất được PNG: %s — bản .html vẫn dùng được)" % exc)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--focus", default="VNM")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--layout", choices=("kamada", "spring"), default="kamada")
    ap.add_argument("--named", type=int, default=16,
                    help="số nút lớn nhất được ghi tên (mặc định 16)")
    args = ap.parse_args()

    print("Đọc đồ thị đã lọc năm %d..." % args.year)
    nodes = load_nodes(args.year)
    pairs, n_directed = load_pairs(args.year, nodes)
    comm = community_order(nodes)
    print("  %s nút · %s cạnh có hướng · %s cặp nước"
          % (R.fmt_vn(len(nodes), 0), R.fmt_vn(n_directed, 0),
             R.fmt_vn(len(pairs), 0)))

    print("Xếp bố cục (%s)..." % args.layout)
    pos = layout(pairs, nodes, args.seed, args.layout)

    print("Dựng biểu đồ:")
    fig = make_figure(nodes, pairs, pos, comm, args.year, args.focus,
                      n_directed, args.named)
    save(fig, "node_link_%d" % args.year if args.layout == "kamada"
         else "node_link_%d_%s" % (args.year, args.layout))

    print("\nBa cụm:")
    for cid in sorted(comm, key=lambda c: comm[c][0]):
        members = [r for r in nodes.values() if r["community"] == cid]
        asean = [r["country_iso3"] for r in members
                 if r["is_focus"] in ("TRUE", "True", "1")]
        print("  %s %s" % (COMMUNITY_PALETTE.get(comm[cid][0], COMMUNITY_FALLBACK),
                           comm[cid][2]))
        if asean:
            print("      chứa %d nước ASEAN: %s" % (len(asean), ", ".join(sorted(asean))))

    row = nodes.get(args.focus)
    if row:
        fp = sorted(((v, k) for k, v in pairs.items() if args.focus in k), reverse=True)
        print("\n%s trong đồ thị đã lọc: %s cặp nước, tổng luồng %s"
              % (row["country_name_vi"], R.fmt_vn(len(fp), 0),
                 R.fmt_usd(float(row["strength_total"]))))
        for v, k in fp[:5]:
            other = k[0] if k[1] == args.focus else k[1]
            print("    %-22s %s" % (nodes[other]["country_name_vi"], R.fmt_usd(v)))


if __name__ == "__main__":
    main()

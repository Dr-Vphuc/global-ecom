# -*- coding: utf-8 -*-
"""Hai ma trận kề của đồ thị đã lọc — T16.

Cùng một dữ liệu, hai cách xếp hàng/cột:

    --order alpha     73 nước theo mã ISO3 A→Z
    --order cluster   73 nước theo cụm Louvain, trong mỗi cụm xếp theo độ mạnh

Đổi thứ tự hàng/cột **không đổi một ô nào** — cùng số ô, cùng tổng giá trị,
cùng ma trận. Nó chỉ đổi chỗ ngồi. Điều phải chứng minh là: chỗ ngồi mới làm
hiện ra cấu trúc khối mà chỗ ngồi cũ giấu đi. Nên script này **đo** mức hiện ra
đó chứ không chỉ nói, bằng hai con số:

1. **Khoảng cách trung bình tới đường chéo** — với mỗi ô có giá trị, lấy
   `|i − j| / (n − 1)` rồi trung bình **có trọng số theo giá trị luồng**. Số
   này phụ thuộc thứ tự, nên nó chính là thứ đo được "hiện ra bao nhiêu".
   Mốc so sánh là 300 lần xếp ngẫu nhiên: một thứ tự vô nghĩa cho ra ≈ 1/3.
   Trọng số theo giá trị vì ma trận tô màu theo giá trị — thước đo phải đo
   đúng cái mắt nhìn thấy, không phải đếm ô suông.
2. **Tỉ lệ giá trị nằm TRONG khối** — tổng giá trị các luồng có hai đầu cùng
   cụm, chia cho tổng tất cả. Số này *không* phụ thuộc thứ tự: nó là tính chất
   của phân hoạch, và chính nó là cái mà bản xếp theo cụm cho nhìn thấy.

Hai con số đi cùng nhau mới đủ: (1) nói "xếp lại thì gọn hơn", (2) nói "gọn
quanh cái gì". Cả hai đều in ra ở khối kiểm chứng và đều nằm trên tiêu đề.

Năm quyết định, kèm lý do
-------------------------
1. **Ma trận giữ HƯỚNG** — hàng là nước xuất, cột là nước nhập. B13 gộp hai
   chiều thành một cạnh, nhưng đó là quyết định cho node-link, nơi hai nửa cạnh
   song song chỉ làm dày hình. Ma trận có sẵn hai ô cho hai chiều nên không mất
   gì khi giữ, và được thêm một thông tin node-link không vẽ nổi: ma trận gần
   đối xứng chính là đối ứng 0,84 của A3, nhìn thấy được.

2. **Màu theo log10 giá trị**, thang `SEQUENTIAL_SCALE`. Giá trị trải gần 3 bậc
   10 (0,49 → 480 tỷ USD năm 2023); tô tuyến tính thì 9/10 số ô cùng một màu
   nhạt và ma trận chỉ còn nói "có hay không có".

3. **Ô trống ≠ ô giá trị nhỏ.** Nền xám `#E8E8E8` cho ô không có luồng vượt
   ngưỡng, vì nấc nhạt nhất của thang (`#FFFFE5`) gần như trắng — để nền trắng
   thì "không có luồng" và "luồng nhỏ nhất" trông giống hệt nhau.

4. **Chỉ ghi nhãn 13 nước, không ghi 73** — quyết định B15, xem khối kiểm
   chứng: cạnh ma trận ~320pt chia cho 73 nhãn còn ~4,4pt mỗi nhãn, dưới sàn
   7pt của style guide. 13 nhãn (10 nước ASEAN + nước mạnh nhất mỗi cụm) được
   ~25pt mỗi nhãn. Bù lại, bản xếp theo cụm ghi nhãn theo KHỐI ở lề phải.

5. **Khung hình tính bằng POINT, không bằng pixel** — xem B16. Layout rộng
   `6,30 inch × 72 = 453,6`, nên mỗi con số trong `FONT_SIZES` là point thật
   khi in ở khổ 6,30 inch, và sàn 7pt kiểm được bằng phép trừ.

Việt Nam nổi bằng hình dạng chứ không bằng màu (B12): hàng và cột của Việt Nam
được đóng khung đen, nhãn in đậm. Không có màu thứ 11 nào được thêm vào.

Chạy
----
    python src/make_adjacency_matrix.py --year 2023
    python src/make_adjacency_matrix.py --year 1995
    python src/make_adjacency_matrix.py --year 2023 --order cluster
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reference_data as R  # noqa: E402

try:
    import networkx as nx
    from networkx.algorithms import community as nx_comm
except ImportError:
    sys.exit("Thiếu networkx. Chạy: python -m pip install -r requirements.txt")

try:
    import plotly.graph_objects as go
except ImportError:
    sys.exit("Thiếu plotly. Chạy: python -m pip install plotly kaleido")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "output")
EDGES_CSV = os.path.join(ROOT, "data", "processed", "edges.csv")
NODES_CSV = os.path.join(ROOT, "data", "processed", "nodes.csv")
METRICS_CSV = os.path.join(ROOT, "data", "processed", "metrics.csv")

# Khung hình tính bằng POINT. 6,30 inch = 453,6pt, nên 1 đơn vị layout = 1pt
# in thật, và FONT_SIZES là point thật chứ không phải point danh nghĩa.
PT_PER_INCH = 72.0
CANVAS_PT = R.FIG_WIDTH_FULL * PT_PER_INCH          # 453,6 — hình vuông
LABEL_FLOOR_PT = 7.0                                 # sàn của style-guide §7

EMPTY_CELL = "#E8E8E8"      # ô không có luồng vượt ngưỡng
BLOCK_LINE = "#3A3A3A"      # viền khối cụm — xám trung tính, không phải màu ngành
DIAG_LINE = "#C4C4C4"       # đường chéo, để dò từ một cột về hàng cùng tên
LEADER = "#9A9A9A"          # nét dẫn từ nhãn về đúng hàng của nó
N_SHUFFLE = 300             # số lần xếp ngẫu nhiên để lấy mốc so sánh

# Lề trái / phải cố định; lề trên và dưới tính từ số dòng chữ thật (xem
# `layout_margins`), vì khung chỉ cao 453,6pt — đoán thừa một dòng là tiêu đề
# đè lên ma trận, đoán thiếu một dòng là chữ bị cắt mép.
MARGIN_L = 50
MARGIN_R = 44
LEADER_PT = 7.0             # bề ngang rãnh nét dẫn
LINE_H = 1.33               # giãn dòng, nhân với cỡ chữ
CB_BLOCK = 46.0             # chỗ cho thanh màu: khe hở + tên + thanh + mốc
TEXT_PAD = 6.0              # lề của khối chữ so với mép khung
TEXT_W = CANVAS_PT - 2 * TEXT_PAD   # bề ngang tối đa của một dòng chữ

SOURCE_TEXT = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab). "
               "Đồ thị đã lọc theo quy tắc T10 (B4).")


# ---------------------------------------------------------------------------
# Dữ liệu
# ---------------------------------------------------------------------------
def load_names():
    """{ISO3: (tên tiếng Việt, có phải nước ASEAN)} — lấy ở nodes.csv."""
    if not os.path.exists(NODES_CSV):
        sys.exit("Chưa có %s.\nChạy trước: python src/build_intermediate.py"
                 % NODES_CSV)
    out = {}
    with open(NODES_CSV, "r", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[row["country_iso3"]] = (
                row["country_name_vi"],
                row["is_focus"] in ("TRUE", "True", "1"))
    return out


def load_edges(year):
    """Các luồng `above_threshold` của năm — [(nước xuất, nước nhập, USD)]."""
    if not os.path.exists(EDGES_CSV):
        sys.exit("Chưa có %s.\nChạy trước: python src/build_intermediate.py"
                 % EDGES_CSV)
    out = []
    with open(EDGES_CSV, "r", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if int(row["year"]) != year:
                continue
            if row["above_threshold"] not in ("TRUE", "True", "1"):
                continue
            out.append((row["source_iso3"], row["target_iso3"],
                        float(row["export_value"])))
    if not out:
        sys.exit("Không có cạnh nào vượt ngưỡng ở năm %d." % year)
    return out


def louvain_communities(edges, seed):
    """Cụm Louvain trên phép chiếu vô hướng — đúng công thức của T18.

    Gộp hai chiều trước khi dò cụm: cộng đồng thương mại là chuyện ai buôn với
    ai, không phải chiều của dòng hàng. Đánh số lại theo CỠ cụm giảm dần, nên
    cụm 0 luôn là cụm đông nhất — B14 khóa màu và thứ tự theo thứ hạng cỡ cụm
    chứ không theo số hiệu Louvain vốn là nhãn tùy ý.
    """
    g = nx.Graph()
    for s, t, v in edges:
        if g.has_edge(s, t):
            g[s][t]["weight"] += v
        else:
            g.add_edge(s, t, weight=v)
    parts = sorted(nx_comm.louvain_communities(g, weight="weight", seed=seed),
                   key=len, reverse=True)
    comm = {}
    for rank, group in enumerate(parts):
        for iso in group:
            comm[iso] = rank
    return comm, [len(p) for p in parts], nx_comm.modularity(g, parts,
                                                             weight="weight")


def metrics_communities(year):
    """Cột `community` của các dòng đồ thị `filtered` trong metrics.csv."""
    if not os.path.exists(METRICS_CSV):
        return {}
    out = {}
    with open(METRICS_CSV, "r", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["graph"] == "filtered" and int(row["year"]) == year:
                out[row["country_iso3"]] = int(row["community"])
    return out


def strengths(edges):
    """Tổng giá trị luồng vượt ngưỡng chạm vào mỗi nước (vào + ra).

    Bằng đúng cột `strength_total` ở dòng `filtered` của metrics.csv — đã đối
    chiếu 73/73 nước năm 2023, lệch 0. Tính tại chỗ để năm nào cũng chạy được,
    kể cả năm metrics.csv chưa có.
    """
    out = {}
    for s, t, v in edges:
        out[s] = out.get(s, 0.0) + v
        out[t] = out.get(t, 0.0) + v
    return out


# ---------------------------------------------------------------------------
# Thước đo
# ---------------------------------------------------------------------------
def diagonal_distance(edges, pos, n):
    """Khoảng cách trung bình tới đường chéo, 0 = sát chéo, 1 = hai góc xa nhất.

    Trả về (có trọng số theo giá trị, không trọng số). Thứ tự hàng/cột đi vào
    qua `pos`; đổi thứ tự là đổi số này, còn tập ô thì không đổi — đó đúng là
    điều hình này phải chứng minh.
    """
    if n < 2:
        return 0.0, 0.0
    total = sum(v for _, _, v in edges)
    w = sum(v * abs(pos[s] - pos[t]) for s, t, v in edges) / total / (n - 1)
    u = sum(abs(pos[s] - pos[t]) for s, t, _ in edges) / len(edges) / (n - 1)
    return w, u


def shuffle_baseline(edges, isos, seed):
    """Mốc so sánh: thứ tự vô nghĩa thì khoảng cách tới đường chéo bằng bao nhiêu.

    Không có mốc này thì con số 0,26 không đọc được — thấp so với cái gì?
    """
    rng = random.Random(seed)
    vals = []
    for _ in range(N_SHUFFLE):
        order = list(isos)
        rng.shuffle(order)
        pos = {iso: i for i, iso in enumerate(order)}
        vals.append(diagonal_distance(edges, pos, len(isos))[0])
    vals.sort()
    return vals[len(vals) // 2], vals[0], vals[-1]


def within_block(edges, comm):
    """(tỉ lệ GIÁ TRỊ trong khối, số ô trong khối, tổng số ô)."""
    total = sum(v for _, _, v in edges)
    inside = sum(v for s, t, v in edges if comm[s] == comm[t])
    cells = sum(1 for s, t, _ in edges if comm[s] == comm[t])
    return inside / total, cells, len(edges)


def block_density(edges, comm, sizes, n):
    """Mật độ ô trong khối so với ngoài khối — "khối đậm hơn nền mấy lần"."""
    cells_in = sum(s * (s - 1) for s in sizes)
    cells_off = n * (n - 1) - cells_in
    hit_in = sum(1 for s, t, _ in edges if comm[s] == comm[t])
    hit_off = len(edges) - hit_in
    d_in = hit_in / cells_in if cells_in else 0.0
    d_off = hit_off / cells_off if cells_off else 0.0
    return d_in, d_off, (d_in / d_off if d_off else float("inf"))


# ---------------------------------------------------------------------------
# Thứ tự hàng/cột
# ---------------------------------------------------------------------------
def order_alpha(isos):
    return sorted(isos)


def order_cluster(isos, comm, stren):
    """Cụm đông nhất trước; trong mỗi cụm, nước mạnh nhất lên đầu khối.

    Xếp theo độ mạnh trong khối để góc trên-trái của mỗi khối là chỗ đậm nhất —
    khối đọc được ngay cả khi người xem không biết tên nước nào.
    """
    return sorted(isos, key=lambda k: (comm[k], -stren.get(k, 0.0), k))


# ---------------------------------------------------------------------------
# Chữ
# ---------------------------------------------------------------------------
def wrap_pt(text, font_pt, width_pt, ratio=0.52):
    """Ngắt dòng theo BỀ RỘNG THẬT tính bằng point, không theo số ký tự đoán mò.

    `ratio` là bề rộng trung bình một ký tự so với cỡ chữ, đo xấp xỉ cho
    Segoe UI / Arial. Khung hình chỉ rộng 453,6pt nên một dòng 13pt chỉ chứa
    khoảng 67 ký tự — ngắt sai là tiêu đề tràn ra ngoài mép.
    """
    limit = max(8, int(width_pt / (font_pt * ratio)))
    lines, cur = [], ""
    for word in text.split(" "):
        probe = (cur + " " + word).strip()
        if len(probe) <= limit or not cur:
            cur = probe
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return "<br>".join(lines)


def n_lines(wrapped):
    return wrapped.count("<br>") + 1


def spread(rows, pitch_pt, gap_pt, n):
    """Đẩy nhãn ra cho khỏi chồng nhau, giữ nguyên thứ tự và nét dẫn về hàng thật.

    Trong bản xếp theo cụm, 7–8 nước ASEAN nằm sát nhau ở đầu khối lớn: cách
    nhau 2–3 hàng, tức 8–12pt, trong khi một dòng chữ 7pt cần ~9pt. Đặt nhãn
    đúng hàng thì chúng đè lên nhau. Nên nhãn được đẩy ra vừa đủ và nối về hàng
    thật bằng một nét mảnh — hàng không bị xê dịch, chỉ cái nhãn xê dịch.

    Trả về vị trí (tính bằng số hàng) của từng nhãn, cùng thứ tự với `rows`.
    """
    gap = gap_pt / float(pitch_pt)       # khoảng cách tối thiểu, quy ra số hàng
    out = list(rows)
    for i in range(1, len(out)):          # đẩy xuống
        out[i] = max(out[i], out[i - 1] + gap)
    over = out[-1] - (n - 1) if out else 0
    if over > 0:                          # tràn đáy thì kéo cả cụm lên
        out = [v - over for v in out]
        for i in range(len(out) - 2, -1, -1):
            out[i] = min(out[i], out[i + 1] - gap)
    return out


# ---------------------------------------------------------------------------
# Hình
# ---------------------------------------------------------------------------
def build_matrix(edges, order):
    """z (log10 giá trị, None nếu trống) + giá trị thô, theo đúng thứ tự `order`.

    plotly đọc `z[hàng][cột]` với hàng chạy theo trục y, nên `z[i][j]` là luồng
    từ nước ở vị trí i (trục y, nước XUẤT) sang nước ở vị trí j (trục x, nước
    NHẬP). Đặt ngược lại là ma trận bị chuyển vị — nhìn vẫn "đẹp" vì mạng gần
    đối xứng (đối ứng 0,84 ở A3), nên lỗi này không tự lộ ra.
    """
    pos = {iso: i for i, iso in enumerate(order)}
    n = len(order)
    z = [[None] * n for _ in range(n)]
    raw = [[0.0] * n for _ in range(n)]
    for s, t, v in edges:
        z[pos[s]][pos[t]] = math.log10(v)
        raw[pos[s]][pos[t]] = v
    return z, raw, pos


def colorbar_ticks(lo, hi):
    """Mốc thanh màu ở các giá trị tròn, ghi bằng TỶ USD.

    Đơn vị để trên đầu thanh chứ không lặp ở từng mốc: "10 tỷ USD" dài 31pt ở
    cỡ 7pt, bảy mốc như thế là 217pt — plotly sẽ tự xoay nghiêng cả hàng nhãn.
    """
    vals, texts = [], []
    for exp in range(int(math.floor(lo)), int(math.ceil(hi)) + 1):
        for mult in (1, 3):
            v = mult * (10 ** exp)
            if lo <= math.log10(v) <= hi:
                vals.append(math.log10(v))
                ty = v / 1e9
                nd = 0 if ty >= 1 else (1 if ty >= 0.1 else 2)
                texts.append(R.fmt_vn(ty, nd))
    return vals, texts


def cluster_heads(isos, comm, stren):
    """{thứ hạng cụm: ISO3 của nước mạnh nhất trong cụm}."""
    out = {}
    for iso in isos:
        c = comm[iso]
        if c not in out or stren.get(iso, 0.0) > stren.get(out[c], 0.0):
            out[c] = iso
    return out


def layout_margins(title, sub, note, source):
    """Lề trên / dưới tính từ SỐ DÒNG CHỮ THẬT, không đoán.

    Khung chỉ cao 453,6pt. Đoán thừa một dòng thì tiêu đề đè lên ma trận, đoán
    thiếu một dòng thì chữ bị cắt mép — lần render đầu của việc này dính cả hai.
    """
    t = (TEXT_PAD + n_lines(title) * R.FONT_SIZES["title"] * LINE_H
         + 2 + n_lines(sub) * R.FONT_SIZES["subtitle"] * LINE_H + 8)
    b = (CB_BLOCK + n_lines(note) * R.FONT_SIZES["annotation"] * LINE_H
         + 5 + n_lines(source) * R.FONT_SIZES["footnote"] * LINE_H + 6)
    return dict(t=t, l=MARGIN_L, r=MARGIN_R, b=b)


def plot_side_pt(margin):
    """Cạnh vùng vẽ, tính bằng point in thật. Đây là mẫu số của phép đo nhãn."""
    w = CANVAS_PT - margin["l"] - margin["r"]
    h = CANVAS_PT - margin["t"] - margin["b"]
    return min(w, h)          # trục y khóa tỉ lệ 1:1 với trục x nên lấy cạnh nhỏ


def resolve_layout(year, orders, sizes, names, heads, m):
    """Lề DÙNG CHUNG cho cả hai bản, và cạnh ma trận đi kèm.

    Hai bản phải có ô bằng nhau từng pt, nếu không thì cái "rậm hơn" có thể chỉ
    là cái được vẽ to hơn — mà toàn bộ lập luận của hình này là hai bản chỉ
    khác thứ tự. Nên lề lấy theo bản cần nhiều chỗ chữ nhất, và lấy cho cả hai,
    kể cả khi chỉ render một bản.

    Chữ và lề phụ thuộc lẫn nhau: số pt mỗi nhãn nằm trong câu ghi chú, mà câu
    ghi chú dài mấy dòng lại quyết định lề dưới. Ba vòng là thừa đủ để đứng im.
    """
    source = wrap_pt(SOURCE_TEXT, R.FONT_SIZES["footnote"], TEXT_W)
    axis_pt = CANVAS_PT - MARGIN_L - MARGIN_R
    margin = dict(t=0, l=MARGIN_L, r=MARGIN_R, b=0)
    for _ in range(3):
        boxes = []
        for kind in ("alpha", "cluster"):
            title, sub, note = compose_text(year, kind, orders[kind], sizes,
                                            names, heads, m, axis_pt)
            boxes.append(layout_margins(title, sub, note, source))
        margin = dict(t=max(b["t"] for b in boxes), l=MARGIN_L, r=MARGIN_R,
                      b=max(b["b"] for b in boxes))
        axis_pt = plot_side_pt(margin)
    return margin, axis_pt, source


def make_figure(year, order_kind, order, edges, comm, sizes, names, stren,
                measures, focus, margin, axis_pt, source):
    n = len(order)
    z, raw, pos = build_matrix(edges, order)
    flat = [v for row in z for v in row if v is not None]
    lo, hi = min(flat), max(flat)
    heads = cluster_heads(order, comm, stren)
    title, sub, note = compose_text(year, order_kind, order, sizes, names,
                                    heads, measures, axis_pt)
    plot_h = CANVAS_PT - margin["t"] - margin["b"]
    pitch = axis_pt / float(n)          # pt cho mỗi hàng

    hover = []
    for i, src in enumerate(order):
        line = []
        for j, dst in enumerate(order):
            if z[i][j] is None:
                line.append("")
            else:
                line.append("<b>%s → %s</b><br>%s<br>cụm %s → cụm %s"
                            % (names[src][0], names[dst][0],
                               R.fmt_usd(raw[i][j]),
                               R.fmt_vn(comm[src] + 1, 0),
                               R.fmt_vn(comm[dst] + 1, 0)))
        hover.append(line)

    tickvals, ticktext = colorbar_ticks(lo, hi)
    scale = [[i / (len(R.SEQUENTIAL_SCALE) - 1.0), c]
             for i, c in enumerate(R.SEQUENTIAL_SCALE)]

    fig = go.Figure(go.Heatmap(
        z=z, x=list(range(n)), y=list(range(n)), text=hover,
        hovertemplate="%{text}<extra></extra>", hoverongaps=False,
        colorscale=scale, zmin=lo, zmax=hi, xgap=0.4, ygap=0.4,
        colorbar=dict(
            orientation="h", x=0.0, xanchor="left", y=-(10.0 / plot_h),
            yanchor="top", len=0.66, thickness=5, outlinewidth=0,
            tickmode="array", tickvals=tickvals, ticktext=ticktext,
            tickangle=0, tickfont=dict(size=R.FONT_SIZES["footnote"]),
            title=dict(text="Giá trị một luồng xuất khẩu, tỷ USD (thang log)",
                       side="top",
                       font=dict(size=R.FONT_SIZES["footnote"])),
        ),
    ))

    # --- nhãn: chỉ tập con, B15 ------------------------------------------
    #
    # Vì sao đúng tập này: ASEAN là lát cắt của đề tài (B2), còn nước mạnh nhất
    # mỗi cụm là chỗ duy nhất đặt tên được cho một khối. Mọi nước khác vẫn có
    # đủ một hàng và một cột trong ma trận, chỉ là không có nhãn — không ô nào
    # bị bỏ đi, và bản .html rê chuột vẫn đọc ra tên.
    #
    # Nhãn chỉ ghi ở HÀNG, không ghi ở cột: hai trục dùng chung một thứ tự nên
    # nhãn cột chỉ lặp lại nhãn hàng, mà lặp lại thì mất 40pt chiều cao cho một
    # hàng chữ xoay đứng — đổi 40pt đó lấy ma trận to hơn thì đáng hơn.
    keep = set(iso for iso in order if names[iso][1])
    keep.add(focus)
    keep |= set(heads.values())
    vals = [i for i, iso in enumerate(order) if iso in keep]
    tick_pt = R.FONT_SIZES["tick"]
    placed = spread(vals, pitch, tick_pt * 1.25, n)

    fig.update_xaxes(tickmode="array", tickvals=vals, ticktext=[""] * len(vals),
                     side="top", showgrid=False, zeroline=False,
                     ticks="outside", ticklen=2, tickwidth=0.6,
                     tickcolor="#777777", range=[-0.5, n - 0.5],
                     constrain="domain")
    fig.update_yaxes(tickmode="array", tickvals=vals, ticktext=[""] * len(vals),
                     autorange="reversed", showgrid=False, zeroline=False,
                     ticks="outside", ticklen=2, tickwidth=0.6,
                     tickcolor="#777777", scaleanchor="x", scaleratio=1,
                     constrain="domain")

    for row, y_lab in zip(vals, placed):
        iso = order[row]
        nm = names[iso][0]
        fig.add_annotation(
            x=-0.5, y=row, xref="x", yref="y",
            text=("<b>%s</b>" % nm) if iso == focus else nm,
            showarrow=True, arrowhead=0, arrowwidth=0.4, arrowcolor=LEADER,
            ax=-LEADER_PT, ay=(y_lab - row) * pitch,
            xanchor="right", yanchor="middle", align="right",
            font=dict(size=tick_pt,
                      color="#000000" if iso == focus else "#333333"))

    shapes = [dict(type="line", xref="x", yref="y", layer="below",
                   x0=-0.5, y0=-0.5, x1=n - 0.5, y1=n - 0.5,
                   line=dict(color=DIAG_LINE, width=0.5))]
    # --- khung khối cụm, chỉ ở bản xếp theo cụm ---------------------------
    if order_kind == "cluster":
        start = 0
        for size in sizes:
            shapes.append(dict(type="rect", xref="x", yref="y",
                               x0=start - 0.5, x1=start + size - 0.5,
                               y0=start - 0.5, y1=start + size - 0.5,
                               line=dict(color=BLOCK_LINE, width=0.9)))
            start += size
    # --- hàng và cột Việt Nam: hình dạng, không phải màu (B12) ------------
    if focus in pos:
        k = pos[focus]
        shapes.append(dict(type="rect", xref="x", yref="y",
                           x0=-0.5, x1=n - 0.5, y0=k - 0.5, y1=k + 0.5,
                           line=dict(color=R.HIGHLIGHT_STROKE, width=0.8)))
        shapes.append(dict(type="rect", xref="x", yref="y",
                           x0=k - 0.5, x1=k + 0.5, y0=-0.5, y1=n - 0.5,
                           line=dict(color=R.HIGHLIGHT_STROKE, width=0.8)))
    fig.update_layout(shapes=shapes)

    # --- nhãn khối ở lề phải ---------------------------------------------
    if order_kind == "cluster":
        start = 0
        for rank, size in enumerate(sizes):
            head = names[heads[rank]][0]
            fig.add_annotation(
                x=n - 0.5, y=start + size / 2.0 - 0.5, xref="x", yref="y",
                text="%s<br>%s nước" % (head, R.fmt_vn(size, 0)),
                showarrow=False, xanchor="left", align="left", xshift=4,
                font=dict(size=R.FONT_SIZES["footnote"], color="#333333"))
            start += size

    fig.update_layout(
        font=dict(family=", ".join(R.FONT_STACK),
                  size=R.FONT_SIZES["annotation"]),
        separators=",.",
        margin=dict(**margin),
        paper_bgcolor="#FFFFFF", plot_bgcolor=EMPTY_CELL,
        hovermode="closest",
    )

    # Tiêu đề và phụ đề là ANNOTATION chứ không phải layout.title: title của
    # plotly tự đo lấy chỗ và với một khung chỉ cao 453,6pt nó cắt mất dòng đầu.
    # Đặt bằng tay thì biết chắc từng dòng rơi vào đâu.
    def text_block(txt, base, above_pt, size, color=None):
        """`base` = 1 cho mép TRÊN vùng vẽ, 0 cho mép DƯỚI; `above_pt` tính lên."""
        fig.add_annotation(
            text=txt, showarrow=False, xref="paper", yref="paper",
            x=0, y=base + (above_pt / plot_h), xshift=-(MARGIN_L - TEXT_PAD),
            xanchor="left", yanchor="top", align="left",
            font=dict(size=size, color=color))

    text_block(title, 1, margin["t"] - TEXT_PAD, R.FONT_SIZES["title"])
    text_block(sub, 1,
               margin["t"] - TEXT_PAD
               - n_lines(title) * R.FONT_SIZES["title"] * LINE_H - 2,
               R.FONT_SIZES["subtitle"], "#555555")

    note_top = CB_BLOCK
    text_block(note, 0, -note_top, R.FONT_SIZES["annotation"], "#444444")
    src_top = note_top + n_lines(note) * R.FONT_SIZES["annotation"] * LINE_H + 5
    text_block(source, 0, -src_top, R.FONT_SIZES["footnote"], "#777777")
    return fig


def compose_text(year, order_kind, order, sizes, names, heads, m, axis_pt):
    """Tiêu đề / phụ đề / ghi chú — dựng từ số đo, không viết cứng câu nào."""
    n = len(order)
    n_cells = m["n_cells"]
    drop = 100.0 * (1.0 - m["d_cluster"] / m["d_alpha"]) if m["d_alpha"] else 0.0

    if order_kind == "alpha":
        # So với mốc ngẫu nhiên: câu nói ra phải đúng cả khi năm khác cho số
        # khác, nên ba nhánh chứ không phải một câu viết sẵn.
        if m["d_alpha"] > m["d_random"] * 1.02:
            verdict = "xa đường chéo hơn cả một thứ tự ngẫu nhiên"
        elif m["d_alpha"] < m["d_random"] * 0.98:
            verdict = "gần đường chéo hơn ngẫu nhiên một chút"
        else:
            verdict = "đúng bằng mức của một thứ tự ngẫu nhiên"
        title = ("Xếp theo mã nước A→Z, %s luồng rải khắp ma trận — %s "
                 "(%s so với %s)"
                 % (R.fmt_vn(n_cells, 0), verdict,
                    R.fmt_vn(m["d_alpha"], 3), R.fmt_vn(m["d_random"], 3)))
    else:
        # Kèm CỠ từng khối ngay trong tiêu đề: năm 1995 khối thứ ba chỉ có 2
        # nước (Brazil, Argentina), nếu chỉ đọc tên thì nó được hiểu ngang
        # hàng với khối 34 nước — ghi cỡ ra là hết hiểu nhầm, mà vẫn là số đo.
        head_names = ", ".join(
            "%s (%s nước)" % (names[heads[r]][0], R.fmt_vn(sizes[r], 0))
            for r in sorted(heads))
        title = ("Vẫn %s ô ấy, xếp theo cụm thì %s khối hiện ra quanh %s — "
                 "%s giá trị nằm trong khối"
                 % (R.fmt_vn(n_cells, 0), R.fmt_vn(len(sizes), 0), head_names,
                    R.fmt_pct(100.0 * m["within_value"], 1)))

    sub = ("Mạng đã lọc %d · %s × %s nước, hàng và cột cùng một thứ tự · "
           "hàng = nước xuất, cột = nước nhập · ô xám = không có luồng vượt "
           "ngưỡng."
           % (year, R.fmt_vn(n, 0), R.fmt_vn(n, 0)))

    per_all = axis_pt / float(n)
    per_sub = axis_pt / float(m["n_labels"])
    note = ("Thước đo: khoảng cách trung bình tới đường chéo |i−j|/(n−1), có "
            "trọng số theo giá trị — theo mã nước %s · theo cụm %s (giảm %s) · "
            "ngẫu nhiên %s lần %s. Hai bản cùng %s ô và cùng %s: đổi thứ tự "
            "hàng/cột không đổi một ô nào. Chỉ %s nhãn (10 nước ASEAN + nước "
            "mạnh nhất mỗi cụm) vì %s nhãn trên cạnh %s pt còn %s pt mỗi nhãn, "
            "dưới sàn 7pt; %s nhãn được %s pt — B15."
            % (R.fmt_vn(m["d_alpha"], 3), R.fmt_vn(m["d_cluster"], 3),
               R.fmt_pct(drop, 1), R.fmt_vn(N_SHUFFLE, 0),
               R.fmt_vn(m["d_random"], 3),
               R.fmt_vn(n_cells, 0), R.fmt_usd(m["total_value"], 2),
               R.fmt_vn(m["n_labels"], 0), R.fmt_vn(n, 0),
               R.fmt_vn(axis_pt, 0), R.fmt_vn(per_all, 1),
               R.fmt_vn(m["n_labels"], 0), R.fmt_vn(per_sub, 1)))

    return (wrap_pt("<b>%s</b>" % title, R.FONT_SIZES["title"], TEXT_W,
                    ratio=0.545),
            wrap_pt(sub, R.FONT_SIZES["subtitle"], TEXT_W),
            wrap_pt(note, R.FONT_SIZES["annotation"], TEXT_W))


def save(fig, name):
    os.makedirs(OUTDIR, exist_ok=True)
    html = os.path.join(OUTDIR, name + ".html")
    fig.write_html(html, include_plotlyjs="cdn", config={"displayModeBar": False})
    print("  %s" % html)
    try:
        png = os.path.join(OUTDIR, name + ".png")
        # Layout tính bằng point; scale đẩy lên đúng FIG_DPI_PRINT.
        fig.write_image(png, width=int(round(CANVAS_PT)),
                        height=int(round(CANVAS_PT)),
                        scale=(R.FIG_WIDTH_FULL * R.FIG_DPI_PRINT)
                              / round(CANVAS_PT))
        print("  %s" % png)
    except Exception as exc:
        print("  (không xuất được PNG: %s — bản .html vẫn dùng được)" % exc)


# ---------------------------------------------------------------------------
# Khối kiểm chứng
# ---------------------------------------------------------------------------
def report(year, order, edges, comm, sizes, mod, names, m, from_metrics,
           agree, heads, stren, focus, axis_pt):
    n = len(order)
    print("\n" + "=" * 70)
    print("KIỂM CHỨNG — ma trận kề năm %d" % year)
    print("=" * 70)
    print("  Đồ thị đã lọc: %s nước, %s luồng có hướng, tổng %s"
          % (R.fmt_vn(n, 0), R.fmt_vn(m["n_cells"], 0),
             R.fmt_usd(m["total_value"], 2)))
    print("  Cùng một tập ô cho cả hai bản: %s ô, tổng giá trị lệch %s USD"
          % (R.fmt_vn(m["n_cells"], 0), R.fmt_vn(m["value_gap"], 0)))
    print("  Cụm Louvain (seed %d): %s cụm, cỡ %s, modularity %s"
          % (m["seed"], R.fmt_vn(len(sizes), 0),
             " / ".join(R.fmt_vn(s, 0) for s in sizes), R.fmt_vn(mod, 3)))
    if from_metrics:
        print("     đối chiếu cột `community` của metrics.csv: %s/%s nước khớp"
              % (R.fmt_vn(agree, 0), R.fmt_vn(n, 0)))
    else:
        print("     metrics.csv chưa có năm này — cụm tính tại chỗ bằng đúng "
              "công thức của src/compute_metrics.py")
    print("\n  THƯỚC ĐO 1 — khoảng cách trung bình tới đường chéo |i-j|/(n-1),")
    print("  có trọng số theo giá trị (0 = sát chéo, 1 = hai góc xa nhất):")
    print("     xếp theo mã nước A→Z   %s" % R.fmt_vn(m["d_alpha"], 4))
    print("     xếp theo cụm           %s   (giảm %s)"
          % (R.fmt_vn(m["d_cluster"], 4),
             R.fmt_pct(100.0 * (1 - m["d_cluster"] / m["d_alpha"]), 1)))
    print("     xếp ngẫu nhiên %s lần  %s   (trung vị; khoảng %s – %s)"
          % (R.fmt_vn(N_SHUFFLE, 0), R.fmt_vn(m["d_random"], 4),
             R.fmt_vn(m["d_rand_lo"], 4), R.fmt_vn(m["d_rand_hi"], 4)))
    print("     không trọng số:  mã nước %s · cụm %s"
          % (R.fmt_vn(m["u_alpha"], 4), R.fmt_vn(m["u_cluster"], 4)))
    print("\n  THƯỚC ĐO 2 — giá trị nằm TRONG khối (không phụ thuộc thứ tự):")
    print("     %s tổng giá trị, %s/%s ô"
          % (R.fmt_pct(100.0 * m["within_value"], 1),
             R.fmt_vn(m["within_cells"], 0), R.fmt_vn(m["n_cells"], 0)))
    print("     mật độ ô trong khối %s so với ngoài khối %s — gấp %s lần"
          % (R.fmt_pct(100.0 * m["dens_in"], 1),
             R.fmt_pct(100.0 * m["dens_off"], 1),
             R.fmt_vn(m["dens_ratio"], 2)))
    print("\n  NHÃN — cạnh vùng vẽ %s pt (khung %s pt = %s inch):"
          % (R.fmt_vn(axis_pt, 1), R.fmt_vn(CANVAS_PT, 1),
             R.fmt_vn(R.FIG_WIDTH_FULL, 2)))
    print("     %s nhãn -> %s pt mỗi nhãn  %s sàn %s pt"
          % (R.fmt_vn(n, 0), R.fmt_vn(axis_pt / n, 2),
             "ĐẠT" if axis_pt / n >= LABEL_FLOOR_PT else "DƯỚI",
             R.fmt_vn(LABEL_FLOOR_PT, 0)))
    print("     %s nhãn -> %s pt mỗi nhãn  %s sàn %s pt  (đang dùng, B15)"
          % (R.fmt_vn(m["n_labels"], 0), R.fmt_vn(axis_pt / m["n_labels"], 2),
             "ĐẠT" if axis_pt / m["n_labels"] >= LABEL_FLOOR_PT else "DƯỚI",
             R.fmt_vn(LABEL_FLOOR_PT, 0)))
    smallest = min(R.FONT_SIZES.values())
    print("     cỡ chữ nhỏ nhất trên hình %s pt  %s sàn %s pt"
          % (R.fmt_vn(smallest, 0),
             "ĐẠT" if smallest >= LABEL_FLOOR_PT else "DƯỚI",
             R.fmt_vn(LABEL_FLOOR_PT, 0)))
    print("\n  Các khối, theo cỡ giảm dần:")
    for rank, size in enumerate(sizes):
        members = [i for i in order if comm[i] == rank]
        top = sorted(members, key=lambda k: -stren.get(k, 0.0))[:3]
        asean = sorted(i for i in members if names[i][1])
        print("     khối %s · %s nước · mạnh nhất: %s"
              % (R.fmt_vn(rank + 1, 0), R.fmt_vn(size, 0),
                 ", ".join(names[t][0] for t in top)))
        if asean:
            print("        chứa %s nước ASEAN: %s"
                  % (R.fmt_vn(len(asean), 0), ", ".join(asean)))
    if focus in comm:
        out = sorted(((v, t) for s, t, v in edges if s == focus), reverse=True)
        inn = sorted(((v, s) for s, t, v in edges if t == focus), reverse=True)
        print("\n  %s: khối %s · %s ô hàng (xuất) · %s ô cột (nhập)"
              % (names[focus][0], R.fmt_vn(comm[focus] + 1, 0),
                 R.fmt_vn(len(out), 0), R.fmt_vn(len(inn), 0)))
        for v, k in out[:3]:
            print("     xuất sang %-18s %s" % (names[k][0], R.fmt_usd(v)))
        for v, k in inn[:3]:
            print("     nhập từ   %-18s %s" % (names[k][0], R.fmt_usd(v)))
    print("=" * 70)


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--order", choices=("alpha", "cluster", "both"),
                    default="both")
    ap.add_argument("--focus", default="VNM")
    ap.add_argument("--seed", type=int, default=42,
                    help="hạt giống Louvain, cố định để chạy lại ra đúng hình cũ")
    args = ap.parse_args()

    names = load_names()
    edges = load_edges(args.year)
    isos = sorted(set(x for s, t, _ in edges for x in (s, t)))
    missing = [i for i in isos if i not in names]
    if missing:
        sys.exit("nodes.csv thiếu %d mã nước: %s" % (len(missing), missing[:5]))

    print("Đọc đồ thị đã lọc năm %d: %s nước, %s luồng vượt ngưỡng"
          % (args.year, R.fmt_vn(len(isos), 0), R.fmt_vn(len(edges), 0)))

    comm, sizes, mod = louvain_communities(edges, args.seed)
    ref = metrics_communities(args.year)
    agree = sum(1 for i in isos if i in ref and ref[i] == comm[i])
    if ref and agree != len(isos):
        # metrics.csv là nguồn chính thức (T15 dùng nó); lệch thì tin nó, và nói ra.
        print("  LƯU Ý: cụm tính tại chỗ lệch metrics.csv ở %d/%d nước — "
              "lấy theo metrics.csv." % (len(isos) - agree, len(isos)))
        comm = dict((i, ref[i]) for i in isos)
        sizes = [sum(1 for i in isos if comm[i] == r)
                 for r in sorted(set(comm.values()))]
        sizes.sort(reverse=True)

    stren = strengths(edges)
    o_alpha = order_alpha(isos)
    o_clust = order_cluster(isos, comm, stren)
    n = len(isos)

    p_a = {iso: i for i, iso in enumerate(o_alpha)}
    p_c = {iso: i for i, iso in enumerate(o_clust)}
    d_a, u_a = diagonal_distance(edges, p_a, n)
    d_c, u_c = diagonal_distance(edges, p_c, n)
    d_r, r_lo, r_hi = shuffle_baseline(edges, isos, args.seed)
    wv, wc, nc = within_block(edges, comm)
    di, do, dr = block_density(edges, comm, sizes, n)

    heads = cluster_heads(isos, comm, stren)
    n_labels = len(set(i for i in isos if names[i][1]) | {args.focus}
                   | set(heads.values()))

    # Bằng chứng "đổi thứ tự không đổi dữ liệu": dựng hai ma trận rồi so tổng.
    z_a, raw_a, _ = build_matrix(edges, o_alpha)
    z_c, raw_c, _ = build_matrix(edges, o_clust)
    cells_a = sum(1 for row in z_a for v in row if v is not None)
    cells_c = sum(1 for row in z_c for v in row if v is not None)
    sum_a = sum(v for row in raw_a for v in row)
    sum_c = sum(v for row in raw_c for v in row)
    if cells_a != cells_c:
        sys.exit("Hai thứ tự ra số ô khác nhau (%d vs %d) — có lỗi lập trình."
                 % (cells_a, cells_c))

    m = dict(n_cells=cells_a, total_value=sum_a, value_gap=abs(sum_a - sum_c),
             d_alpha=d_a, d_cluster=d_c, d_random=d_r, d_rand_lo=r_lo,
             d_rand_hi=r_hi, u_alpha=u_a, u_cluster=u_c, within_value=wv,
             within_cells=wc, dens_in=di, dens_off=do, dens_ratio=dr,
             n_labels=n_labels, seed=args.seed)

    orders = dict(alpha=o_alpha, cluster=o_clust)
    margin, axis_pt, source = resolve_layout(args.year, orders, sizes, names,
                                             heads, m)

    kinds = ["alpha", "cluster"] if args.order == "both" else [args.order]
    print("Dựng biểu đồ:")
    for kind in kinds:
        fig = make_figure(args.year, kind, orders[kind], edges, comm, sizes,
                          names, stren, m, args.focus, margin, axis_pt, source)
        save(fig, "adjacency_%s_%d" % (kind, args.year))

    report(args.year, o_clust, edges, comm, sizes, mod, names, m,
           bool(ref), agree, heads, stren, args.focus, axis_pt)


if __name__ == "__main__":
    main()

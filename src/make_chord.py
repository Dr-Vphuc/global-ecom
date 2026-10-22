# -*- coding: utf-8 -*-
"""T17 — Chord: luồng thương mại giữa các khối và vùng, Việt Nam làm trọng tâm.

Ba quyết định đã chốt trong script này, mỗi cái đều có số đo đứng sau:

1. **Khối suy ra từ dữ liệu, không gán tay.** nodes.csv có sẵn region và
   continent. Trong đồ thị đã lọc, vùng South-East Asia TRÙNG KHÍT 10 nước
   ASEAN ở cả 1995 lẫn 2023, nên "khối" chỉ là: Việt Nam tách riêng (đề tài lấy
   nó làm trọng tâm), ASEAN còn lại, Đông Á tách khỏi phần Á còn lại (A10 cho
   thấy cực Đông Á mới là cực chứa Việt Nam), rồi bốn châu còn lại. Script tự
   kiểm mọi nước thuộc ĐÚNG MỘT khối và in bảng đối chiếu.

2. **Khối mã hoá bằng VỊ TRÍ, không bằng màu (B17).** Đã đo: sau 10 màu ngành
   (T04) và 3 màu cụm (T15), tìm tham lam maximin trên lưới 868 màu in được thì
   màu thứ ba của một bảng mới chỉ còn cách các màu đã chiếm ΔE2000 = 14,2 —
   dưới sàn 15 — mà hai màu đầu tìm được lại là #00FF00 và #FF00FF, tức thuật
   toán đã phải bới vào góc gamut. Không còn chỗ cho bảng màu thứ ba. Trên một
   vòng tròn thì khối đã có vị trí cố định và nhãn riêng, nên hue không cần
   thiết: cung và dải dùng độ sáng, Việt Nam nổi lên bằng viền đen theo B12.

3. **Gộp hai chiều thành một dải, theo B13.** Đối ứng 0,84 nên vẽ hai nửa song
   song chỉ tốn mực. Bề dày = tổng hai chiều của phần vượt ngưỡng. Chiều của
   luồng là việc của T19 (Sankey) — ghi rõ trên hình để không ai đọc nhầm.

Chạy:
    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_chord.py --year 2023
"""
import argparse
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_data as R                                    # noqa: E402

try:
    import plotly.graph_objects as go
except ImportError:
    sys.exit("Thiếu plotly. Chạy: pip install -r requirements.txt")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EDGES_CSV = os.path.join(ROOT, "data", "processed", "edges.csv")
NODES_CSV = os.path.join(ROOT, "data", "processed", "nodes.csv")
OUTDIR = os.path.join(ROOT, "output")

# Khung hình tính bằng POINT theo B16: 1 đơn vị layout = 1 point in thật.
PT_PER_INCH = 72.0
CANVAS_PT = R.FIG_WIDTH_FULL * PT_PER_INCH            # 453,6
LABEL_FLOOR_PT = 7.0

# Thứ tự quanh vòng tròn: Việt Nam ở đỉnh, rồi theo chiều kim đồng hồ từ Đông
# sang Tây. Thứ tự địa lý giữ dải ngắn ở chỗ thương mại dày nhất.
BLOC_ORDER = ["VNM", "ASEAN", "EAS", "ASIA", "OCE", "AFR", "EUR", "AME"]
BLOC_VI = {
    "VNM": "Việt Nam",
    "ASEAN": "ASEAN còn lại",
    "EAS": "Đông Á",
    "ASIA": "Châu Á còn lại",
    "OCE": "Châu Đại Dương",
    "AFR": "Châu Phi",
    "EUR": "Châu Âu",
    "AME": "Châu Mỹ",
}
FOCUS = "VNM"

# Không mở bảng màu mới (B17) — chỉ độ sáng, cộng viền đen cho Việt Nam (B12).
ARC_FILL = "#5A5A5A"
ARC_FOCUS = "#111111"
RIB_FILL = "#A9A9A9"
RIB_FOCUS = "#2E2E2E"
ARC_EDGE = "#FFFFFF"
TEXT_DIM = "#333333"

GAP_DEG = 2.6              # khe giữa hai cung
BAND_PT = 7.0              # bề dày vành cung
LABEL_PAD = 4.0            # khe từ mép vành ra chữ
MARGIN_X = 10.0
TEXT_PAD = 6.0
LINE_H = 1.33
TEXT_W = CANVAS_PT - 2 * TEXT_PAD

SOURCE_TEXT = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab). "
               "Đồ thị đã lọc theo quy tắc T10 (B4).")


# ---------------------------------------------------------------------------
# Dữ liệu
# ---------------------------------------------------------------------------
def bloc_of(iso3, region, continent):
    """Khối của một nước — suy ra, không tra bảng gán tay."""
    if iso3 == FOCUS:
        return "VNM"
    if iso3 in R.ASEAN_ISO3:
        return "ASEAN"
    if continent == "Asia":
        return "EAS" if region == "East Asia" else "ASIA"
    return {"Europe": "EUR", "Americas": "AME",
            "Africa": "AFR", "Oceania": "OCE"}.get(continent)


def load_nodes():
    """{ISO3: (tên tiếng Việt, khối)}."""
    if not os.path.exists(NODES_CSV):
        sys.exit("Chưa có %s.\nChạy trước: python src/build_intermediate.py"
                 % NODES_CSV)
    out = {}
    with open(NODES_CSV, "r", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[row["country_iso3"]] = (
                row["country_name_vi"] or row["country_name"],
                bloc_of(row["country_iso3"], row["region"], row["continent"]))
    return out


def load_flows(year):
    """[(nước xuất, nước nhập, USD)] — các luồng vượt ngưỡng của năm."""
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
    return out


def fold(flows, nodes):
    """Gộp hai chiều (B13) về cặp khối không thứ tự.

    pair[(a, b)] với a, b đã sắp theo BLOC_ORDER, tính cả cặp tự thân a == b.
    """
    rank = {b: i for i, b in enumerate(BLOC_ORDER)}
    pair, members, unassigned = {}, {}, set()
    for s, t, v in flows:
        ok = True
        for iso in (s, t):
            bl = nodes.get(iso, (None, None))[1]
            if bl is None:
                unassigned.add(iso)
                ok = False
            else:
                members.setdefault(bl, set()).add(iso)
        if not ok:
            continue
        a, b = nodes[s][1], nodes[t][1]
        key = (a, b) if rank[a] <= rank[b] else (b, a)
        pair[key] = pair.get(key, 0.0) + v
    return pair, members, unassigned


def arc_values(pair):
    """Giá trị chạm vào mỗi khối — cặp tự thân chỉ tính một lần."""
    arc = dict((b, 0.0) for b in BLOC_ORDER)
    for (a, b), v in pair.items():
        if a == b:
            arc[a] += v
        else:
            arc[a] += v
            arc[b] += v
    return arc


# ---------------------------------------------------------------------------
# Hình học
# ---------------------------------------------------------------------------
def pol(r, deg):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a))


def arc_pts(r, d0, d1, step=1.5):
    n = max(2, int(abs(d1 - d0) / step) + 1)
    return [pol(r, d0 + (d1 - d0) * i / float(n - 1)) for i in range(n)]


def band_path(r_in, r_out, d0, d1):
    pts = arc_pts(r_out, d0, d1) + arc_pts(r_in, d1, d0)
    s = "M %.2f,%.2f " % pts[0]
    s += " ".join("L %.2f,%.2f" % p for p in pts[1:])
    return s + " Z"


def ctrl_radius(r, deg_a, deg_b):
    """Bán kính điểm điều khiển của dải, theo khoảng cách góc hai đầu.

    Hai đầu đối diện nhau (180°) thì điểm điều khiển về đúng tâm và dải cắt
    ngang vòng tròn. Hai đầu sát nhau — ĐIỂN HÌNH LÀ DẢI NỘI KHỐI — thì điểm
    điều khiển nằm gần vành, nên dải chỉ là một thuỳ ôm lấy cung của chính nó.
    Để nguyên tâm cho mọi dải thì dải nội khối của Đông Á, Châu Âu, Châu Mỹ
    phình thành ba mảng chiếm hết lòng hình và che mất mọi dải khác.
    """
    d = abs(deg_a - deg_b) % 360.0
    if d > 180.0:
        d = 360.0 - d
    k = math.cos(math.radians(d / 2.0))
    return r * max(0.0, min(0.95, k))


def ribbon_path(r, a0, a1, b0, b1):
    """Chạy dọc cung nguồn, cong sang cung đích, rồi vòng về."""
    pa = arc_pts(r, a0, a1)
    pb = arc_pts(r, b0, b1)
    c1 = pol(ctrl_radius(r, a1, b0), a1)
    c2 = pol(ctrl_radius(r, a1, b0), b0)
    c3 = pol(ctrl_radius(r, b1, a0), b1)
    c4 = pol(ctrl_radius(r, b1, a0), a0)
    s = "M %.2f,%.2f " % pa[0]
    s += " ".join("L %.2f,%.2f" % p for p in pa[1:])
    s += " C %.2f,%.2f %.2f,%.2f %.2f,%.2f " % (c1 + c2 + pb[0])
    s += " ".join("L %.2f,%.2f" % p for p in pb[1:])
    s += " C %.2f,%.2f %.2f,%.2f %.2f,%.2f Z" % (c3 + c4 + pa[0])
    return s


def layout_angles(arc, total_arc):
    """Góc mỗi cung ∝ giá trị chạm vào khối. Việt Nam đặt giữa đỉnh."""
    span = 360.0 - GAP_DEG * len(BLOC_ORDER)
    angles = {}
    cur = 90.0 + arc[FOCUS] / total_arc * span / 2.0
    for bl in BLOC_ORDER:
        w = arc[bl] / total_arc * span
        angles[bl] = (cur - w, cur)
        cur -= w + GAP_DEG
    return angles


def allocate(pair, arc, angles):
    """Chia mỗi cung thành cung con, một cung con cho mỗi bạn hàng.

    Cặp tự thân chiếm HAI cung con liền nhau (mỗi nửa giá trị) để khép thành
    một vòng nằm gọn trong chính khối đó.
    """
    rank = {b: i for i, b in enumerate(BLOC_ORDER)}
    sub = {}
    for bl in BLOC_ORDER:
        if arc[bl] <= 0:
            continue
        d0, d1 = angles[bl]
        cur, parts = d1, []
        for other in BLOC_ORDER:
            key = (bl, other) if rank[bl] <= rank[other] else (other, bl)
            v = pair.get(key, 0.0)
            if v <= 0:
                continue
            if other == bl:
                parts.append((key, v / 2.0, 0))
                parts.append((key, v / 2.0, 1))
            else:
                parts.append((key, v, 0))
        for key, v, half in parts:
            w = v / arc[bl] * (d1 - d0)
            sub[(bl, key, half)] = (cur - w, cur)
            cur -= w
    return sub


# ---------------------------------------------------------------------------
# Câu chữ dựng từ dữ liệu
# ---------------------------------------------------------------------------
def vn_profile(pair):
    """Việt Nam nối với khối nào, bao nhiêu."""
    by = {}
    for (a, b), v in pair.items():
        if a == FOCUS and b != FOCUS:
            by[b] = by.get(b, 0.0) + v
        elif b == FOCUS and a != FOCUS:
            by[a] = by.get(a, 0.0) + v
    return {"by_bloc": by, "total": sum(by.values())}


def headline(year, pair, total, vn):
    partners = sorted(((v, b) for b, v in vn["by_bloc"].items()), reverse=True)
    top = partners[:2]
    share = sum(v for v, _ in top) / vn["total"] * 100.0 if vn["total"] else 0.0
    title = ("<b>%s nối với %s trong %s khối còn lại, nhưng %s và %s chiếm %s "
             "giá trị thương mại của %s</b>"
             % (BLOC_VI[FOCUS], R.fmt_vn(len(partners), 0),
                R.fmt_vn(len(BLOC_ORDER) - 1, 0),
                BLOC_VI[top[0][1]], BLOC_VI[top[1][1]],
                R.fmt_pct(share, 1), BLOC_VI[FOCUS]))
    inside = sum(v for (a, b), v in pair.items() if a == b)
    sub = ("Mạng đã lọc %d · %s khối, mỗi nước thuộc đúng một khối · bề dày dải "
           "= tổng hai chiều của phần vượt ngưỡng, không có chiều (B13) · %s "
           "giá trị nằm trong nội bộ một khối."
           % (year, R.fmt_vn(len(BLOC_ORDER), 0),
              R.fmt_pct(inside / total * 100.0, 1)))
    note = ("Cung dài theo giá trị chạm vào khối đó; dải nối hai khối, dải khép "
            "trong một khối là thương mại nội khối. Khối phân biệt bằng VỊ TRÍ "
            "chứ không bằng màu: sau 10 màu ngành và 3 màu cụm, màu thứ ba của "
            "một bảng mới chỉ còn cách ΔE 14,2 — dưới sàn 15 (B17). Chiều của "
            "luồng là việc của T19.")
    return title, sub, note


# ---------------------------------------------------------------------------
# Hình
# ---------------------------------------------------------------------------
def build(year, pair, members, nodes):
    arc = arc_values(pair)
    total = sum(pair.values())
    total_arc = sum(arc.values())
    vn = vn_profile(pair)
    title, sub, note = headline(year, pair, total, vn)

    title = R.wrap_pt(title, R.FONT_SIZES["title"], TEXT_W, ratio=0.545)
    sub = R.wrap_pt(sub, R.FONT_SIZES["subtitle"], TEXT_W)
    note = R.wrap_pt(note, R.FONT_SIZES["annotation"], TEXT_W)

    m_t = (TEXT_PAD + R.n_lines(title) * R.FONT_SIZES["title"] * LINE_H
           + R.n_lines(sub) * R.FONT_SIZES["subtitle"] * LINE_H + 8.0)
    m_b = (TEXT_PAD + R.n_lines(note) * R.FONT_SIZES["annotation"] * LINE_H
           + R.FONT_SIZES["footnote"] * LINE_H + 10.0)
    plot_w = CANVAS_PT - 2 * MARGIN_X
    plot_h = CANVAS_PT - m_t - m_b
    block_h = 2 * LABEL_FLOOR_PT * LINE_H
    # Chừa chỗ cho hai nấc đẩy nhãn, mỗi nấc một dòng chữ.
    label_room = block_h + LABEL_PAD + 2 * (LABEL_FLOOR_PT * LINE_H + 2.0)
    r_out = min(plot_w, plot_h) / 2.0 - label_room
    r_in = r_out - BAND_PT

    angles = layout_angles(arc, total_arc)
    sub_arcs = allocate(pair, arc, angles)

    shapes, hov_x, hov_y, hov_t = [], [], [], []

    # Dải: vẽ dải lớn trước để dải nhỏ không bị che; Việt Nam vẽ sau cùng.
    rank = {b: i for i, b in enumerate(BLOC_ORDER)}
    order = sorted(pair.items(), key=lambda kv: (FOCUS in kv[0], kv[1]))
    for (a, b), v in order:
        if (a, (a, b), 0) not in sub_arcs:
            continue
        if a == b:
            a0, a1 = sub_arcs[(a, (a, b), 0)]
            b0, b1 = sub_arcs[(a, (a, b), 1)]
        else:
            a0, a1 = sub_arcs[(a, (a, b), 0)]
            b0, b1 = sub_arcs[(b, (a, b), 0)]
        focus = FOCUS in (a, b)
        shapes.append(dict(
            type="path", path=ribbon_path(r_in, a0, a1, b0, b1),
            fillcolor=RIB_FOCUS if focus else RIB_FILL,
            opacity=0.80 if focus else 0.42,
            line=dict(color=R.HIGHLIGHT_STROKE if focus else "rgba(0,0,0,0)",
                      width=0.6 if focus else 0),
            layer="below" if not focus else "above"))
        mx, my = pol(r_in * 0.42, (a0 + a1) / 2.0)
        nx, ny = pol(r_in * 0.42, (b0 + b1) / 2.0)
        hov_x.append((mx + nx) / 2.0)
        hov_y.append((my + ny) / 2.0)
        same = " (nội khối)" if a == b else ""
        hov_t.append("%s ↔ %s%s<br>%s · %s tổng"
                     % (BLOC_VI[a], BLOC_VI[b], same, R.fmt_usd(v, 1),
                        R.fmt_pct(v / total * 100.0, 1)))

    # Cung + nhãn
    ann, placed = [], []
    for bl in BLOC_ORDER:
        d0, d1 = angles[bl]
        focus = bl == FOCUS
        shapes.append(dict(
            type="path", path=band_path(r_in, r_out, d0, d1),
            fillcolor=ARC_FOCUS if focus else ARC_FILL,
            line=dict(color=R.HIGHLIGHT_STROKE if focus else ARC_EDGE,
                      width=1.5 if focus else 0.6),
            layer="above"))
        mid = (d0 + d1) / 2.0
        name = BLOC_VI[bl]
        line1 = name
        line2 = "%s nước · %s" % (R.fmt_vn(len(members.get(bl, ())), 0),
                                  R.fmt_pct(arc[bl] / total_arc * 100.0, 1))
        cosm = math.cos(math.radians(mid))
        sinm = math.sin(math.radians(mid))
        xa = "left" if cosm > 0.15 else ("right" if cosm < -0.15 else "center")
        ya = "bottom" if sinm > 0 else "top"

        # Nhãn nào đè nhãn đã đặt thì đẩy ra xa tâm một nấc và nối lại bằng nét
        # dẫn. Hai cung mỏng cạnh nhau ở đáy (Châu Phi 0,8% và Châu Đại Dương
        # 1,9%) chắc chắn đè nhau nếu để nguyên bán kính. Nhãn đã bị đẩy thì
        # rút còn MỘT dòng, nên mỗi nấc chỉ tốn nửa chỗ và hai nấc vẫn nằm
        # trong phần lề đã chừa — đẩy mà vẫn hai dòng thì nhãn tụt xuống đè
        # khối chú thích dưới chân hình.
        step = LABEL_FLOOR_PT * LINE_H + 2.0
        for bump in (0, 1, 2):
            one = bump > 0
            txt = ("%s · %s" % (line1, line2)) if one else None
            w = ((len(txt) if one else max(len(line1), len(line2)))
                 * LABEL_FLOOR_PT * 0.52)
            h = (1 if one else 2) * LABEL_FLOOR_PT * LINE_H
            lx, ly = pol(r_out + LABEL_PAD + bump * step, mid)
            x0 = lx if xa == "left" else (lx - w if xa == "right" else lx - w / 2)
            y0 = ly if ya == "bottom" else ly - h
            box = (x0, y0, x0 + w, y0 + h)
            if not any(box[0] < p[2] and p[0] < box[2]
                       and box[1] < p[3] and p[1] < box[3] for p in placed):
                break
        placed.append(box)
        body = txt if bump else ("%s<br>%s" % (line1, line2))
        if bump:
            ax, ay = pol(r_out + 1.0, mid)
            bx, by = pol(r_out + LABEL_PAD + bump * step - 1.0, mid)
            shapes.append(dict(type="line", x0=ax, y0=ay, x1=bx, y1=by,
                               line=dict(color="#9A9A9A", width=0.5),
                               layer="below"))
        if focus:
            body = body.replace(line1, "<b>%s</b>" % line1, 1)
        ann.append(dict(
            x=lx, y=ly, xref="x", yref="y", showarrow=False,
            xanchor=xa, yanchor=ya, align=xa if xa != "center" else "center",
            text=body,
            font=dict(size=LABEL_FLOOR_PT,
                      color="#000000" if focus else TEXT_DIM)))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hov_x, y=hov_y, mode="markers", hoverinfo="text", hovertext=hov_t,
        marker=dict(size=9, color="rgba(0,0,0,0)"), showlegend=False))
    fig.update_layout(
        shapes=shapes, annotations=ann,
        font=dict(family=", ".join(R.FONT_STACK),
                  size=R.FONT_SIZES["annotation"]),
        separators=",.",
        margin=dict(l=MARGIN_X, r=MARGIN_X, t=m_t, b=m_b),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        hovermode="closest", showlegend=False)
    fig.update_xaxes(visible=False, range=[-plot_w / 2.0, plot_w / 2.0],
                     constrain="domain")
    fig.update_yaxes(visible=False, range=[-plot_h / 2.0, plot_h / 2.0],
                     scaleanchor="x", scaleratio=1, constrain="domain")

    # Tiêu đề đặt tay như T16: layout.title tự đo chỗ và cắt mất dòng đầu.
    def block(txt, y_from_top, size, color=None):
        fig.add_annotation(
            text=txt, showarrow=False, xref="paper", yref="paper",
            x=0, y=1 + (m_t - y_from_top) / plot_h,
            xshift=-(MARGIN_X - TEXT_PAD),
            xanchor="left", yanchor="top", align="left",
            font=dict(size=size, color=color))

    block(title, TEXT_PAD, R.FONT_SIZES["title"])
    block(sub, TEXT_PAD + R.n_lines(title) * R.FONT_SIZES["title"] * LINE_H,
          R.FONT_SIZES["subtitle"], TEXT_DIM)

    def bottom(txt, y_from_plot, size, color):
        fig.add_annotation(
            text=txt, showarrow=False, xref="paper", yref="paper",
            x=0, y=-(y_from_plot / plot_h), xshift=-(MARGIN_X - TEXT_PAD),
            xanchor="left", yanchor="top", align="left",
            font=dict(size=size, color=color))

    bottom(note, 10.0, R.FONT_SIZES["annotation"], TEXT_DIM)
    bottom(SOURCE_TEXT,
           10.0 + R.n_lines(note) * R.FONT_SIZES["annotation"] * LINE_H,
           R.FONT_SIZES["footnote"], "#777777")
    return fig, arc, total, total_arc, vn


def save(fig, name):
    os.makedirs(OUTDIR, exist_ok=True)
    html = os.path.join(OUTDIR, name + ".html")
    fig.write_html(html, include_plotlyjs="cdn", config={"displayModeBar": False})
    print("  %s" % html)
    try:
        png = os.path.join(OUTDIR, name + ".png")
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
def report(year, flows, pair, members, unassigned, arc, total, total_arc, vn,
           nodes):
    print("\n" + "=" * 70)
    print("KIỂM CHỨNG — chord khối và vùng, năm %d" % year)
    print("=" * 70)
    n_country = len(set([s for s, _, _ in flows] + [t for _, t, _ in flows]))
    print("  Đồ thị đã lọc: %s nước, %s luồng có hướng, tổng %s"
          % (R.fmt_vn(n_country, 0), R.fmt_vn(len(flows), 0),
             R.fmt_usd(total, 2)))
    print("  Gộp hai chiều (B13): %s luồng → %s cặp khối"
          % (R.fmt_vn(len(flows), 0), R.fmt_vn(len(pair), 0)))

    print("\n  Mỗi nước thuộc đúng một khối?")
    assigned = sum(len(v) for v in members.values())
    overlap = []
    for i, a in enumerate(BLOC_ORDER):
        for b in BLOC_ORDER[i + 1:]:
            both = members.get(a, set()) & members.get(b, set())
            if both:
                overlap.append((a, b, sorted(both)))
    print("    %s nước trong đồ thị, %s nước đã gán, %s nước chưa gán, "
          "%s khối chồng nhau"
          % (R.fmt_vn(n_country, 0), R.fmt_vn(assigned, 0),
             R.fmt_vn(len(unassigned), 0), R.fmt_vn(len(overlap), 0)))
    if unassigned:
        print("    CHƯA GÁN: %s" % ", ".join(sorted(unassigned)))
    for a, b, both in overlap:
        print("    CHỒNG: %s ∩ %s = %s" % (a, b, ", ".join(both)))

    print("\n  %-18s %6s  %14s  %7s  %7s"
          % ("Khối", "nước", "giá trị", "% cung", "% tổng"))
    for bl in BLOC_ORDER:
        print("  %-18s %6s  %14s  %7s  %7s"
              % (BLOC_VI[bl], R.fmt_vn(len(members.get(bl, ())), 0),
                 R.fmt_usd(arc[bl], 1),
                 R.fmt_pct(arc[bl] / total_arc * 100.0, 1),
                 R.fmt_pct(arc[bl] / (2 * total) * 100.0, 1)))

    inside = sum(v for (a, b), v in pair.items() if a == b)
    print("\n  Nội khối %s / %s = %s giá trị"
          % (R.fmt_usd(inside, 1), R.fmt_usd(total, 1),
             R.fmt_pct(inside / total * 100.0, 1)))
    print("  Tổng mọi dải %s — khớp tổng luồng vượt ngưỡng %s, lệch %s USD"
          % (R.fmt_usd(sum(pair.values()), 2), R.fmt_usd(total, 2),
             R.fmt_vn(sum(pair.values()) - total, 0)))

    print("\n  %s nối với %s khối:" % (BLOC_VI[FOCUS], len(vn["by_bloc"])))
    for v, b in sorted(((v, b) for b, v in vn["by_bloc"].items()), reverse=True):
        print("    %-18s %12s   %7s của Việt Nam"
              % (BLOC_VI[b], R.fmt_usd(v, 1),
                 R.fmt_pct(v / vn["total"] * 100.0, 1)))
    out_v = sum(v for s, t, v in flows if s == FOCUS)
    in_v = sum(v for s, t, v in flows if t == FOCUS)
    print("    Chiều (không vẽ ở đây, để dành T19): xuất %s · nhập %s"
          % (R.fmt_usd(out_v, 1), R.fmt_usd(in_v, 1)))
    big = sorted(((v, s, t) for s, t, v in flows
                  if FOCUS in (s, t)), reverse=True)[:3]
    for v, s, t in big:
        print("      %s → %s  %s" % (nodes[s][0], nodes[t][0], R.fmt_usd(v, 1)))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    args = ap.parse_args()

    nodes = load_nodes()
    flows = load_flows(args.year)
    if not flows:
        sys.exit("Không có luồng vượt ngưỡng nào năm %d." % args.year)
    pair, members, unassigned = fold(flows, nodes)

    fig, arc, total, total_arc, vn = build(args.year, pair, members, nodes)
    print("Đã vẽ:")
    save(fig, "chord_bloc_%d" % args.year)
    report(args.year, flows, pair, members, unassigned, arc, total, total_arc,
           vn, nodes)
    return 0


if __name__ == "__main__":
    sys.exit(main())

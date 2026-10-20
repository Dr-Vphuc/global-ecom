# -*- coding: utf-8 -*-
"""Chỉ số mạng lưới theo từng nước (T18).

Đọc data/processed/edges.csv, nodes.csv, country_year.csv rồi sinh hai file:

    data/processed/metrics.csv        bậc, độ mạnh, betweenness, cộng đồng
    data/processed/metrics_top20.csv  bảng xếp hạng top 20 để đưa vào báo cáo

Chạy:
    python src/compute_metrics.py
    python src/compute_metrics.py --year 2015 --seed 7

Cần networkx (có trong requirements.txt). Khác với analyze_network.py vốn chỉ
dùng thư viện chuẩn: betweenness và Louvain không phải thứ nên tự viết lại.

VÌ SAO TÍNH TRÊN HAI ĐỒ THỊ
---------------------------
Mạng đầy đủ năm 2023 có mật độ 0,518 — quá nửa số cặp nước trên đời có thương
mại trực tiếp với nhau. Trên một đồ thị dày như vậy, hầu như mọi cặp đã nối
thẳng nên gần như không đường đi ngắn nhất nào phải vòng qua nước thứ ba, và
betweenness sụp về 0 cho gần hết các nước: nó không còn đo được gì. Bậc cũng
bão hòa theo cùng lý do.

Nên mỗi nước có hai dòng, phân biệt bằng cột `graph`:

  `full`      — toàn bộ cạnh. Đây là chỗ lấy ĐỘ MẠNH (tiền). Xuất khẩu của một
                nước là một đại lượng kinh tế có thật, không được phép phụ
                thuộc vào ngưỡng lọc ta tự chọn.
  `filtered`  — cạnh có above_threshold = TRUE, tức quy tắc đã chốt ở T10
                (0,046% tổng thế giới + bảo hiểm top-3 vào/ra cho ASEAN).
                Đây là đồ thị mà T15, T16, T17 sẽ VẼ, nên betweenness và cộng
                đồng phải tính trên chính nó thì số trong bảng mới khớp hình.

Hệ quả cần nhớ khi dùng file: `strength_out` ở dòng `filtered` là một con số
bị cắt cụt, KHÔNG phải kim ngạch xuất khẩu của nước đó. Muốn tiền thì lấy
dòng `full`.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_data as R  # noqa: E402

try:
    import networkx as nx
    from networkx.algorithms import community as nx_comm
except ImportError:
    sys.exit("Thiếu networkx. Chạy: pip install -r requirements.txt")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "processed")
EDGES = os.path.join(OUT, "edges.csv")
NODES = os.path.join(OUT, "nodes.csv")
CYEAR = os.path.join(OUT, "country_year.csv")

# Số hạt giống thử lại để xem phân hoạch Louvain có ổn định không. Louvain là
# thuật toán tham lam có yếu tố ngẫu nhiên: cùng một đồ thị, hạt giống khác
# nhau có thể ra phân hoạch khác nhau. Không đo độ ổn định mà cứ công bố một
# phân hoạch là giấu mất phần bất định.
N_SEEDS_CHECK = 20

TOP_N = 20


def log(msg):
    print(msg, flush=True)


def need(path):
    if not os.path.exists(path):
        sys.exit("THIẾU FILE: %s\n  -> chạy: python src/build_intermediate.py"
                 % os.path.relpath(path, ROOT))
    return path


# ---------------------------------------------------------------------------
# Đọc dữ liệu
# ---------------------------------------------------------------------------
def load_nodes():
    """Thông tin nước, khóa theo ISO3."""
    out = {}
    with open(need(NODES), encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            out[r["country_iso3"]] = r
    return out


def load_eci(year):
    """ECI và hạng ECI của năm đó. Thiếu thì để trống, không bịa."""
    out = {}
    with open(need(CYEAR), encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if int(r["year"]) != year:
                continue
            out[r["country_iso3"]] = (r.get("eci", ""), r.get("eci_rank", ""))
    return out


def load_edges(year):
    """Cạnh của một năm. Trả về (tất cả, phần qua ngưỡng).

    Trọng số là export_value: nước nguồn tự khai xuất sang nước đích. Cột
    import_value trong cùng dòng là con số đối chiếu của chính nước nguồn, và
    nó là bản soi gương của export_value trên cạnh ngược lại — dùng lẫn hai
    cột vào một đồ thị là đếm trùng. Cả pipeline thống nhất dùng export_value.
    """
    full, filt = [], []
    with open(need(EDGES), encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if int(r["year"]) != year:
                continue
            e = (r["source_iso3"], r["target_iso3"], float(r["export_value"]))
            full.append(e)
            if r["above_threshold"] == "TRUE":
                filt.append(e)
    if not full:
        sys.exit("Không có cạnh nào cho năm %d trong edges.csv" % year)
    return full, filt


def build(edges):
    g = nx.DiGraph()
    for s, t, v in edges:
        # Atlas không lặp cặp, nhưng cộng dồn cho chắc: nếu nguồn dữ liệu sau
        # này có tách dòng thì đồ thị vẫn đúng thay vì âm thầm mất tiền.
        if g.has_edge(s, t):
            g[s][t]["weight"] += v
        else:
            g.add_edge(s, t, weight=v)
    return g


# ---------------------------------------------------------------------------
# Chỉ số
# ---------------------------------------------------------------------------
def betweenness(g):
    """Betweenness có trọng số, cùng với bản không trọng số để đối chiếu.

    networkx hiểu `weight` là KHOẢNG CÁCH, mà giá trị thương mại thì ngược lại
    — buôn càng nhiều càng gần. Nên phải nghịch đảo. Lấy chuẩn hóa theo luồng
    lớn nhất để khoảng cách nhỏ nhất bằng 1, số dễ đọc và không đổi thứ hạng
    (nhân cả thang với một hằng số thì đường đi ngắn nhất vẫn thế).

    Giữ luôn bản không trọng số vì cách nghịch đảo nào cũng là một lựa chọn
    tùy ý; để cạnh nhau thì người đọc tự thấy kết luận có phụ thuộc vào lựa
    chọn đó hay không.
    """
    if g.number_of_edges() == 0:
        return {}, {}
    wmax = max(d["weight"] for _, _, d in g.edges(data=True))
    for _, _, d in g.edges(data=True):
        d["dist"] = wmax / d["weight"]
    return (nx.betweenness_centrality(g, weight="dist", normalized=True),
            nx.betweenness_centrality(g, weight=None, normalized=True))


def undirected_projection(g):
    """Gộp hai chiều thành một cạnh để dò cộng đồng.

    Cộng đồng thương mại là chuyện AI BUÔN VỚI AI, không phải chiều của dòng
    hàng: nếu Việt Nam xuất nhiều sang Mỹ thì hai nước thuộc về nhau bất kể
    đọc cạnh theo chiều nào. Gộp lại cũng tránh việc một cặp buôn hai chiều bị
    tính thành hai liên kết yếu thay vì một liên kết mạnh.
    """
    u = nx.Graph()
    for s, t, d in g.edges(data=True):
        if u.has_edge(s, t):
            u[s][t]["weight"] += d["weight"]
        else:
            u.add_edge(s, t, weight=d["weight"])
    u.add_nodes_from(g.nodes())
    return u


def louvain(u, seed):
    # Đánh số cụm theo kích thước giảm dần, nên cụm 0 luôn là cụm đông nhất.
    # Louvain tự nó trả về thứ tự bất kỳ; nếu không sắp lại thì cùng một phân
    # hoạch có thể đổi số giữa hai lần chạy, và màu trên hình T15, thứ tự hàng
    # ở T16 sẽ nhảy loạn dù cấu trúc không đổi.
    parts = nx_comm.louvain_communities(u, weight="weight", seed=seed)
    parts = sorted(parts, key=len, reverse=True)
    comm = {}
    for i, group in enumerate(parts):
        for c in group:
            comm[c] = i
    return comm, parts


def partition_stability(u, base_comm, seeds):
    """Hai nước cùng cụm ở hạt giống này thì có còn cùng cụm ở hạt giống khác?

    Trả về (tỉ lệ cặp giữ nguyên quan hệ, khoảng số cụm, khoảng modularity).
    Đo trên cặp chứ không đo trên nhãn cụm, vì nhãn chỉ là số thứ tự — hai
    phân hoạch y hệt nhau vẫn có thể đánh số khác nhau.
    """
    nodes = sorted(base_comm)
    base_same = {(a, b): (base_comm[a] == base_comm[b])
                 for i, a in enumerate(nodes) for b in nodes[i + 1:]}
    agree_tot, n_runs = 0.0, 0
    sizes, mods = [], []
    for s in seeds:
        comm, parts = louvain(u, s)
        sizes.append(len(parts))
        mods.append(nx_comm.modularity(u, parts, weight="weight"))
        same = sum(1 for (a, b), v in base_same.items()
                   if (comm[a] == comm[b]) == v)
        agree_tot += same / float(len(base_same))
        n_runs += 1
    return agree_tot / n_runs, (min(sizes), max(sizes)), (min(mods), max(mods))


def ranks(values, higher_is_better=True):
    """Hạng 1 là cao nhất. Bằng điểm thì cùng hạng, hạng kế bị đẩy xuống."""
    order = sorted(values.items(), key=lambda kv: -kv[1] if higher_is_better else kv[1])
    out, prev, prev_rank = {}, None, 0
    for i, (k, v) in enumerate(order, start=1):
        if v != prev:
            prev_rank, prev = i, v
        out[k] = prev_rank
    return out


# ---------------------------------------------------------------------------
# Ghi file
# ---------------------------------------------------------------------------
# Số trong CSV giữ nguyên dấu chấm thập phân và không phân nhóm nghìn: file này
# để MÁY đọc (pandas, plotly ở T15-T17). Mục 6.3 của style guide nói về con số
# NGƯỜI đọc — bảng in ra màn hình bên dưới và nhãn trên hình thì đi qua fmt_*.
FIELDS = [
    "country_iso3", "country_name_vi", "region", "continent", "is_focus",
    "graph", "degree_in", "degree_out", "degree_total",
    "strength_in", "strength_out", "strength_total", "world_export_share",
    "betweenness", "betweenness_unweighted", "community",
    "rank_strength_out", "rank_degree_out", "rank_degree_total",
    "rank_betweenness", "n_tied_betweenness",
    "eci", "eci_rank", "year",
]


def write_csv(path, fields, rows):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    log("  -> %s  (%d dòng, %s KB)"
        % (os.path.relpath(path, ROOT), len(rows),
           R.fmt_vn(os.path.getsize(path) / 1e3)))


def metrics_for(g, label, meta, eci, world_total, year, seed, verbose=True):
    """Một dòng cho mỗi nước CÓ MẶT trong đồ thị này."""
    bw, bw_unw = betweenness(g)
    u = undirected_projection(g)
    comm, parts = louvain(u, seed)
    mod = nx_comm.modularity(u, parts, weight="weight")

    s_out = {c: sum(d["weight"] for _, _, d in g.out_edges(c, data=True)) for c in g}
    s_in = {c: sum(d["weight"] for _, _, d in g.in_edges(c, data=True)) for c in g}

    r_sout = ranks(s_out)
    r_dout = ranks({c: g.out_degree(c) for c in g})
    r_deg = ranks({c: g.in_degree(c) + g.out_degree(c) for c in g})
    r_bw = ranks(bw)
    # Hạng betweenness gần như vô dụng nếu đọc một mình: trên đồ thị dày, phần
    # lớn các nước có betweenness đúng bằng 0 và cùng chung một hạng. "Hạng 16"
    # nghe như đứng thứ 16, thật ra là đồng hạng với 57 nước khác. Nên lưu luôn
    # số nước cùng hạng, để chỗ nào in hạng cũng in được cả cỡ của đám đồng hạng.
    n_tied = {}
    for c in g:
        n_tied[c] = sum(1 for d in g if r_bw[d] == r_bw[c])

    rows = []
    for c in sorted(g.nodes()):
        m = meta.get(c, {})
        e = eci.get(c, ("", ""))
        rows.append({
            "country_iso3": c,
            "country_name_vi": m.get("country_name_vi", c),
            "region": m.get("region", ""),
            "continent": m.get("continent", ""),
            "is_focus": m.get("is_focus", "FALSE"),
            "graph": label,
            "degree_in": g.in_degree(c),
            "degree_out": g.out_degree(c),
            "degree_total": g.in_degree(c) + g.out_degree(c),
            "strength_in": "%.0f" % s_in[c],
            "strength_out": "%.0f" % s_out[c],
            "strength_total": "%.0f" % (s_in[c] + s_out[c]),
            # CHỈ điền ở dòng `full`. Ở dòng `filtered`, tử số đã bị ngưỡng cắt
            # mất phần lớn nên tỉ lệ đó không phải thị phần của nước nào cả;
            # để rỗng thì không ai vô tình dán nhầm nó lên hình. Độ phủ của
            # ngưỡng đã có sẵn trong threshold_coverage.csv của T10.
            "world_export_share": ("%.6f" % (100.0 * s_out[c] / world_total)
                                   if label == "full" else ""),
            "betweenness": "%.6f" % bw.get(c, 0.0),
            "betweenness_unweighted": "%.6f" % bw_unw.get(c, 0.0),
            "community": comm[c],
            "rank_strength_out": r_sout[c],
            "rank_degree_out": r_dout[c],
            "rank_degree_total": r_deg[c],
            "rank_betweenness": r_bw[c],
            "n_tied_betweenness": n_tied[c],
            "eci": e[0],
            "eci_rank": e[1],
            "year": year,
        })

    if verbose:
        n_zero = sum(1 for c in g if bw.get(c, 0.0) == 0.0)
        log("  %-9s %3d nút, %6d cạnh — %d cụm, modularity %s"
            % (label, g.number_of_nodes(), g.number_of_edges(),
               len(parts), R.fmt_vn(mod, 3)))
        log("            betweenness = 0 ở %s nước (%s)"
            % (R.fmt_vn(n_zero, 0),
               R.fmt_pct(100.0 * n_zero / g.number_of_nodes())))
    return rows, u, comm, parts, mod


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--seed", type=int, default=42,
                    help="hạt giống Louvain, cố định để chạy lại ra đúng kết quả cũ")
    args = ap.parse_args()

    log("Đọc dữ liệu năm %d..." % args.year)
    meta = load_nodes()
    eci = load_eci(args.year)
    full_e, filt_e = load_edges(args.year)
    world_total = sum(v for _, _, v in full_e)
    log("  %s cạnh đầy đủ, %s cạnh sau ngưỡng, tổng xuất khẩu thế giới %s"
        % (R.fmt_vn(len(full_e), 0), R.fmt_vn(len(filt_e), 0),
           R.fmt_usd(world_total, 2)))

    g_full = build(full_e)
    g_filt = build(filt_e)

    log("\nTính chỉ số:")
    rows_full, _, _, _, _ = metrics_for(g_full, "full", meta, eci,
                                        world_total, args.year, args.seed)
    rows_filt, u_filt, comm_filt, parts_filt, mod_filt = metrics_for(
        g_filt, "filtered", meta, eci, world_total, args.year, args.seed)

    # Độ ổn định của phân hoạch — chỉ đo trên đồ thị đã lọc, vì đó là đồ thị
    # mà màu cụm sẽ xuất hiện trên hình ở T15 và thứ tự hàng ở T16.
    log("\nĐộ ổn định cộng đồng trên đồ thị đã lọc (%d hạt giống):" % N_SEEDS_CHECK)
    agree, (smin, smax), (mmin, mmax) = partition_stability(
        u_filt, comm_filt, range(N_SEEDS_CHECK))
    log("  %s số cặp nước giữ nguyên quan hệ cùng cụm / khác cụm"
        % R.fmt_pct(100.0 * agree, 1))
    log("  số cụm: %d–%d    modularity: %s–%s"
        % (smin, smax, R.fmt_vn(mmin, 3), R.fmt_vn(mmax, 3)))
    if smin != smax:
        log("  LƯU Ý: số cụm đổi theo hạt giống. Mọi hình phải ghi rõ seed=%d."
            % args.seed)

    log("\nGhi file:")
    write_csv(os.path.join(OUT, "metrics.csv"), FIELDS, rows_full + rows_filt)

    # --- bảng top 20 -------------------------------------------------------
    by_iso_filt = {r["country_iso3"]: r for r in rows_filt}
    top = sorted(rows_full, key=lambda r: -float(r["strength_out"]))[:TOP_N]
    t_fields = ["rank", "country_iso3", "country_name_vi", "export_value",
                "world_export_share", "degree_out_full", "degree_in_full",
                "degree_total_filtered", "betweenness_filtered",
                "community_filtered", "eci", "eci_rank", "year"]
    t_rows = []
    for i, r in enumerate(top, start=1):
        f = by_iso_filt.get(r["country_iso3"], {})
        t_rows.append({
            "rank": i,
            "country_iso3": r["country_iso3"],
            "country_name_vi": r["country_name_vi"],
            "export_value": r["strength_out"],
            "world_export_share": r["world_export_share"],
            "degree_out_full": r["degree_out"],
            "degree_in_full": r["degree_in"],
            # Rỗng nghĩa là nước này không còn cạnh nào sau ngưỡng, khác hẳn 0.
            "degree_total_filtered": f.get("degree_total", ""),
            "betweenness_filtered": f.get("betweenness", ""),
            "community_filtered": f.get("community", ""),
            "eci": r["eci"],
            "eci_rank": r["eci_rank"],
            "year": args.year,
        })
    write_csv(os.path.join(OUT, "metrics_top20.csv"), t_fields, t_rows)

    # --- in ra để kiểm bằng mắt -------------------------------------------
    log("\nTop %d nước xuất khẩu, năm %d:" % (TOP_N, args.year))
    log("  %-4s %-4s %-22s %16s %8s %7s %6s %5s %7s"
        % ("Hạng", "ISO", "Nước", "Xuất khẩu", "Thế giới", "Bậc ra", "Btw", "Cụm", "ECI"))
    for t in t_rows:
        mark = " ◆" if t["country_iso3"] in R.FOCUS_ISO3 else "  "
        log("  %-4d %-4s %-20s%s %16s %8s %7s %6s %5s %7s"
            % (t["rank"], t["country_iso3"], t["country_name_vi"][:20], mark,
               R.fmt_usd(float(t["export_value"]), 1),
               R.fmt_pct(float(t["world_export_share"]), 2),
               t["degree_out_full"],
               R.fmt_vn(float(t["betweenness_filtered"]), 3)
               if t["betweenness_filtered"] != "" else "—",
               t["community_filtered"] if t["community_filtered"] != "" else "—",
               R.fmt_vn(float(t["eci"]), 2) if t["eci"] else "—"))

    # ASEAN nằm ngoài top 20 vẫn phải thấy được: lát cắt của bài là Việt Nam
    # trong ASEAN, một bảng cắt ở hạng 20 sẽ giấu mất phần lớn khối này.
    in_top = {t["country_iso3"] for t in t_rows}
    out_asean = [r for r in rows_full
                 if r["country_iso3"] in R.ASEAN_ISO3 and r["country_iso3"] not in in_top]
    if out_asean:
        log("\nASEAN ngoài top %d:" % TOP_N)
        for r in sorted(out_asean, key=lambda r: int(r["rank_strength_out"])):
            f = by_iso_filt.get(r["country_iso3"], {})
            log("  %-4s %-4s %-20s   %16s %8s %7s %6s %5s %7s"
                % (r["rank_strength_out"], r["country_iso3"],
                   r["country_name_vi"][:20],
                   R.fmt_usd(float(r["strength_out"]), 1),
                   R.fmt_pct(float(r["world_export_share"]), 2),
                   r["degree_out"],
                   R.fmt_vn(float(f["betweenness"]), 3) if f else "—",
                   f.get("community", "—"),
                   R.fmt_vn(float(r["eci"]), 2) if r["eci"] else "—"))

    # --- Việt Nam, đọc kỹ hơn một chút -------------------------------------
    vn_full = next((r for r in rows_full if r["country_iso3"] == "VNM"), None)
    vn_filt = by_iso_filt.get("VNM")
    if vn_full:
        n_full, n_filt = len(rows_full), len(rows_filt)
        log("\nViệt Nam, năm %d:" % args.year)
        log("  xuất khẩu %s — %s tổng thế giới, hạng %s/%s"
            % (R.fmt_usd(float(vn_full["strength_out"]), 1),
               R.fmt_pct(float(vn_full["world_export_share"]), 3),
               vn_full["rank_strength_out"], R.fmt_vn(n_full, 0)))
        log("  đồ thị đầy đủ: %s bạn hàng xuất (hạng %s/%s), %s bạn hàng nhập,"
            " hạng bậc tổng %s/%s"
            % (vn_full["degree_out"], vn_full["rank_degree_out"],
               R.fmt_vn(n_full, 0), vn_full["degree_in"],
               vn_full["rank_degree_total"], R.fmt_vn(n_full, 0)))
        if vn_filt:
            tie = int(vn_filt["n_tied_betweenness"])
            tie_note = ("" if tie == 1
                        else " — ĐỒNG HẠNG với %s nước khác, nên con số hạng này"
                             " không nói lên điều gì" % R.fmt_vn(tie - 1, 0))
            log("  đồ thị đã lọc: còn %s cạnh, betweenness %s (hạng %s/%s)%s"
                % (vn_filt["degree_total"],
                   R.fmt_vn(float(vn_filt["betweenness"]), 4),
                   vn_filt["rank_betweenness"], R.fmt_vn(n_filt, 0), tie_note))
            same = [r["country_iso3"] for r in rows_filt
                    if r["community"] == vn_filt["community"]]
            log("  thuộc cụm số %s, cụm này có %s nước khác: %s"
                % (vn_filt["community"], R.fmt_vn(len(same) - 1, 0),
                   " ".join(c for c in same if c != "VNM")))
        else:
            log("  đồ thị đã lọc: KHÔNG còn cạnh nào — kiểm lại bảo hiểm top-k ở T10.")
        if vn_full["eci"]:
            log("  ECI %s, hạng %s" % (R.fmt_vn(float(vn_full["eci"]), 2),
                                       vn_full["eci_rank"]))

    log("\nXong. Hai file nằm trong data/processed/ (đã bị .gitignore loại trừ).")


if __name__ == "__main__":
    main()

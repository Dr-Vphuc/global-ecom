# -*- coding: utf-8 -*-
"""Thống kê mô tả mạng lưới (T09) và bảng đánh đổi ngưỡng lọc cạnh (T10).

Đọc data/processed/edges.csv rồi sinh ba file:

    data/processed/network_stats.csv        thống kê theo từng năm 1995-2024
    data/processed/degree_distribution.csv  phân bố bậc, dạng dài, sẵn cho log-log
    data/processed/threshold_coverage.csv   bảng ngưỡng-vs-độ-phủ cho T10

Chạy:
    python src/analyze_network.py
    python src/analyze_network.py --year 2015

Script CHỈ ĐO, không vẽ — nên vẫn chỉ dùng thư viện chuẩn như phần còn lại của
pipeline. Việc vẽ thuộc T15-T17 và cần `pip install -r requirements.txt`.
"""

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reference_data import (  # noqa: E402
    ASEAN_ISO3,
    FOCUS_ISO3,
    FOCUS_TOPK,
    MILESTONE_YEARS,
    REFERENCE_YEAR,
    THRESHOLD_SHARE,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "processed")
EDGES = os.path.join(OUT, "edges.csv")

# Cac nguong tuyet doi dem thu, USD. Trai deu tren thang log tu 100 trieu den
# 100 ty de bang ket qua the hien duoc ca doan doc lan doan thoai.
THRESHOLDS = [1e8, 2.5e8, 5e8, 1e9, 2.5e9, 5e9, 1e10, 2.5e10, 5e10, 1e11]

# Nguong tuong doi: ty le tren tong xuat khau the gioi CUA NAM DO. Muc dich la
# so canh giu lai on dinh qua cac nam, de small multiples so sanh duoc.
SHARES = [0.0001, 0.0002, 0.00046, 0.001]

# Phuong an thay the: moi nuoc giu lai k luong xuat khau lon nhat cua chinh no.
# Khac han nguong tuyet doi o mot diem — khong nuoc nao bi xoa khoi ban do.
TOPK = [1, 2, 3, 5, 10, 20]


def log(msg):
    print(msg, flush=True)


def write_csv(path, fieldnames, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    log("  -> %s  (%d dong, %.1f KB)"
        % (os.path.relpath(path, ROOT), len(rows), os.path.getsize(path) / 1e3))


def gini(vals):
    """Do lech cua mot phan phoi: 0 = deu tuyet doi, 1 = mot minh chiem het.

    Dung cho trong so canh. Day moi la cho ma mang luoi thuong mai lech, chu
    khong phai o bac — xem ghi chu trong stage_stats().
    """
    v = sorted(vals)
    n = len(v)
    s = sum(v)
    if n == 0 or s <= 0:
        return 0.0
    cum = sum((i + 1) * x for i, x in enumerate(v))
    return (2.0 * cum) / (n * s) - (n + 1.0) / n


def load_edges():
    """Doc edges.csv mot lan, gom theo nam.

    Tra ve dict: year -> {"e": [(src, dst, value)], "out": {}, "in": {}}.
    Doc mot lan roi giu trong RAM het khoang 80 MB cho ca 750k dong; doc lai
    30 lan cho 30 nam thi sach hon nhung cham gap vai chuc lan.
    """
    if not os.path.exists(EDGES):
        sys.exit("THIEU FILE: %s\n  -> chay: python src/build_intermediate.py"
                 % os.path.relpath(EDGES, ROOT))

    years = {}
    with open(EDGES, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            try:
                y = int(r["year"])
                v = float(r["export_value"])
            except (ValueError, TypeError, KeyError):
                continue
            d = years.setdefault(y, {"e": [], "out": {}, "in": {}})
            s, t = r["source_iso3"], r["target_iso3"]
            d["e"].append((s, t, v))
            d["out"][s] = d["out"].get(s, 0) + 1
            d["in"][t] = d["in"].get(t, 0) + 1
    return years


# ---------------------------------------------------------------------------
# [1/3] network_stats.csv
# ---------------------------------------------------------------------------
def stage_stats(years):
    log("\n[1/3] network_stats.csv")
    rows = []
    for y in sorted(years):
        d = years[y]
        edges = d["e"]
        nodes = set(d["out"]) | set(d["in"])
        n, m = len(nodes), len(edges)
        # Mang co huong: so cap co the la n*(n-1), khong chia doi.
        dens = m / float(n * (n - 1)) if n > 1 else 0.0

        vals = sorted((v for _, _, v in edges), reverse=True)
        tot = sum(vals)
        n_top1 = max(1, m // 100)
        top1 = sum(vals[:n_top1]) / tot if tot else 0.0

        deg = sorted(d["out"].get(c, 0) + d["in"].get(c, 0) for c in nodes)

        # Doi ung: A xuat sang B thi B co xuat nguoc lai khong. Gan 1 nghia la
        # thuong mai gan nhu luon hai chieu, nen huong cua canh mang it thong
        # tin — dang chu y khi chon giua node-link co mui ten va khong mui ten.
        pairs = {(s, t) for s, t, _ in edges}
        recip = sum(1 for s, t in pairs if (t, s) in pairs) / float(m) if m else 0.0

        rows.append({
            "year": y,
            "n_nodes": n,
            "n_edges": m,
            "density": "%.4f" % dens,
            "reciprocity": "%.4f" % recip,
            "total_export_value": "%.0f" % tot,
            "mean_degree": "%.1f" % (sum(deg) / float(n)) if n else "0",
            "median_degree": deg[n // 2] if n else 0,
            "max_degree": deg[-1] if deg else 0,
            "min_degree": deg[0] if deg else 0,
            # Hai cot duoi moi la phan "phan bo trong so" cua T09.
            "gini_edge_value": "%.4f" % gini(vals),
            "top1pct_value_share": "%.4f" % top1,
        })

    write_csv(os.path.join(OUT, "network_stats.csv"), list(rows[0].keys()), rows)

    for r in (rows[0], rows[-1]):
        log("  %d: %3d nut, %6d canh, mat do %s, doi ung %s, Gini %s"
            % (r["year"], r["n_nodes"], r["n_edges"], r["density"],
               r["reciprocity"], r["gini_edge_value"]))
    return rows


# ---------------------------------------------------------------------------
# [2/3] degree_distribution.csv
# ---------------------------------------------------------------------------
def stage_degree(years, focus_years):
    log("\n[2/3] degree_distribution.csv")
    rows = []
    for y in focus_years:
        if y not in years:
            continue
        d = years[y]
        nodes = set(d["out"]) | set(d["in"])
        for kind, src in (("out", d["out"]), ("in", d["in"])):
            degs = [src.get(c, 0) for c in nodes]
            n = len(degs)
            cnt = {}
            for v in degs:
                cnt[v] = cnt.get(v, 0) + 1
            # CCDF = ty le nuoc co bac >= d. Dung CCDF chu khong dung tan suat
            # tho, vi tan suat o phan duoi rat thua — moi bac chi vai nuoc — ve
            # log-log thanh mot dam cham loang xoang. CCDF lam muot ma khong
            # phai chia o, tuc khong phai chon do rong o mot cach cam tinh.
            tail = n
            for k in sorted(cnt):
                rows.append({
                    "year": y,
                    "kind": kind,
                    "degree": k,
                    "n_countries": cnt[k],
                    "ccdf": "%.6f" % (tail / float(n)),
                })
                tail -= cnt[k]

    write_csv(os.path.join(OUT, "degree_distribution.csv"),
              ["year", "kind", "degree", "n_countries", "ccdf"], rows)
    return rows


# ---------------------------------------------------------------------------
# [3/3] threshold_coverage.csv
# ---------------------------------------------------------------------------
def fmt_ty(th):
    return ("%.1f" % (th / 1e9)).rstrip("0").rstrip(".")


def summarise(kept, total_e, total_v, strategy, param, label):
    nodes = set()
    for s, t, _ in kept:
        nodes.add(s)
        nodes.add(t)
    mat = [c for c in ASEAN_ISO3 if c not in nodes]
    val = sum(v for _, _, v in kept)
    return {
        "strategy": strategy,
        "param": param,
        "label": label,
        "n_edges": len(kept),
        "pct_edges": "%.2f" % (100.0 * len(kept) / total_e),
        "pct_value": "%.2f" % (100.0 * val / total_v),
        "n_nodes": len(nodes),
        "n_asean": len(ASEAN_ISO3) - len(mat),
        "asean_missing": " ".join(mat),
        "vnm_edges": sum(1 for s, t, _ in kept if "VNM" in (s, t)),
    }


def pick_chosen(edges, total_v, share, topk):
    """Quy tac da chot o T10: nguong tuong doi + bao hiem cho nuoc trong tam.

    Giu nguyen logic cua mark_threshold() trong build_intermediate.py. Hai cho
    phai khop nhau; neu sua mot ben thi sua ca ben kia.
    """
    th = share * total_v
    keep = set((s, t) for s, t, v in edges if v >= th)
    for c in FOCUS_ISO3:
        outs = sorted([e for e in edges if e[0] == c], key=lambda z: -z[2])
        ins = sorted([e for e in edges if e[1] == c], key=lambda z: -z[2])
        keep.update(e[:2] for e in outs[:topk])
        keep.update(e[:2] for e in ins[:topk])
    return [e for e in edges if (e[0], e[1]) in keep]


def stage_threshold(years, year):
    log("\n[3/3] threshold_coverage.csv  (nam %d)" % year)
    edges = years[year]["e"]
    total_e = len(edges)
    total_v = sum(v for _, _, v in edges)
    rows = []

    for th in THRESHOLDS:
        kept = [e for e in edges if e[2] >= th]
        if kept:
            rows.append(summarise(kept, total_e, total_v, "absolute",
                                  "%.0f" % th, ">= %s ty USD" % fmt_ty(th)))

    # Top-k theo tung nuoc xuat khau. Gop lai bang union nen tong so canh it hon
    # k * so_nuoc: nhieu luong lon duoc dem mot lan du ca hai phia deu chon no.
    by_src = {}
    for e in edges:
        by_src.setdefault(e[0], []).append(e)
    for lst in by_src.values():
        lst.sort(key=lambda e: -e[2])
    for k in TOPK:
        kept, seen = [], set()
        for lst in by_src.values():
            for e in lst[:k]:
                if (e[0], e[1]) not in seen:
                    seen.add((e[0], e[1]))
                    kept.append(e)
        rows.append(summarise(kept, total_e, total_v, "topk_per_country", k,
                              "moi nuoc giu %d luong lon nhat" % k))

    for p in SHARES:
        th = p * total_v
        kept = [e for e in edges if e[2] >= th]
        if kept:
            rows.append(summarise(kept, total_e, total_v, "relative", p,
                                  "%.3f%% tong the gioi (= %s ty)"
                                  % (p * 100, fmt_ty(th))))

    # Quy tac DA CHON: nguong tuong doi cong bao hiem topk vao/ra cho moi nuoc
    # trong tam. Hai dong cuoi bang la cai duoc dua vao bao cao.
    kept = pick_chosen(edges, total_v, THRESHOLD_SHARE, FOCUS_TOPK)
    rows.append(summarise(kept, total_e, total_v, "CHOSEN", THRESHOLD_SHARE,
                          "%.3f%% + top-%d vao/ra cho ASEAN"
                          % (THRESHOLD_SHARE * 100, FOCUS_TOPK)))

    write_csv(os.path.join(OUT, "threshold_coverage.csv"),
              list(rows[0].keys()), rows)

    log("  %-30s %6s %6s %6s %5s %6s" %
        ("phuong an", "canh", "%canh", "%gtri", "nut", "ASEAN"))
    for r in rows:
        log("  %-30s %6d %6s %6s %5d %5d/10%s"
            % (r["label"], r["n_edges"], r["pct_edges"], r["pct_value"],
               r["n_nodes"], r["n_asean"],
               "  thieu " + r["asean_missing"] if r["asean_missing"] else ""))
    return rows


def check_across_years(years, focus_years):
    """Quy tac chon cho mot nam phai dung duoc ca o small multiples (T20).

    Doi chieu thang hai phuong an tren cung mot bang: nguong tuyet doi 10 ty USD
    (phuong an cu) va quy tac da chot. Cot dang nhin la so canh - no phai on
    dinh qua cac nam, neu khong thi cac panel khong so sanh duoc voi nhau.
    """
    log("\nDoi chieu qua cac nam moc:")
    log("  %-6s | %-28s | %s" % ("nam", "cu: nguong co dinh 10 ty USD",
                                 "chot: %.3f%% + top-%d ASEAN"
                                 % (THRESHOLD_SHARE * 100, FOCUS_TOPK)))
    for y in focus_years:
        if y not in years:
            continue
        edges = years[y]["e"]
        tv = sum(v for _, _, v in edges)
        cells = []
        for kept in ([e for e in edges if e[2] >= 1e10],
                     pick_chosen(edges, tv, THRESHOLD_SHARE, FOCUS_TOPK)):
            nodes = set()
            for s, t, _ in kept:
                nodes.add(s)
                nodes.add(t)
            na = sum(1 for c in ASEAN_ISO3 if c in nodes)
            cells.append("%4d canh %5.1f%% gtri %3d nut ASEAN %2d/10"
                         % (len(kept), 100.0 * sum(v for _, _, v in kept) / tv,
                            len(nodes), na))
        log("  %-6d | %-28s | %s" % (y, cells[0], cells[1]))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--year", type=int, default=REFERENCE_YEAR,
                    help="nam dung cho bang nguong (mac dinh %d)" % REFERENCE_YEAR)
    args = ap.parse_args()

    log("Doc %s ..." % os.path.relpath(EDGES, ROOT))
    years = load_edges()
    log("  %d nam, %d canh"
        % (len(years), sum(len(d["e"]) for d in years.values())))
    if args.year not in years:
        sys.exit("Khong co nam %d trong edges.csv" % args.year)

    focus = sorted(set(MILESTONE_YEARS) | {args.year})
    stage_stats(years)
    stage_degree(years, focus)
    stage_threshold(years, args.year)
    check_across_years(years, focus)
    log("\nXong. File nam trong data/processed/ (da bi .gitignore loai tru).")


if __name__ == "__main__":
    main()

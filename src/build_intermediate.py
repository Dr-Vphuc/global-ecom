# -*- coding: utf-8 -*-
"""Sinh 5 file trung gian THẬT từ bộ Atlas theo đúng HỢP ĐỒNG DỮ LIỆU.

    data/atlas/location_country.csv    ->  data/processed/nodes.csv
    data/atlas/cc_year.csv             ->  data/processed/edges.csv
    data/atlas/product_hs92.csv        ->  data/processed/tree.csv
    data/atlas/cp_year_hs2.csv         ->  data/processed/country_product.csv
    data/atlas/hs92_country_year.csv   ->  data/processed/country_year.csv

Chạy:
    python src/build_intermediate.py
    python src/build_intermediate.py --threshold-share 0.00046

Chỉ dùng thư viện chuẩn — chạy được ngay trên máy sạch, không cần pip install.
Mọi đường dẫn đều tương đối so với gốc repo (checklist #21).
"""

import argparse
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reference_data import (  # noqa: E402
    COUNTRY_VI,
    FOCUS_TOPK,
    FOCUS_ISO3,
    MILESTONE_YEARS,
    NON_COUNTRY,
    REFERENCE_YEAR,
    THRESHOLD_SHARE,
    SECTOR_PALETTE_PROVISIONAL,
    UNINHABITED,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "atlas")
OUT = os.path.join(ROOT, "data", "processed")

# csv.field_size_limit mặc định đủ cho bộ này, nhưng tên nước có dấu phẩy
# ("Saint Helena, Ascension and Tristan da Cunha") nên BẮT BUỘC dùng
# csv.DictReader thay vì tách chuỗi bằng split(",").


def log(msg):
    print(msg, flush=True)


def read_csv(path):
    if not os.path.exists(path):
        sys.exit(
            "THIEU FILE: %s\n"
            "Xem README muc 'Tai lai du lieu' de biet cach lay file nay." % path
        )
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path, fieldnames, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    size_mb = os.path.getsize(path) / 1e6
    log("  -> %s  (%d dong, %.1f MB)" % (os.path.relpath(path, ROOT), len(rows), size_mb))


# ---------------------------------------------------------------------------
# nodes.csv
# ---------------------------------------------------------------------------
def build_nodes():
    log("\n[1/5] nodes.csv")
    src = read_csv(os.path.join(RAW, "location_country.csv"))
    rows, missing = [], []

    for r in src:
        iso3 = r["country_iso3_code"].strip()
        if iso3 in COUNTRY_VI:
            name_vi, region, continent = COUNTRY_VI[iso3]
        else:
            missing.append(iso3)
            name_vi, region, continent = r["country_name"].strip(), "Other", "Other"
        rows.append(
            {
                "country_iso3": iso3,
                "country_id": r["country_id"].strip(),
                "country_name": r["country_name"].strip(),
                "country_name_vi": name_vi,
                "region": region,
                "continent": continent,
                "is_focus": "TRUE" if iso3 in FOCUS_ISO3 else "FALSE",
            }
        )

    rows.sort(key=lambda x: x["country_iso3"])
    write_csv(
        os.path.join(OUT, "nodes.csv"),
        ["country_iso3", "country_id", "country_name", "country_name_vi",
         "region", "continent", "is_focus"],
        rows,
    )

    if missing:
        log("  ! THIEU TEN TIENG VIET cho %d ma: %s" % (len(missing), ", ".join(missing)))
        log("    -> bo sung vao COUNTRY_VI trong src/reference_data.py")
    else:
        log("  OK: du ten tieng Viet cho ca %d nuoc" % len(rows))

    flagged = [r["country_iso3"] for r in rows if r["country_iso3"] in NON_COUNTRY]
    if flagged:
        log("  i Co %d ma KHONG phai quoc gia, VAN GIU lai: %s"
            % (len(flagged), ", ".join(flagged)))
        log("    -> giu de tai lap dung con so 230 nut / 25.425 canh. Quyet dinh o T10.")
    return {r["country_iso3"] for r in rows}


# ---------------------------------------------------------------------------
# edges.csv
# ---------------------------------------------------------------------------
def mark_threshold(rows, share, topk):
    """Dien cot above_threshold theo quy tac da chot o T10.

    Hai phan cong lai:
      1. Nguong tuong doi - giu canh co export_value >= share * tong xuat khau
         the gioi CUA NAM DO. Dung ty le chu khong dung so USD co dinh, vi neu
         co dinh thi nam 1995 chi con 89 canh con nam 2024 co 385, va small
         multiples se doc thanh "thuong mai moi xuat hien".
      2. Bao hiem cho nuoc trong tam - moi nuoc trong FOCUS_ISO3 luon giu topk
         luong xuat va topk luong nhap lon nhat cua chinh no. Khong co phan nay
         thi Viet Nam bien mat khoi nam 1995.

    Tra ve (nguong tung nam, so canh duoc giu).
    """
    tot = {}
    for r in rows:
        tot[r["year"]] = tot.get(r["year"], 0.0) + r["export_value"]
    th_year = dict((y, share * v) for y, v in tot.items())

    keep = set()
    out_of, in_of = {}, {}
    for i, r in enumerate(rows):
        if r["export_value"] >= th_year[r["year"]]:
            keep.add(i)
        if r["source_iso3"] in FOCUS_ISO3:
            out_of.setdefault((r["source_iso3"], r["year"]), []).append(i)
        if r["target_iso3"] in FOCUS_ISO3:
            in_of.setdefault((r["target_iso3"], r["year"]), []).append(i)

    for grp in (out_of, in_of):
        for idxs in grp.values():
            idxs.sort(key=lambda i: -rows[i]["export_value"])
            keep.update(idxs[:topk])

    for i, r in enumerate(rows):
        r["above_threshold"] = "TRUE" if i in keep else "FALSE"
    return th_year, len(keep)


def build_edges(known_iso3, share, topk):
    log("\n[2/5] edges.csv  (nguong = %.3f%% tong xuat khau the gioi moi nam)"
        % (share * 100))
    path = os.path.join(RAW, "cc_year.csv")
    if not os.path.exists(path):
        sys.exit("THIEU FILE: %s — xem README." % path)

    rows = []
    n_total = n_zero = n_bad = 0
    unknown = set()
    years = set()

    with open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            n_total += 1
            try:
                exp = float(r["export_value"] or 0)
                imp = float(r["import_value"] or 0)
                year = int(r["year"])
            except (ValueError, TypeError):
                n_bad += 1
                continue

            # Trong so cua canh la export_value. Gia tri 0 khong phai mot canh.
            if exp <= 0:
                n_zero += 1
                continue

            s = r["country_iso3_code"].strip()
            t = r["partner_iso3_code"].strip()
            if s not in known_iso3:
                unknown.add(s)
            if t not in known_iso3:
                unknown.add(t)

            years.add(year)
            rows.append(
                {
                    "source_iso3": s,
                    "target_iso3": t,
                    "year": year,
                    # Giu kieu so de mark_threshold() so sanh duoc; doi
                    # sang chuoi ngay truoc khi ghi.
                    "export_value": exp,
                    "import_value": repr(imp),
                    "log_value": "%.4f" % math.log10(exp),
                    "above_threshold": "",
                }
            )

    th_year, n_keep = mark_threshold(rows, share, topk)
    for r in rows:
        r["export_value"] = repr(r["export_value"])

    rows.sort(key=lambda x: (x["year"], x["source_iso3"], x["target_iso3"]))
    write_csv(
        os.path.join(OUT, "edges.csv"),
        ["source_iso3", "target_iso3", "year", "export_value", "import_value",
         "log_value", "above_threshold"],
        rows,
    )

    log("  doc %d dong -> giu %d canh" % (n_total, len(rows)))
    log("  loc: %d canh dat nguong (%.1f%%), vd nam %d nguong = %.2f ty USD"
        % (n_keep, 100.0 * n_keep / len(rows), REFERENCE_YEAR,
           th_year.get(REFERENCE_YEAR, 0) / 1e9))
    log("  bo %d dong co export_value = 0 (khong phai canh)" % n_zero)
    if n_bad:
        log("  ! bo %d dong hong khong doc duoc so" % n_bad)
    if unknown:
        log("  ! %d ma nuoc khong co trong nodes.csv: %s"
            % (len(unknown), ", ".join(sorted(unknown))))
    log("  nam: %d–%d (%d nam)" % (min(years), max(years), len(years)))

    # Con so cua nam moc - day la bo ba se trich vao bao cao va slide.
    ref = [r for r in rows if r["year"] == REFERENCE_YEAR]
    n_ref = len({r["source_iso3"] for r in ref} | {r["target_iso3"] for r in ref})
    dens = len(ref) / (n_ref * (n_ref - 1)) if n_ref > 1 else 0
    log("  NAM MOC %d: %d canh, %d nut, mat do %.3f"
        % (REFERENCE_YEAR, len(ref), n_ref, dens))
    log("  ! con so cu trong file phan cong (25425 / 230 / 0.483) do tren ban"
        " du lieu bi cat - da bo.")
    return rows


# ---------------------------------------------------------------------------
# tree.csv
# ---------------------------------------------------------------------------
def build_tree():
    log("\n[3/5] tree.csv")
    src = read_csv(os.path.join(RAW, "product_hs92.csv"))
    by_id = {r["product_id"]: r for r in src}

    def sector_of(rec):
        """Leo nguoc len cay de tim to tien cap 1."""
        seen = set()
        cur = rec
        while cur["product_parent_id"]:
            if cur["product_id"] in seen:      # chong vong lap neu du lieu hong
                return None
            seen.add(cur["product_id"])
            cur = by_id.get(cur["product_parent_id"])
            if cur is None:
                return None
        return int(cur["product_id"])

    rows, no_sector = [], []
    levels = {}
    for r in src:
        sid = sector_of(r)
        if sid is None:
            no_sector.append(r["product_id"])
        lvl = int(r["product_level"])
        levels[lvl] = levels.get(lvl, 0) + 1
        rows.append(
            {
                "product_id": r["product_id"],
                "parent_id": r["product_parent_id"],
                "level": lvl,
                "hs92_code": r["product_hs92_code"],   # giu text, khong mat so 0 dau
                "name": r["product_name"],
                "name_short": r["product_name_short"],
                "sector_id": sid if sid else "",
                "sector_color": SECTOR_PALETTE_PROVISIONAL.get(sid, ""),
            }
        )

    rows.sort(key=lambda x: (x["level"], int(x["product_id"])))
    write_csv(
        os.path.join(OUT, "tree.csv"),
        ["product_id", "parent_id", "level", "hs92_code", "name", "name_short",
         "sector_id", "sector_color"],
        rows,
    )

    # T11 — kiem tra chat luong cay.
    expect = {1: 10, 2: 97, 4: 1243, 6: 5040}
    ok = levels == expect
    log("  so nut theo tang: %s" % dict(sorted(levels.items())))
    log("  KIEM TRA T11: %s (mong doi %s)" % ("DAT" if ok else "KHONG DAT", expect))
    ids = set(by_id)
    orphan = [r["product_id"] for r in src
              if r["product_parent_id"] and r["product_parent_id"] not in ids]
    log("  nut mo coi: %d | nut khong gan duoc nganh: %d" % (len(orphan), len(no_sector)))
    log("  ! sector_color dang la bang mau TAM — phai thay o T04.")


# ---------------------------------------------------------------------------
# country_product.csv
# ---------------------------------------------------------------------------
def build_country_product():
    """Co cau xuat khau theo nuoc - san pham HS2, kem RCA tu tinh."""
    log("\n[4/5] country_product.csv")
    path = os.path.join(RAW, "cp_year_hs2.csv")
    if not os.path.exists(path):
        log("  ! THIEU %s" % os.path.relpath(path, ROOT))
        log("    -> chay: python src/download_atlas.py")
        log("    (chi T12-T14 can file nay; ba file tren van dung duoc)")
        return

    names = {r["product_id"]: r["product_name_short"]
             for r in read_csv(os.path.join(RAW, "product_hs92.csv"))}

    # Doc hai luot thay vi giu 628k dong trong bo nho:
    #   luot 1 cong tong theo nuoc-nam, theo san pham-nam va theo nam;
    #   luot 2 tinh RCA roi ghi thang ra file.
    log("  luot 1/2: cong tong theo nuoc, theo san pham, theo nam")
    tot_c, tot_p, tot_w = {}, {}, {}
    n_total = n_zero = 0
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            n_total += 1
            v = float(r["export_value"] or 0)
            if v <= 0:
                n_zero += 1
                continue
            y, c, pid = r["year"], r["country_iso3_code"], r["product_id"]
            tot_c[(c, y)] = tot_c.get((c, y), 0.0) + v
            tot_p[(pid, y)] = tot_p.get((pid, y), 0.0) + v
            tot_w[y] = tot_w.get(y, 0.0) + v

    log("  luot 2/2: tinh RCA va ghi file")
    out = os.path.join(OUT, "country_product.csv")
    os.makedirs(OUT, exist_ok=True)
    fields = ["country_iso3", "product_id", "year", "export_value", "rca", "pci"]

    ref = str(REFERENCE_YEAR)
    gms_dev = 0.0        # lech giua thi phan tu tinh va cot co san trong file goc
    weighted = {}        # kiem dinh: trung binh RCA co trong = 1 cho moi san pham
    vnm_ref = []         # de in thu vai dong cho Viet Nam
    n_out = 0

    src = open(path, encoding="utf-8-sig", newline="")
    dst = open(out, "w", encoding="utf-8", newline="")
    with src, dst:
        w = csv.DictWriter(dst, fieldnames=fields)
        w.writeheader()
        for r in csv.DictReader(src):
            v = float(r["export_value"] or 0)
            if v <= 0:
                continue
            y, c, pid = r["year"], r["country_iso3_code"], r["product_id"]
            xc, xp, xw = tot_c[(c, y)], tot_p[(pid, y)], tot_w[y]

            # RCA Balassa: ti trong san pham p trong ro xuat khau cua nuoc c,
            # chia cho ti trong cua p trong ro xuat khau toan the gioi.
            # RCA > 1 = nuoc do xuat khau p dam dac hon muc trung binh the gioi.
            rca = (v / xc) / (xp / xw)

            # Doi chieu voi cot global_market_share (= v / xp) co san trong file
            # goc. Lech lon nghia la tong theo san pham cua ta bi thieu dong.
            gms = float(r["global_market_share"] or 0)
            if gms >= 1e-4:
                gms_dev = max(gms_dev, abs(v / xp - gms) / gms)

            if y == ref:
                weighted[pid] = weighted.get(pid, 0.0) + (xc / xw) * rca
                if c == "VNM":
                    vnm_ref.append((rca, v, pid))

            w.writerow({
                "country_iso3": c,
                "product_id": pid,
                "year": int(y),
                "export_value": repr(v),
                "rca": "%.4f" % rca,
                "pci": r["pci"],
            })
            n_out += 1

    log("  -> %s  (%d dong, %.1f MB)"
        % (os.path.relpath(out, ROOT), n_out, os.path.getsize(out) / 1e6))
    log("  doc %d dong -> giu %d (bo %d dong export_value = 0)"
        % (n_total, n_out, n_zero))

    # --- Hai phep kiem dinh ---
    # 1. Thi phan tu tinh phai trung cot co san trong du lieu goc.
    log("  KIEM DINH 1 - thi phan tu tinh vs cot goc: lech toi da %.3f%%  %s"
        % (gms_dev * 100, "DAT" if gms_dev < 0.01 else "KHONG DAT"))
    # 2. Voi moi san pham, trung binh RCA co trong theo quy mo nuoc phai bang 1.
    #    Day la tinh chat toan hoc cua chi so Balassa; sai la cong thuc sai.
    worst = max((abs(s - 1.0) for s in weighted.values()), default=0.0)
    log("  KIEM DINH 2 - trung binh RCA co trong (phai = 1): lech toi da %.1e  %s"
        % (worst, "DAT" if worst < 1e-6 else "KHONG DAT"))

    vnm_ref.sort(reverse=True)
    log("  Viet Nam %d - 5 nhom hang co RCA cao nhat:" % REFERENCE_YEAR)
    for rca, v, pid in vnm_ref[:5]:
        log("    RCA %6.2f  %6.1f ty USD  %s" % (rca, v / 1e9, names.get(pid, pid)))


# ---------------------------------------------------------------------------
# country_year.csv
# ---------------------------------------------------------------------------
def build_country_year():
    """Chi so phuc tap kinh te theo nuoc - nam, kem thu hang tu xep."""
    log("\n[5/5] country_year.csv")
    path = os.path.join(RAW, "hs92_country_year.csv")
    if not os.path.exists(path):
        log("  ! THIEU %s" % os.path.relpath(path, ROOT))
        log("    -> chay: python src/download_atlas.py")
        log("    (bon file tren van dung duoc)")
        return

    src = read_csv(path)

    # Thu hang ECI khong co san trong du lieu goc nen phai tu xep theo tung nam.
    # Hang 1 = ECI cao nhat. Nuoc khong co ECI thi de trong, khong xep hang.
    by_year = {}
    for r in src:
        if r["eci"] not in ("", "None"):
            by_year.setdefault(r["year"], []).append(r)

    rank, n_year = {}, {}
    for y, rs in by_year.items():
        rs.sort(key=lambda x: -float(x["eci"]))
        n_year[y] = len(rs)
        for i, r in enumerate(rs, 1):
            rank[(r["country_iso3_code"], y)] = i

    rows = []
    for r in src:
        c, y = r["country_iso3_code"], r["year"]
        rows.append({
            "country_iso3": c,
            "year": int(y),
            "export_value": r["export_value"],
            "import_value": r["import_value"],
            "eci": r["eci"],
            "eci_rank": rank.get((c, y), ""),
            # So nuoc duoc xep hang thay doi theo nam (211 nam 1995 -> 230 nam
            # 2024), nen "hang 70" khong doc duoc neu thieu mau so. Ai ve bieu
            # do thu hang theo thoi gian bat buoc phai dung cot nay.
            "eci_n": n_year.get(y, ""),
            "coi": r["coi"],
            "diversity": r["diversity"],
            # growth_proj la DU BAO cua Growth Lab, khong phai so do duoc, va
            # trong khoang 40% dong. Giu lai nhung dung tron vao chuoi lich su.
            "growth_proj": r["growth_proj"],
        })

    rows.sort(key=lambda x: (x["year"], x["country_iso3"]))
    write_csv(
        os.path.join(OUT, "country_year.csv"),
        ["country_iso3", "year", "export_value", "import_value",
         "eci", "eci_rank", "eci_n", "coi", "diversity", "growth_proj"],
        rows,
    )

    # Kiem dinh: ECI la chi so da chuan hoa - moi nam trung binh xap xi 0 va
    # do lech chuan xap xi 1. Doc lech cot hay mat dong la hai so nay troi ngay.
    worst_m = worst_s = 0.0
    for y, rs in by_year.items():
        e = [float(x["eci"]) for x in rs]
        m = sum(e) / len(e)
        s = (sum((v - m) ** 2 for v in e) / len(e)) ** 0.5
        worst_m, worst_s = max(worst_m, abs(m)), max(worst_s, abs(s - 1))
    good = worst_m < 0.15 and worst_s < 0.12
    log("  KIEM DINH - ECI chuan hoa: |trung binh| <= %.3f,"
        " |do lech chuan - 1| <= %.3f  %s"
        % (worst_m, worst_s, "DAT" if good else "KHONG DAT"))

    n_eci = sum(1 for r in rows if r["eci"] not in ("", "None"))
    n_gp = sum(1 for r in rows if r["growth_proj"] not in ("", "None"))
    log("  %d dong | %d co ECI | %d co du bao tang truong (%.0f%%)"
        % (len(rows), n_eci, n_gp, 100.0 * n_gp / len(rows)))

    # Bang de trich thang vao bao cao va slide.
    look = ["VNM", "THA", "MYS", "PHL", "IDN", "SGP"]
    idx = {(r["country_iso3"], r["year"]): r for r in rows}
    log("  ECI qua cac nam moc  (trong ngoac = thu hang / so nuoc duoc xep):")
    log("    %-5s%s" % ("", "".join("%-18d" % y for y in MILESTONE_YEARS)))
    for c in look:
        cells = []
        for y in MILESTONE_YEARS:
            r = idx.get((c, y))
            cells.append("%-18s" % (
                "%+.2f (#%s/%s)" % (float(r["eci"]), r["eci_rank"], r["eci_n"])
                if r and r["eci"] not in ("", "None") else "-"))
        log("    %-5s%s" % (c, "".join(cells)))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--threshold-share", type=float, default=THRESHOLD_SHARE,
                    help="Nguong loc canh, tinh bang ty le tren tong xuat"
                         " khau the gioi moi nam. Mac dinh %g (chot o T10)."
                         % THRESHOLD_SHARE)
    ap.add_argument("--focus-topk", type=int, default=FOCUS_TOPK,
                    help="So luong xuat/nhap lon nhat luon giu cho moi nuoc"
                         " trong tam. Mac dinh %d." % FOCUS_TOPK)
    args = ap.parse_args()

    log("Goc repo: %s" % ROOT)
    known = build_nodes()
    build_edges(known, args.threshold_share, args.focus_topk)
    build_tree()
    build_country_product()
    build_country_year()
    log("\nXong. File nam trong data/processed/ (da bi .gitignore loai tru).")


if __name__ == "__main__":
    main()

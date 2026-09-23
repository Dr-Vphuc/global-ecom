# -*- coding: utf-8 -*-
"""Sinh 3 file trung gian THẬT từ bộ Atlas theo đúng HỢP ĐỒNG DỮ LIỆU.

    data/atlas/location_country.csv  ->  data/processed/nodes.csv
    data/atlas/cc_year.csv           ->  data/processed/edges.csv
    data/atlas/product_hs92.csv      ->  data/processed/tree.csv

Chạy:
    python src/build_intermediate.py
    python src/build_intermediate.py --threshold 1e10

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
    DEFAULT_THRESHOLD,
    FOCUS_ISO3,
    NON_COUNTRY,
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
    log("\n[1/3] nodes.csv")
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
def build_edges(known_iso3, threshold):
    log("\n[2/3] edges.csv  (nguong tam: %.0f USD)" % threshold)
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
                    "export_value": repr(exp),
                    "import_value": repr(imp),
                    "log_value": "%.4f" % math.log10(exp),
                    "above_threshold": "TRUE" if exp >= threshold else "FALSE",
                }
            )

    rows.sort(key=lambda x: (x["year"], x["source_iso3"], x["target_iso3"]))
    write_csv(
        os.path.join(OUT, "edges.csv"),
        ["source_iso3", "target_iso3", "year", "export_value", "import_value",
         "log_value", "above_threshold"],
        rows,
    )

    log("  doc %d dong -> giu %d canh" % (n_total, len(rows)))
    log("  bo %d dong co export_value = 0 (khong phai canh)" % n_zero)
    if n_bad:
        log("  ! bo %d dong hong khong doc duoc so" % n_bad)
    if unknown:
        log("  ! %d ma nuoc khong co trong nodes.csv: %s"
            % (len(unknown), ", ".join(sorted(unknown))))
    log("  nam: %d–%d (%d nam)" % (min(years), max(years), len(years)))

    # Doi chieu voi con so nhom da do san va se phai bao ve truoc hoi dong.
    e2023 = [r for r in rows if r["year"] == 2023]
    n_focus = len({r["source_iso3"] for r in e2023} | {r["target_iso3"] for r in e2023})
    dens = len(e2023) / (n_focus * (n_focus - 1)) if n_focus > 1 else 0
    log("  KIEM CHUNG 2023: %d canh, %d nut, mat do %.3f  (file phan cong ghi: 25425 / 230 / 0.483)"
        % (len(e2023), n_focus, dens))
    return rows


# ---------------------------------------------------------------------------
# tree.csv
# ---------------------------------------------------------------------------
def build_tree():
    log("\n[3/3] tree.csv")
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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help="Nguong loc canh (USD). Mac dinh %.0e — chot lai o T10."
                         % DEFAULT_THRESHOLD)
    args = ap.parse_args()

    log("Goc repo: %s" % ROOT)
    known = build_nodes()
    build_edges(known, args.threshold)
    build_tree()
    log("\nXong. File nam trong data/processed/ (da bi .gitignore loai tru).")


if __name__ == "__main__":
    main()

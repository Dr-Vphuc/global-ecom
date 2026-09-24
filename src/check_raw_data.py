# -*- coding: utf-8 -*-
"""Kiểm tra toàn vẹn dữ liệu thô TRƯỚC khi chạy pipeline.

Chạy script này ngay sau mỗi lần tải lại dữ liệu từ Harvard Dataverse.
Nó bắt đúng loại lỗi đã từng xảy ra với repo này: file tải về bị cắt giữa chừng,
làm mất hoàn toàn các nước ở cuối thứ tự sắp xếp — trong đó có Hoa Kỳ.

    python src/check_raw_data.py

Thoát với mã 1 nếu phát hiện lỗi, để có thể gắn vào CI hoặc pre-commit.
Chỉ dùng thư viện chuẩn.
"""

import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "atlas")

problems = []


def log(msg):
    print(msg, flush=True)


def fail(msg):
    problems.append(msg)
    log("  [LOI] " + msg)


def ok(msg):
    log("  [OK ] " + msg)


def check_complete_last_line(path, n_fields):
    """File tai bi cat thuong ket thuc bang mot dong thieu truong.

    Doc theo dong chu khong nap ca file: cp_year_hs2.csv co 628k dong.
    """
    n_bad, first = 0, None
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for i, r in enumerate(csv.reader(fh), 1):
            if r and len(r) != n_fields:
                n_bad += 1
                if first is None:
                    first = (i, r)
    if n_bad:
        fail("%s: %d dong khong du %d truong. Dong dau tien: %d -> %r"
             % (os.path.basename(path), n_bad, n_fields, first[0], first[1]))
        fail("  => Rat co the FILE BI CAT khi tai. Phai tai lai.")
    else:
        ok("%s: moi dong du %d truong" % (os.path.basename(path), n_fields))


def main():
    log("Kiem tra du lieu tho trong %s\n" % os.path.relpath(RAW, ROOT))

    loc_path = os.path.join(RAW, "location_country.csv")
    cc_path = os.path.join(RAW, "cc_year.csv")
    prod_path = os.path.join(RAW, "product_hs92.csv")
    cp_path = os.path.join(RAW, "cp_year_hs2.csv")
    cy_path = os.path.join(RAW, "hs92_country_year.csv")

    for p in (loc_path, cc_path, prod_path, cp_path, cy_path):
        if not os.path.exists(p):
            fail("THIEU FILE: %s" % os.path.relpath(p, ROOT))
    if problems:
        log("\nDung lai: thieu file dau vao.")
        return 1

    # --- 1. File co bi cat khong ---
    log("1. Tinh toan ven cua file")
    check_complete_last_line(cc_path, 7)

    # --- 2. Moi nuoc deu phai xuat hien ca hai chieu ---
    log("\n2. Moi nuoc phai xuat hien ca lam NGUON lan lam DOI TAC")
    loc = list(csv.DictReader(open(loc_path, encoding="utf-8-sig")))
    all_iso = {r["country_iso3_code"] for r in loc}

    src_iso, tgt_iso = set(), set()
    with open(cc_path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r.get("year"):
                continue
            src_iso.add(r["country_iso3_code"])
            tgt_iso.add(r["partner_iso3_code"])

    only_target = sorted(tgt_iso - src_iso)
    if only_target:
        fail("%d nuoc chi xuat hien lam DOI TAC, khong bao gio lam NGUON:"
             % len(only_target))
        fail("  " + ", ".join(only_target))
        fail("  => Xuat khau cua cac nuoc nay BI MAT HOAN TOAN.")
    else:
        ok("moi nuoc deu xuat hien o ca hai chieu")

    never = sorted(all_iso - src_iso - tgt_iso)
    if never:
        log("  [i  ] %d ma co trong location_country nhung khong co luong nao: %s"
            % (len(never), ", ".join(never)))

    # --- 3. Cac nuoc xuat khau lon phai co mat ---
    log("\n3. Cac nuoc xuat khau lon nhat the gioi phai co mat lam NGUON")
    must_export = ["CHN", "USA", "DEU", "NLD", "JPN", "KOR", "ITA", "FRA",
                   "HKG", "MEX", "CAN", "GBR", "SGP", "ARE", "IND", "VNM"]
    absent = [c for c in must_export if c not in src_iso]
    if absent:
        fail("cac nuoc sau KHONG co dong xuat khau nao: %s" % ", ".join(absent))
    else:
        ok("du mat 16 nuoc xuat khau lon nhat")

    # --- 4. Tong kim ngach co hop ly khong ---
    log("\n4. Tong kim ngach nam gan nhat so voi thuc te")
    tot = {}
    with open(cc_path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r.get("year"):
                continue
            try:
                y, v = int(r["year"]), float(r["export_value"] or 0)
            except (ValueError, TypeError):
                continue
            tot[y] = tot.get(y, 0.0) + v
    if tot:
        y = max(tot)
        tn = tot[y] / 1e12
        log("  tong xuat khau %d trong file: %.2f nghin ty USD" % (y, tn))
        # Xuat khau hang hoa toan cau khoang 23-25 nghin ty USD nhung nam gan day.
        if y >= 2020 and tn < 20:
            fail("thap bat thuong. Xuat khau hang hoa toan cau ~23-24 nghin ty USD."
                 " Thieu khoang %.1f nghin ty => nghi mat du lieu." % (23 - tn))
        else:
            ok("nam trong khoang hop ly")

    # --- 5. Cay san pham ---
    log("\n5. Cay san pham HS92")
    prod = list(csv.DictReader(open(prod_path, encoding="utf-8-sig")))
    levels = {}
    for r in prod:
        lv = int(r["product_level"])
        levels[lv] = levels.get(lv, 0) + 1
    expect = {1: 10, 2: 97, 4: 1243, 6: 5040}
    if levels == expect:
        ok("du 4 tang %s" % expect)
    else:
        fail("so nut theo tang %s khac mong doi %s" % (levels, expect))
    ids = {r["product_id"] for r in prod}
    orph = [r["product_id"] for r in prod
            if r["product_parent_id"] and r["product_parent_id"] not in ids]
    if orph:
        fail("%d nut mo coi" % len(orph))
    else:
        ok("khong co nut mo coi")

    # --- 6. File nuoc - san pham, va doi chieu cheo hai file ---
    log("\n6. File nuoc - san pham HS2")
    check_complete_last_line(cp_path, 11)

    codes, tot_cp = set(), {}
    with open(cp_path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r.get("year"):
                continue
            codes.add(r["product_hs92_code"])
            try:
                y, v = int(r["year"]), float(r["export_value"] or 0)
            except (ValueError, TypeError):
                continue
            tot_cp[y] = tot_cp.get(y, 0.0) + v
    if len(codes) == 97:
        ok("du 97 ma HS2")
    else:
        fail("chi co %d ma HS2, mong doi 97" % len(codes))

    # --- 7. File nuoc - nam: ECI, COI, diversity ---
    log("\n7. File nuoc - nam (chi so phuc tap kinh te)")
    check_complete_last_line(cy_path, 9)

    cy, tot_cy = [], {}
    with open(cy_path, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if not r.get("year"):
                continue
            cy.append(r)
            try:
                y, v = int(r["year"]), float(r["export_value"] or 0)
            except (ValueError, TypeError):
                continue
            tot_cy[y] = tot_cy.get(y, 0.0) + v

    # ECI la chi so DA CHUAN HOA: moi nam, trung binh xap xi 0 va do lech chuan
    # xap xi 1. Day la tinh chat cua cach tinh chu khong phai trung hop, nen
    # dung duoc lam phep thu: doc lech cot hay mat dong la hai so nay troi ngay.
    worst_m = worst_s = 0.0
    for y in sorted({r["year"] for r in cy}):
        e = [float(r["eci"]) for r in cy
             if r["year"] == y and r["eci"] not in ("", "None")]
        if len(e) < 50:
            continue
        m = sum(e) / len(e)
        s = (sum((x - m) ** 2 for x in e) / len(e)) ** 0.5
        worst_m, worst_s = max(worst_m, abs(m)), max(worst_s, abs(s - 1))
    if worst_m < 0.15 and worst_s < 0.12:
        ok("ECI dung chuan hoa (|trung binh| <= %.3f, |do lech chuan - 1| <= %.3f)"
           % (worst_m, worst_s))
    else:
        fail("ECI sai chuan hoa: |trung binh| %.3f, |do lech chuan - 1| %.3f"
             " => nghi doc lech cot" % (worst_m, worst_s))

    no_eci = sorted({r["country_iso3_code"] for r in cy
                     if r["eci"] in ("", "None")})
    if no_eci:
        log("  [i  ] %d ma khong co ECI nam nao: %s"
            % (len(no_eci), ", ".join(no_eci)))
    thieu = sorted(all_iso - {r["country_iso3_code"] for r in cy})
    if thieu:
        log("  [i  ] %d ma co trong location_country nhung vang mat o day: %s"
            % (len(thieu), ", ".join(thieu)))

    # --- 8. Doi chieu cheo ba file ---
    # Ba file do cung mot nen thuong mai tu ba goc khac nhau: cc_year theo cap
    # nuoc, cp_year_hs2 theo nuoc va san pham, hs92_country_year theo nuoc.
    # Tong xuat khau toan the gioi phai trung nhau o ca ba. Mot file bi cat khi
    # tai se lam tut rieng cot cua no, va phep nay chi ra ngay file nao.
    log("\n8. Doi chieu cheo ba file (tong xuat khau the gioi)")
    chung = set(tot) & set(tot_cp) & set(tot_cy)
    if chung:
        y = max(chung)
        v = [("cc_year.csv", tot[y]), ("cp_year_hs2.csv", tot_cp[y]),
             ("hs92_country_year.csv", tot_cy[y])]
        for ten, gt in v:
            log("  nam %d  %-22s %.4f nghin ty" % (y, ten, gt / 1e12))
        hi = max(gt for _, gt in v)
        lo = min(gt for _, gt in v)
        lech = (hi - lo) / hi if hi else 1.0
        if lech < 0.01:
            ok("ca ba file khop nhau (chenh lech toi da %.3f%%)" % (lech * 100))
        else:
            fail("ba file lech toi %.1f%% => co file thieu du lieu"
                 % (lech * 100))
    else:
        fail("ba file khong co nam nao chung")

    # --- Ket luan ---
    log("\n" + "=" * 60)
    if problems:
        log("KHONG DAT — %d van de. Khong duoc chay pipeline tren du lieu nay." % len(problems))
        return 1
    log("DAT — du lieu tho dung de chay pipeline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

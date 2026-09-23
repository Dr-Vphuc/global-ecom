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

    for p in (loc_path, cc_path, prod_path, cp_path):
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

    # Doi chieu cheo hai file: cc_year do thuong mai theo cap nuoc, cp_year_hs2
    # do theo nuoc va san pham. Hai goc nhin khac nhau nhung tong xuat khau
    # toan the gioi phai trung nhau. Lech lon = mot trong hai file thieu dong.
    log("\n7. Doi chieu cheo cc_year.csv voi cp_year_hs2.csv")
    chung = set(tot) & set(tot_cp)
    if chung:
        y = max(chung)
        a, b = tot[y], tot_cp[y]
        lech = abs(a - b) / a if a else 1.0
        log("  nam %d: cc_year %.2f nghin ty | cp_year_hs2 %.2f nghin ty"
            % (y, a / 1e12, b / 1e12))
        if lech < 0.01:
            ok("hai file khop nhau (lech %.3f%%)" % (lech * 100))
        else:
            fail("hai file lech %.1f%% => mot trong hai thieu du lieu"
                 % (lech * 100))
    else:
        fail("hai file khong co nam nao chung")

    # --- Ket luan ---
    log("\n" + "=" * 60)
    if problems:
        log("KHONG DAT — %d van de. Khong duoc chay pipeline tren du lieu nay." % len(problems))
        return 1
    log("DAT — du lieu tho dung de chay pipeline.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

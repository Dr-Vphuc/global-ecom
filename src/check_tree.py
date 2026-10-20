"""Kiểm tra chất lượng cây phân cấp sản phẩm HS92 (T11).

Cây HS92 là xương sống của mọi biểu đồ phân cấp trong đồ án — treemap (T12),
sunburst (T13), small multiples so sánh nước (T14). Nếu cây hỏng thì diện tích
các ô sai mà không có cảnh báo nào: một nút mồ côi bị rụng khỏi tổng, một cạnh
cha-con sai làm giá trị nhảy sang nhầm ngành. Cả hai lỗi đó đều KHÔNG làm chương
trình báo lỗi, chúng chỉ làm con số sai.

Script chạy 10 phép kiểm, mỗi phép in ra ĐẠT hoặc LỖI kèm số đo thật. Thoát với
mã khác 0 nếu có bất kỳ phép nào hỏng, để dùng được trong CI sau này.

    python src/check_tree.py

Chỉ dùng thư viện chuẩn — chạy được ngay, không cần cài gì.
"""

from __future__ import annotations

import csv
import os
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TREE_CSV = os.path.join(ROOT, "data", "atlas", "product_hs92.csv")
CP_CSV = os.path.join(ROOT, "data", "atlas", "cp_year_hs2.csv")

# Số nút từng tầng theo công bố của Harvard Growth Lab cho bộ HS92.
# Đây là con số nhóm đã nêu trong hợp đồng dữ liệu và sẽ phải bảo vệ khi vấn đáp.
EXPECTED_LEVELS = {1: 10, 2: 97, 4: 1243, 6: 5040}
EXPECTED_TOTAL = sum(EXPECTED_LEVELS.values())

# Tầng này nối lên tầng nào. HS92 nhảy 1 -> 2 -> 4 -> 6 chứ không liên tiếp,
# vì số tầng đặt theo ĐỘ DÀI MÃ HS (2, 4, 6 chữ số), riêng tầng 1 là nhóm ngành
# do Growth Lab tự gộp, không thuộc chuẩn HS.
PARENT_LEVEL = {2: 1, 4: 2, 6: 4}

_fails = 0
_warns = 0

# Tang 1 va 2 la hai tang T12-T14 thuc su ve. Theo doi rieng de ket luan
# noi dung pham vi anh huong thay vi phan xu chung chung.
_level12_ok = True


def ok(msg, detail=""):
    print("  DAT   %-52s %s" % (msg, detail))


def fail(msg, detail=""):
    global _fails
    _fails += 1
    print("  LOI   %-52s %s" % (msg, detail))


def warn(msg, detail=""):
    global _warns
    _warns += 1
    print("  LUU Y %-52s %s" % (msg, detail))


def load_tree():
    """Doc cay. Tra ve (nodes, dup_ids).

    Phai dem trung product_id NGAY LUC DOC: nap vao dict xong thi ban ghi sau
    da de len ban ghi truoc, khong con dau vet nao de kiem.
    """
    if not os.path.exists(TREE_CSV):
        sys.exit("Thieu %s" % TREE_CSV)
    nodes = {}
    seen = Counter()
    with open(TREE_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pid = int(r["product_id"])
            seen[pid] += 1
            nodes[pid] = {
                "level": int(r["product_level"]),
                "parent": int(r["product_parent_id"]) if r["product_parent_id"] else None,
                "code": r["product_hs92_code"],
                "name": r["product_name"],
            }
    dup_ids = [p for p, k in seen.items() if k > 1]
    return nodes, dup_ids


def check_counts(nodes):
    global _level12_ok
    print("\n1. So nut tung tang")
    got = Counter(n["level"] for n in nodes.values())
    for lv in sorted(EXPECTED_LEVELS):
        want = EXPECTED_LEVELS[lv]
        have = got.get(lv, 0)
        (ok if have == want else fail)(
            "tang %d" % lv, "%d nut (mong doi %d)" % (have, want))
        if have != want and lv in (1, 2):
            _level12_ok = False
    extra = set(got) - set(EXPECTED_LEVELS)
    if extra:
        fail("co tang la ngoai 1/2/4/6", str(sorted(extra)))
    else:
        ok("khong co tang la", "chi 1, 2, 4, 6")
    (ok if len(nodes) == EXPECTED_TOTAL else fail)(
        "tong so nut", "%d (mong doi %d)" % (len(nodes), EXPECTED_TOTAL))


def check_roots(nodes):
    print("\n2. Nut goc")
    roots = [p for p, n in nodes.items() if n["parent"] is None]
    (ok if len(roots) == EXPECTED_LEVELS[1] else fail)(
        "so nut khong co cha", "%d (mong doi %d)" % (len(roots), EXPECTED_LEVELS[1]))
    bad = [p for p in roots if nodes[p]["level"] != 1]
    (ok if not bad else fail)("moi nut goc deu o tang 1", "" if not bad else str(bad[:5]))
    lv1_with_parent = [p for p, n in nodes.items() if n["level"] == 1 and n["parent"] is not None]
    (ok if not lv1_with_parent else fail)(
        "khong nut tang 1 nao co cha", "" if not lv1_with_parent else str(lv1_with_parent[:5]))


def check_parents(nodes):
    global _level12_ok
    print("\n3. Tinh hop le cua parent_id")
    dangling = [(p, n["parent"]) for p, n in nodes.items()
                if n["parent"] is not None and n["parent"] not in nodes]
    (ok if not dangling else fail)(
        "moi parent_id tro toi nut co that", "" if not dangling else "%d nut tro vao hu vo" % len(dangling))

    selfref = [p for p, n in nodes.items() if n["parent"] == p]
    (ok if not selfref else fail)("khong nut nao tu lam cha minh", "" if not selfref else str(selfref[:5]))

    wrong = []
    for p, n in nodes.items():
        if n["parent"] is None:
            continue
        want = PARENT_LEVEL.get(n["level"])
        got = nodes[n["parent"]]["level"] if n["parent"] in nodes else None
        if want is not None and got != want:
            wrong.append((p, n["level"], got, want))
    (ok if not wrong else fail)(
        "cha nam dung tang ngay tren",
        "" if not wrong else "%d nut sai, vd %s" % (len(wrong), wrong[:3]))
    if any(lv in (1, 2) for _, lv, _, _ in wrong):
        _level12_ok = False


def check_reachable(nodes):
    print("\n4. Khong mo coi, khong chu trinh")
    orphan, cyclic, depth_bad = [], [], []
    for p in nodes:
        seen = set()
        cur = p
        steps = 0
        while cur is not None:
            if cur in seen:
                cyclic.append(p)
                break
            seen.add(cur)
            nxt = nodes[cur]["parent"]
            if nxt is not None and nxt not in nodes:
                orphan.append(p)
                break
            cur = nxt
            steps += 1
            if steps > 10:
                depth_bad.append(p)
                break
    (ok if not orphan else fail)(
        "moi nut leo nguoc ve duoc goc", "" if not orphan else "%d nut mo coi" % len(orphan))
    (ok if not cyclic else fail)(
        "khong co chu trinh", "" if not cyclic else "%d nut nam trong chu trinh" % len(cyclic))
    (ok if not depth_bad else fail)(
        "do sau khong vuot qua 10", "" if not depth_bad else "%d nut" % len(depth_bad))


def check_codes(nodes, dup_ids):
    print("\n5. Ma HS92")
    (ok if not dup_ids else fail)(
        "product_id khong trung",
        "" if not dup_ids else "%d id trung: %s" % (len(dup_ids), dup_ids[:5]))

    for lv in sorted(EXPECTED_LEVELS):
        codes = [n["code"] for n in nodes.values() if n["level"] == lv]
        dup = [c for c, k in Counter(codes).items() if k > 1]
        (ok if not dup else fail)(
            "ma HS khong trung trong tang %d" % lv,
            "" if not dup else "%d ma trung: %s" % (len(dup), dup[:5]))

    # Do dai ma phai khop tang: tang 2 -> 2 ky tu, tang 4 -> 4, tang 6 -> 6.
    # Tang 1 la nhom nganh tu dat nen khong rang buoc.
    for lv in (2, 4, 6):
        bad = [(n["code"], lv) for n in nodes.values()
               if n["level"] == lv and len(n["code"]) != lv]
        (ok if not bad else warn)(
            "do dai ma tang %d dung %d ky tu" % (lv, lv),
            "" if not bad else "%d ma lech, vd %s" % (len(bad), bad[:3]))

    # Ma con phai bat dau bang ma cha — tinh chat long nhau cua he HS.
    # Chi ap cho tang 4 va 6 (tang 2 co cha la nhom nganh, khong theo ma HS).
    #
    # Ma toan chu X la cho giu cho cua Atlas ("Trade data discrepancies" —
    # phan chenh lech thong ke khong quy duoc ve nhom hang nao), khong phai ma
    # HS that nen khong chiu rang buoc tien to. Tach rieng de khong bao dong gia.
    bad_prefix, placeholder = [], []
    for p, n in nodes.items():
        if n["level"] in (4, 6) and n["parent"] in nodes:
            pc = nodes[n["parent"]]["code"]
            if not n["code"].startswith(pc):
                (placeholder if set(n["code"]) == {"X"} else bad_prefix).append(
                    (n["code"], pc, n["name"][:40]))
    (ok if not bad_prefix else fail)(
        "ma con noi dai ma cha",
        "" if not bad_prefix else "%d nut sai: %s" % (
            len(bad_prefix), ["%s duoi %s" % (c, pc) for c, pc, _ in bad_prefix]))
    if placeholder:
        warn("ma giu cho cua Atlas (khong phai loi)",
             ", ".join("%s duoi %s" % (c, pc) for c, pc, _ in placeholder))


def check_leaves(nodes):
    print("\n6. Nut la")
    children = defaultdict(list)
    for p, n in nodes.items():
        if n["parent"] is not None:
            children[n["parent"]].append(p)

    leaves = [p for p in nodes if not children[p]]
    non_leaf_at_6 = [p for p in nodes if nodes[p]["level"] == 6 and children[p]]
    (ok if not non_leaf_at_6 else fail)(
        "khong nut tang 6 nao co con", "" if not non_leaf_at_6 else "%d nut" % len(non_leaf_at_6))

    leaves_above_6 = [p for p in leaves if nodes[p]["level"] != 6]
    if leaves_above_6:
        by_lv = Counter(nodes[p]["level"] for p in leaves_above_6)
        warn("co nut la nam tren tang 6",
             "%d nut, theo tang: %s" % (len(leaves_above_6), dict(sorted(by_lv.items()))))
    else:
        ok("moi nut la deu o tang 6", "%d la" % len(leaves))

    childless_internal = [p for p in nodes if nodes[p]["level"] in (1, 2, 4) and not children[p]]
    if childless_internal:
        warn("nut trung gian khong co con",
             "%d nut, vd ma %s" % (len(childless_internal),
                                   [nodes[p]["code"] for p in childless_internal[:3]]))
    else:
        ok("moi nut trung gian deu co con", "")


def check_against_exports(nodes):
    print("\n7. Doi chieu voi du lieu xuat khau")
    if not os.path.exists(CP_CSV):
        warn("bo qua — thieu cp_year_hs2.csv",
             "chay: python src/download_atlas.py --only cp_year_hs2.csv")
        return
    used = set()
    with open(CP_CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            used.add(int(r["product_id"]))
    missing = used - set(nodes)
    (ok if not missing else fail)(
        "moi product_id trong du lieu co trong cay",
        "" if not missing else "%d id khong tim thay: %s" % (len(missing), sorted(missing)[:5]))

    lv2 = {p for p, n in nodes.items() if n["level"] == 2}
    not_lv2 = used - lv2
    (ok if not not_lv2 else warn)(
        "du lieu HS2 chi dung nut tang 2",
        "" if not not_lv2 else "%d id khong o tang 2" % len(not_lv2))

    unused = lv2 - used
    if unused:
        warn("nut tang 2 khong xuat hien trong du lieu",
             "%d / %d nut" % (len(unused), len(lv2)))
    else:
        ok("ca %d nut tang 2 deu co mat trong du lieu" % len(lv2), "")


def self_test():
    """Kiem tra chinh bo kiem tra: co lam cay hong roi xem no co bat duoc khong.

    Ly do co ham nay: co _level12_ok tung bi gan ben trong ham ma thieu khai bao
    `global`, nen Python tao bien cuc bo va co o module LUON LUON True. Hau qua
    la cay hong o tang 1-2 van duoc bao "toan ven, T12-T14 dung duoc" — mot cong
    cu kiem tra bao dam sai thi te hon la khong co cong cu nao. Ham nay chot lai
    hanh vi do de khong tai pham.
    """
    global _fails, _warns, _level12_ok
    import io
    import contextlib

    nodes, _ = load_tree()
    cases = []

    # Ca 1: cay that phai cho tang 1-2 toan ven.
    cases.append(("cay that", dict(nodes), True))

    # Ca 2: xoa mot nganh cap 1 -> so nut tang 1 sai -> co phai tat.
    broken_lv1 = dict(nodes)
    first_lv1 = next(p for p, n in broken_lv1.items() if n["level"] == 1)
    del broken_lv1[first_lv1]
    cases.append(("xoa 1 nut tang 1", broken_lv1, False))

    # Ca 3: xoa mot nhom cap 2 -> so nut tang 2 sai -> co phai tat.
    broken_lv2 = dict(nodes)
    first_lv2 = next(p for p, n in broken_lv2.items() if n["level"] == 2)
    del broken_lv2[first_lv2]
    cases.append(("xoa 1 nut tang 2", broken_lv2, False))

    # Ca 4: hong o tang 6 -> KHONG duoc tat co, vi T12-T14 khong ve toi tang do.
    broken_lv6 = dict(nodes)
    first_lv6 = next(p for p, n in broken_lv6.items() if n["level"] == 6)
    del broken_lv6[first_lv6]
    cases.append(("xoa 1 nut tang 6", broken_lv6, True))

    print("TU KIEM TRA BO KIEM TRA")
    print("-" * 78)
    bad = 0
    for name, tree, want in cases:
        _fails, _warns, _level12_ok = 0, 0, True
        with contextlib.redirect_stdout(io.StringIO()):
            check_counts(tree)
            check_parents(tree)
        got = _level12_ok
        mark = "DAT " if got == want else "LOI "
        if got != want:
            bad += 1
        print("  %s %-22s co tang1-2 = %-5s (mong doi %s)" % (mark, name, got, want))

    _fails, _warns, _level12_ok = 0, 0, True
    print("-" * 78)
    print("KET QUA TU KIEM TRA: %s" % ("DAT" if not bad else "%d ca SAI" % bad))
    return 1 if bad else 0


def main():
    if "--self-test" in sys.argv:
        return self_test()

    print("=" * 78)
    print("KIEM TRA CHAT LUONG CAY HS92  (T11)")
    print("Nguon: data/atlas/product_hs92.csv")
    print("=" * 78)

    nodes, dup_ids = load_tree()
    check_counts(nodes)
    check_roots(nodes)
    check_parents(nodes)
    check_reachable(nodes)
    check_codes(nodes, dup_ids)
    check_leaves(nodes)
    check_against_exports(nodes)

    print("\n" + "=" * 78)
    if _fails:
        print("KET QUA: %d LOI, %d luu y." % (_fails, _warns))
    elif _warns:
        print("KET QUA: DAT, kem %d luu y can doc qua." % _warns)
    else:
        print("KET QUA: DAT toan bo.")

    # Ket luan phai noi dung PHAM VI anh huong, khong phan xu chung chung.
    # T12-T14 chi ve toi tang 2, nen loi o tang 4/6 khong lam sai bieu do —
    # nhung van phai ghi lai vi no se sai neu sau nay ai do khoan sau hon.
    if _level12_ok:
        print("Tang 1 va tang 2 toan ven -> T12, T13, T14 dung duoc.")
        if _fails:
            print("Cac loi o tren deu nam tu tang 4 tro xuong: chua anh huong bieu do")
            print("hien tai, nhung phai ghi vao phan phuong phap luan (T25).")
    else:
        print("Tang 1 hoac tang 2 CO LOI -> KHONG dung cho T12-T14 cho toi khi sua.")
    print("=" * 78)
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())

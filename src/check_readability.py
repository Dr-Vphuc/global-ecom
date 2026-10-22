# -*- coding: utf-8 -*-
"""Kiểm khả năng đọc của toàn bộ hình: cỡ chữ, khung, tương phản, mù màu (T24).

`check_palette.py` đã lo phần bảng màu — hai màu bất kỳ có đủ khác nhau không,
kể cả với người mù màu. Nhưng một hình vẫn có thể không đọc được dù bảng màu
đạt: chữ in ra quá nhỏ, chữ đè lên nền cùng độ sáng, hay script xuất PNG bằng
khung pixel nên cỡ chữ khai báo không phải cỡ chữ in ra (lỗi **B16**).

Script này kiểm bốn thứ đó, trên SOURCE chứ không trên ảnh — đọc ngược cỡ chữ
từ một file PNG là bất khả, mà đọc từ code thì chắc chắn và chạy lại được.

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/check_readability.py

Trả về mã thoát khác 0 nếu có mục BẮT BUỘC không đạt, để cắm được vào CI.
"""

from __future__ import print_function

import glob
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_data as R  # noqa: E402
from check_palette import contrast, luminance, simulate, to_lab, ciede2000  # noqa: E402

FLOOR_PT = 7.0           # sàn cỡ chữ của style-guide §7
MIN_CONTRAST = 4.5       # chữ đè nền màu, tiêu chí WCAG AA cho chữ nhỏ
NEEDS_BORDER = 3.0       # dưới mức này ô màu phải có viền trắng mới tách nền
MIN_DE_CVD = 10.0

SRC = os.path.dirname(os.path.abspath(__file__))
SKIP = {"check_readability.py", "check_palette.py", "reference_data.py"}


def _scripts():
    out = []
    for p in sorted(glob.glob(os.path.join(SRC, "make_*.py"))):
        if os.path.basename(p) not in SKIP:
            out.append(p)
    return out


def kiem_co_chu():
    """Mọi cỡ chữ khai báo phải ≥ sàn. Bắt cả FONT_SIZES lẫn số viết thẳng."""
    print("\n1. CỠ CHỮ KHAI BÁO (sàn %s pt)" % R.fmt_vn(FLOOR_PT, 0))
    loi = []
    for k, v in sorted(R.FONT_SIZES.items()):
        dat = v >= FLOOR_PT
        print("   %-12s %4s pt  %s" % (k, R.fmt_vn(v, 0),
                                       "đạt" if dat else "KHÔNG ĐẠT"))
        if not dat:
            loi.append("FONT_SIZES[%r] = %s" % (k, v))

    pat = re.compile(r"size\s*=\s*([0-9]+(?:\.[0-9]+)?)")
    for p in _scripts():
        txt = io.open(p, encoding="utf-8").read()
        for m in pat.finditer(txt):
            val = float(m.group(1))
            # marker.size là ĐƯỜNG KÍNH chấm, không phải cỡ chữ — bỏ qua.
            truoc = txt[max(0, m.start() - 90):m.start()]
            if "marker" in truoc.split("\n")[-1] or "Marker" in truoc[-40:]:
                continue
            if val < FLOOR_PT:
                dong = txt[:m.start()].count("\n") + 1
                loi.append("%s:%d  size=%s" % (os.path.basename(p), dong, val))
    if loi:
        print("   Chỗ dưới sàn:")
        for x in loi:
            print("     - %s" % x)
    else:
        print("   Không chỗ nào khai báo dưới sàn.")
    return loi


def kiem_khung():
    """Script nào còn xuất PNG bằng khung pixel thì cỡ chữ in ra sẽ sai (B16)."""
    print("\n2. KHUNG XUẤT PNG (phải là khung point — B16)")
    loi = []
    for p in _scripts():
        txt = io.open(p, encoding="utf-8").read()
        if "write_image" not in txt and "xuat_png" not in txt:
            continue
        ten = os.path.basename(p)
        if "R.xuat_png" in txt:
            print("   %-28s dùng R.xuat_png" % ten)
            continue
        if re.search(r"write_image\([^)]*FIG_DPI_SCREEN", txt, re.S):
            print("   %-28s KHUNG PIXEL — chữ in ra nhỏ hơn %s lần"
                  % (ten, R.fmt_vn(R.PX_PER_PT_CU, 2)))
            loi.append(ten)
        elif re.search(r"write_image\([^)]*CANVAS_PT", txt, re.S):
            print("   %-28s khung point tự đặt" % ten)
        else:
            print("   %-28s không rõ khung — xem lại tay" % ten)
            loi.append(ten)
    return loi


def kiem_tuong_phan():
    """Chữ đặt trên ô màu ngành phải đủ tương phản để đọc."""
    print("\n3. CHỮ TRÊN Ô MÀU NGÀNH (ngưỡng %s:1)" % R.fmt_vn(MIN_CONTRAST, 1))
    loi = []
    for sid in sorted(R.SECTOR_PALETTE):
        fill = R.SECTOR_PALETTE[sid]
        text = R.SECTOR_TEXT_ON_FILL.get(sid, "#000000")
        c = contrast(text, fill)
        dat = c >= MIN_CONTRAST
        print("   %-26s %s trên %s  %5s:1  %s"
              % (R.SECTOR_NAME_VI.get(sid, sid)[:26], text, fill,
                 R.fmt_vn(c, 2), "đạt" if dat else "KHÔNG ĐẠT"))
        if not dat:
            loi.append("ngành %s: %s trên %s = %.2f:1"
                       % (sid, text, fill, c))
    return loi


def kiem_vien():
    """Ô màu quá nhạt so với nền trắng thì bắt buộc có viền, không thì mất mép."""
    print("\n4. Ô MÀU NHẠT CẦN VIỀN TRẮNG (ngưỡng %s:1 so với nền trắng)"
          % R.fmt_vn(NEEDS_BORDER, 1))
    can = []
    for sid in sorted(R.SECTOR_PALETTE):
        fill = R.SECTOR_PALETTE[sid]
        c = contrast(fill, "#FFFFFF")
        if c < NEEDS_BORDER:
            can.append(R.SECTOR_NAME_VI.get(sid, sid))
            print("   %-26s %s  %5s:1  → phải có viền"
                  % (R.SECTOR_NAME_VI.get(sid, sid)[:26], fill, R.fmt_vn(c, 2)))
    print("   %s / %s ngành cần viền. Đây là nhắc việc, không phải lỗi."
          % (R.fmt_vn(len(can), 0), R.fmt_vn(len(R.SECTOR_PALETTE), 0)))
    return []


def kiem_mu_mau():
    """Hai bảng màu đang dùng, kiểm chéo với ba dạng mù màu."""
    print("\n5. MÙ MÀU — cặp gần nhau nhất trong mỗi bảng (sàn ΔE %s)"
          % R.fmt_vn(MIN_DE_CVD, 0))
    loi = []
    bang = [("ngành hàng", list(R.SECTOR_PALETTE.values())),
            ("cụm Louvain", list(R.COMMUNITY_PALETTE.values()))]
    for ten, cols in bang:
        for kind in ("normal", "protan", "deutan", "tritan"):
            sim = cols if kind == "normal" else [simulate(c, kind) for c in cols]
            labs = [to_lab(c) for c in sim]
            worst = None
            for i in range(len(labs)):
                for j in range(i + 1, len(labs)):
                    d = ciede2000(labs[i], labs[j])
                    if d == d and (worst is None or d < worst):
                        worst = d
            nguong = 15.0 if kind == "normal" else MIN_DE_CVD
            dat = worst is not None and worst >= nguong
            print("   %-14s %-8s ΔE nhỏ nhất %6s  %s"
                  % (ten, kind, R.fmt_vn(worst or 0, 1),
                     "đạt" if dat else "KHÔNG ĐẠT"))
            if not dat:
                loi.append("%s / %s: ΔE %.1f < %.0f" % (ten, kind, worst or 0,
                                                        nguong))
    return loi


def main():
    print("=" * 70)
    print("KIỂM KHẢ NĂNG ĐỌC — T24")
    print("=" * 70)
    print("Kiểm trên mã nguồn của %s script dựng hình."
          % R.fmt_vn(len(_scripts()), 0))

    loi = []
    loi += kiem_co_chu()
    loi += kiem_khung()
    loi += kiem_tuong_phan()
    loi += kiem_vien()
    loi += kiem_mu_mau()

    print("\n" + "=" * 70)
    if loi:
        print("KHÔNG ĐẠT — %s mục phải sửa:" % R.fmt_vn(len(loi), 0))
        for x in loi:
            print("  - %s" % x)
        return 1
    print("ĐẠT — cỡ chữ, khung, tương phản và mù màu đều qua.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

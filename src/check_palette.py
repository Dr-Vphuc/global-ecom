# -*- coding: utf-8 -*-
"""T04 — kiểm định bảng màu 10 ngành cấp 1 HS92.

Không nhận xét cảm tính "nhìn phân biệt được". Đo ba thứ:

1. **Tương phản WCAG** — tỷ lệ tương phản của từng màu với nền trắng và nền
   đen, để biết dùng chữ màu gì đè lên, và màu có đủ nổi khi vẽ thành đường
   mảnh hay không.
2. **Mô phỏng mù màu** — ma trận Machado, Oliveira & Fernandes (2009) cho ba
   dạng: protan (khó thấy đỏ), deutan (khó thấy lục), tritan (khó thấy lam).
   Ma trận nhân trên RGB tuyến tính, không nhân trên giá trị sRGB.
3. **Khoảng cách màu CIEDE2000** — ΔE giữa từng cặp trong 45 cặp, đo ở thị
   giác bình thường và ở cả ba dạng mù màu. ΔE ≈ 1 là ngưỡng mắt người vừa
   nhận ra khác biệt; với ô màu cạnh nhau trong chú giải thì cần lớn hơn
   nhiều.

Chỉ dùng thư viện chuẩn. Chạy: python src/check_palette.py
Thoát mã 1 nếu có tiêu chí không đạt, để dùng được trong kiểm tra tự động.
"""
from __future__ import print_function

import math
import sys

try:
    from reference_data import SECTOR_NAME_VI, SECTOR_PALETTE
except ImportError:  # chạy từ thư mục gốc
    sys.path.insert(0, 'src')
    from reference_data import SECTOR_NAME_VI, SECTOR_PALETTE


# --- ngưỡng đã chốt, xem docs/style-guide.md mục "Vì sao các ngưỡng này" ---
MIN_DE_NORMAL = 15.0     # ΔE2000 nhỏ nhất giữa hai màu bất kỳ, mắt thường
MIN_DE_CVD = 10.0        # ΔE2000 nhỏ nhất khi mô phỏng mù màu
MIN_CONTRAST_TEXT = 4.5  # chữ đè lên ô màu — đây là tiêu chí BẮT BUỘC
NEEDS_BORDER = 3.0       # dưới mức này, ô màu phải có viền trắng mới tách khỏi nền


# --- Machado, Oliveira & Fernandes 2009, mức nặng nhất (severity 1.0) -------
CVD_MATRIX = {
    'protan': ((0.152286, 1.052583, -0.204868),
               (0.114503, 0.786281, 0.099216),
               (-0.003882, -0.048116, 1.051998)),
    'deutan': ((0.367322, 0.860646, -0.227968),
               (0.280085, 0.672501, 0.047413),
               (-0.011820, 0.042940, 0.968881)),
    'tritan': ((1.255528, -0.076749, -0.178779),
               (-0.078411, 0.930809, 0.147602),
               (0.004733, 0.691367, 0.303900)),
}
CVD_VI = {'protan': 'protan (mù đỏ)', 'deutan': 'deutan (mù lục)',
          'tritan': 'tritan (mù lam)'}


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return '#%02X%02X%02X' % tuple(
        int(round(max(0.0, min(1.0, c)) * 255)) for c in rgb)


def to_linear(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def to_srgb(c):
    c = max(0.0, min(1.0, c))
    return c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def luminance(hexcolor):
    """Độ chói tương đối theo WCAG 2.1."""
    r, g, b = (to_linear(c) for c in hex_to_rgb(hexcolor))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(hex_a, hex_b):
    la, lb = luminance(hex_a), luminance(hex_b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)


def simulate(hexcolor, kind):
    """Màu này người mù màu dạng `kind` nhìn thành màu gì."""
    lin = [to_linear(c) for c in hex_to_rgb(hexcolor)]
    m = CVD_MATRIX[kind]
    out = [sum(m[i][j] * lin[j] for j in range(3)) for i in range(3)]
    return rgb_to_hex([to_srgb(c) for c in out])


def to_lab(hexcolor):
    r, g, b = (to_linear(c) for c in hex_to_rgb(hexcolor))
    x = 0.4124564 * r + 0.3575761 * g + 0.1804375 * b
    y = 0.2126729 * r + 0.7151522 * g + 0.0721750 * b
    z = 0.0193339 * r + 0.1191920 * g + 0.9503041 * b
    # chuẩn trắng D65
    x, y, z = x / 0.95047, y / 1.0, z / 1.08883

    def f(t):
        return t ** (1.0 / 3) if t > 216.0 / 24389 else (841.0 / 108) * t + 4.0 / 29

    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def ciede2000(lab1, lab2):
    """ΔE00 — công thức CIE 2000, kL = kC = kH = 1."""
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    rad, deg = math.radians, math.degrees

    c1 = math.hypot(a1, b1)
    c2 = math.hypot(a2, b2)
    cbar = (c1 + c2) / 2.0
    g = 0.5 * (1 - math.sqrt(cbar ** 7 / (cbar ** 7 + 25.0 ** 7))) if cbar else 0.5
    a1p, a2p = (1 + g) * a1, (1 + g) * a2
    c1p, c2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = 0.0 if (a1p == 0 and b1 == 0) else deg(math.atan2(b1, a1p)) % 360
    h2p = 0.0 if (a2p == 0 and b2 == 0) else deg(math.atan2(b2, a2p)) % 360

    dlp = l2 - l1
    dcp = c2p - c1p
    if c1p * c2p == 0:
        dhp = 0.0
    else:
        dhp = h2p - h1p
        if dhp > 180:
            dhp -= 360
        elif dhp < -180:
            dhp += 360
    dhp_big = 2 * math.sqrt(c1p * c2p) * math.sin(rad(dhp / 2.0))

    lbar = (l1 + l2) / 2.0
    cbarp = (c1p + c2p) / 2.0
    if c1p * c2p == 0:
        hbar = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        hbar = (h1p + h2p) / 2.0
    elif h1p + h2p < 360:
        hbar = (h1p + h2p + 360) / 2.0
    else:
        hbar = (h1p + h2p - 360) / 2.0

    t = (1 - 0.17 * math.cos(rad(hbar - 30)) + 0.24 * math.cos(rad(2 * hbar))
         + 0.32 * math.cos(rad(3 * hbar + 6)) - 0.20 * math.cos(rad(4 * hbar - 63)))
    dtheta = 30 * math.exp(-(((hbar - 275) / 25.0) ** 2))
    rc = 2 * math.sqrt(cbarp ** 7 / (cbarp ** 7 + 25.0 ** 7)) if cbarp else 0.0
    sl = 1 + (0.015 * (lbar - 50) ** 2) / math.sqrt(20 + (lbar - 50) ** 2)
    sc = 1 + 0.045 * cbarp
    sh = 1 + 0.015 * cbarp * t
    rt = -math.sin(rad(2 * dtheta)) * rc

    return math.sqrt((dlp / sl) ** 2 + (dcp / sc) ** 2 + (dhp_big / sh) ** 2
                     + rt * (dcp / sc) * (dhp_big / sh))


def pairwise(colors):
    """Trả về (ΔE nhỏ nhất, chỉ số i, chỉ số j) trong danh sách màu."""
    labs = [to_lab(c) for c in colors]
    worst, wi, wj = float('inf'), -1, -1
    for i in range(len(colors)):
        for j in range(i + 1, len(colors)):
            d = ciede2000(labs[i], labs[j])
            if d < worst:
                worst, wi, wj = d, i, j
    return worst, wi, wj


def check(palette, label):
    ids = sorted(palette)
    colors = [palette[i] for i in ids]
    names = [SECTOR_NAME_VI.get(i, str(i)) for i in ids]
    fails = []

    print('=' * 78)
    print(label)
    print('=' * 78)

    print('\n1. TƯƠNG PHẢN WCAG')
    print('%-3s %-30s %-8s %8s %7s  %-6s %s'
          % ('#', 'Ngành', 'Hex', 'vs trắng', 'vs đen', 'chữ', 'ghi chú'))
    for i, c, n in zip(ids, colors, names):
        cw, cb = contrast(c, '#FFFFFF'), contrast(c, '#000000')
        text = 'trắng' if cw >= cb else 'đen'
        tc = max(cw, cb)
        note = ''
        if cw < NEEDS_BORDER:
            # Không tính là hỏng: bảng màu này để TÔ MẢNG, không để vẽ đường
            # mảnh. Nhưng mảng nhạt nằm trên nền trắng thì phải có viền mới
            # thấy được mép.
            note = 'cần viền trắng 1px'
        if tc < MIN_CONTRAST_TEXT:
            note = (note + '; ' if note else '') + 'KHÔNG đặt chữ lên được'
            fails.append('%s: chữ đè lên chỉ đạt %.2f < %.1f'
                         % (n, tc, MIN_CONTRAST_TEXT))
        print('%-3d %-30s %-8s %8.2f %7.2f  %-6s %s'
              % (i, n, c, cw, cb, text, note))

    print('\n2. MÔ PHỎNG MÙ MÀU (màu người mù màu thực sự nhìn thấy)')
    print('%-3s %-30s %-8s %-8s %-8s %-8s'
          % ('#', 'Ngành', 'gốc', 'protan', 'deutan', 'tritan'))
    for i, c, n in zip(ids, colors, names):
        print('%-3d %-30s %-8s %-8s %-8s %-8s'
              % (i, n, c, simulate(c, 'protan'), simulate(c, 'deutan'),
                 simulate(c, 'tritan')))

    print('\n3. KHOẢNG CÁCH CIEDE2000 — %d cặp' % (len(ids) * (len(ids) - 1) // 2))
    cases = [('mắt thường', colors, MIN_DE_NORMAL)]
    for kind in ('protan', 'deutan', 'tritan'):
        cases.append((CVD_VI[kind], [simulate(c, kind) for c in colors],
                      MIN_DE_CVD))
    for lbl, cols, thr in cases:
        d, i, j = pairwise(cols)
        ok = 'ĐẠT ' if d >= thr else 'HỎNG'
        print('  %s  %-16s cặp gần nhất ΔE = %5.1f  (ngưỡng %.0f)  %s ↔ %s'
              % (ok, lbl, d, thr, names[i], names[j]))
        if d < thr:
            fails.append('%s: %s ↔ %s chỉ cách ΔE %.1f, dưới ngưỡng %.0f'
                         % (lbl, names[i], names[j], d, thr))
    return fails


def main():
    fails = check(SECTOR_PALETTE, 'BẢNG MÀU 10 NGÀNH CẤP 1 HS92 (T04)')
    print('\n' + '=' * 78)
    if fails:
        print('KHÔNG ĐẠT — %d vấn đề:' % len(fails))
        for f in fails:
            print('  - ' + f)
        return 1
    print('ĐẠT toàn bộ tiêu chí.')
    print('  ΔE2000 >= %.0f ở mắt thường, >= %.0f ở cả ba dạng mù màu,'
          % (MIN_DE_NORMAL, MIN_DE_CVD))
    print('  và mọi ô màu đều đặt được chữ lên với tương phản >= %.1f:1.'
          % MIN_CONTRAST_TEXT)
    print('  Các màu ghi "cần viền trắng 1px" vẫn dùng được — chỉ là phải có')
    print('  viền mới tách được mép mảng khỏi nền trắng.')
    return 0


if __name__ == '__main__':
    sys.exit(main())

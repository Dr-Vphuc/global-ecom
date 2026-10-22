# -*- coding: utf-8 -*-
"""B17 — còn chỗ trong không gian màu cho một bảng màu thứ ba không?

Chon tham lam maximin: moi buoc lay mau cach xa nhat moi mau DA bi chiem
(10 mau nganh + 3 mau cum) va moi mau da chon. Neu min DeltaE tot nhat dat
duoc van duoi nguong 15 thi khong phai do chon kem - la het cho that.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_palette as C
import reference_data as R

TAKEN = [c for c in R.SECTOR_PALETTE.values()] + [c for c in R.COMMUNITY_PALETTE.values()]
taken_lab = [C.to_lab(h) for h in TAKEN]

# Luoi mau: buoc 15/255, bo mau qua sang hoac qua toi de con in duoc
grid = []
step = 9
for r in range(0, 256, step):
    for g in range(0, 256, step):
        for b in range(0, 256, step):
            h = C.rgb_to_hex((r, g, b))
            L = C.luminance(h)
            if 0.03 <= L <= 0.78:
                grid.append(h)
print('luoi ung vien: %d mau' % len(grid))

lab = {h: C.to_lab(h) for h in grid}

def dmin_to(h, labs):
    ds = [C.ciede2000(lab[h], l) for l in labs]
    ds = [d for d in ds if d == d]          # bo NaN
    return min(ds) if ds else 0.0

picked, picked_lab = [], []
taken_set = set(TAKEN)
for k in range(1, 9):
    scored = [(dmin_to(h, taken_lab + picked_lab), h)
              for h in grid if h not in picked and h not in taken_set]
    scored = [(d, h) for (d, h) in scored if d == d]
    if not scored:
        print('  het ung vien o mau thu %d' % k)
        break
    bestd, best = max(scored)
    picked.append(best)
    picked_lab.append(lab[best])
    print('  mau thu %d: %s  -> min DeltaE con lai = %5.1f' % (k, best, bestd))

print()
for n in (2, 3, 5, 7):
    if n > len(picked):
        continue
    sub = picked[:n]
    sub_lab = [lab[h] for h in sub]
    worst = min(min(C.ciede2000(sub_lab[i], l) for l in taken_lab)
                for i in range(n))
    pair = min(C.ciede2000(sub_lab[i], sub_lab[j])
               for i in range(n) for j in range(i + 1, n))
    cvd = 99.0
    for kind in ('protan', 'deutan', 'tritan'):
        sl = [C.to_lab(C.simulate(h, kind)) for h in sub]
        for i in range(n):
            for j in range(i + 1, n):
                cvd = min(cvd, C.ciede2000(sl[i], sl[j]))
    print('%d mau: cach mau da chiem %4.1f | cach nhau %4.1f | mu mau %4.1f  (can 15 / 15 / 10)'
          % (n, worst, pair, cvd))

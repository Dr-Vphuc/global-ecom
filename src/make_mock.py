# -*- coding: utf-8 -*-
"""T05 — Sinh dữ liệu giả đúng schema hợp đồng để R2 và R3 vẽ ngay.

Từ khi T07 đóng, pipeline thật đã sinh được country_product.csv, nên bản mock
chỉ còn hai vai trò:

    data/mock/metrics.csv   — chưa có bản thật, phải chờ T18
    các file còn lại        — bản rút gọn để nạp nhanh khi thử bố cục
                              (nodes, edges, tree, country_product)

Giá trị là GIẢ nhưng PHÂN BỐ được làm giống thật (lệch phải rất mạnh,
đúng dạng luật lũy thừa của dữ liệu thương mại) để bố cục biểu đồ,
thang log và chú giải không bị lệch khi thay bằng dữ liệu thật.

    python src/make_mock.py

Chỉ dùng thư viện chuẩn.
"""

import csv
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from reference_data import (  # noqa: E402
    ASEAN_ISO3,
    COUNTRY_VI,
    DEFAULT_THRESHOLD,
    FOCUS_ISO3,
    MAJOR_PARTNERS,
    MILESTONE_YEARS,
    SECTOR_PALETTE_PROVISIONAL,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK = os.path.join(ROOT, "data", "mock")

SEED = 20260920          # co dinh de moi nguoi sinh ra cung mot bo gia
random.seed(SEED)

# Tap nuoc gon cho ban mock: ASEAN + doi tac lon + vai nuoc rai rac.
MOCK_COUNTRIES = (
    ASEAN_ISO3
    + MAJOR_PARTNERS
    + ["FRA", "GBR", "AUS", "BRA", "ZAF", "RUS", "MEX", "CAN", "NLD", "ITA",
       "ESP", "TUR", "SAU", "ARE", "BGD", "PAK", "NGA", "EGY", "CHL", "ARG"]
)


def write(path, fieldnames, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print("  -> %s  (%d dong)" % (os.path.relpath(path, ROOT), len(rows)))


def heavy_tail(scale):
    """Gia tri lech phai manh, giong phan bo kim ngach thuc te."""
    return scale * math.exp(random.gauss(0, 1.8))


def mock_nodes():
    rows = []
    # country_id phải CỐ ĐỊNH và DUY NHẤT. Bản cũ dùng abs(hash(iso)) % 900 + 4,
    # sai cả hai đường: hash() của chuỗi bị ngẫu nhiên hoá theo từng tiến trình
    # Python (PYTHONHASHSEED) nên mỗi lần chạy ra một bộ id khác — random.seed()
    # không cứu được vì hash() không dùng tới nó — và nó còn đụng id: IND và RUS
    # cùng nhận 779. Đánh số theo vị trí trong MOCK_COUNTRIES là xong cả hai.
    for i, iso in enumerate(MOCK_COUNTRIES):
        vi, region, continent = COUNTRY_VI[iso]
        rows.append({
            "country_iso3": iso,
            "country_id": 4 + i * 7,
            "country_name": iso,
            "country_name_vi": vi,
            "region": region,
            "continent": continent,
            "is_focus": "TRUE" if iso in FOCUS_ISO3 else "FALSE",
        })
    write(os.path.join(MOCK, "nodes.csv"),
          ["country_iso3", "country_id", "country_name", "country_name_vi",
           "region", "continent", "is_focus"], rows)


def mock_edges():
    rows = []
    for year in MILESTONE_YEARS:
        growth = 1.0 + 0.09 * (year - 1995)     # thuong mai phinh to theo thoi gian
        for s in MOCK_COUNTRIES:
            for t in MOCK_COUNTRIES:
                if s == t or random.random() > 0.55:
                    continue
                exp = heavy_tail(2e8) * growth
                imp = exp * random.uniform(0.85, 1.25)
                rows.append({
                    "source_iso3": s,
                    "target_iso3": t,
                    "year": year,
                    "export_value": round(exp, 2),
                    "import_value": round(imp, 2),
                    "log_value": round(math.log10(exp), 4),
                    "above_threshold": "TRUE" if exp >= DEFAULT_THRESHOLD else "FALSE",
                })
    write(os.path.join(MOCK, "edges.csv"),
          ["source_iso3", "target_iso3", "year", "export_value", "import_value",
           "log_value", "above_threshold"], rows)


def mock_tree():
    """Cay rut gon: 10 nganh cap 1, moi nganh 8 nut cap 2, moi nut 5 nut cap 4."""
    rows, pid = [], 0

    def add(parent, level, code, name, sector):
        nonlocal pid
        pid += 1
        rows.append({
            "product_id": pid,
            "parent_id": parent if parent else "",
            "level": level,
            "hs92_code": code,
            "name": name,
            "name_short": name[:18],
            "sector_id": sector,
            "sector_color": SECTOR_PALETTE_PROVISIONAL.get(sector, ""),
        })
        return pid

    for s in range(1, 11):
        root = add(None, 1, str(s - 1), "Nganh %d" % s, s)
        for c2 in range(8):
            n2 = add(root, 2, "%02d" % (s * 8 + c2), "Nhom %d-%d" % (s, c2), s)
            for c4 in range(5):
                add(n2, 4, "%04d" % (s * 800 + c2 * 10 + c4),
                    "San pham %d-%d-%d" % (s, c2, c4), s)
    write(os.path.join(MOCK, "tree.csv"),
          ["product_id", "parent_id", "level", "hs92_code", "name", "name_short",
           "sector_id", "sector_color"], rows)
    return rows


def mock_country_product(tree_rows):
    leaves = [r for r in tree_rows if r["level"] == 4]
    rows = []
    for iso in MOCK_COUNTRIES:
        for year in MILESTONE_YEARS:
            for p in random.sample(leaves, 60):
                rows.append({
                    "country_iso3": iso,
                    "product_id": p["product_id"],
                    "year": year,
                    "export_value": round(heavy_tail(5e7), 2),
                    "rca": round(math.exp(random.gauss(0, 1.0)), 3),
                    "pci": round(random.gauss(0, 1.0), 3),
                })
    write(os.path.join(MOCK, "country_product.csv"),
          ["country_iso3", "product_id", "year", "export_value", "rca", "pci"], rows)


def mock_metrics():
    rows = []
    n = len(MOCK_COUNTRIES)
    for iso in MOCK_COUNTRIES:
        for year in MILESTONE_YEARS:
            dout = random.randint(int(n * 0.3), n - 1)
            rows.append({
                "country_iso3": iso,
                "year": year,
                "degree_out": dout,
                "degree_in": random.randint(int(n * 0.3), n - 1),
                "strength_out": round(heavy_tail(3e10), 2),
                "betweenness": round(abs(random.gauss(0, 0.03)), 5),
                "community_id": random.randint(1, 5),
                "eci": round(random.gauss(0, 1.0), 3),
            })
    write(os.path.join(MOCK, "metrics.csv"),
          ["country_iso3", "year", "degree_out", "degree_in", "strength_out",
           "betweenness", "community_id", "eci"], rows)


def main():
    print("Sinh du lieu gia (seed=%d) vao data/mock/" % SEED)
    mock_nodes()
    mock_edges()
    tree_rows = mock_tree()
    mock_country_product(tree_rows)
    mock_metrics()
    print("\nXong. GIA TRI LA GIA — chi dung de dung bo cuc bieu do.")
    print("Khong duoc dua bat ky con so nao tu day vao bao cao.")


if __name__ == "__main__":
    main()

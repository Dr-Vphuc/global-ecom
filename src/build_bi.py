# -*- coding: utf-8 -*-
"""Dựng dashboard BI — gói dữ liệu tổng hợp + trang tĩnh, ra ``site/bi/``.

Vì sao tách khỏi bài viết và báo cáo
------------------------------------
Bài viết (``build_web.py``) và báo cáo kể một câu chuyện về Việt Nam năm 2023.
Dashboard thì không kể gì: nó để người xem tự chọn nước, năm, ngành, chiều xuất
hay nhập rồi đọc số. Nên nó không dùng ``do_so()`` hay các file Plotly đã dựng
sẵn (mỗi file chỉ mang một năm), mà vẽ trên trình duyệt từ một gói dữ liệu đã
gộp, và không in một câu nhận xét nào.

Gói dữ liệu
-----------
Gộp từ ``data/processed/`` — không phải dữ liệu thô (Nguyên tắc #5):

* ``data/world.json`` — danh mục nước, ngành, 97 nhóm HS2; theo từng năm: tổng
  xuất khẩu thế giới của mỗi nhóm HS2 (mẫu số của RCA), PCI của mỗi nhóm, và
  chuỗi chỉ số theo nước (xuất, nhập, ECI, hạng ECI).
* ``data/c/<ISO3>.json`` — một file mỗi nước, tải khi được chọn: xuất khẩu theo
  97 nhóm HS2 từng năm; xuất và nhập với 40 đối tác lớn nhất cả giai đoạn (phần
  còn lại gộp "Các nước khác"); và tổng theo khu vực, tính trên MỌI đối tác.

RCA không được chở theo: ``(x_cp / x_c) / (x_p / x_w)`` tính lại trên trình duyệt
từ đúng các số trên khớp với cột ``rca`` của Atlas tới 5·10⁻⁵ (đã đo, năm 2023).
Giá trị tính bằng nghìn USD, số nguyên. Năm cuối là ``REFERENCE_YEAR`` (2023):
bản 2024 còn tạm (A6).

Chạy
----
    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/build_bi.py

Chạy sau ``build_web.py`` hay trước đều được: ``build_web.py`` không đụng tới
``site/bi/``.
"""

from __future__ import print_function

import io
import json
import os
import shutil
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_data as R                      # noqa: E402

DATA = os.path.join("data", "processed")
SRC = os.path.join("src", "web", "bi")
OUT = os.path.join("site", "bi")
NAM0, NAM1 = 1995, R.REFERENCE_YEAR
NAM = list(range(NAM0, NAM1 + 1))
SO_DOI_TAC = 40


def _k(v):
    """USD → nghìn USD, số nguyên (0 khi trống)."""
    return int(round(float(v) / 1000.0)) if v == v else 0


def _ghi(p, obj):
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def doc():
    cp = pd.read_csv(os.path.join(DATA, "country_product.csv"))
    cp = cp[(cp["year"] >= NAM0) & (cp["year"] <= NAM1)]
    cy = pd.read_csv(os.path.join(DATA, "country_year.csv"))
    cy = cy[(cy["year"] >= NAM0) & (cy["year"] <= NAM1)]
    e = pd.read_csv(os.path.join(DATA, "edges.csv"),
                    usecols=["source_iso3", "target_iso3", "year", "export_value"])
    e = e[(e["year"] >= NAM0) & (e["year"] <= NAM1) & (e["source_iso3"] != e["target_iso3"])]
    tree = pd.read_csv(os.path.join(DATA, "tree.csv"), dtype={"hs92_code": str})
    nodes = pd.read_csv(os.path.join(DATA, "nodes.csv"))
    return cp, cy, e, tree, nodes


def danh_muc(cp, cy, tree, nodes):
    hs2 = tree[tree["level"] == 2].sort_values("hs92_code")
    hs2_ids = [int(i) for i in hs2["product_id"]]
    nuoc = sorted(set(cp["country_iso3"]) | set(cy["country_iso3"]))
    nd = nodes.set_index("country_iso3")
    ds_nuoc = []
    for iso in nuoc:
        if iso in nd.index:
            r = nd.loc[iso]
            ten = r["country_name_vi"] if isinstance(r["country_name_vi"], str) \
                and r["country_name_vi"].strip() else r["country_name"]
            kv = R.REGION_VI.get(r["region"], r["region"])
            ca = R.CONTINENT_VI.get(r["continent"], r["continent"])
        else:
            ten, kv, ca = iso, "Không rõ", "Không rõ"
        ds_nuoc.append({"iso": iso, "ten": ten, "kv": kv, "ca": ca})
    ds_hs2 = [{"id": int(r["product_id"]), "ma": r["hs92_code"],
               "ten": R.HS2_NAME_VI.get(r["hs92_code"], r["name_short"]),
               "ng": int(r["sector_id"])} for _, r in hs2.iterrows()]
    ds_nganh = [{"id": k, "ten": R.SECTOR_NAME_VI[k], "mau": R.SECTOR_PALETTE[k]}
                for k in sorted(R.SECTOR_PALETTE)]
    return hs2_ids, ds_nuoc, ds_hs2, ds_nganh


def the_gioi(cp, cy, hs2_ids, ds_nuoc, ds_hs2, ds_nganh):
    # Mẫu số của RCA: xuất khẩu thế giới của từng nhóm, cộng trên CHÍNH bảng
    # country_product để tử và mẫu cùng một nguồn.
    wp = cp.groupby(["year", "product_id"])["export_value"].sum().unstack(fill_value=0)
    wp = wp.reindex(index=NAM, columns=hs2_ids, fill_value=0)
    pci = cp.groupby(["year", "product_id"])["pci"].first().unstack()
    pci = pci.reindex(index=NAM, columns=hs2_ids)
    chi_so = {}
    cyi = cy.set_index(["country_iso3", "year"]).sort_index()
    for n in ds_nuoc:
        iso = n["iso"]
        if iso not in cyi.index.get_level_values(0):
            continue
        d = cyi.loc[iso].reindex(NAM)
        chi_so[iso] = {
            "x": [_k(v) for v in d["export_value"]],
            "m": [_k(v) for v in d["import_value"]],
            "eci": [None if v != v else round(float(v), 3) for v in d["eci"]],
            "er": [None if v != v else int(v) for v in d["eci_rank"]],
            "en": [None if v != v else int(v) for v in d["eci_n"]],
            # Không chở cột diversity: năm 2004 nó gần gấp đôi ở mọi nước (A20).
        }
    return {
        "nam": NAM, "nuoc": ds_nuoc, "nganh": ds_nganh, "hs2": ds_hs2,
        "wp": [[_k(v) for v in wp.loc[y]] for y in NAM],
        "pci": [[None if v != v else round(float(v), 3) for v in pci.loc[y]] for y in NAM],
        "cs": chi_so,
    }


def mot_nuoc(iso, cp_c, ex, im, hs2_ids, kv_cua):
    p = cp_c.pivot_table(index="year", columns="product_id", values="export_value",
                         aggfunc="sum").reindex(index=NAM, columns=hs2_ids)
    out = {"p": [[_k(v) for v in p.loc[y]] for y in NAM]}

    def bang(d, cot):
        t = d.pivot_table(index=cot, columns="year", values="export_value",
                          aggfunc="sum").reindex(columns=NAM).fillna(0.0)
        return t

    tx, tm = bang(ex, "target_iso3"), bang(im, "source_iso3")
    tong = tx.sum(axis=1).add(tm.sum(axis=1), fill_value=0).sort_values(ascending=False)
    dau = list(tong.index[:SO_DOI_TAC])
    tx_, tm_ = tx.reindex(dau).fillna(0.0), tm.reindex(dau).fillna(0.0)
    out["dt"] = dau
    out["x"] = [[_k(v) for v in tx_.loc[i]] for i in dau]
    out["m"] = [[_k(v) for v in tm_.loc[i]] for i in dau]
    out["xk"] = [_k(v) for v in (tx.sum(axis=0) - tx_.sum(axis=0))]
    out["mk"] = [_k(v) for v in (tm.sum(axis=0) - tm_.sum(axis=0))]
    kv = {}
    for ten, t in (("x", tx), ("m", tm)):
        g = t.groupby(t.index.map(lambda i: kv_cua.get(i, "Không rõ"))).sum()
        kv[ten] = {k: [_k(v) for v in g.loc[k]] for k in g.index}
    out["kv"] = kv
    return out


def kiem(world, mau):
    """In khối kiểm chứng; trả về số lỗi."""
    loi = 0
    print("\n" + "=" * 72)
    print("KIỂM CHỨNG — gói dữ liệu dashboard")
    print("=" * 72)
    i = NAM.index(NAM1)
    for iso in ("VNM", "CHN", "USA"):
        c = mau[iso]
        tong_hs2 = sum(c["p"][i])
        tong_dt = sum(r[i] for r in c["x"]) + c["xk"][i]
        tong_kv = sum(v[i] for v in c["kv"]["x"].values())
        cs = world["cs"][iso]["x"][i]
        print("\n  %s %d (tỷ USD): country_year %s · cộng HS2 %s · cộng đối tác %s · "
              "cộng khu vực %s" % (iso, NAM1, R.fmt_vn(cs / 1e6, 1),
                                   R.fmt_vn(tong_hs2 / 1e6, 1), R.fmt_vn(tong_dt / 1e6, 1),
                                   R.fmt_vn(tong_kv / 1e6, 1)))
        # Đối tác và khu vực là hai cách cộng cùng một bảng cạnh: phải khớp tuyệt đối.
        if abs(tong_dt - tong_kv) > len(c["kv"]["x"]) + SO_DOI_TAC + 1:
            print("     LỆCH  đối tác ≠ khu vực")
            loi += 1
        # Ba nguồn tổng (country_year, cộng HS2, cộng cạnh) là ba bảng khác nhau của
        # Atlas; in độ lệch để người xem biết, chỉ coi là lỗi khi quá 5%.
        for ten, v in (("HS2", tong_hs2), ("đối tác", tong_dt)):
            lech = abs(v - cs) / float(cs) * 100.0
            print("     %s so với country_year: lệch %s" % (ten, R.fmt_pct(lech, 2)))
            if lech > 5:
                loi += 1
    vn = mau["VNM"]
    ten = {n["iso"]: n["ten"] for n in world["nuoc"]}
    print("\n  Ba đối tác xuất khẩu lớn nhất của VNM %d: %s" % (NAM1, " · ".join(
        "%s %s" % (ten.get(d, d), R.fmt_vn(r[i] / 1e6, 1)) for d, r in
        sorted(zip(vn["dt"], vn["x"]), key=lambda t: -t[1][i])[:3])))

    tong = 0
    for goc, _, files in os.walk(OUT):
        tong += sum(os.path.getsize(os.path.join(goc, f)) for f in files)
    print("\n  Nước: %d · nhóm HS2: %d · năm: %d–%d · dung lượng site/bi/: %s MB"
          % (len(mau), len(world["hs2"]), NAM0, NAM1, R.fmt_vn(tong / 1048576.0, 1)))
    if tong > 25 * 1048576:
        print("     QUÁ LỚN")
        loi += 1
    print("\n  %s" % ("ĐẠT" if not loi else "KHÔNG ĐẠT — %d lỗi" % loi))
    print("=" * 72)
    return loi


def main():
    print("Đọc data/processed/ ...")
    cp, cy, e, tree, nodes = doc()
    hs2_ids, ds_nuoc, ds_hs2, ds_nganh = danh_muc(cp, cy, tree, nodes)
    world = the_gioi(cp, cy, hs2_ids, ds_nuoc, ds_hs2, ds_nganh)
    kv_cua = {n["iso"]: n["kv"] for n in ds_nuoc}

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "data", "c"))
    for f in os.listdir(SRC):
        shutil.copyfile(os.path.join(SRC, f), os.path.join(OUT, f))
    _ghi(os.path.join(OUT, "data", "world.json"), world)

    ex_g = dict(tuple(e.groupby("source_iso3")))
    im_g = dict(tuple(e.groupby("target_iso3")))
    cp_g = dict(tuple(cp.groupby("country_iso3")))
    trong = e.iloc[0:0]
    mau = {}
    for n in ds_nuoc:
        iso = n["iso"]
        if iso not in cp_g and iso not in ex_g:
            continue
        c = mot_nuoc(iso, cp_g.get(iso, cp.iloc[0:0]), ex_g.get(iso, trong),
                     im_g.get(iso, trong), hs2_ids, kv_cua)
        _ghi(os.path.join(OUT, "data", "c", iso + ".json"), c)
        mau[iso] = c
    # Nước chọn được = có file VÀ có chuỗi country_year (ô chỉ số cần cả hai).
    world["co"] = sorted(iso for iso in mau if iso in world["cs"])
    _ghi(os.path.join(OUT, "data", "world.json"), world)
    print("  %s/ · %d nước" % (OUT, len(mau)))
    return 1 if kiem(world, mau) else 0


if __name__ == "__main__":
    np.seterr(all="ignore")
    sys.exit(main())

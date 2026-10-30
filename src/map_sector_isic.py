"""Ghép 10 ngành Atlas (HS92) sang mã ISIC Rev.4 của OECD TiVA 2025, rồi tính
tỷ lệ giá trị làm ra trong nước của từng ngành xuất khẩu Việt Nam.

Vì sao cần: RCA/PCI/ECI tính trên xuất khẩu gộp (D2, D5). TiVA tách được phần
giá trị gia tăng làm ra trong nước (EXGR_DVA) nhưng chia theo ngành ISIC, không
theo HS. Cầu nối là bảng ghép HS2 -> ISIC ở data/reference/hs2_to_isic4.csv.

Cách tính: với mỗi nhóm HS2, lấy tỷ lệ trong nước của ngành ISIC được ghép,
rồi bình quân gia quyền theo xuất khẩu HS2 của Việt Nam trong cùng năm.

    python src/map_sector_isic.py [--year 2022]

Năm mặc định là 2022 vì TiVA 2025 dừng ở 2022 (REFERENCE_YEAR của dự án là 2023).
Dữ liệu TiVA tải về data/raw/ (đã nằm trong .gitignore) và dùng lại lần sau.
"""
import argparse
import io
import os
import sys
import urllib.request

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_data as R  # noqa: E402

DATA = os.path.join("data", "processed")
RAW = os.path.join("data", "raw")
CONCORDANCE = os.path.join("data", "reference", "hs2_to_isic4.csv")
FOCUS = "VNM"

# Máy chủ "public" của OECD trả lỗi 500 cho truy vấn dữ liệu TiVA; "sti-public" chạy được.
SDMX = "https://sdmx.oecd.org/sti-public/rest/data/OECD.STI.PIE,%s,1.1/%s"
# Khóa theo thứ tự MEASURE.REF_AREA.ACTIVITY.COUNTERPART_AREA.UNIT_MEASURE.FREQ
SHARES = ("DSD_TIVA_MAINSH@DF_MAINSH", "EXGR_DVA.%s...." % FOCUS, "tiva_vnm_exgr_dva_pct.csv")
LEVELS = ("DSD_TIVA_MAINLV@DF_MAINLV", "EXGR.%s...." % FOCUS, "tiva_vnm_exgr_usd.csv")


def fetch(spec):
    flow, key, name = spec
    path = os.path.join(RAW, name)
    if not os.path.exists(path):
        os.makedirs(RAW, exist_ok=True)
        url = (SDMX % (flow, key)) + "?startPeriod=1995&endPeriod=2022"
        req = urllib.request.Request(
            url, headers={"Accept": "application/vnd.sdmx.data+csv",
                          "User-Agent": "curl/8.0"})  # urllib mặc định bị 403
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read()
        with io.open(path, "wb") as f:
            f.write(body)
    return pd.read_csv(path)


def load_exports(year):
    tree = pd.read_csv(os.path.join(DATA, "tree.csv"), dtype={"hs92_code": str})
    h2 = tree[tree["level"] == 2][["product_id", "hs92_code", "sector_id"]]
    cp = pd.read_csv(os.path.join(DATA, "country_product.csv"))
    cp = cp[(cp["country_iso3"] == FOCUS) & (cp["year"] == year)]
    out = h2.merge(cp[["product_id", "export_value", "pci"]], on="product_id", how="left")
    out["export_value"] = out["export_value"].fillna(0.0)
    return out.rename(columns={"hs92_code": "hs2"})


def dva_by_sector(ex, share, col):
    """Bình quân gia quyền tỷ lệ trong nước theo xuất khẩu HS2, mỗi ngành Atlas."""
    d = ex.assign(pct=ex[col].map(share))
    d = d[d["pct"].notna()]
    d = d.assign(dva=d["pct"] * d["export_value"])
    g = d.groupby("sector_id")
    return g["dva"].sum() / g["export_value"].sum(), g["export_value"].sum()


def spearman(x, y, n_perm=10000):
    """Hệ số Spearman và p-value hoán vị hai phía (không cần scipy)."""
    rx, ry = x.rank().values, y.rank().values
    r = float(np.corrcoef(rx, ry)[0, 1])
    rng = np.random.RandomState(0)
    perm = [np.corrcoef(rx, rng.permutation(ry))[0, 1] for _ in range(n_perm)]
    return r, float(np.mean(np.abs(perm) >= abs(r)))


def pci_vs_dva(mapped, share, sector_dva):
    """PCI của hàng (độ phức tạp) so với tỷ lệ trong nước: có thật là hàng càng
    phức tạp thì càng ít giá trị ở lại không? Hai mức: nhóm HS2 và mã ISIC."""
    m = mapped.assign(dva=mapped["isic_primary"].map(share))
    r2, p2 = spearman(m["pci"], m["dva"])
    g = m.assign(w=m["pci"] * m["export_value"]).groupby("isic_primary")
    isic = pd.DataFrame({"pci": g["w"].sum() / g["export_value"].sum(),
                         "dva": g["dva"].first(), "usd": g["export_value"].sum()})
    r1, p1 = spearman(isic["pci"], isic["dva"])
    print("\n=== PCI so với tỷ lệ trong nước (Spearman, hoán vị 10.000 lần) ===")
    print("Mức nhóm HS2 : n=%d  rho=%s  p=%s" % (len(m), R.fmt_vn(r2, 2), R.fmt_vn(p2, 3)))
    print("Mức mã ISIC  : n=%d  rho=%s  p=%s  (PCI bình quân gia quyền theo xuất khẩu)"
          % (len(isic), R.fmt_vn(r1, 2), R.fmt_vn(p1, 3)))
    s = m.assign(w=m["pci"] * m["export_value"]).groupby("sector_id")
    sec = (s["w"].sum() / s["export_value"].sum()).sort_values(ascending=False)
    print("PCI bình quân gia quyền theo ngành Atlas (trong nước ở ngoặc):")
    for sid, v in sec.items():
        print("  %-30s %6s  (%s)" % (R.SECTOR_NAME_VI[sid], R.fmt_vn(v, 2),
                                     R.fmt_pct(float(sector_dva[sid]))))
    return r1, p1, r2, p2, sec, len(isic), len(m)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2022)
    year = ap.parse_args().year

    conc = pd.read_csv(CONCORDANCE, dtype=str, keep_default_na=False)
    ex = load_exports(year).merge(conc, on="hs2", how="left")
    assert ex["isic_primary"].notna().all(), "có nhóm HS2 chưa nằm trong bảng ghép"
    ex["isic_alt"] = ex["isic_alt"].where(ex["isic_alt"] != "", ex["isic_primary"])
    for c in ("isic_primary", "isic_alt"):
        ex[c] = ex[c].replace("", pd.NA)

    shares = fetch(SHARES)
    hist = shares[shares["COUNTERPART_AREA"] == "W"].pivot(
        index="ACTIVITY", columns="TIME_PERIOD", values="OBS_VALUE")
    shares = shares[(shares["TIME_PERIOD"] == year) & (shares["COUNTERPART_AREA"] == "W")]
    share = shares.set_index("ACTIVITY")["OBS_VALUE"]
    used = set(ex["isic_primary"].dropna()) | set(ex["isic_alt"].dropna())
    miss = sorted(used - set(share.index))
    assert not miss, "mã ISIC không có trong TiVA: %s" % miss

    base, weight = dva_by_sector(ex, share, "isic_primary")
    alt, _ = dva_by_sector(ex, share, "isic_alt")
    tot_usd = ex["export_value"].sum()
    unmapped = ex[ex["isic_primary"].isna()]["export_value"].sum()

    res = pd.DataFrame({"export_usd": weight, "dva_pct": base, "dva_alt_pct": alt})
    res["ten"] = [R.SECTOR_NAME_VI[i] for i in res.index]
    res["lo"] = res[["dva_pct", "dva_alt_pct"]].min(axis=1)
    res["hi"] = res[["dva_pct", "dva_alt_pct"]].max(axis=1)
    res["share_of_mapped_pct"] = 100.0 * res["export_usd"] / res["export_usd"].sum()
    res.index.name = "sector_id"
    out = os.path.join(DATA, "sector_dva_%d.csv" % year)

    # ---- khối kiểm chứng ----
    mapped = ex[ex["isic_primary"].notna()]
    w = mapped["export_value"]
    goods_avg = (mapped["isic_primary"].map(share) * w).sum() / w.sum()
    goods_alt = (mapped["isic_alt"].map(share) * w).sum() / w.sum()
    print("=== Tỷ lệ giá trị làm ra trong nước, Việt Nam %d (OECD TiVA 2025) ===" % year)
    print("Tổng xuất khẩu Atlas HS2 %d: %s | không ghép được (HS97, HS99): %s (%s)"
          % (year, R.fmt_usd(tot_usd), R.fmt_usd(unmapped), R.fmt_pct(100 * unmapped / tot_usd)))
    print("%-30s %9s %8s %8s %16s" % ("Ngành", "Xuất khẩu", "Tỷ trọng", "Trong nước", "Khoảng (2 cách ghép)"))
    for sid, r in res.iterrows():
        print("%-30s %9s %8s %10s %9s–%s" % (
            r["ten"], R.fmt_vn(r["export_usd"] / 1e9, 1), R.fmt_pct(r["share_of_mapped_pct"]),
            R.fmt_pct(r["dva_pct"]), R.fmt_vn(r["lo"], 1), R.fmt_pct(r["hi"])))
    print("Bình quân gia quyền hàng hóa ghép được: %s (cách ghép thay thế: %s)"
          % (R.fmt_pct(goods_avg), R.fmt_pct(goods_alt)))
    print("Đối chiếu TiVA: toàn nền kinh tế %s, công nghiệp chế biến (C) %s"
          % (R.fmt_pct(share["_T"]), R.fmt_pct(share["C"])))

    print("Chuỗi dài (TiVA, tỷ lệ trong nước): " + "; ".join(
        "%s %s→%s" % (lab, R.fmt_pct(hist.loc[code, 1995]), R.fmt_pct(hist.loc[code, year]))
        for lab, code in (("toàn nền kinh tế", "_T"), ("điện tử C26", "C26"),
                          ("dệt may C13T15", "C13T15"))) + " (1995→%d)" % year)

    r1, p1, r2, p2, sec_pci, n_isic, n_hs2 = pci_vs_dva(mapped, share, base)
    res["pci"] = sec_pci
    res.reset_index().to_csv(out, index=False, encoding="utf-8")

    # Các con số tiêu đề, để hình / slide / trang web lấy từ một chỗ thay vì tự tính
    # lại (và lệch nhau). Bốn ngành PCI cao nhất: "hàng khó" trong câu chuyện.
    top4 = res.loc[sec_pci.sort_values(ascending=False).index[:4]]
    head = {
        "nam": year,
        "dva_tong_dau": hist.loc["_T", 1995], "dva_tong_cuoi": hist.loc["_T", year],
        "dva_dien_dau": hist.loc["C26", 1995], "dva_dien_cuoi": hist.loc["C26", year],
        "dva_det_dau": hist.loc["C13T15", 1995], "dva_det_cuoi": hist.loc["C13T15", year],
        "dva_rb": goods_avg, "dva_rb_alt": goods_alt,
        "tiva_tong": share["_T"], "tiva_che_bien": share["C"],
        "rho": r1, "p": p1, "n_isic": n_isic,
        "rho_hs2": r2, "p_hs2": p2, "n_hs2": n_hs2,
        "top4_ty_trong": top4["share_of_mapped_pct"].sum(),
        "top4_lo": top4["dva_pct"].min(), "top4_hi": top4["dva_pct"].max(),
        "khac_pct": 100.0 * unmapped / tot_usd,
    }

    # ---- đối chiếu quy mô: bảng ghép có đưa xuất khẩu về đúng ngành không ----
    try:
        lv = fetch(LEVELS)
        lv = lv[(lv["TIME_PERIOD"] == year) & (lv["COUNTERPART_AREA"] == "W")]
        mult = lv["UNIT_MULT"].iloc[0] if "UNIT_MULT" in lv else 6
        usd = lv.set_index("ACTIVITY")["OBS_VALUE"] * (10.0 ** mult)
        print("\n=== Đối chiếu quy mô: Atlas (qua bảng ghép) so với TiVA EXGR, tỷ USD ===")
        print("%-12s %9s %9s %7s" % ("Mã ISIC", "Atlas", "TiVA", "Atlas/TiVA"))
        by = mapped.groupby("isic_primary")["export_value"].sum()
        codes = sorted(set(by.index) | set(mapped["isic_alt"].dropna()),
                       key=lambda c: -by.get(c, 0.0))
        for code in codes:
            v, t = by.get(code, 0.0), usd.get(code)
            print("%-12s %9s %9s %10s" % (
                code, R.fmt_vn(v / 1e9, 1) if v else "—", R.fmt_vn(t / 1e9, 1),
                R.fmt_vn(v / t, 2) if v else "—"))
        # HS84/85/90 chia đôi nhau giữa C26/C27/C28 mà HS2 không tách được. Tổng của
        # khối thì đối chiếu được, nên dùng quy mô của chính TiVA để lấy tỷ lệ khối.
        blk = ["C26", "C27", "C28"]
        tiva_blk = (share[blk] * usd[blk]).sum() / usd[blk].sum()
        hs_blk = mapped[mapped["hs2"].isin(["84", "85", "90", "91"])]
        atlas_blk = (hs_blk["isic_primary"].map(share) * hs_blk["export_value"]).sum() \
            / hs_blk["export_value"].sum()
        print("\nKhối C26+C27+C28: TiVA %s tỷ USD vs Atlas HS84/85/90/91 %s tỷ USD"
              % (R.fmt_vn(usd[blk].sum() / 1e9, 1), R.fmt_vn(hs_blk["export_value"].sum() / 1e9, 1)))
        print("Tỷ lệ trong nước của khối: %s (theo quy mô TiVA) vs %s (theo bảng ghép HS2)"
              % (R.fmt_pct(tiva_blk), R.fmt_pct(atlas_blk)))
        head["dva_khoi"], head["dva_khoi_hs"] = tiva_blk, atlas_blk
    except Exception as e:  # đối chiếu là phần phụ, đừng làm hỏng kết quả chính
        print("\n(bỏ qua phần đối chiếu quy mô: %s)" % e)
    hp = os.path.join(DATA, "tiva_headline_%d.csv" % year)
    pd.Series(head, name="value").rename_axis("key").to_csv(hp, encoding="utf-8")
    print("\nGhi ra %s và %s" % (out, hp))


if __name__ == "__main__":
    main()

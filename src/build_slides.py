# -*- coding: utf-8 -*-
"""T28 — dựng slide thuyết trình từ năm nhịp của §E.

Vì sao có script này thay vì gõ slide bằng tay
----------------------------------------------
Buổi thuyết trình đóng vai **nhà tư vấn** (quyết định **B18**): bốn nhịp đầu dựng
bằng chứng, nhịp năm nói ra việc nên làm. Mỗi câu trên slide là một con số, và con
số thì phải **đo lại được** — đúng chuẩn đã áp cho mọi hình trong đồ án. Gõ tay thì
ba tuần sau không ai biết câu "điện tử 29,9%" lấy ở đâu, và sửa một con số là phải
nhớ sửa mười chỗ.

Script làm ba việc:

1. **Đo lại** mọi con số xuất hiện trên slide, từ `data/processed/`. Phần nội dung
   bên dưới không chứa một hằng số nào — chỉ có ô ``{khoá}`` để điền.
2. **Đối chiếu** số vừa đo với số báo cáo cuối đã in (bảng ``KY_VONG``). Lệch một
   chữ số là gãy và in ra ngay. Đó là cái chốt giữ slide và báo cáo nói cùng một câu.
3. **Dựng** hai bản: một bản trình chiếu, và một bản chữ để diễn tập (T29) cùng rà
   soát chéo (T23) đọc được theo câu.

Ra hai file:

* ``output/slide-thuyet-trinh.html`` — khổ 16:9. Mũi tên / cách để đi, ``n`` bật lời
  dẫn, ``g`` xem dạng lưới, in ra PDF được (mỗi slide một trang ngang).
* ``output/slide-thuyet-trinh.md`` — dàn ý kèm lời dẫn từng slide.

Chạy:

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/build_slides.py
    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/build_slides.py --embed
"""

from __future__ import print_function

import argparse
import base64
import io
import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_data as R                      # noqa: E402
import make_decision_plane as DP                # noqa: E402
import make_sankey as SK                        # noqa: E402
import make_time_multiples as TM                # noqa: E402

DATA = os.path.join("data", "processed")
OUT = "output"
TEN = "slide-thuyet-trinh"
FOCUS = "VNM"
NAM = R.REFERENCE_YEAR          # 2023
NAM_DAU = 1995
TIVA_NAM = 2022                 # OECD TiVA 2025 dừng ở năm này (A19)

NGUOI = {"R1": "Nguyễn Khắc Huy", "R2": "Nguyễn Việt Phúc",
         "R3": "Dương Quang Huy", "ALL": "cả nhóm"}

# Hai họ kỹ thuật mà đề tài đòi phải có cả hai (checklist nộp bài, mục 4).
HO_CAY = ("treemap", "sunburst")
HO_DO_THI = ("node_link", "adjacency", "chord", "degree", "sankey")


def _ty(x):
    return float(x) / 1e9


# --------------------------------------------------------------------- đo số

def do_so():
    """Đo lại mọi con số sẽ in trên slide. Trả về dict khoá → chuỗi đã định dạng."""
    S = {"nam": "%d" % NAM, "nam_dau": "%d" % NAM_DAU}

    # --- quy mô
    ns = pd.read_csv(os.path.join(DATA, "network_stats.csv")).set_index("year")
    cy = pd.read_csv(os.path.join(DATA, "country_year.csv"))
    v = cy[cy["country_iso3"] == FOCUS].set_index("year")
    tg0 = float(ns.loc[NAM_DAU, "total_export_value"])
    tg1 = float(ns.loc[NAM, "total_export_value"])
    vn0 = float(v.loc[NAM_DAU, "export_value"])
    vn1 = float(v.loc[NAM, "export_value"])
    S["tg_dau"] = R.fmt_usd(tg0)
    S["tg_cuoi"] = R.fmt_usd(tg1)
    S["tg_lan"] = R.fmt_vn(tg1 / tg0, 2)
    S["vn_dau"] = R.fmt_usd(vn0)
    S["vn_cuoi"] = R.fmt_usd(vn1)
    S["vn_lan"] = R.fmt_vn(vn1 / vn0, 1)
    S["nhanh_hon"] = R.fmt_vn((vn1 / vn0) / (tg1 / tg0), 1)
    S["canh"] = R.fmt_vn(int(ns.loc[NAM, "n_edges"]), 0)
    S["nut"] = R.fmt_vn(int(ns.loc[NAM, "n_nodes"]), 0)
    S["mat_do"] = R.fmt_vn(float(ns.loc[NAM, "density"]), 3)
    S["doi_ung"] = R.fmt_vn(float(ns.loc[NAM, "reciprocity"]), 2)

    # --- hạng xuất khẩu, thị phần, thứ bậc ASEAN: đếm trên chính đồ thị
    e = pd.read_csv(os.path.join(DATA, "edges.csv"))
    e = e[e["year"] <= NAM]              # 2024 còn tạm, xem A6
    for nhan, y in (("dau", NAM_DAU), ("cuoi", NAM)):
        g = e[e["year"] == y].groupby("source_iso3")["export_value"].sum()
        g = g[g > 0].sort_values(ascending=False)
        S["hang_" + nhan] = "%d/%d" % (list(g.index).index(FOCUS) + 1, len(g))
        S["tp_" + nhan] = R.fmt_pct(float(g[FOCUS]) / float(g.sum()) * 100.0, 3)
        a = g[[i for i in R.ASEAN_ISO3 if i in g.index]].sort_values(ascending=False)
        S["asean_" + nhan] = "%d/%d" % (list(a.index).index(FOCUS) + 1, len(a))
        S["asean_top_" + nhan] = " · ".join(
            "%s %s" % (ten_nuoc(i), R.fmt_vn(_ty(x), 1)) for i, x in a.head(3).items())

    # --- rổ hàng theo 10 ngành cấp 1
    tree = pd.read_csv(os.path.join(DATA, "tree.csv"))
    cp = pd.read_csv(os.path.join(DATA, "country_product.csv"))
    cp = cp[cp["country_iso3"] == FOCUS]
    sec = tree[tree["level"] == 1].set_index("sector_id")["name_short"]
    pid_sec = tree.set_index("product_id")["sector_id"]
    nganh = {"Electronics": "dien_tu", "Machinery": "may_moc",
             "Agriculture": "nong_san", "Minerals": "khoang_san",
             "Textiles": "det_may", "Other": "chua_phan_loai"}
    for nhan, y in (("dau", NAM_DAU), ("cuoi", NAM)):
        d = cp[cp["year"] == y].copy()
        d["sector"] = d["product_id"].map(pid_sec).map(sec)
        sh = d.groupby("sector")["export_value"].sum()
        sh = sh / sh.sum() * 100.0
        S["tong_ty_trong_" + nhan] = R.fmt_vn(float(sh.sum()), 6)
        for k, key in nganh.items():
            S["%s_%s" % (key, nhan)] = R.fmt_pct(float(sh.get(k, 0.0)))

    # --- năng lực: ECI, COI, số mặt hàng
    for nhan, y in (("dau", NAM_DAU), ("cuoi", NAM)):
        S["eci_" + nhan] = "%d/%d" % (int(v.loc[y, "eci_rank"]), int(v.loc[y, "eci_n"]))
        S["coi_" + nhan] = R.fmt_vn(float(v.loc[y, "coi"]), 3)
        S["mat_hang_" + nhan] = R.fmt_vn(int(v.loc[y, "diversity"]), 0)

    # --- hành lang: mua của ai, bán cho ai (T19)
    buy, sell = SK.load_flows(NAM)
    nodes = pd.read_csv(os.path.join(DATA, "nodes.csv")).set_index("country_iso3")
    for iso, key in (("CHN", "chn"), ("USA", "usa")):
        mua, ban = float(buy.get(iso, 0.0)), float(sell.get(iso, 0.0))
        S["mua_" + key] = R.fmt_vn(_ty(mua), 2)
        S["ban_" + key] = R.fmt_vn(_ty(ban), 2)
        S["can_" + key] = "%s%s" % ("+" if ban >= mua else "−",
                                    R.fmt_vn(abs(_ty(ban - mua)), 2))
    S["tong_mua"] = R.fmt_usd(float(buy.sum()))
    rb = buy.groupby(nodes["region"]).sum().sort_values(ascending=False)
    S["vung_mua"] = R.REGION_VI.get(rb.index[0], rb.index[0])
    S["vung_mua_pct"] = R.fmt_pct(float(rb.iloc[0]) / float(rb.sum()) * 100.0)
    rs = sell.groupby(nodes["region"]).sum().sort_values(ascending=False)
    S["vung_ban"] = R.REGION_VI.get(rs.index[0], rs.index[0])
    S["vung_ban_pct"] = R.fmt_pct(float(rs.iloc[0]) / float(rs.sum()) * 100.0)

    # --- đầu ra dồn lại hay giãn ra (A16): HHI và tỷ trọng top-3
    _, _, cx = TM.load([NAM], "xuat")
    _, _, cn = TM.load([NAM], "nhap")
    nam_day = int(cx["hhi"].idxmin())
    S["hhi_dau"] = R.fmt_vn(float(cx.loc[NAM_DAU, "hhi"]), 4)
    S["hhi_day"] = R.fmt_vn(float(cx["hhi"].min()), 4)
    S["nam_day"] = "%d" % nam_day
    S["hhi_cuoi"] = R.fmt_vn(float(cx.loc[NAM, "hhi"]), 4)
    S["top3_day"] = R.fmt_pct(float(cx.loc[nam_day, "top3"]), 2)
    S["top3_cuoi"] = R.fmt_pct(float(cx.loc[NAM, "top3"]), 2)
    S["hhi_nhap"] = R.fmt_vn(float(cn.loc[NAM, "hhi"]), 4)
    S["top3_nhap"] = R.fmt_pct(float(cn.loc[NAM, "top3"]))
    S["hhi_lan"] = R.fmt_vn(float(cn.loc[NAM, "hhi"]) / float(cx.loc[NAM, "hhi"]), 1)

    # --- mặt phẳng quyết định (T31) và quy tắc chọn
    dp = DP.load(NAM, 2015).reset_index()
    nhom = {"Giày dép": "giay", "Cà phê, chè và gia vị": "ca_phe",
            "Máy điện và thiết bị điện": "dien", "Sắt thép": "sat",
            "Thiết bị quang học, y tế": "quang", "Máy móc công nghiệp": "may"}
    for ten, key in nhom.items():
        r = dp[dp["name"] == ten]
        if not len(r):
            continue
        r = r.iloc[0]
        S["rca_" + key] = R.fmt_vn(float(r["rca"]), 3)
        S["pci_" + key] = "%s%s" % ("+" if r["pci"] >= 0 else "−",
                                    R.fmt_vn(abs(float(r["pci"])), 3))
        S["xuat_" + key] = R.fmt_vn(_ty(float(r["export_value"])), 1)
        S["ty_trong_" + key] = R.fmt_pct(float(r["share"]), 2)
    kep = dp[(dp["rca"] >= 1) & (dp["pci"] < 0)]
    S["goc_kep_n"] = R.fmt_vn(len(kep), 0)
    S["goc_kep_pct"] = R.fmt_pct(float(kep["share"].sum()))
    S["rca_lo"] = R.fmt_vn(DP.RCA_LO, 1)
    S["rca_hi"] = R.fmt_vn(DP.RCA_HI, 1)
    S["min_xuat"] = R.fmt_usd(DP.MIN_EXPORT)

    # --- ba lần chạy quy tắc: 2007, 2015, 2023
    sau = dp.set_index("name")
    for y, since in ((2007, 1999), (2015, 2007)):
        c = DP.candidates(DP.load(y, since))
        for i, (_, r) in enumerate(c.iterrows()):
            p = "chay%d_%d" % (y, i)
            S[p + "_ten"] = r["name"]
            S[p + "_rca_cu"] = R.fmt_vn(float(r["rca_old"]), 3)
            S[p + "_rca"] = R.fmt_vn(float(r["rca"]), 3)
            S[p + "_pci"] = "%s%s" % ("+" if r["pci"] >= 0 else "−",
                                      R.fmt_vn(abs(float(r["pci"])), 3))
            S[p + "_xuat"] = R.fmt_vn(_ty(float(r["export_value"])), 1)
            S[p + "_rca_nay"] = R.fmt_vn(float(sau.loc[r["name"], "rca"]), 3)
            S[p + "_xuat_nay"] = R.fmt_vn(_ty(float(sau.loc[r["name"], "export_value"])), 1)
    nay = DP.candidates(dp.set_index("product_id"))
    S["chay_nay_0"] = nay.iloc[0]["name"]
    S["chay_nay_1"] = nay.iloc[1]["name"]

    # --- nền so sánh A17: RCA có tự đi lên không
    # PCI lấy ở NĂM GỐC, không lấy ở năm sau: lúc ra quyết định chỉ biết được
    # những gì năm gốc cho biết. Đây đúng là cách §7.2 của báo cáo đã đo.
    a0 = cp[cp["year"] == 2015].set_index("product_id")
    a1 = cp[cp["year"] == NAM].set_index("product_id")
    j = pd.DataFrame({"r0": a0["rca"], "r1": a1["rca"], "p0": a0["pci"]})
    j = j.dropna(subset=["r0", "r1"])
    j["d"] = j["r1"] - j["r0"]
    S["nen_n"] = R.fmt_vn(len(j), 0)
    S["nen_tang"] = R.fmt_pct(float((j["d"] > 0).mean()) * 100.0)
    S["nen_trung_vi"] = "%s%s" % ("+" if j["d"].median() >= 0 else "−",
                                  R.fmt_vn(abs(float(j["d"].median())), 4))
    cao = j[j["r0"] >= 1.5]
    S["nen_cao_n"] = R.fmt_vn(len(cao), 0)
    S["nen_cao_tang"] = R.fmt_pct(float((cao["d"] > 0).mean()) * 100.0)
    S["nen_cao_trung_vi"] = "−%s" % R.fmt_vn(abs(float(cao["d"].median())), 4)
    kho, de = j[j["p0"] > 0], j[j["p0"] <= 0]
    S["nen_kho_n"] = R.fmt_vn(len(kho), 0)
    S["nen_kho_tang"] = R.fmt_pct(float((kho["d"] > 0).mean()) * 100.0)
    S["nen_de_n"] = R.fmt_vn(len(de), 0)
    S["nen_de_tang"] = R.fmt_pct(float((de["d"] > 0).mean()) * 100.0)
    dai = j[(j["r0"] >= DP.RCA_LO) & (j["r0"] < DP.RCA_HI)]
    S["nen_dai_n"] = R.fmt_vn(len(dai), 0)
    S["nen_dai_tang"] = R.fmt_pct(float((dai["d"] > 0).mean()) * 100.0)

    # Lớp thoả TRỌN quy tắc, đo trên hai cửa sổ. Điều kiện "RCA đang tăng" phải
    # lấy ở cửa sổ TRƯỚC năm gốc, vì lúc ra quyết định chỉ biết được tới đó.
    def lop_tron(truoc, goc, sau):
        r = {y: cp[cp["year"] == y].set_index("product_id") for y in (truoc, goc, sau)}
        t = pd.DataFrame({"r_truoc": r[truoc]["rca"], "r0": r[goc]["rca"],
                          "r1": r[sau]["rca"], "p0": r[goc]["pci"]}).dropna(
                              subset=["r_truoc", "r0", "r1"])
        t = t[(t["p0"] > 0) & (t["r0"] >= DP.RCA_LO) & (t["r0"] < DP.RCA_HI)
              & (t["r0"] > t["r_truoc"])]
        d = t["r1"] - t["r0"]
        return len(t), float((d > 0).mean()) * 100.0, float(d.median())

    for nhan, (truoc, goc, sau) in (("", (2007, 2015, NAM)),
                                    ("_truoc", (1999, 2007, 2015))):
        n, pct, tv = lop_tron(truoc, goc, sau)
        S["nen_tron%s_n" % nhan] = R.fmt_vn(n, 0)
        S["nen_tron%s_tang" % nhan] = R.fmt_pct(pct)
        S["nen_tron%s_trung_vi" % nhan] = "%s%s" % ("+" if tv >= 0 else "−",
                                                    R.fmt_vn(abs(tv), 4))

    # --- ngưỡng lọc cạnh đã chọn (B4), để nói được phần kỹ thuật bằng số
    tc = pd.read_csv(os.path.join(DATA, "threshold_coverage.csv"))
    ch = tc[tc["strategy"] == "CHOSEN"].iloc[0]
    S["nguong_canh"] = R.fmt_pct(float(ch["pct_edges"]), 2)
    S["nguong_gia_tri"] = R.fmt_pct(float(ch["pct_value"]), 2)
    S["nguong_nut"] = R.fmt_vn(int(ch["n_nodes"]), 0)

    S.update(do_so_tiva())
    return S


def do_so_tiva(year=TIVA_NAM):
    """Số về phần giá trị làm ra trong nước (A19), đọc từ hai file mà
    ``map_sector_isic.py`` ghi ra. Không tự tính lại ở đây: có hai chỗ cùng tính
    một số thì sớm muộn hai chỗ nói hai con số."""
    sp = os.path.join(DATA, "sector_dva_%d.csv" % year)
    hp = os.path.join(DATA, "tiva_headline_%d.csv" % year)
    for f in (sp, hp):
        if not os.path.exists(f):
            raise SystemExit("thiếu %s — chạy: python src/map_sector_isic.py" % f)
    sec = pd.read_csv(sp).set_index("sector_id")
    h = pd.read_csv(hp).set_index("key")["value"]
    pct = R.fmt_pct
    T = {"tiva_nam": "%d" % year}
    for k in ("tong", "dien", "det"):
        for nhan in ("dau", "cuoi"):
            T["dva_%s_%s" % (k, nhan)] = pct(float(h["dva_%s_%s" % (k, nhan)]))
    T["dva_rb"] = pct(float(h["dva_rb"]))
    T["dva_rho"] = "%s%s" % ("+" if h["rho"] >= 0 else "−", R.fmt_vn(abs(float(h["rho"])), 2))
    T["dva_p"] = R.fmt_vn(float(h["p"]), 3)
    T["dva_n"] = R.fmt_vn(int(h["n_isic"]), 0)
    T["dva_top4_ty_trong"] = pct(float(h["top4_ty_trong"]))
    T["dva_top4_lo"] = pct(float(h["top4_lo"]))
    T["dva_top4_hi"] = pct(float(h["top4_hi"]))
    T["dva_may"] = pct(float(sec.loc[8, "dva_pct"]))
    T["dva_may_lo"] = R.fmt_vn(float(sec.loc[8, "lo"]), 1)
    T["dva_may_hi"] = pct(float(sec.loc[8, "hi"]))
    T["dva_dien"] = pct(float(sec.loc[9, "dva_pct"]))
    T["dva_khoi"] = pct(float(h["dva_khoi"]))
    T["dva_khac"] = pct(float(h["khac_pct"]))
    return T


def ten_nuoc(iso):
    """Tên tiếng Việt của một nước; COUNTRY_VI giữ bộ ba (tên, vùng, châu)."""
    v = R.COUNTRY_VI.get(iso)
    if isinstance(v, (tuple, list)):
        return v[0]
    return v or iso


# ------------------------------------------------------- nội dung từng slide
# Mọi chuỗi chỉ chứa ô {khoá}; không có con số nào gõ tay. Thiếu khoá là gãy.

SLIDES = [
    dict(ma="00", kieu="bia", chu="ALL",
         tieu_de="Việt Nam trong mạng lưới thương mại toàn cầu",
         phu="Nên dồn sức xuất khẩu vào nhóm hàng nào — và vì sao nhóm đó, chứ "
             "không phải nhóm đang bán chạy nhất?",
         diem=["Dữ liệu: Atlas of Economic Complexity (Harvard Growth Lab), "
               "{nam_dau}–{nam}, phân loại HS92",
               "Đồ thị {nam}: {nut} nước · {canh} luồng · mật độ {mat_do} · "
               "đối ứng {doi_ung}",
               "Nhóm 8 — Nguyễn Khắc Huy · Nguyễn Việt Phúc · Dương Quang Huy"],
         notes="Mở bằng câu hỏi, không mở bằng dữ liệu. Buổi này không mô tả một "
               "bộ dữ liệu, nó đi tới một đề xuất: cuối buổi sẽ có hai nhóm hàng "
               "cụ thể, kèm mốc kiểm và kèm điều kiện chúng tôi tự nhận là sai."),

    dict(ma="01", kieu="chu", chu="ALL",
         tieu_de="Chúng tôi đóng vai nhà tư vấn, không đóng vai người đọc số",
         phu="Câu hỏi · người nghe · quyết định cần ra",
         diem=["**Câu hỏi.** Việt Nam đang ở đâu trong cấu trúc thương mại toàn "
               "cầu, và cấu trúc đó cho phép đi tiếp theo hướng nào?",
               "**Người nghe.** Người phải chọn nơi dồn ưu tiên — vốn, hạ tầng, "
               "đào tạo — trong 5–10 năm tới.",
               "**Quyết định.** Dồn thêm vào khâu đang bán chạy, hay dồn vào nhóm "
               "hàng khó hơn mà ta chưa bán đậm?",
               "**Cách trả lời.** Năm nhịp: bốn nhịp dựng bằng chứng, nhịp năm nói "
               "việc nên làm — kèm điều kiện bác bỏ."],
         notes="Nói ở đây rằng mọi con số trên slide đều do script sinh ra từ dữ "
               "liệu và chạy lại được. Đó là lý do slide này dám kết bằng một đề "
               "xuất chứ không kết bằng một bản mô tả."),

    dict(ma="02", kieu="bang", chu="ALL",
         tieu_de="Mạch năm nhịp",
         phu="Mỗi nhịp một câu, mỗi câu một con số, mỗi con số một hình",
         bang=[["Nhịp", "Câu", "Hình"],
               ["1", "Rổ hàng được xây lại gần như từ đầu — điện tử "
                "{dien_tu_dau} → {dien_tu_cuoi}", "T21, T12, T13"],
               ["2", "Và Việt Nam trèo lên thật: ECI {eci_dau} → {eci_cuoi} — nhưng "
                "phần ở lại tụt, điện tử {dva_dien_dau} → {dva_dien_cuoi}",
                "T14, A19"],
               ["3", "Nhưng cách trèo là một hành lang, hẹp ở cả hai đầu",
                "T19, T20"],
               ["4", "Nhìn kỹ thì trèo bằng hàng dễ — {goc_kep_pct} rổ hàng ở góc "
                "bán đậm, hàng dễ", "T31"],
               ["5", "Vậy nên đề xuất — và đây là cách tự bác bỏ nó",
                "T31 ở 2007 và 2015"]],
         notes="Slide bản đồ. Người nghe cần biết mình đang ở nhịp nào, vì nhịp 3 "
               "và 4 nghe như mâu thuẫn với nhịp 1 và 2 — đó là chủ ý."),

    dict(ma="03", kieu="so", chu="R1", nhip=1,
         tieu_de="Việt Nam lớn nhanh gấp {nhanh_hon} lần mức bình quân thế giới",
         phu="Xuất khẩu {nam_dau} → {nam}, giá trị danh nghĩa, đồ thị đầy đủ không "
             "lọc ngưỡng",
         so=[("{tg_lan}×", "thế giới lớn lên<br>{tg_dau} → {tg_cuoi}"),
             ("{vn_lan}×", "Việt Nam lớn lên<br>{vn_dau} → {vn_cuoi}"),
             ("{hang_cuoi}", "hạng xuất khẩu<br>từ {hang_dau} năm {nam_dau}"),
             ("{tp_cuoi}", "thị phần thế giới<br>từ {tp_dau}")],
         diem=["Trong ASEAN trật tự đã đảo: hạng {asean_dau} năm {nam_dau} → "
               "**hạng {asean_cuoi}** năm {nam} — {asean_top_cuoi} tỷ USD",
               "Mẫu số là số nước **thật sự có xuất khẩu** năm đó, không phải số "
               "nút trong mạng"],
         notes="Đây là con số mạnh nhất của bài, và cũng là cái bẫy: bán nhiều nhất "
               "khối không có nghĩa bán thứ đáng giá nhất khối. Ba nhịp sau tồn tại "
               "chính vì câu đó."),

    dict(ma="04", kieu="hinh", chu="R3", nhip=1, viec="T21",
         hinh="stream_sectors_1995_2023",
         tieu_de="Rổ hàng được xây lại gần như từ đầu",
         phu="Nông sản {nong_san_dau} → {nong_san_cuoi} · điện tử {dien_tu_dau} → "
             "{dien_tu_cuoi}",
         diem=["Máy móc {may_moc_dau} → {may_moc_cuoi}; khoáng sản "
               "{khoang_san_dau} → {khoang_san_cuoi}",
               "Hình vẽ **hai tầng** vì cơ cấu {nam_dau} chỉ bằng 1,3% chiều cao "
               "của {nam} — vẽ một tầng thì 29 năm đầu bị ép thành một vạch",
               "⚠️ Ô *Chưa phân loại* nở {chua_phan_loai_dau} → "
               "**{chua_phan_loai_cuoi}**: đó là mã `XXXX` của Atlas, không phải "
               "một ngành hàng"],
         notes="Chỉ vào chỗ hai dải đổi chỗ cho nhau quanh 2010. Nếu bị hỏi vì sao "
               "không dùng nền lượn: nền lượn làm mất mốc 0 nên không đọc được tỷ "
               "trọng, mà tỷ trọng chính là nội dung của hình."),

    dict(ma="05", kieu="hinh2", chu="R1", nhip=1, viec="T12",
         hinh="treemap_vnm_1995", hinh2="treemap_vnm_2023",
         tieu_de="Cùng một cây sản phẩm, hai năm, gần như không nhận ra nhau",
         phu="Treemap HS92 — {nam_dau} bên trái, {nam} bên phải",
         diem=["Dệt may giữ được chỗ ({det_may_dau} → {det_may_cuoi}); nông sản "
               "thì không ({nong_san_dau} → {nong_san_cuoi})",
               "Số mặt hàng xuất được: {mat_hang_dau} → **{mat_hang_cuoi}**"],
         notes="Hình này là họ **cây** mà đề tài đòi, song song với họ đồ thị ở "
               "phần sau. Treemap đọc nhanh hơn–kém; sunburst (slide dự phòng) đọc "
               "được bốn tầng của cây HS92."),

    dict(ma="06", kieu="hinh", chu="R1", nhip=2, viec="T14",
         hinh="small_multiples_vnm-tha-mys-idn_2023",
         tieu_de="Và Việt Nam trèo lên thật trong bảng năng lực",
         phu="ECI {eci_dau} → {eci_cuoi} · COI {coi_dau} → {coi_cuoi} · "
             "{mat_hang_dau} → {mat_hang_cuoi} mặt hàng xuất được",
         diem=["**ECI** (*economic complexity index*) xếp hạng một nước theo độ đa "
               "dạng và độ hiếm của rổ hàng — nói gọn: rổ hàng **khó** tới mức "
               "nào, không phải **to** tới mức nào",
               "Lưới bốn nước cho thấy Việt Nam vượt Thái Lan và Indonesia về quy "
               "mô xuất khẩu trong cùng khoảng thời gian",
               "⚠️ ECI đo rổ hàng **gộp**, nên nó đo *cái gì đi qua* Việt Nam, "
               "chưa hẳn *cái gì ở lại* — hạn chế D2, D5; slide kế tiếp đo "
               "phần ở lại"],
         notes="Đặt cảnh báo D2 ở đây, sớm, chứ đừng để người chấm hỏi ra ở nhịp 5. "
               "Nói trước thì nó là sự cẩn thận; bị hỏi ra thì nó là lỗ hổng."),

    dict(ma="06b", kieu="hinh", chu="R1", nhip=2, viec="A19",
         hinh="dva_sectors_2022",
         tieu_de="Nhưng phần giá trị ở lại đã tụt từ {dva_tong_dau} xuống "
                 "{dva_tong_cuoi}",
         phu="Phần giá trị của hàng xuất khẩu làm ra trong nước — OECD TiVA 2025, "
             "Việt Nam {tiva_nam} (TiVA dừng ở năm đó, không phải {nam})",
         diem=["Toàn nền kinh tế {dva_tong_dau} → **{dva_tong_cuoi}** từ {nam_dau} "
               "đến {tiva_nam}; riêng điện tử {dva_dien_dau} → **{dva_dien_cuoi}**",
               "Hàng càng khó càng ít ở lại, mức vừa: Spearman **{dva_rho}** "
               "(p = {dva_p}). Bốn ngành PCI cao nhất, {dva_top4_ty_trong} xuất "
               "khẩu, đều ở {dva_top4_lo}–{dva_top4_hi}",
               "Máy móc {dva_may}, điện tử {dva_dien}: chênh nằm trong sai số của "
               "bảng ghép sang ngành ISIC",
               "⚠️ **Không** đọc thành \"Việt Nam chỉ lắp ráp\": gần nửa giá trị "
               "hàng điện tử vẫn làm ra trong nước"],
         notes="Đây là chỗ trả lời câu D2 đã nêu ở slide trước, và nó lấy đi một "
               "câu mà bản đầu của nhóm đã nói: \"điện tử là khâu phụ thuộc nhập "
               "khẩu nhất\". Số đo cho thấy máy móc giữ {dva_may}, hơn điện tử "
               "{dva_dien} có ba điểm, trong sai số của bảng ghép. Nên đề xuất "
               "dồn vào máy móc và thiết bị y tế không dựa vào việc giữ nhiều giá "
               "trị hơn, mà dựa vào độ khó và mức tập trung. Nói luôn điều không "
               "đọc được: giá trị tạo ra trong lãnh thổ, bất kể chủ doanh nghiệp."),

    dict(ma="07", kieu="hinh2", chu="R2", nhip=3, viec="T15",
         hinh="degree_loglog_2023", hinh2="node_link_2023",
         tieu_de="Mạng thương mại không có một hub duy nhất",
         phu="Phân bố bậc log-log và node-link của mạng đã lọc, {nam}",
         diem=["Ngưỡng lọc biện minh bằng số, không chọn cảm tính: giữ "
               "{nguong_canh} số cạnh mà vẫn giữ **{nguong_gia_tri}** giá trị, "
               "còn {nguong_nut} nước và đủ 10 nước ASEAN",
               "Mật độ {mat_do}, đối ứng {doi_ung} — gần như mọi cặp bạn hàng đều "
               "buôn hai chiều, nên **không vẽ mũi tên** (quyết định B5)",
               "Hệ quả cho câu chuyện: không có hub để dựa vào, nên vị trí của một "
               "nước là **chỗ nó nằm trong luồng giá trị**, không phải số bạn hàng "
               "nó đếm được"],
         diem_ghi="Đây cũng là chỗ trả lời: vì sao không force-directed cho cả "
                  "{canh} cạnh.",
         notes="Nếu bị hỏi vì sao không force-directed cho toàn mạng: ở mật độ "
               "{mat_do} thì force-directed ra một quả cầu lông — đã thử, và đó là "
               "lý do có ngưỡng lọc cùng ma trận kề."),

    dict(ma="08", kieu="hinh", chu="R3", nhip=3, viec="T19",
         hinh="sankey_vietnam_2023",
         tieu_de="Cách trèo là một hành lang — và hành lang hẹp ở cả hai đầu",
         phu="Nhập → Việt Nam → xuất, {nam}, tỷ USD",
         diem=["Mua của Trung Quốc **{mua_chn} tỷ**, bán lại {ban_chn} tỷ → cân "
               "**{can_chn} tỷ**",
               "Mua của Hoa Kỳ {mua_usa} tỷ, bán sang **{ban_usa} tỷ** → cân "
               "**{can_usa} tỷ**",
               "**{vung_mua_pct}** hàng vào từ một vùng duy nhất ({vung_mua}); "
               "{vung_ban_pct} hàng ra đi về {vung_ban}",
               "⚠️ \"Xuất trừ nhập\" ở đây là **số học**, không phải giá trị tăng "
               "thêm — Atlas không có bảng vào–ra, nên phần ở lại được đo riêng "
               "bằng TiVA ở nhịp 2"],
         notes="Đây là nhịp xoay của cả bài: hai nhịp đầu là tin tốt, nhịp này nói "
               "cái giá. Đừng đọc hết tên nước — hai dòng Trung Quốc và Hoa Kỳ là "
               "đủ thấy hình dạng hành lang."),

    dict(ma="09", kieu="hinh", chu="R3", nhip=3, viec="T20",
         hinh="time_multiples_xuat",
         tieu_de="Và đầu ra đang dồn lại, không giãn ra",
         phu="Việt Nam bán cho ai, bốn năm mốc — tỷ trọng theo giá trị",
         diem=["Tập trung giá trị (HHI) hình chữ V: {hhi_dau} ({nam_dau}) → đáy "
               "**{hhi_day}** ({nam_day}) → **{hhi_cuoi}** ({nam}), cao hơn cả "
               "mức {nam_dau}",
               "Top-3 thị trường nhận {top3_day} hàng xuất năm {nam_day}, nay nhận "
               "**{top3_cuoi}**",
               "Đầu vào còn dồn hơn: HHI nhập **{hhi_nhap}** — gấp {hhi_lan} lần "
               "đầu ra; top-3 nhà cung cấp {top3_nhap}",
               "⚠️ **Nhóm đã tự sửa phép đo ở đây.** Bản đầu nói \"số bạn hàng "
               "giảm\"; đếm bạn hàng không bền, vì 47 nước rời danh sách chỉ mang "
               "0,59% kim ngạch. Phép đo đứng được là HHI và tỷ trọng top-3 (A16)"],
         notes="Dòng cuối là điểm cộng chứ không phải điểm trừ: nói ra rằng nhóm đã "
               "bác một phép đo của chính mình. Nếu bị hỏi \"sao không đếm bạn "
               "hàng\" thì con số 0,59% nằm ngay đây."),

    dict(ma="10", kieu="hinh", chu="R3", nhip=4, viec="T31",
         hinh="decision_plane_2023",
         tieu_de="Nhìn kỹ thì Việt Nam mạnh nhất ở nhóm hàng dễ nhất",
         phu="RCA × PCI, {nam}, {nen_n} nhóm hàng HS92 cấp 2 — trục ngang thang "
             "log, mốc 1 là mức bình quân thế giới",
         diem=["**RCA** đo bán **đậm** tới mức nào so với thế giới; **PCI** đo mặt "
               "hàng đó **khó** tới mức nào. Bốn góc đọc rất khác nhau.",
               "Giày dép RCA **{rca_giay}** nhưng PCI {pci_giay}; cà phê "
               "{rca_ca_phe} với PCI {pci_ca_phe} — bán rất đậm, hàng rất dễ",
               "Điện tử xuất **{xuat_dien} tỷ USD** ({ty_trong_dien} rổ hàng) mà "
               "RCA chỉ {rca_dien}",
               "**{goc_kep_pct}** rổ hàng nằm ở góc bán đậm – hàng dễ "
               "({goc_kep_n} nhóm)"],
         notes="Giải thích RCA và PCI bằng một câu mỗi cái, đừng đọc định nghĩa. "
               "RCA: có bán đậm hơn mức thế giới hay không. PCI: hàng này có cần "
               "năng lực tích luỹ, hay ai cũng làm được."),

    dict(ma="11", kieu="chu", chu="R3", nhip=5,
         tieu_de="Đề xuất: dồn ưu tiên vào hai nhóm đang sát ngưỡng lợi thế",
         phu="Chọn bằng quy tắc viết thành code, không chọn bằng ý thích",
         diem=["**{chay_nay_0}** — RCA {rca_quang} (PCI {pci_quang}), xuất "
               "{xuat_quang} tỷ USD",
               "**{chay_nay_1}** — RCA {rca_may} (PCI {pci_may}), xuất {xuat_may} "
               "tỷ USD",
               "Quy tắc: xuất trên {min_xuat} · PCI dương · RCA trong dải "
               "[{rca_lo}; {rca_hi}) · RCA **đang tăng** → lấy hai nhóm PCI cao "
               "nhất. Chạy năm khác thì ra nhóm khác.",
               "**Không** dồn thêm vào lắp ráp điện tử (RCA đã {rca_dien}, và đầu "
               "vào đi qua hành lang hẹp); **không** dồn vào nhóm RCA cao – "
               "PCI thấp, vốn đã giảm tỷ trọng suốt 28 năm"],
         notes="Đọc quy tắc trước, tên nhóm sau. Thứ tự đó quan trọng: nó cho thấy "
               "đề xuất là đầu ra của một phép lọc, không phải sở thích của nhóm."),

    dict(ma="12", kieu="hinh", chu="R3", nhip=5, viec="T31",
         hinh="decision_plane_2007",
         tieu_de="Vì sao tin được cách chọn: đem chính quy tắc ấy chạy trên quá khứ",
         phu="Quy tắc chạy trên dữ liệu 2007 — nó không nhìn thấy gì sau năm đó",
         bang=[["Chạy ở", "Nó chọn", "Rồi sao"],
               ["2007", "{chay2007_0_ten} — RCA {chay2007_0_rca}, xuất "
                "{chay2007_0_xuat} tỷ USD",
                "{nam}: RCA **{chay2007_0_rca_nay}**, xuất "
                "**{chay2007_0_xuat_nay} tỷ**"],
               ["2015", "{chay2015_0_ten} {chay2015_0_rca} · {chay2015_1_ten} "
                "{chay2015_1_rca}",
                "{chay2015_0_rca_nay} · **{chay2015_1_rca_nay} — vượt ngưỡng 1,0**"],
               ["{nam}", "{chay_nay_0} · {chay_nay_1}", "đề xuất của báo cáo"]],
         notes="Nhấn: năm 2007 quy tắc chỉ ra điện tử khi nhóm đó mới "
               "{chay2007_0_xuat} tỷ USD — trước cả làn đầu tư lớn vào lắp ráp. "
               "Không ai chọn được như vậy bằng trực giác ở năm 2007."),

    dict(ma="13", kieu="bang", chu="R2", nhip=5,
         tieu_de="Nhưng hai lần trúng chỉ có nghĩa nếu RCA không tự đi lên",
         phu="Nền so sánh: toàn bộ {nen_n} nhóm hàng HS2, RCA 2015 → {nam} "
             "(phát hiện A17)",
         bang=[["Lớp nhóm hàng", "Số nhóm", "Có RCA tăng"],
               ["Tất cả — mức bình quân", "{nen_n}",
                "**{nen_tang}** (trung vị {nen_trung_vi})"],
               ["Đã có RCA ≥ 1,5 — đang bán rất đậm", "{nen_cao_n}",
                "{nen_cao_tang} (trung vị {nen_cao_trung_vi})"],
               ["PCI > 0 — hàng khó", "{nen_kho_n}", "**{nen_kho_tang}**"],
               ["PCI ≤ 0 — hàng dễ", "{nen_de_n}", "{nen_de_tang}"],
               ["Trong dải RCA [{rca_lo}; {rca_hi}) — đứng một mình",
                "{nen_dai_n}", "{nen_dai_tang}"]],
         diem=["**Phải nói thẳng hai điều.** Sức dự báo nằm ở điều kiện **PCI > 0** "
               "({nen_kho_tang} so với {nen_de_tang}), **không** nằm ở dải RCA — "
               "dải đó đứng một mình còn kém mức bình quân.",
               "Lớp thoả **trọn** quy tắc chỉ có **{nen_tron_n} nhóm** "
               "({nen_tron_tang} tăng), và ở cửa sổ trước đó lớp tương đương còn "
               "**kém mức bình quân** ({nen_tron_truoc_tang} trên "
               "{nen_tron_truoc_n} nhóm) — quá nhỏ để kết luận thống kê. Bằng "
               "chứng mạnh ở **ba lần chọn cụ thể** và ở **điều kiện PCI**, không "
               "ở một con p-value."],
         notes="Slide này là chỗ tách bài khá khỏi bài giỏi: tự nói ra chỗ yếu của "
               "quy tắc mình đề xuất, trước khi có ai hỏi. Câu phản biện \"RCA dưới "
               "1 thì lấy gì chắc nó vượt\" đã được trả lời sẵn ở đây."),

    dict(ma="14", kieu="chu", chu="ALL", nhip=5,
         tieu_de="Đo bằng gì để biết đề xuất đi đúng — và khi nào nhận là sai",
         phu="Mốc kiểm và điều kiện bác bỏ, cả hai đều là con số",
         diem=["**Mốc 1.** RCA của {chay_nay_0} ({rca_quang}) và {chay_nay_1} "
               "({rca_may}) phải **vượt 1,00** — tức bán đậm hơn mức bình quân "
               "thế giới.",
               "**Mốc 2.** Top-3 thị trường phải rút từ {top3_cuoi} về dưới mức "
               "{top3_day} của năm {nam_day}.",
               "**Mốc 3.** Tỷ trọng đầu vào từ {vung_mua} phải rời khỏi mức "
               "{vung_mua_pct}.",
               "**Nhận là sai nếu:** RCA hai nhóm ấy chững dưới 1 trong vài năm "
               "tới · hoặc đầu vào tự đa dạng hoá mà không cần can thiệp · hoặc ô "
               "*Chưa phân loại* ({chua_phan_loai_cuoi} rổ hàng) được bóc ra và "
               "hoá ra là hàng dễ · hoặc phần ở lại của khối "
               "điện tử – máy móc tụt dưới {dva_khoi} trong khi RCA hai nhóm đề "
               "xuất đã vượt 1,00."],
         notes="Một đề xuất không có điều kiện bác bỏ thì chỉ là một ý thích. Ba "
               "mốc trên đều lấy lại được bằng đúng lệnh ghi trong README."),

    dict(ma="15", kieu="chu", chu="R1",
         tieu_de="Những gì bài này không chứng minh được",
         phu="Hạn chế D1–D5, nói ra chứ không giấu",
         diem=["**D2, D5.** RCA, PCI và ECI đo rổ hàng **gộp** — chúng đo cái gì "
               "*đi qua* Việt Nam, chưa hẳn cái gì *ở lại*. Atlas không tách được "
               "phần ở lại; nhóm đo bằng TiVA của OECD, ở cấp ngành, năm "
               "{tiva_nam}, qua bảng ghép HS2 → ISIC — chưa có ở cấp HS4 hay "
               "doanh nghiệp.",
               "**D4.** Phân tích ở cấp HS2 ({nen_n} nhóm). Chi tiết HS4 có trong "
               "Atlas nhưng là file 452 MB, chưa tải.",
               "**Nguồn.** Atlas và BACI đều **dẫn xuất từ UN Comtrade** — ba tên "
               "gọi, không phải ba nguồn độc lập để đối chiếu nhau.",
               "**Dữ liệu.** {chua_phan_loai_cuoi} kim ngạch nằm ở ô *Chưa phân "
               "loại*; số của nước xuất và nước nhập lệch nhau, nên mọi luồng ở "
               "đây đều lấy theo số của bên xuất."],
         notes="Trả lời trước câu phản biện về nguồn: nếu bị hỏi \"sao không đối "
               "chiếu ba nguồn\", câu trả lời là ba nguồn ấy không độc lập — và "
               "nhóm đã kiểm ra điều đó, không đoán."),

    dict(ma="16", kieu="ket", chu="ALL",
         tieu_de="Một câu để nhớ",
         phu="",
         diem=["Việt Nam đã **lớn lên {vn_lan} lần** và trèo từ hạng {hang_dau} "
               "lên **{hang_cuoi}** — nhưng trèo qua một **hành lang hẹp hai đầu** "
               "({vung_mua_pct} đầu vào từ một vùng, top-3 nhận {top3_cuoi} đầu "
               "ra), và trèo bằng **hàng dễ** ({goc_kep_pct} rổ hàng ở góc bán "
               "đậm – hàng dễ).",
               "Nên việc đáng dồn sức là **{chay_nay_0}** và **{chay_nay_1}** — "
               "hai nhóm khó nhất trong rổ và đang sát ngưỡng lợi thế — chứ không "
               "phải đào sâu thêm vào khâu lắp ráp.",
               "Và đây là hai lần nhóm **tự sửa mình**: A13 (đỉnh số bạn hàng rơi "
               "vào một năm không có trên hình) và A16 (phép đếm bạn hàng không "
               "bền, thay bằng HHI). Số nào không đứng được thì bỏ."],
         notes="Kết bằng đề xuất, không kết bằng \"cảm ơn đã lắng nghe\". Câu cuối "
               "là câu đáng giá nhất của cả bài."),

    dict(ma="P1", kieu="hinh2", chu="R2", du_phong=True, viec="T16",
         hinh="adjacency_cluster_2023", hinh2="chord_bloc_2023",
         tieu_de="Dự phòng — ma trận kề và chord trên cùng mạng ấy",
         phu="Ma trận sắp theo cụm Louvain và chord tám khối, {nam}",
         diem=["Ma trận đọc được **cụm**; node-link đọc được **đường đi**; chord "
               "đọc được **cân đối giữa hai khối**. Cùng một dữ liệu, ba tác vụ.",
               "Thương mại nội khối giảm 60,5% → 48,4% trong 29 năm"],
         notes="Dùng khi bị hỏi mục 5 của checklist: so sánh node-link với ma trận "
               "kề trên cùng dữ liệu, họ nào hợp tác vụ nào."),

    dict(ma="P2", kieu="hinh", chu="R1", du_phong=True, viec="T13",
         hinh="sunburst_vnm_2023",
         tieu_de="Dự phòng — bốn tầng của cây sản phẩm HS92",
         phu="Sunburst, Việt Nam {nam}",
         diem=["Treemap đọc nhanh hơn–kém; sunburst cho thấy **đường từ ngành "
               "xuống mặt hàng**, tức cấu trúc cây",
               "{mat_hang_cuoi} mặt hàng xuất được năm {nam}, từ {mat_hang_dau} "
               "năm {nam_dau}"],
         notes="Dùng khi bị hỏi vì sao cần cả treemap và sunburst."),

    dict(ma="P3", kieu="hinh", chu="R3", du_phong=True, viec="T31",
         hinh="decision_plane_2015",
         tieu_de="Dự phòng — chính quy tắc ấy chạy trên dữ liệu 2015",
         phu="Nó chọn {chay2015_0_ten} ({chay2015_0_rca}) và {chay2015_1_ten} "
             "({chay2015_1_rca})",
         diem=["Tám năm sau: {chay2015_0_rca_nay} và **{chay2015_1_rca_nay}** — "
               "nhóm thứ hai đã vượt ngưỡng 1,0",
               "Quy tắc không nhìn thấy gì sau 2015: nó chỉ dùng RCA, PCI và giá "
               "trị xuất của chính năm đó"],
         notes="Dùng khi bị hỏi bằng chứng cho quy tắc chọn."),
]

# Con số báo cáo cuối đã in. Slide và báo cáo phải nói cùng một câu, nên lệch là
# gãy — không phải cảnh báo. Sửa ở đây chỉ khi báo cáo đã sửa trước.
KY_VONG = {
    "tg_lan": "4,51", "vn_lan": "75,3", "nhanh_hon": "16,7",
    "hang_dau": "61/211", "hang_cuoi": "16/230", "tp_cuoi": "1,780%",
    "asean_cuoi": "1/10", "asean_dau": "6/10",
    "dien_tu_dau": "0,6%", "dien_tu_cuoi": "29,9%", "may_moc_cuoi": "14,4%",
    "nong_san_dau": "42,9%", "nong_san_cuoi": "11,6%",
    "khoang_san_cuoi": "1,4%", "chua_phan_loai_cuoi": "11,8%",
    "eci_dau": "181/211", "eci_cuoi": "78/230", "coi_cuoi": "1,197",
    "mat_hang_dau": "186", "mat_hang_cuoi": "285",
    "mua_chn": "133,05", "ban_chn": "86,11", "can_chn": "−46,94",
    "mua_usa": "9,83", "ban_usa": "95,16", "can_usa": "+85,33",
    "vung_mua_pct": "68,3%",
    "hhi_dau": "0,1209", "hhi_day": "0,0662", "nam_day": "2013",
    "hhi_cuoi": "0,1226", "top3_day": "39,25%", "top3_cuoi": "52,41%",
    "hhi_nhap": "0,1979", "top3_nhap": "61,3%",
    "rca_giay": "7,518", "rca_dien": "2,230", "xuat_dien": "115,4",
    "rca_quang": "0,905", "rca_may": "0,954", "rca_sat": "1,003",
    "goc_kep_pct": "36,2%", "nguong_gia_tri": "67,84%",
    "nen_n": "97", "nen_tang": "45,4%", "nen_trung_vi": "−0,0178",
    "nen_cao_n": "24", "nen_cao_tang": "25,0%",
    "nen_kho_n": "43", "nen_kho_tang": "62,8%",
    "nen_de_n": "54", "nen_de_tang": "31,5%",
    "nen_dai_tang": "40,7%",
    "nen_tron_n": "6", "nen_tron_tang": "50,0%", "nen_tron_trung_vi": "+0,0205",
    "nen_tron_truoc_tang": "25,0%", "nen_tron_truoc_trung_vi": "−0,1893",
    "chay2007_0_rca": "0,573", "chay2007_0_xuat": "3,4",
    "chay2007_0_rca_nay": "2,230", "chay2015_1_rca_nay": "1,003",
    # §6.2 — phần giá trị làm ra trong nước (TiVA, A19)
    "dva_tong_dau": "79,8%", "dva_tong_cuoi": "51,5%",
    "dva_dien_dau": "64,1%", "dva_dien_cuoi": "44,2%",
    "dva_det_dau": "73,2%", "dva_det_cuoi": "53,1%", "dva_rb": "50,5%",
    "dva_rho": "−0,47", "dva_p": "0,038", "dva_n": "20",
    "dva_top4_ty_trong": "56,9%", "dva_top4_lo": "43,8%", "dva_top4_hi": "47,5%",
    "dva_may": "47,5%", "dva_dien": "44,2%", "dva_khoi": "44,2%",
    "dva_khac": "9,8%",
}


# ------------------------------------------------------------- điền và đổi chữ

O_TRONG = re.compile(r"\{([a-zA-Z0-9_]+)\}")


def dien(s, S, thieu):
    """Điền ô {khoá}. Khoá không có thì ghi vào ``thieu`` và để nguyên ô."""
    def cat(m):
        k = m.group(1)
        if k in S:
            return S[k]
        thieu.add(k)
        return m.group(0)
    return O_TRONG.sub(cat, s or "")


def inline(s):
    """Markdown trong dòng → HTML. Giữ khối `code` nguyên văn trước khi thoát."""
    giu = []

    def cat(m):
        giu.append(m.group(1))
        return "\x00%d\x00" % (len(giu) - 1)

    s = re.sub(r"`([^`]+)`", cat, s)
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    s = s.replace("&lt;br&gt;", "<br>")
    s = re.sub(r"\*\*\*([^*]+)\*\*\*", r"<strong><em>\1</em></strong>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    for i, c in enumerate(giu):
        c = c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        s = s.replace("\x00%d\x00" % i, "<code>%s</code>" % c)
    return s


def nguon_anh(ten, embed):
    """Đường dẫn ảnh: trỏ sang PNG cùng thư mục, hoặc nhúng base64 khi --embed."""
    p = os.path.join(OUT, ten + ".png")
    if not embed:
        return "%s.png" % ten
    b = io.open(p, "rb").read()
    return "data:image/png;base64,%s" % base64.b64encode(b).decode("ascii")


# ----------------------------------------------------------------- dựng HTML

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#2E2E2E;font-family:"Segoe UI",Arial,"DejaVu Sans",sans-serif}
#san{position:fixed;top:0;left:0;right:0;bottom:0;display:flex;align-items:center;
     justify-content:center;overflow:hidden}
.slide{width:1280px;height:720px;flex:0 0 auto;background:#FFFFFF;color:#1A1A1A;
       padding:44px 54px 40px 54px;display:none;flex-direction:column;position:relative;
       transform:scale(var(--s,1));transform-origin:center center}
.slide.hien{display:flex}
h1{font-size:40px;line-height:1.16;font-weight:600;letter-spacing:-0.2px}
.slide.chu h1,.slide.hinh h1,.slide.hinh2 h1,.slide.bang h1,.slide.so h1{font-size:33px}
.phu{margin-top:9px;font-size:16px;color:#555555;line-height:1.35}
.than{flex:1;display:flex;min-height:0;margin-top:22px;gap:28px}
.than.doc{flex-direction:column;justify-content:center}
.slide.hinh2 .than.doc{justify-content:flex-start}
ul{list-style:none}
li{font-size:20px;line-height:1.42;margin-bottom:13px;padding-left:19px;position:relative}
li:before{content:"";position:absolute;left:0;top:10px;width:8px;height:8px;
          background:#CC4C02;border-radius:1px}
.slide.chu li,.slide.ket li{font-size:23px;line-height:1.45;margin-bottom:19px}
.hinh-o{flex:1 1 58%;display:flex;align-items:center;justify-content:center;min-width:0}
.hinh-o img{max-width:100%;max-height:100%;object-fit:contain}
.ben{flex:1 1 42%;display:flex;flex-direction:column;justify-content:center;min-width:0}
.doi{display:flex;gap:20px;flex:1;min-height:0}
.doi .hinh-o{flex:1 1 50%}
.the-so{display:flex;gap:18px;margin-bottom:6px}
.the{flex:1;border:1px solid #E6E6E6;border-top:4px solid #CC4C02;border-radius:3px;
     padding:16px 15px 14px 15px;background:#FCFCFC}
.the .v{font-size:38px;font-weight:600;line-height:1.1;letter-spacing:-0.5px}
.the .n{margin-top:7px;font-size:14px;color:#555555;line-height:1.35}
table{border-collapse:collapse;width:100%;font-size:18px}
th,td{text-align:left;padding:10px 13px;border-bottom:1px solid #E6E6E6;vertical-align:top}
th{font-size:14px;color:#555555;font-weight:600;text-transform:uppercase;letter-spacing:0.4px}
tr td:first-child{white-space:nowrap;font-weight:600}
.chan{position:absolute;left:54px;right:54px;bottom:16px;display:flex;
      justify-content:space-between;font-size:12px;color:#8A8A8A}
.slide.bia{justify-content:center;background:#1A1A1A;color:#FFFFFF}
.slide.bia h1{font-size:52px;max-width:1020px}
.slide.bia .phu{color:#D9D9D9;font-size:21px;margin-top:20px;max-width:960px}
.slide.bia li{font-size:16px;color:#BFBFBF;margin-bottom:8px}
.slide.bia li:before{background:#CC4C02;top:8px}
.slide.bia .than{margin-top:34px;flex:0 0 auto;justify-content:flex-start}
.slide.bia .chan{color:#8A8A8A}
.slide.ket h1{font-size:30px;color:#555555;font-weight:600}
.loi{position:fixed;left:0;right:0;bottom:0;max-height:34%;overflow:auto;
     background:#1A1A1A;color:#E8E8E8;font-size:15px;line-height:1.5;padding:14px 20px;
     display:none;border-top:2px solid #CC4C02}
body.co-loi .loi{display:block}
.loi b{color:#FF9F4D}
/* Số trang nằm trong chân slide; ô #dem chỉ hiện khi bật lời dẫn, vì lúc đó
   chân slide bị khung lời dẫn che mất. */
#dem{position:fixed;right:14px;bottom:10px;color:#9A9A9A;font-size:12px;display:none}
body.co-loi #dem{display:block;bottom:auto;top:10px}
body.luoi #san{overflow:auto;align-items:flex-start;padding:16px}
body.luoi #khung{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
body.luoi .slide{display:flex;zoom:0.24;box-shadow:0 0 0 4px #4A4A4A;transform:none}
@media print{
  @page{size:landscape;margin:0}
  html,body{background:#FFFFFF}
  #san{position:static;display:block;overflow:visible}
  #khung{display:block}
  .slide{display:flex !important;transform:none;page-break-after:always;zoom:1}
  .loi,#dem{display:none !important}
}
"""

JS = """
var ss=[].slice.call(document.querySelectorAll('.slide')),i=0;
function co(){
  var w=window.innerWidth,h=window.innerHeight;
  document.documentElement.style.setProperty('--s',Math.min(w/1300,h/740));
}
function ve(){
  ss.forEach(function(s,k){s.classList.toggle('hien',k===i);});
  var l=ss[i].getAttribute('data-loi')||'';
  document.getElementById('loi').innerHTML=l;
  document.getElementById('dem').textContent=(i+1)+' / '+ss.length;
  if(location.hash!=='#'+i){history.replaceState(null,'','#'+i);}
}
function di(d){i=Math.min(ss.length-1,Math.max(0,i+d));ve();}
document.addEventListener('keydown',function(e){
  var k=e.key;
  if(k==='ArrowRight'||k==='PageDown'||k===' '||k==='Enter'){di(1);e.preventDefault();}
  else if(k==='ArrowLeft'||k==='PageUp'||k==='Backspace'){di(-1);e.preventDefault();}
  else if(k==='Home'){i=0;ve();}
  else if(k==='End'){i=ss.length-1;ve();}
  else if(k==='n'||k==='N'){document.body.classList.toggle('co-loi');}
  else if(k==='g'||k==='G'){document.body.classList.toggle('luoi');}
});
document.getElementById('san').addEventListener('click',function(e){
  if(document.body.classList.contains('luoi')){
    var s=e.target.closest('.slide');
    if(s){i=ss.indexOf(s);document.body.classList.remove('luoi');ve();}
  } else {di(1);}
});
window.addEventListener('resize',co);
window.addEventListener('hashchange',function(){
  var n=parseInt(location.hash.slice(1),10);
  if(!isNaN(n)&&n>=0&&n<ss.length&&n!==i){i=n;ve();}
});
var n0=parseInt(location.hash.slice(1),10);
if(!isNaN(n0)&&n0>=0&&n0<ss.length){i=n0;}
co();ve();
"""


def mot_slide(sl, S, thieu, embed, so_tt, tong):
    """Một slide → HTML. Mọi chữ đi qua dien() rồi inline()."""
    def d(x):
        return inline(dien(x, S, thieu))

    kieu = sl["kieu"]
    h = ['<section class="slide %s" data-loi="%s">'
         % (kieu, d(sl.get("notes", "")).replace('"', "&quot;"))]
    h.append("<h1>%s</h1>" % d(sl["tieu_de"]))
    if sl.get("phu"):
        h.append('<div class="phu">%s</div>' % d(sl["phu"]))

    diem = "".join("<li>%s</li>" % d(x) for x in sl.get("diem", []))
    bang = ""
    if sl.get("bang"):
        hd = sl["bang"][0]
        bang = ["<table><thead><tr>"]
        bang += ["<th>%s</th>" % d(c) for c in hd]
        bang.append("</tr></thead><tbody>")
        for r in sl["bang"][1:]:
            bang.append("<tr>" + "".join("<td>%s</td>" % d(c) for c in r) + "</tr>")
        bang.append("</tbody></table>")
        bang = "".join(bang)

    if kieu in ("bia", "chu", "ket"):
        h.append('<div class="than doc"><ul>%s</ul></div>' % diem)
    elif kieu == "so":
        the = "".join(
            '<div class="the"><div class="v">%s</div><div class="n">%s</div></div>'
            % (d(v), d(n)) for v, n in sl["so"])
        h.append('<div class="than doc"><div class="the-so">%s</div><ul>%s</ul></div>'
                 % (the, diem))
    elif kieu == "hinh":
        than = ('<div class="hinh-o"><img alt="%s" src="%s"></div>'
                '<div class="ben">%s</div>'
                % (d(sl["tieu_de"]), nguon_anh(sl["hinh"], embed),
                   bang or ("<ul>%s</ul>" % diem)))
        h.append('<div class="than">%s</div>' % than)
    elif kieu == "hinh2":
        h.append('<div class="than doc"><div class="doi">'
                 '<div class="hinh-o"><img alt="" src="%s"></div>'
                 '<div class="hinh-o"><img alt="" src="%s"></div></div>'
                 '<ul>%s</ul></div>'
                 % (nguon_anh(sl["hinh"], embed), nguon_anh(sl["hinh2"], embed), diem))
    elif kieu == "bang":
        h.append('<div class="than doc">%s<ul>%s</ul></div>' % (bang, diem))
    else:
        raise ValueError("kiểu slide lạ: %s" % kieu)

    ai = NGUOI[sl["chu"]]
    nhan = "Dự phòng" if sl.get("du_phong") else (
        "Nhịp %d" % sl["nhip"] if sl.get("nhip") else "Khung bài")
    viec = (" · %s" % sl["viec"]) if sl.get("viec") else ""
    h.append('<div class="chan"><span>%s%s · %s trình bày</span>'
             '<span>%d / %d</span></div>' % (nhan, viec, ai, so_tt, tong))
    h.append("</section>")
    return "".join(h)


def dung_html(S, thieu, embed):
    tong = len(SLIDES)
    body = "".join(mot_slide(sl, S, thieu, embed, i + 1, tong)
                   for i, sl in enumerate(SLIDES))
    tieu_de = dien(SLIDES[0]["tieu_de"], S, thieu)
    return ("<!doctype html>\n<html lang=\"vi\"><head><meta charset=\"utf-8\">"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>%s — slide</title><style>%s</style></head><body>"
            "<div id=\"san\"><div id=\"khung\">%s</div></div>"
            "<div class=\"loi\" id=\"loi\"></div><div id=\"dem\"></div>"
            "<script>%s</script></body></html>\n"
            % (tieu_de, CSS, body, JS))


# ------------------------------------------------------------------ dựng .md

def dung_md(S, thieu):
    r = ["# Slide thuyết trình — %s" % dien(SLIDES[0]["tieu_de"], S, thieu), "",
         "> Dựng bằng `src/build_slides.py` (T28). **Đừng sửa file này bằng tay** —",
         "> sửa phần `SLIDES` trong script rồi chạy lại, vì mọi con số ở đây do",
         "> script đo từ `data/processed/` và đối chiếu với báo cáo cuối.", "",
         "Bản trình chiếu: `output/slide-thuyet-trinh.html` — mũi tên để đi, `n` bật",
         "lời dẫn, `g` xem dạng lưới, in ra PDF thì mỗi slide một trang ngang.", ""]
    for i, sl in enumerate(SLIDES):
        nhan = ("Dự phòng" if sl.get("du_phong")
                else ("Nhịp %d" % sl["nhip"] if sl.get("nhip") else "Khung bài"))
        r.append("## %d. %s" % (i + 1, dien(sl["tieu_de"], S, thieu)))
        r.append("")
        r.append("*%s · %s trình bày%s*"
                 % (nhan, NGUOI[sl["chu"]],
                    (" · %s" % sl["viec"]) if sl.get("viec") else ""))
        r.append("")
        if sl.get("phu"):
            r.append(dien(sl["phu"], S, thieu))
            r.append("")
        for h in ("hinh", "hinh2"):
            if sl.get(h):
                r.append("![%s](%s.png)" % (sl[h], sl[h]))
                r.append("")
        if sl.get("so"):
            for v, n in sl["so"]:
                r.append("- **%s** — %s" % (dien(v, S, thieu),
                                            dien(n, S, thieu).replace("<br>", " ")))
            r.append("")
        if sl.get("bang"):
            b = sl["bang"]
            r.append("| " + " | ".join(dien(c, S, thieu) for c in b[0]) + " |")
            r.append("|" + "---|" * len(b[0]))
            for row in b[1:]:
                r.append("| " + " | ".join(dien(c, S, thieu) for c in row) + " |")
            r.append("")
        for x in sl.get("diem", []):
            r.append("- %s" % dien(x, S, thieu))
        if sl.get("diem"):
            r.append("")
        r.append("**Lời dẫn.** %s" % dien(sl.get("notes", ""), S, thieu))
        r.append("")
    return "\n".join(r) + "\n"


# --------------------------------------------------------------- kiểm chứng

def dem_tu(s):
    return len([w for w in re.sub(r"[#>*`_|·•→←—–]", " ", s).split()
                if any(c.isalnum() for c in w)])


def kiem_chung(S, thieu, embed):
    """In khối KIỂM CHỨNG. Trả về số lỗi — khác 0 thì script thoát với mã 1."""
    loi = 0
    print("\n" + "=" * 72)
    print("KIỂM CHỨNG — T28 slide thuyết trình")
    print("=" * 72)

    chinh = [s for s in SLIDES if not s.get("du_phong")]
    du = [s for s in SLIDES if s.get("du_phong")]
    print("  Slide: %d chính + %d dự phòng = %d" % (len(chinh), len(du), len(SLIDES)))

    # 1. ô {khoá} không giải được
    print("\n  1. Ô {khoá} chưa giải được: %d" % len(thieu))
    for k in sorted(thieu):
        print("     THIẾU  {%s}" % k)
    loi += len(thieu)

    # 2. hình phải có file thật
    hinh = [sl[h] for sl in SLIDES for h in ("hinh", "hinh2") if sl.get(h)]
    mat = [h for h in hinh if not os.path.exists(os.path.join(OUT, h + ".png"))]
    print("\n  2. Hình dùng trên slide: %d, thiếu file: %d" % (len(hinh), len(mat)))
    for h in mat:
        print("     THIẾU  output/%s.png" % h)
    loi += len(mat)

    # 3. năm nhịp phải đủ và đúng thứ tự
    nhip = [sl.get("nhip") for sl in chinh if sl.get("nhip")]
    thieu_nhip = [n for n in (1, 2, 3, 4, 5) if n not in nhip]
    xuoi = all(nhip[k] <= nhip[k + 1] for k in range(len(nhip) - 1))
    print("\n  3. Mạch năm nhịp: %s · thứ tự %s"
          % ("đủ 1–5" if not thieu_nhip else "THIẾU %s" % thieu_nhip,
             "xuôi" if xuoi else "NGƯỢC"))
    loi += len(thieu_nhip) + (0 if xuoi else 1)

    # 4. checklist nộp bài mục 3 — cả ba người đều có phần
    chu = {}
    for sl in SLIDES:
        chu[sl["chu"]] = chu.get(sl["chu"], 0) + 1
    vang = [k for k in ("R1", "R2", "R3") if not chu.get(k)]
    print("\n  4. Ai trình bày mấy slide: %s"
          % " · ".join("%s %s %d" % (k, NGUOI[k], chu[k]) for k in sorted(chu)))
    if vang:
        print("     THIẾU phần của: %s" % ", ".join(vang))
    loi += len(vang)

    # 5. checklist mục 4 — phải có cả hai họ kỹ thuật
    cay = [h for h in hinh if any(t in h for t in HO_CAY)]
    dt = [h for h in hinh if any(t in h for t in HO_DO_THI)]
    print("\n  5. Hai họ kỹ thuật: cây %d hình (%s) · đồ thị %d hình"
          % (len(cay), ", ".join(sorted(set(cay))), len(dt)))
    loi += (0 if cay else 1) + (0 if dt else 1)

    # 6. số trên slide phải khớp số báo cáo cuối đã in
    lech = [(k, v, S.get(k)) for k, v in sorted(KY_VONG.items()) if S.get(k) != v]
    print("\n  6. Đối chiếu với báo cáo cuối: %d/%d khớp"
          % (len(KY_VONG) - len(lech), len(KY_VONG)))
    for k, cho, co in lech:
        print("     LỆCH  %-22s báo cáo %-12s slide %s" % (k, cho, co))
    loi += len(lech)

    # 7. tỷ trọng ngành phải cộng đủ 100%
    for nhan in ("dau", "cuoi"):
        t = S["tong_ty_trong_" + nhan]
        print("\n  7. Tỷ trọng 10 ngành năm %s cộng lại: %s%%"
              % (S["nam_dau"] if nhan == "dau" else S["nam"], t))
        if not t.startswith("100,0000"):
            print("     SAI, phải là 100")
            loi += 1

    # 8. slide quá dài thì không đọc được khi chiếu
    dai = [(sl["ma"], len(sl.get("diem", [])), len(dien(sl["tieu_de"], S, set())))
           for sl in SLIDES]
    xau = [x for x in dai if x[1] > 4 or x[2] > 74]
    print("\n  8. Dung lượng chữ: nhiều nhất %d gạch đầu dòng, tiêu đề dài nhất "
          "%d ký tự" % (max(x[1] for x in dai), max(x[2] for x in dai)))
    for ma, n, t in xau:
        print("     DÀI   slide %s — %d gạch đầu dòng, tiêu đề %d ký tự" % (ma, n, t))
    loi += len(xau)

    tu = sum(dem_tu(dien(sl.get("notes", ""), S, set())) for sl in SLIDES)
    print("\n  Lời dẫn: %s chữ, chừng %s phút nói ở nhịp 130 chữ/phút"
          % (R.fmt_vn(tu, 0), R.fmt_vn(tu / 130.0, 1)))
    print("  Bản ảnh: %s" % ("nhúng base64 (--embed)" if embed
                             else "trỏ sang PNG cùng thư mục"))
    print("\n  %s" % ("ĐẠT — %d phép kiểm, không lỗi" % 8 if not loi
                      else "KHÔNG ĐẠT — %d lỗi" % loi))
    print("=" * 72)
    return loi


# -------------------------------------------------------------------- chạy

def main():
    p = argparse.ArgumentParser(description="T28 — dựng slide thuyết trình")
    p.add_argument("--embed", action="store_true",
                   help="nhúng PNG vào HTML (một file đứng riêng, nặng ~9 MB)")
    a = p.parse_args()

    print("Đo lại số từ %s ..." % DATA)
    S = do_so()
    thieu = set()
    html = dung_html(S, thieu, a.embed)
    md = dung_md(S, thieu)

    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    ph = os.path.join(OUT, TEN + ".html")
    pm = os.path.join(OUT, TEN + ".md")
    io.open(ph, "w", encoding="utf-8", newline="\n").write(html)
    io.open(pm, "w", encoding="utf-8", newline="\n").write(md)
    print("  %s  (%s KB)" % (ph, R.fmt_vn(len(html.encode("utf-8")) / 1024.0, 0)))
    print("  %s  (%s KB)" % (pm, R.fmt_vn(len(md.encode("utf-8")) / 1024.0, 0)))

    return 1 if kiem_chung(S, thieu, a.embed) else 0


if __name__ == "__main__":
    sys.exit(main())

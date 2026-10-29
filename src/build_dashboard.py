# -*- coding: utf-8 -*-
"""Dựng trang dashboard — hàng chỉ số ở trên, lưới biểu đồ ở dưới.

Vì sao có trang thứ hai bên cạnh bài viết
-----------------------------------------
``site/index.html`` là một bài viết: đọc từ trên xuống, chữ dẫn rồi mới tới hình.
Hợp để gắn link vào báo cáo, nhưng đem ra demo thì người xem phải cuộn qua từng
đoạn văn mới thấy hình. Trang này đảo lại: số trước, hình ngay dưới, chữ chỉ còn
đúng câu tiêu đề mà chính script vẽ đã dựng từ dữ liệu.

Không đo thêm gì mà không đối chiếu
----------------------------------
Sáu ô chỉ số cần cả chuỗi 1995–2023 để vẽ đường nhỏ (sparkline), thứ mà
``build_slides.do_so()`` không trả về. Chuỗi được tính từ đúng những file và
đúng phép tính mà ``do_so()`` dùng, rồi phép kiểm 8 so điểm đầu và điểm cuối của
từng chuỗi với khoá tương ứng của ``do_so()`` (đã khớp với báo cáo qua
``KY_VONG``). Lệch một chữ số là trang không đạt.

Vì sao tiêu đề hình nằm ngoài khung hình
----------------------------------------
Mỗi file Plotly mang tiêu đề, phụ đề, chú thích và dòng nguồn dưới dạng
annotation ở lề trên và lề dưới. Trên dashboard, tiêu đề lên đầu thẻ, nguồn gộp
một lần ở chân trang, còn khung hình được cắt chỉ chừa vùng vẽ. Cắt chứ không
vẽ lại: file biểu đồ vẫn là đúng file của bài viết, nên hai trang không thể vẽ
hai hình khác nhau. Chỗ cắt đo trong trình duyệt từ chính các annotation đó
(``dash.js``); Python chỉ ghi annotation nào nằm ở lề nào.

Trang này được ``build_web.py`` gọi, không chạy riêng.
"""

from __future__ import print_function

import html
import io
import json
import os
import re

import pandas as pd

import reference_data as R
import build_slides as BS
import build_web as BW
import make_time_multiples as TM

DATA = BS.DATA
FOCUS = BS.FOCUS
NAM = BS.NAM
NAM_DAU = BS.NAM_DAU


# ------------------------------------------------------------------ chuỗi số

def chuoi(S):
    """Sáu chuỗi theo năm cho hàng chỉ số. Mỗi chuỗi: list (năm, giá trị số)."""
    cy = pd.read_csv(os.path.join(DATA, "country_year.csv"))
    v = cy[(cy["country_iso3"] == FOCUS) & (cy["year"] <= NAM)
           & (cy["year"] >= NAM_DAU)].set_index("year").sort_index()

    e = pd.read_csv(os.path.join(DATA, "edges.csv"))
    e = e[(e["year"] <= NAM) & (e["year"] >= NAM_DAU)]
    hang, thi_phan, tong_nuoc = [], [], {}
    for y, d in e.groupby("year"):
        g = d.groupby("source_iso3")["export_value"].sum()
        g = g[g > 0].sort_values(ascending=False)
        if FOCUS not in g.index:
            continue
        hang.append((int(y), list(g.index).index(FOCUS) + 1))
        tong_nuoc[int(y)] = len(g)
        thi_phan.append((int(y), float(g[FOCUS]) / float(g.sum()) * 100.0))

    tree = pd.read_csv(os.path.join(DATA, "tree.csv"))
    cp = pd.read_csv(os.path.join(DATA, "country_product.csv"))
    cp = cp[(cp["country_iso3"] == FOCUS) & (cp["year"] <= NAM)]
    cp = cp.assign(sector=cp["product_id"].map(tree.set_index("product_id")["sector_id"]))
    nganh = cp.groupby(["year", "sector"])["export_value"].sum().unstack(fill_value=0.0)
    nganh = nganh.div(nganh.sum(axis=1), axis=0) * 100.0
    dien_tu = R_ID["Electronics"]

    _, _, cx = TM.load([NAM], "xuat")
    cx = cx[cx.index >= NAM_DAU]

    return {
        "xuat": [(int(y), float(x) / 1e9) for y, x in v["export_value"].items()],
        "hang": hang,
        "eci": [(int(y), int(x)) for y, x in v["eci_rank"].items()],
        "eci_n": {int(y): int(x) for y, x in v["eci_n"].items()},
        "hang_n": tong_nuoc,
        "dien_tu": [(int(y), float(x)) for y, x in nganh[dien_tu].items()],
        "top3": [(int(y), float(x)) for y, x in cx["top3"].items()],
        # Năm thị trường giãn nhất theo HHI, đúng mốc do_so() gọi là nam_day —
        # KHÔNG phải năm top-3 thấp nhất (2001), hai đáy không trùng nhau.
        "nam_day": int(cx["hhi"].idxmin()),
        "thi_phan": thi_phan,
        "nganh": nganh,
    }


def _id_nganh():
    t = pd.read_csv(os.path.join(DATA, "tree.csv"))
    t = t[t["level"] == 1]
    return {n: int(i) for n, i in zip(t["name_short"], t["sector_id"])}


R_ID = _id_nganh()


def gia_tri(C, ma, y):
    return dict(C[ma])[y]


# Mỗi ô chỉ số: khoá chuỗi, nhãn, cách định dạng một giá trị, khoá do_so() mà điểm
# đầu/điểm cuối phải khớp, và chiều "tốt" (hạng thì số nhỏ là tốt nên đảo trục).
O_CHI_SO = [
    dict(ma="xuat", nhan="Kim ngạch xuất khẩu",
         so=lambda C, y: (R.fmt_vn(gia_tri(C, "xuat", y), 1), "tỷ USD"),
         khop=lambda C, y: R.fmt_usd(gia_tri(C, "xuat", y) * 1e9),
         khoa=("vn_dau", "vn_cuoi"), dao=False,
         doi=lambda C: "gấp %s lần năm %d" % (
             R.fmt_vn(gia_tri(C, "xuat", NAM) / gia_tri(C, "xuat", NAM_DAU), 1), NAM_DAU)),
    dict(ma="thi_phan", nhan="Thị phần xuất khẩu thế giới",
         so=lambda C, y: (R.fmt_vn(gia_tri(C, "thi_phan", y), 3), "%"),
         khop=lambda C, y: R.fmt_pct(gia_tri(C, "thi_phan", y), 3),
         khoa=("tp_dau", "tp_cuoi"), dao=False,
         doi=lambda C: "từ %s năm %d" % (R.fmt_pct(gia_tri(C, "thi_phan", NAM_DAU), 3),
                                          NAM_DAU)),
    dict(ma="hang", nhan="Hạng xuất khẩu thế giới",
         so=lambda C, y: ("%d" % gia_tri(C, "hang", y), "/%d" % C["hang_n"][y]),
         khop=lambda C, y: "%d/%d" % (gia_tri(C, "hang", y), C["hang_n"][y]),
         khoa=("hang_dau", "hang_cuoi"), dao=True,
         doi=lambda C: "tăng %d bậc từ năm %d" % (
             gia_tri(C, "hang", NAM_DAU) - gia_tri(C, "hang", NAM), NAM_DAU)),
    dict(ma="eci", nhan="Hạng phức tạp kinh tế (ECI)",
         so=lambda C, y: ("%d" % gia_tri(C, "eci", y), "/%d" % C["eci_n"][y]),
         khop=lambda C, y: "%d/%d" % (gia_tri(C, "eci", y), C["eci_n"][y]),
         khoa=("eci_dau", "eci_cuoi"), dao=True,
         doi=lambda C: "tăng %d bậc từ năm %d" % (
             gia_tri(C, "eci", NAM_DAU) - gia_tri(C, "eci", NAM), NAM_DAU)),
    dict(ma="dien_tu", nhan="Điện tử trong rổ hàng",
         so=lambda C, y: (R.fmt_vn(gia_tri(C, "dien_tu", y), 1), "%"),
         khop=lambda C, y: R.fmt_pct(gia_tri(C, "dien_tu", y)),
         khoa=("dien_tu_dau", "dien_tu_cuoi"), dao=False,
         doi=lambda C: "từ %s năm %d" % (R.fmt_pct(gia_tri(C, "dien_tu", NAM_DAU)),
                                          NAM_DAU)),
    dict(ma="top3", nhan="Xuất khẩu vào ba thị trường lớn nhất",
         so=lambda C, y: (R.fmt_vn(gia_tri(C, "top3", y), 2), "%"),
         khop=lambda C, y: R.fmt_pct(gia_tri(C, "top3", y), 2),
         # Mốc so là năm HHI thấp nhất (nam_day); điểm đầu chuỗi không có khoá.
         khoa=(None, "top3_cuoi"), dao=False,
         doi=lambda C: "từ %s năm %d" % (
             R.fmt_pct(gia_tri(C, "top3", C["nam_day"]), 2), C["nam_day"])),
]


def duong_nho(chuoi_so, dao, mau):
    """Sparkline SVG: toàn chuỗi, chấm ở hai năm có biểu đồ. Không có trục —
    hai năm đầu/cuối ghi dưới đường, giá trị thì đã nằm ở ô số phía trên."""
    W, H, P = 160.0, 40.0, 3.0
    nam = [y for y, _ in chuoi_so]
    gt = [x for _, x in chuoi_so]
    lo, hi = min(gt), max(gt)
    rong = (hi - lo) or 1.0

    def xy(y, x):
        px = P + (y - nam[0]) / float(nam[-1] - nam[0]) * (W - 2 * P)
        t = (x - lo) / rong
        py = P + (t if dao else 1 - t) * (H - 2 * P)
        return px, py

    diem = " ".join("%.1f,%.1f" % xy(y, x) for y, x in chuoi_so)
    cham = "".join(
        '<circle class="spark__dot" data-year="%d" cx="%.1f" cy="%.1f" r="3"/>'
        % ((y,) + xy(y, dict(chuoi_so)[y])) for y in (NAM_DAU, NAM))
    return ('<svg class="spark" viewBox="0 0 %d %d" preserveAspectRatio="none" '
            'aria-hidden="true" focusable="false" style="--spark:%s">'
            '<polyline points="%s"/>%s</svg>' % (W, H, mau, diem, cham))


def o_chi_so(C):
    out = []
    for o in O_CHI_SO:
        gia = {y: o["so"](C, y) for y in (NAM_DAU, NAM)}
        du_lieu = json.dumps({str(y): list(gia[y]) for y in gia}, ensure_ascii=False)
        so, don_vi = gia[NAM]
        out.append(
            '<li class="kpi" data-values=\'%s\'>'
            '<p class="kpi__label">%s</p>'
            '<p class="kpi__value"><span class="kpi__num">%s</span>'
            '<span class="kpi__unit">%s</span></p>'
            '<p class="kpi__delta" data-now="%s" data-base="%s">%s</p>'
            '%s'
            '<p class="kpi__axis" aria-hidden="true"><span>%d</span><span>%d</span></p>'
            '</li>' % (html.escape(du_lieu, quote=True), html.escape(o["nhan"]),
                       so, html.escape(don_vi), html.escape(o["doi"](C)),
                       html.escape("mốc đầu của chuỗi"), html.escape(o["doi"](C)),
                       # Mực cho mọi đường: màu ngành điện tử (xanh nhạt) chỉ
                       # đạt dưới 3:1 trên nền trắng khi đứng một mình.
                       duong_nho(C[o["ma"]], o["dao"], "var(--ink)"),
                       NAM_DAU, NAM))
    return "".join(out)


# ------------------------------------------------------------------ bảng ngành

def bang_nganh(C):
    n = C["nganh"]
    dau, cuoi = n.loc[NAM_DAU], n.loc[NAM]
    thu_tu = sorted(R.SECTOR_PALETTE, key=lambda k: -float(cuoi.get(k, 0.0)))
    dong = []
    lon_nhat = max(abs(float(cuoi.get(k, 0)) - float(dau.get(k, 0)))
                   for k in thu_tu) or 1.0
    for k in thu_tu:
        a, b = float(dau.get(k, 0.0)), float(cuoi.get(k, 0.0))
        d = b - a
        dong.append(
            '<tr><th scope="row"><span class="swatch" style="background:%s"></span>%s</th>'
            '<td>%s</td><td>%s</td>'
            '<td class="delta %s"><span class="delta__bar" style="--d:%.3f"></span>'
            '<span class="delta__txt">%s%s</span></td></tr>'
            % (R.SECTOR_PALETTE[k], html.escape(R.SECTOR_NAME_VI[k]),
               R.fmt_pct(a), R.fmt_pct(b), "delta--up" if d >= 0 else "delta--down",
               abs(d) / lon_nhat, "+" if d >= 0 else "−", R.fmt_vn(abs(d), 1)))
    return "".join(dong)


# ------------------------------------------------------------------ thẻ biểu đồ

def _chu(t):
    t = re.sub(r"<br\s*/?>", " ", t)
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


def doc_bo_cuc(ten):
    """Đọc layout của một file Plotly: annotation nào ở lề trên, lề dưới."""
    s = io.open(os.path.join(BW.OUT, ten + ".html"), encoding="utf-8").read()
    dec = json.JSONDecoder()
    i = s.find("Plotly.newPlot(")
    j = s.find("[", i)
    _, k = dec.raw_decode(s, j)
    lay, _ = dec.raw_decode(s, s.find("{", k))
    tren, duoi = [], []
    for idx, a in enumerate(lay.get("annotations", [])):
        if a.get("yref") != "paper":
            continue
        y = float(a.get("y", 0.5))
        if y > 1:
            tren.append((y, idx, a.get("text", "")))
        elif y < 0:
            duoi.append((y, idx, a.get("text", "")))
    tren.sort(reverse=True)
    m = lay.get("margin", {})
    w, h = BW.khung_hinh(ten)
    return dict(
        w=w, h=h, tren=[i for _, i, _ in tren], duoi=[i for _, i, _ in duoi],
        tieu_de=_chu(tren[0][2]) if tren else "",
        phu_de=" ".join(_chu(t) for _, _, t in tren[1:]),
        # Ước lượng chỗ cắt để giữ chỗ trước khi biểu đồ tải xong; dash.js đo lại.
        cat=[max(0, int(m.get("t", 0)) - 8), int(h - 0.45 * float(m.get("b", 0)))])


# Ba thẻ tab, gom năm nhịp của bài viết theo những gì người xem muốn so cạnh
# nhau trên một màn hình. ``chip`` là vài con số phụ cho riêng tab đó.
TAB = [
    dict(id="ro-hang", nhan="Rổ hàng", nhip=["1", "2"],
         hinh=["dong_chay", "cay", "luoi_asean", "#bang-nganh"],
         chip=[("{asean_cuoi}", "hạng trong ASEAN, từ {asean_dau}"),
               ("{mat_hang_cuoi}", "chỉ số đa dạng của Atlas, từ {mat_hang_dau}"),
               ("{det_may_cuoi}", "dệt may, giày dép, nội thất, từ {det_may_dau}")]),
    dict(id="mang-luoi", nhan="Mạng lưới & hành lang", nhip=["3"],
         hinh=["bac", "mang", "sankey", "ban_cho_ai"],
         chip=[("{nut}", "nước trong mạng năm {nam}"),
               ("{canh}", "luồng xuất khẩu; mật độ {mat_do}"),
               ("{vung_mua_pct}", "hàng nhập đến từ {vung_mua}"),
               ("{hhi_lan}×", "đầu vào tập trung hơn đầu ra (HHI)")]),
    dict(id="loi-the", nhan="Lợi thế & đề xuất", nhip=["4", "5"],
         hinh=["mat_phang", "chay_lai"],
         chip=[("{goc_kep_pct}", "kim ngạch ở nhóm bán mạnh nhưng dễ làm"),
               ("{rca_giay}", "RCA giày dép; PCI {pci_giay}"),
               ("{rca_quang}", "RCA {chay_nay_0}"),
               ("{rca_may}", "RCA {chay_nay_1}")]),
]


def the_hinh(ma, S, thieu, meta):
    h = BW.HINH[ma]
    d = lambda x: BW.dien(x, S, thieu)       # noqa: E731
    tep = {tuple(d(k) for k in khoa): d(v) for khoa, v in h["tep"].items()}
    chieu = [(ten, [(d(k), d(n)) for k, n in lua]) for ten, lua in h["chieu"]]
    mac_dinh = tuple(lua[0][0] for _, lua in chieu)
    ten0 = tep[mac_dinh]
    for v in tep.values():
        if v not in meta:
            meta[v] = doc_bo_cuc(v)
    m0 = meta[ten0]

    dk = []
    for i, (ten, lua) in enumerate(chieu):
        nut = "".join(
            '<button type="button" class="seg__btn" data-dim="%d" data-val="%s" '
            'aria-pressed="%s">%s</button>'
            % (i, html.escape(k), "true" if k == mac_dinh[i] else "false",
               html.escape(n)) for k, n in lua)
        dk.append('<div class="seg" role="group" aria-label="%s" data-name="%s">%s</div>'
                  % (html.escape(ten), html.escape(ten), nut))
    bang = json.dumps({"|".join(k): v for k, v in sorted(tep.items())})
    return (
        '<article class="card" id="the-{id}" data-map=\'{bang}\'>\n'
        '  <header class="card__head">\n'
        '    <p class="card__kicker">{nhan}<span class="card__task">{viec}</span></p>\n'
        '    <h3 class="card__title">{td}</h3>\n'
        '    <p class="card__sub">{pd}</p>\n'
        '  </header>\n'
        '  {dk}\n'
        '  <div class="card__frame" style="--w:{w};--ch:{ch}">\n'
        '    <iframe data-src="charts/{t}.html" title="{nhan}" scrolling="no" '
        'tabindex="-1" width="{w}" height="{h}"></iframe>\n'
        '    <p class="card__loading" aria-hidden="true">Đang tải biểu đồ…</p>\n'
        '  </div>\n'
        '  <footer class="card__foot">\n'
        '    <details><summary>Cách đọc</summary><p>{doc}</p></details>\n'
        '    <a class="card__open" href="charts/{t}.html" target="_blank" rel="noopener">'
        'Mở riêng{icon}<span class="sr-only"> (mở trong thẻ mới)</span></a>\n'
        '  </footer>\n'
        '</article>'
    ).format(id=ma.replace("_", "-"), bang=html.escape(bang, quote=True),
             nhan=html.escape(d(h["nhan"])), viec=html.escape(h["viec"]),
             td=html.escape(m0["tieu_de"]), pd=html.escape(m0["phu_de"]),
             dk="".join(dk), w=m0["w"], h=m0["h"], ch=m0["cat"][1] - m0["cat"][0],
             t=ten0, doc=BW.md(h["doc"], S, thieu), icon=BW.ICON_MO)


def the_bang(C):
    return (
        '<article class="card card--table" id="bang-nganh">\n'
        '  <header class="card__head">\n'
        '    <p class="card__kicker">Mười ngành cấp 1, HS92<span class="card__task">'
        'T12, T21</span></p>\n'
        '    <h3 class="card__title">Tỷ trọng từng ngành trong xuất khẩu của Việt Nam, '
        '%d và %d</h3>\n'
        '    <p class="card__sub">Xếp theo tỷ trọng năm %d. Cột cuối là thay đổi tính '
        'bằng điểm phần trăm; vạch dài nhất là ngành đổi nhiều nhất.</p>\n'
        '  </header>\n'
        '  <div class="table-wrap"><table class="sectors">\n'
        '    <thead><tr><th scope="col">Ngành</th><th scope="col">%d</th>'
        '<th scope="col">%d</th><th scope="col">Thay đổi (điểm %%)</th></tr></thead>\n'
        '    <tbody>%s</tbody>\n'
        '  </table></div>\n'
        '</article>' % (NAM_DAU, NAM, NAM, NAM_DAU, NAM, bang_nganh(C)))


def tab_html(t, S, thieu, meta, C):
    nhip = [n for n in BW.NHIP if n["ma"] in t["nhip"]]
    tieu = "".join('<li>%s</li>' % BW.md(n["tieu_de"], S, thieu) for n in nhip)
    chip = "".join(
        '<div class="chip"><dt>%s</dt><dd>%s</dd></div>'
        % (BW.md(nh, S, thieu), BW.md(gt, S, thieu)) for gt, nh in t["chip"])
    the = []
    for ma in t["hinh"]:
        the.append(the_bang(C) if ma == "#bang-nganh" else the_hinh(ma, S, thieu, meta))
    return (
        '<section class="panel" id="{id}" role="tabpanel" aria-labelledby="tab-{id}"'
        '{an}>\n'
        '  <div class="panel__head">\n'
        '    <ul class="panel__claims">{tieu}</ul>\n'
        '    <dl class="panel__chips">{chip}</dl>\n'
        '  </div>\n'
        '  <div class="grid">\n{the}\n  </div>\n'
        '</section>'
    ).format(id=t["id"], an="" if t is TAB[0] else " hidden", tieu=tieu, chip=chip,
             the="\n".join(the))


def dung_trang(S, thieu):
    C = chuoi(S)
    meta = {}
    tabs = "".join(
        '<button type="button" role="tab" class="tab" id="tab-{id}" '
        'aria-controls="{id}" aria-selected="{sel}" tabindex="{ti}">{nhan}'
        '<span class="tab__count">{n}</span></button>'.format(
            id=t["id"], nhan=html.escape(t["nhan"]),
            sel="true" if t is TAB[0] else "false", ti="0" if t is TAB[0] else "-1",
            n=len(t["hinh"])) for t in TAB)
    panels = "\n".join(tab_html(t, S, thieu, meta, C) for t in TAB)
    thay = {
        "kpi": o_chi_so(C), "tabs": tabs, "panels": panels, "repo": BW.REPO_URL,
        "nam": S["nam"], "nam_dau": S["nam_dau"],
        "meta_json": json.dumps(meta, ensure_ascii=False).replace("</", "<\\/"),
        "nguon": BW.md("Atlas of Economic Complexity · Harvard Growth Lab · HS92 · "
                       "{nam_dau}–{nam}", S, thieu),
        "chu_giai": "".join(
            '<li><span class="swatch" style="background:%s"></span>%s</li>'
            % (R.SECTOR_PALETTE[k], html.escape(R.SECTOR_NAME_VI[k]))
            for k in sorted(R.SECTOR_PALETTE)),
    }
    mau = io.open(os.path.join(BW.ASSETS_SRC, "dashboard.template.html"),
                  encoding="utf-8").read()
    return re.sub(r"\[\[([a-z_]+)\]\]", lambda m: thay[m.group(1)], mau), C, meta


# ------------------------------------------------------------------ kiểm chứng

def kiem(S, C, meta, dung):
    """Trả về số lỗi. In hai phép kiểm (8, 9) nối tiếp bảy phép của build_web."""
    loi = 0
    print("\n  8. Chuỗi của dashboard khớp do_so() ở hai đầu:")
    for o in O_CHI_SO:
        for y, k in zip((NAM_DAU, NAM), o["khoa"]):
            if k is None:
                continue
            co, cho = o["khop"](C, y), S.get(k)
            ok = co == cho
            loi += 0 if ok else 1
            print("     %s  %-12s %d  dashboard %-14s do_so %s"
                  % ("khớp" if ok else "LỆCH", o["ma"], y, co, cho))
    # Mốc so của top-3 cũng là hai khoá đã đối chiếu (nam_day, top3_day).
    y = C["nam_day"]
    co = ("%d" % y, R.fmt_pct(gia_tri(C, "top3", y), 2))
    ok = co == (S["nam_day"], S["top3_day"])
    loi += 0 if ok else 1
    print("     %s  top3 mốc     %s  dashboard %-14s do_so %s (%s)"
          % ("khớp" if ok else "LỆCH", co[0], co[1], S["top3_day"], S["nam_day"]))
    n = C["nganh"]
    for ten, khoa in (("Electronics", "dien_tu"), ("Agriculture", "nong_san"),
                      ("Textiles", "det_may"), ("Machinery", "may_moc")):
        for y, hau in ((NAM_DAU, "dau"), (NAM, "cuoi")):
            co = R.fmt_pct(float(n.loc[y].get(R_ID[ten], 0.0)))
            ok = co == S["%s_%s" % (khoa, hau)]
            loi += 0 if ok else 1
            if not ok:
                print("     LỆCH  bảng ngành %s %d: %s ≠ %s"
                      % (ten, y, co, S["%s_%s" % (khoa, hau)]))
    print("     bảng ngành: 4 ngành × 2 năm đối chiếu với do_so()")

    thieu_tieu_de = sorted(t for t, m in meta.items() if not m["tieu_de"])
    ngoai = sorted(set(meta) - set(dung))
    print("\n  9. Dashboard: %d biểu đồ · thiếu tiêu đề: %d · ngoài bộ của bài viết: %d"
          % (len(meta), len(thieu_tieu_de), len(ngoai)))
    for t in thieu_tieu_de + ngoai:
        print("     LỖI  %s" % t)
    loi += len(thieu_tieu_de) + len(ngoai)
    return loi


def so_go_tay():
    """Chữ tự viết của dashboard (nhãn ô, chip) cũng không được chứa số gõ tay."""
    chu = [o["nhan"] for o in O_CHI_SO] + [t["nhan"] for t in TAB]
    chu += [x for t in TAB for cap in t["chip"] for x in cap]
    return [s for s in chu
            if re.search(r"\d", BW.MA_DINH_DANH.sub("", BS.O_TRONG.sub("", s)))]

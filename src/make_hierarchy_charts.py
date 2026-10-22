"""Dựng treemap và sunburst cơ cấu xuất khẩu Việt Nam theo cây HS92 (T12, T13).

Đây là phần trực quan hóa CÂY của đồ án — họ kỹ thuật ở mục 9.1 của giáo trình:
nhóm lấp đầy không gian (space-filling), gồm bố cục chữ nhật (treemap) và bố cục
xuyên tâm (sunburst). Cùng một dữ liệu, cùng một bảng màu, hai cách biểu diễn —
để so sánh trực tiếp xem mỗi cách làm lộ ra điều gì và giấu đi điều gì.

Dữ liệu
-------
- ``data/atlas/product_hs92.csv``  : cây sản phẩm HS92, 6.390 nút, 4 tầng
- ``data/atlas/cp_year_hs2.csv``   : xuất khẩu theo nước × nhóm HS2 × năm

Chỉ dùng hai tầng đầu của cây — 10 ngành cấp 1 và 97 nhóm cấp 2 — đúng ranh giới
đã chốt ở ``docs/cau-hoi-nghien-cuu.md`` mục 4.

Màu lấy từ ``src/reference_data.py``, KHÔNG chép mã hex vào đây (quy định ở
``docs/style-guide.md``). Bảng màu đã qua ``src/check_palette.py``: ΔE2000 ≥ 15 ở
mắt thường và ≥ 10 ở cả ba dạng mù màu.

Chạy
----
    python src/make_hierarchy_charts.py              # năm mốc 2023
    python src/make_hierarchy_charts.py --year 1995
    python src/make_hierarchy_charts.py --country THA

Xuất ra ``output/``: bản .html tương tác (dùng khi demo, bấm vào ô để drill-down)
và bản .png tĩnh (dán vào slide).
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reference_data as R  # noqa: E402

try:
    import plotly.graph_objects as go
except ImportError:
    sys.exit("Thiếu plotly. Chạy: python -m pip install plotly kaleido")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, "data", "atlas")
OUTDIR = os.path.join(ROOT, "output")

# Viền trắng quanh mỗi ô. Bắt buộc: bốn màu trong bảng (#DDCC77, #44AA99,
# #88CCEE, #DDDDDD) có tương phản với nền trắng dưới 3:1, không có viền thì
# không thấy mép mảng. Xem docs/style-guide.md mục 1.
TILE_BORDER = dict(color="#FFFFFF", width=1)

# Nhom cap 2 nho hon nguong nay (% tong xuat khau) thi khong ghi nhan len o.
# Duoi ~0,8% chu da nho toi muc khong doc duoc o kich thuoc trinh chieu.
LABEL_MIN_SHARE = 0.8


def load_tree():
    """Đọc cây HS92. Trả về dict product_id -> thông tin nút."""
    path = os.path.join(ATLAS, "product_hs92.csv")
    tree = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tree[int(r["product_id"])] = {
                "level": int(r["product_level"]),
                "parent": int(r["product_parent_id"]) if r["product_parent_id"] else None,
                "name": r["product_name"],
                "short": r["product_name_short"],
                "code": r["product_hs92_code"],
            }
    return tree


def sector_of(tree, pid):
    """Leo ngược lên tầng 1 để biết nút thuộc ngành nào — dùng để tô màu."""
    node = tree.get(pid)
    while node and node["level"] > 1:
        node = tree.get(node["parent"])
    return node


def sector_index(tree):
    """Dựng sẵn bảng tra product_id -> (sector_id, số thứ tự ngành 1..10).

    Trước đây mỗi lần cần biết một nút thuộc ngành nào, code leo ngược lên tầng 1
    rồi quét cả 6.390 nút để tìm lại id của nút đó — O(số nút) cho mỗi lần tra.
    Với 97 nhóm HS2 thì không ai thấy chậm, nhưng nếu sau này đổi sang HS4 hoặc
    HS6 (1.243 / 5.040 nhóm) thì chi phí nhân lên hàng chục lần mà không có lý do
    gì chính đáng. Dựng bảng một lần ở đây, mọi chỗ khác tra bằng dict.

    Số thứ tự ngành đánh theo thứ tự product_id của tầng 1 — đúng thứ tự mà
    SECTOR_PALETTE và SECTOR_NAME_VI trong reference_data.py dùng.
    """
    level1 = sorted(k for k, n in tree.items() if n["level"] == 1)
    order = {sid: i + 1 for i, sid in enumerate(level1)}

    index = {}
    for pid in tree:
        cur = pid
        seen = set()
        while cur is not None and cur in tree and tree[cur]["level"] > 1:
            if cur in seen:          # cây hỏng có chu trình — bỏ qua nút này
                cur = None
                break
            seen.add(cur)
            cur = tree[cur]["parent"]
        if cur is not None and cur in order:
            index[pid] = (cur, order[cur])
    return index


def load_exports(country, year):
    """Xuất khẩu của một nước trong một năm, theo nhóm HS2."""
    path = os.path.join(ATLAS, "cp_year_hs2.csv")
    if not os.path.exists(path):
        sys.exit(
            "Thiếu %s\nChạy: python src/download_atlas.py --only cp_year_hs2.csv" % path
        )
    out = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["country_iso3_code"] != country or int(r["year"]) != year:
                continue
            v = float(r["export_value"] or 0)
            if v > 0:
                out[int(r["product_id"])] = out.get(int(r["product_id"]), 0.0) + v
    if not out:
        sys.exit("Không có dữ liệu cho %s năm %d" % (country, year))
    return out


def build_nodes(tree, exports):
    """Dựng danh sách nút phẳng mà plotly cần: ids / labels / parents / values.

    Tầng 1 là 10 ngành, tầng 2 là các nhóm HS2 có xuất khẩu. Giá trị của ngành
    được plotly tự cộng từ các con, nên chỉ truyền giá trị ở tầng lá.
    """
    index = sector_index(tree)

    sector_total = {}
    for pid, v in exports.items():
        hit = index.get(pid)
        if hit:
            sector_total[hit[0]] = sector_total.get(hit[0], 0.0) + v

    ids, labels, parents, values, colors, hovers = [], [], [], [], [], []
    total = sum(exports.values())

    # Tầng 1 — ngành
    for sid in sorted(sector_total, key=lambda k: -sector_total[k]):
        node = tree[sid]
        sector_no = index[sid][1]
        ids.append("s%d" % sid)
        labels.append(R.SECTOR_NAME_VI.get(sector_no, node["short"]))
        parents.append("")
        values.append(0)  # plotly tự cộng từ con
        colors.append(R.SECTOR_PALETTE[sector_no])
        hovers.append(
            "<b>%s</b><br>%s — %s tổng xuất khẩu<extra></extra>"
            % (R.SECTOR_NAME_VI.get(sector_no, node["short"]),
               R.fmt_usd(sector_total[sid]),
               R.fmt_pct(sector_total[sid] / total * 100))
        )

    # Tầng 2 — nhóm HS2
    for pid, v in sorted(exports.items(), key=lambda kv: -kv[1]):
        node = tree.get(pid)
        if not node:
            continue
        hit = index.get(pid)
        if not hit:
            continue
        sid, sector_no = hit
        ids.append("p%d" % pid)
        labels.append(R.HS2_NAME_VI.get(node["code"], node["short"]))
        parents.append("s%d" % sid)
        values.append(v)
        colors.append(R.SECTOR_PALETTE[sector_no])
        hovers.append(
            "<b>%s</b> (HS %s)<br>%s — %s tổng xuất khẩu"
            "<br>Ngành: %s<extra></extra>"
            % (R.HS2_NAME_VI.get(node["code"], node["name"]), node["code"],
               R.fmt_usd(v), R.fmt_pct(v / total * 100),
               R.SECTOR_NAME_VI.get(sector_no, ""))
        )

    # Nhãn hiển thị trên ô. Ngành cấp 1 LUÔN có nhãn — nếu bỏ thì danh tính
    # ngành chỉ còn truyền bằng màu, người mù màu và bản in đen trắng mất thông
    # tin. Nhóm cấp 2 chỉ ghi nhãn khi ô đủ lớn; ô nhỏ hơn ngưỡng để trống và
    # người xem tra bằng hover.
    texts = []
    n_sectors = len(sector_total)
    for i, (lab, val) in enumerate(zip(labels, values)):
        if i < n_sectors:
            sid = int(ids[i][1:])
            texts.append("<b>%s</b><br>%s"
                         % (lab, R.fmt_pct(sector_total[sid] / total * 100)))
        else:
            share = val / total * 100
            texts.append("<b>%s</b><br>%s" % (lab, R.fmt_pct(share))
                         if share >= LABEL_MIN_SHARE else "")

    return dict(ids=ids, labels=labels, parents=parents, values=values,
                colors=colors, hovers=hovers, texts=texts, total=total,
                n_sectors=n_sectors)


# Khung tính bằng POINT theo B16 — xem reference_data.xuat_png.
FIG_H_INCH = 4.00
# Sunburst là hình TRÒN: bề ngang thừa không giúp gì, chỉ chiều cao mới làm
# vành ngoài dày ra. Cho nó khung cao hơn treemap để dán được nhiều nhãn hơn.
SUNBURST_H_INCH = 5.40
MARGIN_X = 8.0
TEXT_PAD = 6.0
LINE_H = 1.33
LABEL_FLOOR_PT = 7.0

SOURCE_TEXT = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab), phân "
               "loại HS92. Giá trị xuất khẩu, USD hiện hành.")


def _layout(title, subtitle, h_inch=None):
    """Bố cục chung của treemap và sunburst, đặt chữ bằng tay theo B16.

    layout.title của plotly không tự ngắt dòng, nên ở khung point câu tiêu đề
    dài hơn bề ngang khung sẽ chạy tuột ra ngoài mép. Ngắt trước bằng wrap_pt
    rồi tự đặt, và tự tính luôn lề trên theo số dòng thật.
    """
    h_inch = FIG_H_INCH if h_inch is None else h_inch
    w_pt = R.khung_pt(R.FIG_WIDTH_FULL)
    h_pt = R.khung_pt(h_inch)
    t_w = w_pt - 2 * MARGIN_X - 2 * TEXT_PAD
    tw = R.wrap_pt(title, R.FONT_SIZES["title"], t_w)
    sw = R.wrap_pt(subtitle, R.FONT_SIZES["subtitle"], t_w)
    cw = R.wrap_pt(SOURCE_TEXT, R.FONT_SIZES["footnote"], t_w)
    h_title = R.n_lines(tw) * R.FONT_SIZES["title"] * LINE_H
    h_sub = R.n_lines(sw) * R.FONT_SIZES["subtitle"] * LINE_H
    m_t = TEXT_PAD + h_title + h_sub + TEXT_PAD
    m_b = 8.0 + R.n_lines(cw) * R.FONT_SIZES["footnote"] * LINE_H + TEXT_PAD
    plot_h = h_pt - m_t - m_b

    def ann(text, y, size, color):
        return dict(text=text, showarrow=False, xref="paper", yref="paper",
                    x=0, y=y, xshift=-(MARGIN_X - TEXT_PAD), xanchor="left",
                    yanchor="top", align="left",
                    font=dict(size=size, color=color))

    return dict(
        font=dict(family=", ".join(R.FONT_STACK), size=R.FONT_SIZES["legend"]),
        # Dấu thập phân và dấu phân nhóm cho MỌI con số plotly TỰ định dạng:
        # vạch trục, %{...:.1f} trong hovertemplate. fmt_vn chỉ lo những chuỗi
        # Python dựng sẵn; chuỗi nào plotly dựng thì nằm ở đây.
        separators=",.",
        margin=dict(t=m_t, l=MARGIN_X, r=MARGIN_X, b=m_b),
        paper_bgcolor="#FFFFFF",
        # Chữ trong ô tự co cho vừa ô; không chặn sàn thì ô nhỏ in ra chữ 2–3 pt.
        # mode="hide" nghĩa là thà giấu còn hơn in dưới sàn 7 pt của §7.
        uniformtext=dict(minsize=LABEL_FLOOR_PT, mode="hide"),
        annotations=[
            ann(tw, 1 + (m_t - TEXT_PAD) / plot_h, R.FONT_SIZES["title"], None),
            ann(sw, 1 + (m_t - TEXT_PAD - h_title) / plot_h,
                R.FONT_SIZES["subtitle"], "#555555"),
            ann(cw, -(8.0 / plot_h), R.FONT_SIZES["footnote"], "#777777"),
        ],
    )


def make_treemap(d, country_vi, year):
    fig = go.Figure(go.Treemap(
        ids=d["ids"], labels=d["labels"], parents=d["parents"], values=d["values"],
        branchvalues="remainder",
        marker=dict(colors=d["colors"], line=TILE_BORDER),
        hovertemplate=d["hovers"],
        text=d["texts"], texttemplate="%{text}",
        textposition="middle center",
        tiling=dict(packing="squarify"),  # treemap vuông hóa — Bruls và cộng sự
        maxdepth=2,
    ))
    top = d["labels"][0]
    fig.update_layout(**_layout(
        "%s: %s chiếm phần lớn nhất trong rổ hàng xuất khẩu năm %d" % (country_vi, top, year),
        "Treemap — bố cục chữ nhật lấp đầy không gian. Diện tích ô tỉ lệ với giá trị xuất khẩu. "
        "Bấm vào một ngành để xem các nhóm hàng bên trong.",
    ))
    return fig


# Vành ngoài của sunburst: lát mỏng hơn mức này thì không dán chữ.
#
# layout.uniformtext (đang bật cho treemap) KHÔNG chặn được chữ ở sunburst khi
# đặt insidetextorientation="radial" — plotly vẫn co chữ xuống khoảng 3 pt cho
# vừa lát, tức dưới hẳn sàn 7 pt của style guide §7. Nên tự cắt: lát nào không
# đủ cung để chứa một dòng 7 pt thì bỏ chữ, còn số liệu vẫn đọc được khi rê
# chuột. Ngưỡng suy từ hình học, không chọn bừa — xem `_nguong_vanh_ngoai`.
def _nguong_vanh_ngoai(h_inch):
    """Tỷ trọng tối thiểu để một lát vành ngoài chứa nổi một dòng chữ 7 pt.

    Đường kính vẽ được xấp xỉ chiều cao phần vẽ; vành ngoài nằm ở bán kính
    khoảng 0,75 lần bán kính ngoài, nên cung của một lát chiếm tỷ trọng p là
    ``p · 2π · 0,75 · R``. Cần cung ấy ít nhất bằng một dòng chữ.
    """
    r = R.khung_pt(h_inch) * 0.5 * 0.62      # bán kính vẽ được, trừ lề chữ
    chu_vi = 2 * 3.14159 * 0.75 * r
    return (LABEL_FLOOR_PT * LINE_H) / chu_vi * 100.0


def make_sunburst(d, country_vi, year, h_inch):
    nguong = _nguong_vanh_ngoai(h_inch)
    # Vành TRONG nằm ở bán kính bằng khoảng một nửa vành ngoài, nên cùng một tỷ
    # trọng cho cung ngắn hơn một nửa — ngưỡng phải gấp đôi. Bỏ qua chỗ này thì
    # ba ngành mỏng (Đá, Khoáng sản, Phương tiện vận tải) vẫn in chữ ~3 pt.
    nguong_trong = nguong * 2.0
    tong = float(d["total"])
    # Nút cấp 1 có values = 0 vì branchvalues="remainder" để plotly tự cộng từ
    # con. Lấy thẳng values của chúng thì tỷ trọng ra 0 và MỌI nhãn ngành bị
    # cắt. Phải cộng con lại mới ra bề dày thật của lát.
    cong_con = {}
    for pid, val in zip(d["parents"], d["values"]):
        if pid:
            cong_con[pid] = cong_con.get(pid, 0.0) + float(val)
    texts = []
    for nid, pid, val, txt in zip(d["ids"], d["parents"], d["values"],
                                  d["texts"]):
        thuc = float(val) if pid else cong_con.get(nid, 0.0)
        share = (thuc / tong * 100.0) if tong else 0.0
        muc = nguong if pid else nguong_trong
        texts.append("" if share < muc else txt)
    n_ngoai = sum(1 for pid in d["parents"] if pid)
    print("  Nhãn: vành ngoài từ %s (%s/%s lát), vành trong từ %s (%s/%s ngành)"
          % (R.fmt_pct(nguong, 2),
             R.fmt_vn(sum(1 for t, pid in zip(texts, d["parents"]) if t and pid), 0),
             R.fmt_vn(n_ngoai, 0), R.fmt_pct(nguong_trong, 2),
             R.fmt_vn(sum(1 for t, pid in zip(texts, d["parents"])
                          if t and not pid), 0),
             R.fmt_vn(len(d["parents"]) - n_ngoai, 0)))
    fig = go.Figure(go.Sunburst(
        ids=d["ids"], labels=d["labels"], parents=d["parents"], values=d["values"],
        branchvalues="remainder",
        marker=dict(colors=d["colors"], line=TILE_BORDER),
        hovertemplate=d["hovers"],
        text=texts, texttemplate="%{text}",
        insidetextorientation="radial",
        maxdepth=2,
    ))
    fig.update_layout(**_layout(
        "%s: cùng dữ liệu đó, nhìn theo cấu trúc phân cấp — năm %d" % (country_vi, year),
        "Sunburst — bố cục xuyên tâm lấp đầy không gian. Vành trong là 10 ngành cấp 1, "
        "vành ngoài là các nhóm HS2. Lát quá mỏng để chứa một dòng chữ 7 pt thì "
        "bỏ nhãn, số liệu xem khi rê chuột. Bấm vào một vành để khoan sâu.",
        h_inch))
    return fig


def save(fig, name, h_inch=None):
    os.makedirs(OUTDIR, exist_ok=True)
    html = os.path.join(OUTDIR, name + ".html")
    fig.write_html(html, include_plotlyjs="cdn", config={"displayModeBar": False})
    print("  %s" % html)
    try:
        png = os.path.join(OUTDIR, name + ".png")
        R.xuat_png(fig, png, R.FIG_WIDTH_FULL,
                   FIG_H_INCH if h_inch is None else h_inch)
        print("  %s" % png)
    except Exception as exc:
        print("  (không xuất được PNG: %s — bản .html vẫn dùng được)" % exc)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--country", default="VNM")
    args = ap.parse_args()

    country_vi = R.COUNTRY_VI.get(args.country, (args.country,))[0]

    print("Đọc cây HS92...")
    tree = load_tree()
    n1 = sum(1 for n in tree.values() if n["level"] == 1)
    n2 = sum(1 for n in tree.values() if n["level"] == 2)
    print("  %d nút, tầng 1: %d ngành, tầng 2: %d nhóm" % (len(tree), n1, n2))

    print("Đọc xuất khẩu %s năm %d..." % (args.country, args.year))
    exports = load_exports(args.country, args.year)
    d = build_nodes(tree, exports)
    print("  %d nhóm hàng có xuất khẩu, tổng %s" % (len(exports), R.fmt_usd(d["total"])))

    print("Dựng biểu đồ:")
    save(make_treemap(d, country_vi, args.year), "treemap_%s_%d" % (args.country.lower(), args.year))
    save(make_sunburst(d, country_vi, args.year, SUNBURST_H_INCH),
         "sunburst_%s_%d" % (args.country.lower(), args.year), SUNBURST_H_INCH)
    print("Xong.")


if __name__ == "__main__":
    main()

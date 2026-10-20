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


def _layout(title, subtitle):
    return dict(
        title=dict(
            text="<b>%s</b><br><span style='font-size:%dpx;color:#555'>%s</span>"
                 % (title, R.FONT_SIZES["subtitle"], subtitle),
            x=0.01, xanchor="left", font=dict(size=R.FONT_SIZES["title"] + 4),
        ),
        font=dict(family=", ".join(R.FONT_STACK), size=R.FONT_SIZES["legend"]),
        # Dấu thập phân và dấu phân nhóm cho MỌI con số plotly TỰ định dạng:
        # vạch trục, %{...:.1f} trong hovertemplate. fmt_vn chỉ lo những chuỗi
        # Python dựng sẵn; chuỗi nào plotly dựng thì nằm ở đây.
        separators=",.",
        margin=dict(t=85, l=8, r=8, b=28),
        paper_bgcolor="#FFFFFF",
        annotations=[dict(
            text="Nguồn: Atlas of Economic Complexity (Harvard Growth Lab), phân loại HS92. "
                 "Giá trị xuất khẩu, USD hiện hành.",
            showarrow=False, xref="paper", yref="paper", x=0, y=-0.04,
            xanchor="left", font=dict(size=R.FONT_SIZES["footnote"], color="#777"),
        )],
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


def make_sunburst(d, country_vi, year):
    fig = go.Figure(go.Sunburst(
        ids=d["ids"], labels=d["labels"], parents=d["parents"], values=d["values"],
        branchvalues="remainder",
        marker=dict(colors=d["colors"], line=TILE_BORDER),
        hovertemplate=d["hovers"],
        text=d["texts"], texttemplate="%{text}",
        insidetextorientation="radial",
        maxdepth=2,
    ))
    fig.update_layout(**_layout(
        "%s: cùng dữ liệu đó, nhìn theo cấu trúc phân cấp — năm %d" % (country_vi, year),
        "Sunburst — bố cục xuyên tâm lấp đầy không gian. Vành trong là 10 ngành cấp 1, "
        "vành ngoài là các nhóm HS2. Bấm vào một vành để khoan sâu.",
    ))
    return fig


def save(fig, name):
    os.makedirs(OUTDIR, exist_ok=True)
    html = os.path.join(OUTDIR, name + ".html")
    fig.write_html(html, include_plotlyjs="cdn", config={"displayModeBar": False})
    print("  %s" % html)
    try:
        png = os.path.join(OUTDIR, name + ".png")
        fig.write_image(png, width=R.FIG_WIDTH_FULL * R.FIG_DPI_SCREEN,
                        height=int(R.FIG_HEIGHT_DEFAULT * R.FIG_DPI_SCREEN), scale=2)
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
    save(make_sunburst(d, country_vi, args.year), "sunburst_%s_%d" % (args.country.lower(), args.year))
    print("Xong.")


if __name__ == "__main__":
    main()

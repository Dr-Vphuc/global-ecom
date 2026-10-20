"""Sankey: nguồn nhập khẩu → Việt Nam → thị trường xuất khẩu (T19).

Hình này tồn tại để KIỂM một giả thuyết, không phải để minh họa một kết luận.
Giả thuyết: "Việt Nam là nút trung chuyển của chuỗi cung ứng châu Á."

Câu trả lời hóa ra là: ĐÚNG MỘT NỬA, và hai nửa đó phải nói tách nhau ra, nếu
không sẽ thành một tuyên bố sai.

Nửa SAI — xét theo tô-pô mạng lưới
-----------------------------------
Betweenness centrality của Việt Nam trong đồ thị đã lọc là 0,0000, đồng hạng
với 57 nước khác (tính ở T18). Việt Nam KHÔNG nằm trên đường đi ngắn nhất giữa
các nước khác. Lý do nằm ở T09: mạng này có mật độ 51,8%, ai cũng nối thẳng với
ai, nên chẳng ai cần đi vòng qua ai cả. Trong một mạng như vậy, "nút trung
chuyển" theo nghĩa lý thuyết đồ thị gần như không tồn tại — với bất kỳ nước nào.

Nửa ĐÚNG — xét theo dòng tiền
------------------------------
Việt Nam nhập 332,1 tỷ USD và xuất 385,5 tỷ USD trong năm 2023. Tức là cứ mỗi
đồng hàng bán ra, có 86 xu là hàng đã mua từ nước khác. Giá trị gia tăng trong
nước chỉ 13,9%. Đó chính là chân dung của một công xưởng lắp ráp: mua linh
kiện, ráp lại, bán đi.

Hình Sankey này cho thấy nửa thứ hai. Nó KHÔNG chứng minh được nửa thứ nhất, và
đây là giới hạn phải nói thẳng:

    ⚠️ Sankey này KHÔNG truy vết được một lô hàng cụ thể. Dữ liệu Atlas cho
    biết Việt Nam nhập bao nhiêu từ Hàn Quốc và xuất bao nhiêu sang Hoa Kỳ,
    nhưng KHÔNG cho biết hàng nhập từ Hàn Quốc có đi tiếp sang Hoa Kỳ hay
    không. Chiều rộng dải bên trái và bên phải nút Việt Nam là hai phép đo
    riêng biệt được đặt cạnh nhau, không phải một dòng chảy liên tục. Ai đọc
    hình này thành "linh kiện Hàn Quốc chảy qua Việt Nam sang Mỹ" là đã đọc
    thêm thứ dữ liệu không nói.

Chạy
----
    python src/make_sankey.py
    python src/make_sankey.py --top 10 --year 2015
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import graph_common as GC  # noqa: E402
import reference_data as R  # noqa: E402

try:
    import plotly.graph_objects as go
except ImportError:
    sys.exit("Thiếu plotly. Chạy: python -m pip install plotly kaleido")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "data", "processed")

FOCUS = "VNM"
# Xám cho dải thường, đậm hơn cho dải của các nước ASEAN — để thấy phần thương
# mại nội khối mà Việt Nam vẫn hay được nói là gắn bó.
LINK_NORMAL = "rgba(150,150,150,0.34)"
LINK_ASEAN = "rgba(60,60,60,0.46)"
NODE_SIDE = "#B8B8B8"
NODE_FOCUS = "#2A2A2A"


def log(msg):
    print(msg)
    sys.stdout.flush()


def load_flows(year):
    """Trả về (nhập về VN, xuất từ VN) — mỗi cái là list (đối tác, giá trị)."""
    path = os.path.join(PROC, "edges.csv")
    if not os.path.exists(path):
        sys.exit("Thiếu %s. Chạy: python src/build_intermediate.py" % path)
    inn, out = [], []
    with open(path, encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if int(r["year"]) != year:
                continue
            v = float(r["export_value"])
            if r["target_iso3"] == FOCUS:
                inn.append((r["source_iso3"], v))
            elif r["source_iso3"] == FOCUS:
                out.append((r["target_iso3"], v))
    return sorted(inn, key=lambda kv: -kv[1]), sorted(out, key=lambda kv: -kv[1])


def topn(rows, n):
    """Giữ n đối tác lớn nhất, gộp phần còn lại thành 'Các nước khác'.

    Gộp chứ không cắt bỏ: nếu cắt, tổng hai bên nút Việt Nam sẽ không còn khớp
    với kim ngạch thật và mọi tỷ lệ đọc từ hình đều sai.
    """
    head = rows[:n]
    tail = rows[n:]
    if tail:
        head = head + [("__OTHER__", sum(v for _, v in tail))]
    return head, len(tail)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--top", type=int, default=12,
                    help="số đối tác hiện riêng mỗi bên (mặc định 12)")
    args = ap.parse_args()

    meta = {}
    with open(os.path.join(PROC, "nodes.csv"), encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            meta[r["country_iso3"]] = r

    log("Đọc luồng của Việt Nam năm %d..." % args.year)
    inn_all, out_all = load_flows(args.year)
    imp_total = sum(v for _, v in inn_all)
    exp_total = sum(v for _, v in out_all)
    log("  nhập %s từ %d nguồn" % (R.fmt_usd(imp_total), len(inn_all)))
    log("  xuất %s sang %d thị trường" % (R.fmt_usd(exp_total), len(out_all)))

    inn, n_other_in = topn(inn_all, args.top)
    out, n_other_out = topn(out_all, args.top)

    def label(iso, side):
        if iso == "__OTHER__":
            n = n_other_in if side == "in" else n_other_out
            return "%d nước khác" % n
        return GC.name_vi(iso, meta)

    # --- Dựng danh sách nút: trái | Việt Nam | phải ------------------------
    labels, colors, xs, ys, customs = [], [], [], [], []

    def add(lbl, color, x, y, custom):
        labels.append(lbl)
        colors.append(color)
        xs.append(x)
        ys.append(y)
        customs.append(custom)
        return len(labels) - 1

    left_idx = {}
    for i, (iso, v) in enumerate(inn):
        left_idx[iso] = add(label(iso, "in"), NODE_SIDE, 0.001,
                            (i + 0.5) / len(inn),
                            "%s → Việt Nam: %s (%s hàng Việt Nam nhập)"
                            % (label(iso, "in"), R.fmt_usd(v),
                               R.fmt_pct(v / imp_total * 100)))

    vn = add("<b>VIỆT NAM</b>", NODE_FOCUS, 0.5, 0.5,
             "Nhập %s · Xuất %s<br>Giá trị gia tăng trong nước: %s"
             % (R.fmt_usd(imp_total), R.fmt_usd(exp_total),
                R.fmt_pct((exp_total - imp_total) / exp_total * 100)))

    right_idx = {}
    for i, (iso, v) in enumerate(out):
        right_idx[iso] = add(label(iso, "out"), NODE_SIDE, 0.999,
                             (i + 0.5) / len(out),
                             "Việt Nam → %s: %s (%s hàng Việt Nam xuất)"
                             % (label(iso, "out"), R.fmt_usd(v),
                                R.fmt_pct(v / exp_total * 100)))

    # --- Dải ---------------------------------------------------------------
    src, dst, val, lcol, lhov = [], [], [], [], []
    for iso, v in inn:
        src.append(left_idx[iso])
        dst.append(vn)
        val.append(v)
        lcol.append(LINK_ASEAN if iso in R.FOCUS_ISO3 else LINK_NORMAL)
        lhov.append("<b>%s → Việt Nam</b><br>%s — %s tổng hàng nhập<extra></extra>"
                    % (label(iso, "in"), R.fmt_usd(v),
                       R.fmt_pct(v / imp_total * 100)))
    for iso, v in out:
        src.append(vn)
        dst.append(right_idx[iso])
        val.append(v)
        lcol.append(LINK_ASEAN if iso in R.FOCUS_ISO3 else LINK_NORMAL)
        lhov.append("<b>Việt Nam → %s</b><br>%s — %s tổng hàng xuất<extra></extra>"
                    % (label(iso, "out"), R.fmt_usd(v),
                       R.fmt_pct(v / exp_total * 100)))

    value_added = (exp_total - imp_total) / exp_total * 100

    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            label=labels, color=colors, x=xs, y=ys,
            pad=13, thickness=16,
            line=dict(color="#FFFFFF", width=0.8),
            customdata=customs,
            hovertemplate="%{customdata}<extra></extra>",
        ),
        link=dict(source=src, target=dst, value=val, color=lcol,
                  customdata=lhov, hovertemplate="%{customdata}"),
        textfont=dict(size=R.FONT_SIZES["legend"], color="#222222"),
    ))

    fig.update_layout(**GC.base_layout(
        # Số "xu" tính từ dữ liệu, KHÔNG viết cứng. Bản đầu viết thẳng "86 xu"
        # kèm một nhánh dự phòng diễn đạt khác hẳn khi số đổi — nghĩa là chạy
        # với --year khác sẽ ra một tiêu đề có văn phong khác, và con số 86 chỉ
        # tình cờ đúng với năm mặc định. Một công thức, một cách nói.
        title="Việt Nam mua %d xu hàng ngoại cho mỗi đồng hàng bán ra"
              % round(100 - value_added),
        subtitle="Nhập %s từ %d nguồn, xuất %s sang %d thị trường, năm %d. "
                 "Giá trị gia tăng trong nước chỉ %s. Dải đậm là các nước "
                 "ASEAN."
                 % (R.fmt_usd(imp_total), len(inn_all), R.fmt_usd(exp_total),
                    len(out_all), args.year, R.fmt_pct(value_added)),
        note="Nguồn: Atlas of Economic Complexity (Harvard Growth Lab), năm %d. "
             "⚠️ Hai bên nút Việt Nam là HAI PHÉP ĐO RIÊNG đặt cạnh nhau, không "
             "phải một dòng chảy liên tục: dữ liệu không truy được lô hàng nhập "
             "từ nước A có đi tiếp sang nước B hay không. Hình này đo mức phụ "
             "thuộc đầu vào, KHÔNG chứng minh trung chuyển."
             % args.year,
        margin=dict(t=108, l=10, r=10, b=70),
        showlegend=False,
    ))

    GC.save(fig, "sankey_vnm_%d" % args.year, width=1500, height=1000, log=log)

    # --- Bằng chứng --------------------------------------------------------
    log("")
    log("GIẢ THUYẾT 'VIỆT NAM LÀ NÚT TRUNG CHUYỂN' — hai cách đo, hai câu trả lời:")
    log("")
    log("  Theo tô-pô mạng  : betweenness = 0,0000, đồng hạng với 57 nước.")
    log("                     KHÔNG phải nút trung chuyển. Mạng mật độ 51,8%,")
    log("                     ai cũng nối thẳng với ai, không ai cần đi vòng.")
    log("")
    log("  Theo dòng tiền   : nhập %s / xuất %s = %s."
        % (R.fmt_usd(imp_total), R.fmt_usd(exp_total),
           R.fmt_pct(imp_total / exp_total * 100)))
    log("                     Giá trị gia tăng trong nước %s."
        % R.fmt_pct(value_added))
    log("                     ĐÚNG là công xưởng lắp ráp.")
    log("")
    log("Top 5 nguồn nhập:")
    for iso, v in inn_all[:5]:
        log("  %-16s %14s  %6s" % (GC.name_vi(iso, meta), R.fmt_usd(v),
                                   R.fmt_pct(v / imp_total * 100)))
    log("Top 5 thị trường xuất:")
    for iso, v in out_all[:5]:
        log("  %-16s %14s  %6s" % (GC.name_vi(iso, meta), R.fmt_usd(v),
                                   R.fmt_pct(v / exp_total * 100)))

    # Con số cho phần thuyết trình: Trung Quốc vào, Hoa Kỳ ra.
    top_in = inn_all[0] if inn_all else None
    top_out = out_all[0] if out_all else None
    if top_in and top_out:
        log("")
        log("  Nguồn nhập lớn nhất là %s, thị trường xuất lớn nhất là %s."
            % (GC.name_vi(top_in[0], meta), GC.name_vi(top_out[0], meta)))
        log("  Đây là hình dạng kinh điển của một nền kinh tế gia công.")


if __name__ == "__main__":
    main()

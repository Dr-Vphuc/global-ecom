"""Chord diagram luồng thương mại giữa các khối, Việt Nam làm trọng tâm (T17).

Chord là cách thứ ba để nhìn cùng một mạng lưới, sau node-link (T15) và ma trận
kề (T16). Mỗi cung trên vòng tròn là một khối; mỗi dải ruy-băng là dòng hàng
giữa hai khối, bề rộng tỷ lệ với giá trị.

Ba khác biệt có chủ ý so với T15 và T16
---------------------------------------
1. **Dùng đồ thị ĐẦY ĐỦ, không lọc ngưỡng.** Ngưỡng ở T10 sinh ra để cứu hình
   node-link khỏi 27.535 cạnh chồng lên nhau. Chord không gặp vấn đề đó vì nó
   đã gộp 231 nước thành một nhúm khối — mỗi cặp khối chỉ còn một dải. Lọc thêm
   chỉ làm mất 32% giá trị mà không được gì. Khác biệt này phải nói ra, vì nếu
   không người đọc sẽ tưởng ba hình dùng cùng một tập cạnh.

   Số khối KHÔNG viết cứng ở đâu cả — nó đếm từ dữ liệu, vì khối "Khác" (vùng
   cực, mã không phải quốc gia) chỉ xuất hiện ở những năm có số liệu cho nhóm
   đó. Bản đầu của hình này ghi cứng "9 khối" trong phụ đề trong khi thực tế vẽ
   10 cung — một con số sai in ngay trên hình.

2. **Việt Nam tách thành một khối riêng**, không nằm trong Đông Nam Á. Cả bài
   nói về Việt Nam; để nó lẫn vào 10 nước ASEAN khác thì chính câu hỏi nghiên
   cứu biến mất khỏi hình.

3. **Không tô màu theo khối.** Chín khối cần chín màu, mà bảng 10 màu ngành đã
   chiếm hết gam an toàn cho người mù màu (đo ở ``reference_data.py``). Thay vì
   bịa thêm một bảng màu trùng với bảng ngành, hình này tô theo NGHĨA: dải nào
   có Việt Nam thì đậm, dải còn lại xám nhạt. Mã hóa đó vừa trả lời đúng câu
   "Việt Nam làm trọng tâm", vừa không nợ thêm một bảng màu nào.

Chạy
----
    python src/make_chord.py
    python src/make_chord.py --year 1995
"""

from __future__ import annotations

import argparse
import csv
import math
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

R_IN, R_OUT = 0.86, 0.96      # bán kính trong / ngoài của cung
GAP = math.radians(2.6)        # khe giữa hai cung, tính bằng radian
VN_FILL = "rgba(40,40,40,0.62)"        # dải có Việt Nam
OTHER_FILL = "rgba(150,150,150,0.17)"  # dải còn lại
# Dải nhỏ hơn ngưỡng này (tính theo tổng thế giới) thì bỏ, nếu không vòng tròn
# đầy những sợi chỉ không đọc được.
#
# ⚠️ Ngưỡng này KHÔNG áp cho dải có Việt Nam. Việt Nam chỉ chiếm 2,1% thương
# mại thế giới, nên một luồng rất lớn ĐỐI VỚI VIỆT NAM vẫn nhỏ so với thế giới:
# luồng Việt Nam ↔ Đông Nam Á là 30 tỷ USD, dưới ngưỡng 32,5 tỷ, và bản đầu
# tiên của hình này đã lặng lẽ xóa mất nó. Một hình mang tên "lấy Việt Nam làm
# trọng tâm" mà giấu đi bốn trong tám luồng của Việt Nam thì tự phản lại tiêu
# đề của chính nó. Ngưỡng tuyệt đối luôn thiên vị kẻ lớn — đây đúng là cái bẫy
# mà phát hiện A5 đã ghi.
MIN_SHARE = 0.0015


def log(msg):
    print(msg)
    sys.stdout.flush()


def bloc_of(iso, region_of):
    if iso == "VNM":
        return "viet_nam"
    return R.BLOC_OF_REGION.get(region_of.get(iso, ""), "khac")


def load_bloc_matrix(year):
    """Gộp mọi luồng của một năm lên cấp khối. Trả về (ma trận, tổng thế giới)."""
    region_of = {}
    with open(os.path.join(PROC, "nodes.csv"), encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            region_of[r["country_iso3"]] = r["region"]

    m = {}
    total = 0.0
    path = os.path.join(PROC, "edges.csv")
    if not os.path.exists(path):
        sys.exit("Thiếu %s. Chạy: python src/build_intermediate.py" % path)
    with open(path, encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if int(r["year"]) != year:
                continue
            a = bloc_of(r["source_iso3"], region_of)
            b = bloc_of(r["target_iso3"], region_of)
            v = float(r["export_value"])
            m[(a, b)] = m.get((a, b), 0.0) + v
            total += v
    return m, total


def arc_points(a0, a1, rad, n=40):
    """Dãy điểm trên một cung tròn."""
    return [(rad * math.cos(a0 + (a1 - a0) * i / n),
             rad * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def bezier(p0, p1, n=40):
    """Đường cong bậc hai từ p0 tới p1, uốn về TÂM vòng tròn.

    Điểm điều khiển đặt ở gốc tọa độ, nên mọi dải đều cong vào giữa. Đó là
    điều làm chord đọc được: dải nối hai cung xa nhau thì cong sâu, dải nối hai
    cung kề nhau thì gần như thẳng, mắt phân biệt được ngay độ "xa" của quan hệ.
    """
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u * u * p0[0] + t * t * p1[0],
                    u * u * p0[1] + t * t * p1[1]))
    return out


def path_of(points):
    """Chuỗi SVG path khép kín từ danh sách điểm."""
    d = "M %.5f,%.5f " % points[0]
    for x, y in points[1:]:
        d += "L %.5f,%.5f " % (x, y)
    return d + "Z"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    args = ap.parse_args()

    log("Gộp luồng thương mại %d lên cấp khối..." % args.year)
    m, total = load_bloc_matrix(args.year)
    log("  tổng %s" % R.fmt_usd(total))

    blocs = [b for b in R.BLOC_ORDER
             if any(k[0] == b or k[1] == b for k in m)]
    # Tổng của một khối = xuất đi + nhập về. Luồng nội khối đếm một lần, vì nó
    # chiếm cả hai đầu của cùng một dải.
    size = {}
    for b in blocs:
        out = sum(v for (a, c), v in m.items() if a == b and c != b)
        inn = sum(v for (a, c), v in m.items() if c == b and a != b)
        self_ = m.get((b, b), 0.0)
        size[b] = out + inn + self_
    blocs = [b for b in blocs if size[b] > 0]

    # grand = tổng ĐỘ DÀI cung, dùng để chia góc. Nó KHÁC tổng thương mại:
    # mỗi luồng A→B được tính hai lần, một lần vào cung của A (xuất) và một
    # lần vào cung của B (nhập). Đó là đúng cho việc chia cung — cung của một
    # khối phải phản ánh cả hàng đi lẫn hàng về. Nhưng tuyệt đối KHÔNG được
    # dùng grand làm mẫu số cho câu "bao nhiêu % thương mại thế giới": làm vậy
    # thì mọi tỷ lệ bị chia cho một số gần gấp đôi và đều sai.
    # Mẫu số cho mọi phát biểu về thị phần là `total`, tổng xuất khẩu thật.
    grand = sum(size.values())
    span = 2 * math.pi - GAP * len(blocs)

    # --- Chia cung cho từng khối ------------------------------------------
    start = {}
    ang = math.pi / 2          # Việt Nam bắt đầu ở đỉnh vòng tròn
    for b in blocs:
        w = span * size[b] / grand
        start[b] = (ang, ang + w)
        ang += w + GAP

    # --- Trong mỗi cung, chia tiếp cho từng đối tác ------------------------
    # Thứ tự đối tác theo BLOC_ORDER để dải giữa hai khối luôn gặp nhau ở đúng
    # một chỗ, không bị xoắn.
    sub = {}
    for b in blocs:
        a0, a1 = start[b]
        cur = a0
        for p in blocs:
            v = m.get((b, p), 0.0) + (m.get((p, b), 0.0) if p != b else 0.0)
            if v <= 0:
                continue
            w = (a1 - a0) * v / size[b]
            sub[(b, p)] = (cur, cur + w)
            cur += w

    shapes, hover_x, hover_y, hover_t = [], [], [], []

    # --- Dải ruy-băng ------------------------------------------------------
    drawn = 0
    for i, a in enumerate(blocs):
        for b in blocs[i:]:
            v = m.get((a, b), 0.0) + (m.get((b, a), 0.0) if a != b else 0.0)
            touches_vn = "viet_nam" in (a, b)
            if v / total < MIN_SHARE and not touches_vn:
                continue
            if v <= 0:
                continue
            sa, sb = sub.get((a, b)), sub.get((b, a))
            if sa is None or sb is None:
                continue
            pts = arc_points(sa[0], sa[1], R_IN)
            pts += bezier(pts[-1], (R_IN * math.cos(sb[0]), R_IN * math.sin(sb[0])))
            pts += arc_points(sb[0], sb[1], R_IN)
            pts += bezier(pts[-1], (R_IN * math.cos(sa[0]), R_IN * math.sin(sa[0])))
            shapes.append(dict(
                type="path", path=path_of(pts),
                fillcolor=VN_FILL if touches_vn else OTHER_FILL,
                line=dict(width=0.4,
                          color="#222222" if touches_vn else "rgba(140,140,140,0.35)"),
                layer="below" if not touches_vn else "above",
            ))
            drawn += 1
            # Điểm hover vô hình đặt ở giữa dải.
            mid = ((sa[0] + sa[1] + sb[0] + sb[1]) / 4)
            rr = R_IN * 0.55
            hover_x.append(rr * math.cos(mid))
            hover_y.append(rr * math.sin(mid))
            ab = m.get((a, b), 0.0)
            ba = m.get((b, a), 0.0)
            if a == b:
                hover_t.append("<b>%s ↔ nội khối</b><br>%s<extra></extra>"
                               % (R.BLOC_NAME_VI[a], R.fmt_usd(ab)))
            else:
                hover_t.append(
                    "<b>%s ↔ %s</b><br>%s → %s: %s<br>%s → %s: %s"
                    "<br>tổng %s — %s thương mại thế giới<extra></extra>"
                    % (R.BLOC_NAME_VI[a], R.BLOC_NAME_VI[b],
                       R.BLOC_NAME_VI[a], R.BLOC_NAME_VI[b], R.fmt_usd(ab),
                       R.BLOC_NAME_VI[b], R.BLOC_NAME_VI[a], R.fmt_usd(ba),
                       R.fmt_usd(v), R.fmt_pct(v / total * 100)))

    # --- Cung của từng khối ------------------------------------------------
    ann = []
    for b in blocs:
        a0, a1 = start[b]
        pts = arc_points(a0, a1, R_OUT) + list(reversed(arc_points(a0, a1, R_IN)))
        is_vn = b == "viet_nam"
        shapes.append(dict(
            type="path", path=path_of(pts),
            fillcolor="#2A2A2A" if is_vn else "#B8B8B8",
            line=dict(color="#FFFFFF", width=1), layer="above",
        ))
        mid = (a0 + a1) / 2
        deg = math.degrees(mid) % 360
        ann.append(dict(
            x=1.045 * math.cos(mid), y=1.045 * math.sin(mid),
            text=("<b>%s</b>" % R.BLOC_NAME_VI[b]) if is_vn else R.BLOC_NAME_VI[b],
            showarrow=False,
            xanchor="left" if 90 > deg or deg > 270 else "right",
            font=dict(size=R.FONT_SIZES["legend"],
                      color="#000000" if is_vn else "#444444"),
        ))

    vn_out = sum(v for (a, b), v in m.items()
                 if a == "viet_nam" and b != "viet_nam")
    vn_total = size.get("viet_nam", 0.0)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hover_x, y=hover_y, mode="markers",
        marker=dict(size=16, color="rgba(0,0,0,0)"),
        hovertemplate=hover_t, showlegend=False,
    ))

    top2 = sorted(((b, v) for (a, b), v in m.items()
                   if a == "viet_nam" and b != "viet_nam"),
                  key=lambda kv: -kv[1])[:2]
    share2 = sum(v for _, v in top2) / vn_out * 100 if vn_out else 0

    lay = GC.base_layout(
        title="%s hàng Việt Nam bán ra đi về %s và %s"
              % (R.fmt_pct(share2), R.BLOC_NAME_VI[top2[0][0]],
                 R.BLOC_NAME_VI[top2[1][0]]),
        subtitle="Luồng thương mại giữa %d khối, năm %d. Bề rộng dải = giá trị "
                 "hai chiều. Dải có Việt Nam tô đậm, dải còn lại xám nhạt. "
                 "Việt Nam tách riêng khỏi Đông Nam Á vì cả bài nói về Việt Nam."
                 % (len(blocs), args.year),
        note="Nguồn: Atlas of Economic Complexity (Harvard Growth Lab), năm %d. "
             "Hình này dùng TOÀN BỘ %s xuất khẩu, KHÔNG lọc ngưỡng như T15 và "
             "T16 — gộp 231 nước thành %d khối đã đủ làm hình đọc được. "
             "Dải nhỏ hơn %s tổng bị bỏ để vòng tròn không đầy sợi chỉ."
             % (args.year, R.fmt_usd(total), len(blocs),
                R.fmt_pct(MIN_SHARE * 100, 2)),
        shapes=shapes,
        xaxis=dict(visible=False, range=[-1.42, 1.42]),
        yaxis=dict(visible=False, range=[-1.16, 1.16],
                   scaleanchor="x", scaleratio=1),
        margin=dict(t=108, l=10, r=10, b=58),
        showlegend=False,
    )
    lay["annotations"] = ann + list(lay["annotations"])
    fig.update_layout(**lay)

    GC.save(fig, "chord_%d" % args.year, width=1250, height=1150, log=log)
    log("  %d dải được vẽ" % drawn)

    # --- Bằng chứng cho tiêu đề -------------------------------------------
    log("")
    log("Việt Nam xuất đi đâu, năm %d (cơ sở của tiêu đề):" % args.year)
    rows = sorted(((b, v) for (a, b), v in m.items()
                   if a == "viet_nam" and b != "viet_nam"), key=lambda kv: -kv[1])
    cum = 0.0
    for b, v in rows:
        cum += v
        log("  %-22s %14s  %6s   (cộng dồn %s)"
            % (R.BLOC_NAME_VI[b], R.fmt_usd(v), R.fmt_pct(v / vn_out * 100),
               R.fmt_pct(cum / vn_out * 100)))
    if len(rows) >= 2:
        two = rows[0][1] + rows[1][1]
        log("")
        log("  -> %s + %s = %s tổng xuất khẩu của Việt Nam."
            % (R.BLOC_NAME_VI[rows[0][0]], R.BLOC_NAME_VI[rows[1][0]],
               R.fmt_pct(two / vn_out * 100)))
    log("")
    log("  Việt Nam: xuất %s = %s tổng xuất khẩu thế giới (%s)."
        % (R.fmt_usd(vn_out), R.fmt_pct(vn_out / total * 100),
           R.fmt_usd(total)))
    log("  Thương mại hai chiều của Việt Nam (xuất + nhập): %s."
        % R.fmt_usd(vn_total))


if __name__ == "__main__":
    main()

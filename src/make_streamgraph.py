"""Streamgraph cơ cấu xuất khẩu Việt Nam theo 10 ngành, 1995–2023 (T21).

Streamgraph là biểu đồ vùng chồng có đường nền ĐỐI XỨNG quanh trục giữa thay vì
nằm trên trục 0. Đổi lấy gì và được gì:

    mất   — không đọc được giá trị tuyệt đối của một ngành ở một năm, vì không
            có trục gốc chung để đo lên.
    được  — thấy rõ HÌNH DẠNG của từng dải qua thời gian, và thấy được tổng
            thể phình ra, vì không ngành nào bị ép nằm sát trục đáy và chịu
            méo hơn các ngành khác.

Nên hình này để trả lời "ngành nào lớn lên, ngành nào teo đi", KHÔNG để tra
"năm 2010 điện tử bao nhiêu tỷ". Ai cần con số đó thì tra treemap ở T12 hoặc
bảng in ra cuối script này.

Hai bản được xuất ra, và nên dùng cả hai
-----------------------------------------
    streamgraph_vnm_tuyet_doi.*  — bề dày = tỷ USD. Thấy quy mô phình lên.
    streamgraph_vnm_ty_trong.*   — chuẩn hóa về 100% mỗi năm. Thấy cơ cấu
                                    chuyển dịch, không bị quy mô át đi.

Bản tỷ trọng mới là bản trả lời đúng câu hỏi của đồ án. Ở bản tuyệt đối, mọi
ngành đều phình to nên mắt đọc ra "cái gì cũng tăng" — đúng nhưng vô nghĩa, vì
tổng tăng 75 lần. Chuyển dịch cơ cấu chỉ hiện ra khi bỏ quy mô đi.

Chạy
----
    python src/make_streamgraph.py
    python src/make_streamgraph.py --country THA
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import graph_common as GC  # noqa: E402
import reference_data as R  # noqa: E402
from make_hierarchy_charts import load_tree, sector_index  # noqa: E402

try:
    import plotly.graph_objects as go
except ImportError:
    sys.exit("Thiếu plotly. Chạy: python -m pip install plotly kaleido")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, "data", "atlas")

FIRST_YEAR, LAST_YEAR = 1995, R.LAST_COMPLETE_YEAR


def log(msg):
    print(msg)
    sys.stdout.flush()


def load_series(country, tree):
    """{năm: {số ngành: giá trị}} cho một nước, đọc thẳng từ cp_year_hs2.csv."""
    index = sector_index(tree)
    path = os.path.join(ATLAS, "cp_year_hs2.csv")
    if not os.path.exists(path):
        sys.exit("Thiếu %s. Chạy: python src/download_atlas.py" % path)
    acc = {}
    with open(path, encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            if r["country_iso3_code"] != country:
                continue
            y = int(r["year"])
            if not (FIRST_YEAR <= y <= LAST_YEAR):
                continue
            try:
                v = float(r["export_value"] or 0)
            except ValueError:
                continue
            if v <= 0:
                continue
            hit = index.get(int(r["product_id"]))
            if hit is None:
                continue
            acc.setdefault(y, {})[hit[1]] = acc.setdefault(y, {}).get(hit[1], 0.0) + v
    return acc


def stream_bands(years, series, order, normalise):
    """Tính mép dưới và mép trên của từng dải, nền đối xứng quanh trục giữa.

    Đường nền "wiggle" của Byron & Wattenberg tối ưu cho độ gập ghềnh, nhưng ở
    đây chỉ có 10 dải và 29 năm nên nền đối xứng đơn giản cho hình sạch hơn mà
    không phải giải thích thêm một thuật toán nữa trong báo cáo.
    """
    lower, upper = {}, {}
    for y in years:
        vals = series.get(y, {})
        total = sum(vals.values()) or 1.0
        scale = 100.0 / total if normalise else 1.0
        stacked = sum(vals.get(s, 0.0) for s in order) * scale
        base = -stacked / 2.0
        for s in order:
            v = vals.get(s, 0.0) * scale
            lower.setdefault(s, []).append(base)
            base += v
            upper.setdefault(s, []).append(base)
    return lower, upper


def build(years, series, normalise, country_vi):
    # Ngành vẽ theo thứ tự ID, KHÔNG theo độ lớn: thứ tự phải giống nhau giữa
    # hai bản và giống mọi hình khác của đồ án, nếu không người xem phải học
    # lại vị trí dải ở mỗi hình.
    order = sorted(R.SECTOR_PALETTE)
    lower, upper = stream_bands(years, series, order, normalise)

    fig = go.Figure()
    for s in order:
        name = R.SECTOR_NAME_VI[s]
        color = R.SECTOR_PALETTE[s]
        # Vẽ mỗi dải bằng một đa giác khép kín: đi hết mép trên rồi quay ngược
        # theo mép dưới. Không dùng stackgroup của plotly vì nó chỉ chồng từ
        # trục 0 lên, không làm được nền đối xứng.
        xs = list(years) + list(reversed(years))
        ys = upper[s] + list(reversed(lower[s]))
        if normalise:
            hov = ["<b>%s</b><br>%d: %s tổng xuất khẩu<extra></extra>"
                   % (name, y, R.fmt_pct(upper[s][i] - lower[s][i]))
                   for i, y in enumerate(years)]
        else:
            hov = ["<b>%s</b><br>%d: %s<extra></extra>"
                   % (name, y, R.fmt_usd(upper[s][i] - lower[s][i]))
                   for i, y in enumerate(years)]
        fig.add_trace(go.Scatter(
            x=xs, y=ys, fill="toself", mode="lines", name=name,
            fillcolor=color, line=dict(color="#FFFFFF", width=0.7),
            hoveron="fills", hoverinfo="text",
            text=name, legendgroup=name,
        ))
        # Trace mỏng chạy giữa dải, chỉ để hover ra số theo từng năm — hoveron
        # fills của plotly chỉ trả về MỘT nhãn cho cả vùng, không theo điểm.
        mid = [(upper[s][i] + lower[s][i]) / 2 for i in range(len(years))]
        fig.add_trace(go.Scatter(
            x=list(years), y=mid, mode="lines", showlegend=False,
            line=dict(color="rgba(0,0,0,0)", width=14),
            hovertemplate=hov, legendgroup=name,
        ))
    return fig


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--country", default="VNM")
    args = ap.parse_args()
    iso = args.country.upper()
    country_vi = R.COUNTRY_VI.get(iso, (iso,))[0]

    log("Đọc cây HS92...")
    tree = load_tree()
    log("Đọc xuất khẩu %s %d–%d..." % (iso, FIRST_YEAR, LAST_YEAR))
    series = load_series(iso, tree)
    years = sorted(series)
    if not years:
        sys.exit("Không có dữ liệu cho %s" % iso)
    # Ghi rõ "mốc năm" chứ không ghi "năm": 1995–2023 có 29 MỐC dữ liệu nhưng
    # chỉ 28 NĂM trôi qua. Tiêu đề biểu đồ nói về mức tăng giữa hai đầu nên
    # dùng 28; dòng log này đếm số điểm dữ liệu nên là 29. Không ghi rõ thì
    # hai con số trông như mâu thuẫn.
    log("  %d mốc năm, %d–%d (tức %d năm trôi qua)"
        % (len(years), years[0], years[-1], years[-1] - years[0]))

    first, last = years[0], years[-1]
    tot_first = sum(series[first].values())
    tot_last = sum(series[last].values())

    def share(y, s):
        t = sum(series[y].values()) or 1.0
        return series[y].get(s, 0.0) / t * 100

    # Ngành chuyển dịch mạnh nhất — dùng cho tiêu đề, tính từ dữ liệu.
    moves = sorted(R.SECTOR_PALETTE,
                   key=lambda s: -(share(last, s) - share(first, s)))
    up, down = moves[0], moves[-1]

    for normalise, stem, tt, sub in [
        (True, "streamgraph_%s_ty_trong" % iso.lower(),
         "%s: %s thay %s làm ngành xuất khẩu chính"
         % (country_vi, R.SECTOR_NAME_VI[up], R.SECTOR_NAME_VI[down].lower()),
         "Tỷ trọng 10 ngành cấp 1 của hệ HS92 trong tổng xuất khẩu, mỗi năm "
         "chuẩn hóa về 100%%. %s đi từ %s lên %s; %s đi từ %s xuống %s."
         % (R.SECTOR_NAME_VI[up], R.fmt_pct(share(first, up)),
            R.fmt_pct(share(last, up)), R.SECTOR_NAME_VI[down],
            R.fmt_pct(share(first, down)), R.fmt_pct(share(last, down)))),
        (False, "streamgraph_%s_tuyet_doi" % iso.lower(),
         "%s: quy mô xuất khẩu tăng %s lần trong %d năm"
         % (country_vi, R.fmt_vn(tot_last / tot_first if tot_first else 0),
            last - first),
         "Giá trị tuyệt đối, USD hiện hành. Bề dày tổng = tổng kim ngạch: %s "
         "năm %d lên %s năm %d. Bản này cho thấy QUY MÔ; muốn thấy chuyển dịch "
         "CƠ CẤU thì xem bản tỷ trọng."
         % (R.fmt_usd(tot_first), first, R.fmt_usd(tot_last), last)),
    ]:
        fig = build(years, series, normalise, country_vi)
        fig.update_layout(**GC.base_layout(
            title=tt, subtitle=sub,
            note="Nguồn: Atlas of Economic Complexity (Harvard Growth Lab), "
                 "phân loại HS92 cấp 1. Nền ĐỐI XỨNG quanh trục giữa: trục dọc "
                 "KHÔNG có gốc 0 nên chỉ đọc được bề dày của dải, không đọc "
                 "được độ cao. Màu 10 ngành dùng chung với mọi hình khác của "
                 "đồ án.",
            xaxis=dict(title="", gridcolor="#EEEEEE", zeroline=False,
                       dtick=5, range=[first, last]),
            yaxis=dict(visible=False, zeroline=False, showgrid=False),
            legend=dict(orientation="h", yanchor="top", y=-0.08,
                        xanchor="left", x=0, font=dict(size=R.FONT_SIZES["footnote"]),
                        traceorder="normal"),
            margin=dict(t=108, l=16, r=16, b=116),
            hovermode="closest",
        ))
        GC.save(fig, stem, width=1500, height=900, log=log)

    # --- Bảng số, vì streamgraph cố ý không cho tra số --------------------
    log("")
    log("Tỷ trọng 10 ngành — tra số ở đây, vì streamgraph không tra được:")
    log("  %-30s %8s %8s %9s" % ("ngành", str(first), str(last), "đổi"))
    log("  " + "-" * 60)
    for s in sorted(R.SECTOR_PALETTE):
        a, b = share(first, s), share(last, s)
        # Dau "+" phai ghep tay: fmt_vn khong co tuy chon hien dau duong, ma
        # cot nay can dau de phan biet nganh len voi nganh xuong.
        d = b - a
        log("  %-30s %8s %8s %9s" % (R.SECTOR_NAME_VI[s], R.fmt_pct(a),
                                     R.fmt_pct(b),
                                     ("+" if d >= 0 else "") + R.fmt_vn(d)))
    log("")
    log("  Lên mạnh nhất  : %-28s +%s điểm %%"
        % (R.SECTOR_NAME_VI[up], R.fmt_vn(share(last, up) - share(first, up))))
    log("  Xuống mạnh nhất: %-28s %s điểm %%"
        % (R.SECTOR_NAME_VI[down], R.fmt_vn(share(last, down) - share(first, down))))
    log("")
    log("  Tổng: %s (%d) -> %s (%d), tăng %s lần."
        % (R.fmt_usd(tot_first), first, R.fmt_usd(tot_last), last,
           R.fmt_vn(tot_last / tot_first if tot_first else 0)))


if __name__ == "__main__":
    main()

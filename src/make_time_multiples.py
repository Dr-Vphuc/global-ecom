"""Vị trí của Việt Nam trong mạng lưới qua bốn mốc thời gian (T20).

"Vị trí trong mạng lưới" ở đây được định nghĩa bằng hai trục đo được, thay vì
bằng chỗ ngồi trên một hình node-link:

    trục ngang  — SỐ bạn hàng (có bao nhiêu kênh bán)
    trục dọc    — TIỀN bán được (các kênh đó mang về bao nhiêu)

Vẽ bốn năm mốc trên bốn khung CÙNG THANG ĐO, nên vị trí của một nước ở khung
này so được trực tiếp với khung kia. Đó là toàn bộ ý nghĩa của small multiples:
giữ nguyên mọi thứ trừ một biến, ở đây biến đó là thời gian.

Vì sao hai trục này, không phải node-link bốn lần
--------------------------------------------------
Bốn hình node-link cạnh nhau KHÔNG so sánh được, vì bố cục force-directed cho
mỗi năm một hình dạng khác nhau — nút nhảy chỗ giữa các khung dù cấu trúc không
đổi, và mắt sẽ đọc cái nhảy chỗ đó thành "có thay đổi". Hai trục số thì cố
định: cùng một tọa độ ở cả bốn khung luôn có cùng nghĩa.

Điều hình này cho thấy
----------------------
Việt Nam đi LÊN (tiền tăng gấp nhiều lần) nhưng đi SANG TRÁI trong giai đoạn
gần đây (số bạn hàng giảm). Tiền vào nhiều hơn qua ít kênh hơn — phát hiện A9.
Một nước bán được nhiều hơn mà qua ít cửa hơn thì dễ tổn thương hơn khi một
cửa đóng lại, chứ không phải mạnh lên đơn thuần.

Chạy
----
    python src/make_time_multiples.py
    python src/make_time_multiples.py --years 1995,2005,2015,2023
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
    from plotly.subplots import make_subplots
except ImportError:
    sys.exit("Thiếu plotly. Chạy: python -m pip install plotly kaleido")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(ROOT, "data", "processed")

# Nước nào được ghi nhãn. Giữ ít, vì 231 nhãn thì không khung nào đọc được.
LABELLED = ["VNM", "THA", "MYS", "IDN", "SGP", "PHL", "CHN", "KOR"]


def log(msg):
    print(msg)
    sys.stdout.flush()


def load_by_year(years):
    """{năm: {iso3: (số thị trường xuất, tổng xuất khẩu)}} từ đồ thị ĐẦY ĐỦ.

    Dùng đồ thị đầy đủ chứ không dùng bản đã lọc: câu hỏi ở đây là "Việt Nam
    bán cho bao nhiêu nước", và ngưỡng lọc của T10 sinh ra cho mục đích khác
    hẳn (làm hình node-link đọc được). Lọc ở đây sẽ cắt mất đúng cái đuôi bạn
    hàng nhỏ mà ta đang muốn đếm.
    """
    want = set(years)
    acc = {y: {} for y in years}
    path = os.path.join(PROC, "edges.csv")
    if not os.path.exists(path):
        sys.exit("Thiếu %s. Chạy: python src/build_intermediate.py" % path)
    with open(path, encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            y = int(r["year"])
            if y not in want:
                continue
            s = r["source_iso3"]
            d, v = acc[y].get(s, (0, 0.0))
            acc[y][s] = (d + 1, v + float(r["export_value"]))
    return acc


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--years", default=",".join(str(y) for y in R.MILESTONE_YEARS))
    args = ap.parse_args()

    years = [int(y) for y in args.years.split(",") if y.strip()]
    if len(years) != 4:
        sys.exit("Cần đúng 4 năm để lưới 2×2 cân đối, đang có %d" % len(years))

    meta = {}
    with open(os.path.join(PROC, "nodes.csv"), encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            meta[r["country_iso3"]] = r

    log("Đọc cạnh cho %s..." % ", ".join(str(y) for y in years))
    data = load_by_year(years)
    for y in years:
        log("  %d: %d nước có xuất khẩu" % (y, len(data[y])))

    # Thang đo chung cho cả bốn khung — điều kiện bắt buộc của small multiples.
    all_deg = [d for y in years for d, _ in data[y].values()]
    all_val = [v for y in years for _, v in data[y].values() if v > 0]
    xmax = max(all_deg) * 1.06
    ymin, ymax = min(all_val), max(all_val)

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=["<b>%d</b>" % y for y in years],
        horizontal_spacing=0.08, vertical_spacing=0.11,
        shared_xaxes=True, shared_yaxes=True,
    )

    for k, y in enumerate(years):
        row, col = k // 2 + 1, k % 2 + 1
        rows_y = data[y]
        others = [(i, d, v) for i, (d, v) in rows_y.items()
                  if v > 0 and i != "VNM" and i not in R.FOCUS_ISO3]
        asean = [(i, d, v) for i, (d, v) in rows_y.items()
                 if v > 0 and i in R.FOCUS_ISO3 and i != "VNM"]

        fig.add_trace(go.Scatter(
            x=[d for _, d, _ in others], y=[v for _, _, v in others],
            mode="markers", showlegend=False,
            marker=dict(size=4.5, color="rgba(170,170,170,0.5)",
                        line=dict(width=0)),
            hovertemplate=["<b>%s</b><br>%d thị trường · %s<extra></extra>"
                           % (GC.name_vi(i, meta), d, R.fmt_usd(v))
                           for i, d, v in others],
        ), row=row, col=col)

        fig.add_trace(go.Scatter(
            x=[d for _, d, _ in asean], y=[v for _, _, v in asean],
            mode="markers+text", showlegend=False,
            marker=dict(size=8, color="#9A9A9A",
                        line=dict(color="#FFFFFF", width=1)),
            text=[GC.name_vi(i, meta) if i in LABELLED else "" for i, _, _ in asean],
            textposition="middle right",
            textfont=dict(size=R.FONT_SIZES["footnote"], color="#555555"),
            hovertemplate=["<b>%s</b><br>%d thị trường · %s<extra></extra>"
                           % (GC.name_vi(i, meta), d, R.fmt_usd(v))
                           for i, d, v in asean],
        ), row=row, col=col)

        if "VNM" in rows_y:
            d, v = rows_y["VNM"]
            fig.add_trace(go.Scatter(
                x=[d], y=[v], mode="markers+text", showlegend=False,
                marker=dict(size=15, color="#E8E8E8", symbol="circle",
                            line=dict(color=R.HIGHLIGHT_STROKE,
                                      width=R.HIGHLIGHT_STROKE_WIDTH + 0.8)),
                text=["<b>Việt Nam</b>"], textposition="middle right",
                textfont=dict(size=R.FONT_SIZES["legend"], color="#000000"),
                hovertemplate="<b>Việt Nam %d</b><br>%d thị trường · %s"
                              "<extra></extra>" % (y, d, R.fmt_usd(v)),
            ), row=row, col=col)

    fig.update_xaxes(range=[0, xmax], gridcolor="#EEEEEE", zeroline=False,
                     title_text="")
    fig.update_yaxes(type="log", range=[__import__("math").log10(ymin * 0.7),
                                        __import__("math").log10(ymax * 1.5)],
                     gridcolor="#EEEEEE", zeroline=False)
    fig.update_xaxes(title_text="Số thị trường xuất khẩu", row=2, col=1)
    fig.update_xaxes(title_text="Số thị trường xuất khẩu", row=2, col=2)
    fig.update_yaxes(title_text="Tổng xuất khẩu, USD (thang log)", row=1, col=1)
    fig.update_yaxes(title_text="Tổng xuất khẩu, USD (thang log)", row=2, col=1)

    vn = {y: data[y].get("VNM", (0, 0.0)) for y in years}
    d0, v0 = vn[years[0]]
    d1, v1 = vn[years[-1]]
    # Phu de phai noi DUNG hinh dang cua chuoi. Ban dau ghi "tu 98 len 166",
    # ky thuat thi dung nhung doc ra thanh "tang deu" — trong khi chuoi that
    # la tang roi GIAM, va chinh cho giam moi la phat hien. Lay nam dinh tu du
    # lieu thay vi viet tay, de doi nam moc thi phu de tu dung theo.
    peak_y = max(years, key=lambda y: vn[y][0])
    if vn[peak_y][0] > d1:
        traj = ("số thị trường lên đỉnh %d nước năm %d rồi lùi về %d"
                % (vn[peak_y][0], peak_y, d1))
    else:
        traj = "số thị trường đi từ %d lên %d" % (d0, d1)

    fig.update_layout(**GC.base_layout(
        title="Việt Nam đi lên nhưng không đi rộng ra",
        subtitle="Vị trí của mọi nước trên hai trục: số thị trường xuất khẩu "
                 "(ngang) và tổng kim ngạch (dọc, thang log). Bốn khung dùng "
                 "CHUNG một thang đo. Việt Nam viền đen, các nước ASEAN khác "
                 "tô xám đậm. Từ %d đến %d: tiền tăng %s lần, còn %s."
                 % (years[0], years[-1], R.fmt_vn(v1 / v0 if v0 else 0), traj),
        note="Nguồn: Atlas of Economic Complexity (Harvard Growth Lab). "
             "Dùng đồ thị ĐẦY ĐỦ, không lọc ngưỡng — câu hỏi ở đây là đếm bạn "
             "hàng, mà ngưỡng T10 lại cắt đúng cái đuôi bạn hàng nhỏ cần đếm. "
             "Trục dọc là log vì kim ngạch lệch 6 bậc độ lớn.",
        margin=dict(t=118, l=72, r=24, b=72),
        showlegend=False,
    ))
    fig.update_annotations(font_size=R.FONT_SIZES["legend"] + 3)

    GC.save(fig, "time_multiples", width=1500, height=1050, log=log)

    # --- Bằng chứng cho tiêu đề -------------------------------------------
    log("")
    log("Việt Nam qua bốn mốc (cơ sở của tiêu đề):")
    log("  %-6s %14s %16s" % ("năm", "số thị trường", "tổng xuất khẩu"))
    prev = None
    for y in years:
        d, v = vn[y]
        delta = ""
        if prev is not None:
            dd = d - prev[0]
            delta = "  (%+d thị trường, tiền ×%s)" % (dd, R.fmt_vn(v / prev[1]))
        log("  %-6d %14d %16s%s" % (y, d, R.fmt_usd(v), delta))
        prev = (d, v)

    log("")
    peak = max(years, key=lambda y: vn[y][0])
    if vn[years[-1]][0] < vn[peak][0]:
        log("  -> Số thị trường ĐẠT ĐỈNH năm %d (%d nước) rồi GIẢM còn %d."
            % (peak, vn[peak][0], vn[years[-1]][0]))
        log("     Trong khi đó tiền vẫn tăng ×%s so với %d."
            % (R.fmt_vn(vn[years[-1]][1] / vn[peak][1]), peak))
        log("     Tiền vào nhiều hơn qua ÍT cửa hơn — đây là phát hiện A9,")
        log("     và nó là một rủi ro, không phải một thành tích.")
    else:
        log("  -> Số thị trường tăng đều, không có đỉnh giữa chừng.")


if __name__ == "__main__":
    main()

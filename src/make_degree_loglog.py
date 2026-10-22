"""Phân bố bậc trên thang log-log — T09, phần biểu đồ.

`src/analyze_network.py` đã đo và ghi `data/processed/degree_distribution.csv`.
Script này chỉ vẽ. Nó vẽ **hai bảng cạnh nhau** vì một bảng không đủ để nói hết:

1. **Trái — thang log-log.** Đây là bài kiểm tra chuẩn cho giả thuyết scale-free:
   nếu phân bố bậc theo luật lũy thừa P(K ≥ k) ~ k^(-α) thì trên thang log-log
   nó phải là **đường thẳng**. Đường thật của thương mại đi ngang rồi rơi dốc
   đứng ở mép phải. Để không ai phải tin vào mắt mình, bảng này còn vẽ **đường
   thẳng khớp nhất** (bình phương tối thiểu trên log-log) kèm R² — con số nói
   đường thẳng giải thích được bao nhiêu phần biến thiên.

2. **Phải — thang thường, so với phân bố đều.** Log-log trả lời "có phải lũy
   thừa không" nhưng không trả lời "thế thì là gì". Trên thang thường, CCDF của
   thương mại gần như trùng một đường chéo — tức các nước trải **gần như đều**
   trên toàn dải bậc. Khoảng lệch lớn nhất được đánh dấu ngay trên hình.

Vì sao dùng CCDF chứ không dùng tần suất thô: xem ghi chú trong
``src/analyze_network.py``. Tóm lại, tần suất thô ở phần bậc thấp chỉ có vài
nước mỗi bậc, vẽ log-log ra một đám chấm loãng; CCDF làm mượt mà không phải
chọn độ rộng ô theo cảm tính.

**Kết quả này là kết quả, không phải lỗi.** Phát hiện A3 trong
``docs/phat-hien-va-quyet-dinh.md`` ghi rõ: mạng thương mại KHÔNG scale-free,
không có hub theo nghĩa tô-pô. Câu đó phải nằm ngay trên hình, nếu không người
đọc quen nhìn hình log-log thẳng sẽ tưởng vẽ sai.

Màu: lấy hai màu ĐẬM trong bảng 10 ngành (kim loại, dệt may). Hình này không có
chú giải ngành nào nên không sợ đọc lẫn, và style guide cấm vẽ đường mảnh bằng
bốn màu nhạt còn lại.

Chạy
----
    python src/make_degree_loglog.py
    python src/make_degree_loglog.py --year 1995
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reference_data as R  # noqa: E402

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    sys.exit("Thiếu plotly. Chạy: python -m pip install plotly kaleido")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "output")

# Khung tính bằng POINT theo B16: cỡ chữ khai báo bao nhiêu point thì in ra
# bấy nhiêu. Phải cao hơn FIG_HEIGHT_DEFAULT vì khối tiêu đề ở cỡ chữ ĐÚNG
# chiếm gần 80 pt — để nguyên 3,90 inch thì phần vẽ chỉ còn hơn 70 pt.
FIG_H_INCH = 4.40
MARGIN_X = 8.0
MARGIN_L = 34.0       # chỗ cho nhãn trục dọc
TEXT_PAD = 6.0
LINE_H = 1.33
AXIS_BAND = 34.0      # nhãn tick + tên trục ngang
LEG_BAND = 50.0       # chú giải xếp ngang, cuộn thành hai hàng
SUBTITLE_BAND = 18.0  # tiêu đề hai bảng con, plotly đặt trong lề trên
DIST_CSV = os.path.join(ROOT, "data", "processed", "degree_distribution.csv")

COLOR_OUT = R.SECTOR_PALETTE[5]   # #332288 — xanh đậm
COLOR_IN = R.SECTOR_PALETTE[1]    # #CC6677 — đỏ hồng
COLOR_REF = "#777777"             # đường tham chiếu: xám, luôn nét gãy
COLOR_GRID = "#E5E5E5"

KIND_VI = {"out": "Bậc xuất khẩu (số nước mua)", "in": "Bậc nhập khẩu (số nước bán)"}


# ---------------------------------------------------------------------------
# Đọc dữ liệu
# ---------------------------------------------------------------------------
def load_ccdf(year):
    """Trả về {kind: [(bậc, ccdf, số_nước), ...]} của một năm, bậc tăng dần."""
    if not os.path.exists(DIST_CSV):
        sys.exit("Chưa có %s.\nChạy trước: python src/analyze_network.py" % DIST_CSV)
    out = {"out": [], "in": []}
    with open(DIST_CSV, "r", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if int(row["year"]) != year:
                continue
            out[row["kind"]].append(
                (int(row["degree"]), float(row["ccdf"]), int(row["n_countries"])))
    if not out["out"]:
        years = sorted({int(r["year"]) for r in
                        csv.DictReader(open(DIST_CSV, "r", encoding="utf-8"))})
        sys.exit("Năm %d không có trong %s.\nCác năm đã đo: %s"
                 % (year, DIST_CSV, ", ".join(str(y) for y in years)))
    for k in out:
        out[k].sort()
    return out


def degrees_of(points):
    """Bung CCDF về danh sách bậc của từng nước, để tính phân vị."""
    degs = []
    for d, _, n in points:
        degs += [d] * n
    degs.sort()
    return degs


# ---------------------------------------------------------------------------
# Hai phép đo đỡ cho hai bảng
# ---------------------------------------------------------------------------
def fit_powerlaw(points):
    """Bình phương tối thiểu log10(CCDF) theo log10(bậc).

    Trả về dict: hệ số a, b (log10 y = a + b·log10 x), R², sai số lớn nhất tính
    theo số LẦN (vì sai số 1 trên thang log10 nghĩa là lệch 10 lần), và bậc mà
    tại đó đường khớp còn đòi CCDF > 1 — một đòi hỏi vô nghĩa, vì CCDF là tỉ lệ.

    Bỏ bậc 0 ra khỏi phép khớp: log10(0) không tồn tại. Đó là một nước duy nhất
    (không xuất khẩu đi đâu) và nó vẫn nằm trong bảng bên phải.
    """
    pts = [(d, c) for d, c, _ in points if d > 0 and c > 0]
    xs = [math.log10(d) for d, _ in pts]
    ys = [math.log10(c) for _, c in pts]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    b = sxy / sxx
    a = my - b * mx
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    worst = max(abs(y - (a + b * x)) for x, y in zip(xs, ys))
    return {
        "a": a, "b": b,
        "r2": 1 - ss_res / ss_tot,
        "worst_ratio": 10 ** worst,
        "n_points": n,
        # 10^((0 - a) / b): bậc mà đường khớp cắt mốc CCDF = 1 = 100%.
        "crosses_one_at": 10 ** (-a / b) if b else float("nan"),
    }


def uniform_gap(points):
    """Khoảng lệch lớn nhất giữa CCDF thật và CCDF của phân bố ĐỀU hoàn toàn.

    Phân bố đều trên dải [bậc nhỏ nhất, bậc lớn nhất] có CCDF là đường chéo
    (max - d) / (max - min). Lấy khoảng lệch tuyệt đối lớn nhất — cùng một đại
    lượng với thống kê Kolmogorov–Smirnov, nhưng ở đây chỉ dùng để mô tả.
    """
    degs = degrees_of(points)
    lo, hi = degs[0], degs[-1]
    best = {"gap": -1.0}
    for d, c, _ in points:
        uni = (hi - d) / float(hi - lo)
        gap = abs(c - uni)
        if gap > best["gap"]:
            best = {"gap": gap, "degree": d, "obs": c, "uni": uni}
    best["lo"], best["hi"] = lo, hi
    # Năm 2023 lệch 0,056 — gọi là "gần như đều" thì đúng. Nhưng năm 1995 lệch
    # tới 0,180, gọi như thế là sai. Nên câu chữ trên hình phải đi theo số đo
    # chứ không được đóng cứng theo năm mốc.
    best["near_uniform"] = best["gap"] < 0.10
    return best


def uniform_phrase(gap):
    """Câu mô tả mức lệch, chọn theo số đo chứ không theo năm."""
    if gap["near_uniform"]:
        return ("Các nước trải gần như ĐỀU trên dải bậc (lệch tối đa %s)"
                % R.fmt_vn(gap["gap"], 3))
    return ("Phân bố còn lệch rõ khỏi mức đều — tối đa %s tại bậc %s, tức vẫn "
            "còn một lớp nước ít bạn hàng"
            % (R.fmt_vn(gap["gap"], 3), R.fmt_vn(gap["degree"], 0)))


# ---------------------------------------------------------------------------
# Hình
# ---------------------------------------------------------------------------
def _hover(kind_vi, points):
    return ["<b>Bậc %s</b><br>%s nước có bậc đúng bằng %s"
            "<br>CCDF: %s số nước có bậc ≥ %s<br><i>%s</i><extra></extra>"
            % (R.fmt_vn(d, 0), R.fmt_vn(n, 0), R.fmt_vn(d, 0),
               R.fmt_pct(c * 100), R.fmt_vn(d, 0), kind_vi)
            for d, c, n in points]


def make_figure(data, year, fit, gap):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            "<b>Thang log-log</b> — phải thẳng nếu scale-free",
            "<b>Thang thường</b> — so với phân bố đều",
        ),
        horizontal_spacing=0.09,
    )

    # --- bảng trái: log-log, cả hai chiều bậc ------------------------------
    for kind, color, width in (("out", COLOR_OUT, R.HIGHLIGHT_LINE_WIDTH),
                               ("in", COLOR_IN, R.DEFAULT_LINE_WIDTH + 0.4)):
        pts = [(d, c, n) for d, c, n in data[kind] if d > 0]
        fig.add_trace(go.Scatter(
            x=[d for d, _, _ in pts], y=[c for _, c, _ in pts],
            mode="lines", name=KIND_VI[kind],
            line=dict(color=color, width=width),
            hovertemplate=_hover(KIND_VI[kind], pts),
            legendgroup=kind,
        ), row=1, col=1)

    # Đường thẳng khớp nhất. Vẽ hết dải để thấy nó chạy vượt mốc 100% ở phần
    # bậc thấp — tức đường thẳng không chỉ khớp kém, nó còn đòi điều bất khả.
    xs_fit = [1.0]
    while xs_fit[-1] < gap["hi"]:
        xs_fit.append(xs_fit[-1] * 1.12)
    fig.add_trace(go.Scatter(
        x=xs_fit, y=[10 ** (fit["a"] + fit["b"] * math.log10(x)) for x in xs_fit],
        mode="lines", name="Đường thẳng khớp nhất (R² = %s)" % R.fmt_vn(fit["r2"], 2),
        line=dict(color=COLOR_REF, width=1.4, dash="dash"),
        hovertemplate="Đường thẳng khớp nhất<br>bậc %{x:.0f} → CCDF %{y:.3f}<extra></extra>",
    ), row=1, col=1)

    # Mốc 100%: CCDF là tỉ lệ, không thể vượt. Đường mảnh, chấm, màu nhạt.
    fig.add_hline(y=1.0, line=dict(color="#BBBBBB", width=1, dash="dot"), row=1, col=1)

    # Hai câu đọc hộ bảng trái. Đặt vào hai khoảng trống sẵn có nên không che
    # dữ liệu: góc trên (phần đường khớp chạy vượt 100%) và góc dưới trái.
    fig.add_annotation(
        x=math.log10(1.15), y=math.log10(4.0), row=1, col=1,
        text="Trên mốc 100%%: đường khớp đòi hơn<br>toàn bộ số nước — bất khả. "
             "Mọi bậc<br>dưới %s đều rơi vào vùng này."
             % R.fmt_vn(fit["crosses_one_at"], 0),
        showarrow=False, xanchor="left", yanchor="top", align="left",
        font=dict(size=R.FONT_SIZES["annotation"], color="#555"),
    )
    fig.add_annotation(
        x=math.log10(1.15), y=math.log10(0.02), row=1, col=1,
        text="Đường thật đi ngang rồi rơi dốc đứng:<br>"
             "gần như nước nào cũng có nhiều bạn hàng,<br>"
             "nên không có nhóm hub tách khỏi phần còn lại.",
        showarrow=False, xanchor="left", yanchor="top", align="left",
        font=dict(size=R.FONT_SIZES["annotation"], color="#333"),
    )

    # --- bảng phải: thang thường, so với đường chéo ------------------------
    pts = data["out"]
    fig.add_trace(go.Scatter(
        x=[d for d, _, _ in pts], y=[c for _, c, _ in pts],
        mode="lines", line=dict(color=COLOR_OUT, width=R.HIGHLIGHT_LINE_WIDTH),
        name=KIND_VI["out"], legendgroup="out", showlegend=False,
        hovertemplate=_hover(KIND_VI["out"], pts),
    ), row=1, col=2)
    fig.add_trace(go.Scatter(
        x=[gap["lo"], gap["hi"]], y=[1.0, 0.0],
        mode="lines", name="Phân bố đều hoàn toàn",
        line=dict(color=COLOR_REF, width=1.4, dash="dash"),
        hovertemplate="Phân bố đều<br>bậc %{x:.0f} → CCDF %{y:.3f}<extra></extra>",
    ), row=1, col=2)

    # Khoảng lệch lớn nhất: một đoạn thẳng đứng nối hai đường, màu đen theo quy
    # ước "nhấn bằng hình dạng, không bằng màu". Không mũi tên.
    fig.add_trace(go.Scatter(
        x=[gap["degree"], gap["degree"]], y=[gap["uni"], gap["obs"]],
        mode="lines", line=dict(color=R.HIGHLIGHT_STROKE, width=R.HIGHLIGHT_STROKE_WIDTH),
        showlegend=False, hoverinfo="skip",
    ), row=1, col=2)
    fig.add_annotation(
        x=gap["degree"], y=gap["obs"], row=1, col=2,
        text="lệch nhiều nhất: %s" % R.fmt_vn(gap["gap"], 3),
        showarrow=False, xanchor="left", yanchor="bottom", xshift=6,
        font=dict(size=R.FONT_SIZES["annotation"], color="#333"),
    )

    # --- trục ---------------------------------------------------------------
    axis_common = dict(showline=True, linecolor="#999999", ticks="outside",
                       gridcolor=COLOR_GRID, tickfont=dict(size=R.FONT_SIZES["tick"]),
                       title_font=dict(size=R.FONT_SIZES["axis"]))
    # Trên trục log, plotly tự rải nhãn ở cả vạch phụ và in ra "1 2 5 10 2 5
    # 100 2" — đọc như số rác. Nên chỉ định thẳng vạch nào có nhãn, và viết
    # nhãn theo kiểu Việt Nam (dấu phẩy thập phân, phần trăm cho CCDF).
    x_ticks = [1, 2, 5, 10, 20, 50, 100, 200]
    y_ticks = [1, .5, .2, .1, .05, .02, .01, .005]
    fig.update_xaxes(type="log", title_text="Bậc (số bạn hàng) — thang log",
                     range=[-0.02, 2.42],
                     tickmode="array", tickvals=x_ticks,
                     ticktext=[R.fmt_vn(v, 0) for v in x_ticks],
                     row=1, col=1, **axis_common)
    fig.update_yaxes(type="log", title_text="CCDF: tỉ lệ nước có bậc ≥ k",
                     range=[-2.6, 0.62],
                     tickmode="array", tickvals=y_ticks,
                     ticktext=[R.fmt_pct(v * 100, 0 if v >= .01 else 1) for v in y_ticks],
                     row=1, col=1, **axis_common)
    fig.update_xaxes(title_text="Bậc (số bạn hàng)", row=1, col=2, **axis_common)
    fig.update_yaxes(title_text="", range=[0, 1.04], tickformat=".0%",
                     row=1, col=2, **axis_common)

    # --- khối chữ đặt tay theo B16 -----------------------------------------
    # layout.title tự đo chỗ và KHÔNG tự ngắt dòng: ở khung point, câu tiêu đề
    # dài hơn bề ngang khung nên nó chạy thẳng ra ngoài mép. Ngắt dòng bằng
    # wrap_pt rồi tự đặt, giống T16/T17/T19.
    title = ("Phân bố bậc không theo luật lũy thừa: thương mại thế giới không "
             "có hub theo nghĩa tô-pô")
    sub = ("Năm %d, %s nước. Đường thẳng khớp nhất trên thang log-log chỉ giải "
           "thích được R² = %s, và có chỗ lệch tới %s lần. %s. Đường không "
           "thẳng là kết quả, không phải lỗi dữ liệu."
           % (year, R.fmt_vn(len(degrees_of(data["out"])), 0),
              R.fmt_vn(fit["r2"], 2), R.fmt_vn(fit["worst_ratio"], 0),
              uniform_phrase(gap)))
    src = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab). Bậc đếm "
           "trên đồ thị đầy đủ, chưa lọc cạnh. CCDF = hàm phân bố tích lũy bù.")

    w_pt = R.khung_pt(R.FIG_WIDTH_FULL)
    h_pt = R.khung_pt(FIG_H_INCH)
    t_w = w_pt - 2 * MARGIN_X - 2 * TEXT_PAD
    title_w = R.wrap_pt(title, R.FONT_SIZES["title"], t_w)
    sub_w = R.wrap_pt(sub, R.FONT_SIZES["subtitle"], t_w)
    src_w = R.wrap_pt(src, R.FONT_SIZES["footnote"], t_w)
    m_t = (TEXT_PAD + R.n_lines(title_w) * R.FONT_SIZES["title"] * LINE_H
           + R.n_lines(sub_w) * R.FONT_SIZES["subtitle"] * LINE_H
           + SUBTITLE_BAND)
    m_b = (AXIS_BAND + LEG_BAND
           + R.n_lines(src_w) * R.FONT_SIZES["footnote"] * LINE_H + TEXT_PAD)
    plot_h = h_pt - m_t - m_b

    fig.update_layout(
        font=dict(family=", ".join(R.FONT_STACK), size=R.FONT_SIZES["legend"]),
        separators=",.",
        margin=dict(t=m_t, l=MARGIN_L, r=MARGIN_X, b=m_b),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        legend=dict(orientation="h", y=-((AXIS_BAND + 2.0) / plot_h), x=0,
                    xanchor="left", yanchor="top",
                    font=dict(size=R.FONT_SIZES["footnote"])),
        hovermode="closest",
    )
    # Tiêu đề hai bảng con nằm trong layout.annotations và mặc định 16 đơn vị —
    # ở khung point thì to ngang tiêu đề chính. Hạ cỡ và căn trái theo mép ô.
    k = 0
    for note in fig.layout.annotations:
        if note.text and note.text.startswith("<b>Thang"):
            note.font = dict(size=R.FONT_SIZES["axis"])
            note.xanchor = "left"
            note.x = fig.get_subplot(1, k + 1).xaxis.domain[0]
            k += 1

    def block(txt, y_from_top, size, color=None):
        fig.add_annotation(text=txt, showarrow=False, xref="paper",
                           yref="paper", x=0,
                           y=1 + (m_t - y_from_top) / plot_h,
                           xshift=-(MARGIN_L - TEXT_PAD), xanchor="left",
                           yanchor="top", align="left",
                           font=dict(size=size, color=color))

    block(title_w, TEXT_PAD, R.FONT_SIZES["title"])
    block(sub_w, TEXT_PAD + R.n_lines(title_w) * R.FONT_SIZES["title"] * LINE_H,
          R.FONT_SIZES["subtitle"], "#555555")
    fig.add_annotation(
        text=src_w, showarrow=False, xref="paper", yref="paper", x=0,
        y=-((AXIS_BAND + LEG_BAND) / plot_h),
        xshift=-(MARGIN_L - TEXT_PAD), xanchor="left", yanchor="top",
        align="left", font=dict(size=R.FONT_SIZES["footnote"], color="#777"))
    return fig


def save(fig, name):
    os.makedirs(OUTDIR, exist_ok=True)
    html = os.path.join(OUTDIR, name + ".html")
    fig.write_html(html, include_plotlyjs="cdn", config={"displayModeBar": False})
    print("  %s" % html)
    try:
        png = os.path.join(OUTDIR, name + ".png")
        R.xuat_png(fig, png, R.FIG_WIDTH_FULL, FIG_H_INCH)
        print("  %s" % png)
    except Exception as exc:
        print("  (không xuất được PNG: %s — bản .html vẫn dùng được)" % exc)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    args = ap.parse_args()

    print("Đọc phân bố bậc năm %d..." % args.year)
    data = load_ccdf(args.year)
    fit = fit_powerlaw(data["out"])
    gap = uniform_gap(data["out"])

    print("Dựng biểu đồ:")
    save(make_figure(data, args.year, fit, gap), "degree_loglog_%d" % args.year)

    # In lại mọi con số đã dùng trong tiêu đề, để ai cũng kiểm được bằng chính
    # script này thay vì phải tin vào câu tiêu đề.
    for kind in ("out", "in"):
        degs = degrees_of(data[kind])
        n = len(degs)
        def pct(p):
            return degs[min(n - 1, int(p * n))]
        print("\n%s — %d nước:" % (KIND_VI[kind], n))
        print("  nhỏ nhất %d · p25 %d · trung vị %d · p75 %d · p90 %d · lớn nhất %d"
              % (degs[0], pct(.25), degs[n // 2], pct(.75), pct(.90), degs[-1]))

    print("\nKiểm giả thuyết scale-free (bậc xuất khẩu, %d điểm):" % fit["n_points"])
    print("  độ dốc đường khớp   %s   (tức α = %s)"
          % (R.fmt_vn(fit["b"], 3), R.fmt_vn(-fit["b"], 2)))
    print("  R²                  %s" % R.fmt_vn(fit["r2"], 4))
    print("  chỗ lệch tệ nhất    %s lần" % R.fmt_vn(fit["worst_ratio"], 1))
    print("  đường khớp còn đòi CCDF > 100%% ở mọi bậc dưới %s"
          % R.fmt_vn(fit["crosses_one_at"], 0))
    print("  -> đường thẳng KHÔNG mô tả được phân bố này.")

    print("\nSo với phân bố đều hoàn toàn trên dải bậc %d–%d:"
          % (gap["lo"], gap["hi"]))
    print("  lệch lớn nhất %s tại bậc %d (thật %s so với đều %s)"
          % (R.fmt_vn(gap["gap"], 4), gap["degree"],
             R.fmt_pct(gap["obs"] * 100), R.fmt_pct(gap["uni"] * 100)))
    print("  -> %s. Phát hiện A3 trong docs/phat-hien-va-quyet-dinh.md."
          % ("gần như ĐỀU" if gap["near_uniform"] else "CHƯA đều"))


if __name__ == "__main__":
    main()

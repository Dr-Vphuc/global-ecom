"""Phân bố bậc trên thang log-log — mạng thương mại KHÔNG phải scale-free (T09).

Biểu đồ này tồn tại để bác bỏ một câu người ta hay nói mà không kiểm: "mạng
lưới thương mại là mạng scale-free, có vài hub lớn và phần còn lại là đuôi dài".
Với dữ liệu Atlas 2023 thì câu đó SAI, và chỗ sai nhìn thấy được bằng mắt trên
thang log-log.

Mạng scale-free có phân bố bậc theo luật lũy thừa, P(K ≥ k) ~ k^(-α), nên trên
giấy log-log nó là một ĐƯỜNG THẲNG dốc xuống. Mạng thương mại không như vậy:
nó gần như phẳng rồi rơi dựng đứng ở cuối. Lý do thực chất rất đơn giản — mật
độ mạng là 51,8%, tức là một nước trung bình giao thương với hơn một nửa thế
giới. Khi gần như ai cũng nối với gần như ai thì không có chỗ cho hub tồn tại:
bậc tối đa (447) chỉ gấp 1,8 lần bậc trung vị (242). Trong một mạng scale-free
thật, tỷ lệ đó là hàng trăm lần.

Tỷ lệ này còn ĐANG GIẢM theo thời gian: 2,6 lần năm 1995 xuống 1,8 lần năm
2023. Mạng thương mại ngày càng xa dạng scale-free, chứ không tiến về phía đó.

Vì sao điều này quan trọng với cả đồ án
---------------------------------------
Nó là lý do kỹ thuật để KHÔNG vẽ node-link cho toàn mạng, và là lý do phải lọc
ngưỡng ở T10. Nếu mạng có hub thật thì node-link sẽ tự hiện ra cấu trúc hình
sao, đọc được. Mạng này không có cấu trúc đó — vẽ cả 27.535 cạnh chỉ ra một
mảng mực. Cấu trúc thật của nó nằm ở TRỌNG SỐ (Gini 0,957), không nằm ở tô-pô.

Hai đường tham chiếu được vẽ kèm để người xem tự so, không phải tin lời:
  - luật lũy thừa α = 2,0 (dáng điệu mà mạng scale-free sẽ có)
  - mạng ngẫu nhiên Erdős–Rényi cùng mật độ (dáng điệu của mạng "ai cũng nối
    với ai một cách tình cờ")
Phân bố thật nằm gần đường ngẫu nhiên hơn hẳn đường lũy thừa.

Chạy
----
    python src/make_degree_dist.py
    python src/make_degree_dist.py --kind in
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
OUTDIR = os.path.join(ROOT, "output")

# Màu cho bốn năm mốc: thang tuần tự của style guide, nhạt = cũ, đậm = mới.
# Dùng thang TUẦN TỰ chứ không phải bảng màu ngành, vì năm là biến có thứ tự.
YEAR_COLORS = {1995: "#FEE391", 2005: "#FE9929", 2015: "#CC4C02", 2023: "#662506"}


def log(msg):
    print(msg)
    sys.stdout.flush()


def load_ccdf(kind):
    """Đọc degree_distribution.csv -> {năm: [(bậc, ccdf), ...]}."""
    path = os.path.join(PROC, "degree_distribution.csv")
    if not os.path.exists(path):
        sys.exit("Thiếu %s. Chạy: python src/analyze_network.py" % path)
    out = {}
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["kind"] != kind:
                continue
            y = int(r["year"])
            out.setdefault(y, []).append((int(r["degree"]), float(r["ccdf"])))
    for y in out:
        out[y].sort()
    return out


def load_stats():
    """Đọc network_stats.csv -> {năm: dict}."""
    path = os.path.join(PROC, "network_stats.csv")
    if not os.path.exists(path):
        sys.exit("Thiếu %s. Chạy: python src/analyze_network.py" % path)
    out = {}
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[int(r["year"])] = r
    return out


def powerlaw_ref(kmin, kmax, alpha, anchor_k, anchor_y):
    """Đường luật lũy thừa đi qua một điểm neo, để so dáng điệu.

    Neo vào một điểm của phân bố thật thay vì khớp bình phương tối thiểu: mục
    đích ở đây là so DÁNG ĐIỆU (thẳng hay không thẳng), không phải ước lượng α.
    Khớp số mũ cho một phân bố không phải lũy thừa sẽ ra một con số vô nghĩa mà
    trông lại có vẻ khoa học.
    """
    ks, ys = [], []
    k = kmin
    while k <= kmax:
        ks.append(k)
        ys.append(min(1.0, anchor_y * (k / anchor_k) ** (-alpha)))
        k = int(k * 1.12) + 1
    return ks, ys


def binomial_ccdf(n, p, kmax):
    """CCDF bậc của mạng ngẫu nhiên Erdős–Rényi: bậc ~ Binomial(n-1, p).

    Tính bằng hàm phân phối tích lũy chính xác, không xấp xỉ chuẩn, vì đuôi
    phân bố là chỗ ta đang muốn nhìn và xấp xỉ chuẩn sai nhiều nhất ở đuôi.
    """
    trials = n - 1
    # pmf dựng theo truy hồi để tránh tràn số khi tính hệ số tổ hợp trực tiếp.
    pmf = [0.0] * (trials + 1)
    pmf[0] = (1 - p) ** trials if p < 1 else 0.0
    for k in range(trials):
        if 1 - p <= 0:
            break
        pmf[k + 1] = pmf[k] * (trials - k) / (k + 1) * p / (1 - p)
    ks, ys = [], []
    tail = 1.0
    for k in range(0, min(kmax, trials) + 1):
        ks.append(k)
        ys.append(max(tail, 1e-6))
        tail -= pmf[k]
    return ks, ys


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kind", choices=["out", "in"], default="out",
                    help="bậc ra (số thị trường xuất) hay bậc vào (nguồn nhập)")
    args = ap.parse_args()

    ccdf = load_ccdf(args.kind)
    stats = load_stats()
    years = [y for y in R.MILESTONE_YEARS if y in ccdf]
    if not years:
        sys.exit("Không có năm mốc nào trong degree_distribution.csv")

    kind_vi = "xuất khẩu" if args.kind == "out" else "nhập khẩu"

    fig = go.Figure()

    # --- Hai đường tham chiếu vẽ TRƯỚC, để nằm dưới dữ liệu thật -----------
    ref_year = years[-1]
    pts = ccdf[ref_year]
    kmax = max(k for k, _ in pts)
    # Neo đường lũy thừa vào trung vị của phân bố thật.
    mid = min(pts, key=lambda kv: abs(kv[1] - 0.5))

    ks, ys = powerlaw_ref(1, kmax * 2, 2.0, mid[0], mid[1])
    fig.add_trace(go.Scatter(
        x=ks, y=ys, mode="lines", name="nếu là scale-free (α = 2,0)",
        line=dict(color="#999999", width=2, dash="dash"),
        hovertemplate="luật lũy thừa α=2,0<br>bậc %{x}: %{y:.3f}<extra></extra>",
    ))

    st = stats[ref_year]
    bk, by = binomial_ccdf(int(st["n_nodes"]), float(st["density"]), kmax)
    fig.add_trace(go.Scatter(
        x=bk, y=by, mode="lines",
        name="nếu nối ngẫu nhiên (cùng mật độ %s)"
             % R.fmt_pct(float(st["density"]) * 100),
        line=dict(color="#BBBBBB", width=2, dash="dot"),
        hovertemplate="mạng ngẫu nhiên<br>bậc %{x}: %{y:.3f}<extra></extra>",
    ))

    # --- Phân bố thật của bốn năm mốc --------------------------------------
    for y in years:
        pts = ccdf[y]
        fig.add_trace(go.Scatter(
            x=[k for k, _ in pts], y=[c for _, c in pts],
            mode="lines", name="thực tế %d" % y,
            line=dict(color=YEAR_COLORS.get(y, "#662506"),
                      width=R.HIGHLIGHT_LINE_WIDTH if y == R.REFERENCE_YEAR
                      else R.DEFAULT_LINE_WIDTH + 0.8),
            hovertemplate=("năm %d<br>có %%{y:.1%%} số nước giao thương với "
                           "%%{x} đối tác trở lên<extra></extra>" % y),
        ))

    st23 = stats[R.REFERENCE_YEAR]
    ratio = int(st23["max_degree"]) / max(1, int(st23["median_degree"]))

    fig.update_layout(
        title=dict(
            text="<b>Mạng lưới thương mại không có hub — nó gần như là một đám "
                 "đông ai cũng biết ai</b>"
                 "<br><span style='font-size:%dpx;color:#555'>"
                 "Phân bố bậc %s trên thang log-log, %d. Nếu là mạng scale-free, "
                 "đường thực tế phải THẲNG như đường gạch xám. "
                 "Nó không thẳng: bậc cao nhất (%d) chỉ gấp %s lần bậc trung vị "
                 "(%d).</span>"
                 % (R.FONT_SIZES["subtitle"], kind_vi, R.REFERENCE_YEAR,
                    int(st23["max_degree"]), R.fmt_vn(ratio),
                    int(st23["median_degree"])),
            x=0.01, xanchor="left", font=dict(size=R.FONT_SIZES["title"] + 4),
        ),
        xaxis=dict(
            title="Số đối tác %s của một nước (bậc k) — thang log" % kind_vi,
            type="log", gridcolor="#EEEEEE", zeroline=False,
        ),
        yaxis=dict(
            title="Tỷ lệ số nước có bậc ≥ k — thang log",
            type="log", gridcolor="#EEEEEE", zeroline=False,
            tickformat=".0%",
        ),
        font=dict(family=", ".join(R.FONT_STACK), size=R.FONT_SIZES["legend"]),
        separators=",.",
        legend=dict(yanchor="bottom", y=0.02, xanchor="left", x=0.02,
                    bgcolor="rgba(255,255,255,0.85)", bordercolor="#DDDDDD",
                    borderwidth=1),
        margin=dict(t=100, l=70, r=20, b=70),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        annotations=[dict(
            text="Nguồn: Atlas of Economic Complexity (Harvard Growth Lab). "
                 "Hai thang đều là log. Đường tham chiếu lũy thừa neo vào trung "
                 "vị của phân bố %d, không phải khớp bình phương tối thiểu."
                 % ref_year,
            showarrow=False, xref="paper", yref="paper", x=0, y=-0.16,
            xanchor="left", font=dict(size=R.FONT_SIZES["footnote"], color="#777"),
        )],
    )

    # Dùng chung graph_common.save để bản .html co giãn đúng như sáu hình mạng
    # lưới kia — nếu không, hình này là hình duy nhất bị thanh cuộn khi nhúng
    # vào trang web ở T27.
    GC.save(fig, "degree_dist_%s" % args.kind, width=1300, height=850, log=log)

    # --- In bằng chứng để ai cũng kiểm lại được ----------------------------
    log("")
    log("Bằng chứng cho tiêu đề — mạng này KHÔNG scale-free:")
    log("  %-6s %9s %9s %9s %9s %12s" % ("năm", "mật độ", "bậc TV", "bậc max",
                                         "max/TV", "Gini trọng số"))
    for y in years:
        s = stats[y]
        r = int(s["max_degree"]) / max(1, int(s["median_degree"]))
        log("  %-6d %9s %9s %9s %9s %12s"
            % (y, R.fmt_pct(float(s["density"]) * 100), s["median_degree"],
               s["max_degree"], R.fmt_vn(r), R.fmt_vn(float(s["gini_edge_value"]), 3)))
    log("")
    log("  Trong mạng scale-free thật, max/TV là hàng trăm lần. Ở đây là %s."
        % R.fmt_vn(ratio))
    log("  Cấu trúc của mạng này KHÔNG nằm ở tô-pô (ai nối với ai) mà nằm ở")
    log("  TRỌNG SỐ (nối chặt đến đâu): Gini = %s."
        % R.fmt_vn(float(st23["gini_edge_value"]), 3))
    log("  -> Đây là lý do kỹ thuật phải lọc ngưỡng ở T10 trước khi vẽ node-link.")


if __name__ == "__main__":
    main()

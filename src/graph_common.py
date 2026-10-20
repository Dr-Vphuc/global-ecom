"""Phần dùng chung của ba hình mạng lưới (T15 node-link, T16 ma trận, T17 chord).

Ba hình đó PHẢI nói về cùng một đồ thị, nếu không thì so sánh chúng vô nghĩa —
và checklist nộp bài mục 5 yêu cầu đúng phép so sánh ấy: "có so sánh trực tiếp
node-link và ma trận kề trên CÙNG dữ liệu". Nên việc chọn cạnh, dò cộng đồng và
sắp thứ tự nút nằm ở đây, một chỗ duy nhất, chứ không chép ba lần.

Đồ thị dùng cho cả ba hình là đồ thị ĐÃ LỌC ở T10: ngưỡng 0,046% tổng xuất khẩu
thế giới cộng với giữ top-3 luồng vào/ra cho mỗi nước ASEAN. Năm 2023 còn 416
cạnh trên 73 nút, giữ 67,8% giá trị. Lý do phải lọc nằm ở T09: mạng đầy đủ có
mật độ 51,8% và không có hub, nên vẽ cả 27.535 cạnh chỉ ra một mảng mực.

Mọi hàm ở đây mượn lại ``compute_metrics.py`` thay vì tự dựng, để hình vẽ và
bảng số không bao giờ lệch nhau.
"""

from __future__ import annotations

import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reference_data as R  # noqa: E402

try:
    import networkx as nx
except ImportError:
    sys.exit("Thiếu networkx. Chạy: python -m pip install networkx")

import compute_metrics as CM  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "output")

# Hạt giống mặc định phải GIỐNG compute_metrics.py, nếu không số cụm trên hình
# sẽ khác số cụm trong metrics.csv và không ai biết tin cái nào.
DEFAULT_SEED = 42


def load_graph(year=None, seed=DEFAULT_SEED):
    """Dựng đồ thị đã lọc của một năm, kèm cộng đồng và thông tin nút.

    Trả về dict gồm:
        g        — DiGraph đã lọc (trọng số = export_value)
        u        — bản vô hướng, dùng để dò cộng đồng và để vẽ
        comm     — {iso3: số cụm}, cụm 0 là cụm đông nhất
        meta     — {iso3: dòng của nodes.csv}
        strength — {iso3: tổng xuất + nhập trong đồ thị đã lọc}
        year     — năm thực dùng
    """
    year = year or R.REFERENCE_YEAR
    meta = CM.load_nodes()
    _, filt = CM.load_edges(year)
    if not filt:
        sys.exit("Năm %d không có cạnh nào qua ngưỡng. Chạy lại "
                 "python src/build_intermediate.py" % year)

    g = CM.build(filt)
    u = CM.undirected_projection(g)
    comm, _parts = CM.louvain(u, seed)

    strength = {}
    for n in g.nodes():
        out = sum(d["weight"] for _, _, d in g.out_edges(n, data=True))
        inn = sum(d["weight"] for _, _, d in g.in_edges(n, data=True))
        strength[n] = out + inn

    return dict(g=g, u=u, comm=comm, meta=meta, strength=strength, year=year)


def name_vi(iso, meta=None):
    """Tên tiếng Việt của một nước. Ưu tiên nodes.csv, rồi đến bảng tra."""
    if meta and iso in meta and meta[iso].get("country_name_vi"):
        return meta[iso]["country_name_vi"]
    return R.COUNTRY_VI.get(iso, (iso,))[0]


def community_order(gd):
    """Thứ tự nút GOM THEO CỤM — dùng cho ma trận kề đã sắp lại (T16).

    Trong mỗi cụm, sắp theo độ mạnh giảm dần để nước lớn nằm trên, nhìn ra khối
    ngay. Giữa các cụm, sắp theo kích thước cụm giảm dần (cụm 0 trước).
    """
    nodes = list(gd["g"].nodes())
    return sorted(nodes, key=lambda n: (gd["comm"].get(n, 99),
                                        -gd["strength"].get(n, 0)))


def alpha_order(gd):
    """Thứ tự nút theo TÊN TIẾNG VIỆT — thứ tự 'mặc định' của ma trận kề.

    Sắp theo tên tiếng Việt, không theo mã ISO3: người xem đọc nhãn tiếng Việt
    nên thứ tự phải khớp với cái họ đọc. Dùng khóa không dấu để Đ không nhảy
    xuống sau Z.
    """
    nodes = list(gd["g"].nodes())
    return sorted(nodes, key=lambda n: strip_tones(name_vi(n, gd["meta"])).lower())


def strip_tones(s):
    """Bỏ dấu để SẮP THỨ TỰ. Không dùng để hiển thị.

    Dựng bảng bằng unicodedata thay vì gõ tay hai dãy ký tự song song: dãy gõ
    tay dài 68 ký tự rất dễ lệch một ô, mà lệch thì str.maketrans() ném lỗi
    ngay lúc import — cả module chết. Tách dấu rồi bỏ ký tự tổ hợp thì không
    có gì để lệch. Chữ đ/Đ phải xử riêng vì nó KHÔNG phải d có dấu, mà là một
    chữ cái khác trong Unicode, nên NFD không tách nó ra.
    """
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if not unicodedata.combining(c))



def source_note(year, extra=""):
    """Chú thích nguồn dùng chung, để ba hình ghi giống nhau từng chữ."""
    base = ("Nguồn: Atlas of Economic Complexity (Harvard Growth Lab), năm %d. "
            "Đồ thị đã lọc theo ngưỡng T10 (%s tổng xuất khẩu thế giới, cộng "
            "top-%d luồng vào/ra mỗi nước ASEAN)."
            % (year, R.fmt_pct(R.THRESHOLD_SHARE * 100, 3), R.FOCUS_TOPK))
    return base + (" " + extra if extra else "")


def base_layout(title, subtitle, note, **kw):
    """Khung layout dùng chung: phông, dấu thập phân, vị trí tiêu đề, nguồn."""
    lay = dict(
        title=dict(
            text="<b>%s</b><br><span style='font-size:%dpx;color:#555'>%s</span>"
                 % (title, R.FONT_SIZES["subtitle"], subtitle),
            x=0.01, xanchor="left", font=dict(size=R.FONT_SIZES["title"] + 4),
        ),
        font=dict(family=", ".join(R.FONT_STACK), size=R.FONT_SIZES["legend"]),
        separators=",.",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
    )
    lay.update(kw)
    anns = list(lay.get("annotations") or [])
    anns.append(dict(text=note, showarrow=False, xref="paper", yref="paper",
                     x=0, y=-0.07, xanchor="left",
                     font=dict(size=R.FONT_SIZES["footnote"], color="#777")))
    lay["annotations"] = anns
    return lay


def save(fig, stem, width=1400, height=950, log=print):
    """Ghi ra .html tương tác và .png tĩnh. Thiếu kaleido thì vẫn có .html.

    Bản .html ghi ở chế độ CO GIÃN (100% khung chứa, ``responsive``), không ghi
    kích thước cố định. Lý do: trang web ở T27 nhúng mỗi biểu đồ vào một
    ``<iframe>``, mà iframe thì có chiều cao do trang ngoài đặt. Nếu biểu đồ
    giữ kích thước cứng thì nó hoặc tràn ra ngoài khung và sinh thanh cuộn
    trong thanh cuộn, hoặc để thừa một mảng trắng. Co giãn thì nó vừa đúng
    khung, và cũng vừa đúng màn hình điện thoại khi mở trực tiếp.

    Bản .png vẫn dùng kích thước cố định ``width`` × ``height``, vì ảnh tĩnh
    cho slide và báo cáo LaTeX thì phải có kích thước xác định.
    """
    os.makedirs(OUTDIR, exist_ok=True)
    html = os.path.join(OUTDIR, stem + ".html")
    fig.write_html(html, include_plotlyjs="cdn",
                   default_width="100%", default_height="100%",
                   config={"responsive": True, "displaylogo": False})
    log("  %s" % html)
    try:
        png = os.path.join(OUTDIR, stem + ".png")
        fig.write_image(png, width=width, height=height, scale=2)
        log("  %s" % png)
    except Exception as exc:
        log("  (không xuất được PNG: %s — bản .html vẫn dùng được)" % exc)

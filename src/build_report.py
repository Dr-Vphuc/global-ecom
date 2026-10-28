# -*- coding: utf-8 -*-
"""T27 — ráp báo cáo cuối từ các mục rời trong `.report/final/`.

Vì sao có script này thay vì ghép tay
-------------------------------------
Quyết định **B21**: báo cáo viết thành nhiều file Markdown, một file một mục, để
diff của một PR đọc được theo câu và rà soát chéo được (T23). Hệ quả là phải có
một bước ráp — và bước ráp đó phải **tự kiểm**, vì sau khi T27 đổi số hiệu mục
(§2.4 → §A.1, §3.6 → §5.3 …) thì mọi tham chiếu chéo trong 10 file đều có thể trỏ
vào chỗ không còn tồn tại. Script in ra danh sách tham chiếu **không giải được**;
đạt là khi danh sách đó rỗng.

Ra hai bản:

* `output/bao-cao-cuoi.md`  — một file Markdown, ảnh trỏ tới PNG cùng thư mục
* `output/bao-cao-cuoi.html` — một file đứng một mình, PNG nhúng base64, in A4 được

Chạy:

    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/build_report.py
    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/build_report.py --no-figures
"""
import argparse
import base64
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_data as R                                    # noqa: E402

SECTIONS = ".report/final"
OUT = "output"
TITLE = "Mạng lưới thương mại quốc tế — vị tr\xed của Việt Nam trong cấu tr\xfac thương mại to\xe0n cầu"

# Mỗi hình đứng sau mục nào, và chú thích của nó.
# Khớp với bảng danh mục hình ở §1.4 — sửa ở đây thì sửa cả ở đó.
FIGURES = [
    ("3.2", "stream_sectors_1995_2023", "T21 — dòng chảy cơ cấu xuất khẩu 10 ngành, 1995–2023"),
    ("3.2", "treemap_vnm_2023", "T12 — treemap cơ cấu xuất khẩu Việt Nam, 2023"),
    ("3.2", "sunburst_vnm_2023", "T13 — sunburst 4 tầng cây sản phẩm HS92, Việt Nam 2023"),
    ("4.1", "degree_loglog_2023", "T09 — phân bố bậc log-log, mạng xuất khẩu toàn cầu 2023"),
    ("4.1", "node_link_2023", "T15 — node-link mạng đã lọc, 2023"),
    ("4.2", "adjacency_cluster_2023", "T16 — ma trận kề sắp theo cụm Louvain, 2023"),
    ("4.2", "chord_bloc_2023", "T17 — chord giữa tám khối, 2023"),
    ("4.2", "chord_bloc_1995", "T17 — cùng hình, năm đối chứng 1995"),
    ("5.1", "small_multiples_vnm-tha-mys-idn_2023", "T14 — Việt Nam so với Thái Lan, Malaysia, Indonesia"),
    ("5.2", "sankey_vietnam_2023", "T19 — Sankey nhập → Việt Nam → xuất, 2023"),
    ("5.3", "time_multiples_xuat", "T20 — Việt Nam bán cho ai, bốn năm mốc"),
    ("5.3", "time_multiples_nhap", "T20 — Việt Nam mua từ ai, bốn năm mốc"),
    ("6.1", "decision_plane_2023", "T31 — mặt phẳng quyết định RCA × PCI, 2023"),
    ("7.2", "decision_plane_2015", "T31 — cùng quy tắc chạy trên dữ liệu 2015"),
]

TU_MOI_TRANG = 500          # chữ/trang A4 cỡ 11pt, giãn 1,15 — để quy ra số trang


# ---------------------------------------------------------------- đọc và ráp

def doc_cac_muc():
    """Đọc các file mục theo đúng thứ tự tên file."""
    fs = sorted(f for f in os.listdir(SECTIONS) if f.endswith(".md"))
    return [(f, io.open(os.path.join(SECTIONS, f), encoding="utf-8").read()) for f in fs]


def dem_tu(s):
    """Đếm chữ của phần văn xuôi: bỏ bảng, khối code, ký hiệu markdown."""
    s = re.sub(r"```.*?```", " ", s, flags=re.S)
    s = "\n".join(l for l in s.split("\n") if not l.lstrip().startswith("|"))
    s = re.sub(r"[#>*`_|·•→←—–]", " ", s)
    return len([w for w in s.split() if any(c.isalnum() for c in w)])


def chen_hinh(body, co_hinh):
    """Chèn ảnh ngay sau đoạn mở của mục tương ứng, trước mục kế tiếp."""
    if not co_hinh:
        return body, []
    dung = []
    for so, ten, chu in FIGURES:
        png = os.path.join(OUT, ten + ".png")
        if not os.path.isfile(png):
            print("  thiếu hình %s — bỏ qua" % png)
            continue
        # chèn ngay trước dòng "Lấy lại:" của mục đó, nếu không có thì cuối mục
        m = re.search(r"^## %s .*$" % re.escape(so), body, flags=re.M)
        if not m:
            print("  không thấy mục §%s để chèn hình %s" % (so, ten))
            continue
        ke = re.search(r"^## ", body[m.end():], flags=re.M)
        het = m.end() + (ke.start() if ke else len(body) - m.end())
        n = len(dung) + 1
        khoi = "\n![H\xecnh %d. %s](%s.png)\n\n*H\xecnh %d. %s*\n" % (n, chu, ten, n, chu)
        body = body[:het].rstrip() + "\n" + khoi + "\n" + body[het:]
        dung.append((n, ten, chu))
    return body, dung


def muc_luc(bodies):
    """Dựng mục lục từ chính các tiêu đề, không viết tay."""
    dong = []
    for _, s in bodies:
        for l in s.split("\n"):
            if re.match(r"^# ", l):
                dong.append("- **%s**" % l[2:].strip())
            elif re.match(r"^## ", l):
                dong.append("  - %s" % l[3:].strip())
    return "\n".join(dong)


# ---------------------------------------------------- Markdown → HTML tối giản

def inline(s):
    # cất khối `code` ra trước: tên cột kiểu source_iso3 có dấu gạch dưới, nếu
    # để nguyên thì phép đổi _nghiêng_ sẽ cắt ngang hai định danh trong cùng câu
    giu = []

    def cat(m):
        giu.append(m.group(1))
        return "\x00%d\x00" % (len(giu) - 1)

    s = re.sub(r"`([^`]+)`", cat, s)
    s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    # đậm có thể bọc nghiêng ("**đồ thị *đã lọc***"), nên phải bắt ba dấu trước,
    # rồi dùng mẫu không tham lam cho hai dấu — mẫu [^*]+ cũ bỏ sót các chỗ đó
    s = re.sub(r"\*\*\*([^*]+)\*\*\*", r"<strong><em>\1</em></strong>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w_])_([^_\n]+)_(?![\w_])", r"<em>\1</em>", s)
    for i, c in enumerate(giu):
        c = c.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        s = s.replace("\x00%d\x00" % i, "<code>%s</code>" % c)
    return s


def md_html(md):
    """Đủ cho đúng tập cú pháp mà báo cáo này dùng, không nhiều hơn."""
    out, i, lines = [], 0, md.split("\n")
    while i < len(lines):
        l = lines[i]
        if l.startswith("```"):
            j = i + 1
            buf = []
            while j < len(lines) and not lines[j].startswith("```"):
                buf.append(lines[j])
                j += 1
            esc = "\n".join(buf).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            out.append("<pre><code>%s</code></pre>" % esc)
            i = j + 1
        elif re.match(r"^#{1,4} ", l):
            n = len(l) - len(l.lstrip("#"))
            out.append("<h%d>%s</h%d>" % (n, inline(l[n + 1:]), n))
            i += 1
        elif l.startswith("|"):
            tbl = []
            while i < len(lines) and lines[i].startswith("|"):
                tbl.append(lines[i])
                i += 1
            out.append(bang_html(tbl))
        elif l.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip(">").strip())
                i += 1
            out.append("<blockquote>%s</blockquote>" % inline(" ".join(buf)))
        elif re.match(r"^\s*[-*] ", l) or re.match(r"^\s*\d+\. ", l):
            thu_tu = bool(re.match(r"^\s*\d+\. ", l))
            buf = []
            while i < len(lines) and (re.match(r"^\s*[-*] ", lines[i])
                                      or re.match(r"^\s*\d+\. ", lines[i])
                                      # dòng nối tiếp của một gạch đầu dòng thụt 2
                                      # dấu cách, của một mục số thì 3
                                      or (lines[i].startswith("  ") and lines[i].strip())):
                if re.match(r"^\s*([-*]|\d+\.) ", lines[i]):
                    buf.append(re.sub(r"^\s*([-*]|\d+\.) ", "", lines[i]))
                else:
                    buf[-1] += " " + lines[i].strip()
                i += 1
            tag = "ol" if thu_tu else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(b) for b in buf), tag))
        elif l.strip() in ("---", "***"):
            out.append("<hr>")
            i += 1
        elif not l.strip():
            i += 1
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not re.match(
                    r"^(#{1,4} |\||>|```|\s*[-*] |\s*\d+\. |---$)", lines[i]):
                buf.append(lines[i])
                i += 1
            txt = " ".join(buf)
            if txt.startswith("*H\xecnh ") and txt.endswith("*"):
                out.append("<p class=\"chu-thich\">%s</p>" % inline(txt))
            else:
                out.append("<p>%s</p>" % inline(txt))
    return "\n".join(out)


def bang_html(rows):
    rows = [r for r in rows if not re.match(r"^\|[\s:|-]+\|$", r)]
    def o(r):
        return [c.strip() for c in r.strip().strip("|").split("|")]
    h = "".join("<th>%s</th>" % inline(c) for c in o(rows[0]))
    b = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in o(r))
                for r in rows[1:])
    return "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (h, b)


CSS = """
:root { --muc: #1f3b57; --phu: #5a6b7a; --vien: #d7dee4; --nen-bang: #f4f7f9; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI", "Helvetica Neue", Arial, sans-serif;
       font-size: 11.5pt; line-height: 1.55; color: #16222c; margin: 0;
       background: #fff; }
.trang { max-width: 19cm; margin: 0 auto; padding: 1.6cm 1.2cm 3cm; }
h1 { font-size: 20pt; color: var(--muc); border-bottom: 2px solid var(--muc);
     padding-bottom: .25em; margin-top: 2.2em; page-break-before: always; }
h1.bia, h1:first-of-type { page-break-before: auto; }
h2 { font-size: 14pt; color: var(--muc); margin-top: 1.8em; }
h3 { font-size: 12pt; color: var(--phu); margin-top: 1.4em; }
p { margin: .55em 0; text-align: justify; }
code { font-family: Consolas, "Courier New", monospace; font-size: .88em;
       background: var(--nen-bang); padding: .08em .3em; border-radius: 3px; }
pre { background: var(--nen-bang); border-left: 3px solid var(--muc);
      padding: .7em .9em; overflow-x: auto; }
pre code { background: none; padding: 0; font-size: .82em; }
blockquote { margin: .9em 0; padding: .6em .95em; background: var(--nen-bang);
             border-left: 3px solid var(--muc); }
blockquote p { margin: 0; }
table { border-collapse: collapse; width: 100%; margin: .9em 0; font-size: .9em;
        page-break-inside: avoid; }
th, td { border: 1px solid var(--vien); padding: .34em .5em; text-align: left;
         vertical-align: top; }
th { background: var(--nen-bang); }
img { max-width: 100%; height: auto; display: block; margin: 1em auto .3em;
      page-break-inside: avoid; }
p.chu-thich { text-align: center; font-size: .85em; color: var(--phu);
              margin: 0 0 1.3em; }
hr { border: 0; border-top: 1px solid var(--vien); margin: 1.6em 0; }
.bia-phu { color: var(--phu); font-size: 1.05em; }
.ml { font-size: .92em; }
.ml a { text-decoration: none; }
@media print {
  .trang { max-width: none; padding: 0; }
  body { font-size: 10.5pt; }
  @page { size: A4; margin: 1.8cm 1.6cm; }
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-figures", action="store_true", help="không chèn hình")
    ap.add_argument("--embed", action="store_true",
                    help="nhúng PNG base64 vào HTML — một file đứng một mình, "
                         "nhưng nặng ~8,6 MB và trình duyệt vẽ chậm hẳn; mặc định "
                         "để HTML trỏ sang PNG cùng thư mục output/")
    a = ap.parse_args()

    bodies = doc_cac_muc()
    if not bodies:
        print("không thấy file mục nào trong %s" % SECTIONS)
        return 1

    # đếm chữ trước khi chèn hình, rồi chèn một lượt trên bản đã ghép —
    # nếu chèn theo từng file thì số hiệu hình sẽ đếm lại từ 1 ở mỗi file
    md_parts = bodies
    tong_md, hinh = chen_hinh("\n\n".join(s for _, s in md_parts),
                              not a.no_figures)
    bia = ("# %s\n\n**Đồ án cuối kỳ — Trực quan hóa dữ liệu**\n\n"
           "Lát cắt Việt Nam – ASEAN · dữ liệu Atlas of Economic Complexity "
           "(Harvard Growth Lab), 1995–2023 · năm tham chiếu **%d**\n\n"
           "Nhóm 8 · `github.com/Dr-Vphuc/global-ecom`\n\n---\n\n"
           "## Mục lục\n\n%s\n" % (TITLE, R.REFERENCE_YEAR, muc_luc(md_parts)))
    full_md = bia + "\n\n" + tong_md

    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    p_md = os.path.join(OUT, "bao-cao-cuoi.md")
    io.open(p_md, "w", encoding="utf-8", newline="\n").write(full_md)

    html_md = full_md
    if a.embed:
        for _, ten, _ in hinh:
            png = os.path.join(OUT, ten + ".png")
            b64 = base64.b64encode(io.open(png, "rb").read()).decode("ascii")
            html_md = html_md.replace("(%s.png)" % ten,
                                      "(data:image/png;base64,%s)" % b64)
    html = ("<!doctype html>\n<html lang=\"vi\"><head><meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            "<title>%s</title>\n<style>%s</style></head>\n<body><div class=\"trang\">\n%s\n"
            "</div></body></html>\n" % (TITLE, CSS, md_html(html_md)))
    p_html = os.path.join(OUT, "bao-cao-cuoi.html")
    io.open(p_html, "w", encoding="utf-8", newline="\n").write(html)

    # ------------------------------------------------------------- kiểm chứng
    print("=" * 70)
    print("KIỂM CHỨNG — ráp báo cáo cuối")
    print("=" * 70)
    tong_tu = 0
    print("  %-28s %7s %7s" % ("mục", "chữ", "trang"))
    for ten, s in md_parts:
        t = dem_tu(s)
        tong_tu += t
        print("  %-28s %7s %7s" % (ten, R.fmt_vn(t, 0), R.fmt_vn(t / float(TU_MOI_TRANG), 1)))
    print("  %-28s %7s %7s" % ("TỔNG", R.fmt_vn(tong_tu, 0),
                               R.fmt_vn(tong_tu / float(TU_MOI_TRANG), 1)))
    phu = dem_tu(dict(md_parts).get("09-phu-luc.md", ""))
    print("  trong đó phụ lục %s chữ — thân báo cáo %s chữ, khoảng %s trang"
          % (R.fmt_vn(phu, 0), R.fmt_vn(tong_tu - phu, 0),
             R.fmt_vn((tong_tu - phu) / float(TU_MOI_TRANG), 1)))

    # tham chiếu chéo: mọi §x.y phải trỏ tới một tiêu đề có thật
    co = set(re.findall(r"^#{1,3} ([0-9A-Z]+\.[0-9]+) ", tong_md, flags=re.M))
    ref = set(re.findall(r"§([0-9A-Z]+\.[0-9]+)", tong_md))
    hong = sorted(ref - co)
    print("\n  Tiêu đề mục có thật: %d — %s" % (len(co), ", ".join(sorted(co))))
    print("  Tham chiếu §x.y xuất hiện: %d loại" % len(ref))
    print("  Tham chiếu KHÔNG giải được: %s"
          % (", ".join("§" + h for h in hong) if hong else "(không có — ĐẠT)"))

    con = re.findall(r"<<<FRAG:[^>]+>>>", tong_md)
    print("  Chỗ đặt mảnh còn sót: %s" % ("%d — LỖI" % len(con) if con else "0 — ĐẠT"))

    print("\n  Hình đã nhúng: %d/%d" % (len(hinh), len(FIGURES)))
    for n, ten, chu in hinh:
        print("    %2d. %-38s %s" % (n, ten + ".png", chu[:44]))

    for p in (p_md, p_html):
        print("\n  %s  (%s MB)" % (p, R.fmt_vn(os.path.getsize(p) / 1024.0 / 1024.0, 2)))
    return 1 if (hong or con) else 0


if __name__ == "__main__":
    sys.exit(main())

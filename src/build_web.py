"""Dựng trang web tương tác từ các biểu đồ đã sinh (T27).

Trang này KHÔNG vẽ lại gì cả. Nó lắp các file .html mà những script vẽ đã xuất
ra ``output/`` vào một mạch kể bốn hồi, rồi ghi thành một thư mục tĩnh chạy
được bằng cách mở file hoặc đẩy lên GitHub Pages.

Vì sao trang TĨNH, không phải Streamlit hay Dash
-------------------------------------------------
Streamlit và Dash cần một tiến trình server chạy nền. Hôm pitching mà máy ngủ,
wifi rớt, hay cổng bị chiếm thì mất luôn phần demo. Trang tĩnh thì chỉ là file:
mở bằng trình duyệt là xong, không phụ thuộc gì. Biểu đồ vẫn tương tác đầy đủ
vì Plotly đã nhúng sẵn JavaScript trong từng file .html.

Đổi lại: không lọc được dữ liệu theo thời gian thực trên trang. Chấp nhận, vì
mỗi script vẽ đã có tham số ``--year`` để sinh sẵn các bản cần dùng.

Vì sao dùng <iframe> chứ không nhúng thẳng
-------------------------------------------
Mỗi file Plotly mang theo CSS và JavaScript toàn cục của riêng nó. Dán mười file
như vậy vào chung một trang thì chúng giẫm lên nhau — biểu đồ sau ghi đè cấu
hình của biểu đồ trước. iframe cho mỗi biểu đồ một vùng cách ly hoàn toàn, và
đó cũng là lý do trang này nhẹ: trình duyệt chỉ tải biểu đồ khi cuộn tới
(``loading="lazy"``).

Chạy
----
    python src/build_web.py
    python src/build_web.py --open     # dựng xong mở luôn bằng trình duyệt

Kết quả nằm ở ``web/``. Đẩy lên GitHub Pages: bật Pages, trỏ vào thư mục
``web/`` của nhánh chính.
"""

from __future__ import annotations

import argparse
import html
import os
import sys
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reference_data as R  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "output")
WEB = os.path.join(ROOT, "web")
CHARTS = os.path.join(WEB, "charts")

# Mạch bốn hồi đã chốt ở docs/phat-hien-va-quyet-dinh.md:
#   Quy mô -> Cấu trúc -> Vị trí Việt Nam -> Ý nghĩa
#
# Mỗi biểu đồ ghi kèm "nhìn vào đâu" — vì một biểu đồ tương tác mà không nói
# nên nhìn gì thì người xem chỉ rê chuột lung tung rồi bỏ qua.
SECTIONS = [
    {
        "id": "quy-mo",
        "no": "1",
        "title": "Quy mô",
        "lead": "Mạng lưới thương mại thế giới lớn cỡ nào, và nó có hình gì?",
        "charts": [
            {
                "file": "degree_dist_out.html",
                "task": "T09",
                "title": "Mạng lưới không có hub",
                "look": "Đường gạch xám là dáng điệu mà một mạng scale-free "
                        "sẽ có — một đường thẳng. Bốn đường thực tế không "
                        "thẳng, và chúng càng ngày càng xa đường gạch đó.",
                "fact": "Mật độ 51,8%. Nước nhiều bạn hàng nhất chỉ gấp 1,8 "
                        "lần nước trung vị.",
            },
        ],
    },
    {
        "id": "cau-truc",
        "no": "2",
        "title": "Cấu trúc",
        "lead": "Thế giới chia thành mấy khối, và chia theo đường nào?",
        "charts": [
            {
                "file": "node_link_2023.html",
                "task": "T15",
                "title": "Ba khối địa lý",
                "look": "Rê chuột vào một nút để xem nước đó buôn bao nhiêu "
                        "và thuộc khối nào. Việt Nam là nút viền đen.",
                "fact": "Cả 10/10 nước ASEAN rơi vào cùng một khối 41 nước do "
                        "Trung Quốc dẫn đầu. Không có khối ASEAN riêng.",
            },
            {
                "file": "adjacency_2023.html",
                "task": "T16",
                "title": "Cùng dữ liệu, đổi thứ tự hàng cột",
                "look": "Hai ma trận chứa ĐÚNG cùng 416 luồng. Bản trái sắp "
                        "theo tên nước, bản phải sắp theo cụm. So hai bên để "
                        "thấy cấu trúc nằm ở thứ tự chứ không ở dữ liệu.",
                "fact": "Mật độ trong khối 12,9% so với ngoài khối 4,1% — đặc "
                        "gấp 3,1 lần.",
            },
        ],
    },
    {
        "id": "viet-nam",
        "no": "3",
        "title": "Vị trí Việt Nam",
        "lead": "Việt Nam bán cái gì, bán cho ai, và đứng ở đâu trong khối đó?",
        "charts": [
            {
                "file": "treemap_vnm_2023.html",
                "task": "T12",
                "title": "Việt Nam bán cái gì, 2023",
                "look": "Bấm vào một ngành để xem 97 nhóm hàng bên trong. "
                        "Bấm vào ô tiêu đề để quay ra.",
                "fact": "Điện tử 29,9% — ngành lớn nhất. Năm 1995 ngành này "
                        "chỉ chiếm 0,6%.",
            },
            {
                "file": "treemap_vnm_1995.html",
                "task": "T12",
                "title": "…và năm 1995, để so",
                "look": "Cùng bảng màu, cùng cách đọc. Nhìn mảng xanh lá "
                        "(nông sản) và mảng nâu (khoáng sản) chiếm bao nhiêu.",
                "fact": "Nông sản 42,9%, khoáng sản 20,6%. Hai ngành này cộng "
                        "lại là hơn nửa kim ngạch.",
            },
            {
                "file": "sunburst_vnm_2023.html",
                "task": "T13",
                "title": "Cùng dữ liệu, bố cục xuyên tâm",
                "look": "So với treemap ở trên: sunburst cho thấy quan hệ "
                        "cha–con rõ hơn, nhưng so diện tích thì khó hơn vì "
                        "mắt người đọc góc kém hơn đọc chiều dài.",
                "fact": "Cùng một cây, hai cách lấp đầy không gian — đây là "
                        "nội dung mục 9.1 của giáo trình.",
            },
            {
                "file": "small_multiples_vnm-tha-mys-idn_2023.html",
                "task": "T14",
                "title": "So với ba nước ASEAN cùng cỡ",
                "look": "Mỗi ô lưới tự chuẩn hóa về 100% nên so được CƠ CẤU. "
                        "Quy mô tuyệt đối ghi dưới tên nước.",
                "fact": "Việt Nam là nước duy nhất còn dựa mạnh vào dệt may "
                        "và giày dép: 18,4%, gấp 2,3 lần Indonesia.",
            },
            {
                "file": "chord_2023.html",
                "task": "T17",
                "title": "Việt Nam bán cho khối nào",
                "look": "Dải đậm là dải có Việt Nam. Rê chuột vào một dải để "
                        "xem giá trị hai chiều.",
                "fact": "63,9% hàng Việt Nam bán ra đi về Đông Á và Bắc Mỹ. "
                        "Đông Nam Á chỉ nhận 7,8%.",
            },
        ],
    },
    {
        "id": "y-nghia",
        "no": "4",
        "title": "Ý nghĩa",
        "lead": "Vị trí đó được tạo nên bởi cái gì, và nó bền đến đâu?",
        "charts": [
            {
                "file": "streamgraph_vnm_ty_trong.html",
                "task": "T21",
                "title": "Cơ cấu chuyển dịch, 1995–2023",
                "look": "Nhìn dải xanh lá (nông sản) teo lại và dải xanh nhạt "
                        "(điện tử) phình ra từ khoảng 2010.",
                "fact": "Điện tử 0,6% → 29,9%. Nông sản 42,9% → 11,6%.",
            },
            {
                "file": "sankey_vnm_2023.html",
                "task": "T19",
                "title": "Nhập vào, xuất ra",
                "look": "So bề dày hai bên nút Việt Nam. Dải đậm là các nước "
                        "ASEAN.",
                "fact": "Nhập 332,1 tỷ, xuất 385,5 tỷ. Giá trị gia tăng trong "
                        "nước chỉ 13,9%.",
            },
            {
                "file": "time_multiples.html",
                "task": "T20",
                "title": "Tiền tăng, cửa giảm",
                "look": "Bám theo chấm viền đen qua bốn khung. Nó đi LÊN "
                        "(tiền) nhưng từ 2005 đi SANG TRÁI (số thị trường).",
                "fact": "Số thị trường: 98 → 200 (2005) → 166. Mất 34 thị "
                        "trường trong khi tiền tăng 11,7 lần.",
            },
        ],
    },
]

CSS = """
:root{
  --bg:#FCFCFB; --surface:#FFFFFF; --ink:#1A1A1A; --ink-2:#555555;
  --ink-3:#808080; --line:#E4E4E2; --accent:#1F3864;
  --maxw:1180px;
}
:root:not([data-theme="light"]){ }
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#15171A; --surface:#1D2024; --ink:#F2F2F0; --ink-2:#B4B4B0;
    --ink-3:#8A8A86; --line:#2E3238; --accent:#9FB8E6;
  }
}
:root[data-theme="dark"]{
  --bg:#15171A; --surface:#1D2024; --ink:#F2F2F0; --ink-2:#B4B4B0;
  --ink-3:#8A8A86; --line:#2E3238; --accent:#9FB8E6;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font-family:"Segoe UI",Arial,"DejaVu Sans",sans-serif;
  font-size:16px; line-height:1.62;
}
.wrap{max-width:var(--maxw); margin:0 auto; padding:0 16px}

header.hero{padding:72px 0 40px; border-bottom:1px solid var(--line)}
.kicker{font-size:12px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--ink-3); margin:0 0 14px}
h1{font-size:clamp(28px,4.6vw,46px); line-height:1.18; margin:0 0 18px;
  letter-spacing:-.016em; max-width:21ch}
.sub{font-size:clamp(16px,2vw,19px); color:var(--ink-2); max-width:64ch; margin:0}
.meta{margin-top:26px; font-size:13px; color:var(--ink-3)}

.answer{margin:34px 0 0; padding:20px 22px; background:var(--surface);
  border:1px solid var(--line); border-left:3px solid var(--accent);
  border-radius:3px}
.answer b{color:var(--ink)}

nav.toc{position:sticky; top:0; z-index:20; background:var(--bg);
  border-bottom:1px solid var(--line); padding:11px 0}
nav.toc ol{list-style:none; display:flex; flex-wrap:wrap; gap:6px;
  margin:0; padding:0}
nav.toc a{display:inline-block; padding:5px 12px; border-radius:999px;
  text-decoration:none; color:var(--ink-2); font-size:13.5px;
  border:1px solid transparent}
nav.toc a:hover{color:var(--ink); border-color:var(--line);
  background:var(--surface)}

section.act{padding:58px 0 10px; border-top:1px solid var(--line)}
section.act:first-of-type{border-top:none}
.actno{font-size:12px; letter-spacing:.14em; text-transform:uppercase;
  color:var(--ink-3)}
h2{font-size:clamp(22px,3vw,31px); margin:8px 0 10px; letter-spacing:-.012em}
.lead{color:var(--ink-2); max-width:62ch; margin:0 0 10px; font-size:17px}

figure.chart{margin:36px 0 0; background:var(--surface);
  border:1px solid var(--line); border-radius:4px; overflow:hidden}
.chead{padding:17px 20px 13px; border-bottom:1px solid var(--line)}
.chead h3{margin:0 0 5px; font-size:18px; letter-spacing:-.008em}
.tag{display:inline-block; font-size:11px; letter-spacing:.06em;
  color:var(--ink-3); border:1px solid var(--line); border-radius:3px;
  padding:1px 7px; margin-left:8px; vertical-align:2px}
.look{margin:0; font-size:14.5px; color:var(--ink-2)}
.look b{color:var(--ink)}
.frame{width:100%; border:0; display:block; background:#FFFFFF}
.fact{margin:0; padding:13px 20px; border-top:1px solid var(--line);
  font-size:14px; color:var(--ink-2); background:var(--bg)}
.fact strong{color:var(--ink)}

.legend{margin:30px 0 0; padding:18px 20px; background:var(--surface);
  border:1px solid var(--line); border-radius:4px}
.legend h3{margin:0 0 12px; font-size:14px; letter-spacing:.04em;
  text-transform:uppercase; color:var(--ink-3)}
.swatches{display:flex; flex-wrap:wrap; gap:7px 16px; margin:0; padding:0;
  list-style:none}
.swatches li{display:flex; align-items:center; gap:7px; font-size:13.5px;
  color:var(--ink-2)}
.sw{width:15px; height:15px; border-radius:3px; border:1px solid rgba(0,0,0,.18);
  flex:0 0 auto}

.caveat{margin:30px 0 0; padding:17px 20px; border:1px solid var(--line);
  border-left:3px solid var(--ink-3); border-radius:3px; background:var(--surface);
  font-size:14.5px; color:var(--ink-2)}
.caveat h3{margin:0 0 8px; font-size:14px; color:var(--ink);
  letter-spacing:.03em; text-transform:uppercase}
.caveat ul{margin:0; padding-left:19px}
.caveat li{margin:5px 0}

footer{margin-top:66px; padding:28px 0 56px; border-top:1px solid var(--line);
  font-size:13.5px; color:var(--ink-3)}
footer a{color:var(--ink-2)}

.themebtn{position:fixed; right:14px; bottom:14px; z-index:30;
  background:var(--surface); color:var(--ink-2); border:1px solid var(--line);
  border-radius:999px; padding:8px 15px; font-size:13px; cursor:pointer;
  font-family:inherit}
.themebtn:hover{color:var(--ink)}

@media (max-width:640px){
  header.hero{padding:44px 0 30px}
  section.act{padding:40px 0 6px}
  figure.chart{margin-top:26px}
}
"""

THEME_JS = """
(function(){
  var k='gecom-theme';
  try{ var s=localStorage.getItem(k); if(s){document.documentElement.dataset.theme=s;} }
  catch(e){}
  document.addEventListener('DOMContentLoaded',function(){
    var b=document.getElementById('themebtn');
    if(!b) return;
    b.addEventListener('click',function(){
      var cur=document.documentElement.dataset.theme;
      if(!cur){
        cur=window.matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';
      }
      var next=cur==='dark'?'light':'dark';
      document.documentElement.dataset.theme=next;
      try{ localStorage.setItem(k,next); }catch(e){}
    });
  });
})();
"""

# Chiều cao khung cho từng biểu đồ. Đặt tay vì mỗi hình một tỷ lệ: ma trận kề
# rất ngang, chord gần vuông. Để chung một chiều cao thì hình nào cũng hoặc bị
# bóp hoặc thừa khoảng trắng.
HEIGHTS = {
    "adjacency_2023.html": 620,
    "chord_2023.html": 880,
    "node_link_2023.html": 780,
    "sankey_vnm_2023.html": 700,
    "time_multiples.html": 760,
    "streamgraph_vnm_ty_trong.html": 660,
    "degree_dist_out.html": 640,
}
DEFAULT_HEIGHT = 680

# Favicon nhúng thẳng dưới dạng data URI: trang chạy được cả khi mở bằng
# file:// lẫn khi đẩy lên Pages, nên không nên phụ thuộc vào một file rời ở gốc
# web server. Ba ô vuông = ba khối trong hình node-link.
#
# Phải để RIÊNG ngoài chuỗi định dạng, không dán thẳng vào: data URI chứa %3C,
# %23, %2F... mà toán tử % của Python đọc những cái đó thành ký tự định dạng và
# ném ValueError ngay lúc dựng trang.
FAVICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E"
    "%3Crect width='16' height='16' fill='%23FCFCFB'/%3E"
    "%3Crect x='2' y='2' width='6' height='6' fill='%23CC6677'/%3E"
    "%3Crect x='9' y='4' width='5' height='5' fill='%2388CCEE'/%3E"
    "%3Crect x='4' y='9' width='5' height='5' fill='%23117733'/%3E"
    '%3C/svg%3E">'
)

# CSS tiêm vào từng file biểu đồ lúc chép sang web/charts/.
#
# Plotly ghi thẻ <div> của biểu đồ với height:100%, nhưng chiều cao theo phần
# trăm chỉ phân giải được khi MỌI thẻ tổ tiên cũng có chiều cao xác định. File
# .html mà Plotly sinh ra không đặt chiều cao cho <html> và <body>, nên 100%
# không tính ra được và biểu đồ rơi về chiều cao mặc định của nó — cao hơn
# iframe, sinh ra thanh cuộn lồng trong thanh cuộn của trang.
#
# Sửa ở đây chứ không sửa trong script vẽ, vì đây là yêu cầu của việc ĐÓNG GÓI
# web, không phải của biểu đồ: file trong output/ mở riêng vẫn phải bình thường.
FIT_CSS = ("<style>html,body{height:100%;margin:0;padding:0;"
           "overflow:hidden;background:#FFFFFF}</style>")


def fit_to_frame(src, dst):
    """Chép một file biểu đồ sang web/charts/ kèm CSS cho vừa khung iframe."""
    with open(src, encoding="utf-8") as fh:
        page = fh.read()
    if FIT_CSS not in page:
        if "</head>" in page:
            page = page.replace("</head>", FIT_CSS + "</head>", 1)
        else:
            # Plotly có chế độ xuất không kèm <head>. Khi đó dán lên đầu file —
            # trình duyệt vẫn áp dụng, và không im lặng bỏ qua phần sửa này.
            page = FIT_CSS + page
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(page)


def log(msg):
    print(msg)
    sys.stdout.flush()


def esc(s):
    return html.escape(s, quote=True)


def build_legend():
    items = []
    for sid in sorted(R.SECTOR_PALETTE):
        items.append(
            '<li><span class="sw" style="background:%s"></span>%s</li>'
            % (R.SECTOR_PALETTE[sid], esc(R.SECTOR_NAME_VI[sid])))
    return ('<div class="legend"><h3>Bảng màu 10 ngành cấp 1 HS92 — '
            'dùng chung trên mọi biểu đồ</h3><ul class="swatches">%s</ul></div>'
            % "".join(items))


def build_section(sec, available):
    figs = []
    for c in sec["charts"]:
        if c["file"] not in available:
            log("  ! thiếu %s — bỏ qua mục này" % c["file"])
            continue
        h = HEIGHTS.get(c["file"], DEFAULT_HEIGHT)
        figs.append(
            '<figure class="chart">'
            '<div class="chead"><h3>%s<span class="tag">%s</span></h3>'
            '<p class="look">%s</p></div>'
            '<iframe class="frame" src="charts/%s" height="%d" '
            'loading="lazy" title="%s"></iframe>'
            '<p class="fact"><strong>Con số:</strong> %s</p>'
            '</figure>'
            % (esc(c["title"]), esc(c["task"]), esc(c["look"]),
               esc(c["file"]), h, esc(c["title"]), esc(c["fact"])))
    if not figs:
        return ""
    return ('<section class="act" id="%s"><div class="wrap">'
            '<div class="actno">Hồi %s</div><h2>%s</h2>'
            '<p class="lead">%s</p>%s</div></section>'
            % (esc(sec["id"]), esc(sec["no"]), esc(sec["title"]),
               esc(sec["lead"]), "".join(figs)))


def build_html(available):
    toc = "".join(
        '<li><a href="#%s">%s. %s</a></li>' % (esc(s["id"]), esc(s["no"]),
                                               esc(s["title"]))
        for s in SECTIONS)
    body = "".join(build_section(s, available) for s in SECTIONS)

    caveat = (
        '<div class="caveat"><h3>Năm giới hạn chúng tôi tự nói ra</h3><ul>'
        '<li><b>Không có nguồn độc lập để kiểm chéo.</b> Atlas đã hòa giải số '
        'liệu hai chiều trước khi phát hành — 2.093/2.093 luồng lớn có hai bản '
        'khai trùng khít. Bộ dữ liệu này không cho phép tự đo sai số của nó.</li>'
        '<li><b>Sankey không truy vết được lô hàng.</b> Hai bên nút Việt Nam là '
        'hai phép đo riêng đặt cạnh nhau, không phải một dòng chảy liên tục.</li>'
        '<li><b>Betweenness của Việt Nam bằng 0 và đồng hạng với 57 nước khác</b> '
        '— nên con số thứ hạng không đọc được.</li>'
        '<li><b>Cây sản phẩm chỉ vẽ tới tầng 2</b> (10 ngành, 97 nhóm), đúng '
        'phạm vi đã chốt. Tính toàn vẹn cả 4 tầng vẫn được kiểm riêng.</li>'
        '<li><b>Năm mốc là 2023, không phải 2024.</b> Bản 2024 còn tạm, thiếu '
        '1.781 cặp nước — riêng Việt Nam mất 37 bạn hàng.</li>'
        '</ul></div>')

    return """<!doctype html>
<html lang="vi" data-palette="%s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vị trí Việt Nam trong mạng lưới thương mại toàn cầu</title>
<meta name="description" content="Phân tích mạng lưới thương mại thế giới 2023 từ dữ liệu Atlas of Economic Complexity, tập trung vào vị trí của Việt Nam.">
%s
<style>%s</style>
<script>%s</script>
</head>
<body>
<header class="hero"><div class="wrap">
  <p class="kicker">Đồ án Trực quan hóa dữ liệu</p>
  <h1>Việt Nam đứng ở đâu trong mạng lưới thương mại toàn cầu?</h1>
  <p class="sub">231 quốc gia · 27.535 luồng xuất khẩu · 21,66 nghìn tỷ USD,
     năm 2023. Dữ liệu từ Atlas of Economic Complexity (Harvard Growth Lab),
     phân loại HS92.</p>
  <div class="answer"><b>Câu trả lời ngắn:</b> Việt Nam đã leo rất nhanh —
     kim ngạch tăng 75 lần từ 1995, ECI từ hạng 181/211 lên 78/230. Nhưng leo
     bằng cách trở thành công xưởng lắp ráp cho một khối do Trung Quốc dẫn
     đầu: nhập 86 xu hàng ngoại cho mỗi đồng bán ra, và từ 2005 đến nay bán
     nhiều tiền hơn qua <b>ít cửa hơn</b> — mất 34 thị trường.</div>
  <p class="meta">Mọi con số trên trang này do script trong <code>src/</code>
     sinh ra và in ra để kiểm lại được. Biểu đồ tương tác: rê chuột để xem giá
     trị, bấm vào ô treemap và sunburst để xem sâu hơn.</p>
</div></header>

<nav class="toc"><div class="wrap"><ol>%s</ol></div></nav>

%s

<section class="act"><div class="wrap">%s%s</div></section>

<footer><div class="wrap">
  Nguồn dữ liệu: <a href="https://atlas.hks.harvard.edu/">The Atlas of Economic
  Complexity</a>, Harvard Growth Lab, phân loại HS92, năm mốc 2023.
  Trang dựng bằng <code>python src/build_web.py</code> từ các biểu đồ trong
  <code>output/</code>.
</div></footer>

<button class="themebtn" id="themebtn" type="button">Đổi nền sáng/tối</button>
</body>
</html>
""" % (",".join(R.SECTOR_PALETTE[s] for s in sorted(R.SECTOR_PALETTE)),
       FAVICON, CSS, THEME_JS, toc, body, build_legend(), caveat)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--open", action="store_true", dest="do_open",
                    help="mở trang bằng trình duyệt sau khi dựng")
    args = ap.parse_args()

    if not os.path.isdir(OUTDIR):
        sys.exit("Chưa có thư mục output/. Chạy các script vẽ trước — xem README.")

    wanted = [c["file"] for s in SECTIONS for c in s["charts"]]
    have = set(os.listdir(OUTDIR))
    missing = [f for f in wanted if f not in have]

    os.makedirs(CHARTS, exist_ok=True)
    copied = 0
    for f in wanted:
        src = os.path.join(OUTDIR, f)
        if os.path.exists(src):
            fit_to_frame(src, os.path.join(CHARTS, f))
            copied += 1

    available = set(os.listdir(CHARTS))
    page = os.path.join(WEB, "index.html")
    with open(page, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(build_html(available))

    log("Dựng trang web:")
    log("  chép %d/%d biểu đồ vào %s" % (copied, len(wanted), CHARTS))
    if missing:
        log("")
        log("  ! THIẾU %d biểu đồ — trang vẫn dựng được nhưng khuyết mục:"
            % len(missing))
        for f in missing:
            log("      %s" % f)
        log("    Chạy lại script vẽ tương ứng rồi dựng lại.")
    log("")
    log("  -> %s" % page)
    log("")
    log("Mở bằng cách bấm đúp vào file, hoặc chạy một server tĩnh:")
    log("    python -m http.server --directory web 8000")
    log("Đẩy lên GitHub Pages: Settings > Pages, chọn nhánh và thư mục /web.")

    if args.do_open:
        webbrowser.open("file:///" + page.replace("\\", "/"))


if __name__ == "__main__":
    main()

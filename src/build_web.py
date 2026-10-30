# -*- coding: utf-8 -*-
"""Dựng trang web demo — 23 biểu đồ tương tác theo năm nhịp của §E.

Vì sao trang này là một script, không phải một file HTML viết tay
-----------------------------------------------------------------
Trang web là chỗ thứ ba in các con số của đồ án, sau báo cáo cuối và slide. Ba
chỗ mà gõ tay thì sớm muộn sẽ nói ba câu khác nhau. Nên trang này **không đo gì
riêng**: nó gọi đúng ``build_slides.do_so()`` — hàm đã đo mọi con số cho slide và
đã được đối chiếu với báo cáo cuối qua bảng ``KY_VONG`` — rồi điền vào ô
``{khoá}`` như slide. Phần chữ bên dưới không chứa một con số nào gõ tay; phép
kiểm số 5 bắt lỗi đó.

Vì sao trang TĨNH
-----------------
GitHub Pages phục vụ file tĩnh, không có server để sập giữa buổi thuyết trình.
Biểu đồ vẫn tương tác đủ vì mỗi file Plotly đã mang sẵn dữ liệu của nó.

Vì sao mỗi biểu đồ nằm trong iframe có KHUNG CỐ ĐỊNH rồi mới thu phóng
-------------------------------------------------------------------
Các script vẽ đặt lề, vị trí tiêu đề và phụ đề theo **point của khung PNG**
(quyết định B16): rộng 454 pt, cao theo từng hình. Để Plotly tự giãn theo khung
khác tỷ lệ thì tiêu đề đè lên vùng vẽ. Nên iframe giữ đúng khung gốc — bề ngang
454, chiều cao suy từ tỷ lệ của chính file PNG — rồi được phóng bằng CSS
``transform`` cho vừa cột. Plotly vẽ bằng SVG nên phóng lên vẫn nét, và tooltip
vẫn đúng chỗ.

Chạy
----
    PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/build_web.py

Cần ``output/`` đã có đủ hình (xem README, khối chạy biểu đồ) và
``output/bao-cao-cuoi.html`` + ``output/slide-thuyet-trinh.html``. Ra thư mục
``site/`` — thư mục này **được commit**, vì Pages phục vụ thẳng từ repo còn dữ
liệu thô thì không có trên máy của GitHub. ``site/`` chỉ chứa HTML biểu đồ và
ảnh, không chứa dữ liệu thô (Nguyên tắc #5).
"""

from __future__ import print_function

import argparse
import html
import io
import os
import re
import shutil
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import reference_data as R                      # noqa: E402
import build_slides as BS                       # noqa: E402

OUT = "output"
SITE = "site"
ASSETS_SRC = os.path.join("src", "web")
REPO_URL = "https://github.com/Dr-Vphuc/global-ecom"

# Khung gốc của mọi hình: bề ngang FIG_WIDTH_FULL tính bằng point (B16).
KHUNG_W = R.khung_pt(R.FIG_WIDTH_FULL)

# Hai file không phải biểu đồ trong output/ — đi vào trang dưới dạng tài liệu.
TAI_LIEU = ("bao-cao-cuoi", "slide-thuyet-trinh")


# ------------------------------------------------------------------ nội dung
# Mỗi hình: một hoặc hai chiều lựa chọn (ví dụ "Năm", "Cách xếp"); ``tep`` ánh
# xạ tổ hợp lựa chọn → tên file trong output/. Tổ hợp không có file thì nút đó
# bị khoá chứ không biến mất, để người xem biết nó không tồn tại chứ không phải
# bị quên.

HINH = {
    "dong_chay": dict(
        viec="T21", lenh="src/make_streamgraph.py",
        nhan="Cơ cấu xuất khẩu theo mười ngành",
        dan="Hình dưới cho thấy cuộc đổi chỗ ấy diễn ra qua từng năm. Tầng trên là "
            "kim ngạch, tầng dưới là cùng dữ liệu quy về tỷ trọng, vì đặt chung một "
            "thang thì cơ cấu những năm đầu mỏng tới mức không đọc được.",
        doc="Rê chuột lên một dải để xem kim ngạch và tỷ trọng của ngành đó trong "
            "từng năm.",
        chieu=[], tep={(): "stream_sectors_1995_2023"}),
    "cay": dict(
        viec="T12, T13", lenh="src/make_hierarchy_charts.py --year {nam}",
        nhan="Rổ hàng của Việt Nam ở hai đầu giai đoạn",
        dan="Thử chuyển qua lại giữa {nam_dau} và {nam}. Dệt may lùi lại nhưng vẫn là "
            "một trụ cột ({det_may_dau} rồi {det_may_cuoi}), còn nông sản thì nhường "
            "phần lớn tỷ trọng cho điện tử.",
        doc="Treemap giúp so độ lớn nhanh; sunburst cho thấy mỗi ngành chia ra những "
            "nhóm hàng nào. Bấm vào một ô để đi sâu, bấm lại để quay ra.",
        chieu=[("Cách vẽ", [("treemap", "Treemap"), ("sunburst", "Sunburst")]),
               ("Năm", [("{nam}", "{nam}"), ("{nam_dau}", "{nam_dau}")])],
        tep={("treemap", "{nam}"): "treemap_vnm_{nam}",
             ("treemap", "{nam_dau}"): "treemap_vnm_{nam_dau}",
             ("sunburst", "{nam}"): "sunburst_vnm_{nam}",
             ("sunburst", "{nam_dau}"): "sunburst_vnm_{nam_dau}"}),
    "luoi_asean": dict(
        viec="T14", lenh="src/make_small_multiples.py",
        nhan="Việt Nam đặt cạnh Thái Lan, Malaysia và Indonesia",
        dan="Đặt cạnh ba nền kinh tế cùng khu vực, rổ hàng của Việt Nam giống "
            "Malaysia ở phần điện tử, nhưng dựa vào dệt may và giày dép nhiều hơn hẳn.",
        doc="Mỗi ô tự quy về tỷ trọng nên so được cơ cấu, không so được độ lớn; kim "
            "ngạch của từng nước ghi ngay dưới tên. Việt Nam viền đậm.",
        chieu=[], tep={(): "small_multiples_vnm-tha-mys-idn_{nam}"}),
    "dva_nganh": dict(
        viec="A19", lenh="src/make_dva_sector.py",
        nhan="Phần giá trị ở lại trong nước, theo ngành",
        dan="Hình dưới đặt chín ngành hàng cạnh nhau, xếp từ hàng khó nhất xuống "
            "hàng dễ nhất. Thanh càng dài thì càng nhiều giá trị của hàng xuất khẩu "
            "được làm ra trong nước.",
        doc="Vạch đứt là mức bình quân của cả rổ hàng, {dva_rb}. Vạch mảnh trên mỗi "
            "thanh là khoảng giữa hai cách ghép sang ngành của OECD; máy móc chỉ "
            "dao động từ {dva_may_lo} đến {dva_may_hi}, nên chênh với điện tử nằm "
            "trong sai số. Hai cột bên phải là phần giữ lại và PCI.",
        chieu=[], tep={(): "dva_sectors_{tiva_nam}"}),
    "bac": dict(
        viec="T09", lenh="src/make_degree_loglog.py --year {nam}",
        nhan="Phân bố bậc của mạng xuất khẩu",
        dan="Trước hết, mạng lưới này có xoay quanh vài trung tâm lớn, như Internet, "
            "hay không? Nếu có, phân bố bậc vẽ trên thang log-log sẽ gần như một "
            "đường thẳng.",
        doc="Các điểm không nằm trên đường thẳng, tức không có vài nước làm trung tâm "
            "cho cả mạng. Ô bên phải so phân bố thật với một phân bố đều.",
        chieu=[("Năm", [("{nam}", "{nam}"), ("{nam_dau}", "{nam_dau}")])],
        tep={("{nam}",): "degree_loglog_{nam}",
             ("{nam_dau}",): "degree_loglog_{nam_dau}"}),
    "mang": dict(
        viec="T15, T16, T17", lenh="src/make_node_link.py · "
                                   "src/make_adjacency_matrix.py · src/make_chord.py",
        nhan="Cùng một mạng đã lọc, ba cách vẽ",
        dan="Ba cách vẽ dưới đây dùng chung một tập luồng đã lọc. Mỗi cách trả lời "
            "tốt một câu hỏi khác nhau, nên chúng tôi giữ cả ba.",
        doc="Node-link cho thấy ai nối với ai. Ma trận cho thấy các cụm mà không có "
            "đường nào đè lên nhau. Chord cho thấy kim ngạch chia giữa các khối ra "
            "sao. Thử đổi ma trận từ xếp A→Z sang xếp theo cụm: vẫn là những ô ấy, "
            "nhưng các khối chỉ hiện ra khi thứ tự đúng.",
        chieu=[("Cách vẽ", [("node", "Node-link"), ("cum", "Ma trận theo cụm"),
                            ("abc", "Ma trận A→Z"), ("chord", "Chord theo khối")]),
               ("Năm", [("{nam}", "{nam}"), ("{nam_dau}", "{nam_dau}")])],
        tep={("node", "{nam}"): "node_link_{nam}",
             ("cum", "{nam}"): "adjacency_cluster_{nam}",
             ("cum", "{nam_dau}"): "adjacency_cluster_{nam_dau}",
             ("abc", "{nam}"): "adjacency_alpha_{nam}",
             ("abc", "{nam_dau}"): "adjacency_alpha_{nam_dau}",
             ("chord", "{nam}"): "chord_bloc_{nam}",
             ("chord", "{nam_dau}"): "chord_bloc_{nam_dau}"}),
    "sankey": dict(
        viec="T19", lenh="src/make_sankey.py --year {nam}",
        nhan="Việt Nam mua của ai, bán cho ai",
        dan="Khi không có trung tâm chung, điều quyết định vị trí của một nước là nó "
            "nằm ở đâu trong các dòng hàng. Với Việt Nam, đó là một hành lang rõ ràng: "
            "năm {nam}, Việt Nam nhập khẩu từ Trung Quốc **{mua_chn} tỷ USD** và xuất "
            "khẩu sang Hoa Kỳ **{ban_usa} tỷ USD**; {vung_mua_pct} hàng nhập đến từ {vung_mua}. Hình "
            "dưới đi theo dòng hàng: bên trái là nơi mua vào, bên phải là nơi bán ra.",
        doc="Phần nhạt trên cột Việt Nam là chênh lệch giữa xuất và nhập. Đó là một "
            "phép trừ, không phải phần giá trị tạo ra trong nước. Chuyển sang "
            "{nam_dau} để thấy hai đầu hành lang khi ấy là những nước khác.",
        chieu=[("Năm", [("{nam}", "{nam}"), ("{nam_dau}", "{nam_dau}")])],
        tep={("{nam}",): "sankey_vietnam_{nam}",
             ("{nam_dau}",): "sankey_vietnam_{nam_dau}"}),
    "ban_cho_ai": dict(
        viec="T20", lenh="src/make_time_multiples.py --direction xuat|nhap",
        nhan="Bạn hàng lớn nhất qua bốn năm mốc",
        dan="Thị trường xuất khẩu cũng ngày càng tập trung. Ba thị trường lớn nhất nhận {top3_cuoi} kim "
            "ngạch xuất khẩu năm {nam}, tăng từ mức {top3_day} năm {nam_day}. Đếm số "
            "bạn hàng thì lại thấy Việt Nam có vẻ mất bớt đối tác, nhưng những nước "
            "rời đi chỉ mang theo một phần rất nhỏ kim ngạch, nên điều đáng nhìn là "
            "tiền dồn về đâu.",
        doc="Mỗi ô là một năm mốc, mỗi thanh là tỷ trọng của một bạn hàng. Nhìn độ "
            "dài vài thanh đầu để thấy mức tập trung; chuyển sang nhập khẩu để thấy "
            "đầu vào còn dồn hơn.",
        chieu=[("Chiều", [("xuat", "Xuất khẩu"), ("nhap", "Nhập khẩu")])],
        tep={("xuat",): "time_multiples_xuat", ("nhap",): "time_multiples_nhap"}),
    "mat_phang": dict(
        viec="T31", lenh="src/make_decision_plane.py",
        nhan="Mọi nhóm hàng trên cùng một mặt phẳng RCA × PCI",
        dan="Đặt tất cả nhóm hàng lên một mặt phẳng thì thấy ngay kim ngạch đang dồn "
            "về góc nào.",
        doc="Trục ngang là RCA (thang log, vạch đứt là mức trung bình thế giới), trục "
            "dọc là PCI. Mỗi vòng tròn là một nhóm hàng, to nhỏ theo kim ngạch. Góc "
            "trên bên trái là hàng khó mà Việt Nam chưa bán mạnh, chỗ đáng đầu tư nhất.",
        chieu=[], tep={(): "decision_plane_{nam}"}),
    "chay_lai": dict(
        viec="T31", lenh="src/make_decision_plane.py --year 2015 --since 2007",
        nhan="Cùng một quy tắc, chạy ở những năm chưa biết tương lai",
        dan="Chọn một năm để xem quy tắc đã chọn gì vào lúc đó, rồi so với vị trí của "
            "nhóm hàng ấy hôm nay.",
        doc="Mỗi lần chạy, quy tắc chỉ dùng RCA, PCI và kim ngạch của chính năm đó. "
            "Đường kẻ nối từ vòng tròn rỗng cho thấy nhóm được chọn đã dịch chuyển từ "
            "đâu tới.",
        chieu=[("Chạy ở", [("2007", "2007"), ("2015", "2015"), ("{nam}", "{nam}")])],
        tep={("2007",): "decision_plane_2007", ("2015",): "decision_plane_2015",
             ("{nam}",): "decision_plane_{nam}"}),
}

# Năm phần — đúng mạch năm nhịp của §E và của slide (B18): bốn phần dựng bằng
# chứng, phần năm nói việc nên làm. Giọng văn theo lối báo chí dữ liệu: mỗi phần
# mở bằng một khẳng định, mỗi con số đi kèm một mốc để so, lời cảnh báo lồng vào
# câu bằng chữ "nhưng" thay vì tách thành hộp riêng.
NHIP = [
    dict(ma="1", id="ro-hang", nav="Rổ hàng", ke="Quy mô",
         tieu_de="Rổ hàng được xây lại gần như từ đầu",
         doan=["Năm {nam_dau}, Việt Nam xuất khẩu {vn_dau}. Năm {nam}, con số là "
               "{vn_cuoi}, gấp **{vn_lan} lần**. Cùng khoảng thời gian, thương mại "
               "thế giới chỉ lớn lên {tg_lan} lần, nên Việt Nam đi nhanh hơn mặt "
               "bằng chung khoảng {nhanh_hon} lần và leo từ hạng {hang_dau} lên hạng "
               "{hang_cuoi}.",
               "Thứ đem đi bán cũng gần như thay hết. Nông sản từng chiếm "
               "{nong_san_dau} rổ hàng, nay còn {nong_san_cuoi}. Điện tử đi theo "
               "chiều ngược lại, từ {dien_tu_dau} lên **{dien_tu_cuoi}**, và trở "
               "thành nhóm hàng lớn nhất."],
         so=[("{vn_lan}×", "kim ngạch xuất khẩu, {nam_dau} → {nam}"),
             ("{hang_cuoi}", "hạng xuất khẩu thế giới, từ {hang_dau}"),
             ("{asean_cuoi}", "hạng trong ASEAN, từ {asean_dau}")],
         hinh=["dong_chay", "cay"]),
    dict(ma="2", id="nang-luc", nav="Năng lực", ke="Năng lực",
         tieu_de="Việt Nam tiến bộ thật về năng lực, nhưng phần giá trị ở lại nhỏ dần",
         doan=["Bán được nhiều chưa chắc đã làm giỏi hơn. Để đo năng lực, giới nghiên "
               "cứu dùng chỉ số phức tạp kinh tế (ECI): một nước càng làm được nhiều "
               "mặt hàng, và càng nhiều mặt hàng ít nước khác làm được, thì điểm càng "
               "cao. Theo thước đo này, Việt Nam đi từ hạng {eci_dau} lên hạng "
               "**{eci_cuoi}**.",
               "Nhưng ECI tính trên kim ngạch xuất khẩu gộp. Một chiếc điện thoại lắp "
               "ráp ở Việt Nam được tính trọn độ phức tạp của nó, dù phần giá trị làm "
               "ra trong nước có thể nhỏ (D2, D5). Bộ số TiVA của OECD đo đúng phần "
               "đó, và kết quả không dễ chịu: trên toàn nền kinh tế, phần giá trị của "
               "hàng xuất khẩu làm ra trong nước đã tụt từ {dva_tong_dau} năm "
               "{nam_dau} xuống **{dva_tong_cuoi}** năm {tiva_nam}; riêng điện tử từ "
               "{dva_dien_dau} xuống **{dva_dien_cuoi}**.",
               "Hàng càng khó thì phần ở lại càng thấp, nhưng chỉ ở mức vừa (hệ số "
               "Spearman {dva_rho}). Bốn ngành khó nhất, chiếm {dva_top4_ty_trong} "
               "kim ngạch ghép được, đều giữ lại {dva_top4_lo} đến {dva_top4_hi}. "
               "Đừng đọc thành \"Việt Nam chỉ lắp ráp\": gần nửa giá trị hàng điện "
               "tử vẫn làm ra trong nước. Và đây là giá trị tạo ra trong lãnh thổ, "
               "chưa nói được lợi nhuận về tay ai (A19)."],
         so=[("{eci_cuoi}", "hạng ECI năm {nam}, từ {eci_dau}"),
             ("{dva_tong_dau} → {dva_tong_cuoi}", "phần giá trị ở lại của hàng xuất "
                                                  "khẩu, {nam_dau} → {tiva_nam}"),
             ("{dva_dien_dau} → {dva_dien_cuoi}", "riêng ngành điện tử, cùng "
                                                  "khoảng thời gian"),
             ("{dva_rho}", "tương quan giữa độ khó (PCI) và phần ở lại")],
         hinh=["luoi_asean", "dva_nganh"]),
    dict(ma="3", id="hanh-lang", nav="Hành lang", ke="Cấu trúc",
         tieu_de="Nhưng Việt Nam lớn lên qua một hành lang hẹp ở cả hai đầu",
         doan=["Mạng thương mại toàn cầu rất dày. Năm {nam}, {nut} nước nối với nhau "
               "bằng {canh} luồng xuất khẩu, và trong hơn một nửa số cặp nước có thể "
               "có, hai bên đều buôn bán trực tiếp với nhau (mật độ {mat_do}).",
               "Để nhìn ra cấu trúc, chúng tôi chỉ giữ những luồng lớn: {nguong_canh} "
               "số luồng, nhưng vẫn giữ {nguong_gia_tri} kim ngạch và đủ mười nước "
               "ASEAN. Cán cân thương mại thì đo trên toàn bộ dữ liệu, vì bỏ các luồng "
               "nhỏ đi sẽ làm cán cân đổi dấu (A15)."],
         so=[("{vung_mua_pct}", "hàng nhập khẩu đến từ {vung_mua}"),
             ("{top3_cuoi}", "kim ngạch đi vào ba thị trường lớn nhất, từ {top3_day} "
                             "năm {nam_day}"),
             ("{hhi_lan}×", "đầu vào tập trung hơn đầu ra, theo chỉ số HHI")],
         hinh=["bac", "mang", "sankey", "ban_cho_ai"]),
    dict(ma="4", id="loi-the", nav="Lợi thế", ke="Lợi thế",
         tieu_de="Và lợi thế lớn nhất vẫn nằm ở những mặt hàng dễ làm",
         doan=["Hai chỉ số giúp tách bạch chuyện này. RCA cho biết một nước bán một "
               "mặt hàng đậm tới mức nào so với trung bình thế giới; lớn hơn một nghĩa "
               "là có lợi thế. PCI cho biết mặt hàng đó khó làm tới đâu.",
               "Giày dép có RCA {rca_giay}, rất cao, nhưng PCI {pci_giay}. Cà phê cũng "
               "vậy: RCA {rca_ca_phe}, PCI {pci_ca_phe}. Tính chung, **{goc_kep_pct}** "
               "kim ngạch xuất khẩu nằm ở nhóm bán mạnh nhưng dễ làm.",
               "Nhóm máy điện và thiết bị điện là trường hợp khác: hàng khó, chiếm "
               "{ty_trong_dien} rổ hàng, nhưng RCA chỉ {rca_dien}. Tức là Việt Nam lớn "
               "ở nhóm này gần đúng theo mức nó lớn trong thương mại thế giới, chứ "
               "chưa vượt trội như ở giày dép."],
         so=[("{goc_kep_pct}", "kim ngạch ở nhóm bán mạnh nhưng dễ làm "
                               "({goc_kep_n} nhóm hàng)"),
             ("{rca_giay}", "RCA của giày dép; PCI chỉ {pci_giay}")],
         hinh=["mat_phang"]),
    dict(ma="5", id="de-xuat", nav="Đề xuất", ke="Đề xuất",
         tieu_de="Nên dồn sức vào hai nhóm hàng khó đang sát ngưỡng lợi thế",
         doan=["Chúng tôi không chọn bằng cảm giác. Điều kiện được viết thành một quy "
               "tắc cố định: kim ngạch trên {min_xuat}, PCI dương, RCA từ {rca_lo} đến "
               "dưới {rca_hi} và đang tăng. Trong các nhóm thoả điều kiện, lấy hai "
               "nhóm khó nhất. Năm {nam}, quy tắc chọn ra **{chay_nay_0}** và "
               "**{chay_nay_1}**.",
               "Để xem quy tắc có đáng tin không, chúng tôi cho nó chạy trên dữ liệu "
               "quá khứ, khi chưa ai biết chuyện gì sẽ xảy ra. Chạy ở năm 2007, nó "
               "chọn {chay2007_0_ten}, lúc nhóm này mới xuất {chay2007_0_xuat} tỷ USD "
               "với RCA {chay2007_0_rca}. Đến {nam}, nhóm đó xuất "
               "{chay2007_0_xuat_nay} tỷ USD và RCA đã lên {chay2007_0_rca_nay}.",
               "Nhưng không nên tin quá mức. Trong {nen_n} nhóm hàng, chỉ {nen_tang} "
               "tự tăng RCA; phần lớn sức dự báo đến từ điều kiện PCI dương "
               "({nen_kho_tang} số nhóm hàng khó tăng RCA, so với {nen_de_tang} ở "
               "nhóm hàng dễ). Số nhóm thoả trọn quy tắc cũng chỉ có {nen_tron_n}, "
               "quá ít để kết luận về mặt thống kê (A17).",
               "Còn một điều cần nói thẳng: đề xuất này không dựa vào việc hai nhóm "
               "ấy giữ nhiều giá trị hơn điện tử. Máy móc giữ {dva_may}, điện tử "
               "{dva_dien}, và cả hai thấp hơn mức bình quân {dva_rb}. Lý do chọn là "
               "độ khó của hàng và mức tập trung; phần ở lại là một mốc phải theo "
               "dõi, và nếu nó tiếp tục tụt trong khi RCA vượt ngưỡng thì chúng tôi "
               "nhận đề xuất là chưa đủ."],
         so=[("{rca_quang}", "RCA hiện tại của {chay_nay_0}; mốc cần vượt là mức "
                             "trung bình thế giới"),
             ("{rca_may}", "RCA hiện tại của {chay_nay_1}; cùng mốc ấy")],
         hinh=["chay_lai"]),
]

HAN_CHE = [
    ("Hàng đi qua, chưa hẳn làm ra ở đây", "RCA, PCI và ECI đều tính trên kim ngạch "
     "xuất khẩu gộp (D2, D5). Phần giá trị làm ra trong nước chỉ đo được bằng TiVA "
     "của OECD, ở cấp ngành chứ chưa tới HS4 hay doanh nghiệp, và qua bảng ghép "
     "HS2 sang ISIC nên còn sai số (A19)."),
    ("Một nguồn dữ liệu, không tự kiểm được", "Mỗi luồng hàng được hai nước khai "
     "báo, nhưng trong dữ liệu hai con số này trùng khít nhau, nên chúng tôi không "
     "tự đo được sai số. Ai đã làm chúng khớp nhau thì dữ liệu không cho biết. Atlas, BACI "
     "và Comtrade cũng chung một gốc, không phải ba nguồn độc lập (A18, B9)."),
    ("Mới dừng ở cấp HS2", "Phân tích dùng {nen_n} nhóm hàng. Chi tiết hơn, ở cấp "
     "HS4, có trong Atlas nhưng chưa được tải, nên nhóm điện tử ở đây gộp cả chip "
     "lẫn dây điện (D4)."),
    ("Lấy năm {nam}, không phải năm mới nhất", "Số liệu năm sau đó vẫn là bản tạm và "
     "còn thiếu nhiều cặp nước, nên mọi con số tính cho một năm đều dùng năm {nam} "
     "(A6, B1)."),
]


# ------------------------------------------------------------------ dựng trang

def dien(s, S, thieu):
    return BS.dien(s, S, thieu)


def md(s, S, thieu):
    """Điền khoá rồi đổi markdown trong dòng sang HTML (cùng luật với slide)."""
    return BS.inline(dien(s, S, thieu))


def khung_hinh(ten):
    """(rộng, cao) của khung gốc, suy từ tỷ lệ của chính file PNG."""
    with open(os.path.join(OUT, ten + ".png"), "rb") as f:
        f.read(16)
        w, h = struct.unpack(">II", f.read(8))
    return KHUNG_W, int(round(KHUNG_W * float(h) / w))


ICON_MO = ('<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" '
           'focusable="false"><path d="M9 2h5v5M14 2L7.5 8.5M12 9.5V14H2V4h4.5" '
           'fill="none" stroke="currentColor" stroke-width="1.5" '
           'stroke-linecap="square"/></svg>')


def mot_hinh(ma_hinh, so_thu_tu, S, thieu, dung):
    h = HINH[ma_hinh]
    tep = {tuple(dien(k, S, thieu) for k in khoa): dien(v, S, thieu)
           for khoa, v in h["tep"].items()}
    chieu = [(ten, [(dien(k, S, thieu), dien(n, S, thieu)) for k, n in lua])
             for ten, lua in h["chieu"]]
    mac_dinh = tuple(lua[0][0] for _, lua in chieu)
    ten0 = tep[mac_dinh]
    w, hh = khung_hinh(ten0)
    for v in tep.values():
        dung.add(v)

    bien = []
    for v in sorted(set(tep.values())):
        vw, vh = khung_hinh(v)
        bien.append('"%s":[%d,%d]' % (v, vw, vh))
    bang = ",".join('"%s":"%s"' % ("|".join(k), v) for k, v in sorted(tep.items()))

    dieu_khien = []
    for i, (ten, lua) in enumerate(chieu):
        nut = []
        for k, n in lua:
            nut.append('<button type="button" class="seg__btn" data-dim="%d" '
                       'data-val="%s" aria-pressed="%s">%s</button>'
                       % (i, html.escape(k), "true" if k == mac_dinh[i] else "false",
                          html.escape(n)))
        dieu_khien.append(
            '<div class="seg" role="group" aria-label="%s"><span class="seg__label">'
            '%s</span>%s</div>' % (html.escape(ten), html.escape(ten), "".join(nut)))

    id_hinh = "hinh-%s" % ma_hinh.replace("_", "-")
    return (
        '<p class="fig__lede">{dan}</p>\n'
        '<figure class="fig" id="{id}" data-map=\'{{{bang}}}\' data-size=\'{{{bien}}}\'>\n'
        '  <figcaption class="fig__head">\n'
        '    <span class="fig__no">Hình {so}</span>\n'
        '    <span class="fig__title">{nhan}</span>\n'
        '    <span class="fig__task">{viec}</span>\n'
        '  </figcaption>\n'
        '  {dk}\n'
        '  <div class="fig__frame" style="--w:{w};--h:{h}">\n'
        '    <iframe data-src="charts/{t}.html" title="{nhan}" loading="lazy" '
        'scrolling="no" width="{w}" height="{h}"></iframe>\n'
        '    <p class="fig__loading" aria-hidden="true">Đang tải biểu đồ…</p>\n'
        '  </div>\n'
        '  <div class="fig__foot">\n'
        '    <p class="fig__read"><span class="fig__key">Cách đọc</span>{doc}</p>\n'
        '    <p class="fig__meta"><code>python {lenh}</code>'
        '<a class="fig__open" href="charts/{t}.html" target="_blank" rel="noopener">'
        'Mở riêng{icon}<span class="sr-only"> (mở trong thẻ mới)</span></a></p>\n'
        '  </div>\n'
        '</figure>'
    ).format(id=id_hinh, bang=bang, bien=",".join(bien), so=so_thu_tu,
             nhan=html.escape(dien(h["nhan"], S, thieu)),
             viec=html.escape(h["viec"]),
             dk="\n  ".join(dieu_khien) if dieu_khien else "",
             w=w, h=hh, t=ten0, doc=md(h["doc"], S, thieu),
             dan=md(h["dan"], S, thieu),
             lenh=html.escape(dien(h["lenh"], S, thieu)), icon=ICON_MO)


def mot_nhip(n, so_hinh, S, thieu, dung):
    so = "".join(
        '<div class="stat"><dt class="stat__label">%s</dt><dd class="stat__value">'
        '%s</dd></div>' % (md(nhan, S, thieu), md(gt, S, thieu))
        for gt, nhan in n["so"])
    doan = "".join("<p>%s</p>" % md(p, S, thieu) for p in n["doan"])
    hinh = []
    for ma in n["hinh"]:
        so_hinh[0] += 1
        hinh.append(mot_hinh(ma, so_hinh[0], S, thieu, dung))
    return (
        '<section class="beat" id="{id}" aria-labelledby="{id}-h">\n'
        '  <header class="beat__head">\n'
        '    <p class="beat__kicker"><span class="beat__no">{ma}</span>'
        '<span><span class="sr-only">Phần {ma}: </span>{ke}</span></p>\n'
        '    <h2 class="beat__title" id="{id}-h">{td}</h2>\n'
        '  </header>\n'
        '  <div class="beat__body">\n'
        '    <div class="beat__text">{doan}</div>\n'
        '    <dl class="beat__stats">{so}</dl>\n'
        '  </div>\n'
        '  {hinh}\n'
        '</section>'
    ).format(id=n["id"], ma=n["ma"], ke=html.escape(n["ke"]),
             td=md(n["tieu_de"], S, thieu), doan=doan, so=so,
             hinh="\n  ".join(hinh))


def dung_trang(S, thieu, dung):
    so_hinh = [0]
    nhip = "\n".join(mot_nhip(n, so_hinh, S, thieu, dung) for n in NHIP)
    nav = "".join('<li><a href="#%s" data-nav="%s"><span class="nav__no">%s</span>'
                  '%s</a></li>' % (n["id"], n["id"], n["ma"], html.escape(n["nav"]))
                  for n in NHIP)
    han_che = "".join('<li><h3>%s</h3><p>%s</p></li>'
                      % (md(t, S, thieu), md(p, S, thieu)) for t, p in HAN_CHE)
    thay = {
        "nav": nav, "nhip": nhip, "han_che": han_che, "repo": REPO_URL,
        "so_hinh": str(so_hinh[0]),
        "hero_tieu_de": md("Việt Nam đã lớn lên {vn_lan} lần. Câu hỏi là lớn lên "
                           "bằng cách nào.", S, thieu),
        "hero_dan": md("Năm {nam}, thương mại hàng hóa toàn cầu có {nut} nước tham "
                       "gia, {canh} luồng xuất khẩu, tổng cộng {tg_cuoi}. Chúng tôi "
                       "dựng mạng lưới đó từ dữ liệu của Đại học Harvard để xem Việt "
                       "Nam đứng ở đâu, đang dựa vào ai, và nên dồn sức vào nhóm hàng "
                       "nào tiếp theo.", S, thieu),
        "hero_so": "".join(
            '<div class="stat stat--hero"><dt class="stat__label">%s</dt>'
            '<dd class="stat__value">%s</dd></div>' % (md(nh, S, thieu), md(gt, S, thieu))
            for gt, nh in (("{vn_lan}×", "kim ngạch xuất khẩu, {nam_dau} → {nam}"),
                           ("{hang_cuoi}", "hạng xuất khẩu thế giới năm {nam}"),
                           ("{top3_cuoi}", "kim ngạch đi vào ba thị trường lớn nhất"),
                           ("{goc_kep_pct}", "kim ngạch ở nhóm bán mạnh nhưng dễ làm"))),
        "meta": md("Atlas of Economic Complexity · Harvard Growth Lab · HS92 · "
                   "{nam_dau}–{nam}", S, thieu),
        # Chú giải màu dựng từ đúng bảng mà mọi script vẽ dùng — không chép hex.
        "chu_giai": "".join(
            '<li><span class="swatch" style="background:%s"></span>%s</li>'
            % (R.SECTOR_PALETTE[k], html.escape(R.SECTOR_NAME_VI[k]))
            for k in sorted(R.SECTOR_PALETTE)),
        "nam": S["nam"],
    }
    mau = io.open(os.path.join(ASSETS_SRC, "index.template.html"),
                  encoding="utf-8").read()
    return re.sub(r"\[\[([a-z_]+)\]\]", lambda m: thay[m.group(1)], mau)


# ------------------------------------------------------------------ chép file

# Biểu đồ Plotly ghi ra với chiều cao 100% của body; trong iframe thì body phải
# không lề và cao đúng khung, nếu không hình lệch 8 px và hiện thanh cuộn.
CHEN = ('<style>html,body{margin:0;padding:0;height:100%;overflow:hidden;'
        'background:#fff}</style>')


def chep_bieu_do(dung):
    d = os.path.join(SITE, "charts")
    os.makedirs(d)
    for ten in sorted(dung):
        s = io.open(os.path.join(OUT, ten + ".html"), encoding="utf-8").read()
        if "<head>" not in s:
            raise SystemExit("output/%s.html không có <head>" % ten)
        s = s.replace("<head>", "<head>" + CHEN, 1)
        io.open(os.path.join(d, ten + ".html"), "w", encoding="utf-8",
                newline="\n").write(s)


def chep_tai_lieu():
    """Báo cáo cuối và slide, kèm đúng những PNG mà hai file đó trỏ tới."""
    d = os.path.join(SITE, "tai-lieu")
    os.makedirs(d)
    anh = set()
    for ten in TAI_LIEU:
        p = os.path.join(OUT, ten + ".html")
        s = io.open(p, encoding="utf-8").read()
        anh.update(re.findall(r'<img[^>]*src="([^"/:]+\.png)"', s))
        shutil.copyfile(p, os.path.join(d, ten + ".html"))
    for a in sorted(anh):
        shutil.copyfile(os.path.join(OUT, a), os.path.join(d, a))
    return anh


# ------------------------------------------------------------------ kiểm chứng

# Mã định danh được phép chứa chữ số trong phần chữ: A16, D2, T19, HS92, B12...
MA_DINH_DANH = re.compile(r"\b(?:[A-Z]{1,3}\d+|20\d\d)\b")


def so_go_tay():
    """Chữ số nằm ngoài ô {khoá} và ngoài mã định danh = con số gõ tay.

    Năm dạng 20xx chỉ được phép ở các lần chạy lại quy tắc (2007, 2015), vì đó là
    tham số của phép thử chứ không phải số đo. Năm tham chiếu và năm đầu thì phải
    đi qua {nam} / {nam_dau}.
    """
    chu = []
    for n in NHIP:
        chu += [n["tieu_de"]] + n["doan"] + [x for cap in n["so"] for x in cap]
    for h in HINH.values():
        chu += [h["nhan"], h["dan"], h["doc"]]
    for t, p in HAN_CHE:
        chu += [t, p]
    loi = []
    for s in chu:
        tran = MA_DINH_DANH.sub("", BS.O_TRONG.sub("", s))
        if re.search(r"\d", tran):
            loi.append(s[:70])
    return loi


def kiem_chung(S, thieu, dung, anh):
    loi = 0
    print("\n" + "=" * 72)
    print("KIỂM CHỨNG — trang web demo")
    print("=" * 72)

    print("\n  1. Ô {khoá} chưa giải được: %d" % len(thieu))
    for k in sorted(thieu):
        print("     THIẾU  {%s}" % k)
    loi += len(thieu)

    co = sorted(os.path.splitext(f)[0] for f in os.listdir(OUT)
                if f.endswith(".html") and os.path.splitext(f)[0] not in TAI_LIEU)
    mat = sorted(v for v in dung if not os.path.exists(os.path.join(OUT, v + ".html")))
    bo_sot = [v for v in co if v not in dung]
    print("\n  2. Biểu đồ trên trang: %d · thiếu file: %d · có trong output/ mà "
          "không dùng: %d" % (len(dung), len(mat), len(bo_sot)))
    for v in mat:
        print("     THIẾU  output/%s.html" % v)
    for v in bo_sot:
        print("     BỎ SÓT output/%s.html" % v)
    loi += len(mat) + len(bo_sot)

    lech = [(k, v, S.get(k)) for k, v in sorted(BS.KY_VONG.items()) if S.get(k) != v]
    print("\n  3. Đối chiếu với báo cáo cuối: %d/%d khớp"
          % (len(BS.KY_VONG) - len(lech), len(BS.KY_VONG)))
    for k, cho, co_ in lech:
        print("     LỆCH  %-22s báo cáo %-12s web %s" % (k, cho, co_))
    loi += len(lech)

    nhip = [n["ma"] for n in NHIP]
    print("\n  4. Mạch năm nhịp: %s" % " → ".join(nhip))
    loi += 0 if nhip == ["1", "2", "3", "4", "5"] else 1

    tay = so_go_tay()
    print("\n  5. Con số gõ tay trong phần chữ: %d" % len(tay))
    for s in tay:
        print("     GÕ TAY  %s…" % s)
    loi += len(tay)

    tl = [os.path.join(SITE, "tai-lieu", t + ".html") for t in TAI_LIEU]
    thieu_anh = [a for a in anh if not os.path.exists(os.path.join(SITE, "tai-lieu", a))]
    print("\n  6. Tài liệu kèm: %d file · %d ảnh, thiếu %d"
          % (sum(os.path.exists(p) for p in tl), len(anh), len(thieu_anh)))
    loi += len(thieu_anh) + sum(not os.path.exists(p) for p in tl)

    tong = 0
    for goc, _, files in os.walk(SITE):
        tong += sum(os.path.getsize(os.path.join(goc, f)) for f in files)
    print("\n  7. Dung lượng site/: %s MB" % R.fmt_vn(tong / 1048576.0, 1))
    if tong > 50 * 1048576:
        print("     QUÁ LỚN — GitHub Pages khuyên dưới 1 GB, repo nhóm thì càng nhỏ càng tốt")
        loi += 1

    print("\n  %s" % ("ĐẠT — 7 phép kiểm, không lỗi" if not loi
                      else "KHÔNG ĐẠT — %d lỗi" % loi))
    print("=" * 72)
    return loi


def main():
    argparse.ArgumentParser(description=__doc__.split("\n")[0]).parse_args()
    print("Đo lại số qua build_slides.do_so() ...")
    S = BS.do_so()
    thieu, dung = set(), set()
    trang = dung_trang(S, thieu, dung)

    # Dọn bên trong chứ không xoá chính thư mục: trên Windows, một server xem
    # thử đang đứng trong site/ sẽ khoá thư mục đó.
    # site/bi/ là dashboard, do build_bi.py dựng riêng — không đụng tới.
    if os.path.isdir(SITE):
        for f in os.listdir(SITE):
            if f == "bi":
                continue
            p = os.path.join(SITE, f)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(os.path.join(SITE, "assets"))
    io.open(os.path.join(SITE, "index.html"), "w", encoding="utf-8",
            newline="\n").write(trang)
    for f in ("site.css", "site.js"):
        shutil.copyfile(os.path.join(ASSETS_SRC, f), os.path.join(SITE, "assets", f))
    # Pages mặc định chạy Jekyll, và Jekyll bỏ qua file/thư mục bắt đầu bằng "_".
    io.open(os.path.join(SITE, ".nojekyll"), "w").close()
    chep_bieu_do(dung)
    anh = chep_tai_lieu()
    print("  %s/index.html · %d biểu đồ · %d ảnh tài liệu"
          % (SITE, len(dung), len(anh)))
    return 1 if kiem_chung(S, thieu, dung, anh) else 0


if __name__ == "__main__":
    sys.exit(main())

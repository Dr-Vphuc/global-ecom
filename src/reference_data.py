# -*- coding: utf-8 -*-
"""Bảng tra cứu dùng chung cho toàn bộ pipeline.

Chứa:
  - COUNTRY_VI : ISO3 -> (tên tiếng Việt, vùng, châu lục)
  - ASEAN_ISO3 : danh sách mã nước ASEAN
  - FOCUS_ISO3 : nước được tô đậm trong biểu đồ (cột is_focus của nodes.csv)
  - NON_COUNTRY : các mã KHÔNG phải quốc gia thật
  - SECTOR_PALETTE        : bảng màu 10 ngành cấp 1 HS92 (T04, đã kiểm định)
  - SECTOR_TEXT_ON_FILL   : màu chữ đặt đè lên từng ô màu đó
  - FONT_STACK, FONT_SIZES, FIG_* : font và kích thước hình chuẩn (T04)
  - SEQUENTIAL_SCALE      : thang màu tuần tự cho ma trận kề / bản đồ nhiệt
  - HIGHLIGHT_*           : cách làm nổi Việt Nam (viền + độ dày, không dùng màu)

Vùng và châu lục theo phân loại UN M49.
Chỉ dùng thư viện chuẩn — không cần cài gì để chạy.
"""

# ---------------------------------------------------------------------------
# Các mã KHÔNG phải quốc gia thật.
# KHÔNG loại bỏ tự động: loại chúng sẽ làm đổi con số 230 nút / 25.425 cạnh
# mà nhóm đã đo và sẽ phải bảo vệ. Quyết định giữ hay bỏ thuộc về T10.
# ---------------------------------------------------------------------------
NON_COUNTRY = {"USP", "ANS"}

# Lãnh thổ không có dân cư thường trú — thường chỉ xuất hiện vài luồng rất nhỏ.
UNINHABITED = {"ATA", "BVT", "HMD", "SGS", "ATF"}

ASEAN_ISO3 = ["BRN", "KHM", "IDN", "LAO", "MYS", "MMR", "PHL", "SGP", "THA", "VNM"]

# Nước được tô đậm trong biểu đồ. Đã chốt: cả khối ASEAN, vì đề tài có
# lát cắt Việt Nam – ASEAN. Muốn quay về chỉ mình Việt Nam thì đổi thành {"VNM"}.
FOCUS_ISO3 = set(ASEAN_ISO3)

# Đối tác ngoài khối đáng so sánh trong phần diễn giải.
MAJOR_PARTNERS = ["CHN", "USA", "JPN", "KOR", "DEU", "IND", "HKG", "TWN"]


# ---------------------------------------------------------------------------
# ISO3 -> (tên tiếng Việt, vùng M49, châu lục)
# ---------------------------------------------------------------------------
COUNTRY_VI = {
    # ----- Đông Nam Á -----
    "BRN": ("Brunei", "South-East Asia", "Asia"),
    "KHM": ("Campuchia", "South-East Asia", "Asia"),
    "IDN": ("Indonesia", "South-East Asia", "Asia"),
    "LAO": ("Lào", "South-East Asia", "Asia"),
    "MYS": ("Malaysia", "South-East Asia", "Asia"),
    "MMR": ("Myanmar", "South-East Asia", "Asia"),
    "PHL": ("Philippines", "South-East Asia", "Asia"),
    "SGP": ("Singapore", "South-East Asia", "Asia"),
    "THA": ("Thái Lan", "South-East Asia", "Asia"),
    "VNM": ("Việt Nam", "South-East Asia", "Asia"),
    "TLS": ("Đông Timor", "South-East Asia", "Asia"),
    # ----- Đông Á -----
    "CHN": ("Trung Quốc", "East Asia", "Asia"),
    "HKG": ("Hồng Kông", "East Asia", "Asia"),
    "JPN": ("Nhật Bản", "East Asia", "Asia"),
    "KOR": ("Hàn Quốc", "East Asia", "Asia"),
    "PRK": ("Triều Tiên", "East Asia", "Asia"),
    "MAC": ("Ma Cao", "East Asia", "Asia"),
    "MNG": ("Mông Cổ", "East Asia", "Asia"),
    "TWN": ("Đài Loan", "East Asia", "Asia"),
    # ----- Nam Á -----
    "AFG": ("Afghanistan", "South Asia", "Asia"),
    "BGD": ("Bangladesh", "South Asia", "Asia"),
    "BTN": ("Bhutan", "South Asia", "Asia"),
    "IND": ("Ấn Độ", "South Asia", "Asia"),
    "IRN": ("Iran", "South Asia", "Asia"),
    "MDV": ("Maldives", "South Asia", "Asia"),
    "NPL": ("Nepal", "South Asia", "Asia"),
    "PAK": ("Pakistan", "South Asia", "Asia"),
    "LKA": ("Sri Lanka", "South Asia", "Asia"),
    # ----- Trung Á -----
    "KAZ": ("Kazakhstan", "Central Asia", "Asia"),
    "KGZ": ("Kyrgyzstan", "Central Asia", "Asia"),
    "TJK": ("Tajikistan", "Central Asia", "Asia"),
    "TKM": ("Turkmenistan", "Central Asia", "Asia"),
    "UZB": ("Uzbekistan", "Central Asia", "Asia"),
    # ----- Tây Á -----
    "ARM": ("Armenia", "West Asia", "Asia"),
    "AZE": ("Azerbaijan", "West Asia", "Asia"),
    "BHR": ("Bahrain", "West Asia", "Asia"),
    "CYP": ("Síp", "West Asia", "Asia"),
    "GEO": ("Gruzia", "West Asia", "Asia"),
    "IRQ": ("Iraq", "West Asia", "Asia"),
    "ISR": ("Israel", "West Asia", "Asia"),
    "JOR": ("Jordan", "West Asia", "Asia"),
    "KWT": ("Kuwait", "West Asia", "Asia"),
    "LBN": ("Liban", "West Asia", "Asia"),
    "OMN": ("Oman", "West Asia", "Asia"),
    "PSE": ("Palestine", "West Asia", "Asia"),
    "QAT": ("Qatar", "West Asia", "Asia"),
    "SAU": ("Ả Rập Xê Út", "West Asia", "Asia"),
    "SYR": ("Syria", "West Asia", "Asia"),
    "TUR": ("Thổ Nhĩ Kỳ", "West Asia", "Asia"),
    "ARE": ("Các Tiểu vương quốc Ả Rập Thống nhất", "West Asia", "Asia"),
    "YEM": ("Yemen", "West Asia", "Asia"),
    # ----- Bắc Âu -----
    "DNK": ("Đan Mạch", "Northern Europe", "Europe"),
    "EST": ("Estonia", "Northern Europe", "Europe"),
    "FIN": ("Phần Lan", "Northern Europe", "Europe"),
    "FRO": ("Quần đảo Faroe", "Northern Europe", "Europe"),
    "ISL": ("Iceland", "Northern Europe", "Europe"),
    "IRL": ("Ireland", "Northern Europe", "Europe"),
    "LVA": ("Latvia", "Northern Europe", "Europe"),
    "LTU": ("Litva", "Northern Europe", "Europe"),
    "NOR": ("Na Uy", "Northern Europe", "Europe"),
    "SWE": ("Thụy Điển", "Northern Europe", "Europe"),
    "GBR": ("Vương quốc Anh", "Northern Europe", "Europe"),
    # ----- Tây Âu -----
    "AUT": ("Áo", "Western Europe", "Europe"),
    "BEL": ("Bỉ", "Western Europe", "Europe"),
    "FRA": ("Pháp", "Western Europe", "Europe"),
    "DEU": ("Đức", "Western Europe", "Europe"),
    "LUX": ("Luxembourg", "Western Europe", "Europe"),
    "NLD": ("Hà Lan", "Western Europe", "Europe"),
    "CHE": ("Thụy Sĩ", "Western Europe", "Europe"),
    # ----- Nam Âu -----
    "ALB": ("Albania", "Southern Europe", "Europe"),
    "AND": ("Andorra", "Southern Europe", "Europe"),
    "BIH": ("Bosnia và Herzegovina", "Southern Europe", "Europe"),
    "HRV": ("Croatia", "Southern Europe", "Europe"),
    "GIB": ("Gibraltar", "Southern Europe", "Europe"),
    "GRC": ("Hy Lạp", "Southern Europe", "Europe"),
    "VAT": ("Vatican", "Southern Europe", "Europe"),
    "ITA": ("Ý", "Southern Europe", "Europe"),
    "MLT": ("Malta", "Southern Europe", "Europe"),
    "MNE": ("Montenegro", "Southern Europe", "Europe"),
    "MKD": ("Bắc Macedonia", "Southern Europe", "Europe"),
    "PRT": ("Bồ Đào Nha", "Southern Europe", "Europe"),
    "SMR": ("San Marino", "Southern Europe", "Europe"),
    "SRB": ("Serbia", "Southern Europe", "Europe"),
    "SVN": ("Slovenia", "Southern Europe", "Europe"),
    "ESP": ("Tây Ban Nha", "Southern Europe", "Europe"),
    # ----- Đông Âu -----
    "BLR": ("Belarus", "Eastern Europe", "Europe"),
    "BGR": ("Bulgaria", "Eastern Europe", "Europe"),
    "CZE": ("Séc", "Eastern Europe", "Europe"),
    "HUN": ("Hungary", "Eastern Europe", "Europe"),
    "POL": ("Ba Lan", "Eastern Europe", "Europe"),
    "MDA": ("Moldova", "Eastern Europe", "Europe"),
    "ROU": ("Romania", "Eastern Europe", "Europe"),
    "RUS": ("Nga", "Eastern Europe", "Europe"),
    "SVK": ("Slovakia", "Eastern Europe", "Europe"),
    "UKR": ("Ukraine", "Eastern Europe", "Europe"),
    # ----- Bắc Phi -----
    "DZA": ("Algeria", "Northern Africa", "Africa"),
    "EGY": ("Ai Cập", "Northern Africa", "Africa"),
    "LBY": ("Libya", "Northern Africa", "Africa"),
    "MAR": ("Maroc", "Northern Africa", "Africa"),
    "SDN": ("Sudan", "Northern Africa", "Africa"),
    "TUN": ("Tunisia", "Northern Africa", "Africa"),
    # ----- Tây Phi -----
    "BEN": ("Benin", "Western Africa", "Africa"),
    "BFA": ("Burkina Faso", "Western Africa", "Africa"),
    "CPV": ("Cabo Verde", "Western Africa", "Africa"),
    "CIV": ("Bờ Biển Ngà", "Western Africa", "Africa"),
    "GMB": ("Gambia", "Western Africa", "Africa"),
    "GHA": ("Ghana", "Western Africa", "Africa"),
    "GIN": ("Guinea", "Western Africa", "Africa"),
    "GNB": ("Guinea-Bissau", "Western Africa", "Africa"),
    "LBR": ("Liberia", "Western Africa", "Africa"),
    "MLI": ("Mali", "Western Africa", "Africa"),
    "MRT": ("Mauritanie", "Western Africa", "Africa"),
    "NER": ("Niger", "Western Africa", "Africa"),
    "NGA": ("Nigeria", "Western Africa", "Africa"),
    "SEN": ("Senegal", "Western Africa", "Africa"),
    "SLE": ("Sierra Leone", "Western Africa", "Africa"),
    "SHN": ("Saint Helena", "Western Africa", "Africa"),
    "TGO": ("Togo", "Western Africa", "Africa"),
    # ----- Trung Phi -----
    "AGO": ("Angola", "Middle Africa", "Africa"),
    "CMR": ("Cameroon", "Middle Africa", "Africa"),
    "CAF": ("Cộng hòa Trung Phi", "Middle Africa", "Africa"),
    "TCD": ("Tchad", "Middle Africa", "Africa"),
    "COG": ("Congo", "Middle Africa", "Africa"),
    "COD": ("CHDC Congo", "Middle Africa", "Africa"),
    "GNQ": ("Guinea Xích Đạo", "Middle Africa", "Africa"),
    "GAB": ("Gabon", "Middle Africa", "Africa"),
    "STP": ("São Tomé và Príncipe", "Middle Africa", "Africa"),
    # ----- Đông Phi -----
    "BDI": ("Burundi", "Eastern Africa", "Africa"),
    "COM": ("Comoros", "Eastern Africa", "Africa"),
    "DJI": ("Djibouti", "Eastern Africa", "Africa"),
    "ERI": ("Eritrea", "Eastern Africa", "Africa"),
    "ETH": ("Ethiopia", "Eastern Africa", "Africa"),
    "KEN": ("Kenya", "Eastern Africa", "Africa"),
    "MDG": ("Madagascar", "Eastern Africa", "Africa"),
    "MWI": ("Malawi", "Eastern Africa", "Africa"),
    "MUS": ("Mauritius", "Eastern Africa", "Africa"),
    "MOZ": ("Mozambique", "Eastern Africa", "Africa"),
    "RWA": ("Rwanda", "Eastern Africa", "Africa"),
    "SYC": ("Seychelles", "Eastern Africa", "Africa"),
    "SOM": ("Somalia", "Eastern Africa", "Africa"),
    "SSD": ("Nam Sudan", "Eastern Africa", "Africa"),
    "TZA": ("Tanzania", "Eastern Africa", "Africa"),
    "UGA": ("Uganda", "Eastern Africa", "Africa"),
    "ZMB": ("Zambia", "Eastern Africa", "Africa"),
    "ZWE": ("Zimbabwe", "Eastern Africa", "Africa"),
    # ----- Nam Phi -----
    "BWA": ("Botswana", "Southern Africa", "Africa"),
    "SWZ": ("Eswatini", "Southern Africa", "Africa"),
    "LSO": ("Lesotho", "Southern Africa", "Africa"),
    "NAM": ("Namibia", "Southern Africa", "Africa"),
    "ZAF": ("Nam Phi", "Southern Africa", "Africa"),
    # ----- Bắc Mỹ -----
    "BMU": ("Bermuda", "Northern America", "Americas"),
    "CAN": ("Canada", "Northern America", "Americas"),
    "GRL": ("Greenland", "Northern America", "Americas"),
    "SPM": ("Saint-Pierre và Miquelon", "Northern America", "Americas"),
    "USA": ("Hoa Kỳ", "Northern America", "Americas"),
    # ----- Trung Mỹ -----
    "BLZ": ("Belize", "Central America", "Americas"),
    "CRI": ("Costa Rica", "Central America", "Americas"),
    "SLV": ("El Salvador", "Central America", "Americas"),
    "GTM": ("Guatemala", "Central America", "Americas"),
    "HND": ("Honduras", "Central America", "Americas"),
    "MEX": ("Mexico", "Central America", "Americas"),
    "NIC": ("Nicaragua", "Central America", "Americas"),
    "PAN": ("Panama", "Central America", "Americas"),
    # ----- Caribe -----
    "AIA": ("Anguilla", "Caribbean", "Americas"),
    "ATG": ("Antigua và Barbuda", "Caribbean", "Americas"),
    "ABW": ("Aruba", "Caribbean", "Americas"),
    "BHS": ("Bahamas", "Caribbean", "Americas"),
    "BRB": ("Barbados", "Caribbean", "Americas"),
    "BES": ("Bonaire", "Caribbean", "Americas"),
    "VGB": ("Quần đảo Virgin thuộc Anh", "Caribbean", "Americas"),
    "CYM": ("Quần đảo Cayman", "Caribbean", "Americas"),
    "CUB": ("Cuba", "Caribbean", "Americas"),
    "CUW": ("Curaçao", "Caribbean", "Americas"),
    "DMA": ("Dominica", "Caribbean", "Americas"),
    "DOM": ("Cộng hòa Dominica", "Caribbean", "Americas"),
    "GRD": ("Grenada", "Caribbean", "Americas"),
    "HTI": ("Haiti", "Caribbean", "Americas"),
    "JAM": ("Jamaica", "Caribbean", "Americas"),
    "MSR": ("Montserrat", "Caribbean", "Americas"),
    "ANT": ("Antilles thuộc Hà Lan", "Caribbean", "Americas"),
    "BLM": ("Saint-Barthélemy", "Caribbean", "Americas"),
    "KNA": ("Saint Kitts và Nevis", "Caribbean", "Americas"),
    "LCA": ("Saint Lucia", "Caribbean", "Americas"),
    "VCT": ("Saint Vincent và Grenadines", "Caribbean", "Americas"),
    "SXM": ("Sint Maarten", "Caribbean", "Americas"),
    "TTO": ("Trinidad và Tobago", "Caribbean", "Americas"),
    "TCA": ("Quần đảo Turks và Caicos", "Caribbean", "Americas"),
    # ----- Nam Mỹ -----
    "ARG": ("Argentina", "South America", "Americas"),
    "BOL": ("Bolivia", "South America", "Americas"),
    "BRA": ("Brazil", "South America", "Americas"),
    "CHL": ("Chile", "South America", "Americas"),
    "COL": ("Colombia", "South America", "Americas"),
    "ECU": ("Ecuador", "South America", "Americas"),
    "FLK": ("Quần đảo Falkland", "South America", "Americas"),
    "GUY": ("Guyana", "South America", "Americas"),
    "PRY": ("Paraguay", "South America", "Americas"),
    "PER": ("Peru", "South America", "Americas"),
    "SUR": ("Suriname", "South America", "Americas"),
    "URY": ("Uruguay", "South America", "Americas"),
    "VEN": ("Venezuela", "South America", "Americas"),
    # ----- Úc và New Zealand -----
    "AUS": ("Úc", "Australia and New Zealand", "Oceania"),
    "NZL": ("New Zealand", "Australia and New Zealand", "Oceania"),
    "NFK": ("Đảo Norfolk", "Australia and New Zealand", "Oceania"),
    "CXR": ("Đảo Christmas", "Australia and New Zealand", "Oceania"),
    "CCK": ("Quần đảo Cocos", "Australia and New Zealand", "Oceania"),
    # ----- Melanesia -----
    "FJI": ("Fiji", "Melanesia", "Oceania"),
    "NCL": ("Nouvelle-Calédonie", "Melanesia", "Oceania"),
    "PNG": ("Papua New Guinea", "Melanesia", "Oceania"),
    "SLB": ("Quần đảo Solomon", "Melanesia", "Oceania"),
    "VUT": ("Vanuatu", "Melanesia", "Oceania"),
    # ----- Micronesia -----
    "GUM": ("Guam", "Micronesia", "Oceania"),
    "KIR": ("Kiribati", "Micronesia", "Oceania"),
    "MHL": ("Quần đảo Marshall", "Micronesia", "Oceania"),
    "FSM": ("Micronesia", "Micronesia", "Oceania"),
    "NRU": ("Nauru", "Micronesia", "Oceania"),
    "MNP": ("Quần đảo Bắc Mariana", "Micronesia", "Oceania"),
    "PLW": ("Palau", "Micronesia", "Oceania"),
    # ----- Polynesia -----
    "ASM": ("Samoa thuộc Mỹ", "Polynesia", "Oceania"),
    "COK": ("Quần đảo Cook", "Polynesia", "Oceania"),
    "PYF": ("Polynesia thuộc Pháp", "Polynesia", "Oceania"),
    "NIU": ("Niue", "Polynesia", "Oceania"),
    "PCN": ("Pitcairn", "Polynesia", "Oceania"),
    "WSM": ("Samoa", "Polynesia", "Oceania"),
    "TKL": ("Tokelau", "Polynesia", "Oceania"),
    "TON": ("Tonga", "Polynesia", "Oceania"),
    "TUV": ("Tuvalu", "Polynesia", "Oceania"),
    # ----- Vùng cực / không dân cư -----
    "ATA": ("Nam Cực", "Antarctica", "Antarctica"),
    "BVT": ("Đảo Bouvet", "Antarctica", "Antarctica"),
    "HMD": ("Đảo Heard và McDonald", "Antarctica", "Antarctica"),
    "SGS": ("Nam Georgia và Quần đảo Nam Sandwich", "Antarctica", "Antarctica"),
    "ATF": ("Vùng đất phía Nam thuộc Pháp", "Antarctica", "Antarctica"),
    # ----- Không phải quốc gia -----
    "USP": ("Đối tác dịch vụ không xác định", "Other", "Other"),
    "ANS": ("Quốc gia không khai báo", "Other", "Other"),
}


# ---------------------------------------------------------------------------
# Bảng màu 10 ngành cấp 1 HS92 — ĐÃ CHỐT ở T04.
#
# Kiểm định bằng `python src/check_palette.py`, không phải bằng mắt. Chi tiết
# và lý do từng lựa chọn nằm ở docs/style-guide.md.
#
# Đo được, ΔE2000 của cặp gần nhau nhất trong 45 cặp:
#
#     mắt thường 16,1  ·  protan 13,3  ·  deutan 12,3  ·  tritan 11,6
#
# Bảng Tableau 10 dùng tạm trước đó KHÔNG đạt: với người mù màu lục (deutan,
# dạng phổ biến nhất) thì Nông sản #59A14F và Phương tiện vận tải #E15759 đều
# hiện ra thành cùng một màu bùn — ΔE = 0,7, tức là không phân biệt nổi. Hai
# nhóm này nằm cạnh nhau trong mọi treemap của đồ án.
#
# Nền của bảng mới: thang "muted" của Paul Tol (9 màu, thiết kế sẵn cho mù
# màu), đổi ô Khoáng sản sang nâu đậm #5D4037 cho hợp nghĩa và để đẩy ΔE mắt
# thường từ 15,0 lên 16,1. Ô "Khác" dùng xám nhạt để tự chìm xuống.
#
# ⚠️ Bảng này để TÔ MẢNG (treemap, sunburst, ruy-băng chord, nền nút). Bốn màu
# nhạt — Đá, Máy móc, Điện tử, Khác — có tương phản với nền trắng dưới 3:1 nên
# mảng phải có viền trắng 1px. Đừng vẽ đường mảnh 1px bằng các màu này.
# ---------------------------------------------------------------------------
SECTOR_PALETTE = {
    1:  "#CC6677",   # Textiles — Dệt may, giày dép, nội thất
    2:  "#117733",   # Agriculture — Nông sản, động vật, gỗ, giấy
    3:  "#DDCC77",   # Stone — Đá, thủy tinh, gốm sứ
    4:  "#5D4037",   # Minerals — Khoáng sản, nhiên liệu, quặng, muối
    5:  "#332288",   # Metals — Kim loại
    6:  "#AA4499",   # Chemicals — Hóa chất và nhựa
    7:  "#999933",   # Vehicles — Phương tiện vận tải
    8:  "#44AA99",   # Machinery — Máy móc và thiết bị đo
    9:  "#88CCEE",   # Electronics — Điện tử
    10: "#DDDDDD",   # Other — Khác
}

# Màu chữ đặt đè lên từng ô màu ở trên. Tính sẵn để không ai phải đoán:
# mọi cặp dưới đây đạt tương phản WCAG >= 4,5:1.
SECTOR_TEXT_ON_FILL = {
    1:  "#000000", 2:  "#FFFFFF", 3:  "#000000", 4:  "#FFFFFF", 5:  "#FFFFFF",
    6:  "#FFFFFF", 7:  "#000000", 8:  "#000000", 9:  "#000000", 10: "#000000",
}

SECTOR_NAME_VI = {
    1:  "Dệt may, giày dép, nội thất",
    2:  "Nông sản, gỗ và giấy",
    3:  "Đá, thủy tinh, gốm sứ",
    4:  "Khoáng sản và nhiên liệu",
    5:  "Kim loại",
    6:  "Hóa chất và nhựa",
    7:  "Phương tiện vận tải",
    8:  "Máy móc và thiết bị",
    9:  "Điện tử",
    10: "Khác",
}

# ---------------------------------------------------------------------------
# Thang màu tuần tự — dùng cho ma trận kề (T16) và mọi bản đồ nhiệt.
#
# Sáng đến tối theo L* giảm đều: 99 → 91 → 72 → 50 → 24. Vì thứ tự nằm ở độ
# sáng chứ không nằm ở sắc độ, người mù màu vẫn đọc đúng thứ tự. Bước ΔE giữa
# các nấc: 15, 23, 23, 23 — đều nhất trong ba thang đã thử.
#
# ⚠️ Không đặt thang này chung một hình với chú giải 10 ngành: nấc #FE9929 nằm
# gần màu ngành Đá #DDCC77 và Phương tiện vận tải #999933.
# ---------------------------------------------------------------------------
SEQUENTIAL_SCALE = ["#FFFFE5", "#FEE391", "#FE9929", "#CC4C02", "#662506"]

# ---------------------------------------------------------------------------
# Làm nổi Việt Nam — BẰNG HÌNH DẠNG, KHÔNG BẰNG MÀU.
#
# Đã thử thêm màu thứ 11 để nhấn Việt Nam. Không còn chỗ: mọi màu cam/đỏ đủ
# khác 10 màu ngành ở mắt thường (ΔE 22–27) đều tụt xuống ΔE 4–8 khi mô phỏng
# mù màu, tức là trùng với màu ngành. Chỉ màu đen còn đứng vững (ΔE 19,9).
#
# Nên Việt Nam được đánh dấu bằng: viền đen 1,5px quanh nút/ô, nhãn in đậm,
# và — nếu là biểu đồ đường — đường dày 2,2px trong khi các nước khác 1,0px.
# Kênh màu để dành cho ngành hàng.
# ---------------------------------------------------------------------------
HIGHLIGHT_STROKE = "#000000"
HIGHLIGHT_STROKE_WIDTH = 1.5
HIGHLIGHT_LINE_WIDTH = 2.2
DEFAULT_LINE_WIDTH = 1.0

# ---------------------------------------------------------------------------
# Font và kích thước hình — T04, xem docs/style-guide.md.
#
# Thứ tự là thứ tự ưu tiên: máy nào có Segoe UI thì dùng, không thì Arial,
# không nữa thì DejaVu Sans. DejaVu Sans đi kèm sẵn trong matplotlib nên chắc
# chắn máy nào cũng có. Đã kiểm: cả ba font đều có đủ 19 ký tự có dấu tiếng
# Việt đem ra thử (ế ữ ợ ằ ẵ ọ ỹ Đ ...), nên chữ không bị mất dấu hay hiện ô
# vuông trên máy người khác.
# ---------------------------------------------------------------------------
FONT_STACK = ["Segoe UI", "Arial", "DejaVu Sans"]

# Khổ A4 dọc, lề 2,5 cm -> vùng chữ rộng 16 cm = 6,30 inch.
# Dùng đúng mấy con số này để mọi hình trong báo cáo cùng một cỡ chữ thật.
FIG_WIDTH_FULL = 6.30    # hình chạy hết chiều ngang trang
FIG_WIDTH_HALF = 3.05    # hai hình đặt cạnh nhau
FIG_HEIGHT_DEFAULT = 3.90
FIG_DPI_SCREEN = 200
FIG_DPI_PRINT = 300

# Cỡ chữ tính bằng point, đã tính cho hình rộng 6,30 inch xuất ở 300 dpi.
FONT_SIZES = {
    "title": 13,      # câu tiêu đề nói kết luận
    "subtitle": 10,   # dòng phụ: nguồn, năm, đơn vị
    "axis": 9,
    "tick": 8,
    "legend": 9,
    "annotation": 8,
    "footnote": 7,    # dòng nguồn dữ liệu dưới cùng
}

# Các mốc thời gian dùng cho small multiples (T20).
MILESTONE_YEARS = [1995, 2005, 2015, 2023]

# Năm "hiện tại" của cả đồ án. Mọi con số một-năm — số cạnh, mật độ, xếp hạng,
# treemap "nay" — phải lấy đúng năm này để báo cáo không tự mâu thuẫn.
REFERENCE_YEAR = 2023

# ---------------------------------------------------------------------------
# Vi sao la 2023 chu khong phai 2024 - DA DO, khong phai phong doan.
#
# Ban phat hanh Atlas 2024 con TAM. So canh dung rat yen suot chin nam roi roi
# dung o nam cuoi:
#
#     2015: 27.323   2022: 27.489   2023: 27.535   2024: 25.754
#
# Trong khi tong gia tri thi binh thuong: 21,66 -> 21,81 nghin ty USD. Tuc la
# cai thieu la cac CAP nuoc, khong phai tien.
#
# Kiem o file tho data/atlas/cc_year.csv: cap VNM-ARE nam 2023 co 6,58 ty USD,
# nam 2024 khong co mot dong nao. Tuong tu VNM-RUS, VNM-LAO, VNM-BGD. Khong
# nuoc nao bien mat han - ca 231 nuoc deu co mat ca hai nam - thieu la thieu
# tung cap. 168 trong 231 nuoc mat ban hang khi sang 2024; UAE nang nhat,
# 218 xuong 129. Dau hieu kinh dien cua mot ban phat hanh tam: nuoc chua nop so
# lieu cho Comtrade thi Atlas chi dung lai duoc phan nao tu bao cao doi tac.
#
# Hau qua cu the voi de tai nay: Viet Nam tut tu 166 xuong 129 ban hang, mat 37
# ban hang mang theo 11,4 ty USD (2,96% xuat khau). Trong so do co LAO - mot
# nuoc ASEAN, ngay giua lat cat Viet Nam-ASEAN. De nguyen thi bieu do doc thanh
# "Viet Nam dang mat ban hang", nguoc han su that.
#
# Rieng GIA TRI thi 2024 van dung duoc (treemap, RCA, PCI, ECI, chord luong
# lon) vi phan thieu chi 2,96%. Hong la hong nhung gi DEM va nhung gi ve HINH
# THU mang. Nhung tron hai nam trong mot bai vi pham Checklist #18, nen ca do
# an dung mot nam duy nhat.
# ---------------------------------------------------------------------------
LAST_COMPLETE_YEAR = 2023

# Cac nam co du lieu chua day du. Bieu do chuoi thoi gian phai dung o
# LAST_COMPLETE_YEAR, hoac ve tiep nhung ghi ro la so tam - khong duoc de nguoi
# xem doc cai hut o panel cuoi nhu mot su that ve the gioi.
PROVISIONAL_YEARS = [2024]

# ---------------------------------------------------------------------------
# Quy tac loc canh - DA CHOT o T10.
# Bang chung: data/processed/threshold_coverage.csv (sinh boi analyze_network.py).
#
# Nguong la MOT TY LE tren tong xuat khau the gioi CUA NAM DO, khong phai mot so
# USD co dinh. Thuong mai toan cau tang 4,51 lan tu 1995 (4,80 nghin ty USD) den
# 2023 (21,66 nghin ty USD), nen mot nguong 10 ty USD co dinh do hai nam bang
# hai cai thuoc khac nhau: giu lai 89 canh nam 1995 nhung 3xx canh nam 2023, va
# small multiples se doc thanh "thuong mai moi xuat hien" thay vi "thuong mai
# lon len". Dung ty le thi so canh on dinh qua cac nam.
#
# Chon 0,046% de nam tham chieu ra 9,96 ty USD, sat con so 10 ty nhom da do va
# ghi trong de bai. Tuc la nam tham chieu KHONG doi thuoc do; chi cac nam con
# lai duoc quy ve cung mot thuoc. Con so nay duoc chon khi nam tham chieu con la
# 2024 (ra 10,03 ty); doi sang 2023 no ra 9,96 ty - lech 0,7%, coi nhu trung -
# nen quy tac T10 song nguyen ven qua lan doi nam nay.
# ---------------------------------------------------------------------------
THRESHOLD_SHARE = 0.00046

# Bao hiem cho nuoc trong tam: moi nuoc trong FOCUS_ISO3 luon giu lai toi da
# ngan nay luong xuat va ngan nay luong nhap lon nhat cua rieng no, du khong dat
# nguong. Khong co no thi nguong tren XOA Viet Nam khoi panel 1995, va xoa Lao /
# Brunei / Myanmar khoi hau het cac nam - khong chap nhan duoc voi mot de tai
# ten la "vi tri cua Viet Nam". Gia phai tra chi la +23 canh (385 -> 408).
FOCUS_TOPK = 3

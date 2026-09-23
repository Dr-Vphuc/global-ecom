# -*- coding: utf-8 -*-
"""Bảng tra cứu dùng chung cho toàn bộ pipeline.

Chứa:
  - COUNTRY_VI : ISO3 -> (tên tiếng Việt, vùng, châu lục)
  - ASEAN_ISO3 : danh sách mã nước ASEAN
  - FOCUS_ISO3 : nước được tô đậm trong biểu đồ (cột is_focus của nodes.csv)
  - NON_COUNTRY : các mã KHÔNG phải quốc gia thật
  - SECTOR_PALETTE_PROVISIONAL : bảng màu tạm cho 10 ngành cấp 1 HS92

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
# Bảng màu 10 ngành cấp 1 HS92.
#
# ⚠️ TẠM THỜI — phải chốt lại ở T04 (R3 sở hữu style-guide.md).
# Đây là bảng Tableau 10 đã đảo thứ tự cho hợp ngữ nghĩa ngành,
# CHƯA kiểm tra mù màu đỏ–lục (checklist #13) và chưa kiểm tra trên nền tối.
# ---------------------------------------------------------------------------
SECTOR_PALETTE_PROVISIONAL = {
    1:  "#4E79A7",   # Textiles  — Dệt may, giày dép, nội thất
    2:  "#59A14F",   # Agriculture — Nông sản, động vật, gỗ, giấy
    3:  "#9C755F",   # Stone — Đá, thủy tinh, gốm sứ
    4:  "#8C564B",   # Minerals — Khoáng sản, nhiên liệu, quặng, muối
    5:  "#B07AA1",   # Metals — Kim loại
    6:  "#F28E2B",   # Chemicals — Hóa chất và nhựa
    7:  "#E15759",   # Vehicles — Phương tiện vận tải
    8:  "#76B7B2",   # Machinery — Máy móc và thiết bị đo
    9:  "#EDC948",   # Electronics — Điện tử
    10: "#BAB0AC",   # Other — Khác
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

# Các mốc thời gian dùng cho small multiples (T20).
MILESTONE_YEARS = [1995, 2005, 2015, 2024]

# Năm "hiện tại" của cả đồ án. Mọi con số một-năm — số cạnh, mật độ, xếp hạng,
# treemap "nay" — phải lấy đúng năm này để báo cáo không tự mâu thuẫn.
REFERENCE_YEAR = 2024

# Ngưỡng lọc cạnh mặc định, USD.
# ⚠️ TẠM THỜI — phải chốt lại ở T10 bằng bảng đánh đổi, không chọn cảm tính.
DEFAULT_THRESHOLD = 1e10

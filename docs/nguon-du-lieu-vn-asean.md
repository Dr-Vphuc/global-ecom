# Nguồn dữ liệu cho đề tài: Chuỗi giá trị & phụ thuộc thương mại Việt Nam – ASEAN

> Ghi chú khảo sát nguồn dữ liệu, lập ngày 2026-09-20.
> Vai trò giả định: chuyên viên phân tích thị trường.
> Các mốc năm phủ dữ liệu cần kiểm tra lại trên website vì mỗi năm nhà cung cấp đều phát hành bản mới.

---

## 1. Ba bộ dữ liệu lõi — dùng vào đâu

| Bộ | Độ chi tiết | Phủ | Ưu / Nhược cho đề tài |
|---|---|---|---|
| **BACI (CEPII)** | Song phương, **HS 6 chữ số**, giá trị (nghìn USD, FOB) + khối lượng (tấn) | ~200 nước, 1995–2023/24, nhiều phiên bản HS92/96/02/07/12/17/22 | **Xương sống nên dùng.** Đã *hòa giải số liệu gương* (mirror reconciliation, phương pháp Gaulier–Zignago): mỗi luồng A→B chỉ có **một** giá trị duy nhất, không còn cảnh "VN báo xuất 10, Thái báo nhập 13". Cực kỳ quan trọng khi vẽ mạng lưới nội khối vì Lào/Myanmar/Campuchia báo cáo rất tệ. Nhược: không có dịch vụ, không có chênh lệch CIF/FOB, độ trễ ~1.5–2 năm. |
| **UN Comtrade** | HS 2–6 số, **theo tháng**, 1962–nay | Toàn cầu, nhưng "reporter-declared" thô | Dùng để **cập nhật phần đuôi thời gian** (2024–2026) mà BACI chưa có, và để lấy **thương mại dịch vụ (EBOPS)**. API miễn phí có giới hạn số lần gọi (`comtradeapicall` — package Python chính chủ của UN). Nhược: dữ liệu thô chưa hòa giải, có luồng bảo mật (confidential), tái xuất của Singapore làm phồng số. |
| **Atlas of Economic Complexity (Harvard Growth Lab)** | Country–product–year + country–partner–product–year | 1962/1995–nay, HS92 & SITC | Giá trị thật nằm ở **chỉ số phái sinh có sẵn**: ECI, PCI, proximity, density, **Complexity Outlook Gain**. Đây là bộ để trả lời "VN đang ở nấc nào của chuỗi giá trị và có thể nhảy sang sản phẩm nào mà Thái/Malaysia đã làm được". Tải qua Harvard Dataverse. Nhược: file country-partner-product khá nặng (vài GB). |

> **Điểm mù chung của cả ba:** chúng đo **thương mại gộp (gross trade)**. Mà "phụ thuộc chuỗi giá trị" thì gross trade *nói dối rất nặng* với Việt Nam — một chiếc điện thoại xuất 500 USD có thể chỉ chứa 30–40 USD giá trị gia tăng nội địa. Nếu chỉ dùng BACI/Comtrade, bài phân tích sẽ bị chấm là "mô tả luồng hàng", không phải "phân tích chuỗi giá trị".

> **Ghi chú cập nhật (2026-09-24):** đọc dòng "Xương sống nên dùng" của BACI
> kèm mục 7 — Atlas **cũng** hoà giải số liệu gương, nên lợi thế riêng của BACI
> hẹp hơn bảng này gợi ý.

---

## 2. Mảnh ghép thiếu: dữ liệu giá trị gia tăng / GVC

Nhóm này **nên bổ sung ít nhất một bộ**:

- **OECD TiVA (Trade in Value Added)** — bản 2023 phủ 1995–2020, ~76 nền kinh tế × 45 ngành. Có đủ VN + hầu hết ASEAN. Cho trực tiếp: **DVA/FVA trong xuất khẩu**, **backward/forward participation**, giá trị gia tăng theo nước-nguồn và theo ngành-nguồn. Miễn phí, tải bulk CSV từ OECD Data Explorer. → Bộ trả lời chuẩn xác câu "VN phụ thuộc bao nhiêu % đầu vào từ ASEAN".
- **ADB MRIO** — bảng I-O đa vùng, ~62–73 nền kinh tế × 35 ngành, 2000 & 2007–2023. **Phủ châu Á tốt hơn OECD**, cập nhật nhanh hơn, miễn phí hoàn toàn (xlsx/csv trên adb.org). ADB còn công bố sẵn bộ **GVC indicators** đã phân rã theo Koopman–Wang–Wei / Borin–Mancini.
- **UIBE GVC Indicators** (ĐH Kinh tế Đối ngoại Bắc Kinh) — **chỉ số GVC đã tính sẵn** trên nền ADB MRIO / WIOD / Eora. Nếu không muốn tự làm ma trận Leontief thì lấy thẳng ở đây, tiết kiệm cả tuần.
- **Eora / Eora26** — 190 nước, phủ cả Lào, Campuchia, Myanmar, Brunei (những nước OECD TiVA hay thiếu). Miễn phí cho mục đích học thuật (worldmrio.com).
- **World Bank GVC Database** — chỉ số Borin–Mancini theo nước-ngành, dễ dùng.

---

## 3. Bộ phụ trợ — để giải thích *tại sao* có sự phụ thuộc đó

### Chính sách thương mại
- **WITS (World Bank)** — cổng gộp Comtrade + **UNCTAD TRAINS**: thuế MFN và **thuế ưu đãi**. Dùng để tính *preference margin* của **ATIGA** (Hiệp định Thương mại Hàng hóa ASEAN) và **RCEP** → giải thích luồng hàng chuyển hướng.
- **UNCTAD NTM database** — biện pháp phi thuế quan (thường mới là rào cản thật trong nội khối ASEAN).
- **WTO Tariff Download Facility / RTA database**, **DESTA** — độ "sâu" của hiệp định.

### Bối cảnh khu vực
- **ASEANstats** (`data.aseanstats.org`) — số liệu **chính thức** của Ban Thư ký ASEAN về thương mại và FDI nội khối. Nên dùng để đối chiếu/trích dẫn con số "tỷ trọng nội khối ASEAN ~21–22%".
- **IMF DOTS** — luồng song phương tổng hợp, theo **tháng**, chuỗi dài từ 1948. Tốt cho time-series tổng quan và vá lỗ hổng.
- **UNCTADstat** — có sẵn **chỉ số tập trung HHI** theo sản phẩm/thị trường cho từng nước, khỏi tự tính.

### Việt Nam
- **Tổng cục Hải quan** (`customs.gov.vn`) — thống kê **theo tháng, theo HS, theo đối tác**, song ngữ, độ trễ chỉ ~3–4 tuần. Nguồn duy nhất cho phần 2025–2026.
- **GSO** — bảng **I-O Việt Nam (2019, 2012)** cho chuỗi giá trị *trong nước*; và thống kê FDI.
- **Cục Đầu tư nước ngoài (MPI)** — vì >70% kim ngạch xuất khẩu VN là của khối FDI. Không có lớp FDI thì không giải thích được bản chất "gia công" của chuỗi giá trị VN.

### Logistics (nếu muốn viz động, ăn điểm hình ảnh)
- **UNCTAD LSCI** (chỉ số kết nối vận tải biển).
- **IMF PortWatch** (`portwatch.imf.org`) — lượt tàu ghé cảng **theo ngày**, miễn phí.

---

## 4. Mẹo kỹ thuật quan trọng nhất: tách hàng trung gian bằng BEC

Nếu chỉ có BACI/Comtrade mà vẫn muốn nói chuyện chuỗi giá trị, dùng bảng tương ứng **HS → BEC (Broad Economic Categories, Rev.5)** của UN Statistics (miễn phí):

- Tách luồng thành **hàng trung gian / tư liệu sản xuất / hàng tiêu dùng cuối**.
- Thương mại **hàng trung gian nội khối ASEAN** chính là proxy trực tiếp của *mạng lưới sản xuất* (production sharing).
- Kết hợp với **chỉ số Grubel–Lloyd** (thương mại nội ngành): GL cao ở nhóm HS 85/84 = dấu hiệu rõ của phân công theo công đoạn, không phải trao đổi hàng hóa thông thường.

### Các chỉ số nên tính

| Chỉ số | Trả lời câu hỏi |
|---|---|
| RCA / Balassa | VN có lợi thế ở nhóm nào so với ASEAN? |
| Trade Complementarity Index | VN và Thái/Indonesia **bổ trợ** hay **cạnh tranh**? |
| Export Similarity Index (Finger–Kreinin) | Mức độ giẫm chân nhau trên thị trường thứ ba |
| Grubel–Lloyd | Thương mại nội ngành = phân công công đoạn |
| HHI (sản phẩm & thị trường) | Mức độ tập trung → rủi ro |
| **Strategic dependency (phương pháp EC-JRC)** | Sản phẩm nào VN nhập >50% từ **một** nguồn + khó thay thế → "điểm nghẽn" |

Chỉ số cuối rất hợp với đề tài **phụ thuộc**: cho ra một danh sách sản phẩm cụ thể, dễ vẽ và dễ kể chuyện.

---

## 5. Đề xuất stack cụ thể cho đồ án DataViz

**Tối thiểu khả thi (1–2 người, ~1 tuần xử lý dữ liệu):**

```
BACI HS92 1995–2023   → luồng song phương VN × 9 nước ASEAN × HS6
  + HS→BEC Rev.5      → tách trung gian / tư liệu sản xuất / hàng cuối
  + ADB MRIO (hoặc UIBE GVC đã tính sẵn) → 1–2 chart giá trị gia tăng
  + Hải quan VN        → cập nhật 2024–2026
```

**Xử lý:** BACI HS92 full ~1.5–2 GB khi giải nén, mỗi năm ~1.2 triệu dòng. Đừng dùng pandas đọc thẳng CSV — nạp vào **DuckDB** rồi xuất **Parquet** đã lọc (chỉ VN + ASEAN + đối tác lớn), file cuối chỉ còn vài chục MB, đủ nhẹ để nhúng vào dashboard web.

### Ý tưởng biểu đồ khớp với đề tài
- **Sankey 3 tầng**: ASEAN → (đầu vào trung gian) → VN chế biến → (thành phẩm) → EU/Mỹ/TQ. Hình ảnh "chuỗi giá trị" trực quan nhất.
- **Chord diagram** luồng nội khối ASEAN, tách riêng hàng trung gian vs hàng cuối.
- **Heatmap phụ thuộc**: nước × nhóm hàng, màu = % nhập khẩu từ nguồn lớn nhất.
- **Bump chart**: thứ hạng đối tác của VN trong ASEAN qua thời gian (Thái Lan tụt, Indonesia lên...).
- **Scatter gross-export vs domestic-value-added**: khoảng cách giữa "kim ngạch hoành tráng" và "giá trị thực nhận".
- **Product space** (từ Atlas) highlight vị trí VN so với Malaysia/Thái Lan.

---

## 6. Ba cạm bẫy dữ liệu phải nêu trong báo cáo

1. **Singapore** là cảng trung chuyển — kim ngạch VN–Singapore bị thổi phồng bởi tái xuất; nhiều hàng ghi "từ Singapore" thực ra xuất xứ nơi khác.
2. **Trade gộp ≠ phụ thuộc thực** (xem mục 2). Luôn có ít nhất một lớp value-added để đối chứng.
3. **Lào, Myanmar, Campuchia, Brunei** báo cáo Comtrade rất thưa → **bắt buộc** dùng số liệu gương. BACI đã xử lý sẵn — đây chính là lý do nên lấy BACI làm gốc thay vì Comtrade thô.

---

## 7. Trạng thái & bước tiếp theo

> Cập nhật **2026-09-24**. Mục này là sổ kiểm kê thật, bám theo repo. Các mục
> 1–6 phía trên giữ nguyên làm bản khảo sát ban đầu.

**Phạm vi đã chốt:** đề tài là *"Mạng lưới thương mại quốc tế — vị trí của Việt
Nam trong cấu trúc thương mại toàn cầu"*, kèm lát cắt Việt Nam – ASEAN. Tài liệu
này được viết cho một đề tài **rộng hơn** ("chuỗi giá trị & phụ thuộc"), nên hãy
đọc nó như một **danh sách khảo sát**, không phải danh sách bắt buộc. Một đồ án
DataViz không cần TiVA + MRIO + ma trận Leontief; nó cần biểu đồ tốt và một câu
chuyện có bằng chứng.

### Đã có gì

| Mục | Trạng thái |
|---|---|
| §1 Ba bộ lõi | **1/3** — chỉ Atlas. BACI và Comtrade chưa đụng tới |
| §2 Giá trị gia tăng / GVC | **0/5** |
| §3 Bộ phụ trợ | **0/11** |
| §4 Mapping HS→BEC Rev.5 | chưa có |
| §4 Bảng chỉ số | **1/6** — mới RCA (Balassa), đã tính và kiểm định trong `src/build_intermediate.py` |

Ngay trong bộ Atlas cũng mới lấy **6 trên 23 file** (≈69 MB trên ≈16,5 GB):
`cc_year`, `cp_year_hs2`, `hs92_country_year`, `hs92_data_dictionary`,
`location_country`, `product_hs92`.

Đủ cho toàn bộ biểu đồ đã lên kế hoạch. Không hạng mục nào của đồ án còn bị
chặn vì thiếu dữ liệu, **trừ T08** — đúng cái task ghi rõ là cần tài khoản CEPII
và API key Comtrade.

### Vì sao không lấy nốt

Đường truyền tới Dataverse từ máy làm bài chỉ khoảng **30 KB/s**:

| File chưa lấy | Dung lượng | Thời gian tải ước tính |
|---|---|---|
| `hs92_country_product_year_4.csv` | 452 MB | ~4,2 giờ |
| `hs92_country_product_year_6.csv` | 1,0 GB | ~9,4 giờ |
| `hs92_country_country_product_year_6_2020_2024.csv` | 2,9 GB | ~26 giờ |
| ba file song phương HS6 còn lại (1995–2019) | 12,2 GB | ~113 giờ |

Bốn file song phương HS6 cộng lại là vài ngày chạy liên tục — coi như không khả
thi trên máy này, và HS6 (5.040 mã) cũng quá mịn để vẽ. HS4 là ranh giới: chạy
qua đêm được, đổi lại 1.243 nhóm hàng thay vì 97.

### Đánh giá lại: BACI có còn là "xương sống nên dùng"?

Lý do mạnh nhất để chọn BACI ở §1 là nó đã **hoà giải số liệu gương**, tức xử lý
được chuyện Lào / Myanmar / Campuchia báo cáo rất thưa. Nhưng Atlas **cũng làm
việc đó** — Growth Lab có bước làm sạch và hoà giải riêng trước khi phát hành.
Ba file Atlas đang dùng khớp nhau đến **0,000%** ở tổng xuất khẩu thế giới năm
2024 (mục 8 của `src/check_raw_data.py`), tức không có lỗ hổng báo cáo nào lọt
qua.

Cái BACI thật sự cho thêm là **HS6 song phương ở dung lượng tải được** — thứ
Atlas chỉ phát hành dưới dạng file nhiều GB. Cần HS6 song phương thì đăng ký
BACI; không cần thì bộ Atlas hiện tại là đủ.

### Việc chỉ thành viên nhóm làm được

- Tài khoản **CEPII** để tải BACI — miễn phí, đăng ký bằng email.
- **API key UN Comtrade** — miễn phí, có hạn mức số lần gọi.

### Nếu còn thời gian, theo thứ tự đáng làm

1. `hs92_country_product_year_4.csv` — HS4, chạy qua đêm, treemap và sunburst
   chi tiết hơn hẳn.
2. Một lớp value-added: lấy **chỉ số UIBE hoặc ADB GVC đã tính sẵn**, đừng tự
   dựng ma trận Leontief.
3. Hải quan Việt Nam cho phần 2025–2026 — chỉ cần nếu báo cáo muốn chạm tới năm
   hiện tại.

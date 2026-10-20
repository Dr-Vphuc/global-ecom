# Phương pháp luận (T25)

Phần này trả lời bốn câu: dữ liệu từ đâu, làm sạch thế nào, giới hạn ở chỗ nào,
và vì sao chọn những ngưỡng đã chọn. Mọi con số đều do script trong `src/` sinh
ra; tên script ghi kèm từng mục để kiểm lại được.

---

## 1. Nguồn dữ liệu

### 1.1 Chọn gì và vì sao

Toàn bộ phân tích dựa trên **The Atlas of Economic Complexity** của Harvard
Growth Lab, phân loại **HS92**, tải qua Harvard Dataverse. Năm file được dùng:

| File | Nội dung | Dung lượng |
|---|---|---|
| `cc_year.csv` | Thương mại song phương nước–nước–năm | 29 MB |
| `cp_year_hs2.csv` | Xuất khẩu nước × nhóm HS2 × năm | 38 MB |
| `hs92_country_year.csv` | ECI, COI, đa dạng hóa theo nước–năm | 0,4 MB |
| `product_hs92.csv` | Cây sản phẩm HS92, 6.390 nút, 4 tầng | 0,8 MB |
| `location_country.csv` | Danh mục quốc gia, mã ISO3, vùng | 10 KB |

Phân công ban đầu dự kiến đối chiếu thêm **CEPII BACI** và **UN Comtrade**.
Chúng tôi đã bỏ kế hoạch đó, có lý do, và lý do ấy nằm ở mục 3.1 — nó là một
phát hiện chứ không phải một việc bị cắt.

### 1.2 Toàn vẹn dữ liệu thô

`src/check_raw_data.py` chạy 8 nhóm kiểm tra và là **cửa chặn**: thoát mã khác 0
thì pipeline dừng. Kết quả trên bộ dữ liệu đang dùng:

- Cây HS92 đủ 4 tầng, đúng **10 / 97 / 1.243 / 5.040** nút, không có nút mồ côi.
- ECI đã chuẩn hóa đúng: |trung bình| ≤ 0,076, |độ lệch chuẩn − 1| ≤ 0,054.
- **Đối chiếu chéo ba file độc lập** về tổng xuất khẩu thế giới năm 2024:
  `cc_year.csv` 21,8129 — `cp_year_hs2.csv` 21,8129 — `hs92_country_year.csv`
  21,8129 nghìn tỷ USD. Lệch tối đa **0,000%**.
- Hai mã không phải quốc gia được giữ lại có chủ ý: `USP` (vùng đặc biệt) và
  `ANS` (không rõ nước). Chúng là nơi dồn phần dư; xóa đi thì tổng không khớp.

### 1.3 Chất lượng cây sản phẩm

`src/check_tree.py` kiểm 10 nhóm tiêu chí trên cây HS92, và tự có chế độ
`--self-test` để chứng minh bản thân nó phát hiện được lỗi (bốn ca kiểm: cây
thật phải đạt; xóa một nút tầng 1 phải báo hỏng; xóa một nút tầng 2 phải báo
hỏng; xóa một nút tầng 6 thì chỉ cảnh báo).

Kết quả: **tầng 1 và tầng 2 toàn vẹn**, nên mọi biểu đồ cây của đồ án dùng
được. Còn tồn tại lỗi ở tầng 4 trở xuống:

- Một số mã dạng `XXXX` — nút giữ chỗ của Atlas, không phải mã HS thật.
- Mã `3501` nằm dưới chương `34` thay vì chương `35`.

Hai lỗi này **không ảnh hưởng** biểu đồ hiện tại vì đồ án chỉ vẽ tới tầng 2,
nhưng phải ghi ra: ai mở rộng xuống HS4 hoặc HS6 sẽ gặp lại chúng.

---

## 2. Làm sạch và xuất file trung gian

`src/build_intermediate.py` chuyển `data/atlas/` thành 5 file theo **hợp đồng dữ
liệu** đã chốt ở Tuần 1 (sheet "Hợp đồng dữ liệu" trong `phan-cong-cong-viec.xlsx`).
Hợp đồng này chốt trước khi ai bắt đầu vẽ, để hai thành viên còn lại sinh dữ
liệu giả đúng schema mà làm song song, không phải chờ.

Bốn quyết định làm sạch:

1. **Bỏ mọi dòng có `export_value = 0`.** Giá trị 0 không phải một cạnh — nó là
   "hai nước này không buôn mặt hàng này", khác hẳn "buôn rất ít". Giữ lại thì
   mật độ mạng bị thổi lên và mọi chỉ số tô-pô sai theo.
2. **Chuẩn hóa mã nước về ISO3** và nối với vùng địa lý từ `location_country.csv`.
3. **Tính sẵn `log_value = log10(export_value)`** vì phân bố lệch 5–6 bậc độ
   lớn và gần như mọi hình đều cần thang log.
4. **Đánh dấu sẵn `above_threshold`** theo quy tắc ở mục 4.2, để mọi script vẽ
   dùng chung đúng một tập cạnh đã lọc thay vì mỗi script tự lọc một kiểu.

Dữ liệu thô và file trung gian **không được commit** (quyết định B8): file lớn
nhất 38 MB, và git không phải chỗ chứa dữ liệu. Thay vào đó `src/download_atlas.py`
tải lại được từ Dataverse, có kiểm **MD5** và hỗ trợ nối tiếp khi đứt mạng.

---

## 3. Giới hạn của dữ liệu

### 3.1 Không có nguồn độc lập để kiểm chéo — và đây là phát hiện, không phải thiếu sót

Phân công ghi "đối chiếu 3–5 luồng giữa Atlas, BACI và Comtrade". Hai vấn đề:

**Thứ nhất, ba cái tên đó không phải ba nguồn độc lập.** Atlas và BACI đều dẫn
xuất từ UN Comtrade. Đối chiếu chúng chỉ đo được khác biệt giữa các thuật toán
làm sạch, không đo được độ tin cậy của số liệu gốc. Báo cáo kết quả đó dưới
dạng "ba nguồn đều khớp" sẽ là một tuyên bố sai.

**Thứ hai, có một phép kiểm độc lập thật sự nằm sẵn trong dữ liệu.** Mỗi luồng
hàng A→B được khai báo hai lần bởi hai cơ quan hải quan khác nhau:

- A khai: "tôi xuất sang B x USD" → `cc_year(A, B).export_value`
- B khai: "tôi nhập từ A y USD" → `cc_year(B, A).import_value`

Chênh lệch giữa hai con số gọi là **chênh lệch gương**, và nó là phép kiểm tiêu
chuẩn trong thống kê thương mại quốc tế. Chênh lệch này bình thường khác 0 vì
ba nguyên nhân hệ thống: giá FOB của nước xuất so với giá CIF của nước nhập
(thường lệch 5–10%); quy tắc nước xuất xứ so với nước gửi hàng; và thời điểm
ghi nhận khi hàng rời cảng cuối năm này, cập cảng đầu năm sau.

`src/compare_mirror.py` đo phép này trên 2.093 luồng từ 1 tỷ USD trở lên. Kết
quả:

> **2.093 / 2.093 luồng (100,0%) có hai con số TRÙNG KHÍT nhau.**
> Trung vị chênh lệch: 0,0%. Phân vị 10 và 90 đều 0,0%.
> Kết quả giống hệt khi chạy lại với năm 1995 (679/679 luồng).

Kết luận: **Growth Lab đã hòa giải số liệu hai chiều trước khi phát hành.** Bộ
dữ liệu cho một con số duy nhất cho mỗi luồng, không giữ hai bản khai gốc.

Hệ quả phải nói thẳng: **chúng tôi không thể tự đo sai số của dữ liệu mình đang
dùng.** Số liệu đã được Growth Lab hòa giải theo phương pháp của họ; chúng tôi
dùng số đó và không có nguồn độc lập nào để kiểm chéo. Đây là một giới hạn
thật, và nói ra nó trung thực hơn là trình bày một bảng ba cột số giống nhau
rồi gọi đó là "đã đối chiếu".

### 3.2 Năm mốc là 2023, không phải 2024

Bản Atlas có dữ liệu 2024 nhưng còn tạm: **thiếu 1.781 cặp nước**, riêng Việt
Nam mất **37 bạn hàng** so với 2023. Dùng 2024 làm năm mốc thì phát hiện "Việt
Nam mất thị trường" sẽ bị thổi phồng bởi dữ liệu chưa về đủ chứ không phải bởi
hiện thực. Chuỗi thời gian vì vậy dừng ở **2023** (quyết định B1, B10).

### 3.3 Cây sản phẩm chỉ vẽ tới tầng 2

Đồ án vẽ **10 ngành cấp 1 và 97 nhóm cấp 2**. Tầng 4 (1.243 nút) và tầng 6
(5.040 nút) có trong `product_hs92.csv` và được kiểm toàn vẹn, nhưng **dữ liệu
giá trị** theo hai tầng đó nằm ở một file 452 MB ngoài phạm vi đã chốt ở T01.

Ranh giới này là có chủ ý, không phải bỏ sót: ở kích thước trình chiếu, 1.243 ô
trên một treemap thành những vệt không đọc được. Nhưng phải ghi rõ, vì mô tả
nhiệm vụ T13 có nhắc "đầy đủ 4 tầng".

### 3.4 Betweenness đo được gì, và không đo được gì

Betweenness của Việt Nam trong đồ thị đã lọc là **0,0000**, xếp hạng 16/73
nhưng **đồng hạng với 57 nước khác**. Con số thứ hạng đó không đọc được, và
`src/compute_metrics.py` tự in ra cảnh báo này cùng với số nước đồng hạng.

Nguyên nhân có thể giải thích được: mật độ mạng là 51,8% (mục 4.1), nên hầu
hết các cặp nước đã nối thẳng với nhau và không ai cần đi vòng qua ai. Trong
một mạng dày như vậy, betweenness gần như bằng 0 với **mọi** nước, không riêng
Việt Nam.

Ngoài ra, betweenness có trọng số phụ thuộc vào cách nghịch đảo trọng số:
networkx hiểu `weight` là **khoảng cách**, trong khi giá trị thương mại thì
ngược lại — buôn càng nhiều càng "gần". Chúng tôi nghịch đảo và chuẩn hóa theo
luồng lớn nhất, đồng thời **giữ luôn bản không trọng số** để người đọc tự thấy
kết luận có phụ thuộc vào lựa chọn đó hay không.

### 3.5 Cộng đồng là kết quả của thuật toán, không phải sự thật khách quan

Phân cụm dùng **Louvain** (modularity) trên đồ thị vô hướng gộp hai chiều. Đây
là thuật toán có yếu tố ngẫu nhiên, nên chúng tôi đo độ ổn định thay vì chỉ
chạy một lần:

> 20 hạt giống khác nhau → **100,0% số cặp nước giữ nguyên quan hệ** cùng cụm /
> khác cụm. Số cụm luôn là 3. Modularity không đổi: **0,337**.

Ổn định tuyệt đối trên đồ thị đã lọc. Vẫn phải nói đây là kết quả của một phép
tính, nhưng kết quả này không phải may mắn của một lần chạy.

---

## 4. Các ngưỡng đã chọn và lý do bằng số

### 4.1 Vì sao phải lọc cạnh

Mạng đầy đủ năm 2023 có **231 nút và 27.535 cạnh**, mật độ **51,8%**. Vẽ thẳng
ra node-link thì được một mảng mực.

Nhưng lý do sâu hơn nằm ở phân bố bậc. Người ta hay giả định mạng thương mại là
**scale-free** — vài hub lớn và một đuôi dài. `src/make_degree_dist.py` kiểm và
bác bỏ:

| Năm | Mật độ | Bậc trung vị | Bậc lớn nhất | max/trung vị | Gini trọng số |
|---|---|---|---|---|---|
| 1995 | 41,5% | 159 | 408 | 2,6 | 0,955 |
| 2005 | 49,0% | 213 | 439 | 2,1 | 0,958 |
| 2015 | 51,9% | 239 | 449 | 1,9 | 0,957 |
| 2023 | 51,8% | 242 | 447 | **1,8** | 0,957 |

Trong một mạng scale-free thật, tỷ lệ max/trung vị là hàng trăm lần. Ở đây là
1,8 — và đang **giảm** theo thời gian.

Kết luận phương pháp: **cấu trúc của mạng này không nằm ở tô-pô mà nằm ở trọng
số.** Gini theo trọng số cạnh là **0,957**; top 1% số cạnh giữ **61,2%** giá
trị. Nên việc lọc phải lọc theo **giá trị**, không theo bậc.

### 4.2 Ngưỡng đã chốt

> **0,046% tổng xuất khẩu thế giới mỗi năm, cộng giữ top-3 luồng vào/ra cho mỗi
> nước ASEAN.**

Năm 2023: còn **416 cạnh trên 73 nút**, giữ **67,8%** giá trị, đủ **10/10** nước
ASEAN. `src/analyze_network.py` in ra bảng so sánh 9 chiến lược ngưỡng khác
nhau để thấy đây không phải lựa chọn cảm tính.

**Vì sao ngưỡng tương đối chứ không tuyệt đối.** Ngưỡng cố định 10 tỷ USD cho
kết quả không so sánh được qua thời gian:

| Năm | Ngưỡng cố định 10 tỷ | Ngưỡng đã chốt |
|---|---|---|
| 1995 | 89 cạnh · 49,5% giá trị · ASEAN **4/10** | 383 cạnh · 73,9% · **10/10** |
| 2005 | 176 cạnh · 56,2% · ASEAN 5/10 | 406 cạnh · 70,2% · 10/10 |
| 2015 | 270 cạnh · 61,6% · ASEAN 6/10 | 407 cạnh · 68,1% · 10/10 |
| 2023 | 390 cạnh · 67,3% · ASEAN 8/10 | 416 cạnh · 67,8% · 10/10 |

Với ngưỡng cố định, phần lớn "thay đổi" quan sát được chỉ là lạm phát và tăng
trưởng danh nghĩa, không phải thay đổi cấu trúc.

**Vì sao có thêm quy tắc top-3 cho ASEAN.** Ngưỡng thuần tỷ lệ vẫn làm rơi
Brunei và Lào — hai nền kinh tế nhỏ nhưng nằm trong nhóm trọng tâm của đồ án.
Giữ top-3 luồng của mỗi nước ASEAN đảm bảo đủ 10/10 ở mọi năm mà chỉ thêm 23
cạnh (393 → 416).

**Một cái bẫy đã gặp thật.** Ngưỡng tuyệt đối luôn thiên vị nước lớn. Trong bản
đầu của biểu đồ chord (T17), ngưỡng 0,15% tổng thế giới đã lặng lẽ xóa mất **4
trong 8** luồng của Việt Nam — vì Việt Nam chỉ chiếm **1,8%** xuất khẩu thế
giới, nên một luồng rất lớn *đối với Việt Nam* vẫn nhỏ *so với thế giới*. Một
hình mang tên "lấy Việt Nam làm trọng tâm" lại giấu đi phần lớn luồng của Việt
Nam. Đã sửa: dải nào có Việt Nam thì không áp ngưỡng.

### 4.3 Vì sao node-link không vẽ mũi tên

**Đối ứng (reciprocity) của mạng là 0,837** — 84% các cặp nước buôn cả hai
chiều. Vẽ mũi tên hai đầu cho 84% số cạnh chỉ thêm mực mà không thêm thông tin
(quyết định B5). Chiều của dòng hàng nằm ở hover và ở ma trận kề, nơi hàng là
nước xuất và cột là nước nhập.

### 4.4 Ba hình mạng lưới dùng ba tập cạnh khác nhau — có chủ ý

| Hình | Tập cạnh | Lý do |
|---|---|---|
| T15 node-link | đã lọc, 416 cạnh | không lọc thì không đọc được |
| T16 ma trận kề | đã lọc, 416 cạnh | **phải giống T15** để so sánh hai họ biểu diễn có nghĩa |
| T17 chord | **đầy đủ**, không lọc | đã gộp 231 nước thành 10 khối nên mỗi cặp khối chỉ còn một dải; lọc thêm chỉ mất 32% giá trị mà không được gì |
| T20 vị trí theo thời gian | **đầy đủ** | câu hỏi là *đếm bạn hàng*, mà ngưỡng lại cắt đúng cái đuôi bạn hàng nhỏ cần đếm |

Khác biệt này được ghi trên chú thích của từng hình, để người đọc không tưởng
cả bốn hình dùng chung một tập cạnh.

---

## 5. Hệ thống thị giác — các lựa chọn đo được

### 5.1 Bảng màu 10 ngành

Nền: thang **"muted" của Paul Tol**, đổi ô Khoáng sản sang nâu đậm `#5D4037`.
Kiểm định bằng `src/check_palette.py` (ma trận Machado 2009 + CIEDE2000), không
kiểm bằng mắt. ΔE2000 của cặp gần nhau nhất:

> mắt thường **16,1** · protan **13,3** · deutan **12,3** · tritan **11,6**
> (ngưỡng đặt ra: 15 ở mắt thường, 10 ở mù màu)

Bảng Tableau 10 dùng tạm trước đó **không đạt**: với người mù màu lục — dạng
phổ biến nhất — Nông sản `#59A14F` và Phương tiện vận tải `#E15759` hiện ra
cùng một màu bùn, ΔE = **0,7**. Hai ngành này nằm cạnh nhau trong mọi treemap.

### 5.2 Việt Nam được làm nổi bằng hình dạng, không bằng màu

Đã thử tìm màu thứ 11 dành riêng cho Việt Nam. Không còn chỗ: mọi màu cam/đỏ
đủ khác 10 màu ngành ở mắt thường (ΔE 22–27) đều tụt xuống **ΔE 4–8** khi mô
phỏng mù màu. Chỉ màu đen còn đứng vững (ΔE 19,9). Nên Việt Nam = **viền đen
1,5px + nhãn in đậm**, và đường dày 2,2px trong biểu đồ đường (quyết định B12).

### 5.3 Cộng đồng mã hóa bằng độ sáng và hình dạng

Cùng một vấn đề, cùng một kết luận. Đã đo **7 bảng 3 màu ứng viên** (Paul Tol
high-contrast, Tol bright, Okabe–Ito và 4 biến thể). Tất cả đạt khoảng cách nội
bộ tốt ở mắt thường (ΔE 26–46), nhưng khoảng cách tới **màu ngành gần nhất**
khi mô phỏng mù màu tụt còn **ΔE 2,6–6,6** — tức trùng với một màu ngành.

Giải pháp: **3 nấc xám + 3 ký hiệu điểm**. Xám không có sắc độ nên mô phỏng mù
màu không làm nó đổi — cặp gần nhau nhất vẫn **ΔE 20,1** với cả protan, deutan
và tritan. Người mù màu hoàn toàn vẫn đọc được các hình mạng lưới.

### 5.4 Nếu một công cụ kiểm màu khác báo hỏng

Nhiều công cụ dùng thang **OKLab** thay vì **CIEDE2000**; hai thang cho hai con
số khác nhau cho cùng một cặp màu và không quy đổi được. Cặp hay bị báo nhất là
Điện tử `#88CCEE` ↔ Khác `#DDDDDD`: đo bằng CIEDE2000 thì ΔE = **18,9** ở mắt
thường và 14,9 / 18,2 / 23,5 ở protan / deutan / tritan — vượt xa ngưỡng.

Hai cảnh báo khác mà công cụ ngoài hay nêu — "dải độ sáng quá rộng" và "độ bão
hòa thấp" — là đặc tính cố hữu của thang Paul Tol muted, và style guide đã bù
bằng quy định **viền trắng 1px bắt buộc** cho bốn màu nhạt (`#DDCC77`, `#44AA99`,
`#88CCEE`, `#DDDDDD`) cùng nhãn chữ trực tiếp trên mảng.

---

## 6. Tái lập kết quả

```bash
python src/download_atlas.py        # tải dữ liệu thô, kiểm MD5
python src/check_raw_data.py        # cửa chặn, phải báo DAT
python src/build_intermediate.py    # sinh 5 file trung gian
python src/analyze_network.py       # thống kê mạng + bảng ngưỡng
python src/compute_metrics.py       # chỉ số mạng + độ ổn định cụm
python src/check_tree.py            # toàn vẹn cây HS92
python src/check_palette.py         # kiểm định bảng màu, thoát 1 nếu hỏng
python src/compare_mirror.py        # chênh lệch gương
```

Mỗi script vẽ đều **in ra bằng chứng đỡ cho tiêu đề của chính nó**. Đây là quy
ước của đồ án: không ai phải tin một câu tiêu đề, vì chạy lại script là thấy
các con số dựng nên câu đó.

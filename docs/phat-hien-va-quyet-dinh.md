# Phát hiện & quyết định — sổ ghi cho báo cáo

> Cập nhật **2026-09-24**. Đây là nơi giữ **những gì đáng đưa vào báo cáo** và
> **những gì đã chốt để khỏi cãi lại**. Khác với ba tài liệu kia:
>
> | File | Trả lời câu gì |
> |---|---|
> | `README.md` | chạy repo thế nào |
> | `docs/kien-thuc-nen-tang.md` | cần học gì trước khi hiểu đề tài |
> | `docs/nguon-du-lieu-vn-asean.md` | lấy dữ liệu ở đâu, đã lấy được gì |
> | **file này** | **viết gì vào báo cáo, và vì sao chọn như vậy** |
>
> Mọi con số dưới đây đều đã đo trên dữ liệu thật và tái lập được bằng các script
> trong `src/`. Không có con số nào chép từ tài liệu ngoài.

---

## A. Phát hiện dùng được trong báo cáo

### A1. Việt Nam đi lên thật, và đo được

`data/processed/country_year.csv` · `src/build_intermediate.py` chặng 5

| | 1995 | 2005 | 2015 | 2023 |
|---|---|---|---|---|
| **Việt Nam** | −1,00 (#181/211) | −0,12 (#132/224) | +0,24 (#109/230) | **+0,58 (#78/230)** |
| Thái Lan | +0,39 (#80) | +0,65 (#58) | +0,93 (#45) | +0,85 (#49) |
| Malaysia | +0,60 (#65) | +0,81 (#47) | +0,96 (#42) | +0,95 (#45) |
| Philippines | +0,11 (#101) | +0,27 (#97) | +0,58 (#77) | +0,76 (#61) |
| Indonesia | −0,14 (#120) | +0,17 (#108) | +0,28 (#104) | +0,28 (#101) |
| Singapore | +0,91 (#33) | +1,23 (#16) | +1,57 (#6) | +1,68 (#5) |

Ba câu đáng viết:

1. Việt Nam đi từ nhóm **14% cuối bảng** lên nhóm **34% đầu bảng** trong 28 năm.
2. Khoảng cách với Thái Lan thu từ **1,39** xuống **0,28** điểm.
3. Thái Lan **đạt đỉnh 2015 rồi đi ngang** (+0,93 → +0,85), trong khi Việt Nam
   vẫn đi lên. Hai đường đang thu hẹp, không phải Việt Nam đuổi theo một mục
   tiêu đang chạy.

⚠️ **Bắt buộc nêu mẫu số.** Số nước được xếp hạng đổi từ 211 (1995) lên 230
(2023). "Hạng 78" không đọc được nếu thiếu mẫu số — dùng cột `eci_n`.

### A2. Nhưng đi lên ở ĐÂU — căng thẳng trung tâm của báo cáo

`data/processed/country_product.csv` · Việt Nam, 2023

| Nhóm hàng HS2 | Xuất khẩu | **RCA** | **PCI** |
|---|---|---|---|
| Điện, điện tử và linh kiện | **115,4 tỷ** | 2,23 | **+0,93** |
| Máy móc công nghiệp | 39,8 tỷ | **0,95** | **+0,78** |
| Thiết bị quang học, đo lường | 11,3 tỷ | **0,91** | **+0,93** |
| Giày dép | 19,6 tỷ | **7,52** | −0,49 |
| Hàng may mặc (dệt kim) | 14,7 tỷ | 3,67 | −0,66 |
| Hàng may mặc (không dệt kim) | 14,2 tỷ | 3,29 | −0,87 |
| Cà phê, chè, gia vị | 4,5 tỷ | **4,21** | −1,38 |
| Đồ nội thất | 11,8 tỷ | 2,36 | +0,25 |

Đọc chéo hai cột cuối, và đây là **phát hiện trung tâm của cả đồ án**:

> **Lợi thế so sánh của Việt Nam mạnh nhất đúng ở nơi sản phẩm đơn giản nhất, và
> yếu nhất đúng ở nơi sản phẩm phức tạp nhất.**

Giày dép PCI −0,49 nhưng RCA **7,52**; cà phê PCI −1,38 mà RCA **4,21**. Ngược
lại, hai nhóm phức tạp nhất bảng — máy móc công nghiệp (PCI +0,78) và thiết bị
quang học (PCI +0,93) — đều có **RCA dưới 1**, tức Việt Nam hiện diện ở đó *ít
hơn* mức bình quân thế giới: **không có lợi thế so sánh nào cả.**

Điện tử là ngoại lệ đáng nói: PCI +0,93 và là nhóm xuất khẩu **lớn nhất** với
115,4 tỷ USD, nhưng RCA chỉ **2,23** — tức Việt Nam lớn trong điện tử gần như
đúng theo tỷ lệ điện tử lớn trong thương mại thế giới, chứ không vượt trội như
cách nước này vượt trội ở giày dép.

**Vì sao điều này quan trọng:** ECI ở A1 tính trên **xuất khẩu gộp**. Một nước
lắp ráp điện thoại được cộng trọn điểm phức tạp của chiếc điện thoại, bất kể giữ
lại bao nhiêu giá trị. Đường ECI dốc đứng của Việt Nam **một phần** đến từ 115,4
tỷ USD điện tử đó.

Hai bảng A1 và A2 đặt cạnh nhau là một lập luận hoàn chỉnh, và nó **không** nói
rằng Việt Nam không tiến bộ — nó nói rằng *chỉ số đo sự tiến bộ này có một điểm
mù, và ta biết điểm mù nằm ở đâu*. Giảng viên chấm chính cái đó.

🔬 Muốn **chứng minh** thay vì chỉ nêu nghi vấn thì cần dữ liệu giá trị gia tăng
(OECD TiVA hoặc ADB MRIO) — xem `nguon-du-lieu-vn-asean.md` §2. Ngoài tầm đồ án
này, nhưng nêu ra được là đủ.

### A3. Mạng lưới thương mại KHÔNG phải scale-free

`data/processed/network_stats.csv`, `degree_distribution.csv` · `src/analyze_network.py`

| | 1995 | 2023 |
|---|---|---|
| Nút / cạnh | 211 / 18.411 | 231 / 27.535 |
| Mật độ | 0,416 | **0,518** |
| Đối ứng | 0,824 | **0,837** |
| Gini trọng số cạnh | 0,955 | **0,957** |

Bậc xuất khẩu 2023 (số bạn hàng): min 0 · p25 62 · **trung vị 116** · p75 177 ·
p90 210 · max 226.

Các nước trải **gần như đều** trên toàn dải. Đo cụ thể: CCDF lệch khỏi một phân
bố đều hoàn toàn nhiều nhất **0,056**.

Ba hệ quả:

1. **Mật độ 51,8%** — hơn một nửa mọi cặp nước có giao dịch. Mạng xã hội hay
   mạng trích dẫn thường dưới 1%. Đây là lý do không thể vẽ thẳng 27.535 cạnh.
2. **Không có hub theo nghĩa tô-pô.** Không tồn tại nhóm nhỏ nối với tất cả
   trong khi phần còn lại nối với vài nước — vì gần như ai cũng nối với nhiều.
3. **Biểu đồ log-log của T09 sẽ không ra đường thẳng.** Nó đi ngang rồi rơi dốc
   đứng ở mép phải. **Đó không phải lỗi dữ liệu, đó là kết quả.** Phải nói rõ
   câu này trong báo cáo, kèm con số 0,056, nếu không người đọc sẽ tưởng vẽ sai.

### A4. Giá trị thì cực kỳ tập trung — và tập trung ổn định

`data/processed/threshold_coverage.csv` · năm 2023 (27.535 cạnh, 21,66 nghìn tỷ USD)

| Giữ lại | % số cạnh | % giá trị |
|---|---|---|
| top 100 cạnh | 0,36% | 43,0% |
| top 416 (quy tắc đã chốt) | 1,51% | 68,5% |
| top 1.000 | 3,63% | 83,5% |
| top 2.754 | 10,0% | 95,2% |

**Vứt 98,5% số cạnh vẫn giữ hơn 2/3 tổng giá trị thương mại thế giới.**

Gộp A3 với A4 ra câu kết luận gọn nhất về cấu trúc mạng lưới:

> **Cấu trúc trung tâm–ngoại vi của thương mại không nằm ở việc ai nối với ai,
> mà nằm ở việc luồng nào lớn.**

Và Gini **0,957 gần như đứng yên suốt 28 năm** (0,955 → 0,957) trong khi mạng
phình từ 18 nghìn lên 27,5 nghìn cạnh: toàn cầu hoá làm mạng **dày thêm** chứ
không làm giá trị **dàn đều hơn**. Đây là một câu đắt, vì nó phản trực giác.

### A5. Cái bẫy so sánh theo thời gian

Thương mại thế giới tăng **4,51 lần**: 4,80 nghìn tỷ USD (1995) → 21,66 nghìn tỷ
(2023). Nên một ngưỡng lọc tính bằng USD danh nghĩa đo hai năm bằng hai cái
thước:

| Năm | Ngưỡng cố định 10 tỷ USD | Quy tắc đã chốt (xem B4) |
|---|---|---|
| 1995 | **89 cạnh**, 49,5% giá trị, ASEAN 4/10 | 383 cạnh, 73,9%, ASEAN 10/10 |
| 2005 | 176 cạnh, 56,2%, ASEAN 5/10 | 406 cạnh, 70,2%, ASEAN 10/10 |
| 2015 | 270 cạnh, 61,6%, ASEAN 6/10 | 407 cạnh, 68,1%, ASEAN 10/10 |
| 2023 | 390 cạnh, 67,3%, ASEAN 8/10 | 416 cạnh, 67,8%, ASEAN 10/10 |

Cột giữa làm small multiples **đọc thành "thương mại mới xuất hiện sau 1995"**
trong khi sự thật là "thương mại lớn lên". Đây là một lỗi trực quan hoá kinh
điển và **đáng viết hẳn một đoạn trong báo cáo** — nó cho thấy nhóm hiểu rằng
lựa chọn kỹ thuật tạo ra thông điệp, chứ không trung tính.

---

### A6. Dữ liệu 2024 chưa đầy đủ — phát hiện được bằng cách nhìn chuỗi số

`data/processed/network_stats.csv` · kiểm chứng ở `data/atlas/cc_year.csv`

Số cạnh đứng rất yên suốt chín năm rồi rơi đúng ở năm cuối, trong khi tổng giá
trị thì bình thường:

| Năm | 2015 | 2020 | 2022 | 2023 | **2024** |
|---|---|---|---|---|---|
| Số cạnh | 27.323 | 27.003 | 27.489 | 27.535 | **25.754** |
| Mật độ | 0,519 | 0,513 | 0,517 | 0,518 | **0,485** |
| Tổng XK (nghìn tỷ USD) | 15,09 | 16,19 | 22,66 | 21,66 | 21,81 |

Giá trị đủ mà cặp nước thiếu → không phải thương mại co lại, mà là **dữ liệu
thiếu**. Kiểm thẳng ở file thô xác nhận:

```
VNM->ARE  2023  export = 6.582.537.191
VNM->ARE  2024  KHÔNG CÓ DÒNG NÀO
```

Tương tự Nga, Lào, Bangladesh, Ghana, Iraq. **Không nước nào biến mất hẳn** —
cả 231 nước đều có mặt cả hai năm — thiếu là thiếu từng **cặp**. 168 trong 231
nước mất bạn hàng khi sang 2024; UAE nặng nhất, 218 → 129. Dấu hiệu quen của
một bản phát hành tạm: nước chưa nộp số liệu cho Comtrade thì Atlas chỉ dựng
lại được phần nào từ báo cáo của đối tác.

**Hậu quả với riêng đề tài này:**

| Việt Nam | 2023 | 2024 |
|---|---|---|
| Xuất khẩu | 385,5 tỷ USD | 429,5 tỷ USD |
| **Số bạn hàng** | **166** | **129** |

37 bạn hàng biến mất mang theo **11,4 tỷ USD = 2,96%** xuất khẩu — trong đó có
**Lào**, một nước ASEAN, ngay giữa lát cắt Việt Nam–ASEAN. Để nguyên thì biểu đồ
đọc thành *"Việt Nam đang mất bạn hàng"*, ngược hẳn sự thật.

Dữ liệu cấp **nước × sản phẩm** thì gần như đủ (18.102 dòng năm 2024 so với
18.590 năm 2023, cùng 230 nước, tổng giá trị bình thường) — nên riêng treemap,
RCA, PCI, ECI vẽ trên 2024 vẫn được. Nhưng trộn hai năm trong một bài vi phạm
Checklist #18, nên cả đồ án dùng **một năm duy nhất: 2023**.

**Vì sao đáng viết vào báo cáo.** Đây là một phát hiện về *dữ liệu*, không phải
về thương mại — và nó cho thấy nhóm kiểm tra chuỗi số trước khi vẽ. Cách phát
hiện cũng đáng kể lại: không phải nhìn một năm, mà nhìn **hình dạng của cả
chuỗi**, thấy một cú gãy không khớp với bất kỳ sự kiện kinh tế nào, rồi lần
ngược về file thô để xác nhận.

---

## B. Quyết định đã chốt

Ghi lại kèm **lý do**, để sau này không ai phải mở lại tranh luận.

| # | Quyết định | Lý do |
|---|---|---|
| B1 | `REFERENCE_YEAR = 2023` | mọi con số một-năm lấy cùng năm, tránh báo cáo tự mâu thuẫn. **Không phải 2024** vì bản Atlas 2024 còn tạm — xem A6 |
| B2 | `is_focus` = **cả 10 nước ASEAN** | đề tài có lát cắt VN–ASEAN, không chỉ VN |
| B3 | `export_value = 0` → **loại** | không phải một cạnh, cũng không phải một dòng xuất khẩu |
| B4 | **Ngưỡng lọc:** `THRESHOLD_SHARE = 0.00046` + `FOCUS_TOPK = 3` | xem bên dưới |
| B5 | **Node-link KHÔNG dùng mũi tên** | đối ứng 0,84 → hướng cạnh gần như vô nghĩa, mũi tên chỉ gây rối |
| B6 | Giữ `USP`, `ANS` trong `nodes.csv` | để tái lập được con số cũ; `USP` không có luồng nào suốt 30 năm **và** vắng mặt khỏi file ECI — hai bằng chứng độc lập |
| B7 | `sector_color` hiện là **bảng màu tạm** | phải thay ở T04 bằng bảng an toàn với người mù màu |
| B8 | **Không commit dữ liệu thô** | Nguyên tắc #5 của nhóm; chỉ 3 bảng tra cứu nhỏ được whitelist |
| B9 | Dùng **Atlas**, không cần BACI | Atlas cũng hoà giải số liệu gương — ba file Atlas khớp nhau 0,000% |
| B10 | **Chuỗi thời gian dừng ở 2023** | `PROVISIONAL_YEARS = [2024]`; vẽ tiếp 2024 thì phải ghi rõ là số tạm — xem A6 |
| B11 | **Bảng màu 10 ngành: thang Tol muted, đổi Khoáng sản sang nâu đậm** | bảng Tableau 10 dùng tạm trước đó có Nông sản và Phương tiện vận tải trùng hẳn nhau với người mù lục (ΔE = 0,7). Bảng mới: ΔE nhỏ nhất 16,1 mắt thường, 11,6 qua cả ba dạng mù màu — `src/check_palette.py`, chi tiết ở `style-guide.md` |
| B12 | **Làm nổi Việt Nam bằng hình dạng, không bằng màu** | đã thử thêm màu thứ 11: mọi màu cam/đỏ khác 10 màu ngành ở mắt thường (ΔE 22–27) đều tụt xuống ΔE 4–8 khi mô phỏng mù màu. Viền đen 1,5px + nhãn đậm thay cho màu riêng |

### B4 chi tiết — quy tắc lọc cạnh

```
giữ cạnh  ⟺  export_value ≥ 0,046% × tổng xuất khẩu thế giới CỦA NĂM ĐÓ
             HOẶC  nằm trong top 3 luồng xuất / top 3 luồng nhập
                   lớn nhất của một nước ASEAN
```

Ba lý do, theo thứ tự quan trọng:

1. **Dùng tỷ lệ chứ không dùng USD cố định** → số cạnh ổn định **378–438 trên cả
   29 năm**, nên các panel của small multiples so sánh được với nhau (xem A5).
2. **Chọn đúng 0,046%** vì nó cho ra **9,96 tỷ USD** ở năm tham chiếu — sát con số
   10 tỷ nhóm đã đo và ghi trong đề bài. Năm tham chiếu **không đổi thước đo**;
   chỉ các năm còn lại được quy về cùng thước.

   *Con số 0,046% được chọn khi năm tham chiếu còn là 2024 (ra 10,03 tỷ). Đổi
   sang 2023 nó ra 9,96 tỷ — lệch 0,7%, coi như trùng — nên quy tắc T10 sống
   nguyên vẹn qua lần đổi năm, không phải hiệu chỉnh lại.*
3. **Bảo hiểm ASEAN là bắt buộc, không phải trang trí.** Ngưỡng tương đối một
   mình **xoá Việt Nam khỏi năm 1995** — đúng 0 cạnh — và xoá Brunei, Lào,
   Myanmar khỏi hầu hết các năm. Với đề tài tên là *"vị trí của Việt Nam"* thì đó
   là lỗi chí mạng. Giá phải trả: **+23 cạnh** (393 → 416), **+0,36 điểm phần
   trăm** giá trị.

**Phương án đã cân nhắc và loại** (đủ 21 dòng trong `threshold_coverage.csv`):

- *Ngưỡng tuyệt đối* mọi mức — không so sánh được giữa các năm.
- *Mỗi nước giữ k luồng lớn nhất* — giữ đủ 231 nút nhưng độ phủ giá trị quá thấp
  (k=3 chỉ 40,5%), và k=10 mới đạt 66% thì đã 2.289 cạnh, quá dày để vẽ.

---

## C. Bẫy kỹ thuật đã vấp — đừng vấp lại

| Bẫy | Hậu quả | Cách tránh |
|---|---|---|
| `hash()` của chuỗi trong Python | **bị ngẫu nhiên hoá theo từng tiến trình** (PYTHONHASHSEED); `random.seed()` KHÔNG cứu được vì `hash()` không dùng tới nó. Từng sinh id trùng: IND và RUS cùng 779 | không bao giờ dùng `hash()` để sinh ID ổn định — đánh số theo vị trí |
| File khoá Excel `~$ten.xlsx` | Windows khoá file khi workbook đang mở → `git add -A` **hỏng cả lệnh** với "Permission denied", không phải chỉ bỏ qua một file | đã thêm `~$*` vào `.gitignore` |
| File tải về bị cắt giữa chừng | mất trọn các nước ở cuối thứ tự sắp xếp — **từng mất Hoa Kỳ** mà không ai biết | `src/check_raw_data.py` chạy trước mọi thứ, là cửa chặn |
| Tốc độ tải Dataverse ~30 KB/s | file HS6 song phương 12,2 GB ≈ 113 giờ | xem bảng khả thi ở `nguon-du-lieu-vn-asean.md` §7 |
| Dataverse API | danh sách file nằm ở `latestVersion.files`, **không phải** `dataFiles`; WAF trả 403 cho User-Agent mặc định của urllib | dùng UA bắt đầu bằng `Mozilla/` |

### Bốn phép kiểm định đang chạy tự động

Đáng nêu trong báo cáo ở phần phương pháp — nó chứng minh dữ liệu được kiểm chứ
không phải tin bừa:

1. **ECI đã chuẩn hoá** — mỗi năm trung bình ≈ 0, độ lệch chuẩn ≈ 1 trên toàn bộ
   các nước. Là tính chất của cách tính, nên đọc lệch cột hay mất dòng là hai số
   này trồi ngay. Đo được: `|trung bình| ≤ 0,076`, `|độ lệch chuẩn − 1| ≤ 0,054`.
2. **Trung bình RCA có trọng số = 1** — tính chất toán học của công thức Balassa.
   Đo được: lệch `1,0e-15`.
3. **Đối chiếu chéo ba file** — `cc_year` (theo cặp nước), `cp_year_hs2` (theo
   nước × sản phẩm), `hs92_country_year` (theo nước) đo cùng một nền thương mại
   từ ba góc. Tổng xuất khẩu thế giới 2024 khớp nhau **0,000%**.
4. **Cây sản phẩm HS92** đúng `{1: 10, 2: 97, 4: 1.243, 6: 5.040}` nút mỗi tầng,
   0 nút mồ côi.

---

## D. Phải nói thật trong báo cáo

Năm hạn chế. Nêu ra thì được điểm trung thực; giấu đi mà bị hỏi thì mất nhiều hơn.

1. **Dữ liệu dừng ở 2023, không phải 2024.** Bản Atlas 2024 còn tạm: thiếu 1.781
   cặp nước, riêng Việt Nam mất 37 bạn hàng trị giá 11,4 tỷ USD. Nói thẳng điều
   này trong phần Phương pháp luận — nó cho thấy nhóm **kiểm tra dữ liệu** chứ
   không chỉ nhận về rồi vẽ. Xem A6.
2. **ECI tính trên xuất khẩu gộp** → thưởng điểm cho việc lắp ráp hàng phức tạp
   bất kể giữ lại bao nhiêu giá trị. Xem A2.
3. **Node-link vứt 98,5% số cạnh.** Nó **không** đọc được là "bản đồ thương mại
   toàn cầu", mà là *"bản đồ các luồng thương mại lớn, cộng chỗ đứng của ASEAN
   trong đó"*. Ai muốn nhìn phần đuôi phải xem ma trận kề (T16) — ma trận chịu
   được nhiều cạnh hơn hẳn node-link.
4. **Dữ liệu dừng ở HS2 (97 nhóm hàng).** Chi tiết hơn cần file HS4 452 MB
   (~4,2 giờ tải). "Điện, điện tử và linh kiện" gộp cả chip lẫn dây điện.
5. **Không có dữ liệu giá trị gia tăng.** Mọi nhận định về "giữ lại bao nhiêu
   giá trị" trong báo cáo là **suy luận từ RCA × PCI**, không phải đo trực tiếp.

---

## E. Mạch chuyện đề xuất cho báo cáo

Bốn nhịp, mỗi nhịp đã có sẵn số liệu:

1. **Thế giới nối nhau dày hơn ta tưởng** — mật độ 51,8%, đối ứng 0,84. Nhưng
   giá trị thì cực lệch: Gini 0,957, top 1,5% cạnh giữ 68,5% giá trị. → A3, A4
2. **Việt Nam trèo lên trong bảng xếp hạng đó** — ECI #181/211 → #78/230, thu
   khoảng cách với Thái Lan từ 1,39 xuống 0,28. → A1
3. **Nhìn kỹ thì trèo bằng gì** — RCA 7,52 ở giày dép (PCI −0,49) và 4,21 ở cà
   phê (PCI −1,38), nhưng **dưới 1** ở máy móc công nghiệp (PCI +0,78) và thiết
   bị quang học (PCI +0,93). Điện tử là 115,4 tỷ USD mà RCA chỉ 2,23. → A2
4. **Vậy con số nói gì và không nói gì** — ECI đo rổ hàng gộp, nên nó đo *cái gì
   đi qua Việt Nam*, chưa hẳn là *cái gì ở lại Việt Nam*. → D2, D5

Nhịp 4 mới là chỗ tách bài khá khỏi bài giỏi.

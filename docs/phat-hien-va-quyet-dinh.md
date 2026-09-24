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

| | 1995 | 2005 | 2015 | 2024 |
|---|---|---|---|---|
| **Việt Nam** | −1,00 (#181/211) | −0,12 (#132/224) | +0,24 (#109/230) | **+0,67 (#70/230)** |
| Thái Lan | +0,39 (#80) | +0,65 (#58) | +0,93 (#45) | +0,81 (#54) |
| Malaysia | +0,60 (#65) | +0,81 (#47) | +0,96 (#42) | +0,86 (#47) |
| Philippines | +0,11 (#101) | +0,27 (#97) | +0,58 (#77) | +0,74 (#60) |
| Indonesia | −0,14 (#120) | +0,17 (#108) | +0,28 (#104) | +0,22 (#115) |
| Singapore | +0,91 (#33) | +1,23 (#16) | +1,57 (#6) | +1,52 (#7) |

Ba câu đáng viết:

1. Việt Nam đi từ nhóm **14% cuối bảng** lên nhóm **30% đầu bảng** trong 29 năm.
2. Khoảng cách với Thái Lan thu từ **1,39** xuống **0,14** điểm.
3. Thái Lan **đạt đỉnh 2015 rồi đi xuống** (+0,93 → +0,81). Hai đường đang cắt
   nhau, không phải Việt Nam đuổi theo một mục tiêu đang chạy.

⚠️ **Bắt buộc nêu mẫu số.** Số nước được xếp hạng đổi từ 211 (1995) lên 230
(2024). "Hạng 70" không đọc được nếu thiếu mẫu số — dùng cột `eci_n`.

### A2. Nhưng đi lên ở ĐÂU — căng thẳng trung tâm của báo cáo

`data/processed/country_product.csv` · Việt Nam, 2024

| Nhóm hàng HS2 | Xuất khẩu | **RCA** | **PCI** |
|---|---|---|---|
| Điện, điện tử và linh kiện | **144,9 tỷ** | 2,45 | **+0,90** |
| Máy móc công nghiệp | 78,0 tỷ | 1,59 | **+0,78** |
| Giày dép | 26,7 tỷ | **9,04** | −0,41 |
| Hàng may mặc (dệt kim) | 15,9 tỷ | 3,62 | −0,61 |
| Hàng may mặc (không dệt kim) | 15,7 tỷ | 3,24 | −0,80 |
| Đồ nội thất | 15,6 tỷ | 2,79 | +0,27 |

Đọc chéo hai cột cuối, và đây là **phát hiện trung tâm của cả đồ án**:

> **Lợi thế so sánh của Việt Nam mạnh nhất đúng ở nơi sản phẩm đơn giản nhất, và
> yếu nhất đúng ở nơi sản phẩm phức tạp nhất.**

Giày dép PCI −0,41 nhưng RCA **9,04** — Việt Nam hiện diện gấp 9 lần mức bình
quân thế giới. Điện tử PCI +0,90, là nhóm xuất khẩu **lớn nhất** với 144,9 tỷ
USD, nhưng RCA chỉ **2,45** — tức Việt Nam lớn trong điện tử gần như đúng theo
tỷ lệ điện tử lớn trong thương mại thế giới, chứ không vượt trội.

**Vì sao điều này quan trọng:** ECI ở A1 tính trên **xuất khẩu gộp**. Một nước
lắp ráp điện thoại được cộng trọn điểm phức tạp của chiếc điện thoại, bất kể giữ
lại bao nhiêu giá trị. Đường ECI dốc đứng của Việt Nam **một phần** đến từ 144,9
tỷ USD điện tử đó.

Hai bảng A1 và A2 đặt cạnh nhau là một lập luận hoàn chỉnh, và nó **không** nói
rằng Việt Nam không tiến bộ — nó nói rằng *chỉ số đo sự tiến bộ này có một điểm
mù, và ta biết điểm mù nằm ở đâu*. Giảng viên chấm chính cái đó.

🔬 Muốn **chứng minh** thay vì chỉ nêu nghi vấn thì cần dữ liệu giá trị gia tăng
(OECD TiVA hoặc ADB MRIO) — xem `nguon-du-lieu-vn-asean.md` §2. Ngoài tầm đồ án
này, nhưng nêu ra được là đủ.

### A3. Mạng lưới thương mại KHÔNG phải scale-free

`data/processed/network_stats.csv`, `degree_distribution.csv` · `src/analyze_network.py`

| | 1995 | 2024 |
|---|---|---|
| Nút / cạnh | 211 / 18.411 | 231 / 25.754 |
| Mật độ | 0,416 | **0,485** |
| Đối ứng | 0,824 | **0,843** |
| Gini trọng số cạnh | 0,955 | **0,956** |

Bậc xuất khẩu 2024 (số bạn hàng): min 0 · p25 55 · **trung vị 104** · p75 170 ·
p90 209 · max 228.

Các nước trải **gần như đều** trên toàn dải. Đo cụ thể: CCDF lệch khỏi một phân
bố đều hoàn toàn nhiều nhất **0,046**.

Ba hệ quả:

1. **Mật độ 48,5%** — gần một nửa mọi cặp nước có giao dịch. Mạng xã hội hay
   mạng trích dẫn thường dưới 1%. Đây là lý do không thể vẽ thẳng 25.754 cạnh.
2. **Không có hub theo nghĩa tô-pô.** Không tồn tại nhóm nhỏ nối với tất cả
   trong khi phần còn lại nối với vài nước — vì gần như ai cũng nối với nhiều.
3. **Biểu đồ log-log của T09 sẽ không ra đường thẳng.** Nó đi ngang rồi rơi dốc
   đứng ở mép phải. **Đó không phải lỗi dữ liệu, đó là kết quả.** Phải nói rõ
   câu này trong báo cáo, kèm con số 0,046, nếu không người đọc sẽ tưởng vẽ sai.

### A4. Giá trị thì cực kỳ tập trung — và tập trung ổn định

`data/processed/threshold_coverage.csv` · năm 2024

| Giữ lại | % số cạnh | % giá trị |
|---|---|---|
| top 100 cạnh | 0,4% | 43,5% |
| top 347 | 1,3% | 65,9% |
| top 1.000 | 3,9% | 84,1% |
| top 2.575 | 10,0% | 94,9% |

**Vứt 98,7% số cạnh vẫn giữ 2/3 tổng giá trị thương mại thế giới.**

Gộp A3 với A4 ra câu kết luận gọn nhất về cấu trúc mạng lưới:

> **Cấu trúc trung tâm–ngoại vi của thương mại không nằm ở việc ai nối với ai,
> mà nằm ở việc luồng nào lớn.**

Và Gini **0,956 gần như đứng yên suốt 30 năm** (0,955 → 0,956) trong khi mạng
phình từ 18 nghìn lên 26 nghìn cạnh: toàn cầu hoá làm mạng **dày thêm** chứ
không làm giá trị **dàn đều hơn**. Đây là một câu đắt, vì nó phản trực giác.

### A5. Cái bẫy so sánh theo thời gian

Thương mại thế giới tăng **4,54 lần**: 4,80 nghìn tỷ USD (1995) → 21,81 nghìn tỷ
(2024). Nên một ngưỡng lọc tính bằng USD danh nghĩa đo hai năm bằng hai cái
thước:

| Năm | Ngưỡng cố định 10 tỷ USD | Quy tắc đã chốt (xem B4) |
|---|---|---|
| 1995 | **89 cạnh**, 49,5% giá trị, ASEAN 4/10 | 383 cạnh, 73,9%, ASEAN 10/10 |
| 2005 | 176 cạnh, 56,2%, ASEAN 5/10 | 406 cạnh, 70,2%, ASEAN 10/10 |
| 2015 | 270 cạnh, 61,6%, ASEAN 6/10 | 407 cạnh, 68,1%, ASEAN 10/10 |
| 2024 | 385 cạnh, 67,7%, ASEAN 7/10 | 408 cạnh, 68,1%, ASEAN 10/10 |

Cột giữa làm small multiples **đọc thành "thương mại mới xuất hiện sau 1995"**
trong khi sự thật là "thương mại lớn lên". Đây là một lỗi trực quan hoá kinh
điển và **đáng viết hẳn một đoạn trong báo cáo** — nó cho thấy nhóm hiểu rằng
lựa chọn kỹ thuật tạo ra thông điệp, chứ không trung tính.

---

## B. Quyết định đã chốt

Ghi lại kèm **lý do**, để sau này không ai phải mở lại tranh luận.

| # | Quyết định | Lý do |
|---|---|---|
| B1 | `REFERENCE_YEAR = 2024` | mọi con số một-năm lấy cùng năm, tránh báo cáo tự mâu thuẫn |
| B2 | `is_focus` = **cả 10 nước ASEAN** | đề tài có lát cắt VN–ASEAN, không chỉ VN |
| B3 | `export_value = 0` → **loại** | không phải một cạnh, cũng không phải một dòng xuất khẩu |
| B4 | **Ngưỡng lọc:** `THRESHOLD_SHARE = 0.00046` + `FOCUS_TOPK = 3` | xem bên dưới |
| B5 | **Node-link KHÔNG dùng mũi tên** | đối ứng 0,84 → hướng cạnh gần như vô nghĩa, mũi tên chỉ gây rối |
| B6 | Giữ `USP`, `ANS` trong `nodes.csv` | để tái lập được con số cũ; `USP` không có luồng nào suốt 30 năm **và** vắng mặt khỏi file ECI — hai bằng chứng độc lập |
| B7 | `sector_color` hiện là **bảng màu tạm** | phải thay ở T04 bằng bảng an toàn với người mù màu |
| B8 | **Không commit dữ liệu thô** | Nguyên tắc #5 của nhóm; chỉ 3 bảng tra cứu nhỏ được whitelist |
| B9 | Dùng **Atlas**, không cần BACI | Atlas cũng hoà giải số liệu gương — ba file Atlas khớp nhau 0,000% |

### B4 chi tiết — quy tắc lọc cạnh

```
giữ cạnh  ⟺  export_value ≥ 0,046% × tổng xuất khẩu thế giới CỦA NĂM ĐÓ
             HOẶC  nằm trong top 3 luồng xuất / top 3 luồng nhập
                   lớn nhất của một nước ASEAN
```

Ba lý do, theo thứ tự quan trọng:

1. **Dùng tỷ lệ chứ không dùng USD cố định** → số cạnh ổn định **378–438 trên cả
   30 năm**, nên các panel của small multiples so sánh được với nhau (xem A5).
2. **Chọn đúng 0,046%** vì nó cho ra 10,03 tỷ USD ở năm 2024 — trùng con số 10 tỷ
   nhóm đã đo và ghi trong đề bài. Năm tham chiếu **không đổi**; chỉ các năm còn
   lại được quy về cùng thước đo.
3. **Bảo hiểm ASEAN là bắt buộc, không phải trang trí.** Ngưỡng tương đối một
   mình **xoá Việt Nam khỏi năm 1995** — đúng 0 cạnh — và xoá Brunei, Lào,
   Myanmar khỏi hầu hết các năm. Với đề tài tên là *"vị trí của Việt Nam"* thì đó
   là lỗi chí mạng. Giá phải trả: **+23 cạnh** (385 → 408), **+0,4 điểm phần
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

Bốn hạn chế. Nêu ra thì được điểm trung thực; giấu đi mà bị hỏi thì mất nhiều hơn.

1. **ECI tính trên xuất khẩu gộp** → thưởng điểm cho việc lắp ráp hàng phức tạp
   bất kể giữ lại bao nhiêu giá trị. Xem A2.
2. **Node-link vứt 98,4% số cạnh.** Nó **không** đọc được là "bản đồ thương mại
   toàn cầu", mà là *"bản đồ các luồng thương mại lớn, cộng chỗ đứng của ASEAN
   trong đó"*. Ai muốn nhìn phần đuôi phải xem ma trận kề (T16) — ma trận chịu
   được nhiều cạnh hơn hẳn node-link.
3. **Dữ liệu dừng ở HS2 (97 nhóm hàng).** Chi tiết hơn cần file HS4 452 MB
   (~4,2 giờ tải). "Điện, điện tử và linh kiện" gộp cả chip lẫn dây điện.
4. **Không có dữ liệu giá trị gia tăng.** Mọi nhận định về "giữ lại bao nhiêu
   giá trị" trong báo cáo là **suy luận từ RCA × PCI**, không phải đo trực tiếp.

---

## E. Mạch chuyện đề xuất cho báo cáo

Bốn nhịp, mỗi nhịp đã có sẵn số liệu:

1. **Thế giới nối nhau dày hơn ta tưởng** — mật độ 48,5%, đối ứng 0,84. Nhưng
   giá trị thì cực lệch: Gini 0,956, top 1,3% cạnh giữ 66% giá trị. → A3, A4
2. **Việt Nam trèo lên trong bảng xếp hạng đó** — ECI #181/211 → #70/230, gần
   bắt kịp Thái Lan. → A1
3. **Nhìn kỹ thì trèo bằng gì** — RCA mạnh nhất ở giày dép (9,04, PCI −0,41),
   yếu nhất ở điện tử (2,45, PCI +0,90) dù điện tử là 144,9 tỷ USD. → A2
4. **Vậy con số nói gì và không nói gì** — ECI đo rổ hàng gộp, nên nó đo *cái gì
   đi qua Việt Nam*, chưa hẳn là *cái gì ở lại Việt Nam*. → D1, D4

Nhịp 4 mới là chỗ tách bài khá khỏi bài giỏi.

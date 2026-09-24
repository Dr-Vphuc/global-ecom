# T04 — Hệ thống thị giác cho cả đồ án

Bảng màu, font, cỡ hình, quy ước nhãn. Mọi con số trong file này do
`python src/check_palette.py` đo ra, không phải nhận xét bằng mắt.

Hằng số dùng trong code nằm ở `src/reference_data.py`:
`SECTOR_PALETTE`, `SECTOR_TEXT_ON_FILL`, `FONT_STACK`, `FONT_SIZES`,
`FIG_*`, `SEQUENTIAL_SCALE`, `HIGHLIGHT_*`. **Đừng chép mã hex vào code
biểu đồ — import từ đó.**

---

## 1. Bảng màu 10 ngành cấp 1 HS92

| # | Ngành | Hex | Chữ đè lên | Tương phản vs trắng | vs đen |
|---|---|---|---|---|---|
| 1 | Dệt may, giày dép, nội thất | `#CC6677` | đen | 3,66 | 5,73 |
| 2 | Nông sản, gỗ và giấy | `#117733` | trắng | 5,66 | 3,71 |
| 3 | Đá, thủy tinh, gốm sứ | `#DDCC77` | đen | 1,62 ⚠️ | 12,98 |
| 4 | Khoáng sản và nhiên liệu | `#5D4037` | trắng | 9,32 | 2,25 |
| 5 | Kim loại | `#332288` | trắng | 12,17 | 1,73 |
| 6 | Hóa chất và nhựa | `#AA4499` | trắng | 5,26 | 4,00 |
| 7 | Phương tiện vận tải | `#999933` | đen | 3,02 | 6,96 |
| 8 | Máy móc và thiết bị | `#44AA99` | đen | 2,82 ⚠️ | 7,46 |
| 9 | Điện tử | `#88CCEE` | đen | 1,76 ⚠️ | 11,92 |
| 10 | Khác | `#DDDDDD` | đen | 1,36 ⚠️ | 15,46 |

⚠️ = tương phản với nền trắng dưới 3:1. **Bốn màu này vẫn dùng được**, nhưng
mảng tô phải có **viền trắng 1px** mới thấy được mép trên nền trắng. Đừng vẽ
đường mảnh 1px bằng bốn màu này.

Cột "Chữ đè lên" đã tính sẵn — mọi cặp đạt WCAG ≥ 4,5:1, mức đủ cho chữ
thường. Dùng `SECTOR_TEXT_ON_FILL[sector_id]`, đừng đoán.

---

## 2. Vì sao đổi bảng màu — bảng cũ **hỏng thật**, không phải hỏng cảm tính

Bảng dùng tạm trước đây là Tableau 10. Đem mô phỏng mù màu thì:

| Với người… | Hai ngành bị trùng | Nhìn thành | ΔE |
|---|---|---|---|
| **deutan** (mù lục) | Nông sản `#59A14F` ↔ Phương tiện `#E15759` | `#9B8E55` / `#9D9056` | **0,7** |
| **protan** (mù đỏ) | Đá `#9C755F` ↔ Phương tiện `#E15759` | `#80785D` / `#7A7358` | **2,1** |

ΔE ≈ 1 là ngưỡng mắt người *vừa mới* nhận ra hai màu khác nhau khi đặt sát
nhau. ΔE = 0,7 nghĩa là **cùng một màu**. Deutan là dạng mù màu phổ biến nhất
(khoảng 6% nam giới), và Nông sản với Phương tiện vận tải nằm cạnh nhau trong
mọi treemap của đồ án. Đây đúng là mục #13 của Checklist nộp bài.

**Bảng mới đo được:**

| Nhìn bằng | Cặp gần nhau nhất | ΔE | Ngưỡng |
|---|---|---|---|
| Mắt thường | Đá ↔ Phương tiện vận tải | **16,1** | ≥ 15 |
| protan (mù đỏ) | Kim loại ↔ Hóa chất | **13,3** | ≥ 10 |
| deutan (mù lục) | Nông sản ↔ Khoáng sản | **12,3** | ≥ 10 |
| tritan (mù lam) | Dệt may ↔ Hóa chất | **11,6** | ≥ 10 |

Nền của bảng mới là thang **"muted" của Paul Tol** (9 màu, thiết kế sẵn cho
mù màu), đổi ô Khoáng sản sang nâu đậm `#5D4037` — vừa hợp nghĩa (than, dầu,
quặng) vừa đẩy ΔE mắt thường từ 15,0 lên 16,1. Ô "Khác" dùng xám nhạt để nó
tự chìm xuống, vì đó là nhóm gộp, không phải một ngành thật.

### Cách đo — để ai muốn kiểm lại thì kiểm được

- **Mô phỏng mù màu**: ma trận Machado, Oliveira & Fernandes (2009), mức nặng
  nhất. Nhân trên **RGB tuyến tính**, không nhân thẳng trên giá trị sRGB —
  nhân sai chỗ này là ra kết quả sai.
- **Khoảng cách màu**: CIEDE2000 trong không gian CIELAB, chuẩn trắng D65.
  Không dùng khoảng cách Euclid trên RGB: RGB không tuyến tính với mắt người,
  đo ra số vô nghĩa.
- **Tương phản**: công thức độ chói tương đối của WCAG 2.1.
- Toàn bộ nằm trong `src/check_palette.py`, chỉ dùng thư viện chuẩn, chạy
  xong thoát mã 1 nếu có tiêu chí không đạt.

### Một phương án đã thử rồi bỏ

Định làm thêm bản "mực" — mỗi ngành một màu đậm hơn, ép tất cả cùng đạt
tương phản 4,5:1 với nền trắng, để vẽ đường mảnh. **Hỏng**: ép mọi màu về
cùng một mức sáng thì mất luôn chênh lệch độ sáng, mà đó chính là thứ giúp
người mù màu phân biệt. ΔE nhỏ nhất tụt từ **11,6 xuống 2,1**.

→ Bài học ghi lại: bảng màu định tính sống được **nhờ** chênh lệch độ sáng.
Đừng san phẳng nó.

---

## 3. Quy tắc dùng màu

1. **Màu = ngành hàng. Chỉ thế thôi.** Không dùng lại 10 màu này để chỉ vùng
   địa lý, cụm Louvain hay bất cứ thứ gì khác trong cùng một bài.
2. **Mảng tô luôn có viền trắng 1px.** Bắt buộc với bốn màu nhạt, nên làm với
   cả mười cho đồng bộ.
3. **Làm nổi Việt Nam bằng hình dạng, không bằng màu.**
   Đã thử thêm màu thứ 11: mọi màu cam/đỏ đủ khác 10 màu ngành ở mắt thường
   (ΔE 22–27) đều tụt xuống **ΔE 4–8** khi mô phỏng mù màu. Chỉ màu đen còn
   đứng vững (ΔE 19,9). Nên quy ước là:

   | | |
   |---|---|
   | Nút / ô của Việt Nam | viền đen 1,5px (`HIGHLIGHT_STROKE`) |
   | Nhãn Việt Nam | in đậm |
   | Đường của Việt Nam | dày 2,2px, các nước khác 1,0px |

   Kênh màu để dành cho ngành hàng. Việt Nam nhận kênh khác.
4. **Thang tuần tự** (ma trận kề T16, bản đồ nhiệt): `SEQUENTIAL_SCALE`,
   `#FFFFE5 → #FEE391 → #FE9929 → #CC4C02 → #662506`. Thứ tự nằm ở độ sáng
   (L* 99 → 91 → 72 → 50 → 24) nên người mù màu vẫn đọc đúng thứ tự.
   ⚠️ Không đặt thang này chung một hình với chú giải 10 ngành — nấc `#FE9929`
   nằm gần màu ngành Đá và Phương tiện vận tải.
5. **Quá 10 nhóm thì không tô màu nữa.** Gộp phần đuôi vào "Khác", hoặc đổi
   sang xếp hạng / vị trí thay vì màu.

---

## 4. Font và cỡ chữ

```python
FONT_STACK = ["Segoe UI", "Arial", "DejaVu Sans"]
```

Thứ tự là thứ tự ưu tiên. **DejaVu Sans đi kèm sẵn trong matplotlib**, nên
máy nào cũng có — kể cả máy không phải Windows. Đã kiểm cả bốn font (thêm
Tahoma) với 19 ký tự có dấu tiếng Việt khó nhất (ế ữ ợ ằ ẵ ọ ỹ Đ …): **đủ hết**,
không font nào làm mất dấu hay hiện ô vuông.

| Thành phần | pt |
|---|---|
| Tiêu đề (câu nói kết luận) | 13 |
| Dòng phụ: năm, đơn vị, nguồn | 10 |
| Nhãn trục | 9 |
| Số trên trục | 8 |
| Chú giải | 9 |
| Chú thích trong hình | 8 |
| Dòng nguồn dưới cùng | 7 |

Cỡ này tính cho hình rộng 6,30 inch. Phóng to thu nhỏ hình thì **phải** đổi
cỡ chữ theo, đừng để matplotlib tự co.

---

## 5. Kích thước hình

Khổ A4 dọc, lề 2,5 cm → vùng chữ rộng **16 cm = 6,30 inch**.

| | inch | dùng cho |
|---|---|---|
| `FIG_WIDTH_FULL` | 6,30 | hình chạy hết chiều ngang trang |
| `FIG_WIDTH_HALF` | 3,05 | hai hình đặt cạnh nhau |
| `FIG_HEIGHT_DEFAULT` | 3,90 | chiều cao mặc định |
| `FIG_DPI_SCREEN` | 200 | bản xem trên màn hình |
| `FIG_DPI_PRINT` | 300 | bản nộp |

Ma trận kề (T16) là ngoại lệ: vuông, 6,30 × 6,30.

---

## 6. Quy ước nhãn

1. **Tiêu đề nói KẾT LUẬN, không nói tên biểu đồ.**
   ✅ "Việt Nam mạnh nhất ở nhóm hàng ít phức tạp nhất"
   ❌ "Biểu đồ phân tán RCA và PCI của Việt Nam năm 2023"
2. **Dòng phụ ngay dưới tiêu đề** ghi: năm, đơn vị, phạm vi.
   Ví dụ: *"Xuất khẩu 2023, tỷ USD, 97 nhóm hàng HS92 cấp 2"*.
3. **Số theo kiểu Việt Nam**: dấu phẩy thập phân, dấu chấm phân nhóm nghìn —
   `27.535 cạnh`, `385,5 tỷ USD`, `0,518`. Không viết `27,535` hay `385.5`.
4. **Đơn vị tiền**: dưới 1.000 tỷ thì "tỷ USD", trên thì "nghìn tỷ USD".
   Không dùng "billion", "trillion", "tr.USD".
5. **Nhãn đặt thẳng vào hình** thay cho chú giải, khi còn chỗ. Chú giải bắt
   người đọc liếc qua liếc lại.
6. **Dòng nguồn dưới cùng mọi hình**:
   *"Nguồn: Atlas of Economic Complexity (Harvard), số liệu 2023."*
   Nếu hình vẽ từ `data/mock/` thì ghi **"DỮ LIỆU GIẢ — chưa dùng được"**
   ngay trên hình, chữ đỏ. Không được quên rồi đem nộp nhầm.
7. **Không có mũi tên trong node-link** — quyết định B5, vì đối ứng 0,84 nên
   mũi tên chỉ làm rối mà gần như không thêm thông tin.

---

## 7. Kiểm trước khi đưa một hình vào báo cáo

- [ ] Màu lấy từ `SECTOR_PALETTE`, không chép hex vào code biểu đồ
- [ ] Mảng tô có viền trắng 1px
- [ ] Tiêu đề là một câu nói kết luận
- [ ] Có năm, có đơn vị, có dòng nguồn
- [ ] Số viết theo kiểu Việt Nam
- [ ] Việt Nam được làm nổi bằng viền / độ dày, không bằng màu riêng
- [ ] Nếu là dữ liệu giả: đã ghi cảnh báo lên hình
- [ ] Chữ nhỏ nhất trong hình ≥ 7pt sau khi xuất

Đổi bảng màu thì chạy lại `python src/check_palette.py` **và**
`python src/build_intermediate.py` (cột `sector_color` trong `tree.csv` lấy
từ đó).

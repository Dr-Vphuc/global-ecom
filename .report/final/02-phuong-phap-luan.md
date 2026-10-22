# 2. Phương pháp luận

> **Việc T25.** Số hiệu mục `2` là tạm — T27 ráp báo cáo mới chốt thứ tự. Mọi con
> số trong phần này đều đo lại được bằng một lệnh ghi ngay cạnh nó; không có con
> số nào chép từ tài liệu ngoài. Danh sách lệnh đầy đủ ở §2.12.
>
> **File phân công dự tính 2–3 trang, bản này dài hơn** (5.728 từ, 12 tiểu mục) vì
> nó là **bản gốc đầy đủ**, chỗ để T23 rà soát và T29 lấy câu trả lời phản biện.
> Khi T27 ráp báo cáo và cần cắt về 2–3 trang thì cắt theo đúng thứ tự này:
>
> - **Giữ trong thân báo cáo:** §2.2 nguồn dữ liệu · §2.3 vì sao 2023 · §2.5 chỉ số
>   nào tự tính · §2.7 hai đồ thị (giữ bảng đổi dấu, bỏ phần 21 phương án) ·
>   §2.11 hạn chế.
> - **Chuyển sang mục Đề xuất:** §2.10 — quy tắc chọn và phép thử lại trên 2015 là
>   lập luận của đề xuất, không phải của phương pháp.
> - **Chuyển sang phụ lục:** §2.4 bảng 10 file · §2.6 sáu cửa kiểm · §2.8 cây HS92
>   · §2.9 quy ước thị giác · §2.12 lệnh tái lập.
>
> **Ghi chú về phụ thuộc:** file phân công ghi T25 phụ thuộc **T08** (đối chiếu
> Atlas với BACI và Comtrade). Phụ thuộc đó **đã được bỏ** từ quyết định **B9**:
> ba file Atlas tự khớp nhau **0,000%**, nên không cần nguồn thứ hai để đối chứng —
> xem §2.2. T08 vẫn còn đó như một việc *nên có nếu có tài khoản*, không phải việc
> chặn T25.

---

## 2.1 Phần này phải trả lời ba câu

Một bài tư vấn chỉ đáng tin bằng đúng phần phương pháp của nó. Ba câu người nghe
sẽ hỏi, và phần này phải trả lời trước khi bị hỏi:

1. **Số ở đâu ra?** → §2.2 – §2.5
2. **Vì sao tin được?** → §2.6 – §2.10
3. **Chỗ nào không chắc?** → §2.3, §2.8, §2.11

Thứ tự đó là có chủ ý. Nhóm **đo trước rồi mới viết mạch chuyện**, không viết mạch
trước rồi đi tìm số đỡ cho nó — và chính thứ tự này đã mấy lần bác bỏ điều nhóm
tưởng là đúng (§2.3, §2.7).

---

## 2.2 Nguồn dữ liệu: một nguồn duy nhất, và vì sao

Toàn bộ số liệu lấy từ **The Atlas of Economic Complexity** — Harvard Growth Lab,
phát hành qua Harvard Dataverse, bản phân loại **HS92**. Hai bộ dữ liệu, sáu file
được tải (`doi:10.7910/DVN/T4CHWJ` cho số liệu thương mại và
`doi:10.7910/DVN/3BAL1O` cho bảng phân loại), năm file đi vào phân tích:

| File thô | Dùng cho | Kích thước |
|---|---|---|
| `cc_year.csv` | thương mại song phương nước × nước × năm → mạng lưới | 30.767.251 byte |
| `cp_year_hs2.csv` | nước × nhóm hàng HS2 × năm → RCA, PCI, rổ hàng | 38.135.675 byte |
| `hs92_country_year.csv` | ECI, COI, diversity theo nước × năm | 363.501 byte |
| `product_hs92.csv` | cây sản phẩm HS92 bốn tầng | 843.499 byte |
| `location_country.csv` | mã nước, vùng, châu lục | 9.911 byte |

File thứ sáu, `hs92_data_dictionary.csv` (3.276 byte), là từ điển mô tả cột — tải
về để đọc, không đi vào phép tính nào.

**Vì sao chỉ một nguồn.** Số liệu thương mại luôn tồn tại hai bản cho cùng một
luồng: nước A báo "xuất sang B bao nhiêu", nước B báo "nhập từ A bao nhiêu", và
hai số không bao giờ bằng nhau — khác nhau về giá CIF/FOB, về thời điểm ghi nhận,
về chất lượng thống kê. Atlas đã **hoà giải** cặp số gương đó trước khi phát hành,
nên dùng Atlas là dùng một bản đã thống nhất. Trộn thêm BACI hay Comtrade vào thì
phải tự hoà giải lại, tức là thêm một nguồn sai số mà không thêm thông tin. Đây là
quyết định **B9**.

Bằng chứng cho lựa chọn đó: ba file Atlas nói trên đo **cùng một nền thương mại từ
ba góc khác nhau** — theo cặp nước, theo nước × sản phẩm, theo nước. Tổng xuất khẩu
thế giới 2024 tính từ ba file khớp nhau **0,000%** (`src/check_raw_data.py`, mục 8).
Một nguồn mà tự nhất quán được như vậy thì không cần nguồn thứ hai để đối chứng.

### Bài học về việc tải dữ liệu — và vì sao có một cửa chặn

Bản `cc_year.csv` dùng trong giai đoạn đầu là **một bản tải bị cắt giữa chừng**:
28.373.409 byte thay vì 30.767.251, mất đúng **7,8% cuối file**. Dữ liệu sắp theo
`country_id`, nên mọi nước có mã lớn hơn 795 mất sạch số liệu — trong đó có **Hoa
Kỳ**, Anh, Ukraine, Ai Cập. Hệ quả: tổng xuất khẩu thế giới 2024 đọc ra 19,07 nghìn
tỷ USD thay vì 21,81; số cạnh 2023 đọc ra 25.425 thay vì 27.535 — **lệch 2.110
cạnh**, toàn bộ do file cụt đuôi.

Đường truyền tới Dataverse chỉ khoảng **30 KB/s**, một lần tải gần 20 phút, và
trình duyệt đứt giữa chừng **không báo lỗi** — file vẫn mở bình thường, chỉ thiếu
đuôi. Vì vậy:

- `src/download_atlas.py` đối chiếu **MD5 chính thức** của Dataverse sau mỗi lần tải.
- `src/check_raw_data.py` là **cửa chặn bắt buộc** trước mọi thứ khác: 8 mục kiểm,
  trong đó có "16 nước xuất khẩu lớn nhất phải có mặt làm nguồn" — đúng cái mà bản
  cụt đã vi phạm. Hiện trạng: **ĐẠT** cả 8 mục.

Lỗi này đáng kể lại trong báo cáo vì nó là lỗi **im lặng**: không có thông báo nào,
chỉ có một con số sai mà nếu không đối chiếu thì không ai biết.

---

## 2.3 Năm tham chiếu là 2023, không phải 2024

`REFERENCE_YEAR = 2023` trong `src/reference_data.py`, và `PROVISIONAL_YEARS = [2024]`.
Mọi con số một-năm trong báo cáo lấy cùng năm 2023 để báo cáo không tự mâu thuẫn
(quyết định **B1**, **B10**).

Lý do không dùng 2024 là **một phát hiện về dữ liệu**, và cách phát hiện đáng kể
lại: không nhìn một năm, mà nhìn **hình dạng của cả chuỗi 30 năm**.

| Năm | 2015 | 2020 | 2022 | 2023 | **2024** |
|---|---|---|---|---|---|
| Số cạnh | 27.323 | 27.003 | 27.489 | 27.535 | **25.754** |
| Mật độ | 0,519 | 0,513 | 0,517 | 0,518 | **0,485** |
| Tổng xuất khẩu (nghìn tỷ USD) | 15,09 | 16,19 | 22,66 | 21,66 | 21,81 |

Số cạnh đứng rất yên suốt chín năm rồi rơi đúng ở năm cuối, **trong khi tổng giá
trị thì bình thường**. Giá trị đủ mà cặp nước thiếu thì không phải thương mại co
lại — là dữ liệu thiếu. Kiểm thẳng ở file thô xác nhận: `VNM->ARE` có dòng năm
2023 (6.582.537.191 USD) và **không có dòng nào** năm 2024; tương tự với Nga, Lào,
Bangladesh, Ghana, Iraq. Không nước nào biến mất hẳn — thiếu là thiếu **từng cặp**,
dấu hiệu quen của một bản phát hành tạm: nước chưa nộp số liệu cho Comtrade thì
Atlas chỉ dựng lại được phần nào từ báo cáo của đối tác.

Hậu quả với riêng đề tài này là nghiêm trọng: Việt Nam có **166 bạn hàng** năm 2023
và **129** năm 2024. 37 bạn hàng biến mất mang theo **11,4 tỷ USD = 2,96%** xuất
khẩu, trong đó có **Lào** — một nước ASEAN, ngay giữa lát cắt Việt Nam–ASEAN. Để
nguyên thì biểu đồ sẽ đọc thành *"Việt Nam đang mất bạn hàng"*, ngược hẳn sự thật.

Riêng dữ liệu nước × sản phẩm năm 2024 thì gần như đủ (18.102 dòng so với 18.590
dòng năm 2023, cùng 230 nước), nên treemap, RCA, PCI, ECI vẽ trên 2024 vẫn được —
nhưng **trộn hai năm trong một bài** là một lỗi khác, nên cả đồ án dùng một năm duy
nhất. Đây là hạn chế **D1**: báo cáo nói về 2023, không nói về hôm nay.

---

## 2.4 Từ dữ liệu thô đến mười bảng sạch

Mười bảng trung gian trong `data/processed/` do ba script sinh ra, không phải một:
`build_intermediate.py` dựng năm bảng đầu (nước, cạnh, cây sản phẩm, nước × sản
phẩm, nước × năm), `analyze_network.py` dựng ba bảng thống kê mạng, và
`compute_metrics.py` dựng hai bảng chỉ số theo nước.

Ba script của giai đoạn đầu — `build_intermediate.py`, `check_raw_data.py` và
`make_mock.py` — **chỉ dùng thư viện chuẩn của Python**, chạy được ngay mà không
cần cài gì.

| File | Nội dung | Dòng |
|---|---|---|
| `nodes.csv` | nước: mã, tên tiếng Việt, vùng, châu lục, `is_focus` | 233 |
| `edges.csv` | luồng xuất khẩu song phương 1995–2024 | 750.855 |
| `tree.csv` | cây sản phẩm HS92 bốn tầng | 6.390 |
| `country_product.csv` | nước × nhóm hàng HS2 × năm, kèm RCA và PCI | 539.986 |
| `country_year.csv` | nước × năm: ECI, thứ hạng, COI, diversity | 6.755 |
| `network_stats.csv` | mỗi năm một dòng: nút, cạnh, mật độ, đối ứng, Gini | 30 |
| `degree_distribution.csv` | phân bố bậc dạng dài, có `ccdf` | 1.094 |
| `threshold_coverage.csv` | 21 phương án lọc cạnh — bằng chứng cho §2.7 | 21 |
| `metrics.csv` | chỉ số mạng theo nước, mỗi nước hai dòng (§2.7) | 304 |
| `metrics_top20.csv` | top 20 nước xuất khẩu kèm chỉ số mạng | 20 |

Hai quy ước lọc ở tầng này:

- `export_value = 0` → **loại bỏ**. Một luồng bằng 0 không phải một cạnh, cũng
  không phải một dòng xuất khẩu (**B3**).
- `is_focus` = **cả 10 nước ASEAN**, không chỉ Việt Nam, vì đề tài có lát cắt
  Việt Nam–ASEAN (**B2**).

**Dữ liệu thô không bao giờ được commit** (Nguyên tắc #5 của nhóm, quyết định
**B8**). Cả mười file trung gian và toàn bộ `output/` đều bị `.gitignore` loại trừ
— sinh lại bằng lệnh, không lưu vào repo. Có đúng một ngoại lệ, và nó là một lỗi
đã ghi nhận: một blob `cc_year.csv` 28,4 MB lọt vào lịch sử `main` từ sớm và không
xoá được nữa vì hai PR đầu gộp bằng merge commit. Nhóm đã thống nhất **để nguyên**
— viết lại lịch sử một repo đang dùng chung thì lợi ít hại nhiều — và từ đó gộp
bằng squash.

---

## 2.5 Chỉ số nào tự tính, chỉ số nào lấy nguyên

Đây là chỗ dễ bị hỏi nhất, nên nói thẳng:

| Chỉ số | Nguồn | Giải thích gọn |
|---|---|---|
| **RCA** | **tự tính** | *Lợi thế so sánh hiện hữu.* Tỷ trọng một nhóm hàng trong rổ xuất khẩu của một nước, chia cho tỷ trọng của nhóm đó trong rổ xuất khẩu toàn thế giới. **RCA > 1** = nước đó bán nhóm hàng ấy **đậm đặc hơn mức trung bình thế giới**. |
| **PCI** | lấy nguyên từ Atlas | *Chỉ số phức tạp sản phẩm.* **PCI > 0** = mặt hàng khó làm hơn mức trung bình thế giới, theo nghĩa chỉ ít nước làm được và những nước đó thường làm được nhiều thứ khác nữa. |
| **ECI** | lấy nguyên từ Atlas | *Chỉ số phức tạp kinh tế.* Đo độ "khó" của cả rổ hàng một nước xuất khẩu. |
| **COI** | lấy nguyên từ Atlas | *Chỉ số cơ hội.* Đo việc từ rổ hàng hiện tại, nước đó dễ bước sang những mặt hàng khó hơn đến mức nào. |
| Thứ hạng ECI | **tự xếp** | xếp lại từ cột ECI để biết "thứ bao nhiêu trên bao nhiêu nước" của từng năm. |

**Vì sao không tự tính ECI và PCI.** Hai chỉ số đó là nghiệm của một phép lặp véc-tơ
riêng trên ma trận nước × sản phẩm của **toàn thế giới**; tính lại thì thêm một
nguồn sai số mà không thêm thông tin, và bản của Atlas chính là bản mà tài liệu
tham khảo trích dẫn. Ngược lại RCA là một phân số đơn giản, tự tính được thì kiểm
được — và nhóm đã dùng chính nó làm phép kiểm (§2.6).

**Một chỗ phải nói thật về độ chính xác.** Cột `rca` trong `country_product.csv`
được ghi ở dạng làm tròn bốn chữ số thập phân (`"%.4f"`). Phép kiểm đồng nhất thức
Balassa chạy **bên trong pipeline trên giá trị chưa làm tròn** và lệch
**1,0 × 10⁻¹⁵** — tức đúng tới giới hạn số thực. Nếu đo lại từ file CSV đã ghi thì
lệch **2,0 × 10⁻⁵**: đó là phần làm tròn, không phải sai số của công thức. Ai muốn
tái lập con số 10⁻¹⁵ phải chạy `src/build_intermediate.py` và đọc dòng
`KIEM DINH 2`, chứ không đọc lại từ CSV.

---

## 2.6 Sáu cửa kiểm chạy tự động

Toàn bộ đều là script, trả về mã thoát khác 0 khi không đạt, nên cắm được vào CI.
Đây là phần chứng minh dữ liệu **được kiểm** chứ không phải được tin.

| # | Cửa kiểm | Kiểm gì | Kết quả đo được |
|---|---|---|---|
| 1 | `check_raw_data.py` | 8 mục trên file thô, kể cả "16 nước xuất khẩu lớn nhất phải có mặt" | **ĐẠT** |
| 2 | ECI đã chuẩn hoá | mỗi năm trung bình ≈ 0, độ lệch chuẩn ≈ 1 trên toàn bộ các nước — đây là tính chất của cách tính, nên đọc lệch cột hay mất dòng là hai số này trồi ngay | `\|trung bình\| ≤ 0,076`; `\|độ lệch chuẩn − 1\| ≤ 0,054` |
| 3 | Trung bình RCA có trọng số = 1 | tính chất toán học của công thức Balassa: với mỗi sản phẩm, trung bình RCA của các nước có trọng số theo quy mô nước phải đúng bằng 1. Sai là công thức sai | lệch **1,0 × 10⁻¹⁵** (xem §2.5) |
| 4 | Đối chiếu chéo ba file | ba file Atlas đo cùng nền thương mại từ ba góc | khớp **0,000%** |
| 5 | `check_tree.py` | cây HS92: số nút từng tầng, nút mồ côi, chu trình, quy tắc mã | `{1: 10, 2: 97, 4: 1.243, 6: 5.040}`, **0 nút mồ côi**; **1 lỗi + 1 lưu ý** → §2.8 |
| 6 | `check_palette.py` + `check_readability.py` | hai cửa chặn thị giác: bảng màu và khả năng đọc | **ĐẠT**; cả **10 script** dựng hình đều trên khung point (§2.9) |

Cửa số 5 đáng chú ý vì **nó không sạch**, và nhóm giữ nguyên kết quả không sạch đó
thay vì nới điều kiện kiểm cho nó qua — chi tiết ở **§2.8**. Một phép kiểm chỉ có
giá trị khi nó được phép báo lỗi.

---

## 2.7 Hai đồ thị, không phải một — và vì sao Sankey dùng đồ thị đầy đủ

Đây là lựa chọn phương pháp **dễ bị đọc thành số liệu mâu thuẫn nhất** của cả báo
cáo, nên phải nói rõ.

### Đồ thị đầy đủ năm 2023

231 nút, **27.535 luồng có hướng**, mật độ **0,518**, đối ứng **0,837**, Gini của
giá trị cạnh **0,957**, và **top 1% số cạnh gánh 61,2% giá trị**. Mật độ 0,518
nghĩa là quá nửa số cặp nước trên đời có thương mại trực tiếp với nhau.

Trên một đồ thị dày như vậy, **betweenness sụp về 0 ở 74,5% số nước** — gần như
không đường đi ngắn nhất nào phải vòng qua nước thứ ba, nên chỉ số đó không còn đo
được gì. Và 27.535 cạnh vẽ ra thì thành một vũng mực, không thành một hình.

### Quy tắc lọc cạnh (quyết định B4)

```
giữ cạnh  ⟺  export_value ≥ 0,046% × tổng xuất khẩu thế giới CỦA NĂM ĐÓ
             HOẶC  nằm trong top 3 luồng xuất / top 3 luồng nhập
                   lớn nhất của một nước ASEAN
```

Năm 2023 ngưỡng tương đối đó tương đương **9,96 tỷ USD**, và cho ra **416 luồng có
hướng, 73 nút, 67,8% giá trị** — tức **bỏ 98,5% số cạnh** để giữ hai phần ba số
tiền. Ba lý do, theo thứ tự quan trọng:

1. **Ngưỡng theo tỷ lệ, không theo USD cố định.** Thương mại thế giới tăng **4,51
   lần** trong 29 năm (4,80 → 21,66 nghìn tỷ USD), nên một ngưỡng 10 tỷ USD cố định
   đo hai năm bằng hai cái thước: 1995 còn **89 cạnh**, 2023 còn **390 cạnh**. Vẽ
   small multiples bằng thước đó thì hình **đọc thành "thương mại mới xuất hiện sau
   1995"** trong khi sự thật là "thương mại lớn lên". Quy tắc tỷ lệ cho **378–438
   cạnh suốt cả 29 năm**, nên các panel so sánh được với nhau.
2. **Chọn đúng 0,046%** vì nó cho ra 9,96 tỷ USD ở năm tham chiếu — sát con số 10 tỷ
   mà đề bài đã ghi. Năm tham chiếu không đổi thước đo; chỉ các năm khác được quy về
   cùng thước.
3. **Bảo hiểm ASEAN là bắt buộc.** Ngưỡng tương đối một mình **xoá Việt Nam khỏi năm
   1995** — đúng 0 cạnh — và xoá Brunei, Lào, Myanmar khỏi hầu hết các năm. Với một
   đề tài tên là *"vị trí của Việt Nam"* thì đó là lỗi chí mạng. Giá phải trả: +23
   cạnh (393 → 416), +0,36 điểm phần trăm giá trị.

Các phương án đã cân nhắc và loại — ngưỡng tuyệt đối ở mọi mức (không so được
giữa các năm) và "mỗi nước giữ k luồng lớn nhất" (k=3 chỉ phủ 40,2% giá trị, k=10
đạt 66,0% nhưng đã 2.289 cạnh, quá dày để vẽ) — nằm đủ **21 dòng** trong
`data/processed/threshold_coverage.csv`.

### Và vì sao Sankey (T19) lại dùng đồ thị đầy đủ

Vì **dùng đồ thị đã lọc cho T19 sẽ đổi dấu con số chính của hình.** Đo được:

| Việt Nam, 2023 | Đồ thị đầy đủ | Đồ thị đã lọc |
|---|---|---|
| Bán ra | **166 nước**, 385,54 tỷ USD | **8 nước**, 249,84 tỷ USD (64,8%) |
| Mua vào | **149 nước**, 332,09 tỷ USD | **10 nước**, 265,01 tỷ USD (79,8%) |
| Xuất trừ nhập | **+53,45 tỷ USD** (thặng dư) | **−15,17 tỷ USD** (thâm hụt) |

Ngưỡng lọc cắt phía bán ra nặng hơn phía mua vào — vì Việt Nam mua tập trung vào
vài nước lớn còn bán rải ra 166 nước — nên cán cân trên đồ thị đã lọc **lật dấu**.
Một hình dựng như thế sẽ in ra một câu sai. Trên đồ thị đầy đủ, Sankey **khớp với
`country_year.csv` lệch 0,00 tỷ USD** ở cả hai chiều.

Từ đó rút ra quy tắc dùng cho cả báo cáo, và đây chính là câu trả lời cho ai thấy
số liệu hai hình không trùng nhau:

> **Hình nói về *cấu trúc toàn cầu* dùng đồ thị đã lọc** (T15 node-link, T16 ma trận
> kề, T17 chord) — ở đó câu hỏi là "ai nối với ai", và 98,5% cạnh nhỏ chỉ làm mờ
> câu trả lời.
> **Hình nói về *một nước* dùng đồ thị đầy đủ** (T19 Sankey, T20 small multiples) —
> ở đó câu hỏi là "bao nhiêu tiền, qua bao nhiêu cửa", và bỏ một cạnh là bỏ một
> phần của câu trả lời.
>
> **Hệ quả: không so trực tiếp con số của hai nhóm hình.** Cùng lý do đó, cột
> `strength_out` ở dòng `filtered` của `metrics.csv` là con số **đã bị cắt cụt**,
> không phải kim ngạch xuất khẩu; cột `world_export_share` ở dòng đó cố tình để
> rỗng để không ai dán nhầm.

`metrics.csv` vì vậy có **hai dòng cho mỗi nước**: dòng `full` để lấy **tiền** (độ
mạnh, thị phần thế giới), dòng `filtered` để lấy **betweenness và cộng đồng**.

Cộng đồng dò bằng **Louvain** trên bản vô hướng, hạt giống cố định `--seed 42`, và
script tự chạy lại 20 hạt giống khác để báo độ ổn định. Năm 2023: **3 cụm,
modularity 0,337, phân hoạch ổn định tuyệt đối** — 100% số cặp nước giữ nguyên quan
hệ cùng cụm hay khác cụm qua cả 20 lần chạy.

---

## 2.8 Cây sản phẩm HS92: hai chỗ lệch đã đo

`src/check_tree.py` chạy 31 mục kiểm trên cây HS92: **29 mục ĐẠT, 1 lỗi, 1 lưu ý**. Nhóm
giữ nguyên hai kết quả đó trong báo cáo thay vì sửa dữ liệu của Atlas.

### Lỗi: nút `3501` nằm sai nhánh

Quy tắc của mã HS là **mã con nối dài mã cha** — `3502` phải nằm dưới `35`. Có đúng
một nút phá quy tắc đó:

| Nút | Tên | Cha hiện tại | Cha đúng theo quy tắc mã |
|---|---|---|---|
| `3501` | Casein, caseinates and casein glues | HS2 **`34`** — xà phòng, sáp, chất đánh bóng | HS2 **`35`** — albuminoid, tinh bột biến tính, keo dán, enzyme |

Sáu nút em của nó (`3502` Albumins, `3503` Gelatin, `3504` Peptones, `3505`
Dextrins, `3506` Glues and adhesives, `3507` Enzymes) đều nằm đúng dưới `35`.

**Ảnh hưởng: không có, với mọi hình trong báo cáo này** — và nói được điều đó là vì
đã kiểm, không vì đoán. Hai nút `34` và `35` **cùng thuộc một ngành** (ngành 6, hoá
chất), nên không một tổng theo ngành nào bị lệch. Toàn bộ hình trong báo cáo dừng ở
**tầng 1 (10 ngành) và tầng 2 (97 nhóm hàng)**, còn chỗ lệch nằm ở tầng 4. Ghi lại
vì bất kỳ ai đi tiếp xuống HS4 sẽ gặp nó.

### Lưu ý: mã `XXXX` dưới nhóm `99`, và 11,83% rổ hàng

Atlas giữ chỗ cho phần số liệu không khớp bằng một nút riêng: nút `XXXX` — *"Trade
data discrepancies"* — nằm dưới HS2 **`99` "Other"**, thuộc ngành 10 (*Chưa phân
loại*, màu xám `#DDDDDD`). Đây **không phải một lỗi cây**, mà là một mã giữ chỗ hợp
lệ của nguồn. Nhưng nó có một hệ quả thật, và lớn:

> Nhóm `99` chiếm **45,60 tỷ USD = 11,83%** xuất khẩu Việt Nam năm 2023, với
> **RCA 2,4408** và **PCI −1,206**.

RCA **2,4408** của ô đó **cao hơn cả điện tử (2,23)** — tức nếu để nguyên thì một
trong những ô "bán đậm nhất" trên mặt phẳng quyết định (T31) lại là **một ô dữ liệu
không phân loại được**, không phải một ngành hàng có thật để mà đề xuất đầu tư. Vì vậy quy tắc chọn đề xuất ở §2.10 **loại thẳng ngành
*Chưa phân loại*** (`sector != UNCLASSIFIED`), và hình T31 vẽ nó ở màu xám trung
tính để người đọc thấy nó tồn tại mà không đọc nó như một lựa chọn.

---

## 2.9 Quy ước trực quan hoá: những gì đo được thì đã đo

Toàn bộ quy ước nằm ở `docs/style-guide.md` và được áp bằng
`src/reference_data.py`; không có hằng số nào viết lại tại chỗ trong các script vẽ.
Bốn quy ước có ảnh hưởng tới việc đọc hình, và cả bốn đều đã được **đo** chứ không
chỉ chọn:

**1. Khung hình tính bằng point, không bằng pixel.** Khổ hình đầy là
`6,30 inch × 72 = 453,6 pt`. Sàn cỡ chữ là **7 pt** (style guide §7). Hai điều này
chỉ kiểm được cùng nhau nếu khung đo bằng cùng đơn vị với chữ — và trước T22 thì
không: các script cũ xuất PNG với khung `6,30 × 200 = 1.260` đơn vị nhưng truyền cỡ
chữ bằng **point** vào đó, tỷ số **200/72 = 2,7778**. Hệ quả đo được: một dòng
nguồn khai **7 pt in ra khoảng 2,5 pt**, dưới sàn. Lỗi này (**B16**) có thật ở năm
hình đầu (T09, T12, T13, T14, T15) và đã sửa ở T22 — sửa đơn vị buộc phải **bố cục
lại cả năm hình**, vì ở cỡ chữ đúng thì tiêu đề tràn khung (`layout.title` của
plotly không tự ngắt dòng), chú giải cuộn thêm hàng đè lên ghi chú nguồn, và nhãn
nút chồng nhau. `check_readability.py` xác nhận hiện **cả 10 script** đã trên khung
point.

**2. Màu là của ngành hàng, chỉ thế thôi.** 10 màu ngành lấy thang Tol muted, đổi
Khoáng sản sang nâu đậm: **ΔE nhỏ nhất 16,1 ở mắt thường và 11,6 qua cả ba dạng mù
màu** (bảng Tableau 10 dùng tạm trước đó có Nông sản trùng hẳn Phương tiện vận tải
với người mù lục, ΔE = 0,7). Cụm Louvain cần màu mà không phải ngành, nên có bảng
**riêng**, qua cùng bộ kiểm: ΔE 24,7 mắt thường, 13,5 ở dạng mù màu khó nhất, và
cách màu ngành gần nhất 20,0 (**B11**, **B14**).

**3. Việt Nam nổi bằng hình dạng, không bằng màu** (**B12**). Đã thử thêm màu thứ
11: mọi màu cam/đỏ tách được khỏi 10 màu ngành ở mắt thường (ΔE 22–27) đều tụt
xuống **ΔE 4–8** khi mô phỏng mù màu. Thay bằng viền đen 1,5 px và nhãn đậm. Đi xa
hơn, `src/probe_colour_space.py` đo được rằng **không gian màu in được đã hết chỗ**:
sau 10 màu ngành và 3 màu cụm, màu thứ ba của một bảng thứ ba chỉ còn **ΔE 14,2**,
dưới sàn 15. Vì vậy chord (T17) **mã hoá khối bằng vị trí, không bằng màu** (**B17**).

**4. Số viết theo kiểu Việt Nam**: dấu phẩy thập phân, dấu chấm hàng nghìn, đi qua
`R.fmt_vn` / `R.fmt_pct` / `R.fmt_usd` — kể cả nhãn trục, và trục log của plotly
phải đặt `tickmode="array"` + `tickvals` + `ticktext`, nếu không nó tự dán nhãn tick
phụ theo kiểu Anh.

**Nhãn thì bị sàn 7 pt ràng buộc, và chỗ nào không đủ thì bỏ nhãn chứ không thu
chữ.** Ví dụ đo được: ma trận kề có cạnh vùng vẽ 250,3 pt trên khung 453,6 pt; chia
cho 73 nước còn **3,4 pt mỗi nhãn**, và không bố trí nào cứu được vì 73 × 7 pt =
511 pt đã dài hơn cả cạnh khung. Nên ma trận ghi **13 nhãn**: 10 nước ASEAN (lát cắt
của đề tài) + nước mạnh nhất mỗi cụm → **19,3 pt mỗi nhãn**, đạt sàn (**B15**).

---

## 2.10 Đề xuất được chọn bằng một quy tắc, và quy tắc đã được thử lại

Phần đề xuất của báo cáo **không phải một lựa chọn bằng tay**. Nó là đầu ra của một
bộ lọc viết trong `src/make_decision_plane.py`:

```python
c = df[(df["export_value"] >= MIN_EXPORT)      # ≥ 1 tỷ USD: đủ lớn để đáng bàn
       & (df["pci"] > 0)                        # khó hơn trung bình thế giới
       & (df["rca"] >= RCA_LO)                  # 0,5: đã có chỗ đứng
       & (df["rca"] < RCA_HI)                   # 1,5: chưa phải nơi đã thắng
       & (df["d_rca"] > 0)                      # đang đi lên, không đi xuống
       & (df["sector"] != UNCLASSIFIED)]        # không phải ô XXXX — xem §2.8
return c.nlargest(N_PICK, "pci")                # lấy 2 nhóm khó nhất còn lại
```

**Vì sao phải là một quy tắc.** Một lựa chọn bằng tay không kiểm được: ai cũng có
thể nói "tôi nghĩ nên dồn vào X". Một quy tắc thì **thử lại được trên quá khứ** —
và đó là bằng chứng mạnh nhất của cả báo cáo:

> Chạy đúng quy tắc đó trên dữ liệu năm **2015** (`--year 2015 --since 2007`) thì nó
> chọn **thiết bị quang học** và **sắt thép**. Tám năm sau, cả hai đi đúng hướng đã
> dự đoán, và **sắt thép chạm RCA 1,00** — vượt ngưỡng lợi thế.

Quy tắc có **thành tích trên chính bộ dữ liệu này**, chứ không chỉ có một lời khẳng
định. Và vì nó là quy tắc, nó cũng nói trước **điều gì sẽ làm nhóm đổi ý**: nếu RCA
của hai nhóm được chọn chững lại dưới 1 trong vài năm tới, hoặc nếu đầu vào tự đa
dạng hoá khỏi mức 68,3% từ một vùng duy nhất, thì luận cứ yếu đi và phải chọn lại.
Một đề xuất có điều kiện bác bỏ thì mới là đề xuất.

Toàn bộ tiêu đề trên các hình cũng tuân theo nguyên tắc này: **tiêu đề dựng từ dữ
liệu của chính lần chạy đó, không viết sẵn**. Lý do rất thực tế — một tiêu đề viết
sẵn sẽ in ra một câu sai khi chạy năm khác. Đã bắt được ba lần: T09 (câu "gần như
đều" sai cho 1995), T15 (câu "ba cụm là ba châu lục" sai), và T14 (tiêu đề viết sẵn
"Việt Nam dựa mạnh vào dệt may" — chạy năm 1995 thì dữ liệu nói **nông sản, gỗ và
giấy 42,9% so với 26,0%** của nước cao thứ nhì). Vì vậy mỗi script còn **render thêm
một năm đối chứng** (thường 1995) và in một khối kiểm chứng ra stdout, đủ để kiểm
lại khẳng định trên tiêu đề mà không cần mở code.

---

## 2.11 Năm hạn chế phải nói trước

Nêu ra thì được điểm trung thực; giấu đi mà bị hỏi thì mất nhiều hơn.

**D1. Dữ liệu dừng ở 2023, không phải 2024.** Bản Atlas 2024 còn tạm: thiếu 1.781
cặp nước, riêng Việt Nam mất 37 bạn hàng trị giá 11,4 tỷ USD. Xem §2.3.

**D2. ECI tính trên xuất khẩu gộp** → nó thưởng điểm cho việc **lắp ráp** hàng phức
tạp bất kể nước đó giữ lại được bao nhiêu giá trị. Nói cách khác, ECI đo *cái gì đi
qua Việt Nam*, chưa hẳn là *cái gì ở lại Việt Nam*.

**D3. Node-link vứt 98,5% số cạnh.** Nó **không** đọc được là "bản đồ thương mại
toàn cầu", mà là *"bản đồ các luồng thương mại lớn, cộng chỗ đứng của ASEAN trong
đó"*. Ai muốn nhìn phần đuôi phải xem ma trận kề (T16) — ma trận vẽ đủ **cả 416
luồng có hướng**, không gộp hai chiều như node-link, và không có cạnh nào chồng lên
cạnh nào. Nhưng nó cũng chỉ vẽ **đúng 416 luồng ấy**: cả hai hình đứng trên cùng
một đồ thị đã lọc, nên ma trận **không** cứu được cái 98,5% đã bỏ.

**D4. Dữ liệu dừng ở HS2 (97 nhóm hàng).** Chi tiết hơn cần file HS4 452 MB, khoảng
4,2 giờ tải ở tốc độ đo được. Hệ quả cụ thể: nhóm "Điện, điện tử và linh kiện" gộp
cả chip lẫn dây điện vào một ô.

**D5. Không có dữ liệu giá trị gia tăng.** Mọi nhận định về "giữ lại bao nhiêu giá
trị" trong báo cáo là **suy luận từ RCA × PCI**, không phải đo trực tiếp. Phần "xuất
trừ nhập" trên Sankey (T19) là **số học**, không phải giá trị tăng thêm — tách được
phần đó cần bảng vào–ra mà Atlas không có.

Hai hạn chế cuối cùng nối thẳng vào chỗ yếu nhất của đề xuất, nên báo cáo nói ra
trước thay vì chờ bị hỏi. Điểm mạnh bù lại là phép thử lại ở §2.10.

---

## 2.12 Tái lập toàn bộ

Môi trường đo được: **Python 3.9.13**, `plotly 7.1.0`, `networkx 3.2.1`,
`pandas 2.2.3`, `kaleido` (xuất PNG). Chạy trong venv của repo:

```bash
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/<script>.py
```

Thứ tự pipeline — năm bước đầu **không cần thư viện ngoài**:

```bash
python src/download_atlas.py        # 0. tải dữ liệu thô + đối chiếu MD5
python src/check_raw_data.py        # 1. CỬA CHẶN, phải báo DAT
python src/build_intermediate.py    # 2. sinh 10 bảng trong data/processed/
python src/analyze_network.py       # 3. thống kê mạng + bảng 21 ngưỡng
python src/check_palette.py         # 4. CỬA CHẶN bảng màu, thoát 1 nếu hỏng
python src/check_tree.py            # 5. kiểm cây HS92 (§2.8)
python src/compute_metrics.py       # 6. metrics.csv, hai đồ thị (§2.7)
python src/check_readability.py     # 7. CỬA CHẶN khả năng đọc, 5 phép kiểm
```

Lệnh lấy lại từng con số trong phần này:

| Con số | Lệnh |
|---|---|
| 8 mục kiểm dữ liệu thô; đối chiếu chéo ba file 0,000% | `src/check_raw_data.py` |
| ECI chuẩn hoá; RCA trung bình có trọng số = 1 (10⁻¹⁵) | `src/build_intermediate.py` |
| 27.535 cạnh, mật độ 0,518, chuỗi 30 năm của §2.3 | `src/analyze_network.py` |
| 416 luồng / 73 nút / 67,8% giá trị; 21 phương án ngưỡng | `data/processed/threshold_coverage.csv` |
| betweenness = 0 ở 74,5% số nước; Louvain 3 cụm, modularity 0,337 | `src/compute_metrics.py` |
| `3501` dưới `34`; `XXXX` dưới `99`; cây 4 tầng | `src/check_tree.py` |
| 166 / 149 bạn hàng, +53,45 tỷ USD, khớp `country_year.csv` lệch 0,00 | `src/make_sankey.py` |
| 11,83% rổ hàng là nhóm `99`; quy tắc chọn đề xuất | `src/make_decision_plane.py` |
| quy tắc chọn thử lại trên 2015 (sắt thép chạm RCA 1,00) | `src/make_decision_plane.py --year 2015 --since 2007` |
| sàn 7 pt, cả 10 script trên khung point, ΔE bảng màu | `src/check_readability.py` · `src/check_palette.py` |
| không gian màu đã hết chỗ (ΔE 14,2 < 15) | `src/probe_colour_space.py` |

Sổ gốc của mọi con số: `docs/phat-hien-va-quyet-dinh.md` — phát hiện **A1–A15**,
quyết định thiết kế **B1–B20**, hạn chế **D1–D5**.

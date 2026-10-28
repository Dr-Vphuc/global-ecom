# 2. Phương pháp luận

> Mọi con số trong báo cáo đều đo lại được bằng một lệnh ghi ngay cạnh nó; không
> có con số nào chép từ tài liệu ngoài. Danh sách lệnh đầy đủ ở **§A.5**.
>
> **Năm mục thuộc phương pháp đã chuyển về phụ lục** khi ráp báo cáo, để phần thân
> giữ mạch lập luận: §A.1 mười bảng sạch · §A.2 sáu cửa kiểm · §A.3 cây HS92 ·
> §A.4 quy ước thị giác · §A.5 lệnh tái lập. Nội dung không bị cắt.
>
> **Ghi chú về phụ thuộc:** file phân công ghi phần này phụ thuộc **T08** (đối
> chiếu Atlas với BACI và Comtrade). Phụ thuộc đó **đã được bỏ** từ quyết định
> **B9**: ba file Atlas tự khớp nhau **0,000%**, nên không cần nguồn thứ hai để
> đối chứng — xem §2.2.

## 2.1 Phần này phải trả lời ba câu

Một bài tư vấn chỉ đáng tin bằng đúng phần phương pháp của nó. Ba câu người nghe
sẽ hỏi, và phần này phải trả lời trước khi bị hỏi:

1. **Số ở đâu ra?** → §2.2 – §2.4, và §A.1
2. **Vì sao tin được?** → §2.5, §A.2, §A.3 — và quy tắc chọn đề xuất ở §7.1
3. **Chỗ nào không chắc?** → §2.3, §A.3, §8.1

Thứ tự đó là có chủ ý. Nhóm **đo trước rồi mới viết mạch chuyện**, không viết mạch
trước rồi đi tìm số đỡ cho nó — và chính thứ tự này đã mấy lần bác bỏ điều nhóm
tưởng là đúng (§2.3, §2.5).

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

Việc hoà giải đó đo được chứ không chỉ là lời của nhà phát hành: với **2.093** luồng
từ 1 tỷ USD trở lên năm 2023, số nước xuất khai và số nước nhập khai **trùng khít ở
cả 2.093 luồng**, và năm 1995 cũng vậy (679/679). Hệ quả là bộ dữ liệu **không cho
tự đo sai số của nó**: không còn bản khai thứ hai độc lập để so (`src/compare_mirror.py`,
phát hiện **A18**).

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

## 2.4 Chỉ số nào tự tính, chỉ số nào lấy nguyên

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
được — và nhóm đã dùng chính nó làm phép kiểm (§A.2).

**Một chỗ phải nói thật về độ chính xác.** Cột `rca` trong `country_product.csv`
được ghi ở dạng làm tròn bốn chữ số thập phân (`"%.4f"`). Phép kiểm đồng nhất thức
Balassa chạy **bên trong pipeline trên giá trị chưa làm tròn** và lệch
**1,0 × 10⁻¹⁵** — tức đúng tới giới hạn số thực. Nếu đo lại từ file CSV đã ghi thì
lệch **2,0 × 10⁻⁵**: đó là phần làm tròn, không phải sai số của công thức. Ai muốn
tái lập con số 10⁻¹⁵ phải chạy `src/build_intermediate.py` và đọc dòng
`KIEM DINH 2`, chứ không đọc lại từ CSV.

---

## 2.5 Hai đồ thị, không phải một — và vì sao Sankey dùng đồ thị đầy đủ

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


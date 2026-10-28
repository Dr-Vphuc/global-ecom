# global-ecom

**Đồ án cuối kỳ — Trực quan hóa dữ liệu**

Đề tài: *Mạng lưới thương mại quốc tế — vị trí của Việt Nam trong cấu trúc thương mại toàn cầu*, kèm một lát cắt sâu về quan hệ Việt Nam – ASEAN.

Kỹ thuật trọng tâm: *Visualization Techniques for Trees, Graphs, and Networks*.

Phân công chi tiết, hợp đồng dữ liệu và tiến độ nằm trong `phan-cong-cong-viec.xlsx`.

📌 **Viết báo cáo thì mở `docs/phat-hien-va-quyet-dinh.md` trước.** Nó gom mọi
phát hiện đã đo được, mọi quyết định đã chốt kèm lý do, và năm hạn chế phải nêu
thẳng. README này chỉ nói cách chạy repo.

📌 **Muốn biết đã làm được gì, ai làm, sản phẩm nằm ở file nào → `docs/nhat-ky-cong-viec.md`.**

---

## Dữ liệu thô: đã sửa, và bài học

Bản `cc_year.csv` từng nằm trong repo là **một bản tải bị cắt giữa chừng**:
28.373.409 byte thay vì 30.767.251, mất đúng 7,8% cuối file. Dữ liệu sắp xếp
theo `country_id` nên mọi nước có mã lớn hơn 795 mất sạch số liệu xuất khẩu —
trong đó có **Hoa Kỳ**, Anh, Ukraine, Ai Cập. Tổng xuất khẩu thế giới 2024 đọc
ra 19,07 nghìn tỷ USD thay vì 21,81.

Kết nối tới Dataverse chỉ khoảng 30 KB/s, nên một lần tải kéo dài gần 20 phút.
Trình duyệt đứt giữa chừng và **không báo lỗi** — file vẫn mở được bình thường,
chỉ cụt đuôi. Đó là lý do `src/download_atlas.py` luôn đối chiếu MD5 chính thức
và `src/check_raw_data.py` là cửa chặn bắt buộc trước khi chạy pipeline.

Hiện tại `python src/check_raw_data.py` báo `DAT` trên cả 8 mục kiểm tra.

### Số liệu đã đo lại — đừng dùng số cũ

Các con số trong `phan-cong-cong-viec.xlsx` được đo trên bản bị cắt. Số đúng,
đo trên năm mốc **2023** — cùng năm mà file phân công ghi, nên so được trực tiếp:

| Chỉ số năm 2023 | Số cũ trong file phân công | Số đúng |
|---|---|---|
| Số cạnh | 25.425 | **27.535** |
| Số nút | 230 | **231** |
| Mật độ | 0,483 | **0,518** |
| Top 1% cạnh chiếm | 60,2% | **61,2%** |
| Ngưỡng 10 tỷ USD | 347 cạnh, 65,7% giá trị | **390 cạnh, 67,3% giá trị** |

Lệch **2.110 cạnh** — toàn bộ do bản tải cụt đuôi, không phải do cách dựng đồ thị.

Các ô trong file Excel đã được cập nhật theo số đo này.

### ⚠️ Dữ liệu 2024 chưa đầy đủ — vì sao năm mốc là 2023

Bản phát hành Atlas cho năm 2024 còn **tạm**. Số cạnh đứng rất yên suốt chín năm
rồi rơi đúng ở năm cuối, trong khi tổng giá trị thì bình thường:

| Năm | 2015 | 2020 | 2022 | 2023 | **2024** |
|---|---|---|---|---|---|
| Số cạnh | 27.323 | 27.003 | 27.489 | 27.535 | **25.754** |
| Mật độ | 0,519 | 0,513 | 0,517 | 0,518 | **0,485** |
| Tổng XK (nghìn tỷ USD) | 15,09 | 16,19 | 22,66 | 21,66 | 21,81 |

Nghĩa là cái thiếu là các **cặp nước**, không phải tiền. Kiểm thẳng ở file thô
`data/atlas/cc_year.csv`:

```
VNM->ARE 2023  export = 6.582.537.191
VNM->ARE 2024  KHÔNG CÓ DÒNG NÀO
```

Tương tự với Nga, Lào, Bangladesh. Không nước nào biến mất hẳn — cả 231 nước đều
có mặt cả hai năm — thiếu là thiếu từng cặp. **168 trong 231 nước** mất bạn hàng
khi sang 2024; UAE nặng nhất, 218 → 129. Đây là dấu hiệu quen thuộc của một bản
phát hành tạm: nước chưa nộp số liệu cho Comtrade thì Atlas chỉ dựng lại được
phần nào từ báo cáo của đối tác.

**Hậu quả với riêng đề tài này:** Việt Nam tụt từ **166 xuống 129 bạn hàng**, mất
37 bạn hàng mang theo **11,4 tỷ USD (2,96% xuất khẩu)** — trong đó có **Lào**,
một nước ASEAN. Để nguyên thì biểu đồ đọc thành *"Việt Nam đang mất bạn hàng"*,
ngược hẳn sự thật.

Dữ liệu cấp **nước × sản phẩm** của 2024 thì gần như đủ (18.102 dòng so với
18.590 năm 2023, cùng 230 nước, tổng giá trị bình thường) — tức là treemap, RCA,
PCI, ECI vẽ trên 2024 vẫn được. Nhưng trộn hai năm trong một bài vi phạm
Checklist #18, nên **cả đồ án dùng một năm duy nhất: 2023**.

Trong `reference_data.py`: `REFERENCE_YEAR = 2023`, `LAST_COMPLETE_YEAR = 2023`,
`PROVISIONAL_YEARS = [2024]`. Biểu đồ chuỗi thời gian phải dừng ở 2023, hoặc vẽ
tiếp nhưng ghi rõ 2024 là số tạm.

### Chỉ số phức tạp kinh tế — vị trí của Việt Nam

`data/processed/country_year.csv` mang **ECI** (Economic Complexity Index) của
Atlas. Đây là chỉ số đã chuẩn hoá: mỗi năm trung bình ≈ 0 và độ lệch chuẩn ≈ 1
trên toàn bộ các nước, nên đọc trực tiếp được như một điểm z.

| | 1995 | 2005 | 2015 | 2023 |
|---|---|---|---|---|
| **Việt Nam** | −1,00 (#181/211) | −0,12 (#132/224) | +0,24 (#109/230) | **+0,58 (#78/230)** |
| Thái Lan | +0,39 (#80) | +0,65 (#58) | +0,93 (#45) | +0,85 (#49) |
| Malaysia | +0,60 (#65) | +0,81 (#47) | +0,96 (#42) | +0,95 (#45) |
| Philippines | +0,11 (#101) | +0,27 (#97) | +0,58 (#77) | +0,76 (#61) |
| Indonesia | −0,14 (#120) | +0,17 (#108) | +0,28 (#104) | +0,28 (#101) |
| Singapore | +0,91 (#33) | +1,23 (#16) | +1,57 (#6) | +1,68 (#5) |

Việt Nam đi từ hạng 181/211 lên hạng 78/230 — từ nhóm 14% cuối bảng lên nhóm
34% đầu bảng trong 28 năm. Khoảng cách với Thái Lan thu từ **1,39** xuống
**0,28** điểm; Thái Lan đạt đỉnh năm 2015 rồi đi ngang.

Số nước được xếp hạng đổi theo năm (211 → 230), nên cột `eci_n` trong file là
bắt buộc khi vẽ biểu đồ thứ hạng theo thời gian — "hạng 78" không đọc được nếu
thiếu mẫu số.

⚠️ ECI tính trên rổ xuất khẩu **gộp**, nên một nước lắp ráp hàng phức tạp vẫn
được cộng điểm phức tạp dù giữ lại ít giá trị gia tăng. Đường ECI dốc đứng đi
kèm RCA điện tử chỉ 2,23 và RCA máy móc công nghiệp **0,95 — dưới 1, tức không
có lợi thế so sánh** (xem `country_product.csv`) là một căng thẳng nên nêu thẳng
trong báo cáo, không nên lờ đi.

### Mạng lưới: hình thù và ngưỡng lọc (T09 + T10)

`src/analyze_network.py` đo mạng lưới rồi sinh ba file. Tóm tắt kết quả:

| | 1995 | 2023 |
|---|---|---|
| Số nút | 211 | 231 |
| Số cạnh | 18.411 | 27.535 |
| **Mật độ** | 0,416 | **0,518** |
| **Đối ứng** | 0,824 | **0,837** |
| **Gini trọng số cạnh** | 0,955 | **0,957** |

Ba con số in đậm là phát hiện chính của T09, và nó **ngược với trực giác về
mạng lưới**:

- **Mật độ 51,8%** — hơn một nửa mọi cặp nước có giao dịch. Mạng xã hội hay mạng
  trích dẫn thường dưới 1%. Mạng thương mại gần như đầy.
- **Đối ứng 0,84** — A xuất sang B thì 84% khả năng B cũng xuất ngược lại. Hướng
  của cạnh mang rất ít thông tin, nên node-link **không cần mũi tên**; dùng mũi
  tên chỉ làm rối thêm mà không thêm ý nghĩa.
- **Gini 0,957, gần như đứng yên suốt 28 năm.** Mạng phình từ 18 nghìn lên 27,5
  nghìn cạnh nhưng độ lệch của giá trị không đổi.

Gộp lại: **cấu trúc trung tâm–ngoại vi của thương mại không nằm ở việc ai nối với
ai, mà nằm ở việc luồng nào lớn.**

Phân bố bậc xác nhận điều đó, và nó là kết quả đáng ngạc nhiên nhất của T09:

| Bậc xuất khẩu 2023 | min | p25 | trung vị | p75 | p90 | max |
|---|---|---|---|---|---|---|
| số bạn hàng | 0 | 62 | 116 | 177 | 210 | 226 |

Các nước **trải gần như đều** từ 0 đến 226 bạn hàng — đo cụ thể, CCDF lệch khỏi
một phân bố đều hoàn toàn nhiều nhất **0,056**. Nghĩa là mạng này *không có*
bậc đặc trưng và cũng *không có* hub theo nghĩa tô-pô: không tồn tại một nhóm
nhỏ các nước nối với tất cả trong khi phần còn lại nối với vài nước.

Hệ quả thực tế cho báo cáo: **biểu đồ log-log của T09 không ra đường thẳng.**
Hình đã vẽ xong — `output/degree_loglog_2023.png`, dựng bằng
`src/make_degree_loglog.py`. Sách giáo khoa hay minh hoạ mạng scale-free bằng
một đường thẳng dốc; ở đây đường CCDF đi ngang rồi rơi dốc đứng ở mép phải.
Đo cụ thể: đường thẳng khớp nhất trên thang log-log chỉ đạt **R² = 0,51**, có
chỗ lệch **41,3 lần**, và nếu kéo về phía bậc thấp nó còn đòi CCDF vượt 100% ở
mọi bậc dưới 31 — một đòi hỏi vô nghĩa, vì CCDF là tỉ lệ. Đó không phải lỗi dữ liệu —
đó là kết quả, và nó chính là lý do **phải lọc theo trọng số; lọc theo bậc vô
nghĩa** vì bậc không phân biệt được nước nào quan trọng.

### Quy tắc lọc cạnh đã chốt ở T10

```
giữ cạnh  ⟺  export_value ≥ 0,046% × tổng xuất khẩu thế giới CỦA NĂM ĐÓ
             HOẶC  nó nằm trong top 3 luồng xuất / top 3 luồng nhập
                   lớn nhất của một nước ASEAN
```

Trong `reference_data.py`: `THRESHOLD_SHARE = 0.00046` và `FOCUS_TOPK = 3`.

**Vì sao không dùng ngưỡng cố định 10 tỷ USD.** Thương mại thế giới tăng **4,51 lần**
từ 1995 (4,80 nghìn tỷ USD) đến 2023 (21,66 nghìn tỷ USD), nên một ngưỡng tính
bằng USD danh nghĩa đo hai năm bằng hai cái thước khác nhau:

| Năm | Ngưỡng cố định 10 tỷ USD | Quy tắc đã chốt |
|---|---|---|
| 1995 | 89 cạnh, 49,5% giá trị, **ASEAN 4/10** | 383 cạnh, 73,9% giá trị, ASEAN 10/10 |
| 2005 | 176 cạnh, 56,2% giá trị, ASEAN 5/10 | 406 cạnh, 70,2% giá trị, ASEAN 10/10 |
| 2015 | 270 cạnh, 61,6% giá trị, ASEAN 6/10 | 407 cạnh, 68,1% giá trị, ASEAN 10/10 |
| 2023 | 390 cạnh, 67,3% giá trị, ASEAN 8/10 | 416 cạnh, 67,8% giá trị, ASEAN 10/10 |

Cột trái là một cái bẫy: panel 1995 chỉ còn 89 cạnh và 25 nút, nên small
multiples sẽ **đọc thành "thương mại mới xuất hiện sau 1995"** trong khi sự thật
là "thương mại lớn lên". Cột phải giữ số cạnh ổn định 383–416 qua mọi năm mốc —
và trên cả 29 năm nó nằm gọn trong khoảng **378–438** — nên các panel so sánh
được với nhau.

**Vì sao có phần bảo hiểm cho ASEAN.** Ngưỡng tương đối một mình vẫn **xoá Việt
Nam khỏi năm 1995** (0 cạnh), và xoá Brunei, Lào, Myanmar khỏi hầu hết các năm.
Với một đề tài tên là *"vị trí của Việt Nam"* thì đó là lỗi chí mạng, không phải
chi tiết nhỏ. Giá phải trả cho phần bảo hiểm rất rẻ: **+23 cạnh** (393 → 416) và
**+0,36 điểm phần trăm** giá trị.

**Cái đang bị bỏ mất, nói thẳng trong báo cáo.** Quy tắc này giữ 1,5% số cạnh và
67,8% giá trị năm 2023 — tức là **vứt 98,5% số cạnh**. Phần bị vứt là hàng vạn
luồng nhỏ; cộng lại chúng bằng gần một phần ba thương mại thế giới. Node-link vì
vậy **không** đọc được là "bản đồ thương mại toàn cầu", mà là *"bản đồ các luồng
thương mại lớn, cộng với chỗ đứng của ASEAN trong đó"*. Ma trận kề của T16 vẽ
đủ **cả 416 luồng có hướng**, không gộp hai chiều và không có cạnh nào chồng lên
cạnh nào — nhưng nó đứng trên cùng đồ thị đã lọc ấy, nên **không** cứu được cái
98,5% đã bỏ. Muốn nhìn phần đuôi thì phải đổi ngưỡng, không phải đổi loại hình.

Toàn bộ 21 phương án đã cân nhắc nằm trong `data/processed/threshold_coverage.csv`
— gồm cả họ ngưỡng tuyệt đối và họ "mỗi nước giữ k luồng lớn nhất" đã bị loại.

### Ma trận kề: đổi thứ tự thì cấu trúc hiện ra (T16)

`src/make_adjacency_matrix.py` vẽ **hai** ma trận 73 × 73 của cùng đồ thị đã
lọc, hình vuông 6,30 × 6,30 inch, thang `SEQUENTIAL_SCALE`: một xếp theo mã
nước A→Z (`adjacency_alpha_2023.png`), một xếp theo cụm Louvain
(`adjacency_cluster_2023.png`). Hàng là nước xuất, cột là nước nhập.

Hai bản có **cùng 416 ô** và **cùng 14,69 nghìn tỷ USD** — script tự dựng cả
hai rồi so, tổng lệch **0 USD**. Khác nhau duy nhất là chỗ ngồi. Và chỗ ngồi
đổi được bao nhiêu thì đã đo, chứ không chỉ nói:

| Thước đo (2023) | Theo mã nước | Theo cụm | Xếp ngẫu nhiên |
|---|---|---|---|
| Khoảng cách trung bình tới đường chéo `\|i−j\|/(n−1)`, có trọng số theo giá trị | 0,398 | **0,258** | 0,341 |
| Giá trị nằm trong khối | 69,7% — không phụ thuộc thứ tự | | |
| Mật độ ô trong khối so với ngoài khối | 12,9% so với 4,1%, gấp **3,14 lần** | | |

Thứ tự alphabet **còn xa đường chéo hơn cả 300 lần xếp ngẫu nhiên** (0,398 so
với 0,341): nó không trung tính, nó chủ động trộn các khối vào nhau. Xếp theo
cụm kéo con số xuống 0,258, giảm **35,1%**.

Năm đối chứng 1995 cho cùng kết luận nhưng mạnh hơn (0,366 → 0,165, giảm
54,9%) và lộ ra một phát hiện mới, **A10**: năm 1995 khối lớn là khối *xuyên
Thái Bình Dương* do **Hoa Kỳ** đứng đầu, chứa cả Nhật Bản, Canada và 10 nước
ASEAN; đến 2023 Hoa Kỳ đã tách ra thành một khối Bắc Mỹ 7 nước, còn khối cũ nở
lên 41 nước với **Trung Quốc** ở tâm. Đồng thời tỉ lệ giá trị nằm trong khối
rơi từ **83,8%** xuống **69,7%** trong khi modularity gần như đứng yên
(0,343 → 0,337) — cấu trúc khối lỏng đi chứ không chặt lại.

Hai quyết định mới đi kèm, cả hai đều từ phép đo: **B15** chỉ ghi nhãn 13 nước
(10 ASEAN + nước mạnh nhất mỗi cụm) vì 73 nhãn trên cạnh 250,3pt chỉ còn 3,4pt
mỗi nhãn, dưới sàn 7pt của style guide; **B16** đặt khung hình bằng point chứ
không bằng pixel, vì không quy đổi được thì không kiểm được cái sàn ấy.

### Chord: Việt Nam nối vào đâu, và không nối vào đâu (T17)

`src/make_chord.py` gộp 73 nước thành **8 khối** suy thẳng từ `nodes.csv`: Việt
Nam tách riêng, ASEAN còn lại, Đông Á tách khỏi phần Á còn lại, rồi bốn châu.
Không có bảng gán tay — script tự kiểm **mọi nước thuộc đúng một khối** và in
bảng đối chiếu (2023: 73 nước, 73 đã gán, 0 chưa gán, 0 khối chồng nhau).

Bề dày dải là **tổng hai chiều** của phần vượt ngưỡng, theo **B13** như T15 —
nên hình này **không** nói chiều của luồng. Chiều là việc của T19 (Sankey), và
cố ý để dành cho nó.

| Bạn hàng của Việt Nam | 1995 | 2023 |
|---|---|---|
| Đông Á | 59,1% | **70,9%** |
| ASEAN còn lại | **33,4%** | 8,4% |
| Châu Mỹ | *không luồng nào vượt ngưỡng* | **18,5%** |
| Tổng giá trị | 6,6 tỷ USD | 514,9 tỷ USD |

Khối phân biệt bằng **vị trí**, không bằng màu — xem **B17**: không gian màu đã
hết chỗ cho bảng thứ ba, và điều đó đo được bằng `src/probe_colour_space.py`.

### Chiều của luồng, và hành lang hai đầu (T19)

`src/make_sankey.py` là hình **duy nhất** còn giữ chiều: T15 và T17 đều gộp hai
chiều theo B13, nên câu "hàng vào từ đâu, hàng ra đi đâu" chỉ hình này trả lời.

Bằng chứng của hành lang là **cán cân ngược dấu ở hai đầu**: Trung Quốc cấp
133,05 tỷ USD và mua lại 86,11 tỷ (**−46,94**), Hoa Kỳ cấp 9,83 tỷ và mua 95,16
tỷ (**+85,33**). Tiêu đề chỉ gọi là "hành lang" khi phép thử ngược dấu đó đạt ở
năm đang vẽ — năm 1995 hai đầu là Singapore và Nhật Bản, và hình tự nói ra.

Hình này dùng **đồ thị đầy đủ**, không lọc ngưỡng B4, nên tổng khớp đúng
`country_year.csv` tới từng xu. Vì thế **đừng so thẳng số của T19 với T17** —
chính là cái bẫy ghi ở A5. Phần nhạt trên thanh Việt Nam là *xuất trừ nhập*,
không phải giá trị tăng thêm trong nước (D2, D5).

### Bán cho ai, và qua bao nhiêu cửa (T20)

`src/make_time_multiples.py` vẽ bốn năm mốc, chung một thang trục ngang. Vẽ đủ
bốn mốc mới thấy **A9 chưa đủ**: số bạn hàng không giảm đều mà **đạt đỉnh 200
nước năm 2005** rồi lùi về 166 — thu hẹp 18 năm chứ không phải 8. So hai đầu
1995 → 2023 sẽ ra "tăng 68 nước", đúng số mà che mất câu chuyện, nên tiêu đề đi
tìm năm đỉnh. Xem **A13**.

### Rổ hàng được xây lại (T21)

`src/make_streamgraph.py` — điện tử 0,6% → **29,9%**, nông sản 42,9% → 11,6%,
tổng xuất khẩu gấp 75 lần. **Không** dùng nền lượn kiểu ThemeRiver: xuất khẩu
gấp 75 lần nên trên thang tuyến tính, cơ cấu năm 1995 chỉ dày 1,3% khung — tức
đúng thứ hình này sinh ra để kể lại là thứ không nhìn thấy. Tách hai tầng: tầng
trên là quy mô, tầng dưới chuẩn hóa 100% cho cơ cấu.

### Mặt phẳng quyết định — hình mang đề xuất (T31)

`src/make_decision_plane.py` là chỗ báo cáo **đề nghị một việc** thay vì chỉ mô
tả. RCA (bán đậm hơn hay nhạt hơn thế giới) trên trục ngang thang log, PCI (hàng
khó hay dễ) trên trục dọc, diện tích hình tròn là giá trị xuất khẩu.

Nhóm được đề xuất chọn bằng **quy tắc viết trong code**, không chọn tay: xuất
trên 1 tỷ USD, PCI dương, RCA trong `[0,5; 1,5)` và đang tăng, lấy hai nhóm PCI
cao nhất. Năm 2023 ra **thiết bị quang học – y tế** (RCA 0,75 → 0,91; PCI +0,93)
và **máy móc công nghiệp** (0,46 → 0,95; +0,78).

Viết thành quy tắc nên **thử lại được**: chạy trên 2015 thì nó chọn thiết bị
quang học và sắt thép, tám năm sau cả hai đi đúng hướng và sắt thép đã chạm RCA
**1,00**. Xem **A14** và quyết định **B18**.

## Quyết định đã chốt

| | |
|---|---|
| Năm mốc | **2023** (`REFERENCE_YEAR`) — mọi con số một-năm phải lấy năm này |
| Dữ liệu 2024 | **là số tạm** (`PROVISIONAL_YEARS`) — thiếu 1.781 cặp nước; dùng được cho giá trị, không dùng được cho đếm hay cấu trúc mạng |
| `is_focus` | **cả 10 nước ASEAN**, không chỉ Việt Nam |
| `export_value = 0` | loại bỏ — không phải một cạnh, cũng không phải một dòng xuất khẩu |
| `USP`, `ANS` | vẫn giữ trong `nodes.csv`; `USP` không có luồng nào suốt 30 năm và cũng vắng mặt trong file ECI |
| `sector_color` | đang là bảng màu tạm, phải thay ở T04 |
| Ngưỡng lọc cạnh | **chốt ở T10**: `THRESHOLD_SHARE = 0.00046` (tỷ lệ theo năm) + `FOCUS_TOPK = 3` |
| Mũi tên trên node-link | **không dùng** — đối ứng 0,84 nên hướng cạnh gần như vô nghĩa |
| Nhãn trên ma trận kề (T16) | **13 nước, không phải 73** — 73 nhãn trên cạnh 250,3pt chỉ còn 3,4pt mỗi nhãn, dưới sàn 7pt. Giữ 10 nước ASEAN + nước mạnh nhất mỗi cụm → 19,3pt (B15) |
| Khung hình của T16 | tính bằng **point** (`6,30 × 72 = 453,6`), không bằng pixel — có thế mới kiểm được sàn 7pt (B16) |

## Cấu trúc repo

```
global-ecom/
├── data/
│   ├── atlas/        # dữ liệu thô (bị .gitignore, trừ 3 file tra cứu nhỏ)
│   ├── processed/    # file trung gian — SINH LẠI, không commit
│   └── mock/         # dữ liệu giả đúng schema — CÓ commit
├── src/
│   ├── download_atlas.py      # tải dữ liệu thô, nối tiếp, kiểm MD5
│   ├── check_raw_data.py      # 8 mục kiểm tra toàn vẹn, cửa chặn
│   ├── reference_data.py      # tên nước tiếng Việt, vùng, hằng số chung
│   ├── build_intermediate.py  # atlas/ -> processed/ (5 file)
│   ├── analyze_network.py     # thống kê mạng + ngưỡng lọc (T09, T10)
│   ├── check_tree.py          # kiểm toàn vẹn cây HS92 (T11)
│   ├── make_mock.py           # sinh dữ liệu giả (T05)
│   ├── check_palette.py       # kiểm định bảng màu: mù màu, tương phản (T04)
│   ├── compute_metrics.py     # bậc, độ mạnh, betweenness, cộng đồng (T18)
│   ├── make_degree_loglog.py     # log-log phân bố bậc, kiểm scale-free (T09)
│   ├── make_node_link.py         # node-link mạng đã lọc, 73 nút (T15)
│   ├── make_adjacency_matrix.py  # hai ma trận kề: alphabet vs cụm (T16)
│   ├── make_chord.py          # chord 8 khối, Việt Nam làm trọng tâm (T17)
│   ├── make_sankey.py         # nhập → VN → xuất, hình duy nhất có chiều (T19)
│   ├── make_time_multiples.py # bán cho ai, bốn năm mốc (T20)
│   ├── make_streamgraph.py    # rổ hàng được xây lại 1995–2023 (T21)
│   ├── make_decision_plane.py # RCA × PCI — hình mang ĐỀ XUẤT (T31)
│   ├── check_readability.py   # kiểm cỡ chữ, khung, tương phản, mù màu (T24)
│   ├── probe_colour_space.py  # còn chỗ cho bảng màu mới không (B17)
│   ├── make_hierarchy_charts.py  # treemap + sunburst cây HS92 (T12, T13)
│   ├── make_small_multiples.py   # lưới 4 nước ASEAN (T14)
│   ├── build_report.py           # T27 ráp 10 mục -> output/bao-cao-cuoi.{md,html}
│   ├── export_cone_tree_glb.py   # cây nón 3D -> .glb (ngoài pipeline)
│   └── pptx_flat_3d_lighting.py  # gỡ đèn PowerPoint gắn cho mô hình 3D
├── docs/
│   ├── nhat-ky-cong-viec.md        # đã làm gì, nằm ở đâu — mở trước khi soạn slide
│   ├── phat-hien-va-quyet-dinh.md  # phát hiện A1–A17, quyết định B1–B23, hạn chế D1–D5
│   ├── cau-hoi-nghien-cuu.md       # câu hỏi, thông điệp, đối tượng (T01)
│   ├── style-guide.md              # màu, font, cỡ hình, quy ước nhãn (T04)
│   ├── nguon-du-lieu-vn-asean.md   # nguồn dữ liệu và vì sao chọn nguồn đó
│   └── kien-thuc-nen-tang.md       # kiến thức kinh tế tối thiểu để đọc số
├── .report/
│   ├── final/        # báo cáo cuối — MỘT FILE MỘT MỤC, Markdown (B21, B23)
│   │   ├── 00-tom-tat.md           # bản một trang
│   │   ├── 01-mo-dau.md            # câu hỏi, thông điệp, bố cục, danh mục hình
│   │   ├── 02-phuong-phap-luan.md  # Phương pháp luận (T25)
│   │   ├── 03-quy-mo.md            # hồi 1 — Quy mô
│   │   ├── 04-cau-truc.md          # hồi 2 — Cấu trúc
│   │   ├── 05-vi-tri-viet-nam.md   # hồi 3 — Vị trí Việt Nam
│   │   ├── 06-y-nghia.md           # hồi 4 — Ý nghĩa
│   │   ├── 07-de-xuat.md           # Đề xuất (T27)
│   │   ├── 08-han-che-ket-luan.md  # hạn chế D1–D5 + kết luận
│   │   └── 09-phu-luc.md           # 5 mục phương pháp chuyển về đây
│   ├── midterm/      # bản dịch chương 9 giữa kỳ (HTML)
│   └── overleaf/     # bản dịch chương 9 giữa kỳ (LaTeX)
└── phan-cong-cong-viec.xlsx
```

## Chạy pipeline

Cả sáu script **chỉ dùng thư viện chuẩn** — chạy được ngay, không cần cài gì.

```bash
python src/download_atlas.py        # 0. tải dữ liệu thô + kiểm MD5
python src/check_raw_data.py        # 1. kiểm tra dữ liệu thô, phải báo DAT
python src/build_intermediate.py    # 2. sinh 5 file trung gian trong processed/
python src/analyze_network.py       # 3. thống kê mạng + bảng ngưỡng (T09, T10)
python src/make_mock.py             # 4. sinh dữ liệu giả để vẽ song song
python src/check_palette.py         # 5. kiểm định bảng màu (T04), thoát 1 nếu hỏng
```

### Hai script cho slide, không thuộc pipeline

Dùng cho mục "cây nón 3D" của bài thuyết trình, chạy riêng khi cần:

```bash
python src/export_cone_tree_glb.py notebooks/exports   # cần numpy + pandas
python src/pptx_flat_3d_lighting.py slide.pptx --glb notebooks/exports/cone_tree.glb
```

`export_cone_tree_glb.py` xuất cây nón ASEAN (10 nước × 10 ngành) ra một file
`.glb` để chèn vào PowerPoint bằng *Chèn > Mô hình 3D*. Màu lá lấy từ
`SECTOR_PALETTE`. Vật liệu đặt màu ở `emissive`, `baseColor` đen và
`metallic = 1` nên không phản chiếu đèn.

`pptx_flat_3d_lighting.py` xử lý một chuyện PowerPoint không cho tắt trong
giao diện: mỗi mô hình 3D bị tự gắn ba đèn điểm `am3d:ptLight` tạo vùng lóa
trên hình cầu. Script xóa các phần tử đó trong `ppt/slides/slideN.xml`, giữ
đèn môi trường, và ghi ra file mới — **không ghi đè file gốc**. Chỉ dùng thư
viện chuẩn.

### File sinh ra trong `data/processed/`

| File | Nội dung | Dòng |
|---|---|---|
| `nodes.csv` | nước: mã, tên tiếng Việt, vùng, châu lục, `is_focus` | 233 |
| `edges.csv` | luồng xuất khẩu song phương 1995–2024, kèm `log_value` | 750.855 |
| `tree.csv` | cây sản phẩm HS92 bốn tầng, có `sector_id` và màu tạm | 6.390 |
| `country_product.csv` | nước × nhóm hàng HS2 × năm, kèm **RCA** tự tính và PCI | 539.986 |
| `country_year.csv` | nước × năm: **ECI**, thứ hạng, COI, diversity | 6.755 |
| `network_stats.csv` | mỗi năm một dòng: nút, cạnh, mật độ, đối ứng, Gini | 30 |
| `degree_distribution.csv` | phân bố bậc dạng dài, có `ccdf` — sẵn cho log-log | 1.094 |
| `threshold_coverage.csv` | 21 phương án lọc cạnh, bằng chứng cho T10 | 21 |
| `metrics.csv` | chỉ số mạng theo nước, mỗi nước 2 dòng — xem dưới | 304 |
| `metrics_top20.csv` | top 20 nước xuất khẩu kèm chỉ số mạng, cho báo cáo | 20 |

Cả mười file đều bị `.gitignore` loại trừ — sinh lại bằng lệnh trên, không commit.

## Biểu đồ và chỉ số — cần thư viện ngoài

```bash
python -m pip install -r requirements.txt

python src/check_tree.py              # T11 kiểm cây HS92, thoát 1 nếu cây hỏng
python src/compute_metrics.py         # T18 metrics.csv + bảng top 20
python src/make_degree_loglog.py      # T09 log-log phân bố bậc
python src/make_node_link.py          # T15 node-link mạng đã lọc
python src/make_adjacency_matrix.py   # T16 hai ma trận kề, alphabet vs cụm
python src/make_adjacency_matrix.py --year 1995   # năm đối chứng
python src/make_chord.py              # T17 chord 8 khối, VN làm trọng tâm
python src/make_chord.py --year 1995  # năm đối chứng
python src/make_sankey.py             # T19 Sankey nhập → VN → xuất
python src/make_sankey.py --year 1995 # năm đối chứng
python src/make_time_multiples.py     # T20 bốn năm mốc, bán cho ai
python src/make_time_multiples.py --direction nhap   # phía mua vào
python src/make_streamgraph.py        # T21 dòng chảy cơ cấu 1995–2023
python src/make_decision_plane.py     # T31 mặt phẳng quyết định (đề xuất)
python src/make_decision_plane.py --year 2015 --since 2007   # thử lại quy tắc
python src/check_readability.py       # T24 kiểm khả năng đọc, ĐẠT thì trả 0
python src/make_hierarchy_charts.py   # T12, T13 treemap + sunburst
python src/make_small_multiples.py    # T14 lưới 4 nước ASEAN
python src/make_decision_plane.py --year 2007 --since 1999  # quy tắc chạy ở 2007
python src/build_report.py            # T27 ráp báo cáo cuối từ .report/final/
python src/build_report.py --embed    # bản HTML một file, nhúng PNG (~8,6 MB)
```

Biểu đồ ra `output/` dưới hai dạng `.html` và `.png`; thư mục này bị
`.gitignore` loại trừ.

### `metrics.csv` có hai dòng cho mỗi nước

Mạng đầy đủ năm 2023 có mật độ **0,518** — quá nửa số cặp nước trên đời có
thương mại trực tiếp. Trên một đồ thị dày như thế, gần như không đường đi ngắn
nhất nào phải vòng qua nước thứ ba, nên **betweenness sụp về 0 ở 74,5% số
nước**: nó không còn đo được gì. Vì vậy cột `graph` phân biệt hai đồ thị:

| `graph` | Là gì | Lấy gì từ đó |
|---|---|---|
| `full` | toàn bộ 27.535 cạnh | **độ mạnh** (tiền) và thị phần thế giới |
| `filtered` | 416 cạnh qua ngưỡng T10 | **betweenness và cộng đồng** — đây đúng là đồ thị T15–T17 sẽ vẽ |

Hệ quả phải nhớ: `strength_out` ở dòng `filtered` là con số **đã bị cắt cụt**,
không phải kim ngạch xuất khẩu. Muốn tiền thì lấy dòng `full` — cột
`world_export_share` cố tình để rỗng ở dòng `filtered` để không ai dán nhầm.

Cộng đồng dò bằng Louvain trên bản vô hướng, hạt giống cố định `--seed 42`.
Script tự chạy lại 20 hạt giống khác để báo độ ổn định; với năm 2023 phân hoạch
**ổn định tuyệt đối** — 3 cụm, modularity 0,337, 100% số cặp nước giữ nguyên
quan hệ cùng cụm hay khác cụm.

## Tải dữ liệu thô

Nguồn: **Atlas of Economic Complexity**, Harvard Growth Lab — hai bộ trên Harvard Dataverse:

| Bộ dữ liệu | DOI |
|---|---|
| International Trade Data (HS, 92) | [10.7910/DVN/T4CHWJ](https://doi.org/10.7910/DVN/T4CHWJ) |
| Classifications Data | [10.7910/DVN/3BAL1O](https://doi.org/10.7910/DVN/3BAL1O) |

### Cách làm

```bash
python src/download_atlas.py --list   # xem file nào thiếu hoặc hỏng
python src/download_atlas.py          # tải — tự nối tiếp khi đứt, tự kiểm MD5
python src/check_raw_data.py          # phải báo DAT mới được chạy pipeline
```

Dataverse công bố kích thước và mã MD5 chính thức cho từng file; script đọc đúng
hai con số đó rồi đối chiếu với file vừa tải về. Đường truyền tới Dataverse rất
chậm (~30 KB/s, tức 29 MB mất khoảng 18 phút) nên script tải **nối tiếp**: đứt
giữa chừng thì chạy lại, nó đi tiếp từ chỗ đứt chứ không tải lại từ đầu. File cũ
sai MD5 được đổi tên thành `*.broken`, không bị xóa.

### Danh sách file

| File trên Dataverse | Lưu thành | Kích thước (byte) | MD5 |
|---|---|---|---|
| `hs92_country_country_year.csv` | `cc_year.csv` | 30.767.251 | `9c39659168dd5212f745572ba35b2a5c` |
| `hs92_country_product_year_2.csv` | `cp_year_hs2.csv` | 38.135.675 | `b767f3c2dad599ecce2204a4b5ba9fa6` |
| `hs92_country_year.csv` | giữ nguyên tên | 363.501 | `9467cc0686c2380659f892948509115d` |
| `hs92_data_dictionary.csv` | giữ nguyên tên | 3.257 | — |
| `location_country.csv` | giữ nguyên tên | 9.677 | `9cc1c0eb7624f2a32d55b6dec1b6b21a` |
| `product_hs92.csv` | giữ nguyên tên | 837.108 | `c4a7dc2bbb9f6711b99bd983dc610d79` |

Số liệu theo phiên bản v18 (22-04-2026) của bộ HS92 và v12 (04-05-2026) của bộ
Classifications. Script luôn đọc giá trị mới nhất từ API nên không bị lệch khi
Growth Lab phát hành phiên bản mới — bảng trên chỉ để tra tay.

### Nếu muốn tải bằng trình duyệt

Mở trang DOI ở trên, tick file cần lấy rồi bấm *Download*. Hoặc tải thẳng theo
số hiệu file:

```
https://dataverse.harvard.edu/api/access/datafile/13685107   # cc_year
https://dataverse.harvard.edu/api/access/datafile/13685112   # cp_year_hs2
```

Tải kiểu này **bắt buộc phải tự kiểm tra lại**, vì trình duyệt không báo gì khi
kết nối đứt giữa chừng — đúng cách mà `cc_year.csv` đã hỏng:

```powershell
certutil -hashfile data\atlas\cc_year.csv MD5
```

Mã in ra phải trùng với cột MD5 ở bảng trên. Chỉ so kích thước là chưa đủ, nhưng
lệch kích thước thì chắc chắn file hỏng.

## Báo cáo cuối đã ráp xong (T27)

Một file một mục, Markdown (quyết định **B21**), ráp bằng `src/build_report.py`
ra `output/bao-cao-cuoi.md` và `output/bao-cao-cuoi.html`. Bố cục chốt ở **B23**:
bốn hồi mà checklist nộp bài đòi — **Quy mô → Cấu trúc → Vị trí Việt Nam → Ý
nghĩa** — kẹp giữa Mở đầu và Phương pháp luận ở trước, Đề xuất và Kết luận ở sau,
rồi Phụ lục. Đo được: **khoảng 19 trang thân + 3 trang phụ lục** (11.100 chữ văn
xuôi, không kể bảng), **14 hình** chèn đúng mục.

`build_report.py` **tự kiểm tham chiếu chéo**: nó so mọi `§x.y` trong bài với danh
sách tiêu đề có thật và in ra những tham chiếu treo. Đó là phép kiểm bắt buộc, vì
T27 đã đổi số hiệu toàn bộ (§2.4 cũ → §A.1, §3.6 cũ → §5.3 …) nên một tham chiếu
sót lại sẽ trỏ vào mục không còn tồn tại. Hiện **0 tham chiếu treo**.

### Phương pháp luận (T25) — `02-phuong-phap-luan.md` + `09-phu-luc.md`

12 tiểu mục, **mỗi con số kèm lệnh lấy lại được**. Nội dung đáng chú ý:

- **Vì sao T19 dùng đồ thị đầy đủ còn T15–T17 dùng đồ thị đã lọc** (§2.5). Đây
  không phải sở thích: dùng đồ thị đã lọc cho Sankey thì cán cân Việt Nam 2023
  **đổi dấu** — từ **+53,45 tỷ USD** thành **−15,17 tỷ USD** — vì ngưỡng cắt phía
  bán ra (166 → 8 nước) nặng hơn phía mua vào (149 → 10 nước). Phát hiện **A15**.
- **Hai chỗ lệch của cây HS92** (§A.3), giữ nguyên kết quả kiểm không sạch: nút
  `3501` (casein) nằm dưới HS2 `34` thay vì `35`, nhưng cùng ngành 6 nên không tổng
  ngành nào lệch; mã `XXXX` dưới HS2 `99` là mã giữ chỗ của Atlas, và nhóm `99` ấy
  chiếm **11,83%** rổ hàng Việt Nam (45,60 tỷ USD, RCA 2,4408, PCI −1,206) nên bị
  loại thẳng khỏi quy tắc chọn đề xuất.
- **Hạn chế D1–D5** nói thẳng, kèm số: 2023 không phải 2024 (thiếu 1.781 cặp nước),
  ECI đo hàng *đi qua* chứ chưa hẳn hàng *ở lại*, node-link vứt 98,5% số cạnh, dữ
  liệu dừng ở HS2, và không có bảng vào–ra.
- **Vì sao tin được đề xuất** (§7.1): nó là một quy tắc trong code, nên thử lại
  được trên quá khứ — chạy trên 2015 thì chọn thiết bị quang học và sắt thép, tám
  năm sau sắt thép chạm **RCA 1,00**.

```bash
# Lấy lại các số của §2.5 và §A.3
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_sankey.py
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/check_tree.py
```

### Phát hiện (T26) — nay là bốn hồi, `03-quy-mo.md` … `06-y-nghia.md`

Chín tiểu mục theo mạch lập luận, không theo thứ tự số A. Phần đáng chú ý nhất là
một **phát hiện sửa chính câu trung tâm của đồ án**:

- **Phép đếm bạn hàng KHÔNG bền** (§5.3, phát hiện **A16**). Câu cũ: "số bạn hàng
  giảm từ 181 xuống 166". Số đúng, phép đo thì không: **47 nước** rời khỏi danh sách
  giữa 2002 và 2023 chỉ mang theo **0,59%** kim ngạch, và đặt một mức sàn vào là kết
  luận **đảo chiều** — trên 100 triệu USD thì số kênh **tăng 13 → 83**. Phép đo bền
  là tập trung giá trị: HHI đáy **0,0662** (2013) → **0,1226** (2023), **cao hơn cả
  mức 1995**; top-3 nhận **52,41%**. Việt Nam đi từ **dưới** trung vị thế giới (2015)
  lên **hạng 30/97** nước xuất trên 10 tỷ USD, và là nước **tập trung nhất ASEAN**
  (gần gấp đôi Thái Lan).
- **Ba kết quả cấu trúc mạng đi ngược trực giác** (§4.1): mật độ **0,5183** nên mạng
  không scale-free (R² của phép khớp lũy thừa chỉ **0,51**); kết nối dàn đều ra
  (lệch khỏi phân bố đều 0,180 → **0,056**) mà giá trị thì không (Gini đứng yên
  0,9548 → 0,9569); và betweenness **bằng 0 ở 172/231 nước**.
- **ASEAN không hiện ra như một cộng đồng** (§4.2) — ba phép đo độc lập cùng nói
  thế: Louvain, tỷ trọng tiền (**7,77%** so với **52,41%**), và chord 1995 vs 2023.

Hai chỗ ghi sai trong sổ phát hiện đã được sửa cùng lúc: **A13** (đỉnh số bạn hàng
là **2002 với 208 nước**, không phải 2005 với 200 — con số cũ chỉ đúng trong bốn năm
mốc được vẽ) và **A4** (dòng "top 416" gộp hai con số khác nhau: 416 cạnh lớn nhất
phủ **68,50%** giá trị, còn quy tắc B4 — cũng 416 cạnh — phủ **67,84%**, vì nó đánh
đổi 0,66 điểm phần trăm để giữ đủ 10 nước ASEAN).

Tiêu đề hình **T20** đã sửa theo: nó từng in *"số bạn hàng đã đạt đỉnh 200 nước năm
2005"* — câu sai, vì nó tìm đỉnh chỉ trong bốn năm được vẽ. Nay nó tìm trên **cả
chuỗi 1995–2023** và dựng khẳng định từ tỷ trọng top-3, còn khối KIỂM CHỨNG in **cả
hai** phép đo kèm bốn mức sàn để không ai dùng lại phép không bền mà không thấy ngay
nó không bền.

```bash
# Lấy lại các số của §5.3 (cả hai chiều)
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_time_multiples.py
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_time_multiples.py --direction nhap
```

### Đề xuất và phép thử lại (T27) — `07-de-xuat.md`

Báo cáo kết bằng một đề xuất, không dừng ở mô tả (**B18**): dồn ưu tiên vào **thiết
bị quang học – đo lường – y tế** (RCA 0,905; PCI +0,934) và **máy móc công nghiệp**
(0,954; +0,783). Đề xuất do **quy tắc trong `make_decision_plane.py`** chọn, nên
chạy lại được trên quá khứ — và T27 đã chạy thêm một năm nữa:

| Chạy quy tắc ở | Nó chọn | Tám năm sau |
|---|---|---|
| 2007 | máy điện – điện tử, RCA 0,573 | RCA **2,230**, xuất **3,4 → 115,4 tỷ USD** |
| 2015 | thiết bị quang học 0,751 · sắt thép 0,604 | 0,905 · **1,003 — vượt ngưỡng** |
| 2023 | thiết bị quang học 0,905 · máy móc công nghiệp 0,954 | *đề xuất của báo cáo* |

Phát hiện **A17** là **nền so sánh** cho ba lần ấy: RCA không tự đi lên — trong 97
nhóm hàng chỉ **45,4%** tăng giữa 2015 và 2023, trung vị **−0,0178**, còn nhóm đã có
RCA ≥ 1,5 thì chỉ **25%** tăng tiếp. A17 cũng nói thẳng chỗ yếu: điều kiện mang sức
dự báo là **PCI > 0** (62,8% tăng, so với 31,5% ở hàng dễ) chứ không phải dải RCA
0,5–1,5 (40,7%, kém cả mức bình quân), và lớp thoả trọn quy tắc chỉ có 6 nhóm — quá
nhỏ để kết luận thống kê.

```bash
# Lấy lại bảng ba lần chạy ở §7.2
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_decision_plane.py --year 2007 --since 1999
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_decision_plane.py --year 2015 --since 2007
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_decision_plane.py --year 2023
```

## Quy ước git

Dữ liệu thô không được commit (Nguyên tắc #5, Checklist #19). `.gitignore` đã cấu hình sẵn.

`data/atlas/cc_year.csv` (28 MB) **hiện đang bị theo dõi từ trước**. Thêm vào `.gitignore` không tự gỡ nó ra. Cần chạy lệnh sau — **thống nhất với cả nhóm trước khi chạy**, vì sau khi pull, file sẽ biến mất khỏi máy hai người kia và họ phải tải lại:

```bash
git rm --cached data/atlas/cc_year.csv
git commit -m "Gỡ dữ liệu thô khỏi git theo Nguyên tắc #5"
```

Lệnh này chỉ gỡ khỏi lần commit tới, không xóa khỏi lịch sử. Repo `.git` hiện mới 9,6 MB nên chưa cần viết lại lịch sử.

## Ghi chú

- `docs/style-guide.md` — **bảng màu, font, cỡ hình, quy ước nhãn** (T04)
- `docs/cau-hoi-nghien-cuu.md` — **T01: câu hỏi + thông điệp + đối tượng** (bản nháp, chờ nhóm duyệt)
- `docs/phat-hien-va-quyet-dinh.md` — **số liệu cho báo cáo + quyết định đã chốt**
- `docs/nguon-du-lieu-vn-asean.md` — khảo sát các nguồn dữ liệu thương mại
- `docs/kien-thuc-nen-tang.md` — kiến thức kinh tế nền cho người làm dữ liệu

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
| Lệch khỏi phân bố đều ¹ | 0,180 | **0,056** |

¹ khoảng lệch lớn nhất giữa CCDF thật và CCDF của một phân bố đều hoàn toàn
trên dải bậc. Càng gần 0 thì các nước càng trải đều. Đo bằng
`src/make_degree_loglog.py`.

Bậc xuất khẩu 2023 (số bạn hàng): min 0 · p25 62 · **trung vị 116** · p75 177 ·
p90 210 · max 226.

Các nước trải **gần như đều** trên toàn dải. Đo cụ thể: CCDF lệch khỏi một phân
bố đều hoàn toàn nhiều nhất **0,056**.

Ba hệ quả:

1. **Mật độ 51,8%** — hơn một nửa mọi cặp nước có giao dịch. Mạng xã hội hay
   mạng trích dẫn thường dưới 1%. Đây là lý do không thể vẽ thẳng 27.535 cạnh.
2. **Không có hub theo nghĩa tô-pô.** Không tồn tại nhóm nhỏ nối với tất cả
   trong khi phần còn lại nối với vài nước — vì gần như ai cũng nối với nhiều.
3. **Biểu đồ log-log của T09 không ra đường thẳng.** Nó đi ngang rồi rơi dốc
   đứng ở mép phải. **Đó không phải lỗi dữ liệu, đó là kết quả.** Phải nói rõ
   câu này trong báo cáo, kèm con số 0,056, nếu không người đọc sẽ tưởng vẽ sai.

Hình đã vẽ: `output/degree_loglog_2023.{html,png}` · `src/make_degree_loglog.py`.
Để không ai phải tin vào mắt mình, hình vẽ kèm **đường thẳng khớp nhất** (bình
phương tối thiểu trên log-log) và ba con số của phép khớp đó, năm 2023:

| Phép khớp lũy thừa, bậc xuất khẩu 2023 | |
|---|---|
| R² | **0,51** — đường thẳng chỉ giải thích được một nửa biến thiên |
| chỗ lệch tệ nhất | **41,3 lần** |
| đòi CCDF > 100% ở | mọi bậc dưới **31** — một đòi hỏi vô nghĩa, vì CCDF là tỉ lệ |

Và một kết quả mới thấy khi dựng hình: **mạng không chỉ dày thêm, nó còn đều
ra.** Năm 1995 phân bố còn lệch 0,180 khỏi mức đều — vẫn còn hẳn một lớp nước ít
bạn hàng; năm 2023 chỉ còn 0,056. Đặt cạnh Gini trọng số cạnh gần như đứng yên
(0,955 → 0,957), ra một câu gọn cho phần kết luận: **ba mươi năm toàn cầu hoá
san phẳng chuyện “ai nối với ai”, nhưng không san phẳng chuyện “luồng nào lớn”.**

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

### A7. Betweenness đo được gì, và nó phụ thuộc vào một lựa chọn tùy ý

`data/processed/metrics.csv` · `src/compute_metrics.py`

Hệ quả trực tiếp của A3. Mật độ 0,518 nghĩa là quá nửa số cặp nước đã nối
thẳng, nên gần như không đường đi ngắn nhất nào phải vòng qua nước thứ ba:

| | Mạng đầy đủ | Mạng đã lọc |
|---|---|---|
| Nút / cạnh | 231 / 27.535 | 73 / 416 |
| Số nước có betweenness = 0 | **172 (74,5%)** | 58 (79,5%) |

**Trên mạng đầy đủ, betweenness gần như không phân biệt được ai với ai.** Nên
mọi chỉ số cấu trúc của đồ án tính trên **mạng đã lọc** — cũng chính là mạng
T15–T17 sẽ vẽ, nên số trong bảng khớp được với hình. Riêng **độ mạnh (tiền)
vẫn phải lấy từ mạng đầy đủ**: kim ngạch xuất khẩu là đại lượng có thật, không
được phụ thuộc vào ngưỡng do ta tự chọn.

Chỗ thứ hai đáng nói hơn. networkx hiểu trọng số là **khoảng cách**, mà giá trị
thương mại thì ngược lại, nên phải nghịch đảo — và **chính phép nghịch đảo đó
đổi kết luận**:

| | Số nước có betweenness > 0 | Việt Nam |
|---|---|---|
| Có trọng số (1/giá trị) | 15 / 73 | **0,000** |
| Không trọng số | 37 / 73 | 0,005 — hạng 15/73 |

Có trọng số thì mọi đường ngắn nhất dồn hết vào ba luồng khổng lồ (CHN 0,550 ·
DEU 0,304 · USA 0,200) và Việt Nam **đúng bằng 0**; bỏ trọng số thì Việt Nam là
một cầu nối nhỏ nhưng có thật. Hai con số đều đúng, chúng trả lời hai câu hỏi
khác nhau. `metrics.csv` giữ **cả hai cột**, và bất kỳ hình hay câu nào dùng
betweenness đều phải ghi rõ đang dùng cột nào.

Kèm theo đó: hạng betweenness đọc một mình là **bẫy**. Việt Nam "hạng 16/73"
nghe như đứng thứ 16, thật ra là đồng hạng với 57 nước cùng bằng 0. Nên
`metrics.csv` có luôn cột `n_tied_betweenness`.

### A8. ASEAN không hiện ra như một cộng đồng

`data/processed/metrics.csv` · Louvain, `--seed 42`

Phân hoạch **ổn định tuyệt đối**: 20 hạt giống khác nhau đều ra 3 cụm,
modularity 0,337, 100% số cặp nước giữ nguyên quan hệ cùng cụm hay khác cụm.
Nên kết quả dưới đây không phải may rủi của một lần chạy.

**Cả 10 nước ASEAN rơi vào cùng một cụm — cụm 0 — chung với Trung Quốc, Nhật
Bản, Hàn Quốc, Ấn Độ, vùng Vịnh và Úc.** Thuật toán không tìm thấy ASEAN. Nó
tìm thấy một khối Á–Thái Bình Dương lấy Trung Quốc làm tâm, và ASEAN tan vào
trong đó.

Đo thẳng trên `edges.csv` thì thấy vì sao: trong 385,5 tỷ USD Việt Nam xuất năm
2023, chỉ **7,8%** đi sang 9 nước ASEAN còn lại, trong khi **ba thị trường đầu
chiếm 52,4%** (Hoa Kỳ 95,2 tỷ · Trung Quốc 86,1 tỷ · Hàn Quốc 20,8 tỷ). Láng
giềng về địa lý, không phải láng giềng về thương mại.

**Hệ quả cho hình vẽ.** Tô màu theo cụm ở T15 **không** làm ASEAN nổi lên —
cả khối chìm trong một màu cùng Trung Quốc. Việt Nam phải được làm nổi bằng
viền đậm theo quyết định B12, chứ không trông cậy vào màu cụm.

Hình đã vẽ: `output/node_link_2023.{html,png}` · `src/make_node_link.py`. Nhìn
vào hình thì thấy đúng như vậy: 9 nhãn ASEAN nằm rải rác trong khối xanh, không
thành mảng riêng ở đâu cả. Trên đồ thị đã lọc, Việt Nam còn **12 cặp nước** vượt
ngưỡng (trong 166 bạn hàng thật), và cặp dày nhất là **Trung Quốc — 219,2 tỷ
USD hai chiều**, gấp **2,3 lần** cặp đứng thứ hai là Hoa Kỳ (95,2 tỷ, và chỉ một
chiều lọt ngưỡng). Ba cụm nên gọi theo nước mạnh nhất chứ đừng gọi theo châu
lục: cụm "Trung Quốc" có 41 nước nhưng gồm cả Úc, Brazil, Nam Phi và vùng Vịnh —
29/41 là châu Á, phần còn lại là bạn hàng của khối đó.

### A9. Tiền tăng gấp đôi, số kênh thì ít đi

`data/processed/edges.csv` · so 2015 với 2023

| Việt Nam | 2015 | 2023 | |
|---|---|---|---|
| Xuất khẩu | 169,4 tỷ USD | 385,5 tỷ USD | **×2,28** |
| Số bạn hàng xuất | 181 | 166 | **−15** |

Con số −15 chỉ có nghĩa khi đặt cạnh phần còn lại của thế giới, nên đã đếm:
trong 230 nước có mặt cả hai năm, **130 nước tăng** số bạn hàng, 85 giảm, 15
giữ nguyên; **trung vị là +1**. Mạng nói chung dày thêm (27.323 → 27.535 cạnh).
Việt Nam đi **ngược** xu thế đó.

Đây không phải lỗ hổng dữ liệu — nếu Atlas bỏ sót nước nhỏ thì cả bảng cùng
giảm, mà thực tế đa số tăng. Và nó nói đúng câu trung tâm của báo cáo bằng một
cặp số duy nhất: **gấp 2,28 lần tiền, qua ít kênh hơn 15 kênh.** Dùng được
thẳng cho T20 (small multiples theo thời gian).

Chưa trả lời được **vì sao**: dữ liệu này không cho biết mất bạn hàng nào, hay
mất vì thương mại thật sự dừng hay vì dồn qua trung gian. Nếu viết vào báo cáo
thì viết đúng phần đo được, đừng đoán phần còn lại.

### A10. Khối Thái Bình Dương tách làm đôi, và Việt Nam ở lại phía đổi tâm

`data/processed/edges.csv` · `src/make_adjacency_matrix.py --year 1995|2023`

Ma trận kề của T16 bắt được điều mà một năm đứng một mình không nói ra. Cùng
một quy tắc lọc, cùng Louvain `--seed 42`, hai năm cho hai bức tranh khác hẳn:

| | 1995 | 2023 |
|---|---|---|
| Nút / luồng vượt ngưỡng | 63 / 383 | 73 / 416 |
| Số cụm, cỡ từng cụm | 3 — **34 / 27 / 2** | 3 — **41 / 25 / 7** |
| Nước mạnh nhất mỗi cụm | **Hoa Kỳ** · Đức · Brazil | **Trung Quốc** · Đức · Hoa Kỳ |
| Modularity | 0,343 | 0,337 |
| **Giá trị nằm trong khối** | **83,8%** | **69,7%** |
| Mật độ ô trong khối / ngoài khối | 15,6% / 4,7% — gấp 3,31 | 12,9% / 4,1% — gấp 3,14 |
| Khoảng cách tới đường chéo: mã nước → cụm | 0,366 → **0,165** | 0,398 → **0,258** |

Ba câu đáng viết, theo thứ tự quan trọng:

1. **Khối lớn đổi tâm.** Năm 1995 khối 34 nước là một khối *xuyên Thái Bình
   Dương*: Hoa Kỳ, Nhật Bản, Canada và cả 10 nước ASEAN trong cùng một ô.
   Năm 2023 Hoa Kỳ đã **ra khỏi** khối đó và đứng đầu một khối Bắc Mỹ riêng 7
   nước, còn khối cũ nở lên 41 nước với **Trung Quốc** ở tâm. Việt Nam ở
   nguyên trong khối lớn suốt — nhưng cái khối ấy đã đổi người cầm trịch.
2. **Cấu trúc khối LỎNG đi, không chặt lại.** Tỉ lệ giá trị nằm trong khối rơi
   từ 83,8% xuống 69,7% — 14,1 điểm phần trăm. Tức là đồng tiền lớn ngày càng
   đi **qua** ranh giới khối chứ không ở trong. Lưu ý khi viết: modularity gần
   như đứng yên (0,343 → 0,337), nên đây **không** phải "phân hoạch kém đi" mà
   là "cùng một chất lượng phân hoạch, nhưng giá trị thoát ra ngoài khối nhiều
   hơn". Hai số đo hai thứ khác nhau, đừng gộp.
3. **Việt Nam dày lên thấy được trên hình.** Hàng và cột Việt Nam năm 1995 chỉ
   có **3 ô xuất + 3 ô nhập** vượt ngưỡng (và cả 6 ô đó tồn tại được là nhờ
   bảo hiểm top-3 ASEAN của B4, xem đoạn thứ 3 của B4); năm 2023 là **8 ô xuất
   + 10 ô nhập**. Luồng lớn nhất đổi từ *xuất sang Nhật Bản 1,5 tỷ USD* thành
   *nhập từ Trung Quốc 133,0 tỷ USD*.

Một chỗ phải cẩn thận khi so hai năm: n khác nhau (63 so với 73) nên khoảng
cách tới đường chéo và mật độ khối **không so trực tiếp được** giữa hai năm;
chúng chỉ so được giữa hai cách xếp **trong cùng một năm**. Tỉ lệ giá trị
trong khối thì so được, vì nó không phụ thuộc thứ tự lẫn cỡ ma trận.

Hình đã vẽ: `output/adjacency_{alpha,cluster}_{1995,2023}.{html,png}`.

---

### A11. Việt Nam rời quỹ đạo ASEAN, vào hành lang Đông Á – châu Mỹ

Chord T17 chia 73 nước thành 8 khối (Việt Nam tách riêng, ASEAN còn lại, Đông Á,
Châu Á còn lại, rồi bốn châu). Nhìn riêng các dải chạm vào Việt Nam:

| Bạn hàng của Việt Nam | 1995 | 2023 |
|---|---|---|
| Đông Á | 59,1% | **70,9%** |
| ASEAN còn lại | **33,4%** | 8,4% |
| Châu Mỹ | *không có luồng nào vượt ngưỡng* | **18,5%** |
| Châu Âu | 7,5% | 2,3% |
| Số khối nối tới | 3 trên 7 | 4 trên 7 |
| Tổng giá trị | 6,6 tỷ USD | 514,9 tỷ USD — **gấp 78 lần** |

Năm 1995, bạn hàng lớn thứ hai của Việt Nam là **chính ASEAN** (33,4%). Đến 2023
chỗ đó thuộc về **châu Mỹ** (18,5%) — một khối mà năm 1995 Việt Nam **không có
lấy một luồng nào vượt ngưỡng** — còn ASEAN tụt xuống 8,4%. Luồng lớn nhất đổi
từ *Singapore bán sang Việt Nam 1,8 tỷ* thành *Trung Quốc bán sang Việt Nam
133,0 tỷ*.

Đặt cạnh **A8** (ASEAN không hiện ra như một cộng đồng) thì hai phát hiện này nói
cùng một điều, từ hai phép đo độc lập: **lát cắt "Việt Nam – ASEAN" của đề tài là
một câu hỏi, không phải một tiền đề.** Việt Nam hội nhập vào hành lang Đông Á –
châu Mỹ chứ không hội nhập vào ASEAN. Đây là chất liệu tốt cho báo cáo, nhưng
phải nói thẳng chứ đừng để người đọc tưởng nhóm đã giả định ngược lại.

Hai con số nền đi kèm, đo trên cùng phân hoạch:

- **Thương mại nội khối lỏng đi:** 60,5% → **48,4%** giá trị nằm trong nội bộ một
  khối. Cùng chiều với A10 (83,8% → 69,7% trên phân hoạch Louvain) — hai phân
  hoạch khác nhau, cùng một kết luận.
- **Trọng tâm dịch sang Đông Á:** cung Đông Á nở từ 23,9% lên 30,1% tổng giá trị
  chạm vào các khối, trong khi cung châu Âu co từ 37,9% xuống 27,6%.

Cảnh báo khi trích: mọi tỉ lệ ở đây tính trên **phần vượt ngưỡng**, không phải
toàn bộ thương mại. Quy tắc B4 giữ lại top-3 bạn hàng của nước trọng tâm nên các
luồng nhỏ của Việt Nam không bị xoá ở **cả hai năm** — so sánh vẫn cùng một thước.

Lấy lại số: `PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_chord.py --year 1995`
Hình đã vẽ: `output/chord_bloc_{1995,2023}.{html,png}`.

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
| B13 | **Node-link gộp hai chiều thành MỘT cạnh** | 416 cạnh có hướng rút còn 271 cặp nước. Đối ứng 0,84 nên vẽ hai nửa cạnh song song chỉ làm dày hình mà không thêm thông tin. Độ dày = **tổng giá trị hai chiều của phần vượt ngưỡng**, không phải tổng thương mại hai nước — có cặp chỉ một chiều lọt ngưỡng |
| B14 | **Cụm Louvain dùng bảng màu RIÊNG, khóa theo thứ hạng cỡ cụm** | quy tắc §3.1 cấm mượn 10 màu ngành sang chỉ cụm. `COMMUNITY_PALETTE` đã qua cùng bộ kiểm: ΔE 24,7 mắt thường, 13,5 ở dạng mù màu khó nhất, và cách màu ngành gần nhất 20,0. Khóa theo cỡ cụm vì số hiệu Louvain là nhãn tùy ý, chạy lại có thể hoán vị |
| B15 | **Ma trận kề chỉ ghi nhãn 13 nước, không ghi 73** | đo được: cạnh vùng vẽ **250,3pt** trên khung 453,6pt (= 6,30 inch), chia cho 73 nước còn **3,4pt mỗi nhãn** — dưới sàn **7pt** của style guide §7, và không có cách bố trí nào cứu được vì 73 × 7pt = 511pt đã dài hơn cả cạnh khung. Tập 13 nhãn = **10 nước ASEAN** (lát cắt của đề tài, B2) **+ nước mạnh nhất mỗi cụm** (chỗ duy nhất đặt tên được cho một khối) → **19,3pt mỗi nhãn**, đạt sàn. Xem chi tiết bên dưới |
| B16 | **Khung hình của T16 tính bằng POINT, không bằng pixel** | `FIG_WIDTH_FULL * 72 = 453,6` thay cho `FIG_WIDTH_FULL * FIG_DPI_SCREEN = 1260`. Lý do: không quy đổi được thì không kiểm được sàn 7pt, mà sàn 7pt là một dòng trong checklist §7. Hệ quả đã đo, và là một lỗi có thật của các hình trước: xem bên dưới |
| B17 | **Khối trong chord mã hoá bằng VỊ TRÍ, không bằng màu** | đã đo chứ không phỏng đoán: sau 10 màu ngành (T04) và 3 màu cụm (T15), tìm tham lam maximin trên lưới 868 màu in được thì hai màu đầu của một bảng mới còn cách ΔE 27,2 và 18,7 — nhưng chúng là `#00FF00` và `#FF00FF`, tức thuật toán đã phải bới vào góc gamut — và **màu thứ ba chỉ còn 14,2, dưới sàn 15**. Hết chỗ cho bảng màu thứ ba. Trên một vòng tròn thì khối đã có vị trí cố định và nhãn riêng nên hue không cần thiết: cung và dải dùng độ sáng, Việt Nam nổi lên bằng viền đen theo B12. Chạy lại: `src/probe_colour_space.py` |

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

### B15 chi tiết — vì sao 73 nhãn là không thể, và 13 nhãn nào

Lấy lại số: `python src/make_adjacency_matrix.py --year 2023`, khối **NHÃN**.

```
cạnh vùng vẽ 250,3 pt (khung 453,6 pt = 6,30 inch)
   73 nhãn ->  3,43 pt mỗi nhãn   DƯỚI sàn 7 pt
   13 nhãn -> 19,25 pt mỗi nhãn   ĐẠT  sàn 7 pt
```

Đây **không** phải vấn đề bố trí khéo hay vụng. 73 dòng chữ, mỗi dòng tối thiểu
7pt, là 511pt — dài hơn cả cạnh khung 453,6pt, chưa trừ tiêu đề và thanh màu.
Không có cách xoay, so le hay thu nhỏ nào cứu được; chỉ còn hai lối ra: **bỏ
bớt nhãn** hoặc **phóng to hình**, mà phóng to thì vi phạm khổ 6,30 inch của
style guide §5 vốn là bề rộng vùng chữ của khổ A4.

Chọn tập 13 theo hai tiêu chí, mỗi tiêu chí trả lời một câu người đọc sẽ hỏi:

| Ai được ghi tên | Vì sao |
|---|---|
| **10 nước ASEAN** (gồm Việt Nam, in đậm) | đề tài có lát cắt VN–ASEAN, B2. Không ghi thì không ai tìm được Việt Nam trên một tấm lưới 73×73 |
| **Nước mạnh nhất mỗi cụm** (2023: Trung Quốc, Đức, Hoa Kỳ) | là chỗ duy nhất gọi tên được một khối. Không có nó thì ba khối chỉ là ba ô vuông vô danh |

Ba thứ đi kèm để việc bỏ nhãn không thành mất thông tin:

1. **Nét dẫn.** Ở bản xếp theo cụm, 7 nước ASEAN nằm cách nhau 2–3 hàng (8–12pt)
   nên nhãn vẫn đè nhau dù chỉ còn 13 cái. Nhãn được đẩy ra vừa đủ và nối về
   đúng hàng bằng một nét 0,4pt — **hàng không xê dịch, chỉ cái nhãn xê dịch**.
2. **Nhãn theo KHỐI ở lề phải** — tên nước mạnh nhất + cỡ khối, thay cho việc
   đọc tên từng thành viên.
3. **Chỉ ghi nhãn ở hàng, không ghi ở cột.** Hai trục dùng chung một thứ tự nên
   nhãn cột chỉ lặp lại nhãn hàng; bỏ đi thì ma trận to thêm **40pt** mỗi cạnh.
   Bù lại có một đường chéo mảnh để dò từ một cột về hàng cùng tên, và các vạch
   chia nhỏ trên trục trên đặt đúng 13 vị trí ấy.
4. **Bản `.html` vẫn đủ 73 × 73**: rê chuột vào bất kỳ ô nào ra tên hai nước,
   giá trị và số hiệu khối. Không ô nào bị bỏ đi, chỉ nhãn bị bỏ.

### B16 chi tiết — point hay pixel, và một lỗi đơn vị của các hình trước

Các script trước đặt khung plotly rộng `FIG_WIDTH_FULL * FIG_DPI_SCREEN = 1260`
rồi truyền thẳng `FONT_SIZES` (13 / 10 / 9 / 8 / 7) vào làm cỡ chữ. Hai con số
ấy **không cùng đơn vị**: 1.260 là pixel ảnh, còn 13 trong style guide là
point in trên khổ 6,30 inch.

Hệ quả đo được: khi dán ảnh vào cột chữ rộng 6,30 inch, một đơn vị khung bằng
`453,6 / 1.260 = 0,36pt`. Nên trên bản in, tiêu đề 17 đơn vị của
`output/node_link_2023.png` chỉ còn **≈ 6,1pt**, và dòng nguồn 7 đơn vị còn
**≈ 2,5pt**. Dòng cuối checklist §7 — *"chữ nhỏ nhất ≥ 7pt sau khi xuất"* —
hiện **không** đạt ở T09, T12–T15, mà không ai thấy vì trên màn hình ảnh được
xem to hơn khổ in khoảng 2,8 lần.

T16 đặt khung `453,6 × 453,6` (= 6,30 inch × 72) và xuất PNG bằng
`scale = 6,30 × 300 / 454 = 4,163` → ảnh 1.890 × 1.890 px, đúng 300 dpi của
`FIG_DPI_PRINT`. Khi đó **một đơn vị khung = một point in thật**, cỡ chữ trong
`FONT_SIZES` là point thật, và câu "3,4pt mỗi nhãn" ở B15 là một phép trừ kiểm
lại được chứ không phải một ước lượng.

**Chưa sửa các hình cũ** — đó là việc của T22 (áp hệ thống thị giác lên toàn bộ
biểu đồ), không phải của T16, và sửa thì phải vẽ lại cả năm hình cùng lúc để
chúng còn cùng một cỡ chữ. Ghi ở đây để T22 không phải phát hiện lại.

---

### B17 chi tiết — không gian màu đã hết chỗ, và đo được là hết

`src/probe_colour_space.py` chọn tham lam maximin trên lưới 868 màu nằm trong
khoảng độ sáng in được: mỗi bước lấy màu cách xa nhất **mọi màu đã bị chiếm** (10
màu ngành + 3 màu cụm) và mọi màu đã chọn trước đó. Nếu cách tốt nhất vẫn dưới
ngưỡng thì không phải do chọn kém — là hết chỗ thật.

| Màu thứ | Màu tìm được | Cách màu đã chiếm (ΔE2000) | Ngưỡng |
|---|---|---|---|
| 1 | `#00FF00` | 27,2 | 15 |
| 2 | `#FF00FF` | 18,7 | 15 |
| 3 | `#0000FF` | **14,2** | 15 — **hỏng** |
| 4 | `#FF0000` | **14,0** | 15 — **hỏng** |

Hai điều đọc ra từ bảng này. Thứ nhất, hai màu đầu *đạt ngưỡng* nhưng là lục và
hồng cánh sen bão hoà hết cỡ — thuật toán đã phải chạy ra sát mép gamut, nghĩa là
chỗ trống chỉ còn ở những nơi không ai muốn in. Thứ hai, chỉ cần tới màu thứ ba
là tụt dưới sàn. Một bảng màu 8 khối thì không có cửa.

Hệ quả cho cả đồ án, không riêng T17: **từ đây, thứ gì cần phân biệt mà không
phải ngành hàng hay cụm Louvain thì phải dùng kênh khác hue** — vị trí, hình
dạng, độ sáng, hoặc nhãn. Quy tắc §3.1 của style guide ("màu = ngành hàng, chỉ
thế thôi") đến đây không còn là một lựa chọn thẩm mỹ nữa mà là một ràng buộc đo
được.

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
   trong đó"*. Ai muốn nhìn phần đuôi phải xem ma trận kề (T16,
   `output/adjacency_cluster_2023.png`) — ma trận vẽ đủ **cả 416 luồng có
   hướng**, không gộp hai chiều như node-link, và không có cạnh nào chồng lên
   cạnh nào. Nhưng nó cũng chỉ vẽ **đúng 416 luồng ấy**: cả hai hình đứng trên
   cùng một đồ thị đã lọc, nên ma trận **không** cứu được cái 98,5% đã bỏ.
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

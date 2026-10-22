# 3. Phát hiện

> **Việc T26.** Số hiệu mục `3` là tạm — T27 ráp báo cáo mới chốt thứ tự. Sổ phát
> hiện `docs/phat-hien-va-quyet-dinh.md` giữ bảng đầy đủ theo số **A**; mục này chỉ
> lấy phần đi vào lập luận, và mỗi con số đều kèm lệnh đo lại.
>
> **Phần này có một phát hiện mới, và nó sửa một câu nằm giữa lập luận của cả đồ
> án.** Khi kiểm lại câu *"tiền vào nhiều hơn qua ít kênh hơn"*, phép đo đỡ cho nó —
> đếm số bạn hàng — hoá ra **không bền**: 47 nước rời khỏi danh sách bạn hàng giữa
> 2002 và 2023 chỉ mang theo **0,59%** kim ngạch, và ở bất kỳ mức sàn giá trị nào
> thì số bạn hàng lại **tăng**. Phép đo bền là **mức tập trung của giá trị**, và nó
> nói mạnh hơn hẳn: HHI đáy **0,0662 năm 2013**, lên **0,1226 năm 2023** — vượt cả
> mức 1995. Đó là **A16**, viết ở §3.6, và nó thay phép đo chính của nhịp 3.
>
> **File phân công dự tính 3–4 trang, bản này dài hơn** (≈5.000 từ) vì cùng lý do
> như §2: đây là **bản gốc đầy đủ** để T23 rà soát và T29 lấy câu trả lời phản
> biện. Kế hoạch cắt khi T27 ráp, theo đúng thứ tự này:
>
> - **Giữ nguyên trong thân báo cáo:** §3.1 · §3.6 (phát hiện mới) · §3.7 (căng
>   thẳng trung tâm) · §3.8 (bản lề sang Đề xuất).
> - **Rút gọn trong thân:** §3.2 và §3.3 — giữ bảng số và câu kết luận, bỏ phần
>   giải thích vì sao phép đo hoạt động như vậy; §3.4 giữ bảng, bỏ ba câu diễn
>   giải; §3.5 giữ bảng hành lang, bỏ đoạn cái bẫy hai đồ thị (đã có ở §2.7).
> - **Gộp hoặc bỏ:** §3.9 trùng §2.11 — khi ráp thì giữ **một** chỗ, nên bỏ §3.9
>   và trỏ sang §2.11.

---

## 3.1 Năm câu, theo thứ tự lập luận

| Nhịp | Phát hiện | Con số đỡ cho nó | Hình |
|---|---|---|---|
| 1 | Rổ hàng đã được xây lại gần như từ đầu | điện tử 0,60% → **29,94%**; tổng xuất khẩu gấp **75,4 lần** | T21 |
| 2 | Và năng lực đi lên thật, đo được | ECI #181/211 → **#78/230**; COI 0,225 → **1,197** | A1 |
| 3 | Nhưng tiền dồn lại vào ít cửa | HHI 0,0662 (2013) → **0,1226** (2023); top-3 nhận **52,41%** | T19, T20 |
| 4 | Và chỗ bán đậm nhất là chỗ hàng dễ nhất | giày dép RCA **7,52** / PCI −0,49; máy móc RCA **0,95** / PCI +0,78 | T31 |
| 5 | → Đề xuất (mục riêng) | — | T31 |

Bốn nhịp đầu là phần **Phát hiện** này; nhịp 5 là mục Đề xuất, dựng trên §3.7 và §3.8.

Trước bốn nhịp đó, §3.2–§3.3 trả lời câu hỏi nghiên cứu ở tầng mạng lưới: **cấu
trúc thương mại toàn cầu trông như thế nào, và Việt Nam nằm ở đâu trong đó.** Ba
kết quả đầu tiên đều đi ngược trực giác thông thường, nên phải nói trước — nếu
không, người đọc sẽ tưởng các hình bị vẽ sai.

---

## 3.2 Ba kết quả về cấu trúc mạng, cả ba đi ngược trực giác

`data/processed/network_stats.csv` · `degree_distribution.csv` · `threshold_coverage.csv`

| Mạng xuất khẩu toàn cầu | 1995 | 2023 |
|---|---|---|
| Nút / cạnh có hướng | 211 / 18.411 | 231 / 27.535 |
| Mật độ | 0,4155 | **0,5183** |
| Đối ứng (có đi có lại) | 0,8235 | 0,8368 |
| Gini trọng số cạnh | 0,9548 | 0,9569 |
| Trung vị số bạn hàng xuất | 78 | **116** |
| Lệch khỏi phân bố đều ¹ | 0,180 | **0,056** |

¹ khoảng lệch lớn nhất giữa CCDF thật và CCDF của một phân bố đều hoàn toàn trên
dải bậc; càng gần 0 thì các nước càng trải đều. Đo bằng `src/make_degree_loglog.py`.

**Kết quả 1 — mạng này không phải scale-free, và đó là kết quả chứ không phải
lỗi.** Mật độ 0,5183 nghĩa là **hơn một nửa** mọi cặp nước trên thế giới có giao
dịch. Mạng xã hội hay mạng trích dẫn thường dưới 1%. Nên không tồn tại "hub" theo
nghĩa tô-pô: không có nhóm nhỏ nối với tất cả trong khi phần còn lại nối với vài
nước — vì gần như ai cũng nối với nhiều. Biểu đồ log-log của T09 vì thế **không ra
đường thẳng**; nó đi ngang rồi rơi dốc ở mép phải. Để không ai phải tin vào mắt
mình, hình vẽ kèm đường khớp lũy thừa tốt nhất và ba con số của phép khớp: **R²
0,51**, chỗ lệch tệ nhất **41,3 lần**, và đường khớp đòi CCDF **lớn hơn 100%** ở
mọi bậc dưới 31 — một đòi hỏi vô nghĩa, vì CCDF là một tỉ lệ.

**Kết quả 2 — ba mươi năm toàn cầu hoá san phẳng chuyện "ai nối với ai", nhưng
không san phẳng chuyện "luồng nào lớn".** Hai dòng cuối bảng trên đi hai hướng
khác nhau, và đó là phần đáng viết: độ lệch khỏi phân bố đều **giảm từ 0,180 xuống
0,056** (năm 1995 vẫn còn hẳn một lớp nước ít bạn hàng; 2023 thì gần như không
còn), trong khi **Gini trọng số cạnh gần như đứng yên**, 0,9548 → 0,9569. Kết nối
thì dàn đều ra, giá trị thì không.

Đo cụ thể mức tập trung ấy trên 27.535 cạnh năm 2023, tổng 21,66 nghìn tỷ USD:

| Giữ lại | % số cạnh | % giá trị |
|---|---|---|
| 100 cạnh lớn nhất | 0,36% | **43,02%** |
| 416 cạnh lớn nhất | 1,51% | **68,50%** |
| 1.000 cạnh lớn nhất | 3,63% | 83,54% |
| 2.754 cạnh lớn nhất | 10,00% | 95,19% |
| **quy tắc lọc đã chốt (B4)** — cũng 416 cạnh | 1,51% | **67,84%** |

**Vứt 98,5% số cạnh vẫn giữ hơn hai phần ba tổng giá trị thương mại thế giới.**
Hai dòng cuối không trùng nhau, và chỗ lệch đó là một lựa chọn chứ không phải sai
số: quy tắc B4 giữ thêm top-3 luồng vào/ra của từng nước ASEAN, nên nó **đánh đổi
0,66 điểm phần trăm độ phủ giá trị** để cả 10 nước ASEAN đều có mặt ở mọi năm — mà
không có chỗ đánh đổi ấy thì năm 1995 Brunei và Lào biến khỏi hình.

Gộp hai kết quả trên ra câu gọn nhất về cấu trúc:

> **Cấu trúc trung tâm–ngoại vi của thương mại không nằm ở việc ai nối với ai, mà
> nằm ở việc luồng nào lớn.**

**Kết quả 3 — và vì vậy một chỉ số mạng quen dùng gần như vô dụng ở đây.**
Betweenness (mức độ "làm cầu nối") đo trên mạng đầy đủ năm 2023: **172 trong 231
nước bằng đúng 0** (74,5%). Mật độ quá cao nên gần như không đường đi ngắn nhất
nào cần vòng qua nước thứ ba. Chi tiết hơn, chính phép **nghịch đảo trọng số** (vì
networkx hiểu trọng số là *khoảng cách*, còn giá trị thương mại thì ngược lại) đổi
hẳn kết luận trên mạng đã lọc:

| Mạng đã lọc 2023, n = 73 | Số nước có betweenness > 0 | Việt Nam |
|---|---|---|
| Có trọng số (1/giá trị) | 15 | **0,0000** — đồng hạng với 57 nước khác |
| Không trọng số | 37 | 0,0050 — **hạng 15/73** |

Hai con số đều đúng; chúng trả lời hai câu khác nhau. Có trọng số thì mọi đường
ngắn nhất dồn vào ba luồng khổng lồ (Trung Quốc 0,5503 · Đức 0,3036 · Hoa Kỳ
0,2001) và Việt Nam bằng 0; bỏ trọng số thì Việt Nam là một cầu nối nhỏ nhưng có
thật. Nên `metrics.csv` giữ **cả hai cột**, mọi câu dùng betweenness phải nói rõ
đang dùng cột nào, và bảng có thêm cột `n_tied_betweenness` vì **một cái hạng đọc
trơ trọi là bẫy** — "hạng 16/73" trên cột có trọng số là đồng hạng với 57 nước cùng
bằng 0.

Lấy lại: `PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/analyze_network.py`
rồi `src/compute_metrics.py` · `src/make_degree_loglog.py`

---

## 3.3 ASEAN không hiện ra như một cộng đồng — ba phép đo độc lập cùng nói thế

Đây là phát hiện phải nói thẳng, vì đề tài có hẳn một lát cắt "Việt Nam – ASEAN".
**Lát cắt ấy là một câu hỏi, không phải một tiền đề.**

**Phép đo 1 — Louvain không tìm thấy ASEAN.** Trên mạng đã lọc 2023 (73 nút, 416
luồng), phân hoạch ra **3 cụm, modularity 0,337**, và **ổn định tuyệt đối**: 20
hạt giống khác nhau đều cho cùng kết quả, 100% số cặp nước giữ nguyên quan hệ cùng
cụm hay khác cụm. Nên đây không phải may rủi của một lần chạy. Cả **10 nước ASEAN
rơi vào cùng một cụm**, chung với Trung Quốc, Nhật Bản, Hàn Quốc, Ấn Độ, vùng Vịnh
và Úc. Thuật toán tìm thấy một khối Á–Thái Bình Dương lấy Trung Quốc làm tâm, và
ASEAN tan vào trong đó. Hệ quả cho hình: tô màu theo cụm ở T15 **không** làm ASEAN
nổi lên, nên Việt Nam phải được làm nổi bằng viền đậm (quyết định B12).

**Phép đo 2 — tiền nói đúng điều đó.** Trong 385,54 tỷ USD Việt Nam bán ra năm
2023, **9 nước ASEAN còn lại nhận 7,77%** (29,97 tỷ), trong khi **ba thị trường
đầu nhận 52,41%**: Hoa Kỳ 95,16 tỷ (24,68%), Trung Quốc 86,11 tỷ (22,34%), Hàn
Quốc 20,80 tỷ (5,40%). Láng giềng về địa lý, không phải láng giềng về thương mại.

**Phép đo 3 — và quỹ đạo đã đổi, thấy được khi so với 1995.** Chord T17 chia 73
nước thành 8 khối rồi nhìn riêng các dải chạm vào Việt Nam:

| Bạn hàng của Việt Nam | 1995 | 2023 |
|---|---|---|
| Đông Á | 59,1% | **70,9%** |
| ASEAN còn lại | **33,4%** | 8,4% |
| Châu Mỹ | *không luồng nào vượt ngưỡng* | **18,5%** |
| Châu Âu | 7,5% | 2,3% |

Năm 1995, bạn hàng lớn thứ hai của Việt Nam **chính là ASEAN**. Đến 2023 chỗ đó
thuộc về châu Mỹ — một khối mà năm 1995 Việt Nam không có lấy một luồng nào vượt
ngưỡng. Việt Nam hội nhập vào **hành lang Đông Á – châu Mỹ**, không hội nhập vào
ASEAN.

Ma trận kề T16 bắt thêm một chuyện mà một năm đứng một mình không nói ra: **khối
lớn đã đổi tâm.** Năm 1995 khối 34 nước là một khối *xuyên Thái Bình Dương* với
Hoa Kỳ ở tâm, có cả Nhật Bản, Canada và 10 nước ASEAN. Năm 2023 Hoa Kỳ đã **ra
khỏi** khối đó và đứng đầu một khối Bắc Mỹ riêng 7 nước, còn khối cũ nở lên 41
nước với **Trung Quốc** ở tâm. Việt Nam ở nguyên trong khối lớn suốt 28 năm — cái
đổi là người cầm trịch khối ấy. Kèm theo: tỉ lệ giá trị **nằm trong khối** rơi từ
83,8% xuống 69,7% trong khi modularity gần như đứng yên (0,343 → 0,337), tức cấu
trúc khối **lỏng đi** chứ không chặt lại; hai số đo hai thứ khác nhau, đừng gộp.

Và Việt Nam dày lên thấy được trên hình: hàng–cột Việt Nam năm 1995 chỉ có **3 ô
xuất + 3 ô nhập** vượt ngưỡng, năm 2023 là **8 ô xuất + 10 ô nhập**; luồng lớn
nhất đổi từ *bán sang Nhật Bản 1,5 tỷ USD* thành *mua từ Trung Quốc 133,05 tỷ
USD*. Trên mạng đã lọc, cặp dày nhất của Việt Nam là **Trung Quốc, 219,16 tỷ USD
hai chiều** — gấp **2,3 lần** cặp thứ hai (Hoa Kỳ, 95,16 tỷ).

Cảnh báo khi trích §3.3: mọi tỉ lệ ở ba bảng trên tính trên **phần vượt ngưỡng**,
không phải toàn bộ thương mại. So sánh hai năm vẫn cùng một thước vì quy tắc B4
giữ top-3 bạn hàng của nước trọng tâm ở **cả hai năm** (xem §3.2 và §2.7).

Lấy lại: `src/make_node_link.py` · `src/make_adjacency_matrix.py --year 1995`
· `src/make_chord.py --year 1995`

---

## 3.4 Việt Nam đi lên thật, và đo được

`data/processed/country_year.csv`

| Việt Nam | 1995 | 2005 | 2015 | 2023 |
|---|---|---|---|---|
| ECI (hạng / số nước xếp hạng) | −1,00 (#181/211) | −0,12 (#132/224) | +0,24 (#109/230) | **+0,58 (#78/230)** |
| COI — độ "gần" các ngành phức tạp | 0,225 | 0,793 | 1,071 | **1,197** |
| Số mặt hàng xuất được | 186 | 230 | 258 | **285** |
| Xuất khẩu | 5,12 tỷ USD | 32,87 tỷ | 169,41 tỷ | **385,54 tỷ** |

ECI (*Economic Complexity Index*) là chỉ số của Atlas đo **độ khó của rổ hàng một
nước xuất được** — làm được nhiều thứ, và nhiều thứ ít nước khác làm được, thì
điểm cao. Ba câu đáng viết:

1. Việt Nam đi từ nhóm **14% cuối bảng** lên nhóm **34% đầu bảng** trong 28 năm.
2. Khoảng cách với Thái Lan thu từ **1,3850** xuống **0,2760** điểm.
3. Và đây là chỗ dễ bỏ qua: Thái Lan **đạt đỉnh 2015 rồi đi ngang** (+0,93 →
   +0,85) trong khi Việt Nam vẫn đi lên. Hai đường đang thu hẹp — Việt Nam không
   đuổi theo một mục tiêu đang chạy.

⚠️ **Bắt buộc nêu mẫu số** khi trích hạng: số nước được xếp hạng đổi từ 211 (1995)
lên 230 (2023), nên "hạng 78" không đọc được nếu thiếu mẫu số. Cột `eci_n` giữ sẵn
mẫu số cho từng năm.

Và một điều phải nói ngay cạnh bảng này, không để sang phần hạn chế: **ECI tính
trên xuất khẩu gộp.** Một nước lắp ráp điện thoại được cộng trọn điểm phức tạp của
chiếc điện thoại, bất kể giữ lại bao nhiêu giá trị. Đường ECI dốc đứng ở trên
**một phần** đến từ 115,43 tỷ USD điện tử — mà §3.7 sẽ cho thấy lợi thế so sánh
trong điện tử chỉ ở mức 2,23, tức gần đúng bằng tỷ lệ điện tử trong thương mại thế
giới.

---

## 3.5 Hành lang đo được: mua của Trung Quốc, bán cho Hoa Kỳ

`data/processed/edges.csv` · đồ thị **đầy đủ**, không lọc ngưỡng

| 2023 | Việt Nam mua | Việt Nam bán | Chênh |
|---|---|---|---|
| Trung Quốc | **133,05 tỷ USD** | 86,11 tỷ USD | **−46,94 tỷ** |
| Hoa Kỳ | 9,83 tỷ USD | **95,16 tỷ USD** | **+85,33 tỷ** |

Hai đầu **ngược dấu**, và đó chính là dấu hiệu mà giả thuyết trung chuyển cần —
thứ mà T15 và T17 không nói được vì cả hai đã gộp hai chiều theo quyết định B13.
Trung Quốc cấp **40,1%** hàng vào; Hoa Kỳ nhận **24,7%** hàng ra. Theo vùng:
**68,3% hàng vào từ Đông Á**, còn hàng ra chia cho Đông Á 37,2% và Bắc Mỹ 26,7%.

Năm đối chứng 1995 ra một hành lang **khác hẳn**: Singapore cấp nhiều nhất (thâm
hụt 1,39 tỷ USD), Nhật Bản mua nhiều nhất (thặng dư 0,60 tỷ). Hành lang không
mới — **hai đầu của nó đã đổi người**, và quy mô gấp 75 lần.

⚠️ Phần "xuất trừ nhập" trên hình Sankey là **số học**, KHÔNG phải giá trị tăng
thêm trong nước. Tách được phần ở lại Việt Nam thì cần bảng vào–ra mà Atlas không
có. Đừng để ai đọc hình này thành "Việt Nam chỉ lắp ráp" — cũng đừng để ai đọc nó
thành ngược lại.

**Và một cái bẫy đã đo được, nằm đúng ở hình này.** Nếu dựng Sankey trên đồ thị
*đã lọc* thì ngưỡng cắt phía bán ra nặng hơn phía mua vào (Việt Nam mua tập trung,
bán rải ra 166 nước), nên cán cân **lật dấu**: hình sẽ in ra *"nhập siêu 15,17 tỷ
USD"* trong khi sự thật là **xuất siêu 53,45 tỷ USD**. Vì vậy báo cáo theo một quy
tắc cố định: hình nói về **cấu trúc toàn cầu** dùng đồ thị đã lọc (T15–T17), hình
nói về **một nước** dùng đồ thị đầy đủ (T19, T20), và **không so trực tiếp con số
của hai nhóm hình**. Đo đầy đủ ở §2.7 phần Phương pháp luận (phát hiện A15).

Lấy lại: `src/make_sankey.py` · Hình: `output/sankey_vietnam_{1995,2023}.png`

---

## 3.6 Kênh bán: phép đo nào bền, phép đo nào không — và vì sao phải đổi phép đo

Đây là phát hiện **A16**, và nó sửa chính câu đang đứng giữa lập luận của đồ án.

**Câu cũ.** "Xuất khẩu gấp 2,28 lần từ 2015 đến 2023 nhưng số bạn hàng giảm từ 181
xuống 166, trong khi trung vị cả thế giới là tăng 1" — tiền vào nhiều hơn qua ít
kênh hơn. Số liệu đúng, và kiểm lại đúng: 130 trong 230 nước tăng số bạn hàng, 85
giảm, trung vị **+1**, Việt Nam **−15**.

**Nhưng phép đo ấy không bền.** Đếm "bạn hàng" là đếm mọi nước có luồng xuất khẩu
**lớn hơn 0**, nên nó đếm cả những luồng cỡ một triệu USD. Ba phép thử:

| Việt Nam bán cho bao nhiêu nước, theo mức sàn giá trị | 1995 | 2002 | 2015 | 2023 |
|---|---|---|---|---|
| trên 0 (phép đo cũ) | 98 | **208** | 181 | 166 |
| trên 10 triệu USD | 32 | 53 | **138** | 128 |
| trên 100 triệu USD | 13 | 23 | 68 | **83** |
| trên 1 tỷ USD | 1 | 4 | 29 | **35** |

1. **Đỉnh thật là 2002 với 208 nước, không phải 2005 với 200** — sổ phát hiện A13
   ghi 2005 vì chỉ nhìn bốn năm mốc 1995/2005/2015/2023. Chuỗi đầy đủ còn cho thấy
   nó không giảm đều: 208 (2002) → 188 (2004) → 200 (2005) → 187 (2007) → …
2. **47 nước rời khỏi danh sách từ 2002 đến 2023 mang theo đúng 0,096 tỷ USD =
   0,59%** kim ngạch 2002. Nước lớn nhất trong số đó là Cuba với 48 triệu USD.
   Trung vị một luồng xuất khẩu đổi từ **1,0 triệu USD** (2002) lên **103,6 triệu
   USD** (2023) — danh sách ngắn đi vì các luồng tí hon biến mất, không vì các
   kênh thật đóng lại.
3. **Ở mọi mức sàn đáng kể, số kênh lại TĂNG.** Trên 100 triệu USD: 13 → 83, tăng
   đều qua từng mốc kể cả 2015 → 2023. Hạng của Việt Nam trong thế giới theo số
   bạn hàng trên 10 triệu USD đi từ **65/211** (1995) lên **24/231** (2023).

Thêm một dấu hiệu nên làm người viết dừng lại: nếu xếp 223 nước theo mức giảm số
bạn hàng 2002 → 2023 thì Việt Nam **giảm mạnh nhất, −42**, trên cả Nga (−38),
Triều Tiên (−37), Iran và Syria (−27). Nhưng xuất khẩu của Việt Nam trong cùng kỳ
gấp **23,6 lần**, còn những nước kia thì bị cấm vận hoặc chiến tranh. Khi một phép
đo đặt một nước vào đúng cái nhóm ấy vì những lý do ngược hẳn nhau, vấn đề nằm ở
phép đo.

**Phép đo bền là mức tập trung của giá trị** — HHI (tổng bình phương tỷ trọng từng
bạn hàng; càng cao càng dồn vào ít nước) và tỷ trọng ba bạn hàng đầu. Hai phép này
không phụ thuộc mức sàn, vì luồng tí hon đóng góp tí hon:

| Việt Nam | 1995 | 2002 | **2013** | 2015 | **2021** | 2023 |
|---|---|---|---|---|---|---|
| HHI | 0,1209 | 0,0687 | **0,0662 ← đáy** | 0,0814 | **0,1330 ← đỉnh** | **0,1226** |
| Top-3 nhận | 47,21% | 36,31% | 39,25% | 42,99% | 54,75% | **52,41%** |
| Số bạn hàng nhận trên 1% | 16 | 21 | 24 | 23 | 20 | 22 |

Hình dạng thật là **một chữ V**, không phải một đường giảm: Việt Nam **đa dạng hoá
suốt 18 năm** (HHI 0,1209 → đáy 0,0662 năm 2013), rồi **dồn lại suốt 10 năm liền**
(0,0662 → 0,1330 năm 2021), và năm 2023 ở mức **0,1226 — cao hơn cả năm 1995**.
Thành quả đa dạng hoá của gần hai thập kỷ đã bị trả lại trong mười năm.

Và so với thế giới, chỗ đứng cũng đã đổi. Trong 97 nước xuất khẩu trên 10 tỷ USD
năm 2023, trung vị HHI là 0,0921 và Việt Nam ở **0,1226 — hạng 30/97** tính từ
phía tập trung nhất. Năm 2015, trên cùng phép đo, Việt Nam **ở dưới trung vị**:
0,0814 so với 0,0856, hạng 47/84. Trong ASEAN năm 2023, Việt Nam là nước **tập
trung nhất**: Thái Lan 0,066 · Singapore 0,067 · Malaysia 0,089 · Indonesia 0,089
· Philippines 0,090 · **Việt Nam 0,123**, tức gần **gấp đôi** Thái Lan.

**Câu mới, dùng cho nhịp 3:**

> Việt Nam **không** bán qua ít cửa hơn — số cửa đáng kể còn tăng. Việt Nam **dồn
> tiền vào ít cửa hơn**: ba thị trường đầu nhận 52,41% hàng xuất năm 2023 so với
> 39,25% năm 2013, và mức tập trung đã quay về trên mức của năm 1995.

Câu mới mạnh hơn câu cũ ở ba điểm: nó sống sót qua phản biện *"anh chỉ đang đếm
mấy luồng tí hon"*; nó có một **năm bước ngoặt** (2013) chứ không chỉ hai đầu; và
nó so được với thế giới cùng ASEAN trên cùng phép đo. Đặt cạnh §3.5 thì hai phát
hiện khớp nhau: tiền dồn vào ba cửa, mà một trong ba cửa ấy (Trung Quốc) đồng thời
là nơi hàng **vào** nhiều nhất.

**Và phía mua vào còn tập trung hơn hẳn.** Chạy cùng phép đo trên chiều nhập khẩu:
HHI **0,0973** (1995) → đáy **0,0791** (2003) → **0,1979** (2023), top-3 nhà cung
cấp chiếm **61,3%** so với 44,4% năm 1995, và số nhà cung cấp chiếm trên 1% **giảm
từ 16 xuống 14**. Tức mức tập trung đầu vào (0,1979) **gấp 1,6 lần** mức tập trung
đầu ra (0,1226). Hành lang ở §3.5 hẹp ở cả hai đầu, nhưng **hẹp hơn ở đầu mua**.
Lệnh: `src/make_time_multiples.py --direction nhap`.

Lấy lại: `src/make_time_multiples.py` (khối KIỂM CHỨNG in cả HHI và tỷ trọng
top-3) · dữ liệu gốc `data/processed/edges.csv`

---

## 3.7 Trèo lên bằng gì: lợi thế mạnh nhất nằm đúng ở nơi hàng dễ nhất

`data/processed/country_product.csv` · Việt Nam, 2023, cấp HS2

| Nhóm hàng | Xuất khẩu | % rổ hàng | **RCA** | **PCI** |
|---|---|---|---|---|
| Điện, điện tử và linh kiện | 115,43 tỷ | 29,94% | 2,2299 | **+0,925** |
| Máy móc công nghiệp | 39,85 tỷ | 10,34% | **0,9537** | **+0,783** |
| Thiết bị quang học, đo lường, y tế | 11,32 tỷ | 2,94% | **0,9052** | **+0,934** |
| Giày dép | 19,64 tỷ | 5,09% | **7,5182** | −0,493 |
| Hàng may mặc (dệt kim) | 14,74 tỷ | 3,82% | 3,6736 | −0,663 |
| Hàng may mặc (không dệt kim) | 14,16 tỷ | 3,67% | 3,2852 | −0,870 |
| Đồ nội thất | 11,77 tỷ | 3,05% | 2,3598 | +0,250 |
| Trái cây, hạt | 6,98 tỷ | 1,81% | 2,8782 | −1,332 |
| Thủy sản | 6,25 tỷ | 1,62% | 2,7539 | −1,589 |

**RCA** (*lợi thế so sánh hiện hữu*) trả lời: nhóm hàng này chiếm tỷ trọng trong rổ
hàng của Việt Nam **gấp bao nhiêu lần** tỷ trọng của nó trong thương mại thế giới —
trên 1 là bán đậm hơn mức bình quân. **PCI** là độ khó của nhóm hàng, cũng của
Atlas. Đọc chéo hai cột cuối ra **phát hiện trung tâm của cả đồ án**:

> **Lợi thế so sánh của Việt Nam mạnh nhất đúng ở nơi sản phẩm đơn giản nhất, và
> yếu nhất đúng ở nơi sản phẩm phức tạp nhất.**

Giày dép PCI −0,49 mà RCA **7,52**; trái cây −1,33 mà 2,88; thủy sản −1,59 mà
2,75. Ngược lại, hai nhóm **phức tạp nhất** bảng — thiết bị quang học (PCI +0,934)
và máy móc công nghiệp (+0,783) — đều có **RCA dưới 1**, tức Việt Nam hiện diện ở
đó *ít hơn* mức bình quân thế giới: **không có lợi thế so sánh nào cả.**

Điện tử là ngoại lệ đáng nói: PCI +0,925, và là nhóm lớn nhất với 115,43 tỷ USD
(29,94% rổ hàng) — nhưng RCA chỉ **2,23**, tức Việt Nam lớn trong điện tử gần đúng
theo tỷ lệ điện tử lớn trong thương mại thế giới, chứ không vượt trội như cách nước
này vượt trội ở giày dép (7,52).

Chia rổ hàng theo bốn góc của mặt phẳng RCA × PCI thì thấy nó **đang** dịch, nhưng
chưa đủ:

| Góc | Nghĩa | 2015 | 2023 |
|---|---|---|---|
| Đã thắng | RCA ≥ 1, PCI > 0 | 32,3% | **38,2%** |
| Cơ hội | RCA < 1, PCI > 0 | 16,5% | **21,6%** |
| **Đang kẹt** | RCA ≥ 1, PCI ≤ 0 | 44,7% | **36,2%** |
| Ngoài cuộc | RCA < 1, PCI ≤ 0 | 6,5% | 4,0% |

Góc "đang kẹt" — bán rất đậm nhưng hàng dễ — co từ 44,7% xuống 36,2% trong tám
năm. Rổ hàng **đang rời** khỏi góc đó, nhưng **hơn một phần ba vẫn nằm lại**, và
các nhóm nằm lại là những nhóm đã giảm tỷ trọng suốt 28 năm.

⚠️ Một chỗ phải nói rõ trước khi ai đó đọc hình T31: ô **`Chưa phân loại` chiếm
11,83% rổ hàng** — 45,60 tỷ USD, RCA **2,4408** (cao hơn cả điện tử), PCI −1,206.
Đó là nhóm HS2 `99` với nút con duy nhất `XXXX` (*Trade data discrepancies*) của
Atlas, **không phải một ngành để đầu tư**. Quy tắc chọn trong
`make_decision_plane.py` loại thẳng nó (`sector != UNCLASSIFIED`); nếu không, ô bán
đậm thứ hai trên mặt phẳng quyết định lại là một ô dữ liệu không phân loại được.
Xem §2.8.

Lấy lại: `src/make_decision_plane.py` · `src/make_hierarchy_charts.py`

---

## 3.8 Những phát hiện này ràng buộc phần Đề xuất như thế nào

Phần Đề xuất là mục riêng, nhưng nó không được tự do: bốn nhịp trên đã khoá sẵn
bốn điều kiện mà bất kỳ đề xuất nào cũng phải thoả.

1. **Không đề xuất "đa dạng hoá thị trường" bằng cách đếm thêm bạn hàng** (§3.6).
   Thêm một nước nhận 5 triệu USD không đổi được HHI. Phép đo phải là tỷ trọng giá
   trị, nên mục tiêu cũng phải phát biểu theo tỷ trọng giá trị.
2. **Không đề xuất dồn thêm vào điện tử** (§3.7). RCA đã 2,23, chiếm 29,94% rổ
   hàng, và là khâu phụ thuộc nhập khẩu nhất trong hành lang ở §3.5.
3. **Không đề xuất dồn thêm vào nhóm RCA cao – PCI thấp** (§3.7). Thủy sản, cà
   phê, trái cây đã bán rất đậm và đã giảm tỷ trọng suốt 28 năm.
4. **Đề xuất phải nói được điều gì sẽ làm nó sai.** §3.6 đưa ra sẵn một mốc kiểm
   chứng: nếu HHI tiếp tục đi xuống từ 0,1226 mà không cần can thiệp gì, thì vấn
   đề tự giải và đề xuất mất phần cấp thiết.

Chỗ còn lại sau bốn điều kiện đó là góc **"cơ hội"** — RCA dưới 1 nhưng PCI dương,
21,6% rổ hàng — và trong góc ấy, hai nhóm đang sát ngưỡng lợi thế: **thiết bị quang
học, y tế** (RCA 0,75 → 0,9052; PCI +0,934) và **máy móc công nghiệp** (0,46 →
0,9537; +0,783). Đó là đầu vào của mục Đề xuất, kèm phép thử lại quy tắc trên dữ
liệu 2015 (xem §2.10 và A14).

---

## 3.9 Những gì phần này KHÔNG trả lời được

Nói trước thì được điểm trung thực; để bị hỏi mới nói thì mất nhiều hơn.

1. **Vì sao các luồng nhỏ biến mất.** §3.6 đo được rằng chúng biến mất và đo được
   rằng chúng không đáng kể về tiền. Nhưng dữ liệu này không cho biết thương mại
   thật sự dừng, hay đã dồn qua trung gian rồi được tính sang nước khác.
2. **Bao nhiêu giá trị ở lại Việt Nam.** Mọi nhận định về "giữ lại bao nhiêu giá
   trị" trong báo cáo là **suy luận từ RCA × PCI**, không phải đo trực tiếp. Muốn
   đo thì cần bảng vào–ra (OECD TiVA hoặc ADB MRIO) — ngoài tầm đồ án này.
3. **Chi tiết dưới cấp HS2.** 97 nhóm hàng là mức chi tiết nhất đang có; "Điện,
   điện tử và linh kiện" gộp cả chip lẫn dây điện. Chi tiết hơn cần file HS4 452 MB
   (~4,2 giờ tải).
4. **Phần đuôi của mạng.** Node-link và chord đứng trên đồ thị đã lọc, tức đã vứt
   98,5% số cạnh. Chúng đọc được là *"bản đồ các luồng lớn, cộng chỗ đứng của ASEAN
   trong đó"*, không phải "bản đồ thương mại toàn cầu".
5. **Năm 2024.** Dữ liệu dừng ở 2023 vì bản Atlas 2024 còn tạm — riêng Việt Nam
   mất 37 bạn hàng trị giá 11,4 tỷ USD, đủ để biểu đồ đọc thành "Việt Nam đang mất
   bạn hàng". Chi tiết ở §2.3.

---

**Đối chiếu sang sổ phát hiện:** §3.2 ← A3, A4, A7 · §3.3 ← A8, A10, A11 · §3.4 ←
A1 · §3.5 ← A12, A15 · §3.6 ← A9, A13, **A16** · §3.7 ← A2, A14 · §3.9 ← D1–D5.

# 4. Cấu trúc: mạng này không có hub, và ASEAN không phải một cộng đồng

Hồi hai trả lời câu hỏi con **(a)** và một nửa câu **(b)** ở §1.1: cấu trúc thương
mại toàn cầu trông như thế nào, và Việt Nam nằm ở đâu trong đó. Cả hai kết quả
dưới đây **đi ngược trực giác thông thường**, nên phải nói trước — nếu không,
người đọc sẽ tưởng các hình bị vẽ sai.

## 4.1 Ba kết quả về cấu trúc mạng, cả ba đi ngược trực giác

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

## 4.2 ASEAN không hiện ra như một cộng đồng — ba phép đo độc lập cùng nói thế

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

Cảnh báo khi trích §4.2: mọi tỉ lệ ở ba bảng trên tính trên **phần vượt ngưỡng**,
không phải toàn bộ thương mại. So sánh hai năm vẫn cùng một thước vì quy tắc B4
giữ top-3 bạn hàng của nước trọng tâm ở **cả hai năm** (xem §4.1 và §2.5).

Lấy lại: `src/make_node_link.py` · `src/make_adjacency_matrix.py --year 1995`
· `src/make_chord.py --year 1995`

---


# Kết luận để nói khi thuyết trình

Mở file này trước khi lên trình bày. Mỗi mục có: **con số**, **lấy từ đâu**, và
**nói thế nào**. Mọi con số ở đây đều do script trong `src/` in ra — chạy lại
script là kiểm được, không ai phải tin trí nhớ của ai.

Quy ước: chỗ nào ghi "⚠️" là chỗ dễ nói quá lời thành sai. Đọc kỹ phần đó,
vì giáo viên hỏi đúng vào những chỗ ấy.

---

## 0. Một câu trả lời cho cả bài

> **Việt Nam đã leo rất nhanh trong thương mại toàn cầu, nhưng leo bằng cách
> trở thành công xưởng lắp ráp cho một khối do Trung Quốc dẫn đầu — bán nhiều
> tiền hơn qua ít cửa hơn.**

Ba vế đó tương ứng ba phần của nhóm:
- "leo rất nhanh" → phần **Huy** (cơ cấu sản phẩm, cây HS92)
- "công xưởng lắp ráp cho một khối" → phần **Phúc** (mạng lưới, cộng đồng)
- "ít cửa hơn" → phần **Dương Quang Huy** (thời gian, luồng)

---

## 1. Phần Huy (R1) — cây sản phẩm, Việt Nam bán cái gì

### 1.1 Chuyển dịch cơ cấu là có thật và đo được

| Ngành | 1995 | 2023 | Đổi |
|---|---|---|---|
| Điện tử | 0,6% | **29,9%** | +29,3 điểm |
| Máy móc và thiết bị | 1,4% | 14,4% | +13,0 |
| Nông sản, gỗ và giấy | **42,9%** | 11,6% | −31,4 |
| Khoáng sản và nhiên liệu | 20,6% | 1,4% | −19,1 |
| Dệt may, giày dép, nội thất | 28,8% | 18,4% | −10,4 |

Tổng kim ngạch: 5,1 tỷ USD (1995) → 385,5 tỷ USD (2023), **tăng 75,3 lần**.

*Nguồn:* `python src/make_streamgraph.py`, `src/make_hierarchy_charts.py`

**Nói thế nào:** "Năm 1995 Việt Nam là một nước bán nông sản và dầu thô. Năm
2023 gần một phần ba kim ngạch là điện tử. Đây không phải tăng trưởng đều —
đây là thay hẳn mặt hàng."

### 1.2 ECI: thước đo độc lập xác nhận điều đó

ECI từ **−1,00 (hạng 181/211)** năm 1995 lên **+0,58 (hạng 78/230)** năm 2023.

⚠️ Phải đọc kèm mẫu số: số nước được xếp hạng đổi từ 211 lên 230. Nói "hạng 78"
mà không nói "trên 230" là giấu mất một nửa thông tin. Cột `eci_n` trong
`country_year.csv` có sẵn mẫu số cho đúng mục đích này.

### 1.3 Việt Nam khác các nước ASEAN cùng cỡ ở chỗ nào

| | VNM | THA | MYS | IDN |
|---|---|---|---|---|
| Dệt may, giày dép | **18,4%** | 2,9% | 1,9% | 7,9% |
| Bốn ngành chế tạo | **64,6%** | 48,6% | 47,6% | 21,7% |
| Ngành lớn nhất | Điện tử 29,9% | Nông sản 18,3% | Điện tử 33,0% | Khoáng sản 26,1% |

*Nguồn:* `python src/make_small_multiples.py`

⚠️ **Không được nói** "Việt Nam chế tạo nhiều hơn các nước ASEAN cùng cỡ" một
cách chung chung — Malaysia có tỷ trọng điện tử **33,0%**, cao hơn Việt Nam
(29,9%). Câu đúng là: **Việt Nam là nước duy nhất trong nhóm còn dựa mạnh vào
dệt may và giày dép** — 18,4%, gấp 2,3 lần nước thứ hai là Indonesia.

### 1.4 Nghịch lý phức tạp — câu hay nhất của phần này

Lợi thế so sánh (RCA) của Việt Nam **mạnh nhất ở nơi sản phẩm đơn giản nhất**
(giày dép RCA 7,52; cà phê RCA 4,21) và **yếu nhất ở nơi sản phẩm phức tạp
nhất** (máy móc công nghiệp, thiết bị quang học).

**Nói thế nào:** "Việt Nam xuất khẩu điện tử rất nhiều, nhưng lợi thế so sánh
thật sự vẫn nằm ở giày dép và cà phê. Hai chuyện đó cùng đúng, và mâu thuẫn
biểu kiến ấy chính là nội dung của phần tiếp theo."

---

## 2. Phần Phúc (R2) — mạng lưới, Việt Nam đứng ở đâu

### 2.1 Mạng thương mại KHÔNG phải mạng scale-free

| Năm | Mật độ | Bậc trung vị | Bậc lớn nhất | max/trung vị |
|---|---|---|---|---|
| 1995 | 41,5% | 159 | 408 | 2,6 |
| 2023 | 51,8% | 242 | 447 | **1,8** |

*Nguồn:* `python src/make_degree_dist.py`

**Nói thế nào:** "Người ta hay nói mạng thương mại có vài hub lớn. Chúng tôi
kiểm thì không phải. Mật độ 51,8% — một nước trung bình buôn với hơn nửa thế
giới. Nước nhiều bạn hàng nhất chỉ gấp 1,8 lần nước trung vị. Trong một mạng
scale-free thật thì tỷ lệ đó là hàng trăm lần. Và tỷ lệ này đang **giảm** theo
thời gian, tức là mạng ngày càng xa dạng scale-free."

**Vì sao điều này quan trọng:** nó là lý do kỹ thuật để lọc ngưỡng ở T10. Cấu
trúc của mạng này không nằm ở **ai nối với ai** (tô-pô) mà nằm ở **nối chặt đến
đâu** (trọng số): Gini = 0,957, top 1% số cạnh giữ 61,2% giá trị.

### 2.2 Ba khối địa lý, và ASEAN không phải một khối

Louvain trên đồ thị đã lọc (73 nút, 416 cạnh) cho đúng 3 cụm:

| Khối | Số nước | Dẫn đầu |
|---|---|---|
| Châu Á do Trung Quốc dẫn đầu | **41** | CHN, JPN, KOR, HKG, TWN, IND |
| Châu Âu | 25 | DEU, FRA, NLD, ITA, GBR |
| Bắc Mỹ do Hoa Kỳ dẫn đầu | 7 | USA, MEX, CAN |

**Cả 10/10 nước ASEAN đều rơi vào khối 0** — cùng với Trung Quốc, Nhật, Hàn,
Ấn, vùng Vịnh, Úc và cả Brazil, Nga, Nam Phi.

*Nguồn:* `python src/make_node_link.py`

**Nói thế nào:** "Chúng tôi kỳ vọng thấy một khối ASEAN. Không có. Thuật toán
gom cả 10 nước ASEAN vào chung một khối 41 nước do Trung Quốc dẫn đầu. Về mặt
dữ liệu thương mại, ASEAN không tồn tại như một đơn vị — các nước ASEAN gắn với
Trung Quốc chặt hơn là gắn với nhau."

### 2.3 Sắp lại hàng cột là thuật toán trực quan hóa

Mật độ trong khối **12,9%** so với ngoài khối **4,1%** — đặc gấp **3,1 lần**.

*Nguồn:* `python src/make_adjacency.py`

**Nói thế nào:** "Hai ma trận này chứa đúng cùng 416 luồng. Không thêm, không
bớt một bit nào. Bản trái sắp theo tên nước trông như nhiễu. Bản phải sắp theo
cụm thì ba khối hiện ra thành ba hình vuông trên đường chéo. Toàn bộ cấu trúc
nằm ở **thứ tự**, không nằm ở dữ liệu. Với ma trận kề, chọn thứ tự hàng cột
chính là chọn thuật toán trực quan hóa."

### 2.4 Betweenness của Việt Nam = 0 — và vì sao không được đọc sai

Betweenness của Việt Nam trong đồ thị đã lọc là **0,0000**, hạng 16/73 nhưng
**đồng hạng với 57 nước khác**.

⚠️ Đây là chỗ dễ sai nhất của cả bài. **Không được nói** "Việt Nam hạng 16 về
trung gian" — con số hạng đó vô nghĩa khi 57 nước cùng điểm. Chính script
`compute_metrics.py` tự in ra cảnh báo này.

**Nói thế nào:** "Betweenness bằng 0, và 57 nước khác cũng bằng 0. Lý do nằm ở
slide trước: mạng có mật độ 51,8%, ai cũng nối thẳng với ai, nên không ai cần
đi vòng qua ai. Trong một mạng như vậy, 'nút trung gian' theo nghĩa lý thuyết
đồ thị gần như không tồn tại — với bất kỳ nước nào, không riêng Việt Nam."

### 2.5 So sánh node-link với ma trận kề — checklist mục 5 hỏi đúng cái này

| | Node-link | Ma trận kề |
|---|---|---|
| Thấy hình dáng tổng thể | ✅ | ❌ |
| Tra một cặp nước cụ thể | ❌ cạnh chồng nhau | ✅ tức thì |
| Đọc mật độ trong khối | ❌ | ✅ |
| Thấy đường đi, nút trung gian | ✅ | ❌ |
| Chịu được đồ thị dày | ❌ phải lọc còn 416 cạnh | ✅ |

**Nói thế nào:** "Chúng tôi vẽ cả hai trên cùng 416 cạnh để so. Kết luận: node-link
trả lời câu 'mạng này hình gì', ma trận trả lời câu 'hai nước này có buôn với
nhau không'. Không họa đồ nào thay được họa đồ kia."

---

## 3. Phần Dương Quang Huy (R3) — thời gian và luồng

### 3.1 Phát hiện mạnh nhất của cả bài: tiền tăng, cửa giảm

| Năm | Số thị trường xuất khẩu | Tổng xuất khẩu |
|---|---|---|
| 1995 | 98 | 5,1 tỷ USD |
| 2005 | **200** ← đỉnh | 32,9 tỷ USD |
| 2015 | 181 | 169,4 tỷ USD |
| 2023 | **166** | 385,5 tỷ USD |

Từ đỉnh 2005: **mất 34 thị trường**, trong khi **tiền tăng 11,7 lần**.

*Nguồn:* `python src/make_time_multiples.py`

**Nói thế nào:** "Đây là biểu đồ tôi muốn mọi người nhớ. Việt Nam đi **lên** —
tiền tăng 75 lần từ 1995. Nhưng từ 2005 Việt Nam đi **sang trái** — mất 34 thị
trường. Bán được nhiều hơn qua ít cửa hơn. Đó không phải thành tích, đó là rủi
ro: một cửa đóng lại thì mất nhiều hơn hẳn so với 20 năm trước."

### 3.2 Việt Nam là công xưởng lắp ráp — con số cụ thể

- Nhập **332,1 tỷ USD** · Xuất **385,5 tỷ USD**
- Nhập bằng **86,1%** giá trị xuất → **giá trị gia tăng trong nước chỉ 13,9%**
- Nguồn nhập lớn nhất: **Trung Quốc 40,1%**
- Thị trường xuất lớn nhất: **Hoa Kỳ 24,7%**

*Nguồn:* `python src/make_sankey.py`

**Nói thế nào:** "Cứ mỗi đồng hàng Việt Nam bán ra, có 86 xu là hàng đã mua từ
nước khác. 40% hàng nhập đến từ Trung Quốc, 25% hàng xuất đi sang Mỹ. Đây là
hình dạng kinh điển của một nền kinh tế gia công."

⚠️ **Giới hạn phải nói thẳng, đừng chờ bị hỏi:** biểu đồ Sankey này **không**
truy vết được lô hàng. Dữ liệu cho biết Việt Nam nhập bao nhiêu từ Hàn Quốc và
xuất bao nhiêu sang Mỹ, nhưng **không** cho biết hàng Hàn Quốc có đi tiếp sang
Mỹ hay không. Hai bên nút Việt Nam là hai phép đo riêng đặt cạnh nhau, không
phải một dòng chảy liên tục.

### 3.3 Hai câu trả lời cho giả thuyết "nút trung chuyển"

Đây là chỗ hay nhất để phối hợp giữa phần Phúc và phần Dương Quang Huy:

| Cách đo | Kết quả | Kết luận |
|---|---|---|
| Tô-pô mạng (betweenness) | 0,0000, đồng hạng 57 nước | **KHÔNG** phải nút trung chuyển |
| Dòng tiền (nhập/xuất) | 86,1%, giá trị gia tăng 13,9% | **ĐÚNG** là công xưởng lắp ráp |

**Nói thế nào:** "Giả thuyết đúng một nửa, và hai nửa phải tách ra. Theo lý
thuyết đồ thị thì không — Việt Nam không nằm trên đường đi của ai cả. Theo dòng
tiền thì có — Việt Nam mua đầu vào rồi bán đầu ra với 14% giá trị thêm vào.
Trả lời 'có' hay 'không' một cách gọn lỏn đều sai."

### 3.4 Thương mại nội khối ASEAN nhỏ hơn người ta tưởng

Việt Nam xuất đi: Đông Á **37,2%**, Bắc Mỹ **26,7%**, Châu Âu 16,2%,
**Đông Nam Á chỉ 7,8%**.

*Nguồn:* `python src/make_chord.py`

**Nói thế nào:** "63,9% hàng Việt Nam bán ra đi về Đông Á và Bắc Mỹ. Còn ASEAN
— 10 nước láng giềng, cùng khối kinh tế — chỉ nhận 7,8%. Cộng với kết quả
Louvain ở phần trước: ASEAN không phải một khối thương mại, cả về cấu trúc lẫn
về dòng tiền."

---

## 4. Phần phương pháp — và một phát hiện bất ngờ

### 4.1 Chúng tôi KHÔNG đối chiếu được ba nguồn, và đã nói ra

Phân công ban đầu ghi "đối chiếu Atlas với BACI và Comtrade". Chúng tôi không
làm vậy, vì **ba cái tên đó không phải ba nguồn độc lập** — Atlas và BACI đều
dẫn xuất từ UN Comtrade. Đối chiếu chúng chỉ đo được khác biệt thuật toán làm
sạch, không đo được độ tin cậy của số gốc.

Thay vào đó chúng tôi làm phép kiểm **chênh lệch gương**: mỗi luồng A→B được
khai hai lần, bởi hải quan nước xuất và hải quan nước nhập. Kết quả:

> **2.093 / 2.093 luồng lớn (100,0%) có hai con số TRÙNG KHÍT nhau.**

*Nguồn:* `python src/compare_mirror.py`

**Nói thế nào:** "Chúng tôi phát hiện Atlas đã hòa giải số liệu hai chiều trước
khi phát hành — 100% các luồng lớn có hai bản khai giống hệt nhau. Nghĩa là bộ
dữ liệu này **không cho phép chúng tôi tự đo sai số của chính nó**. Chúng tôi
báo cáo điều này thay vì nói 'đã đối chiếu ba nguồn và chúng khớp nhau', vì câu
đó sẽ là một tuyên bố sai."

Đây là câu trả lời mạnh nếu bị hỏi "các em có kiểm tra chất lượng dữ liệu
không" — mạnh hơn hẳn một bảng ba cột số giống nhau.

### 4.2 Vì sao chọn 2023 chứ không phải 2024

Bản Atlas 2024 còn tạm: thiếu **1.781 cặp nước**, riêng Việt Nam mất **37 bạn
hàng**. Dùng 2024 thì phát hiện "mất thị trường" ở mục 3.1 sẽ bị thổi phồng bởi
dữ liệu thiếu chứ không phải bởi hiện thực.

### 4.3 Vì sao ngưỡng lọc là tỷ lệ chứ không phải số tuyệt đối

Ngưỡng cố định 10 tỷ USD năm 1995 giữ được 89 cạnh và chỉ **4/10** nước ASEAN;
năm 2023 giữ 390 cạnh và 8/10. So sánh qua thời gian bằng ngưỡng cố định là so
sánh sai — phần lớn "thay đổi" chỉ là lạm phát và tăng trưởng danh nghĩa.

Ngưỡng đã chốt: **0,046% tổng xuất khẩu thế giới mỗi năm + giữ top-3 luồng
vào/ra cho mỗi nước ASEAN** → 416 cạnh, 67,8% giá trị, đủ 10/10 ASEAN ở **mọi**
năm.

⚠️ Chính cái bẫy này suýt làm hỏng biểu đồ chord: ngưỡng tuyệt đối đã lặng lẽ
xóa mất 4 trong 8 luồng của Việt Nam, vì Việt Nam chỉ chiếm **1,8%** tổng xuất
khẩu thế giới nên luồng "rất lớn với Việt Nam" vẫn "nhỏ với thế giới". Đã sửa:
dải nào có Việt Nam thì không áp ngưỡng.

---

## 5. Về thiết kế — nếu bị hỏi về lựa chọn thị giác

### 5.1 Vì sao Việt Nam được làm nổi bằng viền đen, không bằng màu

Đã thử tìm màu thứ 11. **Không còn chỗ:** mọi màu cam/đỏ đủ khác 10 màu ngành ở
mắt thường (ΔE 22–27) đều tụt xuống ΔE 4–8 khi mô phỏng mù màu. Chỉ màu đen còn
đứng vững (ΔE 19,9). Nên Việt Nam = viền đen 1,5px + nhãn đậm.

### 5.2 Vì sao cộng đồng mã hóa bằng xám và hình dạng, không bằng màu

Đã đo **7 bảng 3 màu ứng viên** (Paul Tol high-contrast, Tol bright, Okabe–Ito
và 4 biến thể). Tất cả đều tốt ở mắt thường (ΔE 26–46) nhưng khi mô phỏng mù
màu thì khoảng cách tới màu ngành gần nhất tụt còn **ΔE 2,6–6,6** — tức trùng
với một màu ngành. Bảng 10 ngành đã chiếm hết gam an toàn.

Giải pháp: 3 nấc xám + 3 hình dạng. Xám không có sắc độ nên **mô phỏng mù màu
không làm nó đổi** — cặp gần nhau nhất vẫn ΔE 20,1 với cả protan, deutan và
tritan. Người mù màu hoàn toàn vẫn đọc được hình này.

### 5.3 Bảng màu 10 ngành đã qua kiểm định bằng số

ΔE2000 của cặp gần nhau nhất: **mắt thường 16,1 · protan 13,3 · deutan 12,3 ·
tritan 11,6**. Ngưỡng đặt ra là 15 và 10.

Bảng Tableau 10 dùng tạm trước đó **không đạt**: với người mù màu lục, Nông sản
`#59A14F` và Phương tiện vận tải `#E15759` hiện ra cùng một màu bùn, ΔE = **0,7**
— và hai ngành này nằm cạnh nhau trong mọi treemap.

*Kiểm lại:* `python src/check_palette.py` (thoát mã 1 nếu hỏng)

⚠️ **Nếu ai đó chạy một công cụ kiểm bảng màu khác và báo HỎNG**, nhiều khả
năng họ dùng thang **OKLab** chứ không phải **CIEDE2000**. Hai thang cho hai
con số khác nhau cho cùng một cặp màu, không quy đổi được cho nhau. Cặp bị báo
nhiều nhất là **Điện tử `#88CCEE` ↔ Khác `#DDDDDD`** — đo bằng CIEDE2000 thì
ΔE = **18,9** ở mắt thường và **14,9 / 18,2 / 23,5** ở protan / deutan /
tritan, tức vượt xa ngưỡng 15 và 10 của đồ án.

Hai cảnh báo khác mà công cụ ngoài hay nêu, và đều đã được xử lý có chủ ý:
"dải độ sáng quá rộng" và "độ bão hòa thấp" — đó là đặc tính của thang Paul Tol
muted, và style guide đã bù bằng quy định **viền trắng 1px bắt buộc** cho bốn
màu nhạt cùng với nhãn chữ trực tiếp trên mảng.

---

## 6. Năm giới hạn phải tự nói ra

Nói trước thì là trung thực. Để bị hỏi mới nói thì là bị bắt lỗi.

1. **Không có nguồn độc lập để kiểm chéo** — Atlas đã hòa giải số liệu (mục 4.1).
2. **Sankey không truy vết được lô hàng** — không chứng minh được trung chuyển
   (mục 3.2).
3. **Betweenness đồng hạng hàng loạt** — thứ hạng không đọc được (mục 2.4).
4. **Cây sản phẩm chỉ dùng tới tầng 2** (10 ngành, 97 nhóm). Tầng 4 và 6 cần
   file 452 MB không nằm trong phạm vi đã chốt ở T01. Cây đủ 4 tầng có được
   kiểm toàn vẹn (`check_tree.py`) nhưng chỉ 2 tầng được vẽ.
5. **Cộng đồng Louvain là thuật toán có yếu tố ngẫu nhiên** — nên phải nói rõ
   đây là kết quả của một phép tính, không phải một sự thật khách quan. Nhưng
   ở đây nó ổn định tuyệt đối, và đó là điểm mạnh nên nói ra:

   > Chạy lại với **20 hạt giống** khác nhau: **100,0% số cặp nước giữ nguyên
   > quan hệ** cùng cụm / khác cụm. Số cụm luôn là 3. Modularity không đổi,
   > 0,337 ở mọi lần chạy.

   *Kiểm lại:* `python src/compute_metrics.py` (in ở mục "Độ ổn định cộng đồng")

   **Nói thế nào nếu bị hỏi "sao biết ba khối đó không phải ngẫu nhiên":**
   "Chúng tôi chạy 20 hạt giống. Không có một cặp nước nào đổi quan hệ. Ba khối
   này không phải do may mắn của một lần chạy."

---

## 7. Số liệu nền — nếu cần trích nhanh

| Chỉ số | Giá trị |
|---|---|
| Số quốc gia | 231 |
| Số luồng xuất khẩu 2023 | 27.535 |
| Tổng thương mại 2023 | 21,66 nghìn tỷ USD |
| Mật độ mạng 2023 | 51,8% |
| Đối ứng (reciprocity) | 0,837 |
| Gini theo trọng số cạnh | 0,957 |
| Top 1% cạnh giữ | 61,2% giá trị |
| Xuất khẩu Việt Nam 2023 | 385,5 tỷ USD — **hạng 16/231** |
| Số bạn hàng Việt Nam | 166 — **hạng 67/231** |
| Cây HS92 | 6.390 nút · 10 / 97 / 1.243 / 5.040 |

**Cặp số đáng nói nhất trong bảng này:** hạng **16** về tiền, hạng **67** về số
bạn hàng. Việt Nam bán rất nhiều qua rất ít kênh — đúng phát hiện ở mục 3.1,
nhưng nhìn từ một góc khác.

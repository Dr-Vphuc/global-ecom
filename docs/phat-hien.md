# Phát hiện (T26)

Chín phát hiện, xếp theo mạch bốn hồi của báo cáo: **Quy mô → Cấu trúc → Vị trí
Việt Nam → Ý nghĩa**. Mỗi phát hiện ghi kèm script sinh ra nó.

Câu trả lời tổng cho toàn bộ bài:

> **Việt Nam đã leo rất nhanh trong thương mại toàn cầu, nhưng leo bằng cách
> trở thành công xưởng lắp ráp cho một khối do Trung Quốc dẫn đầu — bán nhiều
> tiền hơn qua ít cửa hơn.**

---

## Hồi 1 — Quy mô: mạng lưới này có hình gì

### F1. Mạng thương mại KHÔNG phải mạng scale-free

`src/make_degree_dist.py`

Giả định phổ biến — mạng thương mại có vài hub lớn và một đuôi dài — không đứng
vững trước dữ liệu. Năm 2023, mật độ mạng là **51,8%**: một nước trung bình
giao thương với hơn một nửa thế giới. Bậc lớn nhất (**447**) chỉ gấp **1,8 lần**
bậc trung vị (**242**). Trong một mạng scale-free thật, tỷ lệ đó là hàng trăm
lần.

Trên thang log-log, phân bố thực tế không phải đường thẳng — nó gần như phẳng
rồi rơi dựng đứng ở cuối, nằm gần đường của một mạng ngẫu nhiên cùng mật độ hơn
hẳn đường luật lũy thừa.

Và xu hướng đi **ngược** phía scale-free: tỷ lệ max/trung vị giảm đều từ **2,6**
(1995) xuống **1,8** (2023).

**Vì sao quan trọng:** khi gần như ai cũng nối với ai, "hub" theo nghĩa tô-pô
không tồn tại — với bất kỳ nước nào. Đây là nền tảng để đọc đúng phát hiện F7
về betweenness của Việt Nam.

### F2. Cấu trúc nằm ở trọng số, không nằm ở tô-pô

`src/analyze_network.py`

| Chỉ số | 2023 |
|---|---|
| Gini theo trọng số cạnh | **0,957** |
| Top 1% số cạnh giữ | **61,2%** giá trị |
| Đối ứng (reciprocity) | 0,837 |

Gini 0,957 là mức tập trung cực đoan, và nó **ổn định** suốt 1995–2023
(0,955 → 0,957). Nghĩa là: thế giới không trở nên công bằng hơn hay bất bình
đẳng hơn về thương mại trong gần ba thập kỷ — nó giữ nguyên hình dạng, chỉ lớn
lên.

**Hệ quả phương pháp:** mọi phép lọc phải lọc theo **giá trị**, không theo bậc.
Lọc theo bậc trong một mạng mật độ 51,8% thì hoặc giữ gần hết, hoặc cắt bừa.

---

## Hồi 2 — Cấu trúc: thế giới chia theo đường nào

### F3. Ba khối địa lý, và ASEAN không phải một trong số đó

`src/make_node_link.py`, `src/compute_metrics.py`

Louvain trên đồ thị đã lọc (73 nút, 416 cạnh) cho đúng **3 cụm**:

| Khối | Số nước | Thành phần | Dẫn đầu |
|---|---|---|---|
| Châu Á do Trung Quốc dẫn đầu | **41** | 29 châu Á, 5 châu Phi, 4 châu Mỹ, 2 Đại Dương, 1 Âu | CHN, JPN, KOR, HKG, TWN, IND |
| Châu Âu | 25 | 21 châu Âu | DEU, FRA, NLD, ITA, GBR |
| Bắc Mỹ do Hoa Kỳ dẫn đầu | 7 | 6 châu Mỹ | USA, MEX, CAN |

**Cả 10/10 nước ASEAN đều rơi vào khối 0** — cùng Trung Quốc, Nhật, Hàn, Ấn,
vùng Vịnh, Úc, và cả Brazil, Nga, Nam Phi.

Đây là phát hiện đi ngược trực giác nhất của đồ án. ASEAN là một khối kinh tế
có thật về mặt thể chế, nhưng **về mặt dữ liệu thương mại nó không hiện ra như
một đơn vị**: các nước ASEAN gắn với Trung Quốc chặt hơn là gắn với nhau.

Kết quả này **ổn định tuyệt đối**: 20 hạt giống ngẫu nhiên, **100,0% số cặp
nước giữ nguyên quan hệ**, modularity không đổi (0,337).

### F4. Thứ tự hàng cột chính là thuật toán trực quan hóa

`src/make_adjacency.py`

Hai ma trận kề 73×73 chứa **đúng cùng 416 luồng** — không thêm, không bớt một
bit nào. Bản sắp theo tên nước trông như nhiễu rắc đều. Bản sắp theo cụm Louvain
hiện ra **ba khối vuông đặc trên đường chéo**.

Đo được: mật độ trong khối **12,9%** so với ngoài khối **4,1%** — đặc gấp
**3,1 lần**.

**Vì sao quan trọng:** đây là minh họa trực tiếp cho nội dung mục 9.1 của giáo
trình. Với ma trận kề, chọn thứ tự hàng cột (seriation) không phải thao tác
trang trí — nó **là** thuật toán trực quan hóa. Toàn bộ "cấu trúc" người xem
thấy ở bản phải vốn đã nằm sẵn trong dữ liệu ở bản trái, chỉ là không nhìn ra.

### F5. Node-link và ma trận kề trả lời hai câu hỏi khác nhau

| | Node-link | Ma trận kề |
|---|---|---|
| Hình dáng tổng thể | ✅ | ❌ |
| Tra một cặp nước cụ thể | ❌ cạnh chồng nhau | ✅ tức thì |
| Đọc mật độ trong khối | ❌ | ✅ |
| Thấy đường đi, nút trung gian | ✅ | ❌ |
| Chịu được đồ thị dày | ❌ phải lọc còn 416 cạnh | ✅ |

Không họa đồ nào thay được họa đồ kia. Node-link trả lời "mạng này hình gì";
ma trận trả lời "hai nước này có buôn với nhau không".

---

## Hồi 3 — Vị trí Việt Nam: bán cái gì, cho ai

### F6. Việt Nam đã thay hẳn mặt hàng, không phải tăng trưởng đều

`src/make_streamgraph.py`, `src/make_hierarchy_charts.py`

| Ngành | 1995 | 2023 | Đổi |
|---|---|---|---|
| Điện tử | 0,6% | **29,9%** | **+29,3** điểm |
| Máy móc và thiết bị | 1,4% | 14,4% | +13,0 |
| Khác | 0,4% | 11,8% | +11,4 |
| Kim loại | 0,9% | 4,6% | +3,7 |
| Hóa chất và nhựa | 2,5% | 5,1% | +2,6 |
| Phương tiện vận tải | 0,4% | 1,8% | +1,4 |
| Đá, thủy tinh, gốm sứ | 1,5% | 0,8% | −0,6 |
| Dệt may, giày dép, nội thất | 28,8% | 18,4% | −10,4 |
| Khoáng sản và nhiên liệu | 20,6% | 1,4% | −19,1 |
| Nông sản, gỗ và giấy | **42,9%** | 11,6% | **−31,4** |

Tổng kim ngạch: **5,1 tỷ USD → 385,5 tỷ USD**, tăng **75,3 lần**.

Năm 1995 Việt Nam là một nước bán nông sản và dầu thô — hai ngành này chiếm
**63,5%** kim ngạch. Năm 2023 chúng còn **13,0%**, còn điện tử một mình chiếm
gần một phần ba.

### F7. Chỉ số phức hợp kinh tế xác nhận độc lập

`src/build_intermediate.py`

ECI của Việt Nam: **−1,00 (hạng 181/211)** năm 1995 → **+0,58 (hạng 78/230)**
năm 2023. Đây là một thước đo hoàn toàn khác — nó đo mức độ tinh vi và độc
quyền của rổ hàng xuất khẩu, không đo kim ngạch — nên việc nó cùng chiều với
F6 là bằng chứng độc lập.

⚠️ Phải đọc kèm mẫu số: số nước được xếp hạng đổi từ 211 lên 230.

### F8. Việt Nam khác các nước ASEAN cùng cỡ ở dệt may, không ở chế tạo

`src/make_small_multiples.py`

| | VNM | THA | MYS | IDN |
|---|---|---|---|---|
| Dệt may, giày dép, nội thất | **18,4%** | 2,9% | 1,9% | 7,9% |
| Tổng bốn ngành chế tạo | **64,6%** | 48,6% | 47,6% | 21,7% |
| Ngành lớn nhất | Điện tử 29,9% | Nông sản 18,3% | **Điện tử 33,0%** | Khoáng sản 26,1% |

⚠️ **Không được nói** "Việt Nam chế tạo nhiều hơn các nước ASEAN cùng cỡ" một
cách chung chung: Malaysia có tỷ trọng điện tử **33,0%**, cao hơn Việt Nam. Một
người xem đối chiếu bảng sẽ bắt được mâu thuẫn ngay.

Câu đúng và kiểm được: **Việt Nam là nước duy nhất trong nhóm còn dựa mạnh vào
dệt may và giày dép** — 18,4%, gấp **2,3 lần** nước thứ hai (Indonesia 7,9%).

### F9. Nghịch lý phức hợp

`src/build_intermediate.py`

Lợi thế so sánh biểu lộ (RCA) của Việt Nam **mạnh nhất ở nơi sản phẩm đơn giản
nhất** — giày dép RCA **7,52**, cà phê/chè/gia vị RCA **4,21** — và **yếu nhất
ở nơi sản phẩm phức tạp nhất**: máy móc công nghiệp và thiết bị quang học.

Việt Nam xuất khẩu rất nhiều điện tử, nhưng lợi thế so sánh thật sự vẫn nằm ở
giày dép và cà phê. Hai điều đó cùng đúng, và mâu thuẫn biểu kiến ấy được giải
ở F11.

---

## Hồi 4 — Ý nghĩa: vị trí đó bền đến đâu

### F10. Tiền tăng, cửa giảm — phát hiện mạnh nhất của đồ án

`src/make_time_multiples.py`

| Năm | Số thị trường xuất khẩu | Tổng xuất khẩu |
|---|---|---|
| 1995 | 98 | 5,1 tỷ USD |
| 2005 | **200** ← đỉnh | 32,9 tỷ USD |
| 2015 | 181 | 169,4 tỷ USD |
| 2023 | **166** | 385,5 tỷ USD |

Từ đỉnh 2005: **mất 34 thị trường**, trong khi tiền tăng **11,7 lần**.

Cùng một hiện tượng, nhìn từ góc khác: năm 2023 Việt Nam đứng **hạng 16/231**
về kim ngạch nhưng chỉ **hạng 67/231** về số bạn hàng.

**Diễn giải:** bán được nhiều hơn qua ít cửa hơn không phải một thành tích. Nó
là rủi ro tập trung: một thị trường đóng lại hôm nay gây thiệt hại lớn hơn hẳn
so với hai mươi năm trước.

### F11. Việt Nam là công xưởng lắp ráp — và đây là lời giải cho F9

`src/make_sankey.py`

| | 2023 |
|---|---|
| Nhập khẩu | **332,1 tỷ USD** từ 149 nguồn |
| Xuất khẩu | **385,5 tỷ USD** sang 166 thị trường |
| Nhập / xuất | **86,1%** |
| Giá trị gia tăng trong nước | **13,9%** |
| Nguồn nhập lớn nhất | Trung Quốc **40,1%** |
| Thị trường xuất lớn nhất | Hoa Kỳ **24,7%** |

Cứ mỗi đồng hàng bán ra, **86 xu là hàng đã mua từ nước khác**. Linh kiện vào
chủ yếu từ Trung Quốc, thành phẩm ra chủ yếu sang Hoa Kỳ.

Đây là lời giải cho nghịch lý F9: Việt Nam **xuất khẩu** điện tử nhưng không
**sản xuất** phần phức tạp của nó. Phần phức tạp được nhập về; phần Việt Nam
làm là khâu lắp ráp. RCA đo cái nước đó thật sự giỏi, và nó chỉ ra giày dép —
đúng với thực tế.

⚠️ **Giới hạn phải nói thẳng:** Sankey này **không** truy vết được lô hàng.
Dữ liệu cho biết Việt Nam nhập bao nhiêu từ Hàn Quốc và xuất bao nhiêu sang Mỹ,
nhưng **không** cho biết hàng Hàn Quốc có đi tiếp sang Mỹ hay không. Hai bên
nút Việt Nam là hai phép đo riêng đặt cạnh nhau, không phải một dòng chảy liên
tục. Con số 86,1% đo **mức phụ thuộc đầu vào**, không chứng minh trung chuyển.

### F12. Giả thuyết "nút trung chuyển" đúng một nửa

`src/compute_metrics.py` + `src/make_sankey.py`

| Cách đo | Kết quả | Kết luận |
|---|---|---|
| Tô-pô mạng (betweenness) | **0,0000**, đồng hạng với 57 nước | **KHÔNG** phải nút trung chuyển |
| Dòng tiền (nhập/xuất) | 86,1%, giá trị gia tăng 13,9% | **ĐÚNG** là công xưởng lắp ráp |

Hai nửa phải tách nhau ra. Theo lý thuyết đồ thị thì không — Việt Nam không nằm
trên đường đi ngắn nhất giữa các nước khác, vì mạng mật độ 51,8% (F1) khiến
không ai cần đi vòng qua ai. Theo dòng tiền thì có — Việt Nam mua đầu vào và
bán đầu ra với 14% giá trị thêm vào.

Trả lời "có" hoặc "không" một cách gọn lỏn đều sai.

### F13. Thương mại nội khối ASEAN nhỏ hơn người ta tưởng

`src/make_chord.py`

Việt Nam xuất khẩu đi đâu, 2023:

| Khối | Giá trị | Tỷ trọng | Cộng dồn |
|---|---|---|---|
| Đông Á | 143,4 tỷ | **37,2%** | 37,2% |
| Bắc Mỹ | 103,0 tỷ | **26,7%** | **63,9%** |
| Châu Âu | 62,5 tỷ | 16,2% | 80,1% |
| Đông Nam Á (trừ VN) | 30,0 tỷ | **7,8%** | 87,9% |
| Nam và Tây Á | 22,8 tỷ | 5,9% | 93,8% |
| Mỹ Latinh | 14,3 tỷ | 3,7% | 97,5% |
| Châu Đại Dương | 6,1 tỷ | 1,6% | 99,1% |
| Châu Phi | 3,5 tỷ | 0,9% | 100,0% |

**63,9%** hàng Việt Nam bán ra đi về Đông Á và Bắc Mỹ. Mười nước láng giềng
ASEAN — cùng khối kinh tế, cùng hiệp định — chỉ nhận **7,8%**.

Cộng với F3: ASEAN không phải một khối thương mại, cả về **cấu trúc** (Louvain
không tách được nó ra) lẫn về **dòng tiền** (chỉ 7,8% kim ngạch).

### F14. Dữ liệu đã bị hòa giải — ta không tự đo được sai số của nó

`src/compare_mirror.py`

**2.093 / 2.093 luồng lớn (100,0%)** có số nước xuất khai và số nước nhập khai
trùng khít nhau. Trung vị chênh lệch 0,0%; phân vị 10 và 90 đều 0,0%. Kết quả
lặp lại y hệt với năm 1995 (679/679).

Growth Lab đã hòa giải số liệu hai chiều trước khi phát hành. Chênh lệch gương
— phép kiểm độc lập tiêu chuẩn của thống kê thương mại — **không dùng được**
trên bộ dữ liệu này, vì bản khai thứ hai đã bị thay bằng một con số hòa giải.

Đây vừa là một giới hạn (mục 3.1 của Phương pháp luận) vừa là một phát hiện về
chính bộ dữ liệu, và nó là câu trả lời mạnh cho câu hỏi "các em có kiểm tra
chất lượng dữ liệu không" — mạnh hơn hẳn một bảng ba cột số giống nhau.

---

## Những gì KHÔNG tìm thấy

Nói ra cả những giả thuyết bị bác là một phần của trung thực nghiên cứu:

- **Không có khối ASEAN** trong cấu trúc cộng đồng (F3) — dù ASEAN là một khối
  kinh tế có thật về thể chế.
- **Không có hub** theo nghĩa tô-pô (F1) — mạng quá dày để hub tồn tại.
- **Không có bằng chứng trung chuyển** theo nghĩa đồ thị (F12) — betweenness
  bằng 0.
- **Không đo được sai số dữ liệu** (F14) — nguồn đã hòa giải.
- **Không có xu hướng tập trung hóa hay phân tán hóa** của thương mại thế giới
  (F2) — Gini đứng yên ở 0,957 suốt 29 năm.

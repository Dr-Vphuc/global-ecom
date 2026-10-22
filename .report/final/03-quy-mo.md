# 3. Quy mô: thế giới lớn lên 4,51 lần, Việt Nam lớn lên 75,3 lần

Hồi đầu của báo cáo chỉ làm một việc: đặt đúng tỷ lệ. Mọi phát hiện về cấu trúc ở
phần 4 và về vị trí ở phần 5 đều phải đọc trên nền quy mô này, vì **một nước lớn
nhanh gấp 16,7 lần mức bình quân thế giới thì mọi tỷ trọng của nó đều đang dịch
chuyển** — và điều đó buộc mọi phép đo phải dùng tỷ lệ chứ không dùng con số tuyệt
đối (xem §2.5).

## 3.1 Việt Nam đi từ hạng 61 lên hạng 16

`data/processed/edges.csv` · đồ thị **đầy đủ**, không lọc ngưỡng

| | 1995 | 2005 | 2015 | 2023 |
|---|---|---|---|---|
| Xuất khẩu toàn thế giới | 4.803,3 tỷ USD | 9.742,9 tỷ | 15.085,2 tỷ | **21.656,9 tỷ** |
| Xuất khẩu của Việt Nam | 5,12 tỷ USD | 32,87 tỷ | 169,41 tỷ | **385,54 tỷ** |
| Thị phần thế giới | 0,107% | 0,337% | 1,123% | **1,780%** |
| Hạng theo giá trị xuất khẩu ¹ | 61/211 | 48/224 | 23/230 | **16/230** |

¹ mẫu số là **số nước thật sự có xuất khẩu** năm đó. Năm 1995 cả 211 nút của
mạng đều xuất; năm 2023 mạng có 231 nút nhưng chỉ 230 nước xuất — nút `ANS`
(vùng không xác định) chỉ xuất hiện ở chiều nhập. Sổ nhật ký §3 ghi *16/231* vì
lấy mẫu số là số nút trong mạng; **hạng không đổi**, chỉ mẫu số khác định nghĩa.

Thế giới gấp **4,51 lần** trong 29 năm; Việt Nam gấp **75,3 lần** — nhanh hơn
**16,7 lần**. Thị phần nhân lên gần **17 lần**, và vị trí trong bảng giá trị xuất
khẩu đi từ nửa dưới (61/211) lên **hạng 16 thế giới**.

Trong ASEAN, trật tự đã đảo hẳn. Năm 1995 Việt Nam đứng **thứ sáu trên mười**, sau
cả Philippines; năm 2023 Việt Nam **xuất khẩu nhiều nhất khối**:

| 1995 (tỷ USD) | 2023 (tỷ USD) |
|---|---|
| Singapore 98,1 · Malaysia 76,6 · Thái Lan 54,3 · Indonesia 47,1 · Philippines 17,7 · **Việt Nam 5,1** | **Việt Nam 385,5** · Malaysia 353,9 · Singapore 346,6 · Thái Lan 290,7 · Indonesia 253,9 · Philippines 81,8 |

Đây là con số mạnh nhất của báo cáo, và cũng là lý do ba phần sau phải tồn tại:
**bán nhiều nhất khối không có nghĩa là bán thứ đáng giá nhất khối** (§5.1), cũng
không có nghĩa là bán qua một mạng lưới rộng (§5.3).

Lấy lại: `PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/analyze_network.py`
· đối chiếu `country_year.csv`, `edges.csv` và `country_product.csv` cho cùng một
con số 5,1170 → 385,5390 tỷ USD, lệch **0,0000**

## 3.2 Rổ hàng được xây lại gần như từ đầu

`data/processed/country_product.csv` · 10 ngành cấp 1 của cây HS92 · T21, T12, T13

Quy mô lớn lên là một chuyện; **thứ đem bán đã đổi gần như hoàn toàn** là chuyện
khác, và đó mới là nền của đề xuất ở phần 7:

| Ngành cấp 1 | 1995 | 2005 | 2015 | 2023 | Đổi |
|---|---|---|---|---|---|
| Điện tử | 0,6% | 5,4% | 26,2% | **29,9%** | **+29,3 đ%** |
| Máy móc và thiết bị | 1,4% | 5,0% | 8,7% | **14,4%** | +13,0 đ% |
| *Chưa phân loại* | 0,4% | 2,5% | 9,6% | *11,8%* | *+11,4 đ%* |
| Kim loại | 0,9% | 2,3% | 3,3% | 4,6% | +3,7 đ% |
| Hóa chất và nhựa | 2,5% | 5,1% | 4,4% | 5,1% | +2,6 đ% |
| Phương tiện vận tải | 0,4% | 1,4% | 1,8% | 1,8% | +1,4 đ% |
| Đá, thủy tinh, gốm sứ | 1,5% | 1,4% | 1,4% | 0,8% | −0,6 đ% |
| Dệt may, giày dép, nội thất | 28,8% | 30,6% | 25,5% | 18,4% | −10,4 đ% |
| Khoáng sản và nhiên liệu | 20,6% | 24,3% | 3,5% | 1,4% | **−19,1 đ%** |
| Nông sản, gỗ và giấy | **42,9%** | 22,1% | 15,6% | 11,6% | **−31,4 đ%** |

Hai ngành đổi chỗ cho nhau: **nông sản, gỗ và giấy** từ gần nửa rổ hàng (42,9%)
xuống 11,6%, còn **điện tử** từ 0,6% — gần như không có gì — lên gần một phần ba.
Khoáng sản và nhiên liệu gần như biến mất, 20,6% → 1,4%. Đây là lý do streamgraph
T21 phải vẽ **hai tầng**: cơ cấu năm 1995 chỉ chiếm **1,3% chiều cao** nếu vẽ
chung một thang tuyến tính với 2023, nên một hình một tầng sẽ ép 29 năm đầu thành
một vạch mỏng.

⚠️ Dòng in nghiêng **không phải một ngành**. Ô *Chưa phân loại* là nhóm HS2 `99`
của Atlas với nút con duy nhất `XXXX` (*Trade data discrepancies*), và nó đã nở từ
0,4% lên **11,8% rổ hàng** — tức gần một phần tám kim ngạch xuất khẩu của Việt Nam
nằm ở một ô dữ liệu không nói được là hàng gì. Báo cáo **không** đọc ô đó thành
một ngành, và quy tắc chọn đề xuất loại thẳng nó (§7.1, §A.3). Nhưng phải nêu ra,
vì nó cũng có nghĩa là mọi tỷ trọng ngành ở bảng trên đều **nhỏ hơn thực tế** một
chút.

Mỗi năm tỷ trọng cộng đủ 100%, lệch lớn nhất **0,000000** — phép kiểm tự in trong
khối KIỂM CHỨNG của T21.

Lấy lại: `src/make_streamgraph.py` (bảng trên in nguyên trong khối KIỂM CHỨNG) ·
`src/make_hierarchy_charts.py --year 1995|2023` cho treemap và sunburst của cùng
rổ hàng ở hai năm

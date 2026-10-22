# 5. Vị trí Việt Nam: trèo lên thật, qua một hành lang đang hẹp lại

Hồi ba là phần có nhiều phát hiện nhất, và nó đi theo ba bước: Việt Nam **có** đi
lên trong bảng xếp hạng năng lực (§5.1); nhưng cách đi lên là một **hành lang** có
hai đầu ngược dấu (§5.2); và hành lang ấy **đang hẹp lại ở cả hai đầu** — đo bằng
một phép đo mà chính báo cáo này đã phải thay (§5.3).

## 5.1 Việt Nam đi lên thật, và đo được

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
**một phần** đến từ 115,43 tỷ USD điện tử — mà §6.1 sẽ cho thấy lợi thế so sánh
trong điện tử chỉ ở mức 2,23, tức gần đúng bằng tỷ lệ điện tử trong thương mại thế
giới.

---

## 5.2 Hành lang đo được: mua của Trung Quốc, bán cho Hoa Kỳ

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

Hình này dùng đồ thị **đầy đủ**, và đó là lựa chọn bắt buộc: dựng cùng hình trên
đồ thị đã lọc thì cán cân **lật dấu** thành *"nhập siêu 15,17 tỷ USD"*. Bảng đo
chỗ lật dấu đó, cùng quy tắc **không so trực tiếp con số của hai nhóm hình**, nằm
ở §2.5 (phát hiện A15).

Lấy lại: `src/make_sankey.py` · Hình: `output/sankey_vietnam_{1995,2023}.png`

---

## 5.3 Kênh bán: phép đo nào bền, phép đo nào không — và vì sao phải đổi phép đo

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
nó so được với thế giới cùng ASEAN trên cùng phép đo. Đặt cạnh §5.2 thì hai phát
hiện khớp nhau: tiền dồn vào ba cửa, mà một trong ba cửa ấy (Trung Quốc) đồng thời
là nơi hàng **vào** nhiều nhất.

**Và phía mua vào còn tập trung hơn hẳn.** Chạy cùng phép đo trên chiều nhập khẩu:
HHI **0,0973** (1995) → đáy **0,0791** (2003) → **0,1979** (2023), top-3 nhà cung
cấp chiếm **61,3%** so với 44,4% năm 1995, và số nhà cung cấp chiếm trên 1% **giảm
từ 16 xuống 14**. Tức mức tập trung đầu vào (0,1979) **gấp 1,6 lần** mức tập trung
đầu ra (0,1226). Hành lang ở §5.2 hẹp ở cả hai đầu, nhưng **hẹp hơn ở đầu mua**.
Lệnh: `src/make_time_multiples.py --direction nhap`.

Lấy lại: `src/make_time_multiples.py` (khối KIỂM CHỨNG in cả HHI và tỷ trọng
top-3) · dữ liệu gốc `data/processed/edges.csv`

---


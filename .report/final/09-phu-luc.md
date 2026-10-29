# Phụ lục

> Năm mục dưới đây **đã nằm trong phần Phương pháp luận** khi mục đó được viết
> (T25) và được chuyển về phụ lục khi ráp báo cáo (T27), để phần thân giữ đúng mạch
> lập luận. Chúng giữ nguyên nội dung, chỉ đổi số hiệu — **§A.1** trước là mục
> 2.4, **§A.2** là 2.6, **§A.3** là 2.8, **§A.4** là 2.9, **§A.5** là 2.12 của
> bản Phương pháp luận. Không mục nào bị cắt bớt.

## A.1 Từ dữ liệu thô đến mười bảng sạch

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
| `threshold_coverage.csv` | 21 phương án lọc cạnh — bằng chứng cho §2.5 | 21 |
| `metrics.csv` | chỉ số mạng theo nước, mỗi nước hai dòng (§2.5) | 304 |
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

## A.2 Sáu cửa kiểm chạy tự động

Toàn bộ đều là script, trả về mã thoát khác 0 khi không đạt, nên cắm được vào CI.
Đây là phần chứng minh dữ liệu **được kiểm** chứ không phải được tin.

| # | Cửa kiểm | Kiểm gì | Kết quả đo được |
|---|---|---|---|
| 1 | `check_raw_data.py` | 8 mục trên file thô, kể cả "16 nước xuất khẩu lớn nhất phải có mặt" | **ĐẠT** |
| 2 | ECI đã chuẩn hoá | mỗi năm trung bình ≈ 0, độ lệch chuẩn ≈ 1 trên toàn bộ các nước — đây là tính chất của cách tính, nên đọc lệch cột hay mất dòng là hai số này trồi ngay | `\|trung bình\| ≤ 0,076`; `\|độ lệch chuẩn − 1\| ≤ 0,054` |
| 3 | Trung bình RCA có trọng số = 1 | tính chất toán học của công thức Balassa: với mỗi sản phẩm, trung bình RCA của các nước có trọng số theo quy mô nước phải đúng bằng 1. Sai là công thức sai | lệch **1,0 × 10⁻¹⁵** (xem §2.4) |
| 4 | Đối chiếu chéo ba file | ba file Atlas đo cùng nền thương mại từ ba góc | khớp **0,000%** |
| 5 | `check_tree.py` | cây HS92: số nút từng tầng, nút mồ côi, chu trình, quy tắc mã | `{1: 10, 2: 97, 4: 1.243, 6: 5.040}`, **0 nút mồ côi**; **1 lỗi + 1 lưu ý** → §A.3 |
| 6 | `check_palette.py` + `check_readability.py` | hai cửa chặn thị giác: bảng màu và khả năng đọc | **ĐẠT**; cả **10 script** dựng hình đều trên khung point (§A.4) |

Cửa số 5 đáng chú ý vì **nó không sạch**, và nhóm giữ nguyên kết quả không sạch đó
thay vì nới điều kiện kiểm cho nó qua — chi tiết ở **§A.3**. Một phép kiểm chỉ có
giá trị khi nó được phép báo lỗi.

---

## A.3 Cây sản phẩm HS92: hai chỗ lệch đã đo

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
không phân loại được**, không phải một ngành hàng có thật để mà đề xuất đầu tư. Vì vậy quy tắc chọn đề xuất ở §7.1 **loại thẳng ngành
*Chưa phân loại*** (`sector != UNCLASSIFIED`), và hình T31 vẽ nó ở màu xám trung
tính để người đọc thấy nó tồn tại mà không đọc nó như một lựa chọn.

---

## A.4 Quy ước trực quan hoá: những gì đo được thì đã đo

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

### Và vì sao mọi tiêu đề hình đều dựng từ dữ liệu

Toàn bộ tiêu đề trên các hình tuân theo một nguyên tắc: **tiêu đề dựng từ dữ liệu
của chính lần chạy đó, không viết sẵn**. Lý do rất thực tế — một tiêu đề viết sẵn
sẽ in ra một câu sai khi chạy năm khác. Đã bắt được **bốn lần**:

| Hình | Câu viết sẵn | Dữ liệu nói gì |
|---|---|---|
| T09 | *"gần như đều"* | sai cho năm 1995 (lệch khỏi phân bố đều 0,180 so với 0,056) |
| T15 | *"ba cụm là ba châu lục"* | sai — cụm lớn là một khối Á–Thái Bình Dương |
| T14 | *"Việt Nam dựa mạnh vào dệt may"* | năm 1995 là **nông sản, gỗ và giấy 42,9%** so với 26,0% của nước cao thứ nhì |
| T20 | *"đạt đỉnh 200 nước năm 2005"* | đỉnh thật là **2002 với 208 nước** — câu cũ chỉ tìm đỉnh trong bốn năm được vẽ (A13, A16) |

Vì vậy mỗi script còn **render thêm một năm đối chứng** (thường 1995) và in một
khối kiểm chứng ra stdout, đủ để kiểm lại khẳng định trên tiêu đề mà không cần mở
code.

## A.5 Tái lập toàn bộ

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
python src/check_tree.py            # 5. kiểm cây HS92 (§A.3)
python src/compute_metrics.py       # 6. metrics.csv, hai đồ thị (§2.5)
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

Hai lệnh thêm vào khi ráp báo cáo (T27):

| Con số | Lệnh |
|---|---|
| quy tắc chọn chạy ở 2007 — chọn điện tử trước đợt bùng nổ | `src/make_decision_plane.py --year 2007 --since 1999` |
| thế giới gấp 4,51 lần, Việt Nam gấp 75,3 lần, hạng 61 → 16 | `src/analyze_network.py` · `edges.csv` |

Nền so sánh của §7.2 — 45,4% trong 97 nhóm có RCA tăng, trung vị −0,0178 — đo trực
tiếp từ `data/processed/country_product.csv`, ghép hai năm theo `product_id`.

Sổ gốc của mọi con số: `docs/phat-hien-va-quyet-dinh.md` — phát hiện **A1–A19**,
quyết định thiết kế **B1–B28**, hạn chế **D1–D5**.

**Đối chiếu sang sổ phát hiện:** §3.2 ← A2 · §4.1 ← A3, A4, A7 · §4.2 ← A8,
A10, A11 · §5.1 ← A1 · §5.2 ← A12, A15 · §5.3 ← A9, A13, **A16** · §6.1 ← A2,
A14 · §6.2 ← **A19**, B27 · §6.3 ← B28 · §7.1–§7.2 ← A14, **A17** · §8.1 ← D1–D5, **A19**.

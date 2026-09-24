# global-ecom

**Đồ án cuối kỳ — Trực quan hóa dữ liệu**

Đề tài: *Mạng lưới thương mại quốc tế — vị trí của Việt Nam trong cấu trúc thương mại toàn cầu*, kèm một lát cắt sâu về quan hệ Việt Nam – ASEAN.

Kỹ thuật trọng tâm: *Visualization Techniques for Trees, Graphs, and Networks*.

Phân công chi tiết, hợp đồng dữ liệu và tiến độ nằm trong `phan-cong-cong-viec.xlsx`.

📌 **Viết báo cáo thì mở `docs/phat-hien-va-quyet-dinh.md` trước.** Nó gom mọi
phát hiện đã đo được, mọi quyết định đã chốt kèm lý do, và bốn hạn chế phải nêu
thẳng. README này chỉ nói cách chạy repo.

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
đo trên năm mốc **2024**:

| Chỉ số | Số cũ trong file phân công | Số đúng |
|---|---|---|
| Số cạnh | 25.425 (năm 2023) | **25.754** (năm 2024) |
| Số nút | 230 | **231** |
| Mật độ | 0,483 | **0,485** |
| Top 1% cạnh chiếm | 60,2% | **60,7%** |
| Ngưỡng 10 tỷ USD | 347 cạnh, 65,7% giá trị | **385 cạnh, 67,7% giá trị** |

⚠️ Con số 2024 trông gần giống số cũ, nhưng **đó là trùng hợp**: số cũ là năm
2023 đo trên dữ liệu cụt. Năm 2023 đo đúng cho ra 27.535 cạnh, lệch hơn 2.000.

Ba ô cần sửa tay trong file Excel: `Tổng quan!B7`,
`Phân công chi tiết!C14`, `Checklist nộp bài!C26`.

### Chỉ số phức tạp kinh tế — vị trí của Việt Nam

`data/processed/country_year.csv` mang **ECI** (Economic Complexity Index) của
Atlas. Đây là chỉ số đã chuẩn hoá: mỗi năm trung bình ≈ 0 và độ lệch chuẩn ≈ 1
trên toàn bộ các nước, nên đọc trực tiếp được như một điểm z.

| | 1995 | 2005 | 2015 | 2024 |
|---|---|---|---|---|
| **Việt Nam** | −1,00 (#181/211) | −0,12 (#132/224) | +0,24 (#109/230) | **+0,67 (#70/230)** |
| Thái Lan | +0,39 (#80) | +0,65 (#58) | +0,93 (#45) | +0,81 (#54) |
| Malaysia | +0,60 (#65) | +0,81 (#47) | +0,96 (#42) | +0,86 (#47) |
| Philippines | +0,11 (#101) | +0,27 (#97) | +0,58 (#77) | +0,74 (#60) |
| Indonesia | −0,14 (#120) | +0,17 (#108) | +0,28 (#104) | +0,22 (#115) |
| Singapore | +0,91 (#33) | +1,23 (#16) | +1,57 (#6) | +1,52 (#7) |

Việt Nam đi từ hạng 181/211 lên hạng 70/230 — từ nhóm 14% cuối bảng lên nhóm
30% đầu bảng trong 29 năm. Khoảng cách với Thái Lan thu từ **1,39** xuống
**0,14** điểm; Thái Lan đạt đỉnh năm 2015 rồi đi xuống.

Số nước được xếp hạng đổi theo năm (211 → 230), nên cột `eci_n` trong file là
bắt buộc khi vẽ biểu đồ thứ hạng theo thời gian — "hạng 70" không đọc được nếu
thiếu mẫu số.

⚠️ ECI tính trên rổ xuất khẩu **gộp**, nên một nước lắp ráp hàng phức tạp vẫn
được cộng điểm phức tạp dù giữ lại ít giá trị gia tăng. Đường ECI dốc đứng đi
kèm RCA điện tử chỉ 2,45 (xem `country_product.csv`) là một căng thẳng nên nêu
thẳng trong báo cáo, không nên lờ đi.

### Mạng lưới: hình thù và ngưỡng lọc (T09 + T10)

`src/analyze_network.py` đo mạng lưới rồi sinh ba file. Tóm tắt kết quả:

| | 1995 | 2024 |
|---|---|---|
| Số nút | 211 | 231 |
| Số cạnh | 18.411 | 25.754 |
| **Mật độ** | 0,416 | **0,485** |
| **Đối ứng** | 0,824 | **0,843** |
| **Gini trọng số cạnh** | 0,955 | **0,956** |

Ba con số in đậm là phát hiện chính của T09, và nó **ngược với trực giác về
mạng lưới**:

- **Mật độ 48,5%** — gần một nửa mọi cặp nước có giao dịch. Mạng xã hội hay mạng
  trích dẫn thường dưới 1%. Mạng thương mại gần như đầy.
- **Đối ứng 0,84** — A xuất sang B thì 84% khả năng B cũng xuất ngược lại. Hướng
  của cạnh mang rất ít thông tin, nên node-link **không cần mũi tên**; dùng mũi
  tên chỉ làm rối thêm mà không thêm ý nghĩa.
- **Gini 0,956, gần như đứng yên suốt 30 năm.** Mạng phình từ 18 nghìn lên 26
  nghìn cạnh nhưng độ lệch của giá trị không đổi.

Gộp lại: **cấu trúc trung tâm–ngoại vi của thương mại không nằm ở việc ai nối với
ai, mà nằm ở việc luồng nào lớn.**

Phân bố bậc xác nhận điều đó, và nó là kết quả đáng ngạc nhiên nhất của T09:

| Bậc xuất khẩu 2024 | min | p25 | trung vị | p75 | p90 | max |
|---|---|---|---|---|---|---|
| số bạn hàng | 0 | 55 | 104 | 170 | 209 | 228 |

Các nước **trải gần như đều** từ 0 đến 228 bạn hàng — đo cụ thể, CCDF lệch khỏi
một phân bố đều hoàn toàn nhiều nhất **0,046**. Nghĩa là mạng này *không có*
bậc đặc trưng và cũng *không có* hub theo nghĩa tô-pô: không tồn tại một nhóm
nhỏ các nước nối với tất cả trong khi phần còn lại nối với vài nước.

Hệ quả thực tế cho báo cáo: **biểu đồ log-log của T09 sẽ không ra đường thẳng.**
Sách giáo khoa hay minh hoạ mạng scale-free bằng một đường thẳng dốc; ở đây
đường CCDF sẽ đi ngang rồi rơi dốc đứng ở mép phải. Đó không phải lỗi dữ liệu —
đó là kết quả, và nó chính là lý do **phải lọc theo trọng số; lọc theo bậc vô
nghĩa** vì bậc không phân biệt được nước nào quan trọng.

### Quy tắc lọc cạnh đã chốt ở T10

```
giữ cạnh  ⟺  export_value ≥ 0,046% × tổng xuất khẩu thế giới CỦA NĂM ĐÓ
             HOẶC  nó nằm trong top 3 luồng xuất / top 3 luồng nhập
                   lớn nhất của một nước ASEAN
```

Trong `reference_data.py`: `THRESHOLD_SHARE = 0.00046` và `FOCUS_TOPK = 3`.

**Vì sao không dùng ngưỡng cố định 10 tỷ USD.** Thương mại thế giới tăng **4,54 lần**
từ 1995 (4,80 nghìn tỷ USD) đến 2024 (21,81 nghìn tỷ USD), nên một ngưỡng tính
bằng USD danh nghĩa đo hai năm bằng hai cái thước khác nhau:

| Năm | Ngưỡng cố định 10 tỷ USD | Quy tắc đã chốt |
|---|---|---|
| 1995 | 89 cạnh, 49,5% giá trị, **ASEAN 4/10** | 383 cạnh, 73,9% giá trị, ASEAN 10/10 |
| 2005 | 176 cạnh, 56,2% giá trị, ASEAN 5/10 | 406 cạnh, 70,2% giá trị, ASEAN 10/10 |
| 2015 | 270 cạnh, 61,6% giá trị, ASEAN 6/10 | 407 cạnh, 68,1% giá trị, ASEAN 10/10 |
| 2024 | 385 cạnh, 67,7% giá trị, ASEAN 7/10 | 408 cạnh, 68,1% giá trị, ASEAN 10/10 |

Cột trái là một cái bẫy: panel 1995 chỉ còn 89 cạnh và 25 nút, nên small
multiples sẽ **đọc thành "thương mại mới xuất hiện sau 1995"** trong khi sự thật
là "thương mại lớn lên". Cột phải giữ số cạnh ổn định 383–408 qua mọi năm mốc —
và trên cả 30 năm nó nằm gọn trong khoảng **378–438** — nên các panel so sánh
được với nhau.

**Vì sao có phần bảo hiểm cho ASEAN.** Ngưỡng tương đối một mình vẫn **xoá Việt
Nam khỏi năm 1995** (0 cạnh), và xoá Brunei, Lào, Myanmar khỏi hầu hết các năm.
Với một đề tài tên là *"vị trí của Việt Nam"* thì đó là lỗi chí mạng, không phải
chi tiết nhỏ. Giá phải trả cho phần bảo hiểm rất rẻ: **+23 cạnh** (385 → 408) và
**+0,4 điểm phần trăm** giá trị.

**Cái đang bị bỏ mất, nói thẳng trong báo cáo.** Quy tắc này giữ 1,6% số cạnh và
68,1% giá trị năm 2024 — tức là **vứt 98,4% số cạnh**. Phần bị vứt là hàng vạn
luồng nhỏ; cộng lại chúng bằng gần một phần ba thương mại thế giới. Node-link vì
vậy **không** đọc được là "bản đồ thương mại toàn cầu", mà là *"bản đồ các luồng
thương mại lớn, cộng với chỗ đứng của ASEAN trong đó"*. Ai muốn nhìn phần đuôi
phải xem ma trận kề (T16), vì ma trận chịu được nhiều cạnh hơn hẳn node-link.

Toàn bộ 21 phương án đã cân nhắc nằm trong `data/processed/threshold_coverage.csv`
— gồm cả họ ngưỡng tuyệt đối và họ "mỗi nước giữ k luồng lớn nhất" đã bị loại.

## Quyết định đã chốt

| | |
|---|---|
| Năm mốc | **2024** (`REFERENCE_YEAR`) — mọi con số một-năm phải lấy năm này |
| `is_focus` | **cả 10 nước ASEAN**, không chỉ Việt Nam |
| `export_value = 0` | loại bỏ — không phải một cạnh, cũng không phải một dòng xuất khẩu |
| `USP`, `ANS` | vẫn giữ trong `nodes.csv`; `USP` không có luồng nào suốt 30 năm và cũng vắng mặt trong file ECI |
| `sector_color` | đang là bảng màu tạm, phải thay ở T04 |
| Ngưỡng lọc cạnh | **chốt ở T10**: `THRESHOLD_SHARE = 0.00046` (tỷ lệ theo năm) + `FOCUS_TOPK = 3` |
| Mũi tên trên node-link | **không dùng** — đối ứng 0,84 nên hướng cạnh gần như vô nghĩa |

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
│   └── make_mock.py           # sinh dữ liệu giả (T05)
├── docs/             # phát hiện, quyết định, nguồn dữ liệu, kiến thức nền
├── .report/          # báo cáo LaTeX
└── phan-cong-cong-viec.xlsx
```

## Chạy pipeline

Cả năm script **chỉ dùng thư viện chuẩn** — chạy được ngay, không cần cài gì.

```bash
python src/download_atlas.py        # 0. tải dữ liệu thô + kiểm MD5
python src/check_raw_data.py        # 1. kiểm tra dữ liệu thô, phải báo DAT
python src/build_intermediate.py    # 2. sinh 5 file trung gian trong processed/
python src/analyze_network.py       # 3. thống kê mạng + bảng ngưỡng (T09, T10)
python src/make_mock.py             # 4. sinh dữ liệu giả để vẽ song song
```

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

Cả tám file đều bị `.gitignore` loại trừ — sinh lại bằng lệnh trên, không commit.

Phần phân tích mạng và vẽ biểu đồ cần thư viện ngoài:

```bash
python -m pip install -r requirements.txt
```

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

## Quy ước git

Dữ liệu thô không được commit (Nguyên tắc #5, Checklist #19). `.gitignore` đã cấu hình sẵn.

`data/atlas/cc_year.csv` (28 MB) **hiện đang bị theo dõi từ trước**. Thêm vào `.gitignore` không tự gỡ nó ra. Cần chạy lệnh sau — **thống nhất với cả nhóm trước khi chạy**, vì sau khi pull, file sẽ biến mất khỏi máy hai người kia và họ phải tải lại:

```bash
git rm --cached data/atlas/cc_year.csv
git commit -m "Gỡ dữ liệu thô khỏi git theo Nguyên tắc #5"
```

Lệnh này chỉ gỡ khỏi lần commit tới, không xóa khỏi lịch sử. Repo `.git` hiện mới 9,6 MB nên chưa cần viết lại lịch sử.

## Ghi chú

- `docs/phat-hien-va-quyet-dinh.md` — **số liệu cho báo cáo + quyết định đã chốt**
- `docs/nguon-du-lieu-vn-asean.md` — khảo sát các nguồn dữ liệu thương mại
- `docs/kien-thuc-nen-tang.md` — kiến thức kinh tế nền cho người làm dữ liệu

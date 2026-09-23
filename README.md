# global-ecom

**Đồ án cuối kỳ — Trực quan hóa dữ liệu**

Đề tài: *Mạng lưới thương mại quốc tế — vị trí của Việt Nam trong cấu trúc thương mại toàn cầu*, kèm một lát cắt sâu về quan hệ Việt Nam – ASEAN.

Kỹ thuật trọng tâm: *Visualization Techniques for Trees, Graphs, and Networks*.

Phân công chi tiết, hợp đồng dữ liệu và tiến độ nằm trong `phan-cong-cong-viec.xlsx`.

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

Hiện tại `python src/check_raw_data.py` báo `DAT` trên cả 7 mục kiểm tra.

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

## Quyết định đã chốt

| | |
|---|---|
| Năm mốc | **2024** (`REFERENCE_YEAR`) — mọi con số một-năm phải lấy năm này |
| `is_focus` | **cả 10 nước ASEAN**, không chỉ Việt Nam |
| `export_value = 0` | loại bỏ — không phải một cạnh, cũng không phải một dòng xuất khẩu |
| `USP`, `ANS` | vẫn giữ trong `nodes.csv`; `USP` không có luồng nào suốt 30 năm |
| `sector_color` | đang là bảng màu tạm, phải thay ở T04 |
| Ngưỡng lọc cạnh | `DEFAULT_THRESHOLD = 1e10` tạm thời, chốt lại ở T10 |

## Cấu trúc repo

```
global-ecom/
├── data/
│   ├── atlas/        # dữ liệu thô (bị .gitignore, trừ 3 file tra cứu nhỏ)
│   ├── processed/    # file trung gian — SINH LẠI, không commit
│   └── mock/         # dữ liệu giả đúng schema — CÓ commit
├── src/
│   ├── download_atlas.py      # tải dữ liệu thô, nối tiếp, kiểm MD5
│   ├── check_raw_data.py      # 7 mục kiểm tra toàn vẹn, cửa chặn
│   ├── reference_data.py      # tên nước tiếng Việt, vùng, hằng số chung
│   ├── build_intermediate.py  # atlas/ -> processed/ (4 file)
│   └── make_mock.py           # sinh dữ liệu giả (T05)
├── docs/             # ghi chú nguồn dữ liệu và kiến thức nền
├── .report/          # báo cáo LaTeX
└── phan-cong-cong-viec.xlsx
```

## Chạy pipeline

Cả bốn script **chỉ dùng thư viện chuẩn** — chạy được ngay, không cần cài gì.

```bash
python src/download_atlas.py        # 0. tải dữ liệu thô + kiểm MD5
python src/check_raw_data.py        # 1. kiểm tra dữ liệu thô, phải báo DAT
python src/build_intermediate.py    # 2. sinh 4 file trung gian trong processed/
python src/make_mock.py             # 3. sinh dữ liệu giả để vẽ song song
```

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

- `docs/nguon-du-lieu-vn-asean.md` — khảo sát các nguồn dữ liệu thương mại
- `docs/kien-thuc-nen-tang.md` — kiến thức kinh tế nền cho người làm dữ liệu

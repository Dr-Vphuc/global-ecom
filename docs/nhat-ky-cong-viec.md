# Nhật ký công việc — đã làm gì, nằm ở đâu, và vì sao

**Cập nhật 20/10/2026** · 13/30 việc Xong · `main` ở commit `adeefdb` (gộp PR #10)

Sổ này chỉ trả lời **một câu: "đã làm được gì rồi"**. Khi cần soạn slide, viết phần
Phương pháp luận, hay trả lời phản biện thì mở sổ này ra trước, nó dẫn sang chỗ cần.

| Cần gì | Mở file nào |
|---|---|
| Đã làm gì, ai làm, nằm ở file nào | **sổ này** |
| Tìm ra điều gì (A1–A9), chốt điều gì (B1–B12) | `docs/phat-hien-va-quyet-dinh.md` |
| Chạy lại pipeline thế nào, số liệu đã đo | `README.md` |
| Câu hỏi nghiên cứu, thông điệp, đối tượng | `docs/cau-hoi-nghien-cuu.md` |
| Màu, font, cỡ hình, quy ước nhãn | `docs/style-guide.md` |
| Nguồn dữ liệu và vì sao chọn nguồn đó | `docs/nguon-du-lieu-vn-asean.md` |
| ECI, RCA, PCI nghĩa là gì | `docs/kien-thuc-nen-tang.md` |

---

## 0. Một phút kể về đồ án

> Đồ án dựng **mạng lưới thương mại toàn cầu năm 2023** từ bộ Atlas of Economic
> Complexity của Harvard: 231 nước, 27.535 luồng xuất khẩu, tổng 21,66 nghìn tỷ USD.
> Trên mạng đó, đi tìm **vị trí của Việt Nam**.
>
> Câu trả lời tìm được, nói bằng một cặp số: từ 2015 đến 2023, xuất khẩu Việt Nam
> **tăng 2,28 lần** nhưng số bạn hàng **giảm từ 181 xuống 166** — trong khi trung vị
> cả thế giới là **tăng 1**. Tiền vào nhiều hơn qua ít kênh hơn: 3 thị trường đầu
> (Hoa Kỳ, Trung Quốc, Hàn Quốc) chiếm **52,41%** hàng xuất, còn 9 nước ASEAN còn
> lại cộng lại chỉ **7,77%**.
>
> Nên "hội nhập sâu" và "phụ thuộc hẹp" ở đây là **cùng một hiện tượng**, và đó là
> điều các biểu đồ phải cho người xem thấy.

Ba con số đỡ cho câu đó: xuất khẩu Việt Nam **hạng 16/231** về giá trị, nhưng
**hạng 66/231** về số bạn hàng và **hạng 78/230** về chỉ số phức tạp kinh tế (ECI
+0,579). Bán nhiều, bán tới ít chỗ, bán thứ không khó làm.

---

## 1. Tiến độ 30 việc

Cột cuối là **sản phẩm thật**, khác với cột "Đầu ra cụ thể" trong file phân công —
cột đó là dự kiến, cột này là cái đang nằm trong repo.

⚠️ `data/processed/` và `output/` đều bị `.gitignore` — ai clone về sẽ **không có** file nào trong hai thư mục đó, phải chạy lại pipeline theo README. Đừng mang laptop đi
thuyết trình mà chưa sinh lại biểu đồ.

### Giai đoạn 1 — Nền tảng (5/5 Xong)

| Mã | Việc | Trạng thái | Sản phẩm thật |
|---|---|---|---|
| T01 | Câu hỏi nghiên cứu + thông điệp + đối tượng | Xong | `docs/cau-hoi-nghien-cuu.md` |
| T02 | Hợp đồng dữ liệu: chốt tên cột 5 file trung gian | Xong | sheet *Hợp đồng dữ liệu* |
| T03 | Dựng repo, `.gitignore`, README tải lại dữ liệu | Xong | `README.md`, `.gitignore` |
| T04 | Hệ thống thị giác: màu, font, cỡ hình, nhãn | Xong | `docs/style-guide.md`, `src/check_palette.py` |
| T05 | Dữ liệu giả đúng schema để vẽ trước | Xong | `src/make_mock.py` → `data/mock/` |

### Giai đoạn 2 — Dữ liệu (4/6 Xong, 1 đang làm)

| Mã | Việc | Trạng thái | Sản phẩm thật |
|---|---|---|---|
| T06 | Tải Atlas từ Harvard Dataverse | Xong | `src/download_atlas.py` (dữ liệu thô **không** vào git) |
| T07 | Làm sạch, xuất file trung gian, gắn vùng địa lý | Xong | `src/build_intermediate.py` → `nodes/edges/tree/country_product/country_year.csv` |
| T08 | Đối chiếu Atlas với BACI và Comtrade | **Chưa** | *cần tài khoản CEPII + khóa API Comtrade — chỉ thành viên nhóm làm được* |
| T09 | Thống kê mô tả mạng lưới theo từng năm | **Đang làm** | `network_stats.csv` (30 năm) xong; **còn thiếu biểu đồ phân bố bậc log-log** |
| T10 | Chốt ngưỡng lọc cạnh, biện minh bằng số | Xong | `threshold_coverage.csv`, quy tắc ở README §"Quy tắc lọc cạnh" |
| T11 | Kiểm chất lượng cây HS92 4 tầng | Xong | `src/check_tree.py` |

### Giai đoạn 3 — Trực quan hóa (4/10 Xong)

| Mã | Việc | Trạng thái | Sản phẩm thật |
|---|---|---|---|
| T12 | Treemap cơ cấu xuất khẩu VN, 2 mốc | Xong | `src/make_hierarchy_charts.py --year 1995\|2023` → `output/treemap_vnm_1995.*`, `_2023.*` |
| T13 | Sunburst 4 tầng cây sản phẩm | Xong | cùng script → `output/sunburst_vnm_1995.*`, `_2023.*` |
| T14 | Small multiples so VN với Thái–Mã–Indo | Xong | `src/make_small_multiples.py` → `output/small_multiples_vnm-tha-mys-idn_2023.*` |
| T15 | Node-link mạng đã lọc, mã hóa bậc + cộng đồng | **Chưa** | — (T18 đã mở đường: có bậc và cộng đồng để mã hóa) |
| T16 | Hai ma trận kề, một theo alphabet một theo cụm | **Chưa** | — (thứ tự cụm lấy ở `metrics.csv` dòng `filtered`) |
| T17 | Chord diagram giữa các khối, VN làm trọng tâm | **Chưa** | — |
| T18 | Chỉ số mạng: bậc, độ mạnh, betweenness, cộng đồng | Xong | `src/compute_metrics.py` → `metrics.csv` (304 dòng), `metrics_top20.csv` |
| T19 | Sankey nhập → VN → xuất (kiểm giả thuyết trung chuyển) | **Chưa** | — |
| T20 | Small multiples theo thời gian 1995·2005·2015·2023 | **Chưa** | — (phát hiện **A9** viết sẵn cho hình này) |
| T21 | Streamgraph 10 ngành, 1995–2023 | **Chưa** | — |

### Giai đoạn 4 — Tích hợp (0/5) · Giai đoạn 5 — Hoàn thiện (0/4)

| Mã | Việc | Trạng thái | Ghi chú đã có sẵn cho việc đó |
|---|---|---|---|
| T22 | Áp hệ thống thị giác lên toàn bộ biểu đồ 3 người | Chưa | 4 biểu đồ đầu **đã** đi qua `fmt_vn`/`fmt_pct`/`fmt_usd` + `separators=",."` (PR #9) |
| T23 | Rà soát chéo, mỗi người review 2 hình của người khác | Chưa | checklist ở `style-guide.md` §7 |
| T24 | Kiểm khả năng đọc: nhãn, chú giải, tương phản, mù màu | Chưa | bảng màu đã kiểm mù màu sẵn ở T04 |
| T25 | Viết phần Phương pháp luận | Chưa | **phải nêu**: hạn chế D1–D5, nút `3501` lệch cây HS92, mã `XXXX dưới 99` |
| T26 | Viết phần Phát hiện | Chưa | nguyên mục A1–A9 của sổ phát hiện là bản thảo |
| T27 | Ráp báo cáo cuối theo mạch 4 hồi | Chưa | mạch chuyện đề xuất ở sổ phát hiện §E |
| T28 | Slide thuyết trình | Chưa | §0 sổ này là bản nháp lời mở |
| T29 | Diễn tập + 10 câu phản biện | Chưa | §4 sổ này có 7 câu kèm câu trả lời |
| T30 | Dọn repo, README tái lập được | Chưa | README đã có mục tải dữ liệu + chạy pipeline |

---

## 2. Nhật ký theo mốc — PR nào mang gì vào `main`

| Ngày gộp | PR | Mang vào | Việc |
|---|---|---|---|
| 07/09 | #1, #2 | khung repo, dữ liệu công khai ban đầu | T03 |
| 23/09 | #3 ² | **gỡ dữ liệu thô khỏi git theo Nguyên tắc #5**; dựng pipeline; sửa dữ liệu bị cắt cụt | T06, T07 |
| 24/09 | #3 | thống kê mạng 30 năm + chốt ngưỡng lọc; dữ liệu ECI; sổ phát hiện | T09 (một phần), T10 |
| 24/09 | #4 | **đổi năm mốc 2024 → 2023** vì bản Atlas 2024 còn tạm | — |
| 25/09 | #5 | câu hỏi nghiên cứu; bảng màu đã kiểm mù màu + style guide | T01, T04 |
| 20/10 ¹ | #7 | bản LaTeX chương 9 + script render; kiểm cây HS92; treemap; sunburst; lưới 4 nước ASEAN ³ | T11, T12, T13, T14 |
| 20/10 | #8 | hai script 3D cho slide; **hàm định dạng số tiếng Việt**; file phân công bắt kịp thực tế | — |
| 20/10 | #9 | 13 chỗ in số trên 4 biểu đồ đầu đi qua hàm định dạng | tiền đề cho T22 |
| 20/10 | #10 | chỉ số mạng theo nước, trên **hai** đồ thị; phát hiện A7, A8, A9 | T18 |

¹ commit trải từ 22/09 đến 13/10 trên nhánh `huynguyenkhac17`, nhưng chỉ vào `main` khi gộp PR #7 ngày 20/10.
² PR #3 gom nhiều commit từ 23–24/09.
³ phần này do **Huy Nguyễn Khắc** làm (7 commit); 18 commit còn lại trên `main` đứng tên `Dr-Vphuc`.

**Nhánh `huyhihi`** (R3 — Dương Quang Huy) đến nay **0 commit**, mà R3 giữ T19, T20,
T21, T22, T24, T27 (ráp báo cáo) và T28 (slide). Nên hỏi trước tuần 5.

---

## 3. Số phải nhớ khi lên trình bày, và lệnh lấy lại

Tất cả đều là số **đã đo trên dữ liệu thật**, không trích từ bài báo nào. Nếu bị hỏi
"số này ở đâu ra" thì chạy lệnh ở cột cuối.

| Con số | Giá trị (2023) | Lấy lại bằng |
|---|---|---|
| Quy mô mạng | 231 nút · 27.535 cạnh | `data/processed/network_stats.csv` dòng 2023 |
| Mật độ · đối ứng | 0,5183 · 0,8368 | cùng file |
| Gini giá trị cạnh | 0,9569 | cùng file |
| Tổng xuất khẩu thế giới | 21,66 nghìn tỷ USD | cùng file, cột `total_export_value` |
| Xuất khẩu Việt Nam | 385,5390 tỷ USD = **75,3×** năm 1995 | `country_year.csv`, lọc `VNM` |
| Thị phần thế giới · hạng | 1,780% · **16**/231 | `metrics_top20.csv` dòng 16 |
| Bạn hàng xuất khẩu · hạng | 166 · **66**/231 | `metrics.csv`, `VNM`/`full`, cột `degree_out` |
| ECI · hạng | +0,579 · **78**/230 | cùng dòng, cột `eci`, `eci_rank` |
| 3 thị trường đầu | **52,41%** (Hoa Kỳ 95,2 · Trung Quốc 86,1 · Hàn Quốc 20,8 tỷ USD) | đếm trên `edges.csv` |
| 9 nước ASEAN còn lại | **7,77%** | đếm trên `edges.csv` |
| Mạng đã lọc (T10) | 73 nút · 416 cạnh · 67,84% giá trị | `threshold_coverage.csv` dòng `CHOSEN` |

Hai cái bẫy khi đọc bảng này:

- **Hạng có đồng hạng.** 166 bạn hàng là con số **ba nước cùng có**, nên khối đồng
  hạng chiếm chỗ 66–68; lấy 66 theo quy ước hạng cạnh tranh. Bản nháp T01 từng ghi
  "68/230" — sai hai lần: lấy số cuối khối, và lấy mẫu số của ECI áp cho cả ba dòng.
- **Mẫu số khác nhau từng dòng**: 231 nước có mặt trong mạng, nhưng chỉ 230 nước có
  ECI.

---

## 4. Bảy câu chắc chắn bị hỏi — câu trả lời đã có sẵn

Đây là **vật liệu cho T29**, chưa phải T29: T29 cần 10 câu và phải diễn tập thành tiếng.

**1. Dữ liệu đến 2024 mà sao lấy 2023?**
Vì bản Atlas 2024 còn tạm. Đếm số cạnh theo năm thì thấy ngay: 27.323 (2015) →
27.489 (2022) → 27.535 (2023) → **25.754 (2024)**, tụt 1.781 cặp nước. Riêng Việt Nam
rơi từ 166 xuống 129 bạn hàng. Một năm mà cả thế giới cùng mất bạn hàng thì đó là
dữ liệu chưa về đủ, không phải thương mại co lại. → A6, PR #4.

**2. Vì sao ngưỡng lọc là 0,046% chứ không phải số khác?**
Đã thử 21 phương án và lập bảng ngưỡng-vs-độ-phủ. Ngưỡng tuyệt đối làm **rụng thành
viên ASEAN** (từ 2,5 tỷ USD là mất Brunei, từ 5 tỷ mất cả Lào) — mà ASEAN là nửa đề
tài. Quy tắc đã chốt: 0,046% tổng xuất khẩu thế giới mỗi năm, **cộng** giữ top-3
luồng vào/ra cho mỗi nước ASEAN → 416 cạnh, giữ 67,84% giá trị, đủ 10/10 ASEAN ở
**mọi** năm. → `threshold_coverage.csv`, B4.

**3. Vì sao `metrics.csv` có hai dòng cho mỗi nước?**
Vì một đồ thị không trả lời được cả hai câu. Mật độ mạng đầy đủ là 0,518 — quá nửa
số cặp nước buôn trực tiếp — nên gần như không đường ngắn nhất nào phải vòng qua nước
thứ ba, và **betweenness bằng đúng 0 ở 172/231 nước**: nó không phân biệt được ai với
ai. Nên chỉ số cấu trúc tính trên mạng đã lọc (73 nút, đúng mạng T15–T17 sẽ vẽ), còn
tiền lấy từ mạng đầy đủ vì kim ngạch là đại lượng thật, không được phụ thuộc vào
ngưỡng ta tự chọn. → A7.

**4. Mạng lưới thương mại có scale-free không?**
**Không**, và đã kiểm chứ không đoán: độ lệch CCDF lớn nhất so với phân bố đều chỉ
0,056. Biểu đồ log-log của T09 sẽ **không ra đường thẳng** — đó là kết quả đúng, không
phải lỗi dữ liệu. Lý do dễ hiểu: mỗi nước chỉ có khoảng 230 đối tác khả dĩ, nên bậc bị
chặn trên, khác hẳn mạng web hay mạng trích dẫn. → A3.

**5. Thuật toán phát hiện cộng đồng có tìm ra ASEAN không?**
Không. Cả 10 nước ASEAN rơi vào **cùng một cụm** với Trung Quốc, Nhật, Hàn, Ấn và vùng
Vịnh. Phân hoạch này ổn định, không phải ngẫu nhiên: cố định `--seed 42` rồi chạy lại
20 hạt giống khác, năm 2023 không xê dịch chút nào (3 cụm, modularity 0,337, 100% số
cặp nước giữ nguyên quan hệ). Đo thẳng thì thấy vì sao: 7,77% hàng Việt Nam sang 9 nước
ASEAN còn lại, so với 52,41% sang ba thị trường đầu. **Hệ quả cho T15**: tô màu theo
cụm sẽ không làm ASEAN nổi lên, Việt Nam phải dựa vào viền đậm của quyết định B12.
→ A8.

**6. Vì sao đổi bảng màu giữa đồ án?**
Không phải vì thấy xấu. Bảng cũ **hỏng đo được**: `src/check_palette.py` chạy mô phỏng
ba kiểu mù màu và tính khoảng cách màu — có cặp ngành không phân biệt nổi. Bảng mới
qua được phép kiểm đó, và phép kiểm nằm trong repo để ai muốn chạy lại thì chạy.
→ `style-guide.md` §2.

**7. Số của Atlas có khớp với số Việt Nam công bố không?**
**Chưa đối chiếu được** — đó là T08, cần tài khoản CEPII và khóa API Comtrade mà chỉ
thành viên nhóm xin được. Phải nói thật trong phần Phương pháp luận, kèm các hạn chế
D1–D5. Nói trước thì là giới hạn đã nhận; để hội đồng phát hiện thì là lỗ hổng.

---

## 5. Việc còn lại, theo thứ tự nên làm

1. **T09 — biểu đồ log-log** (việc duy nhất đang dở). Dữ liệu đã có sẵn cột `ccdf`
   trong `degree_distribution.csv`. Nhớ: đường **không** thẳng, và phải ghi chú ngay
   trên hình rằng đó là kết quả, không phải lỗi.
2. **T15 node-link** — 416 cạnh, không mũi tên (B5), kích thước theo bậc và màu theo
   cụm lấy từ `metrics.csv` dòng `filtered`, viền đen 1,5px cho Việt Nam (B12).
3. **T16 hai ma trận kề** — hình vuông 6,30 × 6,30, `SEQUENTIAL_SCALE`, thứ tự cụm
   lấy cùng chỗ.
4. **T17 chord**, rồi **T19 Sankey**, **T20 small multiples theo thời gian**,
   **T21 streamgraph**.
5. **Hỏi R3** về T19–T21 trước khi tự làm hộ — nhánh `huyhihi` chưa có commit nào.
6. **T08** khi có tài khoản; **T25** viết sẵn được ngay vì hạn chế đã ghi đủ.

Hai quyết định còn treo:

- Có tải `hs92_country_product_year_4.csv` (452 MB, ~4,2 giờ) để có chi tiết HS4 không
  — hiện là hạn chế D4.
- `notebooks/Nhom8_Demo.ipynb` (chưa vào git) **trùng** phần treemap/sunburst của
  T12–T13; chỉ đoạn cone-tree 3D là riêng, mà cone-tree không có trong danh sách 30
  việc. Cần hỏi nhóm giữ hay bỏ.

Ba thứ **đã thấy, chưa xử lý** — ghi ra để khỏi quên, không phải việc gấp:

- **`.report/` nặng vô ích.** Sáu file PNG của chương 9 nằm **ba bản giống nhau**
  (`overleaf/img/`, `midterm/images/`, `midterm/assets/images/`), cộng
  `cover-image.jpg` **2,84 MB**. Dọn ở T30.
- **`cc_year.csv` 28,4 MB nằm vĩnh viễn trong lịch sử `main`.** PR #3 và #4 gộp bằng
  merge commit chứ không squash, nên commit đã gỡ file ra vẫn không xoá được blob.
  **Đã thống nhất để nguyên** — viết lại lịch sử một repo nhóm đang dùng thì lợi ít
  hại nhiều. Từ nay gộp bằng squash.
- **Phụ đề treemap đang giải thích loại biểu đồ** thay vì ghi năm / đơn vị / phạm vi,
  và có câu *"Bấm vào một ngành để xem..."* — một lời hướng dẫn tương tác in trên ảnh
  tĩnh. Vài nhãn lá cũng tụt dưới 7pt khi thu về khổ A4. Việc của **T22 và T24**.

---

## 6. Cách cập nhật sổ này

Mỗi lần gộp một PR, sửa đúng ba chỗ, mất khoảng hai phút:

1. Dòng **Cập nhật** ở đầu file: ngày, số việc Xong, commit `main`.
2. Một dòng mới trong bảng **§2**.
3. Ô trạng thái + ô "sản phẩm thật" trong bảng **§1**, khớp với cột *Trạng thái* của
   `phan-cong-cong-viec.xlsx` (sheet *Phân công chi tiết*, cột H).

Phát hiện mới thì **không** ghi vào đây — ghi vào `phat-hien-va-quyet-dinh.md` theo
số A tiếp theo, rồi ở đây chỉ trỏ sang. Sổ này giữ mỏng để còn đọc được một lượt.

---

## 7. Đợt 21/10/2026 — làm nốt phần còn lại của cả nhóm

Phúc và Dương Quang Huy đang bận việc khác, nên đợt này làm trọn các việc còn
treo. Ghi lại ở đây để hai bạn **không phải đọc code mới nắm được**.

### Việc đã xong

| Mã | Việc | Sản phẩm | Ghi chú quan trọng |
|---|---|---|---|
| T08 | Kiểm chất lượng dữ liệu | `src/compare_mirror.py` | **Đổi cách làm** — xem bên dưới |
| T09 | Phân bố bậc log-log | `output/degree_dist_out.*` | bác bỏ giả định scale-free |
| T15 | Node-link | `output/node_link_2023.*` | cụm mã hóa bằng xám + hình dạng |
| T16 | Hai ma trận kề | `output/adjacency_2023.*` | cùng 416 cạnh với T15 |
| T17 | Chord | `output/chord_2023.*` | dùng đồ thị ĐẦY ĐỦ, không lọc |
| T19 | Sankey | `output/sankey_vnm_2023.*` | giá trị gia tăng 13,9% |
| T20 | Vị trí VN theo thời gian | `output/time_multiples.*` | tiền tăng, cửa giảm |
| T21 | Streamgraph | `output/streamgraph_vnm_*.*` | hai bản: tỷ trọng và tuyệt đối |
| T25 | Phương pháp luận | `docs/phuong-phap-luan.md` | |
| T26 | Phát hiện | `docs/phat-hien.md` | 14 phát hiện F1–F14 |
| T27 | Trang web | `web/` + `src/build_web.py` | tĩnh, chạy được trên Pages |
| T29 | Câu phản biện | `docs/cau-hoi-phan-bien.md` | 12 câu + 3 câu phòng hờ |
| T30 | README | `README.md` | đã bổ sung 10 script mới |

Thêm một tài liệu không nằm trong danh sách task:
**`docs/ket-luan-cho-thuyet-trinh.md`** — mở file này trước khi lên trình bày.
Nó gom mọi con số theo từng người, kèm cách nói và các chỗ dễ nói quá lời.

### Ba thay đổi về cách làm, cần cả nhóm biết

**1. T08 đổi hướng, và đó là một phát hiện.** Phân công ghi "đối chiếu Atlas với
BACI và Comtrade". Ba nguồn đó **không độc lập** — Atlas và BACI đều dẫn xuất từ
Comtrade. Thay bằng phép **chênh lệch gương** ngay trong dữ liệu sẵn có. Kết
quả: **2.093/2.093 luồng trùng khít 100,0%**, tức Atlas đã hòa giải số liệu
trước khi phát hành, nên ta **không tự đo được sai số của nó**. Nói ra điều này
trung thực hơn là trình bày một bảng ba cột số giống nhau.

**2. Cộng đồng KHÔNG được tô màu.** Đã đo 7 bảng 3 màu ứng viên; bảng nào cũng
tụt xuống ΔE 2,6–6,6 so với màu ngành gần nhất khi mô phỏng mù màu. Bảng 10
ngành đã chiếm hết gam an toàn. Dùng **3 nấc xám + 3 hình dạng**, giữ ΔE 20,1 ở
cả ba dạng mù màu. Hằng số ở `reference_data.py`, mục `COMMUNITY_FILL`.

**3. Ba hình mạng lưới dùng ba tập cạnh khác nhau, có chủ ý.** T15 và T16 dùng
đồ thị đã lọc (416 cạnh) vì phải so được với nhau. T17 và T20 dùng đồ thị đầy
đủ — chord đã gộp thành 10 khối nên không cần lọc, còn T20 thì câu hỏi chính là
*đếm bạn hàng*, mà ngưỡng lại cắt đúng cái đuôi cần đếm. Khác biệt này ghi trên
chú thích từng hình.

### Hai lỗi đã mắc và đã sửa — để không ai lặp lại

**Ngưỡng tuyệt đối thiên vị nước lớn.** Bản đầu của chord áp ngưỡng 0,15% tổng
thế giới cho mọi dải, và **xóa mất 4 trong 8 luồng của Việt Nam** — vì Việt Nam
chỉ chiếm 1,8% xuất khẩu thế giới nên luồng "rất lớn với Việt Nam" vẫn "nhỏ với
thế giới". Một hình tên là "lấy Việt Nam làm trọng tâm" lại giấu phần lớn luồng
của Việt Nam. Đã sửa: dải có Việt Nam thì miễn ngưỡng. Đây đúng là cái bẫy mà
phát hiện A5 đã ghi, gặp lại ở một chỗ khác.

**Mẫu số sai trong chú thích chord.** Tổng độ dài cung đếm mỗi luồng hai lần
(một lần phía xuất, một lần phía nhập), nên chú thích ghi "34,9 nghìn tỷ USD
thương mại" trong khi tổng thật là 21,7. Đúng để chia cung, sai để làm mẫu số
cho thị phần. Đã tách hai biến ra.

### Dữ liệu: đã đủ

`check_raw_data.py` báo **DAT**. Hai file từng thiếu (`cc_year.csv`,
`hs92_country_year.csv`) đã tải về. Ba file đối chiếu chéo khớp 0,000%.
`data/processed/` có đủ 10 file.

### Còn lại cho cả nhóm

- **T22 (đồng bộ thị giác)** — 10 biểu đồ đều đã dùng `reference_data.py`, dấu
  thập phân tiếng Việt và viền trắng theo style guide. Còn việc rà lại bằng mắt
  trên máy chiếu thật.
- **T23 (rà soát chéo)** — **không tự làm được**, theo đúng nguyên tắc #4: không
  ai tự duyệt sản phẩm của chính mình. Phúc và Dương Quang Huy cần review.
- **T24 (kiểm khả năng đọc)** — `check_palette.py` thoát 0. Còn việc kiểm nhãn
  chồng nhau ở khổ chiếu thật.
- **T28 (slide)** — mỗi người tự làm phần mình, lấy số từ
  `docs/ket-luan-cho-thuyet-trinh.md`.

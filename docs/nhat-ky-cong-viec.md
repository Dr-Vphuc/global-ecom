# Nhật ký công việc — đã làm gì, nằm ở đâu, và vì sao

**Cập nhật 21/10/2026** · 17/30 việc Xong · `main` ở commit `fdc1798` (gộp PR #13)

Sổ này chỉ trả lời **một câu: "đã làm được gì rồi"**. Khi cần soạn slide, viết phần
Phương pháp luận, hay trả lời phản biện thì mở sổ này ra trước, nó dẫn sang chỗ cần.

| Cần gì | Mở file nào |
|---|---|
| Đã làm gì, ai làm, nằm ở file nào | **sổ này** |
| Tìm ra điều gì (A1–A11), chốt điều gì (B1–B17) | `docs/phat-hien-va-quyet-dinh.md` |
| Luật của repo — chạy sao, commit sao, hình thế nào là xong | `CLAUDE.md` |
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

### Giai đoạn 2 — Dữ liệu (5/6 Xong)

| Mã | Việc | Trạng thái | Sản phẩm thật |
|---|---|---|---|
| T06 | Tải Atlas từ Harvard Dataverse | Xong | `src/download_atlas.py` (dữ liệu thô **không** vào git) |
| T07 | Làm sạch, xuất file trung gian, gắn vùng địa lý | Xong | `src/build_intermediate.py` → `nodes/edges/tree/country_product/country_year.csv` |
| T08 | Đối chiếu Atlas với BACI và Comtrade | **Chưa** | *cần tài khoản CEPII + khóa API Comtrade — chỉ thành viên nhóm làm được* |
| T09 | Thống kê mô tả mạng lưới theo từng năm | Xong | `network_stats.csv` (30 năm) + `src/make_degree_loglog.py` → `output/degree_loglog_2023.*` (và `_1995.*`) |
| T10 | Chốt ngưỡng lọc cạnh, biện minh bằng số | Xong | `threshold_coverage.csv`, quy tắc ở README §"Quy tắc lọc cạnh" |
| T11 | Kiểm chất lượng cây HS92 4 tầng | Xong | `src/check_tree.py` |

### Giai đoạn 3 — Trực quan hóa (7/10 Xong)

| Mã | Việc | Trạng thái | Sản phẩm thật |
|---|---|---|---|
| T12 | Treemap cơ cấu xuất khẩu VN, 2 mốc | Xong | `src/make_hierarchy_charts.py --year 1995\|2023` → `output/treemap_vnm_1995.*`, `_2023.*` |
| T13 | Sunburst 4 tầng cây sản phẩm | Xong | cùng script → `output/sunburst_vnm_1995.*`, `_2023.*` |
| T14 | Small multiples so VN với Thái–Mã–Indo | Xong | `src/make_small_multiples.py` → `output/small_multiples_vnm-tha-mys-idn_2023.*` |
| T15 | Node-link mạng đã lọc, mã hóa bậc + cộng đồng | Xong | `src/make_node_link.py` → `output/node_link_2023.*` · bảng màu cụm mới ở `reference_data.py`, kiểm bằng `check_palette.py` |
| T16 | Hai ma trận kề, một theo alphabet một theo cụm | Xong | `src/make_adjacency_matrix.py --year 2023\|1995` → `output/adjacency_alpha_*.{html,png}`, `adjacency_cluster_*.*` · phát hiện **A10**, quyết định **B15**, **B16** |
| T17 | Chord diagram giữa các khối, VN làm trọng tâm | Xong | `src/make_chord.py --year 2023\|1995` → `output/chord_bloc_*.{html,png}` · 8 khối suy từ `nodes.csv` · phát hiện **A11**, quyết định **B17** |
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
| 20/10 | #11 | **sổ nhật ký công việc** (chính sổ này); README chỉ đường sang nó | — |
| 21/10 | #12 | biểu đồ log-log phân bố bậc + ba con số bác giả thuyết scale-free; A3 thêm mức lệch 1995 | T09 |
| 21/10 | #13 | node-link mạng đã lọc (271 cặp nước); **bảng màu cụm riêng** đã qua kiểm mù màu; B13, B14 | T15 |
| 21/10 | #14 | `CLAUDE.md` + skill `/viec-tiep`: mọi context mới tự biết luật repo và chuẩn "hình thế nào là xong" | — |

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
| Mạng đã lọc (T10) | 73 nút · 416 cạnh (= **271 cặp nước**) · 67,84% giá trị | `threshold_coverage.csv` dòng `CHOSEN` |
| Việt Nam trên đồ thị đã lọc | **12 cặp**, dày nhất là Trung Quốc **219,2 tỷ USD** (gấp 2,3 lần Hoa Kỳ) | `python src/make_node_link.py` (in ra cuối) |
| Bác giả thuyết scale-free | R² **0,51** · lệch tới **41,3 lần** | `python src/make_degree_loglog.py` (in ra cuối) |
| Lệch khỏi phân bố đều | **0,056** (năm 1995 còn 0,180) | cùng lệnh, chạy thêm `--year 1995` |
| Giá trị nằm trong khối cụm | **69,7%** (năm 1995 còn là **83,8%**) | `python src/make_adjacency_matrix.py --year 2023\|1995` (khối kiểm chứng) |
| Xếp lại hàng/cột theo cụm | khoảng cách tới đường chéo **0,398 → 0,258**, giảm **35,1%** (ngẫu nhiên 0,341) | cùng lệnh |
| Ba khối năm 2023 · năm 1995 | **41 / 25 / 7** quanh Trung Quốc, Đức, Hoa Kỳ · **34 / 27 / 2** quanh **Hoa Kỳ**, Đức, Brazil | cùng lệnh, mục "Các khối" |
| Hàng/cột Việt Nam trên ma trận | **8 ô xuất + 10 ô nhập** (năm 1995: **3 + 3**) | cùng lệnh, dòng cuối |
| Bạn hàng lớn thứ hai của Việt Nam | **ASEAN 33,4%** năm 1995 → **châu Mỹ 18,5%** năm 2023; ASEAN tụt còn 8,4% | `python src/make_chord.py --year 1995` và `--year 2023` |
| Đông Á trong rổ của Việt Nam | 59,1% → **70,9%** | cùng lệnh, mục "Việt Nam nối với" |
| Thương mại nội khối (8 khối địa lý) | 60,5% → **48,4%** | cùng lệnh, dòng "Nội khối" |
| Còn chỗ cho bảng màu thứ ba không | **không** — màu thứ ba chỉ cách ΔE **14,2**, dưới sàn 15 | `python src/probe_colour_space.py` |

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
**Không**, và đã kiểm chứ không đoán. Biểu đồ log-log của T09
(`output/degree_loglog_2023.png`) **không ra đường thẳng**, và hình tự mang bằng chứng
đi kèm: đường thẳng khớp nhất chỉ đạt **R² = 0,51**, có chỗ lệch **41,3 lần**, và nếu
kéo về phía bậc thấp nó đòi CCDF vượt 100% — vô nghĩa, vì CCDF là tỉ lệ. Ngược lại,
CCDF thật chỉ lệch **0,056** khỏi một phân bố **đều**. Lý do dễ hiểu: mỗi nước chỉ có
khoảng 230 đối tác khả dĩ, nên bậc bị chặn trên, khác hẳn mạng web hay mạng trích dẫn.
Nếu bị hỏi tiếp "thế 1995 thì sao": lệch 0,180 — **mạng không chỉ dày thêm mà còn đều
ra**, trong khi Gini giá trị cạnh đứng yên. → A3.

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

1. **Hỏi R3 trước đã** — T19, T20, T21, T22, T24 đều của R3 mà nhánh `huyhihi`
   vẫn 0 commit. Trong đó **T22 đang giữ phần sửa lỗi đơn vị B16** cho năm hình
   cũ (T09, T12–T15): chữ in thật của chúng đang nhỏ hơn khai báo 2,78 lần, dòng
   nguồn ra ~2,5pt. Không chốt được ai làm T22 thì năm hình đó in ra sai sàn 7pt.
2. **T19 Sankey** nhập → VN → xuất. Chiều của luồng đã cố ý để dành cho việc này:
   T15 và T17 đều gộp hai chiều theo **B13**, nên Sankey là chỗ duy nhất trả lời
   giả thuyết trung chuyển. Số nền đã có sẵn ở **A11**.
3. Rồi **T20 small multiples theo thời gian**, **T21 streamgraph**.
4. **T08** khi có tài khoản; **T25** viết sẵn được ngay vì hạn chế đã ghi đủ.
5. **T22** phải sửa lỗi đơn vị point/pixel ghi ở **B16** cho T09 và T12–T15 —
   hiện cỡ chữ in thật của chúng nhỏ hơn khai báo khoảng 2,8 lần.

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

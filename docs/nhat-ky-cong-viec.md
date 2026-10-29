# Nhật ký công việc — đã làm gì, nằm ở đâu, và vì sao

**Cập nhật 30/10/2026** · 28/31 việc Xong (tính cả T28 của PR #19, gộp cùng lần sửa xung đột) · `main` ở commit `4a12ac9` (gộp PR #25)

Sổ này chỉ trả lời **một câu: "đã làm được gì rồi"**. Khi cần soạn slide, viết phần
Phương pháp luận, hay trả lời phản biện thì mở sổ này ra trước, nó dẫn sang chỗ cần.

| Cần gì | Mở file nào |
|---|---|
| Đã làm gì, ai làm, nằm ở file nào | **sổ này** |
| Tìm ra điều gì (A1–A19), chốt điều gì (B1–B28) | `docs/phat-hien-va-quyet-dinh.md` |
| **Mạch thuyết trình — năm nhịp, kết bằng đề xuất** | `docs/phat-hien-va-quyet-dinh.md` §E |
| Các mục của báo cáo cuối đã viết | `.report/final/` — một file một mục (**B21**) |
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
> Câu trả lời tìm được, nói bằng một cặp số: xuất khẩu **gấp 75 lần** từ 1995 đến
> 2023, nhưng **tiền dồn lại vào ít cửa** — 3 thị trường đầu (Hoa Kỳ, Trung Quốc,
> Hàn Quốc) nhận **52,41%** hàng xuất, so với **39,25%** năm 2013, còn 9 nước ASEAN
> còn lại cộng lại chỉ **7,77%**. Đo bằng HHI thì rõ hình chữ V: đáy **0,0662**
> (2013) → **0,1226** (2023), **cao hơn cả mức 1995**.
>
> ⚠️ Chỗ này đã **sửa phép đo** ngày 22/10/2026. Câu cũ dựa vào "số bạn hàng giảm
> từ 181 xuống 166" — số đúng, nhưng **A16** đo được rằng phép đếm bạn hàng không
> bền: 47 nước rời khỏi danh sách giữa 2002 và 2023 chỉ mang theo **0,59%** kim
> ngạch, và ở mức sàn 100 triệu USD thì số kênh lại **tăng** 68 → 83. Dùng câu tập
> trung giá trị, đừng dùng câu số đếm.
>
> Nên "hội nhập sâu" và "phụ thuộc hẹp" ở đây là **cùng một hiện tượng**, và đó là
> điều các biểu đồ phải cho người xem thấy.

Ba con số đỡ cho câu đó: xuất khẩu Việt Nam **hạng 16/231** về giá trị, nhưng
**hạng 78/230** về chỉ số phức tạp kinh tế (ECI +0,579) và **hạng 30/97** về mức
tập trung giá trị trong nhóm nước xuất trên 10 tỷ USD. Bán nhiều, bán thứ không
khó làm, và dồn tiền vào ít cửa. *(Dòng này trước ghi "hạng 66/231 về số bạn
hàng" — đã bỏ theo A16, vì đó là phép đo không bền.)*

**Và đồ án không dừng ở mô tả.** Kết bằng một đề xuất: dồn ưu tiên vào **thiết bị
quang học – đo lường – y tế** (RCA 0,905; PCI +0,934) và **máy móc công nghiệp**
(0,954; +0,783) — hai nhóm khó nhất trong rổ mà Việt Nam đã có chỗ đứng — thay vì
đào sâu thêm vào lắp ráp điện tử. Đề xuất ấy do một **quy tắc viết trong code**
chọn ra, và quy tắc đó chạy lại ở 2007 thì chỉ đúng vào điện tử trước đợt bùng
nổ, chạy ở 2015 thì sắt thép tám năm sau chạm RCA 1,00 (A14, A17).

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

### Giai đoạn 2 — Dữ liệu (6/6 Xong)

| Mã | Việc | Trạng thái | Sản phẩm thật |
|---|---|---|---|
| T06 | Tải Atlas từ Harvard Dataverse | Xong | `src/download_atlas.py` (dữ liệu thô **không** vào git) |
| T07 | Làm sạch, xuất file trung gian, gắn vùng địa lý | Xong | `src/build_intermediate.py` → `nodes/edges/tree/country_product/country_year.csv` |
| T08 | Đối chiếu Atlas với BACI và Comtrade | Xong | **đổi hướng**: BACI/Comtrade cùng gốc với Atlas nên không phải phép kiểm độc lập (B9); thay bằng chênh lệch gương `src/compare_mirror.py` → `mirror_gap_2023.csv` · 2.093/2.093 luồng ≥ 1 tỷ USD trùng khít (và 27.534/27.534 khi bỏ ngưỡng; cả 30 năm) · phát hiện **A18**, một đoạn ở §2.2 báo cáo |
| T09 | Thống kê mô tả mạng lưới theo từng năm | Xong | `network_stats.csv` (30 năm) + `src/make_degree_loglog.py` → `output/degree_loglog_2023.*` (và `_1995.*`) |
| T10 | Chốt ngưỡng lọc cạnh, biện minh bằng số | Xong | `threshold_coverage.csv`, quy tắc ở README §"Quy tắc lọc cạnh" |
| T11 | Kiểm chất lượng cây HS92 4 tầng | Xong | `src/check_tree.py` |

### Giai đoạn 3 — Trực quan hóa (11/11 Xong)

| Mã | Việc | Trạng thái | Sản phẩm thật |
|---|---|---|---|
| T12 | Treemap cơ cấu xuất khẩu VN, 2 mốc | Xong | `src/make_hierarchy_charts.py --year 1995\|2023` → `output/treemap_vnm_1995.*`, `_2023.*` |
| T13 | Sunburst 4 tầng cây sản phẩm | Xong | cùng script → `output/sunburst_vnm_1995.*`, `_2023.*` |
| T14 | Small multiples so VN với Thái–Mã–Indo | Xong | `src/make_small_multiples.py` → `output/small_multiples_vnm-tha-mys-idn_2023.*` |
| T15 | Node-link mạng đã lọc, mã hóa bậc + cộng đồng | Xong | `src/make_node_link.py` → `output/node_link_2023.*` · bảng màu cụm mới ở `reference_data.py`, kiểm bằng `check_palette.py` |
| T16 | Hai ma trận kề, một theo alphabet một theo cụm | Xong | `src/make_adjacency_matrix.py --year 2023\|1995` → `output/adjacency_alpha_*.{html,png}`, `adjacency_cluster_*.*` · phát hiện **A10**, quyết định **B15**, **B16** |
| T17 | Chord diagram giữa các khối, VN làm trọng tâm | Xong | `src/make_chord.py --year 2023\|1995` → `output/chord_bloc_*.{html,png}` · 8 khối suy từ `nodes.csv` · phát hiện **A11**, quyết định **B17** |
| T18 | Chỉ số mạng: bậc, độ mạnh, betweenness, cộng đồng | Xong | `src/compute_metrics.py` → `metrics.csv` (304 dòng), `metrics_top20.csv` |
| T19 | Sankey nhập → VN → xuất (kiểm giả thuyết trung chuyển) | Xong | `src/make_sankey.py` → `sankey_vietnam_{1995,2023}` · phát hiện **A12** |
| T20 | Small multiples theo thời gian 1995·2005·2015·2023 | Xong | `src/make_time_multiples.py` → `time_multiples_{xuat,nhap}` · **A13** sửa lại A9 |
| T21 | Streamgraph 10 ngành, 1995–2023 | Xong | `src/make_streamgraph.py` → `stream_sectors_1995_2023` · hai tầng, không dùng nền lượn |
| **T31** | **Mặt phẳng quyết định RCA × PCI — hình mang ĐỀ XUẤT** | Xong | `src/make_decision_plane.py` → `decision_plane_{2015,2023}` · phát hiện **A14**, quyết định **B18** |

### Giai đoạn 4 — Tích hợp (4/5) · Giai đoạn 5 — Hoàn thiện (2/4)

| Mã | Việc | Trạng thái | Ghi chú đã có sẵn cho việc đó |
|---|---|---|---|
| T22 | Áp hệ thống thị giác lên toàn bộ biểu đồ 3 người | Xong | *(T28 sửa thêm phụ đề treemap và sunburst: bỏ câu hướng dẫn bấm chuột in trên ảnh tĩnh — **B25**)* · sửa lỗi đơn vị **B16** cho T09, T12–T15 và bố cục lại cả năm; `R.xuat_png` là chỗ duy nhất định nghĩa phép xuất (**B19**) |
| T23 | Rà soát chéo, mỗi người review 2 hình của người khác | Đang làm | đã sửa lỗi đã biết: phụ đề treemap/sunburst giờ ghi tổng giá trị + phạm vi, bỏ lời *"Bấm vào…"*; còn phần review chéo — checklist ở `style-guide.md` §7 |
| T24 | Kiểm khả năng đọc: nhãn, chú giải, tương phản, mù màu | Xong | `src/check_readability.py` — 5 phép kiểm, chạy được trong CI, hiện **ĐẠT** |
| T25 | Viết phần Phương pháp luận | Xong | `.report/final/02-phuong-phap-luan.md` — 12 mục (T27 chuyển 5 mục sang phụ lục), mỗi số kèm lệnh lấy lại · phát hiện **A15** (đồ thị lọc đổi dấu cán cân), quyết định **B21**, **B22** |
| T26 | Viết phần Phát hiện | Xong | 9 mục, T27 tách thành bốn hồi `03-quy-mo` … `06-y-nghia` · phát hiện **A16** (phép đếm bạn hàng không bền), sửa **A13** và **A4**, sửa tiêu đề T20 |
| T27 | Ráp báo cáo cuối theo mạch 5 nhịp | Xong | 10 file mục trong `.report/final/` + `src/build_report.py` → `output/bao-cao-cuoi.{md,html}`; viết mới **Tóm tắt, Mở đầu, Quy mô, Đề xuất, Kết luận**; chốt số hiệu mục (**B23**); phát hiện **A17** · sau PR #24–#25: thêm §6.2 (phần giá trị làm ra trong nước), sửa §7.3–§7.5 — **A19**, **B27**, **B28** |
| T28 | Slide thuyết trình | Xong | `src/build_slides.py` → `output/slide-thuyet-trinh.{html,md}` — 17 slide chính + 3 dự phòng theo đúng năm nhịp §E; mọi số do script đo lại và **đối chiếu với báo cáo cuối** (**B24**), phép đối chiếu bắt được một con số sai ở A17 · một dòng ở slide 11 đã đổi theo **B28**; chưa có slide riêng cho TiVA |
| T29 | Diễn tập + 10 câu phản biện | Đang làm | §4 sổ này đủ **10** câu kèm câu trả lời (câu 10: ECI đo hàng đi qua hay ở lại); còn diễn tập thành tiếng |
| T30 | Dọn repo, README tái lập được | Đang làm | đã chạy lại 18 lệnh vẽ/kiểm/ráp trong README từ `data/processed/`, cả 18 thoát 0; còn dọn bản ảnh trùng trong `.report/` |

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
| 22/10 | #15 | **toàn bộ phần R3**: T19 Sankey, T20 small multiples, T21 dòng chảy, T22 sửa lỗi đơn vị cho 5 hình cũ, T24 kiểm khả năng đọc, **T31 hình mang đề xuất**; A12–A14, B18–B20, §E viết lại | T19–T22, T24, T31 |
| 22/10 | #16 | **phần Phương pháp luận** của báo cáo cuối (12 mục); A15 — dùng đồ thị đã lọc cho Sankey sẽ đổi dấu cán cân; B21, B22 | T25 |
| 22/10 | #17 | **phần Phát hiện** của báo cáo cuối (9 mục); **A16 — phép đếm bạn hàng không bền, thay bằng tập trung giá trị (HHI)**; sửa A13 (đỉnh thật 2002/208) và A4 (67,84% chứ không phải 68,50%); sửa tiêu đề hình T20 vì nó in một câu sai | T26 |
| 22/10 | #18 | **báo cáo cuối đã ráp xong** — 10 mục trong `.report/final/` + `src/build_report.py` tự kiểm tham chiếu chéo (19 trang thân + 3 trang phụ lục, 14 hình, 0 tham chiếu treo); chốt số hiệu mục (**B23**); **A17 — RCA không tự đi lên**, quy tắc chọn chạy ở 2007 chỉ ra điện tử khi RCA mới 0,573; sửa 75,4× → 75,3× | T27 |
| 29/10 | #20 | nhánh `huynguyenkhac17` đồng bộ với `main` (bản song song cũ bỏ, lấy bản `main`); **T08 đổi hướng sang chênh lệch gương** — `src/compare_mirror.py`, **A18**: hai bản khai trùng khít ở mọi luồng, mọi năm, nên không tự đo được sai số (ai hoà giải thì dữ liệu không nói); phụ đề treemap/sunburst bỏ lời *"Bấm vào…"*; câu phản biện thứ 10; pipeline chạy lại trọn vẹn | T08 · một phần T23, T29, T30 |
| 30/10 | #24 | **đo được phần giá trị làm ra trong nước** bằng OECD TiVA 2025: `src/map_sector_isic.py` + bảng ghép 97 dòng HS2 → ISIC (`data/reference/hs2_to_isic4.csv`); điện tử giữ 44,2%, bình quân rổ 50,5%; **A19**, **B27**; viết lại hạn chế D2, D5 từ "không đo được" thành "đo ở mức ngành, 2022" | — |
| 30/10 | #25 | **dựng lại lập luận quanh phần ở lại**: §6.2 mới trong báo cáo, §7.3 đổi lý do (không còn "điện tử phụ thuộc nhập khẩu nhất"), thêm mốc kiểm và điều kiện đổi ý thứ tư; đề xuất HS90 + HS84 giữ nguyên; **B28** | T27 |

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
| Hai bản khai của một luồng | **2.093/2.093** luồng ≥ 1 tỷ USD trùng khít, đối xứng tuyệt đối → không tự đo được sai số (ai hoà giải: dữ liệu không nói) | `src/compare_mirror.py` (A18) |
| Gini giá trị cạnh | 0,9569 | cùng file |
| Tổng xuất khẩu thế giới | 21,66 nghìn tỷ USD | cùng file, cột `total_export_value` |
| Xuất khẩu Việt Nam | 385,5390 tỷ USD = **75,3×** năm 1995 | `country_year.csv`, lọc `VNM` |
| Mua của Trung Quốc · bán lại | 133,05 tỷ · 86,11 tỷ → **−46,94 tỷ** | `src/make_sankey.py` |
| Mua của Hoa Kỳ · bán sang | 9,83 tỷ · 95,16 tỷ → **+85,33 tỷ** | cùng lệnh |
| Hàng vào từ Đông Á | **68,3%** | cùng lệnh |
| Tập trung đầu ra (HHI) | đáy **0,0662** (2013) → **0,1226** (2023), cao hơn mức 1995 (0,1209) | `src/make_time_multiples.py` (khối A16) |
| Tập trung đầu vào (HHI) | **0,1979** — gấp 1,6 lần đầu ra; top-3 nhà cung cấp **61,3%** | cùng lệnh, `--direction nhap` |
| Hạng tập trung so với thế giới | **30/97** nước xuất trên 10 tỷ USD (2015 còn **dưới** trung vị) | đếm trên `edges.csv` |
| Số bạn hàng xuất — ⚠️ phép đo KHÔNG bền | 98 → **208 (đỉnh 2002)** → 181 → **166**; nhưng trên 100 triệu USD thì **13 → 83** | `src/make_time_multiples.py` (khối A16) |
| Thế giới lớn lên bao nhiêu | **4,51×** (4.803,3 → 21.656,9 tỷ USD) — Việt Nam nhanh hơn **16,7 lần** | `src/analyze_network.py` · `edges.csv` |
| Hạng xuất khẩu của Việt Nam | **61/211** (1995) → **16/230** (2023); nhiều nhất ASEAN, trên Malaysia 353,9 và Singapore 346,6 tỷ | đếm trên `edges.csv` |
| RCA có tự đi lên không — nền so sánh | **không**: chỉ **45,4%** trong 97 nhóm tăng 2015→2023, trung vị **−0,0178**; riêng PCI > 0 thì 62,8% | `country_product.csv` (A17) |
| Quy tắc chọn chạy ở năm 2007 | chỉ ra **điện tử** khi RCA mới 0,573 và xuất 3,4 tỷ → 2023 là 2,230 và **115,4 tỷ USD** | `src/make_decision_plane.py --year 2007 --since 1999` |
| Nền so sánh cửa sổ trước (2007→2015) | **37,1%** trong 97 nhóm có RCA tăng, trung vị −0,0465 — lớp thoả trọn quy tắc ở cửa sổ đó còn kém hơn: 25,0% trên 12 nhóm | `country_product.csv` (A17) |
| Điện tử trong rổ hàng | 0,6% (1995) → **29,9%** (2023) | `src/make_streamgraph.py` |
| Nông sản trong rổ hàng | 42,9% → 11,6% | cùng lệnh |
| Máy móc công nghiệp RCA | 0,46 (2015) → **0,95** (2023), PCI +0,78 | `src/make_decision_plane.py` |
| Thiết bị quang học, y tế RCA | 0,75 → **0,91**, PCI **+0,93** | cùng lệnh |
| Rổ hàng còn kẹt ở góc "hàng dễ" | **36,2%** (2015 là 44,7%) | cùng lệnh |
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
| Nếu Sankey dùng đồ thị đã lọc | cán cân **đổi dấu**: +53,45 tỷ (thặng dư) → **−15,17 tỷ** (thâm hụt); 166→8 nước bán ra, 149→10 nước mua vào | `src/make_sankey.py` + lọc `edges.csv` theo `above_threshold` |
| Ô `Chưa phân loại` trong rổ hàng | **11,83%** = 45,60 tỷ USD, RCA 2,4408, PCI −1,206 — là mã `XXXX` của Atlas, đã loại khỏi đề xuất | `src/make_decision_plane.py` · `src/check_tree.py` |
| Cây HS92 kiểm ra sạch không | **31 mục: 29 ĐẠT, 1 lỗi, 1 lưu ý** — `3501` nằm dưới `34` thay vì `35`, cùng ngành 6 nên không hình nào lệch | `python src/check_tree.py` |

Hai cái bẫy khi đọc bảng này:

- **Hạng có đồng hạng.** 166 bạn hàng là con số **ba nước cùng có**, nên khối đồng
  hạng chiếm chỗ 66–68; lấy 66 theo quy ước hạng cạnh tranh. Bản nháp T01 từng ghi
  "68/230" — sai hai lần: lấy số cuối khối, và lấy mẫu số của ECI áp cho cả ba dòng.
- **Mẫu số khác nhau từng dòng**: 231 nước có mặt trong mạng, nhưng chỉ 230 nước có
  ECI.

---

## 4. Mười câu chắc chắn bị hỏi — câu trả lời đã có sẵn

Đây là **vật liệu cho T29**: đã đủ 10 câu, còn phải diễn tập thành tiếng.

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
**Với một nguồn độc lập thì chưa đối chiếu được** — BACI và Comtrade cần tài khoản
CEPII và khóa API, mà kể cả có thì cả hai cùng gốc Comtrade với Atlas, nên không
phải phép kiểm độc lập (B9). Cái đã đo được là **chênh lệch gương** ngay trong Atlas:
mỗi luồng A→B có hai bản khai, của hải quan A và của hải quan B. Với 2.093 luồng
trên 1 tỷ USD năm 2023, hai bản khai **trùng khít ở cả 2.093 luồng** (và ở mọi
luồng, mọi năm) — đối xứng tuyệt đối, nên bộ dữ liệu này không cho tự đo sai số của
nó; ai hoà giải thì dữ liệu không nói. Phải nói đúng chừng đó, kèm các hạn chế D1–D5. → A18, `src/compare_mirror.py`.

**8. Việt Nam có đang mất bạn hàng không?**
**Không, và chính nhóm đã bác câu đó của chính mình.** Đếm thô thì số bạn hàng rơi từ
đỉnh **208 nước (2002)** xuống **166 (2023)**. Nhưng 47 nước rời khỏi danh sách mang
theo đúng **0,59%** kim ngạch — trung vị một luồng xuất khẩu đi từ **1,0 triệu USD**
(2002) lên **103,6 triệu USD** (2023), nên danh sách ngắn đi vì các luồng tí hon biến
mất. Đặt một mức sàn vào là kết luận đảo chiều: trên **100 triệu USD** thì số kênh
**tăng 13 → 83**, và hạng thế giới của Việt Nam theo số bạn hàng trên 10 triệu USD đi
từ 65/211 lên **24/231**. Điều thật sự xảy ra là **tiền dồn lại**, không phải cửa
đóng lại: HHI đáy 0,0662 (2013) → **0,1226** (2023), top-3 nhận **52,41%**. → A16,
và tiêu đề T20 đã sửa theo.

**9. RCA của hai nhóm được đề xuất còn dưới 1 — lấy gì chắc nó vượt?**
**Không chắc, và báo cáo nói đúng như vậy — nhưng có nền so sánh.** Thứ nhất, quy
tắc chọn đã chạy trên hai năm quá khứ và cả hai lần đều chỉ đúng chỗ: chạy ở 2007
nó chọn **điện tử** khi nhóm đó mới xuất 3,4 tỷ USD với RCA 0,573 (2023: 2,230 và
115,4 tỷ); chạy ở 2015 nó chọn thiết bị quang học và sắt thép, và **sắt thép đã
chạm RCA 1,003**. Thứ hai, RCA **không tự đi lên**: trong 97 nhóm hàng chỉ 45,4%
tăng giữa 2015 và 2023, trung vị **−0,0178**, còn nhóm đã có RCA ≥ 1,5 thì chỉ 25%
tăng tiếp. Thứ ba — và phải nói thẳng — điều kiện mang sức dự báo là **PCI > 0**
(62,8% số nhóm tăng, so với 31,5% ở hàng dễ), chứ không phải dải RCA 0,5–1,5; còn
lớp thoả trọn quy tắc thì chỉ 6 nhóm, quá nhỏ để kết luận thống kê. → A17, §7.2.

**10. ECI của Việt Nam đo hàng đi qua hay hàng ở lại?**
**Hàng đi qua — và báo cáo nói điều đó trước khi bị hỏi.** ECI, PCI và RCA đều tính
trên **xuất khẩu gộp**: một nước lắp ráp điện thoại được cộng trọn độ phức tạp của
chiếc điện thoại, bất kể giữ lại bao nhiêu giá trị. Đường ECI đi từ **−1,00 (#181/211,
1995)** lên **+0,58 (#78/230, 2023)** một phần đến từ 115,4 tỷ USD điện tử. Sankey
(T19) cho thấy dấu hiệu hành lang — mua của Trung Quốc 133,05 tỷ, bán cho Hoa Kỳ
95,16 tỷ — nhưng phần nhạt trên thanh Việt Nam là *xuất trừ nhập*, **không** phải
giá trị tăng thêm trong nước. Atlas không có bảng vào–ra, nên nhóm lấy thêm OECD
TiVA 2025: điện tử giữ **44,2%** giá trị trong nước (2022), bình quân hàng hóa ghép
được 50,5%, và hàng càng phức tạp thì tỷ lệ càng thấp (ρ = −0,47). Vì vậy câu kết
luận đúng là: *chỉ số đo sự tiến bộ này có một điểm mù, và ta đã đo được cỡ của nó
ở mức ngành* — không phải "Việt Nam chỉ lắp ráp" (44% vẫn làm ra ở đây), cũng không
phải "Việt Nam đã làm chủ công nghệ" (56% là linh kiện nhập về). → A2, A12, A19, D2, D5, §2.4.

---

## 5. Việc còn lại, theo thứ tự nên làm

Toàn bộ phần hình đã xong, **báo cáo cuối đã ráp xong** (10 mục trong
`.report/final/` → `output/bao-cao-cuoi.{md,html}`, 19 trang thân + 3 trang phụ lục)
và **slide cũng đã dựng xong** (`output/slide-thuyet-trinh.html`, 17 slide chính +
3 dự phòng, lời dẫn kèm sẵn). Việc còn lại là rà soát và diễn tập — không việc nào
phải bắt đầu từ trang trắng.

1. **T23 rà soát chéo** — mỗi người review 2 hình của người khác, checklist ở
   `style-guide.md` §7, và **sheet *Checklist nộp bài* của file phân công còn 19/23
   mục “Chưa kiểm”** — phần lớn đã có bằng chứng đo được trong repo, chỉ chưa ai
   điền. Chạy `src/check_readability.py` trước cho đỡ mất công. Lỗi phụ đề treemap
   (lời hướng dẫn bấm chuột in trên ảnh tĩnh) **đã sửa** (B25).
2. **T29 diễn tập** — §4 sổ này đã đủ **10** câu kèm câu trả lời; còn nói thành
   tiếng, bấm giờ. Lời dẫn từng slide nằm sẵn trong `output/slide-thuyet-trinh.md`
   (651 chữ, chừng 5 phút).
3. **T30 dọn repo** — pipeline đã chạy lại trọn vẹn; còn dọn ảnh trùng trong
   `.report/` (xem bên dưới), nhớ sửa đường dẫn trong `main.tex` / `index.html`
   nếu xoá.

**Trang demo trực tuyến** — `src/build_web.py` → `site/`, 22 biểu đồ tương tác theo
năm nhịp, đẩy lên GitHub Pages bằng `.github/workflows/pages.yml` (**B26**). Còn một
bước cần admin repo: Settings → Pages → Source: *GitHub Actions*. Thấy khi dựng: phụ
đề hình T20 chạm sát tiêu đề ô 1995 — việc của T23.

Slide chia sẵn ai nói phần nào theo cột *Người phụ trách* của file phân công; muốn
đổi thì sửa khoá `chu` của slide đó trong `src/build_slides.py` rồi chạy lại.

**Chỗ yếu cần biết trước khi lên trình bày.** Đề xuất ở T31 dựa trên RCA và PCI
— hai chỉ số **đo rổ hàng gộp**, nên chúng nói *cái gì đi qua Việt Nam*, chưa hẳn
*cái gì ở lại*. Atlas không tách được; TiVA tách được ở mức ngành cho năm 2022
(A19), nhưng lệch năm so với 2023 và không xuống tới HS4, nên vẫn phải nói thẳng
những giới hạn ấy chứ đừng để người chấm hỏi ra (D2, D5). Điểm mạnh bù lại: quy tắc chọn của
T31 **đã chạy lại trên hai năm quá khứ** và cả hai lần đều chỉ đúng chỗ (2007 →
điện tử, 2015 → sắt thép vượt ngưỡng), trên một nền mà RCA **không** tự đi lên —
xem A14 và A17. Nhưng A17 cũng đo được rằng sức dự báo nằm ở điều kiện **PCI > 0**
chứ không ở dải RCA, và lớp thoả trọn quy tắc chỉ có 6 nhóm; nói đúng chừng đó.

Hai quyết định còn treo:

- Có tải `hs92_country_product_year_4.csv` (452 MB, ~4,2 giờ) để có chi tiết HS4 không
  — hiện là hạn chế D4.
- `notebooks/Nhom8_Demo.ipynb` (chưa vào git) **trùng** phần treemap/sunburst của
  T12–T13; chỉ đoạn cone-tree 3D là riêng, mà cone-tree không có trong danh sách 30
  việc. Cần hỏi nhóm giữ hay bỏ.

Hai thứ **đã thấy, chưa xử lý** — ghi ra để khỏi quên, không phải việc gấp:

- **`.report/` nặng vô ích.** Sáu file PNG của chương 9 nằm **ba bản giống nhau**
  (`overleaf/img/`, `midterm/images/`, `midterm/assets/images/`), cộng
  `cover-image.jpg` **2,84 MB**. Dọn ở T30.
- **`cc_year.csv` 28,4 MB nằm vĩnh viễn trong lịch sử `main`.** PR #3 và #4 gộp bằng
  merge commit chứ không squash, nên commit đã gỡ file ra vẫn không xoá được blob.
  **Đã thống nhất để nguyên** — viết lại lịch sử một repo nhóm đang dùng thì lợi ít
  hại nhiều. Từ nay gộp bằng squash.

---

## 6. Cách cập nhật sổ này

Mỗi lần gộp một PR, sửa đúng ba chỗ, mất khoảng hai phút:

1. Dòng **Cập nhật** ở đầu file: ngày, số việc Xong, commit `main`.
2. Một dòng mới trong bảng **§2**.
3. Ô trạng thái + ô "sản phẩm thật" trong bảng **§1**, khớp với cột *Trạng thái* của
   `phan-cong-cong-viec.xlsx` (sheet *Phân công chi tiết*, cột H).

Phát hiện mới thì **không** ghi vào đây — ghi vào `phat-hien-va-quyet-dinh.md` theo
số A tiếp theo, rồi ở đây chỉ trỏ sang. Sổ này giữ mỏng để còn đọc được một lượt.

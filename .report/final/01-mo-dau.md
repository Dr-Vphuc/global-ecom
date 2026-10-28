# 1. Mở đầu

## 1.1 Câu hỏi, người đọc, và quyết định cần thuyết phục

Câu hỏi nghiên cứu đã chốt ở `docs/cau-hoi-nghien-cuu.md`:

> **Việt Nam đang đứng ở đâu trong mạng lưới thương mại toàn cầu năm 2023, và vị
> trí đó được tạo nên bởi cái gì?**

Ba câu hỏi con, và mỗi câu có một họ kỹ thuật trả lời:

| | Câu hỏi con | Trả lời bằng | Nằm ở |
|---|---|---|---|
| **a** | Mạng lưới thương mại thế giới có hình dạng thế nào? | mật độ, phân bố bậc, Gini trọng số, node-link, ma trận kề | §4.1 |
| **b** | Việt Nam nối với ai, và nối chặt đến đâu? | bậc, độ mạnh, betweenness, cụm Louvain, chord | §4.2, §5.2, §5.3 |
| **c** | Việt Nam bán cái gì, và cái đó đáng giá đến đâu? | treemap, sunburst, RCA × PCI, ECI theo thời gian | §3.2, §5.1, §6.1 |

Lát cắt bắt buộc của đề tài là **Việt Nam trong ASEAN**, và báo cáo xử lý nó như
**một câu hỏi, không phải một tiền đề** — §4.2 cho thấy ba phép đo độc lập đều
không tìm thấy ASEAN như một cộng đồng thương mại.

**Người đọc chính là giảng viên và bạn cùng lớp môn Trực quan hóa dữ liệu**, đọc
kỹ *cách làm* và không mặc định biết kinh tế học. Hệ quả ràng buộc lên cả báo cáo:
mỗi thuật ngữ (RCA, PCI, ECI, Gini, betweenness, Louvain, HHI) được giải thích
bằng một câu đời thường ngay chỗ dùng lần đầu, và **mọi con số lần ngược được về
một script trong `src/`** — không có số nào chép tay từ một trang web.

Và báo cáo **không dừng ở mô tả**. Vai diễn là nhà tư vấn: bốn phần đầu dựng bằng
chứng, phần 7 nói ra việc nên làm, phần 8 nói thẳng chỗ nào lập luận còn yếu. Đó
là quyết định **B18** trong sổ phát hiện, và nó là lý do báo cáo có một quy tắc
chọn viết trong code (§7.1) thay vì một đoạn khuyến nghị viết bằng cảm tính.

## 1.2 Thông điệp chính

Một câu mà toàn bộ báo cáo hướng tới:

> **Từ 1995 đến 2023 Việt Nam đã đi từ rìa vào giữa mạng lưới thương mại thế giới,
> nhưng bước nhảy về _khối lượng_ lớn hơn hẳn bước nhảy về _vị thế_: xuất khẩu
> nhiều nhất ASEAN mà độ phức tạp chỉ đứng thứ năm, và quá nửa hàng hoá đi về đúng
> ba thị trường.**

Ba thứ hạng lệch nhau chính là câu chuyện, và phải ghi kèm mẫu số vì mẫu số đổi
theo năm:

| Việt Nam 2023 xếp hạng theo… | Hạng | Trên |
|---|---|---|
| Giá trị xuất khẩu | **16** | 230 nước có xuất khẩu trong mạng 2023 |
| Độ phức tạp kinh tế (ECI) | **78** | 230 nước Atlas chấm được ECI |
| Mức tập trung giá trị xuất khẩu (HHI) | **30** | 97 nước xuất trên 10 tỷ USD |

Tiền thì hạng 16, chất lượng hàng thì hạng 78, và mức dồn vào ít thị trường thì
nằm ở nhóm **một phần ba tập trung nhất** thế giới.

⚠️ Bản nháp thông điệp ở `docs/cau-hoi-nghien-cuu.md` từng viết *"nhiều tiền chảy
qua ít kênh"* và trích hạng **số bạn hàng** (66/231) làm bằng chứng. Phát hiện
**A16** (§5.3) đã bác phép đo đó: đếm bạn hàng là đếm cả những luồng cỡ một triệu
USD, và ở bất kỳ mức sàn giá trị nào thì số kênh của Việt Nam lại **tăng**. Câu
dùng trong báo cáo này là *"dồn tiền vào ít cửa hơn"*, đo bằng HHI và tỷ trọng
ba bạn hàng đầu — xem §5.3.

## 1.3 Năm câu, theo thứ tự lập luận

| Nhịp | Phát hiện | Con số đỡ cho nó | Hình |
|---|---|---|---|
| 1 | Rổ hàng đã được xây lại gần như từ đầu | điện tử 0,60% → **29,94%**; tổng xuất khẩu gấp **75,3 lần** | T21 |
| 2 | Và năng lực đi lên thật, đo được | ECI #181/211 → **#78/230**; COI 0,225 → **1,197** | A1 |
| 3 | Nhưng tiền dồn lại vào ít cửa | HHI 0,0662 (2013) → **0,1226** (2023); top-3 nhận **52,41%** | T19, T20 |
| 4 | Và chỗ bán đậm nhất là chỗ hàng dễ nhất | giày dép RCA **7,52** / PCI −0,49; máy móc RCA **0,95** / PCI +0,78 | T31 |
| 5 | → Đề xuất (mục riêng) | — | T31 |

Bốn nhịp đầu là **phần 3 đến phần 6** của báo cáo; nhịp 5 là **phần 7 — Đề xuất**, dựng trên §6.1 và §6.2.

Trước bốn nhịp đó, §4.1–§4.2 trả lời câu hỏi nghiên cứu ở tầng mạng lưới: **cấu
trúc thương mại toàn cầu trông như thế nào, và Việt Nam nằm ở đâu trong đó.** Ba
kết quả đầu tiên đều đi ngược trực giác thông thường, nên phải nói trước — nếu
không, người đọc sẽ tưởng các hình bị vẽ sai.

---

## 1.4 Bố cục báo cáo, và mười một hình đứng ở đâu

Báo cáo đi theo bốn hồi mà file phân công đã chốt — **Quy mô → Cấu trúc → Vị trí
Việt Nam → Ý nghĩa** — rồi thêm hai mục mà vai nhà tư vấn đòi phải có:

| Phần | Nội dung | Hồi |
|---|---|---|
| 2 | Phương pháp luận: số ở đâu ra, vì sao tin được | — |
| 3 | **Quy mô**: thế giới gấp 4,51 lần, Việt Nam gấp 75,3 lần | ① |
| 4 | **Cấu trúc**: mạng này không có hub, và ASEAN không phải một cộng đồng | ② |
| 5 | **Vị trí Việt Nam**: trèo lên thật, nhưng qua một hành lang đang hẹp lại | ③ |
| 6 | **Ý nghĩa**: trèo bằng gì, và điều đó ràng buộc đề xuất thế nào | ④ |
| 7 | **Đề xuất** — quy tắc, phép thử lại ba lần, mục tiêu đo được | ⑤ |
| 8 | Hạn chế và kết luận | — |
| Phụ lục | Mười bảng sạch · sáu cửa kiểm · cây HS92 · quy ước thị giác · lệnh tái lập | — |

Mười một họ hình, cả hai họ kỹ thuật của môn học (cây **và** đồ thị), mỗi hình
render ở **hai năm** để câu tiêu đề không bao giờ là một khẳng định viết sẵn:

| Hình | Việc | Script | Đứng ở |
|---|---|---|---|
| Treemap cơ cấu xuất khẩu | T12 | `make_hierarchy_charts.py` | §3.2 |
| Sunburst 4 tầng cây HS92 | T13 | `make_hierarchy_charts.py` | §3.2, §A.3 |
| Small multiples 4 nước ASEAN | T14 | `make_small_multiples.py` | §5.1 |
| Log-log phân bố bậc | T09 | `make_degree_loglog.py` | §4.1 |
| Node-link mạng đã lọc | T15 | `make_node_link.py` | §4.1, §4.2 |
| Hai ma trận kề (alphabet / cụm) | T16 | `make_adjacency_matrix.py` | §4.1, §4.2 |
| Chord giữa tám khối | T17 | `make_chord.py` | §4.2 |
| Sankey nhập → VN → xuất | T19 | `make_sankey.py` | §5.2 |
| Small multiples theo thời gian | T20 | `make_time_multiples.py` | §5.3 |
| Streamgraph 10 ngành, 29 năm | T21 | `make_streamgraph.py` | §3.2 |
| Mặt phẳng quyết định RCA × PCI | T31 | `make_decision_plane.py` | §6.1, §7 |

Hai cặp hình đứng trên **cùng một dữ liệu** để so trực tiếp họ nào hợp việc nào:
node-link và ma trận kề (§4.1), và hai cách sắp hàng–cột của chính ma trận đó —
alphabet so với cụm Louvain (§4.2).

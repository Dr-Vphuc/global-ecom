# T01 — Câu hỏi nghiên cứu, thông điệp chính, đối tượng người xem

**Đồ án:** Mạng lưới thương mại quốc tế — vị trí của Việt Nam trong cấu trúc thương mại toàn cầu
**Dữ liệu:** Atlas of Economic Complexity (Harvard), 1995–2023, 231 quốc gia
**Năm mốc:** 2023 (bản 2024 còn tạm — xem `phat-hien-va-quyet-dinh.md` mục A6)
**Trạng thái:** bản nháp để cả nhóm sửa

---

## 1. Câu hỏi nghiên cứu

> **Việt Nam đang đứng ở đâu trong mạng lưới thương mại toàn cầu năm 2023, và
> vị trí đó được tạo nên bởi cái gì?**

Ba câu hỏi con, tương ứng ba phần của bài:

| | Câu hỏi con | Trả lời bằng |
|---|---|---|
| **a** | Mạng lưới thương mại thế giới có hình dạng thế nào? | mật độ, phân bố bậc, Gini trọng số, node-link, ma trận kề |
| **b** | Việt Nam nối với ai, và nối chặt đến đâu? | bậc, cường độ, trung gian, cụm Louvain, biểu đồ chord |
| **c** | Việt Nam bán cái gì, và cái đó đáng giá đến đâu? | treemap, sunburst, RCA × PCI, ECI theo thời gian |

Lát cắt bắt buộc: **Việt Nam trong ASEAN** — so với 9 nước còn lại, và biến thiên 1995 → 2023.

---

## 2. Thông điệp chính

Một câu mà **toàn bộ** bài hướng tới:

> **Từ 1995 đến 2023 Việt Nam đã đi từ rìa vào giữa mạng lưới thương mại thế giới,
> nhưng bước nhảy về _khối lượng_ lớn hơn hẳn bước nhảy về _vị thế_: xuất khẩu
> nhiều nhất ASEAN mà độ phức tạp chỉ đứng thứ năm, và hơn một nửa hàng hóa đi về
> đúng ba thị trường.**

### Bốn con số đỡ cho thông điệp đó — đã đo, không phải trích dẫn

**① Khối lượng thì nhảy rất xa.** Xuất khẩu 5,1 → **385,5 tỷ USD**, gấp **75,3 lần**,
trong khi cả thế giới chỉ gấp 4,51 lần. Thị phần thế giới 0,107% → **1,780%**.
Năm 2023 Việt Nam **xuất khẩu nhiều nhất ASEAN** — trên cả Malaysia (353,9) và
Singapore (346,6).

**② Vị thế thì nhảy chậm hơn.** ECI −1,00 (hạng 181/211) → **+0,58 (hạng 78/230)**.
Trong ASEAN, đó là **hạng 5**: sau Singapore +1,68, Malaysia +0,95, Thái Lan +0,85,
Philippines +0,76. Bán nhiều nhất khối, nhưng không bán thứ phức tạp nhất khối.

**③ Ba thứ hạng lệch nhau — đó chính là câu chuyện.**

| Việt Nam xếp hạng theo… | Hạng (trên 230 nước) |
|---|---|
| Giá trị xuất khẩu | **16** |
| Số bạn hàng | 68 |
| Độ phức tạp kinh tế (ECI) | 78 |

Tiền thì hạng 16, mà mạng lưới và chất lượng hàng thì hạng gần 70–80.
Nhiều tiền chảy qua **ít kênh**, và là kênh của hàng chưa phức tạp.

**④ Nhìn kỹ hơn nữa thì thấy vì sao.** Điện–điện tử chiếm **29,9%** xuất khẩu
nhưng RCA chỉ 2,23. Hai nhóm phức tạp nhất bảng có RCA **dưới 1** — tức hiện diện
_ít hơn_ mức bình quân thế giới:

| Nhóm hàng | Xuất khẩu | RCA | PCI |
|---|---|---|---|
| Máy móc công nghiệp | 39,8 tỷ | **0,95** | +0,78 |
| Thiết bị quang học | 11,3 tỷ | **0,91** | +0,93 |
| Giày dép | 19,6 tỷ | **7,52** | −0,49 |
| Cà phê, chè, gia vị | 4,5 tỷ | **4,21** | −1,38 |

Chỗ Việt Nam **mạnh nhất** lại là chỗ **ít phức tạp nhất**, và ngược lại.

### Hai phát hiện phụ đủ sức đứng thành một biểu đồ riêng

- **Tập trung thị trường:** top 3 bạn hàng chiếm **52,4%** xuất khẩu. Riêng Hoa Kỳ
  (24,7%) và Trung Quốc (22,3%) đã là **47,0%**.
- **Nghịch lý ASEAN:** Việt Nam nằm trong ASEAN nhưng chỉ bán **7,8%** hàng cho
  9 nước còn lại. Ở trong khối, nhưng buôn bán hướng ra ngoài khối.

---

## 3. Đối tượng người xem

**Người đọc chính: giảng viên và bạn cùng lớp môn Trực quan hóa dữ liệu.**
Họ đọc kỹ *cách làm* — nguồn dữ liệu, phép đo, lựa chọn thiết kế — và **không**
mặc định biết kinh tế học. Hệ quả cụ thể, ràng buộc lên mọi biểu đồ:

1. **Mỗi thuật ngữ được giải thích đúng một lần, ngay chỗ dùng lần đầu, bằng một
   câu đời thường.** RCA, PCI, ECI, Gini, betweenness, Louvain — không có cái nào
   được coi là hiển nhiên. (Bản giải thích sẵn có ở `kien-thuc-nen-tang.md`.)
2. **Mỗi biểu đồ có một câu tiêu đề nói _kết luận_, không nói _tên biểu đồ_.**
   "Việt Nam mạnh ở nhóm hàng ít phức tạp" chứ không phải "Biểu đồ phân tán RCA–PCI".
3. **Mọi con số trong bài phải lần ngược được về một script trong `src/`.**
   Không chép tay số từ trang web nào.
4. Trục, đơn vị, năm ghi rõ trên từng hình — người chấm không đọc chú thích cuối bài.

**Người đọc phụ:** sinh viên hoặc người quan tâm kinh tế Việt Nam, đọc lướt.
→ Bài phải đọc được **chỉ bằng tiêu đề và hình**, bỏ hết chữ thân bài vẫn hiểu.

**Người bài này _không_ nhắm tới: chuyên gia kinh tế thương mại.** Nói rõ vì nó
quyết định phạm vi. Dữ liệu là xuất khẩu **gộp**, không có giá trị gia tăng, nên
bài **không** kết luận được "Việt Nam giữ lại bao nhiêu giá trị". Mọi nhận định
theo hướng đó chỉ là **suy luận từ RCA × PCI**, và phải viết đúng như vậy
(xem mục D trong `phat-hien-va-quyet-dinh.md`).

---

## 4. Ranh giới — để khỏi phình việc

| Có làm | Không làm |
|---|---|
| 1995–2023, dữ liệu Atlas | Dự báo tương lai |
| Xuất khẩu hàng hóa | Dịch vụ, FDI, kiều hối |
| HS92 cấp 1–2 (10 ngành / 97 nhóm) | HS4 (5.040 mã) — trừ khi tải kịp file 452 MB |
| Việt Nam + 9 nước ASEAN làm lát cắt | Phân tích sâu từng nước ASEAN |
| Mô tả cấu trúc và thay đổi | Giải thích nguyên nhân chính sách |

---

## 5. Chốt cái gì ở bản này

Ba thứ, chốt xong thì T02 và T04 mới chạy được:

- [ ] **Câu hỏi** ở mục 1 — sửa chữ được, nhưng chốt phạm vi.
- [ ] **Thông điệp** ở mục 2 — đây là câu quyết định bố cục cả bài.
- [ ] **Ranh giới** ở mục 4 — nhất là dòng HS4 và dòng "không giải thích nguyên nhân".

Ai không đồng ý chỗ nào thì sửa thẳng vào file rồi commit, đừng bình luận miệng —
bài viết ra từ file này.

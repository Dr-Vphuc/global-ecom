# 6. Ý nghĩa: trèo lên bằng gì, và điều đó ràng buộc đề xuất thế nào

Hồi bốn trả lời câu hỏi con **(c)** ở §1.1 — *Việt Nam bán cái gì, và cái đó đáng
giá đến đâu* — rồi chuyển thành bản lề sang phần Đề xuất. §6.1 là **phát hiện
trung tâm của cả đồ án**; §6.2 biến bốn hồi bằng chứng thành bốn điều kiện mà bất
kỳ đề xuất nào cũng phải thoả.

## 6.1 Trèo lên bằng gì: lợi thế mạnh nhất nằm đúng ở nơi hàng dễ nhất

`data/processed/country_product.csv` · Việt Nam, 2023, cấp HS2

| Nhóm hàng | Xuất khẩu | % rổ hàng | **RCA** | **PCI** |
|---|---|---|---|---|
| Điện, điện tử và linh kiện | 115,43 tỷ | 29,94% | 2,2299 | **+0,925** |
| Máy móc công nghiệp | 39,85 tỷ | 10,34% | **0,9537** | **+0,783** |
| Thiết bị quang học, đo lường, y tế | 11,32 tỷ | 2,94% | **0,9052** | **+0,934** |
| Giày dép | 19,64 tỷ | 5,09% | **7,5182** | −0,493 |
| Hàng may mặc (dệt kim) | 14,74 tỷ | 3,82% | 3,6736 | −0,663 |
| Hàng may mặc (không dệt kim) | 14,16 tỷ | 3,67% | 3,2852 | −0,870 |
| Đồ nội thất | 11,77 tỷ | 3,05% | 2,3598 | +0,250 |
| Trái cây, hạt | 6,98 tỷ | 1,81% | 2,8782 | −1,332 |
| Thủy sản | 6,25 tỷ | 1,62% | 2,7539 | −1,589 |

**RCA** (*lợi thế so sánh hiện hữu*) trả lời: nhóm hàng này chiếm tỷ trọng trong rổ
hàng của Việt Nam **gấp bao nhiêu lần** tỷ trọng của nó trong thương mại thế giới —
trên 1 là bán đậm hơn mức bình quân. **PCI** là độ khó của nhóm hàng, cũng của
Atlas. Đọc chéo hai cột cuối ra **phát hiện trung tâm của cả đồ án**:

> **Lợi thế so sánh của Việt Nam mạnh nhất đúng ở nơi sản phẩm đơn giản nhất, và
> yếu nhất đúng ở nơi sản phẩm phức tạp nhất.**

Giày dép PCI −0,49 mà RCA **7,52**; trái cây −1,33 mà 2,88; thủy sản −1,59 mà
2,75. Ngược lại, hai nhóm **phức tạp nhất** bảng — thiết bị quang học (PCI +0,934)
và máy móc công nghiệp (+0,783) — đều có **RCA dưới 1**, tức Việt Nam hiện diện ở
đó *ít hơn* mức bình quân thế giới: **không có lợi thế so sánh nào cả.**

Điện tử là ngoại lệ đáng nói: PCI +0,925, và là nhóm lớn nhất với 115,43 tỷ USD
(29,94% rổ hàng) — nhưng RCA chỉ **2,23**, tức Việt Nam lớn trong điện tử gần đúng
theo tỷ lệ điện tử lớn trong thương mại thế giới, chứ không vượt trội như cách nước
này vượt trội ở giày dép (7,52).

Chia rổ hàng theo bốn góc của mặt phẳng RCA × PCI thì thấy nó **đang** dịch, nhưng
chưa đủ:

| Góc | Nghĩa | 2015 | 2023 |
|---|---|---|---|
| Đã thắng | RCA ≥ 1, PCI > 0 | 32,3% | **38,2%** |
| Cơ hội | RCA < 1, PCI > 0 | 16,5% | **21,6%** |
| **Đang kẹt** | RCA ≥ 1, PCI ≤ 0 | 44,7% | **36,2%** |
| Ngoài cuộc | RCA < 1, PCI ≤ 0 | 6,5% | 4,0% |

Góc "đang kẹt" — bán rất đậm nhưng hàng dễ — co từ 44,7% xuống 36,2% trong tám
năm. Rổ hàng **đang rời** khỏi góc đó, nhưng **hơn một phần ba vẫn nằm lại**, và
các nhóm nằm lại là những nhóm đã giảm tỷ trọng suốt 28 năm.

⚠️ Một chỗ phải nói rõ trước khi ai đó đọc hình T31: ô **`Chưa phân loại` chiếm
11,83% rổ hàng** — 45,60 tỷ USD, RCA **2,4408** (cao hơn cả điện tử), PCI −1,206.
Đó là nhóm HS2 `99` với nút con duy nhất `XXXX` (*Trade data discrepancies*) của
Atlas, **không phải một ngành để đầu tư**. Quy tắc chọn trong
`make_decision_plane.py` loại thẳng nó (`sector != UNCLASSIFIED`); nếu không, ô bán
đậm thứ hai trên mặt phẳng quyết định lại là một ô dữ liệu không phân loại được.
Xem §A.3.

Lấy lại: `src/make_decision_plane.py` · `src/make_hierarchy_charts.py`

---

## 6.2 Những phát hiện này ràng buộc phần Đề xuất như thế nào

Phần Đề xuất là mục riêng, nhưng nó không được tự do: bốn nhịp trên đã khoá sẵn
bốn điều kiện mà bất kỳ đề xuất nào cũng phải thoả.

1. **Không đề xuất "đa dạng hoá thị trường" bằng cách đếm thêm bạn hàng** (§5.3).
   Thêm một nước nhận 5 triệu USD không đổi được HHI. Phép đo phải là tỷ trọng giá
   trị, nên mục tiêu cũng phải phát biểu theo tỷ trọng giá trị.
2. **Không đề xuất dồn thêm vào điện tử** (§6.1). RCA đã 2,23, chiếm 29,94% rổ
   hàng, và là khâu phụ thuộc nhập khẩu nhất trong hành lang ở §5.2.
3. **Không đề xuất dồn thêm vào nhóm RCA cao – PCI thấp** (§6.1). Thủy sản, cà
   phê, trái cây đã bán rất đậm và đã giảm tỷ trọng suốt 28 năm.
4. **Đề xuất phải nói được điều gì sẽ làm nó sai.** §5.3 đưa ra sẵn một mốc kiểm
   chứng: nếu HHI tiếp tục đi xuống từ 0,1226 mà không cần can thiệp gì, thì vấn
   đề tự giải và đề xuất mất phần cấp thiết.

Chỗ còn lại sau bốn điều kiện đó là góc **"cơ hội"** — RCA dưới 1 nhưng PCI dương,
21,6% rổ hàng — và trong góc ấy, hai nhóm đang sát ngưỡng lợi thế: **thiết bị quang
học, y tế** (RCA 0,75 → 0,9052; PCI +0,934) và **máy móc công nghiệp** (0,46 →
0,9537; +0,783). Đó là đầu vào của mục Đề xuất, kèm quy tắc chọn và **ba lần chạy lại nó
trên quá khứ** (xem §7.1, §7.2, A14 và A17).

---


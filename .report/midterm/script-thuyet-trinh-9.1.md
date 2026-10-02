# Script thuyết trình — Phần 9.1 Biểu diễn cấu trúc phân cấp

**Người trình bày:** Nguyễn Khắc Huy · **Thời lượng:** 5 phút · **Slide:** 4 → 11 (đánh số `-1-` đến `-8-`)
**Nguồn nội dung:** bản dịch mục 9.1, `.report/overleaf/main.tex`

| Slide | Nội dung | Thời lượng | Cộng dồn |
|---|---|---|---|
| 4 | 1.1 Sơ đồ Node-Link | 55 s | 0:55 |
| 5–8 | 1.2 Bố cục chữ nhật (4 bước hoạt cảnh) | 70 s | 2:05 |
| 9 | 1.2 Treemap hoàn chỉnh + ưu/nhược | 50 s | 2:55 |
| 10 | 1.3 Bố cục xuyên tâm | 55 s | 3:50 |
| 11 | 1.4 Hiển thị 3 chiều | 45 s | 4:35 |
| — | Chuyển cho bạn Phúc | 10 s | 4:45 |

Script dài khoảng **610 từ**, tương đương 4 phút 15 ở tốc độ 145 từ/phút. Phần dôi ra là khoảng đệm cho chuyển slide và nhịp nghỉ — nói thoải mái, đừng vội.

> **Lưu ý về thứ tự:** slide trình bày node-link **trước**, rồi mới tới treemap và sunburst. Sách và bản dịch thì ngược lại — mục 9.1.1 là nhóm lấp đầy không gian, 9.1.2 mới là nhóm không lấp đầy. Script bám theo **thứ tự slide**. Nếu cô hỏi, xem phần Hỏi đáp ở cuối.

---

## Slide 4 — Sơ đồ Node-Link · 55 giây

> Em là Nguyễn Khắc Huy, em trình bày phần đầu: biểu diễn cấu trúc phân cấp.
>
> Sách chia các kỹ thuật vẽ cây thành hai nhóm: **lấp đầy không gian** và **không lấp đầy không gian**. Em sẽ đi qua cả hai.
>
> Trước hết là sơ đồ node-link — cách biểu diễn phổ biến nhất. Node là đối tượng dữ liệu, link là quan hệ giữa chúng. Sơ đồ tổ chức hay cây gia phả đều thuộc loại này.
>
> Việc vẽ cây chịu ảnh hưởng bởi hai yếu tố: **bậc phân nhánh** — một node cha có bao nhiêu con — và **độ sâu** của cây.
>
> Đây là các tiêu chí thẩm mỹ mà thuật toán vẽ hướng tới: giảm giao cắt đường, giảm diện tích, giảm độ dài cạnh, giảm điểm gấp khúc, hướng tới đối xứng. Điểm đáng nói là **chúng thường xung đột nhau** — tối ưu cái này thì hỏng cái kia. Hình bên phải là cây cân bằng nên thỏa mãn được gần hết.

---

## Slide 5–8 — Bố cục chữ nhật, hoạt cảnh · 70 giây

*Bốn slide này là một mạch liên tục, đừng dừng giữa chừng.*

> Nhóm thứ hai là lấp đầy không gian, đại diện là **treemap**.
>
> Ý tưởng: thay vì dùng cạnh để nối, ta dùng **phép đặt kề** — đặt các ô sát nhau để ngụ ý quan hệ, nên không tốn chỗ cho đường nối.

**[bấm sang slide 5]**

> Bắt đầu với toàn bộ hình chữ nhật, tương ứng node gốc, rồi cắt dọc chia cho các con.

**[bấm sang slide 6]**

> Mấu chốt là **chia theo tỉ lệ nào**. Không chia đôi, mà chia theo **số node lá** trong mỗi cây con. Node 1 chỉ có một lá nên được dải rất hẹp; node 2 chứa mười hai lá nên chiếm gần hết phần còn lại.

**[bấm sang slide 7]**

> Xuống tầng sau, ta **đổi hướng cắt** — lần này cắt ngang — rồi lặp lại quy tắc đó.

**[bấm sang slide 8]**

> Cứ luân phiên ngang, dọc, đệ quy xuống. Chạm node lá thì vẽ ô và dừng.

---

## Slide 9 — Treemap hoàn chỉnh · 50 giây

**[bấm sang slide 9]**

> Đây là kết quả sau mười ba node lá. Số trên cây bên trái khớp với số trên ô bên phải.
>
> **Ưu điểm:** dùng hết không gian màn hình, không lãng phí pixel nào. Hợp khi ta quan tâm tới node lá — ví dụ mặt hàng nào chiếm tỉ trọng xuất khẩu lớn nhất.
>
> **Nhược điểm:** rất khó thấy cấu trúc phân nhánh. Ta thấy ô to ô nhỏ, nhưng không thấy node nào là cha của node nào.
>
> Sách nhắc hai biến thể: **treemap vuông hóa** tránh ô dài và mảnh, và **treemap lồng nhau** làm rõ lại cấu trúc.

---

## Slide 10 — Bố cục xuyên tâm · 55 giây

> Cũng lấp đầy không gian, nhưng chia theo hướng xuyên tâm, là **sunburst**.
>
> Node gốc ở tâm. Mỗi tầng là một vành tròn, càng ra ngoài càng sâu; mỗi vành chia theo số node ở tầng đó.
>
> Nguyên tắc cấp phát diện tích giống treemap. Khác biệt quan trọng: **treemap dồn gần hết không gian cho node lá, còn sunburst thể hiện cả node trung gian** — chính là các vành ở giữa. Nhờ vậy nhìn ra ngay quan hệ cha–con, thứ mà treemap giấu đi.
>
> Đổi lại: cây càng cao thì vành ngoài càng dài, diện tích node lá ở xa bị phóng đại; cây lệch thì hình cũng lệch theo.

---

## Slide 11 — Hiển thị 3 chiều · 45 giây

> Cuối cùng, với cây rất lớn, một hướng là dùng chiều thứ ba — nổi tiếng nhất là **cone tree**, cây hình nón.
>
> Các node con được xếp xuyên tâm tại những góc cách đều, rồi đẩy lệch vuông góc với mặt phẳng, tạo thành hình nón.
>
> Hai tham số quyết định là bán kính và khoảng dịch chuyển. Sách gợi ý cho bán kính tỉ lệ nghịch với độ sâu — node gần gốc tách xa, node gần đáy sát lại.
>
> Nhược điểm cố hữu của 3D là **che khuất**: nhánh trước che node sau. Nên thực tế người ta vẫn ưa cây 2D hơn.

**[chuyển tiếp]**

> Phần của em đến đây là hết. Tiếp theo bạn Phúc sẽ trình bày về đồ thị và mạng tùy ý. Em cảm ơn cô và các bạn.

---

## Nếu còn dư thời gian

Thêm vào cuối slide 9:

> Đây cũng là lý do nhóm em chọn treemap cho đồ án cuối kỳ: cây phân loại sản phẩm HS92 có hơn sáu nghìn node và bốn tầng, treemap cho thấy ngay ngành nào chiếm tỉ trọng lớn trong cơ cấu xuất khẩu của Việt Nam.

## Nếu bị hụt giờ — cắt theo thứ tự này

1. Hai biến thể treemap vuông hóa / lồng nhau (slide 9) — tiết kiệm ~12 giây.
2. Câu về bậc phân nhánh và độ sâu (slide 4) — ~10 giây.
3. Mẹo bán kính tỉ lệ nghịch độ sâu (slide 11) — ~12 giây.

**Tuyệt đối giữ:** quy tắc chia theo số node lá (slide 6) và khác biệt sunburst thể hiện node trung gian (slide 10). Đây là hai ý cốt lõi của cả phần.

---

## Hỏi đáp có thể gặp

**Sách trình bày theo thứ tự nào?**
Ngược với slide: mục 9.1.1 là nhóm lấp đầy không gian (treemap, sunburst), 9.1.2 mới là nhóm không lấp đầy (node-link, cone tree). Nhóm em xếp node-link lên trước vì nó trực giác hơn, giúp người nghe có sẵn hình dung về cây trước khi sang cách biểu diễn trừu tượng hơn.

**Treemap và sunburst khác nhau ở đâu, khi nào dùng cái nào?**
Cùng nguyên tắc cấp phát diện tích theo số node lá. Treemap dồn gần hết không gian cho node lá nên hợp khi cần so sánh độ lớn giữa các lá; sunburst thể hiện cả node trung gian nên hợp khi cần đọc cấu trúc phân nhánh và quan hệ phả hệ.

**Vì sao phải luân phiên hướng cắt ngang – dọc?**
Nếu cắt mãi một hướng, các ô sẽ ngày càng dài và mảnh: khó bấm chuột, khó ước lượng diện tích bằng mắt, không đủ chỗ đặt nhãn. Treemap vuông hóa ra đời chính để xử lý triệt để vấn đề này.

**Diện tích ô tỉ lệ với cái gì?**
Trong thuật toán cơ bản của sách là **số node lá** trong cây con. Ứng dụng thực tế thường thay bằng một giá trị định lượng gắn với node — ví dụ kim ngạch xuất khẩu.

**Vì sao 3D không phổ biến dù thể hiện phả hệ rõ hơn?**
Vì che khuất. Nhánh phía trước che node phía sau, buộc người dùng xoay và thu phóng liên tục mới đọc được — chi phí tương tác lớn hơn lợi ích.

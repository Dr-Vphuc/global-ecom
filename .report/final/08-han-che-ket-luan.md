# 8. Hạn chế và kết luận

## 8.1 Năm hạn chế phải nói trước

Nêu ra thì được điểm trung thực; giấu đi mà bị hỏi thì mất nhiều hơn.

**D1. Dữ liệu dừng ở 2023, không phải 2024.** Bản Atlas 2024 còn tạm: thiếu 1.781
cặp nước, riêng Việt Nam mất 37 bạn hàng trị giá 11,4 tỷ USD. Xem §2.3.

**D2. ECI tính trên xuất khẩu gộp** → nó thưởng điểm cho việc **lắp ráp** hàng phức
tạp bất kể nước đó giữ lại được bao nhiêu giá trị. Nói cách khác, ECI đo *cái gì đi
qua Việt Nam*, chưa hẳn là *cái gì ở lại Việt Nam*. **Phần này đã đo được ở mức
ngành** (xem D5): hàng điện tử giữ 44,2% giá trị trong nước, và hàng càng phức tạp
thì tỷ lệ trong nước càng thấp (ρ = −0,47). Nên ECI đúng là thiên về hàng ít giá trị
ở lại, nhưng ở mức vừa chứ không tuyệt đối.

**D3. Node-link vứt 98,5% số cạnh.** Nó **không** đọc được là "bản đồ thương mại
toàn cầu", mà là *"bản đồ các luồng thương mại lớn, cộng chỗ đứng của ASEAN trong
đó"*. Ai muốn nhìn phần đuôi phải xem ma trận kề (T16) — ma trận vẽ đủ **cả 416
luồng có hướng**, không gộp hai chiều như node-link, và không có cạnh nào chồng lên
cạnh nào. Nhưng nó cũng chỉ vẽ **đúng 416 luồng ấy**: cả hai hình đứng trên cùng
một đồ thị đã lọc, nên ma trận **không** cứu được cái 98,5% đã bỏ.

**D4. Dữ liệu dừng ở HS2 (97 nhóm hàng).** Chi tiết hơn cần file HS4 452 MB, khoảng
4,2 giờ tải ở tốc độ đo được. Hệ quả cụ thể: nhóm "Điện, điện tử và linh kiện" gộp
cả chip lẫn dây điện vào một ô.

**D5. Giá trị gia tăng chỉ đo được ở mức ngành, năm 2022, và là ước lượng.** Atlas không
có bảng vào–ra, nên nhóm lấy thêm bảng TiVA 2025 của OECD (80 nền kinh tế, 50 ngành,
đến 2022) và ghép 10 ngành sang mã ISIC qua nhóm HS2 (A19). Kết quả: bình quân hàng
hóa ghép được giữ **50,5%** trong nước; điện tử **44,2%** (chiếm 36,9% xuất khẩu),
dệt may 53,0%, nông sản 60,4%, kim loại 66,2%. Bốn điều phải nói kèm:
- **Lệch năm:** TiVA dừng ở 2022, đồ án dùng 2023.
- **Lệch độ chi tiết:** TiVA chia theo ngành ISIC, không theo HS, nên không tính lại
  được RCA, PCI hay ECI trên giá trị gia tăng; HS2 cũng không tách máy tính khỏi máy
  móc chung (khối ấy ra 44,2% theo quy mô TiVA và 44,8% theo bảng ghép).
- **"Trong nước" tính theo lãnh thổ, không theo chủ sở hữu:** lợi nhuận của doanh
  nghiệp nước ngoài có thể chuyển ra ngoài mà vẫn được tính là giá trị làm ra ở đây.
- **9,8% xuất khẩu (HS97, HS99) không ghép được**, nên ngành "Khác" không có số.

Phần "xuất trừ nhập" trên Sankey (T19) vẫn là **số học**, không phải giá trị tăng thêm.

Hai hạn chế cuối cùng nối thẳng vào chỗ yếu nhất của đề xuất, nên báo cáo nói ra
trước thay vì chờ bị hỏi. Điểm mạnh bù lại là phép thử lại ở §7.2.

---

## 8.2 Một câu hỏi mà dữ liệu này không trả lời được

Năm hạn chế trên là **giới hạn của dữ liệu**. Còn đúng một câu hỏi mà phát hiện
A16 (§5.3) mở ra mà chính nó không đóng lại được:

**Vì sao các luồng xuất khẩu nhỏ biến mất?** §5.3 đo được rằng chúng biến mất (166
bạn hàng năm 2023 so với 208 năm 2002) và đo được rằng chúng **không đáng kể về
tiền** (47 nước rời danh sách mang theo 0,59% kim ngạch). Nhưng dữ liệu này không
phân biệt được hai cách giải thích: thương mại với những nước đó **thật sự dừng**,
hay nó đã **dồn qua trung gian** rồi được ghi sang tên nước khác. Hai cách ấy có ý
nghĩa khác nhau hẳn cho Đề xuất B ở §7.3, và tách được chúng cần dữ liệu luồng
hàng theo chặng mà Atlas không có.

Bốn câu hỏi mở còn lại đều đã nằm trong năm hạn chế ở §8.1 và không nhắc lại ở đây:
giá trị ở lại Việt Nam (D2, D5) · chi tiết dưới cấp HS2 (D4) · phần đuôi của mạng
đã bị lọc (D3) · năm 2024 (D1). Riêng "giá trị ở lại Việt Nam" nay đã đo ở mức ngành;
phần còn thiếu là mức HS4, năm 2023 và chủ sở hữu (D2, D5).

## 8.3 Kết luận

**Trả lời câu hỏi nghiên cứu.** Năm 2023 Việt Nam đứng ở **hạng 16/230** theo giá
trị xuất khẩu, **nhiều nhất ASEAN**, trong một mạng lưới mà quá nửa số cặp nước có
giao dịch trực tiếp (mật độ 0,5183) nên vị trí không được tạo bởi việc *nối với ai*
mà bởi **luồng nào lớn**. Vị trí đó được tạo nên bởi ba thứ đo được: một rổ hàng đã
được xây lại gần như từ đầu (điện tử 0,6% → 29,9%; nông sản 42,9% → 11,6%), một
**hành lang** mua của Đông Á (68,3% hàng vào) và bán cho Bắc Mỹ (Hoa Kỳ +85,33 tỷ
USD), và một năng lực đi lên thật nhưng chậm hơn khối lượng (ECI #181/211 → #78/230,
hạng 5 trong ASEAN).

**Và điều đáng nói nhất không nằm ở chỗ Việt Nam đã đi được bao xa, mà ở chỗ cách
đi ấy đang hẹp lại:** tỷ trọng ba thị trường đầu **52,41%** so với 39,25% năm 2013,
HHI **0,1226** đã vượt mức của năm 1995, và lợi thế so sánh mạnh nhất vẫn đúng ở
nơi hàng dễ nhất (giày dép RCA 7,52 / PCI −0,49) trong khi hai nhóm khó nhất rổ
hàng vẫn ở RCA **dưới 1**. Từ đó ra đề xuất ở phần 7, và nó kèm sẵn bốn điều kiện
để bị bác bỏ. Một trong bốn đo phần giá trị ở lại: số TiVA cho thấy hai nhóm được đề
xuất giữ khoảng 44–48% giá trị trong nước, không hơn điện tử (§6.2), nên đề xuất
đứng trên độ khó của hàng và mức tập trung chứ không đứng trên việc giữ nhiều hơn.

**Một kết luận về phương pháp, và nó đáng kể hơn vẻ ngoài.** Trong lúc làm, đồ án
đã **tự bác hai phát biểu của chính mình** vì đo lại thì không đúng:

| Phát biểu cũ | Đo lại ra gì | Hệ quả |
|---|---|---|
| *"Số bạn hàng đạt đỉnh 200 nước năm 2005"* | đỉnh thật **2002, 208 nước** — con số cũ chỉ tìm đỉnh trong **bốn năm được vẽ** | sửa A13, sửa tiêu đề hình T20 |
| *"Tiền vào nhiều hơn qua ít kênh hơn"* | phép đếm bạn hàng **không bền**: ở mức sàn 100 triệu USD thì số kênh **tăng** 13 → 83 | thay bằng HHI và tỷ trọng top-3 (**A16**) |

Cả hai đều bị bắt bởi cùng một quy ước làm việc: **mọi con số in trên hình phải
được suy lại từ dữ liệu trong chính lần chạy đó, và mỗi hình phải render thêm một
năm đối chứng rồi đọc kết quả** (§A.4). Quy ước đó tốn thời gian và đã trả lại bằng
việc không để một câu sai nào đi vào bài. Đó cũng là lý do báo cáo này dám kết bằng
một đề xuất: không phải vì tin vào kết luận, mà vì mỗi con số đỡ cho nó đều có một
lệnh in ngay cạnh để người đọc tự chạy lại.

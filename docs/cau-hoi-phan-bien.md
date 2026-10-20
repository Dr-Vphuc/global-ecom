# Mười hai câu phản biện và câu trả lời (T29)

Dùng để diễn tập. Mỗi câu có: **câu trả lời ngắn** (nói ngay), **số liệu đỡ**
(nếu bị hỏi tiếp), và **chỗ tra** khi cần mở ra.

Nguyên tắc chung khi bị hỏi: nếu không biết thì nói không biết, rồi nói ta có
thể kiểm bằng cách nào. Đoán bừa một con số là cách mất điểm nhanh nhất.

---

## Về phương pháp và dữ liệu

### 1. "Các em có kiểm tra chất lượng dữ liệu không?"

**Ngắn:** Có, và chúng em phát hiện ra một điều không định tìm.

**Đỡ:** Phân công ban đầu là đối chiếu Atlas với BACI và Comtrade. Chúng em bỏ
kế hoạch đó vì ba nguồn ấy **không độc lập** — Atlas và BACI đều dẫn xuất từ
Comtrade, nên đối chiếu chúng chỉ đo được khác biệt thuật toán làm sạch.

Thay vào đó chúng em làm phép kiểm **chênh lệch gương**: mỗi luồng A→B được hai
cơ quan hải quan khai riêng. Kết quả: **2.093/2.093 luồng lớn trùng khít
100,0%**. Nghĩa là Growth Lab đã hòa giải số liệu trước khi phát hành, và
**bộ dữ liệu này không cho phép chúng em tự đo sai số của nó**. Chúng em báo
cáo điều đó thay vì nói "ba nguồn đều khớp", vì câu kia sẽ là tuyên bố sai.

**Tra:** `python src/compare_mirror.py`

### 2. "Vì sao chọn năm 2023 mà không phải năm mới nhất?"

**Ngắn:** Vì bản 2024 còn tạm và sẽ làm sai chính phát hiện chính của bọn em.

**Đỡ:** Bản 2024 thiếu **1.781 cặp nước**, riêng Việt Nam mất **37 bạn hàng**.
Phát hiện quan trọng nhất của bọn em là "Việt Nam mất thị trường từ 2005". Nếu
dùng 2024, phần lớn mức giảm đó sẽ là dữ liệu chưa về đủ chứ không phải hiện
thực — bọn em sẽ báo cáo một kết quả bị thổi phồng.

### 3. "Vì sao ngưỡng lọc là 0,046%? Con số đó ở đâu ra?"

**Ngắn:** Nó là ngưỡng nhỏ nhất giữ được đủ 10/10 nước ASEAN ở mọi năm mốc.

**Đỡ:** `analyze_network.py` in ra bảng so sánh **9 chiến lược ngưỡng**. Ngưỡng
0,046% cộng quy tắc giữ top-3 luồng vào/ra cho mỗi nước ASEAN cho **416 cạnh,
67,8% giá trị, đủ 10/10 ASEAN**. Không có quy tắc top-3 thì Brunei và Lào rơi
ra, mà hai nước đó nằm trong nhóm trọng tâm.

Quan trọng hơn là vì sao ngưỡng **tương đối** chứ không tuyệt đối: ngưỡng cố
định 10 tỷ USD giữ 89 cạnh và chỉ 4/10 ASEAN năm 1995, nhưng 390 cạnh và 8/10
năm 2023. So sánh qua thời gian bằng ngưỡng cố định thì phần lớn "thay đổi" chỉ
là lạm phát.

**Tra:** `python src/analyze_network.py`

### 4. "Vì sao không dùng force-directed cho toàn bộ 27.535 cạnh?"

**Ngắn:** Vì mạng này không có cấu trúc tô-pô để force-directed phơi ra.

**Đỡ:** Mật độ **51,8%** — một nước trung bình buôn với hơn nửa thế giới. Bậc
lớn nhất chỉ gấp **1,8 lần** bậc trung vị. Không có hub, nên không có hình sao,
không có lõi–vỏ. Vẽ hết thì ra một mảng mực đều.

Cấu trúc thật nằm ở **trọng số**: Gini **0,957**, top 1% cạnh giữ **61,2%** giá
trị. Vì vậy phép lọc của bọn em lọc theo **giá trị**, không theo bậc — đó là
quyết định xuất phát từ hình dạng dữ liệu chứ không phải từ thẩm mỹ.

**Tra:** `python src/make_degree_dist.py`

### 5. "Bố cục force-directed phụ thuộc hạt giống ngẫu nhiên. Sao tin được?"

**Ngắn:** Bố cục thì đổi, cấu trúc thì không — và bọn em đã đo.

**Đỡ:** Hạt giống chỉ xoay và lật hình. Phân cụm Louvain mới là thứ quyết định
khối nào gồm nước nào, và bọn em chạy **20 hạt giống**: **100,0% số cặp nước
giữ nguyên quan hệ** cùng cụm / khác cụm, số cụm luôn là 3, modularity không
đổi ở **0,337**.

Ngoài ra, ma trận kề ở T16 **không phụ thuộc hạt giống nào cả** mà vẫn cho ra
đúng ba khối — hai phương pháp độc lập cùng kết quả.

**Tra:** `python src/compute_metrics.py`, mục "Độ ổn định cộng đồng"

---

## Về kết quả

### 6. "Betweenness của Việt Nam bằng 0 — vậy Việt Nam không quan trọng?"

**Ngắn:** Không phải. Nó có nghĩa là **không nước nào** quan trọng theo nghĩa
đó, trong một mạng dày như thế này.

**Đỡ:** Betweenness đo "nằm trên đường đi ngắn nhất giữa hai nước khác". Mạng có
mật độ 51,8% nên hầu hết các cặp đã nối thẳng — chẳng ai cần đi vòng qua ai.
Việt Nam được **0,0000 và đồng hạng với 57 nước khác**; chính script tự in ra
cảnh báo rằng thứ hạng này không đọc được.

Mức quan trọng của Việt Nam thể hiện ở chỗ khác: **hạng 16/231** về kim ngạch.

### 7. "Vậy rốt cuộc Việt Nam có phải nút trung chuyển không?"

**Ngắn:** Đúng một nửa, và hai nửa phải tách ra.

**Đỡ:** Theo **tô-pô** thì không — betweenness bằng 0 (câu 6). Theo **dòng
tiền** thì có — Việt Nam nhập **332,1 tỷ** và xuất **385,5 tỷ**, tức nhập bằng
**86,1%** giá trị xuất, giá trị gia tăng trong nước chỉ **13,9%**. 40% hàng
nhập từ Trung Quốc, 25% hàng xuất sang Hoa Kỳ.

Trả lời "có" hoặc "không" gọn lỏn đều sai. Đúng là: Việt Nam là **công xưởng
lắp ráp**, không phải **trạm trung chuyển**.

### 8. "Biểu đồ Sankey của các em chứng minh hàng Trung Quốc đi qua Việt Nam sang Mỹ?"

**Ngắn:** Không, và bọn em đã ghi rõ điều đó trên chính biểu đồ.

**Đỡ:** Dữ liệu Atlas cho biết Việt Nam nhập bao nhiêu từ Trung Quốc và xuất
bao nhiêu sang Mỹ, nhưng **không** liên kết hai việc đó ở cấp lô hàng. Hai bên
nút Việt Nam là **hai phép đo riêng đặt cạnh nhau**, không phải một dòng chảy
liên tục. Biểu đồ đo **mức phụ thuộc đầu vào**, không chứng minh trung chuyển.

Muốn chứng minh thật thì cần dữ liệu thương mại theo **giá trị gia tăng** (như
TiVA của OECD) hoặc dữ liệu hải quan cấp lô hàng — cả hai đều ngoài phạm vi.

### 9. "Việt Nam chế tạo nhiều hơn Thái Lan và Malaysia?"

**Ngắn:** Về tổng bốn ngành chế tạo thì có; về điện tử thì **không** — Malaysia
cao hơn.

**Đỡ:** Tổng bốn ngành chế tạo: VNM **64,6%**, THA 48,6%, MYS 47,6%, IDN 21,7%.
Nhưng riêng điện tử: MYS **33,0%** cao hơn VNM 29,9%.

Điều Việt Nam thật sự khác biệt là **dệt may và giày dép: 18,4%**, gấp **2,3
lần** nước thứ hai là Indonesia (7,9%). Việt Nam là nước duy nhất trong nhóm
còn dựa mạnh vào ngành này.

*Bọn em từng viết sai câu này trong bản nháp và đã sửa sau khi tính lại bảng.*

### 10. "ECI tăng từ −1,00 lên +0,58 — nghĩa là gì?"

**Ngắn:** Rổ hàng xuất khẩu của Việt Nam trở nên tinh vi hơn, không chỉ nhiều
hơn.

**Đỡ:** ECI đo mức độ **đa dạng và độc quyền** của rổ hàng, không đo kim ngạch.
Thứ hạng đi từ **181/211** lên **78/230** — phải nói cả mẫu số vì số nước được
xếp hạng đã đổi.

Nó độc lập với kim ngạch, nên việc nó cùng chiều với chuyển dịch cơ cấu (điện
tử 0,6% → 29,9%) là bằng chứng thứ hai cho cùng một kết luận.

⚠️ Nhưng đọc kèm **nghịch lý RCA**: lợi thế so sánh của Việt Nam vẫn mạnh nhất ở
giày dép (RCA 7,52) và cà phê (4,21), yếu nhất ở máy móc công nghiệp. ECI tăng
vì Việt Nam **xuất** hàng phức tạp, chưa hẳn vì Việt Nam **làm** phần phức tạp.

---

## Về thiết kế

### 11. "Vì sao không tô màu cho từng cộng đồng? Xám khó nhìn."

**Ngắn:** Vì bọn em đã đo và không còn màu nào dùng được.

**Đỡ:** Bọn em thử **7 bảng 3 màu** (Paul Tol high-contrast, Tol bright,
Okabe–Ito và 4 biến thể). Tất cả tốt ở mắt thường (ΔE 26–46), nhưng khi mô
phỏng mù màu thì khoảng cách tới **màu ngành gần nhất** tụt còn **ΔE 2,6–6,6**
— tức là trùng với một màu ngành. Bảng 10 màu ngành đã chiếm hết gam an toàn.

Nên bọn em mã hóa cộng đồng **hai lần, dư thừa có chủ ý**: ba nấc xám (ΔE nội
bộ 20,1 / 36,5 / 61,0) cộng ba hình dạng. Xám không có sắc độ nên mô phỏng mù
màu không làm nó đổi — **ΔE vẫn 20,1 với cả protan, deutan và tritan**. Người
mù màu hoàn toàn vẫn đọc được hình này, điều mà không bảng màu nào làm nổi.

**Tra:** chú thích `COMMUNITY_FILL` trong `src/reference_data.py`

### 12. "Em chạy một công cụ kiểm bảng màu và nó báo hỏng."

**Ngắn:** Nhiều khả năng công cụ đó dùng thang **OKLab**, bọn em dùng
**CIEDE2000** — hai thang khác nhau, không quy đổi được.

**Đỡ:** Cặp hay bị báo nhất là Điện tử `#88CCEE` ↔ Khác `#DDDDDD`. Đo bằng
CIEDE2000: **ΔE 18,9** ở mắt thường, **14,9 / 18,2 / 23,5** ở protan / deutan /
tritan — vượt xa ngưỡng 15 và 10 mà bọn em đặt ra.

Hai cảnh báo khác mà công cụ ngoài hay nêu — "dải độ sáng quá rộng" và "độ bão
hòa thấp" — là đặc tính cố hữu của thang Paul Tol muted. Style guide đã bù bằng
quy định **viền trắng 1px bắt buộc** cho bốn màu nhạt cộng nhãn chữ trực tiếp
trên mảng.

**Tra:** `python src/check_palette.py`

---

## Phòng hờ: ba câu khó không có trong danh sách

**"Nếu có thêm một tháng, các em làm gì?"**
Ba việc, theo thứ tự ưu tiên: (1) tải dữ liệu HS4 để vẽ cây đủ 4 tầng — hiện
chỉ tới tầng 2; (2) lấy dữ liệu TiVA của OECD để kiểm giả thuyết trung chuyển
cho đàng hoàng thay vì chỉ đo tỷ lệ nhập/xuất; (3) phân tích theo ngành×nước
chứ không chỉ theo nước, để biết điện tử của Việt Nam đi đâu riêng.

**"Phát hiện nào các em ít tự tin nhất?"**
Việc đặt tên ba khối. Thuật toán cho ra ba cụm rất ổn định, nhưng gọi chúng là
"khối châu Á do Trung Quốc dẫn đầu" là **diễn giải của bọn em** — cụm 0 có cả
Brazil, Nga và Nam Phi. Bọn em đã kiểm thành phần thật trước khi đặt tên và ghi
lại trong code, nhưng cái tên vẫn là một nhận định chứ không phải một phép đo.

**"Phần nào trong bài này không phải đóng góp của các em?"**
Dữ liệu và chỉ số ECI, PCI, RCA là của Harvard Growth Lab. Thuật toán Louvain,
betweenness là của networkx. Bảng màu nền là thang muted của Paul Tol. Đóng góp
của bọn em là: chọn câu hỏi, chọn phép lọc và biện minh bằng số, kiểm chất
lượng dữ liệu, và các lựa chọn trình bày — gồm cả những chỗ bọn em bác bỏ giả
thuyết ban đầu của chính mình.

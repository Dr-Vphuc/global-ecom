# 7. Đề xuất

Bốn hồi trên là bằng chứng; mục này là việc nên làm. Báo cáo kết thúc bằng một đề
xuất chứ không dừng ở mô tả — đó là quyết định **B18** — và đề xuất phải **suy ra
từ một quy tắc viết trong code**, không chọn bằng tay.

## 7.1 Đề xuất được chọn bằng một quy tắc

Phần đề xuất **không phải một lựa chọn bằng tay**. Nó là đầu ra của một bộ lọc
viết trong `src/make_decision_plane.py`:

```python
c = df[(df["export_value"] >= MIN_EXPORT)      # ≥ 1 tỷ USD: đủ lớn để đáng bàn
       & (df["pci"] > 0)                        # khó hơn trung bình thế giới
       & (df["rca"] >= RCA_LO)                  # 0,5: đã có chỗ đứng
       & (df["rca"] < RCA_HI)                   # 1,5: chưa phải nơi đã thắng
       & (df["d_rca"] > 0)                      # đang đi lên, không đi xuống
       & (df["sector"] != UNCLASSIFIED)]        # không phải ô XXXX — xem §A.3
return c.nlargest(N_PICK, "pci")                # lấy 2 nhóm khó nhất còn lại
```

**Vì sao phải là một quy tắc.** Một lựa chọn bằng tay không kiểm được: ai cũng có
thể nói *"tôi nghĩ nên dồn vào X"*. Một quy tắc thì **chạy lại được trên quá khứ**,
và đó là bằng chứng mạnh nhất của cả báo cáo — §7.2.

Chạy quy tắc trên dữ liệu 2023 thì **8 nhóm** lọt vào vòng chọn, xếp theo PCI:

| Nhóm hàng cấp 2 | RCA 2015 → 2023 | PCI | Xuất khẩu 2023 | |
|---|---|---|---|---|
| Thiết bị quang học, đo lường, y tế | 0,75 → **0,91** | **+0,93** | 11,3 tỷ USD | ← **đề xuất** |
| Máy móc công nghiệp | 0,46 → **0,95** | **+0,78** | 39,8 tỷ USD | ← **đề xuất** |
| Nhựa | 0,45 → 0,60 | +0,43 | 7,1 tỷ USD | |
| Đồ chơi và dụng cụ thể thao | 0,82 → 1,41 | +0,37 | 3,6 tỷ USD | |
| Giấy và bìa | 0,30 → 0,64 | +0,27 | 2,2 tỷ USD | |
| Sắt thép | 0,60 → 1,00 | +0,25 | 8,1 tỷ USD | |
| Sản phẩm từ sắt thép | 0,58 → 0,60 | +0,19 | 3,8 tỷ USD | |
| Nhôm | 0,40 → 0,54 | +0,04 | 2,1 tỷ USD | |

Quy tắc lấy **hai nhóm khó nhất** trong tám nhóm đó. Cả tám đều là lựa chọn hợp lệ
theo bốn điều kiện ở §6.2; thứ phân biệt chúng là PCI, tức độ khó của hàng — và đó
đúng là chiều mà §6.1 cho thấy Việt Nam đang yếu nhất.

Lấy lại: `PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_decision_plane.py --year 2023`

## 7.2 Quy tắc đã được chạy lại trên quá khứ ba lần, và nền so sánh không dễ

Đây là phát hiện **A17**, làm trong lúc ráp báo cáo. Quy tắc ở §7.1 không có tham
số nào gắn với năm 2023, nên chạy được ở bất kỳ năm nào có đủ dữ liệu. Chạy ở hai
năm quá khứ thì nó chọn ra cái gì, và tám năm sau cái đó đi đâu:

| Chạy quy tắc ở | Lệnh | Nó chọn | Tám năm sau |
|---|---|---|---|
| **2007** | `--year 2007 --since 1999` | máy điện – điện tử, RCA 0,573 | RCA **1,996** (2015) → **2,230** (2023); xuất **3,4 → 115,4 tỷ USD** |
| **2015** | `--year 2015 --since 2007` | thiết bị quang học, 0,751 · sắt thép, 0,604 | 0,905 · **1,003 — vượt ngưỡng lợi thế** |
| **2023** | `--year 2023` | thiết bị quang học, 0,905 · máy móc công nghiệp, 0,954 | *đề xuất của báo cáo này* |

Lần chạy 2007 là lần đáng kể nhất: quy tắc chỉ ra **điện tử** khi nhóm đó mới xuất
3,4 tỷ USD và RCA còn 0,573 — trước đợt bùng nổ đưa nó thành 115,43 tỷ USD và
29,94% rổ hàng (§3.2). Quỹ đạo của bốn nhóm từng được quy tắc chọn, đo ở bốn mốc:

| RCA của nhóm | 1999 | 2007 | 2015 | 2023 |
|---|---|---|---|---|
| Máy điện – điện tử (chọn 2007) | 0,345 | **0,573** | 1,996 | 2,230 |
| Sắt thép (chọn 2015) | 0,017 | 0,265 | **0,604** | **1,003** |
| Thiết bị quang học (chọn 2015 và 2023) | 0,116 | 0,455 | **0,751** | **0,905** |
| Máy móc công nghiệp (chọn 2023) | 0,068 | 0,268 | 0,459 | **0,954** |

**Và nền so sánh — phần làm cho ba lần ấy có nghĩa.** Phản biện hiển nhiên là *"cả
rổ hàng cùng lên thì chọn gì chẳng đúng"*. Đo thử: trong **97 nhóm** hàng cấp 2 của
Việt Nam, giữa 2015 và 2023 chỉ **44 nhóm (45,4%)** có RCA tăng, trung vị thay đổi
**−0,0178**. RCA là **tỷ trọng của một tỷ trọng**, nên khi rổ hàng đổi, phần lớn
các nhóm phải đi xuống — không có cái tide nào dâng sẵn:

| Nhóm con, cửa sổ 2015 → 2023 | Số nhóm | % có RCA tăng | Trung vị thay đổi |
|---|---|---|---|
| Tất cả | 97 | 45,4% | −0,0178 |
| RCA 2015 ≥ 1,5 — *nơi đã thắng* | 24 | **25,0%** | **−0,6413** |
| RCA 2015 < 0,5 | 46 | 58,7% | +0,0138 |
| **PCI > 0 — hàng khó** | 43 | **62,8%** | **+0,0260** |
| PCI ≤ 0 — hàng dễ | 54 | 31,5% | −0,0733 |
| PCI > 0 **và** đã tăng ở cửa sổ trước | 19 | **63,2%** | **+0,0907** |
| Dải RCA 0,5–1,5, **không** lọc gì khác | 27 | 40,7% | −0,0405 |

Hai dòng cuối là chỗ phải đọc trung thực, và báo cáo nói ra thay vì để bị hỏi:

- **Điều kiện mang sức dự báo là `PCI > 0`, không phải dải RCA.** Hàng khó tăng RCA
  ở 62,8% số nhóm, hàng dễ chỉ 31,5%. Còn dải RCA 0,5–1,5 đứng một mình thì **kém
  hơn** cả mức bình quân (40,7% so với 45,4%). Dải đó có mặt trong quy tắc vì nó
  chọn *chỗ còn đường để đi* — RCA ≥ 1,5 thì đã thắng và 75% số nhóm ở đó đi xuống
  — chứ không phải vì nó dự báo được.
- **Và lớp các nhóm thoả trọn quy tắc thì quá nhỏ để kết luận:** 6 nhóm ở cửa sổ
  2015 → 2023 (50% tăng, trung vị +0,0205), và ở cửa sổ 2007 → 2015 thì lớp
  tương đương (12 nhóm) lại **tệ hơn** mức bình quân của chính cửa sổ đó —
  **25,0%** tăng so với 37,1% của cả 97 nhóm, trung vị −0,1893. Nên bằng
  chứng mạnh ở **ba lần chọn cụ thể** và ở **điều kiện PCI**, chứ chưa mạnh ở mức
  "quy tắc này đúng về mặt thống kê". Một quy tắc ba lần chọn đúng trên ba nhóm là
  thành tích đáng kể với một bộ dữ liệu 29 năm, không phải một phép kiểm giả thuyết.

Lấy lại: ba lệnh ở cột *Lệnh* bảng trên · bảng nền so sánh đo từ
`data/processed/country_product.csv`, hai năm một cặp, lệnh ghi ở §A.5

## 7.3 Đề xuất: hai nhóm hàng, và một mục tiêu về mức tập trung

> **Đề xuất A — về rổ hàng.** Phần ưu tiên tăng thêm cho xuất khẩu nên dồn vào
> **thiết bị quang học – đo lường – y tế** (HS90; RCA 0,905; PCI +0,934; 11,32 tỷ
> USD) và **máy móc công nghiệp** (HS84; RCA 0,954; PCI +0,783; 39,85 tỷ USD) —
> hai nhóm khó nhất trong rổ hàng mà Việt Nam **đã** có chỗ đứng và đang sát ngưỡng
> lợi thế — thay vì đào sâu thêm vào **lắp ráp điện tử** (RCA đã 2,23, chiếm 29,94%
> rổ hàng, và là khâu phụ thuộc nhập khẩu nhất của hành lang ở §5.2), và **không**
> dồn thêm vào nhóm RCA cao – PCI thấp (thủy sản 2,75 / −1,59; cà phê 4,21 / −1,38;
> trái cây 2,88 / −1,33), vốn đã giảm tỷ trọng suốt 28 năm.

Hai nhóm này thoả cả bốn điều kiện mà §6.2 đã khoá: không đo bằng phép đếm bạn
hàng, không dồn thêm vào điện tử, không dồn thêm vào góc hàng dễ, và có mốc bác bỏ
viết sẵn (§7.5). Chúng cũng ở hai cỡ khác nhau, nên là hai loại việc khác nhau:
HS84 đã **39,85 tỷ USD (10,34% rổ hàng)** — một nhóm lớn, mỗi điểm phần trăm RCA
đổi được nhiều tiền; HS90 chỉ **11,32 tỷ (2,94%)** — một chỗ đặt cược nhỏ hơn
nhưng là nhóm **khó nhất** còn lại trong rổ.

> **Đề xuất B — về mức tập trung.** §5.3 là một phát hiện đòi một câu trả lời,
> không chỉ một lời cảnh báo. Mục tiêu phải phát biểu bằng **tỷ trọng giá trị**,
> không bằng số bạn hàng: đưa **tỷ trọng ba thị trường đầu** từ **52,41%** xuống
> dưới mức 2013 là **39,25%**, tức HHI từ **0,1226** về quanh trung vị của 97 nước
> xuất trên 10 tỷ USD là **0,0921**. Phía mua vào cấp thiết hơn: HHI **0,1979**,
> ba nhà cung cấp đầu **61,3%**, riêng Trung Quốc **40,1%** hàng vào.

Vì sao Đề xuất B không phải "tìm thêm thị trường": thêm một nước nhận 5 triệu USD
không đổi được HHI dù nó làm số bạn hàng tăng — đó đúng là cái bẫy mà §5.3 đã đo.
Và vì sao hai đề xuất đi cùng nhau: hàng khó hơn thì bán được cho nhiều nơi khó
hơn, nên A là một trong vài đường dẫn tới B mà dữ liệu này nhìn thấy được.

## 7.4 Mốc kiểm, không phải dự báo

Báo cáo **không dự báo** (ranh giới đã chốt ở T01), nên những con số dưới đây là
**mốc để kiểm lại đề xuất**, không phải dự đoán về tương lai:

| Mốc kiểm | Hiện tại (2023) | Ngưỡng | Lệnh kiểm |
|---|---|---|---|
| RCA của HS90 vượt 1,00 | 0,9052 | **≥ 1,00** | `src/make_decision_plane.py` |
| RCA của HS84 vượt 1,00 | 0,9537 | **≥ 1,00** | `src/make_decision_plane.py` |
| Góc *đã thắng* nở thêm | 38,2% rổ hàng | **> 38,2%** | `src/make_decision_plane.py` |
| Góc *đang kẹt* co lại | 36,2% rổ hàng | **< 36,2%** | `src/make_decision_plane.py` |
| Tỷ trọng ba thị trường đầu | 52,41% | **< 52,41%**, đích 39,25% | `src/make_time_multiples.py` |
| HHI đầu vào | 0,1979 | **< 0,1979** | `src/make_time_multiples.py --direction nhap` |

Cả sáu mốc đều đọc được từ chính các script đã có, nên lần dữ liệu Atlas sau là
kiểm lại được ngay — không cần viết thêm gì.

## 7.5 Điều gì sẽ làm nhóm đổi ý

Một đề xuất có điều kiện bác bỏ thì mới là đề xuất; không có thì chỉ là một ý
thích. Ba điều kiện, theo thứ tự dễ xảy ra:

1. **RCA của HS90 và HS84 chững lại dưới 1,00 trong vài kỳ dữ liệu tới.** Cả hai
   đã đi lên đều qua ba cửa sổ tám năm (§7.2), nên chững lại là tin trái chiều
   thật. Khi đó quy tắc phải chạy lại và chọn lại — nó sẽ tự chọn khác, vì điều
   kiện `d_rca > 0` loại nhóm đang đi xuống.
2. **Mức tập trung tự đi xuống từ 0,1226 mà không cần can thiệp gì.** Thì Đề xuất
   B mất phần cấp thiết, và báo cáo phải nói rằng vấn đề tự giải. HHI đã từng tự
   giảm 18 năm liền (1995 → 2013), nên đây không phải một khả năng xa.
3. **Đầu vào tự đa dạng hoá khỏi mức 68,3% từ một vùng duy nhất.** Thì luận cứ
   "hành lang hẹp ở cả hai đầu" (§5.2, §5.3) yếu đi, và đề xuất về rổ hàng không
   còn tựa vào được chỗ phụ thuộc nhập khẩu của điện tử.

## 7.6 Và đề xuất này không nói điều gì

Ba chỗ phải nói trước khi bị hỏi, vì chúng là ranh giới của dữ liệu chứ không phải
của lập luận:

- **Không nói "nên làm thế nào".** Dữ liệu Atlas là kim ngạch xuất nhập khẩu theo
  nhóm hàng; nó chỉ ra **chỗ nào đáng ưu tiên**, không chỉ ra cơ chế chính sách nào
  đưa tới đó. Ranh giới *"không giải thích nguyên nhân chính sách"* đã chốt ở T01.
- **Không nói Việt Nam giữ lại bao nhiêu giá trị ở hai nhóm ấy.** RCA và PCI đo rổ
  hàng **gộp**, nên chúng đo *cái gì đi qua Việt Nam*, chưa hẳn *cái gì ở lại* —
  đúng hạn chế **D2** và **D5** ở §8.1. Nếu HS84 và HS90 cũng là lắp ráp thuần thì
  RCA vượt 1,00 vẫn không đổi được phần giá trị giữ lại, và báo cáo này **không đo
  được** chỗ đó. Muốn đo cần bảng vào–ra (OECD TiVA hoặc ADB MRIO).
- **Không nói hai nhóm ấy là hai nhóm tốt nhất có thể.** Chúng là hai nhóm **khó
  nhất trong tám nhóm thoả quy tắc** (§7.1). Đổi `N_PICK` hoặc nới `RCA_HI` thì
  danh sách đổi, và bảng tám nhóm ở §7.1 để ngay đó cho người đọc tự xét.

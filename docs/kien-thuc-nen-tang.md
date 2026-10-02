# Kiến thức nền tảng cần có trước khi làm đề tài VN–ASEAN

> Lập ngày 2026-09-20. Dành cho người xuất phát từ Khoa học dữ liệu, **không** có nền Kinh tế.
> Đi kèm: [nguon-du-lieu-vn-asean.md](./nguon-du-lieu-vn-asean.md) (khảo sát nguồn dữ liệu).

**Rủi ro lớn nhất của một sinh viên DS làm đề tài kinh tế không phải là code — mà là làm ra biểu đồ đẹp nhưng kết luận sai hoặc hiển nhiên.** Tài liệu này liệt kê phần kiến thức tối thiểu để tránh điều đó.

---

## 0. Lợi thế sẵn có của dân DS

Đừng nghĩ mình xuất phát từ số 0. Hai thứ khó nhất của đề tài này lại là sân nhà của DS:

- **Bảng Input–Output / MRIO** — nghe rất "kinh tế", nhưng bản chất chỉ là **đại số tuyến tính**. Ma trận Leontief `L = (I − A)⁻¹` là một phép nghịch đảo ma trận. Dân kinh tế học phải vật lộn với nó; bạn thì không.
- **Phân tích mạng lưới thương mại** (centrality, community detection trên đồ thị nước × nước) — công cụ đã có sẵn.

Cái thiếu là **ngữ nghĩa**: biết con số nghĩa là gì, và biết khi nào con số nói dối.

---

## 1. Tầng từ vựng — nửa ngày, nhưng BẮT BUỘC

Không có tầng này thì không đọc nổi file dữ liệu:

| Khái niệm | Vì sao cần |
|---|---|
| **FOB vs CIF** | Xuất khẩu ghi FOB, nhập khẩu ghi CIF (đã cộng cước + bảo hiểm). Nên số "A xuất sang B" luôn **nhỏ hơn** số "B nhập từ A" ~5–10%. Đây là lý do tồn tại của BACI. |
| **Reporter vs Partner**, chiều luồng | Sai chiều là sai toàn bộ phân tích. |
| **Re-export / entrepôt** | Hàng chỉ đi qua cảng. Singapore, Hong Kong bị thổi phồng khủng khiếp. |
| **Nominal vs Real** | Dữ liệu thương mại là **USD hiện hành**. So 1995 với 2023 mà không khử lạm phát/giá hàng hóa là lỗi kinh điển. |
| **Cấu trúc HS** | Chương (2 số) → Nhóm (4) → Phân nhóm (6). HS sửa 5 năm/lần (HS92→96→02→07→12→17→22) → chuỗi thời gian dài **phải** dùng concordance, nếu không sản phẩm sẽ "biến mất" giữa chừng. |
| **HS / SITC / BEC / ISIC** | Bốn hệ phân loại khác nhau: HS = hải quan, SITC = chuỗi dài lịch sử, **BEC = giai đoạn sử dụng** (trung gian / tư liệu SX / tiêu dùng), ISIC = ngành sản xuất. Đề tài này sống nhờ BEC. |
| **Mã nước** | ISO3, UN M49, và BACI dùng mã số riêng. Merge sai mã = mất nước. |

---

## 2. Kinh tế học thương mại lõi — 2–3 ngày

Chỉ 5 ý, nhưng là 5 ý quyết định chất lượng bài:

### ① Lợi thế so sánh (Ricardo)
Nền tảng duy nhất thật sự cần. Một nước xuất cái mình *tương đối* giỏi, không phải cái mình *tuyệt đối* giỏi.

### ② Chỉ số RCA / Balassa
Phiên bản đo được của ý ①. Công thức 1 dòng, đọc: RCA > 1 = có lợi thế.

### ③ Mô hình trọng lực (Gravity model) ⭐ QUAN TRỌNG NHẤT

> Thương mại giữa hai nước ∝ (GDP₁ × GDP₂) / khoảng cách

Đây là quy luật thực nghiệm vững nhất của kinh tế học thương mại. Ý nghĩa: **VN buôn bán nhiều với Thái Lan phần lớn chỉ vì Thái to và gần** — không phải vì có quan hệ chuỗi giá trị đặc biệt.

Không nắm ý này sẽ đọc mọi luồng hàng lớn thành "phụ thuộc" — lỗi diễn giải nghiêm trọng nhất có thể mắc trong đề tài này. Gravity cho **mức kỳ vọng** để so sánh: cái đáng nói là phần *lệch khỏi* kỳ vọng.

### ④ Thương mại nội ngành + chỉ số Grubel–Lloyd
Tại sao VN vừa xuất vừa nhập cùng một mã HS? Vì đó không phải trao đổi hàng hóa, mà là **phân công công đoạn**. GL cao = dấu vân tay của chuỗi giá trị.

### ⑤ Trade creation vs trade diversion (Viner)
FTA vừa tạo ra thương mại mới, vừa *chuyển hướng* thương mại từ nguồn rẻ sang nguồn có ưu đãi thuế. Cần cho phần ATIGA/RCEP.

---

## 3. Khung Chuỗi giá trị toàn cầu (GVC) — 2–3 ngày, trái tim của đề tài

### ① Đường cong nụ cười (Smile curve) ⭐ — công cụ kể chuyện trung tâm

```
Giá trị
gia tăng
  ↑  ╲                                    ╱
     ╲   R&D, thiết kế            Thương hiệu,  ╱
      ╲  bằng sáng chế            marketing,   ╱
       ╲                          dịch vụ     ╱
        ╲___________  LẮP RÁP  _____________╱
                      ← VN ở đây →
     ────────────────────────────────────────→
     Thượng nguồn      Sản xuất      Hạ nguồn
```

Việt Nam nằm ở đáy nụ cười. Cả câu chuyện "kim ngạch cao nhưng giá trị thực nhận thấp" gói gọn trong hình này.

### ② Phân rã giá trị gia tăng
- **DVA** (giá trị gia tăng nội địa) vs **FVA** (nước ngoài) trong xuất khẩu.
- **Double counting** trong thương mại gộp.
- **Backward participation** (nhập đầu vào để xuất) vs **forward participation** (xuất đầu vào cho nước khác xuất tiếp).
- VN cực mạnh backward, rất yếu forward — đó chính là định nghĩa của "gia công".

### ③ Bảng I-O & MRIO
Học `(I − A)⁻¹` dùng làm gì, MRIO khác I-O một nước ra sao. Đây là phần **dễ nhất** với dân DS — nên tận dụng làm điểm khác biệt của đồ án.

### ④ Từ vựng ngành
lead firm, tier-1 / tier-2 supplier, OEM → ODM → OBM (thang nâng cấp), upstreamness / downstreamness.

---

## 4. Bối cảnh VN & ASEAN — 2 ngày đọc

Không có tầng này, bài sẽ chỉ là "biểu đồ về số liệu", không có *insight*. Các thực tế cốt lõi (**số liệu nên kiểm tra lại khi trích dẫn**):

- **Khối FDI chiếm ~70–74% kim ngạch xuất khẩu VN.** Có giai đoạn riêng Samsung ~20%. → "Xuất khẩu của Việt Nam" phần lớn là xuất khẩu *của doanh nghiệp nước ngoài đặt tại* Việt Nam. Ý này thay đổi toàn bộ cách đọc số liệu.
- **Trung Quốc là nguồn nhập khẩu lớn nhất, ~1/3 tổng nhập khẩu.** Phụ thuộc đầu vào vào TQ **lớn hơn nhiều** so với ASEAN. Bài phải trung thực về điều này, nếu không sẽ bị hỏi ngay khi bảo vệ.
- **Tỷ trọng thương mại nội khối ASEAN đứng yên ~21–25% suốt hai thập kỷ**, trong khi EU ~60%. ⭐ **Nên là câu hỏi trung tâm của đồ án.** Lý do: các nước ASEAN **cạnh tranh nhau** trên thị trường thứ ba nhiều hơn là bổ trợ nhau; chuỗi của họ chạy về Trung Quốc/Nhật/Hàn/Mỹ, không chạy vào nhau. Chứng minh được điều này bằng dữ liệu sẽ khiến đồ án nổi bật.
- **Phân hóa trong khối** — gộp chung "ASEAN" thành một khối là sai:
  - Singapore = trung chuyển + tài chính
  - Thái Lan = cụm ô tô
  - Malaysia = đóng gói/kiểm thử bán dẫn (Penang)
  - Indonesia = tài nguyên + chính sách *downstreaming* (cấm xuất nickel thô)
  - CLMV = dệt may, nông sản
- **China+1** sau 2018: VN hưởng lợi, nhưng kèm nghi vấn "chuyển tải" (transshipment).
- **Quy tắc xuất xứ (Rules of Origin)** và **cumulation nội khối ASEAN** — cơ chế pháp lý *tạo ra* chuỗi giá trị khu vực. Đáng một mục riêng.

---

## 5. Được phép BỎ QUA

- Kinh tế vĩ mô: IS-LM, chính sách tiền tệ, tỷ giá.
- Toán của các mô hình lý thuyết: Heckscher–Ohlin, Krugman, Melitz → **đọc 1 đoạn trực giác mỗi cái là đủ**, bỏ hết phần chứng minh.
- Kinh tế lượng ước lượng gravity (PPML, fixed effects) → chỉ cần nếu muốn chạy hồi quy. Đồ án DataViz mô tả là hợp lệ.
- Lý thuyết thuế quan tối ưu, phúc lợi.

---

## 6. Lộ trình 5 ngày — học bằng cách làm

Đừng đọc giáo trình rồi mới code. Mỗi ngày gắn một khái niệm với một biểu đồ:

| Ngày | Học | Làm ngay |
|---|---|---|
| 1 | Tầng từ vựng + cấu trúc HS/BEC | Nạp BACI vào DuckDB, lọc VN×ASEAN, vẽ 1 biểu đồ đường kim ngạch. Gặp lỗi mã nước / đổi phiên bản HS ngay tại đây — học nhanh nhất. |
| 2 | RCA + Grubel–Lloyd | Tính 2 chỉ số này cho VN vs từng nước ASEAN. Đọc công thức *trong lúc* implement. |
| 3 | Gravity + BEC | Vẽ scatter: kim ngạch thực tế vs (GDP×GDP/khoảng cách). Tách hàng trung gian bằng BEC. |
| 4 | Smile curve + DVA/FVA | Tải ADB MRIO hoặc UIBE, vẽ DVA vs gross exports. |
| 5 | Bối cảnh VN/ASEAN | Đọc WDR 2020 + báo cáo ADB. Viết lại phần diễn giải cho toàn bộ biểu đồ đã có. |

---

## 7. Tài liệu (đều miễn phí)

**Bắt đầu từ một cuốn duy nhất:**
- **World Bank, World Development Report 2020 — "Trading for Development in the Age of Global Value Chains"**. Đúng chủ đề, viết cho người ngoài ngành, hình đẹp. Đọc chương 1–3 là đủ nền.

**Sau đó:**
- **Global Value Chain Development Report** (WTO/WB/OECD/ADB — các bản 2017 / 2019 / 2021 / 2023) — phương pháp phân rã giá trị gia tăng.
- **ADB, Asian Economic Integration Report** (thường niên) — số liệu và diễn giải riêng cho ASEAN.
- **OECD, "Guide to using TiVA"** — định nghĩa từng chỉ số.
- **Gaulier & Zignago (2010), BACI documentation** — hiểu dữ liệu đang dùng.
- **Atlas of Economic Complexity → mục "Learn"** — glossary + phương pháp ECI/PCI.
- **World Bank "Taking Stock"** (báo cáo VN, 2 số/năm) — số liệu VN cập nhật.
- Sách đọc thêm: **Richard Baldwin, "The Great Convergence"** — vì sao sản xuất bị chia nhỏ xuyên biên giới.

---

## 8. Bốn câu tự kiểm tra cho MỌI biểu đồ

Dán lên màn hình:

1. **"So với cái gì?"** — Con số lớn này lớn so với GDP? so với tổng nhập khẩu? so với mức gravity dự báo? Một con số đứng một mình không có ý nghĩa.
2. **"Gộp hay gia tăng?"** — Đang đo kim ngạch gộp hay giá trị thực nhận? Nếu gộp, có đang thổi phồng mức phụ thuộc không?
3. **"Có phải chỉ vì to và gần?"** — Phần nào của luồng này là quy luật trọng lực bình thường, phần nào mới thật sự đáng nói?
4. **"Trung chuyển?"** — Con số Singapore/Hong Kong này có phải hàng chỉ đi ngang qua không?

---

## Tóm lại

Phần kinh tế thật sự cần gói trong khoảng **một tuần đọc có chủ đích**, không phải một học kỳ.

Ba khái niệm mang tính sống còn:
1. **Mô hình trọng lực** (gravity model)
2. **Đường cong nụ cười** (smile curve)
3. **Phân biệt gross trade vs value-added**

Nắm ba cái đó thì phần còn lại là kỹ năng xử lý dữ liệu — thứ dân DS đã có sẵn.

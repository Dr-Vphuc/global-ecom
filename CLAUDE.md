# global-ecom — luật của repo này

Đồ án Trực quan hóa dữ liệu: *Mạng lưới thương mại quốc tế — vị trí của Việt Nam
trong cấu trúc thương mại toàn cầu*, kèm lát cắt Việt Nam–ASEAN. Năm tham chiếu là
**2023** (`REFERENCE_YEAR` trong `src/reference_data.py`) vì bản Atlas 2024 còn tạm.

Người dùng học **Khoa học dữ liệu, không học Kinh tế**: gặp thuật ngữ kinh tế thì
giải thích gọn một câu bằng tiếng Việt thường; phần code thì nói thẳng ở độ sâu kỹ
thuật, không cần hạ cấp.

## Trạng thái dự án nằm ở bốn file — đọc trước khi làm, đừng hỏi lại

| File | Giữ cái gì |
|---|---|
| `docs/nhat-ky-cong-viec.md` | 30 việc T01–T30 + trạng thái. **§5 = việc còn lại theo thứ tự**. §6 = cách cập nhật sổ |
| `docs/phat-hien-va-quyet-dinh.md` | Sổ phát hiện **A**n và quyết định thiết kế **B**n — mọi con số đã đo đều ở đây |
| `docs/style-guide.md` | Màu, phông, khổ hình, quy tắc nhãn |
| `phan-cong-cong-viec.xlsx` | Phân công; sheet *Phân công chi tiết*, cột H = Trạng thái |

Bỏ qua việc chia vai R1/R2/R3 trong file phân công — cứ làm việc.

## Chạy Python

```bash
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/<script>.py
```

- Python **3.9**: không có `Path.write_text(newline=...)`, dùng `io.open(..., newline="\n")`.
- **Không bao giờ truyền `-I`** khi script in tiếng Việt (mất `PYTHONIOENCODING`, ra mojibake).
- Thư viện có sẵn trong venv: plotly, kaleido, networkx 3.2.1, pandas, openpyxl.
  **Không cài thêm gói nào mà không được yêu cầu.**
- `output/` và `data/processed/` đã nằm trong `.gitignore`.

## Dữ liệu

- **Dữ liệu thô không bao giờ được commit** (Nguyên tắc #5 của nhóm). Một blob
  `cc_year.csv` 28,4 MB đã lỡ nằm vĩnh viễn trong lịch sử `main` — đừng thêm cái thứ hai.
- `data/processed/edges.csv`: `source_iso3,target_iso3,year,export_value,import_value,log_value,above_threshold`.
- `data/processed/metrics.csv`: chỉ số theo nước, có cả dòng đồ thị `full` và `filtered`.
- Mọi hằng số dùng chung (màu, khổ, năm mốc, hàm định dạng số tiếng Việt) lấy ở
  `src/reference_data.py`, **không viết lại tại chỗ**.

## Chuẩn mực một hình được coi là xong

Đây là phần dễ làm sai nhất, và là phần đã bắt được nhiều câu sai trước khi in ra:

1. **Mọi con số in trên hình phải được suy ra lại từ dữ liệu trong chính lần chạy đó.**
   Không hardcode con số vào tiêu đề, phụ đề hay chú thích.
2. **Tiêu đề phải dựng từ dữ liệu, không phải từ niềm tin.** Nếu câu tiêu đề là một
   khẳng định ("mạng chia thành ba cực quanh X, Y, Z") thì X, Y, Z phải được tính ra,
   để chạy năm khác không để lại một câu sai in trên hình.
3. **Script tự in một khối kiểm chứng** ra stdout, đủ để người đọc kiểm lại khẳng định
   trên tiêu đề mà không cần mở code.
4. **Render thêm một năm đối chứng** (thường 1995) rồi đọc kết quả. Đây là bộ test:
   T09 nhờ nó mà bắt được câu "gần như đều" sai cho 1995; T15 nhờ nó mà bắt được tiêu
   đề "ba cụm là ba châu lục" sai.
5. **Số viết theo kiểu Việt Nam**: dấu phẩy thập phân, dấu chấm hàng nghìn — đi qua
   `R.fmt_vn` / `R.fmt_pct`, kể cả nhãn trục (trục log của plotly phải đặt
   `tickmode="array"` + `tickvals` + `ticktext`, nếu không nó tự dán nhãn tick phụ).
6. **Màu = ngành hàng, chỉ thế thôi** (style guide §3.1). Thứ gì cần màu mà không
   phải ngành thì mở bảng màu riêng, và bảng riêng phải qua đúng bộ kiểm:
   `PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/check_palette.py`.

## Git

- **Commit bằng tiếng Anh**, thân commit giải thích *vì sao* chứ không kể lại diff,
  kết thúc bằng:
  `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`
- **PR bằng tiếng Việt** (tiêu đề + mô tả), kết thúc bằng:
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)`
- Làm trên nhánh **`graph`**, không commit trực tiếp lên `main`.
- **`gh pr merge` bị chặn — người dùng tự gộp.** Được push và mở PR; gộp thì bàn giao.
- Từ nay gộp bằng **squash**.
- `.report/demo/` và `notebooks/` đang cố ý để ngoài git, đừng thêm vào.

## Sau mỗi lần gộp PR, sửa đúng ba chỗ trong `docs/nhat-ky-cong-viec.md`

Theo §6 của chính sổ đó: (1) dòng **Cập nhật** ở đầu file, (2) một dòng mới trong
bảng **§2**, (3) ô trạng thái + ô sản phẩm trong bảng **§1** — và khớp với cột
*Trạng thái* của `phan-cong-cong-viec.xlsx`. Phát hiện mới **không** ghi vào sổ nhật
ký mà ghi vào `phat-hien-va-quyet-dinh.md` theo số A/B tiếp theo, sổ nhật ký chỉ trỏ sang.

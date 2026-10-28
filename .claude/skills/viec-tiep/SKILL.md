---
name: viec-tiep
description: Làm trọn một việc Txx của đồ án global-ecom từ đầu đến commit — chọn việc, đọc đúng ngữ cảnh, dựng hình, tự kiểm chứng số, ghi sổ, cập nhật Excel, commit. Dùng khi được giao một mã việc (T16, T17, T20...), khi người dùng nói "làm việc tiếp theo", hoặc khi một agent context mới được gọi để làm một việc của đồ án này.
---

# Làm một việc Txx, từ đầu đến commit

Quy trình này đủ để một context hoàn toàn mới làm xong một việc đúng chuẩn, không
cần ai kể lại lịch sử. `CLAUDE.md` ở gốc repo đã nạp luật chung; file này là các bước.

## Bước 0 — Đồng bộ

```bash
git fetch --quiet
git checkout graph
git merge origin/main --ff-only
```

Nếu `--ff-only` thất bại: **dừng, báo người dùng**, đừng tự merge hay rebase nhánh nhóm.

## Bước 1 — Chọn việc

Nếu được giao mã việc cụ thể thì làm đúng việc đó. Không thì lấy mục **1** của §5
trong `docs/nhat-ky-cong-viec.md`. Một lần chạy = **một việc**, không gộp hai việc
vào một commit.

## Bước 2 — Đọc đúng ngữ cảnh, không đọc cả repo

Chỉ bốn chỗ, theo đúng thứ tự này:

1. Dòng của việc đó trong bảng **§1** sổ nhật ký — sản phẩm phải ra là gì.
2. Các mục **A**n / **B**n liên quan trong `docs/phat-hien-va-quyet-dinh.md` — việc
   này đã bị chốt sẵn điều gì. Vi phạm một mục B đã chốt là lỗi, không phải sáng tạo.
3. Mục tương ứng trong `docs/style-guide.md`.
4. Một script `src/make_*.py` đã có **gần nhất với việc này** — để bắt chước cách tổ
   chức, cách gọi `reference_data.py`, cách in khối kiểm chứng. Đừng phát minh lại.

## Bước 3 — Dựng

Script mới tên `src/make_<việc>.py`, nhận `--year` và `--layout`/tham số tương tự
qua `argparse`, ghi ra `output/<tên>_<năm>.{html,png}`.

Bắt buộc theo đúng *"Chuẩn mực một hình được coi là xong"* trong `CLAUDE.md`. Sáu
điểm đó là điều kiện xong, không phải gợi ý. Tóm lại: số suy ra từ dữ liệu, tiêu đề
dựng từ dữ liệu, tự in khối kiểm chứng, render thêm năm đối chứng rồi **đọc** kết
quả, số kiểu Việt Nam, màu không mượn của ngành hàng.

Chạy đúng cách:

```bash
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_<việc>.py --year 2023
PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe src/make_<việc>.py --year 1995
```

Rồi **mở file PNG ra xem** (tool Read đọc được ảnh). Chưa xem hình thì chưa xong —
chữ chồng nhau, phụ đề bị cắt mép, chú thích tụt ra ngoài khung chỉ lộ ra khi nhìn.

## Bước 4 — Ghi lại, bốn chỗ

1. `docs/phat-hien-va-quyet-dinh.md` — phát hiện mới thành **A**n tiếp theo, quyết
   định thiết kế mới thành **B**n tiếp theo. Kèm con số đã đo và lệnh lấy lại số đó.
2. `docs/nhat-ky-cong-viec.md` — §1 đổi trạng thái việc + ô sản phẩm; §3 thêm con số
   đáng nhớ kèm lệnh; §5 bỏ việc vừa xong khỏi danh sách. (Dòng §2 và dòng *Cập nhật*
   chỉ sửa **sau khi PR được gộp**, vì lúc đó mới có số PR và commit `main`.)
3. `README.md` — script mới vào cây `src/`, lệnh mới vào khối chạy biểu đồ, đoạn văn
   của việc đó chuyển sang thì quá khứ với số đã đo.
4. `phan-cong-cong-viec.xlsx` — sheet *Phân công chi tiết*, cột H của dòng việc đó →
   `Xong`, cột E → sản phẩm thật. Sửa bằng openpyxl, rồi **đếm lại** số ô `Xong` và
   đối chiếu với con số viết trong sổ nhật ký.

## Bước 5 — Commit

Tiếng Anh, thân commit nói *vì sao* đã chọn như vậy và cái gì đã được kiểm, không kể
lại diff. Kết thúc bằng dòng `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`.
Soạn trong file tạm ở scratchpad rồi `git commit -F`, đừng nhồi vào `-m` nhiều dòng.

**Không push, không mở PR** nếu đang chạy như agent con — người gọi sẽ gộp cả loạt
vào một PR. Chạy như session chính thì push `graph` và mở PR tiếng Việt.

## Dừng lại và hỏi người dùng khi — và chỉ khi

- Việc cần tài khoản / khoá API không có sẵn (T08 cần CEPII BACI + UN Comtrade).
- Việc cần tải dữ liệu nặng hoặc chạy quá lâu (ví dụ `hs92_country_product_year_4.csv`
  452 MB, ~4,2 giờ).
- Việc thuộc phần người khác đang giữ mà chưa rõ có nên làm hộ (T19–T21 của R3).
- Dữ liệu nói ngược lại điều đề cương đã hứa — đó là tin, không phải lỗi, nhưng
  người dùng cần biết trước khi nó thành một hình.
- `git merge --ff-only` ở bước 0 thất bại, hoặc có xung đột với việc đồng đội đã push.

Ngoài năm trường hợp đó thì tự quyết, làm tiếp, và báo lại một lượt khi xong.

## Báo lại cái gì

Ngắn, và nói bằng kết quả đo được, không bằng tên bước: hình nói điều gì, con số nào
chứng minh, điều gì đã định làm mà dữ liệu bác bỏ, A/B nào mới, file nào đã sửa,
commit nào. Người dùng sẽ dùng đúng đoạn này để lên thuyết trình.

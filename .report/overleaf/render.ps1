<#
.SYNOPSIS
    Biên dịch bản dịch Chương 9 (main.tex) thành PDF bằng XeLaTeX.

.DESCRIPTION
    Tài liệu dùng fontspec + polyglossia tiếng Việt nên BẮT BUỘC biên dịch bằng
    XeLaTeX. Chạy pdflatex sẽ lỗi font và mất dấu tiếng Việt.

    Script ưu tiên dùng latexmk vì nó tự động chạy lại đủ số lần cần thiết để
    mục lục và các tham chiếu chéo (\ref) hội tụ. Nếu máy không có latexmk,
    script tự chuyển sang gọi xelatex 3 lượt.

.PARAMETER File
    Tên file .tex cần biên dịch. Mặc định: main.tex

.PARAMETER Clean
    Xóa các file trung gian (.aux, .log, .toc, .out, .fls, .fdb_latexmk)
    sau khi biên dịch xong. Giữ lại file PDF.

.PARAMETER Open
    Mở file PDF ngay sau khi biên dịch thành công.

.PARAMETER Force
    Ép biên dịch lại từ đầu, kể cả khi latexmk cho rằng không có gì thay đổi.
    Dùng khi PDF trông có vẻ không khớp với file .tex.

.EXAMPLE
    .\render.ps1
    Biên dịch main.tex thành main.pdf

.EXAMPLE
    .\render.ps1 -Clean -Open
    Biên dịch, dọn file rác, rồi mở PDF

.EXAMPLE
    .\render.ps1 -File section_1.tex
    Chỉ biên dịch riêng phần 9.1
#>

param(
    [string]$File = "main.tex",
    [switch]$Clean,
    [switch]$Open,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

# Cho phép hiển thị tiếng Việt có dấu trên console
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

function Write-Step  ([string]$m) { Write-Host "==> $m" -ForegroundColor Cyan }
function Write-Ok    ([string]$m) { Write-Host "OK  $m" -ForegroundColor Green }
function Write-Fail  ([string]$m) { Write-Host "LỖI $m" -ForegroundColor Red }
function Write-Note  ([string]$m) { Write-Host "    $m" -ForegroundColor DarkGray }

# Luôn làm việc trong thư mục chứa script, không phụ thuộc chỗ người dùng đang đứng
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Push-Location $root

try {
    # -----------------------------------------------------------------
    # 1. Kiểm tra đầu vào
    # -----------------------------------------------------------------
    if (-not (Test-Path $File)) {
        Write-Fail "Không tìm thấy '$File' trong $root"
        Write-Note "Các file .tex hiện có:"
        Get-ChildItem -Filter *.tex | ForEach-Object { Write-Note "  - $($_.Name)" }
        exit 1
    }

    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($File)
    $pdfPath  = Join-Path $root "$baseName.pdf"
    $logPath  = Join-Path $root "$baseName.log"

    # -----------------------------------------------------------------
    # 2. Kiểm tra công cụ biên dịch
    # -----------------------------------------------------------------
    $xelatex = Get-Command xelatex -ErrorAction SilentlyContinue
    if ($null -eq $xelatex) {
        Write-Fail "Không tìm thấy xelatex trong PATH."
        Write-Note "Cài MiKTeX (https://miktex.org/download) hoặc TeX Live,"
        Write-Note "rồi mở lại terminal để PATH được nạp lại."
        Write-Note "Hoặc biên dịch trực tiếp trên Overleaf: Menu > Compiler > XeLaTeX."
        exit 1
    }

    $latexmk = Get-Command latexmk -ErrorAction SilentlyContinue

    # KHÔNG xóa PDF cũ trước khi build: nếu build hỏng giữa chừng thì bản PDF
    # cũ vẫn còn đó để dùng tạm, thay vì mất trắng.

    # -----------------------------------------------------------------
    # 3. Biên dịch
    # -----------------------------------------------------------------
    $started = Get-Date

    if ($null -ne $latexmk) {
        Write-Step "Biên dịch '$File' bằng latexmk + XeLaTeX..."
        # latexmk theo dõi thay đổi bằng hash nội dung, không phải timestamp.
        # Nếu không có gì đổi nó sẽ báo "Nothing to do" và trả về 0 — đó là
        # thành công, PDF hiện có chính là bản mới nhất. Dùng -g để ép build lại.
        if ($Force) {
            & latexmk -g -xelatex -interaction=nonstopmode -file-line-error $File
        }
        else {
            & latexmk -xelatex -interaction=nonstopmode -file-line-error $File
        }
        $buildCode = $LASTEXITCODE
    }
    else {
        Write-Step "Không có latexmk — gọi xelatex 3 lượt để mục lục hội tụ..."
        for ($i = 1; $i -le 3; $i++) {
            Write-Note "lượt $i/3"
            & xelatex -interaction=nonstopmode -file-line-error $File | Out-Null
        }
        # xelatex trả mã khác 0 cả với lỗi đã phục hồi được, nên ở nhánh này
        # chỉ dựa vào việc file PDF có được sinh ra hay không.
        $buildCode = 0
    }

    $elapsed = [math]::Round(((Get-Date) - $started).TotalSeconds, 1)

    # -----------------------------------------------------------------
    # 4. Kiểm tra kết quả
    # -----------------------------------------------------------------
    $pdfOk = (Test-Path $pdfPath) -and ($buildCode -eq 0)

    if (-not $pdfOk) {
        if (Test-Path $pdfPath) {
            Write-Fail "Biên dịch lỗi (mã $buildCode) — '$baseName.pdf' có thể không phải bản mới nhất."
            Write-Note "PDF hiện tại từ $((Get-Item $pdfPath).LastWriteTime) vẫn được giữ nguyên."
        }
        else {
            Write-Fail "Biên dịch thất bại — không sinh ra '$baseName.pdf'."
        }
        if (Test-Path $logPath) {
            Write-Note ""
            Write-Note "Các lỗi tìm thấy trong $baseName.log:"
            Get-Content $logPath |
                Select-String -Pattern '^!|^[^:]+:\d+:' |
                Select-Object -First 15 |
                ForEach-Object { Write-Host "    $_" -ForegroundColor Yellow }
            Write-Note ""
            Write-Note "Xem log đầy đủ: $logPath"
        }
        exit 1
    }

    $sizeKb = [math]::Round((Get-Item $pdfPath).Length / 1KB, 1)
    Write-Ok "Đã tạo $baseName.pdf ($sizeKb KB) trong $elapsed giây"
    Write-Note $pdfPath

    # Cảnh báo tham chiếu chưa hội tụ — hay gặp khi chỉ chạy xelatex 1 lượt
    if (Test-Path $logPath) {
        $undef = Get-Content $logPath | Select-String -Pattern 'LaTeX Warning: (Reference|Citation).*undefined'
        if ($undef.Count -gt 0) {
            Write-Host "CẢNH BÁO: còn $($undef.Count) tham chiếu chưa hội tụ — chạy lại script lần nữa." -ForegroundColor Yellow
        }
    }

    # -----------------------------------------------------------------
    # 5. Dọn file trung gian (tùy chọn)
    # -----------------------------------------------------------------
    if ($Clean) {
        Write-Step "Dọn file trung gian..."
        if ($null -ne $latexmk) {
            & latexmk -c $File | Out-Null
        }
        else {
            $exts = @("aux", "log", "toc", "out", "fls", "fdb_latexmk", "synctex.gz", "lof", "lot")
            foreach ($e in $exts) {
                $f = Join-Path $root "$baseName.$e"
                if (Test-Path $f) { Remove-Item $f -Force }
            }
        }
        Write-Ok "Đã dọn xong (giữ lại PDF)"
    }

    # -----------------------------------------------------------------
    # 6. Mở PDF (tùy chọn)
    # -----------------------------------------------------------------
    if ($Open) {
        Write-Step "Đang mở PDF..."
        Invoke-Item $pdfPath
    }
}
finally {
    Pop-Location
}

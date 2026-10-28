"""Đối chiếu chênh lệch gương trong số liệu thương mại song phương (T08).

Vì sao KHÔNG dùng BACI và Comtrade
----------------------------------
Phân công ban đầu ghi "đối chiếu 3–5 luồng giữa Atlas, BACI và Comtrade". Nhưng
quyết định B9 đã chốt dùng Atlas, và checklist nộp bài mục 17 tự ghi ra lý do:
**Atlas và BACI đều DẪN XUẤT từ UN Comtrade**. Ba cái tên đó không phải ba nguồn
độc lập — chúng là ba bản xử lý của cùng một gốc. Đối chiếu chúng với nhau chỉ đo
được chênh lệch do thuật toán làm sạch, không đo được độ tin cậy của số liệu gốc.
Trình bày nó như "ba nguồn độc lập đều khớp" là một tuyên bố sai.

Phép kiểm thật sự nằm ngay trong dữ liệu đang có. Mỗi luồng hàng A→B được khai
báo HAI LẦN bởi hai cơ quan hải quan khác nhau:

    - A khai: "tôi xuất sang B x USD"      -> cc_year(A, B).export_value
    - B khai: "tôi nhập từ A y USD"        -> cc_year(B, A).import_value

Hai con số đo CÙNG MỘT dòng hàng. Chênh lệch giữa chúng gọi là *chênh lệch gương*
(mirror discrepancy), và nó là thước đo độc lập thật sự, vì hai bên không chép số
của nhau. Đây là phép kiểm tiêu chuẩn trong thống kê thương mại quốc tế.

Chênh lệch đó KHÔNG phải lỗi. Có ba nguyên nhân hệ thống:

1. **FOB so với CIF.** Nước xuất khai theo giá FOB (hàng lên tàu ở cảng đi).
   Nước nhập khai theo giá CIF (đã gồm cước vận tải và phí bảo hiểm). Nên số
   nhập khẩu LUÔN có xu hướng lớn hơn số xuất khẩu của cùng dòng hàng, thường
   5–10%. Khoảng cách này lớn hơn với hàng nặng đi xa, nhỏ hơn với hàng nhẹ giá
   trị cao.
2. **Quy tắc nước xuất xứ so với nước gửi hàng.** Hàng Trung Quốc trung chuyển
   qua Hồng Kông: Trung Quốc ghi là xuất sang Hồng Kông, nước đến cuối ghi là
   nhập từ Trung Quốc. Cùng một dòng hàng, hai cặp nước khác nhau.
3. **Thời điểm ghi nhận.** Hàng rời cảng tháng 12 và cập cảng tháng 1 được hai
   bên ghi vào hai năm khác nhau.

Script này đo chênh lệch đó, xếp theo độ lớn, và tách ra phần giải thích được
bằng FOB/CIF khỏi phần không giải thích được.

Chạy
----
    python src/compare_mirror.py
    python src/compare_mirror.py --year 2015
    python src/compare_mirror.py --top 10
    python src/compare_mirror.py --min-flow 0     # mọi luồng, không lọc theo cỡ
    python src/compare_mirror.py --all-years      # tóm tắt mọi năm trong file

Xuất ra ``data/processed/mirror_gap_<năm>.csv`` — một dòng cho mỗi luồng được xét.

Phân biệt hai tầng kết luận
---------------------------
Script chỉ ĐO được một điều: hai bản khai của cùng một luồng có trùng khít hay
không. Còn LÝ DO trùng khít (nhà phát hành hòa giải, hay cột nhập được dựng từ
cột xuất của đối tác) thì dữ liệu này không phân biệt nổi. Output và tài liệu
phải giữ ranh giới đó.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import reference_data as R  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, "data", "atlas")
OUT = os.path.join(ROOT, "data", "processed")

# Dải FOB/CIF coi là giải thích được. Cước vận tải và bảo hiểm trên thương mại
# đường biển quốc tế rơi vào khoảng này; IMF dùng mức quy ước 6% khi phải ước
# lượng. Ngoài dải này thì FOB/CIF một mình không giải thích nổi.
CIF_LOW, CIF_HIGH = 0.0, 15.0

# Luồng nhỏ thì tỷ lệ chênh lệch dao động rất mạnh mà không có ý nghĩa gì —
# một lô hàng lẻ ghi lệch năm là đủ làm sai 100%. Mặc định chỉ xét luồng đủ lớn;
# chạy --min-flow 0 để chứng minh việc lọc không che giấu gì.
MIN_FLOW = 1e9

# Ngưỡng kết luận theo tỷ lệ luồng trùng khít (mẫu số = MỌI luồng được xét, kể cả
# luồng không có số đối ứng). Giữa hai ngưỡng thì không kết luận.
SYMMETRIC_MIN = 0.99     # từ mức này: hai bản khai đối xứng, phép kiểm vô hiệu
INDEPENDENT_MAX = 0.05   # đến mức này: còn hai bản khai độc lập, phép kiểm dùng được
IDENTICAL_PCT = 0.01     # |lệch| dưới mức này (%) coi là trùng khít


def log(msg):
    print(msg)
    sys.stdout.flush()


def load_pairs(years=None):
    """Đọc cc_year.csv một lượt, trả về {năm: {(A, B): (A khai xuất, A khai nhập)}}.

    ``years`` là tập năm cần giữ; None nghĩa là giữ mọi năm.
    """
    path = os.path.join(ATLAS, "cc_year.csv")
    if not os.path.exists(path):
        sys.exit("Thiếu %s. Chạy: python src/download_atlas.py --only cc_year.csv"
                 % path)

    by_year = {}
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            year = int(r["year"])
            if years is not None and year not in years:
                continue
            a = r["country_iso3_code"].strip()
            b = r["partner_iso3_code"].strip()
            # Bỏ mã không phải quốc gia: USP (vùng đặc biệt), ANS (không rõ
            # nước). Chúng là nơi dồn phần dư, không có cơ quan hải quan nào
            # khai báo đối ứng nên không có số gương để so.
            if a in R.NON_COUNTRY or b in R.NON_COUNTRY:
                continue
            try:
                exp = float(r["export_value"] or 0)
                imp = float(r["import_value"] or 0)
            except ValueError:
                continue
            by_year.setdefault(year, {})[(a, b)] = (exp, imp)
    return by_year


def mirror_rows(pairs, min_flow=MIN_FLOW):
    """Ghép mỗi luồng A→B với số đối ứng B khai, trả về danh sách đã tính lệch.

    Luồng A→B có hai người khai:
        - A khai xuất  = pairs[(A, B)][0]
        - B khai nhập  = pairs[(B, A)][1]

    Mỗi dòng mang ``status``: ``paired`` (so được), ``no_mirror`` (B không khai
    gì về A) hoặc ``importer_zero`` (B khai nhập 0). Hai trạng thái sau KHÔNG bị
    loại khỏi thống kê — chúng là mismatch lớn nhất có thể có.
    """
    rows = []
    for (a, b), (exp_ab, _) in pairs.items():
        if exp_ab <= 0 or exp_ab < min_flow:
            continue
        back = pairs.get((b, a))
        base = {"source": a, "target": b, "exporter_says": exp_ab}
        if back is None:
            rows.append(dict(base, importer_says=None, gap_pct=None,
                             status="no_mirror"))
            continue
        imp_ba = back[1]
        if imp_ba <= 0:
            rows.append(dict(base, importer_says=0.0, gap_pct=None,
                             status="importer_zero"))
            continue
        # Dấu dương = nước nhập khai CAO HƠN nước xuất, tức chiều mà FOB/CIF
        # dự đoán. Lấy số nước xuất làm mẫu số vì đó là trọng số cạnh của đồ án.
        rows.append(dict(base, importer_says=imp_ba, status="paired",
                         gap_pct=(imp_ba - exp_ab) / exp_ab * 100.0))
    return rows


def is_identical(r):
    return r["status"] == "paired" and abs(r["gap_pct"]) < IDENTICAL_PCT


def verdict_on_symmetry(rows):
    """Tỷ lệ trùng khít trên MỌI luồng xét -> (tỷ lệ, nhãn kết luận)."""
    if not rows:
        return 0.0, "empty"
    share = sum(is_identical(r) for r in rows) / len(rows)
    if share >= SYMMETRIC_MIN:
        return share, "symmetric"
    if share <= INDEPENDENT_MAX:
        return share, "independent"
    return share, "mixed"


def classify(gap):
    """Chênh lệch này do đâu?

    Lệch đúng 0 KHÔNG phải "FOB/CIF giải thích được" — FOB/CIF luôn tạo ra một
    khoảng cách dương. Lệch đúng 0 nghĩa là hai bản khai đối xứng tuyệt đối, tức
    là không còn bản khai thứ hai độc lập để kiểm. Phải tách hai trường hợp này,
    nếu không bảng xếp loại sẽ báo "100% giải thích được" trong khi thực tế là
    "100% không còn gì để kiểm". (Vì sao đối xứng thì dữ liệu không nói.)
    """
    if gap is None:
        return "khong co so guong"
    if abs(gap) < IDENTICAL_PCT:
        return "trung khit — doi xung tuyet doi, khong con so doc lap"
    if CIF_LOW < gap <= CIF_HIGH:
        return "FOB/CIF giai thich duoc"
    if gap > CIF_HIGH:
        return "nuoc nhap khai cao hon nhieu"
    return "nuoc nhap khai THAP hon"


def name(iso):
    return R.COUNTRY_VI.get(iso, (iso,))[0]


def table(rows, title, note=""):
    log("")
    log(title)
    if note:
        log("  %s" % note)
    log("  %-28s %16s %16s %9s" % ("Luồng", "Nước xuất khai", "Nước nhập khai",
                                   "Lệch"))
    log("  " + "-" * 72)
    for r in rows:
        flow = "%s → %s" % (name(r["source"]), name(r["target"]))
        if r["gap_pct"] is None:
            got = "—" if r["importer_says"] is None else R.fmt_usd(r["importer_says"])
            log("  %-28s %16s %16s %9s"
                % (flow[:28], R.fmt_usd(r["exporter_says"]), got, "—"))
        else:
            log("  %-28s %16s %16s %9s"
                % (flow[:28], R.fmt_usd(r["exporter_says"]),
                   R.fmt_usd(r["importer_says"]),
                   R.fmt_pct(r["gap_pct"])))


def percentile(sorted_vals, q):
    """Phân vị theo nội suy tuyến tính. Không dùng numpy để script chạy trần."""
    if not sorted_vals:
        return float("nan")
    pos = (len(sorted_vals) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(sorted_vals) - 1)
    frac = pos - lo
    return sorted_vals[lo] * (1 - frac) + sorted_vals[hi] * frac


VERDICT_LINES = {
    "symmetric": (
        "Hai bản khai ĐỐI XỨNG tuyệt đối: phép kiểm gương KHÔNG dùng được.",
        "Dữ liệu không cho biết vì sao đối xứng (nhà phát hành hòa giải, hay cột",
        "nhập được dựng từ cột xuất của đối tác). Đó là phần giải thích, không",
        "phải phần đo; muốn khẳng định phải dẫn tài liệu của nhà phát hành.",
    ),
    "independent": (
        "Hai bản khai ĐỘC LẬP nhau: phép kiểm gương dùng được.",
    ),
    "mixed": (
        "Tỷ lệ trùng khít ở khoảng giữa hai ngưỡng: KHÔNG kết luận.",
        "Đọc phân bố bên dưới và xem từng luồng.",
    ),
    "empty": ("Không có luồng nào để xét.",),
}


def all_years_summary(by_year, min_flow):
    log("")
    log("%-6s %9s %10s %12s %10s  %s"
        % ("Năm", "Luồng xét", "Không đối", "Nhập khai 0", "Trùng khít",
           "Kết luận"))
    log("  " + "-" * 70)
    for year in sorted(by_year):
        rows = mirror_rows(by_year[year], min_flow)
        share, tag = verdict_on_symmetry(rows)
        log("%-6d %9d %10d %12d %10s  %s"
            % (year, len(rows),
               sum(r["status"] == "no_mirror" for r in rows),
               sum(r["status"] == "importer_zero" for r in rows),
               R.fmt_pct(share * 100), tag))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--top", type=int, default=5,
                    help="số luồng lớn nhất đưa vào bảng (mặc định 5)")
    ap.add_argument("--min-flow", type=float, default=MIN_FLOW,
                    help="chỉ xét luồng xuất khai từ mức này (USD); 0 = mọi luồng")
    ap.add_argument("--all-years", action="store_true",
                    help="chỉ in bảng tóm tắt mọi năm trong file, không ghi CSV")
    args = ap.parse_args()

    log("=" * 76)
    log("CHÊNH LỆCH GƯƠNG TRONG SỐ LIỆU SONG PHƯƠNG — năm %d (T08)" % args.year)
    log("=" * 76)

    log("")
    log("Đọc cc_year.csv...")
    if args.all_years:
        by_year = load_pairs()
        log("  %d năm trong file; xét luồng từ %s trở lên"
            % (len(by_year), R.fmt_usd(args.min_flow)))
        all_years_summary(by_year, args.min_flow)
        return
    pairs = load_pairs({args.year}).get(args.year, {})
    log("  %d cặp nước có số liệu năm %d" % (len(pairs), args.year))

    rows = mirror_rows(pairs, args.min_flow)
    log("  %d luồng từ %s trở lên — chỉ xét những luồng này"
        % (len(rows), R.fmt_usd(args.min_flow)))

    paired = [r for r in rows if r["status"] == "paired"]
    no_mirror = [r for r in rows if r["status"] == "no_mirror"]
    imp_zero = [r for r in rows if r["status"] == "importer_zero"]
    log("  %d luồng có số gương đối ứng; %d luồng đối tác không khai gì; "
        "%d luồng đối tác khai nhập 0" % (len(paired), len(no_mirror), len(imp_zero)))

    # --- Phát hiện quan trọng nhất: hai bản khai có độc lập không? ----------
    # Mẫu số là MỌI luồng xét. Luồng thiếu đối ứng tính là "không trùng khít",
    # nghĩa là chúng chỉ có thể làm kết luận "đối xứng" khó đạt hơn.
    identical = [r for r in rows if is_identical(r)]
    share, tag = verdict_on_symmetry(rows)
    log("")
    log("CÂU HỎI ĐẦU TIÊN: hai bản khai của một luồng có còn độc lập với nhau không?")
    log("  ĐO ĐƯỢC: %d / %d luồng (%s) có hai số TRÙNG KHÍT nhau"
        % (len(identical), len(rows), R.fmt_pct(share * 100)))
    log("  KẾT LUẬN (ngưỡng: đối xứng từ %s, độc lập đến %s):"
        % (R.fmt_pct(SYMMETRIC_MIN * 100), R.fmt_pct(INDEPENDENT_MAX * 100)))
    for n, line in enumerate(VERDICT_LINES[tag]):
        log(("  -> " if n == 0 else "     ") + line)

    # --- Phân bố chênh lệch ------------------------------------------------
    gaps = sorted(r["gap_pct"] for r in paired)
    if gaps:
        log("")
        log("Phân bố chênh lệch (nước nhập khai cao hơn nước xuất bao nhiêu %):")
        for q, lab in ((0.10, "phân vị 10"), (0.25, "phân vị 25"),
                       (0.50, "TRUNG VỊ   "), (0.75, "phân vị 75"),
                       (0.90, "phân vị 90")):
            log("  %s  %s" % (lab, R.fmt_pct(percentile(gaps, q))))
        log("  nhỏ nhất   %s" % R.fmt_pct(gaps[0]))
        log("  lớn nhất   %s" % R.fmt_pct(gaps[-1]))

    if rows:
        buckets = {}
        for r in rows:
            r["verdict"] = classify(r["gap_pct"])
            buckets[r["verdict"]] = buckets.get(r["verdict"], 0) + 1
        log("")
        log("Xếp loại theo nguyên nhân (mẫu số: mọi luồng xét):")
        for k, v in sorted(buckets.items(), key=lambda kv: -kv[1]):
            log("  %-32s %4d luồng (%s)"
                % (k, v, R.fmt_pct(v / len(rows) * 100)))

    # --- Bảng 1: năm luồng lớn nhất thế giới -------------------------------
    big = sorted(rows, key=lambda r: -r["exporter_says"])[:args.top]
    table(big, "BẢNG 1 — %d luồng thương mại lớn nhất thế giới năm %d"
               % (args.top, args.year),
          "Đây là các luồng mà phân công yêu cầu đối chiếu.")

    # --- Bảng 2: các luồng của Việt Nam ------------------------------------
    vnm = sorted([r for r in rows if r["source"] == "VNM"],
                 key=lambda r: -r["exporter_says"])[:args.top]
    table(vnm, "BẢNG 2 — %d thị trường xuất khẩu lớn nhất của Việt Nam" % args.top,
          "Luồng của riêng nước trọng tâm, vì báo cáo nói về Việt Nam.")

    # --- Bảng 3: lệch nặng nhất --------------------------------------------
    # Luồng đối tác khai nhập 0 là lệch nặng nhất có thể có (100% số nước xuất),
    # nên xếp lên đầu. Luồng không có đối ứng nào thì không có số để lệch.
    # Chỉ in bảng khi thật sự CÓ luồng lệch: nếu mọi luồng đều lệch 0 thì "năm
    # luồng lệch nặng nhất" chỉ là năm dòng đầu theo thứ tự alphabet — một bảng
    # trông như có phát hiện nhưng không chứa phát hiện nào.
    def severity(r):
        return 100.0 if r["status"] == "importer_zero" else abs(r["gap_pct"])

    real = [r for r in rows if r["status"] == "importer_zero"
            or (r["status"] == "paired" and not is_identical(r))]
    if real:
        worst = sorted(real, key=lambda r: -severity(r))[:args.top]
        table(worst, "BẢNG 3 — %d luồng lệch nặng nhất (trong các luồng xét)"
                     % args.top,
              "Nếu có luồng nào lệch mạnh, nó nằm ở đây.")
    else:
        log("")
        log("BẢNG 3 — bỏ, vì không có luồng nào lệch khác 0.")
        log("  Không in bảng \"lệch nặng nhất\" khi mọi luồng đều lệch 0: bảng đó")
        log("  sẽ chỉ là mấy dòng đầu theo thứ tự alphabet, trông như phát hiện")
        log("  nhưng không phải.")

    # --- Ghi file ----------------------------------------------------------
    # Tên file mang năm (và mức lọc nếu khác mặc định) để lần chạy đối chứng
    # không ghi đè bằng chứng của lần chạy chính.
    os.makedirs(OUT, exist_ok=True)
    suffix = "" if args.min_flow == MIN_FLOW else "_min%g" % args.min_flow
    path = os.path.join(OUT, "mirror_gap_%d%s.csv" % (args.year, suffix))
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["source_iso3", "target_iso3", "year", "exporter_reports",
                    "importer_reports", "gap_pct", "status", "verdict"])
        for r in sorted(rows, key=lambda x: -x["exporter_says"]):
            w.writerow([r["source"], r["target"], args.year,
                        repr(r["exporter_says"]),
                        "" if r["importer_says"] is None else repr(r["importer_says"]),
                        "" if r["gap_pct"] is None else "%.4f" % r["gap_pct"],
                        r["status"], r["verdict"]])
    log("")
    log("-> %s  (%d dòng)" % (path, len(rows)))

    # --- Kết luận cho phần Phương pháp luận --------------------------------
    log("")
    log("=" * 76)
    log("KẾT LUẬN ĐỂ VIẾT VÀO PHƯƠNG PHÁP LUẬN (T25)")
    log("=" * 76)
    if tag == "symmetric":
        log("Đo được: %s các luồng xét (%d/%d) có hai bản khai trùng khít; %d luồng"
            % (R.fmt_pct(share * 100), len(identical), len(rows),
               len(no_mirror) + len(imp_zero)))
        log("thiếu đối ứng hoặc nhập khai 0.")
        log("Hệ quả thẳng thắn: bộ dữ liệu này KHÔNG cho ta tự đo sai số của nó.")
        log("Không được nói 'đã đối chiếu ba nguồn và chúng khớp nhau' — ba cái")
        log("tên Atlas / BACI / Comtrade là ba bản xử lý của cùng một gốc Comtrade.")
        log("Phải nói: 'hai bản khai trong số liệu đối xứng tuyệt đối, nhất quán")
        log("với việc đã được hòa giải trước khi phát hành; chúng tôi dùng số đó")
        log("và không có nguồn độc lập để kiểm chéo.' Ai hòa giải thì dữ liệu")
        log("không nói; chỉ khẳng định khi đã dẫn tài liệu của nhà phát hành.")
    elif tag == "independent":
        log("Hai bản khai độc lập, nên đo được chênh lệch gương thật sự.")
        log("Trung vị %s — nằm %s dải FOB/CIF (%s–%s)."
            % (R.fmt_pct(percentile(gaps, 0.5)),
               "trong" if CIF_LOW <= percentile(gaps, 0.5) <= CIF_HIGH else "ngoài",
               R.fmt_pct(CIF_LOW), R.fmt_pct(CIF_HIGH)))
    else:
        log("Không kết luận: tỷ lệ trùng khít %s nằm giữa hai ngưỡng."
            % R.fmt_pct(share * 100))
    log("")


if __name__ == "__main__":
    main()

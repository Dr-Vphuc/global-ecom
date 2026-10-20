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

Xuất ra ``data/processed/mirror_gap.csv`` — một dòng cho mỗi luồng được xét.
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
# một lô hàng lẻ ghi lệch năm là đủ làm sai 100%. Chỉ xét luồng đủ lớn.
MIN_FLOW = 1e9


def log(msg):
    print(msg)
    sys.stdout.flush()


def load_pairs(year):
    """Đọc cc_year.csv, trả về dict (A, B) -> (A khai xuất, A khai nhập)."""
    path = os.path.join(ATLAS, "cc_year.csv")
    if not os.path.exists(path):
        sys.exit("Thiếu %s. Chạy: python src/download_atlas.py --only cc_year.csv"
                 % path)

    pairs = {}
    with open(path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if int(r["year"]) != year:
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
            pairs[(a, b)] = (exp, imp)
    return pairs


def mirror_rows(pairs):
    """Ghép mỗi luồng A→B với số đối ứng B khai, trả về danh sách đã tính lệch.

    Luồng A→B có hai người khai:
        - A khai xuất  = pairs[(A, B)][0]
        - B khai nhập  = pairs[(B, A)][1]
    """
    rows = []
    for (a, b), (exp_ab, _) in pairs.items():
        if exp_ab < MIN_FLOW:
            continue
        back = pairs.get((b, a))
        if back is None:
            # B không khai gì về A — không có số gương, ghi riêng để đếm.
            rows.append({"source": a, "target": b, "exporter_says": exp_ab,
                         "importer_says": None, "gap_pct": None})
            continue
        imp_ba = back[1]
        if imp_ba <= 0:
            rows.append({"source": a, "target": b, "exporter_says": exp_ab,
                         "importer_says": 0.0, "gap_pct": None})
            continue
        # Dấu dương = nước nhập khai CAO HƠN nước xuất, tức chiều mà FOB/CIF
        # dự đoán. Lấy số nước xuất làm mẫu số vì đó là trọng số cạnh của đồ án.
        rows.append({"source": a, "target": b, "exporter_says": exp_ab,
                     "importer_says": imp_ba,
                     "gap_pct": (imp_ba - exp_ab) / exp_ab * 100.0})
    return rows


def classify(gap):
    """Chênh lệch này do đâu?

    Lệch đúng 0 KHÔNG phải "FOB/CIF giải thích được" — FOB/CIF luôn tạo ra một
    khoảng cách dương. Lệch đúng 0 nghĩa là số liệu đã bị hòa giải thành một
    con số duy nhất trước khi phát hành, tức là mất bản khai thứ hai. Phải tách
    hai trường hợp này, nếu không bảng xếp loại sẽ báo "100% giải thích được"
    trong khi thực tế là "100% không còn gì để kiểm".
    """
    if gap is None:
        return "khong co so guong"
    if abs(gap) < 0.01:
        return "trung khit — da hoa giai, khong con so doc lap"
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


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", type=int, default=R.REFERENCE_YEAR)
    ap.add_argument("--top", type=int, default=5,
                    help="số luồng lớn nhất đưa vào bảng (mặc định 5)")
    args = ap.parse_args()

    log("=" * 76)
    log("CHÊNH LỆCH GƯƠNG TRONG SỐ LIỆU SONG PHƯƠNG — năm %d (T08)" % args.year)
    log("=" * 76)

    log("")
    log("Đọc cc_year.csv...")
    pairs = load_pairs(args.year)
    log("  %d cặp nước có số liệu năm %d" % (len(pairs), args.year))

    rows = mirror_rows(pairs)
    log("  %d luồng từ %s trở lên — chỉ xét những luồng này"
        % (len(rows), R.fmt_usd(MIN_FLOW)))

    paired = [r for r in rows if r["gap_pct"] is not None]
    orphan = [r for r in rows if r["gap_pct"] is None]
    log("  %d luồng có số gương đối ứng, %d luồng không có"
        % (len(paired), len(orphan)))

    # --- Phát hiện quan trọng nhất: Atlas đã hòa giải số liệu hay chưa? -----
    identical = [r for r in paired if abs(r["gap_pct"]) < 0.01]
    log("")
    log("CÂU HỎI ĐẦU TIÊN: Atlas giữ cả hai bản khai, hay đã hòa giải thành một số?")
    log("  %d / %d luồng (%s) có hai số TRÙNG KHÍT nhau"
        % (len(identical), len(paired),
           R.fmt_pct(len(identical) / len(paired) * 100 if paired else 0)))
    reconciled = len(identical) / len(paired) > 0.5 if paired else False
    if reconciled:
        log("  -> Atlas ĐÃ hòa giải. Hai con số không còn độc lập với nhau,")
        log("     nên phép kiểm gương KHÔNG dùng được trên bộ dữ liệu này.")
        log("     Đây chính là một giới hạn phải ghi vào phần Phương pháp luận:")
        log("     ta KHÔNG thể tự đo sai số của dữ liệu mình đang dùng.")
    else:
        log("  -> Atlas GIỮ cả hai bản khai. Phép kiểm gương dùng được.")

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

        buckets = {}
        for r in paired:
            buckets[classify(r["gap_pct"])] = buckets.get(classify(r["gap_pct"]), 0) + 1
        log("")
        log("Xếp loại theo nguyên nhân:")
        for k, v in sorted(buckets.items(), key=lambda kv: -kv[1]):
            log("  %-32s %4d luồng (%s)"
                % (k, v, R.fmt_pct(v / len(paired) * 100)))

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
    # Chỉ in bảng này khi thật sự CÓ luồng lệch. Nếu mọi luồng đều lệch 0 thì
    # "năm luồng lệch nặng nhất" chỉ là năm dòng đầu theo thứ tự alphabet —
    # một bảng trông như có phát hiện nhưng không chứa phát hiện nào.
    real = [r for r in paired if abs(r["gap_pct"]) >= 0.01]
    if real:
        worst = sorted(real, key=lambda r: -abs(r["gap_pct"]))[:args.top]
        table(worst, "BẢNG 3 — %d luồng lệch nặng nhất (trong các luồng lớn)"
                     % args.top,
              "Nếu có luồng nào lệch mạnh, nó nằm ở đây.")
    else:
        log("")
        log("BẢNG 3 — bỏ, vì không có luồng nào lệch khác 0.")
        log("  Không in bảng \"lệch nặng nhất\" khi mọi luồng đều lệch 0: bảng đó")
        log("  sẽ chỉ là mấy dòng đầu theo thứ tự alphabet, trông như phát hiện")
        log("  nhưng không phải.")

    # --- Ghi file ----------------------------------------------------------
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "mirror_gap.csv")
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["source_iso3", "target_iso3", "year", "exporter_reports",
                    "importer_reports", "gap_pct", "verdict"])
        for r in sorted(rows, key=lambda x: -x["exporter_says"]):
            w.writerow([r["source"], r["target"], args.year,
                        repr(r["exporter_says"]),
                        "" if r["importer_says"] is None else repr(r["importer_says"]),
                        "" if r["gap_pct"] is None else "%.4f" % r["gap_pct"],
                        classify(r["gap_pct"])])
    log("")
    log("-> %s  (%d dòng)" % (path, len(rows)))

    # --- Kết luận cho phần Phương pháp luận --------------------------------
    log("")
    log("=" * 76)
    log("KẾT LUẬN ĐỂ VIẾT VÀO PHƯƠNG PHÁP LUẬN (T25)")
    log("=" * 76)
    if reconciled:
        log("Atlas đã hòa giải số liệu hai chiều trước khi phát hành: %s"
            % R.fmt_pct(len(identical) / len(paired) * 100 if paired else 0)
            + " các luồng lớn có hai bản khai trùng khít.")
        log("Hệ quả thẳng thắn: bộ dữ liệu này KHÔNG cho ta tự đo sai số của nó.")
        log("Không được nói 'đã đối chiếu ba nguồn và chúng khớp nhau' — ba cái")
        log("tên Atlas / BACI / Comtrade là ba bản xử lý của cùng một gốc Comtrade.")
        log("Phải nói: 'số liệu đã được Growth Lab hòa giải theo phương pháp của")
        log("họ; chúng tôi dùng số đó và không có nguồn độc lập để kiểm chéo.'")
    else:
        log("Atlas giữ cả hai bản khai, nên đo được chênh lệch gương thật sự.")
        log("Trung vị %s — nằm %s dải FOB/CIF (%s–%s)."
            % (R.fmt_pct(percentile(gaps, 0.5)),
               "trong" if CIF_LOW <= percentile(gaps, 0.5) <= CIF_HIGH else "ngoài",
               R.fmt_pct(CIF_LOW), R.fmt_pct(CIF_HIGH)))
    log("")


if __name__ == "__main__":
    main()

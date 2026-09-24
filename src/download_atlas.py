# -*- coding: utf-8 -*-
"""Tải dữ liệu thô từ Harvard Dataverse, có nối tiếp và kiểm chứng MD5.

Vì sao cần script này thay vì bấm nút tải trên trình duyệt:
Dataverse công bố kích thước và mã MD5 chính thức cho từng file. Script đọc
đúng hai con số đó rồi đối chiếu với file vừa tải. Nếu đường truyền đứt giữa
chừng — chuyện đã xảy ra với ``cc_year.csv`` và làm mất toàn bộ số liệu xuất
khẩu của Hoa Kỳ, Anh, Ukraine... — script báo sai ngay, thay vì để một file
cụt trôi vào pipeline.

Kết nối tới Dataverse có thể rất chậm (~30 KB/s), nên script tải nối tiếp
(HTTP Range): chạy lại là nó đi tiếp từ chỗ đứt, không tải lại từ đầu.

    python src/download_atlas.py --list     # chỉ xem file nào thiếu/hỏng
    python src/download_atlas.py            # tải những file thiếu hoặc sai MD5
    python src/download_atlas.py --force    # tải lại tất cả

File cũ không bị xóa: nếu sai MD5 nó được đổi tên thành ``*.broken``.

Chỉ dùng thư viện chuẩn.
"""

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "atlas")

API = "https://dataverse.harvard.edu"
# Tuong lua cua Dataverse tra ve 403 cho User-Agent mac dinh cua urllib,
# nen phai dat mot chuoi co tien to Mozilla. Van ghi ro ten du an phia sau.
UA = "Mozilla/5.0 (compatible; global-ecom-coursework/1.0)"
CHUNK = 256 * 1024

# Ten file tren Dataverse  ->  ten file trong data/atlas/
# Hai bo du lieu deu thuoc Atlas of Economic Complexity, Harvard Growth Lab.
DATASETS = [
    ("doi:10.7910/DVN/T4CHWJ", "International Trade Data (HS, 92)", {
        "hs92_country_country_year.csv": "cc_year.csv",
        "hs92_country_product_year_2.csv": "cp_year_hs2.csv",
        # Giu nguyen ten goc de khong lan voi data/processed/country_year.csv.
        # File chi 0,36 MB nhung chua ECI, COI va diversity - bo chi so do dung
        # "vi tri cua Viet Nam", tuc la ve dung cai ten de tai dat ra.
        "hs92_country_year.csv": "hs92_country_year.csv",
        "hs92_data_dictionary.csv": "hs92_data_dictionary.csv",
    }),
    ("doi:10.7910/DVN/3BAL1O", "Classifications Data", {
        "location_country.csv": "location_country.csv",
        "product_hs92.csv": "product_hs92.csv",
    }),
]


def log(msg):
    print(msg, flush=True)


def human(n):
    return "%.1f MB" % (n / 1e6) if n >= 1e6 else "%.1f KB" % (n / 1e3)


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fetch_metadata(doi):
    """Lay danh sach file + kich thuoc + MD5 chinh thuc cua mot bo du lieu."""
    url = "%s/api/datasets/:persistentId/?persistentId=%s" % (API, doi)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    out = {}
    for f in data["data"]["latestVersion"]["files"]:
        df = f["dataFile"]
        out[df["filename"]] = {
            "id": df["id"],
            "size": df["filesize"],
            "md5": df["checksum"]["value"].lower(),
        }
    return out


def download(file_id, dest, size, md5, tries=8):
    """Tai noi tiep. Tra ve True neu file cuoi cung dung MD5."""
    url = "%s/api/access/datafile/%d" % (API, file_id)
    part = dest + ".part"

    for attempt in range(1, tries + 1):
        have = os.path.getsize(part) if os.path.exists(part) else 0
        if have >= size:
            break
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        mode = "wb"
        if have:
            req.add_header("Range", "bytes=%d-" % have)
            mode = "ab"
            log("      noi tiep tu %s (lan %d/%d)" % (human(have), attempt, tries))
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                # May chu co the lo di header Range -> phai tai lai tu dau.
                if have and resp.getcode() != 206:
                    log("      may chu khong ho tro noi tiep, tai lai tu dau")
                    have, mode = 0, "wb"
                t0, last = time.time(), have
                with open(part, mode) as fh:
                    while True:
                        block = resp.read(CHUNK)
                        if not block:
                            break
                        fh.write(block)
                        have += len(block)
                        if have - last >= 2_000_000:
                            last = have
                            rate = (have / (time.time() - t0 + 1e-9)) / 1e3
                            sys.stdout.write("\r      %s / %s  (%.0f KB/s)   "
                                             % (human(have), human(size), rate))
                            sys.stdout.flush()
                sys.stdout.write("\r" + " " * 60 + "\r")
        except (urllib.error.URLError, OSError, ConnectionError) as exc:
            log("      dut ket noi: %s" % exc)
            time.sleep(min(2 ** attempt, 30))
            continue

    if not os.path.exists(part):
        log("      KHONG tai duoc gi")
        return False

    got_size = os.path.getsize(part)
    if got_size != size:
        log("      SAI KICH THUOC: %d byte, mong doi %d (thieu %s)"
            % (got_size, size, human(size - got_size)))
        log("      -> chay lai lenh nay, script se tai tiep tu cho dut")
        return False

    got_md5 = md5_of(part)
    if got_md5 != md5:
        log("      SAI MD5: %s, mong doi %s" % (got_md5, md5))
        log("      -> file hong. Xoa %s roi tai lai." % os.path.basename(part))
        return False

    if os.path.exists(dest):
        broken = dest + ".broken"
        if os.path.exists(broken):
            os.remove(broken)
        os.rename(dest, broken)
        log("      file cu doi ten -> %s" % os.path.basename(broken))
    os.replace(part, dest)
    log("      OK  %s  md5 khop" % human(size))
    return True


def status(dest, meta):
    """Tra ve 'OK' / 'THIEU' / 'SAI' ma khong tai gi."""
    if not os.path.exists(dest):
        return "THIEU", ""
    got = os.path.getsize(dest)
    if got != meta["size"]:
        return "SAI", "%d byte, mong doi %d -> thieu %s" % (
            got, meta["size"], human(meta["size"] - got))
    if md5_of(dest) != meta["md5"]:
        return "SAI", "dung kich thuoc nhung sai MD5"
    return "OK", human(got)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true",
                    help="chi bao cao tinh trang, khong tai")
    ap.add_argument("--force", action="store_true",
                    help="tai lai ca nhung file dang dung")
    ap.add_argument("--only", metavar="TEN",
                    help="chi xu ly mot file, vd: cc_year.csv")
    args = ap.parse_args()

    os.makedirs(RAW, exist_ok=True)
    log("Thu muc dich: %s\n" % os.path.relpath(RAW, ROOT))

    n_bad = n_done = 0
    for doi, title, wanted in DATASETS:
        log("%s  (%s)" % (title, doi))
        try:
            meta = fetch_metadata(doi)
        except Exception as exc:
            log("  ! khong doc duoc metadata: %s" % exc)
            n_bad += 1
            continue

        for remote, local in sorted(wanted.items()):
            if args.only and args.only not in (remote, local):
                continue
            if remote not in meta:
                log("  ! Dataverse khong con file %s (bo du lieu da doi phien ban?)"
                    % remote)
                n_bad += 1
                continue
            m = meta[remote]
            dest = os.path.join(RAW, local)
            st, note = status(dest, m)
            log("  %-24s %-6s %s" % (local, st, note))

            if args.list:
                if st != "OK":
                    n_bad += 1
                continue
            if st == "OK" and not args.force:
                continue
            log("      tai %s (%s)..." % (remote, human(m["size"])))
            if download(m["id"], dest, m["size"], m["md5"]):
                n_done += 1
            else:
                n_bad += 1
        log("")

    log("=" * 62)
    if args.list:
        if n_bad:
            log("%d file thieu hoac hong. Chay lai khong kem --list de tai." % n_bad)
            return 1
        log("Tat ca file deu dung kich thuoc va dung MD5.")
        return 0
    if n_bad:
        log("Con %d file chua xong. Chay lai lenh nay de tai tiep." % n_bad)
        return 1
    log("Xong (%d file tai moi). Buoc tiep: python src/check_raw_data.py" % n_done)
    return 0


if __name__ == "__main__":
    sys.exit(main())

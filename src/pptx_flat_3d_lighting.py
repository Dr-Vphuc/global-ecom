# -*- coding: utf-8 -*-
"""Gỡ đèn điểm mà PowerPoint tự gắn cho mô hình 3D, và (tuỳ chọn) thay file .glb nằm trong slide bằng bản mới.

PowerPoint bỏ qua ánh sáng trong file .glb và tự gắn cho mỗi mô hình 3D một đèn môi trường (am3d:ambientLight) và ba
đèn điểm (am3d:ptLight), lưu trong ppt/slides/slideN.xml. Ba đèn điểm tạo vùng sáng lóa trên hình cầu; giao diện
PowerPoint không có chỗ nào chỉnh. Cách gỡ theo hướng dẫn của nhóm phát triển 3D của Office: xóa các phần tử
am3d:ptLight trong XML của slide. Đèn môi trường được giữ lại theo mặc định: xóa cả nó thì mô hình chỉ có màu base
(không emissive) sẽ thành đen.

Gỡ đèn chưa đủ: trình vẽ của Office còn có ánh sáng môi trường dựng sẵn không nằm trong XML, làm vật liệu phi kim
bóng như bi crôm. Phần đó phải sửa trong vật liệu của file .glb (xem flat_material trong src/export_cone_tree_glb.py).
Tuỳ chọn --glb thay file .glb trong slide bằng bản mới mà giữ nguyên vị trí, cỡ và góc xoay của mô hình trên slide.

Không ghi đè file gốc: mặc định ghi ra <tên>_flat.pptx bên cạnh. Chỉ dùng thư viện chuẩn.
Chạy: python src/pptx_flat_3d_lighting.py "slide.pptx" [--glb mô_hình.glb] [-o ra.pptx] [--remove-ambient]
"""
from __future__ import print_function

import argparse
import posixpath
import re
import sys
import zipfile
from pathlib import Path

MODEL3D_NS = "http://schemas.microsoft.com/office/drawing/2017/model3d"
MODEL3D_REL = "http://schemas.microsoft.com/office/2017/06/relationships/model3d"
SLIDE = re.compile(r"^ppt/slides/slide\d+\.xml$")


def strip_lights(xml, remove_ambient=False):
    """Xóa phần tử đèn trong một file XML của slide. Trả về (XML mới, số đèn đã xóa)."""
    prefixes = set(re.findall(r'xmlns:([\w.-]+)="%s"' % re.escape(MODEL3D_NS), xml))
    tags = ["ptLight", "ambientLight"] if remove_ambient else ["ptLight"]
    removed = 0
    for p in prefixes:
        for tag in tags:
            name = re.escape("%s:%s" % (p, tag))
            pattern = re.compile(r"<%s\b[^>]*?(?:/>|>.*?</%s>)" % (name, name), re.S)
            xml, n = pattern.subn("", xml)
            removed += n
    return xml, removed


def model_parts(zin, slide):
    """Các file .glb mà slide trỏ tới qua quan hệ model3d, dạng đường dẫn trong zip (ppt/media/...)."""
    rels = posixpath.join(posixpath.dirname(slide), "_rels", posixpath.basename(slide) + ".rels")
    if rels not in zin.namelist():
        return set()
    xml = zin.read(rels).decode("utf-8")
    targets = re.findall(r'<Relationship\b(?=[^>]*Type="%s")[^>]*Target="([^"]+)"' % re.escape(MODEL3D_REL), xml)
    return {posixpath.normpath(posixpath.join(posixpath.dirname(slide), t)) for t in targets}


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("pptx")
    ap.add_argument("--glb", help="file .glb mới thay cho mô hình 3D trong các slide có mô hình")
    ap.add_argument("-o", "--out", help="file ra (mặc định <tên>_flat.pptx)")
    ap.add_argument("--remove-ambient", action="store_true", help="xóa cả đèn môi trường")
    args = ap.parse_args(argv)

    src = Path(args.pptx)
    dst = Path(args.out) if args.out else src.with_name(src.stem + "_flat" + src.suffix)
    if dst.resolve() == src.resolve():
        sys.exit("File ra trùng file gốc; chọn tên khác bằng -o.")
    new_glb = Path(args.glb).read_bytes() if args.glb else None

    with zipfile.ZipFile(src) as zin:
        slides = [n for n in zin.namelist() if SLIDE.match(n) and MODEL3D_NS.encode() in zin.read(n)]
        glbs = set().union(*(model_parts(zin, s) for s in slides)) if new_glb else set()
        lights = 0
        try:
            zout = zipfile.ZipFile(dst, "w")
        except PermissionError:
            sys.exit("Không ghi được %s: file đang mở trong PowerPoint? Đóng file rồi chạy lại." % dst)
        with zout:
            for info in zin.infolist():          # giữ nguyên thứ tự và cách nén của từng phần
                data = zin.read(info.filename)
                if info.filename in slides:
                    xml, n = strip_lights(data.decode("utf-8"), args.remove_ambient)
                    print("%s: xóa %d đèn" % (info.filename, n))
                    data, lights = xml.encode("utf-8"), lights + n
                elif info.filename in glbs:
                    print("%s: thay bằng %s" % (info.filename, args.glb))
                    data = new_glb
                zout.writestr(info, data)
    if not slides:
        dst.unlink()
        print("Không tìm thấy mô hình 3D nào trong %s; không ghi file mới." % src)
        return 1
    print("Đã ghi %s (%d đèn đã xóa, %d mô hình đã thay)." % (dst, lights, len(glbs)))
    print("Mở file rồi xoay mô hình một chút: PowerPoint hiện ảnh đệm cũ cho tới khi vẽ lại.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# -*- coding: utf-8 -*-
"""Xuất cây nón 3D (mục 2 của notebooks/Nhom8_Demo.ipynb) ra file mô hình 3D .glb.

PowerPoint (Microsoft 365: Chèn > Mô hình 3D) nhận .glb, .obj, .fbx, .stl, .3mf, .ply. Chọn .glb vì giữ được màu
vật liệu trong một file duy nhất.

Bố cục lấy đúng từ notebook: ASEAN ở đỉnh, 10 nước trên vòng tròn tầng 1, 10 ngành trên vòng tròn quanh mỗi nước
(mỗi ngành một góc cố định ở mọi nước). Nút là hình cầu: nút nước có bán kính ~ căn bậc hai giá trị xuất khẩu, nút lá
(ngành) cùng một cỡ; lá tô màu ngành theo SECTOR_PALETTE. Mọi cạnh cùng độ dày và màu xám, không tô riêng Việt Nam.
Chỉ có nút và cạnh của đồ thị: không vẽ mặt nón như bản plotly.

Vật liệu không đổ bóng: màu đặt ở emissive, baseColor đen và metallic = 1 nên không phản chiếu đèn hay ánh sáng môi
trường (xem flat_material). Nhãn chữ không có trong file (glTF không có chữ): thêm bằng hộp văn bản trên slide.

Chỉ dùng numpy và pandas. Chạy: python src/export_cone_tree_glb.py [thư_mục_ra]
"""
from __future__ import print_function

import json
import struct
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from reference_data import SECTOR_NAME_VI, SECTOR_PALETTE, REFERENCE_YEAR  # noqa: E402

R1, R2 = 1.0, 0.26             # bán kính đáy nón tầng 1 và tầng 2 (như notebook)
Z0, Z1, Z2 = 0.0, -1.0, -2.0   # độ cao của gốc, tầng nước, tầng ngành
# Bán kính nút (đơn vị mô hình, R1 = 1). Nút phải to hơn hẳn cạnh thì trên slide mới thấy nút; nút lá nhỏ hơn nửa
# khoảng cách giữa hai lá liền kề (2π·R2/10 ≈ 0,16) để không đè nhau.
ROOT_R = 0.12
COUNTRY_R = (0.07, 0.07)       # (nhỏ nhất, thêm cho nước lớn nhất), theo căn bậc hai giá trị
LEAF_R = 0.045                 # mọi nút lá cùng một cỡ
EDGE_R = 0.003                 # cạnh cha-con
EDGE_COLOR = "#6E6E6E"


def build_layout():
    """Trả về (gốc, nước, lá) như notebook: bảng nước có x, y và bảng lá có x, y theo nước cha."""
    data = ROOT / "data" / "processed"
    nodes = pd.read_csv(data / "nodes.csv")
    tree = pd.read_csv(data / "tree.csv")
    cp = pd.read_csv(data / "country_product.csv")
    asean = nodes.loc[nodes["is_focus"], "country_iso3"].tolist()
    names = nodes.set_index("country_iso3")["country_name_vi"].to_dict()

    hs2 = tree[tree["level"] == 2][["product_id", "sector_id"]]
    a = cp[cp["country_iso3"].isin(asean) & (cp["year"] == REFERENCE_YEAR)].merge(hs2, on="product_id")
    a = a.groupby(["country_iso3", "sector_id"], as_index=False)["export_value"].sum()
    a = a[a["export_value"] > 0]
    a["country"] = a["country_iso3"].map(names)

    ctry = (a.groupby(["country_iso3", "country"], as_index=False)["export_value"].sum()
              .sort_values("export_value", ascending=False).reset_index(drop=True))
    ctry["theta"] = 2 * np.pi * ctry.index / len(ctry)
    ctry["x"], ctry["y"] = R1 * np.cos(ctry["theta"]), R1 * np.sin(ctry["theta"])

    lf = a.merge(ctry[["country_iso3", "x", "y"]].add_suffix("_ctry"), left_on="country_iso3", right_on="country_iso3_ctry")
    phi = 2 * np.pi * (lf["sector_id"] - 1) / len(SECTOR_PALETTE)
    lf["x"], lf["y"] = lf["x_ctry"] + R2 * np.cos(phi), lf["y_ctry"] + R2 * np.sin(phi)
    return ctry["export_value"].sum(), ctry, lf


# --- hình học: mỗi hàm trả (đỉnh, pháp tuyến, chỉ số tam giác) --------------------------------------------------------
def sphere(c, r, n_lat=12, n_lon=16):
    lat = np.linspace(0, np.pi, n_lat + 1)[:, None]
    lon = np.linspace(0, 2 * np.pi, n_lon + 1)[None, :]
    nrm = np.stack([np.sin(lat) * np.cos(lon), np.cos(lat) + 0 * lon, np.sin(lat) * np.sin(lon)], -1).reshape(-1, 3)
    idx = np.arange((n_lat + 1) * (n_lon + 1)).reshape(n_lat + 1, n_lon + 1)
    p, q, s, t = idx[:-1, :-1].ravel(), idx[1:, :-1].ravel(), idx[1:, 1:].ravel(), idx[:-1, 1:].ravel()
    return np.asarray(c, float) + r * nrm, nrm, np.r_[np.c_[p, q, s], np.c_[p, s, t]]


def _frame(axis):
    axis = axis / np.linalg.norm(axis)
    helper = np.array([0.0, 1.0, 0.0]) if abs(axis[1]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = np.cross(axis, helper)
    u /= np.linalg.norm(u)
    return u, np.cross(axis, u)


def cylinder(p0, p1, r, n=6):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    u, v = _frame(p1 - p0)
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    ring = np.cos(t)[:, None] * u + np.sin(t)[:, None] * v
    pos = np.r_[p0 + r * ring, p1 + r * ring]
    j = (np.arange(n) + 1) % n
    tris = np.r_[np.c_[np.arange(n), j, n + np.arange(n)], np.c_[j, n + j, n + np.arange(n)]]
    return pos, np.r_[ring, ring], tris


# --- ghi .glb ----------------------------------------------------------------------------------------------------------
def srgb_to_linear(hexcolor):
    c = np.array([int(hexcolor[i:i + 2], 16) for i in (1, 3, 5)]) / 255
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4).tolist()


def flat_material(name, color):
    """Màu phẳng chỉ dùng glTF lõi: emissive = màu thật, baseColor đen và metallic = 1.
    Kim loại lấy baseColor làm màu phản chiếu, nên baseColor đen thì không phản chiếu gì cả, kể cả ánh sáng môi
    trường dựng sẵn của PowerPoint. Với metallic = 0 (phi kim) thì glTF luôn phản chiếu khoảng 4% và lóa mạnh ở viền
    hình cầu: đó là vẻ bóng như bi crôm thấy trên slide."""
    return {"name": name, "emissiveFactor": srgb_to_linear(color),
            "pbrMetallicRoughness": {"baseColorFactor": [0.0, 0.0, 0.0, 1.0], "metallicFactor": 1.0, "roughnessFactor": 1.0}}


def write_glb(path, groups):
    """groups: [(tên, màu hex, [(đỉnh, pháp tuyến, tam giác), ...])]; mỗi nhóm là một mesh một vật liệu."""
    blob, views, accessors, materials, meshes, nodes = bytearray(), [], [], [], [], []

    def add(arr, target, **extra):
        while len(blob) % 4:
            blob.append(0)
        views.append({"buffer": 0, "byteOffset": len(blob), "byteLength": arr.nbytes, "target": target})
        blob.extend(arr.tobytes())
        accessors.append({"bufferView": len(views) - 1, "count": len(arr), **extra})
        return len(accessors) - 1

    for name, color, parts in groups:
        base, pos, nrm, idx = 0, [], [], []
        for p, n, t in parts:
            pos.append(p), nrm.append(n), idx.append(np.asarray(t) + base)
            base += len(p)
        pos, nrm, idx = np.concatenate(pos).astype("<f4"), np.concatenate(nrm).astype("<f4"), np.concatenate(idx).astype("<u4")
        materials.append(flat_material(name, color))
        a_pos = add(pos, 34962, componentType=5126, type="VEC3", min=pos.min(0).tolist(), max=pos.max(0).tolist())
        a_nrm = add(nrm, 34962, componentType=5126, type="VEC3")
        a_idx = add(idx.ravel(), 34963, componentType=5125, type="SCALAR")
        meshes.append({"name": name, "primitives": [{"attributes": {"POSITION": a_pos, "NORMAL": a_nrm},
                                                     "indices": a_idx, "material": len(materials) - 1}]})
        nodes.append({"name": name, "mesh": len(meshes) - 1})

    while len(blob) % 4:
        blob.append(0)
    doc = {"asset": {"version": "2.0", "generator": "src/export_cone_tree_glb.py"}, "scene": 0,
           "scenes": [{"nodes": list(range(len(nodes)))}], "nodes": nodes, "meshes": meshes, "materials": materials,
           "accessors": accessors, "bufferViews": views, "buffers": [{"byteLength": len(blob)}]}
    js =json.dumps(doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    js += b" " * (-len(js) % 4)
    total = 12 + 8 + len(js) + 8 + len(blob)
    Path(path).write_bytes(b"glTF" + struct.pack("<II", 2, total) + struct.pack("<I", len(js)) + b"JSON" + js
                           + struct.pack("<I", len(blob)) + b"BIN\0" + bytes(blob))


def main(out_dir):
    total, ctry, lf = build_layout()
    gl = lambda x, y, z: np.array([x, z + 1.0, -y])         # plotly (z lên) -> glTF (Y lên), dịch để mô hình ở quanh gốc
    cmax = ctry["export_value"].max()
    country_r = lambda v: COUNTRY_R[0] + COUNTRY_R[1] * np.sqrt(v / cmax)

    root_p = gl(0, 0, Z0)
    ctry_p = {r.country_iso3: gl(r.x, r.y, Z1) for r in ctry.itertuples()}
    edges = [cylinder(root_p, ctry_p[r.country_iso3], EDGE_R) for r in ctry.itertuples()]
    edges += [cylinder(ctry_p[r.country_iso3], gl(r.x, r.y, Z2), EDGE_R) for r in lf.itertuples()]

    groups = [("Cạnh", EDGE_COLOR, edges),
              ("ASEAN", "#333333", [sphere(root_p, ROOT_R)]),
              ("Nước", "#666666", [sphere(ctry_p[r.country_iso3], country_r(r.export_value)) for r in ctry.itertuples()])]
    for sid, g in lf.groupby("sector_id"):
        groups.append((SECTOR_NAME_VI[sid], SECTOR_PALETTE[sid], [sphere(gl(r.x, r.y, Z2), LEAF_R) for r in g.itertuples()]))

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    write_glb(out / "cone_tree.glb", groups)
    print("%s: %d KB" % (out / "cone_tree.glb", (out / "cone_tree.glb").stat().st_size // 1024))
    print("%d nước, %d lá, %d nhóm vật liệu" % (len(ctry), len(lf), len(groups)))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT / "notebooks" / "exports")

"""Shared coordinate helpers for mount-maunganui-reef (explicit chains; no make-canonical rotation).
Fig 3 pixel <-> BOPTM (EPSG:2106) <-> NZTM (EPSG:2193) <-> LINZ aerial crop pixel; BOPTM <-> canonical (alongshore, offshore)."""
import json, math
import numpy as np
from pyproj import Transformer
ROOT = 'C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/mount-maunganui-reef/'
T_boptm_to_nztm = Transformer.from_crs(2106, 2193, always_xy=True)
T_nztm_to_boptm = Transformer.from_crs(2193, 2106, always_xy=True)
T_boptm_to_ll = Transformer.from_crs(2106, 4326, always_xy=True)
T_ll_to_boptm = Transformer.from_crs(4326, 2106, always_xy=True)
# Fig 3 tick calibration (METHOD Step 2a): 5.45 px/m
F3_PXM = 5.45
def f3_en(x, y): return (376680 + (x - 109) / F3_PXM, 812960 - (y - 82) / F3_PXM)
def en_f3(e, n): return (109 + (e - 376680) * F3_PXM, 82 + (812960 - n) * F3_PXM)
# LINZ aerial crop
_side = json.load(open(ROOT + 'src/linz_aerial_2010-11_BD37_1000_1314_crop.png.geo.json'))
LZ_E0, LZ_N0 = _side['top_left_nztm']; LZ_PX = 0.125
def lz_px_to_nztm(i, j): return (LZ_E0 + i * LZ_PX, LZ_N0 - j * LZ_PX)
def nztm_to_lz_px(e, n): return ((e - LZ_E0) / LZ_PX, (LZ_N0 - n) / LZ_PX)
def f3_to_lz(x, y):
    e, n = f3_en(x, y); E, N = T_boptm_to_nztm.transform(e, n); return nztm_to_lz_px(E, N)
def lz_to_f3(i, j):
    E, N = lz_px_to_nztm(i, j); e, n = T_nztm_to_boptm.transform(E, N); return en_f3(e, n)

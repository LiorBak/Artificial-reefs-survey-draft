"""mmr_lib.py - shared helpers for the Mount Maunganui reef 3D model (2026-10-06).

Fig 5 (BoPRC 2014; registry mount-maunganui-reef-img-04) = hillshaded colour-coded DEM of the 18 Jul 2013 multibeam survey, own NZ-grid '+' ticks every 20 m
(x_px = 135 + 84.33 k, y_px = 16 + 84.33 k; tick labels E 376620.. / N 812980..) and a continuous colour bar (labels -0.19 .. -4.90 m CD, first label centre y = 14.0,
last y = 733.5).  Hue (hillshade changes brightness, not hue) -> colour bar -> depth in m below Chart Datum (negative numbers = below CD).
Canonical frame (shape.json): origin E0,N0 (NZGD2000 / Bay of Plenty 2000, EPSG:2106), x alongshore toward GRID bearing 315.99 deg, y offshore toward GRID bearing 45.99 deg
(= true 316.15 / 46.15; grid convergence -0.161 deg).  (dE, dN) = (x sin ax + y sin oy, x cos ax + y cos oy)  [the 2x2 matrix is its own inverse].
"""
import json, math
import numpy as np
from PIL import Image
import matplotlib.colors as mc
from scipy import ndimage as ndi

ROOT = 'C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/'
S = ROOT + '07_scale/shapes/mount-maunganui-reef/'
FIG5 = ROOT + '03_images/reefs/mount-maunganui-reef/mount-maunganui-reef_boprc-fig5-multibeam-2013_2013.png'
K5 = 84.33 / 20.0                      # Fig 5 px per m
E0, N0 = 376521.85, 812664.84          # canonical origin in the NZ grid (verifier, shape.json chain)
AX, OY = math.radians(315.99), math.radians(45.99)
MSL_ABOVE_CD = 1.13                    # LINZ standard port Tauranga 2026-27 (MSL 2006-2025)
MVD_ABOVE_CD = 0.9622                  # NIWA 2006 (Bell, Goring et al.)


def en_to_xy(E, N):
    dE, dN = E - E0, N - N0
    return dE * math.sin(AX) + dN * math.cos(AX), dE * math.sin(OY) + dN * math.cos(OY)


def xy_to_en(x, y):
    return E0 + x * np.sin(AX) + y * np.sin(OY), N0 + x * np.cos(AX) + y * np.cos(OY)


def load_fig5():
    """returns depth (m CD, negative; NaN where the pixel is not a colour-bar hue), filled (nearest valid), valid mask, rgb array"""
    im = Image.open(FIG5).convert('RGB'); a = np.array(im).astype(float) / 255; H, W, _ = a.shape
    bar = a[:, 1293:1298, :].mean(1)
    depth_bar = -0.19 + (np.arange(H) - 14.0) / (733.5 - 14.0) * (-4.90 + 0.19)
    hb = mc.rgb_to_hsv(bar)[:, 0][10:745]; order = np.argsort(hb)
    hsv = mc.rgb_to_hsv(a)
    dep = np.interp(hsv[..., 0], hb[order], depth_bar[10:745][order])
    valid = (hsv[..., 1] > 0.55) & (hsv[..., 2] > 0.35) & (hsv[..., 0] < 0.70); valid[:, 1240:] = False
    dep = np.where(valid, dep, np.nan)
    ind = ndi.distance_transform_edt(~valid, return_distances=False, return_indices=True)
    return dep, dep[ind[0], ind[1]], valid, a


def fig5_to_grid(dep, valid, x0, x1, y0, y1, d):
    """resample the Fig 5 DEM onto a canonical-frame grid (cell centres x0 + i d, y0 + j d); returns Z (m CD, NaN outside the survey), grid axes"""
    xs = np.arange(x0, x1 + 1e-9, d); ys = np.arange(y0, y1 + 1e-9, d)
    XX, YY = np.meshgrid(xs, ys)
    E, N = xy_to_en(XX, YY)
    px = 135 + (E - 376620) * K5; py = 16 + (812980 - N) * K5
    z = ndi.map_coordinates(np.where(np.isnan(dep), 0, dep), [py, px], order=1, mode='nearest')
    v = ndi.map_coordinates(valid.astype(float), [py, px], order=1, mode='constant', cval=0) > 0.99
    return np.where(v, z, np.nan), xs, ys


def load_shape():
    sh = json.load(open(S + 'shape.json', encoding='utf-8'))
    c = sh['canonical']
    return sh, [np.array(p) for p in c['polygons_m']], [np.array(p) for p in c['toe_polygons_m']]

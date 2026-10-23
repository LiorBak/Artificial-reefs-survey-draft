"""prep_multibeam.py - digitise Corbett et al. 2023 Fig 3 (pre-works multibeam, ICM 2017; registry img-55) into a depth raster in the
canonical frame of shape.json.  Output: src/multibeam_fig3.npz (D = surface depth, bed = estimated bare seabed, R = relief, all m AHD,
1 m grid, x -90..85, y 190..390) + src/multibeam_fig3.json (parameters and statistics) + annotated/A1_corbett_fig3_digitised.png.
Run from this folder:  python prep_multibeam.py
Method (METHODS_3D 3.2): colour -> depth by HUE through the printed colour bar (linear fit to the 4 tick labels -1,-4,-6,-9; resid <=0.4 m);
bed = grey-scale opening (disk r = 10 px = 4.65 m) + Gaussian smoothing; relief R = D - bed.
Registration (assumed north-up, no rotation): 20 m bar ticks at x = 274, 295, 317 px -> 0.4651 m/px; translation (tx, ty) = (-5, 290) m
(image centre in canonical x, y) chosen by maximising the overlap of relief > 0.6 m with the traced 2020 arm polygons; +-10 m."""
import json, os, math, colorsys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from scipy.ndimage import map_coordinates
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(HERE)
SRC = os.path.join(HERE, 'src'); ANN = os.path.join(HERE, 'annotated')
IMG = os.path.join(BASE, 'src', 'gov', 'corbett2023_extracted', 'p3_x86.png')
S_M = 0.4651; TX, TY, TH = -5.0, 290.0, 0.0; MAPW = 352
TICKS_Y = np.array([140, 198, 253, 305.]); TICKS_D = np.array([-1, -4, -6, -9.])
XH = (-math.sin(math.radians(3.8)), math.cos(math.radians(3.8)))      # canonical x axis: (E, N) components (bearing 356.2)
YH = (math.sin(math.radians(86.2)), math.cos(math.radians(86.2)))      # canonical y axis (bearing 86.2)


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]; return (x * x + y * y) <= r * r


def main():
    im = np.array(Image.open(IMG).convert('RGB')).astype(float) / 255; H, W, _ = im.shape
    b, a = np.polyfit(TICKS_Y, TICKS_D, 1)
    resid = TICKS_D - (a + b * TICKS_Y)
    ys = np.arange(134, 312); col = im[ys, 396:412].mean(1); dep = a + b * ys
    hue = np.array([colorsys.rgb_to_hsv(*c)[0] for c in col]); hue[hue > 0.9] -= 1
    sel = (dep <= -1.7) & (dep >= -7.9)
    h_l = np.maximum.accumulate(hue[sel]); d_l = dep[sel]
    hsv = np.array([[colorsys.rgb_to_hsv(*im[y, x]) for x in range(W)] for y in range(H)])
    hh = hsv[..., 0].copy(); hh[hh > 0.9] -= 1
    D = np.interp(hh, h_l, d_l)
    valid = (hsv[..., 1] > 0.25) & (hsv[..., 2] > 0.2); valid[:, MAPW:] = False
    Df = np.where(valid, D, np.median(D[valid]))
    r = 10
    bed = ndi.gaussian_filter(ndi.grey_dilation(ndi.grey_erosion(Df, footprint=disk(r), mode='nearest'), footprint=disk(r), mode='nearest'), 6)
    R = Df - bed
    # resample to the canonical 1 m grid
    xs = np.arange(-90, 86, 1.0); ys_ = np.arange(190, 391, 1.0); X, Y = np.meshgrid(xs, ys_)
    dx, dy = X - TX, Y - TY
    E = dx * XH[0] + dy * YH[0]; N = dx * XH[1] + dy * YH[1]
    u = E / S_M + MAPW / 2; v = -N / S_M + H / 2
    inside = (u >= 0) & (u < MAPW - 1) & (v >= 0) & (v < H - 1)
    samp = lambda A: map_coordinates(A, [v, u], order=1, mode='nearest')
    Dg, Bg, Rg = samp(Df), samp(bed), samp(R)
    for A in (Dg, Bg, Rg): A[~inside] = np.nan
    np.savez_compressed(os.path.join(SRC, 'multibeam_fig3.npz'), xs=xs, ys=ys_, D=Dg.astype('f4'), bed=Bg.astype('f4'), R=Rg.astype('f4'))
    st = dict(scale_m_per_px=S_M, tx=TX, ty=TY, rot_deg=TH, reg_unc_m=10, map_px=[MAPW, H], extent_m=[round(MAPW * S_M, 1), round(H * S_M, 1)],
              depth_fit=dict(slope_m_per_px=round(float(b), 5), intercept=round(float(a), 3), tick_residuals_m=[round(float(q), 2) for q in resid]),
              relief_p50_p90_p99=[round(float(np.percentile(R[valid], q)), 2) for q in (50, 90, 99)],
              bed_range_m=[round(float(bed[valid].min()), 2), round(float(bed[valid].max()), 2)])
    json.dump(st, open(os.path.join(SRC, 'multibeam_fig3.json'), 'w'), indent=1)
    print(st)


if __name__ == '__main__':
    main()

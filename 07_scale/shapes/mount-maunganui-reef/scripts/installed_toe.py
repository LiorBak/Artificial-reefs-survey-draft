"""ASR 'Mount Reef Installed' image (src/mount-reef-installed.jpg) -> registered onto BoPRC Fig 3 and outlined at depth > -4.2 (toe-ish level).
Steps: (1) legend: colour bar x=531..543, y=103..437, ticks every 23.2 px = 0.4 m from -1.8 (y=113) to -7.4 (y=438) -> depth(y) = -1.8-(y-113)/58.04;
(2) pixel -> depth by nearest bar colour (dist<45), glint none; (3) image rotated 90 deg clockwise (the image is a north-up map turned 90 deg CCW);
(4) similarity transform to Fig 3 pixel frame fitted by maximising the correlation of the (T=-3.8) mask with the Fig 3 -2.0 m bag-field mask (see METHOD);
(5) outline at T=-4.2 warped into Fig 3 frame. Output: ../work_installed_toe_fig3px.json (+ ../work_installed_reg.json).
Fig 3 -2.0 mask is rebuilt from %TEMP%/mmr/dep.npy (segment_fig3.py)."""
import numpy as np, math, json, os
from PIL import Image
from scipy import ndimage as ndi
from scipy.optimize import minimize
from skimage import measure
R = 'C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/mount-maunganui-reef/'
tmp = os.environ['TEMP'] + '/mmr/'
dep3 = np.load(tmp + 'dep.npy')
win = np.zeros(dep3.shape, bool); win[330:790, 180:720] = True
m3 = (dep3 > -2.0) & win
m3 = ndi.binary_closing(m3, iterations=2); m3 = ndi.binary_fill_holes(m3)
lab, n = ndi.label(m3); sizes = ndi.sum(m3, lab, range(1, n+1)); m3 = np.isin(lab, [i+1 for i, s in enumerate(sizes) if s > 300])
H3, W3 = m3.shape
im = np.array(Image.open(R + 'src/mount-reef-installed.jpg').convert('RGB')).astype(float)
bar = im[103:438, 531:543, :].mean(1); bar_depth = -1.8 - (np.arange(103, 438) - 113) / 58.04
d = np.linalg.norm(im[:, :, None, :] - bar[None, None, ::2, :], axis=3)
depI = bar_depth[::2][d.argmin(2)]; okI = d.min(2) < 45
plot = np.zeros(okI.shape, bool); plot[20:505, 30:520] = True; okI &= plot
def imask(T):
    m = (depI > T) & okI; m = ndi.binary_opening(m, iterations=1); return np.rot90(m, k=-1)
def warp(a, s, th, tx, ty):
    c, sn = math.cos(math.radians(th)), math.sin(math.radians(th))
    Rinv = np.array([[c, sn], [-sn, c]]); Mxy = s * Rinv
    M = np.array([[Mxy[1, 1], Mxy[1, 0]], [Mxy[0, 1], Mxy[0, 0]]])
    off_xy = -Mxy @ np.array([tx, ty])
    return ndi.affine_transform(a, M, offset=np.array([off_xy[1], off_xy[0]]), output_shape=(H3, W3), order=1)
m3f = ndi.gaussian_filter(m3.astype(float), 1.5)
def score(p, mIf):
    w = warp(mIf, *p)
    return -(w * m3f).sum() / math.sqrt((w**2).sum() * (m3f**2).sum() + 1e-9)
mIf = ndi.gaussian_filter(imask(-3.8).astype(float), 1.0)
best = None
for s0 in (1.0, 1.05, 1.1, 1.15, 1.2):          # several starts, local optimiser each (translation start from mass-centre alignment)
    cy3, cx3 = ndi.center_of_mass(m3); cyI, cxI = ndi.center_of_mass(mIf)
    p0 = [s0, 0.0, cx3 - cxI / s0, cy3 - cyI / s0]
    r = minimize(score, p0, args=(mIf,), method='Nelder-Mead', options=dict(xatol=1e-4, fatol=1e-8, maxiter=2000))
    if best is None or r.fun < best.fun: best = r
s, th, tx, ty = best.x
w38 = warp(mIf, s, th, tx, ty) > 0.5
print('fit', dict(s=s, th=th, tx=tx, ty=ty, corr=-best.fun, IoU=(w38 & m3).sum() / (w38 | m3).sum()))
json.dump(dict(s=s, theta_deg=th, tx=tx, ty=ty, corr=-best.fun, iou=float((w38 & m3).sum() / (w38 | m3).sum()), installed_px_per_m=5.45 * s,
               note='p3 = R(theta) p_I / s + t ; p_I in 90deg-CW-rotated Installed pixel coords; p3 in Fig 3 native px (5.45 px/m)'), open(R + 'work_installed_reg.json', 'w'), indent=1)
out = {}
for T in (-3.8, -4.2):
    w = warp(ndi.gaussian_filter(imask(T).astype(float), 1.0), s, th, tx, ty) > 0.5
    w = ndi.binary_fill_holes(w)
    lab, n = ndi.label(w); sz = ndi.sum(w, lab, range(1, n+1)); w = np.isin(lab, [i+1 for i, q in enumerate(sz) if q / 5.45**2 > 15])
    lab, n = ndi.label(w); polys = []
    for i in range(1, n+1):
        comp = np.pad((lab == i).astype(float), 1)
        c = max(measure.find_contours(comp, 0.5), key=len) - 1
        c = measure.approximate_polygon(c, 1.5)
        polys.append([[round(float(x), 1), round(float(y), 1)] for y, x in c[:-1]])
    out[str(T)] = polys
    print(T, len(polys), [round(float(w.sum()) / 5.45**2)])
json.dump(out, open(R + 'work_installed_toe_fig3px.json', 'w'))

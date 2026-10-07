"""design_registration.py - georeference the Jackson et al. 2012 Fig 6b / Fig 7 aerial (2011) to the s3 Esri image (METHOD.md Step 2d).
Needs trace_s3_out.json? no - uses only the images. Writes design_registration_out.json (affine Fig7 px -> s3 px).
Chain: (1) Fig 6b -> Fig 7 template match (same photograph, ratio ~1.75); (2) Fig 6b dark-patch mask vs s3 dark-patch mask, normalised
cross-correlation at the adopted scale (Fig 7 = 0.21 m/px from Jackson 2007 Fig 13's 100 m bar chain; Fig 6b = 0.21 x 1.75 m/px)."""
import numpy as np, cv2, json, os
from PIL import Image
from skimage.filters import threshold_otsu
HERE = os.path.dirname(os.path.abspath(__file__)); G = HERE + "/src/gov/narrowneck-gold-coast_jackson2012_"
a = np.asarray(Image.open(G + "fig6b_aerial_2011-07_native.jpeg").convert("RGB")).astype(np.float32)
b0 = np.asarray(Image.open(G + "fig7_overlay_2011-07_aerial_with_design_contours_and_containers_native.jpeg").convert("RGB")).astype(np.float32)
s3 = np.asarray(Image.open(HERE + "/src/wayback/nn_wayback_2020-08-08_r9812_z19.png").convert("RGB")).astype(np.float32)
# (1) Fig 6b -> Fig 7 (white overlay lines of Fig 7 masked out)
white = cv2.dilate((b0.min(axis=2) > 200).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
prep = lambda x, s: cv2.GaussianBlur(x[:, :, 1], (0, 0), s) - cv2.GaussianBlur(cv2.GaussianBlur(x[:, :, 1], (0, 0), s), (0, 0), 20)
A, B = prep(a, 1.0), prep(b0, 1.5); B[white] = 0
best = None
for k in np.arange(1.5, 2.3, 0.05):
    Ak = cv2.resize(A, None, fx=k, fy=k, interpolation=cv2.INTER_CUBIC); h, w = Ak.shape
    t = Ak[int(h * .25):int(h * .75), int(w * .2):int(w * .8)]
    r = cv2.matchTemplate(B, t, cv2.TM_CCOEFF_NORMED); mx = r.max(); loc = np.unravel_index(r.argmax(), r.shape)
    if best is None or mx > best[0]: best = (mx, k, loc[1] - int(w * .2), loc[0] - int(h * .25))
R, ox, oy = 1.75, 82.6, -42.8     # best k was 1.75 (corr 0.40); offsets: x7 = R*x6 + ox, y7 = R*y6 + oy
print("Fig7/Fig6b scale search best:", [round(float(v), 3) for v in best])
# (2) dark masks, NCC at the adopted scale
g = cv2.GaussianBlur(a[:, :, 1], (0, 0), 1.5); d = cv2.GaussianBlur(g, (0, 0), 40) - g
M6 = (d > 0.9 * threshold_otsu(d[40:440, 90:620])).astype(np.float32); M6[:, :90] = 0; M6[200:260, 450:520] = 0
g3 = cv2.GaussianBlur(s3[:, :, 1], (0, 0), 1.0); keep0 = (g3 < 49).astype(np.uint8)
win = np.zeros_like(keep0); win[500:1020, 240:880] = 1; keep0 *= win        # same window and area filter as trace_s3.py
n_, lab_, st_, _ = cv2.connectedComponentsWithStats(keep0, 8)
keep = np.zeros(keep0.shape, np.float32)
for i_ in range(1, n_):
    if st_[i_, cv2.CC_STAT_AREA] >= 60: keep[lab_ == i_] = 1
Sb = cv2.GaussianBlur(keep, (0, 0), 3)[380:1140, 100:1100]
MPP7 = 0.21; MPP6 = MPP7 * R; k = MPP6 / 0.263665
Tk = cv2.resize(cv2.GaussianBlur(M6, (0, 0), 3), None, fx=k, fy=k, interpolation=cv2.INTER_AREA)
best = None
for rot in np.arange(-4, 6, 0.5):
    M = cv2.getRotationMatrix2D((Tk.shape[1] / 2, Tk.shape[0] / 2), rot, 1.0)
    Tr = cv2.warpAffine(Tk, M, (Tk.shape[1], Tk.shape[0]))
    r = cv2.matchTemplate(Sb, Tr, cv2.TM_CCOEFF_NORMED); mx = float(r.max()); loc = np.unravel_index(r.argmax(), r.shape)
    if best is None or mx > best[0]: best = (mx, rot, int(loc[1]), int(loc[0]), M)
mx, rot, lx, ly, M = best
A1 = np.array([[1 / R, 0, -ox / R], [0, 1 / R, -oy / R], [0, 0, 1]]); A2 = np.diag([k, k, 1.0])
A3 = np.vstack([M, [0, 0, 1]]); A4 = np.array([[1, 0, lx + 100], [0, 1, ly + 380], [0, 0, 1]])
T = A4 @ A3 @ A2 @ A1
json.dump({"fig7_px_to_s3_px_affine": T.tolist(), "mpp_fig7": MPP7, "ratio_fig7_over_fig6b": R, "ncc_corr": mx, "rot_deg": rot, "loc": [lx, ly]},
          open(HERE + "/design_registration_out.json", "w"), indent=1)
print("NCC corr %.3f rot %.1f loc %d,%d" % (mx, rot, lx, ly))

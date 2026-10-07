"""VERIFIER (2026-10-06): independent check of the img1 outline against BoPRC Fig 5 (second rendering of the SAME 18 Jul 2013 multibeam survey,
03_images/reefs/mount-maunganui-reef/mount-maunganui-reef_boprc-fig5-multibeam-2013_2013.png, 1299 x 752 px).
Fig 5 has its own '+' grid ticks every 20 m (x = 135 + 84.33 k, y = 16 + 84.33 k; labels 376620.. / 812980..) and a continuous colour bar (labels -0.19..-4.90,
first label centre y=14.0, last y=733.5). Hue of each pixel (hillshade changes brightness, not hue) -> depth through the bar.
Outputs: ../work_verify_fig5.json, ../overlays/verify_fig5_crosscheck_2013.png.
Results: -2.0 m mask of Fig 5 = 1074 m2 vs 1072 m2 (img1 outline), IoU 0.93 at zero shift; crest-depth percentiles inside the outline (see json)."""
import json, math, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from skimage import measure
from skimage.draw import polygon as skpoly
import matplotlib.colors as mc
ROOT = 'C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/'
S = ROOT + '07_scale/shapes/mount-maunganui-reef/'
IMG = ROOT + '03_images/reefs/mount-maunganui-reef/mount-maunganui-reef_boprc-fig5-multibeam-2013_2013.png'
K = 84.33 / 20.0                                    # px per m in Fig 5
im = Image.open(IMG).convert('RGB'); a = np.array(im).astype(float) / 255; H, W, _ = a.shape
bar = a[:, 1293:1298, :].mean(1)
depth_bar = -0.19 + (np.arange(H) - 14.0) / (733.5 - 14.0) * (-4.90 + 0.19)
hb = mc.rgb_to_hsv(bar)[:, 0][10:745]; order = np.argsort(hb)
hsv = mc.rgb_to_hsv(a)
dep = np.interp(hsv[..., 0], hb[order], depth_bar[10:745][order])
valid = (hsv[..., 1] > 0.55) & (hsv[..., 2] > 0.35) & (hsv[..., 0] < 0.70); valid[:, 1240:] = False
dep = np.where(valid, dep, np.nan)
ind = ndi.distance_transform_edt(~valid, return_distances=False, return_indices=True); depf = dep[ind[0], ind[1]]
sh = json.load(open(S + 'shape.json', encoding='utf-8'))
P = [s for s in sh['sources'] if s['id'] == 'img1'][0]['pixel_polygons']
px2en = lambda p: (376680 + (p[0] - 109) / 5.45, 812960 - (p[1] - 82) / 5.45)
en2f5 = lambda E, N: (135 + (E - 376620) * K, 16 + (812980 - N) * K)
polys = [[en2f5(*px2en(p)) for p in poly] for poly in P]
m = np.zeros((H, W), bool)
for poly in polys:
    q = np.array(poly); rr, cc = skpoly(q[:, 1], q[:, 0], (H, W)); m[rr, cc] = True
f5 = (depf > -2.0) & ndi.binary_dilation(m, iterations=25); f5 = ndi.binary_opening(f5, iterations=1)
res = dict(fig5_scale_px_per_m=round(K, 4), outline_area_m2=round(m.sum() / K**2, 1), fig5_shallower_than_m2p0_area_m2=round(f5.sum() / K**2, 1),
           iou_zero_shift=round(float((m & f5).sum() / (m | f5).sum()), 3))
best = max(((((ndi.shift(m.astype(float), (dy, dx), order=0) > .5) & f5).sum() / ((ndi.shift(m.astype(float), (dy, dx), order=0) > .5) | f5).sum()), dx, dy) for dx in range(-8, 9) for dy in range(-8, 9))
res['best_shift_px_dx_dy_iou'] = [int(best[1]), int(best[2]), round(float(best[0]), 3)]
names = ['west 3-bag block', 'mid-top bag', 'NE small bag', 'NE lobe', 'south arm']; stats = {}
for nm, poly in zip(names, polys):
    q = np.array(poly); rr, cc = skpoly(q[:, 1], q[:, 0], (H, W)); v = dep[rr, cc]; v = v[~np.isnan(v)]
    stats[nm] = dict(n_px=int(len(v)), shallowest=round(float(v.max()), 2), p5=round(float(np.percentile(v, 95)), 2), p10=round(float(np.percentile(v, 90)), 2),
                     p25=round(float(np.percentile(v, 75)), 2), median=round(float(np.median(v)), 2))
res['depth_inside_outline_m_CD'] = stats
# bed-relative footprints (robust plane fit of the bed in an annulus 10-40 m from the -2.0 outline)
yy, xx = np.mgrid[0:H, 0:W]; dist = ndi.distance_transform_edt(~m) / K
dom = ndi.binary_fill_holes(ndi.binary_closing(valid, iterations=6)); dom[:, 1240:] = False
ann = dom & (dist > 10) & (dist < 40); X = (xx[ann] - 135) / K; Y = (yy[ann] - 16) / K; Z = depf[ann]
A = lambda X, Y: np.stack([np.ones_like(X), X, Y], 1); w = np.ones_like(Z, bool)
for _ in range(30):
    c, *_ = np.linalg.lstsq(A(X[w], Y[w]), Z[w], rcond=None); r = Z - A(X, Y) @ c; w = np.abs(r) < max(0.25, 1.5 * np.std(r[w]))
bed = c[0] + c[1] * (xx - 135) / K + c[2] * (yy - 16) / K; R = depf - bed
res['bed_plane'] = dict(z0=round(float(c[0]), 3), dz_dx_per_m=round(float(c[1]), 4), dz_dy_per_m=round(float(c[2]), 4), resid_std_m=round(float(r[w].std()), 3))
cx, cy = ndi.center_of_mass(m)[1], ndi.center_of_mass(m)[0]
res['bed_at_reef_centroid_m_CD'] = round(float(c[0] + c[1] * (cx - 135) / K + c[2] * (cy - 16) / K), 2)
ax_, oy_ = math.radians(315.99), math.radians(45.99); fp = {}
for t in (0.3, 0.5, 0.8):
    mm = (R > t) & dom & (dist < 12); mm = ndi.binary_fill_holes(ndi.binary_closing(mm, iterations=1))
    lab, n = ndi.label(mm); sz = ndi.sum(mm, lab, range(1, n + 1)); mm = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s / K**2 > 15])
    ys, xs = np.where(mm); E = 376620 + (xs - 135) / K; N = 812980 - (ys - 16) / K
    xa = (E - 376521.85) * math.sin(ax_) + (N - 812664.84) * math.cos(ax_); ya = (E - 376521.85) * math.sin(oy_) + (N - 812664.84) * math.cos(oy_)
    fp['+%.1f m above plane bed' % t] = dict(area_m2=round(float(mm.sum() / K**2)), alongshore_m=round(float(xa.max() - xa.min() + 1 / K), 1), crossshore_m=round(float(ya.max() - ya.min() + 1 / K), 1))
    if t == 0.5: m05 = mm
res['bed_relative_footprint'] = fp
json.dump(res, open(S + 'work_verify_fig5.json', 'w'), indent=1)
# overlay: crop around the reef, 3x
try: F = ImageFont.truetype('arial.ttf', 15)
except Exception: F = ImageFont.load_default()
box = (470, 290, 850, 650); k = 3
o = im.crop(box).resize(((box[2] - box[0]) * k, (box[3] - box[1]) * k), Image.LANCZOS); d = ImageDraw.Draw(o)
tr = lambda p: [((x - box[0]) * k, (y - box[1]) * k) for x, y in p]
for c_ in measure.find_contours(m05.astype(float), 0.5): d.line(tr([(x, y) for y, x in c_]), fill=(255, 255, 255), width=2)
for poly in polys: d.line(tr(poly) + [tr(poly)[0]], fill=(255, 0, 255), width=3)
d.rectangle([8, 8, 640, 74], fill=(0, 0, 0))
d.line([(14, 24), (44, 24)], fill=(255, 0, 255), width=3); d.text((52, 15), 'img1 -2.0 m CD outline (Fig 3 ticks -> Fig 5 ticks): area 1072 m2', fill=(255, 255, 255), font=F)
d.line([(14, 56), (44, 56)], fill=(255, 255, 255), width=3); d.text((52, 47), 'Fig 5 DEM, 0.5 m above the 2013 plane bed (verifier): 1049 m2', fill=(255, 255, 255), font=F)
Lm = 20 * K * k; d.rectangle([8, o.height - 44, 8 + Lm + 70, o.height - 8], fill=(0, 0, 0)); d.line([(14, o.height - 24), (14 + Lm, o.height - 24)], fill=(255, 255, 255), width=3); d.text((14 + Lm + 6, o.height - 33), '20 m', fill=(255, 255, 255), font=F)
d.text((o.width - 520, o.height - 26), 'BoPRC 2014 Fig 5 (same 18 Jul 2013 survey), own NZ-grid ticks; north up', fill=(0, 0, 0), font=F)
o.save(S + 'overlays/verify_fig5_crosscheck_2013.png')
print(json.dumps(res, indent=1))

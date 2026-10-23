"""fig3_asbuilt_check.py (2026-10-07) - layout check of the as-built survey picture in Mead & Borrero (2011) Fig 3 (bottom),
registry mount-maunganui-reef-img-23 (planned id; not yet registered), against shape.json (2013 -2.0 m outline and ASR toe outline).
The picture (205 x 211 px, extracted from the PDF) has NO scale bar, NO axis numbers, NO north arrow, NO date and NO depth legend;
only unlabelled grid ticks every 26.0 px on all four edges. So it is NOT traced as an outline version. This script
 1. measures the tick spacing,
 2. segments the yellow bag tops (Otsu on the green channel),
 3. registers the shape.json polygons to the mask (rotation + translation + scale by FFT correlation),
 4. reports the implied scale (px per m, hence the grid interval in m), the bag-top area, IoU.
Output: fig3_asbuilt_check.json and annotated/mmr_meadborrero2011_fig3b_layout_check.png
"""
import json, math
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi, signal
from skimage.filters import threshold_otsu
from skimage.draw import polygon as skpoly

R = 'C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/mount-maunganui-reef/'
img = Image.open(R + '3d/src/mmr_meadborrero2011_fig3b_asbuilt-survey-2800m3.png').convert('RGB')
a = np.array(img).astype(float)
H, W, _ = a.shape
inner = a[4:H - 4, 4:W - 4]
G = inner[:, :, 1]
thr = threshold_otsu(G)
mask = G > thr
mask = ndi.binary_opening(mask, iterations=1)
mask = ndi.binary_closing(mask, iterations=1)
lab, n = ndi.label(mask)
sizes = ndi.sum(mask, lab, range(1, n + 1))
keep = [i + 1 for i, s in enumerate(sizes) if s > 150]
mask = np.isin(lab, keep)
area_px = int(mask.sum())

g = a.mean(2)


def ticks(line, thr=248):
    idx = [i for i, v in enumerate(line) if v < thr]
    grp = []
    for i in idx:
        if grp and i - grp[-1][-1] <= 1:
            grp[-1].append(i)
        else:
            grp.append([i])
    return [sum(x) / len(x) for x in grp]


tl = ticks(g[:, 1]); tt = ticks(g[0, :], 250); tb = ticks(g[H - 1, :], 248)


def spacing(t):
    t = [x for x in t if x > 20]
    d = np.diff(t)
    d = d[(d > 20) & (d < 32)]
    return float(np.median(d)) if len(d) else None


tick_spacing = [spacing(tl), spacing(tt), spacing(tb)]

S = json.load(open(R + 'shape.json', encoding='utf8'))
polys_2013 = S['canonical']['polygons_m']; polys_toe = S['canonical']['toe_polygons_m']
allp = np.array([p for poly in polys_2013 for p in poly]); c0 = allp.mean(0)
mh, mw = mask.shape
mk = mask.astype(float)


MIRROR = False


def raster(polys, ang, scale):
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    m = np.zeros(mask.shape, bool)
    for poly in polys:
        P = np.array(poly) - c0
        if MIRROR:
            P = P * np.array([-1.0, 1.0])
        X = (P[:, 0] * ca - P[:, 1] * sa) * scale + mw / 2
        Y = -(P[:, 0] * sa + P[:, 1] * ca) * scale + mh / 2
        rr, cc = skpoly(Y, X, mask.shape); m[rr, cc] = True
    return m


def score(polys, ang, sc):
    tpl = raster(polys, ang, sc).astype(float)
    cc = signal.fftconvolve(mk, tpl[::-1, ::-1], mode='same')
    inter = cc.max(); iy, ix = np.unravel_index(cc.argmax(), cc.shape)
    u = mk.sum() + tpl.sum() - inter
    return inter / u, (float(ix - mw / 2), float(iy - mh / 2))


res = {}
for MIRROR, name, polys in ((m_, n_, p_) for m_ in (False, True) for n_, p_ in (('outline_2013_m2p0', polys_2013), ('toe_outline', polys_toe))):
    name = name + ('_mirrored' if MIRROR else '')
    allr = []
    for sc in [2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2]:
        for ang in range(0, 360, 2):
            iou, sh = score(polys, ang, sc)
            allr.append((iou, sc, ang, sh))
    allr.sort(reverse=True)
    best = allr[0]
    for ang2 in np.arange(best[2] - 2, best[2] + 2.01, 0.5):
        for sc2 in np.arange(best[1] - 0.2, best[1] + 0.21, 0.05):
            iou, sh = score(polys, float(ang2), float(sc2))
            if iou > best[0]:
                best = (iou, float(sc2), float(ang2), sh)
    byscale = {}
    for r in allr:
        byscale[r[1]] = max(byscale.get(r[1], 0), r[0])
    res[name] = {'mirrored': MIRROR, 'best_iou': round(best[0], 3), 'scale_px_per_m': round(best[1], 3), 'rotation_deg': round(best[2], 1),
                 'shift_px': [round(best[3][0], 1), round(best[3][1], 1)],
                 'implied_grid_interval_m': round(26.0 / best[1], 2),
                 'best_iou_by_scale': {str(k): round(v, 3) for k, v in sorted(byscale.items())}}
res['tick_spacing_px'] = tick_spacing
res['tick_counts'] = [len(tl), len(tt), len(tb)]
res['otsu_threshold_G'] = float(thr)
res['mask_area_px'] = area_px
res['mask_area_m2_if_grid_10m'] = round(area_px / 2.6 ** 2, 0)
FITS = ('outline_2013_m2p0', 'toe_outline', 'outline_2013_m2p0_mirrored', 'toe_outline_mirrored')
res['mask_area_m2_at_fitted_scale'] = {k: round(area_px / res[k]['scale_px_per_m'] ** 2, 0) for k in FITS}
res['picture_px'] = [W, H]
res['picture_width_m_if_grid_10m'] = round(W / 2.6, 1)
res['polygon_area_m2'] = {'outline_2013_m2p0': S['canonical']['area_m2'], 'toe_outline': S['canonical']['toe_area_m2']}

canvas = img.resize((W * 4, H * 4), Image.LANCZOS)
d = ImageDraw.Draw(canvas)
for name, colr in (('outline_2013_m2p0_mirrored', (255, 0, 0)), ('toe_outline_mirrored', (0, 160, 255))):
    r = res[name]; ang, sc = r['rotation_deg'], r['scale_px_per_m']
    ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    ox = mw / 2 + r['shift_px'][0] + 4; oy = mh / 2 + r['shift_px'][1] + 4
    polys = polys_2013 if name.startswith('outline') else polys_toe
    for poly in polys:
        P = (np.array(poly) - c0) * np.array([-1.0, 1.0])
        X = (P[:, 0] * ca - P[:, 1] * sa) * sc + ox
        Y = -(P[:, 0] * sa + P[:, 1] * ca) * sc + oy
        d.line([(x * 4, y * 4) for x, y in zip(X, Y)] + [(X[0] * 4, Y[0] * 4)], fill=colr, width=2)
d.text((8, 6), 'Mead & Borrero 2011 Fig 3 bottom + best-fit overlay: red = -2.0 m outline, blue = toe outline (grid interval not labelled)', fill=(255, 255, 255))
canvas.save(R + '3d/annotated/mmr_meadborrero2011_fig3b_layout_check.png')
json.dump(res, open(R + '3d/fig3_asbuilt_check.json', 'w'), indent=1)
print(json.dumps({k: res[k] for k in res if k not in FITS}))
for k in FITS:
    print(k, {x: y for x, y in res[k].items() if x != 'best_iou_by_scale'}, res[k]['best_iou_by_scale'])

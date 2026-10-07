import sys, json, os, numpy as np
sys.path.insert(0, '.')
from geo_tools import *
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
polys = json.load(open(ROOT + 'work_polys_fig3_m20_v2.json'))
im = np.array(Image.open(ROOT + 'src/linz_aerial_2010-11_BD37_1000_1314_crop.png').convert('RGB')).astype(float)
H, W, _ = im.shape
bright = ndi.binary_dilation(im.sum(2) > 400, iterations=3)
idx = ndi.distance_transform_edt(bright, return_distances=False, return_indices=True)
imm = np.stack([im[:, :, c][idx[0], idx[1]] for c in range(3)], 2)
def feat_maps(sig):
    sm = ndi.gaussian_filter(imm, [sig, sig, 0])
    red = sm[..., 0] - 0.5 * (sm[..., 1] + sm[..., 2])
    dark = -sm.mean(2)
    return {'red': red, 'dark': dark, 'red+dark': (red - red.mean()) / red.std() + (dark - dark.mean()) / dark.std()}
mask = Image.new('L', (W, H), 0); d = ImageDraw.Draw(mask)
for p in polys:
    pts = [tuple(f3_to_lz(x, y)) for x, y in p]; d.polygon(pts, fill=255)
M = np.array(mask) > 0
Mf = ndi.gaussian_filter(M.astype(float), 8)
ys, xs = np.nonzero(M)
cy, cx = int(ys.mean()), int(xs.mean())
R0 = 600     # window half-size px (75 m)
sl = (slice(max(cy - R0, 0), min(cy + R0, H)), slice(max(cx - R0, 0), min(cx + R0, W)))
res = {}
for name, fm in feat_maps(8).items():
    F = fm[sl]; F = (F - F.mean()) / F.std()
    best = None
    scores = {}
    for dy in range(-80, 81, 4):          # +-10 m in 0.5 m steps
        for dx in range(-80, 81, 4):
            Ms = np.roll(np.roll(Mf, dy, 0), dx, 1)[sl]
            Ms = (Ms - Ms.mean()) / Ms.std()
            sc = float((F * Ms).mean())
            scores[(dx, dy)] = sc
            if best is None or sc > best[0]: best = (sc, dx, dy)
    # refine
    sc0, bx, by = best
    for dy in range(by - 4, by + 5):
        for dx in range(bx - 4, bx + 5):
            Ms = np.roll(np.roll(Mf, dy, 0), dx, 1)[sl]; Ms = (Ms - Ms.mean()) / Ms.std()
            sc = float((F * Ms).mean())
            if sc > best[0]: best = (sc, dx, dy)
    sc, dx, dy = best
    res[name] = dict(score=round(sc, 3), score_at_zero=round(scores[(0, 0)], 3), shift_px_right=dx, shift_px_down=dy, shift_E_m=round(dx * LZ_PX, 2), shift_N_m=round(-dy * LZ_PX, 2))
    print(name, res[name])
json.dump(res, open(ROOT + 'work_aerial_registration.json', 'w'), indent=1)

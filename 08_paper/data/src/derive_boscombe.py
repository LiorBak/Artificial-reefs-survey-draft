"""Boscombe: rebuild the default idealised loft of METHODS_3D E10 (r = clip(r0 + phi/m, 0, Hc), r0 = 1.0 m, m = 3, crest +0.5 m ACD) on the model.js seabed
and extract the same profile metrics as derive_profiles.py. model.js seabed z_cm is in m MSL (checked: mean bed under the outline = -3.56 m ACD as in METHODS_3D KN); crest +0.5 m ACD = -0.90 m MSL."""
import sys, json
sys.path.insert(0, '/home/user/artificial-reef-survey/08_paper/data/src')
from derive_profiles import load
import numpy as np
from shapely.geometry import Polygon, Point
m = load('boscombe-surf-reef'); sb = m['seabed']; r = m['reef']
nx, ny = sb['nx'], sb['ny']; Z = np.array(sb['z_cm'], float).reshape(ny, nx) / 100.0
poly = r['toe_polygon_xyzz']; pts = [(p[0], p[1]) for p in poly]
P = Polygon(pts); print('poly area', round(P.area, 1), 'bounds', [round(x, 1) for x in P.bounds])
STEP = 1.0; xs = np.arange(P.bounds[0] - 6, P.bounds[2] + 6, STEP); ys = np.arange(P.bounds[1] - 6, P.bounds[3] + 6, STEP)
def S(x, y):
    fx = (x - sb['x0']) / sb['dx']; fy = (y - sb['y0']) / sb['dy']; i, j = int(fx), int(fy); tx, ty = fx - i, fy - j
    return Z[j, i] * (1 - tx) * (1 - ty) + Z[j, i + 1] * tx * (1 - ty) + Z[j + 1, i] * (1 - tx) * ty + Z[j + 1, i + 1] * tx * ty
zc = -0.90; r0 = 1.0; mrun = 3.0
H = np.full((len(ys), len(xs)), np.nan); B = np.full_like(H, np.nan)
for a, y in enumerate(ys):
    for b, x in enumerate(xs):
        s = S(x, y); B[a, b] = s
        d = Point(x, y).distance(P.exterior); phi = d if P.contains(Point(x, y)) else -d
        hc = max(zc - s, 0); rr = min(max(r0 + phi / mrun, 0), hc)
        if rr > 0: H[a, b] = s + rr
valid = np.isfinite(H); print('loft cells', int(valid.sum()), 'area', float(valid.sum() * STEP ** 2))
zmax = np.nanmax(H); jj, ii = np.unravel_index(np.nanargmax(H), H.shape)
res = {}
cols = []
for b in range(len(xs)):
    col = H[:, b]; ok = np.where(np.isfinite(col))[0]
    if len(ok) < 5: continue
    zm = col[ok].max(); yt = ys[ok[-1]]; plateau = ys[ok][col[ok] >= zm - 0.25]; yc = plateau.max()
    toe_d_msl = -B[ok[-1], b]; crest_d_msl = -zm
    cols.append(dict(x=float(xs[b]), y_toe=float(yt), y_crest=float(yc), toe_depth_msl=float(toe_d_msl), crest_depth_msl=float(crest_d_msl), ramp=float(yt - yc), gap=float(toe_d_msl - crest_d_msl), bed_at_crest_msl=float(-B[np.where(ys == yc)[0][0], b])))
def stat(k):
    a = np.array([c[k] for c in cols]); return [float(np.median(a)), float(np.percentile(a, 10)), float(np.percentile(a, 90))]
# transect at the alongshore centre of the crest plateau
pl_j, pl_i = np.where(H >= zmax - 0.05); xc = xs[int(np.round(pl_i.mean()))]
tc = min(cols, key=lambda c: abs(c['x'] - xc))
out = dict(slug='boscombe-surf-reef', method='loft of METHODS_3D E10 on model.js seabed (m MSL); crest -0.90 m MSL = +0.5 m ACD', crest_depth_msl_m=float(-zmax), crest_acd=float(zmax + 1.40), x_crest_centre=float(xc),
           transect=tc, medians={k: stat(k) for k in ('toe_depth_msl', 'crest_depth_msl', 'ramp', 'gap')}, n_columns=len(cols),
           bed_under_outline_acd_mean=float(np.nanmean(B[valid]) + 1.40), bed_under_outline_msl_range=[float(-np.nanmax(B[valid])), float(-np.nanmin(B[valid]))],
           y_extent=[float(ys[np.where(valid.any(axis=1))[0].min()]), float(ys[np.where(valid.any(axis=1))[0].max()])], x_extent=[float(xs[np.where(valid.any(axis=0))[0].min()]), float(xs[np.where(valid.any(axis=0))[0].max()])])
json.dump(out, open('/home/user/artificial-reef-survey/08_paper/data/profile_boscombe.json', 'w'), indent=1)
print(json.dumps(out)[:1500])

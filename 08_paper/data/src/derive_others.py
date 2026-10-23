"""Profile metrics for Palm Beach (reef grid + seabed grid in model.js) and Mount Maunganui (2013 multibeam DEM in model.js 'survey2013'). READ ONLY on model.js.
Same definitions as derive_profiles.py (crest-transect at the alongshore position of the shallowest cell; median over columns)."""
import sys, json
sys.path.insert(0, '/home/user/artificial-reef-survey/08_paper/data/src')
from derive_profiles import load
import numpy as np
def metrics(Z, x0, y0, step, bed, tolc=0.25, label=''):
    ny, nx = Z.shape; jj, ii = np.unravel_index(np.nanargmax(Z), Z.shape); zmax = float(np.nanmax(Z))
    def col(i, tol):
        c = Z[:, i]; ok = np.where(np.isfinite(c))[0]
        if len(ok) < 5: return None
        zm = c[ok].max(); ys = y0 + ok * step; yt = ys[-1]; yc = ys[c[ok] >= zm - tol].max(); x = x0 + i * step
        td = -bed(x, yt); cd = -zm
        return dict(x=float(x), y_toe=float(yt), y_crest_edge=float(yc), toe_depth=float(td), crest_depth=float(cd), ramp=float(yt - yc), gap=float(td - cd), slope=float((td - cd) / (yt - yc)) if yt > yc else None, bed_at_crest_edge=float(-bed(x, yc)), n=int(len(ok)))
    allc = [c for c in (col(i, tolc) for i in range(nx)) if c]
    res = dict(label=label, grid_step_m=step, crest_depth_msl_m=-zmax, crest_cell_xy=[float(x0 + ii * step), float(y0 + jj * step)],
               transect_at_crest={str(t): col(int(ii), t) for t in (0.10, 0.25, 0.50)}, n_columns=len(allc),
               y_extent=[float(y0 + np.where(np.isfinite(Z).any(axis=1))[0].min() * step), float(y0 + np.where(np.isfinite(Z).any(axis=1))[0].max() * step)])
    for k in ('toe_depth', 'crest_depth', 'ramp', 'gap', 'slope'):
        a = np.array([c[k] for c in allc if c[k] is not None]); res[f'median_over_columns_{k}'] = float(np.median(a)); res[f'p10_{k}'] = float(np.percentile(a, 10)); res[f'p90_{k}'] = float(np.percentile(a, 90))
    return res
out = {}
# --- Palm Beach
m = load('palm-beach-gold-coast'); sb = m['seabed']; g = m['reef']['grid']
S = np.array(sb['z_cm'], float).reshape(sb['ny'], sb['nx']) / 100.0
def bedp(x, y):
    fx = min(sb['nx'] - 1.001, max(0, (x - sb['x0']) / sb['dx'])); fy = min(sb['ny'] - 1.001, max(0, (y - sb['y0']) / sb['dx'])); i, j = int(fx), int(fy); tx, ty = fx - i, fy - j
    return S[j, i] * (1 - tx) * (1 - ty) + S[j, i + 1] * tx * (1 - ty) + S[j + 1, i] * (1 - tx) * ty + S[j + 1, i + 1] * tx * ty
Z = np.array(g['z_cm'], float).reshape(g['ny'], g['nx']); Z = np.where(Z == g['nodata'], np.nan, Z / 100.0)
print('PB reef z range', np.nanmin(Z), np.nanmax(Z), 'seabed z at centre', bedp(0, 300))
out['palm-beach-gold-coast'] = metrics(Z, g['x0'], g['y0'], g['dx'], bedp, label='reef grid (absolute z, m MSL) + seabed grid; version = model default')
# --- Mount Maunganui 2013 DEM
m = load('mount-maunganui-reef'); s = m['survey2013']; G = s['grid']; print('MM grid keys', {k: (v if not hasattr(v, '__len__') or len(str(v)) < 60 else '...') for k, v in G.items()}, 'nodata', s.get('nodata'))
out['palm-beach-gold-coast']['version'] = 'model default (council footprint, toe 11,972 m2)'; out['palm-beach-gold-coast']['slug'] = 'palm-beach-gold-coast'
PP = '/home/user/artificial-reef-survey/08_paper/data/profiles_derived.json'
d = json.load(open(PP)); d.update(out); json.dump(d, open(PP, 'w'), indent=1)
p = out['palm-beach-gold-coast']; t = p['transect_at_crest']['0.25']
print('PB crest', p['crest_depth_msl_m'], p['crest_cell_xy'], 'transect', {k: round(v, 2) if isinstance(v, float) else v for k, v in t.items()}, 'medians', {k: round(p[f'median_over_columns_{k}'], 2) for k in ('toe_depth', 'crest_depth', 'ramp', 'gap', 'slope')})

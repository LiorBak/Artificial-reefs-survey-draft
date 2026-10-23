"""Derive crest / toe / ramp metrics from the audited 3D model grids (07_scale/shapes/<slug>/3d/model.js, READ ONLY).
Applies to the four models whose grid is absolute z in cm MSL (int16, -32768 = outside) on a regular x/y grid with a bilinear seabed z[ny][nx] in m MSL:
borth-coastal-defence-reef, cables-reef-wa, narrowneck-gold-coast, southern-ocean-surf-reef-albany.
Run:  python3 -I derive_profiles.py   (writes profiles_derived.json next to this file's parent: ../profiles_derived.json)
Method (DERIVED, see README): frame y = offshore, shoreline at y=0 (per model frame). z up, 0 = MSL.
 crest depth = -max(z) over the reef surface (shallowest point). x* = alongshore position of that cell.
 transect = the grid column(s) at x*; toe = seaward-most valid cell of the column (outline edge); toe depth = -bed(x*, y_toe).
 crest edge = seaward-most cell of the column with z >= zmax_col - TOL; ramp = y_toe - y_crestedge; gap = toe depth - crest depth;
 slope = gap/ramp. Sensitivity: TOL 0.10 / 0.25 / 0.50 m. Also median over all columns that have >= 5 valid cells."""
import json, base64, sys, os
import numpy as np
ROOT = '/home/user/artificial-reef-survey'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'profiles_derived.json')

def load(slug):
    t = open(f'{ROOT}/07_scale/shapes/{slug}/3d/model.js', encoding='utf8').read()
    return json.loads(t[t.index('{', t.index('window.REEF_MODEL')):t.rindex('}') + 1])

def grid(v):
    G = v['grid']; H = np.frombuffer(base64.b64decode(G['h_cm_b64']), dtype='<i2').reshape(G['ny'], G['nx']).astype(float)
    Z = np.where(H == -32768, np.nan, H / 100.0)
    return G, Z

def bed_fn(m):
    SB = m['seabed']; z = np.array(SB['z'], float)
    def f(x, y):
        fx = min(SB['nx'] - 1.001, max(0, (x - SB['x0']) / SB['step'])); fy = min(SB['ny'] - 1.001, max(0, (y - SB['y0']) / SB['step']))
        i, j = int(fx), int(fy); tx, ty = fx - i, fy - j
        return z[j][i] * (1 - tx) * (1 - ty) + z[j][i + 1] * tx * (1 - ty) + z[j + 1][i] * (1 - tx) * ty + z[j + 1][i + 1] * tx * ty
    return f

def col_metrics(Z, G, bed, i, tol):
    col = Z[:, i]; ok = np.where(~np.isnan(col))[0]
    if len(ok) < 5: return None
    x = G['x0'] + i * G['step']; ys = G['y0'] + ok * G['step']
    zc = col[ok]; zmax = zc.max()
    jt = ok[-1]; yt = G['y0'] + jt * G['step']
    inside = ys[zc >= zmax - tol]
    yc = inside.max()
    toe_d = -bed(x, yt); crest_d = -zmax
    ramp = yt - yc
    return dict(x=x, y_toe=yt, y_crest_edge=float(yc), y_crest_inshore=float(inside.min()), toe_depth=float(toe_d), crest_depth=float(crest_d),
                ramp=float(ramp), gap=float(toe_d - crest_d), slope=(float((toe_d - crest_d) / ramp) if ramp > 0 else None),
                y_first=float(ys.min()), n=int(len(ok)), bed_at_crest_edge=float(-bed(x, yc)), toe_surface_minus_bed=float(col[jt] - bed(x, yt)))

THICKNESS = {'southern-ocean-surf-reef-albany'}      # grid = thickness above the seabed (viewer: z = seaAt + h/100); the others are absolute z (m MSL)
SPLIT_X = {'borth-coastal-defence-reef': 'auto'}     # two mounds (north surf reef + south oval breakwater): keep the north one (x below the gap)

def run(slug):
    m = load(slug); v = [x for x in m['versions'] if x['id'] == m['default_version']][0]
    G, Z = grid(v); bed = bed_fn(m)
    if slug in THICKNESS:
        for j in range(G['ny']):
            for i in range(G['nx']):
                if not np.isnan(Z[j, i]): Z[j, i] = bed(G['x0'] + i * G['step'], G['y0'] + j * G['step']) + Z[j, i]
    if slug in SPLIT_X:
        cnt = np.isfinite(Z).sum(axis=0); xs_ = G['x0'] + np.arange(G['nx']) * G['step']
        win = (xs_ > -40) & (xs_ < 60); xsplit = float(xs_[win][np.argmin(cnt[win])])
        Z[:, xs_ >= xsplit] = np.nan
        print('   Borth split x =', xsplit)
    jj, ii = np.unravel_index(np.nanargmax(Z), Z.shape)
    zmax = float(np.nanmax(Z)); xs = G['x0'] + ii * G['step']; ys = G['y0'] + jj * G['step']
    res = dict(slug=slug, version=v['id'], grid_step_m=G['step'], crest_depth_msl_m=-zmax, crest_cell_xy=[float(xs), float(ys)],
               area_grid_m2=float(np.isfinite(Z).sum() * G['step'] ** 2), y_min_m=float(G['y0'] + np.where(np.isfinite(Z).any(axis=1))[0].min() * G['step']),
               y_max_m=float(G['y0'] + np.where(np.isfinite(Z).any(axis=1))[0].max() * G['step']),
               x_min_m=float(G['x0'] + np.where(np.isfinite(Z).any(axis=0))[0].min() * G['step']), x_max_m=float(G['x0'] + np.where(np.isfinite(Z).any(axis=0))[0].max() * G['step']))
    # seabed depth range under the footprint
    bs = [-bed(G['x0'] + i * G['step'], G['y0'] + j * G['step']) for j, i in zip(*np.where(np.isfinite(Z)))]
    res['bed_depth_under_footprint_m'] = dict(min=float(min(bs)), max=float(max(bs)), mean=float(np.mean(bs)))
    # plateau (cells within 0.10 m of the max): centroid
    pj, pi = np.where(Z >= zmax - 0.10)
    res['crest_plateau_cells_within_0.10m'] = int(len(pj)); res['crest_plateau_centroid_xy'] = [float(G['x0'] + pi.mean() * G['step']), float(G['y0'] + pj.mean() * G['step'])]
    res['transect_at_crest'] = {str(t): col_metrics(Z, G, bed, int(ii), t) for t in (0.10, 0.25, 0.50)}
    allc = [col_metrics(Z, G, bed, i, 0.25) for i in range(G['nx'])]; allc = [c for c in allc if c]
    for k in ('toe_depth', 'crest_depth', 'ramp', 'gap', 'slope'):
        a = np.array([c[k] for c in allc if c[k] is not None], float)
        res[f'median_over_columns_{k}'] = float(np.median(a)); res[f'p10_{k}'] = float(np.percentile(a, 10)); res[f'p90_{k}'] = float(np.percentile(a, 90))
    res['n_columns'] = len(allc)
    # whole-reef seaward toe: the deepest bed depth at any outline edge cell facing offshore (max y per column)
    res['toe_depth_max_over_columns_m'] = float(max(c['toe_depth'] for c in allc))
    res['seaward_extent_y_max_m'] = res['y_max_m']
    # save the transect profile at the crest column
    i = int(ii); prof = []
    for j in range(G['ny']):
        y = G['y0'] + j * G['step']
        prof.append((float(y), None if np.isnan(Z[j, i]) else float(Z[j, i]), float(bed(G['x0'] + i * G['step'], y))))
    res['profile_at_crest_column'] = prof
    return res

if __name__ == '__main__':
    slugs = sys.argv[1:] or ['borth-coastal-defence-reef', 'cables-reef-wa', 'narrowneck-gold-coast', 'southern-ocean-surf-reef-albany']
    out = {}
    if os.path.exists(OUT): out = json.load(open(OUT))
    for s in slugs:
        out[s] = run(s)
    json.dump(out, open(OUT, 'w'), indent=1)
    for s in slugs:
        r = out[s]; t = r['transect_at_crest']['0.25']
        print(s, r['version'], 'crest_depth', round(r['crest_depth_msl_m'], 2), 'crest xy', r['crest_cell_xy'], '| transect tol.25', {k: (round(x, 2) if isinstance(x, float) else x) for k, x in t.items()})
        print('   median cols: toe', round(r['median_over_columns_toe_depth'], 2), 'crest', round(r['median_over_columns_crest_depth'], 2), 'ramp', round(r['median_over_columns_ramp'], 1), 'slope', round(r['median_over_columns_slope'], 3), '| area', round(r['area_grid_m2']), 'y', r['y_min_m'], r['y_max_m'], 'bed under', {k: round(x, 2) for k, x in r['bed_depth_under_footprint_m'].items()})

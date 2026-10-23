#!/usr/bin/env python3
"""post_break.py - how far a reef keeps the wave breaking after the break point, on several lines per reef (Section 4.3).

Run:    python3 08_paper/analysis/post_break.py            (add --fig to redraw Figure E2)
Reads:  reef_inputs.py (main-cut profiles from 08_paper/data/profiles/<slug>.json, tidal planes), results_reef_summary.csv
        (rep_line = the Table 2 / Figure 1 cut, outcome score), and the 3D-model grids through extract_profiles.py
        (load_model + ADAPTERS + layer_from: the same seabed, reef surface and footprint rule; 07_scale/shapes/<slug>/3d/,
        read only)
Writes: results_post_break.csv (one row per reef x line x tide x Hb, plus one summary row per reef x line),
        results_post_break_summary.csv (per reef: the median of every line + the Spearman rows),
        results_post_break_lines.json (geometry of every line: rule, anchor, direction, ridge-path vertices),
        figures/figE2_post_break_lines.png/.pdf (with --fig)

Lines (Lior's review of 2026-10-19: "Palm Beach gets 27 m but Figure 1 shows ~100 m of reef"):
  main    : the Figure 1 / Table 2 cut (rep_line; Narrowneck second crest line, Pratte's centreline), for continuity.
  sn25, sn50, sn75 : shore-normal lines at 25 %, 50 % and 75 % of the alongshore extent of the reef footprint measured from
            its LEFT end as seen in Figure 1 (looking seaward). Alongshore coordinate u = projection on the left-pointing
            shore-parallel unit vector l = (d_y, -d_x), d = offshore shore normal in the model frame (model +y for every reef
            but Cables; Cables: perpendicular to the fitted 0 m AHD shoreline, bearing 7.8 deg T, as its Figure 1 cut). In every
            model frame +x points to the left looking seaward (Figure 1 plots -x). The extent is u_max - u_min of the footprint
            cells (thickness >= 0.10 m); the line at fraction f passes through u = u_max - f (u_max - u_min).
  crest   : the LONGEST CREST (RIDE) LINE. Ridge cells = footprint cells whose reef surface is within DZ_CREST = 1.0 m of the
            shallowest reef cell (the band over which a wave that breaks at the crest still finds breaking depth for
            Hb = 1-2 m); gaps up to 3 m are bridged (binary closing) and the largest 8-connected group is kept. The line starts
            at the most seaward ridge cell (where an incoming wave first finds the ridge: the take-off) and ends at the ridge
            cell farthest from it measured along the ridge (geodesic distance inside the ridge cells); between the two the
            path follows the shallowest cells (edge cost = length x (1 + 2 (z_max - z)/DZ_CREST)), is smoothed over 5 m and
            resampled every 1 m with the same bilinear sampling as extract_profiles.py. DZ_CREST = 0.5 and 1.5 m are run as
            sensitivity. The geodesic diameter of the ridge (longest ridge path between any two cells) is also reported.

Breaking model (DERIVED, 1-D, idealised), unchanged from the first version for the shore-normal lines: at low / mid (MSL) /
high water and Hb = 1.0, 1.5, 2.0 m the wave breaks at the first point from offshore where h <= Hb / 0.78 (McCowan), then
  L_dally : Dally, Dean & Dalrymple (1985) energy-flux decay, d(H^2 h^0.5)/dx = -(K/h)(H^2 h^0.5 - (G h)^2 h^0.5), K = 0.15,
            G = 0.4, integrated shoreward on the 1 m grid from Hb; breaking stops where H <= G h (or at the shoreline,
            h <= 0.05 m: flag to_shore);
  L_simple: to the first point where h > Hb / 0.4 (Hb held, upper bound);
  L_reef_supported = min(L_dally, reef length shoreward of the break) = the breaking-length metric of the shore-normal lines.
On the crest line the wave does not travel along the line: it breaks progressively along the arm (peels), each point of the
arm breaking when the still-unbroken part of the crest reaches it. The crest metric is therefore
  L_peel  : length along the crest line from the first point where h <= Hb/0.78 to the end of the contiguous stretch where
            0.05 m < h <= Hb/0.78 (the arm keeps the wave breaking);
  L_dally is also computed along the crest line (as if the broken wave travelled along it), reported only as a check.
Per reef and line: median and max over the on-reef cases (3 heights x 3 water levels); Spearman rho of the medians against
the outcome score (summarize.OUTCOME_SCORE; permutation p from summarize.perm_p), Borth (unknown) excluded.
Limits: normal incidence on the shore-normal lines, no refraction, no 2-D spreading, no set-up, no friction, model surfaces
(survey or idealised, see profiles/SUMMARY.md); the crest-line rule is a geometric judgement documented here.
"""
import csv
import json
import math
import os
import sys

import numpy as np
from scipy import ndimage as ndi
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import dijkstra

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import reef_inputs as RI  # noqa: E402
import extract_profiles as E  # noqa: E402
from surf_analysis import prof_arrays  # noqa: E402

H_SET = [1.0, 1.5, 2.0]
GAMMA_B, GAMMA_S, K = 0.78, 0.4, 0.15
H_SHORE = 0.05
FRACS = [('sn25', 0.25), ('sn50', 0.50), ('sn75', 0.75)]
DZ_CREST = 1.0
DZ_SENS = [0.5, 1.5]
BRIDGE_M = 3.0
SMOOTH_M = 5.0
LINE_IDS = ['main', 'sn25', 'sn50', 'sn75', 'crest']
LINE_NAMES = {'main': 'Figure 1 / Table 2 cut', 'sn25': 'shore-normal, 25 % from the left', 'sn50': 'shore-normal, 50 %',
              'sn75': 'shore-normal, 75 % from the left', 'crest': 'longest crest (ride) line'}


def dally_length(y, h, i0, Hb):
    """Distance from index i0 (break) shoreward until H <= GAMMA_S*h (Dally et al. 1985 decay); None if it reaches shore."""
    G = Hb ** 2 * np.sqrt(h[i0])
    for i in range(i0 + 1, len(y)):
        dx = y[i - 1] - y[i]
        hm = 0.5 * (h[i - 1] + h[i])
        if h[i] <= H_SHORE or hm <= H_SHORE:
            return None, i
        Gs = (GAMMA_S * hm) ** 2 * np.sqrt(hm)
        G = G - K / hm * (G - Gs) * dx
        H = np.sqrt(max(G, 0.0) / np.sqrt(h[i]))
        if H <= GAMMA_S * h[i]:
            return y[i0] - y[i], i
    return None, len(y) - 1


# ----------------------------------------------------------------------------- geometry
def shore_normal(slug, a):
    """unit offshore shore normal (dx, dy) in the model frame (as the Figure 1 cut of extract_profiles.py)"""
    ov = E.CUT_OVERRIDES.get(slug)
    if ov and ov['normal'] != 'model_y':
        ts = a['true_shoreline']
        for b in (ov['normal'][1] - 90.0, ov['normal'][1] + 90.0):
            v = (math.cos(math.radians(b - ts['x_bearing'])), math.cos(math.radians(b - ts['y_bearing'])))
            if v[1] > 0:
                n = math.hypot(*v)
                return (v[0] / n, v[1] / n)
    return (0.0, 1.0)


def load_geom(slug):
    m, mp = E.load_model(slug)
    a = E.ADAPTERS[slug](m, mp)
    layer = E.layer_from(a['rx'], a['ry'], a['RZ'], a['seabed'], a.get('mask'))
    cc = E.crest_and_centre(layer['rx'], layer['ry'], layer['RZ'], layer['X'], layer['Y'], layer['foot'])
    return a, layer, cc, shore_normal(slug, a)


def shore_normal_line(fid, f, a, layer, cc, d):
    X, Y, foot = layer['X'], layer['Y'], layer['foot']
    lv = (d[1], -d[0])                                   # left looking seaward (model +x side)
    U = X * lv[0] + Y * lv[1]
    umin, umax = float(U[foot].min()), float(U[foot].max())
    uf = umax - f * (umax - umin)
    cx, cy = cc['x_centroid'], cc['y_centroid']
    uc = cx * lv[0] + cy * lv[1]
    px, py = cx + (uf - uc) * lv[0], cy + (uf - uc) * lv[1]
    oblique = abs(d[0]) > 1e-9
    blk = E.line_block(fid, px, layer, a['seabed'], cc['y_range'][1], None, '', y_anchor=py if oblique else None,
                       direction=d if oblique else None)
    geo = dict(rule='shore-normal line at %.0f %% of the alongshore extent of the footprint from its left end (looking '
                    'seaward)' % (100 * f), anchor_xy_m=[round(px, 2), round(py, 2)], direction_xy=[round(d[0], 5), round(d[1], 5)],
               alongshore_extent_m=round(umax - umin, 1), reef_run_xy_m=blk.get('reef_run_xy_m'))
    return blk, geo


def ridge_path(layer, seabed, cc, dz, d):
    """longest crest (ride) line: see module docstring. Returns dict with s, x, y, zs, zr, zb and geometry info, or None."""
    rx, ry, RZ, foot = layer['rx'], layer['ry'], layer['RZ'], layer['foot']
    dx = float(rx[1] - rx[0])
    zmax = cc['zmax']
    S = foot & (RZ >= zmax - dz)
    r = max(1, int(round(BRIDGE_M / 2 / dx)))
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    S = ndi.binary_closing(S, structure=(xx ** 2 + yy ** 2) <= r * r) | S
    lab, n = ndi.label(S, structure=np.ones((3, 3)))
    if n == 0:
        return None
    big = np.argmax(np.bincount(lab.ravel())[1:]) + 1
    C = lab == big
    iy, ix = np.nonzero(C)
    N = len(iy)
    idx = -np.ones(C.shape, int)
    idx[iy, ix] = np.arange(N)
    zc = np.clip(np.where(np.isfinite(RZ[iy, ix]), RZ[iy, ix], zmax - dz), zmax - dz, zmax)
    rows, cols, wg, wl = [], [], [], []
    for oy, ox in ((0, 1), (1, 0), (1, 1), (1, -1)):
        jy, jx = iy + oy, ix + ox
        ok = (jy >= 0) & (jy < C.shape[0]) & (jx >= 0) & (jx < C.shape[1])
        ok[ok] = C[jy[ok], jx[ok]]
        a_, b_ = np.arange(N)[ok], idx[jy[ok], jx[ok]]
        ln = dx * math.hypot(oy, ox)
        rows += [a_]
        cols += [b_]
        wl += [np.full(len(a_), ln)]
        wg += [ln * (1 + 2 * (zmax - 0.5 * (zc[a_] + zc[b_])) / dz)]
    rows, cols = np.concatenate(rows), np.concatenate(cols)
    GL = coo_matrix((np.concatenate(wl), (rows, cols)), shape=(N, N)).tocsr()
    GW = coo_matrix((np.concatenate(wg), (rows, cols)), shape=(N, N)).tocsr()
    xs, ys = rx[ix], ry[iy]
    off = xs * d[0] + ys * d[1]
    start = int(np.argmax(off))                       # most seaward ridge cell = take-off
    dist = dijkstra(GL, directed=False, indices=start)
    end = int(np.argmax(np.where(np.isfinite(dist), dist, -1)))
    # geodesic diameter (double sweep), for information
    d1 = dijkstra(GL, directed=False, indices=end)
    far = int(np.argmax(np.where(np.isfinite(d1), d1, -1)))
    diam = float(d1[far])
    _, pred = dijkstra(GW, directed=False, indices=start, return_predecessors=True)
    path = [end]
    while path[-1] != start:
        path.append(int(pred[path[-1]]))
    path = path[::-1]
    px, py = xs[path].astype(float), ys[path].astype(float)
    w = max(1, int(round(SMOOTH_M / dx)))
    if len(px) > 2 * w + 1:
        k = np.ones(2 * w + 1) / (2 * w + 1)
        sx = np.convolve(np.pad(px, w, mode='edge'), k, 'valid')
        sy = np.convolve(np.pad(py, w, mode='edge'), k, 'valid')
        sx[0], sy[0], sx[-1], sy[-1] = px[0], py[0], px[-1], py[-1]
        px, py = sx, sy
    seg = np.hypot(np.diff(px), np.diff(py))
    sc = np.concatenate([[0], np.cumsum(seg)])
    s = np.arange(0.0, sc[-1] + 1e-9, E.STEP)
    qx, qy = np.interp(s, sc, px), np.interp(s, sc, py)
    zb = np.asarray(seabed(qx, qy), float)
    zr = E.sample_reef(rx, ry, layer['RZf'], qx, qy)
    zs = np.where(np.isfinite(zr), np.maximum(zr, zb), zb)
    return dict(s=s, x=qx, y=qy, zb=zb, zr=zr, zs=zs, length_m=float(s[-1]), diameter_m=diam, n_cells=int(N),
                start_xy=[float(xs[start]), float(ys[start])], end_xy=[float(xs[end]), float(ys[end])], zmax=zmax, dz=dz)



# ----------------------------------------------------------------------------- breaking cases
def cases_profile(y, zb, zr, zs, tides, base):
    """shore-normal / main lines: y offshore coordinate, arrays ordered offshore -> shore (as prof_arrays)"""
    rows = []
    reef = np.isfinite(zr) & (zr > zb + 0.10)
    y_reef_shore = float(y[reef].min()) if reef.any() else float('nan')
    for tide, eta in tides.items():
        if eta is None:
            continue
        h = eta - zs
        for Hb in H_SET:
            r = dict(base, tide=tide, eta_msl_m=round(eta, 3), Hb_m=Hb,
                     h_crest_m=round(float(np.nanmin(h[reef])), 3) if reef.any() else '')
            hit = np.where(h <= Hb / GAMMA_B)[0]
            if not reef.any():
                r.update(status='no_reef_on_line')
                rows.append(r)
                continue
            if len(hit) == 0:
                r.update(status='no_break_on_profile')
                rows.append(r)
                continue
            i0 = int(hit[0])
            r.update(y_break_m=round(float(y[i0]), 1), h_break_m=round(float(h[i0]), 3), break_on_reef=bool(reef[i0]),
                     status='breaks_on_reef' if reef[i0] else 'breaks_seaward_of_reef',
                     reef_shoreward_of_break_m=round(float(y[i0] - y_reef_shore), 1))
            deep = np.where((h > Hb / GAMMA_S) & (np.arange(len(y)) > i0))[0]
            shore = np.where((h <= H_SHORE) & (np.arange(len(y)) > i0))[0]
            if len(deep) and (not len(shore) or deep[0] < shore[0]):
                r.update(L_simple_m=round(float(y[i0] - y[deep[0]]), 1), simple_to_shore=False)
            else:
                j = shore[0] if len(shore) else len(y) - 1
                r.update(L_simple_m=round(float(y[i0] - y[j]), 1), simple_to_shore=True)
            L, j = dally_length(y, h, i0, Hb)
            if L is None:
                r.update(L_dally_m=round(float(y[i0] - y[j]), 1), dally_to_shore=True)
            else:
                r.update(L_dally_m=round(float(L), 1), dally_to_shore=False)
            if r['break_on_reef']:
                r['L_metric_m'] = round(min(r['L_dally_m'], r['reef_shoreward_of_break_m']), 1)
            rows.append(r)
    return rows


def cases_crest(P, tides, base):
    rows = []
    s, zs = P['s'], P['zs']
    for tide, eta in tides.items():
        if eta is None:
            continue
        h = eta - zs
        for Hb in H_SET:
            r = dict(base, tide=tide, eta_msl_m=round(eta, 3), Hb_m=Hb, h_crest_m=round(float(np.nanmin(h)), 3),
                     reef_shoreward_of_break_m='')
            brk = (h <= Hb / GAMMA_B) & (h > H_SHORE)
            hit = np.where(brk)[0]
            if len(hit) == 0:
                r.update(status='crest_dry' if (h <= H_SHORE).all() else 'no_break_on_crest')
                rows.append(r)
                continue
            i0 = int(hit[0])
            j = i0
            while j + 1 < len(s) and brk[j + 1]:
                j += 1
            r.update(y_break_m=round(float(s[i0]), 1), h_break_m=round(float(h[i0]), 3), break_on_reef=True,
                     status='peels_along_crest', reef_shoreward_of_break_m=round(float(s[-1] - s[i0]), 1),
                     L_peel_m=round(float(s[j] - s[i0]), 1), peel_to_end=bool(j == len(s) - 1))
            L, jj = dally_length(-s, h, i0, Hb)
            r.update(L_dally_m=round(float(s[jj] - s[i0]) if L is None else float(L), 1), dally_to_shore=L is None)
            r['L_metric_m'] = r['L_peel_m']
            rows.append(r)
    return rows


def med(v):
    return round(float(np.median(v)), 1) if v else ''


def run():
    inp = RI.load()
    summ = {r['slug']: r for r in csv.DictReader(open(os.path.join(HERE, 'results_reef_summary.csv')))}
    rows, geom = [], {}
    for slug, d in inp.items():
        o = summ.get(slug, {})
        a, layer, cc, dvec = load_geom(slug)
        tides = d['tide_levels']
        g = geom[slug] = dict(shore_normal_xy=[round(dvec[0], 5), round(dvec[1], 5)],
                              left_note='left looking seaward = model +x side (Figure 1 plots -x; Cables rotated into its shoreline)')
        base0 = dict(slug=slug, outcome=o.get('outcome'))
        # main
        ml = o.get('rep_line') or 'crest_line'
        if ml not in d['lines']:
            ml = 'crest_line'
        y, zb, zr, zs = prof_arrays(d['lines'][ml])
        rows += cases_profile(y, zb, zr, zs, tides, dict(base0, line_id='main', line=ml))
        pj = json.load(open(os.path.join(RI.DATA, 'profiles', slug + '.json'), encoding='utf-8'))['lines'][ml]
        g['main'] = dict(rule='Figure 1 / Table 2 cut (%s of 08_paper/data/profiles/%s.json)' % (ml, slug),
                         reef_run_xy_m=pj.get('reef_run_xy_m'),
                         direction_xy=(pj.get('oblique') or {}).get('direction_xy', [0.0, 1.0]))
        for fid, f in FRACS:
            blk, gg = shore_normal_line(fid, f, a, layer, cc, dvec)
            y, zb, zr, zs = prof_arrays(blk)
            rows += cases_profile(y, zb, zr, zs, tides, dict(base0, line_id=fid, line=fid))
            g[fid] = gg
        for dz in [DZ_CREST] + DZ_SENS:
            P = ridge_path(layer, a['seabed'], cc, dz, dvec)
            lid = 'crest' if dz == DZ_CREST else 'crest_dz%.1f' % dz
            info = dict(rule='longest crest (ride) line, ridge cells within %.1f m of the shallowest reef cell (z >= %.2f m '
                             'MSL), from the most seaward ridge cell to the ridge cell farthest along the ridge' % (dz, cc['zmax'] - dz),
                        length_m=round(P['length_m'], 1), ridge_diameter_m=round(P['diameter_m'], 1), ridge_cells=P['n_cells'],
                        start_xy_m=[round(v, 2) for v in P['start_xy']], end_xy_m=[round(v, 2) for v in P['end_xy']])
            if dz == DZ_CREST:
                info['path_xy_m'] = [[round(float(x), 2), round(float(yv), 2)] for x, yv in zip(P['x'][::2], P['y'][::2])]
                info['path_z_msl_m'] = [None if not np.isfinite(z) else round(float(z), 2) for z in P['zs'][::2]]
            g[lid] = info
            rows += cases_crest(P, tides, dict(base0, line_id=lid, line=lid))
    # summaries per reef x line
    srows = []
    ids = LINE_IDS + ['crest_dz%.1f' % v for v in DZ_SENS]
    for slug in inp:
        o = summ.get(slug, {})
        rec = dict(slug=slug, outcome=o.get('outcome'), outcome_score=o.get('outcome_score'))
        for lid in ids:
            v = [r['L_metric_m'] for r in rows if r['slug'] == slug and r['line_id'] == lid and 'L_metric_m' in r]
            rec['n_%s' % lid] = len(v)
            rec['L_%s_median_m' % lid] = med(v)
            rec['L_%s_max_m' % lid] = round(float(max(v)), 1) if v else ''
            rows.append(dict(slug=slug, outcome=o.get('outcome'), line_id=lid, line=lid, tide='all', status='summary_on_reef_cases',
                             n_on_reef=len(v), L_median_m=med(v), L_max_m=rec['L_%s_max_m' % lid], outcome_score=o.get('outcome_score')))
        sn = [r['L_metric_m'] for r in rows if r['slug'] == slug and r['line_id'] in ('sn25', 'sn50', 'sn75') and 'L_metric_m' in r]
        rec['n_sn_all'] = len(sn)
        rec['L_sn_all_median_m'] = med(sn)
        rec['L_sn_best_median_m'] = max([rec['L_%s_median_m' % k] for k in ('sn25', 'sn50', 'sn75') if rec['L_%s_median_m' % k] != ''] or [''])
        rec['crest_length_m'] = geom[slug]['crest']['length_m']
        srows.append(rec)
    from scipy.stats import spearmanr
    from summarize import perm_p
    corr = {}
    for key in ['main', 'sn25', 'sn50', 'sn75', 'sn_all', 'sn_best', 'crest', 'crest_dz0.5', 'crest_dz1.5']:
        col = 'L_%s_median_m' % key
        ok = [r for r in srows if r['outcome_score'] not in (None, '') and r[col] != '']
        xs, ys = [float(r[col]) for r in ok], [float(r['outcome_score']) for r in ok]
        rho = spearmanr(xs, ys)[0]
        corr[key] = dict(rho=round(float(rho), 2), p_perm=round(perm_p(xs, ys), 3), n=len(ok))
    ok = [r for r in srows if r['outcome_score'] not in (None, '')]
    xs, ys = [float(r['crest_length_m']) for r in ok], [float(r['outcome_score']) for r in ok]
    corr['crest_line_length'] = dict(rho=round(float(spearmanr(xs, ys)[0]), 2), p_perm=round(perm_p(xs, ys), 3), n=len(ok))
    return rows, srows, corr, geom


def plan_figure(geom):
    """Figure E2: plan of each reef model (reef surface depth) with the lines used in post_break.py"""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import style as S
    S.setup()
    slugs = [s for s in S.SLUGS if s in geom]
    nc = 3
    nr = int(math.ceil(len(slugs) / nc))
    fig, axs = plt.subplots(nr, nc, figsize=(S.cm(17), S.cm(5.6 * nr)))
    for ax, slug in zip(axs.ravel(), slugs):
        a, layer, cc, d = load_geom(slug)
        lv = (d[1], -d[0])

        def uv(x, y):
            x, y = np.asarray(x, float), np.asarray(y, float)
            return -(x * lv[0] + y * lv[1]), x * d[0] + y * d[1]      # plotted x: left looking seaward = left
        U, V = uv(layer['X'], layer['Y'])
        sc = ax.pcolormesh(U, V, np.ma.masked_invalid(layer['RZf']), cmap='viridis', shading='nearest',
                           vmin=cc['zmax'] - 3.0, vmax=cc['zmax'], rasterized=True)
        fx = np.nonzero(layer['foot'])
        pad = max(1.0, 0.05 * np.ptp(U[fx]))
        ax.set_xlim(U[fx].min() - pad, U[fx].max() + pad)
        ax.set_ylim(V[fx].min() - pad, V[fx].max() + 2 * pad)
        g = geom[slug]
        for lid, st in (('main', dict(color='k', ls='--', lw=1.0)), ('sn25', dict(color='#D55E00', lw=0.8)),
                        ('sn50', dict(color='#D55E00', lw=0.8)), ('sn75', dict(color='#D55E00', lw=0.8))):
            rr = g[lid].get('reef_run_xy_m')
            if not rr:
                continue
            (xa, ya), (xb, yb) = rr
            u0, v0 = uv([xa, xb], [ya, yb])
            ax.plot(u0, v0, **st, zorder=4)
            if lid != 'main':
                ax.text(u0[1], v0[1], lid[2:], fontsize=5.5, color='#D55E00', ha='center', va='bottom')
        p = np.array(g['crest']['path_xy_m'])
        u0, v0 = uv(p[:, 0], p[:, 1])
        ax.plot(u0, v0, color='#CC79A7', lw=2.0, solid_capstyle='round')
        ax.plot(u0[0], v0[0], 'o', color='#CC79A7', ms=3)
        ax.set_aspect('equal')
        ax.set_title('%s (crest line %.0f m)' % (S.NAMES[slug], g['crest']['length_m']), fontsize=7, color=S.COLORS[slug])
        ax.tick_params(labelsize=5.5)
        cb = fig.colorbar(sc, ax=ax, fraction=0.04, pad=0.02)
        cb.ax.tick_params(labelsize=5)
        cb.set_label('reef surface (m MSL)', fontsize=5)
    for ax in axs.ravel()[len(slugs):]:
        ax.axis('off')
    fig.tight_layout()
    return S.save(fig, 'figE2_post_break_lines')


def main():
    rows, srows, corr, geom = run()
    keys = ['slug', 'outcome', 'line_id', 'line', 'tide', 'eta_msl_m', 'Hb_m', 'h_crest_m', 'status', 'y_break_m', 'h_break_m',
            'break_on_reef', 'reef_shoreward_of_break_m', 'L_simple_m', 'simple_to_shore', 'L_dally_m', 'dally_to_shore',
            'L_peel_m', 'peel_to_end', 'L_metric_m', 'n_on_reef', 'L_median_m', 'L_max_m', 'outcome_score']
    with open(os.path.join(HERE, 'results_post_break.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, '') for k in keys})
    sk = list(srows[0].keys())
    with open(os.path.join(HERE, 'results_post_break_summary.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=sk + ['note'])
        w.writeheader()
        for r in srows:
            w.writerow(r)
        for k, c in corr.items():
            w.writerow(dict(slug='SPEARMAN_%s' % k, note='rho %.2f, permutation p %.3f, n %d (median vs outcome score; Borth excluded)' % (c['rho'], c['p_perm'], c['n'])))
    json.dump(dict(script='08_paper/analysis/post_break.py', method=__doc__, lines=geom, spearman=corr),
              open(os.path.join(HERE, 'results_post_break_lines.json'), 'w'), indent=1)
    for r in srows:
        print('%-16s %-15s main %5s  sn25 %5s sn50 %5s sn75 %5s  crest %5s (n %d, len %5.0f)  dz0.5 %5s dz1.5 %5s' % (
            r['slug'][:16], r['outcome'], r['L_main_median_m'], r['L_sn25_median_m'], r['L_sn50_median_m'], r['L_sn75_median_m'],
            r['L_crest_median_m'], r['n_crest'], r['crest_length_m'], r['L_crest_dz0.5_median_m'], r['L_crest_dz1.5_median_m']))
    for k, c in corr.items():
        print('rho %-18s %5.2f p %.3f n %d' % (k, c['rho'], c['p_perm'], c['n']))
    if '--fig' in sys.argv:
        print(plan_figure(geom))


if __name__ == '__main__':
    main()

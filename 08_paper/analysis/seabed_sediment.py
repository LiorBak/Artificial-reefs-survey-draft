#!/usr/bin/env python3
"""seabed_sediment.py - sediment-transport signals around the built surf reefs, from the bathymetry data the project already holds.

Run (from anywhere):  python3 08_paper/analysis/seabed_sediment.py [cables] [boscombe] [borth] [navionics] [skips] [figures]
                      (no argument = everything).  Add  --scratch DIR  to change the scratch directory (default /tmp/claude-0/paper/seabed/run).
Reads  (READ ONLY): 07_scale/shapes/<slug>/ (model.js, shape.json, src/, 3d/src/) and 07_scale/bathymetry/.
Writes: 08_paper/analysis/seabed_sediment_results.json   (merged per reef; each reef block is rewritten when that reef is run)
        08_paper/figures/fig_sediment_<slug>.png          (+ fig_sediment_summary.png when 'figures' is run)
Needs : numpy, scipy, shapely (reef polygons), matplotlib, pyproj (through the Boscombe helper in 07_scale, imported read-only).

WHAT IS TESTED (same logic for every reef with MEASURED seabed data; assumed/synthetic seabeds are skipped and listed in 'skipped')
  T1  contour offset.  For alongshore transects every `dx` m, the cross-shore position Y_c(x) of the shoreline (0 m MSL/AHD/ODN) and of the
      -1/-2/-3 m (and deeper, where measured) contours.  LEE window = reef alongshore extent L (and 2L); CONTROL windows = |x - xc| from
      1.5 L to 3.5 L (data permitting).  anomaly = mean(Y_c in lee) - trend(Y_c from the control windows) interpolated to the lee.
      Positive anomaly = the contour lies FARTHER OFFSHORE (closer to the reef) in the lee than at the controls = salient/bulge.
      Uncertainty = PLACEBO windows: the same anomaly computed for width-L windows slid along the control strips (natural alongshore
      variability at this window width); z = anomaly / sd(placebo); n_indep = control length / L.
  T2  bed level.  Mean bed elevation in a lee band (fixed distance range from the shoreline) minus the same band at the controls (same machinery).
  T3  temporal change (only where >= 2 surveys exist): dz at the soundings of the later survey against a TIN of the earlier one
      (<= 25 m from an earlier sounding), binned; lee box minus control boxes (difference-in-differences); the pre-construction pair
      (1998 vs 1995) gives the noise floor.  Boscombe: beach-profile time series (CCO), before/after, lee lines vs control lines.
  T4  burial / toe scour: rings around the reef footprint and the reef surface itself (Cables).
Every result is DERIVED here; assumptions are tagged ASSUMPTION in the results JSON.  Nothing is written outside 08_paper/analysis,
08_paper/figures and the scratch directory.
"""
import json
import math
import os
import sys

import numpy as np
from scipy import ndimage as ndi
from scipy.interpolate import LinearNDInterpolator, RegularGridInterpolator
from scipy.spatial import cKDTree

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SHAPES = os.path.join(REPO, '07_scale', 'shapes')
OUT_JSON = os.path.join(REPO, '08_paper', 'analysis', 'seabed_sediment_results.json')
FIG_DIR = os.path.join(REPO, '08_paper', 'figures')
SCRATCH = '/tmp/claude-0/paper/seabed/run'
if '--scratch' in sys.argv:
    SCRATCH = sys.argv[sys.argv.index('--scratch') + 1]


# ----------------------------------------------------------------------------------------------------------------- utilities
def load_model(slug):
    s = open(os.path.join(SHAPES, slug, '3d', 'model.js'), encoding='utf-8').read()
    i = s.index('window.REEF_MODEL')
    j = s.index('=', i)
    return json.loads(s[j + 1:].strip().rstrip(';'))


def jdump(o):
    def conv(x):
        if isinstance(x, (np.floating,)):
            return None if not np.isfinite(x) else float(x)
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, np.ndarray):
            return [conv(v) for v in x.tolist()] if x.ndim else conv(x.item())
        if isinstance(x, float):
            return None if not np.isfinite(x) else x
        if isinstance(x, dict):
            return {str(k): conv(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [conv(v) for v in x]
        return x
    return conv(o)


def nan_gauss(z, sigma):
    """Normalised (NaN-aware) Gaussian smoothing; sigma in cells."""
    m = np.isfinite(z)
    num = ndi.gaussian_filter(np.where(m, z, 0.0), sigma, mode='nearest')
    den = ndi.gaussian_filter(m.astype(float), sigma, mode='nearest')
    out = np.where(den > 1e-6, num / np.maximum(den, 1e-12), np.nan)
    return np.where(m | (den > 0.5), out, np.nan)


def contour_cols(Z, ys, level, smooth_m=0.0, dy=None, shore_first=True, min_valid=2):
    """Cross-shore position of `level` for every column of Z (rows = offshore distance ys ascending, columns = alongshore).
    Returns the FIRST downward crossing (z >= level on the shore side, z < level farther offshore), linear interpolation, NaN if none
    or if the profile has no valid cell on either side.  A crossing is only accepted when both cells are measured (finite)."""
    out = np.full(Z.shape[1], np.nan)
    for j in range(Z.shape[1]):
        p = Z[:, j]
        ok = np.isfinite(p[:-1]) & np.isfinite(p[1:])
        idx = np.where(ok & (p[:-1] >= level) & (p[1:] < level))[0]
        if len(idx):
            i = idx[0] if shore_first else idx[-1]
            out[j] = ys[i] + (p[i] - level) / (p[i] - p[i + 1]) * (ys[i + 1] - ys[i])
    return out


def window_means(xs, vals, w, step):
    """Mean of vals over every window [x0, x0+w] inside the series; windows need >= 60 % valid samples."""
    res = []
    x0s = np.arange(xs.min(), xs.max() - w + 1e-9, step)
    for x0 in x0s:
        m = (xs >= x0) & (xs <= x0 + w) & np.isfinite(vals)
        tot = ((xs >= x0) & (xs <= x0 + w)).sum()
        if tot and m.sum() >= 0.6 * tot:
            res.append((x0 + w / 2, vals[m].mean()))
    return np.array(res)


def _tau(r):
    """Integral time scale (in samples) of a residual series: 1 + 2 * sum of autocorrelations until the first lag with rho < 0.1 (max 20 lags)."""
    r = np.asarray(r, float) - np.mean(r)
    v = np.dot(r, r)
    if len(r) < 6 or v <= 0:
        return 1.0
    t = 1.0
    for k in range(1, min(20, len(r) // 3)):
        rho = np.dot(r[:-k], r[k:]) / v
        if rho < 0.1:
            break
        t += 2 * rho
    return float(t)


def lee_vs_control(xs, vals, lee, controls, w, step, label='', sens=True, min_lee=3, min_ctrl=6):
    """T1/T2 core.  xs alongshore positions (m, reef centre = 0); vals the metric; lee=(a,b); controls=[(a,b),...]; w = window width.
    The control trend is a straight line through all control samples (constant if the controls are on one side only).
    Returns dict with anomaly (lee mean minus trend at the lee samples), the placebo sd and z, counts and the raw means."""
    xs = np.asarray(xs, float)
    vals = np.asarray(vals, float)
    inl = (xs >= lee[0]) & (xs <= lee[1]) & np.isfinite(vals)
    inc = np.zeros(len(xs), bool)
    for a, b in controls:
        inc |= (xs >= a) & (xs <= b)
    inc &= np.isfinite(vals)
    res = dict(label=label, n_lee=int(inl.sum()), n_ctrl=int(inc.sum()))
    if inl.sum() < min_lee or inc.sum() < min_ctrl:
        res.update(anomaly=np.nan, note='insufficient data (lee n=%d, control n=%d)' % (inl.sum(), inc.sum()))
        return res
    sides = [(xs[inc] < lee[0]).any(), (xs[inc] > lee[1]).any()]
    if all(sides):
        p = np.polyfit(xs[inc], vals[inc], 1)
        trend = lambda x: np.polyval(p, x)
        res['trend_slope_m_per_100m'] = float(p[0] * 100)
        res['trend'] = 'linear through both control strips'
    else:
        c = vals[inc].mean()
        trend = lambda x: c + 0 * x
        res['trend'] = 'constant (controls on one side only)'
    anom = float(np.mean(vals[inl] - trend(xs[inl])))
    res['lee_mean'] = float(vals[inl].mean())
    res['ctrl_mean'] = float(vals[inc].mean())
    res['anomaly'] = anom
    # placebo windows inside each control strip (windows may not cross the lee)
    pl = []
    for a, b in controls:
        m = (xs >= a) & (xs <= b)
        if m.sum() >= 3 and (b - a) >= w:
            wm = window_means(xs[m], vals[m], w, step * 2)
            for xc, v in wm:
                pl.append(v - trend(xc))
    pl = np.array(pl)
    res['n_placebo_windows'] = int(len(pl))
    res['n_indep_control_windows'] = float(sum(max(b - a, 0) for a, b in controls) / w)
    # analytic standard error: residual scatter of the control samples about the trend, corrected for serial correlation along the shore
    # (integral time scale tau = 1 + 2 sum rho_k, summed to the first lag with rho < 0.1; evaluated per control strip and pooled)
    resid, taus = [], []
    for a, b in controls:
        m = (xs >= a) & (xs <= b) & np.isfinite(vals)
        if m.sum() >= 6:
            r = vals[m] - trend(xs[m])
            r = r - r.mean() if not all(sides) else r
            taus.append(_tau(r))
            resid.append(r)
    sig = float(np.std(np.concatenate(resid), ddof=1)) if resid else np.nan
    tau = float(np.mean(taus)) if taus else 1.0
    n_eff_l = max(inl.sum() / tau, 1.0)
    n_eff_c = max(inc.sum() / tau, 1.0)
    res['ctrl_resid_sd'] = sig
    res['tau_samples'] = tau
    res['se_analytic'] = float(sig * math.sqrt(1.0 / n_eff_l + 1.0 / n_eff_c))
    res['z'] = float(anom / res['se_analytic']) if res['se_analytic'] > 0 else np.nan
    if len(pl) >= 8:
        res['placebo_sd'] = float(np.std(pl, ddof=1))
        res['placebo_rms'] = float(np.sqrt(np.mean(pl ** 2)))
        res['z_placebo'] = float(anom / max(res['placebo_sd'], 1e-9))
        res['p_empirical'] = float((np.sum(np.abs(pl) >= abs(anom)) + 1) / (len(pl) + 1))
    else:
        res['placebo_sd'] = np.nan
        res['note'] = 'fewer than 8 placebo windows: no placebo distribution; z uses the analytic standard error'
    if sens and len(controls) == 2:
        # sensitivity to the choice of control: each strip alone (constant reference).  The SPREAD of these anomalies, not the formal SE, is the
        # realistic uncertainty when the natural alongshore gradient is large (the formal SE only measures scatter about the chosen reference).
        a1 = lee_vs_control(xs, vals, lee, controls[:1], w, step, sens=False, min_lee=min_lee, min_ctrl=min_ctrl).get('anomaly', np.nan)
        a2 = lee_vs_control(xs, vals, lee, controls[1:], w, step, sens=False, min_lee=min_lee, min_ctrl=min_ctrl).get('anomaly', np.nan)
        res['anomaly_by_control'] = dict(both_linear=anom, strip1_only=a1, strip2_only=a2)
        vv = [v for v in (anom, a1, a2) if v is not None and np.isfinite(v)]
        res['anomaly_range'] = [float(min(vv)), float(max(vv))]
        res['sign_consistent'] = bool(all(v > 0 for v in vv) or all(v < 0 for v in vv))
    return res


def tin_surface(pts, gx, gy, maxdist=25.0):
    """Linear TIN of scattered soundings (x, y, z) on the grid gx (columns) x gy (rows); cells farther than maxdist from any sounding -> NaN."""
    tri = LinearNDInterpolator(pts[:, :2], pts[:, 2])
    GX, GY = np.meshgrid(gx, gy)
    Z = tri(GX, GY)
    d, _ = cKDTree(pts[:, :2]).query(np.c_[GX.ravel(), GY.ravel()])
    Z[d.reshape(Z.shape) > maxdist] = np.nan
    return Z


def bin_median(x, y, v, edges_x, edges_y, minn=3):
    """Median of v in (x, y) bins; returns array [ny, nx] and counts."""
    ix = np.digitize(x, edges_x) - 1
    iy = np.digitize(y, edges_y) - 1
    nx, ny = len(edges_x) - 1, len(edges_y) - 1
    ok = (ix >= 0) & (ix < nx) & (iy >= 0) & (iy < ny) & np.isfinite(v)
    out = np.full((ny, nx), np.nan)
    cnt = np.zeros((ny, nx), int)
    key = iy[ok] * nx + ix[ok]
    order = np.argsort(key)
    key_s, v_s = key[order], v[ok][order]
    if len(key_s) == 0:
        return out, cnt
    cuts = np.flatnonzero(np.diff(key_s)) + 1
    for k, chunk in zip(np.split(key_s, cuts), np.split(v_s, cuts)):
        kk = k[0]
        cnt[kk // nx, kk % nx] = len(chunk)
        if len(chunk) >= minn:
            out[kk // nx, kk % nx] = np.median(chunk)
    return out, cnt


def ls_over_x(L, x_toe, x_centre, note=''):
    """Black & Andrews (2001) B/S ratio (B = Ls, S = X).  Rules as recorded in 08_paper/lit/LITERATURE.md section 3.8 (read as images from Blacka et al. 2013 s2.5.2;
    the original paper was NOT read; journal volume/pages unconfirmed): no change if B/S < ~0.1, salient if B/S < 2, tombolo if B/S > 0.6 (the rules overlap);
    salient amplitude Y_off = 0.125 D_tot (D_tot = total salient width, not given there -> D_tot = 1-3 B is an ASSUMPTION used only for an ORDER OF MAGNITUDE)."""
    def regime(r):
        if r < 0.1:
            return 'no change expected'
        return 'salient expected (B/S < 2)' + ('; tombolo possible (B/S > 0.6)' if r > 0.6 else '')
    rt, rc = L / x_toe, L / x_centre
    return dict(Ls_alongshore_m=float(L), X_shoreline_to_shoreward_toe_m=float(x_toe), X_shoreline_to_reef_centre_m=float(x_centre),
                Ls_over_X_toe=float(rt), Ls_over_X_centre=float(rc), regime_toe=regime(rt), regime_centre=regime(rc),
                illustrative_salient_amplitude_m=[float(0.125 * 1 * L), float(0.125 * 3 * L)],
                note='DERIVED B/S (B = Ls alongshore extent, S = X shoreline-to-reef distance). Rules (Black & Andrews 2001 via Blacka et al. 2013): no change if B/S < ~0.1, salient if < 2, tombolo if > 0.6; '
                     'Blacka et al. note the method over-predicts salient size for submerged reefs (Narrowneck, Mount Maunganui). Illustrative amplitude = 0.125 x D_tot with D_tot = 1-3 B (ASSUMPTION; D_tot is not '
                     'given in the secondary source) -> an order of magnitude only. ' + note)


RESULTS = {}


def load_results():
    if os.path.exists(OUT_JSON):
        try:
            return json.load(open(OUT_JSON, encoding='utf-8'))
        except Exception:
            return {}
    return {}


def save_results(key, block):
    res = load_results()
    res[key] = jdump(block)
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    json.dump(res, open(OUT_JSON, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)


# ================================================================================================================= CABLES (WA)
def cables_frame():
    B = os.path.join(SHAPES, 'cables-reef-wa')
    G = json.load(open(os.path.join(B, 'scripts', 'georef.json')))['transform']
    E0, N0, TH = G['anchor_E_MGA50_GDA94'], G['anchor_N_MGA50_GDA94'], math.radians(G['theta_ccw_deg'])
    XC, YC = G['anchor_canonical_xy_m']
    poly = np.array(json.load(open(os.path.join(B, 'shape.json')))['canonical']['polygons_m'][0])
    u, v = -(poly[:, 1] - YC), (poly[:, 0] - XC)           # (E,N) = R(theta)(-(y-yc), (x-xc)) + (E0,N0)   [georef.json note]
    pE, pN = E0 + math.cos(TH) * u - math.sin(TH) * v, N0 + math.sin(TH) * u + math.cos(TH) * v
    shore = json.load(open(os.path.join(B, 'scripts', 'shore_datum.json')))
    br = math.radians(shore['shoreline_bearing_deg_T'])      # shoreline bearing 7.8 deg true (fit to the Perth_5m 0 m AHD contour, shore_and_datum.py)
    a = np.array([math.sin(br), math.cos(br)])               # alongshore unit vector (towards NNE)
    o = np.array([math.sin(br + 1.5 * math.pi), math.cos(br + 1.5 * math.pi)])   # offshore unit vector (bearing 277.8 deg)
    cE, cN = pE.mean(), pN.mean()
    def to_sn(E, N):
        d = np.c_[np.asarray(E) - cE, np.asarray(N) - cN]
        return d @ a, d @ o
    ps, pn = to_sn(pE, pN)
    return dict(B=B, to_sn=to_sn, poly_sn=np.c_[ps, pn], origin_EN=(cE, cN), a=a, o=o, shore_bearing=shore['shoreline_bearing_deg_T'])


def run_cables():
    from shapely.geometry import Polygon, Point
    fr = cables_frame()
    B, to_sn = fr['B'], fr['to_sn']
    reef = Polygon(fr['poly_sn'])
    smin, nmin, smax, nmax = reef.bounds
    L = smax - smin
    sc = 0.5 * (smin + smax)
    out = dict(reef='cables-reef-wa', frame='s alongshore (bearing %.1f deg true, + towards NNE), n offshore (+ towards WSW), origin = reef footprint centroid; '
               'shoreline bearing from 07_scale/shapes/cables-reef-wa/scripts/shore_datum.json (7.8 deg, fitted there to the DoT Perth_5m 0 m AHD contour)' % fr['shore_bearing'],
               reef_alongshore_extent_L_m=L, reef_cross_shore_extent_m=nmax - nmin,
               datum='AHD (DoT WA converts every survey to AHD; AHD ~ MSL: the 3D model takes z_MSL = z_AHD, METHODS_3D 3.1)')
    # --- data
    S = {}
    for tag, f, date in [('1995', 'FR19951221_Single', '1995-12-21'), ('1998', 'FR19980330_Reef_Single', '1998-03-30'),
                         ('1999', 'FR19991122_Single', '1999-11-22'), ('2002', 'FR20020201_Single', '2002-02-01')]:
        d = np.loadtxt(os.path.join(B, 'src', 'bathymetry', 'FR_selected', f + '.txt'), usecols=(0, 1, 2))
        s, n = to_sn(d[:, 0], d[:, 1])
        S[tag] = np.c_[s - sc, n, d[:, 2]]
    s_shift = sc          # all s are now relative to the alongshore centre of the reef (s=0)
    out['surveys'] = {k: dict(n_soundings=int(len(v)), s_range=[float(v[:, 0].min()), float(v[:, 0].max())], n_range=[float(v[:, 1].min()), float(v[:, 1].max())],
                              z_range_AHD=[float(v[:, 2].min()), float(v[:, 2].max())]) for k, v in S.items()}
    out['surveys_source'] = ('DoT WA (Department of Transport) singlebeam point files, CC BY 4.0: 07_scale/shapes/cables-reef-wa/src/bathymetry/FR_selected/'
                             'FR19951221_Single.txt (pre-construction), FR19980330_Reef_Single.txt (pre-construction, 30 Mar 1998), FR19991122_Single.txt '
                             '(rock surface 22 Nov 1999, the month before completion), FR20020201_Single.txt (1 Feb 2002). '
                             'Reference list: 07_scale/shapes/cables-reef-wa/3d/SOURCES_3D.md; file ReadMe: DoT_FR_PointData ("accuracy variable, no warranty").')
    # Perth_5m composite resampled to (s,n)
    z = np.load(os.path.join(B, 'src', 'bathymetry', 'DoT_Perth_5m_clip_reef.npz'))
    rz = z['z_AHD'].astype(float)
    rz[rz < -9000] = np.nan
    xl, yt, px = float(z['x_left']), float(z['y_top']), float(z['pixel'])
    H, W = rz.shape
    Ec, Nc = xl + (np.arange(W) + 0.5) * px, yt - (np.arange(H) + 0.5) * px
    f = RegularGridInterpolator((Nc[::-1], Ec), rz[::-1], bounds_error=False)
    gs = np.arange(-560.0, 561.0, 5.0)
    gn = np.arange(-380.0, 300.0, 5.0)
    GS, GN = np.meshgrid(gs, gn)
    cE, cN = fr['origin_EN']
    # s was shifted by sc: invert  P = origin + (s+sc) a + n o
    Eg = cE + (GS + sc) * fr['a'][0] + GN * fr['o'][0]
    Ng = cN + (GS + sc) * fr['a'][1] + GN * fr['o'][1]
    Zc = f(np.c_[Ng.ravel(), Eg.ravel()]).reshape(GS.shape)
    # --- T1: contour offsets
    ctrl = [(-3.5 * L, -1.5 * L), (1.5 * L, 3.5 * L)]
    lee_core = (-L / 2, L / 2)
    lee_ext = (-L, L)
    grids = {'Perth_5m composite (date mixed, contains the reef as a smoothed mound)': (Zc, 'composite')}
    for tag in ('1995', '1998', '2002'):
        grids['DoT singlebeam %s' % tag] = (tin_surface(S[tag], gs, gn, 25.0), tag)
    Zs = {k: v[0] for k, v in grids.items()}
    t1 = []
    contour_store = {}
    levels_by = {'composite': [0, -1, -2, -3, -4], '1995': [-3, -4, -5, -6], '1998': [-4, -5, -6], '2002': [-2, -3, -4, -5, -6]}
    for name, (Z, tag) in grids.items():
        Zsm = nan_gauss(Z, 2.0)            # sigma 10 m, suppresses the sounding-line stripes
        for lev in levels_by[tag]:
            ypos = contour_cols(Zsm, gn, lev)
            contour_store[(tag, lev)] = ypos
            if tag not in ('composite', '2002'):
                continue          # 1995/1998 cover only s = -212..+339 / -120..+110 m: far controls do not exist; they are used in T1b/T3 with adjacent controls
            for lee, nm in ((lee_core, 'lee_L'), (lee_ext, 'lee_2L')):
                r = lee_vs_control(gs, ypos, lee, ctrl, L, 5.0, label='%s | %s m | %s' % (name, lev, nm))
                r.update(dataset=name, level_m_AHD=lev, lee=nm)
                # coverage of the contour (fraction of transects with a crossing) in the lee and controls
                t1.append(r)
    out['T1_contour_offset'] = dict(
        definition='anomaly = mean cross-shore position of the contour in the lee window minus the control-strip trend (m). POSITIVE = contour farther '
                   'OFFSHORE (nearer the reef) in the lee = bulge/salient. Windows in m alongshore from the reef centre: lee_L = +-%.0f, lee_2L = +-%.0f, '
                   'controls = %.0f..%.0f and %.0f..%.0f (1.5-3.5 L). Surfaces: soundings -> linear TIN (<= 25 m from a sounding) on a 5 m grid, Gaussian '
                   'sigma 10 m; first downward crossing from the shore side.' % (L / 2, L, ctrl[0][0], ctrl[0][1], ctrl[1][0], ctrl[1][1]),
        rows=t1)
    lee_cols = (gs >= -L / 2) & (gs <= L / 2)
    n_shore = float(np.nanmean(contour_store[('composite', 0)][lee_cols]))
    out['Ls_over_X'] = ls_over_x(L, nmin - n_shore, -n_shore, 'shoreline = 0 m AHD contour of the Perth_5m composite (undated), mean over the lee window')
    # --- T2/T3 : bed level and change in the lee band (fixed n-range, fixed for all surveys; the 0 m AHD contour lies at n = -250..-270)
    band = (-165.0, -62.0)        # lee band: from the shoreward edge of the 1995 survey to 20 m inside the reef's shoreward toe (n_min of the footprint = %.0f)
    out['lee_band_n_m'] = band
    bi = (gn >= band[0]) & (gn <= band[1])
    colmean = {}
    for k in ('1995', '2002', '1998'):
        Zk = nan_gauss(tin_surface(S[k], gs, gn, 25.0), 1.0)
        colmean[k] = np.nanmean(np.where(bi[:, None], Zk, np.nan), axis=0)
    colmean['composite'] = np.nanmean(np.where(bi[:, None], Zc, np.nan), axis=0)
    t2 = []
    for k, nm in (('1995', 'DoT 1995-12 (pre-construction)'), ('2002', 'DoT 2002-02 (2.2 y after completion)'), ('composite', 'Perth_5m composite')):
        r = lee_vs_control(gs, colmean[k], lee_core, ctrl, L, 5.0, label=nm)
        r['lee_band_n_m'] = list(band)
        t2.append(r)
    out['T2_bed_level_lee_band'] = dict(definition='mean bed elevation (m AHD) over n = %.0f..%.0f m per alongshore column; anomaly = lee minus control trend; '
                                                   'positive = bed HIGHER (sand accumulation or a natural high) in the lee' % band, rows=t2)
    # temporal: dz = later - earlier survey on the common grid (cells with both surveys <= 25 m from a sounding)
    Z95 = tin_surface(S['1995'], gs, gn, 25.0)
    Z98 = tin_surface(S['1998'], gs, gn, 25.0)
    Z02 = tin_surface(S['2002'], gs, gn, 25.0)
    DZ = {'2002-1995': Z02 - Z95, '2002-1998': Z02 - Z98, '1998-1995': Z98 - Z95}
    # The 1995 survey covers the lee band only for s = -150..+125 m (coverage map, 2026-10 run), so the temporal controls are the ADJACENT strips
    # (1.4-2.7 half-lengths from the reef centre).  They may be partly inside the reef's sphere of influence -> a bias TOWARDS zero signal.
    ctrl_t = [(-150.0, -75.0), (75.0, 125.0)]
    boxes = {'lee': lee_core, 'ctrl_S': ctrl_t[0], 'ctrl_N': ctrl_t[1]}
    dzrows = []
    for pair, DZp in DZ.items():
        for bn, (sa, sb) in boxes.items():
            sm = (gs >= sa) & (gs <= sb)
            sub = DZp[np.ix_(bi, sm)]
            ok = np.isfinite(sub)
            dzrows.append(dict(pair=pair, box=bn, s_range=[sa, sb], n_range=list(band), n_cells_valid=int(ok.sum()), n_cells_total=int(sub.size),
                               coverage=float(ok.mean()), mean_dz_m=float(np.nanmean(sub)) if ok.any() else np.nan,
                               sd_cell_dz_m=float(np.nanstd(sub)) if ok.any() else np.nan,
                               volume_change_m3=float(np.nansum(sub) * 25.0) if ok.any() else np.nan))
    out['T3_temporal_boxes'] = dict(definition='dz = later minus earlier survey, per 5 m cell where both surveys have a sounding within 25 m (TIN); '
                                               'boxes in s (m from the reef centre) x n = %.0f..%.0f m; volume = sum(dz) x 25 m2 over VALID cells only '
                                               '(coverage given); pairs 2002-1998 and 1998-1995 do not reach the lee band (1998 covers n > -75 m only)' % (band[0], band[1]), rows=dzrows)
    cm = {p: np.nanmean(np.where(bi[:, None], DZp, np.nan), axis=0) for p, DZp in DZ.items()}
    did = []
    for p, bnd in (('2002-1995', band), ('2002-1995', (-110.0, -62.0))):
        bb = (gn >= bnd[0]) & (gn <= bnd[1])
        col = np.nanmean(np.where(bb[:, None], DZ[p], np.nan), axis=0)
        r = lee_vs_control(gs, col, lee_core, ctrl_t, 55.0, 5.0, label='dz %s, n=%.0f..%.0f' % (p, bnd[0], bnd[1]))
        r['note_controls'] = 'adjacent strips s=-150..-75 and +75..+125 (survey coverage limit); placebo windows 55 m wide (narrower than the lee window: conservative)'
        did.append(r)
    out['T3_dz_difference_in_differences'] = did
    # contour MIGRATION 2002 minus 1995 on the common transects (positive = contour moved offshore = bed raised), lee vs adjacent strips
    mig = []
    for lev in (-4, -5, -6):
        y95, y02 = contour_store.get(('1995', lev)), contour_store.get(('2002', lev))
        if y95 is None or y02 is None:
            continue
        d = y02 - y95
        r = lee_vs_control(gs, d, lee_core, ctrl_t, 55.0, 5.0, label='contour migration 2002-1995, %d m AHD' % lev)
        r['level_m_AHD'] = lev
        r['n_common_transects'] = int(np.isfinite(d).sum())
        mig.append(r)
    out['T3_contour_migration_2002_minus_1995'] = mig
    # the pre-existing contour offset: lee anomaly in the 1995 (PRE-construction) survey itself, adjacent controls, for levels the 1995 survey reaches
    pre = []
    for tag in ('1995', '2002'):
        for lev in (-4, -5, -6):
            y = contour_store.get((tag, lev))
            if y is None:
                continue
            r = lee_vs_control(gs, y, lee_core, ctrl_t, 55.0, 5.0, label='%s survey, %d m AHD contour, lee vs ADJACENT strips' % (tag, lev))
            r['level_m_AHD'] = lev
            r['survey'] = tag
            pre.append(r)
    out['T1b_contour_offset_adjacent_controls_1995_vs_2002'] = dict(
        definition='same as T1 but with the adjacent control strips so that the PRE-construction survey (1995, coverage s = -212..+339 but only -150..+125 in the lee band) can be '
                   'compared with the post-construction survey (2002) on identical transects',
        rows=pre)
    # noise floor from the pre-construction pair (all valid cells in the whole pair-coverage, outside the reef footprint + 20 m)
    reef20 = reef.buffer(20)
    GS2, GN2 = np.meshgrid(gs, gn)
    inreef = np.array([reef20.contains(Point(a, b)) for a, b in zip(GS2.ravel(), GN2.ravel())]).reshape(GS2.shape)
    nf = {}
    for p, DZp in DZ.items():
        v = DZp[np.isfinite(DZp) & ~inreef]
        nf[p] = dict(n_cells=int(len(v)), mean_m=float(v.mean()), sd_m=float(v.std()), p5=float(np.percentile(v, 5)), p95=float(np.percentile(v, 95)))
    out['dz_cell_statistics_outside_reef_buffer'] = nf
    # sounding-level pre-construction repeatability (1998 vs 1995 TIN), as quoted in METHODS_3D 3.4 (mean 0.09, sd 0.29 m, n = 8,063)
    T95 = LinearNDInterpolator(S['1995'][:, :2], S['1995'][:, 2])
    d95 = cKDTree(S['1995'][:, :2]).query(S['1998'][:, :2])[0]
    dz98 = S['1998'][:, 2] - T95(S['1998'][:, :2])
    m = (d95 < 3.0) & np.isfinite(dz98)
    out['repeatability_1998_vs_1995_soundings_within_3m'] = dict(n=int(m.sum()), mean_m=float(dz98[m].mean()), sd_m=float(dz98[m].std()),
        note='nearest-sounding pairs; METHODS_3D 3.4 quotes mean 0.09 m, sd 0.29 m (n=8,063) for the 1995/1998 agreement; includes 2.3 y of natural change')
    # --- T4: rings around the footprint (post minus 1998 bed) and the reef itself
    T98 = LinearNDInterpolator(S['1998'][:, :2], S['1998'][:, 2])
    k98 = cKDTree(S['1998'][:, :2])
    rings = []
    for tag in ('1999', '2002'):
        P = S[tag]
        dist = np.array([reef.exterior.distance(Point(a, b)) if not reef.contains(Point(a, b)) else -reef.exterior.distance(Point(a, b)) for a, b in P[:, :2]])
        near98 = k98.query(P[:, :2])[0]
        dz = P[:, 2] - T98(P[:, :2])
        ok = np.isfinite(dz) & (near98 < 15)
        sector = np.where(P[:, 1] < nmin, 'shoreward', np.where(P[:, 1] > nmax, 'seaward', 'flank'))
        for lo, hi, nm in ((-1e9, 0, 'inside footprint (rock thickness above the 1998 bed)'), (0, 10, 'ring 0-10 m outside'), (10, 25, 'ring 10-25 m outside'),
                           (25, 50, 'ring 25-50 m outside'), (50, 100, 'ring 50-100 m outside')):
            for sec in ('all', 'shoreward', 'seaward', 'flank'):
                mm = ok & (dist > lo) & (dist <= hi) & ((sector == sec) | (sec == 'all'))
                if mm.sum() >= 5:
                    rings.append(dict(survey=tag, zone=nm, sector=sec, n=int(mm.sum()), mean_dz_m=float(dz[mm].mean()), sd_m=float(dz[mm].std()),
                                      se_m=float(dz[mm].std() / math.sqrt(mm.sum()))))
    out['T4_rings_post_minus_1998_bed'] = dict(definition='dz at each post-construction sounding minus the 1998 TIN (soundings <= 15 m from a 1998 sounding). Positive outside '
                                                          'the footprint = sand and/or rock fall-down above the 1998 bed (not separable with echo-sounder data). SE ignores spatial correlation.',
                                               rows=rings)
    # reef surface 1999-11 vs 2002-02: matched soundings within 3 m
    inside = lambda P: np.array([reef.contains(Point(a, b)) for a, b in P[:, :2]])
    P99, P02 = S['1999'], S['2002']
    i99, i02 = inside(P99), inside(P02)
    kk = cKDTree(P02[i02][:, :2])
    d, ix = kk.query(P99[i99][:, :2])
    mm = d < 3.0
    dzm = P02[i02][ix[mm], 2] - P99[i99][mm, 2]
    out['T4_reef_surface_2002_minus_1999_matched_within_3m'] = dict(
        n=int(mm.sum()), mean_m=float(dzm.mean()) if mm.any() else np.nan, sd_m=float(dzm.std()) if mm.any() else np.nan,
        se_m=float(dzm.std() / math.sqrt(mm.sum())) if mm.sum() > 1 else np.nan,
        z95_inside_footprint_1999=float(np.percentile(P99[i99][:, 2], 95)), z95_inside_footprint_2002=float(np.percentile(P02[i02][:, 2], 95)),
        n_inside_1999=int(i99.sum()), n_inside_2002=int(i02.sum()),
        note='negative = 2002 surface lower than 1999 (settlement, or burial is NOT visible as a rise); positive = higher (sand cover, or sounding-line offsets)')
    # --- T5: beach-level point surveys (DoT 'Levels' files in the zip: terrestrial point elevations along profile lines about 50 m apart)
    import io
    import zipfile
    zf = zipfile.ZipFile(os.path.join(B, 'src', 'bathymetry', 'DoT_FR_PointData_FR.zip'))
    bdates = {'2001-01': 'FR20010101_Levels', '2002-02': 'FR20020201_Levels', '2003-01': 'FR20030101_Levels',
              '2011-08': 'FR20110801_PortBeach_Levels', '2012-04': 'FR20120426_PortBeach_Levels'}
    beach = {}
    for dk, fn in bdates.items():
        d = np.loadtxt(io.StringIO(zf.read(fn + '.txt').decode('ascii', 'ignore')), usecols=(0, 1, 2))
        bs, bn = to_sn(d[:, 0], d[:, 1])
        bs = bs - sc
        m = (np.abs(bs) < 900) & (bn > -420) & (bn < -150)
        bs, bn, bz = bs[m], bn[m], d[m, 2]
        o = np.argsort(bs)
        groups, cur = [], [o[0]]
        for i in o[1:]:
            if bs[i] - bs[cur[-1]] > 8:
                groups.append(cur)
                cur = [i]
            else:
                cur.append(i)
        groups.append(cur)
        rows_ = []
        for gi in groups:
            if len(gi) < 5:
                continue
            gi = np.array(gi)
            k = np.argsort(bn[gi])
            nn_, zz_ = bn[gi][k], bz[gi][k]

            def cx(lev):
                for i in range(len(nn_) - 1):
                    if zz_[i] >= lev and zz_[i + 1] < lev and (nn_[i + 1] - nn_[i]) < 40:
                        return nn_[i] + (zz_[i] - lev) / (zz_[i] - zz_[i + 1]) * (nn_[i + 1] - nn_[i])
                return np.nan
            rows_.append((float(np.mean(bs[gi])), cx(0.0), cx(1.0), cx(2.0)))
        beach[dk] = np.array(rows_)
    ctrl_b = [(-385.0, -165.0), (165.0, 385.0)]
    t5 = []
    for dk, A_ in beach.items():
        for j, lev in ((1, 0.0), (2, 1.0), (3, 2.0)):
            r = lee_vs_control(A_[:, 0], A_[:, j], lee_core, ctrl_b, 55.0, 50.0, label='beach levels %s, %+.0f m AHD contour' % (dk, lev), min_lee=2, min_ctrl=4)
            r.update(date=dk, level_m_AHD=lev, n_lines=int(np.isfinite(A_[:, j]).sum()))
            t5.append(r)
    out['T5_beach_levels_spatial'] = dict(
        definition=('DoT WA terrestrial point-elevation files (zip DoT_FR_PointData_FR.zip, FR*_Levels.txt: Jan 2001 = 13 months after completion, Feb 2002, Jan 2003, Aug 2011 and Apr 2012 (Port Beach files); '
                    'capture dates are the file-name end dates, accuracy variable). Points grouped into profile lines (gap > 8 m in s, >= 5 points; about 50 m apart); position of the 0/+1/+2 m AHD contour on each line '
                    '(first downward crossing from the dune); lee = lines within +-55 m, controls = lines 165-385 m either side. Positive = contour farther offshore in the lee.'), rows=t5,
        lines_per_date={k: int(len(v)) for k, v in beach.items()})
    t5t = []
    for da, db in (('2001-01', '2003-01'), ('2003-01', '2012-04'), ('2001-01', '2012-04'), ('2002-02', '2012-04')):
        Aa, Ab = beach[da], beach[db]
        for j, lev in ((1, 0.0), (2, 1.0)):
            sa, ya = Aa[:, 0], Aa[:, j]
            ss_, dy = [], []
            for sb_, yb_ in zip(Ab[:, 0], Ab[:, j]):
                k = int(np.argmin(np.abs(sa - sb_)))
                if abs(sa[k] - sb_) < 20 and np.isfinite(ya[k]) and np.isfinite(yb_):
                    ss_.append(sb_)
                    dy.append(yb_ - ya[k])
            r = lee_vs_control(np.array(ss_), np.array(dy), lee_core, ctrl_b, 55.0, 50.0, label='beach levels, change %s -> %s, %+.0f m AHD contour' % (da, db, lev), min_lee=2, min_ctrl=4)
            r.update(from_date=da, to_date=db, level_m_AHD=lev, n_matched_lines=len(ss_))
            t5t.append(r)
    out['T5b_beach_levels_change'] = dict(definition='change in contour position between survey dates on matched lines (nearest line within 20 m), lee minus control trend; positive = the lee shoreline advanced relative to the controls; '
                                                     'there is NO pre-construction beach survey (the first is 13 months after completion), so this tests growth after Jan 2001 only', rows=t5t)
    # --- keep arrays for the figure
    STORE['cables_beach'] = beach
    STORE['cables'] = dict(gs=gs, gn=gn, Zc=Zc, Z95=Z95, Z02=Z02, Z98=Z98, DZ=DZ, S=S, poly=fr['poly_sn'] - np.array([sc, 0]), L=L, ctrl=ctrl, lee=lee_core,
                           contours=contour_store, band=band, colmean=colmean, cm=cm)
    return out


STORE = {}


# ================================================================================================================= BOSCOMBE (UK)
def run_boscombe():
    import datetime as dt
    import glob
    sys.dont_write_bytecode = True
    sys.path.insert(0, os.path.join(SHAPES, 'boscombe-surf-reef', '3d', 'scripts'))
    from canon import osgb2can                      # read-only import of the project's own OSGB36 -> canonical-frame helper
    src = os.path.join(SHAPES, 'boscombe-surf-reef', 'src', 'cco_profiles')
    m = load_model('boscombe-surf-reef')
    poly = np.array(m['reef']['toe_polygon_xyzz'])[:, :2]
    xa, xb = poly[:, 0].min(), poly[:, 0].max()
    L, xc = xb - xa, 0.5 * (xa + xb)
    D = dt.date.fromisoformat
    T_START, T_OPEN = D('2008-06-01'), D('2009-11-19')          # construction start (lower layer 2008-06, model history) and official opening (2009-11-19)
    data = {}
    for f in sorted(glob.glob(os.path.join(src, '5f*.txt'))):
        pid, date = os.path.basename(f)[:-4].split('_')
        a = np.genfromtxt(f, skip_header=1, usecols=(0, 1, 2, 3))
        a = a[None] if a.ndim == 1 else a
        c = osgb2can(a[:, 0], a[:, 1])
        data.setdefault(pid, {})[date] = np.c_[c[:, 0], c[:, 1], a[:, 2]]
    levels = {'y_+2.0': 2.0, 'y_+1.0': 1.0, 'y_0.0': 0.0}

    def crossing(y, z, lev):
        o = np.argsort(y)
        y, z = y[o], z[o]
        for i in range(len(y) - 1):
            if z[i] >= lev and z[i + 1] < lev and (y[i + 1] - y[i]) < 25:
                return y[i] + (z[i] - lev) / (z[i] - z[i + 1]) * (y[i + 1] - y[i])
        return np.nan
    met = {}
    xline = {}
    for pid, dd in data.items():
        xs_ = []
        for date, v in dd.items():
            y, z = v[:, 1], v[:, 2]
            r = {k: crossing(y, z, lv) for k, lv in levels.items()}
            vol = np.nan
            o = np.argsort(y)
            yy, zz = y[o], z[o]
            if yy.min() <= -55 and np.isfinite(r['y_0.0']):
                g = np.arange(-55, r['y_0.0'], 0.5)
                vol = float(np.trapezoid(np.maximum(np.interp(g, yy, zz), 0.0), g))
            r['vol0_m3_per_m'] = vol
            met[(pid, date)] = r
            sel = (y > -20) & (y < 20)
            if sel.any():
                xs_.append(np.median(v[sel, 0]))
        xline[pid] = float(np.mean(xs_))
    main = ['5f00424', '5f00425', '5f00426', '5f00427', '5f00428', '5f00429']
    allp = sorted(data)
    xrel = {p: xline[p] - xc for p in allp}
    lee_lines = [p for p in main if abs(xrel[p]) <= 0.75 * L]
    ctrl_lines = [p for p in main if abs(xrel[p]) >= 1.5 * L]
    out = dict(reef='boscombe-surf-reef', reef_alongshore_extent_L_m=L, reef_centre_x_m=xc, reef_x_range=[float(xa), float(xb)],
               datum='metres ODN (Ordnance Datum Newlyn) of the CCO profiles; the 3D model takes ODN = MSL within +-0.1 m (A4, METHODS_3D 3.2), so 0 m ODN ~ MSL contour',
               data_source=('Channel Coastal Observatory (CCO) beach-profile surveys, lines 5f00424-5f00429 (+ "A" lines 424A-428A from 2010), 316 files '
                            '07_scale/shapes/boscombe-surf-reef/src/cco_profiles/<line>_<date>.txt, fetched by 3d/scripts/cco_fetch.py (see 3d/SOURCES_3D.md S13); points (E,N,z_ODN,chainage) '
                            'converted to the canonical reef frame with 3d/scripts/canon.py (OSGB36 -> canonical, +-5 m). Profiles run from the sea wall (y about -64 m) to z about -1 m ODN '
                            '(y about +21 m); the reef lies at y = %.0f-%.0f m, i.e. >= 160 m seaward of the end of every profile.' % (poly[:, 1].min(), poly[:, 1].max())),
               periods=dict(pre='before 2008-06-01 (lines 424/427: 2004-07 .. 2008-04; others 5 dates 2004-07 .. 2008-04)', construction='2008-06-01 .. 2009-11-18 (excluded)',
                            post='from 2009-11-19 (official opening) to 2026-03-06'),
               line_x_m={p: xline[p] for p in allp}, lee_lines=lee_lines, control_lines=ctrl_lines)

    def D_(s):
        return D(s)
    # ---- A. raw per-line pre/post table
    tab = []
    for p in allp:
        ds = sorted(data[p])
        pre = [d for d in ds if D_(d) < T_START]
        post = [d for d in ds if D_(d) >= T_OPEN]
        row = dict(line=p, x_m=xline[p], x_rel_reef_centre_m=xrel[p], n_dates_pre=len(pre), n_dates_post=len(post))
        for k in ('y_0.0', 'y_+1.0', 'vol0_m3_per_m'):
            a = np.array([met[(p, d)][k] for d in pre], float)
            a = a[np.isfinite(a)]
            b = np.array([met[(p, d)][k] for d in post], float)
            b = b[np.isfinite(b)]
            row[k] = dict(pre_mean=a.mean() if len(a) else np.nan, pre_sd=a.std(ddof=1) if len(a) > 1 else np.nan, n_pre=len(a),
                          post_mean=b.mean() if len(b) else np.nan, post_sd=b.std(ddof=1) if len(b) > 1 else np.nan, n_post=len(b),
                          post_minus_pre=(b.mean() - a.mean()) if len(a) and len(b) else np.nan)
        tab.append(row)
    out['A_raw_pre_post_by_line'] = tab
    y0_post = float(np.nanmean([met[(p_, d)]['y_0.0'] for p_ in lee_lines for d in data[p_] if D_(d) >= T_OPEN]))
    out['Ls_over_X'] = ls_over_x(L, poly[:, 1].min() - y0_post, poly[:, 1].mean() - y0_post,
                                 'shoreline = mean post-construction 0 m ODN contour of the lee lines (y = %.1f m)' % y0_post)
    # ---- B. yearly means (to show the common-mode / beach-management signal)
    yearly = {}
    for p in main:
        yearly[p] = {}
        for y in range(2004, 2027):
            v = [met[(p, d)] for d in data[p] if d.startswith(str(y))]
            if v:
                yearly[p][y] = dict(y_0=float(np.nanmean([r['y_0.0'] for r in v])), vol0=float(np.nanmean([r['vol0_m3_per_m'] for r in v])), n=len(v))
    out['B_yearly_means_main_lines'] = yearly
    vol_by_year = {y: [yearly[p][y]['vol0'] for p in main if y in yearly[p]] for y in range(2004, 2027)}
    jumps = []
    ys_ = sorted(y for y in vol_by_year if len(vol_by_year[y]) == 6)
    for a, b in zip(ys_[:-1], ys_[1:]):
        dvol = np.array(vol_by_year[b]) - np.array(vol_by_year[a])
        if (b - a) == 1 and np.nanmedian(dvol) > 20:
            jumps.append(dict(from_year=a, to_year=b, median_change_m3_per_m=float(np.nanmedian(dvol)), lines_rising=int((dvol > 20).sum())))
    out['B_common_mode_volume_jumps'] = dict(
        rows=jumps, definition='year-to-year rise of the beach volume above 0 m ODN (between y=-55 m and the 0 m contour) with a median over the 6 main lines > 20 m3 per m. '
                               'DERIVED indicator only: the dates and volumes of Poole Bay recharge / recycling are NOT in the repo (ASSUMPTION that such jumps are beach management, '
                               'not natural; the CCO and BCP Council beach-management records must be checked).')
    # ---- C. common-mode removed (the six main lines, dates on which all six were surveyed)
    alld = sorted(set.intersection(*[set(data[p]) for p in main]))
    pre_d = [d for d in alld if D_(d) < T_START]
    post_d = [d for d in alld if D_(d) >= T_OPEN]
    xr = np.array([xrel[p] for p in main])
    is_ctrl = np.array([p in ctrl_lines for p in main])
    is_lee = np.array([p in lee_lines for p in main])
    rng = np.random.default_rng(20261015)
    C = {}
    for k in ('y_0.0', 'y_+1.0', 'y_+2.0', 'vol0_m3_per_m'):
        def rel(dates):
            M = np.array([[met[(p, d)][k] for p in main] for d in dates])
            M = M[np.isfinite(M).all(1)]
            return M - M.mean(1, keepdims=True)
        Rpre, Rpost = rel(pre_d), rel(post_d)

        def stat(Rpre_, Rpost_):
            dlt = Rpost_.mean(0) - Rpre_.mean(0)                    # change in relative position per line
            pf = np.polyfit(xr[is_ctrl], dlt[is_ctrl], 1)
            anom = float(np.mean(dlt[is_lee] - np.polyval(pf, xr[is_lee])))
            return dlt, anom, pf
        dlt, anom, pf = stat(Rpre, Rpost)
        boots = []
        for _ in range(4000):
            a = Rpre[rng.integers(0, len(Rpre), len(Rpre))]
            b = Rpost[rng.integers(0, len(Rpost), len(Rpost))]
            boots.append(stat(a, b)[1])
        boots = np.array(boots)
        se_line = np.sqrt(Rpre.var(0, ddof=1) / len(Rpre) + Rpost.var(0, ddof=1) / len(Rpost))
        C[k] = dict(n_dates_pre=len(Rpre), n_dates_post=len(Rpost), lines=main, x_rel_m=xr,
                    rel_pre=Rpre.mean(0), rel_post=Rpost.mean(0), change_rel=dlt, se_change=se_line,
                    control_trend_slope_per_100m=float(pf[0] * 100), lee_anomaly=anom,
                    lee_anomaly_ci95=[float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))], bootstrap_sd=float(boots.std()))
    out['C_common_mode_removed_BACI'] = dict(
        definition=('For each date on which all six main lines were surveyed, the line value minus the mean of the six lines (removes common-mode beach-management and seasonal signal). '
                    'change_rel = post mean minus pre mean per line. lee_anomaly = mean change_rel of the lee lines (%s) minus the straight-line trend fitted to the control lines (%s) '
                    'at the lee-line positions; POSITIVE = lee shoreline advanced (or volume rose) relative to the controls after the reef. 95 %% CI by bootstrap over survey dates '
                    '(4000 resamples; pre n=%d dates, post n=%d dates).' % (', '.join(lee_lines), ', '.join(ctrl_lines), len(pre_d), len(post_d))),
        metrics=C)
    # ---- D. post-construction only, all 11 lines, annual dates common to all lines
    d11 = sorted(set.intersection(*[set(data[p]) for p in allp]))
    d11 = [d for d in d11 if D_(d) >= T_OPEN]
    x11 = np.array([xrel[p] for p in allp])
    c11 = np.array([abs(v) >= 1.5 * L for v in x11])
    l11 = np.array([abs(v) <= 0.75 * L for v in x11])
    Dres = {}
    for k in ('y_0.0', 'y_+1.0', 'vol0_m3_per_m'):
        M = np.array([[met[(p, d)][k] for p in allp] for d in d11])
        M = M[np.isfinite(M).all(1)]
        R = M - M.mean(1, keepdims=True)
        an = []
        for r in R:
            pf = np.polyfit(x11[c11], r[c11], 1)
            an.append(np.mean(r[l11] - np.polyval(pf, x11[l11])))
        an = np.array(an)
        Dres[k] = dict(n_dates=len(R), lines=allp, x_rel_m=x11, mean_rel=R.mean(0), sd_rel=R.std(0, ddof=1),
                       lee_anomaly_mean=float(an.mean()), lee_anomaly_se=float(an.std(ddof=1) / math.sqrt(len(an))), lee_lines=[p for p, f in zip(allp, l11) if f],
                       control_lines=[p for p, f in zip(allp, c11) if f])
    out['D_post_only_alongshore_pattern_11_lines'] = dict(
        definition='Post-construction annual surveys on which all 11 lines (6 main + 5 "A") exist; position minus the 11-line mean; anomaly of the lee lines against the '
                   'straight line through the control lines (|x - xc| >= 1.5 L) per date; mean and standard error over dates (dates not independent: nourishment and storms act on all).',
        metrics=Dres)
    # ---- E. largest 4-8 month change of the 0 m ODN contour between consecutive surveys, 2008-06 .. 2010-12 (test of the "60 m in 6 months" statement)
    e_rows = []
    for p in main:
        ds = sorted(d for d in data[p] if T_START <= D_(d) <= D('2010-12-31'))
        for a, b in zip(ds[:-1], ds[1:]):
            gap = (D_(b) - D_(a)).days
            if 120 <= gap <= 240:
                ya, yb = met[(p, a)]['y_0.0'], met[(p, b)]['y_0.0']
                if np.isfinite(ya) and np.isfinite(yb):
                    e_rows.append(dict(line=p, from_date=a, to_date=b, days=gap, d_y0_m=float(yb - ya)))
    out['E_six_month_changes_2008_2010'] = dict(
        rows=e_rows, max_advance_m=float(max([r['d_y0_m'] for r in e_rows])) if e_rows else np.nan,
        note=('Mead & Borrero (2011) p.4-5 (as recorded in 02_research/reefs/boscombe-surf-reef.md) report beach accretion of up to 60 m over >500 m within 6 months; '
              'the 0 m ODN contour at the CCO lines moved by the amounts listed (the claim may use another contour, line or reference; NOT reproduced here).'))
    STORE['boscombe'] = dict(yearly=yearly, C=C, D=Dres, xr=xr, main=main, jumps=jumps, L=L, xc=xc, T_START=T_START, T_OPEN=T_OPEN)
    return out


# ================================================================================================================= BORTH (Wales)
def run_borth():
    from shapely.geometry import Polygon
    sys.dont_write_bytecode = True
    sys.path.insert(0, os.path.join(SHAPES, 'borth-coastal-defence-reef', '3d'))
    import b3d_lib as BL                            # read-only import: Frame (BNG -> canonical) and the LiDAR sampler of the project's own 3D build
    base = os.path.join(SHAPES, 'borth-coastal-defence-reef')
    shape = json.load(open(os.path.join(base, 'shape.json'), encoding='utf-8'))
    F = BL.Frame(shape)
    polys = [np.array(p) for p in shape['canonical']['polygons_m']]
    allp = np.vstack(polys)
    xa, xb = allp[:, 0].min(), allp[:, 0].max()
    L = xb - xa
    xc = 0.5 * (xa + xb)
    f = BL.lidar_sampler(F, os.path.join(BL.SRC, 'lidar_beach_SN6089_2022-03-19.npz'), 'dtm')
    xs = np.arange(-330.0, 420.1, 2.0)
    ys = np.arange(-40.0, 320.1, 2.0)
    X, Y = np.meshgrid(xs, ys)
    Zodn = f(X, Y)
    MSL_ODN = 0.31                                   # model.js datum: MSL = +0.31 mODN (+-0.15)
    Zm = Zodn - MSL_ODN                              # m MSL
    out = dict(reef='borth-coastal-defence-reef', reef_alongshore_extent_L_m=float(L), reef_alongshore_x_range_m=[float(xa), float(xb)], reef_centre_x_m=float(xc),
               frame='x alongshore (+ towards SOUTH, bearing 179.57), y offshore (+ towards WEST), origin on the defence line; project Frame class (BNG -> canonical, fit rms %.3f m)' % F.fit_rms,
               data_source=('Welsh Government LiDAR DTM, tile SN6089, flight 2022-03-19, 1 m cells, 07_scale/shapes/borth-coastal-defence-reef/3d/src/lidar_beach_SN6089_2022-03-19.npz '
                            '(licence/vertical datum: ODN assumed, not stated in the tile; METHODS_3D 3.3). Rock mounds are in the tile; the beach and foreshore down to the water edge '
                            '(about -2.3 mODN) are bare-earth. ONE DATE ONLY (10 y after Phase 1 was completed on 8 Mar 2012): no pre-construction beach survey exists in the repo.'),
               datum='metres MSL = mODN - 0.31 (MSL +0.31 mODN +-0.15 from a 4-level mean; Borth is macrotidal, MHWS +2.56, MLWS -1.74 mODN)',
               not_used='3D model seabed grid (thin-plate-spline of the LiDAR nodes, HRPP576 Fig 2 contours and ASSUMED bridge nodes): only the LiDAR DTM itself is analysed.')
    levels = [0.0, -1.0, -2.0]
    # restrict contour search to the beach/foreshore (y < 255 m): the reef mounds start at y = 257 m
    ymask = ys <= 255.0
    # lee window = reef alongshore extent (2 mounds), controls = beyond 0.5 L from either edge (the tile is only ~730 m long)
    lee = (xa, xb)
    ctrl = [(xs.min(), xa - 0.5 * L), (xb + 0.5 * L, xs.max())]
    out['windows_x_m'] = dict(lee=lee, controls=ctrl,
                              note='LiDAR tile spans x = %.0f..%.0f m only, so the 1.5-3.5 L controls used elsewhere do not fit; controls start 0.5 L beyond the reef edges (inside a possible sphere of influence: biases toward zero). '
                                   'The north (west) control strip contains an unexplained shore-parallel ridge in the DTM (x about -330..-235 m, y about 75-95 m: closed 0 / -1 m contour loops) that kinks the -1 m contour; '
                                   'not identified (possible rock revetment/outfall; not checked).' % (xs.min(), xs.max()))
    t1 = []
    Zsm = nan_gauss(Zm[ymask], 1.5)
    ycont = {}
    for lev in levels:
        yc = contour_cols(Zsm, ys[ymask], lev)
        ycont[lev] = yc
        r = lee_vs_control(xs, yc, lee, ctrl, 0.5 * L, 2.0, label='LiDAR 2022-03-19, %+.0f m MSL contour' % lev)
        r['level_m_MSL'] = lev
        inwin = (xs >= lee[0] - 0.5 * L) & (xs <= lee[1] + 0.5 * L) & np.isfinite(yc)
        k = int(np.argmax(np.where(inwin, yc, -1e9)))
        r['peak_x_m'] = float(xs[k])
        r['peak_y_m'] = float(yc[k])
        r['peak_minus_reef_centre_x_m'] = float(xs[k] - xc)
        r['peak_above_south_control_mean_m'] = float(yc[k] - np.nanmean(yc[xs >= ctrl[1][0]]))
        r['peak_above_north_control_mean_m'] = float(yc[k] - np.nanmean(yc[xs <= ctrl[0][1]]))
        t1.append(r)
    sens = []
    for lev in levels:
        for nm, cc in (('west (north) control only', [ctrl[0]]), ('east (south) control only', [ctrl[1]])):
            r = lee_vs_control(xs, ycont[lev], lee, cc, 0.5 * L, 2.0, label='%+.0f m MSL contour, %s' % (lev, nm))
            r['level_m_MSL'] = lev
            sens.append(r)
    out['T1_contour_offset'] = dict(definition='cross-shore position y (m from the defence line) of the contour, first downward crossing from the shore; anomaly = mean y in the lee window minus the control trend '
                                               '(POSITIVE = contour farther offshore in the lee = bulge toward the reef). Placebo/analytic uncertainty as in lee_vs_control.', rows=t1,
                                    sensitivity_single_side_controls=sens)
    # T2: bed level in fixed bands (m from the defence line)
    t2 = []
    bands = [(40.0, 100.0), (100.0, 160.0), (160.0, 220.0)]
    cols = {}
    for b in bands:
        m = (ys >= b[0]) & (ys <= b[1])
        z = np.nanmean(np.where(m[:, None], Zm, np.nan), axis=0)
        cols[b] = z
        r = lee_vs_control(xs, z, lee, ctrl, 0.5 * L, 2.0, label='LiDAR 2022-03-19, mean bed level in y=%.0f-%.0f m' % b)
        r['band_y_m'] = b
        t2.append(r)
    y0_lee = float(np.nanmean(ycont[0.0][(xs >= lee[0]) & (xs <= lee[1])]))
    ymin_reef = float(allp[:, 1].min())
    north = polys[int(np.argmin([p_[:, 0].mean() for p_ in polys]))]
    out['Ls_over_X'] = ls_over_x(L, ymin_reef - y0_lee, float(allp[:, 1].mean()) - y0_lee,
                                 'Ls = both mounds (x %.0f..%.0f m); shoreline = mean 0 m MSL contour of the lee window (y = %.0f m, 2022); the northern mound alone has Ls = %.0f m (Ls/X toe = %.2f)'
                                 % (xa, xb, y0_lee, np.ptp(north[:, 0]), np.ptp(north[:, 0]) / (ymin_reef - y0_lee)))
    out['T2_bed_level_bands'] = dict(definition='mean bed level (m MSL) in y bands (distance from the defence line); anomaly = lee minus control trend; positive = bed higher in the lee', rows=t2)
    # sand-volume proxy: area above -1.5 m MSL between y=0 and y=250 per unit width
    # burial/settlement of the crest: the project's own comparison of LiDAR with design levels (VERIFY / HANDOFF)
    out['T4_burial_note'] = ('HANDOFF.md of the Borth folder: LiDAR DSM minus design levels above -2.0 mODN = +0.14 +- 0.28 m (crest strips; the DSM sees block tops), i.e. no sign of burial '
                             'or settlement of the crest 10 y after completion at the 0.3 m level. Not recomputed here.')
    STORE['borth'] = dict(xs=xs, ys=ys, Zm=Zm, ycont=ycont, polys=polys, lee=lee, ctrl=ctrl, L=L, cols=cols, levels=levels)
    return out


# ================================================================================================================= PALM BEACH (Gold Coast, chart-derived)
def run_palm_beach():
    m = load_model('palm-beach-gold-coast')
    poly = np.array(m['reef']['toe_polygon'])[:, :2]
    xa, xb = poly[:, 0].min(), poly[:, 0].max()
    L, xc = xb - xa, 0.5 * (xa + xb)
    ymin_reef = poly[:, 1].min()
    out = dict(reef='palm-beach-gold-coast', reef_alongshore_extent_L_m=float(L), reef_cross_shore_y_range_m=[float(poly[:, 1].min()), float(poly[:, 1].max())],
               data_source=('Garmin Navionics SonarChart iso-depth lines 1-10 m (1 m interval), read from z17 screenshots of maps.garmin.com (accessed 2026-10-05, "not for navigation"), '
                            'converted to the canonical frame; model.js navionics.lines; METHODS_3D 3.5. Chart datum assumed LAT (A5; RMS 0.29 m against the pre-reef City survey contours of '
                            'Mortensen et al. 2015 Fig 6a along ONE profile). The chart is compiled from sonar logs and surveys of UNKNOWN date; the reef (built 2019) is drawn as a smoothed shoal, '
                            'so contours of 4 m and deeper are bent by the reef itself (METHODS_3D 4.5: 47-81 m).'),
               datum='metres below chart datum (LAT) as printed; only RELATIVE contour positions are used')
    xs = np.arange(-250.0, 401.0, 10.0)
    lee = (xa, xb)
    ctrl = [(xc - 3.5 * L, xc - 1.5 * L), (xc + 1.5 * L, xc + 3.5 * L)]
    out['windows_x_m'] = dict(lee=lee, controls=ctrl)
    rows = []
    store = {}
    for e in m['navionics']['lines']:
        d = e['depth_chart_m']
        if d > 6:
            continue
        p = np.array(e['poly'])
        o = np.argsort(p[:, 0])
        yy = np.interp(xs, p[o, 0], p[o, 1], left=np.nan, right=np.nan)
        # np.interp clamps; blank outside the digitised x-range
        yy[(xs < p[:, 0].min()) | (xs > p[:, 0].max())] = np.nan
        store[d] = yy
        r = lee_vs_control(xs, yy, lee, ctrl, 0.5 * L, 10.0, label='Navionics SonarChart %.0f m contour' % d)
        r['chart_depth_m'] = d
        r['contour_inside_reef_influence'] = bool(d >= 4)
        rows.append(r)
    out['T1_contour_offset'] = dict(definition='y of the chart iso-line (m offshore of the waterline y=0 of the model frame) vs alongshore x; anomaly = lee mean - control trend; positive = contour '
                                               'farther offshore in the lee. Contours of 4 m and deeper (rows flagged) are bent by the reef itself in the chart and are NOT a sediment signal.', rows=rows)
    out['Ls_over_X'] = ls_over_x(L, ymin_reef, poly[:, 1].mean(), 'shoreline = model waterline y = 0 (Esri 2025-12-01, tide unknown)')
    STORE['palm'] = dict(xs=xs, ycont=store, lee=lee, ctrl=ctrl)
    return out


# ================================================================================================================= PRATTE'S (two surveys, vector contours)
def run_prattes():
    p = os.path.join(SHAPES, 'prattes-reef-el-segundo', '3d', 'src', 'bn2003_fig9_contours.json')
    d = json.load(open(p))
    th = math.radians(154.3)                         # contour bearing 154.3 deg true (METHODS_3D V15: sd 6.1 deg over 8 contours)
    a = np.array([math.sin(th), math.cos(th)])       # along-contour (alongshore) unit vector in (E, N)
    o = np.array([math.sin(th + 0.5 * math.pi), math.cos(th + 0.5 * math.pi)])   # offshore = bearing 244.3 deg (WSW; the shoreline fitted at 155.5 deg, ocean to the west, METHODS_3D A1)
    sets = {True: [], False: []}
    for e in d:
        pts = np.array(e['EN'], float)
        pts = pts - np.array([367505.0, 3754275.0])
        u, v = pts @ a, pts @ o
        sets[bool(e['solid'])].append((u, v))
    # order by mean v: shallow (-1 m) .. deep (-4 m)  (ASSUMPTION: depth increases offshore; levels -1..-4 m per METHODS_3D section 3.10)
    res = []
    for k, (uv_s, uv_d) in enumerate(zip(sorted(sets[True], key=lambda t: t[1].mean()), sorted(sets[False], key=lambda t: t[1].mean()))):
        us, vs = uv_s
        ud, vd = uv_d
        lo, hi = max(us.min(), ud.min()), min(us.max(), ud.max())
        g = np.linspace(lo, hi, 25)
        fs = np.interp(g, us[np.argsort(us)], vs[np.argsort(us)])
        fd = np.interp(g, ud[np.argsort(ud)], vd[np.argsort(ud)])
        dv = fs - fd                                  # solid (later) minus dashed (earlier): + = contour moved offshore
        res.append(dict(level_m=-(k + 1), overlap_alongshore_m=float(hi - lo), mean_shift_m=float(dv.mean()), max_abs_shift_m=float(np.abs(dv).max()), sd_m=float(dv.std()),
                        mean_offshore_position_m=float(fd.mean())))
    return dict(reef='prattes-reef-el-segundo',
                data_source=("Borrero & Nelsen (2003) Fig. 9, two bathymetric surveys (dashed = October 2000, four weeks after Phase I; solid = March 2001; METHODS_3D 3.10 / S10), contours -1..-4 m, vector paths "
                             "digitised by 3d/bn_digitise.py into 3d/src/bn2003_fig9_contours.json (UTM 11N, datum not stated). Window 112 x 71 m, reef (58 x 29 m, 435 m2) not drawn; reef position inside the window "
                             "is NOT known (+-150 m)."),
                result_rows=res,
                interpretation=("Contour-to-contour shifts between the two surveys are listed; the window (about 2 x the reef length) has no control section and the reef is not drawn, so no lee/control test is possible. "
                                "The paper itself states that the bathymetry did not change outside the contours made by the bags (S10)."))


# ================================================================================================================= ALBANY (pre-construction baseline only)
def run_albany_baseline():
    p = os.path.join(SHAPES, 'southern-ocean-surf-reef-albany', '3d', 'src', 'levels2_raw.json')
    d = json.load(open(p))
    xs = np.array([float(k) for k in d if d[k]])
    rows = []
    for lev in ('-1', '-2', '-3'):
        y = np.array([d[str(int(k))][lev] if d[str(int(k))] and d[str(int(k))].get(lev) is not None else np.nan for k in xs])
        ok = np.isfinite(y)
        pf = np.polyfit(xs[ok], y[ok], 1)
        res = y[ok] - np.polyval(pf, xs[ok])
        rows.append(dict(level_m=float(lev), n=int(ok.sum()), mean_y_m=float(y[ok].mean()), trend_m_per_100m=float(pf[0] * 100), resid_sd_after_trend_m=float(res.std(ddof=2)),
                         range_m=float(np.ptp(y[ok]))))
    return dict(reef='southern-ocean-surf-reef-albany',
                data_source=('RHDHV Option B plan (2015, PRE-construction; reef built Mar-Jun 2025) contour crossings read on 8 shore-normal transects 20 m apart (x = -160..-20 m), distance from the beach-face line, '
                             '3d/src/levels2_raw.json (colour reading, +-10 m for the deeper lines; METHODS_3D 3.2). BMT 2018 soundings: spot values only.'),
                baseline_rows=rows,
                use='NATURAL alongshore variability of the -1..-3 m contours before the reef (trend + residual sd) = a noise floor for any future post-construction comparison; no post-construction bathymetry exists in the repo.')


SKIPPED = {
    'narrowneck-gold-coast': ('SKIPPED: the only measured bed is Corbett et al. (2023) Fig. 3 (ICM 2017 pre-works multibeam) digitised by colour hue into a 164 x 145 m window that is filled by the reef itself '
                              '(no lee strip wider than 25 m, no control section; +-0.4 m colour-to-depth fit); outside the window the model bed is an ASSUMED alongshore-uniform profile (METHODS_3D 3.3: shoreward of y=190 '
                              'assumed). City of Gold Coast DTM has NO underwater cells at the reef (07_scale/bathymetry/gold_coast, Q1). Gold Coast beaches are continuously nourished and sand-bypassed (insight b), '
                              'so a shoreline signal would be confounded anyway. Literature pointers only (not tested here): Jackson et al. 2012 Fig. 16 (salient photo 20 May 2010), Mead & Borrero 2011 Fig. 5 '
                              '(beach width envelope), Blacka et al. 2013 p.98 (called the widening an artefact of the reference line).'),
    'mount-maunganui-reef': ('SKIPPED: bed = ASSUMED alongshore-uniform profile (Navionics profile + a reef-centre offset; METHODS_3D 3.3) plus a digitised 2013 multibeam window (178 x 148 m, mostly the reef). '
                             'The Navionics SonarChart z17 iso-lines (reef removed in 2014, so they show the ambient bed) trend by about 70 m over 320 m of coast near Mauao (2 m line: y = 320 m at x = -380 to 250 m at x = -60, 3d/navionics_isolines.json), '
                             'i.e. the natural gradient is larger than any plausible reef signal; BoPRC p.29: the bed fluctuates by more than 1 m.'),
    'bunbury-airwave': ('SKIPPED: the Airwave bladder was in the water for about 3 days in Dec 2019 (installed 9-13 Dec, torn, removed within about 3 days; model.js lifecycle), so no sediment response is possible. '
                        'The 2009 WA DoT airborne lidar grid in the model (10 m, gap-filled) is pre-structure.'),
    'prattes-reef-el-segundo': ('Seabed in the 3D model = ASSUMED alongshore-uniform profile (NOAA DEM 1/3 arc-sec + Navionics, METHODS_3D 3.4) -> SKIPPED for T1-T4; the two vector-contour surveys of Fig. 9 are summarised '
                                'separately under "prattes_two_surveys".'),
    'southern-ocean-surf-reef-albany': ('SKIPPED: the reef was built in 2025 and the repo holds only the PRE-construction 2015 contours and an assumed alongshore-uniform profile (A4); a baseline of natural alongshore '
                                        'variability is given under "albany_baseline".'),
    'kovalam-reef-india / opunake-reef / burkitts-reef-bargara / mexico-reef-2026-unnamed': ('SKIPPED: no 3D model and no bathymetry grid or survey in the repo (their src/ folders hold imagery, outlines and PDFs only; '
                                                                                           'opunake holds only a NZGD2000 grid-shift raster). Kovalam, Opunake and Burkitts: no data for a sediment test.'),
    'EMODnet DTM (07_scale/bathymetry/emodnet)': ('NOT USABLE for this test: cells of 115 x 73 m (about the reef size), reef invisible in every release 2018-2024 (Boscombe cell max -4.87 mLAT vs model crest +0.56), one sounding per cell at Borth, '
                                                  'interpolated at Haifa.'),
}


# ================================================================================================================= FIGURES
C_BLUE, C_ORANGE, C_GREY, C_GREEN, C_RED = '#0072B2', '#D55E00', '#6b6b6b', '#009E73', '#CC3311'


def _style():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 8, 'axes.titlesize': 8.5, 'axes.labelsize': 8, 'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.grid': True, 'grid.color': '#e4e4e4', 'grid.linewidth': 0.5, 'figure.dpi': 100, 'savefig.dpi': 170,
                         'legend.frameon': False, 'legend.fontsize': 7})
    return plt


def _check_layout(fig, name):
    """Programmatic layout check (no image viewing needed): report text/legend/colorbar boxes that overlap or leave the figure."""
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    items = []
    for ax in fig.axes:
        for t in [ax.title, ax._left_title, ax._right_title, ax.xaxis.label, ax.yaxis.label] + list(ax.texts):
            if t.get_text().strip() and t.get_visible():
                items.append((ax, t.get_text()[:30].replace('\n', ' '), t.get_window_extent(rend)))
        lg = ax.get_legend()
        if lg is not None:
            items.append((ax, 'legend', lg.get_window_extent(rend)))
    bad = []
    for i in range(len(items)):
        for k in range(i + 1, len(items)):
            a, b = items[i], items[k]
            if a[2].overlaps(b[2]) and not (a[0] is b[0] and ('legend' in (a[1], b[1])) and False):
                # texts annotating the same axes may overlap data but not each other
                bad.append((a[1], b[1]))
    W, H = fig.canvas.get_width_height()
    for ax, tx, bb in items:
        if bb.x1 > W + 2 or bb.x0 < -2:
            bad.append((tx, 'outside figure width'))
    # titles must not be wider than the axes + 12 % (they would run into the neighbour)
    for ax in fig.axes:
        t = ax._left_title
        if t.get_text().strip():
            bb, ab = t.get_window_extent(rend), ax.get_window_extent(rend)
            if bb.width > ab.width * 1.12:
                bad.append((t.get_text()[:30], 'title wider than its axes (%.0f > %.0f px)' % (bb.width, ab.width)))
    return bad


def fig_cables(res):
    plt = _style()
    from matplotlib.patches import Polygon as MPoly
    st = STORE['cables']
    gs, gn, L = st['gs'], st['gn'], st['L']
    fig = plt.figure(figsize=(7.4, 10.2))
    gsp = fig.add_gridspec(3, 2, height_ratios=[1.0, 1.0, 0.62], hspace=0.46, wspace=0.42, top=0.95, bottom=0.05, left=0.09, right=0.97)
    ax = fig.add_subplot(gsp[0, :])
    for a, b in st['ctrl']:
        ax.axvspan(a, b, color='#f1f1f1', zorder=0)
    ax.axvspan(-L / 2, L / 2, color='#ffe9cc', zorder=0)
    C = st['contours']
    for lev in (0, -1, -2):
        ax.plot(gs, C.get(('composite', lev)), color=C_GREY, lw=0.8)
    for lev in (-2, -3, -4, -5, -6):
        ax.plot(gs, C.get(('2002', lev)), color=C_BLUE, lw=1.1)
    for lev in (-4, -5, -6):
        y = C.get(('1995', lev))
        if y is not None:
            ax.plot(gs, y, color=C_ORANGE, lw=1.1, ls='--')
    ax.add_patch(MPoly(st['poly'], closed=True, fc='#444444', ec='k', lw=0.6, zorder=5))
    ax.text(-435, -305, 'grey: Perth_5m 0, -1, -2 m AHD (shore at the bottom)', color=C_GREY, fontsize=6.5, va='center')
    ax.set_xlim(-440, 440)
    ax.set_ylim(-320, 130)
    ax.set_xlabel('alongshore distance s from the reef centre (m, + towards NNE)')
    ax.set_ylabel('offshore distance n (m)')
    ax.set_title('(a) Contours (m AHD): 1995, before the reef (orange dashed); 2002 (blue)', loc='left', fontsize=7.6)
    ax.text(0, 118, 'lee', ha='center', fontsize=7, color='#8a5a00')
    ax.text(-275, 118, 'control', ha='center', fontsize=7, color=C_GREY)
    ax.text(275, 118, 'control', ha='center', fontsize=7, color=C_GREY)
    i = int(np.argmin(np.abs(gs - 230)))
    for lev in (-2, -3, -4, -5, -6):
        y = C.get(('2002', lev))
        if np.isfinite(y[i]):
            ax.text(236, y[i] + {-5: -9.0, -6: 9.0}.get(lev, 0.0), '%d' % lev, color=C_BLUE, fontsize=6.5, va='center')
    ax.set_aspect('equal', adjustable='box')
    ax2 = fig.add_subplot(gsp[1, 0])
    DZ = st['DZ']['2002-1995']
    sm, nm = (gs >= -200) & (gs <= 200), (gn >= -180) & (gn <= 190)
    im = ax2.pcolormesh(gs[sm], gn[nm], DZ[np.ix_(nm, sm)], cmap='RdBu_r', vmin=-0.6, vmax=0.6, shading='auto')
    ax2.add_patch(MPoly(st['poly'], closed=True, fc='none', ec='k', lw=0.8))
    b0, b1 = st['band']
    ax2.plot([-L / 2, L / 2, L / 2, -L / 2, -L / 2], [b0, b0, b1, b1, b0], color='k', lw=0.8, ls=':')
    ax2.set_aspect('equal', adjustable='box')
    ax2.set_xlabel('s (m)')
    ax2.set_ylabel('n (m)')
    ax2.set_title('(b) bed change 2002 - 1995', loc='left', fontsize=7.6)
    cb = fig.colorbar(im, ax=ax2, orientation='horizontal', fraction=0.045, pad=0.2)
    cb.set_label('m (red = bed higher; dotted box = lee band)', fontsize=6.5)
    cb.ax.tick_params(labelsize=6.5)
    ax3 = fig.add_subplot(gsp[1, 1])
    ctrl_t = [(-150.0, -75.0), (75.0, 125.0)]
    cm = np.zeros(len(gs), bool)
    for a, b in ctrl_t:
        cm |= (gs >= a) & (gs <= b)
    ax3.axvspan(-L / 2, L / 2, color='#ffe9cc', zorder=0)
    for lev, col in ((-4, C_BLUE), (-5, C_ORANGE), (-6, C_GREEN)):
        for tag, ls in (('1995', '--'), ('2002', '-')):
            y = C.get((tag, lev))
            if y is None:
                continue
            ax3.plot(gs, y - np.nanmean(y[cm]), color=col, ls=ls, lw=1.1, label='%d m, %s' % (lev, tag))
    ax3.axhline(0, color='k', lw=0.5)
    ax3.set_xlim(-200, 200)
    ax3.set_ylim(-50, 70)
    ax3.set_xlabel('s (m)')
    ax3.set_ylabel('contour minus adjacent-control mean (m)')
    ax3.set_title('(c) lee offset: 1995 (dashed) vs 2002', loc='left', fontsize=7.6)
    ax3.legend(ncol=2, loc='upper left')
    ax4 = fig.add_subplot(gsp[2, :])
    beach = STORE['cables_beach']
    ax4.axvspan(-L / 2, L / 2, color='#ffe9cc', zorder=0)
    for a, b in ((-385.0, -165.0), (165.0, 385.0)):
        ax4.axvspan(a, b, color='#f1f1f1', zorder=0)
    for (dk, A_), col in zip(beach.items(), ['#9ecae1', '#4292c6', '#08519c', '#fdae6b', '#d94801']):
        mc = ((A_[:, 0] >= -385) & (A_[:, 0] <= -165)) | ((A_[:, 0] >= 165) & (A_[:, 0] <= 385))
        ref = np.nanmean(A_[mc, 1])
        ax4.plot(A_[:, 0], A_[:, 1] - ref, color=col, lw=1.1, marker='o', ms=2.5, label=dk)
    ax4.axhline(0, color='k', lw=0.5)
    ax4.set_xlim(-400, 400)
    ax4.set_xlabel('s (m)')
    ax4.set_ylabel('0 m AHD contour minus\ncontrol mean (m)')
    ax4.set_title('(d) shoreline from beach-level surveys: a lee bulge at every date since Jan 2001 (13 months after completion), shrinking, not growing', loc='left', fontsize=7.4)
    ax4.legend(ncol=5, loc='upper left')
    fig.suptitle('Cables Reef (WA): the lee offsets predate the reef or do not grow; no change detectable 1995-2002', fontsize=9, x=0.09, ha='left', y=0.985)
    os.makedirs(FIG_DIR, exist_ok=True)
    bad = _check_layout(fig, 'cables')
    if bad:
        print('LAYOUT WARNINGS cables:', bad)
    fn = os.path.join(FIG_DIR, 'fig_sediment_cables-reef-wa.png')
    fig.savefig(fn, bbox_inches='tight')
    plt.close(fig)
    return fn


def fig_boscombe(res):
    plt = _style()
    st = STORE['boscombe']
    main, yearly, xr = st['main'], st['yearly'], st['xr']
    fig = plt.figure(figsize=(7.4, 7.0))
    gsp = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0], hspace=0.62, wspace=0.34, top=0.93, bottom=0.08, left=0.1, right=0.97)
    ax = fig.add_subplot(gsp[0, :])
    cols = ['#0b3c5d', '#0072B2', '#56B4E9', '#E69F00', '#D55E00', '#7a2e00']
    for p, c, x in zip(main, cols, xr):
        yy = sorted(yearly[p])
        ax.plot(yy, [yearly[p][y]['vol0'] for y in yy], color=c, lw=1.1, marker='o', ms=2.5, label='%s (x %+.0f m)' % (p[-3:], x + st['xc']))
    ax.axvspan(2008.4, 2009.9, color='#eeeeee', zorder=0)
    ax.text(2009.15, 0.97, 'reef\nbuilt', ha='center', va='top', fontsize=6.5, transform=ax.get_xaxis_transform())
    for j in st['jumps']:
        ax.axvspan(j['from_year'] + 0.5, j['to_year'] + 0.5, color='#ffe9cc', zorder=0)
        ax.text(j['to_year'] - 0.5, 0.97, 'all lines\nrise', fontsize=6.5, ha='center', va='top', transform=ax.get_xaxis_transform())
    ax.text(2016.0, 0.97, 'east lines\nonly', fontsize=6.5, ha='center', va='top', transform=ax.get_xaxis_transform(), color=C_GREY)
    ax.set_ylabel('beach volume above 0 m ODN\n(m3 per m)')
    ax.set_xlabel('year (yearly mean of the surveys)')
    ax.set_title('(a) CCO beach profiles: the whole frontage moves together (colour = alongshore position)', loc='left', fontsize=7.6)
    ax.legend(ncol=6, loc='upper center', bbox_to_anchor=(0.5, -0.22), columnspacing=1.0, handletextpad=0.4)
    for k, (metric, ttl, ylab, pos) in enumerate((('y_0.0', '(b) 0 m ODN contour', 'change vs frontage mean,\npost - pre (m)', gsp[1, 0]),
                                                  ('vol0_m3_per_m', '(c) volume above 0 m ODN', 'change vs frontage mean,\npost - pre (m3/m)', gsp[1, 1]))):
        a = fig.add_subplot(pos)
        c = st['C'][metric]
        a.axvspan(res['reef_x_range'][0], res['reef_x_range'][1], color='#ffe9cc', zorder=0)
        x = np.array(c['x_rel_m']) + st['xc']
        a.errorbar(x, c['change_rel'], yerr=c['se_change'], fmt='o', color=C_BLUE, ms=4, capsize=2, lw=1)
        ctrl_mask = np.array([abs(v) >= 1.5 * st['L'] for v in c['x_rel_m']])
        pf = np.polyfit(np.array(c['x_rel_m'])[ctrl_mask], np.array(c['change_rel'])[ctrl_mask], 1)
        xx = np.linspace(x.min() - 10, x.max() + 10, 20)
        a.plot(xx, np.polyval(pf, xx - st['xc']), color=C_GREY, lw=1, ls='--', label='line through the 4 controls')
        lee = np.array([abs(v) <= 0.75 * st['L'] for v in c['x_rel_m']])
        a.plot(x[lee], np.array(c['change_rel'])[lee], 'o', color=C_ORANGE, ms=6, mfc='none', mew=1.2, label='lee lines')
        a.axhline(0, color='k', lw=0.5)
        a.set_xlabel('alongshore position x (m, east right)')
        a.set_ylabel(ylab)
        a.set_title('%s: lee anomaly %+.1f\n(95%% CI %+.1f to %+.1f)' % (ttl, c['lee_anomaly'], c['lee_anomaly_ci95'][0], c['lee_anomaly_ci95'][1]), loc='left', fontsize=7.6)
        if k == 0:
            a.legend(loc='upper left')
    fig.suptitle('Boscombe (UK): shoreline response before (2004-08) and after (2009-26) the reef', fontsize=9, x=0.1, ha='left', y=0.985)
    bad = _check_layout(fig, 'boscombe')
    if bad:
        print('LAYOUT WARNINGS boscombe:', bad)
    fn = os.path.join(FIG_DIR, 'fig_sediment_boscombe-surf-reef.png')
    fig.savefig(fn, bbox_inches='tight')
    plt.close(fig)
    return fn


def fig_borth(res):
    plt = _style()
    from matplotlib.patches import Polygon as MPoly
    st = STORE['borth']
    xs, ys, Zm = st['xs'], st['ys'], st['Zm']
    fig = plt.figure(figsize=(7.4, 7.2))
    gsp = fig.add_gridspec(2, 1, height_ratios=[1.25, 1.0], hspace=0.38, top=0.93, bottom=0.07, left=0.09, right=0.93)
    ax = fig.add_subplot(gsp[0])
    im = ax.pcolormesh(xs, ys, Zm, cmap='Blues_r', vmin=-2.4, vmax=1.5, shading='auto')
    ax.contour(xs, ys, nan_gauss(Zm, 1.5), levels=[-2.0, -1.0, 0.0], colors=[C_RED, C_ORANGE, 'k'], linewidths=[0.9, 0.9, 0.9])
    for p in st['polys']:
        ax.add_patch(MPoly(p, closed=True, fc='#8a8a8a', ec='k', lw=0.6, zorder=5))
    a, b = st['lee']
    for v in (a, b):
        ax.axvline(v, color='k', lw=0.8, ls=':')
    ax.set_xlim(xs.min(), xs.max())
    ax.set_ylim(-40, 320)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('alongshore x (m, + towards south)')
    ax.set_ylabel('offshore y from the defence line (m)')
    ax.set_title('(a) LiDAR DTM 19 Mar 2022 (m MSL); contours 0 black, -1 orange, -2 red; grey = reef', loc='left', fontsize=7.6)
    cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01)
    cb.ax.tick_params(labelsize=6.5)
    ax.text(-285, 62, 'unexplained\nshore-parallel\nridge (west control)', fontsize=6, color='k', va='top')
    ax2 = fig.add_subplot(gsp[1])
    for (c0, c1) in st['ctrl']:
        ax2.axvspan(c0, c1, color='#f1f1f1', zorder=0)
    ax2.axvspan(a, b, color='#ffe9cc', zorder=0)
    for lev, col in zip(st['levels'], ['k', C_ORANGE, C_RED]):
        ax2.plot(xs, st['ycont'][lev], color=col, lw=1.2, label='%+.0f m MSL' % lev)
    ax2.axvline(res['reef_centre_x_m'], color=C_GREY, lw=0.8, ls='--')
    ax2.text(res['reef_centre_x_m'] + 4, 268, 'reef centre', fontsize=6.5, color=C_GREY, va='top')
    ax2.set_xlim(xs.min(), xs.max())
    ax2.set_ylim(30, 275)
    ax2.set_xlabel('alongshore x (m, + towards south)')
    ax2.set_ylabel('contour position y (m)')
    ax2.legend(ncol=3, loc='upper left')
    t = res['T1_contour_offset']['rows']
    ax2.set_title('(b) lee offset (trend through both controls): %s m for 0/-1/-2 m\n    range over control choices: %s' % (' / '.join('%+.0f' % r['anomaly'] for r in t), '; '.join('%+.0f..%+.0f' % tuple(r['anomaly_range']) for r in t)),
                  loc='left', fontsize=7.4)
    fig.suptitle('Borth (Wales): a lee bulge in the 2022 survey; no pre-construction survey', fontsize=9, x=0.09, ha='left', y=0.985)
    bad = _check_layout(fig, 'borth')
    if bad:
        print('LAYOUT WARNINGS borth:', bad)
    fn = os.path.join(FIG_DIR, 'fig_sediment_borth-coastal-defence-reef.png')
    fig.savefig(fn, bbox_inches='tight')
    plt.close(fig)
    return fn


# ================================================================================================================= DRIVER
def _f(v, nd=1, sign=True):
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return 'n/a'
    txt = ('%+.*f' if sign else '%.*f') % (nd, v)
    if float(txt) == 0.0:
        txt = '%.*f' % (nd, 0.0)
    return txt


def build_summary():
    R = load_results()
    S = []
    if 'cables-reef-wa' in R:
        c = R['cables-reef-wa']
        t1 = {(r['dataset'], r['level_m_AHD'], r['lee']): r for r in c['T1_contour_offset']['rows']}
        comp = sorted([t1[(k, l, 'lee_L')] for (k, l, w) in t1 if k.startswith('Perth_5m') and w == 'lee_L'], key=lambda r: -r['level_m_AHD'])
        s02 = [r for r in c['T1_contour_offset']['rows'] if r['dataset'].endswith('2002') and r['lee'] == 'lee_L']
        b = {(r['survey'], r['level_m_AHD']): r for r in c['T1b_contour_offset_adjacent_controls_1995_vs_2002']['rows']}
        mig = {r['level_m_AHD']: r for r in c['T3_contour_migration_2002_minus_1995']}
        dd = c['T3_dz_difference_in_differences'][0]
        box = {(r['pair'], r['box']): r for r in c['T3_temporal_boxes']['rows']}
        nf = c['dz_cell_statistics_outside_reef_buffer']
        def ring(survey, prefix):
            return [r for r in c['T4_rings_post_minus_1998_bed']['rows'] if r['survey'] == survey and r['zone'].startswith(prefix) and r['sector'] == 'all'][0]
        rs = c['T4_reef_surface_2002_minus_1999_matched_within_3m']
        S.append(dict(
            reef='cables-reef-wa', test='T1 shoreline / contour offset (lee vs far controls)',
            data='DoT WA single-beam 1995-12, 1998-03, 1999-11, 2002-02 + Perth_5m composite (undated mix)',
            signal='yes in the data, NOT attributable to the reef',
            magnitude='lee contours %s m (0 m AHD), %s (-1), %s (-2), %s (-3), %s (-4) from the composite; %s..%s m for -2..-6 m in the 2002 survey, versus controls 1.5-3.5 L away'
                      % (_f(comp[0]['anomaly'], 0), _f(comp[1]['anomaly'], 0), _f(comp[2]['anomaly'], 0), _f(comp[3]['anomaly'], 0), _f(comp[4]['anomaly'], 0),
                         _f(min(r['anomaly'] for r in s02), 0), _f(max(r['anomaly'] for r in s02), 0)),
            uncertainty='formal SE %.0f-%.0f m (placebo sd %.1f-%.1f m); the north-only and south-only controls give the same sign and agree within %.0f m (anomaly_range in the JSON), so the offset is a robust spatial feature; '
                        'its ATTRIBUTION is the problem, not its existence'
                        % (min(r['se_analytic'] for r in comp + s02), max(r['se_analytic'] for r in comp + s02), min(r['placebo_sd'] for r in comp + s02), max(r['placebo_sd'] for r in comp + s02),
                           max(r['anomaly_range'][1] - r['anomaly_range'][0] for r in comp + s02 if r['level_m_AHD'] >= -4)),
            caveats='THE SAME BULGE IS IN THE 1995 PRE-CONSTRUCTION SURVEY: -5 m contour lee offset %s m (1995) vs %s m (2002) against adjacent strips; -6 m: %s vs %s m. The shoreward contours (0 to -3 m) '
                    'have no pre-construction survey (1995 reaches only -2.45 m AHD, at n >= -167 m). Natural limestone reef lines of the Cottesloe coast are the likely cause (ASSUMPTION, not verified).'
                    % (_f(b[('1995', -5)]['anomaly'], 0), _f(b[('2002', -5)]['anomaly'], 0), _f(b[('1995', -6)]['anomaly'], 0), _f(b[('2002', -6)]['anomaly'], 0))))
        S.append(dict(
            reef='cables-reef-wa', test='T3 temporal change 1995 -> 2002 (before/after, lee vs adjacent controls)',
            data='single-beam 1995-12 (pre) and 2002-02 (2.2 y after completion), TIN <= 25 m from a sounding', signal='NO',
            magnitude='contour migration 2002-1995 in the lee relative to adjacent strips: %s m (-4 m), %s m (-5 m), %s m (-6 m); bed change in the lee band (n = -165..-62 m): %s m '
                      '(lee %s m, adjacent strips %s / %s m), volume %s m3 over %.0f %% of the box'
                      % (_f(mig[-4]['anomaly'], 1), _f(mig[-5]['anomaly'], 1), _f(mig[-6]['anomaly'], 1), _f(dd['anomaly'], 2), _f(box[('2002-1995', 'lee')]['mean_dz_m'], 2),
                         _f(box[('2002-1995', 'ctrl_S')]['mean_dz_m'], 2), _f(box[('2002-1995', 'ctrl_N')]['mean_dz_m'], 2), _f(box[('2002-1995', 'lee')]['volume_change_m3'], 0),
                         100 * box[('2002-1995', 'lee')]['coverage']),
            uncertainty='noise floor: single-beam cell sd %.2f m, pre-construction pair (1998 vs 1995) mean %s m, sd %.2f m; a +-0.1 m systematic survey offset = +-1,100 m3 over the lee box (11,300 m2)'
                        % (nf['2002-1995']['sd_m'], _f(nf['1998-1995']['mean_m'], 2), nf['1998-1995']['sd_m']),
            caveats='only 2.2 y after completion; controls are adjacent (1.4-2.7 half-lengths) and may lie inside the reef influence; the contour migration of %s..%s m (formal SE %.0f-%.0f m) equals a bed rise of about '
                    '0.1-0.2 m at the local slope (1:15 to 1:40, ASSUMPTION read from the contour spacing) = within the +-0.1 m systematic offset between surveys; Ls/X = %.2f (toe) / %.2f (centre): the reef is short relative to its '
                    'distance from the shore (thresholds not asserted here)'
                    % (_f(min(r['anomaly'] for r in mig.values()), 0), _f(max(r['anomaly'] for r in mig.values()), 0), min(r['se_analytic'] for r in mig.values()), max(r['se_analytic'] for r in mig.values()),
                       c['Ls_over_X']['Ls_over_X_toe'], c['Ls_over_X']['Ls_over_X_centre'])))
        t2r = {r['label'][:8]: r for r in c['T2_bed_level_lee_band']['rows']}
        S.append(dict(
            reef='cables-reef-wa', test='T2 bed level in the lee band (n = -165..-62 m) vs controls',
            data='single-beam 1995 (pre) and 2002 (post), Perth_5m composite', signal='yes, but PRE-EXISTING (natural high in the lee)',
            magnitude='lee band bed higher than the far controls by %s m in 2002 (range %s..%s over control choice) and by %s m already in 1995 (single-sided control, n=9 samples), %s m in the Perth_5m composite'
                      % (_f(t2r['DoT 2002']['anomaly'], 2), _f(t2r['DoT 2002']['anomaly_range'][0], 2), _f(t2r['DoT 2002']['anomaly_range'][1], 2), _f(t2r['DoT 1995']['anomaly'], 2), _f(t2r['Perth_5m']['anomaly'], 2)),
            uncertainty='formal SE 0.05 m (2002); datum offsets between surveys +-0.1 m',
            caveats='the high bed in the lee is as large before as after the reef: not a sediment-transport effect of the reef within the data'))
        t5 = {(r['date'], r['level_m_AHD']): r for r in c['T5_beach_levels_spatial']['rows']}
        t5c = {(r['from_date'], r['to_date'], r['level_m_AHD']): r for r in c['T5b_beach_levels_change']['rows']}
        S.append(dict(
            reef='cables-reef-wa', test='T5 shoreline from beach-level surveys 2001-2012 (lee lines vs control lines)',
            data='DoT WA beach point-elevation files Jan 2001 (13 months after completion), Feb 2002, Jan 2003, Aug 2011, Apr 2012; profile lines about 50 m apart; 2 lee lines, 6-8 control lines',
            signal='yes (a lee shoreline bulge at every date) but shrinking, not growing; no pre-construction beach survey: inconclusive',
            magnitude='0 m AHD contour, lee minus controls: %s m (2001-01), %s (2002-02), %s (2003-01), %s (2011-08), %s (2012-04); change 2001-01 to 2012-04 %s m (+1 m contour: %s m)'
                      % tuple([_f(t5[(d, 0.0)]['anomaly'], 0) for d in ('2001-01', '2002-02', '2003-01', '2011-08', '2012-04')] + [_f(t5c[('2001-01', '2012-04', 0.0)]['anomaly'], 0), _f(t5c[('2001-01', '2012-04', 1.0)]['anomaly'], 0)]),
            uncertainty='3-4 lines per control strip, no formal SE; north-only and south-only controls differ by up to %.0f m (anomaly_range); scatter between dates 10-26 m'
                        % max(r['anomaly_range'][1] - r['anomaly_range'][0] for r in c['T5_beach_levels_spatial']['rows'] if r['level_m_AHD'] == 0.0),
            caveats='a salient that grows after construction would increase this number; it decreases by about 14 m in 11 y. A decaying initial feature, a natural feature (the offshore -5/-6 m contours show a lee hump already in 1995) '
                    'and beach management at Leighton/Port Beach (NOT checked) are all compatible; the 2011-12 files cover a longer shore with a regional gradient of about 0.05 m/m'))
        S.append(dict(
            reef='cables-reef-wa', test='T2/T4 scour, burial',
            data='post-construction soundings vs the 1998 pre-construction TIN; 1999-11 vs 2002-02 reef surface', signal='NO scour; no burial detectable',
            magnitude='ring 0-10 m outside the footprint %s m (1999) / %s m (2002) above the 1998 bed (rock spill, edge definition +-5 m); 10-25 m: %s / %s m; 25-50 m (2002) %s m; 50-100 m %s m. Reef surface 2002 minus 1999 at matched '
                      'soundings %s m (n=%d, sd %.2f m); 95th-percentile level inside the footprint %.2f (1999) vs %.2f m AHD (2002)'
                      % (_f(ring('1999', 'ring 0-10 m')['mean_dz_m'], 2), _f(ring('2002', 'ring 0-10 m')['mean_dz_m'], 2), _f(ring('1999', 'ring 10-25 m')['mean_dz_m'], 2),
                         _f(ring('2002', 'ring 10-25 m')['mean_dz_m'], 2), _f(ring('2002', 'ring 25-50 m')['mean_dz_m'], 2), _f(ring('2002', 'ring 50-100 m')['mean_dz_m'], 2),
                         _f(rs['mean_m'], 2), rs['n'], rs['sd_m'], rs['z95_inside_footprint_1999'], rs['z95_inside_footprint_2002']),
            uncertainty='sounding sd 0.3 m; positioning of soundings on a rough rock surface +-several m; SE in the JSON ignores spatial correlation',
            caveats='an echo-sounder cannot separate sand cover from rock fall-down; negative values (toe scour) do not occur beyond 10 m'))
    if 'boscombe-surf-reef' in R:
        b = R['boscombe-surf-reef']
        C = b['C_common_mode_removed_BACI']['metrics']
        Dm = b['D_post_only_alongshore_pattern_11_lines']['metrics']
        S.append(dict(
            reef='boscombe-surf-reef', test='BACI of the shoreline at 6 CCO lines (common-mode removed) and post-only alongshore pattern (11 lines)',
            data='CCO beach profiles 2004-2026 (316 surveys on 11 lines); pre = 2004-07..2008-04 (5-16 dates), post = 2009-11..2026-03 (17-43 dates)',
            signal='NO (at most a few metres; not distinguishable from management and tilt signals)',
            magnitude='lee anomaly of the 0 m ODN contour %s m (95%% CI %s..%s), +1 m contour %s m (%s..%s), volume above 0 m ODN %s m3/m (%s..%s); post-only 11 lines: %s +- %s m (0 m), %s +- %s m (+1 m)'
                      % (_f(C['y_0.0']['lee_anomaly'], 1), _f(C['y_0.0']['lee_anomaly_ci95'][0], 1), _f(C['y_0.0']['lee_anomaly_ci95'][1], 1),
                         _f(C['y_+1.0']['lee_anomaly'], 1), _f(C['y_+1.0']['lee_anomaly_ci95'][0], 1), _f(C['y_+1.0']['lee_anomaly_ci95'][1], 1),
                         _f(C['vol0_m3_per_m']['lee_anomaly'], 1), _f(C['vol0_m3_per_m']['lee_anomaly_ci95'][0], 1), _f(C['vol0_m3_per_m']['lee_anomaly_ci95'][1], 1),
                         _f(Dm['y_0.0']['lee_anomaly_mean'], 1), _f(Dm['y_0.0']['lee_anomaly_se'], 1, False), _f(Dm['y_+1.0']['lee_anomaly_mean'], 1), _f(Dm['y_+1.0']['lee_anomaly_se'], 1, False)),
            uncertainty='bootstrap over survey dates; pre n = 5 dates only for 4 of the 6 lines; dates are not independent',
            caveats='Poole Bay is groyned and recharged: the frontage-wide volume jumps (%s) are common to all lines (DERIVED indicator; recharge records not in the repo); about 23,000 m3 of sand was piled on the upper beach to build the reef '
                    '(Rendle 2016 thesis p.125-127: 11,100 m3 stayed on the beach between the pier and the first groyne), which could mimic accretion; the shoreline tilts east-up/west-down by %s m per 100 m after the reef '
                    '(a tilt, not a local bulge); the largest 0 m contour advance 2009-11 -> 2010-04 was %s m (the statement of up to 60 m in 6 months, Mead & Borrero 2011, is not reproduced at these lines)'
                    % ('; '.join('%d->%d: %+.0f m3/m' % (j['from_year'], j['to_year'], j['median_change_m3_per_m']) for j in b['B_common_mode_volume_jumps']['rows']),
                       _f(C['y_0.0']['control_trend_slope_per_100m'], 1), _f(b['E_six_month_changes_2008_2010']['max_advance_m'], 1))))
    if 'borth-coastal-defence-reef' in R:
        b = R['borth-coastal-defence-reef']
        t1 = b['T1_contour_offset']['rows']
        t2 = b['T2_bed_level_bands']['rows']
        S.append(dict(
            reef='borth-coastal-defence-reef', test='T1/T2 lee vs control contour position and bed level, single LiDAR date',
            data='Welsh Government LiDAR DTM 2022-03-19 (1 m), beach and foreshore down to about -2.3 mODN; Phase 1 completed 2012-03-08',
            signal='yes (bulge) but NOT attributable: inconclusive',
            magnitude='lee contour offset %s m (0 m MSL), %s (-1), %s (-2) with a straight line through both controls; range over control choice %s..%s, %s..%s, %s..%s m; bed level in the lee higher by %s, %s, %s m '
                      '(y = 40-100, 100-160, 160-220 m; ranges %s..%s, %s..%s, %s..%s)'
                      % (_f(t1[0]['anomaly'], 0), _f(t1[1]['anomaly'], 0), _f(t1[2]['anomaly'], 0), _f(t1[0]['anomaly_range'][0], 0), _f(t1[0]['anomaly_range'][1], 0), _f(t1[1]['anomaly_range'][0], 0),
                         _f(t1[1]['anomaly_range'][1], 0), _f(t1[2]['anomaly_range'][0], 0), _f(t1[2]['anomaly_range'][1], 0), _f(t2[0]['anomaly'], 2), _f(t2[1]['anomaly'], 2), _f(t2[2]['anomaly'], 2),
                         _f(t2[0]['anomaly_range'][0], 2), _f(t2[0]['anomaly_range'][1], 2), _f(t2[1]['anomaly_range'][0], 2), _f(t2[1]['anomaly_range'][1], 2), _f(t2[2]['anomaly_range'][0], 2), _f(t2[2]['anomaly_range'][1], 2)),
            uncertainty='formal SE 2-9 m, but the choice of control (north strip vs south strip) changes the anomaly by 30-90 m: the beach has a strong natural north-south gradient (village frontage vs dune frontage)',
            caveats='ONE survey 10 y after construction, no pre-construction beach survey in the repo; the south control strip shows the bulge is only +12 m (0 m MSL) and +0.5 m (-1 m) above the southern plateau, so a '
                    'localised peak of about 20-26 m sits on top of a north-south step; the tile is only 730 m long so controls start 0.5 L from the reef; seasonal beach state (March) and bars not considered. '
                    'Crest check from the project (HANDOFF): LiDAR minus design +0.14 +- 0.28 m, no burial.'))
    if 'palm-beach-gold-coast' in R:
        b = R['palm-beach-gold-coast']
        rows = [r for r in b['T1_contour_offset']['rows'] if not r['contour_inside_reef_influence']]
        S.append(dict(
            reef='palm-beach-gold-coast', test='T1 contour offset, chart-derived',
            data='Garmin Navionics SonarChart 1-3 m iso-lines (z17 screenshots 2026-10-05), undated compilation; reef built 2019',
            signal='NO (|anomaly| <= 3 m)',
            magnitude='; '.join('%d m: %s m (range %s..%s)' % (r['chart_depth_m'], _f(r['anomaly'], 1), _f(r['anomaly_range'][0], 0), _f(r['anomaly_range'][1], 0)) for r in rows),
            uncertainty='chart contours are smoothed (a 0.5 m label interval, positional error likely +-10 m, ASSUMPTION), datum and date unknown',
            caveats='LOW CONFIDENCE; 4-6 m contours are bent by the reef shoal in the chart (+38 to +71 m) and are a chart artefact; the Gold Coast is nourished continuously (insight b), natural reef up-coast and bars are in the chart; no pre-reef contour set was digitised '
                    '(Mortensen et al. 2015 Fig. 6a is read along ONE profile only).'))
    if 'prattes_two_surveys' in R:
        pr = R['prattes_two_surveys']
        S.append(dict(
            reef='prattes-reef-el-segundo', test='two surveys, contour shift (Oct 2000 -> Mar 2001)',
            data='Borrero & Nelsen (2003) Fig. 9 vector contours -1..-4 m (112 x 71 m window)', signal='inconclusive',
            magnitude='all four contours moved offshore by %s m on average (%s..%s m per contour)'
                      % (_f(float(np.mean([r['mean_shift_m'] for r in pr['result_rows']])), 0), _f(min(r['mean_shift_m'] for r in pr['result_rows']), 0), _f(max(r['mean_shift_m'] for r in pr['result_rows']), 0)),
            uncertainty='survey datum / tide differences of 0.3 m would shift a 1:35 contour by about 10 m; digitising +-1 m',
            caveats='no control section, reef not drawn, window about 2 reef lengths; the source states there is no change outside the bag contours'))
    return S


def main(argv):
    targets = [a for a in argv if not a.startswith('--') and os.path.sep not in a and a != SCRATCH]
    allt = ['cables', 'boscombe', 'borth', 'navionics', 'skips', 'figures']
    if not targets:
        targets = allt
    os.makedirs(SCRATCH, exist_ok=True)
    meta = dict(script='08_paper/analysis/seabed_sediment.py', run_date='2026-10-15', python=sys.version.split()[0], numpy=np.__version__,
                note='All numbers DERIVED from the project-held bathymetry (read-only). ASSUMPTION flags are in the text fields. Positive anomalies = contour farther offshore / bed higher in the lee.')
    save_results('_meta', meta)
    figs = []
    if 'cables' in targets or 'figures' in targets:
        save_results('cables-reef-wa', run_cables())
    if 'boscombe' in targets or 'figures' in targets:
        save_results('boscombe-surf-reef', run_boscombe())
    if 'borth' in targets or 'figures' in targets:
        save_results('borth-coastal-defence-reef', run_borth())
    if 'navionics' in targets:
        save_results('palm-beach-gold-coast', run_palm_beach())
        save_results('prattes_two_surveys', run_prattes())
        save_results('albany_baseline', run_albany_baseline())
    if 'skips' in targets:
        save_results('skipped', SKIPPED)
    if 'figures' in targets:
        R = load_results()
        if 'cables' in STORE:
            figs.append(fig_cables(R['cables-reef-wa']))
        if 'boscombe' in STORE:
            figs.append(fig_boscombe(R['boscombe-surf-reef']))
        if 'borth' in STORE:
            figs.append(fig_borth(R['borth-coastal-defence-reef']))
    save_results('summary_table', build_summary())
    print('written', OUT_JSON, '; figures:', figs)


if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore', category=RuntimeWarning)
    main(sys.argv[1:])

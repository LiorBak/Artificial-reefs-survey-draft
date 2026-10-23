#!/usr/bin/env python3
"""surf_analysis.py - reef effect on breaking and surf quality (RESULTS.md parts 1-5).

Run:    python3 08_paper/analysis/surf_analysis.py
Reads:  reef_inputs.py (profiles, tides, site waves), results_hypsometry.json (hypsometry.py)
Writes: results_breaking.csv (every reef x line x H x T x tide), results_surf_site.csv (site wave, 3 tides, primary line),
        results_peel.csv, results_tide_window.csv, results_size.csv, results_surf.json (all + metadata)

Model (DERIVED; see RESULTS.md section 2): 1-D cross-shore transformation along each model profile (crest_line =
primary, centreline and second_crest_line = spread). Water depth d(y) = eta - max(seabed, reef). A wave of deep-water
height H0 and period T is shoaled with linear theory (Ks, normal incidence, no refraction, no friction) and breaks at
the first point (from offshore) where H >= gamma d; gamma = 0.78 (McCowan 1894), sensitivity gamma = 0.55 and the
slope-dependent Weggel (1972) index. Break position is classed against the reef toe and crest zone of that line.
Bed slope at the break (tan beta) = least-squares slope of the surface over a window of width max(4 m, L_b/4) centred on
the break point (alternative windows reported). xi_b = tan beta / sqrt(H_b / L0) (Battjes 1974), vortex ratio
Y = 0.065 / tan beta + 0.821 (Mead & Black 2001), peel angle by Snell refraction from the arm angle (wavelib).
"""
import csv
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wavelib as W  # noqa: E402
import reef_inputs as RI  # noqa: E402

H_SET = [0.5, 1.0, 1.5, 2.0, 3.0]
T_SET = [6.0, 8.0, 10.0, 12.0, 14.0]
GAMMAS = {'mccowan': 0.78, 'low': 0.55}
LINES = ['crest_line', 'centreline', 'second_crest_line']
WORKS = ('on_ramp', 'on_crest')


# ------------------------------------------------------------------------------------------------ profile handling
def prof_arrays(line):
    p = line['profile']
    y = np.array(p['offshore_m'], float)
    zb = np.array([np.nan if v is None else v for v in p['seabed_msl_m']], float)
    zr = np.array([np.nan if v is None else v for v in p['reef_msl_m']], float)
    ok = np.isfinite(zb)
    y, zb, zr = y[ok], zb[ok], zr[ok]
    zs = np.where(np.isfinite(zr), np.maximum(zr, zb), zb)
    o = np.argsort(-y)  # offshore -> shore
    return y[o], zb[o], zr[o], zs[o]


def prepare_met(met, y, zb, zr):
    """Copy of the line metrics plus the outermost reef point (outer toe) and its depths, from the profile arrays."""
    m = dict(met)
    if np.isfinite(zr).any():
        i = int(np.argmax(np.where(np.isfinite(zr), y, -1e9)))
        m['outer_toe_y'] = float(y[i])
        m['outer_toe_reef_z'] = float(zr[i])
        m['outer_toe_bed_z'] = float(zb[i])
    else:
        m['outer_toe_y'] = met.get('seaward_toe_y_m', float('nan'))
        m['outer_toe_reef_z'] = met.get('seaward_toe_reef_z_msl_m', float('nan'))
        m['outer_toe_bed_z'] = met.get('seaward_toe_seabed_z_msl_m', float('nan'))
    return m


def local_slope(y, zs, yc, width):
    """Least-squares slope of the surface (rising toward the shore, i.e. dz/d(-y)) over |y - yc| <= width/2."""
    sel = np.abs(y - yc) <= width / 2 + 1e-9
    if sel.sum() < 3:
        return float('nan')
    A = np.vstack([-y[sel], np.ones(sel.sum())]).T
    m = np.linalg.lstsq(A, zs[sel], rcond=None)[0][0]
    return float(m)


def window_slope(y, zs, y0, y1):
    sel = (y >= min(y0, y1) - 1e-9) & (y <= max(y0, y1) + 1e-9)
    if sel.sum() < 3:
        return float('nan')
    A = np.vstack([-y[sel], np.ones(sel.sum())]).T
    return float(np.linalg.lstsq(A, zs[sel], rcond=None)[0][0])


def transform(y, zs, H0, T, eta, gamma='mccowan'):
    """Shoal from offshore; return the first breaking point. gamma: 'mccowan' (0.78), 'low' (0.55) or 'weggel'."""
    d = eta - zs
    wet = d > 0.02
    H = np.full_like(d, np.nan)
    H[wet] = H0 * W.shoaling_coefficient(T, d[wet])
    for i in range(len(y)):
        if not wet[i]:
            return dict(i=i, y=float(y[i]), d=float(max(d[i], 0)), H=float(H[i - 1]) if i else float('nan'), shore=True)
        if gamma == 'weggel':
            j = max(0, i - 5)   # 5 m seaward of i (arrays run offshore -> shore)
            m = max(1e-4, (zs[i] - zs[j]) / max(y[j] - y[i], 1e-6)) if i > j else 1e-3
            g = W.gamma_weggel(min(m, 0.1), H[i], T)   # Weggel calibrated to m <= 0.1; steeper slopes capped (ASSUMPTION)
        else:
            g = GAMMAS[gamma]
        if H[i] >= g * d[i]:
            # 2026-10-16 fix: the 1 m grid let a wave cross a steep face in one step, so H/d at the detected point reached
            # up to 5 (physically impossible). Locate the crossing H0 Ks(d) = g d inside the last 1 m segment instead
            # (depth interpolated linearly along the segment).
            if i > 0 and wet[i - 1] and d[i - 1] > d[i]:
                dd = np.linspace(d[i], d[i - 1], 41)                      # shallow -> deep
                Hd = H0 * W.shoaling_coefficient(T, dd)
                okb = np.where(Hd >= g * dd)[0]
                j = int(okb.max()) if len(okb) else 0                    # deepest depth on the segment that breaks
                fr = (d[i - 1] - dd[j]) / (d[i - 1] - d[i])
                return dict(i=i, y=float(y[i - 1] + fr * (y[i] - y[i - 1])), d=float(dd[j]), H=float(Hd[j]), shore=False,
                            gamma=float(g))
            return dict(i=i, y=float(y[i]), d=float(d[i]), H=float(H[i]), shore=False, gamma=float(g))
    return dict(i=None, y=float('nan'), d=float('nan'), H=float('nan'), shore=True)


def classify(yb, met):
    """Break position vs the reef on this line (y offshore; toe at larger y). The seaward toe is the OUTERMOST reef point
    on the line (met['outer_toe_y'], set by prepare_met), so container fields with gaps count as one reef."""
    if not met.get('reef_on_line') or not np.isfinite(yb):
        return 'no_reef_on_line' if not met.get('reef_on_line') else 'passes_reef'   # no break within the profile = passes
    toe = met.get('outer_toe_y', met['seaward_toe_y_m'])
    cz = met['crest_zone_y_m']
    back = met.get('shoreward_toe_y_m', cz[0])
    if yb > toe + 0.5:
        return 'before_reef'
    if yb > cz[1] + 0.5:
        return 'on_ramp'
    if yb >= cz[0] - 0.5:
        return 'on_crest'
    if yb >= back - 0.5:
        return 'on_back_slope'
    return 'passes_reef'


def is_surfable(r):
    """Stand-up surfable on the reef (ASSUMPTION, RESULTS.md s2.4): breaks on the ramp or crest, xi_b < 2 (not surging /
    collapsing) and vortex ratio >= 1.6 (not beyond 'extreme', Mead 2000 p.121)."""
    if r.get('category') not in WORKS:
        return False
    xi, Y = r.get('xi_b', float('nan')), r.get('vortex_Y', float('nan'))
    return bool(np.isfinite(xi) and np.isfinite(Y) and xi < 2.0 and Y >= 1.6)


def skill_from(Y, xi_b, cat):
    """Interpretive mapping (ASSUMPTION, RESULTS.md s2.4) of breaking intensity to the surfer level it suits."""
    if cat not in WORKS:
        return 'reef not shaping the break'
    if not np.isfinite(Y):
        return 'n/a'
    if xi_b >= 2.0 or Y < 1.6:
        return 'too hollow / collapsing: bodyboard or expert only'
    if xi_b < 0.4:
        return 'beginner-friendly (spilling)'   # Battjes spilling; Mead & Black's fit is for plunging surf waves
    if Y < 1.905:
        return 'expert (extreme, tubing)'
    if Y < 2.505:
        return 'advanced (high to very high)'
    if Y < 3.105:
        return 'intermediate (medium to medium/high)'
    return 'beginner-friendly (gentle plunging / spilling)' if xi_b < 0.4 else 'novice-intermediate (gentle plunging)'


def analyse_case(y, zb, zr, zs, met, H0, T, eta, gamma='mccowan'):
    b = transform(y, zs, H0, T, eta, gamma)
    cat = classify(b['y'], met)
    out = dict(H0=H0, T=T, eta=eta, gamma_mode=gamma, y_break=b['y'], d_break=b['d'], H_break=b['H'], category=cat,
               gamma_used=b.get('gamma'))
    # depth at crest and toe for this tide
    if met.get('reef_on_line'):
        out['d_crest'] = eta - met['crest_z_msl_m']
        out['d_toe'] = eta - met.get('outer_toe_reef_z', met['seaward_toe_reef_z_msl_m'])
        out['d_toe_bed'] = eta - met.get('outer_toe_bed_z', met['seaward_toe_seabed_z_msl_m'])
    if b['i'] is None or not np.isfinite(b['y']) or b.get('shore'):
        return out
    Lb = float(W.wavelength(T, max(b['d'], 0.05)))
    win = max(4.0, Lb / 4)
    tb_c = local_slope(y, zs, b['y'], win)
    tb_s = window_slope(y, zs, b['y'], b['y'] + win)
    tb_l = window_slope(y, zs, b['y'] - win, b['y'])
    L0 = float(W.L0(T))
    for nm, tb in (('c', tb_c), ('s', tb_s), ('l', tb_l)):
        out['tanb_' + nm] = tb
    tb = tb_c if np.isfinite(tb_c) and tb_c > 1e-4 else (tb_s if np.isfinite(tb_s) and tb_s > 1e-4 else float('nan'))
    out['tan_beta'] = tb
    out['window_m'] = win
    out['L_break'] = Lb
    if np.isfinite(tb) and tb > 0:
        xi = tb / math.sqrt(b['H'] / L0)
        Y, X = W.vortex_ratio(tb)
        out.update(xi_b=xi, breaker=W.breaker_type(xi), vortex_Y=Y, slope_X=X, vortex_class=W.vortex_class(Y)[0],
                   vortex_extrapolated=bool(X < 9.2 or X > 40.2))
        out['skill'] = skill_from(Y, xi, cat)
    else:
        out.update(xi_b=float('nan'), breaker='flat/adverse slope', vortex_Y=float('nan'), slope_X=float('nan'),
                   vortex_class=None, skill=skill_from(float('nan'), float('nan'), cat))
    # preparation on the reef: distance from the seaward toe to the break, in local wavelengths; shoaling gain on the reef
    if cat in WORKS:
        prep = met.get('outer_toe_y', met['seaward_toe_y_m']) - b['y']
        out['prep_m'] = prep
        out['prep_in_Lb'] = prep / Lb
        dt = eta - met.get('outer_toe_reef_z', met['seaward_toe_reef_z_msl_m'])
        if dt > 0:
            out['Ks_gain_on_reef'] = float(W.shoaling_coefficient(T, b['d']) / W.shoaling_coefficient(T, dt))
    return out


# ------------------------------------------------------------------------------------------------ tides
def tide_series(A_s, A_n, z0=0.0, days=29.53, dt_min=6.0):
    """Synthetic semidiurnal tide: eta = z0 + A(t) cos(2 pi t / 12.42 h), A between neap and spring over 14.765 d.
    ASSUMPTION (RESULTS.md s2.5)."""
    t = np.arange(0, days * 24, dt_min / 60.0)
    A = (A_s + A_n) / 2 + (A_s - A_n) / 2 * np.cos(2 * math.pi * t / (14.765 * 24))
    return t, z0 + A * np.cos(2 * math.pi * t / 12.42)


def window_fraction(levels, works_mask, series):
    """Fraction of time the water level lies at a level where the reef shapes the break (nearest-level lookup)."""
    idx = np.clip(np.searchsorted(levels, series), 0, len(levels) - 1)
    return float(np.mean(works_mask[idx]))


# ------------------------------------------------------------------------------------------------ main runs
def natural_szw(y, zb, H0, T, eta=0.0, gamma='mccowan'):
    """Natural surf-zone width (no reef): distance from the MSL line to the breaker line on the seabed-only profile."""
    b = transform(y, zb, H0, T, eta, gamma)
    ok = np.where(eta - zb <= 0)[0]
    y_msl = float(y[ok[0]]) if len(ok) else float('nan')
    return b['y'] - y_msl, b, y_msl


def run():
    inp = RI.load()
    RI.dump(inp)
    hyps = json.load(open(os.path.join(HERE, 'results_hypsometry.json')))['reefs']
    reefs_all = {r['slug']: r for r in json.load(open(os.path.join(HERE, '..', 'data', 'reefs.json')))}
    rows, site_rows, peel_rows, tide_rows, size_rows = [], [], [], [], []
    israel_tide = tide_series(RI.ISRAEL['tide_spring_range_m'] / 2, RI.ISRAEL['tide_neap_range_m'] / 2)[1]
    for slug, R in inp.items():
        site = R['site']
        tl = R['tide_levels']
        tide = R['tide']
        series = tide_series(tide['A_spring'], tide['A_neap'], tide.get('z0', 0.0))[1]
        Ts = sorted(set(T_SET + [site['T']] + ([site['T_alt']] if site.get('T_alt') else [])))
        Hs = sorted(set(H_SET + [site['H']]))
        for ln in LINES + [k for k in R['lines'] if k.startswith('layer:')]:
            L = R['lines'].get(ln)
            if not L:
                continue
            is_layer = ln.startswith('layer:')
            y, zb, zr, zs = prof_arrays(L)
            met = prepare_met(L['metrics'], y, zb, zr)
            # ---- full grid: H x T x 3 tides x gamma
            for H0 in Hs:
                for T in (Ts if not is_layer else [site['T']]):
                    for tname, eta in tl.items():
                        for gm in ('mccowan', 'low', 'weggel'):
                            if gm != 'mccowan' and not (ln == 'crest_line' and T == site['T']):
                                continue
                            r = analyse_case(y, zb, zr, zs, met, H0, T, eta, gm)
                            r.update(slug=slug, line=ln, tide=tname)
                            rows.append(r)
            # ---- tide window (crest_line and centreline, McCowan), every H, site T and the T set
            if ln in ('crest_line', 'centreline') or is_layer:
                lev = np.round(np.arange(tide['extreme_lo'] - 0.05, tide['extreme_hi'] + 0.0501, 0.02), 3)
                for H0 in Hs:
                    for T in (sorted(set([site['T'], 8.0, 12.0])) if not is_layer else [site['T']]):
                        res = [analyse_case(y, zb, zr, zs, met, H0, T, float(e)) for e in lev]
                        cats = [r['category'] for r in res]
                        works = np.array([c in WORKS for c in cats])
                        surf = np.array([is_surfable(r) for r in res])
                        crest_only = np.array([c == 'on_crest' for c in cats])
                        before = np.array([c == 'before_reef' for c in cats])
                        # Israeli tide applied to the same geometry (levels around MSL)
                        lev_i = np.round(np.arange(-0.25, 0.2501, 0.01), 3)
                        res_i = [analyse_case(y, zb, zr, zs, met, H0, T, float(e)) for e in lev_i]
                        works_i = np.array([r['category'] in WORKS for r in res_i])
                        surf_i = np.array([is_surfable(r) for r in res_i])
                        wl = lev[works]
                        dc = (0.0 - met['crest_z_msl_m']) if met.get('reef_on_line') else float('nan')
                        tide_rows.append(dict(
                            slug=slug, line=ln, H0=H0, T=T, crest_depth_msl=dc,
                            spring_range=round(2 * tide['A_spring'], 3), neap_range=round(2 * tide['A_neap'], 3),
                            works_eta_min=float(wl.min()) if len(wl) else None, works_eta_max=float(wl.max()) if len(wl) else None,
                            works_band_m=float(wl.max() - wl.min() + 0.02) if len(wl) else 0.0,
                            frac_time_works=window_fraction(lev, works, series),
                            frac_time_on_crest=window_fraction(lev, crest_only, series),
                            frac_time_breaks_before_reef=window_fraction(lev, before, series),
                            frac_time_works_israeli_tide=window_fraction(lev_i, works_i, israel_tide),
                            frac_time_works_no_tide=float(works_i[np.argmin(np.abs(lev_i))]),
                            frac_time_surfable=window_fraction(lev, surf, series),
                            frac_time_surfable_israeli_tide=window_fraction(lev_i, surf_i, israel_tide),
                            surfable_no_tide=float(surf_i[np.argmin(np.abs(lev_i))]),
                            H_break_threshold_range_m=0.78 * 2 * tide['A_spring'],
                            daylight_hours_works=12.0 * window_fraction(lev, works, series),
                            daylight_hours_works_israeli_tide=12.0 * window_fraction(lev_i, works_i, israel_tide),
                            Hmax_crest_low=0.78 * max(0.0, tl['low'] - met['crest_z_msl_m']) if met.get('reef_on_line') else None,
                            Hmax_crest_high=0.78 * max(0.0, tl['high'] - met['crest_z_msl_m']) if met.get('reef_on_line') else None,
                            Hmax_crest_israel_low=0.78 * max(0.0, -0.2 - met['crest_z_msl_m']) if met.get('reef_on_line') else None,
                            Hmax_crest_israel_high=0.78 * max(0.0, 0.2 - met['crest_z_msl_m']) if met.get('reef_on_line') else None,
                        ))
        # ---- site summary (primary line, site H and T, three tides)
        L = R['lines']['crest_line']
        y, zb, zr, zs = prof_arrays(L)
        met = prepare_met(L['metrics'], y, zb, zr)
        for tname, eta in tl.items():
            r = analyse_case(y, zb, zr, zs, met, site['H'], site['T'], eta)
            r.update(slug=slug, tide=tname, H_src=site['H_src'], T_src=site['T_src'])
            site_rows.append(r)
        # ---- peel angle
        if site.get('phi0'):
            for k, phi in enumerate(site['phi0']):
                for H0 in Hs:
                    for T in sorted(set([site['T'], 8.0, 12.0])):
                        b = transform(y, zs, H0, T, 0.0)
                        if not np.isfinite(b['y']) or b.get('shore'):
                            continue
                        h0 = max(0.5, 0.0 - met['outer_toe_bed_z'])
                        hb = max(0.1, b['d'])
                        a_b = W.peel_angle_snell(phi, T, h0, hb)
                        rating, hok = W.hutt_min_rating(a_b, b['H'])
                        peel_rows.append(dict(slug=slug, arm=k + 1, phi0_deg=phi, phi0_src=site['phi0_src'], H0=H0, T=T,
                                              h_toe=h0, h_break=hb, H_break=b['H'], alpha_break_deg=a_b,
                                              alpha_no_refraction_deg=phi, hutt_rating=rating, Hb_in_rating_range=hok,
                                              hutt_rating_no_refraction=W.hutt_min_rating(phi)[0],
                                              peel_rate_ms=W.peel_rate(T, hb, a_b),
                                              category=classify(b['y'], met)))
                if site.get('phi0_alt'):
                    phi = site['phi0_alt'][k]
                    b = transform(y, zs, site['H'], site['T'], 0.0)
                    if np.isfinite(b['y']):
                        a_b = W.peel_angle_snell(phi, site['T'], max(0.5, -met['outer_toe_bed_z']), max(0.1, b['d']))
                        peel_rows.append(dict(slug=slug, arm=k + 1, phi0_deg=phi, phi0_src='ALT: ' + site['phi0_src'], H0=site['H'],
                                              T=site['T'], h_toe=max(0.5, -met['outer_toe_bed_z']), h_break=b['d'],
                                              H_break=b['H'], alpha_break_deg=a_b, alpha_no_refraction_deg=phi,
                                              hutt_rating=W.hutt_min_rating(a_b, b['H'])[0], Hb_in_rating_range=W.hutt_min_rating(a_b, b['H'])[1],
                                              hutt_rating_no_refraction=W.hutt_min_rating(phi)[0],
                                              peel_rate_ms=W.peel_rate(site['T'], max(0.1, b['d']), a_b), category=classify(b['y'], met)))
        # ---- size vs outcome
        hy = hyps.get(slug, {})
        Lt = float(W.wavelength(site['T'], max(0.5, -met['outer_toe_bed_z'])))
        szw, bnat, y_msl = natural_szw(y, zb, site['H'], site['T'])
        szw_storm, _, _ = natural_szw(y, zb, 2.0 * site['H'], site['T'])
        g = R['glob']
        rel = {d['level_m']: d for d in hy.get('relative', [])}
        rj = R['reefs_json']
        size_rows.append(dict(
            slug=slug, outcome=(rj.get('surf_outcome') or {}).get('value'),
            volume_stated_m3=(rj.get('volume_m3') or {}).get('value'), volume_model_m3=hy.get('volume_total_m3'),
            footprint_m2=hy.get('footprint_area_m2'), area_within_0p5m_of_crest_m2=rel.get(-0.5, {}).get('area_m2'),
            area_within_1m_of_crest_m2=rel.get(-1.0, {}).get('area_m2'), volume_top_1m_m3=rel.get(-1.0, {}).get('volume_above_m3'),
            alongshore_len_crest_minus0p5_m=(g.get('alongshore_length_z_ge_crest_minus0p5') or {}).get('union_m'),
            alongshore_span_m=g.get('footprint_alongshore_span_m'), crossshore_span_m=g.get('footprint_cross_shore_span_m'),
            crest_depth_msl=-met['crest_z_msl_m'], relief_m=met.get('crest_height_above_seabed_m'),
            ramp_length_m=met.get('ramp_length_m'), mean_seaward_slope=(met.get('mean_seaward_slope') or {}).get('tan'),
            depth_gap_m=met.get('crest_to_toe_seabed_drop_m'),
            T_site=site['T'], H_site=site['H'], L_at_toe_m=Lt,
            crossshore_over_L=(g.get('footprint_cross_shore_span_m') or float('nan')) / Lt,
            alongshore_over_L=(g.get('footprint_alongshore_span_m') or float('nan')) / Lt,
            szw_natural_m=szw, szw_natural_2H_m=szw_storm, y_msl_line=y_msl,
            crest_offshore_from_msl_m=met.get('crest_distance_from_msl_line_m'),
            Hb_needed_to_break_on_crest_msl=0.78 * (-met['crest_z_msl_m']),
            H0_needed_to_break_on_crest_msl=None))
        # deep-water height needed to break at (or before) the crest at MSL (bisection on H0)
        lo_, hi_ = 0.05, 6.0
        for _ in range(30):
            mid = (lo_ + hi_) / 2
            c = classify(transform(y, zs, mid, site['T'], 0.0)['y'], met)
            if c in ('on_crest', 'on_ramp', 'before_reef'):
                hi_ = mid
            else:
                lo_ = mid
        size_rows[-1]['H0_needed_to_break_on_crest_msl'] = round(hi_, 3)
        # largest H0 that still breaks on the reef (not before it) at MSL
        lo_, hi_ = 0.05, 8.0
        for _ in range(30):
            mid = (lo_ + hi_) / 2
            c = classify(transform(y, zs, mid, site['T'], 0.0)['y'], met)
            if c == 'before_reef':
                hi_ = mid
            else:
                lo_ = mid
        size_rows[-1]['H0_max_before_breaking_seaward_of_reef_msl'] = round(lo_, 3)
    return rows, site_rows, peel_rows, tide_rows, size_rows, inp


def write_csv(path, rows):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})


def main():
    rows, site_rows, peel_rows, tide_rows, size_rows, inp = run()
    write_csv(os.path.join(HERE, 'results_breaking.csv'), rows)
    write_csv(os.path.join(HERE, 'results_surf_site.csv'), site_rows)
    write_csv(os.path.join(HERE, 'results_peel.csv'), peel_rows)
    write_csv(os.path.join(HERE, 'results_tide_window.csv'), tide_rows)
    write_csv(os.path.join(HERE, 'results_size.csv'), size_rows)
    meta = dict(script='08_paper/analysis/surf_analysis.py', status='DERIVED (model results; see RESULTS.md for method, inputs and limits)',
                H_set=H_SET, T_set=T_SET, gammas=dict(GAMMAS, weggel='Weggel 1972 slope-dependent'), lines=LINES,
                site_inputs={s: d['site'] for s, d in inp.items()}, tides={s: dict(planes=d['planes'], model=d['tide'], levels=d['tide_levels']) for s, d in inp.items()},
                israel=RI.ISRAEL)
    with open(os.path.join(HERE, 'results_surf.json'), 'w') as f:
        json.dump(dict(meta=meta, site=site_rows, peel=peel_rows, tide_window=tide_rows, size=size_rows), f, indent=1, default=float)
    print('rows', len(rows), 'site', len(site_rows), 'peel', len(peel_rows), 'tide', len(tide_rows), 'size', len(size_rows))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""coastal_analysis.py - coastal-protection screens per reef (RESULTS.md part 6, insight b).

Run:    python3 08_paper/analysis/coastal_analysis.py   (after surf_analysis.py)
Reads:  reef_inputs.py, results_size.csv (natural surf-zone width), seabed_sediment_results.json (seabed agent; optional)
Writes: results_transmission.csv, results_shoreline.csv, results_coastal.json

1. Wave transmission over the crest (2-D, per metre of crest): d'Angremond et al. (1996) for B/Hi < 10, Briganti et al.
   (2003) for B/Hi >= 10 (wavelib.kt_low_crested). Hi = wave at the outer toe (deep-water H0 shoaled with linear theory;
   if the wave breaks before the toe, Hi = 0.78 x toe depth). Rc = crest level - water level (< 0 submerged).
   B = cross-shore width of the crest-line profile where the reef is within 0.5 m of its line maximum (DERIVED; the 0.10 m
   'crest zone' of the profile JSON is too strict for rough surfaces). tan(alpha) = mean seaward slope of the crest line.
   Permeable form for rock reefs, impermeable (0.80) for geotextile reefs. 2-D: diffraction around a short reef is ignored,
   so Kt is a lower bound of the wave height in the lee (the real lee is less sheltered).
2. Shoreline response predictors: Black & Andrews (2001) B/S with B = alongshore footprint span, S = crest distance from
   the MSL line (centreline; Cables: from the derived true shoreline); Ranasinghe et al. (2006) Sa/SZW with Sa = crest and
   outer-toe distances and SZW = natural surf-zone width (results_size.csv) for the site H and 2 x site H.
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
import surf_analysis as SA  # noqa: E402

ROCK = {'cables-reef-wa', 'palm-beach-gold-coast', 'southern-ocean-surf-reef-albany', 'borth-coastal-defence-reef'}


def crest_width(y, zr, tol=0.5):
    ok = np.isfinite(zr)
    if not ok.any():
        return float('nan')
    zmax = np.nanmax(zr)
    sel = ok & (zr >= zmax - tol)
    return float(y[sel].max() - y[sel].min() + 1.0)


def run():
    inp = RI.load()
    size = {r['slug']: r for r in csv.DictReader(open(os.path.join(HERE, 'results_size.csv')))}
    try:
        seabed = json.load(open(os.path.join(HERE, 'seabed_sediment_results.json')))
        obs = {}
        for row in seabed.get('summary_table', []):
            obs.setdefault(row['reef'], []).append('%s: %s' % (row.get('test'), row.get('signal')))
    except Exception:
        obs = {}
    trows, srows = [], []
    for slug, R in inp.items():
        site = R['site']
        L = R['lines']['crest_line']
        y, zb, zr, zs = SA.prof_arrays(L)
        met = SA.prepare_met(L['metrics'], y, zb, zr)
        zc = met['crest_z_msl_m']
        B = crest_width(y, zr)
        tana = (met.get('mean_seaward_slope') or {}).get('tan') or float('nan')
        perm = slug in ROCK
        d_toe_bed_msl = -met['outer_toe_bed_z']
        for T in sorted(set([site['T'], 8.0, 12.0])):
            for H0 in sorted(set(SA.H_SET + [site['H']])):
                for tname, eta in R['tide_levels'].items():
                    dt = eta - met['outer_toe_bed_z']
                    Hi = float(H0 * W.shoaling_coefficient(T, dt))
                    broken = Hi >= 0.78 * dt
                    Hi = min(Hi, 0.78 * dt)
                    Rc = zc - eta
                    kt, xi, form = W.kt_low_crested(Rc, Hi, B, tana, T, permeable=perm)
                    trows.append(dict(slug=slug, T=T, H0=H0, tide=tname, eta=eta, Hi_toe=Hi, broken_before_toe=broken,
                                      Rc=Rc, Rc_over_Hi=Rc / Hi, B_crest_m=B, B_over_Hi=B / Hi, tan_alpha=tana, xi=xi,
                                      permeable=perm, formula=form, Kt=kt, H_lee=kt * Hi, energy_reduction=1 - kt ** 2))
        # shoreline predictors
        cl = met
        y_msl = float(SA.natural_szw(y, zb, 1.0, site['T'])[2])
        g = R['glob'] or {}
        cen_y = (g.get('footprint_centroid_xy_m') or [None, None])[1]
        if slug == 'cables-reef-wa':   # model frame origin is not the shoreline: use the derived true-shoreline distances
            ts = R['lines']['crest_line'].get('metrics', {})
            S_crest = ts.get('crest_distance_from_true_shoreline_m')
            shift = (ts.get('crest_y_m') or 0) - (S_crest or 0)
            S_cen = cen_y - shift if cen_y is not None else None
            S_toe = met['outer_toe_y'] - shift
        else:
            S_crest = met.get('crest_distance_from_msl_line_m')
            S_cen = cen_y - y_msl if cen_y is not None and np.isfinite(y_msl) else None
            S_toe = met['outer_toe_y'] - y_msl if np.isfinite(y_msl) else None
        S = S_cen if S_cen else S_crest
        Bl = g.get('footprint_alongshore_span_m')
        ba = W.black_andrews(Bl, S)
        sz = size.get(slug, {})
        szw1 = float(sz.get('szw_natural_m') or 'nan')
        szw2 = float(sz.get('szw_natural_2H_m') or 'nan')
        szw_note = 'natural profile (results_size.csv)'
        if not np.isfinite(szw1):   # Cables: the model profile starts at -4.8 m; ASSUMPTION nearshore slope 1:25
            tb = 1 / 25.0
            hb1 = float(W.shoaling_coefficient(site['T'], 2.0)) * site['H'] / 0.78
            hb2 = float(W.shoaling_coefficient(site['T'], 3.0)) * 2 * site['H'] / 0.78
            szw1, szw2 = hb1 / tb, hb2 / tb
            szw_note = 'ASSUMPTION: profile does not reach the shore; SZW = h_b / tan(beta) with tan(beta) = 1/25 (mid of the 1:15-1:40 contour-spacing slopes noted by the seabed agent, seabed_sediment_results.json Cables T3 caveat)'
        r1, m1 = W.ranasinghe_mode(S, szw1)
        r2, m2 = W.ranasinghe_mode(S, szw2)
        r3, m3 = W.ranasinghe_mode(S_toe, szw1) if S_toe else (float('nan'), None)
        # deep-water H0 at which the natural SZW equals S/2 (Ranasinghe accretion peak) and S (erosion threshold)
        hpk = {}
        if slug != 'cables-reef-wa':
            for name, target in (('H0_at_Sa_over_SZW_2', S / 2), ('H0_at_Sa_over_SZW_1', S)):
                lo_, hi_ = 0.1, 8.0
                if SA.natural_szw(y, zb, hi_, site['T'])[0] < target:
                    hpk[name] = '>8'
                    continue
                for _ in range(30):
                    mid = (lo_ + hi_) / 2
                    if SA.natural_szw(y, zb, mid, site['T'])[0] < target:
                        lo_ = mid
                    else:
                        hi_ = mid
                hpk[name] = round(hi_, 2)
        srows.append(dict(slug=slug, alongshore_B_m=Bl, S_centroid_m=S_cen, S_crest_m=S_crest, S_toe_m=S_toe, S_used='centroid' if S_cen else 'crest',
                          B_over_S=ba['B_over_S'], black_andrews_mode=ba['mode'], salient_Yoff_pred_m=ba['Y_off_m'],
                          salient_Dtot_pred_m=ba['D_tot_m'], X_off_pred_m=ba['X_off_m'],
                          SZW_siteH_m=szw1, SZW_2H_m=szw2, SZW_note=szw_note, H_site=site['H'], T_site=site['T'],
                          Sa_over_SZW_siteH=r1, ranasinghe_siteH=m1, Sa_over_SZW_2H=r2, ranasinghe_2H=m2,
                          Sa_toe_over_SZW_siteH=r3, ranasinghe_toe_siteH=m3, **hpk,
                          observed_reefs_json=((R['reefs_json'].get('sediment_shoreline_outcome') or {}).get('value')),
                          observed_seabed_agent=' | '.join(obs.get(slug, [])) or None))
    return trows, srows


def main():
    trows, srows = run()
    SA.write_csv(os.path.join(HERE, 'results_transmission.csv'), trows)
    SA.write_csv(os.path.join(HERE, 'results_shoreline.csv'), srows)
    with open(os.path.join(HERE, 'results_coastal.json'), 'w') as f:
        json.dump(dict(meta=dict(script='08_paper/analysis/coastal_analysis.py', status='DERIVED; formulas in wavelib.py; see RESULTS.md part 6'),
                       transmission=trows, shoreline=srows), f, indent=1, default=float)
    print('transmission rows', len(trows), 'shoreline rows', len(srows))


if __name__ == '__main__':
    main()

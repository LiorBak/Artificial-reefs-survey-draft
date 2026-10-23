#!/usr/bin/env python3
"""stability_analysis.py - material stability and wave loads (RESULTS.md part 7, insights c and e).

Run:    python3 08_paper/analysis/stability_analysis.py
Writes: results_stability_fk.csv (force / sliding-index ESTIMATE per tube, depth, H), results_fk_calibration.json,
        results_stability_tubes.csv (van Steeg criterion vs depth-limited waves), results_stability_rock.csv (Hudson),
        results_stability.json (all + metadata)

A. ESTIMATE of the Bar & Drimer (2023) sliding index (NOT the BELWF model, whose code is not released): linear (Airy)
   incident-wave pressure integrated over a rigid tube section on the bed (Froude-Krylov; no diffraction, no added mass,
   no nonlinearity), BD23 Eqs. 3-5: SI = Fy / (W' - Fz), SIc = Fy / (W' - Fz - Fc), Fc = L_contact (P_UW + P_DW)/2,
   W' = (rho_fill - rho_w) g A. Section (2026-10-20, Lior's review of Fig. 11): the partly filled Bezuijen & Vastenburg shape
   described by BD23 Sec. 2.2 (flat base, quarter-circle sides, semi-elliptical top, continuous curvature; construction in
   bv_shape) for a fixed fabric circumference C (pi x reported diameter, or fitted to the reported filled B x D), at filling
   ratios FA 0.6, 0.7, 0.8 (default, BD23 validation) and 1.0 (full circle, reference). L_contact = flat base length.
   Pressure integrated over the wetted contour (base excluded = sealed base). Evaluated over one period; the critical value
   is the maximum |SI|. Calibrated against BD23 read-offs: validation case (R 3.425 m, FA 0.8, widened by a flat middle
   section to 12 m as BD23 p.4 describes for adjacent tubes; h = 5 m, T = 7 s, H = 0.3-1.6 m; Fy, Fz, SI read from Figs. 5-6
   via 08_paper/notes/bar_drimer_2023_coverage.md s6.4) and design case (11 x 2.2 m, C from the 2.2 m height at FA 0.8,
   h = 4 m, T = 9 s, H = 2.86 m; SI ~0.17, SIc ~0.31 from Fig. 11). U is an index of the cyclic vertical load relative to
   the submerged weight (a tearing driver), not a lift-off prediction. Writes also results_stability_fa_summary.csv.
B. van Steeg et al. (2011) tube criterion chi Hs / (Delta sqrt(B D) (f cos a + sin a)) <= 0.65, chi = 1, f = 0.5
   (ASSUMPTION), compared with the depth-limited significant wave Hs = 0.55 h (ASSUMPTION gamma_s) at the tube base.
C. Hudson (1959) rock stability, K_D = 2.0 (breaking waves, 2 layers, trunk, SPM 1984 via Verhagen 2012 slide 6).
"""
import csv
import json
import math
import os
import sys

import numpy as np
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import wavelib as W  # noqa: E402
import reef_inputs as RI  # noqa: E402
import surf_analysis as SA  # noqa: E402

RHO_FILL_BD23 = 2082.0     # [BD23] p.6 wet saturated sand (low-confidence source in BD23)
F_FRICTION = 0.5           # ASSUMPTION tube-on-sand friction (Corvaro et al. 2022 use 0.48 bag-on-bag)
GAMMA_S = 0.55             # ASSUMPTION depth-limited significant wave / depth


FA_LIST = (0.6, 0.7, 0.8, 1.0)   # filling ratios run; BD23 practical range 0.60-0.85 (p.4), 1.0 = full circle (reference only)
FA_DEFAULT = 0.8                 # BD23 validation value (p.6); design FA not stated in BD23


def _half_ellipse_perimeter(a, c):
    """Ramanujan II perimeter of a full ellipse, halved (error < 1e-5 for c/a >= 0.1)."""
    q = ((a - c) / (a + c)) ** 2
    return math.pi * (a + c) * (1 + 3 * q / (10 + math.sqrt(4 - 3 * q))) / 2


def bv_shape(C, FA):
    """Bezuijen & Vastenburg cross-section as described in words by [BD23] Sec. 2.2 p.4 (no formula given there).
    Construction (ASSUMPTION, this review): flat base of length b; each side a quarter circle of radius r (centre r above the
    base, at the base ends); the top a semi-ellipse with semi-axes a = b/2 + r (horizontal) and c (vertical), centred r above
    the base. Curvature continuity at the arc/ellipse join (radius of curvature of the ellipse there c^2/a = r) gives r = c^2/a.
    Closed by the perimeter b + pi r + half-ellipse = C (fabric circumference) and the area = FA pi R^2, R = C / (2 pi)
    (FA read as the area ratio to a full circle). FA = 1 gives the circle of radius R. Check against BD23 p.6: R 3.425 m,
    FA 0.8 gives a height of 4.01 m against the printed 3.8 m (+6 %), and a width of 8.77 m."""
    R = C / (2 * math.pi)
    if FA >= 0.9999:
        return dict(C=C, FA=1.0, R=R, b=0.0, r=R, a=R, c=R, B=2 * R, D=2 * R, A=math.pi * R * R)

    def geom(q):                        # q = c / a
        a = C / (2 * (1 - q * q) + math.pi * q * q + _half_ellipse_perimeter(1.0, q))
        r, c = q * q * a, q * a
        b = 2 * (a - r)
        return dict(C=C, FA=FA, R=R, b=b, r=r, a=a, c=c, B=2 * a, D=r + c, A=b * r + math.pi * r * r / 2 + math.pi * a * c / 2)
    q = brentq(lambda q: geom(q)['A'] / (math.pi * R * R) - FA, 1e-4, 1 - 1e-9)
    return geom(q)


def bv_contour(s, ext=0.0, n=120):
    """Wetted contour, counter-clockwise from the landward (+x) base end over the top to the seaward base end (the flat
    base itself is excluded) of shape s, with a flat middle section of length ext inserted ([BD23] p.4: adjacent tubes are
    represented by adding a horizontal section in the middle). Returns x, z (z above the bed), base length."""
    b, r, a, c, e = s['b'], s['r'], s['a'], s['c'], ext
    xr = b / 2 + e / 2
    t1 = np.linspace(-math.pi / 2, 0, n // 4 + 1)
    t2 = np.linspace(0, math.pi / 2, n // 2 + 1)
    parts = [(xr + r * np.cos(t1), r + r * np.sin(t1)),                  # landward side arc, up
             (e / 2 + a * np.cos(t2), r + c * np.sin(t2))]                # landward upper quarter-ellipse
    if e > 0:
        parts.append((np.linspace(e / 2, -e / 2, 9), np.full(9, r + c)))  # flat top of the middle section
    parts += [(-e / 2 - a * np.cos(t2[::-1]), r + c * np.sin(t2[::-1])),  # seaward upper quarter-ellipse
              (-xr - r * np.cos(t1[::-1]), r + r * np.sin(t1[::-1]))]     # seaward side arc, down
    x = np.concatenate([p[0] for p in parts]); z = np.concatenate([p[1] for p in parts])
    keep = np.r_[True, np.hypot(np.diff(x), np.diff(z)) > 1e-9]
    return x[keep], z[keep], b + e


def section_for(t, FA):
    """Shape, contour and areas for tube entry t at filling ratio FA (structures with a target width get a middle section)."""
    s = bv_shape(t['C'], FA)
    ext = max(0.0, t.get('width', 0.0) - s['B']) if t.get('width') else 0.0
    x, z, Lc = bv_contour(s, ext)
    return dict(shape=s, x=x, z=z, L_contact=Lc, B=s['B'] + ext, D=s['D'], A=s['A'] + ext * s['D'], ext=ext)


def fk_forces(sec, h, H, T, rho_fill=RHO_FILL_BD23, nph=96, Wsub=None):
    """Linear Froude-Krylov loads per metre on a bottom-mounted rigid section (bed at z = -h). Returns maxima over phase.
    F = -sum p n dS over the wetted contour (base excluded = sealed base); the BD23 Eq. 4 contact term
    Fc = L_contact (P_UW + P_DW)/2 with L_contact = the flat base length (zero for FA = 1)."""
    k = float(W.wavenumber(T, h))
    x, z = sec['x'], sec['z']
    xm, zm = (x[1:] + x[:-1]) / 2, (z[1:] + z[:-1]) / 2
    dx, dz = np.diff(x), np.diff(z)
    A = sec['A']
    Wp = (rho_fill - W.RHO_W) * W.G * A if Wsub is None else Wsub
    amp = W.RHO_W * W.G * H / 2 / math.cosh(k * h)
    xe = sec['L_contact'] / 2
    ph = np.linspace(0, 2 * math.pi, nph, endpoint=False)
    Fy, Fz, Fc = [], [], []
    for w in ph:
        pr = amp * np.cosh(k * zm) * np.cos(k * xm - w)
        Fy.append(float(-np.sum(pr * dz)))             # + onshore (+x, direction of wave travel)
        Fz.append(float(np.sum(pr * dx)))              # + uplift
        pb = amp * np.cos(np.array([-k * xe - w, k * xe - w]))   # dynamic pressure on the bed at the contact ends
        Fc.append(sec['L_contact'] * float(pb.mean()))  # BD23 Eq. 4, + = uplift
    Fy, Fz, Fc = np.array(Fy), np.array(Fz), np.array(Fc)
    SI = Fy / (Wp - Fz)
    SIc = Fy / (Wp - Fz - Fc)
    i = int(np.argmax(np.abs(SI)))
    j = int(np.argmax(np.abs(SIc)))
    # uplift_fraction: sealed base (no dynamic pressure under the tube; upper bound). uplift_fraction_contact: BD23 contact
    # term added (dynamic pressure reaches the base; lower bound). U is an index of the cyclic vertical load relative to W'.
    return dict(k=k, kh=k * h, area=A, Wsub_kN=Wp / 1e3, Fy_max_kN=float(np.abs(Fy).max()) / 1e3, Fz_uplift_max_kN=float(Fz.max()) / 1e3,
                Fz_down_max_kN=float(-Fz.min()) / 1e3, Fz_range_kN=float(Fz.max() - Fz.min()) / 1e3, SI_max=float(abs(SI[i])),
                SI_phase_deg=math.degrees(ph[i]), SIc_max=float(abs(SIc[j])), uplift_fraction=float(Fz.max()) / Wp,
                uplift_fraction_contact=float((Fz + Fc).max()) / Wp, cycles_per_day=86400.0 / T)


def C_from_filled(B, D):
    """Circumference of the B&V section whose filled width/height equal the reported B x D (fits FA and C). Returns C, FA."""
    f = lambda FA: bv_shape(1.0, FA)['B'] / bv_shape(1.0, FA)['D'] - B / D
    FA = 1.0 if B / D <= 1.0 + 1e-6 else brentq(f, 0.2, 0.99999)
    return B / bv_shape(1.0, FA)['B'], FA


def C_from_height(D, FA=FA_DEFAULT):
    return D / bv_shape(1.0, FA)['D']


BD23_VAL = dict(id='BD23 validation pair', C=2 * math.pi * 3.425, width=12.0, src='[BD23] p.6: R = 3.425 m, FA 0.8, 12 m wide, 3.8 m high')
BD23_DES = dict(id='BD23 design tube', C=C_from_height(2.2), width=11.0, src='[BD23] p.10 (11 m wide, 2.2 m high); C from the 2.2 m height at FA 0.8 (ASSUMPTION, design FA not stated), middle section to 11 m')


def calibrate():
    """Compare the estimate (B&V section, FA 0.8) with the BD23 read-offs; returns factors used to scale the estimate."""
    val = [(0.3, 7, 13, 0.016), (1.0, 28, 48, 0.066), (1.6, 44.5, 64, 0.106)]   # H, Fy, Fz, SI (by eye, +-10 %)
    W_sub_val = 467e3   # N/m: (Fg - Fb) DERIVED from the read-offs (450-485 kN) in bar_drimer_2023_coverage.md s6.4
    sv = section_for(BD23_VAL, FA_DEFAULT)
    rows = []
    for H, Fy_b, Fz_b, SI_b in val:
        r = fk_forces(sv, 5.0, H, 7.0, Wsub=W_sub_val)
        rows.append(dict(case='BD23 validation', H=H, Fy_BELWF_kN=Fy_b, Fy_est_kN=r['Fy_max_kN'], Fz_BELWF_kN=Fz_b,
                         Fz_est_kN=r['Fz_uplift_max_kN'], SI_BELWF=SI_b, SI_est=r['SI_max'],
                         ratio_Fy=Fy_b / r['Fy_max_kN'], ratio_Fz=Fz_b / r['Fz_uplift_max_kN'], ratio_SI=SI_b / r['SI_max'],
                         geom_height=sv['D'], geom_Wsub_kN=(RHO_FILL_BD23 - W.RHO_W) * W.G * sv['A'] / 1e3))
    sd = section_for(BD23_DES, FA_DEFAULT)
    d = fk_forces(sd, 4.0, 2.86, 9.0)
    rows.append(dict(case='BD23 design (near breaking, H/h = 0.72)', H=2.86, SI_BELWF=0.17, SI_est=d['SI_max'], SIc_BELWF=0.31,
                     SIc_est=d['SIc_max'], ratio_SI=0.17 / d['SI_max'], ratio_SIc=0.31 / d['SIc_max'], Wsub_est_kN=d['Wsub_kN'],
                     uplift_fraction_est=d['uplift_fraction'], geom_R=sd['shape']['R'], geom_middle_section=sd['ext']))
    lin = float(np.mean([r['ratio_SI'] for r in rows[:3]]))
    nl = rows[3]['ratio_SI']
    return rows, dict(linear_range_SI_factor=lin, near_breaking_SI_factor=nl, near_breaking_SIc_factor=rows[3]['ratio_SIc'])


def _tube(id_, src, Dth=None, BD=None):
    if Dth is not None:
        return dict(id=id_, C=math.pi * Dth, C_rule='C = pi x theoretical diameter %.2g m' % Dth, src=src)
    C, FA = C_from_filled(*BD)
    return dict(id=id_, C=C, C_rule='C fitted to the reported filled section %.3g x %.3g m (fit FA %.2f)' % (BD[0], BD[1], FA), src=src)


# Tubes and containers: circumference C (m) from the reported sizes. Sources in 'src'.
TUBES = [
    dict(BD23_DES, C_rule='C from height 2.2 m at FA 0.8; middle section to 11 m'),
    _tube('Narrowneck container (small)', 'reefs.json material: 20 m long, 3-4.5 m diameter (Blacka 2013 A.2.5 p.97)', Dth=3.0),
    _tube('Narrowneck container (large)', 'as above, D_th = 4.5 m', Dth=4.5),
    _tube('Mount Maunganui container (small)', 'reefs.json material: filled 30 x 1.5 x 1.0 m (Blacka 2013 A.3.3 p.102)', BD=(1.5, 1.0)),
    _tube('Mount Maunganui container (large)', 'reefs.json material: filled 50 x 7.2 x 3.2 m (Blacka 2013 A.3.3 p.102)', BD=(7.2, 3.2)),
    _tube("Pratte's bag", 'reefs.json material: 3.0 x 2.1 x 1.2 m bags (Blacka 2013 A.11.2 p.115); a short bag treated as a 2-D section', BD=(2.1, 1.2)),
    _tube('Boscombe T4 container', 'reefs.json material: ~4 m diameter, 65-70 m long, 746.7 m3 (Rendle 2016 Table 5.3 via reefs.json)', Dth=4.0),
    _tube('Israeli geotube (D_th 5 m)', 'State Comptroller 2024 PDF p.9 generic definition: tube up to 5 m diameter, 30 m long (via 08_paper/notes/israel_geotubes_netanya.md s4); Ashkelon sizes not stated', Dth=5.0),
    _tube('Israeli geotube (D_th 3 m)', 'ASSUMPTION smaller tube for comparison', Dth=3.0),
]
ISRAELI = ('Israeli geotube (D_th 5 m)', 'Israeli geotube (D_th 3 m)')


def state_of(U, si, sic):
    """U = peak vertical wave load / submerged weight (linear estimate): an index of the cyclic vertical load on the fabric,
    not a lift-off prediction (no Israeli tube is known to have lifted; they tore). SI is singular as U -> 1."""
    if U >= 1.0:
        return 'U >= 1 (uplift load >= submerged weight)'
    if U >= 0.8:
        return 'high cyclic load (0.8 <= U < 1)'
    if max(si, sic) > F_FRICTION:
        return 'sliding (SI > 0.5)'
    return 'stable (SI <= 0.5, U < 0.8)'


def _cal(calib, nb):
    return ((calib['near_breaking_SI_factor'], calib['near_breaking_SIc_factor']) if nb else
            (calib['linear_range_SI_factor'], calib['linear_range_SI_factor']))


def tube_runs(calib):
    rows = []
    for t in TUBES:
        for FA in FA_LIST:
            sec = section_for(t, FA)
            for h in (2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0):        # depth at the tube base (m)
                if h <= sec['D'] + 0.3:
                    continue
                for T in (6.0, 9.0, 12.0):
                    Hlim = 0.78 * h
                    for H in sorted(set([0.5, 1.0, 1.5, 2.0, 3.0, 4.0, round(Hlim, 2)])):
                        if H > Hlim + 1e-9:
                            continue
                        r = fk_forces(sec, h, H, T)
                        nb = H / h >= 0.6
                        fac, facc = _cal(calib, nb)
                        rows.append(dict(tube=t['id'], FA=FA, C=t['C'], B=round(sec['B'], 3), D=round(sec['D'], 3), L_contact=sec['L_contact'],
                                         h_base=h, d_over_crest=h - sec['D'], T=T, H=H, H_over_h=H / h,
                                         at_break=bool(abs(H - Hlim) < 1e-6), **{k: v for k, v in r.items() if k not in ('k',)},
                                         SI_calibrated=r['SI_max'] * fac, SIc_calibrated=r['SIc_max'] * facc,
                                         calibration='near-breaking (H/h >= 0.6): BD23 design factor' if nb else 'linear range: BD23 validation factor',
                                         state=state_of(r['uplift_fraction'], r['SI_max'] * fac, r['SIc_max'] * facc),
                                         state_contact=state_of(r['uplift_fraction_contact'], r['SIc_max'] * facc, r['SIc_max'] * facc)))
    return rows


def u1_depth(hs, us):
    """Base depth where U first reaches 1 (linear interpolation); None if never, or the shallowest depth if already >= 1."""
    hs, us = np.asarray(hs, float), np.asarray(us, float)
    if us[0] >= 1:
        return float(hs[0])
    for i in range(1, len(hs)):
        if us[i] >= 1:
            return float(hs[i - 1] + (1 - us[i - 1]) * (hs[i] - hs[i - 1]) / (us[i] - us[i - 1]))
    return None


def fa_summary(fk, isr):
    """Per tube and FA: section, U at h = 4, 5, 6 m under depth-limited breakers, depth where U = 1, SIc range; Israeli storms."""
    import pandas as pd
    g = pd.DataFrame(fk)
    g = g[g.at_break].groupby(['tube', 'FA', 'B', 'D', 'h_base'])[['uplift_fraction', 'uplift_fraction_contact', 'SIc_calibrated', 'SI_calibrated']].max().reset_index()
    rows = []
    for (tube, FA, B, D), d in g.groupby(['tube', 'FA', 'B', 'D']):
        d = d.sort_values('h_base')
        Uat = {h: float(d[d.h_base == h].uplift_fraction.iloc[0]) if (d.h_base == h).any() else None for h in (4.0, 5.0, 6.0)}
        rows.append(dict(case='depth-limited breakers (max over T 6, 9, 12 s)', tube=tube, FA=FA, B=B, D=D, U_h4=Uat[4.0], U_h5=Uat[5.0],
                         U_h6=Uat[6.0], h_U1=u1_depth(d.h_base, d.uplift_fraction), Uc_max=float(d.uplift_fraction_contact.max()),
                         SIc_min=float(d.SIc_calibrated.min()), SIc_max=float(d.SIc_calibrated.max())))
    s = pd.DataFrame(isr)
    for (tube, FA, Hs), d in s.groupby(['tube', 'FA', 'Hs_storm']):
        d = d.sort_values('h_base')
        rows.append(dict(case='Israeli storm Hs %g m' % Hs, tube=tube, FA=FA, B=float(d.B.iloc[0]), D=float(d.D.iloc[0]),
                         U_max=float(d.uplift_fraction.max()), h_at_U_max=float(d.h_base.iloc[int(np.argmax(d.uplift_fraction.values))]),
                         h_U1=u1_depth(d.h_base, d.uplift_fraction),
                         h_U_below1_seaward=(float(d[d.uplift_fraction >= 1].h_base.max()) if (d.uplift_fraction >= 1).any() else None),
                         Uc_max=float(d.uplift_fraction_contact.max())))
    return rows


def vansteeg_rows():
    rows = []
    for t in TUBES:
        for FA in (0.6, FA_DEFAULT):
            sec = section_for(t, FA)
            for rho in (RHO_FILL_BD23, 1900.0):
                hc = W.vansteeg_hs_crit(sec['B'], sec['D'], rho, f=F_FRICTION)
                rows.append(dict(tube=t['id'], FA=FA, B=sec['B'], D=sec['D'], rho_fill=rho, f=F_FRICTION, chi=1.0, Hs_crit=hc,
                                 h_base_where_depth_limited_Hs_equals_crit=hc / GAMMA_S,
                                 note='stable where the depth-limited Hs (0.55 h) or the local storm Hs is below Hs_crit; ' + t['C_rule'] + '; src: ' + t['src']))
    return rows


ROCKS = [
    dict(reef='cables-reef-wa', unit='body granite 1.5 t', M=1500.0, rho=2650.0, src='reefs.json material (Blacka 2013 A.1.3 p.93); rho ASSUMPTION 2650'),
    dict(reef='cables-reef-wa', unit='perimeter granite 3.0 t', M=3000.0, rho=2650.0, src='as above'),
    dict(reef='southern-ocean-surf-reef-albany', unit='armour D50 0.94 m', Dn=0.84 * 0.94, rho=2650.0, src='reefs.json material (design table); Dn50 = 0.84 D50 (ASSUMPTION sieve-to-nominal ratio); rho ASSUMPTION'),
    dict(reef='southern-ocean-surf-reef-albany', unit='core D50 0.49 m', Dn=0.84 * 0.49, rho=2650.0, src='as above'),
    dict(reef='southern-ocean-surf-reef-albany', unit='belly D50 0.16 m', Dn=0.84 * 0.16, rho=2650.0, src='as above'),
    dict(reef='borth-coastal-defence-reef', unit='Type 4 rock 6-10 t (8 t)', M=8000.0, rho=2650.0, src='reefs.json material (card R1)'),
    dict(reef='borth-coastal-defence-reef', unit='Type 1 rock 3-6 t (4.5 t)', M=4500.0, rho=2650.0, src='as above'),
]


def rock_rows(inp):
    rows = []
    for r in ROCKS:
        Dn = r.get('Dn') or (r['M'] / r['rho']) ** (1 / 3)
        M = r.get('M') or r['rho'] * Dn ** 3
        Delta = r['rho'] / W.RHO_W - 1
        met = inp[r['reef']]['lines']['crest_line']['metrics']
        for sl_name in ('mean_seaward_slope', 'max_seaward_slope'):
            tan = (met.get(sl_name) or {}).get('tan')
            if not tan:
                continue
            cot = 1 / tan
            Hst = Delta * Dn * (2.0 * cot) ** (1 / 3)
            rows.append(dict(reef=r['reef'], unit=r['unit'], M_kg=M, Dn50_m=Dn, Delta=Delta, slope=sl_name, cot_alpha=cot,
                             KD=2.0, H_stable_hudson=Hst, depth_where_breaking_H_equals_Hstable=Hst / 0.78,
                             extrapolated=bool(cot > 5.0), src=r['src']))
    return rows


def israel_depth_scan(calib):
    """Load index ESTIMATE for the Israeli geotubes vs base depth in storms (Hs 1 m T 7 s; 3.3 m T 10 s; 5 m T 12 s), for each FA.
    Wave height at the tube Hmax = min(1.8 Hs Ks, 0.78 h) (ASSUMPTION: Rayleigh maximum of ~1000 waves, then depth-limited)."""
    rows = []
    for t in [t for t in TUBES if t['id'] in ISRAELI]:
        for FA in FA_LIST:
            sec = section_for(t, FA)
            hc = W.vansteeg_hs_crit(sec['B'], sec['D'], RHO_FILL_BD23, f=F_FRICTION)
            for Hs, T in ((1.0, 7.0), (3.3, 10.0), (5.0, 12.0)):
                for h in np.arange(math.ceil((sec['D'] + 0.5) * 4) / 4, 16.01, 0.25):
                    Hmax = min(1.8 * Hs * float(W.shoaling_coefficient(T, h)), 0.78 * h)
                    r = fk_forces(sec, float(h), Hmax, T)
                    fac, facc = _cal(calib, Hmax / h >= 0.6)
                    rows.append(dict(tube=t['id'], FA=FA, B=sec['B'], D=sec['D'], Hs_storm=Hs, T=T, h_base=float(h), Hmax=Hmax,
                                     depth_limited=bool(Hmax >= 0.78 * h - 1e-6), SI_est=r['SI_max'], SI_calibrated=r['SI_max'] * fac,
                                     uplift_fraction=r['uplift_fraction'], uplift_fraction_contact=r['uplift_fraction_contact'],
                                     SIc_calibrated=r['SIc_max'] * facc, Fz_range_kN=r['Fz_range_kN'],
                                     state=state_of(r['uplift_fraction'], r['SI_max'] * fac, r['SIc_max'] * facc),
                                     state_contact=state_of(r['uplift_fraction_contact'], r['SIc_max'] * facc, r['SIc_max'] * facc),
                                     Fy_max_kN=r['Fy_max_kN'], Wsub_kN=r['Wsub_kN'], Hmax_rule='Hmax = min(1.8 Hs Ks, 0.78 h) (ASSUMPTION Rayleigh ~1000 waves)',
                                     Hs_crit_vansteeg=hc, Hs_local=min(Hs * float(W.shoaling_coefficient(T, h)), GAMMA_S * h)))
    return rows


def main():
    inp = RI.load()
    cal_rows, calib = calibrate()
    fk = tube_runs(calib)
    vs = vansteeg_rows()
    rk = rock_rows(inp)
    isr = israel_depth_scan(calib)
    fas = fa_summary(fk, isr)
    SA.write_csv(os.path.join(HERE, 'results_stability_fk.csv'), fk)
    SA.write_csv(os.path.join(HERE, 'results_stability_tubes.csv'), vs)
    SA.write_csv(os.path.join(HERE, 'results_stability_rock.csv'), rk)
    SA.write_csv(os.path.join(HERE, 'results_stability_israel_depth.csv'), isr)
    SA.write_csv(os.path.join(HERE, 'results_stability_fa_summary.csv'), fas)
    with open(os.path.join(HERE, 'results_fk_calibration.json'), 'w') as f:
        json.dump(dict(rows=cal_rows, factors=calib), f, indent=1)
    with open(os.path.join(HERE, 'results_stability.json'), 'w') as f:
        json.dump(dict(meta=dict(script='08_paper/analysis/stability_analysis.py', status='ESTIMATE (A, calibrated linear Froude-Krylov, not BELWF) / DERIVED (B, C); see RESULTS.md part 7',
                                 friction=F_FRICTION, gamma_s=GAMMA_S, rho_fill=RHO_FILL_BD23, tubes=TUBES, rocks=ROCKS,
                                 FA_list=FA_LIST, FA_default=FA_DEFAULT,
                                 geometry='Bezuijen & Vastenburg section as described by BD23 Sec. 2.2 (construction in bv_shape)'),
                       calibration=dict(rows=cal_rows, factors=calib), fa_summary=fas, fk=fk, vansteeg=vs, rock=rk, israel_depth=isr), f, indent=1, default=float)
    print(json.dumps(cal_rows, indent=0, default=float)[:2500])
    print(calib)
    for r in fas:
        print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})


if __name__ == '__main__':
    main()

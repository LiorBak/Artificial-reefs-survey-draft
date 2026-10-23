#!/usr/bin/env python3
"""figures_wave.py - Figure 3 of the surf-reef review: the wave over a gradual ramp and over an abrupt rise, to scale.

  python3 -I 08_paper/analysis/figures_wave.py            # writes fig3_wave_sketch.png / .pdf (+ caption by hand)

Inputs (read only; every number on the figure comes from these):
  08_paper/data/profiles/palm-beach-gold-coast.json, boscombe-surf-reef.json   lines.crest_line (profile + metrics), tidal planes
  08_paper/analysis/results_breaking.csv   rows crest_line, H0 = 1.0 m, T = 10 s, tide mid, gamma_mode mccowan (break point,
                                           H_b, d_b, xi_b, Y, class); the same incident wave in both panels
  08_paper/analysis/results_surf_site.csv  Boscombe site wave (0.5 m, 8 s), mid tide
  08_paper/analysis/wavelib.py             Airy shoaling and wavenumber (the water surface up to the break)
Geometry is the DERIVED 3D-model section (profiles/SUMMARY.md); the wave shapes at the break are schematic (height and
position are model values, the lip and foam shapes are drawn by hand); the sinusoids are linear theory (H = H0 Ks(d)).
"""
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style as S  # noqa: E402
import wavelib as W  # noqa: E402
from style import INK, INK2, SAND, SEABED, TIDE  # noqa: E402

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Ellipse, Patch, Polygon, Rectangle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
H0_SHARED, T_SHARED = 1.0, 10.0          # incident wave used in both panels (FIGURE_SPECS F3)
GAMMA = 0.78                             # McCowan 1894 via Weggel 1972 (wavelib REFS)
VE = 5.0                                 # vertical exaggeration of the overview panels
ZLO, ZHI = -8.0, 2.5                     # m MSL
XSEA, XSHORE = 133.0, -55.0              # m seaward of the crest's seaward edge (positive = seaward)
S_SEA, S_SHORE = 4.5, -8.5               # m, detail window: seaward / shoreward of the break (t0 + 1 s fits in)
INSET_Z = (-3.7, 1.75)
WATER = '#CFE3F2'
REEF = '#8C8C8C'
FOAM = '#FFFFFF'
FIG_H = 10.9                             # cm

PANELS = [
    dict(slug='palm-beach-gold-coast', letter='a', name='Palm Beach', kind='Long gradual ramp', site=(1.0, 10.0),
         israel=0.40),
    dict(slug='boscombe-surf-reef', letter='b', name='Boscombe', kind='Abrupt rise', site=(0.5, 8.0), israel=0.40),
]


# --------------------------------------------------------------------------------------------- data
def load(panel):
    s = panel['slug']
    pr = json.load(open(os.path.join(S.DATA_DIR, 'profiles', s + '.json'), encoding='utf-8'))
    L = pr['lines']['crest_line']
    m = L['metrics']
    p = L['profile']
    y = np.array(p['offshore_m'], float)
    bed = np.array(p['seabed_msl_m'], float)
    reef = np.array([np.nan if v is None else v for v in p['reef_msl_m']], float)
    top = np.where(np.isfinite(reef), np.maximum(bed, reef), bed)       # solid surface seen by the water
    b = pd.read_csv(os.path.join(HERE, 'results_breaking.csv'))
    r = b[(b.slug == s) & (b.line == 'crest_line') & (b.H0 == H0_SHARED) & (b['T'] == T_SHARED) & (b.tide == 'mid')
          & (b.gamma_mode == 'mccowan')].iloc[0]
    site = pd.read_csv(os.path.join(HERE, 'results_surf_site.csv'))
    rs = site[(site.slug == s) & (site.tide == 'mid')].iloc[0]
    pl = pr['tidal_planes_m_above_msl']
    lo, hi = (pl['MLWS'], pl['MHWS'])
    ce = m['crest_zone_y_m'][1]                                          # seaward edge of the crest zone (ramp starts here)
    return dict(y=y, bed=bed, reef=reef, top=top, m=m, r=r, rs=rs, lo=lo, hi=hi, ce=ce, spring=hi - lo)


def interp(y, z, yy):
    return np.interp(yy, y, z)


# --------------------------------------------------------------------------------------------- drawing helpers
def surfer_polys(x0, z0, xs=1.0):
    """Front-view standing surfer, 1.8 m from the feet to the top of the head, feet on z0 at x0.
    xs scales the horizontal coordinates only (xs = VE draws an undistorted pictogram in a vertically exaggerated panel).
    Returns (list of Polygon xy arrays, head centre, head radius)."""
    def P(pts):
        return np.array([[x0 + xs * a, z0 + b] for a, b in pts])
    body = [
        P([(-0.17, 0.0), (-0.05, 0.0), (-0.05, 0.90), (0.05, 0.90), (0.05, 0.0), (0.17, 0.0), (0.17, 0.96),     # legs
           (0.20, 1.50), (0.12, 1.55), (-0.12, 1.55), (-0.20, 1.50), (-0.17, 0.96)]),                           # hips, torso
        P([(0.18, 1.50), (0.76, 1.30), (0.78, 1.22), (0.70, 1.22), (0.16, 1.40)]),                              # arm right
        P([(-0.18, 1.50), (-0.76, 1.30), (-0.78, 1.22), (-0.70, 1.22), (-0.16, 1.40)]),                         # arm left
        P([(-0.30, -0.07), (0.30, -0.07), (0.30, 0.0), (-0.30, 0.0)]),                                          # board (end-on)
        P([(-0.04, 1.55), (0.04, 1.55), (0.04, 1.62), (-0.04, 1.62)]),                                          # neck
    ]
    head = (x0, z0 + 1.69, 0.11)
    return body, head


def draw_surfer(ax, x0, z0, xs=1.0, zorder=8):
    body, (hx, hz, hr) = surfer_polys(x0, z0, xs)
    for b in body:
        ax.add_patch(Polygon(b, closed=True, fc=INK, ec=INK, lw=0.3, zorder=zorder))
    ax.add_patch(Ellipse((hx, hz), 2 * hr * xs, 2 * hr, fc=INK, ec=INK, lw=0.3, zorder=zorder))


def bez(p0, p1, p2, p3, n=24):
    t = np.linspace(0, 1, n)[:, None]
    p0, p1, p2, p3 = map(np.array, (p0, p1, p2, p3))
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1 + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3


TROUGH_F = 0.38        # trough 0.35-0.4 H_b below the local mean level, crest about 0.6 H_b above (notes/fig3_theory.md s1)
SETDOWN_F = 0.05       # mean-level set-down at the break, about gamma H_b / 16 (Longuet-Higgins & Stewart 1964)
SETUP_F = 0.25         # set-up at the shoreline, order 0.2-0.3 H_b on a plane beach (order of magnitude, coefficient unverified)
BORE_CREST_F, BORE_TROUGH_F = 0.20, 0.20   # broken-wave bores landward of the break: about 0.4 H_b front (notes s2 spec)


def mean_level(u, Hb, ushore):
    """mean water level landward of the break (u >= 0, m shoreward of the breaking crest): set-down -0.05 H_b at the break,
    rising linearly to +0.25 H_b at the shoreline (u = ushore). Schematic of set-down / set-up theory."""
    return Hb * (-SETDOWN_F + (SETDOWN_F + SETUP_F) * np.clip(np.asarray(u, float) / ushore, 0.0, 1.0))


def bore_train(u, Hb, Lb, ushore, u_start, shift=0.0):
    """instantaneous surface landward of the breaking wave: the trough just in front of it (-0.38 H_b), then the back of the
    previous (already broken) wave rising to its bore crest one wavelength L_b ahead, a steep bore front, and so on; all
    riding on the mean level. u_start = where the breaking wave's front reaches the trough; shift = distance travelled."""
    u = np.asarray(u, float)
    ph = np.maximum(u - u_start, 0.0) / Lb
    k = np.floor(ph)
    f = ph - k
    dk = 0.8 ** k
    trough = np.where(k == 0, -TROUGH_F, -BORE_TROUGH_F * dk) * Hb
    crest = BORE_CREST_F * dk * Hb
    trough_next = -BORE_TROUGH_F * 0.8 ** (k + 1) * Hb
    z = np.where(f < 0.96, trough + (crest - trough) * f / 0.96, crest - (crest - trough_next) * (f - 0.96) / 0.04)
    return mean_level(u, Hb, ushore) + z


def breaker_shapes(H, kind, Lb, ushore, c_b, back=9.0):
    """Two time steps of the breaking wave as (u, z) outlines, u = m shoreward of the t0 crest (schematic shapes, model H_b):
    t0 = onset (plunging: crest sharpened, front near-vertical, lip starting; collapsing: steep front, rounded crest, no
    overturn); t1 = t0 + 1 s, crest moved c_b * 1 s shoreward (plunging: lip about 0.15 H_b thick thrown onto the trough ahead,
    air pocket; collapsing: front collapses from the base, which surges ahead as a thin sheet, crest a lower rounded hump).
    Returns dict(t0=..., t1=..., zt=trough level at the break, face=(u, z) of the surfer's feet, impact=(u, z) or None)."""
    mb = -SETDOWN_F * H
    zt = mb - TROUGH_F * H                         # trough level at the break

    def build(seg, crest_f, du):
        uu = np.linspace(-back, 0.0, 40)
        zb = zt + crest_f * H * (1 + np.cos(np.pi * uu / back)) / 2.0
        pts = [(-back - 8.0 + du, zt)] + [(x + du, z) for x, z in zip(uu, zb)]
        pts += [(du + H * a, zt + H * b) for a, b in seg[1:]]
        u_end = du + H * seg[-1][0]
        ul = np.linspace(u_end, u_end + 70.0, 600)[1:]
        zl = bore_train(ul, H, Lb, ushore, u_end)
        pts += list(zip(ul, zl))
        return np.array(pts), u_end

    if kind == 'plunging':
        s0 = np.vstack([bez((0.0, 1.0), (0.13, 1.01), (0.25, 0.93), (0.28, 0.74)),          # crest sharpened, lip starting
                        bez((0.28, 0.74), (0.29, 0.52), (0.22, 0.24), (0.40, 0.0))[1:]])     # near-vertical front
        s1 = np.vstack([bez((0.0, 0.95), (0.35, 1.00), (0.88, 0.86), (1.08, 0.08)),          # outer surface of the thrown lip
                        bez((1.08, 0.08), (1.02, 0.10), (0.98, 0.14), (0.95, 0.20))[1:],     # tip (about 0.15 H thick)
                        bez((0.95, 0.20), (0.82, 0.68), (0.40, 0.78), (0.27, 0.62))[1:],     # underside of the lip (air pocket below)
                        bez((0.27, 0.62), (0.17, 0.48), (0.14, 0.18), (0.30, 0.0))[1:],      # face down to the trough
                        bez((0.30, 0.0), (0.60, 0.0), (0.90, 0.0), (1.30, 0.0))[1:]])        # trough under the impact point
        cf1 = 0.95
    else:
        s0 = np.vstack([bez((0.0, 1.0), (0.10, 1.0), (0.17, 0.92), (0.20, 0.72)),           # rounded crest, steep front
                        bez((0.20, 0.72), (0.21, 0.46), (0.20, 0.20), (0.28, 0.0))[1:]])
        s1 = np.vstack([bez((0.0, 0.72), (0.22, 0.71), (0.42, 0.52), (0.62, 0.30)),          # lower rounded hump, front collapsing
                        bez((0.62, 0.30), (1.00, 0.14), (1.60, 0.06), (2.60, 0.02))[1:]])    # base surged ahead: thin sheet
        cf1 = 0.72
    s0[0] = (0.0, 1.0)
    s1[0] = (0.0, cf1)
    t0, u0end = build(s0, 1.0, 0.0)
    t1, u1end = build(s1, cf1, c_b * 1.0)
    impact = (c_b + H * 1.08, zt + 0.04 * H) if kind == 'plunging' else None
    return dict(t0=t0, t1=t1, zt=zt, mb=mb, face=(H * 0.40 + 0.30, zt), impact=impact, shift=c_b, u1end=u1end)


def water_surface(P, y_b, eta=0.0):
    """Linear-theory surface seaward of the break: eta + H/2 cos(theta), H = H0 Ks(d), theta = integral of k dy from y_b."""
    yy = np.arange(y_b, P['y'].max(), 0.25)
    d = eta - interp(P['y'], P['top'], yy)
    d = np.maximum(d, 0.05)
    k = W.wavenumber(T_SHARED, d)
    H = H0_SHARED * W.shoaling_coefficient(T_SHARED, d)
    H = np.minimum(H, GAMMA * d)                                         # never above the breaking limit
    theta = np.concatenate([[0.0], np.cumsum(0.5 * (k[1:] + k[:-1]) * np.diff(yy))])
    return yy, eta + 0.5 * H * np.cos(theta)


# --------------------------------------------------------------------------------------------- the figure
BLUE = '#2F6E9E'
RED = '#B03A2E'


def fig3():
    S.setup()
    plt.rcParams.update({'font.size': 7, 'axes.labelsize': 7, 'xtick.labelsize': 7, 'ytick.labelsize': 7})
    fig = plt.figure(figsize=(S.FULL_W, FIG_H * S.CM))
    wcm, hcm = 17.0, FIG_H

    def axes_cm(l, b, w, h, **kw):
        return fig.add_axes([l / wcm, b / hcm, w / wcm, h / hcm], **kw)

    L_OV, W_OV = 1.15, 10.2                                              # overview column (cm)
    L_IN, W_IN = 12.2, 4.7                                               # detail column (cm)
    mpc = (XSEA - XSHORE) / W_OV                                         # m per cm, horizontal (both panels)
    H_OV = (ZHI - ZLO) / (mpc / VE)                                      # cm for 10.5 m of elevation
    rows = [(7.15, PANELS[0]), (2.15, PANELS[1])]
    halo = dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.88)
    dim = dict(arrowstyle='<->', lw=0.7, color=INK, shrinkA=0, shrinkB=0, mutation_scale=5)
    for (bot, pan) in rows:
        P = load(pan)
        r, m = P['r'], P['m']
        ce = P['ce']
        x_of = lambda yv: yv - ce                                        # noqa: E731  model y -> m seaward of the crest edge
        ax = axes_cm(L_OV, bot, W_OV, H_OV)
        ax.set_xlim(XSEA, XSHORE)
        ax.set_ylim(ZLO, ZHI)
        xs = x_of(P['y'])
        yb = float(r.y_break)
        xb = x_of(yb)
        Hb = float(r.H_break)
        db = float(r.d_break)
        kind = 'plunging' if (r.breaker == 'plunging' and r.vortex_Y >= 1.6) else 'collapsing'
        c_b = float(np.sqrt(9.81 * db))                                  # shallow-water speed at the break (m/s): distance in 1 s
        Lb = c_b * T_SHARED                                              # wavelength at the break, L = T sqrt(g h_b)
        ushore = yb - (m.get('y_msl_crossing_m') or 0.0)                 # break to the model MSL shoreline (m)
        BS = breaker_shapes(Hb, kind, Lb, ushore, c_b)
        # water: linear train seaward of the break; landward the t0 breaker front, trough, broken-wave bores on a rising mean
        yy, eta_s = water_surface(P, yb)
        o0 = BS['t0']
        land = o0[o0[:, 0] > 0]
        dz = eta_s[0] - (BS['zt'] + Hb)                                  # match the crest of the linear train at the break
        ys_all = np.concatenate([yb - land[::-1, 0], yy])
        zs_all = np.concatenate([land[::-1, 1] + dz * np.clip(1 - land[::-1, 0] / 6.0, 0, 1), eta_s])
        zs_all = np.maximum(zs_all, interp(P['y'], P['top'], ys_all) + 0.03)
        ax.fill_between(x_of(ys_all), interp(P['y'], P['top'], ys_all), zs_all, color=WATER, lw=0, zorder=1)
        # mean water level: set-down toward the break, set-up landward (schematic of radiation-stress theory)
        um = np.linspace(0.0, -XSHORE + xb + 1, 60)
        sea_m = np.linspace(0.0, Lb, 20)
        ax.plot(np.concatenate([xb + sea_m[::-1], xb - um]),
                np.concatenate([-SETDOWN_F * Hb * (1 - sea_m[::-1] / Lb), mean_level(um, Hb, ushore)]),
                color='#1B3F66', lw=0.8, ls=(0, (5, 1.5, 1, 1.5)), zorder=7)
        # local spring tide band over the water, Israeli range as thin dashed lines
        ax.axhspan(P['lo'], P['hi'], color=TIDE, alpha=0.45, lw=0, zorder=2)
        # seabed sand and reef body
        ax.fill_between(xs, ZLO, P['bed'], color=SAND, lw=0, zorder=3)
        ok = np.isfinite(P['reef'])
        ax.fill_between(xs, np.where(ok, P['bed'], np.nan), np.where(ok, P['reef'], np.nan), facecolor='#CBBE9F',
                        edgecolor=INK2, hatch='////', lw=0, zorder=4)
        ax.plot(xs, P['top'], color=SEABED, lw=0.9, zorder=5, solid_capstyle='round')
        ax.plot(x_of(ys_all), zs_all, color=BLUE, lw=0.9, zorder=6)
        ax.axhline(0, color=INK2, lw=0.5, ls=(0, (6, 3)), zorder=6)
        for sgn in (-1, 1):
            ax.axhline(sgn * pan['israel'] / 2, color=RED, lw=0.6, ls=(0, (2, 2)), zorder=6)
        # dimension lines: crest level, toe-bed level, depth gap, ramp length
        zc = m['crest_z_msl_m']
        zt_bed = m['seaward_toe_seabed_z_msl_m']
        ramp = m['ramp_length_m']
        gap = m['crest_to_toe_seabed_drop_m']
        slope = m['mean_seaward_slope']['one_in']
        ax.plot([0, XSEA - 1], [zc, zc], color=INK, lw=0.5, ls=(0, (1, 2)), zorder=7)
        ax.plot([ramp, XSEA - 1], [zt_bed, zt_bed], color=INK, lw=0.5, ls=(0, (1, 2)), zorder=7)
        ax.annotate('', xy=(0, zc), xytext=(ramp, zc), arrowprops=dim, zorder=8)
        xg = XSEA - 6
        ax.annotate('', xy=(xg, zc), xytext=(xg, zt_bed), arrowprops=dim, zorder=8)
        ax.text(xg - 3, (zc + zt_bed) / 2, 'depth gap\n%.2f m' % gap, ha='left', va='center', fontsize=7, bbox=halo, zorder=9)
        ax.text(xg - 3, zc - 0.12, 'crest depth %.2f m' % (-zc), ha='left', va='top', fontsize=7, bbox=halo, zorder=9)
        ax.text(xg - 3, zt_bed + 0.12, 'toe-bed depth %.2f m' % (-zt_bed), ha='left', va='bottom', fontsize=7, bbox=halo, zorder=9)
        rtxt = 'ramp %.0f m, mean slope 1:%.1f' % (ramp, slope)
        if ramp > 40:
            ax.text(ramp / 2.0, zc + 0.12, rtxt, ha='center', va='bottom', fontsize=7, bbox=halo, zorder=9)
        else:
            ax.text(ramp + 3, zc - 0.15, rtxt, ha='right', va='top', fontsize=7, bbox=halo, zorder=9)
        # zoom window of the 1:1 detail
        z0w, z1w = INSET_Z
        ax.add_patch(Rectangle((xb + S_SHORE, z0w), S_SEA - S_SHORE, z1w - z0w, fill=False, ec=INK, lw=0.6, ls=(0, (3, 2)),
                               zorder=9))
        ax.text(XSEA - 1.5, ZHI - 0.1, '(%s) %s: %s' % (pan['letter'], pan['kind'], pan['name']), ha='left', va='top',
                fontsize=7.5, fontweight='bold', zorder=9)
        ax.text(XSEA - 1.5, ZHI - 0.95, 'H$_0$ = %.1f m, T = %.0f s, tide MSL; local spring range %.2f m' % (H0_SHARED, T_SHARED, P['spring']),
                ha='left', va='top', fontsize=7, color=BLUE, zorder=9)
        # surfer pictogram (true height 1.8 m on the vertical axis; undistorted width) on the face at the break
        zt = BS['zt']
        fu = BS['face'][0]
        draw_surfer(ax, xb - fu, zt + 0.07, xs=VE, zorder=9)
        ax.set_ylabel('Elevation (m MSL)')
        ax.set_yticks([-8, -6, -4, -2, 0, 2])
        ax.set_xticks(np.arange(120, XSHORE - 1, -20))
        ax.set_xlabel('Distance seaward of the crest edge (m); shore to the right; overview vertical exaggeration 5:1' if pan['letter'] == 'b' else '')
        ax.tick_params(length=2.5)

        # ---- 1:1 detail: two time steps (t0 onset, filled; t0 + 1 s, dark outline)
        bz = z1w - z0w
        h_in = bz / ((S_SEA - S_SHORE) / W_IN)                           # cm, equal scale in x and z
        bx = axes_cm(L_IN, bot + H_OV - h_in - 0.55, W_IN, h_in)
        bx.set_xlim(S_SEA, S_SHORE)
        bx.set_ylim(z0w, z1w)
        sx = np.linspace(-60.0, 22.0, 2000)                              # s = y - y_break (positive offshore)
        ysx = yb + sx
        topx = interp(P['y'], P['top'], ysx)
        bedx = interp(P['y'], P['bed'], ysx)
        rf = interp(P['y'], np.nan_to_num(P['reef'], nan=-99.0), ysx)
        reefx = np.where(rf > bedx + 0.02, rf, bedx)
        bx.fill_between(sx, -12, bedx, color=SAND, lw=0, zorder=3)
        bx.fill_between(sx, bedx, reefx, facecolor='#CBBE9F', edgecolor=INK2, hatch='////', lw=0, zorder=4)
        bx.plot(sx, topx, color=SEABED, lw=0.9, zorder=5)
        for key, filled in (('t0', True), ('t1', False)):
            o = BS[key]
            su, zu = -o[:, 0], o[:, 1]                                   # u is shoreward, inset x is s = -u
            if filled:                                                   # water body at t0 (single-valued part)
                zf = np.maximum(zu, np.interp(su, sx, topx))
                msk = (sx >= su.min()) & (sx <= su.max())
                poly = np.vstack([np.column_stack([su, zf]), np.column_stack([sx[msk], topx[msk] - 0.02])])
                bx.add_patch(Polygon(poly, closed=True, fc=WATER, ec='none', zorder=1))
                bx.plot(su, zu, color=BLUE, lw=1.0, zorder=7)
            else:
                bx.plot(su, zu, color='#1B3F66', lw=0.9, ls=(0, (3.5, 1.2)), zorder=7.5)
        # mean water level (set-down at the break, rising landward)
        um = np.linspace(0, -S_SHORE + 1, 30)
        bx.plot(np.concatenate([[S_SEA], -um]), np.concatenate([[-SETDOWN_F * Hb * 0.5], mean_level(um, Hb, ushore)]),
                color='#1B3F66', lw=0.7, ls=(0, (5, 1.5, 1, 1.5)), zorder=6.5)
        sh = BS['shift']
        if BS['impact'] is not None:                                     # white water where the lip hits the trough
            ui, zi = BS['impact']
            bx.add_patch(Ellipse((-ui, zi + 0.08), 0.9, 0.38, fc='white', ec='#1B3F66', lw=0.5, zorder=8))
            bx.text(-ui - 0.2, zi - 0.22, 'air pocket,\nwhite water', ha='center', va='top', fontsize=6.3, color='#1B3F66', zorder=10,
                    bbox=dict(boxstyle='round,pad=0.08', fc='white', ec='none', alpha=0.8))
        else:                                                            # thin foam on the collapsing front / run-up sheet
            uf = sh + Hb * np.array([0.55, 0.9, 1.5, 2.5, 2.5, 1.5, 0.9, 0.55])
            zf = zt + Hb * np.array([0.34, 0.20, 0.10, 0.04, 0.0, 0.03, 0.10, 0.22])
            bx.add_patch(Polygon(np.column_stack([-uf, zf]), closed=True, fc='white', ec='#1B3F66', lw=0.5, zorder=8))
            bx.text(-(sh + Hb * 1.6), zt - 0.22, 'run-up sheet,\nlittle foam', ha='center', va='top', fontsize=6.3, color='#1B3F66',
                    zorder=10, bbox=dict(boxstyle='round,pad=0.08', fc='white', ec='none', alpha=0.8))
        bx.text(2.0, zt + Hb - 0.12, 't$_0$', ha='center', va='top', fontsize=7, color=BLUE, fontweight='bold', zorder=10)
        bx.text(-sh, zt + Hb * (0.95 if kind == 'plunging' else 0.72) + 0.12, 't$_0$ + 1 s', ha='center', va='bottom', fontsize=7,
                color='#1B3F66', zorder=10)
        draw_surfer(bx, -fu, zt + 0.07, xs=1.0, zorder=9)
        # height dimension (H_b) on the seaward side (guide lines from crest and trough), depth dimension (h_b) under the crest
        xh = S_SEA - 0.9
        zc_b = zt + Hb
        bx.plot([0.1, xh + 0.2], [zc_b, zc_b], color=INK, lw=0.4, ls=(0, (1, 2)), zorder=8)
        bx.plot([xh + 0.2, -0.2], [zt, zt], color=INK, lw=0.4, ls=(0, (1, 2)), zorder=8)
        bx.annotate('', xy=(xh, zc_b), xytext=(xh, zt), arrowprops=dim, zorder=10)
        bx.text(xh - 0.45, zc_b + 0.28, 'H$_b$ = %.2f m' % Hb, ha='left', va='bottom', fontsize=7, zorder=10)
        zbed_b = float(interp(P['y'], P['top'], np.array([yb]))[0])
        bx.annotate('', xy=(1.0, 0.0), xytext=(1.0, zbed_b), arrowprops=dim, zorder=10)
        bx.text(1.4, zbed_b / 2 - 0.05, 'h$_b$ = H$_b$/\u03b3\n= %.2f m' % db, ha='right', va='center', fontsize=7, bbox=halo, zorder=10)
        bx.set_xticks([4, 2, 0, -2, -4, -6, -8])
        bx.set_yticks([-4, -2, 0])
        bx.tick_params(length=2.0)
        bx.set_xlabel('Distance seaward of the break (m)', labelpad=1.5)
        bx.set_ylabel('m MSL', labelpad=1.0)
        bx.text(S_SEA, z1w + 0.1, '1:1 detail (dashed box): t$_0$ and t$_0$ + 1 s', ha='left', va='bottom', fontsize=7, color=INK)
        # text block under the inset
        ty = bot + H_OV - h_in - 0.55 - 0.75
        dag = '†' if bool(r.vortex_extrapolated) else ''
        bname = 'plunging' if r.breaker == 'plunging' else 'collapsing'
        vcls = {'beyond_extreme': 'beyond extreme', 'very_high': 'very high', 'extreme': 'extreme'}.get(r.vortex_class, r.vortex_class)
        lines = [
            '\u03be$_b$ = %.2f (%s)' % (r.xi_b, bname),
            'Y = %.2f%s (%s)' % (r.vortex_Y, dag, vcls),
        ]
        if pan['slug'] == 'boscombe-surf-reef':
            rs = P['rs']
            lines.append('site wave 0.5 m, 8 s: \u03be$_b$ %.2f, Y %.2f\u2020' % (rs.xi_b, rs.vortex_Y))
        fig.text(L_IN / wcm, ty / hcm, '\n'.join(lines), ha='left', va='top', fontsize=7, linespacing=1.3, color=INK)

    fig.text((L_OV + W_OV / 2) / wcm, 6.02 / hcm, 'Same depth gap (4.5 to 5.5 m), different ramp: 89 m versus 13 m', ha='center', va='center',
             fontsize=7.5, fontweight='bold', color='#7A1F1F')
    handles = [
        Patch(fc=WATER, ec=BLUE, lw=0.6, label='sea'),
        Patch(fc=SAND, ec=SEABED, lw=0.6, label='seabed'),
        Patch(fc='#CBBE9F', ec=INK2, hatch='////', lw=0.4, label='reef'),
        Patch(fc=TIDE, alpha=0.6, lw=0, label='local spring range'),
        Line2D([0], [0], color=RED, lw=0.8, ls=(0, (2, 2)), label='Israeli spring range 0.40 m'),
        Patch(fc=INK, ec=INK, label='surfer, 1.8 m tall'),
        Line2D([0], [0], color=BLUE, lw=1.0, label='surface at t$_0$ (onset)'),
        Line2D([0], [0], color='#1B3F66', lw=0.9, ls=(0, (3.5, 1.2)), label='t$_0$ + 1 s'),
        Line2D([0], [0], color='#1B3F66', lw=0.8, ls=(0, (5, 1.5, 1, 1.5)), label='mean level (set-down, set-up)'),
    ]
    fig.legend(handles=handles, loc='lower left', bbox_to_anchor=(0.04, -0.005), ncol=5, frameon=False, fontsize=7,
               handlelength=1.5, columnspacing=1.1, handletextpad=0.4)
    return fig


def main():
    paths = S.save(fig3(), 'fig3_wave_sketch')
    print('\n'.join(paths))


if __name__ == '__main__':
    main()

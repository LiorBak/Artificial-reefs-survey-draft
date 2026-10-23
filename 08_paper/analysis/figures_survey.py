#!/usr/bin/env python3
"""figures_survey.py - survey layout figures of the surf-reef review paper (re-runnable).

  python3 -I 08_paper/analysis/figures_survey.py            # all three
  python3 -I 08_paper/analysis/figures_survey.py fig1       # or fig2 / figB

Writes into 08_paper/figures/ (PNG 300 dpi + PDF + <name>.caption.md):
  fig1_plan_and_profiles   (+ _rowA, _rowB)  plan shapes (top) and cross-shore profiles (below), nine reefs, one metric scale
  fig2_reef_size_overview                    dot plot of size, volume, crest depth, depth gap for all 13 reefs
  figB_3d_gallery                            appendix: 3D model previews (07_scale/shapes/<slug>/3d/preview_oblique.png)

Inputs (read only): 07_scale/shapes/<slug>/shape.json (default outline), 08_paper/data/profiles/<slug>.json (sections, datum,
shoreline definition, tidal planes), 08_paper/data/reefs.json (master table), 07_scale/shapes/<slug>/3d/preview_oblique.png.
Every plotted number is DERIVED (traced outline / 3D-model section) or taken from the master table; see the captions.
"""
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style as S  # noqa: E402
from style import COLORS, MARKERS, NAMES, SLUGS, cm  # noqa: E402

import matplotlib.patheffects as pe  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Polygon  # noqa: E402
from matplotlib.ticker import MultipleLocator  # noqa: E402

SCALE = 66.0            # m per cm, plan (x and y) and profile abscissa: ONE horizontal scale
FIG_W = 17.0            # cm
ML, MR = 1.75, 0.08      # left / right margin (cm)
NSLOT = 5
SLOT_W = (FIG_W - ML - MR) / NSLOT          # cm
PAD = 0.10              # cm between profile panels
YLO_PLAN, YHI_PLAN = -14.0, 380.0           # m
PLAN_H = (YHI_PLAN - YLO_PLAN) / SCALE      # cm (equal scale in x and y)
HEAD_H = 0.95
GAP_H = 0.28
PROF_H = 3.3
XLAB_H = 0.85
ZLO, ZHI = -8.6, 2.6                        # m, profile elevation range
VE = (SCALE / ((ZHI - ZLO) / PROF_H))       # vertical exaggeration of the profiles
ROW_H = HEAD_H + PLAN_H + GAP_H + PROF_H + XLAB_H

ORDER_A = ['cables-reef-wa', 'narrowneck-gold-coast', 'prattes-reef-el-segundo', 'mount-maunganui-reef', 'boscombe-surf-reef']
ORDER_B = ['borth-coastal-defence-reef', 'palm-beach-gold-coast', 'bunbury-airwave', 'southern-ocean-surf-reef-albany']
UNKNOWN_SHAPE = ['opunake-reef', 'kovalam-reef-india', 'burkitts-reef-bargara', 'mexico-reef-2026-unnamed']
SHORT_UNK = {'opunake-reef': 'Opunake', 'kovalam-reef-india': 'Kovalam', 'burkitts-reef-bargara': 'Burkitts', 'mexico-reef-2026-unnamed': 'Xala'}
NOTE3 = {'narrowneck-gold-coast': 'renewed 2018', 'bunbury-airwave': 'failed attempt', 'borth-coastal-defence-reef': 'north reef + oval',
         'cables-reef-wa': 'design outline'}
CC = {'AU': 'AU', 'US': 'US', 'NZ': 'NZ', 'UK': 'UK', 'IN': 'IN', 'MX': 'MX'}


# ----------------------------------------------------------------------------- data
def load_reefs():
    return {r['slug']: r for r in json.load(open(os.path.join(S.DATA_DIR, 'reefs.json'), encoding='utf-8'))}


def load_profile(slug):
    return json.load(open(os.path.join(S.DATA_DIR, 'profiles', slug + '.json'), encoding='utf-8'))


def load_shape(slug):
    return json.load(open(os.path.join(S.SHAPES, slug, 'shape.json'), encoding='utf-8'))


def val(r, k):
    x = r.get(k)
    return None if x is None else x.get('value')


def year_label(r):
    yb, yc = val(r, 'year_built'), val(r, 'year_completed')
    if yb is None:
        return '?'
    if yc is None or yc == yb:
        return str(yb)
    return '%d–%s' % (yb, str(yc)[2:] if str(yc)[:2] == str(yb)[:2] else str(yc))


def pick_line(pr, table_crest):
    """Section whose crest depth is closest to the master-table crest depth (ties: crest_line, centreline, second)."""
    if pr['lines']['crest_line'].get('override'):          # per-reef surf cut (Lior 2026-10-19) is always the plotted section
        return 'crest_line'
    best = None
    for ln in ('crest_line', 'centreline', 'second_crest_line'):
        m = pr['lines'][ln]['metrics']
        if not m.get('reef_on_line'):
            continue
        d = abs(m['crest_depth_below_msl_m'] - table_crest)
        if best is None or d < best[0] - 1e-9:
            best = (d, ln)
    return best[1]


def tide_band(pl):
    for lo, hi in (('MLWS', 'MHWS'), ('ANN_LO', 'ANN_HI'), ('MLLW', 'MHHW')):
        if lo in pl and hi in pl:
            return pl[lo], pl[hi], '%s–%s' % (lo, hi)
    return None, None, None


def section_data(slug, R, pr):
    """The plotted cross-shore section: arrays vs distance from the shoreline plus crest/toe/gap read from it."""
    ln = pick_line(pr, val(R[slug], 'crest_depth_msl_m'))
    L = pr['lines'][ln]
    m = L['metrics']
    p = L['profile']
    off = np.array(p['offshore_m'], float)
    bed = np.array(p['seabed_msl_m'], float)
    reef = np.array([np.nan if v is None else v for v in p['reef_msl_m']], float)
    if m.get('y_msl_crossing_m') is not None:
        ysh = float(m['y_msl_crossing_m'])
    else:                                    # Cables: fitted true shoreline (derived in the profile JSON)
        ysh = float(m['crest_y_m'] - m['crest_distance_from_true_shoreline_m'])
    d = off - ysh
    ok = np.isfinite(reef)
    crest_z = m['crest_z_msl_m']
    toe_d = m['seaward_toe_y_m'] - ysh
    toe_bed = m['seaward_toe_seabed_z_msl_m']
    lo, hi, nm = tide_band(pr['tidal_planes_m_above_msl'])
    return dict(line=ln, x_line=L['x_line_m'], ysh=ysh, d=d, bed=bed, reef=reef, reef_d0=d[ok].min(), reef_d1=d[ok].max(),
                crest_d=m['crest_y_m'] - ysh, crest_z=crest_z, crest_depth=-crest_z, toe_d=toe_d, toe_bed=toe_bed,
                toe_depth=-toe_bed, gap=(-toe_bed) - (-crest_z), tide_lo=lo, tide_hi=hi, tide_name=nm,
                ramp=m['ramp_length_m'], off=off, run_xy=L.get('reef_run_xy_m'),
                dirv=(L.get('oblique') or {}).get('direction_xy', [0.0, 1.0]), override=bool(L.get('override')))


def default_polys(sh):
    d = sh.get('default_outline')
    for v in sh.get('outline_versions', []) or []:
        if v['id'] == d:
            return v['polygons_m'], v['id']
    return sh['canonical']['polygons_m'], 'canonical'


def plan_geometry(slug, sec):
    """Outline polygons and section line in the shore-aligned plan frame.
    x_plot = alongshore, seen LOOKING SEAWARD from the beach (unmirrored, offshore up); v = offshore distance from the MSL line.
    All shape.json frames except Cables are 'x alongshore, y offshore = x turned 90 deg clockwise' (compass), so x_plot = -x;
    for Cables the canonical frame is x north / y west (the other handedness), so x_plot = along-shore coordinate u."""
    sh = load_shape(slug)
    polys, vid = default_polys(sh)
    ysh = sec['ysh']
    if slug == 'cables-reef-wa':
        g = sh['geo']
        th = math.radians(g['theta_ccw_deg'])
        xc, yc = g['anchor_canonical_xy_m']
        E0, N0 = g['anchor_E'], g['anchor_N']
        sb = math.radians(g['shoreline_bearing_deg_T'])
        dv, nv = (math.sin(sb), math.cos(sb)), (-math.cos(sb), math.sin(sb))
        S0 = (E0 + g['anchor_to_0m_AHD_line_m']['90'], N0)

        def c2uv(x, y):
            a, b = -(y - yc), (x - xc)
            E = E0 + a * math.cos(th) - b * math.sin(th)
            N = N0 + a * math.sin(th) + b * math.cos(th)
            dE, dN = E - S0[0], N - S0[1]
            return dE * dv[0] + dN * dv[1], dE * nv[0] + dN * nv[1]
        P = [np.array([c2uv(x, y) for x, y in poly]) for poly in polys]
        (xa, ya), (xb, yb) = sec['run_xy']        # model (x, y) of the reef run on the plotted (possibly oblique) cut
        dvx, dvy = sec['dirv']
        sline = np.array([c2uv(-(xa - 8 * dvx), ya - 8 * dvy), c2uv(-(xb + 8 * dvx), yb + 8 * dvy)])   # canonical x = -model x
    elif slug == 'bunbury-airwave':
        P = [np.array([(-x, y + sec['crest_d']) for x, y in poly]) for poly in polys]   # circle D = 12 m, centre at crest distance
        sline = np.array([(0, sec['reef_d0'] - 8), (0, sec['reef_d1'] + 8)], float)
    else:
        P = [np.array([(-x, y - ysh) for x, y in poly]) for poly in polys]
        (xa, ya), (xb, yb) = sec['run_xy']
        dvx, dvy = sec['dirv']
        sline = np.array([(-(xa - 8 * dvx), ya - 8 * dvy - ysh), (-(xb + 8 * dvx), yb + 8 * dvy - ysh)], float)
    allp = np.vstack(P)
    cx = 0.5 * (allp[:, 0].min() + allp[:, 0].max())
    P = [p - np.array([cx, 0]) for p in P]
    sline = sline - np.array([cx, 0])
    return dict(polys=P, section=sline, outline_id=vid, width=np.ptp(allp[:, 0]), v0=allp[:, 1].min(), v1=allp[:, 1].max())


def darker(c, f=0.55):
    c = c.lstrip('#')
    r, g, b = [int(c[i:i + 2], 16) for i in (0, 2, 4)]
    return '#%02x%02x%02x' % (int(r * f), int(g * f), int(b * f))


def lighter(c, f=0.45):
    c = c.lstrip('#')
    r, g, b = [int(c[i:i + 2], 16) for i in (0, 2, 4)]
    return '#%02x%02x%02x' % tuple(int(v + (255 - v) * (1 - f)) for v in (r, g, b))


HALO = [pe.withStroke(linewidth=1.6, foreground='white')]


# ----------------------------------------------------------------------------- figure 1
def tick_window(c, W, dmin, dmax):
    """window [s, s+W] around c; shifted <= 25 m so that the 50-m ticks keep clear of both edges; inside [dmin, dmax]."""
    best = None
    for s in np.arange(c - W / 2 - 25, c - W / 2 + 25.1, 1.0):
        s = min(max(s, dmin), dmax - W)
        ticks = np.arange(math.ceil(s / 50) * 50, s + W, 50)
        sc = min([min(t - s, s + W - t) for t in ticks] or [0]) - 0.1 * abs(s - (c - W / 2))
        if best is None or sc > best[0]:
            best = (sc, s)
    return best[1], best[1] + W


def draw_profile(ax, slug, sec, W, first_col):
    col = COLORS[slug]
    s0, s1 = tick_window(0.5 * (sec['reef_d0'] + sec['reef_d1']), W, sec['d'].min(), sec['d'].max())
    d, bed, reef = sec['d'], sec['bed'], sec['reef']
    ax.set_xlim(s0, s1)
    ax.set_ylim(ZLO, ZHI)
    ax.axhspan(sec['tide_lo'], sec['tide_hi'], color=S.TIDE, alpha=0.55, lw=0, zorder=1)
    ax.axhline(0, color='#2B5F8A', lw=0.7, ls=(0, (4, 2)), zorder=2)
    ax.fill_between(d, ZLO - 1, bed, color=S.SAND, lw=0, zorder=2)
    ax.plot(d, bed, color=S.SEABED, lw=0.8, zorder=3)
    ok = np.isfinite(reef)
    ax.fill_between(d, bed, np.where(ok, reef, bed), where=ok, color=col, lw=0, zorder=4)
    ax.plot(d[ok], reef[ok], color=darker(col), lw=0.7, zorder=5)
    # crest, toe, gap
    zc, zt, dc, dt = sec['crest_z'], sec['toe_bed'], sec['crest_d'], sec['toe_d']
    ax.plot([dc], [zc], 'o', ms=2.6, mfc='white', mec=S.INK, mew=0.7, zorder=7)
    ax.plot([dt], [zt], 'o', ms=2.6, mfc='white', mec=S.INK, mew=0.7, zorder=7)
    xa = s1 - 0.16 * SCALE
    guide = dict(color=S.INK2, lw=0.5, ls=(0, (1.5, 1.5)), zorder=6)
    ax.plot([dc, xa], [zc, zc], **guide)
    ax.plot([dt, xa], [zt, zt], **guide)
    ax.annotate('', xy=(xa, zt), xytext=(xa, zc), arrowprops=dict(arrowstyle='<->', color=S.INK, lw=0.7, shrinkA=0, shrinkB=0,
                                                                  mutation_scale=5), zorder=8)
    ax.text(xa - 4, 0.5 * (zc + zt), 'G %.1f' % sec['gap'], ha='right', va='center', fontsize=7, path_effects=HALO, zorder=9)
    cdep = sec['crest_depth']
    ax.text(dc, zc + 0.28, ('C %.1f' % cdep).replace('-', '\u2212'), ha='center', va='bottom', fontsize=7,
            path_effects=HALO, zorder=9)
    ax.text(dt, zt - 0.32, 'T %.1f' % sec['toe_depth'], ha='center', va='top', fontsize=7, path_effects=HALO, zorder=9)
    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_minor_locator(MultipleLocator(10))
    ax.tick_params(axis='x', which='minor', length=1.2, width=0.4)
    ax.set_yticks([-8, -6, -4, -2, 0, 2])
    if not first_col:
        ax.tick_params(axis='y', labelleft=False)
    ax.spines['left'].set_color(S.INK2)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    return s0, s1


def draw_row(fig, H, y_top, slugs, R, SEC, GEO, with_notes):
    """one row: header + plan + profiles. y_top = distance of the row top from the figure top (cm)."""
    def axes_cm(x, ytop, w, h):
        return fig.add_axes([x / FIG_W, 1 - (ytop + h) / H, w / FIG_W, h / H])
    W_slot_m = SLOT_W * SCALE
    # plan: one wide axes, same metric scale in x and y
    axp = axes_cm(ML, y_top + HEAD_H, NSLOT * SLOT_W, PLAN_H)
    axp.set_xlim(0, NSLOT * W_slot_m)
    axp.set_ylim(YLO_PLAN, YHI_PLAN)
    axp.axhspan(0, YHI_PLAN, color=S.SEA, lw=0, zorder=0)
    axp.axhspan(YLO_PLAN, 0, color=S.SAND, lw=0, zorder=0)
    for yy in (100, 200, 300):
        axp.axhline(yy, color='white', lw=0.7, zorder=1)
    axp.axhline(0, color='#6B5B3A', lw=1.1, zorder=2)
    axp.set_yticks([0, 100, 200, 300])
    axp.set_xticks([])
    axp.spines['bottom'].set_visible(False)
    axp.set_ylabel('Distance offshore from shoreline (m)', labelpad=2)
    if y_top == 0 or True:
        axp.text(6, -10, 'shoreline (MSL line)', fontsize=7, va='center', ha='left', color='#5A4A2A', zorder=5)
    for i, slug in enumerate(slugs):
        r, g = R[slug], GEO[slug]
        xc = (i + 0.5) * W_slot_m
        col = COLORS[slug]
        for k, P in enumerate(g['polys']):
            Q = P + np.array([xc, 0])
            oval = slug == 'borth-coastal-defence-reef' and k == 1
            axp.add_patch(Polygon(Q, closed=True, fc=col, ec=darker(col), lw=0.5, alpha=0.45 if oval else 1.0,
                                  hatch='////' if oval else None, zorder=4))
        if slug == 'bunbury-airwave':
            yc = SEC[slug]['crest_d']
            axp.plot([xc], [yc], 'o', ms=8, mfc='none', mec=darker(col), mew=0.6, zorder=3)
            axp.text(xc + 14, yc, '12 m', fontsize=7, va='center', ha='left', zorder=6)
        axp.plot(g['section'][:, 0] + xc, g['section'][:, 1], color='black', lw=0.55, ls=(0, (3, 1.6)), zorder=6)
        # header (three short lines, left aligned)
        xl = i * W_slot_m + 0.30 * SCALE
        tr = axp.get_xaxis_transform()
        axp.plot([i * W_slot_m + 0.13 * SCALE], [1 + (0.09 + 0.54 + 0.10) / PLAN_H], transform=tr, clip_on=False,
                 **S.marker_kw(slug, ms=4.6))
        axp.text(xl, 1 + 0.09 / PLAN_H + 0.54 / PLAN_H, NAMES[slug], transform=tr, fontsize=7.5, fontweight='bold', va='bottom',
                 ha='left', clip_on=False, color=darker(col, 0.8))
        axp.text(xl, 1 + 0.09 / PLAN_H + 0.27 / PLAN_H, '%s, %s' % (year_label(r), S.PLACE[slug].split(', ')[-1]), transform=tr,
                 fontsize=7, va='bottom', ha='left', clip_on=False, color=S.INK2)
        if slug in NOTE3:
            axp.text(xl, 1 + 0.09 / PLAN_H, NOTE3[slug], transform=tr, fontsize=7, va='bottom', ha='left', clip_on=False,
                     color=S.INK2, style='italic')
    # notes slot (plan region): shapes not known
    if with_notes:
        i = len(slugs)
        x0 = i * W_slot_m + 0.10 * SCALE
        axp.text(x0, 372, 'Shape unknown,\nnot drawn:', fontsize=7, va='top', ha='left', fontweight='bold', color=S.INK2, linespacing=1.15)
        for k, u in enumerate(UNKNOWN_SHAPE):
            yy = 318 - k * 28
            axp.plot([x0 + 6], [yy], marker=MARKERS[u], ms=4, mfc='white', mec=S.UNKNOWN, mew=0.8, ls='')
            axp.text(x0 + 20, yy, '%s (%s, %s)' % (SHORT_UNK[u], S.PLACE[u].split(', ')[-1], year_label(R[u]).split('\u2013')[0]),
                     fontsize=7, va='center', ha='left', color=S.INK2)
        axp.text(x0, 190, 'Dashed line: section\nshown below (through\nthe surfed part, normal\nto the shoreline)', fontsize=7, va='top', ha='left', color=S.INK2)
        axp.plot([x0, x0 + 100], [96, 96], color='black', lw=1.6, solid_capstyle='butt')
        axp.text(x0 + 50, 84, '100 m', fontsize=7, ha='center', va='top')
        axp.text(x0, 58, 'x and y: one scale\n(1 cm = %d m)' % SCALE, fontsize=7, ha='left', va='top', color=S.INK2)
    axp.text(NSLOT * W_slot_m - 6, -10, 'alongshore: arbitrary slots, view seaward', fontsize=7, va='center', ha='right', color='#5A4A2A', zorder=5)
    # profiles
    y_prof = y_top + HEAD_H + PLAN_H + GAP_H
    Wp_m = (SLOT_W - PAD) * SCALE
    for i, slug in enumerate(slugs):
        ax = axes_cm(ML + i * SLOT_W + PAD / 2, y_prof, SLOT_W - PAD, PROF_H)
        draw_profile(ax, slug, SEC[slug], Wp_m, first_col=(i == 0))
        if i == 0:
            ax.set_ylabel('Elevation (m, MSL)', labelpad=2)
    if with_notes:
        ax = axes_cm(ML + len(slugs) * SLOT_W + PAD / 2, y_prof, SLOT_W - PAD, PROF_H)
        ax.axis('off')
        h = [Patch(fc='#8C8C8C', ec='none', label='reef (colour as plan)'), Patch(fc=S.SAND, ec='none', label='natural seabed'),
             Patch(fc=S.TIDE, alpha=0.55, ec='none', label='tide range (spring or\ngreat diurnal / annual,\nsee Table)'),
             Line2D([], [], color='#2B5F8A', lw=0.7, ls=(0, (4, 2)), label='MSL')]
        ax.legend(handles=h, loc='upper left', frameon=False, handlelength=1.3, borderaxespad=0, labelspacing=0.25,
                  bbox_to_anchor=(0.0, 1.03), fontsize=7)
        ax.text(0.0, 0.40, 'C crest depth (m)\nT toe bed depth (m)\nG gap = T \u2212 C (m)\ndepths below MSL;\nC < 0: above MSL', fontsize=7,
                va='top', ha='left', transform=ax.transAxes, linespacing=1.25)
    # row labels (rotated, left of the y axes)
    for ytop, hh, txt in ((y_top + HEAD_H, PLAN_H, 'Top view'), (y_prof, PROF_H, 'Side view')):
        fig.text(0.28 / FIG_W, 1 - (ytop + hh / 2) / H, txt, rotation=90, ha='center', va='center', fontsize=9.5, fontweight='bold')
    # x label of the row
    fig.text((ML + 0.5 * NSLOT * SLOT_W) / FIG_W, 1 - (y_prof + PROF_H + 0.62) / H,
             'Distance offshore along the section (m); window position differs per reef, horizontal scale = plan scale',
             ha='center', va='center', fontsize=7.5)


def build_fig1(rows, name):
    R = load_reefs()
    PR = {s: load_profile(s) for s in ORDER_A + ORDER_B}
    SEC = {s: section_data(s, R, PR[s]) for s in PR}
    GEO = {s: plan_geometry(s, SEC[s]) for s in PR}
    LEG_H = 0.80                                      # bottom strip: outcome-shape legend of the header symbols
    H = 0.1 + len(rows) * ROW_H + (len(rows) - 1) * 0.15 + LEG_H
    fig = plt.figure(figsize=(FIG_W * S.CM, H * S.CM))
    y = 0.1
    for k, slugs in enumerate(rows):
        draw_row(fig, H, y, slugs, R, SEC, GEO, with_notes=(len(slugs) < NSLOT))
        y += ROW_H + 0.15
    fig.legend(handles=S.outcome_legend_handles(ms=5.0), loc='lower center', bbox_to_anchor=(0.5 + 0.5 * ML / FIG_W, 0.0), ncol=5,
               frameon=False, fontsize=7, handletextpad=0.3, columnspacing=1.2,
               title=None, borderaxespad=0.1).set_title('Symbol before each name: surf outcome (shape); colour = reef', prop=dict(size=7))
    out = S.save(fig, name)
    return out, SEC, GEO, R, H


def fig1():
    S.setup()
    out, SEC, GEO, R, H = build_fig1([ORDER_A, ORDER_B], 'fig1_plan_and_profiles')
    build_fig1([ORDER_A], 'fig1_plan_and_profiles_rowA')
    build_fig1([ORDER_B], 'fig1_plan_and_profiles_rowB')
    # numbers used for the caption
    rows = []
    for s in ORDER_A + ORDER_B:
        e, t = SEC[s], R[s]
        rows.append((s, e['line'], round(e['crest_depth'], 2), round(e['toe_depth'], 2), round(e['gap'], 2),
                     val(t, 'crest_depth_msl_m'), val(t, 'seabed_depth_toe_m'), val(t, 'depth_gap_m'), e['tide_name'],
                     round(e['tide_lo'], 2), round(e['tide_hi'], 2), round(GEO[s]['width'], 0), round(e['ysh'], 2)))
    json.dump(dict(scale_m_per_cm=SCALE, vertical_exaggeration=round(VE, 1), fig_height_cm=round(H, 1), rows=rows),
              open('/tmp/claude-0/paper/figsurvey/fig1_numbers.json', 'w'), indent=1)
    for r in rows:
        print(r)
    print('VE', round(VE, 1), 'H cm', round(H, 1), 'ROW_H', round(ROW_H, 2), 'SLOT_W', round(SLOT_W, 3))


# ----------------------------------------------------------------------------- figure E1 (Appendix E)
# Reef arm used for the peel angle phi0 and the assumed incident wave-crest direction, per reef (Appendix E).
# Arm line = TRUE BEARING of the arm axis (shape.json 'angles' / reefs.json arm_angle_to_shoreline_deg), turned into the plan frame
# with the seaward (shore-normal) bearing n:  plan vector = (sin(b - n), cos(b - n)), x = alongshore looking seaward, y = offshore.
# crest = direction of the assumed incident wave crest in the plan frame; status = how phi0 was obtained.
E_REEFS = {   # slug: (n seaward bearing, arm bearings [left, right looking seaward], phi0 text, status, crest rule)
    'narrowneck-gold-coast': (86.2, [104.0, 86.2], '81.1\u00b0 used (both arms)', 'assumed', 'shore'),
    'cables-reef-wa': (277.8, [128.0, 35.0], '45\u00b0 (both arms)', 'sourced', 'bisect'),
    'prattes-reef-el-segundo': (None, None, '44.7\u00b0 / 44.4\u00b0', 'derived', 'shore'),
    'mount-maunganui-reef': (46.15, [86.0, 11.0], '50.1\u00b0 / 54.9\u00b0', 'assumed', 'shore'),
    'boscombe-surf-reef': (173.4, [28.1], '72.9\u00b0', 'derived', 'boscombe'),
    'borth-coastal-defence-reef': (269.6, [63.8], '64.2\u00b0', 'assumed', 'shore'),
    'palm-beach-gold-coast': (64.3, [109.6], '44.7\u00b0', 'assumed', 'shore'),
    'bunbury-airwave': (None, None, 'no arm (dome)', 'none', None),
    'southern-ocean-surf-reef-albany': (120.3, [281.5], '71.2\u00b0', 'assumed', 'shore')}
E_ORDER = ['narrowneck-gold-coast', 'cables-reef-wa', 'prattes-reef-el-segundo', 'mount-maunganui-reef', 'boscombe-surf-reef',
           'borth-coastal-defence-reef', 'palm-beach-gold-coast', 'southern-ocean-surf-reef-albany', 'bunbury-airwave']
E_STATUS = {'assumed': 'assumed', 'sourced': 'sourced (design)', 'derived': 'derived from design drawing', 'none': ''}


def _pca_angle(P):
    c = P - P.mean(0)
    w, v = np.linalg.eigh(np.cov(c.T))
    d = v[:, np.argmax(w)]
    return math.degrees(math.atan2(d[1], d[0])) % 180.0


def _line_ang(vec):
    return math.degrees(math.atan2(vec[1], vec[0])) % 180.0


def _acute(a, b):
    d = abs(a - b) % 180.0
    return min(d, 180.0 - d)


def e_arms(slug, geo):
    """list of (centre xy, direction angle deg mod 180, half-length m) of the arm lines in the plan frame"""
    n, bearings, _, _, _ = E_REEFS[slug]
    polys = geo['polys']
    if slug == 'bunbury-airwave':
        return []
    if slug == 'narrowneck-gold-coast':      # two arm polygons = the two largest
        big = sorted(polys, key=lambda q: -abs(0.5 * np.dot(q[:, 0], np.roll(q[:, 1], -1)) - 0.5 * np.dot(q[:, 1], np.roll(q[:, 0], -1))))[:2]
        groups = sorted(big, key=lambda q: q[:, 0].mean())
    elif slug in ('cables-reef-wa', 'prattes-reef-el-segundo', 'mount-maunganui-reef'):
        allp = np.vstack(polys) if slug == 'mount-maunganui-reef' else polys[0]
        xm = allp[:, 0].mean()
        if slug == 'mount-maunganui-reef':        # the two largest polygons are the arms; others (focus bags) are ignored
            big = sorted(polys, key=lambda q: -np.ptp(q[:, 0]) * np.ptp(q[:, 1]))[:2]
            groups = sorted(big, key=lambda q: q[:, 0].mean())
        else:
            groups = [allp[allp[:, 0] < xm], allp[allp[:, 0] >= xm]]
    else:
        groups = [max(polys, key=lambda q: np.ptp(q[:, 0]) * np.ptp(q[:, 1]))]
    out = []
    for i, Pg in enumerate(groups):
        if bearings:
            b = bearings[i]
            ang = _line_ang((math.sin(math.radians(b - n)), math.cos(math.radians(b - n))))
        else:
            ang = _pca_angle(Pg)
        d = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
        c = Pg.mean(0)
        t = (Pg - c) @ d
        out.append((c, ang, 0.5 * (t.max() - t.min()), _pca_angle(Pg)))
    return out


def e_crest(slug, arms):
    """assumed incident crest line angle (deg mod 180, plan frame) and the travel vector (landward component)"""
    rule = E_REEFS[slug][4]
    if rule == 'shore':
        ang = 0.0
    elif rule == 'bisect':                   # swell nearest to shore-normal that meets both arms at the same angle
        a1, a2 = arms[0][1], arms[1][1]
        cands = [((a1 + a2) / 2) % 180.0, ((a1 + a2) / 2 + 90) % 180.0]
        cands = [c if abs(((a1 - a2 + 90) % 180) - 90) < 90 else c for c in cands]
        ang = min(cands, key=lambda c: _acute(c, 0.0))
    else:                                    # boscombe: crest bearing 101 vs shoreline 83.4 -> turned 17.6 deg clockwise
        ang = (-17.6) % 180.0
    nv = np.array([-math.sin(math.radians(ang)), math.cos(math.radians(ang))])
    if nv[1] > 0:
        nv = -nv                              # travel landward (down in the plan)
    return ang, nv


E_HW0 = 173.5                                     # half-width (m) of the common baseline scale = Albany's panel; zoom z shows E_HW0 / z
E_YSH = 28.0                                      # shoreline sits E_YSH / z m above the bottom edge, i.e. at the same height on the page in every panel
E_ZOOM = {'prattes-reef-el-segundo': 3, 'bunbury-airwave': 5}
E_BAR = {1: 50, 3: 20, 5: 10}
E_TICK = {1: 100, 3: 50, 5: 20}


def figE():
    S.setup()
    R = load_reefs()
    PR = {s: load_profile(s) for s in E_ORDER}
    SEC = {s: section_data(s, R, PR[s]) for s in E_ORDER}
    GEO = {s: plan_geometry(s, SEC[s]) for s in E_ORDER}
    W_CM, H_CM = 17.0, 22.95
    fig = plt.figure(figsize=(W_CM * S.CM, H_CM * S.CM))
    PW, PH, TOP, LEFT, GX, GY = 4.85, 5.8, 1.15, 1.05, 0.30, 1.25
    checks = {}
    for k, slug in enumerate(E_ORDER):
        r, c = divmod(k, 3)
        x0 = LEFT + c * (PW + GX)
        y0 = TOP + r * (PH + GY)
        g, sec, col = GEO[slug], SEC[slug], COLORS[slug]
        allp = np.vstack(g['polys'])
        vmax = max(allp[:, 1].max(), g['section'][:, 1].max())
        z = E_ZOOM.get(slug, 1)
        hw = E_HW0 / z
        sc = PW / (2 * hw)                                   # cm per m (same in x and y; = z x the baseline scale)
        ybot = -E_YSH / z
        ytop = ybot + PH / sc
        ylo_r, yhi_r = min(allp[:, 1].min(), g['section'][:, 1].min()), max(vmax, g['section'][:, 1].max())
        assert yhi_r + 4 / z <= ytop, slug     # reef must fit the common window: no axis breaks
        strips = [(0.0, PH, ybot, ytop)]
        axs = []
        for (b0, b1, ya, yb) in strips:
            ax = fig.add_axes([x0 / W_CM, 1 - (y0 + PH - b0) / H_CM, PW / W_CM, (b1 - b0) / H_CM])
            ax.set_xlim(-hw, hw)
            ax.set_ylim(ya, yb)
            ax.set_aspect('equal', adjustable='box')      # 1 m in x = 1 m in y on paper (window sizes are chosen to match, so the box is unchanged)
            ax.axhspan(0, 1e4, color=S.SEA, lw=0, zorder=0)
            ax.axhspan(-1e4, 0, color=S.SAND, lw=0, zorder=0)
            ax.axhline(0, color='#6B5B3A', lw=1.0, zorder=2)
            ax.set_xticks([])
            for sp in ('left', 'bottom', 'top', 'right'):
                ax.spines[sp].set_visible(sp == 'left')
            ax.tick_params(labelsize=6.5)
            axs.append(ax)
        lo_ax, top_ax = axs[0], axs[-1]
        step = E_TICK[z]
        for ax_, (_, _, ya_, yb_) in zip(axs, strips):
            ax_.set_yticks([t for t in range(0, 500, step) if ya_ - 1e-6 <= t <= yb_ + 1e-6])
        lo_ax.text(-hw + 4 / z, -14 / z, 'shoreline', fontsize=7, color='#5A4A2A', va='center', ha='left', zorder=5)
        arms = e_arms(slug, g)
        for ax in axs:
            for kk, P in enumerate(g['polys']):
                oval = slug == 'borth-coastal-defence-reef' and kk == 1
                ax.add_patch(Polygon(P, closed=True, fc=col, ec=darker(col), lw=0.5, alpha=0.5 if oval else 0.85, hatch='////' if oval else None, zorder=4))
            if slug == 'bunbury-airwave':
                ax.plot([0], [sec['crest_d']], 'o', ms=9 * (1 if z == 1 else 1.0), mfc='none', mec=darker(col), mew=0.6, zorder=3)
            ax.plot(g['section'][:, 0], g['section'][:, 1], color='black', lw=0.9, ls=(0, (3, 1.6)), zorder=7)
            for (cen, ang, hl, pca) in arms:
                d = np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))])
                a0, a1 = cen - d * (hl + 6 / z), cen + d * (hl + 6 / z)
                ax.plot([a0[0], a1[0]], [a0[1], a1[1]], color='white', lw=3.0, zorder=8, solid_capstyle='butt')
                ax.plot([a0[0], a1[0]], [a0[1], a1[1]], color='#1A1A1A', lw=1.5, zorder=9, solid_capstyle='butt')
        mid = g['section'][0]
        lab_main = 'main cut\n(Fig. 1)'
        if slug == 'southern-ocean-surf-reef-albany':
            lab_main = 'ride-section cut\n(main, Fig. 1)'
            s2 = dict(sec)
            s2['run_xy'] = PR[slug]['lines']['crest_line_auto']['reef_run_xy_m']
            s2['dirv'] = [0.0, 1.0]
            g2 = plan_geometry(slug, s2)
            top_ax.plot(g2['section'][:, 0], g2['section'][:, 1], color='#C0392B', lw=1.0, ls=(0, (1, 1.3)), zorder=7)
            top_ax.text(g2['section'][0][0] - 4, g2['section'][0][1] - 4, 'take-off peak cut\n(second cut, Fig. 4)', fontsize=6.3, color='#C0392B',
                        ha='right', va='top', zorder=8)
            checks['albany_takeoff_xy'] = g2['section'].tolist()
        lab_ax = top_ax
        if slug == 'bunbury-airwave':
            lab_ax.text(mid[0] - 5 / z, mid[1] - 2 / z, lab_main, fontsize=6.3, color='black', ha='right', va='top', zorder=8)
        else:
            lab_ax.text(mid[0] + (36 if slug == 'southern-ocean-surf-reef-albany' else 4 / z), mid[1] - 4 / z, lab_main, fontsize=6.3, color='black', ha='left', va='top', zorder=8)
        if arms:
            ang_c, nv = e_crest(slug, arms)          # assumed crest, kept for the phi0 checks only (not drawn)
            checks[slug] = dict(arm_angle_to_shoreline=[round(_acute(a[1], 0.0), 1) for a in arms], arm_pca=[round(_acute(a[3], 0.0), 1) for a in arms],
                                crest_to_shoreline=round(_acute(ang_c, 0.0), 1), phi_drawn=[round(_acute(a[1], ang_c), 1) for a in arms],
                                swell_off_shorenormal=round(math.degrees(math.atan2(abs(nv[0]), abs(nv[1]))), 1))
        # scale bar (shoreline strip)
        L = E_BAR[z]
        lo_ax.plot([hw - 8 / z - L, hw - 8 / z], [-18 / z] * 2, color='black', lw=1.6, solid_capstyle='butt', zorder=9)
        lo_ax.text(hw - 8 / z - L / 2, -14 / z, '%d m' % L, fontsize=6.3, ha='center', va='bottom')
        # header
        phi, status = E_REEFS[slug][2], E_STATUS[E_REEFS[slug][3]]
        tr = top_ax.transAxes
        # header positions are relative to the whole panel, so place them in figure coordinates
        def fx(u): return (x0 + u * PW) / W_CM
        def fy(v): return 1 - (y0 + PH - v * PH) / H_CM          # v in panel fractions (1 = top)
        mk = S.marker_kw(slug, ms=4.6)
        fig.add_artist(Line2D([fx(0.03)], [fy(1 + 0.68 / PH)], transform=fig.transFigure, **mk))
        fig.text(fx(0.08), fy(1 + 0.5 / PH), NAMES[slug], fontsize=7.8, fontweight='bold', va='bottom', ha='left', color=darker(col, 0.8))
        fig.text(fx(0.0), fy(1 + 0.16 / PH), 'φ$_0$ ' + phi + (', ' + status if status else ''), fontsize=6.8, va='top', ha='left',
                 color=('#B03A2E' if E_REEFS[slug][3] == 'assumed' else S.INK2))
        if z > 1:
            top_ax.text(0.98, 0.97, '%d× zoom' % z, transform=tr, fontsize=7.2, fontweight='bold', color=S.INK, ha='right', va='top', zorder=12)
        if c == 0:
            fig.text((x0 - 0.75) / W_CM, fy(0.5), 'Distance offshore (m)', fontsize=7, rotation=90, va='center', ha='center')
    # legend strip
    h = [Line2D([], [], color='black', lw=0.9, ls=(0, (3, 1.6)), label='main profile cut (Figure 1; Figures 4, 5, 7-9)'),
         Line2D([], [], color='#C0392B', lw=1.0, ls=(0, (1, 1.3)), label='second cut kept in Figure 4 (Albany only)'),
         Line2D([], [], color='#1A1A1A', lw=1.5, label='reef arm used for the peel angle φ$_0$')]
    fig.legend(handles=h, loc='lower left', bbox_to_anchor=(0.02, 0.0), ncol=2, frameon=False, fontsize=6.8, columnspacing=1.2,
               labelspacing=0.3, handlelength=2.2)
    fig.text(0.02, 0.95 / H_CM, 'Plan view looking seaward (seaward up, north not up). Red φ$_0$ = assumed value.\n'
             'Every panel uses the axis ranges of the Albany panel (1×, bar = 50 m) divided by its zoom factor; labelled panels are zoomed by that factor, bar as marked.\n'
             'The shoreline (y = 0) is at the same height in every panel; no panel has an axis break.',
             fontsize=6.5, color=S.INK2, ha='left', va='bottom')
    out = S.save(fig, 'figE_lines_per_reef')
    for k_, v_ in checks.items():
        print(k_, v_)
    return out, SEC, GEO


# ----------------------------------------------------------------------------- figure 2
ORDER_ALL = ['burkitts-reef-bargara', 'cables-reef-wa', 'narrowneck-gold-coast', 'prattes-reef-el-segundo', 'mount-maunganui-reef',
             'opunake-reef', 'boscombe-surf-reef', 'kovalam-reef-india', 'borth-coastal-defence-reef', 'palm-beach-gold-coast',
             'bunbury-airwave', 'southern-ocean-surf-reef-albany', 'mexico-reef-2026-unnamed']
OPEN_KEYS = ('LOW', 'LAT', 'bounding rectangle', 'photo trace', 'not confirmed', 'both mounds')
OPEN_OVERRIDE = {('borth-coastal-defence-reef', 'footprint_area_m2')}
F2_COLS = [  # field, header, log?, xlim, ticks, fmt
    ('plan_length_alongshore_m', 'Plan length\nalongshore (m)', False, (0, 215), [0, 100, 200], '{:.0f}'),
    ('footprint_area_m2', 'Footprint\narea (m²)', True, (60, 40000), [100, 1000, 10000], '{:,.0f}'),
    ('volume_m3', 'Volume\n(m³, as stated)', True, (60, 400000), [100, 1000, 10000, 100000], '{:,.0f}'),
    ('crest_depth_msl_m', 'Crest depth\nbelow MSL (m)', False, (-0.7, 3.6), [0, 1, 2, 3], '{:.2f}'),
    ('depth_gap_m', 'Depth gap\ntoe − crest (m)', False, (0, 8.6), [0, 2, 4, 6, 8], '{:.1f}')]


def fig2():
    S.setup()
    R = load_reefs()
    n = len(ORDER_ALL)
    LAB_W, GAPX = 3.75, 0.28
    pw = (FIG_W - LAB_W - MR - 4 * GAPX) / 5
    ROWH, HEAD, FOOT = 0.50, 0.85, 2.25
    H = HEAD + n * ROWH + FOOT
    fig = plt.figure(figsize=(FIG_W * S.CM, H * S.CM))

    def axes_cm(x, ytop, w, h):
        return fig.add_axes([x / FIG_W, 1 - (ytop + h) / H, w / FIG_W, h / H])
    ylim = (n - 0.5, -0.5)
    # label column
    axl = axes_cm(0.05, HEAD, LAB_W, n * ROWH)
    axl.set_xlim(0, 1)
    axl.set_ylim(*ylim)
    axl.axis('off')
    for i, s in enumerate(ORDER_ALL):
        if i % 2 == 0:
            axl.axhspan(i - 0.5, i + 0.5, color='#F3F3F3', lw=0, zorder=0, clip_on=False, xmin=0, xmax=1)
        r = R[s]
        axl.plot([0.05], [i], clip_on=False, **S.marker_kw(s, ms=4.8))
        axl.text(0.14, i, NAMES[s], fontsize=7.5, fontweight='bold', va='center', ha='left', color=darker(COLORS[s], 0.8))
        axl.text(0.945, i, str(val(r, 'year_built')), fontsize=7, va='center', ha='right', color=S.INK2)
    stats = {}
    for c, (f, head, islog, xl, ticks, fmt) in enumerate(F2_COLS):
        ax = axes_cm(LAB_W + c * (pw + GAPX), HEAD, pw, n * ROWH)
        ax.set_ylim(*ylim)
        data_frac = 0.64     # left part of the panel = data, right part = value column
        full = xl[0] * (xl[1] / xl[0]) ** (1 / data_frac) if islog else xl[0] + (xl[1] - xl[0]) / data_frac
        ax.set_xlim(xl[0], full)
        if islog:
            ax.set_xscale('log')
        ax.spines['bottom'].set_bounds(xl[0], xl[1])
        for i in range(n):
            if i % 2 == 0:
                ax.axhspan(i - 0.5, i + 0.5, color='#F3F3F3', lw=0, zorder=0)
        for tk in ticks:
            ax.axvline(tk, color=S.GRID, lw=0.5, zorder=1)
        if f == 'crest_depth_msl_m':
            ax.axvline(0, color='#2B5F8A', lw=0.8, ls=(0, (4, 2)), zorder=2)
        ax.set_yticks([])
        ax.set_xticks(ticks)
        if islog:
            keep = {'footprint_area_m2': (100, 1000, 10000), 'volume_m3': (100, 10000)}[f]
            ax.set_xticklabels([('$10^{%d}$' % round(math.log10(tk))) if tk in keep else '' for tk in ticks])
        else:
            ax.set_xticklabels(['{:g}'.format(tk) for tk in ticks])
        ax.tick_params(axis='x', length=2.2, pad=1.5)
        ax.spines['left'].set_visible(False)
        ax.set_title(head, fontsize=7.5, fontweight='bold', va='bottom', pad=3, linespacing=1.1)
        x0 = xl[0]
        for i, s in enumerate(ORDER_ALL):
            rec = R[s][f]
            v = rec['value']
            if v is None or rec['status'] == 'unknown':
                ax.text(full, i, 'unknown', fontsize=7, style='italic', color=S.UNKNOWN, va='center', ha='right')
                continue
            op = any(k in rec.get('unit', '') for k in OPEN_KEYS) or rec['status'] == 'assumed' or (s, f) in OPEN_OVERRIDE
            col = COLORS[s]
            base = xl[0] if islog else 0
            ax.plot([base, v], [i, i], color=col, lw=0.8, alpha=0.55, zorder=3, solid_capstyle='butt')
            kw = S.marker_kw(s, ms=4.8)
            if op and S.OUTCOME.get(s) != 'unknown':      # low confidence = light (half-tone) fill; unknown outcome stays hollow
                kw.update(mfc=lighter(col), mec=col, mew=0.9)
            ax.plot([v], [i], zorder=4, clip_on=False, **kw)
            lab = fmt.format(v).replace('-', '−')
            ax.text(full, i, lab, fontsize=7, va='center', ha='right', color=S.INK2 if op else S.INK, zorder=5)
            stats[(s, f)] = v
    # footnote / key
    yk = H - 0.95
    fig.text(0.05 / FIG_W, 1 - (H - 1.72) / H,
             'Rows in order of construction start (year at right of name); numbers at the right of each panel are the plotted values. Colour and name = reef;\n'
             'symbol shape = surf outcome (legend below). Solid fill: sourced or derived from traced geometry; light fill: assumed, low-confidence or not directly\n'
             'comparable (photo trace, bounding rectangle, both mounds at Borth, LAT datum at Opunake); "unknown" value: not found in any source checked.',
             fontsize=7, va='top', ha='left', color=S.INK2, linespacing=1.3)
    fig.legend(handles=S.outcome_legend_handles(ms=5.0), loc='lower left', bbox_to_anchor=(0.05 / FIG_W, 0.0), ncol=5, frameon=False,
               fontsize=7, handletextpad=0.3, columnspacing=1.2, title='Surf outcome (symbol shape)', title_fontsize=7, alignment='left')
    S.save(fig, 'fig2_reef_size_overview')
    print('fig2 height cm', round(H, 1), 'plot rows', n)


# ----------------------------------------------------------------------------- appendix figure B: 3D gallery
GALLERY = [  # slug, preview file, crop box (x0, y0, x1, y1) in the 1400 x 900 px preview (viewer panels excluded), model version label
    ('cables-reef-wa', 'preview_oblique.png', (110, 175, 910, 727), 'surveyed surface, Nov 1999'),
    ('narrowneck-gold-coast', 'preview_oblique.png', (10, 160, 1010, 850), 'renewed reef, 2020 photo outline'),
    ('prattes-reef-el-segundo', 'preview_plan.png', (350, 275, 1070, 772), 'Phase I as installed, Sept 2000 (plan view)'),
    ('mount-maunganui-reef', 'preview_plan.png', (307, 160, 1001, 639), '2013 multibeam outline (plan view)'),
    ('boscombe-surf-reef', 'preview_oblique.png', (490, 480, 990, 825), 'as built 2009, idealised loft'),
    ('borth-coastal-defence-reef', 'preview_oblique.png', (0, 150, 1011, 847), '2022 LiDAR outline'),
    ('palm-beach-gold-coast', 'preview_oblique.png', (310, 200, 1210, 821), 'as built 2019'),
    ('bunbury-airwave', 'preview_oblique.png', (130, 307, 690, 693), 'Dec 2019 bladder, cap stand-in'),
    ('southern-ocean-surf-reef-albany', 'preview_oblique.png', (55, 255, 855, 807), 'Bluecoast final design (VE 2x)')]
TILE_ASPECT = 1.45


def figB():
    from PIL import Image
    S.setup()
    R = load_reefs()
    gx, tile_w = 0.2, (FIG_W - 0.4 - 2 * 0.15) / 3
    tile_h = tile_w / TILE_ASPECT
    lab_h = 0.62
    H = 0.15 + 3 * (tile_h + lab_h)
    fig = plt.figure(figsize=(FIG_W * S.CM, H * S.CM))
    for k, (slug, fname, box, ver) in enumerate(GALLERY):
        row, colm = divmod(k, 3)
        x = gx + colm * (tile_w + 0.15)
        ytop = 0.1 + row * (tile_h + lab_h)
        ax = fig.add_axes([x / FIG_W, 1 - (ytop + tile_h) / H, tile_w / FIG_W, tile_h / H])
        im = Image.open(os.path.join(S.SHAPES, slug, '3d', fname)).convert('RGB').crop(box)
        ax.imshow(np.asarray(im), aspect='auto', interpolation='lanczos')
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(True)
            sp.set_linewidth(0.6)
            sp.set_color(S.INK2)
        lab = fig.add_axes([x / FIG_W, 1 - (ytop + tile_h + lab_h) / H, tile_w / FIG_W, lab_h / H])
        lab.axis('off')
        lab.set_xlim(0, 1)
        lab.set_ylim(0, 1)
        lab.plot([0.035], [0.70], **S.marker_kw(slug, ms=4.8))
        lab.text(0.08, 0.70, '(%s) %s, %s' % ('abcdefghi'[k], NAMES[slug], year_label(R[slug])), fontsize=7.5, fontweight='bold', va='center', ha='left',
                 color=darker(COLORS[slug], 0.8))
        lab.text(0.08, 0.24, ver, fontsize=7, va='center', ha='left', color=S.INK2)
    S.save(fig, 'figB_3d_gallery')
    print('figB height cm', round(H, 1), 'tile', round(tile_w, 2), 'x', round(tile_h, 2))


# ----------------------------------------------------------------------------- captions
def write_captions():
    ve = int(round(VE))
    c1 = (
        "**Figure 1.** Plan shapes (upper part of each row) and cross-shore depth profiles (lower part) of the nine surf reefs whose outline is known, "
        "in order of construction; Opunake, Kovalam, Burkitts and Xala (Mexico) are not drawn because no outline could be traced. "
        "All plans share one metric scale in x and y (1 cm = %d m at print width; 100 m bar at lower right), are viewed looking seaward (unmirrored), and each "
        "outline is set at its distance from the MSL shoreline (thick line, y = 0) with arbitrary alongshore slots; the hatched shape is Borth's southern oval, a "
        "shore-parallel breakwater rather than a surf reef, and Bunbury is the 12 m Airwave bladder, torn on installation. "
        "Each profile is the section of the 3D reconstruction marked by the dashed line (the section whose crest depth best matches the master table), drawn at the "
        "plan's horizontal scale (window shifted per reef) with a vertical exaggeration of about %d:1; elevations are relative to MSL, the blue band is the tide "
        "range (spring range MLWS-MHWS; great diurnal range MLLW-MHHW at Pratte's; predicted annual range, about LAT-HAT, of the 2026 WA DoT/BoM predictions at Cables 1.14 m, Bunbury 1.20 m and Albany 1.38 m, centred on MSL; see the tide-range table in Appendix C), and C, T and G are the crest depth, the seabed "
        "depth at the seaward toe and the depth gap (T - C) read from the plotted section, within 0.35 m of the master-table values."
        % (SCALE, ve))
    n1 = (
        "\n\n---\nBuild and data notes (not part of the caption)\n"
        "- Files: `fig1_plan_and_profiles` (both rows, 17 x 22.6 cm); the same rows separately as `fig1_plan_and_profiles_rowA` and `_rowB` (17 x 11.3 cm each) if a full page is too tall. Code: `08_paper/analysis/figures_survey.py` (function `fig1`), palette in `08_paper/analysis/style.py`.\n"
        "- Plan outlines: DEFAULT outline of each `07_scale/shapes/<slug>/shape.json` (Cables: original design plan of Lyons 1992 as reproduced in Blacka et al. 2013 Fig. A.2, fitted to the Nov 1999 soundings; Narrowneck: container field on the Esri image of 8 Aug 2020; Pratte's: Skelly Engineering design drawing of the Phase I layout; Mount Maunganui: -2.0 m CD contour of the 18 Jul 2013 multibeam survey; Boscombe: outline traced on Esri World Imagery Wayback imagery (frame origin = surf line of 28 Sep 2011); Borth: Welsh Government LiDAR edge of 19 Mar 2022; Palm Beach: toe outline traced on the Bluecoast/Nearmap aerial of the completed reef; Bunbury: 12 m circle traced from the 2019 drone photo, orientation arbitrary; Albany: Bluecoast final-design outline). Per-reef sources and confidence: Appendix A, `shape.json` and `08_paper/data/profiles/<slug>.json`.\n"
        "- Frame: every `shape.json` frame is 'x alongshore, y offshore' with +y = +x turned 90 deg clockwise, so x is plotted as -x to give an unmirrored view looking seaward; the Cables frame has the other handedness (x north, y west) and its outline is rotated into the fitted 0 m AHD shoreline (bearing 7.8 deg; 254 m east of the anchor, `geo` block of its `shape.json`), so the axes there are exactly shore-parallel and shore-normal. Distance offshore = model y minus the model y at which the section's seabed crosses MSL (`y_msl_crossing_m`: Borth 90.6 m, Boscombe -8.0 m, Narrowneck -5.0 m, Albany -5.3 m, Bunbury 3.2 m; Cables: fitted shoreline, 3.1 m; Prattes, Mount Maunganui and Palm Beach 0). Shoreline definitions differ by reef (MSL waterline of an aerial image, wet/dry sand edge, back-of-beach line at Borth; `data/README.md`); differences below 30 m are noise. DERIVED.\n"
        "- Sections: `08_paper/data/profiles/<slug>.json`, lines: Cables crest_line, Narrowneck second_crest_line (south arm), Pratte's centreline (apex), Mount Maunganui second_crest_line, Boscombe crest_line, Borth centreline (northern reef), Palm Beach crest_line, Bunbury crest_line, Albany crest_line. Chosen as the line whose crest depth is closest to `crest_depth_msl_m` of `reefs.json`. The Cables section follows the design-frame y axis, about 17.5 deg off the shore normal (distances along the line, not shore-normal). Seabed under the reefs is interpolated except at Cables (1998 pre-construction survey); crest height and ramp slopes inherit the 3D-model assumptions (profiles/SUMMARY.md section 6). Datums: each model uses z = 0 at MSL with the conversions listed in `data/README.md` (Boscombe, Albany and Prattes depend on stated assumptions).\n"
        "- Tide band planes from the profile JSONs (`tidal_planes_m_above_msl`); the Cables, Bunbury and Albany bands (`ANN_LO`/`ANN_HI`) are the predicted annual range of the WA Department of Transport / BoM *Tide Predictions by Location WA 2026* (heights above LAT; Fremantle +0.30 to +1.44 m, Bunbury +0.10 to +1.30 m, Albany +0.09 to +1.47 m), centred on MSL; three of four quarterly blocks were parsed, so they are lower bounds. They replace the earlier Cables +-0.4 m (Blacka et al. 2013 Table 4.3, definition not given) and the Bunbury/Albany MHHW-MLLW bands (0.4 and 0.6 m). Pratte's band is the NOAA great diurnal range (GT 1.654 m). Verification: `08_paper/notes/tides_check.md`.\n"
        "- Annotated C, T, G versus master table (max difference): C 0.27 m (Borth, Pratte's), T 0.32 m (Palm Beach), G 0.32 m (Palm Beach).\n")
    c2 = (
        "**Figure 2.** Size overview of the 13 surf-reef projects (in order of construction): plan length along the shore and footprint area of the traced outline, "
        "volume as stated by the sources (rock or sand fill, not one common quantity), crest depth below MSL (negative: crest above MSL, Borth) and depth gap between the seabed at the "
        "seaward toe and the crest. Open symbols mark assumed, low-confidence or not directly comparable values and 'unknown' means that no source checked gives the value; "
        "the four reefs without a traced shape (Opunake, Kovalam, Burkitts, Xala) therefore have no length or footprint. "
        "Values are those of the master table `08_paper/data/reefs.json` (sources and status of every value in Appendix C; reading of the outlines and 3D models in Appendix A; "
        "main sources include Blacka et al., 2013; Mead and Borrero, 2011; Rendle, 2016; Corbett et al., 2023); lengths, areas, crest depths and gaps are derived from "
        "traced outlines and 3D models, volumes are sourced except Borth and Bunbury (derived)."
        "\n\n---\nBuild notes (not part of the caption): code `08_paper/analysis/figures_survey.py` (function `fig2`). Opunake gap (3.0 m) is relative to chart datum (LAT), design stage, and is plotted open. "
        "Borth footprint and length include the southern oval (both mounds). Narrowneck volume (70,000 m3) is the stated sand-fill volume, the footprint is the visible container field of 2020 (lower bound).\n")
    cb = (
        "**Figure B1.** Three-dimensional reconstructions of the nine modelled reefs (default version of each model; screenshots of the interactive viewer, panels cropped away). "
        "These are reconstructions, not photographs or surveys: each combines a traced or designed outline, a surveyed or inferred seabed, crest levels from design or survey documents "
        "and the local tidal planes, and its confidence differs by reef; the inputs, sources and assumptions of every model are listed per reef in Appendix A. "
        "Tiles are not at a common scale (use the scale bars and labels inside each tile); views are oblique except (c) and (d), which are plan views because the oblique preview was cut by the viewer panels; vertical scale is true except (i) with 2x exaggeration."
        "\n\n---\nBuild notes (not part of the caption): source images `07_scale/shapes/<slug>/3d/preview_oblique.png` (Pratte's and Mount Maunganui: `preview_plan.png`), cropped to the 3D viewport "
        "(crop boxes in `figures_survey.py`, `GALLERY`); the text labels inside the tiles come from the viewer. Plan previews for the other reefs are not used because Figure 1 shows their plan shapes.\n")
    for name, txt in (('fig1_plan_and_profiles', c1 + n1), ('fig2_reef_size_overview', c2), ('figB_3d_gallery', cb)):
        fp = os.path.join(S.FIG_DIR, name + '.caption.md')
        if os.path.exists(fp):        # LEGACY first-draft texts: never overwrite the hand-maintained captions (surf cuts, outcome shapes)
            print('caption exists, not overwritten:', fp)
            continue
        open(fp, 'w', encoding='utf-8').write(txt)



if __name__ == '__main__':
    todo = sys.argv[1:] or ['fig1', 'fig2', 'figB']   # captions are maintained by hand in figures/*.caption.md (since 2026-10-19)
    for t in todo:
        globals()[t]()

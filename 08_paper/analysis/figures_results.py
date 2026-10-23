#!/usr/bin/env python3
"""figures_results.py - result figures F4-F9 of the surf-reef review (Figures 4-9; Figure 3 is figures_wave.py).

  python3 -I 08_paper/analysis/figures_results.py            # all of them
  python3 -I 08_paper/analysis/figures_results.py fig4 fig6  # a selection

Writes into 08_paper/figures/: fig4_gap_ramp, fig5_peel_skill, fig6_volume_outcome, fig7_tide_window, fig8_stability,
fig9_haifa_envelope (.png 300 dpi + .pdf). Captions are in <name>.caption.md (written by hand from RESULTS.md).
Inputs (read only): the results_*.csv / .json files of 08_paper/analysis (made by run_all.py), wavelib.py (Hutt table, Airy
formulas), 08_paper/data/profiles/<slug>.json (Albany centreline), style.py (palette). Every plotted number comes from those
files; the text annotations quote them (rho, p, volumes).
"""
import json
import math
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import style as S  # noqa: E402
import wavelib as W  # noqa: E402
from style import COLORS, INK, INK2, MARKERS, NAMES, UNKNOWN, GRID  # MARKERS = outcome shape per reef  # noqa: E402

import matplotlib.colors as mcolors  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def rd(name):
    return pd.read_csv(os.path.join(HERE, name))


def rj(name):
    return json.load(open(os.path.join(HERE, name), encoding='utf-8'))


def darken(c, f=0.65):
    r, g, b = mcolors.to_rgb(c)
    return (r * f, g * f, b * f)


def outcome_kind(o):
    """works -> full; works rarely / mixed -> half; does not work -> open + x; unknown -> grey (FIGURE_SPECS scheme)."""
    if not isinstance(o, str):
        return 'unknown'
    if o.startswith('works rarely') or o.startswith('mixed'):
        return 'half'
    if o == 'works':
        return 'full'
    if o.startswith('does not'):
        return 'no'
    return 'unknown'


def pt(ax, slug, x, y, outcome, ms=6.0, z=6, ghost=False):
    """One reef marker: colour = reef (style.py), SHAPE = outcome class (style.OUTCOME_MARKER; unknown = small hollow square)."""
    kw = S.marker_kw(slug, ms=ms, outcome=outcome)
    if ghost:
        kw.update(mfc='none', mec=COLORS[slug], mew=0.8, ms=kw['ms'] * 0.8)
        ax.plot([x], [y], zorder=z - 1, alpha=0.75, **kw)
        return
    ax.plot([x], [y], zorder=z, **kw)


def outcome_legend_handles():
    return S.outcome_legend_handles()


def reef_label(ax, slug, x, y, dx, dy, ha='left', va='center', text=None, fs=7, z=7):
    """direct label in the reef's own colour (darkened for contrast), white halo"""
    import matplotlib.patheffects as pe
    t = ax.annotate(text or NAMES[slug], (x, y), xytext=(dx, dy), textcoords='offset points', fontsize=fs, ha=ha, va=va,
                    color=darken(COLORS[slug], 0.8), fontweight='bold', zorder=z)
    t.set_path_effects([pe.withStroke(linewidth=2.2, foreground='white')])
    return t


def halo_text(ax, x, y, s, **kw):
    import matplotlib.patheffects as pe
    t = ax.text(x, y, s, **kw)
    t.set_path_effects([pe.withStroke(linewidth=2.2, foreground='white')])
    return t


def rho_text(corr, key):
    c = corr[key]
    return c['spearman_rho'], c['p_permutation']


# ====================================================================================================== F4
def ray_angle(ax, x, y, factor=1.3):
    """Display angle (deg) of a line of constant slope y = x / X through (x, y) on log-log axes."""
    p0 = ax.transData.transform((x, y))
    p1 = ax.transData.transform((x * factor, y * factor))
    return math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))


def fig4():
    S.setup()
    summ = rd('results_reef_summary.csv').set_index('slug')
    corr = rj('results_outcome_correlations.json')['corr']
    alb = json.load(open(os.path.join(S.DATA_DIR, 'profiles', 'southern-ocean-surf-reef-albany.json'), encoding='utf-8'))
    am = alb['lines'].get('crest_line_auto', alb['lines']['centreline'])['metrics']   # old automatic cut (take-off plateau)
    fig = plt.figure(figsize=(S.cm(14.5), S.cm(13.2)))
    ax = fig.add_axes([0.085, 0.315, 0.905, 0.67])
    xlim, ylim = (0.7, 300.0), (0.9, 10.0)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    xs = np.logspace(math.log10(xlim[0]), math.log10(xlim[1]), 200)
    # Mead (2000) Eq. 6.5, Y = 0.065 X + 0.821: X at the class limits Y = 1.6, 1.9, 2.5, 3.1 (gap / length = 1 / X)
    Xs = [(1.6 - 0.821) / 0.065, (1.9 - 0.821) / 0.065, (2.5 - 0.821) / 0.065, (3.1 - 0.821) / 0.065]   # 12.0, 16.6, 25.8, 35.1
    shades = ['#C4C4C4', '#D6D6D6', '#E6E6E6', '#F2F2F2', '#FAFAFA']
    edges = [0.0] + Xs + [1e9]
    for i in range(5):
        y_top = np.full_like(xs, ylim[1]) if i == 0 else xs / edges[i]
        y_bot = np.full_like(xs, ylim[0] / 10) if i == 4 else xs / edges[i + 1]
        ax.fill_between(xs, y_bot, np.minimum(y_top, ylim[1] * 5), color=shades[i], lw=0, zorder=0)
    for X in Xs:
        ax.plot(xs, xs / X, color='#8F8F8F', lw=0.5, zorder=1)
    # Iribarren limits at a typical swell: tan(beta) = xi sqrt(H / L0), H = 1 m
    for T, ls, col in ((10, (0, (4, 2)), '#1B5E87'), (7, (0, (1.5, 1.5)), '#B03A2E')):
        L0 = float(W.L0(T))
        for xi in (0.4, 2.0):
            Xl = 1.0 / (xi * math.sqrt(1.0 / L0))
            ax.plot(xs, xs / Xl, color=col, lw=0.9, ls=ls, zorder=2)
    # band labels: slope 1:X of each class limit, written along its diagonal near the top edge
    for X, nm in zip(Xs, ['Y = 1.6', 'Y = 1.9', 'Y = 2.5', 'Y = 3.1']):
        yl = 8.6
        xl = yl * X
        if xl < xlim[1] * 0.8:
            ang = ray_angle(ax, xl, yl)
            ax.text(xl, yl, '1:%.0f' % X, fontsize=6.3, color='#6F6F6F', rotation=ang, rotation_mode='anchor', ha='right',
                    va='bottom', zorder=3)
    band_mid = [(1.6, 'collapsing /\nbeyond extreme'), (math.sqrt(Xs[0] * Xs[1]), 'extreme'), (math.sqrt(Xs[1] * Xs[2]), 'very high\n/ high'),
                (math.sqrt(Xs[2] * Xs[3]), 'medium'), (60.0, 'gentle')]
    for X, nm in band_mid:
        yb = 1.25
        xb = yb * X
        if xlim[0] < xb < xlim[1]:
            ax.text(xb, yb, nm, fontsize=6.3, color='#5A5A5A', rotation=ray_angle(ax, xb, yb), rotation_mode='anchor', ha='center',
                    va='center', zorder=3, style='italic')
    ax.text(0.012, 0.985, 'Each diagonal = one constant ramp slope \u0394h / L.\nBreaking intensity depends on the slope only,\n'
            'so its zones are parallel diagonal bands:\nsteeper (upper left) = more intense, plunging/\ncollapsing; '
            'gentler (lower right) = spilling.', transform=ax.transAxes, fontsize=6.5, color=INK, ha='left', va='top', zorder=8,
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=GRID, lw=0.5))
    order = ['narrowneck-gold-coast', 'palm-beach-gold-coast', 'cables-reef-wa', 'mount-maunganui-reef',
             'prattes-reef-el-segundo', 'boscombe-surf-reef', 'borth-coastal-defence-reef', 'bunbury-airwave',
             'southern-ocean-surf-reef-albany']
    off = {  # label offset in points (dx, dy, ha, va)
        'narrowneck-gold-coast': (8, 0, 'left', 'center'), 'palm-beach-gold-coast': (-7, 5, 'right', 'bottom'),
        'cables-reef-wa': (8, 3, 'left', 'bottom'), 'mount-maunganui-reef': (8, 0, 'left', 'center'),
        'prattes-reef-el-segundo': (8, 0, 'left', 'center'), 'boscombe-surf-reef': (-8, 0, 'right', 'center'),
        'borth-coastal-defence-reef': (-7, -2, 'right', 'top'), 'bunbury-airwave': (-8, 0, 'right', 'center'),
        'southern-ocean-surf-reef-albany': (9, 0, 'left', 'center')}
    for s in order:
        r = summ.loc[s]
        x, y = r.rep_ramp_length_m, r.rep_depth_gap_m
        # one cut per reef (Lior 2026-10-19): the Narrowneck north-arm tip cut and Pratte's tip cut were dropped (no surf meaning)
        pt(ax, s, x, y, r.outcome, ms=6.8)
        dx, dy, ha, va = off[s]
        reef_label(ax, s, x, y, dx, dy, ha=ha, va=va, text=('Albany: ride\nsection (main\ncut, Fig. 1)' if s == 'southern-ocean-surf-reef-albany' else None))
    s = 'southern-ocean-surf-reef-albany'                                      # Albany take-off peak (secondary cut, kept: clear meaning)
    xa, ya = am['ramp_length_m'], am['crest_to_toe_seabed_drop_m']
    ax.plot([summ.loc[s].rep_ramp_length_m, xa], [summ.loc[s].rep_depth_gap_m, ya], color=COLORS[s], lw=0.6, zorder=3, alpha=0.8)
    pt(ax, s, xa, ya, 'works', ghost=True)
    reef_label(ax, s, xa, ya, 6, 2, ha='left', va='bottom', text='Albany: take-off peak\n(offshore plateau)', fs=6.5)
    ax.set_xlabel('Ramp length L, from the seaward edge of the crest to the seaward toe (m, log scale)')
    ax.set_ylabel('Depth gap \u0394h = toe bed depth \u2212 crest depth (m, log scale)')
    ax.set_xticks([1, 2, 5, 10, 20, 50, 100, 200])
    ax.set_xticklabels(['1', '2', '5', '10', '20', '50', '100', '200'])
    ax.set_yticks([1, 2, 3, 4, 5, 6, 8, 10])
    ax.set_yticklabels(['1', '2', '3', '4', '5', '6', '8', '10'])
    ax.minorticks_off()
    rg, pg = rho_text(corr, 'rep_depth_gap_m')
    rl, pl = rho_text(corr, 'ramp_length_m')
    rc, pc = rho_text(corr, 'crest_depth_msl_m')
    n = corr['rep_depth_gap_m']['n']
    ax.text(0.985, 0.03, 'Spearman ρ with outcome (n = %d)\ndepth gap %.2f (p$_{perm}$ %.3f)\nramp length %.2f (p$_{perm}$ %.3f)\ncrest depth %.2f (p$_{perm}$ %.1f)'
            % (n, rg, pg, rl, pl, rc, pc), transform=ax.transAxes, ha='right', va='bottom', fontsize=7, color=INK,
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=GRID, lw=0.5), zorder=8)
    h1 = [Line2D([0], [0], color='#1B5E87', lw=0.9, ls=(0, (4, 2)), label='\u03be$_b$ = 0.4 and 2.0, T = 10 s (1:31, 1:6.2)'),
          Line2D([0], [0], color='#B03A2E', lw=0.9, ls=(0, (1.5, 1.5)), label='\u03be$_b$ = 0.4 and 2.0, T = 7 s (1:22, 1:4.4)'),
          Line2D([0], [0], color='#8F8F8F', lw=0.5, label='Mead class limits Y = 1.6, 1.9, 2.5, 3.1\n(slopes 1:12, 1:17, 1:26, 1:35)'),
          Line2D([0], [0], marker='o', ms=5.5, mfc='none', mec=INK2, mew=0.8, ls='none', label='Albany only: second cut through the\ntake-off peak (thin line joins it to the\nride-section cut, Fig. 1); see Appendix E')]
    fig.legend(handles=h1, loc='lower left', bbox_to_anchor=(0.0, 0.0), ncol=1, frameon=False, fontsize=7, handlelength=2.0,
               labelspacing=0.3, title='Lines (all are constant slopes \u0394h / L)', title_fontsize=7, alignment='left')
    h2 = [Patch(fc=shades[i], ec='#8F8F8F', lw=0.4, label=n_) for i, n_ in enumerate(
        ['beyond extreme, Y < 1.6 (steeper than 1:12)', 'extreme, Y 1.6-1.9 (1:12-1:17)', 'very high / high, Y 1.9-2.5 (1:17-1:26)',
         'medium, Y 2.5-3.1 (1:26-1:35)', 'gentle, Y > 3.1 (gentler than 1:35)'])]
    fig.legend(handles=h2, loc='lower left', bbox_to_anchor=(0.415, 0.0), ncol=1, frameon=False, fontsize=7, handlelength=1.4,
               labelspacing=0.3, title='Breaking intensity (Mead 2000, vortex ratio Y)', title_fontsize=7, alignment='left')
    fig.legend(handles=outcome_legend_handles(), loc='lower left', bbox_to_anchor=(0.80, 0.0), ncol=1, frameon=False, fontsize=7,
               labelspacing=0.3, handletextpad=0.4, title='Outcome (shape)', title_fontsize=7, alignment='left')
    return fig


# ====================================================================================================== F5
def fig5():
    S.setup()
    peel = rd('results_peel.csv')
    summ = rd('results_reef_summary.csv').set_index('slug')
    meta = rj('results_surf.json')['meta']['site_inputs']
    reefs = ['narrowneck-gold-coast', 'borth-coastal-defence-reef', 'mount-maunganui-reef', 'prattes-reef-el-segundo',
             'southern-ocean-surf-reef-albany', 'cables-reef-wa', 'boscombe-surf-reef', 'palm-beach-gold-coast']
    assumed = {'narrowneck-gold-coast', 'palm-beach-gold-coast', 'mount-maunganui-reef', 'borth-coastal-defence-reef',
               'southern-ocean-surf-reef-albany'}      # phi0 ASSUMPTION in results_peel.csv (phi0_src); checked below
    fig = plt.figure(figsize=(S.cm(9.6), S.cm(14.0)))
    axT = fig.add_axes([0.285, 0.715, 0.69, 0.275])
    axB = fig.add_axes([0.285, 0.30, 0.69, 0.38], sharex=axT)
    # --- top: Hutt rating rows (a rating can ride a wave with peel angle >= its limit)
    for r in range(1, 11):
        lim = W.HUTT[r][0]
        right = 0.0 if lim is None else lim
        axT.barh(r, right - 90.0, left=90.0, height=1.0, color='#D9D9D9' if lim is not None else '#EEEEEE',
                 edgecolor='white', lw=0.8, hatch=None if lim is not None else '////', zorder=2)
    px, py = [90.0], [0.5]
    for r in range(1, 9):
        lim = W.HUTT[r][0]
        px += [lim, lim]
        py += [r - 0.5, r + 0.5]
    axT.plot(px, py, color=INK, lw=0.9, zorder=3, solid_joinstyle='miter')
    for r in range(1, 11):              # Hutt et al. (2001) Table 3: breaking-wave height range of each rating (m, ASSUMED units)
        lim, hmin, hmax, _ = W.HUTT[r]
        htxt = '%.2f-%s m' % (hmin, ('%.2f' % hmax) if math.isfinite(hmax) else '>4')
        xt = (lim - 2.0) if (lim is not None and lim < 90) else (88.0 if lim is not None else 52.0)
        pre = {1: 'beginner: ', 7: '', 8: ''}.get(r, '')
        axT.text(xt, r, pre + ('%d\u00b0, ' % lim if lim is not None else '') + 'H$_b$ ' + htxt, fontsize=6.3, va='center',
                 ha='left', color=INK if r == 1 else INK2, zorder=4)
    axT.set_ylim(10.5, 0.5)
    axT.set_yticks(range(1, 11))
    axT.set_ylabel('Hutt skill rating')
    axT.text(88, 7.0, 'top amateur', fontsize=7, va='center', ha='left', color=INK, zorder=4)
    axT.text(88, 8.0, 'professional', fontsize=7, va='center', ha='left', color=INK, zorder=4)
    axT.text(88, 9.5, 'no limit', fontsize=7, va='center', ha='left', color=INK, zorder=4,
             bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.8))
    plt.setp(axT.get_xticklabels(), visible=False)
    # --- bottom: reefs
    n = len(reefs)
    axB.set_ylim(n - 0.4, -0.6)
    for i, s in enumerate(reefs):
        T = meta[s]['T']
        sub = peel[(peel.slug == s) & (peel['T'] == T) & (~peel.phi0_src.str.startswith('ALT'))]
        col = COLORS[s]
        amin, amax = sub.alpha_break_deg.min(), sub.alpha_break_deg.max()
        axB.plot([amin, amax], [i, i], color=col, lw=3.2, alpha=0.35, solid_capstyle='butt', zorder=3)
        g = sub.groupby('H0').alpha_break_deg.first()
        for H0, rowsH in sub.groupby('H0'):
            a = rowsH.alpha_break_deg.iloc[0]
            onreef = rowsH.category.iloc[0] in ('on_ramp', 'on_crest')
            inrange = bool(rowsH.Hb_in_rating_range.iloc[0])
            axB.plot([a], [i], marker='o', ms=3.6, mfc=col if onreef else 'white', mec=darken(col), mew=0.7, ls='none', zorder=5)
            if not inrange:
                axB.plot([a], [i], marker='+', ms=7, mec=INK, mew=0.8, ls='none', zorder=6)
        # unrefracted incident angle phi0 (both arms)
        for phi0 in sorted(sub.phi0_deg.unique()):
            axB.plot([phi0], [i], marker='|', ms=8, mec=col, mew=1.6, ls='none', zorder=4)
        # site-H value
        r = summ.loc[s]
        pt(axB, s, r.peel_alpha_snell_deg, i, r.outcome, ms=7.0, z=7)
    # Narrowneck alternative phi0 = 41 deg (dashed variant)
    alt = peel[(peel.slug == 'narrowneck-gold-coast') & peel.phi0_src.str.startswith('ALT')].iloc[0]
    axB.plot([alt.phi0_deg, alt.alpha_break_deg], [0.3, 0.3], color=COLORS['narrowneck-gold-coast'], lw=0.8, ls=(0, (3, 2)), zorder=4)
    axB.plot([alt.phi0_deg], [0.3], marker='|', ms=6, mec=COLORS['narrowneck-gold-coast'], mew=1.2, ls='none', zorder=4)
    axB.plot([alt.alpha_break_deg], [0.3], marker='o', ms=3.2, mfc='white', mec=COLORS['narrowneck-gold-coast'], mew=0.8, ls='none',
             zorder=4)
    axB.annotate('alt. \u03c6$_0$ 41\u00b0', (31.0, 0.3), xytext=(0, -3), textcoords='offset points', fontsize=7, ha='center',
                 va='top', color=INK2)
    axB.set_yticks(range(n))
    axB.set_yticklabels([NAMES[s] + ('*' if s in assumed else '') for s in reefs])
    for tl, s in zip(axB.get_yticklabels(), reefs):        # reef name in the reef's colour
        tl.set_color(darken(COLORS[s], 0.8))
        tl.set_fontweight('bold')
    axB.set_xlim(90, 0)
    axB.set_xlabel('Peel angle at breaking (deg; smaller = faster)')
    axB.set_xticks([90, 70, 60, 50, 40, 30, 20, 10, 0])
    # shared vertical guides: Walker's 30 deg minimum (6-ft plunging wave) and the close-out band
    for ax in (axT, axB):
        ax.axvspan(25, 0, color='#EDEDED', lw=0, zorder=0)
        ax.axvline(30, color='#B03A2E', lw=0.8, ls=(0, (4, 2)), zorder=1)
        for sp in ('top', 'right'):
            ax.spines[sp].set_visible(False)
    axB.text(7.5, (n - 1) / 2.0, 'approaching close-out (< 25\u00b0)', fontsize=7, va='center', ha='center', color=INK2, rotation=90, zorder=2)
    axT.text(28.5, 9.5, 'Walker (1975): 30\u00b0 min.,\n6-ft plunging wave', fontsize=6.3, color='#B03A2E', ha='left', va='center', zorder=4,
             bbox=dict(boxstyle='round,pad=0.1', fc='white', ec='none', alpha=0.85))
    h = [Line2D([0], [0], marker='o', ms=3.8, mfc='#7F7F7F', mec=INK2, mew=0.7, ls='none', label='H$_0$ 0.5-3 m, breaks on reef'),
         Line2D([0], [0], marker='o', ms=3.8, mfc='white', mec=INK2, mew=0.7, ls='none', label='no break on the reef'),
         Line2D([0], [0], marker='+', ms=6, mec=INK, mew=0.8, ls='none', label='H$_b$ above rating\'s height range'),
         Line2D([0], [0], marker='|', ms=7, mec=INK2, mew=1.4, ls='none', label='φ$_0$, no refraction'),
         Line2D([0], [0], color='#B03A2E', lw=0.8, ls=(0, (4, 2)), label='Walker (1975) 30\u00b0 minimum')]
    fig.legend(handles=h, loc='lower left', bbox_to_anchor=(0.0, 0.03), ncol=1, frameon=False, fontsize=6.5, columnspacing=0.8,
               labelspacing=0.3, handletextpad=0.3, title='Small symbols: H$_0$ 0.5-3 m runs', title_fontsize=6.5, alignment='left')
    fig.legend(handles=outcome_legend_handles(), loc='lower left', bbox_to_anchor=(0.6, 0.03), ncol=1, frameon=False, fontsize=6.5,
               labelspacing=0.25, handletextpad=0.3, title='Site-H wave, shape = outcome', title_fontsize=6.5, alignment='left')
    fig.text(0.01, 0.005, '* φ$_0$ (incident angle to the peel line) assumed; see caption', fontsize=6.5, ha='left', va='bottom', color=INK2)
    return fig


# ====================================================================================================== F6
def fig6():
    S.setup()
    vo = rd('results_volume_outcome.csv')
    summ = rd('results_reef_summary.csv').set_index('slug')
    corr = rj('results_outcome_correlations.json')
    fig = plt.figure(figsize=(S.cm(9.6), S.cm(11.4)))
    ax = fig.add_axes([0.21, 0.49, 0.72, 0.495])
    ax.set_xscale('log')
    ax.set_xlim(50, 100000)
    ax.set_ylim(0.45, 3.55)
    ax.axvspan(50, 5000, color='#F0F0F0', lw=0, zorder=0)
    ax.axvline(5000, color='#9A9A9A', lw=0.6, ls=(0, (3, 2)), zorder=1)
    ax.text(5000 * 1.06, 3.5, '5,000 m$^3$', fontsize=7, color=INK2, va='top', ha='left')
    jit = {'bunbury-airwave': 0.0, 'burkitts-reef-bargara': 0.0, 'prattes-reef-el-segundo': 0.0, 'mount-maunganui-reef': -0.16,
           'kovalam-reef-india': 0.16, 'opunake-reef': 0.0, 'cables-reef-wa': -0.16, 'boscombe-surf-reef': 0.0,
           'palm-beach-gold-coast': 0.0, 'southern-ocean-surf-reef-albany': 0.0, 'narrowneck-gold-coast': 0.0}
    lab = {'bunbury-airwave': (0, 10, 'center', 'bottom'), 'burkitts-reef-bargara': (0, 10, 'center', 'bottom'),
           'prattes-reef-el-segundo': (0, 10, 'center', 'bottom'), 'mount-maunganui-reef': (-8, -3, 'right', 'top'),
           'kovalam-reef-india': (-2, 9, 'center', 'bottom'), 'opunake-reef': (8, -2, 'left', 'center'),
           'cables-reef-wa': (8, -3, 'left', 'top'), 'boscombe-surf-reef': (0, 10, 'center', 'bottom'),
           'palm-beach-gold-coast': (-8, 0, 'right', 'center'), 'southern-ocean-surf-reef-albany': (0, 10, 'center', 'bottom'),
           'narrowneck-gold-coast': (14, -9, 'right', 'top')}
    import matplotlib.patheffects as pe
    for _, r in vo.iterrows():
        s = r.slug
        y = r.score + jit[s]
        if s in summ.index and np.isfinite(summ.loc[s].volume_model_m3):
            vm = summ.loc[s].volume_model_m3
            ax.plot([r.volume_stated_m3, vm], [y, y], color=COLORS[s], lw=0.7, zorder=3)
            ax.plot([vm], [y], marker=MARKERS[s], ms=4.6, mfc='white', mec=COLORS[s], mew=1.0, ls='none', zorder=4)
        pt(ax, s, r.volume_stated_m3, y, summ.loc[s].outcome if s in summ.index else S.OUTCOME.get(s), ms=7.5, z=6)
        dx, dy, ha, va = lab[s]
        nm = NAMES[s] if s != 'burkitts-reef-bargara' else 'Burkitts*'
        reef_label(ax, s, r.volume_stated_m3, y, dx, dy, ha=ha, va=va, text=nm, z=8)
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['does not\nwork', 'works rarely\nor mixed', 'works'])
    ax.set_xlabel('Reef volume (m$^3$, log scale)')
    ax.set_xticks([100, 1000, 10000, 100000])
    ax.set_xticklabels(['100', '1,000', '10,000', '100,000'])
    ax.minorticks_off()
    ax.tick_params(axis='y', length=0)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    c = corr['volume_stated_all_reefs']
    cm_ = corr['corr']['volume_model_m3']
    ab = c['built_reefs_asbuilt_basis']
    txt = ('built reefs: ρ = %.2f, p$_{perm}$ = %.3f (n = %d)\nincl. Burkitts*: ρ = %.2f, p$_{perm}$ = %.3f (n = %d)\nmodelled volume: ρ = %.2f, p$_{perm}$ = %.3f (n = %d)'
           '\nas built (Narrowneck mound 13,495,\n  Opunake built ~3,400 m$^3$): ρ = %.2f, p$_{perm}$ = %.3f (n = %d)'
           % (c['built_reefs_excl_burkitts']['spearman_rho'], c['built_reefs_excl_burkitts']['p_permutation'],
              c['built_reefs_excl_burkitts']['n'], c['all_incl_burkitts_natural']['spearman_rho'],
              c['all_incl_burkitts_natural']['p_permutation'], c['all_incl_burkitts_natural']['n'], cm_['spearman_rho'],
              cm_['p_permutation'], cm_['n'], ab['spearman_rho'], ab['p_permutation'], ab['n']))
    fig.text(0.0, 0.335, 'Spearman rank correlation with outcome:\n' + txt, fontsize=7, color=INK, ha='left', va='center', linespacing=1.3)
    h = [Line2D([0], [0], marker='o', ms=6.5, mfc='#7F7F7F', mec=INK2, mew=0.5, ls='none', label='stated volume (source)'),
         Line2D([0], [0], marker='o', ms=4.4, mfc='white', mec='#7F7F7F', mew=1.0, ls='none', label='volume of the 3D model'),
         Line2D([0], [0], color='#7F7F7F', lw=0.7, label='joins the two volumes')]
    fig.legend(handles=h, loc='lower left', bbox_to_anchor=(0.0, 0.03), ncol=1, frameon=False, fontsize=6.5, labelspacing=0.25,
               handletextpad=0.3, title='Colour + label = reef', title_fontsize=6.5, alignment='left')
    fig.legend(handles=outcome_legend_handles()[:4], loc='lower left', bbox_to_anchor=(0.55, 0.03), ncol=1, frameon=False, fontsize=6.5,
               labelspacing=0.25, handletextpad=0.3, title='Shape = outcome', title_fontsize=6.5, alignment='left')
    fig.text(0.0, 0.012, '* Burkitts: natural reef reshaped (about 300 m$^3$ of rock moved)', fontsize=7, color=INK2, ha='left',
             va='center')
    return fig


# ====================================================================================================== F7
def fig7():
    S.setup()
    import matplotlib.patheffects as pe
    t = rd('results_tide_range_summary.csv')
    summ = rd('results_reef_summary.csv').set_index('slug')
    fig = plt.figure(figsize=(S.cm(13.0), S.cm(11.4)))
    ax = fig.add_axes([0.075, 0.375, 0.915, 0.61])
    ax.set_xlim(0, 4.5)
    ax.set_ylim(-0.045, 1.04)
    # Israeli range band (Rosen 2001: neap 0.15 m, spring 0.40 m)
    ax.axvspan(0.15, 0.40, color='#E9C4BF', alpha=0.7, lw=0, zorder=0)
    ax.text(0.275, 1.03, 'Israel', fontsize=7, color='#8E2C21', ha='center', va='top', zorder=2,
            bbox=dict(boxstyle='round,pad=0.08', fc='#E9C4BF', ec='none'))

    def line(ramp, T, col, key, ls, lw, z=3):
        d = t[(t.ramp_one_in == ramp) & (t['T'] == T)].sort_values('spring_range_m')
        ax.plot(d.spring_range_m, d[key], color=col, ls=ls, lw=lw, zorder=z)
    DASH = (0, (4, 2))
    line(12, 7.0, INK, 'mean_frac_surfable_dc1p0', '-', 1.4)
    line(12, 10.0, INK, 'mean_frac_surfable_dc1p0', DASH, 1.4)
    line(12, 7.0, '#1B5E87', 'mean_frac_surfable_best_dc', '-', 0.8)
    line(12, 10.0, '#1B5E87', 'mean_frac_surfable_best_dc', DASH, 0.8)
    order = ['palm-beach-gold-coast', 'cables-reef-wa', 'southern-ocean-surf-reef-albany', 'borth-coastal-defence-reef',
             'mount-maunganui-reef', 'narrowneck-gold-coast', 'prattes-reef-el-segundo', 'boscombe-surf-reef', 'bunbury-airwave']
    off = {'palm-beach-gold-coast': (9, 0, 'left', 'center'), 'cables-reef-wa': (9, 1, 'left', 'center'),
           'southern-ocean-surf-reef-albany': (9, -1, 'left', 'center'), 'borth-coastal-defence-reef': (0, 8, 'center', 'bottom'),
           'mount-maunganui-reef': (9, 1, 'left', 'center'), 'narrowneck-gold-coast': (-9, 3, 'right', 'center'),
           'prattes-reef-el-segundo': (9, 1, 'left', 'center'), 'boscombe-surf-reef': (9, -1, 'left', 'center'),
           'bunbury-airwave': (-10, 3, 'right', 'bottom')}
    for s in order:
        r = summ.loc[s]
        x, y, yi = r.spring_range_m, r.surfable_frac_best_line, r.surfable_frac_israeli_tide_best_line
        col = COLORS[s]
        if abs(x - 0.40) > 1e-6:
            ax.annotate('', xy=(0.40, yi), xytext=(x, y), arrowprops=dict(arrowstyle='-|>', color=col, lw=0.8, shrinkA=4.5, shrinkB=2.5,
                                                                          mutation_scale=5, alpha=0.9), zorder=4)
        kw = S.marker_kw(s, ms=4.4, outcome=r.outcome)
        kw.update(mfc='white', mec=col, mew=1.0)
        ax.plot([0.40], [yi], zorder=5, **kw)
        ax.plot([x, x], [-0.045, -0.018], color=col, lw=1.6, solid_capstyle='butt', zorder=5, clip_on=False)   # range tick
        pt(ax, s, x, y, r.outcome, ms=6.8, z=7)
        dx, dy, ha, va = off[s]
        reef_label(ax, s, x, y, dx, dy, ha=ha, va=va, text='Bunbury' if s == 'bunbury-airwave' else NAMES[s], z=9)
    ax.set_xlabel('Tide range (m): spring; great diurnal at Pratte\'s; annual at WA reefs')
    ax.set_ylabel('Fraction of the lunar month with a surfable break')
    ax.set_xticks([0, 0.4, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5])
    ax.set_xticklabels(['0', '0.4', '1.0', '1.5', '2.0', '2.5', '3.0', '3.5', '4.0', '4.5'])
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    d12 = t[(t.ramp_one_in == 12) & (np.isclose(t.spring_range_m, 0.4))]
    lo = d12.mean_frac_surfable_dc1p0.min()
    hi = d12.mean_frac_surfable_dc1p0.max()
    d8 = t[(t.ramp_one_in == 8)]
    ax.text(0.985, 0.605, 'Israeli tide (0.4 m): %.2f to %.2f of the\nno-tide value (ramp 1:12 to 1:30, crest 1 m);\nwindow set by wave height alone.\nRamps 1:8 stay <= %.2f at every range.' % (lo, hi, d8.mean_frac_surfable_dc1p0.max()),
            transform=ax.transAxes, fontsize=7, ha='right', va='top', color=INK,
            bbox=dict(boxstyle='round,pad=0.25', fc='white', ec=GRID, lw=0.5), zorder=10)
    h1 = [Line2D([0], [0], color=INK, lw=1.4, label='synthetic reef, crest 1.0 m, ramp 1:12 to 1:30: T = 7 s'),
          Line2D([0], [0], color=INK, lw=1.4, ls=DASH, label='    same, T = 10 s'),
          Line2D([0], [0], color='#1B5E87', lw=0.8, label='crest 0.6 m (tuned to the range): T = 7 s'),
          Line2D([0], [0], color='#1B5E87', lw=0.8, ls=DASH, label='    same, T = 10 s'),
          Line2D([0], [0], color=INK2, lw=1.6, label='ticks: tide range of each built reef (see caption)')]
    fig.legend(handles=h1, loc='lower left', bbox_to_anchor=(0.0, 0.0), ncol=1, frameon=False, fontsize=7, handlelength=2.2,
               labelspacing=0.25)
    h2 = outcome_legend_handles() + [Line2D([0], [0], marker='o', ms=4.2, mfc='white', mec='#7F7F7F', mew=1.0, ls='none',
                                           label='small hollow: same reef under\nthe Israeli tide (arrow, own colour)')]
    fig.legend(handles=h2, loc='lower left', bbox_to_anchor=(0.62, 0.0), ncol=1, frameon=False, fontsize=7, labelspacing=0.25,
               handletextpad=0.3, title='Shape = outcome; colour + label = reef', title_fontsize=7, alignment='left')
    return fig


# ====================================================================================================== F8
def tube_color(D):
    return plt.cm.viridis(0.02 + 0.70 * (D - 1.0) / (3.2 - 1.0))


def spread(ys, gap):
    """Greedy de-overlap of label y positions (sorted ascending), keeps order."""
    idx = np.argsort(ys)
    out = np.array(ys, float)
    for k in range(1, len(idx)):
        if out[idx[k]] - out[idx[k - 1]] < gap:
            out[idx[k]] = out[idx[k - 1]] + gap
    return out


def fig8():
    """Figure 11 in the text. Load indices for sand-filled tubes (Bezuijen & Vastenburg section, FA 0.6 and 0.8; full tubes, FA 1.0, are not shown)."""
    S.setup()
    import matplotlib.patheffects as pe
    wcm, hcm = 17.0, 11.6
    fig = plt.figure(figsize=(S.cm(wcm), S.cm(hcm)))

    def axes_cm(l, b, w, h, **kw):
        return fig.add_axes([l / wcm, b / hcm, w / wcm, h / hcm], **kw)
    FA0, FAL = 0.8, 0.6
    fk = rd('results_stability_fk.csv')
    g = fk[fk.at_break == True]            # noqa: E712
    agg = g.groupby(['FA', 'C', 'h_base'])[['uplift_fraction', 'uplift_fraction_contact', 'SIc_calibrated', 'D', 'B']].max().reset_index()
    g0 = g[g.FA == FA0]
    band = g0.groupby('h_base')[['uplift_fraction_contact', 'SIc_calibrated']].agg(['min', 'max'])
    isr = rd('results_stability_israel_depth.csv')
    rock = rd('results_stability_rock.csv')
    XL = (1.5, 9.4)
    RED = '#B03A2E'
    # ---------------- (a) rock strip (top) and tubes under depth-limited breakers (main)
    axR = axes_cm(1.3, 9.1, 7.3, 1.35)
    ax = axes_cm(1.3, 3.2, 7.3, 5.55, sharex=axR)
    rows = [('Albany armour', rock[(rock.reef == 'southern-ocean-surf-reef-albany') & rock.unit.str.startswith('armour')], '#117733', 'right'),
            ('Cables 1.5 t', rock[(rock.reef == 'cables-reef-wa') & rock.unit.str.startswith('body granite 1.5')], '#E69F00', 'right'),
            ('Borth 8 t', rock[(rock.reef == 'borth-coastal-defence-reef') & rock.unit.str.contains('8 t')], '#56B4E9', 'left')]
    for k, (nm, d, col, side) in enumerate(rows):
        lo, hi = d.depth_where_breaking_H_equals_Hstable.min(), d.depth_where_breaking_H_equals_Hstable.max()
        Hlo, Hhi = d.H_stable_hudson.min(), d.H_stable_hudson.max()
        dag = '†' if bool(d.extrapolated.any()) else ''
        hi_c = min(hi, XL[1] - 0.05)
        axR.plot([lo, hi_c], [k, k], color=col, lw=4.2, solid_capstyle='butt', zorder=3, alpha=0.9)
        axR.plot([lo, lo], [k - 0.3, k + 0.3], color=INK, lw=0.8, zorder=4)
        if hi <= XL[1]:
            axR.plot([hi, hi], [k - 0.3, k + 0.3], color=INK, lw=0.8, zorder=4)
        else:
            axR.annotate('', xy=(XL[1], k), xytext=(XL[1] - 0.4, k), arrowprops=dict(arrowstyle='-|>', color=INK, lw=0.8, mutation_scale=5))
        lab = '%s %.1f-%.1f m%s' % (nm, Hlo, Hhi, dag)
        if side == 'right':
            axR.text(hi_c + 0.12, k, lab, fontsize=7, ha='left', va='center', color=darken(col, 0.8), fontweight='bold')
        else:
            axR.text(lo - 0.12, k, lab, fontsize=7, ha='right', va='center', color=darken(col, 0.8), fontweight='bold')
    axR.set_ylim(2.55, -1.4)
    axR.set_yticks([])
    axR.spines['left'].set_visible(False)
    axR.set_xlim(*XL)
    plt.setp(axR.get_xticklabels(), visible=False)
    axR.tick_params(axis='x', length=0)
    axR.text(XL[0] + 0.05, -0.85, 'bars: rock stable up to this depth (Hudson, K$_D$ = 2; stable H in m)', fontsize=7, color=INK2,
             ha='left', va='center')
    for sp in ('top', 'right'):
        axR.spines[sp].set_visible(False)
    ax.axvspan(1.5, 3.0, color='#EFEFEF', lw=0, zorder=0)
    ax.axvspan(2.0, 6.1, color='#E3EEF7', lw=0, zorder=0)       # Haifa reef base depths, crest (1.0-1.2 m + ~1 m tube) to toe (6.1 m)
    ax.axvspan(5.4, 6.1, color='#C9DFF0', lw=0, zorder=0)       # toe depth range, crest 1.0-1.2 m, ramp 1:16-1:20, bed 1:50
    ax.text(2.25, 3.45, 'surf-reef\ncrest tubes', fontsize=7, ha='center', va='top', color=INK2)
    ax.text(4.9, 3.45, 'Haifa reef: base depths\nfrom crest to toe', fontsize=7, ha='center', va='top', color='#1B5E87')
    ax.text(5.75, 2.55, 'toe\n5.4-6.1 m', fontsize=6.6, ha='center', va='top', color='#1B5E87')
    hs = band.index.values
    ax.fill_between(hs, band[('uplift_fraction_contact', 'min')], band[('uplift_fraction_contact', 'max')], color='#9A9A9A', alpha=0.55,
                    lw=0, zorder=2)
    ax.fill_between(hs, band[('SIc_calibrated', 'min')], band[('SIc_calibrated', 'max')], facecolor='none', edgecolor='#555555',
                    hatch='///', lw=0.0, zorder=2)
    ax.plot(hs, band[('SIc_calibrated', 'max')], color='#555555', lw=0.6, zorder=3)
    ax.plot(hs, band[('SIc_calibrated', 'min')], color='#555555', lw=0.6, zorder=3)
    ax.axhline(1.0, color=RED, lw=0.9, ls=(0, (4, 2)), zorder=3)
    ax.axhline(0.5, color='#555555', lw=0.8, ls=(0, (1.5, 1.5)), zorder=3)
    ends = []
    for C, d in agg[agg.FA == FA0].groupby('C'):
        d = d.sort_values('h_base')
        dl = agg[(agg.FA == FAL) & (agg.C == C)].set_index('h_base').uplift_fraction
        col = tube_color(min(max(d.D.iloc[0], 1.0), 3.2))
        hh = [h for h in d.h_base if h in dl.index]
        ax.plot(dl.index, dl.values, color=col, lw=0.7, ls=(0, (3, 1.5)), alpha=0.75, zorder=4)
        ax.plot(d.h_base, d.uplift_fraction, color=col, lw=1.5, marker='o', ms=2.6, zorder=5)
        ends.append((d.B.iloc[0], d.D.iloc[0], col, d.h_base.iloc[-1], d.uplift_fraction.iloc[-1]))
    ys = spread([e[4] for e in ends], 0.17)
    for (B, D, col, x, y), yl in zip(ends, ys):
        tl = ax.annotate('%.3g x %.3g' % (B, D), (x, y), xytext=(x + 0.25, yl), fontsize=7, ha='left', va='center',
                         color=darken(col, 0.85), arrowprops=dict(arrowstyle='-', lw=0.4, color='#9A9A9A', shrinkA=0, shrinkB=2),
                         zorder=10, annotation_clip=False)
        tl.set_path_effects([pe.withStroke(linewidth=3.0, foreground='white')])
    ax.set_xlim(*XL)
    ax.set_ylim(0, 3.5)
    ax.set_xlabel('Water depth at the tube base h (m)')
    ax.set_ylabel('Load index (U, U$_c$, SI$_c$; dimensionless)')
    ax.set_xticks([2, 3, 4, 5, 6, 7, 8, 9])
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax2 = axR.secondary_xaxis('top', functions=(lambda h: 0.78 * h, lambda H: H / 0.78))
    ax2.set_xlabel('Depth-limited breaking height H$_b$ = 0.78 h (m)', labelpad=2)
    ax2.set_xticks([2, 4, 6, 8])
    fig.text(0.004, 0.992, '(a)', fontsize=8.5, fontweight='bold', va='top')
    ha_ = [Line2D([0], [0], color=tube_color(2.0), lw=1.5, marker='o', ms=3, label='U per tube at FA 0.8 (label B x D, m)'),
           Line2D([0], [0], color=tube_color(2.0), lw=0.7, ls=(0, (3, 1.5)), label='same tube filled to FA 0.6 (flatter)'),
           Line2D([0], [0], color=RED, lw=0.9, ls=(0, (4, 2)), label='U = 1: uplift equals submerged weight'),
           Patch(fc='#9A9A9A', alpha=0.6, label='U$_c$ (pressure under the base), range over tubes and periods'),
           Patch(fc='none', ec='#555555', hatch='///', label='computed sliding index SI$_c$, range over tubes and periods'),
           Line2D([0], [0], color='#555555', lw=0.8, ls=(0, (1.5, 1.5)), label='sliding threshold (SI$_c$ = 0.5, friction f = 0.5)')]
    fig.legend(handles=ha_, loc='lower left', bbox_to_anchor=(0.0 / wcm, 0.02), ncol=1, frameon=False, fontsize=6.6,
               handlelength=2.2, handletextpad=0.4, labelspacing=0.22)
    # ---------------- (b) Israeli tubes vs depth in storms, (c) local Hs vs the single-tube sliding criterion
    axb = axes_cm(10.5, 7.0, 5.15, 3.15)
    axc = axes_cm(10.5, 3.85, 5.15, 2.35, sharex=axb)
    storms = [(3.3, 10.0, '-'), (5.0, 12.0, (0, (4, 2))), (1.0, 7.0, (0, (1, 1.5)))]
    tubes = [('Israeli geotube (D_th 5 m)', 5.0), ('Israeli geotube (D_th 3 m)', 3.0)]
    tcol = {}
    for nm, Dth in tubes:
        d8 = isr[(isr.tube == nm) & (isr.FA == FA0)]
        col = tube_color(min(max(d8.D.iloc[0], 1.0), 3.2))
        tcol[nm] = (col, d8.B.iloc[0], d8.D.iloc[0], Dth)
        for Hs, T, ls in storms:
            d = d8[d8.Hs_storm == Hs].sort_values('h_base')
            dl = isr[(isr.tube == nm) & (isr.FA == FAL) & (isr.Hs_storm == Hs)].set_index('h_base').uplift_fraction
            hh = [h for h in d.h_base if h in dl.index]
            axb.fill_between(hh, d.set_index('h_base').uplift_fraction.loc[hh], dl.loc[hh].clip(upper=3.0), color=col, alpha=0.07, lw=0)
            axb.plot(d.h_base, d.uplift_fraction, color=col, ls=ls, lw=1.3)
    axb.axhline(1.0, color=RED, lw=0.9, ls=(0, (4, 2)), zorder=0)
    axb.set_ylim(0, 3.0)
    axb.set_xlim(2, 16)
    axb.set_ylabel('U (sealed base)', labelpad=4)
    axb.set_xticks([2, 4, 6, 8, 10, 12, 14, 16])
    plt.setp(axb.get_xticklabels(), visible=False)
    for sp in ('top', 'right'):
        axb.spines[sp].set_visible(False)
    axb.text(0.0, 1.03, '(b) U of Israeli tubes in storms', transform=axb.transAxes, fontsize=8,
             fontweight='bold', ha='left', va='bottom')
    d0 = isr[(isr.tube == tubes[0][0]) & (isr.FA == FA0)]
    for Hs, T, ls in storms:
        d = d0[d0.Hs_storm == Hs].sort_values('h_base')
        axc.plot(d.h_base, d.Hs_local, color=INK, ls=ls, lw=1.2)
    for nm, Dth in tubes:
        col, B, D, _ = tcol[nm]
        crit = isr[(isr.tube == nm) & (isr.FA == FA0)].Hs_crit_vansteeg.iloc[0]
        axc.axhline(crit, color=col, lw=1.1, zorder=0)
        axc.text(2.1, crit + (0.1 if crit > 1.0 else -0.1), 'sliding limit %.2f m' % crit, fontsize=6.6, color=darken(col, 0.85),
                 ha='left', va='bottom' if crit > 1.0 else 'top')
    axc.set_ylim(0, 5.7)
    axc.set_xlabel('Water depth at the tube base h (m)')
    axc.set_ylabel('Local H$_s$ (m)')
    for sp in ('top', 'right'):
        axc.spines[sp].set_visible(False)
    axc.text(0.0, 1.03, '(c) local H$_s$ against the sliding limit', transform=axc.transAxes, fontsize=8, fontweight='bold',
             ha='left', va='bottom')
    hb = [Line2D([0], [0], color=INK, lw=1.2, ls=ls, label='storm H$_s$ %g m, T %g s' % (Hs, T)) for Hs, T, ls in storms]
    hb += [Line2D([0], [0], color=tcol[nm][0], lw=2.0, label='%.3g x %.3g m tube (D$_{th}$ %g m)' % (tcol[nm][1], tcol[nm][2], Dth))
           for nm, Dth in tubes]
    hb += [Patch(fc=tube_color(2.0), alpha=0.25, lw=0, label='(b) band: same tube filled to FA 0.6 (top)'),
           Line2D([0], [0], color=tube_color(2.0), lw=1.1, label='(c) sliding limit, van Steeg et al. (2011)')]
    fig.legend(handles=hb, loc='lower left', bbox_to_anchor=(9.7 / wcm, 0.0), ncol=1, frameon=False, fontsize=6.6,
               handlelength=2.2, handletextpad=0.4, labelspacing=0.22, columnspacing=0.8)
    return fig


# ====================================================================================================== F9
def fig9():
    S.setup()
    import matplotlib.patheffects as pe
    from matplotlib.transforms import blended_transform_factory
    d = rd('results_israel_design_summary.csv')
    d = d[d.bed_one_in == 50]
    summ = rd('results_reef_summary.csv').set_index('slug')
    Xs = [8, 12, 16, 20, 30]
    Ds = [0.6, 0.8, 1.0, 1.2, 1.5, 2.0]
    xe = [Xs[0] ** 2 / math.sqrt(Xs[0] * Xs[1])] + [math.sqrt(Xs[i] * Xs[i + 1]) for i in range(4)] + [Xs[-1] ** 2 / math.sqrt(Xs[-2] * Xs[-1])]
    ye = [Ds[0] - (Ds[1] - Ds[0]) / 2] + [(Ds[i] + Ds[i + 1]) / 2 for i in range(5)] + [Ds[-1] + (Ds[-1] - Ds[-2]) / 2]
    F = np.zeros((6, 5))
    V = np.zeros((6, 5))
    SH = {}
    for i, dc in enumerate(Ds):
        for j, X in enumerate(Xs):
            r = d[(np.isclose(d.d_c, dc)) & (d.ramp_one_in == X)].iloc[0]
            F[i, j] = r.mean_frac_surfable_israeli
            V[i, j] = r.volume_per_100m_m3
            SH[(i, j)] = [r.share_too_hollow_msl, r.share_advanced_or_expert_msl + r.share_intermediate_msl, r.share_spilling_or_gentle_msl,
                          r.share_not_on_reef_msl]
    wcm, hcm = 17.0, 10.9
    fig = plt.figure(figsize=(S.cm(wcm), S.cm(hcm)))
    ax = fig.add_axes([1.4 / wcm, 2.3 / hcm, 9.0 / wcm, 7.6 / hcm])
    ax.set_xscale('log')
    cmap = mcolors.LinearSegmentedColormap.from_list('gnbu_t', plt.cm.GnBu(np.linspace(0.04, 0.60, 256)))
    ax.pcolormesh(xe, ye, F, cmap=cmap, vmin=0, vmax=1, edgecolor='white', linewidth=1.0, zorder=1)
    ax.set_xlim(xe[0], xe[-1])
    ax.set_ylim(2.55, ye[0])
    ax.set_yticks(Ds)
    ax.set_yticklabels(['%.1f' % v for v in Ds])
    ax.set_xticks(Xs)
    ax.set_xticklabels(['1:%d' % v for v in Xs])
    ax.minorticks_off()
    ax.set_xlabel('Ramp slope (1:X, seaward face; log axis)')
    ax.set_ylabel('Crest depth below MSL, d$_c$ (m)')
    CL = ['#9E2A2B', '#F2B134', '#6A3D9A', '#BDBDBD']
    for i in range(6):
        for j in range(5):
            xl, xr = xe[j], xe[j + 1]
            yt, yb = ye[i], ye[i + 1]
            bw0, bw1 = xl * 1.05, xr / 1.05
            lw_ = math.log(bw1 / bw0)
            pos = math.log(bw0)
            hb = (yb - yt) * 0.17
            y1 = yb - (yb - yt) * 0.07
            for sh, c in zip(SH[(i, j)], CL):
                if sh <= 1e-9:
                    continue
                x0 = math.exp(pos)
                x1 = math.exp(pos + lw_ * sh)
                ax.add_patch(Rectangle((x0, y1 - hb), x1 - x0, hb, fc=c, ec='white', lw=0.3, zorder=3))
                pos += lw_ * sh
    # surfable fraction: 1:8 inside its cells, 1:12 to 1:30 (identical) as a column right of the grid
    for i in range(6):
        ax.text(xe[1] / 1.03, Ds[i] - 0.085, '%.2f' % F[i, 0], fontsize=7, ha='right', va='center', color=INK, zorder=4)
    tr = blended_transform_factory(ax.transAxes, ax.transData)
    for i in range(6):
        ax.text(1.025, Ds[i] - 0.085, '%.2f' % F[i, 1], transform=tr, fontsize=7, ha='left', va='center', color=INK, clip_on=False)
    fig.text(1.4 / wcm + 9.0 / wcm * 1.0, 10.0 / hcm, 'surfable\nfraction\n1:12-1:30', fontsize=7, ha='left', va='bottom', color=INK, linespacing=1.15)
    # volume contours (m3 per 100 m of reef length)
    cs = ax.contour(Xs, Ds, V, levels=[10000, 15000, 25000, 40000], colors=['#222222'], linewidths=0.7, linestyles='-', zorder=2.5)
    ax.clabel(cs, fmt=lambda v: '{:,}'.format(int(v)), fontsize=7, inline=True, inline_spacing=1, colors='#222222')
    # field observations at Haifa (Appendix G, slide 2 of the author's notes): water depth at the peak when the wave breaks,
    # 1.30 m (Hs 0.45 / Hmax 0.6 m) and 1.50 m (Hs 0.60 / Hmax 0.8 m); take-off depth in borderline sea about 1.0 m
    for yy in (1.3, 1.5):
        ax.axhline(yy, color='#444444', lw=0.8, ls=(0, (3, 2)), zorder=2.6)
    ax.axhline(1.0, color='#444444', lw=0.9, ls=(0, (1, 1.5)), zorder=2.6)
    # recommended envelope: crest 1.0-1.2 m, ramp 1:16-1:20 (revised 2026-10-20: model breaking depths for H0 >= 0.6-0.8 m,
    # at least 0.5 m of water over the crest at the 1-year low level -0.38 m MSL; Section 7.5)
    ax.add_patch(Rectangle((xe[2], ye[2]), xe[4] - xe[2], ye[4] - ye[2], fill=False, ec='black', lw=2.2, zorder=6))
    # reference reefs (crest depth, mean seaward ramp slope)
    al = summ.loc['southern-ocean-surf-reef-albany']      # surf cut (crest_line override, Lior 2026-10-19)
    pb, cb_, nn = summ.loc['palm-beach-gold-coast'], summ.loc['cables-reef-wa'], summ.loc['narrowneck-gold-coast']
    ref = [('palm-beach-gold-coast', 'Palm Beach', pb.crest_depth_msl_m, pb.mean_seaward_slope_1_in, pb.outcome, (-8, 4, 'right', 'bottom')),
           ('cables-reef-wa', 'Cables', cb_.crest_depth_msl_m, cb_.mean_seaward_slope_1_in, cb_.outcome, (8, 5, 'left', 'bottom')),
           ('southern-ocean-surf-reef-albany', 'Albany (surf cut)', al.rep_crest_depth_msl_m, al.rep_mean_seaward_slope_1_in, al.outcome,
            (8, 0, 'left', 'center')),
           ('narrowneck-gold-coast', 'Narrowneck (2nd crest line)', nn.rep_crest_depth_msl_m, nn.rep_mean_seaward_slope_1_in, nn.outcome,
            (8, 0, 'left', 'center'))]
    for s, nm, dc, X, outc, (dx, dy, ha, va) in ref:
        pt(ax, s, X, dc, outc, ms=7.0, z=8)
        reef_label(ax, s, X, dc, dx, dy, ha=ha, va=va, text=nm, z=9)
    bx = summ.loc['boscombe-surf-reef']
    ax.annotate('', xy=(xe[0] * 1.0, bx.crest_depth_msl_m), xytext=(xe[0] * 1.2, bx.crest_depth_msl_m),
                arrowprops=dict(arrowstyle='-|>', color=COLORS['boscombe-surf-reef'], lw=1.4, mutation_scale=7), zorder=8)
    t = ax.text(xe[0] * 1.22, bx.crest_depth_msl_m, 'Boscombe\n1:%.1f (off scale)' % bx.mean_seaward_slope_1_in, fontsize=7, ha='left',
                va='center', color=darken(COLORS['boscombe-surf-reef'], 0.8), fontweight='bold', zorder=9, linespacing=1.1)
    t.set_path_effects([pe.withStroke(linewidth=2.4, foreground='white')])
    ax.text(xe[0] * 1.03, 2.5, 'no model rows below 2.0 m', fontsize=7, color=INK2, ha='left', va='center')
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    # bracket right of the number column: observed depths at the peak, from the smallest surfable shoulder (1.15 m)
    # to the depth at which the largest sets break (1.70 m), both bounds (Appendix G)
    bk = '#444444'
    ax.plot([1.17, 1.17], [1.15, 1.70], transform=tr, color=bk, lw=1.0, clip_on=False, solid_capstyle='butt')
    for yy, w in ((1.15, 0.02), (1.70, 0.02), (1.30, 0.012), (1.50, 0.012)):
        ax.plot([1.17 - w, 1.17], [yy, yy], transform=tr, color=bk, lw=1.0, clip_on=False)
    ax.text(1.20, 1.42, 'observed at\nHaifa (indic.),\ndepth at the\npeak: 1.15-1.70 m\n(break 1.30\nand 1.50 m)', transform=tr, fontsize=7, color=bk,
            ha='left', va='center', clip_on=False, linespacing=1.1)
    ax.text(1.20, 1.0, 'take-off\n~1.0 m', transform=tr, fontsize=7, color=bk, ha='left', va='center', clip_on=False, linespacing=1.1)
    # colour bar and class legend
    cax = fig.add_axes([1.4 / wcm, 1.0 / hcm, 4.0 / wcm, 0.25 / hcm])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=mcolors.Normalize(0, 1))
    cb = fig.colorbar(sm, cax=cax, orientation='horizontal')
    cb.set_ticks([0, 0.5, 1.0])
    cb.ax.tick_params(labelsize=7, length=2)
    cb.set_label('Surfable fraction of the time, Israeli tide', fontsize=7, labelpad=1)
    hc = [Patch(fc=c, ec='none', label=l) for c, l in zip(CL, ['too hollow (collapsing)', 'advanced / expert', 'spilling / gentle', 'no break on the reef'])]
    fig.legend(handles=hc, loc='lower left', bbox_to_anchor=(5.75 / wcm, 0.0), ncol=2, frameon=False, fontsize=7, handlelength=1.2,
               columnspacing=1.0, title='Bar in each cell: share of waves at MSL', title_fontsize=7, alignment='left')
    # right column: text box and legend
    fig.text(13.45 / wcm, 10.5 / hcm,
             'Recommended Haifa envelope\n(heavy box): crest 1.0-1.2 m,\nramp 1:16-1:20; rock armour\nDn50 ~ 0.7-0.85 m (1-1.6 t);\n14,000-20,000 m$^3$ per 100 m.\nCells: Haifa waves (T 6-8 s)\nand Israeli tide 0.4 m',
             fontsize=7, ha='left', va='top', color=INK, linespacing=1.25, bbox=dict(boxstyle='round,pad=0.3', fc='white', ec=GRID, lw=0.6))
    ho = [Line2D([0], [0], color='#222222', lw=0.7, label='volume per 100 m (m$^3$)'),
          Line2D([0], [0], color='#444444', lw=0.8, ls=(0, (3, 2)), label='observed breaking\ndepth, Haifa (indicative):\n1.30 m (Hs 0.45 m),\n1.50 m (Hs 0.60 m)'),
          Line2D([0], [0], color='#444444', lw=0.9, ls=(0, (1, 1.5)), label='take-off depth,\nborderline sea')]
    ho += outcome_legend_handles()
    fig.legend(handles=ho, loc='upper left', bbox_to_anchor=(13.4 / wcm, 5.7 / hcm), ncol=1, frameon=False, fontsize=7, handlelength=1.6,
               labelspacing=0.35, handletextpad=0.4, title='Built reefs: geometry\nonly (crest depth, slope);\ncells = Haifa waves, not\nthe reefs\' own climates;\nshape = outcome', title_fontsize=7, alignment='left')
    return fig


FIGS = {'fig4': (fig4, 'fig4_gap_ramp'), 'fig5': (fig5, 'fig5_peel_skill'), 'fig6': (fig6, 'fig6_volume_outcome'),
        'fig7': (fig7, 'fig7_tide_window'), 'fig8': (fig8, 'fig8_stability'), 'fig9': (fig9, 'fig9_haifa_envelope')}


def main(argv):
    sel = argv[1:] or list(FIGS)
    for k in sel:
        fn, name = FIGS[k]
        print('\n'.join(S.save(fn(), name)))


if __name__ == '__main__':
    main(sys.argv)

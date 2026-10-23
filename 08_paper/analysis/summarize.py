#!/usr/bin/env python3
"""summarize.py - one row per reef combining parts 1-7 (writes results_reef_summary.csv). Run after the other scripts."""
import csv
import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUTCOME_SCORE = {'works': 3, 'works rarely': 2, 'mixed/disputed': 2, 'does not work': 1, 'unknown': None}
# Representative profile line for the geometry columns (rep_*). The profile JSON caveats say the crest line is not
# representative for these two reefs: Narrowneck crest line clips the tip of the north arm (use the south-arm
# second_crest_line); Pratte's crest-line ramp (1 m) is a tip artefact (use the centreline through the apex block).
REP_LINE = {'narrowneck-gold-coast': 'second_crest_line', 'prattes-reef-el-segundo': 'centreline'}
WORKS = ('on_ramp', 'on_crest')
# Burkitts: natural basalt platform reshaped (~300 m3 of rock moved), not a built reef volume -> sensitivity only
NATURAL_RESHAPED = {'burkitts-reef-bargara'}


def perm_p(x, y, n=20000, seed=1):
    """Two-sided Monte Carlo permutation p-value of Spearman rho (ties handled by average ranks)."""
    from scipy.stats import rankdata
    rx = rankdata(np.asarray(x, float))
    ry = rankdata(np.asarray(y, float))
    rx = (rx - rx.mean()) / np.linalg.norm(rx - rx.mean())
    ry = (ry - ry.mean()) / np.linalg.norm(ry - ry.mean())
    r0 = float(rx @ ry)   # Spearman rho = Pearson of average ranks
    rng = np.random.default_rng(seed)
    perms = np.array([rng.permutation(ry) for _ in range(n)])
    cnt = int(np.sum(np.abs(perms @ rx) >= abs(r0) - 1e-12))
    return float((cnt + 1) / (n + 1))


def main():
    meta = json.load(open(os.path.join(HERE, 'results_surf.json')))['meta']['site_inputs']
    tw = pd.read_csv(os.path.join(HERE, 'results_tide_window.csv'))
    tw = tw[tw.apply(lambda r: r['T'] == meta[r.slug]['T'], axis=1)]
    size = pd.read_csv(os.path.join(HERE, 'results_size.csv')).set_index('slug')
    peel = pd.read_csv(os.path.join(HERE, 'results_peel.csv'))
    shore = pd.read_csv(os.path.join(HERE, 'results_shoreline.csv')).set_index('slug')
    tr = pd.read_csv(os.path.join(HERE, 'results_transmission.csv'))
    # slope at the break point for every on-reef break (McCowan, profile lines, all H, T and tides of results_breaking.csv)
    br = pd.read_csv(os.path.join(HERE, 'results_breaking.csv'), usecols=['slug', 'line', 'gamma_mode', 'category', 'slope_X', 'xi_b', 'vortex_extrapolated'])
    br = br[(br.gamma_mode == 'mccowan') & br.category.isin(WORKS) & ~br.line.str.startswith('layer')]
    brg = br.groupby('slug').agg(n_on_reef_cases=('xi_b', 'size'), slope_X_at_break_median=('slope_X', 'median'),
                                 xi_b_median=('xi_b', 'median'), share_outside_mead_black_range=('vortex_extrapolated', 'mean'))
    prof = {s: json.load(open(os.path.join(HERE, '..', 'data', 'profiles', s + '.json'))) for s in meta}
    rows = []
    for s, site in meta.items():
        m = prof[s]['lines']['crest_line']['metrics']
        rl = REP_LINE.get(s, 'crest_line')
        mr = prof[s]['lines'][rl]['metrics']
        t = tw[(tw.slug == s) & tw.H0.isin([0.5, 1.0, 1.5, 2.0])]
        sf = t.groupby('line')['frac_time_surfable'].mean()
        sfi = t.groupby('line')['frac_time_surfable_israeli_tide'].mean()
        default_lines = [l for l in sf.index if not l.startswith('layer')]
        # peel angle only where the wave breaks ON the reef (ramp or crest) at MSL: the site H if it does, otherwise the
        # smallest H0 of the set that does (fix 2026-10-16: the earlier version averaged rows where the wave passed the reef)
        pall = peel[(peel.slug == s) & (peel['T'] == site['T']) & ~peel.phi0_src.str.startswith('ALT')]
        pon = pall[pall.category.isin(WORKS)]
        if len(pon[pon.H0 == site['H']]):
            p, pH = pon[pon.H0 == site['H']], site['H']
        elif len(pon):
            pH = float(pon.H0.min())
            p = pon[pon.H0 == pH]
        else:
            p, pH = pon, None
        k = tr[(tr.slug == s) & (tr['T'] == site['T']) & (tr.H0 == site['H'])].set_index('tide')['Kt']
        sz = size.loc[s]
        rows.append(dict(
            slug=s, outcome=sz['outcome'], outcome_score=OUTCOME_SCORE.get(sz['outcome']),
            crest_depth_msl_m=round(-m['crest_z_msl_m'], 2), relief_m=m.get('crest_height_above_seabed_m'),
            depth_gap_crest_to_toe_bed_m=m.get('crest_to_toe_seabed_drop_m'), ramp_length_m=m.get('ramp_length_m'),
            mean_seaward_slope_1_in=(m.get('mean_seaward_slope') or {}).get('one_in'), max_seaward_slope_1_in=(m.get('max_seaward_slope') or {}).get('one_in'),
            vortex_Y_of_mean_face=0.065 * ((m.get('mean_seaward_slope') or {}).get('one_in') or np.nan) + 0.821,
            H_site=site['H'], T_site=site['T'], spring_range_m=float(t['spring_range'].iloc[0]) if len(t) else None,
            H0_to_break_on_crest_at_msl=sz['H0_needed_to_break_on_crest_msl'], H0_max_before_breaking_seaward_msl=sz['H0_max_before_breaking_seaward_of_reef_msl'],
            surfable_frac_crest_line=sf.get('crest_line'), surfable_frac_best_line=float(sf[default_lines].max()) if default_lines else None,
            surfable_frac_israeli_tide_best_line=float(sfi[default_lines].max()) if default_lines else None,
            peel_H0_used=pH,
            peel_alpha_unrefracted_deg=float(p['alpha_no_refraction_deg'].mean()) if len(p) else None,
            peel_alpha_snell_deg=float(p['alpha_break_deg'].mean()) if len(p) else None,
            hutt_rating_range=('%d-%d' % (p['hutt_rating_no_refraction'].min(), p['hutt_rating'].max())) if len(p) else None,
            rep_line=rl, rep_crest_depth_msl_m=round(-mr['crest_z_msl_m'], 2), rep_relief_m=mr.get('crest_height_above_seabed_m'),
            rep_depth_gap_m=mr.get('crest_to_toe_seabed_drop_m'), rep_ramp_length_m=mr.get('ramp_length_m'),
            rep_mean_seaward_slope_1_in=(mr.get('mean_seaward_slope') or {}).get('one_in'),
            rep_max_seaward_slope_1_in=(mr.get('max_seaward_slope') or {}).get('one_in'),
            rep_toe_bed_depth_msl_m=-mr['seaward_toe_seabed_z_msl_m'] if mr.get('seaward_toe_seabed_z_msl_m') is not None else None,
            volume_model_m3=sz['volume_model_m3'], volume_stated_m3=sz['volume_stated_m3'], alongshore_span_m=sz['alongshore_span_m'],
            area_within_1m_of_crest_m2=sz['area_within_1m_of_crest_m2'], crossshore_over_L=sz['crossshore_over_L'],
            Kt_site_low=k.get('low'), Kt_site_mid=k.get('mid'), Kt_site_high=k.get('high'),
            n_on_reef_cases=brg.loc[s, 'n_on_reef_cases'] if s in brg.index else 0,
            slope_X_at_break_median=brg.loc[s, 'slope_X_at_break_median'] if s in brg.index else None,
            vortex_Y_at_median_X=0.065 * brg.loc[s, 'slope_X_at_break_median'] + 0.821 if s in brg.index else None,
            xi_b_median=brg.loc[s, 'xi_b_median'] if s in brg.index else None,
            share_outside_mead_black_range=brg.loc[s, 'share_outside_mead_black_range'] if s in brg.index else None,
            B_over_S=shore.loc[s, 'B_over_S'], salient_pred_m=shore.loc[s, 'salient_Yoff_pred_m'],
            Sa_over_SZW_siteH=shore.loc[s, 'Sa_over_SZW_siteH'], H0_at_ranasinghe_peak=shore.loc[s].get('H0_at_Sa_over_SZW_2')))
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(HERE, 'results_reef_summary.csv'), index=False, float_format='%.3f')
    ok = df.dropna(subset=['outcome_score'])
    from scipy.stats import spearmanr
    corr = {}
    for c in ['surfable_frac_best_line', 'surfable_frac_crest_line', 'volume_model_m3', 'volume_stated_m3', 'alongshore_span_m',
              'area_within_1m_of_crest_m2', 'crest_depth_msl_m', 'mean_seaward_slope_1_in', 'ramp_length_m', 'crossshore_over_L',
              'rep_crest_depth_msl_m', 'rep_relief_m', 'rep_depth_gap_m', 'rep_ramp_length_m', 'rep_mean_seaward_slope_1_in',
              'slope_X_at_break_median', 'xi_b_median']:
        x = ok[[c, 'outcome_score']].dropna()
        if len(x) >= 5:
            r, pval = spearmanr(x[c], x['outcome_score'])
            corr[c] = dict(n=len(x), spearman_rho=round(float(r), 3), p=round(float(pval), 3),
                           p_permutation=round(perm_p(x[c], x['outcome_score']), 4))
    # stated volume (reefs.json, each value cited there) for ALL reefs with a known outcome, incl. the four without a 3D model
    reefs = json.load(open(os.path.join(HERE, '..', 'data', 'reefs.json')))
    vrows = []
    for r in reefs:
        out = (r.get('surf_outcome') or {}).get('value')
        vol = (r.get('volume_m3') or {}).get('value')
        if OUTCOME_SCORE.get(out) is not None and isinstance(vol, (int, float)):
            vrows.append(dict(slug=r['slug'], outcome=out, score=OUTCOME_SCORE[out], volume_stated_m3=vol,
                              volume_source=(r.get('volume_m3') or {}).get('location')))
    vdf = pd.DataFrame(vrows).sort_values('volume_stated_m3')
    vol_corr = {}
    for lab, sub in (('built_reefs_excl_burkitts', vdf[~vdf.slug.isin(NATURAL_RESHAPED)]), ('all_incl_burkitts_natural', vdf)):
        r, pval = spearmanr(sub['volume_stated_m3'], sub['score'])
        vol_corr[lab] = dict(n=len(sub), spearman_rho=round(float(r), 3), p=round(float(pval), 4),
                             p_permutation=round(perm_p(sub['volume_stated_m3'], sub['score']), 4))
    # sensitivity (2026-10-20, notes/cost_volume_check.md): as-built basis where the stated value is a fill or design volume:
    # Narrowneck exposed mound of the 3D model (13,495 m3) instead of the 70,000 m3 sand fill; Opunake ~3,400 m3 built
    # (Blacka et al. 2013 Table 4.4 cost per m3) instead of the 4,900 m3 design
    ALT_BASIS = {'narrowneck-gold-coast': 13495, 'opunake-reef': 3400}
    sub = vdf[~vdf.slug.isin(NATURAL_RESHAPED)].copy()
    sub['volume_alt_m3'] = [ALT_BASIS.get(s_, v_) for s_, v_ in zip(sub.slug, sub.volume_stated_m3)]
    r, pval = spearmanr(sub['volume_alt_m3'], sub['score'])
    vol_corr['built_reefs_asbuilt_basis'] = dict(n=len(sub), spearman_rho=round(float(r), 3), p=round(float(pval), 4),
                                                 p_permutation=round(perm_p(sub['volume_alt_m3'], sub['score']), 4),
                                                 substitutions=ALT_BASIS)
    vdf['volume_alt_m3'] = [ALT_BASIS.get(s_, v_) for s_, v_ in zip(vdf.slug, vdf.volume_stated_m3)]
    vdf.to_csv(os.path.join(HERE, 'results_volume_outcome.csv'), index=False)
    with open(os.path.join(HERE, 'results_outcome_correlations.json'), 'w') as f:
        json.dump(dict(note='Spearman rank correlation with outcome score (works 3, works rarely / mixed 2, does not work 1; unknown excluded). '
                            'p = scipy t-approximation; p_permutation = two-sided Monte Carlo permutation test (20,000, seed 1). '
                            'corr: the 8 modelled reefs with a known outcome (Borth unknown); rep_* = representative line (REP_LINE). '
                            'volume_stated_all_reefs: reefs.json volume_m3 for every reef with a known outcome (results_volume_outcome.csv). '
                            'n is tiny and outcome is an ordinal judgement: descriptive only.',
                       corr=corr, volume_stated_all_reefs=vol_corr), f, indent=1)
    print(df[['slug', 'outcome', 'surfable_frac_crest_line', 'surfable_frac_best_line', 'surfable_frac_israeli_tide_best_line', 'hutt_rating_range', 'volume_model_m3']].round(2).to_string(index=False))
    print(json.dumps(corr))


if __name__ == '__main__':
    main()

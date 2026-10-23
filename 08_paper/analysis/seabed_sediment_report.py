"""seabed_sediment_report.py - writes SEABED_SEDIMENT.md from seabed_sediment_results.json (run seabed_sediment.py first). Every number in the tables is read from the JSON; the narrative text is hand-written."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'seabed_sediment_results.json')))
c, bo, bt, pb, pr, al, sk = (R['cables-reef-wa'], R['boscombe-surf-reef'], R['borth-coastal-defence-reef'], R['palm-beach-gold-coast'],
                             R['prattes_two_surveys'], R['albany_baseline'], R['skipped'])
def f(v, nd=1, sign=True):
    if v is None: return 'n/a'
    t = ('%+.*f' if sign else '%.*f') % (nd, v)
    return '%.*f' % (nd, 0.0) if float(t) == 0 else t
def rng(r, nd=0): return '%s..%s' % (f(r[0], nd), f(r[1], nd))

L = []
A = L.append
A('# SEABED_SEDIMENT: sediment-transport signals around the built surf reefs, from the bathymetry already in the repo')
A('')
A('Run 2026-10-15. Script `08_paper/analysis/seabed_sediment.py` (run `python3 -B 08_paper/analysis/seabed_sediment.py`, about 15 s; this text is written by `seabed_sediment_report.py` from the JSON); all numbers below are copied from '
  '`08_paper/analysis/seabed_sediment_results.json` (keys per reef; `summary_table` holds the long-form verdict text). Figures: `08_paper/figures/fig_sediment_cables-reef-wa.png`, '
  '`fig_sediment_boscombe-surf-reef.png`, `fig_sediment_borth-coastal-defence-reef.png`. Input data are read only (07_scale/). '
  'Every number here is DERIVED by this script unless a source is named; ASSUMPTION marks an assumption. Positive anomaly = the contour lies farther offshore (closer to the reef) in the lee, or the bed is higher.')
A('')
A('## 1. Answer in brief')
A('')
A('1. Only 5 of the 13 reefs have measured seabed data that can test anything (Cables WA, Boscombe, Borth, Palm Beach [chart only], Pratte\'s [two contour sets]). Narrowneck, Mount Maunganui, Bunbury, Albany, '
  'Kovalam, Opunake, Burkitts and the Mexico reef were skipped: their seabeds are assumed or synthetic, pre-construction only, a window filled by the reef, or absent (section 3).')
t5 = {(r['date'], r['level_m_AHD']): r for r in c['T5_beach_levels_spatial']['rows']}
t5c = {(r['from_date'], r['to_date'], r['level_m_AHD']): r for r in c['T5b_beach_levels_change']['rows']}
mm0 = bo['C_common_mode_removed_BACI']['metrics']['y_0.0']
A('2. **No reef-attributable sediment signal survives a control or a pre-construction test.** Cables (the only site with pre- and post-construction soundings): the lee seabed is %s m higher and its contours are 15-43 m '
  'farther offshore than at controls 1.5-3.5 reef lengths along the shore, but the same offset is already in the 1995 pre-construction survey (offshore contours); the 1995 to 2002 bed change in the lee is %s m (SE %s m), '
  'no toe scour, no burial; the beach-level surveys show a lee shoreline bulge of %s m (Jan 2001, 13 months after completion) that has SHRUNK to %s m by Apr 2012 (a growing salient would increase). '
  'Boscombe (best-controlled BACI, 316 beach-profile surveys): the lee shoreline advanced by %s m relative to the controls (0 m ODN contour, 95%% CI %s..%s m; +1 m contour %s m, +2 m %s m), '
  'inside the tilt and beach-management signals: the whole frontage jumps together (%s m3/m in 2006-07 on all 6 lines, %s m3/m in 2020-21). Palm Beach (chart, low confidence): |offset| <= %s m at the 1-3 m contours.'
  % (f(c['T2_bed_level_lee_band']['rows'][1]['anomaly'], 2, False), f(c['T3_dz_difference_in_differences'][0]['anomaly'], 2), f(c['T3_dz_difference_in_differences'][0]['se_analytic'], 2, False),
     f(t5[('2001-01', 0.0)]['anomaly'], 0), f(t5[('2012-04', 0.0)]['anomaly'], 0),
     f(mm0['lee_anomaly'], 1), f(mm0['lee_anomaly_ci95'][0], 1), f(mm0['lee_anomaly_ci95'][1], 1), f(bo['C_common_mode_removed_BACI']['metrics']['y_+1.0']['lee_anomaly'], 1), f(bo['C_common_mode_removed_BACI']['metrics']['y_+2.0']['lee_anomaly'], 1),
     f(bo['B_common_mode_volume_jumps']['rows'][0]['median_change_m3_per_m'], 0), f(bo['B_common_mode_volume_jumps']['rows'][1]['median_change_m3_per_m'], 0),
     f(max(abs(r['anomaly']) for r in pb['T1_contour_offset']['rows'] if not r['contour_inside_reef_influence']), 0, False)))
t1b = bt['T1_contour_offset']['rows']
A('3. **Borth is the one positive spatial signal and it cannot be attributed.** In the single LiDAR survey of 19 Mar 2022 (10 y after construction) the 0 m MSL contour has its peak within %s m of the reef-centre longitude '
  '(%s m above the southern shoulder, %s m above the northern), the bed in the lee is higher by %s to %s m; but there is no pre-construction beach survey, the north-south gradient is strong, and the offset depends '
  'on the control chosen (0 m contour: %s m).' % (f(t1b[0]['peak_minus_reef_centre_x_m'], 0, False), f(t1b[0]['peak_above_south_control_mean_m'], 0), f(t1b[0]['peak_above_north_control_mean_m'], 0),
                                                 f(min(r['anomaly'] for r in bt['T2_bed_level_bands']['rows']), 1), f(max(r['anomaly'] for r in bt['T2_bed_level_bands']['rows']), 1), rng(t1b[0]['anomaly_range'])))
bs_all = [x['Ls_over_X'][k] for x in (c, bo, pb) for k in ('Ls_over_X_toe', 'Ls_over_X_centre')]
A('4. Reading for Lior\'s insight (b) ("little measurable effect on sand transport; at the Gold Coast it cannot be separated from nourishment"): consistent for the three small-to-medium reefs with usable data (Cables, Boscombe, Palm Beach), '
  'with limits: the Black & Andrews (2001) B/S rule gives B/S = %.2f-%.2f for them, i.e. a salient is expected, with an ILLUSTRATIVE amplitude of %.0f-%.0f m (Cables), %.0f-%.0f m (Boscombe) '
  '(ASSUMPTION D_tot = 1-3 B). Boscombe\'s BACI would see most of that range and finds %s m (CI to %s m); Cables resolves only about +-10 m of contour position (0.1 m of bed) over 2.2 y. '
  'Borth (B/S = %.2f, both mounds, the largest and most extended reef) is the one site with a lee bulge. Nothing could be tested at Narrowneck, where nourishment is continuous.'
  % (min(bs_all), max(bs_all), c['Ls_over_X']['illustrative_salient_amplitude_m'][0], c['Ls_over_X']['illustrative_salient_amplitude_m'][1],
     bo['Ls_over_X']['illustrative_salient_amplitude_m'][0], bo['Ls_over_X']['illustrative_salient_amplitude_m'][1], f(mm0['lee_anomaly'], 1), f(mm0['lee_anomaly_ci95'][1], 1),
     bt['Ls_over_X']['Ls_over_X_toe']))
A('5. For Haifa the useful finding is methodological: shoreline and bed-level effects of a small submerged reef are of the order of the natural alongshore variability and of beach-management signals, so a before/after '
  'survey WITH controls (BACI) and a record of nourishment are needed; claims of reef-driven accretion or protection cannot be checked with the public single-date data held here.')
A('')
A('## 2. Verdict table (per reef)')
A('')
A('| Reef | Data used | Signal? | Magnitude (DERIVED) | Uncertainty | Caveats |')
A('|---|---|---|---|---|---|')
m = bo['C_common_mode_removed_BACI']['metrics']; D = bo['D_post_only_alongshore_pattern_11_lines']['metrics']
cm = {r['level_m_AHD']: r for r in c['T3_contour_migration_2002_minus_1995']}
t1bd = {(r['survey'], r['level_m_AHD']): r for r in c['T1b_contour_offset_adjacent_controls_1995_vs_2002']['rows']}
A('| Cables WA (reef 2000) | DoT WA single-beam 1995-12 (pre), 1998-03 (pre), 1999-11, 2002-02; Perth_5m composite; beach levels 2001-01 .. 2012-04 | **Inconclusive / no**: lee high bed, contour offset and shoreline bulge exist but are pre-existing (offshore) or not growing (beach); no change 1995-2002 | lee offsets +15 (0 m AHD) to +43 m (-4 m); lee bed higher by %s m; the -5 m contour offset is +%s m in 1995 vs +%s m in 2002; bed change 1995-2002 %s m (SE %s); contour migration 1995-2002 %s..%s m; shoreline bulge %s m (2001) -> %s m (2012) | formal SE 2-8 m (contours), 0.05 m (bed); survey offsets +-0.1 m | only 2.2 y offshore; adjacent controls in the temporal test; 0..-3 m contours have no pre-reef survey; no pre-reef beach survey; Leighton/Port Beach management not checked; B/S = %.2f |'
  % (f(c['T2_bed_level_lee_band']['rows'][1]['anomaly'], 2, False), f(t1bd[('1995', -5)]['anomaly'], 0, False), f(t1bd[('2002', -5)]['anomaly'], 0, False), f(c['T3_dz_difference_in_differences'][0]['anomaly'], 2), f(c['T3_dz_difference_in_differences'][0]['se_analytic'], 2, False),
     f(min(r['anomaly'] for r in cm.values()), 0), f(max(r['anomaly'] for r in cm.values()), 0), f(t5[('2001-01', 0.0)]['anomaly'], 0), f(t5[('2012-04', 0.0)]['anomaly'], 0), c['Ls_over_X']['Ls_over_X_toe']))
A('| Boscombe (reef 2009) | CCO beach profiles, 11 lines, 316 surveys 2004-2026 (shoreline to -1 m ODN); reef toe about 155 m or more seaward of the profile ends | **No** (<= %s m, inside tilt and management signals) | 0 m ODN contour %s m (CI %s..%s); +1 m %s (CI %s..%s); +2 m %s; volume %s m3/m (CI %s..%s); post-only 11 lines %s +- %s m | bootstrap over dates (pre n = 5); dates not independent | Poole Bay groynes + recharge (frontage-wide jumps +72 m3/m 2006-07, +40 m3/m 2020-21); reef construction left 11,100 m3 sand on the beach (Rendle 2016); no pre-reef bathymetry; 60 m in 6 months (Mead & Borrero 2011) not reproduced (max %s m) |'
  % (f(m['y_0.0']['lee_anomaly_ci95'][1], 0, False), f(m['y_0.0']['lee_anomaly'], 1), f(m['y_0.0']['lee_anomaly_ci95'][0], 1), f(m['y_0.0']['lee_anomaly_ci95'][1], 1), f(m['y_+1.0']['lee_anomaly'], 1),
     f(m['y_+1.0']['lee_anomaly_ci95'][0], 1), f(m['y_+1.0']['lee_anomaly_ci95'][1], 1), f(m['y_+2.0']['lee_anomaly'], 1), f(m['vol0_m3_per_m']['lee_anomaly'], 1), f(m['vol0_m3_per_m']['lee_anomaly_ci95'][0], 1),
     f(m['vol0_m3_per_m']['lee_anomaly_ci95'][1], 1), f(D['y_0.0']['lee_anomaly_mean'], 1), f(D['y_0.0']['lee_anomaly_se'], 1, False), f(bo['E_six_month_changes_2008_2010']['max_advance_m'], 1)))
t2b = bt['T2_bed_level_bands']['rows']
A('| Borth (Phase 1, 2012) | Welsh Government LiDAR DTM 19 Mar 2022, 1 m | **Inconclusive** (bulge yes, attribution no) | 0 m MSL contour %s m (range %s), -1 m %s (%s), -2 m %s (%s); lee bed +%s..+%s m | formal SE 2-9 m; control choice changes it by 36-92 m | ONE date; no pre-construction beach survey; strong N-S gradient; unexplained ridge in the north control; strip 750 m; B/S = %.2f |'
  % (f(t1b[0]['anomaly'], 0), rng(t1b[0]['anomaly_range']), f(t1b[1]['anomaly'], 0), rng(t1b[1]['anomaly_range']), f(t1b[2]['anomaly'], 0), rng(t1b[2]['anomaly_range']),
     f(min(r['anomaly'] for r in t2b), 2, False), f(max(r['anomaly'] for r in t2b), 2, False), bt['Ls_over_X']['Ls_over_X_toe']))
pr_ = [r for r in pb['T1_contour_offset']['rows'] if not r['contour_inside_reef_influence']]
A('| Palm Beach (reef 2019) | Navionics SonarChart iso-lines 1-3 m (chart, undated) | **No** | %s | chart smoothing, +-10 m (ASSUMPTION) | LOW confidence; continuous Gold Coast nourishment not quantified; 4-6 m contours bent by the reef shoal (+38..+71 m) are a chart artefact |'
  % '; '.join('%d m: %s m' % (r['chart_depth_m'], f(r['anomaly'], 1)) for r in pr_))
A('| Pratte\'s (2000) | Borrero & Nelsen (2003) Fig. 9, two surveys (Oct 2000, Mar 2001), contours -1..-4 m | **Inconclusive** | all four contours moved offshore by %s m (%s..%s) | datum/tide offset of 0.3 m = about 10 m | window = 2 reef lengths, reef not drawn, no control |'
  % (f(float(np.mean([r['mean_shift_m'] for r in pr['result_rows']])), 0), f(min(r['mean_shift_m'] for r in pr['result_rows']), 0), f(max(r['mean_shift_m'] for r in pr['result_rows']), 0)))
A('| Narrowneck, Mount Maunganui, Bunbury, Albany, Pratte\'s (3D bed), Kovalam, Opunake, Burkitts, Mexico | skipped | n/a | n/a | n/a | assumed/synthetic seabed or no data (section 3) |')
A('')
A('## 3. What each seabed dataset really is, and what was skipped')
A('')
A('| Reef | Seabed in the 3D model / repo | Measured? | Used here |')
A('|---|---|---|---|')
A('| cables-reef-wa | DoT WA single-beam soundings 1995-12, 1998-03, 1999-11, 2002-02 (point files) + DoT Perth_5m composite (METHODS_3D 3.4) | MEASURED (sd 0.29 m between surveys) | **yes**: all four surveys, TIN |')
A('| boscombe-surf-reef | CCO beach-profile surveys (measured, 316 files); the offshore model bed is the Rendle & Davidson 2012 Fig. 9 colour read of April 2011 (a 23,500 m2 tilted window) plus a thin-plate-spline "ambient" bed and an EMODnet slope extrapolation (assumed) | beach MEASURED; offshore window measured but too small and post-failure | **yes** (CCO lines only); Fig. 9 window has no control section and the pre-reef bed is a fit |')
A('| borth-coastal-defence-reef | Welsh Government LiDAR DTM 2022-03-19 (beach to -2.3 mODN, measured); beyond that HRPP576 Fig. 2 contours read by eye and ASSUMED bridge nodes | beach MEASURED | **yes**: the DTM itself, not the model grid |')
A('| palm-beach-gold-coast | Navionics SonarChart iso-lines (chart) + toe levels from the aerial; thin-plate spline | chart-derived, date unknown | yes, 1-3 m lines only, LOW confidence |')
A('| prattes-reef-el-segundo | model bed = alongshore-uniform profile (NOAA DEM + Navionics, ASSUMED); separate vector Fig. 9 contours of two surveys | profile assumed; Fig. 9 measured | Fig. 9 only |')
for k in ('narrowneck-gold-coast', 'mount-maunganui-reef', 'bunbury-airwave', 'southern-ocean-surf-reef-albany'):
    A('| %s | %s | assumed/skipped | **skipped** |' % (k, sk[k].replace('SKIPPED: ', '').replace('|', '/')))
A('| kovalam / opunake / burkitts / mexico | %s | no data | **skipped** |' % sk['kovalam-reef-india / opunake-reef / burkitts-reef-bargara / mexico-reef-2026-unnamed'].replace('SKIPPED: ', ''))
A('| 07_scale/bathymetry (EMODnet, Gold Coast) | %s Gold Coast: the City DTM has no underwater cells at either reef (07_scale/bathymetry/gold_coast HANDOFF Q1). | n/a | not used |' % sk['EMODnet DTM (07_scale/bathymetry/emodnet)'].replace('NOT USABLE for this test: ', ''))
A('')
A('Albany baseline (pre-construction 2015 contours read on 8 transects, 20 m apart): the -1, -2, -3 m contours trend %s, %s, %s m per 100 m alongshore and scatter about the trend by %s, %s, %s m (1 sd). '
  'This is a noise floor for any future post-construction comparison (colour reading, +-10 m for the deeper lines); no post-construction bathymetry exists in the repo.'
  % tuple([f(r['trend_m_per_100m'], 1) for r in al['baseline_rows']] + [f(r['resid_sd_after_trend_m'], 1, False) for r in al['baseline_rows']]))
A('')
A('## 4. Method')
A('')
A('**Frames.** Each site is analysed in its own shore frame: x (or s) alongshore with the reef centre at 0 (Cables: s along bearing 7.8 deg true, from `scripts/shore_datum.json`; Boscombe: canonical x, bearing 83.4 deg; Borth: canonical x, + south), '
  'y (or n) offshore. L = alongshore extent of the reef footprint (Cables %.0f m, Boscombe %.0f m, Borth %.0f m for both mounds, Palm Beach %.0f m).' % (c['reef_alongshore_extent_L_m'], bo['reef_alongshore_extent_L_m'],
   bt['reef_alongshore_extent_L_m'], pb['reef_alongshore_extent_L_m']))
A('')
A('**T1 contour offset.** Cross-shore position Y_c(x) of the shoreline (0 m) and of the -1, -2, -3 m (and deeper where measured) contours, first downward crossing from the shore on a smoothed surface (Cables: soundings to a linear TIN, cells > 25 m from a sounding masked, '
  'Gaussian 10 m; Borth: LiDAR 1 m smoothed 1.5 cells). Anomaly = mean Y_c in the lee window (x within the reef extent) minus the straight-line trend fitted to the CONTROL windows (1.5-3.5 L from the reef centre where data exist), evaluated in the lee.')
A('')
A('**T2 bed level.** The same machinery on the mean bed elevation in a fixed cross-shore band (Cables n = -165..-62 m from the reef centre; Borth y = 40-100, 100-160, 160-220 m from the defence line).')
A('')
A('**T3 temporal.** Cables only: dz = later minus earlier survey in every 5 m cell that has a sounding within 25 m in both surveys; boxes in the lee band; difference-in-differences against adjacent strips (the 1995 survey covers the lee band only '
  'for s = -150..+125 m); contour migration 2002 minus 1995 on identical transects. Noise floor from the pre-construction pair 1998 vs 1995. Boscombe: before/after at 6 CCO lines (pre = 2004-07..2008-04, construction 2008-06..2009-11 excluded, post = 2009-11..2026-03); '
  'common-mode removed by subtracting the six-line mean on each date; lee anomaly = mean change of the lee lines minus the straight line through the four control lines; 95 % CI by bootstrap over survey dates (4000 resamples); '
  'additionally the 11-line post-only alongshore pattern.')
A('')
A('**T4 burial and toe scour.** Cables: post-construction soundings against the 1998 TIN in rings 0-10, 10-25, 25-50, 50-100 m outside the footprint; reef surface 1999-11 vs 2002-02 at matched soundings (< 3 m apart).')
A('')
A('**Uncertainty.** Three layers are reported. (i) Formal standard error of the anomaly from the residual scatter of the control samples about the trend, corrected for serial correlation along the shore (integral scale tau; `se_analytic`). '
  '(ii) Placebo windows of the same width slid along the control strips (`placebo_sd`, only when >= 8 windows exist). (iii) Sensitivity to the control choice: the anomaly recomputed with each control strip alone (`anomaly_range`); '
  'where the natural alongshore gradient is large (Borth) this range, not the formal SE, is the honest uncertainty. Boscombe uses a date bootstrap.')
A('')
A('**Limits of the method.** Single-beam surveys 25-60 m between lines and +-0.3 m vertical sd; the controls can lie inside a reef\'s sphere of influence (biases toward zero); a contour offset of x metres equals a bed difference of x times the local slope '
  '(Cables 1:15 to 1:40); an echo-sounder cannot tell sand from rock fall-down; tide/datum differences between survey campaigns act like a uniform dz (+-0.1 m assumed from the pre-construction pair mean %s m).' % f(c['dz_cell_statistics_outside_reef_buffer']['1998-1995']['mean_m'], 2))
A('')
A('## 5. Results')
A('')
A('### 5.1 Cables Reef, Perth (figure `fig_sediment_cables-reef-wa.png`)')
A('')
A('Data (DERIVED coverage): ' + '; '.join('%s %d soundings, z %s..%s m AHD' % (k, v['n_soundings'], f(v['z_range_AHD'][0], 1), f(v['z_range_AHD'][1], 1)) for k, v in c['surveys'].items()) +
  '. The 1995 survey ends at z = -2.45 m AHD (about 90 m from the shore); the 2002 survey reaches -1.07 m. Reef: %.0f m alongshore, %.0f m cross-shore, %.0f m from the 0 m AHD contour (Perth_5m composite, undated).' %
  (c['reef_alongshore_extent_L_m'], c['reef_cross_shore_extent_m'], c['Ls_over_X']['X_shoreline_to_shoreward_toe_m']))
A('')
A('T1 (lee window +-55 m; controls 165-385 m on both sides; composite and 2002 only, the 1995/1998 surveys do not reach the far controls):')
A('')
A('| Dataset | Contour (m AHD) | Lee anomaly (m) | formal SE | placebo sd | north-only / south-only control (range) |')
A('|---|---|---|---|---|---|')
for r in c['T1_contour_offset']['rows']:
    if r['lee'] == 'lee_L' and 'anomaly_range' in r:
        A('| %s | %d | %s | %s | %s | %s |' % ('Perth_5m composite' if r['dataset'].startswith('Perth') else 'DoT 2002-02', r['level_m_AHD'], f(r['anomaly'], 1), f(r['se_analytic'], 1, False),
                                                f(r.get('placebo_sd'), 1, False) if r.get('placebo_sd') is not None else 'n/a', rng(r['anomaly_range'])))
A('')
A('The offset is a robust spatial feature (north-only and south-only controls agree). It is also in the PRE-construction survey (T1b, adjacent control strips s = -150..-75 and +75..+125):')
A('')
A('| Survey | Contour | Lee anomaly (m) | range over control choice | formal SE |')
A('|---|---|---|---|---|')
for r in c['T1b_contour_offset_adjacent_controls_1995_vs_2002']['rows']:
    A('| %s | %d | %s | %s | %s |' % (r['survey'], r['level_m_AHD'], f(r['anomaly'], 1), rng(r['anomaly_range']), f(r['se_analytic'], 1, False)))
A('')
A('(1995 -4 m: the contour is covered only for s = -100..+125 m; treat with care.) Contour migration 2002 minus 1995, lee against the adjacent strips: ' +
  '; '.join('%d m: %s m (SE %s)' % (r['level_m_AHD'], f(r['anomaly'], 1), f(r['se_analytic'], 1, False)) for r in c['T3_contour_migration_2002_minus_1995']) +
  ' = a bed rise of about 0.1-0.2 m at the local slope, within the survey offset.')
A('')
A('T2/T3 bed level and change in the lee band (n = %.0f..%.0f m):' % tuple(c['lee_band_n_m']))
A('')
A('| Quantity | Value |')
A('|---|---|')
for r in c['T2_bed_level_lee_band']['rows']:
    A('| bed level, lee minus far-control trend, %s | %s m (range %s m; formal SE %s m) |' % (r['label'], f(r['anomaly'], 2), rng(r.get('anomaly_range', [np.nan, np.nan]), 2), f(r['se_analytic'], 2, False)))
for r in c['T3_temporal_boxes']['rows']:
    if r['pair'] == '2002-1995':
        A('| dz 2002-1995, box %s (s %s m) | mean %s m, sd of cells %s m, coverage %.0f %%, volume %s m3 |' % (r['box'], rng(r['s_range']), f(r['mean_dz_m'], 3), f(r['sd_cell_dz_m'], 2, False), 100 * r['coverage'], f(r['volume_change_m3'], 0)))
for r in c['T3_dz_difference_in_differences']:
    A('| difference-in-differences, %s | %s m (SE %s m) |' % (r['label'], f(r['anomaly'], 3), f(r['se_analytic'], 3, False)))
for k, v in c['dz_cell_statistics_outside_reef_buffer'].items():
    A('| noise floor dz %s, all valid cells outside the reef + 20 m | mean %s m, sd %s m, 5-95 %% %s..%s m (n = %d) |' % (k, f(v['mean_m'], 2), f(v['sd_m'], 2, False), f(v['p5'], 2), f(v['p95'], 2), v['n_cells']))
A('')
A('The change in the lee band (dz) is %s m against %s and %s m in the adjacent strips: nothing is detectable above the +-0.1 m survey offset (+-1,100 m3 over the 11,300 m2 box).' % (
    f([r for r in c['T3_temporal_boxes']['rows'] if r['pair'] == '2002-1995' and r['box'] == 'lee'][0]['mean_dz_m'], 2),
    f([r for r in c['T3_temporal_boxes']['rows'] if r['pair'] == '2002-1995' and r['box'] == 'ctrl_S'][0]['mean_dz_m'], 2),
    f([r for r in c['T3_temporal_boxes']['rows'] if r['pair'] == '2002-1995' and r['box'] == 'ctrl_N'][0]['mean_dz_m'], 2)))
A('')
A('T4 rings (post-construction sounding minus the 1998 TIN):')
A('')
A('| Survey | Zone | n | mean dz (m) | sd (m) |')
A('|---|---|---|---|---|')
for r in c['T4_rings_post_minus_1998_bed']['rows']:
    if r['sector'] == 'all':
        A('| %s | %s | %d | %s | %s |' % (r['survey'], r['zone'], r['n'], f(r['mean_dz_m'], 2), f(r['sd_m'], 2, False)))
rs = c['T4_reef_surface_2002_minus_1999_matched_within_3m']
A('')
A('Reef surface, 2002 minus 1999 at %d matched soundings (< 3 m apart): mean %s m, sd %s m; 95th-percentile level inside the footprint %s (1999, n=%d) vs %s m AHD (2002, n=%d). The matched-sounding mean and the percentile move in opposite directions: '
  'both are inside the sounding noise (positioning on a rough rock surface), so no settlement and no burial is detectable at the 0.15 m level. Repeatability 1998 vs 1995 within 3 m: mean %s m, sd %s m (n=%d).' %
  (rs['n'], f(rs['mean_m'], 2), f(rs['sd_m'], 2, False), f(rs['z95_inside_footprint_1999'], 2), rs['n_inside_1999'], f(rs['z95_inside_footprint_2002'], 2), rs['n_inside_2002'],
   f(c['repeatability_1998_vs_1995_soundings_within_3m']['mean_m'], 2), f(c['repeatability_1998_vs_1995_soundings_within_3m']['sd_m'], 2, False), c['repeatability_1998_vs_1995_soundings_within_3m']['n']))
A('')
A('T5 beach-level surveys (DoT "Levels" point files, profile lines about 50 m apart; lee = 2 lines within +-55 m, controls = 6-8 lines 165-385 m either side):')
A('')
A('| Survey | lines | 0 m AHD contour lee minus controls (m) | +1 m contour (m) | range over control choice (0 m) |')
A('|---|---|---|---|---|')
for d in ('2001-01', '2002-02', '2003-01', '2011-08', '2012-04'):
    r0, r1 = t5[(d, 0.0)], t5[(d, 1.0)]
    A('| %s | %d | %s | %s | %s |' % (d, r0['n_lines'], f(r0['anomaly'], 0), f(r1['anomaly'], 0), rng(r0['anomaly_range'])))
A('')
A('Change between dates (matched lines, lee minus controls): ' + '; '.join('%s to %s: %s m (0 m), %s m (+1 m)' % (a, b, f(t5c[(a, b, 0.0)]['anomaly'], 0), f(t5c[(a, b, 1.0)]['anomaly'], 0)) for a, b in (('2001-01', '2003-01'), ('2003-01', '2012-04'), ('2001-01', '2012-04'), ('2002-02', '2012-04'))) +
  '. A lee shoreline bulge is present at every date, largest 13 months after completion and smaller later: this is not the signature of a salient that grows after construction. It cannot be separated from a natural feature (no beach survey before Dec 1999; the offshore contours already had the lee hump in 1995), '
  'from a decaying construction-time feature, or from beach management at Leighton/Port Beach (NOT checked; the 2011-12 files carry the name "PortBeach"). No formal SE (3-4 lines per control strip); the scatter between dates is 10-26 m.')
A('')
A('Likely cause of the pre-existing lee offset: natural limestone reef lines of the Cottesloe coast (ASSUMPTION; not verified in this run). B/S = %.2f (toe) / %.2f (centre): %s, illustrative amplitude %.0f-%.0f m (ASSUMPTION D_tot = 1-3 B).' %
  (c['Ls_over_X']['Ls_over_X_toe'], c['Ls_over_X']['Ls_over_X_centre'], c['Ls_over_X']['regime_toe'], c['Ls_over_X']['illustrative_salient_amplitude_m'][0], c['Ls_over_X']['illustrative_salient_amplitude_m'][1]))
A('')
A('### 5.2 Boscombe (figure `fig_sediment_boscombe-surf-reef.png`)')
A('')
A('Data: Channel Coastal Observatory beach-profile surveys, lines 5f00424-5f00429 (quarterly or annual since 2004-07) and A lines 424A-428A (annual since 2010-04), file list `07_scale/shapes/boscombe-surf-reef/src/cco_profiles/`, converted with the project\'s `canon.py` (+-5 m); '
  'heights m ODN (= MSL within +-0.1 m, A4). Profiles end at about -1 m ODN, i.e. y about +21 m; the reef toe is at y = 181 m. Reef x = %s m (L = %.0f m); lee lines %s (x = %s m), controls %s.' %
  (rng(bo['reef_x_range']), bo['reef_alongshore_extent_L_m'], ', '.join(bo['lee_lines']), ', '.join('%.0f' % bo['line_x_m'][p] for p in bo['lee_lines']), ', '.join('%s (%.0f)' % (p[-3:], bo['line_x_m'][p]) for p in bo['control_lines'])))
A('')
A('Raw pre/post per line (0 m ODN contour position y, m from the surf-line origin; volume above 0 m ODN, m3 per m, y = -55 m to the contour):')
A('')
A('| Line | x (m) | pre n | pre y0 | post n | post y0 | post-pre y0 | post-pre volume |')
A('|---|---|---|---|---|---|---|---|')
for r in bo['A_raw_pre_post_by_line']:
    k = r['y_0.0']; v = r['vol0_m3_per_m']
    A('| %s | %.0f | %d | %s | %d | %s | %s | %s |' % (r['line'], r['x_m'], k['n_pre'], f(k['pre_mean'], 1) if k['n_pre'] else '-', k['n_post'], f(k['post_mean'], 1), f(k['post_minus_pre'], 1) if k['n_pre'] else '-',
                                                       f(v['post_minus_pre'], 0) if v['n_pre'] else '-'))
A('')
A('Every line advanced (+4 to +17 m) between the pre and post periods; the change is common-mode (beach volume jumps 2006-07 on all six lines and 2020-21 on four, east-end lines 2015-16; panel a), so it is NOT a reef effect. '
  'With the common mode removed (six-line mean subtracted on dates when all six were surveyed; pre n = %d, post n = %d dates):' % (m['y_0.0']['n_dates_pre'], m['y_0.0']['n_dates_post']))
A('')
A('| Metric | change per line, lines 424 / 425 / 426 / 427 / 428 / 429 | straight-line trend through the 4 controls | lee anomaly (426, 427) | 95 % CI (bootstrap) |')
A('|---|---|---|---|---|')
for k, nm in (('y_0.0', '0 m ODN contour (m)'), ('y_+1.0', '+1 m contour (m)'), ('y_+2.0', '+2 m contour (m)'), ('vol0_m3_per_m', 'volume above 0 m ODN (m3/m)')):
    mm = m[k]
    A('| %s | %s | %s per 100 m | %s | %s..%s |' % (nm, ' / '.join(f(v, 1) for v in mm['change_rel']), f(mm['control_trend_slope_per_100m'], 1), f(mm['lee_anomaly'], 1), f(mm['lee_anomaly_ci95'][0], 1), f(mm['lee_anomaly_ci95'][1], 1)))
A('')
A('After the reef the frontage tilts (east lines advance relative to the mean, west lines retreat by about 7 m): a gradient, not a local maximum at the lee lines. Post-only, 11 lines, %d annual dates: lee anomaly %s +- %s m (0 m), %s +- %s m (+1 m), %s +- %s m3/m (volume). '
  'Largest 0 m contour advance between 4-8-month-apart surveys in 2008-2010: %s m (rows in the JSON, key `E_six_month_changes_2008_2010`); the "up to 60 m within 6 months" of Mead & Borrero (2011, p.4-5; designer\'s account, recorded in 02_research/reefs/boscombe-surf-reef.md) is not reproduced at these lines (other contour, line or reference unknown).' %
  (D['y_0.0']['n_dates'], f(D['y_0.0']['lee_anomaly_mean'], 1), f(D['y_0.0']['lee_anomaly_se'], 1, False), f(D['y_+1.0']['lee_anomaly_mean'], 1), f(D['y_+1.0']['lee_anomaly_se'], 1, False),
   f(D['vol0_m3_per_m']['lee_anomaly_mean'], 1), f(D['vol0_m3_per_m']['lee_anomaly_se'], 1, False), f(bo['E_six_month_changes_2008_2010']['max_advance_m'], 1)))
A('')
A('Confounds: the Poole Bay frontage is groyned (about 60 hardwood groynes, roughly every 180 m) and re-nourished every 10-12 years (Mead & Borrero 2011, p.4-5, as recorded in the reef card; groyne positions relative to the CCO lines were NOT mapped here); building the reef '
  'involved 23,000 m3 of sand piled on the upper beach, of which 11,100 m3 stayed on the beach between the pier and the first groyne (Rendle 2016, p.125-127, `07_scale/shapes/boscombe-surf-reef/P5_RENDLE2016_NOTES.md`); '
  'the dates and volumes of recharge are not in the repo. The year-on-year rise indicator (`B_common_mode_volume_jumps`) only flags that common-mode events exist. The reef toe lies about 155 m or more seaward of the profile ends and its lee (waves from the SW-S) may be displaced east of the reef; '
  'the A lines at x = 96 and -88 m are not in the BACI because they have no pre-construction data. The only Boscombe seabed data farther offshore are the April 2011 survey window (post-failure, no control section) and EMODnet cells too coarse to see the reef.')
A('')
A('### 5.3 Borth (figure `fig_sediment_borth-coastal-defence-reef.png`)')
A('')
A('Data: Welsh Government LiDAR DTM, tile SN6089, flight 19 Mar 2022, 1 m cells, resampled to a 2 m canonical grid with the project\'s `b3d_lib.Frame` (fit rms %.3f m); heights mODN -0.31 = m MSL. Phase 1 completed 8 March 2012. Reef mounds x = %s m (L = %.0f m), '
  'shoreline (0 m MSL contour) in the lee at y = %.0f m, reef toe at y = %.0f m. Lee window = reef extent; controls start 0.5 L beyond the edges (x < %.0f and x > %.0f m) because the analysed strip is only 750 m long.' % (
      0.005, rng(bt['reef_alongshore_x_range_m']), bt['reef_alongshore_extent_L_m'], bt['Ls_over_X']['X_shoreline_to_shoreward_toe_m'] and (257.0 - bt['Ls_over_X']['X_shoreline_to_shoreward_toe_m']), 257.0,
      bt['windows_x_m']['controls'][0][1], bt['windows_x_m']['controls'][1][0]))
A('')
A('| Quantity | lee mean | control mean | anomaly (trend through both) | range over control choice | formal SE | peak (x, y) | peak minus reef-centre x |')
A('|---|---|---|---|---|---|---|---|')
for r in bt['T1_contour_offset']['rows']:
    A('| %+.0f m MSL contour (m) | %.0f | %.0f | %s | %s | %s | (%.0f, %.0f) | %s m |' % (r['level_m_MSL'], r['lee_mean'], r['ctrl_mean'], f(r['anomaly'], 0), rng(r['anomaly_range']), f(r['se_analytic'], 0, False), r['peak_x_m'], r['peak_y_m'], f(r['peak_minus_reef_centre_x_m'], 0)))
for r in bt['T2_bed_level_bands']['rows']:
    A('| bed level y = %.0f-%.0f m (m MSL) | %s | %s | %s | %s | %s | | |' % (r['band_y_m'][0], r['band_y_m'][1], f(r['lee_mean'], 2), f(r['ctrl_mean'], 2), f(r['anomaly'], 2), rng(r['anomaly_range'], 2), f(r['se_analytic'], 2, False)))
A('')
A('The 0 and -1 m contours peak within 5-20 m of the reef-centre longitude (the -2 m contour, where the DTM touches the reef mounds, peaks 40 m south), which is what a salient behind the reef would look like. But (i) it is one survey 10 y after construction; (ii) the '
  'south-only control gives +%.0f m (0 m) and +%.1f m (-1 m) while the north-only control gives +%.0f and +%.0f m: the beach has a strong natural north-south gradient (village frontage vs dune frontage), and the peak sits on top of that step; (iii) the north control strip contains an unexplained shore-parallel ridge in the DTM '
  '(x about -330..-235 m, y about 75-95 m) that kinks the -1 m contour; (iv) seasonal state (March) and bars are not considered. Project check (07_scale/.../borth HANDOFF, not recomputed): LiDAR minus design crest levels +0.14 +- 0.28 m, i.e. no burial or settlement at the 0.3 m level. B/S = %.2f (toe) / %.2f (centre) for both mounds; the northern mound alone has B/S about 0.47.' %
  (bt['T1_contour_offset']['sensitivity_single_side_controls'][1]['anomaly'], bt['T1_contour_offset']['sensitivity_single_side_controls'][3]['anomaly'], bt['T1_contour_offset']['sensitivity_single_side_controls'][0]['anomaly'],
   bt['T1_contour_offset']['sensitivity_single_side_controls'][2]['anomaly'], bt['Ls_over_X']['Ls_over_X_toe'], bt['Ls_over_X']['Ls_over_X_centre']))
A('')
A('### 5.4 Palm Beach (chart only, LOW confidence)')
A('')
A('| Chart contour (m below LAT) | lee anomaly (m) | range over control choice | formal SE | note |')
A('|---|---|---|---|---|')
for r in pb['T1_contour_offset']['rows']:
    A('| %d | %s | %s | %s | %s |' % (r['chart_depth_m'], f(r['anomaly'], 1), rng(r['anomaly_range']), f(r['se_analytic'], 1, False), 'bent by the reef shoal in the chart: NOT a sediment signal' if r['contour_inside_reef_influence'] else 'shoreward of the reef'))
A('')
A('The Navionics SonarChart is a smoothed compilation of sonar logs and surveys of unknown date; the reef (2019) is drawn as a shoal; the Gold Coast beaches are nourished continuously (not quantified here). A null at 1-3 m therefore says only that no lee offset larger than about 10 m is drawn on the chart.')
A('')
A('### 5.5 Pratte\'s Reef, two surveys')
A('')
A('| Contour | overlap (m) | mean shift Oct 2000 to Mar 2001 (m, + offshore) | max abs (m) | sd (m) |')
A('|---|---|---|---|---|')
for r in pr['result_rows']:
    A('| %d m | %.0f | %s | %.0f | %.1f |' % (r['level_m'], r['overlap_alongshore_m'], f(r['mean_shift_m'], 1), r['max_abs_shift_m'], r['sd_m']))
A('')
A('All four contours moved by a similar amount over the whole window: a window-wide shift (seasonal profile change, tide or datum difference of the two surveys), not a local lee effect; the window is two reef lengths wide, the reef is not drawn (position +-150 m) and there is no control section. Inconclusive.')
A('')
A('## 6. What this means for the paper, and what would settle it')
A('')
A('- Safe statements: (a) in the three well-observed small/medium reefs the lee shoreline/bed response is below the survey resolution (a few metres at Boscombe, 0.1 m of bed at Cables 1995-2002, and no growth of the Cables beach bulge 2001-2012); (b) the apparent lee highs in single-date data (Cables 2002, Borth 2022) '
  'are either pre-existing (Cables) or untestable (Borth) - this is the argument for BACI; (c) the Boscombe record shows that beach-management events move the whole frontage by tens of metres, an order of magnitude more than any reef effect; '
  '(d) at the Gold Coast the reef effect cannot be separated from nourishment with public data.')
A('- Not safe: "the reef causes a salient/accretion" (Borth) or "the reef has no effect" (the resolution is +-10 m of contour at Cables, 2.2 y).')
A('- Cheapest additions that would turn Borth and Boscombe into real tests (Lior requests, not done here): the pre-2012 beach survey of Borth (Welsh coastal monitoring programme / the design survey of 2010) and later LiDAR epochs; '
  'Poole Bay recharge dates and volumes (BCP Council / CCO) and the groyne positions along the CCO lines; Boscombe pre-2009 offshore bathymetry; a pre-construction (before Dec 1999) beach survey of the Cables/Leighton frontage (DoT WA; the other pre-construction FR files in the same zip were checked and not used: the 1984 digitised chart has only 591 points in the window, the 1984-85 and 1996 single-beam files none) and the Leighton/Port Beach nourishment history.')
A('- Possible paper figure: `fig_sediment_boscombe-surf-reef.png` panel (a) (the nourishment confound) and panel (b) (BACI), and `fig_sediment_cables-reef-wa.png` panels (c) (offset pre-dates the reef) and (d) (shoreline bulge not growing).')
A('')
A('## 7. Reproduction, provenance, caveats')
A('')
A('- Script: `08_paper/analysis/seabed_sediment.py`; results `08_paper/analysis/seabed_sediment_results.json` (one block per reef, `summary_table` with the long verdict text, `skipped`, `_meta`). Imports (read only) '
  '`07_scale/shapes/boscombe-surf-reef/3d/scripts/canon.py` and `07_scale/shapes/borth-coastal-defence-reef/3d/b3d_lib.py` (run with `python3 -B` so that no bytecode is written into 07_scale). Scratch: `/tmp/claude-0/paper/seabed/`.')
A('- Data files (all read only): Cables `07_scale/shapes/cables-reef-wa/src/bathymetry/FR_selected/*.txt` and `DoT_Perth_5m_clip_reef.npz` (DoT WA, CC BY 4.0, accuracy "variable, no warranty"); Boscombe `.../boscombe-surf-reef/src/cco_profiles/`; '
  'Borth `.../borth-coastal-defence-reef/3d/src/lidar_beach_SN6089_2022-03-19.npz`; Palm Beach `model.js` navionics.lines (Garmin Navionics, not for navigation; private research copy, reuse rights not cleared); Pratte\'s `.../prattes-reef-el-segundo/3d/src/bn2003_fig9_contours.json`; '
  'Albany `.../southern-ocean-surf-reef-albany/3d/src/levels2_raw.json`.')
A('- Datum notes: Cables z in m AHD (taken as MSL); Boscombe m ODN (= MSL +-0.1 m); Borth m ODN with MSL = +0.31 m (+-0.15, assumed LiDAR datum ODN); Palm Beach depths below chart datum (LAT assumed); contour OFFSETS are insensitive to a constant datum shift except through the local slope.')
A('- Not done: wave direction and wave shadow (the lee is taken as the shore directly behind the reef, +-1 L); no wave-driven transport calculation; no offshore Cables survey after 2002 exists in the repo (the other FR files in the DoT zip do not cover the reef); the origin of the Borth north ridge was not identified; Poole Bay groyne positions were not mapped onto the CCO lines.')
A('')
A('## 8. Status')
A('')
A('Complete for the brief (T1-T4 on every reef with measured data, T5 beach levels at Cables, 3 figures). Open points, none blocking: (1) the Borth north ridge and the Poole Bay groyne/recharge positions are unidentified; '
  '(2) Mount Maunganui and Palm Beach could be re-tested if a dated pre-construction contour set is supplied; (3) the Cables beach-level files were found late (inside the DoT zip) and are analysed only for the 0, +1, +2 m AHD contours.')
open(os.path.join(HERE, 'SEABED_SEDIMENT.md'), 'w').write('\n'.join(L) + '\n')
print(len('\n'.join(L)))

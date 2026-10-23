# FIGURE_SPECS: result figures F3-F9 (data, columns, axes, annotations)

> Update 2026-10-20: the recommended Haifa crest is now 1.0 to 1.2 m below MSL (was 0.6 to 1.0 m), about 14,000 to 20,000 m3 per 100 m; basis: model breaking depths (gamma 0.78) plus at least 0.5 m of water over the crest at the 1-year low level (-0.38 m MSL). Field breaking depths are indicative only. See 08_paper/sections/07_israel.md section 7.5. Older statements below are superseded.

Status 2026-10-16. For the figure agent. Shared style: `08_paper/analysis/style.py` (one colour + marker per reef: COLORS, MARKERS,
NAMES; neutral SEA/SAND/SEABED/TIDE; FULL_W 17 cm, COL_W 8.3 cm; `save(fig, name)` writes PDF + PNG to 08_paper/figures/).
Outcome encoding used in F4-F6 and F9 (one scheme everywhere): works = filled marker; works rarely / mixed = half-filled (or
open with thick edge); does not work = open marker with an x; unknown = grey. Keep the reef colour for identity. All data files
are in `08_paper/analysis/` unless a path is given; every number on a figure must come from these files. Caption sources: the
RESULTS.md section named per figure. Units: m, s, deg; depths positive downward in labels, z negative below MSL in data.

## F3 Wave over the reef, to scale (two panels, full width, ~17 x 9 cm) - RESULTS s2-s3, insight f/d

Panel (a) "Long gradual ramp" = Palm Beach crest line; panel (b) "Abrupt rise" = Boscombe crest line (idealised 1:3 flank). Same
scales in both panels, vertical exaggeration stated in the caption (suggest 1:5; also draw a 1:1 inset of the 30 m around the
break so the surfer and wave are true to scale).
- Data: `08_paper/data/profiles/palm-beach-gold-coast.json` and `.../boscombe-surf-reef.json`, `lines.crest_line.profile`
  (`offshore_m`, `seabed_msl_m`, `reef_msl_m`, null = no reef); `lines.crest_line.metrics` (crest_z_msl_m, seaward toe, ramp length,
  mean slope). Break point: `results_surf_site.csv` rows slug = palm-beach-gold-coast / boscombe-surf-reef, tide = mid
  (columns y_break, d_break, H_break, xi_b, breaker, vortex_Y, vortex_class, skill). Use the same H0 in both panels for comparison:
  add Boscombe at H0 = 1.0 m, T = 10 s from `results_breaking.csv` (slug, line = crest_line, H0 = 1.0, T = 10, tide = mid,
  gamma_mode = mccowan) and Palm Beach at the same row; show the site wave (Palm 1.0 m 10 s; Boscombe 0.5 m 8 s) as text.
- Axes: x = offshore distance (m), plotted shoreward to the right, window from 30 m seaward of the outer toe to 20 m shoreward of
  the crest; y = elevation (m MSL), -8 to +2.5.
- Draw: seabed (SEABED line, SAND fill), reef body (darker fill, hatch), MSL line, tide band MLWS-MHWS (TIDE colour, label spring
  range: Palm 1.31 m, Boscombe 1.76 m) and the Israeli 0.40 m band as a thin dashed overlay for comparison; incoming wave as a
  sinusoid with height H(y) = H0 Ks(d) up to y_break (compute with `wavelib.shoaling_coefficient`), then the breaking crest drawn
  at y_break with height H_break: plunging lip for xi_b 0.4-2 and Y >= 1.6, collapsing front (near-vertical face) for Y < 1.6;
  a standing surfer 1.8 m tall (simple silhouette or stick figure, true height) on the face at y_break.
- Labels: crest depth (Palm 1.50 m, Boscombe 0.90 m below MSL), toe depth (Palm 6.99 m, Boscombe 5.41 m), depth gap
  (5.49 / 4.51 m), ramp length (89 / 13 m), mean slope (1:17 / 1:3.1), and at the break d_b, H_b, xi_b, Y and class text
  (Palm at MSL: xi_b 0.56, Y 2.05 "very high, plunging"; Boscombe at MSL: xi_b 1.60, Y 1.30 "collapsing, beyond Mead's extreme").
- Annotation: "Same depth gap (4.5-5.5 m), different ramp: 89 m vs 13 m". Mark Boscombe Y as extrapolated (slope 1:3 is outside
  Mead's 1:9-1:40 fit) with a dagger.

## F4 Depth gap vs ramp length for all reefs, with breaker-type bands (one column or 12 x 9 cm) - RESULTS s2-s3, insight f

- Data: `results_reef_summary.csv`: x = `ramp_length_m` (crest line) or `rep_ramp_length_m`, y = `depth_gap_crest_to_toe_bed_m`
  or `rep_depth_gap_m` (use rep_* as the plotted point; draw the crest-line value as a small hollow ghost joined by a thin line
  when different: Narrowneck 16 -> 37 m, Pratte's 1 -> 5 m). Also plot Albany's centreline (113 m ramp, gap 7.27 - 2.01 = 5.26 m,
  from `08_paper/data/profiles/southern-ocean-surf-reef-albany.json` lines.centreline.metrics) as a ghost, since its crest line
  runs along the oblique ridge. Colour/marker = reef (style.py); fill = outcome. Optional third variable: marker size =
  `volume_model_m3`.
- Axes: x = ramp length (m), log scale 1-300; y = depth gap crest to toe bed (m), 0-8 linear.
- Bands: rays of constant mean slope gap/length = 1/X drawn as shaded wedges: Y = 0.065 X + 0.821 (Mead 2000 Eq. 6.5) gives
  X = 12.0 (Y 1.6), 16.6 (1.9), 21.2 (2.2), 25.8 (2.5), 30.4 (2.8), 35.1 (3.1). Shade: X < 12.0 "collapsing (Y < 1.6)", 12.0-16.6
  "extreme", 16.6-25.8 "very high/high", 25.8-35.1 "medium", > 35.1 "gentle". Overlay Iribarren limits for a typical swell
  (H = 1 m, T = 10 s, L0 = 156 m): xi_b = 0.4 at 1:31, xi_b = 2.0 at 1:6.2; and for Israel (H = 1 m, T = 7 s, L0 = 76.5 m):
  xi_b = 0.4 at 1:22, 2.0 at 1:4.4 (dashed lines labelled "spilling | plunging | surging", one set per T).
- Annotations: reef names next to points; text "crest depth vs outcome rho = 0.00; depth gap rho = 0.93 (p_perm 0.005), ramp
  length rho = 0.85 (0.015), n = 8" (`results_outcome_correlations.json`, keys rep_depth_gap_m, ramp_length_m, crest_depth_msl_m).
  Caption note: slopes are along the model y axis; geometry idealised for 6 of 9 reefs.

## F5 Peel angle vs surfer skill (Hutt et al. 2001), with our reefs (one column, 9 x 9 cm) - RESULTS s4, insight g

- Data: Hutt table from `wavelib.HUTT` (rating: peel-angle limit deg, Hb min, Hb max); reef values from `results_peel.csv`
  filtered to T = site T (`results_surf.json` meta.site_inputs[slug].T) and phi0_src not starting with "ALT" (plot ALT for
  Narrowneck as a dashed variant): columns slug, arm, H0, alpha_break_deg, alpha_no_refraction_deg, hutt_rating, category.
- Axes: x = peel angle at breaking (deg), 0-90, reversed or not (state it); y = Hutt skill rating 1-10.
- Draw: the Hutt limit as a step line (rating r needs alpha >= limit: 90, 70, 60, 55, 50, 40, 29, 27; 9-10 "limit not reached"
  shown as an open-ended band below 27); grey band alpha < ~25 deg labelled "approaching close-out" (Mead & Black 2001 via Lewis
  et al. 2015 p.3). For each reef a horizontal bar from min to max alpha_break over H0 0.5-3 m, placed at the reef's row (or at
  the rating of the site-H value), with a hollow tick at alpha_no_refraction (phi0). Site-H point (`results_reef_summary.csv`
  peel_alpha_snell_deg) as the filled marker.
- Annotations: "30 deg (Lior) ~ Hutt 7 (29 deg, top amateur)"; "learners need >= 60-70 deg: no reef reaches it at the break";
  note that phi0 is ASSUMED for 5 of 8 reefs. Bunbury omitted (dome).

## F6 Volume vs outcome (one column, 9 x 7 cm) - RESULTS s6, insight a

- Data: `results_volume_outcome.csv` (slug, outcome, score, volume_stated_m3, volume_source; 11 reefs with a known outcome incl.
  Burkitts) and `results_reef_summary.csv` (volume_model_m3 for the 9 modelled reefs).
- Axes: x = reef volume (m3), log 50-100,000; y = outcome category (does not work / works rarely or mixed / works), points jittered
  vertically by +-0.12 to avoid overlap.
- Draw: stated volume = filled reef marker; model volume = small hollow marker joined by a thin line (shows Narrowneck
  70,000 vs 13,500 m3). Burkitts with a distinct note "natural reef reshaped (300 m3 moved)". Shade x < 5,000 m3 lightly.
- Annotations: "built reefs: rho = 0.72, p_perm = 0.021 (n = 10); incl. Burkitts: rho = 0.43, p = 0.21 (n = 11); modelled
  volume: rho = 0.93, p_perm = 0.005 (n = 8)" (`results_outcome_correlations.json`). Caption: ordinal outcome, small n, size
  collinear with material and age.

## F7 Surfable window vs tide range, incl. Israel (one column or 12 x 8 cm) - RESULTS s5, insight h-A

- Data (lines): `results_tide_range_summary.csv` (columns ramp_one_in, T, spring_range_m, mean_frac_surfable_dc1p0,
  mean_frac_on_crest_dc1p0, best_d_c, mean_frac_surfable_best_dc) from the synthetic Haifa reef; detail per H in
  `results_tide_range_sweep.csv` (d_c, ramp_one_in, T, H0, spring_range_m, frac_surfable, frac_breaks_on_reef, frac_breaks_on_crest).
- Data (points): `results_reef_summary.csv` columns spring_range_m (x), surfable_frac_best_line (y, local tide) and
  surfable_frac_israeli_tide_best_line (same geometry under the Israeli tide, plotted at x = 0.40 m), joined by an arrow per reef.
- Axes: x = spring tide range (m), 0-4.5; y = fraction of the lunar month the reef gives a surfable break (given the swell), 0-1.
- Draw: lines for ramps 1:12, 1:20, 1:30 (T = 7 s solid, T = 10 s dashed) at crest depth 1.0 m; optional thin line for "crest
  depth tuned to the range" (mean_frac_surfable_best_dc). Vertical band at 0.15-0.40 m labelled "Israel (Rosen 2001)"; tick marks
  for the built reefs' ranges (Bunbury 0.40, Albany 0.60, Cables 0.80, Gold Coast 1.31, Pratte's 1.65, Mt Maunganui 1.75,
  Boscombe 1.76, Borth 4.30).
- Annotations: "Israel: 0.87-0.98 of the no-tide value (1:12, crest 1 m)"; "small tide = window depends on wave height only";
  caption: fraction of time, not days per year (no wave climate); synthetic sinusoidal tide.

## F8 Stability: load index vs depth and wave height, geotextile vs rock, Israeli depths (full width, 2 panels) - RESULTS s8

- Panel (a), tubes under depth-limited breakers. Data: `results_stability_fk.csv` rows with at_break = True (columns tube, B, D,
  h_base, T, H, uplift_fraction, uplift_fraction_contact, SIc_calibrated, state, state_contact); take the max over T per tube
  and h_base. Axes: x = water depth at the tube base h (m), 1.5-8.5 (top axis: breaking H = 0.78 h); y = load index, 0-3.5.
  Draw per tube (colour by tube size, not by reef; label B x D): solid line U = uplift / submerged weight (sealed base, upper
  bound), dotted line Uc (pressure reaches the base, lower bound), dash-dot SIc (BD23 sliding index, calibrated). Horizontal
  lines U = 1 "lift-off" and SI = 0.5 "sliding (f = 0.5)". Shade x = 4-6 m "Haifa toe depth (synthetic profile)" and x = 1.5-3 m
  "surf-reef crest tubes".
- Panel (b), Israeli tubes vs depth in storms. Data: `results_stability_israel_depth.csv` (tube, Hs_storm, T, h_base, Hmax,
  uplift_fraction, uplift_fraction_contact, SIc_calibrated, Hs_crit_vansteeg, Hs_local). Axes: x = h_base 2-16 m; y = U (sealed)
  for Hs 1 m/7 s, 3.3 m/10 s, 5 m/12 s; second y or inset: Hs_local vs Hs_crit_vansteeg (1.42 m for 6.5 x 2.75, 0.85 m for
  3.9 x 1.65). Add rock: from `results_stability_rock.csv`, horizontal markers of H_stable_hudson for Albany armour (2.1-2.5 m),
  Cables 1.5 t (3.3-4.5 m), Borth 8 t (4.1-7.0 m) placed on the top (breaking-H) axis, labelled "rock stable up to".
- Annotations: "U grows as H/D: small tubes lift first"; "BD23 validation pair: uplift 3-13 % of weight"; caption must say
  ESTIMATE (calibrated linear Froude-Krylov, not the BELWF model; no tearing modelled) and give the calibration factors (SI 1.42
  linear, 0.94 / SIc 2.24 near breaking; `results_fk_calibration.json`).

## F9 Haifa design envelope (full width or 12 x 10 cm) - RESULTS s10, insights a, f, g, h

- Data: `results_israel_design_summary.csv` filtered bed_one_in = 50 (columns d_c, ramp_one_in, mean_frac_surfable_israeli,
  share_advanced_or_expert_msl, share_too_hollow_msl, share_spilling_or_gentle_msl, share_not_on_reef_msl, reef_cross_section_m2,
  ramp_length_m, volume_per_100m_m3); per-case detail `results_israel_design_sweep.csv` (skill_msl, xi_b, vortex_Y per H0, T).
- Axes: x = ramp slope 1:X (categories 8, 12, 16, 20, 30, plotted on a 1/X or log X axis); y = crest depth below MSL d_c (m),
  0.6-2.0, depth increasing downward.
- Draw: heat map of mean_frac_surfable_israeli (sequential palette, 0-1); in each cell a small stacked bar or pie of the class
  shares (too hollow / expert-advanced / spilling / not on reef); contour lines of volume_per_100m_m3 (10,000, 15,000, 25,000,
  40,000 m3). Overlays: arrow from d_c 0.8 to 1.8 m labelled "+1 m settlement or bed rise" (`results_israel_burial.csv`);
  horizontal dashed band at d_c 1.2-1.5 m "Lior's field breaking depth (Hs 0.45-0.6 m)"; reference reefs placed by crest depth and
  mean ramp slope from `results_reef_summary.csv` (Palm Beach 1.50 m, 1:17; Cables 1.56, 1:20; Albany centreline 2.01, 1:24;
  Boscombe 0.90, 1:3.1 off-scale at left with an arrow; Narrowneck 2.32, 1:12.5 second crest line) with their outcome fill.
- Outline the recommended envelope (crest 0.6-1.0 m, ramp 1:16-1:20) with a heavy line; text box: "rock armour Dn50 ~0.7-0.85 m
  (1-1.6 t); 15,000-25,000 m3 per 100 m; T 6-8 s; Israeli tide 0.4 m". Caption: synthetic 1:50 bed (1:70 gives the same result),
  no refraction/focusing, gamma 0.78.

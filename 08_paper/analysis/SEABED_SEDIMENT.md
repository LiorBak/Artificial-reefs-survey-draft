# SEABED_SEDIMENT: sediment-transport signals around the built surf reefs, from the bathymetry already in the repo

Run 2026-10-15. Script `08_paper/analysis/seabed_sediment.py` (run `python3 -B 08_paper/analysis/seabed_sediment.py`, about 15 s; this text is written by `seabed_sediment_report.py` from the JSON); all numbers below are copied from `08_paper/analysis/seabed_sediment_results.json` (keys per reef; `summary_table` holds the long-form verdict text). Figures: `08_paper/figures/fig_sediment_cables-reef-wa.png`, `fig_sediment_boscombe-surf-reef.png`, `fig_sediment_borth-coastal-defence-reef.png`. Input data are read only (07_scale/). Every number here is DERIVED by this script unless a source is named; ASSUMPTION marks an assumption. Positive anomaly = the contour lies farther offshore (closer to the reef) in the lee, or the bed is higher.

## 1. Answer in brief

1. Only 5 of the 13 reefs have measured seabed data that can test anything (Cables WA, Boscombe, Borth, Palm Beach [chart only], Pratte's [two contour sets]). Narrowneck, Mount Maunganui, Bunbury, Albany, Kovalam, Opunake, Burkitts and the Mexico reef were skipped: their seabeds are assumed or synthetic, pre-construction only, a window filled by the reef, or absent (section 3).
2. **No reef-attributable sediment signal survives a control or a pre-construction test.** Cables (the only site with pre- and post-construction soundings): the lee seabed is 0.60 m higher and its contours are 15-43 m farther offshore than at controls 1.5-3.5 reef lengths along the shore, but the same offset is already in the 1995 pre-construction survey (offshore contours); the 1995 to 2002 bed change in the lee is +0.03 m (SE 0.04 m), no toe scour, no burial; the beach-level surveys show a lee shoreline bulge of +26 m (Jan 2001, 13 months after completion) that has SHRUNK to +10 m by Apr 2012 (a growing salient would increase). Boscombe (best-controlled BACI, 316 beach-profile surveys): the lee shoreline advanced by +3.4 m relative to the controls (0 m ODN contour, 95% CI +1.3..+5.3 m; +1 m contour +1.9 m, +2 m -0.3 m), inside the tilt and beach-management signals: the whole frontage jumps together (+72 m3/m in 2006-07 on all 6 lines, +40 m3/m in 2020-21). Palm Beach (chart, low confidence): |offset| <= 2 m at the 1-3 m contours.
3. **Borth is the one positive spatial signal and it cannot be attributed.** In the single LiDAR survey of 19 Mar 2022 (10 y after construction) the 0 m MSL contour has its peak within 4 m of the reef-centre longitude (+23 m above the southern shoulder, +58 m above the northern), the bed in the lee is higher by +0.7 to +0.8 m; but there is no pre-construction beach survey, the north-south gradient is strong, and the offset depends on the control chosen (0 m contour: +12..+48 m).
4. Reading for Lior's insight (b) ("little measurable effect on sand transport; at the Gold Coast it cannot be separated from nourishment"): consistent for the three small-to-medium reefs with usable data (Cables, Boscombe, Palm Beach), with limits: the Black & Andrews (2001) B/S rule gives B/S = 0.39-0.61 for them, i.e. a salient is expected, with an ILLUSTRATIVE amplitude of 14-41 m (Cables), 11-33 m (Boscombe) (ASSUMPTION D_tot = 1-3 B). Boscombe's BACI would see most of that range and finds +3.4 m (CI to +5.3 m); Cables resolves only about +-10 m of contour position (0.1 m of bed) over 2.2 y. Borth (B/S = 1.22, both mounds, the largest and most extended reef) is the one site with a lee bulge. Nothing could be tested at Narrowneck, where nourishment is continuous.
5. For Haifa the useful finding is methodological: shoreline and bed-level effects of a small submerged reef are of the order of the natural alongshore variability and of beach-management signals, so a before/after survey WITH controls (BACI) and a record of nourishment are needed; claims of reef-driven accretion or protection cannot be checked with the public single-date data held here.

## 2. Verdict table (per reef)

| Reef | Data used | Signal? | Magnitude (DERIVED) | Uncertainty | Caveats |
|---|---|---|---|---|---|
| Cables WA (reef 2000) | DoT WA single-beam 1995-12 (pre), 1998-03 (pre), 1999-11, 2002-02; Perth_5m composite; beach levels 2001-01 .. 2012-04 | **Inconclusive / no**: lee high bed, contour offset and shoreline bulge exist but are pre-existing (offshore) or not growing (beach); no change 1995-2002 | lee offsets +15 (0 m AHD) to +43 m (-4 m); lee bed higher by 0.60 m; the -5 m contour offset is +20 m in 1995 vs +25 m in 2002; bed change 1995-2002 +0.03 m (SE 0.04); contour migration 1995-2002 +3..+7 m; shoreline bulge +26 m (2001) -> +10 m (2012) | formal SE 2-8 m (contours), 0.05 m (bed); survey offsets +-0.1 m | only 2.2 y offshore; adjacent controls in the temporal test; 0..-3 m contours have no pre-reef survey; no pre-reef beach survey; Leighton/Port Beach management not checked; B/S = 0.52 |
| Boscombe (reef 2009) | CCO beach profiles, 11 lines, 316 surveys 2004-2026 (shoreline to -1 m ODN); reef toe about 155 m or more seaward of the profile ends | **No** (<= 5 m, inside tilt and management signals) | 0 m ODN contour +3.4 m (CI +1.3..+5.3); +1 m +1.9 (CI -0.5..+4.3); +2 m -0.3; volume +3.4 m3/m (CI -4.5..+10.5); post-only 11 lines -0.2 +- 0.9 m | bootstrap over dates (pre n = 5); dates not independent | Poole Bay groynes + recharge (frontage-wide jumps +72 m3/m 2006-07, +40 m3/m 2020-21); reef construction left 11,100 m3 sand on the beach (Rendle 2016); no pre-reef bathymetry; 60 m in 6 months (Mead & Borrero 2011) not reproduced (max +3.0 m) |
| Borth (Phase 1, 2012) | Welsh Government LiDAR DTM 19 Mar 2022, 1 m | **Inconclusive** (bulge yes, attribution no) | 0 m MSL contour +30 m (range +12..+48), -1 m +40 (+1..+77), -2 m +57 (+22..+93); lee bed +0.68..+0.78 m | formal SE 2-9 m; control choice changes it by 36-92 m | ONE date; no pre-construction beach survey; strong N-S gradient; unexplained ridge in the north control; strip 750 m; B/S = 1.22 |
| Palm Beach (reef 2019) | Navionics SonarChart iso-lines 1-3 m (chart, undated) | **No** | 1 m: -1.4 m; 2 m: -2.2 m; 3 m: -0.3 m | chart smoothing, +-10 m (ASSUMPTION) | LOW confidence; continuous Gold Coast nourishment not quantified; 4-6 m contours bent by the reef shoal (+38..+71 m) are a chart artefact |
| Pratte's (2000) | Borrero & Nelsen (2003) Fig. 9, two surveys (Oct 2000, Mar 2001), contours -1..-4 m | **Inconclusive** | all four contours moved offshore by +13 m (+9..+18) | datum/tide offset of 0.3 m = about 10 m | window = 2 reef lengths, reef not drawn, no control |
| Narrowneck, Mount Maunganui, Bunbury, Albany, Pratte's (3D bed), Kovalam, Opunake, Burkitts, Mexico | skipped | n/a | n/a | n/a | assumed/synthetic seabed or no data (section 3) |

## 3. What each seabed dataset really is, and what was skipped

| Reef | Seabed in the 3D model / repo | Measured? | Used here |
|---|---|---|---|
| cables-reef-wa | DoT WA single-beam soundings 1995-12, 1998-03, 1999-11, 2002-02 (point files) + DoT Perth_5m composite (METHODS_3D 3.4) | MEASURED (sd 0.29 m between surveys) | **yes**: all four surveys, TIN |
| boscombe-surf-reef | CCO beach-profile surveys (measured, 316 files); the offshore model bed is the Rendle & Davidson 2012 Fig. 9 colour read of April 2011 (a 23,500 m2 tilted window) plus a thin-plate-spline "ambient" bed and an EMODnet slope extrapolation (assumed) | beach MEASURED; offshore window measured but too small and post-failure | **yes** (CCO lines only); Fig. 9 window has no control section and the pre-reef bed is a fit |
| borth-coastal-defence-reef | Welsh Government LiDAR DTM 2022-03-19 (beach to -2.3 mODN, measured); beyond that HRPP576 Fig. 2 contours read by eye and ASSUMED bridge nodes | beach MEASURED | **yes**: the DTM itself, not the model grid |
| palm-beach-gold-coast | Navionics SonarChart iso-lines (chart) + toe levels from the aerial; thin-plate spline | chart-derived, date unknown | yes, 1-3 m lines only, LOW confidence |
| prattes-reef-el-segundo | model bed = alongshore-uniform profile (NOAA DEM + Navionics, ASSUMED); separate vector Fig. 9 contours of two surveys | profile assumed; Fig. 9 measured | Fig. 9 only |
| narrowneck-gold-coast | the only measured bed is Corbett et al. (2023) Fig. 3 (ICM 2017 pre-works multibeam) digitised by colour hue into a 164 x 145 m window that is filled by the reef itself (no lee strip wider than 25 m, no control section; +-0.4 m colour-to-depth fit); outside the window the model bed is an ASSUMED alongshore-uniform profile (METHODS_3D 3.3: shoreward of y=190 assumed). City of Gold Coast DTM has NO underwater cells at the reef (07_scale/bathymetry/gold_coast, Q1). Gold Coast beaches are continuously nourished and sand-bypassed (insight b), so a shoreline signal would be confounded anyway. Literature pointers only (not tested here): Jackson et al. 2012 Fig. 16 (salient photo 20 May 2010), Mead & Borrero 2011 Fig. 5 (beach width envelope), Blacka et al. 2013 p.98 (called the widening an artefact of the reference line). | assumed/skipped | **skipped** |
| mount-maunganui-reef | bed = ASSUMED alongshore-uniform profile (Navionics profile + a reef-centre offset; METHODS_3D 3.3) plus a digitised 2013 multibeam window (178 x 148 m, mostly the reef). The Navionics SonarChart z17 iso-lines (reef removed in 2014, so they show the ambient bed) trend by about 70 m over 320 m of coast near Mauao (2 m line: y = 320 m at x = -380 to 250 m at x = -60, 3d/navionics_isolines.json), i.e. the natural gradient is larger than any plausible reef signal; BoPRC p.29: the bed fluctuates by more than 1 m. | assumed/skipped | **skipped** |
| bunbury-airwave | the Airwave bladder was in the water for about 3 days in Dec 2019 (installed 9-13 Dec, torn, removed within about 3 days; model.js lifecycle), so no sediment response is possible. The 2009 WA DoT airborne lidar grid in the model (10 m, gap-filled) is pre-structure. | assumed/skipped | **skipped** |
| southern-ocean-surf-reef-albany | the reef was built in 2025 and the repo holds only the PRE-construction 2015 contours and an assumed alongshore-uniform profile (A4); a baseline of natural alongshore variability is given under "albany_baseline". | assumed/skipped | **skipped** |
| kovalam / opunake / burkitts / mexico | no 3D model and no bathymetry grid or survey in the repo (their src/ folders hold imagery, outlines and PDFs only; opunake holds only a NZGD2000 grid-shift raster). Kovalam, Opunake and Burkitts: no data for a sediment test. | no data | **skipped** |
| 07_scale/bathymetry (EMODnet, Gold Coast) | cells of 115 x 73 m (about the reef size), reef invisible in every release 2018-2024 (Boscombe cell max -4.87 mLAT vs model crest +0.56), one sounding per cell at Borth, interpolated at Haifa. Gold Coast: the City DTM has no underwater cells at either reef (07_scale/bathymetry/gold_coast HANDOFF Q1). | n/a | not used |

Albany baseline (pre-construction 2015 contours read on 8 transects, 20 m apart): the -1, -2, -3 m contours trend -11.5, -11.2, -11.6 m per 100 m alongshore and scatter about the trend by 2.0, 1.8, 1.1 m (1 sd). This is a noise floor for any future post-construction comparison (colour reading, +-10 m for the deeper lines); no post-construction bathymetry exists in the repo.

## 4. Method

**Frames.** Each site is analysed in its own shore frame: x (or s) alongshore with the reef centre at 0 (Cables: s along bearing 7.8 deg true, from `scripts/shore_datum.json`; Boscombe: canonical x, bearing 83.4 deg; Borth: canonical x, + south), y (or n) offshore. L = alongshore extent of the reef footprint (Cables 110 m, Boscombe 88 m, Borth 195 m for both mounds, Palm Beach 137 m).

**T1 contour offset.** Cross-shore position Y_c(x) of the shoreline (0 m) and of the -1, -2, -3 m (and deeper where measured) contours, first downward crossing from the shore on a smoothed surface (Cables: soundings to a linear TIN, cells > 25 m from a sounding masked, Gaussian 10 m; Borth: LiDAR 1 m smoothed 1.5 cells). Anomaly = mean Y_c in the lee window (x within the reef extent) minus the straight-line trend fitted to the CONTROL windows (1.5-3.5 L from the reef centre where data exist), evaluated in the lee.

**T2 bed level.** The same machinery on the mean bed elevation in a fixed cross-shore band (Cables n = -165..-62 m from the reef centre; Borth y = 40-100, 100-160, 160-220 m from the defence line).

**T3 temporal.** Cables only: dz = later minus earlier survey in every 5 m cell that has a sounding within 25 m in both surveys; boxes in the lee band; difference-in-differences against adjacent strips (the 1995 survey covers the lee band only for s = -150..+125 m); contour migration 2002 minus 1995 on identical transects. Noise floor from the pre-construction pair 1998 vs 1995. Boscombe: before/after at 6 CCO lines (pre = 2004-07..2008-04, construction 2008-06..2009-11 excluded, post = 2009-11..2026-03); common-mode removed by subtracting the six-line mean on each date; lee anomaly = mean change of the lee lines minus the straight line through the four control lines; 95 % CI by bootstrap over survey dates (4000 resamples); additionally the 11-line post-only alongshore pattern.

**T4 burial and toe scour.** Cables: post-construction soundings against the 1998 TIN in rings 0-10, 10-25, 25-50, 50-100 m outside the footprint; reef surface 1999-11 vs 2002-02 at matched soundings (< 3 m apart).

**Uncertainty.** Three layers are reported. (i) Formal standard error of the anomaly from the residual scatter of the control samples about the trend, corrected for serial correlation along the shore (integral scale tau; `se_analytic`). (ii) Placebo windows of the same width slid along the control strips (`placebo_sd`, only when >= 8 windows exist). (iii) Sensitivity to the control choice: the anomaly recomputed with each control strip alone (`anomaly_range`); where the natural alongshore gradient is large (Borth) this range, not the formal SE, is the honest uncertainty. Boscombe uses a date bootstrap.

**Limits of the method.** Single-beam surveys 25-60 m between lines and +-0.3 m vertical sd; the controls can lie inside a reef's sphere of influence (biases toward zero); a contour offset of x metres equals a bed difference of x times the local slope (Cables 1:15 to 1:40); an echo-sounder cannot tell sand from rock fall-down; tide/datum differences between survey campaigns act like a uniform dz (+-0.1 m assumed from the pre-construction pair mean -0.10 m).

## 5. Results

### 5.1 Cables Reef, Perth (figure `fig_sediment_cables-reef-wa.png`)

Data (DERIVED coverage): 1995 13589 soundings, z -9.8..-2.4 m AHD; 1998 14303 soundings, z -10.3..-2.5 m AHD; 1999 840 soundings, z -5.0..-1.4 m AHD; 2002 8373 soundings, z -10.9..-1.1 m AHD. The 1995 survey ends at z = -2.45 m AHD (about 90 m from the shore); the 2002 survey reaches -1.07 m. Reef: 110 m alongshore, 86 m cross-shore, 211 m from the 0 m AHD contour (Perth_5m composite, undated).

T1 (lee window +-55 m; controls 165-385 m on both sides; composite and 2002 only, the 1995/1998 surveys do not reach the far controls):

| Dataset | Contour (m AHD) | Lee anomaly (m) | formal SE | placebo sd | north-only / south-only control (range) |
|---|---|---|---|---|---|
| Perth_5m composite | 0 | +15.4 | 2.1 | 1.5 | +14..+17 |
| Perth_5m composite | -1 | +17.5 | 4.1 | 2.5 | +16..+19 |
| Perth_5m composite | -2 | +17.9 | 5.7 | 3.6 | +16..+20 |
| Perth_5m composite | -3 | +27.4 | 7.5 | 4.6 | +27..+27 |
| Perth_5m composite | -4 | +37.5 | 6.9 | 4.0 | +35..+40 |
| DoT 2002-02 | -2 | +22.7 | 6.1 | 3.3 | +21..+26 |
| DoT 2002-02 | -3 | +33.1 | 6.6 | 3.2 | +30..+37 |
| DoT 2002-02 | -4 | +42.8 | 7.8 | 3.9 | +38..+48 |
| DoT 2002-02 | -5 | +35.1 | 4.9 | 3.0 | -2..+84 |
| DoT 2002-02 | -6 | +23.6 | 5.4 | 4.0 | -5..+63 |

The offset is a robust spatial feature (north-only and south-only controls agree). It is also in the PRE-construction survey (T1b, adjacent control strips s = -150..-75 and +75..+125):

| Survey | Contour | Lee anomaly (m) | range over control choice | formal SE |
|---|---|---|---|---|
| 1995 | -4 | -0.7 | -14..+12 | 3.0 |
| 1995 | -5 | +20.4 | +14..+28 | 3.7 |
| 1995 | -6 | +7.7 | +2..+14 | 1.0 |
| 2002 | -4 | +6.6 | -6..+21 | 0.9 |
| 2002 | -5 | +25.3 | +15..+37 | 3.3 |
| 2002 | -6 | +10.3 | +3..+19 | 2.1 |

(1995 -4 m: the contour is covered only for s = -100..+125 m; treat with care.) Contour migration 2002 minus 1995, lee against the adjacent strips: -4 m: +7.0 m (SE 3.1); -5 m: +4.9 m (SE 1.7); -6 m: +2.6 m (SE 2.1) = a bed rise of about 0.1-0.2 m at the local slope, within the survey offset.

T2/T3 bed level and change in the lee band (n = -165..-62 m):

| Quantity | Value |
|---|---|
| bed level, lee minus far-control trend, DoT 1995-12 (pre-construction) | +0.75 m (range +0.75..+0.75 m; formal SE 0.06 m) |
| bed level, lee minus far-control trend, DoT 2002-02 (2.2 y after completion) | +0.60 m (range +0.48..+0.72 m; formal SE 0.05 m) |
| bed level, lee minus far-control trend, Perth_5m composite | +0.39 m (range +0.37..+0.41 m; formal SE 0.18 m) |
| dz 2002-1995, box lee (s -55..+55 m) | mean +0.036 m, sd of cells 0.18 m, coverage 96 %, volume +414 m3 |
| dz 2002-1995, box ctrl_S (s -150..-75 m) | mean +0.028 m, sd of cells 0.26 m, coverage 63 %, volume +150 m3 |
| dz 2002-1995, box ctrl_N (s +75..+125 m) | mean -0.035 m, sd of cells 0.19 m, coverage 86 %, volume -175 m3 |
| difference-in-differences, dz 2002-1995, n=-165..-62 | +0.032 m (SE 0.040 m) |
| difference-in-differences, dz 2002-1995, n=-110..-62 | -0.055 m (SE 0.026 m) |
| noise floor dz 2002-1995, all valid cells outside the reef + 20 m | mean -0.03 m, sd 0.29 m, 5-95 % -0.45..+0.42 m (n = 4057) |
| noise floor dz 2002-1998, all valid cells outside the reef + 20 m | mean +0.07 m, sd 0.21 m, 5-95 % -0.22..+0.47 m (n = 1526) |
| noise floor dz 1998-1995, all valid cells outside the reef + 20 m | mean -0.10 m, sd 0.24 m, 5-95 % -0.50..+0.28 m (n = 1407) |

The change in the lee band (dz) is +0.04 m against +0.03 and -0.04 m in the adjacent strips: nothing is detectable above the +-0.1 m survey offset (+-1,100 m3 over the 11,300 m2 box).

T4 rings (post-construction sounding minus the 1998 TIN):

| Survey | Zone | n | mean dz (m) | sd (m) |
|---|---|---|---|---|
| 1999 | inside footprint (rock thickness above the 1998 bed) | 600 | +1.28 | 0.69 |
| 1999 | ring 0-10 m outside | 178 | +0.51 | 0.64 |
| 1999 | ring 10-25 m outside | 61 | -0.03 | 0.26 |
| 2002 | inside footprint (rock thickness above the 1998 bed) | 316 | +1.29 | 0.69 |
| 2002 | ring 0-10 m outside | 267 | +0.42 | 0.53 |
| 2002 | ring 10-25 m outside | 502 | +0.09 | 0.17 |
| 2002 | ring 25-50 m outside | 885 | +0.13 | 0.26 |
| 2002 | ring 50-100 m outside | 1084 | +0.05 | 0.24 |

Reef surface, 2002 minus 1999 at 517 matched soundings (< 3 m apart): mean +0.14 m, sd 0.37 m; 95th-percentile level inside the footprint -1.76 (1999, n=600) vs -1.83 m AHD (2002, n=316). The matched-sounding mean and the percentile move in opposite directions: both are inside the sounding noise (positioning on a rough rock surface), so no settlement and no burial is detectable at the 0.15 m level. Repeatability 1998 vs 1995 within 3 m: mean -0.09 m, sd 0.28 m (n=11647).

T5 beach-level surveys (DoT "Levels" point files, profile lines about 50 m apart; lee = 2 lines within +-55 m, controls = 6-8 lines 165-385 m either side):

| Survey | lines | 0 m AHD contour lee minus controls (m) | +1 m contour (m) | range over control choice (0 m) |
|---|---|---|---|---|
| 2001-01 | 13 | +26 | +26 | +26..+26 |
| 2002-02 | 14 | +23 | +24 | +23..+27 |
| 2003-01 | 15 | +15 | +24 | +13..+16 |
| 2011-08 | 23 | +16 | +20 | +16..+34 |
| 2012-04 | 23 | +10 | +10 | +10..+17 |

Change between dates (matched lines, lee minus controls): 2001-01 to 2003-01: -10 m (0 m), -2 m (+1 m); 2003-01 to 2012-04: -4 m (0 m), -13 m (+1 m); 2001-01 to 2012-04: -14 m (0 m), -15 m (+1 m); 2002-02 to 2012-04: -8 m (0 m), -14 m (+1 m). A lee shoreline bulge is present at every date, largest 13 months after completion and smaller later: this is not the signature of a salient that grows after construction. It cannot be separated from a natural feature (no beach survey before Dec 1999; the offshore contours already had the lee hump in 1995), from a decaying construction-time feature, or from beach management at Leighton/Port Beach (NOT checked; the 2011-12 files carry the name "PortBeach"). No formal SE (3-4 lines per control strip); the scatter between dates is 10-26 m.

Likely cause of the pre-existing lee offset: natural limestone reef lines of the Cottesloe coast (ASSUMPTION; not verified in this run). B/S = 0.52 (toe) / 0.44 (centre): salient expected (B/S < 2), illustrative amplitude 14-41 m (ASSUMPTION D_tot = 1-3 B).

### 5.2 Boscombe (figure `fig_sediment_boscombe-surf-reef.png`)

Data: Channel Coastal Observatory beach-profile surveys, lines 5f00424-5f00429 (quarterly or annual since 2004-07) and A lines 424A-428A (annual since 2010-04), file list `07_scale/shapes/boscombe-surf-reef/src/cco_profiles/`, converted with the project's `canon.py` (+-5 m); heights m ODN (= MSL within +-0.1 m, A4). Profiles end at about -1 m ODN, i.e. y about +21 m; the reef toe is at y = 181 m. Reef x = -39..+50 m (L = 88 m); lee lines 5f00426, 5f00427 (x = 43, -58 m), controls 424 (222), 425 (146), 428 (-142), 429 (-221).

Raw pre/post per line (0 m ODN contour position y, m from the surf-line origin; volume above 0 m ODN, m3 per m, y = -55 m to the contour):

| Line | x (m) | pre n | pre y0 | post n | post y0 | post-pre y0 | post-pre volume |
|---|---|---|---|---|---|---|---|
| 5f00424 | 222 | 16 | -13.8 | 43 | -2.4 | +11.4 | +29 |
| 5f00424A | 176 | 0 | - | 17 | -0.6 | - | - |
| 5f00425 | 146 | 5 | -18.0 | 17 | -0.6 | +17.4 | +32 |
| 5f00425A | 96 | 0 | - | 17 | -1.2 | - | - |
| 5f00426 | 43 | 5 | -16.4 | 17 | -4.1 | +12.2 | +24 |
| 5f00426A | -5 | 0 | - | 17 | -4.8 | - | - |
| 5f00427 | -58 | 16 | -14.6 | 43 | -4.0 | +10.6 | +24 |
| 5f00427A | -88 | 0 | - | 17 | -1.8 | - | - |
| 5f00428 | -142 | 5 | -8.1 | 17 | -4.0 | +4.2 | +12 |
| 5f00428A | -183 | 0 | - | 17 | -7.3 | - | - |
| 5f00429 | -221 | 5 | -12.0 | 17 | -7.9 | +4.2 | +8 |

Every line advanced (+4 to +17 m) between the pre and post periods; the change is common-mode (beach volume jumps 2006-07 on all six lines and 2020-21 on four, east-end lines 2015-16; panel a), so it is NOT a reef effect. With the common mode removed (six-line mean subtracted on dates when all six were surveyed; pre n = 5, post n = 17 dates):

| Metric | change per line, lines 424 / 425 / 426 / 427 / 428 / 429 | straight-line trend through the 4 controls | lee anomaly (426, 427) | 95 % CI (bootstrap) |
|---|---|---|---|---|
| 0 m ODN contour (m) | +3.4 / +6.3 / +1.2 / +3.0 / -6.9 / -6.9 | +3.0 per 100 m | +3.4 | +1.3..+5.3 |
| +1 m contour (m) | +5.0 / +5.5 / +0.8 / +1.4 / -5.0 / -7.6 | +3.1 per 100 m | +1.9 | -0.5..+4.3 |
| +2 m contour (m) | +4.1 / +2.7 / 0.0 / -0.5 / -1.9 / -4.3 | +1.8 per 100 m | -0.3 | -4.6..+3.4 |
| volume above 0 m ODN (m3/m) | +13.9 / +9.0 / +0.5 / +3.2 / -11.6 / -15.1 | +6.7 per 100 m | +3.4 | -4.5..+10.5 |

After the reef the frontage tilts (east lines advance relative to the mean, west lines retreat by about 7 m): a gradient, not a local maximum at the lee lines. Post-only, 11 lines, 17 annual dates: lee anomaly -0.2 +- 0.9 m (0 m), -1.2 +- 0.8 m (+1 m), -3.8 +- 4.0 m3/m (volume). Largest 0 m contour advance between 4-8-month-apart surveys in 2008-2010: +3.0 m (rows in the JSON, key `E_six_month_changes_2008_2010`); the "up to 60 m within 6 months" of Mead & Borrero (2011, p.4-5; designer's account, recorded in 02_research/reefs/boscombe-surf-reef.md) is not reproduced at these lines (other contour, line or reference unknown).

Confounds: the Poole Bay frontage is groyned (about 60 hardwood groynes, roughly every 180 m) and re-nourished every 10-12 years (Mead & Borrero 2011, p.4-5, as recorded in the reef card; groyne positions relative to the CCO lines were NOT mapped here); building the reef involved 23,000 m3 of sand piled on the upper beach, of which 11,100 m3 stayed on the beach between the pier and the first groyne (Rendle 2016, p.125-127, `07_scale/shapes/boscombe-surf-reef/P5_RENDLE2016_NOTES.md`); the dates and volumes of recharge are not in the repo. The year-on-year rise indicator (`B_common_mode_volume_jumps`) only flags that common-mode events exist. The reef toe lies about 155 m or more seaward of the profile ends and its lee (waves from the SW-S) may be displaced east of the reef; the A lines at x = 96 and -88 m are not in the BACI because they have no pre-construction data. The only Boscombe seabed data farther offshore are the April 2011 survey window (post-failure, no control section) and EMODnet cells too coarse to see the reef.

### 5.3 Borth (figure `fig_sediment_borth-coastal-defence-reef.png`)

Data: Welsh Government LiDAR DTM, tile SN6089, flight 19 Mar 2022, 1 m cells, resampled to a 2 m canonical grid with the project's `b3d_lib.Frame` (fit rms 0.005 m); heights mODN -0.31 = m MSL. Phase 1 completed 8 March 2012. Reef mounds x = -74..+121 m (L = 195 m), shoreline (0 m MSL contour) in the lee at y = 96 m, reef toe at y = 257 m. Lee window = reef extent; controls start 0.5 L beyond the edges (x < -172 and x > 219 m) because the analysed strip is only 750 m long.

| Quantity | lee mean | control mean | anomaly (trend through both) | range over control choice | formal SE | peak (x, y) | peak minus reef-centre x |
|---|---|---|---|---|---|---|---|
| +0 m MSL contour (m) | 96 | 69 | +30 | +12..+48 | 3 | (28, 107) | +4 m |
| -1 m MSL contour (m) | 159 | 124 | +40 | +1..+77 | 9 | (4, 187) | -20 m |
| -2 m MSL contour (m) | 229 | 176 | +57 | +22..+93 | 5 | (64, 253) | +40 m |
| bed level y = 40-100 m (m MSL) | +0.93 | +0.34 | +0.71 | -0.11..+1.48 | 0.18 | | |
| bed level y = 100-160 m (m MSL) | -0.64 | -1.34 | +0.78 | +0.26..+1.26 | 0.05 | | |
| bed level y = 160-220 m (m MSL) | -1.37 | -1.98 | +0.68 | +0.24..+1.09 | 0.05 | | |

The 0 and -1 m contours peak within 5-20 m of the reef-centre longitude (the -2 m contour, where the DTM touches the reef mounds, peaks 40 m south), which is what a salient behind the reef would look like. But (i) it is one survey 10 y after construction; (ii) the south-only control gives +12 m (0 m) and +0.5 m (-1 m) while the north-only control gives +48 and +77 m: the beach has a strong natural north-south gradient (village frontage vs dune frontage), and the peak sits on top of that step; (iii) the north control strip contains an unexplained shore-parallel ridge in the DTM (x about -330..-235 m, y about 75-95 m) that kinks the -1 m contour; (iv) seasonal state (March) and bars are not considered. Project check (07_scale/.../borth HANDOFF, not recomputed): LiDAR minus design crest levels +0.14 +- 0.28 m, i.e. no burial or settlement at the 0.3 m level. B/S = 1.22 (toe) / 0.85 (centre) for both mounds; the northern mound alone has B/S about 0.47.

### 5.4 Palm Beach (chart only, LOW confidence)

| Chart contour (m below LAT) | lee anomaly (m) | range over control choice | formal SE | note |
|---|---|---|---|---|
| 1 | -1.4 | -9..-1 | 2.9 | shoreward of the reef |
| 2 | -2.2 | -2..+8 | 0.6 | shoreward of the reef |
| 3 | -0.3 | 0..+13 | 0.3 | shoreward of the reef |
| 4 | +38.3 | +38..+57 | 1.0 | bent by the reef shoal in the chart: NOT a sediment signal |
| 5 | +70.7 | +71..+97 | 1.4 | bent by the reef shoal in the chart: NOT a sediment signal |
| 6 | +38.6 | +39..+43 | 5.5 | bent by the reef shoal in the chart: NOT a sediment signal |

The Navionics SonarChart is a smoothed compilation of sonar logs and surveys of unknown date; the reef (2019) is drawn as a shoal; the Gold Coast beaches are nourished continuously (not quantified here). A null at 1-3 m therefore says only that no lee offset larger than about 10 m is drawn on the chart.

### 5.5 Pratte's Reef, two surveys

| Contour | overlap (m) | mean shift Oct 2000 to Mar 2001 (m, + offshore) | max abs (m) | sd (m) |
|---|---|---|---|---|
| -1 m | 54 | +10.8 | 19 | 4.6 |
| -2 m | 81 | +14.1 | 28 | 9.4 |
| -3 m | 68 | +17.8 | 21 | 2.5 |
| -4 m | 68 | +8.8 | 14 | 2.6 |

All four contours moved by a similar amount over the whole window: a window-wide shift (seasonal profile change, tide or datum difference of the two surveys), not a local lee effect; the window is two reef lengths wide, the reef is not drawn (position +-150 m) and there is no control section. Inconclusive.

## 6. What this means for the paper, and what would settle it

- Safe statements: (a) in the three well-observed small/medium reefs the lee shoreline/bed response is below the survey resolution (a few metres at Boscombe, 0.1 m of bed at Cables 1995-2002, and no growth of the Cables beach bulge 2001-2012); (b) the apparent lee highs in single-date data (Cables 2002, Borth 2022) are either pre-existing (Cables) or untestable (Borth) - this is the argument for BACI; (c) the Boscombe record shows that beach-management events move the whole frontage by tens of metres, an order of magnitude more than any reef effect; (d) at the Gold Coast the reef effect cannot be separated from nourishment with public data.
- Not safe: "the reef causes a salient/accretion" (Borth) or "the reef has no effect" (the resolution is +-10 m of contour at Cables, 2.2 y).
- Cheapest additions that would turn Borth and Boscombe into real tests (Lior requests, not done here): the pre-2012 beach survey of Borth (Welsh coastal monitoring programme / the design survey of 2010) and later LiDAR epochs; Poole Bay recharge dates and volumes (BCP Council / CCO) and the groyne positions along the CCO lines; Boscombe pre-2009 offshore bathymetry; a pre-construction (before Dec 1999) beach survey of the Cables/Leighton frontage (DoT WA; the other pre-construction FR files in the same zip were checked and not used: the 1984 digitised chart has only 591 points in the window, the 1984-85 and 1996 single-beam files none) and the Leighton/Port Beach nourishment history.
- Possible paper figure: `fig_sediment_boscombe-surf-reef.png` panel (a) (the nourishment confound) and panel (b) (BACI), and `fig_sediment_cables-reef-wa.png` panels (c) (offset pre-dates the reef) and (d) (shoreline bulge not growing).

## 7. Reproduction, provenance, caveats

- Script: `08_paper/analysis/seabed_sediment.py`; results `08_paper/analysis/seabed_sediment_results.json` (one block per reef, `summary_table` with the long verdict text, `skipped`, `_meta`). Imports (read only) `07_scale/shapes/boscombe-surf-reef/3d/scripts/canon.py` and `07_scale/shapes/borth-coastal-defence-reef/3d/b3d_lib.py` (run with `python3 -B` so that no bytecode is written into 07_scale). Scratch: `/tmp/claude-0/paper/seabed/`.
- Data files (all read only): Cables `07_scale/shapes/cables-reef-wa/src/bathymetry/FR_selected/*.txt` and `DoT_Perth_5m_clip_reef.npz` (DoT WA, CC BY 4.0, accuracy "variable, no warranty"); Boscombe `.../boscombe-surf-reef/src/cco_profiles/`; Borth `.../borth-coastal-defence-reef/3d/src/lidar_beach_SN6089_2022-03-19.npz`; Palm Beach `model.js` navionics.lines (Garmin Navionics, not for navigation; private research copy, reuse rights not cleared); Pratte's `.../prattes-reef-el-segundo/3d/src/bn2003_fig9_contours.json`; Albany `.../southern-ocean-surf-reef-albany/3d/src/levels2_raw.json`.
- Datum notes: Cables z in m AHD (taken as MSL); Boscombe m ODN (= MSL +-0.1 m); Borth m ODN with MSL = +0.31 m (+-0.15, assumed LiDAR datum ODN); Palm Beach depths below chart datum (LAT assumed); contour OFFSETS are insensitive to a constant datum shift except through the local slope.
- Not done: wave direction and wave shadow (the lee is taken as the shore directly behind the reef, +-1 L); no wave-driven transport calculation; no offshore Cables survey after 2002 exists in the repo (the other FR files in the DoT zip do not cover the reef); the origin of the Borth north ridge was not identified; Poole Bay groyne positions were not mapped onto the CCO lines.

## 8. Status

Complete for the brief (T1-T4 on every reef with measured data, T5 beach levels at Cables, 3 figures). Open points, none blocking: (1) the Borth north ridge and the Poole Bay groyne/recharge positions are unidentified; (2) Mount Maunganui and Palm Beach could be re-tested if a dated pre-construction contour set is supplied; (3) the Cables beach-level files were found late (inside the DoT zip) and are analysed only for the 0, +1, +2 m AHD contours.

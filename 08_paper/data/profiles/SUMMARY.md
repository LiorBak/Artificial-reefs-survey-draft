# Cross-shore profiles of the reefs - SUMMARY

Generated 2026-10-19 by `08_paper/analysis/extract_profiles.py` (re-runnable) from the DEFAULT version of each 3D model in `07_scale/shapes/<slug>/3d/model.js` (read only). One JSON per reef with a 3D model: `08_paper/data/profiles/<slug>.json` (metadata, datum, shoreline definition, profiles every 1 m on two or three lines, metrics, sources, caveats); the four reefs without a 3D model: `08_paper/data/profiles/_no_3d_model.json`.

Every number for the nine modelled reefs is **DERIVED** from the model grids by the method stated here and in each JSON (not a new measurement). The inputs behind each model and their sources are cited in the JSON field `key_inputs` and in `07_scale/shapes/<slug>/3d/METHODS_3D.md`. The re-implemented reef surfaces reproduce the volumes stated by the models to within 1 % (JSON `reconstruction_check`). z = metres above MSL (each model's datum link is in the JSON field `datum`); y = offshore distance from the model shoreline y = 0 (defined differently per reef, see section 2).

## 1. Master table, all reefs (default version; crest-line profile)

Crest line = cross-shore line (constant model x) through the shallowest crest cell, EXCEPT for the reefs in section 1a, where a per-reef SURF CUT replaces it (Lior 2026-10-19). Ramp = seaward face from the seaward edge of the crest zone (points within 0.10 m of the line maximum) to the seaward toe (last point where the reef is at least 0.10 m above the natural seabed). Mean slope = ramp drop / ramp length; max slope = steepest 2 m central difference on the ramp. Crest depth below MSL is negative where the crest is above MSL (Borth). "(cut)" = the model surface stops at its outline with more than 0.5 m of reef still standing, so the toe is not where the surface meets the seabed. Alongshore length = x-span of reef cells at or above the level: (a) -0.5 m MSL, (b) 0.5 m below the crest (the request "at crest -0.5 m" is ambiguous, both given).

| Reef | Version / basis | Crest z (m MSL) | Crest depth below MSL (m) | Crest height above bed (m) | Crest distance offshore (m) | Toe z reef / bed (m MSL) | Drop crest to toe, on reef / to bed (m) | Ramp length (m) | Mean seaward slope | Max seaward slope | Alongshore length (a) z>=-0.5 m / (b) z>=crest-0.5 m (m) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **borth-coastal-defence-reef** | lidar_2022 | 0.47 | -0.47 | 4.78 | 251 from MSL line (y=338) | -3.85 / -4.30 | 4.32 / 4.77 | 40 | 1:9.4 (6.0 deg) | 1:2.5 (21.4 deg) | 66 / 14 |
| **boscombe-surf-reef** | idealised | -0.90 | 0.90 | 3.84 | 214 from MSL line (y=206) | -5.16 / -5.41 | 4.26 / 4.51 | 13 | 1:3.1 (17.9 deg) | 1:2.3 (23.8 deg) | none / 69 |
| **bunbury-airwave** | installed_Dec2019_spherical_cap | -0.68 | 0.68 | 1.99 | 34 from MSL line (y=37) | -2.59 / -2.99 | 1.91 / 2.31 | 5 | 1:2.7 (20.4 deg) | 1:1.8 (28.7 deg) | none / 6 |
| **cables-reef-wa** | survey_surface_1999_11 | -1.92 | 1.92 | 1.62 | ~249 from fitted shoreline (derived; y=269) | -3.87 / -6.52 (cut) | 1.95 / 4.59 | 45 | 1:23.7 (2.4 deg) | 1:6.6 (8.6 deg) | none / 82 |
| **mount-maunganui-reef** | multibeam_2013_m2p0 | -2.08 | 2.08 | 2.56 | 302 from MSL line (y=302) | -4.22 / -4.91 (cut) | 2.14 / 2.83 | 20 | 1:9.3 (6.1 deg) | 1:1.7 (30.0 deg) | none / 65 |
| **narrowneck-gold-coast** | photo_2020-08-08 | -1.92 | 1.92 | 0.92 | 221 from MSL line (y=216) | -3.02 / -4.00 (cut) | 1.10 / 2.08 | 16 | 1:14.8 (3.9 deg) | 1:14.3 (4.0 deg) | none / 104 |
| **palm-beach-gold-coast** | as_built_2019 | -1.50 | 1.50 | 3.59 | 263 from MSL line (y=263) | -6.83 / -6.99 | 5.33 / 5.49 | 89 | 1:17.0 (3.4 deg) | 1:13.3 (4.3 deg) | none / 61 |
| **prattes-reef-el-segundo** | state_B | -1.86 | 1.86 | 1.35 | 77 from MSL line (y=77) | -2.60 / -3.27 (cut) | 0.74 / 1.41 | 1 | 1:1.4 (35.2 deg) | 1:2.7 (20.2 deg) | none / 56 |
| **southern-ocean-surf-reef-albany** | design_bluecoast | -1.97 | 1.97 | 2.53 | 123 from MSL line (y=118) | -7.07 / -7.37 | 5.10 / 5.40 | 99 | 1:19.8 (2.9 deg) | 1:3.5 (16.0 deg) | none / 26 |
| **kovalam-reef-india** | no 3D model (card / FEASIBILITY) | unknown as a located value | unknown as a located value. Range only: "submergence 0.2-3.4 m", datum not stated, not tied to any position on the reef (Blacka et al. 2013, Table 4.2, report p.66) | unknown | unknown | toe/bed: unknown. Water depth at the reef "1.3-3.7 m" (a range, datum not stated) (Blacka et al. 2013, Table 4.2, report p.66) | unknown | unknown | unknown | unknown | 65 m (Blacka et al. 2013 Table 4.2: longshore dimension); trace 59 m (LOW) |
| **opunake-reef** | no 3D model (card / FEASIBILITY) | unknown as a located value | shallowest contour 0.0 m below chart datum (chart datum = LAT) (design, consent stage; TRC 2009 printed p.3). Relative to MSL: not converted (no tide level with datum fetched; Blacka 2013 Table 4.3 tide range > 3.0 m) | unknown | unknown | toe/bed: built in 3.0 to 1.8 m of water below chart datum (LAT) on a thin sand layer over rock, no excavation (TRC 2009 printed pp.3-4; Blacka 2013 Table 4.2 p.65: depth 1.8-3.0 m) | unknown | unknown | unknown | unknown | design long axis 99 m, bearing 63 deg (occupation area 189 x 94 m rectangle); true footprint unknown |
| **burkitts-reef-bargara** | no 3D model (card / FEASIBILITY) | unknown as a located value | unknown (no crest or minimum-depth figure found; natural basalt platform awash/exposed on satellite at unknown tide) | unknown | unknown | toe/bed: unknown (dive-site depth "to ~9 m" is a site-wide maximum, not a profile; not used) | unknown | unknown | unknown | unknown | unknown (reef zone not located) |
| **mexico-reef-2026-unnamed** | no 3D model (card / FEASIBILITY) | unknown as a located value | unknown (not disclosed in any source) | unknown | unknown | toe/bed: unknown | unknown | unknown | unknown | unknown | unknown |

### 1a. Per-reef surf cuts (override of the automatic crest line; Lior 2026-10-19)

For these reefs the automatic crest line does not cross the part of the reef where the wave breaks and is surfed, or is not perpendicular to the local shoreline. The row above (and `lines.crest_line` in the JSON, used by every downstream script) is the SURF CUT: a line through the stated anchor, perpendicular to the shoreline, sampled every 1 m by the same bilinear interpolation on the model grids. The automatic line stays in the JSON as `lines.crest_line_auto` (reference only).

| Reef | Automatic line x (m) | Surf cut anchor (x, y) (m) | Cut direction | Reason |
|---|---|---|---|---|
| borth-coastal-defence-reef | -63.0 | -43.5, 338.0 | model y axis (shore-normal frame) | Lior 2026-10-19: move the cut a little to the right in the plan of Figure 1 (looking seaward), i.e. 10 m south (model x -33.5 -> -43.5 m), so that it crosses the middle of the main ridge of the northern (boot) surf reef instead of its northern shoulder. No source locates the surf break at Borth (reef card: no ride or break position found), so the position is a judgement on the plan. Cut perpendicular to the shoreline (model x constant; the Borth frame is shore-normal). |
| cables-reef-wa | -18.0 | -5.0, 274.8 | offshore bearing 277.8 deg T (-17.5 deg from model y) | Lior 2026-10-19: the automatic crest line followed the design-frame y axis, which is about 17.5 deg off the shore normal, and passed through the west arm. The cut now goes through the middle of the reef (area centroid of the footprint) and is perpendicular to the local shoreline: fitted 0 m AHD line, bearing 7.8 deg T (07_scale/shapes/cables-reef-wa/HANDOFF.md, shore_and_datum.py), so the cut runs offshore at bearing 277.8 deg T. Check: the mean down-slope direction of the model seabed over the reef area (x -80..80 m, y 200..330 m) is 17.9 deg from the model +y axis, the same side and within 0.4 deg. |
| southern-ocean-surf-reef-albany | 48.0 | 17.0, 118.0 | model y axis (shore-normal frame) | Lior 2026-10-19: the automatic crest line (x = 48 m, through the -1.0 m AHD take-off plateau at the offshore end) lies on the short offshore part of the reef, not where the wave is ridden. The cut is moved to the middle of the long -2.0 m AHD ridge ("crest 110 m @ -2 m AHD", City of Albany / Bluecoast design table, SOURCE_AUDIT_2026-10-10 design_table): the ridge cells of the model (row-wise maximum of the reef surface, z > -2.15 m) run from (x 3, y 68) to (x 38, y 168); the middle of that -2 m ridge is about (x 17, y 118). Cut perpendicular to the shoreline (model x = 17 m constant; the Albany frame is shore-normal). Built reef is a left-hander with the take-off at the offshore (east) end and the ride along this ridge (design table "left-hander, peel 60 deg, rides to 100 m"; 07_scale/shapes/southern-ocean-surf-reef-albany/HANDOFF.md, 3d/REGISTER_3D.md A7). |

Sizes of the four reefs without a 3D model (card / FEASIBILITY values, full citations in `_no_3d_model.json`):

* **kovalam-reef-india**: plan 65 m longshore x 85 m cross-shore, 90 m offshore (Blacka et al. 2013, Table 4.2 p.66); volume 4,000 m3 (Mead and Borrero 2011, p.4), 4,300 m3 (Rendle 2016 Table 2.1 p.41), 4,800 m3 (RWR / ICM); 30 m long sand-container units. Project trace of the oblique photo: 59 x 41 m default, 546-1,681 m2 depending on the assumed camera height (LOW confidence; 07_scale/shapes/kovalam-reef-india/FEASIBILITY.md). Read in: 07_scale/shapes/kovalam-reef-india/FEASIBILITY.md; 02_research/reefs/kovalam-reef-india.json (size, references R13, R14, R15).
* **opunake-reef**: design about 99 m long x 30 m wide x 3.5 m high, plan area about 2,970 m2 (a bounding rectangle 99 x 30, not the true footprint), volume about 4,900 m3 (TRC 2009 printed p.4); Blacka 2013 Table 4.2: 30 m longshore x 100 m cross-shore, ~300 m offshore; 27 bags in place by April 2008, structure not completed (Sept 2009). Read in: 07_scale/shapes/opunake-reef/FEASIBILITY.md; 02_research/reefs/opunake-reef.json (size, references R18, R14).
* **burkitts-reef-bargara**: about 300 m3 of rock moved, at least 12 large basalt boulders relocated (RWR Burkitts Reef page; Swellnet comment 2022); traced natural basalt platform 31,485 m2 minimum (321 x 377 m, Esri 2025-09-05, LOW confidence) which is NOT the reshaped zone; Redgard Phase 3 work-zone ellipse about 1,750 m2 (43 x 52 m, +-20-30 m, LOW). Read in: 07_scale/shapes/burkitts-reef-bargara/FEASIBILITY.md; 02_research/reefs/burkitts-reef-bargara.json (size; references R4, R8).
* **mexico-reef-2026-unnamed**: not disclosed; "3,000 truckloads" of quarried boulders (Hollywood Reporter 2025-04-22). The 160 x 80 m analogy envelope in 07_scale/reefs/ and Gemini's ~140 x 75 m are unsourced and not used. Read in: 07_scale/shapes/mexico-reef-2026-unnamed/FEASIBILITY.md; 02_research/reefs/mexico-reef-2026-unnamed.json (size; references R1, R3).

## 2. Datum and shoreline definition per reef (what "offshore distance" is measured from)

| Reef | y = 0 (model shoreline) is | z = 0 is | Seabed under the reef |
|---|---|---|---|
| borth-coastal-defence-reef | defence line (back of shingle beach), not the MSL line | z = metres above MSL | model.js seabed (5 m grid, z_MSL) |
| boscombe-surf-reef | surf line of 2011-09-28 (about 8 m seaward of the MSL line) | z = metres above MSL | model.js seabed.z_cm (2 m grid, z_MSL) |
| bunbury-airwave | fitted 0 m AHD contour (about MSL) | z = metres above MSL | model.js seabed (5 m grid resampled from the 10 m 2009 WA DoT airborne-lidar grid, z_MSL = AHD - 0.1; gap-filled cells f |
| cables-reef-wa | nominal design-frame origin, NOT the shoreline (fitted 0 m AHD line about 254 m E of the reef centroid; derived distance given) | z = metres above MSL, MSL taken = AHD (A12). Surveyed versions are in AHD directly. Design versions: reading A (default for design) z_MSL = z_RL - 0.716 (Fremantle LWD to AHD, DNM TR12 Table 3, +-0.04 m) | model.js seabed (5 m grid, y 190-420 m, x -150..150 m) |
| mount-maunganui-reef | wet/dry sand line = MSL line of the model | z = metres above present MSL | Alongshore-UNIFORM cross-shore profile (no x dependence) |
| narrowneck-gold-coast | waterline of Esri 2020-08-08 image | z = metres above MSL | model.js seabed (5 m grid, z_MSL) |
| palm-beach-gold-coast | waterline of Esri 2025-12-01 taken as MSL | z = metres above MSL | model.js seabed.z_cm (4 m grid, z_MSL) |
| prattes-reef-el-segundo | MSL waterline (z = 0 of the DEM profile) | z = metres above MSL (NOAA 9410840 Santa Monica, epoch 1983-2001) | model.js seabed.profile_z_m (5 m spacing, NOAA NGDC 2010 Santa Monica 1/3 arc-second NAVD88 DEM, mean of 31 alongshore s |
| southern-ocean-surf-reef-albany | beach-face line (edge of dry sand); MSL line 5 m landward | z = metres above AHD, taken as MSL (assumption A2) | model.js seabed.profile (17 knots y -> z AHD=MSL, linearly interpolated; the 5 m seabed.z grid reproduces it within 0.04 |

Full wording of datum, frame, shoreline, reef-surface rule and seabed per reef: JSON fields `datum`, `frame`, `shoreline_definition`, `method.reef_surface`, `method.seabed`, `caveats`.

## 3. Centreline (x at the alongshore mid-point of the footprint) and second crest line

| Reef | Line | x (m) | crest z (m MSL) | crest y (m) | seaward toe y (m) | toe z reef / bed (m MSL) | thickness at toe (m) | ramp length (m) | mean seaward slope | max seaward slope | seabed slope MSL line to seaward toe | seabed slope under reef |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| borth-coastal-defence-reef | centreline | -33.5 | 0.46 | 348 | 396 | -3.94 / -4.30 | 0.36 | 46 | 1:10.7 | 1:2.6 | 1:71 | 1:2022 |
| borth-coastal-defence-reef | second_crest_line | -33.0 | 0.46 | 348 | 396 | -3.94 / -4.30 | 0.36 | 47 | 1:10.8 | 1:2.6 | 1:71 | 1:2228 |
| boscombe-surf-reef | centreline | 5.5 | -0.90 | 202 | 249 | -4.95 / -5.25 | 0.30 | 12 | 1:3.0 | 1:2.3 | 1:49 | 1:182 |
| boscombe-surf-reef | second_crest_line | 17.0 | -0.90 | 190 | 242 | -4.56 / -4.82 | 0.26 | 18 | 1:4.9 | 1:2.2 | 1:52 | n/a |
| bunbury-airwave | centreline | 0.0 | -0.68 | 37 | 43 | -2.59 / -2.99 | 0.40 | 5 | 1:2.7 | 1:1.8 | 1:13 | 1:17 |
| bunbury-airwave | second_crest_line | -0.2 | -0.69 | 37 | 43 | -2.60 / -2.99 | 0.39 | 5 | 1:2.7 | 1:1.8 | 1:13 | 1:17 |
| cables-reef-wa | centreline | 1.8 | -2.08 | 267 | 303 | -3.98 / -5.51 | 1.53 | 36 | 1:18.9 | 1:8.3 | n/a | 1:19 |
| cables-reef-wa | second_crest_line | 28.0 | -1.74 | 252 | 272 | -3.48 / -4.03 | 0.55 | 19 | 1:11.4 | 1:5.7 | n/a | 1:31 |
| mount-maunganui-reef | centreline | -0.5 | -2.71 | 340 | 344 | -5.06 / -5.19 | 0.13 | 4 | 1:1.7 | 1:1.2 | 1:66 | 1:70 |
| mount-maunganui-reef | second_crest_line | -22.5 | -2.03 | 299 | 313 | -4.42 / -4.79 | 0.37 | 8 | 1:3.5 | 1:1.7 | 1:65 | 1:67 |
| narrowneck-gold-coast | centreline | -1.0 | -5.43 | 336 | 369 | -6.39 / -7.36 | 0.97 | 32 | 1:33.3 | 1:3.1 | 1:51 | 1:65 |
| narrowneck-gold-coast | second_crest_line | -40.0 | -2.32 | 239 | 332 | -5.27 / -6.24 | 0.97 | 37 | 1:12.5 | 1:2.2 | 1:54 | 1:47 |
| palm-beach-gold-coast | centreline | 0.5 | -1.50 | 274 | 367 | -6.86 / -6.99 | 0.13 | 85 | 1:16.0 | 1:12.9 | 1:53 | 1:55 |
| palm-beach-gold-coast | second_crest_line | -5.0 | -1.50 | 280 | 369 | -6.87 / -6.99 | 0.12 | 80 | 1:15.2 | 1:12.5 | 1:53 | 1:57 |
| prattes-reef-el-segundo | centreline | -0.0 | -2.42 | 94 | 103 | -3.75 / -4.02 | 0.27 | 5 | 1:4.0 | 1:1.8 | 1:26 | 1:33 |
| prattes-reef-el-segundo | second_crest_line | 26.5 | -1.89 | 78 | 80 | -2.58 / -3.30 | 0.73 | 1 | 1:1.5 | 1:2.9 | 1:24 | 1:32 |
| southern-ocean-surf-reef-albany | centreline | -2.0 | -2.01 | 80 | 217 | -6.87 / -7.27 | 0.40 | 113 | 1:23.7 | 1:4.7 | 1:31 | 1:29 |
| southern-ocean-surf-reef-albany | second_crest_line | -3.0 | -2.03 | 83 | 217 | -6.94 / -7.27 | 0.33 | 113 | 1:23.4 | 1:4.8 | 1:31 | 1:29 |

For two-arm reefs (Cables, Mount Maunganui, Narrowneck, Prattes) the centreline passes through the apex block or the gap between the arms and the second crest line is the other arm; for single-body reefs the second crest line lies next to the centreline. See JSON `caveats`.

## 4. Alongshore extent of the reef above given levels (union length of x-columns, m)

| Reef | z>=+0.5 | z>=+0.0 | z>=-0.5 | z>=-1.0 | z>=-1.5 | z>=-2.0 | z>=-2.5 | z>=-3.0 | z>=-4.0 | z>=-5.0 |
|---|---|---|---|---|---|---|---|---|---|---|
| borth-coastal-defence-reef | 21 | 61 | 66 | 71 | 75 | 79 | 88 | 92 | 96 | 96 |
| boscombe-surf-reef | - | - | - | 66 | 71 | 77 | 81 | 83 | 88 | 90 |
| bunbury-airwave | - | - | - | 5 | 8 | 10 | 12 | 12 | 12 | 12 |
| cables-reef-wa | - | - | - | - | - | 76 | 100 | 108 | 119 | 119 |
| mount-maunganui-reef | - | - | - | - | - | - | 58 | 64 | 70 | 70 |
| narrowneck-gold-coast | - | - | - | - | - | 12 | 67 | 76 | 98 | 103 |
| palm-beach-gold-coast | - | - | - | - | 42 | 61 | 73 | 87 | 110 | 121 |
| prattes-reef-el-segundo | - | - | - | - | - | 10 | 56 | 58 | 58 | 58 |
| southern-ocean-surf-reef-albany | - | - | - | - | 16 | 54 | 73 | 83 | 97 | 109 |

Levels are metres above MSL; "-" = no reef cell that shallow. Borth counts the northern surf reef only (the southern oval is a shore-parallel breakwater, reported separately in its JSON under `secondary_structure`). Both readings of "alongshore length at crest -0.5 m" are in each JSON: `global.alongshore_length_z_ge_minus0p5_m_msl` and `global.alongshore_length_z_ge_crest_minus0p5` (span and union).

## 5. Evidence layers and alternative surfaces (not the default; own crest line)

| Reef | Layer | crest z (m MSL) | crest height above bed (m) | seaward toe thickness (m) | ramp length (m) | mean seaward slope | max seaward slope | note |
|---|---|---|---|---|---|---|---|---|
| boscombe-surf-reef | surveyed_surface_2011-04 | -0.72 | 4.08 | 0.11 | 46 | 1:12.1 | 1:5.7 | April 2011 DGPS surface (Rendle and Davidson 2012 Fig. 9, colour read; reef.grid.surveyed_z_cm) AFTER the container failure (March-April 2011); evidence layer,  |
| cables-reef-wa | design_plan_original_1999 (datum reading A) | -1.84 | 1.47 | 0.40 | 44 | 1:12.5 | 1:5.0 | Design surface on the measured bed, original-plan footprint (Lyons 1992 / Blacka 2013 Fig. A.2), crest RL -1.0 = -1.72 m AHD (reading A, offset 0.716 m); grid v |
| mount-maunganui-reef | multibeam_2013-07-18_DEM_from_BoPRC_Fig5 | -1.29 | 3.21 | 0.91 | 81 | 1:24.0 | 1:5.4 | 18 Jul 2013 multibeam DEM decoded from the hue of BoPRC Fig. 5 (colour-read, see model.js survey2013.note; z_MSL cm); evidence layer, 5 years after completion,  |

## 6. Reading guide and caveats common to all reefs

* **What is survey and what is a rule**: Cables (Nov 1999 sounding surface), Borth (2022 LiDAR DSM) and Mount Maunganui (rise inside the -2.0 m CD contour from the 2013 DEM) carry survey information; Boscombe (flat crest, 1:3 flanks), Prattes (constant 1.35 m stack, 1:1 flanks), Bunbury (spherical cap), Palm Beach (contour interpolation), Narrowneck and Albany (design-surface rules) are idealised. Ramp lengths and slopes are model results and inherit these assumptions; the surfaces were not re-measured.
* **Seabed**: the natural seabed under each reef is interpolated (a pre-construction survey exists only for Cables, 1998). Mount Maunganui uses an ASSUMED as-built bed of -3.6 m CD; Palm Beach and Narrowneck rely on Navionics/multibeam with datum assumptions. Crest HEIGHT and ramp slopes depend on these; crest LEVEL is sourced for Mount Maunganui, Boscombe, Palm Beach, Prattes and Albany (design or stated values), surveyed for Cables and Borth.
* **Slopes are along the model y axis** (the cross-shore direction of the model frame). For oblique ridges (Albany, Boscombe, Borth boot) the slope normal to the crest differs; for Cables the frame axis is about 17.5 deg off the shore normal, so the Cables surf cut (crest_line) is turned 17.5 deg to the shore normal and its distances are along that line; the centreline and second crest line of Cables still follow the frame axis.
* **Tidal planes** (m above MSL, small-tide sites): JSON field `tidal_planes_m_above_msl`.
* **JSON layout**: `lines.<name>.profile.{offshore_m, seabed_msl_m, reef_msl_m}` are equal-length arrays at 1 m spacing (`null` = no reef / no data); `lines.<name>.metrics` are the numbers above; `global` holds crest, footprint and alongshore extents; `extra_layers` holds the evidence layers; `reconstruction_check` the volume test.

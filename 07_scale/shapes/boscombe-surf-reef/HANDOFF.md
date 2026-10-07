# HANDOFF - boscombe-surf-reef (shape + 3D model + seabed extension)

Written 2026-10-07 by the agent that finished the seabed-extension re-check run. Read this first; open other files only for a specific fact.
Datums: z = 0 is mean sea level (MSL); ACD = above chart datum (CD); z_ACD = z_MSL + 1.40 (S4 NTSLF: CD is 1.40 m below ODN; ODN ~ MSL, A4). Frame: x alongshore (bearing 83.4 deg, east; the pier is at negative x), y offshore (bearing 173.4 deg), metres.
Source ids S1-S13 are those of `3d/METHODS_3D.md` section 2; equation ids E1-E16 and assumptions A1-A16 are in the same file.

## 1. Status per stage

| Stage | Status | Date | Confidence and reason |
|---|---|---|---|
| Plan trace (`shape.json`) | verified, 25 vertices, 4,042 m2, minimum rotated rectangle 121.1 x 45.0 m, shore normal 173.4 deg | 2026-10-05 | medium: three plan sources agree; area is 60 % below the repeated "about 1 ha" in the literature (VERIFY.md) |
| 3D reef + seabed (survey part) | built; reef = idealised as-built loft (flat crest +0.5 m ACD, 1:3 flanks) on the April 2011 DGPS seabed (Fig. 9) | 2026-10-05 | medium: plan medium; seabed +-0.2 m colour read; datum of the Fig. 9 zero is an assumption (A3) but now supported by two independent tests |
| Seabed extension (beach + offshore) | DONE: grid 161 x 359 cells, 2 m, x -160..160, y -66..650 m; zone codes 3/4/5 added; reef cells unchanged | 2026-10-07 | beach +-0.36 m (CCO, measured); blend +-0.5 m; offshore y > 380 m +-1.2 m (extrapolated) |
| Cross-checks of the extension | DONE: CCO datum test, Navionics z16 nearshore + offshore, EMODnet DTM 2024 | 2026-10-07 | nearshore within 0.26 m; offshore r.m.s. 1.2 m with a known alongshore trend (open issue 1) |
| Documentation | `METHODS_3D.md` (sections 3.4, 3.8, 4 items 9-13, 5, 7, 8 updated), `SOURCES_3D.md`, `docs.js` regenerated | 2026-10-07 | complete |
| Viewer | `index.html`: zone colouring toggle + legend, draped shorelines and waterline of the selected level, default plan/oblique views show beach and reef; scene structure unchanged | 2026-10-07 | previews rendered and viewed |
| Image registry | 32 rows in `03_images/reefs/boscombe-surf-reef/images.json` + `IMAGES.md`; `check_registry.py` reports NO error for Boscombe; pending 3D checks: 0 | 2026-10-07 | complete |
| Page (`04_build`) | NOT touched by this run | - | the page still has the old model; needs the new `model.js` / `docs.js` (see next steps) |

confidence_3d = medium (unchanged). Reason in one line: plan, seabed and crest are sourced and agree; the survey datum and the as-built flanks are assumptions.

## 2. Decisions and why (one line each)

- Seabed extended instead of zooming the camera (Lior 2026-10-07: "make the 3D larger so the shoreline is visible"): the old grid started at y = 0 and the shoreline was outside the model.
- Beach and nearshore from Channel Coastal Observatory (CCO) beach profiles, not from the Gemini folder or extrapolation (S13; public, Open Government Licence v3; heights m ODN).
- CCO survey date 2010-04-20: the nearest date at which all 11 lines exist (the A lines start that day); dates closer to the 2009 as-built state exist only on 2 lines. Date-to-date variability of the beach is 0.1-0.5 m (METHODS validation 10).
- z_MSL = z_ODN on the CCO beach (ODN ~ MSL within +-0.1 m, A4); survey cells keep z_MSL = z_ACD - 1.40 (A3, E6).
- Offshore y 380-650 m: slope only from EMODnet DTM 2024 (-1.41 %, REPORT 9.1), level continued from the model's own row y = 380; EMODnet levels are NOT used (1.1-3.1 m deeper than the survey, no reef in the DTM).
- The original survey cells (code 0), the cells under the reef (code 2) and the whole reef surface were left byte-identical so that the page's "All (compare)" view and the earlier results stay valid (checked cell by cell: 0 of 4,295 + 1,580 cells changed).
- The model shoreline: the viewer draws the tidal waterline of the selected level (contour of z on the grid) plus the 28 Sep 2011 surf line y = 0 as a separate cyan line; y = 0 sits at z = -0.2 m (about MLWN).
- Stated uncertainty of zone 5 raised from +-1.0 m (REPORT 9.1) to +-1.2 m after the Navionics check (r.m.s. 1.20 m).
- Offshore alongshore tilt NOT corrected (kept as specified in REPORT 9.1); the fix is quantified and documented as open issue 1.
- Registry row img-01 corrected: the photo shows a land-side sand heap, not an exposed reef mound.

## 3. Key numbers (units, datum, source)

Reef and survey (unchanged since 2026-10-05)
- Outline area 4,042 m2 (shape.json; model 4,040); min rotated rectangle 121.1 x 45.0 m; shore normal 173.4 deg; position about 220-225 m offshore, west edge 242 m east of the pier head (S7, S6, S2).
- Design crest +0.5 m ACD = -0.9 m MSL (S3); Oct 2009 profile tops +0.45 (across) and +0.65 (along axis) m ACD; April 2011 highest surveyed point +0.68 m ACD at (x 20, y 193) at the shoreward end (S2).
- Seabed under the outline: mean -3.56, min -4.72, max -2.40 m ACD (survey 2011, Fig. 9, +-0.2 m read).
- Flanks 1:3 assumed (A7; survey median gradient 0.172 = 1:5.8; +-30 %).
- Loft volume 13,119 m3 vs about 13,000 m3 stated (+0.9 %); April 2011 survey relief volume 9,573 m3 (damaged).
- Water levels (S3 Table 1 converted with E6, m MSL): HAT +1.19, MHWS +0.81, MHWN +0.27, MSL 0, MLWN -0.23, MLWS -0.95, LAT -1.46; MHWS-MLWS 1.76 m. Double high water; viewer uses static levels. Gauge Bournemouth Pier ~1.5 km west.

Extended seabed (2026-10-07; scripts/extend_seabed.py; METHODS 3.4)
- Grid: nx 161, ny 359, dx = dy = 2 m, x -160..160, y -66..650; one code and one datum weight per cell.
- Zones (cells by code are in the zone map, `3d/annotated/seabed_zone_map.png`): 0 Fig. 9 survey (April 2011), 1 spline extrapolation (survey ends at y about 312 m; 305-380 m is extrapolated), 2 interpolated under the reef, 3 CCO beach profile, 4 blend CCO to survey (40 m decay), 5 EMODnet slope extrapolation (y 382-650).
- CCO data (S13): 11 lines 5f00424, 424A, 425, 425A, 426, 426A, 427, 427A, 428, 428A, 429 at x = +222, +176, +145, +96, +43, -5, -58, -87, -142, -183, -221 m; back of beach y about -66 m at z about +3.3 m ODN; seaward ends y 21-38 m at about -1.0 m ODN; 17-28 points per line (spacing 4-6 m). Seven lines lie inside the grid, 428A and 424A fix the edge columns, 429 and 424 are not needed. Raw copies (316 text files, all dates 2004-2026): `src/cco_profiles/`.
- Equations: E13 beach interpolation across lines; E14 `z = S + R` with the CCO offset decaying over L = 40 m (smoothstep); E15 `z = z(x,380) - 0.0141 (y - 380)`; E16 datum weights. Slope s = 0.0141 +-0.0010 from four EMODnet cells (REPORT 9.1).
- Row y = 380: mean z -7.78 m MSL, alongshore slope +0.76 m per 100 m of x (spline extrapolation); EMODnet cell at y 380 = -7.05 m LAT = -8.51 m MSL (model 0.7 m shallower).
- Shoreline (model contours, depends on x): MSL waterline y = -3 to -8 m; MHWS -10 to -30; HAT -27 to -37; MLWS +24 to +38; LAT +51 to +72; surf line y = 0 at z = -0.2 m. Beach slope about 0.04 between +1.2 and -0.3 m. A level error of 0.35 m moves a waterline by about 9 m.
- Uncertainty (1 sd): beach 0.36 m (date 0.28, ODN 0.1, position 5 m x slope 0.04); blend 0.5 m; zone 5 1.2 m (correlated along x).

Cross-checks of the extension (METHODS section 4)
- Item 9 CCO datum test (A3): at the seaward ends of the 11 lines, CCO (ODN) minus the Fig. 9 spline read as chart datum = +0.03 m (sd 0.30, n = 11); if the Fig. 9 zero were ODN: -1.37 m. Supports chart datum (independent of EMODnet and Navionics; caveat: spline extrapolated 60-80 m, two dates).
- Item 10 beach variability: 2011-03-23 minus 2010-04-20 r.m.s. 0.28 m (11 lines); 2009-09-22: 0.49 m (2 lines); 2009-11-30: 0.13 m (1 line).
- Item 11 Navionics z16 nearshore (31 scans x -150..150, `nav_z16_nearshore.json`): chart HW line at model z +0.96 m (expected +0.81 MHWS, +0.15); chart datum boundary at -1.66 (expected -1.40, -0.26); 1 m below CD at -2.53 (expected -2.40, -0.13).
- Item 12 Navionics z16 offshore (11 soundings, y 428-604, `nav_z16_offshore.json`): model minus chart depth mean -0.27, sd 1.23, r.m.s. 1.20 m; trend -1.21 +- 0.11 m per 100 m of x; flattening row 380 would give r.m.s. 0.51 m (0.46 with the EMODnet gradient). `offshore_tilt_check.json`.
- Item 13 EMODnet DTM 2024 cells vs model seabed: mean -1.80 m (sd 0.66, 7 cells); reef cell -1.39 m; offset not constant, so not a datum shift (EMODnet REPORT 6).
- Earlier checks (2026-10-05, still valid): 16 Navionics soundings model minus chart +0.06 m (sd 0.49); Navionics shoal areas match the survey zones (296 vs 378/492 m2 drying, 956 vs 950 at 0.5 m, 1,609 vs 1,630/2,073 at 1 m).

## 4. File map (all under `07_scale/shapes/boscombe-surf-reef/` unless stated)

| File | What it holds / when to open it |
|---|---|
| `shape.json`, `METHOD.md`, `VERIFY.md`, `sources.md` | verified plan outline and its trace; open only to change the outline |
| `3d/model.js` (727 KB) | the model data `window.REEF_MODEL` (seabed grid, reef grid, water levels, shoreline, provenance); bulky, generated; do not open, regenerate with `build_3d.py` |
| `3d/index.html` | the viewer (three.js r170 via CDN import map; one seabed mesh, one reef mesh, water plane; zone toggle; draped shorelines; photo-match mode; Methods panel) |
| `3d/build_3d.py` | regenerates `model.js` and `docs.js` from `shape.json`, `scripts/` and the md files; run `python build_3d.py` in `3d/` |
| `3d/docs.js` (87 KB) | `window.REEF_DOCS` = METHODS_3D.md + REQUESTS + SOURCES for the Methods panel; generated |
| `3d/METHODS_3D.md` | the academic methods note (8 sections, E1-E16, A1-A16, validation items 1-13); open sections 3.4 / 4 for the extension |
| `3d/SOURCES_3D.md` | chronological source and processing log with registry ids; the "RE-CHECK RUN 2026-10-07" part at the end holds this run (steps A, coordinator check, 1-5) |
| `3d/REQUESTS_FOR_LIOR.md` | what Lior could read in the Navionics app / Google Earth Pro / elsewhere (section D added 2026-10-07) |
| `3d/model_stats.json` | numbers of the last build (areas, volumes) |
| `3d/scripts/extend_seabed.py` | the seabed extension (E13-E15, constants CCO_DATE, BLEND_L, EMODNET_SLOPE, EMODNET_UNC), called by build_3d.py |
| `3d/scripts/cco_fetch.py`, `cco_load.py` | download of the CCO profiles (public API) and their loader; raw data in `src/cco_profiles/` |
| `3d/scripts/navionics_z16_nearshore.py`, `navionics_z16_offshore.py`, `annotate_z16_nearshore.py`, `offshore_tilt_check.py` | the Navionics z16 cross-checks and the tilt analysis (outputs `nav_z16_*.json`, `offshore_tilt_check.json`) |
| `3d/scripts/figures_extension.py` | the three extension figures |
| `3d/scripts/render_previews.py` | headless Chrome previews (own process, random free DevTools port, fresh profile; THREE from `04_build/3d/vendor` because cdn.jsdelivr.net was unreachable here) |
| `3d/scripts/canon.py`, `survey_*.py`, `fields.py`, `navionics.py`, `annotate_*.py` | frame conversions, Fig. 9 colour read, Navionics reads, text annotations (2026-10-05 work) |
| `3d/annotated/` | annotated images (all registered): `cco_profile_lines_plan.png` (img-30), `cco_profiles_cross_sections.png` (img-31), `seabed_zone_map.png` (img-32), `navionics_nauticalchart_z16_nearshore_vs_model_annotated.png` and `..._offshore_soundings_annotated.png` (on img-14), Fig. 9 reads, Mead/Rendle text evidence, Navionics z17/z18 reads, `datum_check_emodnet.png`, `sat2011_model_frame.png` |
| `3d/preview_*.png` | renders of the viewer: plan, oblique, plan at HAT with source colours, ODN datum switch (2026-10-07), beach eye view, 2x lateral (earlier) |
| `src/` | private research copies of sources (Esri Wayback 2011 and 2025, Fig. 9, Mead Fig. 3a, Navionics screenshots with provenance, `cco_profiles/`) |
| `03_images/reefs/boscombe-surf-reef/images.json`, `IMAGES.md` | image registry (32 rows); `03_images/reefs/check_registry.py` checks it |
| `07_scale/bathymetry/emodnet/REPORT.md` (+ data, figures) | the EMODnet test; section 9.1 holds the Boscombe integration values |

## 5. Open issues, discrepancies, pending checks

1. Zone 5 (y 380-650) alongshore error: the extension copies row y = 380 (spline extrapolation, +0.76 m per 100 m of x) to y = 650, whereas EMODnet (27 cells) shows no alongshore gradient and 11 Navionics soundings show a misfit of -1.2 m per 100 m of x (model too deep at x < 0, too shallow at x > 0, up to +-1.7 m). Replacing row 380 by its alongshore mean would cut the Navionics r.m.s. from 1.2 to 0.5 m. NOT applied (REPORT 9.1 formula kept; zone is context only, flagged +-1.2 m). Decision for Lior / coordinator; if yes: in `extend_seabed.py` replace `z380 = base_msl[-1]` by a flat or blended row (e.g. mean of the row, or blend over y 312-440 m) and re-run `build_3d.py`, then re-render the previews; the reef and survey cells stay unchanged.
2. Registry row img-01 (Flickr 2009-07-28) was described as an "exposed reef mound at extreme low tide"; the picture shows a dry sand heap behind a fence and the safety sign, no sea, no reef. The registry row is corrected; the same wording remains in `02_research/reefs/boscombe-surf-reef.json` images[0], in `05_qa/reef/boscombe-surf-reef_media_recheck.json` and probably in the page caption (04_build not touched by this run).
3. Datum A3 (Fig. 9 zero = chart datum) is still an assumption, now supported by the CCO test (+0.03 m vs -1.37 m), the crest and design-depth evidence and Navionics shoal areas. The EMODnet CDI 117452 metadata page (vertical reference and date of the DTM source survey) is still unread: needs a normal browser (REQUESTS_FOR_LIOR D1).
4. The beach is the CCO surface of 2010-04-20 (after completion, before the 2011 failure), not of 28 Sep 2011; the surf line y = 0 of that image is at an unknown tide (z = -0.2 m on the model beach). Waterlines of the viewer carry +-9 m.
5. Zone 4 (y about 40-100 m, between the CCO line ends and the survey rim) is spline plus decayed offset (+-0.5 m); no data exist there. Rows y 312-380 outside the plotted survey are spline extrapolation (checked 2026-10-05 against Navionics: -0.05 +- 0.47 m).
6. Navionics z16 nearshore chart boundaries are 1 m colour classes with generalised lines: offsets of 0.13-0.26 m are inside that resolution; the chart datum is read as ACD (A9, not stated by the viewer).
7. CCO heights are m ODN; the MSL = ODN assumption (A4, +-0.1 m) was not checked against a local MSL value for 2009-2011.
8. The jsDelivr CDN is unreachable from this machine today; the viewer file keeps the CDN import map; previews intercept the two requests. On a normal machine the viewer loads as before.
9. `04_build` integration unverified: the page's "All (compare)" view exports the reef and seabed meshes; model.js now has seabed ny = 359 (was 191) and y0 = -66 (was 0). If the page code assumes the old grid size or a seabed starting at y = 0, check it (the viewer in `3d/index.html` reads nx, ny, x0, y0 from model.js and works).
10. `check_registry.py` currently fails for other reefs (borth-coastal-defence-reef: unregistered `3d/annotated` and `3d/src/navionics` files); not Boscombe, not touched here.
11. The old reef-state caveats stand: as-built is an idealised loft (flat crest, 1:3 flanks); the April 2011 survey surface is the evidence layer; later history (container failure 2011, closure, ASR liquidation 2012, rebranding 2014/2017) is in the caption and METHODS 3.10, not modelled.

## 6. Requests for Lior

1. Decide open issue 1 (flatten the offshore row alongshore: yes / no). Recommended yes if the offshore corners matter for any picture; otherwise leave.
2. Open the CDI 117452 record (EDMO 2607 OceanWise Limited) in a normal browser and tell us the vertical reference and survey date (D1 in REQUESTS_FOR_LIOR.md).
3. Ask the Channel Coastal Observatory whether nearshore or offshore bathymetry of Poole Bay for 2009-2012 exists (would replace zones 4 and 5; D2).
4. From earlier requests (A-C in REQUESTS_FOR_LIOR.md) still useful: Navionics app depth/datum reading on the reef, Google Earth Pro 2009-2010 imagery and a dated waterline with known tide, the Rendle thesis (Plymouth PEARL 412) via a normal browser.
5. If the page should show a different beach date (for example autumn 2009), say so: 2009-09-22 and 2009-11-30 exist on 2 and 1 lines only.

## 7. Next steps for the next agent, in order

1. If Lior says yes to open issue 1: edit `extend_seabed.py` (offshore rows), run `python build_3d.py` in `3d/`, update METHODS 3.4 / 4.12 / A16 and the zone-5 uncertainty (about +-0.5 m expected), re-render previews with `render_previews.py`, update this file.
2. Page integration (04_build, coordinator): replace the page's Boscombe `model.js` / `docs.js` / viewer by the new ones; confirm the "All (compare)" view still works with the 161 x 359 seabed; update the page caption for img-01 (sand heap).
3. Fix the img-01 wording in `02_research/reefs/boscombe-surf-reef.json` and `05_qa/reef/boscombe-surf-reef_media_recheck.json` (those are the coordinator's files).
4. Read the CDI 117452 metadata (or have Lior do it) and close A3; check MSL against a tide-gauge value (open issue 7).
5. If a photo-match run is planned, use e = 1 and the beach as modelled; the surface texture of the bags is not modelled (A12).

## 8. How this run was done (for trust)

- Brief read: common.md; SOURCES_3D.md re-check entries; METHODS_3D.md sections 2, 3.2, 3.4, 3.8, 4, 5, 7, 8; REPORT 9.1 and 6.1.
- Step A (previous agent, usage limit hit afterwards): CCO data, extension, viewer, previews. Steps 1-5 (this agent): Navionics z16 checks, figures, STEP 0 registry views (img-01/02/03/07 viewed, results written), registry (new rows img-30/31/32, img-14 annotations, img-25..29 resolved), METHODS/docs, previews, this file.
- The extension was verified by a cell-by-cell comparison with the previous model.js and by `python build_3d.py` runs; no 04_build file and nothing in the Gemini folder was touched.

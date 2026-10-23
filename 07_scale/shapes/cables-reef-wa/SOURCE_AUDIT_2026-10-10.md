# Source audit 2026-10-10 - cables-reef-wa (shape, 3D model, viewer, image registry)
Standard: _agent_briefs/task_source_audit.md. Status: ok / fixed / missing / mismatch. [SUPERSEDED 2026-10-10 evening: model values WERE changed by the imagery + bathymetry run, see Addendum 1 at the end. Statement as written at audit time:] Model values were NOT changed (model.js recompiled only to refresh docs.js; areas, volumes, thicknesses, edge levels identical to the pre-audit values; no byte backup of the old model.js was kept, comparison by the printed values).

| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | footprint 4,049 m2 (121 x 76 m); with extension 4,355 m2 (121 x 89) | Blacka et al. 2013 Fig A.2 [img-26]; RWR extension [img-06] | p.93; drawing | trace, scale 6.51 px/m | ok |
| 2 | scale 6.51 px/m sd 0.05 (+-3 %) | printed 26.0/30.0/40.0 m, 0.5 m contours at 1:20 | Fig A.2 | four readings, annotated/A1 | ok |
| 3 | crest RL -1.0, set-out RL -3.0, contours -1.5/-2.0/-2.5, slopes 1:20/1:15/~1:13 | Fig A.2 labels; Pattiaratchi 1999 p.3 | as left | labels read | ok |
| 4 | datum: MTL 0.78 m above datum | Pattiaratchi 1999 p.3 | text | reading A (assumption A1), B switch | ok (now A1 / X3) |
| 5 | tide range 0.8 m | Blacka 2013 Table 4.3 p.67 | table | water slider; HW/LW +-0.4 m = estimate A7 | ok |
| 6 | rock volume 5,500 / 5,000 / 3,500 m3 | Blacka A.1.3; Mead and Borrero 2011 p.2; Wikipedia (card R1) | | 5,500 fits bed (A3); others sensitivity | ok | [see addendum 1]
| 7 | 140 x 70 m, 275 m offshore, depth 3.0-6.0 m, crest 1.0-2.5 m below MSL | Blacka A.1.1, Tables 4.2 p.65 | | validation only | ok |
| 8 | 250 m offshore, 45 deg peel angle, 1:20 slope to the 1 m contour | Pattiaratchi 1999 p.3-4 | | cross-check, orientation | ok |
| 9 | bed gradient 1:30 | Pitt sketch [img-07], contours 3.0-7.0 m | annotated/A4 | read by eye, assumption A4 | ok |
| 10 | bed level RL -3.50 m (y = 270 m) | fitted to 5,500 m3 | build_3d.py D0, G_BED | calibration (A3) | ok, flagged estimated | [see addendum 1]
| 11 | extension 347 m2 / 320 m3 / 0.92 m mean | RWR drawing [img-06] | 'VOLUME = 320 m3' | triangle registration (A6) | ok |
| 12 | max rock thickness | model.js 2.48 m | | | mismatch fixed: METHODS_3D said 2.9 m, now 2.5 (2.48); HANDOFF already 2.5 | [see addendum 1]
| 13 | assumptions A3-A7 cited in METHODS_3D with no list | | | | fixed: section 9 A1-A11 added (viewer Methods tab) |
| 14 | decisions not logged | | | | fixed: section 10 X1-X8 added |
| 15 | sources without "how used" for Mead and Borrero, Wikipedia, card, Pitt 2009, Gemini | | | | fixed: SOURCES_3D table "Sources and how each was used" |
| 16 | density 1.82 t/m3 from '> 10,000 t' | card (RWR/ICM text, R2) | | plausibility check only | ok (card figure is a lower bound) |
| 17 | Pitt 2009 'crest ~1.5 m below lowest tide' | card dossier (SurfingRamps.com.au), original not read | | context | ok, second-hand, labelled |
| 18 | Gemini | not in this repo | | none used | ok (X7) |
| 19 | Blacka citation incl. DOI, Pattiaratchi 1999 ref ED1483CP and URL, Mead and Borrero DOI | registry/card | | | ok |
| 20 | Pattiaratchi et al. 2003 | UWA repository listing | COPEDEC VI, Colombo, 15-19 Sep 2003 | not read | citation completed (venue, date); co-authors, pages NOT CONFIRMED |
| 21 | Bancroft 1999 UWA thesis | web search | title only | not read | partial; degree, pages NOT CONFIRMED; possible as-built source |
| 22 | Ranasinghe et al. 2001; Lyons 1992 | cited by Blacka | | not read | NOT CONFIRMED (web search found nothing) |
| 23 | image registry: 31 rows, all files exist, citation / licence / retrieved / page or figure / how_used present | images.json | | | ok; img-14 and own figures 27-31 have no image_url by nature |
| 24 | materials: granite (Blacka, RWR) vs limestone (Mead and Borrero 2011) | | | not used in the model | discrepancy listed, unresolved |
| 25 | reef card vs model: 275 m offshore vs S1 250 m, volume 3,500 vs 5,500, 140 m vs 121 m traced | card; HANDOFF section 5 | | | mismatch recorded, not a model error; page text states ranges |
| 26 | PAGE_TEXTS_FOR_MAIN.json key_numbers | | | | fixed: sources and assumed/fitted labels added; numbers unchanged and consistent with model.js |
| 27 | viewer panels: Sources and Methods tabs show source list, methods, assumptions, decisions | docs.js | | | fixed (content in the two md files; docs.js rebuilt, parses) | [see addendum 1]

Counts: 27 rows; checked statements ~45; fixed 6 (12-15, 20 partly, 26, 27); missing citation details 3 (rows 20-22). Values that look wrong: none.
Page texts (04_build/data): not edited; main should use the revised 3d/PAGE_TEXTS_FOR_MAIN.json (old -> new in that file's key_numbers lines).

## Addendum 1 (2026-10-10, imagery + bathymetry run): what became stale and the new source rows
Standard: _agent_briefs/task_source_audit.md. The first model (design drawing only) is archived in 3d/archive/pre_imagery_2026-10-10/. Rows below replace rows 6, 10, 12 and 27 of the table above (history kept); statuses: ok / fixed / missing / mismatch / superseded.
| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 6' | rock volume: design surface on the MEASURED bed 3,920 m3 (original plan), 4,249 m3 (with extension); surveyed 4,671 (Nov 1999) and 5,219 m3 (Feb 2002), +-1,000; stated 5,500 (Blacka A.1.3), 5,000 (Rendle p.41, Mead and Borrero 2011 p.2), 3,500 (Wikipedia via card R1) | model.js validation.volumes; scripts/survey_volume.py; papers/ | METHODS_3D 3.4, 4 | stated values are comparison only; no volume is fitted any more | ok; row 6 'fits bed (A3)' SUPERSEDED |
| 10' | bed = measured: DoT 1998 soundings + Perth_5m, -3.68 m AHD at the anchor; 2.84-6.63 m below MSL (A) under the outline | DoT1998 (FR19980330_Reef_Single.txt, 30 Mar 1998), DoT5m | scripts/make_bed.py; bed_measured_canonical.npz | replaces RL -3.50 m fitted at y = 270 (A3) | ok (A3, A4 SUPERSEDED); accuracy +-0.3 m (A13, A14) |
| 12' | max rock thickness: design 2.30 m (original) / 2.47 m (with extension); surveyed surface 2.76 m (Nov 1999) / 2.69 m (Feb 2002); mean 0.97-0.98 / 1.15 / 1.29 m | model.js versions[]; first-run 2.48 m (extension) is now 2.47 m because the bed changed | METHODS_3D 3.4, 11 | - | ok (row 12 value 2.48 superseded) |
| 27' | viewer panels show sources, methods, assumptions A1-A17, decisions X1-X13, change table (section 11) | docs.js rebuilt from METHODS_3D.md / SOURCES_3D.md; index.html patched (surveyed versions ignore the A/B switch, water plane, contours hidden for survey versions) | previews checked | - | fixed |
| 28 | georeference: anchor 32.015644 S, 115.748462 E, theta 9.74 deg ccw, 91.0 % of rock soundings inside the outline, 18.5 % of bed soundings inside, free scale 0.979 | DoT1999 (FR19991122_Single.txt, 840 soundings, survey end 22 Nov 1999) over DoT1998; CC BY 4.0, https://s3-ap-southeast-2.amazonaws.com/transport.wa/Bathymetry/PointData/FR.zip, accessed 2026-10-10 | scripts/georef_fit.py -> georef.json | rigid fit by differential evolution (rock = sounding > 0.6 m above 1998 bed, bed = < 0.2 m) | ok; accuracy +-2 m, +-2 deg |
| 29 | SURVEYED SURFACE Nov 1999 (default version): 4,049 m2 footprint, 4,671 m3, mean 1.15 m, top -1.55 m AHD | DoT1999 minus DoT1998 | what was measured: z of 840 soundings (m AHD, single-beam); method: thickness at soundings, LinearNDInterpolator onto 0.5 m raster, clip >= 0, Gaussian 1 m (build_3d.py survey_version); location: model.js versions[survey_surface_1999_11], 3d/METHODS_3D 3.4 | default 3D surface | ok; accuracy +-0.3 m vertical, +-5 m between lines, +-1,000 m3; single-beam smooths ridges (A15, A17); registry img-38 |
| 30 | SURVEYED SURFACE Feb 2002: 4,049 m2, 5,219 m3, mean 1.29 m, top -1.71 m AHD | DoT2002 (FR20020201_Single.txt, survey end 1 Feb 2002; 5,143 soundings in the window) minus DoT1998 | as row 29 | version survey_surface_2002_02 | ok; same accuracy; registry img-39 |
| 31 | extension not confirmed: +0.43 m mean (median 0.29, n = 23) in the drawn triangle vs +1.29 m inside the plan and +0.19 m in the 25 m ring (n = 809); image brightness equals the surroundings | DoT2002 over DoT1998; SAT (Esri images) | METHODS_3D 3.5; scripts/georef_fit.py (survey_2002_vs_1998); scripts/make_imagery_figs.py | demotes the extension to a separate version (X10) | ok; weak test (23 points) |
| 32 | datum test: design ramp RL minus surveyed AHD = 0.59 m (Nov 1999, n = 454), 0.50 m (Feb 2002, n = 236), sd 0.58 m; A needs 0.78, B 0.00; BoM Fremantle MSL 0.773 m above gauge zero (LWD) | DoT1999, DoT2002; BoM NTC 62230 metadata (4 Jun 2026) https://www.bom.gov.au/ntc/IDO50000/IDO50000_62230.pdf and monthly sea levels https://www.bom.gov.au/ntc/IDO70000/IDO70000_62230_SLD.shtml, accessed 2026-10-10 | model.js validation.survey_check; scripts/shore_and_datum.py | supports reading A within 0.2-0.3 m; A12 (AHD = MSL) added | ok; Fremantle CD-AHD offset NOT FOUND (dead end logged) |
| 33 | shoreline bearing 7.8 deg T; anchor to the 0 m AHD line 254 m (090) / 263 m (080, 100) | DoT5m Perth_5m.tif (5 m cells, AHD, CC BY 4.0), https://s3-ap-southeast-2.amazonaws.com/transport.wa/Bathymetry/Rasters/Perth_5m.tif | scripts/shore_and_datum.py | replaces 'shoreline N-S' (A2) and 270 m (Fig 7, assumed grid) | ok; +-2 deg, +-8 m |
| 34 | outline coincides with the dark rock patch on 5 Esri images (2014-12-03, 2020-03-23, 2022-06-08, 2024-08-15 releases; 2025-12-06 capture); luminance inside / ring 0.35-0.87 | Esri World Imagery and Wayback via satellite.py, accessed 2026-10-10 | src/imagery/, annotated/; registry img-32..37 | independent check (no image data entered the fit) | ok; Wayback capture dates unavailable |
| 35 | 'model values unchanged' claim of the first audit | - | - | - | SUPERSEDED: values changed (before / after table in METHODS_3D 11 and VERIFY.md) |
| 36 | text values used in the page: PAGE_TEXTS_FOR_MAIN.json | model.js | 3d/PAGE_TEXTS_FOR_MAIN.json (old_to_new) | revised for the new default | fixed |
| 37 | Papers: Bancroft (1999), Ranasinghe et al. (2001), Pattiaratchi (2003, 2007) | papers/ grep: citations only (Rendle thesis, NSW review 2013 = Blacka, Mead and Borrero 2011, Narrowneck 2023); web: ResearchGate and UWA repository 403 (not bypassed) | 02_research/dead_ends/cables-reef-wa.json | none | missing (still NOT CONFIRMED / not read); listed in REQUESTS_FOR_LIOR.md |
Counts addendum: 10 new rows (28-37) + 4 replaced; assumptions now A1-A17 (A2, A3, A4 superseded; A9 partly tested), decisions X1-X13 (X2, X4 revised, X8 superseded). Values that look wrong (for main): the reef card's 275 m offshore and 5,500 m3 (card R2) vs measured 254-263 m and surveyed 4,671-5,219 m3; reef card coordinates if any are rounded to 32 00 S 115 45 E (the reef is at 32.0156 S 115.7485 E).

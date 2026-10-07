# HANDOFF - borth-coastal-defence-reef (shape verifier 2026-10-06; 3D model finished 2026-10-07; for the page builder and any later agent)

Read this first. Open other files only for one fact (section/page given). Source ids = shape.json sources/references (sat2024, drg1020-1023, lidar2022, hrpp576f2, ref1-ref10 ...); registry ids = 03_images/reefs/borth-coastal-defence-reef/images.json (-img-NN, 30 rows).
The verifier's HANDOFF (2026-10-06) is superseded by this file; its facts are kept below (sections 3.1-3.4) and updated.

## 1. Status per stage
| stage | state | date | confidence / reason |
|---|---|---|---|
| trace | done by the tracer (4 dated Esri images, 79 vertices on the primary 2024-09-17) | 2026-10-05 | - |
| verify (shape.json status "verified") | done: checks 1-7 in VERIFY.md | 2026-10-06 | HIGH: two mounds clearly visible on four geo-referenced images; outline agrees with the georeferenced Royal Haskoning construction plan (position 0.3-4 m, angle 1-3 deg) and with the 2022 LiDAR; area depends on the edge definition (now 3 versions) |
| outline versions | shape.json outline_versions (lidar_2022 DEFAULT, design_1020, sat_2024), default_outline "lidar_2022", versions_info; canonical.polygons_m unchanged (traced 2024 polygon) | 2026-10-07 | Lior chose the LiDAR default 2026-10-06 (VERIFY.md line) |
| 3D model | BUILT: 3d\model.js (660 kB), index.html (viewer), docs.js, METHODS_3D.md (8 sections), SOURCES_3D.md, REQUESTS_FOR_LIOR.md, previews, annotated A1-A10 | 2026-10-07 | MEDIUM: plan and crests high; seabed medium-low (design bed -4.0 +-0.4 m, hand-read Fig 2, assumed anchor); offshore sea floor 0.9 m deeper than Fig 2 -4.0 (open issue 1) |
| image registry | 30 images; all pending_3d rows closed with result lines; check_registry.py exit 0 | 2026-10-07 | rows 26-29 Navionics series (11 files each), 30 = seabed source map |
| page build | nothing done here; shape.json and 3d\ are ready (see 6) | - | - |

## 2. Key decisions and why
1. Primary trace = Esri 2024-09-17 (bare rock at low tide, sharpest edge). Cross-checks sat2022, sat2012. Context sat2013, satshore, satblobs.
2. Canonical frame: +x = SOUTH (bearing 179.57 deg), +y = offshore = WEST (269.57 deg), origin = foot of the perpendicular from the both-mound centroid on the defence line (bearing 359.57). The tracer had used +x = north (mirror image); do not flip back. 3D z = 0 at MSL.
3. STATE modelled = as-built final layout (Phase 1 completed 8 March 2012, ref7). Superseded two-geotube design (A north truncated delta 180 x 65 m, 4.0 m high; B south) is a note only. The oval is a **shore-parallel breakwater** (crest +1.50 mODN), the boot is the **surf reef** (crest +0.50); the page must not call both surf reefs. No later damage/removal found (imagery 2012-2024, LiDAR 2022).
4. Outline versions (Lior 2026-10-06: laser survey or rock layer more accurate than a photo; priority survey > drawing > photo): lidar_2022 (default, 8,675 m2), design_1020 (6,989 m2), sat_2024 (5,743 m2). Default construction = LiDAR DSM above the exposed level (-2.3 mODN) + design toe berm and blanket slopes below it.
5. Datum: ODN is the working datum; model zero = MSL = +0.31 mODN (4-level mean, +-0.15); z_MSL = z_ODN - 0.31 = e_LAT - 2.75. LiDAR heights taken as ODN (not stated; supported by design crests and the flight sea surface).
6. Tide slider LAT -> MHWS (+2.56 mODN = +2.25 m MSL): HAT not found at a primary source (the only HAT-like figure, 5.9 m CD, is a predicted maximum). No Haifa preset.
7. Seabed (orchestrator 2026-10-06): -4.0 mODN under the north arm (derived), -3.6..-4.2 under the oval (printed), Fig 2 -3.0 contour outside the reef zone, LiDAR DTM beach, anchor -4.0 at y = 335 m, EMODnet gradient -1.1 % beyond. EMODnet absolute cells are GEBCO interpolation (not used).
8. Navionics (Garmin Marine Maps web viewer) read as a cross-check only: datum not stated, assumed LAT (best of 7 by RMS); it does not show the reef and is 0.6-1.1 m shallower than Fig 2 / EMODnet offshore -> not used for the model.
9. Rock density 1.7 t/m3 (1.6-1.8) for tonnage; NCE 42,000 t Type 4 for the whole Phase 1 is an upper bound.

## 3. Key numbers (units, datum, source id)
### 3.1 Plan (canonical frame, metres)
- Traced polygons (sat2024): N hook mound 42 vertices 3944.4 m2, length 144.9 m, mean width 27.6 m; S oval 37 vertices 1798.3 m2, 71.8 x 31.0 m; total 5742.7 m2; bbox 195.5 x 140.0 m; x -74.2..+121.3, y 257.0..397.0; centroid 330.5 m offshore (nearest edge 257.0, farthest 397.0); gap between mounds 57.2 m. [shape.json canonical; VERIFY check 3]
- Angles to the shoreline (359.57 deg): N mound axis 64.2 deg (PCA; design 60.9), tail curves toward E (bend 9.1 deg); S oval 0.18 deg (parallel). Shore-normal bearing 269.57.
- Design (drawing 1020 rev C1, 1:500): N armour foot 4956 m2, outer seabed edge 7883 m2; S armour foot 2033 m2, outer edge 3605 m2. Rings 0.76 / 2.0 / 2.0 / 3.0 m apart. Overlay of the design on the traced polygons: IoU 0.79 N, 0.86 S, centroids 0.3-4 m. Design ring 4 in the model reproduces shape.json's armour foot with IoU 0.9998.
- LiDAR exposed footprint 2022-03-19 (at about -2.3 mODN): N 5861 m2, S 2814 m2 (unioned outline 8,675 m2 incl. 1 m cell effects, simplified 0.4 m).
- Position: Esri +-5 m; OS grid -> WGS84 Helmert +-2-5 m; 2012 image is 5 m E of 2024 (registration, not movement). Offshore distance 300 m (Coflein) / 400 m (NCE).
- Setting-out points (BNG, drawing 1020): R1 260409.145 289284.522; R2 260501.860 289331.154; R3 260528.445 289332.669; R4 260527.416 289323.700; R5 260503.909 289322.361; R6 260451.697 289299.380; R7 260449.504 289284.783; R10 260424.002 289276.269; R14 260470.000 289162.000; R15 260470.000 289200.000 (oval crest ends 38 m apart).
### 3.2 Levels (mODN unless stated; design = drawings 1020-1023 rev C1)
- Crest N arm +0.50 (9 m wide); tail +1.00 (15 m transition from SOP R2); head edge +0.00 at R1/R10 rising to +0.50 over about 40 m; oval +1.50 (flat top 6 m). In MSL: +0.19 / +0.69 / -0.31 / +1.19.
- Layers (N3): Type 4 (5-8 t) +0.50 to -2.20 (2.70 m); Type 5 to -3.51 (1.31 m); Type 6 0.5 m blanket on the bed; Type 0 toe berm 1.35 m x 3.0 m top, 1:1.5, apron 2.0 m. Oval S2: Type 4 +1.50 to -1.20, Type 5 to -2.90 (1.7 m), Type 6 below (derived bed -3.4).
- LiDAR DSM in the crest strips (3D agent masks): N arm median +0.58, p90 +0.91; oval median +1.55, p90 +1.75; model max +1.81; LiDAR minus design above -2.0: +0.14 +- 0.28 m (verifier's N-arm median +0.69 used another mask).
- Slopes: design 1:3 arm/oval, 1:4 mid, 1:5 head, toe 1:1.5; as built (LiDAR) 1:4.0-1:5.3 and 8-10 m wider.
- Seabed under the rock (model): north foot -4.04 mean (-4.72..-2.51); oval -3.95 (-4.21..-3.62). Height above the bed: N arm about 4.5 m, oval about 5.5 m (+-0.5).
### 3.3 Tides (ref3 = West of Wales SMP2 Coastal Area C p.4C.3 Aberystwyth; ref4 = NTSLF)
- MHWS +2.56, MHWN +1.06, MLWN -0.64, MLWS -1.74 mODN (MHWS, MLWS also printed on the drawings); extreme still water 10/50/100 yr +3.76/+4.36/+4.73. LAT = -2.44 mODN (Barmouth, Fishguard; Aberystwyth not listed). MSL +0.31. HAT not found. LiDAR flight water level about -2.3 mODN (inferred); Esri 2024 photo waterline about -1.3 mODN (DSM at the traced edge).
### 3.4 3D model numbers (model.js, 1 m grid; volume above the modelled seabed, both mounds incl. berm and blanket)
| version | edge | footprint | volume (+-bed 0.4 m) | tonnes at 1.7 (1.6-1.8) | Type 4 layer |
|---|---|---|---|---|---|
| lidar_2022 (default) | -2.3 | 8,675 m2 (11,518 incl. toe) | 31,336 m3 (+-4,607) | 53,300 (50,100-56,400) | 21,557 m3 = 36,600 t |
| design_1020 | -2.15 | 6,989 m2 (11,491) | 30,091 m3 (+-4,596) | 51,200 (48,100-54,200) | 17,990 m3 = 30,600 t |
| sat_2024 | -1.3 | 5,743 m2 (8,979) | 26,400 m3 (+-3,592) | 44,900 (42,200-47,500) | 15,369 m3 = 26,100 t |
- All Type 4 volumes are below NCE's 42,000 t (whole Phase 1 incl. breakwaters/groynes). No reef-only quantity exists at a primary source.
- Seabed checks: model minus Fig 2 contour: -3.0 -0.01 m (control, n 24), -2.0 -0.14 (n 24), -4.0 **-0.89 m deeper** (sd 0.14, n 13); model at y 287: -3.61 (x -60), -2.91 (x +85). EMODnet cells 1.5 m shallower than the model at y 368-513.
- Navionics: chart zero implied by Fig 2 -4.0 = -3.58 +- 0.07 mODN, by EMODnet -3.07, by the model -4.73; RMS vs LAT 1.15 / 0.64 / 2.30 m (best of 7 datums); drying (0 m) line at y 385-430 m; contours 0.5-2.5 m seaward; reef not charted.
### 3.5 Other
- LiDAR: tile SN6089 DSM https://dmwproductionblob.blob.core.windows.net/lidar-zips/2020-22/dsm/wg_del_29_260289_20220319dsm.tif (DTM: same path with dtm; 1 m, EPSG:27700, origin 260000/290000 top-left, nodata -9999), flown 2022-03-19 03:15-03:20 UTC. Windows kept as npz in 3d\src (beach window E 260300-260900, N 289000-289500).
- Rock: 275,000 t whole Phase 1 (NCE ref6; Type 4 6-10 t 42,000 t); Coflein about 300,000 t. Chart datum / MSL offsets: SMP2 + NTSLF (above).

## 4. File map (07_scale/shapes/borth-coastal-defence-reef/ unless stated)
- HANDOFF.md - this file. shape.json (about 200 KB; open with python for a key: canonical, alt_outlines_m, outline_versions, default_outline, versions_info, angles, dimensions_check, gemini, references). VERIFY.md (25 KB; sections: checks 1-7, '3D inputs' tables, CHECKPOINT, outline-versions decision line). METHOD.md, sources.md.
- src/ - Esri tiles (+ .geo.json sidecars), drawings 1001/1020-1023 (png + vector pdf: open the PDF for exact numbers), HRPP576 pdf; borth_shoreline_z19.png (13.8 MB) and borth_blobs_z19.png (5 MB) are bulky.
- overlays/ - verify_*.png (verifier figures); polys_*_v1.json; scripts_verify/ (README inside).
- 3d/index.html - the viewer (stands alone; three.js from jsDelivr; no source images). Hash parameters: #version=lidar_2022|design_1020|sat_2024, #water=LAT|MLWS|MLWN|MSL|MHWN|MHWS|lidar_flight|photo_2024 or a number (m MSL), #ve=1..5, #view=oblique|plan|crest|beach|side, #tab=t1..t4, #info=1 (opens the version pop-up).
- 3d/model.js (660 kB, generated) - window.REEF_MODEL: frame, datum, levels, slider, seabed (5 m grid, z MSL), versions[] (id, name, date, source_ids, method, level, area, volume, outline_m, 1 m grid as base64 int16 cm), default_version, versions_info, roles, crest_labels, provenance (25 rows), confidence_3d, validation, navionics. docs.js (50 kB) - METHODS_3D.md + SOURCES_3D.md for the viewer's Methods tab.
- 3d/build_3d.py - regenerates model.js and docs.js (`python build_3d.py`; `--shape` also writes outline_versions / default_outline / versions_info into shape.json). Needs 3d\b3d_lib.py (frame, seabed nodes, RBF), 3d\b3d_reef.py (surfaces, volumes), 3d\prep_sources.py (LiDAR windows; needs the tile again only if src\*.npz are lost), 3d\src\ (npz, fig2_contours_canonical.json, design1020_*.json, navionics_reading.json, build_metrics.json).
- 3d/make_annotations.py (A1-A8), 3d/nav_read.py (`python nav_read.py`, `python nav_read.py annotate`: Navionics reading and A9, A10), 3d/register_images.py (registry; idempotent), 3d/src/navionics/ (44 screenshots, capture_navionics.py, probe_geometry.py, nav_geometry.json, nav_lines.json, nav_datum_test.json). Rebuild order after a change: make_annotations.py -> nav_read.py annotate -> build_3d.py [--shape] -> register_images.py.
- 3d/annotated/ - A1 Fig 2 contours read, A2 drawing 1020 rings + SOP, A3-A5 drawings 1021-1023 callouts, A6 LiDAR crest check, A7 beach vs Fig 2, A8 seabed source zones, A9 Navionics SonarChart z17 (datum test), A10 Navionics nautical z18 with reef outline. 3d/preview_plan.png, preview_oblique.png, preview_methods_panel.png - viewer screenshots (regenerate after changes; headless Chrome recipe in SOURCES_3D.md STEP 1: python http.server on a random port, fresh --user-data-dir, --headless=new --use-angle=swiftshader --virtual-time-budget=15000; the first load sometimes fails (CDN race): retry).
- 3d/METHODS_3D.md (8 sections, the reviewer note), SOURCES_3D.md (run log), REQUESTS_FOR_LIOR.md (7 rows; also indexed in the project-root REQUESTS_FOR_LIOR.md, item D6 and section 4).
- 03_images/reefs/borth-coastal-defence-reef/images.json + IMAGES.md (30 rows); 07_scale/bathymetry/emodnet/REPORT.md section 9.2 (EMODnet cells); 02_research/reefs/borth-coastal-defence-reef.* (card); Gemini folder: do not use (wrong, VERIFY check 6).

## 5. Open issues, discrepancies, pending checks
1. **Seabed seaward of the reef (y > 335 m) is 0.9 m deeper than the HRPP576 Fig 2 -4.0 contour** (Fig 2 has -4.0 at y 410-450; model -4.7 at y 400, -5.1 at 440); Navionics (chart zero -3.58) and EMODnet (-3.07) are shallower than the model too. Cause: only the -3.0 contour and the assumed anchor -4.0 at y = 335 m (+ EMODnet gradient) were used. Volumes under the rock are unaffected (design nodes pin the bed). Proposed fix (needs Lior/orchestrator, root REQUESTS D6): add the Fig 2 -4.0 contour (outside the reef zone) as nodes and start the EMODnet gradient from it; change `seabed_nodes` and `seabed_grid` in b3d_lib.py (nodes beyond ANCHOR_Y are currently ignored), then rebuild. Not changed because the orchestrator fixed the anchor on 2026-10-06.
2. Aberystwyth chart-datum offset (Z0) and HAT not tabulated at a primary source; MSL is a 4-level mean (+0.31 +-0.15). Request row 6 (Admiralty / EasyTide).
3. LiDAR vertical datum not stated (ODN assumed); tide state at the flight (-2.3 mODN) inferred, not predicted.
4. Bed under the rock is a design level (-4.0 derived; oval printed -3.6..-4.2, derived -3.4); the tail bed (-3.0..-3.4) is assumed; ground lines in the sections are schematic ("BED LEVELS VARY").
5. As-built flanks are flatter and 8-10 m wider than the design (LiDAR); flanks below -2.3 mODN are design, not measured (need a low-tide imagery / multibeam).
6. Oval length: drawing 1023 S1-S1 dimensions 23,000 + 23,000 mm between SOP R15 and R14 (46 m); the SOP table of drawing 1020 gives 38 m (model uses 38). Worth about 2 % of the oval volume.
7. Navionics shows no reef and is inconsistent with survey contours offshore; the Navionics app (not the web viewer) may show an obstruction symbol (request rows 1-3).
8. Position of design and LiDAR vs satellite limited by the OSGB36->WGS84 Helmert (+-2-5 m); OSTN15 not used. No post-2022 survey or damage record found (Wales Coastal Monitoring Centre map not readable by agents; CoastSnap Borth 2024-25 photos not checked).
9. Reuse rights: every saved image (Navionics screenshots, drawings, Fig 2, annotated copies) is a private research copy; clear rights before any public release.

## 6. Next steps (in order)
1. Page builder: use shape.json (default_outline lidar_2022; show "drawn = laser-survey edge, 8,675 m2" and let the user toggle the other two with the (i) text from versions_info); link or embed 3d\index.html (hash parameters above); the page must label the oval a breakwater; show confidence_3d (MEDIUM) and its one-line reason; tell the user that the Gemini footprint is wrong (VERIFY check 6).
2. Decide root REQUESTS D6 (offshore seabed fix); if yes, apply item 1 of section 5 and rerun build_3d.py --shape, nav_read.py annotate, make_annotations.py, register_images.py; re-render the previews; update METHODS_3D.md 3.3, 4.4, 7 and the viewer's "Seabed in this model" note.
3. If Lior supplies the Navionics-app and Google Earth readings (3d\REQUESTS_FOR_LIOR.md): add them as nodes/checks (a reading at the reef toe would pin the bed to +-0.2 m); update confidence_3d (could become HIGH only if the bed under the rock is measured).
4. Confirm Aberystwyth Z0 / HAT and extend the slider to HAT if found (levels list in build_3d.py TIDES_ODN).
5. Optional: Phase 2 structures north of the reef (ref9) are not modelled (not part of the reef).

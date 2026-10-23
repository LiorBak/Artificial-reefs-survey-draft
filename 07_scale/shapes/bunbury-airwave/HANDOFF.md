# HANDOFF - bunbury-airwave (shape trace 2026-10-05; verify 2026-10-04/05; 3D model 2026-10-05; handoff written 2026-10-10 from the folder's own files)

Read this first. Open other files only for one fact. Source ids = shape.json sources/references (img1, img4, img5; R1-R24 are the reef card's references, `02_research/reefs/bunbury-airwave.json`); 3D ids S_* / A1-A13 / V1-V11 / L1-L11 are those of `3d/METHODS_3D.md`. Registry: `03_images/reefs/bunbury-airwave/images.json` (about 21 ids).

**Verdict recorded on the card: FAILED, despite the developer's claim.** The structure is a 12 m rubber bladder that tore along a glued seam during installation in December 2019 and was removed within about three days. Waveco's About page (R21) says "In 2018 ... successfully created peeling waves ... It wasn't a failure"; the year is contradicted by every dated 2019 report, and no independent report, photo or video of surfable waves was found. The page must say "December 2019 installation attempt (torn)", not "2018 deployment" or "successful". This is not a rock reef and was never a working reef.

## 1. Status per stage
| stage | state | date | confidence / reason |
|---|---|---|---|
| trace | done: img1 (29 vertices, primary), img4 (23, cross-check, oblique ~48 deg), img5 (24, design graphic, not the as-built) | 2026-10-05 | circle clearly visible on a real near-nadir drone photo; size taken from text (12 m), no scale bar/EXIF/geo-reference |
| verify (shape.json status "verified", verified_on 2026-10-04) | done: checks 1-7 in VERIFY.md plus Check 3b (canonical block, geom.py make-canonical bug) | 2026-10-05 | MEDIUM (not high): shape is an image result, every dimension is text; 0.6-0.9 % agreement with 12 m is by construction |
| location | NOT traced: approx centre -33.3276, 115.6284 (+-100 m) from text; the card's old lat/lon (-33.31, 115.64) is ~2 km off | 2026-10-05 | no georeferenced image of the bladder exists (it existed about one week) |
| 3D model | BUILT: `3d/model.js` (60 kB), `index.html`, `docs.js`, METHODS_3D.md (9 sections), SOURCES_3D.md, REQUESTS_FOR_LIOR.md, previews, annotated/ (8 figures) | 2026-10-05 (third run, step 6) | MEDIUM: seabed + tides sourced and cross-checked; reef geometry text-based; crest depth below MLLW 0.69 +- 0.66 m (Monte Carlo) |
| developer-account check | done: five claims (a)-(e) of the Waveco About page compared with independent record; nothing in shape.json or model changed | 2026-10-05 | HIGH that "2018" is wrong; wave claim unsupported |
| image registry | registered (backfill 2026-10-06), about 21 ids; `3d/SOURCES_3D.md` end lists the ids | 2026-10-06 | not re-checked in this handoff run (run `07_scale/tools` registry check if needed) |
| page build | nothing done here; shape.json and 3d/ are ready | - | - |

## 2. Key decisions and why
1. Primary trace = img1, RWR "Airwave from above" drone photo (header of RWR tear post, file dated 2019-12-17). Cross-check img4 (frame of ABC video 11804314, 2019-12-16). img5 (design graphic, "Image: Unofficial Networks") traced only as a concept circle. img2 (3D render) not traced.
2. State drawn/modelled = the single 2019 prototype as installed and torn (base footprint). Only one full-size Airwave has ever been installed; the redesign (stronger welded compound, "more classic dome") was only tank-tested. Removal, redesign and the 2025 granite proposal are notes, not modelled.
3. Scale = known dimension: major axis of the fitted ellipse = 12.0 m (25.59 px/m on img1), oblique correction by ellipse rectification (tilt 26.5 deg). Label "known dimension (text)", never "measured".
4. The paler upper-left crescent is kept in the outline (also seen on the left of img4; Bottegal describes an asymmetric "skateboard ramp" bladder). Without it the disc would be about 8 % narrower (11 m) - main residual ambiguity.
5. Frame: metres, x alongshore toward bearing 12.32 deg true, y seaward toward 282.32 deg true (perpendicular to the fitted 2009 0 m AHD contour), z = 0 at MSL. Shape.json's own canonical frame has an arbitrary orientation (circle); the 3D frame is the shoreline-based one.
6. Datum: AHD working datum; MSL = +0.1 m AHD (GHD 2021 Table 1, Port of Bunbury), z_MSL = z_AHD - 0.1. LAT is the Australian chart datum (-0.6 m AHD; DoT index -0.57). Local tides only: HAT +0.5, MHHW +0.1, MHLW -0.1, MLLW -0.3, LAT -0.7 m MSL (range 1.2 m, diurnal). No Haifa preset.
7. Seabed = WA DoT 2009 airborne lidar (10 m BAG grid, resampled to 5 m in the model frame), not Navionics. Navionics SonarChart (Garmin web viewer, LAT best of 4 datum candidates) is only an independent check; it does not show the structure.
8. Reef surface = symmetric spherical cap on the sloping bed (A5), default H = 2.0 m (range 1.6-2.0 m, ABC/RWR 2 m vs Tracks 1.6 m, both pre-install design figures). Optional ramp-asymmetry slider (0-0.6); no source says which flank was steep, so default is symmetric. No fill, valves, anchors or tear drawn.
9. Default centre y = 37.5 m offshore (midpoint of text range 30-50 m; viewer presets 30, 37.5, 45, 49.1 m). It is unspecified whether the text means centre or near edge.
10. Fill mass 140 t (Tracks 2021, Bunbury Mail 2022) vs 150 t (Waveco): not used in geometry; V8 shows both are physically credible for a mostly sand-filled cap.

## 3. Key numbers (units, datum, source id)
### 3.1 Plan (shape.json)
- Canonical polygon: area 112.06 m2 (circle of D 12 m = 113.1; -0.9 %, by construction), bbox 12.069 x 12.092 m, max dim 12.181 m. Pixel areas: img1 65,673 px2 (bbox 306 x 281), img4 12,813, img5 39,097.
- Ellipse fit img1 (own Fitzgibbon refit by the verifier): centre (446.4, 334.9) px, semi-axes 153.6 / 137.4 px, RMS radial deviation 1.27 %; img4 78.8 / 52.6 px, RMS 2.95 %.
- Edge test: mean |offset| 3.3 px (0.13 m), 24 of 29 vertices within 5 px; outliers 5-16 px (0.2-0.6 m) on a soft fringe; half-max edge would give diameter -2 to -3 %.
- Stated uncertainty 15 % (shape.json); scale +-7 % (L11). Angles to shoreline undefined (circle).
- Offshore distance (text only): RWR 30-45 m; Tracks 2019 "approximately 45 metres off the low tide mark, just to the south of Bunbury surf club"; SurferToday 50 m; img5 label "30m" (not to scale).
- Site point origin of the 3D frame: -33.32767, 115.62880 (2009 0 m AHD contour); contour fit east = a + b north, a = 38.7 m, b = 0.2046, rms 8.4 m; MGA94 zone 50 grid convergence gamma 0.754 deg.
### 3.2 Reef dimensions (text, not measured)
- Base D 12 m (ABC, RWR, Tracks, Bunbury Mail, Tradie). Height 2 m (ABC, RWR, SurferToday) vs 1.6 m (Tracks 2019, Bunbury Mail 2022). Crest "about 1 m under the surface at low tide" (RWR).
- Cap volume: H = 2.0 m: 117.3 m3, R_s 10.00 m, rim angle 36.9 deg; H = 1.6 m: 92.6 m3, R_s 12.05 m, 29.9 deg (E10-E14).
- Sand: 140-150 t = 70-94 m3 settled (1.6-2.0 t/m3), 60-80 % of the 2.0 m cap or 76-101 % of the 1.6 m cap (V8).
- Material: Hypalon (synthetic) rubber, glued seams. Cost: City of Bunbury A$75,000 (approved June 2019); total ~US$350-400k (sources disagree).
### 3.3 Seabed (WA DoT Lidar2009TRBS, BAG BU2009TRBS_Lidar.bag, 67,442,256 bytes, vertical AHD; datum per DoT index)
- Median profile (m AHD, y offshore from 0 m AHD contour): y 20 m -1.10; 30 -2.08; 37.5 -2.58; 40 -2.69; 45 -2.97; 50 -3.20; 60 -3.62; 100 -5.11; 150 -7.12; 200 -8.40. Mean slope y = 30-100 m: 0.0409 (1:24.5).
- Model grid 5 m, x -150..+150, y -40..+200 (61 x 49 nodes); 286 of 2989 nodes (9.6 %) in the surf zone (y about -15..35) gap-filled (E9).
- Lidar uncertainty 0.47-0.48 m (BAG layer, read as 1 sigma, A10). Survey is 10 years older than the install (sigma_change 0.30 m assumed).
### 3.4 Tides (GHD 2021 Table 1, Port of Bunbury; DoT index check LAT -0.57 vs -0.6)
- m AHD: HAT 0.6, MHHW 0.2, MLHW 0.1, MSL 0.1, MHLW 0.0, MLLW -0.2, LAT -0.6. Above chart datum (LAT): 1.3 / 0.9 / 0.7 / 0.7 / 0.6 / 0.5 / 0.1. Range HAT-LAT 1.2 m.
- Crest depth below MLLW / LAT at default y = 37.5 m: H = 1.6 m 0.78 / 0.38 m; H = 2.0 m 0.38 / -0.02 m (the cap just reaches LAT). At y = 49 m: 1.36 / 0.96 (H 1.6), 0.96 / 0.56 (H 2.0). Seabed under reef at y = 37.5 m: -2.58 m AHD.
- Uncertainty chain: sigma_zb 0.61 m, sigma_zc 0.62 m, sigma_dc 0.63 m (E15-E17); Monte Carlo 0.69 m, sd 0.66 m, 5-95 % -0.41..1.78 m.
### 3.5 Validation (V1-V11, METHODS_3D section 4)
- V1 text-implied seabed -3.20 (H 2.0) / -2.80 (H 1.6) m AHD vs lidar -2.58 at default y (0.62 m difference; lidar reaches -3.20 at y = 50 m). V2 Tracks 45 m + RWR 1 m: 0.96 m crest depth (H 2.0), consistent. V4 lidar vs Navionics RMS 0.32 m over 111 lines (mean diff +0.25 m). V5 datum RMS: LAT 0.32, MLLW 0.67, AHD 0.87, MSL 0.96. V9 orientation tilt +2.4 deg.
### 3.6 Chronology (R1, R5-R8, R15, R22)
- Install began week of 9 Dec 2019 (slurry pump on beach 7 Dec per forum observer); tear spotted by a diver Fri 13 Dec 2019 when about 90 % complete and not fully anchored; reported Mon 16 Dec (ABC); removed in about 5 h to 3 days (reports differ). Cause per Bottegal: unexpected swell/undertow flexed the bladder at a glued seam (later: 140 t sand pumped too heavily into one quadrant, Tracks 2021).
- Only quantified wave: Bottegal later (Bunbury Mail 2022) said a wave "peeled nearly all the way to the beach", 0.75 m; self-reported, not independently documented. Planned UWA 12-month study never started.

## 4. File map (07_scale/shapes/bunbury-airwave/ unless stated)
- `shape.json` (924 lines): traced polygons (pixel + canonical), sources, references, verification array (7 entries), dimensions_check, gemini record, location_note. Open for any number.
- `METHOD.md` (112 lines): trace steps 0-4, verification corrections, "Developer's account" section (Waveco table a-e). `VERIFY.md` (90 lines): checks 1-7, 3b, fixes list. `sources.md`: provenance rows for img1-img5 and satellite tiles.
- `src/`: private research copies img1, img2, img4, img5, two Esri tiles with .geo.json. `overlays/`: img1/img4/img5 trace overlays. Reuse rights NOT cleared; repo stays private.
- `3d/METHODS_3D.md` (307 lines, GENERATED by `build_3d.py` from `3d/METHODS_3D.template.md`; edit the template, not the output), `3d/SOURCES_3D.md` (151 lines, steps 1-6, developer account, build state), `3d/REQUESTS_FOR_LIOR.md` (44 lines, generated by `make_requests.py`).
- `3d/model.js`, `index.html`, `docs.js`: viewer (three.js 0.170.0 from jsDelivr). `3d/computed.json`, `data/build_summary.json`: build outputs. `data/lidar_clip_model_frame.csv`, `lidar_derived.json`, `nav_transects.json`: seabed inputs.
- Scripts: `build_3d.py` (model, docs, METHODS), `build_3d_lidar.py` (stage 1, needs the 67 MB BAG, not stored), `nav_annotate.py`, `nav_figures.py`, `src/navionics/` (screenshots + `capture_navionics.py`).
- `3d/annotated/` (8 figures: N1-N4 Navionics, img1_trace_axes_scale, lidar_cells_at_reef, lidar_contours_on_satellite, seabed_profile_with_tides). `3d/preview_*.png`: viewer previews. Bulky or not worth opening: model.js, index.html, previews.
- Reef card: `02_research/reefs/bunbury-airwave.json|.md` (verdict, outcome, developer_account, verdict_reason, R1-R24). Registry: `03_images/reefs/bunbury-airwave/`.

## 5. Open issues, discrepancies, pending checks
1. Reef location not traced (+-100 m alongshore, +-10 m offshore); card lat/lon (-33.31, 115.64) is ~2 km off. Needs Google Earth Pro historical imagery of Dec 2019 (probably none exists). REQUESTS A1-A4.
2. As-installed height (1.6 vs 2.0 m), profile and which flank was steep unknown (L1). Needs Waveco/City of Bunbury installation record (REQUESTS C1-C3).
3. Seabed is 2009; Navionics app readings at points B1-B11 would test it (L3, L4). Lidar uncertainty type (1-sigma vs 95 %) and BAG datum tag unresolved (L5).
4. "Low tide" in the 1 m crest text is MLLW or LAT (0.4 m, L6); tide planes are port gauge, 3 km away (L7). Surf-zone strip is gap-filled (L8).
5. Total cost disagrees (US$350k vs 400k). Offshore distance text range 30-50 m, unspecified centre vs edge.
6. Tradie Magazine 2019 seen from search text only (page 403); some R6/R20 sources Cloudflare-blocked. Gemini footprint (formula 24-gon, 113 m2) and eight further Gemini claims recorded as contradicted/unsupported; nothing from Gemini used.
7. The waves claim is unverified: if a source with video of the 2019 wave turns up, the "failed" wording on the card should be re-checked (the verdict itself rests on the tear and removal, which are well documented).
8. This handoff was assembled from the folder's files without re-running the registry check or the build; registry count (about 21 ids) is from a quick count.

## 6. Next steps (in order)
1. Page builder: use shape.json default outline (circle D 12 m, text-calibrated) and the 3d/ viewer; caption "December 2019 installation attempt (torn), 12 m bladder, sand-slurry filled"; show the developer-account table (METHOD.md) on the page.
2. If Lior supplies Google Earth / Navionics / Waveco data (REQUESTS A-C), update shape.json location_note, rerun `python build_3d.py`, update the V and L tables in the template.
3. Check the registry (`03_images/reefs/bunbury-airwave/`) with the project tool before the page build.
4. Optionally re-fetch Tradie 2019 and Swellnet pages for primary quotes.

## 7. CHECKPOINT 2026-10-10
Bunbury is FINISHED at MEDIUM confidence and consistent; this HANDOFF was written by the housekeeping agent. Nothing was rebuilt or edited besides this file. A fresh agent can proceed to the page build or to the REQUESTS data without reading the sources above.

## 8. UPDATE 2026-10-10 - new source R25 (personal communication)
Lior Bakalo, Zoom interview with Troy (founder of Airwave), 8 Oct 2026, notes as reported by Lior (no URL, unrecorded, developer = interested party). Key points: final design filled with SAND instead of air (air did not respond well with the waves); seam opened a couple of days after installation; worked "amazingly / perfect waves" until then (unverified founder claim); next version is concrete. Recorded on the card as R25 plus a `sources_disagree` list (fill, failure timing, waves, future). Verdict stays FAILED; verdict text now notes the founder's wave claim and the lack of independent confirmation. Caption "sand-slurry filled" in section 6 is consistent with the founder's sand statement; the card's older "air/sand" wording is kept and flagged. Shape and 3D model untouched.

## 9. SOURCE AUDIT 2026-10-10
`SOURCE_AUDIT_2026-10-10.md` done (29 rows: 22 ok, 6 fixed, 1 card/model location mismatch). METHODS_3D now has 2.2 fill disagreement (ABC air / Tracks sand+air / Troy sand not air; unresolved), 2.3 how each source was used, 3.8 A14, 3.9 decisions DEC1-DEC12, L12, Bakalo (2026) reference; S_Troy added to the viewer sources. Rebuilt for docs only: model.js changed in text fields only (built date, verdict_reason, +1 source, fill provenance text). Page text edit proposals for main are in the audit file section 6. Citation authors for ABC/Tracks 2019 not confirmed (REQUESTS E5b).

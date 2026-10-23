# HANDOFF - prattes-reef-el-segundo (shape verified 2026-10-05/stamp 2026-10-04; 3D model built 2026-10-05; RE-VERIFIED 2026-10-10; for the page builder and any later agent)

Read this first. Open other files only for one fact (section/page given). Source ids: shape.json sources (img1-img7) and references (R1-R28); 3D source ids S1-S10, P1 in 3d/METHODS_3D.md section 2 (S10 = Borrero & Nelsen 2003 PDF = shape.json img7 / R28). Registry ids = 03_images/reefs/prattes-reef-el-segundo/images.json (38 rows, ids -img-01 .. -img-38).
Windows paths of old docs map to <repo root>/X/Y. Short paths below are relative to 07_scale/shapes/prattes-reef-el-segundo/.
Short version: Pratte's Reef (El Segundo, California; 110 sand-filled geotextile bags, installed 22 Sept 2000, +90 bags April 2001, removed 2008-2010). Outline = Skelly Engineering DESIGN layout of Phase I (435.2 m2, 58.0 x 28.6 m), confidence MEDIUM. No as-built plan exists. 3D model = Phase I as installed (crest from the 2003 paper), confidence LOW. The re-verification of 2026-10-10 confirmed everything in the pending block; nothing in the polygons or the model's numbers changed.

## 1. Status per stage
| stage | state | date | confidence / reason |
|---|---|---|---|
| trace | done: img1 (RWR copy of the Skelly drawing, 76 vertices, scale bar), img5 (same drawing, 72 vertices), img6 (1996 concept, orientation only) | 2026-09/10 | outline follows the first solid stroke of both arms, 5 x 5 spine and tips |
| verify (shape.json status "verified", verified_on 2026-10-04, reverified_on 2026-10-10) | done: checks 1-7 + re-verification checks 8-12 in VERIFY.md | 2026-10-05; 2026-10-10 | MEDIUM: scaled design drawing of the designer of record, bar fits to 0.5 px, bag pitch within 6% of 7 x 10 ft; not HIGH because it is a design drawing (bags moved, sank, were buried), Phase II absent, position unfixable |
| re-verification of the `pending_reverification` block | done, block removed, replaced by shape.json `reverification` record | 2026-10-10 | all items confirmed (section 2 of VERIFY.md summary table); no polygon / canonical / design_version change |
| outline versions | one outline only (Phase I design layout, solid-outline bags). 1996 concept (6 vertices, img6) is orientation/arm-length reference only | 2026-10-05 | - |
| 3D model | BUILT 3d/model.js, index.html (viewer, three.js 0.170 from jsdelivr), docs.js, METHODS_3D.md (9 sections), SOURCES_3D.md, REQUESTS_FOR_LIOR.md, previews, annotated A1-A17. Re-run of build_3d.py 2026-10-10 changed only stamps (md5, date); data identical | 2026-10-05; 2026-10-10 | LOW (METHODS_3D section 6): crest only at the apex face, thickness assumed, volume gap V8 unresolved, position inferred |
| image registry | 38 images; check_registry.py reports no Pratte's error (rows 33-36 are another agent's "papers intake" rows; mine are 37-38) | 2026-10-10 | 3 rows pending_3d (img-06 building photo, img-29 Fig. 2 aerial, img-35 intake row) |
| page build | not done here; main updates models3d_curated.json / models3d_caveats.json (section 6) | - | - |

## 2. Key decisions and why
1. State drawn = Phase I DESIGN layout, fall 2000, 110 solid-outline bags, 30 dashed "optional" bags excluded (they were wrongly inside the first trace: -49 m2). Why: the only plan view found (printed BAG COUNT 110); reprinted as Fig. 4 "The design layout of Pratte's Reef" of Borrero & Nelsen 2003, which has no as-built plan. The page must say "design layout, fall 2000, not as built, not the 200-bag reef".
2. Primary outline source img1 (RWR copy, bar 1.5712 px/ft, 5.1549 px/m); img5 is a cross-check but is the SAME raster as Fig. 4 of the paper (verified 2026-10-10), so it is independent of img1 only, not of Fig. 4.
3. Canonical frame: origin on the assumed shoreline point on the V axis 91.44 m (100 yd, text) inshore of the polygon centroid; +x alongshore toward 155 deg, +y offshore toward 245 deg. Orientation (apex offshore WSW) from img6's A-A section line and contours, img4 shoreline (155.5 deg own fit), and the paper (apex pointing offshore, p.2; Fig. 20 shows the apex toward the swell).
4. geo = null: three published coordinates disagree by 313 m and none fits the primary sources. A position HINT 33.92058 N, -118.43335 E (+-100 m, maybe +-150 m, see 5) comes from the Fig. 9 survey window of the paper; it is a page-marker hint, not a polygon.
5. 3D state = Phase I as installed. Crest scenario B (default) = paper p.2 "approximately - 6 ft MLLW" at the outermost point (apex): -2.678 m MSL; top follows the DEM seabed at constant thickness 1.349 m. Scenario A = drawing label "TOP OF BAG MIN DEPTH -6' MSL" = -1.829 m MSL, level crest. Both selectable. B chosen because it is the only as-built statement (and its datum MLLW is printed in the paper). Re-verification found no evidence to overturn it and none to prove it (the label ambiguity is real, 0.849 m).
6. Seabed = NOAA 1/3 arc-second DEM (primary), checked against Navionics SonarChart labels and the beds of the paper's Fig. 5; local tides only (NOAA Santa Monica 9410840, cross-checked with Los Angeles 9410660); no Haifa preset.
7. Phase II (April 2001), erosion 2001-02 and removal 2008/2010 are NOT modelled; they appear as notes (METHODS_3D 2.1, 3.11).

## 3. Key numbers (units, datum, source id)
### 3.1 Plan (canonical frame, metres)
- Outline: 435.2 m2 (img1 435.2, img5 437.5), bbox 58.0 x 28.6 m (alongshore x cross-shore), max dimension 58.0 m, 76 vertices, polygon y range 74.65-103.28 m, centroid (0.005, 91.44). Recomputed with shapely 2026-10-10: 435.17 m2, 58.03 x 28.63 m. Source: shape.json canonical, img1 bar.
- Arms 44.7 / 44.4 deg to the V axis (printed 45), 89.1 deg between the arms; spine block 5 x 5 bags = 10.6 m (cross-shore) x 14.1 m (alongshore); arm length from the virtual apex about 41 / 39.7 m. 1996 concept: two 150 ft (45.7 m) wings, not to scale (img6).
- Bag: 4 x 7 x 10 ft, max 280 ft3 = 7.9 m3, filled 80-90 %, about 14 t (S10 p.2; ICCE 2010 Fig. 1 gives 3 m x 1.2 m high). Drawing pitch 6.8-6.9 x 9.4-9.6 ft, i.e. 1-6 % below nominal.
### 3.2 Size cross-checks (new 2026-10-10)
- S10 p.14 "Pratte's only extends 30" (no unit; metres by context) vs 28.6 m: -4.7 %, rounding.
- S10 Fig. 20 (p.14, own 0-50 m bar = 70 px, 1.40 px/m): the V is 82 px tip to tip = 58.5 m and 41 px cross-shore = 29.0 m, i.e. +0.9 % / +1.4 % against our outline. Independent of the Skelly bar. Not diagnostic of the phase: the Phase II centreline bump (Fig. 5) is 29.4 m wide too.
- Fig. 4 bar: 27/27/54/53 px for 15/15/30/30 ft = 1.789 px/ft (= img5's 1.7889).
### 3.3 Levels and tides (m relative to MSL, NOAA 9410840 epoch 1983-2001; recomputed from src json)
- MSL - MLLW = 1.594 - 0.745 = 0.849 m (Los Angeles 9410660: 2.028 - 1.167 = 0.861 m); MSL - NAVD88 = 0.792 m. HAT +1.382, MHHW +0.804, MHW +0.579, MSL 0, MLW -0.566, MLLW -0.849, LAT -1.469 (tidal range MHHW-MLLW 1.653 m).
- Crest B apex -2.678 m MSL = 1.83 m below MLLW = 1.21 m below LAT; tips -1.784 m. Crest A -1.829 m MSL (0.36 m below LAT). Phase II "within 3 ft of MLLW" = -1.763 m MSL (not modelled).
### 3.4 3D model numbers (model.js; computed.json is the machine-readable copy)
- Seabed at the reef centre -3.67 m MSL (apex -4.03, tips -3.13), slope 1:32.0; six estimates span -2.92 to -5.00 m (SD 0.83).
- Height state B 1.35 m (1.12 courses); state A 2.2 m at the apex, 1.3 m at the tips. Side slope 1 H : 1 V (0.5-2.5).
- Volume B 443 m3 (316-514 for slope 2.0-0.5), A 550 m3 (344-672); with the Navionics bed B = 422 m3. 110 bags = 869 m3 nominal, 695-782 m3 at 80-90 % fill: gap -252 to -339 m3 (V8, unresolved). 110 bags x 6.39 m2 = 703 m2 of footprint vs the 435.2 m2 outline (arm bags overlap in the drawing, 3.4 m2 per bag).
- Final reef: 200 bags, about 1,600 m3 nominal (S10 p.16), 1,264-1,422 m3 at 80-90 % fill.
### 3.5 Other
- Chronology: concept 1996-98 (CCC E-98-15, hearing 13 Oct 1998); Phase I 22 Sept 2000 (barge crane, Port of Los Angeles fill); Phase II 23-24 April 2001 (+90 bags, +80 % volume, crest widened and shallower, placed on top of Phase I); crest eroded about 1.45 m May 2001 to Sept 2002 (Fig. 8); removal 30 Sept-17 Oct 2008 and fall 2010.
- Position text vs figure (new 2026-10-10): S10 p.1 "about 200 m south of the 1-mile outfall, within 500 m of outfall and Grand Street jetty"; Fig. 2 (6.25 m/px, range lines 550 m apart) reads about 340 m and 670 m. Reef is NORTH of the Grand Street jetty in both (Fig. 2 label), against the three published coordinates, all south of it.

## 4. File map (07_scale/shapes/prattes-reef-el-segundo/ unless stated)
| file | holds / when to open |
|---|---|
| shape.json | status verified, `verification` array (12 items), `reverification` record, dimensions_check, confidence factors, geo_note, canonical polygon (open only via a script) |
| VERIFY.md | checks 1-7 (2026-10-05) + last section RE-VERIFICATION 2026-10-10 (table of 5 items, methods); open the last section only |
| METHOD.md | trace steps 1-6 (superseded steps marked); line 83 says the pending note was resolved |
| sources.md | source table img1-img7 + consulted-not-saved + rows added 2026-10-10 (Fig. 4, Fig. 20) |
| src/ | img1-img6 (+ geo.json), borrero_nelsen_2003 PDF (img7), bn2003_fig4_design_layout_raster.png, bn2003_fig20_pratte_vs_narrowneck_raster.png |
| overlays/ | img1/img5/img6 final overlays, correction overlay, `_pre_verification/`, bn2003_fig4_with_img5_outline_2026-10-10.png, bn2003_fig20_pratte_scale_check_2026-10-10.png |
| 3d/METHODS_3D.md (generated; edit METHODS_3D.template.md), SOURCES_3D.md, model.js (43 kB), docs.js, index.html, computed.json | the model, its methods and a numbers file; open computed.json by key, METHODS_3D by section (3.2 datums, 3.6 crest, 4 validation V1-V17, 7 limitations) |
| 3d/build_3d.py, reef3d_lib.py, bn_digitise.py, bn_annotate.py, make_annotations.py, nav_annotate.py | rebuild: `cd 3d; python build_3d.py` (0.7 s; add --annotations to redraw annotated/*.png) |
| 3d/annotated/A1-A17 | sources with readings marked (A12-A14, A17 = the 2003 paper); registry rows 20-32 |
| 3d/src/ | NOAA DEM exports, datum json, Navionics captures, digitised paper figures, CCC and ICCE PDFs (bulky, do not open) |
| 3d/REQUESTS_FOR_LIOR.md | Google Earth A1-A3, Navionics B1-B7, e-mail A5/C1 (also in the root list: E1, E2) |
| archive/pre_reverify_2026-10-10/ | shape.json, VERIFY.md, METHOD.md, sources.md, images.json, IMAGES.md, 3d/{model.js,docs.js,computed.json,METHODS_3D.md,SOURCES_3D.md} as they were before the re-verification |
| 03_images/reefs/prattes-reef-el-segundo/ | registry images.json + IMAGES.md (38 rows), five photos and the removal-era pictures |

## 5. Open issues, discrepancies, pending checks
Judgement calls NOT changed (for Lior or main; one line each):
- J1 Crest datum: the same number (6 ft) is "-6' MSL" on the drawing (at the arm tips, "min depth") and "approximately - 6 ft MLLW" in the paper (outermost point = apex, deepest). They differ by exactly 0.849 m. The model default is B (paper, MLLW). Only the authors / dive records can settle it (root REQUESTS E1, 3d C1).
- **J2 DECIDED 2026-10-10 (by us): +-150 m position uncertainty. APPLIED in the 2026-10-10 source audit (build_3d.py sig_x=150, METHODS template, shape.json geo_note, viewer note); the hint and model did not move. J1 DECIDED 2026-10-10 (Lior): keep the paper's MLLW crest datum (METHODS_3D decision D6).**
- J2 (original text) Position hint uncertainty: model and notes say +-100 m; the paper's text (200 m / within 500 m) and Fig. 2 (about 340 m / 670 m) disagree by 140-170 m, so +-150 m may be more honest. Model keeps sigma_x = 100 m (depth effect small, seabed sd 0.14 m alongshore). geo stays null.
- J3 Volume gap V8/V9 (model B 443 m3 vs 695-782 m3 of bags): unresolved, not an uncertainty effect; model A is closer. Possible causes: arm bags overlapped in the drawing, second course elsewhere, less filling. Needs as-built sections.
- J4 Wording: the paper calls the V "obtuse"; the drawing's arms are 89.1 deg apart. The drawing is what was traced; the as-built angle is unknown.
- J5 Paper text says Figure 19 for the Narrowneck comparison; the caption (p.14) is Figure 20.
- J6 Paper has no venue or year in the file; citation R23/R28 keeps the project's earlier venue (3rd International Surfing Reef Symposium, Raglan, 2003). Unverified here (network).
Other known limits: outline +-1 px = +-0.2 m = +-4 % area; solid/dashed classification of the apex-zone edge rows +-10 m2; no as-built plan; position unfixable; viewer needs three.js from the CDN (container preview shows REEF_MODEL loaded but no canvas).
Needs network (blocked in this container; for Lior to widen or for a later run):
- https://raisedwaterresearch.com/spot/artificial-reef/us/california/prattes-reef/ (re-check img1 md5 7db4b8ab...; done 2026-10-05, not repeated)
- https://www.researchgate.net/publication/293137985 (venue/year of Borrero & Nelsen; full text)
- https://www.coastalfrontiers.com/removal-of-prattes-reef (any reef outline map or report)
- https://documents.coastal.ca.gov/reports/1998/10/W5a-10-1998.pdf (only if a page must be re-read)
- https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js (viewer rendering test with a real canvas)
- Google Earth Pro historical imagery 2001-2008 at 33.92058, -118.43335 (position, as-built bag layout): a Lior task (A1-A3)

## 6. Next steps (in order)
1. Main: update 04_build/data/models3d_caveats.json and models3d_curated.json with the optional text changes from the final JSON of this run (position row and footprint row only; no numbers change), then run the page build per UPDATE_PROTOCOL.md. The `ev` snippets all still exist in METHODS_3D.md (the added paragraph is new text in 3.10, nothing removed).
2. Page: the reef's Images gallery should now show 38 rows (new: -img-37 Fig. 4 + outline overlay, -img-38 Fig. 20 + scale check).
3. When Lior has network access widened: fetch the venue/year of the 2003 paper and re-check img1 against RWR (list in section 5).
4. When Lior supplies Google Earth historical views (A1-A3), fix the position and decide J2; with the authors' reply (E1) decide J1 and possibly J3; then rebuild (`python build_3d.py`).
5. If a post-Phase-II plan or survey ever surfaces, a second outline version (Phase II, April 2001) could be added; the current drawing must then be labelled "Phase I design layout".

## 7. Re-verification record 2026-10-10 (before / after)
| item | before | after |
|---|---|---|
| shape.json polygons, canonical frame, design_version.drawn, area 435.2 m2, bbox 58.0 x 28.6 m, confidence medium | as listed | unchanged (md5 of canonical block unchanged) |
| `pending_reverification` | present, status unstamped | removed; `reverification` record + `reverified_on` 2026-10-10 + `updated` 2026-10-10 |
| dimensions_check row 2 (cross-shore) | 28.6 vs "30" = -4.7 %, no unit noted | same -4.7 % but adds Fig. 20 29.0 x 58.5 m (+1.4 % / +0.9 %), notes missing unit and non-diagnostic nature |
| confidence factor "not yet re-verified" | open | re-verified wording; level unchanged |
| geo_note | hint +-100 m | adds the text-vs-Fig. 2 inconsistency, hint possibly +-150 m (not propagated) |
| verification array | 7 items | 12 items (8-12 new) |
| 3D model volumes B / A | 443 / 550 m3 | 443 / 550 m3 (identical; model.js data compared key by key: only md5, mtime and date stamps differ) |
| 3D area, crest B apex, crest A, seabed at centre | 435.2 m2, -2.678 m, -1.829 m, -3.67 m MSL | identical |
| METHODS_3D.md section 3.10 | no note | re-verification note appended (position inconsistency, Fig. 20 size check) |
| registry rows | 36 (32 mine + 4 intake) | 38 (-img-37, -img-38 added) |
Files archived first: archive/pre_reverify_2026-10-10/. Scratch (Fig. 20 measurement scripts) was in /tmp and is not kept; the method is in VERIFY.md.

## 8. Source audit 2026-10-10
See SOURCE_AUDIT_2026-10-10.md. Added to METHODS_3D: 2.2 how each source was used, 3.12 decisions D1-D10, per-element confidence (section 6); viewer sub-tabs for sources/assumptions/decisions/confidence. J1 and J2 applied (text only; model.js data identical). Open: S10 venue/year not confirmed; card says V 64 m x 29 m (Blacka 2013) vs our 58.0 m, and ~12.7 t vs 14 t bags (card not edited; for main).

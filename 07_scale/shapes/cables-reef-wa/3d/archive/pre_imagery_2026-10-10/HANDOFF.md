# HANDOFF - cables-reef-wa (fresh agent 2026-10-10, queue item 9: traced + 3D built; verification partial, needs network)

## 1. Status per stage
| stage | state | confidence and why |
|---|---|---|
| trace | done 2026-10-10 (shape.json status "traced") | MEDIUM: design plan (Lyons 1992, reproduced in Blacka 2013 Fig A.2) traced; scale from its own printed dimensions (6.51 px/m, +-3%); 121 x 76 m vs text 140 x 70 (-13% / +9%); no survey or imagery of the built reef |
| verify | PARTIAL (VERIFY.md): internal checks pass; no satellite / aerial / bathymetry (network blocked) | not marked "verified" |
| 3D | built 2026-10-10 (3d/) | LOW: plan medium, design levels exact but datum of RL not stated (0.78 m), bed modelled, nothing surveyed after construction |
| registry | done: 8 existing rows given results / annotated files, 5 own-figure rows added (img-27..31); NEW_IMAGES_LOG lines added | - |
| page | NOT done (main adds the model, see section 6) | - |

## 2. Key decisions and why
- PRIMARY source = Blacka et al. (2013) Fig A.2 (registry img-26, added by the papers-intake agent): same CAD drawing as the RWR 'original design' but legible (labels RL -1.00..-2.50, slopes 1:20/1:15/~1:13, dimensions 40.0/26.0/30.0 m). Scale from four printed dimensions, not from an assumption.
- DEFAULT outline = design plan (outer foot / 'interface line') + the drawn southern-arm extension (img-06, 320 m3): measured survey > design drawing of the built version > photo trace; no survey exists. Other versions: original plan without extension, paper Fig 7 V (assumed 100 m grid, plan only), Pitt concept sketch (plan only).
- Orientation: apex offshore (west), north = drawing right; arms 42.7 / 44.7 deg to the shore = the 45 deg design peel angle. Shoreline assumed N-S.
- Model frame (model.js): x SOUTH (= -x of shape.json), y WEST, z up, z = 0 at MSL under datum reading A (z_MSL = RL - 0.78). Reading B (RL = MSL, Blacka's wording) is a switch in the viewer (moves the water 0.78 m).
- Bed = plane, gradient 1:30 (Pitt sketch), level fitted so modelled rock volume = 5,500 m3 (Blacka A.1.3): RL -3.50 m at y = 270 m; 5,000 m3 -> 3.36 m; 3,500 m3 -> 2.92 m. A calibration, flagged estimated.
- Only the two Lyons-plan versions have a 3D mesh; Fig 7 and Pitt outlines are plan-only (no design levels).
- 3D viewer derived from the Borth viewer (aux/make_index.py patches it); previews use the vendored three.js (aux/preview.py).

## 3. Key numbers (units, datum, source id)
- Footprint (A2 trace, scale 6.51 px/m): original 4,049 m2, 121.2 x 76.3 m; with extension 4,355 m2, 121 x 89 m; ramp (between the rock bands) 3,113 m2; extension 347 m2 (320 m3 stated, 0.92 m mean) [img-26, img-06]. Scale-range area 4,105-4,629 m2.
- Design levels RL: crest line -1.0, set-out line -3.0, contours -1.5/-2.0/-2.5; slopes 1:20 (apex), 1:15 (north arm), ~1:13 (south arm) [img-26]; model vs drawing rms 0.14 m (centreline), crossings within 0.1-1.4 m on the transects.
- Datum: MTL 0.78 m above datum [S1 p.3]; tide range 0.8 m [Blacka Table 4.3]; typical HW/LW MSL +-0.4 (estimate). Crest depth below MSL: 1.78 m (A) or 1.00 m (B). HAT/LAT not found.
- Rock volume: 5,500 (Blacka A.1.3), 5,000 (P3/ICM), 3,500 (Wikipedia), >10,000 t (card): density 1.82 t/m3 at 5,500. Mean thickness 1.26 m, max 2.5 m.
- Offshore position: centroid 270 m (Fig 7 measurement 271 m with a 100 m grid assumption; text 250 m S1 / 275 m RWR, Blacka).
- Water depth 3.0-6.0 m [Blacka Table 4.2, RWR]; modelled bed under the footprint RL -2.0 to -5.0 (2.8-5.8 m at MSL under reading A).

## 4. File map (07_scale/shapes/cables-reef-wa/)
- shape.json: traced outlines (4 versions), sources, design_surface ramp polygon, dimensions_check; open for the page / any viewer.
- METHOD.md (trace log; the older 2026-10-05 text at the top is superseded by the 2026-10-10 section), sources.md, VERIFY.md.
- scripts/: trace_a2.py -> compute_shape.py -> make_overlays.py -> make_shape_json.py (re-runnable); a2_trace.json, computed.json (numbers), p05_toe_pixels.json.
- overlays/: annotated traces (6 PNG); src/: paper PDF + page renders from the earlier run (kept; registered as img-21..23).
- 3d/: index.html (viewer; versions + (i), water slider, VE 1-5x, views, photo match, sources, methods tabs), model.js (672 KB), docs.js, build_3d.py (+ b3d_lib.py, provenance.py), make_annotations.py, register_images.py, aux/ (make_index.py, preview.py), METHODS_3D.md, SOURCES_3D.md, REQUESTS_FOR_LIOR.md, annotated/ (A1-A4), previews (plan, oblique, crest x3, versions pop-up, methods panel, low water x2).
- Bulky: model.js, preview PNGs. Not worth opening: b3d_lib.py unless the surface changes.

## 5. Open issues, discrepancies, pending checks, needs network
Discrepancies: (1) RL datum 0.78 m (S1/Pitt = chart datum vs Blacka 'below MSL'); (2) text length 140 m vs 121 m traced (-13%); (3) volume 3,500 / 5,000 / 5,500; (4) Pitt 2009 'crest ~1.5 m below the lowest tide' vs design RL -1.0; (5) card says 275 m offshore vs S1 250 m; (6) extension size from a low-resolution drawing; (7) ride-length check inconclusive (crest arms 49 / 52 m vs ride 50-80 / 30-40 m).
NEEDS NETWORK (blocked all run: curl code 000 to raisedwaterresearch.com, services.arcgisonline.com, google.com):
1. Esri World Imagery and Wayback tiles of the reef, zoom 19, about -32.01..-31.99 N, 115.735..115.760 E (run 07_scale/tools/satellite.py fetch; the reef is a V pointing west about 275 m off the Cable Station / McCall Centre waterline, Leighton Beach). Why: georeference and verify the outline, the extension, the arm angles; upgrades the shape to verified and the plan to high confidence if visible.
2. Higher-resolution originals of the RWR drawings: https://raisedwaterresearch.com/wp-content/uploads/2019/11/Cables-Design.jpg and ...Cables-Additional-Fill-Area.jpg (only if larger than 478 / 417 px): extension geometry.
3. Perth coastal bathymetry: WA Department of Transport / Landgate LiDAR bathymetry and AusSeabed (https://portal.ga.gov.au/persona/marine), EMODnet is not applicable: bed under and around the reef, nearshore profile.
4. Navionics https://webapp.navionics.com (redirects to https://maps.garmin.com/en-US/marine/): reef obstruction symbol and depths; or Lior's app readings (3d/REQUESTS_FOR_LIOR.md).
5. Tide datum: Transport WA / BoM Fremantle tide station sheet: LAT, MSL, HAT, chart datum vs AHD (decides reading A vs B).
6. Papers (not local): Lyons (1992) UWA design report; Ranasinghe et al. (2001); Pattiaratchi (2003) video monitoring; Bancroft (1999): extension size, as-built levels.

## 6. Next steps (in order)
1. Main: add the model per 04_build/UPDATE_PROTOCOL.md: edit data/models3d_combined.json (copy a similar entry: frame note 'x south, y west', polygon expression, crest, hand), data/models3d_curated.json (key numbers, state_short), data/models3d_caveats.json; then remove cables-reef-wa from data/models3d_hold.json if present; run python src/update_page.py. Texts are in the final JSON of the agent report.
2. When the network opens: items 1-3, 5 of section 5; rerun scripts/trace_a2.py only if a better drawing arrives; georeference with satellite.py, add "geo" to shape.json, rerun 3d/build_3d.py, re-view previews (aux/preview.py), set shape.json status verified and rewrite VERIFY.md.
3. Resolve the datum with Transport WA (E7): then set READ default in index.html (aux/make_index.py) and the levels in build_3d.py.
4. If Lior supplies Navionics readings: replace the fitted bed (3d/build_3d.py: D0, G_BED) by a read bed and update METHODS_3D sections 3.4 and 4.

## 7. CHECKPOINT 2026-10-10 (end of run)
All stages above finished except network-dependent verification (HANDOFF_STOP: network). No stage is half-written. The 'Fresh-agent run' part of METHOD.md describes the run; scripts reproduce every number.
- Source audit 2026-10-10 done: see SOURCE_AUDIT_2026-10-10.md. METHODS_3D.md now has assumptions A1-A11 and decisions X1-X8; SOURCES_3D.md has a "how used" table; docs.js rebuilt (values unchanged); max thickness corrected to 2.5 m in text.

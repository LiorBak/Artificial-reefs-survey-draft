# VERIFY - cables-reef-wa

## Revision 2026-10-10 (network open): VERIFIED against DoT WA soundings and Esri imagery
Status: shape.json "verified" (verified_on 2026-10-10). Result: the traced original design plan is right in position, orientation and scale; the drawn south-arm extension is NOT confirmed; the first model's assumptions (shoreline N-S, plane bed fitted to 5,500 m3, drawing = built) were replaced or tested. Overlay match: GOOD.

| # | check | verdict | evidence |
|---|---|---|---|
| R1 | position, orientation, scale vs a coordinated survey | pass | DoT WA single-beam soundings of 22 Nov 1999 (FR19991122_Single.txt, 840 pts, AHD) over the 1998 pre-construction bed: the traced outline, moved and rotated only (theta 9.74 deg ccw, anchor 32.015644 S 115.748462 E), contains 91.0 % of the rock soundings (> 0.6 m above bed, n = 564) and 18.5 % of the bed soundings (n = 135); with scale free the best scale is 0.979 (scripts/georef_fit.py; src/bathymetry/figures/survey_1999_thickness.png, img-38) |
| R2 | overlay on georeferenced imagery | good | outline coincides with the dark rock patch on Esri Wayback 2014-12-03, 2020-03-23, 2022-06-08, 2024-08-15 and World Imagery (capture 2025-12-06); on 2020-03-23 a wave breaks on the NE arm; mean luminance inside / ring 0.35-0.87 on 7 images (src/imagery/annotated/overlay_montage_4dates.png, img-37). No image information entered the fit. |
| R3 | design version | answered | the soundings show the original plan footprint (Nov 1999 and Feb 2002); the dossier's southern extension (347 m2, 320 m3 drawn): Feb 2002 soundings in the triangle +0.43 m mean (median 0.29, n = 23) vs +1.29 m inside the plan and +0.19 m in the ring outside; the triangle is as bright as its surroundings. NOT CONFIRMED; kept as a separate version. The page must say the default drawing represents the original plan as surveyed, not the extension. |
| R4 | scale | pass | soundings: 0.979 (2 %); printed dimensions: 6.51 px/m (sd 0.05) |
| R5 | dimensions vs text | ok with note | 121 x 76 m (drawing and soundings agree) vs text 140 x 70 m (-13 % / +9 %): the text is rounded |
| R6 | arm angles | changed | after georeferencing the frame axis is 9.7 deg off true north and the shoreline is at 7.8 deg T (DoT Perth_5m 0 m AHD line), so the arms meet the shoreline at about 27 deg (north arm) and 60 deg (south arm); the 42.7 / 44.7 deg to the frame axis are the design peel angles, not shoreline angles |
| R7 | rock volume | mismatch resolved | design surface on the measured bed: 3,920 (original) / 4,249 m3; surveyed 4,671 (Nov 1999) / 5,219 m3 (Feb 2002), +-1,000; stated 3,500-5,500 |
| R8 | datum | partial | design ramp RL minus surveyed AHD = 0.59 / 0.50 m; A 0.78, B 0.00: A is nearer; Fremantle CD-AHD offset not found |
| R9 | offshore distance | measured | 254 m (E) - 263 m (080/100 deg) from the anchor to the 0 m AHD line; text 250 m (Pattiaratchi) / 275 m (Blacka) |
| R10 | Gemini | n/a | not in this repo; nothing used |
| R11 | confidence | set | plan HIGH (extension LOW), 3D MEDIUM; reasons in shape.json and METHODS_3D 6 |

Before / after of the model (first-run values from archive/pre_imagery_2026-10-10/model.js):
| quantity | before | after |
|---|---|---|
| default version | design plan + extension | Nov 1999 surveyed surface on the original plan |
| footprint (default) | 4,355 m2 (121 x 89 m) | 4,049 m2 (121 x 76 m); extension version 4,355 m2 |
| rock volume (default) | 5,500 m3 (fitted) | 4,671 m3 (surveyed, +-1,000); design surface 3,920 (original) / 4,249 (extension) |
| mean / max thickness (default) | 1.26 / 2.48 m | 1.15 / 2.76 m (design: 0.97 / 2.30) |
| crest | design RL -1.0 = -1.78 m MSL (A) / -1.00 (B) | design unchanged; surveyed surface top -1.55 m AHD, highest sounding -1.40 m (Nov 1999) / -1.67 m (Feb 2002) |
| datum reading A / B | unresolved, 0.78 m apart | A default, survey-implied 0.5-0.6 m; B kept as a switch for the design versions |
| seabed | plane 1:30, RL -3.50 at y = 270 | measured: -3.68 m AHD at the anchor, 2.84-6.63 m below MSL (A) along the outline |
| orientation | shoreline N-S | frame 9.7 deg from true north, shoreline 7.8 deg T |

Open: Fremantle chart-datum to AHD offset and HAT / LAT (Transport WA); Wayback capture dates; the papers (Bancroft 1999, Ranasinghe 2001, Pattiaratchi 2003 / 2007); a survey after 2002. Dead ends: 02_research/dead_ends/cables-reef-wa.json.

---
## First verification (2026-10-10, no network, history)

Status: shape.json stays "traced". The checks that could break the trace (a dated aerial / satellite image of the built reef, the full design drawing set) need the network, so it is not marked "verified".

| # | check | verdict | evidence |
|---|---|---|---|
| 1 | Overlays re-rendered from the stored trace and viewed | pass | overlays/cables-reef-wa-img-26_A2_outline_ramp_scale.png (outline follows the interface line within ~2 px = 0.3 m; ramp polygon follows the inner edges of both bands), -img-06_extension_triangle.png, -img-20_fig7_V_outline_rotated.png, -img-05_retrace_outer_foot.png, -img-07_pitt_concept_outline.png; scripts/make_overlays.py regenerates them |
| 2 | Design version | partial | Fig A.2 is the Lyons (1992) design that Blacka (2013, A.1.1) calls 'the final reef design'; the dossier (card R5) says the south end was extended during construction, drawn in img-06. The built extent and any later change are not documented in any local source. Pitt (2009) recommends a shallower reef and a longer nose: a recommendation, not built. |
| 3 | Scale | pass | four independent readings of printed dimensions on Fig A.2 (26.0 m, 30.0 m, 0.5 m contours at 1:20, 40.0 m) give 6.57 / 6.49 / 6.52 / 6.46 px/m (sd 0.05); the earlier guess from an assumed 50 m grid on the RWR copy (3.6 px/m) was within 6% of the A2-derived 3.39 px/m for that sheet |
| 4 | Arithmetic | pass | areas re-run with shapely (4,048.5 m2 original; 4,355.3 m2 with the extension); canonical frame checked by hand (apex vertex x +10.7 m, y 314.3 m); the make-canonical tool of 07_scale/tools was NOT used, so its old rotation bug does not apply (sheet axes = frame axes) |
| 5 | Dimensions vs text | within 14% | 121.2 x 76.3 m vs the text 140 x 70 m (-13% / +9%); the text says 'approximately'; with the extension the width is 88.7 m |
| 6 | Independent agreement | pass | RWR copy re-traced at an assumed scale: 4,209 m2 (+4%); Fig 7 V with an assumed 100 m grid: 122 x 76 m (A2: 121 x 76 m) and its centroid 271 m from the shore line (text 250-275 m) |
| 7 | Shape / angle test (scale-free) | pass | arms 42.7 and 44.7 deg to the shoreline, apex ~87 deg, versus the 45 deg design peel angle (S1 p.2); long arm to the south on all sheets |
| 8 | Orientation | inferred | apex offshore from Fig 7 (INDIAN OCEAN label) and the Pitt wave arrow; north = sheet right from the Pitt north arrow; shoreline assumed N-S (Fig 7 within ~5-8 deg) |
| 9 | Provenance | pass | each source has url, figure, date, credit and registry id (sources.md, shape.json); the RWR drawings are undated |
| 10 | Gemini findings | not applicable | Gemini folder not in this repo |
| 11 | Confidence | MEDIUM, honest | design drawing with printed scale, within 14% of the text, no survey or image of the built reef; extension from a low-resolution drawing |

Corrections to earlier notes: (a) the earlier footprint file 07_scale/reefs/cables-reef-wa.footprint.json (verified 2026-09-25) drew a thin V band of 2,299 m2 with apex offshore at low confidence; the design drawing shows a solid mound (ramp plus side slopes) of ~4,050 m2, and apex offshore is now supported by Fig 7 labels and the design peel angle; (b) the text 'max width 70 m' fits the cross-shore extent of the V (76 m), not an arm width; (c) the earlier run of this task guessed the scale from the RWR copy (3.6 px/m); the legible Fig A.2 replaced that guess.

To turn this into a verified shape (needs network, HANDOFF.md section 5): a dated aerial / satellite image in which the reef is visible, to georeference the outline, check the extension and the arm angles.

# VERIFY - cables-reef-wa (2026-10-10; no network: PARTIAL verification, internal checks only)

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

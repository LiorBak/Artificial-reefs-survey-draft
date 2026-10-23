# HANDOFF - narrowneck-gold-coast (written 2026-10-06 by the resumed tracer; read this instead of re-reading the sources)

## SOURCE AUDIT 2026-10-10 (documentation only; no model value changed)
- Result file: SOURCE_AUDIT_2026-10-10.md (statement -> source -> location -> how used -> status). 3d\METHODS_3D.md now holds: 2b (how each source was used + id crosswalk to sources.md), 3.6 (assumptions A1-A16 with effect and replacement), 3.7 (other methods, scripts, AI involvement), 3.8 (decisions log D7, N1-N14), 6 (confidence per element). The viewer (3d\index.html, Methods tab) shows them as chips: METHODS_3D.md, Sources: how used, Assumptions, Decisions, SOURCES_3D.md (docs.js rebuilt by build_3d.py; model.js identical except versions_info text).
- D7 (Lior, 2026-10-10): default outline = the 2020 photo trace. Recorded in REQUESTS_FOR_LIOR.md (Decisions taken), shape.json (default_outline_decision, versions_info), 3d\METHODS_3D.md 3.8, model.js versions_info.
- Unconfirmed citation details (listed in REQUESTS_FOR_LIOR.md): Black & Mead 2001 record; Jackson 2012 DOI; Jackson 2007 journal pages (67-79 from a citing paper only).

## VERIFIED 2026-10-10 (stage 1 done; details in VERIFY.md sections STEP 1 DONE, STEPS 2, 3-5, 6-9 and the CORRECTION under step 2)
- shape.json status "verified with issues"; verification[] (10 checks), outline_versions (5), default_outline "photo_2020-08-08", versions_info, faint_seaward_patches. Canonical polygons unchanged (traced 2026-10-06, confirmed).
- SCALE CONFLICT RESOLVED: no conflict. Corbett Fig 2 bar (97 px = 50 m, 0.5155 m/px) gives crest loops 71 m (the 85-90 m was an eye estimate), alongshore crest extent 119 m = text 120 m; Corbett Option 1 and Jackson Fig 2 are the same CAD design on one scale (chamfer s=1.504, 0.65 px); Jackson chain 60-62 m agrees within 3 %.
- Option 2 WAS BUILT (Corbett 2023 PDF p.5): north reef almost fully achieved, south reef + bridge only partly (p.3). No post-renewal as-built plan/survey exists; only the 2017 pre-works multibeam (Corbett Fig 3 = img-55).
- OUTLINE VERSIONS (areas m2, all in canonical frame; scripts in verify_scripts\): photo_2020-08-08 (DEFAULT, 6,239, confidence medium: lower bound); design_option2_2017 (13,941 = -6 m AHD envelope + crest loops, +-15 m, medium-low: concept, partly built); design_2004_revised (13,631, +-15 m, scale +-10 %, pre-renewal); survey_2011-06-09 relief zone (4,922; 3,000-7,000 by threshold; no depth legend; pre-renewal; low); navionics_4.0m_shoals (537, indicative only, low). 96.6 % of traced arms lie inside the Option 2 envelope, 94.5 % inside the 2004 one. D7 (default photo vs Option 2) is with Lior; recommendation: keep the photo (only evidence of the state actually built; Option 2 is a drawing whose south part is not as built).
- Option 2 vs 2004 crest: ~22-25 m seaward (matches text 20 m); placement via panel offset 358 px (grey Option 1 silhouette fit 352, text 363) +-10 m; independent best-fit shifts of the Option 2 halves onto the trace are only -6..-14 m.
- Not possible: Gemini re-fetch (no network to the hosts), Black & Mead paywalled. Navionics "0.9" still needs Lior (REQUESTS 4).
- Registry: now 78 rows (img-54..65 = Corbett 2023 figures; img-55 Fig 3 multibeam was pending then, closed in stage 2); overlays: option2_on_s3, design_2004_minus6_on_s3, survey2011_zone_on_s3, faint_patches_on_s3, navionics_shoals_on_s3 (overlays\).
- Superseded in the text below: section 3b "closed 4.5 m loop over the south arm" (it is an open U); section 5 item 1 (renewal option: settled, Option 2); the "2 untraced seaward patches" (now 24 faint patches, 663 m2, in shape.json).

## STAGE 2 DONE 2026-10-10: 3D MODEL BUILT (3d\; confidence MEDIUM)
- Files in 3d\: model.js (0.6 MB), docs.js, index.html (viewer: five outline versions + (i), datum-rule switch, other outlines as lines, faint patches, photo match), METHODS_3D.md (read this for numbers and the limitations table), SOURCES_3D.md (step log), REQUESTS_FOR_LIOR.md, MAIN_TYPED_TEXTS.json (texts for 04_build\data), build_3d.py + nn_lib.py + prep_multibeam.py + make_annotations.py + make_previews.py + register_images.py, src\multibeam_fig3.npz/.json, annotated\A1-A6, preview_*.png. Rebuild: `python prep_multibeam.py; python build_3d.py; python make_annotations.py` from 3d\. Previews need the vendored three.js (sandbox has no CDN): `python make_previews.py`.
- State: renewed reef June 2018, default = photo_2020-08-08 (D7 DECIDED by Lior 2026-10-10: keep the 2020 photo trace; Option 2 stays a toggle). Other versions: Option 2 2017, 2004 design, 2011 survey zone (solids, volumes) and Navionics 4.0 m shoals (outline only).
- Method: seabed = Corbett 2023 Fig 3 pre-works multibeam (img-55) digitised by hue through its colour bar (scale 0.4651 m/px, placed at x -5, y 290 m +-10 m, AHD assumed), containers removed by grey opening; outside: Navionics labels 7-10 m (seaward) and an ASSUMED nearshore profile (0 / -1.8 / -2.1 m AHD at y 0 / 100 / 190). Reef top = design surface (crest loops -2.5 AHD to -6 envelope, linear in distance rank; checked vs multibeam tops: +0.26 m, sd 0.66 m), default version lowered to the measured crest -2.2 AHD, min. visible height 1.0 m, flank 1.5:1.
- Volumes (mound envelope above the bed, gaps included, m3): photo 13,495 (+-3,100); Option 2 21,271; 2004 13,603; 2011 zone 6,856. Placed sand = 534 x 147 = 78,500 m3: exposed mound is 17-27 %.
- Datum decision: MSQ (AHD = LAT + 0.760, z_MSL = z_AHD - 0.12) as default; the papers' rule (LAT + 1.00) is a viewer switch (geometry +0.24 m). Crest -2.2 AHD = 1.44 m below LAT (MSQ) / 1.20 m (papers). All geometry is in AHD, so only the tide levels move.
- Findings: stage-1 height estimate (4-6 m at the toe) NOT supported: multibeam relief 1-1.5 m at the toe, 2-2.5 m at the crest wedge, p99 1.8-2.2 m. The shallowest multibeam tops (-1.8 S arm, -2.5 N arm) agree with the measured crest -2.2 AHD (supports the AHD assumption of Fig 3). Navionics land edge is ~80 m seaward of our 2020 waterline: its nearshore contours not used.
- Registry: 8 pending rows closed (img-01, 04, 14, 24, 31, 50, 51, 55) + img-69 (Blacka 2013, added by the papers intake); new rows img-75..78 (A5, A6, preview_oblique, preview_plan); check_registry: Narrowneck passes (78 rows; the only errors in the run are Opunake's).
- For main (04_build): see 3d\MAIN_TYPED_TEXTS.json (curated, caveats, combined entries) and UPDATE_PROTOCOL.md "NEW model"; run `python src/update_page.py` from 04_build.
- Open: crest datum offset (City/MSQ); Navionics 0.9 label and nearshore readings (3d\REQUESTS_FOR_LIOR.md); no post-renewal as-built; toe invisible.

Reef: Narrowneck Reef, Gold Coast (Qld). Work folder: 07_scale\shapes\narrowneck-gold-coast\ . Registry: 03_images\reefs\narrowneck-gold-coast\ (78 rows).
Source summary for the Gold Coast papers/datums (pages, quotes): 07_scale\bathymetry\gold_coast\REPORT.md sections 3 (datums) and 6 (Narrowneck) - do not re-open the papers unless a number below must be checked.
Source ids: s1..s12 are in sources.md; img-NN are registry ids (03_images\reefs\narrowneck-gold-coast\images.json). Pixel coordinates "s3 px" = the 1517 x 1517 px image src\wayback\nn_wayback_2020-08-08_r9812_z19.png.

## 1. STATUS PER STAGE
| stage | status | date | confidence + reason |
|---|---|---|---|
| plan-shape TRACE | done, shape.json status "traced" | 2026-10-06 | MEDIUM: both arms resolve into individual 20 m containers on georeferenced 2020 imagery (edges +-1 m; confirmed on a second tile set to 0.2 m and by the Navionics shoal loops to ~20 m), arm length within 10 % of the design drawing; but the deeper toe (below ~6 m) is not visible, 3 channel containers are faint, and which renewal option was built is unverified |
| VERIFY | done 2026-10-10, status "verified with issues" (see top section) | 2026-10-10 | medium: visible field is a lower bound; no post-renewal survey |
| 3D model | DONE 2026-10-10 (3d\; see the STAGE 2 DONE block at the top) | 2026-10-10 | MEDIUM: crest and bed measured (multibeam read from a colour picture, +-0.4 m / +-10 m), no post-renewal survey, toe invisible, datum 0.24 m |
| image registry | 78 rows; check_registry.py passes for Narrowneck | 2026-10-10 | all 3D checks closed (pending 0); img-75..78 = 3D figures |
| page (04_build) | not touched by this task | - | the page needs shape.json, overlays\ and the registry |

## 2. KEY DECISIONS AND WHY
1. STATE DRAWN = the RENEWED reef as left in June 2018 (84 containers added around the existing 2004 revised structure; the City: "minor changes to the shape", REPORT 6.2). Why: Lior's rule (model the latest as-built state; history goes in captions); post-renewal imagery shows the containers.
2. PRIMARY = Esri Wayback release 9812, capture 2020-08-08, z19 (s3, img-45). Why: sharpest post-June-2018 image. The other tile sets: 2019-06-18 (r21485, s5/img-47) blurred/blocky; 2021-04-17 == 2021-08-12 (byte-identical) blurred; 2022-11-06 == 2023-06-09 == 2025-04-27 (byte-identical; s4/img-46) dark but resolved; 2025-10-10 (s2/img-44) featureless; 2016-07-01 (s6/img-48) pre-renewal, murky. The identify date on repeated tile sets is only a lower bound.
3. OUTLINE = the VISIBLE container field (thresholded dark patches + closing radius 3.7 m), not a design contour. Why: the design outline is a prior and may be ~20 m off (unverified, Corbett 2023 snippets); the visible field is what exists. It ends at about the -6 m design contour; deeper toe invisible, so the footprint is a lower bound.
4. Design prior = Jackson et al. 2012 Fig 7 / Fig 6b (img-10 / img-09) georeferenced by chain: Fig 7 = 1.75 x Fig 6b (same photo); scale 0.21 m/px +-10 % (Jackson 2007 Fig 13 100 m bar = 4.275 px/m, img-27, plus dark-patch matching); placed on s3 by dark-patch NCC (corr 0.57, rotation 0.5 deg). Tolerance +-15 m at the ends (translation sensitivity: 12 m). Used only as a cross-check, never to move the polygons.
5. Shoreline frame: waterline of the 2020-08-08 image (z17, 285 rows) -> bearing 356.2 deg (north-heading); origin = waterline foot of the area-weighted centroid; +x alongshore (north), +y offshore (bearing 86.2). geom.py used as fixed 2026-10-05 (selftest 334/334); one point hand-checked (N arm vertex 0, s3 px (379,605) -> (41.399, 239.740) m by pixel algebra, by lat/lon, and by geom.py).
6. Naming: the three E-W shapes in the channel mouth are "channel containers", NOT "weir": the 2004 weir containers (Jackson 2012 Figs 4, 7) are drawn N-S across the channel 25-40 m seaward of them and are invisible in 2020 (lowered up to 2 m, largely buried, Jackson 2012 p.6).
7. Confidence level "medium" (not "high") because of decision 3 and the unverified renewal option.
8. Gemini rejected: two stacked "inshore/offshore lobes", 400 x 220 m, 75,000 m2 - no source supports them (METHOD Step 4).
9. Navionics: used as an independent POSITION check and seabed context; NOT used for the crest (chart smooths the reef to a 4.0-4.5 m shoal; the one crest-like value, a "0.9" spot depth, probably carries an older crest state).
10. Datum policy for crest values: carry +-0.25 m for the ICM rule (AHD = LAT - 1.00) vs MSQ (AHD = LAT + 0.760).

## 3. KEY NUMBERS (units; datum; source)
### 3a. Plan shape (canonical frame, metres; shape.json canonical.polygons_m; s3; geom.py make-canonical)
Frame: origin = s3 px (-517.90, 821.74) = lat -27.986800, lon 153.431127 (2020-08-08 waterline); +x alongshore toward bearing 356.21 deg; +y offshore toward 86.21 deg; scale 0.263665 m/px (1/3.7925 px/m, Web-Mercator z19 at -27.9867). Reef centroid lat/lon -27.986629, 153.434052.
| polygon (index in polygons_m) | area m2 | x range m | y range m | long axis bearing / to shore | length x width m |
|---|---|---|---|---|---|
| north_arm [0] (71 vertices) | 3,678 | -9.3 .. 55.4 | 239.7 .. 369.1 | 104.0 deg / 72.2 deg (min-rect 94.0 / 82.2) | 135.6 x 54.1 (min-rect 134.0 x 53.9) |
| south_arm [1] (51 v.) | 2,269 | -57.9 .. -17.8 | 230.3 .. 341.7 | 86.2 / 90.0 (min-rect 84.5 / 88.3) | 110.5 x 39.0 (111.5 x 39.6) |
| wing_patch_NW_a [2] | 129 | 44.8 .. 52.4 | 211.7 .. 246.5 | 87.4 | 33.6 x 6.6 |
| wing_patch_NW_b [3] | 105 | 23.0 .. 37.4 | 215.3 .. 235.3 | 61.3 | 18.5 x 12.0 |
| channel container 1 [4] (solid) | 25.6 | -5.4 .. -2.0 | 249.3 .. 265.5 | 93.5 | 15.6 x 2.0 |
| channel container 2 [5] (FAINT) | 19.1 | -9.5 .. -7.1 | 247.6 .. 261.0 | 90.5 | 12.5 x 1.6 |
| channel container 3 [6] (FAINT) | 12.7 | -15.7 .. -12.9 | 255.4 .. 265.3 | 97.3 | 9.2 x 1.8 |
Totals: all polygons 6,239 m2; arms only 5,948 m2; bbox all 113.3 m alongshore x 157.4 m cross-shore; arms only 113.3 x 138.8; max dimension 165.6 m; nearest reef edge 211.7 m, arm bodies 230-240 m, area centroid 288 m, tips 342-369 m offshore of the 2020-08-08 waterline (+-15 m, tide/beach state). Channel (minimum gap between arm polygons) 20.7 m; arm centroid separation alongshore 58.7 m. Arms converge seaward by about 18 deg (+-5 deg).
Shoreline bearing 356.2 deg (fits 356.0-356.5 by window; +-0.3 deg), shore normal 86.2 deg. Untraced seaward dark patches (3, raw s3 px x 767-880, y 539-664): shape.json sources s3 extras_not_in_polygons (maybe buried containers or natural reef).
Lat/lon polygons: shape.json geo.polygons_latlon (same order). Pixel polygons: shape.json sources[s3].pixel_polygons and trace_s3_out.json.
### 3b. Cross-checks (numbers)
- s4 vs s3 phase correlation: 0.65 px E, -0.37 px (0.17 m E, 0.10 m N). s5/s6 by eye +-3-4 m.
- Council polygon OBJECTID 4637 (s1): in our frame 171 m alongshore x 262 m cross-shore, 34,565 m2 (attribute 34,409; LENGTH 256, WIDTH 151, HEIGHT 3, TOP_REDUCED_LEVEL -2.5, VOLUME 7,668 unreliable); contains 100 % of the traced area; traced area = 18 % of it.
- Design drawing scale: Jackson 2007 Fig 13 bar 100 m = 428 px (black segments 154-241 and 325-407 px = 20 m each): 4.275 px/m +-1 %. Design north-arm crest loop ~62 m, outer (-6 m) arm length ~121 m (traced 134 m, +10 %), channel wall ~33 m, tip-to-tip ~55 m.
- Design prior vs trace (canonical y, m): N arm design outer contour 217.2-354.1 vs traced 239.7-369.1; S arm 207.8-345.8 vs 230.3-341.7. Fig 7 -> s3 affine in design_registration_out.json and shape.json design_prior. Registration +-15 m.
- Navionics (img-50..53): SonarChart closed 4.0 m loop (+4.5 m loop) over the north arm; closed 4.5 m loop with a "0.9" obstruction label over the south arm; closed 6 m loop between the arms; 5.5-6 m contours around; 7-10 m seaward; 0.5 m labels; nearshore 0-2 m within ~100 m of the beach; restricted-area polygon ~118 x 140 m around both arms. Nautical layer: only spot depths 0.9 and 5.9 inside that polygon. Datum not stated by the app (assumed LAT). Trace laid on the chart (map centre = reef centroid, 0.5273 m/px) falls on the shoal loops within ~20 m.
- Visible container footprint is ~70-80 containers (80 m2 each) vs ~534 placed: most are stacked or deeper than the visible limit.
### 3c. Container facts (see REPORT 6.1-6.3 for pages)
20 m long, 3-4.5 m diameter, 408 placed Aug 1999 - Dec 2000 (Jackson 2007 p.4); ~450 by 2006: +10 (2002-03), +15 (2004: weir 2 + flared wings 2 + replacements), +17 (2006) (Jackson 2012 p.3, Fig 4 table p.4); +84 in the 2017-18 renewal "around the existing structure" (City of Gold Coast 2020 archived page); sand volume ~147 m3 per container (60,000 m3 / 408); settlement: weir containers lowered up to 2 m, now 1.5 m below design; flare containers 1-1.5 m (Jackson 2012 pp.6-7).

## 4. FILE MAP (open only when the line says so)
Top level of 07_scale\shapes\narrowneck-gold-coast\:
- HANDOFF.md - this file; start here.
- shape.json (41 kB) - the deliverable: canonical polygons_m + per-polygon stats, geo (lat/lon), angles, dimensions_check, design_version, design_prior, gemini, references, sources s1-s12. Open for any number; verifier: read confidence/design_version/dimensions_check.
- METHOD.md - full log (Steps 0-6) ending with "INPUTS FOR 3D" (table: source, page, value + datum, uncertainty). Open Step 2d (design-prior registration), Step 5 (Navionics) and the last section when building the 3D model; skip the rest unless auditing.
- sources.md - rows s1-s12 (url, page, date, credit, licence, retrieved, role) + registry id map. Open for citations.
- trace_s3.py (+ trace_s3_out.json) - reproduces the polygons and the shoreline bearing from the images (prints 71/51 vertices, 356.21). Run it to audit the trace.
- design_registration.py (+ design_registration_out.json) - reproduces the Fig 7 -> s3 affine (corr 0.567). Run to audit the design prior.
- scripts\ - the helper scripts used for metrics, overlays, Navionics capture, shape assembly and registry updates (frame.py, metrics.py, council.py, make_overlays.py, make_design_overlays.py, nav_annotate.py, nn_navionics_capture2.py (copy of the Palm Beach capture script, reef = this centroid, random free port + fresh profile), build_shape.py, finish_shape.py, reg_results.py, nnreg.py = registry helper) + their small JSON inputs. They were run from a scratch folder; copy inputs next to them before re-running. Not needed otherwise.
src\ :
- wayback\ - s3 (primary, 0.7 MB), s4, s5, s6 (z19, + .geo.json bounds) and s7 (z17 3 km, 5.5 MB; only for the shoreline). Open s3 to look at the reef; the others only to audit.
- nn_esri_z19_current.png - s2, 2025 image, reef barely visible; do not trace.
- gc_opendata_artificial_reef_raw_{28356,4326}.geojson - s1 council polygon (all 11 reef records).
- navionics\ - 20 PNG screenshots (SonarChart/Nautical, z18 shading 0-8 m series + z17 bases) + capture_log.json; open the two annotated overlays instead.
- gov\ - papers and figures saved by the Gold Coast reports task (Jackson 2007 + 2012 PDFs, Vieira da Silva 2021 manuscript, figure crops, archived City page). Open a figure only for the check you need; bulky: the three PDFs.
overlays\ (all viewable; downscale before viewing):
- s3_primary_trace.png - THE trace (7 polygons) on the primary image, with 20 m bar. Look at this first.
- s4_crosscheck_on_2022-11.png, s5_check_on_2019-06.png, s6_pre_renewal_2016-07_with_s3_trace.png - same polygons on the other tile sets.
- design_prior_fig7_contours_on_s3.png - white 2004 design contours (Fig 7) placed on the 2020 image with the arms; fig7_2011_aerial_design_contours_with_2020_trace.png and fig6b_2011_aerial_with_2020_trace.png - the reverse (our trace on the 2011 aerial) = visual proof of the registration.
- navionics_sonar_z18_shade0/5_with_trace_and_readings.png - trace on the Navionics chart with the readings marked (shade 5 shows the <5 m lobes).
Other places:
- 03_images\reefs\narrowneck-gold-coast\images.json + IMAGES.md (78 rows; img-54..65 Corbett 2023; results of the planform checks written into for_3d_check.result); 03_images\reefs\NEW_IMAGES_LOG.md (9 new lines, img-45..53).
- 07_scale\bathymetry\gold_coast\REPORT.md - sources, quotes, pages, MSQ datums (sections 3 and 6).
- 05_qa\00_STATUS.md - dated entry "2026-10-06 - Narrowneck shape TRACED".
- 02_research\reefs\narrowneck-gold-coast.json/.md (card, text dimensions) and 07_scale\reefs\narrowneck-gold-coast.footprint.json (old schematic 600 x 350 m; superseded).

Added by verification (2026-10-10): verify_scripts\ = design_outline_2004.py/.json, navionics_polys.py/.json, fig5a_register.py/.json, corbett_scale\ (step1 scale tests; step2_*.py there are DISCARDED exploratory scripts of the cut-off run, not used), option2\ (option2_outline.py, option2_compare.py + json = Option 2 placement), survey2011\relief_zone.py/.json, faint\faint_patches.py/.json, finish_shape_versions.py (writes the versions into shape.json), render_version_overlays.py. src\gov\corbett2023_extracted\ = Corbett 2023 text + figure crops (registered img-54..65). VERIFY.md = the verification log (read the STEP sections at the end).

## 5. OPEN ISSUES, DISCREPANCIES, PENDING CHECKS, REQUESTS FOR LIOR
1. SETTLED 2026-10-10: Option 2 was built (south reef and bridge only partly). Old text: which renewal option was built (Corbett, Mulcahy, Elliott-Perkins, Hunt 2023, Coasts & Ports; ResearchGate 403, Informit blocked): the "~20 m seaward" shift of Option 2 is unverified. Our trace-vs-design offsets (+15 m N tip, -4 m S tip, ~22 m shoreward) are inside the +-15 m registration tolerance, so neither confirmed nor excluded. Lior to open the paper (REPORT 8 request 1) or the City to supply the renewal drawings/multibeam (REPORT 8 request 2).
2. Deeper toe not visible: the footprint is the field to about -6 m. Seaward dark patches (3) are untraced; a 2025 State bathymetry lidar (REPORT 4) or the City's multibeam would settle the toe.
3. Identity of the three channel containers; the 2004 weir containers are not visible.
4. Crest datum: measured -2.2 m AHD = -1.44 LAT (MSQ 0.760) or -1.2 LAT (ICM 1.00 rule); target -2.5 AHD = -1.74 LAT (MSQ) or -1.5 LAT (ICM): carry +-0.25 m; ask the City for the offset used in the 2018 survey (REPORT 3 remark ii).
5. Navionics "0.9" spot depth (obstruction symbol, suffix unclear, datum unstated): ask Lior to read it in the app at -27.9866, 153.4341 (Navionics app: label, depth units, datum). It is 0.5 m shallower than the measured crest, probably an older state (2001-2012: ~1.0 m below LAT).
6. (CLOSED 2026-10-10, results in images.json for_3d_check.result) Registry rows that were pending for the 3D agent: img-01 and img-04 (crest labels/datum, seabed), img-14 (stack height), img-24 (crest), img-31 (seabed/crest), img-50 and img-51 (Navionics crest/seabed). All other planform checks are written (pending false for 02, 03, 05, 08, 09, 10, 23, 26, 27, 36, 43).
7. Black & Mead (2001) JCR SI 29 pp.115-130 not opened (paywalled): crest "-0.67 m AHD" is known only via Vieira da Silva 2021.
8. Licences: Esri imagery, Garmin charts and the ICCE/Shore & Beach figures are private research copies; reuse rights to be checked before any public release (every registry row says so).
9. Fig 13 vs Fig 7 are not equally stretched (E-W ratio 1.10, N-S 1.22 between the two drawings): the design drawings are not metric to better than ~10 %.
10. geom.py's canonical origin lies outside the s3 crop (waterline is ~290 m west of the reef); this is intentional.

## 6. INPUTS FOR 3D (summary; the full table with sources and pages is the last section of METHOD.md)
State to model: renewed reef, June 2018. z = 0 at MSL.
- Plan: shape.json canonical.polygons_m (arms [0],[1]; wings [2],[3]; channel containers [4]-[6], two faint). Positions +-1 m; footprint = visible field (lower bound).
- Datums (Gold Coast Seaway, MSQ 2014 / 2026; REPORT 3): AHD = LAT + 0.760; MSL = LAT + 0.88; MHWS 1.53, MHWN 1.24, MLWN 0.51, MLWS 0.22, HAT 2.03 above LAT. With z=0 at MSL: LAT -0.88, AHD -0.12, MLWS -0.66, MLWN -0.37, MHWN +0.36, MHWS +0.65, HAT +1.15 m. z_MSL = z_AHD - 0.12 = z_LAT - 0.88.
- Crest: measured -2.2 m AHD (= -1.44 LAT = -2.32 MSL) after the 2018 renewal (Vieira da Silva 2021 AM p.5), +-0.2 m plus the 0.24 m datum ambiguity; target RL -2.5 m AHD = -1.5 m LAT (Jackson 2007 printed p.7; council TOP_REDUCED_LEVEL -2.5).
- Crest variation (design, 2004; Jackson 2012 Fig 2 right p.3 = img-04; Fig 13 img-27): -2.50 over the shoreward wedge (~60 m of each arm), -3.0 ... -6.0 deepening seaward, outer limit -8.0; settlement since then 1-2 m locally. Do not use a flat crest; do not model the 1998 split V.
- Seabed: Vieira da Silva 2021 Fig 3 (img-31, survey 19 Jul 2018, AHD): inner edge -4/-5, under the reef body -6 to -8, seaward -9/-10 (+-1 m); design reef between the -2 m and -10.4 m AHD contours. Navionics (LAT assumed): 4.0-4.5 over the arms, 5.5-6 around, 7-10 seaward, nearshore 0-2 m within ~100 m of the beach edge (img-50). AHD = -(depth LAT) - 0.76.
- Containers: 20 m x 3-4.5 m; two layers at the crest (T2 on 2 x T4, Jackson 2012 Fig 9 p.7, img-14); estimated height above seabed 2-3 m at the shoreward crest, 4-6 m at the toe (stage-1 ESTIMATE, SUPERSEDED by the multibeam: relief 1-1.5 m at the toe, 2-2.5 m at the crest wedge, METHODS_3D 4.3) (ESTIMATE from crest -2.2 and seabed -4/-5 and -6 to -8 AHD); ~534 containers (408 + 42 + 84).
- Orientation: shoreline 356.2 deg, shore normal 86.2 deg; north arrow = +x in the canonical frame (bearing 356.2).
- Caption material (history, not modelled): crest -1.0 AHD (Waikato), -0.67 AHD design, -1.5 AHD (-0.5 LAT) built 1999, -1.0 LAT 2001 top-up, lowered to -1.5 LAT / -2.5 AHD, measured -2.2 AHD after 2018; weir 2004; renewal 2017-18 (84 containers).

## 7. NEXT STEPS (in order; step 1-2 done by the verifier, 3D agent starts at 3; see STAGE 2 plan at the top)
1. (DONE 2026-10-10) VERIFIER: re-run trace_s3.py and design_registration.py (expect 71/51 vertices, bearing 356.21, corr 0.567); look at overlays\s3_primary_trace.png and design_prior_fig7_contours_on_s3.png (downscaled); spot-check three vertices and one canonical point; check shape.json fields against SHAPE_SPEC.md (it has all blocks; verification[] is empty for you to fill); decide whether "medium" confidence stands.
2. Close or ask: items 1 and 5 of section 5 (Corbett 2023; Navionics "0.9" label) - SendMessage to "main" if Lior can supply them.
3. (DONE 2026-10-10) 3D AGENT: build from shape.json + section 6; do the 7 pending registry rows (img-01, 04, 14, 24, 31, 50, 51) and write results into images.json; use Navionics only as a seabed cross-check; keep crest at -2.2 m AHD with the +-0.25 m datum note; model the crest wedge deepening seaward (do not use a flat crest); mark height/slopes "estimated".
4. PAGE (04_build): show shape.json (confidence medium + reason), overlays\s3_primary_trace.png, the design-prior overlay, and the registry gallery (img-45..53 are new).

## 8. SOURCE PAGE INDEX (the facts above, where they come from; REPORT.md sections 3 and 6 carry the quotes)
- Crest measured -2.2 m AHD after the 2018 top-up: Vieira da Silva et al. 2021, Coastal Eng. 171:104027, accepted manuscript p.5 (src\gov\...vieira_da_silva2021_coastal_engineering_accepted_manuscript_2021.pdf). Same passage: designed -0.67 m AHD (Black & Mead 2001), adopted -1.5 m AHD, lowered to -2.5 m AHD; envelope "200-350 m alongshore and 400-500 m cross-shore" (Jackson & Hornsey 2002).
- Target crest -1.5 m LAT = RL -2.5 m AHD ("compromise between safety and surfing"): Jackson et al. 2007, Shore & Beach 75(4), printed p.7; adopted RL -1.5 m AHD (-0.5 m LAT) for the 1999 contract and Waikato -1.0 m AHD: printed p.4; 2001 top-up -1.0 m LAT, water depth over the crest ~0.3 m at -1.0 LAT and ~1 m at -1.5 LAT: printed p.9; 408 bags 20 m long, 3-4.5 m diameter: printed p.4; "takeoff area is 300 m offshore": printed p.1; Fig 13 (scale bar, surf tracks) printed p.11 (PDF page 12).
- Jackson, Tomlinson, Corbett, Strauss 2012 (ICCE 33): p.3 450 containers, 42 in three campaigns, 2004 modification (weir + flared wings), Figs 2-3; p.4 Fig 4 (2002/03, 2004, 2006 plans + campaign table) and Fig 5; p.5 Figs 6-7 (2004 and 2011 aerials; design contours on the 2011 aerial), seabed burial; p.6 settlement (weir containers lowered up to 2 m, 1.5 m below design; flare containers 1-1.5 m); p.7 Fig 9 (T2 on 2 x T4 slumping sketch); p.13 "crest about 1-1.5 m below low tide".
- Seabed -4/-5, -6 to -8, -9/-10 m AHD and design reef between the -2 and -10.4 m AHD contours: Vieira da Silva 2021 Fig 3 (img-31) and text pp.5, 7.
- MSQ: AHD = LAT + 0.760 (Standard port datum levels 2014, Gold Coast Seaway); MSL 0.88, HAT 2.03, MHWS 1.53, MHWN 1.24, MLWN 0.51, MLWS 0.22 (Semidiurnal tidal planes 2026): REPORT.md section 3 (urls in its section 10).
- Renewal: City of Gold Coast (2020) archived page (84 containers, "minor changes made to the shape", QGHL physical modelling): REPORT 6.2; two options "previous design shape" vs "amended shape": Corbett et al. 2023 (not opened).
- Navionics: img-50..53 (accessed 2026-10-06, maps.garmin.com/en-US/marine). Council layer: s1 (data-goldcoast.opendata.arcgis.com, OBJECTID 4637).

## 9. GEMINI SOURCE VERDICTS (Gemini folder read-only; nothing from it used)
- Black & Mead 2001 JCR SI 29 pp.115-130 (title "Design of the Gold Coast reef for surfing, beach amenity and surfing aspects"): unverifiable (paywalled; bibliographic data confirmed by web search only).
- Jackson et al. 2012 (icce-ojs-tamu.tdl.org/icce/article/view/6956): wrong_design_version - the paper shows two alongshore-adjacent arms with channel, weir and flared wings, no inshore/offshore lobes, no 400 x 220 m.
- ICM case study / webinar (Salyer 2025): dimension_not_in_source (images only).
- Swellnet 2017-11-07: correct as a depth quote (2.5-2.6 m at low tide) but not a plan source; Gemini's crest 2.2 m equals Vieira 2021's measured -2.2 m AHD.
- Gemini's "180 m offshore" = the inshore lobe only (its own audit); ours: 212 m nearest edge, 288 m centroid.

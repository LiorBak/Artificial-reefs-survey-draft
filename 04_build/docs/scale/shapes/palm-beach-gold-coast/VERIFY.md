# VERIFY - palm-beach-gold-coast (adversarial verification, 2026-10-04 run; started per orchestrator brief)

Checks appended one by one below.

## Run notes (2026-10-05, verifier continuing; heading existed from earlier cut-off run, no checks had been recorded)
Files read: METHOD.md, sources.md, shape.json (status "traced"), SHAPE_SPEC.md, tools README. METHOD.md does NOT use geom.py make-canonical (canonical block was computed with a local azimuthal-equidistant projection in scratch code) -> TOOL BUG check = recompute independently (check 3).

### Check 1a - viewed s7 source and the existing s7 overlay (first look)
- Source bluecoast_AR_aerial_Nearmaps.jpg (2079x1386): vertical aerial, ~10 nested grey contour lines, dark rock mound, N arrow vertical, 0-25-50 m bar, boat at NE, mosaic seam at y~185.
- Existing overlay s7_bluecoast_aerial_trace.png: red outline sits on the OUTERMOST grey contour all the way round (NW corner, N edge, E end, S edge). The outermost line has a slight step on the N edge near x~1270 and a doubled line on the E/SE side (two lines ~20 px apart); the trace takes the outer one. Inner red slot sits on the innermost contour, parallel to the others.

### Check 1 - overlays viewed (existing PNGs AND my own re-render from shape.json with overlay.py render + 3-5x zooms drawn by my own crop script)
- s7 (primary, Bluecoast/Nearmap aerial). Re-rendered the 47-vertex outer polygon and 8-vertex slot from shape.json pixel_polygons. Zooms of the E end, SE corner, N edge, NW corner, W end and S edge: the red outline lies ON the outermost grey
  contour line in every zoom (offset < ~2 px = 0.25 m except the NW corner, where two near-parallel outer lines exist and the outline sits on the outer one). On the N edge and the E/SE side the outermost line is doubled (a second
  line a few metres inside); the trace correctly takes the outer. The N-edge step near px (1310,395) is in the contour itself, not a trace error. 8-vertex slot: sits on the innermost closed contour (long edges within 1-2 px, rounded E end
  cut off ~3 px = 0.4 m inside). VERDICT s7: GOOD.
  Note for the page: the outer contour is a drawn survey/design line, not the rock edge. Along the N/NW edge the dark rock stops 3-4 m inside the line; along the S/SE edge the dark rock spills ~2-3 m beyond it.
- s4 (ICCE Fig 1 icon). Outer 32-vertex polygon hugs the icon's dark rim all round (5x zoom); the 11-vertex 'pale band' polygon is a loose trace of a soft gradient (the icon is a shaded render, no hard edge) and cuts the band's tail
  by a few px. VERDICT s4: outline GOOD, inner band APPROXIMATE (the band is not used for any number).
- s2 (Esri z19 visible rock). Percentile-stretched view of the dark patch with the 86-vertex polygon on top: the polygon follows the dark core, but leaves out a darker-than-water halo of ~4-8 m on the N side of the W head and
  along the N edge (the polygon is a conservative 'core' outline). VERDICT s2: APPROXIMATE (cross-check only; 3,443 m2 is a lower bound for the visible patch; METHOD already gives 2,805-3,773 m2 for thresholds 14-18).
- composite overlay: yellow council outline + red Esri patch on the Nearmap aerial: council outline matches the outer contour (visually identical); the Esri patch sits in the SW half of the mound, parallel to the contours.
  Esri sees only the shoreward (shallower) half, the offshore/NE half is dark water in Esri but clearly rock in the Nearmap aerial - consistent with depth-limited visibility, NOT an offset (checked numerically below).
OVERALL overlay_match = good (primary outline), approximate (Esri patch and ICCE inner band, both cross-checks only).

### Check 3 (part 1) - scale, area, bbox, angles recomputed; tool-bug check (my own scripts, shapely/scipy/pyproj; scratch in session scratchpad)
- SCALE BAR re-measured by pixel scan of rows 1168-1192: white tick lines at x = 25-27 (0 m), 238-240 (25 m), 450-452 (50 m) -> centres 26.0 / 239.0 / 451.0; 25 m = 213 and 212 px, 50 m = 425 px -> 8.50 px/m (+-0.02). CONFIRMED.
- SCALE and NORTH independent of the bar/arrow: free similarity fit of the s7 outline (8.5 px/m, north-up, y flipped) to the council polygon (EPSG:28356, 153 vertices, AREA_SQM 11,941.7):
  isotropic: scale 0.9989, rotation 0.0002 deg, IoU 0.9969; ANISOTROPIC (sx, sy free): sx 1.0000, sy 0.9979, rotation -0.037 deg, IoU 0.9972 -> no stretch, north-up exact.
  Centroid-aligned (rotation 0): IoU 0.9963, Hausdorff 0.55 m. The tracer's figures reproduce.
  Caveat: the council polygon and the Bluecoast contours almost certainly come from the same survey/design CAD, so this proves the aerial's scale and orientation (a hard metric check) and the position, not an independent as-built check of the rock.
- Area / extent recomputed with shapely from shape.json s7 pixel polygon at 8.5 px/m: area 11,972.5 m2 (json 11,972), bbox 161.8 x 100.6 m, oriented rectangle 162.3 x 91.3 m, long-axis bearing 109.63 deg true-up (json 109.6). Council oriented rectangle 162.3 x 90.9 m.
  Scale sensitivity: 8.46 -> 12,086 m2, 8.54 -> 11,861 m2 (+-1 %).
- TOOL BUG: METHOD.md never uses geom.py make-canonical/px2m. I recomputed the canonical polygon from scratch with an explicit rotation (x = dE*sin(b)+dN*cos(b), y = dE*sin(b+90)+dN*cos(b+90)+centroid_offset, b = 334.3 deg):
  all 47 vertices agree with shape.json canonical.polygons_m to a CONSTANT 0.30 m (y only; the json centroid sits at y = 304.7, not the 305.0 quoted - rounding of the origin). Extents x -67.6..69.2 (identical), y 225.3..374.5 (json 225.0..374.2).
  Hand check of vertex 0: px (1826.3, 699.1); centroid px (1192.99, 739.94); dE = +74.507 m, dN = +4.805 m; x = 74.507*(-0.43366)+4.805*0.90108 = -27.98 m; y = 74.507*0.90108+4.805*0.43366+305.0 = 374.22 m;
  json canonical[0] = (-27.98, 373.92). Matches (x exactly, y within the 0.30 m origin rounding). The buggy +phi rotation (error 2*phi = 2*24.4 deg here) is NOT present: a +phi error would have moved this vertex by tens of metres.
  Handedness: ux = 334.3 deg, uy = 64.3 deg, cross(ux,uy) = -1 -> x then y runs clockwise on a north-up map; draw with +x to the right and +y pointing DOWN the screen (shore at the top); drawing with y up would mirror the reef.
- Grid convergence of MGA56 here is -0.22 deg (pyproj): true bearings of the long axis are grid +-0.22 -> 109.6-109.9 deg; negligible against the +-2 deg shoreline uncertainty. geo.polygons_latlon vs the council polygon converted to WGS84: Hausdorff 0.63 m, IoU 0.9953.
- SHORELINE direction (the 334.3 deg value, re-tested two independent ways):
  (a) my own waterline from Esri z18 (indicator R-(B+G)/2 smoothed, rightmost sand pixel per row at 20 px step, RANSAC 8 m): 37 inliers of 56, grid bearing 335.3 deg (tracer 334.3), rms 3.3 m; toe distance to this line 228.3..378.3 m, centroid 311 m (tracer 225/374/305).
  (b) OpenStreetMap coastline way 591135103 (Overpass, natural=coastline, within 1.2 km): bearing 336.5-338.6 deg (coarse: 6 vertices within 600 m); reef toe is 279-432 m from it, centroid 361 m.
  => shoreline 334-339 deg; the 334.3 +-2 deg in shape.json is fine; reef long axis (109.6) is 45-46 deg to the shore either way. The OSM line (which is the vegetation/dune-toe coastline) puts the nearest toe at 279 m, i.e. the quoted
  'approx. 270 m offshore' is measured from the beach/dune edge, not the waterline (225 m): that explains the 270-vs-225 difference (supports the existing comment).

### Check 3 (part 2) - Esri patch, s4 scale, council layer re-query (all recomputed today)
- s2: Esri px polygon -> lat/lon (own Web-Mercator interpolation from the sidecar bounds) -> EPSG:28356: area 3,441 m2 (json 3,443), oriented rectangle 120.6 x 41.2 m, grid bearing 105.0 deg; lat/lon agree with shape.json to 0.01 m.
  100 % of the patch lies inside the council polygon; still 100 % for shifts of 5 m in any direction, >=96.7 % for 10 m, 78-100 % for 15 m. Patch/council area 0.288; centroid 19.2 m W and 12.1 m S of the council centroid. Smoothed darkness
  thresholds 12/14/16/18/20/24 give 2,280 / 2,935 / 3,489 / 3,830 / 4,099 / 4,486 m2 (19-38 % of the toe footprint). The traced 3,443 m2 (29 %) is a mid value; the 'Esri shows ~29 %' statement is now given as a 25-38 % range.
  Reason for partial visibility is NOT proven: it is consistent with depth/clarity (the patch is the shoreward, shallower, side; Esri water darkens toward the NE) but could also reflect colour/turbidity; the page should say 'only part of the mound is visible on satellite'.
- s4 (ICCE Fig 1) scale: re-ran geom.py fit-similarity on the 4 recorded control pairs -> scale 1.9285 Esri px per fig px, rotation 0.71 deg, rms 4.7 Esri px (reproduced). Looked at all four landmark pairs side by side at 4-5x
  (groyne tip, 19th Ave tower, blue-roofed and red-roofed buildings): all four are the same objects; the tower point is the weakest (leaning tower, different look angle). Automatic SIFT matching between the two images failed
  (different dates and resolution, <=4 inliers) so no automatic confirmation. Uncertainty +-3 % kept. Independent consistency: icon area 12,017 m2 vs council 11,942 m2 (0.6 %).
- s1 re-query: live FeatureServer OBJECTID 4638 (outSR 28356) = 154 vertices (153 distinct), identical to the saved raw file (max coordinate difference 0.00 m). Layer editingInfo: dataLastEditDate 2026-10-03 17:35 UTC (whole layer touched; polygon unchanged vs the 2026-10-04 pull).
  Layer/service description: 'lines and polygons indicating the location of the artificial reefs' - NO statement of how the polygon was surveyed (as-built vs design). Attributes: BOULDER, INSV, LENGTH_M 160, WIDTH_M 80, HEIGHT_M 5, VOLUME 33,000, AREA_SQM 11,941.7.
- Overlays regenerated in place: s2_esri_z19_visible_patch_red_vs_council_cyan.png (old version had ~240 piled-up vertex numbers; new one is a cropped, brightened view with legend, scale bar, north arrow) and
  composite_s7_aerial_with_council_polygon_yellow_and_esri_visible_rock_red.png (re-drawn from the raw council geojson + the s2 pixel polygon through the s2 georeference; larger legend). s7 and s4 overlays kept as they were (verified good).

### Check 2 - design version (re-opened every source)
- Which state is drawn: the reef AS BUILT in 2019 - toe footprint = outer contour of the Bluecoast/Nearmap aerial = City of Gold Coast asset polygon (OBJECTID 4638, GIS_USER_STATUS INSV, BOULDER) - plus the innermost contour (59 x 6 m, 104.8 deg).
- Evidence it is the built, latest state: EPW Sept 2020 pp.50-51 (s8, page image re-viewed): built May-Sept 2019 by a Hall/Heron joint venture, 60,000 t, "approximately 270 metres offshore from Nineteenth Avenue", footprint 160 x 80 m, structure certified Sept 2019, later condition "comparable to the 'as constructed' RPEQ certification report";
  the June-2020 oblique photo shows the dark rounded oval mound. ICCE 2022 Fig 4 = final multibeam survey, same rounded mound. Prenzler et al. (ICCE 2022 abstract, re-read from the PDF): "stable with insignificant movement or settlement", crest 1.5 m below MSL, 6-8 t armour.
- Superseded designs: Mortensen et al. 2015 concept SCS A/B/C (re-read PDF text and Table 2): SCS B = crest 60 m, 53,319 m3, footprint 21,394 m2 (figure label), max width 144 m, max length 175 m, orientation 105 deg, offshore toe 560 m offshore in 11.4 m depth;
  Raised Water Research page: "moving the reef 50m closer to shore to save rock volume", figure "Design on the left, results on the right" (concept vs multibeam survey; saved as s9). The 144 m / 330 m on Royal HaskoningDHV's page (re-fetched) = concept width, not the built reef.
- Later change / extension / damage / removal: searched (monitoring, top-up, repair, extension, cyclone Alfred March 2025). Found NOTHING. Monitoring to 2023 says stable; search summaries say the beach and reef held up through Alfred (not read at source, treated as hearsay);
  the Esri imagery of 2025-12-01 (nine months after Alfred) still shows the dark mound inside the council polygon. The council layer was re-edited 2026-10-03 but the polygon is identical to the one traced.
- Not resolvable from any source: whether the aerial's grey contour lines are as-surveyed or design lines (the Bluecoast page is a bare gallery with no caption), and the aerial's date. Mitigation: the outer line equals the council asset polygon (IoU 0.996) and the dark rock agrees with it within 3-4 m, so for a footprint drawing the two readings differ by a few metres at most.
- The page must say: "Drawing = the reef as built in 2019; the 2014-15 concept was larger and further offshore; no later change reported." (stored in shape.json design_version.page_note).
VERDICT: the drawn state is correct and is the latest known. PASS.

### Check 4 - dimensions vs text (rubric tolerance ~10 %)
| quantity | text | drawing | diff | verdict |
|---|---|---|---|---|
| length (long axis) | 160 m (council, EPW, card, RWR) | 162.3 m oriented rectangle (163.2 m max vertex distance) | +1.4 % | agrees |
| footprint area | 11,941.7 m2 (council) | 11,972 m2 | +0.25 % | agrees |
| area vs 160 x 80 rectangle | 12,800 m2 | 11,972 m2 | -6.5 % | agrees |
| width | 80 m | 91.3 m max (oriented), 73.8 m mean (area/length), 100.6 m N-S extent | +14 % / -8 % | 80 m is nominal (the council's own polygon: 90.9 m oriented width, 73.6 m mean); the drawing is not wrong; stated on the page |
| offshore distance | ~270 m (EPW, ICCE Fig 1, RWR); 330 m (RHDHV) | toe 225 / centroid 305 / far toe 374 m from the 2025 waterline (my fit: 228 / 311 / 378); from the OSM coastline 279 / 361 / 432 m | -17 % vs waterline, +3 % vs OSM coastline | the text is measured from the beach (Fig 1 arrow ends on dry sand); not a conflict. RHDHV 330 m / 144 m = concept |
| orientation | concept crest 105 deg true | slot 104.8 deg (grid; +-0.2 true), outline 109.6, Esri patch 105.0 | n/a | agrees |
| crest length | concept 60 m | slot 59.2 m | -1.3 % | agrees |
| volume | 25,000 m3 (card) / 33,000 (council) / 60,000 t | not measurable from a plan | n/a | sources disagree; not drawn |
Where text and drawing differ, the text is the nominal or differently-measured one ("80 m wide" is a rounded design figure; "270 m" is from the beach edge); the drawing is right.

### Check 5 - provenance
- Every source row has url, source page, page/figure, date, credit and licence (s1-s9). Fixes: added s9 (new context figure with full provenance), s8 Issuu link marked dead (404) with the Bluecoast-hosted image as the evidence, s7 local-file vs CDN byte difference documented,
  s1 "last edited 2026-10-03" and "survey basis not stated" added. Licences re-confirmed: s1 CC BY 3.0 (item licenseInfo), s4 CC BY 4.0 (article page).
- METHOD.md numbers: scale-bar ticks, north arrow, IoU, areas, bbox, oriented rectangle, shoreline fit, ICCE control points, council attributes - all re-derived today (checks 3, 3b, 3c). Unsourced number found: "~25,000 m3" (from the card; the council says 33,000) - marked unresolved.
  Also: METHOD said the Esri patch covers "~29 %" - now "19-38 % depending on threshold"; METHOD called Gemini's 25,000 m3 correct - not confirmed.

### Check 6 - Gemini findings (re-fetched everything; nothing from Gemini used as input)
Read from the Gemini folder (read-only): 02_world_reefs_data/reef_footprints.json (palm_beach entry), 05_web_build/images/IMAGE_PROVENANCE.md, 05_web_build/images_provenance.json, reef_footprint_scale_analysis.md.
1. "City of Gold Coast: Palm Beach Shoreline Project Monitoring (2021)" - no URL. The nearest real document is Prenzler et al., ICCE 2022 abstract (published 2023), not a 2021 City document. Tracer verdict unverifiable: CONFIRMED.
2. "Royal HaskoningDHV: Palm Beach Artificial Reef Design Summary (2019)" - no URL. The Haskoning project page exists (re-fetched) but gives 144 m / 330 m (concept values) and no design summary. unverifiable: CONFIRMED.
3. "Swellnet: Palm Beach Reef Surfing Evaluation (2020)" - no URL. Swellnet 2019-07-29 "First impressions at the Palm Beach Artificial Reef" exists; a Bluecoast 2020-07-20 news item says Swellnet installed the Wave Peel Tracking camera; no document of that title. unverifiable: CONFIRMED.
4. https://www.bluecoastconsulting.com.au/assets/images/palm-beach-reef.jpg - HTTP 404 today. dead: CONFIRMED. The live Bluecoast page https://www.bluecoastconsulting.com.au/artificialreefs hosts the real plan-view aerial (our s7).
5. Coordinates -28.1181, 153.4732 "11th Avenue" - 1,214 m (pyproj, EPSG:28356) from the council polygon centroid; Esri z18 (2025-12-01) at that point shows beach and surf zone, a groyne to the north and no offshore structure within 450 m. wrong_site: CONFIRMED (it also puts the reef at the waterline, contradicting its own "270 m offshore").
6. Polygon (9 vertices, alongshore chevron, 9,100 m2 net) and shoreline 345 deg: no source image. IoU with the traced outline in the canonical frame, centroid-aligned: 0.41 (0.52 with a mirror flip, so the tracer's 0.52 reproduces); 0.75 at best after rotating it by -60 deg.
   Not overturned. Nuance: Gemini's footprint is roughly the right size but oriented alongshore, while the plan shows a ~45 deg skew. Its shoreline 345 deg vs measured 334-339 deg.
NEW (not on the tracer's list): 7. Gemini's field photo (Wikimedia Commons "Palm Beach, Queensland, Australia.jpg", labelled CC BY-SA 3.0, caption "...fronting the 2019 submerged rock reef") is a February 1967 photograph by Jack Bain (QUT), CC BY 4.0 - it cannot show the reef.
8. Gemini's "Bluecoast (2020) Palm Beach Artificial Reef Monitoring & Review" - no URL, unverifiable. 9. height 8.5 m / crest width 24 m / volume 25,000 m3 / footprint 12,800 m2: the council register says HEIGHT_M 5, VOLUME 33,000; 12,800 = 160 x 80; the 24 m crest width is in no source.

### Check 7 - confidence level and reason
Rubric: high = structure clearly visible on geo-referenced imagery OR an as-built survey with a scale, and dimensions within ~10 % of text.
- Structure clearly visible: yes, on a scaled plan-view aerial (not geo-referenced but pinned by the council vector), and partly (19-38 %) on geo-referenced Esri imagery. Scale and orientation hard-checked against metric data.
- Dimensions: length +1.4 %, area +0.25 % vs council / -6.5 % vs 160 x 80; the width label disagrees (+14 % max, -8 % mean) because it is nominal; the offshore distance is explained.
- Caveats that could argue for "medium": aerial undated, contour basis unlabelled, council polygon and contours probably the same dataset (not independent), Esri shows only part. None moves the outline by more than a few metres (rock edge vs contour 3-4 m; the independent ICCE icon agrees: +0.6 % area, 162 x 92 m).
VERDICT: "high" retained; the reason text in shape.json was rewritten to state these caveats in plain words.

## FINAL STATUS
shape.json: status "verified", verified_on "2026-10-04" (as the brief instructs), verification[] has 9 entries, confidence high, overlay_match good for the primary outline.
Files changed: shape.json, METHOD.md (Step 5 addendum), sources.md (s9 + notes), VERIFY.md, overlays/s2_esri_z19_visible_patch_red_vs_council_cyan.png, overlays/composite_s7_aerial_with_council_polygon_yellow_and_esri_visible_rock_red.png, src/rwr_design_vs_constructed_641x187.jpg (new).

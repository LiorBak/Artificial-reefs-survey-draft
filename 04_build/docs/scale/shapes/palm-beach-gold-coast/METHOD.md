# METHOD log - palm-beach-gold-coast

Run started 2026-10-05

(Appended step by step. Earlier-run leftovers in src\ and overlays\ are treated as unverified notes until their origin is re-established.)

## Step 0 - inspect folder (2026-10-05)
Found at start: overlays\pb_official_overlay.png; src\ with gc_opendata_artificial_reef_raw.geojson, pb_canonical_polygon_m.json,
pb_context_z18.png(+geo), pb_official_latlon.json, pb_official_pixpoly.json, pb_offshore_check.png(+geo), pb_sat_z19.png(+geo),
wide_overview.png(+geo), zoom_pointA/B/B2/B3.png, zoom_waterline_near_centroid.png, zoom_waterline_south.png. No sources.md, no shape.json, no METHOD.md.

## Step 1a - reviewed leftovers + card (2026-10-05)
- gc_opendata_artificial_reef_raw.geojson (EPSG:28356, 11 features): feature 4638 = City of Gold Coast "ARTIFICIAL_REEF", material BOULDER, LENGTH_M 160, WIDTH_M 80,
  AREA_SQM 11941.7, FUNCTIONAL_LOC Y-BEACH-PALMBEA (our Palm Beach reef). Feature 4637 = Narrowneck (geotextile). Origin URL not recorded by earlier run -> must re-find.
- Card 02_research/reefs/palm-beach-gold-coast.json has lat/lon null; earlier text-derived footprint (07_scale/reefs) is a 160x80 m schematic mound, area 9678 m2.

## Step 1b - viewed earlier overlay (2026-10-05)
Viewed overlays/pb_official_overlay.png (earlier run; unverified note): official GC open-data polygon (154 vertices) drawn on Esri World Imagery z19 (capture 2025-12-01 per sidecar). Polygon sits over a lighter-green
patch of seabed with a darker band; no hard-edged rock structure visible at this depth - to re-judge myself below. Provenance (URL) of the geojson not recorded -> searching.

## Step 1c - re-established origin of the council polygon (2026-10-05)
- Dataset: City of Gold Coast Open Data "Artificial Reef" (ArcGIS Hub item c9d0b521374740cc9e9561b04c453736_0), page https://data-goldcoast.opendata.arcgis.com/datasets/c9d0b521374740cc9e9561b04c453736_0 (about: https://hub.arcgis.com/datasets/c9d0b521374740cc9e9561b04c453736_0/about);
  service https://services.arcgis.com/3vStCH7NDoBOZ5zn/arcgis/rest/services/Artificial_Reef/FeatureServer/0 ; owner opendata_goldcoast; license CC-BY-3.0 (Creative Commons Attribution 3.0 Unported); 11 records; credit "City of Gold Coast".
- Re-queried today (OBJECTID=4638, outSR=4326 geojson and outSR=28356): 154-vertex polygon, identical to the earlier-run raw file (coords match within 0.01 m). Attributes: BOULDER, LENGTH_M 160, WIDTH_M 80, AREA_SQM 11941.7,
  HEIGHT_M 5, VOLUME 33000, FUNCTIONAL_LOC Y-BEACH-PALMBEA, GIS_USER_STATUS INSV. Layer metadata has no statement of how the polygon was surveyed (as-built vs design) - to be judged against imagery.
- Verdict on leftover raw geojson: origin now traced -> KEEP (sources row s1).

## Step 1d - looked at the leftover satellite images myself (2026-10-05)
- src/pb_context_z18.png (Esri World Imagery z18, 0.527 m/px, bounds in .geo.json, capture 2025-12-01 per Esri identify): at ~(2200,1250) px there is ONE clearly visible, sharp-edged DARK elongated patch ~270-290 m off the
  beach = the built boulder reef (position coincides with council polygon centroid -28.1073, 153.4709). A second, scattered dark-spot cluster ~300 m up-coast at ~(1500,580) is natural reef / scattered rock (not our reef).
- src/pb_sat_z19.png (z19, 0.263 m/px, 1519 px, bounds in .geo.json): the dark patch is crisp. Visible patch spans roughly x 440-900, y 660-920 px (~120 x 70 m bbox) whereas the council polygon spans ~163 x 99 m bbox
  (x 420-1040, y 572-950) -> the council polygon is LARGER than the dark patch (probably toe/footprint incl. rock apron, or design footprint). To be quantified below.
- Verdict: pb_sat_z19.png and pb_context_z18.png = Esri World Imagery (tile template in the sidecars), origin re-established -> KEEP. Derived crops (wide_overview, pb_offshore_check, zoom_*) and derived json
  notes (pb_official_latlon/pixpoly, pb_canonical_polygon_m) have no independent origin -> to be deleted after I regenerate what I need.

## Step 2a - first segmentation + contrast-stretched view of s2 (2026-10-05)
- Gaussian-smoothed (sigma 1.5 px) luminance of src/pb_sat_z19.png; reef = connected dark component containing px (700,790). Thresholds lum<11..18 give a bbox ~ x 448-890, y 697-917 px
  (= 116 x 58 m axis-aligned), area 2,900-3,800 m2 depending on threshold (lum<14: 42,311 px = 2,935 m2). The patch merges with the deep dark water to the east at higher thresholds (>=20), so a threshold alone cannot give the east/north-east boundary.
- Per-channel percentile stretch + gamma 0.45 of the crop x330-1130,y480-1030 (scratch image in %TEMP%) shows the reef clearly: an elongated rock mound with a bulbous WEST head (around px 440-560, 700-830) and a tail
  running ESE to a blunt east end (~x 880, y 880). Long axis ~130 m, width ~55-60 m on the imagery. Water east of ~x 900 is deep/dark so rock there would be invisible.
- Council polygon (s1) in the same frame: bbox 163 x 99 m, area 11,942 m2, a smooth E-W oval. It hugs the visible rock on the W and S sides but extends ~35 m NORTH and ~40 m EAST of the visible rock -> the council polygon is NOT a tight outline of the visible
  structure (looks like a generalised "160 x 80" design/asset envelope). Both facts recorded; primary trace = visible rock outline (s2); s1 = cross-check envelope.

## Step 1e - web search for design / as-built plan figures (2026-10-05)
Searched: "Palm Beach artificial reef design plan view ... DHI Mortensen / ICCE / Coasts and Ports"; "icce-ojs.tamu.edu Palm Beach artificial reef monitoring". Found and downloaded:
1. Hunt, Britton, Messiter, Prenzler, Knight, Watterson (2022/23) "Palm Beach Shoreline Project: Innovative Coastal Management Solution", 37th ICCE, Coastal Engineering Proceedings,
   DOI 10.9753/icce.v37.management.66, https://icce-ojs-tamu.tdl.org/icce/article/view/13024 (download .../download/13024/12297 = a .docx). CC BY 4.0. Contains
   Fig 1 "Location and orientation of the artificial reef" (aerial photo + schematic reef icon, N arrow, "Approx. 270m" arrow, 21st Avenue groyne) -> saved src/icce13024_fig1_location_orientation.jpeg (1459x777);
   Fig 4 "Final survey of the completed reef structure" (oblique 3D multibeam, 1029x501, NOT a plan view) -> saved src/icce13024_fig4_final_survey.png.
2. Mortensen, Hibberd, Kaergaard, Kristensen, Deigaard, Hunt (2015) "Concept Design of a Multipurpose Submerged Control Structure for Palm Beach, Gold Coast", Australasian Coasts & Ports 2015,
   https://www.dhigroup.com/upload/publications/coastsea/Mortensen_2015.pdf . Fig 3 = CONCEPT design "SCS B": oblique 3D, max length 175 m, max width 144 m, footprint 21,394 m2, volume 53,319 m3,
   crest -1.5 m, orientation 105 deg, offshore toe 560 m offshore in 11.4 m depth -> a larger, further-offshore concept that was NOT built (built reef is ~270 m offshore, ~25,000 m3). Saved the figure
   as src/mortensen2015_fig3_concept_SCS_B.png as the "alternative design seen" (context only, oblique, not traced).
3. ICCE 12921 "Monitoring of the Palm Beach Artificial Reef" (Prenzler et al., 2-page abstract): text only - basalt/greenstone, 4 rock classes, crest 1.5 m below MSL with 6-8 t rocks, inspections show stable, insignificant movement or settlement. No plan figure.
Gives design-version evidence: reef built = detailed design (Royal HaskoningDHV Design Reference Report), "refined the location and dimensions" vs the 2015 concept; final survey Fig 4 shows it built.

## Step 1f - Gemini's sources checked (read-only), found a plan-view aerial (2026-10-05)
Gemini's reef_footprints.json entry for Palm Beach: 3 citations with NO URLs: "City of Gold Coast: Palm Beach Shoreline Project Monitoring (2021)", "Royal HaskoningDHV: Palm Beach Artificial Reef Design Summary (2019)",
"Swellnet: Palm Beach Reef Surfing Evaluation (2020)" -> titles not matching any document I could find (closest real ones: ICCE 2022 monitoring paper by Prenzler et al.; RHDHV project page; Swellnet 2019 articles) -> verdict unverifiable.
Gemini image provenance row for this reef: https://www.bluecoastconsulting.com.au/assets/images/palm-beach-reef.jpg -> fetched: HTTP 404 -> dead. Gemini coordinates (-28.1181, 153.4732, "11th Avenue") are ~1.2 km SSE of the council polygon
(-28.1073, 153.4709; 19th Ave) -> wrong site; Gemini polygon is a 9-vertex chevron 160x80 "apex seaward" - an invention (no source image), see gemini_checks in shape.json.
Fetched the page Gemini was pointing at (Bluecoast "Artificial Reefs for Coastal Protection and Amenity" https://www.bluecoastconsulting.com.au/artificialreefs): it hosts AR_aerial_Nearmaps.jpg = a vertical Nearmap aerial of the reef with
survey/design contour lines, north arrow and a 0-25-50 m scale bar (2079x1386). BEST plan-view source found -> saved src/bluecoast_AR_aerial_Nearmaps.jpg (s7). Also saved the page's image of EPW (IPWEAQ) Sept 2020 pp.50-51 (s8): text says
"built approximately 270 metres offshore from Nineteenth Avenue ... reef footprint is 160 metres long, 80 metres wide and is 1.5 metres below the average water level at its highest point"; includes oblique June-2020 photo showing the dark oval rock mound.
Other Bluecoast page images (barge dumping photos, CFD still, Albany render) are not plan views -> not kept.
Plan: PRIMARY = s7 (scale bar + north arrow; outer contour = toe footprint; rock visible as dark mound); CROSS-CHECKS = s2 (Esri z19, georeferenced; shows visible upper mound) and s4 (ICCE Fig 1 schematic on aerial). Council polygon s1 compared numerically.

## Step 2b - PRIMARY image s7 (Bluecoast / Nearmap aerial): scale, orientation, trace (2026-10-05)
Image src/bluecoast_AR_aerial_Nearmaps.jpg, 2079 x 1386 px. Contains: vertical aerial of the reef, 10 grey contour lines (outer = toe footprint; inner ones step in toward a rounded-rectangle crest slot),
N arrow, scale bar 0-25-50 m, a small boat (NE), and a mosaic seam across the top (y~185).
- SCALE (method: scale bar). Pixel evidence: white tick lines of the bar at x = 26 (0 m), 239 (25 m), 451 (50 m) [found by scanning row 1162/1198 for lum>225; bar black fill x 29-236]. 25 m = 213 px, 50 m = 425 px
  -> 8.50 px/m (0.1176 m/px); resolution error +-1 px on 425 = +-0.25 %. Quoted scale uncertainty +-1 % (bar drawing + image resampling).
- ORIENTATION (method: north arrow). Zoomed the arrow: tip (214,943), notch (214,1016), base corners (165,1063)/(258,1063) -> arrow axis vertical => north is up, rotation 0 +-1 deg.
- TRACE of the OUTER contour line (the toe outline). Method: top-hat filter (R - grey_opening 9x9 > 28) to isolate the thin grey contour lines, remove components <1500 px (noise/foam), then cast 360 rays from (1130,760) and
  take the outermost line pixel on each ray; 5-degree median smoothing of radius; Douglas-Peucker 2.5 px (0.3 m) -> 47 vertices. Checked visually on an overlay (yellow points sit on the outer grey line all the way round).
  Result: bbox 1375 x 855 px = 161.8 x 100.6 m (axis-aligned, north-up); area 865,900 px2 = 11,972 m2 (simplified polygon).
- CROSS-CHECK against council polygon s1 (EPSG:28356 vector, 154 vertices, AREA_SQM 11,941.7): shapely IoU = 0.996 with centroid alignment only (rotation 0); IoU falls to 0.97 at +-2 deg and to 0.94 at +-3 % scale ->
  the best-fit rotation is 0.0 deg and the best-fit scale 1.00 (both found by free search, independent of the north arrow and scale bar); Hausdorff distance between the outlines 0.55 m. => the council polygon IS the survey toe outline
  drawn in the Bluecoast aerial; and the aerial's scale bar and north arrow are confirmed by the council's metric coordinates.
- Visible rock vs line: the dark rock fills the outline; along the N/NW edge the line lies ~3-4 m outside the dark rock, along the S/SE edge the dark rock spills ~2-3 m beyond the line (dark apron at ~x 850-1000,y 990-1010).
  So the line is the survey/design toe, rock cover agrees within a few metres.
- Image date unknown (no caption). Rock mound appears complete; a boat sits at the NE corner; page published ~Sept 2020, construction finished Sept 2019.

## Step 2c - second trace on s7: innermost contour; Esri trace of s2; shoreline; registration (2026-10-05)
- INNERMOST CONTOUR of s7 (a thin rounded slot): auto ray-cast failed at the W end (foam), so read 8 vertices by hand from 3x zoom grids: NW corner (636,724), top edge to (1105,848), rounded E end (1116,851),(1119,862),(1114,884),(1107,897),(1100,898),
  SW corner (623,772). Slot = 59.2 x 5.9 m, area 345 m2, axis bearing 104.8 deg true. (Contour values are NOT labelled on the image, so I do not call it "the crest"; the sources say crest = -1.5 m MSL.)
- s2 (Esri z19, georeferenced) trace of the VISIBLE DARK ROCK: Gaussian-smoothed luminance < 16 connected component at the reef (px 700,790), hole-filled; 2-degree ray polygon, DP 1.5 px -> 86 vertices;
  bbox 444-890 x 697-914 px, area 3,456 m2 (thresholds 14/16/18 give 2,805 / 3,456 / 3,773 m2). It is the upper part of the mound only (see below). Viewed on overlay: edge follows the dark patch.
- REGISTRATION s2 -> s1 -> s7: Esri px -> lon/lat via the .geo.json bounds (exact Web-Mercator interpolation, same maths as satellite.py) -> EPSG:28356 (pyproj). The Esri patch lies 100 % inside the council polygon
  and still >96 % inside when shifted by up to 5 m in any direction, so Esri imagery and council survey agree to ~5 m or better. Centroid of the patch is 19 m W and 12 m S of the polygon centroid
  (the visible rock is the SW/upper part: Esri sees only the shallower mound, Nearmap sees the whole rock apron). Drawn on s7 (composite overlay) the patch sits on the inner contours, parallel to them.
- s7 placement: best translation (+-3 m search, 0.25 m step) maximising IoU with the council polygon = 0,0 -> centroid-aligned, IoU 0.995 (true-north ENU about the polygon centroid). The aerial itself carries no coordinates:
  geographic position of the primary outline = position of the council polygon (rotation/scale from the aerial's own north arrow/scale bar, both confirmed by the fit).
- SHORELINE (from s3, Esri z18, georeferenced, 2025-12-01): per image row (every 25 px, y 700-1800) took the right-most contiguous sand-coloured run (R>=G-3, R>120, B<R-12, opened 2x) = sand/water edge; 44 points;
  RANSAC line (2000 trials, inlier tol 12 px) -> 30 inliers; converted to ENU and fitted by SVD: direction toward NNW = bearing 334.3 deg true (shore normal toward ENE = 64.3 deg), rms 3.4 m over a 578 m stretch.
  Outliers (14 pts) are at the groyne and where a rip/foam band pushes the sand mask seaward. Uncertainty of the bearing ~ +-2 deg (the waterline is wavy and tide-dependent).
  Canonical origin = foot of the perpendicular from the reef-outline centroid onto this line (lat/lon in shape.json).
- RESULTS (primary outline, canonical frame x alongshore toward 334.3 deg, y offshore): alongshore extent -67.6..+69.2 m (136.7 m), cross-shore 225.0..374.2 m (149.2 m) -> nearest toe 225 m, centroid 305 m, farthest 374 m from the waterline;
  max vertex distance 163.2 m; oriented bounding rectangle 162.3 x 91.3 m with long axis bearing 109.6 deg (44.7 deg to the shoreline); area 11,972 m2 (council 11,942 m2).
  IMPORTANT correction to the earlier text-derived footprint: the 160 m axis is NOT alongshore - the mound is skewed ~45 deg to the shore (long axis ESE), as in the Mortensen concept (orientation 105 deg).

## Step 3 - shape.json written (status "traced") (2026-10-05)
Wrote shape.json from the primary s7 trace + the results above (canonical frame, geo polygon, angles, dimensions_check, gemini block, references). Checkpoint reached.
Remaining: trace s4 (ICCE Fig 1 schematic) as 2nd cross-check, copy final overlays, delete unused src files, finalise sources.md, add Wayback check if cheap.

## Step 2d - CROSS-CHECK 2: ICCE Fig 1 (s4) schematic icon, scaled by control points (2026-10-05)
- Image src/icce13024_fig1_location_orientation.jpeg (1459 x 777): aerial photo, N arrow (checked: vertical, 1410/40-118 px), labelled 21st Avenue groyne, "Approx. 270m" arrow, and a drawn reef icon (grey outline + pale band).
- No scale bar. SCALE method = known features: matched 4 landmarks between the figure and Esri z18 (s3): 21st Avenue groyne seaward tip fig (358,413) = z18 (1526,1168); tall tower with shadow at 19th Ave fig (309,690) = z18 (1425,1697);
  blue-roofed building fig (280,542) = z18 (1363,1410); red-roof building fig (245,542) = z18 (1298,1413). geom.py fit-similarity -> scale 1.9285 Esri px per figure px, rotation 0.7 deg (so the figure is north-up), rms residual 4.7 Esri px (~2.5 m).
  => 1.016 m per figure px. (A first attempt with 6 points incl. a mis-matched building gave rms 43 px and was discarded; the circular-complex point was also dropped, it disagreed by 7 %.)
- The "Approx. 270m" arrow (251 px) measures 255 m on this scale -> only approximate (-5 %); not used for scale.
- Trace: outer icon outline 32 vertices read from 5x zoom grid (overlays/s4_icce_fig1_icon_trace.png, viewed: follows the icon edge), pale band 11 vertices.
- Result in true metres: icon outline area 12,017 m2, oriented rectangle 162.3 x 92.5 m, long-axis bearing 110.8 deg, canonical extents x -62..74 m, y 218..365 m. Compared with s7: area +0.4 %, IoU 0.97 centroid-aligned (best rotation 0.0 deg), 0.84 with no alignment (offset 5 m alongshore, -9 m offshore).
  Conclusion: the icon is a faithful simplified outline of the built reef, independent of the Bluecoast aerial and the council GIS. It is a drawn symbol, so used only as a cross-check, not for vertices.
- s5 (ICCE Fig 4, oblique final-survey render) viewed, not traced: rounded rectangle with flat crest, consistent.
- s6 (Mortensen Fig 3, oblique concept render) viewed, not traced: different, larger design (see shape.json alternatives).

## Step 4 - cleanup, confidence, summary (2026-10-05)
- Deleted the earlier-run derived files with no independent origin (see sources.md notes). Kept: s1 geojson, s2 + s3 Esri crops (+sidecars), s4 Fig 1, s5 Fig 4, s6 Mortensen Fig 3, s7 Bluecoast aerial, s8 EPW pages.
- Final overlays in overlays\: s7_bluecoast_aerial_trace.png (primary trace, outer + inner contour), s2_esri_z19_visible_patch_red_vs_council_cyan.png, s4_icce_fig1_icon_trace.png,
  composite_s7_aerial_with_council_polygon_yellow_and_esri_visible_rock_red.png.
- CONFIDENCE = high. Reason: plan-view aerial with scale bar and north arrow; outline equals the City of Gold Coast GIS polygon (IoU 0.995, Hausdorff 0.55 m, area +0.25 %); an independent drawn icon (ICCE Fig 1) georeferenced with control points gives
  the same area (+0.4 %) and orientation; rock visible on georeferenced Esri imagery inside the polygon; length 162 m vs 160 m text. Weaker: width label 80 m vs 91 m max / 74 m mean; shoreline direction +-2 deg; aerial undated/ungeoreferenced.
- GEMINI: three named sources have no URL (unverifiable); image URL dead (404); coordinates 1.2 km off (wrong_site); polygon is an unsourced chevron aligned alongshore (IoU 0.52 vs traced outline); its 160 x 80 m / 270 m / 25,000 m3 figures are correct.
- Not done: Esri Wayback history (not needed - the reef is clearly visible in current imagery and the aerial); no oblique-photo tracing.
- Caveat for the page: the 160 m axis is skewed ~45 deg to the shore (long axis bearing ~105-110 deg, shoreline 154/334 deg). The earlier text-derived schematic had it alongshore - replace it.

## Step 5 - VERIFICATION addendum (2026-10-05, independent verifier; details in VERIFY.md)
Nothing above was deleted; these are the corrections and additions. Numbers are tied to the checks in VERIFY.md.
- Scale (step 2b): ticks re-measured at x = 26 / 239 / 451 (rows 1168-1192) = 8.50 px/m. A free anisotropic similarity fit of the traced outline to the council polygon gives sx 1.000, sy 0.998, rotation 0.04 deg, IoU 0.997.
- Canonical frame (step 2c): NOT made with geom.py make-canonical, so the 2026-10-05 rotation bug does not apply. An independent explicit rotation (x = dE sin b + dN cos b; y = dE sin(b+90) + dN cos(b+90) + 305.0, b = 334.3 deg) agrees with shape.json to a constant 0.30 m
  (the stored polygon centroid is at y = 304.7). Hand check of vertex 0 recorded in VERIFY.md. Handedness: draw with +y pointing down the screen.
- Shoreline direction: re-measured on Esri z18 (335.3 deg) and on the OSM coastline (336.5-338.6 deg); 334.3 +-2 deg kept. The OSM coastline puts the nearest toe at 279 m, which is how the text's "~270 m offshore" arises (beach/dune edge, not waterline).
- Esri patch (step 2c): "covers ~29 %" is now "about a quarter to a third (19-38 % for darkness thresholds 12-24)"; the traced 3,443 m2 is a mid, conservative value. The reason for partial visibility is not proven.
- Step 1e / step 4: "~25,000 m3" came from the project card; the council register says VOLUME 33,000 and EPW 2020 says 60,000 t. Treated as unresolved; not used for any drawing. Gemini's 25,000 m3 is therefore NOT confirmed "correct".
- Mortensen 2015 (step 1e): Table 2 columns are crest length / offshore depth / nearshore depth / volume / max width / max length. SCS B has a 60 m crest "oriented 105 to true north", which equals the 59.2 m x 5.9 m innermost contour at 104.8 deg (grid) in the aerial: the slot is very probably the design crest.
- Design evolution added: Raised Water Research (s9) shows the concept (175 x 144 m) beside the multibeam survey of the built reef and says the reef was moved 50 m closer to shore; Royal HaskoningDHV's "144 m wide, 330 m offshore" is the concept.
- No later change found: monitoring papers to 2023 report a stable structure; the rock is visible on Esri imagery of 2025-12-01. The aerial's contours are not labelled design/as-surveyed anywhere.
- Gemini checks (step 1f) re-done: image URL still 404; coordinates 1,214 m away (beach/surf zone on Esri); chevron IoU 0.41 (0.52 mirrored; 0.75 only after a -60 deg rotation); Gemini's field photo is a 1967 image (Commons, J. Bain); height 8.5 m, crest width 24 m and volume are not supported.
- Overlays: the s2 overlay and the composite overlay were regenerated (the old s2 overlay had ~240 piled-up vertex labels; both are now drawn from the raw council geojson and the s2 pixel polygon via the s2 georeference). The s7 and s4 overlays are unchanged.
- New file: src/rwr_design_vs_constructed_641x187.jpg (s9, context only).

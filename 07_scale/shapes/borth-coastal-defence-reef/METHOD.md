# METHOD - borth-coastal-defence-reef

Run started 2026-10-05

## Step 0 - resume inspection (2026-10-05)
- Folder had src\ (10 PNGs + .geo.json sidecars from satellite.py = Esri World Imagery / Wayback, provenance recoverable from sidecars: bounds, zoom, release, capture date, retrieved 2026-10-04) and overlays\ (zoom1..10 grid crops, unverified earlier notes). No METHOD.md/sources.md/shape.json existed.
- The src PNGs are satellite fetches, so origin is re-establishable from the .geo.json sidecars. Overlays treated as unverified scratch.

## Step 1a - satellite inventory (2026-10-05)
Viewed src\ images (all Esri World Imagery, via satellite.py; sidecars give bounds/zoom/release/capture date):
- borth_current_z18.png (centre 52.469,-4.0681, r=600 m): wrong area (cliffs south of Borth) - no reef. role: delete.
- borth_esri_{2012-10-27 (wayback 18358), 2013-06-04 (11351), 2017-05-09 (15423), 2020-03-26 (11475), 2022-08-25 (34007), 2024-09-17 (current)}_z19.png, centre 52.4832,-4.0562, r=140 m, 0.1818 m/px.
  Contact sheet viewed: the reef is CLEARLY visible on every one of these: two separate mounds - a northern curved/hook ("boot"-shaped) mound trending SW->NE, and a southern oval/racetrack mound trending N-S. Seabed to the east is a sand beach edge.
  2012-10 and 2013-06: rock mounds submerged/awash, covered in green algae; 2017-05: cloud over (unusable); 2020-03: rough/low-contrast, partly submerged; 2022-08 and 2024-09: low tide, bare light-grey rock fully exposed = sharpest outlines.

## Step 1b - housekeeping (2026-10-05)
- Wrote sources.md (6 satellite rows). Deleted src files not used: current_z18 (wrong area), wide_z17, 2017-05-09 (cloud), 2020-03-26 (poor contrast).
- borth_shoreline_z19 (centre 52.4834,-4.051) shows the village frontage: shingle ridge + sea wall along the village, sand flats exposed at low tide (2024-09-17), and the detached reef mounds at its west edge ~300+ m from the shingle crest.
- Plan: PRIMARY = sat2024 (bare rock at low tide, sharpest outlines; current state = as-built state since sat2012/2013/2022 show the same footprint). Cross-checks: sat2022 and sat2012 (same pixel frame, so one polygon set can be overlaid on all and shifts/settlement detected).

## Step 2a - trace of PRIMARY sat2024 (2026-10-05)
- Zoomed (overlay.py zoom, grid 50/25 px) on the northern mound (box 350,130-1250,700) and southern mound (box 620,840-980,1320) of src/borth_esri_2024-09-17_z19.png (1540x1540, 0.18183 m/px, georeferenced).
- Outline traced at the OUTER EDGE of the bare light-grey rock (where rock meets the dark shadow/water halo): N mound 42 vertices, S mound 37 vertices -> polys_v1.json (pixel coords). Rendered with overlay.py render and viewed: outline follows the rock edge closely on both mounds (within ~3-5 px = 0.5-1 m except at loose-rock fringes).
- Two separate mounds confirmed (gap between them ~ 270 px = 50 m of open water): N = curved "boot/hook" mound trending SW-NE, with a fat SW head and slimmer NE tail; S = oval/racetrack mound trending N-S.

## Step 2b - cross-check traces (2026-10-05)
- Overlaid the sat2024 polygons on sat2022 and sat2012 first (same pixel frame): same footprint, no visible rock movement over 2012-2024; sat2012 shows an apparent whole-image offset of ~+19 to +30 px east (3-5 m) vs sat2024 -> imagery registration difference between vintages, not reef movement (both mounds shift together).
- Traced sat2022 independently from zoom grids (polys_2022_v1.json): outline = outer edge of bare rock plus breaking-foam fringe on W side (swell was running). N mound 42 vtx, S mound 37 vtx. Rendered, viewed: fits.
- Traced sat2012 independently (polys_2012_v1.json): reef is awash and algae-covered, outline soft (edge = pale-green algal rock vs darker water); N 42 vtx, S 29 vtx. Rendered, viewed: fits within ~5 px except diffuse NW halo.
- Scope cap respected: 3 images traced (sat2024 primary; sat2022, sat2012 cross-checks).

## Step 3a - scale, georeference, canonical frame (2026-10-05)
- Scale: all three traced images are the same Esri z19 frame (bounds in .geo.json; 1540 px). Ground scale 0.18183 m/px at 52.4832 N (zoom-19 Web-Mercator 0.29858 m/px x cos(lat)); pixel -> lat/lon with satellite.py pix2ll (exact Web-Mercator interpolation), lat/lon -> local metres (equirectangular about 52.4832,-4.0562). Method: "georeferenced". Check: S mound length 71.8 m and width 31 m are identical on 3 imagery dates within +-3 m.
- Registration: individual-mound centroids agree between sat2024 and sat2022 within 0.8 m (E) / 0.6 m (N); sat2012 sits ~5-6 m east and ~1-2 m north of sat2024 (both mounds shift together = imagery-vintage registration offset, not reef movement). Absolute position uncertainty of the geo-referenced polygon: about +-5 m (Esri/Maxar positional accuracy; vintage-to-vintage spread 6 m).
- Shoreline reference = "defence line" = back of the shingle beach / toe of the village frontage (seaward edge of the building line and grass bank), read on borth_shoreline_z19 at px (1795,1100),(1800,1500),(1803,2000),(1805,2500),(1808,2600); total-least-squares fit residual <0.3 m; bearing 359.57 deg (i.e. due N-S, 0.4 deg west of north). The shingle/low-tide-sand foot (px x~1510-1530, same image) is a second reference (bearing 0.48 deg); it moves with tide so is not used as the frame.
- Canonical frame: origin = foot of the perpendicular from the reef (both-mound) centroid onto the defence line; +x = along the defence line toward the NORTH (bearing 359.57 deg), +y = offshore = WEST (bearing 269.57 deg). shore_normal_bearing_deg = 269.57. (NOTE: geom.py make_canonical / px_to_m has a rotation-sign bug for any alongshore direction other than (1,0): tested alongshore-dir-px 0,-1, point 100 px along that direction returns x=-100 instead of +100. I therefore computed the canonical frame myself with numpy/shapely from the lat/lon-derived metres; tools untouched.)
- Results sat2024: N mound 3,944 m2, S mound 1,798 m2, total 5,743 m2; canonical bbox x -121.3..+74.2 (195.5 m alongshore), y 257.0..397.0 (140.0 m cross-shore); reef centroid 330.5 m offshore of the defence line (nearest edge 257 m, farthest edge 397 m); 206-346 m from the shingle/sand foot at 2024-09-17 low tide.
- Cross-check areas: sat2022 4,848 m2 (-15.6%, tighter trace + wave wash), sat2012 5,535 m2 (-3.6%, algae-covered awash outline). Lengths: N mound 141-147 m, S mound 69-72 m x 29-31 m on all 3 dates; gap between mounds 57-61 m.
- Angles (true bearings, acute angle to shoreline in brackets): N mound long axis 61-64 deg (61-64 deg to shore), head part 64-67 deg, tail part 76-77 deg (bend 9-12 deg, tail curves toward E); S mound long axis 359.7 deg (0.2 deg, i.e. parallel to the shore); N-mound centroid lies 124 m from S-mound centroid at bearing 356 deg (i.e. nearly due north along the shore).

## Step 3b - checkpoint (2026-10-05)
- Wrote shape.json (status traced): sources sat2024 (primary), sat2022 + sat2012 (cross-checks), satshore + sat2013 (context); canonical metres polygons, lat/lon polygons, angles. Confidence / design_version / dimensions_check / gemini / references still provisional pending web research (steps 1b, 1d, 1e).
- Scratch scripts and renders live in scratchpad\borth\ (not the project).

## Step 3c - canonical-frame check after orchestrator's geom.py warning (2026-10-05)
- I did NOT use geom.py make-canonical / px_to_m for the canonical frame (I had already found the same rotation-sign bug: alongshore-dir-px (0,-1), a point 100 px along it returned x=-100). The frame is computed explicitly: pixel -> lat/lon (pix2ll) -> local east/north metres -> x = dot(v, alongshore unit), y = dot(v, offshore unit) with alongshore bearing 359.57 deg and offshore bearing 269.57 deg, origin on the fitted defence line.
- Independent hand check of ALL 79 vertices: haversine distance and great-circle bearing from the origin (lat/lon) to each vertex, then x = d*cos(bearing-359.57), y = d*cos(bearing-269.57). Max difference to the stored canonical coordinates 0.007 m. Examples: px (402,525) -> hand (16.90, 396.96) = stored; px (1100,210) -> (73.21, 269.61) vs stored (73.22, 269.61); px (780,887) -> (-49.45, 328.73) vs (-49.44, 328.73).
- Area, bbox, centroid and max-dimension were also computed with shapely, not with the geom.py rotation path.

## Step 4 - verification, corrections and added sources (verifier, 2026-10-06; full evidence in VERIFY.md)
- Tracer's note on geom.py confirmed and re-tested: the canonical block was NOT made with the buggy path; I recomputed it independently (max diff 0.005 m, 79 vertices) and with the fixed geom.py (selftest 334/334). CORRECTION: the frame was mirror-handed (+x north, +y west = +y is +x turned COUNTER-clockwise). All other shapes and geom.py use +y = +x turned clockwise. canonical.polygons_m now has +x = SOUTH (x -> -x, bearing 179.57), +y = west (269.57). Areas, bbox sizes, y values and angles to the shoreline are unchanged; x_range is -74.2..+121.3.
- The tracer's checkpoint (step 3b) had left confidence reason, design_version, dimensions_check, gemini and references provisional/empty. They are now filled (VERIFY.md checks 2, 4-7).
- Design version (new evidence): HRPP576 (HR Wallingford 2013) says the original two surfable reefs (north A, south B) became ONE surfable northern reef (extended, rock, small hook on the near side) plus a shore-parallel breakwater C; the Royal Haskoning 'For Construction' drawings 9V5090/1001, 1020-1023 (rev C1, Jan 2011) show exactly the boot-shaped Northern Reef and the oval Southern Reef that the imagery shows. The drawn state is therefore the built final layout (Phase 1 completed March 2012). The oval is a breakwater (crest +1.50 mODN), the boot is the surf reef (crest +0.50 mODN).
- New cross-checks: (a) the plan 1020 is georeferenced by its 15 printed OS-grid setting-out points (fit residual 0.02 m, scale exactly 1:500); its five concentric vector rings per reef were extracted from the PDF and overlaid on the 2024 image: armour-foot IoU 0.79 (north) / 0.86 (south); (b) Welsh Government LiDAR tile SN6089 (flown 2022-03-19 03:15 UTC, sea near LAT) gives the exposed footprint (N 5861 m2, S 2814 m2) and crest heights; the shapes are in canonical.alt_outlines_m. The drawn outline is the visible rock edge and is the innermost of the three footprint definitions (5743 vs design foot 6989 vs LiDAR 8675 m2).
- OS grid -> WGS84 uses pyproj EPSG:27700->4326 (Helmert, +-2-5 m, no OSTN15 grid); this is the limit of the design/LiDAR-to-satellite position check.
- New sources are in src/ (drawing PDFs + 110 dpi PNGs, HRPP576 PDF) and 03_images/reefs/borth-coastal-defence-reef/ (HRPP576 figures); all registered in images.json (img-17..25).

# METHODS_3D - Borth coastal defence reef (Phase 1, Ceredigion, Wales)

3D model v1, 2026-10-07 (3D agent, Sonnet 5.5). Files: `3d\model.js` (data), `3d\index.html` (viewer), `3d\build_3d.py` (rebuilds model.js, docs.js and, with `--shape`, shape.json), `3d\make_annotations.py` and `3d\nav_read.py` (annotated images), `3d\SOURCES_3D.md` (step-by-step log). Not for navigation.

## 1. Summary

The model shows the **as-built final layout of Borth Phase 1 (completed 8 March 2012)**: a northern boot-shaped **surf reef** (crest +0.50 mODN, tail +1.00, head edge +0.00 rising over about 40 m) and a southern oval that is a **shore-parallel breakwater, not a surf reef** (crest +1.50 mODN), on a seabed rebuilt from the 2022 LiDAR beach, the HRPP576 Fig 2 contours, the design bed levels and the EMODnet trend, with the water surface selectable from LAT to MHWS. Three outlines of the same structure are modelled and selectable: the **laser-survey edge (Welsh Government LiDAR, 19 Mar 2022, 8,675 m2, default, chosen by Lior on 2026-10-06)**, the design rock-layer foot of drawing 9V5090/1020 (Jan 2011, 6,989 m2) and the visible rock edge in the Esri photo of 17 Sep 2024 (5,743 m2). The default surface is the 1 m LiDAR DSM above the exposed level (about -2.3 mODN) plus the design toe berm and blanket of drawings 1021-1023 below it; the model rock volume is 31,300 m3 (about 53,000 t at 1.7 t/m3, +-15 %). No later damage, deflation or removal was found (imagery 2012-2024, 2022 LiDAR), so no second state is modelled. **3D confidence: MEDIUM**: the plan and the crest levels are well supported (laser survey and design agree within 0.3 m), but the seabed under and around the rock rests on a design bed level (about -4.0 mODN, "bed levels vary"), a hand-read contour figure and an estimated MSL offset, and the modelled sea floor seaward of the reef is 0.9 m deeper than the Fig 2 -4.0 contour (section 4.4), so heights above the bed are known to about +-0.5 m and volumes to about +-15 %.

## 2. Data sources

Citations are author-year; "id" is the source id used in `model.js` provenance and `shape.json`. Registry ids refer to `03_images\reefs\borth-coastal-defence-reef\images.json`. All local copies are private research copies; reuse rights are to be checked before any public release.

| id | citation | contributed | resolution / date |
|---|---|---|---|
| drg1020-1023 | Haskoning UK Ltd for Ceredigion County Council (2010-11). *Borth Coastal Protection Scheme - Phase 1*, drawings 9V5090/1020, /1021, /1022, /1023 rev C1 (For Construction, Jan 2011). http://www.borthcommunity.info/index.php/planning-drawings/65-planning-drawings, accessed 2026-10-06 (registry img-20..23) | plan rings, 15 setting-out points (OS grid), crest levels +0.50 / +1.00 / +0.00 / +1.50, layers (Type 4 2.70 m, Type 5, Type 6 0.5 m), toe berm (1.35 m, 3 m top, 1:1.5), slopes 1:3 / 1:4 / 1:5, tide levels printed (MHWS +2.56, MLWS -1.74), bed note "-4.2 to -3.6m AOD" | vector PDF, 1:500 plan, 1:200 sections; georeference residual 0.02 m |
| lidar2022 | Welsh Government (2022). *LiDAR 2020-22, 1 m DSM and DTM, tile SN6089*, flown 2022-03-19 03:15-03:20 UTC. DataMapWales; Open Government Licence. https://dmwproductionblob.blob.core.windows.net/lidar-zips/2020-22/dsm/wg_del_29_260289_20220319dsm.tif (DTM: same path with dtm), accessed 2026-10-06 (registry img-24) | as-built exposed surface (DSM), beach and foreshore (DTM), water edge about -2.3 mODN | 1 m, EPSG:27700, vertical datum not stated (ODN assumed, A4) |
| hrpp576f2 | Rigden, T., Stewart, T., Allsop, W. and Johnson, A. (2013). *Surf reefs - physical modelling results, not pipe dreams*. HR Wallingford report HRPP576; ICE Coasts, Marine Structures and Breakwaters, Edinburgh, Sept 2013, Fig 2. https://eprints.hrwallingford.com/931/1/HRPP576_SurfReefs.pdf, accessed 2026-10-06 (registry img-17) | pre-construction contours +0.0 ... -5.0 mODN around the reefs (traced -2, -3, -4); oval C position; 500 m scale bar | figure 849 x 349 px, 1.776 m/px, +-10 m |
| sat2024 | Esri World Imagery (2024-09-17, also 2012-10-27, 2013-06-04, 2022-08-25), zoom 19, 5.4995 px/m. https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer, accessed 2026-10-06 (registry img-08..11) | traced visible-rock outline (version sat_2024), waterline height at the traced edge | +-5 m absolute |
| emodnet | EMODnet Bathymetry Consortium (2024). *EMODnet Digital Bathymetry (DTM 2024)*. https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1 (CC BY 4.0); survey cells CDI 115084 (OceanWise Ltd), accessed 2026-10-06 (registry img-14..16) | offshore gradient -1.1 % from y = 335 m outwards; reef-zone cells are GEBCO interpolation (1.0-1.4 m too shallow) and are not used | 1/16 arc-minute cells, one sounding per cell, age > 30 y |
| ref3 | Royal HaskoningDHV (2011). *West of Wales Shoreline Management Plan 2*, Section 4 Coastal Area C Introduction, p. 4C.3, water-level table (Aberystwyth). https://www.grwparfordirolgorllewincymru.cymru/sites/default/files/2019-06/4c1%20-%20Section%204%20Coastal%20Area%20C%20Introduction.pdf, accessed 2026-10-06 | MHWS +2.56, MHWN +1.06, MLWN -0.64, MLWS -1.74 mAOD (= mODN) | tabulated |
| ref4 | National Tidal and Sea Level Facility (n.d.). *Chart datum and ordnance datum: differences at selected ports*. https://ntslf.org/tides/datum, accessed 2026-10-06 | LAT = chart datum = ODN - 2.44 m at Barmouth and Fishguard (Aberystwyth not listed) | +-0.1 m |
| ref6 | Hansford, M. (2011). Borth's Big Dig. *New Civil Engineer*, 15 Sept 2011. https://www.newcivilengineer.com/archive/borths-big-dig-15-09-2011/ | 275,000 t rock for the whole Phase 1, Type 4 (6-10 t) 42,000 t | upper bound only |
| ref7 | RCAHMW (2020). Coflein, Coastal Defences, Borth, NPRN 424699. https://coflein.gov.uk/en/site/424699, accessed 2026-10-06 | completion 8 March 2012, reef about 300 m offshore | - |
| navionics | Garmin Ltd / Navionics (2026). Marine Maps web viewer (Nautical Charts and SonarChart Maps), "Not to be used for navigation". https://maps.garmin.com/en-US/marine?maps=another-brand&overlay=false&key=gcm4edq678dp (successor of webapp.navionics.com), accessed 2026-10-07 (registry rows added this run) | cross-check of the seabed and datum (section 3.6); NOT used as a model input | zoom 17 / 18, 0.73 / 0.36 m/px; contour interval 0.5 m shallow |

Not found at a primary source (searched): the highest astronomical tide (HAT) at Aberystwyth; a reef-only rock volume or tonnage; an as-built plan or post-construction survey of the reef; a Navionics/SonarChart depth for the reef itself.

## 3. Methods

### 3.1 Frame and datums

* Canonical frame of `shape.json` (metres): x alongshore, + toward SOUTH (bearing 179.57 deg); y offshore, + toward WEST (bearing 269.57 deg); origin at the foot of the perpendicular from the centroid of both mounds on the defence line (back of the shingle beach, bearing 359.57 deg). z up.
* OS grid to canonical is an affine map fitted over a 600 x 600 m window to the exact chain (OSGB36 -> WGS84 Helmert via pyproj -> local tangent plane -> rotation): residual rms 0.005 m, max 0.02 m (`b3d_lib.Frame`). Absolute position is limited by the Helmert (+-2-5 m), not by this fit.
* Vertical: working datum Ordnance Datum Newlyn (ODN = mAOD). Model zero = mean sea level:

```
z_MSL = z_ODN - 0.31                     (E1)  MSL = +0.31 mODN = (MLWS + MLWN + MHWN + MHWS)/4, +-0.15 m  (A2)
z_LAT = z_ODN + 2.44      (depth below chart datum d_CD = -(z_ODN + 2.44) for the sea floor)   (E2)  LAT = -2.44 mODN (A3)
z_MSL = e_LAT - 2.75                     (E3)  EMODnet cells are given relative to LAT
```

* Tide levels (mODN / m MSL): LAT -2.44 / -2.75; MLWS -1.74 / -2.05; MLWN -0.64 / -0.95; MSL +0.31 / 0; MHWN +1.06 / +0.75; MHWS +2.56 / +2.25. **The slider stops at MHWS** because the HAT of Aberystwyth was not found at a primary source (the only HAT-like figure, 5.9 m chart datum, is a predicted maximum, not HAT), and MHWS is the highest level with a published source (ref3; also printed on drawing 9V5090/1021). Two photo/flight levels are offered as extra presets: LiDAR flight 19 Mar 2022 (about -2.3 mODN, read as the sea surface at the rock edge) and the Esri photo of 17 Sep 2024 (about -1.3 mODN, median DSM height along the traced edge).
* No Haifa/Israel tide preset (Lior's rule): local tides only.

### 3.2 Reef surface, three versions (1 m grid, window x -105..150, y 235..420 m)

Common design constants (drawings 1021-1023): crest +0.50 (arm, 9 m wide), +1.00 (tail, strip R2/R5-R3/R4, transition 15 m from SOP R2), +0.00 at the head edge (R1/R10) rising to +0.50 over about 40 m, +1.50 (oval, flat top 6 m x 38-46 m between R14 and R15); Type 4 layer 2.70 m thick; toe berm 1.35 m high, 3 m top, 1:1.5 sides; flat apron 2.0 m; blanket 0.5 m with 1:1.5 edge; foot of the Type 4 slope = top of the toe berm = **-2.15 mODN** (bed -4.0 + blanket 0.5 + berm 1.35).

* **design_1020** (Royal Haskoning rock-layer foot). Concentric rings 0-4 of drawing 1020 are extracted from the vector PDF and georeferenced with the 15 setting-out points. Between rings the surface is interpolated linearly in the distance to the two bounding rings: ring 0 (apron outer edge) at the seabed -> ring 1 (blanket top edge, +0.5 m) -> ring 2 -> ring 3 (berm top outer edge) -> ring 4 at -2.15; inside ring 4 the surface rises linearly in distance to the crest outline (R1-R6, R2-R5 paths, crest zones with the heights above) at the crest height of the zone. The 1:3 / 1:4 / 1:5 slopes are therefore not imposed separately; they result from ring spacing (the plan is drawn to those slopes). Surface = max(design, seabed).
* **lidar_2022** (default). Inside the outline of the exposed rock (cells with a LiDAR return, water edge about -2.3 mODN, 1 m cells, simplified 0.4 m) the surface is the LiDAR DSM, lightly smoothed (normalised Gaussian, sigma 0.8 m, A9) and never below the edge level; outside the outline the design toe is attached with the **same toe slopes as drawings 1021-1023**: 1:1.5 down from the edge level to the blanket top (bed + 0.5 m), 2 m flat apron, 1:1.5 blanket edge to the seabed (A11). The surface below the water edge is therefore design, not measured.
* **sat_2024** (visible rock edge). The same construction with the 79-vertex outline traced on the 2024 Esri image and edge level -1.3 mODN. Because the toe slope is imposed from the edge (1:1.5) it is steeper than the real flanks and the volume is smaller.
* Zones for colour: 1 armour / surveyed surface (Type 4), 2 toe berm (Type 0), 3 blanket and apron (Type 6).
* Rock volume is the integral of (surface - modelled seabed) over the 1 m grid, both mounds, including berm and blanket. Type-4-layer volume is the integral of min(2.70 m, surface - bed) over the armour zone. Tonnes = volume x 1.7 t/m3 (A8).

### 3.3 Seabed

Thin-plate-spline radial basis function (scipy `RBFInterpolator`, smoothing 0.5, 80 nearest neighbours) through control nodes in the canonical frame, evaluated on a 5 m grid (x -200..260, y 0..520 m); the nodes are drawn by source in `annotated\A8_seabed_source_zones.png`:

| nodes | source | level | note |
|---|---|---|---|
| 3,081 | LiDAR DTM 19 Mar 2022, beach and lower foreshore, 6 m grid, y < 255 m, rock buffered out by 12 m, only cells above -2.35 mODN | measured | water edge reached about y 245 m |
| 12 | HRPP576 Fig 2 -3.0 mODN contour, outside the reef zone (x not in -115..+160) | -3.0 | read by eye, +-0.5 m, +-10 m horizontally |
| 12 + 3 | design bed under the north arm (drawing 1021 N3: 2.70 + 1.31 + 0.50 below +0.50 = -4.01) and N4 (-3.8) | -4.0 / -3.8 | derived from layer thicknesses; the section ground line is schematic ("EXISTING SEABED VARIES") |
| 6 | tail: ASSUMED -3.0 (y 272) and -3.4 (y 282), shallower than the arm | assumed | no drawing value |
| 10 | oval: printed note on S2 "-4.2 TO -3.6m AOD": -3.6 shoreward (y 309), -4.2 seaward (y 340) | -3.6 / -4.2 | |
| 6 | anchor line y = 335 m outside the reef x range | -4.0 | ASSUMED (design bed level extended along the shore, A7) |

Beyond y = 335 m the level at the anchor is continued with the EMODnet gradient (A7):

```
z(x, y) = z_RBF(x, 335) - 0.011 (y - 335)         for y > 335 m   (E4)       (-1.1 %, soundings y 368-652 m, CDI 115084)
```

The RBF reproduces all nodes (rms < 0.01 m). Under the footprints the modelled bed is -4.04 mean (-4.72..-2.51) under the north foot ring and -3.95 (-4.21..-3.62) under the oval (design -4.0 and -3.6..-4.2: met).

### 3.4 Tides, water surface, viewer

The water is a horizontal plane at the selected level (static still water; no wave set-up, run-up or surf). The viewer shows seabed (coloured by depth), reef (coloured by zone), the water plane at 38 % opacity, a 10 m grid (50 m bold), 10 m and 50 m scale bars, a north arrow, the defence line y = 0, an outline of the selected version at its edge level, and a camera read-out (position, true heading, pitch, field of view). Vertical exaggeration 1-5 x (default 1) multiplies z only and is always shown; presets: oblique from the sea, plan (north to the left), along the surf-reef crest, from the beach at eye height 1.7 m, side view. Photo-match mode: a local image is overlaid on the canvas and camera x, y, z, true heading, pitch and field of view are adjusted until the rock outlines line up; "Copy camera" prints the parameters (vertical exaggeration forced to 1). Version selector with an (i) pop-up (`versions_info` plus a table name | date | source | footprint | volume); `#version=<id>` in the URL selects a version; `#water=`, `#ve=`, `#view=` also work.

### 3.5 Assumptions

* A1 The drawn design is the built design (no as-built plan was published); the layout is the final one completed on 8 March 2012 (ref7); the superseded two-geotube design is mentioned only.
* A2 MSL = +0.31 mODN (+-0.15). A3 LAT = -2.44 mODN (+-0.1; from Barmouth and Fishguard, MHWS 5.00 m CD and the LiDAR sea surface at a spring low).
* A4 LiDAR heights are ODN (not stated in the tile); supported by the agreement with the design crests (oval p90 +1.75 vs +1.50 design, a block-top effect) and the sea surface at the flight (-2.2..-2.4 vs LAT -2.44).
* A5 The LiDAR edge level (water at the flight) is -2.3 mODN (+-0.1), inferred from the data, not from a tide prediction.
* A6 Seabed under the rock: arm -4.0 (derived), tail -3.0 .. -3.4 (assumed), N4 -3.8, oval -3.6 / -4.2 (printed note). Derived bed under the oval centreline from S1-S1 is -3.4, 0.2 m shallower than the printed range.
* A7 Anchor -4.0 mODN at y = 335 m outside the reef range and the EMODnet gradient -1.1 % beyond (orchestrator decision 2026-10-06).
* A8 Placed-rock bulk density 1.7 t/m3 (range 1.6-1.8; solid 2.65 t/m3, voids about 36 %).
* A9 The DSM is smoothed with sigma 0.8 m; the DSM shows block tops, 0.1-0.3 m above the design surface.
* A10 Edge levels of the versions: -2.3 (lidar_2022), -2.15 (design_1020), -1.3 (sat_2024; median DSM height along the traced edge: north -1.25, south -1.36 mODN).
* A11 Flanks below the water edge are design (1:1.5 berm and blanket slopes, 2 m apron); the as-built flanks above the edge are flatter than the design (LiDAR 1:4.0-1:5.3 vs 1:3) and 8-10 m wider; below the edge they are unknown.
* A12 Still, horizontal water surface at each tide level.
* A13 The Navionics chart datum is LAT (UK convention); the viewer does not state it.

### 3.6 Navionics chart reading and datum test

*Access.* The old Navionics ChartViewer (webapp.navionics.com) now redirects to Garmin's Marine Maps viewer. In my own headless Chrome (a random free DevTools port, a fresh temporary profile, process terminated by PID afterwards; never the shared browser pane) the page loaded without login, CAPTCHA or consent dialog; nothing was accepted or bypassed. The map was centred on the centroid of the two mounds (52.483453 N, 4.056205 W) with the page's geohash key; options Depth units = Metres; chart types SonarChart Maps and Nautical Charts; zoom 17 and 18 (maximum); "Shallow shading" 0, 1, ... 10 m (44 screenshots, `src\navionics\`, `capture_navionics.py`, `capture_log.json`). The viewer does **not** state a datum or a contour interval and shows no data dates; screenshots are private research copies ("Not to be used for navigation", Garmin Navionics).

*Geometry.* The screenshot is the 982 x 655 px map container, north up; the page itself reports the centre pixel (491, 327). Pixel to ground:

```
r = 156543.03392 / 2^zoom   (Mercator m/px; 0.730 m/px of ground at zoom 17)      (E5)
(col,row) -> Mercator (x_c + (col-491) r, y_c - (row-327) r) -> WGS84 -> OS grid -> canonical (E6)
```

*Reading.* Along 8 pixel rows (x from -194 to +198 m) thin dark runs are contour lines; counted outward from the edge of the green "drying" area (the 0 m line) they are 0, 0.5, 1, 1.5, 2, 2.5 m (the printed labels 0.5, 1, 1.5, 2, 2.5 confirm the 0.5 m interval). The 0 m line is at y = 385 (x -56) to 430 m (x +198), then 0.5 m at +45 m, 1 m at +105, 1.5 m at +163, 2 m at +212, 2.5 m at +293 m farther offshore. The Nautical Chart layer shows only the 0 m and 2 m lines and one drying-height label (0.2 m at x -108.5, y 248). `annotated\A9_navionics_sonarchart_z17_annotated.png`, `A10_navionics_nautical_z18_reef_outline.png`.

*Datum test.* If a reference gives the seabed level z_ref (mODN) at a point where the chart gives depth d below its datum, the chart zero is z_ref + d (mODN). Zero levels implied by each reference (mean +- sd, n):

| reference | implied chart zero (mODN) | RMS vs LAT -2.44 | MLWS -1.74 | MLWN -0.64 | MSL +0.31 | ODN 0 | MHWN +1.06 | MHWS +2.56 |
|---|---|---|---|---|---|---|---|---|
| HRPP576 Fig 2 -4.0 contour, 7 points x -194..+169 | -3.58 +- 0.07 (7) | **1.15** | 1.84 | 2.94 | 3.89 | 3.58 | 4.64 | 6.14 |
| EMODnet cells at x -31 (y 368, 440, 513) | -3.07 +- 0.08 (3) | **0.64** | 1.34 | 2.43 | 3.38 | 3.07 | 4.13 | 5.63 |
| this model's seabed (24 line crossings, y <= 515) | -4.73 +- 0.20 (24) | **2.30** | 3.00 | 4.10 | 5.05 | 4.74 | 5.79 | 7.29 |

LAT is the best standard datum against all three references and the one drying-height label agrees with it (0.2 m above chart datum = -2.24 mODN; the LiDAR has water there at -2.3: within 0.1 m), so the chart datum is taken as LAT (A13). But no datum fits well offshore: the charted 0 m line lies 140-180 m seaward of the LiDAR water edge (y about 245 m at -2.3 mODN) and the chart is 0.6-1.1 m shallower than the Fig 2 and EMODnet references; SonarChart contours are partly interpolated and their survey dates are not shown. The chart is therefore a cross-check only and was **not** used to build the seabed.

*Crest and height.* The structure still exists (LiDAR 2022; imagery to 2024) but it is **not resolved** by either layer: the rock mounds (0 to +1.5 mODN, 2.4-4 m above LAT) lie inside the uniformly green drying area with no symbol, label or contour at the footprint. The only charted shoal (closed 0.5 and 1 m loops) is at canonical (37, 405), 35 m seaward of the nearest rock, and is not the reef. Navionics therefore gives no crest depth or height, and no cross-check of the design figures was possible.

## 4. Validation

### 4.1 The three outline versions compared

| | lidar_2022 (default) | design_1020 | sat_2024 |
|---|---|---|---|
| name | Laser survey edge (Welsh Government LiDAR, 19 Mar 2022) | Design rock-layer foot (Royal Haskoning drawing 9V5090/1020 rev C1, Jan 2011) | Visible rock edge (Esri satellite photo, 17 Sep 2024) |
| kind / date | laser survey, 2022-03-19 | design drawing, 2011-01 | photo trace, 2024-09-17 |
| edge definition | rock exposed at the water level of the flight, about -2.3 mODN | foot of the Type 4 armour = top of the toe berm, -2.15 mODN | rock above the waterline in the photo, about -1.3 mODN |
| footprint at the edge | 8,675 m2 (207 x 150 m bbox) | 6,989 m2 (197 x 144 m) | 5,743 m2 (196 x 140 m) |
| footprint incl. toe and blanket | 11,518 m2 | 11,491 m2 | 8,979 m2 |
| surface | LiDAR DSM above the edge + design toe below | design (rings 0-4 + crest zones) | LiDAR DSM above the edge + design toe (1:1.5) below |
| rock volume above the modelled seabed | 31,336 m3 (+-4,607) | 30,091 m3 (+-4,596) | 26,400 m3 (+-3,592) |
| tonnes at 1.7 t/m3 (range 1.6-1.8) | 53,300 (50,100-56,400) | 51,200 (48,100-54,200) | 44,900 (42,200-47,500) |
| Type 4 armour layer (2.70 m) | 21,557 m3 = 36,600 t | 17,990 m3 = 30,600 t | 15,369 m3 = 26,100 t |

The footprints differ because the three edges sit at different heights on the same sloping flanks (-2.3, -2.15, -1.3 mODN at about 1:4-1:5), not because the structure moved (no change was found in the imagery 2012-2024: the 2022 outline lies within 0.8 m of the 2024 one; the 5 m offset of the 2012 image is registration). The volumes differ much less than the footprints: the default and the design agree within 4 % in total volume, the photo version is 16 % lower because its edge is high and the imposed 1:1.5 toe is steep, and the Type 4 layer volume rises from 15.4k to 21.6k m3 as the edge moves down. In every version the Type 4 layer (26-37 kt) stays below the 42,000 t of Type 4 rock that NCE (ref6) gives for the **whole** Phase 1 (breakwaters, groynes and revetment included), so the model is consistent with that upper bound. No reef-only quantity exists at a primary source.

### 4.2 Crest and shape against the laser survey

(`annotated\A6_lidar_crest_check.png`.) LiDAR DSM inside the design crest strips: north arm median +0.58, p90 +0.91 mODN (design +0.50); oval median +1.55, p90 +1.75 (design +1.50); the model max crest is +1.81 (DSM block tops). On the common cells above -2.0 mODN the default surface minus the design surface is +0.14 m mean, sd 0.28 m. Along the arm axis the DSM follows the design steps (+0.0 -> +0.5 over about 40 m, +0.5 -> +1.0 over about 15 m). Across the oval the DSM top agrees (+1.5) and the flanks are 8-10 m wider than the design 1:3 (as-built slope 1:4.0-1:4.1). The earlier verification quotes N arm median +0.69 on a different cell mask; the difference (0.11 m) is the mask, not a conflict.

### 4.3 Geometry checks

* Frame fit rms 0.005 m (max 0.02 m); design foot ring (ring 4) reproduced from the PDF against `shape.json` alt_outlines: IoU 0.9998; the PDF-to-OS-grid fit of drawing 1020 has maximum residual 0.12 pt (0.02 m); the re-projected rings, crest paths and setting-out points lie on the drawing to about 1 pixel (`A2_drg1020_rings_and_sop_read.png`).
* Section readings on drawings 1021-1023 (`A3`-`A5`): arm crest +0.50, Type 4 underside -2.20, head +0.00 / -2.70, tail +1.00 / -1.70, oval +1.50 / -1.20 / -2.90, toe berm 1350 mm, apron 2000, blanket 500; MHWS +2.56 and MLWS -1.74 printed; transitions 40 m and 15 m; oval S1-S1 is dimensioned 23,000 + 23,000 mm between SOP R15 and R14 (46 m), whereas the setting-out table of drawing 1020 puts R14 and R15 38 m apart (the model uses the table; the strip measured on the plan is 38 m): an unresolved inconsistency inside the drawing set, worth about 2 % of the oval volume.

### 4.4 Seabed checks

* Under the footprints: model -4.04 mean under the north foot ring (design -4.0) and -3.95 under the oval (design -3.6..-4.2): met. The bed derived from S1-S1 under the oval centreline (+1.50 - 2.70 - 1.70 - 0.50 = -3.4) is 0.2 m above the printed range, inside the +-0.4 m.
* HRPP576 Fig 2 contours (`A1`, `A7`): at the traced points outside the reef zone the model minus the contour level is -0.01 m (sd 0.03, n 24) for -3.0 (this contour is a control), -0.14 m (sd 0.04, n 24) for -2.0 (not a control), and **-0.89 m (sd 0.14, n 13) for -4.0: the model is 0.89 m deeper than the -4.0 contour** (the -4.0 contour is not a node: the anchor -4.0 at y = 335 m plus the -1.1 % gradient gives -4.7 mODN at y 400 m and -5.1 at y 440, where Fig 2 has -4.0 at y 410-450). Under the footprints the design nodes pin the bed, so the volumes do not change; the visible sea floor in front of the reef does. Navionics (implied zero -3.6) and EMODnet (-3.1) are both shallower than the model, i.e. three independent sources agree against it. Not corrected in this run (the -4.0 anchor and the EMODnet trend were fixed by the orchestrator on 2026-10-06); recommended fix in section 7.
* Beach (`A7`): the 2022 LiDAR DTM has a salient (contours pushed offshore) behind the mounds at x -20..+100 m: its -2.0 contour is at y about 245 m there against about 205 m elsewhere and in Fig 2 (survey about 12 years older). The measured 2022 DTM is used there.
* EMODnet absolute cells are 1.5-1.6 m shallower than the model at y 368-513 (known: the reef-zone cells are GEBCO interpolation); only the gradient is used.

### 4.5 Registry rows closed (STEP 0)

| id | what it bore on | result |
|---|---|---|
| img-14, img-15, img-16 (EMODnet viewer, sources, profile) | seabed, tides | MSL - LAT = 2.75 m (E3); reef-zone cells 1.0-1.4 m too shallow versus the design bed (interpolated); only the gradient -1.1 % is used (E4); the three images are kept as context |
| img-17 (HRPP576 Fig 2) | seabed -3..-5 mODN | -3.0 contour is a control (model -0.01 m); -2.0 -0.14 m; -4.0 -0.89 m (model deeper; section 4.4) |
| img-20 (drawing 1020) | planform, crest zones | rings, crest paths and SOP re-projected and used; design foot IoU 0.9998 |
| img-21 (drawing 1021) | crest, layers, slopes | +0.50 / +1.00 / +0.00, ramps 40 m / 15 m, layer 2.70 m, toe berm confirmed; bed -4.0 derived |
| img-22 (drawing 1022) | head slope, mid slope | N4 +0.50, 1:4 flanks, N5 / N6 +0.00 / -2.70 confirmed |
| img-23 (drawing 1023) | oval crest, bed | +1.50, flat top 6 m, 1:3, printed bed range -4.2..-3.6 AOD; bed derived from S1 -3.4 |
| img-24 (LiDAR DSM sections) | crest and flank shape | section 4.2: median +0.58 / +1.55 against +0.50 / +1.50; LiDAR minus design +0.14 +- 0.28 m |

## 5. Uncertainty

Simple (root-sum-square) propagation, independent inputs:

```
sigma(z_crest, design) = 0.1 m                      (drawing labels, 0.05 m measured on a 300 dpi render)
sigma(z_crest, LiDAR)  = 0.15 m (vertical datum A4) + 0.1-0.3 m (block tops)
sigma(z_bed under rock) = 0.4 m                     (A6: derived layer thicknesses; beds "vary")
sigma(H = z_crest - z_bed) = sqrt(0.15^2 + 0.4^2) = 0.43 m  ->  north arm H = 0.50 + 4.04 = 4.5 m +- 0.5; oval 1.50 + 3.95 = 5.5 m +- 0.5     (E7)
sigma(z_MSL) = sqrt(0.15^2 [MSL offset] + 0.1^2) = 0.18 m  -> crest height above MSL +0.19 m (arm) is +-0.2 m
crest depth below the water, d = z_water - z_crest: sigma(d) = sqrt(0.18^2 + sigma_crest^2) = 0.2-0.3 m                                     (E8)
dV = 0.4 m x A(footprint incl. toe) = 0.4 x 11,518 = 4,607 m3 (15 %); density 1.6-1.8 t/m3 -> +-6 %; edge-level choice: +-8 % (section 4.1)    (E9)
```

Position: +-5 m (Esri), +-2-5 m (Helmert); horizontal seabed contours +-10 m. The sea floor outside the reef is less certain than under it: at y 400-500 m the modelled level is 0.9 m deeper than Fig 2 and 1-2 m deeper than Navionics / EMODnet (section 4.4). Vertical exaggeration k multiplies every height and every slope in the picture by k while plan distances stay true; at k = 5 the 1:4 flanks look like 1:0.8. Heights, slopes and tide read-outs on screen are always true values (divided by k); the photo-match mode forces k = 1.

## 6. Confidence

**MEDIUM.** Against the project rubric (high = every input sourced and cross-checked within about 10 %, medium = key inputs sourced but at least one first-order input estimated, low = a first-order input missing): the plan is high (design rings and laser survey agree to 1 pixel / 0.3 m), the crest levels are high (three independent readings: design drawing, LiDAR, section drawings), the tide offsets are medium (MSL is a four-level estimate +-0.15 m, LAT from neighbouring ports), and the seabed is medium-low: under the rock it is the drawing-derived -4.0 mODN (+-0.4 m), around the rock a hand-read contour figure and an assumed anchor, and seaward of y 335 m an extrapolated gradient that disagrees with three sources by 0.6-1.5 m. Because the first-order unknown for "height above the bed" and for the volume is the bed level, the overall level is medium.

## 7. Limitations and unknowns

| gap | effect on the model | what would resolve it | Lior could supply |
|---|---|---|---|
| bed level under the rock ("EXISTING SEABED VARIES"; no survey) | reef height +-0.5 m, volume +-15 % | post-construction multibeam or the Phase 1 as-built; Ceredigion beach-profile monitoring | Navionics app: spot depths at the reef toe (REQUESTS_FOR_LIOR.md) |
| seabed seaward of the reef is 0.9 m deeper than the Fig 2 -4.0 contour | visible sea floor and its depth read-outs at y > 335 m | add the Fig 2 -4.0 contour (outside the reef zone) as nodes and blend the EMODnet gradient from y of that contour instead of the anchor -4.0 at y = 335 m; check with a sounding | Navionics / Google Earth depth readings along y 335-520 m |
| HAT not found; MSL and LAT offsets for Aberystwyth not tabulated | slider top is MHWS; +-0.15 m on z_MSL | Admiralty Tide Tables / UKHO EasyTide Aberystwyth (Z0, HAT) | a tide-table reading |
| LiDAR vertical datum not stated | +-0.15 m on crest heights | tile metadata | - |
| flanks below the water edge unknown (LiDAR flown at about LAT, edge -2.3) | toe geometry and the lower part of the volume are design, not measured | a multibeam or drone survey at a spring low | Google Earth Pro historical imagery at a very low tide |
| as-built plan, post-2022 state | later damage would not be modelled | Wales Coastal Monitoring Centre data, CoastSnap Borth photos | - |
| Navionics shows neither the reef nor a consistent seabed | no crest cross-check; datum assumed | the Navionics app (SonarChart live) may show more than the web viewer | Navionics app reading at the listed coordinates |
| rock density | tonnage +-6 % | quarry bulk-density data (Type 4 supply) | - |

## 8. References

* Garmin Ltd / Navionics (2026). Marine Maps web viewer, SonarChart and Nautical Charts. https://maps.garmin.com/en-US/marine, accessed 2026-10-07. Not to be used for navigation.
* EMODnet Bathymetry Consortium (2024). EMODnet Digital Bathymetry (DTM 2024). https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1. CC BY 4.0.
* Esri (2012-2024). World Imagery (Wayback dates 2012-10-27, 2013-06-04, 2022-08-25, 2024-09-17). https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer.
* Hansford, M. (2011). Borth's Big Dig. New Civil Engineer, 15 September 2011. https://www.newcivilengineer.com/archive/borths-big-dig-15-09-2011/.
* Haskoning UK Ltd (2010-11). Borth Coastal Protection Scheme - Phase 1, drawings 9V5090/1001, 1020, 1021, 1022, 1023 rev C1. Ceredigion County Council; published at borthcommunity.info.
* National Tidal and Sea Level Facility (n.d.). Chart datum and ordnance datum. https://ntslf.org/tides/datum.
* RCAHMW (2020). Coflein, Coastal Defences, Borth, NPRN 424699. https://coflein.gov.uk/en/site/424699.
* Rigden, T., Stewart, T., Allsop, W. and Johnson, A. (2013). Surf reefs - physical modelling results, not pipe dreams. HR Wallingford report HRPP576; ICE Coasts, Marine Structures and Breakwaters, Edinburgh.
* Royal HaskoningDHV (2011). West of Wales Shoreline Management Plan 2, Section 4 Coastal Area C Introduction, p. 4C.3 (report 9T9001).
* Royal HaskoningDHV (2013). Ceredigion Beach Profile Monitoring Volume I, 2012-2013 survey, report 9W1559, section 2.15 Borth LiDAR.
* Welsh Government (2022). LiDAR 2020-22, 1 m DSM/DTM, tile SN6089 (flown 19 March 2022). DataMapWales; Open Government Licence. https://datamap.gov.wales/.

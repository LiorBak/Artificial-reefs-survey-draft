# REQUESTS FOR LIOR - Palm Beach Reef (Gold Coast), 3D model (2026-10-05)

What the model already has: plan outline (verified, high), crest level -1.5 m MSL (four sources), tide planes (Maritime Safety Queensland), a seabed from the Garmin Navionics SonarChart (I read it myself in my own headless Chrome; no login, no CAPTCHA) cross-checked against the aerial's contour lines, and a reef surface from those contour lines.
What I could NOT read, and could not find anywhere online, is below. The model is already built with stated assumptions; each row says what it would change. Nothing here is needed to open the viewer.

All coordinates are decimal degrees, WGS84 (lat, lon); `x, y` are metres in the model frame (+x alongshore toward 334.3 deg true, +y offshore toward 64.3 deg). The points were computed from `shape.json` (reef outline) through the frame check in `build_3d.py` (vertex check: 47 of 47 vertices reproduce the lat/lon polygon to 0.02 m).

## A. Navionics app (phone / tablet; SonarChart layer ON, depth units METRES)

Tap each point and read the depth label (long-press shows a depth at the pin). Note for every reading: the time of day, whether the app says the depth is "chart datum" / "tide corrected", and the app's tide station name and the predicted tide height at that time (Settings > Tides & currents). One reading of the tide per session is enough.

| # | tool | exact lat/lon | what to read | datum / units to note | why it matters for the model |
|---|---|---|---|---|---|
| A1 | Navionics app | -28.107442, 153.470670 (crest centre) | depth at the pin, and whether the app draws any contour or label over the reef | m; "chart datum"? time + tide height | the crest: model -1.5 m MSL = 0.62 m below LAT; the web chart (without the reef) would give 4.1 m here and shows only the label "FISH HAVEN 1.5MT" |
| A2 | Navionics app | tap the fish-haven symbol at -28.107475, 153.470822 | the pop-up text (name, "min depth", source, date) | m; datum stated? | the web chart shows 1.5 m; the design gives 0.62 m below LAT. If the app says the minimum depth is below chart datum (LAT), the structure is 0.88 m deeper than the design; if the app says MSL, the two agree |
| A3 | Navionics app | -28.107427, 153.470064 (toe nearest the beach) | depth | m | landward toe: model -4.35 m MSL (3.5 m below LAT); chart-interpolated bed 3.8 m below LAT |
| A4 | Navionics app | -28.107265, 153.471661 (toe farthest offshore) | depth | m | seaward toe: model -7.0 m MSL (6.1 m below LAT); chart-interpolated bed 6.0 m below LAT; this toe fixes the reef height at the seaward end (crest to toe 5.5 m) |
| A5 | Navionics app | -28.107723, 153.471586 (SSE toe) and -28.106895, 153.470319 (NNW toe) | depth at each | m | flank toes: the model's toe is 0.5-0.7 m deeper than the chart's seabed at the SSE side and 0.4 m shallower on the NNW side (datum or scour) |
| A6 | Navionics app | -28.107584, 153.469697 (40 m shoreward of the reef) and -28.107030, 153.472211 (60 m seaward) | depth at each | m | natural seabed next to the reef, free of rock (my chart reading: 3.1 m and 7.7 m below LAT): the check of the whole datum assumption (chart datum = LAT) |
| A7 | Navionics app | -28.105950, 153.470166 and -28.108715, 153.471666 (about 170 m up-coast / down-coast of the reef, same distance offshore as the reef centre) | depth at each | m | alongshore uniformity of the seabed (my chart reading: 5.5 m up-coast, 4.7 m down-coast below LAT; the model uses the chart's own contours, no extra trend) |

## B. Google Earth Pro

| # | tool | exact lat/lon or place | what to read | datum / units to note | why it matters for the model |
|---|---|---|---|---|---|
| B1 | Google Earth Pro, historical imagery slider | centred on -28.107334, 153.470913, 400 m box | every image date from mid-2019 (construction) to now in which the rock mound or its breaking-wave line is visible; for the clearest low-tide image: the date and time | image date (dd mmm yyyy), tide state (wet sand line vs. dune) | whether anything changed after construction (rock loss, slumping, top-up): the model is "as built, no later works found" |
| B2 | Google Earth Pro, ruler (path) | from the NE-most corner of the dark rock (about -28.107265, 153.471661) to the water's edge on the same image, along bearing 245 deg | distance (m) and the date and tide of the image | m | the model measures the offshore distance from the waterline of 2025-12-01 (225 m nearest, 374 m farthest); the quoted "270 m" is measured from the beach; a ruler reading on a low-tide image tells the true low-water distance |
| B3 | Google Earth Pro, ruler | along the crest slot, from -28.107342, 153.470238 to -28.107475, 153.470822 | length (m) | m | 59 m expected; confirms that the rock actually visible at low tide is where the model puts the crest (visibility = depth) |
| B4 | Google Earth Pro, historical imagery | same place, the first image AFTER cyclone Alfred (March 2025) and the one before it | dates | dd mmm yyyy | the only storm check I could make is the 2025-12-01 Esri image (rock still there); a before/after pair would settle 'no damage' |

## C. Not a tool of yours (optional, only if you want the survey-grade number)

| # | tool | what | datum | why |
|---|---|---|---|---|
| C1 | e-mail to City of Gold Coast (Palm Beach Shoreline Project team) | the "Palm Beach Reef Design Reference Report" (Royal HaskoningDHV) and the final as-built multibeam survey (ICCE 2022 Fig 4 was made from it) as a point cloud or contour PDF; and the meaning/units of the asset-register fields HEIGHT_M = 5 and VOLUME = 33,000 | m vs AHD or LAT? | would replace the inferred seabed and contour interval with surveyed values and settle the 20-33 % gap between the register and the model |
| C2 | Gold Coast DTM (data.gov.au, City of Gold Coast, CC BY 2.5 AU, 4.1 GB file geodatabase, "includes bathymetry in certain areas") | download and open the layer around the reef (needs your go-ahead: size) | AHD | if it contains Palm Beach nearshore soundings, it replaces the Navionics seabed |

## D. Not needed from you
Tide planes (MSQ 2026 table fetched and read), the contour interval (inferred twice, see METHODS_3D.md 4.2), the plan outline, the frame and handedness check. No Haifa / Israel tide preset (local tides only).

# REQUESTS FOR LIOR - Pratte's Reef (El Segundo), 3D model (updated 2026-10-05, revision 3)

What the model already has: tide datums (NOAA), seabed (NOAA 1/3 arc-second DEM, checked against Garmin Navionics depth labels and the beds in the 2003 paper), crest depth (the 2003 paper's "approximately - 6 ft MLLW" at the outermost point; the drawing's "-6' MSL" as the alternative), plan outline (verified design layout), position (inferred from the paper's Fig. 9 survey window, +-100 m).
What I could NOT read, and could not find anywhere online, is listed here. The model is already built with stated assumptions; each row says what it would change.

All coordinates are decimal degrees, WGS84 (lat, lon). Points marked "hypothetical reef" are where parts of the reef would be IF the reef centre is at the inferred position 33.92058, -118.43335 (+-100 m); a depth reading at such a point is still a valid seabed reading whatever the true reef position is.

## A. Where was the reef, and what did it look like as built?

| # | tool | exact lat/lon or place | what to read | datum / units to note | why it matters for the model |
|---|---|---|---|---|---|
| A1 | Google Earth Pro, historical imagery slider | Dockweiler State Beach, El Segundo, centred on 33.92058, -118.43335; look 100-300 m offshore (west-south-west of the beach); the Hyperion 1-mile outfall comes ashore about 33.9231, -118.4337 (north) and the Grand Street groin is at about 33.91685, -118.43030 (south) | the date of every image from Oct 2000 to Oct 2010 in which the V-shaped reef (or its sand halo / darker patch / breaking-wave line) can be seen; for the clearest one: add placemarks on the V apex (offshore point) and the two arm tips and copy their lat/lon; the image date; whether the tide looks low | WGS84 decimal degrees; image date (day if shown) | confirms or corrects the inferred position (+-100 m) and may show the as-built footprint, which would replace the design drawing (the one input that is only a design) |
| A2 | Google Earth Pro, ruler (path tool) | from the V apex placemark (A1) to the nearest point of the water's edge in the SAME image, along the shore-normal (bearing about 65 degrees) | distance in metres; the bearing the ruler shows | metres; image date, wet/dry sand at the edge | the distance offshore (model: 91.44 m from the MSL waterline from the text '100 yards'; the paper's profiles give 72-94 m; each 25 m moves the seabed depth by 0.8 m) |
| A3 | Google Earth Pro, ruler | (a) from the 1-mile outfall landfall (33.9231, -118.4337; check it on the imagery) to the apex placemark; (b) from the groin at 33.91685, -118.43030 to the apex | distance (m) and compass direction for both | metres; degrees true | the paper says about 200 m from the outfall, its Fig. 2 scale gives 325 m, the groin-based estimate puts the reef 160 m further north; this settles the along-shore position |
| A4 | Borrero & Nelsen (2003) - **RESOLVED 2026-10-05**: you supplied the paper. It holds no as-built plan (Fig. 4 is the design drawing again); it gave the crest datum (6 ft MLLW), bag size, dates, the Fig. 9 UTM survey window and the centreline profiles (see METHODS_3D.md 3.10-3.11) | - | - | - | - |
| A5 | e-mail to the authors of the paper (their addresses are in the footnotes of p.1 of the PDF; they date from 2003 and may be out of date): J.C. Borrero (USC / eCoast) and C. Nelsen (Surfrider Foundation) | - | ask for: (1) the datum and units of Figs 5-9 (Fig. 5 and Fig. 7/8 differ by 1.44 m and 5.5 m for the same Oct 2001 profile), (2) the horizontal datum of the UTM coordinates of Fig. 9, (3) where the reef lies inside the Fig. 9 window, (4) the raw bathymetry / profile files of the first survey after Phase I (Oct 2000), (5) any as-built sketch, bag count per row or number of courses of Phase I | stated in the reply | would settle the datum ambiguity of the paper's profiles, fix the position to a few metres and give the as-built stack height (the volume gap of 250-430 m3 depends on it) |

## B. Seabed depth (cross-check of the DEM and of my reading of the chart)

Navionics app (phone/tablet, SonarChart layer ON; set depth units to feet or metres and say which). Tap the point and read the depth label; if the app shows the date/time and a tide-correction note, copy it. My own readings come from the Garmin web viewer (labels read directly; contour counting beyond 6 ft is uncertain by +-2 lines).

| # | tool | exact lat/lon | what to read | datum / units to note | why it matters |
|---|---|---|---|---|---|
| B1 | Navionics app | 33.92080, -118.43277 (0 ft line: about 59 m shoreward of the inferred reef position) | depth at the point (should read about 0-1 ft if my counting is right) | ft or m; whether the app says the depth is "chart datum" / "tide corrected"; time of day | tests my reading of the 0 ft line and the datum assumption (MLLW) |
| B2 | Navionics app | 33.92058, -118.43335 (inferred reef position, s = 0) | depth (my reading: about 10 ft = 3.1 m) | same | seabed under the reef centre |
| B3 | Navionics app | 33.92048, -118.43360 (+25 m seaward) | depth (my reading: about 11 ft) | same | toe of the offshore face |
| B4 | Navionics app | 33.92029, -118.43409 (+75 m seaward) | depth (my reading: about 14.5 ft; the printed label '15' lies near here) | same | slope seaward of the reef |
| B5 | Navionics app | 33.92001, -118.43482 (+150 m seaward) | depth (my reading: about 21 ft; the DEM is about 0.7 m deeper than the chart in this zone) | same | the offshore part where Navionics and the DEM differ most |
| B6 | Navionics app | arm tips 33.92039, -118.43309 and 33.92087, -118.43334; apex 33.92057, -118.43349 (hypothetical reef) | depth at each | same | the three corners of the reef: tests the assumption that the top follows the seabed (tips shallower than the apex by about 0.9 m) |
| B7 | Navionics app | anywhere on this stretch, same hour as the readings | the app's tide-station name and the predicted tide height at the time of reading (Settings > Tides & currents) | m or ft above chart datum | converts a tide-corrected depth to the chart datum (MLLW) and settles whether the app depth is tide-corrected |

## C. Crest of the built reef (not found anywhere)

| # | tool | place | what to read | datum / units | why |
|---|---|---|---|---|---|
| C1 | Surfrider Foundation LA / Coastal Frontiers Corp. (e-mail; not an app) | request the 2000-2008 monitoring surveys and the 2008 removal mapping | any crest depth along the arms, the apex, the bag layout actually built and the number of courses | state the datum (MLLW / MSL / NGVD29) | the model has one as-built crest number (6 ft MLLW at the outermost point) and a design label (-6' MSL) 0.85 m apart; the 110 bags need 250-430 m3 more volume than the single-course model holds |

## D. Not needed from you
Tide datums (NOAA CO-OPS 9410840 and 9410660, fetched and cross-checked), the NOAA DEM, the CCC, ICCE and Borrero & Nelsen texts: done. No Haifa / Israel tide preset (local tides only).

# METHODS_3D - Pratte's Reef (El Segundo, California): three-dimensional model

Built 2026-10-05 by `build_3d.py` (numbers in this note are filled in by that script from `shape.json`, the NOAA files in `src/`, `src/navionics/nav_transect.json` and `src/bn2003_digitised.json`; edit `METHODS_3D.template.md`, not this file). Companion notes: `SOURCES_3D.md` (running log of what was read where), `REQUESTS_FOR_LIOR.md` (what could not be read), `annotated/A1-A17` (the sources with the readings marked). Revision 3: the 2003 monitoring paper of Borrero & Nelsen, supplied by Lior, is now used (sections 3.10, 3.11).

## 1. Summary

The model shows **Pratte's Reef as built in Phase I (22 September 2000)**: a V of two bag arms (two arms at 45 deg to the shore normal and a 5 x 5 bag apex block; 435.2 m2, 58.0 x 28.6 m) on the nearshore seabed of Dockweiler Beach, with the water surface at any tidal datum from LAT to HAT. The footprint is the verified Skelly Engineering **design layout** of fall 2000: the 2003 monitoring paper reprints the same drawing as its Fig. 4 and contains no as-built plan. The top is fixed by the only as-built crest number, which the paper gives as "approximately - 6 ft MLLW" at the outermost point (= -2.678 m relative to MSL, datum confirmed as MLLW); it follows the seabed at a constant thickness of 1.349 m, which is one 1.2 m bag course. The seabed is the NOAA 1/3 arc-second DEM (primary), checked against Garmin Navionics SonarChart depth labels and against the beds in the paper's profiles; tides are NOAA CO-OPS Santa Monica. The position (+-100 m) is now inferred from the georeferenced survey window of the paper (33.92058 N, 118.43335 W). Later events are **not modelled** and appear in the caption only: Phase II (23-24 April 2001, +90 bags placed on top, crest widened and made shallower to within 3 ft of MLLW, -1.763 m MSL, eroded by about 1.45 m by September 2002), and removal in two phases (fall 2008 and fall 2010). The 3D confidence is **LOW**: every number has a source and the datums, bag size, dates, position and seabed slope are well supported, but there is still no as-built plan, the stack height is not stated anywhere, the single-course model holds 443 m3 against 695-782 m3 (80-90 % fill) or 869 m3 (nominal) for 110 bags, the Phase I crest is one point that differs by 0.849 m from the design reading, and the vertical uncertainty (+-0.85 m) is more than half the reef height (1.35 m).

## 2. Data sources

Access dates are 2026-10-05 unless stated. "Licence" is the licence stated by the publisher; reuse of every private research copy is NOT cleared for public release.

| id | reference (author-year) | what it contributed | resolution / date | licence |
|---|---|---|---|---|
| S10 | Borrero, J.C. & Nelsen, C. (2003). Results of a comprehensive monitoring program at Pratte's Reef. In: Black, K. & Mead, S. (eds), *Proceedings of the 3rd International Surfing Reef Symposium*, Raglan, New Zealand. File `src/borrero_nelsen_2003_prattes_monitoring_results.pdf`, 16 pp., supplied by Lior on 2026-10-05 (his `Downloads\Pratte_results.pdf`; original URL unknown). Page 1 title *Results of a comprehensive monitoring program at Pratte's Reef*, authors J.C. Borrero (USC) and C. Nelsen (Surfrider Foundation); **the file prints neither venue nor year** (the PDF metadata title is *2 Years of Pratte's Reef: Performance and Considerations for Future Artificial Reef Endeavors in Santa Monica Bay*, re-saved 2020-11-03); venue and year are those of the citation R23 in `shape.json`, consistent with the content (monitoring to Oct 2002) | bag size, counts and dates; Phase I crest depth (6 ft MLLW) and Phase II crest (3 ft MLLW); the design drawing (Fig. 4); position text, aerial (Fig. 2) and a georeferenced bathymetry window (Fig. 9); centreline profiles after Phase II (Figs 5-8) | text; Figs 5, 7, 9 vector graphics (digitised from the PDF paths), Figs 2, 4, 8 rasters (432 x 231, 371 x 468, 969 x 560 px); survey Oct 2000 - Sept 2002 | copyright holder; private research copy |
| P1 | Skelly Engineering (c. 2000). *Pratte's Reef* plan-view design drawing (110 bags + 30 optional), as reproduced by Raised Water Research (2019). https://raisedwaterresearch.com/wp-content/uploads/2019/07/Pratts-Reef-Diagram.png. Outline traced and verified in `shape.json` (this project, verified 2026-10-04); the same drawing is Fig. 4 of S10 | plan outline (76 vertices), design crest label "TOP OF BAG MIN DEPTH -6' MSL" at both arm tips, scale bar 0-90 ft | raster 308 x 385 px, 5.155 px/m; drawing c. fall 2000 | unknown / all rights reserved (private copy) |
| S1 | California Coastal Commission (1998). *Staff report W5a, application E-98-15 (Surfrider Foundation - Pratte's Reef)*, hearing 13 Oct 1998; Exhibits 2 and 3 by Skelly Engineering (1997, 1996). https://documents.coastal.ca.gov/reports/1998/10/W5a-10-1998.pdf | text distance (300 yd north of the Grand Avenue jetty, 100 yd offshore, "15 feet of water (MSL)"), tidal labels MHHW +2.6 ft and MLLW -2.8 ft MSL, concept section | text and 1996-97 sketches, not to scale | public agency record, terms not stated |
| S2 | Borrero, J.C., Mead, S.T. & Moores, A. (2010). Stability considerations and case studies of submerged structures constructed from large, sand filled, geotextile containers. *Coastal Engineering Proceedings* 1(32), structures.60 (ICCE 2010, Shanghai). https://doi.org/10.9753/icce.v32.structures.60 | the same crest depths in metres (1.8 m and 1 m), bag size, 80-90 % fill, 2002 survey, removal late 2008 | text, p.2 Fig. 1 and p.7; 2010 | CC BY 4.0 (ICCE-OJS record) |
| S3 | Raised Water Research (n.d.). *Pratte's Reef*. https://raisedwaterresearch.com/spot/artificial-reef/us/california/prattes-reef/ | Phase II bags "placed on top of the existing bags"; "roughly 100 meters" offshore; "rose from about 5m deep" (datum not stated) | web page | unknown |
| S4 | NOAA CO-OPS (2026). *Tidal datums, station 9410840 Santa Monica, CA* (34.0083 N, 118.5 W; 11.7 km from the site), epoch 1983-2001. https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/9410840/datums.json?units=metric | MSL, MLLW, MHW, MHHW, MLW, NAVD88, LAT, HAT (m above station datum) | epoch 1983-2001; LAT/HAT from the station record | NOAA, public domain |
| S8 | NOAA CO-OPS (2026). *Tidal datums, station 9410660 Los Angeles Outer Harbor, CA* (33.72 N, 118.272 W; 26.6 km from the site), epoch 1983-2001. https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/9410660/datums.json?units=metric | cross-check of MSL - MLLW (0.861 m vs 0.849 m) | as S4 | public domain |
| S5 | NOAA National Geophysical Data Center (2010). *Santa Monica, California 1/3 arc-second NAVD 88 Coastal Digital Elevation Model*. NOAA National Centers for Environmental Information, metadata gov.noaa.ngdc.mgg.dem:726 (published 2010-03-12). https://www.ngdc.noaa.gov/metaview/page?xml=NOAA/NESDIS/NGDC/MGG/DEM/iso/xml/726.xml. Read through the NCEI ImageServer (`DEM_mosaics/DEM_all`, raster id 173) as a 216 x 270 px float32 export, `src/export_dem.py` | seabed profile (primary) | cell 1/3 arc-second (about 10 m); sources dated 1932-2009 (NOS soundings, multibeam 1992-2008, SHOALS lidar 2002-2007); "not to be used for navigation" | NOAA, public domain |
| S6 | NOAA National Geophysical Data Center (2012/2013). *U.S. Coastal Relief Model - Southern California v2*, 1 arc-second, MSL datum. doi:10.7289/V5V985ZM | independent check of the DEM | 1 arc-second (about 30 m) | public domain |
| S7 | Garmin Navionics (2026). *Marine Maps web viewer*, SonarChart Maps and Nautical Charts layers (https://webapp.navionics.com/ redirects to https://maps.garmin.com/en-US/marine/). Screenshots in `src/navionics/` (two captures: the new position and the earlier text hint, `hint1_33.9188_-118.4324/`) | independent seabed: 24 one-foot contours along a shore-normal transect, 24 depth labels / spot soundings, outfall landfall | zoom 18 (max), 0.4955 m/px; survey dates not shown; depth datum and contour interval not stated by the app | (c) Garmin; private research copy; "Not to be used for navigation" |
| S9 | Reef card `02_research/reefs/prattes-reef-el-segundo.json` (this project; verified 2026-09-25), citing Surfrider Foundation news, Coastal Frontiers Corp. (https://www.coastalfrontiers.com/removal-of-prattes-reef) and Surfline (2008) | removal dates: Phase I removal 30 Sept-17 Oct 2008, remaining bags fall 2010 | not re-fetched in this run | n/a |

### 2.1 Chronology of the structure (state modelled and what is not)

| date | event | modelled? | source |
|---|---|---|---|
| 1996-1998 | concept of about 30 large bags, CCC permit hearing 13 Oct 1998 | no (superseded design) | S1 |
| 22 September 2000 | **Phase I installed**: 110 sand-filled geotextile bags (4 x 7 x 10 ft) filled at the Port of Los Angeles and placed by barge-mounted crane in an obtuse V with the apex offshore; outermost point approximately 6 ft below MLLW | **yes** | S10 p.2 |
| October 2000 | first bathymetric survey (Fig. 9, dashed contours); November 2000 profile before any significant swell | no | S10 pp.5, 7 |
| winter 2000-01 | Phase I bags largely covered by sand that moved offshore | no | S10 p.3 |
| 23-24 April 2001 | Phase II: 90 bags placed directly over Phase I, volume +80 %, crest widened and made shallower (to within 3 ft of MLLW) | no (later change; caption only) | S10 p.3 |
| May 2001 - Sept 2002 | crest of the widened reef eroded by about 1.45 m (Fig. 8); by October 2002 the bags were mostly level with the sand | no | S10 Fig. 8, p.16 |
| August 2002 | dive survey: several bags ripped, losing fill | no | S10 p.8; S2 |
| fall 2008 | removal of the mostly buried remnants begins (30 Sept-17 Oct) | no | S2, S9 |
| fall 2010 | removal completed at permit expiry | no | S9 |

## 3. Methods

### 3.1 Coordinate frame and orientation

The model frame is the canonical frame of `shape.json`: metres, **x alongshore** toward bearing 155 deg (SSE), **y offshore** toward bearing 245 deg (WSW) = x turned 90 deg clockwise, **z up**, z = 0 at mean sea level (MSL, epoch 1983-2001). The origin is the MSL waterline on the V axis; the reef centroid is at y = 91.44 m (text value, assumption A2). (x, y, z-up) is left-handed; the viewer therefore maps model (x, y, z) to three.js (X, Y, Z) = (x, z, y), which is mirror-free (looking toward the beach from the sea, x runs to the right).

Pixel to metre on the Skelly drawing (img1, 5.1549 px/m from the printed scale bar, origin (ox, oy) = (628.5, 156.2) px, `shape.json` `transform_note`):

```
x = (py - oy) / 5.1549          y = -(px - ox) / 5.1549          (origin placed so that the polygon centroid is at x = 0, y = 91.44 m)
```

Frame to compass (bx = 155 deg, by = bx + 90 = 245 deg) and to latitude/longitude (used only for the Navionics and DEM sampling and for the position hint):

```
E = x sin(bx) + y sin(by)     N = x cos(bx) + y cos(by)         (metres east / north)
lat = lat0 + N / 111132       lon = lon0 + E / (111320 cos(lat0))    (lat0, lon0 = 33.92058, -118.43335)
north in the model frame = (cos bx, cos by) = (-0.906, -0.423)
```

Orientation (assumption A1): the drawing has no north arrow; its horizontal "wave direction" axis is taken as the shore normal. Support: the present shoreline fitted on the 2026-01-09 Esri image has bearing 155.5 deg (own RANSAC fit, +-2 deg); the 1996 concept plan has its V bisector at 61 deg (onshore; shore normal 65 deg); the Navionics 0 ft line trends about 158 deg; and the eight depth contours of the 2003 survey (Fig. 9) have a mean true bearing of 154.3 deg (spread 6.1 deg between contours; UTM convergence -0.8 deg applied). Stated uncertainty +-5 deg.

### 3.2 Vertical datums and conversions

All NOAA datum values are heights above the station datum (STND) of the gauge, so with `h` a height above STND at the gauge:

```
z_MSL = h - MSL                                         (E1)
depth d below datum D  ->  z_MSL = -d - (MSL - D)       (E2)    D in {MLLW, LAT, NAVD88}
MSL - MLLW  = 1.594 - 0.745 = 0.849 m (Santa Monica 9410840);  0.861 m (Los Angeles 9410660)     (E3)
MSL - NAVD88 = 1.594 - 0.802 = 0.792 m     z_MSL = z_NAVD88 - 0.792     (E4)
```

Datum levels used (z relative to MSL, metres): HAT 1.382, MHHW 0.804, MHW 0.579, MSL 0, MLW -0.566, MLLW -0.849, LAT -1.469; MHHW - MLLW = 1.653 m. Crest and water depths below LAT use `D_LAT = z_LAT - z` (positive = below LAT).

Crest readings converted with E2/E3 (A = drawing, datum label MSL; B, C = Borrero & Nelsen 2003, datum MLLW):

```
A:  z = -6 ft x 0.3048 = -1.829 m MSL  = -0.98 m rel. MLLW  (0.98 m below MLLW; with 9410660: 0.968 m)            (E5)
B:  z = -(6 ft x 0.3048 + 0.849) = -(1.829 + 0.849) = -2.678 m MSL     [ICCE 2010 rounds 6 ft to 1.8 m: -2.649 m, -0.029 m apart]   (E6)
C:  z = -(3 ft x 0.3048 + 0.849) = -1.763 m MSL   (after Phase II; NOT modelled)                                         (E7)
```

A and B are the same number (6 ft) with different datum labels (the drawing says MSL, the paper says MLLW); they differ by exactly MSL - MLLW = 0.849 m. The paper does not say which label is right. The drawing's "MSL" is the local NOAA mean sea level: CCC Exhibit 2 (Skelly, June 1997) prints MHHW +2.6 ft and MLLW -2.8 ft relative to MSL, and NOAA gives +2.64 ft and -2.79 ft (differences 0.01 m), see validation V1.

### 3.3 Plan shape

The toe polygon (76 vertices, 435.2 m2) is read unchanged from `shape.json` (status verified, verified 2026-10-04, md5 2ce341598d22b61dac771292388e8935); only the solid-outline bags of the drawing are included (the 30 dashed "optional" bags are excluded; including them would add an estimated 15-20 % area). It is the *design* layout of Phase I (assumption A9): the 2003 paper reprints it as Fig. 4 ("The design layout of Pratte's Reef", annotated figure A13) and shows no later layout; bags were crane-placed, moved, sank and were buried, so the real footprint differed from it by metres.

### 3.4 Seabed from the NOAA DEM (primary)

For each of 31 alongshore stations x_k = -150, -140, ... +150 m about the position hint (33.92058 N, 118.43335 W) the DEM was sampled (bilinear in the 1/3 arc-second grid) every 1 m along bearing 245 deg for s = -300 ... +500 m, converted with E4, and the most seaward z_MSL = 0 crossing with s < 150 m was taken as that station's MSL waterline s_w,k (linear interpolation). Each profile was then re-expressed relative to its own waterline and the mean and standard deviation over the stations were kept (5 m steps):

```
z_k(y) = z_MSL( s_w,k + y )        zbar(y) = (1/31) sum_k z_k(y)        sd(y) = std_k z_k(y)       y = -60 ... 300 m   (E8)
```

The mean MSL waterline lies at s = -101.9 m along the transect (sd 5.4 m), i.e. the hint is 101.9 m seaward of the DEM's MSL waterline. The seabed is thus **alongshore uniform** (assumption A3; sd at the reef 0.14 m): z(y = 91.44 m) = -3.67 m, z(tips, y = 74.65 m) = -3.13 m, z(apex, y = 103.28 m) = -4.03 m, slope 1:32.0 over the reef. The same procedure about the earlier text hint (33.9188 N, 118.4324 W, 217 m away) gave z(91.44 m) = -3.75 m (sd 0.18 m): a 0.08 m difference, which is the practical test of A3. The DEM is the seabed without the reef (6 x 3 cells; removed 2008-2010). Between nodes the model interpolates linearly in y.

### 3.5 Seabed from Navionics SonarChart (independent check, selectable)

*Access.* Navionics' web chart (webapp.navionics.com) now redirects to Garmin's Marine Maps viewer. In my own headless Chrome (DevTools protocol, a random free port and a fresh temporary profile; the process was terminated afterwards) the page loaded without login, CAPTCHA or consent dialog; nothing was accepted or bypassed. The map was centred on the position hint with Leaflet `setView` at zoom 17 and 18 (the maximum), with options View = Map, Chart type = SonarChart Maps or Nautical Charts, Depth units = Feet, Seabed areas = Hide, Shallow shading = 6 ft (default). Two captures exist: the first at the earlier text hint (`src/navionics/hint1_...`), the second at the new hint. Screenshots are private research copies ("Not to be used for navigation") and were analysed offline.

*Scale.* Web-Mercator, 256 px tiles: `res = 156543.034 cos(lat) / 2^zoom` = 0.4955 m/px at zoom 18.

*Counting.* Along the shore-normal line (bearing 245 deg) through the screenshot centre the screenshot was sampled every 0.25 px; dark pixels (max RGB < 175) that belong to long connected components (>= 30 px: contour lines, not label glyphs or chart symbols) are contour lines; runs closer than 0.8 m were merged. Contour index 0 is the first line within 3 m of the seaward edge of the green "drying" band (the 0 ft contour, s = -59.17 m); index n is the n-th line seaward (24 lines to s = 200.88 m). The 1 ft interval is *inferred*: the seven lines 0-6 bound the 6 ft shallow-shading band. **The counting is only partly reliable at the new position**: the printed depth labels 1, 4 and 5 ft are reproduced exactly, but only 4 of 12 labels overall (the 7-11 ft lines crowd, and symbols interrupt lines), so the count carries +-2 lines (+-0.6 m) beyond 6 ft; the 15th line lies 10.5 m from the Nautical-layer spot sounding "15" ft.

*Conversion* (datum assumption A8: chart datum = MLLW, US convention; the app does not state it):

```
z_MSL(n) = -(n x 0.3048) - 0.849 m          y = y_hint + s = 101.9 + s            (E9)
```

*Datum test without counting.* Every printed depth label and spot sounding (24 points on both captures) was compared with the DEM at the same ground point. In the reef zone (labels 8-18 ft, n = 7) the bias (Navionics - DEM) is 0.142 m if the depths are below MLLW, 0.199 m if NAVD88, -0.478 m if LAT and 0.991 m if MSL (RMS 0.286 / 0.318 / 0.539 / 1.021 m): MSL and LAT are rejected; MLLW and NAVD88 are only 0.057 m apart and cannot be separated. Outside the reef zone the DEM is deeper than the chart by 0.922 m (surf zone, labels < 8 ft) and by 0.288 m (labels > 18 ft), assuming MLLW.

*Use.* Seabed only: the reef was removed (2008-2010) and no contour at the hint shows an anomaly, so the chart gives no crest or height information. In the viewer the Navionics profile can replace the DEM wherever it has contours (y = 43.0 m to the end of the model profile at 300 m); elsewhere the DEM is used.

### 3.6 Crest scenarios

Two scenarios are selectable; only B is the as-built Phase I and is the default.

* **B - Phase I as installed (Borrero & Nelsen 2003 p.2).** "After the initial installation, the depth at the outermost point of the reef was approximately - 6 ft MLLW". The outermost point is read as the offshore face of the V apex block. Its elevation z_B = -2.678 m is the top of the reef at y = y_apex = 103.28 m; the top is carried along the reef at constant thickness above the bed (assumption A4):
  `h_top = max( z_B - z_bed(y_apex), 1.2 m ) = 1.349 m`  (1.12 bag courses of 1.2 m). Tops are then -2.678 m MSL at the apex (1.83 m below MLLW, 1.21 m below LAT) and -1.784 m at the arm tips (0.94 m below MLLW, 0.32 m below LAT).
* **A - design minimum depth (Skelly).** Level crest at z_A = -1.829 m MSL: `h_top(y) = max( z_A - z_bed(y), 1.2 m )` = 1.3 m at the tips and 2.2 m (1.83 courses) at the apex. Crest 0.36 m below LAT.
* **C - after Phase II** (-1.763 m MSL, 0.294 m below LAT; "within 3 ft of MLLW"): later change, **not modelled**. The paper's profiles show that the widened reef was far wider at the centreline than the Phase I outline (section 3.11).

### 3.7 Reef surface

With d_in(x, y) the distance from a point inside the toe polygon to the polygon boundary and s the horizontal run per metre of rise of the side slope (assumption A5, default s = 1.0, range 0.5-2.5):

```
h(x, y)  =  max( 0 , min( h_top , d_in(x, y) / s ) )                    inside the toe polygon
z_surface = z_bed(y) + h(x, y)                                           (E10)
V = sum over a 0.25 m grid of h x (0.25 m)^2                              (E11)
```

The surface is a smooth height field (no individual bags). The viewer meshes it on a 0.4 m grid; the polygon outline is drawn separately at the seabed. The reef can be moved along y (reef-centre slider, 60-130 m): the seabed under it and, in state B, the thickness change accordingly.

### 3.8 Water

A translucent plane at the selected level: LAT, MLLW, MLW, MSL, MHW, MHHW, HAT (E1/E3 values above). Local tides only.

### 3.9 Assumptions (numbered)

| id | assumption | basis | range / effect |
|---|---|---|---|
| A1 | the drawing's horizontal axis is the shore normal; x = 155 deg | shoreline fit 155.5 deg; Fig. 9 contours 154.3 deg; concept plan | +-5 deg: rotates the picture, no effect on depths |
| A2 | reef centroid 91.44 m from the MSL waterline | text "100 yards" (CCC), "roughly 100 m" (RWR); the paper's profiles give 72.3-94.3 m (V13) | +-25 m moves the seabed by +-0.78 m (slope 1:32.0); the hint gives 101.9 m |
| A3 | seabed uniform alongshore; mean DEM profile; reef absent from the DEM | alongshore sd 0.14 m (DEM), 0.39 m (Navionics, 7 transects); old and new hint differ by 0.08 m | hides bars and troughs of the 10 m grid |
| A4 | the 6 ft MLLW depth applies at the apex face; the top follows the bed at constant thickness | the tips' tops then agree with the design label (V6); the apex thickness is one bag course (V12); no other as-built crest value exists | tips top -1.784 m; a level crest at -2.678 m would leave only 0.46 m of reef at the tips (less than one bag) |
| A5 | bag-stack side slope s = 1.0 (0.5-2.5) | bag edge of a 1.2-1.5 m course; no cross-section of the Phase I reef | volume 443 m3 (B), range in section 5 |
| A6 | minimum thickness one 1.2 m course | bag height 4 ft (S10) | applies only if crest minus bed < 1.2 m |
| A7 | NOAA Santa Monica datums apply at the site; epoch 1983-2001; no sea-level trend applied | 11.7 km, same bay; LA harbour MSL-MLLW differs 0.012 m | +-0.03 m |
| A8 | Navionics chart datum = MLLW; contour interval 1 ft | US convention; label test (MSL and LAT rejected in the reef zone); 0-6 ft shading band | MLLW vs NAVD88 0.057 m; +-2 lines counting error beyond 6 ft |
| A9 | footprint = Phase I design layout (solid-outline bags only) | no as-built plan: the paper's Fig. 4 is the same drawing | metres; 30 optional bags excluded (+15-20 % area if built) |
| A10 | no settlement, scour or burial modelled | "largely covered in sand" (winter 2000-01) | the real structure sank and was buried |
| A11 | water is static at the chosen datum | - | no waves, set-up or surge |
| A12 | the vertical axis of the paper's Fig. 5 is MLLW-referenced | the zero line is labelled "Approx. Min Low Tide" and the high-tide line sits at +1.84 m (6 ft) | the paper's profile figures are used only for cross-checks (V13, V14), not for model numbers; if the axis were MSL the beds would be 0.85 m deeper |
| A13 | the reef lies within the Fig. 9 survey window; position = window centre, +-100 m | the paper puts the reef about 200 m south of the 1-mile outfall; the outfall-based estimate lies within 35 m of the window centre (section 3.10) | no effect on depths (A3); moves the picture only |

### 3.10 Position from the 2003 paper (new in revision 3)

The paper's Fig. 9 compares two bathymetric surveys (October 2000, four weeks after Phase I; March 2001) in a UTM frame. It is a vector graphic: the eight contour paths (-1 ... -4 m) and the axis ticks were read from the PDF (`bn_digitise.py`). Axis calibration from the tick marks (20 m spacing):

```
E = 367460 + (x_pt - 216.1) / 2.495        N = 3754240 + (309.5 - y_pt) / 2.485          (metres, UTM zone 11 N; datum not stated, NAD83/WGS84 assumed)   (E12)
window: E 367449-367560, N 3754239-3754310  ->  centre (367505, 3754275) = 33.92058 N, 118.43335 W (pyproj EPSG:32611 -> 4326)
```

The reef is not drawn in the figure and no contour shows a bag signature, but the paper says the offshore bathymetry has not changed "outside of the contours created by the reef bags themselves", and the window (about 112 x 71 m) is just large enough for the 58 x 29 m reef. Independent text evidence for the position: p.1 "approximately 200 m south of the Hyperion Sewage Treatment Plant's 1-mile outfall" and "within 500 m" of the outfall and the Grand Street jetty; Fig. 2 (aerial, range lines 550 m apart, scale 6.3 m per original pixel) places the reef chevron on range line 3, 325 m from the outfall and 672 m from the Grand Street jetty arrow. The outfall landfall was read on the Navionics chart (33.9231 N, 118.4337 W, +-20 m); 200 to 318 m south along 155 deg plus 91 m offshore gives 33.9202-33.9211 N, 118.4332-118.4337 W, within 35 m of the window centre. A jetty-based estimate (660 m north of the groin at 33.91685 N, 118.43030 W) gives 33.9219 N, 118.4342 W, 160 m further north. The three estimates span 190 m, so the hint is stated as +-100 m. The earlier text hint (33.9188 N, 118.4324 W, from the 1996-98 concept siting "300 yards north of the Grand Avenue jetty") lies 217 m away and is superseded. The survey is not a georeferenced outline of the reef, so `shape.json` keeps `geo = null`.

### 3.11 Profiles through the reef after Phase II (new in revision 3)

Figs 5 and 7 are vector graphics (curves read from the PDF paths), Fig. 8 a raster (read by eye). Calibration (tick marks):

```
Fig. 5:  d = (x_pt - 141.5) / 1.0980 m ;   z = (455.82 - y_pt) / 8.60 m           Fig. 7:  d = (x_pt - 143.63) / 1.1807 m ;   z = (135.23 - y_pt) / 8.844 m          (E13)
```

All profiles are along range line 3 (the reef centreline) from the dune base. Fig. 5 (Oct 2001) and Fig. 7/8 (Oct 2001) are the same data on shifted axes: Fig. 5 = Fig. 7 + 1.44 m vertically (peak and bed alike) and about 5.5 m horizontally. The vertical datum is not stated. Reading A12 (Fig. 5 zero = MLLW, from the tide lines) gives crest -0.51 m MLLW at d = 197.2 m, beds -2.63 m (landward) and -3.14 m (seaward) = -3.48 / -3.99 m MSL, relief 2.12 m above the landward bed and 2.21 m above the seaward bed, base width 29.4 m (the design apex block is only 10.6 m wide at the centreline: the widened Phase II reef was about three times as wide). The Fig. 7/8 axis is 1.44 m higher, equal to MHW - MLLW (1.43 m) or MSL - LAT (1.47 m); it cannot be decided from the paper. Fig. 8 gives the crest history on the Fig. 7/8 axis: May 2001 -1.77 m, October 2001 -1.94 m, February 2002 -2.64 m, September 2002 -3.22 m, i.e. 1.45 m of erosion in 16 months. The Phase I profile is NOT available: the November 2000 profile stops at d = 109 m, before the reef.

## 4. Validation (cross-checks performed)

| id | check | numbers | verdict |
|---|---|---|---|
| V1 | CCC Exhibit 2 tidal labels vs NOAA | MHHW +2.6 ft = +0.79 m vs +0.804 m; MLLW -2.8 ft = -0.85 m vs -0.849 m | agree to 0.01 m; confirms the drawing's "MSL" is the NOAA epoch MSL |
| V2 | datum transfer | MSL - MLLW 0.849 m (Santa Monica) vs 0.861 m (Los Angeles): 0.012 m apart | consistent (A7) |
| V3 | DEM vs Coastal Relief Model at y = 91.44 m | -3.67 vs -2.92 m MSL (-0.75 m) | CRM is 1 arc-second and shallower; both used in the spread (section 5) |
| V4 | DEM vs CCC text "15 feet of water (MSL)" = -4.57 m | the DEM reaches -4.57 m at y = 121.6 m, 30.2 m further out than 91.44 m | within about 1 sigma of A2 |
| V5 | DEM vs Navionics SonarChart (Navionics - DEM, MLLW assumed) | hint: -3.92 vs -3.99 m; reef zone +0.29 m (max 0.55); s = 40-150 m +0.66 m; s > 150 m +0.69 m; surf zone s < -17 m +0.88 m (max 1.00); label test in the reef zone 0.142 m (n = 7) | agree within 0.3 m over the reef; they diverge in the surf zone and offshore (beach morphology, survey dates, counting error) |
| V6 | tips: design label vs bed | one 1.2 m course on the DEM bed at the tips reaches -1.93 m vs the drawing's -1.829 m (-0.1 m); state B's tip top -1.784 m is 0.04 m from it | consistent within the uncertainty (not independent: both use the DEM bed) |
| V7 | bag volume | 3.0 x 2.13 x 1.2 m = 7.67 m3 vs 7.9 m3 stated (-2.9 %). Phase II: 90 / 110 bags = 0.82 vs "+80 %" stated. 200 bags x 7.9 = 1580 m3 vs "approximately 1600 m3" in the paper (nominal volume; at 80-90 % fill 1264-1422 m3) | consistent |
| V8 | **model volume vs 110 bags** | 110 bags: 869 m3 nominal, 695-782 m3 at 80-90 % fill; model B = 443 m3 (ratio 0.51 of nominal, 0.57-0.64 of the filled volume); model A = 550 m3 (ratio 0.63 nominal); with the Navionics bed B = 422 m3 | **FAILS for B; NOT resolved by the paper** (see below) |
| V9 | bag footprint vs outline | 110 bags x 6.39 m2 = 703 m2 of bag footprint vs 435.2 m2 outline: mean 1.62 layers | the outline cannot hold 110 single-layer bags |
| V10 | position vs chart coastline | the hint is 106.2 m from the Navionics coastline (text: 91.4 m); at 91.44 m from the chart coastline the chart depth is 7.11 ft = -3.02 m MSL | consistent (A2) |
| V11 | paper vs ICCE | "approximately - 6 ft MLLW" = 1.829 m vs ICCE's 1.8 m (-0.029 m); "within 3 ft of MLLW" = 0.914 m vs ICCE's "within 1 m" | ICCE (same first author) converted and rounded the paper's feet; datum MLLW confirmed |
| V12 | apex thickness vs bag height | z_B minus the DEM bed at the apex = 1.349 m vs bag height 1.2 m (1.12 courses) | the as-installed depth and the DEM bed give one bag course at the outermost point |
| V13 | reef distance from the MSL waterline in the paper's profile | crest 72.3 m, base centre 83.8 m (Fig. 5 as MLLW: MSL = +0.849 m at d = 124.9 m); 88.7 / 94.3 m if the Fig. 7 axis is MSL (zero crossing at d = 114.1 m); text 91.44 m | within +-25 m (A2) in either reading |
| V14 | beds beside the reef in the paper vs DEM | Fig. 5 (axis read as MLLW): -3.48 / -3.99 m MSL (mean -3.73) vs DEM -3.67 m at y = 91.44 and -4.03 m at the apex; Fig. 7/8 axis: -4.07 / -4.16 m | agree within 0.3 m (Fig. 5 reading); 0.4 m deeper if the Fig. 7 axis is MSL |
| V15 | Fig. 9 contour bearing | 154.3 deg true (sd 6.1 deg over 8 contours) vs the model's 155 deg | consistent (A1) |
| V16 | Fig. 9 contours vs NOAA DEM at the same points | survey value minus DEM z_MSL: 1.23 m (Oct 2000), 1.61 m (Mar 2001) | positions consistent; datum of Fig. 9 not stated (MLLW would give +0.85 m; the winter profile is steeper and seaward, the DEM has 10 m cells) |
| V17 | May 2001 crest vs "within 3 ft of MLLW" | Fig. 8 crest -1.77 m on its axis = -0.33 m on the Fig. 5 axis (MLLW) or -0.92 m MLLW if the axis is MSL; limit -0.914 m | holds in either reading |

*V8/V9 are an unresolved discrepancy, not a pass.* The single-course model B holds 252-339 m3 less than 110 bags at 80-90 % fill (about 38-50 bags) and 426 m3 less than the nominal volume. The paper does not give a stack height or layout, so it cannot close the gap; it removes one explanation: V12 shows one bag course at the outermost point, so a second course there is not supported. What remains: the 110 bags (703 m2 of bag footprint) did not fit in the 435.2 m2 traced outline (the drawing's arm bags overlap, 3.4 m2 per bag in `VERIFY.md`), or part of the structure was already two bags high elsewhere, or the bags were less full. Model A (level crest, up to 1.83 courses at the apex) is closer to the bag volume. This is why A stays selectable and why the confidence is low.

## 5. Uncertainty

Per input (all are 1-sigma-like ranges, not statistical intervals; where only readings exist I state my judgement):

| input | uncertainty | basis |
|---|---|---|
| outline | +-0.2 m, +-4 % area; scale bar +-3-5 % | `shape.json` verification |
| position along y | sigma_y = +-25.0 m | text distances; the paper's profiles give 72.3-94.3 m; hint vs text 101.9 vs 91.44 m |
| position along x | +-100 m; irrelevant to depth (uniform bed) | window half-length 56 m; outfall- and jetty-based estimates span 190 m |
| crest B reading | sigma_zc = +-0.3 m | "approximately 6 ft"; single point; datum transfer 0.012 m |
| crest A reading | +-0.15 m | integer-foot label; datum label disputed (A vs B differ by 0.849 m) |
| seabed depth at the reef | sigma_zb = +-0.8 m | sample SD of six estimates (0.83 m, table below); slope x sigma_y = 0.78 m |
| paper's profile axes | Fig. 5 vs Fig. 7/8: 1.44 m, datum unstated | A12 |
| tide datums | +-0.03 m (transfer), LAT +-0.05 m | S4, S8 |
| side slope s | 0.5-2.5 | A5 |

| estimate of the seabed depth at the nominal reef position | z (m MSL) |
|---|---|
| NOAA DEM at y = 91.44 m | -3.67 |
| NOAA CRM 1 arc-sec at y = 91.44 m | -2.92 |
| CCC 1998 text '15 feet (MSL)' | -4.57 |
| RWR text 'about 5 m deep' (datum not stated) | -5.00 |
| B&N 2003 Fig. 5: beds either side of the reef, Oct 2001 (axis read as MLLW) | -3.73 |
| Navionics SonarChart 91.44 m from the chart coastline (MLLW assumed) | -3.02 |

**Propagation** (independent errors added in quadrature):

```
reef height / thickness   H = z_c - z_b           sigma_H = sqrt( sigma_zc^2 + sigma_zb^2 ) = sqrt(0.3^2 + 0.8^2) = 0.85 m
seabed term               sigma_zb^2 ~ (slope x sigma_y)^2 + sigma_dem^2   (slope x sigma_y = 0.78 m; empirical SD 0.83 m)
crest depth below LAT     D_LAT = z_LAT - z_c    sigma_D = sqrt( sigma_zc^2 + sigma_LAT^2 ) = 0.30 m (B), 0.16 m (A)
water over the crest      d_c(T) = T - z_top     sigma_d = sqrt( sigma_T^2 + sigma_ztop^2 )      (T = tidal level)
volume                    sigma_V^2 = (dV/dh0 sigma_h0)^2 + (dV/dy sigma_y)^2 + (dV/ds sigma_s)^2
```

Numerically: state B, V = 443 m3 with half-differences 48 m3 (thickness +-0.3 m), 81 m3 (reef moved +-25 m) and 99 m3 (s 0.5-2.0), giving sigma_V = 136 m3; state A, V = 550 m3 with 24, 110, 164 m3, sigma_V = 199 m3. At +1 sigma (579 m3) state B is still below the 695-782 m3 of the filled bags; it reaches that range only at about +2 sigma (716 m3) and not even at +3 sigma (852 m3) the nominal 869 m3, so the volume gap is not just an uncertainty effect. Volume by slope run s (m3):

| state | s = 0.5 | 0.75 | **1.0** | 1.5 | 2.0 |
|---|---|---|---|---|---|
| B | 514 | 478 | 443 | 374 | 316 |
| A | 672 | 611 | 550 | 435 | 344 |

Sensitivity to the reef position (centroid moved along y):

| reef moved by (m) | seabed z under the centre (m MSL) | thickness state B (m) | crest height state A (m) |
|---|---|---|---|
| -25 | -2.87 | 1.20 | 1.04 |
| +0 | -3.67 | 1.35 | 1.84 |
| +25 | -4.42 | 2.09 | 2.59 |
| +40 | -4.85 | 2.50 | 3.02 |

So the crest (state B) is 1.21 +- 0.30 m below LAT at the apex; the water over the apex top ranges from 1.21 m (LAT) to 4.06 m (HAT) and over the tip tops from 0.32 m to 3.17 m (MHHW - LAT = 2.27 m); the reef height is 1.35 +- 0.85 m. **Vertical exaggeration** VE multiplies every z (water, seabed, reef) and leaves x and y unchanged: tan(angle_apparent) = VE tan(angle_true); at VE = 5 the 1:32.0 bed looks like 1:6.4 and the reef looks 6.8 m high at the apex. Camera angles read for photo alignment are only valid at VE = 1; the viewer forces VE = 1 in photo-match mode.

## 6. Confidence

**LOW.** Rubric used (my extension of the plan-shape rubric in `SHAPE_SPEC.md`, which covers only the outline): *high* = built-state footprint from a survey or georeferenced image, crest and seabed from surveys at the site and mutually consistent within 0.3 m, position known to better than 10 m; *medium* = all vertical inputs sourced and consistent within 0.5 m, with at most one of (footprint is a design, position known only to +-50 m, assumed stack height); *low* = two or more of those, or vertical uncertainty at least half the reef height. Against it: the footprint is a design layout (A9), the position is inferred (+-100 m), the stack height and slope are assumed (A4, A5), the two crest readings differ by 0.849 m (one number, two datum labels), the volume check fails for the as-built-based state (V8), and sigma_H = 0.85 m is more than half the reef height. In favour: the 2003 paper confirmed the crest datum (MLLW), the bag size, the dates and the position text; the tidal datums are cross-checked (V1, V2); the seabed is supported by three sources agreeing within 0.3 m in the reef zone (V5, V14); the apex thickness is one bag course (V12). The paper did **not** change the level: it holds no as-built plan and no stack height. The *plan* confidence (medium) is separate from this one. Before the paper the level was also LOW (reasons: crest datum unconfirmed, bag width only from web summaries, position +-150 m).

## 7. Limitations and unknowns

| id | unknown | how it could bias the model | what would resolve it | Lior could supply |
|---|---|---|---|---|
| L1 | true position (lat/lon) of the reef (now +-100 m, inferred) | picture mis-located; depths unaffected (A3) | Google Earth Pro historical imagery 2001-2008; ruler from the shoreline | yes (REQUESTS A1-A3) |
| L2 | as-built footprint and bag layout (the paper has none) | footprint differs by metres; the optional bags may or may not exist | Coastal Frontiers 2008 removal mapping; aerials; the raw survey files of the paper | partly (A5, C1) |
| L3 | crest elevation along the reef (only the apex face, 6 ft MLLW, and a design label exist) | tops biased by the assumption of constant thickness (A4): +-0.5 m at the tips | as-built survey; dive depth-gauge records (the paper mentions them) | no (C1) |
| L4 | number of courses / second layer (volume gap 252-339 m3 filled, 426 m3 nominal) | heights under-estimated by up to one course (1.2 m) in places, or the footprint under-estimated | as-built cross-sections; photographs of bag stacks | no |
| L5 | side slope and bag shapes | volume +-99 m3; the surface is a smooth height field, not bags | photographs; Phase I dive survey | no |
| L6 | Navionics datum and contour interval (inferred), survey dates unknown; contour counting +-2 lines beyond 6 ft | +-0.06 m (datum), +-0.6 m (counting) | app readings at listed points | yes (B1-B7) |
| L7 | DEM vertical accuracy not stated (composite of surveys 1932-2009, 10 m cells) | +-0.3 m or more; surf-zone difference to Navionics up to 1.00 m | high-resolution lidar/multibeam (NOAA Digital Coast, USGS CMGP) | partly |
| L8 | tide: epoch 1983-2001 datums, no sea-level trend, no meteorological surge | +-0.05 m | - | no |
| L9 | scour, settlement, burial, deflation not modelled | the real reef sank into the bed within a year (S10, S2) | monitoring data | no |
| L10 | datum and units of the paper's Figs 5-9 not stated; Fig. 5 and Fig. 7/8 differ by 1.44 m and 5.5 m horizontally | the profile cross-checks (V13, V14) carry 0.85-1.4 m datum ambiguity; the UTM datum (NAD27 would shift positions by about 100 m) | the paper's authors (J. Borrero, C. Nelsen) or the raw survey files | yes (REQUESTS A5) |
| L11 | Phase I profile through the reef: none (the Nov 2000 profile stops at d = 109 m) | Phase I height and width at the centreline unknown | the Feb 2001 / Oct 2000 survey lines | no |

## 8. References

* Borrero, J.C. & Nelsen, C. (2003). Results of a comprehensive monitoring program at Pratte's Reef. In: Black, K. & Mead, S. (eds), *Proceedings of the 3rd International Surfing Reef Symposium*, Raglan, New Zealand. 16-page PDF supplied by Lior on 2026-10-05 (venue and year not printed in the file; PDF metadata title *2 Years of Pratte's Reef: Performance and Considerations for Future Artificial Reef Endeavors in Santa Monica Bay*). Private research copy; copyright holder.
* Borrero, J.C., Mead, S.T. & Moores, A. (2010). Stability considerations and case studies of submerged structures constructed from large, sand filled, geotextile containers. *Coastal Engineering Proceedings*, 1(32), structures.60. doi:10.9753/icce.v32.structures.60. Accessed 2026-10-05. CC BY 4.0.
* California Coastal Commission (1998). *Staff report W5a: Coastal development permit application E-98-15 (Surfrider Foundation - Pratte's Reef)*, hearing of 13 October 1998. https://documents.coastal.ca.gov/reports/1998/10/W5a-10-1998.pdf. Accessed 2026-10-05.
* Coastal Frontiers Corporation (n.d.). *Removal of Pratte's Reef - a man-made surf enhancement structure*. https://www.coastalfrontiers.com/removal-of-prattes-reef (cited through the reef card; not re-fetched).
* Garmin Ltd. (2026). *Garmin Navionics Marine Maps (SonarChart Maps and Nautical Charts layers)*. https://maps.garmin.com/en-US/marine/ (formerly webapp.navionics.com). Accessed 2026-10-05. (c) Garmin; not for navigation.
* Henriquez, M. (2005). *Artificial surf reefs*. MSc thesis, Delft University of Technology (Fig. 2.10, after Borrero & Nelsen 2003). https://repository.tudelft.nl/record/uuid:75b15cd7-08a1-48e5-8fc9-337f184ae318.
* NOAA CO-OPS (2026). *Tidal datums for stations 9410840 (Santa Monica) and 9410660 (Los Angeles)*, Metadata API. https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/9410840/datums.json. Accessed 2026-10-05. Public domain.
* NOAA National Geophysical Data Center (2010). *Santa Monica, California 1/3 arc-second NAVD 88 Coastal Digital Elevation Model*. NOAA National Centers for Environmental Information. https://www.ngdc.noaa.gov/metaview/page?xml=NOAA/NESDIS/NGDC/MGG/DEM/iso/xml/726.xml. Accessed 2026-10-05. Public domain.
* NOAA National Geophysical Data Center (2012). *U.S. Coastal Relief Model - Southern California (v2), 1 arc-second*. doi:10.7289/V5V985ZM. Accessed 2026-10-05. Public domain.
* Raised Water Research (n.d.). *Pratte's Reef*. https://raisedwaterresearch.com/spot/artificial-reef/us/california/prattes-reef/. Accessed 2026-10-05.
* Skelly Engineering (2000). *Pratte's Reef* (plan-view design drawing, 110 bags + 30 optional), reproduced by Raised Water Research (2019) and as Fig. 4 of Borrero & Nelsen (2003). https://raisedwaterresearch.com/wp-content/uploads/2019/07/Pratts-Reef-Diagram.png.
* Surfline (2008). Fontaine, E. *Sandbagged: after years of unspectacular closeouts, Pratte's Reef is removed from El Segundo* (11 Oct 2008) (cited through the reef card; not re-fetched).
* Wikipedia contributors (2026). *Chevron Reef*. https://en.wikipedia.org/wiki/Chevron_Reef (bag counts and dates, used by `shape.json`).

## 9. Reproduction

```
cd 07_scale/shapes/prattes-reef-el-segundo/3d
python bn_digitise.py              # src/bn2003_digitised.json from the PDF paths of Borrero & Nelsen (2003) Figs 5, 7, 9 (+ Fig. 8 by-eye table)
python build_3d.py                 # model.js, docs.js, METHODS_3D.md, computed.json, auto block of SOURCES_3D.md
python build_3d.py --annotations   # also redraws annotated/A1-A17 (needs PyMuPDF, matplotlib, Pillow, shapely, numpy, scipy, pyproj)
```
Inputs: `../shape.json`, `../src/borrero_nelsen_2003_prattes_monitoring_results.pdf`, `src/noaa_9410840_datums.json`, `src/noaa_9410660_datums.json`, `src/noaa_santa_monica_13as_navd88_export.tif`, `src/noaa_socal_crm_1as_export.tif`, `src/navionics/*.png` and `nav_transect.json`. Viewer: `index.html` (three.js 0.170.0 from jsDelivr; `model.js`, `docs.js` loaded as scripts, works from a local web server or file://).

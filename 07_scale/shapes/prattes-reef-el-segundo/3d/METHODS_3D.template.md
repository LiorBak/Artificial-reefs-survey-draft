# METHODS_3D - Pratte's Reef (El Segundo, California): three-dimensional model

Built {{build_date}} by `build_3d.py` (numbers in this note are filled in by that script from `shape.json`, the NOAA files in `src/`, `src/navionics/nav_transect.json` and `src/bn2003_digitised.json`; edit `METHODS_3D.template.md`, not this file). Companion notes: `SOURCES_3D.md` (running log of what was read where), `REQUESTS_FOR_LIOR.md` (what could not be read), `annotated/A1-A17` (the sources with the readings marked). Revision 3: the 2003 monitoring paper of Borrero & Nelsen, supplied by Lior, is now used (sections 3.10, 3.11).

## 1. Summary

The model shows **Pratte's Reef as built in Phase I (22 September 2000)**: a V of two bag arms (two arms at 45 deg to the shore normal and a 5 x 5 bag apex block; {{area_m2}} m2, {{bbox_alongshore}} x {{bbox_crossshore}} m) on the nearshore seabed of Dockweiler Beach, with the water surface at any tidal datum from LAT to HAT. The footprint is the verified Skelly Engineering **design layout** of fall 2000: the 2003 monitoring paper reprints the same drawing as its Fig. 4 and contains no as-built plan. The top is fixed by the only as-built crest number, which the paper gives as "approximately - 6 ft MLLW" at the outermost point (= {{zB}} m relative to MSL, datum confirmed as MLLW); it follows the seabed at a constant thickness of {{thickB}} m, which is one 1.2 m bag course. The seabed is the NOAA 1/3 arc-second DEM (primary), checked against Garmin Navionics SonarChart depth labels and against the beds in the paper's profiles; tides are NOAA CO-OPS Santa Monica. The position (+-{{sig_x}} m) is now inferred from the georeferenced survey window of the paper ({{hint_lat}} N, {{hint_lon}} W). Later events are **not modelled** and appear in the caption only: Phase II (23-24 April 2001, +90 bags placed on top, crest widened and made shallower to within 3 ft of MLLW, {{zC}} m MSL, eroded by about {{bn_erosion}} m by September 2002), and removal in two phases (fall 2008 and fall 2010). The 3D confidence is **LOW**: every number has a source and the datums, bag size, dates, position and seabed slope are well supported, but there is still no as-built plan, the stack height is not stated anywhere, the single-course model holds {{volB}} m3 against {{vol_bag_lo}}-{{vol_bag_hi}} m3 (80-90 % fill) or {{vol_bag_nom}} m3 (nominal) for 110 bags, the Phase I crest is one point that differs by {{zAB_diff}} m from the design reading, and the vertical uncertainty (+-{{sig_H}} m) is more than half the reef height ({{hB_apex}} m).

## 2. Data sources

Access dates are 2026-10-05 unless stated. "Licence" is the licence stated by the publisher; reuse of every private research copy is NOT cleared for public release.

| id | reference (author-year) | what it contributed | resolution / date | licence |
|---|---|---|---|---|
| S10 | Borrero, J.C. & Nelsen, C. (2003). Results of a comprehensive monitoring program at Pratte's Reef. In: Black, K. & Mead, S. (eds), *Proceedings of the 3rd International Surfing Reef Symposium*, Raglan, New Zealand. File `src/borrero_nelsen_2003_prattes_monitoring_results.pdf`, 16 pp., supplied by Lior on 2026-10-05 (his `Downloads\Pratte_results.pdf`; original URL unknown). Page 1 title *Results of a comprehensive monitoring program at Pratte's Reef*, authors J.C. Borrero (USC) and C. Nelsen (Surfrider Foundation); **the file prints neither venue nor year** (the PDF metadata title is *2 Years of Pratte's Reef: Performance and Considerations for Future Artificial Reef Endeavors in Santa Monica Bay*, re-saved 2020-11-03); venue and year are those of the citation R23 in `shape.json`, consistent with the content (monitoring to Oct 2002) | bag size, counts and dates; Phase I crest depth (6 ft MLLW) and Phase II crest (3 ft MLLW); the design drawing (Fig. 4); position text, aerial (Fig. 2) and a georeferenced bathymetry window (Fig. 9); centreline profiles after Phase II (Figs 5-8) | text; Figs 5, 7, 9 vector graphics (digitised from the PDF paths), Figs 2, 4, 8 rasters (432 x 231, 371 x 468, 969 x 560 px); survey Oct 2000 - Sept 2002 | copyright holder; private research copy |
| P1 | Skelly Engineering (c. 2000). *Pratte's Reef* plan-view design drawing (110 bags + 30 optional), as reproduced by Raised Water Research (2019). https://raisedwaterresearch.com/wp-content/uploads/2019/07/Pratts-Reef-Diagram.png. Outline traced and verified in `shape.json` (this project, verified 2026-10-04); the same drawing is Fig. 4 of S10 | plan outline ({{n_vertices}} vertices), design crest label "TOP OF BAG MIN DEPTH -6' MSL" at both arm tips, scale bar 0-90 ft | raster 308 x 385 px, 5.155 px/m; drawing c. fall 2000 | unknown / all rights reserved (private copy) |
| S1 | California Coastal Commission (1998). *Staff report W5a, application E-98-15 (Surfrider Foundation - Pratte's Reef)*, hearing 13 Oct 1998; Exhibits 2 and 3 by Skelly Engineering (1997, 1996). https://documents.coastal.ca.gov/reports/1998/10/W5a-10-1998.pdf | text distance (300 yd north of the Grand Avenue jetty, 100 yd offshore, "15 feet of water (MSL)"), tidal labels MHHW +2.6 ft and MLLW -2.8 ft MSL, concept section | text and 1996-97 sketches, not to scale | public agency record, terms not stated |
| S2 | Borrero, J.C., Mead, S.T. & Moores, A. (2010). Stability considerations and case studies of submerged structures constructed from large, sand filled, geotextile containers. *Coastal Engineering Proceedings* 1(32), structures.60 (ICCE 2010, Shanghai). https://doi.org/10.9753/icce.v32.structures.60 | the same crest depths in metres (1.8 m and 1 m), bag size, 80-90 % fill, 2002 survey, removal late 2008 | text, p.2 Fig. 1 and p.7; 2010 | CC BY 4.0 (ICCE-OJS record) |
| S3 | Raised Water Research (n.d.). *Pratte's Reef*. https://raisedwaterresearch.com/spot/artificial-reef/us/california/prattes-reef/ | Phase II bags "placed on top of the existing bags"; "roughly 100 meters" offshore; "rose from about 5m deep" (datum not stated) | web page | unknown |
| S4 | NOAA CO-OPS (2026). *Tidal datums, station 9410840 Santa Monica, CA* (34.0083 N, 118.5 W; 11.7 km from the site), epoch 1983-2001. https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/9410840/datums.json?units=metric | MSL, MLLW, MHW, MHHW, MLW, NAVD88, LAT, HAT (m above station datum) | epoch 1983-2001; LAT/HAT from the station record | NOAA, public domain |
| S8 | NOAA CO-OPS (2026). *Tidal datums, station 9410660 Los Angeles Outer Harbor, CA* (33.72 N, 118.272 W; 26.6 km from the site), epoch 1983-2001. https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/9410660/datums.json?units=metric | cross-check of MSL - MLLW ({{msl_mllw_la}} m vs {{msl_mllw}} m) | as S4 | public domain |
| S5 | NOAA National Geophysical Data Center (2010). *Santa Monica, California 1/3 arc-second NAVD 88 Coastal Digital Elevation Model*. NOAA National Centers for Environmental Information, metadata gov.noaa.ngdc.mgg.dem:726 (published 2010-03-12). https://www.ngdc.noaa.gov/metaview/page?xml=NOAA/NESDIS/NGDC/MGG/DEM/iso/xml/726.xml. Read through the NCEI ImageServer (`DEM_mosaics/DEM_all`, raster id 173) as a 216 x 270 px float32 export, `src/export_dem.py` | seabed profile (primary) | cell 1/3 arc-second (about 10 m); sources dated 1932-2009 (NOS soundings, multibeam 1992-2008, SHOALS lidar 2002-2007); "not to be used for navigation" | NOAA, public domain |
| S6 | NOAA National Geophysical Data Center (2012/2013). *U.S. Coastal Relief Model - Southern California v2*, 1 arc-second, MSL datum. doi:10.7289/V5V985ZM | independent check of the DEM | 1 arc-second (about 30 m) | public domain |
| S7 | Garmin Navionics (2026). *Marine Maps web viewer*, SonarChart Maps and Nautical Charts layers (https://webapp.navionics.com/ redirects to https://maps.garmin.com/en-US/marine/). Screenshots in `src/navionics/` (two captures: the new position and the earlier text hint, `hint1_33.9188_-118.4324/`) | independent seabed: {{nav_n}} one-foot contours along a shore-normal transect, {{nav_lab_n_all}} depth labels / spot soundings, outfall landfall | zoom 18 (max), {{nav_m_per_px}} m/px; survey dates not shown; depth datum and contour interval not stated by the app | (c) Garmin; private research copy; "Not to be used for navigation" |
| S9 | Reef card `02_research/reefs/prattes-reef-el-segundo.json` (this project; verified 2026-09-25), citing Surfrider Foundation news, Coastal Frontiers Corp. (https://www.coastalfrontiers.com/removal-of-prattes-reef) and Surfline (2008) | removal dates: Phase I removal 30 Sept-17 Oct 2008, remaining bags fall 2010 | not re-fetched in this run | n/a |

### 2.1 Chronology of the structure (state modelled and what is not)

| date | event | modelled? | source |
|---|---|---|---|
| 1996-1998 | concept of about 30 large bags, CCC permit hearing 13 Oct 1998 | no (superseded design) | S1 |
| 22 September 2000 | **Phase I installed**: 110 sand-filled geotextile bags (4 x 7 x 10 ft) filled at the Port of Los Angeles and placed by barge-mounted crane in an obtuse V with the apex offshore; outermost point approximately 6 ft below MLLW | **yes** | S10 p.2 |
| October 2000 | first bathymetric survey (Fig. 9, dashed contours); November 2000 profile before any significant swell | no | S10 pp.5, 7 |
| winter 2000-01 | Phase I bags largely covered by sand that moved offshore | no | S10 p.3 |
| 23-24 April 2001 | Phase II: 90 bags placed directly over Phase I, volume +80 %, crest widened and made shallower (to within 3 ft of MLLW) | no (later change; caption only) | S10 p.3 |
| May 2001 - Sept 2002 | crest of the widened reef eroded by about {{bn_erosion}} m (Fig. 8); by October 2002 the bags were mostly level with the sand | no | S10 Fig. 8, p.16 |
| August 2002 | dive survey: several bags ripped, losing fill | no | S10 p.8; S2 |
| fall 2008 | removal of the mostly buried remnants begins (30 Sept-17 Oct) | no | S2, S9 |
| fall 2010 | removal completed at permit expiry | no | S9 |

## 3. Methods

### 3.1 Coordinate frame and orientation

The model frame is the canonical frame of `shape.json`: metres, **x alongshore** toward bearing 155 deg (SSE), **y offshore** toward bearing 245 deg (WSW) = x turned 90 deg clockwise, **z up**, z = 0 at mean sea level (MSL, epoch 1983-2001). The origin is the MSL waterline on the V axis; the reef centroid is at y = {{y_nom}} m (text value, assumption A2). (x, y, z-up) is left-handed; the viewer therefore maps model (x, y, z) to three.js (X, Y, Z) = (x, z, y), which is mirror-free (looking toward the beach from the sea, x runs to the right).

Pixel to metre on the Skelly drawing (img1, 5.1549 px/m from the printed scale bar, origin (ox, oy) = (628.5, 156.2) px, `shape.json` `transform_note`):

```
x = (py - oy) / 5.1549          y = -(px - ox) / 5.1549          (origin placed so that the polygon centroid is at x = 0, y = {{y_nom}} m)
```

Frame to compass (bx = 155 deg, by = bx + 90 = 245 deg) and to latitude/longitude (used only for the Navionics and DEM sampling and for the position hint):

```
E = x sin(bx) + y sin(by)     N = x cos(bx) + y cos(by)         (metres east / north)
lat = lat0 + N / 111132       lon = lon0 + E / (111320 cos(lat0))    (lat0, lon0 = {{hint_lat}}, -{{hint_lon}})
north in the model frame = (cos bx, cos by) = (-0.906, -0.423)
```

Orientation (assumption A1): the drawing has no north arrow; its horizontal "wave direction" axis is taken as the shore normal. Support: the present shoreline fitted on the 2026-01-09 Esri image has bearing 155.5 deg (own RANSAC fit, +-2 deg); the 1996 concept plan has its V bisector at 61 deg (onshore; shore normal 65 deg); the Navionics 0 ft line trends about 158 deg; and the eight depth contours of the 2003 survey (Fig. 9) have a mean true bearing of {{fig9_bearing}} deg (spread {{fig9_bearing_sd}} deg between contours; UTM convergence -0.8 deg applied). Stated uncertainty +-5 deg.

### 3.2 Vertical datums and conversions

All NOAA datum values are heights above the station datum (STND) of the gauge, so with `h` a height above STND at the gauge:

```
z_MSL = h - MSL                                         (E1)
depth d below datum D  ->  z_MSL = -d - (MSL - D)       (E2)    D in {MLLW, LAT, NAVD88}
MSL - MLLW  = 1.594 - 0.745 = {{msl_mllw}} m (Santa Monica 9410840);  {{msl_mllw_la}} m (Los Angeles 9410660)     (E3)
MSL - NAVD88 = 1.594 - 0.802 = {{navd88_to_msl}} m     z_MSL = z_NAVD88 - {{navd88_to_msl}}     (E4)
```

Datum levels used (z relative to MSL, metres): HAT {{hat}}, MHHW {{mhhw}}, MHW {{mhw}}, MSL 0, MLW {{mlw}}, MLLW {{mllw}}, LAT {{lat}}; MHHW - MLLW = {{tidal_range_mhhw_mllw}} m. Crest and water depths below LAT use `D_LAT = z_LAT - z` (positive = below LAT).

Crest readings converted with E2/E3 (A = drawing, datum label MSL; B, C = Borrero & Nelsen 2003, datum MLLW):

```
A:  z = -6 ft x 0.3048 = {{zA}} m MSL  = {{zA_mllw}} m rel. MLLW  (0.98 m below MLLW; with 9410660: {{zA_mllw_la}} m)            (E5)
B:  z = -(6 ft x 0.3048 + {{msl_mllw}}) = -(1.829 + {{msl_mllw}}) = {{zB}} m MSL     [ICCE 2010 rounds 6 ft to 1.8 m: {{zB_icce}} m, {{zB_diff_icce}} m apart]   (E6)
C:  z = -(3 ft x 0.3048 + {{msl_mllw}}) = {{zC}} m MSL   (after Phase II; NOT modelled)                                         (E7)
```

A and B are the same number (6 ft) with different datum labels (the drawing says MSL, the paper says MLLW); they differ by exactly MSL - MLLW = {{zAB_diff}} m. The paper does not say which label is right. The drawing's "MSL" is the local NOAA mean sea level: CCC Exhibit 2 (Skelly, June 1997) prints MHHW +2.6 ft and MLLW -2.8 ft relative to MSL, and NOAA gives +2.64 ft and -2.79 ft (differences 0.01 m), see validation V1.

### 3.3 Plan shape

The toe polygon ({{n_vertices}} vertices, {{area_m2}} m2) is read unchanged from `shape.json` (status {{plan_status}}, verified {{plan_verified_on}}, md5 {{plan_md5}}); only the solid-outline bags of the drawing are included (the 30 dashed "optional" bags are excluded; including them would add an estimated 15-20 % area). It is the *design* layout of Phase I (assumption A9): the 2003 paper reprints it as Fig. 4 ("The design layout of Pratte's Reef", annotated figure A13) and shows no later layout; bags were crane-placed, moved, sank and were buried, so the real footprint differed from it by metres.

### 3.4 Seabed from the NOAA DEM (primary)

For each of 31 alongshore stations x_k = -150, -140, ... +150 m about the position hint ({{hint_lat}} N, {{hint_lon}} W) the DEM was sampled (bilinear in the 1/3 arc-second grid) every 1 m along bearing 245 deg for s = -300 ... +500 m, converted with E4, and the most seaward z_MSL = 0 crossing with s < 150 m was taken as that station's MSL waterline s_w,k (linear interpolation). Each profile was then re-expressed relative to its own waterline and the mean and standard deviation over the stations were kept (5 m steps):

```
z_k(y) = z_MSL( s_w,k + y )        zbar(y) = (1/31) sum_k z_k(y)        sd(y) = std_k z_k(y)       y = -60 ... 300 m   (E8)
```

The mean MSL waterline lies at s = {{wl_mean}} m along the transect (sd {{wl_sd}} m), i.e. the hint is {{y_hint}} m seaward of the DEM's MSL waterline. The seabed is thus **alongshore uniform** (assumption A3; sd at the reef {{sd_dem_nom}} m): z(y = {{y_nom}} m) = {{z_dem_nom}} m, z(tips, y = {{y_min}} m) = {{z_dem_tips}} m, z(apex, y = {{y_max}} m) = {{z_dem_apex}} m, slope 1:{{slope_1_in}} over the reef. The same procedure about the earlier text hint (33.9188 N, 118.4324 W, {{dist_hint_old_m}} m away) gave z(91.44 m) = -3.75 m (sd 0.18 m): a 0.08 m difference, which is the practical test of A3. The DEM is the seabed without the reef (6 x 3 cells; removed 2008-2010). Between nodes the model interpolates linearly in y.

### 3.5 Seabed from Navionics SonarChart (independent check, selectable)

*Access.* Navionics' web chart (webapp.navionics.com) now redirects to Garmin's Marine Maps viewer. In my own headless Chrome (DevTools protocol, a random free port and a fresh temporary profile; the process was terminated afterwards) the page loaded without login, CAPTCHA or consent dialog; nothing was accepted or bypassed. The map was centred on the position hint with Leaflet `setView` at zoom 17 and 18 (the maximum), with options View = Map, Chart type = SonarChart Maps or Nautical Charts, Depth units = Feet, Seabed areas = Hide, Shallow shading = 6 ft (default). Two captures exist: the first at the earlier text hint (`src/navionics/hint1_...`), the second at the new hint. Screenshots are private research copies ("Not to be used for navigation") and were analysed offline.

*Scale.* Web-Mercator, 256 px tiles: `res = 156543.034 cos(lat) / 2^zoom` = {{nav_m_per_px}} m/px at zoom 18.

*Counting.* Along the shore-normal line (bearing 245 deg) through the screenshot centre the screenshot was sampled every 0.25 px; dark pixels (max RGB < 175) that belong to long connected components (>= 30 px: contour lines, not label glyphs or chart symbols) are contour lines; runs closer than 0.8 m were merged. Contour index 0 is the first line within 3 m of the seaward edge of the green "drying" band (the 0 ft contour, s = {{nav_green_end}} m); index n is the n-th line seaward ({{nav_n}} lines to s = {{nav_last_s}} m). The 1 ft interval is *inferred*: the seven lines 0-6 bound the 6 ft shallow-shading band. **The counting is only partly reliable at the new position**: the printed depth labels 1, 4 and 5 ft are reproduced exactly, but only {{nav_label_match}} of {{nav_label_n}} labels overall (the 7-11 ft lines crowd, and symbols interrupt lines), so the count carries +-2 lines (+-0.6 m) beyond 6 ft; the 15th line lies {{nav_anchor_off}} m from the Nautical-layer spot sounding "15" ft.

*Conversion* (datum assumption A8: chart datum = MLLW, US convention; the app does not state it):

```
z_MSL(n) = -(n x 0.3048) - {{msl_mllw}} m          y = y_hint + s = {{y_hint}} + s            (E9)
```

*Datum test without counting.* Every printed depth label and spot sounding ({{nav_lab_n_all}} points on both captures) was compared with the DEM at the same ground point. In the reef zone (labels 8-18 ft, n = {{nav_lab_n_reef}}) the bias (Navionics - DEM) is {{nav_bias_mllw}} m if the depths are below MLLW, {{nav_bias_navd}} m if NAVD88, {{nav_bias_lat}} m if LAT and {{nav_bias_msl}} m if MSL (RMS {{nav_rms_mllw}} / {{nav_rms_navd}} / {{nav_rms_lat}} / {{nav_rms_msl}} m): MSL and LAT are rejected; MLLW and NAVD88 are only 0.057 m apart and cannot be separated. Outside the reef zone the DEM is deeper than the chart by {{nav_lab_surf_mllw}} m (surf zone, labels < 8 ft) and by {{nav_lab_off_mllw}} m (labels > 18 ft), assuming MLLW.

*Use.* Seabed only: the reef was removed (2008-2010) and no contour at the hint shows an anomaly, so the chart gives no crest or height information. In the viewer the Navionics profile can replace the DEM wherever it has contours (y = {{nav_y0}} m to the end of the model profile at 300 m); elsewhere the DEM is used.

### 3.6 Crest scenarios

Two scenarios are selectable; only B is the as-built Phase I and is the default.

* **B - Phase I as installed (Borrero & Nelsen 2003 p.2).** "After the initial installation, the depth at the outermost point of the reef was approximately - 6 ft MLLW". The outermost point is read as the offshore face of the V apex block. Its elevation z_B = {{zB}} m is the top of the reef at y = y_apex = {{y_max}} m; the top is carried along the reef at constant thickness above the bed (assumption A4):
  `h_top = max( z_B - z_bed(y_apex), 1.2 m ) = {{thickB}} m`  ({{coursesB}} bag courses of 1.2 m). Tops are then {{topB_apex}} m MSL at the apex ({{topB_apex_mllw}} m below MLLW, {{topB_apex_lat}} m below LAT) and {{topB_tips}} m at the arm tips ({{topB_tips_mllw}} m below MLLW, {{topB_tips_lat}} m below LAT).
* **A - design minimum depth (Skelly).** Level crest at z_A = {{zA}} m MSL: `h_top(y) = max( z_A - z_bed(y), 1.2 m )` = {{hA_tips}} m at the tips and {{hA_apex}} m ({{coursesA_apex}} courses) at the apex. Crest {{zA_lat}} m below LAT.
* **C - after Phase II** ({{zC}} m MSL, {{zC_lat}} m below LAT; "within 3 ft of MLLW"): later change, **not modelled**. The paper's profiles show that the widened reef was far wider at the centreline than the Phase I outline (section 3.11).

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
| A1 | the drawing's horizontal axis is the shore normal; x = 155 deg | shoreline fit 155.5 deg; Fig. 9 contours {{fig9_bearing}} deg; concept plan | +-5 deg: rotates the picture, no effect on depths |
| A2 | reef centroid {{y_nom}} m from the MSL waterline | text "100 yards" (CCC), "roughly 100 m" (RWR); the paper's profiles give {{bn_peak_from_msl5}}-{{bn_mid_from_zero7}} m (V13) | +-25 m moves the seabed by +-{{sig_pos}} m (slope 1:{{slope_1_in}}); the hint gives {{y_hint}} m |
| A3 | seabed uniform alongshore; mean DEM profile; reef absent from the DEM | alongshore sd {{sd_dem_nom}} m (DEM), {{nav_al_sd_m}} m (Navionics, 7 transects); old and new hint differ by 0.08 m | hides bars and troughs of the 10 m grid |
| A4 | the 6 ft MLLW depth applies at the apex face; the top follows the bed at constant thickness | the tips' tops then agree with the design label (V6); the apex thickness is one bag course (V12); no other as-built crest value exists | tips top {{topB_tips}} m; a level crest at {{zB}} m would leave only {{lvlB_tips_h}} m of reef at the tips (less than one bag) |
| A5 | bag-stack side slope s = 1.0 (0.5-2.5) | bag edge of a 1.2-1.5 m course; no cross-section of the Phase I reef | volume {{volB}} m3 (B), range in section 5 |
| A6 | minimum thickness one 1.2 m course | bag height 4 ft (S10) | applies only if crest minus bed < 1.2 m |
| A7 | NOAA Santa Monica datums apply at the site; epoch 1983-2001; no sea-level trend applied | 11.7 km, same bay; LA harbour MSL-MLLW differs 0.012 m | +-0.03 m |
| A8 | Navionics chart datum = MLLW; contour interval 1 ft | US convention; label test (MSL and LAT rejected in the reef zone); 0-6 ft shading band | MLLW vs NAVD88 0.057 m; +-2 lines counting error beyond 6 ft |
| A9 | footprint = Phase I design layout (solid-outline bags only) | no as-built plan: the paper's Fig. 4 is the same drawing | metres; 30 optional bags excluded (+15-20 % area if built) |
| A10 | no settlement, scour or burial modelled | "largely covered in sand" (winter 2000-01) | the real structure sank and was buried |
| A11 | water is static at the chosen datum | - | no waves, set-up or surge |
| A12 | the vertical axis of the paper's Fig. 5 is MLLW-referenced | the zero line is labelled "Approx. Min Low Tide" and the high-tide line sits at +{{bn_maxhigh5}} m (6 ft) | the paper's profile figures are used only for cross-checks (V13, V14), not for model numbers; if the axis were MSL the beds would be 0.85 m deeper |
| A13 | the reef lies within the Fig. 9 survey window; position = window centre, +-{{sig_x}} m | the paper puts the reef about 200 m south of the 1-mile outfall; the outfall-based estimate lies within 35 m of the window centre (section 3.10) | no effect on depths (A3); moves the picture only |

### 3.10 Position from the 2003 paper (new in revision 3)

The paper's Fig. 9 compares two bathymetric surveys (October 2000, four weeks after Phase I; March 2001) in a UTM frame. It is a vector graphic: the eight contour paths (-1 ... -4 m) and the axis ticks were read from the PDF (`bn_digitise.py`). Axis calibration from the tick marks (20 m spacing):

```
E = 367460 + (x_pt - 216.1) / 2.495        N = 3754240 + (309.5 - y_pt) / 2.485          (metres, UTM zone 11 N; datum not stated, NAD83/WGS84 assumed)   (E12)
window: E {{fig9_win_e}}, N {{fig9_win_n}}  ->  centre (367505, 3754275) = {{hint_lat}} N, {{hint_lon}} W (pyproj EPSG:32611 -> 4326)
```

The reef is not drawn in the figure and no contour shows a bag signature, but the paper says the offshore bathymetry has not changed "outside of the contours created by the reef bags themselves", and the window (about 112 x 71 m) is just large enough for the 58 x 29 m reef. Independent text evidence for the position: p.1 "approximately 200 m south of the Hyperion Sewage Treatment Plant's 1-mile outfall" and "within 500 m" of the outfall and the Grand Street jetty; Fig. 2 (aerial, range lines 550 m apart, scale 6.3 m per original pixel) places the reef chevron on range line 3, 325 m from the outfall and 672 m from the Grand Street jetty arrow. The outfall landfall was read on the Navionics chart (33.9231 N, 118.4337 W, +-20 m); 200 to 318 m south along 155 deg plus 91 m offshore gives 33.9202-33.9211 N, 118.4332-118.4337 W, within 35 m of the window centre. A jetty-based estimate (660 m north of the groin at 33.91685 N, 118.43030 W) gives 33.9219 N, 118.4342 W, 160 m further north. The three estimates span 190 m, so the hint is stated as +-{{sig_x}} m. The earlier text hint (33.9188 N, 118.4324 W, from the 1996-98 concept siting "300 yards north of the Grand Avenue jetty") lies {{dist_hint_old_m}} m away and is superseded. The survey is not a georeferenced outline of the reef, so `shape.json` keeps `geo = null`.

### 3.11 Profiles through the reef after Phase II (new in revision 3)

Figs 5 and 7 are vector graphics (curves read from the PDF paths), Fig. 8 a raster (read by eye). Calibration (tick marks):

```
Fig. 5:  d = (x_pt - 141.5) / 1.0980 m ;   z = (455.82 - y_pt) / 8.60 m           Fig. 7:  d = (x_pt - 143.63) / 1.1807 m ;   z = (135.23 - y_pt) / 8.844 m          (E13)
```

All profiles are along range line 3 (the reef centreline) from the dune base. Fig. 5 (Oct 2001) and Fig. 7/8 (Oct 2001) are the same data on shifted axes: Fig. 5 = Fig. 7 + {{bn_offset57}} m vertically (peak and bed alike) and about 5.5 m horizontally. The vertical datum is not stated. Reading A12 (Fig. 5 zero = MLLW, from the tide lines) gives crest {{bn_peak5}} m MLLW at d = {{bn_peak_d5}} m, beds {{bn_bed5_land}} m (landward) and {{bn_bed5_sea}} m (seaward) = {{bn_bed5_land_msl}} / {{bn_bed5_sea_msl}} m MSL, relief {{bn_relief}} m above the landward bed and {{bn_relief_sea}} m above the seaward bed, base width {{bn_base_w}} m (the design apex block is only 10.6 m wide at the centreline: the widened Phase II reef was about three times as wide). The Fig. 7/8 axis is 1.44 m higher, equal to MHW - MLLW (1.43 m) or MSL - LAT (1.47 m); it cannot be decided from the paper. Fig. 8 gives the crest history on the Fig. 7/8 axis: May 2001 {{bn_may01}} m, October 2001 {{bn_oct01}} m, February 2002 {{bn_feb02}} m, September 2002 {{bn_sep02}} m, i.e. {{bn_erosion}} m of erosion in 16 months. The Phase I profile is NOT available: the November 2000 profile stops at d = 109 m, before the reef.

## 4. Validation (cross-checks performed)

| id | check | numbers | verdict |
|---|---|---|---|
| V1 | CCC Exhibit 2 tidal labels vs NOAA | MHHW +2.6 ft = +0.79 m vs +{{mhhw}} m; MLLW -2.8 ft = -0.85 m vs {{mllw}} m | agree to 0.01 m; confirms the drawing's "MSL" is the NOAA epoch MSL |
| V2 | datum transfer | MSL - MLLW {{msl_mllw}} m (Santa Monica) vs {{msl_mllw_la}} m (Los Angeles): {{msl_mllw_diff}} m apart | consistent (A7) |
| V3 | DEM vs Coastal Relief Model at y = {{y_nom}} m | {{z_dem_nom}} vs {{z_crm_nom}} m MSL ({{dem_crm_diff}} m) | CRM is 1 arc-second and shallower; both used in the spread (section 5) |
| V4 | DEM vs CCC text "15 feet of water (MSL)" = -4.57 m | the DEM reaches -4.57 m at y = {{y_15ft}} m, {{y15_diff}} m further out than {{y_nom}} m | within about 1 sigma of A2 |
| V5 | DEM vs Navionics SonarChart (Navionics - DEM, MLLW assumed) | hint: {{nav_hint_z}} vs {{dem_hint_z}} m; reef zone {{nav_d_reef}} m (max {{nav_dmax_reef}}); s = 40-150 m {{nav_d_40_150}} m; s > 150 m {{nav_d_far}} m; surf zone s < -17 m {{nav_d_surf}} m (max {{nav_dmax_surf}}); label test in the reef zone {{nav_bias_mllw}} m (n = {{nav_lab_n_reef}}) | agree within 0.3 m over the reef; they diverge in the surf zone and offshore (beach morphology, survey dates, counting error) |
| V6 | tips: design label vs bed | one 1.2 m course on the DEM bed at the tips reaches {{tip_single_course_top}} m vs the drawing's {{zA}} m ({{tip_diff_A}} m); state B's tip top {{tipB_top}} m is {{tipB_diff_A}} m from it | consistent within the uncertainty (not independent: both use the DEM bed) |
| V7 | bag volume | 3.0 x 2.13 x 1.2 m = {{bag_rect_vol}} m3 vs 7.9 m3 stated ({{bag_rect_vs_stated_pct}} %). Phase II: 90 / 110 bags = {{bag_ratio_phase2}} vs "+80 %" stated. 200 bags x 7.9 = {{vol_total_nom}} m3 vs "approximately 1600 m3" in the paper (nominal volume; at 80-90 % fill {{vol_final_lo}}-{{vol_final_hi}} m3) | consistent |
| V8 | **model volume vs 110 bags** | 110 bags: {{vol_bag_nom}} m3 nominal, {{vol_bag_lo}}-{{vol_bag_hi}} m3 at 80-90 % fill; model B = {{volB}} m3 (ratio {{ratioB_nom}} of nominal, {{ratioB_lo}}-{{ratioB_hi}} of the filled volume); model A = {{volA}} m3 (ratio {{ratioA_nom}} nominal); with the Navionics bed B = {{vol_nav_B}} m3 | **FAILS for B; NOT resolved by the paper** (see below) |
| V9 | bag footprint vs outline | 110 bags x {{bag_foot_m2}} m2 = {{bag_foot_total_m2}} m2 of bag footprint vs {{area_m2}} m2 outline: mean {{bag_mean_courses}} layers | the outline cannot hold 110 single-layer bags |
| V10 | position vs chart coastline | the hint is {{nav_coast_abs}} m from the Navionics coastline (text: 91.4 m); at 91.44 m from the chart coastline the chart depth is {{nav_reef_ft}} ft = {{nav_reef_z}} m MSL | consistent (A2) |
| V11 | paper vs ICCE | "approximately - 6 ft MLLW" = 1.829 m vs ICCE's 1.8 m ({{zB_diff_icce}} m); "within 3 ft of MLLW" = {{bn_3ft_m}} m vs ICCE's "within 1 m" | ICCE (same first author) converted and rounded the paper's feet; datum MLLW confirmed |
| V12 | apex thickness vs bag height | z_B minus the DEM bed at the apex = {{thickB}} m vs bag height 1.2 m ({{coursesB}} courses) | the as-installed depth and the DEM bed give one bag course at the outermost point |
| V13 | reef distance from the MSL waterline in the paper's profile | crest {{bn_peak_from_msl5}} m, base centre {{bn_mid_from_msl5}} m (Fig. 5 as MLLW: MSL = +0.849 m at d = {{bn_msl5}} m); {{bn_peak_from_zero7}} / {{bn_mid_from_zero7}} m if the Fig. 7 axis is MSL (zero crossing at d = {{bn_zero7}} m); text 91.44 m | within +-25 m (A2) in either reading |
| V14 | beds beside the reef in the paper vs DEM | Fig. 5 (axis read as MLLW): {{bn_bed5_land_msl}} / {{bn_bed5_sea_msl}} m MSL (mean {{bn_bed5_mean_msl}}) vs DEM {{z_dem_nom}} m at y = {{y_nom}} and {{z_dem_apex}} m at the apex; Fig. 7/8 axis: {{bn_bed7_land}} / {{bn_bed7_sea}} m | agree within 0.3 m (Fig. 5 reading); 0.4 m deeper if the Fig. 7 axis is MSL |
| V15 | Fig. 9 contour bearing | {{fig9_bearing}} deg true (sd {{fig9_bearing_sd}} deg over 8 contours) vs the model's 155 deg | consistent (A1) |
| V16 | Fig. 9 contours vs NOAA DEM at the same points | survey value minus DEM z_MSL: {{fig9_off_oct}} m (Oct 2000), {{fig9_off_mar}} m (Mar 2001) | positions consistent; datum of Fig. 9 not stated (MLLW would give +0.85 m; the winter profile is steeper and seaward, the DEM has 10 m cells) |
| V17 | May 2001 crest vs "within 3 ft of MLLW" | Fig. 8 crest {{bn_may01}} m on its axis = {{bn_may01_5}} m on the Fig. 5 axis (MLLW) or {{bn_may01_mllw_if_msl}} m MLLW if the axis is MSL; limit -{{bn_3ft_m}} m | holds in either reading |

*V8/V9 are an unresolved discrepancy, not a pass.* The single-course model B holds {{missing_vol_lo}}-{{missing_vol_hi}} m3 less than 110 bags at 80-90 % fill (about {{missing_bags_lo}}-{{missing_bags_hi}} bags) and {{missing_nom}} m3 less than the nominal volume. The paper does not give a stack height or layout, so it cannot close the gap; it removes one explanation: V12 shows one bag course at the outermost point, so a second course there is not supported. What remains: the 110 bags (703 m2 of bag footprint) did not fit in the {{area_m2}} m2 traced outline (the drawing's arm bags overlap, 3.4 m2 per bag in `VERIFY.md`), or part of the structure was already two bags high elsewhere, or the bags were less full. Model A (level crest, up to {{coursesA_apex}} courses at the apex) is closer to the bag volume. This is why A stays selectable and why the confidence is low.

## 5. Uncertainty

Per input (all are 1-sigma-like ranges, not statistical intervals; where only readings exist I state my judgement):

| input | uncertainty | basis |
|---|---|---|
| outline | +-0.2 m, +-4 % area; scale bar +-3-5 % | `shape.json` verification |
| position along y | sigma_y = +-{{sig_y}} m | text distances; the paper's profiles give {{bn_peak_from_msl5}}-{{bn_mid_from_zero7}} m; hint vs text {{y_hint}} vs {{y_nom}} m |
| position along x | +-{{sig_x}} m; irrelevant to depth (uniform bed) | window half-length 56 m; outfall- and jetty-based estimates span 190 m |
| crest B reading | sigma_zc = +-{{sig_zc}} m | "approximately 6 ft"; single point; datum transfer 0.012 m |
| crest A reading | +-0.15 m | integer-foot label; datum label disputed (A vs B differ by {{zAB_diff}} m) |
| seabed depth at the reef | sigma_zb = +-{{sig_zb}} m | sample SD of six estimates ({{sd_est}} m, table below); slope x sigma_y = {{sig_pos}} m |
| paper's profile axes | Fig. 5 vs Fig. 7/8: {{bn_offset57}} m, datum unstated | A12 |
| tide datums | +-0.03 m (transfer), LAT +-0.05 m | S4, S8 |
| side slope s | 0.5-2.5 | A5 |

{{est_table_md}}

**Propagation** (independent errors added in quadrature):

```
reef height / thickness   H = z_c - z_b           sigma_H = sqrt( sigma_zc^2 + sigma_zb^2 ) = sqrt({{sig_zc}}^2 + {{sig_zb}}^2) = {{sig_H}} m
seabed term               sigma_zb^2 ~ (slope x sigma_y)^2 + sigma_dem^2   (slope x sigma_y = {{sig_pos}} m; empirical SD {{sd_est}} m)
crest depth below LAT     D_LAT = z_LAT - z_c    sigma_D = sqrt( sigma_zc^2 + sigma_LAT^2 ) = {{sig_D_lat_B}} m (B), {{sig_D_lat_A}} m (A)
water over the crest      d_c(T) = T - z_top     sigma_d = sqrt( sigma_T^2 + sigma_ztop^2 )      (T = tidal level)
volume                    sigma_V^2 = (dV/dh0 sigma_h0)^2 + (dV/dy sigma_y)^2 + (dV/ds sigma_s)^2
```

Numerically: state B, V = {{volB}} m3 with half-differences {{dV_B_thick}} m3 (thickness +-0.3 m), {{dV_B_y}} m3 (reef moved +-25 m) and {{dV_B_s}} m3 (s 0.5-2.0), giving sigma_V = {{sig_V_B}} m3; state A, V = {{volA}} m3 with {{dV_A_zc}}, {{dV_A_y}}, {{dV_A_s}} m3, sigma_V = {{sig_V_A}} m3. At +1 sigma ({{volB_p1}} m3) state B is still below the {{vol_bag_lo}}-{{vol_bag_hi}} m3 of the filled bags; it reaches that range only at about +2 sigma ({{volB_p2}} m3) and not even at +3 sigma ({{volB_p3}} m3) the nominal {{vol_bag_nom}} m3, so the volume gap is not just an uncertainty effect. Volume by slope run s (m3):

{{vol_table_md}}

Sensitivity to the reef position (centroid moved along y):

{{sens_md}}

So the crest (state B) is {{topB_apex_lat}} +- {{sig_D_lat_B}} m below LAT at the apex; the water over the apex top ranges from {{water_apex_lat}} m (LAT) to {{water_apex_hat}} m (HAT) and over the tip tops from {{water_tips_lat}} m to {{water_tips_hat}} m (MHHW - LAT = {{range_mhhw_lat}} m); the reef height is {{hB_apex}} +- {{sig_H}} m. **Vertical exaggeration** VE multiplies every z (water, seabed, reef) and leaves x and y unchanged: tan(angle_apparent) = VE tan(angle_true); at VE = 5 the 1:{{slope_1_in}} bed looks like 1:{{ve5_slope_inv}} and the reef looks {{ve5_apex}} m high at the apex. Camera angles read for photo alignment are only valid at VE = 1; the viewer forces VE = 1 in photo-match mode.

## 6. Confidence

**LOW.** Rubric used (my extension of the plan-shape rubric in `SHAPE_SPEC.md`, which covers only the outline): *high* = built-state footprint from a survey or georeferenced image, crest and seabed from surveys at the site and mutually consistent within 0.3 m, position known to better than 10 m; *medium* = all vertical inputs sourced and consistent within 0.5 m, with at most one of (footprint is a design, position known only to +-50 m, assumed stack height); *low* = two or more of those, or vertical uncertainty at least half the reef height. Against it: the footprint is a design layout (A9), the position is inferred (+-{{sig_x}} m), the stack height and slope are assumed (A4, A5), the two crest readings differ by {{zAB_diff}} m (one number, two datum labels), the volume check fails for the as-built-based state (V8), and sigma_H = {{sig_H}} m is more than half the reef height. In favour: the 2003 paper confirmed the crest datum (MLLW), the bag size, the dates and the position text; the tidal datums are cross-checked (V1, V2); the seabed is supported by three sources agreeing within 0.3 m in the reef zone (V5, V14); the apex thickness is one bag course (V12). The paper did **not** change the level: it holds no as-built plan and no stack height. The *plan* confidence ({{confidence_plan}}) is separate from this one. Before the paper the level was also LOW (reasons: crest datum unconfirmed, bag width only from web summaries, position +-150 m).

## 7. Limitations and unknowns

| id | unknown | how it could bias the model | what would resolve it | Lior could supply |
|---|---|---|---|---|
| L1 | true position (lat/lon) of the reef (now +-{{sig_x}} m, inferred) | picture mis-located; depths unaffected (A3) | Google Earth Pro historical imagery 2001-2008; ruler from the shoreline | yes (REQUESTS A1-A3) |
| L2 | as-built footprint and bag layout (the paper has none) | footprint differs by metres; the optional bags may or may not exist | Coastal Frontiers 2008 removal mapping; aerials; the raw survey files of the paper | partly (A5, C1) |
| L3 | crest elevation along the reef (only the apex face, 6 ft MLLW, and a design label exist) | tops biased by the assumption of constant thickness (A4): +-0.5 m at the tips | as-built survey; dive depth-gauge records (the paper mentions them) | no (C1) |
| L4 | number of courses / second layer (volume gap {{missing_vol_lo}}-{{missing_vol_hi}} m3 filled, {{missing_nom}} m3 nominal) | heights under-estimated by up to one course (1.2 m) in places, or the footprint under-estimated | as-built cross-sections; photographs of bag stacks | no |
| L5 | side slope and bag shapes | volume +-{{dV_B_s}} m3; the surface is a smooth height field, not bags | photographs; Phase I dive survey | no |
| L6 | Navionics datum and contour interval (inferred), survey dates unknown; contour counting +-2 lines beyond 6 ft | +-0.06 m (datum), +-0.6 m (counting) | app readings at listed points | yes (B1-B7) |
| L7 | DEM vertical accuracy not stated (composite of surveys 1932-2009, 10 m cells) | +-0.3 m or more; surf-zone difference to Navionics up to {{nav_dmax_surf}} m | high-resolution lidar/multibeam (NOAA Digital Coast, USGS CMGP) | partly |
| L8 | tide: epoch 1983-2001 datums, no sea-level trend, no meteorological surge | +-0.05 m | - | no |
| L9 | scour, settlement, burial, deflation not modelled | the real reef sank into the bed within a year (S10, S2) | monitoring data | no |
| L10 | datum and units of the paper's Figs 5-9 not stated; Fig. 5 and Fig. 7/8 differ by {{bn_offset57}} m and 5.5 m horizontally | the profile cross-checks (V13, V14) carry 0.85-1.4 m datum ambiguity; the UTM datum (NAD27 would shift positions by about 100 m) | the paper's authors (J. Borrero, C. Nelsen) or the raw survey files | yes (REQUESTS A5) |
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

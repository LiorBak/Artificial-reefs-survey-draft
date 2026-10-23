# METHODS_3D - Boscombe Surf Reef (Bournemouth, UK): three-dimensional model

Note date: 2026-10-05; seabed extension (sections 3.4, 4 items 9-13, 7) added 2026-10-07. Offshore alongshore flattening D2 applied 2026-10-10 (block D2 in 3.4, validation 12, A16, sections 5 and 7). Model files: `model.js`, `index.html`, `build_3d.py` (regenerates `model.js` and `docs.js`). Frame, units and datums are defined in section 3.1. Every number below has a source line in `SOURCES_3D.md`.

## 1. Summary

The model shows the **as-built state of the Boscombe geotextile surf reef (finished September-October 2009)**: the verified plan outline (4,042 m2, traced on the Esri Wayback image of 28 September 2011, which still shows the bag field clearly) lofted into a two-layer mound with a flat crest at the designers' +0.5 m above chart datum (ACD), 1:3 flanks, standing on a seabed read from the April 2011 DGPS bathymetry plot of Rendle and Davidson (2012, Fig. 9). Later events (container failure from March-April 2011, closure on 31 March 2011, aborted repairs, ASR liquidation in 2012, re-branding for diving in 2014 and 2017) are in the viewer caption and in section 3.10, not modelled as a second state. Garmin Navionics (accessed 2026-10-05) still shows the structure as a shoal with a 380-490 m2 drying patch at the right place, so the bags are damaged but not removed; its shoal areas match the April 2011 survey zones to 1-2 % at the 0.5 m and 1 m levels and 16 spot soundings agree with the model seabed to a mean difference of +0.06 m (sd 0.49 m). **Confidence (3D): medium**: outline, seabed and crest are sourced and mutually consistent, but the zero of the survey plot is assumed to be chart datum (the whole absolute height scale would shift by 1.4 m if it were Ordnance Datum, relief would not), the as-built flanks and flat crest are an idealised loft, and the beach and the ground under the reef are interpolated or extrapolated. **Revision of 2026-10-07:** the seabed grid was enlarged from y 0-380 m to y -66 to 650 m (x -160 to 160 m) so that the shoreline is inside the model: the beach and nearshore (y -66 to about +40 m) come from 11 Channel Coastal Observatory beach-profile lines surveyed on 2010-04-20 (S13), the offshore rows (y 380-650 m) extend the model along the EMODnet DTM 2024 seabed slope (S5), and a blend joins the beach to the Fig. 9 survey. The reef, the survey cells and the cells under the reef are unchanged; the new zones are coloured and labelled by source in the viewer (section 3.4).

## 2. Data sources

| ID | Citation | What it contributed | Resolution / date | Licence / status |
|---|---|---|---|---|
| S1 | Esri, Maxar, Earthstar Geographics and the GIS User Community (2011). World Imagery Wayback, release 10, tiles captured 2011-09-28. https://livingatlas.arcgis.com/wayback/ (retrieved 2026-10-04) | plan outline of the bag field (traced in the project, `shape.json`), georeference of the canonical frame, shoreline (surf line) bearing 83.4 deg | 0.378 m/px, 28 Sep 2011 | Esri/Maxar terms; private research copy, reuse not cleared |
| S2 | Rendle, E. and Davidson, M. (2012). An evaluation of the physical impact and structural integrity of a geotextile surf reef. *Coastal Engineering Proceedings* 1(33) (ICCE 2012), OJS article 6794, Fig. 9; e-published 28 Sep 2012 (Plymouth research portal). https://icce-ojs-tamu.tdl.org/icce/article/view/6794 (accessed 2026-10-05; DOI and paper identifier not confirmed). Survey data: Channel Coastal Observatory / Bournemouth Borough Council | seabed and reef surface heights (Fig. 9 left map, April 2011 DGPS bathymetry, colour bar +0.93 to -5.30 m); crest levels and flank slope from the four cross-section profiles (Oct 2009, May 2010, Oct 2010, Apr 2011); text: "Situated 225 m offshore in 2.7 to 5 m depth", damage description | map about 0.5 m/px (1.908 px/m E, 1.091 px/m N), plot itself interpolated from DGPS lines | authors' copyright; research copy |
| S3 | Mead, S., Blenkinsopp, C., Moores, A. and Borrero, J. (2010). Design and construction of the Boscombe multi-purpose reef. *Coastal Engineering Proceedings* 1(32), structures.58 (proceedings of ICCE 2010, Shanghai; the OJS listing dates the paper 2011), OJS article 1352. https://icce-ojs-tamu.tdl.org/icce/article/view/1352 (accessed 2026-10-05; citation form re-checked 2026-10-10; DOI not confirmed) | design crest "0.5 m above chart datum"; Table 1 water levels (m ACD) HAT 2.59, MHWS 2.21, MHWN 1.67, MLWN 1.17, MLWS 0.45, LAT -0.06 (Bournemouth Pier gauge); MHWS-MLWS range 1.76 m; design depth plan Fig. 3a (design in 3-5 m CD); 54 containers 1-5 m diameter, 15-70 m long, about 13,000 m3 | Table 1 to 0.01 m | authors' copyright; research copy |
| S4 | National Tidal and Sea Level Facility (n.d.). Chart datum and ordnance datum. https://ntslf.org/tides/datum (accessed 2026-10-05) | Bournemouth chart datum is 1.40 m below Ordnance Datum (table row "Bournemouth -1.40m") | 0.01 m | open web page |
| S5 | EMODnet Bathymetry Consortium (2026). EMODnet Digital Bathymetry (DTM), WMS GetFeatureInfo, layer `emodnet:mean`. https://ows.emodnet-bathymetry.eu/wms (queried 2026-10-05); and EMODnet Bathymetry Consortium (2024). EMODnet Digital Bathymetry (DTM 2024), ERDDAP `bathymetry_dtm_2024`, https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1 (queried 2026-10-06; project test `07_scale/bathymetry/emodnet/REPORT.md`) | datum plausibility check (2026-10-05); since 2026-10-07 also the far-field seabed SLOPE (-1.41 %, y > 380 m) of the offshore rows; no EMODnet level is used | cells about 115 m, depths relative to LAT | open data, EMODnet terms of use |
| S6 | Herbert, R.J.H., Collins, K., Mallinson, J., Hall, A.E., Pegg, J., Ross, K., Clarke, L. and Clements, T. (2017). Epibenthic and mobile species colonisation of a geotextile artificial surf reef on the south coast of England. *PLoS ONE* 12(9): e0184100. https://pmc.ncbi.nlm.nih.gov/articles/PMC5604948/ (accessed 2026-10-05) | "shallow water (0-5 m Chart Datum)"; "upper section is exposed on low spring tides"; 220 m offshore, 210 m east of the pier | text | CC-BY |
| S7 | This project (2026). `07_scale/shapes/boscombe-surf-reef/shape.json`, METHOD.md, VERIFY.md, status verified 2026-10-05 | verified canonical polygon (25 vertices, area 4,042 m2, minimum rotated rectangle 121.1 x 45.0 m), shore normal 173.4 deg | +-1 m | project file |
| S8 | riverlevels.uk (n.d.). Tide at Bournemouth. https://riverlevels.uk/tide-bournemouth (accessed 2026-10-05) | usual range -1.08 to +1.11 m above Ordnance Datum (mid-range +0.02 m ODN): supports ODN approximately equal to MSL | text | open web page |
| S9 | Garmin Ltd / Navionics (2026). Marine Maps viewer, Nautical Charts and SonarChart Maps layers. https://maps.garmin.com/en-US/marine (screenshots 2026-10-05; the former webapp.navionics.com redirects here; the old ChartViewer was decommissioned in 2024) | present-day shoal at the reef: drying patch, 0.5 m and 1 m depth contours, 33 soundings and contour labels | zoom 18 = 0.378 m/px; soundings 0.1 m | "Garmin Navionics, not for navigation"; private research copy, reuse not cleared; datum not stated |
| S10 | University of Liverpool (n.d.). Depth surveys; crowd sourced charts (Navionics SonarChart, TeamSurv). https://www.liverpool.ac.uk/~cmi//mag/survey_h.html (accessed 2026-10-05) | statement that later SonarChart versions keep drying areas as given by the Hydrographic Office and add contours by interpolation | text | open web page |
| S11 | Solent Forum (n.d.). Waves and tides. https://solentforum.org/solent/our_coastal_zone/waves_and_tides/ (accessed 2026-10-05) | context: tidal range 1.2 m (Christchurch Bay) to 3.0 m (Chichester Harbour), double high water in this part of the Channel | text | open web page |
| S13 | Channel Coastal Observatory, Southeast Regional Coastal Monitoring Programme (2026). Beach profile surveys, lines 5f00424, 424A, 425, 425A, 426, 426A, 427, 427A, 428, 428A, 429 (survey 2010-04-20; Easting, Northing, Elevation_OD, Chainage). https://coastalmonitoring.org/ (profile API `cco/profiles/api.php`; accessed 2026-10-06; raw copies `07_scale/shapes/boscombe-surf-reef/src/cco_profiles/`) | beach and nearshore seabed y -66 to about +40 m (zones 3/4); independent datum test of A3 (validation 9) | 11 lines 29-55 m apart alongshore (x -221 to +222 m), 17-28 points per line (median spacing 4-6 m); heights m ODN; 2010-04-20 | Open Government Licence v3.0 (acknowledge source; hydrographic data not for navigation) |
| S12 | Wikipedia (2026). Boscombe Surf Reef (accessed 2026-09-24, via the project dossier `02_research/reefs/boscombe-surf-reef.md`, refs R1, R4, R6, R8); Leisure Opportunities (2012), "Future of Boscombe surf reef in doubt"; Newsroom.co.nz (2021), "The Kiwi scientist and the failed surf breaks" | dated history after 2009 (section 3.10) | text | secondary sources |

| S14 | This project (2026). `07_scale/bathymetry/emodnet/REPORT.md`, sections 6 and 9.1 (EMODnet test and integration plan) | slope 0.0141 +-0.0010 of zone 5 (four DTM cells) and the DTM-versus-model comparison (validation 13) | cells about 116 x 73 m | project file; derived from S5 |
| S15 | Rendle, E.J. (2016). *The Environmental, Social and Economic Impacts of an Artificial Surf Reef - The UK Experience.* PhD thesis, School of Biological and Marine Sciences, University of Plymouth. https://pearl.plymouth.ac.uk/bms-theses/412/ (received from Lior as PDF in `papers/`, read 2026-10-10; printed page = PDF page - 3; notes `07_scale/shapes/boscombe-surf-reef/P5_RENDLE2016_NOTES.md`) | read 2026-10-10, validation only, NO model value changed: built crest about +0.5 m CD (p. 70), design 0 m CD (Table 4.4) and 0.3 m CD (Fig. 5.3), design footprint 4,474 / 5,450 m2, design volume 11,900 / 12,200 m3, bag counts 32 / about 46, survey dates, "relative to MSL" wording of Fig. 5.6 | text and figures; Fig. 5.7 is the same April 2011 survey as S2 Fig. 9 | author's copyright; private research copy; images img-33 to img-40 |

Not used: any value from the Gemini folder (no Gemini number, outline or conclusion enters this model; an earlier agent's estimates were only used as starting hypotheses and every value above was re-read from its original source); GEBCO (grid far too coarse for a 120 m object). Read but used for validation only: S15.

## 3. Methods

### 3.1 Coordinate frame and conversions

The model frame is the canonical frame of `shape.json`: metres, **x alongshore** (true bearing 83.4 deg, towards the east; Boscombe Pier is at negative x), **y offshore** (bearing 173.4 deg, the shore normal), **z up**. The origin is the point on the surf line of the 2011-09-28 image nearest to the reef centroid (50.719552 N, 1.839278 W; OSGB36 E 411442 N 91115). Heights are metres above mean sea level (MSL), z = 0 at MSL. The three.js scene uses X = x, Y = z, Z = y (right-handed, not mirrored).

(E1) Compass bearing of a canonical direction (dx, dy): `bearing = 83.4 deg + atan2(dy, dx)`. True north in the frame is the unit vector (cos 83.4, cos 173.4) = (0.115, -0.993), i.e. north points mostly towards the beach (-y).

(E2) Image pixel (px, py) of S1 to canonical metres, with s = 0.37808 m/px (Web-Mercator ground scale at 50.72 N, `156543.034 cos(phi) / 2^18`), origin pixel O = (1509.7, 747.8), alongshore unit u = (cos a, sin a), a = -6.59 deg, offshore unit n = (-u_y, u_x):
`x = s [(px - 1509.7) u_x + (py - 747.8) u_y]`, `y = s [(px - 1509.7) n_x + (py - 747.8) n_y]`.
The 25 traced vertices are reproduced by the fitted 2 x 2 matrix to 0.006 m (the shared tool `geom.py` had a rotation bug, not used).

(E3) Web-Mercator: `X = R lambda`, `Y = R ln tan(pi/4 + phi/2)`, R = 6,378,137 m; pixel = (X - X0)/(X1 - X0) W, using the bounds in the `.geo.json` sidecar of S1.

(E4) Fig. 9 pixel (Xp, Yp) of the left map to OSGB36 metres (gridlines read on the figure: E 411400 at Xp = 147.3, E 411550 at 433.5; N 91000 at Yp = 39.0, N 90820 at 235.3):
`E = 411400 + (Xp - 147.3)/1.908`, `N = 91000 - (Yp - 39.0)/1.0909`;
OSGB36 (EPSG:27700) to WGS84 with pyproj (Helmert, about +-5 m), then E3 and E2 to canonical metres.

(E5) Fig. 9 colour to height: the printed colour bar has ticks 0 to -5 m at bar rows 55, 93, 131, 168, 206, 244 px; the linear fit is `z_survey = -0.02646 Y_bar + 1.455` (top +0.93 m, bottom -5.30 m). Each map pixel takes the value of the nearest bar colour (Euclidean RGB distance; median distance 11.7, 95th percentile 20 on a 0-441 scale); pixels whose distance exceeds 70 are rejected. Pixels hidden by the black section line on the left map are taken from the right map (the same surface, offset +469 px, -1 px by template match, SQDIFF 0.028), the rest inpainted (TELEA, r = 4 px). The colour bar saturates at +0.93 m, so crest peaks above it are not resolved.

### 3.2 Datums and tide levels

(E6) Chart datum (CD) at Bournemouth is 1.40 m below Ordnance Datum Newlyn (S4): `z_ACD = z_ODN + 1.40`. With ODN approximately equal to MSL (A4): `z_MSL = z_ACD - 1.40`. Depth below chart datum `d_CD = -z_ACD`; depth below LAT `d_LAT = -(z_ACD - z_LAT,ACD) = -z_ACD - 0.06`.

(E7) Water levels (S3 Table 1, converted with E6; model frame, metres above MSL): HAT +1.19, MHWS +0.81, MHWN +0.27, MSL 0 (estimated, A4), MLWN -0.23, MLWS -0.95, LAT -1.46. Check: MHWS - MLWS = 2.21 - 0.45 = 1.76 m, equal to the "1.76 m" printed in the text of S3; the mean of the four mean levels is 1.375 m ACD, consistent with the 1.40 m offset.

(E8) Cover over the design crest (+0.5 m ACD) at level k: `c_k = L_k,ACD - 0.50`: HAT 2.09 m, MHWS 1.71, MHWN 1.17, MLWN 0.67, MLWS -0.05 (dry), LAT -0.56 (dry). This agrees with S6, which says the upper section is exposed at low spring tides.

The tide at the site is semi-diurnal with a small range and a **double high water** (a stand around high water; S3 Fig. 1b "highly asymmetrical tide signal"; S11). The viewer uses a **static** level (slider LAT to HAT, buttons for each datum) and does not model the time curve, wave set-up or surge. Level source: Bournemouth Pier gauge, about 1.5 km west of the reef (S3).

### 3.3 Plan outline

The outline is the verified polygon of `shape.json` (S7): the outer edge of the dark bag field on S1, 25 vertices, area 4,042 m2. Its nearest edge lies 181 m, centroid 226 m and far edge 276 m offshore of the surf line (A1, A10). The model draws it as the toe line (magenta) and as the plan of the loft.

### 3.4 Seabed

The Fig. 9 grid (E4, E5) is resampled to a 1 m canonical grid by bilinear interpolation (no registration shift: a +-30 m search of the best overlap between the survey relief and the outline gives 0, 0 with IoU 0.90), normalised-convolved with a Gaussian of sigma 1 m, with the rim of the plot eroded by 2 cells. The plotted area is 23,500 m2 (y about 100 to 305 m).

The ambient (pre-reef) seabed S(x, y) is a thin-plate spline through the survey cells **outside** a reef mask (relief above a second-order polynomial > 0.5 m, plus the outline, dilated 5 m; cells decimated to a 6 m spacing; rim buffer 3 m):
(E9) `S(p) = a0 + a1 x + a2 y + sum_i w_i |p - p_i|^2 ln|p - p_i|` (Duchon 1977; `scipy.interpolate.RBFInterpolator`, kernel thin_plate_spline, smoothing 2.0; Virtanen et al. 2020); the fit r.m.s. on the survey cells is 0.021 m. Inside the survey S = w S_survey + (1 - w) S_TPS with `w = clip((d_rim - 2)/8, 0, 1)`; under the reef S = S_TPS plus the nearest ring residual decayed as exp(-d/8 m) (A8); outside the survey S = S_TPS (extrapolation, A10). The survey-derived grid (E9) is 161 x 191 cells at 2 m (x -160 to 160, y 0 to 380), z in cm, with a code per cell: 0 survey, 1 extrapolated, 2 interpolated under the reef. Until 2026-10-07 this was the whole seabed and its beach cells (y < 100) were spline extrapolation, so the shoreline lay outside the model; the extension below replaces that part.

**Seabed extension (revision of 2026-10-07).** Lior asked for a larger model in which the shoreline is visible. The seabed grid is now 161 x 359 cells at 2 m (x -160 to 160, y -66 to 650 m; z in cm, one code and one datum weight per cell). Original cells keep their values wherever they carry code 0 or 2 (checked cell by cell against the previous `model.js`: 0 of 4,295 survey cells and 0 of 1,580 under-reef cells changed; the reef grid, reef statistics, Navionics layer, water levels and the datum switch are identical to the 2026-10-05 build). The new or changed cells carry three further codes:

| Code | Zone | y range (m) | Source | Vertical uncertainty (1 sd) |
|---|---|---|---|---|
| 3 | CCO beach profile (measured) | -66 to y_end(x), y_end = 21-38 | S13, survey 2010-04-20, 11 lines, linear between lines | 0.3 m (section 5) |
| 4 | blend, CCO to survey | y_end to about 80 | spline S (E9) + CCO offset decaying over 40 m | 0.5 m |
| 5 | EMODnet slope extrapolation | 382 to 650 | S5 slope applied to the alongshore mean of the model row y = 380 (D2, flat alongshore) | 0.5 m (validation 12) |

(E13) *Beach rows, y = -66 ... -2 m (code 3).* The CCO points (E, N, z_ODN) of each of the 11 lines l are converted from OSGB36 to the canonical frame with the chain used for Fig. 9 (OSGB36 to WGS84 with `pyproj`, then the S1 pixel grid, +-5 m), giving x_l(y) and z_l(y) (points with equal y averaged, clamped beyond the first and last point). At a row y the surface is the piecewise-linear interpolation across the lines ordered by x, constant beyond the outer lines: `z(x, y) = interp_x(x; {x_l(y)}, {z_l(y)})`. The lines are nearly shore-normal (x_l drifts by at most about 6 m over y -60 to +20 m), so interpolation at constant y is adequate. Seven lines lie inside the 320 m grid (x -142 to +145 m); 428A (x -183 m) and 424A (+176 m) lie just outside and fix the edge columns by interpolation; 429 and 424 (x -221 and +222 m) lie further out and are not needed for the grid.

(E14) *Transition rows, y = 0 ... 380 m, only cells that were code 1 (no survey, not under the reef).* With S the thin-plate spline of E9: `z(x, y) = S(x, y) + R(x, y)`, `R = interp_x(x; {x_l(y)}, {r_l(y)})`, where `r_l(y) = z_l(y) - S(x_l(y), y)` for y <= y_end,l (the seaward end of line l, y = 21-38 m; code 3 there) and `r_l(y) = delta_l (1 - sm((y - y_end,l)/L))` beyond it (code 4 while the blend weight exceeds 0.02), with `delta_l = z_l(y_end,l) - S(x_l, y_end,l)`, `sm(t) = t^2 (3 - 2t)` clipped to [0, 1] and L = 40 m. The offsets delta_l are the data of the datum test (validation 9) and are small (mean +0.03 m, sd 0.30 m), so the join is nearly seamless.

(E15) *Offshore rows, y = 382 ... 650 m (code 5).* `z(x, y) = z380 - s (y - 380)` with `z380` the alongshore mean of the model row y = 380 (since D2, 2026-10-10; before D2 it was the column value `z(x, 380)`), s = 0.0141 m/m (+-0.0010), the mean seabed slope of the four complete EMODnet DTM 2024 cells at y about 380, 445-505 and 605 m (cell means -7.05, -8.52 to -9.10 and -10.17 m LAT; project test REPORT 9.1). Only the slope is taken from EMODnet, not its levels: its cell means are 1.1 to 3.1 m deeper than the survey seabed and the DTM does not show the reef, so the absolute level continues from the model's own row y = 380 (alongshore mean -7.78 m MSL; the EMODnet cell at y 380 is -7.05 m LAT = -8.51 m MSL with z_MSL = z_LAT - 1.46, i.e. the model is 0.7 m shallower, inside the +-1.5 m datum/sampling uncertainty of EMODnet here). Row y = 380 is itself a spline extrapolation (the survey ends at y about 312 m) and had an alongshore slope of +0.76 m per 100 m of x which E15 copied to y = 650 m before D2; validation 12 showed that this was the main error of zone 5. Since D2 (2026-10-10) row y = 380 and all rows seaward are set to the alongshore mean (block D2 in 3.4); stated uncertainty of zone 5 now +-0.5 m.

(E16) *Datums of the extension.* CCO heights are m ODN; the model zero is MSL and ODN = MSL within +-0.1 m (A4), so `z_MSL = z_ODN` on the beach. Survey-derived cells keep E6, `z_MSL = z_ACD - 1.40`. The viewer's alternative reading "survey zero = ODN" adds `1.40 dw` to the survey-derived cells, with the datum weight `dw = 0` on the CCO beach (referenced to ODN independently of Fig. 9), `dw = 1 - W` in the blend (W the blend weight) and `dw = 1` on survey, spline and zone 5 cells.

*Shoreline.* The waterline of a level is the contour of z at that level on this grid; the viewer draws it for the selected level and keeps the 2011-09-28 surf line y = 0 as a separate line. With the CCO beach (slope about 0.04 between +1.2 and -0.3 m) the waterlines lie at y = -3 to -8 m (MSL), -10 to -30 m (MHWS), -27 to -37 m (HAT), +24 to +38 m (MLWS) and +51 to +72 m (LAT, in the blend zone), depending on x; the surf line y = 0 stands at z = -0.2 m (about MLWN). A level error of 0.35 m (section 5) moves a waterline by about 9 m. The model beach is the surface of 2010-04-20, after the reef was finished and before the 2011 container failure; it is not the beach of the date of any image used elsewhere (A14).

**D2 (2026-10-10) - offshore row y = 380 and seaward flattened alongshore.**

*Cause.* The extension (E15) copied the model row y = 380 column by column to y = 650 m. That row is a thin-plate-spline extrapolation of the Fig. 9 survey (which ends at y about 312 m) and carries an alongshore slope of +0.76 m per 100 m of x (-8.94 m at x = -160 to -6.79 m at x = +160, range 2.15 m). Neither the 27 EMODnet DTM 2024 cells (-0.07 m per 100 m of x) nor the 11 Navionics soundings support it (misfit -1.21 +- 0.11 m per 100 m of x, r.m.s. 1.20 m; validation 12).

*Fix.* In `scripts/extend_seabed.py` (flag `OFFSHORE_FLATTEN`) the 161 cells of row y = 380 (all code 1, asserted) are replaced by their alongshore mean (-7.78 m MSL) and E15 starts from that value: `z(x, y) = -7.78 - 0.0141 (y - 380)` for y >= 380. The EMODnet cross-shore gradient (0.0141) is kept. Rows y < 380 (survey, beach, blend, reef, zone codes, datum weights) are not touched; stated uncertainty of zone 5 changed from +-1.2 to +-0.5 m. Archive of the pre-D2 files: `archive/pre_D2/`. Check script: `scripts/d2_check.py` (output `scripts/d2_check.json`).

*Grid check (Borth lesson).* No node, clamp or min()/max() ignores part of the grid: the grid has the same 161 x 359 nodes; 21,779 cells changed, all at y >= 380 (0 cells below y = 380, so the survey, reef, beach and blend rows are byte-identical); the zone codes and datum weights are identical; all values are finite; in every zone-5 row the 161 cells are equal (spread < 0.006 m); seabed, reef, stats, shoreline and water levels outside `seabed` and `provenance` of `model.js` are identical to the pre-D2 file.

| Quantity | Before D2 | After D2 |
|---|---|---|
| Navionics z16 offshore, model minus chart (11 soundings): mean / sd / r.m.s. | -0.27 / 1.23 / **1.20 m** | -0.18 / 0.51 / **0.51 m** |
| Range of the misfit | -1.67 to +1.47 m | -0.85 to +0.46 m |
| Alongshore trend of the zone-5 model (m per 100 m of x) | +0.76 | **0.00** |
| Alongshore trend of the Navionics misfit (fit, m per 100 m of x) | -1.21 +- 0.11 | -0.44 +- 0.09 |
| Range of z across x at row y = 380 / 650 | 2.15 / 2.15 m | 0 / 0 m |
| Cross-shore gradient y >= 382 | -0.0141 | -0.0141 |
| Model at x = 0: y 380 / 446 / 506 / 604 (m MSL) | -7.63 / -8.56 / -9.41 / -10.79 | -7.78 / -8.71 / -9.55 / -10.94 (0.15 m deeper: the row mean replaces the column value) |
| Reef volume (idealised loft / survey relief) | 13,119 / 9,573 m3 | 13,119 / 9,573 m3 (unchanged) |
| Crest: design +0.5 m ACD; highest survey point; crest-zone areas (-1.0 / -0.5 / 0.0 m) | +0.68 m ACD at (20, 193); 1,609 / 956 / 296 m2 | unchanged (reef grid byte-identical) |
| Seabed under the outline (mean / min / max, m ACD) | -3.56 / -4.72 / -2.40 | unchanged |

*Remaining limitations.* (1) Rows y = 378 and y = 380 now differ by up to 1.13 m at the x edges of the grid (x = -160: -8.94 -> -7.78 m; x = +160: -6.79 -> -7.78 m; at x = 0 the step is 0.04 m): the spline surface of y 312-378 is kept as it was (no data there either) and the correction is applied as one step at the zone boundary, as specified for D2. (2) The soundings still show -0.44 +- 0.09 m per 100 m of x against the new model (11 hand-read values, +-0.05 m value and +-15 m position; EMODnet shows -0.07). (3) The absolute level is unchanged: the model is 0.7-1.3 m shallower than EMODnet cell means (datum/sampling uncertainty of EMODnet here +-1.5 m).

### 3.5 Reef surface (as-built, default)

(E10) Idealised loft: `r(x, y) = clip(r0 + phi/m, 0, H_c)`, `H_c = max(z_c - S, 0)`, `z_reef = S + r`, with phi the signed distance to the outline (positive inside, metres), `r0 = 1.0 m` (the outline is placed on the 1 m relief contour of the survey, which gives IoU 0.90 with the satellite outline), `m = 3.0` (run per rise, A7) and the crest `z_c = +0.5 m ACD` (the BUILT crest, Rendle 2016 p. 70; design 0 m CD, Rendle Table 4.4, or 0.3 m CD, Fig. 5.3 drawing; A6). The flat crest plateau covers 1,780 m2; the mean relief inside the outline is 3.2 m. Volume `V = sum r dx dy = 13,119 m3` against about 13,000 m3 stated (S3).

(E11) Evidence layer (not a reef state): the April 2011 survey surface `z_surv = S + max(Z_s - S, 0)` inside the reef mask, available through the "Reef surface" selector. It shows the container failure (offshore half of the axis at -0.8 to -2.8 m ACD, S2 profile: a 2 m crest dip and a trough of -1.1 to -2.2 m) and supplies the shoal-area comparisons in section 4.

### 3.6 Garmin Navionics reading (S9)

The old ChartViewer is gone; the Garmin Marine Maps page (title "Garmin | Marine Maps", footer "Not to be used for navigation") serves the Navionics Nautical Chart and SonarChart layers without login or CAPTCHA, and was used in an own headless Chrome (private profile, not the shared browser pane). Settings: chart type Nautical Charts or SonarChart Maps, depth units metres, shallow shading 1 m (blue = shallower than 1 m; SonarChart splits it into 0-0.5 m dark blue and 0.5-1 m light blue; green = drying, above chart datum). The Google Places search box gave no suggestions in headless mode, so the map was centred on 50.71753 N, 1.83891 W with the page's own Leaflet `setView` at zoom 16, 17 and 18 (18 is the maximum). Pixel to ground (E12): mercator metres per pixel `156543.034 / 2^z`, pane 1000 x 751 px at screenshot offset (400, 113), centre (500, 375.5); validated against Leaflet's own `latLngToContainerPoint` to 0.5 px. Areas are pixel counts times `(0.378 m)^2` at zoom 18; outlines come from `skimage.measure.find_contours`; positions go through E3 and E2 to canonical metres. Thirty-three soundings and contour labels printed on the chart (a digit with a subscript is metres and tenths) were read by eye from 3x enlarged crops (`scripts/navionics_reads.json`); position reading accuracy about 1 m.

**Is the structure "ruined" for the Navionics rule?** The bags were damaged (S2: one 70 m container lost about 80 t of sand in April 2011, an adjacent one lost by 2012; S12: repairs never completed, debris on the beach in 2017) but not removed: the 2025 Esri image shows a blurred patch with the same envelope (METHOD.md), and Navionics today shows a distinct shoal with a green drying patch at the shoreward-east half of the old bag field (centroid canonical (15, 209), 12.7 m from the survey crest zone). The offshore half is no longer distinguishable from the sloping seabed. Decision: the structure still exists and is recognisable, so Navionics is used for the **seabed** and as a **cross-check of the shoal and the post-damage crest**, but it does not set the as-built crest (that comes from the designers and the Oct 2009 profiles) because it shows the damaged state.

### 3.7 Viewer rendering

Seabed and reef are triangulated heightfields coloured by depth (seabed) or relief (reef). The water surface is a translucent plane at the chosen level L. Vertical exaggeration e (1 to 5, default 1, always displayed) scales all heights, including the water level and the datum labels: `z_shown = e z`, so the apparent flank gradient is `tan(theta') = e tan(theta)` (a 1:3 flank, 18.4 deg, looks like 33.7 deg at e = 2 and 59 deg at e = 5); distances in plan are never exaggerated. The photo-match mode forces e = 1. The survey-datum switch (A3 alternative) lifts the surveyed seabed and the April 2011 surface by 1.40 m against the water; the as-built crest is NOT lifted (the designers state it in chart datum, +0.5 m ACD = -0.90 m MSL), so under the switch the loft is rebuilt on the raised seabed, the relief shrinks by up to 1.4 m, the crest ends up under water at MSL, and the survey no longer matches the Navionics shoal lines (which are drawn in chart datum and never move). Camera parameters follow: heading as E1, pitch positive up, roll, vertical field of view, horizontal `hfov = 2 atan(tan(vfov/2) aspect)`, 35 mm equivalent focal length `f = 18 mm / tan(hfov/2)`.

### 3.8 Assumptions

- **A1** The outline traced on S1 (28 Sep 2011) is the as-built outer envelope; the envelope did not change between 2009 and 2011 (S7: same footprint in the 2025 image; the loss of containers lowered crest heights, not the footprint).
- **A2** Fig. 9 is a faithful, smooth rendering of the DGPS surfaces: features finer than 3-5 m are not trustworthy; heights are read to +-0.2 m.
- **A3** The depth axis of Fig. 9 is referred to chart datum (ACD). Evidence: crest in the Oct 2009 profiles +0.05 to +0.65 m against the designers' +0.5 m ACD; "225 m offshore in 2.7 to 5 m depth" and "3-5 m (CD)" match the survey seabed -3 to -5 m; S6: upper section exposed at low springs; EMODnet is 1.3-1.7 m deeper than the survey read as ACD but 3 m deeper if read as ODN; Navionics shoal areas match without a shift. The text of S2 ("MSL is equivalent to Chart Datum, Newlyn") is garbled and is not used. A switch in the viewer shows the alternative (survey zero = ODN).
- **A4** MSL = ODN within +-0.1 m at Bournemouth (S8: usual range centred +0.02 m ODN), so MSL is 1.40 +-0.1 m above chart datum.
- **A5** The Bournemouth Pier tide levels (S3 Table 1) apply at the reef 1.5 km east.
- **A6** As-built crest: flat at +0.5 m ACD along the whole outline (the BUILT crest, Rendle 2016 p. 70: "built crest approximately 0.5 m CD"; the design was 0 m CD, Table 4.4, or 0.3 m CD, Fig. 5.3 drawing, with 0.3-0.5 m settlement expected; the same number as the Mead et al. 2010 quote "0.5 m above chart datum"; the Oct 2009 profile tops are +0.05 to +0.65 m, typically +0.2 to +0.3, so +-0.3 m).
- **A7** Flanks 1:3 (run:rise), outline at 1 m relief. Source: the SW flank of the Fig. 9 across-reef section rises 2.0 m over 6-8 m (1:3 to 1:4, steepest 2 m window 1:1.5); the NE side is 1:5 to 1:7; the smoothed map gives a median gradient of 1:5.8. +-30 %.
- **A8** The seabed under the reef is the spline interpolation of the surrounding survey seabed; scour at the reef base (S2 reports erosion of the -3.5 m contour near the base) is ignored.
- **A9** Navionics depths are referred to chart datum (the viewer states no datum) and the shoal is the same structure; its survey date is unknown.
- **A10** Beyond the survey the seabed is a spline extrapolation (corners, y 305-380 m); since 2026-10-07 the beach and nearshore (y < about 40-80 m) are the CCO surface (A14) and y > 380 m is the EMODnet slope extension (A16). The line y = 0 is the surf line of 28 Sep 2011 at an unknown tide, drawn separately from the tidal waterlines.
- **A11** Static water level; no waves, set-up, surge or double-high-water time curve.
- **A12** The reef is a smooth 1 m heightfield: no container texture, no overhangs, the 54 containers are not individually modelled (layout unpublished).
- **A14** The CCO profiles of 2010-04-20 represent the beach and nearshore of the modelled state (as-built 2009 to April 2011): beach levels change by 0.28 m r.m.s. between 2010-04-20 and 2011-03-23 (11 lines), 0.49 m between 2009-09-22 and 2010-04-20 (2 lines only), 0.13 m for 2009-11-30 (1 line); heights are m ODN = m MSL (A4); alongshore the surface is linear between lines 29-55 m apart.
- **A15** The surface between the seaward ends of the CCO lines (y 21-38 m) and the survey rim (y about 100 m) is the spline S plus the CCO offset decayed over 40 m (E14), +-0.5 m.
- **A16** Beyond y = 380 m (row 380 included, since D2 2026-10-10) the seabed is flat alongshore and deepens uniformly at 1.41 % with contours parallel to the canonical x axis (E15). Before D2 the tilt of the spline row was copied seaward and gave a Navionics misfit of -1.2 m per 100 m of x; a smaller trend of -0.44 +- 0.09 m per 100 m of x remains in the 11 hand-read soundings (validation 12).
- **A13** Pixel scale of S1 is the Web-Mercator ground scale at the latitude; checked against the 180 m pier (measured 167.5-178 m).

### 3.9 State drawn

AS-BUILT 2009 (default, Lior's rule of 2026-10-05). The "April 2011 survey surface" option is an evidence layer only. Differences are shown in the viewer as the crest-cover readout for both the design crest and the highest surveyed point.

### 3.10 Later history (not modelled; dated, sourced)

| Date | Event | Source |
|---|---|---|
| 2008-06 | construction starts (lower layer 2008) | S3, S12 |
| 2009-09/10 | upper layer finished; Oct 2009 DGPS survey: crest +0.05 to +0.65 m ACD (state modelled) | S3, S2 |
| 2009-11-19 | official opening | S12 |
| 2011-03-23 / 03-31 | council inspection finds "substantial changes"; reef closed for safety | S12 |
| 2011-04 | DGPS survey: one 70 m container lost about 80 t of sand, 4 m gap, 2 m crest dip (probably a propeller strike) | S2, S12 |
| 2011-08 | repairs by ASR begin, suspended for winter, never completed | S12 |
| 2011-09-28 | satellite image used for the outline | S1 |
| 2012 | adjacent container lost, gap up to 10 m | S2 |
| 2012-09 | ASR Ltd liquidated (one source: Nov 2012); insurance settlement 2013 | S12 |
| 2014-04 / 2017 | site re-branded "Coastal Activity Park": diving, snorkelling, kite and windsurfing; surfing dropped | S12 |
| 2017-12-26 | debris from the decaying bags still washing ashore | S12 |
| 2026-10-05 | Navionics still shows the shoal and a drying patch | S9 |

## 4. Validation

1. **Survey versus outline**: area of survey relief above 1 m = 3,841 m2 against 4,042 m2 (-5 %); IoU 0.90 without shift. (An earlier IoU of 0.77 came from tracing the -2/-3 m colour edge, not from a registration error.)
2. **Volume**: loft 13,119 m3 against about 13,000 m3 stated (+0.9 %); sensitivity (E10): slope 1:2 / 1:3 / 1:4 gives 14,184 / 13,119 / 12,161 m3 at crest +0.5; crest +0.2 / +0.8 gives 12,554 / 13,625 m3 at 1:3; r0 = 0.5 / 1.5 m gives 11,640 / 14,678 m3. So the stated volume is reproduced within the parameter ranges. The April 2011 survey relief volume is 9,573 m3 (damaged and smoothed). The designers' Fig. 3a design relief gives 11,540 m3 (project verification). Rendle (2016, P5): designers' footprint 4,474 m2 (Fig. 5.3 notes, p. 95) and 5,450 m2 (Table 4.4, p. 70), against the traced 4,042 m2 (+10.7 % / +35 %; the survey and satellite outline outranks the design drawings); designers' volume 11,900 m3 (Table 4.4, p. 70) and 12,200 m3 (bags 10,450 + fill 1,750, Fig. 5.3 notes), against the loft 13,119 m3 (+10.3 % / +7.5 %), inside the volume uncertainty. The text "about 1 ha" would need 1.3 m of mean thickness, which does not fit two layers of 1-5 m containers; 4,042 m2 gives 3.2 m.
3. **Crest**: highest surveyed crest point in April 2011 is +0.68 m ACD at (x 20, y 193) at the shoreward end; the Oct 2009 profile tops are +0.45 (across) and +0.65 (along the axis); design +0.5; Navionics: the shoal dries (crest at or above chart datum), no height printed. Rendle (2016, P5): the +0.5 m CD is the BUILT crest (p. 70), design 0 m CD (Table 4.4) / 0.3 m CD (Fig. 5.3). Bag counts differ by source: 32 containers (Rendle p. 68), about 46 labelled bags on the design drawing Fig. 5.3 (p. 95), 54-55 (Mead et al. 2010 and the card); bags missing from the final build (p. 122). The outline-based loft does not use a bag count.
4. **Datum (A3)**: crest and seabed pointers listed under A3; EMODnet (cells 115 m, relative to LAT) along x = 0: y 100-200: -3.99 m, y 220-320: -5.62 m, y 340-440: -7.05 m; the survey read as ACD gives -1.4 to -2.5 m and -3 to -4.8 m, so EMODnet is deeper by 1.3-1.7 m (older and smoothed grid); read as ODN the difference would be 2.7-3.1 m. Evidence favours ACD. Open question (P5, p. 70): Rendle gives local MSL as 1.66 m ODN ("1.66 mODN = MSL"), the official NTSLF table gives chart datum 1.40 m below ODN (model E6, default kept); Rendle's figures are not reliable on this point (she also states MSL = chart datum, Fig. 5.11). Resolve with the BODC/NTSLF Bournemouth mean sea level value for 2009-2011. Effect: 0.26 m on every absolute height.
5. **Navionics areas (m2)**, Navionics versus survey zones of the April 2011 surface:

| Level | Survey (Fig. 9) | SonarChart | Nautical Chart |
|---|---|---|---|
| drying, above 0 m ACD | 296 | 378 | 492 |
| shallower than 0.5 m | 956 | 950 | - |
| shallower than 1 m | 1,609 | 1,630 | 2,073 |

The drying-patch centroid is 12.7 m from the survey zone centroid. The close match at 0.5 and 1 m supports the same datum, but it may also mean that both come from the same survey; the viewer shows no survey date, and S10 says the SonarChart keeps drying areas from the Hydrographic Office and interpolates the contours below (so SonarChart is not fully independent of older chart data).
6. **Navionics soundings**: 16 soundings on seabed inside the model grid (4 inside the plotted survey area, 12 in the spline-extrapolated area): model minus Navionics mean +0.06 m, sd 0.49 m, r.m.s. 0.48 m (survey area: mean +0.41 m, sd 0.41, n = 4; extrapolated area: mean -0.05 m, sd 0.47, n = 12). The extrapolation is therefore good to about 0.5 m over 100-150 m beyond the survey; the largest single differences (+1.0 m and -0.9 m) are near the reef toe and at the edges.
7. **Design plan**: Mead Fig. 3a gives a design relief of crest about 0 m (colour bar saturates) over a seabed of -2.0 m (east) to -5.0 m (west), and -3.9 m / -3.1 m at the two ends of the long axis (soundings E and F on the annotated figure); compatible with the survey seabed -3.0 to -3.3 m west of the reef (Oct 2009) and -3.2 to -3.9 m at the shoreward end.
8. **Tide**: Table 1 reproduces the printed 1.76 m MHWS-MLWS range (E7); S2 quotes a maximum spring range of 1.96 m (different definition, not used).
9. **Datum test with the CCO profiles (A3, new 2026-10-07).** At the seaward end of each of the 11 CCO lines (y 21-38 m) the CCO height (m ODN, S13, independent of Fig. 9, EMODnet and Navionics) minus the spline seabed S of the Fig. 9 survey read as chart datum (E6) is **+0.03 m (sd 0.30 m, n = 11)**. Had the Fig. 9 zero been ODN the difference would be -1.37 m (4.5 standard errors away, standard error 0.09 m). The comparison extrapolates S by 60-80 m and spans two survey dates (2010 and April 2011), so a bias up to +-0.5 m is possible, still far below 1.4 m. The test supports ACD; it does not need EMODnet or Navionics.
10. **Beach variability between CCO dates** (same 11 lines, y -50 to +20 m): 2011-03-23 minus 2010-04-20: r.m.s. 0.28 m (11 lines); 2009-09-22 minus 2010-04-20: 0.49 m (2 lines, 5f00427 and 5f00424 only); 2009-11-30: 0.13 m (1 line). The date of the beach therefore matters at the 0.3-0.5 m level, i.e. 7-12 m in waterline position.
11. **Navionics z16, nearshore (S9).** On the z16 Nautical Chart screenshot (1.51 m/px) the colour boundaries were scanned along 31 shore-normal lines (x -150 to 150 m, every 10 m) and the extended seabed was read at those points: chart high-water line (yellow/green, y = -20 m on average) at model z = **+0.96 m** (sd 0.06; MHWS is +0.81 m, difference +0.15 m); chart datum 0 m (green/blue, y = 62 m) at **-1.66 m** (sd 0.13; expected -1.40 m, difference -0.26 m = 13 m of horizontal offset on the 0.02 slope); 1 m below chart datum (blue/white, y = 105 m) at **-2.53 m** (sd 0.10; expected -2.40 m, difference -0.13 m). The model contours follow the shape of the chart boundaries along the whole 320 m; the 1 m colour classes and the generalised chart lines explain the offsets. The y = 0 line lies in the middle of the chart's drying band. Figure: `annotated/navionics_nauticalchart_z16_nearshore_vs_model_annotated.png`.
12. **Navionics z16, offshore soundings (zone 5).** 25 spot soundings were read by eye from 2.4x crops (value +-0.05 m, position +-15 m); 11 lie inside |x| <= 160 m and y 428-604 m. With depth below chart datum `d = -(z_MSL + 1.40)`, model minus chart depth is mean **-0.27 m, sd 1.23 m, r.m.s. 1.20 m** (range -1.67 to +1.47 m). The misfit is organised: a fit `e = a + b x/100 + c (y - 500)/100` gives a = -0.23 m, **b = -1.21 +- 0.11 m per 100 m of x**, c = +0.31 +- 0.20 m per 100 m of y, residual sd 0.36 m: the model is too deep at x < 0 and too shallow at x > 0. The cause is the row y = 380 copied by E15 (alongshore slope +0.76 m per 100 m of x, spline extrapolation); the 27 EMODnet DTM 2024 cells at y 380-700 m, |x| < 400 m show no such trend (-0.07 m per 100 m of x, z at y = 500 m -8.85 m LAT = -10.31 m MSL, slope in y -0.98 m per 100 m, residual sd 0.20 m). Replacing row 380 by its alongshore mean gives mean -0.17 m, sd 0.51 m (0.45 m with the EMODnet gradient) against the soundings; this was **applied as D2 on 2026-10-10** (block D2 in 3.4; the numbers in this item up to here are the pre-D2 state; after D2: mean -0.18 m, sd 0.51 m, r.m.s. 0.51 m, range -0.85 to +0.46 m, fit trend -0.44 +- 0.09 m per 100 m of x, residual sd 0.27 m). The stated uncertainty of zone 5 was +-1.2 m before D2 (REPORT 9.1 gave +-1.0 m) and is +-0.5 m since. Scripts: `scripts/navionics_z16_offshore.py`, `scripts/offshore_tilt_check.py`; figure `annotated/navionics_nauticalchart_z16_offshore_soundings_annotated.png`.
13. **EMODnet DTM 2024 against the model (S5; project test REPORT 6.1).** Cell means (116 x 73 m cells, m LAT, converted with z_LAT = z_MSL + 1.46) are deeper than the model seabed in the 7 cells fully inside the old grid and seaward of y = 90 m by **1.80 m on average (sd 0.66 m, range 1.14 to 3.05 m)**; the three best-sampled cells (n = 12) give 1.14, 1.39 and 1.30 m; the reef cell gives 1.39 m (EMODnet -5.62 m LAT against the model seabed -4.23 m) and 2.52 m against the as-built loft. The DTM shows no reef (the cells are larger than the reef, the source patch CDI 117452 dates, by inference from the release history, from about 2011-2012 and is itself smoothed). The offset is not constant (1.1 to 3.1 m), so it is not a datum shift; no EMODnet level enters the model; only its slope (E15) does, and that slope reproduces the cell means up to y = 605 m within about 0.8 m.

## 5. Uncertainty

Propagation (independent errors, first order): `sigma_f^2 = sum_i (df/dx_i)^2 sigma_i^2`.

- Crest in the model frame (E6): `z_crest,MSL = h_c - D`, `sigma^2 = sigma_hc^2 + sigma_D^2`, with sigma_hc = 0.3 m (A6), sigma_D = 0.1 m (A4): **sigma = 0.32 m**. Crest below LAT: `d_LAT = -(h_c - z_LAT)`, so the crest stands 0.56 m above LAT (d_LAT = -0.56 m), `sigma^2 = sigma_hc^2 + sigma_LAT^2`, sigma_LAT = 0.05 m (table precision): **sigma = 0.30 m**.
- Reef height at a point: `H = z_c - S`, `sigma_H^2 = sigma_hc^2 + sigma_read^2 + sigma_tps^2`, with colour read 0.2 m and interpolation under the reef 0.3 m (TPS ring r.m.s. 0.02 m, but the pre-reef seabed is unobserved): **sigma_H = 0.47 m** on a mean height of 3.2 m (median surveyed relief 2.3 m, maximum 4.1 m, after damage and smoothing). The datum risk is separate: if the survey zero were ODN, S would be 1.4 m higher in the model frame and H smaller by 1.4 m (absolute heights of the survey shift, relief of the survey does not).
- Beach and nearshore (zone 3, E13): `sigma^2 = sigma_date^2 + sigma_D^2 + (sigma_pos tan(beta))^2` with sigma_date = 0.28 m (validation 10), sigma_D = 0.1 m (ODN = MSL, A4) and the position error 5 m on a slope tan(beta) = 0.04 (0.2 m): **sigma = 0.36 m**. A waterline at a given level is displaced by `sigma / tan(beta)` = about **9 m**. Blend zone (code 4): 0.5 m (A15). Offshore zone 5: **0.5 m** since D2 (validation 12; it was 1.2 m before D2), correlated along x.
- Seabed depth at a point inside the survey: sigma = 0.2 m (colour read) plus the plot's own interpolation; extrapolated: 0.5 m from the Navionics comparison (validation 6), growing with distance.
- Volume: `(sigma_V/V)^2 = (sigma_A/A)^2 + (sigma_H/H)^2 + (sigma_m)^2`, with area +-5 % (1 m outline error on a 120 x 45 m field), height 0.47/3.2 = 15 %, slope 5 %: about **16 %** (the sensitivity runs in validation 2 span -12 % to +14 %).
- Outline: +-1 m on the west, east and south edges, +-1.1 m on the shoreward edge (S7); position of the whole frame relative to the true geography about +-5 m (Esri georeference, OSGB conversion).
- Navionics: area +-10 % (pixel read, boundary smoothing), soundings +-0.05 m read, +-1 m in position.
- Vertical exaggeration: affects only the picture. At e = 3 a height error of 0.3 m looks like 0.9 m; slopes, crest cover and volume look larger by e. Use e = 1 for any quantitative reading and for photo matching.

## 6. Confidence

**Level: medium.** Against the rubric: the plan shape is itself rated medium (area 60 % below a repeated "about 1 ha" in the literature, three plan-view sources agree with each other); the seabed is read from a real DGPS plot (+-0.2 m) and confirmed by 16 independent Navionics soundings (mean difference +0.06 m); the as-built crest is given by the designers and checked against the Oct 2009 profiles (+-0.3 m); tide levels come from a gauge table in the design paper and the datum offset from the national tide facility. What keeps it from "high": the zero of the survey plot is an assumption (A3), strongly supported but not stated by the authors (the text is garbled); the as-built flanks and the flat crest are idealised (A6, A7; the two-level "focus" and "wedge" sections of the design are not published); the beach and the pre-reef seabed under the reef are interpolated (A8, A10); no as-built survey grid exists in the sources, only profiles of October 2009.

## 7. Limitations and unknowns

| Gap | How it could bias the model | What would resolve it | Lior can supply |
|---|---|---|---|
| vertical datum of the Fig. 9 plot and of Navionics not stated | all absolute heights +-1.4 m if wrong (relief unchanged) | Rendle PhD thesis (Plymouth PEARL 412, bot-checked), CCO survey metadata, or the Navionics app datum setting | Navionics app: depth readings and the datum / tide setting; the thesis via a normal browser |
| as-built plan not directly observed (outline from 2011-09-28) | outline may differ by a few m on the damaged offshore half | a 2009-2010 aerial image | Google Earth Pro historical imagery 2009-2010 |
| crest height along the whole reef is the design value | local crest heights +-0.3 m; "focus" and "wedge" sections have different heights | Oct 2009 survey grid, thesis bag layout | thesis, CCO data request |
| beach and surf line | since 2026-10-07 the beach is the measured CCO surface of 2010-04-20 (+-0.36 m, waterline +-9 m); the 2011-09-28 surf line y = 0 is at an unknown tide; other dates differ by 0.1-0.5 m | CCO profiles of other dates (all 2004-2026 are in `src/cco_profiles/`); a dated waterline with known tide | Google Earth Pro waterline in a dated image |
| seabed beyond y = 380 m (zone 5, y 380-650) | extrapolation along the EMODnet slope from the alongshore mean of a spline row (flat alongshore since D2, 2026-10-10); r.m.s. 0.5 m against 11 Navionics soundings (1.2 m before D2); contours assumed parallel to x (A16); a 1.1 m step between rows y = 378 and 380 at the x edges (D2) | a real bathymetric survey (CCO / UKHO) of y 40-100 m and y 312-650 m | ask CCO whether nearshore or offshore bathymetry of 2009-2012 exists for Poole Bay |
| gap y about 40-100 m (zone 4) between the CCO lines and the Fig. 9 rim | spline plus decayed offset, +-0.5 m | same survey as above | - |
| vertical datum of the CCO ODN heights vs MSL | ODN = MSL assumed within +-0.1 m (A4) | tide-gauge MSL 2009-2011 at Bournemouth (NTSLF / BODC) | - |
| EMODnet CDI 117452 metadata (vertical reference and date of the source survey of the DTM cells) | would give a third datum check and the survey age | the CDI record page https://cdi.seadatanet.org/ (EDMO 2607 OceanWise) | open the record in a normal browser |
| Navionics survey date, drying height | cannot tell what epoch the shoal shows | Navionics app (tap on the drying area) | Navionics app |
| no time curve of the tide, double high water not modelled | the "level" is a static picture | Bournemouth predictions (UKHO EasyTide) for the photo time | tide table for the photo date |
| no bag texture | photo matching of the surface texture is impossible; only silhouette and horizon | container layout from the thesis | thesis |

See `REQUESTS_FOR_LIOR.md` for exact points and values to read.

## 8. References

- Duchon, J. (1977). Splines minimizing rotation-invariant semi-norms in Sobolev spaces. In W. Schempp and K. Zeller (eds), *Constructive Theory of Functions of Several Variables*, Springer, 85-100.
- EMODnet Bathymetry Consortium (2026). EMODnet Digital Bathymetry (DTM). https://ows.emodnet-bathymetry.eu/wms (queried 2026-10-05).
- Channel Coastal Observatory, Southeast Regional Coastal Monitoring Programme (2026). Beach profile surveys, lines 5f00424-5f00429, survey of 2010-04-20 [data]. https://coastalmonitoring.org/ (accessed 2026-10-06). Open Government Licence v3.0 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). Not for navigation.
- EMODnet Bathymetry Consortium (2024). EMODnet Digital Bathymetry (DTM 2024). https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1 (ERDDAP `bathymetry_dtm_2024`, queried 2026-10-06). CC BY 4.0.
- Esri, Maxar, Earthstar Geographics and the GIS User Community (2011). World Imagery Wayback, release 10, capture date 2011-09-28. https://livingatlas.arcgis.com/wayback/ (retrieved 2026-10-04).
- Garmin Ltd / Navionics (2026). Marine Maps viewer, Nautical Charts and SonarChart Maps. https://maps.garmin.com/en-US/marine (accessed 2026-10-05). Not for navigation.
- Herbert, R.J.H., Collins, K., Mallinson, J., Hall, A.E., Pegg, J., Ross, K., Clarke, L. and Clements, T. (2017). Epibenthic and mobile species colonisation of a geotextile artificial surf reef on the south coast of England. *PLoS ONE* 12(9): e0184100. https://pmc.ncbi.nlm.nih.gov/articles/PMC5604948/ (accessed 2026-10-05).
- Leisure Opportunities (2012). Future of Boscombe surf reef in doubt. https://www.leisureopportunities.co.uk/news/Future-of-Boscombe-surf-reef-in-doubt/303273 (accessed 2026-09-24).
- Mead, S., Blenkinsopp, C., Moores, A. and Borrero, J. (2010/2011). Design and construction of the Boscombe multi-purpose reef. *Coastal Engineering Proceedings* 1(32), structures.58 (ICCE 2010; OJS article 1352; DOI not confirmed). https://icce-ojs-tamu.tdl.org/icce/article/view/1352 (accessed 2026-10-05).
- National Tidal and Sea Level Facility (n.d.). Chart datum and ordnance datum. https://ntslf.org/tides/datum (accessed 2026-10-05).
- Newsroom.co.nz (2021). The Kiwi scientist and the failed surf breaks. https://newsroom.co.nz/2021/12/06/the-kiwi-scientist-and-the-failed-surf-breaks/ (accessed 2026-09-24).
- Rendle, E.J. (2016). The Environmental, Social and Economic Impacts of an Artificial Surf Reef - The UK Experience. PhD thesis, University of Plymouth. https://pearl.plymouth.ac.uk/bms-theses/412/ (P5 in the project, S15 above).
- Rendle, E. and Davidson, M. (2012). An evaluation of the physical impact and structural integrity of a geotextile surf reef. *Coastal Engineering Proceedings* 1(33) (ICCE 2012; OJS article 6794; DOI not confirmed). https://icce-ojs-tamu.tdl.org/icce/article/view/6794 (accessed 2026-10-05).
- riverlevels.uk (n.d.). Tide at Bournemouth. https://riverlevels.uk/tide-bournemouth (accessed 2026-10-05).
- Solent Forum (n.d.). Waves and tides. https://solentforum.org/solent/our_coastal_zone/waves_and_tides/ (accessed 2026-10-05).
- Three.js authors (2024). three.js r170, MIT licence. https://threejs.org/
- University of Liverpool (n.d.). Depth surveys; crowd sourced charts (Navionics SonarChart, TeamSurv). https://www.liverpool.ac.uk/~cmi//mag/survey_h.html (accessed 2026-10-05).
- Virtanen, P. et al. (2020). SciPy 1.0: fundamental algorithms for scientific computing in Python. *Nature Methods* 17, 261-272.
- Wikipedia (2026). Boscombe Surf Reef. https://en.wikipedia.org/wiki/Boscombe_Surf_Reef (accessed 2026-09-24).
- Wavve Boating (2024). Navionics Chart Viewer website "decommissioned" by Garmin. https://www.wavveboating.com/boating-tips/navionics-chart-viewer/ (accessed 2026-10-05).

## 9. Audit registers (source audit of 2026-10-10)

Added by the source audit of 2026-10-10 (details and the statement-by-statement table: `../SOURCE_AUDIT_2026-10-10.md`). No model value was changed. "P5" in sections 4 and 7 is source S15. Decision ids D1-D3 follow Lior's list in the root `REQUESTS_FOR_LIOR.md` (D2 = offshore flattening, D3 = beach date); BD1-BD10 are decisions of this model.

### 9.1 How each source was used, by model element

| Source | Read off / how | Accuracy of the reading | Feeds | Role |
|---|---|---|---|---|
| S1 Esri Wayback 2011-09-28 | outline of the bag field traced by hand on the z18 mosaic (25 vertices), checked with an independent per-channel stretch; georeference by Web-Mercator bounds (E2, E3) | +-1 m (W, E, S edges), +-1.1 m (shoreward edge); frame +-5 m | plan; frame; surf line y = 0 | primary |
| S2 Rendle and Davidson 2012, Fig. 9 | colour read of the printed DGPS plot by nearest colour-bar colour (E5), gridlines to OSGB36 (E4), resampled to 1 m then 2 m grid, thin-plate-spline ambient seabed (E9); profiles and text for crest, flank, damage | +-0.2 m height (colour read), position +-5 m (Helmert) | seabed y about 100-305 m; under-reef seabed; evidence layer (April 2011 surface); flank slope (A7); crest check | primary |
| S3 Mead et al. 2010 | design crest "0.5 m above chart datum"; Table 1 water levels typed in (to 0.01 m); 13,000 m3 and 54 containers; design plan Fig. 3a read by eye for the design depth | table values exact; Fig. 3a +-0.3 m | crest (A6), tide levels (E7), volume check, validation 7 | primary |
| S4 NTSLF | CD 1.40 m below ODN (table row Bournemouth) | 0.01 m as printed | datum conversion E6 | primary for the offset |
| S5, S14 EMODnet | DTM cell means (WMS 2026-10-05; ERDDAP 2026-10-06); only the cross-shore SLOPE 0.0141 is used | slope +-0.0010; levels 1.1-3.1 m deeper than the survey, so NOT used | zone 5 slope (E15); datum plausibility (A3); validation 13 | slope used, levels rejected (BD7) |
| S6 Herbert et al. 2017 | text: 0-5 m CD, exposed at low springs, 220 m offshore, 210 m east of pier | text | A3 evidence, crest exposure check | context and validation |
| S7 project shape.json | verified polygon (4,042 m2) | +-1 m | plan | primary (derived from S1) |
| S8 riverlevels.uk | usual range -1.08 to +1.11 m ODN, mid-range +0.02 | 0.01 m; web page of unknown method | A4 (ODN = MSL +-0.1 m) | weak support, assumption A4 |
| S9 Garmin Navionics | shoal areas by colour class on z18 screenshots; soundings read by eye; z16 nearshore boundaries scanned along 31 lines; 11 offshore soundings read by eye | areas +-10 %; soundings +-0.05 m, position +-1 m (z18) / +-15 m (z16) | validation 5, 6, 11, 12 only; NOT used to build any cell | validation only |
| S10, S11 | text statements (SonarChart policy; tide range, double high water) | text | caveat on S9 independence; tide context | context |
| S12 Wikipedia, Leisure Opportunities, Newsroom.co.nz | dated history | secondary | section 3.10, viewer history table | context only, not in any number |
| S13 CCO profiles 2010-04-20 | 11 lines, OSGB36 converted with the Fig. 9 chain, linear across lines (E13), CCO offset decayed over 40 m (E14) | beach +-0.36 m; blend +-0.5 m | beach (zone 3), blend (zone 4), datum test of A3 (validation 9) | primary for the beach; independent datum test |
| S15 Rendle 2016 | text and figures read 2026-10-10 | page/figure per row in `../P5_RENDLE2016_NOTES.md` | none; validation 2-4 and BD10 | validation only |
| Gemini folder | nothing used | - | - | rejected (standing rule 2) |

### 9.2 Assumption register (A1-A16): effect and replacement

| Id | Assumption (short) | Why | Effect if wrong | What would replace it |
|---|---|---|---|---|
| A1 | footprint of 2009 = footprint seen on 2011-09-28 | same envelope in the 2025 image (S7); damage lowered crests, not the envelope | edge shift of a few m on the offshore half; area +-5 % (1 m on a 120 x 45 m field) | 2009-2010 aerial image (Google Earth Pro) |
| A2 | Fig. 9 is a faithful smooth rendering of the DGPS surfaces | author-made plot | features finer than 3-5 m untrustworthy; +-0.2 m | the council xyz survey |
| A3 | Fig. 9 zero = chart datum | CCO test +0.03 m vs -1.37 m (validation 9); crest and design depths; Navionics areas; Rendle Fig. 5.6 content | all absolute survey heights +-1.4 m; relief, volume and shape unchanged | CDI 117452 metadata or the survey report; viewer switch shows the alternative |
| A4 | ODN = MSL within +-0.1 m | S8 range centred +0.02 m ODN | all MSL heights +-0.1 m; crest sigma 0.32 m | NTSLF/BODC mean level 2009-2011 |
| A5 | pier gauge levels apply at the reef 1.5 km away | same bay, no local gauge | effect not quantified (no local record) | local tide record |
| A6 | built crest flat +0.5 m ACD (Mead, Rendle p. 70) | designers' value, Oct 2009 tops +0.05 to +0.65 m | +-0.3 m crest; volume 12,554 / 13,625 m3 at crest +0.2 / +0.8 (-4 % / +4 %); crest cover and the dry-at-low-water statement | Oct 2009 as-built survey |
| A7 | flanks 1:3, 1 m relief at the outline | Fig. 9 section 1:3-1:4 (SW), 1:5-1:7 (NE), median 1:5.8 | +-30 %; volume 14,184 / 12,161 m3 at 1:2 / 1:4 (+8 % / -7 %); r0 0.5 / 1.5 m: 11,640 / 14,678 m3 | Oct 2009 survey grid |
| A8 | seabed under the reef = spline of the surroundings | no pre-reef survey | +-0.3 m (volume about +-9 % on 3.2 m mean height); scour ignored | pre-construction survey |
| A9 | Navionics depths are chart datum; same structure | viewer states no datum | validation 5, 6, 11, 12 shift by up to 1.4 m (they are not model inputs) | Navionics app datum setting |
| A10 | beyond the survey the seabed is spline / CCO / EMODnet slope; y = 0 line drawn at unknown tide | no data | zone dependent, 0.5 m (zones 4, 5), waterline +-9 m | CCO or UKHO nearshore survey |
| A11 | static water level | simplification | tide time curve, set-up, surge and double high water absent | tide table for a photo date |
| A12 | smooth 1 m heightfield, 54 containers not modelled | layout unpublished (Rendle: no as-built plan) | no texture, no overhangs; silhouette matching only | as-built layout drawing |
| A13 | S1 pixel scale = Web-Mercator ground scale | latitude formula; pier check measured 167.5-178 m for a 180 m pier | up to -7 % on lengths at the worst reading, about -1 % at the best | pier survey length |
| A14 | CCO 2010-04-20 beach represents 2009-2011 | the only date with all 11 lines | 0.28-0.49 m, waterline 7-12 m (D3) | other CCO dates (in `src/cco_profiles/`) |
| A15 | transition rows = spline + decayed CCO offset | no data in y 40-100 m | +-0.5 m | nearshore survey |
| A16 | zone 5 flat alongshore, 1.41 % slope, contours parallel to x | EMODnet slope; D2 | +-0.5 m r.m.s.; residual trend -0.44 +- 0.09 m per 100 m of x; step 1.13 m at x edges | offshore survey |

### 9.3 Decision register

| Id | Choice | Options | Decided by, date | Reason |
|---|---|---|---|---|
| BD1 | State drawn | as-built 2009 / April 2011 damaged / design | Lior rule 4-5 (CLAUDE.md), applied 2026-10-05 | default = built version; survey surface kept as evidence layer |
| BD2 | Outline source | Wayback 2011 trace / Fig. 9 relief / Mead design plan | agent, 2026-10-04/05 | only plan-view trace with date and checks; agrees with April 2011 survey (IoU 0.90) |
| BD3 | Datum of Fig. 9 zero | chart datum / ODN | agent, 2026-10-05 (A3); supported 2026-10-07 and 2026-10-10 | evidence list in A3; viewer switch for the alternative |
| BD4 | ODN to MSL | ODN = MSL (A4) / local MSL 1.66 m (Rendle p. 70) | agent; 1.40 kept 2026-10-10 | official NTSLF value; 1.66 listed as open question |
| BD5 | Seabed extended to beach and offshore | camera zoom / extend grid | Lior request 2026-10-07 ("make the 3D larger"); agent chose CCO data | measured source available (S13) |
| BD6 | Beach date | 2010-04-20 (11 lines) / autumn 2009 (2 lines) | agent 2026-10-07; Lior's D3 default 2010-04-20 | all lines exist; variability 0.1-0.5 m |
| BD7 | EMODnet use | slope only / levels too | agent 2026-10-07 | levels 1.1-3.1 m deeper than survey, no reef in the DTM |
| BD8 | D2 offshore flattening | keep spline tilt / flatten row y = 380 | agent proposed, applied 2026-10-10, Lior did not object | tilt unsupported by EMODnet; r.m.s. 1.20 to 0.51 m |
| BD9 | Crest value | design 0 / 0.3 m CD, built +0.5 m CD | agent 2026-10-05; relabelled built 2026-10-10 | Rendle p. 70 states built crest; value unchanged |
| BD10 | Use of Rendle 2016 | replace outline or seabed / validate only | agent 2026-10-10 | no as-built plan in P5; Fig. 5.7 is the same survey as Fig. 9 |
| BD11 | Navionics | model input / validation only | agent 2026-10-05 | datum and date unknown, A9 |
| BD12 | Original survey and reef cells untouched in the extension | rebuild all / keep | agent 2026-10-07 | earlier results and the page "All (compare)" view stay valid |

### 9.4 Confidence per element

| Element | Level | Reason |
|---|---|---|
| Plan | medium | three plan sources agree (+-1 m) but area is 60 % below the repeated "about 1 ha" |
| Crest | medium | built +0.5 m CD (Rendle p. 70, Mead) vs Oct 2009 tops +0.05 to +0.65 m: +-0.3 m; flat crest is idealised |
| Seabed (survey part) | medium-high for relief, medium for absolute height | +-0.2 m read; datum A3 supported by two independent tests |
| Beach, nearshore | medium | measured CCO, +-0.36 m, other date than 2011 |
| Zone 4, zone 5 | low-medium | interpolated / extrapolated, +-0.5 m |
| Tides | medium | pier gauge 1.5 km away, ODN = MSL assumed (A4, A5) |
| Volume | medium | 13,119 m3 vs about 13,000 (+0.9 %); about 16 % propagated |
| Overall | **medium** | unchanged; the survey datum and the as-built flanks are assumptions |

### 9.5 Processing methods not obvious from the text

Hand tracing (outline); colour-bar nearest-colour classification (Fig. 9); Helmert OSGB36-WGS84 with pyproj; template matching between the two Fig. 9 maps (inpainting of the section line, TELEA); Gaussian smoothing sigma 1 m; thin-plate spline (scipy RBFInterpolator); signed-distance loft (E10); smoothstep decay (E14); headless-Chrome previews (`scripts/render_previews.py`). The scripts are in `scripts/` and `build_3d.py`; each number's script is named in `SOURCES_3D.md`. Artificial-intelligence tools: no output of Gemini is used; image reading, scripts and text were produced by Claude agents (project sessions 2026-10-05 to 2026-10-10) and every value was checked against its original source as logged in `SOURCES_3D.md`.

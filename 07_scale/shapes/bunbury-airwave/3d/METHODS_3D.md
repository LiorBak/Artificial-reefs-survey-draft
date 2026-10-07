# METHODS_3D - Bunbury Airwave (Bunbury Back Beach, Western Australia): three-dimensional model

Built 2026-10-05 by `build_3d.py` (numbers in this note are filled in by that script from `shape.json`, the reef card, `data/lidar_*`, and `data/nav_transects.json`; edit `METHODS_3D.template.md`, not this file). Companion notes: `SOURCES_3D.md` (running log of what was read where), `REQUESTS_FOR_LIOR.md` (what could not be read), `annotated/` (the sources with the readings marked: lidar figures and N1-N4 for Navionics).

## 1. Summary

The model shows **the Bunbury Airwave as installed in December 2019**: a 12 m diameter bladder of Hypalon (synthetic) rubber with glued seams, partly filled with sand slurry (washed beach sand, 140-150 t by the developer's own figures), water and air, lying on the nearshore seabed of Back Beach, 30-50 m off the waterline, with the water surface at any tidal plane from LAT to HAT. It is **not a rock reef and not a working reef**: the installation began in the week of 9 December 2019, a diver spotted a tear along a glued seam on Friday 13 December when the bladder was about 90 % complete and not fully anchored, and it was removed within about three days. The card verdict is **FAILED** and stays so; the developer's page says "In 2018" and "wasn't a failure", but the year is contradicted by every dated 2019 report and no independent source documents rideable waves (section 2.1). The seabed is the WA Department of Transport airborne-lidar survey of 2009 (10 m grid), cross-checked against Garmin Navionics SonarChart contours I counted from the web viewer (RMS 0.32 m once its depths are read below LAT, the Australian chart datum); tides are the Port of Bunbury planes (GHD 2021). The footprint is the verified circle of `shape.json`; the height (1.6-2.0 m), crest depth ("about 1 m" at low tide) and profile are text-based, and the surface drawn is a symmetric spherical-cap stand-in because no cross-section of the installed bladder exists. Later events (removal, redesign, the 2025 granite proposal) are **not modelled**; they are in the viewer caption and in section 2.1. The 3D confidence is **MEDIUM**: the seabed and tides are sourced and independently cross-checked, but the reef geometry is text-based, the crest depth below MLLW is 0.69 +- 0.66 m (Monte Carlo over the position and height ranges) against "about 1 m" in the text, and the real bladder was partly filled and torn.

## 2. Data sources

Access dates are 2026-10-05 unless stated. "Licence" is the licence stated by the publisher; reuse of every private research copy is NOT cleared for public release.

| id | reference (author-year) | what it contributed | resolution / date | licence |
|---|---|---|---|---|
| S_shape | This project (2026). `shape.json`, verified 2026-10-04: 29-vertex outline traced on the Raised Water Research drone photo "Airwave from above" (Raised Water Research 2019b) | plan outline (circle, 112.1 m2) | photo 956 x 587 px, no scale bar: size from the text-stated 12 m | photo (c) RWR, private copy |
| S_card | This project (2026). Reef card `02_research/reefs/bunbury-airwave.json` (verified 2026-09-24; developer-account check 2026-10-05), references R1-R24 | verdict, install dates, material, fill, chronology | text | n/a |
| S_RWR | Raised Water Research (n.d.). *Bunbury Airwave* (spot page). https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/bunbury-airwave/ | "shallow point about 1 m under the surface at low tide", "rises about 2 m off the sea floor", "30-45 meters off the beach" | web text | unknown |
| S_Tracks19 | Tracks Magazine (2019). Airwave set for live trial at Bunbury, 15 Nov. https://tracksmag.com.au/airwave-set-for-live-trial-at-bunbury-534049 | 12 m diameter, 1.6 m tall "at the highest point", "approximately 45 metres off the low tide mark", sand + air fill | web text | unknown |
| S_ABC19 | ABC News (2019). Bunbury's Back Beach surfers deflated as artificial reef, Airwave, tears during installation, 16 Dec. https://www.abc.net.au/news/2019-12-16/word-first-surf-reef-tears-during-installation/11803228 | tear, 90 % complete, not completely anchored, "two-metre-high, 12-metre-wide" | web text | (c) ABC |
| S_BunMail | Bunbury Mail (2022). Airwave founder Troy Bottegal ..., 22 Mar. https://www.bunburymail.com.au/story/7667604/bunbury-still-set-to-become-surfing-destination/ | Hypalon, glued seams, 140 t of sand, removal within three days, developer's account of one 0.75 m wave | web text | (c) | 
| S_Tracks21 | Kennedy, L. (2021). The Airwave Pumps Again. *Tracks Magazine*, 8 Oct. https://tracksmag.com.au/the-airwave-pumps-again | "skateboard ramp" profile of the first bladder; admission that the first trial failed; redesign | web text | unknown |
| S_Waveco | Waveco Pty Ltd (2025). All About Us - the story behind the Airwave (About page, last modified 2025-12-22). https://www.waveco.com.au/about/ | the developer's own account ("In 2018 ... 150-tonne sand-slurry bladder ... successfully created peeling waves ... wasn't a failure"). **Self-published, not independent.** | web text | (c) Waveco |
| S_lidar | Western Australia Department of Transport (2009). *Two Rocks - Naturaliste Lidar 2009* (survey Lidar2009TRBS), BAG file BU2009TRBS_Lidar.bag, 67,442,256 bytes, md5 a5742ce2217aef90670cee1426f76933. https://dotazprdauegisextpubst01.blob.core.windows.net/transport-wa-public/bathymetry/rasters/BU2009TRBS_Lidar.bag; index https://services6.arcgis.com/67Ks15nDmWoIbK8b/arcgis/rest/services/Survey_index_linkedbagfiles/FeatureServer/0 | seabed (primary) | 10 m cells, GDA94 / MGA zone 50, 4978 x 1693 cells; elevation positive up; uncertainty layer 0.47 m at the reef zone (type not stated); survey index: vertical datum AHD, DataRestri NO | "Approved for Public Release", "Not to be used for navigation" |
| S_tide | GHD (2021). *Tidal Inundation Monitoring and Modelling Report*, Appendix B of the Southern Ports Authority Turkey Point Access Road approvals, Table 1 "Tidal planes for Port of Bunbury" (source cited there: Department of Defence 2018). https://www.epa.wa.gov.au/sites/default/files/PER_documentation2/App%20B%20-%20Tidal%20innudation%20report.pdf | HAT, MHHW, MLHW, MSL, MHLW, MLLW, LAT in m CD and m AHD | rounded to 0.1 m; gauge in Bunbury Port, about 3 km NE | public record |
| S_DoTidx | Western Australia Department of Transport (n.d.). *Bathymetric survey index* (same URL as the index above), Bunbury records: vertical datum LAT, AHD_Diff 0.57 below | independent check of LAT = AHD - 0.57 m | table | as above |
| S_nav | Garmin Ltd (2026). *Navionics Marine Maps web viewer*, SonarChart Maps and Nautical Charts layers, metres. https://maps.garmin.com/en-US/marine/ (formerly https://webapp.navionics.com/). Screenshots in `src/navionics/` | independent seabed contours and spot soundings, zoom 18 (maximum) | 0.2495 m per pixel (zoom 18, device pixel ratio 2); survey dates not shown; datum and contour interval not stated by the app | (c) Garmin; private research copy; "Not to be used for navigation" |
| S_sat | Esri (2025). *World Imagery*, Back Beach tile of 2025-08-30 (private copy `src/sat_backbeach_current.png`) | approximate waterline for the site point; surf-zone foam over the lidar contours (figure `lidar_contours_on_satellite.png`) | about 0.3 m/px | rights not cleared |

The full list of reference ids R1-R24 of the card is: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R13, R15, R18, R19, R20, R21, R22, R23, R24. Other sources used for the chronology only (full citations in section 8): Tracks Magazine (2019, 12 Aug), Raised Water Research (2019, 14 Oct and 16 Dec), ABC News (2019, 13 June), The Inertia (2019), SurferToday (2018, 2019), South Western Times (2020), Swellnet forum (2019-2021, secondary), ABC listen (2022).

### 2.1 Chronology of the structure: what state is modelled, what is not, and why December 2019

Dates are as the card records them (`year`: "Installation attempted December 2019 (failed during install); concept development began ~2008-2009 [R2]"). The date check below is the one in the card's `developer_account` table (5 claims checked on 2026-10-05).

| date | event | in the model? | source (card refs) |
|---|---|---|---|
| 2018-08 | Waveco's crowd-funding campaign (Kickstarter) fails; nothing deployed. The only 2018 events found. | no (caption/methods only) | R3, R19 |
| 2019-06-13 | ABC: the Airwave is set to be installed in November 2019. | no (caption/methods only) | R2 |
| 2019-08-12 | Tracks: first live trial planned for mid-November at about 45 m offshore; the crowd-funding was 'last year'. | no (caption/methods only) | R23 |
| 2019-10-14 | Raised Water Research: construction half-way. | no (caption/methods only) | R4 |
| 2019-11-15 | Tracks: 12 m diameter, 1.6 m tall at the highest point; live trial 'in the next couple of months'. | no (caption/methods only) | R9 |
| 2019-12-07 to 12-13 | Installation week (from Mon 9 Dec): slurry pump and hoses on the beach (7 Dec, forum observer); three divers and a boat. | no (caption/methods only) | R9, R15, R1 |
| 2019-12-13 (Fri) | A diver spots the tear along a glued seam: bladder about 90 % complete, not fully anchored. THIS INSTALLED, TORN STATE IS WHAT THE MODEL SHOWS (geometry only). | **yes (geometry)** | R1, R5, R7, R15 |
| 2019-12-16 (Mon) | Tear reported (ABC, RWR, The Inertia, SurferToday). Bottegal: unexpected deep swell and undertow. | no (caption/methods only) | R1, R5, R6, R7 |
| within about 3 days | Bladder removed from the water (reports range from about 5 hours to 3 days). | no (caption/methods only) | R8, R18, R15 |
| 2020-07-09 | Second prototype planned for December 2020 (about A$300,000 more needed); not confirmed built. | no (caption/methods only) | R18 |
| 2021-10-08 | Tracks: Bottegal 'readily admits' the first trial was a failure; sand pumped too heavily into one quadrant; redesign with welded compound, only tank-tested. | no (caption/methods only) | R22 |
| 2022-03-22 | Bunbury Mail: Bottegal says 'not a failure'; glued Hypalon seams; a lone 0.75 m wave seen (developer's account only); back in the water 'by Summer 2024'. | no (caption/methods only) | R8 |
| 2025 | Waveco's Bunbury proposal is a granite (rock) reef, not the rubber Airwave. The About page (last modified 2025-12-22) says 'In 2018 ... successfully created peeling waves ... wasn't a failure' (year contradicted, waves not independently supported). | no (caption/methods only) | R20, R21 |

**Waveco's "2018" versus the record.** The developer's page says: "In 2018, we deployed a 150-tonne sand-slurry bladder at Bunbury’s Back Beach. While it successfully created peeling waves, a final-day overpressure event led to a seam split. It wasn't a failure—it was the catalyst for our next breakthrough." (Waveco 2025; the passage is undated; the page was created 2019-08-11 and last modified 2025-12-22). The independent record places the installation in **December 2019**: ABC (2019a) said on 13 June 2019 that it would be installed in November; Tracks (2019a) on 12 August 2019 described a trial planned for mid-November and a crowd-funding campaign "last year"; Raised Water Research (2019a) said on 14 October 2019 that construction was half-way; Tracks (2019b) on 15 November said the live trial would be "in the next couple of months"; and then ABC (2019b), Raised Water Research (2019b) and The Inertia (2019) reported the tear on 16 December 2019, with a forum observer (Swellnet 2019) describing a slurry pump and hoses on the beach on 7 December and the bladder "partially filled" on 13 December. The only 2018 events are a failed Kickstarter and a "may be installed" preview (SurferToday 2018). One outlier, the 2022 Bunbury Mail intro ("four years since", a supplied photo captioned 2018), conflicts with every dated 2019 report. **This model therefore uses December 2019 (installation week of 9 December, tear spotted Friday 13 December), not 2018.** The geometry does not depend on the date, but the label does.

| Waveco claim (2025) | independent record (card) | assessment |
|---|---|---|
| "In 2018, we deployed" | December 2019, see above | contradicted |
| "a 150-tonne sand-slurry bladder" | sand slurry corroborated (Tracks 2019b, Bunbury Mail 2022, RWR, forum observer); mass developer-only, 140-150 t | type consistent; mass unverified |
| "successfully created peeling waves" | no independent report, photo or video of surfable waves; at most one 0.75 m wave, reported by the developer 27 months later; nobody rode it | not independently supported |
| "a final-day overpressure event led to a seam split" | seam split confirmed; "overpressure" matches his 2021-22 explanations, not his 2019 one (deep swell and undertow); the tear was on about the fifth day, at about 90 % complete | partly supported |
| "It wasn't a failure" | Tracks (2021): Bottegal "readily admits" the first trial was a failure; no completed trial; second prototype unconfirmed; 2025 proposal is a granite reef | a judgement, not a checkable fact |

The card's verdict reason, verbatim: "The structure tore along a glued seam during installation (spotted Fri 13 Dec 2019, about 90% installed and not fully anchored), was removed within days, and never operated as a completed reef [R1][R5][R8][R18]. No independent report, photo or video documents rideable waves on it; the only wave claim is the developer's own later account of one lone 0.75 m wave seen during installation [R8][R21]. The developer's page says the trial 'wasn't a failure' [R21], but it misdates the deployment to 2018 (it was December 2019), Tracks reported in 2021 that Bottegal 'readily admits' the first trial was a failure [R22], no second install is confirmed [R18][R8], and by 2025 Waveco's Bunbury proposal is a different (granite) design [R20]. Verdict kept as 'failed' after checking the developer's account (2026-10-05)." **The verdict stays FAILED; no developer claim overrides it** (rule of this project).

## 3. Methods

### 3.1 Coordinate frame and orientation

The model frame is the canonical frame of `shape.json`: metres, **x alongshore** toward bearing 12.32 deg true (NNE), **y seaward** toward bearing 282.32 deg true (WNW, x turned 90 deg anticlockwise), **z up**, z = 0 at mean sea level (MSL). (x, y, z) is right-handed; the viewer maps model (x, y, z) to three.js (X, Y, Z) = (x, z, -y), which is mirror-free. The origin O is the foot of the perpendicular from the site point on the fitted 0 m AHD contour of the 2009 lidar (MGA94 zone 50: E 372378.8, N 6311547.1); y = 0 is that contour (about the MSL waterline of 2009).

The contour was fitted to the zero crossings of the lidar along 201 grid rows (|north| <= 500 m): east = a + b north with a = 38.7 m and b = 0.2046 (relative to the site point; rms scatter 8.4 m). With t = (b, 1)/sqrt(1 + b^2) the unit vector along the contour and n = (-t_N, t_E) its seaward normal:

```
(E, N)_grid = O + x t + y n                                   (E1)
bearing_true = bearing_grid + gamma,   gamma = 0.754 deg   (PROJ, MGA94 zone 50 at the site)   (E2)
north in the model frame = (cos bx, cos by)                   (bx, by = true bearings of +x, +y)    (E3)
```

Orientation assumption (A1): +y is perpendicular to the 2009 0 m AHD contour. The Navionics 0 m line (green/blue edge) is tilted +2.4 deg against the model x axis (section 4, V9): slightly more than the +-2 deg contour scatter, which is plausible for two lines drawn 10 years apart.

### 3.2 Vertical datums and conversions

All elevations are held relative to AHD and converted to the model zero with the Port of Bunbury table (GHD 2021, Table 1: MSL = +0.1 m AHD):

```
z_MSL = z_AHD - (MSL - AHD) = z_AHD - 0.1 m                              (E4)
a depth d below datum D (D given in m relative to AHD):   z_AHD = D - d          (E5)
depth of a point at level L below a plane P (both m AHD):  d(L | P) = P - L        (positive = below)   (E6)
crest depth below plane P:                                  d_c(P) = P - (z_bed + H)                  (E7)
```

Tidal planes used (m relative to AHD; the model z is that minus 0.1): HAT 0.6, MHHW 0.2, MLHW +0.1, MSL +0.1, MHLW 0.0, MLLW -0.2, LAT -0.6 (LAT is the chart datum since 2009; in m above chart datum 1.3 / 0.9 / 0.7 / 0.7 / 0.6 / 0.5 / 0.1). In model z: HAT 0.5, MHHW 0.1, MHLW -0.1, MSL 0, MLLW -0.3, LAT -0.7 m. The range HAT - LAT is 1.2 m ("maximum tidal range of 1.2 m", "predominantly diurnal", GHD 2021). The DoT survey index gives LAT = AHD - 0.57 m for Bunbury (difference to the table: 0.03 m). The values are rounded to 0.1 m by the source; the gauge is the Bunbury Port inner harbour, assumed valid at Back Beach (A9). "Low tide" in the RWR crest-depth text is not defined; MLLW is assumed (A6) and LAT shown as the alternative (0.4 m lower).

### 3.3 Plan shape

The toe polygon (29 vertices, 112.1 m2) is read unchanged from `shape.json` (status verified, verified 2026-10-04, plan confidence medium, md5 f046605f97ddb20b3fb80a86d07b9a03). It is a circle seen at about 27 deg off nadir on the drone photo, rectified by stretching the minor axis; the 12 m scale is the text-stated diameter (so the agreement of 112.1 m2 with pi 6^2 = 113.1 m2, -0.9 %, is by construction). The photo shows a paler crescent on one rim (probably a slumped or damaged quadrant); excluding it would shrink the diameter by about 8 %. The viewer evaluates the outline as a radial function r(theta) about the polygon centre.

### 3.4 Seabed from the WA DoT 2009 airborne lidar (primary)

The BAG (10 m point grid, MGA94 zone 50, SW cell centre E361415 N6305610) was read once (stage 1, `build_3d_lidar.py`) and resampled bilinearly into the model frame on a 5 m grid, x = -150 ... +150 m, y = -40 ... +200 m (61 x 49 nodes):

```
z_AHD(x, y) = bilinear( grid, E1^-1 (x, y) )                                       (E8)
```

In the surf zone (y about -15 ... 35 m) there is no lidar return; 286 of 2989 nodes (9.6 %) are filled with the alongshore median profile P(y) (linear across the gap) plus a smoothed per-column offset o(x):

```
z_fill(x, y) = P(y) + o(x),   o(x) = 5-column moving average of median_y[ z(x, y) - P(y) ],  -40 <= y <= 80 m      (E9)
```

The profile statistics (median, 10th and 90th percentile over |x| <= 100 m, native sampling, 2.5 m in y) give, in m AHD: y = 20 m -1.10, 30 m -2.08, 37.5 m -2.58, 40 m -2.69, 45 m -2.97, 50 m -3.20, 60 m -3.62, 100 m -5.11, 150 m -7.12, 200 m -8.40. The mean slope for y = 30-100 m is 0.0409 (1:24.5), with no bar or trough within 200 m. The MLLW line (-0.2 m AHD) lies at y = 4.1 m, the LAT line (-0.6 m AHD) at 13.9 m and the MSL line at 2.4 m. The viewer meshes the 5 m grid; filled nodes are tinted. Contours (every 1 m AHD) are drawn from the filled grid.

The 12 m reef covers 1-2 native cells, so the seabed beneath it is a sloping plane, not resolved relief (A7). The survey is 10 years older than the installation (A8).

### 3.5 Reef surface (spherical-cap stand-in)

No cross-section of the installed bladder is published; the sources say "dome" (ABC 2019b), "a very subtle, flattened dome with a steeply angled back" (The Tradie Magazine 2019, seen in search text only), and, for the first bladder, "a bit of a skateboard ramp type thing" (Kennedy 2021). Default surface (A5): a symmetric spherical cap of base radius a = 6.0 m and height H (default 2.0 m, range 1.6-2.0 m, both design figures reported before the install). With R_s the sphere radius and t = r / r_rim(theta) in [0, 1] the normalised radial distance (so that the base follows the traced outline):

```
R_s = (a^2 + H^2) / (2 H)                                  H = 2.0 m: 10.00 m, H = 1.6 m: 12.05 m          (E10)
cap(t) = sqrt( R_s^2 - (a t)^2 ) - (R_s - H)                                                                       (E11)
z_surface(x, y) = z_bed(x, y) + 0.03 + cap(t)             (the cap follows the sloping bed; 0.03 m seats it)       (E12)
V = pi H (3 a^2 + H^2) / 6                                 H = 2.0 m: 117.3 m3, H = 1.6 m: 92.6 m3     (E13)
rim angle  theta_rim = asin(a / R_s)                       H = 2.0 m: 36.9 deg, H = 1.6 m: 29.9 deg  (E14)
```

An optional ramp asymmetry A (0-0.6) displaces the apex towards a chosen true bearing (steeper on that side); no source says which side was steep, so the default is symmetric. No fill, valves, hoses, anchors or the tear are drawn (A12). The default centre is y = 37.5 m (`shape.json`); the viewer presets 30, 37.5, 45, 49.1 m (Tracks: "approximately 45 metres off the low tide mark", i.e. 4.1 + 45) and 50 m (SurferToday 2019).

Crest depth below low tide for the centre of the cap (E7, seabed from E8), by position and height (positive = below the plane):

| reef centre y (m) | seabed (m AHD) | crest H = 1.6 m: below MLLW / LAT (m) | crest H = 2.0 m: below MLLW / LAT (m) |
|---|---|---|---|
| 30 | -2.08 | 0.28 / -0.12 | -0.12 / -0.52 |
| 37.5 | -2.58 | 0.78 / 0.38 | 0.38 / -0.02 |
| 45 | -2.97 | 1.17 / 0.77 | 0.77 / 0.37 |
| 49 | -3.16 | 1.36 / 0.96 | 0.96 / 0.56 |
| 50 | -3.20 | 1.40 / 1.00 | 1.00 / 0.60 |

### 3.6 Navionics (Garmin Marine Maps) as an independent seabed check

*Access.* webapp.navionics.com redirects to Garmin's Marine Maps viewer (https://maps.garmin.com/en-US/marine/). In my own headless Chrome (a fresh temporary profile and a random free DevTools port, never the shared browser pane; the script `src/navionics/capture_navionics.py` terminates only its own process tree) the page loaded with no login, CAPTCHA or consent dialog; nothing was accepted or bypassed. The page's own `key` (a geohash of the site) and Leaflet `setView` centred the map on -33.3276, 115.6284 at zoom 18 (the maximum) and 17, with Chart type = SonarChart Maps (or Nautical Charts), Depth units = Meters, Seabed areas = Hide, Shallow shading 1 m (the metres default). The app states **no depth datum and no contour interval**. Screenshots (private research copies, "Not to be used for navigation") were analysed offline; they were re-captured after a port-isolation notice and are byte-identical.

*Scale and geometry.* Web-Mercator: `res = 156543.034 cos(lat) / 2^zoom / dpr` = 0.2495 m per pixel at zoom 18 with device pixel ratio 2. A model point maps to the image through the true bearings of the model axes (E3).

*Counting.* 9 shore-normal transects (alongshore offsets -120 ... +120 m, step 30 m) run from the site point along +y. Along each, band boundaries (green drying area, dark blue, light blue, white) and thin dark contour lines were located (runs closer than 2.5 m merged because depth digits cross some lines). Index n = 0 is the green/blue boundary (the 0 m contour), n = 1 the dark/light blue boundary, n = 2 the light blue/white boundary (the 1 m shallow-shading limit), n >= 3 the thin lines. The interval 0.5 m is inferred and checked against the printed labels (1, 1.5, 2, 3, 3.5, 4, 4.5, 5 ... 8.5 on successive lines); every transect has 17-18 lines, monotonic and mutually consistent. The Nautical Charts layer shows contours 0 / 2 / 5 / 10 m and spot soundings, and agrees with the SonarChart lines (2 m at s = 3.1 m and 5 m at 75.1 m from the site on the main transect, against 2.1 and 77.2 m in SonarChart).

*Datum test.* For the n-th line the depth is d_n = 0.5 n m below the unknown datum D, so the lidar elevation there must equal D - d_n (E5). For a candidate datum D_c the misfit is the RMS of z_lidar(y_n) - (D_c - d_n) over the lines with valid lidar (y >= 30 m, inside the 300 x 240 m grid, not gap-filled); the free-fit datum is the mean of z_lidar + d_n:

| candidate datum | z (m AHD) | RMS, 9 transects (n=111) | bias lidar - Navionics | RMS, main transect (n=12) |
|---|---|---|---|---|
| LAT | -0.60 | 0.32 | -0.24 | 0.35 |
| LAT (DoT index) | -0.57 | 0.34 | -0.27 | 0.38 |
| MLLW | -0.20 | 0.67 | -0.64 | 0.73 |
| MHLW | +0.00 | 0.87 | -0.84 | 0.93 |
| AHD | +0.00 | 0.87 | -0.84 | 0.93 |
| MSL | +0.10 | 0.96 | -0.94 | 1.03 |

The free-fit datum is -0.84 m AHD (sd 0.20 m over lines; standard error 0.019 m if the lines were independent, which they are not). **Result: the Navionics depths are below LAT** (the Australian chart datum); MSL and AHD are rejected (RMS 0.87-0.96 m), MLLW is disfavoured (RMS 0.67 m, twice that of LAT) but not excluded by the lidar's own 0.48 m uncertainty alone. Independent anchors: the 0 m Navionics contour lies at lidar -0.69 +- 0.19 m AHD (surf-zone strip, indicative; LAT is -0.60, DoT index -0.57); the only Nautical-chart spot sounding inside the lidar grid (3.5 m at x = 106.8, y = 76.0 m, lidar -4.02 m AHD) implies -0.52 m AHD; the 2 m and 5 m Nautical contours imply -0.78 and -0.69 m AHD.

*Seabed comparison.* With depths read below LAT (A11) the mean Navionics profile (9 transects) minus the lidar median profile is:

| y (m) | Navionics on LAT (m AHD) | lidar median (m AHD) | Navionics - lidar (m) |
|---|---|---|---|
| 30 | -1.76 | -2.08 | +0.32 |
| 37.5 | -2.35 | -2.58 | +0.24 |
| 45 | -2.79 | -2.97 | +0.18 |
| 50 | -3.02 | -3.20 | +0.18 |
| 60 | -3.36 | -3.62 | +0.25 |
| 100 | -4.93 | -5.11 | +0.18 |
| 150 | -6.71 | -7.12 | +0.41 |

mean +0.25 m over y = 30-150 m (Navionics shallower than the lidar).

*Use.* **Seabed only.** The bladder was removed within days (December 2019); no closed contour or 12 m anomaly exists at the default position or at +-60 m alongshore (annotated N4), so the chart gives no crest depth or height. The viewer can switch the seabed to the Navionics check (LAT assumed): the lidar surface shifted in y by the difference between the mean Navionics profile and the lidar median profile (about +0.25 m), so the alongshore structure is kept; contours are hidden in that mode and the live cross-section shows both profiles.

### 3.7 Water

A translucent plane at the selected plane (LAT, MLLW, MHLW, MSL, MLHW, MHHW, HAT; E4). Local tides only (no other region's preset). The water is static (A13).

### 3.8 Assumptions (numbered)

| id | assumption | basis | range / effect |
|---|---|---|---|
| A1 | +y is perpendicular to the fitted 2009 0 m AHD contour; x = 12.32 deg true | contour fit, rms 8.4 m; Navionics 0 m line tilted +2.4 deg | rotates the picture; no effect on depths |
| A2 | the 2009 0 m AHD contour is the zero of "distance offshore"; the text distances (30-45, 45 from the low-tide mark, 50 m) are mapped onto y directly | site point 37.9 m from the contour; beach moves seasonally | +-10 m in y = +-0.41 m of seabed depth (slope 0.0409 x 10 m) |
| A3 | the footprint is the traced circle D = 12.0 m centred at the default y = 37.5 m, x = 0; the lateral position is irrelevant | alongshore p10-p90 of the bed +-0.15 m | none for depths |
| A4 | height H = 2.0 m default (range 1.6-2.0 m) | ABC and RWR 2 m; Tracks 1.6 m; both are pre-install design figures | volume 92.6-117.3 m3; crest +-0.2 m |
| A5 | the surface is a symmetric spherical cap on the sloping bed | text only (dome / flattened dome / ramp) | flank shape +-0.3 m locally; asymmetry slider |
| A6 | "low tide" in "about 1 m under the surface at low tide" = MLLW | no definition in the source | LAT would be 0.4 m lower |
| A7 | the seabed under the footprint is the bilinear 10 m lidar grid resampled to 5 m | 12 m reef = 1-2 cells | local relief unresolved |
| A8 | the 2009 seabed is unchanged to December 2019 | none; 10 years | sigma_change = 0.30 m (judgement) |
| A9 | Bunbury Port tidal planes hold at Back Beach; MSL = +0.1 m AHD | 3 km, same coast; DoT LAT offset 0.57 vs 0.6 m | +-0.10 m including the 0.1 m rounding |
| A10 | the lidar vertical datum is AHD; BAG uncertainty layer (0.47 m) read as 1 sigma | DoT index; the BAG's own VERT_CS tag only says "Instantaneous Water Level" | if the 0.47 m were a 95 % value, sigma_lidar is 0.24 m |
| A11 | Navionics: chart datum = LAT, contour interval 0.5 m, 0 m line = green/blue boundary | datum RMS test, labels, 1 m shading limit | MLLW is 0.4 m higher; counting +-0.5 m worst case |
| A12 | no settlement, scour, slumping of the sand fill, deflation or tear modelled; no anchors, valves or hoses drawn | none; the real bladder was partly filled, unanchored and torn | the real surface is lower and flatter in places |
| A13 | the water is static at the chosen plane | - | no waves, set-up or surge |

## 4. Validation (cross-checks performed)

| id | check | numbers | verdict |
|---|---|---|---|
| V1 | text-implied seabed vs lidar: seabed = MLLW - crest 1.0 m - H | H = 2.0: -3.20 m AHD; H = 1.6: -2.80; lidar at the default y = 37.5 m: -2.58; the lidar reaches -3.20 at y = 50.0 m and -2.80 at y = 42.0 m (with LAT as "low tide": y = 59.6 and 50.0 m) | differences at the default 0.62 m (H = 2.0) and 0.22 m (H = 1.6): about one sigma of the seabed estimate (sigma_zb = 0.61 m, section 5); the solving positions lie in the text range 30-50 m |
| V2 | Tracks "approximately 45 metres off the low tide mark" vs RWR "about 1 m under the surface at low tide" | y = 4.1 + 45 = 49.1 m, seabed -3.16 m AHD; crest below MLLW 0.96 m (H = 2.0), 1.36 m (H = 1.6) | H = 2.0 gives 0.96 m vs "about 1 m": the three text statements (1 m crest, 2 m height, 45 m from the low-tide mark) are mutually consistent (not independent of the placement) |
| V3 | tide table vs DoT survey index | LAT -0.6 (GHD) vs -0.57 (DoT) | agree to 0.03 m |
| V4 | lidar vs Navionics SonarChart (LAT-referenced) | RMS 0.32 m over 111 lines (main transect 0.35 m); mean difference +0.25 m at y = 30-150 m | agree within the lidar uncertainty (0.48 m) |
| V5 | Navionics datum candidates | LAT 0.32, MLLW 0.67, AHD 0.87, MSL 0.96 m RMS | LAT best; MSL/AHD rejected |
| V6 | Navionics Nautical vs SonarChart contours | 2 m at 3.1 vs 2.1 m, 5 m at 75.1 vs 77.2 m along the main transect | agree to about 2 m horizontally |
| V7 | footprint area | traced 112.1 m2 vs circle 113.1 m2 (-0.9 %) | by construction (scale from the text diameter) |
| V8 | sand mass vs cap volume (own arithmetic; dry bulk 1.6, saturated 2.0 t/m3 for beach sand, assumption) | see table below | 140-150 t is physically credible; a mostly sand-filled bladder |
| V9 | orientation: Navionics 0 m line vs the fitted 2009 0 m AHD contour | tilt +2.4 deg, spread of the 2 m line across transects 3.2 m, of the 5 m line 4.4 m | about the contour scatter (+-2 deg) plus the 10-year gap |
| V10 | georegistration of the lidar | the -2 and -3 m lidar contours lie under the surf-zone foam on the 2025 Esri image (annotated `lidar_contours_on_satellite.png`); the 0 m AHD contour falls at the MSL waterline | qualitative support |
| V11 | independent chronology (section 2.1) | every dated 2019 report (ABC, Tracks, RWR, The Inertia, SurferToday, the forum observer) places the install in December 2019; the developer's "2018" is contradicted | resolved |

Sand mass versus cap volume (V8; the settled sand volume is the mass divided by the bulk density; at 1.6 t/m3 dry and 2.0 t/m3 saturated):

| sand mass | settled volume (1.6-2.0 t/m3) | share of cap, H = 2.0 m (117.3 m3) | share of cap, H = 1.6 m (92.6 m3) |
|---|---|---|---|
| 140 t | 70-88 m3 | 60-75 % | 76-94 % |
| 150 t | 75-94 m3 | 64-80 % | 81-101 % |

At 150 t and dry bulk density the sand alone would just fill a 1.6 m cap (101 %), so either the density is higher, the dome was taller, or the round number includes water; the 7 % gap between 140 and 150 t is smaller than the density uncertainty (about 25 %) and changes no model input. The mean load of 150 t on the 113.1 m2 footprint is 1.33 t/m2 (about 13 kPa); not used by the model.

## 5. Uncertainty

Per input (1-sigma-like ranges, not statistical intervals; where only text exists I state my judgement):

| input | uncertainty | basis |
|---|---|---|
| outline | +-0.4 m outline reading; size from the text, not measured | `shape.json` verification |
| centre offshore, y | uniform over 30-50 m: sigma_y = 5.8 m | text range (RWR 30-45, Tracks 45 from the low-tide mark, SurferToday 50) |
| lidar seabed | sigma_lidar = 0.48 m | BAG uncertainty layer (A10) |
| seabed change 2009-2019 | sigma_change = 0.30 m | judgement (A8) |
| tide planes | sigma_tide = 0.10 m | port-to-beach transfer and 0.1 m rounding (A9) |
| height H | uniform over 1.6-2.0 m: sigma_H = 0.115 m | text (A4) |
| crest depth in the text | sigma_text = 0.30 m | "about 1m" |

**Propagation** (independent errors added in quadrature):

```
seabed under the reef   sigma_zb^2 = sigma_lidar^2 + (s sigma_y)^2 + sigma_change^2            s = 0.0409  ->  sigma_zb = 0.61 m   ((s sigma_y) = 0.24 m)    (E15)
crest elevation         z_c = z_b + H        sigma_zc^2 = sigma_zb^2 + sigma_H^2               ->  sigma_zc = 0.62 m                                                      (E16)
crest depth below MLLW  d_c = MLLW - z_c     sigma_dc^2 = sigma_zc^2 + sigma_tide^2            ->  sigma_dc = 0.63 m   (below LAT: the same, 0.63 m)           (E17)
reef height             H itself: 0.115 m (range 1.6-2.0 m); there is no as-installed measurement
```

A Monte Carlo check (40000 draws: y uniform 30-50 m, H uniform 1.6-2.0 m, seabed and tide errors Gaussian as above) gives a crest depth below MLLW of 0.69 m with sd 0.66 m (5th-95th percentile -0.41 to 1.78 m); 32 % of draws are at least as deep as the text's 1.0 m. Weighting the draws by the text ("about 1 m", sigma 0.30 m) puts the reef centre at y = 41.2 +- 5.4 m (the viewer's "set offshore so crest = 1 m under MLLW" button solves the same condition). At the default y = 37.5 m, H = 2.0 m the crest is 0.38 m below MLLW, which is 0.9 standard deviations shallower than the text's 1.0 m (combined sigma of E17 and the text): consistent.

So the crest is 0.38 m (H = 2.0) to 0.78 m (H = 1.6) below MLLW at the default position, with sigma_dc = 0.63 m. Below LAT the crest is -0.02 m (H = 2.0: the cap just reaches LAT) to 0.38 m (H = 1.6).

**Vertical exaggeration** VE multiplies every z (water, seabed, reef) and leaves x and y unchanged: tan(angle_apparent) = VE tan(angle_true); at VE = 5 the 1:24.5 bed looks like 1:4.9 and the 2.0 m cap looks 10.0 m high, with its rim angle 36.9 deg steepening to 75.1 deg. Camera angles read for photo alignment are only valid at VE = 1; the viewer forces VE = 1 in photo-match mode.

## 6. Confidence

**MEDIUM.** Rubric used (my extension of the plan-shape rubric in `SHAPE_SPEC.md`, which covers only the outline): *high* = built-state footprint from a survey or georeferenced image, crest and seabed from surveys at the site and mutually consistent within 0.3 m, position known to better than 10 m, a measured as-built surface; *medium* = all vertical inputs sourced and consistent within 0.5 m, with at most one of (the surface shape is assumed, the footprint is a design, position known only to +-50 m); *low* = two or more of those, or vertical uncertainty at least half the reef height. Against it: the seabed is sourced (lidar) and independently supported (Navionics, RMS 0.32 m below LAT); the tides are sourced and cross-checked (0.03 m); the text-implied seabed and the lidar agree to 0.22-0.62 m at the default position and exactly at y = 42.0-50.0 m, inside the text range; the footprint is a verified outline from a photograph of the installed bladder (plan confidence medium); the offshore position is known to +-10 m (sigma_y 5.8 m). The one assumed element is the surface shape (A5), which makes it MEDIUM rather than HIGH; the height (1.6-2.0 m) and crest depth are text-only and the vertical uncertainty of the crest depth (0.63 m) is below half the reef height (0.8-1.0 m) so it is not LOW. Two cautions keep it from being stronger: the survey is 10 years older than the install and its cells cannot resolve the footprint, and the real bladder was partly filled, unanchored and torn, so the cap drawn is a stand-in for a shape nobody measured. The *plan* confidence (medium) is separate from this one.

## 7. Limitations and unknowns

| id | unknown | how it could bias the model | what would resolve it | Lior could supply |
|---|---|---|---|---|
| L1 | the as-installed surface (height, profile, which flank was steep, fill level, the torn quadrant) | the cap may be taller/flatter than the real bladder by 0.3 m or more; "skateboard ramp" asymmetry | Waveco/Bottegal installation photos or dive survey, City of Bunbury incident records | partly (REQUESTS C1-C2) |
| L2 | the true position (lat/lon, distance from the waterline at the install tide) | +-10 m offshore = +-0.41 m of seabed depth and of crest depth below MLLW | Google Earth Pro historical imagery of December 2019 (probably none exists) | yes (REQUESTS A1-A3) |
| L3 | seabed change since 2009 (10 years, 2019 conditions) | sigma_change = 0.30 m assumed | a newer survey: WA DoT, Navionics app readings at listed points | yes (REQUESTS B1-B7) |
| L4 | Navionics datum, contour interval and tide correction (inferred) | MLLW vs LAT 0.4 m; counting +-0.5 m | the app's settings and readings at listed points | yes (REQUESTS B6-B8) |
| L5 | the lidar vertical uncertainty type (1-sigma or 95 %) and the BAG's own datum label | sigma_lidar 0.24-0.48 m | the DoT survey report | no |
| L6 | "low tide" in the crest-depth text (MLLW or LAT) | 0.4 m in crest depth | RWR/Waveco design document | no |
| L7 | tide planes at Back Beach vs the port gauge; no sea-level trend or surge | +-0.1 m | a local tide table | no |
| L8 | the surf-zone strip (y about -15 to 35 m): no lidar return, gap-filled | +-0.3 m there (not at the reef if it is beyond y = 35 m) | a newer lidar or sonar line | partly |
| L9 | scour, settlement, slumping of the sand fill, deflation not modelled | the real bladder rested on a slumping sand mass | monitoring data (none; the planned UWA study never started) | no |
| L10 | the mass of the fill (140 vs 150 t, developer-only) | none on the geometry | an independent weighing (none) | no |
| L11 | 2D drone photo has no scale bar: 12 m is the text value | outline scale +-7 % | a second photo with a scale | no |

## 8. References

* ABC News (2019a). 'World-first' inflatable surf reef to be installed at beach in Western Australia, 13 June 2019. https://www.abc.net.au/news/2019-06-13/world-first-artificial-surf-reef-to-be-installed-at-bunbury/11204280. Accessed 2026-09-24. (c) ABC.
* ABC News (2019b). Bunbury's Back Beach surfers deflated as artificial reef, Airwave, tears during installation, 16-17 December 2019. https://www.abc.net.au/news/2019-12-16/word-first-surf-reef-tears-during-installation/11803228. Accessed 2026-09-24. (c) ABC.
* ABC listen (2022). Meet the surfer who says Bunbury can have world class waves. South West WA Breakfast, 7 October 2022 (program summary text; audio not heard). https://www.abc.net.au/listen/programs/southwestwa-breakfast/bunbury-waves/101511922. Accessed 2026-10-05.
* Bunbury Mail (2022). Airwave founder Troy Bottegal moves towards making Bunbury ..., 22 March 2022 (story 7667604). https://www.bunburymail.com.au/story/7667604/bunbury-still-set-to-become-surfing-destination/. Accessed 2026-09-24.
* Department of Defence (2018). Tidal planes for the Port of Bunbury; cited in GHD (2021), not accessed directly.
* Esri (2025). World Imagery, Back Beach tile of 30 August 2025. Esri, Maxar and contributors; private research copy, rights not cleared.
* GHD (2021). *Tidal Inundation Monitoring and Modelling Report*, Appendix B of the Southern Ports Authority Turkey Point Access Road approvals, Table 1. https://www.epa.wa.gov.au/sites/default/files/PER_documentation2/App%20B%20-%20Tidal%20innudation%20report.pdf. Accessed 2026-10-05.
* Garmin Ltd (2026). *Navionics Marine Maps (SonarChart Maps and Nautical Charts layers)*. https://maps.garmin.com/en-US/marine/ (formerly https://webapp.navionics.com/). Accessed 2026-10-05. (c) Garmin; not for navigation.
* Kennedy, L. (2021). The Airwave Pumps Again. *Tracks Magazine*, 8 October 2021. https://tracksmag.com.au/the-airwave-pumps-again. Accessed 2026-10-05.
* PROJ contributors (2026). PROJ coordinate transformation software library (via the Python package pyproj), used for the grid convergence of MGA94 zone 50.
* Raised Water Research (2019a). Progress Update on the Bunbury Airwave, 14 October 2019. https://raisedwaterresearch.com/progress-update-on-the-bunbury-airwave/. Accessed 2026-09-24.
* Raised Water Research (2019b). The Bunbury Airwave Artificial Surf Reef Tears During Installation, 16 December 2019 (also the drone photo "Airwave from above"). https://raisedwaterresearch.com/the-bunbury-airwave-artificial-reef-tears-during-installation/. Accessed 2026-09-24.
* Raised Water Research (n.d.). *Bunbury Airwave* (spot page). https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/bunbury-airwave/. Accessed 2026-09-24.
* South Western Times (2020). Airwave back for second wave of Bunbury surf, 9 July 2020. https://www.swtimes.com.au/news/south-western-times/airwave-back-for-second-wave-of-bunbury-surf-ng-b881601738z (read via archive.org). Accessed 2026-09-24.
* Swellnet (2019-2021). Surf Forums: Airwave inflatable reef (thread 472884; anonymous posts; secondary source, used for dated observations only). https://www.swellnet.com/forums/surfing-reef-designs/472884. Accessed 2026-10-05.
* SurferToday (2018). Inflatable surf reef may be installed in Western Australia, 31 August 2018. https://www.surfertoday.com/surfing/inflatable-surf-reef-may-be-installed-in-western-australia. Accessed 2026-09-24.
* SurferToday (2019). Ripped seam puts world's first inflatable surf reef on hold, 17 December 2019. https://www.surfertoday.com/surfing/ripped-seam-puts-worlds-first-inflatable-surf-reef-on-hold. Accessed 2026-09-24 (figure seen via search text).
* The Inertia (2019). The World's First Inflatable Reef Tore During Installation, December 2019. https://www.theinertia.com/surf/airwave-worlds-first-inflatable-reef-tore-during-installation/ (read via archive.org). Accessed 2026-09-24.
* The Tradie Magazine (2019). Creating the Perfect Wave, 31 January 2019. https://www.tradiemagazine.com.au/creating-the-perfect-wave/ (page returned 403; quote seen in search text only).
* Tracks Magazine (2019a). Inflatable Artificial Reef is Ready for the Ultimate Test, 12 August 2019. https://tracksmag.com.au/inflatable-artificial-reef-is-ready-for-the-ultimate-test-529463. Accessed 2026-10-05.
* Tracks Magazine (2019b). Airwave set for live trial at Bunbury, 15 November 2019. https://tracksmag.com.au/airwave-set-for-live-trial-at-bunbury-534049. Accessed 2026-10-05.
* Waveco Pty Ltd (2025). All About Us - The Story Behind the Airwave (About page; created 2019-08-11, last modified 2025-12-22; self-published, promotional). https://www.waveco.com.au/about/. Accessed 2026-10-05.
* Western Australia Department of Transport (2009). *Two Rocks - Naturaliste Lidar 2009* (Lidar2009TRBS), BAG BU2009TRBS_Lidar.bag; and *Bathymetric survey index* (ArcGIS FeatureServer). https://dotazprdauegisextpubst01.blob.core.windows.net/transport-wa-public/bathymetry/rasters/BU2009TRBS_Lidar.bag. Accessed 2026-10-05. "Approved for Public Release; not to be used for navigation".

## 9. Reproduction

```
cd 07_scale/shapes/bunbury-airwave/3d
python build_3d.py                 # model.js, docs.js, METHODS_3D.md, computed.json, REQUESTS_FOR_LIOR.md, auto block of SOURCES_3D.md
python build_3d.py --annotations   # also re-runs nav_annotate.py and nav_figures.py (annotated/N1-N4, data/nav_transects.json)
python build_3d_lidar.py --bag <BU2009TRBS_Lidar.bag>   # stage 1 only if the lidar inputs must be re-derived (67 MB download, md5 in section 2)
python src/navionics/capture_navionics.py               # re-take the Navionics screenshots (own headless Chrome, random port, fresh profile)
```

Inputs: `../shape.json`, `../../../../02_research/reefs/bunbury-airwave.json`, `data/lidar_clip_model_frame.csv`, `data/lidar_derived.json`, `data/nav_transects.json`, `src/navionics/*.png`. Viewer: `index.html` (three.js 0.170.0 from jsDelivr; `model.js`, `docs.js` loaded as scripts, works from a local web server or file://).

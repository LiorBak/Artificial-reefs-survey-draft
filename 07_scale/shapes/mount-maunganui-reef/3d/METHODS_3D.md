# METHODS_3D - Mount Maunganui Beach Reef ("Mount Reef"), New Zealand: three-dimensional model

Built 2026-10-07 by `build_3d.py` (numbers in this note are filled in from `computed.json`, `navionics_profile.json`, `checks.json` and `../shape.json`; edit `METHODS_3D.template.md`, not the generated file).

## 1. Summary
The model shows the **as-built reef, completed mid-2008**: a delta-wing ("7") of geotextile sand-bag containers off Mount Maunganui main beach (Bay of Plenty), lofted from the verified plan outline with a crest at **-0.9 m below Chart Datum** (z = -2.03 m relative to present mean sea level) over a seabed taken from the **2026 Garmin Navionics SonarChart** and shifted to an as-built bed level of **-4.0 m CD** (selector -3.0 to -4.5). Two outline versions are built: the **default**, the -2.0 m CD contour of the 18 Jul 2013 multibeam survey (1,071 m2) with a 1:1 skirt to the bed, and the **as-built toe outline** of the ASR "Installed" survey image (2008, 1,424 m2) lofted through the contour to the crest. Later changes (apex deflation by 2013, buried base bags, removal 25 Sep to 8-9 Nov 2014) are caption and documentation only. **Confidence (3D): medium** - the outline, crest and tides are sourced; the as-built bed (decision -4.0 +-0.5 m CD) and therefore the 3 m height and the flank shape are not: every later source reads the bed 1.0-1.6 m shallower, and the stated built volume (2,800 m3) is reproduced only with a bed of -3.51 (survey outline) to -3.66 m CD (toe loft).

## 2. Data sources
Each source has an id used in the viewer's provenance table; registry ids (`mount-maunganui-reef-img-NN`) link to the saved copies and citations in `03_images/reefs/mount-maunganui-reef/`.

| id | source | what it contributed | resolution / date |
|---|---|---|---|
| img1 (img-08) | Focus Resource Management Group (2013/14). *Mount Maunganui Reef - Assessment of Management Options*, Fig 3. Report for Bay of Plenty Regional Council. https://www.boprc.govt.nz/media/558385/mount-maunganui-reef-assessment-of-management-options.pdf (accessed 2026-10-05; licence not stated) | the -2.0 m CD outline (default version), NZ-grid georeference, crest and bed text (p6, p21, p23, p28, p29) | multibeam 18 Jul 2013 (University of Waikato / Discovery Marine Ltd), 5.45 px/m |
| ctx9 (img-04) | same report, Fig 5 (second raster of the same survey with a colour bar) | hue -> depth DEM (1 m grid); crest percentiles; inner (rise) profile; evidence layer; datum test of the Navionics profile | 4.2 px/m, depth +-0.15 m |
| img3 (img-10) | ASR / Raised Water Research, "Mount Reef Installed" bathymetry. https://raisedwaterresearch.com/wp-content/uploads/2019/11/Mount-Reef-Installed.jpg | as-built toe outline (version 2); ring bed depth; built volume check (2,835-2,861 m3) | undated (after Aug 2008); datum not stated (read as MVD-53); scale +-6 % |
| img2 (img-09) | LINZ (2010-11). Bay of Plenty 0.125 m Urban Aerial Photos, tile BD37_1000_1314, CC BY 4.0 | position and size check of the outline (about 2 m) | 0.125 m, Dec 2010 - Mar 2011 |
| ctx5 (img-15/16) | Esri World Imagery (Wayback), 15 Jan 2011 | shoreline y = 0 (wet/dry sand line) | 0.3-0.6 m |
| N1 (img-19..22) | Garmin Ltd / Navionics (2026). Marine Maps viewer, SonarChart Maps and Nautical Charts, metres, zoom 17-18, Shallow-shading 0-10 m; https://maps.garmin.com/en-US/marine (centre -37.6447833, 176.2025908; accessed 2026-10-06). **Not for navigation**; private research copy, no open licence | the seabed profile outside the reef (contours 1-8 m), depth at the reef centre, one spot sounding | contour edges +-2-5 m; chart data date not shown |
| R6 | LINZ. Standard port tidal levels, Tauranga row (page updated 8 Jun 2026; accessed 2026-10-06). https://www.linz.govt.nz/guidance/marine-information/tide-prediction-guidance/standard-port-tidal-levels | HAT, MHWS, MHWN, MSL, MLWN, MLWS, LAT in m above Chart Datum | MHWS..MLWS predicted 1 Jul 2026 - 30 Jun 2027; HAT/LAT 2000-2018; MSL observed 2006-2025 |
| R5 | NIWA (2006). *MHWS level for the Bay of Plenty*. Client report HAM2006-133 (Bell, Goring et al.). https://www.boprc.govt.nz/media/32572/NIWA-091119-MHWSlevelforBOP.pdf | MVD-53 = Chart Datum + 0.9622 m (Tauranga) | |
| R7 | LINZ. Notes about the Moturiki Annual Mean Sea Level Data (16 Feb 2023). https://www.linz.govt.nz/sites/default/files/data/Moturiki_Readme.pdf | chart datum 4.103 m below BM BC84; gauge zero 1.487 m below MVD-53 | |
| R4 | Scarfe, B.E. (2008). *Oceanographic considerations for the management and protection of surfing breaks*. PhD thesis, University of Waikato. https://hdl.handle.net/10289/2668 | MVD-53 datum; 2007 crest -1.25 m MSL; scour hole 7,500 m2; reef distance 257-324 m | Jan-May 2007 (70 % complete) |
| R9 | Moores, A. (2006). Artificial surf reefs - coming to a beach near you. *New Zealand Geographic* 78. https://www.nzgeo.com/stories/artificial-surf-reefs-coming-to-a-beach-near-you/ | design: largest bags 3.5 m high x 50 m long (660 m3); design depth 4.5 m | design only |
| R3, R10, R11 | Raised Water Research Mount Maunganui page (built volume 2,800 m3); Balvert (2014), SunLive 10 Nov 2014 (removal); NZ Herald (2014, 2023) | volume check; chronology for the caption | |

## 3. Methods
### 3.1 Frame and datums
- Canonical metres (shape.json): origin on the wet/dry-sand shoreline nearest the outline centroid (lat -37.6467041, lon 176.2000765); **+x alongshore toward true bearing 316.15 deg (NW), +y offshore toward 046.15 deg (NE)**, z up. (x, y, z-up) is left-handed; the viewer maps (x, y, z) to three.js (X, Y, Z) = (x, z, y), which is right-handed and not mirrored. Compass bearing of a canonical direction (dx, dy): atan2(dx sin BX + dy sin BY, dx cos BX + dy cos BY), BX = 316.15, BY = 46.15; true north in the frame is (0.7206, 0.6934).
- Georeference chain (explicit, `mmr_lib.py`): canonical (x, y) <-> NZGD2000 / Bay of Plenty 2000 (EPSG:2106) E, N: (dE, dN) = (x sin ax + y sin oy, x cos ax + y cos oy), ax = 315.99 deg and oy = 45.99 deg grid bearings, origin E0 = 376521.85, N0 = 812664.84; grid convergence -0.161 deg.
- **z = 0 at present mean sea level**: z_MSL = z_CD - 1.13 (LINZ Tauranga MSL, 2006-2025 observations). MVD-53 (Moturiki Vertical Datum 1953, the datum of Scarfe 2008 and, assumed, of the ASR image) = CD + 0.9622 m: z_MVD = z_CD - 0.9622 and z_MSL = z_MVD - 0.168; present MSL is 0.17 m above MVD-53. MVD-53 and Chart Datum are drawn as labelled datum lines and on the tide staff.
- Levels in z_MSL: HAT +1.07, MHWS +0.83, MHWN +0.53, MSL 0, MLWN -0.56, MLWS -0.92, LAT -1.16, MVD-53 -0.168, CD -1.13. Check: spring range 1.75 = 0.83 + 0.92; HAT - MSL = 1.07 vs MSL - LAT = 1.16.

### 3.2 Reef surface (per outline version)
All reef elevations are computed on a 0.5 m grid (x -44..41, y 277..351) in m CD and converted to MSL; `mmr_model.py` (Python) and `index.html` (JavaScript) implement the same rules on the same grids.
- Inside the -2.0 m polygons: z = ZC + r(d2) (crest - ZC), ZC = -2.0 m CD, d2 = distance to the polygon edge, r = RISE(d2)/1.10 with RISE = 0 / 0.30 / 0.50 / 0.70 / 0.85 / 0.95 / 1.05 / 1.10 m at d2 = 0 / 0.5 / 1.0 / 1.5 / 2.0 / 2.5 / 3.0 / 3.5 m (linear interpolation). RISE is the shape of the 2013 DEM (median height above the -2.0 m contour vs distance inside it, west block and south arm: 0.09 / 0.24 / 0.45 / 0.65 / 0.79 / 0.88 / 0.99 / 1.01 / 1.02 m in 0.5 m bins up to 4 m), scaled to the 1.10 m between the contour and the chosen crest -0.9 m CD (A3, A4). Crest options -0.8 / -0.9 / -1.0 m CD.
- **Default version (survey outline), outside the contour:** z = max(S, ZC - dout/run), dout = distance from the -2.0 m region, run = 1 (H:V) (A7). Run is adjustable 0.25-2 in the viewer.
- **Toe version, between the toe and the contour:** z = S + (ZC - S) t, t = dT/(dT + dout), dT = distance inside the union U of the toe and the contour area to its edge (A8). Only 11 m2 of the contour area lies outside the toe, so U = the toe (1,435 m2 vs 1,424 m2).
- Reef height h = z - S >= 0 (S = local seabed); volume = sum(h) x 0.25 m2. The reef is idealised: bag-by-bag relief, the scour hole and the 2013 deflation are not modelled.

### 3.3 Seabed
- S(y) is alongshore uniform: **S(y) = Pnav(y) + (bed - Pnav(y_ref)) x clamp((y - 111.2)/(307.7 - 111.2), 0, 1)** in m CD, y_ref = 307.7 m (the reef centroid), Pnav = the Navionics profile of 3.4 (dry beach y < 0: schematic 1:15 ramp, not sourced). Landward of the 1 m contour (y < 111 m) the profile is Navionics as it is; the offset is ramped in towards the reef and kept seaward, so the seaward slope stays the Navionics slope (1:64 at 3-5 m; 1:61 in the 2013 plane fit; BoPRC 1:60-1:110) (A5, A6).
- **Bed level at the reef centre** (selector): -4.0 m CD by decision (range -3.0 to -4.5), "Navionics as it is" = -2.76 m. Evidence: BoPRC p23 (north-arm side 3.0-4.0 m deep in 2008), ASR Installed ring median -5.4 m MVD-53 = -4.46 m CD (datum assumed), consent depth 3.7-4.6 m, Moores 4.5 m (design); versus 2013 survey -2.4 (NW) to -3.3 m CD (seaward) and Navionics 2026 -2.76 m CD at the centre. BoPRC p29: the bed fluctuates by more than 1 m.

### 3.4 Navionics reading (seabed only, because the reef was removed in 2014)
- Garmin's Marine Maps viewer (maps.garmin.com/en-US/marine; the successor of webapp.navionics.com) opened without login, banner or CAPTCHA in an own headless Chrome (random debug port, fresh profile) on 2026-10-06; layers SonarChart Maps (contours every 0.5 m) and Nautical Charts (2 m and 5 m contours only); depth units metres; zoom 17 (0.946 m/px) and 18. The viewer states **no datum and no contour interval**.
- With "Shallow shading" = v m the chart paints water shallower than v blue, so the edge of the blue area is the v-m contour (checked against the printed labels). `nav_isolines.py` extracts the edges (v = 1..10, both layers, both zooms), converts pixels (map centred on the reef centroid, Web Mercator) to canonical metres, and `nav_profile.py` crosses them with five shore-normal transects x = -100, -50, 0, 50, 100 m. Median y of each contour: 1 m: y = 111, 2 m: y = 242, 3 m: y = 329, 4 m: y = 399, 5 m: y = 463, 6 m: y = 546, 7 m: y = 642, 8 m: y = 728, 9 m: y = 798 (m from the shoreline)
- Chart depth at the reef centre (y = 307.7) = -2.76 m (interpolated). The 3 m contour bulges 12-17 m seaward at x = 0..50 right at the reef (possible residual of the removed reef; not used). Zoom 18 agrees within 0-6 m. The Nautical layer gives the 2 m contour at y = 266 m and the 5 m contour at y = 489 m (coarser) and one spot sounding **2.4 m at (x 36, y 345)**, the NE tip of the footprint, where the SonarChart interpolation gives 3.22 m (recorded, not used).
- **Datum test** against the 2013 multibeam bed (12,874 one-metre cells of Fig 5 outside the reef and scour-hole zone): reading the chart as CD gives mean difference 0.21 m and RMS **0.30 m** (best), as LAT 0.32 m, as MVD-53 0.78 m, as MSL 0.95 m. The chart datum is therefore taken as CD (A5). Figures: `annotated/nav_sonar_z17_profile.png`, `nav_naut_z17_check.png`, `nav_datum_test.png`.

### 3.5 Assumptions
- **A1** State = as built, completed mid-2008 (BoPRC p6). The 2013 survey is evidence for the plan and the crest only.
- **A2** z = 0 at present MSL (CD + 1.13); MVD-53 shown as a datum line (orchestrator decision 2026-10-06).
- **A3** Crest -0.9 m CD on every bag (BoPRC: 0.8-1.0 below CD; the deflated apex bags, -2.0 to -2.4 m CD in 2013, are drawn at the same crest because their as-built height is not documented).
- **A4** The inner profile follows the 2013 DEM statistics, scaled to the crest.
- **A5** Navionics depths are relative to Chart Datum (tested, RMS 0.30 m) and the 2026 seabed outside the reef stands for the 2008 seabed shape.
- **A6** The as-built bed is the decision -4.0 m CD at the reef centre; the offset from the Navionics profile is ramped in over y = 111 to 308 m.
- **A7** Skirt (default version): the flank continues from the -2.0 m contour to the bed at 1:1 (H:V), from the 2013 transects (seaward ~1:1, landward ~1:2, west-arm north edge near vertical); see 4.3 for why the toe outline implies steeper.
- **A8** Toe version: linear loft between the toe (at the bed) and the contour.
- **A9** The dry beach (y < 0) is a 1:15 ramp for appearance only.
- **A10** The ASR "Installed" image is on MVD-53 and its scale (5.96 px/m, +-6 %) is right.

## 4. Validation
### 4.1 Registry images (STEP 0, registry ids; pending flags set false with a result line)
- **img-04 (BoPRC Fig 5, 2013 DEM):** main-bag crest -0.8 to -1.0 m CD (west block shallowest 5 % -0.80, south-arm hot spot -0.33) confirms the model crest -0.9 m CD. The 2013 bed, -2.4 (NW) to -3.3 m CD (seaward), is 0.7-1.6 m shallower than the as-built bed -4.0 (2013 vs 2008-09; flagged). Deflated apex bags (-2.0 to -2.4 m CD) are a 2013 state: caption only.
- **img-06 (apex render):** same survey, no scale: apex bags deflated 1.0-1.4 m below the main crest. The as-built apex height is unknown, so the model gives it the main crest.
- **img-10 (ASR Installed):** the crest is only bounded (legend ends at -1.8 m MVD-53 = -0.84 m CD), consistent with -0.9; the ring bed -4.46 m CD (if MVD-53) is the deep end of the evidence; its grid volume 2,835-2,861 m3 compares with the model at 4.2.
- **img-19..22 (Navionics):** seabed read, datum tested (3.4).

### 4.2 Crest and inner profile against the 2013 DEM
`annotated/mmr_model_checks.png` (panels b, c) overlays the model sections at x = -20 m (south arm) and x = +20 m (west block) on the 2013 DEM: the modelled crest plateau sits at -2.03 m MSL, within the 0.1-0.2 m relief of the DEM crest (DEM crest -1.8 to -2.2 m MSL, bag grooves down to -2.9 m); the flanks of the DEM are near vertical over the last 0.5-1 m, steeper than the 1:1 skirt of the default version and similar to the toe version.

### 4.3 Outline versions compared (crest -0.9 m CD)
| version (rule) | date | source ids | footprint at the outline (m2) | vol. at bed -3.0 | vol. at bed -3.5 | **vol. at bed -4.0 (default)** | vol. at bed -4.5 | Navionics bed as is | bed that gives 2,800 m3 | footprint at bed -4.0 (m2) |
|---|---|---|---|---|---|---|---|---|---|---|
| Multibeam survey outline (-2.0 m CD, 18 Jul 2013) (outline + 1:1 skirt) | 2013-07-18 | img1, ctx9 | 1,071 | 2,030 | 2,784 | **3,620** | 4,537 | 1,692 | -3.51 m CD | 1,788 |
| As-built toe outline (ASR 'Installed' survey image, 2008) (toe loft) | 2008 (undated image, after Aug 2008) | img3, img1 | 1,424 | 1,999 | 2,606 | **3,212** | 3,819 | 1,703 | -3.66 m CD | 1,430 |

Volumes in m3, crest -0.9 m CD, sum(h) dx dy on a 0.5 m grid (`mmr_model.py`); stated volume 2,800 m3 (BoPRC p28, Raised Water Research). The bed is the seabed level at the reef centre; "Navionics bed as is" uses the 2026 SonarChart without shifting it (-2.76 m CD at the reef centre).
- Even a vertical-flanked bag field on the -2.0 m outline holds 2,892 m3 at a bed of -4.0 m CD (volume above the contour 750 m3 + 1,071 m2 x 2.0 m), more than the 2,800 m3 stated: the stated 2,800 m3 and the -2.0 m outline are compatible only with a bed shallower than about -3.91 m CD even with vertical flanks (the extreme case), and with sloping flanks only with about -3.5 to -3.7 m CD (1:1 skirt -3.51, toe loft -3.66).
- The 1:1 skirt gives a footprint at the bed of 1,788 m2 at bed -4.0, larger than the as-built toe outline (1,424 m2). A skirt run of 0.5 reproduces the toe area (1,439 m2) and, at bed -4.0, the toe-loft volume (3,245 vs 3,212 m3). The toe lies a median 0.56 m (75 % 1.12 m, 90 % 2.83 m) outside the -2.0 m contour, i.e. the as-built flanks were steeper than 1:1. The default 1:1 follows the orchestrator's decision; the viewer's "Skirt run" slider shows the alternatives.
- **Volume finding:** at the decided bed of -4.0 m CD the loft gives 3,212 m3 (toe version, 15 % above the stated 2,800 m3) and 3,620 m3 (survey outline with the 1:1 skirt, 29 %). The stated volume is reproduced at a bed of -3.66 m CD (toe) and -3.51 m CD (survey, 1:1). All post-2008 evidence is shallower (2013 survey -2.4 to -3.3; Navionics -2.76), so a bed of about -3.6 m CD is more consistent with the volume than -4.0.
- Volume sensitivity: +-0.5 m of bed moves the toe-loft volume by +-607 m3 (+-19 %); crest -0.8 / -1.0 changes it by +68 / -68 m3.

### 4.4 Navionics versus the 2013 survey (y bands, cells outside the reef zone, m CD)
| y band (m from shoreline) | cells | 2013 multibeam median (m CD) | Navionics 2026 (m CD) | Navionics minus 2013 (m) |
|---|---|---|---|---|
| 250 to 275 | 1717 | -2.47 | -2.28 | +0.19 |
| 275 to 300 | 1691 | -2.21 | -2.52 | -0.31 |
| 300 to 325 | 2092 | -2.40 | -2.82 | -0.42 |
| 325 to 350 | 2777 | -2.85 | -3.13 | -0.28 |
| 350 to 375 | 3276 | -3.28 | -3.47 | -0.19 |
| 375 to 400 | 1320 | -3.62 | -3.74 | -0.12 |

## 5. Uncertainty
| input | range | effect |
|---|---|---|
| crest | -0.9 +-0.1 m CD (0.8-1.0 below CD) | crest z_MSL = -2.03 +-0.1 m; below LAT 0.87 +-0.1 m; below MLWS 1.11 +-0.1 m |
| MSL offset | +-0.03 m (LINZ MSL 2006-2025); MVD-53 differs by 0.17 m | all z shift together |
| bed at the reef | -4.0 +-0.5 m CD (range -3.0 to -4.5; 2013 -2.4 to -3.3) | reef height H = crest - bed = 3.1 m, sigma_H = sqrt(sigma_crest^2 + sigma_bed^2) = sqrt(0.1^2 + 0.5^2) = 0.51 m; volume +-607 m3 |
| flank run | 0.25-2 (default 1) | survey-version volume 3,049 to 4,327 m3 at bed -4.0 |
| plan outline | +-1-2 m position; lower-bound definition | footprint 1,071 to 1,424 m2 (toe) to 1,723 m2 (aerial dark mass) |
| Navionics profile | contour +-2-5 m; datum +-0.3 m | seabed away from the reef only; at the reef the bed is the selector value |

Vertical exaggeration (1-5x, always shown on screen) stretches heights only: slopes look 1-5x steeper, the plan and the photo-match mode (forced to 1x) are not affected.

## 6. Confidence
**Medium.** Against the rubric: plan = sourced (verified outline, medium), crest = sourced (BoPRC text and two survey figures agree to 0.1 m), tides = sourced (LINZ primary values), seabed shape = sourced (Navionics, datum tested) but dated 2026; reef height, bed level and flank shape = estimated, with an unresolved 1.0-1.6 m disagreement between the decided as-built bed and every later measurement, and a +15 to +29 % volume mismatch at that bed. Not high because the height - the quantity a surfer cares about - rests on a decision rather than a measurement; not low because the footprint, crest and datum are individually well supported.

## 7. Limitations and unknowns
- The 2008-09 seabed is not known at the reef (the Installed image shows it but its datum is unstated; the 2013 and 2026 sources are shallower). **Lior could supply:** Mead, Black & Moores (2007) or Mead (2011) with an as-built plan or section, or the datum of the ASR image (see `REQUESTS_FOR_LIOR.md`).
- No section drawing exists; the flank shape is an assumption (steeper than 1:1 is likely); the inner profile is a smooth shape (bags had rounded, grooved tops).
- The scour hole (to -4.9 m CD in 2013, -6.4 m CD in 2008-09, 7,500 m2) landward in the V is not modelled; the seabed is alongshore uniform.
- Apex bags are drawn intact at the main crest; the buried base bags of the north arm are in the toe version only.
- Navionics SonarChart is crowd-sourced and not for navigation; its date is unknown; the viewer states no datum.
- Google Earth historical imagery 2008-2010 (if the reef is visible) could confirm the as-built footprint; Navionics app depth reads at the reef centre and the 2.4 m sounding would check the web viewer.

## 8. References
- BoPRC / Focus Resource Management Group (2013/14). *Mount Maunganui Reef - Assessment of Management Options*. Bay of Plenty Regional Council. https://www.boprc.govt.nz/media/558385/mount-maunganui-reef-assessment-of-management-options.pdf
- Garmin Ltd / Navionics (2026). *Marine Maps viewer (SonarChart, Nautical Charts)*. https://maps.garmin.com/en-US/marine (accessed 2026-10-06; not for navigation).
- LINZ (2010-11). *Bay of Plenty 0.125 m Urban Aerial Photos (2010-2011)*, CC BY 4.0.
- LINZ (2026). *Standard port tidal levels*. https://www.linz.govt.nz/guidance/marine-information/tide-prediction-guidance/standard-port-tidal-levels (accessed 2026-10-06).
- LINZ (2023). *Notes about the Moturiki Annual Mean Sea Level Data*. https://www.linz.govt.nz/sites/default/files/data/Moturiki_Readme.pdf
- Moores, A. (2006). Artificial surf reefs - coming to a beach near you. *New Zealand Geographic* 78.
- NIWA (2006). *MHWS level for the Bay of Plenty*. Client report HAM2006-133.
- Raised Water Research. *Mount Maunganui artificial reef* (ASR "Installed" image). https://raisedwaterresearch.com/spot/artificial-reef/new-zealand/north-island/mount-maunganui/
- Scarfe, B.E. (2008). *Oceanographic considerations for the management and protection of surfing breaks*. PhD thesis, University of Waikato. https://hdl.handle.net/10289/2668
- Balvert, L. (2014). Time called on artificial reef. *SunLive*, 10 Nov 2014. https://www.sunlive.co.nz/news/86837-time-called-on-artificial-reef.html
- NZ Herald (2014). NZ's first artificial surf reef wiped out; Bay of Plenty Times (2023). Artificial reef washes ashore at Mount Maunganui.

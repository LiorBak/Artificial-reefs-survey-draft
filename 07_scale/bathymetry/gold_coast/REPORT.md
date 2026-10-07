# REPORT - Nearshore depth evidence for Palm Beach Reef and Narrowneck Reef (Gold Coast, Queensland)

Run date 2026-10-06. Work folder `07_scale\bathymetry\gold_coast\`. All access dates 2026-10-06. All image copies are private research copies (reuse rights to be checked before any public release). Nothing larger than 6.3 MB was downloaded; the 4.1 GB DTM was not.

## 1. Answers (rule first, evidence after)

**Q1. Does the City of Gold Coast DTM contain underwater depths at the two reefs? NO.**
Neither reef, nor any open-coast seabed seaward of the beach, has a cell in the DTM. Its "bathymetry in certain areas" is the estuaries, canals and the Broadwater. Four independent lines of evidence (section 2): (a) the City's own wording; (b) the 104-row source table and 65-step lineage of the DTM's metadata raster, which name no ocean survey; (c) that metadata raster has no cell at either reef (block row 370/col 238 at Palm Beach, row 265/col 210 at Narrowneck; data blocks end at the beach); (d) the City's contour layers have minimum elevation 0 m AHD at both reefs and all 226 negative contours lie in inland waterways. The DTM cannot replace the Navionics seabed at Palm Beach (answers REQUESTS_FOR_LIOR item C2 with "no").

**Q2. Is there any published or accessible nearshore depth measurement at or around each reef, with its datum? Yes, but only as design levels, text values and figure labels. No surveyed point cloud, grid or profile is public.**

| reef | what exists in the open literature | datum | where |
|---|---|---|---|
| Palm Beach | crest -1.5 m (concept: "-1.5 m AHD"; as built: "1.5 m below mean sea level" / "below the average water level at its highest point") | AHD or MSL (not distinguished; differ by 0.12 m at the Seaway) | Mortensen et al. 2015 p.4; Prenzler et al. 2022 p.1; City brochure 2020 pp.8-9 |
| Palm Beach | pre-reef seabed contours 1.5-13.5 m at 0.5 m interval (concept site, City survey before 2014); concept toe depths 11.4 m (offshore), 6.6 m (nearshore) | not stated (AHD assumed; tested in 5.2) | Mortensen et al. 2015 Fig 6, Table 2 |
| Palm Beach | natural-reef buoy depths 11.33, 11.29, 11.75, 23.80 m at four points 500-900 m off the beach; natural reef 10-16 m (seaward edge), 5-9 m (shore edge) | not stated | Daniels et al. 2022 Table 1, p.2 |
| Narrowneck | revised-design (2004) crest-top contour -2.50 and side contours -3.00 ... -5.0, -6.0, -8.00; original design labels -2 to -10 | not stated in that paper (AHD in the others) | Jackson et al. 2012 Fig 2 |
| Narrowneck | crest history: -1.0 AHD (Waikato recommendation) / -0.67 AHD (Black and Mead 2001, as quoted); built -1.5 AHD (-0.5 LAT); 2001 top-up -1.0 LAT; lowered to -2.5 AHD (-1.5 LAT); measured after the 2018 renewal -2.2 AHD | AHD and LAT as stated | Jackson et al. 2007; Vieira da Silva et al. 2021 (accepted manuscript) p.5 |
| Narrowneck | seabed around the reef from ten 2018-2020 surveys: inner edge -4/-5, reef body -6 to -8, seaward -9/-10 (read by eye); design reef between the -2 m and -10.4 m AHD contours | AHD (text) | Vieira da Silva et al. 2021 Fig 3, pp.5, 7 |

**Narrowneck renewal planform (June 2018).** The built renewed reef is the AMENDED shape with minor changes to the 2004 planform. The City states the new container locations "were influenced by physical modelling" at the Queensland Government Hydraulics Laboratory, "with some minor changes made to the shape of the renewed reef" (City of Gold Coast 2020, archived page). The only quantitative description of the two options (Option 2 further seaward, slight realignment, about 20 m seaward shift of the crest line) comes from search-engine summaries of Corbett et al. (2023), which could not be opened: treat the 20 m as unverified (6.2).

**Narrowneck crest level.** "Designed -0.67 m AHD, adopted -1.5 m AHD" is verified as a quotation in Vieira da Silva et al. (2021, AM p.5, citing Black and Mead 2001 and Jackson et al. 2007), but it is the history, not the renewed state: the crest was later lowered to a target of RL -2.5 m AHD (= -1.5 m LAT) and **the multibeam survey after the 2018 renewal gives -2.2 m AHD**. Use -2.2 m AHD for the renewed reef (6.3). Jackson et al. (2007) do not contain -0.67; they give -1.0 m AHD as the University of Waikato recommendation.

## 2. Q1 - the City of Gold Coast DTM

### 2.1 What the City says
City of Gold Coast (2024), data.gov.au "Gold Coast DTM" (created 2020-10-12, modified 2024-05-13, CC BY 2.5 AU): "Digital Terrain Model of the Gold Coast LGA, including bathymetry in certain areas. This dataset has been created from multiple data sources and surveys, details of which can be found in the associated metadata dataset - DTM Metadata." Disclaimer: DEM accuracy "can differ by at least 15 cm". The dataset JSON-LD lists the DTM (4,141,282,150 bytes; NOT downloaded) and "Digital Elevation Terrain (DTM) Metadata" (6,257,930 bytes, a separate small City dataset; downloaded to %TEMP%). The data.gov.au page states no datum; the geodatabase raster definition carries GDA94 MGA zone 56 with vertical CS AHD (EPSG 5711).

### 2.2 The metadata geodatabase
`DTM_Metadata.gdb` holds one raster `DTM_Metadata_Feb_2024_1m` (1 m cells, 128 x 128 tiles, origin 515775, 6938225, EPSG:28356) whose value is an ID into a 104-row value attribute table (model area, survey type, section interval, date, files). pyogrio cannot open the .gdb folder here (permission error) but opens single .gdbtable files, so the VAT, the tile table (zlib uint8 tiles) and the item table (raster definition + lineage XML) were read directly. Evidence copies: `q1_dtm_evidence\`.
- Sources named: aerial laser scans (value 5 "Lidar 2022", 2022-04-22, 30 ppm, +/-150 mm; value 9 "Lidar 2015", +/-50 mm); value 100 "Bathymetric Lidar 2014" (Aug 2014, 2 ppm, 82.8 million 1 m cells; lineage name "Broadwater_2014_Lidar_100", i.e. the Broadwater); Broadwater multi-scan soundings 2011; Jumpinpin lidar/sections 2005; creek, river and canal cross-sections (Nerang, Coomera, Currumbin, Tallebudgera, Pimpama, Logan-Albert ...) 1998-2023. **No row names the open coast, a beach, a reef, a nearshore or an ocean hydrographic survey.**
- Lineage, 65 steps: ExtractByMask to clip polygon `Greater_GCCC1`, then mosaics of ALS_2022_Base_5, Broadwater_2014_Lidar_100, ALS_2015_Cane_9 and the estuary/canal rasters.
- Georeferencing: x = 515775 + 128 col, y = 6938225 - 128 row (from the raster definition); reproduces the Seaway notch and Tallebudgera estuary in a block overview and puts the City's 0 m contour along the beach crest and canal edges in the overlay figures.

### 2.3 Coverage at the two reefs (128 m tile grid)

| site (WGS84) | MGA56 (E, N) | block | result |
|---|---|---|---|
| Palm Beach Reef centre (-28.107334, 153.470913) | 546256, 6890818 | row 370, col 238 | **absent**; last data block in that row is col 235 (east edge x = 545,983, 273 m landward of the reef centre; mode value 0 = partly valid beach-edge block); nothing seaward |
| Narrowneck centre (-27.9866, 153.4346) | 542736, 6904206 | row 265, col 210 | **absent**; last data block col 207 (value 5 = Lidar 2022; east edge x = 542,399, 337 m landward of the council polygon centre); nothing seaward |

Figures: palm-beach-gold-coast-img-11 (`annotated\q1_palm_beach_dtm_source_coverage_on_esri.png`) and narrowneck-gold-coast-img-22 (`annotated\q1_narrowneck_dtm_source_coverage_on_esri.png`): yellow blocks have a source value, cyan outlines none; red = City 1 m contour at 0 m AHD.

### 2.4 Independent check: the City's contour service
`https://maps1.goldcoast.qld.gov.au/arcgis/rest/services/Contours/MapServer` (50, 10, 5, 1 m layers; extent x 516,000-556,000). Statistics queries only:

| window | 1 m layer min / max ELEVATION | 5 m layer min / max |
|---|---|---|
| Palm Beach, 2.8 x 2.2 km around the reef | 0 / 8 m (718 lines) | 0 / 5 |
| Narrowneck, 2.8 x 2.4 km around the reef | 0 / 9 m (697 lines) | 0 / 5 |
| strip x 544,000-556,000, y 6,884,000-6,910,000 (offshore, Seaway to Palm Beach) | 0 / 126 m | 0 / 125 |
| whole layer | -32 / 1172 m | -30 / 1170 |

All 226 negative contours of the 1 m layer (33 of the 5 m layer) are at x <= 542,156 (Nerang River, Broadwater, canals); none east of x = 543,500 anywhere. The City's ArcGIS Hub has no bathymetry, hydrographic or DEM item (only the Artificial Reef layer, already used, and the Contours and Hillshade services).

### 2.5 Limits
(1) The test uses the DTM's source map and contours, not its cells. (2) Feb 2024 is the latest raster listed (dataset modified 2024-05-13). (3) A safety-classifier refusal interrupted a first 1 m decode; not repeated in another form; the 128 m block analysis sufficed. (4) DTM vertical datum is AHD.

## 3. Datum notes and conversions (Gold Coast Seaway standard port, MSQ)

MSQ gives (a) AHD above LAT at the standard-port benchmark: **0.760 m** (MSQ 2014 "Standard port datum levels"; "applies at the standard port benchmark only and will vary at secondary locations"); (b) Seaway tidal planes above LAT, epoch 2010-2029 (MSQ 2026): MHWS 1.53, MHWN 1.24, **MSL 0.88**, MLWN 0.51, MLWS 0.22, HAT 2.03; benchmark 6.688 m above LAT (PSM 702548 in 2026, PM QGS564 in 2014).
With h = height of a level above the named datum (negative below):

```
h_AHD = h_LAT - 0.760          (MSQ 2014, Seaway)
h_MSL = h_LAT - 0.88           (MSQ 2026, epoch 2010-2029)
h_AHD = h_MSL + 0.12           (MSL lies 0.12 m above AHD at the Seaway)
ICM / Jackson et al. (2007) pairs: RL -1.5 AHD = -0.5 LAT and RL -2.5 AHD = -1.5 LAT, i.e. h_AHD = h_LAT - 1.00 (rounded; 0.24 m more than MSQ)
```

| level (as stated) | in LAT | in AHD | in MSL |
|---|---|---|---|
| Palm Beach crest "1.5 m below mean sea level" | -0.62 | -1.38 | -1.50 |
| Palm Beach crest "-1.5 m AHD" (concept) | -0.74 | -1.50 | -1.62 |
| Narrowneck target "-1.5 m LAT" converted with MSQ | -1.50 | -2.26 | -2.38 |
| Narrowneck "RL -2.5 m AHD" converted with MSQ | -1.74 | -2.50 | -2.62 |
| Narrowneck renewed crest, multibeam 2018 (-2.2 AHD) | -1.44 (MSQ) or -1.2 (ICM rule) | -2.20 | -2.32 |
| Narrowneck as-built 1999 "-1.5 AHD (-0.5 LAT)" | -0.74 (MSQ) | -1.50 | -1.62 |

Remarks. (i) At Palm Beach AHD vs MSL is 0.12 m, inside the 3D crest uncertainty (+/-0.2 m). (ii) ICM's 1.00 m and MSQ's 0.760 m differ by 0.24 m: the measured -2.2 AHD equals -1.44 LAT by MSQ (almost the -1.5 LAT target) but is 0.3 m shallower than -2.5 AHD; which is right depends on the offset the City used for its 2018 survey (ask, section 8). (iii) Tide levels vary along the coast: the Snapper Rocks row of the same MSQ table has MSL 1.09 (Seaway 0.88). Palm Beach is about 18 km from the Seaway and 10 km from Snapper Rocks; distance-weighted interpolation gives MSL - LAT of about 1.0 m (range 0.88-1.09), so its crest would be about -0.50 m LAT instead of -0.62 (estimate; MSQ has no Palm Beach row). Narrowneck (4 km from the Seaway) can use the Seaway row. (iv) The Navionics datum is not stated by the app; 5.2 supports LAT.

## 4. Q2 - survey data that exist but are not public

| item | what it is | status 2026-10-06 |
|---|---|---|
| City "Whole of Coast" hydrographic survey | 80 beach-profile transects (ETA lines) about 400 m apart, Rainbow Bay to The Spit, 2-4 surveys a year; geometry from 1965 (Delft Hydraulics Laboratory); ETA 63 Surfers Paradise, ETA 67 Narrowneck, ETA 70 Southport; data since the 1960s | internal / Griffith; not on the hub (Alvarez et al. 2023 s.2.3.1; Vieira da Silva et al. 2021b) |
| City nearshore surveys at Narrowneck | ten topo-bathymetric surveys 19 Jul 2018 - 23 Apr 2020, single-beam + RTK-GPS, 2 x 2 m grid, AHD, ETA 63-70 | only as Fig 3 of Vieira da Silva et al. (2021) |
| as-built multibeam of the two reefs | Narrowneck multibeam after 2018 (crest -2.2 AHD); Palm Beach survey "throughout construction" and certification (Hunt et al. 2022 Fig 4, qualitative) | not published; ask the City |
| Palm Beach Design Reference Report (Royal HaskoningDHV) | detailed design | not found online |
| Queensland State-wide Nearshore Bathymetry Survey | airborne bathymetric lidar, 1 m DEM from 200 m onshore to 6 km offshore, relative to AHD; Gold Coast stage one, flown from mid-July 2025; free to councils; "No decision on public availability" (Sultmann 2025) | not released; older Queensland data are "up to 40 years old" BPA surveys of uncertain accuracy; only the Sunshine Coast 2011-12 pilot is open |
| Queensland Hydrographic Charts 1802-2013 (data.qld.gov.au) | scanned historic charts, current to 2010 | lead only (portal challenged scripts); not read |
| QSpatial / Queensland Globe, AusSeabed, GCWA, MSQ surveys | no open-coast Gold Coast beach-profile, multibeam or lidar layer found | negative result |
| City Contours / DTM | none offshore | negative (section 2) |

## 5. Palm Beach Reef

### 5.1 Findings (page references)
- Crest. Mortensen et al. (2015, p.4): "The crest level was chosen to be -1.5 m AHD. This level was chosen to assure that the structure remained fully submerged during even the lowest tides, while still inducing frequent wave breaking" (concept; Fig 3: crest -1.5 m, average depth 8.7 m, footprint 21,394 m2, volume 53,319 m3). Prenzler et al. (2022, p.1): "The crest of the reef is 1.5m below mean sea level and consists of 6 to 8 tonne rocks." City of Gold Coast (2020, p.8): "160 metres long, 80 metres wide and is 1.5 metres below the average water level at its highest point", about 270 m offshore of Nineteenth Avenue; section view p.9 (palm-beach-gold-coast-img-14: core rock, armour layers, 6-8 t at the crest, 1-4 t at the toes, shoreward slope shorter than seaward, not to scale).
- Concept seabed (a different, larger structure, not built): offshore toe 560 m offshore in 11.4 m; nearshore toe 6.6 m (Table 2); offshore slope 1:12.
- Buoys (Daniels et al. 2022 Table 1; datum not stated): PBO3 11.75 m at (-28.107191, 153.473845), about 214 m seaward of the built reef's offshore toe; PBO2 11.29 m (-28.109683, 153.474469); PBO1 11.33 m; PBO4 23.80 m.
- Condition: hydrographic survey and inspections show "insignificant movement or settlement" (Prenzler et al. 2022); satellite views after 2019 still show the mound (palm-beach-gold-coast-img-15).

### 5.2 Datum test of the 3D seabed (new)
Mortensen et al. (2015) Fig 6 top (pre-reef City survey) was read along y = 3050 m (17 labels, 2.0-12.0 m; `annotated\palm_beach_mortensen2015_fig6a_profile_y3050.csv`; figure `annotated\palm_beach_mortensen2015_fig6a_depth_contours_read_along_y3050.png`) and compared with the Navionics SonarChart depths below LAT used in the Palm Beach 3D model (read-only from `3d\validation_3d.json`: mean of x = +/-150 m at y = 150 ... 450 m). Unknowns: horizontal shift s and optionally a vertical offset c; 13 labels, 3.5-11.5 m; script `tools\pb_profile_compare.py`:

| conversion applied to the chart | c fixed 0: shift, RMS | c fitted: shift, c, RMS |
|---|---|---|
| none (chart = LAT) | 284 m, 0.52 m | 335 m, +1.27 m, 0.20 m |
| AHD = LAT + 0.76 (MSQ 2014) | 316 m, **0.29 m** | 335 m, +0.51 m, 0.20 m |
| MSL = LAT + 0.88 (MSQ 2026) | 320 m, 0.26 m | 335 m, +0.39 m, 0.20 m |

Reading: a City survey of 2013-14 and a crowd-sourced chart of about 2025 agree to 0.2-0.3 m RMS over 3.5-11.5 m depth once the chart is moved from LAT to AHD/MSL (unconverted: worse, 0.52 m, or a 1.3 m offset needed). This supports "Navionics chart datum = LAT" and the MSQ offsets; AHD and MSL (0.12 m apart) cannot be told apart. With the best offset the chart bed is 0.4-0.5 m shallower than the 2013-14 bed, consistent with the 470,000 m3 nourishment of 2017 (a "final sand placement" went to the reef site, Hunt et al. 2022). Gradient between 4.5 and 8 m is 1:51 in both. The shift of 316-335 m puts the waterline of the figure's x axis near x = 330 m (2 m contour at x = 394).

### 5.3 Integration plan for the Palm Beach 3D model (3d\ folder NOT edited here)
1. **No DTM seabed.** The DTM has no Palm Beach nearshore cells (2.3). Keep the Navionics seabed; close REQUESTS C2 as "answered: no".
2. **Crest.** Keep -1.5 m MSL. Add provenance with pages: Mortensen 2015 p.4 and Fig 3 ("-1.5 m AHD", concept), Prenzler 2022 p.1, City brochure 2020 pp.8-9. State the AHD/MSL 0.12 m difference and that the crest is -0.62 m LAT (Seaway MSL) or about -0.50 m LAT (interpolated Palm Beach MSL).
3. **Seabed datum.** Cite the 0.29 m RMS cross-check (5.2) for "chart datum = LAT" and the +0.76 / +0.88 conversions. The chart bed may be about 0.5 m shallower than the pre-reef survey; no change recommended. In METHODS_3D section 7 replace "no surveyed seabed value read" by "pre-reef survey profile read from Mortensen 2015 Fig 6, datum assumed AHD".
4. **Offshore validation point.** Add PBO3 (Daniels 2022): 11.75 m at (-28.107191, 153.473845), about 214 m seaward of the offshore toe; consistent with toe about 7 m plus 214 m / 45 = 4.8 m.
5. **Surface and section.** Use the City section view (img-14) for layer logic and rock-class zones and the shoreward-steeper asymmetry; not to scale, so take no slope ratio.
6. **Camera-match candidates.** Hunt 2022 Fig 5 (img-03) and Prenzler 2022 Fig 1 (img-04, CCTV wedge and frame).
7. **Open mismatch.** Register HEIGHT_M 5 / VOLUME 33,000 still unexplained (City text: 60,000 t of rock; bulk density 1.82 t/m3 if 33,000 m3, already in validation_3d.json). Request to the City stands.

## 6. Narrowneck Reef

### 6.1 Chronology of the planform
- 1998-99 original design: two separate tapered arms ("split V" after a "conventional V" produced high seaward velocities, Jackson et al. 2007 p.3), no weir, no flared wings; 408 containers 20 m long, 3-4.5 m in diameter, 60,000 m3 (Jackson 2007; Vieira da Silva 2021), placed Aug 1999 - Dec 2000 (img-26).
- 2004 modification: submerged weir (2 containers) in the central channel and flared wings (Jackson et al. 2012 pp.3-4; Figs 2 right, 4); about 450 containers by 2007.
- 2011: GCCC survey 9 June 2011 and aerial of July 2011 (Figs 5-7); about 10 containers compromised since 2008, seaward containers partly buried.
- 2017: "Design studies - modelling of 2 reef renewal options" (Vieira da Silva 2021 Table 1); works Sep 2017 - Jun 2018 (84 containers on top of the existing footprint).
- After 2018: surveys show no settlement (City via Swellnet 2019); two yellow buoys mark a Prohibited Anchorage Area (City 2020).

### 6.2 "Previous design shape" vs "amended shape" (Corbett et al. 2023)
In decreasing weight:
1. City of Gold Coast (2020, archived 2020-08-04): "The locations of the new containers were influenced by physical modelling undertaken at the Queensland Government Hydraulics Laboratory, with some minor changes made to the shape of the renewed reef"; "84 additional mega geotextile sandbags were placed around the existing structure" over 10 months. Primary statement that the built reef is the amended shape.
2. Nettle (2017), Swellnet: the City "could confirm that data from the physical modelling informed their decision to alter the shape of the reef"; containers placed "on top of the existing reef footprint".
3. Vieira da Silva et al. (2021) Table 1: two renewal options modelled in 2017 (ICM 2017).
4. Corbett et al. (2023) abstract and captions only as reproduced by search engines (ResearchGate 403; Informit Cloudflare challenge; not bypassed): "the previous design shape and an amended shape"; Option 1 = the 2004 design with crest -2.5 m AHD (-1.5 m LAT); Option 2 "located further seaward with slight realignment", crest shifted about 20 m seaward, similar alongshore width and crest planform. **Unverified at the source.**
Conclusion: built = amended (Option 2 or a variant, "minor changes"); exact shift not established. For a tracer the consequence is small: trace the real container patches on post-June-2018 imagery; do not force the outline onto the 2004 design contours (they may be about 20 m off seaward).

### 6.3 Crest level (verified at the sources; AHD unless stated)

| stage | value | source (page) |
|---|---|---|
| Waikato recommendation | -1.0 m AHD (AHD = approximately MSL) | Jackson et al. 2007 pp.3-4 (reprint pages) |
| "initially designed" | -0.67 m AHD | Black and Mead 2001, as quoted by Vieira da Silva 2021 AM p.5 (original not opened) |
| original design (Waikato) | crest "at approximately LAT" | Jackson 2007 p.9 |
| adopted for the 1999 contract | RL -1.5 m AHD (-0.5 m LAT) | Jackson 2007 p.4; Vieira 2021 p.5 |
| 2001 top-up | -1.0 m LAT | Jackson 2007 p.9 |
| target since about 2004-07 | -1.5 m LAT = RL -2.5 m AHD ("compromise between safety and surfing"); depth over crest about 1 m, about 0.3 m at -1.0 m LAT | Jackson 2007 pp.7, 9-10 |
| 2012 summary | "1-1.5 m below low tide" | Jackson et al. 2012 p.13 |
| before the 2018 renewal | low-tide depths on the reef 2.5-2.6 m (boat operator) | Nettle 2017 |
| after the 2018 renewal, multibeam | **-2.2 m AHD** | Vieira da Silva 2021 AM p.5 |
| council asset register | TOP_REDUCED_LEVEL -2.5 (read in the Narrowneck METHOD.md) | equals the design RL -2.5 m AHD |

Verdict on the snippet: right as history, outdated for the renewed state. Raised Water Research (2019) says the renewal restored "its original designed depth of 1.5m below low tide": that conflates the -1.5 m LAT target with the 1999 contract level; do not use.

### 6.4 Depth context
Revised-design levels (Jackson 2012 Fig 2 right; `annotated\narrowneck_jackson2012_fig2_design_depth_labels_read.png`): -2.50 crest top, -3.00, -3.50, -4.00, -4.50, -5.0, -6.0, -8.00 outer limit. Seabed at the reef (Vieira da Silva 2021 Fig 3, survey 1 of 19 Jul 2018; `annotated\narrowneck_vieira2021_fig3_survey1_2018-07-19_depth_labels_read.png`): about -4/-5 m inner edge, -6 to -8 m under the reef body, -9/-10 m seaward (+/-1 m by eye; single-beam, reef blurred). Text: design reef between the -2 m AHD contour and -10.4 m AHD (Black 1999 via Vieira 2021). Scale: Jackson et al. (2007) Fig 13 has a 0-100 m bar, calibrated 4.28 px/m (0.234 m/px) in the 300 dpi crop (`annotated\narrowneck_jackson2007_fig13_scale_calibration_100m.png`); the same planform is in Jackson 2012 Fig 2 right (no scale).

### 6.5 Integration plan for the Narrowneck tracer (shape.json, METHOD.md NOT edited here)
1. **State to draw:** the renewed reef as left in June 2018 (amended shape, minor changes). Primary imagery: post-June-2018 Esri Wayback (2019-06-18 first), as already planned; qualitative checks: narrowneck-gold-coast-img-23, -24 (ICM drone photos during/after the works; no scale).
2. **Design outline as a prior, not truth:** Jackson 2012 Fig 7 (img-10) and Fig 6b (img-09), georeferenced to Esri on container patches; scale from Jackson 2007 Fig 13 (img-27). Expect the renewed outline to differ from the 2004 design by up to about 20 m seaward of the crest line (unverified).
3. **Topology:** two arms, central weir channel, flared wings (img-04, img-05). Use the 1998 split-V drawing (img-26) as history only.
4. **Checks:** containers 20 m long, 3-4.5 m in diameter; 84 added in 2018; envelope "200-350 m alongshore and 400-500 m cross-shore" (Vieira 2021 citing Jackson and Hornsey 2002); the council polygon (256 x 151 m) is a loose envelope.
5. **Levels for a later 3D stage:** crest -2.2 m AHD (measured 2018), target RL -2.5 m AHD (-1.5 m LAT), seabed -4/-5 to -8 m AHD, conversions in section 3. Quote the history in captions; do not model a second state (Lior's rule).
6. **Gemini items:** (G4) Swellnet 2017 confirmed at the original: "some of the depths at low tide on the reef are 2.5m to 2.6m"; "lowered the depth of the reef a metre prior to construction". (G1) Black and Mead 2001 not opened (only quoted). (G3) the ICM page has Narrowneck images but no planform or levels.
7. **Pending checks** are in the registry (`for_3d_check.pending`): narrowneck img-01, 02, 03, 04, 05, 08, 09, 10, 14, 23, 24, 26, 27, 31, 36.

## 7. Images saved and registered
51 images (36 Narrowneck img-01..36, 15 Palm Beach img-01..15) in `07_scale\shapes\<slug>\src\gov\` (originals, 200 dpi page renders, 300 dpi crops), `07_scale\bathymetry\gold_coast\annotated\` and `03_images\reefs\<slug>\`. Registry: `03_images\reefs\<slug>\images.json` + `IMAGES.md`; log `03_images\reefs\NEW_IMAGES_LOG.md`; provenance `SOURCES.md`. Required four: j12_p3.png = narrowneck-gold-coast-img-01 (Jackson 2012 p.3, Figs 2-3); j12_p4.png = narrowneck-gold-coast-img-02 (p.4, Figs 4-5); q1_palm_beach... = palm-beach-gold-coast-img-11; q1_narrowneck... = narrowneck-gold-coast-img-22. Annotated reads: Jackson 2012 Fig 2 labels, Mortensen 2015 Fig 6a profile (+CSV), Vieira 2021 Fig 3, Jackson 2007 Fig 13 scale. Full-size council renewal images are not archived: only 200 px thumbnails (img-32..36).

## 8. Requests for Lior
1. Open Corbett, Mulcahy, Elliott-Perkins and Hunt (2023) "Narrowneck Artificial Reef Renewal" yourself (ResearchGate or the Coasts & Ports 2023 proceedings on Informit): its figures of Renewal Options 1 and 2 would settle 6.2 (login or manual download needed; not bypassed).
2. E-mail the City (beaches@goldcoast.qld.gov.au, address on the City's page): Narrowneck 2018 renewal drawings and as-built multibeam (and the datum offset behind "-2.2 m AHD"); Palm Beach as-built certification survey and Design Reference Report; meaning of HEIGHT_M and VOLUME in the asset register.
3. Ask DETSI (Queensland) whether the Gold Coast stage of the State-wide Nearshore Bathymetry Survey (flown from July 2025, AHD) will be public.
4. Navionics readings A1-A7 of the Palm Beach REQUESTS file are unchanged.

## 9. Limitations
Figure readings are by eye (+/-0.5 to 1 m); datum assumptions stated where the source is silent; Black and Mead (2001), Corbett et al. (2023) and the ResearchGate papers not opened; the MSQ AHD offset is valid at the Seaway benchmark only; Palm Beach tide levels interpolated; Q1 relies on DTM metadata and the contour service, not on DTM cells.

## 10. References (author-year; accessed 2026-10-06; licence)
- Alvarez, F., De Lucia, L., Vieira da Silva, G. and Javernig, B. (2023) A coastal erosion risk assessment framework. Australasian Coasts & Ports 2023. Griffith Research Online http://hdl.handle.net/10072/429692. Copyright, personal use.
- City of Gold Coast (2020) Palm Beach Shoreline Project - project overview (brochure 19-TI-00753). https://www.goldcoast.qld.gov.au/files/sharedassets/public/v/1/pdfs/environment/palm-beach-shoreline-project-brochure-a4.pdf. Licence not stated.
- City of Gold Coast (2020) Narrowneck Reef Renewal (project page, archived 2020-08-04). http://web.archive.org/web/20200804025419/https://www.goldcoast.qld.gov.au/narrowneck-reef-renewal-39934.html. Licence not stated.
- City of Gold Coast (2024) Gold Coast DTM; Digital Elevation Terrain (DTM) Metadata. data.gov.au https://data.gov.au/data/dataset/digital-elevation-models-dem. CC BY 2.5 AU.
- City of Gold Coast (2026) Contours MapServer. https://maps1.goldcoast.qld.gov.au/arcgis/rest/services/Contours/MapServer. Licence not stated.
- Corbett, B.B., Mulcahy, M.G., Elliott-Perkins, Z. and Hunt, S. (2023) Narrowneck Artificial Reef Renewal. Australasian Coasts & Ports 2023. NOT OBTAINED (abstract via search engines only).
- Daniels, R., Metters, D. and Ryan, J. (2022) Wave transformation over Palm Beach reef. Coastal Engineering Proceedings 37, papers.63, doi:10.9753/icce.v37.papers.63. CC BY 4.0.
- Hunt, S., Britton, G., Messiter, D., Prenzler, P., Knight, S. and Watterson, E. (2022) Palm Beach Shoreline Project: innovative coastal management solution. Coastal Engineering Proceedings 37, management.66, doi:10.9753/icce.v37.management.66. CC BY 4.0.
- International Coastal Management (2023) Artificial reefs and nearshore nourishment on the Gold Coast: what the monitoring shows. https://www.coastalmanagement.com.au/artificial-reefs-and-nearshore-nourishment-on-the-gold-coast-real-world-results. Licence not stated.
- Jackson, A., Tomlinson, R., Corbett, B. and Strauss, D. (2012) Long term performance of a submerged coastal control structure: a case study of the Narrowneck multi-functional artificial reef. Coastal Engineering Proceedings 33, structures.54, doi:10.9753/icce.v33.structures.54. CC BY 4.0 badge on the ICCE site; no per-article statement.
- Jackson, L.A., Corbett, B., McGrath, J., Tomlinson, R. and Stuart, G. (2007) Narrowneck Reef: review of seven years of monitoring. Shore & Beach 75(4). Griffith Research Online http://hdl.handle.net/10072/17995. (c) authors; reproduced under the publisher's policy.
- Maritime Safety Queensland (2014) Standard port datum levels - height above LAT. https://www.msq.qld.gov.au/-/media/TMROnline/msqinternet/MSQFiles/Home/Tides/standardportdatumlevels2014.pdf. Licence not stated.
- Maritime Safety Queensland (2026) Semidiurnal tidal planes 2026. https://www.msq.qld.gov.au/_/media/tmronline/msqinternet/msqfiles/home/tides/tidal-planes/2026-semidiurnal-tidal-planes.pdf.
- Mortensen, S.B., Hibberd, W.J., Kaergaard, K., Kristensen, S.E., Deigaard, R. and Hunt, S. (2015) Concept design of a multipurpose submerged control structure for Palm Beach, Gold Coast Australia. Australasian Coasts & Ports 2015. https://www.dhigroup.com/upload/publications/coastsea/Mortensen_2015.pdf. Licence not stated.
- Nettle, S. (2017) Narrowneck artificial reef nears completion (updated), Swellnet 7 Nov 2017; (2019) Narrowneck renewal deemed a success, 19 Aug 2019; (2019) Palm Beach Artificial Reef is currently under construction, 23 May 2019. https://www.swellnet.com. Licence not stated.
- Prenzler, P., Hunt, S., Elliott-Perkins, Z., Hamilton, D., Messiter, D., Wharton, C. and Watterson, E. (2022) Monitoring of the Palm Beach artificial reef. Coastal Engineering Proceedings 37, structures.65, doi:10.9753/icce.v37.structures.65. CC BY 4.0.
- Queensland Government (2013, reviewed 2024) Seabed mapping; Coastal and Estuarine Risk Mitigation Program. https://www.qld.gov.au/environment/coasts-waterways/beach/studies/studies-seabed. CC BY 4.0 (site default).
- Raised Water Research (2019) Narrowneck. https://raisedwaterresearch.com/spot/artificial-reef/australia/queensland/narrowneck/. Licence not stated (secondary; conflicts with primary papers on the crest).
- Sultmann, S. (2025) State-wide Nearshore Bathymetry Survey for Improved Coastal Hazard Assessment (slides, QCoast2100 forum), Qld DETSI. https://www.qcoast2100.com.au/files/assets/qcoast2100/v/1/events/forum-9-documents/2._qcoast_forum_2025_detsi_sel_sultmann_final.pdf (read from the WebFetch-cached copy). Licence not stated.
- Vieira da Silva, G., Hamilton, D., Strauss, D., Murray, T. and Tomlinson, R. (2021a) Sediment pathways and morphodynamic response to a multi-purpose artificial reef - new insights. Coastal Engineering 171, 104027, doi:10.1016/j.coastaleng.2021.104027 (accepted manuscript, http://hdl.handle.net/10072/409362). CC BY-NC-ND 4.0.
- Vieira da Silva, G., Strauss, D., Murray, T., Tomlinson, R., Taylor, J. and Prenzler, P. (2021b) Building coastal resilience via sand backpassing. Ocean & Coastal Management (accepted manuscript, http://hdl.handle.net/10072/408348). CC BY-NC-ND 4.0.
- Black, K.P. and Mead, S.T. (2001) Design of the Gold Coast Reef: mitigating storm erosion. Journal of Coastal Research (as cited by Vieira da Silva et al. 2021a; NOT opened).

## 11. Files
`METHOD.md`, `SOURCES.md`, `annotated\` (Q1 overlays, depth-label reads, CSV), `q1_dtm_evidence\` (VAT, lineage XML, JSON-LD, contour query results, overlay script), `tools\` (`register_images.py`, `register_entries*.py`, `generate_sources.py`, `pb_profile_compare.py` + output). Images: `07_scale\shapes\narrowneck-gold-coast\src\gov\`, `07_scale\shapes\palm-beach-gold-coast\src\gov\`, `03_images\reefs\<slug>\`.

# EMODnet Bathymetry as a seabed-depth source for the reef 3D models: feasibility test and extraction for Boscombe and Borth

Run of 2026-10-06. Work folder `07_scale/bathymetry/emodnet/`. Step log in `METHOD.md`. Every number below can be regenerated with the scripts in `scripts/`. Prepared for Lior's question whether the EMODnet viewer (https://emodnet.ec.europa.eu/geoviewer/) can give seabed depths for the 3D models.

## 0. Answer first

1. **Coverage.** EMODnet Bathymetry covers European seas only.
   - Of our 13 reefs, **two are covered: Boscombe Surf Reef (UK) and the Borth coastal defence reef (Wales)**.
   - The other 11 are outside the grid: 6 Australia, 2 New Zealand, 1 USA, 1 India, 1 Mexico.
   - The REST service returns HTTP 204 (empty) at every one of their coordinates (section 5.1).
2. **What the data are.**
   - The product is the EMODnet Digital Bathymetry **DTM 2024**.
   - Depths are in metres relative to **Lowest Astronomical Tide (LAT)**. This is verified in the ISO metadata and in the ERDDAP attribute `long_name`.
   - The grid is **1/16 arc-minute**. A cell is **115.8 m (N-S) x 73.4 m (E-W) at Boscombe** and **115.8 x 70.6 m at Borth**.
   - Each cell also carries a minimum, maximum, standard deviation, sounding count, interpolation flag and a reference to its source survey.
3. **Rule for the 3D agents.** Take the datum frame (LAT) and the offshore seabed gradient only. Do **not** take crest, toe or reef-height values.
   - The cells are 1.5-2.5 times larger than the 120 x 45 m Boscombe reef. The reef outline (4,042 m2) is 48 % of one cell.
   - The reef is **not visible in the DTM** in any release 2018-2024. The cell containing the reef centre has a maximum of -4.87 m (LAT), while the model crest is +0.56 m (LAT).
4. **Boscombe.**
   - Depth at the reef centre: **-5.62 m rel. LAT**. This is the cell mean, with min -6.21, max -4.87, 12 soundings. In the model's MSL frame it is -7.08 m.
   - Source: survey **CDI 117452**, EDMO 2607 = OceanWise Limited. OceanWise is the UK lead of EMODnet Bathymetry and processes UKHO survey data.
   - Quality classes: multibeam (>100 kHz), horizontal accuracy <20 m, age class 10-30 y.
   - The survey year is not stated by any machine service. I infer about 2011-2012 (section 6.4).
   - **EMODnet minus our model seabed = -1.8 +- 0.7 m** over 7 cells (reef cell -1.39 m). EMODnet is deeper. The offset is not constant, so it is not a simple datum shift (section 6.2).
5. **Borth.**
   - The cells that contain the reef are **GEBCO 2024 interpolation, not survey data**. The centre value is -0.18 m rel. LAT, flagged "interpolated".
   - Real source cells (CDI 115084) have one sounding per cell, age class >30 y and horizontal accuracy class "unknown". They start 335 m from the defence line and give a seaward gradient of -1.1 %.
   - Nothing at the reef itself is usable.
6. **Finer data.**
   - No EMODnet high-resolution composite DTM exists at either site.
   - The nearest is **BY_CHERISH_Wales_14m (1/128 arc-min, about 14 m), 22 km north of Borth**. For Boscombe the nearest is 106 km away.
   - Finer UK data exist outside EMODnet (Channel Coastal Observatory, UK Civil Hydrography Programme, Welsh coastal monitoring). I did not retrieve them.
7. **Haifa (one line).** Covered by the same 1/16 arc-minute DTM (cells about 115.8 x 97.4 m). The cells off Haifa are interpolated (composite `JOINT_ISRAEL_NBS_QUARTMIN_GEO`, 1/4 arc-min). Real survey data (IOLR EEZ 2012 multibeam) exist only offshore, and no high-resolution DTM lies within 900 km (section 8).

## 1. Sources

All accessed 2026-10-06 unless stated.

- **Licence of the EMODnet data products: CC BY 4.0.** I verified this on the EMODnet Terms of Use page. Users must also check the licence of the individual data originators.
- The ISO record says "DO NOT USE FOR NAVIGATION". The ERDDAP licence string says the data "may be used and redistributed for free but is not intended for legal use".
- This report and the images are a **private research copy**. Reuse of the Esri basemap in the screenshots is not cleared.

| ID | Citation (author-year) | Used for |
|---|---|---|
| E1 | EMODnet Bathymetry Consortium (2024). *EMODnet Digital Bathymetry (DTM 2024)*. https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1. Sextant record cf51df64-56f9-4a99-b1aa-36b8d7b743a1, published 2024-12-31, metadata revised 2025-05-16. Read as ISO XML at https://emodnet.ec.europa.eu/geonetwork/srv/api/records/cf51df64-56f9-4a99-b1aa-36b8d7b743a1/formatters/xml | grid, resolution, vertical reference (LAT), contents (22,063 surveys and composite DTMs from 66 providers; gaps filled with GEBCO 2024 and IBCAO v4) |
| E2 | EMODnet Bathymetry Consortium (2024). *The EMODnet Grid*, ERDDAP dataset `bathymetry_dtm_2024`. https://erddap.emodnet.eu/erddap/griddap/bathymetry_dtm_2024 | cell values and per-cell statistics (primary numeric source) |
| E3 | EMODnet Bathymetry (n.d.). *EMODnet Bathymetry REST service*. https://rest.emodnet-bathymetry.eu/ | point and profile cross-check, source reference of a cell |
| E4 | EMODnet Bathymetry Consortium (n.d.). WMS / WFS / WCS. https://ows.emodnet-bathymetry.eu/ | source-reference patches, quality index, high-resolution areas, older releases |
| E5 | EMODnet Bathymetry Consortium (n.d.). *Quality Index* metadata record 6572ee07-a078-4adc-b868-fd1f7084c660 | class definitions: horizontal, vertical, age, purpose |
| E6 | EMODnet (n.d.). *Terms of use for EMODnet online services, data and data products*. https://emodnet.ec.europa.eu/en/terms-use-emodnet-online-services-data-and-data-products | licence CC BY 4.0, acknowledgement wording |
| E7 | EMODnet (n.d.). *EMODnet Map Viewer*. https://emodnet.ec.europa.eu/geoviewer/ (catalogue `config.php`, layers 14159 and 13012) | screenshots |
| O1 | OceanWise (2021). *OceanWise UK lead to latest European Bathymetry Digital Terrain Model*, 18 Jan 2021. https://www.oceanwise-global.com/oceanwise-uk-lead-to-latest-european-bathymetry-digital-terrain-model/. SeaDataNet EDMO register entry 2607 "OceanWise Limited", http://edmo.seadatanet.org/report/2607 | meaning of EDMO 2607; UKHO origin of the UK cells |
| O2 | OceanWise Limited / SeaDataNet (n.d.). CDI survey polygons, WFS `emodnet_bathymetry:polygons`. http://geo-service.maris.nl/emodnet_bathymetry/wfs | survey names near the sites |
| O3 | Joint Nature Conservation Committee and Natural England (2013). *HI 1366 2012 MCZ CHP Multibeam Survey Poole Bay* (GB100215; survey 2011-08-26 to 2012-01-04; Open Government Licence). https://emodnet.ec.europa.eu/geonetwork/srv/api/records/6d906048-5195-4f53-90d0-4d17807117b1 | candidate (unconfirmed) for the 2011-2012 survey |
| M1 | Mead, S., Blenkinsopp, C., Moores, A. and Borrero, J. (2010). Design and construction of the Boscombe multi-purpose reef. *Coastal Engineering Proceedings* 32 (ICCE 2010), 1352, Table 1 | LAT = -0.06 m ACD; design crest +0.5 m ACD |
| M2 | Rendle, E. and Davidson, M. (2012). An evaluation of the physical impact and structural integrity of a geotextile surf reef. *Coastal Engineering Proceedings* 33 (ICCE 2012), 6794, Fig. 9 | April 2011 DGPS surfaces (through the project model) |
| M3 | National Tidal and Sea Level Facility (n.d.). *Chart datum and ordnance datum*. https://ntslf.org/tides/datum. Re-read 2026-10-06: Bournemouth -1.40 m, Barmouth -2.44 m, Fishguard -2.44 m; Aberystwyth not listed | chart datum 1.40 m below ODN |
| M4 | This project (2026-10-05). Boscombe model `07_scale/shapes/boscombe-surf-reef/3d/model.js` and `METHODS_3D.md` (read only) | the model compared with |
| M5 | This project (2026). `07_scale/shapes/<slug>/shape.json` (Boscombe, Borth) | positions, frames, shore-normal bearings |
| B1 | Garmin Ltd / Navionics (2026). Marine Maps viewer, via the 33 soundings in the Boscombe `model.js` (read 2026-10-05 by the 3D agent). Not for navigation; private research copy | independent sounding check |
| B2 | Esri, Maxar, Earthstar Geographics (n.d.). World Imagery basemap in the viewer | basemap only |

## 2. Endpoints and queries used

Coordinates are decimal degrees WGS84. `curl -g` is needed for the ERDDAP brackets. Everything requested was small (1-10 KB) except the one-off lists noted.

| # | Service | Query | Purpose |
|---|---|---|---|
| 1 | Viewer | `https://emodnet.ec.europa.eu/geoviewer/?layers=14159&basemap=esri-imagery&bounds=<xmin,ymin,xmax,ymax in EPSG:3857>&filters=&projection=EPSG:3857`, in my own headless Chrome (section 3.2) | screenshots |
| 2 | Viewer config | `https://emodnet.ec.europa.eu/geoviewer/config.php?legacybaselayers=1` (236 KB JSON layer catalogue) | layer ids, service URLs |
| 3 | REST point | `https://rest.emodnet-bathymetry.eu/depth_sample?geom=POINT(-1.838909 50.717532)` | cell mean/min/max/stdev, elementary surfaces, interpolation flag, source reference (type, EDMO, id) |
| 4 | REST profile | `https://rest.emodnet-bathymetry.eu/depth_profile?geom=LINESTRING(lon lat,lon lat)`, returns 1,000 equally spaced cell values | profile cross-check |
| 5 | ERDDAP | `https://erddap.emodnet.eu/erddap/griddap/bathymetry_dtm_2024.csv?elevation[(lat0):(lat1)][(lon0):(lon1)],value_count[...],cdi_index[...],interpolation_flag[...],elevation_min[...],elevation_max[...],stdev[...]` (10 KB per site). Lattice 1/960 deg, cell centres at 15+(k+0.5)/960 N and -36+(k+0.5)/960 E | primary cell data |
| 6 | WCS 2.0.1 | `https://ows.emodnet-bathymetry.eu/wcs?service=WCS&version=2.0.1&request=GetCoverage&coverageId=emodnet__mean[_2022\|_2020\|_2018]&format=image/tiff&subset=Lat(a,b)&subset=Long(c,d)` (1.4-2.5 KB) | land/foreshore cells that ERDDAP masks; older releases |
| 7 | WFS source patches | `https://ows.emodnet-bathymetry.eu/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=emodnet:source_references&outputFormat=application/json&cql_filter=release='2024' AND INTERSECTS(geom, POINT(lat lon))&propertyName=release,edmo_id,identifier,type,device,metadata_url`. In CQL the point order is lat lon; for boxes use `BBOX(geom,lon0,lat0,lon1,lat1,'EPSG:4326')` | source survey of a cell |
| 8 | WFS quality index | same, with `typeNames=emodnet:quality_index&propertyName=release,edmo_id,identifier,type,combined,horizontal,vertical,age,purpose` | quality classes per release |
| 9 | WFS high-resolution areas | `typeNames=emodnet:hr_bathymetry_area` (1,617 areas, 1.6 MB once; saved as `data/hr_areas.json`) | finer composite DTMs |
| 10 | CDI polygons (plain HTTP only) | `http://geo-service.maris.nl/emodnet_bathymetry/wfs?...typeNames=emodnet_bathymetry:polygons&bbox=lat0,lon0,lat1,lon1,urn:ogc:def:crs:EPSG::4326` | survey names |
| 11 | ISO metadata | `https://emodnet.ec.europa.eu/geonetwork/srv/api/records/<uuid>/formatters/xml` for DTM 2024, QI and HI 1366 | vertical reference, resolution, QI classes |
| 12 | WMS GetCapabilities | `https://ows.emodnet-bathymetry.eu/wms?service=WMS&request=GetCapabilities&version=1.3.0` | layer list (emodnet:mean = 2024; mean_2022 ... mean_2016) |

The CDI detail pages `https://cdi-bathymetry.seadatanet.org/report/edmo/2607/117452` and `/115084` sit behind a "Checking your browser" JavaScript check (plain HTTP) and a "Web Page Blocked" firewall page (headless Chrome). **They were not bypassed.** Reading them is a request for Lior in `REQUESTS_FOR_LIOR.md`.

## 3. Methods

### 3.1 Coordinates (step 1)
`reefs_coords.csv` holds one coordinate per reef and where it came from. Priority: traced `shape.json` geo, then shape work file, then `location_note`, then the card `lat`/`lon` in `02_research/reefs/<slug>.json`.

- **Boscombe:** outline centroid 50.717532 N, 1.838909 W. The card value 50.7185, -1.8417 is about 310 m away and was not used.
- **Borth:** union centroid of the two mounds 52.483453 N, 4.056205 W. The card value is the village centre.
- **Burkitts Reef:** the card JSON stores +24.8205 but the card text says 24 49 14 S. I corrected the sign.
- **Mexico:** no coordinate exists in any verified source.

### 3.2 Access with an isolated headless Chrome (step 2)
`scripts/cdp.py` starts `chrome.exe` (Google Chrome 153.0.8010.53, `--headless=new`) on a **random free port**, with a **fresh `--user-data-dir`** under `%TEMP%`. It connects only to that port and kills only the process tree it started. The shared browser pane was never used. The cookie banner was not clicked.

Two findings about the viewer:
- **A URL with parameters crashes the application**, including its own Share link. It appends `location.search` to its own `config.php?legacybaselayers=1` request and receives a different base-layer format. I rewrite only that request through the DevTools Fetch domain to the clean URL the app uses on a plain load. No access control is touched.
- The map is OpenLayers on canvases. A `drawImage` hook records the destination rectangle of every drawn tile. From these a least-squares affine Web-Mercator-to-pixel map is fitted, with residual <1 px (0.897 px/m at Boscombe, 0.996 px/m at Borth). This puts the points and profile exactly on the screenshots.

Layers in the viewer catalogue (EMODnet Bathymetry group):
- mean depth in natural, multi and rainbow colour (14159, 14157, 14158)
- bathymetric contours (12995)
- **high-resolution bathymetry (13007)**
- **source reference of the DTM (13012)**
- survey tracks and polygons (12425)
- data-quality layers: age, horizontal, vertical, purpose, combined (12999-13003)
- satellite-derived coastlines at LAT, MHW and MSL (12996-12998)
- DTM tile download (12721)

### 3.3 Frames and points (step 4)
Frames are the canonical frames of `shape.json` (x alongshore, y offshore, metres). I re-derived the origins by least squares between `polygons_m` and `polygons_latlon` (residual 0.06-0.07 m).

- **Boscombe:** origin 50.719553 N, 1.839278 W; +x bearing 83.4 deg; +y 173.4 deg.
- **Borth:** origin 52.483475 N, 4.05134 W on the defence line; +x bearing 359.57 deg; +y (offshore, west) 269.57 deg.

Conversion: E = x sin(bx) + y sin(by), N = x cos(bx) + y cos(by), then a WGS84 geodesic forward from the origin.

Points:
- **Boscombe:** the 11 points of `3d/REQUESTS_FOR_LIOR.md`: reef centre, Navionics drying patch, survey peak, 4 toes, 4 seabed.
- **Borth:** it has no 3D folder and no request file, so I generated 16 points from the outline. They are the centre of both mounds, then per mound the centre, four toes, seabed 60 m shoreward and 60 m seaward, plus the gap between the mounds.

### 3.4 Profiles
Shore-normal lines through the reef centroid: Boscombe x = 0.1 m; Borth x = 0 m and through each mound centre. y runs from -100 to 650 m every 5 m.

- **(a)** The nearest-cell value. This is the true structure of the DTM, a set of steps. The cell's min, max, sounding count and flags are kept.
- **(b)** Bilinear interpolation between cell centres, for plotting only.
- **(c)** The REST `/depth_profile` over y = 0-500 m as an independent check. It returns the same cell steps: Boscombe 6, Borth 8.

Where ERDDAP masks a cell (landward of the coastline) the WCS value is used and flagged.

### 3.5 Source survey and age
The WFS patch of release 2024 at a point gives EDMO and CDI identifier. REST gives its own cell reference.
- At the 11 Boscombe points they agree (CDI 117452).
- At Borth the WFS patch is CDI 115084 everywhere. REST says GEBCO2024 for the interpolated cells. The patch is the survey's coverage; the cell value is a fill.

The survey age is not published by these services. The **Quality Index age class** is: 0 = >30 y, 1 = 10-30 y, 2 = 5-10 y, 3 = 0-5 y (E5). I assume the classes are evaluated at the release date. CDI 117452 has age 2 in releases 2018 and 2020 and age 1 in 2022 and 2024. That brackets the survey between 2011.0 and 2012.99.

### 3.6 Comparison with the Boscombe model (step 5)
`scripts/compare_boscombe.py` loads `model.js` read-only (a node dump to `%TEMP%`; nothing is written under any `3d\` folder). For each DTM cell that overlaps the model grid, the cell rectangle is transformed to the canonical frame. The model is then averaged over the 2 m seabed grid points and the 1 m reef grid points inside it. The equations are in section 4.

## 4. Datum handling (equations)

EMODnet `e` is the height of the cell mean above LAT in metres (negative below), so depth below LAT is `d_LAT = -e`. The project model uses `z` in metres above MSL.

- **(D1)** `z_MSL = e - (MSL - LAT)`.
  - At Boscombe `MSL - LAT = (MSL - CD) + (CD - LAT) = 1.40 + 0.06 = 1.46 m`.
  - 1.40 m is chart datum below ODN (M3), with the model's assumption ODN = MSL +-0.10 m (A4). 0.06 m is LAT relative to ACD (M1 Table 1).
  - It equals the model's own LAT level (-1.46 m MSL).
- **(D2)** `z_ACD = e + LAT_ACD = e - 0.06`. The model's survey datum is ACD (assumption A3).
- **(D3)** Comparison in the LAT frame: `z_LAT = z_MSL + 1.46` and `Delta_c = e_c - (1/N_c) sum_{p in c} (z_model(p) + 1.46)`.
- **(D4)** Navionics soundings of depth `d` below chart datum, assumed ACD (model assumption A9): `z_LAT = -d - LAT_ACD = -d + 0.06`.
- **(D5)** Alternative reading, tested in 6.2: if the Boscombe values were referenced to ODN (about MSL) and merely labelled LAT, then `Delta' = Delta + 1.46`.
- **(D6)** Uncertainty: `sigma(Delta)^2 = sigma_e^2 + sigma_model^2 + sigma_off^2`.
  - `sigma_e = stdev/sqrt(n)`. For the reef cell this is 0.43/sqrt(12) = 0.12 m.
  - `sigma_model` is about 0.35 m (colour read 0.2 plus interpolation under the reef 0.3, from the model's `METHODS_3D.md` section 5).
  - `sigma_off` is 0.10 m. The total is about **0.4 m**.
  - This formula excludes the sampling mismatch. A cell mean over 8,500 m2 of a seabed that drops 1.2-1.9 m per 100 m adds up to +-0.7-1.0 m.
- **(D7) Borth:** `z_MSL = e - (MSL - LAT)_Borth`. I did not verify the local value.
  - NTSLF lists Barmouth and Fishguard (-2.44 m) but not Aberystwyth.
  - A web-search summary gave -2.25 m for Aberystwyth, which I could not confirm on a primary page. The Borth 3D agent must take it from a tide table.
  - EMODnet values in interpolated (GEBCO-filled) cells are nominally LAT. The metadata does not say how the fill was reduced to LAT, so they carry an additional unknown offset.

## 5. Results

### 5.1 Coverage of the 13 reefs

| Reef (slug) | Coordinate used | REST depth_sample | In DTM domain | Covered |
|---|---|---|---|---|
| narrowneck-gold-coast | -27.9864, 153.4297 | 204 (empty) | no | **no** |
| cables-reef-wa | -32.0000, 115.7400 | 204 (empty) | no | **no** |
| prattes-reef-el-segundo | 33.9151, -118.4326 | 204 (empty) | no | **no** |
| mount-maunganui-reef | -37.6448, 176.2026 | 204 (empty) | no | **no** |
| opunake-reef | -39.4600, 173.8600 | 204 (empty) | no | **no** |
| boscombe-surf-reef | 50.7175, -1.8389 | 200 | yes | **yes** |
| kovalam-reef-india | 8.4004, 76.9787 | 204 (empty) | no | **no** |
| borth-coastal-defence-reef | 52.4835, -4.0562 | 200 | yes | **yes** (reef cell = GEBCO fill) |
| palm-beach-gold-coast | -28.1073, 153.4709 | 204 (empty) | no | **no** |
| southern-ocean-surf-reef-albany | -35.0236, 117.9136 | 204 (empty) | no | **no** |
| burkitts-reef-bargara | -24.8205, 152.4625 | 204 (empty) | no | **no** |
| bunbury-airwave | -33.3276, 115.6284 | 204 (empty) | no | **no** |
| mexico-reef-2026-unnamed | none (no coordinate in any verified source) | - | no (Pacific Mexico) | **no** |

### 5.2 Per-reef result table (covered reefs)

| Reef | Covered | Resolution at the reef | Vertical reference | Depth at the reef (m rel. LAT) | Profile file | Source survey |
|---|---|---|---|---|---|---|
| boscombe-surf-reef | yes | DTM cell 115.8 x 73.4 m. Sub-cell source spacing about 27 m (12 soundings) to 46 m (4). High-resolution DTM: none (nearest 106 km) | LAT (ISO record E1; ERDDAP `long_name`) | **-5.62** at the centre (cell mean; min -6.21, max -4.87; sd 0.43; n 12). Toe and seabed points -3.99 ... -5.62 (5.3) | `data/boscombe-surf-reef_profile_through_reef_centre.csv` (5 m steps), `..._with_model.csv`, `..._profile_REST_depth_profile_y0_500.csv` | CDI 117452, EDMO 2607 OceanWise Ltd (UKHO-derived). QI: horizontal 3 (<20 m), vertical 4 (MBES >100 kHz), age 1 (10-30 y), purpose 3. Survey about 2011-2012 (inferred). CDI polygons "Poole Bay, Blocks 14-17" and "Block 12" |
| borth-coastal-defence-reef | yes, but the reef cells are interpolation | DTM cell 115.8 x 70.6 m. 1 source value per cell (about 90 m spacing) or interpolated. High-resolution DTM: none at the site (CHERISH Wales 14 m is 22 km north) | LAT (grid). GEBCO-filled cells: LAT nominal, reduction not documented | **-0.18** at the centre of both mounds (interpolated; REST reference GEBCO2024). Mounds -0.13 ... -0.40. Seabed 60 m seaward -1.10 (surveyed cell) | `data/borth-coastal-defence-reef_profile_through_reef_centre.csv`, `..._through_N_hook_centre.csv`, `..._through_S_oval_centre.csv`, `..._profile_REST_depth_profile_y0_500.csv` | CDI 115084, EDMO 2607 OceanWise Ltd. QI: horizontal 0 (unknown), vertical 3, age 0 (>30 y), purpose 3. Reef cells: GEBCO 2024 fill |
| the other 11 reefs | no | - | - | - | - | - |

### 5.3 Boscombe: points

Cell values. The model seabed at the same point is shown for orientation only, because the cell is an average and the point is not.

| # | Point | lat, lon | Cell mean (m rel. LAT) | MSL frame | min .. max (n) | Model seabed at point (LAT) |
|---|---|---|---|---|---|---|
| 1 | centre_outline_centroid (reef centre) | 50.717532, -1.838909 | -5.62 | -7.08 | -6.21 .. -4.87 (12) | -3.30 |
| 2 | drying_patch_centre (Navionics drying patch centre) | 50.717704, -1.838728 | -5.62 | -7.08 | -6.21 .. -4.87 (12) | -3.10 |
| 3 | survey_peak_Apr2011 (reef crest) | 50.717851, -1.838682 | -3.99 | -5.45 | -4.66 .. -2.80 (4) | -3.34 |
| 4 | toe_shoreward (toe) | 50.718010, -1.838597 | -3.99 | -5.45 | -4.66 .. -2.80 (4) | -3.31 |
| 5 | toe_west_flank (toe) | 50.717505, -1.839447 | -5.62 | -7.08 | -6.21 .. -4.87 (12) | -3.30 |
| 6 | toe_east_flank (toe) | 50.717817, -1.838276 | -4.03 | -5.49 | -4.34 .. -3.87 (6) | -2.37 |
| 7 | toe_offshore_tail (toe) | 50.717033, -1.839104 | -5.62 | -7.08 | -6.21 .. -4.87 (12) | -4.69 |
| 8 | seabed_y100 (seabed) | 50.718660, -1.839115 | -3.99 | -5.45 | -4.66 .. -2.80 (4) | -1.34 |
| 9 | seabed_y320 (seabed) | 50.716697, -1.838757 | -5.62 | -7.08 | -6.21 .. -4.87 (12) | -5.04 |
| 10 | seabed_80m_west (seabed) | 50.717462, -1.840039 | -5.53 | -6.99 | -6.07 .. -4.74 (12) | -3.44 |
| 11 | seabed_90m_east (seabed) | 50.717726, -1.837660 | -4.03 | -5.49 | -4.34 .. -3.87 (6) | -2.68 |

Cell structure along the shore-normal line (x = 0.1 m; y from the origin on the 2011-09-28 surf line). The cells are tilted slightly because the frame is rotated 6.6 deg from north.

| y range (m) | Cell mean (m rel. LAT) | min .. max | n | Flag |
|---|---|---|---|---|
| -100 .. 85 | land / foreshore (WCS fill; ERDDAP masked): +8.5 .. +0.14 | - | - | land |
| 90 .. 205 | -3.99 | -4.66 .. -2.80 | 4 | surveyed |
| 210 .. 320 | **-5.62** (contains the reef) | -6.21 .. -4.87 | 12 | surveyed |
| 325 .. 435 | -7.05 | -7.67 .. -6.37 | 16 | surveyed |
| 440 .. 450 / 455 .. 555 | -8.52 / -9.10 | -9.28 .. -7.78 / -9.62 .. -8.24 | 16 | surveyed |
| 560 .. 650 | -10.17 | -10.53 .. -9.73 | 16 | surveyed |

The offshore gradient from the four full cells (y centres 148-605 m) is **-1.41 %**. This is a regression of cell means on cell-centre y; it is -1.45 % for y >= 250 m.

### 5.4 Borth: points

| # | Point | lat, lon | Cell mean (m rel. LAT) | n | Cell status | REST reference |
|---|---|---|---|---|---|---|
| 1 | centre_both_mounds (reef centre) | 52.483453, -4.056205 | -0.18 | 3 | interpolated (GEBCO fill) | DTM GEBCO2024 |
| 2 | N_hook_centre | 52.483802, -4.056242 | -0.18 | 3 | interpolated | DTM GEBCO2024 |
| 3 | N_hook_toe_shoreward | 52.483803, -4.056043 | -0.18 | 3 | interpolated | DTM GEBCO2024 |
| 4 | N_hook_toe_seaward | 52.483800, -4.056800 | -0.40 | 1 | source sounding | CDI 115084 |
| 5 | N_hook_toe_north | 52.483978, -4.056244 | -0.18 | 3 | interpolated | DTM GEBCO2024 |
| 6 | N_hook_toe_south | 52.483734, -4.056241 | -0.18 | 3 | interpolated | DTM GEBCO2024 |
| 7 | N_hook_seabed_60m_shoreward | 52.483807, -4.055160 | -0.34 | 1 | interpolated | CDI 115084 |
| 8 | N_hook_seabed_60m_seaward | 52.483795, -4.057683 | -1.10 | 1 | source sounding | CDI 115084 |
| 9 | S_oval_centre | 52.482686, -4.056124 | -0.13 | 3 | interpolated | DTM GEBCO2024 |
| 10 | S_oval_toe_shoreward | 52.482687, -4.055915 | -0.13 | 3 | interpolated | DTM GEBCO2024 |
| 11 | S_oval_toe_seaward | 52.482685, -4.056335 | -0.12 | 3 | interpolated | DTM GEBCO2024 |
| 12 | S_oval_toe_north | 52.483004, -4.056128 | -0.13 | 3 | interpolated | DTM GEBCO2024 |
| 13 | S_oval_toe_south | 52.482367, -4.056120 | -0.13 | 3 | interpolated | DTM GEBCO2024 |
| 14 | S_oval_seabed_60m_shoreward | 52.482691, -4.055032 | +0.97 | 3 | interpolated | DTM GEBCO2024 |
| 15 | S_oval_seabed_60m_seaward | 52.482681, -4.057218 | -0.12 | 3 | interpolated | DTM GEBCO2024 |
| 16 | gap_between_mounds | 52.483244, -4.056183 | -0.13 | 3 | interpolated | DTM GEBCO2024 |

Cell structure along the line through the centre of both mounds (x = 0; y from the defence line towards the west):

| y range (m) | Cell mean (m rel. LAT) | n | Flag |
|---|---|---|---|
| -100 .. 50 | +3.2 / +5.2 / +4.5 (WCS fill: beach, promenade, houses) | - | land |
| 55 .. 120, 125 .. 190 | +5.41, +2.70 | 1, 3 | interpolated (GEBCO fill) |
| 195 .. 260 | -0.34 | 1 | interpolated |
| 265 .. 330 | **-0.18** (reef centre cell) | 3 | interpolated; REST reference GEBCO2024 |
| 335 .. 400 | -0.40 | 1 | source sounding (CDI 115084) |
| 405 .. 475 / 480 .. 545 / 550 .. 615 / 620 .. 685 | -1.10 / -1.91 / -2.73 / -3.36 | 1 each | source soundings |

The gradient of the surveyed cells (y centres 368-652 m) is **-1.1 %**, about 1:90. The residuals about the fitted line are <= 0.06 m.

### 5.5 Viewer screenshots and plots
Annotated screenshots of the EMODnet Map Viewer (own Chrome, 2026-10-06) show the DTM cell grid with values, the reef outline, the numbered points and the profile.
- `viewer/<slug>_viewer_dtm_annotated.png` uses layer 14159.
- `viewer/<slug>_viewer_sources_annotated.png` uses layer 13012 (source patches).
- The raw captures are `*_raw.png`.

Plots in `figures/`:
- `boscombe-surf-reef_profile_emodnet_vs_model.png`
- `boscombe-surf-reef_cells_emodnet_vs_model.png`
- `boscombe-surf-reef_dtm_release_history.png`
- `borth-coastal-defence-reef_profile_emodnet.png`

All are registered in `03_images/reefs/<slug>/images.json` as boscombe-surf-reef-img-25..29 and borth-coastal-defence-reef-img-14..16.

## 6. Comparison with the Boscombe model

### 6.1 Numbers (EMODnet minus model, metres, after the datum conversion D1-D3)

Cells fully inside the model grid and seaward of y = 90 m (7 cells; `data/boscombe-surf-reef_cells_emodnet_vs_model.csv`):

| Cell (ki/kj) | y (m) | EMODnet mean (n) | model seabed | model as-built (with reef) | Delta vs seabed | Delta vs as-built |
|---|---|---|---|---|---|---|
| 34289/32793 | 140 | -4.67 (4) | -1.62 | -1.62 | -3.05 | -3.05 |
| 34289/32794 | 148 | -3.99 (4) | -2.39 | -2.09 | -1.60 | -1.90 |
| 34289/32795 | 156 | -4.03 (6) | -1.91 | -1.81 | -2.12 | -2.22 |
| 34288/32793 | 255 | -5.53 (12) | -4.39 | -4.39 | -1.14 | -1.14 |
| **34288/32794 (reef centre)** | 263 | **-5.62 (12)** | **-4.23** | **-3.10** | **-1.39** | **-2.52** |
| 34288/32795 | 272 | -5.26 (12) | -3.96 | -3.95 | -1.30 | -1.31 |
| 34288/32796 | 280 | -5.76 (9) | -3.80 | -3.80 | -1.96 | -1.96 |

- Mean Delta vs the seabed is **-1.80 m (sd 0.66 m, range -1.14 to -3.05)**.
- The three best-sampled cells (n = 12) give -1.14, -1.39 and -1.30 m.
- Against the April 2011 survey surface, the reef cell gives -2.11 m.
- Against 33 Navionics soundings (assumed chart datum, D4): mean **-1.61 m (sd 1.13)**.
  - For cells with n >= 12 soundings and y >= 280 m (10 soundings): **-0.76 +- 0.63 m**.
  - For cells with n < 12 (13 soundings): **-2.08 +- 0.91 m**.

Plots: `figures/boscombe-surf-reef_cells_emodnet_vs_model.png` and `..._profile_emodnet_vs_model.png`.

### 6.2 Is the offset a datum shift?
A pure datum error would be constant. This offset is not.
- It is smallest in the well-sampled deeper cells (about -0.8 m at 5-6 m depth) and largest in the shallow cells with 4-6 soundings (-1.6 to -3.1 m).
- EMODnet cell means fall 1.4 % between the cell centres at y = 148 and 265 m. The model falls about 1.9 % and Navionics about 2.2 % over the same stretch.
- A likely contributor is the source survey's shallow limit. Cells at the edge of a multibeam survey contain only the soundings from their deeper part, which biases the cell mean deep.

**Two readings remain open and cannot be separated with these data:**
- (a) EMODnet is correctly LAT, and the nearshore cells are biased deep by sampling.
- (b) The source values are effectively referenced to ODN (about MSL) and labelled LAT. Then `Delta' = Delta + 1.46` is **+0.18 m** for the three n = 12 cells and **-0.34 m** for all seven. Against Navionics it is -0.15 m. That is a better match.

The vertical datum of CDI 117452, read from its CDI page, would decide. It is listed for Lior. For the model this means **EMODnet absolute levels at Boscombe carry about +-1.5 m of datum and sampling uncertainty** and must not override the Fig. 9 survey and the Navionics soundings.

### 6.3 Can the resolution show a reef of about 120 x 45 m?
**No, only the seabed trend.**
- The cell footprint is 8,500 m2 against a reef outline of 4,042 m2 (minimum rotated rectangle 121 x 45 m).
- The reef is narrower than one cell (73 m E-W) and about as long as one cell (116 m N-S). Resolving a 45 m wide object needs cells of 20 m or less.
- A reef signal could appear as a shallower cell mean or maximum. The model predicts it clearly. With the as-built reef the reef cell mean would be **-3.10 m instead of -4.23 m (1.13 m shallower)**, and the cell maximum **+0.56 m**.
- The DTM cell has mean -5.62 m and maximum **-4.87 m**. None of its 12 soundings (spacing about 27 m, enough for 5-6 hits on the reef) lies above -4.87 m.

### 6.4 Is the reef visible, and in which survey year?
**Not visible** in any release.
- Releases 2018, 2020, 2022 and 2024 were checked.
- Releases 2020, 2022 and 2024 are identical at every sea cell of the Boscombe box.
- Release 2018 differs by 0.4 m at the reef cell and by 2.6 m in the shoreward cell (`figures/boscombe-surf-reef_dtm_release_history.png`).

The DTM source at the reef is CDI 117452. Its quality-index age class is 2 (5-10 y) in releases 2018 and 2020 and 1 (10-30 y) in 2022 and 2024. That places the survey in **2011-2012** if the classes are counted to the release date.
- A candidate is the Maritime and Coastguard Agency multibeam survey of Poole Bay, 2011-08-26 to 2012-01-04 (O3).
- The record's extent (50.678-50.695 N) ends 2.5 km south of the reef, and its identity with CDI 117452 is **not confirmed**.

The reef (damaged but present) existed in 2011-2012. The April 2011 DGPS crest was +0.68 m ACD, and it is still a shoal on Navionics. A survey of that date should have shown it if its soundings reached the reef zone. So either the DTM cells at the reef do not carry the survey's shallow detail, or the survey is older than the age class suggests. This is an **open question for the CDI record**.

## 7. Limitations

1. **Resolution:** 116 x 70 m cells. No shape, toe or crest information; slopes only at the 100 m scale.
2. **Survey identity and date** cannot be obtained from the machine services. The CDI pages are behind a bot check (not bypassed). The 2011-2012 date is an inference from the QI class history under an assumption.
3. **Vertical reference:** LAT is stated for the product.
   - At Boscombe the empirical offset to our survey- and Navionics-based seabed (-1.8 m in the LAT frame, -0.3 m if ODN) cannot be attributed (6.2).
   - For interpolated cells (the Borth reef) the reduction of the GEBCO fill is not documented.
   - The MSL-LAT offset at Borth is unverified.
4. **Borth reef cells are GEBCO interpolation.** The surveyed cells hold one sounding each, are older than 30 y, and have horizontal accuracy class "unknown or > 500 m".
5. **Land mask:** ERDDAP returns NaN landward of the DTM coastline. Foreshore and beach values were taken from the WCS coverage, which blends land data and is not survey-based. The beach part of both profiles is indicative only.
6. **Releases:**
   - The 2018 WCS coverage is stored positive-down (sign flipped in `wcs_2018_signflipped`).
   - The 2016 release is a coarser 1/8 arc-min grid and empty in our boxes.
   - 2020-2024 are identical here.
7. **Comparison:** the model is itself a read of a plotted DGPS surface (+-0.2 m). Its seabed is spline-extrapolated beyond y = 305 m (+-0.5 m). Some cell averages cover that extrapolated part. The cell footprints use the model's 2 m grid (about 2,100 nodes per cell).
8. **Navionics** soundings assume chart datum = ACD (model assumption A9). The viewer never states a datum.
9. **Screenshots:** the Esri basemap date is not stated by the viewer. The cookie banner was left untouched.
10. **Licence:** EMODnet CC BY 4.0, with originator licences to be checked before any public release. Not for navigation.

## 8. Haifa (one line, for later)
**EMODnet covers the Israeli coast near Haifa with the same 1/16 arc-minute DTM (cells about 115.8 x 97.4 m at 32.8 N). The cells at the Haifa shore and 1 km off it are interpolated (composite `JOINT_ISRAEL_NBS_QUARTMIN_GEO`, 1/4 arc-min). Real survey data (IOLR-GEO-EEZ-2012-1, multibeam) exist only offshore, about 10 km out. No high-resolution DTM lies within 900 km** (`data/haifa_check.json`; nothing further researched).

## 9. Integration plan: exactly what each 3D model should take from EMODnet, and why

The 3D agents integrate later; this is the specification. Values are metres relative to LAT unless "MSL" is written. At Boscombe `z_MSL = e - 1.46` (D1).

### 9.1 `boscombe-surf-reef` (model exists)

| Take | Value | Why / how |
|---|---|---|
| **Datum statement** | EMODnet DTM 2024 vertical reference = LAT. Model LAT level = -1.46 m MSL | Upgrade provenance row S5 from "WMS GetFeatureInfo, ~115 m" to the verified metadata: cell 115.8 x 73.4 m, CDI 117452, EDMO 2607, QI classes |
| **Offshore seabed trend beyond the model grid** (y > 380 m, up to 650 m) | Slope **-1.41 %** (+-0.10 %) from the four full cells. Cell means at centres y = 380 / 445-505 / 605 m: -7.05 / -8.52..-9.10 / -10.17 m LAT = -8.51 / -9.98..-10.56 / -11.63 m MSL | The model grid ends at y = 380 m (spline extrapolation). Extend it as `z(y) = z_model(380) - 0.0141 (y - 380)`. This ties to the EMODnet cell means within about 0.8 m at y = 605. Mark the cells as code 1 (extrapolated), source EMODnet, uncertainty +-1.0 m |
| **Provenance cross-check row** (not a model value) | Reef-centre cell -5.62 (-7.08 MSL), n 12, min/max -6.21/-4.87. Model minus EMODnet = +1.39 m. Seven-cell mean +1.80 +- 0.66 m. No reef in the DTM | Add to `METHODS_3D.md` section 4 (validation) and to the model `provenance` with `estimated: false`, `uncertainty: +-1.5 m datum/sampling` |
| **Do NOT take** | Crest, toe depths, seabed under or around the reef (y 100-305 m), beach (y < 100 m), reef height | The cells are larger than the reef. EMODnet is 1.1-3.1 m deeper than Fig. 9 plus Navionics and shows no reef. Those two sources and the design depth "3-5 m CD" agree with each other |
| **Datum assumption A3** | Keep chart datum (ACD) for Fig. 9 | EMODnet does not overturn it, because the offset is not constant (6.2). Re-open only if the CDI 117452 page shows ODN referencing (Lior request 1) |
| **Optional context layer** | The 143 DTM cells of `data/boscombe-surf-reef_cells_dtm2024_erddap.csv` as a coarse backdrop beyond y = 380 m | Shows the regional bathymetry. Label it "EMODnet DTM 2024, 116 x 73 m cells, LAT, not for navigation" |

### 9.2 `borth-coastal-defence-reef` (model not built yet)

| Take | Value | Why / how |
|---|---|---|
| **Datum** | EMODnet = LAT. Convert with `z_MSL = e - (MSL - LAT)_Borth` once that offset is verified from a tide table | The model zero is MSL. NTSLF lists Barmouth and Fishguard at -2.44 m, not Aberystwyth. The -2.25 m for Aberystwyth is unverified |
| **Offshore seabed gradient** beyond the reef toe (y >= 335 m from the defence line, west) | **-1.1 %** (about 1:90). Cell means -0.40 (y 368), -1.10 (440), -1.91 (513), -2.73 (583), -3.36 (652) m LAT | These are the only survey-based cells. One sounding per cell, age class >30 y, horizontal class unknown. Uncertainty +-0.4 m in level and +-0.3 % in slope |
| **"Reef sits near LAT" check** (not a model value) | Cells covering the reef: -0.34 .. -0.13 m LAT (interpolated GEBCO) | Agrees qualitatively with rock that is bare at low tide (Esri 2024-09-17 low-tide image in `shape.json`). It cannot give crest or toe |
| **Do NOT take** | Reef-cell values as seabed or crest. The interpolated shoreward cells (+0.97 .. +5.4 m) as the beach profile. Anything as reef height | GEBCO interpolation, not a survey. The beach and foreshore must come from other sources: Welsh coastal monitoring LiDAR or beach profiles, Google Earth, Lior's Navionics reading |
| **Finer data** | BY_CHERISH_Wales_14m (22 km north, 1/128 arc-min) | Not at Borth. Do not extrapolate it to the reef |

### 9.3 The other 11 reefs
EMODnet is not available. Use the national sources named in `model_3d.md` (AusSeabed or council LiDAR, LINZ, NOAA), or Lior's Navionics and Google Earth readings.

## 10. Files
- `METHOD.md` (step log)
- `reefs_coords.csv`
- `REQUESTS_FOR_LIOR.md`
- `REPORT.md` (this text)
- `data/`: coverage, cells, points, profiles, releases, comparison CSV/JSON, survey patches, HR areas, Haifa check
- `scripts/`:
  - `make_coords.py`, `coverage_all.py`, `cdp.py`, `extract_site.py`, `rest_profiles.py`
  - `compare_boscombe.py`, `viewer_lib.py`, `make_viewer_figures.py`, `make_plots.py`
  - `haifa_check.py`, `register_images.py`
- `viewer/` and `figures/` (images)
- Software: Python 3.14.4 with numpy 2.4.4, pandas 3.0.2, pyproj 3.8.0, shapely 2.1.2, matplotlib 3.10.9, tifffile 2026.9.20, websockets 16.0, and Node for the model dump.

## 11. References
- EMODnet Bathymetry Consortium (2024). EMODnet Digital Bathymetry (DTM 2024). https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1 (accessed 2026-10-06).
- EMODnet Bathymetry Consortium (n.d.). EMODnet Bathymetry Quality Index, Sextant record 6572ee07-a078-4adc-b868-fd1f7084c660 (accessed 2026-10-06).
- EMODnet (n.d.). Terms of use for EMODnet online services, data and data products. https://emodnet.ec.europa.eu/en/terms-use-emodnet-online-services-data-and-data-products (accessed 2026-10-06).
- EMODnet Bathymetry (n.d.). EMODnet Bathymetry REST service. https://rest.emodnet-bathymetry.eu/ (accessed 2026-10-06).
- Joint Nature Conservation Committee and Natural England (2013). HI 1366 2012 MCZ CHP Multibeam Survey Poole Bay (GB100215). https://emodnet.ec.europa.eu/geonetwork/srv/api/records/6d906048-5195-4f53-90d0-4d17807117b1 (accessed 2026-10-06).
- Mead, S., Blenkinsopp, C., Moores, A. and Borrero, J. (2010). Design and construction of the Boscombe multi-purpose reef. Coastal Engineering Proceedings 32 (ICCE 2010), 1352.
- National Tidal and Sea Level Facility (n.d.). Chart datum and ordnance datum. https://ntslf.org/tides/datum (accessed 2026-10-06).
- OceanWise (2021). OceanWise UK lead to latest European Bathymetry Digital Terrain Model. https://www.oceanwise-global.com/oceanwise-uk-lead-to-latest-european-bathymetry-digital-terrain-model/ (accessed 2026-10-06).
- Rendle, E. and Davidson, M. (2012). An evaluation of the physical impact and structural integrity of a geotextile surf reef. Coastal Engineering Proceedings 33 (ICCE 2012), 6794.
- SeaDataNet (n.d.). EDMO register, entry 2607 (OceanWise Limited). http://edmo.seadatanet.org/report/2607 (accessed 2026-10-06).

---


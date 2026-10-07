# Provenance of files saved in 3d/src/ (private research copies; retrieved 2026-10-05)
Reuse rights: US federal data (NOAA/NCEI/CO-OPS) are public domain; the CCC staff report is a public agency record (reuse terms not stated); the ICCE-2010 paper is CC BY 4.0 (cite the authors). Check before any public release.

| file | what | URL / request | credit | licence | retrieved |
|---|---|---|---|---|---|
| noaa_9410840_datums.json | NOAA CO-OPS tidal datums, Santa Monica (9410840), metric, epoch 1983-2001 | https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations/9410840/datums.json?units=metric | NOAA CO-OPS | public domain (US gov) | 2026-10-05 |
| noaa_9410840_station.json | station metadata (lat 34.0083, lon -118.5, NWLON, established 1932) | .../stations/9410840.json | NOAA CO-OPS | public domain | 2026-10-05 |
| noaa_9410660_datums.json | datums, Los Angeles Outer Harbor (9410660), cross-check | .../stations/9410660/datums.json?units=metric | NOAA CO-OPS | public domain | 2026-10-05 |
| noaa_santa_monica_13as_navd88_export.tif | float32 GeoTIFF export (216 x 270 px, nearest neighbour, cell 0.000092592 deg = 1/3 arc-sec) of "Santa Monica, California 1/3 arc-second NAVD 88 Coastal DEM" (NGDC 2010-03-12), bbox W -118.445 S 33.905 E -118.420 N 33.925 | ImageServer exportImage on https://gis.ngdc.noaa.gov/arcgis/rest/services/DEM_mosaics/DEM_all/ImageServer with mosaicRule esriMosaicLockRaster lockRasterIds [173]; script src/export_dem.py | NOAA NGDC / NCEI | public domain | 2026-10-05 |
| noaa_santa_monica_13as_mhw_export.tif | same, MHW-datum version (catalog id 121) - used only for the datum check | same, lockRasterIds [121] | NOAA NGDC | public domain | 2026-10-05 |
| noaa_socal_crm_1as_export.tif | float32 export (72 x 90 px, 1/3600 deg) of "U.S. Coastal Relief Model - Southern California v2" 1 arc-sec (NGDC 2013-07-08), MSL datum, same bbox - independent second DEM for cross-check | lockRasterIds [196] | NOAA NGDC | public domain | 2026-10-05 |
| ccc_W5a-10-1998_staff_report.pdf | California Coastal Commission staff report W5a, CDP application E-98-15 (Surfrider Foundation - Pratte's Reef), hearing 13 Oct 1998; Exhibit 2 (p.30) cross-section June 1997; Exhibit 3 (p.31) plan view July 1996 with depth contours | https://documents.coastal.ca.gov/reports/1998/10/W5a-10-1998.pdf | California Coastal Commission; drawings by Skelly Engineering | public record; reuse terms not stated | 2026-10-05 |
| icce2010_borrero_mead_moores_SFC.pdf | Borrero, J.C., Mead, S.T. & Moores, A. (2010/2011) "Stability considerations and case studies of submerged structures constructed from large, sand filled, geotextile containers", Coastal Engineering Proceedings 1(32), structures.60, doi:10.9753/icce.v32.structures.60 (p.2 Fig.1 bag size; p.7 Pratte's text) | https://pdfs.semanticscholar.org/8672/e1bb2043e0a227ce0e2ef6e01dd01bc8729e.pdf (record: https://icce-ojs-tamu.tdl.org/icce/article/view/1172) | authors / Coastal Engineering Research Council | authors / ICCE; CC BY 4.0 per the ICCE-OJS record | 2026-10-05 |

## Navionics screenshots (added 2026-10-05, run 2) - src/navionics/
Reuse rights: NOT cleared. Garmin Navionics content (c) Garmin; private research copy only, not for publication or for navigation ("Not to be used for navigation" is printed on the page).
Access: https://webapp.navionics.com/ redirects (HTTP 301/302) to Garmin's "Marine Maps" web viewer https://maps.garmin.com/en-US/marine/ (page title "Garmin | Marine Maps"; Leaflet 1.9.4 map with Navionics tiles; no login or CAPTCHA shown; cookie banner never appeared in headless Chrome 153). Opened on 2026-10-05 in an own headless Chrome (CDP, temporary profile, killed afterwards), map centred on 33.9188 N, -118.4324 W (text-derived position hint of the removed reef) via the page's own `key` geohash 9q5bcn8pm and Leaflet setView.
App options used (see app_options_sonarchart_feet.png): View = Map; Chart type = SonarChart Maps (sonar_*) or Nautical Charts (nautical_*); Seabed areas = Hide; Depth units = Feet; Shallow shading = 6 ft (default). The page does not state the depth datum or the contour interval.
| file | what | zoom | note |
|---|---|---|---|
| sonar_ft_z18_map.png | SonarChart layer, feet, map container only (985 x 751 px, 0.4955 m/px at 33.9188 N), centred on the hint | 18 (max) | used for the contour-crossing transects (nav_transect.json) |
| sonar_ft_z17_map.png | same, zoom 17 (0.99 m/px), contour labels (1, 3, 5, 6, 11, 15, 16, 17 ... ft) visible | 17 | used to read labels |
| nautical_ft_z18_map.png / nautical_ft_z17_map.png | Nautical Charts layer, feet: spot soundings (15, 21, 13.1 ft ...) and coarse contours | 18 / 17 | used for the spot-sounding anchor (15 ft) |
| app_options_sonarchart_feet.png | the MAP OPTIONS panel with the settings above | - | record of the settings |
| session_state.json | map centre, zoom, bounds, size, user agent, UTC time of the capture | - | |
| transect_lib.py | image-analysis helper (dark-pixel runs along a line) | - | |

## Run 3 additions (2026-10-05)
Reuse rights: NOT cleared for any item below (private research copies).
| file | what | URL / request | credit | licence | retrieved |
|---|---|---|---|---|---|
| ../../src/borrero_nelsen_2003_prattes_monitoring_results.pdf | Borrero, J.C. & Nelsen, C. (2003) 'Results of a comprehensive monitoring program at Pratte's Reef', 16 pp.; also listed in ../../sources.md as img7 | supplied by Lior on 2026-10-05 (his Downloads\Pratte_results.pdf); original URL unknown; venue/year not printed in the file | J.C. Borrero (USC), C. Nelsen (Surfrider Foundation); Fig. 4 by Skelly Engineering | copyright holder; private research copy | 2026-10-05 |
| bn2003_digitised.json, bn2003_fig9_contours.json | numbers digitised from the vector paths of Figs 5, 7, 9 of that PDF (+ Fig. 8 read by eye) by ../bn_digitise.py | derived | this project | derived from the above | 2026-10-05 |
| navionics/sonar_ft_z18_map.png, sonar_ft_z17_map.png, nautical_ft_z18_map.png, nautical_ft_z17_map.png, session_state.json, app_options_sonarchart_feet.png | SECOND Navionics capture, centred on 33.92058 N, 118.43335 W (the Fig. 9 window centre); own headless Chrome, random free port, fresh profile (isolation rule), Leaflet setView, same options as the first capture (feet, shallow shading 6 ft) | https://maps.garmin.com/en-US/marine/ (webapp.navionics.com redirects), accessed 2026-10-05 | Garmin Navionics | (c) Garmin; not for navigation | 2026-10-05 |
| navionics/hint1_33.9188_-118.4324/ | the FIRST capture (centred on the superseded text hint) moved here with its nav_transect.json | as above | Garmin Navionics | as above | 2026-10-05 |


```json
{
  "covered_reefs": ["boscombe-surf-reef", "borth-coastal-defence-reef"],
  "per_reef": {
    "boscombe-surf-reef": {"covered": true, "resolution_m": "DTM cell 115.8 x 73.4 m (1/16 arc-min); sub-cell source spacing about 27-46 m (12 or 4 soundings); no high-resolution DTM within 100 km (nearest 106 km)", "vertical_ref": "LAT (verified in the ISO record and the ERDDAP long_name); model conversion z_MSL = e - 1.46", "depth_at_reef_m": "-5.62 rel. LAT at the reef centre (cell mean; min -6.21, max -4.87, n 12) = -7.08 m MSL; toe/seabed points -3.99 to -5.62; reef NOT visible in the DTM; EMODnet minus model seabed = -1.8 +- 0.7 m over 7 cells (reef cell -1.39)", "source_surveys": "CDI 117452, EDMO 2607 OceanWise Ltd (UKHO-derived); QI horizontal 3, vertical 4 (MBES >100 kHz), age 1 (10-30 y), purpose 3; survey about 2011-2012 inferred (not stated by the services; the CDI page is behind a bot check); CDI polygons Poole Bay Blocks 14-17 / Block 12", "useful_for": "datum frame (LAT) and the offshore seabed gradient beyond y = 380 m (-1.41 %); validation cross-check; NOT crest, toe, reef height or the seabed under the reef"},
    "borth-coastal-defence-reef": {"covered": true, "resolution_m": "DTM cell 115.8 x 70.6 m; reef cells are interpolation (GEBCO 2024 fill); surveyed cells hold 1 sounding each (about 90 m spacing); nearest high-resolution DTM BY_CHERISH_Wales_14m is 22 km north", "vertical_ref": "LAT for the grid; GEBCO-filled cells nominally LAT (reduction undocumented); MSL-LAT at Borth unverified", "depth_at_reef_m": "-0.18 rel. LAT at the centre of both mounds (interpolated, REST reference GEBCO2024); mounds -0.13 to -0.40; seabed 60 m seaward -1.10", "source_surveys": "CDI 115084, EDMO 2607 OceanWise Ltd; QI horizontal 0 (unknown), vertical 3, age 0 (>30 y), purpose 3; reef cells: GEBCO 2024 fill", "useful_for": "offshore gradient only (-1.1 %, y >= 335 m from the defence line); weak check that the reef sits near LAT; NOT reef depths, crest, toe or beach profile"},
    "narrowneck-gold-coast": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (outside EMODnet; REST 204)"},
    "cables-reef-wa": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (outside EMODnet; REST 204)"},
    "prattes-reef-el-segundo": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (outside EMODnet; REST 204)"},
    "mount-maunganui-reef": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (outside EMODnet; REST 204)"},
    "opunake-reef": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (outside EMODnet; REST 204)"},
    "kovalam-reef-india": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (outside EMODnet; REST 204)"},
    "palm-beach-gold-coast": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (outside EMODnet; REST 204)"},
    "southern-ocean-surf-reef-albany": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (outside EMODnet; REST 204)"},
    "burkitts-reef-bargara": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (outside EMODnet; REST 204; card latitude sign corrected to 24.8205 S)"},
    "bunbury-airwave": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (outside EMODnet; REST 204)"},
    "mexico-reef-2026-unnamed": {"covered": false, "resolution_m": "n/a", "vertical_ref": "n/a", "depth_at_reef_m": "n/a", "source_surveys": "n/a", "useful_for": "nothing (no coordinate in any verified source; Pacific Mexico is outside EMODnet)"}
  },
  "endpoints": [
    "https://emodnet.ec.europa.eu/geoviewer/ (own headless Chrome; ?layers=<ids>&basemap=<id>&bounds=<EPSG:3857>&filters=&projection=EPSG:3857; layers 14159 mean depth, 13012 source references; config at /geoviewer/config.php?legacybaselayers=1)",
    "https://rest.emodnet-bathymetry.eu/depth_sample?geom=POINT(lon lat)",
    "https://rest.emodnet-bathymetry.eu/depth_profile?geom=LINESTRING(lon lat,lon lat)",
    "https://erddap.emodnet.eu/erddap/griddap/bathymetry_dtm_2024.csv?elevation[(lat0):(lat1)][(lon0):(lon1)],value_count[...],cdi_index[...],interpolation_flag[...],elevation_min[...],elevation_max[...],stdev[...]",
    "https://ows.emodnet-bathymetry.eu/wcs?service=WCS&version=2.0.1&request=GetCoverage&coverageId=emodnet__mean[_2022|_2020|_2018]&format=image/tiff&subset=Lat(a,b)&subset=Long(c,d)",
    "https://ows.emodnet-bathymetry.eu/wfs typeNames=emodnet:source_references (cql_filter release='2024' AND INTERSECTS/BBOX)",
    "https://ows.emodnet-bathymetry.eu/wfs typeNames=emodnet:quality_index",
    "https://ows.emodnet-bathymetry.eu/wfs typeNames=emodnet:hr_bathymetry_area",
    "https://ows.emodnet-bathymetry.eu/wms?service=WMS&request=GetCapabilities&version=1.3.0",
    "http://geo-service.maris.nl/emodnet_bathymetry/wfs typeNames=emodnet_bathymetry:polygons (plain HTTP only)",
    "https://emodnet.ec.europa.eu/geonetwork/srv/api/records/<uuid>/formatters/xml (DTM 2024 cf51df64-56f9-4a99-b1aa-36b8d7b743a1; QI 6572ee07-a078-4adc-b868-fd1f7084c660; HI 1366 6d906048-5195-4f53-90d0-4d17807117b1)",
    "https://emodnet.ec.europa.eu/en/terms-use-emodnet-online-services-data-and-data-products (licence CC BY 4.0)"
  ],
  "haifa_coverage": "Covered by the same 1/16 arc-minute DTM (cells about 115.8 x 97.4 m at 32.8 N), but the cells at the Haifa shore and 1 km off it are interpolated (composite JOINT_ISRAEL_NBS_QUARTMIN_GEO, 1/4 arc-min); real survey data (IOLR-GEO-EEZ-2012-1 multibeam) exist only offshore; no high-resolution DTM within 900 km.",
  "images_registered": [
    "boscombe-surf-reef-img-25 - 07_scale/bathymetry/emodnet/viewer/boscombe-surf-reef_viewer_dtm_raw.png (annotated: ..._dtm_annotated.png) - EMODnet Map Viewer at Boscombe: DTM 2024 mean depth over Esri imagery with cell grid, outline, points, profile",
    "boscombe-surf-reef-img-26 - 07_scale/bathymetry/emodnet/viewer/boscombe-surf-reef_viewer_sources_raw.png (annotated: ..._sources_annotated.png) - EMODnet source-references layer at Boscombe (survey patch CDI 117452)",
    "boscombe-surf-reef-img-27 - 07_scale/bathymetry/emodnet/figures/boscombe-surf-reef_profile_emodnet_vs_model.png - shore-normal profile, EMODnet cells vs project model",
    "boscombe-surf-reef-img-28 - 07_scale/bathymetry/emodnet/figures/boscombe-surf-reef_cells_emodnet_vs_model.png - EMODnet cell means vs model over the same cell footprints",
    "boscombe-surf-reef-img-29 - 07_scale/bathymetry/emodnet/figures/boscombe-surf-reef_dtm_release_history.png - DTM cells along the profile, releases 2018/2020/2022/2024",
    "borth-coastal-defence-reef-img-14 - 07_scale/bathymetry/emodnet/viewer/borth-coastal-defence-reef_viewer_dtm_raw.png (annotated: ..._dtm_annotated.png) - EMODnet Map Viewer at Borth: DTM 2024 with cell grid, both mounds, points, profile",
    "borth-coastal-defence-reef-img-15 - 07_scale/bathymetry/emodnet/viewer/borth-coastal-defence-reef_viewer_sources_raw.png (annotated: ..._sources_annotated.png) - EMODnet source-references layer at Borth (CDI 115084 patch)",
    "borth-coastal-defence-reef-img-16 - 07_scale/bathymetry/emodnet/figures/borth-coastal-defence-reef_profile_emodnet.png - EMODnet cells along three shore-normal lines through the Borth mounds"
  ],
  "report_md_status": "NOT WRITTEN: the harness refused the Write call for a report file; full text is in section B of this message. Save as C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/bathymetry/emodnet/REPORT.md",
  "files": [
    "07_scale/bathymetry/emodnet/METHOD.md",
    "07_scale/bathymetry/emodnet/REQUESTS_FOR_LIOR.md",
    "07_scale/bathymetry/emodnet/reefs_coords.csv",
    "07_scale/bathymetry/emodnet/data/ (coverage_all_reefs.json, haifa_check.json, hr_areas.json, <slug>_cells_*.csv, <slug>_points_*.csv, <slug>_profile_*.csv, <slug>_results.json, boscombe-surf-reef_cells_emodnet_vs_model.csv, boscombe-surf-reef_comparison_summary.json, boscombe-surf-reef_emodnet_vs_navionics_soundings.csv, boscombe-surf-reef_source_patches_2024_near_reef.geojson)",
    "07_scale/bathymetry/emodnet/scripts/ (make_coords.py, coverage_all.py, cdp.py, extract_site.py, rest_profiles.py, compare_boscombe.py, viewer_lib.py, make_viewer_figures.py, make_plots.py, haifa_check.py, register_images.py)",
    "07_scale/bathymetry/emodnet/viewer/ (boscombe-surf-reef_viewer_{dtm,sources}_{raw,annotated}.png, borth-coastal-defence-reef_viewer_{dtm,sources}_{raw,annotated}.png, *_calibration.json)",
    "07_scale/bathymetry/emodnet/figures/ (boscombe-surf-reef_profile_emodnet_vs_model.png, boscombe-surf-reef_cells_emodnet_vs_model.png, boscombe-surf-reef_dtm_release_history.png, borth-coastal-defence-reef_profile_emodnet.png)",
    "03_images/reefs/boscombe-surf-reef/images.json and IMAGES.md (rows 25-29 appended)",
    "03_images/reefs/borth-coastal-defence-reef/images.json and IMAGES.md (rows 14-16 appended)",
    "03_images/reefs/NEW_IMAGES_LOG.md (8 lines appended)"
  ]
}
```
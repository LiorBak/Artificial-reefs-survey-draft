# Sources - borth-coastal-defence-reef (shape tracing, run 2026-10-05)

All images below are Esri World Imagery (Maxar/Earthstar) tiles fetched with 07_scale/tools/satellite.py on 2026-10-04 (earlier run) and kept as a PRIVATE RESEARCH COPY. Reuse rights (Esri / Maxar licence) must be checked before any public release. Each file has a .geo.json sidecar with exact Web-Mercator bounds.

| id | kind | title | url (tile template) | source page | image date | credit | licence | local file | retrieved | role |
|---|---|---|---|---|---|---|---|---|---|---|
| sat2024 | satellite | Esri World Imagery, current layer, Borth reef, z19 r=140 m | https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x} | Esri World Imagery (identify DATE field) | 2024-09-17 (low tide, rock bare) | Esri, Maxar, Earthstar Geographics, GIS User Community | Esri/Maxar terms - check before public use | src/borth_esri_2024-09-17_z19.png | 2026-10-04 | primary |
| sat2022 | satellite | Esri Wayback release 34007, same frame | https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/34007/{z}/{y}/{x} | Esri Wayback | 2022-08-25 (low tide, rock bare) | as above | as above | src/borth_esri_2022-08-25_z19.png | 2026-10-04 | cross_check |
| sat2012 | satellite | Esri Wayback release 18358, same frame | .../tile/18358/{z}/{y}/{x} (Wayback WMTS) | Esri Wayback | 2012-10-27 (reef awash, algae covered; ~7 months after completion) | as above | as above | src/borth_esri_2012-10-27_z19.png | 2026-10-04 | cross_check (as-built state) |
| sat2013 | satellite | Esri Wayback release 11351, same frame | .../tile/11351/{z}/{y}/{x} (Wayback WMTS) | Esri Wayback | 2013-06-04 | as above | as above | src/borth_esri_2013-06-04_z19.png | 2026-10-04 | context (not traced) |
| satshore | satellite | Esri World Imagery current, Borth frontage, z19 r=350 m | current layer tile template | Esri World Imagery | 2024-09-17 | as above | as above | src/borth_shoreline_z19.png | 2026-10-04 | context: shoreline / offshore distance |
| satblobs | satellite | Esri World Imagery current, wider frame around the reef, z19 r=250 m | current layer tile template | Esri World Imagery | 2024-09-17 | as above | as above | src/borth_blobs_z19.png | 2026-10-04 | context (duplicate date of sat2024) |

Deleted (not used): borth_current_z18 (wrong area, cliffs 1.7 km S), borth_wide_z17 (context only), borth_esri_2017-05-09 (cloud cover), borth_esri_2020-03-26 (low contrast, reef partly submerged/spray).


## Registry ids (added 2026-10-06, image registry backfill)

Each image above is registered with full citation and 'how used' in 03_images/reefs/borth-coastal-defence-reef/images.json (human-readable: IMAGES.md).

| source id | registry id |
|---|---|
| sat2024 | borth-coastal-defence-reef-img-08 |
| sat2022 | borth-coastal-defence-reef-img-09 |
| sat2012 | borth-coastal-defence-reef-img-10 |
| sat2013 | borth-coastal-defence-reef-img-11 |
| satshore | borth-coastal-defence-reef-img-12 |
| satblobs | borth-coastal-defence-reef-img-13 |

## Added by the verifier (2026-10-06)
| id | kind | title | url | image date | credit / licence | local file | registry id | role |
|---|---|---|---|---|---|---|---|---|
| drg1020 | design_drawing | Royal Haskoning DRG 9V5090/1020 rev C1 Multi-Purpose Reef Plan, 1:500 (For Construction) | http://www.borthcommunity.info/images/default_images/CoastalDefences/PlanningDrawings/9v5090%201020_rev%20c1.pdf | 2010-05 (rev C1 2011-01) | Royal Haskoning / Ceredigion CC; no licence stated, private research copy | src/borth_rh-drg-9V5090-1020_multipurpose-reef-plan_2010.png (+ .pdf) | borth-coastal-defence-reef-img-20 | cross_check (georeferenced by 15 setting-out points) |
| drg1021 | design_drawing | DRG 9V5090/1021 Northern Reef Sections 1/2 (N1-N3) | same folder, 9v5090%201021_rev%20c1.pdf | 2010-10 | as above | src/borth_rh-drg-9V5090-1021_northern-reef-sections-1_2010.png | -img-21 | context, 3D inputs |
| drg1022 | design_drawing | DRG 9V5090/1022 Northern Reef Sections 2/2 (N4-N6) | 9v5090%201022_rev%20c1.pdf | 2010-10 | as above | src/..._1022_northern-reef-sections-2_2010.png | -img-22 | context, 3D inputs |
| drg1023 | design_drawing | DRG 9V5090/1023 Southern Reef Sections (S1, S2) | 9v5090%201023_rev%20c1.pdf | 2010-09 | as above | src/..._1023_southern-reef-sections_2010.png | -img-23 | context, 3D inputs |
| drg1001 | design_drawing | DRG 9V5090/1001 General Arrangement 1:2000 | 9v5090%201001_rev%20c1.pdf | 2010-09 | as above | src/..._1001_general-arrangement_2010.png | -img-19 | context |
| hrpp576f2 / f3 | paper_figure | HRPP576 Figs 2 and 3 (Rigden et al. 2013) | https://eprints.hrwallingford.com/931/1/HRPP576_SurfReefs.pdf | pre-construction | HR Wallingford; open eprint | 03_images/reefs/borth-coastal-defence-reef/..._hrpp576-fig2-..._2013.png / ..._fig3-... (PDF in src/) | -img-17 / -img-18 | context (design history, seabed contours) |
| lidar2022 | other | Welsh Government LiDAR 1 m DSM tile SN6089, 2022-03-19; our map + sections | https://dmwproductionblob.blob.core.windows.net/lidar-zips/2020-22/dsm/wg_del_29_260289_20220319dsm.tif (not kept) | 2022-03-19 | Welsh Government, OGL v3 | overlays/verify_lidar_dsm_2022-03-19_sections.png | -img-24 | cross_check, 3D inputs |
Also new in overlays/: verify_trace_sat2024/2022/2012.png (re-rendered traces, annotated versions of img-08/09/10) and verify_design_lidar_vs_trace_sat2024.png (img-25).

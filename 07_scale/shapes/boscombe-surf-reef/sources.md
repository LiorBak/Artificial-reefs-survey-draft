# sources.md - boscombe-surf-reef (images saved in src/)

PRIVATE RESEARCH COPIES. Reuse rights must be checked before any public release (Esri World Imagery / Maxar terms: attribution required, redistribution restricted; the two conference-paper figures are the authors' copyright - link/research copy only).

| id | kind | title | url | source page | page / figure | image date | credit | license | retrieved | role | local file |
|---|---|---|---|---|---|---|---|---|---|---|---|
| img1 | satellite | Esri World Imagery Wayback release 10 - wide crop (pier + groynes + reef), 800 m box centred 50.7185 N 1.8417 W, zoom 18, 2116x2116 px | https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/10/{z}/{y}/{x} | Esri Wayback (https://livingatlas.arcgis.com/wayback/) | z18 tiles stitched with 07_scale/tools/satellite.py | 2011-09-28 (SRC_DATE2 of the release-10 metadata layer at the crop centre) | Esri, Maxar, Earthstar Geographics, and the GIS User Community | Esri/Maxar imagery terms - not cleared for public reuse | 2026-10-04 | PRIMARY (traced) | src/esri_wayback10_2011-09-28_z18_wide.png (+ .geo.json) |
| img2 | paper_figure | Rendle & Davidson (2012), "An evaluation of the physical impact and structural integrity of a geotextile surf reef" - Fig. 9 (left panel): April 2011 bathymetry of the reef, colour-coded depth with Eastings/Northings gridlines (OSGB36) | https://icce-ojs-tamu.tdl.org/icce/article/download/6794/pdf_441/27535 | https://icce-ojs-tamu.tdl.org/icce/article/view/6794 (Coastal Engineering Proceedings 2012, Univ. of Plymouth) | PDF p.7, Figure 9 (embedded image 998x580); left panel cropped and y-stretched x1.749 to equal axis scales; calibration in the .geo.json | survey April 2011 (Channel Coast Observatory / Bournemouth Borough Council DGPS bathymetry) | Rendle & Davidson, Plymouth University; survey data CCO / BBC | Conference paper, open PDF; figure copyright of the authors - research copy only | 2026-10-05 | cross_check (traced; independent geo-referenced survey plan) | src/rendle_davidson_2012_fig9_bathymetry_apr2011_native.png ; src/rendle_davidson_2012_fig9_left_isotropic.png (+ .geo.json) |
| img3 | design_drawing | Mead, Blenkinsopp, Moores & Borrero (2010), "Design and construction of the Boscombe multi-purpose reef" - Fig. 3(a): numerical-model design shape of the reef (depth plan with metric axes and a 0.05 km scale bar; 'focus' and 'wedge' sections) | https://icce-ojs-tamu.tdl.org/icce/index.php/icce/article/download/1352/pdf_106/ | https://icce-ojs-tamu.tdl.org/icce/ (Coastal Engineering Proceedings 2010, article 1352; authors are ASR Ltd, the reef designers) | PDF p.3, Figure 3(a) (embedded image 871x617); 3(b) layout schematic and 3(c) Google-Earth overlay not traced | design stage (published 2010; designed 2006-2008, before construction) | Mead et al., ASR Ltd / UNSW-WRL | Conference paper, open PDF; figure copyright of the authors - research copy only | 2026-10-05 | cross_check (traced; DESIGN shape, not as-built) | src/mead_et_al_2010_fig3a_design_bathymetry.png (+ .geo.json) |
| img4 | satellite | Esri World Imagery current (MapServer), 400 m box centred 50.7175 N 1.8388 W, zoom 19, 2116x2116 px | https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x} | Esri World Imagery | z19 tiles stitched with satellite.py | 2025-06-15 (DATE field of the identify operation) | Esri, Maxar, Earthstar Geographics, and the GIS User Community | Esri/Maxar imagery terms - not cleared for public reuse | 2026-10-04 | context (blurred dark patch; the img1 outline, projected by lat/lon, fits it; not independently traced) | src/esri_current_2025-06-15_z19.png (+ .geo.json) |

## Looked at but not saved (links only)
- YouTube 0Oi6D6Xp0oY "Aerial view of Boscombe Reef" (BoscombeReef channel, 2009): oblique helicopter view, no scale -> context only.
- Raised Water Research "Boscombe-Arial" and "Boscombe-From-Above" (credit Bournemouth Echo): oblique / no scale -> context only.
- Rendle & Davidson 2012 Fig. 1 (oblique aerial 2009) and Mead et al. 2010 Figs 3(b), 3(c), 7, 9: oblique photographs, schematics or small overlays -> context only.

## Images downloaded, looked at, then DELETED
- Esri Wayback releases 15423 (2017-06-20), 48376 (2020-05-07), 16245 (2021-09-06), 57965 (2022-08-26), 60013 (2023-09-03): reef not visible / not traceable (wave glint or near-black water).
- Esri 2025 z18 wide crop (duplicate imagery of img4) and the 500 m tight crop of the 2011 imagery (duplicate imagery of img1).


## Verifier note 2026-10-05
No new images were saved. Text sources used for the dimension check (Wikipedia, Raised Water Research, Herbert et al. 2017, council releases of 12 Aug and 24 Oct 2011, BBC 15 Aug 2011) are listed in shape.json references. Overlays added: overlays/img1_verify_closeup.png, overlays/img3_relief_footprint_verify.png (derived from img1 and img3; same private-research-copy status). overlays/img1_outline_on_2025.png was re-rendered.

## Registry ids (added 2026-10-06, image registry backfill)

Every image is registered with full citation and 'how used' in 03_images/reefs/boscombe-surf-reef/images.json (IMAGES.md).

| source id | registry id |
|---|---|
| img1 | boscombe-surf-reef-img-08 |
| img2 (left, traced) | boscombe-surf-reef-img-10 |
| img2 (whole figure) | boscombe-surf-reef-img-09 |
| img3 | boscombe-surf-reef-img-11 |
| img4 | boscombe-surf-reef-img-12 |

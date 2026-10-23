# sources.md - cables-reef-wa (rows added as images are saved to src\)
Private research copies only. Reuse rights must be checked before any public release.

| id | kind | title | url | source page | page/figure | image date | credit | license | retrieved | role | local file |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | paper_figure | Pattiaratchi C., "Design Studies for an Artificial Surfing Reef: Cable Station, Western Australia", Centre for Water Research UWA ref ED1483CP (5-page PDF) | http://joas.free.fr/studies/bei/g2s/reefdesign.pdf (mirror; byte-identical re-download 2026-10-05, MD5 02a6075b...) | same | whole paper; Fig 1 p2, Fig 3-4 p3, Fig 5-7 p4 | 1999 (PDF created 1999-04-13; construction started Feb 1999) | C. Pattiaratchi / Centre for Water Research, UWA | unknown / all rights reserved - private research copy | 2026-10-04 (earlier run), re-verified 2026-10-05 | primary candidate (design drawing, Figs 4 and 7) | src/S1_pattiaratchi_reefdesign.pdf ; page renders src/S1_fig1_sitemap_full_page.png, S1_fig4_wavebasin_full_page.png, S1_fig7_location_map.png |

## Registry ids (added 2026-10-06, image registry backfill)

Every image is registered in 03_images/reefs/cables-reef-wa/images.json (IMAGES.md); the paper's native figure extracts and the RWR page images are in 03_images/reefs/cables-reef-wa/.

| source id | registry id |
|---|---|
| S1 page render S1_fig1_sitemap_full_page.png | cables-reef-wa-img-21 |
| S1 page render S1_fig4_wavebasin_full_page.png | cables-reef-wa-img-22 |
| S1 page render S1_fig7_location_map.png | cables-reef-wa-img-23 |

## Added 2026-10-10 (fresh-agent run) - sources used for the trace and the 3D model
All are registered in 03_images/reefs/cables-reef-wa/images.json (registry id in the second column). Roles as in shape.json.
| shape.json id | registry id | what | role | url / location |
|---|---|---|---|---|
| img26 | cables-reef-wa-img-26 | Blacka et al. (2013) WRL TR 2012/08, Fig A.2 p.93 (PDF p.105): 'Cable Station ASR Design (After Lyons, 1992)', 917 x 682 px, legible labels | PRIMARY (traced, scale from printed dimensions) | https://doi.org/10.4225/53/58e1dc7368c7a ; Lior's copy papers/Review of artificial reefs for coastal protection in NSW 2013.pdf |
| img05 | cables-reef-wa-img-05 | RWR 'Cables Design' ('The original design'): the same drawing at 478 px, labels illegible | independent re-trace (assumed scale) | https://raisedwaterresearch.com/wp-content/uploads/2019/11/Cables-Design.jpg |
| img06 | cables-reef-wa-img-06 | RWR 'Cables Additional Fill Area' ('The extension to the right'): triangle, text 'VOLUME = 320 m3' | extension triangle | https://raisedwaterresearch.com/wp-content/uploads/2019/11/Cables-Additional-Fill-Area.jpg |
| img07 | cables-reef-wa-img-07 | RWR 'Cables Drawing' (Image: Pitt): proposal plan, scale bar, contours 3.0-7.0 m | concept version; bed gradient; scale bar | https://raisedwaterresearch.com/wp-content/uploads/2019/11/Cables-Drawing.jpg |
| img20 | cables-reef-wa-img-20 (-23 upscale) | Pattiaratchi (1999) Fig 7 (native raster, printed rotated) | cross-check; orientation; 270 m offshore | http://joas.free.fr/studies/bei/g2s/reefdesign.pdf |
| S1 | img-15/16/17/20/23 | Pattiaratchi (1999) paper text (3 m contour extended offshore, 1:20 slope to the 1 m contour, peel angle 45 deg, MTL 0.78 m above datum, 250 m offshore) | text source | same PDF |
| P8 text | - | Blacka (2013) A.1.1-A.1.5, Tables 4.2-4.4: 140 x 70 m, crest submergence 1.0-2.5 m, water depth 3.0-6.0 m, 275 m, 5,500 m3, tide range 0.8 m | text source | same DOI |
Our overlays (annotated copies) are in overlays/ and 3d/annotated/ and are registered as annotated_files / own-figure rows. Image dates: RWR drawings are undated (1990s); the Lyons design is 1992 (reproduced 2013); paper 1999-04-13. Licences: none stated, private research copies only.

## Added 2026-10-10 (imagery + bathymetry run)
| source id | registry id | what | role | url / location |
|---|---|---|---|---|
| DoT1999 | - (data; figure img-38) | DoT WA single-beam soundings FR19991122_Single.txt, 840 pts, survey end 22 Nov 1999, m AHD, GDA94 / MGA 50 | georeference (fit), default 3D surface | https://s3-ap-southeast-2.amazonaws.com/transport.wa/Bathymetry/PointData/FR.zip ; src/bathymetry/ |
| DoT1998 | - | FR19980330_Reef_Single.txt, 14,303 pts, 30 Mar 1998 (pre-construction) | measured bed | same |
| DoT2002 | - (figure img-39) | FR20020201_Single.txt, 8,373 pts, 1 Feb 2002 | second surveyed surface; extension test | same |
| DoT5m | - (figure img-40) | Perth_5m.tif composite, 5 m, AHD; clip kept | bed beyond the survey, shoreline | https://s3-ap-southeast-2.amazonaws.com/transport.wa/Bathymetry/Rasters/Perth_5m.tif ; src/bathymetry/DoT_Perth_5m_clip_reef.npz |
| SAT | img-32..36 (overlays img-37) | Esri World Imagery z19, current + 4 Wayback releases | independent check | https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer ; src/imagery/ |
| BoM | - | NTC 62230 Fremantle metadata sheet and monthly sea levels | datum evidence | https://www.bom.gov.au/ntc/IDO50000/IDO50000_62230.pdf ; src/datum/ |
Licences: DoT data CC BY 4.0; Esri imagery under Esri / Maxar terms (private research copy). Dead ends: 02_research/dead_ends/cables-reef-wa.json.

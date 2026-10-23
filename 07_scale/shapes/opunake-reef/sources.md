# sources.md - opunake-reef (2026-10-10)

Images (all private research copies; reuse rights not cleared). Registry ids in 03_images/reefs/opunake-reef/images.json.

| id | kind | title | url / tile | page/figure | image date | credit | licence | retrieved | local file | registry | role |
|---|---|---|---|---|---|---|---|---|---|---|---|
| sat_z20 | satellite | Esri World Imagery z20, centre -39.4577, 173.8545, r 250 m | https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x} | tiles z20, 4338 px, 0.115 m/px | 2025-01-16 (capture date field) | Esri, Maxar, Earthstar Geographics, GIS User Community | Esri terms (not stated as open) | 2026-10-04 | 07_scale/shapes/opunake-reef/src/opunake_sat_z20.png | opunake-reef-img-10 | context (reef not visible) |
| sat_mid | satellite | same service, mid zoom | same | - | see .geo.json | same | same | 2026-10-04 | src/opunake_sat_mid.png | img-08 | context |
| sat_wide | satellite | same, wide | same | - | see .geo.json | same | same | 2026-10-04 | src/opunake_sat_wide.png | img-09 | context |
| sat_current | satellite | same, "current" | same | - | see .geo.json | same | same | 2026-10-04 | src/opunake_sat_current.png | img-07 | context |
| ov_search | overlay | our annotation of sat_z20 (scale bar + negative finding) | - | - | made 2026-10-10 | this project | private | 2026-10-10 | overlays/search_frame_z20_no_structure.png | annotated_files of img-10 | documentation |

Text sources (card references, not re-fetched; network blocked): R1 Newsroom 2021-12-06; R2 Raised Water Research Opunake; R3 NZ Geographic 078 (2006); R4 SurferToday; R9 ResearchGate 273133845 (snippet only). Values taken: footprint ~90 x 20 m, 27 bags (2009), single right-hand wave design. No coordinates, bearing, depth or volume with a datum.

## Search log 2026-10-10 (item 9b: local papers, Gemini extracts, WebSearch). Result: NO plan source.
Local papers/ (PyMuPDF text layer, grep Opunake; WebFetch/download unavailable):
| paper (file in papers/) | Opunake pages (PDF) | content |
|---|---|---|
| Mead & Borrero (2011) Multi-Purpose Reefs - A Decade of Applications | 1 (Fig 1 world map), 3-4 (3.1.5) | 4,800 m3, start 2006, last work May 2008, 1,400 m3 short, no drawing |
| Rendle (2016) PhD thesis, Univ. Plymouth, 343 pp | 41 (Table 2.1), 298 (refs) | 4,800 m3, A$760,000, "not officially completed"; cites TRC (2009) monitoring report. No Opunake figure |
| Blacka et al. (2013) Review of artificial reefs for coastal protection in NSW, WRL | 75, 77, 79, 81, 102 | Tables 4.1-4.4: 30 m x 100 m, depth 1.8-3.0 m, ~300 m offshore, "At LAT", tide >3.0 m, A$0.93M; ref list TRC (2009) Tech. Rep. 2009-33. No plan |
| Mount Maunganui 2007 (6 pp, 1,404 chars text; mostly scanned) | none in text layer | image-only pages not OCR'd (tesseract not installed, no installs allowed); title says Mount Maunganui, not expected to cover Opunake |
| Narrowneck Renewal 2023 (7 pp) | none | - |
Gemini extracts (06_gemini_compare/02_gemini_extract.*, README; 07_scale/00_gemini_footprints_extract.*): only Gemini's own Opunake polygon (dimensions 80 x 30 m, polygon 30 x 67 m, inverted, per its own audit; our card 90 x 20 m) and three unverifiable/fabricated quotes. No original source cited that we could confirm. NOT used.
WebSearch (standard unless noted), all 2026-10-10; none returned a plan, coordinates, crest datum or survey:
1. "Opunake surfing reef geotextile bags plan drawing dimensions crest depth Black ASR" -> raisedwaterresearch.com/?p=3339, artificialreefs.org Stuff article (2009), theinertia.com/?p=261061, geosyntheticsmagazine.com; text only (90 x 20 m, 1.5-2 m high bags, 27 bags 2009).
2. "Opunake artificial reef monitoring programme Taranaki Regional Council Technical Report 2009-33 ..." -> report itself not found online.
3. "Black Mead Opunake surfing reef resource consent studies 2004 ..." -> nothing on the 2004 study; TRC hits were Opunake Power hydro consents (unrelated).
4. "Opunake surf reef aerial photo bags visible offshore ... coordinates" -> surf-forecast, tourism pages; no aerial of the bags.
5. "Mead Black Opunake reef design ... Coasts and Ports OR ..." -> nzgeo.com/stories/artificial-surf-reefs-coming-to-a-beach-near-you/ (R3, text), newsroom.co.nz (R1), ICCE tdl.org downloads (general surfing-reef papers, not Opunake).
6. "trc.govt.nz Opunake artificial reef monitoring report bathymetry ..." -> none from TRC.
7. "icce-ojs-tamu.tdl.org article 8509 ... Opunake" -> no Opunake paper.
8. "researchcommons.waikato.ac.nz 10289/12221 Opunake" -> handle not identified.
9. (extended) "Opunake Artificial Surf Reef Trust STDC reef survey plan crest chart datum bags layout" -> stuff.co.nz/taranaki-daily-news/news/5456452/Money-for-surf-reef-a-wipeout (NZ$400k write-off), surfertoday, ausleisure ASR liquidation; text only.
Candidate leads found (not fetched; downloads blocked): https://www.stuff.co.nz/taranaki-daily-news/news/5456452/Money-for-surf-reef-a-wipeout ; https://www.ausleisure.com.au/news/asr-liquidation-cast-doubts-over-future-of-artificial-surf-reefs ; https://geosyntheticsmagazine.com/2023/06/07/why-have-most-geotextile-artificial-reefs-never-really-worked/ . None expected to hold a plan.

## Network pass 2026-10-10 (all private research copies; reuse rights not cleared; none shows the reef)
| id | kind | title / tile | url | image date | credit / licence | local file | registry | role |
|---|---|---|---|---|---|---|---|---|
| L1 | aerial | LINZ Taranaki 0.4 m rural aerials 2011-2012, tile BJ28_5000_0806 (crop 1 km, 0.4 m/px) | https://nz-imagery.s3.ap-southeast-2.amazonaws.com/taranaki/taranaki_2011-2012_0.4m/rgb/2193/BJ28_5000_0806.tiff | flown 2011-11-30 to 2012-03-30 | LINZ / NZ Aerial Mapping / Taranaki Regional Consortium, CC BY 4.0 | src/linz_aerial_2011-12_0.4m_crop.png (+.geo.json) | img-11 | search; structure not visible |
| L2 | aerial | LINZ Taranaki 0.25 m rural aerials 2021-2022, same tile (crop 1 km, 0.25 m/px; JPEG q93) | .../taranaki_2021-2022_0.25m/rgb/2193/BJ28_5000_0806.tiff | flown 2021-11-23 to 2022-01-07 | LINZ / Aerial Surveys / TRC, CC BY 4.0 | src/linz_aerial_2021-22_0.25m_crop.jpg (+.geo.json) | img-12 | search; structure not visible |
| W1-W4 | satellite | Esri Wayback releases 2015-08-19, 2019-05-15, 2023-08-31, 2024-05-09, z19 9 x 9 tile mosaics | https://wayback.maptiles.arcgis.com (config s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json) | release dates (capture dates not retrieved) | Esri / Maxar / Earthstar | src/esri_wayback_<date>_z19.png (+.geo.json) | img-13 to img-16 | search; structure not visible |

Other LINZ imagery for Taranaki exists (1976-2002 film scans, 2016-18 0.3 m, 2022-23 0.1 m / 0.05 m urban) but its tiles for this site were not found or are other tile schemes; the 2022-23 0.1 m set has BJ28_500_* tiles (not fetched: same cove, later than L2).

### Search log (network pass 2026-10-10)
- LINZ Basemaps tiles need an API key; not used (a key seen in the data.linz.govt.nz page source belongs to that site and was not borrowed). LINZ open imagery read from the public AWS bucket instead (no login).
- data.linz.govt.nz chart/bathymetry layers need login/export key: not used. AWS nz-coastal / nz-elevation buckets hold no Opunake bathymetry (coastal LiDAR only Awakino and Urenui-Oakura 2025; land DEM 2021).
- Esri Wayback: 197 releases scanned at z19 tile 515337/324775; 173 have a tile here, 4 distinct versions (2015-08-19, 2019-05-15, 2023-08-31, 2024-05-09).
- Raised Water Research Opunake page: fetched with curl (the 3 gallery images were already registered as img-01..06 era files); text facts added to the card.
- NZ Geographic (nzgeo.com, ?p=5057), Taranaki Regional Council (trc.govt.nz) pages: HTTP 403 Cloudflare challenge; not bypassed. WebSearch for TRC Technical Report 2009-33, STDC consent plan, Black et al. 2004: nothing openly available. ResearchGate skipped (login).

Wayback capture dates (Esri metadata service query, 2026-10-10): 2015-08-19 release - none returned; 2019-05-15 - Taranaki Rural 2018 (0.3 m, 2018-01-01 nominal); 2023-08-31 - TRC 2021 (0.25 m, 2021-11-24, same flight as L2); 2024-05-09 - TRC 2022 (0.1 m, 2022-12-28). The 2022-12 0.1 m image is not in the open LINZ BJ28_5000 set fetched here.

## New sources 2026-10-13 (Lior's uploads P15 and P16; all images private research copies, reuse rights not cleared)
Citation of P15: Taranaki Regional Council (2009). Opunake Artificial Reef Monitoring Programme 2005-2009. Technical Report 2009-33 (ISSN 0114-8184 print; 1178-1467 online; document 631513). Stratford, NZ, September 2009. 58 pp. (PDF metadata title '09-33 Opunake Artificial Reef Monitoring Programme 2005-2009.pdf', created 2009-08-30.) File: `new uploads from lior/Opunake Artificial Reef monitoring programme 2005-2009.pdf`. Page numbers below: printed page (PDF page = printed + 6; Appendix pages are unnumbered, PDF page given).
Citation of P16: Moores, A. (2006). Artificial surf reefs - coming to a beach near you. New Zealand Geographic (Geo News; issue 078, Mar-Apr 2006 per card R3, not shown on the print; year 2006 follows from the text: Mount Maunganui started Oct 2005, Opunake 'slated for March this year'). https://www.nzgeo.com/stories/artificial-surf-reefs-coming-to-a-beach-near-you/ . Lior's print to PDF 2026-10-11: `new uploads from lior/New Zyland Geographic.pdf` (6 pp., no text layer; OCR in 05_qa/papers_intake/nzgeo_moores_2006_artificial_surf_reefs_ocr.md). Issue and date could not be confirmed (nzgeo.com not reachable here; WebSearch 2026-10-13 did not show them).
| id | kind | what | location | registry | role |
|---|---|---|---|---|---|
| c6376 | scan of consent text | Coastal Permit 6376-1 'to occupy an area ... defined by the Taranaki local circuit grid co-ordinates' | TRC 2009-33 Appendix I, PDF p. 39 (crop src/trc2009-33_p39_consent6376-1_occupation_area_coordinates.png) | img-24 | PRIMARY for position: 4 corner co-ordinates |
| fig1 | report figure | aerial with white rectangle 'Proposed location of surf reef', orange 'Area of water to be used during the construction process', boat ramp, groyne | TRC 2009-33 printed p. 3 (PDF p. 9), Figure 1; src/trc2009-33_fig1_p9_reef_location.png (+ .geo.json) | img-17 | georeferenced on the consent corners; position check |
| fig2 | report figure | survey sites + hatched 'Approximate location of artificial reef' | printed p. 10 (PDF p. 16), Figure 2; src/trc2009-33_fig2_p16_survey_sites.png | img-18 | context only (schematic) |
| ph1 | report photo | geo-textile bags awaiting deployment | printed p. 4 (PDF p. 10), Photograph 1 | img-19 | context |
| ph2 | report photo | Trust construction sign, works period Feb 2007 - May 200? (blurred, read 2008) | printed p. 5 (PDF p. 11), Photograph 2 | img-20 | context (dates) |
| ph4, ph5 | report photos | sand slurry pipe on buoys; pumping equipment | printed p. 9 (PDF p. 15), Photographs 4, 5 | img-21, img-22 | context (method) |
| ph7 | report photo | Opunake Bay 2 intertidal monitoring site | printed p. 14 (PDF p. 20), Photograph 7 | img-23 | context (shore) |
| nzg_hero | photo in the NZ Geographic print | aerial of a pumping barge; no caption, site not stated (probably Mount Maunganui) | print p. 1, src/nzgeo_moores2006_p1_hero_sand_pumping_aerial.png | img-25 | context; NOT Opunake geometry |
| trc_text | text | reef description, depths, volume, bags, dates; consent conditions | TRC 2009-33 printed pp. 3-7 (PDF pp. 9-13) and Appendix I PDF pp. 33-37 (consent 6377-1 conditions 3, 9, 10, 15) | - | PRIMARY for size, depth, state |
| nzg_text | text | north reef cost about NZ$1.3 m, waves 1.8-2.5 m, 100 m ride, south reef 200 m / 3.6 m, 'March this year' | NZ Geographic print pp. 3-4 (OCR) | - | context |
| dm2004 | web page | 'Surf reef decision has Opunake buzzing at tourism prospects', The Daily News, 11 June 2004: bags 1.5-2 m high, about 90 m x 20 m, slight hook, NZ$1.1 m | https://artificialreefs.org/Articles/STUFF%20%20TRAVEL%20%20IN%20NEW%20ZEALAND%20-%20STORY%20%20New%20Zealand's%20leading%20news%20and%20information%20website.htm (curl 200, 2026-10-13; author not printed) | - | origin of the '90 x 20 m' figure |
| ov_fig1 | overlay | Fig 1 (50 percent) warped onto Esri 2025-01-16 with the consent polygon | overlays/fig1_georef_check_on_esri2025.png | annotated_files of img-17 | documentation |
| ov_cons | overlay | consent polygon (yellow) and assumed 99 x 30 m rectangle (red) on LINZ 2011-12 | overlays/consent_area_and_envelope_on_linz2011-12.png | annotated_files of img-17 | documentation |
Other data: LINZ grid nz_linz_nzgd2kgrid0005.tif (NZGD49 to NZGD2000, 0.2 m; https://cdn.proj.org/nz_linz_nzgd2kgrid0005.tif, LINZ open licence CC BY 4.0, downloaded 2026-10-13, 197 KB) kept in scripts/proj_grid/. Esri World Imagery z18 frame (capture 2025-01-16, fetched 2026-10-13 with 07_scale/tools/satellite.py, 23 MB) used only in scratch for the overlay and the ramp landmark; not saved in the repo (re-fetch: `satellite.py fetch --lat -39.4594 --lon 173.8510 --radius-m 800 --zoom 18`).
Search log 2026-10-13: WebSearch x3 (TRC post-construction dive survey / monitoring 2010; NZ Geographic issue 078; 'Opunake Reef Construction Manual' Black and Mead 2006): none found openly. WebFetch cannot resolve nzgeo.com / artificialreefs.org (curl worked for artificialreefs.org). Not bypassed: nzgeo.com and trc.govt.nz (bot checks).

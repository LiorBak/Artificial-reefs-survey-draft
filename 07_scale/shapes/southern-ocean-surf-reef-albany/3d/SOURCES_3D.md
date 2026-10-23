# SOURCES_3D - run log, southern-ocean-surf-reef-albany
Run started 2026-10-10 (fresh agent; network FULL). Source register with "how used": REGISTER_3D.md section 1.

## Steps
1. Read CLAUDE.md, briefs, HANDOFF, FEASIBILITY, source audit. papers/ checked first (5 PDFs, text grep for Albany / Middleton Beach / Bluecoast): nothing.
2. City of Albany pages and documents fetched by curl (browser UA): project page, executive summary of the detailed design report (5 pp.), FAQs 2023, project profile 2024, 2015 feasibility executive summary, information posters, 2016 survey results, 2020 business case. None has seabed depths or sections.
3. EPA WA referral documents found via search (BMT 2018 EIA, 160 pp.): Fig 6.9 has spot soundings in m CD; appendix has regional bathymetry (Fig 29). Saved to src/epa/.
4. Raised Water Research page: gallery images downloaded; the RHDHV 2015 Option B plan with depth contours (Albany-Model2.jpg) found = seabed source.
5. WA DoT / BoM tide predictions 2024 (Albany): statistics (scripts/tides_from_dot.py).
6. Esri Wayback: all 19 releases from 2024-10 to 2026-09 fetched at the site (z18, r 250 m); only three distinct captures exist (2022-12-19, 2025-01-16, 2026-01-20). No construction image.
7. Navionics (maps.garmin.com/en-US/marine) opened in own headless Chrome (random port, fresh profile): page loads, no login or CAPTCHA, but the map pane stays blank (no tile request). Not bypassed. Nothing saved.
8. Geoscience Australia ArcGIS services (AusSeabed holdings): HTTP 403. Not bypassed.
9. Georeferenced the 2015 plan on the Esri 2025-01-16 mosaic, read contour crossings, built profile; georeferenced BMT Fig 6.9 by its UTM grid; built model.

## Annotated images (3d/annotated/)
- A1_rhdhv_2015_contours_read_on_plan.png: the 2015 plan with the georeference control points, the transects and the contour crossings read; design and satellite outlines overlaid. (registry img-16 annotated)
- A2_seabed_profile_and_crest_section.png: profile with the crossing medians and IQR, BMT soundings under both datum readings, section along the crest ridge.
- A3_bmt2018_fig6-9_soundings_georeferenced.png: BMT Fig 6.9 with the soundings read and the outlines overlaid. (registry img-14 annotated)

## Scripts (3d/scripts/)
geo.py (georeference, frame), prof.py + read_contours.py (contour crossings -> src/levels2_raw.json), tides_from_dot.py (-> src/tides_derived.json), make_annotations.py, make_viewer_from_borth.py (viewer derived from the Borth viewer), preview.py (headless screenshots), ../build_3d.py (model.js, docs.js, src/build_metrics.json).

## Run 2026-10-13 (Lior's uploads: Albany FAQ PDF and three Raised Water Research PDFs; live pages)
- Read: Albany FAQ PDF (byte-identical to src/city_docs copy, S8: nothing new); RWR spot, design-2019 and moved-rocks pages (S15-S17; Lior's PDFs are screenshots, text checked against the live pages); live pages and articles S18-S22 (curl through the cloud proxy, no login); GA 2021 holdings file S23 (42 MB; the 69 MB 2019 file was not downloaded: over the 50 MB limit).
- Result: no source gives an as-built level, crest, section or seabed depth, so geometry is unchanged (D11). Corrected: state "completed March 2025" -> placement 18 Mar - June 2025, opened 16 Jul 2025 (A12). New: later changes section (Methods 3.4), three validation rows, A13 (70,000 t sensitivity), D11, D12, full reference list, change log (Methods 9).
- Rebuilt with `python -I build_3d.py`: model.js differs only in two text strings and the added sensitivity key `if_built_70000_t` (checked by diff).
- W8: GA services return 403 and the portal scripts are served as HTML (cannot render); GA's public 2021 holdings file names WA DoT "Middleton Bay & Oyster Harbour" multibeam and laser-scanner surveys. `W8_how_to.png` (lat/lon, point, 5 steps) saved here.

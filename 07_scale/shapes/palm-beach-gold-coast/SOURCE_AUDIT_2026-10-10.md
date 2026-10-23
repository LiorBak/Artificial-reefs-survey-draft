# SOURCE AUDIT 2026-10-10 - palm-beach-gold-coast (shape, 3D model, viewer, image registry)

Standard: `_agent_briefs/task_source_audit.md`. Audited: `shape.json`, `HANDOFF.md`, `sources.md`, `3d/METHODS_3D.md`, `3d/SOURCES_3D.md`, `3d/provenance_3d.json` (21 rows, 15 sources), `3d/validation_3d.json`, `3d/docs.js` (what the viewer shows), `03_images/reefs/palm-beach-gold-coast/images.json` + `IMAGES.md` (34 rows), card `02_research/reefs/palm-beach-gold-coast.json/.md` (read only), `07_scale/bathymetry/gold_coast/HANDOFF.md` (read only). Primary sources were not re-read; two citations were re-searched on the web (below). No model value was changed.
Status: ok = sourced and consistent; fixed = documentation fixed here; missing = not obtainable now; mismatch = values or wording differ between files (recorded, not changed).

## 1. Statement -> source -> location -> how used -> status
| statement / number | source | location | how used | status |
|---|---|---|---|---|
| Toe outline 47 vertices, 11,972 m2 (grid 11,989 m2), 162.3 x 91.3 m | s7 Bluecoast/Nearmap aerial (img-20); s1 City polygon | METHOD.md step 2; shape.json; METHODS_3D 3.2 | traced by colour/line; IoU 0.995, Hausdorff 0.55 m vs s1 | ok (11,972 vs 11,989 = polygon vs 1 m grid, explained) |
| Scale 8.50 px/m | s7 scale bar 0-25-50 m | METHOD.md | bar ticks 26/239/451 px | ok |
| Crest slot 59.2 x 5.9 m, 104.8 deg | s7 innermost contour | METHODS_3D 3.3 | traced | ok |
| Council text 160 x 80 m, 270 m offshore, 60,000 t | s8 EPW 2020 pp.50-51 (img-21), c1 brochure 2020 pp.8-9 (img-12) | provenance rows | nominal figures; check only | ok; c1 URL only in provenance json (added full ref to METHODS 8) |
| Register HEIGHT_M 5, VOLUME 33,000 | s1 attributes | METHODS_3D 4.7 | check; units/datum not stated | ok as "unresolved" (DEC11) |
| Crest -1.5 m MSL | p1 p.1, c1, s8, p2 (+ s6 -1.5 m AHD concept) | METHODS_3D 3.4, HANDOFF 3.2 | four sources agree; MSL kept | ok (DEC5) |
| Crest 0.62 m below LAT | p2 "60 cm at LAT"; t1 MSL 0.88 | HANDOFF 3.2 | arithmetic 0.88 - 1.5 | ok |
| Tide planes HAT 2.03 ... MLWS 0.22 | t1 MSQ 2026 | METHODS_3D 2 | table values | ok |
| AHD = LAT + 0.760 (MSL = AHD + 0.12) | t2 MSQ 2014 via bathymetry REPORT sec 3 | METHODS_3D A11 | benchmark only | ok; reference added to METHODS 8 |
| Seabed 1-10 m on the chart | n1 Navionics SonarChart | METHODS_3D 3.5 | screenshots digitised (`navionics_isolines.py`) | ok |
| Chart datum = LAT | inferred, RMS test (LAT 0.61, MSL 1.28 m) | METHODS_3D 4.3 | assumption A5 | ok (labelled) |
| Contour interval 0.5 m | assumed (A3); fitted 0.459 +-0.003 m | METHODS_3D 4.2 | assumption | ok (labelled) |
| Contour lines show as-built, not design | none | not stated before | assumption | fixed: A12 added |
| Seabed unchanged since survey (nourishment 2017) | none | HANDOFF 5.4 only | assumption | fixed: A13 added |
| Mortensen Fig 6a depths in AHD | none stated | METHODS_3D 4.9 "assumed AHD" | assumption | fixed: A14 added |
| Volume 22,020 m3 (21,966 with ramp); +-0.5 m bed = 28 % | model calc `build_3d.py` | validation_3d.json | integral zr - zb | ok |
| Mean / max height 1.84 / 4.17 m | validation_3d.json | HANDOFF 3.3 | model output | ok |
| Offshore 225 / 305 / 374 m | s3 waterline + shape.json | VERIFY.md | measured in canonical frame | ok |
| Re-check table (9 images) | registry img-03/04/05/09/12-16 | METHODS_3D 4.9, HANDOFF 3.5 | by-eye reads vs model | ok |
| Daniels 2022 PBO1-4 depths | d1 Table 1 | provenance c1/d1 | check; datum unstated | ok; DOI not re-confirmed (below) |
| Prenzler 2022 | p1 | METHODS 8 | text | citation incomplete: DOI/pages not confirmed (REQUESTS) |
| Hunt 2022 DOI 10.9753/icce.v37.management.66 | s4; sources.md verification note | METHODS 8 | confirmed on the article page 2026-10-05 | ok |
| Gemini figures | rejected folder | VERIFY.md | polygon rejected; 160 x 80 / 270 m re-confirmed in s1/s8/c1 | ok; AI use statement added (METHODS 3.10) |
| Decisions | scattered in HANDOFF/VERIFY | - | - | fixed: DEC1-DEC15 added (METHODS 3.9) |
| Per-source "how used" | section 2 listed contributions only | - | - | fixed: METHODS 2.2 table (accuracy, method, element) |
| Processing steps/tools | in 3.x text | - | - | fixed: METHODS 3.10 summary |
| Image registry, 34 rows | images.json | all of citation, url, licence, retrieved date, shows, how_used, date, credit, figure present (checked by script) | - | ok |
| IMAGES.md "3D check pending: YES" on 9 rows | images.json says pending = false (checked 2026-10-10) | IMAGES.md | - | mismatch -> fixed (text now "no (done 2026-10-10...)") |

Counts: 28 statements checked; 21 ok, 6 fixed (A12-A14, DEC list, per-source table, tool/AI statement) plus 1 registry text fix, 1 missing citation detail (Prenzler DOI/pages), 0 wrong values. (Mismatches below.)

## 2. Mismatches and unresolved differences (not changed)
1. Rock volume: model envelope 22,020 m3; card 25,000 m3 "quarried rock" (ICM, R13; 60,000 t / 2.4 t/m3); register 33,000 (units unknown). Different quantities (envelope vs quarried vs register) - the card should say which; text for main below.
2. Offshore distance: card says "270 m vs Royal HaskoningDHV 330 m (unresolved)"; model nearest toe 225 m, centroid 305 m, 279 m from the OSM coast (text 270 m, start point not stated).
3. Width: card 80 m vs 144 m (concept SCS width); model 91 max / 74 mean.
4. PBO3 distance from the toe: bathymetry HANDOFF says about 214 m; Palm Beach HANDOFF says 197 m (different reference point). Not a model number.
5. Seabed/profile test RMS: bathymetry HANDOFF "RMS 0.29 m" (Navionics vs Fig 6a, 17 labels) vs METHODS 4.9 "0.33 m" (model profile vs Fig 6a, 13 labels). Different tests; both labelled by their own docs.
6. Crest: card says 1.5 m below MSL; charted "FISH HAVEN 1.5MT" and design 0.62 m below LAT differ by 0.88 m (HANDOFF 5.2). Open.

## 3. Citations
- Hunt et al. 2022: complete (DOI confirmed on the article page).
- Prenzler et al. 2022 (ICCE abstract 12921): WebSearch 2026-10-10 confirmed title, first authors and ICCE OJS page only. DOI, pages: not confirmed. Added to root REQUESTS.
- Daniels, Metters and Ryan 2022 (abstract 12702): authors, title, affiliation (Queensland Department of Environment and Science) and page confirmed by WebSearch; DOI (papers.63) recorded earlier, not re-confirmed.
- Added to METHODS_3D section 8: c1 City brochure 2020, d1 Daniels 2022, t2 MSQ 2014.

## 4. Viewer panels
The viewer (`3d/index.html`) has tabs Provenance and confidence / Methods / Source log. Sources with "Used for" are in the Provenance tab (Source ids table); Methods tab renders METHODS_3D.md, which now holds the per-source "how used" table (2.2), the assumptions A1-A14 (3.8), the decisions DEC1-DEC15 (3.9) and the tools/AI statement (3.10). No template change was needed. `docs.js` regenerated with `build_3d.write_docs_js()` only (not the whole build); `model.js` byte-identical before and after; docs.js parses in node and contains DEC15. The viewer was not re-rendered (no CDN in the container).

## 5. Page text for main (04_build/data, not edited)
- Card/page key-number rows on rock volume should read "Rock: about 22,000 m3 envelope in the 3D model (inferred); about 25,000 m3 quarried rock and 60,000 t (City / ICM text); council register 33,000 (units unknown)". Old text in `models3d_curated.json` was not read by this audit; main to compare.
- Caveat row "Seabed and reef surface are inferred": add "Assumptions A12-A14 (aerial lines are as built; chart bed unchanged since the survey; Mortensen profile in AHD) and decisions DEC1-DEC15 are listed in the viewer's Methods tab, sections 3.8-3.9."

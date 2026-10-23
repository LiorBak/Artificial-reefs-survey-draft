# SOURCE AUDIT 2026-10-10 - Pratte's Reef (El Segundo) - shape + 3D model + image registry

Standard: `_agent_briefs/task_source_audit.md`. Status: ok = already sourced and consistent; fixed = changed in this audit (documentation only); missing = no source obtainable now; mismatch = values differ between files (listed, not changed).
Decisions applied today: J1 crest datum = the paper's MLLW (Lior, 2026-10-10) = decision D6 in METHODS_3D 3.12; J2 position uncertainty = +-150 m (project team, 2026-10-10) = D10. The model did not move: model.js compared key by key before/after, only 3 text strings differ (provenance uncertainty, confidence reason_short, inputs_status position); computed.json differs only in `sig_x` 100 -> 150.
Source ids: S1-S10, P1 = `3d/METHODS_3D.md` section 2; img1-img7, R1-R28 = `shape.json`; registry ids = `03_images/reefs/prattes-reef-el-segundo/images.json`.

## A. Statement table
| statement / number | source | location | how used | status |
|---|---|---|---|---|
| Outline 435.2 m2, 58.0 x 28.6 m, 76 vertices | P1 = img1 (Skelly drawing via RWR); = Fig. 4 of S10 (img5/img7) | shape.json canonical; VERIFY.md checks 1-7 | traced by hand on the raster, scale bar 0-90 ft = 5.155 px/m; shapely recompute 435.17 m2 | ok |
| Outline accuracy +-0.2 m, +-4 % area | VERIFY.md | check 3 (bar fit 0.5 px) | judgement from +-1 px | ok |
| Size cross-check 30 m (no unit) | S10 p.14 | text | consistency only (-4.7 %) | ok |
| Size cross-check 29.0 x 58.5 m | S10 Fig. 20 own bar | VERIFY.md check 10 | measured on the figure | ok |
| 110 solid bags, 30 optional excluded | P1 printed BAG COUNT; S10 Fig. 4 | drawing legend | classification solid vs dashed (+-10 m2) | ok |
| Bag 4 x 7 x 10 ft, 80-90 % fill | S10 p.2; S2 Fig. 1 | text | volume V8 check | ok |
| Bag mass "about 14 t" | S10 p.2 | text | context | mismatch: reef card says ~12.7 t (Blacka et al. 2013 via card); different sources, not a model input |
| Crest B = approx. -6 ft MLLW at the outermost point = -2.678 m MSL | S10 p.2 | text | MLLW -> MSL with MSL-MLLW 0.849 m (S4) | ok; datum reading confirmed by Lior 2026-10-10 (D6) |
| Crest A = -6 ft MSL = -1.829 m | P1 label "TOP OF BAG MIN DEPTH -6' MSL" | drawing | alternative scenario | ok |
| Crest 1.8 m below MLLW | S2 text; reef card | - | confirmation, same authors as S10 | ok (not independent) |
| MSL-MLLW 0.849 m (0.861 at LA); MSL-NAVD88 0.792 m; HAT, MHHW etc. | S4, S8 NOAA CO-OPS datums API, epoch 1983-2001 | datums.json | formula z_MSL = z_MLLW - 0.849 | ok |
| Seabed -3.67 m MSL at the reef centre, slope 1:32 | S5 NOAA 1/3 arc-sec DEM | METHODS 3.4 | 31 stations, bilinear, mean profile | ok |
| Seabed check +-0.3 m | S6 CRM, S7 Navionics, S10 Figs 5-9 | METHODS 3.5, V5, V13-V16 | independent cross-checks | ok |
| Navionics datum = MLLW | assumption A8 | METHODS 3.9 | label test | ok (assumption labelled) |
| Position hint 33.92058 N, 118.43335 W | S10 Fig. 9 window centre + p.1 text + Fig. 2 | METHODS 3.10 | UTM 11N to lat/lon, pyproj | ok |
| Position uncertainty | S10 p.1 text (200 m) vs Fig. 2 (about 340 m) | METHODS 3.10, VERIFY check 12 | decision | FIXED: +-100 m -> +-150 m (D10) in build_3d.py, METHODS template (3.10, 5, A13, L1, 6), shape.json geo_note, METHOD.md, VERIFY.md, SOURCES_3D.md, 3d/REQUESTS_FOR_LIOR.md, index.html note; hint and model unchanged |
| Frame bearings 155 / 245 deg | img4 shoreline fit, img6 north arrow, Fig. 9 | METHODS 3.1, A1 | fitted | ok (+-5 deg) |
| Reef centroid 91.44 m from MSL waterline | S1 "100 yd"; S3 "roughly 100 m" | A2 | assumption, +-25 m | ok |
| Chronology (22 Sept 2000, Apr 2001, 2008, 2010) | S10, S2, S9 (card; Surfline 2008, Coastal Frontiers) | METHODS 2.1 | notes only, not modelled | ok; S9 not re-fetched (stated) |
| Volume B 443 m3, A 550 m3 | computed.json (build_3d.py) | METHODS 5 | prism integration over the polygon, side slope 1:1 (A5) | ok |
| Volume gap V8 (443 vs 695-782 m3) | computed | V8 | unresolved, flagged | ok (open issue) |
| Side slope 1:1, thickness one 1.2 m course | assumptions A4-A6 | METHODS 3.9 | assumed, ranges given | ok |
| Gemini footprints (40 x 20 m, 584-650 m2) | not used | shape.json rejected record; METHODS 2.2 | compared and rejected | FIXED: now stated in METHODS_3D 2.2 |
| Earlier agent estimates (first trace -49 m2; 324 m2 schematic) | superseded | shape.json, VERIFY | corrected | ok; stated in 2.2 |
| Each source's "how used" | - | METHODS_3D 2.2 | - | FIXED: new table (previous table said only what each contributed) |
| Decisions list | - | METHODS_3D 3.12 (D1-D10) | - | FIXED: new (decisions were spread over HANDOFF section 2, SOURCES_3D RUN 2, shape.json) |
| Per-element confidence | - | METHODS_3D 6 | - | FIXED: new table (was overall LOW only) |
| Assumptions A1-A13 | - | METHODS_3D 3.9 | basis and effect given | ok (A13 uses {{sig_x}} = 150 now) |
| Scripts producing numbers | build_3d.py, bn_digitise.py, nav_annotate.py, make_annotations.py, reef3d_lib.py | METHODS 9 | listed | ok |
| Citation of S10 (venue, year, pages) | Borrero & Nelsen 2003; the PDF prints neither | METHODS 2, 8; root REQUESTS P13/W10 | WebSearch 2026-10-10: not confirmed (no catalogue entry found; other search hits unrelated) | missing: venue "3rd International Surfing Reef Symposium, Raglan" and year 2003 remain unverified; pages unknown |
| S3 RWR "(n.d.)", S9 Coastal Frontiers "(n.d.)" | web pages | METHODS 8 | access date 2026-10-05 for RWR | ok; Coastal Frontiers/Surfline not re-fetched (stated) |
| Image registry, 38 rows | images.json | all rows have citation, licence, retrieved, shows, how_used, image_url, image_date (script check: 0 empty) | - | ok |

## B. Consistency (card vs model) - card NOT edited
| item | model / shape.json | card (`02_research/reefs/prattes-reef-el-segundo.json`) | status |
|---|---|---|---|
| V size | 58.0 x 28.6 m, Phase I design layout (Skelly drawing, scale bar) | "64 m x 29 m V, depth 3.0 m (MLLW), 50 m from the undisturbed shoreline" (Blacka et al. 2013 Table A.11, via card) | mismatch, 64 vs 58.0 m (10 %), and 50 m vs 91.4 m from shoreline; the 64 m figure is not discussed in shape.json or METHODS_3D (possible Phase II or rounded value). Not changed; for main |
| Crest | -6 ft MLLW at apex (S10) | "crest 1.8 m below MLLW" | consistent |
| Bag mass | 14 t (S10 p.2) | ~12.7 t | mismatch, context only |
| Position uncertainty | +-150 m (D10) | card has no coordinate (geo null in shape.json) | check card/page text for "+-100 m" - none found in card |

## C. Viewer
`3d/index.html` Methods & sources pane gained sub-tabs "Sources: how used", "Assumptions", "Decisions", "Confidence" (each shows one section of methods_md; the full Methods tab also contains them). Checked: module script passes `node --check`; section extraction tested on docs.js. A real canvas/CDN render could not be tested here (three.js loads from jsdelivr; no network).

## D. Page texts for main (04_build/data not edited)
Any occurrence of "+-100 m" for the Pratte's position in `models3d_curated.json` / `models3d_caveats.json` -> "+-150 m (paper text and Fig. 2 differ by 140-170 m)". Exact old strings were not in my brief; grep them for "100 m" near "position". The HANDOFF section 6 step 1 snippets are otherwise unchanged.

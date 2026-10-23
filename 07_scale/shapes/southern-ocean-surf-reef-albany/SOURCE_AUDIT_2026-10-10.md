# SOURCE AUDIT 2026-10-10 - southern-ocean-surf-reef-albany (Southern Ocean Surf Reef, "Midds Reef", Middleton Beach, Albany WA)

Auditor: fresh agent, task brief `_agent_briefs/task_source_audit.md`. Files audited: shape.json, FEASIBILITY.md, METHOD.md, VERIFY.md, sources.md, HANDOFF.md, registry `03_images/reefs/southern-ocean-surf-reef-albany/images.json`. No 3D model exists (point 8 does not apply). No model value was changed.
Network: WebFetch/curl do not work; WebSearch worked and was used to re-confirm the City of Albany design-table values and to complete citations.
Status key: ok = source and location confirmed; ok(card) = taken from the reef card, not re-fetched in this audit; fixed = text corrected in this audit; mismatch = inconsistency recorded, value untouched; missing = no source yet.

## 1. Sources and how each was used (point 2)
| id | full citation | location | what was read / how | accuracy | feeds | status |
|---|---|---|---|---|---|---|
| sat2026 (reg. img-13) | Esri, Maxar, Earthstar Geographics and the GIS User Community. World Imagery (current layer), tile service https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer, centre -35.018, 117.9207, r 250 m, z18; capture date 2026-01-20 (identify DATE field); retrieved 2026-10-04 | file `src/esri_current_2026-01-20_z18.png` + `.geo.json`; 1022x1022 px | 20-vertex outline traced by eye on a contrast-stretched copy; an objective mask (green < 30) used as a check; georeferenced, 0.4891 m/px | edge +-1.5-4 m landward, +-5-7 m offshore (soft edge); area -30 % / +20 % by edge definition | plan, version `sat_2026`; shoreline; frame | ok. Scale recomputed here: 156543.03 x cos(35.018 deg) / 2^18 = 0.4891 m/px (matches sidecar) |
| sat2025 (img-12) | Same provider, Esri World Imagery Wayback release 13192, capture 2025-01-16 | `src/esri_wayback13192_2025-01-16_z18.png` | before/after: mean green inside polygon 137 (2025) vs 57 (2026) | - | validation only (shows the dark patch is the reef) | ok |
| design_plan (img-11) | Bluecoast Consulting Engineers, "Southern Ocean Surf Reef Design" plan, via Raised Water Research, https://raisedwaterresearch.com/wp-content/uploads/2019/12/Souther-Ocean-Surf-Reef-Design-by-Bluecoast.png (page: https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/albany-artificial-surf-reef/); upload path 2019-12; retrieved 2026-10-04 | 984x702 px gallery image; scale bar ticks at x = 493.5 / 569.5 / 645.5 px = 0 / 50 / 100 m | outermost contour traced (25 vertices); scaled by the bar (1.52 px/m, +-3 %); positioned by overlap with sat2026 (see A3) | outline about 2 m; position +-3 m alongshore | plan, version `design_bluecoast` (default) | ok |
| design_table (img-10) | City of Albany / Bluecoast, "Final Reef Design" table + plan (design.jpg), https://www.albany.wa.gov.au/Profiles/albany/Assets/ClientData/Surf_Reef/design.jpg; page https://www.albany.wa.gov.au/council/projects/completed-projects/southern-ocean-surf-reef-sosr.aspx; retrieved 2026-10-04 | table, 1026x521 px | values read by eye: left-hander; 34,000 m3 (2017 bathymetry); 350 m N of Big4 Middleton Beach Caravan Park; 140 m from landward toe; crest 110 m @ -2 m AHD; crest -1.00 m AHD; orientation 270-305 N; peel 60 deg; rides to 100 m / 12 s; 41 % of year | read values 100 % legible | crest level, volume, orientation text, validation of plan | ok. Re-confirmed this audit by WebSearch of the City project profile (https://www.albany.wa.gov.au/documents/804/southern-ocean-surf-reef-project-profile and the current-projects page): -1.00 m AHD, 34,000 m3 on 2017 bathymetry, 110 m @ -2 m AHD, 350 m, 140 m, 270-305 N, armour 1-4 t all agree |
| constr_aerials (img-03, img-05) | ABC News "Supplied" 2025; Raised Water Research construction overview 2025-05 | registry | oblique, no scale | - | context only, not traced | ok |
| card R3 | City of Albany SOSR project pages (current + completed), accessed 2026-09-24 | https://www.albany.wa.gov.au/council/projects/completed-projects/southern-ocean-surf-reef-sosr.aspx | 165 m long, up to 110 m wide, 62,800 t, layers (belly D50 0.16 m 12,400 t 18 %; core 0.49 m 23,600 t 36 %; armour 0.94 m 26,800 t 46 %), crest -1.0 m AHD = 0.74 m below mean low water / 1.34 m below mean high water | text | dimensions check; levels | ok(card). 62,800 t, layer splits and the 0.74 / 1.34 m statements were not visible in the WebSearch snippets: not re-confirmed |
| card R5 | Wikipedia, "King George Sound (Western Australia)", https://en.wikipedia.org/wiki/King_George_Sound_(Western_Australia), accessed 2026-09-24 | - | mean tidal range 0.4 m, spring range 1.1 m | secondary source | tides (context) | ok(card), WEAK source. Replace by Bureau of Meteorology / WA Department of Transport tide tables for Albany (added to REQUESTS) |
| card R11 + R18 | Albany Advertiser, Melissa Sheil, 11 March 2026, "Eighteen rocks of Southern Ocean Surf Reef repositioned in successful bid to reduce user injuries", https://www.albanyadvertiser.com.au/news/albany-advertiser/eighteen-rocks-of-southern-ocean-surf-reef-repositioned-in-successful-bid-to-reduce-user-injuries-c-21896905 | headline, byline, date only (body paywalled) | 18 rocks moved after the 2026-01-20 image | - | note only (no model effect) | fixed: shape.json/HANDOFF cited "card R11" only; R18 is the dedicated re-verification entry; both now cited |
| card R4, R15 | Wikipedia "Middleton Beach, Western Australia" (reef ~120 m offshore); City of Albany FAQ May 2023 PDF (~145 m) | https://www.albany.wa.gov.au/documents/803/albany-artificial-surf-reef-community-update-and-faqs | earlier offshore distances | - | rejected alternatives (superseded by the final table, 140 m) | ok(card) |
| Gemini | 07_scale/00_gemini_footprints_extract.json (polygon, 13,500 m2, "160-190 deg") | - | compared only | its three sources have no URL and cannot be fetched | none | ok: not used. Area 13,500 is within 3 % of our design outline by coincidence of the same City numbers; orientation text unsupported |

## 2. Statement-by-statement check (point 1)
| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | Placement of rock Jan-Mar 2025, quarry from Oct 2024, opened 16 July 2025 | card R3, R2 (ABC News, Daniel Mercer, 2025-07-16, https://www.abc.net.au/news/2025-07-16/southern-ocean-surf-reef-transforms-albany-wa/105530202) | card Quick facts / Built section | state drawn = as built | fixed: shape.json `design_version.drawn` said "built Oct 2024 - Mar 2025"; Oct 2024 is quarry establishment, placement was Jan-Mar 2025. Text clarified |
| 2 | Length 165 m, width up to 110 m | card R3 | City page | dimensions check | ok(card) |
| 3 | Crest -1.0 m AHD; crest length 110 m at -2 m AHD | design_table img-10; re-confirmed by WebSearch of City profile | table rows | crest | ok |
| 4 | MLLW = -0.26 m AHD, MHHW = +0.34 m AHD | derived: -1.00 + 0.74 and -1.00 + 1.34 from the City's two statements (card R3) | FEASIBILITY e. | tide levels | ok arithmetic; sources of 0.74/1.34 = ok(card). The implied MHHW-MLLW = 0.60 m lies between the Wikipedia mean 0.4 m and spring 1.1 m: plausible, no conflict |
| 5 | Mean range 0.4 m, spring 1.1 m | card R5 (Wikipedia) | - | context | ok(card), weak source |
| 6 | 62,800 t = 34,000 m3 (implied 1.85 t/m3) | City table (34,000 m3) and card R3 (62,800 t) | - | volume cross-check | ok. The 1.85 t/m3 is the ratio of two City numbers (62,800 / 34,000 = 1.847), not an independent density source |
| 7 | Mean height 2.6 m (design outline) / 3.1 m (sat patch) | 34,000 / 13,104 = 2.59; 34,000 / 10,918 = 3.11 (recomputed here) | - | inference | ok arithmetic; INFERENCE (assumes the whole volume lies inside the outline and a flat bed; not a measurement) |
| 8 | Design outline area 13,104 m2; sat outline 10,918 m2; objective mask 7,707 m2 | shape.json polygons (shoelace recomputed here: 13,104.7 and 10,918.5) | - | plan | ok |
| 9 | Along / across the crest 164.6 / 121.2 m (design), 157.2 / 116.7 m (sat) | scripts/analysis_out.json | - | dimension check | ok(script); not recomputed |
| 10 | Shoreline bearing 30.3 deg true (95 % CI 27.7-33.0), 16.7 deg northern rows, 27.0 deg whole beach | Theil-Sen fit, scripts/analysis.py | METHOD 2a.5 | frame | ok(script) |
| 11 | Nearest edge 66.8 m (design) / 70.8 m (sat) from the beach-face line; "140 m from landward toe" not reproducible | City table vs our measurement | VERIFY 4 | validation | mismatch (open): reference line of the City's 140 m is undefined. Recorded, no model effect |
| 12 | Design position, rotation -3 deg, IoU 0.84 (free fit), 0.807 (north-up fit) | scripts, METHOD 2b.5 | - | position of default outline | ok(script); see A2, A3 |
| 13 | Registry img-10 volume | images.json/IMAGES.md said 54,000 m3 | - | - | fixed earlier by the tracing agent (now 34,000 m3); re-checked here: ok |
| 14 | `canonical` in shape.json is derived from sat2026 (area 10,918 m2) while `default_outline` = design_bluecoast (13,104 m2) | shape.json | canonical vs default_outline | page | mismatch, for main: SHAPE_SPEC and compile_data say the drawn outline is `canonical.polygons_m`; if the page draws canonical it shows the sat trace, not the stated default. Not changed (model value). Main to check the page |
| 15 | sources.md role of design_table = "context (parameters read)"; shape.json role = "context" | - | - | - | mismatch (wording): the table is the source of the crest level, volume, orientation text, so its role is "primary for parameters". Wording fixed in sources.md |
| 16 | Esri retrieved 2026-10-04 (sources.md, registry) vs the images' own dates 2025-01-16 / 2026-01-20 | sidecars | - | - | ok (retrieval date and image date are different things and both given) |

## 3. Methods (point 3)
- Scale of sat2026: georeferenced tile, m/px from the sidecar, recomputed (above).
- Outline sat2026: hand trace on an enhanced copy (7x7 minimum filter + gaussian sigma 3 of the green channel) in `scripts/trace_mask.py`; objective threshold mask as check.
- Outline design: hand trace of the outermost contour; scale bar; position by translation chosen to maximise overlap with sat2026 (`scripts/build_shape.py`); free similarity fit only as a check (rotation -3 deg, scale 0.90).
- Shoreline: first bright dry-sand run (R > 165) in 30 rows, Theil-Sen line (`scripts/analysis.py`).
- Frame and areas: `scripts/build_shape.py`, shapely/geom.py; areas recomputed here by shoelace in shape.json.
- Tide levels: arithmetic from the City's two statements. No interpolation, smoothing or lofting; no AI tool influenced a number (Gemini only compared and rejected).

## 4. Assumptions (point 4)
| id | assumption | why | effect | replaced by |
|---|---|---|---|---|
| A1 | The Bluecoast final design is the reef as built | City page dimensions equal the design table; satellite wedge has the same shape and orientation (IoU 0.84) | outline could differ by metres to tens of metres at the toe; area of the default outline 13,100 m2 vs visible 10,900 m2 is the measured spread | as-built survey (City, March 2025 practical completion) |
| A2 | The design figure is north-up | dashed crest line reads 278 deg vs text 270-305 N; free fit -3 deg | +-3 deg rotation = about +-3 m at 60 m from the centroid | a Bluecoast CAD plan with coordinates |
| A3 | Design figure position = translation giving the best overlap with sat2026 | figure has no coordinates | +-3 m alongshore (centroid-aligned IoU 0.792 vs 0.807) | CAD coordinates |
| A4 | Shoreline = beach-face line (edge of bright dry sand) | swash line unmeasurable (foam); true swash 10-15 m seaward | offshore distances (66.8 / 70.8 m) would be 10-15 m smaller to the swash line | dated low-tide image with a clean waterline |
| A5 | The dark patch on 2026-01-20 is the reef and its edge is the visible toe | before/after pair | offshore edge +-5-7 m; area -30 % / +20 % | multibeam or LiDAR |
| A6 | The 110 m / 140 m dimension arrows on the figure are schematic; only the bar scales it | arrows measure 69 m / 117 m by the bar | none if right; +-10 % size if the arrows were right | the report drawing |
| A7 | AHD is read as about mean sea level for the MLLW/MHHW derivation | no source; the City gives levels relative to AHD and to MLLW/MHHW in one sentence | tide levels +-0.1 m possible | WA Department of Transport datum sheet for Albany |
| A8 | Rock volume of 34,000 m3 lies inside the traced outline (mean-height inference) | design table | mean height 2.6-3.1 m; not used by any model | bathymetry |
| A9 | The March 2026 move of 18 rocks does not change the planform | after the image, article body paywalled | unquantified, expected small | post-2026 survey |
The inference "seabed about -3.5 to -4.5 m AHD under the crest" (FEASIBILITY) is NOT an assumption used anywhere; it is a hint only and is marked as such.

## 5. Decisions (point 5)
| id | decision | options | who / when | reason |
|---|---|---|---|---|
| D1 | Default outline = Bluecoast final design; toggle = visible reef 2026-01-20 | design vs satellite trace | agent, 2026-10-10, applying Lior's rule (measured survey > design drawing of the built version > photo trace) | no survey found |
| D2 | State drawn = as built (March 2025); rock move 2026 = note | as built / after 2026 | agent, 2026-10-10 | rule 5 |
| D3 | Frame: +x NNE 30.3 deg, +y offshore 120.3 deg, true unmirrored | shoreline-aligned vs north-up | agent, 2026-10-10 | page spec, matches Borth |
| D4 | Shoreline = beach-face line | swash vs beach face | agent | see A4 |
| D5 | 3D NOT built | assume bed at -4 m / wait | agent, 2026-10-10 | no seabed, height or slope source; an assumed bed would look like data |
| D6 | Gemini not used | - | agent | rule 2 |
| D7 | Design arrows not used | - | agent | A6 |

## 6. Confidence per element (point 6)
Plan: HIGH (position, orientation, length; area -30 % / +20 %). Crest: MEDIUM-LOW (design value -1.00 m AHD, confirmed on the City profile; no as-built level). Seabed: NONE. Slopes / height: NONE. Tides: LOW-MEDIUM (Wikipedia ranges; derived MLLW/MHHW). Volume: MEDIUM (design table; 2017 bathymetry). Overall for the shape: HIGH; for a 3D model: not buildable.

## 7. Consistency (point 7)
Checked shape.json vs HANDOFF vs METHOD vs VERIFY vs sources.md: areas, extents, scale, dates agree (items 8, 12, 16). Mismatches: items 11, 14, 15. Card vs shape: card says "construction began March 2025 (main placement Jan-Mar 2025)" and later "ran from roughly October 2024"; shape text now says placement Jan-Mar 2025 (item 1). Card calls tonnage "~70,000 t" in Type/materials but 62,800 t in Dimensions (R3): card-internal difference, for card owner, card not edited.

## 8. Counts
Statements checked 16 (+9 assumptions, 7 decisions); ok 11; fixed 3 (1, 15, R18 citation); mismatch 3 (11, 14, 15; 15 fixed as wording); missing 1 (primary tide source).

## 9. Image registry check (03_images/reefs/southern-ocean-surf-reef-albany/)
13 rows checked by script: every row has citation, image_url, source_page, page_or_figure, image_date, credit, license, retrieved, shows, how_used and file; every file exists on disk. Licences are "not cleared" private copies as recorded. IMAGES.md not rewritten.

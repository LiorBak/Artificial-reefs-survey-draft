# HANDOFF - palm-beach-gold-coast (shape traced and verified 2026-10-05; 3D model built 2026-10-05; 3D image re-check 2026-10-10; for the page builder and any later agent)

Read this instead of METHOD.md / VERIFY.md / METHODS_3D.md unless you must check one number. Paths are relative to
`07_scale/shapes/palm-beach-gold-coast/` unless a root path is given. Source ids: s1 council GIS polygon, s3 Esri 2025-12-01, s4 Hunt 2022 (ICCE 13024),
s6 Mortensen 2015, s7 Bluecoast/Nearmap aerial, s8 EPW 2020, p1 Prenzler 2022 (ICCE 12921), p2 Swellnet 2019, t1 MSQ tidal planes 2026, t2 MSQ 2014 AHD,
n1/n2 Garmin Navionics SonarChart / nautical layers, c1 City brochure 2020, d1 Daniels 2022 (ICCE 12702), g1 GEBCO. Registry ids `palm-beach-gold-coast-img-NN`.

## 1. Status per stage

| stage | state | date | confidence and why |
|---|---|---|---|
| Trace (plan) | done, `shape.json` status `verified` | 2026-10-05 | HIGH: outline read off a scaled, north-up aerial (8.50 px/m) and equal to the City GIS polygon (IoU 0.995, Hausdorff 0.55 m, area +0.25 %); same shape in ICCE Fig 1; rock visible on Esri 2025-12-01. Soft spots: the "80 m wide" label (91 m max, 74 m mean), undated aerial, contours unlabelled |
| Verify | done (`VERIFY.md`) | 2026-10-05 | Gemini's chevron polygon and wrong coordinates (1.2 km off) rejected; its 160 x 80 m / 270 m figures are right |
| 3D model | built, `3d/index.html` + `model.js` | 2026-10-05; re-checked and rebuilt 2026-10-10 | MEDIUM: plan, crest (-1.5 m MSL) and tides sourced; seabed (Navionics SonarChart, datum assumed LAT) and reef surface (10 unlabelled contours, assumed 0.5 m) inferred. Council register height 5 m / 33,000 m3 is 22 / 33 % above the model: unresolved |
| 3D image re-check | done, no geometry change | 2026-10-10 | 9 flagged images checked (section 3.5); 7 within tolerance, PBO3 marginal (+0.62 m, extrapolated), 2 qualitative only |
| Image registry | complete: 34 images, all saved locally, sha256 checked, `pending_3d` = 0 | 2026-10-10 | `03_images/reefs/check_registry.py` reports Palm Beach clean (other reefs have their own errors) |
| Page | not touched by this folder's agents; main must update `04_build/data/models3d_curated.json` / `models3d_caveats.json` (section 6, item 1) | - | - |

State drawn: the reef AS BUILT in May-September 2019 (rock placed by a Hall/Heron joint venture, certified Sept 2019). No later works, damage, loss or
renewal found (Prenzler 2022 "insignificant movement or settlement"; ICM 2023; Esri 2025-12-01 shows the rock). One state only, no outline versions.

## 2. Key decisions and why

- Default outline = the outer survey contour of the Bluecoast/Nearmap aerial (s7) = City asset polygon (s1) = toe footprint; plus the innermost contour (59 x 6 m slot at 104.8 deg) as the crest. Measured survey > design > photo trace (rule 4); the Esri visible-rock patch (s2) is only a cross-check (25-38 % of the footprint shows as dark rock).
- The 160 m axis is skewed about 45 deg to the shore (long axis 109.6 deg true; shoreline 334.3 +-2 deg). The earlier text-derived schematic had it alongshore and was replaced.
- Concept designs (Mortensen 2015 SCS A/B/C: 175 x 144 m, 53,319 m3, 560 m offshore) were NOT built; used only for slope labels 1/12, 1/5, crest orientation 105 deg and the depth profile of Fig 6a.
- Crest = -1.5 m vs MSL (four sources, section 3.2). The AHD vs MSL difference (0.12 m) is inside the +-0.2 m crest uncertainty and is not applied.
- Frame = canonical frame of shape.json; z = 0 at MSL; tide planes of the Gold Coast Seaway standard port (MSQ 2026, MSL = LAT + 0.88 m). Local tides only, no Haifa preset.
- Seabed = thin-plate spline through the Navionics SonarChart 1 m iso-lines (outside a 25 m buffer) plus the toe elevations ("hybrid"); chart datum taken = LAT (tested twice, 3.4). The Navionics-only surface is kept as the independent check.
- Reef surface = Delaunay interpolation between the survey contours at z = -1.5 - 0.5 k m. One rock surface, envelope volume (voids included); layers (core 300-1000 kg, armour 1-8 t, crest 6-8 t) are not drawn: no thicknesses published.
- Re-check 2026-10-10: nothing changed in the geometry. Judgement calls (PBO3, register volume/height) are documented, not "fixed". Changed only documentation: crest provenance pages, PBO3 and Mortensen rows, AHD offset now VERIFIED (MSQ 2014, read at the source by the bathymetry report), section 4.9.

## 3. Key numbers (units, datum, source id)

### 3.1 Plan (canonical frame: x alongshore toward 334.3 deg, y offshore toward 64.3 deg, metres; origin = foot of the perpendicular from the centroid to the 2025-12-01 Esri waterline)
| quantity | value | source |
|---|---|---|
| toe outline | 47 vertices, 11,972 m2 (grid 11,989 m2), oriented rectangle 162.3 x 91.3 m, mean width 73.8 m, long axis 109.6 deg true | s7, s1 |
| crest slot | 59.2 x 5.9 m, axis 104.8 deg (concept crest 60 m at 105 deg, s6) | s7 |
| council text | 160 x 80 m, AREA_SQM 11,941.7 | s1, c1, s8 |
| offshore distance | nearest toe 225 m, centroid 305 m, farthest 374 m from the waterline; 279 / 361 m from the OSM coast; text says "approx. 270 m" (from the beach edge, start point not stated) | VERIFY.md |
| centroid | -28.107334, 153.470913 (canonical origin -28.108526, 153.468119) | shape.json geo |
| frame check | 47 vertices round-trip to 0.024 m; mirrored x would be 82 m off (left-handed canonical triple, viewer converts to E-N-U) | validation_3d.json |

### 3.2 Levels (z in metres vs MSL unless stated)
| quantity | value | source |
|---|---|---|
| crest | -1.5 m MSL = -0.62 m vs LAT (Seaway MSL); about -0.50 m vs LAT with the interpolated Palm Beach MSL (1.0 m above LAT) | p1 p.1 ("1.5m below mean sea level"), c1 pp.8-9 ("average water level"), s8, p2 ("60 cm at LAT"), s6 p.4 (concept -1.5 m AHD) |
| tide planes (above LAT) | HAT 2.03, MHWS 1.53, MHWN 1.24, MSL 0.88, MLWN 0.51, MLWS 0.22 (Gold Coast Seaway, epoch 2010-2029); ocean beaches tide 20 min earlier | t1 |
| AHD | AHD = LAT + 0.760 m at the Seaway benchmark, so MSL = AHD + 0.12 m (benchmark only) | t2 (bathymetry REPORT sec 3) |
| toe elevation | -4.0 to -7.0 m MSL (landward to seaward end, +-0.5 m) | s7 + interval 0.5 m (A3, A4) |
| seabed | 1 m to 10 m below LAT on the chart (z = -d - 0.88); under the reef a smooth interpolation (+-0.5 m) | n1 |
| contour interval of the aerial lines | 0.5 m ASSUMED; Navionics implies 0.459 m (bands 0.65 / 0.51 / 0.43); 1.0 m would put the seaward toe at -12.5 m | 3d/METHODS_3D.md 4.2 |
| side slopes | 1:12 (N flank, outer E end), 1:4.9 (S flank), 1:25 near-crest platform at the E end; concept labels 1/12 and 1/5 | s7, s6 Fig 3 |

### 3.3 3D model numbers (validation_3d.json, 1 m reef grid, 4 m seabed grid x -300..300, y -40..620 m)
| quantity | value |
|---|---|
| rock envelope volume | 22,020 m3 (21,966 m3 with the 2.5 m edge ramp); Navionics-only seabed 16,358 m3 |
| volume vs seabed offset (-1.0 / -0.5 / -0.25 / +0.25 / +0.5 / +1.0 m) | 34,004 / 28,010 / 25,013 / 19,158 / 16,537 / 11,957 m3 |
| crest height above seabed | 3.89 m (3.51 m Navionics-only seabed); mean seabed under the crest -5.39 m MSL |
| mean / max reef height | 1.84 m / 4.17 m at (-8, 291) m |
| toe vs Navionics seabed | mean -0.27 m (rock toe deeper), sd 0.55 m, n = 427; datum RMS test: LAT 0.61, MLWS 0.74, MLWN 0.96, AHD 1.17, MSL 1.28 m |
| register | HEIGHT_M 5, VOLUME 33,000 (units/datum not stated); card 25,000 m3; 60,000 t (EPW) -> 1.82 t/m3 if 33,000 m3 |
| confidence_3d | medium |

### 3.4 Other
- Offshore anchors: model seabed at y = 560 m is 11.8 m below LAT; concept design 11.4 m at "560 m" (different structure); GEBCO 2024 -13 m in a 450 m cell (1.1 m from the model, too coarse).
- Buoys (d1 Table 1, datum not stated): PBO3 11.75 m at (-28.107191, 153.473845); PBO2 11.29; PBO1 11.33; PBO4 23.80 m. Only PBO3 lies inside the model grid.
- City DTM has no Palm Beach nearshore cells (REQUESTS C2 closed, img-11); the Queensland nearshore LiDAR (2025) is not released.

### 3.5 Re-check table 2026-10-10 (details and method: `3d/METHODS_3D.md` 4.9; numbers in `3d/validation_3d.json` key `recheck_2026_10_10`)
Tolerance: 2 m plan (4 m georeferenced), source's stated vertical accuracy (none stated by any source: model +-0.5 m seabed, +-0.2 m crest used).
| img | source value | model value | difference | verdict |
|---|---|---|---|---|
| 14 | crest 1.5 m below "average water level" | -1.5 m MSL | 0 (0.12 m if AHD) | within; keep |
| 12 | 160 x 80 m, ~270 m offshore, crest 1.5 m | 162.3 x 91.3 m (mean 73.8); nearest toe 225 m (279 m OSM coast); -1.5 m | +2.3 m length; width 80 vs 91/74; offshore 270 vs 225-279 | within against the council polygon (0.55 m); text nominal |
| 13 | 270 m, icon not in raster, no scale | as 12 | not measurable here | same as 12 |
| 09 | 13 labels 3.5-11.5 m, datum assumed AHD | model profile (+-150 m), AHD = MSL-0.12 | RMS 0.33 m, mean -0.07, max 0.52 (0.89 at the 3.5 m surf-zone label), shift 313 m | within +-0.5 m; keep |
| 05 | PBO3 11.75 m (datum unstated) | 12.37 m below LAT (13.25 below MSL) at canonical (-110.7, 571.2), 197 m seaward of the toe, extrapolated beyond the 10 m line | +0.62 m (LAT) / +1.50 m (MSL) | marginal; no change (a 23 m shift of the 12 m contour removes it); validation row added |
| 04 | north-up aerial, patch axis ~102 deg (+-5), L/W 2.0 | slot 104.8, outline 109.6 deg, L/W 1.8 | 2.6 / 7 deg | within error; camera wedge = camera-match candidate |
| 15 | mound present at 2 dates, axis 108.3 / 108.8 deg | 109.6 deg | ~1 deg | within; supports "no later change" |
| 03 | one wave breaking beyond the shore-break | crest slot 59 x 6 m | not quantifiable (no camera, no scale) | qualitatively consistent |
| 16 | oblique, dredger on the dark patch, no scale | 162 x 91 m, 225 m toe | not quantifiable | qualitatively consistent |

Before / after the rebuild (identical): seabed grid, reef grid (12,830 valid cells, 12,200 above the seabed, the rest are the h = 0 edge ramp, minimum
h -0.01 m = cm rounding), contours, crest, toe, volume 22,020 m3 (change 1e-4 m3 float noise), height at crest 3.886 m, max 4.171 m. New: 3 provenance rows (21 total), 3 sources (15 total), validation key `recheck_2026_10_10`, METHODS_3D 4.9, AHD wording.

## 4. File map

| path | what it holds / when to open |
|---|---|
| `shape.json` | verified plan shape (canonical + lat/lon), design_version, dimensions_check, references. Open for any plan number |
| `METHOD.md`, `VERIFY.md`, `sources.md` | tracing method, independent verification, source table s1-s8. Open only to check a number |
| `src/` | source images (aerial, ICCE figs, Esri tiles, `gov/` council + ICCE originals, `navionics/` 44 screenshots - bulky) |
| `overlays/` | trace overlays on the aerial / Esri / ICCE icon (s7 is the primary) |
| `3d/index.html`, `model.js`, `docs.js` | the viewer and its data (generated; model.js ~300 kB, do not open, parse it). The viewer was not re-rendered 2026-10-10 (index.html unchanged; model.js / docs.js parse-checked) |
| `3d/build_3d.py` | regenerates model.js, docs.js, validation_3d.json, provenance_3d.json (calls `write_provenance.py`); constants at its top = assumptions A3-A7. `recheck_2026_10_10()` is the PBO3 / Mortensen check |
| `3d/METHODS_3D.md` | academic methods note (sections 1-9; 4.9 = re-check). Rendered inside the viewer |
| `3d/SOURCES_3D.md` | source log with captions and the registry-id map |
| `3d/validation_3d.json`, `provenance_3d.json` | every number of the model; provenance rows shown in the viewer panel |
| `3d/contours_s7.py/.json/_sd.npz`, `navionics_*.py/.json` | contour tracing and Navionics iso-line extraction (capture needs Chrome and the network; outputs are kept) |
| `3d/annotated/` | annotated source images (contour ranks, datum test, Navionics reads, `recheck_orientation_img04_img15.png`) |
| `3d/preview_*.png` | viewer screenshots from 2026-10-05 (not re-rendered) |
| `3d/archive/pre_recheck_2026-10-10/` | model.js, docs.js, provenance/validation json, METHODS_3D, SOURCES_3D, build_3d, write_provenance, index.html, REQUESTS as they were before this re-check (508 kB; delete when the re-check is accepted) |
| `3d/REQUESTS_FOR_LIOR.md` | Navionics app A1-A7, Google Earth B1-B4, e-mail C1; C2 closed 2026-10-10 |
| Root: `03_images/reefs/palm-beach-gold-coast/images.json`, `IMAGES.md` | image registry (34 rows) |
| Root: `07_scale/bathymetry/gold_coast/REPORT.md` sec 2.3, 3, 5 | DTM coverage, MSQ datums, Mortensen profile test, integration plan 5.3 |

## 5. Open issues, discrepancies, pending checks

1. Register HEIGHT_M 5 / VOLUME 33,000 vs model 3.9 m / 22,000 m3: unexplained. Needs the City's as-built survey or Design Reference Report (Royal HaskoningDHV, unpublished). All independent seabed evidence (chart, toe elevations, Mortensen survey, GEBCO) is shallower than a seabed that would give 33,000 m3.
2. Charted crest "FISH HAVEN 1.5MT" vs design 0.62 m below LAT: if the chart datum is LAT the charted top is 0.88 m deeper than design; the figure probably copies the design number. Needs Lior's Navionics app reading (A1, A2).
3. PBO3 marginal (+0.62 m): extrapolated seabed beyond the 10 m line (gradient 1:37). The chart's 10-12 m contours would settle it (Lior, Navionics app or a deeper shallow-shading capture).
4. Contour interval of the aerial lines (0.5 m) is assumed; datum of Navionics (LAT) is inferred. The chart bed may be about 0.5 m shallower than the 2013-14 survey (nourishment 2017, 470,000 m3).
5. Palm Beach MSL is not published (Seaway 0.88, Snapper Rocks 1.09 m above LAT); crest -0.62 vs -0.50 m LAT. Local tide table needed.
6. No Google Earth history read (B1-B4): post-2019 state rests on ICM 2023, Prenzler 2022 and Esri 2025-12-01.
7. Camera-match candidates (not done): img-03 (Hunt Fig 5, beach side), img-04 (CCTV frame; camera on the beach about 100 m south of the perpendicular to the reef, +-50 m), img-16 (oblique, dredger).
8. Width label 80 m is nominal (91 m max, 74 m mean); the page should say so (already in shape.json dimension notes).
9. Repo-wide: `check_registry.py` fails for other reefs (Narrowneck unregistered annotated files, Opunake missing overlays); not Palm Beach.

Needs network (blocked in the cloud container; list for when it is widened):
- https://icce-ojs-tamu.tdl.org/icce/article/view/12702 (Daniels 2022): datum and accuracy of the buoy depths in Table 1.
- https://icce-ojs-tamu.tdl.org/icce/article/view/12921 and /13024: full PDFs to quote crest wording and Fig 4 survey legend.
- MSQ tidal planes page for any ocean-beach row near Palm Beach (MSL interpolation).
- https://maps.garmin.com/en-US/marine: re-capture with shallow shading 11-13 m around (-28.1072, 153.4738) for the PBO3 check (own headless Chrome; 3d/navionics_capture.py).
- Google Earth Pro history (Lior's PC).

## 6. Next steps (in order)

1. MAIN: update `04_build/data/models3d_curated.json` (`models.palm-beach-gold-coast.key_numbers` rows "Crest level" and "Toe / seabed depth") and `models3d_caveats.json` (rows "Datum: AHD vs MSL and the tide planes" and "Seabed and reef surface are inferred, not surveyed"), copy `3d/docs.js` / `3d/model.js` into the page build as the update protocol requires, then `python src/update_page.py`. Exact old -> new texts are in the agent's JSON summary (2026-10-10 status entry).
2. Show the 9 re-checked images and the new annotated figure in the Images tab (registry already lists them; `display` true).
3. If Lior supplies Navionics readings A1-A7 or the City as-built survey: re-run `3d/build_3d.py` after editing the constants / adding the points, archive first, compare volumes (before: 22,020 m3, crest height 3.89 m).
4. Camera-match work with img-03 / 04 / 16 in the viewer's photo-match mode.
5. When the network is open: the PBO3 / Daniels datum and the deeper Navionics contours (section 5).
6. Delete `3d/archive/pre_recheck_2026-10-10/` once the re-check is accepted.

## 7. CHECKPOINT 2026-10-10 (Palm Beach re-check agent, finished, not cut off)

Done: steps 1-5 of the task (re-check table, no geometry change, provenance/docs rebuild, registry rows set to checked with a result line, NEW_IMAGES_LOG lines
marked CHECKED, this HANDOFF, status entry). `3d/build_3d.py` last run rc = 0 (log /tmp only); `model.js` and `docs.js` load in node. Not done: viewer
screenshots (Chrome script is Windows-specific and needs three.js from the CDN, blocked here); camera matching; anything needing the network.
No decision for Lior is required; REQUESTS_FOR_LIOR.md (root) was not changed.

## 8. SOURCE AUDIT 2026-10-10
`SOURCE_AUDIT_2026-10-10.md` (statement -> source table, mismatches, citations). METHODS_3D.md now has 2.2 (how each source was used), A12-A14, 3.9 decisions DEC1-DEC15, 3.10 tools/AI statement, three added references; docs.js regenerated (model.js identical). IMAGES.md stale "3D check pending: YES" lines fixed. Open: Prenzler 2022 DOI/pages not confirmed; card volume/offshore wording differs (audit sec 2).

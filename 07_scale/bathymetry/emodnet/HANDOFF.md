# HANDOFF - bathymetry/emodnet (EMODnet Bathymetry feasibility test run 2026-10-06; handoff written 2026-10-10 from REPORT.md and the file list)

Read this first. `REPORT.md` (403 lines, sections 0-11) is the full evidence; open it only for one fact (section numbers given). `METHOD.md` is the step log.
REPORT.md check (2026-10-10): EXISTS and looks COMPLETE (sections 0-11, ends with the reference list of section 11; no TODO/TBD markers found). Not independently re-verified number by number.

## 1. Status per stage
| stage | state | date | confidence / reason |
|---|---|---|---|
| coverage test, 13 reefs | done (REST depth_sample at each coordinate) | 2026-10-06 | HIGH: HTTP 204 vs 200 is unambiguous |
| extraction Boscombe, Borth | done (ERDDAP DTM 2024 cells, WCS releases, profiles, source patches) | 2026-10-06 | MEDIUM: data fine, but cells are 1.5-2.5x the reef |
| Boscombe comparison with the 3D model | done (REPORT section 6) | 2026-10-06 | MEDIUM: offset EMODnet minus model not a datum shift |
| integration into the 3D models | NOT done: spec only (REPORT section 9); Boscombe METHODS_3D/provenance not yet updated from it | - | needs the 3D agents |
| Haifa | one-line check only (section 8, data/haifa_check.json) | 2026-10-06 | paused section 3 of the project |
| images | registered (data/images_registered.json) | 2026-10-06 | - |

## 2. Reefs covered
- Covered (only 2 of 13): boscombe-surf-reef (50.7175, -1.8389) and borth-coastal-defence-reef (52.4835, -4.0562; reef cell is GEBCO interpolation). Not covered (REST returns HTTP 204): 6 Australia (narrowneck, cables, palm-beach, albany, burkitts, bunbury), 2 NZ, 1 USA, 1 India; mexico-reef-2026-unnamed has no coordinate.

## 3. Key numbers (units, datum, source id)
- Product: EMODnet Digital Bathymetry DTM 2024, depths in m relative to LAT (ISO metadata + ERDDAP long_name). Grid 1/16 arc-min: cell 115.8 x 73.4 m (Boscombe), 115.8 x 70.6 m (Borth). Each cell also has min, max, sd, sounding count, interpolation flag, source-survey reference.
- Boscombe reef-centre cell: mean -5.62 m LAT (min -6.21, max -4.87, 12 soundings) = -7.08 m MSL (z_MSL = e - 1.46, D1). Source survey CDI 117452, EDMO 2607 OceanWise Ltd; multibeam >100 kHz, horizontal accuracy <20 m, age class 10-30 y; survey year inferred about 2011-2012 (not stated).
- The reef is not visible in the DTM in any release 2018-2024 (reef outline 4,042 m2 = 48 % of one cell; cell max -4.87 vs model crest +0.56 m LAT).
- EMODnet minus the model seabed: -1.80 m (sd 0.66, range -1.14..-3.05) over 7 cells; reef cell -1.39 m; best-sampled cells (n=12) -1.14, -1.39, -1.30 m; vs April 2011 survey surface -2.11 m; vs 33 Navionics soundings -1.61 m (sd 1.13). EMODnet is deeper; offset not constant, so not a simple datum shift (6.2).
- Boscombe offshore gradient beyond the model grid (y > 380 m, to 650 m): -1.41 % (+-0.10 %); cell means -7.05 (y 380), -8.52..-9.10 (445-505), -10.17 (605) m LAT.
- Borth: reef cells -0.34..-0.13 m LAT, GEBCO interpolation (flagged). Survey cells (CDI 115084): one sounding per cell, age >30 y, horizontal class unknown, start 335 m from the defence line; seaward gradient -1.1 % (about 1:90); cell means -0.40 (y 368), -1.10 (440), -1.91 (513), -2.73 (583), -3.36 (652) m LAT. MSL-LAT at Borth unverified (-2.25 m Aberystwyth unverified; NTSLF lists Barmouth and Fishguard -2.44).
- Finer data: none in EMODnet at either site. Nearest HR DTM: BY_CHERISH_Wales_14m (1/128 arc-min), 22 km north of Borth; 106 km from Boscombe.
- Haifa: same 1/16 arc-min DTM (cell about 115.8 x 97.4 m), cells off Haifa interpolated (JOINT_ISRAEL_NBS_QUARTMIN_GEO, 1/4 arc-min); real IOLR EEZ 2012 multibeam only offshore.

## 4. Rule for the 3D agents (REPORT 0.3, 9)
Take only the datum statement (LAT) and the offshore gradient. Do NOT take crest, toe or reef height, nor the seabed at or around the reef. Boscombe: keep datum assumption A3 (chart datum for Fig 9); add the validation row and provenance. Borth: gradient -1.1 % beyond the toe; convert LAT to MSL only after the offset is verified; beach and foreshore from other sources (Welsh coastal monitoring LiDAR, profiles). Other 11 reefs: use national sources (AusSeabed, LINZ, NOAA) or Lior's readings.

## 5. File map (07_scale/bathymetry/emodnet/)
- `REPORT.md` full report; `METHOD.md` step log; `REQUESTS_FOR_LIOR.md` 5 requests; `agent_final_report.json.md` the run's final JSON; `reefs_coords.csv` coordinates used.
- `data/`: `coverage_all.json`, `haifa_check.json`, `hr_areas.json`, `images_registered.json`; per reef (`boscombe-surf-reef_*`, `borth-coastal-defence-reef_*`): `_points_emodnet.csv`, `_cells_dtm2024_erddap.csv` (143 cells at Boscombe), `_cells_releases_wcs.csv`, `_profile_*.csv`, `_results.json`, `_extract_log.txt`; Boscombe only: `_cells_emodnet_vs_model.csv`, `_points_emodnet_vs_model.csv`, `_comparison_summary.json`, `_emodnet_vs_navionics_soundings.csv`, `_source_patches_2024_near_reef.geojson`.
- `scripts/`: make_coords, coverage_all, cdp (headless Chrome), extract_site, rest_profiles, compare_boscombe, viewer_lib, make_viewer_figures, make_plots, haifa_check, register_images. `figures/` 4 plots; `viewer/` annotated EMODnet viewer screenshots (+ calibration json). Bulky: the CSVs under data/.

## 6. Open issues
1. Survey date/datum of CDI 117452 and 115084: pages behind a bot check (not bypassed). Lior requests 1-3 (open in a normal browser, EMODnet viewer popups).
2. Boscombe offset (-1.8 m LAT frame, -0.3 m if ODN) unattributed: re-open datum A3 only if CDI 117452 shows ODN referencing.
3. Borth MSL-LAT offset needs a tide table (request 5). Finer UK data (Channel Coastal Observatory, UK CHP, Welsh coastal monitoring) not retrieved (request 4, optional).
4. Licence: CC BY 4.0 with originator licences; not for navigation; check before any public release.
5. Interpolation of GEBCO fill at Borth undocumented; WCS 2018 sign flipped; 2016 release coarser and empty here.

## 7. Next steps
1. 3D agents apply REPORT section 9.1 (Boscombe provenance row S5, validation row, offshore gradient) and 9.2 (Borth) when they next touch those models.
2. Lior supplies requests 1-5 if wanted; then update this file and REPORT 6.2.

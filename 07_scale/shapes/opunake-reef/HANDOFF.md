# HANDOFF - opunake-reef (item 9 agent, 2026-10-10)

## 0. STATE 2026-10-13 (agent: Opunake TRC/NZGeo task) - read this first
Lior's two uploads were read (TRC Technical Report 2009-33 = P15, NZ Geographic print = P16). Result: the reef POSITION and design SIZE are now known; the BAG LAYOUT is still not. Full detail: FEASIBILITY.md (verdict), METHOD.md (2026-10-13 steps 1-14), sources.md ("New sources 2026-10-13"), consent_georef.json (every number), shape.json.
| item | result |
|---|---|
| position | Coastal Permit 6376-1 (31 May 2005) occupation area, corners published in TRC 2009-33 Appendix I (PDF p. 39): 189 x 94 m rectangle, 17,726 m2, long axis 63 deg, centre -39.459433, 173.851625. First easting printed 257484 = misprint of 267484. Checked by rectangle closure, GR P20:832-937, and TRC Fig 1 (white rectangle = this area; 4-GCP residual 0.3 m; boat ramp 0.7 m). Card lat/lon now -39.4594, 173.8516 (old -39.46, 173.86 was 720 m east). |
| size | design 99 m long x 30 m wide x 3.5 m high, area about 2,970 m2 (= 99 x 30, bounding rectangle), volume about 4,900 m3 (TRC printed p. 4). 90 x 20 m = 2004 concept (Daily News 11 Jun 2004); 99 x 30 = Blacka 100 x 30. |
| depth / crest | built in 3.0-1.8 m below chart datum (= LAT), shallowest contour 0.0 m below chart datum (TRC printed p. 3). |
| state | 27 bags April 2008, not finished Sept 2009 (TRC printed pp. 4, 15); works Feb 2007 - May 2008 per sign photo. |
| shape | status envelope_only (consent area default outline + optional assumed 99 x 30 m rectangle); NOT the bag outline; page stays hidden; no 3D. |
| registry | 9 new rows img-17..25 (Fig 1, Fig 2, 5 photos, consent page crop, NZGeo hero); check_registry PASSED. |
| dead ends | +5 entries (TRC report partial, NZGeo no figure, construction manual, later TRC reports, imagery in consent area). |
| card | 02_research/reefs/opunake-reef.json/.md: R18 TRC, R19 Daily News 2004, R20 LINZ grid; size, year, design, state, position, gaps updated. |
For main (exact): (1) nothing to un-hide; (2) the card changes are picked up by update_page.py; (3) optional Lior decision in FEASIBILITY.md "Recommendation for main" (show the consent area only). No 3D, so no PAGE_TEXTS_FOR_MAIN.json. 04_build and papers/ untouched.

## CHECKPOINT 2026-10-13 (end of task, nothing in progress)
Done: all of the above. Files changed (this folder): FEASIBILITY.md, HANDOFF.md, METHOD.md, VERIFY.md, sources.md, shape.json, consent_georef.json (new), scripts/ (new: build_consent_georef.py, update_shape_json_2026-10-13.py, proj_grid/nz_linz_nzgd2kgrid0005.tif), overlays/ (2 new), src/ (9 new images + 1 .geo.json). Elsewhere: 03_images/reefs/opunake-reef/ (images.json, IMAGES.md), 03_images/reefs/NEW_IMAGES_LOG.md (9 lines), 02_research/reefs/opunake-reef.json/.md, 02_research/dead_ends/opunake-reef.json, 05_qa/papers_intake/ (2 OCR files), REQUESTS_FOR_LIOR.md and 05_qa/00_STATUS.md (appends).
Next steps for a fresh agent, in order (only if new documents arrive): (1) if TRC/STDC consent file, Black and Mead 2006 manual, Black et al. 2004 or a later TRC report with a plan/survey arrives: trace the bag layout inside the consent area (georeferenced base: LINZ crops in src/, consent_georef.json canonical frame), replace the assumed rectangle, then set status traced and give crest levels with chart datum; (2) Google Earth Pro history (REQUESTS G8) at the polygon corners in consent_georef.json; (3) LINZ tide tables and a chart datum -> NZVD2016/MSL offset for Opunake/New Plymouth before any 3D; (4) then build 3d/ from Borth as template.
Re-running the scripts: build_consent_georef.py (add --overlays; needs the Esri z18 frame in /tmp/claude-0/opunake/, re-fetch command in sources.md) and update_shape_json_2026-10-13.py (idempotent).


(2026-10-10 text below; sections 1-9 are history, superseded in part by section 0.) Source ids = sources.md.

## 1. Status per stage
| stage | state | date | confidence / reason |
|---|---|---|---|
| trace | not possible; shape.json status "no_source", canonical null | 2026-10-10 | LOW: no plan figure, reef not visible on Esri 2025-01-16 z20 |
| verify | VERIFY.md (negative finding only) | 2026-10-10 | - |
| 3D | NOT built; FEASIBILITY.md | 2026-10-10 | plan, crest datum, seabed all missing |
| registry | 10 rows (none shows structure); img-10 gets annotated_files + how_used | 2026-10-10 | - |
| page | main may add slug to 04_build/data/models3d_hold.json ("Not yet modelled"); nothing else | - | - |

## 2. Key decisions
- Did not trace the old wedge schematic (07_scale/reefs/opunake-reef.footprint.json): a placeholder by analogy to Mount Maunganui, not evidence.
- Old overlays (3) archived in overlays/archive_unverified_2026-10-04/ (origin unrecorded).
- Network probe 2026-10-10: Esri, LINZ, nzgeo refused -> everything needing them is in the list below.

## 3. Key numbers
Text only: ~90 x 20 m footprint, 27 bags (2009), north reef only (card R1-R4). z20 frame 0.1153 m/px, capture 2025-01-16, bounds in src/opunake_sat_z20.png.geo.json. No crest, volume, seabed, bearing.

## 4. File map (07_scale/shapes/opunake-reef/)
METHOD.md (log), sources.md, VERIFY.md, shape.json (no_source), FEASIBILITY.md (what is missing), overlays/search_frame_z20_no_structure.png, src/ (4 Esri PNGs 6-28 MB, not worth opening; registry has 3000 px copies in 03_images/reefs/opunake-reef/).

## 5. Open issues / needs network
- Network pass 2026-10-10 done (section 9): LINZ aerials 2011-12 and 2021-22, Esri Wayback 2015-2024: reef NOT visible. Still no plan source.
- Still needed (browser or library): NZ Geographic 078 figure (nzgeo.com, Cloudflare check), TRC Technical Report 2009-33 (trc.govt.nz, Cloudflare check), Black et al. 2004 (ResearchGate, login), STDC consent plans, Google Earth Pro history 2007-2010, Navionics soundings, LINZ chart (login).

## 6. Next steps
1. When network or papers arrive: locate reef (consent plan or historical aerial), georeference, trace (METHOD.md steps), set outline_versions (design drawing vs photo trace).
2. Then crest datum + seabed (LINZ), tide levels (LINZ), then build 3d/ using Borth as template.

## 7. CHECKPOINT 2026-10-10
Stage reached: feasibility only; HANDOFF_STOP for network/papers. Nothing in progress.

## 8. CHECKPOINT 2026-10-10 (second pass, item 9b)
Checked papers/ (5 PDFs), Gemini extracts and 9 web searches: still NO plan source; shape.json stays no_source. Details: FEASIBILITY.md "Checked in the second pass", sources.md "Search log". Done: flag DO_NOT_DISPLAY/display:false added at top of 07_scale/reefs/opunake-reef.footprint.json (file kept); card 02_research/reefs/opunake-reef.json/.md got R15 (Rendle 2016 Table 2.1: A$760,000, 4,800 m3) and the TRC 2009 report lead; no new images (none exist locally). WARNING for main: 04_build/src/compile_data.py load_footprint() still reads that footprint file and may draw the wedge in the reef dialog ("Footprint & how we drew it"); it does not check the new flag (04_build is off-limits to this agent). Ask the 04_build owner to skip footprints with DO_NOT_DISPLAY/display false and add opunake-reef to models3d_hold.json.
Next: only when TRC 2009-33, Black et al. 2004 or dated imagery arrive (see FEASIBILITY "What would give a shape").

## Source audit 2026-10-10
SOURCE_AUDIT_2026-10-10.md in this folder holds the sources-with-how-used, statement check, assumptions (A#), decisions (D#), confidence and consistency tables. FEASIBILITY.md / shape.json now carry the why / checked / assumed text (page_status for hidden reefs). Open mismatches are listed in the audit section 2. If kovalam build_shape_json.py is re-run it overwrites the audit additions in shape.json: re-apply from the audit.

## 9. NETWORK PASS 2026-10-10 (fresh agent)
- Open public data works: LINZ imagery on AWS (s3://nz-imagery/taranaki/..., COG tiles read by HTTP range, no login), Esri Wayback config https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json. WebFetch does not resolve these hosts; use curl. LINZ Basemaps tiles need an API key (not used); nzgeo.com and trc.govt.nz return a Cloudflare challenge (not bypassed).
- Result: no structure visible in LINZ 2011-12 (clear water, 0.4 m) or 2021-22 (0.25 m), nor in 4 distinct Wayback versions. Saved to src/ (linz_aerial_*, esri_wayback_*; .geo.json sidecars) and registered as opunake-reef-img-11..16 (structure_visible false). shape.json untouched (no_source, hidden). Card: R16, R17 and md section. Details: FEASIBILITY.md, sources.md (search log), METHOD.md.
- Next: only a document (P9, P15, P16) or Google Earth history can give a shape; then trace using the LINZ crops as georeferenced base (2011-12 crop: EPSG:2193, 0.4 m/px, top-left 1672970.8 E / 5632659.2 N).

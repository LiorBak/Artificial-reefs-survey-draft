# SOURCE AUDIT 2026-10-10 - boscombe-surf-reef (shape, 3D model, viewer, P5 notes, image registry)

Brief: `_agent_briefs/task_source_audit.md`. Scope: `shape.json`, `METHOD.md`, `VERIFY.md`, `sources.md`, `3d/` (METHODS_3D.md, SOURCES_3D.md, build_3d.py, model.js, docs.js, index.html, model_stats.json), `P5_RENDLE2016_NOTES.md`, registry `03_images/reefs/boscombe-surf-reef/`. Reef card NOT edited (listed below). No model value changed.
Method: read HANDOFF, METHODS_3D sections 1-9, shape.json summary fields; recomputed arithmetic checks (script, no model files touched); compared the rebuilt model.js with `3d/archive/pre_D2/model.js`; grep of 04_build/data texts (read only). Status codes: ok / fixed / missing / mismatch.

## 1. Statement table (grouped; every number of METHODS_3D sections 2-8 was checked against its source line in SOURCES_3D / the S-table)
| Statement / number | Source | Location | How used | Status |
|---|---|---|---|---|
| Outline 25 vertices, 4,042 m2 (model 4,040), 121.1 x 45.0 m, shore normal 173.4 deg | S1, S7 `shape.json` | canonical.polygons_m, area_m2 | plan | ok (4,040 = rasterised area, stated in HANDOFF) |
| Pixel scale 0.37808 m/px | E2, Web-Mercator formula | recomputed 0.378071 | frame | ok |
| E5 colour-bar fit z = -0.02646 Y + 1.455 | S2 Fig. 9 bar ticks | recomputed from ticks | seabed | ok |
| Tide levels HAT 2.59 ... LAT -0.06 m ACD; MSL-based +1.19 ... -1.46 | S3 Table 1 + S4 (1.40) | recomputed all six, MHWS-MLWS 1.76, mean of four 1.375 | tides | ok |
| Crest cover values (E8) | arithmetic | recomputed | tides | ok |
| Crest +0.5 m CD | S3 (design quote), S15 p. 70 (BUILT), Table 4.4 (design 0), Fig. 5.3 (0.3) | A6, E10 | crest | ok (labelled built since 2026-10-10) |
| Loft 13,119 vs 13,000 m3 (+0.9 %) | model_stats.json, S3 | validation 2 | check | ok |
| Seabed under outline -3.56 / -4.72 / -2.40; crest max +0.68 at (20,193); crest-zone areas 1,609/956/296 | model_stats.json | validation 3, 5 | evidence layer | ok (same in METHODS, HANDOFF, model.js) |
| Footprint 4,474 m2 (design) +10.7 %; volume 11,900-12,200 vs 13,119; area >1 m 3,841 vs 4,042 (-5.0 %) | S15, model_stats | validation 2 | validation | ok (percentages recomputed) |
| CCO test +0.03 m (sd 0.30, n 11) vs -1.37 m; beach variability 0.28 / 0.49 / 0.13 m | S13 | validation 9-10, scripts/ | A3, A14 | ok (values as in SOURCES_3D) |
| Navionics: areas, 16 soundings (+0.06, sd 0.49), z16 nearshore (+0.96 etc.), z16 offshore after D2 r.m.s. 0.51 | S9 | validation 5, 6, 11, 12; `scripts/nav_z16_*.json` | validation only | ok |
| EMODnet slope 0.0141 +-0.0010; cells 1.1-3.1 m deeper | S5, S14 | validation 13 | zone 5 slope | ok |
| Zone 5 uncertainty | D2 | section 5 | uncertainty | FIXED: section 5 still said 1.2 m (pre-D2); now 0.5 m since D2 |
| Section 2 line "Not used ... Rendle thesis (blocked)" | - | stale since 2026-10-10 | - | FIXED: thesis added as S15 (validation only); line rewritten, Gemini wording explicit |
| Mead et al. 2010 citation form "32 (ICCE 2010), article 1352" | ICCE OJS listing (WebSearch 2026-10-10) | S3, references | citation | FIXED to Coastal Engineering Proceedings 1(32), structures.58 (OJS 1352); conference 2010, listing dated 2011; DOI not confirmed |
| Rendle and Davidson 2012 citation | Plymouth portal / ICCE OJS | S2, references | citation | FIXED to 1(33), OJS 6794, e-pub 28 Sep 2012; DOI and paper identifier not confirmed (REQUESTS) |
| S14 (project EMODnet report) existed in build_3d.py sources but not in the METHODS S-table | - | S-table | - | FIXED: row S14 added |
| Rendle (2016) thesis not in the viewer source list | - | build_3d.py sources | - | FIXED: S15 added to build_3d.py (model.js `sources`), METHODS S-table and references |
| Each source: "how used" | - | METHODS S-table had "what it contributed" only | - | FIXED: new METHODS 9.1 (read-off, method, accuracy, model element, role per source) |
| Assumptions with effect and replacement | A1-A16 | METHODS 3.8 had text without effect/replacement | - | FIXED: new 9.2 (A1-A16; sensitivities from validation 2 and section 5; A5 effect stated as "not quantified") |
| Decisions logged | - | no decision list | - | FIXED: new 9.3 (BD1-BD12; Lior's D2/D3 cross-referenced) |
| Confidence per element | - | one overall level only | - | FIXED: new 9.4 |
| AI/Gemini influence statement | CLAUDE.md rule 2 | - | - | FIXED: stated in section 2 and 9.5 (no Gemini value used) |
| 3.8 lists A14-A16 before A13 | - | ordering | - | left (cosmetic) |
| Registry: 43 rows, all fields filled (file, citation, URLs, page/figure, date, licence, retrieved, shows, how_used, sha256); `check_registry.py` reports no Boscombe error | images.json | scripts check | - | ok. Note: img-41..43 were added after the HANDOFF (32/40 rows); HANDOFF file map updated |
| img-01 text "exposed mound" | registry corrected 2026-10-07 | - | - | ok in registry; STILL WRONG in card and media_recheck (below) |
| Viewer: source list with citations (Model data panel), Methods panel = METHODS_3D.md + REQUESTS + SOURCES_3D (docs.js) | index.html reads docs.js | verified docs.js parses (node) and contains section 9 | - | ok: assumptions, decisions, methods, source use now reach the viewer through docs.js; no viewer code change needed. Visual render not re-run (CDN unreachable; markdown tables are the same syntax as existing ones) |

## 2. Values that look wrong or disputed (not changed)
1. Local MSL: Rendle p. 70 "1.66 mODN = MSL" vs 1.40 m (NTSLF) used in E6; Navionics boundary test also gave -1.66 m (validation 11). Default 1.40 kept; open (HANDOFF).
2. Distance from pier: S6 "210 m east of pier", Mead (shape.json R-Mead2010) "280 m offshore and east of the pier", Rendle p. 68-69 "240 m east", model west edge 242 m. Different reference points; model uses the traced position.
3. The shoreline step of 1.13 m between rows y = 378 and 380 (D2 limitation, documented).

## 3. Mismatches in files outside my folder (for main / card agent)
- Card `02_research/reefs/boscombe-surf-reef.json`: "footprint about 1 hectare" and "220 m from the seawall base" are literature values; the traced outline is 4,042 m2 and 181-276 m from the surf line (centroid 226 m). Card lacks the 4,042 m2 figure and the datum conversion (CD = ODN - 1.40 m). Card images[0] still describes an exposed mound (picture shows a sand heap).
- `05_qa/reef/boscombe-surf-reef_media_recheck.json`: same img-01 wording.
- Page texts (do NOT edited here), exact old -> new in `04_build/data/models3d_curated.json`:
  - `/models/boscombe-surf-reef/state_short`: "at the design crest +0.5 m ACD" -> "at the built crest +0.5 m ACD (Rendle 2016, p. 70; design 0 m CD, Table 4.4)".
  - `/models/boscombe-surf-reef/confidence_short`: "the as-built crest (designers +0.5 m ACD; Oct 2009 profiles)" -> "the built crest (+0.5 m ACD, Rendle 2016 p. 70 and Mead et al. 2010; Oct 2009 profiles)".
  - `/models/boscombe-surf-reef/key_numbers/0/note`: "Design value used as the as-built crest (A6). An unverified search snippet says the final crest was 0.5 m above design." -> "Built crest per Rendle (2016, p. 70: built crest approximately 0.5 m CD); design was 0 m CD (Table 4.4) or 0.3 m CD (Fig. 5.3 drawing); the same number as the Mead et al. 2010 design quote (A6)."
  - `models3d_caveats.json /rows/10/ev/0` ("The final crest height of Boscombe ASR was 0.5 m higher than the final design height", a search snippet): now confirmed by Rendle p. 70; may be cited with that page.
- After this audit main must refresh `04_build/3d/boscombe-surf-reef/` with the rebuilt `model.js` and `docs.js` (only text, sources, provenance changed; D2 seabed was already applied).

## 4. Rebuild check
`python build_3d.py` run in `3d/` after editing METHODS_3D.md and build_3d.py (new source S15). The pre-audit D2 model.js was overwritten by a parallel agent's file in the shared /tmp before comparison, so the new model.js was compared with `archive/pre_D2/model.js`: differences only in `seabed` (z_cm at y >= 380: 21,779 cells = the D2 change; code_key; extension text), `provenance` (text), `sources` (S15 and wording), `confidence_3d.reason`; `reef`, `stats`, `levels`, shoreline, navionics identical. Conclusion: no value changed by this audit.

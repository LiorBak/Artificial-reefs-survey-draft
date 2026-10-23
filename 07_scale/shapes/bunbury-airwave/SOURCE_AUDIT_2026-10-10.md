# Source audit - bunbury-airwave (2026-10-10)

Scope: `07_scale/shapes/bunbury-airwave/` (shape.json, METHOD.md, VERIFY.md, sources.md, HANDOFF.md, 3d/ model + viewer) and the registry `03_images/reefs/bunbury-airwave/`. Standard: `_agent_briefs/task_source_audit.md`. The reef card was read only. No model value was changed. Reference ids R1-R25 are the card's; S_* / A / V / L / DEC ids are those of `3d/METHODS_3D.md`.

## 0. Result in one paragraph
The folder was already documented to a high standard (sources table, 13 numbered assumptions, validation V1-V11, limitations L1-L11, confidence). Gaps found and fixed in the model's own documentation: (1) no per-source "how used" table, (2) no numbered decisions list, (3) the new source R25 (Troy interview) and the fill disagreement were not recorded, (4) the viewer's Sources list lacked R25. After the fixes the viewer's Methods tab shows: sources with contribution (section 2), source disagreement on fill (2.2), how each source was used (2.3), assumptions A1-A14 (3.8), decisions DEC1-DEC12 (3.9), validation, uncertainty, confidence, limitations L1-L12, references. The Model data tab lists S_Troy among the Sources and carries the disagreement in the "fill" provenance row. Model geometry and every number are unchanged (checked, section 4).

## 1. New source R25 and the fill disagreement (requested)
| statement | source | location | how used | status |
|---|---|---|---|---|
| "Final design uses SAND instead of air; engineers found air did not respond well with the waves" | Bakalo, L. (2026), Zoom interview with Troy, Airwave founder, 8 Oct 2026; personal communication, unrecorded, no transcript; card key `interview_2026_10_10` (R25), recorded 2026-10-10 | card `interview_2026_10_10.fill`; `sources_disagree[0]` | context and disagreement log only; no model value | recorded: METHODS_3D 2.2, A14, DEC12, L12, S_Troy (viewer sources), "fill" provenance row |
| "a seam opened up a couple of days after installation"; worked "amazingly" until then | same | `interview_2026_10_10.failure_mode`, `.performance_before_failure`; `sources_disagree[1]`, `[2]` | context only | recorded in 2.2; verdict stays FAILED (DEC11) |
| ABC: "two-metre-high, 12-metre-wide, dome-like bladder filled with air" | ABC News (2019b), 16 Dec 2019, https://www.abc.net.au/news/2019-12-16/word-first-surf-reef-tears-during-installation/11803228, re-fetched 2026-10-05 | `shape.json` references R1 `accessed` field; `3d/SOURCES_3D.md` fill discussion | cited for 2 m / 12 m / tear; its "air" wording is the only place the folder says air | disagreement recorded with both sources (2.2) |
| Tracks 2019b: "sand + air fill" (washed coarse beach sand for the slurry); Bunbury Mail 2022 and Waveco 2025: sand slurry, 140 / 150 t | as cited in METHODS_3D section 8 | METHODS_3D S_Tracks19, S_BunMail, S_Waveco rows | material label "sand slurry + water + air"; mass not used in geometry (DEC10) | ok |
| Does the model documentation say the fill was air? | model.js `meta.name`, `provenance` "fill", METHODS_3D 1 and 3.5, HANDOFF | - | They say sand slurry (+ water + air); never air-only. The 3D reef is a rigid cap with no fill (A12). | no model change needed; wording clarified (A14) |

Unresolved, both sources kept: whether the Dec 2019 bladder was already the "sand" design Troy calls final, and what "final design" refers to. Ask: REQUESTS_FOR_LIOR.md (appended line E5b).

## 2. Statement-level audit
Columns: statement -> source -> location -> how used -> status (ok / fixed / missing / mismatch).

| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | Base diameter 12 m | ABC 2019b; RWR spot page; Tracks 2019b; Bunbury Mail 2022 | shape.json dimensions_check; METHODS_3D S_* rows | scale of the traced outline (25.59 px/m) | ok |
| 2 | Plan area 112.1 m2 (circle of 12 m = 113.1; -0.9 %) | own trace, img1, 29 vertices; ellipse refit | shape.json canonical.area_m2; VERIFY checks 1-7; METHODS_3D 3.3 | plan; agreement is by construction (documented) | ok |
| 3 | Oblique tilt 26.5 deg, ellipse semi-axes 153.6 / 137.4 px, RMS 1.27 % | own refit (Fitzgibbon) | shape.json img1 evidence; arccos(137.4/153.6) = 26.5 deg checked | rectification | ok |
| 4 | Outline uncertainty 15 %, scale +-7 % | judgement of trace + verifier | shape.json confidence; L11 | confidence | ok (labelled judgement) |
| 5 | Height 2.0 m (1.6-2.0) | ABC, RWR (2 m); Tracks 2019b (1.6 m) | A4; DEC8 | cap height range | ok |
| 6 | Crest "about 1 m under the surface at low tide" | RWR spot page | A6 (low tide = MLLW, assumed); V1, V2 | validation of seabed/position | ok |
| 7 | Offshore distance 30-50 m, default 37.5 m | RWR 30-45 m; Tracks 45 m off low-tide mark; SurferToday 50 m | A2; DEC9 | y position | ok |
| 8 | Seabed -2.58 m AHD at y = 37.5 m; profile y = 20..200 m | WA DoT (2009) Lidar2009TRBS BAG, 67,442,256 bytes, md5 in METHODS_3D S_lidar | METHODS_3D 3.4; data/lidar_clip_model_frame.csv; computed.json (z375 = -2.58) | seabed grid, 10 m to 5 m bilinear, surf-zone gap fill E9 (286 of 2989 nodes) | ok |
| 9 | Lidar uncertainty 0.47 m read as 1 sigma | BAG uncertainty layer | A10 | error budget | ok (assumption labelled) |
| 10 | Tides HAT 0.6 ... LAT -0.6 m AHD, MSL = +0.1 m AHD | GHD (2021) Table 1 (from Dept of Defence 2018, not seen directly); DoT index LAT offset 0.57 | A9; METHODS_3D 3.2; computed.json lat_diff 0.03 | datum conversion z_MSL = z_AHD - 0.1 | ok |
| 11 | Navionics datum LAT, RMS 0.32 m (n = 111) | Garmin Navionics web viewer, 2026-10-05; nav_annotate.py | 3.6; V4, V5; A11 | validation only | ok |
| 12 | Crest depth 0.69 +- 0.66 m (Monte Carlo) | own propagation E15-E17 | METHODS_3D 5; computed.json mc_mean 0.69, mc_sd 0.66 | uncertainty | ok (HANDOFF, page JSON agree) |
| 13 | Volume cap 117.3 / 92.6 m3, R_s 10.00 / 12.05 m, rim 36.9 / 29.9 deg | own arithmetic E10-E14 | computed.json | derived | ok (verified equal in HANDOFF, models3d_curated.json) |
| 14 | Sand 140 t (Tracks 2021, Bunbury Mail 2022) vs 150 t (Waveco, forum summary); 70-94 m3, 60-80 % of cap | developer; own arithmetic V8 (bulk density 1.6-2.0 t/m3, assumed) | METHODS_3D V8, L10 | plausibility only | ok |
| 15 | Install week of 9 Dec 2019, tear spotted Fri 13 Dec at ~90 % complete, removed in 5 h to 3 days | ABC 2019b; RWR 2019b; Bunbury Mail 2022; Swellnet forum (secondary) | METHODS_3D 2.1; HANDOFF 3.6 | state modelled | ok (removal time: sources differ, stated) |
| 16 | Waveco "2018" | Waveco 2025 | METHODS_3D 2.1 table | rejected, contradicted by dated 2019 reports | ok |
| 17 | Wave 0.75 m, "peeled nearly to the beach" | Bunbury Mail 2022 (Bottegal, self-reported) | HANDOFF 3.6 | context only | ok |
| 18 | Cost A$75,000 (City of Bunbury, June 2019); total US$350-400k | card R1/R2/R3/R10 | HANDOFF 3.2 | context | ok (sources disagree, stated) |
| 19 | Site point -33.32767, 115.62880; card lat/lon (-33.31, 115.64) ~2 km off | 2009 0 m AHD contour + Esri 2025 tile; card | shape.json location_note; HANDOFF 5.1 | frame origin | MISMATCH (card vs model; known, listed; card is read-only, main to fix) |
| 20 | Registry: 21 ids; files present; sha256 of every file matches; no empty citation, link, licence, date, shows, how_used field | `03_images/reefs/bunbury-airwave/images.json` (script check) | - | - | ok |
| 21 | Registry titles use "inflated bladder" (ids 06, 08), "inflatable" (01) | titles taken from the press captions | images.json | wording only; describes the press captions, not the fill | ok (note) |
| 22 | Gemini footprint (24-gon, 113 m2) and 8 further Gemini claims | not used; recorded as contradicted / unsupported | shape.json gemini; VERIFY | rejected, rule 2 | ok |
| 23 | Tradie Magazine 2019 "very subtle, flattened dome with a steeply angled back" | search text only (page 403) | METHODS_3D 3.5 | asymmetry hint, not a number | ok (limit stated) |
| 24 | Per-source "how used" | - | METHODS_3D | there was only a "what it contributed" column | FIXED: new 2.3 table |
| 25 | Numbered decisions | - | HANDOFF had 10 decisions, METHODS_3D had none | FIXED: new 3.9, DEC1-DEC12, who and when |
| 26 | Interview R25 + fill disagreement | card | not in any model file | FIXED (section 1) |
| 27 | Assumption on fill | - | A12 said "no fill drawn" only | FIXED: A14 |
| 28 | Limitation on fill record | - | - | FIXED: L12 |
| 29 | Viewer source list lacked R25 | model.js sources (18) | build_3d.py | FIXED: S_Troy added (19 sources) |

Counts: 29 rows; ok 22, fixed 6, mismatch 1, missing 0. "Statements checked" counts distinct numbers or claims; roughly 60 individual figures were compared against computed.json / shape.json / HANDOFF / models3d_curated.json with no difference.

## 3. Citations
Section 8 of METHODS_3D has full citations with URLs and access dates for 21 items. Added: Bakalo (2026), the Troy interview. Not confirmed (left as is, no invention): Department of Defence (2018) tidal planes (cited via GHD 2021, not seen); Tradie Magazine 2019 and SurferToday 2019 (seen in search text only); Swellnet thread (anonymous, secondary). Authors of the 2019 ABC, Tracks and RWR articles are not given in the section 8 entries (ABC photo credit "De Poloni, Gian" is in the registry). WebSearch (2 queries, 2026-10-10) did not return the ABC 2019b or Tracks 2019b article pages or their bylines, so those author names are NOT confirmed; listed in REQUESTS_FOR_LIOR.md (E5b).

## 4. Rebuild check
`python build_3d.py` was run only to refresh documentation. model.js before/after compared as JSON: changed fields = `meta.built` (date), `meta.verdict_reason` (the card now carries the 2026-10-10 update with R25), one new entry in `sources` (S_Troy), `provenance[1].uncertainty` (fill-row text). No geometry, grid, tide or number changed. computed.json: only `build_date`, `verdict_reason`, `ref_ids` (now includes R25). index.html unchanged (md5 identical). Line endings kept CRLF (model.js, docs.js, METHODS_3D.md, SOURCES_3D.md, computed.json, build_3d.py, template).

## 5. Values that look wrong (for main)
None in the model. One card/model mismatch: the card's `lat`/`lon` (-33.31, 115.64) is ~2 km from the traced site (-33.3276, 115.6284); the card is read-only here.

## 6. Page text edits for main (04_build/data, not edited)
`models3d_curated.json` /models/bunbury-airwave/state_short
- old: "As installed, December 2019: 12 m sand-slurry bladder, torn along a glued seam before completion (card verdict FAILED). Geometry only; it never operated as a reef. Removal, redesign and the 2025 granite proposal are not modelled."
- new: "As installed, December 2019: 12 m rubber bladder with a sand-slurry fill (press also mentions air; the developer says the final design uses sand instead of air), torn along a glued seam before completion (card verdict FAILED). Geometry only; it never operated as a reef. Removal, redesign and the 2025 granite proposal are not modelled."
Optional, `models3d_caveats.json`: add a caveat "Fill type: sources disagree (ABC 'air'; Tracks 'sand + air'; developer interview 'sand instead of air'); the model draws no fill. See METHODS_3D 2.2."

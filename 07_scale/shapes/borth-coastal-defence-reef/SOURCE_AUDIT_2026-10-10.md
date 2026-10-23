# SOURCE_AUDIT_2026-10-10 - borth-coastal-defence-reef (shape files, 3d model and viewer, image registry)

Auditor: fresh agent, 2026-10-10, brief `_agent_briefs/task_source_audit.md`. Scope: this folder and `03_images/reefs/borth-coastal-defence-reef/`. The reef card (02_research/reefs/borth-coastal-defence-reef.json) was read-only for comparison. No model value was changed; `3d/model.js` is byte-identical before and after the rebuild (checked with cmp); `shape.json` changed only in the ref6 first name. Primary sources were not re-read (HANDOFF/VERIFY/METHODS were trusted for page numbers); citations were completed or confirmed by web search where possible.

Status: ok / fixed / missing / mismatch (mismatch = recorded, not a model value error).

| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | MSL = +0.31 mODN = mean of MHWS 2.56, MHWN 1.06, MLWN -0.64, MLWS -1.74 | ref3 SMP2 p.4C.3 | METHODS 3.1 E1; model.js datum | recomputed: (2.56+1.06-0.64-1.74)/4 = 0.31 | ok |
| 2 | z_MSL = e_LAT - 2.75 | ref4 + A2/A3 | METHODS 3.1 E3 | 0.31 + 2.44 = 2.75 | ok |
| 3 | volumes 30,119 / 28,919 / 25,504 m3; tonnes 51,203 / 49,162 / 43,357 at 1.7 t/m3 | model | model.js versions[]; HANDOFF 3.4; METHODS 3.3 | recomputed volume x 1.7 | ok |
| 4 | bed uncertainty 0.4 m x 11,391 m2 = 4,556 m3 (15 %) | A6 | METHODS 5 E9; provenance row | recomputed | ok |
| 5 | footprints 8,675 / 6,989 / 5,743 m2 | LiDAR / drg1020 / sat2024 | model.js, shape.json outline_versions, HANDOFF 3.4, METHODS 1 | compared | ok |
| 6 | tide levels and LAT -2.44 in the viewer | ref3, ref4 | model.js levels vs METHODS 3.1 | compared | ok |
| 7 | confidence MEDIUM, same reason in model.js, METHODS 6, HANDOFF 1 | - | - | compared | ok |
| 8 | HRPP576 citation (authors, title, venue, Edinburgh Sept 2013, eprint 931) | HR Wallingford eprints | ref1, METHODS 2, img-17/18 | confirmed by WebSearch 2026-10-10 (authors Rigden, Stewart, Allsop, Johnson; ICE Coasts, Marine Structures and Breakwaters; CC BY) | ok |
| 9 | ref6 author "Hansford, M." | reef card R1 "Mark Hansford" | shape.json ref6, METHODS 2 and 8 | first name added | fixed |
| 10 | ref6 article itself (275,000 t; Type 4 42,000 t) | New Civil Engineer 2011-09-15 | - | not re-found by web search on 2026-10-10; the card cites it as R1 with the same numbers | missing (page/URL not re-verified; added to REQUESTS) |
| 11 | Coflein "about 300,000 t", completion 8 Mar 2012 | ref7 coflein.gov.uk NPRN 424699 (quoting BBC, 8 Mar 2012) | METHODS 2 | search result confirms the BBC quote | ok |
| 12 | registry has 30 rows (HANDOFF, text) | images.json | HANDOFF 1, 4; images.json | registry has 31 rows (img-31 Blacka et al. 2013 added 2026-10-10); check_registry.py shows no Borth error | fixed (HANDOFF, METHODS 2 updated) |
| 13 | img-31 (Blacka et al. 2013, Fig 4.1) is not in METHODS references | DOI 10.4225/53/58e1dc7368c7a | METHODS 8; REGISTER_3D R1 | added as context-only reference | fixed |
| 14 | LiDAR crest statistics: N arm p90 +0.91 (METHODS 4.2) vs +0.72..+0.88 (VERIFY, img-24) | LiDAR SN6089 | METHODS 4.2; VERIFY 3D inputs; img-24 | different cell masks, neither is a model input (crests are design values) | mismatch (explained; note added to img-24 in images.json and IMAGES.md; REGISTER_3D R6) |
| 15 | each source "how used" | - | METHODS 2 listed what each contributed but not how read, accuracy, rejected | new table R1 in `3d/REGISTER_3D.md` | fixed |
| 16 | assumptions A1-A13 lacked effect, evidence and replacement per item | METHODS 3.5 | - | table R3 (effects quote only existing numbers; unquantified effects say "not quantified") | fixed |
| 17 | implicit assumption: Aberystwyth/Barmouth/Fishguard tide data apply at Borth | ref3, ref4 | - | A14 added | fixed |
| 18 | decisions scattered over HANDOFF 2, SOURCES_3D, METHODS 3.3 | - | - | decision log DEC1-DEC14 (R4) with options, who, when, reason | fixed |
| 19 | methods and scripts not listed in one place | - | - | table R2 with parameters and script paths | fixed |
| 20 | viewer shows source list with "how used", assumptions, decisions | index.html, docs.js | Methods tab | added third document REGISTER_3D to docs.js (build_3d.py) and a button in the Methods tab; pointer line added to the Sources tab. Checked with node: the viewer's own md() renders 5 tables, 6 h2 from register_md, no raw pipes. NOT checked in a browser (no Chrome in this session, nothing installed) | fixed (render check partial) |
| 21 | model.js unchanged by the documentation rebuild | - | - | cmp against the pre-audit copy: identical | ok |
| 22 | HRPP576 Fig 2 contour reading +-0.5 m / +-10 m | by eye | METHODS 3.3, provenance | stated, not independent | ok (low accuracy, labelled) |
| 23 | Navionics: cross-check only, datum assumed LAT | A13 | METHODS 3.6 | labelled ASSUMED | ok |
| 24 | Gemini footprint (12,500 m2, 110,000 t, Halcrow) rejected | VERIFY check 6 | shape.json gemini | rejection recorded; now in REGISTER_3D R1/DEC10 | ok |
| 25 | Aberystwyth chart-datum offset Z0 and HAT | Admiralty / UKHO | METHODS 7 | not at a primary source; already in REQUESTS_FOR_LIOR.md (3d request row 6) | missing (open, requested) |
| 26 | oval crest length 38 m (SOP table) vs 46 m (drawing 1023 dimensions) | drg1020 / drg1023 | HANDOFF 5.6 | worth about 2 % of the oval volume; logged as DEC11 | ok (open choice, flagged for main/Lior) |
| 27 | who/when for DEC5, DEC8, DEC11-DEC14 | - | - | not recorded explicitly in the logs; attributed to the "3D agent, 2026-10-06/07" from SOURCES_3D and METHODS | ok (attribution inferred, stated as such here) |
| 28 | page texts in 04_build/data (Borth): 36,100 t, -3.86, 15 % | model | models3d_curated.json, models3d_caveats.json | already updated (no old 36,600 / -4.04 / -4.72 found) | ok |
| 29 | card: north reef 72 x 170 m, south reef 85 x 45 m, "crest at MSL", depth 4.0 m | Blacka et al. 2013 Table 4.2/4.3, superseded two-reef design | reef card `size` field | model (final layout): N mound 144.9 m long, mean width 27.6 m, crest +0.19 m MSL (arm); S oval 71.8 x 31.0 m, crest +1.19 m MSL | mismatch (card is about the superseded design; for the card agent, not edited) |
| 30 | card: reef 400 m (contractor) / 300 m (Coflein) / 110-140 m (Blacka) offshore | - | card `size` | model: centroid 330.5 m from the defence line (nearest edge 257 m, farthest 397 m) | mismatch (sources disagree; documented in the card; no change) |
| 31 | card: Type 4 42,000 t, 275,000 t, 300,000 t | ref6, ref7 | card `size` | same as METHODS 2 and HANDOFF | ok |
| 32 | registry rows 1-30 carry citation, link, licence, date, shows, how_used | images.json | - | spot checks img-17, 24, 31: complete; check_registry.py: no Borth error; one row still pending_3d (img-31, not used by the 3D build) | ok |
| 33 | 3D confidence per element | - | METHODS 6 | table R5 (plan, crest, tides, seabed, volume, overall) | fixed |
| 34 | ref4 LAT -2.44 and ref3 table values, Fig 2 scale, drawing labels | primary sources | - | not re-read in this audit (trusted from VERIFY / METHODS, accessed 2026-10-06) | ok (not re-verified) |

Counts: 34 statements checked: 19 ok, 10 fixed, 2 missing/open (rows 10, 25), 3 mismatches explained (14, 29, 30). Row 20 is fixed but the browser render was not checked (no Chrome available). Rows 29 and 30 concern the card, not the model.

## Values that look wrong
None found. Plan, tide arithmetic, volumes and tonnes recompute from the model's own inputs. Open choice only: oval length 38 m vs 46 m (row 26).

## Page text edits for main
None needed for the 3D numbers (already current). Optional wording: where the page names the New Civil Engineer article, use "Hansford, Mark (2011)". For the card agent: `size` field quotes Blacka et al. dimensions of the superseded two-reef design (row 29).

## Files changed
`3d/REGISTER_3D.md` (new), `3d/METHODS_3D.md` (section 2 pointer, Hansford, Blacka reference), `3d/build_3d.py` (docs list), `3d/index.html` (Methods tab buttons, Sources tab pointer), `3d/docs.js` (rebuilt), `shape.json` (ref6 name), `HANDOFF.md`, `SOURCE_AUDIT_2026-10-10.md`, registry `images.json` and `IMAGES.md` (img-24 note). Backups of the pre-audit files were kept only in /tmp.

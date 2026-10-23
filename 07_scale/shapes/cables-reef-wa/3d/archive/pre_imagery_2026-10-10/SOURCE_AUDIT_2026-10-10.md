# Source audit 2026-10-10 - cables-reef-wa (shape, 3D model, viewer, image registry)
Standard: _agent_briefs/task_source_audit.md. Status: ok / fixed / missing / mismatch. Model values were NOT changed (model.js recompiled only to refresh docs.js; areas, volumes, thicknesses, edge levels identical to the pre-audit values; no byte backup of the old model.js was kept, comparison by the printed values).

| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | footprint 4,049 m2 (121 x 76 m); with extension 4,355 m2 (121 x 89) | Blacka et al. 2013 Fig A.2 [img-26]; RWR extension [img-06] | p.93; drawing | trace, scale 6.51 px/m | ok |
| 2 | scale 6.51 px/m sd 0.05 (+-3 %) | printed 26.0/30.0/40.0 m, 0.5 m contours at 1:20 | Fig A.2 | four readings, annotated/A1 | ok |
| 3 | crest RL -1.0, set-out RL -3.0, contours -1.5/-2.0/-2.5, slopes 1:20/1:15/~1:13 | Fig A.2 labels; Pattiaratchi 1999 p.3 | as left | labels read | ok |
| 4 | datum: MTL 0.78 m above datum | Pattiaratchi 1999 p.3 | text | reading A (assumption A1), B switch | ok (now A1 / X3) |
| 5 | tide range 0.8 m | Blacka 2013 Table 4.3 p.67 | table | water slider; HW/LW +-0.4 m = estimate A7 | ok |
| 6 | rock volume 5,500 / 5,000 / 3,500 m3 | Blacka A.1.3; Mead and Borrero 2011 p.2; Wikipedia (card R1) | | 5,500 fits bed (A3); others sensitivity | ok |
| 7 | 140 x 70 m, 275 m offshore, depth 3.0-6.0 m, crest 1.0-2.5 m below MSL | Blacka A.1.1, Tables 4.2 p.65 | | validation only | ok |
| 8 | 250 m offshore, 45 deg peel angle, 1:20 slope to the 1 m contour | Pattiaratchi 1999 p.3-4 | | cross-check, orientation | ok |
| 9 | bed gradient 1:30 | Pitt sketch [img-07], contours 3.0-7.0 m | annotated/A4 | read by eye, assumption A4 | ok |
| 10 | bed level RL -3.50 m (y = 270 m) | fitted to 5,500 m3 | build_3d.py D0, G_BED | calibration (A3) | ok, flagged estimated |
| 11 | extension 347 m2 / 320 m3 / 0.92 m mean | RWR drawing [img-06] | 'VOLUME = 320 m3' | triangle registration (A6) | ok |
| 12 | max rock thickness | model.js 2.48 m | | | mismatch fixed: METHODS_3D said 2.9 m, now 2.5 (2.48); HANDOFF already 2.5 |
| 13 | assumptions A3-A7 cited in METHODS_3D with no list | | | | fixed: section 9 A1-A11 added (viewer Methods tab) |
| 14 | decisions not logged | | | | fixed: section 10 X1-X8 added |
| 15 | sources without "how used" for Mead and Borrero, Wikipedia, card, Pitt 2009, Gemini | | | | fixed: SOURCES_3D table "Sources and how each was used" |
| 16 | density 1.82 t/m3 from '> 10,000 t' | card (RWR/ICM text, R2) | | plausibility check only | ok (card figure is a lower bound) |
| 17 | Pitt 2009 'crest ~1.5 m below lowest tide' | card dossier (SurfingRamps.com.au), original not read | | context | ok, second-hand, labelled |
| 18 | Gemini | not in this repo | | none used | ok (X7) |
| 19 | Blacka citation incl. DOI, Pattiaratchi 1999 ref ED1483CP and URL, Mead and Borrero DOI | registry/card | | | ok |
| 20 | Pattiaratchi et al. 2003 | UWA repository listing | COPEDEC VI, Colombo, 15-19 Sep 2003 | not read | citation completed (venue, date); co-authors, pages NOT CONFIRMED |
| 21 | Bancroft 1999 UWA thesis | web search | title only | not read | partial; degree, pages NOT CONFIRMED; possible as-built source |
| 22 | Ranasinghe et al. 2001; Lyons 1992 | cited by Blacka | | not read | NOT CONFIRMED (web search found nothing) |
| 23 | image registry: 31 rows, all files exist, citation / licence / retrieved / page or figure / how_used present | images.json | | | ok; img-14 and own figures 27-31 have no image_url by nature |
| 24 | materials: granite (Blacka, RWR) vs limestone (Mead and Borrero 2011) | | | not used in the model | discrepancy listed, unresolved |
| 25 | reef card vs model: 275 m offshore vs S1 250 m, volume 3,500 vs 5,500, 140 m vs 121 m traced | card; HANDOFF section 5 | | | mismatch recorded, not a model error; page text states ranges |
| 26 | PAGE_TEXTS_FOR_MAIN.json key_numbers | | | | fixed: sources and assumed/fitted labels added; numbers unchanged and consistent with model.js |
| 27 | viewer panels: Sources and Methods tabs show source list, methods, assumptions, decisions | docs.js | | | fixed (content in the two md files; docs.js rebuilt, parses) |

Counts: 27 rows; checked statements ~45; fixed 6 (12-15, 20 partly, 26, 27); missing citation details 3 (rows 20-22). Values that look wrong: none.
Page texts (04_build/data): not edited; main should use the revised 3d/PAGE_TEXTS_FOR_MAIN.json (old -> new in that file's key_numbers lines).

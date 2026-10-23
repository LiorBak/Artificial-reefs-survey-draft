# Cards citations audit, all 13 cards (2026-10-10)

Scope: `02_research/reefs/<slug>.json` + `.md` of the 13 reef cards. Standard: `_agent_briefs/task_source_audit.md` (every statement has a source). Follows `cards_group_A_2026-10-10.md` and `cards_group_B_2026-10-10.md`.

## Method
1. Script scan of every narrative field (hover_text, purpose, type, size, cost, financed_by, motivation, designer, contractor, year, status_now, design_as_planned, as_built_vs_design, outcome, why_worked_or_failed, unexpected_results, could_be_better, relevance_to_israel, gaps, verdict_reason, sources_disagree): sentences (split on full stops, abbreviations like "et al." respected) that contain a digit OR are longer than 45 characters, and carry no `[R#]` tag. Start state: 172 flagged over the 13 cards (the 183 of group A were counted with a splitter that also cut at semicolons; the audits had already tagged some). End state: about 70 remain, all of them (a) meta statements in `gaps`/`verdict_reason` that describe the card's own state, (b) sentences that are labelled "negative finding of this card" / "(unsourced)" / "INFERENCE" / "DERIVED" in the text, or (c) splitter false positives (a quotation cut at its full stop; the tag follows).
2. Each flagged sentence was matched to a reference by that reference's `supports` field and the card's own paragraph tags, then to the shape files (`07_scale/shapes/<slug>/HANDOFF.md`, `SOURCE_AUDIT_2026-10-10.md`, `3d/METHODS_3D.md`) for the model-derived values. Web pages were not re-fetched (network blocked); WebSearch used for the checks below.
3. Where a sentence sits in a multi-source paragraph and the pages cannot be re-read, the tag group of the paragraph was copied to the sentence and the text says so ("paragraph-level attribution"), never a guessed single source.
4. Edits: JSON loaded, edited, written back with the same indent, line endings (CRLF kept on cables, kovalam, mexico, palm-beach, albany, burkitts, bunbury), key order and field types; all 13 parse; every `[R#]` has a reference. The `.md` dossier prose differs from the JSON wording, so each card's `.md` got the same replacement where the identical text exists, and otherwise a "Citations audit 2026-10-10" section at the end listing the new JSON wording.

## Fixes asked for
| # | item | result |
|---|---|---|
| 1 | Opunake R4 (SurferToday) | 31 `[R4]` tags removed from JSON and md; R4 marked "NOT READ" (blocked 403 also in Wayback) with supports "nothing"; each R4 sat beside R2. |
| 2 | Albany 6-8 s; tonnage | The 6-8 s is now attributed to the 4Surfers forecast cross-check (Lior's notes p.1); his buoy readings 5.7-6.2 s (pp.3-4, 6 and 15 Aug 2025) [R12]; the 0.45-0.6 m stays his buoy-based definition. Tonnage: `type` now states 62,800 t (City design table [R3]) and keeps ~70,000 t [R6] as a rounded journalistic figure; 34,000 m3 marked DERIVED (62,800 / assumed 1.85 t/m3, shape agent's assumption; the 70,000 t would give ~37,800 m3). |
| 3 | Mexico "unveiled 16 April 2026" | Reworded in year, status_now, hover_text, outcome, R9 and md: R1 is a 31 March 2026 announcement that bills a reveal event for 16 April 2026; no source seen reports it took place. `07_scale/shapes/mexico-reef-2026-unnamed/HANDOFF.md` line 15 corrected the same way (the one permitted edit there). |
| 4 | Coordinates | See table below. |
| 5 | Burkitts 9 m dive depth | The dive-site sentence rewritten: the marine-park dive site "Burkitts Reef" [R10][R15] is NOT established to be the surf break (registry img-06/07 reject the dive video, Lior 2026-09-25); the ~9 m depth is not used for the surf reef; R10 supports text qualified. |
| 6 | Kovalam cost_usd_approx | Corrected 1,100,000 -> 1,580,000 (integer kept) = Rs 75,000,000 / 47.44 (2009-10 average rupee rate, RBI series via the MoSPI dataset, WebSearch result https://dataful.in/datasets/586; RBI daily reference rates 27 Apr 2010 Rs 44.45 and 15 Jun 2010 Rs 46.73 bracket it). Secondary source, RBI table itself not opened: stated in the card. hover_text now ~US$1.6M. |
| 7 | Mount Maunganui 17th vs 18th | WebSearch (proceedings.com listing): Coasts and Ports 2007 = joint 18th Australasian Coastal and Ocean Engineering Conference, Melbourne, 18-20 July 2007. The card (18th) is right; `07_scale/shapes/mount-maunganui-reef/shape.json` sources text corrected (that one field only). |
| 8 | Pending page-edit CARD items | Checked first, already applied by today's audits: Boscombe 1 ha / 220 m note and img-01 wording (images[0].depicts says sand heap); Narrowneck crest, volume, containers (size, as_built_vs_design); Palm Beach offshore/width (size, gaps); Pratte's V size and bag mass (as_built_vs_design); Mount Maunganui crest depth (type). Applied now: Borth `size` Blacka dimensions marked as the superseded two-reef design. `05_qa/reef/boscombe-surf-reef_media_recheck.json` still says exposed mound: not a card, not edited. |

## Coordinates (lat/lon = the reef, not the town)
| card | before | after | distance | source of the position |
|---|---|---|---|---|
| narrowneck | -27.986629, 153.434052 | unchanged | 11 m | traced centroid (shape.json geo) |
| cables | -32.0, 115.74 | -32.01575, 115.748417 | ~1.9 km | Mondo.surf surf-spot listing (found by search, page not opened, commercial, UNCONFIRMED); no georeferenced shape exists. Flagged in the card and REQUESTS |
| prattes | 33.915123, -118.432624 | 33.92058, -118.43335 | ~600 m | model position hint, +-150 m (decision J2), Fig 9 survey window of Borrero & Nelsen 2003; note in the card |
| mount-maunganui | -37.6447833, 176.2025908 | unchanged | 5 m | shape.json centroid |
| opunake | -39.46, 173.86 | unchanged, UNVERIFIED | - | no source locates the reef; value rounded to 0.01 deg (~1 km); note added |
| boscombe | 50.7185, -1.8417 | 50.717532, -1.838909 | 228 m | shape.json geo.centroid_latlon |
| kovalam | 8.4004, 76.9787 | 8.387313, 76.975188 | 1,507 m | mean of traced default outline (LOW confidence trace) |
| borth | 52.48533, -4.05103 | 52.48346, -4.05621 | ~480 m | area-weighted centroid of the two traced mounds |
| palm-beach | -28.107334, 153.470913 | unchanged | 6 m | traced centroid |
| albany | -35.0236, 117.9136 | -35.018005, 117.920991 | ~900 m | reef centroid in HANDOFF section 3 |
| burkitts | -24.8205, 152.4625 | -24.8157, 152.4675 | ~740 m | traced rock-platform polygon (the platform that carries the reef, LOW) |
| bunbury | -33.32767, 115.6288 | unchanged | ~40 m from the model site point | 3D model site point (already fixed by group A); stale gaps text replaced |
| mexico | null | null | - | no source |
All stay numeric (float / null). Each changed or unverified card has a dated "Position" item as the last entry of `gaps`.

## Per-card counts (sentences flagged at start / tagged / marked DERIVED / labelled unsourced, inference or negative finding / removed)
| card | flagged | tagged | derived | labelled | removed | notes |
|---|---|---|---|---|---|---|
| narrowneck-gold-coast | 18 | 9 | 2 | 2 | 0 | 147 m3 per container derived from Jackson 2007 Table 2 / p.4; Haifa-tide inference labelled |
| cables-reef-wa | 9 | 5 | 2 | 2 | 0 | R21 added (Pattiaratchi 1999 design paper = project source S1); -13 % / +9 % derived |
| prattes-reef-el-segundo | 15 | 10 | 0 | 3 | 0 | "to be resolved" replaced by 23-24 Apr 2001 [R28]; UV sentence sourced to the diver survey [R4][R2] |
| mount-maunganui-reef | 8 | 3 | 0 | 2 | 0 | superseded "no crest figure" sentence |
| opunake-reef | 14 | 8 | 1 | 3 | 31 tags (R4) | |
| boscombe-surf-reef | 9 | 6 | 0 | 0 | 0 | |
| kovalam-reef-india | 10 | 3 | 4 | 3 | 0 | cost_usd_approx corrected |
| borth-coastal-defence-reef | 8 | 3 | 0 | 3 | 0 | R21 added (Haifa tide table, not primary) |
| palm-beach-gold-coast | 11 | 4 | 1 | 0 | 0 | |
| southern-ocean-surf-reef-albany | 7 | 5 | 1 | 1 | 0 | |
| burkitts-reef-bargara | 22 | 17 | 0 | 8 | 1 sentence rewritten (dive site) | R18 added (Haifa tide table) |
| bunbury-airwave | 23 | 8 | 0 | 6 | 0 | stale gaps coordinates replaced |
| mexico-reef-2026-unnamed | 20 | 9 | 0 | 12 | 0 | "unveiled" reworded |
Counts per card are tallied from the edit scripts and are approximate (+-2). Totals: 174 flagged, about 90 tagged, 11 derived, about 45 labelled, 3 references added (cables R21, borth R21, burkitts R18) plus the 1 reworded.

## Items left unsourced or unconfirmed
1. Bunbury "2-8 ft face range": still labelled UNSOURCED (no reference gives it).
2. Narrowneck relevance: Lior's hypothesis that Haifa's small tide is an advantage rests on R18 (his notes); no sourced Haifa tide figure on the card; the inference is labelled.
3. Kovalam relevance: Kerala tide regime statement and Kovalam-vs-Israel wave-energy comparison: card author's, labelled (unsourced).
4. Burkitts: swell season Nov-Apr, Israeli wave climate, "gutter that split the wave" detail, rock more durable than bags: no isolated source; labelled.
5. Mexico: "harder surface complaints at Palm Beach Reef": no source in either card; labelled (unsourced).
6. Opunake coordinates: no source; Cables coordinates: weak listing only.
7. Kovalam rate: secondary (MoSPI/RBI dataset via search), RBI table not opened.
8. Prattes: Borrero & Nelsen 2003 venue/year still unconfirmed (group A).
9. Cables R19-R21: Bancroft thesis not read; Pattiaratchi = Hutt et al. identity not confirmed.
10. Wikipedia revision dates, "n.d." web-page authors and dates, forum summaries (Bunbury 150 t) remain as in the group A and B audits.
11. Albany: AUD 20,000 repositioning cost, single secondary source (unchanged).

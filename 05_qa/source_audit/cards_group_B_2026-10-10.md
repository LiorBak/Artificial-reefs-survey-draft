# Source audit, reef cards group B (2026-10-10)

Cards: cables-reef-wa, opunake-reef, kovalam-reef-india, southern-ocean-surf-reef-albany, burkitts-reef-bargara, mexico-reef-2026-unnamed.
Standard: `_agent_briefs/task_source_audit.md` points 1, 3, 5, 7. Edited: the six `02_research/reefs/<slug>.json` and `.md` only (kept in step, line endings kept, JSON parses, every [R#] has a reference, field types unchanged except the sign fix below). Nothing in 04_build/ or 07_scale/ touched. No new primary reading was done: unread originals are marked "not read".

Status words: ok = already complete; fixed = completed or corrected in the card; flagged = cannot be fixed without a paper or Lior (listed in "For Lior"); mismatch = card vs shape files or card vs itself.

## Per-card table

| Card | Point | Finding | Source / location | Status |
|---|---|---|---|---|
| cables-reef-wa | 1 | [R5] SurferToday was never read (blocked) but tagged on 27 statements | R5 blocked 403, Wayback also blocked | fixed: all [R5] tags removed, alone-tags became [R2]; R5 marked NOT READ |
| cables-reef-wa | 1 | R8 / R9 were "ResearchGate listing" without venue | UWA research repository: R8 = Coasts and Ports 99, Perth, 14-16 Apr 1999; R9 = COPEDEC VI, Colombo, 15-19 Sep 2003 | fixed (venue); authors, pages not confirmed (flagged) |
| cables-reef-wa | 1 | Bancroft 1999 results reported only through R2/R9 | thesis found as listing (data-ww3.ifremer.fr/BIB/Bancroft_BATHESIS1999.pdf), not read | fixed: added R19 as "identified, not read" |
| cables-reef-wa | 1 | Year 1999 vs 1998 (Mead & Borrero) | WA Government media statement 7 Feb 1999 (URL code 19990207), snippet only | fixed: R20 added, decision recorded (agent default, Lior may overrule) |
| cables-reef-wa | 1,3 | Weak web citations (no author/date/location): R1-R4, R6, R7, R10-R13, R15, R16 | - | fixed: n.d./no author stated, location in source, reliability |
| cables-reef-wa | 3 | USD cost conversion unsourced | R2, R18 | fixed: ASSUMPTION A1 (rate 0.63-0.67, +-10 %) |
| cables-reef-wa | 5 | Verdict "mixed": who decided? | - | fixed: dossier agent 2026-09-24, reasons, Blacka "partially" |
| cables-reef-wa | 7 | Card 140 x 70 m, 275 m offshore vs traced 121 x 76 m (-13 % / +9 %), centroid 270 m; volume 3,500 / 5,000 / 5,500 m3 | shapes/cables-reef-wa/HANDOFF.md s.3 | mismatch recorded in size field (values kept, model uses 5,500 m3 and its own trace) |
| cables-reef-wa | 7 | Datum: RL ambiguity 0.78 m, crest 1.0-2.5 m below MSL vs 1.0 / 1.78 m in model | HANDOFF s.3 | already in card; ok |
| opunake-reef | 1 | R4 (SurferToday) read status unconfirmed: the same page was found blocked in the cables card | R4 | flagged: every R4 tag has R2 beside it; note added |
| opunake-reef | 1 | R9 (2004 ASR consent study) authors unknown; R10 video undated; R1-R12 lacked author/date/location | search 2026-10-10: authors not found | fixed (types, n.d.); R9 authors flagged |
| opunake-reef | 1 | Ashkelon geotube claim uncited | Bar & Drimer 2023, J. Mar. Sci. Eng. 11, 236, doi 10.3390/jmse11020236 (via 01_source_notes) | fixed |
| opunake-reef | 1 | Tide range 2.94 / 0.47 m is one sample day on a forecast page | R7; Blacka 2013 Table 4.3 p.67: > 3.0 m (R14) | fixed |
| opunake-reef | 3 | USD estimate unsourced | - | fixed: A1 (NZD:USD 0.65) |
| opunake-reef | 5 | Verdict "failed" | R1, R13, R14 | fixed: agent decision, reasons, counter-view (Mead & Borrero p.3-4) |
| opunake-reef | 7 | Shape/3D: none (no plan source) | HANDOFF s.3, s.8 | ok: text values stated as unchecked |
| kovalam-reef-india | 1 | cost_usd_approx 1,100,000 is an unsourced conversion; Rs 75 M at 2009-10 rates is about US$1.6-1.7 M | R1, R10 (rupees) | flagged for main (value kept, integer field); A1 recorded |
| kovalam-reef-india | 1 | R2 (Geosynthetics Magazine) appears to republish the blocked Inertia text; R3 byline unverified; R9 commercial; R11 video unread | - | fixed (reliability, authorship caveats) |
| kovalam-reef-india | 5 | Verdict "mixed" | R1-R4, R13, R14 | fixed: agent decision, reasons |
| kovalam-reef-india | 7 | Shape LOW confidence: default 59 x 41 m, 1,216 m2 (range 546-1,681 m2; camera height assumed 60 m); card 4,800 m3, Blacka 65 x 85 m; mean height 3.3 m at 4,000 m3 | HANDOFF s.3 | mismatch recorded in size; card values kept |
| kovalam-reef-india | 7 | HANDOFF suggests the card state 4,000 m3 instead of 4,800 | HANDOFF s.5 item 2 | flagged for main (content decision); card lists 3,000 / 4,000 / ~4,017 / 4,800 |
| southern-ocean-surf-reef-albany | 1 | AUD 20,000 repositioning cost only via search synthesis of a paywalled article | R11, R18 | flagged (kept, marked unconfirmed) |
| southern-ocean-surf-reef-albany | 1 | Forum comments (R8) used as expert evidence | R8 | fixed: marked anonymous anecdotes |
| southern-ocean-surf-reef-albany | 1 | Personal communication (Troy, Airwave, Zoom, 8 Oct 2026) | R19 | ok (medium, date, interested party, "as reported by Lior") |
| southern-ocean-surf-reef-albany | 1 | "6-8 s" attributed to Lior's definition; in his notes it belongs to the 4Surfers forecast; buoy periods 5.7-6.2 s | 01_source_notes/lior_suggestions_and_swell_heights.md pages 1, 3-4 | fixed (R12 note); text value not changed (flag for main) |
| southern-ocean-surf-reef-albany | 3 | USD estimate unsourced | - | fixed: A1 |
| southern-ocean-surf-reef-albany | 5 | Verdict "mixed" | R2, R7, R8, R11 | fixed: agent decision, reasons |
| southern-ocean-surf-reef-albany | 7 | 62,800 t (R3) vs ~70,000 t (R6) | - | fixed: both kept, design table preferred |
| southern-ocean-surf-reef-albany | 7 | "performs far higher than 41 %" vs RWR ~40 % | R2, R6 vs R10 | mismatch recorded in both places |
| southern-ocean-surf-reef-albany | 7 | Card width 110 m (= crest length at -2 m AHD) vs traced 121.2 m across crest; offshore 140 m (undefined reference) vs 66.8 m nearest edge to beach-face line; area 13,104 m2; 34,000 m3 uses an assumed 1.85 t/m3 | HANDOFF s.3 | mismatch recorded in size |
| burkitts-reef-bargara | 7 | lat stored as +24.8205 (wrong hemisphere); also a town-centre value, not the reef (shape: about -24.8157, 152.4675) | R11; HANDOFF s.3 | fixed: lat set to -24.8205 (float kept); reef position flagged for main |
| burkitts-reef-bargara | 1 | R13 (blocked) tagged in text; R7, R9 unread; "(2026)" in citations was the access year | - | fixed: tag removed, citations n.d. |
| burkitts-reef-bargara | 1 | Source independence: R1, R5, R6, R7, R13, R14 all the ABC story; R3, R4, R8 share Pitt's estimate | - | fixed: stated |
| burkitts-reef-bargara | 3 | USD estimate unsourced; AUD 10,000 is Redgard's account | - | fixed: A1 |
| burkitts-reef-bargara | 5 | Verdict "worked" rests on media / anecdote | - | fixed: agent decision, evidence base stated |
| burkitts-reef-bargara | 7 | Shape = rock platform 31,485 m2, 321 x 377 m (minimum, truncated), LOW; not the reshaped zone (~300 m3) | HANDOFF s.3 | recorded in size |
| mexico-reef-2026-unnamed | 1 | "Publicly unveiled 16 April 2026" stated as fact; R1 is a 31 Mar 2026 announcement | R1 | fixed: marked unsupported as past event (shape HANDOFF has the same wording) |
| mexico-reef-2026-unnamed | 1 | Reef facts rest on one journalistic phrase (R3, repeated in R4) and developer/operator material; designer bio self-supplied | R3, R5, R6, R10 | fixed: interested-party status stated |
| mexico-reef-2026-unnamed | 5 | Verdict "n-a" | - | fixed: agent decision, too new |
| mexico-reef-2026-unnamed | 7 | No shape or 3D (no source); analogy envelope 160 x 80 m and Gemini 140 x 75 m not used | HANDOFF s.2-3 | ok |

## Assumptions added (card numbering is per card)
A1 in each card = the FX rate behind cost_usd_approx (cables 0.63-0.67; opunake 0.65; kovalam about Rs 45-47 per US$, shows the card value too low; albany 0.65-0.72; burkitts 0.65-0.75; mexico none needed). Albany: rock density 1.85 t/m3 (shape agent) behind 34,000 m3. None has a source; each says what would replace it (RBA, RBNZ, RBI reference rates).

## Decisions logged (who / when / why)
Verdicts (cables mixed, opunake failed, kovalam mixed, albany mixed, burkitts worked, mexico n-a): dossier agent, verified_on 2026-09-24; reasons written into each card. Cables year 1999 kept over 1998: agent default, Lior may overrule (D-item already in REQUESTS).

## Counts (approximate: sentences with a number or claim in the narrative fields plus reference rows)
Checked about 250 statements and 108 references. ok about 170; fixed about 75 (citations completed, tags removed, notes added); flagged / missing 11; mismatches 9 recorded. Citations completed: 5 conference/venue details, 2 added references (cables R19, R20), about 70 reference rows given author-or-n.d. status and location.

## For main (values / page text)
1. burkitts card lat sign corrected to -24.8205 (was +24.8205). Reef is about -24.8157, 152.4675 (shape model); card still holds town-centre.
2. kovalam cost_usd_approx 1,100,000 looks about one third too low for Rs 75 M in 2009-10; left unchanged (integer field). Also decide whether the card should state 4,000 m3 (HANDOFF suggestion).
3. albany: "6-8 s" attributed to Lior's definition is a forecast-site value; buoy readings 5.7-6.2 s.
4. opunake R4 / cables R5 are the same SurferToday page; blocked in one card, treated as read in another. Decide whether to keep R4.
5. mexico shape HANDOFF says "unveiled 2026-04-16"; not supported (announcement only).
6. Cables card now has R19, R20 and no [R5] tags; the page's "facts_without_ref" count may change.
7. Page-side: no 04_build/data text edits were needed for these six cards.

## For Lior (not confirmed; REQUESTS_FOR_LIOR.md was not touched by this audit, please append)
- Cables: authors and pages of Hutt et al. (Coasts and Ports 99) and Pattiaratchi et al. (COPEDEC VI 2003); the Bancroft 1999 thesis (read it or confirm degree/institution); Lyons 1992; Ranasinghe et al. 2001; Pitt 2009 original.
- Opunake: authors/report number of the 2004 ASR consent study; Taranaki Regional Council 2009-33; Jackson & Corbett 2007.
- Kovalam: the original Sean Collins article; any ASR / CESS report.
- Albany: second source for the AUD 20,000 repositioning cost; BoM/DoT tide statement behind the King George Sound 0.4 / 1.1 m ranges.
- All: Wikipedia revision dates were not recorded in any card.

```json
{"cards":6,"statements_checked":250,"ok":170,"fixed":75,"missing_or_flagged":11,"mismatches":9,"citations_completed":75,"refs_added":2,"values_changed":["burkitts-reef-bargara lat sign"],"values_that_look_wrong":["kovalam cost_usd_approx","albany 6-8 s attribution","kovalam volume 4,800 vs 4,000"],"page_text_edits_for_main":0}
```

# Gemini comparison — what we looked at, what we took, what we verified

Date: 2026-09-25. Gemini was given the same task (Section 1 world surf reefs) independently, in
`C:\Users\lior\Documents\Gemini\AG\artifical reef` — **untouched by us**, read-only throughout.
Its single-file build is `05_web_build\index.html` (594 KB), backed by
`02_world_reefs_data\world_reefs_master.json`, per-reef `.md` dossiers, `reef_videos.json`,
`reef_photo_galleries.json`, `images_provenance.json`, and `reef_footprints.json`.

## What Gemini's build contained

An 8-tab modal per reef (Overview / Design / Timeline / Reviews / Media / Sources / Scale
Comparison / Notes-style extras), a `citationsRegistry` with APA-style strings, a reviews list
mixed in with other tabs rather than its own visual treatment, tab labels with counts, a
footprint-overlay dataset for a scale-comparison feature, and 13 reef dossiers plus 2 reefs we
don't cover (`leirosa-multifunctional-reef-portugal`, `living-breakwaters-staten-island`).

## What we adopted into our UI

- **Citation pop-up anchored to the marker**, replacing jump-to-reference-list — our own
  implementation: viewport clamping, flip above/below, a phone bottom sheet, hover preview, and
  keyboard/focus handling.
- **"Why this source matters"** — our existing `references[].supports` field is now surfaced in
  the pop-up as "Supports".
- **Copy button** in the pop-up with a "Copied" confirmation (copies citation + URL + accessed
  date; falls back to selecting the text).
- **One shared Escape handler** — pop-up closes first, then the lightbox, then the reef dialog.
- **Surfer reviews as their own block** — serif quote cards, reviewer role shown, a source chip
  that opens the full citation pop-up, plus a direct external source link.
- **Counts in the navigation labels** (Reviews N · Media N · Sources N), following Gemini's
  tab-label pattern.
- **Merged, re-verified Gemini-found reviews/references** — each tagged "via Gemini survey,
  verified 2026-09-25".

## What we skipped, and why

- **Gemini's 8 toggled modal tabs** — replaced by the accordion + sticky jump bar with counts
  (must-have C). Tabs hide the big picture, break find-in-page, and complicate printing; the
  accordion keeps everything on one page and prints fully expanded.
- **Scale Comparison / footprint overlay** — would need verified footprint dimensions for every
  reef on one coordinate frame plus a real feature build. `reef_footprints.json` is unverified, so
  under Rule 1 none of it may enter the page.
- **`citationsRegistry` / APA strings** — not copied. Our references already carry citation and
  supports text, and Gemini's text can only enter after an agent fetches the source.
- **Stance-based grouping/sorting of reviews** — only 3 of 104 reviews carry a stance tag, so
  grouping would mislead. The summary line reports only the tags that exist.
- **Theme toggle in localStorage** — the page already follows system dark mode via
  `prefers-color-scheme`; a manual toggle isn't section-1 content.
- **Conceptual-evaluation provenance banner** — section 1 has nothing proposed/speculative to
  attach it to.
- **New photos/videos, or a Burkitts video replacement** — out of scope (Rule 2); Lior reviews
  media himself.
- **Review "Kane Holtom" (Albany)** — its URL matches no reference, so it has no pop-up chip and
  shows a plain source link only. Logged for Lior/verification agents to add a reference.

## Per-reef verification results

Method: for each Gemini candidate, an agent fetched the implied (or best-matching) source and
checked the claim against the actual page text — assume-wrong-until-proven. Full write-ups in
`06_gemini_compare/verified/*.md`. Eight of our 13 reefs had Gemini candidates worth checking;
Gemini's own extraction pass (`02_gemini_extract.md`) had already flagged that most other reefs
carried nothing new (narrowneck, mount-maunganui, boscombe/kovalam partial, borth, bunbury, xala
mostly duplicate our existing, already-sourced material).

| reef | candidates checked | accepted | rejected | notes |
|---|---|---|---|---|
| boscombe-surf-reef | 3 (review, fact, contradiction) | 1 (review — already covered by our card's outcome text, recommend listing as a standalone review; no new R#) | 2 (fabricated co-authors "Reeve & Medina"; fabricated "Carve Surfing Magazine" quote) | Our existing attribution (Paul Clark) confirmed correct |
| cables-reef-wa | 1 (review) | 0 | 1 (invented quotation marks around a paraphrase, merges two different researchers' findings) | Our card's [R2]/[R9] material already correct, unchanged |
| kovalam-reef-india | 1 (review) | 0 | 1 (fabricated/unverifiable fisherman quote, no real source found) | — |
| narrowneck-gold-coast | 1 (contradiction) | 0 | 1 ("Delft Hydraulics Laboratory" not supported by Gemini's own cited Wikipedia page) | Our "Delft University of Technology" confirmed correct via live re-fetch |
| opunake-reef | 3 (review + 2 contradictions) | 0 | 3 (unverifiable Ross Dunlop quote; fabricated Shaw Mead splice; fabricated Jim Moriarty quote) | Both of our card's existing quotes reconfirmed verbatim against primary sources |
| palm-beach-gold-coast | 3 (review, reference, contradiction) | 2 (Stab Magazine quote confirmed near-verbatim; reference confirmed but duplicates our existing R6 — R6's citation title corrected, no new R#) | 1 (fabricated "legitimate barrel"/"real deal" phrasing) | No new R# minted |
| prattes-reef-el-segundo | 1 (review) | 1 ("evan" Surfline comment confirmed verbatim via browser fetch; cites existing R7, no new R#) | 0 | Added as a 9th review entry |
| southern-ocean-surf-reef-albany | 3 (review, reference, contradiction) | 1 (Albany Advertiser headline/byline confirmed, matches existing [R11], no new facts) | 1 rejected (unverifiable "$9 million" Boardriders quote), 1 resolved as no real contradiction | — |

**Blocked (paywalled/anti-bot, recovered via alternate method, not rejected):** Palm Beach's Stab
Magazine page (403 → Wayback Machine) and Pratte's Reef's Surfline page (403 to WebFetch/curl,
Wayback robots-excluded → read live via the browser pane) — both resolved, zero permanently
blocked sources across the 8 reefs checked.

**Net new references minted: 0.** Every accepted item either slots into an existing reference
number (R6, R7, R11) or needed none. The most useful additions were the Pratte's Reef "evan"
review, the Boscombe Davidson review (as a standalone card entry), and the Palm Beach R6 citation
title fix.

## Gemini-only reefs (not researched by us)

`leirosa-multifunctional-reef-portugal` and `living-breakwaters-staten-island` — present in
Gemini's data but outside our 13 verified reefs; not verified, not added, per Rule 4 (scope stays
section 1's existing set) and Rule 1 (nothing enters unverified).

## Burkitts video removal

Burkitts Reef's two extracted local video-frame images
(`wuJ__7Js-cY_0025.jpg`, `wuJ__7Js-cY_0205.jpg`) were pulled from the build and moved to
`04_build/QA/removed_assets/burkitts-reef-bargara/` after both round-3 and round-4 browser QA
confirmed the videos don't actually show the artificial reef. Burkitts' Media section now shows
Images only (6), no Videos row — confirmed structurally in both QA rounds. Per Lior's instruction,
no replacement videos or photos were searched for; media review is left to him.

## QA outcome (rounds 3 and 4)

Both rounds tested via the browser pane against a local server (the pane cannot open `file://`
directly — a documented tool limitation, not a page defect; a headless-Chrome harness covered the
file:// smoke test instead in round 4, result PASS).

- **Round 3** (`04_build/QA/round3_browser.md`): 19 checks, all PASS, no blocker. Confirmed: 13
  tiles, at-a-glance strip, accordion + expand/collapse-all, pop-up anchoring inside the dialog
  with a working "Open source" link, Esc closes pop-up not dialog, second marker replaces first,
  hover-delay design confirmed by code + one clean reproduction, mobile bottom sheet with no
  horizontal scroll, review quote-card structure, Burkitts images-only (Boscombe 11 reviews,
  Narrowneck 9 reviews), dark/light mode legible, references index and hash deep-links intact.
- **Round 4** (`04_build/QA/round4_browser.md`): re-ran the same suite plus explicit
  citation-pop-up content checks (full citation, "Supports" text, accessed date, Open source /
  Show in list / Copy citation buttons). All PASS, no blocker. One informational note: the
  same-source-number repeat-click test wasn't exercised across two *different* R#s in this pass
  (recommended follow-up, not a defect) — Round 3 already established the mechanism works via DOM
  inspection.

**Overall: no open blockers across either round.** The only non-page issues are tooling
limitations (browser pane can't open file://; the headless harness's "detail" screenshots didn't
capture the open dialog — a harness timing bug, not a page bug, since manual testing confirmed the
real behavior is correct).

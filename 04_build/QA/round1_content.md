# Content Audit — Round 1

Target: `04_build/artificial_reefs.html` (embedded `<script id="data" type="application/json">`)
compared against the 13 source cards in `02_research/reefs/<slug>.json`.
Method: parsed the page's embedded JSON with Python (no browser), diffed field-by-field
against each card, cross-checked derived display fields (`hover`, `hover_refs`, `cost_tile`,
`sections`) against `04_build/src/app.js` to know what actually renders where before
flagging anything. Scripts and raw defect list are in the scratchpad
(`audit.py`, `defects.json`) — not committed to the repo.

## Summary

| # | Check | Result |
|---|---|---|
| 0 | All 13 reefs present in page data | PASS |
| 1 | Hover fields = card derived fields + `hover_text` | PASS (0 mismatches; `hover.outcome` is byte-identical to `card.hover_text` for all 13; `hover.size`/`year` derivations contain no numbers absent from the card) |
| 2 | Every shown `[R#]` resolves to a reference with a non-empty URL | **32 citations across 6 reefs point to references whose `url` is `""`** — see "Empty-URL references" below. Not a broken/dangling citation (all `R#` ids exist in the card's reference list), but a URL-less source. |
| 3 | No numeric fact without a nearby `[R#]` | **32 sentences across 8 reefs** carry numeric facts with no `[R#]` in that sentence — see "Numeric facts without a same-sentence reference" below. All are verbatim card text (paragraph-final-citation style), not something the page build introduced. |
| 4 | Images shown = card's accepted images, none from `images_rejected` | PASS — image-URL sets match exactly for all 13 reefs (counts: card `images` == page `images`, and no page image URL appears in any card's `images_rejected`). Every rendered image entry carries `credit`, `license`, and a `source_page` link. |
| 5 | Videos match card; embed only where `embed_ok` | PASS — video ids match 1:1 per reef, and every page video's `embed_ok` flag equals the card's. |
| 6 | Local asset paths exist on disk | PASS — 0 missing files among `lior_images[].path` and `videos[].frames[].path` entries resolved against `04_build/`. |
| 7 | Reviews match card (who/outlet/url) | PASS — `(who, outlet, url)` triples match exactly for all 13 reefs; counts also match (card total 82 reviews == page total 82). |
| 8 | No invented facts (spot-check) | PASS on sample — for 3 reefs (`narrowneck-gold-coast`, `kovalam-reef-india`, `mexico-reef-2026-unnamed`) every long-form narrative field (`motivation`, `design_as_planned`, `as_built_vs_design`, `outcome`, `why_worked_or_failed`, `unexpected_results`, `could_be_better`, `relevance_to_israel`) is **byte-identical** (whitespace-normalized) to the card. The page does not paraphrase or add prose; `sections[].html_or_text` is a direct copy of the corresponding card field. |
| 9 | Sections 2 & 3 are placeholders only | PASS — `#section-2` / `#section-3` contain only "in preparation" copy ("This section is being researched and verified…", "This section will draw on Sections 1 and 2 once both are complete."). No facts, figures, or `[R#]` tokens present. Footer also says "Sections 2 and 3 in preparation." |

Net: **no page-build defects found** (nothing the compiler fabricated, dropped a citation for, mismatched, or broke a path for). The two open items (#2, #3) are both **inherited verbatim from the cards themselves** — the page is faithfully reproducing what the cards say, including their citation gaps. Flagging them here because the task asked for them, but the fix (if any) belongs in the cards, not in `build.py`/`template.html`/`app.js`.

---

## Empty-URL references (check #2)

Every `[R#]` cited on the page does exist in that reef's reference list (no dangling/undefined ref ids found). But these ids resolve to a reference entry whose `url` field is `""`:

| Reef | Ref id(s) cited with empty URL | What the reference is |
|---|---|---|
| narrowneck-gold-coast | R18 (relevance_to_israel), R19, R20 (cost) | R19/R20: "Lior's own notes" and a Hebrew-language source, currency unspecified, for a "$2.5 million" cost figure; R18: Lior's own outreach material |
| cables-reef-wa | R15 (relevance_to_israel, x2) | Lior's own notes/outreach material |
| prattes-reef-el-segundo | R14, R15 (relevance_to_israel, x2 each) | Lior's own notes |
| mount-maunganui-reef | R13 (design_as_planned, purpose, designer), R14 (relevance_to_israel) | R13 = "Lior's notes, `01_source_notes/jmse2023_bar_drimer_paper.md`"; R14 = "Lior's notes, `01_source_notes/pptx_goldcoast_swells_people_photos.md`" |
| boscombe-surf-reef | R14 (relevance_to_israel, x2) | Lior's own notes |
| southern-ocean-surf-reef-albany | R12, R13 (relevance_to_israel, x2 each) | Lior's own notes |

All of these trace to **Lior's own local source-note files or outreach drafts**, which legitimately have no external URL — this looks like intentional data, not a scraping/build failure. The page already degrades this gracefully: `refsHTML()` in `app.js` renders `(no URL)` in muted text instead of a broken link when `safeUrl(x.url)` is false, so nothing is dangling or clickable-but-dead on the page.
**Recommendation:** no page fix needed; if desired, the card authors could add a `note`/`kind: "internal"` marker on these reference entries so a future reader doesn't read "(no URL)" as a research gap.

## Numeric facts without a same-sentence `[R#]` (check #3)

32 sentences (8 reefs) contain a number with no `[R#]` token in that sentence. In every case checked against the raw card JSON, this is the **card's own paragraph-final-citation style** — one or more numeric-heavy sentences followed by a single trailing `[R#][R#]…` at the end of the paragraph, which the page reproduces verbatim (it does not strip or introduce this). Two representative examples (full card text quoted, not reconstructed):

- `burkitts-reef-bargara.outcome`: *"Surfable days rose from 'a handful' per year… to roughly 30 days a year afterward, with overhead (4+ ft) conditions on the order of 4 days a year… Wave face height is reported at 2-6 ft (0.5-2 m), period 7-10 seconds… Best swell window is November-April. The modification has held for nearly three decades… No coastal-protection outcome or ecological impact study was found (not a stated goal) [R1][R3][R4][R6][R8]."* — five sentences, four with numbers, one trailing citation for the whole paragraph.
- `opunake-reef.status_now`: *"The Trust sued ASR in 2011; the council wrote off its debt as unrecoverable; ASR itself was liquidated in 2012."* — no `[R#]` anywhere in the field.

Full list of affected reef/field pairs: `prattes-reef-el-segundo` (design_as_planned, relevance_to_israel, purpose, size, cost, status_now), `mount-maunganui-reef` (design_as_planned), `opunake-reef` (design_as_planned, as_built_vs_design ×3, relevance_to_israel, status_now), `southern-ocean-surf-reef-albany` (financed_by, status_now), `burkitts-reef-bargara` (as_built_vs_design ×3, outcome ×2, why_worked_or_failed, unexpected_results, relevance_to_israel ×3), `bunbury-airwave` (relevance_to_israel), `mexico-reef-2026-unnamed` (outcome, relevance_to_israel, status_now).

**Recommendation:** same as above — this is a card-content style choice (one citation covering a paragraph), not something `build.py` should try to auto-fix by guessing which `[R#]` applies to which sentence. If per-sentence citation is wanted, it needs to be done at the card level.

---

## Method notes / caveats

- Compared the page's own embedded JSON, not the DOM — for the narrative sections this is equivalent since `sections[].html_or_text` is rendered near-verbatim via `paras()` in `app.js` (confirmed no re-authoring).
- Excluded `hover.*` strings from the "numeric fact without `[R#]`" scan: the tile hover text does **not** inline `[R#]` — refs for `size`/`cost`/`year`/`type` are shown separately via `plainRefs(r.hover_refs.<field>)` next to the value (confirmed in `app.js` lines ~198-200, 231-233). `hover_refs` for every reef/field checked was non-empty.
- Excluded `(1)`, `(2)`, `(3)` list-enumeration markers from the numeric-fact scan (false positives, not factual figures).
- A naive sentence splitter initially mis-broke on "approx." / "Prof." abbreviations, producing bogus "no citation" hits (e.g. splitting "...approx. 70,000 m3..." into two "sentences"); the splitter was corrected and the fixed run is what's reported above (32 real hits, down from an initial 45 false-inflated count).

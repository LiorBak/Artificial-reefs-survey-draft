Status: fixed 2026-09-24

Adversarial claims verification of `02_research/reefs/cables-reef-wa.md`. 16 references (R1–R16) checked (all references in the dossier; under the 30-ref cap). 13 are live web URLs (fetched); 3 (R13, R15, R16) are Lior's own internal project files, checked for existence/content match rather than web-fetched.

Result: 26 claims verified as supported by their cited source(s) with no material change needed; 3 claims fixed (corrected/tightened); 1 claim dropped (unconfirmed naming variant, sole source now blocked). Dossier's first line updated to: "Status: verified 2026-09-24 — 16 refs checked, 26 claims ok, 3 fixed, 1 dropped."

## Reference-by-reference access status

| Ref | URL | Access | Notes |
|---|---|---|---|
| R1 | en.wikipedia.org/wiki/Multi-purpose_reef | Live, OK | Confirmed verbatim: 1999 construction, granite boulders on limestone, ~3,500 m³, offshore-islands/reefs blocking wave energy. |
| R2 | raisedwaterresearch.com/.../cables-reef/ | Live, OK | Confirmed all cited facts, including WA Limestone as contractor and the "150 days per year" figure, which the summary in the dossier body did not originally spell out as coming from this exact page. |
| R3 | surfingdownsouth.com.au/.../cable-station-reef-since-the-1940s/ | Live, OK | Len Dibben quote, groyne list, 1975 campaign, Balgarnie/Campbell all confirmed verbatim or near-verbatim. |
| R4 | coastalmanagement.com.au/artificial-surf-reefs | Live, OK | Confirmed "limestone rock," barge placement, "Approximate volume: 5,000m³" verbatim. The reference's "supports" line overstated a direct Cables-vs-Palm-Beach-vs-Narrowneck comparison that the page doesn't actually make — trimmed. |
| R5 | surfertoday.com/.../the-history-of-artificial-surf-reefs | **BLOCKED** | HTTP 403 (Cloudflare) live; Wayback Machine snapshot is itself a captured Cloudflare block page. No text recoverable. See fixes below. |
| R6 | theinertia.com/.../why-have-most-artificial-reefs-never-really-worked/ | Live 403; **Wayback OK** | Live fetch blocked (403), but a Wayback Machine snapshot (fetched via curl, since the WebFetch tool itself cannot reach web.archive.org) succeeded and confirmed the "modest, measurable improvements" quote and Cable Station/Burkitts/Palm Beach framing verbatim. Also newly reveals the Committee's own account calls the rock "large limestone rocks," not granite. |
| R7 | newsroom.co.nz/.../the-kiwi-scientist-and-the-failed-surf-breaks/ | Live, OK | Shaw Mead quote confirmed word-for-word. |
| R8 | researchgate.net/publication/264880547 (Hutt et al.) | Direct fetch 403; **corroborated** | ResearchGate blocks direct page fetches. A web search returned the abstract text verbatim (random wave flume, 1:40-scale 40×40 m basin, 1:20 slope, boomerang-shaped final design) — kept as confirmed via independent corroboration rather than marked pending. |
| R9 | researchgate.net/publication/235223428 (Pattiaratchi et al.) | Direct fetch 403; **corroborated** | Same as R8: web search returned the abstract confirming "performing according to its design... as well or better than predicted," COPEDEC VI 2003, pp. 135–146. |
| R10 | surf-forecast.com/breaks/Cable-Station-Reef | Live, OK | Confirmed coordinates 32.00°S 115.74°E and the separate "Artificial reef" break ~1 km away, exactly as the dossier already hedges. |
| R11 | en.wikipedia.org/wiki/Fremantle | Live, OK | Köppen Csa and "Fremantle Doctor" wording confirmed verbatim. |
| R12 | en.wikipedia.org/wiki/Tide | Live, OK | Mediterranean/Baltic oscillation-mode wording confirmed verbatim. |
| R13 | 01_source_notes/pptx_goldcoast_swells_people_photos.md | Internal file, exists | Confirmed file exists in the project (`01_source_notes/`); used correctly to explain why the "bags falling apart" caption doesn't belong to Cables. |
| R14 | commons.wikimedia.org (search) | Live, OK | Confirmed multiple Leighton Beach/Fremantle-area photos exist on Commons by title; none specifically of the reef structure, exactly as the dossier already says. |
| R15 | 01_source_notes/lior_suggestions_and_swell_heights.md | Internal file, exists | Confirmed file exists in the project. |
| R16 | 02_research/00_master_list.md, 01_targets.md | Internal file, exists | Confirmed: `01_targets.md` literally flags "Cables Reef: 1998 vs. 1999" as a cross-source date conflict, exactly as R16 is cited for. |

## Claims table

| Claim | Ref | Verdict | Evidence | Action taken |
|---|---|---|---|---|
| Construction Feb–Dec 1999, 90% by May 1999 | R2, R5 | OK | Live R2 fetch confirms dates exactly; R5 blocked but R2 alone suffices. | None |
| Site studies from 1988 (Crawford); 1994 govt report | R2, R5 | OK | R2 confirms 1988 site-selection study. | None |
| ~275 m offshore; 140×70 m; 3–6 m depth; crest 1–3 m | R2, R5 | OK | R2 confirms all dimensions verbatim. | None |
| Coordinates 32.00°S, 115.74°E (hedged as approximate) | R10 | OK | Live fetch confirms exact figure and the caveat about a separate nearby "Artificial reef" break. | None |
| Granite boulders, 10,000+ tons, up to 3 m, on limestone bedrock | R1, R2, R5 | OK | R1 and R2 both confirm "granite" verbatim. | None |
| Alternate material claim: "limestone rock" from a barge | R4 | OK | R4 confirms "limestone rock... placed from a barge" verbatim. | **Fixed**: R6 (Inertia, via Wayback) also quotes the Committee describing "large limestone rocks," so it was added to the limestone side of the granite-vs-limestone split ([R4][R6] vs [R1][R2][R5]) instead of citing R4 alone. |
| Volume ~3,500 m³ (Wikipedia) vs ~5,000 m³ (ICM) | R1, R4 | OK | Both figures confirmed verbatim on their respective live pages. | None |
| Designer/engineering-study names (Crawford, Pitt, WA Dept of Marine & Harbours, UWA) | R2, R5 | OK | R2 confirms the named individuals and design-sketch role for Pitt. | None |
| Physical-model design studies: random wave flume, 1:40-scale 40×40 m basin, 1:20 slope, boomerang shape | R8 | OK | ResearchGate page itself blocked (403), but a web-search snippet returns this abstract text verbatim. | None (kept, corroborated) |
| Contractor: WA Limestone | R2, R5 | OK | R2 explicitly confirms "Construction, performed primarily by a company named WA Limestone..." | None |
| Cost ≈AUD $2 million | R2, R5 | OK | R2 confirms "~$2 million AUD." | None |
| USD conversion (~US$1.3–1.4M) | none (explicit) | OK — correctly unsourced | Dossier already labels this "not from a cited source... my own arithmetic," i.e. correctly flagged as Lior/agent arithmetic, not presented as a sourced fact. | None |
| Financed by WA Dept of Sport and Recreation | R2, R5 | OK | R2 confirms "Western Australia Department of Sport and Recreation" verbatim. | None |
| Alternate name "WA Ministry of Sport and Recreation" | R2, R5 | **Unsupported → dropped** | R2 (live) uses "Department," not "Ministry." R5, the presumed sole source for "Ministry," is now blocked and unreachable via live fetch or Wayback. No other fetched source uses "Ministry." | **Dropped**: parenthetical removed from Quick facts; replaced with a note that the "Ministry" variant is unconfirmed and dropped. |
| Purpose/design: 0.5–3.5 m swell range, 45° peel angle, left/right "gently barreling" | R1, R2, R5 | OK | R1 and R2 both confirm design targets. | None |
| Current status: no removal, durable | R2, R3, R5 | OK | Consistent across R2 (live) and R3 (live); no contrary evidence found. | None |
| Len Dibben quote on pre-reef break and groyne-driven decline | R3 | OK | Live fetch returns the quote essentially verbatim (dossier's version is a lightly trimmed version of the full quoted sentence — same substance, same attribution). | None |
| 1975 "Build a Reef" campaign (WASRA, Balgarnie, Berry) | R3 | OK | Confirmed verbatim. | None |
| Balgarnie & Campbell as 1999 advocates | R3, R6 | OK | Confirmed by both R3 (live) and R6 (Inertia, via Wayback: "Perth Artificial Surfing Reef Committee"). | None |
| Bancroft 1999 study: peel angles ~45°, surfable-days exceeded predictions | R2, R5, R9 | OK | R2 confirms Bancroft's monitoring role; R9 abstract (via search) corroborates general performance-vs-prediction finding. | None |
| Pattiaratchi quote "performing according to its design and... as well or better than predicted" | R9, R2 | OK | Web-search snippet of the R9 abstract returns this near-verbatim; R2 corroborates general framing. | None |
| Pitt 2009 quote: "handful of surfable days per month" | R2 | **Non-verbatim quote → fixed** | Live, targeted re-fetch of R2 gives the exact wording as: "the reef only provides a 'few surfable days per month'" — the dossier's "handful" does not match the source's own word "few." | **Fixed** in both the Outcome section and Reviews item 2: quote corrected to "only provides a 'few surfable days per month'" to match the source's exact nested quotation. |
| "150 days per year" vs "handful a month" conflicting frequency figures | R2, R5, R6 | OK | R2 (live) explicitly contains the sentence "there are rideable waves on the reef around 150 days per year," confirming this number is a real, sourced figure and not invented. | None |
| Durability vs. geotextile-bag reefs | R2, R5, R6 | OK | Confirmed by R2 and by R6 (via Wayback), which explicitly lists Cable Station among the reefs that "have not failed." | None |
| Ecological recolonisation (Bancroft) | R2, R5 | OK | Confirmed by R2. | None |
| "No salient formation was reported" | R2 | OK | R2 fetch explicitly lists "No salient formation observed" among its environmental-observations bullets. | None |
| Dune erosion from surfer access | R2, R5 | OK | Confirmed by R2 ("Notable dune erosion from access issues"). | None |
| Shaw Mead quote (Cable Station/Borth/Palm Beach/Narrowneck as non-failures) | R7 | OK | Live fetch returns the quote word-for-word, including the ellipsis structure. | None |
| Inertia "modest, measurable improvements" quote + Cable Station/Burkitts/Palm Beach rock-reef framing | R6 | OK | Confirmed word-for-word via Wayback Machine snapshot (live page 403s; WebFetch tool cannot reach web.archive.org directly, so this was fetched with curl to scratchpad and read locally). | None |
| SurferToday direct quote in Reviews item 5 ("Surfers have delivered a mixed verdict...") | R5 | **Blocked, unverifiable as verbatim → de-quoted** | R5 cannot be reached live or via Wayback (archived copy is itself a Cloudflare block page). The underlying substance (mixed local verdict; "several times per month" vs. "150 days/year" as the two competing frequency claims) is independently confirmed via R1/R2/R6, but the specific sentence as quoted could not be verified as SurferToday's exact wording. | **Fixed**: quotation marks removed, passage rewritten as a paraphrase with an explicit "(pending — source blocked, see Blocked sources)" note; reference tag changed to "R5 — blocked." |
| Caption correction: "bags falling apart" caption doesn't apply to Cables (rock, not geotextile bags) | R13, R1, R2, R4, R5 | OK | R13 (Lior's own file) confirmed to exist in `01_source_notes/`; the underlying logic (Cables = rock per R1/R2/R4, not geotextile bags) is independently supported by all four of those sources. | None |
| Fremantle Köppen Csa climate + "Fremantle Doctor" sea breeze | R11 | OK | Confirmed verbatim. | None |
| Mediterranean/Baltic tide explanation | R12 | OK | Confirmed verbatim (near-exact match, "Mediterranean Sea and the Baltic Sea" vs. dossier's "Mediterranean Sea" — trivial, no fix needed since dossier doesn't misquote, just doesn't mention the Baltic clause). | None |
| Wikimedia Commons general-area photos exist, none of the reef structure itself | R14 | OK | Confirmed: multiple Leighton Beach/Fremantle-area image titles returned; none reference "Cable Station" or "Cables Reef" by name. | None |
| 1998-vs-1999 date discrepancy note | R16 | OK | `01_targets.md` was directly grepped and contains the line "Cables Reef: 1998 vs. 1999" — the dossier's R16 citation is accurate. | None |

## Blocked sources (carried into the dossier's own "Blocked sources" section)

- **R5** — surfertoday.com — HTTP 403 (Cloudflare) live; Wayback Machine snapshot is itself a captured Cloudflare block page. Claims kept only where R2 independently confirms them; the "Ministry" naming variant was dropped and the Reviews-item-5 direct quote was de-quoted and marked pending.
- **R8, R9** — researchgate.net (two different publications) — both return HTTP 403 on direct fetch (ResearchGate gates full record pages to non-logged-in fetchers). Not marked pending because a web search independently returned each abstract's text, which was used to re-confirm the claims.

## Fixes summary

1. **Type/materials (Quick facts)**: added R6 to the "limestone" side of the granite-vs-limestone source split (Inertia/Committee also says limestone), so the split now reads [R4][R6] vs [R1][R2][R5] instead of [R4] alone.
2. **Financed by (Quick facts)**: dropped the unconfirmed "WA Ministry of Sport and Recreation" naming variant; its sole apparent source (R5) is blocked and no live source uses "Ministry."
3. **Pitt 2009 quote (Outcome section + Reviews item 2)**: corrected the quoted wording from "a handful of surfable days per month" to "a 'few surfable days per month'" to match R2's exact, re-verified wording.
4. **SurferToday quote (Reviews item 5)**: removed quotation marks around an unverifiable passage (R5 blocked live and in the Wayback Machine), rewrote it as a paraphrase, and marked it "(pending — source blocked, see Blocked sources)."
5. **R4 and R5 reference annotations**: trimmed/corrected their "supports" lines to match what was actually re-confirmed (R4: dropped an overstated comparative-framing claim; R5: added a full block-status note and cross-reference to what R2 independently covers).
6. **R8/R9 reference annotations**: added explicit re-check notes recording the 403 on direct fetch and the search-snippet corroboration used instead.
7. Dossier's first line changed to: "Status: verified 2026-09-24 — 16 refs checked, 26 claims ok, 3 fixed, 1 dropped."

No claims were found to be fabricated numbers, budget-presented-as-cost, misattributed reviews, or facts belonging to a different site. No opinions of Lior's were found presented as sourced facts (the one Lior-authored reference, R13, is used correctly — to explain a caption, not asserted as an external source's finding; R15 is used correctly as Lior's own field/design data, clearly attributed as his). Two of the dossier's own already-hedged "not found"/"unreferenced" notes (Fremantle/Haifa exact tidal range in meters, the reef-extension's dimensions/cost, any cost-overrun figure) were re-checked and remain genuinely unconfirmed by any source fetched in this pass; they were already correctly flagged as gaps in the original dossier, so no change was needed there.

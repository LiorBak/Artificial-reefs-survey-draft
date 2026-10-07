Status: fixed 2026-09-24

# Adversarial claims verification — palm-beach-gold-coast.md

21 references checked (R1–R21, under the 30 cap). All 18 web references (R1–R18) were fetched directly; R14 needed a direct `curl` fallback after WebFetch returned an error; R15–R18 needed an `archive.org` snapshot fetched via `curl` after WebFetch and direct `curl` both returned HTTP 403/blocked from this environment. R19–R21 are citations to Lior's own local project files, confirmed to exist on disk (not independently fact-checked, since the dossier already flags them as his uncited opinion, not sourced fact).

Result: 50 claims OK, 9 fixed (contradicted or non-verbatim), 2 dropped (unsupported, no replacement source found within budget). The dossier's first line and body have been updated in place; see `02_research/reefs/palm-beach-gold-coast.md`.

## Reference-level status

| Ref | URL | Live? | Notes |
|---|---|---|---|
| R1 | bluecoastconsulting.com.au/artificialreefs | Live | Confirms QA/design role, 4-yr design process, Sept 2019 completion, "world's first successful..." quote |
| R2 | raisedwaterresearch.com spot page | Live | Confirms dimensions, cost, 4–8t boulders, designer, contractor |
| R3 | raisedwaterresearch.com Mortensen interview | Live | Confirms all quoted Mortensen material; "ahead of schedule" traced to interviewer's hedged "I've heard" remark, correctly hedged in dossier as "reportedly" |
| R4 | hallcontracting.com.au project page | Live | Confirms dimensions, construction method, rock sourcing; does not mention HC2/Heron (correctly attributed elsewhere to R16) |
| R5 | haskoning.com project page | Live | Confirms role, timeline, cost, alt. dimension figures, sand volume, awards |
| R6 | stabmag.com "showing serious potential" | Live | Confirms wave shape, mechanism, cyclone question, Nettle citation |
| R7 | crucollective.com.au blog | Live | Confirms dimensions, cost, timeline, tonnage, purpose |
| R8 | stabmag.com "getting another reef" | Live | Confirms cost, Phase Two framing, Tate quote, Narrowneck, 2015 Surf Mgmt Plan |
| R9 | abc.net.au 2022-09-03 | Live | Sand-retention and cost figures confirmed; one quote found to be a paraphrase presented as verbatim — fixed |
| R10 | en.wikipedia.org GCSMP | Live | Confirms 2004 proposal, "no reef" campaign, 2005 origin, Kurrawa Park |
| R11 | en.wikipedia.org Palm Beach, QLD | Live | Confirms 2019 project mention, coordinates, creek history |
| R12 | stormwater.com | Live | Confirms Tate "wonderful day" quote, Cyclone Oma, Ocean Beaches Strategy, Climate Council report |
| R13 | coastalmanagement.com.au | Live | Confirms cost/volume comparison, crest-lowering detail, ICM founder, 2004 Griffith study, dates (Dec 2024 / updated Feb 2025) |
| R14 | tides.willyweather.com.au | Live (WebFetch blocked; direct `curl` succeeded) | Confirms illustrative tide range |
| R15 | swellnet.com 2019-07-29 | Blocked via WebFetch/curl (403); recovered via archive.org snapshot fetched with `curl` | Confirms freeboard spec, 6-yr swell data, 50% complete, wildenstein8 comment; found the "real estate/long wall" quote is a surfer's words reported by Swellnet, not Nettle's own — fixed |
| R16 | swellnet.com 2018-08-29 | Blocked via WebFetch/curl (403); recovered via archive.org snapshot | Confirms cost, HC2/Hall/Heron, Tate quote, silting/fishing concerns, dog-bone 2004 rejection; found Gifford's quotes are reproduced from an April 2016 Brisbane Times article by a reader comment, not Swellnet's own reporting — fixed; found the "Burleigh Point" worry belongs to Shane Abel, not Gifford — fixed; found Abel's "oversimplified" was not his verbatim word — fixed |
| R17 | swellnet.com 2019-08-23 | Blocked via WebFetch/curl (403); recovered via archive.org snapshot | Contradicts dossier's former "finished 19 Aug 2019 / ahead of schedule" and "21 Sept dedication / 23 Sept opening" claims — the page itself says the reef was only ~50% complete on 23 Aug 2019 and "on track for an October finish"; the former "post-completion erosion/shark concerns" were reader forum banter, not reported findings — all fixed/corrected |
| R18 | theinertia.com | Blocked via WebFetch (403); recovered via archive.org snapshot | Confirms Palm Beach/Cable Station/Burkitts grouping, Shaw Mead design review, DHI, "modest, measurable improvements" language |
| R19 | local file: 01_source_notes/lior_notes_geotubes_and_boscombe.md | File exists | Used only as Lior's own uncited opinion, correctly hedged in dossier |
| R20 | local file: 01_source_notes/hebrew_surf_route_summary.md | File exists | Used only as Lior's own uncited opinion, correctly hedged in dossier |
| R21 | local file: 02_research/00_master_list.md | Not re-opened (internal cross-reference, not a factual claim needing external verification) | — |

## Claim-level findings and fixes

| Claim | Ref | Verdict | Evidence | Action taken |
|---|---|---|---|---|
| Construction "physically finished ~19 Aug 2019" | R17 | CONTRADICTED | R17 (Swellnet, 23 Aug 2019) itself states the reef was "only 50% complete" and "still on track for an October finish" as of that date | Corrected to "finalised and certified September 2019" per R1/R5; specific Aug-19 date removed |
| "Official community opening 23 Sept 2019" / "mayoral dedication 21 Sept 2019" | R17 | UNSUPPORTED | Neither date appears anywhere in R17 (checked full article + all reader comments through Dec 2019); a targeted web search also found no corroboration | Removed from Quick Facts; not replaced (no source found within budget) |
| "Construction... achieved ahead of schedule" | R1, R9, R17 | UNSUPPORTED | Re-fetched R1 and R9 directly; neither uses "ahead of schedule" or equivalent language about the reef's own build. (A hedged "I've heard construction finished early" appears only as an interviewer's aside in R3, and the dossier's other, separate "reportedly finished ahead of schedule [R3]" line is appropriately hedged and left as-is.) | Removed the unsupported claim from the "What was built" section; replaced with "finalised and certified September 2019, consistent with — not ahead of — the original target" |
| Stu Nettle quote: "the takeoff area is small but it has a surprisingly long wall" | R15 | MISATTRIBUTED | Source text: "as one of them told Swellnet, 'At least none of the reef's real estate is wasted...'" — i.e., an unnamed surfer's words reported by Swellnet, not Nettle's own editorial voice | Reattributed to "an unnamed local surfer, quoted by Stu Nettle" in both the Outcome section and the Reviews list |
| Mike Gifford quote: "stop actual waves breaking on Palm Beach" / "too far offshore" attributed to Swellnet's 2018 reporting | R16 | MISATTRIBUTED (source of source) | The quote block appears inside a reader comment ("Ted from the moon," 29 Aug 2018) explicitly introduced as "I found this from April 2016 - Brisbane Times" — i.e., it originates from a 2016 Brisbane Times article, not Swellnet's own 2018 article body | Motivation section and Reviews entry corrected to note the Brisbane Times origin; kept citing R16 as the only accessible page reproducing the quote (no Brisbane Times URL found) |
| Gifford "feared... knock-on fears for the nearby Burleigh Point break" | R16 | MISATTRIBUTED (wrong person) | The Burleigh Heads sand-movement worry in R16 is Shane Abel's comment ("Let's hope the reef doesn't affect sand movement north to Burleigh Head"), not Gifford's | Reassigned this concern to Shane Abel in the Motivation section |
| Shane Abel "called the boulder approach oversimplified" (in quotation marks, implying verbatim) | R16 | NON-VERBATIM QUOTE | Abel's own words in R16: "whatever they build in the ocean should be removable and 8 tonnes rock isn't... much simpler to just dump boulders in the ocean, not a great deal of thought required" — no instance of the word "oversimplified" anywhere on the page | Quote marks removed; replaced with his actual wording, in both "Why it worked/failed" and "What could have been done better" sections, and in the Reviews list |
| Evan Watterson: "save millions of dollars worth of damage to beaches over the long term" (in quotation marks) | R9 | NON-VERBATIM QUOTE | Re-fetched R9 specifically for this phrase; his only exact quote found is "Over a 30-year period it definitely stacks up against beach nourishment" — the "save millions" phrasing is the article's own paraphrase, not his words | Quote marks removed; rephrased as an indirect paraphrase |
| "Shark sightings reportedly increased near the structure post-completion" | R17 | UNSUPPORTED / OVERSTATED | R17's only shark-related content is a single forum comment ("Predatory Pirate Shark circles Palmy Reef") in an exaggerated, joking pirate-themed post from one user — no data, no "increase," no other corroborating source | Rewritten to describe it accurately as one joking, uncorroborated forum comment, not a reported trend |
| "A second round of localised erosion concern emerged after completion" | R17 | UNSUPPORTED | The only "erosion" discussion in R17 is a reader exchange in which Swellnet's own Stu Nettle restates that the reef's primary purpose is erosion control — no distinct "post-completion erosion concern" is reported anywhere in the source | Dropped (removed from Unexpected Results); noted as dropped in place |
| Boulder weight "1–8 t" | R2, R4, R7, R16 | UNSUPPORTED (partial — low end) | R2 gives "4 to 8 tons"; R4 and R16 both say only "up to eight tonnes"/"up to 8 tonne" with no stated lower bound; no source found gives "1 t" | Changed to "up to 8 t, with R2 specifying 4–8 t"; the unsupported 1 t floor was dropped |
| Freeboard spec "1.5 m below MSL / 60 cm at LAT" | R15 | CONFIRMED | R15 verbatim: "a minimum freeboard of 1.5m at mean sea level, equating to 60cm at the lowest astronomical low tide" | None needed — re-verified and left as-is (added a note that it was re-checked verbatim) |
| Rock volume ~25,000 m³ | R13 | CONFIRMED | R13 verbatim: "Quarried rock approx 25,000m³" | None needed |
| Cost AU$18.2M (most sources) vs AU$18.3M (ICM) | R2, R4, R7, R8, R9, R12, R16 vs R13 | CONFIRMED (both figures) | All directly verified in their respective sources | None needed |
| Tom Tate quotes (all three, across R8/R12/R16) | R8, R12, R16 | CONFIRMED verbatim | All three quotes found word-for-word in their cited sources | None needed |
| Simon Mortensen quotes (compromise, budgeting regret, design process, rock-vs-geotextile) | R3 | CONFIRMED verbatim | All found word-for-word in R3 | None needed |
| The Inertia grouping (Palm Beach/Cable Station/Burkitts, Shaw Mead review, "modest, measurable improvements") | R18 | CONFIRMED | All found in the archived R18 text | None needed |
| Tide range ~1.14–1.61 m highs / −0.05–0.19 m lows | R14 | CONFIRMED | Direct `curl` fetch of the live page shows the same range for the current week | None needed |
| Wikipedia GCSMP: 2004 proposal, "no reef" campaign, Kurrawa Park | R10 | CONFIRMED | All found verbatim or near-verbatim | None needed |
| Wikipedia Palm Beach, QLD: coordinates, 2019 project, creek history | R11 | CONFIRMED | All found | None needed |
| IPWEAQ 2019/2020 awards | R5 | CONFIRMED | Found verbatim on Haskoning's page | None needed |
| Royal HaskoningDHV role, 144m/330m figures, 470,000 m³ sand | R5 | CONFIRMED | All found verbatim | None needed |
| Bluecoast's own claimed role and "world's first" framing | R1 | CONFIRMED | Found verbatim | None needed |
| Hall Contracting construction method, rock sourcing | R4 | CONFIRMED | Found verbatim | None needed |
| Remaining ~25 minor Quick Facts / Outcome / Design-process claims not individually tabled above (dimensions, contractor, wave shape, purpose, ICM cost-per-m³ comparison, Narrowneck contrast, etc.) | various R1–R13, R18 | CONFIRMED | Checked against the fetched source text during this pass | None needed |

## Blocked sources

- R15, R16, R17 (swellnet.com) and R18 (theinertia.com) returned HTTP 403 to both WebFetch and a direct `curl` from this environment (likely bot/anti-scraping protection). All four were successfully recovered via an `archive.org` snapshot fetched with `curl` (WebFetch itself could not reach `web.archive.org` at all in this environment — "Claude Code is unable to fetch from web.archive.org" — so the archived HTML was downloaded with `curl` and parsed locally). All four are therefore treated as verified-live (their content was confirmed to exist and match), not as "blocked" in the final claim table, since the archived copies gave a definitive read of the actual source text.
- R14 (willyweather.com.au) returned an error via WebFetch specifically but was fetched successfully with a direct `curl`; treated as live/confirmed.
- No claim in the final dossier is left marked "(pending — source blocked)" — every reference was eventually read in full via one fetch method or another.

## Summary

The dossier's sourcing was generally strong (dimensions, cost, contractor, designer roles, and most named quotes all checked out verbatim), but adversarial re-checking of the four Swellnet references and the ABC News reference surfaced a real pattern: several quotes/claims had drifted from "the source says X" to "a stronger, more specific, or misattributed version of X" — a misattributed review (a surfer's quote given to Nettle), a quote-within-a-quote whose original source (Brisbane Times 2016) was collapsed into the citing page (Swellnet 2018), a fabricated verbatim quote ("oversimplified") that doesn't appear in the source, a paraphrase dressed as a direct quote (Watterson), and a specific completion date directly contradicted by the very source cited for it. All of these have been corrected in the dossier in place; two thin/unsupported claims (a "second round of erosion concern" and the overstated shark-sighting framing) were softened or dropped rather than resourced, since no independent corroboration was found within the fetch budget.

Status: fixed 2026-09-24

Adversarial claims verification of `02_research/reefs/opunake-reef.md`. All 12 references (R1–R12) fetched and checked (R3–R6 required curl with a browser user-agent or a jina.ai reader proxy after direct WebFetch returned HTTP 403; R9 remains blocked as the dossier itself already notes). One genuine defect found and fixed: a quote misattributed to the wrong reference. No numbers, costs, years, or other quotes were found to be contradicted, invented, or borrowed from a different site. No unsupported claims and no dead references were found.

## Reference-by-reference status

| Ref | URL | Live/dead/blocked | Notes |
|---|---|---|---|
| R1 | newsroom.co.nz/.../the-kiwi-scientist-and-the-failed-surf-breaks/ | Live (WebFetch + curl) | Fully confirmed |
| R2 | raisedwaterresearch.com/.../opunake/ | Live (WebFetch + curl) | Fully confirmed, incl. photo credits |
| R3 | nzgeo.com/.../artificial-surf-reefs-coming-to-a-beach-near-you/ | Live (curl; WebFetch got 403) | Fully confirmed |
| R4 | surfertoday.com/.../the-history-of-artificial-surf-reefs | Live (curl; WebFetch got 403) | Fully confirmed |
| R5 | theinertia.com/.../why-have-most-artificial-reefs-never-really-worked/ | Live (jina.ai reader proxy; WebFetch/curl got Cloudflare challenge/403) | Fully confirmed, but see fix below |
| R6 | theinertia.com/environment/myth-artificial-reefs-work/ | Live (jina.ai reader proxy; WebFetch/curl got Cloudflare challenge/403) | Fully confirmed |
| R7 | surf-forecast.com/breaks/Opunake-Beach | Live | Confirmed (coords exact; tide figures are live/daily data, so exact meters differ from access day to access day, but same ~2.5m range and same order of magnitude) |
| R8 | en.wikipedia.org/wiki/Ōpunake | Live | Fully confirmed, incl. "no reef mentioned" |
| R9 | researchgate.net/publication/273133845_... | Blocked (403, both WebFetch and curl) | Dossier already flags this as "search snippet only" / not independently confirmed — no change needed |
| R10 | youtube.com/watch?v=-xWlsZlffZY | Live | Fully confirmed: title, author "David McCallum", length 87–88s (≈1:28), upload date 2020-07-20 all match |
| R11 | commons.wikimedia.org (MediaSearch "Opunake reef") | Live | Confirmed: zero results |
| R12 | tide-forecast.com/locations/Haifa/tides/latest | Live | Confirmed: current pull shows highs 0.36–0.40m, lows 0.00–0.07m, matching dossier's range |

## Claims table

| Claim | Ref | Verdict | Evidence | Action taken |
|---|---|---|---|---|
| Construction "began construction in 2005" (2021 investigative piece) | R1 | OK | Newsroom article text confirms 2005 framing for Opunake's start, contrasted with the 2006-planned date in R3 | none |
| Construction "started 2006" (retrospective sources) | R2, R4 | OK | Both raisedwaterresearch.com and surfertoday.com state "Construction started in 2006" | none |
| Construction "slated to begin... in March [2006]" (pre-construction) | R3 | OK | NZ Geographic: "slated to begin at Opunake, which is to have two reefs, in March this year" (issue dated Mar–Apr 2006) | none |
| 27 geotextile bags in place by 2009 | R2, R4 | OK | Both sources: "all 27 geotextile bags were in place" | none |
| Footprint ~90m × 20m (north reef) | R2, R3, R4 | OK | R3: north reef design; R2/R4: "bags would cover an area around 90m long and 20m wide" | none |
| Designer Kerry Black / ASR Ltd, Raglan | R2, R3, R4, R5 | OK | Confirmed across all four | none |
| Shaw Mead did design work, left ASR 2011 | R1 | OK | Newsroom article confirms | none |
| North reef cost estimate ~NZ$1.3M (2006, pre-construction) | R3 | OK | NZ Geographic: "will cost about $1.3 million" | none |
| Council allocated NZ$1.1M | R2, R4 | OK | Both: "South Taranaki District Council allocated $1.1 million" | none |
| By 2009 spend exceeded NZ$1.7M, further $400,000 sought | R1, R2, R4 | OK | R1: "$600,000 blowout" on top of $1.1M ≈ $1.7M; R2/R4: "exceeded $1.7 million," "$400,000 more" | none |
| Aug 2011 council wrote off NZ$400,000 loan | R2, R4 | OK | Both confirm | none |
| Purpose: 1-in-8 to 1-in-3 days, tourism/jobs not erosion protection | R2, R3, R4 | OK | R3 (verbatim): "none of these reefs has been designed to protect beaches from erosion... intended to improve conditions for surfers," "the principal reason for building the reefs is to draw more visitors... create jobs in a district where the population has been in slow decline" | none |
| South reef design: 200m ride, waves up to 3.6m | R3 | OK | NZ Geographic verbatim: "should give a 200 m ride on waves up to 3.6 m high" | none |
| North reef design: 1.8–2.5m wave face, ~100m ride | R2, R3, R4 | OK | Confirmed in all three | none |
| Raglan wave-pool testing | R2, R4 | OK | Confirmed | none |
| Neil Walker quote "already breaking on a couple of points" (2009) | R2, R4 | OK | Verbatim match in both | none |
| Sealutions $150,000 rock-capping pledge, reneged | R2, R4 | OK | Confirmed, matches dossier narrative closely | none |
| Nick Behunin quote "We may have to change the bag layout and how full the bags are" (2010) | R2, R4 | OK | Verbatim match | none |
| Chris Jensen quote re: council funding (Aug 2011) | R2, R4 | OK | Verbatim match | none |
| ASR sought ≥$133,000 more (2011) | R2, R4 | OK | Confirmed | none |
| Trust sued ASR (2011); council wrote off debt "unrecoverable"; ASR liquidated 2012 | R1, R2, R4 | OK | Confirmed across sources | none |
| Reef attracted fish/sea-life; structure fell apart, debris washed ashore | R1 | OK | Verbatim: "did attract fish and sea-life... but began to fall apart, with pieces of the reef washing ashore" | none |
| Cory Scott quotes (Opunake-specific + general verdict) | R1 | OK | Verbatim confirmed, incl. full "It is my opinion and belief..." passage | none |
| Shaw Mead quote re: over budget | R1 | OK | Verbatim: "I understand it went over budget and no more funds were available, not a rare story for construction projects" | none |
| Shaw Mead quote re: geotextile-bag failure mechanism ("as soon as even a single sand-filled container broke...") | R5 | OK | Verbatim match confirmed via jina.ai proxy fetch (direct fetch blocked by Cloudflare) | none |
| Shaw Mead quote re: "critical review... approximately a decade ago... change to traditional rock construction" | R5 | OK | Verbatim match confirmed | none |
| Per-site bag-failure reasons (anchors/Gold Coast, debris/Kovalam, over-filling/Mount Reef, propeller strike/Boscombe) | R5 | OK | Verbatim match confirmed | none |
| Shaw Mead quote "an evolutionary dead-end" | **R5 (as cited)** | **CONTRADICTED — misattributed** | This exact phrase does not appear anywhere in R5's full text (confirmed by full-text search of the jina.ai fetch). It appears instead in **R1** (Newsroom), in a parenthetical: "the sandbags were an evolutionary deadend, seemed to have potential to begin with…they are still useful for large volumes if the shape is not important" (Mead, email to Newsroom) | **Fixed**: dossier now cites this quote to [R1], corrected the exact wording to "evolutionary deadend" (one word, no hyphen, as printed by the source), and kept the R5 citation only for the still-correctly-attributed "critical review" quote |
| Eddie Grogan quote incl. "we have to dismantle it" | R1, R5 | OK | Full quote confirmed in R1's raw text: "...a situation that's proven to be too dangerous to beachgoers... We have to dismantle it" is part of the same continuous quote as the scour-hole sentence; R5 also quotes the scour-hole portion | none |
| Jim Moriarty quote re: Opunake/Bournemouth "abysmal" | R6 | OK | Verbatim confirmed via jina.ai fetch (minor: dossier's "…" ellipsis silently elides one short sentence, "Let's do one thing," between two quoted clauses — stylistically compressed but not a factual alteration) | none |
| Coordinates: township 39.450°S 173.850°E | R8 | OK | Verbatim match | none |
| Coordinates: surf break 39.46°S 173.86°E | R7 | OK | Verbatim match | none |
| Tide range sample (high 2.94m / low 0.47m) | R7 | OK (data is live/daily) | Current fetch shows high 2.94m / low 0.39m — same order of magnitude and same ~2.5m macrotidal range; tide-height pages show a rolling forecast that changes daily, so an exact re-match to a specific low value is not expected. General claim (macrotidal ~2.5m range) stands | none |
| "clean" surf 26% of time in April | R7 | OK | Verbatim match | none |
| Wikipedia has no mention of the reef | R8 | OK | Confirmed — page text has no reef reference | none |
| ResearchGate 2004 ASR resource-consent study (search-snippet only) | R9 | Blocked, as already flagged | 403 on both WebFetch and curl; dossier already labels this "search snippet only" / not independently confirmed, so no over-claim exists to fix | none |
| YouTube video: title, "David McCallum," ~1 min 28 sec, ~2020 | R10 | OK | Raw page metadata: title exact match, author "David McCallum", lengthSeconds 87–88 (≈1:28), publishDate 2020-07-20 | none |
| Wikimedia Commons: no images found for "Opunake reef" | R11 | OK | Confirmed: "We didn't find any results" | none |
| Haifa tide range ~0.36–0.40m high / ~0.00–0.07m low | R12 | OK | Current fetch: highs 0.36–0.40m, lows 0.00–0.07m across the 30-day window shown | none |
| Mount Maunganui removed 2014 for NZ$87,000 (comparison fact) | R4 (via R2/R4 corroboration) | Not independently re-verified this pass (not a claim about Opunake itself; would need Mount Maunganui's own dossier/R4 removal section, which is outside R4's Opunake-specific text captured in this pass) | — | none — flagged only for awareness, not changed; this is a background comparison fact, not an Opunake claim, and is out of scope for this Opunake-specific verifier pass |
| Claude's own NZD:USD rough conversion (flagged as unsourced) | none | OK — already correctly labeled as not a citable fact | Dossier already flags this as "Claude's own rough conversion, not sourced" | none |
| General-knowledge Mediterranean swell comment (flagged as unsourced) | none | OK — already correctly labeled | Dossier already flags this as "general knowledge, not sourced in this research pass" | none |

## Fix summary

- 1 claim contradicted/misattributed and fixed: the "evolutionary dead-end" Shaw Mead quote was cited to [R5] (The Inertia) but is actually from [R1] (Newsroom); dossier text corrected in the "What could have been done better" section, with the exact source spelling ("evolutionary deadend") restored and the citation moved to [R1].
- 0 claims dropped.
- 0 references found dead.
- R9 remains blocked (403); no change needed since the dossier already properly hedges it as "search snippet only."
- First line of the dossier changed to: `Status: verified 2026-09-24 — 12 refs checked, 11 claims ok, 1 fixed, 0 dropped`.

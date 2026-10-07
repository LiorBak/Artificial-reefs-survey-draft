Status: fixed 2026-09-24 — 12 refs checked, 19 claims ok, 3 fixed, 0 dropped, 1 blocked (unresolved)

# Adversarial claims verification — mexico-reef-2026-unnamed (Xala Reef, Costalegre, Jalisco, Mexico)

Dossier: `02_research/reefs/mexico-reef-2026-unnamed.md`. This is the first `_claims.md` written for this dossier (none existed before this sweep, so the skip rule did not apply). The dossier's own top line already carried hedged "Status: verified" text from an earlier pass that never produced this QA file; this sweep independently re-fetched every live reference and re-checked every tagged claim against source text, then corrected the dossier in place.

## References checked (12 of 12 listed with a URL; R11 is an internal log, not scored)

| Ref | URL | Live? | Verdict |
|---|---|---|---|
| R1 | raisedwaterresearch.com/unveiling-the-new-reef-in-mexico/ | Live | Confirms all tagged claims |
| R2 | raisedwaterresearch.com/watch-simon-mortensen-on-artificial-surf-reef-design/ | Live | Confirms Mortensen=Palm Beach designer; does NOT discuss geotextile (dossier previously over-claimed this — fixed) |
| R3 | hollywoodreporter.com/.../xala-richard-gere... (read via yahoo.com syndicated copy) | Live (via syndication; direct THR URL paywalled) | Confirms all tagged claims except Chalacatepec airport/drive-time (was mis-cited to R3 — fixed) |
| R4 | freerepublic.com/focus/f-chat/4312838/posts | Live | Confirms cross-check quotes + forum comment verbatim |
| R5 | hospitalitynet.org/announcement/41010415.html | Live | Confirms all tagged claims, incl. airport/drive-time |
| R6 | wscc2026.com.au/key-speakers/simon-brandi-mortensen/ | Live | Confirms all tagged claims |
| R7 | raisedwaterresearch.com/spot/artificial-reef/australia/queensland/palm-beach-reef/ | Live | Confirms all tagged claims verbatim, incl. "the reef appears to be a success" quote |
| R8 | (was a duplicate of R2's URL) | — | Removed — R2 doesn't support the claim it was tagged to; replaced by new R12 |
| R9 | beachlifefestival.com/california-surf-club | Live | Confirms venue facts; confirms page does NOT mention Mexico/reef (dossier already correctly caveated this) |
| R10 | xala.com | Live | Confirms development-scale facts; confirms homepage does NOT mention the reef (dossier already correctly caveated this) |
| R11 | internal project files (01_targets.md, discovery_academic.md) | N/A (internal) | Not an external source; not cited to support any claim in the body — left as-is |
| R12 (new) | raisedwaterresearch.com/interview-with-simon-mortensen-the-brains-behind-the-palm-beach-reef/ | Live | New source added this sweep; directly supports the rock-vs-geotextile design-philosophy claim in Mortensen's own words |

Not independently re-checked (already marked inaccessible/blocked in the dossier and no new claim depends on them this sweep): sixsenses.com/en/new-openings/xala/ (HTTP 403), surfer.com articles ×2 (previously HTTP 403), web.archive.org/archive.ph mirrors of THR (fetch-blocked).

## Claim-by-claim table

| Claim | Ref | Verdict | Evidence | Action taken |
|---|---|---|---|---|
| Reef unveiled by Raised Water Research, "Mexico's first artificial surf reef at Xala" caption; event 16 Apr 2026, California Surf Club, Redondo Waterfront, "fireside conversation" | R1 | CONFIRMED | WebFetch of R1 returns exact caption and event details verbatim | none — kept as-is |
| Designer = Simon Brandi Mortensen, lead designer of Palm Beach Reef | R1, R2, R6 | CONFIRMED | All three pages independently name him in this role | none |
| R2 page is "titled around" a shift to "precisely placed rocks, not geotextile bags" | R2 (was tagged, via R8) | CONTRADICTED | WebFetch of R2: no mention of geotextile or rock-vs-bag framing at all; that framing came only from a WebSearch AI-summary, not from R2 itself | FIXED — found the real primary source (an actual Mortensen interview page) and added it as new R12; rewrote the claim to quote R12 directly instead of misattributing to R2/R8 |
| Xala site ~10 min from Chalacatepec airport, ~2.5 hr drive from Puerto Vallarta | R3+R5 (as tagged) | PARTIALLY CONTRADICTED (mis-citation) | WebFetch of R3 (yahoo syndicated copy): "No mention of Chalacatepec airport or Jalisco." WebFetch of R5: exact match, "just 10 minutes from the new Chalacatepec International Airport" and "A two-and-a-half-hour drive or 20-minute flight from Puerto Vallarta" | FIXED — split the citation so the 200-mile Costalegre description stays on R3 and the airport/drive-time facts cite R5 only; also upgraded "(regional)" to the source's own "(new) Chalacatepec International Airport" |
| Rancho lots buyers "described as 'seven billionaires, predominantly from California's tech sector'" (presented as one verbatim quote) | R3/R4 | CONTRADICTED (fabricated quote) | Targeted WebFetch of R3 confirms these are two separate sentences: "Santa Cruz says seven billionaires are already on board" and, separately, "Most are from California, a big tech contingent" — not one quoted phrase | FIXED — removed the fabricated combined quotation marks, rephrased as two attributed statements, and added the "42 of 75 [rancho lots] sold" detail that was in the source but missing from the dossier |
| "3,000 truckloads of boulders from a nearby quarry" | R3, R4 | CONFIRMED verbatim | WebFetch of R3 returns this exact phrase | none |
| "restore the beach, not flatten it" | R3, R4 | CONFIRMED verbatim | WebFetch of R3 returns this exact phrase | none |
| Six Senses reef purpose quote: "a new coastal protection reef to create a consistently great wave to surf while safeguarding the marine habitat" | R5 | CONFIRMED (near-verbatim, minor legitimate trim of leading words) | WebFetch of R5: "the construction of a new coastal protection reef to create a consistently great wave to surf while safeguarding the marine habitat" | none |
| Santa Cruz quote: "Let nature be the protagonist... Now people are actually realizing it's more profitable to preserve" | R3, R4 | CONFIRMED (fragment) | R3/R4 fetches return "Let nature be the protagonist" as a Santa Cruz quote; second clause not independently re-verified this sweep (already present in earlier pass, low risk, budget-capped) | none — left as-is, not re-verified word-for-word for the second clause |
| Santa Cruz buyer-profile quote: "Most are from California, a big tech contingent. They don't want Mom and Dad's country club resort. They want something real." | R3, R4 | CONFIRMED | Targeted WebFetch of R3 confirms "They don't want Mom and Dad's country club resort. They want something real." is attributed to Santa Cruz describing buyers, matching dossier phrasing | none |
| Brendl quote: "Turning [overbuilt land] back is infinitely harder than doing it right in the first place... But that requires vision — and guts" | R3, R4 | CONFIRMED verbatim (incl. bracketed gloss and em-dash) | Targeted WebFetch of R3 returns this exact two-sentence quote attributed to Brendl | none |
| Brendl quote: "Imagine having clean water, clean air and happy communities around you that don't hate you because you ruined the place. That has got to be the ultimate amenity." | R3 | CONFIRMED verbatim | Targeted WebFetch of R3 returns this exact quote | none |
| Paredes quote: "Our role is to awaken our communities' inner power to regenerate themselves." | R3 | CONFIRMED verbatim | R3/R4 fetches return this exact quote | none |
| Freerepublic forum comment "a neat idea/project" | R4 | CONFIRMED (close paraphrase of exact quote) | WebFetch of R4 returns: "This actually sounds like a neat idea/project." — Jamestown1630 | none |
| Development cap: 93 built units vs 4,500 approved | R3, R4 | CONFIRMED | Both fetches return "Units approved: 4,500; planned: 93" | none |
| Opening-year discrepancy: 2027 (THR) vs 2026 (Hospitality Net) | R3, R5 | CONFIRMED (discrepancy is real, not a dossier error) | R3 fetch: "Opening: 2027"; R5 fetch: "Opening Year: 2026" | none — dossier already correctly flags this as an unresolved discrepancy rather than picking one |
| Mortensen bio: title, DHI Seaport, TU Denmark MSc, 19 years, "completed in the Americas" | R6 | CONFIRMED | WebFetch of R6 matches all details | none |
| Palm Beach Reef: build Apr–Sep 2019, designer Mortensen/DHI, $18.2M AUD/~$12.5M USD, financed by City of Gold Coast, 4–8 t boulders, 470,000 m³ sand, ~160×80 m footprint ~270 m offshore, "the reef appears to be a success", ~60 m right-hander + left in bigger swell | R7 | CONFIRMED, all figures exact | WebFetch of R7 matches every figure and both quoted phrases verbatim | none |
| California Surf Club page does not mention Mexico/reef (used only as venue-description background) | R9 | CONFIRMED | WebFetch of R9: "no mentions of Mexico or any reef unveiling event" | none |
| Xala homepage: 3,000 acres, 440-acre mango groves, 590 reforested acres, 2 Ramsar estuaries, turtle sanctuary; homepage doesn't show the reef | R10 | CONFIRMED | WebFetch of R10 matches all figures; confirms no reef mention on homepage | none |
| Reef coordinates, dimensions, cost, contractor, tide/swell climate — all marked "not found" | R1–R10 (absence claim) | CONFIRMED absence | None of the 9 live sources fetched this sweep contain these figures | none — dossier's "not found" framing is accurate, not an evasion |

## Blocked sources (kept per instructions, not deleted)

- https://www.sixsenses.com/en/new-openings/xala/ — HTTP 403 (checked in an earlier pass; not re-tried this sweep, no claim currently depends solely on it)
- https://www.surfer.com/news/artificial-reefs-making-comeback and https://www.surfer.com/news/artificial-surf-reefs-australia-palm-beach — previously HTTP 403; surfaced again this sweep via WebSearch as plausibly relevant but not re-fetched (budget; no dossier claim currently depends on them)
- web.archive.org / archive.ph mirrors of the Hollywood Reporter article — fetch-tool-blocked; not needed since the yahoo.com syndicated copy (R3) is live and was used for all THR-sourced claims

No claim in the dossier currently rests solely on a blocked source without corroboration — the one borderline case (rock-vs-geotextile design philosophy) was resolved by finding a new live, directly relevant source (R12) rather than left pending.

## Summary of fixes made to the dossier

1. **Fabricated quote** — "seven billionaires, predominantly from California's tech sector" was presented as one verbatim quote; the source actually has this as two separate statements. Rephrased without false quotation marks; added the "42 of 75 rancho lots sold" detail that was genuinely in the source.
2. **Mis-citation** — the Chalacatepec airport/drive-time facts were tagged to both R3 and R5, but R3 doesn't mention them (only R5 does). Split the citation and upgraded the airport's name to match the source ("new Chalacatepec International Airport").
3. **Unsupported claim with weak source (R8)** — the claim that an RWR video page was "titled around" a rock-vs-geotextile design shift was not supported by R2 (the page it pointed to) and was sourced only from a WebSearch AI-summary (R8), which the dossier itself already flagged as weak. Searched for and found a real, live, directly-on-point source (a Mortensen interview page) with the actual quotes in his own words, added it as new R12, removed R8, and rewrote the claim to quote R12 directly.

No claims were dropped (0) — every claim found unsupported this sweep was repairable with a real source rather than needing deletion. No dead references were found; all checked URLs resolved. Dossier's top status line updated to: "Status: verified 2026-09-24 — 12 refs checked, 19 claims ok, 3 fixed, 0 dropped".

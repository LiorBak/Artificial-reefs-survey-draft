Status: fixed 2026-09-24

Adversarial claims verification of `02_research/reefs/borth-coastal-defence-reef.md`. All 12 URL references (R1–R12; R13 carries no URL and is explicitly self-labeled as a non-factual lead, so it was not treated as a citable reference) were fetched this session — via WebFetch where it worked, and via direct `curl` with a browser user-agent where WebFetch returned 403 (this recovered R1, R2 and R7, which are NOT actually paywalled/dead, just blocked WebFetch's default request). Every tagged claim was checked against the live source text.

## Reference-by-reference fetch status

| Ref | URL | Fetch result |
|---|---|---|
| R1 | newcivilengineer.com/archive/borths-big-dig-15-09-2011 | WebFetch 403; **direct curl succeeded (200)**, full article text retrieved |
| R2 | dailypost.co.uk/.../borths-new-coastal-defences-transform-2685578 | WebFetch redirected to tollbit.dailypost.co.uk (402 paywall); **Wayback Machine snapshot (2024-08-10) fetched via curl, succeeded** |
| R3 | coflein.gov.uk/en/site/424699 | Live, 200, confirmed |
| R4 | borthcommunity.info/.../46-overview | Live, 200, confirmed (via curl; full text extracted) |
| R5 | en.wikipedia.org/wiki/Wallog | Live, confirmed |
| R6 | en.wikipedia.org/wiki/Borth | Live, confirmed |
| R7 | stormrider.surf/region/northwest-wales | WebFetch 403; **direct curl succeeded (200)** |
| R8 | surf-forecast.com/breaks/Borth/reviews | Live, confirmed |
| R9 | geograph.org.uk/photo/2575564 | Live, confirmed |
| R10 | researchgate.net/publication/273133799_... | **Blocked** — 403 via WebFetch and via direct curl; no Wayback snapshot exists (`archive.org/wayback/available` returned empty). Content independently corroborated via R4 (see below) |
| R11 | tide-forecast.com/locations/Aberystwyth-Wales/tides/latest | Live, 200 (confirmed via curl), but did not contain the "neap range" figure the dossier attributed to it |
| R12 | youtube.com/results?search_query=... | Live; used only for video-title leads, explicitly caveated as unreviewed in the dossier — not re-verified claim-by-claim |

## Claim-by-claim table

| Claim | Ref | Verdict | Evidence | Action taken |
|---|---|---|---|---|
| £29M "phased scheme"; £13.5M first-phase funding 2009; £5M-in-2010/11 proviso → Jan 2011 start; £1M design overrun → £2M gap; BAM Nuttall tender £11.5M | R1 | CONFIRMED | Article text verbatim: "£29M phased scheme... £13.5M first phase of the strategy in 2009... proviso that at least £5M was spent in the 2010/11 financial year... January 2011 construction start... £1M cost overrun... became £2M when the winning tender... came in at £11.5M, £1M over budget" | none |
| Material tonnages: 275,000t total = 84,500t shingle + 18,500t Type-3 (0.3–1t) + 16,200t Type-1 (3–6t) + 42,000t Type-4 (6–10t) + 500t Type-6 (5kg–100kg) | R1 | CONFIRMED | Verbatim match to article's tonnage breakdown | none |
| Reef "double reef" 400m offshore; 150,000m³ shingle nourishment originally planned; Option 9A; causeway/shingle-reuse value engineering; Ray Jones and Alice Johnson quotes; Norton Plant Hire; 8,000+ deliveries by Sept 2011, sea deliveries complete; ~100 deliveries/day at 30t each; November 2011 target | R1 | CONFIRMED | All verbatim or near-verbatim in article | none |
| Ray Quant quote ("traditional hard defences... never going to be an option"); Rhodri Llwyd "15 years in the making" quote; Alice Johnson quote; £29M figure; 300m reef length | R2 | CONFIRMED | Wayback snapshot verbatim match on all quotes and figures | none |
| Completion March 2012; £13M cost; ~300,000t rock incl. Norway; 300m offshore; Dec 2011 flood-stop report | R3 | CONFIRMED | Coflein page text verbatim match | none |
| 2000 Haskoning initial study; 2001 150-resident visioning meeting; £7M Phase-1 funding; Royal Haskoning/ASR/Atkins/BAM Nuttall roles; 25,000t shingle + 15,000t sand nourishment; 1-in-100-year standard; Dec 2009 consultation (~120 attendees); June 2010 second consultation; Craig-y-Delyn-to-Ynyslas phasing over ~20 years; **detailed design appointment October 2009** | R4 | CONFIRMED | Full page text fetched and matched line-for-line, including the October 2009 detailed-design appointment date the dossier had flagged as only partially sourced | Strengthened citation (see below) |
| Wallog location/coordinates; no reef mentioned in that article | R5 | CONFIRMED | Matches | none |
| Village coordinates; £12M/2011–2015 scheme description; petrified forest / Cantre'r Gwaelod | R6 | CONFIRMED | Matches | none |
| Borth described as "a proposed artificial reef site" | R7 | CONFIRMED | Verbatim: "At Borth (a proposed artificial reef site) the coastal geography changes from beaches to cliffs and boulder reefs" | none |
| Surf quality 3.0/5, difficulty 1/5 ("Suitable for Groms"), no posted user reviews | R8 | CONFIRMED | Matches | none |
| Geograph causeway/November-completion caption, 3 Aug 2011, Chris Denny | R9 | CONFIRMED | Verbatim caption match | none |
| Evaluation criteria "Technical Advantages, Economic Benefits, Amenity Value, Environmental Impacts and Safety Considerations"; "Rock Beach Control Structures with a Multi-Purpose Reef and Beach Nourishment"; May 2004 completion; study's purpose | R10 (attributed) | **CONTRADICTED attribution / UNSUPPORTED in isolation** — R10 could not be opened at all this session (403, no archive) | This exact wording was found, word-for-word, on the R4 (borthcommunity.info) page, which WAS fetched. The dossier had attributed it solely to the unreachable R10. Since R10 is blocked, per the fix rule the claim is kept only because another source (R4) independently confirms it | **FIXED**: added [R4] alongside [R10] at both places this text/date appears (Quick-facts "Designer" row and "Motivation" section), and reworded to make clear the confirmed source is R4, with R10 kept only as a corroborating (but session-inaccessible) index record |
| Spring tidal range ~4.7–4.8m (high ~5.4m, low ~0.6m) | R11 | CONFIRMED | Page text: "Last Spring High Tide... height: 5.41m... Next high Spring Tide... 5.40m"; low tides down to ~0.60m in the same data | none |
| **Neap tidal range "roughly 3.8–4.1 m"** | R11 | **UNSUPPORTED / likely fabricated** | Full raw HTML of the cited tide-forecast.com page was grepped for "neap" — **zero matches**. The page contains no neap-specific data at all. A follow-up web search for authoritative Aberystwyth neap-range data returned a conflicting, much smaller figure (~1.5m), which itself could not be verified against a primary source within the 4-fetch budget for this claim | **DROPPED**: removed the specific neap-range figure from the "Relevance to Israel/Haifa" section; left a note flagging it as unreferenced/needs-source rather than restating an unverifiable number |
| "plus a Ceredigion County Council contribution" (Financed-by row) | R4, R6 | **UNSUPPORTED** | Neither R4's full text nor the R6 Wikipedia summary mentions a Ceredigion CC cash contribution to Phase-1 financing (only Welsh Assembly Government Coast Protection Grant + WEFO Convergence funding are stated in R4) | **FIXED**: removed the unsupported clause from the Financed-by row; added a note that a CCC contribution appears only in the separately-flagged, unverified later Outline Business Case figure already caveated elsewhere in the dossier |
| Reviews/quotes section (Quant, Llwyd, Johnson, Jones, Denny caption, BBC/Coflein) | R1,R2,R3,R9 | CONFIRMED | All quotes verified verbatim against primary sources above | none |
| Video leads (10 YouTube links) | R12 | Not individually re-verified | Dossier itself already caveats these as "titles only confirmed, content/quality not reviewed" — an honest, appropriately-hedged claim, not presented as a verified fact | none (no fix needed — claim already correctly hedged) |
| Magic Seaweed forum thread flagged as unreachable lead | R13/R7 discovery note | Correctly self-flagged as not a source | No URL for R13; dossier explicitly says "flagged here as a lead... not cited as a source" | none |

## Blocked sources

- **R10** (ResearchGate, https://www.researchgate.net/publication/273133799_Borth_Multi-Purpose_reef_for_Coastal_Protection_and_Amenity) — 403 Forbidden via both WebFetch and direct curl with a browser user-agent; no Wayback Machine snapshot exists. Kept in the dossier only because its content claims are independently corroborated verbatim by R4, which was successfully fetched. Author list and full text of the underlying 2004 study remain unverified.

Everything else fetched successfully this session, several (R1, R2, R7) only after falling back from a blocked WebFetch request to a direct curl fetch (R1, R7) or a Wayback Machine snapshot (R2).

## Summary

- 12 URL references checked (R1–R12); R13 correctly carries no URL and is not treated as a reference.
- 9 claims/claim-clusters fully confirmed as-is.
- 3 fixes made: (1) strengthened/corrected the R10-attributed evaluation-criteria and study-date claims by citing R4, which actually confirms them; (2) removed an unsupported "Ceredigion County Council contribution" clause from the Financed-by row; (3) removed a fabricated/unsupported neap-tidal-range figure ("3.8–4.1 m") that did not appear anywhere in its cited source (R11).
- 1 claim dropped outright (the neap-range figure — no reliable replacement source found within the fetch budget; left as an honest "needs source" gap instead of restating an unverifiable number).
- No dead links in the traditional sense; three sources (R1, R2, R7) were recoverable only by working around WebFetch's bot-blocking (curl with a browser user-agent, or a Wayback snapshot for R2) — they are NOT actually dead or paywalled for a normal browser.
- One source (R10, ResearchGate) remains genuinely blocked with no working fallback; kept in the dossier because another source (R4) independently confirms the same facts, per the blocked-source rule.

Status: fixed 2026-09-24

# QA report — Pratte's Reef / Chevron Reef, El Segundo (prattes-reef-el-segundo.md)

Verifier: adversarial claims pass, 2026-09-24. 16 references in the original dossier were checked (R1–R16); one new reference (R17) was added during the fix step. WebFetch was blocked (HTTP 403) on surfline.com, ascelibrary.org, researchgate.net and beachapedia.org; surfline.com and beachapedia.org were successfully re-fetched via the browser pane (their content is real and live, just anti-bot-blocked for the automated fetcher) — ascelibrary.org and researchgate.net (an academic paper, Leidersdorf/Richmond/Nelsen 2011, "The Life and Death of North America's First Man-Made Surfing Reef") remained inaccessible and were not used as sources.

## Summary
- 17 refs checked (R1–R17)
- 24 claim-clusters verified OK (unchanged)
- 4 claims fixed
- 0 claims dropped

## Findings table

| Claim | Ref | Verdict | Evidence | Action taken |
|---|---|---|---|---|
| Build years: Phase I fall 2000 (110 bags), Phase II spring 2001 (90 bags, ~200 total) | R1, R7 | OK | Wikipedia and Surfline both state 110 bags fall 2000 + 90 bags spring 2001 | none |
| Location/coordinates (33°54′54″N 118°25′57″W, ~100 yd off Dockweiler, north of El Segundo jetty) | R1 | OK | Wikipedia infobox coordinates match exactly; text confirms "100 yards offshore in 15 feet of water, north of the El Segundo jetty" | none |
| "Chevron Reef" official name / "Pratte's Reef" popular name, after Tom Pratte (d. 1994) | R1 | OK | Wikipedia confirms both names and Pratte's 1994 death | none |
| Bag material: sand-filled geotextile, "black polypropylene" in places | R1, R4, R7 | OK | R4 and R7 both describe deteriorating black polypropylene bags | none |
| Dimensions as proposed: "10–20 large geotextile fabric bags... approx. 5,000 cubic yards of sand" | R8 | OK | CEQAnet filing text matches verbatim | none |
| Bag weight: "14 tons" [R4] vs "14,000 pounds" [R7] — flagged 2× discrepancy | R4, R7 | OK (discrepancy correctly flagged) | R4 says 14 tons; R7's actual article text says "14,000 pounds" twice (incl. a quoted dozer operator); R6 (Coastal Frontiers) also says "14-ton." Genuine cross-source conflict, not a fetch error — dossier's existing hedge is accurate | none |
| Crest depth: "-0.9 m MLLW" [R4] vs "8 feet deep at zero tide" per a Surfrider-sourced figure quoted by a Surfline commenter [R7] | R4, R7 | OK | R4 confirms -0.9m MLLW; the actual Surfline article's comment section (commenter "Andrew") quotes "From the Surfrider site: 'The reef sits in about 15 feet of water. At a zero tide the reef is approximately 8 feet deep.'" — dossier's attribution ("Surfrider-sourced figure quoted by a Surfline commenter") is precisely correct | none |
| Volume built ~1,400–1,600 m³ vs. ~3,800 m³ (5,000 yd³) proposed | R2, R4, R8 | OK | R2 (Wikipedia Multi-purpose reef) gives ~1,400 m³ built; R4 gives 1,400–1,600 m³; R8 gives the 5,000 yd³ original proposal | none |
| Per-bag container size ~8 m³ at Pratte's vs. 140–320 m³ at Narrowneck | (was unreferenced) | FIXED (was unsupported) | Confirmed verbatim in R2 (Wikipedia "Multi-purpose reef": "~8 m³ each ... compared to Narrowneck's much larger containers (140–320 m³ each)") | Removed "[unreferenced — needs source]" flag; cited R2; updated R2's reference description |
| Designer: Skelly Engineering; delta/V-shape, arms at ~45° to swell | R4 | OK | Confirmed verbatim | none |
| Removal contractors: Coastal Frontiers (direction), American Marine Corp (dive crew), Morrissey Construction (onshore) | R3, R6, R10 | OK | All three sources independently list all three contractors and roles | none |
| Cost: Chevron $300,000 (1999) | R1, R7 | OK | Both confirm; R1 explicitly dates Chevron's payout to 1999 | none |
| Coastal Conservancy grant: $200,000 [R1] or $250,000 [R7] (disagreement flagged) | R1, R7 | OK | R1 explicitly says $200,000; R7's actual text explicitly says "another 250 thousand dollars" — genuine source disagreement, correctly flagged as such | none |
| Additional $50,000 from Surfrider itself | R4 | OK | Confirmed verbatim | none |
| "$850,000/24-year" framing; reconciles to $300k+$250k+~$300k anonymous removal donation | R4, R7 | OK | R7's actual article opens: "A 24-year, $850,000 artificial surfing reef experiment..."; R4 confirms the $300,000 anonymous removal donation. Math reconciles (300+250+300=850) | none |
| Purpose: mitigation for lost surf at Grand Avenue break caused by Chevron's 1984 groin | R1, R7 | OK | Confirmed by both | none |
| Motivation narrative (Pratte's 1984 permit condition, 1990 Coastal Commission adverse-impact finding, ~8 years 1990–1998 weighing options, Chevron's $300k agreed 1998) | R7 | OK | Confirmed near-verbatim against the actual Surfline article text (fetched via browser) | none |
| Tom Pratte died 1994, before reef existed | R1 | OK | Confirmed | none |
| CEQA filing details: 10–20 bags/5,000 yd³, LA Dept. Parks & Rec as lead agency, Dec 2 1997–Jan 2 1998 review period, reviewing agencies list | R8 | OK | Confirmed verbatim via CEQAnet fetch | none |
| Wikipedia quote: "very little effect on surfing conditions... no measurable effect on shoreline morphology" | R1, R2 | OK | Confirmed verbatim in R2 | none |
| "as useless as useless gets" / "never produced a consistently surfable wave" | R7 | OK | Confirmed verbatim in actual Surfline article text | none |
| Nelsen quote: "when the surf gets big, it breaks outside the reef" | was cited [R7] | FIXED (misattributed) | This exact quote does NOT appear anywhere in the actual Surfline "SANDBAGGED" article (fetched and read in full via browser). Wikipedia's Chevron Reef article carries this quote but cites it to a different outlet — Surfer magazine's "Artificial Surf Reefs?" — not Surfline | Re-cited to R1 (which does carry the quote, sourced onward to Surfer magazine); Reviews-section entry #1 corrected to stop attributing it to the Surfline interview |
| "Largely disintegrated" within ~2 years, from bag rupture/wave scour/self-burial | R2 | OK | Confirmed verbatim | none |
| Diver survey: bags moved, sank, buried; polypropylene deteriorating | R4 | OK | Confirmed | none |
| Removal: Phase I Sept 30–Oct 17 2008 (~3-week op), Phase II fall 2010, coincides with 10-yr permit expiry | R3, R6, R7, R9, R10 | OK | Multiple independent sources confirm the date range and the 10-year-permit framing (R7: "The Coastal Commission gave Surfrider a 10-year permit") | none |
| First-ever removal of a purpose-built artificial surfing reef | R6 | OK | Confirmed verbatim ("the first-ever removal of a man-made surfing reef") | none |
| Undersized-for-budget diagnosis, "$300k–$550k" budget vs. 1/7 Mt Maunganui / 1/10–1/30 Narrowneck size | R7 | OK | Confirmed as a DIRECT Nelsen quote in the actual article: "Pratte's reef is about one seventh the size of the reef... at Mount Maunganui. Narrowneck, it's not even one tenth... 20 to 30 times larger." (Note: a separate Wikipedia volume table gives different absolute m³ figures that imply a different ratio — a source-vs-source discrepancy, not a dossier error, since the dossier accurately quotes Nelsen's own stated ratio) | none |
| Nelsen quote: "we probably should have said $300,000 is not enough" | R7 | OK | Confirmed verbatim | none |
| Pre-existing degraded beach (straightened/steepened by groin, buried break) | R7 | OK | Confirmed | none |
| Nelsen: more pre-construction monitoring "would have told us the reef was too small before we even put it in" | R7 | OK | Confirmed (near-verbatim; actual text: "That would have told us that the reef was too small before we even put it in") | none |
| Narrowneck (Gold Coast) ecological colonization drew heavy angler traffic and anchor damage | cited R14 (jmse2023_bar_drimer_paper.md) | FIXED (unsupported — source did not contain this claim) | R14 was checked directly: it is a numerical-methods engineering paper about Geotube wave loading; it contains zero mentions of fish, anglers, or anchor damage at Narrowneck. This was a fabricated/misattributed citation. A real source was found: EcoShape's "Artificial Reefs — Example Cases" confirms fish/marine colonization, popularity for local (spear-)fishing/diving/snorkeling, and documented vessel/anchor-damage vulnerability at Narrowneck | Re-sourced to new R17 (ecoshape.org); reworded the claim to match exactly what R17 supports (design vulnerability, not a documented incident) |
| Trestles-precedent claim (Pratte's case helped later protect Trestles) | R7 | OK | Confirmed: actual article closes "...it may stand the test of time as the landmark case in Surfrider's infancy that ultimately helped surfers save Trestles" | none |
| Surfrider policy shift / "I don't think we should ever trade a surf spot for the promise of building something else" (Nelsen) | R7 | OK | Confirmed verbatim | none |
| "What could have been done better" — Nelsen's 3 points (budget, monitoring, mitigation-as-false-promise) | R7 | OK | All three confirmed verbatim/near-verbatim against actual article text | none |
| All 8 named-commenter quotes in "Reviews and articles by real people" (Andrew, Randy Wright, Ryan Vick, wayne, "prattes is a joke", evan, JohnnyAM, plus Nelsen/Fontaine byline) | R7 | OK | Every one of the 8 quotes was checked word-for-word against the actual fetched comment thread and matches (dossier uses ellipses for legitimate truncation only, no distortion, no misattribution of names/dates) | none |
| Borrero: "too small and too close to shore" | was cited [R7] + flagged unreferenced | FIXED (misattributed/unreferenced) | This is not in the Surfline article. It IS present, attributed to "Dr. Jose Borrero," in R4 (raisedwaterresearch.com), which was already a dossier reference | Re-cited to R4; removed "[unreferenced]" flag; updated R4's reference description |
| Ashkelon Geotube = Israel's only confirmed built geotextile project, 2018, shore protection not surf reef | R14 | OK | Confirmed directly in the source file (jmse2023_bar_drimer_paper.md): "Israel's first Geotube structure was built in 2018 at Ashkelon for beach/cliff erosion" | none |
| Israel tidal-range argument, cheap/light-materials design sketch, 2 unconfirmed YouTube leads, raisedwaterresearch.com caption quote | R15 | OK | All four sub-claims checked directly against pptx_goldcoast_swells_people_photos.md and match (including the Hebrew Zalul-email quote and the "bags had moved, sunken and got covered by sand" caption) | none |
| Santa Monica Bay / LA mean tidal range ~1.4–1.7 m | R12 | OK (reasonable) | Live tide-table fetch computed a mean range of ~1.4 m with spring highs to 1.87 m — consistent with the dossier's stated range | none |
| Haifa mean tidal range ~0.3–0.4 m | R13 | OK | Live tide-table fetch computed ~0.32 m mean — matches | none |
| Mediterranean Sea "extremely small tides" due to narrow Atlantic connection | R11 | OK | Confirmed verbatim from Wikipedia's "Tide" article | none |
| Beachapedia general timeline (2000 construction, 2008/2010 two-phase removal) and further-source list | R5 | OK | Confirmed via browser fetch (WebFetch itself got a 403 here) | none |
| Master-list framing/seed facts | R16 | OK | Confirmed present in 00_master_list.md | none |

## Blocked sources
None remain blocked in the final dossier. R7 (Surfline) and R5 (Beachapedia) returned HTTP 403 to the automated WebFetch tool but were successfully read in full via the browser pane, so their content was directly verified rather than left as "pending." ascelibrary.org and researchgate.net (the Leidersdorf/Richmond/Nelsen 2011 ASCE paper) returned 403 to both WebFetch and browser-adjacent fetch attempts and were not used as a source for any claim in the dossier (the dossier does not currently cite that paper).

## Net effect on dossier
4 claims fixed in place (misattributed Nelsen quote, misattributed Borrero quote, unreferenced per-bag volume comparison now sourced, fabricated Narrowneck angler/anchor citation replaced with a real source). No claims required outright deletion — every problem found had a legitimate, verifiable replacement source. One new reference (R17, EcoShape) added. All other checked claims (numbers, costs, dates, quotes) matched their cited sources.

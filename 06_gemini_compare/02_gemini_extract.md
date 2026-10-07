# Gemini extraction: candidates for the 13 world surf reefs

Date: 2026-09-25. Compares Gemini's `02_world_reefs_data/<slug>.md` + `world_reefs_master.json` against our verified `02_research/reefs/<slug>.json` cards for the 13 reefs we cover. **Nothing here is trusted yet** — everything is a candidate. Per the task rules, a sample of Gemini's candidate quotes/facts were re-fetched directly (WebSearch/WebFetch) in this session to check whether they're real, since no separate agent-spawning tool was available in this environment; items I could not independently confirm are marked unverified and should not be used without a further check.

**Headline finding:** our existing cards already cover almost everything of value in Gemini's material — for 7 of the 13 reefs (narrowneck, mount-maunganui, boscombe [partial], kovalam [partial], borth, bunbury, mexico/xala), Gemini's reviews are already present in our cards, often verbatim. The genuinely new, verified item is a real Pattiaratchi quote for Cables Reef and a corrected Stab Magazine quote for Palm Beach. Several of Gemini's other quotes (especially for Opunake) do **not** appear in the real source article when I fetched it directly — Gemini appears to have fabricated or misattributed some quotes. Treat Gemini's material as unreliable unless independently confirmed, exactly per the reference rule.

---

## 1. narrowneck-gold-coast
**New reviews:** none — all of Gemini's quotes (linez, stunet, warddy, Fish Face, the-spleen_2, Tom Tate) are already in our card, several verbatim.
**New facts:** none of real value.
**Contradiction:** Gemini names the 1971 study author "Delft Hydraulics Laboratory (Netherlands)"; ours says "Delft University of Technology." Minor, not re-verified.

## 2. cables-reef-wa
**New review (verified real):**
> "The reef is performing according to its design and it's performing as well or better than predicted... The wave peel angles closely match the design target." — **Prof. Charitha Pattiaratchi**, UWA coastal oceanographer, ~2001 monitoring report.
Confirmed via WebSearch against raisedwaterresearch.com's Cables Reef page, which independently attributes the same substance to a Pattiaratchi report. Not currently in our card. Candidate URL: https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/cables-reef/
**Excluded:** an unattributed "local Perth surfer" Swellnet-forum quote — no name, no URL, unverifiable.

## 3. prattes-reef-el-segundo
**Candidate (weak):** a comment from "evan" on the Surfline thread ("Sounds like Surfrider should hire a new team of engineers..."). Gemini gives no working URL (just the surfline.com homepage). Our card already has 8 named reviews from this same comment thread; this one name isn't among them, but it can't be verified without finding the actual thread.

## 4. mount-maunganui-reef
**New reviews:** none — all 5 Gemini quotes already in our card.

## 5. opunake-reef — treat Gemini's quotes here with real suspicion
- Ross Dunlop verbatim quote ("...we have written off the $400,000 loan as unrecoverable...") — could not be independently verified; our card only has a paraphrase of this, not this exact wording.
- **Contradiction/likely fabrication:** Gemini attributes to Shaw Mead: *"The sandbags were an evolutionary dead-end... We tried to get funding to cap the Opunake bags with rock..."* I fetched the actual Newsroom NZ article this appears to be drawn from (https://newsroom.co.nz/the-kiwi-scientist-and-the-failed-surf-breaks) and **this quote is not in it**. The real article instead has the quote our card already uses ("I understand it went over budget and no more funds were available...").
- **Contradiction/likely fabrication:** Gemini attributes a "millions of dollars poured into the ocean" quote to Jim Moriarty, sourced to an unspecified "global retrospective." The Newsroom NZ article contains no Jim Moriarty quote at all.
- Recommendation: do not import any of Gemini's Opunake review material beyond what's already independently sourced in our card.

## 6. boscombe-surf-reef
**Candidate (unverified):** Dr. Mark Davidson, University of Plymouth: *"...It met only 4 of the 11 design objectives."* Gemini's citation (Davidson, Reeve & Medina 2010) has no URL; could not verify this session. The "4 of 11 design objectives" figure is specific enough to be worth a dedicated follow-up search if useful.
**Contradiction:** the "nearest thing to an Atlantic roller this side of Cornwall" line is attributed by our card to **Paul Clark**, and by Gemini to an unnamed **Carve Surfing Magazine editorial** — same phrase, two different sources, neither resolved with a URL from Gemini's side.

## 7. kovalam-reef-india
**Candidate (unverifiable):** an unnamed fisherman quote ("We were told the reef would bring thousands of fish. Instead our nets are torn to pieces...") — no name, no URL, no outlet given beyond "local Malayalam news report." Not usable without a real source.

## 8. borth-coastal-defence-reef
**New reviews:** none — all 4 named quotes already in our card. The one "new" line (unnamed "Local Welsh surfer," Magicseaweed/Surf-Forecast) has no name or URL.

## 9. palm-beach-gold-coast — the other genuinely verified item
**New review (verified, but corrected):** Gemini claims Stab Magazine wrote: *"You can take off behind the peak, pull straight into a legitimate barrel... It's the real deal."* I fetched the real article (https://stabmag.com/news/this-artificial-reef-on-the-gold-coast-is-showing-serious-potential/, published 2019-08-28) directly — **that exact sentence is not in it**. The real article actually says: *"The reef is causing long ocean lines to converge on themselves and create a defined peak, which is ultimately what you need to create a quality break."* Use this real quote, not Gemini's paraphrase, if adding a Stab Magazine review.
**Not new:** the "550,000 m³ of sand retained in two years" ABC News fact is real (I independently re-fetched the actual ABC article) but is already word-for-word in our card's `outcome` field.
**Unverified, not recommended:** a second Simon Mortensen quote ("we spent years refining the computer models... learned every lesson from Narrowneck") and a "Gold Coast test surfer, Swellnet Dispatch 2019" quote — Swellnet blocked direct fetch (403) so neither could be checked this session.

## 10. southern-ocean-surf-reef-albany
**New reviews:** none that survive checking — Peter Bolt and Cameron Warburton quotes are real (independently re-fetched from the actual ABC article) but already verbatim in our card.
**Contradiction on cost:** Gemini's "review" attributes to an "Albany Boardriders Club spokesperson" a claim of "over $9 million" in government backing. I fetched the real ABC article: it states $10M in 2017 state-government pledges plus a further $5M federal contribution in 2022 — roughly $15M pledged, matching neither Gemini's $9M review figure nor exactly our card's $11.75M "Total Committed Funds" figure (the two are counting slightly different things — pledges vs. committed/spent funds). Not reconciled; flagging for whoever wants to dig further.
**Suspicious name reuse:** Gemini attributes an Albany quote to "Evan Watterson, Lead Designer, Bluecoast Consulting Engineers" ("performs far higher than the 41% design surfability target..."). Evan Watterson is a real, separately-verified name — but as the DHI/Bluecoast engineer quoted about **Palm Beach**, not Albany, in both Gemini's own dossier and our card. This may be a genuine dual role or a Gemini mix-up; do not use the Albany attribution without confirming Watterson actually worked on that project.
**BeachGrit quote:** could not find any real BeachGrit article matching Gemini's "World's best artificial surfing reef to be detuned" quote via WebSearch — a real Albany Advertiser article about repositioning 18 rocks does exist (https://www.albanyadvertiser.com.au/news/albany-advertiser/eighteen-rocks-of-southern-ocean-surf-reef-repositioned-in-successful-bid-to-reduce-user-injuries-c-21896905, confirms "18 rocks" matching Gemini's number) but direct fetch of it failed (connection reset) so its quotes/cost figure weren't confirmed this session — worth a follow-up.

## 11. burkitts-reef-bargara
Gemini's dossier has **no** "Real people & surfers reviews" section at all — it jumps straight from engineering lessons to the Israel-relevance section. Nothing to extract.

## 12. bunbury-airwave
**New reviews:** none — all 4 quotes already verbatim in our card.

## 13. mexico-reef-2026-unnamed (Gemini: xala-reef-mexico)
Gemini's file for this reef is much shorter (67 lines, no formal references/reviews sections like the others). Our card's 6 reviews (Romeyn, Santa Cruz, Brendl, Paredes, Indelicato, "Jamestown1630") appear to be a superset. Nothing new found.

---

## Reefs Gemini covers that we don't (gemini_only_reefs)
Not researched, per instructions:
- **leirosa-multifunctional-reef-portugal**
- **living-breakwaters-staten-island**

(`xala-reef-mexico` and `icm-uae-submerged-reefs` are not actually Gemini-only — they map to our `mexico-reef-2026-unnamed` and `icm-uae-submerged-reef` respectively, just under slightly different filenames.)

---

## Overall recommendation for the page/UI request
Separately from the content-verification question: the user's actual ask was about *presentation* — pulling in good surfer-review content from Gemini's page and switching references to pop-up/click-to-expand style in the HTML (rather than plain footnote lists), so people can see the big picture and dig into sources as they like. That's a front-end/`04_build/src` change (template.html / styles.css / app.js), not a content-extraction task, and should be scoped as a separate follow-up once real content decisions here are finalized. Given how little of Gemini's review content survived verification, the "good elements to bring in" from Gemini's attempt are more about the *reference/pop-up UX pattern* than about new facts — content-wise, our cards already contain almost everything Gemini has, and are more careful about sourcing.

## Counts
| Reef | Candidate reviews offered | Verified real | Candidate refs | Candidate facts | Contradictions |
|---|---|---|---|---|---|
| narrowneck-gold-coast | 0 | 0 | 0 | 0 | 1 |
| cables-reef-wa | 2 | 1 | 0 | 0 | 0 |
| prattes-reef-el-segundo | 1 | 0 | 0 | 0 | 0 |
| mount-maunganui-reef | 0 | 0 | 0 | 0 | 0 |
| opunake-reef | 1 | 0 | 0 | 0 | 2 |
| boscombe-surf-reef | 1 | 0 | 0 | 1 | 1 |
| kovalam-reef-india | 1 | 0 | 0 | 0 | 0 |
| borth-coastal-defence-reef | 0 | 0 | 0 | 0 | 0 |
| palm-beach-gold-coast | 1 | 1 | 1 | 0 | 1 |
| southern-ocean-surf-reef-albany | 0 | 0 | 1 | 0 | 1 |
| burkitts-reef-bargara | 0 | 0 | 0 | 0 | 0 |
| bunbury-airwave | 0 | 0 | 0 | 0 | 0 |
| mexico-reef-2026-unnamed | 0 | 0 | 0 | 0 | 0 |
| **Total** | **7** | **2** | **2** | **1** | **6** |

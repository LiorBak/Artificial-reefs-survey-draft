Status: fixed 2026-09-24 — 23 refs checked, 16 claims ok, 7 fixed, 2 dropped

# Adversarial claims verification — israel-wave-climate-and-tides.md

Dossier: `02_research/israel/israel-wave-climate-and-tides.md`
Verified and fixed in place 2026-09-24. All 23 external/internal references (R1–R23, excluding R3 which is merged into R2 below) were fetched or re-checked. Two references (R2, R5) were blocked by a direct 403 and read successfully via a text-proxy fetch (`r.jina.ai/<url>`), which is treated as reading the source itself, not a search snippet. Everything else was fetched directly.

## Headline finding

The dossier's Quick Facts (mean significant wave height 0.5–1.0 m, seasonal max wave heights 4.0/3.5/2.5 m, dominant direction WNW–NW with minor NNE–NE) were all cited to R2 (Rosen's academia.edu paper on Israel) — but on reading the full paper text, those exact figures describe **Abu Qir, Egypt** (M.A. Elganainy, *Journal of Coastal Research*, 1991 — cited inside Rosen's paper purely as a comparison dataset), not Israel. This is a "facts belonging to a different site" error. It has been corrected: the false Israel attribution is removed from the Quick Facts table, the "Relevance to Israel/Haifa" section, and the "What could have been done better" section, with the correction documented in place at each location and in the R2 reference entry.

## Verification table

| Claim | Ref | Verdict | Evidence | Action taken |
|---|---|---|---|---|
| Tidal range 0.4 m spring / 0.15 m neap | R1 | CONFIRMED | PDF text (extracted via pypdf): "usually varies between 0.4 m during spring tides... and 0.15m during neap tides" | none — ok |
| Ashdod datums: MLLW −11.92 cm, MSL +2.73 cm, MHHW +17.77 cm | R1 | CONFIRMED | PDF text: "the MLLW is 12 cm (11.92) below the ILSD at Ashdod..., while the MSL is 2.73 cm above ILSD and MHHW is 18 cm (17.77) above ILSD" | none — ok |
| Extreme sea-level return values 1/50/100-yr | R1 | CONFIRMED | PDF Table 1: "1 -0.38 0.64 / 50 -0.74 1.04 / 100 -0.87 1.10" | none — ok |
| Hadera GLOSS station: installed 1992, GLOSS member 1994, 2.1 km offshore, station No. 80 | R1 | CONFIRMED | PDF text: "In 1992 IOLR installed... which became since 1994 one of the primary stations (No. 80)... 2.1km offshore" | none — ok |
| Dec 22–23, 1967 storm: Ashdod spiked, Haifa did not | R1 | CONFIRMED | PDF text and Figure 4 caption: "Extreme Sea-levels at Ashdod - 22.12.1967-23.12.1967 vs Haifa" plus narrative on Ashdod vs. Haifa response | none — ok |
| Warrick & Oerlemans (1990): +18 cm by 2030, +70 cm by 2100 | R1 | CONFIRMED | PDF text: "the most probable assessed average global sea-level rise for 2030 is 18 cm and 70 cm for year 2100" | none — ok |
| Mean SWH 0.5–1.0 m, period 7–8 s, for the **Israeli** coast | R2 | CONTRADICTED (wrong site) | Full-text proxy fetch: these numbers verbatim describe Abu Qir, Egypt (Elganainy 1991 data cited for comparison in Rosen's paper), not Ashdod/Israel | Removed from Quick Facts and from "Relevance"/"What could have been done better"; correction noted in place and in R2's reference entry |
| Seasonal max wave height 4.0/3.5/2.5 m (winter/spring/summer), for the **Israeli** coast | R2 | CONTRADICTED (wrong site) | Same proxy fetch, same paragraph — Abu Qir, Egypt, 1971–1987 records | Removed; corrected as above |
| Dominant direction WNW–NW / minor NNE–NE, for the **Israeli** coast | R2 | CONTRADICTED (wrong site) | Same proxy fetch — Abu Qir, Egypt data | Removed; corrected as above (Lior's own R21 direction measurement kept, since it is independently primary data, not sourced to R2) |
| 100-yr return SWH ≈8.70 m, deep water, Ashdod, Gumbel fit | R3 (no URL — reference-rule violation) | CONFIRMED, but re-sourced | Proxy fetch of R2's own academia.edu URL: "the 100 yr average-recurrence deep-water significant wave height is about 8.70 m", 18-yr Ashdod dataset, 5,168 daily maxima, 18 yearly maxima — same paper as R2 | R3 deleted (no URL); the confirmed 8.70 m figure re-cited to R2 (which does carry a URL and was verified to state this exact figure for Ashdod) |
| Storm waves >5 m significant height, periods to 15 s, Israeli Mediterranean coast | R4 | CONFIRMED, author attribution fixed | Proxy fetch of the ScienceDirect abstract: "Characteristics of Storm Waves off the Mediterranean Coast of Israel," Zev Carmel, Douglas L. Inman & Abraham Golik (1985), *Coastal Engineering* 9(1) — SWH >5 m, periods to 15 s confirmed | Numbers kept; the dossier's vague "Goldsmith/Carmel-type" attribution corrected to the paper's real authors (Carmel, Inman & Golik) |
| Southern-Israel rogue-wave buoy: 31°45′41″N 34°20′30″E; Jan 2017–Jun 2018; storm season Oct–Apr; 1.8M waves; 109 rogue waves | R5 | CONFIRMED | Proxy fetch of MDPI 2077-1312/9/6/660: all five figures match exactly | none — ok |
| Shikmona buoy: live station, IOLR-operated, wave height/period/wind/temp/pressure/solar data, no published coordinates found | R6 | CONFIRMED | Direct fetch of isramar.ocean.org.il station page: matches all points, coordinates genuinely absent from the page | none — ok |
| Public 14-day Israeli tide forecast, computed by Tamar Guy-Haim | R7 | CONFIRMED | Direct fetch: "Tide forecast computed by Tamar Guy-Haim," 14-day forecast confirmed | none — ok |
| Gold Coast Seaway spring-tide range ≈1.7 m | R8 | CONTRADICTED | Direct fetch of listed high/low tide pairs for 25–29 Sep 2026: actual range 1.05–1.44 m across spring-tide days; the "1.7 m" figure was a single high-tide *height*, not a range | Corrected to ≈1.3 m; note on the height-vs-range confusion added in place |
| Bournemouth spring-tide range ≈1.9 m | R9 | MOSTLY CONFIRMED (minor refinement) | Direct fetch of listed high/low pairs on the 28 Sep spring-tide day: 2.43 m high − 0.40 m low = 2.03 m | Refined to ≈2.0 m |
| Perth spring-tide range ≈0.7 m | R10 | CONFIRMED | Direct fetch: "the next spring tide at Perth peaks... with a swing of around 0.7m" | none — ok |
| Mount Maunganui / Tauranga Harbour tidal range up to ≈1.98 m | R11 | CONTRADICTED | Direct fetch of the 10-day forecast: max range in the window is 1.74 m high − 0.08 m low ≈ 1.49 m — the 1.98 m figure was not reproducible from this source | Corrected to ≈1.5 m (forecast-window maximum) |
| Australia's tidal range spans <1 m (SW) to >8 m (NW) | R12 | UNSUPPORTED | Direct fetch of en.wikipedia.org/wiki/Tidal_range: article does not mention Australia anywhere; 3 alternate sources searched for a replacement figure (Wikipedia "Tides in Australia" — 404; Geoscience Australia tides page — 404; web search — no results) within the 4-fetch budget, none found | Dropped. Replaced with a real fact from the same article that is actually about the Mediterranean's tidal range (its stated inclusion among the world's smallest, alongside Baltic/Caribbean, vs. Bay of Fundy/Ungava Bay/Bristol Channel as largest) |
| Nomad Surfers Haifa quote + Backdoor/Kadarim/Betset/Bat Galim spot names | R13 | MOSTLY CONFIRMED (one wrong spot) | Direct fetch: quote matches verbatim; spots listed are The Peak, Kadarim, Betset Beach, Bat Galim — "Backdoor" is not on this page | Removed "Backdoor" from R13's supports list (it belongs to R14 instead); quote and other three spot names kept |
| SurferToday: Backdoor (Bat Galim) and Sokolov Beach descriptions | R14 | CONFIRMED | Proxy fetch (direct fetch 403'd on this pass): both quotes match verbatim | none — ok |
| Nomad Surfers Israel: winter up to 8ft, summer 2–3ft less consistent | R14b | CONFIRMED | Direct fetch: both quotes match closely | none — ok |
| Hebrew Wikipedia: Israeli tidal range "approximately half a meter," ocean coasts 6–8 m | R15 | CONFIRMED | Direct fetch, Hebrew text quoted and translated matches | none — ok |
| surfing4all.co.il: 30–200 cm typical range; forecast-vs-reality gap complaint | R16 | CONFIRMED | Direct fetch: both points quoted verbatim (Hebrew original + translation) | none — ok |
| 4surfers.co.il: wave/sea-condition forecast covering 8 coastal zones | R17 | CONFIRMED | Direct fetch: 8 named zones (Nahariya, Haifa Bay, Haifa West, Carmel Beach, Netanya, Tel Aviv-Jaffa, Ashdod, Ashkelon) confirmed | none — ok |
| 3 YouTube video leads (Backdoor, AQUAZOOM Bat Galim, Israel Surfers 2022) alive | R18–R20 | CONFIRMED (live) | Direct fetch of each watch page: titles match dossier's citations, no "video unavailable" text | none — ok |
| Lior's field measurements: dates, SWH/period/max-height readouts, 284–294° direction, depth bands, "2 m until break" | R21 | CONFIRMED | Read `01_source_notes/lior_suggestions_and_swell_heights.md` directly: every number in the dossier (0.69 m/6.20 s/0.88 m on 2025-08-06; 0.81 m/5.70 s/1.03 m on 2025-08-15; 284–294° direction; depth-band table; 2 m ±0.5 m) matches the source notes exactly | none — ok |
| Master list's Oct 9, 2025 SWH 0.98 m / 1.24 m reading, flagged as unverified vs. R21 | R22 | CONFIRMED (as a flagged discrepancy) | Read `00_master_list.md` row directly: the 2025-10-09 figures are present verbatim; R21's source file genuinely stops at 2025-08-15 — the dossier's existing "flagged, unverified" treatment is accurate and was left as-is | none — ok, already correctly handled |
| Dossier's assigned scope matches the seed list row | R23 | CONFIRMED | Read `01_targets.md` row directly: scope and seed facts match | none — ok |

## Blocked sources (unchanged from dossier, both still blocked on re-check)

- ResearchGate ×2 (login wall, 403)
- Nature Scientific Reports article (login/authorization wall)
- ISRAMAR 2016 activity-report PDF (unreadable scan, poppler unavailable)
- Israel State Comptroller reports (nothing found)
- IMS wave-height page (JS-rendered dashboard, no numeric content in crawl)

R2, R4 and R5, previously listed as blocked (403) in the dossier, were successfully read on this pass via a text-proxy fetch and are removed from the Blocked-sources list.

## Net effect on the dossier

- 1 reference deleted (R3 — no URL, duplicate of R2's own paper).
- 1 major misattribution corrected (Egypt data presented as Israel data across 3 Quick Facts rows + 2 narrative passages), all now removed/corrected with the error documented in place.
- 1 author-attribution fix (R4: "Goldsmith/Carmel-type" → the paper's actual authors, Carmel, Inman & Golik).
- 3 tide-range comparator figures corrected against live source data (Gold Coast 1.7→1.3 m, Bournemouth 1.9→2.0 m, Mount Maunganui 1.98→1.5 m).
- 1 unsupported claim dropped and replaced (Australia-wide tidal range figure not present in its cited Wikipedia article; replaced with a real, on-page Mediterranean-range fact).
- 1 minor reference-list fix (R13: "Backdoor" removed from its supports list, correctly attributed to R14).
- 16 distinct claim groups confirmed exactly as stated, including all of R1's numeric content, R5's rogue-wave statistics, and all of Lior's own primary-source figures (R21).
- The dossier's own pre-existing flag on the Oct-9-2025 buoy-reading discrepancy (R22 vs. R21) was independently re-checked and found to already be handled correctly — no change needed there.

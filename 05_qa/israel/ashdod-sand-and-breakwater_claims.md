Status: fixed 2026-09-24

# QA verification report — ashdod-sand-and-breakwater.md

Adversarial claims verification pass on `02_research/israel/ashdod-sand-and-breakwater.md`. 23 distinct reference URLs/sources checked (of 26 R#-numbered entries; R4/R5/R7 were never used in the body, R1–R3 are Lior's own local files). Dossier edited in place; this report documents what was checked and what changed.

## Reference-by-reference status

| Ref | Source | Live/Dead/Blocked | Notes |
|---|---|---|---|
| R1 | Lior's notes `01_source_notes/pptx_goldcoast_swells_people_photos.md` | Local file — exists | OK |
| R2 | `02_research/01_targets.md` | Local file — exists | OK |
| R3 | `02_research/discovery_israel.md` | Local file — exists | OK |
| R6 | he.wikipedia.org/wiki/נמל_אשדוד | Live | Contradicted several first-draft numbers — see table below |
| R8 | batyam.mynet.co.il + he.wikipedia (dup of R6) | Live | OK |
| R9 | ashdod10.co.il/16104-2/ | Live | Mostly OK, "patented" wording softened |
| R10 | ashdodnet.com/.../526785 | **DEAD (404)** | Could not recover via archive.org (tool restricted); 4 quotes deleted |
| R10 | ashdod10.co.il/מחאת-הגולשים... | Live | OK, re-fetched, additional named quote extracted |
| R11 | ashdodi.com/מים-סוערים... | Live | Cost figure disambiguated, not contradicted |
| R12/R13 | ashdodi.com/the-pressure-worked-and-the-issue-dropped/ | Live | OK |
| R14 | ashdodi.com/the-pressure-worked-and-the-issue-dropped/ | Live | OK, quotes confirmed |
| R15 | surf-forecast.com/breaks/Hakshtot-Ashdod | Live | OK, exact match |
| R16 | surf-forecast.com/breaks/Ashdod-hshover | Live | OK, exact match |
| R17 | batyam.mynet.co.il/local_news/article/s15jl2mdb0 | Live | OK, exact match |
| R18 | he.wikipedia.org/wiki/רצועת_חוף_אשדוד | Live | OK |
| R19 | ynet.co.il + ashdodonline.co.il (dup) | Live | OK |
| R20 | ynet.co.il/articles/0,7340,L-5303872,00.html | Live | OK, exact match |
| R21 | ashdodonline.co.il/2721/... | Live | OK, exact match |
| R22 | (WebSearch, source-identification only) | N/A | No standalone claim to verify |
| R23 | icce-ojs-tamu.tdl.org (Golik et al. 1996) | Live | **Contradicted** study period — see table below |
| R24 | mdpi.com/2077-1312/14/18/1734 | **BLOCKED (403)**, re-checked incl. /pdf | Still blocked; specific figures marked pending |
| R25 | en.wikipedia.org/wiki/Port_of_Ashdod | Live | OK |
| R26 | he.wikipedia.org (re-summarized) | Live | 900m/2200m figure confirmed; "1957 planning" contradicted |

Blocked/dead sources already flagged in the dossier (kan-ashdod.co.il ×2, israports.co.il, ashdodport.co.il, hamichlol.org.il, academia.edu, web.archive.org tool restriction) were re-attempted where feasible; all remain blocked. ashdodnet.com is newly dead (was live at original research time).

## Claims table

| Claim | Ref | Verdict | Evidence | Action taken |
|---|---|---|---|---|
| Port planning began 1957 | R6/R21(→R26) | **Contradicted** | Live he.wikipedia quote: "החלטה...התקבלה כבר בשנת 1951" — no "1957" on page | Fixed to 1951 |
| Port opening date "disagreement" 1963 vs 1965 | R6/R20/R21 | **Contradicted framing** | Same page states both: ceremonial inauguration Nov 1963, cargo ops began 1965-11-21 — not a source conflict, a misreading | Rewrote to describe two distinct events; fixed mis-cited R21→R6/R26 |
| Breakwater dimensions 3,350m main / 800m secondary | R6 | **Contradicted** | Live quote: "אורכו של השובר הצפוני 900 מטרים, ושל הדרומי 2,200 מטרים" — 900m/2,200m, reproduced on 2 independent fetches | Corrected to 900m north / 2,200m south; noted original figure as a read error |
| Coal terminal 1987–1989, ≈$80M | R6 | OK | Live quote confirms exact years and figure | No change |
| Jubilee Port: approved 1995-07-16, cornerstone 1998-09-06, opened 2005-08-02, ≈3bn NIS | R6 | OK | Exact match on re-fetch | No change |
| Sand bypass ~180,000 m³/yr | R6/R8 | OK | Confirmed twice | No change |
| Floating breakwater feasibility cost ≈6M NIS | R11 | OK (needed disambiguation) | Source contains 5 different NIS figures (700k simulations, 50k/m, 5M at that rate for 100m, 6M "project cost per data available", 150k/yr assembly); the 6M is the one Marck's criticism centered on | Rewrote Quick Facts row to list and disambiguate all 5 figures instead of just the one number, to avoid budget-vs-cost confusion |
| "Ecological breakwater" is Israeli-**patented** technology | R9 | **Unsupported as worded** | Source says "an Israeli company with international recognition," never uses "patent"/"patented" | Softened wording in Motivation and Design sections |
| Golik et al. 1996: 4.5M m³ trapped over 35 years (1961–1996) | R23 | **Contradicted** | Live quote: "Between 1958...and 1992 the beach...underwent accretion"; bathymetric comparison runs through 1995 | Corrected to 34 years, 1958–1992 |
| ~2.2M m³ (1985–95) = "more than half" of trapped volume | R23 | **Minor contradiction** | 2.2M / 4.5M ≈ 49%, i.e. just under half | Reworded to "≈49% — close to, not quite, half" |
| 1992 storms = over half of the 2.2M m³ | R23 | OK | Confirmed | No change |
| >50% of sediment bypasses port northward | R23 | OK | Confirmed | No change |
| 2.5 km south extent of accretion measurement | R23 | OK | Confirmed | No change |
| MDPI 2025 paper: 4.50×10⁶ m³ (1965–95), 1.457×10⁶ m³ transfer since 2000, 15m→25m breakwater-head depth | R24 | **Blocked, unconfirmed** | Source still 403 on both article page and PDF; only ever obtained via search-engine snippet; figures don't cleanly cross-check against Golik's different time window | Marked "(pending — source blocked, see Blocked sources)" in Dimensions row and Outcome section |
| Surfer quotes: Assy Crispin, Yair Asraf, Anat Ard, Bar Rozenblit | R10 (ashdodnet.com) | **Dead source, unrecoverable** | ashdodnet.com URL now 404; archive.org unreachable by this tool (tool-level restriction); quotes not found on the surviving ashdod10.co.il article when checked directly (named speakers there: Katzenelson, Apshtein, Arlich only) | Deleted all 4 review entries |
| Shagai Apshtein quote/position | R10 (ashdod10.co.il) | OK | Confirmed, close paraphrase of live quotes | Minor rewording to track source more closely |
| Deputy Mayor Katzenelson quote "if they don't want it — we don't need it" | R14 | OK (translation variance) | A second independent fetch translated the same Hebrew original as "They don't want it? We don't need it" | Noted translation variance, kept claim |
| Oren Weil quote on item's removal | R14 | OK | Exact match | No change |
| Jan 4, 2023 removal date; Mayor pulled item after protest threat | R11/R12/R13/R14 | OK | R11 (published Jan 3, "meeting tomorrow/Wednesday") + R14 (Jan 4 removal) internally consistent | No change |
| Mayor named as "Dr. Yechiel Lasri" | R11/R12/R13/R14 | **Not directly confirmed, but corroborated** | R14 fetch didn't name him explicitly; independently confirmed he has been Ashdod's mayor continuously since Nov 2008 (through 2023 and beyond) via he.wikipedia.org/wiki/יחיאל_לסרי, which makes him the only person who could have been "the mayor" in Jan 2023 | Left as-is (low risk, corroborated indirectly) |
| Sharon Marck credited with blocking the plan | R1/R11/R14 | OK | Corroborated by Lior's notes + two independent live fetches | No change |
| Bat Yam sand-nourishment cycle (~40 yrs, Rock Beach Sand Nourishment Project, 2021, Ministry oversight) | R17 | OK | Exact match, including direct quote "This has been happening for 40 years already" | No change |
| Surf-break coordinates, tide range (both breaks) | R15/R16 | OK | Exact match | No change |
| Coastline length 6km, beach names, marina, Blue Flag | R18 | OK | Exact match | No change |
| Tetrapod art project: 40+ tetrapods, 3m/>12t, ~20yrs old, 9 artists, 2018-07-05 | R20 | OK | Exact match | No change |
| 2015 detached-breakwater proposal, Tzachi Abu, Lido/Mey-Ami, Ashkelon/Tel Aviv models | R21 | OK | Exact match | No change |
| 2019 "ecological breakwater" concept, Gershon Feldman, Coastal Protection Committee | R9 | OK | Exact match (except "patented" wording — see above) | No change beyond wording fix |
| Local-file references (R1, R2, R3) exist | — | OK | Verified files present on disk | No change |

## Blocked sources (unresolved)

- mdpi.com/2077-1312/14/18/1734 (and /pdf) — 403 Forbidden, re-checked. Richest quantitative source, never read in full. Specific figures marked pending in the dossier.
- kan-ashdod.co.il/news/122249, kan-ashdod.co.il/ashdodim/70762, israports.co.il, ashdodport.co.il, hamichlol.org.il, academia.edu/32067048 — all still blocked (403/rejected), unchanged from prior pass.
- web.archive.org — this session's WebFetch tool refuses this domain entirely (tool-level restriction, confirmed again this pass); could not be used to recover the now-dead ashdodnet.com article.

## Dropped sources

- ashdodnet.com/.../526785 — newly dead (HTTP 404); was live at original research time. Four surfer-quote review entries sourced only to this URL were deleted from the dossier.

## Summary

23 references checked. 15 claims/reference-groups confirmed as-is. 6 distinct claims fixed (planning year, opening-date framing, breakwater dimensions, Golik et al. study period, the "≈half" sediment-volume framing, and the "patented" technology wording; the cost figure was clarified/disambiguated rather than corrected). 2 claim-groups dropped (4 surfer quotes sourced to a now-dead page, and the previously-asserted "resolved via primary source" status of the MDPI figures, which are now explicitly marked pending). The dossier's first-line status was updated to reflect this pass.

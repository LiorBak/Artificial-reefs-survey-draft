# Source audit: reef cards, group A (2026-10-10)

Scope: `02_research/reefs/<slug>.json` + `.md` for borth-coastal-defence-reef, boscombe-surf-reef, bunbury-airwave, mount-maunganui-reef, palm-beach-gold-coast, prattes-reef-el-segundo, narrowneck-gold-coast. Standard: `_agent_briefs/task_source_audit.md` points 1, 3, 5, 7.
Method: (1) script scan of every narrative field for sentences with a digit and no `[R#]` tag (183 flagged; the large majority are continuation clauses cut by the sentence splitter, as SCHEMA.md warns; the real gaps are in the rows below); (2) every reference checked for author/date/title/venue/URL/access date and a location; (3) card numbers compared with each reef's `07_scale/shapes/<slug>/HANDOFF.md` key numbers (read-only); (4) PDFs in the repo used where a page number was missing (Borrero & Nelsen 2003 text checked directly). Web pages were NOT re-fetched (network blocked); locations for them are "whole web page, URL + access date". No card value was changed except where stated; every edit is labelled "AUDIT NOTE / 2026-10-10" in the card.
Status words: ok / fixed (card edited) / missing (cannot be obtained now) / mismatch (card vs model files, recorded; fixed in the card where the card was wrong).

Common fixes on all 7 cards
- `verdict_reason` field added (Bunbury already had one; extended): who decided (the card-writing research agent on the `verified_on` date; no Lior ruling is recorded for any of the 7) and why, with tags. Verdict values unchanged.
- References: LOCATION note appended to every web reference; tertiary sources (Wikipedia, consultancy pages) labelled; project notes (R13/R14/R15/R16-type rows: Lior's notes, master list) labelled NOT A CITABLE SOURCE; model-source references added where the card now quotes model facts.
- Currency conversions (`cost_usd_approx`) without a rate source labelled ASSUMPTION (Boscombe, Bunbury, Narrowneck) or corrected (Borth).
- `.md` kept in step: References section regenerated from the JSON, plus a "Source audit 2026-10-10" section listing the added wording (the md prose was not rewritten sentence by sentence).

## 1. borth-coastal-defence-reef
| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | Type "submerged" reef | R1/R4 vs drawings 9V5090/1020-1023: arm crest +0.50 mODN, oval +1.50 mODN; MSL +0.31 mODN | R16 (DRG 1020-1023), R18 (SMP2 p.4C.3), R19 (Esri 2024 rock bare) | design crest levels | mismatch -> fixed: card now says "submerged only at high water"; oval = breakwater |
| 2 | offshore distance 300 / 400 m; Blacka 110/140 m | R1, R2, R3, R14 | R14 Table 4.2 p.66 | text | ok; traced centroid 330.5 m (nearest 257, farthest 397) added [R19] |
| 3 | footprint (Blacka 72x170, 85x45 m) | R14 | Table 4.2 p.66 | text | mismatch with traced outline (N mound 144.9 x 27.6 m, oval 71.8 x 31.0 m): both kept, note added |
| 4 | spring range 4.7-4.8 m (R11), 6.0 m (Blacka) | R11, R14; SMP2 gives 4.30 m (MHWS +2.56 - MLWS -1.74 mODN) | R18 p.4C.3 | Israel comparison | mismatch -> three values listed, none preferred |
| 5 | cost_usd_approx US$15-17M / US$36M "at 1.25-1.6" | none | - | - | wrong low rate: fixed to ~1.56 USD/GBP (2013 value, CIA Factbook via IndexMundi, WebSearch result only) -> US$19-20M / ~US$45M, labelled ASSUMPTION [R20] |
| 6 | feasibility study May 2004 | R10 (blocked, web-search snippet) | - | year | ok; R4 added as the corroborating tag |
| 7 | all other cost, date, quote statements | R1-R4, R6 | whole pages | text | ok (page-level only); R2, R4 authors not confirmed |
| 8 | R5, R12 unused in the text; BBC News item in md Reviews has no JSON review | - | - | - | recorded |
| 9 | verdict "mixed" | agent, 2026-09-24 | - | - | fixed: reason + who added |

## 2. boscombe-surf-reef
| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | "~1 hectare" footprint, 55 bags, 13,000 m3 | R4, R1 (tertiary) | web pages | text | mismatch: reef plan area traced 4,042 m2 (121.1 x 45.0 m); Rendle design 4,474 / 5,450 m2; basis of 1 ha not stated -> both kept, note added [R22, R17] |
| 2 | "submerged mound" | R1; Rendle p.70-71 crest exposed at low tide | R17 | text | fixed (note: built crest +0.5 m CD = about -0.9 m MSL, conversion 1.40 m NTSLF vs Rendle 1.66 m, unresolved) |
| 3 | tide range "0.9-1.1 m" (one day, R12) | Mead et al. 2010 Table 1: MHWS +0.81, MLWS -0.95 m MSL (range 1.76 m) | R20 Table 1 | water levels of 3D model | fixed (sentence added) |
| 4 | Haifa wave figures 0.45-0.8 m [R14 = internal master list] | Lior's IsraMar Shikmona buoy screenshots Jul-Oct 2025 | 03_images/from_lior/suggestions/page2-4 | context | fixed: R14 re-cited as Lior's own readings; values not re-read |
| 5 | opening 19 Nov 2009 vs 2 Oct 2009; 32/46/54-55 bags; 4 vs 7 of 11 objectives | R1, R17, R18 | Rendle p.64-70; M&B p.4 | text | ok, disagreements already listed; not resolved |
| 6 | cost GBP 3.2M; USD 5.1M at 1.59, NZD 0.70 | R1, R2, R17 p.65 | - | text | cost ok; FX rates unsourced -> ASSUMPTION label |
| 7 | R13 (Lior's notes), R14 (master list) as references | - | - | - | labelled not citable; R11, R15, R16 unused |
| 8 | "n.d." web pages (R2, R4, R7, R10, R12) | - | - | - | missing: dates/authors not confirmed (listed in gaps) |
| 9 | Rendle thesis year 2016 (card) vs 2015 (shape.json) | PEARL record | - | - | open; PEARL not re-read |
| 10 | verdict "failed" | agent | - | - | fixed: reason + who added; M&B 7/11 flagged as interested party |

## 3. bunbury-airwave
| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | lat/lon (-33.31, 115.64) | model site point -33.32767, 115.62880 (2009 0 m AHD contour, WA DoT lidar) | R27 | position | mismatch (2 km) -> fixed in card |
| 2 | "Installation attempted Dec 2019" (no tag) | R1, R5 | whole pages | year | fixed (tags) |
| 3 | interview sentence in as_built_vs_design | R25 | Lior's notes | text | fixed ([R25] added); R25 citation completed (Bakalo 2026; surname "Troy ..." not given, presumed Bottegal, flagged) |
| 4 | "2-8 ft face range" (relevance) | none in the card | - | - | missing: labelled UNSOURCED |
| 5 | tide range ~1 m (sample day R13) | GHD 2021 Table 1: HAT 0.6, LAT -0.6 m AHD, MSL +0.1 | R26 p.6 Table 1 | 3D tides | fixed (sentence + reference) |
| 6 | R10 "Stab Magazine / The Inertia" but URL is The Inertia only | - | - | - | fixed: citation corrected, Stab item not located |
| 7 | A$75,000 = ~US$50,000 | unsourced rate | - | - | ASSUMPTION label |
| 8 | fill sand vs air, failure timing, waves "perfect", concrete | R25 vs press | - | - | ok (already in `sources_disagree`) |
| 9 | verdict "failed" | orchestrator brief, developer account checked 2026-10-05 | - | - | fixed: "who decided" added (research agent; not overruled by Lior) |

## 4. mount-maunganui-reef
| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | design paper "Black, S.M.; Kerry, A. 1999, Coastal Manag. 27:355-365" | real: Mead, S. and Black, K. (1999), Coastal Management 27(4): 355-365 | bibliographic record via web search; full text not seen | context | fixed (card text and R13 replaced) |
| 2 | "no crest-depth figure found" | BoPRC/Focus report: main bags -0.8..-1.0 m CD | R19 pp.6, 21 | crest of 3D model | mismatch -> fixed (type field + gap) |
| 3 | lat/lon null | shape.json centroid -37.6447833, 176.2025908 (Fig 3 NZ grid) | R19 Fig 3 | position | fixed |
| 4 | footprints 50x100, 70x30 arms, 90x70 (Blacka) | R2, R8, R18 | - | text | ok; traced -2.0 m CD outline 1,071 m2 (67.9 x 60.4 m), toe 1,424 m2 added |
| 5 | volume 2,800 vs design 5,000 / 6,000 / 6,500 m3 | R2, R17 Fig 3, R1 | M&B Fig 3 | text | ok; model 2,945 m3 at ASSUMED bed -3.6 m CD (D1; +-0.5 m = +-22 %) stated |
| 6 | tides (tides4fishing) | LINZ Tauranga: MHWS 1.96, MLWS 0.21 m CD (range 1.75 m); MSL = CD + 1.13 | R21, R22 | 3D tides | fixed |
| 7 | R14, R15 (Lior's notes, master list) | - | - | - | labelled not citable |
| 8 | Mead et al. 2007 conference: card "18th ACOEC", shape.json "17th ... Melbourne" | - | - | - | recorded: card is likely right (2005 Adelaide = 17th, 2007 = 18th); shape.json wording for main/3D owner; not confirmed |
| 9 | verdict "failed" | agent; M&B call it "a failure in terms of surfing" | R17 | - | fixed: reason + who |

## 5. palm-beach-gold-coast
| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | 160 x 80 m; Royal HaskoningDHV 144 m | City asset polygon 160 x 80 m, 11,941.7 m2; traced 162.3 x 91.3 m (mean width 73.8 m); 144 m = concept width | R19, R20, R22 | plan | mismatch explained, added |
| 2 | ~270 m vs 330 m offshore | traced: nearest toe 225, centroid 305, farthest 374 m; 279 m from OSM coast | R21 | plan | mismatch recorded; start point of "270 m" unknown |
| 3 | 25,000 m3 / 60,000 t | ICM text; model envelope 22,020 m3; register 33,000 (units?) | R13 | volume | added with their different meanings |
| 4 | crest "1.5 m below MSL; 60 cm at LAT" | MSQ: MSL = LAT + 0.88 m; -1.5 m MSL = -0.62 m LAT; concept paper -1.5 m AHD | R22, R23 | crest | ok + conversion added; chart label "FISH HAVEN 1.5MT" differs by 0.88 m (open) |
| 5 | tide "~1.5 m illustrative weekly" (WillyWeather) | MSQ planes: spring range 1.31 m, HAT-LAT 2.03 m | R23 | tides | fixed |
| 6 | lat/lon null | traced centroid -28.107334, 153.470913 | R19, R20 | position | fixed |
| 7 | status: monitoring | Prenzler et al. 2022 ICCE abstract 12921: stable | R24 (abstract only; DOI/pages/authors not confirmed) | status | fixed (sentence + ref) |
| 8 | AU$18.2M vs 18.3M; ~US$12.5M (RWR conversion) | R2, R4, R5, R7, R9, R13 | web pages | cost | ok (disagreement kept); price year not stated |
| 9 | 12 refs with "n.d." | - | - | - | missing: dates/authors not confirmed |
| 10 | verdict "partly worked" | agent | - | - | fixed: reason + who |

## 6. prattes-reef-el-segundo
| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | Phase 2 date: 2000 (Blacka) vs spring 2001 | Borrero & Nelsen 2003: 23-24 April 2001, 90 bags, +80 % | R28 p.3 | chronology | disagreement RESOLVED for 2001 (primary text checked in the PDF) |
| 2 | bag weight 14 t vs 12.7 t (Blacka) | R28 p.2: ~14 tons | p.2 | size | added; 12.7 t is derived/lower |
| 3 | crest -0.9 m MLLW vs ~2.4 m "at zero tide" | R28 p.2-3: -6 ft MLLW (1.83 m) after Phase I; within 3 ft (0.91 m) after Phase II; 8 ft is a commenter's remark | R28 | crest | gap updated; drawing label "-6 ft MSL" (0.849 m) still open (HANDOFF J1, decided by Lior to keep MLLW) |
| 4 | 64 x 29 m (Blacka) vs traced 58.0 x 28.6 m (435.2 m2, Phase I design layout, 110 bags) | R19; Skelly drawing via RWR; R28 Fig 4 | R19 Table 4.2; R29 | plan | mismatch recorded (+10 %); the traced outline is the DESIGN layout, not the 200-bag reef |
| 5 | ~1,400-1,600 m3, 200 bags | R28 p.16: ~1600 m3 in 200 bags; 1,264-1,422 m3 at 80-90 % fill (project arithmetic); M&B 1,350 m3 | R28, R18 | volume | ok, listed |
| 6 | tidal range 1.4-1.7 m (live tide page) | NOAA 9410840: MHHW - MLLW = 1.653 m | R30 | tides | fixed |
| 7 | lat/lon (33.915123, -118.432624) | model: no fix; hint 33.92058, -118.43335 +-150 m (600 m away) | gap note | position | mismatch: NOT changed (compile_data uses the shape hint); decision for main/Lior |
| 8 | "UV/wave abrasion ... within ~2 years" (no tag) | probably R3/R7/R10 | - | - | missing: source not confirmed |
| 9 | Borrero & Nelsen 2003 venue/year (file prints neither) | project record: 3rd Int. Surfing Reef Symposium, Raglan | - | - | missing: not confirmed |
| 10 | R14, R15, R16 notes/master list | - | - | - | labelled not citable; R5 unused |
| 11 | verdict "failed" | agent | - | - | fixed: reason + who (bag-degradation clause dropped because untagged) |

## 7. narrowneck-gold-coast
| # | statement / number | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | ~400 containers, 70,000 m3 | R1, R3, R9 (tertiary) vs Jackson et al. 2007: 408 containers, 20 m x 3-4.5 m; ~450 by 2006; +84 in 2018; 534 total; 60,000 m3 behind the 147 m3/container | R26 p.4; R27 pp.3-4 | size | mismatch 60,000 vs 70,000 m3 recorded, not reconciled |
| 2 | footprint 350x600 / 450x250 / Blacka 170x280 m | R9, R8, R23 | - | plan | mismatch: council polygon 171 x 262 m agrees with Blacka; photo trace 6,239 m2 (bbox 113.3 x 157.4 m) is a lower bound; 350x600 and 450x250 unsupported |
| 3 | crest "lowered 1 m ... 1.5 m below low-tide waterline" | design -0.67 m AHD (via Vieira da Silva), adopted -1.5 m AHD, target -1.5 m LAT = -2.5 m AHD, measured -2.2 m AHD | R26 pp.4, 7; R29 p.5 | crest | mismatch: levels listed side by side; AHD = LAT + 0.760 [R25] |
| 4 | lat/lon (-27.98639, 153.42972) | traced centroid -27.986629, 153.434052 (420 m east) | R30 | position | fixed |
| 5 | tide comparison missing numbers | MSQ: spring range 1.31 m, HAT 2.03 m | R25 | tides | fixed |
| 6 | R22 title wrong ("Multi-purpose reefs: lessons learned") | Mead & Borrero 2011 "Multi-Purpose Reefs - A Decade of Applications" | - | - | fixed |
| 7 | secondary citations inside text (Raybould & Mules 1998, Turner 2005/2006, Ranasinghe 2001, Mead 2000, Vieira da Silva 2021) | via Blacka 2013 / Mead & Borrero 2011 | - | - | ok as "cited in"; originals not opened |
| 8 | cost A$2.3M / 2.1M / 2.5M (Lior, currency unstated) ; FX 0.65 / 0.75 | R3, R5, R10, R19-20 | - | - | cost disagreement kept; FX = ASSUMPTION |
| 9 | Black & Mead 2001, Jackson 2007 pages 67-79, Jackson 2012 DOI | - | - | - | missing: not confirmed (already in REQUESTS) |
| 10 | commenter "warddy" 2019; anonymous Swellnet comments | R14 | - | - | ok as opinion; labelled in card |
| 11 | R17-R21, R24 internal notes/master list/report | - | - | - | labelled not citable |
| 12 | verdict "mixed" | agent | - | - | fixed: reason + who |

## Totals (key items checked, not every sentence)
See the counts in the final message. Values that look wrong for main: Borth USD conversion (fixed in the card); Prattes card lat/lon 600 m from the model hint; shape.json of Mount Maunganui gives "17th ... Melbourne" for Mead et al. 2007 (card says 18th); Narrowneck/Palm Beach/Boscombe `cost_usd_approx` rates unsourced. Page-text edits for main (04_build/data): none required by this audit; the compile step takes card fields as they are (new field `verdict_reason` is passed through, lat/lon on Bunbury, Mount Maunganui, Palm Beach, Narrowneck changed, see compile_data.py location logic).

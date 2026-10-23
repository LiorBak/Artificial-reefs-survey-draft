# SOURCE AUDIT 2026-10-10 - mexico-reef-2026-unnamed (Xala Reef, Costalegre, Jalisco, Mexico)

Files audited: FEASIBILITY.md, HANDOFF.md (this folder has no shape.json, METHOD.md, sources.md or VERIFY.md, on purpose: nothing was traced), registry `03_images/reefs/mexico-reef-2026-unnamed/images.json` (2 rows), the reef card `02_research/reefs/mexico-reef-2026-unnamed.json/.md` (read only, not edited), and `07_scale/reefs/mexico-reef-2026-unnamed.footprint.json` (read only, outside this folder). No outline, no 3D (point 8 n/a). No model value exists.
Page status (Lior, 2026-10-10): HIDDEN. Mechanism: no shape.json (compile_data: "No shape.json: no traced outline exists") plus footprint.json display:false.
Network: raisedwaterresearch.com returned HTTP 403 in the earlier run and WebFetch does not work; the RWR post was therefore NOT re-fetched. WebSearch was used.

## 1. Sources and how each was used (point 2)
| id | full citation | location | what was read / how | accuracy | feeds | status |
|---|---|---|---|---|---|---|
| R1 (card) | Indelicato, P., Raised Water Research (2026-03-31). Unveiling the new reef in Mexico. https://raisedwaterresearch.com/unveiling-the-new-reef-in-mexico/ (also https://raisedwaterresearch.com/?p=5715) | post text; accessed 2026-09-24 and re-fetched 2026-09-25 by the footprint task (per the footprint file) | reef tag "Xala"; designer Simon Brandi Mortensen; unveiling event 16 Apr 2026 (California Surf Club, Redondo Waterfront); images | text; NO dimensions, NO coordinates | identity and designer only | ok(card). WebSearch snippet of the same post (this audit) does not itself show the word "Xala" or any size; the Xala name rests on the image caption "Mexico's first artificial surf reef at Xala" recorded in the card (see A1) |
| R3 (card) | Romeyn, K. (2025-04-22). With Xala, Richard Gere has Co-Founded a Luxury Mexican Paradise. The Hollywood Reporter. https://www.hollywoodreporter.com/lifestyle/lifestyle-news/xala-richard-gere-luxury-mexican-paradise-1236192415/ (read through a syndicated copy https://www.yahoo.com/lifestyle/richard-gere-next-great-role-130000544.html) | article text | "3,000 truckloads of boulders from a nearby quarry"; reef already reported by April 2025 | journalistic, no engineering numbers | material, timeline | ok(card) |
| R4 (card) | Free Republic repost of R3 (https://freerepublic.com/focus/f-chat/4312838/posts) | - | cross-check copy | NOT independent of R3 | corroboration of R3 text only | ok(card) |
| R5, R10 (card) | Hospitality Net (2026), Six Senses Xala opening, https://www.hospitalitynet.org/announcement/41010415.html; Xala homepage https://www.xala.com | - | location (Costalegre, ~10 min from Chalacatepec airport), developer, purpose statement | no reef dimensions | location context | ok(card) |
| R6, R7, R12 (card) | WSCC 2026 speaker bio (https://www.wscc2026.com.au/key-speakers/simon-brandi-mortensen/); RWR Palm Beach Reef page (https://raisedwaterresearch.com/spot/artificial-reef/australia/queensland/palm-beach-reef/); RWR interview with Simon Mortensen (https://raisedwaterresearch.com/interview-with-simon-mortensen-the-brains-behind-the-palm-beach-reef/) | - | designer pedigree; Palm Beach comparison data (~160 x 80 m, ~270 m offshore, crest ~1.5 m below MSL; DHI news 2019-11 also lists these in WebSearch snippets); rock-vs-geotextile philosophy | about ANOTHER reef | analogy only | ok(card). Not evidence of Xala's size |
| img-01, img-02 | Raised Water Research post images, https://raisedwaterresearch.com/wp-content/uploads/2026/03/Reef2.jpg and .../2026/04/Reef1.jpg; post date 2026-03-31; all rights reserved, licence not stated, private copies | registry | looked at: surfer in a wave; drone shot of a peeling left; structure submerged, no scale, no coastline, no landmark | - | context only; nothing measured | ok |
| analogy envelope | 07_scale/reefs/mexico-reef-2026-unnamed.footprint.json: 160 x 80 m, 11,200 m2, 230-310 m offshore, crest 1.5 m below MSL, all copied from Palm Beach (R7) | - | admitted "design analogy, not measured" | NOT a measurement | none | ok: rejected, flagged display:false |
| Gemini | "~140 x 75 m"; no CAD entry in its reef_footprints.json | 07_scale/00_gemini_footprints_extract.md | compared | no source | none | ok: not used |
| area pin | Google Maps pin 19.71861, -105.23222 (card images_rejected) | - | near Chalacatepec airport | explicitly NOT the reef | none | ok |

## 2. Statement-by-statement check (point 1)
| # | statement | source | how used | status |
|---|---|---|---|---|
| 1 | Rock/boulder reef, "3,000 truckloads" | R3 (Romeyn, THR 2025-04-22), R4 | material | ok(card); a truckload is not a volume: converting it to m3 would need a truck size (not given) |
| 2 | Designer Simon Brandi Mortensen, DHI Seaport | R1; R6 (WSCC bio: "Principal Coastal Engineer, Managing Director, DHI Seaport") | designer | ok(card). The WebSearch snippet of R1 did not show the name; the card quotes it from the page |
| 3 | Unveiled 16 April 2026 (event); post 2026-03-31 | R1 | date | ok(card) |
| 4 | Built "by April 2025" (R3) vs "newly completed" March 2026 (R1) | R3, R1 | timeline | OPEN: one-year gap unresolved (phased build? 2025 reports of works in progress?). Not used in any geometry |
| 5 | Coordinates, length, width, crest depth, volume, cost, contractor, dates: not disclosed | card gaps list; 2026-09-24 sweep; 2026-10-10 re-check; WebSearch 2026-10-10 (Xala + Mortensen + DHI + dimensions): only Palm Beach data returned | the reason for hiding | ok. Search returns nothing for Xala |
| 6 | Palm Beach 160 x 80 m, ~270 m offshore, crest 1.5 m below MSL | RWR Palm Beach page (card R7); DHI news 2019-11 (WebSearch snippet, https://worldwide.dhigroup.com/global/news/2019/11/construction%20of%20dhi%20artificial%20reef%20design%20to%20enhance%20coastal%20protection%20and%20surfing%20is%20completed) | analogy only | ok as facts about Palm Beach; NOT facts about Xala |
| 7 | FEASIBILITY section 4 said: "If the page shows it, label it 'schematic, analogy only, confidence low'" | - | - | fixed: contradicts Lior's rule (2026-10-10); replaced by "must not be shown" |
| 8 | FEASIBILITY: "satellite imagery would only show the wave line, not the reef toe" | reasoning, no test (no coordinates, no tiles) | - | ok as an unsupported expectation: marked as expectation (A3) |
| 9 | Registry licence / date fields | images.json | - | ok: retrieval and image dates present; "2026-03/04 (upload path)" for img-02 is an upload path date, not a capture date |

## 3. Methods (point 3)
No method beyond reading: card, registry, footprint file, one web search. Nothing traced, scaled or estimated. The Palm Beach analogy was used by an earlier agent to make the envelope and was rejected.

## 4. Assumptions (point 4)
| id | assumption | why | effect | replaced by |
|---|---|---|---|---|
| A1 | "The Mexican reef unveiled by RWR/California Surf Club in April 2026" is the Xala reef | RWR image caption "Mexico's first artificial surf reef at Xala" (card), Mortensen as designer of both, Hollywood Reporter 2025 on Xala's boulder reef | if wrong, every Xala-specific fact in the card (3,000 truckloads, Costalegre) belongs to another site | RWR post text with the site named; DHI case study |
| A2 | The 2025 "boulder surf break" (R3) and the 2026 "newly completed reef" (R1) are the same structure | same developer, same designer, same material | timeline and "built" date uncertain by a year | construction record / SEMARNAT MIA |
| A3 | A submerged boulder reef would not be visible on satellite imagery (only the wave line) | other submerged reefs in this project (Opunake, Kovalam) are not visible | would only matter once coordinates exist | test on dated imagery after coordinates |
| A4 | Designer pedigree (Palm Beach) does NOT tell us Xala's size | different site, wave climate and brief | none (nothing drawn) | design report |

## 5. Decisions (point 5)
| id | decision | options | who / when | reason |
|---|---|---|---|---|
| D1 | No outline, no shape.json, no METHOD / sources / VERIFY files created | draw the analogy envelope / schematic / nothing | agent 2026-10-10; confirmed by Lior's rule the same day | any outline would be invented |
| D2 | Analogy envelope (160 x 80 m) not promoted to shape.json | - | agent 2026-10-10 | it measures Palm Beach, not Xala |
| D3 | Gemini 140 x 75 m not used | - | agent | no source (rule 2) |
| D4 | Hidden on the page, text reason from FEASIBILITY | - | Lior 2026-10-10 | shapes we do not know are not shown |

## 6. Confidence (point 6)
Plan, position, size, crest, seabed, tides, volume: NONE (no data). Identity of the structure: MEDIUM (A1). Build date: LOW (A2). Verdict "cannot be traced": HIGH.

## 7. Consistency (point 7)
FEASIBILITY, HANDOFF, card and footprint file agree that no dimension exists, except FEASIBILITY item 4 (fixed). Card `size` field already says "not disclosed"; the 160 x 80 m envelope still sits in the footprint file with `verified_on 2026-09-25` and `confidence low` (hidden by display:false; for main, consider removing the polygon from that file when convenient: not edited here).

## 8. Counts
Statements checked 9; ok 7; fixed 1; open 1 (build year gap); missing: every plan/dimension source (listed in FEASIBILITY section 3); assumptions 4; decisions 4.

## 9. Image registry check (03_images/reefs/mexico-reef-2026-unnamed/)
2 rows checked by script: every row has citation, image_url, source_page, page_or_figure, image_date, credit, license, retrieved, shows, how_used and file; every file exists on disk. Licences are "not cleared" private copies as recorded. IMAGES.md not rewritten.

## 10. Addendum - network pass 2026-10-10 (full access)
The earlier statement "the RWR post was not re-fetched / RWR returned 403" is now superseded: the post was fetched (HTTP 200) and its text saved in src/web_text/rwr_unveiling-the-new-reef-in-mexico_2026-03-31_text.txt.
| # | statement | source | location | how used | status |
|---|---|---|---|---|---|
| N1 | Reef location to be revealed 16 April 2026, 6:30 PM, California Surf Club, Redondo Waterfront; designer Simon Brandi Mortensen; reef "newly completed" | Indelicato, P. (2026-03-31). Unveiling the new reef in Mexico. Raised Water Research. https://raisedwaterresearch.com/unveiling-the-new-reef-in-mexico/ , accessed 2026-10-10 | post text | card R1 re-verified from the page | ok (re-fetched) |
| N2 | Xala: 3,000 acres, five miles of coastline, ~65 miles south of Puerto Vallarta, 10 min from the Costalegre airport, two Ramsar estuaries | Xala (n.d.). Xala Community: Life on Mexico's Costalegre. https://xala.com/community/ ; Beachfront Real Estate in Costalegre, Jalisco. https://xala.com/real-estate/ ; both accessed 2026-10-10 | page text (saved in src/web_text) | location context only | ok (developer marketing, not independent) |
| N3 | "construction of a new coastal protection reef to create a consistently great wave to surf while safeguarding the marine habitat" | Six Senses Xala press page, https://xala.com/press/six-senses-xala/ , accessed 2026-10-10 | page text | purpose | ok (marketing text) |
| N4 | Mortensen designed "three additional surfing reefs globally, most recent in the Americas" | WSCC 2026 speaker bio, https://www.wscc2026.com.au/key-speakers/simon-brandi-mortensen/ , accessed 2026-10-10 | bio | supports A1 weakly (does not name Xala) | ok |
| N5 | Chalacatepec airstrip at about 19.719,-105.231; Xola-Paraman lagoon mouth about 19.731,-105.291 | read off Esri World Imagery 2025-05-23 (registry img-03) via satellite.py pix2ll, by eye | src/imagery | location context | ok (by eye, +-100 m) |
| N6 | No artificial rock works visible on the coast or at a rocky point (19.679,-105.262) | Esri imagery 2025-05-23, registry img-03, img-04 | viewed once each | none (no geometry) | ok; A3 (submerged reef invisible) still untested |
| N7 | No MIA / DHI case study / paper found | dead_ends/mexico-reef-2026-unnamed.json | - | verdict | ok |
New assumption A5: the Xala reef lies on the ~5-mile Xala coast (developer text); the exact stretch is unknown, so the images img-03/04 are not shown. No decision changes (D1-D4 stand). Counts of this addendum: statements 7, ok 7.

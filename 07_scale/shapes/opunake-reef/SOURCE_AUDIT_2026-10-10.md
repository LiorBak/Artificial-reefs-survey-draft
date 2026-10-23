# SOURCE AUDIT 2026-10-10 - opunake-reef (Opunake Surf Reef, north reef, geotextile bags, Taranaki NZ)

Files audited: shape.json (status `no_source`, no outline), FEASIBILITY.md, METHOD.md, VERIFY.md, sources.md, HANDOFF.md, registry `03_images/reefs/opunake-reef/images.json` (10 rows). No outline and no 3D exist (point 8 n/a). No model value changed.
Page status (Lior, 2026-10-10): HIDDEN. Mechanism: `07_scale/reefs/opunake-reef.footprint.json` has display:false and DO_NOT_DISPLAY; shape.json status `no_source` and `canonical` null also hide it in compile_data. Warning from the earlier agent (still open for main): 04_build/src/compile_data.py load_footprint() read the old wedge file before the flag existed; the SHAPE_SPEC comment block in compile_data now says hidden reefs keep no polygon, so check once on the next page build that no wedge appears.
The papers in `papers/` were re-read here at the cited places; WebSearch used for citations.

## 1. Sources and how each was used (point 2)
| id | full citation | location | what was read / how | accuracy | feeds | status |
|---|---|---|---|---|---|---|
| sat_z20 / mid / wide / current (reg. img-07 to 10) | Esri, Maxar, Earthstar Geographics and the GIS User Community. World Imagery, https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer, centre -39.4577, 173.8545, r 250 m, z20 (4338 px, 0.115 m/px), capture 2025-01-16; retrieved 2026-10-04 | `src/opunake_sat_*.png` + `.geo.json` | looked at once (downscaled): no bag field, no linear feature in the water | scale recomputed here: 156543.03 x cos(39.4577 deg) / 2^20 = 0.1153 m/px, matches | search for the structure: negative result only | ok |
| ov_search | our annotation of sat_z20 (scale bar + negative finding) | overlays/search_frame_z20_no_structure.png | - | - | documentation | ok |
| R1 | Reid, M. and Sumner, B. (2021-12-06). The Kiwi scientist and the failed surf breaks. Newsroom (NZ). https://newsroom.co.nz/2021/12/06/the-kiwi-scientist-and-the-failed-surf-breaks/ | article body | 90 x 20 m footprint | text, one lineage | the only size we have | ok(card) |
| R2 | Raised Water Research (n.d.). Opunake [spot page], https://raisedwaterresearch.com/spot/artificial-reef/new-zealand/north-island/opunake/ (relays Stuff.co.nz 2009/2010, not seen in the original) | page text | 90 x 20 m, 27 bags by 2009 | secondary | size | ok(card) |
| R3 | Moores, A. (Mar-Apr 2006). Artificial surf reefs - coming to a beach near you. New Zealand Geographic 078. https://www.nzgeo.com/stories/artificial-surf-reefs-coming-to-a-beach-near-you/ | text only; the page figure NOT seen | pre-construction design details | text | size / design (figure still wanted) | ok(card) |
| R4 | Luis, M.P. (n.d.). The history of artificial surf reefs. SurferToday. https://www.surfertoday.com/surfing/the-history-of-artificial-surf-reefs | - | near-identical to R2 | same lineage | corroboration (not independent) | ok(card) |
| R9 | Black, K. / ASR Ltd (2004). Studies for Resource Consent: Opunake Surfing Reef (report for South Taranaki District Council). https://www.researchgate.net/publication/273133845 | only a search snippet seen | existence of the study | authors, report number, pages NOT confirmed | would hold the plan | ok(card); NOT HELD |
| P-MB | Mead, S. and Borrero, J. (2011). Multi-Purpose Reefs - A Decade of Applications. Proc. 20th Australasian Coastal and Ocean Engineering Conference (Coasts & Ports 2011), ASR Ltd, Raglan NZ (authors read on p.1 of Lior's PDF) | s.3.1.5 (PDF p.3-4): "4,800 m3 Opunake Reef commenced early 2006 ... plagued with construction problems"; Fig 1 world map | re-read here | as published (designers' own account) | volume, timeline | ok. URL https://search.informit.org/doi/10.3316/informit.715072832934166 is given by the card; NOT confirmed by search in this audit |
| P-WRL | Blacka, M.J., Shand, T.D., Carley, J.T. and Mariani, A. (2013). A Review of Artificial Reefs for Coastal Protection in NSW. UNSW WRL Technical Report 2012/08. https://doi.org/10.4225/53/58e1dc7368c7a | Table 4.1-4.4; Opunake row in Table 4.2 printed p.65 (PDF p.77): GCs, 30 m x 100 m, depth 1.8-3.0 m, ~300 m offshore, "At LAT"; Table 4.3 printed p.67 (PDF p.79): tide >3.0 m; Table 4.4 printed p.69 (PDF p.81): A$0.93 M, 274 | re-read here | as published, primary data not given (it cites TRC 2009) | second size (conflicts with R1/R2) | ok (re-read) |
| P-Rendle | Rendle, E.J. (2016). The Environmental, Social and Economic Impacts of an Artificial Surf Reef - The UK Experience. PhD thesis, University of Plymouth. Table 2.1, printed p.41 (PDF p.41): "Opunake 2006* North Island NZ 4,800 SFC AUS$ 760,000 (US$ 494,682)" (column header "Total [AUS$] BPS US$ £/m3" read here); reference list PDF p.298: Taranaki Regional Council 2009 | re-read here | as published | volume, cost | ok. fixed: shape.json said "Rendle 2012 thesis"; the thesis is 2016 (Rendle and Davidson 2012 is a different, conference paper) |
| TRC2009 | Taranaki Regional Council (2009). Opunake Artificial Reef Monitoring Programme 2005-2009. Technical Report 2009-33 (number from the card/earlier pass; Rendle's reference list gives place "Opunake, New Zealand", the card says Stratford: place NOT confirmed) | - | WebSearch 2026-10-10: not found online | - | would hold monitoring surveys | NOT HELD |
| R7 | Surf-Forecast.com (n.d.). Opunake Beach Surf Guide. https://www.surf-forecast.com/breaks/Opunake-Beach | sample tide cycle | high 2.94 m / low 0.47 m is ONE sample day, datum not stated | not a tidal range | context only | ok(card). Blacka Table 4.3 (>3.0 m) is the better source |
| R8 | Wikipedia, Opunake. https://en.wikipedia.org/wiki/%C5%8Cpunake | township coordinates 39.450 S 173.850 E | - | township, not the reef | search frame centre only | ok(card) |
| Gemini | polygon 30 x 67 m inverted, dims 80 x 30 m; "Mead & Black 2007 Design Dossier", "TRC Monitoring Records 2010" | - | compared | self-contradictory; sources inaccessible | none | ok: not used |
| old wedge | 07_scale/reefs/opunake-reef.footprint.json (-10,110),(10,110),(0,200) | - | analogy to Mount Maunganui, admitted placeholder | not evidence | none | ok: flagged DO_NOT_DISPLAY |

## 2. Statement-by-statement check (point 1)
| # | statement | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | Footprint "around 90 m long and 20 m wide", north reef only | R1, R2, R3, R4 (one lineage) | article text | only size; no outline | ok(card); axis assignment (90 m shore-normal?) is an inference of the earlier file, not stated |
| 2 | Second size: 30 m longshore x 100 m cross-shore, depth 1.8-3.0 m, ~300 m offshore, at LAT | Blacka et al. 2013 Table 4.2 | printed p.65 | conflict recorded | ok (re-read). OPEN conflict 90 x 20 vs 30 x 100; the WRL values may be the design extent. Neither is used |
| 3 | 27 geotextile bags by 2009 | R2, R4 | - | context | ok(card) |
| 4 | Design volume 4,800 m3; ~1,400 m3 still needed; last work May 2008 | Mead & Borrero s.3.1.5 (PDF p.3-4); Rendle Table 2.1 (4,800 m3, A$760,000) | re-read here | context | ok. Cost conflict: Rendle A$760,000, WRL A$0.93 M, R1 NZ$1.1 M allocation (card). Not used in geometry |
| 5 | Location "north side of the cove"; coordinates uncertain by several hundred metres (township 39.450 S 173.850 E; surf break 39.46 S 173.86 E) | R8; R7 | - | frame centre | ok; the two points are 0.5-1 km apart: stated |
| 6 | Reef not visible on Esri 2025-01-16 | our viewing | METHOD 2 | negative finding | ok (one image, one date; submerged bags, breaking waves, turbid water) |
| 7 | Scale 0.115 m/px | sidecar; recomputed here | - | scale bar on overlay | ok |
| 8 | Papers searched 2026-10-10: Opunake only in text/tables (Mead & Borrero p.1,3-4; Rendle Table 2.1 + refs p.298; Blacka Tables 4.1-4.4 + refs) | PyMuPDF text layer | sources.md search log | no plan | ok; re-confirmed here for Rendle p.41 and Blacka PDF p.77-81. The 2007 Mount Maunganui paper is a scanned PDF, not OCR'd (no installs allowed) and is about Mount Maunganui: unread, so "no plan in papers/" is complete for text layers only |
| 9 | WebSearch x9 found no plan, coordinates, crest datum or survey | sources.md search log | - | - | ok; one more search in this audit for TRC Technical Report 2009-33: not found online |
| 10 | Tide: sample 2.94 / 0.47 m; >3.0 m range | R7; WRL Table 4.3 | - | context | ok; no gauge or datum |
| 11 | shape.json `no_source` list names "Rendle 2012 thesis" | - | - | - | fixed -> Rendle (2016) |
| 12 | shape.json references list only R2 | - | - | - | fixed: R1, R3, R9, Mead & Borrero, Blacka, Rendle, TRC 2009 added |

## 3. Methods (point 3)
Negative-search method only: (a) local registry and card read; (b) saved Esri frames viewed once at 1100 px; (c) text-layer search of the five PDFs in papers/; (d) nine plus one WebSearch queries; (e) Gemini extracts compared. Nothing was traced, interpolated or scaled. No AI estimate influenced any number (Gemini rejected).

## 4. Assumptions (point 4)
| id | assumption | why | effect | replaced by |
|---|---|---|---|---|
| A1 | The reef is "on the north side of the cove" within a few hundred metres of 39.457 S 173.854 E | card text + two coordinates 0.5-1 km apart | search frame only; no outline depends on it | consent plan, aerial, Navionics |
| A2 | Absence of a visible structure on the 2025-01-16 frame is NOT evidence that the reef is absent | bags submerged, surf and turbid water | none (nothing drawn) | dated clear-water image |
| A3 | The text size 90 x 20 m and WRL 30 x 100 m may refer to different things (bag field vs design extent) | no definition in either source | none; both recorded | TRC 2009 or Black et al. 2004 |
| A4 | The built state is the unfinished north reef (27 bags, ~1,400 m3 short) | Mead & Borrero | which state any drawing would show is unknown | as-built survey |
No numeric assumption feeds any model; none can be hidden in a drawing because there is none.

## 5. Decisions (point 5)
| id | decision | options | who / when | reason |
|---|---|---|---|---|
| D1 | Do not trace the old wedge schematic | trace / ignore | agent 2026-10-10 | placeholder by analogy, not evidence |
| D2 | shape.json status `no_source`, no outline | draw text bbox 90 x 20 m / nothing | agent 2026-10-10, confirmed by Lior's rule | an unsourced bbox would look like a measurement |
| D3 | Archive the 3 unlabelled overlays of 2026-10-04 | keep / archive | agent 2026-10-10 | origin unrecorded (overlays/archive_unverified_2026-10-04/) |
| D4 | Shape hidden on the page; no 3D | - | Lior 2026-10-10 | shapes we do not know are not shown |
| D5 | Gemini not used | - | agent | unverifiable |

## 6. Confidence (point 6)
Plan: NONE (no outline). Position: very low (hundreds of metres). Size: LOW (90 x 20 vs 30 x 100 m conflict). Crest: NONE (no datum; design wave height 1.8-2.5 m is not a crest level). Seabed: NONE. Tides: LOW (WRL >3.0 m range, no levels). Volume: LOW-MEDIUM (design 4,800 m3; built less). Overall: no shape.

## 7. Consistency (point 7)
shape.json, FEASIBILITY, METHOD, VERIFY, sources agree except items 11 and 12 (fixed). The card correctly shows both sizes. sources.md/HANDOFF say Rendle 2016; shape.json said 2012 (fixed).

## 8. Counts
Statements checked 12; ok 10; fixed 2; mismatch 1 open (size 90 x 20 vs 30 x 100; recorded, not a defect of the files); missing 3 documents (TRC 2009, Black et al. 2004, NZ Geographic figure); assumptions 4; decisions 5.

## 9. Image registry check (03_images/reefs/opunake-reef/)
10 rows checked by script: every row has citation, image_url, source_page, page_or_figure, image_date, credit, license, retrieved, shows, how_used and file; every file exists on disk. Licences are "not cleared" private copies as recorded. IMAGES.md not rewritten.

## Update 2026-10-13 (agent: Opunake TRC/NZGeo task) - what this audit no longer says
This audit (2026-10-10) predates the reading of TRC Technical Report 2009-33 and the NZ Geographic print. Superseded items: (1) 'no reef coordinates / position very low': position is now bounded by the consent 6376-1 occupation area (189 x 94 m, centre -39.45943, 173.85163), confidence medium-high for the area, low for the reef inside it; (2) 'sizes disagree 90 x 20 vs 30 x 100 m': resolved, design 99 x 30 x 3.5 m (TRC printed p.4), 90 x 20 m = 2004 concept (Daily News 2004-06-11); (3) 'crest none': shallowest contour 0.0 m below chart datum (LAT), seabed 1.8-3.0 m below chart datum (TRC printed p.3); (4) assumptions A1 and A3 closed, A5-A11 and decisions D6-D9 added in shape.json; (5) the old unread leads TRC 2009-33 and NZ Geographic are now read. Unchanged: no bag layout, no as-built survey, shape stays hidden (status envelope_only). See FEASIBILITY.md, METHOD.md (2026-10-13), sources.md.

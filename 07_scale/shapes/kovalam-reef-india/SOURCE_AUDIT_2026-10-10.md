# SOURCE AUDIT 2026-10-10 - kovalam-reef-india (Kovalam Reef, Lighthouse Beach, Kerala)

Files audited: shape.json, FEASIBILITY.md, METHOD.md, VERIFY.md, sources.md, HANDOFF.md, rectify_result.json, registry `03_images/reefs/kovalam-reef-india/images.json`. No 3D (point 8 n/a). No model value changed.
Page status (Lior, 2026-10-10): HIDDEN. Mechanism: `07_scale/reefs/kovalam-reef-india.footprint.json` display:false with a reason (outside this folder, not edited). Reason / checks / assumptions now in FEASIBILITY.md and shape.json (`page_status`).
In this audit the papers in `papers/` were re-read at the cited places (PyMuPDF text layer) and WebSearch was used for citations.

## 1. Sources and how each was used (point 2)
| id | full citation | location | what was read, how | accuracy | feeds | status |
|---|---|---|---|---|---|---|
| img1 (reg. img-07, crop of img-06) | ASR Ltd (2011). Multi-Purpose Reef Design and Construction, Kovalam, India (brochure, "kovalam-coastal-protection.pdf"), Wayback capture 2011-11-06, http://web.archive.org/web/20111106035249/http://www.asrltd.com/media/project-pdf/kovalam-coastal-protection.pdf; photo reproduced uncropped in Blacka et al. 2013 Fig 4.5, printed p.71 (PDF p.83), "Source: ASR, 2012" | brochure p.1, upper-left photo; 915x735 px | oblique photo from the lighthouse end; 18 vertices around 5-6 olive strips + whitewater patch, read with a 20 px grid; then unprojected to the sea plane with a fitted pinhole camera | photo space +-8 px (clear part), +-25 px at the haze-covered tip; metric scale NOT fixed (see A2) | plan (3 versions) | ok. Photo date: undated, between completion (late Feb 2010) and brochure (2011-03-24); WRL credits 2012 |
| sat2011 (reg. img-09) | Esri World Imagery Wayback release 10, z17, capture 2011-02-28 (sidecar), https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/10/{z}/{y}/{x}; native 1.18 m/px | `src/satellite_2014.png` (file name wrong, capture 2011) | swash line read at 11 points as ground control for the camera fit | +-6 m (eyeball on a 2x view) | position + scale of the camera fit; frame | ok; known name mismatch recorded |
| sat2026 (reg. img-10 to 14) | Esri World Imagery current layer, capture 2026-01-23, z16-19 | src/satellite_*.png | reef not visible | - | context only | ok |
| img2 (reg. img-08) | Raised Water Research, "Kovalam Outline", https://raisedwaterresearch.com/wp-content/uploads/2019/12/Kovalam-Outline.jpg (page https://raisedwaterresearch.com/spot/artificial-reef/asia/india/kovalam/) | 475x305 px | hand-drawn foam line, not traced | no scale | typology cross-check only | ok |
| wrl | Blacka, M.J., Shand, T.D., Carley, J.T. and Mariani, A. (2013). A Review of Artificial Reefs for Coastal Protection in NSW. UNSW Water Research Laboratory Technical Report 2012/08, June 2013 (the UNSWorks cover page prints "No. 1012/08", a typo). DOI https://doi.org/10.4225/53/58e1dc7368c7a; handle http://hdl.handle.net/1959.4/57524 | Table 4.2 printed p.66 (PDF p.78): Kovalam GCs 65 x 85 m, water depth 1.3-3.7 m, offshore 90 m, submergence 0.2-3.4 m; Table 4.3 printed p.68 (PDF p.80): tide ~1.0 m, T 11-15 s, H 1-2.5 m; Table 4.4 printed p.69 (PDF p.81): A$1.41 M, A$351/m3; p.70 (PDF p.82): "damage to this reef is now hampering its effectiveness (E. Rendle, pers. comm., 2013)" | values re-read in this audit | values are as published; datum not stated | cross-check only (dimensions), and ONE input to choosing H (see A3) | ok. fixed: sources.md credited "Carley et al."; corrected to the four authors |
| decade | Mead, S. and Borrero, J. (2011). Multi-Purpose Reefs - A Decade of Applications. Coasts & Ports 2011 (Australasian Coastal and Ocean Engineering / Port and Harbour conferences), ASR Ltd, Raglan, New Zealand (authors and affiliation read on p.1 of Lior's PDF). Persistent URL given earlier (https://search.informit.org/doi/10.3316/informit.715072832934166) NOT confirmed by search | s.3.1.7: "4,000 m3 Kovalam Reef completed late February 2010"; s.4.1.4: weekly photo monitoring from the lighthouse viewing platform; beach 10-15 m wider (monsoon), up to 30 m wider (non-monsoon), Fig 7 | re-read in this audit | as published (authors are the reef's designers: interested party) | volume; camera position; beach width | ok; URL = not confirmed |
| rendle | Rendle, E.J. (2016). The Environmental, Social and Economic Impacts of an Artificial Surf Reef - The UK Experience. PhD thesis, University of Plymouth (title page read; WebSearch: Plymouth research portal, supervisors M. Davidson, L. Rodwell) | reference list PDF p.279: "ASR Ltd., 2010a. Kovalam coastal protection." | only used to name a report we do not hold | - | lead for missing design plan | fixed: FEASIBILITY said "Rendle 2013 thesis"; the thesis is 2016; "pers. comm. 2013" is a separate item in WRL p.70 |
| card R1/R-ASR | ASR via Raised Water Research: ~4,800 m3 (3,000 initial), tubes ~30 m long | card | - | secondary | volume alternative | ok(card); conflict kept (4,000 vs 4,800 m3) |
| Gemini | crest 1.6 m, offshore 150 m, smooth crescent | - | not re-fetchable | - | none | ok: not used |

## 2. Statement-by-statement check (point 1)
| # | statement | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | Completed late Feb 2010 | Mead & Borrero 2011 s.3.1.7, s.4.1.4 | p.4-5 of PDF | state drawn | ok |
| 2 | Volume 4,000 m3 (card 4,800 m3; WRL rate implies 1.41 M / 351 = 4,017 m3) | Mead & Borrero; card; WRL Table 4.4 (recomputed 1,410,000 / 351 = 4,017) | - | volume inference | ok; UNRESOLVED conflict: 4,000 (Mead & Borrero), 4,800 (card/RWR), 4,300 m3 (Rendle 2016 thesis Table 2.1, printed p.41 / PDF p.41: Kovalum 2010, 4,300 m3 SFC, cost 1,640,321 in the table's first currency column; currency header not checked) and 4,017 derived. Four values for one reef; the shape uses none of them in geometry. Card not edited |
| 3 | 65 m long-shore, 85 m cross-shore ("for V-shape reefs refer to max. alongshore and cross-shore dimension") | WRL Table 4.2 | printed p.66 | dimension check | ok (re-read) |
| 4 | Water depth 1.3-3.7 m; submergence 0.2-3.4 m; 90 m offshore ("distance to the undisturbed shoreline prior construction") | WRL Table 4.2 | printed p.66 | FEASIBILITY b, d | ok as published; NOT locatable on the reef, no datum |
| 5 | Tide range ~1.0 m | WRL Table 4.3 | printed p.68 | FEASIBILITY e | ok |
| 6 | Camera at the lighthouse end looking NNW | Mead & Borrero s.4.1.4 (monitoring from the lighthouse viewing platform) + identification of the tombolo rock on sat2011 | METHOD 2 | camera fit starting point | ok; the fitted camera sits at the tombolo rock (8.38724 N 76.97608 E at H 34), not on the lighthouse platform: consistent only roughly (inference) |
| 7 | Horizon row 191 px; principal point (467, 360); zero roll | read on the photo | METHOD 3.2 | camera model | ok (reading), assumptions A2 |
| 8 | Fit: one basin H = 34 m, f = 1,045 px, rms 2.2 px; rms 2.2-2.8 px for H 30-80 m; footprint 546 m2 (H 30) to 1,681 m2 (H 80) | rectify_result.json H_sweep (re-read here: H30 546 m2 rms 2.39; H35 640 m2 rms 2.22; H80 1,681 per HANDOFF) | - | scale uncertainty | ok(script) |
| 9 | Default H = 60 m: area 1,216 m2 (59 x 41 m) | rectify_result.json `selected`; shoelace of shape.json polygon gives 1,217.2 | - | default outline | ok; mismatch of 1 m2 (canonical.area_m2 1,217 vs outline_versions 1,216): rounding, no action. Choice of H = 60 uses WRL's 90 m (circular), stated in shape.json |
| 10 | H35 version: bbox 43 x 24 m (shape.json) vs sweep along 38 / cross 29 m (rectify_result.json, H = 35) | - | - | version list | mismatch (open): the two files give different extents for the same version; areas agree (640 / 641.5). Not changed; for main / next agent to check how bbox is defined (HANDOFF repeats 43 x 24) |
| 11 | Strips about 38 deg (+-15) to the swash line; swash bearing 196 deg | rectify_fit.py | - | description | ok(script) |
| 12 | Position +-20 m (swash points +-6 m, season 10-30 m) | VERIFY sensitivity; Mead & Borrero s.4.1.4 | - | uncertainty | ok |
| 13 | Reef later deflated and sank | card (RWR); WRL p.70 (E. Rendle pers. comm. 2013) | - | note only, not drawn | ok |
| 14 | 2005 Kerala Tourism proposal (500 x ~200 m, Eve's Beach) never built | card R5 | - | rejected alternative | ok(card) |
| 15 | sources.md `wrl` credit "Carley et al." | WRL cover | - | - | fixed (above) |
| 16 | "Rendle 2013 thesis" | Rendle thesis title page 2016 | - | - | fixed in FEASIBILITY/METHOD |
| 17 | shape.json references: Mead & Borrero URL (informit) | - | - | - | not confirmed; marked in shape.json |

## 3. Methods (point 3)
Single-view camera fit (`rectify_fit.py`, ~4 min run): pinhole, zero roll, principal point at the photo centre, horizon row gives pitch for any focal length f (tan pitch = (360-191)/f); 250 random starts over camera position, height 25-120 m, azimuth, f; cost = nearest distance in pixels from 14 photo swash points to the satellite swash curve (11 points) projected through the camera. Each traced vertex is intersected with the sea plane z = 0 (t = H / -ray_z). Local metres about 8.3885 N 76.9745 E (111,320 cos(lat) and 110,574 m/deg); canonical frame by explicit rotation (geom.py make-canonical not used because of a known rotation bug). The photo does not fix H (rms flat); H is chosen by argument (A3). No AI tool; Gemini compared only.

## 4. Assumptions (point 4)
| id | assumption | why | effect | replaced by |
|---|---|---|---|---|
| A1 | The sea surface is a plane at z = 0 and the strips lie on it | submerged reef, small relief | strips higher than 0 would lie nearer the camera: scale error of a few % | survey |
| A2 | Pinhole camera, zero roll, principal point at the photo centre, no lens distortion | photo has no EXIF/calibration | +-6 px horizon = area 1,177-1,251 m2 | calibrated photo |
| A3 | Camera height H = 60 m (default); 35 and 80 m kept as alternates | the photo cannot fix H (rms 2.2-2.8 px for 30-80 m); 60 m gives a normal 72 deg wide-angle lens and reproduces WRL's 90 m offshore. Circular: WRL's 90 m was used to choose H, so the agreement is not independent | area 640-1,681 m2 (x2.6) | vertical image, or a plan |
| A4 | The 2011-02-28 swash line represents the beach at the time of the photo (2010-11) | different dates; beach moves 10-30 m with season | position +-20 m | satellite from the photo date |
| A5 | The traced outline (strips + whitewater patch) is the reef; faint streaks right of the whitewater and the haze-covered tip are excluded or guessed | visibility | the real footprint is probably larger (4,000 m3 over 1,216 m2 = 3.3 m mean height; WRL 85 m cross-shore vs 41 m) | plan |
| A6 | The aerial shows the intact reef (before the deflation reported later) | photo before 2011-03 | none for that date | - |
| A7 | Swash line read by eye on a 2x view (+-10 view px = +-6 m) | resolution 1.18 m/px | +-6 m position | z19 tiles |

## 5. Decisions (point 5)
| id | decision | options | who / when | reason |
|---|---|---|---|---|
| D1 | Trace the ASR aerial (not satellite) | satellite / aerial | agent 2026-10-10 | reef not resolved from above |
| D2 | Camera-fit rectification instead of a guessed scale | eyeball / fit | agent 2026-10-10 | traceable method |
| D3 | Default H = 60 m, plus H35 and H80 as toggles | single outline / three | agent 2026-10-10 | scale undetermined |
| D4 | Earlier crescent draft (2026-09) rejected | - | agent | outlined the dark patch, not the strips |
| D5 | Shape HIDDEN on the page; 3D not built | draw with three outlines / hide | Lior 2026-10-10 (rule), applied through footprint.json display:false | scale unknown (area 546-1,681 m2) |
| D6 | Gemini not used | - | agent | unfetchable |

## 6. Confidence (point 6)
Plan: LOW (one oblique photo, scale free). Position: LOW-MEDIUM (+-20 m). Crest: NONE (0.2-3.4 m submergence is an unlocated range, no datum). Seabed: NONE (one range 1.3-3.7 m, no profile). Tides: LOW (range ~1.0 m, no levels). Volume: MEDIUM-LOW (4,000 vs 4,800 m3). Overall LOW; hidden.

## 7. Consistency (point 7)
Areas, scale, dates agree across shape.json, METHOD, VERIFY, HANDOFF. Mismatches: 9 (1 m2 rounding), 10 (H35 extent), 2 (4,000 vs 4,800 m3, card), 15-17 (fixed / flagged). Registry img-09 file name 2014 vs capture 2011 (known).

## 8. Counts
Statements checked 17; ok 12; fixed 3; mismatch 2 open (10, volume 2) + 1 rounding; missing 1 (confirmed URL/DOI of Mead & Borrero 2011); assumptions 7; decisions 6.

## 9. Image registry check (03_images/reefs/kovalam-reef-india/)
16 rows checked by script: every row has citation, image_url, source_page, page_or_figure, image_date, credit, license, retrieved, shows, how_used and file; every file exists on disk. Licences are "not cleared" private copies as recorded. IMAGES.md not rewritten.

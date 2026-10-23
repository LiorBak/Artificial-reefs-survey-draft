# SOURCE AUDIT 2026-10-10 - burkitts-reef-bargara (Burkitts Reef, "Greg's Reef", Bargara, Queensland)

Files audited: shape.json, FEASIBILITY.md, METHOD.md, VERIFY.md, sources.md, HANDOFF.md, registry `03_images/reefs/burkitts-reef-bargara/images.json`. No 3D (point 8 n/a). No model value changed.
Page status (Lior, 2026-10-10: shapes we do not know are not shown): HIDDEN. Mechanism: `07_scale/reefs/burkitts-reef-bargara.footprint.json` has `display:false` with a reason (not edited here, outside this folder). Reason, checks and assumptions are now written in FEASIBILITY.md and shape.json (`page_status`).
Status key: ok / ok(card) = from the reef card, not re-fetched / fixed / mismatch / missing.

## 1. Sources and how each was used (point 2)
| id | full citation | location | what was read, how | accuracy | feeds | status |
|---|---|---|---|---|---|---|
| img1 (reg. img-08) | Esri, Maxar, Earthstar Geographics and the GIS User Community. World Imagery (current layer), https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer, centre -24.8153, 152.4671, r 270 m, z19; capture 2025-09-05; retrieved 2026-10-04 | `src/burkitts_esri_2025-09-05_z19.png` + `.geo.json` (1992x1992 px, bounds N -24.812875 S -24.817725 E 152.469772 W 152.464429) | 38-vertex outline of the visible basalt platform read by eye on two zoom crops with a 50 px grid; pixels to lat/lon linear in longitude and in Web-Mercator y between the sidecar bounds; to UTM 56S (EPSG:32756, pyproj) | seaward edge within ~10 m of the breaker line; landward edge +-5 m; waterline edge could move tens of metres with tide (state unknown) | the only outline (platform, NOT the reef) | ok. Scale recomputed: 156543.03 x cos(24.815 deg) / 2^19 = 0.2710 m/px (matches sidecar). Area recomputed by shoelace from shape.json: 31,484.4 m2 (stated 31,484.8) |
| img2 (reg. img-01) | Redgard, G. (7 Sept 1980, as dated on the sheet; day/month order assumed Australian). Petition for Rock Removal (hand sketch). "Supplied: Greg Redgard", in ABC News, 2024-01-28, article photo 1, https://live-production.wcms.abc-cdn.net.au/a450bbac522bee4892941b966b64fea8 | registry img-01 | looked at by eye: boulder mass at the point, linear rock rows at the beach side | no scale, no north | context, qualitative match only | ok |
| card R1 | Howells, S. and O'Neal, D. (2024-01-28). How a sugarcane cutter and his mates created a world-first DIY surf break at Burkitts Reef, Bargara. ABC News. https://www.abc.net.au/news/2024-01-28/diy-surf-break-built-by-mates-at-burkitts-reef-bargara/103387450 | - | works Feb 1997 (approval), excavator, who | text | context, dates | ok(card) |
| card R3 | Coastal Management / ICM (Angus Jackson), "Building Artificial Surf Reefs: Worldwide Lessons & Applications", https://www.coastalmanagement.com.au/artificial-surf-reefs, 2026, accessed 2026-09-24 | - | ~300 m3, basalt boulders, excavator at low tide | text | volume (not used in geometry) | ok(card) |
| card R4 | Raised Water Research, Burkitts Reef spot page, https://raisedwaterresearch.com/spot/artificial-reef/australia/queensland/burkitts-reef/, accessed 2026-09-24 | - | ~12 boulders, ~300 m3, ~AUD 10,000, "~2.5 m tide swing" | text; tide figure has no datum, no stated gauge | context | ok(card); WEAK for tides |
| card R10 | DivePlanit (2026). From macro to megafauna: shore diving the Bundaberg coast. https://www.diveplanit.com/diving/dive-bundaberg/ | - | dive site depth to ~9 m | site-wide maximum, location on the headland unknown | context only | mismatch, see item 9 |
| P-Rendle | Rendle, E.J. (2016). The Environmental, Social and Economic Impacts of an Artificial Surf Reef - The UK Experience. PhD thesis, University of Plymouth, Table 2.1 (PDF p.41): "Bargara 1997, Harvey Bay [sic], QLD, Australia, 300 m3, Rock, AUS$ 10,000" | Lior's PDF in papers/, read in this audit | corroborates ~300 m3 and AUD 10,000 in an academic table (probably itself derived from the same web lineage; independence not established) | as published | context only | ok (new; added to shape.json references) |
| Gemini | 80 x 40 m prose; 4 references = 1 dead ABC URL + 3 homepages (2026-09-25 pass) | - | compared | - | none | ok: not used, not re-fetched |
| earlier footprint | 07_scale/reefs/burkitts-reef-bargara.footprint.json, 120 x 46 m, 2,480 m2 from Google Maps 2026-09-25, no image saved | - | - | not reproducible | none | ok: rejected, kept as a note |

## 2. Statement-by-statement check (point 1)
| # | statement | source | location | how used | status |
|---|---|---|---|---|---|
| 1 | Greg Redgard moved ~300 m3 / ~12 boulders in Feb 1997 with an excavator | card R1, R3, R4 | card Dimensions row | context | ok(card). Card also records conflicting accounts of the duration (2 days vs "within weeks") and of the first application (1982, forum/database sources only) |
| 2 | Cost ~AUD 10,000 | card R1, R4, R8 (Swellnet comment 540429) | card Cost row | context | ok(card) |
| 3 | Tide swing ~2.5 m | card R4 only (RWR) | - | FEASIBILITY e. | ok(card), single weak source, no datum. A primary source exists but was not retrieved: Maritime Safety Queensland tidal planes for Burnett Heads (the nearest standard port) https://www.msq.qld.gov.au/_/media/tmronline/msqinternet/msqfiles/home/tides/tidal-planes/2026-semidiurnal-tidal-planes.pdf (URL from WebSearch 2026-10-10; Burnett Heads row not read). Added to REQUESTS_FOR_LIOR |
| 4 | Platform outline area 31,485 m2; bbox 321 E-W x 377 N-S m; perimeter 1,133 m; centroid -24.81574, 152.46750 | scripts/computed_v1.json; shoelace recomputed here | - | plan | ok (area), bbox/perimeter ok(script) |
| 5 | Area three ways 31,646 (pixel) / 31,485 (UTM) / 31,508 (geodesic) | VERIFY 4 | - | consistency | ok |
| 6 | Reef at about -24.8157, 152.4675; card lat/lon (24.8205, 152.4625) is Bargara town centre | card R11 (Wikipedia "Bargara, Queensland": 24 49 14 S 152 27 45 E); our trace | HANDOFF 3 | location | ok. mismatch for the card owner: card JSON stores lat as +24.8205 (north) although Bargara is at 24.8 deg SOUTH; and the point is the town, not the reef. Card not edited |
| 7 | Edge trends: east flank 160/340 deg; north-facing edge 107 deg | scripts/compute_shape.py | - | description only | ok(script) |
| 8 | Distance offshore 0 m | card R1, R2, R10 (headland attached to the beach) | - | frame | ok(card) |
| 9 | "Dive depth to ~9 m" is a depth at this reef | card R10 and card Ecology line say the dive site is "the same headland reef"; registry img-06/07 were REJECTED on 2026-09-25 because that dive video is at a marine-park reef that "shares the name" and is "not the rock-reshaped Bargara surf break" | card vs registry | FEASIBILITY d. | mismatch (open): the card and the registry disagree on whether the dive site is the surf platform. The 9 m figure is therefore NOT used as the platform's seabed (FEASIBILITY already says site-wide maximum, now also "may be a different site"). Card not edited; for main/card owner |
| 10 | "No later alteration reported since 1997" | absence of evidence in the card | design_version | state drawn | ok as an ASSUMPTION (A5); labelled |
| 11 | 1980 sketch date 7/9/1980 = 7 Sept | registry img-01 note: day/month order assumed Australian | - | context | ok, assumption A8 |
| 12 | sources.md says "Text sources behind numbers: card R1, R3/R4, R10"; shape.json references list only R1, R4, Esri | - | - | - | fixed: R3 and R10 added to shape.json references |
| 13 | Retrieval dates: Esri 2026-10-04 (sidecar `retrieved`), ABC sketch 2026-10-06 | sidecar, registry | - | - | ok |

## 3. Methods (point 3)
Pixel to geographic: linear in longitude, linear in Web-Mercator y between the sidecar bounds (`scripts/compute_shape.py`); then pyproj to UTM 56S for area and metres. Frame: north-up metres, origin = polygon centroid, +x east, +y north (no shoreline frame because the platform wraps a curved headland). Vertices read by eye; no smoothing, no interpolation of heights, no AI estimate used.

## 4. Assumptions (point 4)
| id | assumption | why | effect | replaced by |
|---|---|---|---|---|
| A1 | The visible rock platform is the stage the reef sits on; the reef (reshaped boulder sub-zone) lies somewhere inside it | no source locates it | the outline is NOT the reef; reef area is unknown (300 m3 of boulders over 31,500 m2 shows it is a small part) | local account (Redgard, Bargara Boardriders), 1990s before/after aerials |
| A2 | The platform edge at image time is the outer edge of dark rock on the breaker line | breaking water marks the edge | tide state unknown: edge could move tens of metres | dated low-tide imagery + Burnett Heads tide at capture time |
| A3 | Landward edge = rock/vegetation or rock/sand boundary judged by eye | visible on image | +-5 m | LiDAR |
| A4 | North-up frame | curved headland | none (presentation) | - |
| A5 | No change to the platform since 1997 | none found in the card | unknown | 1997-98 and 2025 aerial comparison |
| A6 | Distance offshore = 0 (headland attached) | card R1/R2/R10 | none | - |
| A7 | Tide swing 2.5 m is typical; datum unknown | single RWR statement | none used in geometry | MSQ tidal planes Burnett Heads |
| A8 | Sketch date 7/9/1980 read day/month | Australian format | context only | the original |

## 5. Decisions (point 5)
| id | decision | options | who / when | reason |
|---|---|---|---|---|
| D1 | Trace the whole visible platform, not a sub-zone | platform / earlier 120 x 46 m estimate | agent, 2026-10-10 | the estimate cannot be reproduced; no source locates the sub-zone |
| D2 | One outline version, photo trace, default by necessity | - | agent, 2026-10-10 | no survey or design drawing exists |
| D3 | North-up frame | shoreline-aligned | agent | A4 |
| D4 | Polygon cut by the image frame at the south, kept | extend with a larger frame (needs network) | agent | area and bbox are minimums |
| D5 | Shape HIDDEN on the page; 3D not built | draw platform with a caveat / hide | Lior, 2026-10-10 (rule: shapes we do not know are not shown); applied via footprint.json display:false | the drawing would show the platform, not the reef |
| D6 | Gemini and the dive depth not used | - | agent | unverifiable; location mismatch (item 9) |

## 6. Confidence (point 6)
Platform outline: LOW (one image, truncated, tide-dependent edge). Reef zone: NONE. Crest: NONE. Seabed: NONE. Tides: LOW (one undated, datum-less figure). Volume: LOW (~300 m3 from news/spot sites, not a survey). Overall: LOW; page: hidden.

## 7. Consistency (point 7)
Areas, scale, dates agree across shape.json, METHOD, VERIFY, HANDOFF (items 4, 5, 13). Mismatches: 6 (card lat sign), 9 (dive-site identity), 12 (fixed). Status "verified" in shape.json is the same agent's self-check (VERIFY.md says so): the page rule hides it regardless.

## 8. Counts
Statements checked 13; ok 9; fixed 1; mismatch 2 (+1 fixed); missing 1 (primary tide levels); assumptions 8; decisions 6.

## 9. Image registry check (03_images/reefs/burkitts-reef-bargara/)
8 rows checked by script: every row has citation, image_url, source_page, page_or_figure, image_date, credit, license, retrieved, shows, how_used and file; every file exists on disk. Licences are "not cleared" private copies as recorded. IMAGES.md not rewritten.

## 10. Addendum - network pass 2026-10-10 (full access)
Supersedes: item 2 statement 3 (tide primary source "not retrieved"; now retrieved, R20) and the 'Network blocked' notes. Sources are fully cited in shape.json references R19-R22.
| # | statement | source | location | how used | status |
|---|---|---|---|---|---|
| N1 | Work areas marked on an oblique aerial: reprofile several surface rocks / remove to lengthen break (ellipse) / improve shore break / reprofile dangerous rocks | Jackson and Corbett (2007), Review of Existing Multi-Functional Artificial Reefs, Australasian Conference on Coasts and Ports 2007, p.1 Fig. 1 "Bargara Reef Phase 3 [Source: Greg Redgard]"; https://ref.coastalrestorationtrust.org.nz/site/assets/files/7954/2007_cp-review_mfar.pdf ; accessed 2026-10-10 (registry img-09; RWR copy img-10) | p.1 | georeferenced (METHOD 7); shape.json reef_zone | ok; LOW position |
| N2 | "additional works have been 'designed' [Figure 1]" (Redgard 2006) = Phase 3 is later than the initial works | J&C 2007 p.1 section 2.2 | - | label: Phase 3, not 1997 | ok |
| N3 | Site on the north side of a headland, effectively a half V; no modelling; no scientific monitoring; ~300 m3; ~A$10,000; Table 1 tide range 3.7 m, Hs <1 m | J&C 2007 pp.1-2, 6 (Table 1) | - | context, tide cross-check | ok |
| N4 | Boulders "relocated ... to gaps in the reef where the wave would break at higher tides"; two days (8 hours) in Feb 1997; Kobelco excavator; at least 12 boulders | RWR Burkitts Reef spot page, https://raisedwaterresearch.com/spot/artificial-reef/australia/queensland/burkitts-reef/ , accessed 2026-10-10 (card R4 re-verified) | Design and Construction | context | ok (re-fetched). Note ABC/Swellnet say 'within weeks' (2 days vs weeks: kept side by side) |
| N5 | Burnett Heads (standard port) MHWS 2.94, MHWN 2.35, MLWN 1.20, MLWS 0.61, MSL 1.78, HAT 3.68 m above LAT (epoch 2010-2029) | Maritime Safety Queensland (2026), Semidiurnal Tidal Planes 2026, PDF p.8, https://www.msq.qld.gov.au/_/media/tmronline/msqinternet/msqfiles/home/tides/tidal-planes/2026-semidiurnal-tidal-planes.pdf , accessed 2026-10-10 | p.8 | tide (port, not site) | ok (fixes audit item 3 'missing') |
| N6 | Spring range 2.33 m (MHWS-MLWS) and HAT-LAT 3.68 m match 'about 2.5 m' and '3.7 m' | computed from N5; J&C text / Table 1 | - | consistency | ok |
| N7 | Esri image dates: 2016-07-31 (release 23264), 2022-10-03, 2025-02-26, 2025-09-05; 2010-09-11 at z17 | Esri Wayback metadata layers (World_Imagery_Metadata_2017_r18 layer 5, 2023, 2025, 2014_r01 layer 6/7: SRC_DATE) | - | image dates | ok (release dates differ from capture dates; capture dates used) |
| N8 | Platform and zone are NoData in the BRC 2016 DEM; lowest valid 0.58 m; 3,841 of 9,025 grid points valid | Bundaberg Regional Council (2016) BRC DEM 1m, REST identify, https://mappingdata.bundaberg.qld.gov.au/arcgis/rest/services/BRC_2016_DEM_1m/MapServer | src/dem/*.json | context | ok; datum not stated (A13) |
| N9 | Dive site 'stretching along the headland in depths of two to eight metres' | Bundaberg Region (n.d.), Burkitts Reef Dive Site, https://www.bundabergregion.org/?p=5180 , accessed 2026-10-10 | page text | supports card R10 (same headland); resolves item 9 only partly: registry img-06/07 (video) remain rejected as a different place | ok(context) |
New assumptions A9-A13 and decisions D6-D8 (shape.json numbering; this audit file's own D5/D6 numbering differs, a pre-existing inconsistency: shape.json D5 = Gemini, audit D5 = hidden, D6 = Gemini) are in shape.json (assumptions / decisions) and METHOD section 7. Audit counts for this addendum: statements 9, ok 9, mismatch 0. Item 9 of the original audit (dive-site identity) is partially resolved by N9.

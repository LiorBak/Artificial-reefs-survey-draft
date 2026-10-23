# HANDOFF - kovalam-reef-india (shape trace + self-verification 2026-10-10, queue item 9; 3D NOT built - FEASIBILITY.md; for the page builder and any later agent)

HANDOFF_STOP: shape is at LOW confidence and needs network or Lior input to improve (section 7). Nothing else is pending in this folder.

## 1. Status per stage
| stage | status | confidence / reason |
|---|---|---|
| trace | done 2026-10-10 | LOW: one oblique, unscaled photo (ASR aerial); scale (camera height) not fixed by it |
| verify | done 2026-10-10 (self-check, VERIFY.md) | LOW confirmed: scale undetermined (area 546-1,681 m2); cross-shore size -52% vs WRL table at the default |
| 3D | NOT built (FEASIBILITY.md) | crest/seabed/tides are unlocated ranges without datum; plan scale estimated |
| image registry | done: img-07, -08, -09, -16 updated, overlays attached; planform pendings closed; img-03/-04 (underwater, reef height) still pending 3D check | check_registry.py passes for this reef |
| page | main to add: hold-list entry + shape text (section 8) | |

## 2. Key decisions and why
- Source of the plan = the ASR aerial (img-07, same photo uncropped as WRL Fig 4.5 = img-16): only image where strips are visible. Satellite never resolves the reef (submerged).
- Camera-fit rectification onto the 2011-02-28 Esri frame (swash line as ground control) instead of eyeballing a scale; fit cannot fix camera height H, so H is a stated assumption: default 60 m, alternates 35 and 80 m as toggleable versions.
- Default outline = photo trace (no survey, no design drawing exists in our files). Three versions share one frame.
- 3D withheld: brief rule needs plan + crest + seabed sourced.
- Draft crescent polygon of 2026-09 rejected (outlined the dark patch).

## 3. Key numbers (units, datum, source id)
### 3.1 Plan (canonical frame, metres; origin 8.387161 N, 76.975992 E on the 2011-02-28 swash line; x bearing 196 deg, y bearing 286 deg)
| version | area m2 | along x m | across y m | nearest edge offshore m | source |
|---|---|---|---|---|---|
| photo_trace_H60 (default) | 1,216 | 59 | 41 | 65 (mean 90, max 106) | img1 + sat2011, rectify_result.json |
| photo_trace_H35 | 640 | 43 | 24 | 58 | same |
| photo_trace_H80 | 1,681 | 64 | 68 | 92 | same |
Strips at about 38 deg (+-15) to the swash line. Camera (fitted, H60): 8.386659 N, 76.975706 E (at the tombolo rock). Position +-20 m.
### 3.2 Text values (secondary, WRL TR 2012/08 Table 4.2 p.66; datum not stated)
65 m long-shore, 85 m cross-shore (max dims), water depth 1.3-3.7 m, offshore 90 m (to pre-reef shoreline), submergence 0.2-3.4 m, no nourishment. Table 4.3 p.68: tide range about 1.0 m, T 11-15 s, H 1-2.5 m. Table 4.4: A$1.41 M (2013), A$351/m3 => ~4,017 m3.
### 3.3 Other
Volume 4,000 m3 (Mead & Borrero 2011 s.3.1.7) vs 4,800 m3 (card, ASR via RWR; 3,000 initial). Completed late Feb 2010. Beach 10-15 m wider in monsoon, up to 30 m in non-monsoon (Mead & Borrero 2011 s.4.1.4). Damage hampers the reef by 2013 (WRL p.70, Rendle pers. comm.).

## 4. File map (07_scale/shapes/kovalam-reef-india/)
- shape.json - spec file, status verified, confidence low, 3 outline versions, default photo_trace_H60 (viewers read outline_versions).
- METHOD.md (trace log, 5 sections), sources.md, VERIFY.md, FEASIBILITY.md (why no 3D), HANDOFF.md.
- rectify_fit.py (camera fit, sweeps, overlays; ~4 min) -> rectify_result.json; build_shape_json.py -> shape.json. pixel_polys_img1_v2.json = traced pixels.
- overlays/: img1_trace_v2.png, img1_camera_fit_check.png, sat2011_plan_reconstruction.png; _draft_2026-09/ = superseded draft (not worth opening).
- src/: img1_asr_aerial.png (primary), img2_rwr_outline.jpg, satellite_*.png (+.geo.json; satellite_2014.png is the 2011-02-28 capture, bulky satellite_current/point 5-10 MB: not needed), asr_brochure_wayback.pdf.
- pixel_polys_img1.json = old draft, ignore.

## 5. Open issues, discrepancies, pending checks
1. Scale: H unconstrained (section 3). Cross-shore 41 m vs WRL 85 m; volume 4,000 m3 over 1,216 m2 = 3.3 m mean height, so the real footprint is probably bigger than the traced strips (H80 or an extended tail).
2. Volume 4,000 vs 4,800 m3 (card) unresolved; card should say 4,000 per two sources (intake notes say main applies).
3. Date mismatch: swash line 2011-02 vs aerial (undated, 2010-11).
4. Registry img-09 file named satellite_2014 is a 2011-02-28 capture.
5. WRL "submergence 0.2-3.4 m" and "water depth 1.3-3.7 m" cannot be located on the reef (see FEASIBILITY.md).
6. Gemini sources (crest 1.6 m etc.) not re-fetchable here.

## 6. Next steps (in order)
1. With network: do the fetches of section 7 (no code changes needed except reading the reef in a vertical image).
2. If a vertical image shows the strips: trace there, georeference, make it the default outline (measured > photo trace), keep the three photo versions as alternates, set confidence medium.
3. Then 3D per _agent_briefs/model_3d.md using the Borth pipeline; needs seabed (Navionics) and a tide table.
4. Lior: see REQUESTS_FOR_LIOR.md lines.

## 7. NEEDS NETWORK (exact items and why)
| URL / tile | why |
|---|---|
| Esri Wayback releases 2010-2014 for the Kovalam bay, z19 (0.3 m/px): tile template https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/{release}/19/{y}/{x}, tiles covering lat 8.3862-8.3880, lon 76.9745-76.9768 (west of the tombolo rock); try releases 10 (2011-02-28) and the nearest of 2012-2013 | the strips may show as olive streaks from above; a vertical image would fix the scale |
| Google Earth Pro historical imagery (Lior) | same, Feb 2010-2012 |
| https://webapp.navionics.com/ (redirects to https://maps.garmin.com/en-US/marine/) at 8.3867 N, 76.9757 E, z18 | seabed profile 0-250 m off the rock, datum (input d) |
| https://www.surfer.com/features/india%E2%80%99s-first-artificial-reef%E2%80%A6works/ (Wayback), https://surfingindia.net/random-stuff/artificial-reef-kovalam/ , Vimeo 11274816 | contemporaneous 2010 photos/video of the reef, maybe a vertical view or a scale |
| ASR 2010a "Kovalam coastal protection" report / CESS morphological assessment (papers) | design plan, crest level, container size |
| Esri tile re-fetch of img-09 area at z18/z19 for the 2011-02-28 capture | finer swash line (reduces +-6 m) |

## 8. For main: page texts (per 04_build/UPDATE_PROTOCOL.md, new-model section)
- No 3D yet: add `kovalam-reef-india` to `04_build/data/models3d_hold.json` ("Not yet modelled"). Do NOT add to models3d_combined/curated/caveats (no model.js).
- Shapes tab text: "Traced from one oblique ASR photo (Feb 2010 - Mar 2011) and placed on the 2011-02-28 satellite frame through a fitted camera. LOW confidence: the photo cannot fix the scale, so three outlines (camera 35 / 60 / 80 m) are shown; default 60 m, area 1,216 m2, 59 x 41 m. Later deflation and sinking of the reef are not drawn."
- (i) text = versions_info in shape.json. Reason for confidence = confidence.reason.
- Gallery: registry rows updated (img-07, -08, -09, -16; overlays as annotated versions).

## 9. CHECKPOINT 2026-10-10
Everything above is final for this run. If resumed: do section 6 step 1 when the network allows; no half-finished work.

## Source audit 2026-10-10
SOURCE_AUDIT_2026-10-10.md in this folder holds the sources-with-how-used, statement check, assumptions (A#), decisions (D#), confidence and consistency tables. FEASIBILITY.md / shape.json now carry the why / checked / assumed text (page_status for hidden reefs). Open mismatches are listed in the audit section 2. If kovalam build_shape_json.py is re-run it overwrites the audit additions in shape.json: re-apply from the audit.

## 10. NETWORK PASS 2026-10-10 (fresh agent) - result: nothing better found
Done from section 7: Esri Wayback (no releases 2010-2013; z19 blank before 2022, z17 1.19 m/px shows no strips 2011-2020), surfingindia.net + Vimeo page (text/video only), RWR gallery (3 new surf photos, img-17 to -19), ASR/CESS report searches (no open copy), Wayback web and ASR site unreachable (proxy), surfer.com 403, Navionics not readable (no Chrome here). New registry rows img-17 to -20 (img-20 = z17 sheet in src/wayback_z17_2011_to_2020_sheet.png). Shape unchanged: LOW, hidden, no 3D. Details METHOD.md section 6, FEASIBILITY.md.
Still needs Lior (or a session with Chrome): Navionics readings, Google Earth Pro historical imagery Feb 2010-2012, ASR 2010a / CESS report, Vizhinjam tide table; or a retry of web.archive.org / surfer.com from a PC.
HANDOFF_STOP: nothing else can be done in this folder without those inputs.

## 11. CHECKPOINT 2026-10-13 (agent: W1/W2 SeaDataNet + Kovalam, resumed after the interruption)
Done:
- Card `02_research/reefs/kovalam-reef-india.json/.md` (CRLF kept): added Rendle (2016) thesis Table 2.1 (PDF p.41 = printed p.41, checked in papers/ 2026-10-13: "Kovalum 2010, Kerala, India, 4,300, SFC, 1,640,321 ...") as reference R15 and in the volume disagreement (3,000 / 4,000 / 4,300 / 4,800), the gaps list, and the bounding-box mismatch note (shape.json H35 bbox 43 x 24 m = axis-aligned extent of the polygon in the canonical swash frame, recomputed from the vertices: 42.7 x 24.1 m; rectify_result.json H_sweep H = 35 gives along 38 x cross 29 m, np.ptp of the sweep script's own frame, rectify_fit.py line 64; same shape, areas 640 / 641.5 m2; the frame of the sweep script not checked). Nothing in shape.json or the page data was changed.
- web.archive.org works now, but only through `https://web.archive.org/web/2/<url>` (redirects to the 2017-05-20 snapshot of the surfer.com article); the article has no plan, dimensions or crest level; its lead photo is not archived (404). The ASR brochure is already held (`src/asr_brochure_wayback.pdf`, no plan). Archived asrltd.com pages: none usable (parked domain, 404, CDX resets). Three dead ends added to `02_research/dead_ends/kovalam-reef-india.json`.
- Navionics: webapp.navionics.com redirects to https://maps.garmin.com/en-US/marine; with `?maps=another-brand&overlay=false&key=<12-character geohash of lat/lon>` (format used on Lior's PC for Borth, 2026-10-05) the cloud headless Chrome draws NO map (empty grey area, default location box). Geohash of 8.3867 N 76.9757 E = t9qxxwgbpf4n. No depth read; dead end logged.
Verdict: Kovalam stays hidden (no real plan source). Recommendation for main: none beyond the card text.
Next (exact): (1) Navionics reading needs Lior's PC (his normal Chrome, URL `https://maps.garmin.com/en-US/marine?maps=another-brand&overlay=false&key=t9qxxwgbpf4n`; it drew maps on the PC) or Google Earth Pro history (REQUESTS section 5, Kovalam rows). (2) If main shows a Kovalam location block: use the geohash URL above as the Navionics link (works only in a normal browser). (3) Optional: check which axes rectify_fit.py uses for along_m/cross_m and put the answer in SOURCE_AUDIT row 10.

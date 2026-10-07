# VERIFY - borth-coastal-defence-reef

Run started 2026-10-06 (adversarial verification + fix + 3D-input preparation; verifier session).

Starting state found: shape.json status "traced", confidence.level "high" with reason "(provisional - to be finalised)", design_version.why_this_one "(provisional)",
dimensions_check [], gemini {}, references [] -> the earlier tracing run stopped at a checkpoint (METHOD.md step 3b); web research / design-version / Gemini steps were never completed.

## Check 1 - overlays viewed and re-rendered (2026-10-06)
- shape.json pixel_polygons for sat2024 / sat2022 / sat2012 are identical to polys_v1.json / polys_2022_v1.json / polys_2012_v1.json (checked in code). Re-rendered all three with overlay.py render (alpha 0.15, numbered vertices) and viewed them, then zoomed (3x) on the N-mound head, N-mound tail and the S mound of sat2024.
- sat2024 (primary): outline follows the outer edge of the bare light-grey rock where it meets the dark wet/shadow halo, on both mounds; offsets 3-5 px (0.5-1 m) at loose-rock fringes; on the E side of the S mound and the S side of the N-mound tail the line includes the dark wet band (about 1 m), so the 2024 trace is the generous one. Verdict GOOD.
- sat2022: tight trace on the bare rock (swell foam W side left out); fits. Area 15.6 % smaller than sat2024 only because of that tighter edge rule. IoU 2024 vs 2022 = 0.84, Hausdorff 5.5 m (N) / 2.8 m (S), centroid shifts 0.8 m E / 0.6 m S (N mound), 0.4 m / 0.3 m (S mound). GOOD.
- sat2012: soft algal outline, fits within ~5 px except the diffuse NW halo (not included). The 2012 polygons sit 6.2 m E (N mound) and 4.8 m E (S mound) of the 2024 ones; translating the 2012 trace by 5.1 m W and 1.5 m N gives IoU 0.94 with 2024 -> same two mounds, whole-frame imagery registration offset, not reef movement (agrees with METHOD.md step 2b). APPROXIMATE only because of the algal soft edge.
- overlays\zoom1..zoom10 (earlier session): these are grid-labelled zoom crops of the source frames, not outline overlays (no polygon is drawn on them); pixel labels refer to the 2750-px 'blobs' frame / the shoreline frame. They are scratch aids; kept and registered as derived crops. The verified outline overlays are the new overlays\verify_*.png (see Check 1 files at the end).
- overlay_match: GOOD (sat2024, sat2022), APPROXIMATE (sat2012 soft algal edge).

## Check 3 - scale, area, bbox, canonical frame (2026-10-06)
- px_per_m re-derived from the sidecar bounds with my own Web-Mercator code: 1540 px span -> 0.18183 m/px (x cos lat) in both axes (ground lat-span and lon-span agree) -> 5.4995 px/m; shape.json says 5.4995, 1 %. OK. Same for the 3850-px shoreline frame.
- METHOD.md states geom.py make-canonical / px_to_m was NOT used (the tracer found the rotation-sign bug itself and computed the frame with numpy/shapely). I did not trust that statement: I recomputed the whole canonical block from the raw pixel polygons with an independent script (pixel -> Web-Mercator -> local metres, total-least-squares line through the five defence-line points read on the shoreline frame, foot of the perpendicular from the both-mound centroid as origin): max difference to the stored polygons_m = 0.005 m on all 79 vertices; area 5742.7 m2 (N 3944.4, S 1798.3), bbox 195.5 x 140.0 m (x -121.26..74.20, y 256.98..396.96), centroid 330.5 m offshore, max dimension 203.4 m, defence-line bearing 359.568 deg (residuals 0.06-0.26 m). All equal the stored values.
- Hand check of one vertex: sat2024 N-mound vertex 0 at pixel (402,525) -> canonical (16.90, 396.96); S-mound vertex 10 at (875,1107) -> (-89.57, 311.76); both equal the stored numbers.
- Fixed geom.py: `python geom.py selftest` = 334 checks, 0 failed. Running the FIXED make_canonical on a scratch copy with alongshore_dir_px = the SOUTH direction reproduces the stored polygons with x -> -x to 1.4 cm (max diff), area 5742.7 m2, bbox 195.46 x 139.98 m.
- FOUND (frame handedness): the stored frame is +x = NORTH (bearing 359.57), +y = WEST (269.57), i.e. +y is +x turned 90 deg COUNTER-clockwise. geom.py (docstring, selftest) and every other shape.json (Boscombe 83.4/173.4, Palm Beach 334.3/64.3, Mount Maunganui 316.15/46.15, Pratte's 155/245) define +y = +x turned 90 deg CLOCKWISE, which makes the drawing with x right / y down a true, non-mirrored plan view. With +x = north the Borth drawing would be a MIRROR IMAGE of the satellite plan (the hook would curve the wrong way). The metres are right; the handedness is not. Fix applied: canonical re-expressed with +x = SOUTH (bearing 179.57 deg), +y = WEST (269.57 deg) = x_old -> -x_old; every other number (area, bbox sizes, y range, distance offshore, angles to the shoreline) unchanged; x range becomes -74.2..+121.3. A fixed-tool run (above) confirms it.

## Findings log (written early, 2026-10-06; sections below are completed afterwards)
Scratch work lives in the session scratchpad (borth_verify\ ... dl\ plans\). Primary sources found this run (all fetched and read by me):
- HR Wallingford HRPP576 (Rigden, Stewart, Allsop, Johnson; ICE Coasts, Marine Structures and Breakwaters, Edinburgh, Sept 2013), https://eprints.hrwallingford.com/931/1/HRPP576_SurfReefs.pdf : original design = two surfable reefs A (north) + B (south); FINAL design = single surfable northern reef A (extended, rock, small hook on the near side) + shore-parallel breakwater C (the oval) replacing B. Fig 2 gives mODN seabed contours (0 to -5 mODN) round the structures; Fig 3 = initial geotube northern reef 180 m x 65 m, 4.0 m high, crest ~MSL. Water levels in mODN (surf tests 0.86-2.36 mOD).
- Royal Haskoning drawings, Borth Coastal Protection Scheme Phase 1, 'FOR CONSTRUCTION', rev C1 (Jan 2011), job 9V5090 (http://www.borthcommunity.info/index.php/planning-drawings/65-planning-drawings): 1001 general arrangement 1:2000 (Northern Reef + Southern Reef = 'Multi-Purpose Reef'), 1020 reef plan 1:500 with setting-out points R1-R15 in OS National Grid, 1021/1022 northern reef sections, 1023 southern reef sections. All levels m ODN; drawn design tide levels MHWS +2.56 mODN, MLWS -1.74 mODN; N reef crest +0.50 (arm), +1.00 (tail), +0.00 at the head edge, side slopes 1:3 / 1:4 / 1:5; S reef crest +1.50, slopes 1:3, 'existing seabed varies -4.2 to -3.6 m AOD'.
- Welsh Government LiDAR 2020-22 DSM/DTM tile SN6089, flown 2022-03-19 03:15-03:20 UTC at about LAT (water edge -2.2..-2.4 mODN): both mounds are exposed and measured (read values only, 2 files of ~1 MB each, kept in scratch, not in the project).
- NTSLF 'Chart datum and ordnance datum' table (https://ntslf.org/tides/datum): Barmouth -2.44 m, Fishguard -2.44 m; Aberystwyth is not listed.

## CHECKPOINT 2026-10-06 (complete enough for a fresh agent to finish)
DONE: checks 1 and 3 (above); research for checks 2, 4, 6 and the 3D inputs; numbers below are final unless marked TODO.
SCRATCH (session scratchpad, may be gone): borth_verify\ (recompute.py, sop.py, design1/2.py, compare3.py, lidar1-3.py, dl\ = downloaded PDFs/tiles).
KEY NUMBERS
- Design plan DRG 9V5090/1020 rev C1 (1:500, For Construction) is georeferenced by its 15 setting-out points R1-R15 (OSGB36 BNG): similarity fit residual <= 0.02 m, scale 5.669 pt/m = exactly 1:500. Vector rings read from the PDF: Northern Reef 5 concentric rings, areas 7894 / 7595 / 6814 / 6049 / 4963 m2 (outer = seabed edge of the 0.5 m Type 6 apron ... inner = foot of the Type 4 armour slope); Southern Reef rings 3610 / 3444 / 3010 / 2596 / 2036 m2 (inner 72 x 32 m). Design armour-foot rings vs our satellite trace (sat2024): S IoU 0.86, N IoU 0.79, centroid offsets 0.3-4 m (inside the +-5 m georeference / OSGB->WGS84 Helmert error). Trace area vs design armour foot: N 3944 vs 4963 (-20 %), S 1798 vs 2036 (-12 %); S length 71.8 vs 72 m.
- WG LiDAR SN6089 (flown 2022-03-19 03:15 UTC, water edge -2.2..-2.4 mODN): exposed footprint N 5865 m2, S 2816 m2 (150 x 86 m and 80 x 41 m bbox), crest (DSM p90) N arm +0.7, tail +1.0..+1.15, S oval +1.5 (max 2.13); mean flank slope 1:4-1:5 (H:V) between -1.5 and 0 mODN; width at -2.3 mODN N arm 34-37 m, head 50 m, S 38-41 m.
- Tide (m ODN): MHWS +2.56, MHWN +1.06, MLWN -0.64, MLWS -1.74 (West of Wales SMP2 Coastal Area C, Nov 2011, p. 4C.3, Aberystwyth row; the same MHWS/MLWS are printed on the Haskoning Borth drawings); LAT = chart datum = -2.44 mODN (NTSLF: Barmouth/Fishguard -2.44; consistent with MHWS 5.00 m CD); MSL ~ +0.31 mODN (mean of the 4 levels; = 2.75 m CD); MSL-LAT = 2.75 m (EMODnet note: the -2.25 web-summary value is NOT supported).
- Gemini (all values wrong or unsupported): see check 6 below (to be written).
TODO: write checks 2/4/5/6/7 text, '3D inputs' section, new overlays + registry rows + NEW_IMAGES_LOG, shape.json (status verified, flip frame to +x south, add design/LiDAR cross-check, dimensions_check, gemini, references, verification, confidence), METHOD.md corrections, 05_qa\00_STATUS.md, final JSON.

## Check 2 - design version, as-built, later works (2026-10-06)
- Drawn state: the FINAL BUILT layout of Phase 1 (completed March 2012; Coflein: 8 March 2012). Two separate rock mounds off the south end of Borth: the boot/hook-shaped 'Northern Reef' (the surfable multi-purpose reef) and the oval 'Southern Reef' (called the 'shore parallel breakwater C' in HRPP576). The page must say: "as-built layout, outline = visible rock edge at low water".
- Design history (HR Wallingford HRPP576, p. 3-4, Figs 2-3): original concept = two surfable geotube reefs, north A (truncated delta, 180 x 65 m, 4.0 m high) and south B; after the 1:45 physical model (cross waves between the reefs) the final design 'was changed to a single surfable reef and a shore parallel breakwater (SPB)'; the northern reef was extended and built in rock, 'a small hook was included on the near side'. The built boot shape with a hooked head is exactly this reef; the oval replaced B.
- Built = Royal Haskoning drawings 9V5090/1001, /1020-1023 rev C1 'For Construction' (Jan 2011). Plan 1020 georeferenced by its 15 OS-grid setting-out points (residual 0.02 m, scale exactly 1:500) and overlaid on the 2024 image: armour-foot IoU 0.79 (N) / 0.86 (S), centroid offsets 0.3-4 m (inside the +-5 m georeference and the 2-5 m OSGB36->WGS84 Helmert error). Figure: overlays/verify_design_lidar_vs_trace_sat2024.png (registry img-25).
- Unchanged since: imagery 2012-10-27, 2013-06-04, 2022-08-25, 2024-09-17 (all same two mounds; IoU 2024/2022 0.84; 2012 offset 5 m = imagery registration) and the Welsh Government LiDAR of 2022-03-19 (both mounds intact, crest levels within +0.2-0.3 m of design).
- Later works: Phase 2 (design 2012-13, target start autumn 2013 per the posters, weekly progress reports 2014 on borthcommunity.info; rock breakwaters/groynes/breastwork along the frontage north of the reef; Ceredigion monitoring report 2013 sec. 2.15; Phase 2 posters p. 1-3). The Borth-to-Ynyslas outline business case (AECOM, 2020) concerns the frontage north. A search for reef damage, repair, rock movement or removal (2026-10-06) found nothing. The 2013 report notes 'pockets of erosion around the offshore breakwaters, which may still be down to construction works' (beach, not the reef).
- Verdict: the drawing represents the as-built layout; no redesign, extension, damage or removal found. Not yet verified: any survey after 2022 (none public found).

## Check 4 - dimensions vs text (2026-10-06)
- Text sources give only the distance offshore (Coflein: 'The reef is 300m off the coast'; New Civil Engineer 2011: 'double reef located 400m offshore') and tonnage (275,000 t whole scheme; Coflein about 300,000 t). No text gives length, width, area or crest. So the comparison is against the Royal Haskoning plan (a primary design source).
- Offshore: drawing 330.5 m (both mounds' centroid from the defence line; edges 257-397 m) lies between 300 and 400 m: consistent; which line each source measures from is not stated.
- Against plan 1020 (armour foot ring): N length 144.9 vs 150.9 m (-4.0 %); N mean width 27.6 vs 32.9 m (-16 %); S length 71.8 vs 71.5 m (+0.4 %); S width 31.0 vs 31.5 m (-1.6 %); N area 3944 vs 4963 (-20 %); S area 1798 vs 2033 (-12 %); total 5743 vs 6989 m2 (-18 %); axis bearing 61.4-64.2 vs 60.5 deg; centroid separation 124.4 vs 123.2 m.
- Which is 'wrong'? Neither: the drawn polygon is the visible rock edge on imagery (waterline about -1 to -1.5 mODN, unrecorded), the design polygon is the foot of the Type 4 armour slope (about -2.2 mODN) and the LiDAR (sea near LAT, -2.3 mODN) shows the as-built mounds wider than the design (exposed 5861 + 2814 = 8675 m2). Flanks are 1:4-1:5 as built vs 1:3 designed. The drawn area is therefore the smallest of three legitimate footprint definitions; shape.json canonical.alt_outlines_m holds the other two.
- Gemini's 200 x 65 m / 12,500 m2 matches none of them (see check 6).

## Check 5 - provenance (2026-10-06)
- All sources have url, page/figure, date, credit, licence; the tracer's six Esri rows are complete (sidecars). The tracer's shape.json had no references, dimensions_check, gemini or design_version text: now filled (ref1-ref10). Every number in METHOD.md has a source or method. New sources saved (src/ and 03_images/reefs/borth-coastal-defence-reef/) and registered (img-17..25).

## Check 6 - Gemini findings (2026-10-06)
The tracer had left shape.json gemini = {}; I judged each source myself. Gemini record: 02_world_reefs_data/reef_footprints.json id 'borth' (read only).
| Gemini value | Verdict | Evidence |
|---|---|---|
| two-part 'double reef' | correct (topology) | New Civil Engineer 2011 'double reef'; drawings 1001/1020 |
| 200 m offshore | wrong | built 330 m; Coflein 300 m; NCE 400 m |
| 200 x 65 m, 12,500 m2 (units 120 x 45 and 180 x 65 m) | wrong | built: boot 145-151 m (outer toe 166.5 x 65.1 m) + oval 72 x 32 m; visible rock 5,743 m2, foot 6,989 m2; '180 x 65 m' is Fig 3 of HRPP576, the superseded initial geotube design |
| crest -1.5 m CD / -2.0 m; seabed -6.8 m; height 5.3 m | wrong | crests +0.50 / +1.00 / +1.50 mODN = +2.94 / +3.44 / +3.94 m above chart datum, seabed about -4.0 mODN (-1.6 m CD), height 4.5 m (N) / 5.1-5.7 m (S) |
| designer Halcrow (Jacobs) | wrong | Royal Haskoning (HaskoningDHV) + ASR; HR Wallingford modelling (drawings title block; HRPP576) |
| shoreline orientation 025 deg | wrong | frontage bearing 359.57 deg (fit through the shingle back, residual < 0.3 m) |
| 110,000 t / 45,000 m3 | unverifiable / contradicted | whole scheme 275,000 t (NCE), about 300,000 t (Coflein); no reef volume published |
| tidal range 4.8 m | partly | design mean spring range 4.30 m (MHWS +2.56, MLWS -1.74); 4.8 m = largest spring range |
| cited: Ceredigion 'Final Review 2013', BAM Nuttall 'case study 2012', Coflein 'Craig y Delyn Reef 2015' | not found / mis-cited | the Coflein record is 'Coastal Defences, Borth' (NPRN 424699, record 2020); the other two do not exist as far as searched |
| image provenance: 'authentic blueprint' (Phase 2 poster p. 3) | wrong use | no scale, generic icons; Gemini did not use the real drawings 9V5090 |
| photo credit 'Alan Fryer' (Geograph 2802002) | wrong credit | photographer is Jeremy Bolwell; photo shows beach works, not the reef |

## Check 7 - confidence (2026-10-06)
'high' kept. Rubric: structure clearly visible on geo-referenced imagery (four dates) - yes; dimensions within about 10 % of the text/design - yes for length (-4 % / +0.4 %), angle (1-3 deg), position (0.3-4 m) and the oval's width (-1.6 %); the area is 18 % below the design armour foot because the drawn edge is the visible rock edge. The previous reason '(provisional - to be finalised)' was replaced. If the page compares footprint areas across reefs it should use the right footprint level (see 3D inputs, footprint).

## 3D inputs (prepared for the 3D stage, 2026-10-06)
All levels metres. Datum codes: ODN = Ordnance Datum Newlyn (same as 'AOD'); CD = Admiralty chart datum = LAT; MSL = mean sea level (the 3D model zero). Offsets are derived in the tide block below. Source ids: see shape.json sources/references and the registry ids.

### Tide levels at Borth / Aberystwyth (m ODN)
| level | value | source | quote / figure | uncertainty |
|---|---|---|---|---|
| MHWS | +2.56 mODN (= 5.00 m CD) | West of Wales SMP2, Coastal Area C Introduction, p. 4C.3, Aberystwyth row (Royal HaskoningDHV, Nov 2011; ref3); also printed on Royal Haskoning drawings 9V5090/1021-1023 | table row 'Aberystwyth -1.74 -0.64 1.06 2.56' (MLWS, MLWN, MHWN, MHWS) | +-0.05 (0.1 rounding in the table) |
| MHWN | +1.06 mODN | same row | same | +-0.05 |
| MLWN | -0.64 mODN | same row (the drawings print only MHWS/MLWS) | same | +-0.05 |
| MLWS | -1.74 mODN (= 0.70 m CD) | same row; drawings 1021-1023 'MLWS -1.74' | same | +-0.05 |
| LAT = chart datum | -2.44 mODN | NTSLF 'Chart datum and ordnance datum' table (ref4): Barmouth -2.44 m, Fishguard -2.44 m (Aberystwyth NOT listed); consistent with MHWS 2.56 = 5.00 m CD at Aberystwyth (tide-forecast.com listing 5.0 / 0.7 m CD, secondary); the 2022-03-19 LiDAR sea surface at a spring low read -2.2..-2.4 mODN | NTSLF: 'Barmouth -2.44m'; 'Fishguard -2.44m' | +-0.05 m (neighbour ports + three consistent clues); NOT confirmed at UKHO / NTSLF for Aberystwyth itself |
| MSL | about +0.31 mODN | mean of MLWS, MLWN, MHWN, MHWS above (-1.74 -0.64 +1.06 +2.56)/4 = +0.31; equals 2.75 m CD - 2.44 | derived | +-0.15 m (4-level mean, no harmonic Z0 found) |
| MSL - LAT | 2.75 m | derived (0.31 + 2.44) | - | +-0.15 m; the 2.25 m web-search value in emodnet/REPORT.md is NOT supported |
| mean spring / neap range | 4.30 m / 1.70 m | MHWS-MLWS, MHWN-MLWN | derived | +-0.1 |
| extreme still water | 10 / 50 / 100 yr: +3.76 / +4.36 / +4.73 mAOD | SMP2 C p. 4C.3 (SMP1 values, Aberystwyth) | table | HAT itself not found at a primary source |
| test water levels | 0.86-2.36 mOD (surf tests); 1.81 mODN (morphology tests) | HRPP576 p. 5-7 | 'WL = 0.86-2.36mOD increasing in 0.5m increments' | - |
Conversions: z_MSL = z_ODN - 0.31; z_MSL = e_LAT - 2.75 where e_LAT is a height above LAT (EMODnet depth below LAT = -e_LAT); chart-datum height = z_ODN + 2.44.

### Crest level
| part | value | source | quote / figure | uncertainty |
|---|---|---|---|---|
| north (surf) reef, main arm | +0.50 mODN (+0.19 m MSL); flat crest 9 m wide (R5-R2 dimension 9000) | DRG 9V5090/1020 (img-20) and /1021 N1, N3, /1022 N4 (img-21, 22) | crest label '+0.50' on N3-N3, N4-N4; plan label '+0.50 CREST' | design nominal; LiDAR DSM median +0.69 / p90 +0.72..+0.88 (blocks stick up 0.2-0.3 m) |
| north reef, tail end (toward SOP R3-R4) | +1.00 mODN (+0.69 m MSL), 15 m transition from +0.50 starting at SOP R2 | DRG 1021 section N1-N1 (tail), plan '+1.00 CREST' | label '+1.00', 'TRANSITION APPROX. 15m' | LiDAR p90 +1.0..+1.15 |
| north reef, head (SW lens) | +0.00 mODN at the head edge (SOP R1, R10, R9..R6) rising to +0.50 over about 40 m; lens polygon R1-R10-R9-R8-R7-R6 (grey on the plan) | DRG 1021 N1 (left), 1022 N5/N6 | labels '+0.00', 'TRANSITION APPROX. 40m' | design; LiDAR p90 -0.1..+0.6 over the head bins (46-52 m wide) |
| south (oval) reef | +1.50 mODN (+1.19 m MSL), flat crest 6 m wide (3000 + 3000 about the centreline) and 38 m long between SOP R15 and R14 | DRG 1023 S1, S2 (img-23); plan 1020 | label '+1.50' | LiDAR p90 +1.44..+1.58 (max 2.13) |
| (initial, superseded) | crest at about MSL, height 4.0 m | HRPP576 Fig 3 | 'MSL' line at the crest, '4.0' | not the built reef |

### Reef height, side slopes, layers (rock)
| quantity | value | source | quote / figure | uncertainty |
|---|---|---|---|---|
| layers N arm (section N3-N3) | Type 4 rock (sheet note 6: Type 4 5-8 t, Type 5 500-1000 kg, Type 6 5-100 kg, Type 0 8 t) from +0.50 down to -2.20 (2.70 m); Type 5 (500-1000 kg) -2.20 to -3.51; Type 6 (5-100 kg) 0.50 m blanket on the seabed; Type 0 (8 t) toe berm 1.35 m high, 3.0 m wide top, side slopes 1:1.5, 2.0 m apron | DRG 1021 N3, notes 6 | labels '+0.50', '-2.20', '2700', '1350', '3000', '2000', '500' | levels measured on a 300 dpi render of the 1:200 sheet, +-0.05 m |
| height above seabed | about 4.5 m (N arm; crest +0.50 above seabed about -4.0); tail about 4.4-5.0 m (crest +1.00 above -3.4..-4.0, read roughly on section N2); 5.1-5.7 m (oval; +1.50 above -3.6..-4.2) | DRG 1021/1023 | derived | +-0.4 m (seabed 'varies'); HRPP576 Fig 3 initial design 4.0 m |
| side slopes, design | 1:3 (arm and oval flanks, both sides); 1:4 (mid-reef flanks, N4); 1:5 (head); toe berm 1:1.5 | DRG 1020 slope labels; 1021 N3 '3', 1022 N4 '4', N1/N5 '5' | 'x:1' triangles | design nominal |
| side slopes, as built (LiDAR 1 m DSM) | median 1:4.4 (H:V) between -1.5 and -0.5 mODN, 1:5.3 between -0.5 and +0.2 (N); 1:4.1 / 1:4.0 (oval); crest zone flat | WG LiDAR SN6089, 2022-03-19 (ref5; fig img-24) | gradient of the 5x5-smoothed DSM | +-1 in the ratio; flatter than design because the rock spreads / DSM sees block tops |
| width of exposed mound at -2.3 mODN | N arm 33-37 m, head 46-52 m, tail end 34-40 m; oval 38-41 m | LiDAR | cell counts across the axis | +-2 m |

### Seabed and toe depths
| quantity | value | source | quote / figure | uncertainty |
|---|---|---|---|---|
| existing seabed under the north arm | about -4.0 mODN (section N3: -4.01; N4: about -3.8) = -4.3 m MSL | DRG 1021 N3 / 1022 N4: ground line of the section at 1:200 | 'EXISTING SEABED VARIES' | +-0.3 m ('varies') |
| seabed under the oval | -3.6 to -4.2 mAOD (note); the drawn ground line on S2 sits at about -4.5 | DRG 1023 S2 | 'EXISTING SEABED VARIES -4.2 TO -3.6m AOD' | +-0.4 m |
| pre-construction contours | -3 to -5 mODN around the reefs (C about -3.5, A/B about -4 to -5), by eye | HRPP576 Fig 2 (img-17) | contour labels '-3.0mODN' .. '-5.0mODN' | +-0.5 m |
| toe of the structure | foot of the Type 4 armour at about -2.2 mODN; toe berm top -2.15 (1.35 m above the 0.5 m blanket); outer seabed edge of the apron about 3.5-6.5 m beyond (outer ring) | DRG 1020/1021 | ring offsets 0.76 / 2.0 / 2.0 / 3.0 m | design |
| offshore profile | EMODnet cells at the reef are GEBCO interpolation (-0.34..-0.13 m rel. LAT = -2.78..-2.57 mODN) = 1.0-1.4 m shallower than the design seabed; surveyed cells start 335 m offshore, -1.1 % gradient | emodnet/REPORT.md 9.2; this check | - | use only as an offshore trend |
| intertidal sand east of the reef | LiDAR 2022 sand surface east of E 260505 (window 260 x 300 m): median -1.37 mODN, range -2.35..-0.37 | WG LiDAR SN6089 | cell statistics | +-0.15 m |
Footprint level for the 3D model (choose one and state it): visible rock edge (drawn polygon, 5,743 m2), design armour foot (6,989 m2, about -2.2 mODN) or LiDAR exposed outline (8,675 m2, about -2.3 mODN); the toe at the seabed is larger (design outer ring 11,488 m2).

### Welsh coastal monitoring / LiDAR (read-only, nothing over 50 MB)
- Welsh Government LiDAR 2020-22 tiles SN6089 DSM and DTM (about 1 MB each, read in a scratch folder, not kept): the one useful dataset. Flight 2022-03-19 03:15-03:20 UTC at about LAT.
- Ceredigion annual beach monitoring (Royal HaskoningDHV Volume I 2012-13, ref8): Borth profiles are LiDAR-derived beach profiles to the frontage; no reef levels. Wales Coastal Monitoring Centre (wcmc.wales): data platform is an interactive map (no static values readable); CoastSnap Borth photographs (2024-25) exist but were not saved or checked for the reef.
- NRW metadata for the 2020-22 tiles does not state the vertical datum; 'ODN' is assumed from agreement with the design levels (+-0.15 m).

## Files made or changed by this verification
shape.json (status verified; frame +x south; alt_outlines_m; sources drg1020/1021/1022/1023/1001, hrpp576f2/f3, lidar2022; dimensions_check, gemini, references, verification, confidence), METHOD.md (step 4), sources.md (added rows), VERIFY.md, HANDOFF.md, overlays/verify_trace_sat2024|2022|2012.png, overlays/verify_design_lidar_vs_trace_sat2024.png, overlays/verify_lidar_dsm_2022-03-19_sections.png, src/borth_rh-drg-9V5090-*.pdf|png, src/borth_hrpp576_*.pdf; 03_images/reefs/borth-coastal-defence-reef/images.json + IMAGES.md (img-17..25 added, rows 01-16 for_3d_check updated), 03_images/reefs/NEW_IMAGES_LOG.md, 05_qa/00_STATUS.md.
Run completed 2026-10-06.


## Outline versions - decision (added 2026-10-07 by the 3D agent)
Lior chose the LiDAR default, 2026-10-06. shape.json now carries outline_versions (lidar_2022 = default, design_1020, sat_2024), default_outline = "lidar_2022" and versions_info (written by 3d\build_3d.py --shape); canonical.polygons_m is unchanged (the traced 2024 polygon, kept for traceability).

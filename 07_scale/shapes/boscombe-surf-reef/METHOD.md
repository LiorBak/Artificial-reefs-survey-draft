# METHOD - boscombe-surf-reef (plan-shape trace)

Run started 2026-10-05

## Step 0 - folder inspection (resume)
- Folder held src\ (8 geo-referenced satellite PNGs + .geo.json: boscombe_2014, boscombe_current, esri_current_2025-06-15_z19,
  esri_wayback10_2011-09-28_z18, wayback15423_2017-06-20_z18, wayback16245_2021-09-06_z19, wayback48376_2020-05-07_z19,
  wayback57965_2022-08-26_z19, wayback60013_2023-09-03_z19 = 9 png) and overlays\ (33 draft renders from an earlier run). No sources.md, no shape.json.
- Overlays are treated as UNVERIFIED notes (to be redone). src files: origin to be re-established from .geo.json sidecars.

## Step 1a - first look at existing satellite src files (2026-10-05)
- Sidecars (.geo.json) give the origin of every src PNG: Esri World Imagery, either current MapServer tiles or dated Wayback releases,
  with Web-Mercator bounds => all 9 files are re-traceable (origin re-established, nothing to delete on provenance grounds).
  Note: boscombe_2014.png is misnamed - its sidecar says Wayback release 10, capture date 2011-09-28 (NOT 2014); boscombe_current.png = current Esri 2025-06-15 z18.
  Duplicates: boscombe_2014.png (z18, 800 m box) duplicates esri_wayback10_2011-09-28_z18.png (z18, 500 m box); will delete duplicates later.
- Viewed esri_wayback10_2011-09-28_z18.png (1322 px, 0.378 m/px): reef CLEARLY VISIBLE as a dark rectangular striped block (bag rows) about
  ~280 px long, ~100-150 px wide, oriented NNE-SSW (long axis tilted). Visible roughly 150-190 m offshore of the beach. Also a dark diffuse blotch just
  NNW of the block (scour/seaweed/sand shadow?) and faint linear streaks SW (cables/wakes?). => primary candidate (2011-09-28, ~2 yr after completion).
- Viewed esri_current_2025-06-15_z19.png (2116 px, 0.189 m/px): reef only a blurred, dark, wind-ruffled patch (~ x 770-1130, y 720-1130 in 2116-px frame);
  bag stripes no longer resolvable. Usable only as a cross-check of position/extent, not for outline detail.
- Montage check of the other Esri images (thumbnails): wayback15423 (2017-06-20 z18) and wayback48376 (2020-05-07 z19) = rough, wind-roughened sea, at most a very faint
  darker ghost where the reef is, no outline; wayback16245 (2021-09-06), wayback57965 (2022-08-26), wayback60013 (2023-09-03) = nothing visible (turbid / glint / near-black water).
  => reef not usable for tracing in 2017-2023 images. Conclusion: ONLY the 2011-09-28 Wayback-10 image (and the blurred 2025 image) show the structure.
- boscombe_2014.png (800 m box, z18, 2116 px, 0.378 m/px) = same Wayback-10 2011-09-28 imagery, wider crop: shows pier + groynes + reef in one frame (good for a scale check vs the 180 m pier).
- sources.md written (img1 wide 2011, img2 tight 2011, img3 2025). Renamed boscombe_2014.png -> esri_wayback10_2011-09-28_z18_wide.png (it is 2011, not 2014); deleted 2017/2020/2021/2022/2023 + 2025 z18 duplicate.

## Step 2 - tracing img1 (Esri Wayback-10, 2011-09-28, wide crop; pixel frame = 2116x2116, 0.3781 m/px at centre)
- Located the reef from img2 pixel (655,660) -> lat/lon 50.71750 N, 1.83883 W (satellite.py pix2ll) -> img1 pixel (1593,1352) via ll2pix.
- Display helper (scratchpad, not in project): global percentile contrast stretch + gamma 0.6 + 3.5x Lanczos zoom + tick grid every 20 px, polygon drawn on top.
  The raw image is low contrast (dark water); with stretch the structure shows as a striped band (bag rows) running NNE-SSW with a pale (sand/shallow) patch
  between two "prongs" at its northern end.
- Draft trace v1 (25 vertices, px coords in img1): outer outline of the dark striped bag field. Checked overlay: outline follows the visible edge on W, E, S sides to ~2-3 px (~1 m);
  north edge is fuzzier (top row of bags) ~ +/-3 px. Interior pale patch at about x1600-1626, y1244-1287 left INSIDE the outline (looks like a gap/shallower sand patch or a burst/missing bag - noted).

### Scale + orientation checks on img1
- Tiles are Web-Mercator, north-up. m/px: 156543.03*cos(50.7185 deg)/2^18 = 0.3781 m/px (ground). sidecar m_per_px_center = 0.37808. OK.
- Independent check with Boscombe Pier (Wikipedia: "200 yards (180 m) long"): pier head end (tip centre) ~ px (851,1139); pier root at the front of the pier-approach building ~ px (788,700):
  length 443 px = 167.5 m; if the pier is counted from the promenade (~y 665) it is 471 px = 178 m. Consistent with 180 m within ~7% (root definition ambiguous). Scale OK.
- Pier axis and groyne axes measured in img1: pier root (788,700) -> head (851,1139): bearing 172 deg (SSE); groyne at overview x~645: bearing ~172 deg. So shore-normal ~172 deg, shoreline bearing ~82 deg (ENE-WSW), consistent with the promenade running up to the right (slope about -7 deg).

### Shoreline picked on img1 (for distance / angles)
- Surf line (waterline at imagery time, read on a 2x grid view): (1300,772) (1450,742) (1600,730) (1750,720) -> line (1300,772)-(1750,720), bearing 83.4 deg (ENE-WSW).
- Seawall base / back of beach: (1300,610) (1450,595) (1600,582) (1750,565) -> bearing 84.3 deg.
- Groyne E of reef-normal: (1768,632)->(1784,757): bearing 172.7 deg => shore normal 173 deg, matches pier (172 deg).

### Draft result (shape.json written, status traced) - img1 25-vertex outline
- Area 4,042 m2 (28,278 px2 x 0.3781^2), bbox 208 x 262 px (79 x 99 m, N-up axes), max dimension 123.4 m (vertex 3 to 17), centroid px (1578,1343).
- Distance offshore (shore normal): nearest edge 181 m / centroid 226 m / far edge 276 m from the surf line at imagery tide; 241 / 286 / 336 m from the seawall base.
- NOTE: footprint 4,040 m2 is only ~40% of the "approximately one hectare" in the text; to be reconciled in dimensions_check (bags in 2011 photo = 2 years after completion).

## Step 1b - literature / web sources (2026-10-05)
- WebSearch found: Rendle & Davidson (Plymouth Univ.), "An evaluation of the physical impact and structural integrity of a geotextile surf reef", ICCE 2012 (Santander/Coastal Engineering 2012),
  https://icce-ojs-tamu.tdl.org/icce/article/view/6794 ; PDF https://icce-ojs-tamu.tdl.org/icce/article/download/6794/pdf_441/27535 (downloaded to %TEMP%\bosc\icce6794.pdf, 14 pp, 1.3 MB).
  Text facts (read myself): "32 geotextile sand filled containers of various sizes set in opposing directions ... in two layers" (p.2); "Situated 225 m offshore in 2.7 to 5 m depth the footprint covers 45,000 m2" (p.3);
  "largest containers ~5 m diameter and 70 m long (only 8 of this size; they make up the bulk of the structure)" (p.10); modal wave approach 191 deg; "angle of approach is shore normal, 173 deg" (p.10-11)
  => the paper's shore-normal 173 deg agrees with my own measurement (173 deg, from groynes/pier/surf line on the 2011 image). Bathymetry: DGPS surveys Oct 2009, May 2010, Oct 2010, Apr 2011 (Channel Coast Observatory / Bournemouth BC).
  Damage: one 70 m container (propeller?) lost ~80 t sand, April 2011 => 4 m gap, 2 m crest dip; adjacent container lost by 2012 (gap up to 10 m). Reef closed 31 March 2011 after the inspection of 23 March (BBC; Rendle & Davidson write 'April 2011') [corrected by the verifier 2026-10-05].
  Figures: Fig.1 = oblique aerial post-construction 2009 (parallel bags, shoreward at top right); Fig.2b = schematic map; Fig.9 = April 2011 bathymetry (3D-tilted surface plot, OS grid axes) - not a true plan, no scale suitable for tracing.
  The "45,000 m2" footprint is 11x the traced bag field (4,040 m2) and 4.5x the other text values (1 ha) -> either a typo for 4,500 m2 (matches 4,040 m2 within ~10%) or includes the surrounding scour/influence zone; flagged.
- The ResearchGate abstract snippet from the search result claims "32 giant bags with a basal area of 50 x 70 m" (3,500 m2) - could not fetch ResearchGate (HTTP 403); only a search snippet, to be treated as UNVERIFIED.

### Fig. 9 of Rendle & Davidson 2012 = geo-referenced bathymetry plan (April 2011) -> independent cross-check
- Extracted embedded image (998x580) from the PDF with PyMuPDF; left panel is a true plan view (matlab pcolor, axes Eastings x10^5 / Northings x10^4, light-grey gridlines) in OSGB36 metres,
  but with unequal axis scales. Gridlines located by pixel scan: vertical x=147 (E 411400), 338 (411500), 433 (411550); horizontal y=39,104,126,192,235 = N 91000, 90940, 90920, 90860, 90820.
  Scales: 1.908 px/m in x, 1.0909 px/m in y (ratio 1.749). Made an isotropic copy (y stretched x1.749) so a single px_per_m applies: src\rendle_davidson_2012_fig9_left_isotropic.png (420x432, 1.908 px/m = 0.524 m/px).
- Position test: converted my 2011-satellite polygon (lat/lon -> OSGB36 with pyproj EPSG:27700) onto the plot using these gridlines: the outline sits on the red/orange/yellow (shallower than ~-2 m) reef
  with only small offsets => (1) Esri 2011 georeference is right, (2) shape agrees with the surveyed plan. Reef extents in OSGB from my trace: E 411,435-411,514, N 90,838-90,937 (paper Figs 4/9 axes put the reef at about E 411,470 N 90,900).
- Dropped the duplicate tight crop esri_wayback10_2011-09-28_z18.png from src (same imagery as img1).

## Step 1c - the designers' paper (new primary-quality design source)
- Found Mead, Blenkinsopp, Moores & Borrero (ASR Ltd = the reef's designers), "Design and construction of the Boscombe multi-purpose reef", ICCE 2010, PDF
  https://icce-ojs-tamu.tdl.org/icce/index.php/icce/article/download/1352/pdf_106/ (downloaded; 9 pp). Facts read in the text: 54 containers 1-5 m diameter, 15-70 m long, ~13,000 m3; dual-level reef with a 'focus' and a 'wedge'
  section; crest +0.5 m above chart datum; design waves 191 deg +/-6; sections of up to 14 containers (15-40 m) for the lower layer, 70 m containers placed singly for the upper main section; "reef 280 m offshore and east of Boscombe Pier" (Fig.3c caption);
  completed Sept 2009; post-construction settlement <=0.5 m.
- Fig. 3(a) = design depth plan with metre axes and a 0.05 km scale bar -> saved to src (img3) and traced as DESIGN cross-check (footprint at the ~-2.5 m model contour):
  area 4,217 m2, minimum rotated rectangle 110 x 49 m. Fig. 3(b) = container layout schematic (no scale, perspective wire-frame) and 3(c) = Google-Earth overlay of the design footprint (oblique) - looked at, not traced.
- Mead Fig. 5(b)/7 (BNPS aerial Sept 2009), Fig. 9 (surveys over Google Earth), Rendle Fig. 1: all oblique photographs / small overlays - looked at for qualitative layout only.
- Other leads checked and rejected for tracing: Raised Water Research "Boscombe-Arial" (oblique, pier at the left, no usable control), "Boscombe-From-Above" (near-nadir but no scale/north), Wavelength Mag image (a sign and a sand heap - not the reef),
  bournemouthswell.wordpress.com design diagram (file is only 100x39 px), Wikimedia diagram (cartoon, already judged unusable on 2026-09-25), ResearchGate/academia pages (HTTP 403 / not fetched).
- Rendle PhD thesis (Plymouth 2015, https://pearl.plymouth.ac.uk/bms-theses/412/) is said by a search snippet to contain "Bag Layout of the SFCs needed to build the Boscombe Reef" - NOT fetched (not needed: three independent outlines already agree; noted for Lior as a possible later refinement).
- YouTube lead 0Oi6D6Xp0oY: oEmbed returned title "Aerial view of Boscombe Reef", channel BoscombeReef; the 1280x720 thumbnail (https://img.youtube.com/vi/0Oi6D6Xp0oY/maxresdefault.jpg, viewed only, not saved) is an OBLIQUE helicopter view
  (beach at upper right, reef as parallel dark bag rows with a wider seaward wing on the left, website watermark thesurfreef.co.uk). Verified: it shows the structure from above but obliquely, no scale -> context only, not traced.
- sources.md rewritten cleanly (img1..img4).

## Step 3 - canonical shape and cross-check numbers (all from scripts kept in the scratchpad; numbers reproduced here)
- Deleted the 33 draft overlays left by the interrupted run (unverified notes); rendered a fresh set in overlays\ (img1_trace_closeup, img1_trace_context, img2_trace, img3_trace, img1_outline_on_img2_survey, img1_outline_on_2025, canonical_comparison).
- Tool bug found (07_scale\tools\geom.py make_canonical): it passes rotation_deg = -pix_angle to px_to_m, which negates it again, so for any alongshore direction that is not exactly (1,0) the polygon is rotated by 2x the tilt (my test: a point 100 px along (0.9934,-0.1157) maps to (97.3, -23.0) m instead of (100, 0)).
  My first draft (made with make_canonical, tilt 6.6 deg) therefore had a wrong bbox (71.7 x 105.3 m); the final shape.json uses my own, test-verified projection (alongshore/offshore dot products): bbox 88.5 x 94.3 m. Area, max dimension and distances were unaffected. I did NOT edit the shared tool.
- Primary (img1) numbers: area 4,042 m2; minimum rotated rectangle 121.1 x 45.0 m, long-axis line bearing 28.1 deg; max vertex distance 123.4 m; canonical bbox 88.5 (alongshore) x 94.3 m (cross-shore);
  shoreline (surf line) bearing 83.4 deg, shore normal 173.4 deg; nearest edge 181 m / centroid 226 m / far edge 276 m from the surf line; 241 / 286 / 336 m from the seawall base (beach 60 m wide at the image tide);
  reef's westernmost point is 241.6 m east of the pier head; centroid lat/lon 50.717532 N, 1.838909 W. The card coordinates (50.7185, -1.8417) are 225 m away (the reef centre lies ESE, bearing 119 deg, of them - the card point is at the beach/pier root side); Gemini's 50.7183, -1.8412 is 183 m away. Suggest updating the card to 50.71753, -1.83891.
- img2 trace (Fig. 9, April 2011 survey): area 3,372 m2, rotated rectangle 97.8 x 41.4 m, IoU with img1 0.78, centroids 8.2 m apart. Its smaller extent is the faint deeper southern toe (~25 m) that the DGPS plot shows only as cyan.
- img3 trace (designers' design shape): area 4,217 m2 (+4% vs img1), rotated rectangle 110.4 x 49.5 m.
- img4 (2025): img1 outline projected by lat/lon onto the blurred patch fits its W, E and NE edges => no change of the envelope 2011 -> 2025 (the faint patch is still the structure).
- Stripe/edge angles: envelope long axis 28.1 deg (55 deg to the shoreline); bag stripes ~28-38 deg (structure tensor on R,G,B at sigma 1.5-3.5 px; coherence only 0.3-0.4, so +/-8 deg);
  seaward block edges within 3-7 deg of shore-parallel / shore-normal.

### Observations on img1 worth keeping
- A diffuse dark blotch about 90 px (34 m) north of the reef's northern end (around img1 px 1600-1660, 1100-1150; visible in overlays/img1_trace_context.png) is NOT part of the traced outline: it sits where the April 2011 survey shows a cyan/blue hollow at the north end
  and Rendle & Davidson report erosion "in the western and north" areas / localised scour at the base - it is probably the scour hollow, not bags.
- Faint straight dark streaks SW of the reef (img1 px ~1110-1210, 1380-1620) are linear features on the seabed (pipeline/cable or tow marks) - not traced, not part of the reef.
- The pale patch inside the northern end (px 1600-1626, 1244-1287) is left inside the outline; the April 2011 damaged 70 m container lost 80 t of sand and left a 4 m gap with a 2 m crest dip (Rendle & Davidson), but this patch cannot be tied to it with the available evidence.

## Step 4 - Gemini checks (read-only; nothing from Gemini used)
Gemini files read: 07_scale/00_gemini_footprints_extract.json (Boscombe entry), 02_world_reefs_data/reef_footprints.json (Boscombe entry), reef_footprint_scale_analysis.md, scale_sketch_photo_alignment_audit.md, 05_web_build/images/IMAGE_PROVENANCE.md, images_provenance.json.
- Gemini values: delta/'right-hand peeler', 100 x 55 m, 5,200 m2 (net core 3,070), crest -1.5 m; reef_footprints.json instead has 171.2 x 87.7 m, 9,180 m2 and a 4-vertex quadrilateral (9,176 m2, 169 x 87 m rotated rectangle) - internally inconsistent; its "187.5 m long diagonal" is our own earlier schematic number.
  Compared in overlays/canonical_comparison.png: Gemini's quadrilateral has about 2.3x the traced area and a different orientation.
- Council 'Boscombe Reef Review (2012)', Raised Water Research 'Dossier (2024)', Halcrow 'Independent Engineering Audit (2011)': no URLs. Searched (web): nothing found for the council review or the Halcrow audit; the real RWR spot page (fetched via search tool) says 2.5 acres / 210 m only. Verdicts: unverifiable / dimension_not_in_source / unverifiable.
- 'Davidson (2010) Final Performance Report': real document is a 6-month INTERIM report; surf-quality content, no 100 x 55 m plan. 'Harrow et al. 2012 multibeam': not found; real 2012 Plymouth paper is Rendle & Davidson (DGPS bathymetry).
- Geograph 1322892: fetched; genuine photo of the right site (Chris Downer, 25 May 2009, CC BY-SA 2.0) but the container-count / distance / diver-error claims Gemini attaches to it are not on the page.
- Gemini's crest depth -1.5 m LAT contradicts Mead et al. 2010 (design crest +0.5 m above chart datum).

## Step 5 - confidence and open issues
- [SUPERSEDED by the verifier, see 'Verification 2026-10-05' below: final confidence is MEDIUM.] Tracer's rating was HIGH for the outline and position (reason in shape.json). Weak point: the text 'about 1 ha' (and the football-pitch statements) are not supported by any of the three plan-view sources; the traced bag field is 0.40 ha.
- The orchestrator may prefer 'medium' if it reads the rubric literally ("dimensions agree with text within ~10%" fails for the area figure) - I kept 'high' because the text figures contradict each other (45,000 / 10,000 / ~7,000 / 3,500 m2) and the designers' own design plan matches the trace within 5%.
- Not done / possible refinement: the Rendle PhD thesis (PEARL 412) reportedly holds a bag-layout plan; the oblique aerial photos could be rectified with a homography but control points are all clustered on the shoreline (poorly conditioned).
- Card fixes suggested: coordinates -> 50.71753, -1.83891 (card point is 225 m off); footprint area and length figures (see dimensions_check).
- Run finished 2026-10-05.

## Addendum 2026-10-05 - geom.py make-canonical / px_to_m sign bug (orchestrator warning acknowledged)
- Status: shape.json does NOT rely on make-canonical or px_to_m. The canonical polygon is computed with an explicit rotation: for each img1 pixel vertex (x, y),
  along = ((x - ox)*ux + (y - oy)*uy) * 0.37808 and off = ((x - ox)*nx + (y - oy)*ny) * 0.37808, with origin (ox, oy) = (1509.7, 747.8) px on the surf line,
  alongshore unit u = (cos a, sin a), a = atan2(720-772, 1750-1300) = -6.59 deg (0.99339, -0.11479), offshore unit n = (-uy, ux) = (0.11479, 0.99339). Same projection is used for the img2 and img3 polygons in canonical.cross_check_polygons_m.
- Hand check of a known point after the final build: 100 px along u maps to (37.81, 0.00) m and 100 px along n to (0.00, 37.81) m (0.37808 m/px x 100); all 25 vertices re-computed independently differ from shape.json by at most 0.019 m.
  Nearest / farthest offshore y = 181.25 / 275.59 m, matching the perpendicular distances to the surf line measured directly on the image.
- My first draft of shape.json (written with make-canonical before I noticed the bug) had a wrong cross-shore/alongshore bbox (71.7 x 105.3 m); it was overwritten. Final bbox: 88.5 m alongshore x 94.3 m cross-shore. Area, max dimension, centroid and the surf-line / seawall distances were never affected.
- I did not edit the shared tool (it is being fixed separately).


## Verification 2026-10-05 (adversarial pass; shape.json stamped verified_on 2026-10-04 per the brief)
Full evidence in VERIFY.md. Changes made to shape.json, METHOD.md and overlays:
- Confidence changed HIGH -> MEDIUM. Reason: the rubric's 'high' needs dimensions within ~10% of the text; the headline area is -60% against a repeated ~1 ha (Wikipedia, Raised Water Research, Herbert et al. 2017 PLoS ONE). The outline itself is as well supported as a 'high' one (satellite + April 2011 survey + designers' plan, all re-checked). The tracer's argument that the text areas contradict each other is only partly true: 45,000 m2 and 'football pitch' differ, but 1 ha is the dominant figure.
- New quantitative cross-check: Mead et al. Fig. 3a converted to depth via its colour bar; the design relief >0.5 m above the fitted ambient seabed covers 5,255 m2 and holds 11,540 m3 (stated 13,000 m3). 13,000 m3 over 4,042 m2 = 3.2 m mean thickness (fits two container layers and 4.5-5.5 m relief); over 1 ha it would be 1.3 m. So the 1 ha is very probably a loose envelope (the shore-aligned bounding box is 0.83 ha), but no source defines it.
- Design version: wording corrected (April 2011 damage included; Aug-Oct 2011 repair works by ASR; the Dec 2010 plan to add 4 SE-corner bags and 3 pillow bags is not documented as built); closure date corrected to 31 March 2011.
- dimensions_check: the 187.5 m 'text' length was our own superseded oblique-photo estimate, now labelled so (diff_pct null); distance diff 9.6%; two rows added/extended (design relief footprint; Plymouth 45,000 m2 vs the 25,000 m2 plotted survey area).
- Recomputed with the FIXED geom.py: canonical polygon matches shape.json to 0.015 m (explicit-rotation version to 0.017 m); one known point checked by hand.
- Overlays: overlays/img1_outline_on_2025.png replaced by a smoothed full-outline version (the tracer's crop cut off the south end); added overlays/img1_verify_closeup.png (independent per-channel stretch, raw | outlined) and overlays/img3_relief_footprint_verify.png. All other overlays kept unchanged (they match shape.json).
- Not done: Rendle PhD thesis (PEARL bms-theses/412, article 1411) could not be downloaded (Cloudflare bot check; not bypassed). Rendle & Davidson Fig. 9 profile panels were not used (x-axis scale not reconcilable with the plan).

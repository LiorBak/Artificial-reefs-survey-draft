# METHOD - bunbury-airwave shape trace

Run started 2026-10-05

## Step 0 - RESUME inspection (2026-10-05)
Folder held: src/ (img1..img4 jpgs, sat_card_coords.png, sat_backbeach_current.png, sat_wayback_2019-12-12.png + .geo.json sidecars),
overlays/ (img1, img4 traces), shape.json (draft, status "traced", dated 2026-10-04), sources.md (draft). No METHOD.md -> created now.
Plan: treat all drafts as unverified. Re-download each src URL and compare file hashes to re-establish origin; re-view and re-trace img1 myself.

## Step 1a - provenance re-established (2026-10-05)
Re-downloaded the three raisedwaterresearch.com URLs listed in the draft sources.md (HTTP 200); md5 identical to the saved files:
img1 Airwave-from-Above.jpg (701a3d5d...), img2 AirwaveDiagram2.jpg (e055191e...), img3 Airwave-Tear.jpg (b1dd72d5...).
img4 (805bff5e...) is byte-identical to project file 03_images/video_frames/bunbury-airwave/11804314_0005.jpg, the frame from the ABC News
video https://www.abc.net.au/news/2019-12-16/11804314 (see 02_research/videos/bunbury-airwave/videos.json: "aerial/drone shot of the inflated bladder
on the seabed with a diver alongside"). All four src images therefore kept. Satellite sat_* files carry .geo.json sidecars (provenance = Esri tiles).
Viewed img1 and img4 directly: img1 is a near-nadir drone photo of a roughly circular pale disc with a crescent-shaped paler lobe on its upper-left
rim, a ring/valve mark and "BUNBURY" lettering on the crown, an orange buoy NNE of the disc and a long thin tether line to the lower right.
img4 is the same scene from a much more oblique, higher-altitude angle (disc looks ~1.5:1 wide), with a swimmer/diver beside the disc's lower right.

## Step 2 - tracing img1 (primary), 2026-10-05
- Zoomed img1 (956x587) with overlay.py zoom (box 250,150-650,520, x2.5, grid 25) and read 29 vertices of the outer edge of the pale disc
  (the full disc including the paler crescent on the upper-left rim, where the dome wall shows; edge = where the pale sand/bladder meets green water).
- Rendered with overlay.py render, viewed: outline hugs the disc all round. Final overlay: overlays/img1.png.
- Polygon bbox 306 x 281 px (1.09:1); shoelace area 65,673 px2.
- img1 is near-nadir (the disc is almost round, tether line and buoy visible, no horizon) but not perfectly so.
- 2026-10-05: img5 ReefTopView.png saved to src/ and logged in sources.md

## Step 2b - cross-check traces (2026-10-05)
- img4 (ABC video frame 1024x576, more oblique): zoomed (box 540,280-760,450, x4.5, grid 10) and read 23 vertices of the outer edge of the pale disc;
  polygon bbox 157.8 x 107.4 px (1.47:1), area 12,813 px2. Overlay viewed: follows the disc closely. Saved overlays/img4.png. The draft's img4 "ellipse"
  was a formula-generated ellipse, not a read trace; replaced.
- img5 (RWR "ReefTopView.png", 1433x794 plan-view concept graphic): the structure is drawn as a perfect circle with concentric seam/contour rings
  over a stock photo of a beach. Read the four extreme points of the circle in a zoom (x 584.3-807.1, y 481.0-707.0) -> circle centre (695.7, 594.0),
  radius ~112 px; polygon = 24-vertex circle on those extremes (overlays/img5.png, viewed, fits). The graphic carries an arrow labelled "30m"
  (shore -> bladder). Scale test: the arrow spans y=100..472 (372 px) while the circle is 223 px wide, i.e. if the arrow were to scale the bladder would be
  ~18 m across, not 12 m -> the graphic is NOT to scale; used only to show the DESIGN plan shape = circle, and the design intent of ~30 m offshore.
- Circularity test (ellipse fit, Fitzgibbon least squares, numpy): img1 outline = ellipse with semi-axes 153.6 / 137.4 px (ratio 1.118), RMS deviation
  from the fitted ellipse 1.3% of radius (min/max normalised radius 0.967/1.027); img4 outline = ellipse 78.8 / 52.6 px (ratio 1.498), RMS 3.0%
  (0.951/1.049). Both outlines are ellipses to within a few percent, exactly what a flat circle gives when seen obliquely; the different ratios
  (1.12 vs 1.50) are explained by different camera tilt (approx. 27 deg off nadir in img1, approx. 48 deg in img4, from acos(b/a)). So the plan shape is a
  circle; the earlier draft's remark that the two images "disagree" on shape is resolved this way.
- Plausibility scale check on img4 (independent of the text): the swimmer's visible arms/splash span ~17 px (x 686-703, zoom at y~420) while the disc is
  157.8 px wide. An arm span of ~1.5-1.8 m gives ~9.5-11 px/m -> disc ~14-17 m. That brackets the text value (12 m) only loosely (swimmer is partly
  submerged and at the disc edge; +-40%); it excludes a 6 m or 25 m structure. Not used for the canonical scale.

## Step 3 - canonical shape (2026-10-05)
- Primary = img1 (no geo-referenced imagery of this reef exists; no as-built survey; img1 is the only near-nadir photo of the installed bladder).
- Ellipse fit of the img1 trace (Fitzgibbon least squares): centre (446.4, 334.9) px, semi-axes a = 153.55, b = 137.39 px, major axis along image
  angle -156 deg. Because an obliquely viewed circle keeps its true diameter along the major axis, scale = 2a / 12.0 m = 25.59 px/m (text-calibrated).
- Rectification: translate to the ellipse centre, rotate to the axes, stretch the minor axis by a/b = 1.118, divide by 25.59 px/m.
  Result: polygon of 29 vertices, bbox 12.07 x 12.09 m, max vertex distance 12.18 m, shoelace area 112.1 m2 (ideal 12 m circle 113.1 m2; the
  difference is the chord loss of a 29-gon plus +-0.4 m edge reading error). Unrectified, the same trace gives 100.3 m2 at that scale (11% low).
- The size therefore equals the text value by construction. Independent content of the images: (1) plan shape is a circle (ellipse residual 1.3% and 3.0%),
  (2) loose swimmer check on img4: ~14-17 m +-40%, no contradiction with 12 m.
- geom.py make-canonical was not used: it assumes a similarity transform with a shoreline-based frame; this photo is oblique and has no shoreline.
- distance_offshore_m = 37.5 (midpoint of the text range 30-45 m, Raised Water Research). Not measurable from any image.
- Angles: none. A circle has no edges and there is no shoreline in the photo.
- Geo-reference: not possible for the polygon. Approximate centre only (location_note): the Back Beach SLSC building is at about -33.3271, 115.6298 on the
  2025-08-30 Esri image (matches the wanderboat coordinate -33.327276, 115.629902 within 15 m). Text: reef 30-45 m off the beach, just south of the club.
  45 m seaward of the waterline (read from the image at pixel (525, 870)) = -33.3276, 115.6284, +-100 m.
- Card lat/lon (-33.31, 115.64) is on the boat-harbour groyne ~2.2 km NE of the site (sat1). Gemini's -33.3362, 115.6261 is ~1 km south of the site.

## Step 4 - confidence: medium
Circle clearly visible on a real photo from the install week, corroborated by a second frame from another angle and a design plan graphic; but no scale or geo-reference, so size is text-sourced.
Rubric 'high' needs geo-referenced imagery or a scaled as-built; 'low' means no image of the structure.

## Gemini sources checked
See sources.md (verdicts: ABC 11802958 wrong_site; ABC image URL dead; Wikimedia Back Beach photos dimension_not_in_source; Bottegal brief, Surfer review and
Inertia article unverifiable; Gemini's footprint is a formula 24-gon circle). Nothing from Gemini was used.

## Housekeeping
Deleted unused src files: img3 (underwater tear close-up) and the Wayback 2019-12-12 tile (holds 2016 imagery). Replaced the draft overlays with
overlays/img1.png, img4.png, img5.png. Draft shape.json (2026-10-04) was rebuilt from scratch values above; draft's text-only items (references, Gemini
footprint values) were kept after re-fetching where possible. Searches stopped after the primary + two cross-checks (scope cap).
Other RWR page ("The Bunbury Airwave Artificial Surf Reef Tears During Installation") was not opened - cap reached.

## Verification pass (2026-10-05, run dated 2026-10-04) - corrections made
- Verdicts and evidence are in `VERIFY.md` and `shape.json` -> `verification`. Status set to "verified"; confidence stays medium.
- Tear date: the seam tear was spotted by a diver on Friday afternoon (13 Dec 2019); 16 Dec is the date ABC and RWR reported it. Earlier wording "torn on 16 Dec" and "one day after the 16 Dec install attempt" removed. Photo img1 is the header image of RWR's 16 Dec post; exact capture day unknown.
- img1 source page corrected to the RWR tear post (the profile page serves a different file, uploads/2019/09/Airwave-From-Above.jpg). img5 credit corrected to "Image: Unofficial Networks" (RWR caption).
- Redesign wording: Tracks (2021-10-08) says only "a stronger compound that can be welded", made in Australia, "a more classic dome shape"; the earlier "welded PVC/polyurethane" appears in no source and was removed. The redesign was only tested in the Queensland hydraulic tank, never installed.
- Profile note: the as-built had an asymmetric "skateboard ramp" profile on a circular base (Tracks 2021; Tradie 2019). The drawing is the plan outline only.
- Offshore distance text range is 30-50 m (RWR 30-45; Tracks 2019 ~45 m off the low-tide mark; SurferToday 50 m), not 30-45 m. 37.5 m kept as a text-only midpoint.
- Outline-to-edge test (brightness gradient along the outline normal, 29 vertices of img1): mean |offset| 3.3 px = 0.13 m, 24/29 within 5 px; half-max edge would shrink the diameter 2-3%. Excluding the pale upper-left crescent would shrink it about 8%.
- Canonical polygon: built by explicit rotation here (geom.py make-canonical was not used, so its rotation-sign bug does not apply); recomputed independently, all 29 vertices agree to 0.0005 m; vertex 0 hand-checked (see `shape.json` -> canonical.notes).
- Gemini: all tracer verdicts re-confirmed against the originals; Wikimedia OIC photo is dated 2006 (not 2021); eight further Gemini claims contradicted or unsupported.


## Developer's account (Waveco About page, accessed 2026-10-05)
Checked 2026-10-05 against sources that do not depend on the page. The developer's own About page (Waveco Pty Ltd, https://www.waveco.com.au/about/, accessed 2026-10-05) [R21], section "The Path to Discovery" > "The Bunbury Deployment", says verbatim:

> In 2018, we deployed a 150-tonne sand-slurry bladder at Bunbury’s Back Beach. While it successfully created peeling waves, a final-day overpressure event led to a seam split. It wasn't a failure—it was the catalyst for our next breakthrough.

Confirmed in the raw page HTML (curly apostrophe in "Bunbury’s"; the passage is undated; WordPress metadata: page created 2019-08-11, last modified 2025-12-22). Self-published and promotional. Several comparison sources quote Bottegal himself (Tracks 2021, Bunbury Mail 2022); that is flagged in each row. Card verdict stays "failed" (reason in the card's `verdict_reason`).

| Waveco page says [R21] | Independent record | Assessment |
|---|---|---|
| **(a) Year:** "In 2018, we deployed..." | Installation was attempted in **December 2019**: it began the week of 9 Dec, a diver spotted the seam tear on the afternoon of Fri 13 Dec, and it was reported on Mon 16 Dec [R1][R5][R6][R7][R15]. Before that it had not been deployed: ABC (2019-06-13) said it was set to be installed in November [R2]; Tracks (2019-08-12) described a trial planned for mid-November and a crowd-funding campaign "last year" [R23]; Raised Water Research (2019-10-14) said construction was half-way [R4]; Tracks (2019-11-15) said the live trial was "some time in the next couple of months" [R9]; RWR's spot page says it was installed in December 2019 [R3]; ABC listen (2022-10-07) says "In 2019 ... attempted to install" [R24]. The only 2018 events found are Waveco's failed Aug 2018 Kickstarter [R3] and a "may be installed" preview [R19]. One outlier: the 2022 Bunbury Mail intro says "four years since" and captions a supplied photo "The original 'Bunbury Airwave' in 2018" [R8]; that conflicts with every dated 2019 report above. | **Contradicted.** December 2019, not 2018. |
| **(b) Fill:** "a 150-tonne sand-slurry bladder" | Sand-slurry fill is corroborated: Tracks 2019 ("washed, coarse beach sand ... for that slurry") [R9]; Bottegal in the Bunbury Mail ("irrigate the sandslurry") [R8]; RWR ("partially filling it with sand", the rest water and air) [R3]; a local observer on Swellnet saw a slurry pump and hoses on the beach on 7 Dec 2019 [R15]. ABC and SurferToday call it "filled with air" [R1][R7]; Tracks 2019 says "a mixture of sand and air" [R9]; the card's "air bladder anchored with sand ballast" fits all of these. The **mass** has no independent source: 140 tonnes in Tracks 2021 and the Bunbury Mail 2022, both reporting Bottegal [R22][R8]; "150T" in a forum summary of his Feb 2020 conference talk [R15]. | **Material and bladder type consistent.** Mass is developer-only, 140-150 t (the 7% gap is inside the developer's own statements); the card keeps 140 t and flags 150 t. |
| **(c) Waves:** "While it successfully created peeling waves" | **No independent report, photograph or video of surfable waves on the reef was found.** ABC (2019-12-16) reports only the tear; it paraphrases a tourist as "looking forward to riding whatever wave the Airwave produced", and beach-goers were told to keep away [R1]. RWR, SurferToday and The Inertia report no wave [R5][R6][R7]. The ABC video 11804314 shows the bladder on the seabed with a diver and no wave (card video notes). Tracks 2021 says the plan to webcast "perfectly peeling waves" "didn't quite play that way" [R22]; the webcam was not live for the install [R15]. The wave claim comes from the developer alone: Bottegal told the Bunbury Mail in 2022 that "a wave did break" just before the tear, a "lone wave" that "peeled for about thirty metres" and "created a 0.75 metre wave" seen by onlookers [R8] (his recollection 27 months later; no footage or named witness cited). Second-hand only: a Swellnet user quoting Waveco's Dec 2019 Instagram says the redesign reflects "small wave action" observed during install, and a forum summary of his Feb 2020 talk lists "Small Wave Peak" among positives [R15]. | **Not independently supported.** At most one small wave (about 0.75 m, about 30 m long) reported by the developer himself, while the bladder was about 90% installed and not anchored; nobody surfed it and no footage was found. "Successfully created peeling waves" overstates even Bottegal's own account. |
| **(d) Cause:** "a final-day overpressure event led to a seam split" | **Seam split:** confirmed; the tear was along a glued seam, not through the rubber [R1][R5][R8]. **"Final-day":** the tear was spotted on about the fifth day of the install week (Fri 13 Dec) when, per ABC reporting Bottegal, it was "90 per cent complete" but "not completely anchored" [R1][R7]; a local observer saw it "partially filled" that afternoon [R15]. It never operated as a finished reef. **"Overpressure":** this is the developer's own later explanation, and it changes. Dec 2019: an unexpected deep swell and undertow flexed the airbag against the seam [R1][R5][R7]. Oct 2021 (Tracks): sand pumped too heavily into one quadrant put too much pressure on one section of the skin, and the new valves avoid "the same over pressurization problem" [R22]. Mar 2022 (Bunbury Mail): glued overlapped Hypalon seams plus "full pump pressure applied to a confined space in the final fill phase" caused a tear in the back quadrant [R8]. No independent engineering report exists. | **Partly supported.** Seam split true; "overpressure" matches his 2021-22 accounts but not his 2019 one; "final-day" makes an unfinished install sound like a completed deployment. |
| **(e) Judgement:** "It wasn't a failure" | Bottegal told the Bunbury Mail in Mar 2022 the installation "certainly was not a failure" [R8]. But Tracks (2021-10-08) writes that he "readily admits that the first trial of his Airwave was a failure" (Tracks' paraphrase, not a direct quote) [R22]. On record: the bladder tore during installation and was removed within days (reports range from about 5 hours to 3 days) [R8][R18][R15]; no completed trial, and the planned 12-month UWA study never started [R9]; a second prototype (planned Dec 2020, about A$300,000 more needed) is not confirmed built [R18][R8]; the redesign has only been tank-tested [R22]; by 2025 Waveco's Bunbury proposal is a granite reef [R20]; and the same About page says Waveco "pivoted" away from the rubber Airwave after 2018 [R21]. | **A judgement, not a checkable fact.** The record supports "learning prototype" as the developer's framing, not "success". |

**How the developer's own account has moved** (all Bottegal/Waveco; later items are second-hand where marked): Dec 2019, tear caused by unexpected swell and undertow, "100 per cent" confident [R1]; Feb 2020 conference talk (forum summary, second-hand): "150T", "Small Wave Peak", removal in 5 hours, "98% success" [R15]; Jul 2020, removed "in half a day" [R18]; Oct 2021, Tracks says he admits the trial was a failure, sand pumped too heavily into one quadrant, 140 t [R22]; Mar 2022, "certainly was not a failure", glued Hypalon seams and full pump pressure, a lone 0.75 m wave, removed within three days, 140 t [R8]; current About page, "In 2018", "150-tonne", "successfully created peeling waves", "final-day overpressure event", "wasn't a failure" [R21].

Legend: R# are the reference ids of the reef card (`02_research/reefs/bunbury-airwave.json` / `.md`, where each is described in full). R1 ABC News 2019-12-16 https://www.abc.net.au/news/2019-12-16/word-first-surf-reef-tears-during-installation/11803228; R2 ABC News 2019-06-13 https://www.abc.net.au/news/2019-06-13/world-first-artificial-surf-reef-to-be-installed-at-bunbury/11204280; R3 RWR spot page https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/bunbury-airwave/; R4 RWR 2019-10-14 https://raisedwaterresearch.com/progress-update-on-the-bunbury-airwave/; R5 RWR 2019-12-16 https://raisedwaterresearch.com/the-bunbury-airwave-artificial-reef-tears-during-installation/; R6 The Inertia 2019-12-16 https://www.theinertia.com/surf/airwave-worlds-first-inflatable-reef-tore-during-installation/ (read via archive.org); R7 SurferToday 2019-12-17 https://www.surfertoday.com/surfing/ripped-seam-puts-worlds-first-inflatable-surf-reef-on-hold; R8 Bunbury Mail 2022-03-22 https://www.bunburymail.com.au/story/7667604/bunbury-still-set-to-become-surfing-destination/; R9 Tracks 2019-11-15 https://tracksmag.com.au/airwave-set-for-live-trial-at-bunbury-534049; R15 Swellnet forum thread (secondary) https://www.swellnet.com/forums/surfing-reef-designs/472884; R18 South Western Times 2020-07-09 https://www.swtimes.com.au/news/south-western-times/airwave-back-for-second-wave-of-bunbury-surf-ng-b881601738z (via archive.org); R19 SurferToday 2018-08-31 https://www.surfertoday.com/surfing/inflatable-surf-reef-may-be-installed-in-western-australia; R20 Waveco site/Instagram 2025 https://www.waveco.com.au/; R21 Waveco About page (developer, self-published) https://www.waveco.com.au/about/ (accessed 2026-10-05); R22 Tracks 2021-10-08 https://tracksmag.com.au/the-airwave-pumps-again; R23 Tracks 2019-08-12 https://tracksmag.com.au/inflatable-artificial-reef-is-ready-for-the-ultimate-test-529463; R24 ABC listen 2022-10-07 https://www.abc.net.au/listen/programs/southwestwa-breakfast/bunbury-waves/101511922.

What this means for the shape trace (nothing in `shape.json` was changed):
- The traced plan outline (circle, D 12 m, text-calibrated) is not affected by any of the four claims; none of them concerns the plan geometry.
- Date of the source photos: img1 is the header image of RWR's tear post of 2019-12-16 (file uploaded 2019-12-17 03:31 UTC, decoded from its `?v=` stamp, see VERIFY.md Check 5) and img4 is a frame of the ABC video 11804314 (Last-Modified 2019-12-16). Both files are dated December 2019 by their hosts, which independently supports December 2019 and contradicts "In 2018" for the install shown in the photos.
- State drawn: the installed, partly anchored bladder of the December 2019 attempt (about 90% installed, torn). It is not a successfully operating reef; any page caption should say "December 2019 installation attempt (torn)", not "2018 deployment" or "successful".
- Fill/mass (140 t per Tracks 2021 and Bunbury Mail 2022; 150 t per the Waveco page) is not used in the trace; the 3D note in `3d/SOURCES_3D.md` discusses it.

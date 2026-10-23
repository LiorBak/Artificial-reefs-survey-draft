# METHOD - southern-ocean-surf-reef-albany (Southern Ocean Surf Reef, "Midds Reef", Middleton Beach, Albany WA)

Run started 2026-10-10 (queue item 9, fresh agent). Network: only package servers reachable (albany.wa.gov.au, Esri, Navionics all
time out), so only locally saved sources were used. All code is in `scripts/` (re-runnable: `trace_mask.py`, `build_shape.py`,
`analysis.py`, `make_overlays.py`, `write_shape_json.py`; traced pixel polygons in `scripts/polys_px.json`).

## Step 0 - registry
`03_images/reefs/southern-ocean-surf-reef-albany/images.json` holds 13 rows. Viewed once, downscaled: img-10 (design.jpg), img-11 (RWR plan
diagram), img-13 (Esri 2026-01-20), img-12 (Esri 2025-01-16, as a before/after crop), img-05 and img-03 (construction aerials). The rest
(surf photos 01, 02, 04, 07; barge 06; quarry 08; vessel-track map 09) show no plan information and were not opened (shows-lines read).

## Step 1 - sources found (all already saved locally; see sources.md)
- sat2026 (img-13): Esri World Imagery, captured 2026-01-20, z18, 0.489 m/px, geo-referenced. Reef visible as a dark wedge with a
  breaking wave at its shoreward crest. PRIMARY for the as-built visible outline.
- sat2025 (img-12): same footprint 2025-01-16 (before construction). Before/after check: the dark patch is absent in 2025
  (mean green 137 inside the polygon vs 129 offshore) and present in 2026 (57 vs 68). `overlays/before_after_2025-01-16_vs_2026-01-20.png`.
- design_plan (img-11, 984x702) and design_table (img-10, 1026x521): Bluecoast final design plan with design contours over an aerial,
  scale bar 0-0.05-0.1 km, "ASR Design" legend, dashed crest line labelled 270 N - 305 N, design table (volume 34,000 m3 on 2017
  bathymetry, crest -1.00 m AHD, crest length 110 m @ -2 m AHD, 140 m from landward toe, 350 m north of Big4 Middleton Beach Caravan
  Park, left-hander, 60 deg peel angle). The plan is the same drawing in both files; img-11 is larger and is the one traced.
  NOTE: the registry text for img-10 quotes "volume 54,000 m3"; the table reads 34,000 m3 (checked on the image). Consistent with 62,800 t / 1.85 t/m3 = 33,950 m3.
- img-03 / img-05 (drone / oblique aerials of the berm under construction, 2025): no scale, oblique or partly built: context only.
- Not available (network): Esri Wayback intermediate dates, any as-built / post-construction survey, Bluecoast report PDF.

## Step 2 - trace
### 2a. sat2026 (primary)
1. Viewed the image, then zoom crops (3x with a 20 px grid, then without the grid and with contrast stretched, 2.5x). The grid and the
   glint-covered water hide the soft east edge, so a contrast-stretched green channel with a 7x7 minimum filter + gaussian (sigma 3)
   was used to see the wedge (`scripts/trace_mask.py`).
2. Objective check: threshold green < 30 (reef interior 12-20, ambient deep water 40-55) -> largest component, filled, simplified 3 px.
   Area 7,707 m2 (32,389 px). It misses the foam patch on the shoreward crest and has a ragged east edge.
3. Manual outline (20 vertices, px in `scripts/polys_px.json`): apex at px (397,418), crest edge ESE to (600,418), (670,428),
   east tip (712,482), south-east edge to (600,618), bottom tip (520,641), west edge back up via (472,582), (449,482), (405,440).
   It follows the visible dark edge; the mask lies 99 % inside it (IoU 0.69, the rest of the difference is edge fuzz and the foam patch).
   The foam patch on the crest (white oval, px 460-515, 428-455) is breaking water ON the crest and is included.
4. Scale: georeferenced. m/px = 0.4891 (sidecar), image centre (511,511) = (-35.018, 117.9207) (checked with satellite.py pix2ll).
   px -> east/north: E = (px-511)*0.4891, N = -(py-511)*0.4891.
5. Shoreline: no sharp swash line (foam), so the BEACH-FACE LINE = seaward end of the first bright dry-sand run (R > 165) in 30 rows.
   Theil-Sen fit over rows 440-720 (the stretch beside the reef): bearing 30.3 deg true (95 % CI 27.7-33.0; median abs residual 1.6 m).
   The beach curves: rows 40-320 give 16.7 deg, whole beach 27.0 deg. `overlays/shoreline_fit.png`. The true swash line is about 10-15 m
   further seaward (checked on one row); the vegetation edge is about 80 m landward.
6. Canonical frame: origin = foot of the perpendicular from the reef centroid on that line; +x alongshore toward bearing 30.3 deg (NNE);
   +y offshore, bearing 120.3 deg; this is a true unmirrored plan (+y = +x turned 90 deg clockwise, like geom.py and Borth).
   Result: area 10,918 m2; x -65.4..61.5, y 70.8..223.9 (centroid y 165.0); max dimension 157.2 m; extents along / across the crest
   bearing (281.5 deg) 157.2 m / 116.7 m.
### 2b. design_plan (cross-check and default outline)
1. Scale bar: zoom 5x with a 10 px grid: ticks at x = 493.5, 569.5, 645.5 px for 0, 50, 100 m -> 1.52 px/m (0.658 m/px), +-3 %.
2. North-up check: the dashed crest line runs px (765,335) -> (520,300) = bearing 278 deg (design text 270-305 N); a free rotation fit of the
   design outline to the satellite outline gives -3 deg (no rotation needed). Therefore north-up.
3. The 110 m and 140 m dimension arrows on the figure are NOT drawn to the bar's scale (arrow lengths 105 px = 69 m and 178 px = 117 m by the
   bar) - they are schematic, so only the scale bar was used for scaling (the earlier footprint file reached the same conclusion).
4. Traced the outermost contour (25 vertices, `scripts/polys_px.json`), rendered on a 2x crop, adjusted until it followed the outer contour.
5. Positioning: the figure has no coordinates. Rotation = 0 (north-up), scale = bar, translation chosen by maximising overlap (IoU 0.807) with
   the satellite outline; centroid-aligned IoU would be 0.792 (so the position is robust, +-3 m in the shore-parallel direction).
   A free similarity fit gives rotation -3 deg, scale 0.90, IoU 0.837 - the design outer contour is simply about 20 % bigger in area than the
   visible patch (toe vs visible edge). Result: area 13,104 m2; extents along/across the crest (278.1 deg): 164.6 m / 121.2 m.
### 2c. Not traced
img-03, img-05 (construction aerials: oblique, no scale, partly built), img-12 (no structure), img-10 (table; same plan as img-11 at lower resolution).

## Step 3 - dimensions check (see shape.json dimensions_check)
- Length 165 m (City): design 164.6 (-0.2 %), satellite 157.2 (-4.7 %).
- Width up to 110 m: design 121.2 (+10 %), satellite 116.7 (+6 %), measured across the crest.
- Crest orientation 270-305 N: satellite 281.5, design 278.1.
- 140 m from landward toe: 71 m from the dry-sand edge (centroid 165 m); about 150 m from the vegetation edge (+7 %). Reference line undefined.
- Volume 34,000 m3 over the design outline = 2.6 m mean height; over the satellite patch 3.1 m. Consistent with a crest at -1.0 m on a
  seabed about 3-5 m deep (inference only; no depth source - see FEASIBILITY.md).

## Step 4 - confidence: HIGH (planform position, size, orientation); area carries -30 % / +20 % edge-definition uncertainty. Reasons in shape.json.

## Gemini checks
Gemini's three sources have no URLs and cannot be fetched (network blocked); verdict unverifiable; its "2022 post-construction monitoring"
cannot exist for a reef built 2024-25. Its numbers equal the City page; its orientation "160-190 deg" is unsupported. Nothing used.

## Decisions
- Default outline = design drawing (Lior's priority: measured survey > design drawing of the built version > photo trace); satellite trace is the toggle version.
- State drawn: as built (Jan-Mar 2025). The March 2026 move of 18 rocks (card R11) is a note only.

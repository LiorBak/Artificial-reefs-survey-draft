# Scale drawings and the page's "Scale" tab: how they were made

Built 2026-09-25. This file documents the drawing step. The research behind each outline (which
text, which figure, which photo was read, and what was read off it) is in the per-reef provenance
files `07_scale/reefs/<slug>.md` and in the machine-readable `07_scale/reefs/<slug>.footprint.json`.
The page shows the same material under each drawing, in the "How we drew this" block.

## 1. Inputs (nothing else was used)

| Input | Role |
|---|---|
| `07_scale/reefs/<slug>.footprint.json` (13 files, status `verified`, verified 2026-09-25) | polygon(s) in metres, plan box, area, crest depth + datum, distance offshore + what it is measured from, derivation table, images relied on, Gemini comparison, confidence, open issues, verification log, references (R# = the card's ids, S# = sources added by the footprint pass) |
| `07_scale/reefs/<slug>.md` | full provenance write-up; copied unchanged to `04_build/docs/scale/<slug>.md` so the page package is self-contained |
| `02_research/reefs/<slug>.json` (verified cards) | reef name, verdict (fill colour), the reef's reference list, the accepted and rejected media lists |
| Wikipedia, "Football pitch" (https://en.wikipedia.org/wiki/Football_pitch, checked 2026-09-25) | the reference size: "FIFA recommends that the field of play measures exactly 105 metres ... long and 68 metres ... wide", so one pitch = 7,140 m² |

Gemini's folder (`C:\Users\lior\Documents\Gemini\AG\artifical reef`) was not read by this step.
Gemini's numbers appear only as quoted inside each footprint's `gemini_comparison` block, which the
footprint agents wrote after checking each value at the source. Lior's reference graphic
(`03_images/from_lior/goldcoast_pptx/image26.png`, third-party) was used only as a layout idea
(several reefs side by side with one shared shoreline and one scale bar). It is not embedded
anywhere; `sheet.svg` below follows that layout with our own outlines.

No new photo or video search was made for this step.

## 2. Drawing conventions (same in the page and in these files)

- Coordinates are metres. x = alongshore, y = offshore (positive seaward). The shoreline is the
  line y = 0. The origin is the shoreline point nearest the reef centroid. Each footprint's
  `coords` field states its own alongshore direction and how sure it is (mostly an unsourced
  convention: see the "Coordinates" note in each How-we-drew block).
- Plan view: sea at the top, beach at the bottom. The beach is a tinted band below the shoreline.
- One common scale. On the page the default is 1 px = 1 m, with zoom steps from ×0.125 to ×8
  (buttons −×0.5 / +×2). Every drawing always carries a 100 m scale bar. The files here are at
  1 px = 1 m.
- Panel frame: the drawing's alongshore extent + 15 m on each side, at least 150 m wide so the
  100 m bar fits. Height runs from the shoreline to the reef's farthest point + 15 m.
- Fill = the card's verdict colour (worked / partly worked / mixed / failed / too early to tell).
- Dashed vertical line = the drawn distance from the shoreline to the nearest point of the outline.
  This is a property of our drawing. The sourced "distance offshore" (and what it was measured to:
  inner edge, centroid, seawall base, landward toe...) is in the label below the drawing.
- Area = shoelace area of the polygon(s), computed by `compile_data.geometry_of`. Separate rings
  (Narrowneck's two arms, Borth's two mounds, Mount Maunganui's two arms) are summed as absolute
  areas. Every computed area is within 1.2 % of the footprint's `area_m2` (checked by `check.py`).
  Largest gap: Bunbury, 111.8 m² from a 24-gon vs π·6² = 113.1 m².
- "× football pitch" = area / 7,140 m².
- Overlay: every reef is centred alongshore on its own centroid. "By shoreline" keeps each reef's
  true drawn distance offshore on one shared shoreline. "By centroid" puts every centroid on one
  point and hides the shoreline. The frame fits the reefs that are switched on, so hiding the large
  ones zooms in on the small ones. The scale bar length is picked from 5/10/20/25/50/100/200/250/500 m.
- Football-pitch silhouette: 105 × 68 m, dashed, long side alongshore, next to the shoreline (or
  on the common centroid).

## 3. How each number on the page is sourced

- Plan box L × W: the footprint's `bbox_m`. The markers next to it are the sources of every
  derivation row about length, width, diameter, shape or topology.
- Area: the markers are the sources of the derivation rows about area. Where the area is only our
  polygon's geometry, the label says "derived".
- Crest depth and distance offshore: the footprint's own `ref` field. With no ref, the label says
  "derived". The short labels (for example "1.0 m below AHD (≈ MSL)") are copied from each
  footprint's `datum` / `measured_from` text in `compile_data.py` (`CREST_SHORT`, `DIST_SHORT`).
  Each one is guarded by a value + text needle, so an edited footprint cannot keep a stale label.
- Every R#/S# in the derivation tables opens the same source pop-up as the rest of the page.
  `check.py` confirms that all 75 ids used in the derivations have a pop-up target with citation text.

## 4. Reference merging and media rules applied

- Footprint references with a new id (S#, or an R# the card lacks) are appended to the reef's
  reference list and tagged "added by the Scale-tab footprint check, 2026-09-25".
- Where a footprint R# has the same id as the card's R# but a different URL (only Mexico R3: the
  Yahoo syndicated copy of the same Hollywood Reporter article), the card's entry is kept. The
  second URL is shown as "also read at".
- References that pointed to local Gemini files (Pratte's S2–S4, `file:///...`) are shown as
  internal notes with no link.
- Rejected media: if an image the footprint relied on is in the card's `images_rejected` (the three
  Opunake photos), the page shows "Image withheld", together with what was read off it (it gave no
  measurement). The URL is not rendered anywhere, and `check.py` enforces this. The provenance .md
  copies still name those URLs, because they are the research record.
- Thumbnails in "Images relied on" are hotlinked only for images already in the card's accepted
  `images` list with `hotlink_ok: true`. Everything else is a link.
- Media labels (whole page): images and video frames with a `shows` verdict get a caption tag
  ("shows the structure" / "shows the reef's effect" / "site context only"). Videos show their
  `about` label. "Site only — not about the reef" videos are a plain link (no player, thumbnail or
  frames); their two frame files were moved to `04_build/QA/removed_assets/opunake-reef/`. The hero
  image is chosen by structure visible, then reef effect visible, then site context. Within a tier
  the order is: the media re-check's hero recommendation, then a permissive-licence photo, then card order.

## 5. Per-reef summary (largest first)

| Reef | Shape | L × W (m) | Area (m²) | Crest depth | Distance offshore | Confidence | Gemini disagreements | Images relied on | Ids in derivation |
|---|---|---|---|---|---|---|---|---|---|
| Narrowneck Reef (Gold Coast Reef) | chevron | 600 × 350 | 114,950 | 1.5 m below low tide (≈ LAT), 2012 value | 200 m (to the inner edge) | medium | 5 | 2 | R1 R2 R3 R4 R8 R9 |
| Xala Reef (Costalegre) | other | 160 × 80 | 11,200 | 1.5 m below MSL (analogy estimate) | ≈270 m (analogy estimate) | low | 5 | 2 | R3 R7 |
| Boscombe Surf Reef | linear | 195 × 127.6 (envelope; structure 187.5 × 58) | 10,862 | +0.5 m, above LAT (designed crest) | 220 m from the seawall base | medium | 5 | 3 | R1 R2 R4 R7 R10 S1 |
| Southern Ocean Surf Reef ("Midds Reef") | crescent | 165 × 110 | 9,720 | 1.0 m below AHD (≈ MSL) | 140 m (to the landward toe) | medium | 5 | 3 | R2 R3 R4 R10 R15 |
| Palm Beach Reef | mound | 160 × 80 | 9,678 | 1.5 m below MSL | 270 m (centroid placed there) | medium | 8 | 3 | R2 R4 R5 R6 R7 R9 R13 R15 S1 |
| Borth coastal defence reef | other (two mounds) | 145 × 73 | 3,785 | not established (no source) | ≈350 m (midpoint of two conflicting figures) | low | 4 | 6 | R1 R2 R3 R11 S1 S2 |
| Mount Maunganui Beach Reef | chevron | 67.8 × 72.9 | 2,497 | 0.9 m below Chart Datum (≈ LAT) | 250 m | medium | 4 | 7 | R1 R2 R8 R12 S1 S2 S4 |
| Burkitts Reef ("Greg's Reef") | other | 120 × 46 | 2,480 | 0 m: rock exposed at low tide | 0 m (at the shoreline) | low | 3 | 3 | R1 R2 R3 R4 R6 R8 R10 S1 |
| Cable Station Reef | V | 140 × 70 | 2,299 | 1.5 m below water (average tide) | ≈275 m | medium | 5 | 2 | R1 R2 R4 R5 R6 R8 S1 S2 |
| Kovalam Reef | chevron | 87.9 × 41.6 | 1,084 | not found in any source | ≈55 m (schematic, not published) | low | 6 | 2 | R1 R2 R10 S2 S3 |
| Opunake Surf Reef | single-arm wedge (schematic) | 20 × 90 | 900 | 1.5 m, datum not stated | ≈150 m (estimated, to centroid) | medium | 3 | 3 (all withheld: rejected media) | R2 R3 R4 R7 S1 |
| Pratte's Reef | V (asymmetric chevron) | 57.8 × 31.2 | 324 | 1.83 m below MSL (design minimum) | ≈95 m ("~100 yards") | medium | 5 | 3 | R1 R4 R7 S1 S5 |
| Bunbury Airwave | mound (12 m circle) | 12 × 12 | 113 | 1.0 m below low tide (≈ LAT) | 37.5 m (design range 30–45 m) | medium | 2 | 2 | R1 R2 R3 R6 R8 |

## 6. Files in this folder

| File | What it is |
|---|---|
| `<slug>.svg` / `.png` (13) | one reef, 1 px = 1 m, a title band plus exactly the page's drawing |
| `overlay.svg` / `.png` | all 13 on one frame, by shoreline, with the football-pitch silhouette and a legend |
| `overlay_centroid.svg` / `.png` | the same, all centroids on one point |
| `sheet.svg` / `.png` | all 13 panels side by side, shorelines aligned, 1 px = 1 m (the image26-style layout) |

PNGs: `cairosvg` was installed but cannot load the cairo DLL on this machine, so the PNGs were
rendered by headless Chrome from the SVGs (same pixels as the SVG at 100 %).

## 7. How to rebuild

```
python 04_build/src/compile_data.py     # loads footprints, merges refs, media labels, copies docs/scale/*.md
python 04_build/src/build.py            # inlines styles.css, scale.js, app.js, data
python 04_build/src/check.py            # static + Scale-view checks (incl. headless DOM dump)
python 04_build/src/qa_shots.py --prefix round5
python 07_scale/make_drawings.py        # these documentation drawings
```

`07_scale/make_drawings.py` is a port of `04_build/src/scale.js` (panelFrame / panelSVG /
overlaySVG). It imports area, bbox and centroid from `compile_data.geometry_of`. If you change one
of the two, change the other.

## 8. Known limitations

- The outlines are documented schematics, not surveys. Four reefs are low confidence (Xala, Borth,
  Burkitts, Kovalam), and Opunake rests on text only.
- The alongshore direction (which way is +x) is an unsourced convention for most reefs. Mirror
  images are therefore possible.
- The page is not drawn over real aerial imagery as in Lior's reference, because there is no
  geo-referenced imagery for all 13 reefs and this step added no new images.
- The headless "mobile" screenshots use a minimum window width wider than 390 px. At a true 390 px
  viewport (checked in the in-app browser), the page has no horizontal overflow.

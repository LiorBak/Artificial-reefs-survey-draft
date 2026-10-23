# METHOD - cables-reef-wa (Cables Reef, Western Australia)

Run started 2026-10-05


## Step 0 - Resume inspection of src\ (2026-10-05)
src\ held 4 files from an earlier cut-off run, with no sources.md/shape.json/overlays:
- S1_pattiaratchi_reefdesign.pdf (256123 B), S1_fig1_sitemap_full_page.png, S1_fig4_wavebasin_full_page.png (2480x3509), S1_fig7_location_map.png (2409x3900).
- Origin re-established: re-downloaded http://joas.free.fr/studies/bei/g2s/reefdesign.pdf (HTTP 200, 256123 B) - MD5 02a6075b1eac84a68180bbfd89226fea, byte-identical to src PDF. PDF metadata: title "Microsoft Word - rr.doc", author Lorraine, creator Microsoft Word / Acrobat Distiller 3.01, created 1999-04-13. Content: C. Pattiaratchi, "Design Studies for an Artificial Surfing Reef: Cable Station, Western Australia", Centre for Water Research UWA, ref ED1483CP, 5 pages. The 3 PNGs are page renders of that PDF (pages 2-4 contain Fig 1, Figs 3-4, Figs 5-7) -> origin traceable, kept for now; may be replaced by native-resolution embedded-image extracts.
- Card dossier (07_scale/reefs/cables-reef-wa.md) already read: text values 140 m N-S x 70 m max width, 275 m offshore (RWR) / 250 m (paper), 3-6 m depth; previous pass called Fig 4 a V/chevron and could NOT resolve apex direction or scale.

## Step 1a - Paper figures read at native resolution (2026-10-05)
Extracted the embedded rasters of the PDF with PyMuPDF (scratch: %TEMP%\cables): Fig 1 p2 (225x165 px), Fig 3 p3 (225x119), Fig 4 p3 (226x145), Figs 5/6 p4, Fig 7 p4 (226x367 px, placed 225 x 366 pt on page, i.e. ~1 px per pt). The figures are low-res 1999 scans; the earlier full-page PNG renders are just upscales of these.
- Fig 4 "Final design": 3-D oblique contour sketch of the wave-basin model - a V / chevron with unequal arms. Oblique -> no scale, not traceable in plan. Qualitative only.
- Fig 7 "geographic location of the proposed reef": a plan map, printed ROTATED 90 deg (text "INDIAN OCEAN" rotated, "COTTESLOE" top-left, "MOSMAN PARK" top-right, roads/shore contours across the top, depth contours below, '+' grid marks, bold V outline with internal contour lines). Because Cottesloe lies north of Mosman Park and the ocean (west) is at the bottom of the figure, north points LEFT in the figure as printed (map rotated 90 deg counter-clockwise). The V apex points DOWN = OFFSHORE (west); the two arms sweep up toward shore. => resolves the previous run's open "apex direction" question (apex offshore). To be double-checked against satellite below.

## Fresh-agent run 2026-10-10 (queue item 9) - network blocked, local files only
Network check: raisedwaterresearch.com, services.arcgisonline.com, google.com unreachable (curl code 000). No satellite, Wayback or higher-resolution originals. Everything below uses repo files. Scripts (re-runnable from this folder, in order): scripts/trace_a2.py -> scripts/compute_shape.py -> scripts/make_overlays.py -> scripts/make_shape_json.py. Results: scripts/a2_trace.json, scripts/computed.json, scripts/p05_toe_pixels.json.

### Step 2 - Candidate images viewed (each once, downscaled)
- img-26 = Blacka et al. (2013) Fig A.2 'Cable Station ASR Design (After Lyons, 1992)', 917 x 682 px (added to the registry by the papers-intake agent on 2026-10-10 from papers/Review of artificial reefs ... 2013.pdf, p.93). The same CAD plan as the RWR image img-05 but about twice the resolution and with LEGIBLE labels: contours RL -1.00, -1.50, -2.00, -2.50; slope marks 1:20 (apex), 1:15 (right arm), ~1:13 (left arm); dimensions 40.0 m (centreline), 26.0 m (left transect), 30.0 m (right transect); radii R5 m, R7.82 m, R165 m, R187 m; 'REEF SETOUT LINE', 'INTERFACE LINE'; points P1, P2, P6, P7, IP3-IP9, TP1-TP6. Chosen PRIMARY.
- img-05 (RWR copy, 478 x 339): same drawing, labels illegible. Kept as an independent re-trace.
- img-06 (RWR 'extension'): same outline plus the hatched 'ADDITIONAL FILL AREA' triangle, text 'VOLUME = 320 m3, MASS ~ 688 tonne' (small).
- img-07 (Pitt sketch, scale bar 0-200 m, north arrow right, wave arrow from the top, existing contours 3.0-7.0 m, 'proposed contours in metres below low water mark (i.e. 0.0 on tide gauge)', '100 metres to sandy shoreline'): concept.
- img-20 (paper Fig 7, native 226 x 367, printed rotated): rotated 90 deg clockwise so INDIAN OCEAN reads upright: north up, west left, V apex pointing left (offshore).
- Not traceable: Fig 4 (oblique), Fig 3 / img-10 (section, no numbers), photos img-01..04 (reef submerged), img-24 (rock placement photo), img-25 (location map).

### Step 3 - Orientation (scale-free)
Apex offshore (Fig 7 labels; Pitt wave arrow). Sheet axes: north = right, offshore (west) = up (Pitt north arrow points right and its wave arrow comes from the top; Fig 7 arm bearings 40 / 47 deg agree with the A2 arms). On A2 the arms are 42.7 deg (south arm) and 44.7 deg (north arm) from the shoreline, the paper's 45 deg design peel angle (S1 p.2). South arm longer on all sheets. Shoreline taken as N-S (Fig 7: within ~5-8 deg; not measured).

### Step 4 - Scale of A2 (from the drawing itself, 6.51 px/m, sd 0.05)
1. Left transect printed '26.0 m': ends picked at (257,360) and (355,500) px = 170.9 px -> 6.57 px/m.
2. Right transect printed '30.0 m': ends (767,268) and (652,425) px = 194.6 px -> 6.49 px/m.
3. Centreline x = 560: dark lines at rows 154, 221, 286, 349.5 (RL -2.5, -2.0, -1.5, -1.0); spacing 65.2 px for 0.5 m at the printed 1:20 slope = 10 m -> 6.52 px/m.
4. Printed '40.0 m' between the set-out edge (row 91, RL -3.0) and the crest edge (row 349.5, RL -1.0) = 258.5 px (= 2 m at 1:20 = 40 m) -> 6.46 px/m.
Mean 6.51 px/m; allowance +-3% for picking. Picks are by eye at 4-5x zoom (crops with 10 px grid); scripts/trace_a2.py records them.

### Step 5 - Trace of A2
Outer foot ('interface line'): grey < 215, 5x5 closing, fill holes, 11x11 opening, 1 px erosion, marching squares, Douglas-Peucker 0.8 px -> 111 vertices. Overlay check: the outline follows the interface line within ~2 px (0.3 m). Design ramp (area between the two hatched rock bands, i.e. between the set-out line RL -3.0 and the crest line RL -1.0): dense-hatch mask (11x11 box density > 0.22) removed from the silhouette, 25x25 closing to absorb label notches -> 208 vertices, 3,113 m2.
Footprint 4,049 m2, bbox 121.2 x 76.3 m (alongshore x cross-shore). Text (Blacka Table 4.2 / RWR): 140 x 70 m -> -13% / +9%.

### Step 6 - Extension (img-06 -> A2)
Triangle picked in img-06 at 3x zoom: P2 tip (76.7, 190.0), P1 (165.0, 212.7), N (111.7, 248.3) (+-3 px). Registered onto A2 corners P2 (84, 467.5) and P1 (307.5, 546) by a 2-point similarity (scale 2.598 A2 px per img-06 px, rotation 4.9 deg). Triangle 347 m2 at 6.51 px/m; img-06 states 320 m3 -> 0.92 m mean fill. It sits at the end of the south (long) arm; dossier: 'extension of the reef's southern end' (R5). Built extent not documented; size rests on a low-resolution drawing.

### Step 7 - Independent checks
img-05 re-trace at an assumed 3.6 px/m (50 m grid guess): 4,209 m2, 123.1 x 77.8 m, +4% area vs A2 (A2 implies 3.39 px/m on that sheet, so the guess was 6% high). Fig 7 V (18 hand-picked vertices, 2 m/px = grid assumed 100 m): 122 x 76 m, 4,586 m2 (+13% area; dimensions within 1%): the independent agreement supports the 100 m grid reading and the 270 m offshore figure. Pitt concept (23 vertices, scale bar 0.855 px/m): 170 x 159 m, 10,619 m2: larger, symmetric, drawn 100 m off the shore, so not the built design.

### Step 8 - Canonical frame
x = (u - u_c)/6.51 (north = sheet right); y = 270 + (v_c - v)/6.51 (offshore = sheet up); (u_c, v_c) = centroid of the default polygon (A2 px 482.7, 337.2), placed 270 m offshore (Fig 7: centroid 271 m from the shore line with the 100 m grid; text 250 m S1 / 275 m RWR and Blacka). No rotation: sheet axes are the frame axes. Hand check: apex vertex (552.5, 49) -> y = 270 + (337.2 - 49)/6.51 = 314.3 m.

### Step 9 - Results
Default (design plan + extension): 4,355 m2, 121 x 89 m. Original: 4,049 m2, 121 x 76 m. Area range for +-3% scale: 4,105-4,629 m2. Confidence MEDIUM (reason in shape.json). Gemini: folder not in this repo, nothing used or checked.

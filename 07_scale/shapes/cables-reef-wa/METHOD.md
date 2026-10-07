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

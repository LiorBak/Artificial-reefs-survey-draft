# VERIFY - southern-ocean-surf-reef-albany (2026-10-10)

Status: verified (self-verification in the same run with recomputation; see check 8). Confidence: HIGH for position, orientation and length; area -30 % / +20 % (edge definition).
Full table is in shape.json "verification". Summary:

1. Overlays: re-rendered from shape.json and viewed. Satellite outline matches the dark wedge (1.5-4 m landward, soft offshore edge +-5-7 m); objective mask 99 % inside it (IoU 0.69). Design outline matches the outermost contour (about 2 m). Files: overlays/sat2026-01-20_trace.png, design_diagram_trace.png, canonical_versions_m.png, shoreline_fit.png, before_after_2025-01-16_vs_2026-01-20.png.
2. Design version: the Bluecoast final design is the built version (City page numbers equal the design table; satellite shape/orientation agree, rotation -3 deg, IoU 0.84). March 2026 rock repositioning (18 rocks) is after the image and is a note only.
3. Scale: sat 0.4891 m/px (georef); design 1.52 px/m (bar). Areas recomputed three ways; one vertex by hand; geom.py selftest PASS.
4. Dimensions: length 157 (sat) / 165 (design) vs 165 m; width 117 / 121 vs up to 110 m; crest bearing 281.5 / 278.1 vs 270-305 N. 140 m offshore not reproducible (reference line undefined): 71 m from the dry-sand edge, about 150 m from the vegetation edge. The figure's 110 m and 140 m arrows are not to the bar's scale.
5. Provenance complete; registry img-10 text said 54,000 m3 but the table reads 34,000 m3 (noted in the registry).
6. Gemini: unverifiable (network). Area 13,500 within 3 % of our design outline; orientation text unsupported. Not used.
7. Open: no measured as-built survey (City/Bluecoast/WA DoT) located; offshore toe edge soft; design position from the satellite fit.
8. Limitation: same agent traced and verified. A later independent look at a second dated image (Wayback intermediate releases, needs network) would help.

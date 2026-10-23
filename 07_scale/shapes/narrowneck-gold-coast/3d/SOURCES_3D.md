# SOURCES_3D - Narrowneck Reef 3D model: step log

Run started 2026-10-10 (stage 2, fresh agent, Sonnet 5.5). Inputs read: CLAUDE.md, _agent_briefs/common.md + model_3d.md, HANDOFF.md (stage 2 plan, sections 3 and 6), METHOD.md "INPUTS FOR 3D", VERIFY.md steps 6-9. Template: borth-coastal-defence-reef/3d (format only).

## CHECKPOINT 0 (2026-10-10) - plan
Frame = shape.json canonical (x alongshore bearing 356.2, y offshore bearing 86.2). z = 0 at MSL. Datum: z_MSL = z_AHD - 0.12 (MSQ). Versions: 5 from shape.json outline_versions, default photo_2020-08-08. Next: STEP 0 image checks (img-55 first), then seabed + reef surface build.

## STEP 0 + inputs (2026-10-10)
- img-55 (Corbett 2023 Fig 3, pre-works multibeam ICM 2017, 460 x 312 px native, map 352 px wide): scale bar ticks at x = 274, 295, 317 px = 0, 10, 20 m -> 0.4651 m/px (+-1.2 %); map covers 163.7 x 145.1 m. Colour bar -1 to -9 (tick labels at y = 140, 198, 253, 305 px; linear fit residuals 0.03, -0.23, 0.37, -0.17 m); depth read by HUE through the bar (prep_multibeam.py). Datum NOT stated; assumed AHD (the shallowest container tops read -1.8 (south arm) and -2.5 (north arm) vs measured crest -2.2 AHD: consistent).
- Registration of the figure (north-up, rotation 0) onto the traced arms by overlap of relief > 0.6 m: image centre = canonical (x -5, y 290) m, +-10 m (the score peak is broad: 0.52 vs 0.51 at 5 m offsets; the south arm fits best). Annotated: annotated/A1_corbett_fig3_digitised.png.
- img-31 (Vieira da Silva 2021 Fig 3, survey 1 = 19 Jul 2018, AHD, colour scale -10..8): viewed once; at the MPAR circle the bed is cyan (about -4 to -6), seaward dark blue (-7 to -9); nearshore yellow-green (-1 to -2) within about 100 m of the beach; consistent with the multibeam bed (-4 at the arm ends, -7 at the toe). Annotated: A3.
- img-04 / img-01 (Jackson 2012 Fig 2): right panel contours -2.50, -3.00, -3.50, -4.00, -4.50, -5.00, -6.00 and outer -8.00 (labelled; datum not printed on the figure); crest wedge -2.50 at the shoreward end of each arm. Used for the surface rule (crest loops + envelope). Annotated: A4.
- img-50 (Navionics SonarChart z18): contour labels read on the existing overlay (4.0 over arms, 5.5-6 around, 7, 8, 9, 10 seaward; LAT assumed): used for the seaward bed extension y 385-500 (+-15 m) only. The chart's land edge lies about 80 m seaward of the 2020-08-08 waterline in our frame, so its nearshore contours are NOT used. Annotated: A2. img-51 (nautical): spot depths 0.9 and 5.9 only; 0.9 not used (older crest state; Lior's reading pending).
- img-14 (Fig 9 sketch, T2 on 2 x T4): cross-section sketch, no dimensions; supports "two layers at the crest", not a height. img-24 (drone photo): planform and crest consistent with the model (arms converge seaward, surf peels from the north arm); no number read. img-01: same figure as img-04 (page render).

## CHECKPOINT 1 (2026-10-10) - model built
Files: prep_multibeam.py, nn_lib.py, build_3d.py (model.js 0.6 MB, docs.js), index.html (adapted from the Borth viewer: version selector + (i), datum-rule switch, other-outline overlays, photo match), make_previews.py (serves a copy with the vendored three.js; the sandbox cannot reach the CDN). Volumes (mound envelope, m3): photo 13.5k, Option 2 20.9k, 2004 13.8k, 2011 zone 6.9k. Next: annotated images, registry, METHODS_3D.md, docs.js rebuild, HANDOFF/STATUS/REQUESTS.

## CHECKPOINT 2 (2026-10-10) - documentation, registry, hand-over
- annotated/: A1 (Corbett Fig 3 digitised: bar ticks, colour-bar fit, registration, derived bed and relief), A2 (Navionics labels used / not used), A3 (Vieira Fig 3 reading), A4 (Jackson Fig 2 contour labels), A5 (profile: model vs sources), A6 (five versions on the model seabed). Previews: preview_oblique.png, preview_plan.png, preview_methods_panel.png (made by make_previews.py with the vendored three.js, own headless Chrome, random port, fresh profile).
- Registry (03_images/reefs/narrowneck-gold-coast): pending rows closed (img-01, 04, 14, 24, 31, 50, 51, 55 and img-69 from the papers intake); new rows img-75 (A5), img-76 (A6), img-77 (preview_oblique), img-78 (preview_plan); lines appended to NEW_IMAGES_LOG.md; check_registry.py: Narrowneck passes.
- img-69 (Blacka et al. 2013 Fig 5.1, surfer standing on the crest in a wave trough): qualitatively consistent with a crest 1.2-1.7 m below LAT; no value read.
- Navionics y-positions of the seaward labels corrected for the 3.8 deg frame rotation (7 -> y 402, 8 -> 411, 9 -> 474, 10 -> 514 m, +-20 m).
- Bugs fixed on the way: seabed blend used the array bounds instead of the valid map area (a -5 m dip at y 200 m); viewer AHD read-out under the papers' datum rule.
- Smoke test (own Chrome): all five versions load, datum switch, other-outline overlay, (i) pop-ups, no console errors.
- Done. Hand-over: HANDOFF.md top block; 3d/MAIN_TYPED_TEXTS.json.

## SOURCE AUDIT (2026-10-10, fresh agent) - documentation only
- METHODS_3D.md extended: 2b (how each source was used, accuracy, model element; id crosswalk to sources.md), 3.6 assumptions A1-A16 (effect, replacement), 3.7 other methods / AI involvement, 3.8 decisions (D7 by Lior, N1-N14), 6 confidence per element; citations completed (Corbett pp. 663-669 confirmed on the PDF; Vieira da Silva authors; Jackson 2007 Fall 2007; Blacka 2013 full citation); Black & Mead 2001 and the Jackson 2012 DOI listed as not confirmed.
- build_3d.py: versions_info says D7 decided; confidence text 18 Jul -> 19 Jul 2018 (Vieira da Silva AM p.8 line 176 and p.12 line 312); extra docs keys sources_use_md, assumptions_md, decisions_md (sections cut from METHODS_3D.md); index.html lists them as chips. model.js regenerated: only versions_info and confidence_3d.reason text differ (compared field by field with a build of the previous script); docs.js regenerated.
- Smoke test (own Chrome): Methods tab shows 5 chips, tables render, no console errors except favicon 404.

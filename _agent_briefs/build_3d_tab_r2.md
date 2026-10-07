# Brief: 3D models tab - round 2 UI changes (2026-10-07, Lior's review of round 9)

Lior's words (verbatim):
1. "should enabling exit full screen mode after getting in to it, and also easy going back to main page or switching tabs from all pages"
2. "photos should be write benith the 3d model, so one can view them alongside to it to see how model correspond to them. all of the
   text should apear later"
3. "In the top of the page there is too much text - shorten it and allow to read more by hovering some (i) or referencing to appendix
   tab or below section"
4. "Inside the tab, somewhere clear at the top, allow to switch between reefs. it should display one at a time. if you can add 'show all'
   that will show a 3d model of all combined so one can compare them this is good - and it should be another 'all' selection."

Start from 04_build\HANDOFF.md (module map, data flow, decisions) and 04_build\QA\round9_3d_LOG.md (last entries only). Same ground
rules as build_3d_tab.md: edit only 04_build\src\ (+ 04_build\data\ curated files), never 07_scale or 03_images; rebuild with
python src/build.py; python src/check.py; python src/qa_models3d.py --prefix round10_3d; own headless Chrome via src\qa_cdp.py.

## 1. Full screen and navigation everywhere
- "Full screen" uses the Fullscreen API on the viewer container (iframe + photo panel if feasible) with a visible "Exit full screen"
  button (top-right, always on top) + Esc; the button label/icon toggles. Test enter -> exit -> page intact.
- The standalone viewer pages (04_build\3d\<slug>\index.html, copied at build time) get an injected slim top bar: "<- Back to the page"
  (to artificial_reefs.html#view/models3d/<slug>) and links to the page's main tabs. Inject in the COPY only.
- The page's tab bar stays reachable from every view: sticky top navigation (does not scroll away), visible in every tab and dialog
  state; every dialog/lightbox has a visible close button + Esc. A "back to top" control on long views.

## 2. Layout of one model: viewer + photos together, text after
Order per model: compact header (name, state/date, confidence badge + one-line reason) -> VIEWER and PHOTOS side by side on wide
screens (viewer ~60 %, photo panel ~40 %; stacked on phones, photos directly under the viewer) -> everything else (key numbers, versions
table, texts relied on, methods, caveats) BELOW.
- Photo panel: a large view of the selected picture + a thumbnail strip (grouped by role, as now) right under/next to it. Clicking a
  thumbnail shows it in the panel next to the 3D model (not a modal that hides the model); the annotated-version toggle lives in the
  panel. Hover tooltip (how used + source) stays on thumbnails; the panel shows a short caption + "details" (i).
- Optional, if cheap: "camera hint" - if the registry row or SOURCES_3D.md gives a view direction (plan view / from the beach), a button
  that sets the viewer to the matching preset.

## 3. Less text at the top
- The tab intro (and the page's top header if it is long) becomes 1-2 short lines. Longer explanations move to (i) pop-overs (hover /
  click / keyboard) or to an "Appendix" (a section at the bottom of the tab or its own tab "Appendix: methods & references") with
  anchor links ("read more ->").
- Same rule inside each model section: long paragraphs collapse behind (i) or "more".

## 4. Reef selector + "All (compare)"
- A clear selector at the top of the tab (segmented buttons or a dropdown, with each reef's confidence dot): ONE model shown at a time;
  the URL hash follows it (#view/models3d/<slug>); default = the first built model; keyboard accessible.
- Last option "All (compare)": ONE combined three.js scene with every built model at the SAME scale, side by side along a shared
  shoreline (like the mega figure), each reef with its own seabed patch, z = 0 at each site's MSL, labels with name + confidence,
  default outline version where versions exist, shared vertical exaggeration slider (default 1x, always shown), water toggle, metre grid,
  50 m / 100 m scale bars, plan / oblique presets, and an "overlay" mode that stacks all reefs on one origin for footprint comparison.
- Geometry for the combined scene must be faithful to each model's own viewer (schemas differ per model). Preferred: at build time,
  load each copied viewer headless, export its reef and seabed meshes (three.js GLTFExporter, or a JSON of positions/indices) into
  04_build\3d\combined\<slug>.glb|json, and the combined viewer loads those. If a viewer does not expose its scene, inject a tiny hook
  in the COPY only. Document the method, and add a check that each exported reef's footprint area and crest z match model.js within
  tolerance (state it). If a model cannot be exported, show it as "not in comparison" with the reason.
- The combined view works from file:// (vendored bundle; no fetch of local files - embed the exported data as JS like model.js).

## Checks and docs
Extend qa_models3d.py: selector switches models (one visible), hash routing, fullscreen enter/exit, back-bar on standalone viewer,
sticky nav visible after scrolling, photo panel shows a clicked thumbnail next to the viewer, combined scene renders all models,
overlay mode, mobile layout. Screenshots round10_3d_* (overview, model with photo panel, fullscreen with exit button, combined, overlay,
mobile); VIEW them downscaled and fix. Update README.md, data\SCHEMA.md, HANDOFF.md (up to ~300 lines), STATUS entry, log every step
in 04_build\QA\round10_3d_LOG.md.

## Final JSON
{"html_path","size_kb","changes":["..."],"combined_models":["slug - exported ok|not"],"check_passed":bool,"screenshots":["..."],"limitations":["..."]}

# Brief: "3D models" tab in the page (added 2026-10-06 at Lior's request)

Lior's words: "update the 3d models in a new tab in the html, and below each model show the relevant pictures that were used to
construct it. hovering over the picture should display the method - how it was used, and its source. at the bottom of the page u may
add more methodological text, or text you relied on, caveats (like the differences in the volume between 3d model and report), and
references."

## Ground rules
- Edit only 04_build\src\ (new modules allowed, e.g. src\models3d.js + src\models3d.css, inlined by build.py; never hand-edit the
  generated artificial_reefs.html). Keep every existing tab working. Run compile_data.py -> build.py -> check.py -> qa_shots.py
  (--prefix round9_3d). Back up the current artificial_reefs.html to 04_build\QA\prev\ before the first rebuild.
- READ ONLY: every 07_scale\shapes\<slug>\3d\ folder and 03_images\reefs\ (other agents update them; your build copies them at build
  time, so a rebuild picks up later changes). Do not edit model.js, METHODS_3D.md, shape.json or images.json.
- DATA-DRIVEN: discover models at build time = every 07_scale\shapes\<slug>\3d\index.html + model.js (today: prattes-reef-el-segundo,
  boscombe-surf-reef, bunbury-airwave, palm-beach-gold-coast; Mount Maunganui, Borth, Narrowneck will follow). Reefs with
  3d\FEASIBILITY.md get a "not modelled - why / what is missing" card instead. Reefs with neither: "not yet modelled" (one line).
- Headless checks in YOUR OWN Chrome (random free DevTools port, fresh --user-data-dir under %TEMP%); never the shared browser pane.

## 1. Viewers, offline-safe
Copy each 3d\ (index.html, model.js, docs.js, annotated\ if the viewer references it) to 04_build\3d\<slug>\. Vendor three.js 0.170
(build/three.module.js + examples/jsm/controls/OrbitControls.js, plus any other addon a viewer imports) ONCE into 04_build\3d\vendor\
and rewrite each COPIED viewer's import map to the relative vendor path (originals untouched). Test one viewer from file:// AND via
python -m http.server.

## 2. The tab "3D models" (one section per model, in a sensible order: built models first, by name)
Per model:
- Header: reef name, state modelled (as-built + date, from model.js / METHODS_3D.md summary), confidence_3d badge + one-line reason
  ALWAYS visible, vertical exaggeration note.
- Viewer: an iframe created on click ("Load 3D model" button; lazy - never more than one or two live WebGL contexts; unload others),
  + "open full screen" link to 04_build\3d\<slug>\index.html.
- Key numbers table, from model.js provenance / METHODS_3D.md (each with its source id): crest level (and below LAT), seabed / toe
  depth, reef height, side slopes, footprint, volume - MODEL vs STATED IN SOURCES side by side with the difference, plus local tide
  levels (LAT, MSL, HAT/MHWS) with source.
- "Pictures used to construct this model" gallery, directly below the viewer, grouped by role: Plan shape / Crest & height /
  Seabed & depth / Tides & datum / Validation & cross-checks / Flagged, not yet checked (for_3d_check.pending true). Picture set =
  registry rows (03_images\reefs\<slug>\images.json) whose used_for has a 3d_* / scale / plan_trace / camera_match role, or whose
  linked_records point at 3d\SOURCES_3D.md / model.js provenance, plus every 3d\annotated\ image (it is registered; match by file).
  Thumbnails 400 px and web copies <= 1600 px in 04_build\assets\images\<slug>\ (never inline image bytes; lazy-load).
  HOVER (and keyboard focus / tap on touch) shows a tooltip: "How it was used:" how_used (+ the model value it gave, if any) and
  "Source:" the full citation with credit, date and licence. CLICK opens a lightbox: large image, annotated-version toggle when
  annotated_files exist, full citation, source-page link, image link, rights_note, what it shows, for_3d_check status/result.
- "Methods, sources & uncertainty" collapsible: the rendered METHODS_3D.md + SOURCES_3D.md (pip install markdown; pre-render at
  build time), and REQUESTS_FOR_LIOR.md as "Open questions / what would resolve them".

## 2b. Outline / model versions (added 2026-10-06, Lior)
If a model.js has "versions" (+ default_version, versions_info) - Borth first, others may follow - show the default, a version
toggle with meaningful names + dates in the section header, and an (i) icon that opens a pop-up with versions_info and a table
(name | date | source | footprint | volume). Switching the toggle tells the iframe which version to show (postMessage or URL hash
#version=<id>, whichever the viewer supports) and updates the key-numbers table. The caveats table lists the version differences.

## 3. Bottom of the tab - academic apparatus (write it from the documents; do not invent; cite everything)
a. Methods (project-wide, ~1-2 pages): canonical frame (x alongshore, y offshore, z up, z = 0 at MSL; the left-handed frame and the
   three.js mapping), plan shape from verified traces, crest/toe lofting and slope rules, seabed construction (survey figures, Navionics
   SonarChart / chart readings, thin-plate spline etc. as each model did), datum handling with the equations actually used, e.g.
   z_MSL = z_AHD - (MSL - AHD); Pratte's z_MSL = z_MLLW - 0.849 (NOAA 9410840); Boscombe z_MSL = z_ACD - 1.40 (NTSLF);
   Palm Beach MSL = LAT + 0.88, HAT = LAT + 2.03 (MSQ 2026); the Navionics datum inference by RMS against an independent survey;
   uncertainty propagation; the confidence rubric; what vertical exaggeration does.
b. Texts we relied on: per model, the key quotations (<= 25 words each) with page numbers and links that fix crest, height, volume,
   dates and state (from SOURCES_3D.md / METHODS_3D.md).
c. Caveats and discrepancies - one table across models: model | quantity | our model | stated in source (citation) | difference |
   likely reason | status / what would resolve it. Must include at least (verify each number in the documents first):
   - Palm Beach: model envelope ~22,000 m3 and height 3.9 m vs council register VOLUME 33,000 / HEIGHT_M 5 (units unexplained);
     chart "FISH HAVEN 1.5MT" vs design crest (0.88 m datum ambiguity); concept design (53,319 m3, Mortensen 2015) is not the built reef.
   - Pratte's: model 443 m3 vs 695-782 m3 (110 bags at 80-90 % fill) / 869 m3 nominal - bag courses unknown; position +-100 m;
     crest A (design) vs crest B (6 ft MLLW).
   - Boscombe: loft 13,119 m3 vs ~13,000 m3 stated (agreement); Fig 9 zero assumed chart datum (ODN would shift 1.4 m); EMODnet
     1.8 +- 0.7 m deeper than the model seabed (07_scale\bathymetry\emodnet\REPORT.md section 6).
   - Bunbury: installed bladder torn before completion (verdict FAILED); Waveco's "2018" date rejected; crest 0.69 +- 0.66 m below MLLW.
   - Any further discrepancy listed in a METHODS_3D.md section 4/5/7, and later models' ones automatically (parse or curate per model
     in a small 04_build\data\models3d_caveats.json you write, each row with source ids).
d. References: one merged, de-duplicated author-year list from all METHODS_3D.md / SOURCES_3D.md reference sections (+ the
   bathymetry reports), with links; each model section links into it.

## 4. Checks (extend check.py)
Every discovered model has a section; every gallery picture's file exists in assets; every tooltip has non-empty how_used and
citation; the vendor three.js exists and no copied viewer still points at a CDN; the confidence badge renders per model; page size
(warn > 15 MB). Screenshot the tab (overview, one gallery hover with tooltip, one loaded viewer) into 04_build\QA\round9_3d_*.png,
VIEW them, fix until right. Document in 04_build\README.md (section "3D models tab") and 04_build\data\SCHEMA.md.

## Final JSON
{"html_path","size_kb","models_shown":["slug - confidence"],"pictures_per_model":{"slug":n},"caveats_rows":n,"references":n,
"check_passed":bool,"screenshots":["..."],"limitations":["..."]}

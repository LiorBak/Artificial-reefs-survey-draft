# Brief: 3D model of ONE reef with three.js (slug given in your prompt)

Lior's words: "draft it in 3D with three.js - only the reef, the ocean floor and the ocean height, no coastal buildings. Make sure to
specify what source and what info from the source you used (if the source is an image, also draw on it to show the source, how water
depth was estimated, and so on). The 3D model will also help estimate camera angles when aligning photos. If agents struggle to find
depth info in our sources, leave it to me (Google Earth, an ocean-depth scanning app)."

Inputs: the VERIFIED plan shape 07_scale\shapes\<slug>\shape.json (+ METHOD.md, VERIFY.md, sources.md, src\), the card and dossier
02_research\reefs\<slug>.*, the earlier footprint 07_scale\reefs\<slug>.* (crest depth, offshore distance, volumes), and the sources they cite.
Tools: 07_scale\tools\ (overlay.py for annotating images; geom.py - its make-canonical rotation was buggy before 2026-10-05, see README).
Work folder: 07_scale\shapes\<slug>\3d\  (create it).

## RESUME RULE
Earlier runs may have been cut off by a usage limit. If 3d\ already holds SOURCES_3D.md, model.js, annotated images or a partial
index.html, read them first and continue from where they stop; re-check any value you keep (it must have a source line in SOURCES_3D.md).

## CHECKPOINT RULE
FIRST create 3d\SOURCES_3D.md (heading + "Run started <date>") and append after every step. Write files as soon as each part exists.

## LIOR'S DECISIONS (2026-10-05)
- STATE: model the AS-BUILT state (or the drawn design version if no as-built exists). Later changes (damage, deflation, collapse,
  removal, renewal) go in the viewer caption and in METHODS_3D.md with dates and sources - not modelled as a second state.
- NO Haifa/Israel tide preset - local tides only.
- NAVIONICS: try the Navionics web chart yourself (Garmin Navionics ChartViewer, e.g. https://webapp.navionics.com/ - nautical chart
  and SonarChart layers) in YOUR OWN headless Chrome (never the shared browser pane). Zoom to the reef; screenshot; read the depth
  contours / soundings at the toe, offshore, and over the reef. Record: layer (chart vs SonarChart), the app's stated depth datum
  (if not stated, say so and state your assumption), contour interval, access date; credit "Garmin Navionics, not for navigation",
  private research copy. Save the screenshot to 3d\annotated\ with what you read marked on it, and add it as a source in model.js
  provenance and METHODS_3D.md.
  * If the STRUCTURE STILL EXISTS (not removed or ruined), check whether the reef shows in the contours / SonarChart and use it as an
    extra source for crest depth and reef height (cross-check vs the design figures; report the difference).
  * If the reef was removed or ruined, use Navionics for the seabed only and say why.
  * If the app needs a login, is blocked or shows a CAPTCHA: do NOT bypass it. Move the reading into the requests for Lior (below).
  * TIP from the Pratte's run (2026-10-05): webapp.navionics.com redirects to https://maps.garmin.com/en-US/marine/; it opened with no
    login; zoom 18 max; layers "SonarChart Maps" and "Nautical Charts"; units feet. The app states NO datum and NO contour interval -
    infer the interval from the shading bands, and test candidate datums (MLLW/LAT/MSL/NAVD88/AHD/CD...) against an independent DEM or
    survey along one transect by RMS (see prattes-reef-el-segundo\3d\METHODS_3D.md section 3.5 and nav_annotate.py / reef3d_lib.py,
    which you may reuse).
  * HEADLESS CHROME ISOLATION (2026-10-05 incident: an agent's fixed DevTools port 9341 hijacked another agent's tab): ALWAYS pick
    a free remote-debugging port at random (e.g. bind a socket to port 0, or 9400-9999 after checking it is free) AND a fresh
    --user-data-dir under %TEMP% unique to your run; never attach to a port you did not launch. If your own tab suddenly shows
    something you did not load, re-navigate it.
- REQUESTS FOR LIOR (he will use BOTH the Navionics app and Google Earth Pro): whatever you could not read, list it in
  3d\REQUESTS_FOR_LIOR.md as a table: tool (Navionics app / Google Earth Pro) | exact lat/lon (decimal, WGS84) or place | what to
  read (depth at point, contour value, ruler distance, historical imagery date) | datum/units to note | why it matters for the model.
  Keep building with stated assumptions where possible; do not wait for him.

## STEP 0 - IMAGE REGISTRY CHECK (added 2026-10-06)
Read 03_images\reefs\<slug>\images.json (convention: _agent_briefs\image_registry.md). VIEW every image whose
for_3d_check.pending is true (and any with structure_visible true that your sources do not already cover). For each: confirm or
contradict the model value it bears on (crest, seabed, planform, volume, tides), annotate it into 3d\annotated\ if you read a value off
it, record the result in METHODS_3D.md section 4 (Validation) with the registry id, add it to model.js provenance if used, and set
for_3d_check.pending false with a "result" line in the registry row. Register every new image you make or find (common.md rule 6).
If the model is already built (re-check run), do only this step plus the documentation updates it requires, and rebuild with build_3d.py.

## OUTLINE VERSIONS (added 2026-10-06, Lior)
If shape.json has outline_versions (07_scale\SHAPE_SPEC.md "Outline versions"), build the reef for EACH version, default =
default_outline (measured survey > design drawing > photo trace). model.js gets "versions": [{id, name, date, source_ids, method,
reef mesh data, volume_m3, area_m2}] + "default_version" + "versions_info". The viewer shows a version selector (meaningful names
with dates) with an (i) icon next to it that opens a pop-up: versions_info + a table (name | date | source | footprint | volume).
METHODS_3D.md section 4 compares the versions.

## STEP 1 - FEASIBILITY (decide before building)
List what the sources give for each input, with source + quote/figure + value + uncertainty:
 a. plan shape (from shape.json canonical - already verified);
 b. crest elevation / crest depth below a stated datum, and its variation (e.g. apex shallower than arms);
 c. reef height above the seabed, side slopes (rock 1:1.5-1:2, stacked bags, inflatable dome profile...), layers;
 d. seabed depth around the reef: depth at the toe, nearshore profile (depth vs distance offshore), contours from a survey or design figure,
    or a published beach slope. Public bathymetry may help (e.g. EMODnet for UK, AusSeabed / council LiDAR for Australia, NOAA for the US,
    LINZ for NZ) - only if you can actually read a value for this site; GEBCO is too coarse for a reef this size - say so if it is all there is;
 e. water level datums at the site: MSL, LAT / MLLW, MHWS / HAT or the spring tide range (tide tables, port authority, papers).
Decide: BUILD if a, b and d are sourced (c and e may be estimated with stated assumptions). Otherwise write 3d\FEASIBILITY.md with
"what we have" and "what is missing" in plain language for Lior (he can help with Google Earth and a depth-sounding app), and STOP
without building.

## STEP 2 - SHOW THE SOURCES ON THE SOURCES
For every image-derived input, save an annotated copy to 3d\annotated\ that marks exactly what was read: e.g. the contour lines and their
labels highlighted, the cross-section line drawn on the plan, the scale bar ticks, the point where a depth sounding was read, the tide
gauge reading. Caption each in SOURCES_3D.md. Text-derived inputs get a quote (<= 25 words) and the URL.

## STEP 3 - MODEL DATA
Write 3d\model.js as  window.REEF_MODEL = {...}  (a JS file so the viewer works from file:// without fetch). Frame: the canonical frame of
shape.json (metres; x alongshore, y offshore) with z up, z = 0 at MSL. Contents: seabed (a heightfield grid or profile + contour
interpolation, with its extent), reef (crest polygon(s) with crest z per vertex or region, toe polygon, side-slope rule, layers if any),
water levels {MSL: 0, LAT/MLLW: z, MHWS/HAT: z, label + source each}, shoreline line (y = 0), north arrow direction (from shape.json geo or
the source's north arrow), and a "provenance" array {parameter, value, unit, source_id, method, uncertainty, estimated: bool}.
Also a "confidence_3d": {level high|medium|low, reason (1-2 plain sentences)} - separate from the plan-shape confidence.

## STEP 4 - VIEWER 3d\index.html (stands alone; no source images inside it)
three.js via an import map from https://cdn.jsdelivr.net/npm/three@0.170.0/ (build/three.module.js + examples/jsm/controls/OrbitControls.js);
<script src="model.js"></script> before the module script. Scene: seabed mesh (shaded by depth), reef mesh (extruded / lofted from crest
and toe outlines; colour by material), translucent water surface at the selected level, metre grid, 10 m and 50 m scale bars, north
arrow, shoreline line. Controls: orbit / pan / zoom; water level slider (LAT -> HAT) with the datum labels; vertical exaggeration
(1x-5x, default 1x, always shown on screen); toggles for water, seabed, reef, labels; a camera readout (position, heading, pitch,
field of view) and presets (plan view, along-crest, from the beach at eye height 1.7 m). If feasible: a "photo match" mode - load a local
image file as a semi-transparent overlay on the canvas and adjust camera position / heading / pitch / FOV with sliders to line the model
up with the photo, then copy the camera parameters (for later alignment work). A side panel lists the provenance table and confidence_3d
with its reason. No coastal buildings.

## STEP 5 - CHECK
Render it headless (Chrome or Edge: --headless=new --use-angle=swiftshader --enable-unsafe-swiftshader --screenshot ... --window-size=1400,900;
serve the folder with python -m http.server on a free port 8800-8899) into 3d\preview_plan.png and 3d\preview_oblique.png (use URL hash
parameters for camera presets if needed); VIEW them with Read; fix until the reef, seabed and water render and the scale is right.
Do not use the shared browser pane (other agents use it).

## STEP 6 - ACADEMIC-LEVEL DOCUMENTATION (added 2026-10-05 at Lior's request)
Write 3d\METHODS_3D.md as a self-contained methods note a reviewer could reproduce, in this order:
 1. Summary (3-5 sentences: what was modelled, state/date represented, confidence_3d level and why).
 2. Data sources - full citations in author-year style (author/organisation, year, title, publisher/venue, URL, accessed date, licence),
    with what each contributed and its resolution/date.
 3. Methods - each processing step in reproducible detail: coordinate frame and datum conversions (write the equations, e.g.
    z_MSL = z_AHD - (MSL - AHD); depth below LAT; pixel -> metre transforms), seabed interpolation method, reef surface construction
    (crest/toe lofting, slope rule), every assumption stated explicitly and numbered (A1, A2, ...).
 4. Validation - cross-checks performed and their numbers (e.g. implied toe depth vs survey, volume implied vs stated volume).
 5. Uncertainty - per input: range or +/-, and how it propagates to crest depth below LAT / reef height (simple propagation is fine;
    show the formula); what the vertical exaggeration does.
 6. Confidence - the level and a paragraph of justification against the rubric.
 7. Limitations and unknowns - what is missing, what would resolve it (and which of those Lior could supply: Google Earth history,
    a depth-sounding app reading, a tide table), and how each gap could bias the model.
 8. References - consistent author-year list.
Make it readable INSIDE the viewer: build_3d.py (or equivalent) writes 3d\docs.js as  window.REEF_DOCS = {"methods_md": "..."}  (the
markdown of METHODS_3D.md, plus SOURCES_3D.md) and index.html gets a "Methods & sources" panel/tab that renders it as HTML (a small
markdown-to-HTML routine in the page, or pre-rendered HTML in docs.js). Keep the confidence badge + one-line reason always visible.
Provide build_3d.py so model.js and docs.js can be regenerated from shape.json and the source notes if the plan shape changes later.

## Final JSON
{"slug","built":bool,"confidence_3d","confidence_3d_reason","inputs":{"plan","crest","height_slopes","seabed","tides"} (each: "sourced|estimated|missing - short note"),
"missing_for_lior":["..."],"files":["paths"],"camera_match_mode":bool}

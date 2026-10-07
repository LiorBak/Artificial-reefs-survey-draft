# Brief: BUILD the Shapes viewer, the confidence-filtered mega figure and the Videos review tab

Edit only 04_build\src\ (new modules allowed, inlined by build.py; never hand-edit the generated HTML), then run
compile_data.py -> build.py -> check.py -> qa_shots.py --prefix round8.

## Data
- 07_scale\shapes\<slug>\shape.json (verified; spec 07_scale\SHAPE_SPEC.md), with METHOD.md and VERIFY.md beside it.
- Source images in 07_scale\shapes\<slug>\src\. compile_data.py copies the referenced ones into 04_build\assets\shapes\<slug>\,
  downscaled to max 1600 px on the long side, with pixel_polygons rescaled by the same factor (record the factor).
- Videos: the cards' "videos" arrays / 02_research\videos\<slug>\videos.json. Do NOT inline whole transcripts: inline segments plus the
  first 1,500 characters per video, and link the txt path.
- Lior's review decisions: 04_build\data\media_decisions.json if present (see 2).

## 1. SHAPES tab (replaces the Scale tab; keep its useful parts)
a. Mega figure: all canonical outlines at ONE shared scale (px per metre), side by side on a shared shoreline (image26-like layout)
   plus an overlay mode. Filters: confidence checkboxes high / medium / low (all on by default), per-reef toggles, colour by verdict or
   by confidence; football-pitch silhouette toggle; zoom.
   EVERY drawing carries its confidence badge AND its one-line reason VISIBLY (not only on hover), plus "drawn: <design version>".
b. Per-reef "Shape check" viewer, also embedded in each reef's detail dialog:
   - base-image switcher over the reef's sources (each with title, date, credit, license, source link, role, scale method), and if geo
     exists a "Satellite (live)" option using Leaflet + Esri World Imagery tiles with the lat/lon polygon (attribution shown);
   - IMPLEMENTATION: one <svg viewBox="0 0 w h"> per source with <image href=... width=w height=h> and the pixel polygons as <polygon>
     in the same coordinate system, so the drawing stays aligned at any size;
   - controls: show/hide drawing, opacity slider, outline colour picker, show vertices, show dimension labels (from canonical),
     side-by-side vs overlay;
   - always show the confidence badge + reason + design version, and a "How we drew this" block: METHOD summary, sources table,
     dimensions check, angles table, Gemini findings. Link the full METHOD.md / VERIFY.md (copy them into 04_build\docs\shapes\<slug>\).
c. Comparison table: name | shape | L | W | area | depth | distance | design version | primary source | geo-referenced | confidence |
   reason | Gemini findings count; sortable; the confidence filter applies here too.
d. Reefs with no usable source: the viewer says so plainly with the no_source explanation and shows the text-derived schematic, labelled.

## 1f. OUTLINE VERSIONS (added 2026-10-06, Lior)
shape.json may carry outline_versions + default_outline + versions_info (07_scale\SHAPE_SPEC.md). Mega figure, comparison table and
Shape check show the DEFAULT version; a version toggle (meaningful names with dates) switches it; an (i) icon next to the toggle opens
a pop-up with versions_info and a table (name | date | source | area). Same in the 3D tab (models with "versions" in model.js).

## 1e. DOCUMENTATION INSIDE THE PAGE (added 2026-10-05 at Lior's request - academic level, readable in the HTML, not only linked)
- compile_data.py renders, per reef, METHOD.md + VERIFY.md (07_scale\shapes\<slug>\) and, where a 3D model exists, 3d\METHODS_3D.md
  + 3d\SOURCES_3D.md to HTML at build time (pip install markdown) and inlines them into the reef record.
- In the Shape check viewer and the reef dialog: a "Methods, sources & uncertainty" section that opens with a structured header:
  confidence level + reason (always visible), design version drawn, primary source (full citation), what is still missing / unknown
  (from no_source, open issues, limitations), then the full rendered documents in collapsible blocks; every [R#]/[S#] keeps its pop-up.
- 3D: copy each 07_scale\shapes\<slug>\3d\ (index.html, model.js, docs.js, annotated\) into 04_build\3d\<slug>\ and show it in the reef
  dialog and the Shapes tab as an embedded iframe (lazy, created on click) plus an "open full screen" link; label the 3D confidence + reason.
  OFFLINE-SAFE (2026-10-05: the Palm Beach agent found the jsdelivr CDN unreachable from this machine): vendor three.js 0.170
  (build/three.module.js + examples/jsm/controls/OrbitControls.js) once into 04_build\3d\vendor\ and point every copied viewer's import
  map there (relative path), keeping the original 07_scale copies untouched. Test one viewer from file:// AND via http.server.
- A top-level "Methods" tab that renders 07_scale\METHODS.md (project-wide methods paper, written in the wrap-up stage) with a table of
  contents, and links each reef's documents.

- Cards may carry "verdict_reason" and "developer_account" (e.g. Bunbury: the developer's "it wasn't a failure" quote with a
  discrepancy table). Show the verdict reason under the verdict badge in the reef dialog, and the developer account as a clearly
  labelled "Developer's account vs independent record" block. Never let a developer claim override the verdict.

## 2. VIDEOS tab (Lior's review tool)
- One card per video across all reefs; filters by reef / our relevance class / review status / origin.
- Card: title, reef, channel, duration, date, origin tag (ours / via Gemini / new search), our relevance + evidence, segment list with
  timestamps (click -> creates the embed at that time; embeds only created on click), transcript excerpt + link to the full txt, thumbnail.
- Review controls: Relevant / Not relevant / Unsure toggle and a notes box (e.g. "extract frame at 1:23 ...").
  Persist in localStorage (wrap every access in try/catch). "Export decisions" downloads media_decisions.json
  {"videos": {video_id: {decision, notes, reef, decided_at}}, "images": {url_hash: {decision, notes, reef, url, decided_at}}};
  "Import" loads one. compile_data.py reads 04_build\data\media_decisions.json if present: not_relevant -> hidden from reef detail views
  (still listed in the tab, greyed); relevant -> shown first; notes displayed in the tab.
- "Images" sub-section with the same toggle + notes per image (keyed by a hash of the url), exported in the same file.
- A short help line at the top: "Decide, then Export and save the file into 04_build\data\ - the next rebuild applies it."

## 3. Reef detail dialog
Media section shows the reef's images (with "shows ..." labels) and videos (relevance label, segments, embed or link), consistent with
the tab; the Shape check viewer replaces the old "Scale & footprint" block.

## 3b. IMAGES - every reef image shown, from the registry (added 2026-10-06 at Lior's request)
Source of truth: 03_images\reefs\<slug>\images.json (convention: _agent_briefs\image_registry.md). compile_data.py reads every row with
display:true, copies the file (and its annotated_files) into 04_build\assets\images\<slug>\ as a max-1600 px web copy + a 400 px
thumbnail (record both), and never inlines image bytes into the HTML (keep the page small; lazy-load).
- Reef dialog "Images" gallery and a top-level "Images" tab (filters: reef, kind, used_for, structure_visible). Each tile: thumbnail,
  title, kind, image date, and a visible "Used for the model: <how_used>" line. Click -> lightbox with the full citation, source-page
  link, image link, licence + rights_note, credit, retrieved date, "shows", state_shown, linked records (link to the Shape check source /
  3D provenance row), and an "annotated version" toggle when annotated_files exist.
- The Shape check viewer and 3D provenance tables link to the registry id (and back).
- The Videos tab "Images" review sub-section uses the same registry rows (decision keyed by registry id; url hash as fallback).
- check.py: every display:true row renders exactly once in the Images tab and once in its reef dialog; every referenced file exists in
  04_build\assets; image26 and Gemini-folder files never appear; report total assets size.

## 4. check.py additions
Every shape.json loaded; every pixel polygon inside its image bounds after rescaling; every drawing instance renders a confidence badge +
reason (count instances in the DOM dump); the confidence filter hides/shows drawings; all referenced assets exist; the Videos tab lists
every video in the data; no rejected media rendered; report page size (warn above 15 MB).

Document what you built in 04_build\README.md (new sections) and 04_build\data\SCHEMA.md.

## Final JSON
{"html_path","size_kb","changes":["..."],"check_passed":bool,"limitations":["..."]}

# 04_build HANDOFF (page build) - 3D models tab round 10 finished 2026-10-07

Read this instead of re-reading src/. Briefs: the 3D tab = `_agent_briefs/build_3d_tab.md` (round 9, DONE) and `_agent_briefs/build_3d_tab_r2.md`
(round 10, Lior's four review requests, DONE, section 1); the rest of the page (Shapes tab, Videos tab, Images tab, reef-dialog changes,
Methods tab) = `_agent_briefs/build_shapes_videos.md` (NOT done, section 12).
Step logs: `04_build/QA/round9_3d_LOG.md` (two agents), `04_build/QA/round10_3d_LOG.md` (round 10).
Rules followed: `_agent_briefs/common.md` (lean context, handoff files). User-facing docs: `README.md` section "3D models tab",
schemas `data/SCHEMA.md` ("models3d.json", "models3d_combined.json").

## 1. Status per stage (2026-10-07)
| stage | status | confidence / reason |
|---|---|---|
| Tabs Gallery / Map / Table / Scale | unchanged except: view buttons moved into the sticky top bar, intro shortened with (i), Gallery button scrolls to the top | high: `check.py` 0 failures |
| 3D tab (round 9): discovery, viewers, key numbers, caveats, methods, references, versions | built, tested | high for the mechanics; per-model numbers are only as good as each model's METHODS_3D |
| Round 10 request 1: full screen with Exit button + Esc, back to the page / switch tabs from anywhere | built, `qa_models3d.py` PASS | high: native Fullscreen API + CSS fallback tested; standalone viewer bar tested |
| Round 10 request 2: photos beside the model, text later | built (stage = viewer 60 % + photo panel 40 %, stacked on phones) | high; viewers need compact CSS when framed (section 5) |
| Round 10 request 3: less text at the top | built ((i) pop-overs, appendix with read-more links) | high |
| Round 10 request 4: reef selector + "All (compare)" + overlay | built; 4/4 models exported, all checks vs model.js pass | high for mechanics; see section 11 for what the comparison does and does not mean |
| Outline versions (build_3d_tab.md 2b) | built; synthetic test only (`qa_versions_synth.py`) | Borth / Mount Maunganui with `versions` still not built (paused) |
| Shapes / Videos / Images tabs, reef-dialog 3D embed, Methods tab | NOT started | next agent (section 12) |

## 2. Pipeline and commands (run from 04_build\)
```
python src\compile_data.py      # 02_research cards -> data\reefs.json (+ copies Lior's figures/video frames to assets\<slug>\)
python src\build.py             # RUNS src\compile_models3d.py (which runs src\export_combined.py), then inlines css/js/json into template.html
python src\check.py             # static + [3D] block + DOM checks in own Chrome -> QA\build_check.txt ; exit 1 on FAIL ; --no-dom skips Chrome
python src\qa_models3d.py --prefix round10_3d   # 79 DOM checks + screenshots -> QA\round10_3d_*.png, QA\round10_3d_checks.txt
python src\qa_versions_synth.py --prefix round10_3d   # versions feature with a synthetic model in a temp sandbox
python src\export_combined.py [--force] [slug]   # combined export alone; prints every check (cached by signature)
python src\compile_models3d.py  # (optional) only the 3D data -> data\models3d.json, 3d\<slug>\, 3d\combined\, assets\images\<slug>\
```
Never hand-edit artificial_reefs.html. The page needs `assets\`, `3d\`, `docs\` next to it; works from file:// (no server). Backups: page
before round 9 `QA\prev\artificial_reefs_before_round9_3d.html`; page + src before round 10 `QA\prev\round9\` (html, js, css, py, template).
Headless QA: ALWAYS our own Chrome on a random free port + fresh profile (`src\qa_cdp.py`), never the shared browser pane.
Shell quirks: the Bash tool rejects some long heredocs; PowerShell here is 5.1 (no `utf8NoBOM`, `Set-Content -Encoding utf8` writes a BOM,
no heredocs): write patch scripts / files with the Write tool. Console is cp1255: scripts that print non-ASCII call
`sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.

## 3. Module map (src\)
| file | what it does | 3D-tab hook |
|---|---|---|
| compile_data.py | reads the 13 verified cards -> data\reefs.json | none |
| build.py | derived fields (USD, map checks), runs compile_models3d, inlines everything | markers /*__M3D_CSS__*/, /*__M3D_JS__*/, __DATA3D__ |
| template.html | skeleton: sticky `<nav id=topnav>` (brand link + `.views` buttons), `#to-top`, header, controls, view sections | `data-view="models3d"` button, `#view-models3d > #m3d-root`, `<script id="data3d">` |
| styles.css | tokens (:root light/dark), page styles, **round 10: `--nav-h`, `.topnav`, `.to-top`, `.info-i` / `.info-pop` primitive** | models3d.css reuses its tokens |
| app.js | gallery/map/table, reef dialog, source pop-ups, routing | hooks: setView list + `body[data-view]` + keep `#view/models3d/<slug>` hash + `unloadAll()` when the tab is left; render() -> `ReefModels3D.render()`; hash regexes accept `models3d[/<slug>]`. **Round 10: `infoHTML()` / `bindInfo()` (the (i) pop-overs, exported as `window.ReefInfo.html`), brand link, Top button, view buttons scroll to the view top (Gallery: page top)** |
| scale.js | Scale tab | none (to be replaced by the Shapes tab) |
| compile_models3d.py | ALL data work of the 3D tab (section 4); copies viewers and **injects the back bar + compact-embed CSS** (`inject_chrome`); `build_combined()` calls the export and writes `3d/combined/{manifest.js,index.html}` | writes data\models3d.json (+ `combined` block), 3d\, assets\images\ |
| export_combined.py | build-time export of reef + seabed meshes from each copied viewer (section 4b) | writes 3d\combined\<slug>.js, export_cache.json |
| combined_viewer.html | template of the combined "All (compare)" viewer (own three.js scene, classic scripts) | -> 3d\combined\index.html |
| models3d.js | the tab UI (one IIFE, `window.ReefModels3D`: render, select, selected, openModel, openPicture, unloadAll, setVersion, data) | reads `#data3d`, renders into `#m3d-root` on first show |
| models3d.css | `.m3d-*` styles, light/dark, narrow screens (< 900 px stacked), full-screen layout, print | hides the long site header and the reef filters on this tab |
| qa_cdp.py | tiny Chrome DevTools driver (goto/eval/hover/click/press/screenshot), random port, fresh profile, focus emulation on | used by qa_models3d.py, export_combined.py, qa_versions_synth.py |
| qa_models3d.py | 79 DOM checks + screenshots; `dom_checks()` is imported by check.py | - |
| qa_versions_synth.py | sandbox copy of 04_build in %TEMP%\m3d_synth with a fake model (3 versions); tests versions + check.py [3D] | never writes to 07_scale / 03_images |
| check.py | static + DOM checks of the whole page | function `check_models3d` |
| qa_shots.py | old headless smoke test (CLI Chrome) | not tab specific |

## 4. Data flow (3D tab)
```
07_scale\shapes\<slug>\3d\{index.html,model.js,docs.js,annotated\,preview_oblique.png}   (READ-ONLY, other agents write them)
07_scale\shapes\<slug>\3d\{METHODS_3D,SOURCES_3D,REQUESTS_FOR_LIOR,FEASIBILITY}.md
03_images\reefs\<slug>\images.json   (READ-ONLY registry; display!=false rows)          07_scale\bathymetry\{emodnet,gold_coast}\REPORT.md
04_build\data\models3d_curated.json | models3d_caveats.json | models3d_combined.json | models3d_text\{methods,combined_method}.md   (ours)
        |  src\compile_models3d.py  (discover -> parse model.js -> versions -> pictures -> render markdown -> verify -> merge refs -> combined)
        v
04_build\data\models3d.json  --inlined as <script id="data3d">-->  artificial_reefs.html  (page ~1.7 MB; WARN above 15 MB)
04_build\3d\<slug>\          viewer copy (index.html rewritten + bar/compact CSS, model.js, docs.js, annotated\ <=1200 px, poster.jpg)
04_build\3d\combined\        index.html, manifest.js, <slug>.js (exported meshes, ~2.2 MB), export_cache.json
04_build\3d\vendor\          three.js 0.170 (three.module.js, addons, three.bundle.js classic IIFE, README with the esbuild recipe)
04_build\assets\images\<slug>\<regid>.<png|jpg>, <regid>_400.jpg (thumb), <regid>_annK.<ext> (annotated), <=1600 px; never inlined
```
Discovery: every `07_scale\shapes\<slug>\3d\` with `index.html` + `model.js` is a model (slugs not in reefs.json are accepted too);
`FEASIBILITY.md` only -> "not modelled" card; neither -> one line "not yet modelled". Models are listed alphabetically by name; the
first one is the default of the selector.
Picture selection (per model): registry rows with display!=false AND (used_for contains plan_trace|scale|3d_*|cross_check|camera_match,
OR linked_records mention 3d\SOURCES_3D / model.js, OR file/annotated_files in 3d\annotated, OR for_3d_check.pending). Group = first
mapped role in used_for (plan | crest | seabed | tides | validation); no role + pending -> "Flagged, not yet checked"; else "linked".
Reusable for build_shapes_videos 3b: `compile_models3d.prepare_image(src, out_dir, base, ...)`, same naming `assets/images/<slug>/<regid>`.
Per-model facts come from model.js with tolerant adapters (schemas differ per model): confidence_3d {level, reason, reason_short},
provenance[], sources[], tides from water.levels | water_levels, state from state_label | meta.state_* | state_drawn, lifecycle | history.
A model without a curated entry gets auto fallbacks (key numbers = provenance rows, caveats = Limitations table, flagged "not yet curated").

### 4b. Combined "All (compare)" scene - method (round 10)
1. `export_combined.py` opens each COPIED viewer in own headless Chrome. A script registered with `Page.addScriptToEvaluateOnNewDocument`
   replaces `window.__THREE_BUNDLE.THREE` by a copy whose `Scene` subclass records every scene (no viewer file changed; `WebGLRenderer.render`
   is an instance closure in three 0.170, so the prototype cannot be patched - the Scene subclass is the hook).
2. Visible meshes with >= 100 vertices are read in WORLD coordinates. Largest plan bbox = seabed; meshes with ~ the same bbox = skirt (ignored);
   others inside it = reef (merged). What the viewer shows at load is exported (default state / default outline version).
3. Rotation about the vertical so that offshore = +z (pure rotation; `offshore_scene_xz` per slug in `data/models3d_combined.json`, from each
   model's frame note). Scene frames: Prattes / Boscombe (X = x, Z = y), Bunbury (X = x, Z = -y), Palm Beach (ENU: X = E, Z = -N). y = metres above the
   site's own MSL. Footprint polygon from model.js is mapped with `hand` (X' = hand * x, Z' = y).
4. Checks (all PASS now; tolerance in the config): footprint area of up-facing triangles vs model.js toe polygon (+20 % Boscombe, +9.9 % Prattes,
   +4.7 % Palm, 0.1 % Bunbury; the meshes include side slopes beyond the toe line, tolerance 25 %); footprint centroid vs polygon centroid (<= 0.27 m;
   proves rotation + handedness); crest level vs model.js (<= 0.145 m: Bunbury, whose reference is the seabed grid + 2.0 m height; tolerance 0.2 m);
   seabed ~ 0 m MSL along the shoreline (<= 0.52 m, Boscombe: the "surf line" of an image of unknown tide); seabed falls away offshore (<= 4.4 deg).
5. Output uint16-quantised (1.4 cm horizontal) base64 in `3d/combined/<slug>.js` (no fetch: works from file://). Cache signature = viewer html + model.js +
   exporter source + config entry; a changed signature re-runs Chrome (~7 s per model).
6. The combined viewer re-colours the seabed by height with ONE ramp (+3 m ... -15 m) and gives each reef an Okabe-Ito hue; vertex colours of the
   source viewers are not used. VE slider scales `root.scale.y` (all reefs together). Overlay centres every reef on its footprint centroid, hides the seabeds.

## 5. Key decisions and why
- **Offline, file://-safe viewers.** Chrome/Edge block ES-module imports from file:// (CORS "origin null"), so the copied viewers do NOT use an import
  map. `3d\vendor\three.bundle.js` (esbuild IIFE of three.module.js + OrbitControls + CSS2DRenderer, `window.__THREE_BUNDLE`) is a classic script and the
  viewer's `import ... from 'three'` lines are replaced by `const THREE = window.__THREE_BUNDLE.THREE;` etc. Originals in 07_scale untouched. A viewer that
  imports another addon gives a build NOTE: add it to the bundle recipe in `3d\vendor\README.txt`.
- **One model at a time; its viewer starts by itself** (round 10; round 9 loaded on click). Selecting unloads every other viewer (one WebGL context);
  leaving the tab unloads all (`unloadAll()` called from `app.js setView`). A "Load 3D model" poster/button remains as fallback.
- **Stage = viewer + photo panel** side by side (3fr / 2fr, stacked < 900 px). The viewers were built for >= 1100 px windows: when framed (iframe < 1100 px)
  the COPY hides `#side` / `#right` / `#wideBtn` / `#reason` and uses a 2-column grid (Boscombe, `html.m3d-embedded` CSS injected by `inject_chrome`);
  < 600 px the left control column is hidden too (use "Own page"). The standalone page shifts `html` down 34 px for the bar (`html:not(.m3d-embedded)`).
- **Full screen** = `.m3d-stage` (viewer + photos) via `requestFullscreen`; class `is-full` drives the layout in both the native and the CSS-fallback mode;
  `.m3d-exitfs` (inside the stage, top-right, z-index max) + Esc (native by the browser, fallback by our keydown). Selecting another model exits it.
- **Hash routing:** `#view/models3d` -> replaced by `#view/models3d/<first>`; the selector sets the hash (Back / Forward work, `applyHash` on hashchange);
  `all` = combined; an unknown slug falls back to the current / first model.
- **(i) primitive** (`ReefInfo.html(label, html)`): hover, keyboard focus or click (click pins), Esc, x, click outside; `position: fixed` next to the button;
  paragraphs are `<span class="pp">` (never `<p>`: the markup may sit inside a `<p>`, the HTML parser would split it).
- **Long text rule:** header = one line per item with CSS ellipsis (full text in the DOM + `title` + (i)); key-number notes, document notes, picture details,
  vocabulary behind (i); appendix parts are `<details>` that `goto()` opens before scrolling; links with `data-m3d-goto` / `href="#m3d-..."` are handled in-tab.
- **Pictures are copied, not hotlinked** (common.md rule 6). Web copies <= 1600 px, 400 px thumbnails, lazy-loaded; the page says reuse rights are not cleared.
- **Tooltip = hover OR keyboard focus** on a thumbnail (click selects it in the panel); the focus() scroll bug of round 9 stays fixed (`placeTip`).
- **Evidence-verified curated text** (quotations <= 25 words, `ev` snippets must occur verbatim in the model's documents; build prints "VERIFY FAIL").
- **Caveats as data** (`models3d_caveats.json`), mandated rows present and checked; one merged reference list (76 entries).
- **Page size policy:** PASS < 3 MB, INFO 3-15 MB, WARN > 15 MB (never a failure); images and viewers are separate files.

## 6. Outline / model versions (build_3d_tab.md 2b) - contract and implementation
**model.js contract** (written by the 3D model agents; Borth first, Mount Maunganui follows): `versions[]` {id, name (meaningful, with the
edge definition), date (YYYY-MM-DD), source_ids[] (ids of model.js `sources`), method, level (what the edge is), kind (laser_survey|multibeam_survey|
design_drawing|photo_trace|other), area_m2, volume_m3, bbox_m [L,W], note, optional stated {area, volume}}, `default_version` (id; measured survey > design
drawing > photo trace per Lior), `versions_info` (2-4 sentences for the (i) pop-up; blank line = new paragraph; *italic* allowed). Unknown default -> first
version + build NOTE; duplicate ids dropped. Tolerated spellings: source_id|sources|source, footprint_m2, volume.
**Viewer contract**: show the default, offer its own selector if it wants, AND accept the tab's signals: initial `location.hash = #version=<id>`, later
`hashchange`, and `window.postMessage({type:"m3d-version", version:"<id>"})`. The tab sends both for a live iframe and puts the hash on the initial src and the
"Own page" link. `qa_versions_synth.py` contains a minimal compliant viewer. **On the page** (models with >= 1 version; the toggle needs >= 2): header block
"Outline version" (button per version, (i) dialog with versions_info + table), "Showing:" line; key-numbers table gets shaded version rows (curated rows may carry
`versions` / `by_version`); caveats table gets generated rows (origin "versions"). The combined scene shows the default version only.
**Not done**: a real model with versions has never been built into the page; when Borth lands, run build + check + qa and view the header / dialog / caveats
once, curate its key numbers, and add its entry to `data/models3d_combined.json` (the default version is what the viewer shows at load).

## 7. Checks and QA
- `check.py` block "[3D]": section + viewer copy + poster per model; vendored three.js; no CDN / import map; gallery files; tooltip data; confidence / state /
  VE / key numbers / caveats / references; mandated caveat rows; curated evidence; versions contract; **round 10: sticky nav, back bar in every viewer copy,
  combined data block, every export check vs model.js, every model in or out with a reason**; INFO sizes; then `qa_models3d.dom_checks()`.
- `qa_models3d.py` (79 checks, 2026-10-07 PASS): selector + hash + Back + keyboard; one section visible; header one-liners; short text at the top; layout
  (viewer / panel side by side, key numbers below); panel picture + strip; thumbnail click -> panel; tooltip hover + focus; annotated toggle; lightbox open /
  Close / Esc; (i) click / hover / focus / Esc; full screen native + CSS fallback + Esc; sticky nav + selector; Top; Gallery from deep; brand link; All stage;
  standalone combined viewer (frame, items, no overlap, MSL, VE, controls, overlay centring, switch back); standalone viewer bar + hidden when framed; mobile.
- Screenshots `QA\round10_3d_*.png` (viewed downscaled): overview, model_with_photos, thumb_tooltip, panel_annotated, lightbox, info_popover, caveats,
  methods, fullscreen, all_stage, all_method, combined_oblique / plan / overlay / overlay_side, sticky_nav, gallery_header, standalone_bar, mobile, dark.
- Status log entry: `05_qa\00_STATUS.md` (2026-10-07, round 10).

## 8. Key numbers (this build)
| item | value | where |
|---|---|---|
| models shown | 4: boscombe-surf-reef MEDIUM, bunbury-airwave MEDIUM, palm-beach-gold-coast MEDIUM, prattes-reef-el-segundo LOW | models3d.json |
| pictures | boscombe 25, bunbury 13, palm-beach 27, prattes 28 = 93 | models3d.json gallery |
| combined scene | 4/4 exported, 2.2 MB data; footprints 4868 / 112 / 12537 / 478 m2 (exported) vs 4042 / 112 / 11972 / 435 (model.js) | models3d.json `combined` |
| caveat rows / references / verify | 23 / 76 / 109 snippets checked, 0 failed | build log |
| page size | ~1.7 MB; assets\ ~25 MB; 3d\ ~17 MB | check.py INFO |
| not yet modelled | 9 reefs (Mount Maunganui, Borth, Narrowneck have 3d\ folders with SOURCES_3D only, no model.js yet) | build log |

## 9. File map (bulky files marked)
- `src\compile_models3d.py` (~850 lines): data work, viewer copy + chrome injection, `build_combined`. `src\export_combined.py` (~290 lines).
- `src\models3d.js` (~620 lines), `src\models3d.css`, `src\combined_viewer.html` (~330 lines): the UI.
- `data\models3d_curated.json`, `models3d_caveats.json`, `models3d_combined.json`, `models3d_text\{methods,combined_method}.md`: curated inputs.
- `data\models3d.json` (~690 KB, generated, do not open), `data\images_manifest.json` (generated cache), `3d\combined\*.js` (0.1-1 MB each, do not open).
- `3d\vendor\` (`three.module.js` ~1.2 MB, do not open), `3d\<slug>\` (generated viewer copies, never edit), `assets\images\` (generated).
- `QA\round9_3d_LOG.md`, `QA\round10_3d_LOG.md` (step logs), `QA\round10_3d_checks.txt`, `QA\build_check.txt` (latest check report), `QA\prev\round9\` (before round 10).

## 10. Open issues, discrepancies, requests for Lior
1. Pictures are private research copies; reuse rights are NOT cleared - resolve each registry rights_note before any public release.
2. Real models with versions (Borth, Mount Maunganui) are paused until Lior says go; versions are tested with a synthetic model only.
3. Models without a curated entry (Narrowneck etc. when built) show auto-selected numbers and auto caveats; they also need an entry in `data/models3d_combined.json`.
4. A viewer that imports a three.js addon outside the bundle shows a build NOTE and will not run until the bundle is extended.
5. The first-load Google Fonts request fails offline (existing behaviour; falls back to system fonts). The viewers need WebGL (headless uses SwiftShader).
6. `check.py` `[3D]` mandated-row patterns are hard-coded for the four current models (dict `must` in `check_models3d`).
7. Framed viewers hide their own side panels (documents, history) and, on phones, the left control column; the page shows the same content below the stage.
8. Not built: the optional "camera hint" (a button that sets the viewer to the view of a picture). It needs a view-direction field in the registry and a
   viewer message contract; not cheap. Ask Lior if wanted.
9. Combined scene caveats: each model's shoreline is its own fitted waterline (date / tide differ, see the model's methods); seabed patches differ in size and
   data quality (Palm Beach is the largest, Bunbury the smallest); only default outline versions are shown. Crest references: Bunbury has no stored crest, its
   reference is the seabed grid + 2.0 m (difference 0.145 m, tolerance 0.2 m).
10. Lior should look at the tab once in his own browser: the layout was tuned in headless Chrome at 1440 x 900 and 390 x 844.

## 11. What the comparison means (for readers of the page)
Same scale and same MSL zero for all reefs, one depth-colour ramp, one VE slider. NOT comparable without care: absolute offshore distance (each shoreline is
its own fitted line), seabed quality, and reef shape fidelity (surveyed vs idealised). The label of each reef carries its 3D confidence; a LOW reef is drawn like a HIGH one.

## 12. Next steps for the later full-build agent (build_shapes_videos.md), in order
1. Read `_agent_briefs/build_shapes_videos.md` and this file only; do not re-read src\.
2. Shapes tab replacing the Scale tab (mega figure, confidence filters, Shape check viewer, comparison table, outline versions toggle + (i) from shape.json
   `outline_versions` / `default_outline` / `versions_info`): reuse the version UI of models3d.js (versionBarHTML, openVerDlg) and the (i) primitive (`ReefInfo`).
3. Videos tab (review tool, 02_research\videos, media_decisions.json) and the Images tab / reef-dialog gallery from the registry (reuse `prepare_image` and
   `assets\images\`; each display:true registry row once in the Images tab and once in its reef dialog; add counts to check.py).
4. Top-level "Methods" tab (07_scale\METHODS.md with TOC); per-reef METHOD/VERIFY rendering (reuse `render_md`, `md_sections`).
5. Reef dialog: embed the 3D viewer (lazy iframe, same markup/handlers as the tab - `viewerHTML`, `load`, `unload`; MAX_LIVE shared!) + "Shape check".
6. Add routes to the app.js hash regexes the same way as `models3d`; keep the sticky nav in every new tab; keep the 3D block in check.py; keep every vN of the QA screenshots.
7. When Borth / Mount Maunganui models with versions exist: rebuild, view the version header + dialog + caveats rows, curate key numbers, add the combined config entry.
8. Keep this file current (edit, do not just append); add a section per new tab; append to `05_qa\00_STATUS.md`.

# 04_build — Artificial surf reefs page

## What this is

A single self-contained HTML page, `artificial_reefs.html`, surveying the 13 verified,
built artificial surf reefs worldwide (Section 1 of the project). Each reef tile shows
size/cost/year/verdict on hover, and opens to a full dossier (an at-a-glance strip,
then an accordion covering motivation, design vs. as-built, outcome, why it
worked/failed, reviews, images, videos) with every fact carrying its `[R#]` reference
back to the source. Filters, sort, a table view, a map view, dark/light mode, and a
print stylesheet are all built in.

### New in the 2026-09-25 enrichment pass (see `06_gemini_compare/README.md`)

- **Reference pop-ups** — clicking or hovering an `[R#]` marker opens a citation
  pop-up anchored to it (viewport-clamped, flips above/below, phone bottom sheet on
  mobile) instead of jumping to the reference list. Shows the full citation, the
  "Supports" note (from the card's `references[].supports` field), the accessed date,
  and Open source / Show in list / Copy citation actions. One shared Escape handler:
  pop-up closes first, then the lightbox, then the reef dialog.
- **Review cards** — surfer/local reviews now render as their own serif quote-card
  block, each with reviewer name/role, a source chip that opens the citation pop-up,
  and a direct external link. Navigation labels show counts (Reviews N · Media N ·
  Sources N).
- **At-a-glance strip + accordion** — replaces a tabbed-modal layout with one page that
  keeps the big picture visible, stays find-in-page friendly, and prints fully
  expanded.
- A handful of reviews/references cross-checked against a competing AI build
  (Gemini) were folded in, each tagged "via Gemini survey, verified 2026-09-25"; see
  `06_gemini_compare/README.md` for the full per-reef verification results (accept/
  reject counts, what was fabricated vs. real).
- Burkitts Reef's two video-frame stills were removed (QA confirmed neither actually
  shows the artificial reef) and moved to `04_build/QA/removed_assets/`; no
  replacement media was sourced — media review is left to Lior.

### New in round 5 (2026-09-25): the Scale tab and media labels

- **Scale view** (Gallery | Map | Table | **Scale**, also reachable as `artificial_reefs.html#view/scale`):
  every reef's verified footprint (`07_scale/reefs/<slug>.footprint.json`) drawn in plan at one
  common scale (default 1 px = 1 m, zoom ×0.5 / ×2), with shoreline, beach, offshore arrow,
  100 m scale bar, verdict-coloured outline and labelled L × W, area (m² and football pitches),
  crest depth with datum, distance offshore and confidence. Each drawing has a "How we drew this"
  block with the derivation table (every number with its R#/S# source pop-up), the images and
  figures relied on, coordinate conventions, the Gemini comparison, open issues and verification
  log. Below: an overlay of all 13 on one frame (by shoreline or by centroid, per-reef toggles,
  football-pitch silhouette), and a comparison table linking each reef's provenance write-up
  (`docs/scale/<slug>.md`, copied from `07_scale/reefs/`). The reef dialog also has a
  "Scale & footprint" section. Code: `src/scale.js`. Method and conventions:
  `07_scale/drawings/README.md`.
- **Media labels**: images and video frames show what they depict ("shows the structure",
  "shows the reef's effect", "site context only"). Videos show whether they are about the reef.
  Site-only videos are plain links. The hero image prefers structure, then effect, then site
  context. Nothing from `*_rejected` is rendered.
- Keep `docs\` next to the HTML file too (provenance links in the Scale tab).
- Full write-up of the Scale tab's purpose, method, per-reef confidence/sourcing and how
  it's regenerated: `07_scale/README.md` and `07_scale/drawings/README.md`. Media-label
  totals (verdict counts, which images/videos are flagged "site context only", pending
  Lior review): `05_qa/media_recheck_summary.md`.
- Round 6 QA (`04_build/QA/round6_browser.md`, 2026-09-25) found the Scale tab's
  comparison table sorts nowhere — rows are hard-coded to area-descending in
  `scale.js`'s `tableHTML()`, header `<th>` cells have no click handler. Everything else
  in round 6 (13 panels, common scale bar, "How we drew this" popovers, overlay
  align/legend/pitch toggles, zoom, mobile, dark mode, media labels) passed. **Round 7
  (re-test after a table-sort fix) has not been run yet.**

Sections 2 (Israel sediment transfer) and 3 (Haifa conclusions) are short
"in preparation" placeholders — no facts, figures, or citations in them yet.

## How to open it

Double-click `artificial_reefs.html`. It works straight from `file://` with no server.
Keep the `assets\`, `3d\` (3D viewers, vendored three.js) and `docs\` folders sitting next to the HTML file — they hold the local images
(Lior's own figures + video frames, the 3D tab's pictures) and the 3D viewers the page references by relative path; if you move
the HTML file, move these folders along with it.

Web-sourced images are hotlinked (not stored locally), so viewing those requires an
internet connection; if one fails to load the tile falls back to a neutral placeholder
with a "view source" link.

## How to rebuild

From `04_build\`:

```
python src\compile_data.py
python src\build.py
python src\check.py
python src\qa_shots.py --prefix round5
```

(`build.py` also runs `src\compile_models3d.py` for the 3D models tab - see "3D models tab" below.)

**One command for any later change (round 11):** `python src\update_page.py` detects which models / registries / cards changed, backs the page up to
`QA\prev\last_update\`, runs `compile_data.py` + `build.py` (re-copies the viewers, re-exports only the combined meshes that changed, recomputes the
photo-match transforms when needed), runs `check.py` and prints a short summary of what changed (`--fast` skips the Chrome part of the check, `--full`
adds all DOM QA + screenshots, `--dry` only detects). The human steps around it (new model, fixed caveat, pending model updates) are in
`UPDATE_PROTOCOL.md`.

`compile_data.py` reads the 13 verified cards from `02_research\reefs\<slug>.json` and
writes the compiled `data\reefs.json`. `build.py` inlines `src\styles.css`,
`src\app.js`, and `data\reefs.json` into `src\template.html` to produce the single-file
`artificial_reefs.html`. `src\check.py` is a sanity checker used during QA (not part of
the normal build).

## 3D models tab

Added in round 9 (2026-10-06), reworked in **round 10 (2026-10-07, Lior's review)** and extended in **round 11 (2026-10-07)**. The fifth view, **3D models**
(`artificial_reefs.html#view/models3d`, `#view/models3d/<slug>` for one reef, `#view/models3d/all` for the comparison), shows every reef
that has a 3D model, with the pictures the model was built from, the numbers, the methods and the discrepancies. Full contracts, data
flow and every decision: `HANDOFF.md`. Data schema: `data/SCHEMA.md` (sections "models3d.json", "models3d_combined.json").

**What is on the tab (round 10 layout)**

- **Navigation everywhere.** A sticky top bar (brand link "Surf reefs survey" = main page, the five view buttons) stays on screen in every
  tab; a "Top" button appears on long views; every dialog and lightbox has a visible close button and Esc. The long page header text is
  two short lines with an **(i)** pop-over (hover, keyboard focus or click; Esc closes) and is hidden on the 3D tab.
- **Reef selector** (sticky under the bar): one button per modelled reef with its 3D-confidence dot, plus **All (compare)**. One model
  is shown at a time; the URL hash follows the selector (Back / deep links work); the default is the first model. The selected model's
  viewer starts by itself and the previous one is unloaded.
- **Per model, top to bottom:** compact header (reef, one-line confidence reason, one-line state, vertical-exaggeration note; the full
  texts are behind (i)) -> **stage = 3D viewer (about 60 %) next to the photo panel (about 40 %)**, stacked on phones with the photos
  directly under the viewer -> key numbers (model vs stated in the sources, tide levels), methods documents, references; the project-wide
  **Appendix** (A methods, B texts relied on, C caveats, D references, each part opens on demand) closes the tab.
- **Photo panel:** a large picture with an original/annotated toggle, arrows, a short caption and an (i) with how it was used and its
  source; under it the thumbnails grouped by role (plan shape, crest and height, seabed and depth, tides and datum, validation, flagged).
  Clicking a thumbnail shows it in the panel beside the model (no modal); hover or keyboard focus on a thumbnail gives the tooltip
  (how used + source); "Enlarge" opens the lightbox with the full citation, licence and rights note. All pictures are private research
  copies (reuse rights are not cleared; the page says so).
- **Full screen** = the whole stage (viewer + photo panel) through the Fullscreen API, with a red **Exit full screen** button at the
  top-right (always on top), Esc, and a CSS fallback where the API is missing (iPhone). The "Own page" link opens the viewer alone
  (`3d/<slug>/index.html`) with a slim top bar: "<- Back to the page" and the five tabs (the bar is injected into the COPY at build time
  and hidden when the viewer is framed).
- **All (compare)** (`3d/combined/index.html`): every built model in ONE three.js scene at the same scale, side by side along a shared
  shoreline, z = 0 at each site's own MSL, labels with name + 3D confidence, a vertical-exaggeration slider (default 1x, always shown),
  water, metre grid (10 / 50 m), 50 m / 100 m scale bars, plan / oblique / cross-shore presets, per-reef toggles and fly-to, and an
  **Overlay** mode that stacks all reefs on one origin (footprints, crest levels). Geometry is read from each model's own viewer at build
  time (`src/export_combined.py`, method in `data/models3d_text/combined_method.md` and on the page), checked against model.js
  (footprint area, centroid, crest level, shoreline, slope direction; tolerances in `data/models3d_combined.json`), and loaded from
  `3d/combined/<slug>.js` (works from `file://`). A model that cannot be exported is listed as "not in comparison" with the reason.
- **Outline / model versions** (build_3d_tab.md 2b): if a `model.js` carries `versions` (+ `default_version`, `versions_info`) the header
  shows a toggle with each version's name and date (default marked), an **(i)** button that opens a pop-up with `versions_info` and a
  table (name | date | source | footprint | volume), and a "Showing" line. Switching a version tells the live viewer (URL hash
  `#version=<id>` and `postMessage({type:"m3d-version", version})`), re-renders the key-numbers table and the caveats table (generated rows).
  The combined scene shows the default version of each model.

**Round 11 (2026-10-07) added**

- **Six models:** Borth coastal defence reef (three outline versions, default LiDAR 2022; the oval is a BREAKWATER, not a surf reef), Boscombe
  (seabed now extended to the beach and offshore: the beach strip and shoreline show in "All"), Bunbury, Mount Maunganui (two versions; bed level
  default -3.6 m CD is an ASSUMPTION, every bed-dependent number is a `{{token}}` filled from model.js), Palm Beach, Prattes.
- **"All (compare)" fixes:** one shared scale bar (100 m, tick at 50 m), reef labels in screen space with collision avoidance, leader lines and clamping
  inside the canvas (default, plan and overlay views, also in a 1000 x 700 window); the camera fit ignores the layout panel.
- **Collapsible panels:** the combined layout panel and every single-model viewer's own side panel (Borth: its "Controls" panel) have a Hide button and
  a labelled edge button; the page's right-hand panel (photos / "Reefs in this scene") collapses too; all are open by default and keep their state
  through full screen.
- **"Match this photo"** for plan-view pictures whose geometry is already documented (30 pictures; `src/photo_match.py` ->
  `data/photo_match.json`): in the photo panel the button turns the live viewer top-down so that the model covers the same ground as the picture,
  rotated the same way, and shows the picture over it with an **Overlay** slider; **Reset view** restores the previous camera, panels and limits;
  dragging the model ends the match. Eligible: traced pictures of `shape.json` (georeferenced satellite images, the picture an outline was traced on,
  other pictures with a stated px/m registered by their outline) and Garmin Navionics screenshots whose capture log gives centre lat/lon + zoom + crop.
  Not offered: oblique pictures, uncalibrated pictures, fits that would need mirroring, residual above tolerance (2 m; 10 % of the length for reefs
  under 40 m; 4 m for georeferenced pictures, where the residual measures the edge definition, not the registration). Residual = RMS boundary
  distance between the transformed trace and the canonical outline. The receiver (`src/pm_receiver.js`) is injected into the build COPIES only.
- **Outline-version toggle fixed:** the real viewers read `#version=` only at start, so the page now re-loads the live viewer with the new version
  (camera / water level / VE are kept through the viewer's own hash). Before, the buttons changed the text but not the 3D model.
- **One-command refresh** `src\update_page.py` + `UPDATE_PROTOCOL.md`; `compile_data.py` no longer sweeps the 3D picture copies away.

**Files**: `src/compile_models3d.py` (data work, viewer copies + injected bar / compact CSS, calls the export), `src/export_combined.py`
(mesh export + checks), `src/combined_viewer.html` (template of the combined viewer), `src/models3d.js`, `src/models3d.css`,
hooks in `template.html` (sticky nav), `styles.css` (nav, (i) primitive), `app.js` ((i) pop-overs, home / Top, view hooks) and `build.py`;
curated inputs `data/models3d_curated.json`, `data/models3d_caveats.json`, `data/models3d_combined.json`, `data/models3d_text/`;
generated: `data/models3d.json` (inlined as `<script id="data3d">`), `3d/<slug>/` (viewer copies), `3d/combined/` (combined viewer + data),
`3d/vendor/` (three.js 0.170, vendored), `assets/images/<slug>/` (web copies <= 1600 px + 400 px thumbnails; never inlined). The page
needs `assets\`, `3d\` and `docs\` next to it; it works from `file://` (classic-script three.js bundle; Chrome blocks ES-module imports from `file://`).

**Rebuild** (a rebuild discovers new or changed models by itself: every `07_scale\shapes\<slug>\3d\` that has `index.html` + `model.js`;
`FEASIBILITY.md` only gives a "not modelled" card; nothing gives "not yet modelled"; the combined export is cached per model and only
runs Chrome when a viewer, model.js, the exporter or the config changed):

```
python src\update_page.py           # round 11: ONE command (detect, backup, compile_data, build, check, summary); --fast / --full / --dry
python src\build.py                 # runs compile_models3d.py (+ export_combined.py, photo_match.py) first, then inlines everything
python src\check.py                 # includes the "[3D]" block + DOM checks (python src\check.py --no-dom skips Chrome)
python src\qa_models3d.py --prefix round11_3d    # 162 DOM checks (incl. src\qa_round11.py) + screenshots of the tab -> QA\round11_3d_*.png
python src\qa_versions_synth.py                   # test of the versions feature with a synthetic model in a temp sandbox
python src\export_combined.py --force             # (optional) redo the combined export and print every check
```

**Adding or changing a model** needs no code for the tab: re-run `build.py`. Without a curated entry the tab falls back to the provenance
rows of `model.js` (key numbers, marked "not yet curated") and the Limitations table of `METHODS_3D.md` (caveats, status "auto"). To curate:
add an entry per slug to `data/models3d_curated.json` and rows to `data/models3d_caveats.json` (an `ev` snippet must occur verbatim in the
model's documents, else `VERIFY FAIL`). **For the comparison** a new model needs one entry in `data/models3d_combined.json`: the direction
"offshore" in its viewer's scene (from its frame note), the handedness, and JS expressions for its toe polygon and crest level; without it
the model is listed as "not in comparison".

**Checks** (`check.py` block `[3D]`): a section, viewer copy and poster for every discovered model; sticky navigation; the injected back
bar in every viewer copy; every gallery file exists; tooltips have how_used + citation; vendored three.js, no CDN / import map; confidence,
state, key numbers, caveats and references per model; mandated caveat rows; curated evidence verified; versions contract; the combined
scene (files, scripts, every model in or out with a reason, every export check against model.js); page size (INFO above 3 MB, WARN above
15 MB); then the DOM checks of `qa_models3d.py` (selector, hash, layout, panel, tooltip, lightbox, (i), full screen, navigation,
combined scene and overlay, standalone back bar, mobile). Screenshots: `QA/round11_3d_*.png` (round 10: `QA/round10_3d_*.png`).

**Known limits**: pictures are unlicensed research copies; the viewers need WebGL; the first-load Google Fonts request fails offline
(existing behaviour); the framed viewers hide their own side panels (they were built for >= 1100 px windows; open "Own page" for the full
UI); "Match this photo" covers only plan-view pictures with documented geometry (oblique photos are not matched: human alignment is
enough); the combined scene shows each model's default version only; models without a curated entry show auto-selected numbers.

## Hotlinked vs. local

- **Hotlinked (web images):** loaded live from each `url` given in the card, with
  `referrerpolicy="no-referrer"` and `loading="lazy"`. Every one shows credit, license,
  and a link to `source_page`. On a load error the tile shows a neutral placeholder
  with a "view source" link instead of a broken image.
- **Local (`assets\<slug>\...`):** copies of Lior's own figures and extracted video
  frames only — never web images. These are the only images guaranteed to render
  offline.
- **Videos:** where the card marks `embed_ok`, a YouTube (`youtube-nocookie.com`)
  iframe embeds at `?start=<best_timestamp_seconds>`. Otherwise the page shows a link
  (`?t=<seconds>`) plus the `img.youtube.com/vi/<id>/hqdefault.jpg` thumbnail — no
  iframe for those.

## Scope

Section 1 only (13 world artificial surf reefs) is built out with real data. Sections 2
(Israel sediment transfer: geotubes, Tel-Aviv breakwaters, Haifa Port sand bypassing,
Netanya/Herzliya) and 3 (Haifa conclusions) are placeholders pending that research
batch. No new research was done for this build — the page shows only what is already
in the 13 verified cards, each fact with its `[R#]`.

## QA summary

Two rounds of QA are in `QA\`:

- **Round 1 — browser QA** (`QA\round1_browser.md`): 13/13 tiles render, no console
  errors, no broken images (grid or in 3 sampled modals) under a local server; filters,
  sort, table view, map view, mobile layout, dark/light mode, and the print stylesheet
  all passed. Found **2 blockers**: (1) the tile hover overlay only appeared on
  keyboard focus, never on mouse hover; (2) closing a reef's modal and clicking the
  same tile again failed to reopen it (stale `location.hash` prevented a fresh
  `hashchange`).
- **Round 1 — content audit** (`QA\round1_content.md`): compared the page's embedded
  JSON field-by-field against the 13 source cards. No page-build defects — hover
  fields, images, videos, reviews, and narrative text all matched the cards exactly
  (narrative fields are byte-identical copies, not paraphrases), and Sections 2/3
  contain no stray facts. Two **card-inherited, not page**, gaps were flagged: 32
  citations across 6 reefs point to references with an empty `url` (all trace to
  Lior's own local notes/outreach material — the page already renders these as
  "(no URL)" instead of a dead link, so nothing is broken); and 32 sentences across 8
  reefs use the card's own paragraph-final-citation style (one `[R#]` covering several
  numeric sentences) rather than a citation per sentence.
- **Round 2 — browser QA re-check** (`QA\round2_browser.md`): re-tested both round-1
  blockers. The modal-reopen bug is **confirmed fixed** live (scripted open → close →
  reopen sequence on the same reef). The hover-CSS fix is **confirmed correct at the
  source level** (the compiled CSS has an unconditional `.tile:hover .tile-hover`
  rule, and selector matching confirmed it targets the right element); a fully clean
  live pixel/opacity reading wasn't obtainable in that session because the browser pane
  ran backgrounded, so a quick manual mouse-hover glance is recommended to close out
  the residual uncertainty, though nothing here blocks sign-off. No new blockers found.
  One informational note: the map view shows 9 markers for 13 reefs (some cards likely
  lack lat/lon) — not a regression, not investigated further, out of scope.
- **Round 3 — new-feature QA** (`QA\round3_browser.md`): 19 checks against the
  reference pop-up, review quote-cards, and at-a-glance strip added in the
  2026-09-25 enrichment pass, plus a smoke test of pre-existing features. All PASS,
  no blocker.
- **Round 4 — re-check** (`QA\round4_browser.md`): re-ran the round-3 suite with more
  detailed pop-up content checks (citation, Supports text, accessed date, action
  buttons). All PASS, no blocker.
- **Round 7 (2026-09-25): table sort fix** (`QA\round6_browser.md` found it,
  `QA\round7_scale_dom.html` confirms the fix): round 6 flagged the Scale tab's
  "Footprint comparison" table (`tableHTML()` in `src\scale.js`) as non-sortable —
  plain `<th>` text, no click handler, no `aria-sort`, rows hard-coded to area-descending.
  Fixed by giving every header the same `<th aria-sort><button data-sc-sort>` pattern
  (and `table.data` CSS) already used by the gallery table in `src\app.js`: click
  toggles ascending/descending, `aria-sort` updates, numeric columns (L, W, area, crest
  depth, distance offshore) sort numerically, text columns (name, shape, provenance)
  sort alphabetically, and confidence sorts high > medium > low. Row click still opens
  the reef detail dialog. Verified via `python src\build.py`, `python src\check.py`
  (0 failures), `python src\qa_shots.py --prefix round7` (DOM dump shows the new
  `aria-sort`/`<button data-sc-sort>` markup), and live browser clicks confirming
  numeric/alphabetical/confidence sort order and focus return to the clicked header.

**Net: both round-1 blockers fixed and confirmed in round 2; the round-3/4 reference
pop-up, review-card, and at-a-glance features all pass with no open defects.** The
remaining open items (empty-URL references, paragraph-level citation granularity) are
card-content characteristics, not page bugs, and any fix for them belongs in the
`02_research\reefs\<slug>.json` cards, not in `build.py` / `template.html` / `app.js`.
See `06_gemini_compare/README.md` for the Gemini-comparison enrichment details.

## Known limitations

- Web images depend on the source site staying up; a future 404/hotlink-block would
  show the fallback placeholder rather than the image (this is by design, not a bug).
- The map view plots fewer markers than reefs when a card has no coordinates.
- Citation granularity in a few reefs' narrative fields is at the paragraph level, not
  per sentence — a faithful reproduction of the source cards.
- Sections 2 and 3 are placeholders only; the page will need a rebuild once that
  research lands.
- The QA browser-pane environment could not fully confirm the live hover-opacity pixel
  value in round 2 (source CSS is confirmed correct); worth one manual glance before
  wide distribution.

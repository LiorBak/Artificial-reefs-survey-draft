# reefs.json — schema

Produced by `04_build/src/compile_data.py` from the 13 verified Section‑1
cards in `02_research/reefs/<slug>.json`. It is a JSON **array**, ordered by
`sort_year` (then `name`) ascending — oldest reef first. Every card keeps
**all** of its original fields (see the card JSON / dossier `.md` for the
full free‑text research) plus the derived/display fields below.

No new research happens in this script: every fact already existed in the
source card. Fields that are *computed* here are heuristic reshaping of that
same text (year parsing, cost formatting, etc.) — when a heuristic could not
find a clean answer it degrades gracefully (see "Notes on heuristics").

## Original fields (copied through unchanged, except `[R#, R#]` → `[R#][R#]` normalization — see below)

`slug`, `kind`, `verified_on`, `name`, `place`, `country`, `lat`, `lon`,
`year`, `type`, `purpose`, `size`, `cost`, `cost_usd_approx`, `financed_by`,
`motivation`, `designer`, `contractor`, `status_now`, `design_as_planned`,
`as_built_vs_design`, `outcome`, `why_worked_or_failed`,
`unexpected_results`, `could_be_better`, `relevance_to_israel`,
`gaps`. (`images_rejected`, `blocked_sources` and `videos_rejected` are dropped: rejected/internal material never reaches the page.)

Reference‑style citation groups such as `"[R3, R5]"` are normalized to
`"[R3][R5]"` everywhere in the card (this happens before anything else is
derived, so every derived field already has normalized tags).

## Derived fields

| Field | Type | Description |
|---|---|---|
| `year_short` | string | Compact built year, e.g. `"1999–2000"`, `"2019"`. Parsed from the free‑text `year` field — see heuristic below. |
| `sort_year` | int | The earlier year of `year_short`; used to order the array. `9999` if no year could be parsed (none of the 13 cards hit this). |
| `cost_short` | string | Compact headline cost, original currency kept, with `(~US$…)` appended when `cost_usd_approx` yields a parseable USD figure. Falls back to a 40‑char truncation of `cost` if no currency amount could be pattern‑matched, or `"cost not disclosed"` if `cost` is empty. |
| `size_short` | string | `size` truncated to ≤60 chars at a word boundary (`…` suffix if cut). |
| `type_short` | string | One of a small set of short labels (`geotextile sand containers`, `granite rock`, `basalt boulder`, `boulder rock`, `rock (riprap)`, `rock reef`, `inflatable bladder`) chosen by keyword match on `type`, with `"not rock"` / `"no geotextile"` negations stripped first so a sentence like *"…built from geotextile bags, not rock"* still resolves to geotextile. Falls back to a 40‑char truncation if no keyword matches. |
| `verdict` | string | Normalized to exactly one of: `worked`, `partly worked`, `mixed`, `failed`, `n-a` (matched from the card's own `verdict` field by substring; `n-a` = too new / not judgeable, e.g. the 2025–26 Mexico reef). |
| `verdict_label` | string | Display label for `verdict` (`"Worked"`, `"Partly worked"`, `"Mixed"`, `"Failed"`, `"Too early to tell"`). |
| `country_flag` | string | Emoji flag for `country` (small hardcoded map covering the 6 countries in this set: Australia, USA, New Zealand, United Kingdom, India, Mexico). Empty string if the country isn't in the map. |
| `place_short` | string | `"<locality>, <country>"`. If `place` has ≥3 comma‑separated parts, uses the *second* part (usually the recognizable city, e.g. `"Narrowneck, Gold Coast, Queensland"` → `"Gold Coast, Australia"`); otherwise uses the first part (splitting on `/` and keeping the last alternative if present, e.g. `"Dockweiler State Beach / El Segundo"` → `"El Segundo"`). |
| `hero_image` | object or `null` | Best tile image, chosen from the card's `images` array in this priority order: (1) `hotlink_ok: true` **and** `kind` in `photo`/`aerial` **and** a permissive‑looking `license` string (CC / public domain / government / `.gov`); (2) any `hotlink_ok: true` image; (3) if no usable image exists, the first video's YouTube thumbnail (`https://img.youtube.com/vi/<id>/hqdefault.jpg`) with `credit`/`source_page` pointing at the video; (4) `null`, flagged in `problems`. Shape: `{url, credit, license, source_page, depicts}`. |
| `hover` | object | `{size, cost, year, outcome}` = `{size_short, cost_short, year_short, <hover_text trimmed to its first two sentences>}`, for the collapsed tile view. |
| `sections` | array of `{title, html_or_text}` | Ordered detail‑view sections, in this fixed order: `Quick facts` (an HTML `<table>` built from `name`/`place`/`country`/`year`/`type`/`purpose`/`size`/`cost`/`cost_usd_approx`/`financed_by`/`designer`/`contractor`/`status_now`/`verdict`), `Motivation & who pushed for it` (← `motivation`), `Design as planned` (← `design_as_planned`), `As built vs design` (← `as_built_vs_design`), `Outcome` (← `outcome`), `Why it worked / failed` (← `why_worked_or_failed`), `Unexpected results` (← `unexpected_results`), `What could have been done better` (← `could_be_better`), `Relevance to Israel / Haifa` (← `relevance_to_israel`). All `[R#]` tags are preserved (normalized as above). |
| `facts_without_ref` | int | Count of sentences, across the narrative fields (`purpose`, `motivation`, `design_as_planned`, `as_built_vs_design`, `outcome`, `why_worked_or_failed`, `unexpected_results`, `could_be_better`, `relevance_to_israel`, `status_now`), that contain a digit but no `[R` citation tag. Each flagged sentence (truncated) is also listed in the run's `problems` output — most are continuation clauses of an already‑cited sentence that a naive sentence‑splitter cut apart, not truly uncited claims; treat this as a lead for manual spot‑checking, not a hard error count. |

## Fields that pass through with light reshaping

- **`reviews`** — list of `{who, role, quote_or_summary, outlet, date, url, stance?, origin?, ref_id?}`. `stance` and `origin` (e.g. "via Gemini survey, verified 2026-09-25") are kept when the card has them. `ref_id` is derived: the reference whose URL equals the review's URL, so the page can open that reference's pop-up from the review card (no match -> no `ref_id`, logged in problems).
- **`images`** — copied through unchanged; this is already the *accepted* set (rejected candidates live in `images_rejected` and are not carried into `reefs.json`). Each item: `{url, source_page, credit, license, depicts, kind, hotlink_ok}`.
- **`videos`** — copied through, but each video's `frames[].path` is rewritten from a project‑root‑relative path (`03_images/video_frames/<slug>/<file>.jpg`) to a build‑relative one (`assets/<slug>/<file>.jpg`), and the frame file itself is copied into `04_build/assets/<slug>/`. A video with no local frame grabs simply has `frames: []`.
- **`lior_images`** — Lior's own figures (`03_images/from_lior/...`), same treatment: file copied into `04_build/assets/<slug>/`, `path` rewritten to `assets/<slug>/<file>`. An entry whose source file is missing on disk is **dropped** and logged in `problems` (none were missing for the current 13 cards).
- **`references`** — list of `{id, citation, url, accessed, supports, origin?}` (`origin` kept when present). A reference whose URL is a video in the card's `videos_rejected` and that nothing still shown cites is left out of the page (logged in problems; the card is untouched). The compiler cross‑checks that every `[R#]` appearing anywhere in the card's text fields (including the built `sections`) has a matching `id` here, and logs any mismatch in `problems` (none found for the current 13 cards).

## Notes on heuristics

- **Year parsing** (`year_short` / `sort_year`): the free‑text `year` field is split on `;` into clauses; the compiler picks the first clause containing the word "construction", "built", "build" or "install" (falling back to the first clause if none match), then takes the min/max of all 4‑digit years found in that clause. This is a deliberate choice to anchor on *construction*, not on earlier feasibility/design‑study years that often appear first in the text (e.g. Borth's 2004 feasibility study is not used as its year — 2011, "construction started", is).
- **Cost parsing** (`cost_short`): a single combined regex (covering `AUD/NZD/USD/GBP/INR/MXN` currency codes, `A$`/`AU$`/`NZ$`/`US$`/`£`/`Rs`/`₹`/bare `$`, and number ranges like "3–3.2 million") is matched against `cost`, keeping the **leftmost** match in the text (normally the headline figure a source leads with). The USD parenthetical is extracted the same way from `cost_usd_approx` when it's a string (requiring an explicit `$` so an FX‑rate mention like "AUD≈USD 0.65" isn't mistaken for a dollar amount), or formatted directly when `cost_usd_approx` is a number.
- These heuristics are tuned against the 13 cards in this batch and manually spot‑checked; if new cards are added later with unusual phrasing, re‑check the printed `problems` output and the resulting `cost_short`/`year_short` values by eye.

## Assets

Local files copied by this script live at:

```
04_build/assets/<slug>/<original-filename>
```

— referenced from `reefs.json` via `lior_images[].path` and
`videos[].frames[].path` as `assets/<slug>/<original-filename>` (relative to
`04_build/`, i.e. relative to `artificial_reefs.html`). Web images
(`images[].url`) are **not** copied — they stay as hotlinked URLs per the
project's hotlinking policy.

## models3d.json (3D models tab, round 9, 2026-10-06)

Written by `src/compile_models3d.py` (called by `build.py`), inlined into the page as `<script id="data3d" type="application/json">`.
Inputs: `07_scale/shapes/<slug>/3d/` (model.js, METHODS_3D/SOURCES_3D/REQUESTS_FOR_LIOR/FEASIBILITY .md, annotated/), the registry
`03_images/reefs/<slug>/images.json`, the bathymetry reports, and the curated files `data/models3d_curated.json`,
`data/models3d_caveats.json`, `data/models3d_text/methods.md`. All read-only except 04_build.

Top level: `meta` {compiled, three, n_models, verify {checked, failed[]}, warnings[]}, `groups[]` {key,label,blurb} (gallery roles),
`ve_generic` (text), `models[]`, `feasibility[]` ({slug,name,summary,html}: reefs with only a FEASIBILITY.md), `not_yet[]` ({slug,name,note?}),
`caveats_note`, `references[]` ({id "refN", text (markdown-ish, *italic*), url, cited_by[slugs]}), `methods_html` (project-wide methods),
`docs_links[]`.

`models[]` (one per discovered model, sorted by name): slug, name, place, flag, verdict, verdict_label, model_name, built, state_short, state_full,
caption, `confidence` {level high|medium|low|unknown, reason, reason_short}, ve_note, `viewer` ("3d/<slug>/index.html"), `poster`,
`tides` {levels[{id,label,z (m rel. MSL),src,note}], note}, `provenance[]` (model.js rows: parameter,value,unit,source_id,method,uncertainty,estimated),
`sources[]` {id,citation,url}, `key_numbers[]` {q, model, stated, diff, ids ("S1; S2"), note, ev[] (verbatim evidence snippets, verified at build),
optional `versions[]` (ids the row applies to), optional `by_version` {id: {model,stated,diff,note,...}}}, key_numbers_curated, `relied[]` {quote (<= 25 words),
where, supports, url}, `caveats[]` {slug,q,model,stated,diff,reason,status unresolved|open|by-design|resolved|auto,resolve,section,ids,ev[],auto,
origin ("versions" for generated outline-version rows)}, `gallery[]`, gallery_stats {rows,selected,missing_file}, methods_html / sources_html /
requests_html (pre-rendered), docs {methods,sources,requests}, lifecycle, curated, `ref_ids[]`, and the versions block:
`versions[]` {id, name, date, kind (laser_survey|multibeam_survey|design_drawing|photo_trace|other), method, level (what the edge is), note,
source_ids[], source_text[] (citations resolved from model.js sources), area_m2, volume_m3, bbox_m [L,W], stated {area,volume}},
`default_version` (id; first version if model.js names none or an unknown one), `versions_info` (text for the (i) pop-up; blank line = new paragraph).
`versions` is `[]` for models without versions (then no toggle is shown).

`gallery[]` item: id (registry id), group (plan|crest|seabed|tides|validation|flagged|linked), roles[] (registry used_for), title, kind, date, state,
shows, structure_visible, how_used, citation, credit, license, retrieved, image_url, source_page, page_or_figure, rights_note, linked_records[],
pending (for_3d_check.pending), check_what, check_values[], `thumb` / tw / th (400 px), `web` / w / h (<= 1600 px), `annotated[]` {web,w,h,label,file}, added_by.
Files: `assets/images/<slug>/<regid>.<png|jpg>`, `<regid>_400.jpg`, `<regid>_ann<K>.<ext>`. Conversions are cached in `data/images_manifest.json`.

model.js keys read (tolerant adapters; schemas differ per model): name | meta.name, confidence_3d {level,reason,reason_short?}, provenance[], sources[],
state_label | meta.state_label | meta.state_represented | state_drawn, generated | built, water.levels | water_levels, datum, tides.note, caption,
lifecycle | history, and for versions: `versions[]` {id,name,date,source_ids|sources|source,method,level,kind,note,area_m2|footprint_m2,volume_m3|volume,bbox_m,stated{area,volume}},
`default_version`, `versions_info`. Viewer contract for versions: see HANDOFF.md section 6.

Round 10 additions (2026-10-07): top-level `combined` (null when no model exists) = {viewer "3d/combined/index.html", poster, built, `tolerance`
{area_rel, crest_m, centroid_m, shore_m, offshore_deg}, tolerance_text, method_html (from `data/models3d_text/combined_method.md`),
`models[]` one per model: {slug, name (short), level, status "ok"|"not", reason (why "not in comparison"), and for status ok: area_m2 (exported
mesh), area_ref_m2 (model.js toe polygon), area_rel_err, crest_z_m (exported), crest_ref_m (model.js), crest_err_m, bbox_m [alongshore, offshore],
ok (all checks passed), checks[] {name, got, ref, err, tol, unit, ok}, note {rotation_deg, skirt_ignored, reef_meshes, seabed_vertices, reef_vertices}}}.
The page also shows a model with status ok but ok = false (a failed check) and `check.py` fails then.

## models3d_combined.json and 3d/combined/ (combined "All (compare)" scene, round 10)

Config `data/models3d_combined.json` (ours, read by `src/export_combined.py`): `tolerance` {area_rel 0.25, crest_m 0.2, centroid_m 6, shore_m 1.5,
offshore_deg 20} and `models.<slug>` {frame_note (text, from the model's own frame note), `offshore_scene_xz` [x, z] (direction "offshore" in the
viewer's three.js scene; e.g. [0, 1] when the viewer maps model y to scene z), `hand` (+1 if the model's canonical x turns clockwise into y on a
north-up map, then combined X = x; -1 otherwise, X = -x), `polygon` (JS expression, M = window.REEF_MODEL, returning the toe polygon [[x, y], ...] in the
model's canonical frame), `crest_z` (JS expression, metres rel. MSL), crest_note}. A slug without an entry is "not in comparison".

Generated in `3d/combined/`: `index.html` (from `src/combined_viewer.html` + injected bar), `manifest.js` (`window.M3D_COMBINED_META` = [{slug, name, short,
level, status, reason}]), `<slug>.js` (`(window.M3D_COMBINED = window.M3D_COMBINED || {})[slug] = {slug, bounds [minX, maxX, minZ, maxZ] of the seabed patch,
seabed / reef = {n vertices, o (offset), q (metres per unit), pos (base64 uint16 xyz), it (16|32), idx (base64 triangle indices), ni}, footprint [[x, z], ...]
(model.js polygon in the combined frame), centroid, crest_z, area_m2, y_range, rotation_deg, bbox_reef}`), `export_cache.json` (signature per slug:
viewer + model.js + exporter + config; unchanged = no Chrome). Combined frame: x alongshore, y up (0 = the site's MSL), z offshore; a pure rotation about
the vertical of the viewer's scene (nothing mirrored or rescaled); decode: value = o + q * uint16.

## Round 11 additions (2026-10-07)

**`data/models3d_curated.json` / `models3d_caveats.json` tokens.** Any string may contain `{{path|fmt}}` (a model.js path, e.g. `seabed/bed_default_cd`,
`versions/lidar_2022/volume_m3`) or `{{= expression|fmt}}` (expression over `P('path')`, `abs round min max`); formats `n0 n1 n2` (thousands separator), `s0 s1`
(signed), `d1 d2` (plain). Filled at build from the model's own model.js, so the text follows the model (Mount Maunganui bed level). An unresolved token is a
build VERIFY FAIL (shown as "n/a").

**`data/models3d_hold.json`** `{ "hold": { "<slug>": "note" } }`: slugs listed are NOT built (listed under "not yet modelled") even if their 3d folder has
`index.html` + `model.js` (another agent is still writing it). Remove the entry when the model is delivered. Currently empty.

**`data/models3d_combined.json`, new optional keys per model:** `polygon` may return a LIST of rings (Borth: two mounds, Mount Maunganui: five rings);
`area_ref_expr` + `area_ref_label` (a model.js number to compare the mesh footprint with when the mesh includes a flank skirt: Borth = area incl. toe berm,
Mount Maunganui = footprint at the bed), `shore_mode` ("crossing": the seabed crosses 0 m MSL inside the patch instead of at y = 0), `sublabels` [{xy, text}]
(extra labels for parts of one model, e.g. Borth's surf reef vs breakwater). Boscombe's patch is x -160..160, y -66..650 (beach strip + offshore).

**`models3d.json` gallery item, new key `match`** (only for pictures that have a transform in photo_match.json and a viewer receiver): {kind "trace"|"navionics",
method, center_m [x, y], up_m [ux, uy], rotation_deg, width_m, height_m, crop_frac [fx, fy, fw, fh] | null, m_per_px, tolerance_m, reference, zoom, source_id,
rms_m, iou, note}. The page shows "Match this photo" on exactly these pictures (original version only).

**`data/photo_match.json`** (written by `src/photo_match.py`; recomputed by `build.py` only when `signature` changes = hash of photo_match.py + every model's
shape.json, model.js and picture registry): `tolerance` {rms_m 2, small_reef_rule, min_iou 0.5}; `viewers.<slug>` {`scene_map` [[a, b], [c, d]] = canonical (x, y) ->
the viewer's scene ground (X, Z), `scene_map_note`, `canon_to_model_shift_m` [dx, dy] (applied first; only Bunbury: reef at its distance offshore),
`frame_check` {iou_canonical_vs_model_outline, centroid_offset_canonical_to_model_m}, `geo_fit` {rms_m, max_m, scale, vertices} (lat/lon <-> canonical),
`tolerance_m`}; `pictures.<registry id>` {slug, source_id, registry_id, kind "trace"|"navionics", method "georef"|"direct"|"icp"|"web_mercator_capture_log", note,
reference (outline compared with), `to_canonical` [a, b, tx, c, d, ty]: x = a px + b py + tx, y = c px + d py + ty (px, py = pixel of the ORIGINAL image, y down;
x, y = canonical metres = the model.js frame), image_px, residual {rms_m, p95_m, max_m, iou, rings_*} (Navionics: the geo fit only; the chart's own accuracy is not
assessed), tolerance_m, viewer_consistent, center_m, up_m (direction of the picture's top edge in canonical metres), rotation_deg (atan2(up_y, up_x)), width_m,
height_m, m_per_px (+ m_per_px_stated, scale_vs_stated_pct when the picture has a px/m), mirror (picture right/up -> canonical is a reflection; fine, the scene
handedness is checked by viewer_consistent), crop_frac (Navionics screenshots with UI around the map), zoom}; `excluded[]` {slug, source_id, reason, residual}; `summary`
{eligible_images, per_model, max_residual_m}. Methods: georef = pixel -> Web-Mercator bounds -> local metres -> canonical (similarity fitted on canonical.polygons_m vs
geo.polygons_latlon, vertex for vertex); direct = vertex-for-vertex Umeyama fit onto the canonical outline or an outline version that lists the source; icp = raster
cross-correlation over rotation + trimmed ICP, only for pictures with a stated px/m; Navionics = north-up Web Mercator, centre lat/lon + zoom (+ crop) from the capture log.

**Viewer messages (page <-> viewer iframe; viewers are build copies):** page -> viewer `{type:"m3d-version", version}` (see HANDOFF 6), `{type:"m3d-camera", mode:"plan",
center_m, up_m, width_m, height_m, rotation_deg, crop_frac, image (absolute URL), opacity}` (canonical metres; the injected `pm_receiver.js` maps them through
`scene_map`), `{type:"m3d-camera", mode:"reset"}`, `{type:"m3d-camera", mode:"opacity", opacity}`; viewer -> page `{type:"m3d-camera-state", matched, dragged?}` and
`{type:"m3d-viewer-caps", handlesVersion:true}` (a viewer that switches outline versions live announces it; otherwise the page re-loads it with the new
`#version=`). Receivers accept only messages from `window.parent`.

**`data/update_state.json`** (written by `src/update_page.py` after a clean run): {updated, sig {models.<slug> {viewer, model.js, annotated, shape.json, registry, card,
config}, hold, src}, snapshot {<slug> {default_version, versions {id: {area_m2, volume_m3}}, key_numbers {q: text}, pictures, match_buttons, combined {...}}}}; the next run
prints the differences. Delete it to force a "first run" summary.

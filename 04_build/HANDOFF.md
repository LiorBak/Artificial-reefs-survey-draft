# 04_build HANDOFF (page build) - 3D models tab round 11 finished 2026-10-07

Read this instead of re-reading src/. Briefs: the 3D tab = `_agent_briefs/build_3d_tab.md` (round 9, DONE), `build_3d_tab_r2.md` (round 10, DONE) and
`build_3d_tab_r3.md` (round 11, DONE, section 1); the rest of the page (Shapes tab, Videos tab, Images tab, reef-dialog changes, Methods tab) =
`_agent_briefs/build_shapes_videos.md` (NOT done, section 12). Step logs: `04_build/QA/round9_3d_LOG.md`, `round10_3d_LOG.md`, `round11_3d_LOG.md`
(round 11 = two agents; the log has a checkpoint section). Rules followed: `_agent_briefs/common.md`. User-facing docs: `README.md` section "3D models
tab", `UPDATE_PROTOCOL.md` (how to bring in model updates), schemas `data/SCHEMA.md` ("models3d.json", "models3d_combined.json", "Round 11 additions").

## 0. Map and Scale tabs REMOVED (2026-10-10, Lior: "only Gallery, Table and 3D tabs") - read first
- Top navigation = Gallery, Table, 3D models. `#view/map` and `#view/scale` (also old links from viewers) fall back to the gallery. Viewer top bars (`BAR_TABS` in compile_models3d.py, incl. 3d/combined) list the same three. Launcher HTML at the repo root only opens the page: nothing to change.
- Gone from the page: Leaflet + OSM/Carto tile loading (CDN), `renderMap`, map pins sanity code in build.py, map/overlay/comparison-table/panels of the Scale view, their CSS. Not touched: `data/reefs.json` fields (`lat`, `lon`) and the cards.
- **Traceability kept (rule 1):** the reef dialog still has the section "Footprint & how we drew it" (jump button "Footprint"): traced plan drawing at a fixed px/m, facts, the full derivation table
  (quantity, method, source, uncertainty), images relied on, notes, Gemini comparison, open issues, verification, link to the provenance md in `docs/scale/`. It exists for all 13 reefs, so reefs without a 3D model
  keep their traced outline and method. It comes from the slim `src/footprint.js` (successor of scale.js; still `window.ReefScale.detailSection`). The 3D tab keeps the outline versions + methods of modelled reefs. The only thing lost is the side-by-side
  overlay/comparison of all 2D footprints (the 3D tab "All (compare)" scene replaces it for modelled reefs).
- **Archived (restore = copy back):** `archive/04_build_removed_2026-10-10/src/scale.js` (full old Scale view) and `src_before/` (template.html, app.js, styles.css, build.py, compile_models3d.py, check.py, qa_models3d.py, qa_round11.py, qa_shots.py, update_page.py as they were + the page).
  To restore: copy `scale.js` back to `src/`, copy the `src_before` files over `src/` (or re-apply: template buttons/sections + `/*__SCALE_JS__*/` marker, app.js `renderMap`/view lists/hash regexes, build.py scale_js, BAR_TABS), then `python src/update_page.py --full`. Note `photo_match.py` / `pm_receiver.js` / models3d.* changes below are independent and should be kept.
- Checks changed: check.py Scale-view render check -> "footprint detail code present", "no Map/Scale/Leaflet code in page" and "#view/scale falls back to gallery" (qa_shots.retired_view_checks); the "not plotted on map" INFO and qa_shots scale shots removed;
  qa_models3d.py "Map -> 3D models" tab switch now "Table -> 3D models" and the standalone bar expects Gallery/Table/3D models. qa_round11.py and update_page.py needed no check changes (update_page: dropped the "not on map" note filter). No other check weakened.
- Small fixes same day: (a) `pm_receiver.js` scales sizeAttenuation:false sprites by tan(8 deg/2)/tan(home fov/2) while a photo is matched (Palm Beach labels were about 5x too big in "Palm s4"); restored on Reset. (b) compact "Outline version" block (3 buttons on one row, one-line "Showing", title tooltip with the full name): Borth viewer top 585 -> 450 px at 1440 x 900.
  (c) `photo_match.py` now skips slugs in `data/models3d_hold.json` (Narrowneck's half-built folder made photo_match fail and silently removed all 30 "Match this photo" buttons).

## 0b. Hidden shapes, Maps links, interview cards (2026-10-10, Lior's decisions) - read with section 0
- **Rule: draw an outline only if it comes from a real plan source.** compile_data.py `footprint_hide_reason()` hides a reef when ANY of: `07_scale/reefs/<slug>.footprint.json` has `display:false` or `DO_NOT_DISPLAY`; no `07_scale/shapes/<slug>/shape.json`; shape.json `status` not in verified / traced / verified with issues; no `canonical.polygons_m`. Future agents change only those files (flag, shape.json). A hidden reef gets `footprint = {display:false, hidden_reason, docs.feasibility, polygons:[]}`: NO polygon reaches the page data. Reason text = footprint.json `display_reason` (or `status_flag`), else shape.json confidence reason. FEASIBILITY.md is copied to `docs/scale/shapes/<slug>/`.
- **Hidden now (4):** mexico-reef-2026-unnamed (no shape.json; old analogy envelope), opunake-reef (shape.json no_source; footprint.json DO_NOT_DISPLAY), burkitts-reef-bargara (trace = natural rock platform), kovalam-reef-india (one oblique photo, scale unknown). I added `display:false` + `display_reason` to the Burkitts / Kovalam / Mexico footprint.json and a `display_reason` to Opunake (flags only; nothing deleted). Dialog shows "Shape not drawn: no plan, survey or clear image of the reef found (see FEASIBILITY)", the reason, the card's text-only size (r.size, with source markers) and the FEASIBILITY link.
- **Found while checking the other 9:** the dialog used to draw the OLD text-derived footprint.json polygon (schematic), which differs a lot from the traced shape.json (areas, footprint.json -> shape.json m2: Narrowneck 114,950 -> 6,239; Boscombe 10,862 -> 4,042; Cables 2,299 -> 4,049; Borth 3,785 -> 5,743; Mount Maunganui 2,497 -> 1,071; Palm Beach 9,678 -> 11,972; Prattes 324 -> 435; Albany 9,720 -> 10,918; Bunbury 113 -> 112). Now ALL shown outlines are `canonical.polygons_m` of shape.json (rings closed; x reversed for the sea-at-top plan unless the frame text says "sheet right"/"mirror", i.e. Cables/Bunbury; `fp.plan_x_flipped`). Area, plan box, status, confidence and "Outline source" (source, date, credit, method/verify/sources md copies in docs/scale/shapes/<slug>/) come from shape.json. The old derivation table is kept but titled "Earlier text-based estimate (not the drawing)" (crest depth / distance offshore still come from it). Shown (9): narrowneck, cables (design plan, traced, agent still running), prattes (scaled design drawing), mount-maunganui, boscombe, borth, palm-beach, albany (high), bunbury (circle from a drone photo, 12 m text-calibrated, medium; judgement call: not georeferenced - hide it by setting display:false in bunbury-airwave.footprint.json if Lior disagrees).
- **Maps link** (`r.location`, compile_data `location_for()`): order = shape.json `geo` (centre of the traced outline) > shape.json `location_note.approx_centre_latlon` (Bunbury) > card lat/lon. `approximate` when the card gives <= 3 decimals (Opunake -39.46/173.86; Cables was -32.0/115.74 until its agent updated the card to -32.01575/115.748417, now "ok"), the shape has a `geo_note` (Prattes), the centre is of a hidden trace (Burkitts, Kovalam) or it is an estimate (Bunbury +-100 m). Mexico: no coordinates -> "Location: not published", no link. URLs: `https://www.google.com/maps/search/?api=1&query=LAT,LON` plus a satellite view link; target=_blank rel="noopener noreferrer". Shown in the dialog (line under the place, Quick facts row with source), gallery tile, new table column "Location". Card coordinates NOT used because they are far from the traced outline: Albany 0.9 km, Borth 0.4, Narrowneck 0.4, Kovalam 1.5; Burkitts card lat is +24.8205 (sign error, should be -24.82). For the card owners: fix these lat/lon (Burkitts sign, Albany, Kovalam, Bunbury -33.31/115.64 vs shape estimate -33.3276/115.6284, Prattes hint 33.92058/-118.43335 in shape geo_note).
- **Cards of 2026-10-10:** compile_data passes unknown keys through (`interview_2026_10_10`, `sources_disagree`). `sources_disagree` renders as the accordion "Sources disagree" (table topic / card says / interview says / note, with source markers) + nav button; the interview itself shows through reference R25 (Bunbury) / R19 (Albany) and the reviews "Troy ..." (outlet "Personal communication"): process_reviews links a URL-less personal-communication review to the card's single personal-communication reference; references without URL say "personal communication, unpublished - no URL" (reference list and pop-up).
- **Hold list:** data/models3d_hold.json reasons for burkitts, kovalam, mexico, opunake, albany = "Not yet modelled"; cables-reef-wa unchanged (agent running).
- **check.py added:** hidden set = decided 4 + (flag / no shape / status) recomputed from the source files; no polygon in hidden reefs' data; reason + FEASIBILITY copy; every drawn outline has an outline_source; Maps URL format + coordinates for every reef with coordinates; only Mexico without link; headless DOM of all 13 dialogs (no svg for hidden + "Shape not drawn" text; Maps link new tab/noopener/"approximate location" label; "location not published" for Mexico) and the table links. Area check skips hidden reefs.

## 0c. Final page agent (2026-10-10): pending edits, Cables + Albany on the 3D tab, dead ends - read with 0 and 0b
- **Page now (update_page.py --full: "state saved", check 247 PASS / 0 FAIL, qa_models3d 191 PASS / 0 FAIL, 52 shots `QA/update_*.png`):** 9 models on the 3D tab (Borth, Boscombe, Bunbury, Cables, Mount Maunganui, Narrowneck, Albany, Palm Beach, Prattes; combined scene OK 9/9; section 1 below still counts the 6 of round 11). Hold list = burkitts, kovalam, mexico, opunake. Hidden outlines still the 4 (mexico, opunake, burkitts, kovalam; check.py asserts it). `footprint_hide_reason()` never reads shape.json `reef_zone`: Burkitts has `reef_zone.displayable = true` but stays hidden by its footprint.json `display:false` (D9 open); its page data holds no polygon (the card text only mentions the zone in prose).
- **Pending edits applied** (`05_qa/pending_page_edits/audit_*` and the two json files now in `applied/`): Boscombe (state_short, confidence_short, key number 0 note; caveat "As-built crest height": ev now the Rendle p.70 sentence of METHODS A6, stated/diff reworded because the search snippet is confirmed), Bunbury (state_short with the developer's account; new caveat "Fill type: sources disagree"), Mount Maunganui (key numbers 1, 2, 4 stated/ids/note, header "Model source ids" with a tooltip: the model's own R-numbers differ from the card's), Narrowneck (state_short + D7; the (i) text in model.js already says it), Palm Beach (volume row names the three quantities; caveat points to A12-A14 / DEC1-DEC15), Prattes (relied-quote +-150 m). The palm-beach and prattes json files had been applied before. Card notes of the audits were already in the cards (grep: Bunbury lat/lon, Burkitts sign and 9 m depth, Boscombe 4,042 m2, Borth 144.9 m, Palm Beach 279 m, Prattes 64 x 29, Narrowneck crest/containers, Mount Maunganui crest); Kovalam Rendle 4,300 m3 and bbox 43x24 vs 38x29 are NOT in the card.
- **Cables (default = Nov 1999 DoT survey surface):** entries in curated (5 key numbers with tokens), caveats (6 rows, every `ev` verified), combined (`shore_mode:"none"`: the seabed window starts at y = 190 m, no shoreline in the patch; the "falls away offshore" trend uses the whole window because 190-260 m is the natural reef bump). Card: lat/lon -32.0156, 115.7485 (Maps link = shape centre -32.015648, 115.748452), size text now gives surveyed 4,671 / 5,219 m3, 254-263 m to the 0 m AHD line, stated 250 / 275 m and 3,500 / 5,000 / 5,500 m3 kept as stated; new reference R22 (DoT WA bathymetry). Its METHODS_3D "References" is a pointer: references come from `parse_refs_fallback()`.
- **Albany (LOW, plain on the page: badge, state, caveats):** entries from its PAGE_TEXTS_FOR_MAIN.json (default outline = Bluecoast design 13,104 m2). **Defect in its viewer, fixed only in the page copy:** `buildReef` drew `grid.h_cm_b64` (height above the seabed) as absolute z, so the pile floated up to +6 m MSL (combined check: crest 5.96 vs -1.0). `compile_models3d.py VIEWER_FIXES` patches the COPY (`seaAt(x,y) + h`); crest now -1.16 vs -1.0 (smoothing, within 0.2). Owner: fix `07_scale/.../albany/3d/index.html` (the entry then becomes a no-op). Card: R20 (BMT 2018 EIA), R21 (RHDHV 2015 Option B via RWR), R22 (DoT/BoM 2024 tides) added where they back size, design_as_planned (EIA text read at the source: "widening of the shoreline" PDF p.151, offshore placement no significant impact p.38), relevance_to_israel (official tide figures next to Wikipedia's); the City table's "34,000 m3 (based on 2017 bathymetry)" verified on design.jpg and added. Card lat/lon already match the shape (10 m).
- **Dead ends:** `compile_data.py load_dead_ends()` -> `reef.dead_ends`; `app.js deadEndsBody()` = last accordion "Checked, nothing useful (N)" (closed by default, also in print; nav button "Dead ends N"), not in References. check.py: all 13 present, count and order = file, closed, last, after References; leak tests (rejected videos / images, Mexico "no map link") now ignore the dead-ends data on purpose. 196 entries at build time; main appends to the files, the next `update_page.py` picks them up. Seen on a 390 px screen: readable.
- **Other fixes found by QA:** combined labels (9 reefs) overlapped by 2 px at 1000x700 -> `combined_viewer.html placeLabels()` scans the free area when all 12 preferred spots collide; Cables version buttons: the long date text overflowed and covered the neighbour button (unclickable) -> models3d.css truncates the date, title shows name + date.
- **For the owners (not edited here):** Cables model.js names the version `design_plan_original_1999` "(default)" although `default_version` is `survey_surface_1999_11`; Albany/Cables METHODS_3D "References" are one-line pointers; photo_match.py skips Narrowneck, Cables and Albany frames with a note (build does not fail).

## 0d. "Open location in..." block (2026-10-13, Lior: open a reef in Google Earth Pro / Navionics / other software) - read with 0b
- **What it is:** `r.location` (compile_data.py `location_for()`, same point as before: shape.json geo > location_note > card; "approximate" label kept; Mexico = "location not published", no links) now also carries `dd` ("lat, lon", 5 decimals), `dm` (degrees + decimal minutes), `earth_url` (https://earth.google.com/web/@LAT,LON,0a,1000d,35y,0h,0t,0r) and, ONLY for reefs whose outline is shown, `outline_latlon` (= shape.json `geo.polygons_latlon`, the same canonical outline drawn in the dialog, default version) + `outline_source`. Hidden reefs (Opunake, Kovalam, Mexico, Burkitts) carry the point only: no outline can reach a KML (check.py asserts it).
- **Where it shows (app.js `locExtras`, `locMenu`, `kmlFor`, `window.ReefLoc`):** (1) reef dialog: second line under the Google Maps / satellite line (coordinates, Copy, Google Earth (web), KML for Google Earth Pro, Navionics hint); (2) gallery tile: a "Location v" `<details>` menu (opens inline in the tile, does not open the dialog; click outside closes it) with Maps, satellite and the same items; the table keeps its compact "Map" link; (3) 3D tab: every model header (`models3d.js headerHTML`, new `<p class="m3d-loc">`, calls `window.ReefLoc.extras(slug)`); the viewer's own header/side panel was not touched (separate owner folders). The gallery controls row has an "All reefs (KML)" button (template.html).
- **KML:** built in the browser (Blob + download, works from file://): Placemark with name, description (place, location confidence ok/approximate, source, note, whether it is point-only) and, for shown reefs, a Polygon per ring (lon,lat,0; rings closed). "All reefs (KML)" = one Document with every reef that has coordinates (12). Copy button = `navigator.clipboard` with an execCommand fallback (file:// is not a secure context).
- **Tested 2026-10-13 (headless Chrome, network Full):** webapp.navionics.com/#boating@12&key=<encoded polyline of the point> does NOT open a map: it lands on a Garmin "What chartplotter is on your boat?" page. So no Navionics link: the text "Navionics: paste the copied coordinates into its search box" is shown (check.py asserts no webapp.navionics.com link). Google Earth web URL: format as specified, loads (headless Chrome has no WebGL, so "centred" could not be confirmed by screenshot; the @lat,lon,...a,1000d,35y,0h,0t,0r pattern is Google Earth's own).
- **NOT done (no time before the 00:04 deadline): EMODnet Map Viewer link for Boscombe / Borth and a GEBCO / global bathymetry viewer link.** The centred-URL formats of both were not tested, so no link was added (a dead link is worse than none). Next agent: test `https://emodnet.ec.europa.eu/geoviewer/?...` and `https://download.gebco.net/` URL parameters in headless Chrome (it is a JS app: use --virtual-time-budget and a screenshot); if one centres on lat/lon without a login, add `bathy_url` in `location_for()` (Boscombe, Borth only for EMODnet), render it in `locExtras`, add a URL-format test next to "location block data" in check.py.
- **check.py added:** "location block data" (dd / dm / Earth URL format for all reefs with coordinates), "KML outline data only for shown reefs", "[gallery] every reef with coordinates has the menu in its tile", "[gallery] All reefs (KML) button", "Navionics hint, no Navionics link", "[3D tab] every model entry has the block" (9 models), and per dialog "[dialog slug] Open location in block".

- **CHECKPOINT 2026-10-13 (page-map-links agent, stopped at the 00:04 UTC deadline):** DONE: everything above except EMODnet/GEBCO. Page rebuilt (`python src/update_page.py --full`: build step OK; its check.py run had 3 failures: 2 are NOT mine (Albany image 6 lacks a caption label; Cables key-number 'Crest level' quote snippet no longer matches its document: the other agents' unfinished work), 1 was mine (KML test expected an outline for Prattes and Bunbury, which are shown but have no georeferenced `geo.polygons_latlon`, so they get the point only; test fixed, re-run result below / in `/tmp/claude-0/page-map-links/chk3.log`). "state saved" was therefore NOT reached by update_page: after the Albany and Cables owners fix their two items, run `python src/update_page.py --full` once more. Seen: gallery tile menu (opens inline, does not open the dialog), 390 px dialog (no horizontal scroll, block wraps to 4 lines), 3D header block (visible, 336 x 154 px at 390 px width; DOM checked, not photographed). KML in the page: Boscombe 1 polygon, Opunake 0, all-reefs 12 placemarks. Files changed: src/compile_data.py (CRLF kept), src/app.js, src/models3d.js, src/styles.css, src/template.html, src/check.py, HANDOFF.md. Next steps: (1) EMODnet / GEBCO URL test (see above); (2) a Google Earth Pro desktop test of a downloaded .kml by Lior (headless cannot); (3) re-run update_page --full when the Albany and Cables fixes are in; (4) optional: tile menu makes the tile taller than its row neighbours when open (inline, by design because `.tile` has overflow hidden).

## 1. Status per stage (2026-10-07)
| stage | status | confidence / reason |
|---|---|---|
| Tabs Gallery / Table / 3D models (Map and Scale removed 2026-10-10, section 0) | built; full update + 163 DOM checks pass | high |
| 3D tab mechanics (round 9 + 10): discovery, viewers, key numbers, caveats, methods, references, full screen, selector, All (compare) | built, tested | high for the mechanics; per-model numbers are only as good as each model's METHODS_3D |
| Round 11 models: Borth, Boscombe (extended seabed), Mount Maunganui added/updated; 6 models, 6/6 in the combined scene | built | each model medium confidence except Prattes LOW |
| Round 11 combined-scene fixes (Lior's screenshot): Boscombe beach + shoreline, ONE scale bar, labels without overlap inside the canvas | built, QA 80 checks | high |
| Round 11 collapsible panels (combined layout panel, every viewer's side panel, page right panel; kept through full screen) | built | high |
| Round 11 "Match this photo" (30 plan-view pictures, overlay + slider + Reset view) | built; corner-geometry test for every picture | high for the camera maths; registration accuracy = the residual in `photo_match.json` |
| Outline versions with the REAL models (Borth 3, Mount Maunganui 2) | built; a live-switch bug in the old toggle found and fixed (section 6) | high |
| One-command refresh `src\update_page.py` + `UPDATE_PROTOCOL.md` | built, tested end to end incl. a real change | high |
| Shapes / Videos / Images tabs, reef-dialog 3D embed, Methods tab | NOT started | next agent (section 12) |

## 2. Pipeline and commands (run from 04_build\)
```
python src\update_page.py              # ONE command: detect -> backup -> compile_data -> build -> check -> summary (--fast no Chrome, --full + all QA, --dry, --force-export)
python src\compile_data.py             # 02_research cards -> data\reefs.json (+ copies Lior's figures/video frames to assets\<slug>\)
python src\build.py                    # RUNS src\compile_models3d.py (which runs photo_match.ensure + src\export_combined.py), then inlines css/js/json into template.html
python src\check.py                    # static + [3D] block + DOM checks in own Chrome (90 s) -> QA\build_check.txt ; exit 1 on FAIL ; --no-dom skips Chrome (5 s)
python src\qa_models3d.py --prefix round11_3d   # 162 DOM checks (its own 79 + qa_round11.py's 83) + 41 screenshots QA\round11_3d_*.png, report QA\round11_3d_checks.txt (5 min)
python src\qa_round11.py --prefix round11_3d    # only the round-11 checks (combined labels / scale bar, panels, versions with real models, photo match)
python src\qa_versions_synth.py --prefix round11_3d   # versions feature with a synthetic model in a temp sandbox (27 checks)
python src\photo_match.py              # (optional) recompute data\photo_match.json and print every picture with its residual and every exclusion
python src\export_combined.py [--force] [slug]   # combined export alone; prints every check (cached by signature)
```
Never hand-edit artificial_reefs.html. The page needs `assets\`, `3d\`, `docs\` next to it; works from file:// (no server). Backups: page before round 9
`QA\prev\artificial_reefs_before_round9_3d.html`; page + src before round 10 `QA\prev\round9\`, before round 11 `QA\prev\round10\`, rolling copy of the page
before the latest update_page run `QA\prev\last_update\`. Headless QA: ALWAYS our own Chrome on a random free port + fresh profile (`src\qa_cdp.py`).
Shell quirks: the Bash tool rejects some long heredocs with quotes; PowerShell here is 5.1 (no heredocs, `Set-Content -Encoding utf8` writes a BOM): write patch
scripts with the Write tool. Console is cp1255: scripts that print non-ASCII call `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.

## 3. Module map (src\)
| file | what it does | 3D-tab hook |
|---|---|---|
| compile_data.py | reads the 13 verified cards -> data\reefs.json; round 11: no longer sweeps `assets\images\` (3D picture copies) into QA\removed_assets | none |
| build.py | derived fields (USD, map checks), runs compile_models3d, inlines everything | markers /*__M3D_CSS__*/, /*__M3D_JS__*/, __DATA3D__ |
| template.html, styles.css, app.js, scale.js | page skeleton, tokens, gallery/map/table/dialog, (i) primitive, Scale tab | hooks for `models3d` view, hash regexes, `unloadAll()`, `ReefInfo` |
| compile_models3d.py (~1000 lines) | ALL data work of the 3D tab (section 4); copies viewers + injects back bar, compact-embed CSS, collapsible-panel CSS/JS (`BAR_CSS`) and the photo-match receiver (`inject_receiver`); curated `{{tokens}}` (`fill_tokens`); hold list; prunes stale picture copies; `build_combined()` | writes data\models3d.json, 3d\, assets\images\ |
| export_combined.py | build-time export of reef + seabed meshes from each copied viewer (section 4b) | 3d\combined\<slug>.js, export_cache.json |
| combined_viewer.html | template of the combined viewer: shared scale bar, screen-space labels, collapsible layout panel | -> 3d\combined\index.html |
| photo_match.py | transforms of the plan-view pictures (section 4c) -> data\photo_match.json; `ensure()` recomputes only when an input changed | read by compile_models3d |
| pm_receiver.js | "Match this photo" receiver injected at the END of each viewer's last module script (sees `camera`, `controls`) | message contract in SCHEMA.md |
| models3d.js (~780 lines) / models3d.css | the tab UI (one IIFE `window.ReefModels3D`): selector, stage, photo panel (+ match row), versions (reload of the live viewer), panels, full screen | reads `#data3d` |
| update_page.py | one-command refresh (UPDATE_PROTOCOL.md) | state in data\update_state.json |
| qa_cdp.py | tiny Chrome DevTools driver (random port, fresh profile) | used by every QA script |
| qa_models3d.py / qa_round11.py / qa_versions_synth.py / check.py / qa_shots.py | QA (section 7) | `dom_checks()`, `dom_checks11()` imported by check / update_page |

## 4. Data flow (3D tab)
```
07_scale\shapes\<slug>\3d\{index.html,model.js,docs.js,annotated\,preview_oblique.png}  + {METHODS_3D,SOURCES_3D,REQUESTS_FOR_LIOR,FEASIBILITY}.md (READ-ONLY)
07_scale\shapes\<slug>\shape.json (traces, scale, georef, canonical outline, outline_versions)    03_images\reefs\<slug>\images.json (registry, display!=false)
04_build\data\models3d_curated.json | models3d_caveats.json | models3d_combined.json | models3d_hold.json | models3d_text\{methods,combined_method}.md   (ours)
        |  src\compile_models3d.py  (photo_match.ensure -> discover -> parse model.js -> versions -> pictures + match -> tokens -> render markdown -> verify -> merge refs -> combined)
        v
04_build\data\models3d.json --inlined as <script id="data3d">--> artificial_reefs.html (2.1 MB; WARN above 15 MB)     data\photo_match.json  data\update_state.json
04_build\3d\<slug>\   viewer copy (index.html rewritten: vendored three, bar, compact + panel CSS/JS, receiver; model.js, docs.js, annotated\ <=1200 px, poster.jpg)
04_build\3d\combined\ index.html, manifest.js, <slug>.js (exported meshes), export_cache.json     3d\vendor\ three.js 0.170 (classic bundle)
04_build\assets\images\<slug>\<regid>.<png|jpg>, <regid>_400.jpg, <regid>_annK.<ext>  (<=1600 px; generated, pruned by compile_models3d; never inlined)
```
Discovery: every `07_scale\shapes\<slug>\3d\` with `index.html` + `model.js` is a model unless listed in `data\models3d_hold.json`; `FEASIBILITY.md` only ->
"not modelled" card; neither -> "not yet modelled". Models are listed alphabetically; the first is the selector default (now Borth).
Picture selection (per model): registry rows with display!=false AND (used_for contains plan_trace|scale|3d_*|cross_check|camera_match, OR linked_records mention
3d\SOURCES_3D / model.js, OR file/annotated_files in 3d\annotated, OR for_3d_check.pending); a row corrected to `context` only (Boscombe img-01, img-07) drops out and its
stale copy is pruned. Per-model facts come from model.js with tolerant adapters. Curated text may carry `{{path|fmt}}` tokens read from model.js (Mount Maunganui bed,
Borth versions); a model without a curated entry gets auto fallbacks.

### 4b. Combined "All (compare)" scene - method
1. `export_combined.py` opens each COPIED viewer in own headless Chrome; a Scene subclass registered before the viewer runs records every scene (no viewer file changed).
2. Visible meshes with >= 100 vertices are read in WORLD coordinates: largest plan bbox = seabed (Boscombe now x -160..160, y -66..650: beach + offshore); same bbox = skirt;
   inside = reef. What the viewer shows at load is exported (default state / default outline version).
3. Rotation about the vertical so offshore = +z (`offshore_scene_xz`, `hand` per slug). Frames: X = x, Z = y (Prattes, Boscombe, Mount Maunganui, Borth), Bunbury Z = -y, Palm Beach ENU.
   Round 11: `polygon` may be several rings; `area_ref_expr` compares the mesh with a model.js area that includes the flank skirt (Borth: incl. toe berm; Mount Maunganui:
   footprint at the bed); `shore_mode: crossing`; `sublabels` (Borth: surf reef vs breakwater).
4. Checks per model (footprint area, centroid, crest, shoreline, slope direction; tolerances in the config) - 6/6 pass; footprint 11,922 / 4,868 / 112 / 1,904 / 12,537 / 478 m2 (exported).
5. Output uint16-quantised base64 in `3d/combined/<slug>.js`; cache signature = viewer html + model.js + exporter + config entry (~7 s per changed model).
6. The combined viewer (round 11): ONE shared scale bar (100 m, tick at 50 m; sits at the first visible patch, moves to the reef last flown to; overlay: bottom-left); reef labels are
   HTML in screen space with candidate offsets, leader lines and clamping into the visible area (clear of the layout panel); the camera fit uses the stage width minus the panel
   and re-fits when the frame is resized unless the user moved the camera; "Hide" / bottom-left "Layout" buttons collapse the layout panel (only phones < 600 px start collapsed).

### 4c. "Match this photo" - method (round 11, `src/photo_match.py`)
Per picture a similarity pixel -> canonical metres (canonical = shape.json frame = model.js frame; checked per model: `frame_check`). Methods: `georef` (pixel -> Web-Mercator bounds of the
image -> local metres -> canonical, similarity fitted on canonical.polygons_m vs geo.polygons_latlon; geo-fit residual 0.005-0.15 m), `direct` (vertex-for-vertex Umeyama fit of the traced
rings onto the canonical outline or an outline version that lists the source), `icp` (pictures with a stated px/m: raster cross-correlation over rotation, trimmed ICP, only the proper-handedness
variant of the viewer), Navionics (centre lat/lon + zoom + crop of the capture log: Borth, Mount Maunganui, Palm Beach 982 x 655 clips; Boscombe a 1000 x 751 map pane inside 1400 x 900;
Bunbury and Prattes excluded: no geo in shape.json). Residual = symmetric RMS boundary distance trace vs outline (outer rings only). Tolerance 2 m, 10 % of the length for reefs < 40 m,
4 m for georef pictures (edge definition differs between years / definitions, the registration is exact). Excluded: oblique (Bunbury img4), uncalibrated (Bunbury img5), mirrored fit,
Boscombe img2 / img3 (4.6 / 5.0 m: contour colour edge / design-stage outline), Palm s2 (dark rock only, 28 m), Prattes img6 (1996 concept, 4 m).
Eligible 30: Borth 8 (sat2024 0.0 m, sat2022 2.2, sat2012 3.3, drg1020 0.13, 4 Navionics), Boscombe 6 (img1 + 5 Navionics), Bunbury 1 (img1, 0.23 m), Mount Maunganui 7 (img1 0.15, img2 0.77,
img3 0.02, 4 Navionics), Palm Beach 6 (s7 0.0, s4 1.1, 4 Navionics), Prattes 2 (img1 0.0, img5 0.19); max trace residual 3.25 m (Borth sat2012).
Viewer side (`pm_receiver.js`): narrow-FOV (8 deg) top-down camera over the picture centre, picture up = screen up (camera a hair behind the bottom edge), overlay `<div id=m3d-pmo>`
sized from the ground footprint, side panels folded while matching, Reset restores camera / FOV / limits / panels, dragging hides the overlay. Test hook `__m3dMatch.screenOf`.

## 5. Key decisions and why
- **Offline, file://-safe viewers.** Chrome blocks ES-module imports from file://, so the copied viewers use `3d\vendor\three.bundle.js` (esbuild IIFE: three + OrbitControls + CSS2DRenderer,
  `window.__THREE_BUNDLE`) and their `import` lines are rewritten; originals in 07_scale untouched; a viewer needing another addon gives a build NOTE.
- **One model at a time; its viewer starts by itself**; selecting unloads the others (one WebGL context); leaving the tab unloads all.
- **Stage = viewer 60 % + photo panel 40 %** (stacked < 900 px). Framed (iframe < 1100 px) the COPY hides `#side` / `#right` / `#wideBtn` / `#reason`; Borth's only panel `#side` holds the
  CONTROLS (class `m3d-sidectl`) and is kept; Boscombe is a 3-column grid (`m3d-grid3`). Round 11: Hide / edge buttons on every viewer panel (state in sessionStorage `m3d-panels`, hook `__m3dPanels`).
- **Full screen** = `.m3d-stage` through the Fullscreen API with an Exit button + Esc and a CSS fallback; the page right panel (`.m3d-pics`) collapses (class `pics-off`).
- **Hash routing:** `#view/models3d[/<slug>|/all]`. **(i) primitive** `ReefInfo`. **Long text rule:** one line + ellipsis + (i) / appendix `<details>`.
- **Pictures are copied, not hotlinked** (common.md rule 6); reuse rights are not cleared (the page says so).
- **Evidence-verified curated text:** quotations <= 25 words, `ev` snippets must occur verbatim in the model's documents ("VERIFY FAIL" otherwise); numbers that depend on a model value are
  `{{tokens}}` so they follow model.js (nothing hard-codes -4.0 m CD for Mount Maunganui).
- **Caveats as data** (`models3d_caveats.json`, 47 rows + generated version rows), mandated rows per model checked in `check.py` (`must`).
- **Match this photo only for plan-view pictures with documented geometry; no oblique pictures** (Lior); the receiver is injected into the build COPIES (`inject_receiver`), never into 07_scale.
- **Versions: the page re-loads the live viewer** (section 6). **Combined scene shows each model's default version only.**
- **update_page.py never writes to 07_scale / 03_images / 02_research;** one rolling page backup; state file written only after a clean run.
- **compile_data.py skips `assets\images\`** (it used to move the 3D picture copies to QA\removed_assets on every run, forcing a 55 s re-encode; 39 MB of such copies are still in `QA\removed_assets`, safe to delete).

## 6. Outline / model versions - contract and implementation
**model.js contract**: `versions[]` {id, name (meaningful, with the edge definition), date, source_ids[], method, level, kind (laser_survey|multibeam_survey|design_drawing|photo_trace|other),
area_m2, volume_m3, bbox_m, note, optional stated}, `default_version` (measured survey > design drawing > photo trace per Lior), `versions_info`. Real models: Borth `lidar_2022` (default, 8,675 m2, 31,336 m3),
`design_1020` (30,091 m3), `sat_2024` (26,400 m3); Mount Maunganui `multibeam_2013_m2p0` (default, 1,071 m2, 3,620 m3 at the default bed) and `asr_installed_toe_2008`.
**Viewer contract (corrected in round 11)**: viewers read `#version=<id>` at START (none of the real ones re-reads it later). The page therefore re-loads the live viewer with
`index.html?r=<time>#version=<id>&<its current hash>` (camera / water / VE live in the hash). A viewer that switches live announces `postMessage({type:"m3d-viewer-caps", handlesVersion:true})`
and then only gets `postMessage({type:"m3d-version"})` + a hash change (the synthetic test viewer does). Before this fix the buttons changed text and key numbers but NOT the 3D model
(the round-10 test used a synthetic viewer). QA now reads the viewer's own version `<select>` after each switch. On the page: header "Outline version" (button per version, (i) dialog,
"Showing:" line), shaded version rows in key numbers, generated caveat rows (origin "versions"). A photo match is cleared on a switch.

## 7. Checks and QA
- `check.py` "[3D]" block: section + viewer copy + poster per model; vendored three.js; gallery files; confidence / state / VE / key numbers / caveats / references; mandated caveat rows; curated
  evidence; versions contract; sticky nav; back bar; combined data and every export check; unreferenced assets (held slugs ignored); INFO sizes; then `dom_checks()`.
- `qa_models3d.py` 162 checks (2026-10-07 PASS): the 79 of round 10 (selector, hash, layout, panel, tooltip, lightbox, (i), full screen, navigation, combined scene, standalone bar, mobile) +
  `qa_round11.py` 83: combined labels do not overlap and stay inside the canvas, one scale bar (default / plan / overlay / 1000 x 700), Boscombe seabed reaches the beach; layout panel Hide / Layout;
  page panel + full-screen panels and state; every viewer's panel collapse; versions with Borth and Mount Maunganui incl. "really applied"; "Match this photo" UI per model and the corner-geometry
  test for all 30 pictures (overlay corners = picture corners projected by the viewer's camera, <= 3 px); no page errors.
- Screenshots `QA\round11_3d_*.png` (41, viewed downscaled): combined_oblique / plan / overlay / panel_hidden, fullscreen_panels_open / hidden, viewer_panel_hidden_borth, versions_borth_* /
  versions_mount_*, photomatch_<model> (6) and the round-10 set. `QA\round11_3d_versions_checks.txt` = synthetic versions test.
- Status log entry: `05_qa\00_STATUS.md` (2026-10-07, round 11).

## 8. Key numbers (this build)
| item | value | where |
|---|---|---|
| models shown | 6: borth-coastal-defence-reef MEDIUM, boscombe-surf-reef MEDIUM, bunbury-airwave MEDIUM, mount-maunganui-reef MEDIUM, palm-beach-gold-coast MEDIUM, prattes-reef-el-segundo LOW | models3d.json |
| pictures | borth 22, boscombe 26, bunbury 13, mount-maunganui 8, palm-beach 27, prattes 28 = 124; "Match this photo" on 30 of them | models3d.json gallery |
| combined scene | 6/6 exported, all checks pass; Borth 11,922 m2 vs model.js 11,518 (area incl. toe), Boscombe 4,868 vs 4,042, Mount Maunganui 1,904 vs 1,788 | models3d.json `combined` |
| caveat rows / references / verify | 47 (+ generated version rows) / 95 / 119 snippets checked, 0 failed | build log |
| page size | 2.16 MB; assets\ 42 MB; 3d\ 25 MB; models3d.json ~1 MB | check.py INFO |
| not yet modelled | 7 reefs (Narrowneck has a 3d\ folder without model.js) | build log |

## 9. File map (bulky files marked)
- `src\` see section 3. `data\models3d_{curated,caveats,combined,hold}.json`, `data\models3d_text\{methods,combined_method}.md`: curated inputs. `data\photo_match.json` (generated, ~60 KB, readable),
  `data\update_state.json` (generated), `data\models3d.json` (~1 MB, do not open), `data\images_manifest.json`, `3d\combined\*.js` (do not open), `3d\vendor\` (do not open), `3d\<slug>\` and `assets\images\` (generated, never edit).
- `UPDATE_PROTOCOL.md` (how to bring in model updates), `QA\round11_3d_LOG.md` (step log + checkpoint), `QA\round11_3d_checks.txt`, `QA\build_check.txt` (latest check report), `QA\build_log.txt` (latest build output),
  `QA\prev\{round9,round10,last_update}\`, `QA\removed_assets\` (39 MB of old picture copies, deletable).

## 10. Open issues, discrepancies, requests for Lior
1. Pictures are private research copies; reuse rights are NOT cleared - resolve each registry rights_note before any public release.
2. **Pending model updates (come in with `update_page.py`, see UPDATE_PROTOCOL.md):** Mount Maunganui bed (default -3.6 m CD, later -2.8; the bed is an ASSUMPTION until the 2007 survey; all bed numbers are tokens);
   Borth offshore fix (seabed beyond 335 m is 0.89 m deeper than the Fig 2 -4.0 m contour; the 0.89 figure is typed in the caveat row and key number, update by hand); Boscombe flattening (offshore alongshore tilt, HANDOFF open issue 1 of that model).
3. Borth: oval length 38 m (drawing 1020) vs 46 m (1023) unresolved; volumes LiDAR 31,336 / design 30,091 / photo 26,400 m3; tide slider LAT..MHWS (HAT not found); the oval is a BREAKWATER, not a surf reef.
4. A viewer that imports a three.js addon outside the bundle shows a build NOTE and will not run until the bundle is extended.
5. The first-load Google Fonts request fails offline (falls back to system fonts). The viewers need WebGL.
6. Match-photo limits: Palm Beach text labels are drawn at world size and look huge in the 1.5 km Palm s4 view; pictures matched through a schematic icon (Palm s4) are only as good as the icon;
   Navionics screenshots are placed from the capture log, the chart's own positional accuracy is not assessed; Bunbury / Prattes Navionics have no geo.
7. With seven reef buttons the selector row wraps at 1440 px and the stage starts lower (full-screen button below the fold at 900 px high).
8. Combined scene: each shoreline is its own fitted waterline; only default outline versions are shown; patches differ in size and data quality.
9. Lior should look at the tab once in his own browser (tuned in headless Chrome at 1440 x 900 / 1000 x 700 / 390 x 844); `check.py` `must` rows are hard-coded per model.

## 11. What the comparison means (for readers of the page)
Same scale and same MSL zero for all reefs, one depth-colour ramp, one VE slider. NOT comparable without care: absolute offshore distance (each shoreline is its own fitted line), seabed
quality, and reef shape fidelity (surveyed vs idealised). The label of each reef carries its 3D confidence; a LOW reef is drawn like a HIGH one.

## 12. Next steps for the later full-build agent (build_shapes_videos.md), in order
1. Read `_agent_briefs/build_shapes_videos.md` and this file only; do not re-read src\. Run `python src\update_page.py --fast` first to see the baseline.
2. Shapes tab replacing the Scale tab (mega figure, confidence filters, Shape check viewer, comparison table, outline versions toggle + (i) from shape.json `outline_versions` / `default_outline` /
   `versions_info`): reuse the version UI of models3d.js (versionBarHTML, openVerDlg), the (i) primitive and `data\photo_match.json` (pixel -> canonical transforms of the traced pictures).
3. Videos tab (review tool, 02_research\videos, media_decisions.json) and the Images tab / reef-dialog gallery from the registry (reuse `prepare_image` and `assets\images\`; the 3D tab prunes
   `assets\images\<slug>\` to the pictures it shows: an Images tab must register its own copies in the same naming or extend `_keep` in compile_models3d.main).
4. Top-level "Methods" tab (07_scale\METHODS.md); per-reef METHOD/VERIFY rendering (reuse `render_md`, `md_sections`).
5. Reef dialog: embed the 3D viewer (lazy iframe, same markup/handlers as the tab - `viewerHTML`, `load`, `unload`; MAX_LIVE shared!) + "Shape check".
6. Add routes to the app.js hash regexes the same way as `models3d`; keep the sticky nav; keep the 3D block in check.py; keep every vN of the QA screenshots.
7. Keep this file current (edit, do not append); add a section per new tab; append to `05_qa\00_STATUS.md`; model updates always through `update_page.py`.

## 0e. Paper-review additions (2026-10-19, page agent) - small changes, NO 3D change
- **Cards** (02_research/reefs, each `.md` got a dated "Added" section): new keys `rating` ({rank,A,B,C,reason,scale,source}) on the 13 rated reefs and `tide_check` (text with [R#]) on Albany, Bunbury, Cables, Opunake, Burkitts, Prattes; new references (rating = repo notes rating_final.md / rating_evidence.md, no URL; tide sources WA DoT/BoM 2026, LINZ Port Taranaki, MSQ Burnett Heads, NOAA 9410840). Pratte's: 6 new reviews (YouTube DK7cqXDzLpM, grade D, retrieved 2026-10-19 via Lior) + one sentence in why_worked_or_failed.
- **Pipeline**: `app.js` quickFacts rows "Tide range (checked 2026-10-19)" and "Rating A / B / C" (with (i) `RATING_INFO()`), Table column "Rating A/B/C" (sorts by rank; hover = reason). `template.html` section `#paper-figures` (collapsed `<details>`, figures 1-9 from 08_paper/figures, downscaled JPG in `assets/paper_figures/`, captions from the *.caption.md); `compile_data.py` no longer moves `assets/paper_figures/` out as unreferenced. To refresh the figures: re-run the small copy (PIL thumbnail 1100 px) and paste captions into the template.
- **Text fixes**: Albany image 6 `shows` now starts with "structure visible" (card); Cables + Albany PAGE_TEXTS (2026-10-13) applied to data/models3d_curated|caveats|combined.json (text only; Cables `crest_z` expression comment and all geometry NOT touched). Build failures gone.
- Run: `--full` ended "state saved", check.py 0 FAIL (see QA/build_check.txt).

## 0f. Palm Beach video + comment (2026-10-19, page agent)
- Card `palm-beach-gold-coast.json`: new video 8Ebp7VNAGEY ("Wave Pocket Tracking at the Palm Beach Artificial Reef", channel Michael Thompson, via oEmbed; year not retrieved; Lior's description and note in `what_it_shows`; linked only) and review @rebeccaeccles1480 (grade D). `.md` card got a dated "Added" section. Run: full update ended "state saved", check.py 0 FAIL.

## 0g. Open-licence hot-links localised (2026-10-20, page agent)
- `src/compile_data.py local_copy_for()`: an image whose licence says CC / public domain AND whose original is saved + registered in `03_images/reefs/<slug>/images.json` (matched by image_url) gets a `local` path (copied to `assets/<slug>/`); `src/app.js` shows `local` in the tile and the Media list (url stays the source link). Effect: Opunake hero + Media photo (Wikimedia, CC BY-SA 3.0, Gonzalobaeza) and 6 more CC/registered images (Borth geograph, Boscombe, Mount Maunganui, Narrowneck) now local. All other hot-links (raisedwaterresearch, abc-cdn, wixstatic, crucollective, squarespace, albany.wa.gov.au, ...) stay hot-linked: licence "not stated / all rights reserved / link only".
- Pratte's (DK7cqXDzLpM) and Palm Beach (mHSiPEh-93M, 8Ebp7VNAGEY) testimony + A/B/C rating verified in Gallery dialogs (Reviews / Media) and the Table (playwright, 1200x800). Palm Beach viewer comment has no R-number source button (card has no matching reference).
- Run: `--full` "state saved", check.py 0 failures.

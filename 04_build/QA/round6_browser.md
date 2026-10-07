# Round 6 browser QA — Scale tab + media labels + smoke test

Date: 2026-09-25
Method: built-in browser pane, page served from `python -m http.server 8767` in `04_build/`, loaded at `http://localhost:8767/artificial_reefs.html`. Checks below were driven with a mix of real `computer` clicks (via `find`/`read_page` refs) and, where an element was off the rendered viewport (long single-page app, `<details>` and dialog content far down the DOM), `javascript_tool` calls that call `.click()` on the exact DOM node found by text/class — i.e. still a real DOM click dispatch on the real element, not a state fake. Screenshots were used opportunistically; `read_page`/`get_page_text`/direct DOM queries were the primary read method because the pane's screenshot call repeatedly timed out while backgrounded (documented Claude_Browser behavior, not a page bug).

## Smoke test

- Page loads, HTTP 200, no build/template errors.
- Console: **no errors**. One harmless `[warn] Unrecognized feature: 'web-share'` (browser feature-policy noise, unrelated to the page's own JS).
- Network: only the two expected `GET /artificial_reefs.html` 200s logged by the pane (external image/CDN fetches aren't surfaced by this network log, consistent with prior rounds).
- Gallery, Map, Table, Scale tab buttons all present and switch `aria-pressed` correctly.

## Scale view

- Opens from the "Scale" nav button; content renders (13 `<article class="sc-panel">` elements inside `#scale-root`, one per documented reef).
- **13 panels confirmed**, each with its own SVG plan drawing (`svg.sc-svg`), verdict badge, confidence label, PLAN BOX / FOOTPRINT AREA / CREST DEPTH / DISTANCE OFFSHORE / SHAPE fields, each carrying `[R#]`/`[S#]` reference markers.
- **Scale bars checked programmatically across all 13 SVGs** (`.sc-bar rect` width): all 13 read **50.0 px at 100% zoom** (1 px = 1 m), i.e. every 100 m scale bar is the same pixel length — panels are genuinely drawn at one common scale. At ×2 zoom all 13 read **100.0 px** — still uniform, and the "1 px = 0.5 m (200%)" label updates correctly.
- Labels present: reef name, country flag + place + year, verdict icon + text, confidence, dimension callouts, scale bar with "0" / "100 m" ticks, "1 px = 1 m" caption.
- **Click a panel → detail dialog**: clicking a panel's "Open the full record of …" control opens `<dialog open>` with the matching reef's full record (confirmed for Narrowneck Reef). Dialog closes cleanly via `.close()`.
- **"How we drew this" expand**: implemented as a native `<details class="sc-how">`; clicking the `<summary>` toggles `open` true/false and reveals "1 · Derivation …", the quantity/value/method/source/uncertainty table, "2 · Images and figures relied on", "3 · Coordinate conventions", "4 · Gemini comparison", "5 · Open issues", "6 · Verification" — confirmed on Narrowneck's panel.
- **`[R#]`/`[S#]` markers inside "How we drew this"**: are real `<button class="ref-mark">` elements; clicking one opens a `.ref-pop.show` popover with the source title, publisher, a working `<a href>` link, and what it supports (confirmed for `R4`, which opened linking to `icce-ojs-tamu.tdl.org`).

## Overlay (all-reefs comparison figure)

- `role="group" aria-label="Overlay options"` present with: **By shoreline (true distance offshore)**, **By centroid**, **Football pitch silhouette**, **Show all**, **Hide all**.
- Overlay SVG (`aria-label="Overlay of 13 reef footprints…"`) shows all 13 footprints by default.
- **Football-pitch toggle**: clicking it flips `aria-pressed` false→true and a `[class*="pitch"]` element appears inside the overlay SVG. Confirmed.
- **Align mode switch**: clicking "By centroid" flips its `aria-pressed` to true and the overlay SVG's markup changes (re-laid-out); the SVG's own `aria-label` updates to "…centred on their centroids". Confirmed.
- **Legend toggles**: 13 toggle buttons (`role="group" aria-label="Show or hide reefs in the overlay"`), one per reef with swatch + name + area. Clicking one flips its `aria-pressed` and the overlay SVG's `aria-label` count drops from "13 reef footprints" to "12 reef footprints" (Narrowneck hidden); "Show all" restores the count to 13. Confirmed both directions.

## Comparison table

- A `<table class="data sc-cmp">` ("Footprint comparison") lists all 13 reefs with columns Name / Shape / L / W / Area / Crest depth / Distance offshore / Confidence / vs Gemini / Provenance, each row's name a button that opens that reef's detail dialog.
- **Defect found (see below): the table does not sort.** Rows are hard-coded to a fixed `area desc` order in `scale.js` (`tableHTML()`), the `<th>` cells have no click handler, no `aria-sort`, and are not buttons — clicking a header does nothing (verified: dispatching a real `.click()` on the "Area (m²)" `<th>` left row order unchanged, twice in a row). This is a gap against the round's checklist item "comparison table sorts."

## Zoom

- Zoom ×2 (`+ ×2`) doubles the label to "1 px = 0.5 m (200 %)" and every one of the 13 scale bars grows from 50 px to 100 px — still uniform across panels, so relative comparison stays valid after zooming. "Reset to 1 px = 1 m" returns to the 100 % state. Zoom out (`− ×0.5`) button is present (not separately re-verified numerically beyond the reset path, given ×2 and reset both checked cleanly).

## Mobile (375×812 emulated)

- No horizontal scroll: `document.documentElement.scrollWidth === clientWidth === innerWidth === 375` on the Scale view.
- Panels stack in a single column (checked 3 `.sc-panel` elements: all `left: 16px`, `width: 343px` — full-width stack, no side-by-side leftover grid).
- Overlay figure (`#sc-ov-fig`) fits its box at this width (SVG 329px inside a 341px-wide box) with no page-level overflow; overlay-specific internal scrolling wasn't triggered at this size because content simply fit, but no bleed onto the page was observed either way.
- Scale tab remains the active/selected nav item through the resize (`aria-pressed="true"`), confirming state survives a viewport change.

## Dark mode

- Dark mode is the page default; checked visually via screenshot at mobile width — verdict pills, headings, stat tiles and body text all render with clear light-on-dark contrast, no invisible/low-contrast text spotted on the Scale intro/stats block.

## Gallery / detail / media labels

- Gallery tab still opens reef tiles and each tile's button opens the same detail `<dialog>` used from the Scale panels.
- **Burkitts Reef ("Greg's Reef")**: detail dialog headings list "Images 6" but **no "Videos" heading at all** — confirmed Burkitts has no videos section, matching the checklist expectation.
- **Site-only video, link-only rendering**: verified on Opunake Reef's "Every Breaking Wave at OPUNAKE beach." video — renders as `<div class="video video-linkonly">` with a `tag-about about-site` label ("site only — not about the reef"), a plain "▶ Watch on YouTube (from 0:05)" link, and explanatory text "listed for site context only; it does not show the reef." No player/thumbnail/frames rendered for it, as intended.
- **Image "shows …" labels**: confirmed present via `.tag-shows` spans in image captions (e.g. Narrowneck Reef's gallery has 5 `tag-shows` labels: "site context only", "shows the reef's effect" ×2, "shows the structure" ×2); Opunake's single image also carries a descriptive caption noting it doesn't show the submerged structure.

## Verdict

**Not a blocker.** The Scale view opens, all 13 panels render at one verified common scale, the detail dialog and "How we drew this" derivation/reference popovers all work, the overlay's align/legend/football-pitch controls all work, zoom is consistent, mobile has no horizontal scroll and panels stack, dark mode is readable, and the video/image labeling checks (Burkitts no-video, Opunake link-only video, "shows…" caption tags) all pass.

**One real defect to fix:** the Scale tab's comparison table (`<table class="sc-cmp">` built by `tableHTML()` in `04_build/src/scale.js`) has no working sort — headers are plain `<th>` text with no click handler/`aria-sort`, and row order is hard-coded to area-descending. Recommend adding click-to-sort on the header cells (at minimum Area, L, W) analogous to the gallery's sort control, then re-running `build.py` and re-testing this specific check in round 7.

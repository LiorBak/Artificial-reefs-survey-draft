# Browser QA — round 1

**Target:** `04_build\artificial_reefs.html`
**Served at:** http://localhost:8765/artificial_reefs.html (python -m http.server 8765, stopped at end of session)
**Also opened:** `file:///C:/Users/lior/Documents/Claude/Projects/Artificial%20reef/04_build/artificial_reefs.html`
**Tool:** Claude built-in browser pane (mcp__Claude_Browser__*)
**Date:** 2026-09-25

## Summary

13/13 tiles render, no console errors, no broken images anywhere under the http server (all local + hotlinked images verified fetchable, in the grid and inside 3 separate detail modals). Filters, sort, Table view and Map view all work without throwing. Mobile layout has no horizontal scroll and the modal is usable full-screen. Dark mode and light mode both render with good contrast and no stray white boxes. A print stylesheet is present.

Two real functional bugs were found in modal open/close and hover behavior — see Blockers below.

## Checks

### Console / images (PASS)
- `read_console_messages(onlyErrors)` → no errors on load, and none after all interactions (filter, sort, table, map, mobile, dark mode).
- 13 `.tile` elements present, 13 `<img>` elements; `[...document.images].filter(i=>i.complete&&i.naturalWidth===0)` → `[]` (no broken hero images).
- Opened 3 different reef detail modals (narrowneck-gold-coast, mount-maunganui-reef, boscombe-surf-reef). For each, fetched every `<img src>` inside `#reef-dialog` — all returned OK/200 or opaque (no-cors) success; zero broken. Image counts per modal: 8, 6, 7. iframe counts: 3, 1, 4. Reference-superscript link counts: 101, —, 81 (all had non-empty, well-formed `#reef/<slug>/R<n>` hrefs; 0 malformed).
- Figure captions include credit/license/source-link text (`fig-box` blocks with a `view source` link + accessed-date/credit line); the `fallback` `<span>Image unavailable here</span>` block is present but correctly `hidden` while the image is fine — its text simply shows up in `textContent` reads even when hidden, which briefly looked like a false positive during testing but was confirmed harmless (naturalWidth check + direct fetch both confirm the images load).

### Hover overlay / keyboard focus — **BLOCKER**
- Requirement: "hover overlay appears on a tile (hover action) and shows size/cost/year/outcome; keyboard focus shows it too."
- Found the per-tile overlay element (`#hv-<slug>`, class `.tile-hover`, referenced via `aria-describedby` on the tile's title button). It correctly contains Size / Cost / Year / outcome text with `[R#]` citations.
- Inspected the actual CSS rules for `.tile-hover`: the **only** rule that sets `opacity: 1` is `.tile:focus-within .tile-hover`. There is **no `:hover` rule at all** for `.tile-hover` or any ancestor.
- Confirmed live: `computer.hover` over a tile's title button leaves `getComputedStyle(overlayEl).opacity === "0"` — the overlay never appears on mouse hover, only when the tile gains keyboard focus (e.g. via Tab or click-to-focus).
- Impact: mouse-only desktop users (the majority) never see the promised hover summary by hovering a tile — the stated design ("hover to preview size/cost/year/outcome") does not work for them at all.
- Fix: add a `.tile:hover .tile-hover { opacity: 1; }` rule alongside the existing `:focus-within` rule.

### Modal open / close / reopen / hash — **BLOCKER**
- Click opens the modal: **PASS**. `Esc` closes it: **PASS** (verified with a genuine `computer` Escape keypress, `dialog.open` goes `true → false`).
- URL hash updates to `#reef/<slug>` on open: **PASS**.
- Full page reload with `#reef/<slug>` in the URL reopens that reef's modal: **PASS** (verified via `location.reload()`; a simple same-page `navigate` call to the same hash is not a true reload and doesn't exercise this path, so that route was tested separately with an actual reload).
- **However:** closing the dialog does **not** clear `location.hash`. Reproduced repeatedly and reliably, with real `computer` clicks and a real `computer` Escape key: open reef A → close (Esc) → click reef A's tile again → **the modal does not reopen** (`dialog.open` stays `false`), because the hash is already `#reef/A` so setting it again fires no `hashchange` event, and the click handler evidently doesn't call `showModal()` unconditionally. Calling `document.getElementById('reef-dialog').showModal()` directly always works, confirming the dialog element itself is fine — the bug is in the open-trigger logic not re-invoking `showModal()` when the target hash is unchanged.
- Opening a **different** reef after closing one works fine (new hash → hashchange fires → opens). Only same-reef reopen after a close is broken.
- Impact: any user who opens a reef, closes it, and clicks the same tile again (an extremely common action — e.g. reread a detail, or re-open after checking another tab) gets no response. This is a core, explicitly-tested interaction and it fails.
- Fix: either (a) have the close handler clear/replace the hash (e.g. `history.replaceState(null,'',location.pathname)` on close) so a later click always produces a real hashchange, or (b) have the open-tile click handler call `dialog.showModal()` directly (not gated solely on a hashchange listener) whenever the dialog isn't already open for that slug.

### Filters / sort / Table / Map (PASS)
- Verdict filter "Failed" → grid shows exactly 5 tiles, matching the "5 judged failed" summary stat. Toggling it back off restores 13.
- Sort `<select>` → `cost:-1` (cost, highest first): value change dispatched cleanly, 13 tiles still render, no throw, no console errors.
- Table view button → `<table>` with 13 `<tbody><tr>` rows.
- Map view button → Leaflet map renders (`#map.leaflet-container`), 9 SVG marker `<path>` elements for the 13 reefs (some reefs share/are near the same coordinates, e.g. multiple Gold Coast, Australia entries — not itself a bug, just fewer distinct visual clusters than reef count). No console errors from any of these transitions.

### Mobile (PASS)
- `resize_window(preset: mobile)` (375×812) + reload: `document.documentElement.scrollWidth (375) <= window.innerWidth (375)` → no horizontal scroll.
- Tiles stack at full width (343px, i.e. viewport minus gutters).
- Opened a modal at mobile width: renders full-screen (375×812), no horizontal overflow (`scrollWidth` stayed 375).
- Viewport reset to desktop afterward.

### Dark mode / light mode (PASS)
- `resize_window(colorScheme: dark)` + reload: `prefers-color-scheme: dark` matched; `body` background `rgb(16,19,22)`, heading text `rgb(231,233,236)` (light-on-dark, good contrast), no elements found with a literal white (`rgb(255,255,255)`) background of meaningful size — no stray white boxes.
- `resize_window(colorScheme: light)` + reload: `body` background `rgb(248,247,243)`, `prefers-color-scheme: dark` correctly false.
- Reset to light at the end.

### Print stylesheet (PASS, presence only as scoped)
- Confirmed a print-specific stylesheet/rules exist (`@media print` rules present via `document.styleSheets` inspection, plus a dedicated `#print-all.print-only` DOM block built for print output). Actual print rendering not exercised (out of scope per task — "just confirm a print stylesheet exists").

### file:// (no server) — informational note, not a page bug
- Opened `file:///C:/Users/lior/Documents/Claude/Projects/Artificial%20reef/04_build/artificial_reefs.html` directly. Page loaded (title, 13 tiles, 13 `<img>` all present), modal opened and closed fine.
- The Claude browser pane renders this particular local file as a sandboxed "static snapshot" — `document.baseURI` inside that tab resolves to a `data:` URL, not the real `file://` path. Under that sandboxing, the two purely-relative local asset images inside the Narrowneck modal (`assets/narrowneck-gold-coast/image26.png`, `image29.png`) reported `naturalWidth === 0`.
- This is very likely a limitation of the QA tool's `file://` handling, not a real bug in the page: (a) the exact same images loaded with zero broken images under the real `http://localhost:8765` server; (b) the `assets/narrowneck-gold-coast/` folder does contain `image26.png` and `image29.png` on disk, as siblings of the HTML file, matching the relative paths used; (c) `document.baseURI` being a `data:` URL confirms relative-path resolution was broken by the snapshot mechanism itself, not by the page's own markup.
- Recommendation: **spot-check this manually by double-clicking the file in a real desktop browser (Chrome/Edge)** to be fully certain, since this tool could not give a clean file:// signal for local relative assets. Not counted as a blocker here because the evidence points to a tool artifact, but flagging it since the task specifically asked to confirm file:// works.

## Verdict

**2 blockers** (hover overlay never appears on mouse hover — only on keyboard focus; modal fails to reopen for the same reef after being closed once, via click or hash). Both are core, explicitly-required interactions and both were reproduced with real user-input events (`computer.hover`, `computer.left_click`, `computer` Escape keypress), not just synthetic JS dispatch.

No blocker-level broken images found anywhere (grid or inside any modal, under the real http server). Filters/sort/Table/Map, mobile layout, and dark/light mode all pass cleanly with no console errors.

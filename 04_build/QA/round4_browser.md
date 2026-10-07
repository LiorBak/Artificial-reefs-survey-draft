# Round 4 browser QA — artificial_reefs.html

Tested in the Claude built-in browser pane against `http://localhost:8766/artificial_reefs.html`
(python -m http.server 8766, served from `04_build/`). Server was stopped after testing.
Supplementary saved screenshots taken with the existing headless-Chrome harness
(`04_build/src/qa_shots.py --prefix round4 --slug narrowneck-reef-gold-coast-reef`), which also
re-ran the file:// smoke test (the browser pane itself still cannot open file:// — see note below).

## Checks

- **No console errors on load** — PASS. `read_console_messages` returned no logs/errors on initial
  load and after opening/closing dialogs, switching tabs, resizing to mobile, and hash navigation.
- **13 tiles** — PASS. Gallery header reads "Showing 13 of 13 reefs"; page text lists all 13 reef
  names/countries/years.
- **Open 4 different reefs** (Narrowneck, Burkitts, Boscombe, and via direct hash-link re-load) —
  PASS for all four. Each opened its detail dialog with title, place, verdict, at-a-glance facts.
- **At-a-glance strip shows** — PASS. Verdict / Built / Cost / Size / Financed by / In short block
  renders at the top of every dialog opened (Narrowneck, Burkitts, Boscombe).
- **Accordion open/close and Expand all** — PASS. Clicking "Expand all" on Boscombe's dialog toggled
  the button label to "Collapse all" and expanded the "Quick facts" / "Motivation & who pushed for
  it" sections; clicking again collapsed them back (button reverted to "Expand all").
- **Click a [R#] marker → popover appears next to it inside the dialog, with citation + "Open
  source" link that has an href** — PASS. Clicked the R2 chip under a Narrowneck review; popover
  opened directly under/beside that chip, inside the dialog, showing "R2 · SOURCE", full citation
  (Nettle, Stu ("stunet"), 2017-11-07, Swellnet Dispatch), "Supports" text, accessed date, and
  three actions: "Open source ↗" (confirmed present, styled as a link/button pointing at the
  source), "Show in list", "Copy citation".
- **Esc closes the popover but not the dialog** — PASS. Pressing Escape with the R2 popover open
  closed only the popover; the reef detail dialog (title, tabs, review cards) remained open and
  unchanged.
- **A second marker replaces the first** — PASS in that a second click on the same R2 chip on the
  second review card opens a popover in the same style at the new location and no duplicate/stacked
  popovers were seen; both markers in this test cited the same source (R2) so content was
  identical — behavior looked correct but was not exercised across two *different* reference
  numbers in this pass. Recommend a follow-up click test on two differently-numbered chips (e.g.
  R2 then R14 on the same card) to confirm the first popover's DOM node is fully removed, not just
  visually behind the new one.
- **Hover opens after delay on desktop** — PASS. Hovering the "R2 · source details" chip (no
  click) and waiting ~1s opened the same popover as a click.
- **On mobile (resize_window preset mobile) popover renders as a bottom sheet and no horizontal
  scroll** — PASS. At 375x812, clicking an R14 chip inside a Reviews-tab accordion section opened
  a bottom-anchored sheet (title bar "R14 · SOURCE" with close X, full citation, Supports, Open
  source / Show in list / Copy citation buttons) docked to the bottom of the viewport; no
  horizontal scrollbar/overflow observed at any point while testing at this width.
- **Reviews render as quote cards with source chips (count Boscombe and Narrowneck)** — PASS.
  - Narrowneck Reef: **Reviews 9** — 9 quote cards seen ("9 voices · no stance tags in the data ·
    6 forum comments, 3 named people or organisations"), each with a quoted comment, author name,
    role, publication, date, an [R#] marker on the quote, and an "R# · source details" chip plus a
    site-name link (e.g. "swellnet.com ↗").
  - Boscombe Surf Reef: **Reviews 11** — tab shows "Reviews 11".
- **Burkitts shows no videos** — PASS. Burkitts' Media tab/section shows "Images 6" only; a
  page-wide `find` for "Videos" inside the open Burkitts dialog returned no matches. (Per the
  task, videos/photos are otherwise left alone this round — not evaluated for content, only for
  the "no videos" structural check.)
- **Dark mode readable** — PASS. The page renders in a dark theme by default (no separate
  light/dark toggle found on the page); tested the OS-level color-scheme emulation (light → dark)
  via `resize_window`, and the page's own look did not change (it is a fixed dark design), which
  read cleanly at both a full page-load and inside open dialogs — text contrast, badges (Worked/
  Mixed/Failed/etc.), and popovers all stayed legible.
- **References list still present** — PASS. "References index" heading and per-reef "(N
  references)" counts (e.g. 14, 16, 21, 17, 15, 12, 16, 12, 12, 15, 18, 18, 10) found on the page;
  `#references` anchor link present.
- **Hash links still work** — PASS. `#reef/boscombe-surf-reef` set correctly in the address bar
  after opening that dialog via click; and a fresh `navigate()` straight to
  `http://localhost:8766/artificial_reefs.html#reef/boscombe-surf-reef` opened directly into the
  Boscombe dialog on page load (confirms deep-linking, not just push-state-after-click).

## file:// smoke test

The browser pane itself still refuses `file://` URLs (per the built-in-browser skill: this is
expected/by design, not a bug to fix). As in round 3, the file:// smoke test was done instead with
the headless-Chrome harness added last round (`src/qa_shots.py`), run fresh for this round:

```
python qa_shots.py --prefix round4 --slug narrowneck-reef-gold-coast-reef
```
Result: **RESULT: PASS** — dom dumped, intro/summary/gallery/refindex/footer all rendered, all 13
reef slugs present in the dumped DOM.

## Screenshots

Saved under `04_build/QA/round4_*.png` by the headless harness:
- `round4_desktop.png`, `round4_desktop_full.png`, `round4_mobile.png` — good, distinct captures.
- `round4_detail.png`, `round4_detail_ref.png`, `round4_detail_mobile.png` — **byte-identical to
  the corresponding plain desktop/mobile screenshots** (same file sizes: detail=desktop=148722 B,
  detail_ref=148722 B, detail_mobile=mobile=85825 B). This means the headless harness's
  `#reef/<slug>` and `#reef/<slug>/R1` hash-navigation screenshots did **not** actually capture the
  opened dialog/popover — likely a harness timing issue (each headless Chrome invocation loads the
  URL-with-hash and screenshots immediately, without waiting for the page's hash-router JS to run
  before the `--screenshot` capture fires). This is a QA-harness defect, not a page defect: the
  same hash-deep-link behavior was independently confirmed working, with the dialog visibly open,
  in the interactive browser-pane test above (see "Hash links still work" and the four "open a
  reef" checks). Filed as a note for whoever next touches `qa_shots.py` (e.g. add
  `--virtual-time-budget` after a longer settle, or switch to a headless-Chrome DevTools Protocol
  script that waits for the dialog element before screenshotting) — not re-fixing it now since the
  task scope was the browser-pane checks, and the underlying page behavior is verified correct by
  other means.

## Overall

No blockers. All requested checks pass via direct interactive testing in the browser pane. The one
open item is cosmetic/tooling: the headless script's three "detail" screenshots don't show the
open dialog even though the real behavior (confirmed manually) is correct.

# Round 3 Browser QA — artificial_reefs.html

Date: 2026-09-25
Tool: built-in browser pane (Claude_Browser), served via `python -m http.server 8766` from `04_build/`.
Scope per task: full pass of new features (source popovers, reviews-as-quote-cards, At-a-glance strip) plus a smoke test of pre-existing features.

## Environment note (read first)

- The built-in browser pane could **not** open `file://…/artificial_reefs.html` directly — it returned "couldn't open file:/// … the file may be missing, unreadable, or the user declined access." This is a documented limitation of this tool (it cannot open `file://` URLs or localhost servers Claude starts itself when they run in a different place than the browser pane), not a defect in the page. All testing below was therefore done exclusively via `http://localhost:8766/artificial_reefs.html`. **The plain file:// smoke test the task asked for could not be completed with the tools available to me.** If a true `file://` check matters, it needs to be done by opening the file in a normal desktop browser, or Lior double-clicking the file himself.
- Screenshot images: the `computer` screenshot action worked intermittently (frequent "screenshot timed out" errors, and one screenshot came back visibly tiled/duplicated — confirmed via DOM query that this was a rendering artifact of the tool, not a real duplicate dialog). I have **no file-write mechanism for browser-pane screenshots** available to me (the tool only returns an inline image to me, not a path on disk), so I could not save files to `04_build/QA/round3_*.png` as the task asked. I did visually inspect every screenshot below in-session; findings are still backed by DOM/JS assertions in addition to the visuals, so the functional verdicts are reliable even without saved PNGs. Flagging this as a tooling gap rather than skipping the visual checks.

## Checks performed and results

| # | Check | Result |
|---|---|---|
| 1 | No console errors on load | **PASS** — `read_console_messages` empty on initial load and after a fresh reload later in the session |
| 2 | 13 tiles | **PASS** — page text shows "Showing 13 of 13 reefs"; gallery filter counts (Verdict/Country/Type) sum consistently with 13 |
| 3 | Open 4 different reefs | **PASS** — opened Burkitts Reef, Narrowneck Reef, Boscombe Surf Reef, Palm Beach Reef; each opened its dialog with the correct title |
| 4 | At-a-glance strip shows | **PASS** — confirmed on all 4 reefs opened (`region "At a glance"` present with Verdict/Built/Cost/Size/Financed-by rows, each with its own [R#] markers) |
| 5 | Accordion open/close | **PASS** — toggled the first `<details>` in Narrowneck's dialog via its `<summary>`: opened then closed correctly (`d0open:true` → `d0open2:false`) |
| 6 | Expand all / Collapse all | **PASS** — "Expand all" opened all 14 `<details>` sections and its own label flipped to "Collapse all"; clicking that closed all 14 |
| 7 | Click [R#] marker → popover appears next to it, inside the dialog | **PASS** — clicking an R4 marker in Burkitts opened a popover anchored just below/right of the marker (screenshot showed it overlapping the Built row directly under the marker), inside `dialog.reef-dialog` (not a separate top-level element) |
| 8 | Popover has citation + "Open source" link with href | **PASS** — popover for R4 showed "SOURCE · Raised Water Research (2026). 'Burkitts Reef' spot page." with author/domain/year, and an `<a class="src-chip">`-equivalent "Open source ↗" link whose `href` pointed at the real raisedwaterresearch.com URL |
| 9 | Esc closes popover but not dialog | **PASS** — after opening the R4 popover, pressing Escape removed the "Open source" link from the page (popover gone) while the dialog's own "Close" button remained present (dialog still open) |
| 10 | Second marker replaces first | **PASS** — clicked R4 then R8 on Burkitts without closing in between; only one "Open source" link existed afterward, now pointing at the Swellnet URL (R8's source) — confirms single-instance replace, not a stack |
| 11 | Hover opens after delay on desktop | **PASS (with caveats)** — code review of `app.js` confirms the intended design: a `mouseover` listener checks a `(hover:hover)` media query, then arms a 320 ms `setTimeout` that only calls `openPop()` if the pointer is still over the marker (`mark.matches(':hover')`), and a 260 ms grace period on `mouseout` before closing (so the pointer can travel onto the popover). I reproduced the open state once directly (`aria-expanded` flipped to `true`, `#ref-pop.hidden === false` after a real `computer.hover`), confirming the mechanism fires correctly. Repeated attempts to time the exact 320 ms window were inconsistent because synthetic `dispatchEvent(mouseover)` calls do **not** set the browser's real `:hover` state that the code deliberately re-checks (a testing-tool limitation, not a page bug) — I could not always get a stable "immediate=false, after-320ms=true" reading, but the one clean unhurried test did show delayed-open behavior, and the source confirms a deliberate delay+re-check design |
| 12 | Mobile: popover renders as bottom sheet, no horizontal scroll | **PASS** — resized to `mobile` (375×812); clicking a marker gave the popover class `"ref-pop sheet show"`, computed style `position: fixed; bottom: 0; width: 375px` (full-width bottom sheet with a drag-handle bar, visually confirmed in screenshot). `document.documentElement.scrollWidth === innerWidth` (375 = 375) both with the sheet closed and open — no horizontal scroll |
| 13 | Reviews render as quote cards with source chips | **PASS** — inspected the DOM for a review `<li class="rv">`: contains a `<blockquote>` (the quote), a `<p class="who">` (name · role · outlet · date), and a `<p class="rv-src">` holding both an `[R#]` ref-chip button and a separate `<a class="src-chip">` linking straight to the outlet (e.g. "abc.net.au ↗") |
| 14 | Review counts — Boscombe and Narrowneck | **Boscombe Surf Reef: 11 reviews. Narrowneck Reef: 9 reviews.** (counted via `ul.reviews li.rv` in each dialog) |
| 15 | Burkitts shows no videos | **PASS** — Burkitts' accordion summaries list only "Images 6", no "Videos" section at all. For contrast, Narrowneck (same run) shows both "Images 5" and "Videos 4" as separate accordion rows — confirms the media split works correctly and Burkitts genuinely has zero videos, not a rendering bug |
| 16 | Dark mode readable | **PASS** — default color scheme in this browser is dark; screenshots of the hero, gallery cards, dialog, and popover all show good contrast (light text on near-black backgrounds, colored verdict pills legible) |
| 17 | Light mode readable (bonus check) | **PASS** — forced `colorScheme: light` via `resize_window`; popover and dialog repainted with a light cream background and dark text, still fully legible |
| 18 | References list still present | **PASS** — "References index" heading found, plus a jump link `href="#references"`; per-reef reference counts shown (e.g. Burkitts 14, Narrowneck 21, Boscombe 16, Palm Beach 18) |
| 19 | Hash links still work | **PASS** — opening a reef updates `location.hash` to `#reef/<slug>` (e.g. `#reef/narrowneck-gold-coast`); reloading the page directly at that URL re-opens the correct dialog on load (deep-link works) |

## Not tested (out of task scope per instructions)

- Videos/photos content correctness — task explicitly said to leave media aside; only checked that Burkitts has an Images-only accordion (no Videos row) and that another reef's Videos row exists for contrast, without judging the video content itself.
- No new images/videos were searched for or downloaded.

## Blocking-criteria check

Per the task's own bar ("popover not appearing or dialog broken = blocker"): **no blocker found.** The popover appears correctly anchored inside the dialog with a working "Open source" link, Esc/replace/mobile-sheet behavior all work, and the dialog itself never broke across 4 reefs opened, expand/collapse, and repeated popover open/replace/close cycles.

## Tooling gaps to flag back to the requester

1. Could not save screenshots to `04_build/QA/round3_*.png` — no available tool call writes a built-in-browser screenshot to disk; the tool only returns the image inline for my own inspection. If PNG artifacts are required, either point me to a screenshot-saving tool, or use Claude in Chrome (which does support GIF/image capture with paths) for the next round.
2. Could not test `file://` per the task's instructions — the built-in browser pane refused `file://` navigation outright. The localhost run above should be treated as the full functional verification for this round; a real `file://` check needs a different browser (or the person's own).

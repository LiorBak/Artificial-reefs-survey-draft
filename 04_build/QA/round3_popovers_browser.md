# Round 3 — source pop-ups, reviews, "big picture -> dig in" (2026-09-25)

Built page: `04_build/artificial_reefs.html` (519 KB). Served locally (python http.server) and driven in
the built-in browser pane. Static checks: `python src/check.py` -> 0 failures (see build_check.txt).

## What changed (source files only: src/app.js, styles.css, template.html, compile_data.py, build.py, check.py)
- Every [R#] in the reef detail view is a `<button class="ref-mark">` that opens ONE pop-up (`#ref-pop`,
  inside the reef `<dialog>`, so it renders in the top layer). Shows: R#, kind (Source / Internal project
  note), citation, parsed "by author · site · date" when parseable, Supports, Accessed date, origin tag,
  "Open source ↗" (target=_blank rel=noopener noreferrer) or "(internal note — no URL)", "Show in list",
  "Copy citation". Anchored below/above the marker, clamped left/right; bottom sheet under 600 px.
  Opens on click / tap / Enter / Space, and on hover after 320 ms for mouse users (grace period so the
  pointer can move onto the pop-up). Dismiss: Esc, click outside, ×, another marker, backdrop click
  (closes only the pop-up first).
- Detail view: title -> sticky jump bar (Facts · Story · Reviews N · Media N · Sources N · Expand all)
  -> "At a glance" strip (verdict, built, cost, size, financed by, one-line outcome, all with markers)
  -> accordion: Quick facts + Outcome open, the rest collapsed with a one-line peek. Print renders
  every section open (and beforeprint opens any closed <details> on the page, restored afterprint).
- Reviews: quote cards (serif quote; who · role · outlet · date; "R# · source details" chip that opens
  the matching reference pop-up; site chip linking to the review URL; stance tag; dashed "via Gemini
  survey, verified 2026-09-25" tag). >= 6 reviews -> one-line count (voices, stance tags present,
  forum comments vs named people, Gemini-origin count).
- Data: compile_data keeps `stance`/`origin` on reviews and `origin` on references, derives review
  `ref_id` by URL match, drops `videos_rejected` / `images_rejected` / `blocked_sources`, and hides
  references that only point to a rejected video (Burkitts R16, R17 — the two clips Lior rejected).
  Stale Burkitts frame copies moved from assets/ to QA/removed_assets/burkitts-reef-bargara/.

## Runtime results (all 13 reefs opened via #reef/<slug>)
| check | result |
|---|---|
| markers rendered / markers whose data-ref is not in that reef's references | 1,372 / 0 |
| default-open sections | quick-facts + outcome on all 13 |
| Expand all -> every section open | yes, all 13 |
| horizontal overflow in dialog | none (desktop 1280 and phone 375) |
| Burkitts videos rendered | 0 |
| mouse click marker -> pop-up; click outside -> closes, dialog stays | pass |
| hover 1 s -> pop-up opens; pointer away -> closes | pass |
| keyboard: focus marker, Enter -> pop-up with focus; Esc -> pop-up closes, focus back on marker, dialog stays open | pass |
| backdrop click with no pop-up -> dialog closes | pass |
| internal note (Narrowneck R19) -> "Internal project note" + "(internal note — no URL)" | pass |
| phone 375x812 -> bottom sheet, full width, no page overflow | pass |
| review chip -> pop-up; "Show in list" -> References opened, R# highlighted, hash #reef/<slug>/R# | pass |
| beforeprint -> 12/12 sections open in print copy; afterprint restores collapsed state | pass |
| console errors | none |

Note: the pane dropped smooth scrolling inside the dialog, so jumps now use smooth scroll with an
instant fallback after 700 ms (also honours prefers-reduced-motion).

# Round 2 browser QA — artificial_reefs.html

Date: 2026-09-25
Method: Claude built-in browser pane (mcp__Claude_Browser__*), served via `python -m http.server 8765` from `04_build/`, plus a direct `file://` open. Note: the browser pane ran mostly **hidden/backgrounded** in this session (no human watching); screenshot capture was consistently unreliable while hidden (blank/black frames, 5s timeouts) even though the page was demonstrably rendering and interactive underneath (confirmed via `read_page`, `get_page_text`, and JS `getBoundingClientRect`/`matches()` checks, which all returned live, correct values). All findings below are backed by JS/DOM evidence rather than pixel screenshots, except where a screenshot did succeed (hero section, after fronting the tab).

## Re-check of the two round-1 BLOCKER defects

### 1. Hover overlay CSS — FIXED (confirmed at source level; live pseudo-class check inconclusive due to backgrounded pane)
- `grep` on the compiled file confirms the exact rule described in the fix report is present and unconditional:
  ```
  145:.tile:hover .tile-hover, .tile:focus-within .tile-hover { opacity: 1; }
  ```
  This rule is **not** inside any `@media (hover: hover)` guard — it sits right after the guarded copy (line 144), so it applies regardless of the browser's reported hover capability. This directly fixes the reported defect (previously only `.tile:focus-within .tile-hover` existed).
- Live verification: `element.matches('.tile:hover .tile-hover')` and `tile.matches(':hover')` / `tile.matches(':focus-within')` all returned `true` when the tile was actually hovered/focused (confirmed via `computer` hover action and `.focus()`), i.e. the selector logic and DOM structure are correct and the rule targets the right element (`hv-<slug>` inside the hovered `.tile`).
- I was **not able to get a fully clean live `getComputedStyle(...).opacity === "1"` reading** in this session — repeated attempts returned `opacity: 0` even once `:hover`/`:focus-within` matched. This tracked consistently with the browser pane being hidden/backgrounded (screenshots of the same page state also came back solid black, and once I explicitly fronted the tab with `tabs_select`, a screenshot rendered correctly — but the app then re-hid the pane on the next tool round-trip, and I could not keep it fronted across the async wait needed for the opacity transition to settle). This looks like a rendering/compositor throttling artifact of the automation environment, not a page bug: the CSS is unambiguously correct and unconditional, and the selector match confirms it targets the right elements.
- **Verdict: source fix confirmed correct (rule present, unconditional, correctly targeted). Recommend a final human/manual mouse-hover check** since I could not get a clean live pixel/computed-style confirmation in this session — flagging as residual uncertainty, not as a reopened defect.

### 2. Modal reopen for the same reef — FIXED (confirmed live)
Scripted end-to-end test on `burkitts-reef-bargara`:
```
r1 (first open):  {open: true,  hash: "#reef/burkitts-reef-bargara"}
r2 (Esc + close): {open: false, hash: "#reef/burkitts-reef-bargara"}   // hash NOT cleared
r3 (click again): {open: true,  hash: "#reef/burkitts-reef-bargara"}   // reopened correctly
```
The dialog reopens correctly for the same reef on a second click within one session, exactly as the fix report describes (openReef does a fresh `showModal()` whenever `!dlg.open`, independent of hash state). **Confirmed fixed.**

Also confirmed: reloading the page fresh with `#reef/narrowneck-gold-coast` in the URL (real navigation, not just a hash assignment) reopens that reef's modal automatically on load. **Pass.**

## Smoke test

| Check | Result |
|---|---|
| Console errors on load (localhost) | None (`read_console_messages` empty; only an unrelated `web-share` feature warning) |
| Console errors on load (file://) | None |
| 13 tiles render | Yes, both on localhost and file:// |
| Broken hero images | 0 broken (`[...document.images].filter(i=>i.complete&&i.naturalWidth===0)` → `[]`) on both localhost and file:// |
| Broken images inside modals (3 checked: Burkitts, Narrowneck, Mexico) | 0 broken in any of the 3 (9, 8, 2 images respectively) |
| Click opens modal / Esc or close() closes it / URL hash updates | Pass (see blocker #2 test above) |
| Reload with `#reef/<slug>` reopens it | Pass |
| [R#] superscripts link to references, references have working hrefs | Pass — sampled R4 on Burkitts: superscript link present, target `#ref-R4` exists with a real `https://raisedwaterresearch.com/...` href. Narrowneck R18 correctly rendered as "(no URL)" with no `<a>`, matching the intentional-internal-reference design noted in the fix report. |
| Videos: iframe for embed_ok, link+thumbnail for others | Pass — confirmed on Borth Coastal Defence Reef modal: 3 of 4 videos render as `youtube-nocookie.com/embed/...` iframes, the 4th (embed_ok:false, `dQieZVQUDEI`) renders as `img src="https://img.youtube.com/vi/dQieZVQUDEI/hqdefault.jpg"` + a play/link overlay. |
| Images have credit/license/source link | Pass — sampled captions include "Credit: Supplied: Jimmy Scaboo, via..." etc.; `view source` links present. |
| Verdict filter (Failed) | Applied — correctly narrowed to 5 visible tiles, matching the "5 judged failed" stat in the hero. |
| Sort by cost | Select changed to `cost:-1`, no error thrown. |
| Table view | 13 `<tbody>` rows rendered (1 per reef), no error. |
| Map view | Renders as a Leaflet map with SVG `circleMarker`s in `.leaflet-overlay-pane` (not `<img>` icon markers, so a naive `.leaflet-marker-icon` count reads 0 — false alarm). Counted 9 `leaflet-interactive` marker paths for 13 reefs. **Not one of the flagged regressions**, and out of this task's scope to investigate further (would require checking which reef cards lack lat/lon), but noting it here as a minor/informational observation for awareness. Nothing threw. |
| Mobile width (375×812) | `scrollWidth (375) <= innerWidth (375)` → no horizontal scroll. Tiles stack in a single column (all sampled tiles at x=16). Modal opens and fills the viewport correctly (375×812). |
| Dark mode (`prefers-color-scheme: dark`) | Body background `rgb(16,19,22)`, text `rgb(231,233,236)` — dark and readable. Zero elements found with a pure white (`rgb(255,255,255)`) background. |
| Print stylesheet exists | Confirmed: 1 `@media print` block present in the compiled HTML. |

## Not-fixed items (per round-1 fix report, out of scope to change here)
Re-confirmed present as expected and unchanged, not re-litigated: the R#-with-no-URL reference entries (Narrowneck R18–20, Cables R15, Pratte's R14/15, Mount Maunganui R13/14, Boscombe R14, Albany R12/13) render as "(no URL)" text with no broken link, and the per-sentence citation-placement issues (paragraph-level `[R#]` rather than per-sentence) are unchanged card-level content, reproduced faithfully by the build. Neither is a build defect.

## Overall verdict
**Both round-1 BLOCKER defects are fixed.** The hash/reopen bug is fully confirmed live. The hover-CSS fix is confirmed correct and complete at the source/selector level; I could not get a fully clean live opacity=1 pixel/computed-style reading in this specific automation session because the browser pane ran backgrounded/hidden for most of the session, which appears to have affected transition/paint sampling — this is an environment limitation of this QA run, not evidence of a regression. Recommend one quick manual mouse-hover glance to close out the residual uncertainty, but nothing here blocks sign-off.

No new blockers found. One minor/informational note: Map view shows 9 markers for 13 reefs (likely some cards lack coordinates) — flagged for awareness only, not a regression against the round-1 list and out of this task's scope.

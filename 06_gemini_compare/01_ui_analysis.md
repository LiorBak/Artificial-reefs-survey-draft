# UI/UX comparison — Gemini's build vs ours (read-only analysis)

Scope: section 1 (world surf reefs) only. Gemini's folder was read-only; nothing was
copied into our data/build files. No new media was searched for or downloaded.
No live-browser screenshots were captured this pass — the built-in browser pane cannot
open `file://` pages, and the Claude-in-Chrome extension reported "not connected" when
tried. Everything below comes from direct code reading of
`C:\Users\lior\Documents\Gemini\AG\artifical reef\05_web_build\index.html` (grep/sed,
full read of the relevant JS/CSS blocks) plus our own `04_build\src\app.js` for
comparison. If Lior wants pixel screenshots too, say so and I'll retry with the browser
once the extension is reconnected.

---

## 1. How Gemini's citation system works (the "pop-up sources" Lior liked)

**Marker / trigger.** Every sourced claim, table cell, review, and reference-list row
carries a small pill button:
`<button onclick="showCitation(event,'bar_drimer_2023')" class="cite-btn">📖 Cite</button>`
(index.html lines ~601–762, 3047, 3056, 3077). The button text varies contextually —
sometimes "📖 Cite", sometimes the author name ("📖 Bar & Drimer 2023"), sometimes just
"📖 Notes" — but it's always the same `cite-btn` CSS class and the same `onclick`
pattern, `showCitation(event, '<citeKey>')`.

**Data source.** A single JS object `citationsRegistry` (line 1695, ~20 entries) keyed
by a slug like `bar_drimer_2023`, each entry holding:
`category` (an emoji-tagged label e.g. "🎓 Academic Peer-Reviewed Paper", "🏄 Surf
Journalistic Review", "🏛️ State Comptroller Audit"), `title`, `authors`, `year`,
`publication`, `apa_citation` (pre-formatted APA string), `url`, and `note` (1–3 sentence
plain-English gloss of what the source actually shows/proves, written by hand, not just
a citation dump — this is the highest-value ingredient).

**Popover markup.** One single hidden `<div id="cite-popover">` sits once in the page
(line 1172), reused for every citation. `showCitation()` (line 1788) just repoints its
contents: category pill → title → APA block (`select-all` CSS so it's one-click
copyable) → an optional "📐 Mathematical Derivation & Engineering Context" box built
from `note` → footer with "Open Source Document ↗" link and a "📋 Copy APA" button
(clipboard write with a 2s "✅ Copied!" confirmation, line 1864).

**Positioning.** Smart-anchored to the clicked button, not screen-centered: reads
`getBoundingClientRect()` of the trigger, places the popover `rect.bottom + 8px` below
it, clamps left edge so it never overflows the viewport right edge, and flips above the
trigger if it would overflow the bottom (lines 1827–1852). Falls back to
viewport-centered only if there's no click target (e.g. programmatic open). Width is
`min(440px, 92vw)` — this is what makes it work on mobile without a separate mobile
layout.

**Dismissal.** Three ways, all wired (lines 3567–3584): Escape key, an explicit ✕ button
in the popover header, and a document-level click listener that closes it if the click
lands outside the popover AND outside any `.cite-btn` (so clicking a different citation
button just re-targets the same popover instead of closing-then-reopening).

**What this buys them:** a reader can stay on the sentence they're reading, tap the
inline pill, see full APA + a one-line "why this matters" note + the live link, and
dismiss without losing place or scroll position. That's strictly better than jumping to
a bottom-of-dossier reference list and back (our current pattern).

### Our current mechanism, for contrast
`app.js` `refify()` (line 56) turns `[R#]` tokens into `<a href="#reef/<slug>/R#">`
anchors that jump to `<li id="ref-R#">` in the References section at the bottom of the
same open dialog (`refsHTML()`, line 52). It's an in-page jump (not a full navigation,
since it's all inside one `<dialog>`), so it isn't as bad as a real page reload, but it
does: (a) scroll the reader away from the sentence they were reading, (b) show only the
raw citation string + URL + "Accessed" date, no plain-English note of what the source
supports, (c) require a manual scroll-back to resume reading.

### Recommendation for our page
Add a citation popover, keyed off our existing `references[]` array (which already has
`id`, `citation`, `url`, `accessed`, `supports` — `supports` is basically Gemini's
`note` field, already there, just not surfaced this way).

Implementation notes against our src files:
- `app.js`: change `refify()`'s link mode from `href="#reef/.../R#"` to
  `onclick="showRefPopover(event,'${r.slug}','${id}')"` (keep the `href` as a fallback
  anchor for no-JS / print). Add `showRefPopover(evt, slug, refId)` mirroring Gemini's
  `showCitation()`: look up `BY_SLUG[slug].references` by `id`, fill a single reusable
  `#ref-popover` panel (title = `citation`, note = `supports`, link = `url`,
  "Accessed" date), position via `getBoundingClientRect()` exactly as Gemini does.
- `template.html`: add the one hidden `#ref-popover` div (reuse Gemini's layout: header
  pill + close button, citation text, optional "why it matters" box, footer with
  external link + a "Copy citation" button).
- `styles.css`: port the `.cite-btn` pill styling (small, monospace, rounded, subtle
  border, hover state) and `#ref-popover`'s fade-in animation + `max-w` clamp for
  mobile.
- Dismissal: reuse our existing dialog's Escape handling (`closeReef()` already listens
  for the dialog's native Escape) — add the same "outside click but not on a `.cite-btn`"
  listener Gemini uses, scoped inside `#reef-dialog` so it doesn't fight the dialog's own
  backdrop-click-to-close.
- Effort: **low**. All the data already exists in our `references[]`; this is a
  render-path change, not a data-model change. No new verification needed since we're
  not adding facts, just changing how existing verified references are displayed.

---

## 2. How Gemini presents surfer reviews

**Location.** A dedicated modal tab, "4. Surfer Reviews (N)" (line 1250), separate from
Overview/Design-vs-Reality/Outcomes/Haifa-Lessons/References/Paper-Figures/Videos — i.e.
reviews get their own first-class section instead of being folded into the general prose
(our `reviewsHTML()` renders reviews as one more `<section>` at the bottom of the single
scrolling dossier).

**Per-review fields** (from the `reviews[]` array on each reef object, e.g.
`narrowneck-gold-coast`): `quote` (verbatim), `reviewer` (name, sometimes a forum handle
like "linez" or "stunet"), `role` (e.g. "Gold Coast Surfer", "Swellnet Founder and
Editor" — this identifies whether the voice is a random commenter vs. a named expert),
`source` (publication/thread name), `date`, `url` (direct link to the original
comment/article), `type` ("press" tag, presumably also "forum"/"video" elsewhere),
`apa_citation` (optional, only for citable press pieces, null for anonymous forum
comments), and `cite_key` linking back into `citationsRegistry` for the fuller
citation-with-note popover.

**Card layout** (lines 3037–3060): italic serif blockquote of the verbatim quote → byline
row ("— reviewer (role)") → a `cite-btn` showing "📖 {source} [{date}]" that opens the
full citation popover (math/engineering note if relevant, APA, copy button) → a separate
"[Source ↗]" pill that's a direct external link to the original comment thread → if an
APA citation exists, a footer line with the full APA text plus a second
"[Full Citation & Notes ↗]" trigger.

**Stance / grouping.** Reviews are NOT pre-sorted into positive/negative bins — they're
shown in original array order, several conflicting voices back to back (e.g. Narrowneck
has both "never noticed a salient" skepticism and "Absolute waste of money" alongside a
founder's neutral on-site report). This is a deliberate "let conflicting witnesses speak"
approach rather than a curated single verdict — matches our own "conflicts between
sources are stated, not resolved" principle already in our footer text.

### Our current mechanism
`reviewsHTML()` (line 415) already has most of the same fields conceptually: `who`,
`role`, `outlet`, `date`, `quote_or_summary`, `url` — rendered as a plain `<ul class="reviews">`
list, each item a blockquote + one metadata line with `extLink()`. What's missing versus
Gemini: (a) no visual separation between "named expert" and "anonymous commenter" voices,
(b) reviews are just another section in the linear dossier scroll rather than a
dedicated tab a reader can jump straight to, (c) no APA/full-citation drill-down per
review — the review's `url` is the only source pointer, no "why this source matters"
note.

### Recommendation for our page
- Give reviews their own top-level tab/anchor inside the reef dialog rather than a
  mid-scroll section — cheap because our dialog is already a single scrolling document;
  this just needs a small in-dialog nav (see item 3 below, same mechanism would serve
  both).
- Reuse the citation-popover work from item 1: attach the same `showRefPopover()` (or a
  thin `cite_key` variant) to each review's source instead of a bare `extLink()`, so a
  reader can see the review's provenance without leaving the review.
- Visually distinguish reviewer authority tier (named professional vs. forum handle) —
  a one-word `role` badge is enough; we already store `role`, just add a small
  `<span class="role-tag">` styled differently when `role` contains a title like
  "Editor"/"Founder"/"Engineer" vs. a bare handle. Low effort, cosmetic only.
- Effort: **low-medium**. Data model barely changes (optionally add `apa_citation`/
  `cite_key` fields, but these can be omitted and the feature still degrades cleanly).

---

## 3. Big-picture → dig-in navigation pattern

Gemini's reef modal has **8 numbered tabs** across the top of the dialog body (line
1246–1254): 1. Overview & Motivation, 2. Design vs Reality, 3. Outcomes & Post-Mortem,
4. Surfer Reviews (N), 5. Lessons for Haifa, 6. Academic References (N), 7. Paper
Figures & Sediment (N), 8. Video Footage (N). Each tab is a `.modal-content-pane`
toggled by `switchModalTab()`, with review/reference/video/figure **counts baked into
the tab label itself** (`<span id="modal-tab-rev-count">`) so a reader sees at a glance,
without opening the tab, whether there's anything there (e.g. "Academic References (12)"
vs "(0)").

The card grid itself (before opening a reef) already surfaces a compact synopsis on
hover (dimensions/cost/year/outcome) before the click — i.e. there are genuinely three
zoom levels: grid tile (name + hero stat) → hover tooltip (headline metrics) → click →
full 8-tab dossier. That's the "big picture, dig in as far as you like" structure Lior
is describing.

Two more things worth flagging that reuse the same "annotate the summary, let the
citation carry the depth" idea:
- **Scale Comparison tab** (top-level, not inside a reef — line 277): four sub-views
  (Grid / Master composite image / Interactive overlay / Historical archive image /
  Methodology) that let a reader compare all ~16 structures' real-world footprints on one
  coordinate frame, with an "Interactive Overlay" mode (`renderInteractiveOverlay()`,
  line 2061) that lets you toggle by material/submergence/typology and click a structure
  to jump straight to its citation via `openCurrentOverlayCite()` — i.e. the scale-compare
  view is itself wired into the same citation-popover mechanism.
- **Methodology sub-tab** (line 646) explains, in plain prose with inline `cite-btn`
  citations, exactly how every $L_x$/$W_y$/$A_f$ measurement was derived (georeferencing
  method, salient-vs-tombolo formula from Hsu & Silvester 1990, wave-refraction threshold
  from Bar & Drimer 2023) — this is documentation-as-content, letting a skeptical reader
  audit the numbers instead of just trusting a table.

### Recommendation for our page
- We already have gallery/map/table top-level views plus a per-reef dialog — the
  missing piece is **in-dialog tabs**. Splitting our current single long scroll
  (`detailHTML()`, line ~466: Quick facts → sections → reviews → images → videos →
  Lior's figures → references) into tabs (Overview / Design vs Reality-equivalent if we
  have discrepancy content / Reviews / References / Media) would let readers who want
  "just the reviews" or "just the references" jump there without scrolling past photos.
  This is mostly a CSS/markup reorg of `detailHTML()` plus a `switchTab()`-equivalent in
  `app.js`; the section content generators (`reviewsHTML`, `refsHTML`, `imagesHTML`,
  `videosHTML`) barely change.
- Put the reference/review/video **counts in the tab labels** — trivial (`.length`
  already available on each array) and gives readers the same at-a-glance signal.
- A world-scale footprint comparison view (all our verified reefs' real dimensions on
  one coordinate frame) is a nice-to-have but is out of scope right now per the "no new
  media" instruction if it needs new artwork; if we already have footprint numbers in
  our verified JSON, a lightweight SVG-based version (no images, just drawn rectangles
  to scale) would fit the "no new media" constraint — flagged under "consider later"
  below rather than "adopt now" since it's a bigger lift.

---

## 4. Other notable elements

- **Copy-to-clipboard APA button** on every citation popover — trivial, nice touch,
  costs nothing to add once the popover exists (item 1).
- **Provenance/conceptual-evaluation disclosure banner** for the one speculative
  (Haifa-proposed) entry (line ~3086: "⚠️ CONCEPTUAL EVALUATION (?) PROVENANCE NOTICE"
  distinguishing verified-empirical inputs from synthesized/evaluated conclusions).
  Good practice for any conceptual/proposed (non-built) entry we might carry; we don't
  currently have a proposed/speculative reef in section 1 scope, so this is a pattern to
  keep in mind rather than something to build now.
- **Theme toggle persisted to localStorage** (`initTheme`/`toggleTheme`, lines
  1714–1741) — standard, low effort if we don't already have dark mode (need to check
  our `styles.css`; not verified in this pass since it's out of the requested scope).
- Reef modal tabs are keyboard/Escape-aware and the same Escape handler also closes the
  citation popover, the scale modal, and other overlays in one keystroke (line 3567) —
  worth copying the "one Escape handler closes whatever's open" pattern rather than
  wiring Escape per-widget.

---

## Where ours is already better (keep)

- **Verification discipline**: every fact in our cards carries a mandatory `[R#]` tag
  resolved against a `references[]` array with `accessed` date and `supports` field;
  Gemini's `note` field is richer prose but nothing in Gemini's data model enforces that
  *every* claim traces to a citation the way our `[R#]` convention does.
- **Print/export path** (`preparePrint()`, `detailHTML(r, true)` mode) — Gemini's build
  has no equivalent single/all-reefs print view.
  Confirmed absent: no `@media print` or `window.print()` in Gemini's `index.html`.
- **Table view and map view** as first-class alternate views of the full reef set (our
  `setView('map'|'table'|'gallery')`) — Gemini's top-level tabs are World Reefs / Scale
  Comparison / (others), with no plain sortable table and no map view of all reefs by
  location.
- **Deep-linkable state**: our `#reef/<slug>/R#` hash routing means any reef+reference
  combination is a shareable URL; Gemini's modal open/close doesn't appear to update
  `location.hash` (no `history.pushState`/`replaceState` call found in the file), so a
  Gemini reef view isn't bookmarkable/shareable.
- **Accessibility basics**: our dialog uses the native `<dialog>` element with focus
  management (`lastFocus`, `focus({preventScroll:true})` restore on close) and
  `aria-label`s on reference links; Gemini's modal is a plain `div` with `hidden` toggling
  and no evidence of managed focus-trap/return-focus logic in the sections read.
- **Footer methodology statement** — ours states the verification method up front
  project-wide; Gemini scatters similar disclosure per-structure (the conceptual-eval
  banner) rather than as a standing site-wide policy statement.

---

## Ranked "adopt now" list (fits section 1, no new media, ranked value/effort)

1. **Citation pop-up popover** (replace jump-to-bottom refs with an anchored popover) —
   highest value/effort ratio; reuses existing `references[].supports` data;
   implementation is `app.js` (`refify`, new `showRefPopover`), `template.html` (one new
   hidden div), `styles.css` (port `.cite-btn` + popover styles). No new verification
   needed — displays only facts we've already verified.
2. **Reviews get a distinct in-dialog tab/section with a role badge + inline citation
   popover on the source**, instead of a plain end-of-page list — reuses #1's popover
   mechanism, so marginal effort is small once #1 exists.
3. **In-dialog tabs (Overview / Reviews / References / Media) with counts in the tab
   labels** — bigger reorg of `detailHTML()`, but no new data needed, pure
   markup/render-path change.
4. **"Copy APA" clipboard button** and **one shared Escape handler closing whatever's
   open** — trivial additions once #1 exists.

## Consider later (bigger lift or needs data we may not have verified yet)

- A world-scale footprint-comparison SVG view drawing all verified reefs to one metric
  coordinate frame (no photos/images needed if done as drawn rectangles, so it could
  respect the "no new media" rule, but it's a real feature build, not a tweak).
- A "conceptual vs. verified" provenance banner pattern, to keep in reserve for if/when
  we ever add a proposed (not-yet-built) structure to our verified set.
- Any adoption of Gemini's *specific* review quotes, sources, or citation entries into
  our own `<slug>.json`/`<slug>.md` — per the task rules, none of that content may enter
  our cards until an independent agent has fetched each cited URL and confirmed the
  quote/fact against the live source; that verification work was out of scope for this
  UI/UX pass and was not done here.

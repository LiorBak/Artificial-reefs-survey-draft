# Task: academic-level source audit (Lior, 2026-10-10)

Lior: "Make sure all sources are documented - academic level. Each statement should have a source. The model should say its
sources and how each one was used. If another method was used in the process, say it. Also be clear about assumptions and
decisions."

## The standard (apply to every file you audit)
1. **Every statement has a source.** Every number, date, dimension, level, cost, quality claim and verdict carries a reference
   that a reader can follow: full citation (authors, year, title, venue/publisher, volume/pages or report number, DOI/URL,
   access date for web pages) and the exact location (page, figure, table, section; for images the registry id).
   Personal communications: name/role, medium, date ("Zoom interview with Troy, Airwave founder, 8 Oct 2026, reported by Lior").
2. **Each source says how it was used.** For each source of a model: what was read off it (values, contours, outline), how
   (digitised by colour / traced by hand / read by eye / OCR / georeferenced with N control points / fitted), the accuracy of
   that reading, and which model element it feeds (plan, crest, seabed, tides, volume, validation only, context only, rejected
   and why).
3. **Methods are explicit.** Every processing step that is not a direct reading is named and explained: interpolation (which,
   parameters), smoothing, lofting, extrapolation, camera fitting, datum conversion (formula and source of the offset),
   gradient fits, any script (path) that produced a number. If an AI tool (Gemini) or an earlier agent's estimate influenced
   anything, say so and how it was checked.
4. **Assumptions are labelled.** Each assumption is a numbered item (A1, A2, ...) with: what is assumed, why (no source / which
   evidence suggests it), its effect on results (sensitivity, e.g. "+-0.5 m bed = +-19 % volume"), and what would replace it.
   Every place the assumption is used or shown says ASSUMPTION (or "assumed").
5. **Decisions are logged.** Each choice between alternatives (default outline, datum reading, rejected source, Lior's
   decisions D1-D9) is a numbered item with: options, who decided (Lior / agent / orchestrator) and when, and the reason.
6. **Confidence** per model element (plan, crest, seabed, tides, volume) with the reason, and an overall confidence.
7. **Consistency.** The same number has the same value and source in METHODS_3D.md, SOURCES_3D.md, shape.json, model.js /
   docs.js (what the viewer shows), the reef card (02_research/reefs/<slug>.json/.md) and the image registry. Fix or list
   every mismatch.
8. **The viewer shows it.** The model's own viewer (3d/index.html, its Sources / Methods panels, built from docs.js) must let a
   reader see: the source list with "how used", the methods, the assumptions list and the decisions list. If a panel is
   missing one of these, add it in the model's own build (build_3d.py / docs template), rebuild, and check it renders.

## How to work
- Read CLAUDE.md, `_agent_briefs/common.md`, this file, and the folder's `HANDOFF.md`. Then audit with grep and short reads;
  do not re-read the primary sources unless a citation detail or page number is missing or doubtful (then check that one).
- Use WebSearch (it works) to complete citations (authors, venue, pages, DOI). WebFetch/curl/downloads do not work. Never invent
  a citation detail: if not confirmed, write "not confirmed" and add it to REQUESTS_FOR_LIOR.md (append only).
- Write the result as a table in a new file `SOURCE_AUDIT_2026-10-10.md` in the folder you audit: statement/number -> source ->
  location -> how used -> status (ok / fixed / missing / mismatch). Then fix what you can in place.
- Do NOT change model values. If the audit finds a wrong value, record it and the evidence and tell main (do not rebuild a
  model with new numbers). Rebuilding only to refresh documentation (docs.js) is allowed; compare model.js before/after and
  confirm only text changed.
- Page texts in 04_build/data (models3d_curated.json, models3d_caveats.json): do NOT edit; list exact old -> new for main.
- Finish: HANDOFF.md line, short dated entry appended to 05_qa/00_STATUS.md via bash `cat >> file <<'EOF'`.

## Hard rules
NEVER install packages. Never run git. Never edit 04_build/ or papers/. Edit only your own folder(s); shared root files get
appends only (many agents run in parallel). Keep each file's line endings (several use CRLF). No whole-file dumps; view each
image once downscaled to <=1200 px; scratch files to /tmp. If near a limit, checkpoint in HANDOFF.md and stop with HANDOFF_STOP.
End with a ```json summary: counts (statements checked, ok, fixed, missing, mismatches), citations completed, assumptions and
decisions listed, viewer panels added/fixed, values that look wrong (for main), page text edits for main.

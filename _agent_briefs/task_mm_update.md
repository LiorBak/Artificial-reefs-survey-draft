# Task: Mount Maunganui update (queue item 1; started 2026-10-07)

**Folder.** `07_scale/shapes/mount-maunganui-reef/`; `3d/` holds the 3D work.

**Checkpoint.** `HANDOFF.md` section 0, then `3d/SOURCES_3D.md` "CHECKPOINT (2026-10-07, stopped ...)". Follow its ordered TO DO.
This file adds the decisions and papers that arrived since then.

**Read.**
- `CLAUDE.md`, `_agent_briefs/common.md`, this file, `HANDOFF.md`, and the CHECKPOINT section.
- From `_agent_briefs/model_3d.md`, only the STEP 0 and OUTLINE VERSIONS sections.
- Open any other file only for a specific fact. If something is unclear, ask "main" with SendMessage.

## Decisions (Lior, 2026-10-07)
- **D1, as-built bed.**
  - Default bed = **−3.6 m CD**, labelled **ASSUMPTION** in the viewer, `model.js` and `METHODS_3D.md`.
  - Option **"later seabed" = −2.8 m CD**, because later surveys give −2.4 to −3.3 m.
  - The reef must stay below the water line. Crest is −0.9 m CD. Check the crest against every water level the viewer shows. If any part would rise above the lowest level, report it; do not clip.
- **Bed selector.** Add a seabed-scenario selector in the viewer, built like the versions selector, with an (i) text and a `#bed=<id>` hash.
  - In `model.js`, record `bed_scenarios[{id,name,z_cd,z_msl,source,note}]` and `default_bed`.
  - Keep every `model.js` path the page reads. Find them with `grep -o "{{[^}]*}}"` in `04_build/data/models3d_curated.json` and `04_build/data/models3d_caveats.json`.
  - If a path must change, list it in your final JSON under `tokens_changed`.

## Papers (in `papers/`, Lior's folder: read only, never move)
- **P2. Mead, Black & Moores (2007),** Coasts & Ports 2007. It is a scan with no text layer.
  - OCR pages 2-6 with `07_scale/tools/ocr_windows.ps1`, and view the figure pages downscaled.
  - CORRECTION (agent, confirmed by main 2026-10-07): the "Fig. 3 design 6,500 m³ vs as-built survey 2,800 m³" is Fig. 3 of **P3 (Mead & Borrero 2011, PDF p3)**, not P2. P2's own Fig. 3 is a 1:20 physical-model plan; P2 Fig. 12 = Oct 2006 unfinished bathymetry, Fig. 8 = container layout. Use P2 for design/construction facts. The as-built candidate below = **P3 Fig. 3 (bottom)**:
  - P3 Fig. 3: design 6,500 m³ (top) vs as-built survey 2,800 m³ (bottom). Lior's caption: "The 2 containers end to end on the left of the picture are the replacements for the damaged and removed 60 x 6 m container."
  - Register the figure (image rule).
  - If Fig. 3 (bottom) has a usable scale, grid or contours:
    - trace it as a new outline version, "As-built survey (Mead & Borrero 2011 Fig. 3)" with the survey date if the paper gives it;
    - make it the default. Reason: it is the earliest measured survey of the completed reef, and the rules are measured survey > design > photo, and 3D = as-built.
  - If its geometry is too poor to trace, keep the 2013 multibeam as the default and write down why.
  - Also extract slopes, crest levels, the seabed level and construction notes, each with its page or figure.
- **P3. Mead & Borrero (2011),** Coasts & Ports 2011.
  - Take the Mount Maunganui facts: performance, as-built, monitoring.
  - Add them to `HANDOFF.md`, and to the reef card `02_research/reefs/mount-maunganui-reef.json/.md` as new references `[Rn]` in the card's existing format. Edit only this reef's card.

## Volumes
Recompute the volume table for each outline version × each bed scenario. Keep the "model vs stated 2,800 m³" comparison.

## Do NOT
- edit `04_build` (main refreshes the page with `update_page.py` after you finish);
- run git;
- touch other reefs' folders.

## Finish
- **Docs:**
  - `HANDOFF.md`: up to 300 lines; rewrite section 0.
  - `3d/SOURCES_3D.md`: the log.
  - `3d/METHODS_3D.md`.
- **Images:** registry rows, with `for_3d_check` cleared.
- **Previews:** run `render_previews.py` and view the results downscaled.
- **Root files:**
  - `REQUESTS_FOR_LIOR.md`: D1 applied; P2 and P3 used.
  - `05_qa/00_STATUS.md`: an entry for this task.
- **Checkpoint:** after each finished TO DO item, update the CHECKPOINT so a fresh agent can continue.

## Final JSON
{"slug","default_outline","bed_default_cd","bed_option_cd","volume_m3":{"<version>/<bed>":n},"p2_fig3_used":bool,"images_registered":n,"tokens_changed":[],"open_issues":[]}

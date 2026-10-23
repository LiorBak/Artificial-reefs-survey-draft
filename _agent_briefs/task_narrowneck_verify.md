# Task: Narrowneck verification finish (queue item 2, stage 1 of 2; started 2026-10-07)

**Folder.** `07_scale/shapes/narrowneck-gold-coast/`.

**Checkpoint.** `VERIFY.md` "CHECKPOINT (2026-10-07, stopped for Lior's usage limit)". Follow its 10-step TO DO.
Checks 1-3 are done; `shape.json` is still marked "traced".

**Read.**
- `CLAUDE.md`, `_agent_briefs/common.md`, this file, `HANDOFF.md`, and the CHECKPOINT section.
- From `_agent_briefs/verify_shape.md` and `07_scale/SHAPE_SPEC.md`, only the sections you need ("Outline versions" in the spec).
- For Gold Coast data, read only the Narrowneck parts of `07_scale/bathymetry/gold_coast/REPORT.md`.
- If something is unclear, ask "main" with SendMessage.

## Scope: stage 1 = verification and outline versions only
A fresh agent will build the 3D model afterwards (stage 2). If you finish early, do not start the 3D model. Instead, write a 3D plan in `HANDOFF.md`: datums, crest, seabed sources and versions.

## Key points
- **Scale conflict.** Corbett et al. (2023) Fig. 2 shows crest loops of ~85-90 m; Jackson Fig. 7 shows 60-62 m.
  - Decide which scale is wrong, using independent references: the measured scale of the 2020 z19 photo, the Esri Wayback georeference, known objects, and dimensions stated in the texts.
  - Document the method and the result.
- **Built state, Corbett 2023 (P1, in `papers/`).**
  - Option 2 was built: crest −2.5 m AHD (= −1.5 m LAT), crest 20 m seaward, south reef rotated 5°.
  - The north reef is nearly complete; the south reef and the bridge are partly built.
- **Outline versions** (spec "Outline versions").
  - Default = the 2020 photo trace (Esri Wayback r9812, 2020-08-08, z19), because it shows the reef as actually built.
  - Toggles, as listed in the CHECKPOINT: Corbett Option 2 renewal design, the earlier design, the 2011 survey relief, and Navionics (indicative only: the verifier found an open U-shape, not closed loops).
  - Lior has not yet chosen between the photo and the Option 2 design as default. Add it as **D7** in the root `REQUESTS_FOR_LIOR.md` section 5 if it is not there. State the recommendation and why.
- **Confidence.** Keep it honest. If the scale conflict cannot be fully resolved, say so.

## Do NOT
- edit `04_build`;
- run git;
- touch other reefs' folders.

## Finish
- **Narrowneck files:**
  - `shape.json`: status "verified" (or "verified with issues"), plus `outline_versions` and `default_outline`;
  - `VERIFY.md`: checks completed;
  - `HANDOFF.md`: up to 300 lines, including the stage-2 3D plan.
- **Images:** registry rows for any new images (image rule).
- **Root files:**
  - `REQUESTS_FOR_LIOR.md`: D7, plus the Navionics "0.9" item if still open.
  - `05_qa/00_STATUS.md`: an entry for this task.
- **Checkpoint:** after each TO DO step, update the CHECKPOINT in `VERIFY.md`.

## Final JSON
{"slug","status","default_outline","versions":[{"id","area_m2"}],"scale_conflict":"resolved|open + why","confidence","images_registered":n,"open_issues":[],"plan_3d_written":bool}

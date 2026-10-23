# Narrowneck stage 1 (verification and outline versions): agent report, 2026-10-10 (cloud)

Saved by the orchestrator from the agent's hand-back. Details: `VERIFY.md` (step log), `HANDOFF.md` (status, 3D plan).

## Outcome
- `shape.json` status: **verified with issues**. Default outline stays the 2020 photo trace (Esri Wayback r9812, 2020-08-08).
- Cut-off run audit: the earlier run had finished step 1 (scale conflict) and checkpointed. Partial work after it was four
  exploratory `step2_*.py` scripts (Windows paths, no outputs, no notes): discarded; step 2 redone. Everything else was
  complete and consistent with the checkpoint (recorded in `VERIFY.md`).

## Scale conflict: none
- Corbett 2023 Fig 2 crest loops "85-90 m" was an eye estimate; measured on the figure's 50 m bar they are about 71 m, and
  both reefs' total crest is 119 m (text: 120 m).
- Corbett Option 1 and Jackson Fig 2 are the same CAD design on one scale, so Jackson Fig 7 60-62 m holds within about 3 %.

## Built state
- Corbett 2023: Option 2 was built; north reef nearly fully achieved, south reef and bridge partly. No post-renewal as-built
  survey; only the 2017 pre-works multibeam (Corbett Fig 3, img-55).

## Option 2 placement
- First placement used a wrong inter-panel offset (Option 2 on top of Option 1, against the caption); corrected using the
  grey Option 1 outline in the right panel (logged in `VERIFY.md`). Option 2 crest is then 22-25 m seaward of the 2004
  design (text: 20 m); 96.6 % of the traced reef lies inside the Option 2 envelope. A 2 px hand patch closes the south loop
  where a label broke the line. Placement uncertainty about +-10-15 m.

## Versions (`outline_versions` in shape.json)
| version | area m2 | confidence |
|---|---|---|
| photo_2020-08-08 (default) | 6,239 | medium; lower bound (deeper toe not visible) |
| design_option2_2017 (-6 m envelope) | 13,941 | medium-low; concept drawing, south reef partly built |
| design_2004_revised (-6 m envelope) | 13,631 | medium-low; pre-renewal |
| survey_2011-06-09 relief zone | 4,922 | low; pre-renewal, no depth legend (3,000-7,000 by threshold) |
| navionics_4.0m_shoals | 537 | low; indicative only |
Also 24 faint seaward patches (663 m2) stored in shape.json, outside every outline.

## Images
14 new images registered (img-54..img-65 and overlays attached to 4 existing rows): Corbett 2023 figures and tables,
including the 2017 pre-works multibeam (img-55, 3D check pending). Lines added to `03_images/reefs/NEW_IMAGES_LOG.md`.
`check_registry.py` passes for Narrowneck (other reefs' failures, e.g. Boscombe sha, are not from this run).

## Open issues
- Option 2 placement +-10-15 m; south reef and bridge only partly built.
- Crest datum ambiguity 0.24 m (MSQ AHD = LAT + 0.76 vs the papers' LAT - 1.00).
- Deeper toe (to about 10 m) not visible; the photo footprint is a lower bound.
- Corbett Fig 3 multibeam not digitised (img-55); other pending 3D-check rows img-01, 04, 14, 24, 31, 50, 51.
- Gemini re-fetch not possible from the cloud (WebFetch could not resolve the hosts); Jackson 2012 confirmed from the local
  PDF; nothing from Gemini used. Black & Mead 2001 paywalled.
- Navionics "0.9" label needs Lior's app reading at -27.9866, 153.4341.

## Decisions for Lior
- D7 default outline: keep the 2020 photo (agent recommends) or Corbett Option 2.

## Next
Stage 2 (3D model, brief `model_3d.md`) from the 3D plan in `HANDOFF.md`.

# Task: seabed fixes for Borth (D6) and Boscombe (D2) (queue item 3; started 2026-10-07)

**Folders.**
- `07_scale/shapes/borth-coastal-defence-reef/3d/`
- `07_scale/shapes/boscombe-surf-reef/3d/`

**Read.**
- `CLAUDE.md`, `_agent_briefs/common.md`, this file, and the two `HANDOFF.md` files (`07_scale/shapes/<slug>/HANDOFF.md`).
- Open the named sections of `METHODS_3D.md` only when you edit them.
- If something is unclear, ask "main" with SendMessage.

Both fixes change only the context seabed outside the reef. They are applied as recommended in REQUESTS D2 and D6 (Lior was told "proceeding unless you object"), and they are reversible. Before editing, copy each model's current `model.js` (and any seabed file you will change) to `3d/archive/pre_D6/` or `3d/archive/pre_D2/`.

## Borth, D6
The problem and the fix are in Borth `HANDOFF.md`, open issue 1 and next-step 2.
- **The problem.** The model seabed seaward of the reef (y > 335 m) is **0.89 m deeper** than the HRPP576 Fig. 2 −4.0 m contour (sd 0.14, n 13).
- **The fix.**
  - Add the Fig. 2 −4.0 contour, outside the reef zone, as seabed nodes.
  - Start the EMODnet gradient from that contour.
  - Change `seabed_nodes` / `seabed_grid` in `b3d_lib.py`; nodes beyond `ANCHOR_Y` are currently ignored.
- **Rebuild:** `build_3d.py --shape`, `nav_read.py annotate`, `make_annotations.py`, `register_images.py`; then re-render the previews and view them downscaled.
- **Acceptance:**
  - model minus the −4.0 contour: |mean| < 0.2 m;
  - the −3.0 and −2.0 contour checks do not get worse;
  - volumes under the rock: originally "UNCHANGED" (31,336 / 30,091 / 26,400 m³ for lidar_2022 / design_1020 / sat_2024).
    REVISED 2026-10-07 (main approved option B). The old grid clamped y to ANCHOR_Y = 335, so the design bed nodes at y 360/385
    were ignored. Volumes may now change only through that bed-node fix, documented. Agent's numbers: 30,132 / 28,929 /
    25,505 m³ (−3.4 to −3.9 %).
  Report the new Navionics and EMODnet differences too.
- **Update:** `METHODS_3D.md` sections 3.3, 4.4 and 7, the viewer's "Seabed in this model" note, `HANDOFF.md`, and root REQUESTS D6 → "applied <date>".

## Boscombe, D2
The details are in Boscombe `HANDOFF.md`, item 12 and open issue 1; the data is in `offshore_tilt_check.json` and `nav_z16_offshore.json`.
- **The fix.** Flatten the offshore extension alongshore (row y = 380 and seaward), keeping the EMODnet cross-shore gradient. This is the context zone only; the reef zone and beach stay unchanged.
- **Expected result.** Navionics offshore r.m.s. drops from 1.20 m to ~0.5 m (0.46 m with the EMODnet gradient).
- **Acceptance:** the reef volume and crest numbers are unchanged; the alongshore trend is ~0.
- **Update:** `METHODS_3D.md`, `HANDOFF.md`, and root REQUESTS D2 → "applied <date>". Re-render the previews.

## Do NOT
- edit `04_build`. Main refreshes the page with `update_page.py`, and edits the typed "0.89 m" caveat there from the numbers you report;
- run git;
- touch other reefs.

## Finish
- `05_qa/00_STATUS.md` entry.
- Checkpoint in each `HANDOFF.md` after each fix: do Borth first, then Boscombe.

## Final JSON
{"borth":{"minus4_contour_mean_m_before":-0.89,"after":x,"minus3_after":x,"minus2_after":x,"volumes_unchanged":bool,"nav_diff_m":x,"emodnet_diff_m":x},"boscombe":{"nav_rms_before":1.20,"after":x,"trend_per_100m_after":x,"reef_unchanged":bool},"files_changed":[],"page_text_to_update":["exact old text -> new text for main"],"open_issues":[]}

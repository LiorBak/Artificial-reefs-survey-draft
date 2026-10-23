# Next steps - start here

**2026-10-15: PRIORITY = Lior's course paper (deadline ~1 day). Plan: `08_paper/PLAN.md`. Rounds: 1 gather, 2 compute+figures, 3 write, 4 verify+PDF. Page work below is on hold.**
 (written 2026-10-11, end of the cloud session)

Read `CLAUDE.md` first, then this file. Agent rules: `_agent_briefs/common.md` (items 10-11 are new: check `papers/` first;
log dead ends). Source standard: `_agent_briefs/task_source_audit.md`. Who did what: `_agent_briefs/orchestrator.md` section 7.
Lior's to-do list: `REQUESTS_FOR_LIOR.md` (✅ = done/received).

## State on 2026-10-11
- Page tabs: Gallery, Table, 3D only (Map/Scale removed 2026-10-10, archived in `archive/04_build_removed_2026-10-10/`).
- 3D models: Borth, Boscombe, Bunbury, Mount Maunganui, Narrowneck, Palm Beach, Pratte's on the page; Cables (verified on
  WA DoT surveys, 3D medium) and Albany (3D LOW) added 2026-10-11.
- Hidden shapes (no plan source; Lior: "don't show shapes you don't know"): Opunake, Kovalam, Mexico, Burkitts.
- Every reef dialog: Google Maps link; "Checked, nothing useful" section from `02_research/dead_ends/<slug>.json`.
- Network: environment set to Full on 2026-10-10 (web pages, imagery, PDFs reachable; login and bot-check sites still are not).

## STATE 2026-10-14 00:10 UTC (all agents stopped; nothing running) - resume here first
Task prompts: `_agent_briefs/workflows/reef-small-tasks-2026-10-13c.js`. Each folder's HANDOFF.md has the details/CHECKPOINT.
| task | state | next |
|---|---|---|
| Opunake uploads | DONE: consent area 189 x 94 m at -39.45943, 173.85163; design 99 x 30 x 3.5 m, ~4,900 m3; no bag layout, shape stays hidden | main: card/page coords + size per `07_scale/shapes/opunake-reef/FEASIBILITY.md`; Lior: show consent area? |
| Albany uploads | DONE (HANDOFF_STOP): no as-built levels in the uploads, 3D geometry unchanged (LOW); timeline fixed (first rock 18 Mar 2025, storm 26 May, opened 16 Jul 2025); ~18 rocks moved late Feb 2026 (note); 70,000 t sensitivity; full refs list; W8 picture (GA portal 403) | main: apply `3d/PAGE_TEXTS_FOR_MAIN.json` key `_update_2026-10-13`; Lior: W8, D12, E9 |
| Cables fixes | DONE (HANDOFF_STOP): default label fixed; refs list; datum A12 closed: AHD = Fremantle chart datum + 0.716 m (Roelse et al. 1975 DNM TR12 Table 3), reading A kept; HAT/LAT not found (e-mail draft for Lior) | main: apply its PAGE_TEXTS; fix the 'Crest level' caveat quote that no longer matches METHODS_3D.md (page check fails) |
| SeaDataNet + Kovalam | DONE: CDI 117452 = 1982230 (Poole Bay, UKHO 2011-12), 115084 = 1981385 (Cardigan Bay, 1969 single-beam); datums behind a bot check, so W1/W2 go to Lior with click figures; Kovalam card fixed (Rendle 4,300 m3, bbox explained); web.archive nothing new; Navionics no map in headless Chrome | Lior: W1/W2 figures in each reef's `3d/annotated/` |
| OCR MM 2007 (Haiku) | DONE: `05_qa/papers_intake/P2_mead_black_moores_2007_ocr.md` + index `P2_mead_black_moores_2007.md`; not proof-read (check numbers on the page image) | optional: check '900 m3' and '30 x 1.5 m' on the image |
| Page map links | MOSTLY DONE (HANDOFF_STOP), 04_build/HANDOFF.md 0d: coords + Copy, Google Maps, satellite, Google Earth web, per-reef and all-reefs KML (outline only for shown reefs) in dialog, gallery tile menu, 3D header; check.py 262 PASS | 1) fix the 2 build failures (Albany image without caption label; Cables 'Crest level' quote); 2) Navionics link: use `https://maps.garmin.com/en-US/marine?maps=another-brand&overlay=false&key=<12-char geohash>` (worked on Lior's PC 2026-10-05; Kovalam example key t9qxxwgbpf4n); 3) EMODnet/GEBCO links (test in 0d); 4) gallery tile grows when menu open; then `update_page.py --full` until "state saved" |
The page is NOT rebuilt with these changes yet. First job tomorrow: items in the last row, apply the Albany/Cables PAGE_TEXTS, rebuild, commit.

## Last page build: 2026-10-11, `update_page.py --full` state saved (check.py 247 PASS, qa_models3d 191 PASS). 9 models on the
page incl. Cables and Albany; dead-ends sections rendered. Details: `04_build/HANDOFF.md` section 0c.

## Small fixes left (quick, do first)
- Cables `3d/model.js` labels version `design_plan_original_1999` "(default)" but the default is `survey_surface_1999_11` (fix in its build_3d.py, rebuild).
- Cables and Albany `3d/METHODS_3D.md`: the 'References' section is a one-line pointer; make it a real list (the page currently takes them from REGISTER_3D.md).
- Kovalam card: add Rendle 4,300 m3 and the bbox mismatch 43x24 vs 38x29 m.
- Albany viewer fixed in `07_scale` 2026-10-11 (pile height is above the seabed); `VIEWER_FIXES` in `04_build/src/compile_models3d.py` is now a no-op and can be removed.

## Queue (in order of value; one agent each, brief = the task file named)
1. **Lior's new uploads** (`new uploads from lior/`; Lior's folder like `papers/`: never move or rename). Not yet read by any agent.
   - Opunake: `Opunake Artificial Reef monitoring programme 2005-2009.pdf` (TRC, P15) and `New Zyland Geographic.pdf` (P16,
     design figure). May finally give a plan -> `trace_shape.md`, then decide whether Opunake can be shown. Cite fully; update card.
   - Albany: `Albany-Artificial-Surf-Reef-Community-Update-and-FAQs.pdf` + 3 Raised Water Research pages (design, construction,
     "moved rocks"). Check for as-built levels, crest, seabed, changes after construction; update the Albany 3D (now LOW: seabed
     from RHDHV 2015 contours, datum assumed AHD, 1.6 m conflict with BMT 2018), card references, dead ends. One RWR page may
     concern another Australian reef: check which.
2. **EMODnet W1/W2 (Boscombe, Borth survey metadata)**: Lior asked us to try the SeaDataNet portal ourselves first:
   https://cdi.seadatanet.org/search (records 117452, 115084, 1982230). Only if blocked: give Lior a figure of the coast with
   the exact point to click and what to copy.
3. **W8 Albany GA portal**: https://portal.ga.gov.au/persona/marine is only a map to Lior. Give exact lat/lon (reef centre
   -35.018, 117.921) and an annotated screenshot of where to click and which layer, or fetch the data directly (GA services
   gave 403 before: do not bypass).
4. **Kovalam**: retry web.archive.org copies (surfer.com article, ASR brochure) now that the network is Full; Navionics in the
   headless Chrome at /opt/pw-browsers (no login; if it needs one, stop).
5. **Cables**: Fremantle chart datum (LWD) to AHD offset (Transport WA), closes the 0.2-0.3 m datum gap (A12 in its METHODS_3D.md).
6. **OCR**: the Mount Maunganui 2007 PDF in `papers/` has no text layer. Orchestrator installs tesseract quietly (CLAUDE.md), an
   agent writes the text to `05_qa/papers_intake/` (never into `papers/`).
8. Optional: photo-match buttons for Narrowneck, Cables, Albany (`04_build/src/photo_match.py` model_rings / scene_map).
9. Mexico: nothing to do until coordinates or a plan appear.

## Lior's open decisions (REQUESTS_FOR_LIOR.md section 6)
D3, D4, D5, D8, D9 (Burkitts: Phase 3 zone now located, LOW, kept hidden), Cables default (surveyed 1999 surface, now default,
vs design plan + extension), Bunbury shown as a 12 m circle from a drone photo (hide if Lior prefers).

# Orchestrator playbook - for the MAIN session only (agents do not need this file). Written 2026-10-07.

## 1. Role
- You orchestrate: plan, write or point to briefs, spawn agents, check their results, and report to Lior.
- Agents do the research and build work. Lior: "you should orchestrate, not do the work". Small checks are fine
  (grep, a downscaled screenshot, a one-line fix).
- Start each session with:
  - `CLAUDE.md`;
  - this file;
  - the last 2-3 entries of `05_qa/00_STATUS.md`;
  - `REQUESTS_FOR_LIOR.md`.

## 2. Agents
- **Spawning.** Use Sonnet agents (general-purpose, model sonnet, in the background). In the cloud there is NO cap (Lior, 2026-10-10: "we have a lot of credits, run all agents simultaneously"); the old 3-agent cap was for the PC. Parallel agents: one agent per folder; shared root files get appends only; new 3D models are listed in `04_build/data/models3d_hold.json` until their agent finishes; only one agent edits `04_build` at a time. Spawn only work Lior
  has given the go for.
- **Prompts.** Each prompt names:
  - the files to read: `CLAUDE.md`, `_agent_briefs/common.md`, the task brief, and the folder's `HANDOFF.md`;
  - the exact checkpoint section;
  - the TO DO list.
  Tell the agent not to re-read the sources its HANDOFF already summarises, and to ask "main" (SendMessage) instead of reading
  everything.
- **Restarts.** Never resume a large agent (~300k tokens); subagents cannot be /compacted. After a usage-limit stop, or once an
  agent is large, start a FRESH agent from its checkpoint (HANDOFF.md, the round LOG, 3d/SOURCES_3D.md, VERIFY.md CHECKPOINT).
- **Endings.** Agents end with a ```json summary, or with `HANDOFF_STOP:` / `NEEDS_CLARIFICATION:`. The harness may refuse to let
  a subagent write a "report" file. If so, save it yourself from the hand-back.
- **Usage window.** When Lior's 5-hour usage window nears its end:
  - most agents checkpoint and stop;
  - the page (04_build) agent may run on to its next checkpoint.
- **Reporting.** After a page change, show Lior 2-3 downscaled screenshots (`04_build/QA/...png`) and say what changed. Agents
  take their screenshots in their OWN headless Chrome (random free port, fresh `--user-data-dir`), never in a shared browser.

## 3. Running in the cloud (Linux) instead of Lior's Windows PC
- **Python.** Run `pip install -r requirements.txt`. The scripts were tested on Python 3.14; 3.11 or later should work.
- **Chrome.**
  - Needed for: the page QA and the export of the combined "All (compare)" meshes (`04_build/src/export_combined.py`, run by
    `build.py` / `update_page.py`).
  - Install Chromium, e.g. `pip install playwright && python -m playwright install --with-deps chromium`.
  - `04_build/src/qa_cdp.py` and `qa_shots.py` look for Chrome in this order:
    1. `CHROME_PATH`;
    2. the Windows paths;
    3. chrome / chromium on PATH;
    4. Playwright's Chromium in `~/.cache/ms-playwright`.
    So after the install above nothing needs setting.
  - Suggested cloud setup script:
    `pip install -r requirements.txt playwright && python -m playwright install --with-deps chromium && apt-get install -y tesseract-ocr`.
- **OCR.** `07_scale/tools/ocr_windows.ps1` is Windows-only. On Linux use tesseract: `apt-get install tesseract-ocr`, then
  PyMuPDF's OCR text page or pytesseract. P2 (Mead, Black & Moores 2007) is a scan with no text layer.
- **Network.** Research steps fetch web pages, Esri Wayback tiles, EMODnet, Navionics web charts and papers. The environment
  needs internet access beyond package registries.
- **Hard-coded paths.** About 47 one-off research scripts under `07_scale/` and `05_qa/` use Windows paths. They were already run
  and their outputs are saved. Re-running one means first switching it to repo-relative paths. The page pipeline
  (`04_build/src`) uses relative paths.
- **Gemini folder.** It is not in the repo. Our verified extracts are in `06_gemini_compare/` and
  `07_scale/00_gemini_footprints_extract.*`. Only the final wrap-up (`wrap_report.md` → `SOURCES_AND_GEMINI_REPORT.md`) may need
  more. If it does, ask Lior to add a read-only snapshot.
- **Viewing the page.** Lior views it on his PC: pull the repo, then open `04_build/artificial_reefs.html` (or
  `Artificial reef launcher.html`). Its 3D viewers are separate HTML files under `04_build/3d/`.

## 4. Lior's recorded decisions and defaults (details in REQUESTS_FOR_LIOR.md section 5 and the reef HANDOFFs)
- **D1, Mount Maunganui as-built bed (decided 2026-10-07).**
  - Default −3.6 m CD, written explicitly as an ASSUMPTION.
  - Option "later seabed" −2.8 m CD: later surveys give −2.4 to −3.3. Check the reef stays below the water line (crest −0.9 m CD).
  - Not yet applied to the model.
- **Borth.** Default outline = Welsh Government LiDAR 2022, confidence high. Toggles: design drawing 1020 and the 2024 satellite
  photo. The oval is the BREAKWATER.
- **D2, Boscombe.** Flatten the offshore extension alongshore. Told Lior "proceeding unless you object"; no objection so far.
- **D6, Borth offshore seabed.** Add the HRPP576 Fig 2 −4.0 m contour as nodes and start the EMODnet gradient there.
  Recommended; still open.
- **Bunbury.** Verdict FAILED, despite the developer's claim.
- **Narrowneck default outline.** The 2020 photo (Esri Wayback r9812, 2020-08-08), unless Lior chooses the Corbett 2023
  Option 2 design. Open.
- **Page tabs (Lior, 2026-10-10).** Only Gallery, Table and 3D models. The Map and Scale (2D) tabs are removed (code archived, reversible); traced outlines stay reachable through the 3D outline versions and reef files.
- **Lior, 2026-10-10:** (1) "Don't show the shape of reefs you don't know": no outline on the page unless a real plan source exists (survey, scaled drawing, or clearly visible structure in a dated georeferenced image). Hidden: Mexico, Opunake, Burkitts (platform is not the reshaped zone), Kovalam (scale unknown). (2) Keep a Google Maps link per reef (location) on the page although the Map tab is gone. (3) D7 agreed: Narrowneck default = 2020 photo. (4) Pratte's J1: paper datum (MLLW) as now; J2 our call (+-150 m). (5) Depth/app readings: later; keep them in REQUESTS_FOR_LIOR.md "Later". (6) Bunbury/Albany: Zoom interview with Troy (Airwave founder), 8 Oct 2026, as a source.
- **Source standard (Lior, 2026-10-10):** academic level: every statement sourced (full citation + location), each source says how it was used, methods explicit, assumptions (A#) and decisions (D#) listed, shown in each model viewer. Brief: `_agent_briefs/task_source_audit.md`.
- **Network (cloud):** Lior set the environment to Full network on 2026-10-10 (evening); web pages, tiles and downloads work now.
- **Navionics/Garmin.** Used without login. Their datum is inferred by RMS against an independent survey.
- **Photo-match tolerance.** 2 m (or 10 % of length for reefs under 40 m); 4 m for georeferenced pictures. Set by the page agent;
  not yet confirmed by Lior.

## 5. Work queue (each item restarts only on Lior's go; checkpoint files in brackets)
1. **Mount Maunganui update.** RUNNING since 2026-10-07; task file `_agent_briefs/task_mm_update.md` (see section 7).
   - OCR P2 pages 2-6 (design/construction facts). The as-built survey figure (2,800 m³ vs design 6,500 m³) is Fig. 3 of P3
     (Mead & Borrero 2011), not P2; it may give a measured default outline.
   - Apply D1.
   - Add facts from P3 (Mead & Borrero 2011).
   - Then run `update_page.py`.
2. **Narrowneck.** Stage 1 (verification and versions) RUNNING since 2026-10-07; task file `_agent_briefs/task_narrowneck_verify.md`.
   Stage 2 (the 3D model, brief `model_3d.md`) starts after it, from the 3D plan in its `HANDOFF.md`.
   - Resolve the scale conflict: Corbett 2023 Fig 2 crest loops ~85-90 m vs Jackson Fig 7 60-62 m.
   - Versions: 2020 photo (default), Corbett Option 2, the 2004 design, 2011 survey relief, Navionics (indicative only).
   - Then build the 3D model.
3. **Seabed fixes.** RUNNING since 2026-10-07; task file `_agent_briefs/task_seabed_fixes.md`. Covers Borth D6 and Boscombe D2 in
   their `3d/` folders, then `update_page.py`. The Borth "0.89 m" caveat text is
   typed by hand (`04_build/UPDATE_PROTOCOL.md`).
4. **Boscombe from Rendle 2016** (P5, 343 pp): as-built bag layout, crest levels, survey datum.
5. **Papers intake.** P3 (Mead & Borrero 2011) and P8 (Blacka et al. 2013): per-reef facts and figures into cards, HANDOFFs and
   the image registry.
6. **Palm Beach 3D re-check:** `model_3d.md` STEP 0, plus `07_scale/bathymetry/gold_coast/REPORT.md` section 5.3.
7. **Pratte's re-verify:** the `pending_reverification` block in its `shape.json`.
8. **HANDOFF.md** for Pratte's, Bunbury, Palm Beach and `07_scale/bathymetry/*` (they predate the HANDOFF rule).
9. **Remaining reefs:** trace, verify and 3D, or a FEASIBILITY.md, for Cables, Opunake, Kovalam, Albany, Burkitts and Mexico
   (briefs `trace_shape.md`, `verify_shape.md`, `model_3d.md`).
10. **Full page build** (`build_shapes_videos.md`): the Shapes, Images, Videos review and Methods tabs.
11. **Browser QA** (`qa_browser.md`).
12. **Wrap-up** (`wrap_report.md`): `07_scale/METHODS.md` (academic methods paper) and `SOURCES_AND_GEMINI_REPORT.md`.
13. **Cleanup.** Archive or delete smoke tests and temporary scripts (e.g. `04_build/src/qa_round11.py` if it is temporary).
    Folders stay ordered.

**Small page fixes for the next page round:**
- Palm Beach labels are oversized in the "Palm s4" photo-match view.
- At 900 px height, Borth's version block pushes its viewer below the fold.
- Optional: a version toggle in "All (compare)".
- Fold in whatever Lior reports after viewing the page.

## 6. Lior's own open items
All of them are in `REQUESTS_FOR_LIOR.md`:
- papers P4 (optional) and P7 (only via the City of Gold Coast);
- e-mails E1-E8 (Claude never sends e-mail; drafts on request);
- browser pages W1-W3;
- Navionics app and Google Earth readings;
- decisions D2-D6;
- the media review (`05_qa/media_recheck_summary.md`).

## 7. Running agents (live table: update it when you start or finish an agent, and commit)
| Started | Task file | Work folder | Checkpoint a fresh agent continues from | Status |
|---|---|---|---|---|
| 2026-10-07 | `_agent_briefs/task_mm_update.md` | `07_scale/shapes/mount-maunganui-reef/` | `HANDOFF.md` section 0 + `3d/SOURCES_3D.md` CHECKPOINT | STOPPED 2026-10-07 (clean). Done: P2 OCR + figures, P3 read, Fig 3 check (not traced: corroborates the toe version), Oct 2006 bed read. NEXT (fresh agent): D1 in code (bed selector, bed_scenarios), volume table version x bed, register the 16 saved figures (img-23..38), card [Rn] refs, previews - from `3d/SOURCES_3D.md` "CHECKPOINT (2026-10-07 b ...)" |
| 2026-10-07 | `_agent_briefs/task_narrowneck_verify.md` | `07_scale/shapes/narrowneck-gold-coast/` | `VERIFY.md` CHECKPOINT + `HANDOFF.md` | CUT OFF by the usage limit 2026-10-07 (no new checkpoint written). Fresh agent: start from the old `VERIFY.md` CHECKPOINT, but first list files in the folder changed on 2026-10-07 after it (partial work of the cut-off run) |
| 2026-10-07 | `_agent_briefs/task_seabed_fixes.md` | Borth and Boscombe `3d/` | each reef's `HANDOFF.md` (Borth first) | Borth D6 DONE 2026-10-07; Borth page texts + `update_page.py --full` DONE 2026-10-10 (cloud). Boscombe D2: see the 2026-10-10 row below |
| 2026-10-10 | `_agent_briefs/task_mm_update.md` | `07_scale/shapes/mount-maunganui-reef/` | `3d/SOURCES_3D.md` CHECKPOINT (2026-10-07 b) + `HANDOFF.md` section 0 | DONE 2026-10-10: D1 in code (bed -3.6 ASSUMPTION / -2.8), volume table, img-23..38, card R16-R17; page refreshed. Report `3d/REPORT_D1_2026-10-10.md`. D8 open |
| 2026-10-10 | `_agent_briefs/task_narrowneck_verify.md` | `07_scale/shapes/narrowneck-gold-coast/` | `VERIFY.md` CHECKPOINT + `HANDOFF.md` | DONE 2026-10-10: verified with issues; scale conflict resolved (none); 5 outline versions, default 2020 photo; img-54..65 registered. Report: `REPORT_stage1_2026-10-10.md`. Page refresh not needed (no 3D yet) |
| 2026-10-10 | `_agent_briefs/task_seabed_fixes.md` (Boscombe part) | `07_scale/shapes/boscombe-surf-reef/3d/` | `HANDOFF.md` | DONE 2026-10-10: D2 applied; Navionics rms 1.20 -> 0.51 m, reef unchanged. Report `3d/REPORT_D2_2026-10-10.md`. Page texts edited; page refresh pending (after the MM agent) |
| 2026-10-10 | `_agent_briefs/model_3d.md` (Narrowneck stage 2) | `07_scale/shapes/narrowneck-gold-coast/3d/` | `HANDOFF.md` 3D plan | DONE 2026-10-10: 3D built, confidence medium. Report `3d/REPORT_stage2_2026-10-10.md`. PENDING main: merge `3d/MAIN_TYPED_TEXTS.json`, remove hold, update_page (after the page agent); card additions from P3/P8 || 2026-10-10 | queue item 4 (Boscombe from Rendle 2016, P5; prompt only, no task file) | `07_scale/shapes/boscombe-surf-reef/` (notes, card, images; model NOT changed) | `HANDOFF.md` | DONE 2026-10-10: no model change needed; img-33..40, card R17. Report `REPORT_P5_2026-10-10.md`. Follow-up: METHODS wording (built crest) || 2026-10-10 | page agent (prompt only) | `04_build/` (remove Map + Scale tabs; small page fixes) | `HANDOFF.md` | RUNNING (fresh cloud agent) |
| 2026-10-10 | `model_3d.md` STEP 0 (queue 6) + HANDOFF (queue 8) | `07_scale/shapes/palm-beach-gold-coast/` | `HANDOFF.md` | DONE 2026-10-10: 9 flagged images agree, geometry unchanged; HANDOFF written. Page texts pending in `05_qa/pending_page_edits/palm-beach_2026-10-10.json` (apply after the page agent) |
| 2026-10-10 | `verify_shape.md` (queue 7) + HANDOFF (queue 8) | `07_scale/shapes/prattes-reef-el-segundo/` | `HANDOFF.md` | DONE 2026-10-10: re-verified, nothing changed; img-37/38; HANDOFF written. Page texts pending in `05_qa/pending_page_edits/prattes_2026-10-10.json` |
| 2026-10-10 | housekeeping (queue 8 + Boscombe P5 wording) | Bunbury, `07_scale/bathymetry/*`, Boscombe METHODS wording | `HANDOFF.md` | DONE 2026-10-10: Bunbury + emodnet + gold_coast HANDOFFs; EMODnet REPORT.md complete; Boscombe built-crest wording. TODO main: re-run Boscombe `3d/build_3d.py` (docs.js/provenance label only) before the next page refresh |
| 2026-10-10 | papers intake P3 + P8 (queue 5) | `05_qa/papers_intake/` + image registries (cards: main applies later) | notes files | DONE 2026-10-10: facts for 8 reefs, 25 figures registered, 9 contradictions with cards listed. Cards: applied by the next row for 5 reefs; narrowneck, cables, kovalam after their agents |
| 2026-10-10 | apply P3/P8 card additions (prompt only) | `02_research/reefs/` borth, boscombe, mount-maunganui, opunake, prattes | the notes files | DONE 2026-10-10 (contradictions kept side by side with sources) |
| 2026-10-10 | apply P3/P8 to the Narrowneck card (prompt only) | `02_research/reefs/narrowneck-gold-coast.*` | the notes files | DONE 2026-10-10 (R22-R24; contradictions kept) |
| 2026-10-10 | `trace_shape.md` / `verify_shape.md` / `model_3d.md` (queue 9) | `07_scale/shapes/cables-reef-wa/` | `HANDOFF.md` | DONE 2026-10-10: traced (medium, design plan Blacka 2013 Fig A.2) + 3D (low; RL datum A/B switch). Report `REPORT_2026-10-10.md`. PENDING page agent: add to the page (hold, combined/curated/caveats) |
| 2026-10-10 | `trace_shape.md` / `verify_shape.md` / `model_3d.md` (queue 9) | `07_scale/shapes/opunake-reef/` | `HANDOFF.md` | STOPPED 2026-10-10: feasibility only (text size ~90 x 20 m, 27 bags; not visible on Esri 2025 z20; no plan/survey). Not yet checked: papers/ and the Gemini footprint extract. Restart when the network is Full (LINZ, Esri Wayback) or Lior supplies Black et al. 2004 |
| 2026-10-10 | `trace_shape.md` / `verify_shape.md` / `model_3d.md` (queue 9) | `07_scale/shapes/kovalam-reef-india/` | `HANDOFF.md` | STOPPED 2026-10-10: low-confidence photo trace (one oblique photo, scale free: 640-1,681 m2); per Lior's rule NOT shown on the page. No 3D. Needs a vertical image (Wayback/Google Earth 2010-12) or ASR/CESS reports. P3/P8 card additions pending |
| 2026-10-10 | `trace_shape.md` / `verify_shape.md` / `model_3d.md` (queue 9) | `07_scale/shapes/southern-ocean-surf-reef-albany/` | `HANDOFF.md` | DONE 2026-10-10: traced + verified (high; self-verified): default Bluecoast design outline 13,104 m2, toggle Esri 2026-01-20 visible reef 10,918 m2; length 157-165 m vs City 165 m. No 3D (no seabed/pile height/slopes): FEASIBILITY. img-10 volume corrected 54,000 -> 34,000 m3. Restart 3D with network Full or Lior's Navionics/Bluecoast report |
| 2026-10-10 | `trace_shape.md` / `verify_shape.md` / `model_3d.md` (queue 9) | `07_scale/shapes/burkitts-reef-bargara/` | `HANDOFF.md` | DONE 2026-10-10: traced + self-verified (low): visible rock platform, Esri 2025-09-05, 31,485 m2 (south edge cut); NOT the moved-boulder zone (no source locates it). No 3D (no crest/seabed/datum). Restart with network Full |
| 2026-10-10 | `trace_shape.md` / `verify_shape.md` / `model_3d.md` (queue 9) | `07_scale/shapes/mexico-reef-2026-unnamed/` | `HANDOFF.md` | DONE 2026-10-10: FEASIBILITY only (no coordinates, size or plan; 2 underwater photos). Needs: coordinates / design plan / Xala MIA, or network. Lior: show the analogy envelope or no shape? || 2026-10-10 | `_agent_briefs/task_source_audit.md` | `07_scale/shapes/borth-coastal-defence-reef/` | `SOURCE_AUDIT_2026-10-10.md` | DONE: 34 checked, 10 fixed; new 3d/REGISTER_3D.md (sources used, A1-A14, DEC1-DEC14) in the viewer; model.js identical; no page edits. Card: size quotes the superseded two-reef design |
| 2026-10-10 | `_agent_briefs/task_source_audit.md` | `07_scale/shapes/boscombe-surf-reef/` | `SOURCE_AUDIT_2026-10-10.md` | DONE: 34 checked, 11 fixed; METHODS section 9 (sources used, A1-A16, BD1-BD12, confidence, AI statement); model values unchanged. Page edits: `05_qa/pending_page_edits/audit_boscombe_2026-10-10.md` |
| 2026-10-10 | `_agent_briefs/task_source_audit.md` | `07_scale/shapes/bunbury-airwave/` | `SOURCE_AUDIT_2026-10-10.md` | DONE: 29 checked, 6 fixed; fill disagreement recorded (A14, DEC12, L12); card lat/lon 2 km off. Page edits: `05_qa/pending_page_edits/audit_bunbury_2026-10-10.md` |
| 2026-10-10 | `_agent_briefs/task_source_audit.md` | `07_scale/shapes/mount-maunganui-reef/` | `SOURCE_AUDIT_2026-10-10.md` | DONE: 31 checked, 11 fixed; viewer tabs Sources/Assumptions (A1-A14)/Decisions (M1-M15); BoPRC = Dahm & Gibberd 2013. Page edits: `05_qa/pending_page_edits/audit_mount-maunganui_2026-10-10.md` |
| 2026-10-10 | `_agent_briefs/task_source_audit.md` | `07_scale/shapes/palm-beach-gold-coast/` | `SOURCE_AUDIT_2026-10-10.md` | DONE: 28 checked, 7 fixed; source-use table, A12-A14, DEC1-15 in Methods; model.js identical. Page edits: `05_qa/pending_page_edits/audit_palm-beach_2026-10-10.md` |
| 2026-10-10 | `_agent_briefs/task_source_audit.md` | `07_scale/shapes/prattes-reef-el-segundo/` | `SOURCE_AUDIT_2026-10-10.md` | DONE: 35 checked, 6 fixed; J1/J2 applied (D6, D10 +-150 m); viewer sub-tabs Sources/Assumptions/Decisions/Confidence; numbers unchanged. Page edits: `05_qa/pending_page_edits/audit_prattes_2026-10-10.md` |
| 2026-10-10 | `_agent_briefs/task_source_audit.md` | `07_scale/shapes/narrowneck-gold-coast/` | `SOURCE_AUDIT_2026-10-10.md` | DONE: 47 checked, 13 fixed; D7 recorded as Lior's; viewer chips Sources/Assumptions (A1-A16)/Decisions; survey date 19 Jul 2018 fixed. Page edits: `05_qa/pending_page_edits/audit_narrowneck_2026-10-10.md` |
| 2026-10-10 | `_agent_briefs/task_source_audit.md` | `07_scale/shapes/cables-reef-wa/` | `SOURCE_AUDIT_2026-10-10.md` | DONE: 45 checked, 6 fixed (max thickness text 2.9 -> 2.5 m); A1-A11, X1-X8, how-used table; PAGE_TEXTS_FOR_MAIN.json revised |
| 2026-10-10 | `_agent_briefs/task_source_audit.md` | non-3D shapes: albany, burkitts, kovalam, opunake, mexico | `SOURCE_AUDIT_2026-10-10.md` | DONE: 67 checked, 10 fixed, 8 open mismatches (listed in pending_page_edits); FEASIBILITY 'why hidden' sections; A#/D# in shape.json |
| 2026-10-10 | `_agent_briefs/task_source_audit.md` | cards group A (7 cards with models) | `05_qa/source_audit/cards_group_A_2026-10-10.md` | DONE: 7 cards, verdict reasons, 31 refs added, coordinates fixed (Bunbury, Palm, Narrowneck, MM); 183 uncited number sentences -> follow-up agent |
| 2026-10-10 | `_agent_briefs/task_source_audit.md` | cards group B (6 other cards) | `05_qa/source_audit/cards_group_B_2026-10-10.md` | DONE: ~250 checked, ~75 fixed; unread SurferToday tags removed (Cables); Burkitts lat sign fixed. Follow-ups for main listed in the audit file (Opunake R4 unread, Albany 6-8 s attribution, Mexico 'unveiled' date, Burkitts/Bunbury coordinates, Kovalam cost check) || 2026-10-10 | card citations + fixes (prompt) | `02_research/reefs/*` | `05_qa/source_audit/cards_citations_2026-10-10.md` | DONE: 174 flagged, ~90 tagged, 11 derived, ~45 labelled; 8 fixes done (coords on 6 cards, Kovalam cost US$1.58 M, Opunake R4 untagged); unsourced leftovers listed in the report. Not on page until next build |
| 2026-10-10 | Albany 3D with network | `07_scale/shapes/southern-ocean-surf-reef-albany/` | `HANDOFF.md` | DONE: 3D built, confidence LOW (plan high; seabed from RHDHV 2015 contours, datum assumed AHD; BMT 2018 sounding conflicts by 1.6 m); design 34,000 m3 fitted (unfitted 20,826), satellite outline 30,273 m3. Page texts in 3d/PAGE_TEXTS_FOR_MAIN.json |
| 2026-10-10 | Cables imagery verification | `07_scale/shapes/cables-reef-wa/` | `HANDOFF.md` | DONE: verified (plan high, 3D medium) on WA DoT surveys 1998/1999/2002 + Esri imagery; default now Nov 1999 surveyed surface (4,049 m2, 4,671 m3 +-1,000); extension not confirmed (toggle); datum A kept, 0.2-0.3 m gap open; true position 32.0156 S 115.7485 E. Page texts revised in 3d/PAGE_TEXTS_FOR_MAIN.json |
| 2026-10-10 | Kovalam with imagery | `07_scale/shapes/kovalam-reef-india/` | `HANDOFF.md` | DONE (HANDOFF_STOP): no usable image (Wayback has nothing 2010-13; z17 2011-20 shows no reef); stays hidden, no 3D. Needs Lior: Google Earth Pro 2010-12, Navionics, ASR/CESS report |
| 2026-10-10 | Opunake with imagery | `07_scale/shapes/opunake-reef/` | `HANDOFF.md` | DONE: LINZ 2011-12/2021-22 and Wayback 2015-24 show no reef; stays hidden (no_source); 6 images registered. Needs Lior: NZ Geographic figure, TRC 2009-33, Black 2004, GE Pro 2007-10 |
| 2026-10-10 | Burkitts + Mexico with network | their `07_scale/shapes/` folders | `HANDOFF.md` | DONE: Burkitts Phase 3 work zone located (LOW, +-20-30 m; Redgard's later plan, not the 1997 works) - stays HIDDEN on the page by default (Lior's rule; D9 open); MSQ Burnett Heads tidal planes found; LiDAR NoData on platform, 3D not buildable. Mexico/Xala: nothing traceable. 25 dead ends logged |
| 2026-10-10 | page agent 2 (prompt) | `04_build/` | `04_build/HANDOFF.md` section 0b | DONE: 4 unknown shapes hidden (data-driven); dialog draws shape.json outlines (was old text footprints, e.g. Narrowneck 114,950 -> 6,239 m2); Google Maps links (dialog, tile, table); Sources-disagree section; build state saved. NEXT: final page agent after Albany, Cables, Burkitts/Mexico, dead-ends finish: pending_page_edits, Cables 3D (unhold), Albany 3D if built, dead-ends section, card coordinate re-sync |
| 2026-10-10 | dead-ends back-fill (prompt; common.md items 10-11) | `02_research/dead_ends/` | `02_research/dead_ends/README.md` | DONE: 181 entries over 13 reefs. NEXT PAGE AGENT must render each reef's dead_ends as a collapsed 'Checked, nothing useful (N)' section at the end of the reef dialog (closed by default, not in References) |
| 2026-10-10 | final page agent (prompt) | `04_build/`, `02_research/reefs/` (Cables, Albany) | `04_build/HANDOFF.md` section 0c | DONE 2026-10-11: 9 models on page (Cables, Albany added), pending edits applied, dead-ends section, build PASS; leftovers in NEXT_STEPS.md |
| 2026-10-13 | workflow wf_c969d6bd-f09 (6 agents, restarted with Lior's rules 12-13) | opunake-uploads, albany-uploads, cables-fixes, europe-meta-kovalam (SeaDataNet W1/W2 + Kovalam), ocr-mm-2007 (Haiku, 05_qa/papers_intake/*.md), page-map-links (04_build: copy coords, Google Earth web, KML for GE Pro, Navionics, bathymetry viewer in dialog + gallery + 3D tab) | each folder's `HANDOFF.md`; HANDOFF_STOP -> fresh agent continues automatically | STOPPED 2026-10-13 (usage limit): Opunake done, others partial or not started; see NEXT_STEPS.md 'INTERRUPTED 2026-10-13'; prompts in `_agent_briefs/workflows/reef-small-tasks-2026-10-13b.js` |
| 2026-10-13 | workflow wf_4fdc5ea7-96f (resume of 5 tasks, prompts `_agent_briefs/workflows/reef-small-tasks-2026-10-13c.js`) | Albany, Cables, SeaDataNet+Kovalam, OCR MM 2007 (Haiku), page map links | each HANDOFF CHECKPOINT by 00:04 UTC | FINISHED 2026-10-14 ~00:00 UTC: all 5 done or checkpointed; state table in NEXT_STEPS.md; page not rebuilt (2 check failures to fix first) |
**When an agent finishes:**
- save its report from the hand-back;
- refresh the page: `python src/update_page.py` from `04_build`, after the model agents. Check the SUMMARY and FAIL lines;
- make the hand edits it lists. The Borth "0.89 m" caveat is in `04_build/data/models3d_caveats.json` and `models3d_curated.json`;
- set its row to done;
- commit;
- start the next queue item, keeping at most 3 agents at a time.

**Rules for agents running in parallel:**
- Agents never run git; the orchestrator commits.
- Model agents never edit `04_build`.
- Each agent edits only its own reef folders. Shared root files (`05_qa/00_STATUS.md`, `REQUESTS_FOR_LIOR.md`, `03_images/reefs/NEW_IMAGES_LOG.md`) get short appends only.

## 8. Transfer protocol: Lior's PC to a cloud session
Repo: https://github.com/liorbakalo2/Artificial-reef-survey (PRIVATE; pushed by Lior with GitHub Desktop 2026-10-10). The cloud environment
has no setup script (Lior's choice): the cloud orchestrator runs the install steps in CLAUDE.md "Cloud session start".
**On the PC (the orchestrator, when Lior says "hand over"):**
1. Tell every running agent (SendMessage) to finish its current step, write its checkpoint (the file in the section 7 table) and stop.
   Wait for the hand-backs; use TaskStop only for an agent that does not respond.
2. Set each row in section 7 to "stopped at <step>, continue from <checkpoint>". Add a dated `05_qa/00_STATUS.md` entry.
3. Commit everything, with the message "handover to cloud <date>". Push to the private GitHub repo. The first push needs Lior: he
   creates the empty private repo and gives its URL, and Git Credential Manager signs him in. Then "Continue in cloud" (or Lior
   opens a new cloud session on that repo).

**In the cloud (the new orchestrator):**
1. Read `CLAUDE.md`, this file (sections 2-3 and 5-8), and the last `05_qa/00_STATUS.md` entry.
2. Run the setup check:
   - `pip install -r requirements.txt`;
   - Chromium (section 3);
   - `python src/update_page.py --dry` from `04_build` must run without errors.
3. For each section 7 row marked stopped or running: start a FRESH agent with the same task file and the checkpoint named in the
   row. Never try to resume PC agents; they do not exist in the cloud.
4. Continue the queue (section 5) only as far as Lior has given the go. On 2026-10-07 he gave it for the queue in order.
   Commit after each finished agent and push. Prefer pushing to `main`. If the session must use its own branch, tell Lior the
   branch name each time. He views it in GitHub Desktop: Fetch origin → Current branch → that branch. Or merge it into main
   when a step is accepted.
5. First jobs in the cloud, in this order:
   1. Borth page refresh. Apply the typed-text edits listed in Borth `HANDOFF.md` section 7 item 1, then run
      `python src/update_page.py --full`.
   2. Then up to 3 fresh agents, using the section 7 rows:
      - Mount Maunganui D1 in code;
      - Narrowneck stage 1;
      - Boscombe D2.
   3. Lior's open decisions D7 and D8 are in REQUESTS_FOR_LIOR.md. Ask him briefly; do not block on them.

**Back to the PC:** Lior runs `git pull` in the project folder before any local session works there. Work in one place at a time.

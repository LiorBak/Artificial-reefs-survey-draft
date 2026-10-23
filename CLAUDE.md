# Artificial surf reefs - read first (every session, every agent)

Lior's research project: an interactive page, `04_build/artificial_reefs.html`, surveying artificial surf reefs worldwide.
For each reef it covers year, place, cost and financing, motivation, design vs as-built, why it worked or failed, lessons and
reviews; every fact carries a linked reference. It also holds traced plan shapes and three.js 3D models (reef + seabed + water
levels). Purpose: inform a planned reef at Haifa, Israel, where the tidal range is small. Section 2 (Israel sediment transfer),
section 3 (Haifa conclusions) and video transcription are PAUSED until Lior says otherwise.

## Where things are (open only what you need)
- `NEXT_STEPS.md`: START HERE: current state, the work queue, open decisions (updated at the end of each session).
- `new uploads from lior/`: files Lior supplied 2026-10-11 (like `papers/`: his folder, never move or rename).
- `05_qa/00_STATUS.md`: dated log of all work. Read only the last 2-3 entries (`grep -n '^## '`, then print that range).
- `REQUESTS_FOR_LIOR.md`: the single list of what Lior must supply or decide (papers, e-mails, browser pages, app readings, decisions D1-D6).
- `_agent_briefs/`: task briefs. `common.md` holds the rules every agent follows; `orchestrator.md` holds the main session's
  playbook, cloud notes and the work queue.
- `HANDOFF.md` in each work folder (`04_build/`, `07_scale/shapes/<slug>/`): status, decisions, key numbers with sources, file map,
  open issues, next steps. Read it instead of the sources it summarises.
- `02_research/reefs/<slug>.json|.md`: reef cards. `03_images/reefs/<slug>/images.json` + `IMAGES.md`: the picture registry.
- `07_scale/`: shapes, 3D models (`shapes/<slug>/3d/`), `SHAPE_SPEC.md`, bathymetry, tools.
- `papers/`: PDFs Lior supplied. It is his folder: never move or rename anything in it.
- `04_build/`: the page. `src/` is the pipeline. Refresh with `python src/update_page.py` run from `04_build/` (rules in `UPDATE_PROTOCOL.md`).
- The 13 reef slugs are listed in `_agent_briefs/common.md`.

## Paths
Briefs, HANDOFFs and logs were written on Lior's Windows PC. Read
`C:\Users\lior\Documents\Claude\Projects\Artificial reef\X\Y` as `<repo root>/X/Y`, with backslashes as forward slashes.
Gemini's folder (`C:\Users\lior\Documents\Gemini\AG\artifical reef`) is NOT in this repo; see `_agent_briefs/orchestrator.md`.

## Cloud session start (no setup script in the environment; keep it cheap)
Install output costs tokens. NEVER let pip, playwright or apt print into the conversation: send it to a log file, check first
and skip what is already there, and read only the last 15 log lines if something fails. Only the orchestrator runs these, once
per session; agents never reinstall. Run from the repo root:
```
python -c "import numpy,shapely,PIL,scipy,pyproj,fitz,websockets" 2>/dev/null && echo DEPS_OK || { pip install -q -r requirements.txt >/tmp/pip.log 2>&1 && echo DEPS_OK || { echo DEPS_FAILED; tail -n 15 /tmp/pip.log; }; }
{ command -v chromium || command -v google-chrome || ls ~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome; } >/dev/null 2>&1 && echo CHROME_OK || { pip install -q playwright >/tmp/pw.log 2>&1 && python -m playwright install --with-deps chromium >>/tmp/pw.log 2>&1 && echo CHROME_OK || { echo CHROME_FAILED; tail -n 15 /tmp/pw.log; }; }
```
- **OCR**, only when a scanned paper needs it:
  `command -v tesseract >/dev/null || { (sudo apt-get install -y -qq tesseract-ocr || apt-get install -y -qq tesseract-ocr) >/tmp/apt.log 2>&1; tail -n 3 /tmp/apt.log; }`
- **Check:** run `python src/update_page.py --dry >/tmp/dry.log 2>&1; tail -n 12 /tmp/dry.log` from `04_build/`. It must end without errors.
- **Network errors:** if an install fails with one, tell Lior that the environment's network access must be Full.
- **Zero-token option:** the same two lines pasted into the environment's setup script run before the session starts, so they
  cost no tokens.
- **Details:** `_agent_briefs/orchestrator.md` section 3.

## Standing rules (Lior's)
1. Traceability, academic level. Every number and every drawn vertex has:
   - a source (URL, page or figure, date);
   - what was read off it;
   - the method used.
   Methods, confidence (and why) and unknowns are documented in files and reachable from the page.
2. Gemini's work (another AI's attempt) is used only after we fetch and confirm the original source ourselves. Never write in its folder.
3. Image rule. Every picture showing a reef, its site, design, seabed or surf is:
   - saved and registered (see `_agent_briefs/image_registry.md`);
   - recorded with full citation, link, licence, date, what it shows and how it was used for the model;
   - shown in the page.
4. Outline versions. Default = measured survey > design drawing of the built version > photo trace. The other outlines are
   toggleable versions with meaningful names and dates, and an (i) pop-up explains them.
5. 3D shows the as-built state; later changes appear as notes. Use local tides only.
6. Folder hygiene. Use subfolders and keep things ordered. Scratch files and smoke tests go to a temp dir, never the repo.
   Archive (`archive/`) or delete what is no longer needed, but check the target first.
7. Never:
   - send e-mail;
   - log in, or bypass logins, CAPTCHAs or bot checks;
   - download a file over 50 MB;
   - make pictures or papers public. They are private research copies whose reuse rights are not cleared, so this repo stays PRIVATE.
8. Lean context:
   - no whole-file dumps; use grep, head, or short scripts that print summaries;
   - view each image once, downscaled to 1200 px or less;
   - checkpoint often, so a fresh agent can continue from the checkpoint.
9. Before ending a step:
   - update the folder's `HANDOFF.md` (up to ~300 lines);
   - add a dated entry to `05_qa/00_STATUS.md`;
   - update `REQUESTS_FOR_LIOR.md` (root);
   - the orchestrator commits, with a clear message. Agents never run git: parallel agents share one working tree. Never
     force-push or rewrite history.
10. Moving between Lior's PC and the cloud: follow `_agent_briefs/orchestrator.md` section 8 (transfer protocol). Section 7
    there lists the running agents and their checkpoints.

## Talking to Lior
- Lead with the outcome, or with the decision you need. Details live in files.
- Use plain words.
- Ask only about decisions that are his (`REQUESTS_FOR_LIOR.md` section 5); otherwise use the recorded default and say so.

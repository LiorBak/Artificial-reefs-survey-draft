# Common brief for every agent (2026-10-04)

OUR PROJECT ROOT: C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git
Windows 11; Bash (Git Bash) + PowerShell; Python 3.14 (pip install allowed). Quote paths: they contain spaces.

Key locations (ours):
- Verified reef cards: 02_research\reefs\<slug>.json, dossiers 02_research\reefs\<slug>.md
- Earlier text-derived footprints (schematic): 07_scale\reefs\<slug>.md / .footprint.json, verification 07_scale\verified\<slug>.md
- Media re-check: 05_qa\reef\<slug>_media_recheck.md / .json
- Videos: 02_research\videos\<slug>\videos.json + transcript .txt files
- Page source: 04_build\src\ (compile_data.py, build.py, template.html, styles.css, app.js, scale.js, check.py, qa_shots.py) -> 04_build\artificial_reefs.html
- Shape work (new): 07_scale\shapes\<slug>\ ; spec: 07_scale\SHAPE_SPEC.md ; tools: 07_scale\tools\
- Transcription tools (new): 02_research\videos\tools\

GEMINI FOLDER (READ-ONLY, another AI's attempt at the same task): C:\Users\lior\Documents\Gemini\AG\artifical reef
NEVER write, move, rename or delete anything there. Its footprints are known to be partly wrong. Useful files:
02_world_reefs_data\reef_footprints.json, reef_footprint_scale_analysis.md, scale_sketch_photo_alignment_audit.md,
05_web_build\images\IMAGE_PROVENANCE.md, 05_web_build\images_provenance.json, 05_web_build\images\scale\*,
05_web_build\reef_videos.json, 05_web_build\index.html. Our earlier extract of Gemini's footprints: 07_scale\00_gemini_footprints_extract.md / .json

The 13 reefs (our slug): narrowneck-gold-coast, cables-reef-wa, prattes-reef-el-segundo, mount-maunganui-reef, opunake-reef,
boscombe-surf-reef, kovalam-reef-india, borth-coastal-defence-reef, palm-beach-gold-coast, southern-ocean-surf-reef-albany,
burkitts-reef-bargara, bunbury-airwave, mexico-reef-2026-unnamed (Gemini calls the last one xala-reef-mexico).

Lior's layout reference (third-party graphic, never embed it): 03_images\from_lior\goldcoast_pptx\image26.png - reef outlines drawn over real aerial photos.

RULES
1. Every number and every drawn vertex must be traceable: source image (URL, page/figure, date), what was read off it, method.
2. Nothing from Gemini is used unless you fetched the ORIGINAL source yourself and confirmed it.
3. Source images used for overlays MAY be saved locally as a private research copy under 07_scale\shapes\<slug>\src\ with a provenance row (url, source page, credit, license, retrieved date). Reuse rights must be checked before any public release - say so in provenance.
4. Document methods in files as you go. Scratch/temp files go to %TEMP% or your scratchpad, not the project.
5. Your final message is read by an orchestrator, not a human: end it with the JSON summary your task brief asks for, inside a ```json block.
6. IMAGE RULE (2026-10-06, Lior): every image you find or make that shows a reef, its site, design, seabed or surf must be SAVED in our
   folders and REGISTERED in 03_images\reefs\<slug>\images.json + IMAGES.md with full citation, link, licence, date, what it shows and
   HOW IT WAS USED FOR THE MODEL. Read _agent_briefs\image_registry.md before saving any image. Add "images_registered" to your final JSON.
   (This replaces the old "link only" policy of 03_images\web\.)
7. LEAN CONTEXT (2026-10-06, Lior: agents reaching 300k+ tokens use too much of the usage budget):
   - never print whole files, JSON or logs into your context; grep / head / a short python summary instead;
   - view images downscaled (<= 1200 px) or cropped to the part you need; view each image once and write down what you saw;
   - do heavy lifting in scripts that write results to files and print only a few summary lines;
   - checkpoint often (your brief's checkpoint file): a fresh agent may be started from your checkpoint instead of resuming you,
     so the checkpoint must hold everything needed to continue (state, decisions, next steps).
8. HANDOFF FILES - read little, summarise for the next agent (2026-10-06, Lior):
   - READ ONLY what you need: this file, your task brief, and the HANDOFF.md of your work folder (per reef:
     07_scale\shapes\<slug>\HANDOFF.md; page build: 04_build\HANDOFF.md; bathymetry: 07_scale\bathymetry\<src>\HANDOFF.md).
     Do NOT open every file "to get context". Open another file only for a specific fact, and then only the part you need (grep /
     a section / a page). Do not re-read files the HANDOFF already summarises unless you must check a number.
   - If something is unclear or missing, ASK the orchestrator: SendMessage to "main" with a short, specific question, and keep
     working on the parts that do not depend on it. If you are fully blocked, end your turn with "NEEDS_CLARIFICATION: <question>"
     in your final message; you will be resumed with the answer. Do not guess on decisions that are Lior's.
   - BEFORE YOU FINISH (and at each checkpoint), create/update that HANDOFF.md, up to ~300 lines (comprehensive - Lior 2026-10-06), so a future agent need not re-read
     your sources:
       1. Status per stage (trace / verify / 3D / registry / page) with dates and confidence + reason.
       2. Key decisions and why (design version / state drawn, primary source, datum choices) - one line each.
       3. Key numbers with units, datum and source id (dimensions, crest, seabed, height, volume, tides, offsets/equations).
       4. File map: each important file, one line on what it holds and when a future agent needs to open it
          (and which files are bulky/not worth opening).
       5. Open issues, discrepancies, pending checks, requests for Lior.
       6. Next steps for the next agent, in order.
     Facts only, each with its source id; keep older sections current (edit, don't just append).
9. REQUESTS FOR LIOR (2026-10-07): the single list is REQUESTS_FOR_LIOR.md at the PROJECT ROOT. Whenever you add a request to a
   per-folder REQUESTS_FOR_LIOR.md (or a report), also add/update one line in the root file (right section: papers with FULL
   citation, e-mails, browser pages, Navionics / Google Earth readings, decisions, media review) and mark items you resolve as done.

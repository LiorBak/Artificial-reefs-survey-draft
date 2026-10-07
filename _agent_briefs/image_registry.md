# IMAGE RULE + per-reef image registry (added 2026-10-06 at Lior's request)

Lior's words: "any image showing a reef should be in our folders and displayed in the html - so make sure agents document them
(full source citation and link too, and save the image, and how it was used for the model)."

This REPLACES the earlier "link only, nothing downloaded" policy of 03_images\web\<slug>.md/.json (those files stay as history).

## The rule (every agent, every task)
Whenever you find or make an image that shows a reef, its site, its design, its seabed or its surf (photo, aerial, satellite tile,
design drawing, plan figure, survey / contour plot, cross-section, chart or Navionics screenshot, video frame, report photo), you:
1. SAVE the file into our folders (original resolution; if > 10 MB, also keep a <= 3000 px copy and say so). Never only link it.
   - Images that belong to a task folder stay there (07_scale\shapes\<slug>\src\, ...\3d\annotated\, 07_scale\bathymetry\<src>\...).
   - Every other reef image goes to 03_images\reefs\<slug>\ (create it). File name: <slug>_<short-topic>_<yyyy or date>.<ext>.
   - PDF figures: render the page (pymupdf, 200 dpi) and crop the figure; note page + figure number.
   - Do NOT save: Lior's third-party graphic 03_images\from_lior\goldcoast_pptx\image26.png (never embed); anything copied from the
     Gemini folder (fetch the ORIGINAL source yourself, then save that); whole video files (frames are fine).
2. REGISTER it in 03_images\reefs\<slug>\images.json (create if missing; append, never drop others' rows) AND a matching section in
   03_images\reefs\<slug>\IMAGES.md (human-readable). One row per image, including images saved elsewhere (point "file" at them;
   do not duplicate the file). Fields:
   {"id": "<slug>-img-NN",                       (next free number)
    "file": "path relative to the project root",
    "annotated_files": ["our annotated / overlay versions of it, if any"],
    "kind": "photo|aerial|satellite|design_drawing|plan_figure|survey_plot|cross_section|chart_screenshot|report_photo|video_frame|diagram",
    "title": "...",
    "citation": "Author/Organisation (Year). Title. Publisher/venue, page X, Figure Y. URL. Accessed YYYY-MM-DD.",
    "image_url": "direct url of the image or PDF", "source_page": "page that hosts it",
    "page_or_figure": "...", "image_date": "date the image was TAKEN/DRAWN (or 'unknown' + best bound)",
    "credit": "...", "license": "as stated by the source, or 'not stated'", "retrieved": "YYYY-MM-DD",
    "shows": "one sentence: what is visible (structure visible? waves breaking? seabed? which design version / state)",
    "structure_visible": true|false,
    "state_shown": "design | as-built | damaged | renewed | removed | pre-construction | unknown (+ date)",
    "used_for": ["plan_trace","3d_seabed","3d_crest","3d_height_slopes","3d_tides","scale","cross_check","camera_match","context","not_used"],
    "how_used": "1-3 sentences: exactly what was read off it (value, units, datum) and where it went (shape.json source id,
                 model.js provenance row, METHOD/METHODS_3D section) - or why it was not used",
    "linked_records": ["e.g. 07_scale/shapes/<slug>/sources.md img2", "07_scale/shapes/<slug>/3d/SOURCES_3D.md A4"],
    "bytes": n, "px": [w, h], "sha256": "...",
    "rights_note": "Private research copy; reuse rights to be checked before any public release.",
    "display": true,                              (false only if Lior rejected it or it is image26)
    "added_by": "task name, YYYY-MM-DD"}
2b. REGISTER AS YOU GO, not at the end, and per reef: an image of reef X goes to reef X's folder and registry, even when your task is
   about reef Y. Add these fields too:
   "for_3d_check": {"pending": true|false, "what_to_check": "e.g. crest depth label 1.5 m vs model -1.5 m MSL; toe contour; planform of
   the renewal vs shape.json", "model_values_affected": ["crest_z", "seabed", "planform", "volume", "tides"]}
   (pending true whenever the image could confirm or contradict a 3D model or shape value; a 3D agent sets it to false and writes the result).
   Also append one line per new image to 03_images\reefs\NEW_IMAGES_LOG.md (create if missing):
   date | slug | registry id | file | one-line shows | for_3d_check what_to_check | added_by.
   The orchestrator reads this log to schedule the page rebuild and the 3D re-checks.
3. If the image is used for the model, ALSO keep the existing records (sources.md / SOURCES_3D.md / model.js provenance) and make
   them name the registry id, so the page can link both ways.
4. Final JSON of every task gains: "images_registered": ["<slug>-img-NN - file - one-line shows"].

## What the page does with it (04_build, see build_shapes_videos.md section 3b)
Every display:true row is shown in the reef's Images gallery and the Images tab with its citation, source link, licence, date, what
it shows and HOW IT WAS USED FOR THE MODEL; annotated versions are one click away.

## BACKFILL task (one agent, all 13 reefs)
Build/complete 03_images\reefs\<slug>\images.json + IMAGES.md for every reef from: the cards' "images" arrays (02_research\reefs\),
03_images\web\<slug>.json, 05_qa\reef\<slug>_media_recheck.*, 03_images\video_frames\<slug>\, 07_scale\shapes\<slug>\src\ +
sources.md + overlays\, 07_scale\shapes\<slug>\3d\annotated\ + 3d\src\ + SOURCES_3D.md, 07_scale\bathymetry\*\.
- Download every hotlinked image into 03_images\reefs\<slug>\ (browser User-Agent; Wikimedia needs a descriptive UA). If a URL is dead,
  try the source page / Wayback; if still dead, register it with "file": null and "display": false and say so.
- Re-open each source page to complete the citation (author, year, title, venue) - do not invent; write "not stated".
- Fill how_used from the records (sources.md roles, SOURCES_3D.md captions, model.js provenance); "context" if only shown on the page.
- Write 03_images\reefs\README.md (the convention above, counts per reef) and a check script 03_images\reefs\check_registry.py
  (every file exists, sha256 matches, required fields present, ids unique, every image file under shapes\*\src and 3d\annotated
  is registered). Do not edit shape.json / model.js; only add registry ids to sources.md / SOURCES_3D.md as a new column or note.
Final JSON: {"reefs": {"<slug>": {"registered": n, "downloaded": n, "dead": n, "used_for_model": n}}, "check_passed": bool, "issues": ["..."]}

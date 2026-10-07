# 03_images\reefs - per-reef image registry

Started 2026-10-06 at Lior's request: "any image showing a reef should be in our folders and displayed in the html - so make sure agents
document them (full source citation and link too, and save the image, and how it was used for the model)."
Convention: `_agent_briefs\image_registry.md` (rule 6 of `_agent_briefs\common.md`). This replaces the old link-only files in
`03_images\web\` (kept as history).

## Layout
```
03_images\reefs\
  README.md              this file
  check_registry.py      integrity check (run it after every change; exit code 0 = passed)
  NEW_IMAGES_LOG.md      one line per registered image: date | slug | id | file | shows | 3D check | added_by (read by the orchestrator)
  <slug>\images.json     source of truth, a JSON list with one row per image (fields below)
  <slug>\IMAGES.md       the same rows in readable form (generated from images.json), each with a thumbnail link
  <slug>\<slug>_<topic>_<yyyy>.<ext>   images that belong to no task folder (downloads, PDF figure extracts, <=3000 px copies)
```
Images that belong to a task folder are NOT copied: `file` points at them
(`07_scale\shapes\<slug>\src\`, `...\3d\annotated\`, `...\3d\src\`, `07_scale\bathymetry\<src>\`, `03_images\video_frames\<slug>\`,
Lior's own folders). Annotated / overlay versions hang off their source row in `annotated_files`.

## Row fields (all required, see check_registry.py)
`id` (`<slug>-img-NN`), `file`, `annotated_files`, `kind`, `title`, `citation` (full: author, year, title, venue, page/figure, URL, accessed date),
`image_url`, `source_page`, `page_or_figure`, `image_date` (when TAKEN/DRAWN), `credit`, `license` (as stated, else "not stated"), `retrieved`,
`shows`, `structure_visible`, `state_shown` (design / as-built / damaged / removed / pre-construction ...), `used_for`, `how_used`
(what was read off it and where it went: shape.json source id, model.js provenance row, METHOD / METHODS_3D section),
`linked_records`, `bytes`, `px`, `sha256`, `rights_note`, `display`, `for_3d_check` (`pending`, `what_to_check`, `model_values_affected`), `added_by`.
Optional: `notes`, `source_pdf` (the PDF a figure was extracted from), `other_resolutions` (<=3000 px copy of an original > 10 MB),
`duplicate_files` (byte-identical copies elsewhere), `group_files` + `group_sha256` (one row for a numbered series, e.g. the 11 shallow-shading
screenshots of one Navionics layer).

## Rules used by the backfill (2026-10-06)
* Every hotlinked image was downloaded from its ORIGINAL url (browser User-Agent; Wikimedia with a descriptive UA). Where the card used a resized
  variant the full file was saved and the card url is quoted in the citation. No download exceeded 50 MB; files > 10 MB also have a <=3000 px JPEG copy.
* Figures of PDFs are rendered or extracted (PyMuPDF; native raster where one exists, else 200 dpi crop) and the page + figure number is in `page_or_figure`.
* Citations were completed by re-opening the source pages. Where a page was blocked (Geograph and Wavelength return 403) the same photo's Wikimedia
  Commons / Flickr record was used and the row says so. Nothing is invented: unknown fields say "not stated" / "unknown".
* `how_used` is filled from sources.md / shape.json / SOURCES_3D.md / model.js / METHOD(S) records. "context" = shown on the page only.
* `for_3d_check.pending = true` where the image could confirm or contradict a shape/3D value that it has NOT yet been used for.
* sources.md and SOURCES_3D.md of each reef got a note "Registry ids (added 2026-10-06 ...)" mapping source ids / files to registry ids.

## Not registered (on purpose)
* `03_images\from_lior\goldcoast_pptx\image26.png` (Lior's third-party reef-comparison graphic; never embedded) and its RWR original
  `Artificial-Reef-Comparison.jpg` (not downloaded). Anything from the Gemini folder.
* `3d\preview_*.png` of every reef (screenshots of our own model viewer, regenerated whenever the model changes) and `07_scale\drawings\*`
  (our earlier schematic footprints). PDFs and GeoTIFFs under `src` are source documents / DEM data: figures taken from them are registered
  through `source_pdf`.
* `07_scale\bathymetry\gold_coast\q1_dtm_evidence\dtm_metadata_raster_block_overview_raw.png` (DTM coverage raster, no reef; its overlays are registered).
* Lior's other pptx/PDF images (IsraMar charts, clip-art, wave-pool screenshots, Haifa/Poleg items) belong to none of the 13 reefs.
* Google Maps links on the cards (not image files).

## Decisions for Lior / QA (display left TRUE unless stated)
* Opunake: the 2026-09-25 recheck called three RWR photos "unrelated or wrong site" (and said its viewer was unreliable); re-viewed on 2026-10-06 they are
  genuine Opunake photos as the card described (no reef visible). The page build had removed two Opunake video frames (site context only). All five are
  registered as site context - confirm or hide.
* Kovalam: the recheck rejected four RWR images; re-viewed 2026-10-06 they match their file names (geotextile mat, two underwater views of a low mound, ASR beach
  widening composite). Registered with a note.
* Burkitts: two dive-video frames (marine-park reef, wrong feature) registered with `display: false`.
* Albany: the granite-quarry photo and the vessel-track map (RWR page) registered with `display: false` (not reef images).
* Cables: Lior's two screenshots in `Initial info from Lior\` are registered (the design plan is byte-identical to RWR `Cables-Design.jpg`; the composite is `display: false`).
* Narrowneck: Lior's `image29.png` (ICM webinar slide with the presenter's webcam thumbnail) and his YouTube screenshot are registered (identifiable-person flag in the row).

## Counts (snapshot 2026-10-06 after the backfill; `python check_registry.py --table` for the current figures)
"downloaded" = files saved under `03_images\reefs\<slug>\` (downloads, PDF extracts, <=3000 px copies). "used for model" = rows whose `used_for` has
anything other than context / not_used. Rows from other agents (Gold Coast reports, EMODnet) are included in the counts.

| reef | registered | downloaded | dead | used for model | displayed | 3D checks pending |
|---|---|---|---|---|---|---|
| narrowneck-gold-coast | 44 | 13 | 0 | 22 | 44 | 16 |
| cables-reef-wa | 23 | 19 | 0 | 9 | 22 | 7 |
| prattes-reef-el-segundo | 32 | 3 | 0 | 21 | 32 | 2 |
| mount-maunganui-reef | 18 | 7 | 0 | 3 | 18 | 3 |
| opunake-reef | 10 | 4 | 0 | 0 | 10 | 0 |
| boscombe-surf-reef | 29 | 5 | 0 | 19 | 29 | 9 |
| kovalam-reef-india | 14 | 6 | 0 | 3 | 14 | 4 |
| borth-coastal-defence-reef | 16 | 5 | 0 | 8 | 16 | 3 |
| palm-beach-gold-coast | 34 | 5 | 0 | 26 | 34 | 9 |
| southern-ocean-surf-reef-albany | 13 | 9 | 0 | 2 | 11 | 8 |
| burkitts-reef-bargara | 8 | 5 | 0 | 0 | 6 | 2 |
| bunbury-airwave | 21 | 5 | 0 | 9 | 21 | 0 |
| mexico-reef-2026-unnamed | 2 | 2 | 0 | 0 | 2 | 1 |
| **total** | 264 | 88 | 0 | 122 | 259 | 64 |

## Adding images later
1. Save the file (task folder, or `03_images\reefs\<slug>\`), 2. append a row to `images.json` (next free id; never edit or drop other agents' rows) and
a section to `IMAGES.md`, 3. add a line to `NEW_IMAGES_LOG.md`, 4. name the registry id in sources.md / SOURCES_3D.md, 5. run `python check_registry.py`.

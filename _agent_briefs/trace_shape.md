# Brief: find source images and TRACE the plan shape of ONE reef (slug given in your prompt)

Lior's words: "use images from the papers / news reports or whatever source you can; draw the shape on the image; use the most
updated one (a paper can show several designs - make sure we use the correct one); make sure it is accurate; later we may use its angles."

## RESUME RULE (2026-10-04, after an interruption)
An earlier run of this task was cut off by a usage limit. Your folder 07_scale\shapes\<slug>\ may already hold src\ images, overlays\
and even a draft shape.json, but no METHOD.md. Start by inspecting it: keep a src\ file only if you can re-establish its origin
(URL / paper / figure) - from its filename, a draft sources.md or shape.json, or by finding it again online; delete any you cannot trace.
Treat draft overlays and a draft shape.json as unverified notes, not results. Then complete every step below and write all outputs.

## CHECKPOINT RULE (2026-10-05 - two earlier runs were cut off before writing anything durable)
- FIRST action: create METHOD.md (heading + "Run started 2026-10-05"). After EVERY step append what you did and found.
- Add a row to sources.md the moment you save an image to src\.
- Write shape.json (status "traced") as soon as the PRIMARY image is traced and scaled; refine it afterwards.
- Scope cap: trace at most 3 images (the primary + up to 2 cross-checks). Stop searching once you have a good primary.
- Delete src\ files you will not use (keep the folder lean); never delete one that sources.md lists.

Tools: 07_scale\tools\ (read its README.md first). Spec + confidence rubric: 07_scale\SHAPE_SPEC.md.
Work folder: 07_scale\shapes\<slug>\  with  src\  (source images)  and  overlays\  (rendered checks).

## STEP 0 - IMAGE REGISTRY (added 2026-10-06)
Start from 03_images\reefs\<slug>\images.json (every reef image we hold, with citation and file path; convention in
_agent_briefs\image_registry.md). VIEW the rows with structure_visible true or for_3d_check.pending true before searching the web -
they are your first candidate sources. After tracing, write the planform result into each pending row (set pending false only for
planform/position-only checks) and register every new image you save (append only; re-read before writing; NEW_IMAGES_LOG.md line).

## STEP 1 - SOURCES (aim for 2-5 images)
a. Our card / dossier references and the earlier footprint files (07_scale\reefs\<slug>.*): design papers, council/designer reports,
   as-built or multibeam surveys, aerial photos already accepted in the card (images whose "shows" says structure visible).
b. Web search (WebSearch / WebFetch; load them with ToolSearch "select:WebSearch,WebFetch" if not loaded) for plan-view figures:
   "<reef> plan view", "layout", "multibeam", "as-built", "bathymetry", "design drawing"; Google Scholar, ResearchGate, ICCE proceedings
   (icce-ojs.tamu.edu), council PDFs, Raised Water Research, news graphics. For PDFs: curl to %TEMP%, render the figure page
   (pip install pymupdf; page.get_pixmap(dpi=200)), crop the figure, save to src\.
c. Satellite: locate the reef precisely (the card lat/lon may be wrong - e.g. Burkitts has the wrong hemisphere sign). Run
   satellite.py at zoom 18-19, radius ~300-500 m; LOOK whether the structure is visible (rock reefs and shallow bag reefs often are;
   deep, degraded or removed ones are not). If removed or very new, try Esri Wayback releases for a date when it existed (2014+ only).
d. Gemini's sources for this reef (read-only; 07_scale\00_gemini_footprints_extract.json and Gemini's provenance files): fetch each
   ORIGINAL url yourself and judge it: correct / wrong_site / wrong_design_version / dimension_not_in_source / dead / unverifiable.
e. DESIGN VERSION: if sources show several designs or stages, establish which was BUILT (as-built survey or post-construction aerial
   beats a design drawing; a later redesign beats an earlier one). Record the alternatives and why they were not used.

Save each used image in src\ and write 07_scale\shapes\<slug>\sources.md (one row per image: id, kind, title, url, source page,
page/figure, image date, credit, license, retrieved date, role).

## STEP 2 - TRACE each useful image
Read pixel coordinates with overlay.py zoom (grid), write pixel_polygons, render with overlay.py render, VIEW the overlay with the Read
tool, adjust, repeat until the outline follows the visible structure (or the design drawing's outline) closely. Save final overlays to
overlays\<img id>.png. Establish the scale per image (scale bar, georeference, or a known dimension from text - say which, with the
pixel evidence). Do not trace what you cannot see: if the reef is not visible on an image, give it role "context" with no polygon.

## STEP 3 - CANONICAL shape
From the PRIMARY source (geo-referenced satellite where the structure is visible > as-built survey > latest design drawing).
Compute with geom.py: area, bbox, max dimension, offshore distance, edge/arm angles to the shoreline (and to north if
geo-referenced); lat/lon polygon if geo-referenced. Fill dimensions_check against the card and the earlier footprint values.

## STEP 4 - CONFIDENCE
Per the rubric in SHAPE_SPEC.md, with a 1-2 sentence reason. If NO usable image exists: fill "no_source" (what you searched,
what Gemini used and whether it was wrong), fall back to the text-derived schematic, confidence low.

Write shape.json ("status": "traced") and 07_scale\shapes\<slug>\METHOD.md: a step-by-step log of every image looked at, every
measurement taken (with pixel evidence), every judgement, and every Gemini source checked.

## Final JSON
{"slug","sources_found","primary_source":"kind - title - date - url","design_version","geo_referenced":bool,
"confidence","confidence_reason","dims":"L x W m, area m2","no_source":bool,"overlays":["paths"],"gemini_checks":["url - verdict"]}

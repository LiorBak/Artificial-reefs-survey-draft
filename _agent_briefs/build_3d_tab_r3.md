# Brief: 3D models tab - round 3 (queued 2026-10-07; run AFTER the Boscombe, Mount Maunganui and Borth 3D agents finish)

## A. "Match this photo" button (Lior: "select image, then press it, and it will rotate, zoom, and move the 3d model to be at the
same shape as the photo ... only for relevant photos where it is easy and agent already documented something about it, like aerial
photos or garmin (possibly only for those tagged as 'Plan shape')")
Scope = PLAN-VIEW pictures whose geometry is already documented - no new research, no oblique photos:
- Traced images in 07_scale\shapes\<slug>\shape.json (sources with pixel_polygons + scale + georef; today: borth sat2024/sat2022/
  sat2012/drg1020, boscombe img1-3, bunbury img1/4/5, mount-maunganui img1-3, narrowneck s3, palm-beach s2/s4/s7, prattes img1/5/6).
  Fit the pixel -> canonical-metre similarity transform (scale, rotation, translation; mirror flag if the frame is mirrored) from the
  pixel polygon vs canonical polygon correspondence (or from the stored georef/scale), report the RMS residual per image, and keep only
  images with residual <= ~2 m (or a stated tolerance).
- Navionics / Garmin screenshots and Esri tiles whose capture log records centre lat/lon + zoom (+ crop) and whose model has geo
  (lat/lon <-> canonical): compute the same transform from Web Mercator. Include only where the log is complete.
Behaviour: in the photo panel, a "Match this photo" button appears only on eligible pictures (registry row -> its shape.json source /
capture log). Pressing it sends the viewer a message (postMessage {type:"m3d-camera", mode:"plan", center_m:[x,y], rotation_deg,
width_m, height_m, aspect} or URL hash) that sets a top-down (orthographic or narrow-FOV) camera so the model fills the same ground
footprint as the picture, rotated the same way; optionally shows the picture as a semi-transparent overlay in the viewer (opacity
slider) so the user can compare; "Reset view" restores the preset. Inject the receiver into the build COPY of each viewer only.
Write the transforms into 04_build\data\photo_match.json with source ids, residuals and method; document in README / SCHEMA /
combined method notes. Oblique photos (CCTV, beach photos): no button - human alignment is enough (Lior).

## B. Add the new and updated models
- Rebuild with the updated Boscombe model (seabed now extended to the shoreline and offshore) and the new Mount Maunganui and Borth
  models (with outline versions). Add their entries to data\models3d_combined.json, curate key numbers / caveats
  (data\models3d_curated.json, models3d_caveats.json: e.g. Mount Maunganui volume vs bed level, Borth footprint versions, Boscombe
  EMODnet offset), and check the "All (compare)" view still looks right (Boscombe's larger seabed patch must not break spacing or
  overlay mode; consider clipping seabed patches to a common extent in the combined view if needed, documented).
- Exercise the versions toggle with the real Borth and Mount Maunganui models (screenshots).
- Lior's screenshot of "All (compare)" (2026-10-07, built before the Boscombe extension) shows: Boscombe has no beach strip / shoreline
  while the others do; the "50 m" / "100 m" scale-bar labels of neighbouring reefs overlap each other; the reef name labels overlap
  (Bunbury label runs into the next patch) and Boscombe's label is clipped at the left edge. Fix: Boscombe's shoreline + beach must be
  visible in the combined view after the rebuild; one shared scale bar (or non-overlapping bars), labels placed without overlap and
  kept inside the canvas (offset / leader lines / collision avoidance), check at the default camera and in plan view.

Same ground rules as build_3d_tab.md / build_3d_tab_r2.md; start from 04_build\HANDOFF.md; log in 04_build\QA\round11_3d_LOG.md;
screenshots round11_3d_*; update HANDOFF.md, README.md, data\SCHEMA.md, STATUS.

## Final JSON
{"html_path","size_kb","photo_match":{"eligible_images":n,"per_model":{"slug":n},"max_residual_m":x},"models_shown":["slug - confidence"],
"combined_models":["slug - ok|not"],"check_passed":bool,"screenshots":["..."],"limitations":["..."]}

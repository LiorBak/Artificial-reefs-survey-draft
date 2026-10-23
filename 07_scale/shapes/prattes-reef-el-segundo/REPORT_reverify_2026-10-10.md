# Pratte's Reef re-verification: agent report, 2026-10-10 (cloud)

Saved by the orchestrator. Details: VERIFY.md, shape.json `reverification`, HANDOFF.md.

- All `pending_reverification` items confirmed; polygons, frame, design version, confidence (shape medium, 3D low) unchanged.
  Rebuilt model: only md5/mtime/date stamps differ (area 435.2 m2; volume B/A 443/550 m3; crest B apex -2.678, A -1.829 m MSL;
  seabed at centre -3.67 m MSL).
- Fig. 4 of the 2003 paper = img1 drawing; img5 is a crop of the same raster (one reproduction, not two independent sources).
- "30" cross-shore (no unit) agrees: the paper's Fig. 20 on its own 0-50 m bar gives 29.0 x 58.5 m vs outline 28.6 x 58.0 m.
- Datums: MSL - MLLW 0.849 m; crest values recompute exactly from NOAA files.
- New finding: the paper is inconsistent on position (text ~200 m from outfall, <500 m from both structures; its Fig. 2 ~340 /
  670 m). geo stays null.
- Images: img-37 (Fig. 4) and img-38 (Fig. 20) registered with overlays. images.json was truncated by a script error during the
  run and restored from the agent's archive copy; check_registry reports no Pratte's errors.
- Viewer canvas not rendered here (three.js CDN blocked); model data loads.
- Decisions for Lior (none changed): J1 crest datum (paper MLLW vs drawing MSL, 0.849 m); J2 position uncertainty +-100 vs
  +-150 m; J3 volume gap 443 vs 695-782 m3; J4/J5 paper wording slips; J6 venue/year unverified (network).
- Page texts: 05_qa/pending_page_edits/prattes_2026-10-10.json.

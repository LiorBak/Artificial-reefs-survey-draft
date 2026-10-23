# HANDOFF - southern-ocean-surf-reef-albany (network run + 3D build, fresh agent, 2026-10-10; for main and any later agent)

## 1. Status per stage
- Registry: 28 rows (img-14 ... 28 added 2026-10-10); check_registry.py PASSED. Pending 3D checks left: img-01, img-07 (weak camera-match items).
- Trace: done 2026-10-10, confidence HIGH (position, size, orientation; area -30 %/+20 % by edge definition). shape.json status "verified" (one agent traced and verified; an independent look would help).
- 3D: BUILT 2026-10-10, confidence LOW (plan high, crest medium-low, seabed low, pile height/slopes low, volume medium-low because fitted, tides low-medium). Folder `3d/`. Viewer checked in headless Chrome over http (no JS error; plan, oblique, methods panel, version pop-up previews).
- Page: nothing done in 04_build (main's job): paste `3d/PAGE_TEXTS_FOR_MAIN.json` into data/models3d_combined / curated / caveats, remove the slug from data/models3d_hold.json, run update_page.py. Viewer imports three.js from a CDN import map (as the Borth template); the page build swaps it for the vendored bundle.
- Network fetches done: City of Albany pages/documents, EPA WA referral (BMT 2018 EIA), Raised Water Research gallery, DoT/BoM tide predictions, Esri Wayback (19 releases). Navionics: viewer did not render (not bypassed). AusSeabed/GA: 403 (not bypassed).

## 2. Key decisions and why (full list D1-D10 in 3d/REGISTER_3D.md)
- Default outline = Bluecoast final-design outermost contour (13,104 m2); toggle = visible reef on Esri 2026-01-20 (10,918 m2). Unchanged from the shape run.
- Seabed from the RHDHV 2015 contours (read as AHD), not from BMT soundings (sparse, near-shore value conflicts). Model zero = AHD (about MSL); LAT derived = -0.74 m.
- Built despite the weak seabed (rule: plan, crest, seabed sourced); confidence LOW with the reason on the page.
- Reef surface = loft between a crest ridge (9 m inside the shoreward edge; -1.0 m AHD over the first 15 m from the offshore end, -2.0 m beyond 40 m) and the toe; exponent N = 2.73 FITTED to the stated 34,000 m3; toe slope capped at 1:2.
- Frame: +x NNE (30.26 deg true), +y offshore ESE (120.26 deg), z up, 0 = AHD.

## 3. Key numbers (units, datum, source id; sources S1-S14 = 3d/REGISTER_3D.md)
| item | value | source |
|---|---|---|
| crest | -1.0 m AHD shallowest; -2.0 m AHD over 110 m; 0.74 m below MLLW, 1.34 m below MHHW | S5, S6 (City table, project page) |
| MLLW / MHHW | -0.26 / +0.34 m AHD | S6 (derived from the crest statement) |
| LAT | -0.74 m AHD (2024 predicted extremes mean 0.742 m above LAT; AHD = MSL assumed) | S13 |
| highest predicted tide 2024 | +0.66 m AHD (1.40 m above LAT); HAT not found | S13 |
| tidal range | spring 0.9 m, neap 0.3 m; surge +0.4-1.0 m | S12 (EIA s.5) |
| seabed profile (m AHD at y m from beach-face line) | -0.5 @7, -1 @36, -1.5 @50, -2 @64, -2.5 @75, -3 @88, -3.5 @98, -4 @105, -4.5 @118, -5 @126, -6 @150, -7 @178, -7.5 @250, -8 @330 | S11 (RHDHV 2015 plan, read by colour, +-5 m position) |
| seabed under footprint | -2.1 m (apex, y 67) to -7.4 m (offshore toe, y 234) | profile |
| volume design outline | 34,000 m3 (fitted); unfitted loft 20,826 m3; mean height 2.59 m; max 6.0 m | S5; build_metrics.json |
| volume satellite outline | 30,273 m3 (result) | build_metrics.json |
| volume sensitivity (design) | bed +1 m deeper +7.7k / shallower -7.9k m3; CD = LAT +5.7k; crest all -1.0 m +6.4k, all -2.0 m -1.4k | build_metrics.json |
| rock | 62,800 t, layers belly D50 0.16 m 18 %, core 0.49 m 36 %, armour 0.94 m 46 %; 1.847 t/m3 | S6 |
| BMT soundings (m CD) | 8.4 at (188, 315) agrees (-8.0 AHD); 2.7 at (-53, 32) is 1.6 m deeper than the profile (-1.1): UNRESOLVED | S12, A3 figure |
Earlier numbers of the shape run (area 13,104 / 10,918 m2, crest bearing 278 / 281 deg, 165 m along crest) are unchanged (shape.json).

## 4. File map (07_scale/shapes/southern-ocean-surf-reef-albany/)
- shape.json, METHOD.md, VERIFY.md, sources.md, FEASIBILITY.md (updated 2026-10-10), SOURCE_AUDIT_2026-10-10.md, overlays/, scripts/ (shape scripts, as before).
- src/: shape-run images (Esri tiles, design.jpg, Bluecoast diagram) + NEW: city_docs/ (City PDFs and project page html), epa/ (BMT 2018 EIA 6.4 MB, referral form, determination, advice, Fig 6.9 raster and render, Fig 29 render), rwr_images/ (RHDHV 2015 plan and oblique, renders, video stills), tides/ (DoT/BoM 2024 predictions PDF 1.9 MB, DoT Albany tide page), esri_wayback6543_2022-12-19_z18.png.
- 3d/index.html (viewer), model.js (data; 322 kB), docs.js (METHODS/REGISTER/SOURCES as the viewer panels), METHODS_3D.md, REGISTER_3D.md (sources with how-used, assumptions A1-A12, decisions D1-D10), SOURCES_3D.md (run log), REQUESTS_FOR_LIOR.md, PAGE_TEXTS_FOR_MAIN.json, build_3d.py (regenerates model.js + docs.js + src/build_metrics.json), annotated/A1-A3, preview_*.png.
- 3d/scripts/: geo.py (georeference + frame), prof.py + read_contours.py (contour crossings), tides_from_dot.py, make_annotations.py, make_viewer_from_borth.py (re-creates index.html from the Borth viewer), preview.py, register_images_3d.py (run once; done). 3d/src/: levels2_raw.json, tides_derived.json, provenance.json, confidence.json, build_metrics.json, Esri 1200 m mosaic (9 MB, bulky).
- Not worth opening: src/epa/*.pdf (160-page EIA; only p. 42 and appendix p. 140 matter), src/tides PDF.

## 5. Open issues, discrepancies, pending checks
- Seabed: 2015 RHDHV contours (unstated datum) vs BMT 2018 near-shore sounding: 1.6 m. Resolve with Navionics readings (Lior), the full Bluecoast report / 2017 bathymetry, or the March 2025 as-built survey (e-mail E9 in root REQUESTS).
- Volume of the design outline is fitted (A9); the unfitted loft gives 61 % of the City volume (fuller pile or deeper bed; evidence cannot separate them).
- Which end of the crest is shallowest (A7) and the ridge position (A6): from a design plan, no section.
- Wayback: only 2022-12-19, 2025-01-16, 2026-01-20 exist; the soft offshore edge of the visible patch cannot be re-checked with a second finished-reef image. Google Earth Pro history (Lior) might have more.
- The City FAQ (2023) gives an earlier footprint of about 16,000 m2 and 145 m offshore; the final table gives 140 m (shape decision). Card R15 already records this.
- Dead ends logged in 02_research/dead_ends/southern-ocean-surf-reef-albany.json (11 entries by this run; the file also holds entries written by another agent, check for overlap).
- If kovalam build_shape_json.py is re-run it overwrites the audit additions in shape.json: re-apply from the audit.
- The reef card (02_research/reefs/southern-ocean-surf-reef-albany.*) was not edited; main may add references S11-S13 (RHDHV 2015 plan via RWR, BMT 2018 EIA Fig 6.9 p. 32, DoT/BoM tides 2024).

## 6. Next steps for the next agent, in order
1. Main: paste PAGE_TEXTS_FOR_MAIN.json entries, remove the slug from models3d_hold.json, run update_page.py, view the Albany model on the page.
2. Lior: Navionics readings and the City e-mail (3d/REQUESTS_FOR_LIOR.md); then edit `PROFILE` in build_3d.py (and the A3 text), rerun build_3d.py, make_annotations.py, preview.py, update METHODS_3D 4 and REGISTER_3D A3/A4.
3. If an as-built survey or cross-sections arrive: replace the loft by the surveyed surface, add it as a third outline version (default), drop the fit (A9).
4. Optional: digitise EIA appendix Fig 29 (img-15, 1 m colour bins, 2016 survey) to cross-check the -3 ... -6 m bands.

## 7. CHECKPOINT 2026-10-10 (final for this run)
Fetched, built, documented, registered; nothing half-done. Not touched: 04_build, other reefs, papers/. STATUS and REQUESTS appended. No HANDOFF_STOP.

## 8. CHECKPOINT 2026-10-13 (uploads run; HANDOFF_STOP at the 250k context budget) - read this first
DONE (all files in this folder unless stated)
- Read all 4 uploads + live pages. Facts and sources: `3d/REGISTER_3D.md` S15-S23, `3d/METHODS_3D.md` 3.4 (later changes), 4 (3 new validation rows), 8 (full reference list), 9 (before/after). Summary of findings:
  * Albany FAQ PDF = byte-identical to our `src/city_docs/albany_community_update_faqs_2023.pdf` (sha256 042fd350...): nothing new (concept 16,000 m2, 145 m offshore, 41 %, 33 % by 2050, 0.05 %/yr upkeep, NPV 19.4 M).
  * None of the 3 RWR pages is another reef: all Albany (spot page title "Midds Reef"). The RWR page images: only `Rocks-at-Southern-Ocean-Surf-Reef.png` was new (registered img-29). `Reef2.jpg` (RWR upload 2026/03) seen in the sidebar of the RWR page "Construction Underway" is NOT Albany (a barrel; belongs to RWR's "Unveiling the new reef in Mexico" post, i.e. probably our `mexico-reef-2026-unnamed`): not saved, not registered; main/Mexico agent may check https://raisedwaterresearch.com/ news "Unveiling the new reef in Mexico".
  * No as-built level, crest, section or seabed depth in any source => 3D geometry unchanged (D11). RWR numbers (1.61 ha, 140-375 m offshore, 47,000 m3 / 70,000 t, crest "0.75 m under the surface") mix 2015 and final-design values, no source: validation only.
  * Timeline (corrects the card and A12): first rock 18 Mar 2025 (Albany Advertiser); planned 6 weeks; 16 May "more than two-thirds complete", finish mid-June; storm Mon 26 May 2025 (highest waves in King George Sound since 2017) moved some CORE rock shoreward (ABC Great Southern via RWR 28 May); opened 16 Jul 2025 ("after four months of work", final cost 13 M AUD). City programme "Jan-Mar 2025, practical completion Mar 2025" was a plan.
  * Moved rocks 2026: about 18 "high rocks", two days late Feb 2026, commercial divers + local vessel + Albany Boardriders, after late-2025 surveys, cost "more than $20,000" (lede) / "about $24,000" (City estimate). No coordinates. Text came from the schema.org articleBody in the page source of two paywalled Albany Advertiser pages (no login; flagged as D12 for Lior).
  * Funding conflict: City page = Commonwealth 4.75 M, WA 5 M; WA Government statement 14 Jan 2025 and RWR = WA 4.75 M (Commonwealth 5 M).
  * Wave direction: RWR 2019 "Long Right" = 2015 feasibility option; built reef is a left (City FAQ Q6, ABC, RWR spot page).
- 3D: `build_3d.py` text strings changed (state, design-version date) + new sensitivity `if_built_70000_t` (design outline: 37,898 m3, N 3.89, mean 2.89 m, max 6.1 m); rebuilt; model.js differs only in those (diff-checked); docs.js refreshed; `PAGE_TEXTS_FOR_MAIN.json` updated (key `_update_2026-10-13` lists the 10 exact old -> new; 2 new caveat rows, ev snippets verified verbatim).
- W8: GA services return 403 and portal scripts come back as HTML (cannot render in headless Chrome; not bypassed). Public GA file "AusSeabed Bathymetry Coverage 2021" (data.gov.au, CloudFront zip 42 MB, FileGDB, no GIS reader here) lists WA DoT surveys "Middleton Bay & Oyster Harbour" (multibeam; laser scanner), "Middleton Bay" (single beam), "King George Sound" (single beam, RTK) with Data Access URL https://maps.slip.wa.gov.au/Marine/app/ (S23). `3d/W8_how_to.png` (red point lat -35.018005, lon 117.920991, 5 steps; honest note that the portal itself could not be drawn) + the 5-line text appended to `3d/REQUESTS_FOR_LIOR.md`. The 69 MB 2019 holdings zip was NOT downloaded (50 MB rule).
- Registry: img-29 (moved rocks photo, file in 03_images/reefs/<slug>/), img-30 (W8_how_to.png); `check_registry.py` PASSES for Albany (10 other-reef errors belong to other agents).
- OCR of Lior's RWR PDFs saved: `05_qa/papers_intake/albany_rwr_pdfs_ocr.md`.
FILES CHANGED: 3d/METHODS_3D.md, REGISTER_3D.md, SOURCES_3D.md, REQUESTS_FOR_LIOR.md, build_3d.py, model.js, docs.js, src/build_metrics.json, PAGE_TEXTS_FOR_MAIN.json, W8_how_to.png (new); 03_images/reefs/southern-ocean-surf-reef-albany/{images.json, IMAGES.md, ..._rwr-abc-moved-rocks_2025-05.png}; 05_qa/papers_intake/albany_rwr_pdfs_ocr.md. Scratch (may vanish): /tmp/claude-0/albany/ (live/*.txt page texts, pg/ OCR, imgs/, w8/).
DONE in the second run (2026-10-13, same day, resumed before the 00:04 UTC deadline)
- Dead ends: 5 entries appended to `02_research/dead_ends/southern-ocean-surf-reef-albany.json` (uploads gave no levels; GA portal 403 with the AusSeabed 2021 lead; beachgrit/ausleisure bot checks; original ABC article not found; no public as-built survey).
- Card `02_research/reefs/southern-ocean-surf-reef-albany.json` (CRLF kept) and `.md`: year, as_built_vs_design, status_now, unexpected_results, financed_by (CONFLICT flagged), size, gaps; R10, R11, R18 extended; R23-R33 added with full citations; moved-rocks photo in `images`; md has an "Update 2026-10-13" section.
- Root `REQUESTS_FOR_LIOR.md`: appended W8 FAQ DONE, W8 PARTIAL (lat/lon, picture, lead), decision Albany D12, e-mail E9 wording. `05_qa/00_STATUS.md`: dated entry appended.
- Viewer check: `3d/index.html` loads headless (window.__ready true), only a favicon 404; preview_*.png NOT refreshed (no visible change).
- check_registry: Albany passes (30 registered); the 8 errors are Boscombe/Borth files of another agent.
OPEN (for main or a later agent)
1. Main: apply `3d/PAGE_TEXTS_FOR_MAIN.json` key `_update_2026-10-13` (10 exact old -> new, 2 new caveat rows) to `04_build/data/models3d_curated.json` / `models3d_caveats.json`, then `update_page.py --full`. The card also changed (year, status, refs R23-R33).
2. Lior: W8 (GA portal click-through, `3d/W8_how_to.png`), decision Albany D12, e-mail E9 for the March 2025 as-built survey.
3. Optional: open the 42 MB AusSeabed 2021 FileGDB in QGIS to read year/extent of the WA DoT "Middleton Bay & Oyster Harbour" survey (not possible here: no GIS reader).
4. Optional: card md line about "18 rocks ... in 2026" (section Outcome) still says "more than AUD $20,000"; the Update 2026-10-13 section corrects it.

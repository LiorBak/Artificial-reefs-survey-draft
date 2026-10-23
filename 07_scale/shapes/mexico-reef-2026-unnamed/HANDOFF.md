# HANDOFF - mexico-reef-2026-unnamed (queue item 9 agent, 2026-10-10)

Read this first. Verdict and reasons: FEASIBILITY.md in this folder.

## 1. Status per stage
- Trace: NOT POSSIBLE 2026-10-10, re-checked with full network access the same day (no image shows the structure, no dimensions, no coordinates; RWR post, Xala site, THR, WSCC, DHI, SEMARNAT search, Esri imagery all checked). No METHOD.md/sources.md/shape.json/overlays created on purpose.
- Verify: n/a. 3D: not feasible. Registry: 2 images (img-01, img-02), both context only, unchanged. Page: keep card text; no shape drawing (or the labelled schematic).
- Confidence of the verdict: high (evidence list is short and complete in the card gaps).

## 2. Key decisions
- No invented outline; the analogy envelope (07_scale/reefs/mexico-reef-2026-unnamed.footprint.json, 160 x 80 m) is not promoted to shape.json.
- Gemini's "~140 x 75 m" has no source: not used.

## 3. Key numbers (all from the card, source ids R#)
- Rock/boulder reef, "3,000 truckloads" (R3 Hollywood Reporter 2025-04-22); designer S. B. Mortensen, DHI Seaport (R1 RWR 2026-03-31); announced 2026-03-31 by RWR [R1] with a reveal event billed for 2026-04-16 (no source seen reports that it took place; wording corrected 2026-10-10, 'unveiled' was unsupported).
- Not disclosed: coordinates, length, width, crest depth, volume, cost, contractor, build dates. Area pin 19.71861, -105.23222 is NOT the reef.

## 4. File map
- FEASIBILITY.md: why no shape + what is needed. Nothing else here.
- 03_images/reefs/mexico-reef-2026-unnamed/{images.json,IMAGES.md}: 2 images. 02_research/reefs/mexico-reef-2026-unnamed.json: card.

## 5. Open issues
- Reef location undisclosed; construction timeline unresolved (2025 vs 2026); no independent design/as-built document.

## 6. Next steps (when new evidence arrives)
1. Add the document/coordinates to papers or the registry; 2. follow trace_shape.md; 3. verify; 4. model_3d.md.

## 7. NETWORK PASS DONE 2026-10-10 (full access): nothing new found, see FEASIBILITY.md section 6 and 02_research/dead_ends/mexico-reef-2026-unnamed.json. Remaining ideas below are for Lior (browser / contacts) - the list is kept for reference
- https://raisedwaterresearch.com/unveiling-the-new-reef-in-mexico/ and RWR site search "Xala" / "Mortensen": newer posts with plan graphics or coordinates.
- DHI Seaport / dhigroup.com search "Xala" "Mortensen" "artificial surf reef Mexico": case study, conference abstract (ICSR 2026, Coastal Structures, ICCE).
- SEMARNAT MIA (Manifestacion de Impacto Ambiental) "Xala" / "Costalegre" / "Chalacatepec" "arrecife": gaceta.semarnat.gob.mx, apps1.semarnat.gob.mx (coordinates, reef dimensions, drawings).
- Esri Wayback tiles around 19.72, -105.23 (zoom 17-19, 2024-2026 releases) to locate the break and shoreline orientation, only after coordinates are confirmed.
- Tides: NOAA/UNAM tide predictions for Manzanillo (needed only if a 3D model becomes possible).

## 8. CHECKPOINT 2026-10-10
Agent finished the whole task (no partial state). Fresh agent: only act if new evidence in section 6 exists.

## Source audit 2026-10-10
SOURCE_AUDIT_2026-10-10.md in this folder holds the sources-with-how-used, statement check, assumptions (A#), decisions (D#), confidence and consistency tables. FEASIBILITY.md / shape.json now carry the why / checked / assumed text (page_status for hidden reefs). Open mismatches are listed in the audit section 2. If kovalam build_shape_json.py is re-run it overwrites the audit additions in shape.json: re-apply from the audit.

## 9. Network pass 2026-10-10 (agent: Burkitts+Mexico, cloud)
- Result: verdict unchanged (HIGH confidence). Added: src/web_text/ (6 saved page texts), src/imagery/ (2 Esri images, registry img-03/04, display:false), 10 dead-end entries, FEASIBILITY section 6.
- New facts (context only): Xala ~5 miles (8 km) of coast, ~65 miles S of Puerto Vallarta, 10 min from Chalacatepec airport; lagoon mouth Xola-Paraman ~19.731,-105.291; airstrip ~19.719,-105.231 (this is the card's area pin). Reef position on that coast unknown.
- Fresh agent: do not repeat these searches (see dead_ends). Act only if Lior supplies the 16 Apr 2026 event material, DHI/Mortensen material or a SEMARNAT document.

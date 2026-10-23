# FEASIBILITY - mexico-reef-2026-unnamed (Xala Reef, Costalegre, Jalisco) - 2026-10-10

Verdict: a plan shape CANNOT be traced and no 3D model can be built from current evidence. Nothing is drawn; no shape.json was created.
Any outline would be invented. The only shape on file is the earlier text-derived envelope (see 4), which is not a measurement.

## 1. What the evidence is (all checked 2026-10-10 from local files)
- Registry (03_images/reefs/mexico-reef-2026-unnamed/images.json): 2 images, both Raised Water Research (RWR) post images, 2026-03-31
  (https://raisedwaterresearch.com/unveiling-the-new-reef-in-mexico/). img-01 = surfer in a wave, img-02 = drone shot of a peeling left.
  Both: structure_visible false (rock reef submerged), no scale, no coastline, no landmark. Nothing can be measured or georeferenced.
- Card 02_research/reefs/mexico-reef-2026-unnamed.json: lat/lon null (location withheld by RWR until the 16 Apr 2026 event); size "not disclosed";
  gaps list: no length, width, crest depth, volume, contractor, construction timeline; no design report, EIS or as-built drawing found.
  Only facts: quarried boulders, "3,000 truckloads" (Hollywood Reporter 2025-04-22), designer Simon B. Mortensen (DHI Seaport).
- No shape folder, no src/ image, no papers/ item for this reef. The only approximate position is a Google Maps area pin (19.71861, -105.23222)
  near Chalacatepec airport, explicitly NOT the reef (card images_rejected).
- Gemini: its dossier gives "~140 m x ~75 m" with no source and no CAD entry (07_scale/00_gemini_footprints_extract.md); not used (rule 2).
- Network (first test 2026-10-10, before the network opened): raisedwaterresearch.com returned HTTP 403; map tiles, EMODnet, Navionics blocked. SUPERSEDED: see section 6 (network pass, same day, full access).

## 2. Why this fails the rubric (SHAPE_SPEC.md)
No image of the structure, no scaled drawing, no dimensions, no coordinates. Even a "low" confidence trace needs a sketch or figure to trace; there is none.
A submerged boulder reef cannot be seen on the two photos; satellite imagery would only show the wave line, not the reef toe.

## 3. What would be needed (any ONE of A, B+C is enough for a medium/low trace; A is best)
A. A design or as-built plan figure: DHI/Mortensen paper, ICSR/ICCE/Coastal Structures proceedings, a Xala/ACTUR EIA (MIA - Manifestacion de Impacto
   Ambiental, SEMARNAT Gaceta Ecologica, Xala or "Costalegre" project), a DHI Seaport case study page, RWR follow-up post or video with plan graphics.
B. Reef coordinates (from Lior's contacts, the 16 Apr 2026 California Surf Club event, or SEMARNAT MIA documents) so that recent satellite
   imagery (Esri Wayback / Google Earth) can be checked for a break line, shoreline orientation and rock works above the water (a beach
   nourishment/groyne-like head may be visible).
C. At least length, width, crest depth and layout type (e.g. Palm Beach-style V/reef + sand) from a published statement, for a schematic 3D.
For 3D also: nearshore bathymetry (nautical chart, EMODnet does not cover Mexican Pacific well; Navionics reading), local tides (Manzanillo/Cuyutlan,
CICESE or NOAA tide predictions), and as-built crest levels.

## 4. Existing fallback (not a trace)
07_scale/reefs/mexico-reef-2026-unnamed.footprint.json: symmetric 160 x 80 m envelope placed 230-310 m offshore by analogy to Palm Beach Reef;
declared "not a measurement of Xala". It must NOT be shown on the page (Lior, 2026-10-10: shapes we do not know are not shown; footprint.json has display:false).

## 5. Status
Trace: not done (no source). Verify: n/a. 3D: not feasible. Registry: unchanged (2 rows, none new). Re-open when A, B or C arrives.

## Why this reef is hidden on the page, what was checked, what is assumed (source audit 2026-10-10)
Rule (Lior, 2026-10-10): shapes we do not know are not shown. Xala is hidden (no shape.json; footprint.json display:false).
- Why: no plan, no survey, no coordinates, no dimensions and no image of the structure (it is submerged) exist in any source we found. The reef's location was withheld until the 16 April 2026 event.
- Checked, with sources: Raised Water Research post of 2026-03-31 "Unveiling the new reef in Mexico" and its two images (registry img-01, img-02: surfer and drone shot, no scale); The Hollywood Reporter, K. Romeyn, 2025-04-22 ("3,000 truckloads of boulders"); Hospitality Net and the Xala website (location context only); WSCC 2026 speaker bio and RWR Palm Beach / Mortensen pages (designer pedigree, Palm Beach figures); web search 2026-10-10 for Xala dimensions (nothing found); Gemini "~140 x 75 m" (no source). The RWR site was not reachable in the audit (HTTP 403 earlier): the post was not re-fetched.
- Assumed (ASSUMPTION): the April 2026 reef is the Xala reef (identified by an RWR image caption); the 2025 boulder break and the 2026 reef are one structure; a submerged boulder reef would not show on satellite imagery (an expectation, untested); Palm Beach figures say nothing about Xala's size.
- Confidence: every geometric element none; identity of the structure medium. Full tables: SOURCE_AUDIT_2026-10-10.md.

## 6. Network pass 2026-10-10 (full network access): what was checked, result unchanged
Verdict: STILL NOT TRACEABLE. No plan, coordinates or size exist in any source reachable today. Full per-source list with URLs and results: 02_research/dead_ends/mexico-reef-2026-unnamed.json (10 entries added); copies of the pages are in src/web_text/.
- RWR post "Unveiling the new reef in Mexico" (Indelicato, 2026-03-31, https://raisedwaterresearch.com/unveiling-the-new-reef-in-mexico/): fetched (HTTP 200). Announcement only: reveal of the location at the California Surf Club, Redondo Waterfront, 16 April 2026, 6:30 PM; designer Simon Brandi Mortensen; no coordinates, size or graphics. RWR site search for Xala / Mortensen / Mexico: no follow-up post.
- Xala developer pages (xala.com press, community, real-estate; life.xala.com), checked 2026-10-10: "five miles of coastline", ~65 miles south of Puerto Vallarta, 10 minutes from the Costalegre (Chalacatepec) airport, 3,000 acres, two Ramsar estuaries; "construction of a new coastal protection reef to create a consistently great wave to surf while safeguarding the marine habitat"; the surf page: "pristine bay ... uncrowded waves". No dimensions or coordinates.
- Hollywood Reporter 2025-04-22: only "3,000 truckloads of boulders from a nearby quarry" (no size). WSCC 2026 bio: Mortensen designed "three additional surfing reefs globally, most recent in the Americas" (Xala not named).
- DHI group site and WebSearch (English): nothing on Xala. SEMARNAT: gaceta.semarnat.gob.mx unreachable (proxy 502); sinat.semarnat.gob.mx is an interactive form (not driven); WebSearch in Spanish and English found no MIA / Gaceta entry for a Xala reef or breakwater. papers/ (5 PDFs): nothing (the NSW 2013 review only cites Mortensen 2010, CFD).
- Imagery: Esri World Imagery (image 2025-05-23) of the Xala coast (z15, r=6.5 km; registry img-03) and of a natural rocky point at about 19.679,-105.262 (z17; img-04): a long surf beach with the Xola-Paraman lagoon; Chalacatepec airstrip at 19.719,-105.231 (the card's area pin). No artificial rock works are visible. The point is a candidate by eye only: nothing ties it to the reef. A submerged boulder reef would not show (assumption A3, still untested because no coordinates exist). Both images display:false (site not identified).
- New location context (fact, not geometry): Xala spans about 5 miles (8 km) of coast near the Xola-Paraman lagoon; that is consistent with the straight beach seen in img-03. The reef lies somewhere on it: unknown.
- Decision: no shape.json, no overlay, no trace (rubric needs a figure or coordinates). Status unchanged: hidden.
What would still work: (1) the 16 Apr 2026 event recording or slides (Lior / RWR); (2) Mortensen / DHI Seaport directly (Lior); (3) a SEMARNAT SINAT / Gaceta search by Lior in a browser; (4) Google Earth Pro imagery after April 2026 once the beach is known.

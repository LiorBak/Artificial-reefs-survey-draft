# Burkitts Reef ("Greg's Reef") -- Footprint Provenance

## Summary

Burkitts Reef is **not an engineered structure** -- it is a natural volcanic-basalt headland/rock shelf at the southern end of Bargara Beach (near Bill Fritz Park / Burkitt Street) that Greg Redgard had reshaped in place in February 1997, using a rented excavator to break down and relocate existing boulders. No source found -- ours or Gemini's -- publishes a plan-view length, width, or footprint for it, and our own verified card already states this explicitly ("No footprint length/width figure found -- not found"). Wikipedia is the most direct confirmation: the 1997 works were "not a structure in and of itself."

Because no designed footprint exists, this dossier instead documents the **natural rock/reef extent visible in satellite imagery today**, as a low-confidence estimate, clearly separate from a surveyed or engineered footprint:

- **Shape:** `other` -- an attached natural point/headland, wedge-shaped, widest and rockiest at its seaward tip. No V/delta/chevron/linear/crescent/L/mound template fits.
- **Size (estimated, not published):** roughly **120 m** alongshore x **46 m** seaward, area **~2,480 m²** (order-of-magnitude only, ±35-50%).
- **Depth / tidal exposure:** exposed dry basalt at low tide, submerged under roughly **2.5 m** of water at high spring tide (the local tide range already in our card) -- not a fixed engineered crest depth.
- **Position:** **0 m offshore** -- it is an attached shoreline headland, not a detached structure.
- **Orientation:** a right-hand point break; the densest boulder mass / seaward apex lies toward the north-east end of the point (qualitative only -- no compass bearing published).
- **Confidence: low.** Every geometric number above is our own estimate from a real, cited image (satellite imagery with an on-screen scale bar), not a published or surveyed figure.

## Sources and what each gave

- **[R1]** ABC News, 2024-01-28, "How a sugarcane cutter and his mates created a world-first DIY surf break at Burkitts Reef, Bargara" -- https://www.abc.net.au/news/2024-01-28/diy-surf-break-built-by-mates-at-burkitts-reef-bargara/103387450. Re-fetched and searched specifically for size/length/width/depth/area/extent language; found **none** beyond "you'd take off, go for about 2 or 3 metres and you would just run into rocks" (a ride distance, not a reef dimension) and "a 30-tonne excavator." Also the source of two images used here (petition sketch, construction photo).
- **[R2]** Wikipedia, "Multi-purpose reef" -- https://en.wikipedia.org/wiki/Multi-purpose_reef. States plainly: the 1997 effort "consisted of shifting boulders... not a structure in and of itself." No dimensions. This is the strongest single sentence for classifying the reef as `shape_type: other` / `distance_offshore_m: 0`.
- **[R3]** Coastal Management / ICM, "Building Artificial Surf Reefs: Worldwide Lessons & Applications" -- https://www.coastalmanagement.com.au/artificial-surf-reefs. Re-fetched: only quantifiable figure is "Approximate volume: 300m³." No length/width/footprint. Describes the wave as "a peeling right-hand wave," used for `orientation_notes`.
- **[R4]** Raised Water Research, Burkitts Reef spot page -- https://raisedwaterresearch.com/spot/artificial-reef/australia/queensland/burkitts-reef/. Re-fetched: only "estimates put it around 300 cubic meters" of rock moved. No length, width, depth or footprint stated. Confirms the ~2.5 m tide swing (already in the card), used here to derive the intertidal exposure range.
- **[R6]** Yahoo Lifestyle, "How a Motivated Surfer Created an Epic New Surf Break in Australia" -- corroborates method (30-tonne excavator, bricks carried out on a surfboard); no dimensions.
- **[R8]** Swellnet comment thread ("truebluebasher") -- re-fetched 2026-09-25 (via built-in browser, since WebFetch returned ECONNRESET for this URL twice): confirms the 1982 proposal / $10,000 cost / 1997 completion timeline and the "30 days/yr + overhead 4 days/yr" before/after performance figures already in the card. **Correction:** it does **not** itself state a "~2.5 m" tide-swing figure anywhere in the visible thread text -- that specific number comes from R4 alone. The draft version of this file over-cited R8 alongside R4 for the tide swing; fixed throughout (derivation table, JSON `crest_depth_m.ref`, Gemini-comparison rows) to cite R4 only for that number. No footprint dimensions in either case.
- **[R10]** DivePlanit, "From macro to megafauna: shore diving the Bundaberg coast" -- https://www.diveplanit.com/diving/dive-bundaberg/. Re-fetched: describes Burkitt's Reef as a shore-dive site "accessible from the beach," "depths to 9 m" (the dive site's overall depth range, not a reef-crest figure). Used only to corroborate `distance_offshore_m = 0` (it is entered from the beach, not boated to).
- **[S1]** Google Maps satellite imagery (live, via the built-in browser), searches "Burkitts Reef Dive Site, Bargara QLD" and "Burkitt St, Bargara QLD," accessed 2026-09-25. This is a re-check of the same Google Maps resource already listed (as a bare search-URL) in our verified card's images array -- not a new photo/video search. Gave the only size numbers in this file (see Images/figures below).

No new photo or video search was performed, per the task's rules; only already-cited pages/images were re-checked, plus the Google Maps link already present in the card.

## Images/figures relied on

1. **Redgard's 1980 hand-drawn petition sketch** (image hosted via R1's ABC News page): headed "PETITION FOR ROCK REMOVAL," dated 7/9/1980, labeling the headland "BURKITTS REEF." Shows a dense boulder mass at the seaward/outer end ("swell builds up here, tripling its size"), a diagonal band of wave-crest marks running down toward the beach ("waves break here with rocks obstructing surfer"), a cleared "swimmers passage" / "boat passage" channel on the shoreward side, and hazard rocks marked "X" roughly midway along the point. Background landmarks (Esplanade, houses, "Basin," golf course) match today's satellite imagery, confirming the sketch's real-world orientation. **Method:** this is a schematic, not-to-scale hand drawing -- no metric dimensions were or could be read off it. It was used only to corroborate the plan **shape and orientation** (wedge/point, apex seaward), not size.
2. **Construction-era photo, February 1997** (image hosted via R1): the rented Kobelco hydraulic excavator on the basalt boulder shore, with a person standing among boulders marked with white "X" paint. **Method:** used only to cross-check boulder scale (roughly 0.3-1 m across, by eye against the person) and the "X"-marking method matching the sketch. No wide shot / no scale bar, so it was **not** used to estimate the reef's overall length, width or area.
3. **Google Maps satellite imagery** of the point south of Bargara Esplanade Turtle Park (Burkitt Street / Bill Fritz Park), viewed live on 2026-09-25 at zoom levels carrying on-screen "20 m" and "50 m" scale bars. **Method:** identified the rocky point/headland with visibly exposed and breaking rock extending from shore (matching the 1980 sketch's location and general shape); measured the alongshore extent and seaward extent of the visibly rocky/breaking area against the on-screen scale bar (~0.5 m/pixel at the zoom level used); traced a polygon over that extent and computed its area with `shapely`. This is the source of every metric size figure in this file (length ~120 m, width ~46 m, area ~2,480 m²) and of the `distance_offshore_m = 0` confirmation (the rock is continuous with the beach, not a separated bar).

## Derivation table

| Quantity | Value | Method | Source | Uncertainty |
|---|---|---|---|---|
| Shape classification | other / natural headland reshaped in place | Stated in text (converging sources) + 1980 sketch | R1,R2,R3,R6,R8 | None -- well corroborated |
| Alongshore length | 120 m | Satellite imagery, on-screen scale bar | S1 | ±40 m (~35%) |
| Seaward (cross-shore) width | 46 m | Satellite imagery, on-screen scale bar | S1 | ±20 m (~45%) |
| Footprint area | 2,480 m² | Computed (shapely) from traced polygon | S1 | ±50% |
| Distance offshore | 0 m | Stated in text ("not a structure in and of itself"; "accessible from the beach") | R1,R2,R10 | ±0 -- high confidence |
| Intertidal exposure / crest condition | 0 m (dry, low tide) to ~2.5 m (submerged, high spring tide) | Inferred from stated local tide range | R4 | No fixed engineered crest exists; this is the natural tidal range, not a single measured depth |
| Orientation | Right-hand point break; seaward apex roughly NE of takeoff zone | Text description + satellite shape + 1980 sketch | R1,R3,S1 | Qualitative only -- no bearing/angle published |

## Polygon construction

**Coordinate convention:** metres; origin = the shoreline point nearest the reef centroid (approximately the beach access point at the southern end of Bargara Beach, near Bill Fritz Park / Burkitt Street). x = alongshore, positive toward north (approximate -- the coastline here trends roughly N-S; no source gives an exact azimuth). y = offshore, positive seaward (approximately east, into the Coral Sea). The shoreline is approximated as the line y = 0.

**How the vertices were placed:** Because Burkitts Reef is an attached headland rather than a detached structure, its landward edge runs at or near y = 0 for most of its alongshore length. The polygon was traced by eye over the Google Maps satellite view [S1] to follow the visible boundary of exposed/breaking rock: it starts and ends at two points where the rock meets the sandy beach (x = -70 and x = 10, both at y ≈ 0), bulges seaward to a maximum of y ≈ 46 m near the densest boulder mass identified in both the satellite image and the 1980 sketch (around x = 25-42), and tapers back toward shore at the northern end. The polygon is closed (first vertex = last vertex) and was checked with `shapely.geometry.Polygon` -- confirmed `is_valid = True` (non-self-intersecting), area = 2,479.5 m² (rounded to 2,480 in the JSON).

This polygon is **explicitly an estimate of the natural rock/reef extent visible today, not a designed or surveyed footprint** -- no such footprint exists for this reef in any source checked.

## Gemini comparison

| Quantity | Gemini | Ours | Verdict |
|---|---|---|---|
| shape_type | N/A -- no CAD entry | `other` (rough polygon now drawn) | We agree no engineered footprint exists, but provide a documented rough estimate rather than leaving it blank |
| length_m / width_m | 80 x 40 (uncited prose) | ~120 x ~46 (satellite scale-bar estimate) | **Disagree with Gemini's specific number** -- see below |
| area_m2 | Not computed | ~2,480 m² | New -- Gemini computed nothing |
| crest_depth_m | 0.2 to 2.5 (uncited prose) | 0 to ~2.5 (re-derived from R4's stated tide swing) | Same order of magnitude/direction; ours is tied to a specific sourced figure |
| distance_offshore_m | "not stated -- in-situ... not an offshore structure" | 0 m (sourced) | **Agree** in substance; we make it an explicit sourced value |
| orientation | N/A | Right-hand point break, qualitative | We provide a qualitative description Gemini did not attempt |

**On the 80 m x 40 m figure specifically:** the task brief already flagged this as suspicious (Gemini's own card presents it with zero citation). We independently verified this is worse than just "uncited":

- Gemini's own reference list for this reef has 4 entries. We checked all 4:
  1. **"ABC News Australia 2024-01-21"** -- Gemini's file gives the URL `https://www.abc.net.au/news/2024-01-21/burkitts-reef-bundaberg-greg-redgard-surfing/103328224`. We fetched it directly: **HTTP 404 -- the page does not exist.** The real ABC News story about this reef (which we cite as R1) is dated 2024-01-28 with a different URL and slug, and contains no dimensions at all when re-checked.
  2. **"The Inertia 2021"** -- Gemini's file links only to `theinertia.com` (the homepage), not a specific article.
  3. **"Swellnet Australia 2022"** -- links only to `swellnet.com` (the homepage).
  4. **"Tracks Magazine 2023"** -- links only to `tracksmag.com.au` (the homepage).
- None of the 4 references, even if fully accessible, could plausibly be the source of a specific "80m x 40m" figure -- three are bare homepages and the fourth is a dead link.
- We instead measured the visible rock/reef extent on Google Maps satellite imagery with an on-screen scale bar and got a larger footprint (~120 x ~46 m) with a different aspect ratio than Gemini's 80 x 40. Both numbers are estimates rather than published measurements, but ours is tied to a specific, checkable method (S1) with stated uncertainty; Gemini's is not traceable to any source at all, and one of its four citations is a dead link.

## Open issues

- Burkitts Reef is a natural basalt headland reshaped in place, not an engineered structure -- every geometric figure in the footprint JSON (polygon, length, width, area) is our own visual estimate from satellite imagery, not a surveyed or designed footprint. Confidence is **low**.
- The boundary between "the reef" and the surrounding sandy/rocky shore is inherently fuzzy and was judged by eye; a different analyst could reasonably draw a materially different, differently-sized polygon.
- Precise reef coordinates remain unpublished (already flagged in the verified card); the card's lat/lon is Bargara town centre, not the reef itself. The footprint polygon here uses local metres relative to an approximate shoreline origin, not a surveyed lat/lon.
- No source gives a compass bearing or numeric arm angle for the point; orientation is qualitative only.
- Gemini's ABC News reference for this reef (URL ending `103328224`, dated 2024-01-21) returns HTTP 404 -- it appears to be a dead or fabricated link, a distinct and additional problem beyond the uncited "80m x 40m" figure the task brief already flagged.
- Adding this reef to a scale-comparison UI tab in `04_build` (the site itself) is outside the scope of this footprint-research task; this pass only produces the researched JSON and this provenance document.

## Verification 2026-09-25

Adversarial re-check of every row of the Derivation table and every claim in the Gemini comparison, performed by opening each cited source directly (WebFetch for text pages; the built-in browser for Google Maps and the two ABC-hosted images) and by recomputing the polygon geometry independently in Python. Full itemized results are in the JSON's `verification` array; summary:

**Confirmed as stated (no change needed):**
- R1 (ABC News 2024-01-28) loads, has no dimension figures, and is the correct source of the "2 or 3 metres" quote and the two images used for shape corroboration.
- R2 (Wikipedia) contains the exact "not a structure in and of itself" sentence, no dimensions.
- R3 (Coastal Management/ICM) gives "Approximate volume: 300m³" and the "peeling right-hand wave" phrase, no length/width.
- R4 (Raised Water Research) gives the exact "2.5m tide swings" sentence, no footprint figure.
- R6 (Yahoo Lifestyle) confirms the 30-tonne excavator / hand-carried-bricks method, no dimensions.
- R10 (DivePlanit) confirms "accessible from the beach" and "depths to 9m" exactly as characterized (dive-site range, not a reef-crest figure).
- Gemini's `reef_footprints.json` (16 structures, checked by loading and parsing the file directly) contains **no** Burkitts Reef entry at all -- confirms `shape_type: "N/A - no CAD entry"` is accurate, not an exaggeration.
- Gemini's prose dossier (`02_world_reefs_data/burkitts-reef-bargara.md`) was read directly and matches our characterization word-for-word: "operates over an 80m × 40m intertidal basalt flat," "0.2m ... to 2.5m," and all 4 references (ABC News 2024-01-21, The Inertia, Swellnet Australia, Tracks Magazine) exactly as quoted.
- Gemini's cited ABC News URL (`.../2024-01-21/.../103328224`) independently re-confirmed as HTTP 404.
- Polygon math: recomputed bbox, shoelace area, and max pairwise vertex distance from the exact `polygon_m` array in Python -- bbox is exactly 120 × 46 m, area is 2,479.5 m² (rounds to the stated 2,480), max dimension is 124.19 m (rounds to the stated 124). No arithmetic errors found.
- Shape classification and `distance_offshore_m = 0` were re-checked against a fresh live view of the point on Google Maps satellite imagery (built-in browser, 2026-09-25): a wedge-shaped rocky point continuous with the shoreline at Bill Fritz Park/Esplanade, consistent with "other" / attached headland and inconsistent with any engineered template shape.

**One correction made:** the draft cited **R8** (Swellnet comment thread) alongside R4 for the "~2.5 m tide swing" figure used to derive `crest_depth_m`. Re-fetching the exact R8 URL (the built-in browser was needed -- WebFetch returned `ECONNRESET` for this URL twice) shows the "truebluebasher" post discusses the 1982 proposal, the ~300 m³/12-boulder figures, the $10,000 cost, and the "30 days/yr + overhead 4 days/yr" before/after performance stats, but the string "2.5" does not appear anywhere in the visible thread text. **Fixed**: the JSON's `crest_depth_m.ref`, the matching derivation-table row, the Sources bullet for R8, and both Gemini-comparison rows referencing the tide swing now cite **R4 alone**; R8 remains cited only for what it actually supports (timeline/cost/before-after stats).

**Left as an open, honestly-flagged uncertainty (not changed):** the core geometry figures (120 m alongshore × 46 m seaward, ~2,480 m²) are S1's (this dossier's own) visual estimate from satellite imagery, not a published or surveyed figure. I attempted an independent rough re-measurement using the same live Google Maps view -- reading the on-screen scale bar via the page's own DOM (cross-checked at two zoom levels, internally consistent at ≈1.3 m per screenshot pixel) and eyeballing pixel spans across the point. Google Maps' "measure distance" tool could not be driven reliably through the browser-automation interface used here (menu-click targeting was inconsistent across attempts), so no exact independent distance readout was obtained. My rough pixel-ruler cross-check landed in the same broad order of magnitude (tens of meters both alongshore and cross-shore) as the stated 120 m / 46 m, but my own measurement carries comparable imprecision (different plausible choices of shoreline "attachment point" on a continuously curving coastline can swing the answer by 30-60%). Per the task's instruction to default to "unsupported" rather than invent a tighter number, **the L/W/area values are left unchanged** and confidence stays **low** -- this file does not claim more precision than either estimate can support, and says so explicitly here rather than silently keeping the original number unchallenged.

**Net effect on confidence:** unchanged at **low** (this was already the lowest tier available and remains appropriate -- if anything, this pass reinforces rather than reduces the uncertainty already flagged).

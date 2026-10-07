# Media re-check — Pratte's Reef / Chevron Reef (El Segundo, CA)

Date: 2026-09-25. Trigger: Lior found two accepted videos for other reefs showed only beach/surfing, never the structure, so every accepted image/video/frame on this card was re-checked against the rubric (structure_visible / reef_effect_visible / site_context_only / unrelated_or_wrong_site / could_not_load).

Method: each image URL was downloaded to a session scratchpad with `curl -L -A "Mozilla/5.0"`, viewed directly (not just captioned), classified against the dossier's structure description (submerged V/chevron sand-filled geotextile bags, built 2000-2001, ~200 bags, crest below low-tide level), then the scratch copy was deleted. No frame folder exists for this reef (03_images/video_frames/prattes-reef-el-segundo/ is empty — nothing to check there). The one video was checked via its saved transcript (mCOc7Knhdwc.txt) and the JSON's key_quotes/what_it_shows field — not re-downloaded.

## Images (dossier `images` array, in card order)

| # | URL | What I saw | Verdict | Evidence relied on |
|---|---|---|---|---|
| 1 | raisedwaterresearch.com/.../Building-Prattes-Reef.jpg | Crane on a barge hoisting a large light-tan sand-filled geotextile bag out of the water; El Segundo power-station red/white-striped smokestacks and the DWP building visible onshore behind Dockweiler Beach | **structure_visible** | Direct viewing — the bag itself is the subject, mid-air during placement. Matches dossier's "barge-mounted crane" construction method and the smokestack landmark confirms El Segundo/Dockweiler location |
| 2 | raisedwaterresearch.com/.../Diving-Prattes-Reef.jpg | Underwater photo: a long ribbed/segmented sand-filled bag lying on a sandy seabed, sunlight from the surface above, a diver's fin at bottom-left | **structure_visible** | Direct viewing — the submerged bag structure is the entire frame, consistent with dossier's diver-survey findings ("bags had moved, sunk, and been buried by sand") |
| 3 | raisedwaterresearch.com/.../Prattes-Reef-Bag-Size.jpg | Scale diagram: a single Pratte's Reef bag (3 m × 1.2 m) drawn beside a VW camper, a city bus, and a Mount Reef "bag" (20-60 m) for comparison | **structure_visible** (diagram, not photo) | Direct viewing — this is exactly the kind of scale-comparison diagram Lior's `image26.png` reference uses; it independently confirms the dossier's "bags were markedly smaller (~8 m3 each)" claim with a concrete 3 m × 1.2 m dimension |
| 4 | raisedwaterresearch.com/.../Prattes-Removal.jpg | Sepia-toned beach photo: a workboat/tug offshore, a bulldozer and two workers on the sand, an orange traffic cone; no bag or reef structure visible in frame | **site_context_only** (borderline) | Direct viewing — the boat+bulldozer combination is consistent with the dossier's description of the fall-2008 removal operation and the source page's own EXIF-dated caption, but no bag/structure is actually visible in this shot, so it does not meet the `structure_visible` bar on image content alone |
| 5 | images.squarespace-cdn.com/.../Pulling+Bag+Ashore.JPG | A worker in a red shirt pulling a flattened, discolored/stained fabric bag up the beach by ropes; a tug/workboat is visible offshore | **structure_visible** | Direct viewing — the actual deteriorated geotextile bag is the main subject on the sand, and the source page (Coastal Frontiers, "Removal of Pratte's Reef") captions it "Pulling Bag Ashore," directly tying it to the reef |
| 6 | raisedwaterresearch.com/.../Pratts-Reef-Diagram.png | Skelly Engineering plan-view CAD diagram: V/chevron rows of bag outlines at 45° to "WAVE DIRECTION," labeled "PRATTE'S REEF," bag count 110, scale bar, engineer's stamp | **structure_visible** (diagram) | Direct viewing — matches dossier's "V-shaped (delta/chevron) reef... arms at roughly 45 degrees" design description and the Phase I bag count of 110 |
| 7 | Google Maps satellite link (live map, not a static file) | Not downloaded — this is a live Google Maps view, not a static hotlinkable image file | **could_not_load** (not a checkable static image) | Per dossier's own `gaps` note: "Google Maps satellite link (image #7) is a live map, not a static, independently hotlink-testable image file" |

`images_rejected` array in the card is empty — nothing to re-check there.

## Videos

| Video | Title | Channel | Verdict | Best timestamp | Evidence |
|---|---|---|---|---|---|
| https://www.youtube.com/watch?v=mCOc7Knhdwc | "Pratte's Reef" | Kurt Schaefer | **about_the_reef** | 1116 s (00:18:36) | Transcript (mCOc7Knhdwc.txt) confirms the video is a ~30-min documentary built around on-camera interviews with reef designer Dave Skelly explaining the design directly: "[00:18:36] My concept is to put out gigantic sand bags — a nice bag weighs about 12 to 14 tons... Geotextile fabrics... will last probably at least two decades" and "[00:19:04] ...The formation... is a chevron shape formation, or v-shaped..." The film's own closing line ("[00:26:03] whether the crest of the perfect wave will ever rise from the waters off El Segundo remains to be seen") confirms it predates/brackets construction and is entirely about this project's origin, design and mitigation history — not generic beach/surf footage. |

Note: unlike the two videos Lior flagged elsewhere, this one is not surf footage at all — it is a talking-head documentary about the reef's history and design, so the "shows surfing but never the structure" failure mode does not apply here. It contains no shots of the built structure itself, but its content (interviews about the design) is squarely `about_the_reef`, not `site_only`.

## Frames

No frame files exist for this reef (`03_images/video_frames/prattes-reef-el-segundo/` is present but empty, and there is no `rejected/` subfolder). Nothing to classify.

## Recommended hero image

**Image #1 — Building-Prattes-Reef.jpg** (crane hoisting a bag, smokestacks in background). It is unambiguous `structure_visible`, shows the reef's actual sand-filled geotextile bag material and scale being placed, and is visually the most legible single frame (compare to #2's murky underwater shot, #4's structure-less removal-day beach shot, and #5's close-up ground-level bag that lacks any wider context). Diagrams #3 and #6 are excellent supporting scale/plan graphics but are not photographs, so they are a poor fit for a "hero" photo slot.

## Everything downgraded/flagged vs. the existing card

None of the 6 checkable images fail the rubric outright; all are legitimately tied to the reef (5 clearly `structure_visible`, 1 borderline `site_context_only` — #4, the removal-day beach shot with no bag visible in frame). Recommend the card's caption for image #4 be tightened to make clear it documents removal-operation logistics rather than showing the structure itself. Image #7 (Google Maps) was already correctly flagged in the card's own `gaps` field as not a static file.

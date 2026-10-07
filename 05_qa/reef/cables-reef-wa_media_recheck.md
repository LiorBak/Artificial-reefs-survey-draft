# Media re-check — Cable Station Reef (cables-reef-wa)

Date: 2026-09-25
Method: each accepted image was downloaded to a scratch folder with `curl -L -A "Mozilla/5.0"`, viewed directly, classified against the rubric using the dossier's description of the structure (granite boulders on limestone bedrock, submerged, crest 1-3 m below average tide — never exposed, never a construction/aerial shot possible), and the source page's own caption/context was checked. Scratch copies were deleted after viewing (`rm cables/*.jpg`). No videos or frames exist for this reef — the card's own `videos: []` and its `gaps` note ("No video content found for this site (0 videos, 0 frames)") were confirmed against `02_research/videos/cables-reef-wa/` and `03_images/video_frames/cables-reef-wa/`, neither of which exists on disk, so there is nothing to re-check in those two categories.

## Images

| # | URL | Source page | What I saw | Classification | Reasoning |
|---|---|---|---|---|---|
| 1 | raisedwaterresearch.com/.../Cables-Reef.jpg | Raised Water Research "Cables Reef" spot page | A clean, peeling left-hand wave breaking with ~8 surfers in the lineup, overcast light, offshore/point-break framing | **reef_effect_visible** | The reef structure is permanently submerged (crest 1-3 m below average tide per the dossier) so it can never be "visible" itself; this is the site's dedicated spot-page hero photo of the wave the reef produces, at the named break, matching the dossier's description of a "gently barreling," 45°-peel-angle left/right |
| 2 | raisedwaterresearch.com/.../cabletopturn.jpg | Raised Water Research "Cables Reef" spot page | A surfer completing a top turn on a clean wave face, one other surfer sitting in the water | **reef_effect_visible** | Same source page dedicated to this specific break; shows the wave quality (clean face, makeable turn section) the reef was designed to create, at the reef's location |
| 3 | raisedwaterresearch.com/.../Cables-Side-View.jpg | Raised Water Research "Cables Reef" spot page | Hand-drawn cross-section diagram labelled "Existing Sea Bed" and "Proposed Enhancement," showing a mound of fill placed on the seabed and the resulting sea-surface profile | **structure_visible** | This is a schematic of the reef structure itself (the design cross-section), not a photo of surf — it directly shows the engineered profile (rock placed on existing bedrock, raising the bed to shape the wave), matching the dossier's "physical-model design" description [R8] |
| 4 | surfingdownsouth.com.au/.../1948-Surfing-Cable-Station-Cottesloe...jpg | Surfing Down South, "Cable Station reef since the 1940s" | 1948 black-and-white water photo: three riders on paddleboard/toothpick boards riding a wave, bow of a boat in foreground | **site_context_only** | Same natural break location, but this predates the 1999 artificial reef by 51 years — it documents the pre-existing natural reef, not the built structure or its effect; keeping it only as historical/site context per the dossier's own caption |
| 5 | i0.wp.com/surfingdownsouth.com.au/.../1957-City-Beach-BC-crew...jpg | Surfing Down South, "Cable Station reef since the 1940s" | 1957 black-and-white beach photo: five young men posing on sand with paddles and a car, boards racked on the car roof, no water/wave visible at all | **site_context_only** | Onshore group photo, no wave or structure visible, predates the reef by 42 years; generic historical beach-culture image with no link to the artificial reef |

No images were `unrelated_or_wrong_site` or `could_not_load` — all five downloaded and displayed correctly and are genuinely of Cable Station/Cottesloe.

## Videos

None. `videos: []` in the reef card, and no `02_research/videos/cables-reef-wa/` folder exists on disk. Nothing to classify.

## Frames

None. No `03_images/video_frames/cables-reef-wa/` folder exists on disk (consistent with zero videos). Nothing to classify.

## Recommended hero image

**Image #1 (`Cables-Reef.jpg`)** — the clean, well-formed peeling wave with a full lineup of surfers, on the site's own dedicated Cables Reef page. It is the single clearest visual demonstration of the reef's surf-enhancement effect (the wave shape/consistency being what the whole project was built for), and is already the raisedwaterresearch.com header image for this exact break. Image #3 (the side-view diagram) is the best available **structure** image — the only one that shows the engineered form itself rather than its surface effect — and is worth keeping as a secondary "how it's built" panel, since no other image in the accepted set shows the reef's mass at all (it is fully submerged and no construction/aerial/drone imagery was found for this site, consistent with the dossier's own gap note).

No changes to `images_rejected` are needed — the existing Google Maps rejection stands. No image needs to move from `images` to `images_rejected`: all five are genuinely tied to the correct location, they simply split between showing the reef's surf effect (1, 2), the engineered structure in diagram form (3), and pre-reef historical site context (4, 5). Recommend re-tagging 4 and 5 in the card's `images` array with an explicit note that they predate construction (pre-1999, natural reef only), so a future reader does not mistake them for post-construction evidence.

# Media re-check — Southern Ocean Surf Reef ("Midds Reef"), Albany WA

Date: 2026-09-25. Rubric applied per harness instructions to every accepted image, video, and frame
listed in `02_research/reefs/southern-ocean-surf-reef-albany.json`. No new photo/video search was
performed; only already-cited media was re-examined.

Reference context used to judge the images (from the dossier, all already-cited):
- `size`: "Length 165 m; width up to 110 m; crest at -1.0 m AHD ... reef sits ~140 m offshore [R3]"
- `type`: "Submerged rock-berm surf reef, ~70,000 t of layered granite in three graded layers ... no geotextile [R2][R3][R1]"
- The reef is fully **submerged** (crest -1.0 m AHD) — it is never expected to break the surface, so a
  correct "structure visible" classification for this reef means an aerial/drone shot showing the
  dark elongated rock-berm shadow under shallow turquoise water (construction-era images), not a
  dry, exposed structure.

## Images (6 accepted in the card)

| # | URL (truncated) | Source page | Caption/context relied on | Classification | Notes |
|---|---|---|---|---|---|
| 1 | abc-cdn `1acef1f7...` | ABC News article (R2) | Same article as #2; wide establishing shot: hills, anchored bulk carrier, breaking wave with surfer | **reef_effect_visible** | No structure visible (submerged reef), but the peeling wave shape, the surfer, and the identical hill/ship backdrop to image #2 (which ABC explicitly captions as the reef wave) place this at the reef break. Article is entirely about this reef opening — no other wave in the area is the subject. |
| 2 | abc-cdn `1927a3b2...` | ABC News article (R2) | ABC's own caption: **"A clean wave breaks on the Albany surf reef."** | **reef_effect_visible** | Direct source caption naming the reef. Strongest-evidence image in the set. |
| 3 | abc-cdn `8ffae200...` | ABC News article (R2) | ABC caption: "Specialised vessels came from around the world to build the Albany surf reef." Viewed image: aerial/drone shot, dredge/crane barge working over a submerged elongated dark rock-berm shape in turquoise water. | **structure_visible** | The reef footprint (dark elongated shadow under the barge) is directly visible mid-construction — matches the dossier's "no geotextile, rock-berm" description and the ~165 m elongated shape. |
| 4 | raisedwaterresearch `...Surfing-Waves...png` | Raised Water Research spot page (R10) | Surfer bottom-turning on a breaking wave, whitewater peeling left. Page is RWR's dedicated "Midds Reef" spot page (not a generic WA surf page). | **reef_effect_visible** | No structure visible (expected — reef is submerged), but the image sits on a page whose entire subject is this specific reef break; no caption explicitly says "at the reef" the way image #2 does, so evidence is slightly weaker — kept as reef_effect_visible rather than site_context_only because RWR spot pages are reef-specific, not beach-generic. |
| 5 | raisedwaterresearch `...construction-overview.jpg` | Raised Water Research spot page (R10) | Embedded EXIF caption: **"An aerial shot of the Great Southern's artificial surf reef under construction in May, 2025."** Viewed image: aerial shot of turquoise water, clear elongated dark submerged rock-berm shadow, small dredge vessel alongside. | **structure_visible** | EXIF caption plus visible footprint shape (elongated, ~165 m proportions) both confirm this is the reef under construction, not a generic beach shot. |
| 6 | albany.wa.gov.au `design.jpg` | City of Albany project page (R3) | Official Bluecoast Consulting Engineers design table + plan-view diagram: crest length 110 m, offshore 140 m, left-hander, 41% surfability, position 350 m north of Big4 caravan park. | **structure_visible** (diagram, not photo) | This is an engineering design diagram, not a photograph — it directly documents the structure's plan shape, dimensions and position (matches `size` field numbers exactly), so it counts as structure-visible documentation even though no camera image of rock is present. Flagged distinctly from photographic evidence in case the build wants photo-only heroes. |

No images were reclassified as `site_context_only` or `unrelated_or_wrong_site`; none failed to load.
No `images_rejected` entries needed re-checking (the one rejected entry is a non-downloadable Google
Maps link, already correctly excluded).

## Videos (3 in videos.json)

| Video | Title | Classification | Evidence |
|---|---|---|---|
| SE4GNR4EiUQ | "'High-performance' artificial reef transforms town's surf scene" — ABC News | **about_the_reef** | Transcript (`SE4GNR4EiUQ.txt`): "The $13 million project involved the placement of 70,000 tons of rock on the seabed" (~00:19); shows surfers riding the wave at Middleton Beach specifically framed as the reef story throughout; interviews Peter Bolt (reef advocate) and a local surfer praising "a really high performance wave." best_timestamp_seconds: 19 (cost/construction fact) and 87 ("It's a really high performance wave"). |
| lLr6z5axJew | "Albany Artificial Surf Reef Project" — City of Albany (2020) | **about_the_reef** | Per dossier's own verified description: official 2020 pre-construction consultation video, description names Bluecoast Consulting Engineers and Middleton Beach — content is entirely about this reef proposal (concept-stage, not built footage, but unambiguously about the reef, not the beach in general). No transcript file was saved; classification rests on the already-verified yt-dlp metadata (title + description) cited in the card, consistent with the harness's "no new photo/video searches" instruction. |
| 6kwDBzf67EU | "Middleton Beach Artificial Reef" — filmed by Liam De Lucia (2025) | **unknown** | Confirmed dead: yt-dlp reports "This video is not available." Cannot classify content; correctly kept link-only per the card's existing SKIP-uncertain rule. No re-check possible without a new external search, which is out of scope. |

## Frames

`03_images/video_frames/southern-ocean-surf-reef-albany/` does not exist (confirmed by directory
listing during this re-check). This matches the dossier's own `gaps` entry: "No frame files exist in
03_images/video_frames/southern-ocean-surf-reef-albany/ for this item." Nothing to classify.

## Comparison to the flagged problem

Lior's original concern — "two accepted videos showed surfing at the beach but never the artificial
reef" — does **not** reproduce for the two live videos in this card as currently listed: both
SE4GNR4EiUQ and lLr6z5axJew are specifically about the Albany reef project (opening-day news segment;
official project video), not generic Middleton Beach surf footage. The one video that could plausibly
match "surfing shown, reef not shown" is the dead/unconfirmable 6kwDBzf67EU, which is unreachable for
verification either way. If Lior has a different pair of videos in mind (e.g. from a different reef,
or videos since removed from this card), that should be flagged back for reconciliation.

## Recommended hero image

**Image #2** (abc-cdn `1927a3b21137e3775326b744d308276e...`, ABC News) — the only image in the set with
an explicit source caption ("A clean wave breaks on the Albany surf reef") tying the visual directly
to this reef, showing a clean peeling wave with a surfer, plus recognisable King George Sound
background (hills, anchored ship) that a reader can cross-check against the location. If a
construction/structure hero is wanted instead, **image #5** (Raised Water Research aerial, EXIF-
captioned "artificial surf reef under construction") is the clearest photographic view of the
submerged rock-berm footprint itself.

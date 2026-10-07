# Media re-check — Bunbury Airwave

Checked 2026-09-25. Method: each accepted image was downloaded to a temp scratchpad (`curl -L -A "Mozilla/5.0"`), viewed, classified, and deleted afterward. The one accepted video was not downloaded (per rules); its `videos.json` entry, manual shot-log transcript (`11804314_notes.txt`), and both saved frame files were read/viewed instead. Rubric: **structure_visible** / **reef_effect_visible** / **site_context_only** / **unrelated_or_wrong_site** / **could_not_load**.

Context for this check: Lior flagged that on a *different* reef, two accepted videos showed surfing at the beach but never the structure. For Bunbury Airwave, only **one** video is in the accepted card (`11804314`, ABC News); the two YouTube videos (live surf-cam, podcast) are already marked `"status": "unavailable"` in `videos.json` and were never promoted into the card's `videos` array — so there was no live risk of that specific failure mode here, but every item was re-checked from scratch anyway per the instructions.

## Images (6 accepted)

| # | URL (short) | Card says it depicts | Classification | Agrees w/ card? |
|---|---|---|---|---|
| 1 | `...cc84b431...` (ABC) | Torn seam, underwater, post-tear | **structure_visible** | Yes |
| 2 | `...1a68756f...` (ABC, via Instagram airwavesurfreef) | Design/technology graphic | **structure_visible** (design render, not a photo) | Yes |
| 3 | `...0db44994...` (ABC) | Aerial of Back Beach, install site (pre-install) | **site_context_only** | Yes |
| 4 | Raised Water Research `Airwave-from-Above.jpg` | Aerial/drone of bladder in water during install | **structure_visible** | Yes |
| 5 | Raised Water Research `Airwave-Tear.jpg` | Close-up of torn seam | **structure_visible** | Yes |
| 6 | Raised Water Research `AirwaveDiagram2.jpg` | Waveco's own technical diagram | **structure_visible** (design render, not a photo) | Yes |

Notes:
- Images 2 and 6 are computer-generated concept renders of the dome bladder, not photographs of the real installed unit. The card already describes them correctly as "design/technology graphic" and "technical diagram," so there is no mismatch — just flagging here that they should not be treated as photographic proof of as-built appearance.
- Image 3 is a genuine pre-installation site photo (June 2019 companion article, before the December 2019 install) with no structure visible — again, the card's own caption already frames it as a site photo, not reef evidence, so no change needed.
- Images 1, 4, and 5 are all consistent, independently-sourced (ABC + Raised Water Research) photographic evidence of the actual bladder in the water and its torn seam. Image 4 in particular matches the ABC video's own aerial frame (`11804314_0005.jpg`) almost exactly — buoy position, tether line, and bladder shape line up — which cross-confirms both sources are showing the same real event.
- The one rejected image (Google Maps URL) was re-confirmed as correctly excluded — it is an HTML app shell, not a fetchable image.

## Video (1 accepted)

| Video | Classification | Best timestamp | Evidence |
|---|---|---|---|
| ABC News `11804314` "Dream on hold for Bunbury surfers" | **about_the_reef** | ~00:03 | Shot log: aerial shot (00:00–00:08) shows "the inflated white Airwave bladder sitting on the seabed, a diver near it, and an orange marker buoy nearby." Frame `11804314_0005.jpg` (viewed) confirms this. The remainder of the 35s clip is a vox-pop with tourist surfer Camille-Audrey Perron reacting to the reef's installation failure — on-topic throughout, not incidental beach surfing footage. |

The two excluded YouTube videos (live surf-cam `K2DQ-C7OR0U`, Digital Hitmen podcast `hfz92plwENs`) were re-confirmed as genuinely unavailable (yt-dlp "Video unavailable," thumbnail 404s) and correctly kept out of the accepted card.

## Frames (2, non-rejected folder)

| Frame | Classification | What I saw |
|---|---|---|
| `11804314_0005.jpg` | **structure_visible** | Aerial drone shot, ABC watermark: pale circular submerged bladder, orange marker buoy, faint tether line, diver's shadow at the bladder's edge. |
| `11804314_0010.jpg` | **site_context_only** | Beachfront interview shot of Camille-Audrey Perron at the Back Beach access point (surf-club mural, "NO ACCESS BEYOND THIS POINT" sign); no reef/water/bladder visible in frame. Legitimate as the sourced quote's visual anchor, but not reef evidence on its own. |

## Verdict

No problems found matching the "surfing at the beach, never the structure" failure pattern for this reef. Of 6 accepted images, 5 are structure_visible (3 real photos + 2 design renders, all correctly labeled as such in the card) and 1 is a correctly-labeled pre-install site photo. The single accepted video and its two saved frames are consistent and on-topic. **No changes to `bunbury-airwave.json` are recommended based on this re-check.**

## Recommended hero image

**`https://raisedwaterresearch.com/wp-content/uploads/2019/12/Airwave-from-Above.jpg?v=1576553483`** (Raised Water Research, "Airwave-from-Above.jpg")

Rationale: clearest, highest-resolution, unambiguous aerial photo of the actual bladder in the water (dome + orange buoy + tether line all visible), and independently corroborated by the ABC video's own near-identical aerial frame (`11804314_0005.jpg`) — two independent sources agree on the structure's real in-situ appearance, which is the strongest evidentiary basis available among the accepted media.

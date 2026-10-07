# Media re-check — Burkitts Reef ("Greg's Reef"), Bargara

Verified against card `02_research/reefs/burkitts-reef-bargara.json` (2026-09-25). Method: each image URL downloaded to a scratch temp folder with `curl -L -A "Mozilla/5.0"`, viewed directly, classified per the rubric, then the scratch copy deleted. Videos were not downloaded; classified from `02_research/videos/burkitts-reef-bargara/videos.json`, its embedded captions/frame descriptions, and the two already-extracted frame files. No new photo/video search was performed.

## Images (card's `images[]`, in order)

| # | URL (truncated) | Depicts (card) | What I actually saw | Classification | Basis |
|---|---|---|---|---|---|
| 1 | `...a450bbac.../` (ABC) | Redgard's 1980 hand-drawn petition sketch | A hand-drawn diagram labeled "PETITION FOR ROCK REMOVAL," 7/9/1980, with the headland explicitly labeled "BURKITTS REEF," arrows marking "swell builds up here tripling its size" and "waves break here with rocks obstructing surfer," rocks/houses/esplanade sketched in plan view | **structure_visible** | It is a planning sketch, not a photo, but it directly and explicitly depicts the reef's location, shape and the hazard rocks by name — the dossier's own source for the pre-1997 hazard layout [R1] |
| 2 | `...a6112bacd.../` (ABC) | Kobelco excavator + boulder shoreline, Feb 1997 construction | A yellow Kobelco hydraulic excavator on a basalt boulder shoreline, a man standing among the rocks near the waterline, white-painted X marks on several boulders (consistent with marking boulders for removal) | **structure_visible** | Matches dossier's "Kobelco hydraulic excavator...breaking down/relocating boulders" construction description exactly [R1][R4] |
| 3 | `...a315cc055.../` (ABC) | Greg Redgard surfing "Greg's Reef" | A surfer crouched, riding inside a clean peeling green wave face, no reef structure visible (it is submerged) | **reef_effect_visible** | Structure is a reshaped natural reef, submerged/awash — caption on the ABC source page explicitly places this at Burkitts Reef ("Greg's Reef"), and the peeling wave face matches the dossier's described wave [R1] |
| 4 | `...8e0f6ec39.../` (ABC) | Surfer at Burkitts Reef, captioned "reef remains a popular surfing location" | Backlit silhouette of a surfer doing a top turn on a breaking wave | **reef_effect_visible** | Source-page caption explicitly ties this shot to the reef location and current-day surfing use [R1] |
| 5 | `...69d978b4b.../` (ABC) | Tahlija Redgard surfing pro circuit, grew up on Burkitts Reef | Surfer deep inside a large green barrel, wave curling overhead | **reef_effect_visible** | Caption on source page explicitly attributes this to growing up surfing Burkitts Reef; wave shape (peeling, occasionally barreling) matches dossier's outcome text [R1] |
| 6 | Google Maps search link | Map/satellite search, approximate place-name | Not a photo — a Google Maps search-by-name URL, not a pinned coordinate, not downloadable/viewable as an image | **site_context_only** | It is a location pointer only, carries no structural evidence of its own; correctly labeled "map" in the card, not a claim about the structure |

No images were reclassified out of "accepted" — all 5 photos hold up; the map entry is not a photo and was already labeled honestly as a map link.

## Videos (`02_research/videos/burkitts-reef-bargara/videos.json`)

| Video | Title | Classification | Evidence |
|---|---|---|---|
| `wuJ__7Js-cY` | "Diving Bargara, Burkitt's Reef Marine Park" (Black Beard Diving, 2021) | **site_only** | Uploader description covers a shore dive at "Burkitts Reef Marine Park" (sandy/rocky bottom, hard coral bommies, reef fish, per description also sea snakes/moray eels/gummy sharks). This is the dive-tourism reef at the same place name, but nothing in the title/description mentions Greg Redgard, the 1997 excavator reshaping, or the surf break — it documents marine life, not the artificial/reshaped surf structure the card is about. Both extracted frames (`wuJ__7Js-cY_0025.jpg` snail on sand, `wuJ__7Js-cY_0205.jpg` fish over coral) show generic dive-site marine life with no boulders/excavator/surf context, and were already moved to `03_images/video_frames/burkitts-reef-bargara/rejected/` by a prior pass — confirmed correct on re-view. |
| `O3bEn8029XQ` | "Surfing at Bargara Beach, QLD" (Campr, 2018) | **site_only** | Card's own `what_it_shows` already flags this as generic Bargara Beach surf-tourism footage with no mention of Burkitts Reef, Greg Redgard, or the point break in title/description/metadata; `embed_ok: false`. This matches the exact failure pattern Lior flagged (surfing at the beach, never at/about the reef) — correctly already labeled as an uncertain/unconfirmed lead in the card, not asserted as depicting the reef. No stronger link found on re-check. |

Neither video should be treated as `about_the_reef`; both were already correctly hedged/excluded in the existing card (video1 as marine-park diving footage with no surf-reef content, video2 explicitly labeled unconfirmed). No change needed to the card's `videos: []` list (it is empty — these two live only in the separate videos.json index, not asserted as accepted evidence in the reef card itself).

## Frames (`03_images/video_frames/burkitts-reef-bargara/`)

The only two extracted frames for this reef are already inside the `rejected/` subfolder (`wuJ__7Js-cY_0025.jpg`, `wuJ__7Js-cY_0205.jpg`); there are zero frame files directly under the reef's `video_frames` folder outside `rejected/`. Both were re-viewed above under the video section and confirmed correctly rejected (generic dive-site marine life, no link to the artificial/reshaped structure or its surf effect).

## Recommended hero image

**Image #2** (Kobelco excavator on the boulder shoreline, Feb 1997) — it is the single clearest, most unambiguous `structure_visible` shot: it shows the actual construction work (excavator + marked boulders) that is the entire subject of this reef's story, and is unlikely to be confused with generic beach/surf photography the way the wave-riding shots (#3-5) could be. Runner-up: Image #3 (Redgard surfing "Greg's Reef") for a hero that shows the *effect* rather than the construction.

## Summary of changes vs. the existing card

No accepted image or the empty `videos: []` list needed correction — the card was already accurate: all 5 photos have direct source-page captions or unmistakable content tying them to the reef (construction or its wave effect), and the two videos in the separate `videos.json` index were already appropriately hedged/excluded rather than asserted as confirmed reef evidence. This re-check is a confirmation pass, not a fix.

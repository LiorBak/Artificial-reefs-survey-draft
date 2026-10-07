Status: verified 2026-09-24 — 5 web images tested, 1 map link (no image test needed), 3 videos tested, 0 video frames (none extracted for this item).

# Adversarial media verification — Kovalam Reef (Lighthouse Beach), India

Target: `03_images/web/kovalam-reef-india.json`, `02_research/videos/kovalam-reef-india/videos.json`, `03_images/video_frames/kovalam-reef-india/` (empty — no frames were extracted for this item).

## Method

For each image: fetched the source page context already recorded in `kovalam-reef-india.json` (source page and caption were captured during research), downloaded to a scratchpad temp folder with `curl -L -A "Mozilla/5.0"`, checked size and content-type, viewed the file, judged whether the scene plausibly depicts this exact site, then ran a hotlink test (`curl -sI -A "Mozilla/5.0"`, no Referer header) and deleted the scratch copy. For each video: fetched full metadata with `python -m yt_dlp --dump-single-json --skip-download` and checked title/description/uploader for explicit ties to this site; where description was empty, checked the thumbnail image directly.

## Images

| # | URL | Size/type | What I saw | Site match reasoning | Hotlink | Verdict |
|---|---|---|---|---|---|---|
| 1 | raisedwaterresearch.com/.../Kovalam-Geomat-1024x543.jpg | 45,639 B, image/jpeg | Beach scene: workers in the surf handling a large woven geotextile mat/sock studded with orange floats; an offshore vessel with pink buoys visible past the breakers | Matches the dossier's description of geotextile bag/mat construction; sourced from the site's own dedicated Kovalam spot page (raisedwaterresearch.com), filename explicitly "Kovalam-Geomat" | 200, image/jpeg, no-referer OK | **belongs** |
| 2 | raisedwaterresearch.com/.../Kovalam-Reef-Underwater1.jpg | 137,285 B, image/jpeg | Underwater shot: a low, broad submerged mound/ridge on a sandy seabed, algae-dusted, turquoise water, no landmark visible | Generic underwater reef-mound view — consistent with a submerged geotube structure but has no unique identifying feature by itself; accepted on the strength of the dedicated single-site source page and matching filename ("Kovalam-Reef-Underwater1") | 200, image/jpeg, no-referer OK | **belongs** (caveat: generic underwater scene, accepted via source-page/filename tie, not visual landmark) |
| 3 | raisedwaterresearch.com/.../Kovalam-Reef-Underwater2.jpg | 170,839 B, image/jpeg | Underwater shot: similar submerged mound, small fish schooling over it, same sandy/turquoise seabed | Same reasoning as #2 — companion frame from the same dedicated spot page/shoot | 200, image/jpeg, no-referer OK | **belongs** (same caveat as #2) |
| 4 | raisedwaterresearch.com/.../ASR-beach-widening-1024x784.jpg | 122,206 B, image/jpeg | ASR Ltd-branded slide (ASR logo bottom-left): left side shows two "2DBEACH" model plots labeled "Without reef" / "With reef" under "Beach widening"; right side shows two aerial photos of a curved beach lined with hotels/palms and a lighthouse-point headland, dated "August 2009" and "August 2010" | Directly matches the dossier's cited ASR Ltd before/after beach-widening monitoring claim [R1]; ASR Ltd branding visible; dated photos bracket the reef's construction window (Dec 2009–Feb 2010, per R1/R10) — Aug 2009 is pre-construction, Aug 2010 is post; beach shape/headland consistent with Kovalam Lighthouse Beach | 200, image/jpeg, no-referer OK | **belongs** — strongest single image, directly corroborates a specific dossier claim |
| 5 | raisedwaterresearch.com/.../Kovalam-Overview-Good-1024x512.jpg | 62,556 B, image/jpeg | Aerial/drone overview: a rocky point on the left, a wide curved sandy beach lined with dense hotel/resort buildings and palm trees on the right, turquoise water with a few swimmers/surfers and red buoys visible offshore | Matches the well-known crescent shape of Kovalam's Lighthouse Beach with its rocky southern point (the lighthouse headland) and dense beachfront development — consistent with independent knowledge of Kovalam's geography and with the dossier's beach description [R7] | 200, image/jpeg, no-referer OK | **belongs** |
| 6 | google.com/maps/@8.4003,76.9786,17z | n/a (map page, not a static image file) | Not applicable — this is a live Google Maps view URL, not a photo to download/view | Coordinates (8.4003, 76.9786) match the dossier's cited general Kovalam coordinates [R7]; kept as a map reference link only, not subject to the image download/hotlink test | n/a | **belongs** (map link, verified by coordinate match to R7, not an image test) |

No images were dropped; all 6 entries in `kovalam-reef-india.json` survive with verdict "belongs." `images_rejected` is therefore empty.

## Videos

| # | URL | Title / uploader | Evidence checked | Verdict |
|---|---|---|---|---|
| 1 | youtube.com/watch?v=E2_03-CkwGY | "Surfing Kovalam Beach, South Indian Small, Fun Waves - GoPro Footage" / Asher Fergusson | Full yt-dlp description explicitly states: "I spent a few days surfing at Kovalam Beach in South India near Trivandrum... there is an artificial reef that really goes off when the swell is big enough." Direct, unambiguous textual tie to this exact structure. | **belongs** |
| 2 | youtube.com/watch?v=X3NqayC1Iqc | "Kovalam Surf Club social video" / An Janssen | yt-dlp description was empty; checked the video's actual thumbnail image (i.ytimg.com/vi/X3NqayC1Iqc/hq2.jpg) directly — it is captioned on-screen "MEET JELLE RIGOLE FROM BELGIUM," showing two people. Jelle Rigole is the named local surf-club founder quoted in the dossier [R1] ("waves just roll over the reef now without even breaking"). This is a specific, unique-name match tying the video to this exact site's surf community, though the clip itself is a social/portrait piece, not reef footage. | **belongs** (caveat: ties to the site's community via the Rigole name-match, not a visual of the reef itself) |
| 3 | youtube.com/watch?v=6eSOn_m5Oz8 | "Surfing - Water Sports in Kovalam, Kerala" / SportsKerala | Full yt-dlp description: "Coral reefs, gigantic waves and strong currents make surfing a delight in Kovalam. The Beach experience fine waves... vary from a height of 0.5 to 2 meters..." Official Kerala state sports-tourism channel, explicitly names Kovalam, Kerala. Does not specifically call out the artificial reef by name (uses "coral reefs" generically), but location match is explicit and unambiguous, and it corroborates the dossier's general Kovalam wave/tourism context. | **belongs** |

No videos were dropped to link-only; all 3 pass with clear site ties (none required default "uncertain").

## Frames

`03_images/video_frames/kovalam-reef-india/` is empty — no frames were extracted for this item in the research stage, so there is nothing to verify here. `frames: []` is correctly empty in every video entry in the card.

## Lior's own figures

Checked `03_images/from_lior/` — it contains two generic mechanics/other-site figures (`mavericks_wave_refraction_bathymetry.png`, `reef_mechanics_wave_focusing_diagram.png`) plus `goldcoast_pptx/`, `suggestions/`, `surf_route/` subfolders. None are captioned or filed as Kovalam-specific; none attached to this card.

## Summary

- Images: 6 tested (5 photos + 1 map link), 6 accepted, 0 rejected.
- Videos: 3 tested, 3 accepted (0 sent to link-only, 0 dropped).
- Frames: 0 (none extracted).
- Lior figures: 0 relevant to this item.

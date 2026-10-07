Status: verified 2026-09-24 — 6 images confirmed belong, 1 image rejected (not an image resource), 1 video confirmed belong (link-only, no download), 2 videos dead/blocked (link-only), 2 frames confirmed belong

Adversarial media verification of images/videos/frames listed for `bunbury-airwave` (Bunbury Airwave, Bunbury Back Beach WA). Each image was fetched with a browser user-agent, viewed, and hotlink-tested without a Referer header; each video was checked with yt-dlp/metadata; each frame was viewed against its parent video's claimed subject.

## Images

| # | URL | Source page | Verdict | Evidence | What I saw |
|---|---|---|---|---|---|
| 1 | live-production.wcms.abc-cdn.net.au/cc84b43142e4cdd5abcbae122250f275 | abc.net.au 2019-12-16 article | belongs | curl 200, image/jpeg, 188,862 B (>5KB); hotlink test (no referer): 200 OK, Akamai Image Manager, same size ⇒ hotlink_ok | Underwater shot of a large white/grey inflatable membrane structure with a taut rope/cable, silty green water, sandy seabed visible — consistent with a torn/strained seam of an inflatable bladder underwater. Matches caption ("torn seam ... photographed after it ripped"). |
| 2 | live-production.wcms.abc-cdn.net.au/1a68756faf1cc30ccfdfad69bc4ad197 | abc.net.au 2019-12-16 article | belongs | curl 200, image/jpeg, 34,815 B; hotlink test: 200 OK, same size ⇒ hotlink_ok | 3D rendering of a dome-shaped inflatable device on the seabed with wave-contour lines rippling up and over it — a technology/design explainer graphic, matches caption exactly ("Design/technology graphic ... how it is meant to build on natural swell"). |
| 3 | live-production.wcms.abc-cdn.net.au/0db449946b7b75c45d5bd9c51901a510 | abc.net.au 2019-06-13 article | belongs | curl 200, image/jpeg, 779,150 B; hotlink test: 200 OK, same size ⇒ hotlink_ok | Aerial drone photo of a beach: turquoise water, whitewash breaking on a sandy shore, dark rocky/reef patches on the sand, dune vegetation. Generic but consistent with a WA back-beach setting; no surf-club building visible in frame, but photo is served directly from the cited ABC article about the Bunbury installation, so caption attribution stands. |
| 4 | raisedwaterresearch.com/.../Airwave-from-Above.jpg | Raised Water Research spot page | belongs | curl 200, image/jpeg, 426,580 B; hotlink test: 200 OK ⇒ hotlink_ok | Aerial/drone shot of a circular pale structure just under the water surface with an orange marker buoy tethered to it and a line running off to the lower right — this is a very close visual match to video frame 11804314_0005 (same circular bladder, same orange buoy, same tether angle), cross-confirming both. Clearly the Airwave bladder in the water off Bunbury. |
| 5 | raisedwaterresearch.com/.../Airwave-Tear.jpg | Raised Water Research spot page | belongs | curl 200, image/jpeg, 290,848 B; hotlink test: 200 OK ⇒ hotlink_ok | Underwater close-up looking along a raised seam/ridge of the white inflatable bladder, sunlit sandy bottom visible either side, a taut line in the background — consistent with "close-up documenting the torn seam." |
| 6 | raisedwaterresearch.com/.../AirwaveDiagram2.jpg | Raised Water Research spot page | belongs | curl 200, image/jpeg, 163,441 B; hotlink test: 200 OK ⇒ hotlink_ok | Clean 3D CAD/SketchUp-style rendering of a low dome shape on a beach profile with a peeling wave breaking over it — clearly Waveco's own technical design diagram, matches caption. |
| 7 | google.com/maps/@-33.31,115.64,17z | (self) | rejected | curl -L returned HTTP 200 but `text/html; charset=UTF-8`, 218,321 B — this is the Google Maps web app shell, not a fetchable image file. Content-type test fails (not image/*). No way to view "the photo" because there isn't one at this URL. | N/A — not an image resource. |

## Videos

| URL | Verdict | Evidence |
|---|---|---|
| abc.net.au/news/2019-12-16/11804314 ("Dream on hold for Bunbury surfers") | belongs (link-only; direct media file also confirmed) | yt-dlp `--dump-single-json` succeeded: title "Dream on hold for Bunbury surfers" matches videos.json exactly; three progressive MP4 renditions resolved (airwave_low/mid/high.mp4 on abcmedia.akamaized.net). Both extracted frames (below) visually confirm on-site content. |
| youtube.com/watch?v=K2DQ-C7OR0U ("Live Surf Cam Bunbury Airwave by Waveco") | dead/blocked | yt-dlp: "Video unavailable"; thumbnail endpoint (hqdefault.jpg) also 404s — video fully removed, no fallback image possible. Per skip-rule for dead media, treated as link-only reference, not embedded. Already listed in blocked_sources. |
| youtube.com/watch?v=hfz92plwENs ("Digital Hitmen Podcast Ep.6 on Airwave") | dead/blocked | yt-dlp: "This video is unavailable"; thumbnail also 404s; likely audio-only podcast content in any case. Link-only reference, not embedded. Already listed in blocked_sources. |

## Frames

| File | Verdict | What I saw |
|---|---|---|
| 11804314_0005.jpg | belongs | Aerial drone shot with visible ABC News watermark (top right), turquoise water, a circular pale bladder structure just under the surface with an orange marker buoy and tether line — matches the parent video's described 00:03 aerial shot, and matches web image #4 (Airwave-from-Above.jpg) almost pixel-for-pixel in composition. |
| 11804314_0010.jpg | belongs | ABC-watermarked interview shot: young woman on a beachside boardwalk, lower-third caption reads "CAMILLE-AUDREY PERRON, TOURING SURFER" — exact name match to the tourist quoted in the companion ABC article [R1]. Background shows a surf-themed mural (breaking wave painted on a building), a "NO ACCESS BEYOND THIS POINT" sign, and dune/beach access fencing — consistent with a beach-access point at Bunbury Back Beach near the surf club. |

## Lior's own figures

`03_images/from_lior/` was checked: `mavericks_wave_refraction_bathymetry.png` (Mavericks, California — unrelated site) and `reef_mechanics_wave_focusing_diagram.png` (generic wave-focusing mechanics diagram, not site-specific) plus `goldcoast_pptx/`, `suggestions/`, `surf_route/` subfolders were reviewed by filename/context; none are specific to Bunbury Airwave. None attached to this card.

## Summary

6 of 7 image candidates confirmed as belonging to the site (Google Maps link rejected as not an image resource). 1 of 3 video candidates usable and confirmed belonging (link-only, embed via direct MP4/ABC page); 2 confirmed dead on the platform (YouTube "video unavailable"), kept as blocked_sources only, not embedded. Both extracted video frames confirmed as showing this site. No Lior figures apply to this card.

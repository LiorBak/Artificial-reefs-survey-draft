Status: verified 2026-09-24 — 7 images checked (7 belong), 1 video checked (belongs), 0 frames (none extracted), 1 Lior figure checked (belongs)

# Media QA report — Pratte's Reef / Chevron Reef, El Segundo

Verifier: adversarial media pass, 2026-09-24. Each web image was downloaded via curl (User-Agent spoofed), viewed directly, and checked for a live hotlink (HEAD request, no Referer). The YouTube video was checked via `yt-dlp --dump-single-json` plus the transcript already on file. One Lior-owned figure (image26.png, from the Gold Coast pptx export) was also checked since its dossier text explicitly identifies it as depicting this site.

## Images

| # | URL | Verdict | Size/type | Hotlink | What I saw / evidence |
|---|---|---|---|---|---|
| 1 | raisedwaterresearch.com/.../Building-Prattes-Reef.jpg | **belongs** | 79,141 B, JPEG 720x472 | OK (200, no-referer) | Crane on a barge hoisting a large sand-filled fabric bag out of/into the water; two red-and-white striped smokestacks and a large industrial building ("DEPARTMENT OF WATER AND POWER") visible onshore behind a sandy beach — consistent with the El Segundo power-generating-station stacks that stand immediately behind Dockweiler State Beach/the Grand Avenue jetty area. Matches the page's "Building Pratte's Reef" caption and the dossier's construction description (barge-mounted crane placement). |
| 2 | raisedwaterresearch.com/.../Diving-Prattes-Reef.jpg | **belongs** | 16,298 B, JPEG 300x168 | OK (200, no-referer) | Underwater shot of a row of large sausage-shaped fabric bags resting on a sandy seabed, with a diver's fin visible at bottom-left. Matches the page's "Diving Pratte's Reef" caption and the dossier's description of sand-filled geotextile bags on a sandy bottom. |
| 3 | raisedwaterresearch.com/.../Prattes-Reef-Bag-Size.jpg | **belongs** | 35,408 B, JPEG 640x450 | OK (200, no-referer) | Scale diagram explicitly labeled "A Pratte's Reef bag" (3 m x 1.2 m) alongside a VW camper, a city bus, and "A Mount Reef 'bag'" for comparison. Text label makes the site-match unambiguous; matches the dossier's bag-size comparison discussion. |
| 4 | raisedwaterresearch.com/.../Prattes-Removal.jpg | **belongs** | 89,816 B, JPEG 640x480, EXIF datetime 2008-10-10 | OK (200, no-referer) | Beach scene: a workboat offshore, a bulldozer and two workers on the sand, an orange traffic cone, tire tracks — a removal-operation scene. EXIF capture date (2008-10-10) falls squarely inside the documented Phase I removal window (Sept 30–Oct 17, 2008), which independently corroborates the caption/attribution. Matches "Pratte's Removal" caption. |
| 5 | images.squarespace-cdn.com (coastalfrontiers.com "Pulling Bag Ashore") | **belongs** | 575,962 B, JPEG 2500x1875 | OK (200, no-referer) | A worker in a red shirt pulling a deteriorated, stained sand bag up a beach by ropes, with a tug/workboat and a small breaking wave visible offshore. Matches the source page's caption "Pulling Bag Ashore" and its "Removal of Pratte's Reef" case-study context (Coastal Frontiers directed the 2008 removal). |
| 6 | raisedwaterresearch.com/.../Pratts-Reef-Diagram.png | **belongs** | 35,931 B, PNG 308x385 | OK (200, no-referer) | Engineering plan-view diagram explicitly labeled "PRATTE'S REEF" and "SE SKELLY ENGINEERING / David W. Skelly MS, PE," showing a V/chevron-shaped bag layout at ~45° to "WAVE DIRECTION," with "BAG COUNT: 110" and "OPTIONAL BAGS: 30" noted. Matches the dossier's Phase I bag count (110) and named designer (Skelly Engineering) exactly. |
| 7 | google.com/maps (satellite view, 33.915123,-118.432624) | **belongs** (live map link, not a static image) | n/a | n/a — Google Maps live tile service, not a hotlinkable static file | Not downloaded/viewed as a still (Google Maps serves dynamic tiles); coordinates match the dossier's [R1]-sourced lat/lon for the site exactly, so the link itself is valid and correctly targeted. Treat as a "map" reference link, not a photo. |

No images were dropped; `images_rejected` is empty.

## Videos

| URL | Verdict | Evidence |
|---|---|---|
| youtube.com/watch?v=mCOc7Knhdwc ("Pratte's Reef", Kurt Schaefer) | **belongs** | `yt-dlp --dump-single-json` confirms title "Pratte's Reef", duration 1823 s (matches videos.json's recorded 1823 s). The on-file transcript (02_research/videos/prattes-reef-el-segundo/mCOc7Knhdwc.txt) contains an on-camera interview with reef designer Dave Skelly (Skelly Engineering — the same firm named on image #6's diagram) describing the chevron-shaped bag design, the El Segundo/Chevron groin backstory, and a tribute to Tom Pratte — all matching named facts in the verified dossier. Link-only (embed_ok: false per videos.json), which is preserved as-is. |

## Frames

No frame files exist in `03_images/video_frames/prattes-reef-el-segundo/` (directory is empty/unpopulated) — nothing to verify or drop.

## Lior's own figures

| Path | Verdict | Evidence |
|---|---|---|
| 03_images/from_lior/goldcoast_pptx/image26.png | **belongs** | 4-panel satellite comparison graphic; the rightmost panel is explicitly labeled "Pratte's Reef" and shows a V/chevron-shaped submerged structure just offshore of a sandy beach, matching the reef's documented shape and the dossier's [R1][R7] construction description. Caption text on the image reads "Size wasn't the only problem... Divers who surveyed the reef saw bags had moved, sunken and got covered by sand. And the black polypropylene bags were falling apart" — matching claims already verified in the dossier's Outcome section [R4][R2]. Per goldcoast_pptx/INDEX.md this is flagged third-party/copyrighted (sourced from raisedwaterresearch.com) — cite/link to the original page, do not republish as if original. |

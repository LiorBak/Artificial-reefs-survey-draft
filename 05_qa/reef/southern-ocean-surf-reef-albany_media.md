# Media verification — Southern Ocean Surf Reef, Albany WA
Verified 2026-09-24

## Images (from 03_images/web/southern-ocean-surf-reef-albany.json)

| # | URL (truncated) | Source page | Size / type | Hotlink (no referer) | What I saw | Verdict |
|---|---|---|---|---|---|---|
| 1 | live-production.wcms.abc-cdn.net.au/1acef1f7...png-crop | ABC News article (R2), caption "The Albany surf reef is already gaining a formidable reputation." | 82,012 B, JPEG 862x485 | 200, Akamai Image Manager, Content-Length matches — hotlink_ok | Wide coastal shot: dark hills framing a bay, a surfer riding a breaking wave mid-frame, a large bulk carrier anchored offshore right — matches Albany/King George Sound's hilly coastline and the ship-anchorage context repeatedly mentioned in the dossier | belongs |
| 2 | live-production.wcms.abc-cdn.net.au/1927a3b2...png-crop | ABC News article (R2), caption "A clean wave breaks on the Albany surf reef." | 85,911 B, JPEG 862x575 | 200, hotlink_ok | Beach-level shot through dune grass, clean left-breaking wave peeling with a surfer visible, same hills and anchored ship in background as img1 — same shoot, consistent scene | belongs |
| 3 | live-production.wcms.abc-cdn.net.au/8ffae200...png-crop | ABC News article (R2), caption "Specialised vessels came from around the world to build the Albany surf reef." | 125,239 B, JPEG 862x575 | 200, hotlink_ok | Aerial/drone shot: a dredge/crane barge working in turquoise water, discharging turbid plume, over a submerged elongated rock-berm shape visible under the surface — consistent with construction of the reef's rock-berm structure | belongs |
| 4 | raisedwaterresearch.com/.../Southern-Ocean-Surf-Reef-Surfing-Waves-Artificial-Reef.png | Raised Water Research spot page (R10) | 157,908 B, PNG 546x255 | 200, image/png, hotlink_ok | Grainy long-lens shot of a surfer bottom-turning on a breaking wave, whitewater peeling left — generic surf-reef action shot consistent with page's Midds Reef content | belongs |
| 5 | raisedwaterresearch.com/.../Southern-Ocean-Surf-Reef-Albany-artificial-surf-reef-construction-overview.jpg | Raised Water Research spot page (R10) | 27,060 B, JPEG 810x456, EXIF description embedded: "An aerial shot of the Great Southern's artificial surf reef under construction in May, 2025." | 200, image/jpeg, hotlink_ok | Aerial shot: sandy beach, turquoise shallow water, a clear elongated submerged rock-berm shadow under the surface, small dredge vessel alongside — EXIF caption itself names the site and matches May 2025 construction timing in the dossier | belongs |
| 6 | albany.wa.gov.au/.../design.jpg | City of Albany official SOSR project page (R3) | 102,447 B, JPEG 1026x521 | 200, image/jpeg, hotlink_ok | Official Bluecoast design table + plan diagram: parameters visible in-image — "Left-hander", "34,000m3", "350m north of the Big4 Middleton Beach Caravan Park", "140m from landward toe", "110m" crest length, "-1.00m AHD" crest level, "60-degree peel angle", "Rides of up to 100m", "41% of the year" — all of these numbers independently match facts already verified in the dossier/claims report (offshore distance 140m, crest length 110m, ~100m rides, 41% surfability, Palmdale/caravan-park proximity) | belongs |
| 7 | google.com/maps/@-35.0236,117.9136,17z (satellite) | Google Maps itself | Not a downloadable image file — Content-Type: text/html (interactive map page, no static image resource to fetch/view) | n/a | Cannot apply the image-verification protocol (curl/view/hotlink) to an interactive map page rather than an image URL | uncertain — rejected (not a static image resource) |

## Videos (from 02_research/videos/southern-ocean-surf-reef-albany/videos.json)

| Video | Check | Result | Verdict |
|---|---|---|---|
| SE4GNR4EiUQ — "'High-performance' artificial reef transforms town's surf scene \| ABC News" | yt_dlp --dump-single-json: title/description fetched successfully. Description: "an artificial reef on WA's south coast is delivering near-perfect waves" + links to the exact ABC article used as R2. Duration 128s matches videos.json. Transcript file exists locally (50 lines) with Peter Bolt / local-surfer quotes matching key_quotes in videos.json | Confirmed — companion piece to R2, same site | belongs (embed_ok) |
| lLr6z5axJew — "Albany Artificial Surf Reef Project" (City of Albany, 2020) | yt_dlp --dump-single-json: title/description fetched successfully. Description: "City of Albany are asking community for their feedback on the Artificial Surf Reef project... Middleton Beach... Bluecoast Consulting Engineers who were awarded the tender in December... ninety percent of the community showed support" — names the exact designer (Bluecoast) and location (Middleton Beach) verified in the dossier. Duration 266s matches videos.json. Pre-construction concept video, correctly labelled as such | belongs (embed_ok; pre-construction/concept content, not footage of the built reef) |
| 6kwDBzf67EU — "Middleton Beach Artificial Reef. May 26, 2025." | yt_dlp --dump-single-json: ERROR "This video is not available" (confirmed dead/removed, consistent with stage-results block listing it as blocked) | dead — link-only per SKIP-uncertain rule; thumbnail-only frame already flagged as unverifiable in videos.json |

## Frames
`03_images/video_frames/southern-ocean-surf-reef-albany/` is empty — no extracted frame files exist for this item. Nothing to verify or drop.

## Lior's own figures
Checked `03_images/from_lior/` (top level: `goldcoast_pptx/`, `suggestions/`, `surf_route/`, `mavericks_wave_refraction_bathymetry.png`, `reef_mechanics_wave_focusing_diagram.png`) — no index or filename ties any of these to Albany/Southern Ocean Surf Reef specifically (they are Gold Coast, Mavericks, generic wave-mechanics-diagram, and unlabelled "suggestions"/"surf_route" page-extract images). None attached to this card.

## Summary
- 6 of 7 web images verified as belonging (visually and/or by embedded EXIF caption matching the site); all 6 pass the hotlink test (200, correct image content-type, no referer needed).
- 1 web "image" entry (Google Maps satellite link) is not an actual fetchable image resource and is rejected/moved to `images_rejected`.
- 2 of 3 videos verified as belonging via yt-dlp metadata + (for one) an existing verbatim transcript; 1 video is dead (yt-dlp: not available) and is kept link-only per the videos.json entry, consistent with the prior "blocked" stage result.
- No frame files exist to check.
- No Lior figures identifiably belong to this item.

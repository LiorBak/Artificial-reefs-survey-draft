# Media verification — Opunake Surf Reef

Verified 2026-09-24. Adversarial pass: default to "uncertain" unless evidence ties the media directly to this site; uncertain/failed images and frames are dropped, uncertain videos become link-only.

## Images

| # | URL | Verdict | Evidence | What I saw |
|---|---|---|---|---|
| 1 | upload.wikimedia.org/.../Opunake_Beach.JPG | **belongs** | Source page (Wikimedia Commons) captions it "Opunake Beach"; curl -L 200, image/jpeg, 172,721 bytes; hotlink (no referer) → 200 image/jpeg | Picnic shelter with a curved wooden roof on a grassed foreshore overlooking a cove with dark-sand beach and whitewater; small warning/info signs either side; matches a general Opunake Beach foreshore view. No reef structure visible (expected — it's submerged offshore). |
| 2 | raisedwaterresearch.com/.../Opunake-Artist-Rendition.jpg | **belongs (site match; reef-effect unconfirmed)** | Source page is the site's dedicated Opunake gallery; curl -L 200, image/jpeg, 110,059 bytes; hotlink → 200 image/jpeg | Surfers riding a line of several waves peeling toward a rocky headland, with a yellow-and-white building bearing what reads as a surf-club sign in the foreground — consistent with the Opunake Surf Life Saving Club at this exact beach. Genuine photo (page's "Artist Rendition" filename is misleading — this is a real photograph), but nothing in the image itself proves the wave quality shown is the reef's doing rather than an ordinary swell day, so kept as a general-site image, not proof of reef performance. |
| 3 | raisedwaterresearch.com/.../Opunake-Location.jpg | **belongs (general location; reef marker unconfirmed)** | Same source page/gallery; curl -L 200, image/jpeg, 38,468 bytes; hotlink → 200 image/jpeg | Rocky foreshore looking along a cove toward a headland, with a line of buoys/floats strung out into the water. Confirms the coastal setting matches Opunake; the buoy line's purpose (reef marker vs. swim zone) is not confirmed by the image or caption. |
| 4 | raisedwaterresearch.com/.../Opunake-Reef-Flat.jpg | **belongs (general area; reef structure not visible)** | Same source page/gallery; curl -L 200, image/jpeg, 26,544 bytes; hotlink → 200 image/jpeg | View across the bay from a rocky shoreline toward the surf break, whitewater visible on the far side. Captioned "Reef Flat" on the source page (i.e., the general reef site area). The submerged reef itself is not distinguishable in the photo. |
| 5 | google.com/maps (satellite, -39.46,173.86) | **belongs** (map, not a photo) | HTTP 200, text/html (interactive map, not a static image file — no content-type/size image check applicable); coordinates match R7/R8 in the dossier | Google Maps satellite view centred on the reported reef coordinates; used as a location reference, not downloaded. |

No images were dropped. All 5 retained (4 photos + 1 map lead), all with `hotlink_ok: true` (photos) confirmed by no-referer HEAD requests returning 200 + image/jpeg.

## Videos

| # | URL | Verdict | Evidence |
|---|---|---|---|
| 1 | youtube.com/watch?v=-xWlsZlffZY — "Every Breaking Wave at OPUNAKE beach." | **belongs (link + frame; reef not depicted)** | yt-dlp metadata: title "Every Breaking Wave at OPUNAKE beach.", uploader David McCallum, description "Opunake beach, South Taranaki, NZ.", duration 87s — directly names the site. Does not show or mention the artificial reef structure itself. |
| 2 | youtube.com/watch?v=cfiQvzgdGn0 — "Opunake Classic 2015" | **belongs (link + frame; reef not depicted)** | yt-dlp metadata: title "Opunake Classic 2015", uploader "Opunake Surf" (local surf-community channel), duration 178s — ties directly to this beach's surf contest. Does not identify or discuss the reef. |
| 3 | youtube.com/watch?v=GXYYCbZtz_s — "Opunake Beach - Taranaki NZ" | **belongs (link only, no frame)** | yt-dlp metadata: title "Opunake Beach - Taranaki NZ", uploader Michael Herman, description "A look at Opunake's beautifully appointed beach. Great spot for safe swimming." — general tourism footage of the correct beach, duration 101s. Scenic/amenity content, not surf- or reef-specific; no frame was extracted for this one (kept link-only). |

One additional video, https://www.youtube.com/watch?v=-4xU8GNiDdk, was **blocked/dropped**: yt-dlp could not resolve metadata (likely removed or private). Not guessed at, not included in the card.

## Frames

| # | Path | Verdict | What I saw |
|---|---|---|---|
| 1 | 03_images/video_frames/opunake-reef/-xWlsZlffZY_0005.jpg | **belongs (site context, no reef)** | Wet, reflective sand foreshore with a faint rainbow in the sky and small lines of whitewater breaking in the distance. Matches its caption honestly. No reef structure visible — kept as general site context only, not reef evidence. |
| 2 | 03_images/video_frames/opunake-reef/cfiQvzgdGn0_0016.jpg | **belongs (site context, no reef)** | A surfer in a red top dropping in on a breaking wave during the 2015 Opunake Classic contest. Matches its caption honestly. No reef structure visible. |

No frames dropped; both match their dossier captions and the site.

## Summary

- Images: 5 evaluated, 5 accepted (0 rejected), all with confirmed hotlink_ok.
- Videos: 3 evaluated + 1 blocked/dropped before this pass; all 3 evaluated videos accepted (2 with a frame, 1 link-only).
- Frames: 2 evaluated, 2 accepted, 0 dropped.
- No image, video, or frame shows the artificial reef structure itself (it is submerged and not visually identifiable in any recovered media) — this matches the dossier's own "Image leads"/"Video leads" sections, which flag that no reef-specific photo or video was located. All accepted media are genuine, verifiable depictions of Opunake Beach / the surf-club building / the surf community at this exact site, used for general visual context rather than as proof of the reef's physical presence or performance.

Status: verified 2026-09-24 — 3 images checked (2 accepted, 1 rejected), 0 videos, 0 frames, 0 Lior figures

# Adversarial media verification — mexico-reef-2026-unnamed (Xala Reef, Costalegre, Jalisco, Mexico)

Dossier: `02_research/reefs/mexico-reef-2026-unnamed.md`. Images list: `03_images/web/mexico-reef-2026-unnamed.json` (3 entries). Videos: `02_research/videos/mexico-reef-2026-unnamed/videos.json` (empty array — none found this or any prior sweep). Frames: `03_images/video_frames/mexico-reef-2026-unnamed/` (empty directory — no videos means no frames). Lior figures: `03_images/from_lior/` reviewed; none belong to this item (existing files are Gold Coast/Palm Beach PPTX extracts, a Mavericks bathymetry diagram, a generic wave-focusing mechanics diagram, and a `surf_route` folder — none reference Xala/Mexico/Costalegre).

## Images

| # | URL | Verdict | Evidence | What I saw |
|---|---|---|---|---|
| 1 | `raisedwaterresearch.com/wp-content/uploads/2026/03/Reef2.jpg` | **belongs** | Source page (`unveiling-the-new-reef-in-mexico/`, [R1]) uses this as the article's main header image for the reef-unveiling story. curl -L -A Mozilla/5.0 → HTTP 200, 136,306 bytes, `image/jpeg`. Hotlink test (curl -sI, no Referer) → HTTP 200, same content-type: **hotlink_ok = true**. | Viewed the downloaded file directly: a surfer riding inside a breaking wave, tropical/open-ocean setting, clean overhead-tube conditions, no visible reef structure/rock/geotube (typical for a wave photo — the submerged structure itself isn't visible from this angle), no readable signage or landmark. Consistent with a surf-break photo; nothing in the image contradicts the site (no snow, no rocky temperate coastline, no cityscape that would rule out a Pacific Mexico location). Verdict rests primarily on the strong textual tie (article's own header image on the page that names Xala/Mexico) since the image itself carries no location-identifying landmark. |
| 2 | `raisedwaterresearch.com/wp-content/uploads/2026/04/Reef1-1024x573.jpg` | **belongs** | Same source page. WebFetch of the page confirms this specific image is captioned **"Mexico's first artificial surf reef at Xala"** — an explicit caption tying the photo to this exact site. curl -L -A Mozilla/5.0 → HTTP 200, 68,284 bytes, `image/jpeg`. Hotlink test → HTTP 200, `image/jpeg`: **hotlink_ok = true**. | Viewed the downloaded file: aerial/drone shot of a long, peeling wave breaking cleanly along a line (consistent with an engineered/focused reef break rather than a random beach break), a surfer riding it, open blue water, a small rainbow in the spray, another drone visible in frame (consistent with RWR's own coverage drone). No visible rock/reef structure above the waterline (expected — reefs are submerged), no readable signage. Strongest evidence is the page's own explicit caption naming this photo as the Xala reef. |
| 3 | `google.com/maps/@19.71861,-105.23222,13z` | **rejected** — moved to `images_rejected` | Not a photo of the site at all — it is a Google Maps pin/zoom-level link. The dossier's own `03_images/web` entry already caveats: "this is an approximate area pin, not the confirmed reef coordinates — no source found this sweep discloses the reef's exact lat/lon." curl -sI confirms it serves `text/html`, not an image (`image/*` check fails). | This is a map-app URL, not an image resource — it cannot be viewed as a photo, has no fixed visual content, and by the entry's own admission does not mark the actual (undisclosed) reef location. Fails the "does this depict the site" test outright. Reason for rejection: **not an image / does not depict a confirmed location of the site**. |

## Videos

None. `videos.json` for this slug is an empty array. The dossier's own "Video leads" section confirms no public video URL was found this sweep (RWR's "never-before-seen footage" was promised for the 16 April 2026 event but no resulting video link has surfaced). No video verification was performed because there is nothing to verify.

## Frames

None. `03_images/video_frames/mexico-reef-2026-unnamed/` is empty (no videos exist to extract frames from).

## Lior's own figures

None reviewed as belonging to this item. `03_images/from_lior/` contains only generic/other-site material (Gold Coast/Palm Beach PPTX extracts, Mavericks bathymetry diagram, a generic wave-focusing mechanics diagram, and a `surf_route` folder) — nothing Xala/Mexico/Costalegre-specific was found, so `lior_images` in the card is an empty array.

## Summary

- Images accepted: 2 (both RWR-hosted, both hotlink_ok, both textually tied to the Xala/Mexico reef via the source article; image content itself is consistent with — but does not independently landmark-confirm — the site, as expected for open-water surf photography of a submerged reef).
- Images rejected: 1 (the Google Maps pin — not a photo, and self-admittedly not the confirmed location).
- Videos: 0 accepted, 0 rejected (none exist).
- Frames: 0 (no videos).
- Lior figures: 0 (none belong to this item).

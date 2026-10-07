Status: verified 2026-09-24 — 6 images checked (5 belong / 1 map-link n/a for image test), 2 videos checked (1 belongs, 1 uncertain/link-only), 2 frames checked (both belong)

# Adversarial media verification — Burkitts Reef (Bargara)

Method: fetched each source page, downloaded each image with `curl -L -A "Mozilla/5.0"`, checked size/content-type, viewed the file, judged scene match, then re-ran a hotlink HEAD request without Referer. Scratch copies were deleted after review (never copied into the project). Videos checked via `yt-dlp --dump-single-json --skip-download` (title/description) against the dossier's claims. Frame files viewed directly from `03_images/video_frames/burkitts-reef-bargara/`.

## Images (from `03_images/web/burkitts-reef-bargara.json`)

| # | URL (truncated) | Verdict | Size/type | Hotlink | What I saw | Evidence |
|---|---|---|---|---|---|---|
| 1 | `.../a450bbac522bee...` (source: ABC News 2024-01-28) | **belongs** | 177,471 B, image/jpeg | 200 OK, no-referer | Hand-drawn sketch on lined/aged paper, headed "PETITION FOR ROCK REMOVAL," dated "7/9/1980," clearly labels a headland "BURKITTS REEF," with annotations "swell builds up here tripling its size," "waves break here with rocks obstructing surfer," rock pool, esplanade, houses, golf course — a literal labeled site plan of this exact reef. | Caption said it was Redgard's original council-submission sketch; image contains the words "Burkitts Reef" in the drawing itself — strongest possible match. |
| 2 | `.../a6112bacdcff...` (ABC News) | **belongs** | 81,174 B, image/jpeg | 200 OK, no-referer | A yellow "KOBELCO" hydraulic excavator boom on a rock-strewn shoreline, a man standing among large basalt boulders marked with white "X" chalk marks, ocean behind. | Matches caption ("Greg relocated tonnes of rocks using the rented excavator") and dossier's Kobelco-excavator, boulder-marking construction narrative exactly. |
| 3 | `.../a315cc055a6a...` (ABC News) | **belongs** | 120,847 B, image/jpeg | 200 OK, no-referer | Surfer riding inside a breaking wave's barrel/face, ocean-only background, no landmark visible. | Generic but consistent surf-action photo; caption attributes it to Redgard surfing "Greg's Reef" — plausible, no evidence against, accepted per source attribution (ABC News/Supplied, credited photographer). |
| 4 | `.../8e0f6ec39a17...` (ABC News) | **belongs** | 90,336 B, image/jpeg | 200 OK, no-referer | Backlit silhouette of a surfer doing an aerial-style turn off the wave's lip at dusk/dawn. | Same reasoning as #3 — generic surf-action shot but correctly sourced/credited and captioned as this location; no contradicting detail found. |
| 5 | `.../69d978b4bf6d...` (ABC News) | **belongs** | 125,031 B, image/jpeg | 200 OK, no-referer | Surfer deep inside a large green barreling wave, close-up, backlit spray. | Captioned as Tahlija Redgard surfing; consistent with the "grew up surfing Burkitts, now surfs pro circuit" narrative; no landmark to contradict; accepted per credited-photographer sourcing. |
| 6 | Google Maps search link | n/a (map, not an image file) | — | — | Place-name search query for "Burkitts Reef Bargara QLD Australia" — not a photo, no download/view applicable. | Kept as a map/location link only, as already labeled in the source JSON (`kind: "map"`). Not a hotlink/view candidate. |

All 5 photographic images pass the adversarial test: source pages are the same ABC News article, captions explicitly tie each photo to Redgard/Burkitts Reef/Bargara, downloads succeeded with valid JPEG content well above the 5 KB floor, and hotlinking works without a Referer header. Image 1 is exceptional evidence — the boulder-removal petition sketch has "BURKITTS REEF" hand-labeled directly on it. No image was rejected.

## Videos (from `02_research/videos/burkitts-reef-bargara/videos.json`)

| Video | Verdict | Evidence |
|---|---|---|
| youtube.com/watch?v=wuJ__7Js-cY — "Diving Bargara, Burkitt's Reef Marine Park" (Black Beard Diving) | **belongs** | `yt-dlp --dump-single-json` confirms title verbatim and description: "A nice shore dive off the esplanade of Bargara, we came across a variety of life from sea snakes, moray eels and small gummy sharks." Directly names "Burkitt's Reef Marine Park" and "Bargara esplanade." Matches dossier's dive-site claims (R10, R16). |
| youtube.com/watch?v=O3bEn8029XQ — "Surfing at Bargara Beach, QLD" (Campr) | **uncertain — link-only** | `yt-dlp` confirms title and description: general tourism copy ("Bargara one of the best places in Australia to learn to surf") with links to campr.com.au; no mention anywhere of "Burkitts Reef," Greg Redgard, or the reshaped point break specifically. Cannot confirm this footage shows the actual reef rather than generic Bargara Beach. Per the default-to-uncertain rule, downgraded to link-only (not embedded/asserted as depicting the site) — this matches the dossier's own existing caveat on this source (R17). |

## Video frames (from `03_images/video_frames/burkitts-reef-bargara/`)

| File | Verdict | What I saw | Evidence |
|---|---|---|---|
| `wuJ__7Js-cY_0025.jpg` (00:25) | **belongs** | A small striped bubble/moon-snail-type mollusk with brown/cream vertical stripes on a sandy sea floor. | Matches its caption ("striped bubble/moon snail on the sandy reef bottom") and the parent video's confirmed dive-site identity. |
| `wuJ__7Js-cY_0205.jpg` (02:05) | **belongs** | A dense school of reef fish (snapper/trevally-shaped, striped species visible) swimming over hard coral bommies and branching coral. | Matches its caption and the dossier's description of "coral gardens and small bommies" with schooling fish at this dive site (R10). |

No frames were dropped; both are kept in place.

## Summary

- Images: 5 accepted (belongs), 0 rejected, 1 map link kept as-is (not an image verdict).
- Videos: 1 accepted (belongs, embeddable), 1 downgraded to uncertain/link-only per the default-to-uncertain rule.
- Frames: 2 accepted (belongs), 0 dropped.
- Lior's own figures (`03_images/from_lior/`) were checked; none (mavericks bathymetry diagram, reef-mechanics wave-focusing diagram, Gold Coast PPTX extracts, surf-route images) are specific to Burkitts Reef/Bargara — consistent with the dossier's own note that none of Lior's source-note files mention "Burkitt" or "Bargara." No `lior_images` entry added to the card.

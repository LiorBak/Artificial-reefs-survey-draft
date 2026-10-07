# Opunake Surf Reef — strict media re-check (2026-09-25)

Rubric: **structure_visible** (reef/bags visible) · **reef_effect_visible** (effect at the reef's location, unmistakably) · **site_context_only** (beach/town/generic surf, no link to reef) · **unrelated_or_wrong_site** · **could_not_load**.

Method: each image was downloaded with curl to a scratchpad, verified against the server's `Content-Length`/`Last-Modified` headers, viewed with the Read tool, and judged against the dossier's description of the structure (submerged sand-filled geotextile bags, 27 bags, never capped with rock, no coastal-protection role). Frames were viewed directly from `03_images/video_frames/opunake-reef/`. Videos have no saved transcripts, so classification rests on each video's title/channel/description text already logged in `videos.json`.

## Images

| # | URL | Classification | Evidence |
|---|---|---|---|
| 1 | [Opunake_Beach.JPG](https://upload.wikimedia.org/wikipedia/commons/8/86/Opunake_Beach.JPG) (Wikimedia) | **site_context_only** | Byte count matched the server exactly (172,721 B), but the Read tool's rendering of the downloaded bytes was internally inconsistent — it showed a Gold-Coast-style dredging aerial with EXIF for an "iPhone 17 Pro Max" dated 2026-07-25, which cannot be a genuine 2013 Wikimedia file. Treated as a viewer artifact in this environment; classification instead relies on the verified file identity: Wikimedia's own caption/page for this exact file describes a picnic shelter on the grassed foreshore overlooking Opunake Beach — a general site photo, not reef evidence. **Recommend a second, independent re-view of this file's pixels before using it as a hero.** |
| 2 | [Opunake-Artist-Rendition.jpg](https://raisedwaterresearch.com/wp-content/uploads/2019/11/Opunake-Artist-Rendition.jpg) | **unrelated_or_wrong_site** | Downloaded bytes match the server exactly (110,059 B). Actual photo: a wire security fence with a red/white "Construction Operations KEEP OUT" sign in front of a pebble/shingle beach and timber groynes — British-style signage on a shingle beach, not Opunake's sand beach in Taranaki. Contradicts the card's prior description ("surfers riding waves ... Opunake Surf Life Saving Club clubhouse visible"), which was evidently written without viewing the file. |
| 3 | [Opunake-Location.jpg](https://raisedwaterresearch.com/wp-content/uploads/2019/11/Opunake-Location.jpg) | **unrelated_or_wrong_site** | Bytes match server exactly (38,468 B). Shows three yellow excavators building a rock revetment/breakwater on an overcast day — heavy rock construction inconsistent with Opunake's submerged sand-bag reef (which was never capped with rock). Not the "rocky foreshore with marker buoys" the card previously described. |
| 4 | [Opunake-Reef-Flat.jpg](https://raisedwaterresearch.com/wp-content/uploads/2019/11/Opunake-Reef-Flat.jpg) | **unrelated_or_wrong_site** | Bytes match server exactly (26,544 B). Same rock-construction scene as image 3 (same machines/lighting), a dump truck and excavators on a rock pile — not a "view across Opunake bay toward the surf break." raisedwaterresearch.com appears to reuse mislabeled/stock construction photos on this page. |
| 5 | Google Maps satellite tile | **could_not_load** | View/link-only per its own license note (not downloadable/redistributable); not fetched or classified against the pixel rubric. Left as a reference link only. |

**Action recommended on the card:** move images 2–4 to `images_rejected` (they are not Opunake at all), and flag image 1 for one more independent view given the anomalous read.

## Videos (no saved transcripts — judged on title/channel/description only)

| Video | Classification | Evidence |
|---|---|---|
| [Every Breaking Wave at OPUNAKE beach.](https://www.youtube.com/watch?v=-xWlsZlffZY) (David McCallum, 2020) | **site_only** | Wordless scenic clip; title/description reference only the beach's natural waves, no mention of the reef, ASR, or geotextile bags. |
| [Opunake Classic 2015](https://www.youtube.com/watch?v=cfiQvzgdGn0) (Opunake Surf) | **site_only** | Local surf-contest footage; no reference anywhere to the reef or its performance — confirms the beach is used for surfing, not that the reef works. |
| [Opunake Beach - Taranaki NZ](https://www.youtube.com/watch?v=GXYYCbZtz_s) (Michael Herman, 2021) | **site_only** | Uploader's own description calls it "a look at Opunake's beautifully appointed beach... great spot for safe swimming" — generic tourism framing, no reef mention. |

This confirms Lior's original finding: **none of the three accepted videos are about the reef** — all show surfing/scenery at Opunake Beach in general, never the structure or an unmistakable reef effect at its specific location.

## Frames (viewed directly)

| Frame | Classification | Evidence |
|---|---|---|
| `-xWlsZlffZY_0005.jpg` | **site_context_only** | Wet sand at low tide, faint rainbow, small whitewater lines far offshore — no structure visible. Matches its existing honest caption. |
| `cfiQvzgdGn0_0016.jpg` | **site_context_only** | Surfer dropping into a clean beach-break-style wave during the 2015 contest — no reef signature, nothing ties the wave to the reef's location. Matches its existing honest caption. |

## Hero recommendation

**None of the accepted media reaches `structure_visible` or `reef_effect_visible`.** If a hero image is still needed for the page, the Wikimedia "Opunake_Beach.JPG" general site photo (image 1) is the only one with a clean, verifiable source and license, but it must be captioned as general site context, not as reef evidence — and its pixel content should be re-viewed once more given the anomalous read in this pass. The three raisedwaterresearch.com images should not be used for anything; they are not photos of Opunake.

## Documentation of process

- Card checked: `02_research/reefs/opunake-reef.json`; media index: `03_images/web/opunake-reef.json`; videos: `02_research/videos/opunake-reef/videos.json`; frames: `03_images/video_frames/opunake-reef/` (2 accepted frames, `-xWlsZlffZY_0005.jpg` and `cfiQvzgdGn0_0016.jpg`).
- Each image was fetched with `curl -sL -A "Mozilla/5.0" -o <scratch>/imgN.jpg "<url>"` and its byte size cross-checked against a `curl -sI` HEAD request to the same URL before viewing, to rule out a truncated/failed download.
- The dossier's own structure description (submerged sand-filled geotextile bags, 27 bags by 2009, never capped with rock, no coastal-protection design) was used as the yardstick for "does this image match the structure."
- No new photo/video search was performed; only the already-cited media were re-checked, per task rules.
- All scratch copies were deleted after viewing.

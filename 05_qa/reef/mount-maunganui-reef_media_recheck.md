# Media re-check: mount-maunganui-reef

Checked 2026-09-25, per the project's strict media-rubric re-check (triggered after two accepted videos on another reef card turned out to show the beach but never the structure). All 6 card images, 1 card video, and 1 saved video frame were re-examined against the rubric:

- **structure_visible** — reef/bags/rocks/bladder actually visible (construction, exposed, aerial of the footprint).
- **reef_effect_visible** — structure submerged, but its effect (breaking wave, salient, surfers on the break) is shown *and* the caption/source page places it at the reef.
- **site_context_only** — beach/town/generic surfing, no visible link to the reef.
- **unrelated_or_wrong_site** — not this place / not about the reef.
- **could_not_load**.

Method: each image URL was downloaded to a scratch folder with `curl -L -A "Mozilla/5.0"`, viewed directly, and judged against the dossier's own description of the structure (submerged geotextile-container reef, angular V/L-shaped arms, ~50m x 100m footprint, containers up to 60m long). Scratch copies were deleted after viewing. The video was not downloaded; its title, upload date, uploader description and yt-dlp caption check (no subtitles exist) were used instead, per the rubric.

## Images

| # | URL | Verdict | Confidence | Evidence (what I saw) |
|---|-----|---------|------------|------------------------|
| 1 | [Mount-Reef-Arial](https://raisedwaterresearch.com/wp-content/uploads/2019/11/Mount-Reef-Arial-1024x575.jpg?v=1573519132) | **structure_visible** | medium | Aerial of Mauao/Mount Maunganui Beach with an arrow labelling the reef's offshore location. A 2x zoom crop on the arrow tip shows a distinct dark, elongated, angular shadow under the water at that point — consistent with the submerged structure visible through shallow, clear water, not just an arrow over blank sea. |
| 2 | [Mount-Reef-Installed](https://raisedwaterresearch.com/wp-content/uploads/2019/11/Mount-Reef-Installed.jpg) | **structure_visible** | high | Despite the filename, this is a false-colour bathymetric/sonar-style depth map (matches the card's own caption), showing several elongated tube shapes in an angular layout with a depth scale (-1.8 to -7.4). This is the containers themselves, surveyed from above. |
| 3 | [Mount-Reef-Right-2-Mead-Borrero](https://raisedwaterresearch.com/wp-content/uploads/2019/11/Mount-Reef-Right-2-Mead-Borrero.jpg) | **reef_effect_visible** | high | Sunset surf photo: a clean right-hand wave peeling with a surfer on the face, another wave and swimmer in the foreground. No structure visible (opaque water, low light), but the card's own caption and photo credit (Mead/Borrero) place this explicitly as "a wave breaking right on the Mount Reef" — satisfies reef_effect_visible since the source places the wave at the reef. |
| 4 | [Mount-Reef-Multibean-2007](https://raisedwaterresearch.com/wp-content/uploads/2019/11/Mount-Reef-Multibean-2007.jpg) | **structure_visible** | high | Rainbow-coloured 2007 multibeam depth survey with a north arrow and two grey arrows pointing at a gap between container arms. Clearly shows the reef's angular multi-arm footprint from above, plus the "missing bag" gap the card's caption describes. |
| 5 | [Mount-Reef-Deflated-Bag](https://raisedwaterresearch.com/wp-content/uploads/2019/11/Mount-Reef-Deflated-Bag.jpg) | **structure_visible** | medium | **Card error found and corrected here (not in the card):** this file is not a photograph as the card's `"kind": "photo"` claims — it is another false-colour bathymetric/survey render (green/yellow/orange), visually similar to image #4, with a white arrow into a gap at the reef's apex. It does legitimately show the reef structure and the described gap, so the site classification stands, but its `kind` should read "diagram/survey image," not "photo." |
| 6 | [Google Maps link](https://www.google.com/maps/@-37.6471741,176.1986412,17z) | **could_not_load** | high | This is a live interactive map URL, not a fixed image file — there is nothing stable to download or classify; it shows whatever satellite tile is default when opened. Treated as a general location reference only, not usable as reef-specific visual evidence. |

## Videos

| URL | Verdict | Evidence | Best timestamp |
|-----|---------|----------|-----------------|
| [MOUNT REEF DREAM TURNS INTO REALITY!](https://www.youtube.com/watch?v=QsyH6FEzDx4) (fjsoto1, 2006-10-21) | **about_the_reef** | Uploaded 4 days after the reef's right/second half was installed (4 Oct 2006), per the dossier's own construction timeline. No captions/subtitles exist on this video (`yt-dlp --dump-single-json` confirms: "There are no subtitles for the requested languages"), so the uploader's own YouTube description is the only text evidence: a small 1.5m NE swell producing "fast hollow right hand barrels and up to 50 metre rides on both left and right hand breaks," and the description links to the reef project's own (now defunct) site mountreef.co.nz. Title + upload-date match + uploader description are all internally consistent and specific to this structure, not generic Mount Maunganui surf footage. | 85s |

## Frames

| Path | Verdict | Evidence |
|------|---------|----------|
| `03_images/video_frames/mount-maunganui-reef/QsyH6FEzDx4_0125.jpg` | **reef_effect_visible** | Low-res (428x240 source) frame: a small, clean wave peeling left-to-right with a surfer/swimmer past the peak; plain horizon, overcast sky, no coastline or landmark in frame. The frame alone cannot prove location (no visible coastline), so this rests on the parent video's title/date/description match rather than the pixel content — consistent with the rubric's reef_effect_visible category (structure submerged, effect shown, source places it at the reef). |

## Findings and recommendations

1. **No unrelated/site-only media found.** Unlike the other reef where two videos showed beach surfing unconnected to the reef, every accepted item here is either structure_visible or reef_effect_visible with a defensible source basis. Nothing needs to be dropped from the card.
2. **One metadata error found and documented (fix in the card, not here):** image #5 (`Mount-Reef-Deflated-Bag.jpg`) is tagged `"kind": "photo"` in the card but is actually a bathymetric/survey render, not a photograph. Recommend the card's `images[4].kind` be corrected to `"diagram/survey image"`. (This QA file documents the finding; the actual card edit is a separate, tracked change to `02_research/reefs/mount-maunganui-reef.json`.)
3. **The Google Maps entry (#6) is not a stable image** and should probably not count toward the card's image gallery for build/display purposes, since it has no fixed, citable visual content — it is a location reference only.
4. **Hero image recommendation:** `Mount-Reef-Multibean-2007.jpg` — the clearest, best-sourced structure_visible image, directly showing the as-built angular multi-arm footprint (matching the dossier's "as-built vs design" narrative, including the visible gap where a container is missing). The aerial photo (#1) is a reasonable second choice as a wide establishing/context shot, but the reef itself is only a faint shadow in it.

## Files/process record

- Card checked: `02_research/reefs/mount-maunganui-reef.json`
- Videos index checked: `02_research/videos/mount-maunganui-reef/videos.json`
- Frames directory checked: `03_images/video_frames/mount-maunganui-reef/` (only non-rejected file: `QsyH6FEzDx4_0125.jpg`)
- Images downloaded to a session scratchpad with `curl -L -A "Mozilla/5.0"`, viewed with the Read tool, then deleted (scratch folder removed after this check).
- No new photo/video searches were performed; only already-cited/accepted media was re-examined, per the task rule.
- Structured verdicts: `05_qa/reef/mount-maunganui-reef_media_recheck.json`

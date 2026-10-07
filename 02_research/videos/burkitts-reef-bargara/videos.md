# Video index — Burkitts Reef, Bargara QLD

## 1. Diving Bargara, Burkitt's Reef Marine Park (embed this one — short, on-topic)
- **URL:** https://www.youtube.com/watch?v=wuJ__7Js-cY
- **Channel:** Black Beard Diving — uploaded 2021-03-27
- **Duration:** 4:46 (286 s) → **embed_ok: true**
- **What it shows:** Shore-dive footage at Burkitts Reef Marine Park, Bargara esplanade — sandy/rocky bottom, hard coral bommies, reef fish. Uploader's description: "A nice shore dive off the esplanade of Bargara, we came across a variety of life from sea snakes, moray eels and small gummy sharks."
- **Transcript:** none available — YouTube reports no subtitles/auto-captions for this video (checked with `yt-dlp --write-auto-subs --write-subs`).
- **Frames extracted (2, both kept — both clearly show real underwater reef content matching the dive-site description):**
  - `03_images/video_frames/burkitts-reef-bargara/wuJ__7Js-cY_0025.jpg` (00:25) — a striped bubble/moon snail on the sandy bottom.
  - `03_images/video_frames/burkitts-reef-bargara/wuJ__7Js-cY_0205.jpg` (02:05) — school of reef fish over hard coral bommies.

## 2. Surfing at Bargara Beach, QLD (uncertain lead — NOT confirmed to be Burkitts Reef)
- **URL:** https://www.youtube.com/watch?v=O3bEn8029XQ
- **Channel:** Campr — uploaded 2018-02-20
- **Duration:** 1:19 (79 s)
- **embed_ok: false** — flagged, not embedded/linked as if it depicts this site: title, description and full metadata only reference "Bargara Beach" generally (a tourism piece promoting Bargara as a learn-to-surf destination), with no mention of Burkitts Reef, Greg Redgard, or the reshaped point break. Kept in the index only as a labeled possible/uncertain lead per Lior's honesty-over-quantity instruction — a researcher should re-watch it before using it as evidence of the reef itself.
- No transcript or frames pulled, since the video's relevance to this exact structure is unconfirmed.

## Searched but not usable / not found
- No dedicated surf-footage YouTube video of Burkitts Reef itself (the point break, not the dive site) was found despite multiple targeted searches ("Burkitts Reef" + surf/drone/dive, "Greg Redgard" video, ABC News YouTube channel, site:youtube.com Bargara reef).
- **Instagram post** by @abcbrisbane (https://www.instagram.com/abcbrisbane/p/C2n6UcWvcGV/) — contains video/photo of the surf break per its caption, but `yt-dlp` failed to extract it ("No video formats found"), and Instagram requires login for reliable scraping. Not retrievable; listed under blocked_sources.
- **X/Twitter post** by @abcsport (https://x.com/abcsport/status/1751370066221051992) — has an embedded video/photo per the tweet text, but X requires authentication for yt-dlp extraction and was not attempted (out of scope for this pass; flagged as a further lead).
- **ABC Radio "The Bright Side"** episode (https://www.abc.net.au/listen/programs/the-bright-side/mates-surf-break-still-going-strong/103068400) is audio-only, not video — not included here (already cited as [R5] in the dossier).

## Blocked sources
- https://www.instagram.com/abcbrisbane/p/C2n6UcWvcGV/ (yt-dlp: "No video formats found" — Instagram extraction blocked without login)

## Media note 2026-09-25
Lior reviewed both videos and confirmed neither shows the artificial reef itself. Both entries moved from `videos` to `videos_rejected` in `02_research/reefs/burkitts-reef-bargara.json` (reason: "Lior 2026-09-25: video does not show the artificial reef"). The two extracted frames (`wuJ__7Js-cY_0025.jpg`, `wuJ__7Js-cY_0205.jpg`) were moved to `03_images/video_frames/burkitts-reef-bargara/rejected/` and their card paths updated accordingly.

# Video index — Israeli Mediterranean wave climate, surfable days and tidal range (israel-wave-climate-and-tides)

All three researcher-supplied leads are Bat Galim / Haifa surf clips (not of the Shikmona buoy or Hadera tide gauge themselves, which are unmanned instruments with no video coverage found). They are used here to visually confirm the wave-climate description in the dossier (modest, wind-swell-dominated waves, WNW-facing coast, jetty/reef breaks) at the actual site.

## 1. BackDoor, Bat Galim Haifa, Israeli Surfing
- URL: https://www.youtube.com/watch?v=rZ7CNaKz9Ns
- Channel: Zeev D — uploaded 2015-01-04
- Duration: 52 s
- embed_ok: **true** (≤480 s, directly about this site) — Lior can embed this one.
- What it shows: black-and-white footage of a surfer riding a small, steep wave at "Backdoor," the jetty-protected reef break at Bat Galim, Haifa — matches SurferToday's description of Backdoor as "a reef break protected by two jetties that produces a steep and hollow right-hand wave" [R14 in the dossier].
- Transcript: not extracted — this is a short, music-only clip with no spoken dialogue, and yt-dlp's caption download endpoint returned HTTP 429 (Too Many Requests) on repeated attempts during this research session; there is no indication captions exist for this video regardless (auto-caption list included only "en, iw" tracks, likely auto-generated from ambient audio/music with no speech to transcribe).
- Frame captured: `03_images/video_frames/israel-wave-climate-and-tides/rZ7CNaKz9Ns_0017.jpg` at 00:17 — viewed directly; shows a surfer dropping into a wave with a rock jetty visible at frame-right. Matches expectations; kept.

## 2. Israel Surfers 2022 Haifa Bat Galim Beach
- URL: https://www.youtube.com/watch?v=DhUt9TGKnEg
- Channel: MyLife Film Production - Home Studio — uploaded 2022-01-29
- Duration: 146 s (2:26)
- embed_ok: **true** (≤480 s, directly about this site) — Lior can embed this one.
- What it shows: colour footage at Bat Galim beach, Haifa: a kite/windsurfer rigging up on the sand facing breaking waves, rocky breakwater in the foreground, and anchored cargo ships of Haifa Bay visible on the horizon behind the swell line — a good visual anchor for the dossier's mean-SWH (0.5–1.0 m) and WNW–NW direction figures.
- Transcript: not extracted — no subtitle tracks were listed as available for this video ("There are no subtitles for the requested languages"), consistent with it being a music-scored montage with no spoken narration.
- Frame captured: `03_images/video_frames/israel-wave-climate-and-tides/DhUt9TGKnEg_0042.jpg` at 00:42 — viewed directly; shows the kite/windsurfer kneeling on the beach with breaking waves and the breakwater/ships backdrop described above. Matches expectations; kept.

## 3. Wave surfing in Bat Galim Haifa Israel (AQUAZOOM) — BLOCKED
- URL: https://www.youtube.com/watch?v=M5A2xbuh4AM
- Channel: Aquazoom Amir Weizman
- yt-dlp result: `ERROR: [youtube] M5A2xbuh4AM: This video is not available` (fails on both `--dump-single-json` and subtitle/download attempts).
- Title and channel confirmed instead via the YouTube oEmbed API (`https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=M5A2xbuh4AM&format=json`), which returned: title "Wave surfing in Bat Galim Haifa Israel by AQUAZOOM", author "Aquazoom Amir Weizman" — so the video exists and is (per its own title) about Bat Galim, Haifa, but is not fetchable by yt-dlp in this environment (likely an extractor-side restriction, not necessarily unavailable to a human viewer in a browser).
- Recorded as an image entry instead (see `03_images/web/israel-wave-climate-and-tides.json` / `.md` entry 6), using its thumbnail `https://img.youtube.com/vi/M5A2xbuh4AM/hqdefault.jpg` (verified HTTP 200, image/jpeg).
- Listed under blocked_sources below.

## Recommendation for Lior

Both usable videos (#1, #2) are short (under 3 minutes) and directly about Bat Galim, Haifa — both are good candidates to embed directly per Lior's stated preference for short videos. Neither needed a "best timestamp" link-only treatment since both qualify for embedding.

## Blocked sources

- https://www.youtube.com/watch?v=M5A2xbuh4AM — yt-dlp extractor error ("This video is not available"); recorded as a thumbnail image entry instead (see above).

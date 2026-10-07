# Gemini video material extract (READ-ONLY sweep of Gemini's folder)

Agent task, 2026-10-04. Scope: Gemini's `05_web_build/reef_videos.json` + `05_web_build/parse_videos.py`, grepped `05_web_build/index.html` and `02_world_reefs_data/*.md` for youtube/youtu.be/vimeo/abc.net.au links and transcript text, across our 13 reefs. Gemini's folder was not modified.

## Headline finding: Gemini has no real, independent video transcripts

Two mechanisms account for everything in Gemini's video data:

1. **Circular copy.** `05_web_build/parse_videos.py` (read in full) parses markdown files at the literal path
   `C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\02_research\videos\*\videos.md` — **our own project**, not Gemini's.
   Its output, `reef_videos.json`, is therefore our own research reflected back at us for boscombe-surf-reef, burkitts-reef-bargara,
   cables-reef-wa (empty both sides), kovalam-reef-india, narrowneck-gold-coast's first two videos, palm-beach-gold-coast, and
   southern-ocean-surf-reef-albany — every id, title, channel and quote matches our own `videos.json` entries, in several cases
   word-for-word. Some entries don't even bother to re-type the quote: they literally say *"Key quotes: see videos.json (...)"*,
   a stub pointing back at this same circular file rather than a real transcript excerpt.
2. **One unsupported, likely-fabricated quote.** A video id `Gi6wNNP6OKE` appears exactly once, hardcoded into
   `05_web_build/index.html`'s provenance modal, with no entry anywhere else in Gemini's project (not in `reef_videos.json`,
   not in any `.md`). It's labelled "ICM Gold Coast Webinar (Slide 16 / image29.png)" and gives a very specific quote
   attributed to "Aaron Salyer (ICM)" about Narrowneck's 2018 renewal. We already know what `image29.png` actually is — our own
   `01_source_notes/pptx_goldcoast_swells_people_photos.md` (written independently of Gemini) identifies it as a **static
   screenshot** from Lior's pptx of someone else's webinar recording (presenter thumbnail "aaronsalyer", ICM/coastalmanagement.com.au
   watermark), not a video anyone transcribed. The same bare id is also cited, over an hour later in-video, for an unrelated
   Israeli "CCell Michmoret" claim — an implausible pairing. No full URL, channel, or caption file corroborates it anywhere.
   **Flagged as likely fabricated** and copied verbatim (not acted on) to
   `02_research/videos/narrowneck-gold-coast/gemini_Gi6wNNP6OKE.txt`.

`has_real_transcripts: false` in the JSON below reflects this.

## Per-reef results

| Slug | New videos Gemini has (not in ours) | Gemini transcript text copied | Already rejected by Lior (not resurrected) |
|---|---|---|---|
| narrowneck-gold-coast | `Gi6wNNP6OKE` — flagged likely fabricated, see above | `gemini_oUfLGStUKPs.txt`, `gemini_Gi6wNNP6OKE.txt` | — |
| boscombe-surf-reef | none | none (only "see videos.json" stubs, no real text to copy) | — |
| burkitts-reef-bargara | none | `gemini_wuJ__7Js-cY.txt` (itself a rejected video, kept only for the audit trail) | `wuJ__7Js-cY`, `O3bEn8029XQ` |
| cables-reef-wa | none | none | — |
| kovalam-reef-india | none | none | — |
| mexico-reef-2026-unnamed | none — Gemini's "xala_unveiling" entry is a fake id for the same raisedwaterresearch.com source we already researched in depth as R1 | none | — |
| mount-maunganui-reef | none (Gemini has no videos for this reef) | none | — |
| opunake-reef | none (Gemini has no videos for this reef) | none | — |
| palm-beach-gold-coast | none (Gemini's 4th "video" is literally our own `palm_beach_gold_coast.mp4` field footage, copied into its folder) | `gemini_i6k6WN2GtWI.txt` | — |
| prattes-reef-el-segundo | none (Gemini has no videos for this reef) | none | — |
| southern-ocean-surf-reef-albany | none | `gemini_SE4GNR4EiUQ.txt` | — |
| bunbury-airwave | **possible new lead**: ABC article `11802958` ("Airwave artificial surf reef bursts during installation at Bunbury Back Beach") — different article id than our existing `11804314`; claimed to have its own video footage, not yet checked | none (bare citation only, no transcript text) | — |
| borth-coastal-defence-reef | none (Gemini has no videos for this reef) | none | — |

Notes:
- Gemini's `reef_videos.json` has **no key at all** for `bunbury-airwave` — the one lead for that reef came only from prose in `02_world_reefs_data/bunbury-airwave.md`, not from Gemini's video registry.
- `burkitts-reef-bargara.md` also cites an ABC article (`103328224`, Greg Redgard profile) we don't have, but Gemini's own citation treats it as a plain text article with no video/transcript claim, so it isn't listed as a video lead here.
- Slugs present in Gemini's files but outside our 13-reef list (ashdod-sand-and-breakwater, ashkelon-geotubes-2018, haifa-bay-sediment-budget, tel-aviv-detached-breakwaters, israel-geotubes-other-sites, israel-wave-climate-and-tides, and Gemini's own xala-reef-mexico naming of our mexico-reef-2026-unnamed) belong to Gemini's separate Haifa/Israel proposal and were out of scope except where they map onto one of our 13 slugs.

## Files written this pass

- `02_research/videos/00_gemini_video_extract.md` (this file)
- `02_research/videos/00_gemini_video_extract.json`
- `02_research/videos/narrowneck-gold-coast/gemini_oUfLGStUKPs.txt`
- `02_research/videos/narrowneck-gold-coast/gemini_Gi6wNNP6OKE.txt`
- `02_research/videos/palm-beach-gold-coast/gemini_i6k6WN2GtWI.txt`
- `02_research/videos/southern-ocean-surf-reef-albany/gemini_SE4GNR4EiUQ.txt`
- `02_research/videos/burkitts-reef-bargara/gemini_wuJ__7Js-cY.txt`

No files were created, modified, moved, or deleted anywhere under Gemini's folder (`C:\Users\lior\Documents\Gemini\AG\artifical reef`); it was read-only throughout.

```json
{"per_reef": "see 02_research/videos/00_gemini_video_extract.json for the full structured object", "has_real_transcripts": false}
```

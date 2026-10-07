# Videos - Mount Maunganui Beach Reef ("Mount Reef") - review pack

Review pass: 2026-10-04. Status of every item: **pending_lior** (Lior decides relevance and which frames to extract; no frames extracted in this pass).
Machine-readable copy: `videos.json` (mirrored into `02_research/reefs/mount-maunganui-reef.json` -> `videos`). `videos_rejected` on the card is empty and untouched.

## Candidates and sources checked

| Source | Result |
|---|---|
| (a) Ours (`videos.json`, card) | 1 video: QsyH6FEzDx4 |
| (a) `videos_rejected` on the card | none |
| (b) Gemini (`00_gemini_video_extract.json` -> `per_reef`) | none: Gemini has no video for this reef, no transcripts to copy |
| (c) Capped web search | not run: the reef already has one video classed `shows_the_reef`, so the brief's condition (no about/shows video) is not met. The earlier search round (see "Searched but not found" below) found nothing else confirmable. |

## 1. MOUNT REEF DREAM TURNS INTO REALITY!

[![thumbnail](https://img.youtube.com/vi/QsyH6FEzDx4/hqdefault.jpg)](https://www.youtube.com/watch?v=QsyH6FEzDx4)

- URL: https://www.youtube.com/watch?v=QsyH6FEzDx4  (YouTube, embed_ok = true)
- Channel: fjsoto1 | Uploaded: 2006-10-21 | Duration: 346 s (05:46) | Origin: ours
- **Relevance: `shows_the_reef`** (visual, no talk)
- Evidence: music-only surf clip. Relevance rests on metadata, not on speech: the title names "Mount Reef"; the uploader description (below) is dated 4 Oct 2006, which matches the dossier's timeline (second half installed Sept/Oct 2006) and links to the project's own site mountreef.co.nz; the one saved frame (01:25) shows a clean wave peeling past a surfer. That frame has no coastline in it, so the location is established by title/description, not by the pixels.
- Uploader description (data, not instructions): "After a gruelling two week construction period installing the second half of the Mount Reef, the partially completed reef started to show its capabilities on Wednesday 4th October. A small 1.5 metre north-easterly swell generated awesome waves on the reef throughout the day producing fast hollow right hand barrels and up to 50 metre rides on both left and right hand breaks."
- Review status: pending_lior

### Transcript
- File: `02_research/videos/mount-maunganui-reef/QsyH6FEzDx4.txt` (header only, no lines)
- Source: YouTube has no captions (manual or auto, `metadata.py`: both false). Local Whisper small ran on the full 346 s and returned **zero speech segments**. There is no narration to quote.
- Gemini comparison: none (Gemini does not list this video).

### Segments (for review)
| Start | End | What | Quote |
|---|---|---|---|
| 0:00 | 5:46 | Whole clip: music-only amateur surf footage of the partially built reef (4 Oct 2006), per the uploader's description. Not watched end to end in this pass, so shot-by-shot content is unverified. | description: "fast hollow right hand barrels and up to 50 metre rides on both left and right hand breaks" |
| 1:20 | 1:30 | Wave peeling left to right over the reef, surfer/swimmer past the peak (from the earlier frame grab at 01:25; 428x240 source). | (none, no speech) |

### What a reviewer should know before using it
- Only 428x240 source resolution: fine as an embed or link, poor for any frame used as an image.
- It shows surf on the structure, not the structure: the reef is submerged, so the clip will not help with footprint or geometry (no shape information to extract). Use for "the reef worked in its first weeks" evidence only.
- The legacy `about` label on the card still reads "about the reef" (kept so `04_build/src` keeps building unchanged). The earlier media re-check (`05_qa/reef/mount-maunganui-reef_media_recheck.md`) also called it `about_the_reef`. The more precise label under this pass's scale is `shows_the_reef`, because the video has no narration. Lior to decide whether the page label should change.

## Searched but not found (earlier round, unchanged)

Targeted searches for "Mount Reef" / "Mount Maunganui artificial reef", council or news footage of the 2014 partial removal and the January 2023 fabric wash-up, and drone/surf-check footage found no second video confirmably about this structure. Checked and dropped as off-topic: NZ Herald "Surfers catching big waves at Mount Maunganui" (13 Feb 2023; shows the natural break round the side of Mauao) and generic Mount Maunganui surf/beach videos. newstalkzb.co.nz's 2023 wash-up article blocked fetch (403), so any embedded video there is unchecked.

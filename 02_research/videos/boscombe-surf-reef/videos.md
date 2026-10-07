# Video review pack - Boscombe Surf Reef

Prepared 2026-10-04. Status of every video: **pending_lior** (Lior decides relevance and which frames to extract; no frames extracted in this pass).
Machine-readable version: `videos.json` (same list is mirrored into the card `02_research/reefs/boscombe-surf-reef.json` -> `videos`; `videos_rejected` is empty and untouched).

Candidates checked: our 4 videos (all from the dossier's "Video leads"); Gemini's list (4 videos, the same 4 ids - see below); no web search needed
because two videos are `about_the_reef` and one is `shows_the_reef`.

**Gemini check:** Gemini's `reef_videos.json` for this reef is a copy of OUR catalog (its parse_videos.py reads our videos.md). Its only "transcript"
text is the stub `Key quotes: see videos.json ...` - no independent claims, nothing to compare against our transcripts.

Transcript note: the earlier `.txt` files here had no header or timestamps (plain deduplicated text). All three captioned videos were re-pulled on 2026-10-04
with `transcribe.py` (YouTube auto captions, English), so each `.txt` now has the full header and `[mm:ss]` stamps. Quotes below are verbatim auto-caption text
(ASR errors such as "reath" = reef, "bosam" = Boscombe are left as captioned).

| # | Video | Length | Relevance | Segments | Transcript |
|---|-------|--------|-----------|----------|------------|
| 1 | Boscombe Surf Reef - The Story | 5:15 | about_the_reef | 9 | auto captions |
| 2 | Boscombe Surf Reef - the regeneration of Boscombe | 6:07 | mentions_reef_briefly | 6 | auto captions |
| 3 | Boscombe Surf Reef the construction story so far | 2:03 | about_the_reef | 5 | auto captions (new this pass) |
| 4 | Boscombe Surf Reef in action November 2009 | 1:03 | shows_the_reef | 1 (whole clip) | none - no captions, no speech |

---

## 1. Boscombe Surf Reef - The Story
- https://www.youtube.com/watch?v=F0PslWKkbf4  | BoscombeReef | 2010-02-25 | 315 s | embed OK | thumbnail https://img.youtube.com/vi/F0PslWKkbf4/hqdefault.jpg
- Origin: ours. Transcript: `02_research/videos/boscombe-surf-reef/F0PslWKkbf4.txt` (YouTube auto captions, en).
- **Relevance: about_the_reef.** Evidence: the description calls it "a mini-documentary about Europe's first artificial surf reef... the story of how, where and why it was built"; the transcript covers history, structure, construction, size/position and wave mechanics.
- Segments (what the narration covers; whether matching footage is on screen is not known from text):

| Time | What | Quote |
|------|------|-------|
| 0:04-0:25 | Intro: Europe's first artificial surf reef, GBP 11m regeneration scheme | "home to Europe's first artificial surf Reef thanks to an 11 million pound regeneration scheme" |
| 0:47-1:09 | Project history: idea 1999, car park sold to finance, government permission 2007 | "Bournemouth burough Council sold an underused car park to finance the scheme" |
| 1:09-1:31 | Structure: base layer, top layer, ramp; webbing base + geotextile bags | "each layer consists of two elements a webbing base and huge geotextile bags" |
| 1:31-1:50 | Prefabrication on a field; section folded by cranes onto a barge | "the section was then concertina by huge cranes and laid onto a barge" |
| 1:50-2:27 | Aug 2008 deployment just east of Boscombe Pier; divers, anchors, sand filling; largest bags 70 x 2 x 6 m | "the largest bags were 70 M long 2 m high and 6 M wide" |
| 2:27-2:43 | Base layer done 2008, winter stop, top layer and ramp autumn 2009 | "in the Autumn the top layer and ramp was laid and filled" |
| 2:43-3:22 | Size, position, hydraulics: football-pitch size, 250 m offshore, ramp not wave machine | "it's the size of a football pitch and positioned 250 M offshore" |
| 3:19-3:46 | Surf use (right-handers, RNLI cover) and marine life | "a variety of species now live on the reef including crabs Lobster pipe fish seab bass and mullet" |
| 3:46-4:02 | Regeneration outcome: 60-country coverage, new businesses, ~80 jobs | "around 80 jobs have been created along the seafront alone" |

- Gemini claims: none independent (copy of our catalog).
- Legacy card note kept: one frame already grabbed earlier (`03_images/video_frames/boscombe-surf-reef/F0PslWKkbf4_0045.jpg`, "Before" overlay near the pier).

## 2. Boscombe Surf Reef - the regeneration of Boscombe
- https://www.youtube.com/watch?v=HeiYPXt85LM  | BoscombeReef | 2009-11-20 | 367 s | embed OK | thumbnail https://img.youtube.com/vi/HeiYPXt85LM/hqdefault.jpg
- Origin: ours. Transcript: `02_research/videos/boscombe-surf-reef/HeiYPXt85LM.txt` (YouTube auto captions, en).
- **Relevance: mentions_reef_briefly.** Evidence: the description is about "positive changes in the previously run-down area"; the reef is named as catalyst, economic driver and surf-school draw, but its structure, size and build are never described.
- Silent music stretches 0:53-1:16 and 1:22-1:47 have no speech - the transcript cannot say whether the reef is on screen there (worth a quick look by Lior).

| Time | What | Quote |
|------|------|-------|
| 1:16-1:22 | Reef framed as the regeneration opportunity | "putting the surf Reef out to seea this being the landbased Leisure was the real opportunity to regenerate" |
| 1:47-2:15 | "The Reef is the economic driver"; investment along the seafront | "The Reef is the economic driver" |
| 2:41-3:15 | Surf-school owner Sean Taylor: people coming to surf the reef, beginners on very small waves | "people are taking beginners lessons on very small waves" |
| 3:34-3:50 | Publicity value estimated at "10 million" (currency not captioned), "a lot" attributed to the reef | "a lot of that's been attributable to the reef" |
| 4:10-4:45 | Businesses named after the reef; reef "probably the Catalyst" | "a hotel Redevelopment was renamed the reef" |
| 5:20-5:36 | Funding: residential land and beach-pod sales, not council tax | "funded by the sale of the [residential] land and the sale of the beach pods" |

- Correction vs. the earlier card: the third key quote read "estimated already at [multi-]million"; the caption actually says "10 million". Card text updated.
- Gemini claims: none independent.

## 3. Boscombe Surf Reef the construction story so far
- https://www.youtube.com/watch?v=7xMwL09a1TI  | BoscombeReef | 2009-07-08 | 123 s | embed OK | thumbnail https://img.youtube.com/vi/7xMwL09a1TI/hqdefault.jpg
- Origin: ours. Transcript: `02_research/videos/boscombe-surf-reef/7xMwL09a1TI.txt` (YouTube auto captions, en) - **newly transcribed this pass** (was metadata-only). Description on YouTube is empty.
- **Relevance: about_the_reef.** Evidence: the whole video is the build - NZ materials, base sections, barge deployment, divers, sand filling.
- Worth noting for the footprint work: it says the **first base section** is "approximately the size of a football pitch" and the base is "three separate sections", whereas video 1 says the **whole reef** is football-pitch sized. The two statements need reconciling against the plan dimensions.

| Time | What | Quote |
|------|------|-------|
| 0:06-0:29 | Materials shipped from NZ; base made of three triple-stitched sections | "the base of the Sur reath is formed from three separate sections" |
| 0:37-0:53 | 1,000+ ties; first base section ~football-pitch size, folded for transport | "the first section of the reef base layer is approximately the size of a football pitch" |
| 0:53-1:06 | 10-tonne section lifted onto a barge | "the section weighs 10 tons and so lifting is a delicate process" |
| 1:01-1:30 | Barge to site 250 m from the beach; section unfolds on the seabed; divers anchor it | "the site of the reef just 250 M from boson Beach Shoreline" |
| 1:25-1:52 | Bags filled one by one with beach sand via a 300 m pipeline; 1-4 h per bag | "a 300 M pipeline transports the sand out to sea where divers attach the pipes to the bags" |

- Gemini claims: none independent.

## 4. Boscombe Surf Reef in action November 2009, Bournemouth UK
- https://www.youtube.com/watch?v=eceOTU06Dts  | Sean Gardiner | 2009-11-06 | 63 s | embed OK | thumbnail https://img.youtube.com/vi/eceOTU06Dts/hqdefault.jpg
- Origin: ours. **Transcript: none** - the video has no captions (manual or auto) and no speech (music-only surf clip); nothing for Whisper to transcribe. `transcript_path` is null.
- **Relevance: shows_the_reef - classified from the title and description only, not from any transcript.** Title: "Boscombe Surf Reef in action November 2009"; description: "A few clips of the Bournemouth Surf Reef being used by body boarders one day after the official press launch."
- Consistent with the frame noted in an earlier pass (`03_images/video_frames/boscombe-surf-reef/eceOTU06Dts_0018.jpg`: wave breaking, two bodyboarders, yellow marker buoy), but sub-timings are not determined, so one whole-clip segment (0-63 s) is listed.
- Caution: the uploader's 2020 update calls the reef a council "fiasco" / "white elephant" and says the reef makers "disappeared back to NZ"; that is opinion in a description, unverified, and not used as fact.
- Gemini claims: none independent.

---

## Further leads from the dossier, NOT added to this list (outside the brief's candidate set)
Metadata fetched 2026-10-04 so you can decide; none transcribed or reviewed. All have no captions except the last (auto only).

| Video id | Title | Channel | Length | Uploaded | Note |
|----------|-------|---------|--------|----------|------|
| 0Oi6D6Xp0oY | Aerial view of Boscombe Reef | BoscombeReef | 36 s | 2009-10-15 | no description; likely the most useful for footprint/plan view |
| WWcZc1KZyvw | New Surf Reef at Boscombe, Bournemouth, UK | Stephen Derrick | 2:24 | 2009-11-02 | "Big waves at the new Surf Reef... filmed Sunday 1st November 2009" |
| E2erk3lrE2I | How the Boscombe Reef will look | BoscombeReef | 0:28 | 2009-07-08 | computer-generated underwater visualisation (auto captions only) |
| Ft4niInpw7M | Boscombe Artificial Surf Reef Bait Cam - Bournemouth University | Wessex Portal | 5:41 | 2015-03-23 | GoPro bait-cam fish survey, summers 2013 and 2014 |

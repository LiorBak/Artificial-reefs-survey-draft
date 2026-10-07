# Video index — Kovalam Reef (Lighthouse Beach), India

3 videos found and confirmed about this exact site, all short enough (≤59s) to embed directly per Lior's rule (short videos embedded, long ones linked with a timestamp).

## 1. Surfing Kovalam Beach, South Indian Small, Fun Waves - GoPro Footage
- https://www.youtube.com/watch?v=E2_03-CkwGY
- Asher Fergusson, 2013-03-02, 22s. **Embed.**
- GoPro POV/selfie surf clip. The uploader's own YouTube description explicitly names the artificial reef: "They have some decent waves and there is an artificial reef that really goes off when the swell is big enough." This is the strongest direct textual link between a video and the reef itself found in this pass.
- No spoken dialogue (ambient wave/wind sound only) — no transcript attempted for content reasons; see "Transcripts" note below re: also being blocked by rate-limiting.

## 2. Kovalam Surf Club social video
- https://www.youtube.com/watch?v=X3NqayC1Iqc
- Channel "An Janssen", 2017-12-13, 59s. **Embed.**
- Confirmed as this exact site: the video's own thumbnail reads "MEET JELLE RIGOLE FROM BELGIUM" — Jelle Rigole is the named founder of a local Kovalam surf club quoted in the dossier ([R1], via Raised Water Research) describing the reef's structural failure ("the reef sank deeper into the sand so most of the waves just roll over the reef now without even breaking"). This ties the video directly to the dossier's own named source.
- No transcript attempted (social-clip style, no confirmed dialogue; also blocked by rate-limiting, see below).

## 3. Surfing - Water Sports in Kovalam, Kerala
- https://www.youtube.com/watch?v=6eSOn_m5Oz8
- SportsKerala (official Kerala sports-tourism channel), 2017-11-21, 52s. **Embed.**
- General surfing/water-sports promo footage explicitly located at "Kovalam, Kerala," describing wave heights of 0.5–2 m and surf-tourism amenities. Confirms the Kerala site (as opposed to the similarly-named Covelong Point near Chennai, which a couple of search hits under "Kovalam" actually referred to — see rejected videos below).
- No transcript attempted (promo b-roll style; also blocked by rate-limiting, see below).

## Transcripts
`yt-dlp --write-auto-subs` was attempted for all three videos and repeatedly returned `HTTP Error 429: Too Many Requests` from YouTube's subtitle endpoint specifically (separate from the metadata/`--dump-single-json` calls, which succeeded normally), even after retries. No transcript files were produced. Given these are short (22-59s) ambient/social/promo clips with no description indicating substantive spoken narration, the loss is likely minor, but this is a genuine gap, not a judgment call — a future pass with a working subtitle endpoint should retry.

## Frames
No frames extracted. All three videos are short enough to embed directly (≤480s rule), so per the task's own rule ("frames when the page relies on a video") frames were not needed. One test frame extraction was done on video #1 (00:05 and 00:14) to confirm the pipeline works (yt-dlp download → imageio_ffmpeg → ffmpeg frame grab); both frames were a surfer selfie and undifferentiated whitewash, not useful reef-structure imagery, so they were deleted rather than saved, per the "delete frames that don't show what you expected" rule.

## Rejected / not used
- **"How Kovalam became a top surfing destination"** (The Hindu, youtube.com/watch?v=oSFOPrdgJro, 2019-09-03, 51s) — despite the title, its own description is about the "Covelong Point Surf, Music and Yoga Festival," which is at Covelong/Kovalam Beach near Chennai, Tamil Nadu — a different, unrelated beach that shares a similar name with Kovalam, Kerala. Rejected as wrong site.
- **"Surfing at Kovalam Beach | India Video"** (indiavideodotorg, youtube.com/watch?v=KyNAtHI1j0c, 2014-05-31, 72s) — located at Eve's/Hawah Beach, Kovalam (per its own description), which per the dossier is a different one of Kovalam's four beaches than Lighthouse Beach, where the reef was actually built. Not used to avoid conflating beaches, though it is genuinely in Kovalam, Kerala.
- **Vimeo "India's First Multi-Purpose Reef Goes Off"** (vimeo.com/11274816, dossier [R11]) — could not be fetched: yt-dlp reports "The web client only works when logged-in," requiring Vimeo account credentials, which this task does not authorize entering. Confirmed still blocked in this pass. Listed under blocked_sources.

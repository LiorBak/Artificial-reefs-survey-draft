# Brief: VIDEO REVIEW PACK for ONE reef (slug given in your prompt)

Goal: make every candidate video easy for Lior to review. He will decide relevance and tell us which frames to extract later.
Do NOT extract frames. Tools: 02_research\videos\tools\ (README.md has the tested commands).

## RESUME RULE (2026-10-04, after an interruption)
An earlier run may have been stopped part-way. Transcript .txt files already in 02_research\videos\<slug>\ can be reused if their header
is complete. Before writing, confirm the card JSON and videos.json parse; write each JSON file in one step (build it in memory, then
save), never field by field.

## Candidates
a. Ours: 02_research\videos\<slug>\videos.json, plus the card's videos_rejected (02_research\reefs\<slug>.json). Rejected ones stay
   rejected with Lior's reason; do not re-add them.
b. Gemini's: 02_research\videos\00_gemini_video_extract.json -> per_reef[<slug>] (new videos + any copied transcripts). Gemini material
   is unverified until you check it.
c. ONLY if this reef still has no video classed about_the_reef or shows_the_reef after (a)+(b): a capped web search (<= 3 new candidates:
   news, council, drone footage) - mark origin "new_search".

## Per video
- metadata.py (title, channel, duration, upload date, description).
- Transcript: reuse our existing txt if present; else transcribe.py (captions first, else local Whisper) into
  02_research\videos\<slug>\<id>.txt. Where Gemini supplied transcript text, compare with ours and note differences.
  Whisper is CPU-heavy and other agents run in parallel: transcribe at most 40 minutes of audio per video.
- Read transcript + description; mark SEGMENTS where the reef is shown or discussed:
  [{"start_s","end_s","what" (e.g. "drone shot over the bag field", "engineer explains crest depth"),"quote" (<= 20 words)}].
- relevance: about_the_reef | shows_the_reef (visual, little talk) | mentions_reef_briefly | site_only | unrelated |
  unknown (no transcript and metadata unclear), with one line of evidence.
- embed_ok only for YouTube; thumbnail https://img.youtube.com/vi/<id>/hqdefault.jpg

## Output
Write the updated 02_research\videos\<slug>\videos.json; per video fields: url, platform, video_id, title, channel, duration_seconds,
upload_date, origin (ours | gemini | new_search), relevance, relevance_evidence, segments, transcript_path (relative to project root,
forward slashes), transcript_source, gemini_claims, embed_ok, thumbnail, review_status "pending_lior". Also write a readable videos.md.
Mirror the list into the card's "videos" array (same fields; leave videos_rejected untouched); validate the JSON parses.

## Final JSON
{"slug","videos":[{"url","title","duration_seconds","relevance","origin","transcript_source","segments":n}],"notes"}

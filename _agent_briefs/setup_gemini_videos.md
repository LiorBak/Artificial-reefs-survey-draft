# Brief: extract Gemini's video material (READ-ONLY on Gemini's folder)

Read Gemini's 05_web_build\reef_videos.json and 05_web_build\parse_videos.py; grep 05_web_build\index.html and 02_world_reefs_data\*.md
for youtube / youtu.be / vimeo / abc.net.au links and any transcript text (look for "transcript", timestamps like 01:23, quote blocks).
Decide whether Gemini has REAL transcripts or only quote stubs (several stubs say "see videos.json", i.e. they point back at OUR files).
For each of our 13 reefs list:
- videos in Gemini that are not in our 02_research\videos\<slug>\videos.json (compare by video id; also check the card's videos_rejected - do not resurrect rejected ones, list them separately);
- any transcript text Gemini has: copy it verbatim into 02_research\videos\<slug>\gemini_<id>.txt with a header
  "Source: Gemini survey (UNVERIFIED) - <file path in Gemini folder>";
- Gemini's claims about each video.
Write 02_research\videos\00_gemini_video_extract.md and 02_research\videos\00_gemini_video_extract.json shaped
{"per_reef": {"<slug>": {"new_videos": [{"url","id","title","gemini_claims"}], "gemini_transcripts": ["paths"], "already_rejected_by_lior": ["ids"]}}, "has_real_transcripts": bool, "notes": "..."}

Final JSON: the same object.

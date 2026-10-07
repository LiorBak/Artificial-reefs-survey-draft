# Brief: build and test the transcription toolchain -> 02_research\videos\tools\

Write README.md there with the exact working commands.
1. metadata.py URL -> JSON (title, channel, duration_seconds, upload_date, description, thumbnail, captions available?) via python -m yt_dlp --dump-single-json --skip-download.
2. transcribe.py URL --out DIR [--max-min 40]
   a. Captions first: python -m yt_dlp --skip-download --write-subs --write-auto-subs --sub-langs "en.*,he.*,iw.*" --sub-format vtt
      -> convert to timestamped plain text lines "[mm:ss] text" (dedupe rolling auto-caption lines) -> <id>.txt with a header block:
      title, channel, duration, upload date, url, "Transcript source: YouTube captions (manual|auto)", retrieved date.
   b. No captions: download audio only to %TEMP% (yt_dlp -f bestaudio), transcribe the first --max-min minutes with local Whisper:
      try faster-whisper (pip install faster-whisper; model "small"; device cpu; compute_type int8);
      else openai-whisper; if neither installs on Python 3.14, try another installed Python ("py -0", "py -3.12 -m pip ..."),
      or pip install uv then "uv run --python 3.12 --with faster-whisper python transcribe_whisper.py ...".
      Header: "Transcript source: local Whisper <model> (speech-to-text, may contain errors)". Delete the audio afterwards.
   c. Non-YouTube pages (e.g. abc.net.au news): try yt_dlp on the page URL first.
TEST on one short captioned video (https://www.youtube.com/watch?v=eceOTU06Dts) via captions, and force the Whisper path on a 60-second slice of the same video. Keep no test output in the project.

Final JSON: {"captions_path_ok": bool, "whisper_path_ok": bool, "whisper_command": "...", "seconds_per_audio_minute": number, "caveats": ["..."]}

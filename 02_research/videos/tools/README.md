# Video transcription toolchain

Three scripts, one shared helper module. All take a video (or video-page)
URL and work for YouTube and, via yt-dlp's generic extractor, other sites
that embed a playable video (e.g. abc.net.au news pages) -- there is no
YouTube-specific code path; the same commands are simply tried first for
every URL.

- `common.py` -- shared helpers (yt-dlp invocation, caption-language
  picking, VTT parsing/dedup, header-block writer). Not run directly.
- `metadata.py` -- `URL -> JSON` metadata.
- `transcribe.py` -- `URL --out DIR [--max-min 40] [--model small] [--force-whisper]`
  orchestrator: captions first, local Whisper fallback.
- `transcribe_whisper.py` -- standalone local-Whisper backend
  (`AUDIO_PATH -> JSON segments` on stdout). Invoked by `transcribe.py` as a
  subprocess, once per interpreter it tries -- never imported directly --
  so the fallback chain below works even if the *current* interpreter has
  no whisper package installed at all.

Environment this was built/tested on: Windows 11, Python 3.14.4
(`C:\Users\lior\AppData\Local\Python\pythoncore-3.14-64\python.exe`),
yt-dlp 2026.08.19, faster-whisper 1.2.1 (installs fine on 3.14; no need for
the Python-3.12 fallback in practice here, see Caveats).

## 1. metadata.py

```bash
python metadata.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Wraps `python -m yt_dlp --dump-single-json --skip-download` and prints:

```json
{
  "id", "title", "channel", "duration_seconds", "upload_date",
  "description", "thumbnail",
  "captions_available", "auto_captions_available",
  "caption_languages", "auto_caption_languages",
  "url", "extractor"
}
```

`captions_available` / `auto_captions_available` are the "captions
available?" field the brief asked for, split into manual vs. automatic
(both are useful -- `transcribe.py` prefers manual when both exist).

## 2. transcribe.py

```bash
python transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID" --out "02_research/videos/<slug>"
python transcribe.py URL --out DIR --max-min 40          # cap on Whisper minutes (default 40)
python transcribe.py URL --out DIR --force-whisper        # skip captions, go straight to local Whisper
python transcribe.py URL --out DIR --model small           # Whisper model size (default: small)
```

Writes `<out_dir>/<video_id>.txt`:

```
Title: ...
Channel: ...
Duration: 315s (05:15)
Upload date: 2010-02-25
URL: https://www.youtube.com/watch?v=...
Transcript source: YouTube captions (auto, lang=en)   <- or: local Whisper small (speech-to-text, may contain errors)
Retrieved: 2026-10-04
------------------------------------------------------------

[00:00] [Music]
[00:04] oh bosum is now the UK's most Innovative
...
```

Prints one JSON line to stdout summarizing what happened (path, source,
line count, and for the Whisper path the backend/command/timings used).

### 2a. Captions path (tried first, unless `--force-whisper`)

Runs, verbatim per the brief:

```bash
python -m yt_dlp --write-subs --write-auto-subs --sub-langs "en.*,he.*,iw.*" --sub-format vtt --skip-download -o "<out_dir>/%(id)s.%(ext)s" URL
```

(plus `--js-runtimes node:<path>` -- see Caveats) then, among whatever
`<id>.<lang>.vtt` files land in `--out`, picks the best one: manual beats
automatic, then language rank en\* > he\*/iw\*, then the plain variant over
an `-orig` one. The `.vtt` files are left in `--out` alongside the `.txt`
(matches the existing convention already in e.g.
`02_research/videos/boscombe-surf-reef/`, which has `*.en.vtt` +
`*.en-orig.vtt` + `*.txt` per video).

Conversion to `[mm:ss] text` lines (`common.vtt_to_timestamped_lines`)
flattens every cue's text lines in order and drops a line that is identical
to the immediately-preceding *emitted* line. This is what collapses
YouTube's rolling two-line auto-caption windows (each new word-group is
shown first growing against the previous finished line, then repeated
alone once "finished") down to one line per new phrase, stamped with the
cue's start time. **Important subtlety**: YouTube's auto-caption VTT uses
a literal single-space line (`" "`) as a "nothing here yet" placeholder in
the two-line window, which is cue *content*, not a WebVTT blank-line
separator -- the parser must check for an exactly-empty line (`""`) to end
a cue, not a whitespace-stripped-empty one, or the first line of audio
("[Music]" in the test video) silently disappears. (Found and fixed this
during testing -- see `common.parse_vtt_cues`.)

### 2b. Local Whisper path (no usable captions, or `--force-whisper`)

1. Downloads audio only (`-f bestaudio`, native container, no ffmpeg
   needed) to a fresh `%TEMP%\reef_audio_XXXXXXXX\` directory.
2. Decodes up to `--max-min` minutes of it to a mono 16kHz float32 array
   with PyAV (bundled with faster-whisper -- no system ffmpeg required;
   this machine has none on PATH) and transcribes with faster-whisper.
3. Deletes the temp audio directory in a `finally` block, always (verified
   empty afterwards: `C:\Users\lior\AppData\Local\Temp\reef_audio_*` does
   not survive a run).
4. Writes the same header + `[mm:ss] text` body format, with
   `Transcript source: local Whisper <model> (speech-to-text, may contain errors)`.

Backend fallback chain (`transcribe.py: whisper_fallback_chain`), tried in
order until one exits 0, exactly matching the brief:

1. Run `transcribe_whisper.py` with the *current* interpreter
   (`sys.executable`) -- this is the path that actually ran in testing.
2. `pip install faster-whisper` (then `openai-whisper`) on the current
   interpreter, retry.
3. Other Python versions found via `py -0p` (e.g. `py -3.12 -m pip install
   faster-whisper`, then rerun through that interpreter).
4. `pip install uv`, then
   `uv run --python 3.12 --with faster-whisper python transcribe_whisper.py AUDIO --max-min N --model small`.

## Caveats / things found while building and testing this

- **YouTube needs a JS runtime now.** Without one, yt-dlp prints
  `WARNING: ... Only deno is enabled by default ...` and subtitle/format
  extraction can silently come back incomplete. Deno isn't installed here,
  but Node is (`C:\Program Files\nodejs\node.exe`), so both `metadata.py`
  and `transcribe.py` auto-detect Node via `shutil.which("node")` and pass
  `--js-runtimes node:<path>` to every yt-dlp invocation
  (`common.ytdlp_base_cmd`). If Node isn't found, yt-dlp still runs (just
  with the warning) -- it is not a hard dependency, just a reliability
  improvement.
- **The brief's test URL (`https://www.youtube.com/watch?v=eceOTU06Dts`)
  has no captions at all** (`--list-subs` confirms: "has no automatic
  captions" / "has no subtitles"), and forcing local Whisper on it produces
  an empty transcript (0 segments). This is consistent, not a bug: it's a
  63-second clip of surf footage with no dialogue, so there is nothing for
  either YouTube's ASR or local Whisper to transcribe. Confirmed the
  pipeline still completes cleanly (correct header, empty body, exit 0)
  rather than crashing.
- Because of the above, the captions path was validated end-to-end against
  a different, real video from this same project that **does** have
  captions (`F0PslWKkbf4`, "Boscombe Surf Reef - The Story", already
  catalogued in `02_research/videos/boscombe-surf-reef/`) -- output
  written only to the scratch temp dir, nothing left in the project. The
  dedup produced 116 clean lines matching the already-known transcript.
- Local Whisper accuracy was validated the same way: transcribing the
  first 60s of `F0PslWKkbf4`'s audio with faster-whisper/small reproduced
  the known script near-verbatim (e.g. "The reef is the first of its kind
  in the Northern Hemisphere..."), modulo a plausible ASR miss on the
  place name ("BOSKUM" for "Boscombe").
- **First Whisper run on a machine is slow**: the very first
  `--force-whisper` run took ~219s for 60s of audio because it also
  downloaded the "small" model weights from Hugging Face. A second,
  warm-cache run transcribing 60s of real speech took ~19.8s -- i.e.
  roughly **20 seconds of CPU time per minute of audio** once the model is
  cached locally (int8, CPU, faster-whisper `small`). Budget for a
  few-hundred-MB one-time model download on a fresh machine.
- No system ffmpeg is installed (`ffmpeg -version` -> not found). Not
  needed here: `-f bestaudio` downloads a native container directly
  (yt-dlp just warns "Install ffmpeg to fix this" re: DASH m4a container
  compatibility, which doesn't matter since we decode it ourselves via
  PyAV, bundled with faster-whisper) and caption `.vtt` files are parsed
  by hand rather than converted.
- yt-dlp's audio-only format download (`-f bestaudio`) hit a transient
  `HTTP Error 403: Forbidden` once; an immediate retry succeeded. Worth a
  retry loop in production use if this is seen often; not added to
  `transcribe.py` since it didn't recur in repeated testing.
- `pip install faster-whisper` on this Python 3.14 env force-upgraded
  `click` 7.1.2 -> 8.5.0, which pip flags as incompatible with an unrelated
  pre-existing package (`uvicorn 0.13.4` wants `click==7.*`). Not touched
  further since it's outside this toolchain's scope -- flagging in case
  `uvicorn` is used elsewhere on this machine.

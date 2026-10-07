"""Shared helpers for metadata.py / transcribe.py / transcribe_whisper.py.

No third-party imports at module level beyond the stdlib, so this file can be
imported cheaply from any of the three entry points (and from transcribe.py
before it knows whether faster-whisper etc. are even installed).
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


# --------------------------------------------------------------------------
# yt-dlp invocation
# --------------------------------------------------------------------------

def find_node() -> str | None:
    """Locate a Node.js binary to hand to yt-dlp's --js-runtimes.

    Recent YouTube extraction needs a JS runtime (deno by default, which is
    usually not installed on a dev box). Node is far more likely to already
    be present, so we prefer it explicitly when found.
    """
    return shutil.which("node")


def ytdlp_base_cmd() -> list[str]:
    """Base argv for invoking yt-dlp as a module of the *current* interpreter."""
    cmd = [sys.executable, "-m", "yt_dlp"]
    node = find_node()
    if node:
        cmd += ["--js-runtimes", f"node:{node}"]
    return cmd


def run_ytdlp(args: list[str], timeout: int = 180) -> subprocess.CompletedProcess:
    """Run yt-dlp with the given extra args, capturing output as text."""
    cmd = ytdlp_base_cmd() + args
    return subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
        timeout=timeout,
    )


def fetch_metadata_json(url: str, timeout: int = 180) -> dict:
    """Run yt-dlp --dump-single-json and return the parsed dict.

    Raises RuntimeError with stderr attached if yt-dlp fails outright.
    """
    result = run_ytdlp(["--dump-single-json", "--skip-download", url], timeout=timeout)
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(
            f"yt-dlp metadata fetch failed (exit {result.returncode}):\n{result.stderr.strip()}"
        )
    return json.loads(result.stdout)


def summarize_metadata(url: str, data: dict) -> dict:
    """Project the full yt-dlp info dict down to the fields the brief wants."""
    subs = data.get("subtitles") or {}
    auto = data.get("automatic_captions") or {}
    return {
        "id": data.get("id"),
        "title": data.get("title"),
        "channel": data.get("channel") or data.get("uploader"),
        "duration_seconds": data.get("duration"),
        "upload_date": data.get("upload_date"),
        "description": data.get("description"),
        "thumbnail": data.get("thumbnail"),
        "captions_available": bool(subs),
        "auto_captions_available": bool(auto),
        "caption_languages": sorted(subs.keys()),
        "auto_caption_languages": sorted(auto.keys()),
        "url": data.get("webpage_url") or url,
        "extractor": data.get("extractor"),
    }


def get_metadata(url: str, timeout: int = 180) -> dict:
    return summarize_metadata(url, fetch_metadata_json(url, timeout=timeout))


# --------------------------------------------------------------------------
# Caption language selection
# --------------------------------------------------------------------------

LANG_PRIORITY_PREFIXES = ["en", "he", "iw"]


def lang_rank(lang: str) -> tuple:
    for i, pref in enumerate(LANG_PRIORITY_PREFIXES):
        if lang == pref or lang.startswith(pref + "-"):
            # exact match ranks ahead of a "-XX" regional/translated variant,
            # and an "-orig" variant ranks ahead of other suffixes.
            exact = 0 if lang == pref else (1 if lang.endswith("-orig") else 2)
            return (i, exact, lang)
    return (len(LANG_PRIORITY_PREFIXES), 0, lang)


def pick_caption_track(meta_json: dict) -> tuple[str, str] | tuple[None, None]:
    """Pick the best (lang, kind) to download, kind in {"manual","auto"}.

    Manual subtitles are preferred over automatic captions for any given
    language rank; language preference follows en* > he* > iw* per the brief.
    """
    subs = meta_json.get("subtitles") or {}
    auto = meta_json.get("automatic_captions") or {}

    candidates = []
    for lang in subs:
        if lang_rank(lang)[0] < len(LANG_PRIORITY_PREFIXES):
            candidates.append((lang_rank(lang), 0, lang, "manual"))  # 0 = manual beats auto
    for lang in auto:
        if lang_rank(lang)[0] < len(LANG_PRIORITY_PREFIXES):
            candidates.append((lang_rank(lang), 1, lang, "auto"))

    if not candidates:
        return (None, None)
    candidates.sort(key=lambda c: (c[0], c[1]))
    _, _, lang, kind = candidates[0]
    return (lang, kind)


# --------------------------------------------------------------------------
# VTT -> deduped "[mm:ss] text" lines
# --------------------------------------------------------------------------

_TIMING_RE = re.compile(
    r"^(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})"
)
_TAG_RE = re.compile(r"<[^>]*>")


def _ts_to_seconds(ts: str) -> float:
    h, m, s = ts.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def parse_vtt_cues(vtt_text: str) -> list[tuple[float, float, list[str]]]:
    """Parse a WEBVTT file into (start_s, end_s, [text_lines]) cues.

    Strips inline karaoke-style tags (<00:00:05.160><c>word</c>) and cue
    settings (align:start position:0%). Does not attempt full VTT spec
    compliance -- just enough to handle yt-dlp's manual and auto-caption
    output.
    """
    lines = vtt_text.splitlines()
    cues: list[tuple[float, float, list[str]]] = []
    i = 0
    n = len(lines)
    while i < n:
        m = _TIMING_RE.match(lines[i].strip())
        if not m:
            i += 1
            continue
        start_s = _ts_to_seconds(m.group(1))
        end_s = _ts_to_seconds(m.group(2))
        i += 1
        text_lines = []
        # A true cue-ending separator is an *exactly* empty line. YouTube's
        # rolling auto-captions use a single-space line (" ") as a deliberate
        # placeholder for "no text on this row yet" -- that is cue content,
        # not a separator, so we must not treat it as one by stripping first.
        while i < n and lines[i] != "":
            cleaned = _TAG_RE.sub("", lines[i]).strip()
            text_lines.append(cleaned)
            i += 1
        cues.append((start_s, end_s, text_lines))
        # skip the blank separator line(s)
        while i < n and lines[i] == "":
            i += 1
    return cues


def vtt_to_timestamped_lines(vtt_text: str) -> list[tuple[float, str]]:
    """Convert raw VTT text to a deduped list of (start_seconds, line).

    YouTube's rolling auto-captions repeat the previous line verbatim as a
    cue grows (two-line "top=finished, bottom=being-typed" windows). We
    flatten all cue text lines in order and drop a line if it is identical
    to the immediately preceding *emitted* line -- this collapses the
    rolling repeats while leaving genuinely new content (including
    legitimate repeated words that aren't adjacent) untouched.
    """
    cues = parse_vtt_cues(vtt_text)
    out: list[tuple[float, str]] = []
    last_line: str | None = None
    for start_s, _end_s, text_lines in cues:
        for line in text_lines:
            line = line.strip()
            if not line:
                continue
            if line == last_line:
                continue
            out.append((start_s, line))
            last_line = line
    return out


def format_mmss(seconds: float) -> str:
    total = int(round(seconds))
    mm, ss = divmod(total, 60)
    return f"{mm:02d}:{ss:02d}"


def lines_to_text(lines: list[tuple[float, str]]) -> str:
    return "\n".join(f"[{format_mmss(t)}] {text}" for t, text in lines)


# --------------------------------------------------------------------------
# Header block shared by both transcript sources
# --------------------------------------------------------------------------

def format_duration(seconds) -> str:
    if seconds is None:
        return "unknown"
    try:
        seconds = int(seconds)
    except (TypeError, ValueError):
        return str(seconds)
    return f"{seconds}s ({format_mmss(seconds)})"


def format_upload_date(upload_date) -> str:
    if not upload_date or len(str(upload_date)) != 8:
        return str(upload_date)
    s = str(upload_date)
    return f"{s[0:4]}-{s[4:6]}-{s[6:8]}"


def build_header(meta: dict, transcript_source: str, retrieved_date: str) -> str:
    rows = [
        f"Title: {meta.get('title')}",
        f"Channel: {meta.get('channel')}",
        f"Duration: {format_duration(meta.get('duration_seconds'))}",
        f"Upload date: {format_upload_date(meta.get('upload_date'))}",
        f"URL: {meta.get('url')}",
        f"Transcript source: {transcript_source}",
        f"Retrieved: {retrieved_date}",
        "-" * 60,
    ]
    return "\n".join(rows) + "\n\n"


def write_transcript_file(out_path: Path, meta: dict, transcript_source: str,
                           retrieved_date: str, body_text: str) -> None:
    header = build_header(meta, transcript_source, retrieved_date)
    out_path.write_text(header + body_text + "\n", encoding="utf-8")

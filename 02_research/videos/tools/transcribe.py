#!/usr/bin/env python
"""transcribe.py URL --out DIR [--max-min 40] [--model small] [--force-whisper]

1. Captions first (works for YouTube and anything yt-dlp's generic/other
   extractors expose subtitles for): download manual + auto subs in
   en*/he*/iw*, convert the best track to deduped "[mm:ss] text" lines.
2. No usable captions -> download audio only (to %TEMP%, deleted afterwards)
   and transcribe the first --max-min minutes with local Whisper
   (faster-whisper first, several interpreter/uv fallbacks per the brief).
3. Non-YouTube pages: no special-casing needed -- yt-dlp's generic extractor
   is simply tried first for whatever URL is given, exactly like YouTube.

Writes <out_dir>/<video_id>.txt with a header block (title, channel,
duration, upload date, url, transcript source, retrieved date) followed by
the transcript body. Prints a one-line JSON result summary to stdout.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path

from common import (
    fetch_metadata_json,
    lang_rank,
    lines_to_text,
    run_ytdlp,
    summarize_metadata,
    vtt_to_timestamped_lines,
    write_transcript_file,
)

TOOLS_DIR = Path(__file__).resolve().parent
WHISPER_SCRIPT = TOOLS_DIR / "transcribe_whisper.py"


# --------------------------------------------------------------------------
# Captions path
# --------------------------------------------------------------------------

def pick_downloaded_vtt(out_dir: Path, video_id: str, raw_meta: dict):
    """Among freshly-downloaded <video_id>.<lang>.vtt files, pick the best one.

    Returns (path, base_lang, kind) or None. kind is "manual" or "auto",
    determined by cross-referencing the lang against yt-dlp's metadata
    subtitles/automatic_captions dicts (the downloaded filename itself does
    not distinguish the two).
    """
    candidates = sorted(out_dir.glob(f"{video_id}.*.vtt"))
    if not candidates:
        return None

    subs = raw_meta.get("subtitles") or {}
    auto = raw_meta.get("automatic_captions") or {}

    def lang_of(p: Path) -> str:
        return p.name[len(video_id) + 1: -len(".vtt")]

    def score(p: Path):
        lang = lang_of(p)
        base_lang = lang[: -len("-orig")] if lang.endswith("-orig") else lang
        is_manual = (base_lang in subs) or (lang in subs)
        kind_rank = 0 if is_manual else 1
        orig_rank = 1 if lang.endswith("-orig") else 0  # prefer the plain variant
        return (lang_rank(base_lang)[0], kind_rank, orig_rank)

    candidates.sort(key=score)
    best = candidates[0]
    lang = lang_of(best)
    base_lang = lang[: -len("-orig")] if lang.endswith("-orig") else lang
    is_manual = (base_lang in subs) or (lang in subs)
    kind = "manual" if is_manual else "auto"
    return best, base_lang, kind


def try_captions(url: str, out_dir: Path, raw_meta: dict):
    video_id = raw_meta.get("id")
    r = run_ytdlp(
        [
            "--skip-download", "--write-subs", "--write-auto-subs",
            "--sub-langs", "en.*,he.*,iw.*", "--sub-format", "vtt",
            "-o", str(out_dir / "%(id)s.%(ext)s"), url,
        ],
        timeout=300,
    )
    if video_id is None:
        return None
    picked = pick_downloaded_vtt(out_dir, video_id, raw_meta)
    if not picked:
        print(f"[transcribe] caption download stderr tail:\n{r.stderr[-1000:]}", file=sys.stderr)
        return None
    vtt_path, lang, kind = picked
    vtt_text = vtt_path.read_text(encoding="utf-8", errors="replace")
    lines = vtt_to_timestamped_lines(vtt_text)
    if not lines:
        return None
    return lines, lang, kind, vtt_path


# --------------------------------------------------------------------------
# Whisper path: audio download + multi-interpreter fallback chain
# --------------------------------------------------------------------------

def download_audio_to_temp(url: str, video_id: str | None):
    tmp_dir = Path(tempfile.mkdtemp(prefix="reef_audio_"))
    out_tmpl = str(tmp_dir / "%(id)s.%(ext)s")
    r = run_ytdlp(["-f", "bestaudio", "-o", out_tmpl, url], timeout=600)
    if r.returncode != 0:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise RuntimeError(f"audio download failed (exit {r.returncode}):\n{r.stderr[-2000:]}")
    candidates = sorted(tmp_dir.iterdir())
    if not candidates:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise RuntimeError("yt-dlp reported success but no audio file was found in temp dir")
    return tmp_dir, candidates[0]


def find_py_launcher_versions() -> list[tuple[str, str]]:
    """Parse `py -0p` for other installed Python versions: [(ver, path), ...]."""
    try:
        r = subprocess.run(["py", "-0p"], capture_output=True, text=True, timeout=15)
    except Exception:
        return []
    out = []
    for line in r.stdout.splitlines():
        m = re.search(r"-V:(\d+\.\d+)(?:-\d+)?\s*\*?\s*(\S.*)$", line.strip())
        if m:
            out.append((m.group(1), m.group(2).strip()))
    return out


def try_pip_install(py_args: list[str], package: str) -> bool:
    cmd = list(py_args) + ["-m", "pip", "install", package]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except Exception:
        return False
    return r.returncode == 0


def run_whisper_via(py_args: list[str], audio_path: Path, max_min: float, model: str):
    cmd = list(py_args) + [str(WHISPER_SCRIPT), str(audio_path), "--max-min", str(max_min), "--model", model]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600)
    return cmd, r


def whisper_fallback_chain(audio_path: Path, max_min: float, model: str, attempts_log: list):
    current_ver = f"{sys.version_info.major}.{sys.version_info.minor}"

    # 1. current interpreter, as-is (this is the normal/fast path when
    #    faster-whisper or openai-whisper is already installed).
    cmd, r = run_whisper_via([sys.executable], audio_path, max_min, model)
    attempts_log.append({"cmd": cmd, "rc": r.returncode, "stderr_tail": r.stderr[-800:]})
    if r.returncode == 0:
        return json.loads(r.stdout), cmd

    # 2. try installing faster-whisper, then openai-whisper, on the current interpreter.
    for pkg in ("faster-whisper", "openai-whisper"):
        if try_pip_install([sys.executable], pkg):
            cmd, r = run_whisper_via([sys.executable], audio_path, max_min, model)
            attempts_log.append({"cmd": cmd, "rc": r.returncode, "stderr_tail": r.stderr[-800:]})
            if r.returncode == 0:
                return json.loads(r.stdout), cmd

    # 3. another installed Python via the `py` launcher (e.g. py -3.12).
    for ver, _path in find_py_launcher_versions():
        if ver == current_ver:
            continue
        py_args = ["py", f"-{ver}"]
        if try_pip_install(py_args, "faster-whisper"):
            cmd, r = run_whisper_via(py_args, audio_path, max_min, model)
            attempts_log.append({"cmd": cmd, "rc": r.returncode, "stderr_tail": r.stderr[-800:]})
            if r.returncode == 0:
                return json.loads(r.stdout), cmd

    # 4. pip install uv; uv run --python 3.12 --with faster-whisper python transcribe_whisper.py ...
    uv = shutil.which("uv")
    if not uv and try_pip_install([sys.executable], "uv"):
        uv = shutil.which("uv")
    if uv:
        cmd = [
            uv, "run", "--python", "3.12", "--with", "faster-whisper", "python",
            str(WHISPER_SCRIPT), str(audio_path), "--max-min", str(max_min), "--model", model,
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=3600)
        except Exception as exc:
            r = subprocess.CompletedProcess(cmd, 1, "", str(exc))
        attempts_log.append({"cmd": cmd, "rc": r.returncode, "stderr_tail": r.stderr[-800:]})
        if r.returncode == 0:
            return json.loads(r.stdout), cmd

    raise RuntimeError("All local-Whisper backends failed. Attempts:\n" + json.dumps(attempts_log, indent=2)[-4000:])


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url")
    ap.add_argument("--out", required=True, help="Output directory for <video_id>.txt (and caption .vtt files)")
    ap.add_argument("--max-min", type=float, default=40, help="Cap on minutes of audio sent to local Whisper")
    ap.add_argument("--model", default="small", help="Whisper model size (default: small)")
    ap.add_argument("--force-whisper", action="store_true",
                     help="Skip the captions path entirely and go straight to local Whisper (for testing)")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_meta = fetch_metadata_json(args.url)
    meta = summarize_metadata(args.url, raw_meta)
    video_id = raw_meta.get("id") or "video"
    retrieved = date.today().isoformat()
    txt_path = out_dir / f"{video_id}.txt"

    if not args.force_whisper:
        try:
            result = try_captions(args.url, out_dir, raw_meta)
        except Exception as exc:  # noqa: BLE001
            print(f"[transcribe] captions attempt raised: {exc}", file=sys.stderr)
            result = None
        if result:
            lines, lang, kind, vtt_path = result
            body = lines_to_text(lines)
            source = f"YouTube captions ({kind}, lang={lang})"
            write_transcript_file(txt_path, meta, source, retrieved, body)
            print(json.dumps({
                "ok": True, "path": str(txt_path), "source": source,
                "lines": len(lines), "vtt": str(vtt_path),
            }, ensure_ascii=False))
            return 0
        print("[transcribe] no usable captions found, falling back to local Whisper", file=sys.stderr)

    # ---- Whisper path ----
    t0 = datetime.now(timezone.utc)
    tmp_dir, audio_path = download_audio_to_temp(args.url, video_id)
    t_downloaded = datetime.now(timezone.utc)
    attempts: list = []
    try:
        result, used_cmd = whisper_fallback_chain(audio_path, args.max_min, args.model, attempts)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)  # delete the audio afterwards, always
    t_done = datetime.now(timezone.utc)

    segs = result.get("segments", [])
    lines = [(s["start"], s["text"]) for s in segs if s.get("text")]
    body = lines_to_text(lines)
    source = f"local Whisper {result.get('model')} (speech-to-text, may contain errors)"
    write_transcript_file(txt_path, meta, source, retrieved, body)
    print(json.dumps({
        "ok": True, "path": str(txt_path), "source": source, "lines": len(lines),
        "whisper_backend": result.get("backend"), "whisper_command": " ".join(used_cmd),
        "download_seconds": (t_downloaded - t0).total_seconds(),
        "transcribe_seconds": (t_done - t_downloaded).total_seconds(),
        "attempts": len(attempts),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

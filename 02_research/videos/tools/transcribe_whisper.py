#!/usr/bin/env python
"""Standalone local-Whisper backend: AUDIO_PATH -> JSON segments on stdout.

Deliberately dependency-light at import time (only argparse/json/sys) so this
file can be invoked by whichever Python interpreter actually has a working
faster-whisper / openai-whisper install -- including via:

    uv run --python 3.12 --with faster-whisper python transcribe_whisper.py AUDIO --max-min 40

transcribe.py (the orchestrator) shells out to this script rather than
importing it, so it can try several interpreters in turn without the whole
process dying because the *current* interpreter lacks a whisper package.

Output (stdout, on success): a JSON object
    {"backend": "faster-whisper"|"openai-whisper", "model": "small",
     "language": "en", "segments": [{"start": 0.0, "end": 2.3, "text": "..."}]}

Diagnostics go to stderr so stdout stays pure JSON.
"""
from __future__ import annotations

import argparse
import json
import sys


def _load_audio_array(audio_path: str, max_min: float | None, sr: int = 16000):
    """Decode audio to a mono float32 numpy array at `sr` Hz using PyAV.

    Only decodes up to max_min minutes of source audio (if given) -- this is
    what makes "--max-min" cheap rather than decoding+transcribing the whole
    file and discarding the tail.
    """
    import av
    import numpy as np

    max_samples = int(max_min * 60 * sr) if max_min else None

    container = av.open(audio_path)
    stream = container.streams.audio[0]
    resampler = av.audio.resampler.AudioResampler(format="s16", layout="mono", rate=sr)

    chunks = []
    total = 0
    for frame in container.decode(stream):
        for rframe in resampler.resample(frame):
            arr = rframe.to_ndarray()
            chunks.append(arr)
            total += arr.shape[-1]
        if max_samples and total >= max_samples:
            break
    container.close()

    if not chunks:
        return np.zeros(0, dtype=np.float32)

    data = np.concatenate(chunks, axis=-1).reshape(-1)
    data = data.astype(np.float32) / 32768.0
    if max_samples:
        data = data[:max_samples]
    return data


def run_faster_whisper(audio_path: str, max_min: float | None, model_size: str):
    from faster_whisper import WhisperModel

    print(f"[transcribe_whisper] loading faster-whisper model={model_size} device=cpu compute_type=int8",
          file=sys.stderr)
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    audio = _load_audio_array(audio_path, max_min, sr=16000)
    print(f"[transcribe_whisper] decoded {audio.shape[0] / 16000:.1f}s of audio", file=sys.stderr)

    segments_gen, info = model.transcribe(audio, vad_filter=True)
    segments = []
    for seg in segments_gen:
        segments.append({"start": seg.start, "end": seg.end, "text": seg.text.strip()})

    return {
        "backend": "faster-whisper",
        "model": model_size,
        "language": getattr(info, "language", None),
        "segments": segments,
    }


def run_openai_whisper(audio_path: str, max_min: float | None, model_size: str):
    import whisper

    print(f"[transcribe_whisper] loading openai-whisper model={model_size}", file=sys.stderr)
    model = whisper.load_model(model_size)

    audio = _load_audio_array(audio_path, max_min, sr=16000)
    result = model.transcribe(audio, fp16=False)

    segments = [
        {"start": s["start"], "end": s["end"], "text": s["text"].strip()}
        for s in result.get("segments", [])
    ]
    return {
        "backend": "openai-whisper",
        "model": model_size,
        "language": result.get("language"),
        "segments": segments,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("audio_path")
    ap.add_argument("--max-min", type=float, default=None,
                     help="Only decode/transcribe the first N minutes of audio")
    ap.add_argument("--model", default="small", help="Whisper model size (default: small)")
    args = ap.parse_args()

    try:
        try:
            result = run_faster_whisper(args.audio_path, args.max_min, args.model)
        except ImportError:
            print("[transcribe_whisper] faster-whisper not available, trying openai-whisper",
                  file=sys.stderr)
            result = run_openai_whisper(args.audio_path, args.max_min, args.model)
    except Exception as exc:  # noqa: BLE001
        print(f"[transcribe_whisper] FAILED: {exc!r}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

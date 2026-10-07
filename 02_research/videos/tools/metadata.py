#!/usr/bin/env python
"""metadata.py URL -> JSON metadata (title, channel, duration, captions?, ...).

Wraps: python -m yt_dlp --dump-single-json --skip-download

Usage:
    python metadata.py "https://www.youtube.com/watch?v=XXXXXXXXXXX"
    python metadata.py URL --pretty
"""
from __future__ import annotations

import argparse
import json
import sys

from common import get_metadata


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("url", help="Video (or video page) URL")
    ap.add_argument("--timeout", type=int, default=180, help="yt-dlp timeout in seconds")
    args = ap.parse_args()

    try:
        meta = get_metadata(args.url, timeout=args.timeout)
    except Exception as exc:  # noqa: BLE001 - surface as JSON error, not a traceback
        print(json.dumps({"error": str(exc), "url": args.url}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

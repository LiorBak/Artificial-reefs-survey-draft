#!/usr/bin/env python3
"""check_registry.py - integrity check of the per-reef image registry (03_images/reefs/<slug>/images.json).

Convention: _agent_briefs/image_registry.md ; overview: 03_images/reefs/README.md
Usage:   python check_registry.py            (from anywhere; paths are resolved relative to this file)
         python check_registry.py --table    (also print the per-reef counts as a markdown table)
         python check_registry.py --json     (print the summary JSON only)
Exit code 0 = no errors (warnings are allowed), 1 = at least one error.

Errors:   missing/unreadable images.json; duplicate or mis-prefixed ids; required fields missing or empty; bad kind / used_for value;
          file missing on disk or sha256/bytes mismatch; annotated_files / other_resolutions / duplicate_files / group_files missing;
          display true without a file; for_3d_check malformed; image26 or a Gemini-folder path registered; an image file under
          07_scale/shapes/*/src, 07_scale/shapes/*/3d/annotated, 07_scale/shapes/*/3d/src, 03_images/video_frames/<13 reefs>, or the
          reef's own 03_images/reefs/<slug>/ folder that is not registered; a row id without its section in IMAGES.md.
Warnings: overlays/ images not registered; rows with no image_url/source_page; PDFs and GeoTIFFs under src (source documents/data, not images).
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                  # .../03_images/reefs
ROOT = HERE.parent.parent                               # project root
SHAPES = ROOT / "07_scale" / "shapes"
FRAMES = ROOT / "03_images" / "video_frames"

SLUGS = ["narrowneck-gold-coast", "cables-reef-wa", "prattes-reef-el-segundo", "mount-maunganui-reef", "opunake-reef",
         "boscombe-surf-reef", "kovalam-reef-india", "borth-coastal-defence-reef", "palm-beach-gold-coast",
         "southern-ocean-surf-reef-albany", "burkitts-reef-bargara", "bunbury-airwave", "mexico-reef-2026-unnamed"]
KINDS = {"photo", "aerial", "satellite", "design_drawing", "plan_figure", "survey_plot", "cross_section", "chart_screenshot",
         "report_photo", "video_frame", "diagram"}
USED = {"plan_trace", "3d_seabed", "3d_crest", "3d_height_slopes", "3d_tides", "scale", "cross_check", "camera_match", "context", "not_used"}
KEYS_PRESENT = ["id", "file", "annotated_files", "kind", "title", "citation", "image_url", "source_page", "page_or_figure", "image_date",
                "credit", "license", "retrieved", "shows", "structure_visible", "state_shown", "used_for", "how_used", "linked_records",
                "bytes", "px", "sha256", "rights_note", "display", "for_3d_check", "added_by"]
NONEMPTY = ["id", "kind", "title", "citation", "image_date", "credit", "license", "retrieved", "shows", "state_shown", "used_for",
            "how_used", "added_by", "page_or_figure"]
IMG_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
DOC_EXT = {".pdf", ".tif", ".tiff"}


def norm(s):
    return str(s).replace("\\", "/")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def main():
    as_json = "--json" in sys.argv
    errors, warnings = [], []
    summary = {}
    all_registered = {}                                  # slug -> set of registered rel paths

    def err(slug, msg):
        errors.append("%s: %s" % (slug, msg))

    def warn(slug, msg):
        warnings.append("%s: %s" % (slug, msg))

    for slug in SLUGS:
        d = HERE / slug
        jp = d / "images.json"
        if not jp.exists():
            err(slug, "images.json missing")
            continue
        try:
            rows = json.loads(jp.read_text(encoding="utf-8"))
        except Exception as e:                           # truncated / invalid JSON
            err(slug, "images.json unreadable: %s" % e)
            continue
        if not isinstance(rows, list):
            err(slug, "images.json is not a list")
            continue
        reg = set()
        ids = set()
        n_dl = n_dead = n_model = 0
        for r in rows:
            rid = r.get("id", "?")
            if rid in ids:
                err(slug, "duplicate id %s" % rid)
            ids.add(rid)
            if not re.fullmatch(re.escape(slug) + r"-img-\d{2,}", str(rid)):
                err(slug, "%s: id is not '<slug>-img-NN'" % rid)
            for k in KEYS_PRESENT:
                if k not in r:
                    err(slug, "%s: field '%s' missing" % (rid, k))
            for k in NONEMPTY:
                if k in r and r[k] in (None, "", []):
                    err(slug, "%s: field '%s' empty" % (rid, k))
            if r.get("kind") not in KINDS:
                err(slug, "%s: bad kind %r" % (rid, r.get("kind")))
            uf = r.get("used_for")
            if not isinstance(uf, list) or not set(uf) <= USED:
                err(slug, "%s: bad used_for %r" % (rid, uf))
            for k in ("structure_visible", "display"):
                if k in r and not isinstance(r[k], bool):
                    err(slug, "%s: '%s' must be true/false" % (rid, k))
            f3 = r.get("for_3d_check")
            if not (isinstance(f3, dict) and isinstance(f3.get("pending"), bool) and "what_to_check" in f3 and "model_values_affected" in f3):
                err(slug, "%s: for_3d_check must be {pending: bool, what_to_check, model_values_affected}" % rid)
            if not r.get("image_url") and not r.get("source_page"):
                warn(slug, "%s: neither image_url nor source_page" % rid)
            # files
            fl = r.get("file")
            if fl:
                fl = norm(fl)
                reg.add(fl)
                p = ROOT / fl
                if "image26" in fl:
                    err(slug, "%s: image26 must never be registered" % rid)
                if "Gemini" in fl or "/AG/" in fl:
                    err(slug, "%s: file points into the Gemini folder" % rid)
                if not p.exists():
                    err(slug, "%s: file missing on disk: %s" % (rid, fl))
                else:
                    if r.get("sha256") and sha256(p) != r["sha256"]:
                        err(slug, "%s: sha256 mismatch for %s" % (rid, fl))
                    if r.get("bytes") not in (None, p.stat().st_size):
                        err(slug, "%s: bytes mismatch for %s" % (rid, fl))
                    if fl.startswith("03_images/reefs/") and "/video_frames/" not in fl:
                        n_dl += 1
            else:
                n_dead += 1
                if r.get("display") is True:
                    err(slug, "%s: display is true but there is no file" % rid)
            for k in ("annotated_files", "other_resolutions", "duplicate_files", "group_files"):
                for a in r.get(k) or []:
                    a = norm(a)
                    reg.add(a)
                    if not (ROOT / a).exists():
                        err(slug, "%s: %s entry missing on disk: %s" % (rid, k, a))
            for a, sh in (r.get("group_sha256") or {}).items():
                if (ROOT / norm(a)).exists() and sha256(ROOT / norm(a)) != sh:
                    err(slug, "%s: group sha256 mismatch for %s" % (rid, a))
            if set(uf or []) - {"context", "not_used"}:
                n_model += 1
        # IMAGES.md has a section per id
        md = d / "IMAGES.md"
        if not md.exists():
            err(slug, "IMAGES.md missing")
        else:
            t = md.read_text(encoding="utf-8")
            for rid in ids:
                if "## %s " % rid not in t and "## %s\n" % rid not in t:
                    err(slug, "IMAGES.md has no section for %s" % rid)
        # orphan files in the reef's own folder
        for p in sorted(d.iterdir()):
            if p.is_file() and p.suffix.lower() in IMG_EXT and norm(p.relative_to(ROOT)) not in reg:
                err(slug, "orphan image in the registry folder (not registered): %s" % norm(p.relative_to(ROOT)))
        all_registered[slug] = reg
        summary[slug] = {"registered": len(rows), "downloaded": n_dl, "dead": n_dead, "used_for_model": n_model,
                         "displayed": sum(1 for r in rows if r.get("display") is True),
                         "pending_3d_checks": sum(1 for r in rows if isinstance(r.get("for_3d_check"), dict) and r["for_3d_check"].get("pending") is True)}
        # coverage of task folders
        base = SHAPES / slug
        for sub, strict in (("src", True), ("3d/annotated", True), ("3d/src", True), ("overlays", False)):
            dd = base / sub
            if not dd.exists():
                continue
            for p in sorted(dd.rglob("*")):
                if not p.is_file():
                    continue
                rel = norm(p.relative_to(ROOT))
                if p.suffix.lower() in IMG_EXT:
                    if rel not in reg:
                        (err if strict else warn)(slug, "%s not registered" % rel)
                elif p.suffix.lower() in DOC_EXT and sub != "overlays":
                    pass                                   # source documents / DEM data: not images (referenced through source_pdf)
        fd = FRAMES / slug
        if fd.exists():
            for p in sorted(fd.rglob("*")):
                if p.is_file() and p.suffix.lower() in IMG_EXT and norm(p.relative_to(ROOT)) not in reg:
                    err(slug, "video frame not registered: %s" % norm(p.relative_to(ROOT)))
    for p in sorted(HERE.iterdir()):
        if p.is_dir() and p.name not in SLUGS:
            warnings.append("unexpected folder in 03_images/reefs: %s" % p.name)

    result = {"reefs": summary, "check_passed": not errors, "issues": errors[:200], "warnings": len(warnings)}
    if as_json:
        print(json.dumps(result, indent=1))
    else:
        print("Image registry check (%s)" % HERE)
        tot = {"registered": 0, "downloaded": 0, "dead": 0, "used_for_model": 0, "displayed": 0, "pending_3d_checks": 0}
        for slug in SLUGS:
            s = summary.get(slug)
            if not s:
                print("  %-34s MISSING" % slug)
                continue
            for k in tot:
                tot[k] += s[k]
            print("  %-34s registered %3d  downloaded %3d  dead %d  used_for_model %3d  displayed %3d  pending_3d %3d" %
                  (slug, s["registered"], s["downloaded"], s["dead"], s["used_for_model"], s["displayed"], s["pending_3d_checks"]))
        print("  %-34s registered %3d  downloaded %3d  dead %d  used_for_model %3d  displayed %3d  pending_3d %3d" %
              ("TOTAL", tot["registered"], tot["downloaded"], tot["dead"], tot["used_for_model"], tot["displayed"], tot["pending_3d_checks"]))
        if "--table" in sys.argv:
            print("\n| reef | registered | downloaded | dead | used for model | displayed | 3D checks pending |\n|---|---|---|---|---|---|---|")
            for slug in SLUGS:
                s = summary.get(slug)
                if s:
                    print("| %s | %d | %d | %d | %d | %d | %d |" % (slug, s["registered"], s["downloaded"], s["dead"], s["used_for_model"], s["displayed"], s["pending_3d_checks"]))
            print("| **total** | %d | %d | %d | %d | %d | %d |" % (tot["registered"], tot["downloaded"], tot["dead"], tot["used_for_model"], tot["displayed"], tot["pending_3d_checks"]))
        for w in warnings[:60]:
            print("  WARNING", w)
        if len(warnings) > 60:
            print("  ... %d more warnings" % (len(warnings) - 60))
        for e in errors[:200]:
            print("  ERROR", e)
        print("RESULT:", "PASSED" if not errors else "FAILED (%d errors)" % len(errors))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

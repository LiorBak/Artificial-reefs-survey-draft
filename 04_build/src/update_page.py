"""update_page.py - ONE command that brings artificial_reefs.html up to date after any input changed (round 11).

    python src/update_page.py              # detect -> backup -> compile_data -> build (copies viewers, re-exports changed meshes, photo match) -> check.py -> summary
    python src/update_page.py --fast       # same, check.py without the Chrome part (5 s instead of 90 s)
    python src/update_page.py --full       # + qa_models3d.py (all DOM checks incl. round-11: panels, labels, scale bar, photo match) + screenshots QA/<prefix>_*.png
    python src/update_page.py --prefix NAME --force-export --dry

What it does (see UPDATE_PROTOCOL.md for the human steps around it):
  1. DETECT   signature per model of every input (07_scale/shapes/<slug>/3d viewer + model.js + docs.js + annotated/, shape.json, 03_images registry,
              02_research card, its entries in data/models3d_*.json) and of src/ ; compared with data/update_state.json (written after a clean run).
  2. BACKUP   the current page -> QA/prev/last_update/artificial_reefs.html (one rolling copy: roll back by copying it back).
  3. BUILD    compile_data.py, then build.py = compile_models3d (re-copies viewers + pictures, prunes stale copies, photo_match.ensure, re-exports ONLY the
              combined meshes whose signature changed, curated tokens read from model.js) + page inlining.
  4. CHECK    check.py (static + [3D] + Chrome DOM; --fast skips Chrome).
  5. SUMMARY  what changed, what was re-exported, numbers that moved since the last update, warnings (new model without combined / curated entries ...).
Exit code 1 when the build or a check fails. Never writes to 07_scale, 03_images or 02_research.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
ROOT = BUILD.parent
SHAPES = ROOT / "07_scale" / "shapes"
REGS = ROOT / "03_images" / "reefs"
CARDS = ROOT / "02_research" / "reefs"
DATA = BUILD / "data"
QA = BUILD / "QA"
PAGE = BUILD / "artificial_reefs.html"
STATE = DATA / "update_state.json"
PY = sys.executable


def sha(*chunks: bytes) -> str:
    h = hashlib.sha256()
    for c in chunks:
        h.update(c)
    return h.hexdigest()[:16]


def fbytes(p: Path) -> bytes:
    return p.read_bytes() if p.is_file() else b"-"


def dir_stamp(p: Path) -> bytes:
    """name + size + mtime of every file below p (annotated images: fast, content hash not needed)."""
    if not p.is_dir():
        return b"-"
    return "|".join(f"{f.relative_to(p).as_posix()}:{f.stat().st_size}:{f.stat().st_mtime_ns}" for f in sorted(p.rglob("*")) if f.is_file()).encode()


def jslice(path: Path, slug: str) -> bytes:
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return b"-"
    if "rows" in d:
        d = [r for r in d["rows"] if r.get("slug") == slug]
    elif "models" in d:
        d = d["models"].get(slug)
    return json.dumps(d, sort_keys=True).encode()


def model_slugs() -> list[str]:
    return sorted(p.name for p in SHAPES.iterdir() if (p / "3d" / "index.html").is_file() and (p / "3d" / "model.js").is_file())


def signatures() -> dict:
    out: dict = {"models": {}}
    for s in model_slugs():
        d3 = SHAPES / s / "3d"
        parts = {
            "viewer": sha(fbytes(d3 / "index.html"), fbytes(d3 / "docs.js")),
            "model.js": sha(fbytes(d3 / "model.js")),
            "annotated": sha(dir_stamp(d3 / "annotated")),
            "shape.json": sha(fbytes(SHAPES / s / "shape.json")),
            "registry": sha(fbytes(REGS / s / "images.json")),
            "card": sha(fbytes(CARDS / f"{s}.json")),
            "config": sha(*(jslice(DATA / f"models3d_{k}.json", s) for k in ("combined", "curated", "caveats"))),
        }
        out["models"][s] = parts
    out["hold"] = sha(fbytes(DATA / "models3d_hold.json"))
    srcs = [f for f in sorted(HERE.iterdir()) if f.suffix in (".py", ".js", ".css", ".html")]
    out["src"] = sha(*(fbytes(f) for f in srcs), fbytes(BUILD / "src" / "template.html"))
    return out


def run(cmd: list[str], title: str, env_extra: dict | None = None, quiet: bool = False) -> tuple[int, str]:
    env = dict(os.environ, PYTHONIOENCODING="utf-8", **(env_extra or {}))
    t0 = time.time()
    p = subprocess.run(cmd, cwd=str(BUILD), env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out = (p.stdout or "") + (p.stderr or "")
    if not quiet:
        print(f"  [{time.time() - t0:5.1f} s] {title}: exit {p.returncode}")
    return p.returncode, out


def snapshot() -> dict:
    """Numbers worth comparing between two updates, read from the built data3d."""
    try:
        d = json.loads((DATA / "models3d.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    comb = {c["slug"]: c for c in d.get("combined", {}).get("models", [])}
    snap = {}
    for m in d.get("models", []):
        c = comb.get(m["slug"], {})
        snap[m["slug"]] = {
            "default_version": m.get("default_version"),
            "versions": {v["id"]: {"area_m2": v.get("area_m2"), "volume_m3": v.get("volume_m3")} for v in (m.get("versions") or [])},
            "key_numbers": {k["q"]: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", str(k.get("model", ""))))[:140] for k in (m.get("key_numbers") or [])},
            "pictures": len(m.get("gallery") or []),
            "match_buttons": sum(1 for g in (m.get("gallery") or []) if g.get("match")),
            "combined": {"status": c.get("status"), "ok": c.get("ok"), "area_m2": c.get("area_m2"), "crest_z_m": c.get("crest_z_m")},
        }
    return snap


def diff_snapshots(old: dict, new: dict) -> list[str]:
    lines = []
    for s, n in new.items():
        o = old.get(s)
        if o is None:
            lines.append(f"{s}: NEW model ({len(n['versions'])} version(s), {n['pictures']} pictures, {n['match_buttons']} photo-match buttons)")
            continue
        if o.get("default_version") != n["default_version"]:
            lines.append(f"{s}: default version {o.get('default_version')} -> {n['default_version']}")
        for vid, vn in n["versions"].items():
            vo = (o.get("versions") or {}).get(vid)
            if vo is None:
                lines.append(f"{s}: version {vid} added (area {vn['area_m2']}, volume {vn['volume_m3']})")
            else:
                for k in ("area_m2", "volume_m3"):
                    if vo.get(k) != vn.get(k):
                        lines.append(f"{s}: version {vid} {k} {vo.get(k)} -> {vn.get(k)}")
        for q, t in n["key_numbers"].items():
            if (o.get("key_numbers") or {}).get(q) not in (None, t):
                lines.append(f"{s}: key number '{q[:40]}' now: {t[:90]}")
        if o.get("pictures") != n["pictures"]:
            lines.append(f"{s}: pictures {o.get('pictures')} -> {n['pictures']}")
        if o.get("match_buttons") != n["match_buttons"]:
            lines.append(f"{s}: photo-match buttons {o.get('match_buttons')} -> {n['match_buttons']}")
        co, cn = o.get("combined") or {}, n["combined"]
        for k in ("status", "ok", "area_m2", "crest_z_m"):
            if co.get(k) != cn.get(k):
                lines.append(f"{s}: combined scene {k} {co.get(k)} -> {cn.get(k)}")
    for s in old:
        if s not in new:
            lines.append(f"{s}: no longer on the page")
    return lines


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="One-command refresh of artificial_reefs.html")
    ap.add_argument("--full", action="store_true", help="also run qa_models3d.py (all DOM checks + screenshots)")
    ap.add_argument("--fast", action="store_true", help="check.py without the Chrome part")
    ap.add_argument("--prefix", default="update", help="screenshot prefix for --full (QA/<prefix>_*.png)")
    ap.add_argument("--force-export", action="store_true", help="re-export every combined mesh (ignore the signature cache)")
    ap.add_argument("--dry", action="store_true", help="only detect and print what would be rebuilt")
    a = ap.parse_args()
    t0 = time.time()
    stamp = time.strftime("%Y-%m-%d %H:%M")
    print(f"update_page {stamp}")

    # 1. detect
    sig_new = signatures()
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        state = {}
    old_sig = state.get("sig") or {}
    changed = []
    for s, parts in sig_new["models"].items():
        o = (old_sig.get("models") or {}).get(s)
        if o is None:
            changed.append((s, "NEW (no previous state)"))
        else:
            ch = [k for k, v in parts.items() if o.get(k) != v]
            if ch:
                changed.append((s, ", ".join(ch)))
    gone = [s for s in (old_sig.get("models") or {}) if s not in sig_new["models"]]
    other = [k for k in ("hold", "src") if old_sig.get(k) != sig_new[k]]
    print("1 detect: " + ("; ".join(f"{s} [{why}]" for s, why in changed) if changed else "no model input changed") +
          (f"; REMOVED {gone}" if gone else "") + (f"; also changed: {', '.join(other)}" if other else "") + ("" if state else "  (first run: no previous state)"))
    if a.dry:
        return 0

    # 2. backup
    bdir = QA / "prev" / "last_update"
    bdir.mkdir(parents=True, exist_ok=True)
    if PAGE.is_file():
        shutil.copyfile(PAGE, bdir / "artificial_reefs.html")
        (bdir / "WHEN.txt").write_text(f"page as it was before the update of {stamp}\n", encoding="utf-8")
    size_before = PAGE.stat().st_size if PAGE.is_file() else 0
    print(f"2 backup: QA/prev/last_update/artificial_reefs.html ({size_before // 1024} KB)")

    # 3. build
    if a.force_export:
        try:
            (BUILD / "3d" / "combined" / "export_cache.json").unlink()
        except OSError:
            pass
    rc, out = run([PY, str(HERE / "compile_data.py")], "3a compile_data.py")
    if rc:
        print(out[-1500:])
        print("FAILED at compile_data.py")
        return 1
    rc, bout = run([PY, str(HERE / "build.py")], "3b build.py (viewers, meshes, photo match, page)")
    (QA / "build_log.txt").write_text(bout, encoding="utf-8")
    if rc:
        print(bout[-2500:])
        print("FAILED at build.py: nothing else was run (the previous page is in QA/prev/last_update/)")
        return 1
    exported = re.findall(r"combined: ([\w-]+): (?!cached)\w+ ok=\S+ \((\d+) s\)", bout)
    cached = re.findall(r"combined: ([\w-]+): cached", bout)
    pm = "photo-match transforms recomputed" if "photo_match: recomputed" in bout else "photo-match transforms unchanged"
    pruned = re.findall(r"pruned stale generated copy (\S+)", bout)
    m = re.search(r"models3d: (\d+) models.*?verify (\d+) checked, (\d+) failed", bout)
    notes = [ln for ln in bout.splitlines() if ln.startswith("NOTE:") and "not on map" not in ln][:12]
    warns = [ln for ln in bout.splitlines() if re.search(r"VERIFY|FAIL|HELD|no combined|not in the vendored|unresolved", ln)]
    print(f"3 build: {m.group(1) + ' models' if m else '?'}; text snippets verified {m.group(2) if m else '?'}, failed {m.group(3) if m else '?'}; "
          f"re-exported meshes: {', '.join(s for s, _ in exported) or 'none'}; cached: {len(cached)}; {pm}; pruned {len(pruned)} stale picture copies")

    # 4. check
    rc_check, cout = run([PY, str(HERE / "check.py")] + (["--no-dom"] if a.fast else []), "4 check.py" + (" --no-dom" if a.fast else ""))
    fails = [ln for ln in cout.splitlines() if ln.startswith("FAIL")]
    nfail = re.search(r"(\d+) failure\(s\)", cout)
    print(f"4 check: {nfail.group(1) if nfail else '?'} failure(s)" + ("".join("\n    " + f[:200] for f in fails[:10]) if fails else ""))

    # 5. full QA
    qa_msg = ""
    rc_qa = 0
    if a.full:
        rc_qa, qout = run([PY, str(HERE / "qa_models3d.py"), "--prefix", a.prefix], f"5 qa_models3d.py --prefix {a.prefix}")
        npass = sum(1 for ln in qout.splitlines() if ln.startswith("PASS"))
        bad = [ln for ln in qout.splitlines() if ln.startswith("FAIL")]
        shots = sorted(f.name for f in QA.glob(f"{a.prefix}_*.png"))
        qa_msg = (f"5 qa_models3d: {npass} passed, {len(bad)} failed; {len(shots)} screenshots QA/{a.prefix}_*.png (report QA/{a.prefix}_checks.txt)"
                  + "".join("\n    " + x[:200] for x in bad[:10]))
        print(qa_msg)

    # 6. summary
    snap = snapshot()
    delta = diff_snapshots(state.get("snapshot") or {}, snap)
    ok = rc_check == 0 and rc_qa == 0
    if ok:
        STATE.write_text(json.dumps({"updated": stamp, "sig": sig_new, "snapshot": snap}, indent=1), encoding="utf-8")
    size_after = PAGE.stat().st_size
    comb_bad = [s for s, n in snap.items() if n["combined"].get("status") != "ok" or not n["combined"].get("ok")]
    print("\n== SUMMARY ==")
    print(f"page {size_after // 1024} KB (was {size_before // 1024} KB); {len(snap)} models on the page; combined scene OK for {len(snap) - len(comb_bad)}/{len(snap)}"
          + (f" (NOT ok: {', '.join(comb_bad)})" if comb_bad else "") + f"; photo-match buttons {sum(n['match_buttons'] for n in snap.values())}; pictures {sum(n['pictures'] for n in snap.values())}")
    if delta:
        print("changed since the last update:")
        for ln in delta[:25]:
            print("  - " + ln)
        if len(delta) > 25:
            print(f"  ... and {len(delta) - 25} more")
    else:
        print("no model number changed since the last update")
    try:
        cfg_slugs = set(json.loads((DATA / "models3d_combined.json").read_text(encoding="utf-8"))["models"])
        cur_slugs = set(json.loads((DATA / "models3d_curated.json").read_text(encoding="utf-8"))["models"])
        for s in snap:
            miss = [n for n, have in (("combined entry", s in cfg_slugs), ("curated key numbers", s in cur_slugs)) if not have]
            if miss:
                print(f"  ! {s}: missing {', '.join(miss)} (UPDATE_PROTOCOL.md, 'new model')")
    except (OSError, ValueError, KeyError):
        pass
    for ln in (warns + notes)[:8]:
        print("  note: " + ln[:200])
    print(f"state {'saved' if ok else 'NOT saved (a check failed: fix, then run again)'}; {time.time() - t0:.0f} s; log QA/build_log.txt, report QA/build_check.txt")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

"""Test of the outline-VERSIONS feature of the 3D tab with a SYNTHETIC model (build_3d_tab.md 2b).

    python src/qa_versions_synth.py [--prefix round9_3d] [--keep]

Nothing in the project is touched except QA/<prefix>_versions_*.png and QA/<prefix>_versions_checks.txt: the script builds a SANDBOX copy of
04_build in %TEMP%\\m3d_synth (src, data, 3d/vendor, a fake 07_scale/shapes/synthetic-versions-reef/3d model with 3 versions, a fake image
registry, and read-only junctions to the real prattes model so the page also has a model WITHOUT versions), runs the sandbox build.py, opens
the page in our own headless Chrome (src/qa_cdp.py) and checks: toggle names + dates, default shown, (i) dialog (versions_info + table
name|date|source|footprint|volume), key-numbers rows follow the toggle, the iframe gets #version=<id> initially and on every switch
(hash) AND the postMessage {type:"m3d-version", version}, automatic caveat rows for the version differences, no toggle for models without
versions. The synthetic viewer implements the contract a real viewer must keep (see 04_build/HANDOFF.md section 6) and reports back to the
parent with postMessage {type:"m3d-viewer-version", version, via}. Real Borth / Mount Maunganui models are NOT involved.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
ROOT = BUILD.parent
QA = BUILD / "QA"
SLUG = "synthetic-versions-reef"
sys.path.insert(0, str(HERE))

VIEWER = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Synthetic versions viewer</title>
<style>body{margin:0;font:16px system-ui;background:#10161c;color:#eaf0f5;display:grid;place-items:center;height:100vh}
#box{background:#1c2a36;border:3px solid #4aa3d6;height:120px;transition:width .2s;display:grid;place-items:center}</style></head>
<body><div><h2 id="t">version: ?</h2><div id="box"></div><p id="via"></p></div>
<script src="model.js"></script>
<script>
// contract: initial #version=<id>, hashchange, postMessage {type:'m3d-version', version}; a viewer that switches live announces it (round 11): the page then does not re-load it
window.M3D_HANDLES_VERSION = true;
try { parent.postMessage({type: 'm3d-viewer-caps', handlesVersion: true}, '*'); } catch (e) {}
var WIDTH = {a: 420, b: 300, c: 200};
function apply(v, via) {
  if (!v) return;
  document.getElementById('t').textContent = 'version: ' + v;
  document.getElementById('box').style.width = (WIDTH[v] || 100) + 'px';
  document.getElementById('via').textContent = 'via ' + via;
  try { parent.postMessage({type: 'm3d-viewer-version', version: v, via: via}, '*'); } catch (e) {}
}
function fromHash() { var m = /version=([^&]+)/.exec(location.hash); return m ? decodeURIComponent(m[1]) : null; }
apply(fromHash() || (window.REEF_MODEL && window.REEF_MODEL.default_version), 'initial');
window.addEventListener('hashchange', function () { apply(fromHash(), 'hash'); });
window.addEventListener('message', function (e) { if (e.data && e.data.type === 'm3d-version') apply(e.data.version, 'postMessage'); });
</script></body></html>
"""

MODEL = {
    "name": "Synthetic versions reef (test)",
    "confidence_3d": {"level": "medium", "reason": "Synthetic test model used only to test the outline-versions feature; it does not describe a real reef."},
    "state_label": "Synthetic as-built state, 2020 (test data)",
    "caption": "synthetic",
    "provenance": [
        {"parameter": "Crest level", "value": -1.2, "unit": "m MSL", "source_id": "S1", "method": "test", "uncertainty": "n/a", "estimated": False},
        {"parameter": "Reef volume", "value": 1000, "unit": "m3", "source_id": "S1", "method": "test", "uncertainty": "n/a", "estimated": False},
    ],
    "sources": [
        {"id": "S1", "citation": "Test Authority (2020) Synthetic design drawing 1. Not a real document.", "url": "https://example.org/s1"},
        {"id": "S2", "citation": "Test Survey Ltd (2022) Synthetic laser survey. Not a real document.", "url": "https://example.org/s2"},
        {"id": "S3", "citation": "Test Photos (2024) Synthetic aerial photo. Not a real document.", "url": "https://example.org/s3"},
    ],
    "water": {"levels": [{"key": "MSL", "z": 0.0, "label": "mean sea level", "source": "S1"}, {"key": "HAT", "z": 1.1, "label": "highest astronomical tide", "source": "S1"}]},
    "default_version": "b",
    "versions_info": "Three outline versions of the same synthetic reef: the design drawing (a), a laser survey (b) and a photo trace (c). The default is the survey.\n\nThis paragraph checks that a second paragraph of versions_info is rendered and that *italic* markers survive.",
    "versions": [
        {"id": "a", "name": "Design rock-layer foot (drawing, 2020)", "date": "2020-01-15", "source_ids": ["S1"], "method": "Digitised from the design drawing.",
         "level": "design armour foot", "kind": "design_drawing", "area_m2": 8000, "volume_m3": 1000, "bbox_m": [140, 70], "stated": {"area": "8,000 m2 (S1, nominal)"}},
        {"id": "b", "name": "Laser survey edge (LiDAR, 2022)", "date": "2022-03-19", "source_ids": ["S2"], "method": "Traced on the laser DSM.",
         "level": "rock exposed above -2.3 m MSL", "kind": "laser_survey", "area_m2": 9500, "volume_m3": 1250, "bbox_m": [150, 80]},
        {"id": "c", "name": "Visible rock edge (aerial photo, 2024)", "date": "2024-07-02", "source_ids": ["S3", "S1"], "method": "Traced on the photo.",
         "level": "visible rock in the photo", "kind": "photo_trace", "area_m2": 6200, "bbox_m": [130, 60]},
    ],
}

METHODS = """# Methods (synthetic)

## 1 Summary
Synthetic test model.

## 7 Limitations
| Unknown | Bias | What would resolve it |
|---|---|---|
| Everything | n/a | nothing, it is a test |

## 8 References
- Test Authority (2020) *Synthetic design drawing 1*. Not a real document.
"""


def mklink_junction(link: Path, target: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True)


def build_sandbox(sb: Path) -> Path:
    if sb.exists():
        # remove junction links first, without following them (never delete the real folders behind them)
        for link in [sb / "07_scale" / "shapes" / "prattes-reef-el-segundo", sb / "03_images" / "reefs" / "prattes-reef-el-segundo", sb / "07_scale" / "bathymetry"]:
            if link.exists():
                os.rmdir(link)
        shutil.rmtree(sb, ignore_errors=True)
    b = sb / "04_build"
    (b / "src").mkdir(parents=True)
    for f in HERE.glob("*"):
        if f.suffix in (".py", ".js", ".css", ".html"):
            shutil.copyfile(f, b / "src" / f.name)
    (b / "data").mkdir()
    for n in ("reefs.json", "models3d_caveats.json", "models3d_combined.json"):
        shutil.copyfile(BUILD / "data" / n, b / "data" / n)
    shutil.copytree(BUILD / "data" / "models3d_text", b / "data" / "models3d_text")
    cur = json.loads((BUILD / "data" / "models3d_curated.json").read_text(encoding="utf-8"))
    cur["models"][SLUG] = {
        "state_short": "Synthetic reef, as built 2020 (test)", "ve_note": "Synthetic: no vertical exaggeration.", "confidence_short": "Synthetic test model.",
        "key_numbers": [
            {"q": "Crest level", "model": "-1.2 m MSL", "stated": "-1.0 m MSL (S1)", "diff": "-0.2 m", "ids": "S1", "note": "applies to every version", "ev": []},
            {"q": "Volume (design only)", "model": "1,000 m3", "stated": "1,000 m3 (S1)", "diff": "0", "ids": "S1", "versions": ["a"], "ev": []},
            {"q": "Toe depth", "model": "-4.0 m MSL", "stated": "-", "diff": "-", "ids": "S2", "by_version": {"c": {"model": "-3.5 m MSL (photo version)", "note": "override for version c"}}, "ev": []},
        ],
        "relied": [],
    }
    (b / "data" / "models3d_curated.json").write_text(json.dumps(cur, ensure_ascii=False, indent=1), encoding="utf-8")
    shutil.copytree(BUILD / "3d" / "vendor", b / "3d" / "vendor")
    d3 = sb / "07_scale" / "shapes" / SLUG / "3d"
    d3.mkdir(parents=True)
    (d3 / "index.html").write_text(VIEWER, encoding="utf-8")
    (d3 / "model.js").write_text("window.REEF_MODEL = " + json.dumps(MODEL, indent=1) + ";\n", encoding="utf-8")
    (d3 / "METHODS_3D.md").write_text(METHODS, encoding="utf-8")
    # fake registry with two pictures
    from PIL import Image, ImageDraw  # noqa: PLC0415
    reg = sb / "03_images" / "reefs" / SLUG
    (reg / "files").mkdir(parents=True)
    rows = []
    for i, col in enumerate(((60, 120, 180), (200, 150, 60)), 1):
        im = Image.new("RGB", (800, 500), col)
        ImageDraw.Draw(im).text((20, 20), f"synthetic picture {i}", fill=(255, 255, 255))
        fn = f"03_images/reefs/{SLUG}/files/img-{i:02d}.png"
        im.save(reg / "files" / f"img-{i:02d}.png")
        rows.append({"id": f"img-{i:02d}", "file": fn, "display": True, "title": f"Synthetic picture {i}", "used_for": ["plan_trace"], "how_used": "Synthetic test picture.",
                     "citation": "Synthetic (2026) test picture, not a real source.", "credit": "none", "license": "none", "image_date": "2026-10-06",
                     "shows": "a coloured rectangle", "kind": "test", "linked_records": ["3d/SOURCES_3D.md"]})
    (reg / "images.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    # a real model WITHOUT versions for contrast (read-only junctions to the project)
    mklink_junction(sb / "07_scale" / "shapes" / "prattes-reef-el-segundo", ROOT / "07_scale" / "shapes" / "prattes-reef-el-segundo")
    mklink_junction(sb / "03_images" / "reefs" / "prattes-reef-el-segundo", ROOT / "03_images" / "reefs" / "prattes-reef-el-segundo")
    mklink_junction(sb / "07_scale" / "bathymetry", ROOT / "07_scale" / "bathymetry")
    return b


def cleanup(sb: Path) -> None:
    for link in [sb / "07_scale" / "shapes" / "prattes-reef-el-segundo", sb / "03_images" / "reefs" / "prattes-reef-el-segundo", sb / "07_scale" / "bathymetry"]:
        if link.exists():
            os.rmdir(link)
    shutil.rmtree(sb, ignore_errors=True)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="round9_3d")
    ap.add_argument("--keep", action="store_true", help="keep the sandbox in the temp folder")
    a = ap.parse_args()
    sb = Path(tempfile.gettempdir()) / "m3d_synth"
    b = build_sandbox(sb)
    r = subprocess.run([sys.executable, str(b / "src" / "build.py")], cwd=str(b), capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("\n".join(r.stdout.strip().splitlines()[-3:]))
    if r.returncode != 0:
        print(r.stderr[-1500:])
        return 2
    # check.py's [3D] block on the sandbox (the other blocks of check.py do not apply to a sandbox: only [3D] lines are judged)
    r2 = subprocess.run([sys.executable, str(b / "src" / "check.py"), "--no-dom"], cwd=str(b), capture_output=True, text=True, encoding="utf-8", errors="replace")
    f3d = [ln for ln in r2.stdout.splitlines() if ln.startswith("FAIL [3D]")]
    ver_line = [ln for ln in r2.stdout.splitlines() if "outline-version contract" in ln]
    from qa_cdp import Chrome  # noqa: PLC0415
    page = b / "artificial_reefs.html"
    res: dict[str, object] = {}
    shots: list[str] = []
    prefix = a.prefix + "_versions"

    def shot(c, name, **kw):
        p = QA / f"{prefix}_{name}.png"
        c.screenshot(p, **kw)
        shots.append(p.name)

    def js(c, e):
        return c.eval(e)

    sel = f'section.m3d-model[data-slug="{SLUG}"]'
    res["check.py [3D] block passes on the sandbox"] = (not f3d) or str(f3d[:3])
    res["check.py versions contract was exercised (1 model with versions)"] = bool(ver_line) and "1 model(s) with versions" in ver_line[0]
    with Chrome(1440, 900) as c:
        c.set_color_scheme("light")
        c.goto(page.as_uri() + "#view/models3d", 3)
        c.eval("document.documentElement.style.scrollBehavior='auto'")
        c.eval("window.__vlog=[];window.addEventListener('message',function(e){if(e.data&&e.data.type==='m3d-viewer-version')window.__vlog.push([e.data.version,e.data.via]);});")
        res["synthetic model discovered (slug not in reefs.json)"] = bool(js(c, f"!!document.querySelector('{sel}')"))
        res["model without versions has no version bar"] = js(c, "!document.querySelector('section.m3d-model[data-slug=\"prattes-reef-el-segundo\"] .m3d-versions')") is True
        res["toggle shows 3 buttons with names and dates"] = js(
            c, f"(()=>{{const b=Array.from(document.querySelectorAll('{sel} .m3d-vbtn'));return b.length===3&&b.every(x=>x.querySelector('.n').textContent.length>8&&/\\d{{4}}-\\d\\d-\\d\\d/.test(x.querySelector('.d').textContent));}})()") is True
        res["default version (b) is pressed on load"] = js(c, f"document.querySelector('{sel} .m3d-vbtn[aria-pressed=\"true\"]').getAttribute('data-m3d-ver')==='{SLUG}|b'") is True
        res["key numbers show the default version rows"] = js(c, f"document.querySelector('{sel} [data-knbody] tr.ver').textContent.includes('Laser survey edge')") is True
        res["version-specific curated row hidden for default (row 'versions: [a]')"] = js(c, f"!document.querySelector('{sel} [data-knbody]').textContent.includes('Volume (design only)')") is True
        # round 10: selecting the model starts its viewer by itself (initial #version=b)
        c.eval(f"window.ReefModels3D.select('{SLUG}')")
        c.wait_for(f"document.querySelector('{sel} iframe')", 10)
        c.pump(1.0)
        res["selecting the synthetic model shows only it (one model at a time)"] = js(c, f"document.querySelectorAll('section.m3d-model:not([hidden])').length===1&&!document.querySelector('{sel}').hidden") is True
        res["iframe src carries #version=<default>"] = js(c, f"document.querySelector('{sel} iframe').getAttribute('src').endsWith('#version=b')") is True
        c.wait_for("window.__vlog.length>=1", 10)
        res["viewer applied the initial version"] = js(c, "JSON.stringify(window.__vlog[0])") == '["b","initial"]'
        res["full-screen link carries the hash"] = js(c, f"document.querySelector('{sel} a[data-m3d-full]').getAttribute('href').endsWith('#version=b')") is True
        # switch to version a via the toggle
        c.click_selector(f'{sel} .m3d-vbtn[data-m3d-ver="{SLUG}|a"]', settle=1.5)
        res["toggle: pressed state follows the click"] = js(c, f"document.querySelector('{sel} .m3d-vbtn[data-m3d-ver=\"{SLUG}|a\"]').getAttribute('aria-pressed')==='true'") is True
        res["key numbers follow the toggle (version a rows + 'design only' row appear)"] = js(
            c, f"(()=>{{const t=document.querySelector('{sel} [data-knbody]').textContent;return t.includes('Design rock-layer foot')&&t.includes('8,000')&&t.includes('Volume (design only)');}})()") is True
        c.wait_for("window.__vlog.length>=2", 10)
        log = js(c, "JSON.stringify(window.__vlog)")
        res["iframe was told: postMessage reached the viewer"] = '"a","postMessage"' in str(log)
        res["iframe was told: hash navigation reached the viewer"] = '"a","hash"' in str(log)
        res["iframe src follows (#version=a)"] = js(c, f"document.querySelector('{sel} iframe').getAttribute('src').endsWith('#version=a')") is True
        c.click_selector(f'{sel} .m3d-vbtn[data-m3d-ver="{SLUG}|c"]', settle=1.0)
        res["by_version override applied for version c"] = js(c, f"document.querySelector('{sel} [data-knbody]').textContent.includes('-3.5 m MSL (photo version)')") is True
        res["version c without volume: no volume row"] = js(c, f"!document.querySelector('{sel} [data-knbody]').textContent.includes('Reef volume (this version)')") is True
        c.eval(f"(()=>{{const e=document.querySelector('{sel}');window.scrollTo(0,e.getBoundingClientRect().top+window.scrollY-6);}})()")
        c.pump(0.8)
        shot(c, "toggle_viewer")
        # (i) dialog
        c.click_selector(f'{sel} [data-m3d-vinfo]', settle=0.8)
        res["(i) opens the versions dialog"] = js(c, "document.querySelector('dialog.m3d-vdlg').open") is True
        res["dialog shows versions_info (both paragraphs, italic rendered)"] = js(
            c, "(()=>{const d=document.querySelector('.m3d-vdlg-in');return d.querySelectorAll(':scope > p').length>=2&&d.textContent.includes('Three outline versions')&&!!d.querySelector('i');})()") is True
        res["dialog table: name | date | source | footprint | volume, 3 rows"] = js(
            c, "(()=>{const t=document.querySelector('.m3d-vt');const h=Array.from(t.querySelectorAll('thead th')).map(x=>x.textContent).join('|');return h==='Name|Date|Source|Footprint|Volume'&&t.querySelectorAll('tbody tr').length===3;})()") is True
        res["dialog table cells filled (areas, volumes, dates, sources)"] = js(
            c, "(()=>{const t=document.querySelector('.m3d-vt').textContent;return t.includes('9,500')&&t.includes('1,250')&&t.includes('2022-03-19')&&t.includes('Synthetic laser survey')&&t.includes('not computed');})()") is True
        shot(c, "dialog")
        c.press("Escape")
        res["Escape closes the dialog"] = js(c, "!document.querySelector('dialog.m3d-vdlg').open") is True
        res["focus returns to the (i) button"] = js(c, "document.activeElement&&document.activeElement.hasAttribute('data-m3d-vinfo')") is True
        # caveats: automatic version rows
        n = js(c, f"document.querySelectorAll('table.m3d-cav tr[data-origin=\"versions\"][data-slug=\"{SLUG}\"]').length")
        res["automatic caveat rows for the version differences (2 other versions x area + volume where known = 3)"] = n == 3 or f"got {n}"
        res["version caveat row text names both versions and the difference"] = js(
            c, f"(()=>{{const r=document.querySelector('table.m3d-cav tr[data-origin=\"versions\"][data-slug=\"{SLUG}\"]');return !!r&&r.textContent.includes('Laser survey edge')&&r.textContent.includes('%')&&r.textContent.includes('by-design');}})()") is True
        c.eval("(()=>{const e=document.querySelector('table.m3d-cav tr[data-origin=\"versions\"]');window.scrollTo(0,e.getBoundingClientRect().top+window.scrollY-200);})()")
        c.pump(0.6)
        shot(c, "caveats")
    out = QA / f"{prefix}_checks.txt"
    lines = [("PASS " if v is True else "FAIL ") + k + ("" if v is True else f"  -> {v}") for k, v in res.items()]
    out.write_text("\n".join(lines) + "\n" + "\n".join("shot  " + s for s in shots) + "\n", encoding="utf-8")
    print("\n".join(lines))
    ok = all(v is True for v in res.values())
    print("RESULT:", "PASS" if ok else "FAIL", f"({sum(v is True for v in res.values())}/{len(res)})")
    if not a.keep:
        cleanup(sb)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

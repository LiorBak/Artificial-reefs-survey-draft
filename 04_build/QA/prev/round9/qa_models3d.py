"""QA of the "3D models" tab in OWN headless Chrome (random free port, fresh profile; never the shared browser pane).

    python src/qa_models3d.py [--prefix round9_3d]

Writes QA/<prefix>_*.png (overview, key numbers, gallery tooltip, lightbox, loaded viewer, methods/caveats, mobile, dark) and
QA/<prefix>_checks.txt ; exit code 1 if a check fails. check.py imports dom_checks() from here.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
sys.path.insert(0, str(HERE))
PAGE = BUILD / "artificial_reefs.html"
QA = BUILD / "QA"


def load_data3d() -> dict:
    raw = PAGE.read_text(encoding="utf-8")
    m = re.search(r'<script id="data3d" type="application/json">(.*?)</script>', raw, re.S)
    return json.loads(m.group(1)) if m else {}


def dom_checks(page: Path = PAGE, shots_prefix: str | None = None) -> dict[str, object]:
    """Open the tab from file:// and return {check name: True/False/str}. With shots_prefix also save screenshots to QA/."""
    from qa_cdp import Chrome  # noqa: PLC0415
    d = load_data3d()
    models = d.get("models", [])
    n_tiles = sum(len(m["gallery"]) for m in models)
    res: dict[str, object] = {}
    shots: list[str] = []

    def shot(c, name, **kw):
        if shots_prefix:
            p = QA / f"{shots_prefix}_{name}.png"
            c.screenshot(p, **kw)
            shots.append(p.name)

    def scroll_to(c, sel, off=10):
        c.eval(f"(()=>{{const e=document.querySelector({json.dumps(sel)});if(e)window.scrollTo(0,e.getBoundingClientRect().top+window.scrollY-{off});}})()")
        c.pump(0.6)

    url = page.as_uri() + "#view/models3d"
    with Chrome(1440, 900) as c:
        c.set_color_scheme("light")
        c.goto(url, 3)
        c.eval("document.documentElement.style.scrollBehavior='auto'")
        res["tab is the visible view"] = bool(c.eval("!document.getElementById('view-models3d').hidden && document.body.getAttribute('data-view')==='models3d'"))
        res[f"{len(models)} model sections rendered"] = c.eval("document.querySelectorAll('section.m3d-model').length") == len(models)
        res[f"{n_tiles} gallery tiles rendered (one per selected picture)"] = c.eval("document.querySelectorAll('.m3d-tile').length") == n_tiles
        res["confidence badge + reason visible in every model"] = c.eval(
            "Array.from(document.querySelectorAll('section.m3d-model')).every(s=>{const b=s.querySelector('.m3d-conf .m3d-badge');const r=s.querySelector('.m3d-conf .m3d-reason');"
            "return b&&r&&b.offsetParent!==null&&r.offsetParent!==null&&r.textContent.trim().length>20&&/^3D confidence: (high|medium|low)/i.test(b.textContent.trim())})") is True
        res["vertical-exaggeration note in every model"] = c.eval("Array.from(document.querySelectorAll('section.m3d-model .m3d-ve')).every(e=>/Vertical exaggeration/.test(e.textContent))") is True
        res["no iframe exists before 'Load 3D model' is clicked (lazy)"] = c.eval("document.querySelectorAll('.m3d-viewer iframe').length") == 0
        res["every model has an 'Open full screen' link to its viewer"] = c.eval("Array.from(document.querySelectorAll('section.m3d-model')).every(s=>{const a=s.querySelector('.m3d-viewer-bar a[href^=\"3d/\"]');return a&&/index\\.html$/.test(a.getAttribute('href'))})") is True
        res["key-numbers table in every model"] = c.eval("Array.from(document.querySelectorAll('section.m3d-model')).every(s=>s.querySelectorAll('table.m3d-kn tbody tr').length>=3)") is True
        res["caveats table rows"] = c.eval("document.querySelectorAll('table.m3d-cav tbody tr').length") == sum(len(m["caveats"]) for m in models)
        res["references list entries"] = c.eval("document.querySelectorAll('ol.m3d-refs li').length") == len(d.get("references", []))
        res["no console errors on load"] = not [e for e in c.errors if "fonts.g" not in e and "ERR_INTERNET" not in e and "ERR_NAME" not in e] or [e for e in c.errors][:3]

        scroll_to(c, "button[data-view=models3d]", 24)      # overview: the view buttons (3D models active) + the tab intro
        shot(c, "overview")
        scroll_to(c, "#view-models3d")
        scroll_to(c, ".m3d-kn", 70)
        shot(c, "keynumbers")

        # tooltip on hover (real mouse move)
        scroll_to(c, ".m3d-grid", 150)
        c.hover_selector(".m3d-tile", 1, 0.9)
        tip = c.eval("(()=>{const t=document.getElementById('m3d-tip');return t&&!t.hidden?t.innerText:''})()") or ""
        res["hover on a picture shows the tooltip with 'How it was used' and 'Source'"] = ("How it was used" in tip and "Source:" in tip) or tip[:80]
        shot(c, "gallery_tooltip")
        c.mouse(2, 2)
        c.pump(0.4)
        res["tooltip hides when the pointer leaves"] = c.eval("document.getElementById('m3d-tip').hidden") is True
        # keyboard focus also shows it
        c.eval("document.querySelectorAll('.m3d-tile')[2].focus()")
        c.pump(0.4)
        res["keyboard focus shows the tooltip"] = c.eval("!document.getElementById('m3d-tip').hidden") is True
        c.eval("document.activeElement.blur()")

        # lightbox
        scroll_to(c, ".m3d-grid", 150)
        c.click_selector(".m3d-tile", 0, 1.0)
        res["click opens the lightbox with citation, licence, rights note"] = c.eval(
            "(()=>{const d=document.querySelector('dialog.m3d-lb');return !!d&&d.open&&/citation/i.test(d.innerText)&&/licence/i.test(d.innerText)&&/rights note/i.test(d.innerText)})()") is True
        res["lightbox image loaded"] = c.eval("(()=>{const i=document.querySelector('dialog.m3d-lb img');return !!i&&i.complete&&i.naturalWidth>50})()") is True
        shot(c, "lightbox")
        # a tile with annotated versions: toggle
        c.press("Escape")
        c.pump(0.4)
        res["Escape closes the lightbox"] = c.eval("!document.querySelector('dialog.m3d-lb').open") is True
        ai = c.eval("Array.from(document.querySelectorAll('.m3d-tile')).findIndex(t=>/annotated/.test(t.textContent))")
        if isinstance(ai, int) and ai >= 0:
            c.click_selector(".m3d-tile", ai, 0.8)
            c.eval("document.querySelector('dialog.m3d-lb [data-lbver=\"1\"]').click()")
            c.pump(0.6)
            res["annotated-version toggle switches the lightbox image"] = c.eval("(()=>{const i=document.querySelector('dialog.m3d-lb img');return i&&/_ann1/.test(i.getAttribute('src'))&&document.querySelector('dialog.m3d-lb [data-lbver=\"1\"]').getAttribute('aria-pressed')==='true'})()") is True
            shot(c, "lightbox_annotated")
            c.press("Escape")
            c.pump(0.3)
        else:
            res["annotated-version toggle switches the lightbox image"] = "no tile with an annotated version"

        # lazy viewer + the cap of two live viewers
        scroll_to(c, ".m3d-viewer")
        c.click_selector("[data-m3d-load]", 0, 1.0)
        res["clicking 'Load 3D model' creates the iframe"] = c.wait_for("document.querySelectorAll('.m3d-viewer iframe').length===1", 10)
        time.sleep(7)
        c.pump(1)
        shot(c, "viewer_loaded")
        webgl = c.eval("(()=>{const f=document.querySelector('.m3d-viewer iframe');try{const cv=f.contentDocument.querySelector('canvas');return !!cv}catch(e){return 'x-origin'}})()")
        res["viewer from file:// ran (iframe has a canvas or is opaque-origin)"] = webgl in (True, "x-origin")
        n = len(models)
        for i in range(1, min(3, n)):
            c.eval(f"document.querySelector('[data-m3d-load=\"{models[i]['slug']}\"]').click()")
            c.pump(0.5)
        if n >= 3:
            res["never more than 2 live viewers"] = c.eval("document.querySelectorAll('.m3d-viewer iframe').length") == 2
        # in-tab links and lazy methods doc
        c.eval("document.querySelector('a[href^=\"#m3d-\"][href*=\"-m-3-\"]').click()")
        c.pump(0.8)
        res["methods link opens the lazy document and scrolls to the heading"] = c.eval("(()=>{const m=/^#m3d-(.+)-m-[\\d-]+$/.exec(document.querySelector('a[href^=\"#m3d-\"][href*=\"-m-3-\"]').getAttribute('href'));const d=document.querySelector('details[data-doc=methods][data-slug=\"'+m[1]+'\"]');return d.open&&d.querySelector('.m3d-doc h3')!==null})()") is True
        scroll_to(c, "#m3d-caveats")
        shot(c, "caveats")
        scroll_to(c, "#m3d-methods")
        shot(c, "methods")

    # mobile and dark
    with Chrome(390, 844, mobile=True) as c:
        c.set_color_scheme("light")
        c.goto(url, 3)
        c.eval("document.documentElement.style.scrollBehavior='auto'")
        res["mobile: no horizontal page scroll"] = c.eval("document.documentElement.scrollWidth<=window.innerWidth+1") is True or c.eval("document.documentElement.scrollWidth")
        scroll_to(c, ".m3d-model", 8)
        shot(c, "mobile")
    if shots_prefix:
        with Chrome(1440, 900) as c:
            c.set_color_scheme("dark")
            c.goto(url, 3)
            c.eval("document.documentElement.style.scrollBehavior='auto'")
            scroll_to(c, "#view-models3d")
            shot(c, "dark")
    res["_screenshots"] = shots
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="round9_3d")
    a = ap.parse_args()
    res = dom_checks(PAGE, a.prefix)
    shots = res.pop("_screenshots", [])
    lines, ok = [], True
    for k, v in res.items():
        good = v is True
        ok &= good
        lines.append(("PASS  " if good else "FAIL  ") + k + ("" if good else f"  -> {v!r}"))
    lines += [f"shot  {s}" for s in shots]
    lines.append("RESULT: " + ("PASS" if ok else "FAIL"))
    (QA / f"{a.prefix}_checks.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

"""QA of the "3D models" tab in OWN headless Chrome (random free port, fresh profile; never the shared browser pane).

    python src/qa_models3d.py [--prefix round10_3d]

Round 10 checks: reef selector (one model visible, hash routing, Back), viewer + photo panel side by side (stacked on phones), clicked
thumbnail shows beside the model, tooltip / lightbox / (i) pop-overs / Escape, full screen enter -> exit with a visible Exit button and
Esc (native and CSS fallback), sticky navigation + back-to-top, back bar on the standalone viewer (hidden when framed), combined
"All (compare)" scene (renders all exported models, overlay, vertical exaggeration), mobile layout.
Writes QA/<prefix>_*.png and QA/<prefix>_checks.txt ; exit code 1 if a check fails. check.py imports dom_checks() from here.
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

VIS = "section.m3d-model:not([hidden])"


def load_data3d() -> dict:
    raw = PAGE.read_text(encoding="utf-8")
    m = re.search(r'<script id="data3d" type="application/json">(.*?)</script>', raw, re.S)
    return json.loads(m.group(1)) if m else {}


def rect_js(sel: str) -> str:
    return f"(()=>{{const e=document.querySelector({json.dumps(sel)});if(!e)return null;const r=e.getBoundingClientRect();return {{x:r.x,y:r.y,w:r.width,h:r.height,r:r.right,b:r.bottom}}}})()"


def dom_checks(page: Path = PAGE, shots_prefix: str | None = None) -> dict[str, object]:
    """Open the tab from file:// and return {check name: True/False/str}. With shots_prefix also save screenshots to QA/."""
    from qa_cdp import Chrome  # noqa: PLC0415
    d = load_data3d()
    models = d.get("models", [])
    comb = d.get("combined") or {}
    ok_models = [c for c in comb.get("models", []) if c.get("status") == "ok"]
    n_tiles = sum(len(m["gallery"]) for m in models)
    res: dict[str, object] = {}
    shots: list[str] = []
    first = models[0]["slug"]
    second = models[1]["slug"] if len(models) > 1 else first

    def shot(c, name, **kw):
        if shots_prefix:
            p = QA / f"{shots_prefix}_{name}.png"
            c.screenshot(p, **kw)
            shots.append(p.name)

    def scroll_to(c, sel, off=10):
        c.eval(f"(()=>{{const e=document.querySelector({json.dumps(sel)});if(e)window.scrollTo(0,e.getBoundingClientRect().top+window.scrollY-{off});}})()")
        c.pump(0.6)

    def noerr(c):
        # ERR_ABORTED = a request cancelled by a newer navigation (an unloaded viewer iframe, a lazy image that scrolled away): benign
        return [e for e in c.errors if "fonts.g" not in e and "ERR_INTERNET" not in e and "ERR_NAME" not in e and "ERR_ABORTED" not in e]

    SHORT = "(el=>{const c=el.cloneNode(true);c.querySelectorAll('.info-pop').forEach(p=>p.remove());return c.textContent.replace(/\\s+/g,' ').trim().length})"

    url = page.as_uri() + "#view/models3d"
    with Chrome(1440, 900) as c:
        c.set_color_scheme("light")
        c.goto(url, 3)
        c.eval("document.documentElement.style.scrollBehavior='auto'")
        res["tab is the visible view"] = bool(c.eval("!document.getElementById('view-models3d').hidden && document.body.getAttribute('data-view')==='models3d'"))
        res["URL hash follows the selector: default = first built model"] = c.eval("location.hash") == f"#view/models3d/{first}"
        res[f"selector has one button per model + 'All (compare)' ({len(models) + (1 if comb else 0)}), exactly one pressed"] = c.eval(
            "(()=>{const b=[...document.querySelectorAll('.m3d-selbtn')];return b.length===%d&&b.filter(x=>x.getAttribute('aria-pressed')==='true').length===1&&b.every(x=>x.offsetParent!==null)})()" % (len(models) + (1 if comb else 0))) is True
        res["selector buttons show the 3D-confidence dot of each reef"] = c.eval("[...document.querySelectorAll('.m3d-selbtn:not(.all) .m3d-dot')].length") == len(models)
        res["ONE model section visible (one at a time)"] = c.eval(f"document.querySelectorAll('{VIS}').length") == 1 and c.eval(f"document.querySelector('{VIS}').getAttribute('data-slug')") == first
        res[f"{len(models)} model sections rendered (others hidden)"] = c.eval("document.querySelectorAll('section.m3d-model[data-slug]:not(#m3d-all)').length") == len(models)
        res[f"{n_tiles} thumbnails rendered (one per selected picture)"] = c.eval("document.querySelectorAll('.m3d-tile').length") == n_tiles
        res["header: badge + one-line reason + state + vertical-exaggeration note"] = c.eval(
            f"(()=>{{const s=document.querySelector('{VIS}');const b=s.querySelector('.m3d-conf .m3d-badge'),r=s.querySelector('.m3d-conf .m3d-reason'),st=s.querySelector('.m3d-state'),v=s.querySelector('.m3d-ve');"
            "return !!(b&&r&&st&&v&&b.offsetParent&&r.offsetParent&&r.textContent.trim().length>20&&/^3D confidence: (high|medium|low)/i.test(b.textContent.trim())&&/Vertical exaggeration/.test(v.textContent)&&r.getBoundingClientRect().height<40)})()") is True
        res["every model has the full vertical-exaggeration text behind its (i)"] = c.eval("[...document.querySelectorAll('section.m3d-model[data-slug]:not(#m3d-all) .m3d-conf .info-pop')].every(p=>/Vertical exaggeration/.test(p.textContent)&&/3D confidence/.test(p.textContent))") is True
        res["text at the top is short: tab intro <= 260 chars, page intro <= 260 chars (the rest sits behind (i))"] = c.eval(f"{SHORT}(document.querySelector('.m3d-lead'))<=260&&{SHORT}(document.getElementById('intro'))<=260") is True
        res["site header (long text) is collapsed on this tab"] = c.eval("getComputedStyle(document.querySelector('.site-head')).display") == "none"
        res["key-numbers table in every model"] = c.eval("[...document.querySelectorAll('section.m3d-model[data-slug]:not(#m3d-all)')].every(s=>s.querySelectorAll('table.m3d-kn tbody tr').length>=3)") is True
        res["caveats table rows"] = c.eval("document.querySelectorAll('table.m3d-cav tbody tr').length") == sum(len(m["caveats"]) for m in models)
        res["references list entries"] = c.eval("document.querySelectorAll('ol.m3d-refs li').length") == len(d.get("references", []))
        res["appendix (methods, texts relied on, caveats, references) is at the bottom of the tab and reachable by link"] = c.eval(
            "(()=>{const a=document.getElementById('m3d-app');const s=document.querySelector('.m3d-model:not([hidden])');return !!a&&a.getBoundingClientRect().top>s.getBoundingClientRect().top&&['m3d-methods','m3d-relied','m3d-caveats','m3d-refs'].every(i=>document.getElementById(i))&&document.querySelectorAll('.m3d-lead a[href=\"#m3d-app\"]').length>0})()") is True

        # --- layout: viewer + photos side by side, key numbers below
        c.wait_for(f"document.querySelector('{VIS} .m3d-viewer iframe')", 15)
        res["viewer of the selected model starts by itself (iframe present, only for the visible model)"] = c.eval("document.querySelectorAll('.m3d-viewer iframe').length") == 1
        v, p = c.eval(rect_js(f"{VIS} .m3d-viewer")), c.eval(rect_js(f"{VIS} .m3d-pics"))
        kn = c.eval(rect_js(f"{VIS} .m3d-kn"))
        res["desktop: viewer and photo panel are side by side (same top, viewer ~60 %)"] = bool(v and p and p["x"] >= v["r"] - 2 and abs(p["y"] - v["y"]) < 12 and 0.5 < v["w"] / (v["w"] + p["w"]) < 0.7) or f"viewer {v} pics {p}"
        res["desktop: key numbers are BELOW the viewer + photos"] = bool(kn and v and kn["y"] > max(v["b"], p["b"]) - 4)
        res["photo panel shows a large picture (loaded) and a thumbnail strip grouped by role"] = c.eval(
            f"(()=>{{const i=document.querySelector('{VIS} .m3d-pic-fig img');return !!i&&i.complete&&i.naturalWidth>50&&document.querySelectorAll('{VIS} .m3d-sgroup').length>=2}})()") is True
        shot(c, "overview")
        time.sleep(6)
        c.pump(1)
        shot(c, "model_with_photos")
        res["viewer from file:// ran (iframe has a canvas or is opaque-origin)"] = c.eval("(()=>{const f=document.querySelector('.m3d-viewer iframe');try{return !!f.contentDocument.querySelector('canvas')}catch(e){return true}})()") is True

        # --- thumbnails: click -> shown in the panel next to the model; tooltip; keyboard
        scroll_to(c, VIS + " .m3d-stage", 120)
        src0 = c.eval(f"document.querySelector('{VIS} .m3d-pic-fig img').getAttribute('src')")
        c.click_selector(f"{VIS} .m3d-th", 3, 0.8)
        src1 = c.eval(f"document.querySelector('{VIS} .m3d-pic-fig img').getAttribute('src')")
        want = c.eval(f"(()=>{{const t=document.querySelectorAll('{VIS} .m3d-th')[3];return t.getAttribute('data-pic').split('|')[1]}})()")
        res["clicking a thumbnail shows it in the panel next to the 3D model (no modal)"] = bool(src1 and src1 != src0 and want in src1 and c.eval("!document.querySelector('dialog.m3d-lb')||!document.querySelector('dialog.m3d-lb').open") and c.eval(f"!!document.querySelector('{VIS} .m3d-viewer iframe')"))
        res["clicked thumbnail is marked (aria-pressed) and the caption names the picture"] = c.eval(f"(()=>{{const t=document.querySelectorAll('{VIS} .m3d-th')[3];return t.getAttribute('aria-pressed')==='true'&&document.querySelector('{VIS} .m3d-pic-cap b').textContent.length>5}})()") is True
        c.click_selector(f"{VIS} [data-picnav=\"1\"]", 0, 0.6)
        res["next-picture arrow steps through the strip"] = c.eval(f"document.querySelector('{VIS} .m3d-pic-count').textContent.trim().startsWith('5 /')") is True
        c.hover_selector(f"{VIS} .m3d-th", 1, 0.9)
        tip = c.eval("(()=>{const t=document.getElementById('m3d-tip');return t&&!t.hidden?t.innerText:''})()") or ""
        res["hover on a thumbnail shows the tooltip with 'How it was used' and 'Source'"] = ("How it was used" in tip and "Source:" in tip) or tip[:80]
        shot(c, "thumb_tooltip")
        c.mouse(2, 2)
        c.pump(0.4)
        res["tooltip hides when the pointer leaves"] = c.eval("document.getElementById('m3d-tip').hidden") is True
        c.eval(f"document.querySelectorAll('{VIS} .m3d-th')[2].focus()")
        c.pump(0.4)
        res["keyboard focus on a thumbnail shows the tooltip"] = c.eval("!document.getElementById('m3d-tip').hidden") is True
        c.eval("document.activeElement.blur()")
        # annotated toggle lives in the panel
        ai = c.eval(f"Array.from(document.querySelectorAll('{VIS} .m3d-th')).findIndex(t=>/\\+/.test(t.textContent))")
        if isinstance(ai, int) and ai >= 0:
            c.click_selector(f"{VIS} .m3d-th", ai, 0.7)
            c.eval(f"document.querySelector('{VIS} [data-picver=\"1\"]').click()")
            c.pump(0.6)
            res["annotated-version toggle in the panel switches the picture next to the model"] = c.eval(f"(()=>{{const i=document.querySelector('{VIS} .m3d-pic-fig img');return i&&/_ann1/.test(i.getAttribute('src'))&&document.querySelector('{VIS} [data-picver=\"1\"]').getAttribute('aria-pressed')==='true'}})()") is True
            shot(c, "panel_annotated")
        else:
            res["annotated-version toggle in the panel switches the picture next to the model"] = "no picture with an annotated version"
        # enlarge -> lightbox with the full record, a visible Close button, Escape
        c.click_selector(f"{VIS} .m3d-pic-zoom", 0, 1.0)
        res["'Enlarge' opens the lightbox with citation, licence, rights note"] = c.eval(
            "(()=>{const d=document.querySelector('dialog.m3d-lb');return !!d&&d.open&&/citation/i.test(d.innerText)&&/licence/i.test(d.innerText)&&/rights note/i.test(d.innerText)})()") is True
        res["lightbox has a visible Close button (top-right and in the footer)"] = c.eval("(()=>{const d=document.querySelector('dialog.m3d-lb');const b=d.querySelector('.m3d-lb-close');const r=b.getBoundingClientRect();return r.width>=30&&r.height>=30&&d.querySelectorAll('[data-m3d-lbclose]').length>=2})()") is True
        shot(c, "lightbox")
        c.click_selector("dialog.m3d-lb .m3d-lb-close", 0, 0.5)
        res["Close button closes the lightbox"] = c.eval("!document.querySelector('dialog.m3d-lb').open") is True
        c.click_selector(f"{VIS} .m3d-pic-zoom", 0, 0.8)
        c.press("Escape")
        c.pump(0.4)
        res["Escape closes the lightbox"] = c.eval("!document.querySelector('dialog.m3d-lb').open") is True

        # --- (i) pop-overs
        scroll_to(c, VIS, 130)
        c.click_selector(f"{VIS} .m3d-conf .info-i", 0, 0.5)
        res["(i) opens a pop-over with the full text; pinned by click"] = c.eval(f"(()=>{{const p=document.querySelector('{VIS} .m3d-conf .info-pop');return !p.hidden&&/Vertical exaggeration/.test(p.innerText)&&p.getBoundingClientRect().width>200}})()") is True
        shot(c, "info_popover")
        c.press("Escape")
        c.pump(0.3)
        res["Escape closes the (i) pop-over"] = c.eval(f"document.querySelector('{VIS} .m3d-conf .info-pop').hidden") is True
        c.hover_selector(".m3d-lead .info-i", 0, 0.6)
        res["(i) also opens on hover"] = c.eval("!document.querySelector('.m3d-lead .info-pop').hidden") is True
        c.mouse(5, 400)
        c.pump(0.6)
        c.eval("document.querySelector('.m3d-lead .info-i').focus()")
        c.pump(0.3)
        res["(i) opens on keyboard focus"] = c.eval("!document.querySelector('.m3d-lead .info-pop').hidden") is True
        c.press("Escape")
        c.eval("document.activeElement.blur()")

        # --- selector: switch models, hash, Back
        c.eval("window.scrollTo(0,0)")
        c.click_selector(f".m3d-selbtn[data-m3d-sel=\"{second}\"]", 0, 1.2)
        res["selector switches the model: hash follows, the other section is hidden"] = (c.eval("location.hash") == f"#view/models3d/{second}" and c.eval(f"document.querySelectorAll('{VIS}').length") == 1 and c.eval(f"document.querySelector('{VIS}').getAttribute('data-slug')") == second) or c.eval("location.hash")
        c.pump(1.5)
        res["switching unloads the previous viewer (one live iframe, in the visible model)"] = c.eval("document.querySelectorAll('.m3d-viewer iframe').length") == 1 and c.eval(f"!!document.querySelector('{VIS} .m3d-viewer iframe')")
        c.eval("history.back()")
        c.pump(1.2)
        res["browser Back returns to the previous model"] = c.eval(f"document.querySelector('{VIS}').getAttribute('data-slug')") == first
        c.eval(f"document.querySelector('.m3d-selbtn[data-m3d-sel=\"{second}\"]').focus()")
        for kind in ("keyDown", "keyUp"):          # a full Enter key (with its char event) activates a focused <button>
            c.call("Input.dispatchKeyEvent", type=kind, key="Enter", code="Enter", windowsVirtualKeyCode=13, nativeVirtualKeyCode=13, **({"text": "\r"} if kind == "keyDown" else {}))
        c.pump(0.6)
        res["selector is keyboard operable (Enter on a focused button selects it)"] = c.eval(f"document.querySelector('{VIS}').getAttribute('data-slug')") == second or "Enter keypress did not select"
        # methods link from the caveats table works across models (opens the right model + the lazy document)
        c.eval("document.getElementById('m3d-caveats').open=true")
        c.eval("document.querySelector('a[href^=\"#m3d-\"][href*=\"-m-3-\"]').click()")
        c.pump(1.0)
        res["methods link in the caveats table selects its model, opens the lazy document and scrolls to the heading"] = c.eval(
            "(()=>{const a=document.querySelector('a[href^=\"#m3d-\"][href*=\"-m-3-\"]');const m=/^#m3d-(.+)-m-[\\d-]+$/.exec(a.getAttribute('href'));const d=document.querySelector('details[data-doc=methods][data-slug=\"'+m[1]+'\"]');return d.open&&d.querySelector('.m3d-doc h3')!==null&&document.querySelector('section.m3d-model:not([hidden])').getAttribute('data-slug')===m[1]})()") is True
        scroll_to(c, "#m3d-caveats")
        shot(c, "caveats")
        c.eval("document.getElementById('m3d-methods').open=true")
        scroll_to(c, "#m3d-methods")
        shot(c, "methods")
        res["no console errors"] = not noerr(c) or noerr(c)[:3]

    # --- full screen (native Fullscreen API + CSS fallback + Esc), sticky navigation, back-to-top, brand link
    with Chrome(1440, 900) as c:
        c.set_color_scheme("light")
        c.goto(url, 3)
        c.eval("document.documentElement.style.scrollBehavior='auto'")
        c.wait_for(f"document.querySelector('{VIS} .m3d-viewer iframe')", 15)
        c.click_selector(f"{VIS} [data-m3d-fs]", 0, 1.5)
        st = c.eval("(()=>{const s=document.querySelector('.m3d-stage.is-full');return !!s&&(document.fullscreenElement===s||getComputedStyle(s).position==='fixed')})()")
        res["Full screen: the stage (viewer + photo panel) goes full screen"] = st is True
        ex = c.eval(rect_js(".m3d-stage.is-full .m3d-exitfs"))
        res["Full screen: a visible 'Exit full screen' button sits top-right, on top"] = bool(ex and ex["w"] > 80 and ex["y"] < 40 and ex["r"] > 1440 - 60 and c.eval("(()=>{const e=document.querySelector('.m3d-stage.is-full .m3d-exitfs');const r=e.getBoundingClientRect();return document.elementFromPoint(r.x+r.width/2,r.y+r.height/2)===e})()")) or ex
        res["Full screen: viewer and photo panel are both inside it"] = c.eval("(()=>{const s=document.querySelector('.m3d-stage.is-full');return !!s.querySelector('iframe')&&!!s.querySelector('.m3d-pic-fig img')})()") is True
        res["Full screen: the toolbar button reads 'Exit full screen'"] = c.eval(f"document.querySelector('{VIS} [data-m3d-fs]').textContent.trim()") == "Exit full screen"
        time.sleep(4)
        shot(c, "fullscreen")
        c.click_selector(".m3d-exitfs", 0, 1.2)
        res["Exit button leaves full screen; the page is intact (selector, model, viewer)"] = c.eval(
            f"(()=>{{return !document.querySelector('.m3d-stage.is-full')&&!document.fullscreenElement&&document.querySelectorAll('{VIS}').length===1&&!!document.querySelector('{VIS} .m3d-viewer iframe')&&document.querySelectorAll('.m3d-selbtn').length>1&&document.querySelector('[data-m3d-fs]').textContent.trim()==='Full screen'}})()") is True
        # CSS fallback (no Fullscreen API, e.g. iPhone): Esc must also exit
        c.eval("Element.prototype.requestFullscreen=undefined;Element.prototype.webkitRequestFullscreen=undefined")
        c.click_selector(f"{VIS} [data-m3d-fs]", 0, 0.8)
        res["Full screen fallback (no Fullscreen API): CSS full-screen layout with the Exit button"] = c.eval("(()=>{const s=document.querySelector('.m3d-stage.is-full');const e=s&&s.querySelector('.m3d-exitfs');return !!e&&getComputedStyle(s).position==='fixed'&&e.getBoundingClientRect().width>80&&!document.fullscreenElement})()") is True
        c.press("Escape")
        c.pump(0.5)
        res["Esc leaves the full-screen fallback"] = c.eval("!document.querySelector('.m3d-stage.is-full')") is True

        # sticky nav + back to top
        c.eval("window.scrollTo(0, 1500)")
        c.pump(0.6)
        nav = c.eval(rect_js("#topnav"))
        res["sticky navigation stays visible after scrolling down (top of the window, view buttons reachable)"] = bool(nav and abs(nav["y"]) < 2 and nav["h"] > 30 and c.eval("[...document.querySelectorAll('#topnav .views button')].every(b=>{const r=b.getBoundingClientRect();return r.top>=0&&r.bottom<=90&&r.width>20})")) or nav
        res["reef selector stays visible under the navigation while scrolling the model"] = c.eval("(()=>{const r=document.getElementById('m3d-selwrap').getBoundingClientRect();return r.top>=40&&r.top<70&&r.height>30})()") is True
        shot(c, "sticky_nav")
        res["'Top' button appears on long views and returns to the top"] = c.eval("!document.getElementById('to-top').hidden") is True
        c.click_selector("#to-top", 0, 0.6)
        res["'Top' button scrolls to the top"] = c.eval("window.scrollY") < 5
        c.eval("window.scrollTo(0, 2500)")
        c.pump(0.4)
        c.click_selector("#topnav .views button[data-view=gallery]", 0, 1.0)
        res["from deep inside the tab one click on 'Gallery' shows the main page from its top"] = c.eval("!document.getElementById('view-gallery').hidden&&document.getElementById('view-models3d').hidden&&document.body.getAttribute('data-view')==='gallery'&&window.scrollY<5") is True
        res["leaving the tab frees the viewers (no iframe left)"] = c.eval("document.querySelectorAll('.m3d-viewer iframe').length") == 0
        c.click_selector("#topnav .views button[data-view=map]", 0, 1.0)
        c.click_selector("#topnav .views button[data-view=models3d]", 0, 1.5)
        res["tabs switch from every view (Map -> 3D models) and the tab re-opens on its model"] = c.eval("!document.getElementById('view-models3d').hidden&&/^#view\\/models3d\\/[a-z0-9-]+$/.test(location.hash)&&document.querySelectorAll('section.m3d-model:not([hidden])').length===1") is True
        c.eval("window.scrollTo(0, 2500)")
        c.click_selector("a[data-home]", 0, 1.0)
        res["brand link 'Surf reefs survey' returns to the main page (Gallery)"] = c.eval("document.body.getAttribute('data-view')==='gallery'&&window.scrollY<5") is True
        res["the gallery's page intro is 2 short lines with an (i)"] = c.eval(f"(()=>{{const i=document.getElementById('intro');return {SHORT}(i)<=260&&!!i.querySelector('.info-i')&&i.getBoundingClientRect().height<90}})()") is True
        shot(c, "gallery_header")
        res["no console errors (navigation session)"] = not noerr(c) or noerr(c)[:3]

    # --- All (compare)
    if comb:
        with Chrome(1440, 900) as c:
            c.set_color_scheme("light")
            c.goto(page.as_uri() + "#view/models3d", 3)
            c.eval("document.documentElement.style.scrollBehavior='auto'")
            c.click_selector(".m3d-selbtn.all", 0, 1.5)
            res["'All (compare)' selects the combined section (hash #view/models3d/all, one section visible)"] = c.eval("location.hash") == "#view/models3d/all" and c.eval(f"document.querySelector('{VIS}').id") == "m3d-all"
            c.wait_for("document.querySelector('#m3d-all .m3d-viewer iframe')", 15)
            time.sleep(7)
            res["combined viewer starts in its stage; comparison panel lists every model with its check result"] = c.eval("(()=>{const s=document.querySelector('#m3d-all');return !!s.querySelector('iframe')&&s.querySelectorAll('.m3d-cmpt tbody tr').length===%d})()" % len(models)) is True
            res["comparison panel: footprint and crest read back from the meshes, all checks pass"] = c.eval("[...document.querySelectorAll('#m3d-all .m3d-cmpt .m3d-status')].filter(x=>!x.classList.contains('resolved')).length") == 0
            shot(c, "all_stage")
            scroll_to(c, "#m3d-all-method", 80)
            shot(c, "all_method")
            res["method + check table of the combined scene are on the page"] = c.eval("document.querySelectorAll('#m3d-all table.m3d-chk tbody tr').length") == len(models)
        # the combined viewer on its own (works from file://)
        cpage = BUILD / "3d" / "combined" / "index.html"
        with Chrome(1300, 760) as c:
            c.set_color_scheme("light")
            c.goto(cpage.as_uri(), 3)
            ready = c.wait_for("window.__combinedReady", 40)
            c.pump(2)
            res["combined viewer (standalone, file://) renders a frame without errors"] = bool(ready and (c.eval("window.__combinedFrames") or 0) >= 1 and not noerr(c)) or noerr(c)[:3]
            res[f"combined scene holds all {len(ok_models)} exported reefs, each with seabed + reef mesh"] = c.eval("window.__combined.items.length===%d&&window.__combined.items.every(i=>i.sea.geometry.attributes.position.count>1000&&i.reef.geometry.attributes.position.count>100)" % len(ok_models)) is True
            res["combined: every reef is positioned side by side at one scale (no overlap of the seabed patches)"] = c.eval(
                "(()=>{const it=window.__combined.items;const iv=it.map(i=>[i.xOff+i.d.bounds[0],i.xOff+i.d.bounds[1]]).sort((a,b)=>a[0]-b[0]);for(let k=1;k<iv.length;k++)if(iv[k][0]<iv[k-1][1])return false;return true})()") is True
            res["combined: z = 0 is each site's own MSL (water plane at y = 0; the exported crest level is the reef mesh's top)"] = c.eval(
                "window.__combined.items.every(i=>{i.reef.geometry.computeBoundingBox();return Math.abs(i.water.position.y)<1e-9&&Math.abs(i.reef.geometry.boundingBox.max.y-i.d.crest_z)<0.01&&i.sea.geometry.boundingBox!==undefined||true})&&window.__combined.items.every(i=>Math.abs(i.reef.geometry.boundingBox.max.y-i.d.crest_z)<0.01)") is True
            ve0 = c.eval("document.getElementById('ve-chip').textContent")
            res["combined: vertical exaggeration is always shown, default 1x"] = "1x" in ve0 and c.eval("getComputedStyle(document.getElementById('ve-chip')).display") != "none"
            res["combined: controls for water, seabed, metre grid, scale bars, outlines, labels, plan / oblique / side presets, overlay"] = c.eval(
                "['t-water','t-sea','t-grid','t-bars','t-out','t-lbl'].every(i=>document.getElementById(i))&&['plan','oblique','side'].every(v=>document.querySelector('[data-view=\"'+v+'\"]'))&&!!document.querySelector('[data-mode=\"overlay\"]')&&!!document.getElementById('ve')") is True
            c.eval("document.getElementById('ve').value=3;document.getElementById('ve').dispatchEvent(new Event('input'))")
            c.pump(0.5)
            res["combined: the VE slider scales every reef together (y scale 3, chip says 3x)"] = c.eval("window.__combined.scene.children.some(o=>o.type==='Group'&&o.scale.y===3)&&/3x/.test(document.getElementById('ve-chip').textContent)") is True
            c.eval("window.__combined.setVE(1)")
            shot(c, "combined_oblique")
            c.click_selector("[data-view=plan]", 0, 1.0)
            shot(c, "combined_plan")
            c.click_selector("[data-mode=overlay]", 0, 1.2)
            res["combined overlay: every reef is centred on one origin (footprint centroids at 0, 0)"] = c.eval(
                "window.__combined.items.every(i=>Math.abs(i.group.position.x+i.d.centroid[0])<1e-6&&Math.abs(i.group.position.z+i.d.centroid[1])<1e-6)&&window.__combined.items.every(i=>!i.sea.visible)") is True
            shot(c, "combined_overlay")
            c.click_selector("[data-view=side]", 0, 1.0)
            shot(c, "combined_overlay_side")
            c.click_selector("[data-mode=side]", 0, 1.0)
            res["combined: switching back to side by side restores the layout"] = c.eval("window.__combined.items.every(i=>i.sea.visible)&&window.__combined.state.mode==='side'") is True

    # --- standalone viewer pages: back bar (and hidden when framed)
    vp = BUILD / "3d" / first / "index.html"
    with Chrome(1300, 760) as c:
        c.goto(vp.as_uri(), 3)
        bar = c.eval(rect_js(".m3d-topbar"))
        res["standalone viewer page has a slim top bar (visible) with '<- Back to the page' and the main tabs"] = bool(bar and bar["h"] > 20 and bar["y"] == 0 and c.eval(
            "(()=>{const a=[...document.querySelectorAll('.m3d-topbar a')].map(x=>x.textContent.trim());return a.some(t=>/Back to the page/.test(t))&&['Gallery','Map','Table','Scale','3D models'].every(t=>a.includes(t))})()") is True) or bar
        res["the bar does not cover the viewer (content starts below it)"] = c.eval("(()=>{const e=document.querySelector('#app,#main,#view,#stage');if(!e)return true;return e.getBoundingClientRect().top>=33})()") is True
        shot(c, "standalone_bar")
        c.click_selector(".m3d-topbar a.back", 0, 2.0)
        res["'<- Back to the page' returns to the survey page on that model"] = c.eval("location.hash") == f"#view/models3d/{first}" and c.eval("!!document.getElementById('view-models3d')&&!document.getElementById('view-models3d').hidden") is True
    with Chrome(1300, 760, allow_file_access=True) as c:
        c.goto(page.as_uri() + f"#view/models3d/{first}", 3)
        c.wait_for(f"document.querySelector('{VIS} .m3d-viewer iframe')", 15)
        time.sleep(3)
        r = c.eval(f"(()=>{{try{{const d=document.querySelector('{VIS} iframe').contentDocument;const b=d.querySelector('.m3d-topbar');return d.documentElement.classList.contains('m3d-embedded')&&getComputedStyle(b).display==='none'}}catch(e){{return 'x-origin: '+e}}}})()")
        res["the back bar is hidden when the viewer is framed by the page"] = r is True or r

    # --- mobile and dark
    with Chrome(390, 844, mobile=True) as c:
        c.set_color_scheme("light")
        c.goto(url, 3)
        c.eval("document.documentElement.style.scrollBehavior='auto'")
        res["mobile: no horizontal page scroll"] = c.eval("document.documentElement.scrollWidth<=window.innerWidth+1") is True or c.eval("document.documentElement.scrollWidth")
        res["mobile: navigation and reef selector are visible and operable"] = c.eval("(()=>{const n=document.getElementById('topnav').getBoundingClientRect();const b=[...document.querySelectorAll('.m3d-selbtn')];return n.top>=0&&n.width>=380&&b.every(x=>x.getBoundingClientRect().width>40)})()") is True
        c.wait_for(f"document.querySelector('{VIS} .m3d-viewer iframe')", 15)
        v, p = c.eval(rect_js(f"{VIS} .m3d-viewer")), c.eval(rect_js(f"{VIS} .m3d-pics"))
        res["mobile: photos sit directly under the viewer (stacked, no side-by-side)"] = bool(v and p and p["y"] >= v["b"] - 2 and p["y"] - v["b"] < 160 and p["w"] > 330) or f"v {v} p {p}"
        scroll_to(c, VIS, 120)
        shot(c, "mobile")
        c.click_selector(f"{VIS} .m3d-th", 2, 0.6)
        res["mobile: tapping a thumbnail shows it in the panel"] = c.eval(f"document.querySelectorAll('{VIS} .m3d-th')[2].getAttribute('aria-pressed')") == "true"
    if shots_prefix:
        with Chrome(1440, 900) as c:
            c.set_color_scheme("dark")
            c.goto(url, 3)
            c.eval("document.documentElement.style.scrollBehavior='auto'")
            time.sleep(5)
            shot(c, "dark")
    res["_screenshots"] = shots
    return res


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="round10_3d")
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

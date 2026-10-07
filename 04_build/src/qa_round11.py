"""Round 11 QA of the "3D models" tab (own headless Chrome, random free port, fresh profile; never the shared browser pane).

    python src/qa_round11.py [--prefix round11_3d]

Checks: (1) combined "All (compare)" scene: Boscombe's beach + shoreline are in the exported seabed, ONE scale bar, reef labels do not overlap and stay
inside the canvas (default oblique view, plan view, overlay, a narrow window); (2) collapsible panels: combined layout panel, every single-model viewer's
own left panel, the page's right-hand panel (photos / reefs in this scene), state kept across full screen; (3) outline-version toggle with the real
models that have versions (Mount Maunganui, Borth); (4) "Match this photo" (when data/photo_match.json exists).
Writes QA/<prefix>_*.png and QA/<prefix>_checks.txt ; exit code 1 on a failed check. check.py --full and update_page.py --full import dom_checks11().
"""
from __future__ import annotations

import argparse
import json
import re
import sys
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


LABELS_JS = """(function(){var W=document.getElementById('stage').clientWidth,H=document.getElementById('stage').clientHeight,pw=document.getElementById('ctrl').offsetParent?document.getElementById('ctrl').offsetWidth:0;
var L=[].slice.call(document.querySelectorAll('#rlabels .lbl')).filter(function(e){return e.style.display!=='none';}).map(function(e){var r=e.getBoundingClientRect(),s=document.getElementById('stage').getBoundingClientRect();return {x:r.left-s.left,y:r.top-s.top,w:r.width,h:r.height,t:e.textContent.slice(0,24)};});
var ov=0,out=0;for(var i=0;i<L.length;i++){var a=L[i];if(a.x<-0.5||a.y<-0.5||a.x+a.w>W+0.5||a.y+a.h>H+0.5)out++;for(var j=i+1;j<L.length;j++){var b=L[j];if(a.x<b.x+b.w&&b.x<a.x+a.w&&a.y<b.y+b.h&&b.y<a.y+a.h)ov++;}}
var underPanel=0;if(pw)L.forEach(function(a){if(a.x<pw-1)underPanel++;});
return JSON.stringify({n:L.length,overlaps:ov,outside:out,underPanel:underPanel,bars:document.querySelectorAll('#labels .bar').length,W:W,H:H});})()"""


def dom_checks11(page: Path = PAGE, shots_prefix: str | None = None) -> dict[str, object]:
    from qa_cdp import Chrome  # noqa: PLC0415
    d = load_data3d()
    models = d.get("models", [])
    slugs = [m["slug"] for m in models]
    res: dict[str, object] = {}
    shots: list[str] = []

    def errs(c):      # ERR_ABORTED = a request cancelled by a newer navigation (unloaded iframe, scrolled-away lazy image): benign
        return [e for e in c.errors if "fonts.g" not in e and "ERR_INTERNET" not in e and "ERR_NAME" not in e and "ERR_ABORTED" not in e]

    def shot(c, name, **kw):
        if shots_prefix:
            p = QA / f"{shots_prefix}_{name}.png"
            c.screenshot(p, **kw)
            shots.append(p.name)

    comb_url = (BUILD / "3d" / "combined" / "index.html").as_uri()
    # ---------------------------------------------------------------- (1) combined scene
    for tag, (w, h) in (("1440x900", (1440, 900)), ("1000x700", (1000, 700))):
        with Chrome(w, h, allow_file_access=True) as c:
            c.goto(comb_url, 2.0)
            c.wait_for("window.__combinedReady", 40)
            c.pump(1.5)
            if tag == "1440x900":
                bos = json.loads(c.eval("JSON.stringify(window.M3D_COMBINED['boscombe-surf-reef']?{b:window.M3D_COMBINED['boscombe-surf-reef'].bounds,y:window.M3D_COMBINED['boscombe-surf-reef'].y_range}:null)") or "null")
                res["combined: Boscombe seabed reaches the beach (y from about -66 m, land above MSL) and offshore (y to 650 m)"] = bool(bos and bos["b"][2] <= -60 and bos["b"][3] >= 600 and bos["y"][1] > 1.0)
                res["combined: Boscombe is in the scene (all exported models present)"] = bool(c.eval("window.__combined.items.length===%d" % len([m for m in d.get("combined", {}).get("models", []) if m.get("status") == "ok"])))
            for view, shotname in (("oblique", "combined_oblique"), ("plan", "combined_plan")):
                c.eval(f"window.__combined.setView('{view}',0)"); c.pump(1.2)
                r = json.loads(c.eval(LABELS_JS))
                res[f"combined {tag} {view}: reef labels do not overlap and sit inside the canvas, clear of the panel ({r['n']} labels)"] = bool(r["n"] >= 1 and r["overlaps"] == 0 and r["outside"] == 0 and r["underPanel"] == 0)
                res[f"combined {tag} {view}: exactly one scale bar (one label '100 m')"] = r["bars"] == 1
                if tag == "1440x900":
                    shot(c, shotname)
            if tag == "1440x900":
                c.eval("window.__combined.setMode('overlay')"); c.pump(1.2)
                r = json.loads(c.eval(LABELS_JS))
                res["combined overlay: labels do not overlap, inside the canvas, one scale bar"] = bool(r["overlaps"] == 0 and r["outside"] == 0 and r["underPanel"] == 0 and r["bars"] == 1)
                shot(c, "combined_overlay")
                c.eval("window.__combined.setMode('side')"); c.pump(0.8)
                # collapsible layout panel
                res["combined panel: open by default (Hide button visible, Layout button hidden)"] = bool(c.eval("document.getElementById('ctrl').offsetParent!==null&&!document.getElementById('ctrlOpen').offsetParent"))
                c.click_selector("#ctrlHide", settle=1.0)
                res["combined panel: Hide collapses the panel and shows a labelled 'Layout' button at the bottom-left edge"] = bool(c.eval("!document.getElementById('ctrl').offsetParent&&document.getElementById('ctrlOpen').offsetParent!==null&&/Layout/.test(document.getElementById('ctrlOpen').textContent)&&document.getElementById('ctrlOpen').getBoundingClientRect().left<40&&document.getElementById('ctrlOpen').getBoundingClientRect().bottom>window.innerHeight-60"))
                r = json.loads(c.eval(LABELS_JS))
                res["combined panel collapsed: labels still do not overlap and stay inside"] = bool(r["overlaps"] == 0 and r["outside"] == 0)
                shot(c, "combined_panel_hidden")
                c.click_selector("#ctrlOpen", settle=1.0)
                res["combined panel: the Layout button opens it again"] = bool(c.eval("document.getElementById('ctrl').offsetParent!==null"))
                res["combined: no page errors"] = not errs(c)

    # ---------------------------------------------------------------- (2) page panels + versions + full screen
    with Chrome(1440, 900, allow_file_access=True) as c:
        c.goto(page.as_uri() + "#view/models3d/all", 3.0)
        c.wait_for("document.querySelector('section.m3d-model:not([hidden]) iframe')", 40)
        c.pump(4.0)
        stage = "section.m3d-all .m3d-stage"
        res["page panel (All): open by default, 'Hide' in the panel, 'Reefs' button hidden"] = bool(c.eval(f"(()=>{{var s=document.querySelector('{stage}');return s&&!s.classList.contains('pics-off')&&s.querySelector('.m3d-pics').offsetParent!==null&&!s.querySelector('.m3d-pcol-open').offsetParent}})()"))
        c.eval("document.querySelector('section.m3d-all [data-m3d-fs]').scrollIntoView({block:'center'})"); c.pump(0.6)   # the 7th reef chip wraps the selector row: the button can sit below the fold
        c.click_selector(f"{stage} [data-m3d-fs]" if c.eval(f"!!document.querySelector('{stage} [data-m3d-fs]')") else "section.m3d-all [data-m3d-fs]", settle=2.0)
        res["full screen (All): the stage is full screen with the reefs panel and the viewer's layout panel both open"] = bool(c.eval(f"(()=>{{var s=document.querySelector('{stage}');var f=s.querySelector('iframe').contentWindow;return s.classList.contains('is-full')&&s.querySelector('.m3d-pics').offsetParent!==null&&f.document.getElementById('ctrl').offsetParent!==null}})()"))
        shot(c, "fullscreen_panels_open")
        c.click_selector(f"{stage} .m3d-pcol-bar .m3d-pcol", settle=1.5)
        res["full screen (All): 'Hide' collapses the right-hand panel; a 'Reefs' button appears; the viewer fills the width"] = bool(c.eval(f"(()=>{{var s=document.querySelector('{stage}');var f=s.querySelector('iframe');var b=s.querySelector('.m3d-pcol-open');return s.classList.contains('pics-off')&&!s.querySelector('.m3d-pics').offsetParent&&b.offsetParent!==null&&/Reefs/.test(b.textContent)&&f.clientWidth>window.innerWidth-40}})()"))
        c.eval(f"document.querySelector('{stage} iframe').contentWindow.document.getElementById('ctrlHide').click()")
        c.pump(1.5)
        res["full screen (All): the layout panel can be collapsed too (both panels hidden: the model is unobstructed)"] = bool(c.eval(f"(()=>{{var f=document.querySelector('{stage} iframe').contentWindow;return !f.document.getElementById('ctrl').offsetParent&&f.document.getElementById('ctrlOpen').offsetParent!==null}})()"))
        shot(c, "fullscreen_panels_hidden")
        c.press("Escape"); c.pump(1.0)
        if c.eval(f"document.querySelector('{stage}').classList.contains('is-full')"):
            c.click_selector(f"{stage} [data-m3d-exitfs]", settle=1.0)
        res["leaving full screen keeps both panels collapsed (state survives)"] = bool(c.eval(f"(()=>{{var s=document.querySelector('{stage}');var f=s.querySelector('iframe').contentWindow;return !s.classList.contains('is-full')&&s.classList.contains('pics-off')&&!f.document.getElementById('ctrl').offsetParent}})()"))
        c.click_selector(f"{stage} .m3d-pcol-open", settle=1.0)
        res["the 'Reefs' button opens the right-hand panel again"] = bool(c.eval(f"(()=>{{var s=document.querySelector('{stage}');return !s.classList.contains('pics-off')&&s.querySelector('.m3d-pics').offsetParent!==null}})()"))
        c.eval(f"document.querySelector('{stage} iframe').contentWindow.document.getElementById('ctrlOpen').click()"); c.pump(0.8)

        # single-model viewers: own left panel collapsible, canvas keeps rendering
        for slug in slugs:
            c.goto(page.as_uri() + "#view/models3d/" + slug, 2.0)
            c.wait_for(f"document.querySelector(\"section.m3d-model[data-slug='{slug}'] iframe\")", 40)
            c.pump(3.5)
            sel = f"section.m3d-model[data-slug='{slug}']"
            # the panel this viewer collapses: 'left' (layout / controls) or, for Borth (its only panel #side holds the controls), 'right'
            k = c.eval(f"(function(){{var d=document.querySelector(\"{sel} iframe\").contentWindow.document;return d.getElementById('m3d-hide-left')?'left':(d.getElementById('m3d-hide-right')?'right':'')}})()")
            info = c.eval(f"(function(){{var f=document.querySelector(\"{sel} iframe\");var w=f&&f.contentWindow;if(!w||!w.__m3dPanels)return null;var d=w.document;var hb=d.getElementById('m3d-hide-{k}'),sb=d.getElementById('m3d-show-{k}');return JSON.stringify({{hide:!!hb&&hb.offsetParent!==null,show:!!sb&&!!sb.hidden}});}})()") if k else None
            ok_open = bool(info) and json.loads(info)["hide"] and json.loads(info)["show"]
            panel_ids = "(d.getElementById('left')||d.getElementById('ctrl'))" if k == "left" else "d.getElementById('side')"
            c.eval(f"document.querySelector(\"{sel} iframe\").contentWindow.document.getElementById('m3d-hide-{k}').click()"); c.pump(1.2)
            after = c.eval(f"(function(){{var w=document.querySelector(\"{sel} iframe\").contentWindow,d=w.document;var cv=[].slice.call(d.querySelectorAll('canvas')).sort(function(a,b){{return b.clientWidth*b.clientHeight-a.clientWidth*a.clientHeight}})[0];var sb=d.getElementById('m3d-show-{k}');return JSON.stringify({{panelGone:!{panel_ids}.offsetParent,btn:!sb.hidden&&/(Layout|Controls)/.test(sb.textContent),cw:cv.clientWidth,iw:w.innerWidth}});}})()")
            a = json.loads(after)
            res[f"{slug}: viewer's {k} panel is open by default and collapsible; the canvas then uses the full width; '{'Layout' if k == 'left' else 'Controls'}' button at the edge"] = bool(ok_open and a["panelGone"] and a["btn"] and a["cw"] >= a["iw"] - 4)
            if slug == slugs[0] or slug.startswith("borth"):
                shot(c, f"viewer_panel_hidden_{slug.split('-')[0]}")
            c.eval(f"document.querySelector(\"{sel} iframe\").contentWindow.document.getElementById('m3d-show-{k}').click()"); c.pump(0.6)
        res["page: no errors while exercising panels"] = not errs(c)

        # ---------------------------------------------------------------- (3) versions toggle with real models
        for slug in slugs:
            m = next(x for x in models if x["slug"] == slug)
            vs = m.get("versions") or []
            if len(vs) < 2:
                continue
            c.goto(page.as_uri() + "#view/models3d/" + slug, 2.0)
            c.wait_for(f"document.querySelector(\"section.m3d-model[data-slug='{slug}'] iframe\")", 40)
            c.pump(3.5)
            sel = f"section.m3d-model[data-slug='{slug}']"
            c.eval(f"document.querySelector(\"{sel}\").scrollIntoView()"); c.pump(0.6)
            short = slug.split("-")[0]
            shot(c, f"versions_{short}_default")
            res[f"{slug}: default version '{m['default_version']}' is pressed on load, {len(vs)} versions offered"] = bool(c.eval(f"document.querySelector(\"{sel} .m3d-vbtn[aria-pressed='true']\").getAttribute('data-m3d-ver')===\"{slug}|{m['default_version']}\""))
            for v in vs:
                if v["id"] == m["default_version"]:
                    continue
                c.click_selector(f"{sel} .m3d-vbtn[data-m3d-ver=\"{slug}|{v['id']}\"]", settle=3.0)
                c.pump(2.5)
                src = c.eval(f"document.querySelector(\"{sel} iframe\").src")
                res[f"{slug}: version '{v['id']}' is really applied in the 3D viewer (its own version selector reads it after the switch)"] = bool(c.eval(f"(function(){{var d=document.querySelector(\"{sel} iframe\").contentWindow.document;var s=[].slice.call(d.querySelectorAll('select')).filter(function(x){{return [].some.call(x.options,function(o){{return o.value==={json.dumps(v['id'])}}})}})[0];return !!s&&s.value==={json.dumps(v['id'])}}})()"))
                res[f"{slug}: version '{v['id']}' -> iframe hash, pressed state, 'Showing' line and key-number rows follow"] = bool(("version=" + v["id"]) in src and c.eval(f"document.querySelector(\"{sel} .m3d-vbtn[data-m3d-ver='{slug}|{v['id']}']\").getAttribute('aria-pressed')==='true'") and c.eval(f"document.querySelector(\"{sel} [data-vnow]\").textContent.indexOf({json.dumps(v['name'][:25])})>=0"))
                shot(c, f"versions_{short}_{v['id'][:12]}")
            c.click_selector(f"{sel} [data-m3d-vinfo]", settle=1.0)
            res[f"{slug}: the versions (i) dialog opens and lists every version"] = bool(c.eval(f"(()=>{{var d=document.querySelector('dialog.m3d-vdlg')||document.querySelector('dialog[open]');return !!d&&d.open&&d.textContent.indexOf({json.dumps(vs[0]['name'][:20])})>=0}})()"))
            shot(c, f"versions_{short}_dialog")
            c.press("Escape"); c.pump(0.5)
            # default again for the next model
            c.click_selector(f"{sel} .m3d-vbtn[data-m3d-ver=\"{slug}|{m['default_version']}\"]", settle=1.0)
        res["page: no errors while exercising versions"] = not errs(c)

        # ---------------------------------------------------------------- (4) "Match this photo"
        pm_path = BUILD / "data" / "photo_match.json"
        pm = json.loads(pm_path.read_text(encoding="utf-8")) if pm_path.is_file() else {"pictures": {}}
        for slug in slugs:
            m = next(x for x in models if x["slug"] == slug)
            pics = {pid: e for pid, e in pm["pictures"].items() if e["slug"] == slug}
            if not pics:
                continue
            gal = {g["id"]: g for g in m.get("gallery", [])}
            c.goto(page.as_uri() + "#view/models3d/" + slug, 2.0)
            c.wait_for(f"document.querySelector(\"section.m3d-model[data-slug='{slug}'] iframe\")", 40)
            c.pump(3.5)
            sel = f"section.m3d-model[data-slug='{slug}']"
            short = slug.split("-")[0]
            ids_with_button = [pid for pid in pics if pid in gal and gal[pid].get("match")]
            in_panel = [pid for pid in pics if pid in gal]
            res[f"{slug}: every eligible picture of photo_match.json that is in the picture panel carries its transform ({len(ids_with_button)} of {len(pics)}; {len(pics) - len(in_panel)} not in the panel)"] = len(ids_with_button) >= 1 and len(ids_with_button) == len(in_panel)
            first = ids_with_button[0]
            # UI flow: thumbnail -> button -> overlay -> slider -> reset
            c.eval(f"document.querySelector(\"{sel} [data-pic='{slug}|{first}']\").click()"); c.pump(0.8)
            res[f"{slug}: 'Match this photo' button appears on an eligible picture"] = bool(c.eval(f"!!document.querySelector(\"{sel} [data-m3d-match]\")"))
            other = [g["id"] for g in m.get("gallery", []) if not g.get("match") and g.get("group") != "unused"][:1]
            if other:
                c.eval(f"document.querySelector(\"{sel} [data-pic='{slug}|{other[0]}']\").click()"); c.pump(0.6)
                res[f"{slug}: no button on a picture without a documented plan-view transform"] = bool(c.eval(f"!document.querySelector(\"{sel} [data-m3d-match]\")"))
                c.eval(f"document.querySelector(\"{sel} [data-pic='{slug}|{first}']\").click()"); c.pump(0.6)
            c.eval(f"document.querySelector(\"{sel} [data-m3d-match]\").click()"); c.pump(3.0)
            st = json.loads(c.eval(f"(function(){{var w=document.querySelector(\"{sel} iframe\").contentWindow;var o=w.document.getElementById('m3d-pmo');return JSON.stringify({{active:!!(w.__m3dMatch&&w.__m3dMatch.active()),vis:!!o&&o.style.display==='block',op:o&&o.style.opacity,reset:!!document.querySelector(\"{sel} [data-m3d-pmreset]\"),slider:!!document.querySelector(\"{sel} [data-m3d-pmop]\")}})}})()"))
            res[f"{slug}: pressing the button sets a top-down camera, shows the overlay, and the panel offers the opacity slider + Reset view"] = bool(st["active"] and st["vis"] and st["reset"] and st["slider"])
            shot(c, f"photomatch_{short}")
            c.eval(f"var r=document.querySelector(\"{sel} [data-m3d-pmop]\");r.value=15;r.dispatchEvent(new Event('input',{{bubbles:true}}))"); c.pump(0.6)
            res[f"{slug}: the opacity slider changes the overlay opacity"] = bool(c.eval(f"Math.abs(parseFloat(document.querySelector(\"{sel} iframe\").contentWindow.document.getElementById('m3d-pmo').style.opacity)-0.15)<0.01"))
            c.eval(f"document.querySelector(\"{sel} [data-m3d-pmreset]\").click()"); c.pump(1.2)
            res[f"{slug}: Reset view restores the viewer (no overlay, camera back, panels back)"] = bool(c.eval(f"(function(){{var w=document.querySelector(\"{sel} iframe\").contentWindow;var o=w.document.getElementById('m3d-pmo');return !w.__m3dMatch.active()&&(!o||o.style.display==='none')&&!document.querySelector(\"{sel} [data-m3d-pmreset]\")}})()"))
            # geometry: the overlay's four corners must sit where the picture's corners project through the viewer's own camera (all pictures of the model)
            bad = []
            for pid, e in pics.items():
                if pid not in gal:
                    continue
                a, b, tx, cc, d, ty = e["to_canonical"]
                w, h = e["image_px"]
                cf = e.get("crop_frac") or [0, 0, 1, 1]
                cx0, cy0, cx1, cy1 = cf[0] * w, cf[1] * h, (cf[0] + cf[2]) * w, (cf[1] + cf[3]) * h
                corners = [(cx0, cy0), (cx1, cy0), (cx1, cy1), (cx0, cy1)]
                can = [[a * px + b * py + tx, cc * px + d * py + ty] for px, py in corners]
                spec = {"type": "m3d-camera", "mode": "plan", "center_m": e["center_m"], "up_m": e["up_m"], "width_m": e["width_m"], "height_m": e["height_m"], "crop_frac": e.get("crop_frac"), "image": page.as_uri().rsplit("/", 1)[0] + "/" + gal[pid]["web"], "opacity": 0.5}
                got = json.loads(c.eval(f"(function(){{var w=document.querySelector(\"{sel} iframe\").contentWindow;w.__m3dMatch.match({json.dumps(spec)});var o=w.document.getElementById('m3d-pmo').getBoundingClientRect();var P={json.dumps(can)}.map(function(p){{return w.__m3dMatch.screenOf(p[0],p[1])}});return JSON.stringify({{box:[[o.left,o.top],[o.right,o.top],[o.right,o.bottom],[o.left,o.bottom]],proj:P}})}})()"))
                err = max(((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5 for p1, p2 in zip(got["box"], got["proj"]))
                if err > 3.0:
                    bad.append((pid[-6:], round(err, 1)))
            res[f"{slug}: overlay corners = the picture corners projected by the viewer's camera, all {len(pics)} pictures within 3 px (rotation / mirror / scale / centre)"] = not bad or str(bad)
            c.eval(f"document.querySelector(\"{sel} iframe\").contentWindow.__m3dMatch.reset()"); c.pump(0.5)
        res["page: no errors while matching photos"] = not errs(c)
    if shots_prefix:
        res["_screenshots"] = ", ".join(shots)
    return res


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="round11_3d")
    a = ap.parse_args()
    res = dom_checks11(PAGE, a.prefix)
    lines, bad = [], 0
    for k, v in res.items():
        if k.startswith("_"):
            lines.append(f"INFO {k}: {v}")
            continue
        ok = v is True
        bad += 0 if ok else 1
        lines.append(("PASS " if ok else "FAIL ") + k + ("" if ok else f"  [{v}]"))
    (QA / f"{a.prefix}_checks.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"{len(res) - sum(1 for k in res if k.startswith('_')) - bad} passed, {bad} failed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

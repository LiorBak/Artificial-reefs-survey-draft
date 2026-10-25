"""Static checks on the built page. Writes 04_build/QA/build_check.txt.

Run after build.py:  python "04_build/src/check.py"
Checks: HTML parses with balanced tags; inline JSON parses; all 13 slugs present;
every "assets/..." path referenced exists on disk; file < 3 MB; every [R#] token
in the data resolves to a reference of its own reef; no web image is copied locally;
every [R#] marker has a source pop-up target; no rejected video is rendered; Burkitts has 0 videos.
Scale tab (2026-09-25): 13 footprints present; every polygon closed and its shoelace area within 15 %
of area_m2; every R#/S# used in a footprint derivation has a pop-up target; provenance md copied
next to the page; the retired #view/scale route falls back to the gallery (headless DOM dump via qa_shots.dump_dom); media rules
(labels on images, site-only videos link-only, hero preference, nothing from *_rejected rendered).
3D models tab (round 9, 2026-10-06; function check_models3d): every model discovered in 07_scale/shapes/*/3d has a section / viewer copy /
poster; every gallery picture has its web copy, thumbnail, annotated copies on disk and a non-empty how_used + citation (the tooltip); vendored
three.js present and no copied viewer uses a CDN or an import map; confidence badge data per model; key numbers / caveats / references present,
mandated caveat rows present; curated evidence snippets verified at build time; outline-version contract (default in the list, names + dates,
automatic caveat rows); page size (WARN above 15 MB, never a failure); then the DOM checks of src/qa_models3d.py in our own headless Chrome
(skip them with --no-dom).
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

BUILD = Path(__file__).resolve().parent.parent
HTML = BUILD / "artificial_reefs.html"
REPORT = BUILD / "QA" / "build_check.txt"
SLUGS = ["narrowneck-gold-coast", "cables-reef-wa", "prattes-reef-el-segundo", "mount-maunganui-reef",
         "opunake-reef", "boscombe-surf-reef", "kovalam-reef-india", "borth-coastal-defence-reef",
         "palm-beach-gold-coast", "southern-ocean-surf-reef-albany", "burkitts-reef-bargara",
         "bunbury-airwave", "mexico-reef-2026-unnamed"]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Balance(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.data_json = [], [], None
        self._in_data = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and a.get("id") == "data":
            self._in_data = True
            self.data_json = ""
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "script":
            self._in_data = False
        if tag in VOID:
            return
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"unexpected </{tag}> at {self.getpos()} (open: {self.stack[-3:]})")
            if tag in self.stack:
                while self.stack and self.stack.pop() != tag:
                    pass
        else:
            self.stack.pop()

    def handle_data(self, data):
        if self._in_data:
            self.data_json += data


def check_models3d(raw: str, out: list, with_dom: bool = True) -> int:
    """Checks of the '3D models' tab. Appends PASS/FAIL/INFO/WARN lines to out; returns the number of failures."""
    fails = 0

    def check(ok, msg):
        nonlocal fails
        out.append(("PASS " if ok else "FAIL ") + "[3D] " + msg)
        if not ok:
            fails += 1

    root = BUILD.parent
    m = re.search(r'<script id="data3d" type="application/json">(.*?)</script>', raw, re.S)
    check(bool(m), "data3d JSON present in the page")
    if not m:
        return fails
    d = json.loads(m.group(1))
    models = d.get("models", [])
    slugs = [x["slug"] for x in models]
    check('data-view="models3d"' in raw and 'id="view-models3d"' in raw and "ReefModels3D" in raw, "3D tab button, view section and script are in the page")

    # 1. every model discovered on disk has a section (data) + viewer copy + poster
    try:
        held = json.loads((BUILD / "data" / "models3d_hold.json").read_text(encoding="utf-8")).get("hold", {})   # round 11: models still being built elsewhere
    except (OSError, ValueError):
        held = {}
    disc = sorted(p.parent.parent.name for p in (root / "07_scale" / "shapes").glob("*/3d/index.html") if (p.parent / "model.js").is_file() and p.parent.parent.name not in held)
    check(sorted(slugs) == disc, f"every discovered model has a section: disk {disc} vs page {sorted(slugs)}" + (f" (held, not built: {sorted(held)})" if held else ""))
    feas = sorted(p.parent.parent.name for p in (root / "07_scale" / "shapes").glob("*/3d/FEASIBILITY.md") if not (p.parent / "model.js").is_file())
    check(sorted(f["slug"] for f in d.get("feasibility", [])) == feas, f"every reef with only a FEASIBILITY.md has a 'not modelled' card ({feas})")
    for x in models:
        vd = BUILD / "3d" / x["slug"]
        check((vd / "index.html").is_file() and (vd / "model.js").is_file(), f"{x['slug']}: viewer copy 3d/{x['slug']}/index.html + model.js exist")
        if x.get("poster"):
            check((BUILD / x["poster"]).is_file(), f"{x['slug']}: poster {x['poster']} exists")
    # 2. vendored three.js + no CDN in any copied viewer
    vend = BUILD / "3d" / "vendor"
    need = ["three.module.js", "three.bundle.js", "OrbitControls.js"]
    have = {p.name for p in vend.rglob("*") if p.is_file()}
    check(all(n in have for n in need), f"vendored three.js present ({need}; vendor holds {len(have)} files)")
    cdn = []
    for x in models:
        vh = BUILD / "3d" / x["slug"] / "index.html"
        h = vh.read_text(encoding="utf-8", errors="replace") if vh.is_file() else ""
        if re.search(r"<script[^>]+src=[\"']https?://|import\s[^;]*from\s*[\"']https?://|<link[^>]+href=[\"']https?://|type=[\"']importmap|cdn\.|jsdelivr|unpkg", h):
            cdn.append(x["slug"])
        for ref in re.findall(r"<script[^>]+src=[\"']([^\"'#?]+)", h):
            if not ref.startswith(("http", "data:")) and not (BUILD / "3d" / x["slug"] / ref).resolve().is_file():
                cdn.append(f"{x['slug']}: missing {ref}")
    check(not cdn, f"no copied viewer uses a CDN / import map and every script it loads exists (bad={cdn})")
    # 3. gallery: files on disk, tooltip content
    miss, no_tip = [], []
    n_pics = 0
    for x in models:
        for pic in x.get("gallery", []):
            n_pics += 1
            files = [pic.get("web"), pic.get("thumb")] + [a.get("web") for a in pic.get("annotated", [])]
            miss += [f for f in files if not f or not (BUILD / f).is_file()]
            if not (pic.get("how_used") or "").strip() or not (pic.get("citation") or "").strip():
                no_tip.append(f"{x['slug']}:{pic.get('id')}")
            if not pic.get("group"):
                no_tip.append(f"{x['slug']}:{pic.get('id')} no group")
    check(not miss, f"all gallery files exist on disk ({n_pics} pictures; web copy, thumbnail, annotated copies; missing={miss[:6]})")
    check(not no_tip, f"every gallery picture has a non-empty how_used + citation for its tooltip and a group (bad={no_tip[:6]})")
    # 4. per-model content
    bad = []
    for x in models:
        c = x.get("confidence") or {}
        if c.get("level") not in ("high", "medium", "low") or len((c.get("reason_short") or c.get("reason") or "").strip()) < 20:
            bad.append(f"{x['slug']}: confidence")
        if not x.get("key_numbers"):
            bad.append(f"{x['slug']}: key numbers")
        if not (x.get("ve_note") or d.get("ve_generic")):
            bad.append(f"{x['slug']}: vertical exaggeration note")
        if not x.get("caveats"):
            bad.append(f"{x['slug']}: caveat rows")
        if not x.get("ref_ids"):
            bad.append(f"{x['slug']}: references")
        if not (x.get("state_short") or "").strip():
            bad.append(f"{x['slug']}: state modelled")
    check(not bad, f"every model has confidence badge data, state, vertical-exaggeration note, key numbers, caveats and references (bad={bad})")
    # 5. mandated caveat rows (build_3d_tab.md section 3c)
    must = {"palm-beach-gold-coast": ["volume and height", "charted crest", "concept design"], "prattes-reef-el-segundo": ["^volume", "crest level", "reef position"],
            "boscombe-surf-reef": ["^volume", "vertical datum", "emodnet"], "bunbury-airwave": ["state and verdict", "crest depth"],
            "mount-maunganui-reef": ["^volume", "bed level", "vertical datum"],
            "borth-coastal-defence-reef": ["^volume", "offshore seabed", "vertical datum"]}
    lack = []
    for x in models:
        qs = [(c.get("q") or "").lower() for c in x.get("caveats", [])]
        for pat in must.get(x["slug"], []):
            if not any(re.search(pat, q) for q in qs):
                lack.append(f"{x['slug']}: {pat}")
    check(not lack, f"mandated caveat rows present (lacking={lack})")
    n_cav = sum(len(x.get("caveats", [])) for x in models)
    refs = d.get("references", [])
    check(len(refs) > 0 and all(r.get("id") and r.get("text") for r in refs), f"merged reference list: {len(refs)} entries, each with id and text")
    ver = d.get("meta", {}).get("verify", {})
    check(not ver.get("failed"), f"curated quotes / evidence snippets verified against the documents at build time ({ver.get('checked')} checked, failed={ver.get('failed', [])[:3]})")
    check(bool(d.get("methods_html")), "project-wide methods text rendered")
    check(all(len(q["quote"].split()) <= 25 for x in models for q in x.get("relied", [])), "every relied-on quotation is <= 25 words")
    # 6. versions contract
    vbad = []
    n_vm = 0
    for x in models:
        vs = x.get("versions") or []
        if not vs:
            continue
        n_vm += 1
        ids = [v["id"] for v in vs]
        if x.get("default_version") not in ids:
            vbad.append(f"{x['slug']}: default_version not in versions")
        for v in vs:
            if not (v.get("name") or "").strip() or not (v.get("date") or "").strip():
                vbad.append(f"{x['slug']}:{v['id']}: needs name and date")
        dflt = next(v for v in vs if v["id"] == x["default_version"]) if x.get("default_version") in ids else None
        if dflt:
            for v in vs:
                if v["id"] != dflt["id"] and (v.get("area_m2") is not None and dflt.get("area_m2") is not None):
                    if not any(c.get("origin") == "versions" and "area" in c["q"].lower() and v["name"] in c.get("stated", "") for c in x["caveats"]):
                        vbad.append(f"{x['slug']}:{v['id']}: no automatic caveat row for the footprint difference")
        if len(vs) > 1 and not (x.get("versions_info") or "").strip():
            vbad.append(f"{x['slug']}: versions_info missing (the (i) pop-up has no text)")
    check(not vbad, f"outline-version contract for the {n_vm} model(s) with versions (bad={vbad})")
    out.append(f"INFO [3D] {len(models)} models {[x['slug'] + ' - ' + x['confidence']['level'] for x in models]}; pictures {n_pics}; caveat rows {n_cav}; references {len(refs)}; "
               f"with versions {n_vm}; not yet modelled {[n['slug'] for n in d.get('not_yet', [])]}")

    # 6b. round 10: sticky navigation, back bar in every copied viewer, combined "All (compare)" scene
    check('id="topnav"' in raw and raw.find('id="topnav"') < raw.find('data-view="models3d" aria-pressed') < raw.find('<header class="site-head"'),
          "sticky top navigation (#topnav) holds the view buttons and comes before the site header")
    check('id="to-top"' in raw, "back-to-top control present")
    nobar = []
    for x in models + [{"slug": "combined"}]:
        vh = BUILD / "3d" / x["slug"] / "index.html"
        h = vh.read_text(encoding="utf-8", errors="replace") if vh.is_file() else ""
        if 'class="m3d-topbar"' not in h or "Back to the page" not in h or "../../artificial_reefs.html#view/models3d/" not in h or "m3d-embedded" not in h:
            nobar.append(x["slug"])
    check(not nobar, f"every copied viewer (and the combined viewer) has the injected 'Back to the page' bar, hidden when framed (missing={nobar})")
    comb = d.get("combined")
    if models:
        check(bool(comb) and bool(comb.get("models")), "combined 'All (compare)' data block present in models3d.json")
    if comb:
        ci = BUILD / "3d" / "combined" / "index.html"
        h = ci.read_text(encoding="utf-8", errors="replace") if ci.is_file() else ""
        check(bool(h) and not re.search(r"<script[^>]+src=[\"']https?://|type=[\"']importmap|cdn\.|jsdelivr|unpkg", h), "combined viewer 3d/combined/index.html exists and uses no CDN / import map")
        miss_s = [s for s in re.findall(r"<script[^>]+src=[\"']([^\"'#?]+)", h) if not (BUILD / "3d" / "combined" / s).resolve().is_file()]
        check(not miss_s, f"every script of the combined viewer exists (missing={miss_s})")
        okm = [c for c in comb["models"] if c["status"] == "ok"]
        notm = [c for c in comb["models"] if c["status"] != "ok"]
        check(all((BUILD / "3d" / "combined" / f"{c['slug']}.js").is_file() and f"{c['slug']}.js" in h for c in okm), f"every exported model has its data file and is loaded by the combined viewer ({[c['slug'] for c in okm]})")
        check(len(okm) + len(notm) == len(models) and all(c.get("reason") for c in notm), f"every model is either in the comparison or listed as 'not in comparison' with a reason ({[c['slug'] + ': ' + c['reason'] for c in notm]})")
        for c in okm:
            for ch in c.get("checks", []):
                check(ch["ok"], f"combined export {c['slug']}: {ch['name']}: err {ch['err']:.3g} {ch['unit']} (tolerance {ch['tol']:g})")
        out.append("INFO [3D] combined scene: " + "; ".join(f"{c['slug']} {c['status']}" for c in comb["models"]) + f"; tolerances {comb.get('tolerance')}")

    # 7. sizes
    def tree(p):
        return sum(f.stat().st_size for f in p.rglob("*") if f.is_file()) / (1024 * 1024) if p.is_dir() else 0
    out.append(f"INFO [3D] folder sizes: assets/images {tree(BUILD / 'assets' / 'images'):.1f} MB, 3d/ {tree(BUILD / '3d'):.1f} MB (page itself {len(raw) / (1024 * 1024):.2f} MB)")
    # 8. DOM checks in our own headless Chrome
    if with_dom:
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            import qa_models3d  # noqa: PLC0415
            res = qa_models3d.dom_checks(HTML)
            for k, v in res.items():
                if k.startswith("_"):
                    continue
                check(v is True, f"DOM: {k}" + ("" if v is True else f"  -> {v}"))
        except Exception as e:  # noqa: BLE001
            check(False, f"DOM checks could not run: {type(e).__name__}: {e}")
    else:
        out.append("INFO [3D] DOM checks skipped (--no-dom)")
    return fails


def main() -> int:
    out, fails = [], 0

    def check(ok, msg):
        nonlocal fails
        out.append(("PASS " if ok else "FAIL ") + msg)
        if not ok:
            fails += 1

    raw = HTML.read_text(encoding="utf-8")
    size = HTML.stat().st_size
    MB = 1024 * 1024
    if size > 15 * MB:
        out.append(f"WARN page size {size / MB:.1f} MB is above 15 MB (inline data too large: move data out of the page or trim it)")
    elif size > 3 * MB:
        out.append(f"INFO page size {size / MB:.1f} MB (between 3 and 15 MB: fine, WARN above 15 MB)")
    else:
        check(True, f"file size {size / 1024:.0f} KB < 3 MB")

    p = Balance()
    p.feed(raw)
    p.close()
    check(not p.errors and not p.stack, f"HTML parses with balanced tags (errors={p.errors[:3]}, unclosed={p.stack})")
    check("<title>Artificial Surf Reefs Survey</title>" in raw, "title is 'Artificial Surf Reefs Survey'")

    data = json.loads(p.data_json)
    reefs = data["reefs"]
    got = {r["slug"] for r in reefs}
    check(set(SLUGS) == got and len(reefs) == 13, f"data has exactly the 13 slugs (missing={set(SLUGS) - got}, extra={got - set(SLUGS)})")
    check(all(s in raw for s in SLUGS), "all 13 slugs appear in the HTML")

    asset_paths = sorted(set(re.findall(r"(?<![\w/.:%-])assets/[^\"'\s)<>\\]+", raw)))   # not when part of a longer path / URL (reference links contain /assets/)
    missing = [a for a in asset_paths if not (BUILD / a).is_file()]
    check(not missing, f"{len(asset_paths)} referenced assets/ paths exist on disk (missing={missing})")
    on_disk = sorted(str(f.relative_to(BUILD)).replace("\\", "/") for f in (BUILD / "assets").rglob("*") if f.is_file())
    try:
        _held = list(json.loads((BUILD / "data" / "models3d_hold.json").read_text(encoding="utf-8")).get("hold", {}))
    except (OSError, ValueError):
        _held = []
    unused = [f for f in on_disk if f not in asset_paths and not any(f.startswith(f"assets/images/{h}/") for h in _held)]   # stale copies of a held model are ignored (round 11)
    check(not unused, f"no unreferenced files in assets/ ({len(on_disk)} files; unused={unused})")

    bad_refs = []
    for r in reefs:
        ids = {x["id"] for x in r.get("references", [])}
        blob = json.dumps({k: v for k, v in r.items() if k != "references"}, ensure_ascii=False)
        for tok in set(re.findall(r"\[(R\d+)\]", blob)):
            if tok not in ids:
                bad_refs.append(f"{r['slug']}:{tok}")
    check(not bad_refs, f"every [R#] token resolves to its reef's references (unresolved={bad_refs})")

    # --- source pop-ups: every [R#] marker must have something to open ---------------------
    # The page turns each [R#] into <button class="ref-mark" data-ref="R#"> that opens the one
    # #ref-pop element inside the reef <dialog>, filled from that reef's references[] entry.
    dlg_m = re.search(r'<dialog id="reef-dialog".*?</dialog>', raw, re.S)
    check(bool(dlg_m) and 'id="ref-pop"' in dlg_m.group(0),
          "source pop-up #ref-pop exists inside the reef <dialog> (renders in the top layer)")
    js_ok = all(x in raw for x in ('class="ref-mark', 'data-ref="', 'aria-controls="ref-pop"', 'function openPop', 'function positionPop'))
    check(js_ok, "markers are rendered as pop-up buttons (ref-mark / data-ref / aria-controls=ref-pop, openPop, positionPop)")
    no_target, n_markers = [], 0
    for r in reefs:
        refs = {x["id"]: x for x in r.get("references", [])}
        blob = json.dumps({k: v for k, v in r.items() if k != "references"}, ensure_ascii=False)
        for tok in re.findall(r"\[(R\d+)\]", blob):
            n_markers += 1
            ref = refs.get(tok)
            if not ref or not (ref.get("citation") or "").strip():
                no_target.append(f"{r['slug']}:{tok}")
        for rv in r.get("reviews", []):
            if rv.get("ref_id"):
                n_markers += 1
                if rv["ref_id"] not in refs:
                    no_target.append(f"{r['slug']}:review->{rv['ref_id']}")
    check(not no_target, f"every one of {n_markers} [R#] markers has a pop-up target with citation text (missing={no_target[:10]})")
    no_url = sum(1 for r in reefs for x in r.get("references", []) if not (x.get("url") or "").strip())
    out.append(f"INFO references without a URL (pop-up shows 'internal note — no URL'): {no_url}")
    lost = [f"{r['slug']}:{rv.get('who')}" for r in reefs for rv in r.get("reviews", []) if not rv.get("url") and not rv.get("ref_id")]
    check(not lost, f"every review has a source link or a reference pop-up (none={lost})")

    # --- rejected videos must not reach the page ------------------------------------------
    cards = BUILD.parent / "02_research" / "reefs"
    rejected = []
    for slug in SLUGS:
        cp = cards / f"{slug}.json"
        if cp.is_file():
            card = json.loads(cp.read_text(encoding="utf-8"))
            for v in card.get("videos_rejected") or []:
                rejected += [x for x in (v.get("video_id"), v.get("url"), v.get("title")) if x]
    # 2026-10-10: the collapsed 'Checked, nothing useful' section may NAME a rejected video / image as a source that gave nothing (text + link, never an embed or a reference),
    # so the leak tests below look at the page without the dead_ends data
    raw_nd = raw
    try:
        _dnd = json.loads(p.data_json)
        for _r in _dnd["reefs"]:
            _r.pop("dead_ends", None)
        raw_nd = raw.replace(p.data_json, json.dumps(_dnd, ensure_ascii=False)) if p.data_json in raw else raw
    except (ValueError, KeyError):
        pass
    out.append(f"INFO leak tests run on the page without the dead-ends data ({len(raw) - len(raw_nd):,} characters removed)")
    leaked = [x for x in rejected if x in raw_nd]
    check("videos_rejected" not in p.data_json and not leaked,
          f"no videos_rejected content rendered ({len(rejected)} rejected ids/urls/titles checked; leaked={leaked})")
    bk = next((r for r in reefs if r["slug"] == "burkitts-reef-bargara"), {})
    bk_hero = (bk.get("hero_image") or {}).get("url") or ""
    check(bk and len(bk.get("videos") or []) == 0 and "youtube" not in bk_hero and "ytimg" not in bk_hero,
          f"Burkitts shows 0 videos (videos={len(bk.get('videos') or [])}, hero={bk_hero[:60]})")
    gem = [(r["slug"], x.get("who") or x.get("id")) for r in reefs for x in (r.get("reviews", []) + r.get("references", [])) if x.get("origin")]
    out.append(f"INFO items tagged with an origin (e.g. via Gemini survey, verified): {len(gem)} {gem}")

    # --- Scale tab: footprints --------------------------------------------------------------
    def shoelace(ring):
        return abs(sum(ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1] for i in range(len(ring) - 1))) / 2

    fps = {r["slug"]: r.get("footprint") for r in reefs}
    missing_fp = [s for s in SLUGS if not fps.get(s)]
    check(not missing_fp, f"13 footprints present (missing={missing_fp})")
    not_closed, bad_area, area_rows = [], [], []
    for s, f in fps.items():
        if not f or f.get("display") is False:
            continue            # hidden reefs carry no outline (checked below)
        polys = f.get("polygons") or []
        if not polys or any(len(rg) < 4 or rg[0] != rg[-1] for rg in polys):
            not_closed.append(s)
        a = sum(shoelace(rg) for rg in polys)
        stated = f.get("area_m2") or 0
        dev = abs(a - stated) / stated if stated else 1
        area_rows.append(f"{s}: computed {a:,.0f} vs area_m2 {stated:,.0f} ({dev * 100:.1f} %)")
        if dev > 0.15:
            bad_area.append(f"{s} ({dev * 100:.1f} %)")
    check(not not_closed, f"every footprint polygon is closed (not closed={not_closed})")
    check(not bad_area, f"every polygon's computed area is within 15 % of area_m2 (outside={bad_area})")
    out.extend("INFO area " + x for x in area_rows)
    no_target_fp, n_ids = [], 0
    for r in reefs:
        f = r.get("footprint")
        if not f or f.get("display") is False:
            continue
        refs = {x["id"]: x for x in r.get("references", [])}
        text = json.dumps(f.get("derivation"), ensure_ascii=False)
        for tok in sorted(set(re.findall(r"\b([RS]\d{1,3})\b", text))):
            n_ids += 1
            ref = refs.get(tok)
            if not ref or not (ref.get("citation") or "").strip():
                no_target_fp.append(f"{r['slug']}:{tok}")
    check(not no_target_fp, f"every one of {n_ids} R#/S# ids used in footprint derivations has a pop-up target (missing={no_target_fp})")
    docs_missing = [s for s, f in fps.items() if f and f.get("display") is not False and not (BUILD / (f.get("provenance_md") or "x")).is_file()]
    check(not docs_missing, f"provenance md for every footprint copied to docs/scale/ (missing={docs_missing})")
    # 2026-10-10: Map and Scale tabs removed; the footprint section of the reef dialog (footprint.js) stays = rule 1 traceability
    check("function linkRefs" in raw and "window.ReefScale" in raw and "function detailSection" in raw,
          "footprint detail code (reef dialog 'Footprint & how we drew it') is in the page")
    check(all(x not in raw.lower() for x in ('id="view-scale"', 'id="view-map"', 'data-view="scale"', 'data-view="map"', "leaflet.min", "l.map(", "tile.openstreetmap")),
          "no Map / Scale view, button, Leaflet or map-tile code remains in the page")
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import qa_shots
        exe, sdom = qa_shots.dump_dom(HTML.as_uri() + "#view/scale")
        if not sdom:
            out.append("INFO no headless browser available: retired-route check skipped")
        else:
            for k, v in qa_shots.retired_view_checks(sdom).items():
                check(v, f"retired #view/scale route (headless DOM dump): {k}")
    except Exception as e:  # noqa: BLE001
        check(False, f"retired-route check crashed: {e!r}")

    # --- 2026-10-10 (Lior): "don't show the shape of reefs you don't know" + a Google Maps link per reef --------------------
    ROOT = BUILD.parent
    must_hide = ["mexico-reef-2026-unnamed", "opunake-reef", "burkitts-reef-bargara", "kovalam-reef-india"]
    hide_expected = set(must_hide)
    for s in SLUGS:
        fpj = ROOT / "07_scale" / "reefs" / f"{s}.footprint.json"
        shp = ROOT / "07_scale" / "shapes" / s / "shape.json"
        rawfp = json.loads(fpj.read_text(encoding="utf-8")) if fpj.is_file() else {}
        sh = json.loads(shp.read_text(encoding="utf-8")) if shp.is_file() else None
        if rawfp.get("display") is False or rawfp.get("DO_NOT_DISPLAY") or sh is None or str(sh.get("status")).lower() not in ("verified", "traced", "verified with issues"):
            hide_expected.add(s)
    by = {r["slug"]: r for r in reefs}
    wrong = [s for s in SLUGS if (by[s].get("footprint") or {}).get("display") is False] 
    check(set(wrong) == hide_expected, f"hidden-shape reefs = the 4 decided (Mexico, Opunake, Burkitts, Kovalam) + anything whose shape.json is missing / not traced or verified (compiled hidden={sorted(wrong)}, expected={sorted(hide_expected)})")
    leak = [s for s in hide_expected if (by[s].get("footprint") or {}).get("polygons") or (by[s].get("footprint") or {}).get("geom")]
    check(not leak, f"no hidden reef carries an outline polygon in the page data (leaking={leak})")
    nohint = [s for s in hide_expected if not (by[s].get("footprint") or {}).get("hidden_reason")]
    check(not nohint, f"every hidden reef has a plain-text reason (missing={nohint})")
    no_feas = [s for s in hide_expected if not (BUILD / ((by[s].get("footprint") or {}).get("docs") or {}).get("feasibility", "x")).is_file()]
    check(not no_feas, f"every hidden reef links a FEASIBILITY.md copy next to the page (missing={no_feas})")
    shown_bad = [s for s in SLUGS if s not in hide_expected and not (by[s].get("footprint") or {}).get("outline_source")]
    check(not shown_bad, f"every drawn outline comes from shape.json (has an outline_source) (not from the old text-derived footprint; bad={shown_bad})")

    mapsre = re.compile(r"^https://www\.google\.com/maps/search/\?api=1&query=-?\d{1,3}\.\d+,-?\d{1,3}\.\d+$")
    bad_loc, no_loc = [], []
    for s in SLUGS:
        L = by[s].get("location") or {}
        if L.get("lat") is not None:
            if not (mapsre.match(L.get("maps_url") or "") and L["maps_url"].endswith(f"query={L['lat']},{L['lon']}") and -90 <= L["lat"] <= 90 and -180 <= L["lon"] <= 180):
                bad_loc.append(s)
            if L.get("status") not in ("ok", "approximate"):
                bad_loc.append(s + ":status")
        elif L.get("maps_url"):
            bad_loc.append(s + ":link without coordinates")
        else:
            no_loc.append(s)
    check(not bad_loc, f"every reef with coordinates has a Google Maps link in the right format https://www.google.com/maps/search/?api=1&query=LAT,LON (bad={bad_loc})")
    check(all(by[s].get("location") for s in SLUGS) and set(no_loc) <= {"mexico-reef-2026-unnamed"},
          f"only reefs with no published coordinates have no link (no link: {no_loc}; expected only Mexico)")
    out.append("INFO locations: " + "; ".join(f"{s}={(by[s].get('location') or {}).get('status')}:{(by[s].get('location') or {}).get('lat')},{(by[s].get('location') or {}).get('lon')}" for s in SLUGS))
    # "Open location in..." block (Lior 2026-10-13): data and URL formats
    earthre = re.compile(r"^https://earth\.google\.com/web/@-?\d{1,3}\.\d+,-?\d{1,3}\.\d+,0a,1000d,35y,0h,0t,0r$")
    ddre = re.compile(r"^-?\d{1,3}\.\d{5}, -?\d{1,3}\.\d{5}$")
    dmre = re.compile(r"^\d{1,2}\u00b0\d{2}\.\d{3}'[NS] \d{1,3}\u00b0\d{2}\.\d{3}'[EW]$")
    bad_blk = []
    for s in SLUGS:
        L = by[s].get("location") or {}
        if L.get("lat") is None:
            if any(k in L for k in ("dd", "dm", "earth_url", "outline_latlon")):
                bad_blk.append(s + ":links without coordinates")
            continue
        if not (ddre.match(L.get("dd") or "") and L["dd"] == f"{L['lat']:.5f}, {L['lon']:.5f}" and dmre.match(L.get("dm") or "")
                and earthre.match(L.get("earth_url") or "") and L["earth_url"] == f"https://earth.google.com/web/@{L['lat']},{L['lon']},0a,1000d,35y,0h,0t,0r"):
            bad_blk.append(s)
    check(not bad_blk, f"location block data: 5-decimal 'lat, lon' text, degrees-decimal-minutes text, Google Earth web URL format (bad={bad_blk})")
    kml_out = sorted(s for s in SLUGS if (by[s].get("location") or {}).get("outline_latlon"))
    def _georef(s):
        try:
            return bool((((json.loads((ROOT / "07_scale" / "shapes" / s / "shape.json").read_text(encoding="utf-8")) or {}).get("geo") or {}).get("polygons_latlon")))
        except Exception:  # noqa: BLE001
            return False
    # a shown reef without a georeferenced outline (Prattes: coordinates disagree; Bunbury: estimated centre) gets its point only: a polygon would be misplaced
    kml_exp = sorted(s for s in SLUGS if s not in hide_expected and (by[s].get("location") or {}).get("lat") is not None and _georef(s))
    check(kml_out == kml_exp and not any(s in hide_expected for s in kml_out) and all(len(rg) >= 3 for s in kml_out for rg in by[s]["location"]["outline_latlon"]),
          f"KML outline data only for reefs whose outline is shown AND georeferenced in shape.json geo ({len(kml_out)} reefs; never for the hidden {sorted(hide_expected)}; expected={kml_exp}; got={kml_out})")
    try:
        import qa_shots as _qs
        _exe, _dom = _qs.dump_dom(HTML.as_uri())
        if _dom:
            _body = _qs.strip_scripts(_dom)
            _tiles = re.findall(r'<article class="tile" data-slug="([a-z0-9-]+)">(.*?)</article>', _body, re.S)
            _tb = {s: t for s, t in _tiles}
            # 2026-10-24 (Lior D10, D11): reefs in data/page_overrides.json gallery_excluded / announced have no Gallery tile and no Table row
            _ov = json.loads((BUILD / "data" / "page_overrides.json").read_text(encoding="utf-8"))
            _off = set(_ov.get("gallery_excluded", {})) | set(_ov.get("announced", {}))
            _gal = [s for s in SLUGS if s not in _off]
            check(not (_off & set(_tb)), f"[gallery] no tile for the reefs Lior took out of the Gallery ({sorted(_off)})")
            bad_t = [s for s in _gal if (by[s].get("location") or {}).get("lat") is not None and
                     not ('class="loc-menu"' in _tb.get(s, "") and 'data-loc-copy="' + by[s]["location"]["dd"] + '"' in _tb.get(s, "") and 'data-loc-kml="' + s + '"' in _tb.get(s, "")
                          and by[s]["location"]["earth_url"] in _tb.get(s, "") and 'rel="noopener noreferrer"' in _tb.get(s, ""))]
            check(not bad_t and len(_tb) == len(_gal), f"[gallery] every reef with coordinates has the 'Open location in' menu in its tile (copy, KML, Google Earth; bad={bad_t}; tiles={len(_tb)})")
            check('data-loc-kml="all"' in _body, "[gallery] 'All reefs (KML)' button in the controls header")
            check('Navionics: paste the copied coordinates' in "".join(_tb.values()) and "webapp.navionics.com" not in _body, "Navionics: paste-the-coordinates hint, no Navionics web link (webapp.navionics.com redirects to a Garmin page, tested 2026-10-13)")
            _m3 = [m["slug"] for m in json.loads((BUILD / "data" / "models3d.json").read_text(encoding="utf-8"))["models"]]
            bad_3 = []
            for s in _m3:
                _e, _d = _qs.dump_dom(HTML.as_uri() + "#view/models3d/" + s, _exe)
                _hd = re.search(r'<header class="m3d-mhead">.*?</header>', _qs.strip_scripts(_d) if _d else "", re.S)
                _hs = _hd.group(0) if _hd else ""
                L = by[s].get("location") or {}
                if not (L.get("dd") and 'class="m3d-loc"' in _d and 'data-loc-copy="' + L["dd"] + '"' in _d and 'data-loc-kml="' + s + '"' in _d and L["earth_url"] in _d):
                    bad_3.append(s)
            check(not bad_3, f"[3D tab] every model entry has the 'Open location in' block (copy, KML, Google Earth; models={len(_m3)}; bad={bad_3})")
        else:
            out.append("INFO no headless browser available: gallery / 3D location-block DOM checks skipped")
    except Exception as exc:  # noqa: BLE001
        check(False, f"location block DOM checks crashed: {exc}")
    # dead ends (Lior 2026-10-10): the data of every reef equals its 02_research/dead_ends/<slug>.json
    de_files = {}
    for s in SLUGS:
        dp = ROOT / "02_research" / "dead_ends" / f"{s}.json"
        de_files[s] = json.loads(dp.read_text(encoding="utf-8")).get("entries", []) if dp.is_file() else []
    bad_de = [s for s in SLUGS if len(by[s].get("dead_ends") or []) != len(de_files[s]) or not de_files[s]
              or any(e.get("what") != d.get("what") or e.get("result") != d.get("result") for e, d in zip(by[s].get("dead_ends") or [], de_files[s]))]
    check(not bad_de, f"dead ends: all 13 reefs carry their 02_research/dead_ends/<slug>.json entries in the page data, same count and order ({sum(len(v) for v in de_files.values())} entries; bad={bad_de})")
    leak_de = [s for s in SLUGS if any(e["what"] in json.dumps(by[s].get("references") or [], ensure_ascii=False) for e in by[s].get("dead_ends") or [])]
    check(not leak_de, f"dead ends are not in the references list (leaking={leak_de})")
    # DOM: open every reef dialog headlessly
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import qa_shots
        exe0 = None
        for s in SLUGS:
            exe0, dom = qa_shots.dump_dom(HTML.as_uri() + "#reef/" + s, exe0)
            if not dom:
                out.append("INFO no headless browser available: dialog drawing / Maps-link DOM checks skipped")
                break
            body = qa_shots.strip_scripts(dom)
            dlg_m = re.search(r'<dialog id="reef-dialog".*?</dialog>', body, re.S)
            dd = dlg_m.group(0) if dlg_m else ""
            hid = s in hide_expected
            has_svg = 'class="sc-svg"' in dd or 'class="sc-reef"' in dd
            check(bool(dd) and (has_svg != hid), f"[dialog {s}] {'no outline drawn (shape not drawn note present)' if hid else 'outline drawn'}" +
                  ("" if (bool(dd) and (has_svg != hid)) else f" (dialog found={bool(dd)}, svg={has_svg})"))
            if hid:
                check("Shape not drawn" in dd, f"[dialog {s}] shows the 'Shape not drawn' text")
            L = by[s].get("location") or {}
            if L.get("maps_url"):
                ok = (f'href="{L["maps_url"].replace("&", "&amp;")}"' in dd and 'target="_blank"' in dd and "noopener" in dd and "Google Maps" in dd
                      and (L["approximate"] is False or "approximate location" in dd))
                check(ok, f"[dialog {s}] Location link to Google Maps (new tab, noopener{', labelled approximate' if L['approximate'] else ''})")
                check('class="loc-block"' in dd and 'data-loc-copy="' + L["dd"] + '"' in dd and 'data-loc-kml="' + s + '"' in dd and L["earth_url"] in dd and "Navionics: paste" in dd,
                      f"[dialog {s}] 'Open location in' block: coordinates + Copy, Google Earth web, KML, Navionics hint")
            else:
                dd_main = re.sub(r'<details class="acc acc-de".*?</details>', "", dd, flags=re.S)       # the dead-ends section may link a Google Maps page it checked
                check("location: not published" in dd.lower() and "google.com/maps" not in dd_main, f"[dialog {s}] says location not published and has no map link (outside the dead-ends section)")
            # 2026-10-10 (Lior): "Checked, nothing useful (N)" = last section of the dialog, closed by default, not part of References, N = entries in the file
            n_de = len(de_files.get(s, []))
            art_m = re.search(r'<article class="detail">.*?</article>', dd, re.S)
            art = art_m.group(0) if art_m else dd
            m_de = re.search(r'<details class="acc acc-de"( open="")? id="d-dead-ends">(.*?)</details>', art, re.S) or re.search(r'<details class="acc acc-de" id="d-dead-ends"( open="")?>(.*?)</details>', art, re.S)
            body_de = m_de.group(2) if m_de else ""
            n_items = body_de.count('class="de-item"')
            refs_m = re.search(r'<details class="acc" id="d-references"[^>]*>(.*?)</details>', art, re.S)
            is_closed = bool(m_de) and not m_de.group(1)
            is_last = art.rfind("<details") == art.find('<details class="acc acc-de"') and art.find('id="d-references"') < art.find('id="d-dead-ends"')
            ok_de = (bool(m_de) and is_closed and f"Checked, nothing useful ({n_de})" in art and n_items == n_de
                     and bool(refs_m) and "de-item" not in refs_m.group(1) and is_last)
            check(ok_de, f"[dialog {s}] 'Checked, nothing useful ({n_de})' section: present, closed by default, last section, after (not inside) References, {n_de} entries as in dead_ends/{s}.json"
                  + ("" if ok_de else f" (found={bool(m_de)}, closed={is_closed}, items={n_items}, last={is_last})"))
        else:
            tdom = qa_shots.dump_dom(HTML.as_uri() + "#view/table", exe0)[1]
            tb = qa_shots.strip_scripts(tdom)
            n_links = len(re.findall(r'<td class="loc"><a class="loc-link" href="https://www\.google\.com/maps/search/\?api=1&amp;query=', tb))
            _off2 = set(json.loads((BUILD / "data" / "page_overrides.json").read_text(encoding="utf-8")).get("gallery_excluded", {}))   # no Table row (Lior D10)
            n_expect = sum(1 for s in SLUGS if (by[s].get("location") or {}).get("maps_url") and s not in _off2)
            check(n_links == n_expect and 'class="loc"' in tb, f"table: a Location link in every row that has coordinates ({n_links} of {n_expect}; Mexico shows 'not published')")
    except Exception as e:  # noqa: BLE001
        check(False, f"dialog / Maps-link DOM check crashed: {e!r}")

    # --- media rules (2026-09-25 media re-check) -------------------------------------------
    unlabelled = [f"{r['slug']}:{i}" for r in reefs for i, im in enumerate(r.get("images", [])) if im.get("shows") and not im.get("shows_label")]
    check(not unlabelled, f"every image with a 'shows' verdict carries a caption label (missing={unlabelled})")
    bad_site = []
    for r in reefs:
        for v in r.get("videos", []):
            if str(v.get("about", "")).lower().startswith("site only"):
                if not v.get("link_only") or v.get("frames"):
                    bad_site.append(f"{r['slug']}:{v.get('video_id')}")
                if v.get("video_id") and f'data-yt="{v["video_id"]}"' in raw:
                    bad_site.append(f"{r['slug']}:{v.get('video_id')} embedded")
    check(not bad_site and "video-linkonly" in raw, f"site-only videos render as link-only with their label (bad={bad_site})")
    rank = {"structure visible": 0, "reef effect visible": 1, "site context only": 2}
    hero_bad = []
    for r in reefs:
        h = r.get("hero_image") or {}
        if h.get("override") is not None or r["slug"] in (json.loads((BUILD / "data" / "page_overrides.json").read_text(encoding="utf-8")).get("heroes") or {}):
            continue          # hero chosen by Lior (data/page_overrides.json, 2026-10-24): not ranked
        ims = [im for im in r.get("images", []) if im.get("hotlink_ok") is True]
        best = min([rank.get(str(im.get("shows")).lower(), 3) for im in ims] or [9])
        got = next((rank.get(str(im.get("shows")).lower(), 3) for im in ims if im.get("url") == h.get("url")), 9 if ims else best)
        if got != best:
            hero_bad.append(f"{r['slug']} (hero tier {got}, best {best})")
    check(not hero_bad, f"hero image prefers structure visible > reef effect > site context (bad={hero_bad})")
    rej_img = []
    for slug in SLUGS:
        cp = BUILD.parent / "02_research" / "reefs" / f"{slug}.json"
        if cp.is_file():
            card = json.loads(cp.read_text(encoding="utf-8"))
            rej_img += [x["url"] for x in card.get("images_rejected") or [] if x.get("url")]
    leaked_img = [u for u in rej_img if u in raw_nd or u.split("?")[0] in raw_nd]
    check("images_rejected" not in p.data_json and not leaked_img,
          f"no images_rejected URL rendered anywhere, incl. the Scale tab ({len(rej_img)} checked; leaked={leaked_img})")

    hero_null = [r["slug"] for r in reefs if not r.get("hero_image")]
    check(not hero_null, f"every reef has a hero image (null={hero_null})")
    m = data["meta"]
    out.append(f"INFO total documented cost ~US${m['usd_total_mid']:,.0f} (range {m['usd_total_low']:,.0f}-{m['usd_total_high']:,.0f}) of {m['n_with_cost']} with cost data")
    ext = sorted(set(re.findall(r"(?:src|href)=\"(https?://[^\"]+)\"", raw)))
    out.append(f"INFO static external resources in HTML: {ext}")

    fails += check_models3d(raw, out, "--no-dom" not in sys.argv)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))
    print(f"\n{fails} failure(s); report: {REPORT}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

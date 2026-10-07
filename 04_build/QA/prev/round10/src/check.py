"""Static checks on the built page. Writes 04_build/QA/build_check.txt.

Run after build.py:  python "04_build/src/check.py"
Checks: HTML parses with balanced tags; inline JSON parses; all 13 slugs present;
every "assets/..." path referenced exists on disk; file < 3 MB; every [R#] token
in the data resolves to a reference of its own reef; no web image is copied locally;
every [R#] marker has a source pop-up target; no rejected video is rendered; Burkitts has 0 videos.
Scale tab (2026-09-25): 13 footprints present; every polygon closed and its shoelace area within 15 %
of area_m2; every R#/S# used in a footprint derivation has a pop-up target; provenance md copied
next to the page; the Scale view renders (headless DOM dump via qa_shots.dump_dom); media rules
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
    disc = sorted(p.parent.parent.name for p in (root / "07_scale" / "shapes").glob("*/3d/index.html") if (p.parent / "model.js").is_file())
    check(sorted(slugs) == disc, f"every discovered model has a section: disk {disc} vs page {sorted(slugs)}")
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
            "boscombe-surf-reef": ["^volume", "vertical datum", "emodnet"], "bunbury-airwave": ["state and verdict", "crest depth"]}
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
    unused = [f for f in on_disk if f not in asset_paths]
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
    leaked = [x for x in rejected if x in raw]
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
        if not f:
            continue
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
        if not f:
            continue
        refs = {x["id"]: x for x in r.get("references", [])}
        text = json.dumps(f.get("derivation"), ensure_ascii=False)
        for tok in sorted(set(re.findall(r"\b([RS]\d{1,3})\b", text))):
            n_ids += 1
            ref = refs.get(tok)
            if not ref or not (ref.get("citation") or "").strip():
                no_target_fp.append(f"{r['slug']}:{tok}")
    check(not no_target_fp, f"every one of {n_ids} R#/S# ids used in footprint derivations has a pop-up target (missing={no_target_fp})")
    docs_missing = [s for s, f in fps.items() if f and not (BUILD / (f.get("provenance_md") or "x")).is_file()]
    check(not docs_missing, f"provenance md for every footprint copied to docs/scale/ (missing={docs_missing})")
    check("function linkRefs" in raw and 'id="view-scale"' in raw and 'data-view="scale"' in raw,
          "Scale view code, view section and view toggle button are in the page")
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import qa_shots
        exe, sdom = qa_shots.dump_dom(HTML.as_uri() + "#view/scale")
        if not sdom:
            out.append("INFO no headless browser available: Scale view render check skipped")
        else:
            for k, v in qa_shots.scale_view_checks(sdom, len(reefs)).items():
                check(v, f"Scale view renders (headless DOM dump): {k}")
    except Exception as e:  # noqa: BLE001
        check(False, f"Scale view render check crashed: {e!r}")

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
    leaked_img = [u for u in rej_img if u in raw or u.split("?")[0] in raw]
    check("images_rejected" not in p.data_json and not leaked_img,
          f"no images_rejected URL rendered anywhere, incl. the Scale tab ({len(rej_img)} checked; leaked={leaked_img})")

    hero_null = [r["slug"] for r in reefs if not r.get("hero_image")]
    check(not hero_null, f"every reef has a hero image (null={hero_null})")
    no_map = [f"{r['slug']} ({r['map_note']})" for r in reefs if not r.get("map_ok")]
    out.append(f"INFO not plotted on map: {no_map}")
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

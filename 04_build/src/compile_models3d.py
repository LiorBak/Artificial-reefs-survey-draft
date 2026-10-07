"""Compile the data of the "3D models" tab:  04_build/data/models3d.json  (+ copies viewers, vendors images).

Run standalone:   python src/compile_models3d.py        (build.py also calls main() before inlining)

What it does (all READ-ONLY on 07_scale/shapes/*/3d and 03_images/reefs; only 04_build is written):
  1. DISCOVER models: every 07_scale/shapes/<slug>/3d with index.html + model.js  (reefs with 3d/FEASIBILITY.md but no model
     -> "not modelled" card; reefs with neither -> "not yet modelled" line).
  2. VIEWERS: copy index.html, model.js, docs.js, annotated/ (downscaled) to 04_build/3d/<slug>/ and rewrite the viewer so it needs
     no CDN and works from file:// (the import map is replaced by the vendored classic bundle 04_build/3d/vendor/three.bundle.js).
  3. PICTURES: select registry rows (03_images/reefs/<slug>/images.json) used for the model, write <=1600 px web copies + 400 px
     thumbnails to 04_build/assets/images/<slug>/ (never inline image bytes), group them by role.
  4. DOCS: render METHODS_3D.md / SOURCES_3D.md / REQUESTS_FOR_LIOR.md (and FEASIBILITY.md) to HTML (python `markdown`).
  5. TABLES: key numbers (data/models3d_curated.json), caveats (data/models3d_caveats.json, auto-extracted fallback), merged
     references (METHODS_3D "References" sections + the bathymetry reports), project-wide methods (data/models3d_text/methods.md).
  6. VERIFY: every curated 'ev' snippet / quote must occur in the model's documents (reported in meta.verify).
Reusable helpers for the later full build: prepare_image(), render_md(), parse_model_js(), norm().
"""
from __future__ import annotations

import hashlib
import html as htmlmod
import json
import re
import shutil
import sys
import time
from pathlib import Path

SRC = Path(__file__).resolve().parent
BUILD = SRC.parent
ROOT = BUILD.parent
SHAPES = ROOT / "07_scale" / "shapes"
REGS = ROOT / "03_images" / "reefs"
BATHY = ROOT / "07_scale" / "bathymetry"
DATA = BUILD / "data"
OUT_JSON = DATA / "models3d.json"
VIEW_DIR = BUILD / "3d"
VENDOR = VIEW_DIR / "vendor"
IMG_DIR = BUILD / "assets" / "images"
MANIFEST = DATA / "images_manifest.json"
THREE_VERSION = "0.170.0"

# bathymetry reports: which reefs each one concerns (its references are attached to those reefs when they are shown)
REPORTS = [
    {"id": "emodnet", "path": BATHY / "emodnet" / "REPORT.md", "slugs": ["boscombe-surf-reef", "borth-coastal-defence-reef"],
     "label": "EMODnet bathymetry report (07_scale/bathymetry/emodnet/REPORT.md)"},
    {"id": "gold_coast", "path": BATHY / "gold_coast" / "REPORT.md", "slugs": ["palm-beach-gold-coast", "narrowneck-gold-coast"],
     "label": "Gold Coast depth-evidence report (07_scale/bathymetry/gold_coast/REPORT.md)"},
]

GROUPS = [
    ("plan", "Plan shape", "Images read to fix the outline and its scale."),
    ("crest", "Crest & height", "Images read for crest level, reef height and side slopes."),
    ("seabed", "Seabed & depth", "Images read for the seabed around and under the reef."),
    ("tides", "Tides & datum", "Images read for tide levels and datum offsets."),
    ("validation", "Validation & cross-checks", "Images used to check the model (camera matches, independent values)."),
    ("flagged", "Flagged, not yet checked", "Registry flag for_3d_check.pending = true: could confirm or contradict a model value; not yet compared."),
    ("linked", "Other pictures named in the model sources", "Registered pictures that the model's SOURCES_3D.md / provenance points at."),
]
ROLE_TO_GROUP = {"plan_trace": "plan", "scale": "plan", "3d_crest": "crest", "3d_height_slopes": "crest", "3d_seabed": "seabed",
                 "3d_tides": "tides", "cross_check": "validation", "camera_match": "validation"}
ROLE_LABEL = {"plan_trace": "plan trace", "scale": "scale", "3d_crest": "crest", "3d_height_slopes": "height / slopes", "3d_seabed": "seabed",
              "3d_tides": "tides", "cross_check": "cross-check", "camera_match": "camera match", "context": "context", "not_used": "not used"}

WARN: list[str] = []


def warn(msg: str) -> None:
    WARN.append(msg)
    print("NOTE:", msg)


# ----------------------------------------------------------------------------------------------- text helpers
def norm(s: str) -> str:
    """Normalise for verbatim-snippet matching: lower case, plain quotes/dashes, no markdown emphasis, collapsed spaces."""
    s = str(s).lower()
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), (" ", " ")):
        s = s.replace(a, b)
    s = s.replace("*", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


TOKEN = re.compile(r"\{\{(=?)\s*([^{}|]+?)\s*(?:\|\s*([A-Za-z0-9]+))?\s*\}\}")


def _mpath(m: dict, path: str):
    """'a/b/c' into model.js; list items are picked by index or by their "id"; keys may contain dots ('-3.6')."""
    cur = m
    for part in path.split("/"):
        if isinstance(cur, dict):
            cur = cur[part]
        elif isinstance(cur, list):
            cur = cur[int(part)] if re.fullmatch(r"-?\d+", part) else next(x for x in cur if isinstance(x, dict) and x.get("id") == part)
        else:
            raise KeyError(path)
    return cur


def _tfmt(v, f: str | None) -> str:
    if not isinstance(v, (int, float)) or isinstance(v, bool):
        return str(v)
    if not f:
        return f"{v:g}"
    kind, nd = f[0], int(f[1:] or 0)
    return {"n": f"{v:,.{nd}f}", "s": f"{v:+,.{nd}f}", "d": f"{v:.{nd}f}"}.get(kind, f"{v:g}")


def fill_tokens(obj, m: dict, where: str, problems: list):
    """Replace {{path|fmt}} and {{= expression|fmt}} (expression may call P('path')) in every string of a curated entry by values read from
    model.js, so that the curated text follows the model when its numbers change (Mount Maunganui bed level, round 11). Formats: n0 n1 n2 (thousands
    separator), s0 s1 (signed), d1 d2 (plain). A token that cannot be resolved is recorded in `problems` (-> build VERIFY FAIL) and left as 'n/a'."""
    if isinstance(obj, str):
        def one(mo):
            try:
                if mo.group(1):
                    val = eval(mo.group(2), {"__builtins__": {}}, {"P": lambda q: _mpath(m, q), "abs": abs, "round": round, "min": min, "max": max})  # noqa: S307 (own data)
                else:
                    val = _mpath(m, mo.group(2).strip())
                return _tfmt(val, mo.group(3))
            except Exception as e:  # noqa: BLE001
                problems.append(f"{where} | token {mo.group(0)} -> {type(e).__name__}: {e}")
                return "n/a"
        return TOKEN.sub(one, obj)
    if isinstance(obj, list):
        return [fill_tokens(x, m, where, problems) for x in obj]
    if isinstance(obj, dict):
        return {k: fill_tokens(x, m, where, problems) for k, x in obj.items()}
    return obj


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def parse_model_js(path: Path) -> dict | None:
    t = read(path)
    i = t.find("{", t.find("REEF_MODEL"))
    if i < 0:
        return None
    try:
        obj, _ = json.JSONDecoder().raw_decode(t[i:])
        return obj
    except ValueError as e:
        warn(f"{path}: cannot parse model.js ({e})")
        return None


def _clean_html(h: str) -> str:
    h = re.sub(r"<(script|style|iframe|object|embed)\b.*?</\1>", "", h, flags=re.S | re.I)
    h = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", h, flags=re.I)

    def fix_a(m):
        attrs, body = m.group(1), m.group(2)
        href = re.search(r'href\s*=\s*"([^"]*)"', attrs)
        u = href.group(1) if href else ""
        if re.match(r"https?://", u):
            return f'<a href="{u}" target="_blank" rel="noopener noreferrer">{body}</a>'
        if u.startswith("#"):
            return f'<a href="{u}">{body}</a>'
        return f"<span class=\"m3d-nolink\">{body}</span>"
    return re.sub(r"<a\b([^>]*)>(.*?)</a>", fix_a, h, flags=re.S)


def render_md(text: str, id_prefix: str | None = None) -> str:
    """Markdown -> HTML (tables, fenced code). With id_prefix, numbered headings ('3.5 ...') get id=<prefix><3-5>."""
    import markdown  # noqa: PLC0415  (pip install markdown)
    h = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"], output_format="html")
    if id_prefix:
        def hid(m):
            lvl, inner = m.group(1), m.group(2)
            plain = re.sub(r"<[^>]+>", "", inner).strip()
            n = re.match(r"^(\d+(?:\.\d+)*)\.?\s", plain)
            if not n:
                return m.group(0)
            return f'<h{lvl} id="{id_prefix}{n.group(1).replace(".", "-")}">{inner}</h{lvl}>'
        h = re.sub(r"<h([1-6])>(.*?)</h\1>", hid, h, flags=re.S)
    h = _clean_html(h)
    # wide tables scroll inside their own box
    return re.sub(r"<table>", '<div class="m3d-tablewrap"><table>', h).replace("</table>", "</table></div>")


def md_sections(text: str) -> dict[str, str]:
    """Split markdown at '## ' headings -> {heading text: body}."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = line[3:].strip(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def md_table_rows(body: str) -> list[dict]:
    """First markdown table in `body` -> list of {header: cell}."""
    lines = [l for l in body.splitlines() if l.strip().startswith("|")]
    if len(lines) < 3:
        return []
    split = lambda l: [c.strip() for c in l.strip().strip("|").split("|")]  # noqa: E731
    head = split(lines[0])
    rows = []
    for l in lines[2:]:
        cells = split(l)
        if len(cells) >= len(head):
            rows.append(dict(zip(head, cells)))
    return rows


# ----------------------------------------------------------------------------------------------- images
Image = None


def _pil():
    global Image
    if Image is None:
        from PIL import Image as _I  # noqa: PLC0415
        _I.MAX_IMAGE_PIXELS = 400_000_000
        Image = _I
    return Image


def _load_manifest() -> dict:
    try:
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    except Exception:
        return {}


_MAN = _load_manifest()


def _save_manifest() -> None:
    for k in [k for k, v in _MAN.items() if not (BUILD / v["res"]["web"]).exists()]:
        del _MAN[k]                                  # prune cache entries whose output was deleted
    MANIFEST.write_text(json.dumps(_MAN, indent=0, sort_keys=True), encoding="utf-8")


def prepare_image(src: Path, out_dir: Path, base: str, max_px: int = 1600, thumb_px: int = 400, want_thumb: bool = True,
                  jpg_over: int | None = 400_000, quantize: bool = False, force_jpg: bool = False) -> dict | None:
    """Write a <=max_px web copy `<base>.<png|jpg>` (+ `<base>_400.jpg` thumbnail) into out_dir. Cached by (src size, mtime).
    Returns {web, thumb, w, h, tw, th, bytes} with paths relative to 04_build (forward slashes), or None if unreadable."""
    I = _pil()
    st = src.stat()
    key = f"{out_dir.relative_to(BUILD).as_posix()}/{base}"
    sig = [str(src), st.st_size, int(st.st_mtime), max_px, thumb_px, want_thumb, jpg_over, quantize, force_jpg]
    ent = _MAN.get(key)
    if ent and ent.get("sig") == sig and (BUILD / ent["res"]["web"]).exists() and (not want_thumb or (BUILD / ent["res"]["thumb"]).exists()):
        return ent["res"]
    try:
        im = I.open(src)
        im.load()
    except Exception as e:  # noqa: BLE001
        warn(f"cannot open image {src}: {e}")
        return None
    out_dir.mkdir(parents=True, exist_ok=True)
    w0, h0 = im.size
    scale = min(1.0, max_px / max(w0, h0))
    web = im if scale == 1.0 else im.resize((max(1, round(w0 * scale)), max(1, round(h0 * scale))), I.LANCZOS)
    has_alpha = web.mode in ("RGBA", "LA") or (web.mode == "P" and "transparency" in web.info)
    ext = src.suffix.lower()
    for old in out_dir.glob(base + ".*"):
        old.unlink()
    def as_jpg(path: Path) -> None:
        bg = I.new("RGB", web.size, "white")
        rgba = web.convert("RGBA")
        bg.paste(rgba, mask=rgba.split()[3])
        bg.save(path, "JPEG", quality=82, optimize=True)

    if ext in (".jpg", ".jpeg") or force_jpg:
        p = out_dir / f"{base}.jpg"
        as_jpg(p)
    else:
        p = out_dir / f"{base}.png"
        (web if has_alpha else web.convert("RGB")).save(p, "PNG", optimize=True)
        if quantize and p.stat().st_size > 300_000:   # palette PNG: diagrams / screenshots shrink a lot, name stays .png
            q = web.convert("RGB").quantize(colors=256, method=I.Quantize.MEDIANCUT, dither=I.Dither.NONE)
            q.save(p, "PNG", optimize=True)
        elif jpg_over is not None and p.stat().st_size > jpg_over:
            p.unlink()
            p = out_dir / f"{base}.jpg"
            as_jpg(p)
    res = {"web": p.relative_to(BUILD).as_posix(), "w": web.size[0], "h": web.size[1], "bytes": p.stat().st_size,
           "src_w": w0, "src_h": h0, "scale": round(scale, 5)}
    if want_thumb:
        ts = min(1.0, thumb_px / max(w0, h0))
        th = im.resize((max(1, round(w0 * ts)), max(1, round(h0 * ts))), I.LANCZOS) if ts < 1 else im
        tp = out_dir / f"{base}_400.jpg"
        bg = I.new("RGB", th.size, "white")
        rgba = th.convert("RGBA")
        bg.paste(rgba, mask=rgba.split()[3])
        bg.save(tp, "JPEG", quality=80, optimize=True)
        res.update({"thumb": tp.relative_to(BUILD).as_posix(), "tw": th.size[0], "th": th.size[1]})
    _MAN[key] = {"sig": sig, "res": res}
    return res


# ----------------------------------------------------------------------------------------------- viewers
IMPORT_STAR = re.compile(r"^import\s+\*\s+as\s+(\w+)\s+from\s+['\"]three['\"]\s*;?\s*$", re.M)
IMPORT_NAMED = re.compile(r"^import\s*\{([^}]*)\}\s*from\s*['\"]three/addons/[^'\"]+['\"]\s*;?\s*$", re.M)
BUNDLE_NAMES = {"THREE", "OrbitControls", "CSS2DRenderer", "CSS2DObject"}


# --- round 10: chrome injected into the COPY of every viewer (never into 07_scale) -----------------------------------------
BAR_TABS = [("Gallery", ""), ("Table", "#view/table"), ("3D models", "#view/models3d/{slug}")]
BAR_CSS = """<style id="m3d-bar-css">
/* injected by 04_build/src/compile_models3d.py (round 10); the original viewer is in 07_scale and is untouched */
html:not(.m3d-embedded) { position: relative; top: 34px; height: calc(100% - 34px); }
html:not(.m3d-embedded) #app { height: 100% !important; }
.m3d-topbar { position: fixed; top: 0; left: 0; right: 0; height: 34px; z-index: 2147483000; display: flex; align-items: center; gap: 6px; padding: 0 10px; background: #0b1117; border-bottom: 1px solid #2b3a46; font: 600 13px/1 system-ui, "Segoe UI", Roboto, sans-serif; white-space: nowrap; overflow-x: auto; }
.m3d-topbar a { color: #cfe6f5; text-decoration: none; padding: 6px 11px; border-radius: 6px; border: 1px solid #2b3a46; background: #16222b; }
.m3d-topbar a.back { background: #0b6b9e; border-color: #0b6b9e; color: #fff; }
.m3d-topbar a:hover { border-color: #7cc4ff; }
.m3d-topbar a:focus-visible { outline: 2px solid #ffd479; outline-offset: 1px; }
.m3d-topbar .sp { flex: 1 1 8px; }
.m3d-topbar .tt { color: #8fa3b1; font-weight: 400; }
html.m3d-embedded .m3d-topbar { display: none; }
html.m3d-embedded:not(.m3d-sidectl) #side, html.m3d-embedded #right, html.m3d-embedded #wideBtn, html.m3d-embedded #reason { display: none !important; }
/* Borth: #side holds the controls (view, water level, toggles), so it stays when framed, narrower, and the header is compacted */
html.m3d-sidectl.m3d-embedded #app { grid-template-columns: minmax(0, 1fr) 280px; }
html.m3d-sidectl.m3d-embedded #conf, html.m3d-sidectl.m3d-embedded #state, html.m3d-sidectl.m3d-embedded #top h1 { display: none; }
html.m3d-sidectl.m3d-embedded #top { padding: 3px 8px; grid-template-columns: minmax(0, 1fr); grid-template-areas: 'v'; }
html.m3d-sidectl.m3d-embedded #cap { display: none; }
html.m3d-sidectl.m3d-hide-right #app { grid-template-columns: minmax(0, 1fr) !important; grid-template-rows: minmax(0, 1fr) !important; }   /* stacked (narrow) layout: no empty row where the hidden panel was */
html.m3d-sidectl #m3d-show-right { top: auto !important; bottom: 8px; }   /* framed: the page shows the same content next to / below the stage (round 11: at every width) */
html.m3d-grid3.m3d-embedded #app { grid-template-columns: 220px minmax(0, 1fr) !important; }
html.m3d-grid3.m3d-embedded #top { grid-column: 1 / 3; }
html.m3d-embedded #caption { right: 10px !important; }
@media (max-width: 1099px) {   /* framed next to the photo panel: side panels would squeeze the 3D canvas */
  html.m3d-embedded #hud { right: 10px !important; }
}
@media (max-width: 599px) {    /* phones: the canvas first; the control column stays on the viewer's own page */
  html.m3d-grid3.m3d-embedded #app { grid-template-columns: minmax(0, 1fr) !important; }
  html.m3d-grid3.m3d-embedded #top { grid-column: 1 / 2; }
  html.m3d-embedded #app > #left { display: none; }
  html.m3d-sidectl.m3d-embedded #app { grid-template-columns: minmax(0, 1fr) !important; grid-template-rows: 58% 42%; }
  html.m3d-embedded #ctrl { width: 190px; font-size: 11px; }
}
</style>
<style id="m3d-panel-css">
/* round 11: collapsible side panels (open by default; state kept in sessionStorage and while the viewer lives, so it survives full screen) */
.m3d-pbtn { position: fixed; z-index: 2147482500; font: 600 12px/1 system-ui, "Segoe UI", Roboto, sans-serif; color: #e8eef2; background: #1d2b36; border: 1px solid #38505f; border-radius: 6px; padding: 7px 11px; cursor: pointer; box-shadow: 0 1px 6px rgba(0,0,0,.5); }
.m3d-pbtn:hover { background: #27404f; border-color: #ffb347; }
.m3d-pbtn:focus-visible, .m3d-phide:focus-visible { outline: 2px solid #ffd479; outline-offset: 1px; }
.m3d-pbtn[hidden] { display: none !important; }
#m3d-show-left { left: 8px; bottom: 8px; }
#m3d-show-right { right: 8px; top: 8px; }
html:not(.m3d-embedded) #m3d-show-right { top: 44px; }
.m3d-phide { display: block; margin: 0 0 6px auto; font: 600 11px/1 system-ui, "Segoe UI", Roboto, sans-serif; color: #cfe6f5; background: #16222b; border: 1px solid #38505f; border-radius: 5px; padding: 4px 9px; cursor: pointer; }
.m3d-phide:hover { border-color: #ffb347; }
html.m3d-hide-left #left, html.m3d-hide-left #ctrl { display: none !important; }
html.m3d-hide-right #right, html.m3d-hide-right #side { display: none !important; }
html.m3d-hide-left #view { left: 0 !important; }
html.m3d-hide-left #hud { left: 112px !important; }
html.m3d-hide-left #caption { left: 8px !important; }
html.m3d-grid3.m3d-hide-left #app > #stage { grid-column: 2; grid-row: 2; }   /* grid viewers place #stage / #right automatically: keep them in their own tracks when #left is gone */
html.m3d-grid3.m3d-hide-left #app > #right { grid-column: 3; grid-row: 2; }
html.m3d-grid3.m3d-hide-left.m3d-embedded #app { grid-template-columns: 0px minmax(0, 1fr) !important; }
html.m3d-grid3.m3d-hide-left:not(.m3d-embedded) #app { grid-template-columns: 0px minmax(0, 1fr) 420px !important; }
html.m3d-grid3.m3d-hide-right:not(.m3d-embedded) #app { grid-template-columns: 290px minmax(0, 1fr) 0px !important; }
html.m3d-grid3.m3d-hide-left.m3d-hide-right:not(.m3d-embedded) #app { grid-template-columns: 0px minmax(0, 1fr) 0px !important; }
@media (max-width: 1100px) {
  html.m3d-grid3.m3d-hide-left:not(.m3d-embedded) #app { grid-template-columns: 0px minmax(0, 1fr) 320px !important; }
  html.m3d-grid3.m3d-hide-right:not(.m3d-embedded) #app { grid-template-columns: 250px minmax(0, 1fr) 0px !important; }
  html.m3d-grid3.m3d-hide-left.m3d-hide-right:not(.m3d-embedded) #app { grid-template-columns: 0px minmax(0, 1fr) 0px !important; }
}
</style>
<script>(function () {
  var root = document.documentElement, KEY = 'm3d-panels', st = { left: true, right: true };
  try { var o = JSON.parse(sessionStorage.getItem(KEY) || 'null'); if (o) { st.left = o.left !== false; st.right = o.right !== false; } } catch (e) { /* no storage: stay open */ }
  function save() { try { sessionStorage.setItem(KEY, JSON.stringify(st)); } catch (e) { /* ignore */ } }
  function ready(f) { if (document.readyState !== 'loading') f(); else document.addEventListener('DOMContentLoaded', f); }
  ready(function () {
    if (document.getElementById('ctrlOpen')) return;   /* the combined viewer has its own native panel buttons */
    var emb = root.classList.contains('m3d-embedded'), q = function (sels) { for (var i = 0; i < sels.length; i++) { var e = document.querySelector(sels[i]); if (e) return e; } return null; };
    var side = { left: { el: q(['#left', '#ctrl']), label: 'Layout', hide: 'Hide \u25C2', what: 'layout and controls panel' }, right: (emb && !root.classList.contains('m3d-sidectl')) ? { el: null } : (root.classList.contains('m3d-sidectl') ? { el: q(['#side']), label: 'Controls', hide: 'Hide \u25B8', what: 'controls panel' } : { el: q(['#side', '#right']), label: 'Info', hide: 'Hide \u25B8', what: 'information panel' }) };
    window.__m3dPanels = { state: st, set: set };
    ['left', 'right'].forEach(function (k) {
      var d = side[k]; if (!d.el) return;
      var hb = document.createElement('button'); hb.type = 'button'; hb.className = 'm3d-phide'; hb.id = 'm3d-hide-' + k; hb.textContent = d.hide; hb.title = 'Hide the ' + d.what + ' (a "' + d.label + '" button stays at the edge)';
      hb.setAttribute('aria-controls', d.el.id); hb.setAttribute('aria-expanded', 'true'); d.el.insertBefore(hb, d.el.firstChild);
      var sb = document.createElement('button'); sb.type = 'button'; sb.className = 'm3d-pbtn'; sb.id = 'm3d-show-' + k; sb.hidden = true; sb.innerHTML = d.label + ' &#9656;'; sb.title = 'Show the ' + d.what;
      sb.setAttribute('aria-controls', d.el.id); sb.setAttribute('aria-expanded', 'false'); document.body.appendChild(sb);
      hb.addEventListener('click', function () { set(k, false); sb.focus(); });
      sb.addEventListener('click', function () { set(k, true); hb.focus(); });
    });
    function set(k, open) {
      if (!side[k] || !side[k].el) return;
      st[k] = open; save(); root.classList.toggle('m3d-hide-' + k, !open);
      var sb = document.getElementById('m3d-show-' + k), hb = document.getElementById('m3d-hide-' + k);
      if (sb) { sb.hidden = open; sb.setAttribute('aria-expanded', String(open)); } if (hb) hb.setAttribute('aria-expanded', String(open));
      try { window.dispatchEvent(new Event('resize')); setTimeout(function () { window.dispatchEvent(new Event('resize')); }, 120); } catch (e) { /* ignore */ }
    }
    ['left', 'right'].forEach(function (k) { if (side[k] && side[k].el && st[k] === false) set(k, false); });
  });
})();</script>
<script>try { var _c = '/*M3D_CLASSES*/'; if (_c) _c.split(' ').forEach(function (x) { document.documentElement.classList.add(x); }); } catch (e) { /* ignore */ }</script>
<script>try { if (window.self !== window.top) document.documentElement.classList.add('m3d-embedded'); } catch (e) { document.documentElement.classList.add('m3d-embedded'); }</script>
"""


def bar_html(slug: str, title: str) -> str:
    links = "".join(f'<a href="../../artificial_reefs.html{h.format(slug=slug)}">{n}</a>' for n, h in BAR_TABS)
    return (f'<nav class="m3d-topbar" aria-label="Back to the survey page"><a class="back" href="../../artificial_reefs.html#view/models3d/{slug}">&larr; Back to the page</a>'
            f'<span class="sp"></span><span class="tt">{title}</span>{links}</nav>\n')


def layout_classes(html: str) -> str:
    """Round 11: classes on <html> that tell the injected CSS which layout family a viewer belongs to.
    m3d-grid3 = #app is a grid of #left | #stage | #right (Boscombe); m3d-sidectl = the only side panel (#side) holds the CONTROLS (Borth: no #ctrl / #left)."""
    cls = []
    if 'id="left"' in html and 'id="right"' in html:
        cls.append("m3d-grid3")
    if 'id="side"' in html and 'id="ctrl"' not in html and 'id="left"' not in html:
        cls.append("m3d-sidectl")
    return " ".join(cls)


PM_VIEWERS: dict = {}      # data/photo_match.json "viewers" (slug -> scene map); set in main()
PM_PICS: dict = {}         # data/photo_match.json "pictures" (registry id -> transform)


def inject_receiver(html: str, slug: str) -> str:
    """Round 11: the 'Match this photo' receiver goes to the END of the viewer's last module script (it needs the viewer's own camera / controls)."""
    cfg = PM_VIEWERS.get(slug)
    if not cfg:
        return html
    js = (SRC / "pm_receiver.js").read_text(encoding="utf-8").replace("/*PM_CFG*/null", json.dumps({"A": cfg["scene_map"], "shift": cfg.get("canon_to_model_shift_m", [0, 0])}))
    mods = list(re.finditer(r'<script type="module">(.*?)</script>', html, re.S))
    if not mods:
        warn(f"{slug}: no module script to carry the photo-match receiver")
        return html
    end = mods[-1].end() - len("</script>")
    return html[:end] + "\n" + js + "\n" + html[end:]


def inject_chrome(html: str, slug: str, title: str) -> str:
    html = inject_receiver(html, slug)
    i = html.find("<script")
    css = BAR_CSS.replace("/*M3D_CLASSES*/", layout_classes(html))
    html = html[:i] + css + html[i:] if i >= 0 else html + css
    m = re.search(r"<body[^>]*>", html)
    if m:
        html = html[:m.end()] + "\n" + bar_html(slug, title) + html[m.end():]
    return html


def rewrite_viewer(html: str, slug: str, title: str = "") -> str:
    """Replace the CDN import map + ES-module imports by the vendored classic bundle (works from file:// and http)."""
    html = re.sub(r'<script type="importmap">.*?</script>\s*', "", html, flags=re.S)
    problems = []

    def star(m):
        return f"const {m.group(1)} = window.__THREE_BUNDLE.THREE;"

    def named(m):
        names = [n.strip() for n in m.group(1).split(",") if n.strip()]
        bad = [n for n in names if n.split(" as ")[0].strip() not in BUNDLE_NAMES]
        if bad:
            problems.append(bad)
        return "const { " + ", ".join(n.replace(" as ", ": ") for n in names) + " } = window.__THREE_BUNDLE;"
    html = IMPORT_STAR.sub(star, html)
    html = IMPORT_NAMED.sub(named, html)
    if re.search(r"^import\s", html, re.M):
        problems.append(["unhandled import line"])
    if problems:
        warn(f"{slug}: viewer imports something that is not in the vendored bundle: {problems} (add it to 04_build/3d/vendor/README.txt recipe)")
    # classic bundle before the first script of the page
    tag = '<script src="../vendor/three.bundle.js"></script>\n'
    i = html.find("<script")
    html = html[:i] + tag + html[i:] if i >= 0 else html + tag
    if not title:
        mt = re.search(r"<title>(.*?)</title>", html, re.S)
        title = htmlmod.escape(re.sub(r"\s+", " ", mt.group(1)).strip()) if mt else ""
    return inject_chrome(html, slug, title)


def copy_viewer(slug: str, d3: Path) -> dict:
    dest = VIEW_DIR / slug
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "index.html").write_text(rewrite_viewer(read(d3 / "index.html"), slug), encoding="utf-8", newline="\n")
    for f in ("model.js", "docs.js"):
        if (d3 / f).exists():
            shutil.copyfile(d3 / f, dest / f)
    n_ann = 0
    ann = d3 / "annotated"
    if ann.is_dir():
        (dest / "annotated").mkdir(exist_ok=True)
        keep = set()
        for f in sorted(ann.iterdir()):
            if f.suffix.lower() not in (".png", ".jpg", ".jpeg"):
                continue
            r = prepare_image(f, dest / "annotated", f.stem, max_px=1200, want_thumb=False, jpg_over=None, quantize=True)
            if r:
                keep.add(Path(r["web"]).name)
                # keep the original file name (docs.js links to it): the web copy may have changed the extension
                want = f.name
                got = BUILD / r["web"]
                if got.name != want:
                    shutil.copyfile(got, dest / "annotated" / want)
                    keep.add(want)
                n_ann += 1
        for f in (dest / "annotated").iterdir():
            if f.name not in keep:
                f.unlink()
    poster = None
    for cand in ("preview_oblique.png", "preview_beach_eye.png", "preview_plan.png"):
        if (d3 / cand).exists():
            r = prepare_image(d3 / cand, dest, "poster", max_px=900, want_thumb=False, force_jpg=True)
            if r:
                poster = r["web"]
            break
    return {"viewer": f"3d/{slug}/index.html", "poster": poster, "annotated_copied": n_ann}


# ----------------------------------------------------------------------------------------------- registry pictures
def label_from_file(name: str) -> str:
    s = Path(name).stem
    s = re.sub(r"^[A-Za-z]\d+_", "", s)
    return s.replace("_", " ").replace("-", " ").strip()


def build_gallery(slug: str, files_3d_ann: set[str]) -> tuple[list, dict]:
    reg_path = REGS / slug / "images.json"
    try:
        rows = json.loads(reg_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        warn(f"{slug}: no readable registry ({e})")
        return [], {}
    items = []
    stats = {"rows": len(rows), "selected": 0, "missing_file": 0}
    for r in rows:
        if r.get("display") is False:
            continue
        used = r.get("used_for") or []
        lr = " ".join(r.get("linked_records") or []).replace("\\", "/")
        f = (r.get("file") or "").replace("\\", "/")
        anns = [a.replace("\\", "/") for a in (r.get("annotated_files") or [])]
        in_3d_ann = "3d/annotated/" in f or any("3d/annotated/" in a for a in anns)
        linked = ("3d/SOURCES_3D" in lr) or ("model.js" in lr) or ("3d/METHODS_3D" in lr)
        role_groups = [ROLE_TO_GROUP[u] for u in used if u in ROLE_TO_GROUP]
        pending = bool((r.get("for_3d_check") or {}).get("pending"))
        if not (role_groups or in_3d_ann or linked or pending):
            continue
        if not f or not (ROOT / f).is_file():
            stats["missing_file"] += 1
            warn(f"{slug}/{r.get('id')}: registry file missing on disk ({f})")
            continue
        base = r["id"]
        img = prepare_image(ROOT / f, IMG_DIR / slug, base)
        if not img:
            continue
        ann_out = []
        for k, a in enumerate(anns, 1):
            ap = ROOT / a
            if not ap.is_file() or ap.suffix.lower() not in (".png", ".jpg", ".jpeg"):
                continue
            ai = prepare_image(ap, IMG_DIR / slug, f"{base}_ann{k}", want_thumb=False)
            if ai:
                ann_out.append({"web": ai["web"], "w": ai["w"], "h": ai["h"], "label": label_from_file(ap.name), "file": a})
        if role_groups:
            group = role_groups[0]
        elif in_3d_ann:
            group = "seabed" if "nav" in f.lower() else "validation"
        elif pending:
            group = "flagged"
        else:
            group = "linked"
        chk = r.get("for_3d_check") or {}
        items.append({
            "id": r["id"], "group": group, "roles": [ROLE_LABEL.get(u, u) for u in used],
            "title": r.get("title") or r["id"], "kind": r.get("kind"), "date": r.get("image_date"), "state": r.get("state_shown"),
            "shows": r.get("shows"), "structure_visible": r.get("structure_visible"), "how_used": r.get("how_used") or "",
            "citation": r.get("citation") or "", "credit": r.get("credit"), "license": r.get("license"), "retrieved": r.get("retrieved"),
            "image_url": r.get("image_url"), "source_page": r.get("source_page"), "page_or_figure": r.get("page_or_figure"),
            "rights_note": r.get("rights_note"), "linked_records": r.get("linked_records") or [],
            "pending": pending, "check_what": chk.get("what_to_check") or "", "check_values": chk.get("model_values_affected") or [],
            "thumb": img.get("thumb"), "tw": img.get("tw"), "th": img.get("th"), "web": img["web"], "w": img["w"], "h": img["h"],
            "annotated": ann_out, "added_by": r.get("added_by"),
        })
        stats["selected"] += 1
    order = {g[0]: i for i, g in enumerate(GROUPS)}
    items.sort(key=lambda x: (order[x["group"]], x["id"]))
    return items, stats


# ----------------------------------------------------------------------------------------------- model facts
def extract_tides(m: dict) -> dict:
    lv = None
    src_note = ""
    w = m.get("water")
    if isinstance(m.get("water_levels"), list):
        lv = m["water_levels"]
    elif isinstance(w, dict) and isinstance(w.get("levels"), list):
        lv = w["levels"]
        src_note = w.get("source") or ""
    out = []
    for l in lv or []:
        if not isinstance(l, dict) or l.get("z") is None:
            continue
        s = l.get("source") or l.get("source_id") or src_note
        out.append({"id": l.get("id") or l.get("key"), "label": l.get("label") or l.get("id") or l.get("key"), "z": l["z"],
                    "src": s, "note": l.get("note") or ""})
    out.sort(key=lambda x: -x["z"])
    note = ""
    for k in ("datum_note",):
        if isinstance(w, dict) and w.get(k):
            note = w[k]
    d = m.get("datum")
    if isinstance(d, dict):
        note = (note + " " if note else "") + f"Survey datum: {d.get('survey_datum', '')}; z_MSL = {d.get('z_msl_equals', '')}; survey zero in MSL {d.get('survey_zero_in_msl_m', '')} m."
    t = m.get("tides")
    if isinstance(t, dict) and t.get("note"):
        note += " " + t["note"]
    if isinstance(w, dict) and w.get("source") and not out:
        note += " " + w["source"]
    return {"levels": out, "note": note.strip()}


def first_str(m: dict, *paths) -> str:
    for p in paths:
        cur = m
        for k in p.split("."):
            cur = cur.get(k) if isinstance(cur, dict) else None
        if isinstance(cur, str) and cur.strip():
            return cur.strip()
    return ""


def auto_key_numbers(prov: list[dict]) -> list[dict]:
    pat = re.compile(r"crest|reef height|height|seabed|slope|volume|footprint|plan outline|toe|depth", re.I)
    rows = []
    for p in prov:
        if pat.search(str(p.get("parameter", ""))) and len(rows) < 12:
            rows.append({"q": p.get("parameter"), "model": f"{p.get('value')} {p.get('unit') or ''}".strip(), "stated": "", "diff": "",
                         "ids": p.get("source_id") or "", "note": (p.get("uncertainty") or ""), "ev": []})
    return rows


def _num(x):
    try:
        return float(x) if x is not None and x != "" and not isinstance(x, bool) else None
    except (TypeError, ValueError):
        return None


def norm_versions(m: dict, slug: str) -> dict | None:
    """Outline / model versions (build_3d_tab.md 2b): model.js "versions" [{id,name,date,source_ids,method,level,kind,area_m2,
    volume_m3,bbox_m,note,stated{area,volume}}] + "default_version" + "versions_info". Tolerant of alternative key spellings.
    Returns None when the model has no versions; otherwise {"list": [...], "default": id, "info": str}."""
    vs = m.get("versions")
    if not isinstance(vs, list) or not vs:
        return None
    srcs = {s.get("id"): s for s in (m.get("sources") or []) if isinstance(s, dict)}
    out, seen = [], set()
    for i, v in enumerate(vs):
        if not isinstance(v, dict):
            continue
        vid = re.sub(r"[^A-Za-z0-9_.-]", "_", str(v.get("id") or f"v{i + 1}"))
        if vid in seen:
            warn(f"{slug}: duplicate version id '{vid}' ignored")
            continue
        seen.add(vid)
        sid = v.get("source_ids") or v.get("source_id") or v.get("sources") or v.get("source") or []
        if isinstance(sid, str):
            sid = [x.strip() for x in re.split(r"[;,]", sid) if x.strip()]
        sid = [str(x) for x in sid if x]
        bbox = v.get("bbox_m") if isinstance(v.get("bbox_m"), list) else None
        st = v.get("stated") if isinstance(v.get("stated"), dict) else {}
        out.append({
            "id": vid, "name": str(v.get("name") or v.get("label") or vid), "date": str(v.get("date") or ""),
            "kind": str(v.get("kind") or ""), "method": str(v.get("method") or ""), "level": str(v.get("level") or ""),
            "note": str(v.get("note") or ""), "source_ids": sid,
            "source_text": [str((srcs.get(x) or {}).get("citation") or x) for x in sid],
            "area_m2": _num(v.get("area_m2") if v.get("area_m2") is not None else v.get("footprint_m2")),
            "volume_m3": _num(v.get("volume_m3") if v.get("volume_m3") is not None else (v.get("volume") if v.get("volume") is not None else v.get("volume_m3_default"))),
            "bbox_m": [_num(b) for b in bbox[:2]] if bbox and len(bbox) >= 2 else None,
            "stated": {"area": str(st.get("area") or ""), "volume": str(st.get("volume") or "")},
        })
    if not out:
        return None
    ids = [v["id"] for v in out]
    default = str(m.get("default_version") or "")
    if default not in ids:
        warn(f"{slug}: default_version '{default}' is not one of {ids}: using '{ids[0]}'")
        default = ids[0]
    return {"list": out, "default": default, "info": str(m.get("versions_info") or "")}


def version_caveats(slug: str, ver: dict) -> list[dict]:
    """Automatic caveat rows: how each non-default outline version differs from the default (footprint area, volume)."""
    rows = []
    vs = {v["id"]: v for v in ver["list"]}
    d = vs[ver["default"]]
    for o in ver["list"]:
        if o["id"] == d["id"]:
            continue
        for key, label, unit in (("area_m2", "Footprint area", "m²"), ("volume_m3", "Reef volume", "m³")):
            a, b = d.get(key), o.get(key)
            if a is None or b is None:
                continue
            pct = (a - b) / b * 100 if b else 0
            rows.append({
                "slug": slug, "q": f"{label} depends on the outline version",
                "model": f"{a:,.0f} {unit} - {d['name']} (default)", "stated": f"{b:,.0f} {unit} - {o['name']}",
                "diff": f"{a - b:+,.0f} {unit} ({pct:+.0f} % of the other version)",
                "reason": "Different edge definitions: " + (d["level"] or d["name"]) + " (default) versus " + (o["level"] or o["name"]) + ".",
                "status": "by-design",
                "resolve": "Not an error: the page shows the default version; switch versions in the model header. Which edge fits a given use is Lior's choice (see the (i) pop-up).",
                "section": "", "ids": "; ".join(dict.fromkeys(d["source_ids"] + o["source_ids"])), "ev": [], "auto": False, "origin": "versions"})
    return rows


def parse_refs(text: str) -> list[str]:
    secs = md_sections(text)
    body = next((b for h, b in secs.items() if re.search(r"references", h, re.I)), "")
    refs, cur = [], None
    for line in body.splitlines():
        m = re.match(r"^\s*[-*]\s+(.*\S)\s*$", line)
        if m:
            cur = [m.group(1)]
            refs.append(cur)
        elif cur is not None and line.strip() and not line.startswith("#") and not line.startswith("```"):
            cur.append(line.strip())
        elif not line.strip():
            cur = None
    return [" ".join(r) for r in refs]


STOP = {"the", "and", "for", "from", "with", "that", "this", "into", "their", "over", "using", "data", "accessed", "https", "http", "www", "pdf", "html"}


def ref_sig(t: str):
    t = re.sub(r"[*_`]", "", t)
    m = re.search(r"\(?((?:19|20)\d\d|n\.d\.)[a-z]?(?:/\d{4})?\)?", t)
    year = m.group(1) if m else ""
    head = t[:m.start()] if m else t[:30]
    toks = re.sub(r"[^a-z ]", " ", head.lower()).split()
    surname = toks[0] if toks else ""
    title = t[m.end():] if m else t
    words = {w for w in re.findall(r"[a-z0-9]+", title.lower()) if len(w) > 3 and w not in STOP}
    url = re.search(r"https?://[^\s)>\]]+", t)
    u = re.sub(r"^https?://(www\.)?", "", url.group(0)).rstrip("/.,;") if url else ""
    return surname, year, words, u


def merge_refs(entries: list[tuple[str, str]]) -> list[dict]:
    """entries: (text, cited_by). De-duplicate by author-year + title words / URL."""
    merged: list[dict] = []
    for text, cb in entries:
        s = ref_sig(text)
        hit = None
        for m in merged:
            ms = m["_sig"]
            same_au = s[0] == ms[0] and s[1] == ms[1] and s[0]
            if (same_au and len(s[2] & ms[2]) >= 2) or (s[3] and s[3] == ms[3]) or (same_au and s[0] in ("garmin",)):
                hit = m
                break
        if hit:
            if cb not in hit["cited_by"]:
                hit["cited_by"].append(cb)
            if len(text) > len(hit["text"]):
                hit["text"], hit["_sig"] = text, s
        else:
            merged.append({"text": text, "cited_by": [cb], "_sig": s})
    for m in merged:
        url = re.search(r"https?://[^\s)>\]]+", m["text"])
        m["url"] = url.group(0).rstrip(".,;") if url else ""
        del m["_sig"]
    merged.sort(key=lambda m: re.sub(r"[^a-z]", "", m["text"].lower())[:60])
    for i, m in enumerate(merged, 1):
        m["id"] = f"ref{i}"
    return merged


# ----------------------------------------------------------------------------------------------- main
def build_combined(models: list[dict]) -> dict | None:
    """Combined 'All (compare)' scene (round 10): export every model's meshes from its copied viewer (cached, src/export_combined.py),
    write 3d/combined/{manifest.js,index.html} and return the data block of models3d.json ("combined")."""
    if not models:
        return None
    sys.path.insert(0, str(SRC))
    import export_combined  # noqa: PLC0415
    res = export_combined.run([m["slug"] for m in models], log=lambda s: print(s))
    comb = VIEW_DIR / "combined"
    comb.mkdir(parents=True, exist_ok=True)
    meta, rows = [], []
    for m in models:
        r = res.get(m["slug"]) or {"status": "not", "reason": "not exported"}
        ok = r.get("status") == "ok"
        short = re.sub(r"\s*\(.*$", "", m["name"]).strip()
        lvl = m["confidence"]["level"]
        meta.append({"slug": m["slug"], "name": m["name"], "short": short, "level": lvl, "status": "ok" if ok else "not", "reason": r.get("reason", "")})
        row = {"slug": m["slug"], "name": short, "level": lvl, "status": "ok" if ok else "not", "reason": r.get("reason", "")}
        if ok:
            row.update({k: r[k] for k in ("area_m2", "area_ref_m2", "area_rel_err", "crest_z_m", "crest_ref_m", "crest_err_m", "ok", "checks", "bbox_m")})
            row["note"] = r.get("note", {})
        else:
            warn(f"combined view: {m['slug']} is not in the comparison: {row['reason']}")
        rows.append(row)
        if ok and not r.get("ok"):
            warn(f"combined view: {m['slug']} exported but a check against model.js failed: " + "; ".join(c["name"] for c in r["checks"] if not c["ok"]))
    (comb / "manifest.js").write_text("window.M3D_COMBINED_META = " + json.dumps(meta, ensure_ascii=False) + ";\n", encoding="utf-8", newline="\n")
    tpl = read(SRC / "combined_viewer.html")
    scripts = '<script src="manifest.js"></script>\n' + "".join(f'<script src="{x["slug"]}.js"></script>\n' for x in meta if x["status"] == "ok")
    if "<!--M3D_DATA_SCRIPTS-->" not in tpl:
        raise SystemExit("combined_viewer.html lost its <!--M3D_DATA_SCRIPTS--> marker")
    html = inject_chrome(tpl.replace("<!--M3D_DATA_SCRIPTS-->", scripts), "all", "All reefs compared")
    (comb / "index.html").write_text(html, encoding="utf-8", newline="\n")
    tol = export_combined.load_config()["tolerance"]
    tol_text = (f"Tolerances: footprint area within {tol['area_rel'] * 100:.0f} % of the model.js toe polygon (the exported mesh includes the side slopes beyond the toe line); "
                f"footprint centroid within {tol['centroid_m']:g} m of the polygon centroid; crest level within {tol['crest_m']:g} m; "
                f"seabed within {tol['shore_m']:g} m of 0 m MSL along the shoreline; seabed falls away offshore within {tol['offshore_deg']:g} degrees.")
    mtxt = read(DATA / "models3d_text" / "combined_method.md")
    return {"viewer": "3d/combined/index.html", "poster": "", "built": time.strftime("%Y-%m-%d"), "models": rows, "tolerance": tol,
            "tolerance_text": tol_text, "method_html": render_md(mtxt) if mtxt else ""}


def main() -> int:
    t0 = time.time()
    global PM_VIEWERS, PM_PICS
    try:                                                  # round 11: plan-view photo transforms (re-computed only when an input changed)
        sys.path.insert(0, str(SRC))
        import photo_match
        if photo_match.ensure():
            print("photo_match: recomputed")
        _pm = json.loads(read(DATA / "photo_match.json") or "{}")
        PM_VIEWERS, PM_PICS = _pm.get("viewers", {}), _pm.get("pictures", {})
    except Exception as e:  # noqa: BLE001
        warn(f"photo_match unavailable ({e}): no 'Match this photo' buttons")
        PM_VIEWERS, PM_PICS = {}, {}
    reefs = json.loads(read(DATA / "reefs.json") or "[]")
    names = {r["slug"]: r for r in reefs}
    all_slugs = [r["slug"] for r in reefs] or sorted(p.name for p in SHAPES.iterdir() if p.is_dir())
    if SHAPES.is_dir():     # models of slugs that are not in reefs.json (tests, future reefs): only if they carry a model or a feasibility note
        for p in sorted(SHAPES.iterdir()):
            if p.is_dir() and p.name not in all_slugs and (((p / "3d" / "index.html").is_file() and (p / "3d" / "model.js").is_file()) or (p / "3d" / "FEASIBILITY.md").is_file()):
                all_slugs.append(p.name)
    curated = json.loads(read(DATA / "models3d_curated.json") or '{"models": {}}')
    cav_all = json.loads(read(DATA / "models3d_caveats.json") or '{"rows": []}')["rows"]
    verify = {"checked": 0, "failed": []}

    def check_ev(slug: str, corpus: str, snippet: str, where: str) -> None:
        verify["checked"] += 1
        if norm(snippet) not in corpus:
            verify["failed"].append(f"{slug} | {where} | {snippet[:90]}")

    models, feas, notyet = [], [], []
    ref_entries: list[tuple[str, str]] = []
    VIEW_DIR.mkdir(exist_ok=True)
    if not (VENDOR / "three.bundle.js").is_file():
        warn("04_build/3d/vendor/three.bundle.js missing: viewers will not run (see 04_build/3d/vendor/README.txt)")

    hold = json.loads(read(DATA / "models3d_hold.json") or '{"hold": {}}').get("hold", {})   # round 11: models that are still being built by another agent
    for slug in all_slugs:
        d3 = SHAPES / slug / "3d"
        rname = names.get(slug, {}).get("name") or slug
        if slug in hold:
            warn(f"{slug}: HELD by data/models3d_hold.json ({hold[slug]})")
            notyet.append({"slug": slug, "name": rname, "note": hold[slug]})
            continue
        if (d3 / "index.html").is_file() and (d3 / "model.js").is_file():
            m = parse_model_js(d3 / "model.js")
            if m is not None and slug not in names:
                rname = m.get("name") or (m.get("meta") or {}).get("name") or slug
            if m is None:
                warn(f"{slug}: model.js unreadable (another agent may be writing it): model skipped this build")
                notyet.append({"slug": slug, "name": rname, "note": "model files present but model.js could not be read at build time"})
                continue
            methods_md, sources_md, req_md = read(d3 / "METHODS_3D.md"), read(d3 / "SOURCES_3D.md"), read(d3 / "REQUESTS_FOR_LIOR.md")
            report_txt = "".join(read(r["path"]) for r in REPORTS if slug in r["slugs"])
            corpus = norm("\n".join([methods_md, sources_md, req_md, read(d3 / "model.js"), report_txt]))
            cur = fill_tokens(curated.get("models", {}).get(slug) or {}, m, f"{slug} curated", verify["failed"])
            conf = m.get("confidence_3d") or {}
            reason = conf.get("reason") or ""
            reason_short = cur.get("confidence_short") or conf.get("reason_short") or (reason if len(reason) < 260 else reason[:257].rsplit(" ", 1)[0] + "...")
            prov = m.get("provenance") if isinstance(m.get("provenance"), list) else []
            srcs = m.get("sources") if isinstance(m.get("sources"), list) else []
            state_auto = first_str(m, "state_label", "meta.state_label", "meta.state_represented", "state_drawn")
            built = first_str(m, "generated", "built", "meta.built", "meta.generated")
            vinfo = copy_viewer(slug, d3)
            ann_names = set((d3 / "annotated").iterdir()) if (d3 / "annotated").is_dir() else set()
            gallery, gstats = build_gallery(slug, {a.name for a in ann_names})
            for g in gallery:                                   # round 11: pictures with a documented plan-view transform get a 'Match this photo' button
                pmv = PM_PICS.get(g["id"])
                if pmv and pmv.get("slug") == slug and slug in PM_VIEWERS:
                    g["match"] = {k: pmv.get(k) for k in ("kind", "method", "center_m", "up_m", "rotation_deg", "width_m", "height_m", "crop_frac", "m_per_px", "tolerance_m", "reference", "zoom", "source_id")}
                    g["match"]["rms_m"] = (pmv.get("residual") or {}).get("rms_m")
                    g["match"]["iou"] = (pmv.get("residual") or {}).get("iou")
                    g["match"]["note"] = pmv.get("note", "")
            # round 11: prune generated copies the registry no longer selects (a row corrected to 'context', a renamed file, ...)
            _keep = {Path(x).name for x in re.findall(r"assets/images/[^\"'\s]+", json.dumps(gallery))}
            for _f in (IMG_DIR / slug).glob("*") if (IMG_DIR / slug).is_dir() else []:
                if _f.is_file() and _f.name not in _keep:
                    _f.unlink()
                    warn(f"{slug}: pruned stale generated copy {_f.name}")
            # key numbers / caveats / quotes with verification
            kn = cur.get("key_numbers") or auto_key_numbers(prov)
            kn_curated = bool(cur.get("key_numbers"))
            for row in kn:
                for ev in row.get("ev", []):
                    check_ev(slug, corpus, ev, f"key number '{row.get('q')}'")
            relied = cur.get("relied") or []
            for q in relied:
                if len(q["quote"].split()) > 25:
                    verify["failed"].append(f"{slug} | quote longer than 25 words | {q['quote'][:60]}")
                check_ev(slug, corpus, q["quote"], "relied-on quote")
            if cur.get("ve_ev"):
                for ev in cur["ve_ev"]:
                    check_ev(slug, corpus, ev, "VE note")
            cav = [dict(fill_tokens(c, m, f"{slug} caveat '{c.get('q')}'", verify["failed"]), auto=False) for c in cav_all if c["slug"] == slug]
            for c in cav:
                for ev in c.get("ev", []):
                    check_ev(slug, corpus, ev, f"caveat '{c.get('q')}'")
            if not cav:   # auto fallback: the Limitations table of METHODS_3D.md
                secs = md_sections(methods_md)
                lim = next((b for h, b in secs.items() if re.search(r"limitations|unknowns", h, re.I)), "")
                for r in md_table_rows(lim):
                    vals = list(r.values())
                    keys = [k.lower() for k in r]
                    pick = lambda *ks: next((r[k0] for k0, kl in zip(r, keys) if any(x in kl for x in ks)), "")  # noqa: E731
                    cav.append({"slug": slug, "q": pick("unknown", "gap") or (vals[1] if len(vals) > 1 else vals[0]), "model": "see METHODS_3D.md",
                                "stated": "-", "diff": "", "reason": pick("bias"), "status": "open", "resolve": pick("resolve", "what would"),
                                "section": "7", "ids": "", "ev": [], "auto": True})
            ver = norm_versions(m, slug)
            if ver:
                cav += version_caveats(slug, ver)
            # references
            ref_n = 0
            for t in parse_refs(methods_md):
                ref_entries.append((t, slug))
                ref_n += 1
            for rep in REPORTS:
                if slug in rep["slugs"]:
                    for t in parse_refs(read(rep["path"])):
                        ref_entries.append((t, slug))
            models.append({
                "slug": slug, "name": rname, "place": names.get(slug, {}).get("place_short") or "",
                "flag": names.get(slug, {}).get("country_flag") or "", "verdict": names.get(slug, {}).get("verdict") or "",
                "verdict_label": names.get(slug, {}).get("verdict_label") or "",
                "model_name": m.get("name") or (m.get("meta") or {}).get("name") or "", "built": built,
                "state_short": cur.get("state_short") or (state_auto if len(state_auto) < 330 else state_auto[:327].rsplit(" ", 1)[0] + "..."),
                "state_full": state_auto, "caption": first_str(m, "caption"),
                "confidence": {"level": (conf.get("level") or "unknown").lower(), "reason": reason, "reason_short": reason_short},
                "ve_note": cur.get("ve_note") or "", "viewer": vinfo["viewer"], "poster": vinfo["poster"],
                "tides": extract_tides(m), "provenance": [{k: p.get(k) for k in ("parameter", "value", "unit", "source_id", "method", "uncertainty", "estimated")} for p in prov],
                "sources": [{"id": s.get("id"), "citation": s.get("citation"), "url": s.get("url")} for s in srcs],
                "key_numbers": kn, "key_numbers_curated": kn_curated, "relied": relied,
                "caveats": cav, "gallery": gallery, "gallery_stats": gstats,
                "methods_html": render_md(methods_md, f"m3d-{slug}-m-") if methods_md else "",
                "sources_html": render_md(sources_md) if sources_md else "",
                "requests_html": render_md(req_md) if req_md else "",
                "docs": {"methods": bool(methods_md), "sources": bool(sources_md), "requests": bool(req_md)},
                "lifecycle": m.get("lifecycle") or m.get("history") or [],
                "curated": bool(cur),
                "versions": ver["list"] if ver else [], "default_version": ver["default"] if ver else "",
                "versions_info": ver["info"] if ver else "",
            })
        elif (d3 / "FEASIBILITY.md").is_file():
            ft = read(d3 / "FEASIBILITY.md")
            plain = re.sub(r"[#*`|>-]", " ", ft)
            feas.append({"slug": slug, "name": rname, "summary": re.sub(r"\s+", " ", plain).strip()[:700], "html": render_md(ft)})
        else:
            notyet.append({"slug": slug, "name": rname})

    models.sort(key=lambda x: x["name"].lower())
    combined = build_combined(models)
    refs = merge_refs(ref_entries)
    # per-model reference ids
    for m in models:
        m["ref_ids"] = [r["id"] for r in refs if m["slug"] in r["cited_by"]]
    methods_txt = read(DATA / "models3d_text" / "methods.md")
    payload = {
        "meta": {"compiled": time.strftime("%Y-%m-%d"), "three": THREE_VERSION, "n_models": len(models),
                 "verify": verify, "warnings": WARN[:60]},
        "groups": [{"key": k, "label": l, "blurb": b} for k, l, b in GROUPS],
        "ve_generic": curated.get("ve_generic", ""),
        "models": models, "feasibility": feas, "not_yet": notyet,
        "caveats_note": "Rows marked 'auto' were extracted from the Limitations table of the model's METHODS_3D.md; they have not been curated into a model-vs-source comparison. Rows about outline versions are generated automatically from the versions in model.js (default version against each other version).",
        "references": refs,
        "combined": combined,
        "methods_html": render_md(methods_txt) if methods_txt else "",
        "docs_links": [{"slug": m["slug"], "files": [f"07_scale/shapes/{m['slug']}/3d/{n}" for n in ("METHODS_3D.md", "SOURCES_3D.md", "REQUESTS_FOR_LIOR.md")]} for m in models],
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    _save_manifest()
    n_pics = {m["slug"]: len(m["gallery"]) for m in models}
    print(f"models3d: {len(models)} models, {len(feas)} feasibility, {len(notyet)} not yet; pictures {n_pics}; "
          f"{len(refs)} references (from {len(ref_entries)}); caveat rows {sum(len(m['caveats']) for m in models)}; "
          f"verify {verify['checked']} checked, {len(verify['failed'])} failed; json {OUT_JSON.stat().st_size // 1024} KB; {time.time() - t0:.1f}s")
    for f in verify["failed"][:40]:
        print("VERIFY FAIL:", f)
    return 0


if __name__ == "__main__":
    sys.exit(main())

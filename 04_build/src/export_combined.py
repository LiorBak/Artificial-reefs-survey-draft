"""Export the reef + seabed meshes of every copied 3D viewer for the combined "All (compare)" scene.

    python src/export_combined.py [--force] [slug ...]       (compile_models3d.py calls run() at the end of every build)

METHOD (documented for Lior; see also README.md "3D models tab" and data/SCHEMA.md "models3d_combined.json")
  1. Each copied viewer 04_build/3d/<slug>/index.html is opened in OWN headless Chrome (src/qa_cdp.py: random free port, fresh profile).
     A script registered with Page.addScriptToEvaluateOnNewDocument wraps THREE.Scene / THREE.WebGLRenderer of the vendored bundle so that
     the viewer's scene graph can be read - no file of the viewer is changed and nothing is redrawn from model.js.
  2. All VISIBLE meshes with >= 100 vertices are read in WORLD coordinates. The one with the largest plan-view (x,z) bounding box is the
     seabed; meshes with a nearly identical bounding box are its skirt (ignored); the others lying inside it are the reef (merged).
     Whatever the viewer shows at load (its default state / outline version) is what is exported.
  3. Positions are rotated about the vertical axis (a pure rotation: nothing is mirrored or rescaled) so that "offshore" points to +z
     for every model, and heights stay as in the viewer (y = metres above the model's own MSL zero). The direction "offshore" comes from
     the model's frame note (data/models3d_combined.json) and is re-checked against the seabed slope (it must fall away offshore).
  4. CHECKS against model.js (tolerances in data/models3d_combined.json): footprint area of the exported reef (up-facing triangles,
     projected) vs the area of the model's own toe polygon; footprint centroid vs the polygon centroid (this also proves the rotation /
     handedness); crest level (max y of the exported reef) vs the model's crest value; the seabed is within shore_m of 0 along the shoreline.
     A model failing a check is still written but flagged ok = false; a model that cannot be exported is "not in comparison" with the reason.
  5. Output: 3d/combined/<slug>.js (window.M3D_COMBINED[slug] = {...}; quantised uint16 positions + uint16/32 indices as base64, so the
     combined viewer works from file:// without fetch), 3d/combined/export_cache.json (signature per slug: unchanged inputs skip Chrome).
Only 04_build is written; 07_scale and 03_images are never touched.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import sys
import time
from pathlib import Path

import numpy as np

SRC = Path(__file__).resolve().parent
BUILD = SRC.parent
VIEW_DIR = BUILD / "3d"
OUT_DIR = VIEW_DIR / "combined"
CONFIG = BUILD / "data" / "models3d_combined.json"
CACHE = OUT_DIR / "export_cache.json"
VERSION = "1"            # bump when the extraction / check logic changes (invalidates the cache)

HOOK = r"""
(function(){
  var _b;
  Object.defineProperty(window, '__THREE_BUNDLE', { configurable: true, get: function(){ return _b; }, set: function(v){
    _b = v;
    try {
      var T = v.THREE, C = {};
      for (var k in T) C[k] = T[k];
      C.Scene = class extends T.Scene { constructor(){ super(); (window.__scenes = window.__scenes || []).push(this); } };
      _b = Object.assign({}, v, { THREE: C });
    } catch (e) { window.__hookerr = String(e); }
  }});
})();
"""

EXTRACT = r"""
(function(){
  var T = window.__THREE_BUNDLE.THREE;
  var sc = (window.__scenes || [])[0];
  if (!sc) return JSON.stringify({error: 'no scene'});
  sc.updateMatrixWorld(true);
  function vis(o){ for (var p = o; p; p = p.parent) if (p.visible === false) return false; return true; }
  var cands = [];
  sc.traverse(function(o){
    if (!o.isMesh || o.isInstancedMesh || !o.geometry || !vis(o)) return;
    var g = o.geometry, pos = g.attributes.position;
    if (!pos || pos.count < 100) return;
    var mw = o.matrixWorld, v = new T.Vector3(), arr = new Float32Array(pos.count * 3), mn = [1e9,1e9,1e9], mx = [-1e9,-1e9,-1e9];
    for (var i = 0; i < pos.count; i++) {
      v.fromBufferAttribute(pos, i).applyMatrix4(mw);
      arr[3*i] = v.x; arr[3*i+1] = v.y; arr[3*i+2] = v.z;
      for (var k = 0; k < 3; k++) { var c = arr[3*i+k]; if (c < mn[k]) mn[k] = c; if (c > mx[k]) mx[k] = c; }
    }
    cands.push({n: pos.count, ic: g.index ? g.index.count : 0, bb: [mn, mx], pos: arr, idx: g.index ? g.index.array : null,
                col: (o.material && o.material.color) ? o.material.color.getHexString() : null, nm: o.name || ''});
  });
  window.__cands = cands;
  return JSON.stringify({n_meshes: cands.length, cands: cands.map(function(c, i){ return {i: i, n: c.n, ic: c.ic, bb: c.bb, col: c.col, nm: c.nm}; })});
})()
"""

GET = r"""
(function(i){
  var c = window.__cands[i];
  function b64(buf){ var u8 = new Uint8Array(buf.buffer, buf.byteOffset, buf.byteLength), s = '', CH = 0x8000; for (var k = 0; k < u8.length; k += CH) s += String.fromCharCode.apply(null, u8.subarray(k, k + CH)); return btoa(s); }
  return JSON.stringify({pos: b64(c.pos), idx: c.idx ? b64(c.idx) : null, itype: c.idx ? (c.idx instanceof Uint32Array ? 32 : 16) : 0});
})(%d)
"""


def sha(*parts: bytes) -> str:
    h = hashlib.sha1()
    for p in parts:
        h.update(p)
    return h.hexdigest()


def fread(p: Path) -> bytes:
    try:
        return p.read_bytes()
    except FileNotFoundError:
        return b""


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def signature(slug: str, cfg: dict) -> str:
    d = VIEW_DIR / slug
    return sha(fread(d / "index.html"), fread(d / "model.js"), fread(Path(__file__)), VERSION.encode(), json.dumps(cfg["models"].get(slug), sort_keys=True).encode(), json.dumps(cfg["tolerance"], sort_keys=True).encode())


# ----------------------------------------------------------------------------------------------- geometry helpers
def b64a(s: str, dtype) -> np.ndarray:
    return np.frombuffer(base64.b64decode(s), dtype=dtype)


def top_faces(pos: np.ndarray, idx: np.ndarray | None):
    """Return (areas of the up-facing triangles projected to the plan, their plan centroids)."""
    tri = idx.reshape(-1, 3) if idx is not None else np.arange(len(pos)).reshape(-1, 3)
    a, b, c = pos[tri[:, 0]], pos[tri[:, 1]], pos[tri[:, 2]]
    n = np.cross(b - a, c - a)                        # normal; y component = twice the signed plan area (x,z) up to sign
    # plan area (x,z) and orientation: the triangle faces up when its (x,z) winding gives n_y > 0 (three.js, y up)
    cen = (a + b + c) / 3.0
    flat = np.abs(n[:, 1]) > 1e-9
    # the winding may differ between meshes (and closed meshes have as many bottom as top faces): the highest non-vertical triangle is a
    # top face by definition, its sign of n_y defines "up-facing"
    top = np.argmax(np.where(flat, cen[:, 1], -1e18))
    sign = 1.0 if n[top, 1] > 0 else -1.0
    up = (n[:, 1] * sign) > 1e-9
    area = np.abs(n[:, 1]) / 2.0
    return area[up], cen[up][:, [0, 2]], tri


def poly_area_centroid(poly: np.ndarray):
    x, y = poly[:, 0], poly[:, 1]
    x1, y1 = np.roll(x, -1), np.roll(y, -1)
    cr = x * y1 - x1 * y
    A = cr.sum() / 2.0
    if abs(A) < 1e-9:
        return 0.0, poly.mean(0)
    cx = ((x + x1) * cr).sum() / (6 * A)
    cy = ((y + y1) * cr).sum() / (6 * A)
    return abs(A), np.array([cx, cy])


def quantise(pos: np.ndarray):
    o = pos.min(0)
    ext = np.maximum(pos.max(0) - o, 1e-6)
    q = ext / 65535.0
    u = np.rint((pos - o) / q).astype(np.uint16)
    return o, q, u


def enc(buf: np.ndarray) -> str:
    return base64.b64encode(np.ascontiguousarray(buf).tobytes()).decode("ascii")


def pack_mesh(pos: np.ndarray, idx: np.ndarray) -> dict:
    o, q, u = quantise(pos)
    it = np.uint16 if len(pos) < 65535 else np.uint32
    return {"n": int(len(pos)), "o": [round(float(v), 5) for v in o], "q": [float(f"{v:.6g}") for v in q], "pos": enc(u), "it": 16 if it is np.uint16 else 32, "idx": enc(idx.astype(it)), "ni": int(len(idx))}


# ----------------------------------------------------------------------------------------------- one model
def export_one(c, slug: str, cfg: dict, tol: dict) -> dict:
    mc = cfg["models"].get(slug)
    res: dict = {"slug": slug, "status": "not", "reason": "", "ok": False}
    if not mc:
        res["reason"] = "no entry in data/models3d_combined.json (add the frame / polygon / crest expressions for this model)"
        return res
    c.call("Page.addScriptToEvaluateOnNewDocument", source=HOOK)
    c.goto((VIEW_DIR / slug / "index.html").as_uri(), 3.0)
    if not c.wait_for("window.__scenes && window.__scenes.length && window.REEF_MODEL", 40):
        res["reason"] = "the viewer did not create a three.js scene (WebGL unavailable or viewer error)"
        return res
    c.pump(3.0)
    ex = json.loads(c.eval(EXTRACT))
    if ex.get("error"):
        res["reason"] = ex["error"]
        return res
    cands = ex["cands"]
    area = lambda k: (k["bb"][1][0] - k["bb"][0][0]) * (k["bb"][1][2] - k["bb"][0][2])
    if not cands:
        res["reason"] = "no visible mesh with >= 100 vertices in the scene"
        return res
    sea = max(cands, key=area)
    sbb = sea["bb"]
    skirt = [k for k in cands if k is not sea and area(k) >= 0.9 * area(sea)]
    reefs = [k for k in cands if k is not sea and k not in skirt and area(k) < 0.5 * area(sea)
             and k["bb"][0][0] >= sbb[0][0] - 3 and k["bb"][1][0] <= sbb[1][0] + 3 and k["bb"][0][2] >= sbb[0][2] - 3 and k["bb"][1][2] <= sbb[1][2] + 3]
    if not reefs:
        res["reason"] = "could not identify a reef mesh inside the seabed bounding box (visible meshes: %s)" % [(k["n"], k["col"]) for k in cands]
        return res

    def fetch(k):
        r = json.loads(c.eval(GET % k["i"]))
        pos = b64a(r["pos"], np.float32).reshape(-1, 3).astype(np.float64)
        idx = b64a(r["idx"], np.uint16 if r["itype"] == 16 else np.uint32).astype(np.int64) if r["idx"] else np.arange(len(pos), dtype=np.int64)
        return pos, idx

    # --- rotate scene -> combined frame (offshore -> +z), pure rotation about y
    ox, oz = mc["offshore_scene_xz"]
    nrm = math.hypot(ox, oz)
    ox, oz = ox / nrm, oz / nrm
    a = math.atan2(ox, oz)
    ca, sa = math.cos(a), math.sin(a)

    def rot(p: np.ndarray) -> np.ndarray:
        return np.stack([p[:, 0] * ca - p[:, 2] * sa, p[:, 1], p[:, 0] * sa + p[:, 2] * ca], axis=1)

    spos, sidx = fetch(sea)
    spos = rot(spos)
    rparts = []
    for k in reefs:
        p, i = fetch(k)
        rparts.append((rot(p), i))
    base = 0
    rpos, ridx = [], []
    for p, i in rparts:
        rpos.append(p)
        ridx.append(i + base)
        base += len(p)
    rpos, ridx = np.concatenate(rpos), np.concatenate(ridx)

    # --- model.js reference values (evaluated in the viewer page)
    raw = json.loads(c.eval("JSON.stringify((function(){var M=window.REEF_MODEL;return %s;})())" % mc["polygon"]))
    rings = raw if (raw and isinstance(raw[0][0], list)) else [raw]               # round 11: one ring or a list of rings (Mount Maunganui has 5 bag polygons)
    rings_c = [np.stack([mc["hand"] * np.array(r, dtype=float)[:, 0], np.array(r, dtype=float)[:, 1]], axis=1) for r in rings]    # combined frame (x', z')
    crest_ref = c.eval("(function(){var M=window.REEF_MODEL;return %s;})()" % mc["crest_z"])
    ac = [poly_area_centroid(r) for r in rings_c]
    A_poly = sum(a for a, _ in ac)
    C_ref = sum(a * cc for a, cc in ac) / A_poly
    A_ref = A_poly
    area_ref_label = "footprint area vs model.js toe polygon"
    if mc.get("area_ref_expr"):      # reference = a model.js number that already includes the flank skirt (the mesh footprint includes it)
        A_ref = float(c.eval("(function(){var M=window.REEF_MODEL;return %s;})()" % mc["area_ref_expr"]))
        area_ref_label = mc.get("area_ref_label") or "footprint area vs model.js footprint at the bed"

    # --- measures read back from the exported meshes
    ar, ce, _ = top_faces(rpos, ridx)
    A_mesh = float(ar.sum())
    C_mesh = (ce * ar[:, None]).sum(0) / ar.sum() if ar.sum() > 0 else np.array([np.nan, np.nan])
    crest = float(rpos[:, 1].max())
    foot_x = (float(rpos[:, 0].min()), float(rpos[:, 0].max()))
    foot_z = (float(rpos[:, 2].min()), float(rpos[:, 2].max()))
    res["metrics"] = {"area_m2": A_mesh, "area_ref_m2": float(A_ref), "centroid": [float(C_mesh[0]), float(C_mesh[1])], "centroid_ref": [float(C_ref[0]), float(C_ref[1])],
                      "crest_z_m": crest, "bbox_alongshore_m": foot_x[1] - foot_x[0], "bbox_offshore_m": foot_z[1] - foot_z[0], "n_reef_meshes": len(reefs), "n_skirt_ignored": len(skirt)}
    if crest_ref is None:
        crest_ref = float("nan")
    # seabed checks: slope falls away offshore (direction), and z = 0 along the shoreline
    sel = (spos[:, 2] > 20) & (spos[:, 2] < 260)
    if sel.sum() < 30:
        sel = np.ones(len(spos), dtype=bool)
    Amat = np.c_[spos[sel][:, 0], spos[sel][:, 2], np.ones(sel.sum())]
    gx, gz, _g = np.linalg.lstsq(Amat, spos[sel][:, 1], rcond=None)[0]
    off_deg = math.degrees(math.atan2(-gx, -gz))                              # angle of the downhill direction from +z towards +x
    band = np.abs(spos[:, 2]) <= 6
    if band.sum() < 10:
        band = np.abs(spos[:, 2]) <= 20
    shore_dev = float(np.abs(spos[band][:, 1]).mean()) if band.sum() >= 10 else float("nan")
    shore_name = "seabed at the shoreline is near 0 m MSL"
    if mc.get("shore_mode") == "crossing":
        # round 11 (Borth): frame y = 0 is a defence line / back of the beach (about +5 m), not the shoreline: require instead that the exported seabed
        # runs from land (> 0 m MSL) to sea (< 0 m MSL) along the cross-shore profile, i.e. a beach whose waterline lies inside the patch
        zb = np.floor(spos[:, 2] / 10.0).astype(int)
        prof = [(b, float(spos[zb == b][:, 1].mean())) for b in sorted(set(zb.tolist()))]
        cross = next((prof[i][0] * 10.0 for i in range(1, len(prof)) if prof[i - 1][1] > 0 >= prof[i][1]), None)
        shore_dev = 0.0 if cross is not None else 99.0
        shore_name = "seabed crosses 0 m MSL on a beach inside the patch (waterline at offshore %s m; the frame's y = 0 is not the shoreline)" % ("%.0f" % cross if cross is not None else "none")
    d_c = float(np.hypot(*(C_mesh - C_ref)))
    checks = [
        {"name": area_ref_label, "got": A_mesh, "ref": float(A_ref), "err": abs(A_mesh - A_ref) / A_ref, "tol": tol["area_rel"], "unit": "relative"},
        {"name": "footprint centroid vs polygon centroid", "got": [float(C_mesh[0]), float(C_mesh[1])], "ref": [float(C_ref[0]), float(C_ref[1])], "err": d_c, "tol": tol["centroid_m"], "unit": "m"},
        {"name": "crest level vs model.js", "got": crest, "ref": float(crest_ref), "err": abs(crest - crest_ref), "tol": tol["crest_m"], "unit": "m"},
        {"name": "seabed falls away offshore (+z)", "got": off_deg, "ref": 0.0, "err": abs(off_deg), "tol": tol["offshore_deg"], "unit": "deg"},
        {"name": shore_name, "got": shore_dev, "ref": 0.0, "err": shore_dev, "tol": tol["shore_m"], "unit": "m"},
    ]
    for ch in checks:
        ch["ok"] = bool(ch["err"] == ch["err"] and ch["err"] <= ch["tol"])
    res["checks"] = checks
    res["ok"] = all(ch["ok"] for ch in checks)
    res["area_m2"], res["area_ref_m2"] = A_mesh, float(A_ref)
    res["area_rel_err"] = checks[0]["err"]
    res["crest_z_m"], res["crest_ref_m"], res["crest_err_m"] = crest, float(crest_ref), checks[2]["err"]
    res["bbox_m"] = [round(foot_x[1] - foot_x[0], 1), round(foot_z[1] - foot_z[0], 1)]      # reef extent alongshore x offshore (m)

    # --- write the data file
    sb = [float(spos[:, 0].min()), float(spos[:, 0].max()), float(spos[:, 2].min()), float(spos[:, 2].max())]
    data = {"slug": slug, "bounds": sb, "seabed": pack_mesh(spos, sidx), "reef": pack_mesh(rpos, ridx),
            "footprint": [[[round(float(x), 2), round(float(z), 2)] for x, z in r] for r in rings_c], "centroid": [round(float(C_ref[0]), 2), round(float(C_ref[1]), 2)],
            "crest_z": round(crest, 3), "area_m2": round(A_mesh, 1), "y_range": [float(spos[:, 1].min()), float(spos[:, 1].max())],
            "rotation_deg": round(math.degrees(a), 3), "bbox_reef": [foot_x[0], foot_x[1], foot_z[0], foot_z[1]]}
    subs = []      # round 11: extra labels inside a model (Borth: the oval is a breakwater, not a surf reef), evaluated in the viewer page
    for sl in mc.get("sublabels", []):
        xy = json.loads(c.eval("JSON.stringify((function(){var M=window.REEF_MODEL;return %s;})())" % sl["xy"]))
        txt = c.eval("(function(){var M=window.REEF_MODEL;return %s;})()" % sl["text"])
        subs.append([round(mc["hand"] * float(xy[0]), 2), round(float(xy[1]), 2), str(txt)])
    data["sublabels"] = subs
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{slug}.js").write_text("(window.M3D_COMBINED = window.M3D_COMBINED || {})[%s] = %s;\n" % (json.dumps(slug), json.dumps(data, separators=(",", ":"))), encoding="utf-8", newline="\n")
    res["status"], res["file"] = "ok", f"3d/combined/{slug}.js"
    res["size_kb"] = round((OUT_DIR / f"{slug}.js").stat().st_size / 1024)
    res["note"] = {"rotation_deg": round(math.degrees(a), 2), "skirt_ignored": len(skirt), "reef_meshes": len(reefs), "seabed_vertices": int(len(spos)), "reef_vertices": int(len(rpos))}
    return res


def run(slugs: list[str], force: bool = False, log=print, prune: bool = True) -> dict[str, dict]:
    """Export every slug (cached by signature). Returns {slug: result}."""
    cfg = load_config()
    tol = cfg["tolerance"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    try:
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        cache = {}
    out: dict[str, dict] = {}
    todo = []
    for s in slugs:
        sig = signature(s, cfg)
        ent = cache.get(s)
        if not force and ent and ent.get("sig") == sig and (ent["result"]["status"] != "ok" or (OUT_DIR / f"{s}.js").exists()):
            out[s] = ent["result"]
            log(f"combined: {s}: cached ({out[s]['status']})")
        else:
            todo.append((s, sig))
    if todo:
        from qa_cdp import Chrome  # noqa: PLC0415
        for s, sig in todo:
            t0 = time.time()
            try:
                with Chrome(1200, 800) as c:
                    out[s] = export_one(c, s, cfg, tol)
            except Exception as e:  # noqa: BLE001
                out[s] = {"slug": s, "status": "not", "ok": False, "reason": f"export failed: {type(e).__name__}: {e}"[:300]}
            cache[s] = {"sig": sig, "result": out[s]}
            r = out[s]
            log(f"combined: {s}: {r['status']}{'' if r['status'] == 'ok' else ' - ' + r.get('reason', '')} ok={r.get('ok')} ({time.time() - t0:.0f} s)")
        CACHE.write_text(json.dumps(cache, indent=1), encoding="utf-8")
    # drop files of slugs that are gone (not when only a few slugs were asked for on the command line: round 11 fix)
    for f in (OUT_DIR.glob("*.js") if prune else []):
        if f.stem not in slugs and f.stem != "manifest":
            f.unlink()
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("slugs", nargs="*")
    a = ap.parse_args()
    slugs = a.slugs or sorted(p.name for p in VIEW_DIR.iterdir() if p.is_dir() and (p / "index.html").exists() and p.name not in ("vendor", "combined"))
    res = run(slugs, a.force, prune=not a.slugs)
    for s, r in res.items():
        print(s, r["status"], "OK" if r.get("ok") else "CHECK-FAIL/NOT", r.get("reason", ""))
        for ch in r.get("checks", []):
            print("    ", "PASS" if ch["ok"] else "FAIL", ch["name"], "got", ch["got"], "ref", ch["ref"], "err", round(ch["err"], 4), "tol", ch["tol"], ch["unit"])
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""photo_match.py - "Match this photo" transforms for the 3D models tab (round 11, brief build_3d_tab_r3.md part A).

    python src/photo_match.py            # -> data/photo_match.json (+ a short summary on stdout)

Scope: PLAN-VIEW pictures whose geometry is already documented (no new research, no oblique photos):
  (1) pictures TRACED in 07_scale/shapes/<slug>/shape.json (sources[] with pixel_polygons + scale / georef);
  (2) Garmin Navionics screenshots whose capture log gives the map centre (lat/lon), the zoom and the crop, for models that have geo.
For each picture the similarity pixel -> canonical metres (the frame of shape.json = the frame of the 3D model's model.js) is computed:
  georef  : pixel -> lon/lat (Web-Mercator bounds of the image) -> local metres -> canonical (fitted on shape.json canonical.polygons_m vs
            geo.polygons_latlon, vertex for vertex);
  direct  : the picture the canonical outline was traced on (derived_from): Umeyama fit of its pixel polygon onto canonical.polygons_m;
  icp     : any other traced picture without a georeference: the pixel polygon (metres by its stated px/m, else scaled to the outline) is
            registered onto the canonical outline (raster cross-correlation over rotation / mirror, then trimmed ICP).
Residual = RMS (symmetric, both ways) of the distance between the transformed trace and the canonical outline boundary, plus the IoU.
A picture is ELIGIBLE (button in the page) when residual <= tolerance (2 m; 10 % of the longest dimension for reefs < 40 m long).
Navionics screenshots have no outline: their residual is the geo <-> canonical fit of the model (cm); the chart's own positional accuracy is
not assessed (stated in the output).  The model's viewer receives the camera message {type:'m3d-camera', mode:'plan', ...}; scene_map (below)
is canonical (x, y) -> scene ground (X, Z) of that viewer, checked against the model.js outline.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import cKDTree
from shapely.geometry import Polygon
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
ROOT = BUILD.parent
SHAPES = ROOT / "07_scale" / "shapes"
REGS = ROOT / "03_images" / "reefs"
OUT = BUILD / "data" / "photo_match.json"

R_EARTH = 6378137.0
TOL_M = 2.0
TOL_REL_SMALL = 0.10      # reefs shorter than 40 m: 10 % of the longest dimension
EDGE_STEP = 0.0           # set per reef


# ------------------------------------------------------------------------------------------------ small geometry helpers
def merc(lat: float, lon: float) -> tuple[float, float]:
    return R_EARTH * math.radians(lon), R_EARTH * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def umeyama(src: np.ndarray, dst: np.ndarray, scale: bool = True, fixed_scale: float | None = None):
    """Least-squares similarity dst ~ s R src + t (reflection allowed). Returns s, R (2x2), t."""
    mu_s, mu_d = src.mean(0), dst.mean(0)
    xs, xd = src - mu_s, dst - mu_d
    cov = xd.T @ xs / len(src)
    u, d, vt = np.linalg.svd(cov)
    r = u @ vt                                   # reflection allowed: no sign correction
    var_s = (xs ** 2).sum() / len(src)
    if fixed_scale is not None:
        s = fixed_scale
    elif scale:
        s = float(d.sum() / var_s) if var_s > 0 else 1.0
    else:
        s = 1.0
    t = mu_d - s * r @ mu_s
    return s, r, t


def apply(s: float, r: np.ndarray, t: np.ndarray, pts: np.ndarray) -> np.ndarray:
    return s * (pts @ r.T) + t


def sample_ring(ring: np.ndarray, step: float) -> np.ndarray:
    ring = np.asarray(ring, float)
    if not np.allclose(ring[0], ring[-1]):
        ring = np.vstack([ring, ring[:1]])
    out = []
    for a, b in zip(ring[:-1], ring[1:]):
        n = max(1, int(math.ceil(np.hypot(*(b - a)) / step)))
        out.append(a + (b - a) * (np.arange(n)[:, None] / n))
    return np.vstack(out)


def sample_rings(rings, step: float) -> np.ndarray:
    return np.vstack([sample_ring(np.asarray(r, float), step) for r in rings])


def union_poly(rings):
    ps = []
    for r in rings:
        p = Polygon(r)
        if not p.is_valid:
            p = p.buffer(0)
        ps.append(p)
    return unary_union(ps)


def chamfer(src_rings, ref_rings, step: float) -> dict:
    """Symmetric boundary distance between the transformed trace and the canonical outline, plus IoU. Rings that are not part of the
    other outline (a trace ring > 10 m from every canonical ring: e.g. an inner contour; a canonical ring not drawn on this picture) are left
    out of the comparison and counted in rings_*."""
    ru_all = union_poly(ref_rings)
    su_all = union_poly(src_rings)
    keep_s = [r for r in src_rings if Polygon(r).buffer(0).distance(ru_all) <= 10.0] or list(src_rings)
    su = union_poly(keep_s)
    keep_r = [r for r in ref_rings if Polygon(r).buffer(0).distance(su) <= 10.0] or list(ref_rings)
    ru = union_poly(keep_r)
    a = sample_rings(keep_s, step)
    b = sample_rings(keep_r, step)
    d = np.concatenate([cKDTree(b).query(a)[0], cKDTree(a).query(b)[0]])
    iou = su.intersection(ru).area / max(1e-9, su.union(ru).area)
    return {"rms_m": float(np.sqrt((d ** 2).mean())), "p95_m": float(np.percentile(d, 95)), "max_m": float(d.max()),
            "iou": float(iou), "rings_trace": len(src_rings), "rings_trace_compared": len(keep_s), "rings_canonical": len(ref_rings), "rings_canonical_compared": len(keep_r)}


def raster(rings, cell: float, origin: np.ndarray, size: int) -> np.ndarray:
    im = Image.new("L", (size, size), 0)
    dr = ImageDraw.Draw(im)
    for r in rings:
        px = [((p[0] - origin[0]) / cell, (p[1] - origin[1]) / cell) for p in r]
        dr.polygon(px, fill=255)
    return np.asarray(im, float) / 255.0


def icp_register(src_m, ref_rings, fixed_scale: float | None, step: float, mirrors=(1, -1)):
    """Register trace rings (metres, picture frame: x right, y UP) onto the canonical rings. Raster cross-correlation over mirror x rotation
    for the translation, then trimmed ICP on the boundaries. fixed_scale = None -> the scale is fitted too (picture not calibrated)."""
    ref_pts = sample_rings(ref_rings, step)
    ref_tree = cKDTree(ref_pts)
    ref_c = np.array(union_poly(ref_rings).centroid.coords[0])
    src_all = np.vstack([np.asarray(r, float) for r in src_m])
    src_c = np.array(union_poly(src_m).centroid.coords[0])
    a_ref, a_src = union_poly(ref_rings).area, union_poly(src_m).area
    s0 = fixed_scale if fixed_scale is not None else math.sqrt(a_ref / a_src)
    ext = max(np.ptp(ref_pts[:, 0]), np.ptp(ref_pts[:, 1]))
    cell = max(0.05, ext / 110.0)
    size = 512
    origin = ref_c - cell * size / 2
    R = raster(ref_rings, cell, origin, size)
    FR = np.fft.rfft2(R)
    cands = []
    for mirror in mirrors:
        for th in range(0, 360, 2):
            c, s_ = math.cos(math.radians(th)), math.sin(math.radians(th))
            rot = np.array([[c, -s_], [s_, c]]) @ np.diag([mirror, 1.0])
            rings = [s0 * (np.asarray(r, float) - src_c) @ rot.T + ref_c for r in src_m]
            S = raster(rings, cell, origin, size)
            corr = np.fft.irfft2(FR * np.conj(np.fft.rfft2(S)), s=S.shape)
            iy, ix = np.unravel_index(np.argmax(corr), corr.shape)
            dy = iy if iy < size // 2 else iy - size
            dx = ix if ix < size // 2 else ix - size
            cands.append((float(corr[iy, ix]), mirror, th, np.array([dx * cell, dy * cell])))
    cands.sort(key=lambda c: -c[0])
    best = None
    for _, mirror, th, shift in cands[:6]:
        c, s_ = math.cos(math.radians(th)), math.sin(math.radians(th))
        r0 = np.array([[c, -s_], [s_, c]]) @ np.diag([mirror, 1.0])
        s, r, t = s0, r0, ref_c + shift - s0 * (r0 @ src_c)
        free = fixed_scale is None
        src_s = sample_rings(src_m, step)
        for _it in range(60):
            q = apply(s, r, t, src_s)
            dist, idx = ref_tree.query(q)
            keep = dist <= np.percentile(dist, 85)
            s2, r2, t2 = umeyama(src_s[keep], ref_pts[idx[keep]], scale=free, fixed_scale=None if free else fixed_scale)
            if free:
                s2 = min(max(s2, 0.5 * s0), 2.0 * s0)
            if abs(s2 - s) < 1e-7 and np.allclose(t2, t, atol=1e-6) and np.allclose(r2, r, atol=1e-8):
                s, r, t = s2, r2, t2
                break
            s, r, t = s2, r2, t2
        res = chamfer([apply(s, r, t, np.asarray(x, float)) for x in src_m], ref_rings, step)
        if best is None or res["rms_m"] < best[0]["rms_m"]:
            best = (res, s, r, t)
    return best


def outer_rings(rings):
    """Drop rings that lie inside another ring (inner contours, crest bands): the canonical outlines are outer edges."""
    ps = [Polygon(r).buffer(0) for r in rings]
    keep = []
    for i, p in enumerate(ps):
        if not any(j != i and ps[j].area > p.area and ps[j].contains(p) for j in range(len(ps))):
            keep.append(rings[i])
    return keep or list(rings)


def match_rings(pix, ref):
    """Indices of trace rings that correspond vertex for vertex (same order, same vertex count, +-1 for a closing duplicate) to each reference ring; None if any is missing."""
    idx, j = [], 0
    for q in ref:
        while j < len(pix) and abs(len(pix[j]) - len(q)) > 1:
            j += 1
        if j >= len(pix):
            return None
        idx.append(j)
        j += 1
    return idx


# ------------------------------------------------------------------------------------------------ model.js access
def load_model(slug: str) -> dict:
    t = (SHAPES / slug / "3d" / "model.js").read_text(encoding="utf-8")        # the model agent's file (the page's 3d/<slug>/model.js is a copy of it)
    return json.loads(t[t.index("{"): t.rindex("}") + 1])


def default_version(m: dict) -> dict:
    return [v for v in m["versions"] if v["id"] == m["default_version"]][0]


def model_rings(slug: str, m: dict):
    """The default outline of the model in ITS frame, as a list of rings (used only to verify frame + offset against shape.json)."""
    if slug.startswith("borth"):
        return default_version(m)["outline_m"]
    if slug.startswith("mount-maun"):
        return default_version(m)["polygons_m"]
    if slug.startswith("boscombe"):
        return [[p[:2] for p in m["reef"]["toe_polygon_xyzz"]]]
    if slug.startswith("bunbury"):
        c = m["reef"]["centre_default"]
        return [[[p[0] + c[0], p[1] + c[1]] for p in m["reef"]["toe_polygon_m"]]]
    if slug.startswith("palm"):
        return [m["reef"]["toe_polygon"]]
    if slug.startswith("prattes"):
        return [m["reef"]["toe_polygon_xy_m"]]
    raise KeyError(slug)


def scene_map(slug: str, m: dict):
    """canonical (x, y) -> scene ground (X, Z) of the model's own viewer, 2x2 matrix (rows X, Z). From the combined-scene frame notes
    (data/models3d_combined.json): 'X = x, Z = y' for most; Bunbury Z = -y; Palm converts to east / north (E = x sin bx + y sin by, N = x cos bx + y cos by,
    scene X = E, Z = -N)."""
    if slug.startswith("bunbury"):
        return [[1.0, 0.0], [0.0, -1.0]], "scene X = x, Z = -y (viewer frame note, Bunbury)"
    if slug.startswith("palm"):
        bx, by = math.radians(m["frame"]["x_bearing_deg"]), math.radians(m["frame"]["y_bearing_deg"])
        return [[round(math.sin(bx), 8), round(math.sin(by), 8)], [round(-math.cos(bx), 8), round(-math.cos(by), 8)]], \
            "scene X = E = x sin(bx) + y sin(by), Z = -N = -(x cos(bx) + y cos(by)) (viewer toT())"
    return [[1.0, 0.0], [0.0, 1.0]], "scene X = x, Z = y (viewer frame note)"


# ------------------------------------------------------------------------------------------------ one model
def sha_of(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def geo_fit(shape: dict):
    """local metres (Mercator x cos(lat0)) -> canonical, from canonical.polygons_m vs geo.polygons_latlon (vertex for vertex)."""
    g = shape.get("geo") or {}
    pl = g.get("polygons_latlon") or g.get("toe_polygons_latlon")
    cm = shape["canonical"]["polygons_m"]
    if not pl or not isinstance(pl[0], list) or not isinstance(pl[0][0], list):
        return None
    src, dst = [], []
    for ring_ll, ring_m in zip(pl, cm):
        if len(ring_ll) == len(ring_m) + 1 and ring_ll[0] == ring_ll[-1]:
            ring_ll = ring_ll[:-1]
        if len(ring_ll) != len(ring_m):
            return None
        src += [merc(la, lo) for la, lo in ring_ll]
        dst += [tuple(p) for p in ring_m]
    src, dst = np.array(src), np.array(dst)
    lat0 = float(np.mean([p[0] for ring in pl for p in ring]))
    k = math.cos(math.radians(lat0))
    s, r, t = umeyama(src * k, dst, scale=True)
    res = np.sqrt(((apply(s, r, t, src * k) - dst) ** 2).sum(1))
    return {"k": k, "s": s, "r": r, "t": t, "lat0": lat0, "rms_m": float(np.sqrt((res ** 2).mean())), "max_m": float(res.max()), "n": len(src)}


def latlon_to_canon(gf: dict, lat: float, lon: float) -> np.ndarray:
    x, y = merc(lat, lon)
    return apply(gf["s"], gf["r"], gf["t"], np.array([[x * gf["k"], y * gf["k"]]]))[0]


def affine_from_func(f) -> list[float]:
    p0 = np.asarray(f(0.0, 0.0), float)
    px = np.asarray(f(1.0, 0.0), float) - p0
    py = np.asarray(f(0.0, 1.0), float) - p0
    return [float(px[0]), float(py[0]), float(p0[0]), float(px[1]), float(py[1]), float(p0[1])]    # x = a px + b py + tx ; y = c px + d py + ty


def describe(aff: list[float], w: int, h: int, crop=None) -> dict:
    a, b, tx, c, d, ty = aff
    fx, fy, fw, fh = crop or (0.0, 0.0, 1.0, 1.0)
    cx_px, cy_px = (fx + fw / 2) * w, (fy + fh / 2) * h
    center = [a * cx_px + b * cy_px + tx, c * cx_px + d * cy_px + ty]
    wpx, hpx = fw * w, fh * h
    width_m = math.hypot(a, c) * wpx
    height_m = math.hypot(b, d) * hpx
    up = np.array([-b, -d], float)
    up /= np.hypot(*up)
    right = np.array([a, c], float)
    right /= np.hypot(*right)
    det_rh = float(right[0] * up[1] - right[1] * up[0])          # (picture right, picture up) -> canonical: +1 proper, -1 mirrored
    return {"center_m": [round(center[0], 3), round(center[1], 3)], "up_m": [round(float(up[0]), 6), round(float(up[1]), 6)],
            "rotation_deg": round(math.degrees(math.atan2(up[1], up[0])), 3), "width_m": round(width_m, 3), "height_m": round(height_m, 3),
            "m_per_px": round(float(math.sqrt(abs(a * d - b * c))), 6), "mirror": det_rh < 0}


def process_model(slug: str, out: dict) -> None:
    sj = json.loads((SHAPES / slug / "shape.json").read_text(encoding="utf-8"))
    m = load_model(slug)
    canon = [np.asarray(r, float) for r in sj["canonical"]["polygons_m"]]
    max_dim = float(sj["canonical"].get("max_dim_m") or max(np.ptp(np.vstack(canon)[:, 0]), np.ptp(np.vstack(canon)[:, 1])))
    tol = TOL_M if max_dim >= 40 else round(TOL_REL_SMALL * max_dim, 2)
    step = max(0.05, min(1.0, max_dim / 150.0))
    # (a) frame check: canonical outline vs the model.js default outline (the viewer's own frame)
    mr = [np.asarray(r, float) for r in model_rings(slug, m)]
    cu, mu = union_poly(canon), union_poly(mr)
    off = np.array(mu.centroid.coords[0]) - np.array(cu.centroid.coords[0])
    sm, sm_note = scene_map(slug, m)
    out["viewers"][slug] = {"scene_map": sm, "scene_map_note": sm_note,
                            "frame_check": {"iou_canonical_vs_model_outline": round(cu.intersection(mu).area / cu.union(mu).area, 3),
                                            "centroid_offset_canonical_to_model_m": [round(float(off[0]), 2), round(float(off[1]), 2)],
                                            "note": "model.js default outline vs shape.json canonical outline (different edge definitions are expected for Borth / Mount Maunganui versions); an offset > 3 m means the viewer frame is shifted against the canonical frame"},
                            "tolerance_m": tol}
    shift = off if out['viewers'][slug]['frame_check']['iou_canonical_vs_model_outline'] < 0.2 else np.zeros(2)   # outlines do not overlap at all = the viewer frame is shifted (Bunbury: reef at its distance offshore); applied before the scene map
    out["viewers"][slug]["canon_to_model_shift_m"] = [round(float(shift[0]), 3), round(float(shift[1]), 3)]
    det_a = sm[0][0] * sm[1][1] - sm[0][1] * sm[1][0]               # +1 / -1: handedness of canonical -> scene
    gf = geo_fit(sj)
    if gf:
        out["viewers"][slug]["geo_fit"] = {"rms_m": round(gf["rms_m"], 3), "max_m": round(gf["max_m"], 3), "scale": round(gf["s"], 6), "vertices": gf["n"]}
    try:
        reg = json.loads((REGS / slug / "images.json").read_text(encoding="utf-8"))
    except OSError:
        reg = []
    by_sha = {r.get("sha256"): r for r in reg}
    by_url = {r.get("image_url"): r for r in reg if r.get("image_url")}
    by_name = {Path((r.get("file") or "").replace("\\", "/")).name: r for r in reg}

    def reg_row(src: dict):
        lf = ROOT / (src.get("local_file") or "")
        row = by_sha.get(sha_of(lf)) if lf.is_file() else None
        return row or by_url.get(src.get("url"))

    versions = [(f"outline version {v['id']}", [np.asarray(r, float) for r in v["polygons_m"]], v.get("source_ids") or [])
                for v in (sj.get("outline_versions") or []) if v.get("polygons_m")]
    for src in sj["sources"]:
        pp = src.get("pixel_polygons") or []
        if not pp:
            continue
        sid = src["id"]
        row = reg_row(src)
        if row is None:
            out["excluded"].append({"slug": slug, "source_id": sid, "reason": "no registry row (picture is not in the page's picture panel)"})
            continue
        w, h = src.get("image_size") or [None, None]
        sc = src.get("scale") or {}
        ppm = sc.get("px_per_m") if isinstance(sc.get("px_per_m"), (int, float)) else None
        txt = " ".join(str(x) for x in (src.get("title"), sc.get("method"), sc.get("evidence"), src.get("traced_what"))).lower()
        if "oblique" in txt and "near-nadir" not in txt:
            out["excluded"].append({"slug": slug, "source_id": sid, "registry_id": row["id"], "reason": "oblique picture (no plan-view button; human alignment is enough)"})
            continue
        pix = [np.asarray(r, float) for r in pp]
        refs = []                                                    # reference outlines in the canonical frame this picture may be compared with
        if sj["canonical"].get("derived_from", "").split(" ")[0] == sid:
            refs.append(("canonical outline (shape.json, traced on this picture)", canon))
        refs += [(n, rr) for n, rr, sids in versions if sid in sids]
        if not any(n.startswith("canonical") for n, _ in refs):
            refs.append(("canonical outline (shape.json)", canon))
        georef = src.get("georef") if isinstance(src.get("georef"), dict) and src["georef"].get("bounds") else None
        method, aff, note, used_rings, ref_name = None, None, "", None, None
        try:
            if georef and gf and w:
                bnd = georef["bounds"]
                x0, y_s = merc(bnd["south"], bnd["west"])
                x1, y_n = merc(bnd["north"], bnd["east"])

                def f(px, py, x0=x0, x1=x1, y_n=y_n, y_s=y_s):
                    xm = x0 + (x1 - x0) * px / w
                    ym = y_n + (y_s - y_n) * py / h                   # py = 0 is the NORTH edge
                    return apply(gf["s"], gf["r"], gf["t"], np.array([[xm * gf["k"], ym * gf["k"]]]))[0]
                aff = affine_from_func(f)
                method = "georef"
                note = f"pixel -> Web-Mercator bounds of the image ({str(georef.get('provider', ''))[:60]}) -> canonical via the geo <-> canonical fit (rms {gf['rms_m']:.3f} m, scale {gf['s']:.5f})"
                used_rings = outer_rings(pix)
            else:
                for rn, rr in refs:                                   # vertex-for-vertex correspondence with a reference outline
                    idx = match_rings(pix, rr)
                    if idx is None:
                        continue
                    sp = np.vstack([np.c_[pix[j][:min(len(pix[j]), len(q))][:, 0], -pix[j][:min(len(pix[j]), len(q))][:, 1]] for j, q in zip(idx, rr)])
                    dp = np.vstack([q[:min(len(pix[j]), len(q))] for j, q in zip(idx, rr)])
                    s_, r_, t_ = umeyama(sp, dp, scale=True)
                    rms_v = float(np.sqrt(((apply(s_, r_, t_, sp) - dp) ** 2).sum(1).mean()))
                    if rms_v > 0.75:
                        continue
                    aff = [float(s_ * r_[0, 0]), float(-s_ * r_[0, 1]), float(t_[0]), float(s_ * r_[1, 0]), float(-s_ * r_[1, 1]), float(t_[1])]
                    method, ref_name = "direct", rn
                    used_rings = [pix[j] for j in idx]
                    note = f"vertex-for-vertex Umeyama fit of {len(idx)} traced ring(s) onto the {rn} (vertex rms {rms_v:.3f} m)"
                    refs = [(rn, rr)]
                    break
                if aff is None and not (georef or ppm):
                    out["excluded"].append({"slug": slug, "source_id": sid, "registry_id": row["id"], "reason": "picture not calibrated (no px/m, no georeference, no vertex correspondence): scale would only be fitted to the outline"})
                    continue
                if aff is None:
                    used_rings = outer_rings(pix)
                    src_m = [np.c_[p[:, 0], -p[:, 1]] / (ppm if ppm else 1.0) for p in used_rings]
                    best = None
                    for rn, rr in refs:
                        res_i, s_, r_, t_ = icp_register(src_m, rr, 1.0 if ppm else None, step, mirrors=((-1,) if det_a > 0 else (1,)))
                        if best is None or res_i["rms_m"] < best[0]["rms_m"]:
                            best = (res_i, s_, r_, t_, rn)
                    res_i, s_, r_, t_, ref_name = best
                    k = 1.0 / (ppm if ppm else 1.0)
                    aff = [float(s_ * k * r_[0, 0]), float(-s_ * k * r_[0, 1]), float(t_[0]), float(s_ * k * r_[1, 0]), float(-s_ * k * r_[1, 1]), float(t_[1])]
                    method = "icp"
                    note = ("trace registered onto the " + ref_name + " (raster correlation over rotation, trimmed ICP); "
                            + (f"scale = the stated {ppm} px/m" if ppm else "picture not calibrated: scale fitted to the outline"))
        except Exception as e:  # noqa: BLE001
            out["excluded"].append({"slug": slug, "source_id": sid, "reason": f"transform failed: {e}"})
            continue
        a, b_, tx, c, d_, ty = aff
        tr = [np.c_[a * p[:, 0] + b_ * p[:, 1] + tx, c * p[:, 0] + d_ * p[:, 1] + ty] for p in used_rings]
        resid = None
        for rn, rr in refs:
            ri = chamfer(tr, rr, step)
            if resid is None or ri["rms_m"] < resid["rms_m"]:
                resid, ref_name = ri, rn
        info = describe(aff, w, h)
        if ppm:
            info["m_per_px_stated"] = round(1.0 / ppm, 6)
            info["scale_vs_stated_pct"] = round((info["m_per_px"] * ppm - 1) * 100, 2)
        tol_m = 2 * tol if method == "georef" else tol
        ent = {"slug": slug, "source_id": sid, "registry_id": row["id"], "kind": "trace", "method": method, "note": note, "reference": ref_name,
               "to_canonical": [round(v, 9) for v in aff], "image_px": [w, h], "residual": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in resid.items()},
               "tolerance_m": tol_m, "traced": src.get("traced_what", ""), "image_role": src.get("role"), **info}
        consistent = (info["mirror"] == (det_a > 0))          # the picture shows the world un-mirrored in this viewer: canonical (right, up) det = -det(scene_map)
        ent["viewer_consistent"] = bool(consistent)
        if not consistent:
            out["excluded"].append({"slug": slug, "source_id": sid, "registry_id": row["id"], "method": method,
                                    "reason": "the fitted transform is a MIRROR image relative to the viewer's scene (picture would have to be flipped)", "residual": ent["residual"]})
        elif resid["rms_m"] <= tol_m and resid["iou"] >= 0.5:
            out["pictures"][row["id"]] = ent
        else:
            out["excluded"].append({"slug": slug, "source_id": sid, "registry_id": row["id"], "method": method,
                                    "reason": f"residual {resid['rms_m']:.2f} m (IoU {resid['iou']:.2f}) > tolerance {tol_m} m (vs {ref_name})", "residual": ent["residual"]})
    process_navionics(slug, sj, gf, reg, out)


# ------------------------------------------------------------------------------------------------ Navionics / Garmin screenshots
NAV_LOGS = {
    # slug: (centre lat/lon, source of the number, image-size -> (container px: centre px), crop (x, y, w, h) in image px or None, filename rule)
    "borth-coastal-defence-reef": dict(center=(52.483453, -4.056205), size=(982, 655), crop=None,
                                       log="07_scale/shapes/borth-coastal-defence-reef/3d/src/navionics/capture_log.json (reef_latlon) + nav_geometry.json (clip 982 x 655, centre pixel 491,327)"),
    "mount-maunganui-reef": dict(center=(-37.6447833, 176.2025908), size=(982, 655), crop=None,
                                 log="07_scale/shapes/mount-maunganui-reef/3d/navionics_capture.py (REEF = shape.json geo.centroid_latlon, CLIP x400 y113 982 x 655, Leaflet setView)"),
    "palm-beach-gold-coast": dict(center=(-28.107334, 153.470913), size=(982, 655), crop=None,
                                  log="07_scale/shapes/palm-beach-gold-coast/3d/navionics_capture.py (REEF = council polygon centroid = shape.json geo.centroid_latlon, CLIP 982 x 655, Leaflet setView)"),
    "boscombe-surf-reef": dict(center=(50.71753, -1.83891), size=(1400, 900), crop=(400, 113, 1000, 751),
                               log="07_scale/shapes/boscombe-surf-reef/src/navionics_garmin_screenshots.provenance.json (map centred on 50.71753 N, 1.83891 W by Leaflet setView; 1400 x 900 screenshot, map pane x 400..1400, y 113..864)"),
}


def process_navionics(slug: str, sj: dict, gf, reg: list, out: dict) -> None:
    cfg = NAV_LOGS.get(slug)
    if not cfg:
        why = "no geo (lat/lon <-> canonical) in shape.json" if not gf else "capture log incomplete (centre / zoom / crop not recorded per screenshot)"
        n = sum(1 for r in reg if r.get("kind") == "chart_screenshot")
        if n:
            out["excluded"].append({"slug": slug, "source_id": "navionics", "reason": f"Navionics/Garmin screenshots ({n}) not offered: {why}"})
        return
    if not gf:
        out["excluded"].append({"slug": slug, "source_id": "navionics", "reason": "no geo in shape.json"})
        return
    import re
    for r in reg:
        if r.get("kind") != "chart_screenshot":
            continue
        name = Path((r.get("file") or "").replace("\\", "/")).name
        mz = re.search(r"_z(\d+)", name)
        if not mz or "options" in name:
            continue
        w0, h0 = cfg["size"]
        px = r.get("px") or [None, None]
        if tuple(px) != (w0, h0):
            out["excluded"].append({"slug": slug, "source_id": name, "registry_id": r["id"], "reason": f"image size {px} differs from the capture log's {cfg['size']}"})
            continue
        z = int(mz.group(1))
        crop = cfg["crop"]
        cx, cy = (crop[0] + crop[2] / 2, crop[1] + crop[3] / 2) if crop else (w0 / 2, h0 / 2)
        mpp = 156543.03392 / 2 ** z                                   # Mercator metres per px at zoom z (256-px tiles)
        lat0, lon0 = cfg["center"]
        xc, yc = merc(lat0, lon0)

        def f(pxx, pyy):
            xm, ym = xc + (pxx - cx) * mpp, yc - (pyy - cy) * mpp
            lon = math.degrees(xm / R_EARTH)
            lat = math.degrees(2 * math.atan(math.exp(ym / R_EARTH)) - math.pi / 2)
            return latlon_to_canon(gf, lat, lon)
        aff = affine_from_func(f)
        cfrac = [crop[0] / w0, crop[1] / h0, crop[2] / w0, crop[3] / h0] if crop else None
        info = describe(aff, w0, h0, cfrac)
        out["pictures"][r["id"]] = {"slug": slug, "source_id": name, "registry_id": r["id"], "kind": "navionics", "method": "web_mercator_capture_log",
                                    "note": f"north-up Web-Mercator screenshot, zoom {z}, centred on {lat0}, {lon0} ({cfg['log']}); canonical via the geo <-> canonical fit",
                                    "to_canonical": [round(v, 9) for v in aff], "image_px": [w0, h0], "crop_frac": cfrac, "zoom": z,
                                    "residual": {"rms_m": round(gf["rms_m"], 3), "max_m": round(gf["max_m"], 3), "note": "geo <-> canonical fit only; the chart's own positional accuracy is not assessed"},
                                    "tolerance_m": TOL_M, "traced": "", "image_role": "chart", **info}


# ------------------------------------------------------------------------------------------------ main
def model_slugs() -> list[str]:
    return sorted(p.name for p in SHAPES.iterdir() if (p / "3d" / "model.js").is_file() and (p / "3d" / "index.html").is_file() and (p / "shape.json").is_file())


def signature(slugs: list[str] | None = None) -> str:
    """Hash of everything photo_match.py reads: itself, every model's shape.json + model.js + picture registry."""
    h = hashlib.sha256()
    h.update(Path(__file__).read_bytes())
    for s in (slugs if slugs is not None else model_slugs()):
        for f in (SHAPES / s / "shape.json", SHAPES / s / "3d" / "model.js", REGS / s / "images.json"):
            h.update(f.read_bytes() if f.is_file() else b"-")
    return h.hexdigest()[:20]


def ensure() -> bool:
    """Re-run main() only when an input changed. True when it ran."""
    try:
        if json.loads(OUT.read_text(encoding="utf-8")).get("signature") == signature():
            return False
    except (OSError, ValueError):
        pass
    main()
    return True


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    slugs = model_slugs()
    out: dict = {"_about": ("'Match this photo' transforms (src/photo_match.py, round 11). pictures.<registry id>: to_canonical = [a, b, tx, c, d, ty] with x = a*px + b*py + tx, "
                            "y = c*px + d*py + ty (px, py = pixel of the ORIGINAL image, y down; x, y = canonical metres = the model.js frame); center_m / up_m / width_m / height_m "
                            "= the picture's ground footprint (up_m = direction of the picture's top edge); residual = RMS boundary distance of the transformed trace to the canonical "
                            "outline. viewers.<slug>.scene_map maps canonical (x, y) to the viewer's scene ground (X, Z)."),
                 "version": 1, "tolerance": {"rms_m": TOL_M, "small_reef_rule": "reefs < 40 m long: 10 % of the longest dimension", "min_iou": 0.5},
                 "viewers": {}, "pictures": {}, "excluded": []}
    for s in slugs:
        if not (SHAPES / s / "shape.json").is_file():
            out["excluded"].append({"slug": s, "source_id": "-", "reason": "no shape.json"})
            continue
        process_model(s, out)
    per = {}
    for pid, e in out["pictures"].items():
        per[e["slug"]] = per.get(e["slug"], 0) + 1
    out["summary"] = {"eligible_images": len(out["pictures"]), "per_model": per,
                      "max_residual_m": max([e["residual"]["rms_m"] for e in out["pictures"].values() if e["kind"] == "trace"] or [0.0]),
                      "max_residual_m_all_kinds": max([e["residual"]["rms_m"] for e in out["pictures"].values()] or [0.0])}
    out["signature"] = signature(slugs)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"photo_match: {out['summary']['eligible_images']} eligible pictures {per}; max trace residual {out['summary']['max_residual_m']:.2f} m; {len(out['excluded'])} excluded -> {OUT.relative_to(BUILD)}")
    for pid, e in out["pictures"].items():
        print(f"  OK  {pid[-24:]:24s} {e['kind']:8s} {e['method']:10s} rms {e['residual']['rms_m']:.2f} m  iou {e['residual'].get('iou','-')}  {e['width_m']:.0f} x {e['height_m']:.0f} m  mirror={e['mirror']}")
    for x in out["excluded"]:
        print(f"  --  {x['slug'][:10]} {x['source_id'][:14]:14s} {x['reason'][:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

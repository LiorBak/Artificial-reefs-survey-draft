#!/usr/bin/env python3
"""
geom.py - geometry helpers for reef shape tracing (07_scale/tools/).

Importable module AND a CLI. All CLI subcommands read/write JSON (stdin/file/string),
so they can be chained from PowerShell or Bash without extra parsing glue.

Functions (import these from Python):
    shoelace_area(poly) -> float                  # unsigned area, metres^2 or px^2
    signed_area(poly) -> float                     # signed; >0 = counter-clockwise (y-up)
    bbox(poly) -> dict                             # {minx,miny,maxx,maxy,width,height}
    centroid(poly) -> (cx, cy)                     # area-weighted polygon centroid
    max_dimension(poly) -> (dist, (i, j))          # largest pairwise vertex distance
    px_to_m(point, px_per_m, rotation_deg, origin_px) -> (x_m, y_m)
    m_to_px(point_m, px_per_m, rotation_deg, origin_px) -> (x_px, y_px)
    latlon_to_local_m(lat, lon, anchor_lat, anchor_lon) -> (x_m, y_m)   # equirectangular
    local_m_to_latlon(x_m, y_m, anchor_lat, anchor_lon) -> (lat, lon)
    edge_bearings_latlon(poly_latlon) -> [deg, ...]      # great-circle initial bearing per edge
    edge_bearings_xy(poly_xy, north_deg=0.0) -> [deg, ...]  # compass bearing of each edge in an
                                                            # xy plane where north_deg is the
                                                            # compass bearing of the +y axis
    angle_to_shoreline(bearing_deg, shoreline_bearing_deg) -> float   # 0-90, line-to-line angle
    fit_similarity(control_pairs) -> dict          # least-squares similarity transform + residuals
    make_canonical(shape_json_path, source_id, origin_px, alongshore_dir_px,
                    alongshore_compass_deg=None, write=True) -> dict
    selftest(verbose=True) -> bool                 # also: python geom.py selftest

Conventions (see 07_scale/SHAPE_SPEC.md "canonical" block):
    - canonical frame is in metres; origin = a shoreline point nearest the reef centroid;
      +x = alongshore (toward a stated compass direction); +y = offshore.
    - pixel frame: standard image coordinates, +x right, +y DOWN (row-major, matches Pillow).
      Because pixel +y is down and canonical +y is "offshore", the convention is: offshore =
      alongshore turned 90 deg clockwise ON SCREEN (alongshore (1,0), sea below -> +y = down).
      rotation_deg in px_to_m / m_to_px rotates the pixel-space offset (dx, dy) BY rotation_deg
      (plain [[c,-s],[s,c]] matrix), so rotation_deg = -atan2(ady, adx) puts the vector pointing
      along "alongshore_dir_px" onto +x. (Sign bug fixed 2026-10-05; run `geom.py selftest`.)

CLI examples:
    python geom.py area --polys polys.json
    python geom.py bbox --polys "[[[0,0],[10,0],[10,5],[0,5]]]"
    python geom.py centroid --polys polys.json
    python geom.py maxdim --polys polys.json
    python geom.py px2m --point 512,300 --px-per-m 4.2 --rotation-deg 15 --origin-px 500,480
    python geom.py latlon2local --lat -27.9960 --lon 153.4310 --anchor-lat -27.9965 --anchor-lon 153.4305
    python geom.py local2latlon --x 12.3 --y -40.1 --anchor-lat -27.9965 --anchor-lon 153.4305
    python geom.py bearings-latlon --polys poly_latlon.json
    python geom.py bearings-xy --polys polys.json --north-deg 0
    python geom.py angle-to-shore --bearing-deg 37 --shoreline-bearing-deg 0
    python geom.py fit-similarity --pairs pairs.json
    python geom.py make-canonical --shape shape.json --source-id img1 \
        --origin-px 640,512 --alongshore-dir-px 1,0 --alongshore-compass-deg 90
    python geom.py selftest        # rotation-convention regression test; exit code 0 = pass
"""
import argparse
import json
import math
import sys
from pathlib import Path


# --------------------------------------------------------------------------- #
# basic polygon geometry
# --------------------------------------------------------------------------- #

def signed_area(poly):
    """Signed polygon area via the shoelace formula. poly = [[x,y], ...]."""
    n = len(poly)
    if n < 3:
        return 0.0
    s = 0.0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return s / 2.0


def shoelace_area(poly):
    """Unsigned polygon area."""
    return abs(signed_area(poly))


def bbox(poly):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    return {"minx": minx, "miny": miny, "maxx": maxx, "maxy": maxy,
            "width": maxx - minx, "height": maxy - miny}


def centroid(poly):
    """Area-weighted polygon centroid. Falls back to vertex average if area ~ 0
    (degenerate / collinear points, e.g. a line traced as a 'polygon')."""
    a = signed_area(poly)
    n = len(poly)
    if abs(a) < 1e-9:
        xs = [p[0] for p in poly]
        ys = [p[1] for p in poly]
        return (sum(xs) / n, sum(ys) / n)
    cx = cy = 0.0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        cross = x1 * y2 - x2 * y1
        cx += (x1 + x2) * cross
        cy += (y1 + y2) * cross
    cx /= (6 * a)
    cy /= (6 * a)
    return (cx, cy)


def max_dimension(poly):
    """Largest pairwise distance between any two vertices (O(n^2); fine for traced
    polygons which have at most a few dozen vertices)."""
    best = 0.0
    best_pair = (0, 0)
    n = len(poly)
    for i in range(n):
        for j in range(i + 1, n):
            dx = poly[i][0] - poly[j][0]
            dy = poly[i][1] - poly[j][1]
            d = math.hypot(dx, dy)
            if d > best:
                best = d
                best_pair = (i, j)
    return best, best_pair


# --------------------------------------------------------------------------- #
# pixel <-> metres (canonical frame)
# --------------------------------------------------------------------------- #

def px_to_m(point, px_per_m, rotation_deg, origin_px):
    """Convert one pixel coordinate to canonical metres.

    point, origin_px: (x_px, y_px) in image pixel space (+y down).
    px_per_m: pixel scale (pixels per metre) measured on the image.
    rotation_deg: the angle the pixel-space offset (dx, dy) = point - origin_px is
        rotated BY, using the plain matrix [[cos,-sin],[sin,cos]] applied to (dx, dy).
        Because pixel +y is down, a positive angle looks clockwise on screen.
        It is the rotation that carries the pixel-space 'alongshore' direction onto
        canonical +x, so for an alongshore vector (adx, ady) it is
        -atan2(ady, adx) in degrees (this is what make_canonical() passes).
        rotation_deg = 0 means the image x axis already is the alongshore axis.

    FIX 2026-10-05: this used to rotate by -rotation_deg (a double negation with
    make_canonical), which was only right for rotation_deg = 0 or 180.
    """
    dx = point[0] - origin_px[0]
    dy = point[1] - origin_px[1]
    theta = math.radians(rotation_deg)
    rx = dx * math.cos(theta) - dy * math.sin(theta)
    ry = dx * math.sin(theta) + dy * math.cos(theta)
    return (rx / px_per_m, ry / px_per_m)


def m_to_px(point_m, px_per_m, rotation_deg, origin_px):
    """Inverse of px_to_m (rotates by -rotation_deg, then adds origin_px)."""
    rx = point_m[0] * px_per_m
    ry = point_m[1] * px_per_m
    theta = math.radians(-rotation_deg)
    dx = rx * math.cos(theta) - ry * math.sin(theta)
    dy = rx * math.sin(theta) + ry * math.cos(theta)
    return (dx + origin_px[0], dy + origin_px[1])


# --------------------------------------------------------------------------- #
# lat/lon <-> local metres (equirectangular about an anchor point)
# --------------------------------------------------------------------------- #

_EARTH_R = 6378137.0  # metres, WGS84 equatorial radius (matches Web Mercator sphere)


def latlon_to_local_m(lat, lon, anchor_lat, anchor_lon):
    """Equirectangular projection about (anchor_lat, anchor_lon). Good to a few cm of
    error over the ~1 km scale these reef sites span. +x = east, +y = north."""
    anchor_rad = math.radians(anchor_lat)
    x = math.radians(lon - anchor_lon) * _EARTH_R * math.cos(anchor_rad)
    y = math.radians(lat - anchor_lat) * _EARTH_R
    return (x, y)


def local_m_to_latlon(x_m, y_m, anchor_lat, anchor_lon):
    anchor_rad = math.radians(anchor_lat)
    lon = anchor_lon + math.degrees(x_m / (_EARTH_R * math.cos(anchor_rad)))
    lat = anchor_lat + math.degrees(y_m / _EARTH_R)
    return (lat, lon)


# --------------------------------------------------------------------------- #
# bearings and angles
# --------------------------------------------------------------------------- #

def _great_circle_bearing(lat1, lon1, lat2, lon2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dlon = math.radians(lon2 - lon1)
    y = math.sin(dlon) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(dlon)
    return (math.degrees(math.atan2(y, x)) + 360.0) % 360.0


def edge_bearings_latlon(poly_latlon):
    """Compass bearing (deg, clockwise from true north) of each edge, computed as the
    great-circle initial bearing between consecutive [lat, lon] vertices."""
    n = len(poly_latlon)
    out = []
    for i in range(n):
        lat1, lon1 = poly_latlon[i]
        lat2, lon2 = poly_latlon[(i + 1) % n]
        out.append(_great_circle_bearing(lat1, lon1, lat2, lon2))
    return out


def edge_bearings_xy(poly_xy, north_deg=0.0):
    """Compass bearing of each edge of a polygon given in a flat xy plane (e.g. the
    canonical metres frame, or georeferenced local metres), where north_deg is the
    compass bearing (deg, clockwise from true north) that the plane's +y axis points.
    Standard screen/plot xy (+x right, +y 'up' in-plane) is assumed; for pixel-space
    polygons (+y down) negate dy before calling, or use north_deg + 180 as needed."""
    n = len(poly_xy)
    out = []
    for i in range(n):
        x1, y1 = poly_xy[i]
        x2, y2 = poly_xy[(i + 1) % n]
        dx, dy = x2 - x1, y2 - y1
        # bearing of vector (dx,dy) in a plane whose +y is north_deg: standard math angle
        # atan2(dx, dy) gives angle clockwise from +y (= north_deg), which is exactly a
        # compass bearing once offset by north_deg.
        bearing = (math.degrees(math.atan2(dx, dy)) + north_deg) % 360.0
        out.append(bearing)
    return out


def angle_to_shoreline(bearing_deg, shoreline_bearing_deg):
    """Angle (0-90 deg) between an edge/arm and the shoreline, treating both as
    undirected lines (so a bearing and its reciprocal, +/-180 deg, are equivalent)."""
    diff = abs((bearing_deg - shoreline_bearing_deg) % 180.0)
    return min(diff, 180.0 - diff)


# --------------------------------------------------------------------------- #
# similarity-transform fit (for checking a traced shape against known control points)
# --------------------------------------------------------------------------- #

def fit_similarity(control_pairs):
    """Least-squares similarity transform (uniform scale + rotation + translation,
    NO reflection) mapping src -> dst, given control_pairs = [[[sx,sy],[dx,dy]], ...]
    with >= 2 pairs. Returns scale, rotation_deg, translation (tx,ty), per-point
    residual distances after transform, and their RMS.

    Uses the closed-form (Umeyama-style) solution for a 2D similarity transform.
    """
    n = len(control_pairs)
    if n < 2:
        raise ValueError("fit_similarity needs at least 2 control pairs")
    src = [p[0] for p in control_pairs]
    dst = [p[1] for p in control_pairs]
    sx_mean = sum(p[0] for p in src) / n
    sy_mean = sum(p[1] for p in src) / n
    dx_mean = sum(p[0] for p in dst) / n
    dy_mean = sum(p[1] for p in dst) / n

    sxx = sxy = syx = syy = 0.0
    src_var = 0.0
    for (sx, sy), (dx, dy) in zip(src, dst):
        sx0, sy0 = sx - sx_mean, sy - sy_mean
        dx0, dy0 = dx - dx_mean, dy - dy_mean
        sxx += sx0 * dx0
        sxy += sx0 * dy0
        syx += sy0 * dx0
        syy += sy0 * dy0
        src_var += sx0 * sx0 + sy0 * sy0

    # Rotation that best aligns src onto dst (no reflection): theta = atan2(a, b)
    # derived from the 2x2 cross-covariance, restricted to SO(2).
    a = sxy - syx
    b = sxx + syy
    theta = math.atan2(a, b)
    scale = (b * math.cos(theta) + a * math.sin(theta)) / src_var if src_var > 1e-12 else 1.0

    cos_t, sin_t = math.cos(theta), math.sin(theta)
    tx = dx_mean - scale * (cos_t * sx_mean - sin_t * sy_mean)
    ty = dy_mean - scale * (sin_t * sx_mean + cos_t * sy_mean)

    residuals = []
    for (sx, sy), (dx, dy) in zip(src, dst):
        px = scale * (cos_t * sx - sin_t * sy) + tx
        py = scale * (sin_t * sx + cos_t * sy) + ty
        residuals.append(math.hypot(px - dx, py - dy))
    rms = math.sqrt(sum(r * r for r in residuals) / n)

    return {
        "scale": scale,
        "rotation_deg": math.degrees(theta),
        "translation": [tx, ty],
        "residuals": residuals,
        "rms_residual": rms,
        "n_pairs": n,
    }


# --------------------------------------------------------------------------- #
# make_canonical: fill the shape.json "canonical" block from one source's trace
# --------------------------------------------------------------------------- #

def make_canonical(shape_json_path, source_id, origin_px, alongshore_dir_px,
                    alongshore_compass_deg=None, write=True):
    """Read shape.json, take the pixel_polygons + scale.px_per_m of the source whose
    id == source_id, and fill the top-level 'canonical' block per SHAPE_SPEC.md:
    metres frame, origin = origin_px (a shoreline point), +x = alongshore in the
    direction of alongshore_dir_px (a pixel-space vector, need not be unit length),
    +y = offshore, DEFINED as +x turned 90 deg clockwise as seen on screen. In pixel
    coordinates (y down) with u = alongshore_dir_px / |alongshore_dir_px| that is the
    direction (-u_y, u_x). Normal case: alongshore_dir_px = (1, 0) (shore runs
    left-to-right) and the sea is below the shoreline -> offshore = image down.
    If the sea is on the other side in the photo, reverse alongshore_dir_px; the
    canonical y of a reef in the sea is then positive again. (Sign convention
    verified by `python geom.py selftest`.)

    alongshore_compass_deg: if known (real-world compass bearing of the chosen +x
    direction, image assumed north-up), the shore-normal (offshore) bearing is
    recorded as (alongshore_compass_deg + 90) % 360; left None if not supplied.

    Returns the canonical dict. If write=True (default), writes it back into
    shape.json under the "canonical" key.
    """
    shape_path = Path(shape_json_path)
    data = json.loads(shape_path.read_text(encoding="utf-8"))

    source = None
    for s in data.get("sources", []):
        if s.get("id") == source_id:
            source = s
            break
    if source is None:
        raise ValueError(f"source id '{source_id}' not found in {shape_json_path}")

    polys_px = source.get("pixel_polygons")
    if not polys_px:
        raise ValueError(f"source '{source_id}' has no pixel_polygons")

    scale = source.get("scale") or {}
    px_per_m = scale.get("px_per_m")
    if not px_per_m:
        raise ValueError(f"source '{source_id}' has no scale.px_per_m")

    # rotation_deg: the rotation px_to_m applies to the pixel offset (dx, dy) so that
    # the alongshore_dir_px vector lands on canonical +x. The vector sits at pix_angle
    # (atan2(ady, adx), clockwise on screen because pixel y is down), so rotate by
    # -pix_angle. px_to_m rotates by +rotation_deg (sign bug fixed 2026-10-05).
    adx, ady = alongshore_dir_px
    if math.hypot(adx, ady) < 1e-12:
        raise ValueError("alongshore_dir_px must be a non-zero direction vector")
    pix_angle = math.degrees(math.atan2(ady, adx))  # angle of the vector in pixel space
    rotation_deg = -pix_angle

    polygons_m = []
    for poly in polys_px:
        polygons_m.append([list(px_to_m(pt, px_per_m, rotation_deg, origin_px)) for pt in poly])

    all_pts = [pt for poly in polygons_m for pt in poly]
    bb = bbox(all_pts)
    area_m2 = sum(shoelace_area(poly) for poly in polygons_m)
    max_dim, _ = max_dimension(all_pts)

    # distance offshore: how far the farthest offshore point (+y, since +y = offshore)
    # sits from the origin along y -- i.e. max y amongst all points (origin y = 0).
    distance_offshore_m = max(pt[1] for pt in all_pts)

    shore_normal_bearing_deg = None
    if alongshore_compass_deg is not None:
        shore_normal_bearing_deg = (alongshore_compass_deg + 90.0) % 360.0

    canonical = {
        "frame": "metres; origin = shoreline point nearest reef centroid; "
                 "+x alongshore; +y offshore",
        "derived_from": source_id,
        "polygons_m": polygons_m,
        "area_m2": area_m2,
        "bbox_m": {"alongshore": bb["width"], "crossshore": bb["height"]},
        "max_dim_m": max_dim,
        "distance_offshore_m": distance_offshore_m,
        "shore_normal_bearing_deg": shore_normal_bearing_deg,
    }

    if write:
        data["canonical"] = canonical
        shape_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    return canonical


# --------------------------------------------------------------------------- #
# selftest:  python geom.py selftest
# --------------------------------------------------------------------------- #

def selftest(verbose=True):
    """Check the pixel <-> canonical-metres chain (px_to_m, m_to_px, make_canonical) and
    fit_similarity. Returns True if every check passes. Added 2026-10-05 with the fix of
    the rotation-sign bug (px_to_m used to rotate by -rotation_deg, i.e. by +phi instead
    of -phi, so any alongshore direction other than (1,0)/(-1,0) came out rotated by 2*phi).

    Convention under test (SHAPE_SPEC.md: +x alongshore, +y offshore; README: offshore =
    alongshore turned 90 deg clockwise on screen, so shore (1,0) with the sea below the
    shoreline gives +y = image down)."""
    import tempfile

    state = {"n": 0, "bad": []}

    def check(label, got, want, tol=1e-9):
        state["n"] += 1
        ok = all(abs(g - w) <= tol for g, w in zip(got, want))
        if not ok:
            state["bad"].append(label)
            print(f"  FAIL {label}: got {tuple(round(v, 9) for v in got)} want {tuple(want)}")

    def group(name, n_before, bad_before):
        n = state["n"] - n_before
        nb = len(state["bad"]) - bad_before
        if verbose:
            print(f"[{'ok' if nb == 0 else 'FAIL'}] {name}: {n - nb}/{n} checks")

    def unit(d):
        h = math.hypot(d[0], d[1])
        return (d[0] / h, d[1] / h)

    def rot_for(d):  # what make_canonical derives
        return -math.degrees(math.atan2(d[1], d[0]))

    def with_shape(directions_fn):
        with tempfile.TemporaryDirectory() as td:
            return directions_fn(Path(td))

    ORIGIN = (200.0, 300.0)

    # 1. the bug report, directly through px_to_m / make_canonical -------------------
    n0, b0 = state["n"], len(state["bad"])
    # alongshore (0,1) = image down. 10 px below the origin at 1 px/m -> x = +10 (was -10).
    check("alongshore (0,1): 10 px below origin -> x=+10",
          px_to_m((ORIGIN[0], ORIGIN[1] + 10), 1.0, rot_for((0, 1)), ORIGIN), (10.0, 0.0))
    check("same, via rotation_deg=-90 given directly",
          px_to_m((ORIGIN[0], ORIGIN[1] + 10), 1.0, -90.0, ORIGIN), (10.0, 0.0))
    check("rotation 0 unchanged", px_to_m((230, 330), 2.0, 0.0, ORIGIN), (15.0, 15.0))
    group("bug report (alongshore (0,1), point 10 px below origin)", n0, b0)

    # 2. pixel image axes under each alongshore direction -----------------------------
    # Expected (x_m, y_m) of a 1 px step RIGHT (+px x) and DOWN (+px y), at 1 px/m,
    # taken from first principles: x = step . u,  y = step . n,  u = alongshore,
    # n = u turned 90 deg clockwise on screen = (-u_y, u_x) in pixel coordinates.
    n0, b0 = state["n"], len(state["bad"])
    table = {            # direction: (right-step -> (x,y), down-step -> (x,y))
        (1, 0):  ((1, 0), (0, 1)),
        (0, 1):  ((0, -1), (1, 0)),
        (-1, 0): ((-1, 0), (0, -1)),
        (0, -1): ((0, 1), (-1, 0)),
    }
    for d, (right, down) in table.items():
        r = rot_for(d)
        check(f"dir {d}: pixel +x step", px_to_m((ORIGIN[0] + 1, ORIGIN[1]), 1.0, r, ORIGIN), right)
        check(f"dir {d}: pixel +y (down) step", px_to_m((ORIGIN[0], ORIGIN[1] + 1), 1.0, r, ORIGIN), down)
    group("both pixel axes (y down) for (1,0),(0,1),(-1,0),(0,-1)", n0, b0)

    # 3. general directions incl. a 30-degree diagonal and a small tilt ---------------
    n0, b0 = state["n"], len(state["bad"])
    dirs = {
        "(1,0)": (1.0, 0.0), "(0,1)": (0.0, 1.0), "(-1,0)": (-1.0, 0.0),
        "30deg diag (cos30,sin30)": (math.cos(math.radians(30)), math.sin(math.radians(30))),
        "-30deg diag": (math.cos(math.radians(-30)), math.sin(math.radians(-30))),
        "150deg diag": (math.cos(math.radians(150)), math.sin(math.radians(150))),
        "tilt (0.9934,-0.1157) (Boscombe)": (0.9934, -0.1157),
        "non-unit (3,4)": (3.0, 4.0),
    }
    for label, d in dirs.items():
        u = unit(d)
        nrm = (-u[1], u[0])
        ppm = 4.25
        r = rot_for(d)
        # 10 m alongshore, 7 m offshore, and both, laid out in pixels from first principles
        p_al = (ORIGIN[0] + u[0] * 10 * ppm, ORIGIN[1] + u[1] * 10 * ppm)
        p_of = (ORIGIN[0] + nrm[0] * 7 * ppm, ORIGIN[1] + nrm[1] * 7 * ppm)
        p_bo = (ORIGIN[0] + (10 * u[0] + 7 * nrm[0]) * ppm, ORIGIN[1] + (10 * u[1] + 7 * nrm[1]) * ppm)
        check(f"{label}: 10 m alongshore", px_to_m(p_al, ppm, r, ORIGIN), (10.0, 0.0), 1e-9)
        check(f"{label}: 7 m offshore", px_to_m(p_of, ppm, r, ORIGIN), (0.0, 7.0), 1e-9)
        check(f"{label}: 10 m along + 7 m off", px_to_m(p_bo, ppm, r, ORIGIN), (10.0, 7.0), 1e-9)
        check(f"{label}: origin -> (0,0)", px_to_m(ORIGIN, ppm, r, ORIGIN), (0.0, 0.0))
    group("general directions incl. 30-degree diagonal (px_to_m)", n0, b0)

    # 4. round trips px -> m -> px and m -> px -> m ------------------------------------
    n0, b0 = state["n"], len(state["bad"])
    pts_px = [(200.0, 300.0), (250.5, 280.25), (10.0, 900.0), (-40.0, -15.5), (640.0, 512.0)]
    pts_m = [(0.0, 0.0), (12.5, -3.0), (-80.25, 44.0), (300.0, 150.0)]
    for rot in (0.0, 90.0, -90.0, 180.0, 30.0, -30.0, 6.6, 123.4, -271.0):
        for ppm in (0.5273, 1.0, 5.1549):
            for p in pts_px:
                m = px_to_m(p, ppm, rot, ORIGIN)
                check(f"px->m->px rot={rot} ppm={ppm} p={p}", m_to_px(m, ppm, rot, ORIGIN), p, 1e-8)
            for q in pts_m:
                px = m_to_px(q, ppm, rot, ORIGIN)
                check(f"m->px->m rot={rot} ppm={ppm} q={q}", px_to_m(px, ppm, rot, ORIGIN), q, 1e-8)
    # m_to_px also puts metres where the geometry says (30 deg diagonal, 10 m alongshore)
    u30 = (math.cos(math.radians(30)), math.sin(math.radians(30)))
    check("m_to_px 30deg: (10,0) m -> along the diagonal",
          m_to_px((10.0, 0.0), 2.0, rot_for(u30), ORIGIN),
          (ORIGIN[0] + 20 * u30[0], ORIGIN[1] + 20 * u30[1]))
    group("round trips px<->m, plus m_to_px direction", n0, b0)

    # 5. make_canonical end to end: reef in the sea is at +y (offshore) ---------------
    n0, b0 = state["n"], len(state["bad"])
    # reef rectangle (metres): 20 m alongshore x 30 m cross-shore, its near edge 10 m
    # from the shoreline (alongshore 5..25, offshore 10..40). Shoreline passes through
    # the origin along u; the sea is on the offshore side n; land is on the other side.
    reef_m = [(5.0, 10.0), (25.0, 10.0), (25.0, 40.0), (5.0, 40.0)]
    land_pt_m = (0.0, -15.0)  # a point on land
    ppm = 3.0

    def scene(d, compass):
        u = unit(d)
        nrm = (-u[1], u[0])

        def to_px(m):
            return [ORIGIN[0] + (m[0] * u[0] + m[1] * nrm[0]) * ppm,
                    ORIGIN[1] + (m[0] * u[1] + m[1] * nrm[1]) * ppm]

        shape = {"slug": "selftest", "sources": [{
            "id": "img1", "scale": {"px_per_m": ppm},
            "pixel_polygons": [[to_px(m) for m in reef_m]]}]}

        def run(tmp):
            sp = tmp / "shape.json"
            sp.write_text(json.dumps(shape), encoding="utf-8")
            res = make_canonical(sp, "img1", ORIGIN, d, compass, write=True)
            written = json.loads(sp.read_text(encoding="utf-8"))["canonical"]
            return res, written, to_px(land_pt_m)
        return with_shape(run)

    for label, d, compass in (("(1,0)", (1, 0), 90.0), ("(0,1)", (0, 1), 180.0),
                              ("(-1,0)", (-1, 0), 270.0),
                              ("30deg diag", (math.cos(math.radians(30)), math.sin(math.radians(30))), 120.0),
                              ("tilt (0.9934,-0.1157)", (0.9934, -0.1157), 83.4)):
        res, written, land_px = scene(d, compass)
        got_poly = res["polygons_m"][0]
        for i, (g, w) in enumerate(zip(got_poly, reef_m)):
            check(f"make_canonical {label}: vertex {i} recovered", g, w, 1e-8)
        check(f"make_canonical {label}: all reef y > 0 (offshore)",
              (1.0 if min(p[1] for p in got_poly) > 0 else 0.0,), (1.0,))
        check(f"make_canonical {label}: area/bbox/offshore",
              (res["area_m2"], res["bbox_m"]["alongshore"], res["bbox_m"]["crossshore"],
               res["distance_offshore_m"], res["max_dim_m"]),
              (600.0, 20.0, 30.0, 40.0, math.hypot(20, 30)), 1e-8)
        check(f"make_canonical {label}: shore_normal_bearing_deg",
              (res["shore_normal_bearing_deg"],), ((compass + 90.0) % 360.0,))
        check(f"make_canonical {label}: file written == returned",
              (1.0 if written == json.loads(json.dumps(res)) else 0.0,), (1.0,))
        # a land-side pixel must land at negative y (the shore-side of the origin)
        back = px_to_m(land_px, ppm, rot_for(d), ORIGIN)
        check(f"make_canonical {label}: land side is -y", back, land_pt_m, 1e-8)
    # wrong-way alongshore (sea on the other side of the line) -> mirrored: y < 0.
    flipped = with_shape(lambda tmp: _flip_case(tmp, ppm, reef_m))
    check("sea on the 'wrong' side of alongshore (1,0): y<0 (caller must reverse the dir)",
          (1.0 if flipped < 0 else 0.0,), (1.0,))
    group("make_canonical end to end (+y = offshore, 5 directions)", n0, b0)

    # 6. fit_similarity uses the same kind of rotation: recover a known one -------------
    n0, b0 = state["n"], len(state["bad"])
    th = math.radians(30.0)
    srcp = [(0.0, 0.0), (10.0, 0.0), (0.0, 10.0), (7.0, 4.0)]
    dstp = [(2.0 * (math.cos(th) * x - math.sin(th) * y) + 5.0,
             2.0 * (math.sin(th) * x + math.cos(th) * y) - 3.0) for x, y in srcp]
    fit = fit_similarity([[list(s), list(d)] for s, d in zip(srcp, dstp)])
    check("fit_similarity recovers scale/rotation/translation/rms",
          (fit["scale"], fit["rotation_deg"], fit["translation"][0], fit["translation"][1], fit["rms_residual"]),
          (2.0, 30.0, 5.0, -3.0, 0.0), 1e-9)
    group("fit_similarity known 30 deg rotation", n0, b0)

    ok = not state["bad"]
    print(f"selftest: {state['n']} checks, {len(state['bad'])} failed -> {'PASS' if ok else 'FAIL'}")
    return ok


def _flip_case(tmp, ppm, reef_m):
    """helper for selftest(): reef placed on the side of the shoreline that is NOT the
    documented offshore side for alongshore (1,0) (i.e. image UP). Returns its min y_m."""
    ox, oy = 200.0, 300.0
    poly = [[ox + m[0] * ppm, oy - m[1] * ppm] for m in reef_m]  # sea above the line
    sp = tmp / "shape.json"
    sp.write_text(json.dumps({"sources": [{"id": "img1", "scale": {"px_per_m": ppm},
                                           "pixel_polygons": [poly]}]}), encoding="utf-8")
    res = make_canonical(sp, "img1", (ox, oy), (1, 0), None, write=False)
    return max(p[1] for p in res["polygons_m"][0])


# --------------------------------------------------------------------------- #
# CLI plumbing
# --------------------------------------------------------------------------- #

def _load_polys(arg):
    """arg is either a path to a JSON file or a literal JSON string: list of polygons,
    each a list of [x,y]."""
    p = Path(arg)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return json.loads(arg)


def _parse_xy(s):
    parts = s.split(",")
    return (float(parts[0]), float(parts[1]))


def main():
    ap = argparse.ArgumentParser(prog="geom.py", description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("area", help="shoelace area of each polygon + total")
    p.add_argument("--polys", required=True)

    p = sub.add_parser("bbox", help="bounding box over all points in all polygons")
    p.add_argument("--polys", required=True)

    p = sub.add_parser("centroid", help="area-weighted centroid of each polygon")
    p.add_argument("--polys", required=True)

    p = sub.add_parser("maxdim", help="largest pairwise vertex distance over all points")
    p.add_argument("--polys", required=True)

    rot_help = ("rotation applied to the pixel offset (dx,dy) by the plain matrix [[c,-s],[s,c]]; "
                "to put an alongshore pixel vector (adx,ady) on +x use -atan2(ady,adx) in degrees "
                "(sign convention fixed 2026-10-05; 0 = image x axis is already alongshore)")

    p = sub.add_parser("px2m", help="pixel point -> canonical metres")
    p.add_argument("--point", required=True, help="x,y in pixels")
    p.add_argument("--px-per-m", required=True, type=float)
    p.add_argument("--rotation-deg", required=True, type=float, help=rot_help)
    p.add_argument("--origin-px", required=True, help="x,y in pixels")

    p = sub.add_parser("m2px", help="canonical metres point -> pixel")
    p.add_argument("--point", required=True, help="x,y in metres")
    p.add_argument("--px-per-m", required=True, type=float)
    p.add_argument("--rotation-deg", required=True, type=float, help=rot_help)
    p.add_argument("--origin-px", required=True, help="x,y in pixels")

    p = sub.add_parser("latlon2local", help="lat/lon -> local equirectangular metres")
    p.add_argument("--lat", required=True, type=float)
    p.add_argument("--lon", required=True, type=float)
    p.add_argument("--anchor-lat", required=True, type=float)
    p.add_argument("--anchor-lon", required=True, type=float)

    p = sub.add_parser("local2latlon", help="local equirectangular metres -> lat/lon")
    p.add_argument("--x", required=True, type=float)
    p.add_argument("--y", required=True, type=float)
    p.add_argument("--anchor-lat", required=True, type=float)
    p.add_argument("--anchor-lon", required=True, type=float)

    p = sub.add_parser("bearings-latlon", help="great-circle bearing of each edge of a [lat,lon] polygon")
    p.add_argument("--polys", required=True, help="one polygon: [[lat,lon], ...] (or a list of such polygons)")

    p = sub.add_parser("bearings-xy", help="compass bearing of each edge of an xy polygon")
    p.add_argument("--polys", required=True)
    p.add_argument("--north-deg", type=float, default=0.0)

    p = sub.add_parser("angle-to-shore", help="angle (0-90) between a bearing and the shoreline bearing")
    p.add_argument("--bearing-deg", required=True, type=float)
    p.add_argument("--shoreline-bearing-deg", required=True, type=float)

    p = sub.add_parser("fit-similarity", help="least-squares similarity transform from control pairs")
    p.add_argument("--pairs", required=True, help="JSON file or string: [[[sx,sy],[dx,dy]], ...]")

    p = sub.add_parser("make-canonical", help="fill shape.json's canonical block from one source")
    p.add_argument("--shape", required=True, help="path to shape.json")
    p.add_argument("--source-id", required=True)
    p.add_argument("--origin-px", required=True, help="x,y in pixels")
    p.add_argument("--alongshore-dir-px", required=True, help="dx,dy in pixels (direction, not a point)")
    p.add_argument("--alongshore-compass-deg", type=float, default=None)
    p.add_argument("--no-write", action="store_true", help="print result, don't modify shape.json")

    sub.add_parser("selftest", help="check px<->m rotation conventions and make-canonical "
                                    "(exit code 0 = pass, 1 = fail)")

    args = ap.parse_args()

    if args.cmd == "area":
        polys = _load_polys(args.polys)
        areas = [shoelace_area(p) for p in polys]
        print(json.dumps({"areas_m2_or_px2": areas, "total": sum(areas)}, indent=2))

    elif args.cmd == "bbox":
        polys = _load_polys(args.polys)
        pts = [pt for poly in polys for pt in poly]
        print(json.dumps(bbox(pts), indent=2))

    elif args.cmd == "centroid":
        polys = _load_polys(args.polys)
        print(json.dumps([list(centroid(p)) for p in polys], indent=2))

    elif args.cmd == "maxdim":
        polys = _load_polys(args.polys)
        pts = [pt for poly in polys for pt in poly]
        d, pair = max_dimension(pts)
        print(json.dumps({"max_dim": d, "vertex_indices": pair}, indent=2))

    elif args.cmd == "px2m":
        pt = _parse_xy(args.point)
        origin = _parse_xy(args.origin_px)
        result = px_to_m(pt, args.px_per_m, args.rotation_deg, origin)
        print(json.dumps({"x_m": result[0], "y_m": result[1]}, indent=2))

    elif args.cmd == "m2px":
        pt = _parse_xy(args.point)
        origin = _parse_xy(args.origin_px)
        result = m_to_px(pt, args.px_per_m, args.rotation_deg, origin)
        print(json.dumps({"x_px": result[0], "y_px": result[1]}, indent=2))

    elif args.cmd == "latlon2local":
        x, y = latlon_to_local_m(args.lat, args.lon, args.anchor_lat, args.anchor_lon)
        print(json.dumps({"x_m": x, "y_m": y}, indent=2))

    elif args.cmd == "local2latlon":
        lat, lon = local_m_to_latlon(args.x, args.y, args.anchor_lat, args.anchor_lon)
        print(json.dumps({"lat": lat, "lon": lon}, indent=2))

    elif args.cmd == "bearings-latlon":
        data = _load_polys(args.polys)
        # accept either one polygon [[lat,lon],...] or a list of polygons
        if data and isinstance(data[0][0], (int, float)):
            data = [data]
        out = [edge_bearings_latlon(poly) for poly in data]
        print(json.dumps(out, indent=2))

    elif args.cmd == "bearings-xy":
        polys = _load_polys(args.polys)
        out = [edge_bearings_xy(poly, args.north_deg) for poly in polys]
        print(json.dumps(out, indent=2))

    elif args.cmd == "angle-to-shore":
        print(json.dumps({"angle_deg": angle_to_shoreline(args.bearing_deg, args.shoreline_bearing_deg)}, indent=2))

    elif args.cmd == "fit-similarity":
        pairs_arg = Path(args.pairs)
        pairs = json.loads(pairs_arg.read_text(encoding="utf-8")) if pairs_arg.exists() else json.loads(args.pairs)
        print(json.dumps(fit_similarity(pairs), indent=2))

    elif args.cmd == "make-canonical":
        origin = _parse_xy(args.origin_px)
        direction = _parse_xy(args.alongshore_dir_px)
        result = make_canonical(args.shape, args.source_id, origin, direction,
                                 args.alongshore_compass_deg, write=not args.no_write)
        print(json.dumps(result, indent=2))

    elif args.cmd == "selftest":
        sys.exit(0 if selftest() else 1)

    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

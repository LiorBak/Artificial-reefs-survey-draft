"""b3d_lib.py - shared helpers of the Borth 3D build (frame, grids, seabed, reef surfaces).
Part of 07_scale/shapes/borth-coastal-defence-reef/3d/ ; used by build_3d.py.  Written 2026-10-06 (3D agent).

Frame: shape.json canonical frame = metres, +x SOUTH (179.57 deg), +y OFFSHORE/WEST (269.57 deg),
origin on the defence line (bearing 359.57 deg).  Height z in mODN inside the lib; the model.js writer converts to MSL
(z_MSL = z_ODN - ZOFF with ZOFF = 0.31).
BNG (EPSG:27700) -> canonical: pyproj Helmert EPSG:27700 -> 4326, local tangent metres about (52.4832,-4.0562),
frame (org, d, n) re-derived exactly as scripts_verify/adds.py did for shape.json alt_outlines_m; a 2-D affine fit over
the reef window reproduces that chain to < 0.01 m (checked in build_3d.py).
"""
import json, math, os
import numpy as np
from pyproj import Transformer
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)            # .../borth-coastal-defence-reef
SRC = os.path.join(HERE, 'src')
ZOFF = 0.31                              # z_MSL = z_ODN - ZOFF  (MSL = +0.31 mODN, +-0.15)
LAT0, LON0 = 52.4832, -4.0562
R_E = 6378137.0


# --------------------------------------------------------------------------------------------- frame
def _merc(lat, lon):
    return R_E * math.radians(lon), R_E * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def _imerc(x, y):
    return math.degrees(2 * math.atan(math.exp(y / R_E)) - math.pi / 2), math.degrees(x / R_E)


def _pix2ll(g, x, y):
    b = g['bounds']; w, h = g['width'], g['height']
    xw, yn = _merc(b['north'], b['west']); xe, ys = _merc(b['south'], b['east'])
    return _imerc(xw + x / w * (xe - xw), yn + y / h * (ys - yn))


def _loc(lat, lon):
    return np.array([math.radians(lon - LON0) * R_E * math.cos(math.radians(LAT0)), math.radians(lat - LAT0) * R_E])


def frame_params(shape):
    """org, d, n of the canonical frame (local tangent metres) - same recipe as scripts_verify/adds.py."""
    from shapely.geometry import Polygon
    g24 = json.load(open(os.path.join(BASE, 'src', 'borth_esri_2024-09-17_z19.png.geo.json')))
    gsh = json.load(open(os.path.join(BASE, 'src', 'borth_shoreline_z19.png.geo.json')))
    pts = [(1795, 1100), (1800, 1500), (1803, 2000), (1805, 2500), (1808, 2600)]   # defence-line pixels (VERIFY check 1)
    E = np.array([_loc(*_pix2ll(gsh, *p)) for p in pts]); c = E.mean(0)
    d = np.linalg.svd(E - c)[2][0]
    if d[1] < 0: d = -d
    n = np.array([-d[1], d[0]])
    polys = shape['sources'][0]['pixel_polygons']
    P = [np.array([_loc(*_pix2ll(g24, x, y)) for x, y in p]) for p in polys]
    cens = [Polygon(p).centroid.coords[0] for p in P]; ar = [Polygon(p).area for p in P]
    cen = (np.array(cens[0]) * ar[0] + np.array(cens[1]) * ar[1]) / sum(ar)
    org = c + np.dot(cen - c, d) * d
    return org, d, n


class Frame:
    """BNG <-> canonical. Affine fitted to the exact chain over a 600 x 600 m window."""
    def __init__(self, shape):
        org, d, n = frame_params(shape)
        tf = Transformer.from_crs('EPSG:27700', 'EPSG:4326', always_xy=True)
        Es = np.linspace(260300, 260900, 13); Ns = np.linspace(289000, 289500, 11)
        src, dst = [], []
        for e in Es:
            for nn in Ns:
                lon, lat = tf.transform(e, nn); rel = _loc(lat, lon) - org
                src.append([e, nn, 1.0]); dst.append([-(rel @ d), rel @ n])
        src = np.array(src); dst = np.array(dst)
        self.A, *_ = np.linalg.lstsq(src, dst, rcond=None)      # (3,2)
        self.fit_rms = float(np.sqrt(np.mean((src @ self.A - dst) ** 2)))
        self.fit_max = float(np.abs(src @ self.A - dst).max())
        M = self.A[:2].T                                       # [x,y] = M @ [E,N] + t
        self.M = M; self.t = self.A[2]
        self.Minv = np.linalg.inv(M)
        self.org_local = org; self.d = d; self.n = n
        # rotation angle of canonical axes relative to BNG axes (for information)
        self.rot_deg = math.degrees(math.atan2(M[1, 0], M[0, 0]))

    def bng2can(self, en):
        en = np.asarray(en, float)
        return en @ self.M.T + self.t

    def can2bng(self, xy):
        xy = np.asarray(xy, float)
        return (xy - self.t) @ self.Minv.T


# --------------------------------------------------------------------------------------------- grids
def bilinear(grid, x0, y0, step, X, Y, fill=np.nan):
    """Bilinear sample of grid[iy,ix] (x = x0 + ix*step, y = y0 + iy*step) at X,Y (arrays)."""
    fx = (np.asarray(X) - x0) / step; fy = (np.asarray(Y) - y0) / step
    return ndi.map_coordinates(grid, [fy, fx], order=1, mode='nearest', cval=fill)


def lidar_sampler(frame, npz_path, which='dsm'):
    """Return f(X,Y)-> LiDAR z (mODN) at canonical points, NaN where the cell has no return (sea)."""
    d = np.load(npz_path)
    G = d[which].astype(float); E0 = float(d['E0']); N1 = float(d['N1'])
    G[G < -9000] = np.nan
    def f(X, Y):
        en = frame.can2bng(np.c_[np.ravel(X), np.ravel(Y)])
        c = en[:, 0] - E0 - 0.5; r = N1 - en[:, 1] - 0.5          # cell-centre indices
        # nearest-valid bilinear: do bilinear on NaN-filled values with weights
        Gz = np.where(np.isnan(G), 0.0, G); Wv = (~np.isnan(G)).astype(float)
        a = ndi.map_coordinates(Gz, [r, c], order=1, mode='nearest')
        w = ndi.map_coordinates(Wv, [r, c], order=1, mode='nearest')
        out = np.where(w > 0.999, a / np.maximum(w, 1e-9), np.nan)
        return out.reshape(np.shape(X))
    return f


# --------------------------------------------------------------------------------------------- seabed
from scipy.interpolate import RBFInterpolator
from shapely.geometry import Polygon, Point, LineString, MultiPoint
from shapely.ops import unary_union

# seabed grid (canonical metres)
SB_X0, SB_X1, SB_Y0, SB_Y1, SB_STEP = -200.0, 260.0, 0.0, 520.0, 5.0
ANCHOR_Y = 335.0          # offshore of this the EMODnet gradient is used (orchestrator decision 2026-10-06)
EMODNET_GRAD = 0.011      # -1.1 % (REPORT.md 5.4 / 9.2: cells y 368-652 m)
DESIGN_BED_ARM = -4.0     # mODN, drawings 1021 N3 (-4.01), N4 about -3.8
DESIGN_BED_OVAL = (-3.6, -4.2)   # mODN, note on drawing 1023 S2 (shoreward .. seaward)


def seabed_nodes(frame, shape, beach_npz, fig2_json, exposed_union, arm_axis=((-60.8, 268.8), (-9.9, 380.8))):
    """Control nodes (x, y, z_ODN, weight-class, source).  Returns list of dict."""
    nodes = []
    b = np.load(beach_npz); G = b['dtm'].astype(float); G[G < -9000] = np.nan
    E0 = float(b['E0']); N1 = float(b['N1'])
    # (A) LiDAR DTM, beach: sample on a 6 m canonical grid, y 0..255, skip reef rock (buffer 12 m) and invalid
    xs = np.arange(-200, 261, 6.0); ys = np.arange(0, 256, 6.0)
    X, Y = np.meshgrid(xs, ys)
    en = frame.can2bng(np.c_[X.ravel(), Y.ravel()])
    c = en[:, 0] - E0 - 0.5; r = N1 - en[:, 1] - 0.5
    Gz = np.where(np.isnan(G), 0.0, G); Wv = (~np.isnan(G)).astype(float)
    a = ndi.map_coordinates(Gz, [r, c], order=1, mode='nearest'); w = ndi.map_coordinates(Wv, [r, c], order=1, mode='nearest')
    z = np.where(w > 0.999, a / np.maximum(w, 1e-9), np.nan)
    ok = ~np.isnan(z)
    pts = np.c_[X.ravel(), Y.ravel()]
    buf = exposed_union.buffer(12.0)
    for (x, y), zz, o in zip(pts, z, ok):
        if not o or zz < -2.35: continue
        if buf.contains(Point(x, y)): continue
        nodes.append(dict(x=float(x), y=float(y), z=float(zz), src='lidar_dtm_2022'))
    # (B) Fig 2 -3.0 contour, outside the reef zone
    f2 = json.load(open(fig2_json))['contours_mODN']
    for x, y in f2['-3'][::2]:
        if -200 <= x <= 260 and not (-115 <= x <= 160):
            nodes.append(dict(x=x, y=y, z=-3.0, src='fig2_-3.0'))
    # (C) design bed levels under the reefs (METHODS A5..A7): arm axis from the tail mid-point to the head mid-point
    (tx, ty), (hx, hy) = arm_axis
    def on_axis(y):
        return tx + (y - ty) * (hx - tx) / (hy - ty)
    for y, zz, src in ((272, -3.0, 'assumed_tail'), (282, -3.4, 'assumed_tail'), (292, -3.8, 'design_N4'),
                       (310, DESIGN_BED_ARM, 'design_N3_arm'), (335, DESIGN_BED_ARM, 'design_N3_arm'),
                       (360, DESIGN_BED_ARM, 'design_N3_arm'), (385, DESIGN_BED_ARM, 'design_N3_arm')):
        for dx in (-8.0, 0.0, 8.0):
            nodes.append(dict(x=float(on_axis(y) + dx), y=float(y), z=zz, src=src))
    for x in (49, 70, 85, 100, 121):
        nodes.append(dict(x=float(x), y=309.0, z=DESIGN_BED_OVAL[0], src='design_S2_shoreward'))
        nodes.append(dict(x=float(x), y=340.0, z=DESIGN_BED_OVAL[1], src='design_S2_seaward'))
    # (D) anchor line at y=ANCHOR_Y alongshore: design bed level
    for x in range(-200, 261, 40):
        if -80 <= x <= 130: continue
        nodes.append(dict(x=float(x), y=ANCHOR_Y, z=-4.0, src='anchor_335'))
    return nodes


def seabed_grid(nodes, step=SB_STEP):
    xs = np.arange(SB_X0, SB_X1 + 1e-6, step); ys = np.arange(SB_Y0, SB_Y1 + 1e-6, step)
    P = np.array([[n['x'], n['y']] for n in nodes]); V = np.array([n['z'] for n in nodes])
    rbf = RBFInterpolator(P, V, kernel='thin_plate_spline', smoothing=0.5, neighbors=80)
    X, Y = np.meshgrid(xs, ys)
    Yc = np.minimum(Y, ANCHOR_Y)
    Z = rbf(np.c_[X.ravel(), Yc.ravel()]).reshape(X.shape)
    # beyond the anchor: EMODnet gradient
    Z = np.where(Y > ANCHOR_Y, Z - EMODNET_GRAD * (Y - ANCHOR_Y), Z)
    return xs, ys, Z, rbf

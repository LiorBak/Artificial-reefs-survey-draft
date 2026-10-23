"""cables-reef-wa 3D: design-surface and bed construction on a 0.5 m raster in the canonical frame (x north, y offshore/west, metres).
All heights here are RL (design datum, m; negative = below). Conversion to MSL is done in build_3d.py (A: z_MSL = RL - 0.78, or B: z_MSL = RL)."""
import json, numpy as np
from scipy import ndimage as ndi
from scipy import sparse
from scipy.sparse.linalg import spsolve
from shapely.geometry import Polygon
from skimage.draw import polygon as skpoly
HERE = __file__.rsplit('/', 1)[0]
SH = json.load(open(HERE + '/../shape.json'))
CO = json.load(open(HERE + '/../scripts/computed.json'))
STEP = 0.5
X0, X1, Y0, Y1 = -75.0, 75.0, 205.0, 335.0          # raster window (m), covers the footprint + the extension
nx, ny = int((X1 - X0) / STEP) + 1, int((Y1 - Y0) / STEP) + 1
def raster(poly_m):
    P = np.array(poly_m); m = np.zeros((ny, nx), bool)
    rr, cc = skpoly((P[:, 1] - Y0) / STEP, (P[:, 0] - X0) / STEP, m.shape); m[rr, cc] = True; return m
def build(version_polys_m, ramp_m, setout_class_fn=None, bed_gradient=1/30., bed_level_at_ref=None, y_ref=300.0, side='linear'):
    """returns dict of rasters: sil, ramp, z_ramp (RL), z_surf (RL), z_bed (RL), t (thickness)"""
    sil = np.zeros((ny, nx), bool)
    for p in version_polys_m: sil |= raster(p)
    ramp = raster(ramp_m) & sil
    return sil, ramp

def sil_chain_points(sil_m):
    """densified outline points with chain class: 'outer' (P2 -> apex -> P6), 'inner' (P7 -> inner apex -> P1), 'end' (P1-P2, P6-P7).
    vertex index ranges refer to the 111-vertex A2 silhouette in scripts/a2_trace.json (checked on the overlay)."""
    P = np.array(sil_m); n = len(P); pts, cls = [], []
    def klass(i):
        if 12 <= i <= 72: return 'outer'
        if 78 <= i <= 108: return 'inner'
        return 'end'
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]; k = klass(i)
        L = np.hypot(*(b - a)); m = max(2, int(L / 0.25))
        for t in np.linspace(0, 1, m, endpoint=False): pts.append(a + (b - a) * t); cls.append(k)
    return np.array(pts), np.array(cls)

def ramp_solution(sil_orig_m, ramp_m):
    """harmonic design surface z_RL on the ramp: -3.0 on the outer (set-out) edge, -1.0 on the inner (crest) edge, natural Neumann at the ends"""
    from scipy.spatial import cKDTree
    ramp = raster(ramp_m)
    pts, cls = sil_chain_points(sil_orig_m); tree = cKDTree(pts)
    er = ndi.binary_erosion(ramp); bd = ramp & ~er
    jj, ii = np.where(bd); xy = np.c_[X0 + ii * STEP, Y0 + jj * STEP]
    dist, idx = tree.query(xy); k = cls[idx]
    fixed = np.full(ramp.shape, np.nan)
    for (j, i), kk, d in zip(zip(jj, ii), k, dist):
        if kk == 'outer': fixed[j, i] = -3.0
        elif kk == 'inner': fixed[j, i] = -1.0
    # unknowns: all ramp pixels without a fixed value
    idmap = -np.ones(ramp.shape, int); unk = ramp & np.isnan(fixed); idmap[unk] = np.arange(unk.sum())
    N = unk.sum(); rows, cols, vals, rhs = [], [], [], np.zeros(N)
    for (j, i) in zip(*np.where(unk)):
        r = idmap[j, i]; nb = 0; b = 0.0
        for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            jn, in_ = j + dj, i + di
            if not (0 <= jn < ny and 0 <= in_ < nx) or not ramp[jn, in_]: continue
            nb += 1
            if idmap[jn, in_] >= 0: rows.append(r); cols.append(idmap[jn, in_]); vals.append(-1.0)
            else: b += fixed[jn, in_]
        rows.append(r); cols.append(r); vals.append(float(nb)); rhs[r] = b
    A = sparse.csr_matrix((vals, (rows, cols)), shape=(N, N)); u = spsolve(A, rhs)
    z = np.full(ramp.shape, np.nan); z[ramp] = np.where(np.isnan(fixed[ramp]), 0, fixed[ramp]); z[unk] = u
    # Neumann-end boundary pixels (ramp edge, neither fixed nor unknown?) are unknowns above, so z is complete on the ramp
    return ramp, z, fixed


def ramp_distance_surface(sil_orig_m, ramp_m, smooth=1.5):
    """alternative design surface: z = -3 + 2 d_out/(d_out + d_in), d = Euclidean distance to the outer (set-out) / inner (crest) edge pixels of the ramp"""
    from scipy.spatial import cKDTree
    if smooth:
        P = Polygon(ramp_m).buffer(smooth, join_style=1).buffer(-2 * smooth, join_style=1).buffer(smooth, join_style=1)   # open-close: removes label notches / pixel jaggedness
        if P.geom_type != 'Polygon': P = max(P.geoms, key=lambda g: g.area)
        ramp_m = [list(c) for c in P.exterior.coords][:-1]
    ramp = raster(ramp_m); pts, cls = sil_chain_points(sil_orig_m); tree = cKDTree(pts)
    bd = ramp & ~ndi.binary_erosion(ramp); jj, ii = np.where(bd); xy = np.c_[X0 + ii * STEP, Y0 + jj * STEP]
    _, idx = tree.query(xy); k = cls[idx]
    out_m = np.zeros(ramp.shape, bool); in_m = np.zeros(ramp.shape, bool)
    for (j, i), kk in zip(zip(jj, ii), k):
        if kk == 'outer': out_m[j, i] = True
        elif kk == 'inner': in_m[j, i] = True
    d_out = ndi.distance_transform_edt(~out_m) * STEP; d_in = ndi.distance_transform_edt(~in_m) * STEP
    z = np.where(ramp, -3.0 + 2.0 * d_out / np.maximum(d_out + d_in, 1e-9), np.nan)
    return ramp, z, out_m, in_m

def surfaces(sil_mask, ramp, z_ramp, bed_fn, ext_mask=None, ext_volume=None, smooth_px=2.0):
    """full reef surface z_RL on the footprint raster: ramp = design surface; band (footprint minus ramp) = linear from the ramp-edge level to the bed at the footprint edge."""
    yy = Y0 + np.arange(ny)[:, None] * STEP * np.ones((1, nx)); xx = X0 + np.arange(nx)[None, :] * STEP * np.ones((ny, 1))
    bed = bed_fn(xx, yy)
    band = sil_mask & ~ramp
    d1, (jj, ii) = ndi.distance_transform_edt(~ramp, return_indices=True)           # distance to the ramp, index of nearest ramp pixel
    d2 = ndi.distance_transform_edt(sil_mask)                                       # distance to the footprint edge (inside)
    zedge = z_ramp[jj, ii]
    frac = (d1 * STEP) / np.maximum(d1 * STEP + d2 * STEP, 1e-9)
    zb = zedge * (1 - frac) + bed * frac
    surf = np.where(ramp, z_ramp, np.where(band, zb, np.nan))
    if ext_mask is not None and ext_mask.any():              # extension fill: footprint + stated volume known only; pyramid-like thickness k * distance to the edge, k from the volume
        de = ndi.distance_transform_edt(sil_mask) * STEP
        k = ext_volume / float(np.sum(de[ext_mask]) * STEP * STEP)
        surf = np.where(ext_mask, bed + k * de, surf)
    surf = np.where(sil_mask, np.maximum(surf, bed), np.nan)
    if smooth_px:                                            # remove raster jaggedness (nearest-pixel edge levels): normalised Gaussian inside the footprint, sigma 1 m
        w = ndi.gaussian_filter(sil_mask.astype(float), smooth_px); v = ndi.gaussian_filter(np.where(sil_mask, surf, 0.0), smooth_px)
        surf = np.where(sil_mask, np.maximum(v / np.maximum(w, 1e-9), bed), np.nan)
    return xx, yy, bed, surf, band
def volume(surf, bed):
    t = np.where(np.isfinite(surf), surf - bed, 0.0); return float(np.nansum(t) * STEP * STEP), t

def transect_crossings(z, p0, p1, levels=(-2.5, -2.0, -1.5)):
    """distances (m) from p0 (A2 px) along the transect p0->p1 at which the modelled ramp surface crosses the given RL levels"""
    s = CO['scale_px_per_m']; uc, vc = CO['centroid_px_asbuilt']; n = 800
    us = np.linspace(p0[0], p1[0], n); vs = np.linspace(p0[1], p1[1], n); Ln = np.hypot(p1[0] - p0[0], p1[1] - p0[1]) / s
    zz = []
    for u, v in zip(us, vs):
        x = (u - uc) / s; y = 270 + (vc - v) / s; j = int(round((y - Y0) / STEP)); i = int(round((x - X0) / STEP)); zz.append(z[j, i])
    zz = np.array(zz); out = []
    for lv in levels:
        k = np.where((zz[:-1] - lv) * (zz[1:] - lv) <= 0)[0]; out.append(round(float(k[0] / n * Ln), 1) if len(k) else None)
    return out
DRAWN_TRANSECT_CROSSINGS = {"left_26.0m": {"p": [(257, 360), (355, 500)], "drawn_m_from_outer_end": [6.6, 13.2, 19.9]}, "right_30.0m": {"p": [(767, 268), (652, 425)], "drawn_m_from_outer_end": [6.9, 14.2, 21.5]}}

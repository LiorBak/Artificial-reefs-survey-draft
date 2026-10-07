"""b3d_reef.py - reef surfaces of the three outline versions (heightfields on a 1 m canonical grid, z in mODN).
2026-10-06, 3D agent.  Used by build_3d.py.  All design numbers: Royal Haskoning drawings 9V5090/1020-1023 rev C1 (see SOURCES_3D.md)."""
import json, os, numpy as np, shapely
from shapely.geometry import Polygon, LineString, Point
from scipy import ndimage as ndi
import b3d_lib as L

# window of the fine reef grid (canonical m)
WX0, WX1, WY0, WY1, WSTEP = -105.0, 150.0, 235.0, 420.0, 1.0
# design constants (drawing 1021/1022/1023 sections; all mODN unless stated)
CREST_ARM, CREST_TAIL, CREST_HEAD_EDGE, CREST_OVAL = 0.50, 1.00, 0.00, 1.50
Z_FOOT = -2.15        # top of the toe berm = foot of the Type 4 armour slope (seabed -4.0 + blanket 0.5 + berm 1.35)
BLANKET, BERM_H = 0.50, 1.35
TOE_SLOPE = 1.5       # H:V of toe berm and blanket edge
APRON = 2.0           # m, flat blanket in front of the berm
RAMP_HEAD, RAMP_TAIL = 40.0, 15.0     # TRANSITION APPROX. 40m (R1 to +0.50) and 15m (R2 to +1.00)
RHO_BULK = 1.7        # t/m3 placed-rock bulk density, assumption A8 (2.65 t/m3 solid, about 36 % voids); range 1.6-1.8


def grid():
    xs = np.arange(WX0, WX1 + 1e-6, WSTEP); ys = np.arange(WY0, WY1 + 1e-6, WSTEP)
    X, Y = np.meshgrid(xs, ys)
    return xs, ys, X, Y


def seabed_at(sb, X, Y):
    xs, ys, Z = sb
    return L.bilinear(Z, xs[0], ys[0], xs[1] - xs[0], X, Y)


SOP = {'R1': (260409.145, 289284.522), 'R2': (260501.860, 289331.154), 'R3': (260528.445, 289332.669),
       'R4': (260527.416, 289323.700), 'R5': (260503.909, 289322.361), 'R6': (260451.697, 289299.380),
       'R7': (260449.504, 289284.783), 'R10': (260424.002, 289276.269), 'R14': (260470.0, 289162.0), 'R15': (260470.0, 289200.0)}


def design_polys(frame, src=L.SRC):
    rings = json.load(open(os.path.join(src, 'design1020_rings_bng.json')))
    cp = json.load(open(os.path.join(src, 'design1020_crest_paths_bng.json')))['paths']
    out = {}
    for k in 'NS':
        out[k] = [Polygon(frame.bng2can(np.array(r))) for r in rings[k]]

    def P(i): return np.array(cp[i]['bng'], float)
    # N crest ring R1 -> R2 -> R3 -> R4 -> R5 -> R6 -> R1 (path ids from drawing 1020, see design1020_crest_paths_bng.json)
    seq = [P('588')[::-1], P('583')[::-1], P('584')[::-1], P('585'), P('586'), P('587')]
    crest_n = Polygon(frame.bng2can(np.vstack(seq))).buffer(0)
    S = {k: frame.bng2can(np.array([v]))[0] for k, v in SOP.items()}
    r6p = frame.bng2can(np.array([P('2030')[0]]))[0]       # R6' = end of the 40 m transition on the upper edge
    # oval crest: flat top 6 m wide, 38 m long between the ends R14 and R15
    a, b = S['R14'], S['R15']; u = (b - a) / np.linalg.norm(b - a)
    crest_s = LineString([a + 3 * u, b - 3 * u]).buffer(3.0)
    out.update(crest_N=crest_n, crest_S=crest_s, sop=S, r6p=r6p)
    mh = (S['R1'] + S['R10']) / 2; mt = (S['R3'] + S['R4']) / 2           # head and tail mid-points: ramp axis
    ax = (mt - mh) / np.linalg.norm(mt - mh)
    out['axis'] = (mh, ax)
    out['s'] = {k: float((S[k] - mh) @ ax) for k in ('R1', 'R2', 'R3', 'R10')}
    out['s']['R6p'] = float((r6p - mh) @ ax)
    return out


def crest_height_N(X, Y, dp):
    mh, ax = dp['axis']; s = (X - mh[0]) * ax[0] + (Y - mh[1]) * ax[1]
    s1 = dp['s']['R1']; s2 = dp['s']['R2']
    h = CREST_HEAD_EDGE + (CREST_ARM - CREST_HEAD_EDGE) * np.clip((s - s1) / RAMP_HEAD, 0, 1)
    h = np.where(s > s2, CREST_ARM + (CREST_TAIL - CREST_ARM) * np.clip((s - s2) / RAMP_TAIL, 0, 1), h)
    return h


def _dist(poly, pts):
    return shapely.distance(poly.exterior, pts)


def design_surface(X, Y, zs, dp):
    """Design (drawings 1020-1023) rock surface; H (mODN, NaN where no rock) and zone (0 none, 1 armour, 2 toe berm, 3 blanket)."""
    xr, yr = X.ravel(), Y.ravel(); pts = shapely.points(xr, yr)
    H = np.full(xr.shape, np.nan); Zn = np.zeros(xr.shape, np.uint8)
    zsr = zs.ravel()
    for reef, crest, hcf in (('N', dp['crest_N'], lambda x, y: crest_height_N(x, y, dp)),
                             ('S', dp['crest_S'], lambda x, y: np.full(np.shape(x), CREST_OVAL))):
        rg = dp[reef]
        ins = [shapely.contains_xy(r, xr, yr) for r in rg]
        d = [_dist(r, pts) for r in rg]
        zb = np.minimum(zsr + BLANKET, Z_FOOT)               # blanket top (cannot exceed the berm top)
        zlev = [zsr, zb, zb, np.full_like(zsr, Z_FOOT), np.full_like(zsr, Z_FOOT)]
        zone_of_band = [3, 3, 2, 2]
        for k in range(4):
            m = ins[k] & ~ins[k + 1]
            t = d[k] / np.maximum(d[k] + d[k + 1], 1e-9)
            H[m] = (zlev[k] + t * (zlev[k + 1] - zlev[k]))[m]; Zn[m] = zone_of_band[k]
        m4 = ins[4]
        incr = shapely.contains_xy(crest, xr, yr)
        dc = shapely.distance(crest.exterior, pts)
        hc = hcf(xr, yr)
        t = d[4] / np.maximum(d[4] + dc, 1e-9)
        z_arm = np.where(incr, hc, Z_FOOT + t * (hc - Z_FOOT))
        H[m4] = z_arm[m4]; Zn[m4] = 1
    H = H.reshape(X.shape); Zn = Zn.reshape(X.shape)
    H = np.where(np.isfinite(H), np.maximum(H, zs), np.nan)
    return H, Zn


def smooth_dsm(f, X, Y, sigma=0.8):
    """LiDAR DSM sampled on X,Y, filled and lightly smoothed (normalised Gaussian); also returns the raw sample."""
    z = f(X, Y)
    w = np.isfinite(z).astype(float); z0 = np.where(np.isfinite(z), z, 0.0)
    num = ndi.gaussian_filter(z0, sigma); den = ndi.gaussian_filter(w, sigma)
    out = np.where(den > 0.05, num / np.maximum(den, 1e-9), np.nan)
    return np.where(w > 0, out, np.nan), z


def outline_surface(X, Y, zs, dsm_s, polys, z_e):
    """Outline-driven surface: DSM (>= z_e) inside the outline polygon(s); design toe slopes outside
    (1:1.5 berm slope, 2 m flat apron, 1:1.5 blanket edge).  z_e = elevation of the outline edge (mODN)."""
    xr, yr = X.ravel(), Y.ravel(); pts = shapely.points(xr, yr)
    zsr = zs.ravel(); dsmr = dsm_s.ravel()
    H = np.full(xr.shape, np.nan); Zn = np.zeros(xr.shape, np.uint8)
    u = np.full(xr.shape, np.inf); ins = np.zeros(xr.shape, bool)
    for p in polys:
        ins |= shapely.contains_xy(p, xr, yr)
        u = np.minimum(u, shapely.distance(p, pts))
    zin = np.where(np.isfinite(dsmr), np.maximum(dsmr, z_e), z_e)
    H[ins] = zin[ins]; Zn[ins] = 1
    zb = np.minimum(zsr + BLANKET, z_e)
    u1 = TOE_SLOPE * np.maximum(z_e - zb, 0.0)
    u2 = u1 + APRON
    u3 = u2 + TOE_SLOPE * (zb - zsr)
    zout = np.where(u <= u1, z_e - u / TOE_SLOPE,
                    np.where(u <= u2, zb, np.where(u <= u3, zb - (u - u2) / TOE_SLOPE, zsr)))
    mo = (~ins) & (u <= u3)
    H[mo] = zout[mo]; Zn[mo] = np.where(u[mo] <= u1[mo], 2, 3)
    H = H.reshape(X.shape); Zn = Zn.reshape(X.shape)
    H = np.where(np.isfinite(H), np.maximum(H, zs), np.nan)
    return H, Zn


def volume(H, zs, step=WSTEP):
    d = np.where(np.isfinite(H), np.maximum(H - zs, 0.0), 0.0)
    return float(d.sum() * step * step)

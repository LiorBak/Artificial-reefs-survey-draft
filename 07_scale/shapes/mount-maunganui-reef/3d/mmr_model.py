"""mmr_model.py - the Mount Maunganui reef loft and seabed rules (2026-10-06).  Imported by build_3d.py; the JavaScript viewer (index.html) implements the SAME
rules on the grids that build_3d.py writes into model.js, so the numbers printed here and the live numbers in the viewer agree.

FRAME  canonical metres (shape.json): x alongshore toward true 316.15 (NW), y offshore toward 046.15 (NE), z up.  Elevations are kept in m CD (chart datum) here;
       the viewer / model.js use z_MSL = z_CD - 1.13 (present MSL = CD + 1.13, LINZ standard port Tauranga 2026-27).
SEABED S(y) (alongshore uniform)  = Pnav(y) + (bed - Pnav(YC)) * w(y)       [A5, A6]
         Pnav = Navionics SonarChart profile (nav_profile.py), dry beach y < 0 a schematic 1:15 ramp;  w = clamp((y - 111.2) / (YC - 111.2), 0, 1)
REEF (per outline version), cell (x, y) on a 0.5 m grid:
   inside the -2.0 m CD polygons:  z = ZC + r(d2) * (crest - ZC),  ZC = -2.0,  r = RISE(d2) / 1.10,  d2 = distance to the polygon edge   [A3, A4]
   survey version, outside:        z = max(S, ZC - dout / run),  dout = distance to the -2.0 region, run = 1 (H:V)                          [A7]
   toe version, between toe and the -2.0 region (U = toe + -2.0 union): z = S + (ZC - S) * t,  t = dT / (dT + dout),  dT = distance to the U edge inside U   [A8]
"""
import json, math, os, sys
import numpy as np
import shapely
from shapely.geometry import Polygon
from shapely.ops import unary_union
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mmr_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
MSL = L.MSL_ABOVE_CD                   # 1.13
MVD = L.MVD_ABOVE_CD                   # 0.9622
ZC = -2.0                              # CD, the survey contour
CREST_CD = -0.9                        # CD, crest decision (0.8-1.0 below CD)
# RISE above the -2.0 contour vs distance d2 inside it (2013 DEM statistics of the west block + south arm, crest -0.9; checkpoint 1, re-checked by build_3d.py)
RISE_D = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
RISE_Z = [0.0, 0.30, 0.50, 0.70, 0.85, 0.95, 1.05, 1.10]
RISE_MAX = 1.10
DX = 0.5
X0, X1, Y0, Y1 = -44.0, 41.0, 277.0, 351.0
BEDS = [-3.0, -3.5, -4.0, -4.5]        # CD at the reef centroid; plus 'nav' (the Navionics profile as it is)
BED_DEFAULT = -4.0
W_Y0 = 111.2


def load_profile():
    p = json.load(open(os.path.join(HERE, 'navionics_profile.json')))
    kn = [tuple(k) for k in p['profile_y_zCD']]
    return kn, p['z_cd_at_reef_centroid']


KNOTS, Z_NAV_REEF = load_profile()
SH, P2, PT = L.load_shape()
REGION = unary_union([Polygon(p) for p in P2]); TOE = unary_union([Polygon(p) for p in PT]); U = unary_union([REGION, TOE])
XC, YC = REGION.centroid.coords[0]


def pnav(y):
    y = np.asarray(y, float); ky = np.array([k[0] for k in KNOTS]); kz = np.array([k[1] for k in KNOTS])
    z = np.interp(y, ky, kz)
    z = np.where(y > ky[-1], kz[-1] + (y - ky[-1]) * (kz[-1] - kz[-2]) / (ky[-1] - ky[-2]), z)          # last slope continued
    return np.where(y < 0, MSL - y / 15.0, z)                                                          # schematic dry beach


def bed_z(y, bed):
    """seabed elevation (m CD) at offshore distance y for a reef-centroid bed level `bed` (None = the Navionics profile as it is)"""
    y = np.asarray(y, float); base = pnav(y)
    if bed is None: return base
    w = np.clip((y - W_Y0) / (YC - W_Y0), 0, 1)
    return base + (bed - float(pnav(YC))) * w


def rise(d2):
    return np.interp(d2, RISE_D, RISE_Z)


def make_grid():
    xs = np.arange(X0, X1 + 1e-9, DX); ys = np.arange(Y0, Y1 + 1e-9, DX)
    XX, YY = np.meshgrid(xs, ys); pts = shapely.points(XX.ravel(), YY.ravel())
    inreg = shapely.contains_xy(REGION, XX.ravel(), YY.ravel()); inU = shapely.contains_xy(U, XX.ravel(), YY.ravel())
    d_edge = shapely.distance(pts, REGION.boundary)                      # distance to the -2.0 polygons' edges
    d_out = np.where(inreg, 0.0, d_edge)
    d_U = shapely.distance(pts, U.boundary)
    inner = np.where(inreg, np.round(rise(d_edge) / RISE_MAX * 1000), -1).astype(int)
    skirt = np.where(~inreg & (d_out <= 5.0), np.round(d_out * 100), -1).astype(int)
    with np.errstate(invalid='ignore', divide='ignore'):
        t = np.where(inU & ~inreg, d_U / (d_U + d_out), -1)
    loft = np.where(inU & ~inreg, np.round(t * 1000), -1).astype(int)
    shp = (len(ys), len(xs))
    return dict(xs=xs, ys=ys, shape=shp, inner=inner.reshape(shp), skirt=skirt.reshape(shp), loft=loft.reshape(shp), d_edge=d_edge.reshape(shp), inreg=inreg.reshape(shp))


def surface(G, version, bed, crest=CREST_CD, run=1.0):
    """reef surface elevation (m CD) on the grid and the local seabed; NaN where there is no reef"""
    S = bed_z(G['ys'], bed)[:, None] * np.ones((1, len(G['xs'])))
    z = np.full(G['shape'], np.nan)
    inn = G['inner'] >= 0
    z[inn] = ZC + G['inner'][inn] / 1000.0 * (crest - ZC)
    if version == 'multibeam_2013_m2p0':
        m = G['skirt'] >= 0
        z[m] = np.maximum(S[m], ZC - G['skirt'][m] / 100.0 / run)
    else:
        m = G['loft'] >= 0
        z[m] = np.maximum(S[m], S[m] + (ZC - S[m]) * G['loft'][m] / 1000.0)
    return z, S


def stats(G, version, bed, crest=CREST_CD, run=1.0):
    z, S = surface(G, version, bed, crest, run)
    h = np.where(np.isfinite(z), z - S, 0.0); h = np.where(h < 0, 0, h)
    fp = h > 0.02
    return dict(volume_m3=float(h.sum() * DX * DX), footprint_area_m2=float(fp.sum() * DX * DX), h_max_m=float(h.max()), h_mean_m=float(h[fp].mean()),
                crest_z_cd=float(np.nanmax(z)))


def solve_bed(G, version, target=2800.0, crest=CREST_CD, run=1.0):
    lo, hi = -6.0, -2.0
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        v = stats(G, version, mid, crest, run)['volume_m3']
        if v > target: lo = mid            # deeper bed = more volume -> need shallower
        else: hi = mid
    return 0.5 * (lo + hi)


if __name__ == '__main__':
    G = make_grid(); print('grid', G['shape'], 'cells inner', int((G['inner'] >= 0).sum()), 'skirt', int((G['skirt'] >= 0).sum()), 'loft', int((G['loft'] >= 0).sum()))
    for ver in ('multibeam_2013_m2p0', 'asr_installed_toe_2008'):
        for b in BEDS + [None]:
            s = stats(G, ver, b); print(ver, b, {k: round(v, 2) for k, v in s.items()})
        print(ver, 'bed for 2800 m3 =', round(solve_bed(G, ver), 3))

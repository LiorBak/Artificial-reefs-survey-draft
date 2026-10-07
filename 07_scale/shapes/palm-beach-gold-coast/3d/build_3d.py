"""build_3d.py - regenerate model.js, docs.js and validation_3d.json for the Palm Beach reef 3D model.

Inputs : ../shape.json                 verified plan shape (toe outline, crest slot, geo block)
         contours_s7.json              contour lines read off the Bluecoast/Nearmap aerial   (python contours_s7.py)
         navionics_isolines.json       iso-depth lines read off the Garmin Navionics chart   (python navionics_isolines.py, from ../src/navionics/*.png)
         provenance_3d.json            hand-written provenance rows, source list and confidence_3d
         METHODS_3D.md, SOURCES_3D.md  texts shown in the viewer
Outputs: model.js (window.REEF_MODEL), docs.js (window.REEF_DOCS), validation_3d.json
Run    : python contours_s7.py ; python navionics_isolines.py ; python build_3d.py
Every numeric assumption is a named constant below and is repeated in METHODS_3D.md (A1 ... An).
Frame  : canonical frame of shape.json: x alongshore toward 334.3 deg (NNW), y offshore toward 64.3 deg (ENE), z up, z = 0 at MSL. With z up this triple is
         LEFT-handed; the viewer converts to east / north / up (right-handed): E = x sin(bx) + y sin(by), N = x cos(bx) + y cos(by).
"""
import json, os, math, datetime
import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator, RBFInterpolator
from shapely.geometry import Polygon, Point
from shapely import contains_xy
from pyproj import Proj

HERE = os.path.dirname(os.path.abspath(__file__))
P = lambda *a: os.path.join(HERE, *a)

# ---- constants (sourced values or declared assumptions; see METHODS_3D.md) ---------------------------------------------------------
CREST_Z = -1.5            # m vs MSL. ICCE 12921 (Prenzler et al. 2022), EPW 2020, Swellnet 2019: crest 1.5 m below mean sea level
DZ = 0.5                  # m, contour interval of the aerial's survey lines - ASSUMPTION A3 (not labelled in the source; see METHODS_3D.md 3.3)
# tide planes above Queensland Port Datum (LAT 1992), Gold Coast Seaway standard port, MSQ 'Semidiurnal Tidal Planes 2026' (epoch 2010-2029)
TIDE_ABOVE_LAT = dict(HAT=2.03, MHWS=1.53, MHWN=1.24, MSL=0.88, MLWN=0.51, MLWS=0.22, LAT=0.0)
MSL_ABOVE_LAT = TIDE_ABOVE_LAT['MSL']
CHART_DATUM_ABOVE_LAT = 0.0   # ASSUMPTION A5: Navionics depths are referred to chart datum = LAT (not stated by the viewer)
AHD_ABOVE_LAT = 0.76          # UNVERIFIED (search-result snippet of an MSQ page); used only for the AHD <-> MSL note, never in the geometry
NAV_BUFFER_M = 25.0       # m, Navionics iso-line points closer than this to the reef toe outline are not used for the natural seabed (A6)
NAV_MIN_PIECE = 100       # samples; shorter iso-line pieces are fragments at the window edge
NAV_SMOOTH = 1.0          # RBF smoothing (thin-plate spline) for the natural seabed (iso-line points are quantised to 1 m)
TOE_SMOOTH = 0.2          # smoothing at the toe points of the hybrid seabed
TOE_STEP = 4              # every 4th toe sample (1 m apart) enters the hybrid seabed
BEACH_SLOPE = 1 / 15.0    # visual only: rise landward of the waterline (not surveyed)
SB_X, SB_Y, SB_DX = (-300.0, 300.0), (-40.0, 620.0), 4.0
GRID = 1.0                # m, reef height grid
BLEND_M = 2.5             # m, edge ramp where the reef surface meets the seabed
THIN_M = 1.0              # m, thinning of contour vertices used in the reef TIN
SLOT_FILL_M = 1.0


def smoothstep(t):
    t = np.clip(t, 0, 1)
    return t * t * (3 - 2 * t)


# ---- frame check ----------------------------------------------------------------------------------------------------------------------
def frame_check(shp):
    """Re-derive the lat/lon of every vertex of shape.json canonical.polygons_m from the frame definition and compare with geo.polygons_latlon.
    Also the mirrored frame (x -> -x), to show that the handedness matters."""
    g, c = shp['geo'], shp['canonical']
    lat0, lon0 = g['canonical_origin_latlon']
    bx, by = math.radians(g['shoreline_bearing_deg']), math.radians((g['shoreline_bearing_deg'] + 90) % 360)
    aeqd = Proj(proj='aeqd', lat_0=lat0, lon_0=lon0, datum='WGS84')

    def ll(x, y):
        lon, lat = aeqd(x * math.sin(bx) + y * math.sin(by), x * math.cos(bx) + y * math.cos(by), inverse=True)
        return lat, lon
    poly, ref = c['polygons_m'][0], g['polygons_latlon'][0]

    def err(pt, q):
        return math.hypot((pt[0] - q[0]) * 111132.0, (pt[1] - q[1]) * 111320.0 * math.cos(math.radians(pt[0])))
    e = [err(ll(*p), q) for p, q in zip(poly, ref)]
    em = [err(ll(-p[0], p[1]), q) for p, q in zip(poly, ref)]
    la, lo = ll(*poly[0])
    return dict(vertex0_canonical_m=poly[0], vertex0_latlon_from_frame=[round(la, 7), round(lo, 7)], vertex0_latlon_in_shape_json=ref[0],
                n_vertices=len(e), max_err_m=round(max(e), 3), mean_err_m=round(float(np.mean(e)), 3), mirrored_x_mean_err_m=round(float(np.mean(em)), 1),
                x_bearing_deg=g['shoreline_bearing_deg'], y_bearing_deg=(g['shoreline_bearing_deg'] + 90) % 360,
                handedness='canonical (x, y, z up) is left-handed; ENU (E = x sin bx + y sin by, N = x cos bx + y cos by, U = z) is right-handed')


# ---- natural seabed from the Navionics SonarChart iso-lines -----------------------------------------------------------------------------
def navionics_seabed(N, toe, toe_pts=None):
    buf = toe.buffer(NAV_BUFFER_M)
    pts, vals = [], []
    for v, pieces in N['sonar']['17'].items():
        for Pc in pieces:
            if len(Pc) < NAV_MIN_PIECE:
                continue
            for x, y in Pc[::2]:
                if not buf.contains(Point(x, y)):
                    pts.append([x, y]); vals.append(float(v) + CHART_DATUM_ABOVE_LAT)
    n_lines = len(pts)
    # waterline anchors: y = 0 is the waterline of the 2025-12-01 Esri image, taken as z = 0 (MSL) -> depth below chart datum = -(MSL above chart datum)
    for x in np.arange(SB_X[0], SB_X[1] + 1, 25.0):
        pts.append([float(x), 0.0]); vals.append(-(MSL_ABOVE_LAT - CHART_DATUM_ABOVE_LAT))
    n_anchor = len(pts) - n_lines
    sm = [NAV_SMOOTH] * len(pts)
    n_toe = 0
    if toe_pts is not None:          # hybrid seabed: the toe elevations (read from the aerial's contours) are where rock meets the bed
        for (x, y), z in zip(*toe_pts):
            pts.append([float(x), float(y)]); vals.append(-float(z) - (MSL_ABOVE_LAT - CHART_DATUM_ABOVE_LAT)); sm.append(TOE_SMOOTH)
        n_toe = len(toe_pts[1])
    pts, vals = np.array(pts), np.array(vals)
    rbf = RBFInterpolator(pts, vals, kernel='thin_plate_spline', smoothing=np.array(sm))
    res = rbf(pts[:n_lines]) - vals[:n_lines]
    nx = int(round((SB_X[1] - SB_X[0]) / SB_DX)) + 1
    ny = int(round((SB_Y[1] - SB_Y[0]) / SB_DX)) + 1
    xs, ys = SB_X[0] + np.arange(nx) * SB_DX, SB_Y[0] + np.arange(ny) * SB_DX
    GX, GY = np.meshgrid(xs, ys)
    d = rbf(np.c_[GX.ravel(), GY.ravel()]).reshape(GX.shape)          # depth below LAT-equivalent chart datum (m)
    # d = depth below the chart datum; z_MSL = -d - (MSL above chart datum) = -d - MSL_ABOVE_LAT + CHART_DATUM_ABOVE_LAT
    zb = -d - (MSL_ABOVE_LAT - CHART_DATUM_ABOVE_LAT)
    # landward of the waterline: visual beach face
    beach = GY < 0
    zb = np.where(beach, -GY * BEACH_SLOPE, zb)
    fit = dict(n_points_iso=int(n_lines), n_points_anchor=int(n_anchor), n_points_toe=int(n_toe), rms_residual_m=float(np.sqrt((res ** 2).mean())),
               max_abs_residual_m=float(np.abs(res).max()), kernel='thin_plate_spline', smoothing=NAV_SMOOTH, buffer_m=NAV_BUFFER_M)
    return dict(xs=xs, ys=ys, zb=zb, d=d, fit=fit, rbf=rbf, pts=pts[:n_lines], vals=vals[:n_lines])


def seabed_at(sb, x, y):
    """bilinear sample of the natural-seabed grid (m vs MSL)"""
    fx = (np.asarray(x) - sb['xs'][0]) / SB_DX
    fy = (np.asarray(y) - sb['ys'][0]) / SB_DX
    ix = np.clip(np.floor(fx).astype(int), 0, len(sb['xs']) - 2)
    iy = np.clip(np.floor(fy).astype(int), 0, len(sb['ys']) - 2)
    tx, ty = np.clip(fx - ix, 0, 1), np.clip(fy - iy, 0, 1)
    z = sb['zb']
    return (z[iy, ix] * (1 - tx) * (1 - ty) + z[iy, ix + 1] * tx * (1 - ty) + z[iy + 1, ix] * (1 - tx) * ty + z[iy + 1, ix + 1] * tx * ty)


# ---- reef surface (TIN through the contour lines) ----------------------------------------------------------------------------------------
def thin(points, step):
    out = [points[0]]
    acc = 0.0
    for a, b in zip(points[:-1], points[1:]):
        acc += math.hypot(b[0] - a[0], b[1] - a[1])
        if acc >= step:
            out.append(b); acc = 0.0
    return out


def reef_surface(Cn, toe, slot):
    P2, Z2 = [], []
    contours = []
    for c in Cn['chains']:
        k = c['rank']
        z = CREST_Z - DZ * k
        pts = thin(c['canon_m'], THIN_M)
        for p in pts:
            P2.append(p); Z2.append(z)
        contours.append(dict(rank=k, z=z, part=c['part'], poly=[[round(p[0], 2), round(p[1], 2)] for p in thin(c['canon_m'], 2.0)]))
    # toe outline: elevation = (nearest inside contour) - DZ * min(1, distance / local spacing)   (assumption A4)
    toe_z = []
    for t in Cn['toe_samples']:
        f = min(1.0, t['d_to_K_m'] / max(t['spacing_m'], 0.5))
        z = CREST_Z - DZ * (t['K'] + f)
        P2.append(t['xy']); Z2.append(z); toe_z.append(z)
    minx, miny, maxx, maxy = slot.bounds
    gx, gy = np.meshgrid(np.arange(minx, maxx + SLOT_FILL_M, SLOT_FILL_M), np.arange(miny, maxy + SLOT_FILL_M, SLOT_FILL_M))
    mm = contains_xy(slot, gx, gy)
    for x, y in zip(gx[mm], gy[mm]):
        P2.append([float(x), float(y)]); Z2.append(CREST_Z)
    for p in Cn['slot_canon_m']:
        P2.append(p); Z2.append(CREST_Z)
    P2, Z2 = np.array(P2, float), np.array(Z2, float)
    return LinearNDInterpolator(P2, Z2), NearestNDInterpolator(P2, Z2), contours, np.array(toe_z), P2, Z2


def main():
    shp = json.load(open(P('..', 'shape.json'), encoding='utf8'))
    Cn = json.load(open(P('contours_s7.json')))
    N = json.load(open(P('navionics_isolines.json')))
    toe, slot = Polygon(Cn['toe_canon_m']), Polygon(Cn['slot_canon_m'])
    fchk = frame_check(shp)

    # ---- reef surface from the aerial's contour lines ------------------------------------------------------------------------------------
    tin, nn, contours, toe_z, P2, Z2 = reef_surface(Cn, toe, slot)
    txy = np.array([t['xy'] for t in Cn['toe_samples']])
    # ---- seabed: (a) Navionics only (independent check), (b) hybrid = Navionics outside the reef + toe elevations (used by the model) ---------
    sb_nav = navionics_seabed(N, toe)
    sb = navionics_seabed(N, toe, (txy[::TOE_STEP], toe_z[::TOE_STEP]))
    bx0, by0, bx1, by1 = toe.bounds
    x0, y0 = math.floor(bx0) - 2, math.floor(by0) - 2
    nx, ny = int(math.ceil(bx1) + 2 - x0), int(math.ceil(by1) + 2 - y0)
    xs, ys = x0 + np.arange(nx) * GRID, y0 + np.arange(ny) * GRID
    GX, GY = np.meshgrid(xs, ys)
    inside = contains_xy(toe, GX, GY)
    zt = tin(GX, GY)
    zt = np.where(np.isnan(zt), nn(GX, GY), zt)
    zb = seabed_at(sb, GX, GY)
    h = np.clip(zt - zb, 0, None)
    ring = toe.exterior
    dist_edge = np.array([[ring.distance(Point(x, y)) for x in xs] for y in ys])
    w = smoothstep(dist_edge / BLEND_M)
    zr = np.where(inside, zb + w * h, zb)
    cell = GRID * GRID
    V_env = float(((zr - zb) * inside).sum() * cell)
    V_raw = float((h * inside).sum() * cell)
    area = float(inside.sum() * cell)
    hmax = float((h * inside).max())
    ij = np.unravel_index(np.argmax(h * inside), h.shape)
    hmax_xy = (float(xs[ij[1]]), float(ys[ij[0]]))
    cs = np.array(Cn['slot_canon_m'])
    crest_bed = float(np.mean(seabed_at(sb, cs[:, 0], cs[:, 1])))
    crest_bed_nav = float(np.mean(seabed_at(sb_nav, cs[:, 0], cs[:, 1])))
    h_nav = np.clip(zt - seabed_at(sb_nav, GX, GY), 0, None)
    V_nav = float((h_nav * inside).sum() * cell)
    mean_h = V_raw / area
    sens = {str(o): float((np.clip(zt - (zb + o), 0, None) * inside).sum() * cell) for o in (-1.0, -0.5, -0.25, 0.25, 0.5, 1.0)}

    # ---- validation numbers ---------------------------------------------------------------------------------------------------------------
    zb_toe = seabed_at(sb_nav, txy[:, 0], txy[:, 1])             # Navionics-only natural seabed at the toe outline
    res_toe = toe_z - zb_toe
    buried = float((res_toe < 0).mean())
    # plane through the contour-derived toe depths (the earlier, navigation-free estimate): z = a0 + g y
    A = np.c_[np.ones(len(toe_z)), txy[:, 1]]
    keep = np.ones(len(toe_z), bool)
    for _ in range(8):
        coef = np.linalg.lstsq(A[keep], toe_z[keep], rcond=None)[0]
        r = A @ coef - toe_z
        keep = np.abs(r) < max(0.6, 2.5 * r[keep].std())
    plane = dict(a0=float(coef[0]), g=float(coef[1]), rms=float(np.sqrt((r[keep] ** 2).mean())), n=int(keep.sum()), n_all=int(len(toe_z)))
    # natural seabed profile from Navionics along y at the reef's x (mean of the two sides, x = +-150 m): depth below LAT
    prof = {}
    for yv in (150, 225, 260, 300, 340, 374, 450):
        prof[str(yv)] = round(float(np.mean([-seabed_at(sb_nav, np.array([xx]), np.array([float(yv)]))[0] - MSL_ABOVE_LAT for xx in (-150.0, 150.0)])), 2)
    # side-slope spacing from the tracked offsets (contours_s7_sd.npz)
    slopes = {}
    try:
        Z = np.load(P('contours_s7_sd.npz'))
        rings, merged = Z['rings'], Z['merged']
        mpp = Cn['transform']['scale_m_per_px']
        for name, (a, b) in {'N flank (long side, 6 m spacing)': (150, 850), 'S flank (short side)': (1300, 1950)}.items():
            sp = []
            for k in range(1, rings.shape[0] - 1):
                if k >= len(merged) or merged[k - 1][a:b].any() or merged[k][a:b].any():
                    continue
                sp.append(float(np.median(rings[k + 1][a:b] - rings[k][a:b]) * mpp))
            slopes[name] = [round(s_, 2) for s_ in sp]
    except Exception as e:
        slopes['error'] = str(e)
    # E end spacing along the crest axis (fan on the axis ray: peaks counted outward from the centre of the E end of the crest outline)
    mpp = Cn['transform']['scale_m_per_px']
    pk = Cn['axis_radii']['E']['peaks_px']
    east_sp = [round((b_ - a_) * mpp, 2) for a_, b_ in zip(pk[:-1], pk[1:])]
    # contour interval implied by the Navionics seabed at the toe: z_toe = -1.5 - s (K + f)  ->  s (crest level held fixed)
    rk = np.array([min(t['K'] + min(1.0, t['d_to_K_m'] / max(t['spacing_m'], 0.5)), 99) for t in Cn['toe_samples']])
    s_hat = {}
    for lab, off in (('LAT', 0.0), ('MSL', MSL_ABOVE_LAT)):
        zz = zb_toe + off
        s_ = -np.sum((zz + 1.5) * rk) / np.sum(rk * rk)
        rs_ = zz - (-1.5 - s_ * rk)
        s_hat[lab] = dict(s_m=float(s_), se_m=float(np.sqrt(np.sum(rs_ ** 2) / (len(rk) - 1) / np.sum(rk * rk))), rms_m=float(np.sqrt((rs_ ** 2).mean())))
    bands = {}
    for lo, hi in ((4, 6), (6, 8), (8, 11)):
        sel = (rk >= lo) & (rk < hi)
        bands['%d-%d' % (lo, hi)] = dict(n=int(sel.sum()), mean_rank=float(rk[sel].mean()), s_m=float(-(zb_toe[sel].mean() + 1.5) / rk[sel].mean()))
    interval_fit = dict(s_nav_m=s_hat['LAT']['s_m'], by_datum=s_hat, by_rank_band=bands, assumed_m=DZ,
                        e_toe_if_1m_interval=CREST_Z - 1.0 * float(rk.max()))
    datum_test = {}
    for nm, off in (('LAT', 0.0), ('MLWS', 0.22), ('MLWN', 0.51), ('AHD (0.76, unverified)', 0.76), ('MSL', 0.88), ('MHWN', 1.24), ('MHWS', 1.53), ('HAT', 2.03)):
        rr_ = toe_z - (zb_toe + off)
        datum_test[nm] = dict(offset_above_LAT_m=off, mean_m=float(rr_.mean()), rms_m=float(np.sqrt((rr_ ** 2).mean())))
    offs = np.arange(-1.0, 2.01, 0.01)
    best_off = float(offs[int(np.argmin([np.sqrt(((toe_z - (zb_toe + o)) ** 2).mean()) for o in offs]))])
    sectors = {}
    for lab, sel in (('W end (x < -40)', txy[:, 0] < -40), ('E end (y > 340)', txy[:, 1] > 340), ('N flank (x > 20, y < 300)', (txy[:, 0] > 20) & (txy[:, 1] < 300)),
                     ('S flank', (txy[:, 0] < 20) & (txy[:, 1] > 260) & (txy[:, 1] < 340))):
        rr_ = (toe_z - zb_toe)[sel]
        sectors[lab] = dict(n=int(sel.sum()), mean_m=float(rr_.mean()), sd_m=float(rr_.std()))
    seabed_gebco = float(-seabed_at(sb_nav, np.array([23.0]), np.array([534.0]))[0])    # chart-seabed depth (m below MSL) at the GEBCO cell centre
    # does the reef show in the SonarChart? deviation of each iso-depth line from the straight chord between its positions at x = -250 and x = +250 m
    sig = {}
    for v, pieces in N['sonar']['17'].items():
        Pc = max(pieces, key=len)
        Pc = np.array(Pc)
        if len(Pc) < NAV_MIN_PIECE:
            continue
        o = np.argsort(Pc[:, 0])
        Pc = Pc[o]
        if Pc[0, 0] > -240 or Pc[-1, 0] < 240:
            continue
        ya, yb = np.interp(-250, Pc[:, 0], Pc[:, 1]), np.interp(250, Pc[:, 0], Pc[:, 1])
        chord = ya + (yb - ya) * (Pc[:, 0] + 250) / 500.0
        sel = (Pc[:, 0] > -100) & (Pc[:, 0] < 100)
        dev = (Pc[:, 1] - chord)[sel]
        sig[v] = dict(max_dev_m=float(dev[np.argmax(np.abs(dev))]), min_dist_to_toe_m=float(min(toe.exterior.distance(Point(*p)) for p in Pc[sel][::5])))
    min_iso = min(float(v) for v, pcs in N['sonar']['17'].items() if any(len(p_) >= NAV_MIN_PIECE for p_ in pcs) and min(toe.exterior.distance(Point(*q)) for p_ in pcs if len(p_) >= NAV_MIN_PIECE for q in p_[::5]) < 40)
    anchors = {'navionics_reef_signature': dict(lines=sig, shallowest_iso_line_within_40m_of_toe_m=min_iso), 'sonar_depth_below_LAT_at_y_(mean of x=+-150 m)': prof}
    stated = dict(register_volume_m3=33000, register_height_m=5, card_volume_m3=25000, rock_tonnes=60000,
                  bulk_density_t_m3_if_33000=60000 / 33000.0, solid_density_t_m3_if_25000=60000 / 25000.0,
                  volume_model_over_register=V_raw / 33000.0)
    val = dict(interval_fit=interval_fit, datum_test=datum_test, datum_rms_minimum_offset_above_LAT_m=best_off, toe_residual_by_sector=sectors, east_axis_spacing_m=east_sp,
               gebco=dict(value_m=-13.0, cell_centre_canonical=[23.0, 534.0], navionics_z_msl=float(-seabed_gebco), diff_m=float(-13.0 + seabed_gebco)),
               frame_check=fchk, volume_envelope_m3=V_raw, volume_blended_m3=V_env, area_m2=area, mean_height_m=mean_h, max_height_m=hmax,
               max_height_at_xy=hmax_xy, crest_mean_bed_z=crest_bed, height_at_crest_m=CREST_Z - crest_bed,
               navionics_only=dict(crest_mean_bed_z=crest_bed_nav, height_at_crest_m=CREST_Z - crest_bed_nav, volume_envelope_m3=V_nav),
               volume_sensitivity_by_seabed_offset_m=sens,
               toe_depth_range_m=[float(toe_z.min()), float(toe_z.max())], crest_below_LAT_m=CREST_Z + MSL_ABOVE_LAT,
               toe_vs_navionics=dict(mean_m=float(res_toe.mean()), sd_m=float(res_toe.std()), fraction_toe_below_seabed=buried,
                                     mean_if_chart_datum_were_MSL_m=float(np.mean(toe_z - (zb_toe + MSL_ABOVE_LAT))),
                                     n=int(len(toe_z))),
               contour_plane_fit=plane, navionics_fit=sb_nav['fit'], hybrid_fit=sb['fit'], side_slope_spacing_m=slopes, anchors=anchors, stated=stated,
               fish_haven=dict(charted_least_depth_m=1.5, crest_depth_below_LAT_m=-CREST_Z - MSL_ABOVE_LAT,
                               difference_m=1.5 - (-CREST_Z - MSL_ABOVE_LAT)))

    # ---- model.js ---------------------------------------------------------------------------------------------------------------------
    rel = {k: round(v - MSL_ABOVE_LAT, 2) for k, v in TIDE_ABOVE_LAT.items()}
    zgrid = np.round(zr * 100).astype(int)
    zgrid = np.where(inside | (dist_edge < 2.0), zgrid, -32768)
    sbz = np.round(sb['zb'] * 100).astype(int)
    xb, yb = shp['geo']['shoreline_bearing_deg'], (shp['geo']['shoreline_bearing_deg'] + 90) % 360
    nav_lines = []
    for v, pieces in N['sonar']['17'].items():
        for Pc in pieces:
            if len(Pc) >= NAV_MIN_PIECE:
                nav_lines.append(dict(depth_chart_m=float(v), z=-float(v) - (MSL_ABOVE_LAT - CHART_DATUM_ABOVE_LAT), poly=[[round(p[0], 1), round(p[1], 1)] for p in Pc[::3]]))
    hr = N['hand_reads']
    model = dict(
        meta=dict(slug='palm-beach-gold-coast', name=shp['name'], generated=datetime.date.today().isoformat(),
                  state_represented='As built (rock placed May-Sept 2019, certified Sept 2019). No later works, damage or renewal found (monitoring to 2023: stable; rock visible on Esri imagery of 2025-12-01). Contour lines from the Bluecoast/Nearmap aerial of the completed reef (image undated, Sept 2019 - Sept 2020).',
                  units='metres; z up; z = 0 at mean sea level (MSL)', vertical_datum='MSL (Gold Coast Seaway MSL = %.2f m above LAT 1992)' % MSL_ABOVE_LAT),
        frame=dict(x_bearing_deg=xb, y_bearing_deg=yb,
                   note=('Canonical frame of shape.json: +x alongshore toward %.1f deg true (NNW), +y offshore toward %.1f deg true (ENE); x then y run CLOCKWISE on a north-up map, '
                         'so with z up the triple (x, y, z) is LEFT-handed. The viewer converts to east/north/up (right-handed) before drawing: E = x sin(bx) + y sin(by); N = x cos(bx) + y cos(by); '
                         'vertex check: canonical vertex 0 -> %s vs %s in shape.json geo.polygons_latlon (max error over 47 vertices %.2f m; the mirror image would be %.0f m off).')
                        % (xb, yb, fchk['vertex0_latlon_from_frame'], fchk['vertex0_latlon_in_shape_json'], fchk['max_err_m'], fchk['mirrored_x_mean_err_m']),
                   origin_latlon=shp['geo']['canonical_origin_latlon'], centroid_latlon=shp['geo']['centroid_latlon'],
                   north_in_xy=[round(math.cos(math.radians(xb)), 4), round(math.cos(math.radians(yb)), 4)],
                   east_in_xy=[round(math.sin(math.radians(xb)), 4), round(math.sin(math.radians(yb)), 4)], check=fchk),
        shoreline=dict(y=0.0, note='waterline fitted to Esri World Imagery 2025-12-01 (shape.json canonical.frame); taken as z = 0 (MSL) - tide stage of that image unknown (assumption A7)'),
        seabed=dict(kind='grid', x0=float(sb['xs'][0]), y0=float(sb['ys'][0]), dx=SB_DX, nx=int(len(sb['xs'])), ny=int(len(sb['ys'])), z_cm=sbz.flatten().tolist(),
                    note=('Seabed without the reef: thin-plate-spline surface through (i) the Garmin Navionics SonarChart iso-depth lines (1 m interval, z17 screenshots) outside a %.0f m '
                          'buffer round the reef (depth below chart datum taken = depth below LAT, assumption A5; z_MSL = -d - %.2f) and (ii) the toe elevations read from the aerial contour lines (hybrid; the Navionics-only surface is kept as the independent check). '
                          'Under the reef and seaward of the 10 m line the surface is interpolated / extrapolated. Landward of the waterline (y < 0) a visual beach face rises at 1:15 (not surveyed). '
                          'Sand bars, rips and the natural reef up-coast are NOT modelled.') % (NAV_BUFFER_M, MSL_ABOVE_LAT),
                    fit=sb['fit'], datum_assumption='chart datum = LAT'),
        reef=dict(toe_polygon=Cn['toe_canon_m'], crest_polygon=Cn['slot_canon_m'], crest_z=CREST_Z,
                  grid=dict(x0=x0, y0=y0, dx=GRID, nx=nx, ny=ny, z_cm=zgrid.flatten().tolist(), nodata=-32768),
                  contours=contours, contour_interval_m=DZ,
                  side_slope_rule=('surface = linear (Delaunay) interpolation between the survey contour lines read off the aerial, each at z = -1.5 - 0.5 k m (k = number of lines crossed outward from the 59 x 6 m crest outline); '
                                   'the toe outline lies at the next 0.5 m level, interpolated by its fractional position (<= one interval); edge ramped (%.1f m) onto the seabed' % BLEND_M),
                  layers=[dict(name='core', rock='300-1000 kg', source='EPW 2020 (s8)'), dict(name='armour', rock='1-8 t; crest 6-8 t', source='EPW 2020 (s8); ICCE 12921'),
                          dict(note='layer thicknesses NOT sourced - the viewer draws one rock surface')],
                  stats=dict(area_m2=area, volume_m3=V_raw, max_height_m=hmax, mean_height_m=mean_h, height_at_crest_m=CREST_Z - crest_bed)),
        navionics=dict(note='Garmin Navionics SonarChart iso-depth lines (read from screenshots of maps.garmin.com/en-US/marine, zoom 17, accessed 2026-10-05; not for navigation)',
                       lines=nav_lines, fish_haven=dict(text='FISH HAVEN 1.5MT (nautical chart label)', xy=hr['fish_haven_label']['canon_m'], symbol_xy=hr['fish_haven_symbol']['canon_m'])),
        water=dict(levels=[dict(key=k, label=lab, z=rel[k], above_lat=TIDE_ABOVE_LAT[k]) for k, lab in
                           [('LAT', 'LAT (lowest astronomical tide)'), ('MLWS', 'MLWS'), ('MLWN', 'MLWN'), ('MSL', 'MSL'), ('MHWN', 'MHWN'), ('MHWS', 'MHWS'), ('HAT', 'HAT (highest astronomical tide)')]],
                   source='Maritime Safety Queensland (2026), Semidiurnal Tidal Planes 2026, Gold Coast Seaway standard port, epoch 2010-2029; heights above LAT converted to MSL by subtracting %.2f m' % MSL_ABOVE_LAT,
                   default='MSL', ahd_note='AHD is about %.2f m above LAT at the Seaway standard port (UNVERIFIED snippet), i.e. MSL = AHD + %.2f m; not applied' % (AHD_ABOVE_LAT, MSL_ABOVE_LAT - AHD_ABOVE_LAT)),
        validation=val)
    extras = dict(toe_z=toe_z, toe_xy=txy, zb_toe=zb_toe, sb=sb, sb_nav=sb_nav, grid=dict(xs=xs, ys=ys, zr=zr, zb=zb, zt=zt, inside=inside), tin_points=(P2, Z2), plane=plane)
    return model, val, extras


def write_model_js(model):
    open(P('model.js'), 'w', encoding='utf8').write('window.REEF_MODEL = ' + json.dumps(model, separators=(',', ':')) + ';\n')


def write_docs_js():
    docs = {}
    for key, fn in (('methods_md', 'METHODS_3D.md'), ('sources_md', 'SOURCES_3D.md')):
        fp = P(fn)
        docs[key] = open(fp, encoding='utf8').read() if os.path.exists(fp) else '(missing %s)' % fn
    open(P('docs.js'), 'w', encoding='utf8').write('window.REEF_DOCS = ' + json.dumps(docs) + ';\n')


if __name__ == '__main__':
    model, val, _extras = main()
    json.dump(val, open(P('validation_3d.json'), 'w'), indent=1)
    import write_provenance
    prov = write_provenance.build(val)
    json.dump(prov, open(P('provenance_3d.json'), 'w', encoding='utf8'), indent=1)
    model.update(prov)
    write_model_js(model)
    write_docs_js()
    print('model.js bytes', os.path.getsize(P('model.js')))
    print(json.dumps({k: val[k] for k in ('area_m2', 'volume_envelope_m3', 'mean_height_m', 'max_height_m', 'height_at_crest_m', 'toe_depth_range_m', 'crest_below_LAT_m')}))
    print('frame check', json.dumps(val['frame_check']))
    print('toe vs navionics', json.dumps(val['toe_vs_navionics']))
    print('navionics fit', json.dumps(val['navionics_fit']))
    print('plane fit', json.dumps(val['contour_plane_fit']))
    print('anchors', json.dumps(val['anchors']))
    print('slopes', json.dumps(val['side_slope_spacing_m']))
    print('sens', json.dumps(val['volume_sensitivity_by_seabed_offset_m']))

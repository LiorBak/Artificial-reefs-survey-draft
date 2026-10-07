"""contours_s7.py - read the survey contour lines off the Bluecoast/Nearmap aerial (source s7) of the Palm Beach reef.

Reads  ../src/bluecoast_AR_aerial_Nearmaps.jpg  and  ../shape.json ; writes contours_s7.json (pixel + canonical-metre polylines per contour rank)
and contours_s7_sd.npz (the tracked offset curves, used by the figure scripts).  See METHODS_3D.md section 3.3.

Method (all steps are deterministic; every constant is below):
  1. LINE FILTER. Red channel, mean along a 31 px segment minus the mean of two parallel flanks 4.5 px either side, maximum over 30 orientations.
     Contour lines are thin grey lines drawn on the photo; the filter gives a high response on them (typically 30-200) and <= ~25 on rock/foam texture.
  2. OFFSET COORDINATES. Base curve B(s) = the 59 x 6 m crest outline (8 hand-read vertices, METHOD.md step 2c) smoothed with a 12 px Gaussian (periodic),
     s = arc length (0.5 px steps), n(s) = outward unit normal. A point is p(s, d) = B(s) + d n(s). The response is resampled on (s, d): in this image every
     contour line is a smooth, nearly horizontal ridge (the lines are close to offset curves of the crest outline).
  3. RING TRACKING. Line k (k = 1, 2, ... counted outward from the crest outline, which is line 0) is the ridge d_k(s) that maximises
     sum_s [ min(R, 60) - 0.6 (d_k - d_{k-1}) ] - 0.6 sum_s |change in spacing|  (dynamic programming, periodic in s).
     The 0.6 per px term makes the NEAREST ridge win, so a line cannot be skipped; the spacing-change term lets the path follow the end cap.
     The council toe outline (shape.json canonical polygon, = outermost contour) bounds the domain: a line k exists at s only if it lies at least
     0.55 of the local spacing inside the outline, otherwise it has MERGED with the outline (lines peel off the outline towards the seaward end).
  4. The outline is itself contour K(s)+1, where K(s) = number of lines strictly inside it along the ray s.
Output polylines are in aerial pixels and in canonical metres (similarity fit of the 47-vertex traced outline to shape.json canonical.polygons_m).
"""
import json, os, math
import numpy as np
import cv2
from scipy import ndimage as ndi
from shapely.geometry import Polygon, Point

HERE = os.path.dirname(os.path.abspath(__file__))
SHAPE = os.path.join(HERE, '..', 'shape.json')
IMG = os.path.join(HERE, '..', 'src', 'bluecoast_AR_aerial_Nearmaps.jpg')
OUT = os.path.join(HERE, 'contours_s7.json')
OUT_NPZ = os.path.join(HERE, 'contours_s7_sd.npz')

# hand-read crest outline in s7 pixels (METHOD.md step 2c, re-checked on 3x zoom grids)
SLOT_PX = [(636, 724), (1105, 848), (1116, 851), (1119, 862), (1114, 884), (1107, 897), (1100, 898), (623, 772)]
S_STEP = 0.5            # px, spacing of the rays along the crest outline
SMOOTH_PX = 12.0
D0 = 0.0
DMAX = 1100             # px, longest offset considered
JMIN, JMAX = 14, 135    # px, allowed spacing between successive lines
DJ = 3                  # px, largest change of spacing between neighbouring rays (0.5 px apart): lines are smooth
LAM, CAP, R0, PRI = 1.0, 60.0, 30.0, 15.0   # DP weights: smoothness, response cap, response offset, nearest-ridge prior
MERGE_FRAC = 1.40       # line k merges with the outline if (outline - line k-1) < MERGE_FRAC * local spacing
MIN_SPACING = 15.0      # px, local spacing used where the previous two lines coincide
MAX_RINGS = 18
MIN_RUN_PX = 140.0      # px, shortest accepted line segment (= 16 m on the ground)
MIN_RUN_R = 30.0        # mean line response along an accepted segment
FAN_MAX_DEG, FAN_STEP_DEG, FAN_TOL_PX, FAN_MIN_R = 80.0, 0.25, 7.0, 24.0
FAN_L0_MAX_PX = 35.0
MAX_SLOPE = 0.45        # largest trusted slope (px of offset per px of arc length) of a flank contour
CAP_EXCLUDE_PX = 60.0   # flank rays whose base point is within this distance of the E-end centre are replaced by part B


def similarity_fit(P, C):
    Pm, Cm = P.mean(0), C.mean(0)
    A, B = P - Pm, C - Cm
    U, S, Vt = np.linalg.svd(A.T @ B)
    R = Vt.T @ U.T
    if np.linalg.det(R) < 0:
        Vt[-1] *= -1
        R = Vt.T @ U.T
    s = S.sum() / (A ** 2).sum()
    res = s * (A @ R.T) + Cm - C
    return dict(scale_m_per_px=float(s), R=R.tolist(), Pm=Pm.tolist(), Cm=Cm.tolist(),
                rot_deg=float(np.degrees(np.arctan2(R[1, 0], R[0, 0]))),
                max_resid_m=float(np.sqrt((res ** 2).sum(1)).max()))


def px_to_canon(p, T):
    p = np.asarray(p, float)
    R = np.array(T['R'])
    return T['scale_m_per_px'] * ((p - np.array(T['Pm'])) @ R.T) + np.array(T['Cm'])


def line_filter(img_bgr):
    red = img_bgr[..., 2].astype(np.float32)
    Lb = cv2.GaussianBlur(red, (0, 0), 0.7)
    k = 31
    best = np.full(red.shape, -1e9, np.float32)
    for ang in np.arange(0, 180, 6):
        c = (k + 14) // 2
        kern_c = np.zeros((k + 14, k + 14), np.float32)
        kern_s = np.zeros_like(kern_c)
        a = np.radians(ang)
        dx, dy = np.cos(a), np.sin(a)
        nx, ny = -dy, dx
        for t in np.linspace(-k / 2, k / 2, k * 2):
            kern_c[int(round(c + t * dy)), int(round(c + t * dx))] = 1
            for s in (-4.5, 4.5):
                kern_s[int(round(c + t * dy + s * ny)), int(round(c + t * dx + s * nx))] = 1
        kern_c /= kern_c.sum()
        kern_s /= kern_s.sum()
        best = np.maximum(best, cv2.filter2D(Lb, -1, kern_c - kern_s))
    return best


def resample_closed(P, step):
    P = np.vstack([P, P[:1]])
    seg = np.hypot(*np.diff(P, axis=0).T)
    L = np.concatenate([[0], np.cumsum(seg)])
    t = np.arange(0, L[-1], step)
    return np.c_[np.interp(t, L, P[:, 0]), np.interp(t, L, P[:, 1])]


def track(dprev, dprev2, R, dtoe):
    """one DP pass (periodic in s via 3 copies). Returns the offset curve of the next line and a 'merged' flag per ray.
    States: 0 = merged with the previous line / the outline (j = 0); 1..M = free, spacing j = JMIN + state - 1."""
    ns = len(dprev)
    reps = 3
    N3 = ns * reps
    dp3, dq3, dt3 = np.tile(dprev, reps), np.tile(dprev2, reps), np.tile(dtoe, reps)
    Rt = np.tile(R, (reps, 1))
    js = np.arange(JMIN, JMAX + 1)
    M = len(js)
    NEG = -1e9
    cost = np.full((N3, M + 1), NEG, np.float32)
    for i in range(N3):
        room = dt3[i] - dp3[i]
        sloc = max(dp3[i] - dq3[i], MIN_SPACING)
        if room < MERGE_FRAC * sloc:       # no room for another line: it has merged with the outline
            cost[i, 0] = 0.0
            continue
        d = dp3[i] + js
        ok = d <= dt3[i] - 0.45 * sloc
        di = np.clip(np.round(d).astype(int), 0, Rt.shape[1] - 1)
        cost[i, 1:] = np.where(ok, np.minimum(Rt[i, di], CAP) - R0 - PRI * js / sloc, NEG)
        cost[i, 0] = 0.0 if not ok.any() else NEG
    score = np.full((N3, M + 1), -1e12, np.float32)
    back = np.zeros((N3, M + 1), np.int16)
    score[0] = cost[0]
    shifts = list(range(-DJ, DJ + 1))
    jq = LAM * (JMIN + np.arange(DJ + 1))          # penalty for leaving / joining the merged state at free state 1..DJ+1
    for i in range(1, N3):
        prev = score[i - 1]
        P = prev[1:]
        new = np.full(M, -1e12, np.float32)
        bk = np.zeros(M, np.int16)
        for dj in shifts:
            if dj >= 0:
                cand = P[:M - dj] - LAM * dj
                sl = slice(dj, M)
            else:
                cand = P[-dj:] - LAM * (-dj)
                sl = slice(0, M + dj)
            m = cand > new[sl]
            tmp = new[sl]
            tmp[m] = cand[m]
            btmp = bk[sl]
            btmp[m] = dj
        # merged -> free
        cm = prev[0] - jq
        m = cm > new[:DJ + 1]
        tmp = new[:DJ + 1]
        tmp[m] = cm[m]
        btmp = bk[:DJ + 1]
        btmp[m] = 999
        # free -> merged, merged -> merged
        cf = prev[1:DJ + 2] - jq
        qf = int(np.argmax(cf))
        m0, b0 = prev[0], 0
        if cf[qf] > m0:
            m0, b0 = cf[qf], 1000 + qf + 1
        score[i, 0] = m0 + cost[i, 0]
        back[i, 0] = b0
        score[i, 1:] = new + cost[i, 1:]
        back[i, 1:] = bk
    st = int(np.argmax(score[-1]))
    path = [st]
    for i in range(N3 - 1, 0, -1):
        a = int(back[i][st])
        if st == 0:
            st = 0 if a == 0 else a - 1000
        else:
            st = 0 if a == 999 else st - a
        st = int(np.clip(st, 0, M))
        path.append(st)
    path = np.array(path[::-1])
    mid = path[ns:2 * ns]
    j = np.where(mid == 0, 0.0, JMIN + mid - 1.0)
    return dprev + j, (mid == 0)


def clean_runs(mk, dk, dprev, rr, Bs, Nn):
    """a free run of line k is kept only if its polyline is >= MIN_RUN_PX long and its mean line response >= MIN_RUN_R; otherwise it is treated as
    'no line here' (merged with the previous line = absent), because a real contour is a long smooth line while fragments are rock/foam texture."""
    n = len(mk)
    free = ~mk
    if free.all():
        return mk, dk
    start = int(np.argmax(mk))
    idx_all = [(start + t) % n for t in range(n)]
    out_m = mk.copy()
    out_d = dk.copy()
    run = []
    def close(run):
        if not run:
            return
        idx = np.array(run)
        P = np.c_[Bs[idx, 0] + Nn[idx, 0] * (dk[idx] - D0), Bs[idx, 1] + Nn[idx, 1] * (dk[idx] - D0)]
        length = float(np.hypot(*np.diff(P, axis=0).T).sum()) if len(P) > 1 else 0.0
        if length < MIN_RUN_PX or rr[idx].mean() < MIN_RUN_R:
            out_m[idx] = True
            out_d[idx] = dprev[idx]
    for i in idx_all:
        if free[i]:
            run.append(i)
        else:
            close(run)
            run = []
    close(run)
    return out_m, out_d


def fan_lines(best, ce, a0, toe_poly, name='E'):
    """PART B - the seaward (E) end. Rays are cast from the centre of the E end of the crest outline, 0.25 deg apart over +-FAN_MAX_DEG about the crest axis.
    On the axis ray the peaks, counted outward, are line 0 (the crest outline), line 1, 2, ...; the outermost peak is the toe outline. Going away from the axis
    each line is followed ray by ray (nearest peak to the prediction within a tolerance, up to 10 missed rays), so a line keeps its number;
    a line ends where it reaches the toe outline (it has merged with it). Returns {rank: [(alpha_deg, r_px), ...]} and the outline radius per alpha."""
    from scipy.signal import find_peaks
    from shapely.geometry import LineString
    H, W = best.shape
    out = {}
    dt_of = {}

    def peaks_on(alpha):
        t = a0 + math.radians(alpha)
        u = np.array([math.cos(t), math.sin(t)])
        ds = np.arange(0, 1150, 0.5)
        X, Y = ce[0] + u[0] * ds, ce[1] + u[1] * ds
        ok = (X >= 0) & (X < W - 1) & (Y >= 0) & (Y < H - 1)
        val = ndi.map_coordinates(best, [Y[ok], X[ok]], order=1)
        pk, _ = find_peaks(val, height=FAN_MIN_R, prominence=10, distance=12)
        x = LineString([ce, ce + u * 3000]).intersection(toe_poly.exterior)
        pts = [x] if x.geom_type == 'Point' else list(getattr(x, 'geoms', []))
        dt = max(math.hypot(p.x - ce[0], p.y - ce[1]) for p in pts) if pts else 1e9
        return ds[ok][pk], dt
    r0, dt0 = peaks_on(0.0)
    inner = [r for r in r0 if r < dt0 - 12]
    # the first peak is line 0 (the crest outline itself) only if it lies close to the centre; at the W end the centre is ON the crest edge, the outline is
    # not found as a peak and the first peak is already line 1
    first_rank = 0 if r0[0] < FAN_L0_MAX_PX else 1
    print('fan %s: peaks on the axis ray' % name, [int(r) for r in r0], 'outline at', int(dt0), '-> lines %d..%d inside the outline' % (first_rank, len(inner) - 1 + first_rank))
    for sign in (+1, -1):
        state = {k + first_rank: dict(r=float(r), slope=0.0, miss=0, alive=True) for k, r in enumerate(inner)}
        for k in state:
            out.setdefault(k, []).append((0.0, state[k]['r']))
        for a in np.arange(FAN_STEP_DEG, FAN_MAX_DEG + 1e-9, FAN_STEP_DEG):
            alpha = sign * a
            pk, dt = peaks_on(alpha)
            dt_of[round(alpha, 3)] = dt
            for k, st in state.items():
                if not st['alive']:
                    continue
                pred = st['r'] + st['slope']
                if pred > dt - 8:
                    st['alive'] = False
                    continue
                if len(pk):
                    j = int(np.argmin(np.abs(pk - pred)))
                    if abs(pk[j] - pred) <= FAN_TOL_PX:
                        st['slope'] = 0.6 * st['slope'] + 0.4 * (pk[j] - st['r'])
                        st['r'], st['miss'] = float(pk[j]), 0
                        out[k].append((alpha, st['r']))
                        continue
                st['miss'] += 1
                st['r'] = pred
                if st['miss'] > 10:
                    st['alive'] = False
    for k in out:
        out[k] = sorted(out[k])
    return out, dt_of, [float(r) for r in r0], float(dt0)


def main():
    shp = json.load(open(SHAPE, encoding='utf8'))
    s7 = [s for s in shp['sources'] if s['id'] == 's7'][0]
    toe_px = np.array(s7['pixel_polygons'][0])
    toe_m = np.array(shp['canonical']['polygons_m'][0])
    T = similarity_fit(toe_px, toe_m)
    print('pixel->canonical fit', {k: T[k] for k in ('scale_m_per_px', 'rot_deg', 'max_resid_m')})
    img = cv2.imread(IMG)
    H, W = img.shape[:2]
    best = line_filter(img)

    from shapely.geometry import Polygon, LineString
    B = resample_closed(np.array(SLOT_PX, float), S_STEP)
    n = len(B)
    sg = SMOOTH_PX / S_STEP
    Bs = np.c_[ndi.gaussian_filter1d(B[:, 0], sg, mode='wrap'), ndi.gaussian_filter1d(B[:, 1], sg, mode='wrap')]
    Tg = np.roll(Bs, -1, axis=0) - np.roll(Bs, 1, axis=0)
    Tg /= np.hypot(*Tg.T)[:, None]
    Nn = np.c_[Tg[:, 1], -Tg[:, 0]]
    if np.mean(np.sum((Bs - Bs.mean(0)) * Nn, axis=1)) < 0:
        Nn = -Nn
    ds = np.arange(0, DMAX, 1.0)
    X = Bs[:, 0][:, None] + Nn[:, 0][:, None] * (ds - D0)[None, :]
    Y = Bs[:, 1][:, None] + Nn[:, 1][:, None] * (ds - D0)[None, :]
    R = ndi.map_coordinates(best, [Y, X], order=1, mode='nearest')
    R[~((X >= 0) & (X < W - 1) & (Y >= 0) & (Y < H - 1))] = 0
    dom = np.zeros((H, W), np.float32)
    cv2.fillPoly(dom, [np.round(toe_px).astype(np.int32)], 1)
    inside = ndi.map_coordinates(dom, [Y, X], order=1, mode='constant')
    dtoe = np.array([np.argmax(inside[i] < 0.5) if (inside[i] < 0.5).any() else DMAX - 1 for i in range(n)], float)

    rings = [np.zeros(n), np.zeros(n)]      # rings[0] = crest outline (d = 0); the extra entry is a dummy 'line -1' = same curve
    merged = []
    for k in range(1, MAX_RINGS + 1):
        dprev2 = rings[-2] if k > 1 else np.full(n, -40.0)   # nominal first spacing 40 px
        dk, mk = track(rings[-1], dprev2, R, dtoe)
        rr = np.array([R[i, int(np.clip(round(dk[i]), 0, DMAX - 1))] for i in range(n)])
        mk, dk = clean_runs(mk, dk, rings[-1], rr, Bs, Nn)
        rr = np.array([R[i, int(np.clip(round(dk[i]), 0, DMAX - 1))] for i in range(n)])
        frac_free = float((~mk).mean())
        print('line %2d: free on %.0f%% of the rays, mean response where free %.1f (>30 on %.0f%%)' % (
            k, 100 * frac_free, rr[~mk].mean() if (~mk).any() else 0, 100 * (rr[~mk] > 30).mean() if (~mk).any() else 0))
        rings.append(dk)
        merged.append(mk)
        if frac_free < 0.01:
            break
    rings = rings[1:]                        # rings[0] = crest outline, rings[k] = line k
    nlines = len(rings) - 1
    # ---- part B (both ends) --------------------------------------------------------------------------------------------------------
    sp = np.array(SLOT_PX, float)
    c0 = sp.mean(0)
    ends = {'E': sp[2:6].mean(0), 'W': sp[[0, 7]].mean(0)}
    toe_poly = Polygon(toe_px)
    fans = {}
    axis_radii = {}
    for name, cc in ends.items():
        a0 = math.atan2(*(cc - c0)[::-1])
        fan, dt_of, r_axis, dt_axis = fan_lines(best, cc, a0, toe_poly, name)
        fans[name] = (cc, a0, fan)
        axis_radii[name] = dict(peaks_px=r_axis, outline_px=dt_axis)
    # ---- chains: A (flank rays away from the E end) + B (fan) -----------------------------------------------------------------------
    valid = np.ones(n, bool)
    for cc in ends.values():
        valid &= np.hypot(*(Bs - cc).T) > CAP_EXCLUDE_PX
    chains = []
    for k in range(1, nlines + 1):
        free = (~merged[k - 1]) & valid
        # a contour is smooth: where the tracked offset changes faster than MAX_SLOPE per px of arc length (corner chamfers, foam streaks) the
        # track is not trusted and the piece is dropped (the TIN then interpolates from the neighbouring lines and the toe outline)
        dk_s = ndi.uniform_filter1d(rings[k], 21, mode='wrap')
        slope = np.abs(np.gradient(dk_s)) / S_STEP
        bad = ndi.binary_dilation(slope > MAX_SLOPE, iterations=30)
        free &= ~bad
        if free.sum() < 4:
            continue
        runs, cur = [], []
        start = int(np.argmax(~free))
        for t in range(n):
            i = (start + t) % n
            if free[i]:
                cur.append(i)
            else:
                if len(cur) > 3:
                    runs.append(cur)
                cur = []
        if len(cur) > 3:
            runs.append(cur)
        runs = [r for r in runs if len(r) >= 160]     # >= 80 px of arc
        for r in runs:
            idx = np.array(r)
            px = np.c_[Bs[idx, 0] + Nn[idx, 0] * (rings[k][idx] - D0), Bs[idx, 1] + Nn[idx, 1] * (rings[k][idx] - D0)]
            chains.append(dict(rank=k, part='A', closed=False, n_points=len(px), px=px[::4].round(1).tolist(),
                               canon_m=px_to_canon(px[::4], T).round(2).tolist()))
    for name, (cc, a0, fan) in fans.items():
        for k, lst in fan.items():
            if k == 0 or len(lst) < 8:
                continue
            al = np.array([x for x, _ in lst])
            rr_ = np.array([y for _, y in lst])
            t = a0 + np.radians(al)
            px = np.c_[cc[0] + np.cos(t) * rr_, cc[1] + np.sin(t) * rr_]
            brk = np.where(np.diff(al) > 1.0)[0] + 1
            for seg in np.split(np.arange(len(al)), brk):
                if len(seg) < 8:
                    continue
                chains.append(dict(rank=int(k), part='B' + name, closed=False, n_points=len(seg), px=px[seg].round(1).tolist(),
                                   canon_m=px_to_canon(px[seg], T).round(2).tolist(), alpha_deg=[float(al[seg[0]]), float(al[seg[-1]])]))
    # ---- splice check: B points against A points of the same rank -------------------------------------------------------------------
    from scipy.spatial import cKDTree
    byrank = {}
    for c in chains:
        byrank.setdefault(c['rank'], []).append(c)
    splice = {}
    for k, lst in byrank.items():
        A_ = np.vstack([np.array(c['px']) for c in lst if c['part'] == 'A']) if any(c['part'] == 'A' for c in lst) else None
        B_ = np.vstack([np.array(c['px']) for c in lst if c['part'].startswith('B')]) if any(c['part'].startswith('B') for c in lst) else None
        if A_ is None or B_ is None:
            continue
        d, _ = cKDTree(A_).query(B_)
        splice[k] = dict(min_gap_px=float(d.min()), min_gap_m=float(d.min() * T['scale_m_per_px']))
    print('gap between the flank part (A) and the end-fan part (B) of the same line:', json.dumps(splice))
    # ---- toe outline: elevation rank from the nearest inside line ---------------------------------------------------------------------
    toe_c = toe_m
    ring = Polygon(toe_c).exterior
    L = ring.length
    ns_ = int(L // 1.0)
    S = np.array([[ring.interpolate(i * L / ns_).x, ring.interpolate(i * L / ns_).y] for i in range(ns_)])
    trees = {k: cKDTree(np.vstack([np.array(c['canon_m']) for c in lst])) for k, lst in byrank.items()}
    toe_samples = []
    for p in S:
        dists = {k: float(t.query(p)[0]) for k, t in trees.items()}
        K = min(dists, key=dists.get)
        dK = dists[K]
        # local spacing: distance from the nearest point of line K to line K-1 (or to the crest outline for K = 1)
        _, iK = trees[K].query(p)
        q = trees[K].data[iK]
        if K - 1 in trees:
            sloc = float(trees[K - 1].query(q)[0])
        else:
            sloc = float(Polygon(px_to_canon(np.array(SLOT_PX, float), T)).exterior.distance(Point(*q)))
        toe_samples.append(dict(xy=[round(float(p[0]), 2), round(float(p[1]), 2)], K=int(K), d_to_K_m=round(dK, 2), spacing_m=round(sloc, 2)))
    out = dict(transform=T, slot_px=SLOT_PX, slot_canon_m=px_to_canon(np.array(SLOT_PX), T).round(2).tolist(),
               toe_px=toe_px.tolist(), toe_canon_m=toe_m.tolist(), centre_px=[float(c0[0]), float(c0[1])], cap_centres_px={k: v.tolist() for k, v in ends.items()},
               chains=chains, toe_samples=toe_samples, splice_check=splice, axis_radii=axis_radii,
               params=dict(s_step_px=S_STEP, jmin=JMIN, jmax=JMAX, dj=DJ, lam=LAM, cap=CAP, r0=R0, pri=PRI, merge_frac=MERGE_FRAC,
                           filter_len_px=31, flank_px=4.5, smooth_px=SMOOTH_PX, fan_max_deg=FAN_MAX_DEG, fan_step_deg=FAN_STEP_DEG,
                           fan_tol_px=FAN_TOL_PX, cap_exclude_px=CAP_EXCLUDE_PX))
    json.dump(out, open(OUT, 'w'))
    np.savez_compressed(OUT_NPZ, B=Bs, N=Nn, rings=np.array(rings), merged=np.array(merged), dtoe=dtoe)
    print('chains:', sorted([(c['rank'], c['part'], c['n_points']) for c in chains]))
    ks = sorted(set(t['K'] for t in toe_samples))
    print('toe samples: nearest-inside-line ranks present:', ks, ' counts', {k: sum(1 for t in toe_samples if t['K'] == k) for k in ks})


if __name__ == '__main__':
    main()

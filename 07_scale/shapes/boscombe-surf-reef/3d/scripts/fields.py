"""Boscombe Surf Reef - height fields for the 3D model (called by ../build_3d.py).

Everything here is derived from two sources only:
  * shape.json  (canonical plan polygon, verified 2026-10-05)  -> reef toe polygon
  * Rendle & Davidson (2012) Fig. 9 left map (April 2011 DGPS bathymetry, colour bar)  -> depth grid (survey_read2.py)
plus the water-level constants in CONSTANTS below.  No Gemini data.

Vertical datums (see METHODS_3D.md, equations M3-M5):
    z_survey  : metres, '+' up, in the survey plot's own datum, ASSUMED Chart Datum (ACD) - assumption A3
    z_MSL     : model z.   z_MSL = z_survey + SURVEY_ZERO_IN_MSL   with SURVEY_ZERO_IN_MSL = -(MSL above CD) = -1.40
"""
import numpy as np
from scipy import ndimage as ndi
from scipy.interpolate import RBFInterpolator
from matplotlib.path import Path as MPath

from canon import CAN_POLY, can2osgb
import survey_read2 as sr

# ---------------------------------------------------------------- constants (each has a source line in SOURCES_3D.md / METHODS_3D.md)
MSL_ABOVE_CD = 1.40                  # m ; NTSLF 'Chart datum and ordnance datum': Bournemouth -1.40 m (CD below ODN); ODN ~ MSL
SURVEY_ZERO_IN_MSL = -MSL_ABOVE_CD   # z_MSL = z_survey + this
ALT_DATUM_SHIFT = +MSL_ABOVE_CD      # switch 'survey zero = ODN ~ MSL': z_MSL(alt) = z_MSL(default) + 1.40
TIDES_ACD = {                        # Mead et al. (2010) Table 1, metres above chart datum
    "HAT": 2.59, "MHWS": 2.21, "MHWN": 1.67, "MLWN": 1.17, "MLWS": 0.45, "LAT": -0.06,
}
DESIGN_CREST_ACD = 0.5               # Mead et al. (2010) p.2
SLOPE_RUN_PER_RISE = 3.0             # idealised flank (A6): SW flank of the Fig. 9 section, 2 m rise over 6-8 m = 1:3 .. 1:4 (steepest 2 m window 1:1.5)
POLY_RELIEF_LEVEL = 1.0              # m above ambient seabed at which the satellite outline lies (validated, IoU 0.90)

# domain of the exported seabed grid (canonical metres)
SEABED = dict(x0=-160.0, x1=160.0, y0=0.0, y1=380.0, step=2.0)
FINE = 1.0                           # working grid (m)


def _nconv(a, valid, sigma):
    """Normalised (nan-aware) gaussian smoothing."""
    v = np.where(valid, a, 0.0)
    num = ndi.gaussian_filter(v, sigma)
    den = ndi.gaussian_filter(valid.astype(float), sigma)
    return np.where(den > 1e-6, num / np.maximum(den, 1e-6), np.nan)


def survey_on_canonical(step=FINE):
    """Fig. 9 colour-read depth sampled on the canonical grid (no shift).  Returns xs, ys, Z (nan outside the plotted area)."""
    xs = np.arange(SEABED["x0"], SEABED["x1"] + 1e-6, step)
    ys = np.arange(SEABED["y0"], SEABED["y1"] + 1e-6, step)
    XX, YY = np.meshgrid(xs, ys)
    E, N = can2osgb(XX.ravel(), YY.ravel())
    PX, PY = sr.osgb2px(E, N)
    val, dist, still, take = sr.depth_image()
    v = np.nan_to_num(val, nan=0.0); w = np.isfinite(val).astype(float)
    vs = ndi.map_coordinates(v, [PY, PX], order=1, mode="nearest")
    ws = ndi.map_coordinates(w, [PY, PX], order=1, mode="nearest")
    Z = np.where(ws > 0.999, vs / np.maximum(ws, 1e-9), np.nan).reshape(YY.shape)
    return xs, ys, Z


def build(step_out=SEABED["step"]):
    xs, ys, Zraw = survey_on_canonical(FINE)
    XX, YY = np.meshgrid(xs, ys)
    ok0 = np.isfinite(Zraw)
    # valid area: fill 1-cell holes (white spot in the plot), erode 2 cells at the rim (anti-aliased border pixels)
    filled = ndi.binary_fill_holes(ndi.binary_closing(ok0, iterations=3))
    valid = ndi.binary_erosion(filled, iterations=2)
    Zs = _nconv(Zraw, ok0, 1.0)                      # gaussian sigma 1 m, nan-aware
    Zs = np.where(valid, Zs, np.nan)
    # fill remaining nan inside valid by nearest
    bad = valid & ~np.isfinite(Zs)
    if bad.any():
        idx = ndi.distance_transform_edt(~np.isfinite(Zs) | ~valid, return_distances=False, return_indices=True)
        Zs = np.where(bad, Zs[tuple(idx)], Zs)

    poly = MPath(CAN_POLY)
    inside = poly.contains_points(np.c_[XX.ravel(), YY.ravel()]).reshape(XX.shape)

    # ---- first pass: relief against an order-2 polynomial, to find the reef footprint in the survey
    def design(x, y):
        xn = x / 100.0; yn = (y - 200.0) / 100.0
        return np.stack([np.ones_like(xn), xn, yn, yn ** 2, xn * yn, xn ** 2], -1)
    far = valid & (ndi.distance_transform_edt(~inside) > 35)
    for _ in range(3):
        c, *_ = np.linalg.lstsq(design(XX[far], YY[far]), Zs[far], rcond=None)
        poly_fit = design(XX, YY) @ c
        R0 = Zs - poly_fit
        core = valid & (R0 > 0.5)
        core = ndi.binary_opening(core, iterations=2)
        lab, n = ndi.label(core); sizes = ndi.sum(core, lab, range(1, n + 1)); core = lab == (1 + np.argmax(sizes))
        far = valid & (ndi.distance_transform_edt(~core) > 25)
    reef_mask = ndi.binary_dilation(core | inside, iterations=5)          # cells whose seabed is replaced

    # ---- ambient seabed: thin-plate spline through survey cells outside the reef mask (decimated 6 m)
    d_rim = ndi.distance_transform_edt(valid)                              # distance to the survey rim (inside)
    sel = valid & ~reef_mask & (d_rim > 3)
    ii = np.zeros_like(sel); ii[::6, ::6] = True
    pts = np.c_[XX[sel & ii], YY[sel & ii]]; vals = Zs[sel & ii]
    tps = RBFInterpolator(pts, vals, kernel="thin_plate_spline", smoothing=2.0)
    def eval_tps(X, Y, chunk=4000):
        P = np.c_[X.ravel(), Y.ravel()]
        out = np.empty(len(P))
        for i in range(0, len(P), chunk):
            out[i:i + chunk] = tps(P[i:i + chunk])
        return out.reshape(X.shape)
    S_tps = eval_tps(XX, YY)
    res_fit = (Zs - S_tps)[sel]
    fit_rms = float(np.sqrt(np.mean(res_fit ** 2)))

    # ---- seabed estimate S on the fine grid
    resid = np.where(sel, Zs - S_tps, np.nan)
    # residual inside the reef hole: nearest ring residual decayed with distance
    idx, dd = None, None
    dmask, ind = ndi.distance_transform_edt(reef_mask | ~valid, return_indices=True)
    nearest_res = np.where(np.isfinite(resid), resid, 0.0)[tuple(ind)]
    hole_res = nearest_res * np.exp(-dmask / 8.0)
    w_valid = np.clip((d_rim - 2) / 8.0, 0.0, 1.0)                         # survey weight rises 0->1 over 8 m from the rim
    S = np.where(valid & ~reef_mask, w_valid * Zs + (1 - w_valid) * S_tps,
                 np.where(valid & reef_mask, S_tps + hole_res * (w_valid), S_tps))
    # a gaussian smoothing of the seam (sigma 1.5 m) keeps the blend continuous
    S = ndi.gaussian_filter(S, 1.0)
    # mask code for the seabed grid: 0 survey value, 1 extrapolated (outside the plotted survey), 2 interpolated under the reef
    code = np.zeros(S.shape, np.uint8)
    code[~valid] = 1
    code[valid & reef_mask] = 2
    code[(~valid) & reef_mask] = 2

    relief = np.where(valid, Zs - S, 0.0)
    relief = np.where(reef_mask, np.maximum(relief, 0.0), 0.0)
    Zreef = S + relief                                                      # reef surface (survey datum)

    # ---- idealised intact reef (loft of the verified outline): relief = clip(1 + phi/m, 0, Hc)
    din = ndi.distance_transform_edt(inside)
    dout = ndi.distance_transform_edt(~inside)
    phi = np.where(inside, din, -dout)                                      # + inside, - outside (metres, ~cell centres)
    Hc = np.maximum(DESIGN_CREST_ACD - S, 0.0)
    ideal_rel = np.clip(POLY_RELIEF_LEVEL + phi / SLOPE_RUN_PER_RISE, 0.0, Hc)
    near = ndi.binary_dilation(inside, iterations=int(POLY_RELIEF_LEVEL * SLOPE_RUN_PER_RISE) + 2)
    ideal_rel = np.where(near, ideal_rel, 0.0)
    ideal_ramp = np.where(near, np.clip(POLY_RELIEF_LEVEL + phi / SLOPE_RUN_PER_RISE, 0.0, 30.0), 0.0)   # relief before the crest cap (used by the viewer's datum switch)

    return dict(xs=xs, ys=ys, XX=XX, YY=YY, Zs=Zs, Zraw=Zraw, valid=valid, S=S, code=code, relief=relief, Zreef=Zreef,
                reef_mask=reef_mask, core=core, inside=inside, ideal_rel=ideal_rel, ideal_ramp=ideal_ramp, S_tps=S_tps, fit_rms=fit_rms,
                R0=R0, poly_fit=poly_fit)


if __name__ == "__main__":
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "fields_check.png"
    F = build()
    print("TPS fit rms (survey cells outside reef):", round(F["fit_rms"], 3), "m")
    print("valid cells", F["valid"].sum(), " reef mask cells", F["reef_mask"].sum(), " relief>1 area", (F["relief"] > 1).sum(), "m2")
    print("S range", np.nanmin(F["S"]), np.nanmax(F["S"]))
    xs, ys = F["xs"], F["ys"]
    ext = [xs[0], xs[-1], ys[0], ys[-1]]
    fig, ax = plt.subplots(2, 3, figsize=(20, 14))
    kw = dict(origin="lower", extent=ext, cmap="jet", vmin=-5.3, vmax=1.0)
    ax[0, 0].imshow(F["Zs"], **kw); ax[0, 0].set_title("survey Zs (ACD)")
    ax[0, 1].imshow(F["S"], **kw); ax[0, 1].set_title("seabed estimate S (survey + TPS)")
    ax[0, 2].imshow(F["Zreef"], **kw); ax[0, 2].set_title("Zreef = S + relief")
    ax[1, 0].imshow(F["code"], origin="lower", extent=ext); ax[1, 0].set_title("code 0 survey / 1 extrap / 2 under reef")
    ax[1, 1].imshow(F["relief"], origin="lower", extent=ext, cmap="magma"); ax[1, 1].set_title("relief")
    ax[1, 2].imshow(F["ideal_rel"], origin="lower", extent=ext, cmap="magma"); ax[1, 2].set_title("idealised relief")
    for a in ax.ravel():
        a.plot(*np.vstack([CAN_POLY, CAN_POLY[:1]]).T, "w", lw=1); a.set_aspect("equal")
    plt.tight_layout(); plt.savefig(out, dpi=55)
    np.savez_compressed(out.replace(".png", ".npz"), **{k: F[k] for k in ("xs", "ys", "Zs", "S", "code", "relief", "Zreef", "ideal_rel", "valid")})

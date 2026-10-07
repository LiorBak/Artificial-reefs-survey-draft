"""Boscombe Surf Reef - EXTENSION of the seabed grid (re-check run 2026-10-07, called by ../build_3d.py).

Lior's request: make the 3D larger so the shoreline is visible.  The original grid was x -160..160, y 0..380 m (the Fig. 9 survey
covers y ~100..312 m only; y < 100 was a spline extrapolation that never reached the beach).  This module only ADDS rows and
only changes cells that carry code 1 (no survey, not under the reef) at y < ~80 m; every survey cell (code 0) and every cell under the
reef (code 2), and therefore the whole reef surface, is left exactly as built.

  shoreward  y -66 .. 0     CCO beach profiles (Southeast Regional Coastal Monitoring Programme / Channel Coastal Observatory),
                             survey of CCO_DATE, Elevation_OD (= m ODN), interpolated alongshore between the profile lines   -> code 3
  transition y 0 .. y_end+L  base seabed (thin-plate-spline extrapolation of the Fig. 9 survey, unchanged) + the residual
                             (CCO - base) at the seaward end of each profile line, decaying to 0 over L = 40 m                -> code 3 (data, y <= y_end) / 4 (decay)
  offshore   y 380 .. 650    z(y) = z_model(x, 380) - 0.0141 (y - 380)  (EMODnet DTM 2024 slope, REPORT 9.1), +-1.2 m          -> code 5

Datum: CCO Elevation_OD is metres above Ordnance Datum Newlyn.  The model zero is MSL and ODN ~ MSL (assumption A4, +-0.1 m), so
z_MSL = z_ODN.  Heights taken from the Fig. 9 survey are z_MSL = z_ACD - 1.40 (E6).

Datum weight (for the viewer's 'survey zero = ODN' switch): dw = fraction of the +1.40 m switch that applies to the cell.  The CCO beach is
referenced to ODN independently of the Fig. 9 plot, so dw = 0 on it and rises to 1 across the transition.
"""
import json
import numpy as np
from pathlib import Path

from cco_load import load, SRC

CCO_DATE = "2010-04-20"          # nearest survey date to the 2009 as-built state for which ALL 11 profile lines near the reef exist
CCO_DATE_CHECK = ["2009-09-22", "2009-11-30", "2011-03-23", "2011-09-15"]   # other dates used only for the variability check
BEACH_Y0 = -66.0                 # top of the grid (back of the beach, z about +3.3 m ODN)
OFFSHORE_Y1 = 650.0
EMODNET_SLOPE = 0.0141           # m per m, EMODnet DTM 2024 REPORT 9.1 (+-0.0010)
EMODNET_UNC = 1.2                # m (1 sd; Navionics z16 check, 11 soundings: rms 1.2 m; REPORT 9.1 had +-1.0 m)
BLEND_L = 40.0                   # m, decay length of the CCO offset beyond the seaward end of each profile line
CELL = 2.0
ALL_LINES = ["5f00424", "5f00424A", "5f00425", "5f00425A", "5f00426", "5f00426A", "5f00427", "5f00427A", "5f00428", "5f00428A", "5f00429"]


def smoothstep(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def _line(pid, date):
    p = load(pid, date)
    o = np.argsort(p["y"])
    y, x, z = p["y"][o], p["x"][o], p["z"][o]
    # merge duplicate y (keep the mean) so that np.interp stays well defined
    yu, inv = np.unique(np.round(y, 3), return_inverse=True)
    zu = np.bincount(inv, weights=z) / np.bincount(inv)
    xu = np.bincount(inv, weights=x) / np.bincount(inv)
    return dict(pid=pid, date=date, y=yu, x=xu, z=zu, n=len(y), ch_min=float(p["ch"].min()), ch_max=float(p["ch"].max()),
                y_end=float(yu[-1]), z_end=float(zu[-1]), y_start=float(yu[0]), z_start=float(zu[0]))


def beach_lines(date=CCO_DATE):
    L = [_line(pid, date) for pid in ALL_LINES]
    L.sort(key=lambda d: np.interp(0.0, d["y"], d["x"]))
    return L


def _at(l, y):
    """x position and z of a profile line at canonical y (clamped to the first / last measured point)."""
    return float(np.interp(y, l["y"], l["x"])), float(np.interp(y, l["y"], l["z"]))


def extend(xs, base_msl, code, lines=None, ys_new=None):
    """xs: 2 m columns (-160..160); base_msl: (ny0, nx) seabed z (MSL) of the ORIGINAL grid y = 0..380 step 2; code: its codes (uint8).
    Returns dict with ys, z (MSL, m), code, dw (0..1), y_end_by_x, plus per-line diagnostics."""
    lines = lines or beach_lines()
    ny0 = base_msl.shape[0]
    ys0 = np.arange(ny0) * CELL                                   # 0..380
    ys_beach = np.arange(BEACH_Y0, 0.0, CELL)                     # -66 .. -2
    ys_off = np.arange(380.0 + CELL, OFFSHORE_Y1 + 1e-6, CELL)    # 382 .. 650
    nx = len(xs)

    # ---- diagnostics at the seaward end of every line (offset CCO - base seabed)
    diag = []
    for l in lines:
        xe, ze = _at(l, l["y_end"])
        j = int(np.clip(round(l["y_end"] / CELL), 0, ny0 - 1))
        b = float(np.interp(xe, xs, base_msl[j]))
        l["delta"] = ze - b
        diag.append(dict(pid=l["pid"], date=l["date"], n=l["n"], y_start=round(l["y_start"], 1), y_end=round(l["y_end"], 1), z_end_odn=round(l["z_end"], 3),
                         base_z_msl_at_end=round(b, 3), delta_cco_minus_base=round(l["delta"], 3), x_at_y0=round(float(np.interp(0.0, l["y"], l["x"])), 1)))

    # ---- shoreward rows (y < 0): CCO surface only
    z_beach = np.zeros((len(ys_beach), nx));
    for r, y in enumerate(ys_beach):
        xl = np.array([_at(l, y)[0] for l in lines]); zl = np.array([_at(l, y)[1] for l in lines])
        z_beach[r] = np.interp(xs, xl, zl)

    # ---- rows y = 0..380: base + residual field (only on code-1 cells)
    z_mid = base_msl.copy(); dw_mid = np.ones_like(base_msl); code_mid = code.copy().astype(np.uint8)
    y_end_x = np.zeros(nx);
    xe_lines = np.array([np.interp(0.0, l["y"], l["x"]) for l in lines])
    for r, y in enumerate(ys0):
        xl = np.array([_at(l, y)[0] for l in lines])
        res = []; wc = []
        for l in lines:
            if y <= l["y_end"]:
                x_l, z_l = _at(l, y)
                res.append(z_l - float(np.interp(x_l, xs, base_msl[r]))); wc.append(1.0)
            else:
                w = 1.0 - smoothstep((y - l["y_end"]) / BLEND_L)
                res.append(l["delta"] * w); wc.append(w)
        R = np.interp(xs, xl, np.array(res)); W = np.interp(xs, xl, np.array(wc))
        ye = np.interp(xs, xe_lines, [l["y_end"] for l in lines])
        if r == 0:
            y_end_x = ye
        m = code[r] == 1
        z_mid[r] = np.where(m, base_msl[r] + R, base_msl[r])
        dw_mid[r] = np.where(m, 1.0 - W, 1.0)
        cc = code[r].copy()
        cc = np.where(m & (y <= ye), 3, cc)
        cc = np.where(m & (y > ye) & (W > 0.02), 4, cc)
        code_mid[r] = cc.astype(np.uint8)

    # ---- offshore rows: EMODnet slope from the last row
    z380 = base_msl[-1]
    z_off = np.array([z380 - EMODNET_SLOPE * (y - 380.0) for y in ys_off])

    ys = np.concatenate([ys_beach, ys0, ys_off])
    z = np.vstack([z_beach, z_mid, z_off])
    cd = np.vstack([np.full((len(ys_beach), nx), 3, np.uint8), code_mid, np.full((len(ys_off), nx), 5, np.uint8)])
    dw = np.vstack([np.zeros((len(ys_beach), nx)), dw_mid, np.ones((len(ys_off), nx))])
    return dict(ys=ys, z=z, code=cd, dw=dw, y_end_by_x=y_end_x, diag=diag, lines=lines)


def beach_validation(lines_main, base_fn=None):
    """Variability of the beach between survey dates (same lines): rms of z differences in y -50..20 m between CCO_DATE and other dates."""
    out = []
    ygrid = np.arange(-50.0, 20.1, 2.0)
    for d2 in CCO_DATE_CHECK:
        diffs = []
        n_lines = 0
        for l in lines_main:
            try:
                l2 = _line(l["pid"], d2)
            except Exception:
                continue
            if l2["y_end"] < 15:
                continue
            ok = ygrid <= min(l["y_end"], l2["y_end"])
            if ok.sum() < 5:
                continue
            d = np.interp(ygrid[ok], l2["y"], l2["z"]) - np.interp(ygrid[ok], l["y"], l["z"])
            diffs.append(d); n_lines += 1
        if diffs:
            dd = np.concatenate(diffs)
            out.append(dict(date=d2, lines=n_lines, mean=round(float(dd.mean()), 3), sd=round(float(dd.std()), 3), rms=round(float(np.sqrt((dd ** 2).mean())), 3),
                            p5_p95=[round(float(np.percentile(dd, 5)), 2), round(float(np.percentile(dd, 95)), 2)]))
    return out

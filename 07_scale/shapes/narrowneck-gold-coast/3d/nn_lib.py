"""nn_lib.py - shared helpers for the Narrowneck 3D build (grids, design surface, seabed). Frame: shape.json canonical (x alongshore, bearing 356.2;
y offshore, bearing 86.2), metres; z in m AHD inside the library (converted to MSL by build_3d.py: z_MSL = z_AHD - 0.12)."""
import json, os
import numpy as np
from shapely.geometry import Polygon
from shapely import contains_xy
from scipy import ndimage as ndi
from scipy.interpolate import PchipInterpolator
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = os.path.dirname(HERE); SRC = os.path.join(HERE, 'src')
GX0, GX1, GY0, GY1, GSTEP = -110.0, 110.0, 190.0, 420.0, 1.0       # reef grid (m)
Z_CREST = -2.5          # design crest, m AHD
Z_ENV = -6.0            # design envelope contour, m AHD
FLANK = 0.67            # side slope of the container mound: 1.5 H : 1 V (estimated), m of height per m inward from the footprint edge


def grid():
    xs = np.arange(GX0, GX1 + 1e-9, GSTEP); ys = np.arange(GY0, GY1 + 1e-9, GSTEP); X, Y = np.meshgrid(xs, ys); return xs, ys, X, Y


def mask_of(polys, X, Y):
    m = np.zeros(X.shape, bool)
    for p in polys: m |= contains_xy(p, X, Y)
    return m


def design_top(loops, env, X, Y, gamma=1.0):
    """Design crest surface (m AHD): -2.5 inside the crest loops, falling to -6 at the envelope boundary; f = d_in/(d_in+d_out)."""
    min_ = mask_of(loops, X, Y); men = mask_of(env, X, Y) | min_
    d_in = ndi.distance_transform_edt(~min_) * GSTEP
    d_out = ndi.distance_transform_edt(men) * GSTEP
    f = np.where(men, d_in / np.maximum(d_in + d_out, 1e-9), 1.0) ** gamma
    return Z_CREST + (Z_ENV - Z_CREST) * np.clip(f, 0, 1), men


def seabed_profile(mb):
    """Alongshore-uniform bed profile b(y) (m AHD): control points, PCHIP. Window part = multibeam bed (median over x, smoothed)."""
    ys = mb['ys']; B = mb['bed']; med = np.array([np.nanmedian(r) if np.isfinite(r).sum() > 20 else np.nan for r in B])
    ok = np.isfinite(med); yw = ys[ok][::10]; zw = ndi.gaussian_filter1d(med[ok], 6)[::10]
    yw = yw[(yw >= 215) & (yw <= 365)]; zw = zw[:len(yw)] if False else np.interp(yw, ys[ok], ndi.gaussian_filter1d(med[ok], 6))
    ctrl = [(-40, 1.2), (0, 0.0), (100, -1.8), (190, -2.1)] + list(zip(yw, zw)) + [(402, -7.76), (411, -8.76), (474, -9.76), (514, -10.76), (540, -11.0)]
    ctrl.sort(); y = np.array([c[0] for c in ctrl]); z = np.array([c[1] for c in ctrl])
    return PchipInterpolator(y, z), ctrl

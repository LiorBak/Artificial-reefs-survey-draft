"""Resample the colour-read April 2011 survey depth image onto the canonical 1 m grid (no registration shift yet)."""
import numpy as np
from scipy import ndimage as ndi
from canon import can2osgb
from survey_read import depth_image, osgb2px
from pathlib import Path

def build(xmin=-160, xmax=160, ymin=40, ymax=380, step=1.0):
    val, dist, dark = depth_image()
    xs = np.arange(xmin, xmax + 1e-6, step); ys = np.arange(ymin, ymax + 1e-6, step)
    XX, YY = np.meshgrid(xs, ys)               # shape (ny, nx)
    E, N = can2osgb(XX.ravel(), YY.ravel())
    PX, PY = osgb2px(E, N)
    # nan-aware bilinear sampling: sample value*valid and valid separately
    v = np.nan_to_num(val, nan=0.0); w = np.isfinite(val).astype(float)
    # light median smoothing of the colour-quantisation noise (3x3) before sampling
    vs = ndi.map_coordinates(v, [PY, PX], order=1, mode="nearest")
    ws = ndi.map_coordinates(w, [PY, PX], order=1, mode="nearest")
    Z = np.where(ws > 0.999, vs / np.maximum(ws, 1e-9), np.nan).reshape(YY.shape)
    return xs, ys, Z

if __name__ == "__main__":
    xs, ys, Z = build()
    np.savez(Path(__file__).with_name("_survey_can_1m.npz"), xs=xs, ys=ys, Z=Z)
    ok = np.isfinite(Z)
    print("grid", Z.shape, "valid cells", ok.sum(), "x range", xs[ok.any(axis=0)][[0, -1]], "y range", ys[ok.any(axis=1)][[0, -1]])
    print("z min/max", np.nanmin(Z), np.nanmax(Z))

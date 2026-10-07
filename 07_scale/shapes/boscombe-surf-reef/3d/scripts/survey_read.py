"""Read the April 2011 DGPS bathymetry plot (Rendle & Davidson 2012 Fig. 9, left panel) as a depth grid.

Method: the plot is a continuous 'jet' colour field. The colour bar (right of the right panel) gives colour -> depth;
every pixel of the left panel is mapped to the nearest colour-bar colour (RGB distance). Axes: gridlines read in the
image (E 411400 at x=147.3 px, E 411550 at x=433.5; N 91000 at y=39.0 px, N 90820 at y=235.3).
Depth values are metres, '+' up, in the plot's own vertical datum (taken here as Chart Datum, see SOURCES_3D.md).
"""
import numpy as np, cv2
from PIL import Image
from pathlib import Path
from canon import ROOT

SRC = ROOT / "src" / "rendle_davidson_2012_fig9_bathymetry_apr2011_native.png"
RGB = np.array(Image.open(SRC).convert("RGB"))
H, W, _ = RGB.shape

# --- colour bar: x = 937..943, y = 20..255 ; tick labels 0,-1,..,-5 at y = 55,93,131,168,206,244
TICK_Y = np.array([55.0, 93.0, 131.0, 168.0, 206.0, 244.0]); TICK_V = np.array([0, -1, -2, -3, -4, -5.0])
_slope, _icpt = np.polyfit(TICK_Y, TICK_V, 1)           # value = slope*y + icpt   (slope ~ -0.0265 m/px)
def bar_value(y):
    return _slope * y + _icpt
BAR_Y = np.arange(20, 256)
BAR_RGB = RGB[BAR_Y][:, 937:944, :].astype(float).mean(axis=1)
BAR_VAL = bar_value(BAR_Y + 0.0)

# --- axes
X_E0, E0, PXM_X = 147.3, 411400.0, 1.9080
Y_N0, N0, PXM_Y = 39.0, 91000.0, 1.0909
def px2osgb(X, Y):
    return E0 + (np.asarray(X) - X_E0) / PXM_X, N0 - (np.asarray(Y) - Y_N0) / PXM_Y
def osgb2px(E, N):
    return X_E0 + (np.asarray(E) - E0) * PXM_X, Y_N0 + (N0 - np.asarray(N)) * PXM_Y

PANEL = (73, 20, 478, 255)   # x0,y0,x1,y1 of the plot area of the left panel (inside the axes box)

def depth_image(max_dist=70.0):
    img = RGB.astype(float)
    # invalid masks
    dark = (img.sum(axis=2) < 200)                       # black survey line, text
    # inpaint dark pixels (survey line) from neighbours
    m8 = cv2.dilate(dark.astype(np.uint8), np.ones((3, 3), np.uint8))
    inp = cv2.inpaint(RGB, m8, 4, cv2.INPAINT_TELEA).astype(float)
    # nearest bar colour
    flat = inp.reshape(-1, 3)
    d2 = ((flat[:, None, :] - BAR_RGB[None, :, :]) ** 2).sum(axis=2)
    idx = d2.argmin(axis=1)
    dist = np.sqrt(d2[np.arange(len(flat)), idx]).reshape(H, W)
    val = BAR_VAL[idx].reshape(H, W)
    val[dist > max_dist] = np.nan
    x0, y0, x1, y1 = PANEL
    mask = np.zeros((H, W), bool); mask[y0:y1, x0:x1] = True
    val[~mask] = np.nan
    return val, dist, dark

if __name__ == "__main__":
    val, dist, dark = depth_image()
    print("bar value range", BAR_VAL.min(), BAR_VAL.max(), "slope m/px", _slope)
    print("valid px", np.isfinite(val).sum(), "min/max", np.nanmin(val), np.nanmax(val))
    np.save(Path(__file__).with_name("_survey_depth_native.npy"), val)

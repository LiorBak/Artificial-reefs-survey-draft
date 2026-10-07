"""Second-generation read of Rendle & Davidson (2012) Fig. 9 (April 2011 DGPS bathymetry plot).
Improvement on survey_read.py: the thick black section line drawn across the LEFT map (and a different one across the RIGHT map)
hid pixels. The right map is the same surface offset by (+469 px, -1 px) (template match, SQDIFF 0.028), so pixels hidden by the
left line are taken from the right map where those are not hidden; remaining dark pixels are inpainted (cv2 TELEA, r=4).
Colour -> depth: every pixel -> nearest colour of the printed colour bar (RGB distance), bar ticks 0..-5 read at y=55..244.
"""
import numpy as np, cv2
from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]                      # .../shapes/boscombe-surf-reef
SRC = ROOT / "src" / "rendle_davidson_2012_fig9_bathymetry_apr2011_native.png"
RGB = np.array(Image.open(SRC).convert("RGB"))
H, W, _ = RGB.shape

TICK_Y = np.array([55.0, 93.0, 131.0, 168.0, 206.0, 244.0]); TICK_V = np.array([0, -1, -2, -3, -4, -5.0])
_slope, _icpt = np.polyfit(TICK_Y, TICK_V, 1)
def bar_value(y): return _slope * np.asarray(y, float) + _icpt
BAR_Y = np.arange(20, 256)
BAR_RGB = RGB[BAR_Y][:, 937:944, :].astype(float).mean(axis=1)
BAR_VAL = bar_value(BAR_Y)

# axes of the LEFT map (native px)
X_E0, E0, PXM_X = 147.3, 411400.0, 1.9080
Y_N0, N0, PXM_Y = 39.0, 91000.0, 1.0909
def px2osgb(X, Y): return E0 + (np.asarray(X) - X_E0) / PXM_X, N0 - (np.asarray(Y) - Y_N0) / PXM_Y
def osgb2px(E, N): return X_E0 + (np.asarray(E) - E0) * PXM_X, Y_N0 + (N0 - np.asarray(N)) * PXM_Y
PANEL = (73, 20, 478, 255)
RIGHT_DX, RIGHT_DY = 469, -1

def dark_mask(img):
    # black section line / text = ALL channels low. (The old test sum<200 also caught the dark-red (103,10,15) and
    # dark-blue (4,2,139) ends of the jet colour bar, i.e. real crest / deep-water data.)
    return (img.max(axis=2) < 90)

def merged_rgb():
    img = RGB.copy()
    dkL = cv2.dilate(dark_mask(RGB).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    shifted = np.zeros_like(RGB); shifted[:] = 255
    ys, xs = np.mgrid[0:H, 0:W]
    xr = xs + RIGHT_DX; yr = ys + RIGHT_DY
    okr = (xr >= 0) & (xr < W) & (yr >= 0) & (yr < H)
    shifted[ys[okr], xs[okr]] = RGB[yr[okr], xr[okr]]
    dkR = np.zeros((H, W), bool)
    dkR[ys[okr], xs[okr]] = cv2.dilate(dark_mask(RGB).astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)[yr[okr], xr[okr]]
    take = dkL & ~dkR & okr
    img[take] = shifted[take]
    still = dkL & ~take
    return img, still, take

def depth_image(max_dist=70.0):
    img, still, take = merged_rgb()
    m8 = cv2.dilate(still.astype(np.uint8), np.ones((3, 3), np.uint8))
    inp = cv2.inpaint(img, m8, 4, cv2.INPAINT_TELEA).astype(float)
    flat = inp.reshape(-1, 3)
    d2 = ((flat[:, None, :] - BAR_RGB[None, :, :]) ** 2).sum(axis=2)
    idx = d2.argmin(axis=1)
    dist = np.sqrt(d2[np.arange(len(flat)), idx]).reshape(H, W)
    val = BAR_VAL[idx].reshape(H, W)
    val[dist > max_dist] = np.nan
    x0, y0, x1, y1 = PANEL
    mask = np.zeros((H, W), bool); mask[y0:y1, x0:x1] = True
    val[~mask] = np.nan
    return val, dist, still, take

if __name__ == "__main__":
    val, dist, still, take = depth_image()
    L = (slice(20, 255), slice(73, 478))
    print("valid px", np.isfinite(val).sum(), "min/max", np.nanmin(val), np.nanmax(val), "px taken from right map", take[L].sum(), "px inpainted", still[L].sum())
    print("colour distance to bar: median %.1f  95th %.1f" % (np.nanmedian(dist[L][np.isfinite(val[L])]), np.nanpercentile(dist[L][np.isfinite(val[L])], 95)))
    np.save(HERE / "_survey_depth_native2.npy", val)

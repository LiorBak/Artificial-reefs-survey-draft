"""cables-reef-wa: measured pre-construction seabed (replaces the fitted plane D0 + 1:30 of the first model).
Sources: DoT WA singlebeam survey FR19980330_Reef_Single (30 Mar 1998, pre-construction; AHD) inside its coverage; DoT 'Perth_5m' composite surface
(AHD, 5 m cells) elsewhere, shifted by the mean raster-minus-sounding difference over the 1998 soundings more than 120 m from the reef (the composite contains the reef itself).
Method: 1 m world grid (MGA50 metres relative to the anchor); survey points averaged per 1 m cell, linear-interpolated (LinearNDInterpolator) where the
nearest sounding is < 8 m; raster bilinear elsewhere; whole field Gaussian-smoothed sigma 2 m (removes sounding-line stripes); then re-sampled into the
canonical frame (x north, y west of shape.json) by the georeference in georef.json and saved as ../3d/bed_measured_canonical.npz (z in m AHD, 1 m grid).
numpy/scipy only."""
import json, numpy as np
from scipy.interpolate import LinearNDInterpolator
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
HERE = __file__.rsplit('/', 1)[0]; S = HERE + '/../src/bathymetry/'
G = json.load(open(HERE + '/georef.json'))['transform']; E0, N0, TH = G['anchor_E_MGA50_GDA94'], G['anchor_N_MGA50_GDA94'], np.radians(G['theta_ccw_deg']); XC, YC = G['anchor_canonical_xy_m']
R = 330; step = 1.0; n = int(2 * R / step) + 1
gx = -R + step * np.arange(n); EE, NN = np.meshgrid(gx, gx)                      # E right, N up (rows = N ascending)
pre = np.loadtxt(S + 'FR_selected/FR19980330_Reef_Single.txt', usecols=(0, 1, 2)); pre[:, 0] -= E0; pre[:, 1] -= N0
pre = pre[(abs(pre[:, 0]) < R + 20) & (abs(pre[:, 1]) < R + 20)]
# raster clip
z = np.load(S + 'DoT_Perth_5m_clip_reef.npz'); rz = z['z_AHD'].astype(float); rz[rz < -9000] = np.nan; xl, yt, px = float(z['x_left']), float(z['y_top']), float(z['pixel'])
def raster_at(E, N):
    c = (E + E0 - xl) / px - 0.5; r = (yt - (N + N0)) / px - 0.5
    return ndi.map_coordinates(np.nan_to_num(rz, nan=-9999), [r, c], order=1, mode='nearest')
rv = raster_at(pre[:, 0], pre[:, 1])
far = np.hypot(pre[:, 0], pre[:, 1]) > 120                    # exclude the reef itself: the Perth_5m composite contains the reef (post-construction soundings merged in)
bias = float(np.mean((rv - pre[:, 2])[far])); bias_all = float(np.mean(rv - pre[:, 2]))
cell = {}
ci = np.floor((pre[:, :2] + R) / step).astype(int)
sums = np.zeros((n, n)); cnt = np.zeros((n, n))
ok = (ci >= 0).all(1) & (ci < n).all(1)
np.add.at(sums, (ci[ok, 1], ci[ok, 0]), pre[ok, 2]); np.add.at(cnt, (ci[ok, 1], ci[ok, 0]), 1)
mk = cnt > 0; pts = np.c_[EE[mk], NN[mk]]; vals = sums[mk] / cnt[mk]
f = LinearNDInterpolator(pts, vals); sv = f(EE, NN)
near = cKDTree(pre[:, :2]).query(np.c_[EE.ravel(), NN.ravel()])[0].reshape(EE.shape)
ras = raster_at(EE.ravel(), NN.ravel()).reshape(EE.shape) - bias
use_s = np.isfinite(sv) & (near < 8.0)
field = np.where(use_s, sv, ras)
field = ndi.gaussian_filter(field, 2.0)
# canonical resampling
cx = np.arange(-170.0, 170.1, 1.0); cy = np.arange(180.0, 430.1, 1.0); XX, YY = np.meshgrid(cx, cy)      # x north, y west
Ec = -(YY - YC); Nc = (XX - XC)
c, s = np.cos(TH), np.sin(TH)
Ew = c * Ec - s * Nc; Nw = s * Ec + c * Nc
rr = (Nw + R) / step; cc = (Ew + R) / step
bed = ndi.map_coordinates(field, [rr, cc], order=1, mode='nearest')
src_flag = ndi.map_coordinates(use_s.astype(float), [rr, cc], order=1, mode='nearest') > 0.5
np.savez_compressed(HERE + '/../3d/bed_measured_canonical.npz', x=cx, y=cy, z_AHD=bed.astype('float32'), from_survey=src_flag)
res = {"raster_minus_sounding_bias_m": round(bias, 3), "raster_minus_sounding_bias_all_points_m": round(bias_all, 3), "share_canonical_grid_from_1998_survey": round(float(src_flag.mean()), 3),
       "bed_AHD_at_anchor": round(float(bed[np.argmin(abs(cy - YC)), np.argmin(abs(cx - XC))]), 2),
       "smoothing_sigma_m": 2.0, "n_1998_soundings_used": int(len(pre))}
json.dump(res, open(HERE + '/bed_measured.json', 'w'), indent=1); print(res)

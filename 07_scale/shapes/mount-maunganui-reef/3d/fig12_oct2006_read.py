"""fig12_oct2006_read.py (2026-10-07) - read the colour-coded bathymetry of Mead, Black & Moores (2007) Fig 12 top
(October 2006 survey of the UNFINISHED reef; registry mount-maunganui-reef-img-37 (planned id; not yet registered)) with its legend.
Legend: 25 classes, depth in m (positive down), datum NOT stated. Class k=0: 0.33-0.70; k>=1: 0.71 + 0.1895 (k-1) .. 0.71 + 0.1895 k
(bin edges reconstructed from the legend labels that are legible: 0.71-0.88, 0.89-1.06, 1.09-1.27, ..., 2.23-2.41, 2.42-2.60, 4.88-5.06, 5.07-5.25;
the labels are 3-4 px tall JPEG text, so the numbers are +-0.02 m uncertain, the swatch colours are reliable).
Method: swatch colours sampled at fixed positions of the 300 dpi crop, pixels classified by nearest swatch in CIELAB, median-filtered.
Output: fig12_oct2006_read.json, annotated/mmr_mead2007_fig12a_depth_classes.png
"""
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.color import rgb2lab

R = 'C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/mount-maunganui-reef/'
im = Image.open(R + '3d/src/mmr_mead2007_fig12a_oct2006-bathymetry-survey.png').convert('RGB')
a = np.array(im).astype(float) / 255
H, W, _ = a.shape
# swatch centres in crop px (legend zoom x5 at offset (605,360))
lx = {0: 605 + 130 / 5, 1: 605 + 450 / 5, 2: 605 + 775 / 5}
rows_left = [330, 400, 465, 530, 600, 665, 740, 810, 885, 960]
rows_mid = [190, 260, 330, 400, 465, 530, 600, 665, 740, 810, 885, 960]
rows_right = [190, 260, 330]
sw = []
for col, rows in ((0, rows_left), (1, rows_mid), (2, rows_right)):
    for r in rows:
        x, y = int(round(lx[col])), int(round(360 + r / 5))
        sw.append(a[y - 1:y + 2, x - 3:x + 4].reshape(-1, 3).mean(0))
sw = np.array(sw)
K = len(sw)
lab_sw = rgb2lab(sw[None])[0]
edges = [0.33, 0.71] + [0.71 + 0.1895 * k for k in range(1, K)]
centres = [(edges[i] + edges[i + 1]) / 2 for i in range(K)]
# map area (exclude legend box x>600,y>355, the title strip and the frame)
lab_img = rgb2lab(a)
d2 = ((lab_img[:, :, None, :] - lab_sw[None, None, :, :]) ** 2).sum(-1)
cls = d2.argmin(-1); dmin = np.sqrt(d2.min(-1))
valid = dmin < 18
valid[355:, 600:] = False; valid[:12, :] = False; valid[-14:, :] = False; valid[:, :12] = False; valid[:, -12:] = False
cls_f = ndi.median_filter(cls, size=5)
depth = np.take(np.array(centres), cls_f)
depth = np.where(valid, depth, np.nan)
# reef mask = shallow classes (depth < 1.6 m) in the reef region
reef = (depth < 1.6) & np.isfinite(depth)
reef = ndi.binary_opening(reef, iterations=2)
lab, n = ndi.label(reef)
sizes = ndi.sum(reef, lab, range(1, n + 1)); reef = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 400])
# whole reef body: dilate the mask to join the bags
body = ndi.binary_closing(reef, iterations=12)
ys, xs = np.nonzero(body)
dist = ndi.distance_transform_edt(~body)
ring = (dist > 12) & (dist < 40) & np.isfinite(depth)
ring_far = (dist > 40) & (dist < 110) & np.isfinite(depth)
ring_mid = (dist > 25) & (dist < 55) & np.isfinite(depth)
out = {'classes': K, 'edges_m': [round(e, 3) for e in edges], 'swatch_rgb': np.round(sw * 255).astype(int).tolist(),
       'reef_body_bbox_px': [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
       'reef_depth_percentiles_m_P1_P5_P50': [round(float(np.nanpercentile(depth[reef], p)), 2) for p in (1, 5, 50)],
       'reef_shallowest_class_m': round(float(np.nanmin(depth[reef])), 2),
       'ring_bed_depth_percentiles_m_P10_P25_P50_P75_P90': [round(float(np.nanpercentile(depth[ring], p)), 2) for p in (10, 25, 50, 75, 90)],
       'ring_mid_25_55px_P10_P50_P90': [round(float(np.nanpercentile(depth[ring_mid], p)), 2) for p in (10, 50, 90)],
       'ring_far_40_110px_P10_P50_P90': [round(float(np.nanpercentile(depth[ring_far], p)), 2) for p in (10, 50, 90)],
       'deepest_class_in_map_m': round(float(np.nanmax(depth)), 2),
       'pixels_ring': int(ring.sum()), 'pixels_reef': int(reef.sum()),
       'note': 'datum of the legend depths is not stated in the paper; scale of the figure is not stated (no scale bar)'}
# the shallow/deep composition within 40 px of the body
out['ring_fraction_by_class_m'] = {f'{edges[i]:.2f}-{edges[i + 1]:.2f}': round(float((cls_f[ring] == i).mean()), 3) for i in range(K) if (cls_f[ring] == i).mean() > 0.02}
json.dump(out, open(R + '3d/fig12_oct2006_read.json', 'w'), indent=1)
# annotated: classified map with reef mask outline and the ring tinted
vis = np.array(im).copy()
cl = (np.zeros_like(vis)); cl[:] = 255
cmap_rgb = (sw * 255).astype(np.uint8)
cl_img = cmap_rgb[cls_f]
cl_img[~valid] = 255
b1 = ndi.binary_dilation(body, iterations=1) & ~body
b2 = ring & ~ndi.binary_erosion(ring)
cl_img[b1] = (0, 0, 0); cl_img[b2] = (255, 0, 255)
both = np.concatenate([vis, cl_img], axis=1)
Image.fromarray(both).save(R + '3d/annotated/mmr_mead2007_fig12a_depth_classes.png')
print(json.dumps({k: v for k, v in out.items() if k not in ('swatch_rgb', 'edges_m')}, indent=0))

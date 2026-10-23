"""Objective dark-patch outline of the built reef on the Esri 2026-01-20 z18 tile.
Method: green channel -> 7x7 minimum filter (suppresses glints/foam) -> gaussian sigma 3 -> threshold T
(midway between reef interior ~12-20 and ambient deep water ~40-55) -> largest connected component inside the ROI
-> fill holes -> contour -> Douglas-Peucker 3 px. Writes polygon (px) to JSON.
Usage: python -I trace_mask.py T out.json"""
import sys, json
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter, minimum_filter, label, binary_fill_holes
from skimage import measure
T = float(sys.argv[1]); out = sys.argv[2]
IMG = '../src/esri_current_2026-01-20_z18.png'
a = np.asarray(Image.open(IMG).convert('RGB')).astype(float)
s = gaussian_filter(minimum_filter(a[..., 1], 7), 3)
m = s < T
roi = np.zeros_like(m); roi[380:660, 370:760] = True
m &= roi
lab, n = label(m)
sizes = [(lab == i).sum() for i in range(1, n + 1)]
k = 1 + int(np.argmax(sizes)); m = binary_fill_holes(lab == k)
c = max(measure.find_contours(m.astype(float), 0.5), key=len)
c = measure.approximate_polygon(c, 3.0)
poly = [[round(float(x), 1), round(float(y), 1)] for y, x in c[:-1]]
json.dump(poly, open(out, 'w'))
print(T, 'area_px', int(m.sum()), 'verts', len(poly), 'bbox', m.nonzero()[1].min(), m.nonzero()[1].max(), m.nonzero()[0].min(), m.nonzero()[0].max())

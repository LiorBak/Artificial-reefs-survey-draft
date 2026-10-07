"""Segment BoPRC Fig 3 (July 2013 multibeam, native raster 900x1064) into the bag field shallower than -2.0 m CD.
Output: ../work_polys_fig3_m20_v2.json (pixel polygons in the native raster) + depth grid npy in %TEMP%/mmr.
Method: nearest-legend-colour classification (26 swatches read at x=66..84), accept dist<60; black contour lines/labels are unclassified
and filled by nearest classified pixel; mask = swatch depth > -2.0 (i.e. shallower than the -2.0 m boundary); binary closing x2,
hole filling, components > 300 px; outline = skimage find_contours(0.5) + Douglas-Peucker 1.0 px."""
import numpy as np, json, os
from PIL import Image
from scipy import ndimage as ndi
from skimage import measure
R = 'C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/mount-maunganui-reef/'
im = np.array(Image.open(R + 'src/boprc_fig3_2013_survey.png').convert('RGB')).astype(float)
seps = [619,634,649,663,678,693,708,723,737,752,767,782,796,811,826,841,855,870,885,900,915,929,944,959,974,988,1003]
cols = np.array([np.median(im[(seps[k]+seps[k+1])//2-2:(seps[k]+seps[k+1])//2+3, 66:84].reshape(-1,3), axis=0) for k in range(26)])
depth = np.array([+0.1] + [-(0.2*(k-1)+0.1) for k in range(1, 26)])   # swatch mid-depth, m CD (swatch 0 = above 0.0)
d = np.linalg.norm(im[:, :, None, :] - cols[None, None, :, :], axis=3)
dep = depth[d.argmin(2)]; ok = d.min(2) < 60
m = np.zeros(ok.shape, bool); m[60:920, 60:900] = True; m[600:1010, 60:90] = False
valid = ok & m
ind = ndi.distance_transform_edt(~valid, return_distances=False, return_indices=True)
dep_f = dep[ind[0], ind[1]]
tmp = os.environ.get('TEMP', '.') + '/mmr/'; os.makedirs(tmp, exist_ok=True)
np.save(tmp + 'dep.npy', dep_f)
win = np.zeros(dep_f.shape, bool); win[330:790, 180:720] = True
mask = (dep_f > -2.0) & win
mask = ndi.binary_closing(mask, iterations=2); mask = ndi.binary_fill_holes(mask)
lab, n = ndi.label(mask); sizes = ndi.sum(mask, lab, range(1, n+1))
polys = []
for i, s in enumerate(sizes):
    if s <= 300: continue
    comp = np.pad((lab == i+1).astype(float), 1)
    cs = measure.find_contours(comp, 0.5)
    c = max(cs, key=len) - 1                      # (row, col)
    c = measure.approximate_polygon(c, 1.0)
    polys.append([[round(float(x), 1), round(float(y), 1)] for y, x in c[:-1]])
polys.sort(key=lambda p: (np.mean([q[1] for q in p]) > 480, np.mean([q[0] for q in p])))
json.dump(polys, open(R + 'work_polys_fig3_m20_v2.json', 'w'))
print(len(polys), [len(p) for p in polys])

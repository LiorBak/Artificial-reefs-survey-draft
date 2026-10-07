"""prep_sources.py - one-off preparation of the source windows used by build_3d.py (2026-10-06, 3D agent).
 (a) Welsh Government LiDAR tile SN6089 (flown 2022-03-19; DSM/DTM 1 m, EPSG:27700, origin 260000/290000 top-left, nodata -9999):
     the original tile is NOT kept in the project (re-download: see SOURCES_3D.md S2); this script cuts the beach window (values only).
 (b) HRPP576 Fig 2 (img-17): digitises the -2/-3/-4 mODN contour lines by tracking the grey lines, georeferences them to the canonical
     frame through the oval 'C' (centre pixel <-> centroid of the traced south oval) and the 500 m scale bar.
Run:  python prep_sources.py [path to scratch tif folder]
"""
import json, sys, os, numpy as np, tifffile
import b3d_lib as L
from PIL import Image
from shapely.geometry import Polygon

D = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\lior\AppData\Local\Temp\claude\C--\cd973dbd-a674-4cd5-adf1-ffb4c361545f\scratchpad\borth_verify\dl"
# ---- (a) beach window -------------------------------------------------------------------------------
out = os.path.join(L.SRC, 'lidar_beach_SN6089_2022-03-19.npz')
if os.path.exists(os.path.join(D, 'wg_dtm_SN6089.tif')):
    dtm = tifffile.imread(os.path.join(D, 'wg_dtm_SN6089.tif')).astype(np.float32)
    dsm = tifffile.imread(os.path.join(D, 'wg_dsm_SN6089.tif')).astype(np.float32)
    E0, E1, N0, N1 = 260300, 260900, 289000, 289500
    r0, r1, c0, c1 = 290000 - N1, 290000 - N0, E0 - 260000, E1 - 260000
    np.savez_compressed(out, dtm=dtm[r0:r1, c0:c1], dsm=dsm[r0:r1, c0:c1], E0=E0, N1=N1, cell_m=1.0)
    print('beach window written', out, os.path.getsize(out), 'bytes')

# ---- (b) Fig 2 contours --------------------------------------------------------------------------------
img = os.path.join(L.BASE, '..', '..', '..', '03_images', 'reefs', 'borth-coastal-defence-reef',
                   'borth-coastal-defence-reef_hrpp576-fig2-layout-contours_2013.png')
im = np.array(Image.open(img).convert('L')).astype(int)
def centres(col, thr=225):
    ys = np.where(im[:, col] < thr)[0]; o = []; s = None
    for y in ys:
        if s is None: s = y; p = y
        elif y == p + 1: p = y
        else: o.append((s + p) / 2); s = y; p = y
    if s is not None: o.append((s + p) / 2)
    return np.array(o)
def track(x0, y0, xs, maxjump=3.5):
    res = {}; y = y0
    for x in xs:
        c = centres(x)
        if len(c) == 0: continue
        j = np.argmin(abs(c - y))
        if abs(c[j] - y) <= maxjump: y = c[j]; res[x] = y
    return res
# start rows read at column 330 (-2: 139, -3: 191, -4: 262), labels checked against the left-hand labels (VERIFY in SOURCES_3D.md)
tr = {}
for lab, y0 in (('-2', 139), ('-3', 191), ('-4', 262)):
    tr[lab] = {**track(330, y0, range(330, 250, -1)), **track(330, y0, range(330, 640))}
# -4.0 right of x=446 was confused by the reef drawings: manual points read on a 3x crop (orig px)
m4 = [(463, 250), (503, 258), (563, 262), (577, 267), (597, 280), (630, 300), (663, 348)]
tr['-4'] = {x: y for x, y in tr['-4'].items() if x <= 446}
# calibration: oval C
sh = json.load(open(os.path.join(L.BASE, 'shape.json'), encoding='utf-8'))
oval = Polygon(sh['canonical']['polygons_m'][1]); cx, cy = oval.centroid.coords[0]
px_c, py_c = 549.5, 204.5            # centre of the outer ring of oval C in Fig 2 (orig px), read from the ASCII dump of the figure
s_m_px = 500.0 / (434.0 - 152.5)     # 500 m bar: 0 at x=152.5, 500 at x=434 (orig px) -> 1.776 m/px
def can(px, py):                      # Fig 2: right = SOUTH (+x), down = offshore (+y)
    return [round(cx + (px - px_c) * s_m_px, 1), round(cy + (py - py_c) * s_m_px, 1)]
res = {'calibration': {'oval_centre_px': [px_c, py_c], 'oval_centroid_canonical_m': [round(cx, 2), round(cy, 2)], 'm_per_px': round(s_m_px, 4),
                       'note': 'Fig 2 up = landward, right = south; canonical x = cx + (px-px_c)*s, y = cy + (py-py_c)*s; no rotation (oval axis is shore-parallel in the figure)',
                       'accuracy': 'about +-10 m horizontally (by eye, 1 px = 1.8 m); contour heights are the figure labels'},
       'contours_mODN': {}}
for lab in ('-2', '-3', '-4'):
    pts = [(x, y) for x, y in sorted(tr[lab].items())]
    if lab == '-4': pts += m4
    pts = pts[::4] if len(pts) > 60 else pts
    res['contours_mODN'][lab] = [can(x, y) for x, y in pts]
    print(lab, len(pts), res['contours_mODN'][lab][:2], res['contours_mODN'][lab][-1])
json.dump(res, open(os.path.join(L.SRC, 'fig2_contours_canonical.json'), 'w'))
json.dump({k: {str(a): b for a, b in v.items()} for k, v in tr.items()}, open(os.path.join(L.SRC, 'fig2_contour_tracks_px.json'), 'w'))

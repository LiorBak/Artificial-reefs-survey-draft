"""nav_isolines.py - Garmin Navionics screenshots (src/navionics/*.png from navionics_capture.py) -> iso-depth lines in the canonical frame,
a cross-shore depth profile, and an annotated figure.  Private research copy, 'Garmin Navionics, not for navigation'.
Principle (as palm-beach): with 'Shallow shading' = v m the chart paints water shallower than v blue, so the edge of the blue area is the v-m contour.
Pixel -> canonical: the map is centred on the reef centroid (shape.json geo.centroid_latlon) at screenshot pixel (491, 327.5); Web Mercator, 256 px tiles;
pixel -> lon/lat -> EPSG:2106 (E,N) -> canonical (x,y) with mmr_lib.en_to_xy.   Output: navionics_isolines.json."""
import json, math, os, sys
import numpy as np, cv2
from pyproj import Transformer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mmr_lib as L
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(HERE, '..', 'src', 'navionics')
SIZE = (982, 655); CENTRE = (-37.6447833, 176.2025908)
T = Transformer.from_crs(4326, 2106, always_xy=True)

def merc(lat, lon, z):
    n = 256 * 2 ** z
    return n * (lon + 180) / 360, n * (0.5 - math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) / (2 * math.pi))

def clip2ll(px, py, z):
    cx, cy = merc(*CENTRE, z); n = 256 * 2 ** z
    x, y = cx + px - SIZE[0] / 2, cy + py - SIZE[1] / 2
    return math.degrees(2 * math.atan(math.exp((0.5 - y / n) * 2 * math.pi)) - math.pi / 2), x / n * 360 - 180

def clip2canon(px, py, z):
    lat, lon = clip2ll(px, py, z); E, N = T.transform(lon, lat); return L.en_to_xy(E, N)

def canon2clip(x, y, z):
    E, N = L.xy_to_en(np.array(x), np.array(y)); lon, lat = T.transform(E, N, direction='INVERSE')
    cx, cy = merc(*CENTRE, z); a, b = zip(*[merc(la, lo, z) for la, lo in zip(np.atleast_1d(lat), np.atleast_1d(lon))])
    return SIZE[0] / 2 + np.array(a) - cx, SIZE[1] / 2 + np.array(b) - cy

def load(chart, z, v):
    return cv2.cvtColor(cv2.imread(os.path.join(SRC, '%s_z%d_shade%04.1f.png' % (chart, z, v))), cv2.COLOR_BGR2RGB).astype(int)

def iso_lines(chart, z, v, min_len=60):
    im = load(chart, z, v)
    m = ((im[:, :, 2] - im[:, :, 0]) > 9).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    h, w = m.shape; out = []
    for c in cv2.findContours(m, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]:
        c = c[:, 0, :]
        keep = (c[:, 0] > 8) & (c[:, 0] < w - 8) & (c[:, 1] > 8) & (c[:, 1] < h - 8)
        keep &= ~((c[:, 0] < 175) & (c[:, 1] < 65)); keep &= ~((c[:, 0] > 930) & (c[:, 1] > 555))
        run = []
        for p, k in zip(c, keep):
            if k: run.append(p)
            else:
                if len(run) >= min_len: out.append(np.array(run))
                run = []
        if len(run) >= min_len: out.append(np.array(run))
    res = []
    for l in out:
        xy = np.array([clip2canon(float(px), float(py), z) for px, py in l[::3]])
        res.append(xy.round(2).tolist())
    return res

if __name__ == '__main__':
    out = {}
    for chart in ('sonar', 'naut'):
        out[chart] = {}
        for z in (17, 18):
            out[chart][str(z)] = {str(v): iso_lines(chart, z, float(v)) for v in range(1, 11)}
            print(chart, z, {v: [len(p) for p in ps] for v, ps in out[chart][str(z)].items()})
    # land edge (yellow / green region of the shade-0 image) -> canonical y of the chart's shoreline
    im = load('sonar', 17, 0.0); land = ((im[:, :, 0] > 140) & (im[:, :, 2] < 130) & (im[:, :, 1] > 150)).astype(np.uint8)
    cs = cv2.findContours(land, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    big = max(cs, key=len)[:, 0, :]; big = big[(big[:, 0] > 8) & (big[:, 1] < 640) & (big[:, 0] < 970)]
    out['land_edge_canon_z17'] = [clip2canon(float(px), float(py), 17) for px, py in big[::5]]
    json.dump(out, open(os.path.join(HERE, 'navionics_isolines.json'), 'w'))
    # profile: robust line y = a + b x per contour (z17 SonarChart), then y at x = 0
    prof = {}
    for v, ps in out['sonar']['17'].items():
        pts = np.array([p for l in ps for p in l])
        if len(pts) < 20: continue
        A = np.c_[np.ones(len(pts)), pts[:, 0]]; w = np.ones(len(pts), bool)
        for _ in range(10):
            c, *_ = np.linalg.lstsq(A[w], pts[w, 1], rcond=None); r = pts[:, 1] - A @ c; w = np.abs(r) < max(10, 2 * r[w].std())
        prof[v] = dict(y_at_x0=round(float(c[0]), 1), slope_dy_dx=round(float(c[1]), 3), rms=round(float(r[w].std()), 1), n=int(w.sum()))
    print(json.dumps(prof)); json.dump(prof, open(os.path.join(HERE, 'navionics_profile_sonar_z17.json'), 'w'), indent=1)
    le = np.array(out['land_edge_canon_z17']); print('land edge canon y at x=0 ~', np.interp(0, np.sort(le[:, 0]), le[np.argsort(le[:, 0]), 1]).round(1), 'range y', le[:, 1].min().round(1), le[:, 1].max().round(1))

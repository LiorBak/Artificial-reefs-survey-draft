"""navionics_isolines.py - turn the Navionics screenshots (src/navionics/*.png, made by navionics_capture.py) into iso-depth lines in the canonical frame.

Principle: with 'Shallow shading' = v metres the chart paints every cell shallower than v blue, so the outline of the blue region IS the v-m contour.
(Checked: the printed contour labels 1, 2, 3, 5, 6, 7, 8, 9, 10 of the SonarChart lie within 0.5-1.2 m of the extracted lines of the same value.)
Screenshot pixel -> canonical metres: the map is centred on the reef centroid (shape.json geo.centroid_latlon), Web-Mercator, tile size 256 px,
pixel -> lon/lat -> local azimuthal-equidistant (shape.json canonical origin) -> rotate by the frame bearings (334.3 / 64.3 deg) -> (x, y).
The shape.json vertex check (canonical vertex 0 -> lat/lon) is repeated in build_3d.py.
Output: navionics_isolines.json  {chart: {zoom: {depth_m: [[ [x, y], ... ], ...]}}}  (canonical metres, +x alongshore NNW, +y offshore ENE).
"""
import json, math, os
import numpy as np
import cv2
from pyproj import Proj

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'src', 'navionics')
SHAPE = os.path.join(HERE, '..', 'shape.json')
OUT = os.path.join(HERE, 'navionics_isolines.json')
SIZE = (982, 655)


class Geo:
    def __init__(self):
        d = json.load(open(SHAPE, encoding='utf8'))
        g = d['geo']
        self.lat0, self.lon0 = g['canonical_origin_latlon']
        self.centre = tuple(g['centroid_latlon'])
        self.bx = math.radians(g['shoreline_bearing_deg'])                      # +x alongshore toward 334.3 deg true
        self.by = math.radians((g['shoreline_bearing_deg'] + 90.0) % 360.0)      # +y offshore toward 64.3 deg true
        self.aeqd = Proj(proj='aeqd', lat_0=self.lat0, lon_0=self.lon0, datum='WGS84')
        self.A = np.array([[math.sin(self.bx), math.sin(self.by)], [math.cos(self.bx), math.cos(self.by)]])

    def canon2ll(self, x, y):
        E = x * math.sin(self.bx) + y * math.sin(self.by)
        N = x * math.cos(self.bx) + y * math.cos(self.by)
        lon, lat = self.aeqd(E, N, inverse=True)
        return lat, lon

    def ll2canon(self, lat, lon):
        E, N = self.aeqd(lon, lat)
        return tuple(np.linalg.solve(self.A, [E, N]))

    @staticmethod
    def merc(lat, lon, z):
        n = 256 * 2 ** z
        return n * (lon + 180) / 360, n * (0.5 - math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) / (2 * math.pi))

    def clip2ll(self, px, py, z):
        cx, cy = self.merc(*self.centre, z)
        n = 256 * 2 ** z
        x, y = cx + px - SIZE[0] / 2, cy + py - SIZE[1] / 2
        return math.degrees(2 * math.atan(math.exp((0.5 - y / n) * 2 * math.pi)) - math.pi / 2), x / n * 360 - 180

    def clip2canon(self, px, py, z):
        return self.ll2canon(*self.clip2ll(px, py, z))

    def canon2clip(self, x, y, z):
        lat, lon = self.canon2ll(x, y)
        cx, cy = self.merc(*self.centre, z)
        a, b = self.merc(lat, lon, z)
        return SIZE[0] / 2 + a - cx, SIZE[1] / 2 + b - cy

    def m_per_px(self, z):
        return 2 * math.pi * 6378137 * math.cos(math.radians(self.centre[0])) / (256 * 2 ** z)


def load(chart, z, v):
    return cv2.cvtColor(cv2.imread(os.path.join(SRC, '%s_z%d_shade%04.1f.png' % (chart, z, v))), cv2.COLOR_BGR2RGB).astype(int)


def iso_lines(chart, z, v, geo, min_len=60):
    """pieces of the boundary of the shaded (blue) region, as canonical [x, y] lists. Pieces on the landward side (y < 25 m: the waterline), at the window
    border, under the 'MAP OPTIONS' button or the zoom buttons are discarded."""
    im = load(chart, z, v)
    m = ((im[:, :, 2] - im[:, :, 0]) > 9).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    h, w = m.shape
    cs, _ = cv2.findContours(m, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    out = []
    for c in cs:
        c = c[:, 0, :]
        keep = (c[:, 0] > 8) & (c[:, 0] < w - 8) & (c[:, 1] > 8) & (c[:, 1] < h - 8)
        keep &= ~((c[:, 0] < 175) & (c[:, 1] < 65))
        keep &= ~((c[:, 0] > 930) & (c[:, 1] > 555))
        run = []
        for p, k in zip(c, keep):
            if k:
                run.append(p)
            else:
                if len(run) >= min_len:
                    out.append(np.array(run))
                run = []
        if len(run) >= min_len:
            out.append(np.array(run))
    res = []
    for l in out:
        xy = np.array([geo.clip2canon(float(px), float(py), z) for px, py in l[::3]])
        if np.median(xy[:, 1]) < 25:
            continue
        res.append(xy.round(2).tolist())
    return res


def main():
    geo = Geo()
    out = {}
    for chart in ('sonar', 'naut'):
        out[chart] = {}
        for z in (17, 18):
            out[chart][str(z)] = {str(v): iso_lines(chart, z, float(v), geo) for v in range(1, 11)}
            print(chart, z, {v: [len(p) for p in ps] for v, ps in out[chart][str(z)].items()})
    # hand-read features of the chart (z18 screenshot sonar_z18_shade00.0.png / naut_z18_shade00.0.png, pixel positions read on a 1:1 view)
    reads = dict(
        fish_haven_label=dict(text='FISH HAVEN 1.5MT', px_z18=[480, 322]),
        fish_haven_symbol=dict(text='fish icon with dotted outline', px_z18=[442, 359]),
        obstruction_star=dict(text='small red star symbol (not interpreted)', px_z18=[498, 356]),
        sonar_labels_z18={'1': [85, 520], '1.5': [125, 445], '2': [155, 370], '2.5': [87, 143], '3': [103, 89], '4.5': [597, 537], '5': [628, 454],
                          '5.5': [672, 445], '6': [680, 395], '6.5': [690, 360], '7': [731, 404], '7.5': [762, 435], '8': [787, 436],
                          '8.5': [823, 448], '9': [846, 428], '10': [894, 394], '10.5': [935, 435], '11': [947, 405]})
    for k in ('fish_haven_label', 'fish_haven_symbol', 'obstruction_star'):
        reads[k]['canon_m'] = [round(float(t), 1) for t in geo.clip2canon(*reads[k]['px_z18'], 18)]
    reads['sonar_labels_canon_m'] = {k: [round(float(t), 1) for t in geo.clip2canon(*v, 18)] for k, v in reads['sonar_labels_z18'].items()}
    out['hand_reads'] = reads
    out['m_per_px'] = {str(z): geo.m_per_px(z) for z in (17, 18)}
    json.dump(out, open(OUT, 'w'))
    print('written', OUT)


if __name__ == '__main__':
    main()

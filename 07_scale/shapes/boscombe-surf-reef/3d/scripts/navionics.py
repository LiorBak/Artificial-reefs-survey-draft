"""Garmin Navionics web-viewer screenshots (2026-10-05) -> numbers for the Boscombe 3D model (called by ../build_3d.py).

What is read from the screenshots (all private research copies in ../../src/navionics_garmin_*_2026-10-05.png):
  * fills of the shoal that marks the reef: green = drying (above chart datum), dark blue / light blue = depth < 0.5 m / 0.5-1 m
    (SonarChart) or < 1 m (Nautical Chart), because the viewer was set to 'shallow shading 1 m';
  * 30 spot soundings and contour labels typed in navionics_reads.json (read by eye from 3x enlarged crops, pixel positions + value in m).
Pixel -> ground: Leaflet web-mercator, map pane 1000 x 751 px at screenshot offset (400, 113); centre = 50.71753 N, 1.83891 W;
  mercator metres per px = 156543.03392 / 2^z ; lat/lon -> OSGB/canonical via canon.py (img1 georeference).
Datum of every Navionics depth: NOT stated by the viewer; assumed chart datum (ACD) - assumption A9 in METHODS_3D.md.
"""
import json, math
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

import canon

HERE = Path(__file__).resolve().parent
SRC = canon.ROOT / "src"
R_EARTH = 6378137.0
LAT0, LON0 = 50.71753, -1.83891
PANE_OFFSET = (400.0, 113.0)           # map pane origin in the screenshot
PANE_CENTRE = (500.0, 375.5)           # centre of the pane (pane 1000 x 751)
COLS = {"green": (152, 200, 0), "dblue": (32, 176, 248), "lblue": (160, 216, 248)}
WINDOW = {18: (780, 330, 1120, 600), 17: (800, 380, 1040, 520)}      # x0, y0, x1, y1 in screenshot px: only the reef shoal (not the beach shading)
FILES = {
    ("nautical", 17): "navionics_garmin_nauticalchart_z17_2026-10-05.png",
    ("nautical", 18): "navionics_garmin_nauticalchart_z18_2026-10-05.png",
    ("sonar", 17): "navionics_garmin_sonarchart_z17_2026-10-05.png",
    ("sonar", 18): "navionics_garmin_sonarchart_z18_2026-10-05.png",
}


def _merc(lat, lon):
    return R_EARTH * math.radians(lon), R_EARTH * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


class Mapper:
    def __init__(self, z):
        self.z = z
        self.res = 156543.03392 / 2 ** z                       # mercator m per px
        self.cx, self.cy = _merc(LAT0, LON0)
        self.mpp = self.res * math.cos(math.radians(LAT0))     # ground m per px

    def px2ll(self, px, py):
        x = self.cx + (np.asarray(px) - PANE_OFFSET[0] - PANE_CENTRE[0]) * self.res
        y = self.cy - (np.asarray(py) - PANE_OFFSET[1] - PANE_CENTRE[1]) * self.res
        return np.degrees(2 * np.arctan(np.exp(y / R_EARTH)) - math.pi / 2), np.degrees(x / R_EARTH)

    def ll2px(self, lat, lon):
        x, y = _merc(lat, lon)
        return PANE_OFFSET[0] + PANE_CENTRE[0] + (x - self.cx) / self.res, PANE_OFFSET[1] + PANE_CENTRE[1] - (y - self.cy) / self.res

    def px2can(self, px, py):
        px = np.atleast_1d(px).astype(float); py = np.atleast_1d(py).astype(float)
        lat, lon = self.px2ll(px, py)
        out = np.array([canon.px2can(canon.ll2px(float(a), float(b))) for a, b in zip(lat, lon)])
        return out                                            # (n,2)

    def can2px(self, x, y):
        p = canon.can2px(np.c_[np.atleast_1d(x), np.atleast_1d(y)])
        lat, lon = zip(*[canon.px2ll(a, b) for a, b in p])
        return np.array([self.ll2px(a, b) for a, b in zip(lat, lon)])


def load(kind, z):
    return np.array(Image.open(SRC / FILES[(kind, z)]).convert("RGB")).astype(int)


def mask_of(im, names, win):
    m = np.zeros(im.shape[:2], bool)
    for n in names:
        m |= np.abs(im - np.array(COLS[n])).sum(2) < 12
    w = np.zeros_like(m); x0, y0, x1, y1 = win; w[y0:y1, x0:x1] = True
    return m & w


def shape_stats(mask, mp):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    pts = mp.px2can(xs[::4], ys[::4])
    ctr = pts.mean(0); ev, evec = np.linalg.eigh(np.cov(pts.T))
    return {"area_m2": int(round(mask.sum() * mp.mpp ** 2)), "centroid_xy": [round(float(ctr[0]), 1), round(float(ctr[1]), 1)],
            "length_4sigma_m": round(float(4 * math.sqrt(ev[1])), 1), "width_4sigma_m": round(float(4 * math.sqrt(ev[0])), 1),
            "long_axis_deg_from_x": round(math.degrees(math.atan2(evec[1, 1], evec[0, 1])) % 180, 1)}


def outline(mask, mp, tol=0.8):
    from skimage import measure
    from shapely.geometry import LineString
    m = ndi.binary_closing(mask, iterations=1)
    cs = measure.find_contours(np.pad(m.astype(float), 1), 0.5)
    if not cs:
        return []
    c = max(cs, key=len) - 1.0
    xy = mp.px2can(c[:, 1], c[:, 0])
    s = LineString(xy).simplify(tol)
    return [[round(float(a), 1), round(float(b), 1)] for a, b in s.coords]


def derive():
    reads = json.load(open(HERE / "navionics_reads.json", encoding="utf-8"))
    out = {"layers": {}, "soundings": [], "contour_labels": []}
    for kind in ("nautical", "sonar"):
        z = 18; mp = Mapper(z); im = load(kind, z); win = WINDOW[z]
        L = {}
        L["drying"] = {"mask": ["green"]}
        if kind == "sonar":
            L["depth_lt_0.5m"] = {"mask": ["green", "dblue"]}
            L["depth_lt_1m"] = {"mask": ["green", "dblue", "lblue"]}
        else:
            L["depth_lt_1m"] = {"mask": ["green", "dblue"]}
        for name, d in L.items():
            m = mask_of(im, d["mask"], win)
            d.update(shape_stats(m, mp) or {}); d["outline_xy"] = outline(m, mp)
            d.pop("mask")
        out["layers"][kind] = L
    mp17 = Mapper(17)
    for kind_key, store in (("nautical_z17_soundings", "soundings"), ("nautical_z17_contour_labels", "contour_labels")):
        for px, py, depth in reads[kind_key]:
            x, y = mp17.px2can(px, py)[0]
            out[store].append({"px": px, "py": py, "depth_m": depth, "x": round(float(x), 1), "y": round(float(y), 1)})
    out["mpp_z17"] = mp17.mpp; out["mpp_z18"] = Mapper(18).mpp
    return out


def compare(nav, F, stats, zones):
    """Navionics vs the model (survey grid, April 2011).  F = fields.build() dict; zones = reef.crest_zones list."""
    xs, ys, S, code = F["xs"], F["ys"], F["S"], F["code"]
    rows = []
    for s in nav["soundings"] + nav["contour_labels"]:
        j = int(round(s["y"] - ys[0])); i = int(round(s["x"] - xs[0]))
        if 0 <= j < len(ys) and 0 <= i < len(xs):
            model_depth = float(-S[j, i]); c = int(code[j, i])
        else:
            model_depth, c = None, -1
        rows.append({**s, "model_depth_m": None if model_depth is None else round(model_depth, 2), "code": c,
                     "diff_model_minus_nav_m": None if model_depth is None else round(model_depth - s["depth_m"], 2),
                     "used": c in (0, 1)})
    def stat(sel):
        d = np.array([r["diff_model_minus_nav_m"] for r in rows if sel(r)])
        return {"n": int(len(d)), "mean": round(float(d.mean()), 2), "sd": round(float(d.std(ddof=1)), 2), "rms": round(float(np.sqrt((d ** 2).mean())), 2)} if len(d) > 2 else {"n": int(len(d))}
    from shapely.geometry import Polygon
    zone_area = {z["level_acd"]: z["area_m2"] for z in zones}
    cen = {}
    for z in zones:
        if z["loops"]:
            big = max(z["loops"], key=lambda l: Polygon(l).area)
            p = Polygon(big); cen[z["level_acd"]] = [round(p.centroid.x, 1), round(p.centroid.y, 1)]
    son, nau = nav["layers"]["sonar"], nav["layers"]["nautical"]
    cmp = {
        "area_m2": {
            "drying_above_0m_acd": {"survey_april2011": zone_area.get(0.0), "sonarchart": son["drying"]["area_m2"], "nautical_chart": nau["drying"]["area_m2"]},
            "shallower_than_0.5m": {"survey_april2011": zone_area.get(-0.5), "sonarchart": son["depth_lt_0.5m"]["area_m2"]},
            "shallower_than_1m": {"survey_april2011": zone_area.get(-1.0), "sonarchart": son["depth_lt_1m"]["area_m2"], "nautical_chart": nau["depth_lt_1m"]["area_m2"]},
        },
        "centroid_xy_drying": {"survey_zone_0m": cen.get(0.0), "sonarchart": son["drying"]["centroid_xy"], "nautical_chart": nau["drying"]["centroid_xy"]},
        "soundings_all": stat(lambda r: r["code"] in (0, 1)),
        "soundings_in_survey_area": stat(lambda r: r["code"] == 0),
        "soundings_in_extrapolated_area": stat(lambda r: r["code"] == 1),
    }
    return rows, cmp

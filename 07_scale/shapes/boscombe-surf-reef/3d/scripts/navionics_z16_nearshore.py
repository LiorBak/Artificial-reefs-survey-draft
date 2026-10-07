"""Garmin Navionics Nautical Chart, zoom 16 screenshot (2026-10-05, same capture session as the z17/z18 images) -> NEARSHORE zone boundaries
compared with the extended Boscombe seabed (re-check run 2026-10-07).

Colour classes of the chart (RGB sampled on the screenshot): yellow (240,216,80)/(248,232,112) = land above the chart's high-water line,
green (152,200,0) = drying (between high-water line and chart datum), blue (32,176,248) = depth 0-1 m below chart datum (shallow shading 1 m),
white (248,248,248) = deeper than 1 m.  For canonical x = -150..150 (step 10) the profile is scanned from y = -60 to 260 m (step 1 m) and the first
transitions land->green (high-water line), green->blue (chart datum, 0 m), blue->white (1 m below CD) are recorded and compared with the
model heights there.   Expected if the Navionics datum is chart datum and the model is right:
    green->blue : z_ACD = 0  -> z_MSL = -1.40 ;  blue->white : z_ACD = -1 -> z_MSL = -2.40 ;  land->green: high-water line of the chart (MHWS ~ +0.81 m MSL, assumed).
Pixel -> ground: Leaflet web mercator, see navionics.Mapper (pane 1000 x 751 at screenshot offset (400, 113); z16 = 1.512 m / px).
Output: nav_z16_nearshore.json (scripts folder).
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import navionics as nv
import canon

IM = np.array(Image.open(nv.SRC / "navionics_garmin_nauticalchart_z16_2026-10-05.png").convert("RGB")).astype(int)
MP = nv.Mapper(16)
CLS = {"land": [(240, 216, 80), (248, 232, 112)], "green": [(152, 200, 0)], "blue": [(32, 176, 248)], "white": [(248, 248, 248)]}


def classify(rgb):
    best, bd = None, 1e9
    for k, cols in CLS.items():
        for c in cols:
            d = sum((a - b) ** 2 for a, b in zip(rgb, c))
            if d < bd:
                best, bd = k, d
    return best if bd < 40 ** 2 else None


def scan(x, ys):
    P = MP.can2px(np.full(len(ys), x), ys)            # (n, 2) pixel positions
    out = []
    for (px, py) in P:
        ix, iy = int(round(px)), int(round(py))
        if 400 <= ix < 1400 and 113 <= iy < 864:
            out.append(classify(IM[iy, ix]))
        else:
            out.append(None)
    return out


def transitions(x):
    ys = np.arange(-60.0, 261.0, 1.0)
    cl = scan(x, ys)
    res = {}
    # first y where the class changes from a to b (ignoring None and thin labels: require 3 consecutive cells of b)
    def first(a, b):
        seen_a = False
        for i in range(len(ys) - 3):
            if cl[i] == a:
                seen_a = True
            if seen_a and cl[i] != a and cl[i] == b and cl[i + 1] == b and cl[i + 2] == b:
                return float(ys[i])
        return None
    res["land_green"] = first("land", "green")
    res["green_blue"] = first("green", "blue")
    res["blue_white"] = first("blue", "white")
    return res


if __name__ == "__main__":
    M = json.loads(open(HERE.parent / "model.js", encoding="utf8").read().split("=", 1)[1].rstrip().rstrip(";"))
    sb = M["seabed"]
    Z = np.array(sb["z_cm"]).reshape(sb["ny"], sb["nx"]) / 100.0

    def zmodel(x, y):
        fx = (x - sb["x0"]) / sb["dx"]; fy = (y - sb["y0"]) / sb["dy"]
        i = int(np.clip(np.floor(fx), 0, sb["nx"] - 2)); j = int(np.clip(np.floor(fy), 0, sb["ny"] - 2)); tx, ty = fx - i, fy - j
        return (Z[j, i] * (1 - tx) + Z[j, i + 1] * tx) * (1 - ty) + (Z[j + 1, i] * (1 - tx) + Z[j + 1, i + 1] * tx) * ty

    rows = []
    for x in range(-150, 151, 10):
        t = transitions(float(x))
        r = {"x": x, **{k: v for k, v in t.items()}}
        for k, zexp in (("land_green", None), ("green_blue", -1.40), ("blue_white", -2.40)):
            if t[k] is not None:
                r["z_model_" + k] = round(float(zmodel(x, t[k])), 2)
        rows.append(r)
    json.dump(rows, open(HERE / "nav_z16_nearshore.json", "w"), indent=0)
    for k, exp in (("land_green", None), ("green_blue", -1.40), ("blue_white", -2.40)):
        v = np.array([r["z_model_" + k] for r in rows if "z_model_" + k in r])
        y = np.array([r[k] for r in rows if k in r and r[k] is not None])
        print(k, "n", len(v), "model z at the Navionics boundary: mean %.2f sd %.2f (expected %s); boundary y mean %.1f m" % (v.mean(), v.std(), exp, y.mean()))

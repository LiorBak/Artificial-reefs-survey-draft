"""Annotated image for the Navionics z16 NEARSHORE cross-check (re-check run 2026-10-07).
Reads nav_z16_nearshore.json (written by navionics_z16_nearshore.py) and the extended model seabed, and draws on a 3.5x crop of the z16
Nautical Chart screenshot (2026-10-05):
  dots    = Navionics colour boundaries read by the script (yellow/green = chart high-water line, green/blue = chart datum 0 m, blue/white = 1 m below CD)
  lines   = model contours at z_MSL = -1.40 (= 0 m ACD, solid red), -2.40 (= -1 m ACD, solid magenta), +0.81 (MHWS, dashed orange)
  box     = model grid extent (x -160..160, y -66..650, only y < 260 is inside the crop), cyan = y = 0 shoreline (surf line of the 28 Sep 2011 image)
Output: ../annotated/navionics_nauticalchart_z16_nearshore_vs_model_annotated.png
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import navionics as nv

SC = 3.5
M = json.loads(open(HERE.parent / "model.js", encoding="utf8").read().split("=", 1)[1].rstrip().rstrip(";"))
sb = M["seabed"]
Z = np.array(sb["z_cm"]).reshape(sb["ny"], sb["nx"]) / 100.0
rows = json.load(open(HERE / "nav_z16_nearshore.json"))
mp = nv.Mapper(16)

# crop box in screenshot pixels around canonical x -220..220, y -100..270
corners = mp.can2px(np.array([-220, 220, -220, 220]), np.array([-100, -100, 270, 270]))
x0, y0 = int(corners[:, 0].min()) - 5, int(corners[:, 1].min()) - 5
x1, y1 = int(corners[:, 0].max()) + 5, int(corners[:, 1].max()) + 5
im = Image.open(nv.SRC / "navionics_garmin_nauticalchart_z16_2026-10-05.png").convert("RGB")
out = im.crop((x0, y0, x1, y1)).resize((int((x1 - x0) * SC), int((y1 - y0) * SC)), Image.LANCZOS)
dr = ImageDraw.Draw(out)


def to_img(x, y):
    p = mp.can2px(np.atleast_1d(x), np.atleast_1d(y))
    return [((a - x0) * SC, (b - y0) * SC) for a, b in p]


def contour(level):
    pts = []
    for i in range(sb["nx"]):
        col = Z[:, i]
        ys = sb["y0"] + np.arange(sb["ny"]) * sb["dy"]
        k = np.where((col[:-1] > level) & (col[1:] <= level) & (ys[:-1] > -70) & (ys[:-1] < 300))[0]
        if len(k):
            j = k[0]
            y = ys[j] + (col[j] - level) / (col[j] - col[j + 1]) * sb["dy"]
            pts.append((sb["x0"] + i * sb["dx"], y))
    return pts


for level, col, dash in ((-1.40, (230, 0, 0), False), (-2.40, (200, 0, 200), False), (0.81, (255, 140, 0), True)):
    c = contour(level)
    P = to_img([p[0] for p in c], [p[1] for p in c])
    if dash:
        for a in range(0, len(P) - 1, 4):
            dr.line([P[a], P[min(a + 2, len(P) - 1)]], fill=col, width=3)
    else:
        dr.line(P, fill=col, width=3)
# y = 0 shoreline and the grid box edges inside the crop
P = to_img([-160, 160], [0, 0]); dr.line(P, fill=(0, 220, 220), width=3)
box = to_img([-160, 160, 160, -160, -160], [-66, -66, 260, 260, -66]); dr.line(box, fill=(60, 60, 60), width=2)
# Navionics boundaries
for key, col in (("land_green", (255, 255, 0)), ("green_blue", (0, 0, 0)), ("blue_white", (0, 90, 255))):
    for r in rows:
        if r.get(key) is not None:
            (X, Y), = to_img([r["x"]], [r[key]])
            dr.ellipse([X - 5, Y - 5, X + 5, Y + 5], fill=col, outline=(255, 255, 255))
dr.rectangle([6, 6, 1010, 108], fill=(255, 255, 255))
dr.text((12, 10), "Garmin Navionics Nautical Chart z16 (2026-10-05) vs the extended model seabed, canonical frame (x alongshore, y offshore).", fill=(0, 0, 0))
dr.text((12, 28), "Dots: chart boundaries read every 10 m of x - yellow = land/drying (HW line), black = drying/blue (chart datum 0 m), blue = blue/white (1 m below CD).", fill=(0, 0, 0))
dr.text((12, 46), "Lines: model z_MSL = -1.40 (0 m ACD) red; -2.40 (-1 m ACD) magenta; +0.81 (MHWS) orange dashed; cyan = y = 0 (surf line); dark box = model grid.", fill=(0, 0, 0))
dr.text((12, 64), "Result (31 profiles, x -150..150): model z at the black dots %.2f m (sd %.2f), expected -1.40; at the blue dots %.2f m (sd %.2f), expected -2.40." % (
    np.mean([r["z_model_green_blue"] for r in rows if "z_model_green_blue" in r]), np.std([r["z_model_green_blue"] for r in rows if "z_model_green_blue" in r]),
    np.mean([r["z_model_blue_white"] for r in rows if "z_model_blue_white" in r]), np.std([r["z_model_blue_white"] for r in rows if "z_model_blue_white" in r])), fill=(0, 0, 0))
dr.text((12, 82), "Navionics shades the chart in 1 m classes and generalises the lines; the reef mesh is separate from the seabed grid (the seabed contours do not include the reef).", fill=(0, 0, 0))
dest = HERE.parent / "annotated" / "navionics_nauticalchart_z16_nearshore_vs_model_annotated.png"
out.save(dest)
print(dest, out.size)

"""Garmin Navionics Nautical Chart z16 (2026-10-05): spot soundings south of the old model grid (y > 380 m), read by eye from 2.4x crops
(crop A = screenshot x 400-900, y 600-864; crop B = x 900-1400, y 600-864; red gridlines every 50 screenshot px).  Values in metres,
printed with the decimal as a subscript (8_4 = 8.4 m).  Only soundings inside the model grid |x| <= 160 m are used.
Compared with the EMODnet-slope extension of the seabed (y 382-650 m, code 5) assuming the Navionics depths are below chart datum:
    depth_model = -(z_MSL + 1.40).
Outputs: nav_z16_offshore.json and the annotated image ../annotated/navionics_nauticalchart_z16_offshore_soundings_annotated.png.
"""
import json, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import navionics as nv

# (crop, cx, cy, value_m)
READS = [
    ("A", 903, 32, 6.8), ("A", 1050, 72, 6.7), ("A", 962, 112, 7.3), ("A", 867, 137, 7.7), ("A", 1128, 248, 8.4), ("A", 979, 321, 8.7),
    ("A", 1074, 330, 8.9), ("A", 1170, 338, 9.3), ("A", 1016, 410, 9.4), ("A", 1150, 530, 10.4), ("A", 1038, 620, 10.4),
    ("B", 90, 134, 8.7), ("B", 178, 178, 9.1), ("B", 268, 134, 8.8), ("B", 347, 190, 9.0), ("B", 258, 238, 9.4), ("B", 50, 272, 8.8),
    ("B", 155, 272, 9.6), ("B", 260, 303, 9.7), ("B", 110, 462, 10.3), ("B", 258, 426, 10.3), ("B", 197, 497, 10.6), ("B", 50, 538, 10.5),
    ("B", 268, 584, 10.7), ("B", 365, 592, 10.7),
]
ORIG = {"A": (400, 600), "B": (900, 600)}
SC = 2.4

if __name__ == "__main__":
    M = json.loads(open(HERE.parent / "model.js", encoding="utf8").read().split("=", 1)[1].rstrip().rstrip(";"))
    sb = M["seabed"]
    Z = np.array(sb["z_cm"]).reshape(sb["ny"], sb["nx"]) / 100.0
    mp = nv.Mapper(16)
    src = np.array([[ORIG[c][0] + cx / SC, ORIG[c][1] + cy / SC] for c, cx, cy, v in READS])
    can = mp.px2can(src[:, 0], src[:, 1])

    def zmodel(x, y):
        fx = (x - sb["x0"]) / sb["dx"]; fy = (y - sb["y0"]) / sb["dy"]
        i = int(np.clip(np.floor(fx), 0, sb["nx"] - 2)); j = int(np.clip(np.floor(fy), 0, sb["ny"] - 2)); tx, ty = fx - i, fy - j
        return (Z[j, i] * (1 - tx) + Z[j, i + 1] * tx) * (1 - ty) + (Z[j + 1, i] * (1 - tx) + Z[j + 1, i + 1] * tx) * ty

    rows = []
    for (c, cx, cy, v), (px, py), (x, y) in zip(READS, src, can):
        if abs(x) > 160 or not (sb["y0"] <= y <= sb["y0"] + (sb["ny"] - 1) * sb["dy"]):
            continue
        dm = -(zmodel(x, y) + 1.40)
        rows.append({"crop": c, "px": round(float(px), 1), "py": round(float(py), 1), "x": round(float(x), 1), "y": round(float(y), 1), "depth_nav_m": v,
                     "depth_model_below_cd_m": round(float(dm), 2), "model_minus_nav_m": round(float(dm - v), 2), "zone_code": int(sb["code"][int(round((y - sb["y0"]) / sb["dy"])) * sb["nx"] + int(round((x - sb["x0"]) / sb["dx"]))])})
    d = np.array([r["model_minus_nav_m"] for r in rows])
    ysel = np.array([r["y"] for r in rows])
    res = {"n": len(rows), "mean": round(float(d.mean()), 2), "sd": round(float(d.std(ddof=1)), 2), "rms": round(float(np.sqrt((d ** 2).mean())), 2),
           "y_range": [round(float(ysel.min()), 0), round(float(ysel.max()), 0)],
           "by_zone": {}, "rows": rows,
           "note": "model depth = -(z_MSL + 1.40) = depth below chart datum, extension grid; positive = model deeper than Navionics. Reads by eye from 2.4x crops, +-0.05 m value, +-10 px (15 m) position"}
    for code in sorted({r["zone_code"] for r in rows}):
        q = np.array([r["model_minus_nav_m"] for r in rows if r["zone_code"] == code])
        res["by_zone"][str(code)] = {"n": int(len(q)), "mean": round(float(q.mean()), 2), "sd": round(float(q.std(ddof=1)) if len(q) > 1 else 0.0, 2)}
    # linear trend of the difference with y (is the EMODnet slope right?)
    if len(rows) > 4:
        A = np.c_[np.ones(len(rows)), ysel - 500.0]
        coef = np.linalg.lstsq(A, d, rcond=None)[0]
        res["diff_vs_y"] = {"intercept_at_y500_m": round(float(coef[0]), 2), "slope_m_per_100m": round(float(coef[1] * 100), 2)}
    json.dump(res, open(HERE / "nav_z16_offshore.json", "w"), indent=1)
    print({k: v for k, v in res.items() if k not in ("rows", "note")})

    # annotated image: the two crops side by side are rebuilt from the screenshot; marks = soundings used (red box + value)
    try:
        FONT = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        FONT = ImageFont.load_default()
    im = Image.open(nv.SRC / "navionics_garmin_nauticalchart_z16_2026-10-05.png").convert("RGB")
    out = im.crop((400, 600, 1400, 864)).resize((int(1000 * SC), int(264 * SC)), Image.LANCZOS)
    dr = ImageDraw.Draw(out)
    for (c, cx, cy, v) in READS:
        X = (ORIG[c][0] + cx / SC - 400) * SC; Y = (ORIG[c][1] + cy / SC - 600) * SC
        dr.rectangle([X - 26, Y - 22, X + 26, Y + 22], outline=(255, 0, 0), width=3)
    for r in rows:
        X = (r["px"] - 400) * SC; Y = (r["py"] - 600) * SC
        dr.text((X - 22, Y + 24), "%+.1f" % r["model_minus_nav_m"], fill=(200, 0, 0), font=FONT)
    canvas = Image.new("RGB", (out.width, out.height + 80), (255, 255, 255)); canvas.paste(out, (0, 80)); out = canvas; dr = ImageDraw.Draw(out)
    dr.text((10, 6), "Garmin Navionics Nautical Chart z16, 2026-10-05 (screenshot rows 600-864, y ~ 390-790 m): red boxes = soundings read (m).", fill=(200, 0, 0), font=FONT)
    dr.text((10, 28), "Red numbers = model minus Navionics depth (m, positive = model deeper) for the %d soundings inside |x| <= 160 m: mean %+.2f, sd %.2f, rms %.2f." % (res["n"], res["mean"], res["sd"], res["rms"]), fill=(200, 0, 0), font=FONT)
    dr.text((10, 50), "Pattern: model deeper than the chart at x < 0 and shallower at x > 0 (about -1.2 m per 100 m of x) - see METHODS_3D.md section 4, item 12.", fill=(200, 0, 0), font=FONT)
    out.save(HERE.parent / "annotated" / "navionics_nauticalchart_z16_offshore_soundings_annotated.png")

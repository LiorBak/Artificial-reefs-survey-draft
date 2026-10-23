"""Alongshore-trend check of the offshore extension (code 5), re-check run 2026-10-07.
The extension is z(x,y) = z_model(x,380) - 0.0141 (y-380), so it carries the alongshore variation of the y = 380 row (a thin-plate-spline
EXTRAPOLATION of the Fig. 9 survey, which ends at y ~312 m) out to y = 650 m.  This script (a) fits the 11 Navionics soundings
(nav_z16_offshore.json), (b) fits the EMODnet DTM 2024 cells (y 380-700, |x| < 400 m, 27 cells, files in 07_scale/bathymetry/emodnet/data),
(c) shows what the Navionics misfit would be if the y = 380 row were replaced by a flat (alongshore-mean) row.  Model NOT changed.
Prints a few lines and writes offshore_tilt_check.json.
"""
import csv, json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import canon

M = json.loads(open(HERE.parent / "model.js", encoding="utf8").read().split("=", 1)[1].rstrip().rstrip(";"))
sb = M["seabed"]
Z = np.array(sb["z_cm"]).reshape(sb["ny"], sb["nx"]) / 100.0
xs = sb["x0"] + np.arange(sb["nx"]) * sb["dx"]
row = Z[int(round((380 - sb["y0"]) / sb["dy"]))]
res = {"row380_slope_m_per_100m_x": round(float(np.polyfit(xs, row, 1)[0] * 100), 2), "row380_mean_z": round(float(row.mean()), 2)}

rows = json.load(open(HERE / "nav_z16_offshore.json"))["rows"]
x = np.array([r["x"] for r in rows]); y = np.array([r["y"] for r in rows]); e = np.array([r["model_minus_nav_m"] for r in rows])
A = np.c_[np.ones(len(x)), x / 100, (y - 500) / 100]
c = np.linalg.lstsq(A, e, rcond=None)[0]
s2 = ((e - A @ c) ** 2).sum() / (len(e) - 3); se = np.sqrt(np.diag(s2 * np.linalg.inv(A.T @ A)))
res["navionics_misfit_fit"] = {"const_m": round(float(c[0]), 2), "per_100m_x_m": round(float(c[1]), 2), "per_100m_y_m": round(float(c[2]), 2), "se": [round(float(v), 2) for v in se], "resid_sd_m": round(float(np.sqrt(s2)), 2)}

cells = [r for r in csv.DictReader(open(HERE.parents[3] / "bathymetry" / "emodnet" / "data" / "boscombe-surf-reef_cells_dtm2024_erddap.csv")) if r["elevation"]]
m = canon.px2can(np.array([canon.ll2px(float(r["latitude"]), float(r["longitude"])) for r in cells]))
z = np.array([float(r["elevation"]) for r in cells])
s = (m[:, 1] > 380) & (m[:, 1] < 700) & (abs(m[:, 0]) < 400)
B = np.c_[np.ones(s.sum()), m[s, 0] / 100, (m[s, 1] - 500) / 100]
cc = np.linalg.lstsq(B, z[s], rcond=None)[0]
res["emodnet_plane_LAT"] = {"n": int(s.sum()), "z500_m": round(float(cc[0]), 2), "per_100m_x_m": round(float(cc[1]), 3), "per_100m_y_m": round(float(cc[2]), 2), "resid_sd_m": round(float((z[s] - B @ cc).std()), 2)}

out = {}
for name, f in (("as built (row 380 + EMODnet slope)", lambda xx: np.interp(xx, xs, row)), ("row 380 replaced by its alongshore mean", lambda xx: row.mean() + 0 * xx),
                ("row mean + EMODnet alongshore gradient -0.0007 m/m", lambda xx: row.mean() - 0.0007 * xx)):
    d = np.array([-(f(r["x"]) - 0.0141 * (r["y"] - 380) + 1.40) - r["depth_nav_m"] for r in rows])
    out[name] = {"mean": round(float(d.mean()), 2), "sd": round(float(d.std(ddof=1)), 2), "rms": round(float(np.sqrt((d ** 2).mean())), 2)}
res["navionics_misfit_variants"] = out
json.dump(res, open(HERE / "offshore_tilt_check.json", "w"), indent=1)
print(json.dumps(res))

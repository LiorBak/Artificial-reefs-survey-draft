"""Step 5: compare EMODnet DTM 2024 with the project's Boscombe 3D model (READ ONLY on 07_scale/shapes/boscombe-surf-reef/3d/).
Datum:  z_LAT = z_MSL - z_LAT,MSL = z_MSL + 1.46   (model water_levels: LAT = -1.46 m MSL; chart datum ACD = MSL - 1.40; LAT = ACD - 0.06)
        EMODnet elevation e is already relative to LAT.   Delta = e_cell - <z_model,LAT>_cell
"""
import json, math, os, subprocess, sys
import numpy as np, pandas as pd
from matplotlib.path import Path as MPath
sys.path.insert(0, os.path.dirname(__file__))
import extract_site as E

ROOT = E.ROOT; DATA = E.DATA; slug = "boscombe-surf-reef"
MODEL_JS = f"{ROOT}/07_scale/shapes/{slug}/3d/model.js"
tmp = os.path.join(E.SCRATCH, "boscombe_model.json")
if not os.path.exists(tmp):
    subprocess.run(["node", "-e", f'global.window={{}};require({json.dumps(MODEL_JS)});require("fs").writeFileSync({json.dumps(tmp)},JSON.stringify(window.REEF_MODEL))'], check=True)
M = json.load(open(tmp, encoding="utf-8"))
LAT_MSL = [w["z"] for w in M["water_levels"] if w["key"] == "LAT"][0]      # -1.46
OFF = -LAT_MSL                                                            # z_LAT = z_MSL + OFF
CD_MINUS_MSL = -M["datum"]["msl_above_cd_m"]                              # -1.40
LAT_ACD = M["datum"]["lat_acd_m"]                                         # -0.06
print("OFF (z_LAT = z_MSL + OFF):", OFF)
fr = E.Frame(50.719552, -1.839278, 83.4, 173.4)

sb = M["seabed"]; SB = np.array(sb["z_cm"], float).reshape(sb["ny"], sb["nx"]) / 100.0; SBC = np.array([int(c) for c in sb["code"]]).reshape(sb["ny"], sb["nx"])
g = M["reef"]["grid"]
def garr(name):
    a = np.array(g[name], float).reshape(g["ny"], g["nx"]); a[a == g["nodata"]] = np.nan; return a / 100.0
RI, RS = garr("idealised_z_cm"), garr("surveyed_z_cm")


def bil(A, x0, y0, dx, dy, x, y):
    fi, fj = (y - y0) / dy, (x - x0) / dx
    if fi < 0 or fj < 0 or fi > A.shape[0] - 1 or fj > A.shape[1] - 1: return np.nan
    i, j = min(int(fi), A.shape[0] - 2), min(int(fj), A.shape[1] - 2); a, b = fi - i, fj - j
    v = [A[i, j], A[i + 1, j], A[i, j + 1], A[i + 1, j + 1]]
    if any(np.isnan(v)): return np.nan
    return v[0] * (1 - a) * (1 - b) + v[1] * a * (1 - b) + v[2] * (1 - a) * b + v[3] * a * b


def seabed(x, y): return bil(SB, sb["x0"], sb["y0"], sb["dx"], sb["dy"], x, y)
def surf_ideal(x, y):
    r = bil(RI, g["x0"], g["y0"], g["dx"], g["dy"], x, y); return seabed(x, y) if np.isnan(r) else r
def surf_survey(x, y):
    r = bil(RS, g["x0"], g["y0"], g["dx"], g["dy"], x, y); return seabed(x, y) if np.isnan(r) else r


# ---------------------------------------------------------------- 1. profile through the reef centre: add model columns (LAT frame)
prof = pd.read_csv(f"{DATA}/{slug}_profile_through_reef_centre.csv")
prof["model_seabed_LAT_m"] = [seabed(x, y) + OFF for x, y in zip(prof.x_m, prof.y_m)]
prof["model_asbuilt_surface_LAT_m"] = [surf_ideal(x, y) + OFF for x, y in zip(prof.x_m, prof.y_m)]
prof["model_apr2011_surface_LAT_m"] = [surf_survey(x, y) + OFF for x, y in zip(prof.x_m, prof.y_m)]
prof["delta_emodnet_minus_model_seabed_m"] = prof.elev_LAT_m - prof.model_seabed_LAT_m
prof.to_csv(f"{DATA}/{slug}_profile_through_reef_centre_with_model.csv", index=False)

# ---------------------------------------------------------------- 2. per-cell comparison
cells = pd.read_csv(f"{DATA}/{slug}_cells_dtm2024_erddap.csv")
cells = cells[cells.elevation.notna()]
xs = sb["x0"] + sb["dx"] * np.arange(sb["nx"]); ys = sb["y0"] + sb["dy"] * np.arange(sb["ny"]); XX, YY = np.meshgrid(xs, ys)
nodes = np.c_[XX.ravel(), YY.ravel()]
rows = []
for r in cells.itertuples():
    la, lo = r.latitude, r.longitude; h = 0.5 / 960
    corners = [fr.ll2xy(la + dy, lo + dx) for dy, dx in [(-h, -h), (-h, h), (h, h), (h, -h)]]
    path = MPath(corners + [corners[0]]); ins = path.contains_points(nodes)
    if ins.sum() == 0: continue
    area = 0.5 * abs(sum(corners[i][0] * corners[(i + 1) % 4][1] - corners[(i + 1) % 4][0] * corners[i][1] for i in range(4)))
    P = nodes[ins]
    zs = np.array([seabed(x, y) for x, y in P]) + OFF; zi = np.array([surf_ideal(x, y) for x, y in P]) + OFF; zv = np.array([surf_survey(x, y) for x, y in P]) + OFF
    code = SBC.ravel()[ins]
    cx, cy = fr.ll2xy(la, lo)
    rows.append(dict(ki=int(r.latitude * 0 + math.floor((la - 15) * 960)), kj=int(math.floor((lo + 36) * 960)), cell_x=round(cx, 1), cell_y=round(cy, 1), cell_area_m2=round(area),
                     model_coverage=round(len(P) * sb["dx"] * sb["dy"] / area, 2), frac_survey_code0=round(float((code == 0).mean()), 2),
                     emodnet_mean=r.elevation, emodnet_min=r.elevation_min, emodnet_max=r.elevation_max, emodnet_stdev=r.stdev, emodnet_n=r.value_count,
                     model_seabed_mean=zs.mean(), model_seabed_min=zs.min(), model_seabed_max=zs.max(),
                     model_asbuilt_mean=zi.mean(), model_asbuilt_max=zi.max(), model_apr2011_mean=zv.mean(), model_apr2011_max=zv.max(),
                     delta_vs_seabed=r.elevation - zs.mean(), delta_vs_asbuilt=r.elevation - zi.mean(), delta_vs_apr2011=r.elevation - zv.mean(),
                     reef_in_cell_frac=round(float((zi - zs > 0.3).mean()), 3)))
C = pd.DataFrame(rows); C.to_csv(f"{DATA}/{slug}_cells_emodnet_vs_model.csv", index=False)
full = C[(C.model_coverage >= 0.9) & (C.cell_y >= 90)]            # cells fully inside the model grid, seaward of the beach (y>=90 m)
print(full[["ki", "kj", "cell_x", "cell_y", "emodnet_mean", "model_seabed_mean", "model_asbuilt_mean", "delta_vs_seabed", "delta_vs_asbuilt", "reef_in_cell_frac", "frac_survey_code0"]].round(2).to_string())

# ---------------------------------------------------------------- 3. Navionics soundings (chart datum assumed = ACD): EMODnet cell mean minus sounding in LAT
cellmap = {(int(r.latitude * 0 + math.floor((r.latitude - 15) * 960)), int(math.floor((r.longitude + 36) * 960))): r for r in cells.itertuples()}
nrows = []
for s in M["navionics"]["soundings"]:
    la, lo = fr.xy2ll(s["x"], s["y"]); k = E.cell_k(la, lo); r = cellmap.get(k)
    if r is None: continue
    zl = -s["depth_m"] - LAT_ACD                                  # z_LAT = z_ACD - z_LAT,ACD ; z_ACD = -depth ; LAT_ACD = -0.06
    nrows.append(dict(x=s["x"], y=s["y"], nav_depth_m=s["depth_m"], nav_z_LAT=zl, emodnet_mean=r.elevation, emodnet_min=r.elevation_min, emodnet_max=r.elevation_max,
                      delta=r.elevation - zl, model_depth=s["model_depth_m"], code=s["code"]))
N = pd.DataFrame(nrows); N.to_csv(f"{DATA}/{slug}_emodnet_vs_navionics_soundings.csv", index=False)
print("Navionics soundings in valid EMODnet cells:", len(N), "mean delta", N.delta.mean().round(2), "sd", N.delta.std().round(2))

# ---------------------------------------------------------------- 4. summary numbers
def st(a): a = np.asarray(a, float); return dict(n=int(len(a)), mean=float(np.mean(a)), sd=float(np.std(a, ddof=1)) if len(a) > 1 else None, min=float(a.min()), max=float(a.max()))
reef_cells = full[full.reef_in_cell_frac > 0.02]
summ = dict(OFF_z_LAT_equals_z_MSL_plus=OFF, cd_minus_msl=CD_MINUS_MSL, lat_acd=LAT_ACD,
            all_cells_y90plus=st(full.delta_vs_seabed), reef_cells=reef_cells[["ki", "kj", "cell_x", "cell_y", "emodnet_mean", "emodnet_min", "emodnet_max", "model_seabed_mean", "model_asbuilt_mean", "model_asbuilt_max", "model_apr2011_mean", "model_apr2011_max", "delta_vs_seabed", "delta_vs_asbuilt", "delta_vs_apr2011", "reef_in_cell_frac"]].round(3).to_dict("records"),
            non_reef_cells_delta=st(full[full.reef_in_cell_frac <= 0.02].delta_vs_seabed) if (full.reef_in_cell_frac <= 0.02).any() else None,
            navionics=st(N.delta), navionics_by_code={int(c): st(g_.delta) for c, g_ in N.groupby("code")},
            alt_datum_note="if the survey zero were ODN the model seabed in the MSL frame rises by 1.40 m: Delta becomes Delta - 1.40")
json.dump(summ, open(f"{DATA}/{slug}_comparison_summary.json", "w"), indent=1)
print(json.dumps({k: v for k, v in summ.items() if k != "reef_cells"}, indent=1)); print(pd.DataFrame(summ["reef_cells"]).to_string())

# ---------------------------------------------------------------- 5. point table (the 11 REQUESTS_FOR_LIOR points): EMODnet cell vs model at the point
P = pd.read_csv(f"{DATA}/{slug}_points_emodnet.csv")
P["emodnet_mean_LAT"] = P.elev_LAT_m
P["emodnet_mean_MSL"] = P.elev_LAT_m - OFF
P["model_seabed_at_point_LAT"] = [seabed(x, y) + OFF for x, y in zip(P.x_m, P.y_m)]
P["model_asbuilt_at_point_LAT"] = [surf_ideal(x, y) + OFF for x, y in zip(P.x_m, P.y_m)]
P["delta_emodnet_minus_model_seabed_at_point"] = P.emodnet_mean_LAT - P.model_seabed_at_point_LAT
P[["point", "role", "x_m", "y_m", "lat", "lon", "emodnet_mean_LAT", "emodnet_mean_MSL", "elev_min", "elev_max", "value_count", "model_seabed_at_point_LAT", "model_asbuilt_at_point_LAT",
   "delta_emodnet_minus_model_seabed_at_point", "rest_ref_id", "wfs2024_ref_id"]].round({"x_m": 1, "y_m": 1, "lat": 7, "lon": 7, "emodnet_mean_LAT": 2, "emodnet_mean_MSL": 2, "elev_min": 2, "elev_max": 2, "model_seabed_at_point_LAT": 2, "model_asbuilt_at_point_LAT": 2, "delta_emodnet_minus_model_seabed_at_point": 2}).to_csv(f"{DATA}/{slug}_points_emodnet_vs_model.csv", index=False)
print(P[["point", "emodnet_mean_LAT", "emodnet_mean_MSL", "model_seabed_at_point_LAT", "model_asbuilt_at_point_LAT", "delta_emodnet_minus_model_seabed_at_point"]].round(2).to_string())

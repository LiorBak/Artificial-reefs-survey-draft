"""REST /depth_profile cross-check: the same shore-normal line (y = 0..500 m offshore of the frame origin) sent to
https://rest.emodnet-bathymetry.eu/depth_profile  -> 1000 equally spaced samples (cell values)."""
import sys, os, json, requests, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__)); import extract_site as E
for slug in ["boscombe-surf-reef", "borth-coastal-defence-reef"]:
    S = E.site_def(slug); fr = S["frame"]; x = S["centre_xy"][0]
    a = fr.xy2ll(x, 0); b = fr.xy2ll(x, 500)
    geom = f"LINESTRING({a[1]:.7f} {a[0]:.7f},{b[1]:.7f} {b[0]:.7f})"
    r = requests.get("https://rest.emodnet-bathymetry.eu/depth_profile", params={"geom": geom}, timeout=60)
    v = np.array(r.json(), float); y = np.linspace(0, 500, len(v))
    pd.DataFrame({"y_m": y.round(2), "x_m": round(x, 1), "emodnet_LAT_m": v}).to_csv(f"{E.DATA}/{slug}_profile_REST_depth_profile_y0_500.csv", index=False)
    runs = []; s = 0
    for i in range(1, len(v) + 1):
        if i == len(v) or v[i] != v[s]: runs.append((round(y[s]), round(y[i - 1]), round(float(v[s]), 3))); s = i
    print(slug, r.status_code, len(v), "samples; step runs (y_from, y_to, value):", runs, "\n GET", r.url[:200])

"""Step 6 (one line only): does EMODnet cover the coast near Haifa, and at what resolution? Points: Haifa port approach 32.83N 34.97E (shore ~34.99),
offshore 32.83N 34.90E and 32.83N 34.80E. REST depth_sample + ERDDAP cell + nearest HR composite DTM from data/hr_areas.json."""
import json, math, requests, io, pandas as pd, os
HERE = os.path.dirname(__file__); out = {}
pts = {"Haifa Bay shore (32.80N 35.00E)": (32.80, 35.00), "off Haifa 1 km (32.83N 34.96E)": (32.83, 34.96), "off Haifa 10 km (32.83N 34.85E)": (32.83, 34.85)}
for k, (la, lo) in pts.items():
    r = requests.get("https://rest.emodnet-bathymetry.eu/depth_sample", params={"geom": f"POINT({lo} {la})"}, timeout=60)
    out[k] = dict(status=r.status_code, body=(r.json() if r.status_code == 200 and r.text else None))
    q = f"[({la-0.0005}):({la+0.0005})][({lo-0.0005}):({lo+0.0005})]"
    e = requests.get("https://erddap.emodnet.eu/erddap/griddap/bathymetry_dtm_2024.csv?elevation" + q + ",value_count" + q + ",interpolation_flag" + q + ",cdi_index" + q, timeout=60)
    out[k]["erddap"] = e.text.strip().split("\n")[2:4] if e.status_code == 200 else e.status_code
hr = json.load(open(os.path.join(HERE, "..", "data", "hr_areas.json")))
la, lo = 32.83, 34.95
def dist(r):
    dx = max(r["w"] - lo, 0, lo - r["e"]) * 111.32 * math.cos(math.radians(la)); dy = max(r["s"] - la, 0, la - r["n"]) * 111.32; return math.hypot(dx, dy)
nn = sorted(hr, key=dist)[:3]; out["nearest_HR"] = [dict(id=r["id"], res=r["res"], dist_km=round(dist(r), 1), bbox=[round(r[k], 2) for k in "wsen"]) for r in nn]
qi = requests.get("https://ows.emodnet-bathymetry.eu/wfs", params=dict(service="WFS", version="2.0.0", request="GetFeature", typeNames="emodnet:quality_index", outputFormat="application/json",
     cql_filter=f"release='2024' AND INTERSECTS(geom, POINT(32.83 34.96))", propertyName="release,edmo_id,identifier,type,combined,horizontal,vertical,age,purpose"), timeout=60)
out["QI_2024_off_Haifa_1km"] = [f["properties"] for f in qi.json()["features"]] if qi.content[:1] == b"{" else qi.text[:200]
json.dump(out, open(os.path.join(HERE, "..", "data", "haifa_check.json"), "w"), indent=1)
print(json.dumps(out, indent=1))

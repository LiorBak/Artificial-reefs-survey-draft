# Step 3a: coverage test for the 13 reef coordinates (REST depth_sample + ERDDAP 2024 domain check)
import csv, json, requests, os
HERE = os.path.dirname(__file__)
rows = list(csv.DictReader(open(os.path.join(HERE, "..", "reefs_coords.csv"), encoding="utf-8")))
out = []
for r in rows:
    rec = dict(slug=r["slug"], lat=r["lat"], lon=r["lon"])
    if not r["lat"]:
        rec.update(rest_status="no coordinate", covered="no (no coordinate; Pacific Mexico is outside the DTM domain anyway)"); out.append(rec); continue
    lat, lon = float(r["lat"]), float(r["lon"])
    url = f"https://rest.emodnet-bathymetry.eu/depth_sample?geom=POINT({lon} {lat})"
    resp = requests.get(url, timeout=60)
    rec["rest_url"] = url; rec["rest_status"] = resp.status_code; rec["rest_body"] = resp.text[:400]
    in_domain = (-36.0 <= lon <= 43.0) and (15.0 <= lat <= 90.0)
    rec["inside_ERDDAP_2024_lon_lat_domain"] = in_domain
    out.append(rec); print(r["slug"], resp.status_code, resp.text[:200].replace("\n", " "), "| domain:", in_domain)
json.dump(out, open(os.path.join(HERE, "..", "data", "coverage_all_reefs.json"), "w"), indent=1)

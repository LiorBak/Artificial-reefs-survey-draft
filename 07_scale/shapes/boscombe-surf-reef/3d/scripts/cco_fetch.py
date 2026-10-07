"""Fetch Channel Coastal Observatory (Southeast Regional Coastal Monitoring Programme) beach-profile lines near the reef.

Run:  python scripts/cco_fetch.py
1. WFS GetFeature (layer national_profiles) with a bbox around the reef, EPSG:27700 -> list of profile lines + their line geometry.
2. For every line whose landward end lies within |x| <= 230 m of the reef origin (canonical frame): the profile API returns the dates that exist
   (JSON) and a zip of survey text files (Easting, Northing, Elevation_OD, Chainage, FC, Profile, Reg_ID) for the chosen dates.
Saves ../src/cco_profiles/<profile>_<date>.txt (raw, unchanged) + cco_lines.json (line geometry, canonical x/y of the line ends).
Source: https://coastalmonitoring.org/ (CCO). Licence: Open Government Licence v3.0; hydrographic data not for navigation.
"""
import json, re, sys, io, zipfile, urllib.request, urllib.parse
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from canon import osgb2can

OUT = HERE.parents[1] / "src" / "cco_profiles"; OUT.mkdir(parents=True, exist_ok=True)
WMS = "https://coastalmonitoring.org/maps?map=/home/www/cco/lib/services/maps/etc/main-wms.map"
API = "https://coastalmonitoring.org/cco/profiles/api.php"

def get(url, binary=False):
    with urllib.request.urlopen(url, timeout=90) as r:
        d = r.read()
    return d if binary else d.decode("utf8", "replace")

q = WMS + "&SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=national_profiles&COUNT=300&BBOX=410300,90500,412800,92200,urn:ogc:def:crs:EPSG::27700"
xml = get(q)
(OUT / "wfs_national_profiles_bbox.xml").write_text(xml, encoding="utf8")
lines = []
for m in re.finditer(r'<ms:national_profiles gml:id="[^"]*">(.*?)</ms:national_profiles>', xml, re.S):
    b = m.group(1)
    rid = re.search(r"<ms:regional_n>(.*?)<", b).group(1); su = re.search(r"<ms:su>(.*?)<", b).group(1)
    wkt = re.search(r"<ms:geometry_wkt>(.*?)<", b).group(1)
    nums = [float(v) for v in re.findall(r"[\d.]+", wkt)]
    e0, n0, e1, n1 = nums[0], nums[1], nums[-2], nums[-1]
    c0 = osgb2can([e0], [n0])[0]; c1 = osgb2can([e1], [n1])[0]
    lines.append(dict(id=rid, mu=su, e0=e0, n0=n0, e1=e1, n1=n1, can0=[round(float(c0[0]), 1), round(float(c0[1]), 1)], can1=[round(float(c1[0]), 1), round(float(c1[1]), 1)]))
sel = [l for l in lines if abs(l["can0"][0]) <= 230]
print("lines in bbox", len(lines), "selected (|x0|<=230):", [(l["id"], l["can0"], l["can1"]) for l in sel])
json.dump(dict(lines=sel, all_lines=lines), open(OUT / "cco_lines.json", "w"), indent=1)

for l in sel:
    pid = l["id"]
    try:
        d = json.loads(get(f"{API}?profile-id={pid}&mu={l['mu']}"))
    except Exception as e:
        print(pid, "no data", e); continue
    if "datasets" not in d:
        print(pid, "no datasets", str(d)[:80]); continue
    dates = sorted({ds["label"] for ds in d["datasets"]})
    z = get(f"{API}?profile-id={pid}&mu={l['mu']}&download_txt=1&selectedDatesArr=" + ",".join(dates), binary=True)
    zf = zipfile.ZipFile(io.BytesIO(z))
    for n in zf.namelist():
        (OUT / n.replace("profile_", "")).write_bytes(zf.read(n))
    print(pid, len(dates), "dates saved", dates[0], "..", dates[-1])

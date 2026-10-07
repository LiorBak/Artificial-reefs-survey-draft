# Step 1: collect best lat/lon for the 13 reefs (see METHOD.md). Reads project files, writes ../reefs_coords.csv
import json, csv, os
from shapely.geometry import Polygon
from shapely.ops import unary_union
R = r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git"
def card(s): return json.load(open(f"{R}/02_research/reefs/{s}.json", encoding="utf-8"))
def shape(s): return json.load(open(f"{R}/07_scale/shapes/{s}/shape.json", encoding="utf-8"))
def cent(polys):
    u = unary_union([Polygon([(lo, la) for la, lo in p]) for p in polys]); return u.centroid.y, u.centroid.x
rows = []
def add(slug, name, country, lat, lon, kind, src, note, acc):
    rows.append(dict(slug=slug, name=name, country=country, lat=None if lat is None else round(lat, 6), lon=None if lon is None else round(lon, 6),
                     coord_kind=kind, source_file=src, source_note=note, accuracy_m=acc))
# UK (covered region)
s = shape("boscombe-surf-reef"); c = s["geo"]["centroid_latlon"]
add("boscombe-surf-reef", "Boscombe Surf Reef", "UK", c[0], c[1], "reef outline centroid (traced)",
    "07_scale/shapes/boscombe-surf-reef/shape.json geo.centroid_latlon",
    "Traced bag-field outline on georeferenced Esri Wayback 2011-09-28 (source_id img1). Card lat/lon 50.7185,-1.8417 (latitude.to, 02_research/reefs/boscombe-surf-reef.json) lies ~310 m WNW of the traced reef (towards the pier) and is NOT used.", "5")
la, lo = cent(shape("borth-coastal-defence-reef")["geo"]["polygons_latlon"])
add("borth-coastal-defence-reef", "Borth coastal defence reef (multi-purpose reef, Phase 1)", "UK", la, lo, "reef outline centroid (traced, both mounds)",
    "07_scale/shapes/borth-coastal-defence-reef/shape.json geo.polygons_latlon (union centroid of 2 mounds)",
    "Traced from Esri World Imagery 2024-09-17 (sat2024). Card lat/lon 52.48533,-4.05103 is the Borth village centre (Wikipedia), not the reef, and is NOT used.", "5")
# non-UK, traced
s = shape("palm-beach-gold-coast"); c = s["geo"]["centroid_latlon"]
add("palm-beach-gold-coast", "Palm Beach Reef (Gold Coast)", "Australia", c[0], c[1], "reef outline centroid (traced to council polygon)",
    "07_scale/shapes/palm-beach-gold-coast/shape.json geo.centroid_latlon", "Aerial s7 registered to City of Gold Coast polygon; position ~1-2 m vs council data.", "2")
w = json.load(open(f"{R}/07_scale/shapes/mount-maunganui-reef/work_canonical_v2.json", encoding="utf-8"))
c = w["survey_centroid_latlon"]
add("mount-maunganui-reef", "Mount Maunganui reef", "New Zealand", c[0], c[1], "2013 multibeam bag-field centroid (traced, work file)",
    "07_scale/shapes/mount-maunganui-reef/work_canonical_v2.json survey_centroid_latlon",
    "BoPRC Fig 3 (July 2013 multibeam, EPSG:2106) registered to Esri 2011; card lat/lon is null (only town centre 37 39 35 S 176 12 53 E given).", "10")
b = shape("bunbury-airwave")["location_note"]
add("bunbury-airwave", "Bunbury Airwave (Back Beach)", "Australia", b["approx_centre_latlon"][0], b["approx_centre_latlon"][1], "approximate centre (not traced)",
    "07_scale/shapes/bunbury-airwave/shape.json location_note.approx_centre_latlon", f"uncertainty_m={b['uncertainty_m']}; {b['method'][:160]}", str(b["uncertainty_m"]))
d = shape("prattes-reef-el-segundo"); k = card("prattes-reef-el-segundo")
add("prattes-reef-el-segundo", "Pratte's Reef (El Segundo)", "USA", k["lat"], k["lon"], "card coordinate (published, not tied to structure)",
    "02_research/reefs/prattes-reef-el-segundo.json lat/lon; shape.json geo_note says 3 published coordinates disagree by up to 313 m",
    "Reef removed 2008-2010; no traced position. Alternatives in geo_note: Gemini 33.9162,-118.4312 (unverified, not used); RWR page 33.913666,-118.429733.", "300")
# card coordinates
cards = [
 ("narrowneck-gold-coast", "Australia", "card lat/lon (Wikipedia Narrow Neck QLD, 27 59 11 S 153 25 47 E)", "Isthmus coordinate; reef ~100-200 m offshore, not traced.", "300"),
 ("cables-reef-wa", "Australia", "card lat/lon (surf-forecast.com generic break coordinate)", "Card md: generic surf-break coordinates, not a surveyed structure position.", "1000"),
 ("opunake-reef", "New Zealand", "card lat/lon (surf-forecast.com Opunake Beach break)", "Township 39.450 S 173.850 E; break 39.46 S 173.86 E.", "1500"),
 ("kovalam-reef-india", "India", "card lat/lon (Wikipedia Kovalam, 8 24 01 N 76 58 43 E)", "Town coordinate; no reef coordinate found.", "1000"),
 ("southern-ocean-surf-reef-albany", "Australia", "card lat/lon (Wikipedia Middleton Beach, 35 01 25 S 117 54 49 E)", "Beach coordinate; reef ~140 m offshore, 150 m N of Surfer's Beach car park.", "300"),
]
names = {"narrowneck-gold-coast":"Narrowneck Reef (Gold Coast)","cables-reef-wa":"Cables Reef (Perth, WA)","opunake-reef":"Opunake Reef (Taranaki)","kovalam-reef-india":"Kovalam reef (Kerala)","southern-ocean-surf-reef-albany":"Southern Ocean Surf Reef (Albany, WA)"}
for slug, ctry, kind, note, acc in cards:
    k = card(slug); add(slug, names[slug], ctry, k["lat"], k["lon"], kind, f"02_research/reefs/{slug}.json lat/lon", note, acc)
k = card("burkitts-reef-bargara")
add("burkitts-reef-bargara", "Burkitts Reef (Bargara)", "Australia", -abs(k["lat"]), k["lon"], "card lat/lon (Bargara town centre, Wikipedia) with SIGN FIXED",
    "02_research/reefs/burkitts-reef-bargara.json lat/lon", "Card JSON stores +24.8205 (north) but the card text says 24 49 14 S: latitude negated here. Town centre; reef coordinates not found.", "1000")
add("mexico-reef-2026-unnamed", "Xala reef (Costalegre, Jalisco)", "Mexico", None, None, "NONE - no coordinate in any verified source",
    "02_research/reefs/mexico-reef-2026-unnamed.json lat/lon = null", "Card md: 'Exact reef coordinates: not found'. Costalegre coast of Jalisco, Pacific side: outside EMODnet regardless. Gemini coordinates not used (rule 2).", "")
order = ["narrowneck-gold-coast","cables-reef-wa","prattes-reef-el-segundo","mount-maunganui-reef","opunake-reef","boscombe-surf-reef","kovalam-reef-india","borth-coastal-defence-reef","palm-beach-gold-coast","southern-ocean-surf-reef-albany","burkitts-reef-bargara","bunbury-airwave","mexico-reef-2026-unnamed"]
rows.sort(key=lambda r: order.index(r["slug"]))
out = os.path.join(os.path.dirname(__file__), "..", "reefs_coords.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for r in rows: print(r["slug"], r["lat"], r["lon"], r["coord_kind"])

"""cables-reef-wa: (1) shoreline bearing and anchor-to-shore distance from the DoT Perth_5m clip (0 m AHD); (2) Fremantle MSL above gauge zero from the BoM NTC monthly table.
Writes shore_datum.json. numpy, scipy only. Inputs: ../src/bathymetry/DoT_Perth_5m_clip_reef.npz, georef.json, ../src/datum/BoM_NTC_Fremantle_monthly_sea_levels_2026-10-10.html"""
import json, re, numpy as np, collections
HERE = __file__.rsplit('/', 1)[0]
G = json.load(open(HERE + '/georef.json'))['transform']; E0, N0 = G['anchor_E_MGA50_GDA94'], G['anchor_N_MGA50_GDA94']
z = np.load(HERE + '/../src/bathymetry/DoT_Perth_5m_clip_reef.npz'); a = z['z_AHD'].astype(float); xl, yt, px = float(z['x_left']), float(z['y_top']), float(z['pixel'])
def val(E, N):
    c = int((E - xl) / px); r = int((yt - N) / px); v = a[r, c]; return np.nan if v < -9000 else v
dist = {}
for br in (80, 90, 100):
    d = 0.0
    for d in np.arange(0, 560, 1.0):
        v = val(E0 + d * np.sin(np.radians(br)), N0 + d * np.cos(np.radians(br)))
        if np.isnan(v) or v >= 0: break
    dist[str(br)] = round(float(d), 0)
cols, rows = [], []
for r in range(0, a.shape[0], 4):
    row = a[r]; w = np.where((row >= 0) & (row < 100))[0]
    if len(w): cols.append(xl + w[0] * px); rows.append(yt - r * px)
rows = np.array(rows); cols = np.array(cols); m = abs(rows - N0) < 400
p = np.polyfit(rows[m], cols[m], 1); brg = float(np.degrees(np.arctan2(p[0], 1)) % 360)
t = open(HERE + '/../src/datum/BoM_NTC_Fremantle_monthly_sea_levels_2026-10-10.html', errors='ignore').read()
t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S); t = re.sub(r'<[^>]+>', ' ', t).replace('&nbsp;', ' '); t = re.sub(r'\s+', ' ', t)
body = t[t.index('Monthly sea levels for Fremantle Mth'):]
rows_ = re.findall(r'(\d+) (\d{4}) (\d+) (\d+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)', body)
y = collections.defaultdict(list)
for r in rows_: y[int(r[1])].append(float(r[6]))
ann = {k: np.mean(v) for k, v in y.items() if len(v) >= 10 and 1992 <= k <= 2011}
stats = re.search(r'Mean sea level = ([\d.]+).*?Maximum recorded level of ([\d.]+) metres at (\d+ hours \d+/\d+/\d+).*?Minimum recorded level of (-?[\d.]+) metres at (\d+ hours \d+/\d+/\d+)', body)
out = {"anchor_to_0mAHD_m_by_bearing_deg": dist, "shoreline_bearing_deg_T": round(brg, 1), "shoreline_fit_rows": int(m.sum()),
       "BoM_Fremantle_MSL_above_gauge_zero_mean_of_annual_means_1992_2011_m": round(float(np.mean(list(ann.values()))), 3), "n_years": len(ann),
       "BoM_page_mean_sea_level_all_record_m": float(stats.group(1)), "BoM_page_max_recorded_m": float(stats.group(2)), "BoM_page_max_when": stats.group(3), "BoM_page_min_recorded_m": float(stats.group(4)), "BoM_page_min_when": stats.group(5),
       "note": "gauge zero = Fremantle Low Water Datum (BoM NTC metadata 62230); monthly means are above that zero; the page's year labels start at 1900 (as printed)"}
json.dump(out, open(HERE + '/shore_datum.json', 'w'), indent=1); print(json.dumps(out, indent=1))

"""Step 4: extract EMODnet Bathymetry DTM 2024 depths for one covered reef (see METHOD.md).
Usage: python extract_site.py boscombe-surf-reef | borth-coastal-defence-reef
Writes data/<slug>_*.csv and data/<slug>_results.json.  All numbers are metres relative to LAT (EMODnet vertical reference)
unless a column name says otherwise.  Only small bounding boxes are requested (a few KB each).
"""
import json, csv, os, io, math, sys, time
import numpy as np, pandas as pd, requests, tifffile
from pyproj import Geod
from matplotlib.path import Path as MPath
from shapely.geometry import Polygon, LineString, Point
from shapely.ops import unary_union

ROOT = r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git"
OUT = os.path.join(ROOT, "07_scale", "bathymetry", "emodnet")
DATA = os.path.join(OUT, "data")
SCRATCH = os.path.join(os.environ["TEMP"], "emodnet_scratch")
geod = Geod(ellps="WGS84")
ERDDAP = "https://erddap.emodnet.eu/erddap/griddap/bathymetry_dtm_2024.csv"
WCS = "https://ows.emodnet-bathymetry.eu/wcs"
WFS = "https://ows.emodnet-bathymetry.eu/wfs"
REST = "https://rest.emodnet-bathymetry.eu"
MARIS = "http://geo-service.maris.nl/emodnet_bathymetry/wfs"
VARS = ["elevation", "value_count", "cdi_index", "interpolation_flag", "elevation_min", "elevation_max", "stdev"]
RELEASES = {"2016": "emodnet__mean_2016", "2018": "emodnet__mean_2018", "2020": "emodnet__mean_2020", "2022": "emodnet__mean_2022", "2024": "emodnet__mean"}
LOG = []


def log(*a):
    s = " ".join(str(x) for x in a); print(s); LOG.append(s)


# ---------------------------------------------------------------- grid helpers (EMODnet DTM lattice: 1/960 deg, centres at k+0.5)
def cell_k(lat, lon):
    return int(math.floor((lat - 15.0) * 960)), int(math.floor((lon + 36.0) * 960))


def cell_centre(ki, kj):
    return 15.0 + (ki + 0.5) / 960, -36.0 + (kj + 0.5) / 960


def cell_size_m(lat):
    return 111_132.9 / 960, 111_320.0 * math.cos(math.radians(lat)) / 960   # dN-S, dE-W (approx)


class Frame:
    """canonical frame of shape.json: x along bearing bx, y along bearing by (degrees true), origin lat0, lon0."""
    def __init__(s, lat0, lon0, bx, by):
        s.lat0, s.lon0, s.bx, s.by = lat0, lon0, math.radians(bx), math.radians(by)
        s.A = np.array([[math.sin(s.bx), math.sin(s.by)], [math.cos(s.bx), math.cos(s.by)]])  # [E,N] = A [x,y]

    def xy2ll(s, x, y):
        e, n = s.A @ np.array([x, y]); d = math.hypot(e, n); az = math.degrees(math.atan2(e, n)) % 360
        lon, lat, _ = geod.fwd(s.lon0, s.lat0, az, d); return lat, lon

    def ll2xy(s, lat, lon):
        az, _, d = geod.inv(s.lon0, s.lat0, lon, lat); e, n = d * math.sin(math.radians(az)), d * math.cos(math.radians(az))
        x, y = np.linalg.solve(s.A, np.array([e, n])); return float(x), float(y)

    def bearing_x(s): return math.degrees(s.bx)


# ---------------------------------------------------------------- site definitions
def site_def(slug):
    shape = json.load(open(f"{ROOT}/07_scale/shapes/{slug}/shape.json", encoding="utf-8"))
    polys = shape["canonical"]["polygons_m"]
    if slug == "boscombe-surf-reef":
        fr = Frame(50.719552, -1.839278, 83.4, 173.4)
        reefpoly = [Polygon(p) for p in polys]
        centre = unary_union(reefpoly).centroid
        pts = [  # REQUESTS_FOR_LIOR.md points of the Boscombe 3d folder (lat, lon from that file)
            ("centre_outline_centroid", "reef centre", (50.717532, -1.838909)),
            ("drying_patch_centre", "reef (Navionics drying patch centre)", (50.717704, -1.838728)),
            ("survey_peak_Apr2011", "reef crest (survey peak)", (50.717851, -1.838682)),
            ("toe_shoreward", "toe", (50.718010, -1.838597)),
            ("toe_west_flank", "toe", (50.717505, -1.839447)),
            ("toe_east_flank", "toe", (50.717817, -1.838276)),
            ("toe_offshore_tail", "toe", (50.717033, -1.839104)),
            ("seabed_y100", "seabed", (50.71866, -1.839115)),
            ("seabed_y320", "seabed", (50.716697, -1.838757)),
            ("seabed_80m_west", "seabed", (50.717462, -1.840039)),
            ("seabed_90m_east", "seabed", (50.717726, -1.837660)),
        ]
        named = [(n, role, fr.ll2xy(la, lo), (la, lo)) for n, role, (la, lo) in pts]
        extra_profiles = []
    elif slug == "borth-coastal-defence-reef":
        fr = Frame(52.483475, -4.05134, 359.57, 269.57)
        reefpoly = [Polygon(p) for p in polys]
        centre = unary_union(reefpoly).centroid
        named = []
        named.append(("centre_both_mounds", "reef centre", (centre.x, centre.y), None))
        for nm, pg in zip(["N_hook", "S_oval"], reefpoly):
            c = pg.centroid
            lnorm = LineString([(c.x, -50), (c.x, 700)]).intersection(pg); b = lnorm.bounds   # (minx,miny,maxx,maxy)
            lalong = LineString([(-300, c.y), (300, c.y)]).intersection(pg); a = lalong.bounds
            named += [(f"{nm}_centre", "mound centre", (c.x, c.y), None),
                      (f"{nm}_toe_shoreward", "toe", (c.x, b[1]), None),
                      (f"{nm}_toe_seaward", "toe", (c.x, b[3]), None),
                      (f"{nm}_toe_north", "toe", (a[2], c.y), None),
                      (f"{nm}_toe_south", "toe", (a[0], c.y), None),
                      (f"{nm}_seabed_60m_shoreward", "seabed", (c.x, b[1] - 60), None),
                      (f"{nm}_seabed_60m_seaward", "seabed", (c.x, b[3] + 60), None)]
        named.append(("gap_between_mounds", "seabed", ((reefpoly[0].centroid.x + reefpoly[1].centroid.x) / 2, (reefpoly[0].centroid.y + reefpoly[1].centroid.y) / 2), None))
        named = [(n, r, xy, fr.xy2ll(*xy)) for n, r, xy, _ in named]
        extra_profiles = [("N_hook_centre", reefpoly[0].centroid.x), ("S_oval_centre", reefpoly[1].centroid.x)]
    else:
        raise SystemExit("unknown slug")
    return dict(slug=slug, shape=shape, frame=fr, polys=polys, reefpoly=reefpoly, centre_xy=(centre.x, centre.y),
                centre_ll=fr.xy2ll(centre.x, centre.y), named=named, extra_profiles=extra_profiles,
                shore_bearing=shape["geo"]["shoreline_bearing_deg"])


# ---------------------------------------------------------------- data access
def get(url, **kw):
    for k in range(3):
        try:
            r = requests.get(url, timeout=120, **kw)
            if r.status_code in (200, 204): return r
        except Exception as e:
            err = e
        time.sleep(2)
    raise RuntimeError(f"failed {url}")


def erddap_box(lat_a, lat_b, lon_a, lon_b):
    q = f"[({lat_a:.6f}):({lat_b:.6f})][({lon_a:.6f}):({lon_b:.6f})]"
    url = ERDDAP + "?" + ",".join(v + q for v in VARS)
    r = get(url); log("ERDDAP", url[:140] + "...", r.status_code, len(r.content), "bytes")
    df = pd.read_csv(io.StringIO(r.text), skiprows=[1])
    df["ki"] = np.floor((df.latitude - 15.0) * 960).astype(int); df["kj"] = np.floor((df.longitude + 36.0) * 960).astype(int)
    return df, url


def wcs_box(cov, lat_a, lat_b, lon_a, lon_b):
    params = [("service", "WCS"), ("version", "2.0.1"), ("request", "GetCoverage"), ("coverageId", cov), ("format", "image/tiff"),
              ("subset", f"Lat({lat_a:.6f},{lat_b:.6f})"), ("subset", f"Long({lon_a:.6f},{lon_b:.6f})")]
    r = get(WCS, params=params); log("WCS", cov, r.status_code, len(r.content), "bytes")
    return tifffile.imread(io.BytesIO(r.content)).astype(float)


def align_wcs(W, ref, allkeys):
    """find ki_top, kj_left so that W[r,c] = cell (ki_top-r, kj_left+c) best matches the ERDDAP reference dict {(ki,kj):elev}"""
    kis = [k[0] for k in allkeys]; kjs = [k[1] for k in allkeys]; best = None
    for kt in range(max(kis) - 4, max(kis) + 5):
        for kl in range(min(kjs) - 4, min(kjs) + 5):
            d = []
            for (ki, kj), v in ref.items():
                r, c = kt - ki, kj - kl
                if 0 <= r < W.shape[0] and 0 <= c < W.shape[1] and not np.isnan(W[r, c]): d.append(abs(W[r, c] - v))
            if len(d) > 50 and (best is None or np.mean(d) < best[0]): best = (np.mean(d), kt, kl, len(d))
    return best


def rest_point(lat, lon):
    r = get(f"{REST}/depth_sample", params={"geom": f"POINT({lon:.7f} {lat:.7f})"})
    return r.json() if r.status_code == 200 and r.text else {}


def wfs_json(typ, cql, props):
    p = dict(service="WFS", version="2.0.0", request="GetFeature", typeNames=typ, outputFormat="application/json", cql_filter=cql, propertyName=props)
    r = get(WFS, params=p)
    return [f["properties"] for f in r.json()["features"]] if r.content[:1] == b"{" else []


def maris(layer, bbox):
    p = dict(service="WFS", version="2.0.0", request="GetFeature", typeNames="emodnet_bathymetry:" + layer, outputFormat="application/json", count=50,
             bbox=f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]},urn:ogc:def:crs:EPSG::4326")
    r = requests.get(MARIS, params=p, timeout=90)
    try: return [f["properties"] for f in r.json()["features"]]
    except Exception: return []


# ---------------------------------------------------------------- main
def main(slug):
    S = site_def(slug); fr = S["frame"]; os.makedirs(DATA, exist_ok=True)
    lat_c, lon_c = S["centre_ll"]
    log(f"== {slug}: reef centre canonical {S['centre_xy'][0]:.1f},{S['centre_xy'][1]:.1f} -> lat/lon {lat_c:.6f},{lon_c:.6f}; shoreline bearing {S['shore_bearing']}")
    dN, dE = cell_size_m(lat_c); log(f"cell size at {lat_c:.3f} N: {dN:.1f} m (N-S) x {dE:.1f} m (E-W)")

    # ---- bbox: profile (y -100..650) + points, +0.003 deg margin
    ys = np.arange(-100, 650.1, 5.0)
    xp = S["centre_xy"][0]
    pl = [fr.xy2ll(xp, y) for y in ys]
    all_ll = pl + [n[3] for n in S["named"]] + [fr.xy2ll(*p) for poly in S["polys"] for p in poly]
    lat_a, lat_b = min(a[0] for a in all_ll) - 0.003, max(a[0] for a in all_ll) + 0.003
    lon_a, lon_b = min(a[1] for a in all_ll) - 0.004, max(a[1] for a in all_ll) + 0.004
    # snap to cell centres
    ka, kb = cell_k(lat_a, lon_a), cell_k(lat_b, lon_b)
    la_c = cell_centre(ka[0], 0)[0]; lb_c = cell_centre(kb[0], 0)[0]; lo_c = cell_centre(0, ka[1])[1]; lp_c = cell_centre(0, kb[1])[1]
    df, url = erddap_box(la_c, lb_c, lo_c, lp_c)
    cells = {(int(r.ki), int(r.kj)): r for r in df.itertuples()}
    ref = {k: r.elevation for k, r in cells.items() if not np.isnan(r.elevation)}
    log(f"ERDDAP cells {len(df)}, valid (sea) {len(ref)}, masked (land / outside) {len(df) - len(ref)}")
    df.drop(columns=["ki", "kj"]).to_csv(f"{DATA}/{slug}_cells_dtm2024_erddap.csv", index=False)

    # ---- WCS releases (also gives land / foreshore values that ERDDAP masks)
    wcs = {}
    for rel, cov in RELEASES.items():
        W = wcs_box(cov, la_c, lb_c, lo_c, lp_c)
        if rel == "2024":
            best = align_wcs(W, ref, list(cells.keys())); log("WCS alignment vs ERDDAP (mean abs diff, ki_top, kj_left, n):", best)
            assert best[0] < 1e-3, "WCS/ERDDAP misaligned"
            kt, kl = best[1], best[2]
        wcs[rel] = W
    def wcs_val(rel, ki, kj):
        r, c = kt - ki, kj - kl; W = wcs[rel]
        return float(W[r, c]) if 0 <= r < W.shape[0] and 0 <= c < W.shape[1] else float("nan")
    rows = []
    for (ki, kj), r in sorted(cells.items()):
        la, lo = cell_centre(ki, kj); x, y = fr.ll2xy(la, lo)
        rows.append(dict(ki=ki, kj=kj, lat=la, lon=lo, x_m=round(x, 1), y_m=round(y, 1), erddap_elev=r.elevation, **{f"wcs_{k}": wcs_val(k, ki, kj) for k in RELEASES}))
    pd.DataFrame(rows).to_csv(f"{DATA}/{slug}_cells_releases_wcs.csv", index=False)

    def cell_info(lat, lon):
        ki, kj = cell_k(lat, lon); r = cells.get((ki, kj)); la, lo = cell_centre(ki, kj)
        d = dict(cell_ki=ki, cell_kj=kj, cell_lat=round(la, 6), cell_lon=round(lo, 6))
        if r is not None and not np.isnan(r.elevation):
            d.update(elev_LAT_m=float(r.elevation), elev_min=float(r.elevation_min), elev_max=float(r.elevation_max), stdev=float(r.stdev),
                     value_count=int(r.value_count), cdi_index=int(r.cdi_index) if not np.isnan(r.cdi_index) else None,
                     interpolated=bool(r.interpolation_flag == 1), status="ERDDAP DTM2024 sea cell")
        else:
            d.update(elev_LAT_m=wcs_val("2024", ki, kj), status="ERDDAP masked (land/foreshore): value from WCS emodnet__mean")
        d.update({f"wcs_{k}": wcs_val(k, ki, kj) for k in RELEASES})
        return d

    # ---- named points
    prow = []
    for name, role, (x, y), (la, lo) in S["named"]:
        d = dict(point=name, role=role, x_m=round(x, 1), y_m=round(y, 1), lat=round(la, 7), lon=round(lo, 7)); d.update(cell_info(la, lo))
        rj = rest_point(la, lo); time.sleep(0.15)
        d.update(rest_avg=rj.get("avg"), rest_min=rj.get("min"), rest_max=rj.get("max"), rest_stdev=rj.get("stdev"), rest_elementary=rj.get("elementarySurfaces"),
                 rest_interpolationType=rj.get("interpolationType"), rest_smoothed=rj.get("smoothed"),
                 rest_ref_type=(rj.get("reference") or {}).get("type"), rest_ref_edmo=(rj.get("reference") or {}).get("organisation_id"),
                 rest_ref_id=(rj.get("reference") or {}).get("identifier"))
        sr = wfs_json("emodnet:source_references", f"release='2024' AND INTERSECTS(geom, POINT({la} {lo}))", "release,edmo_id,identifier,type,device")
        d.update(wfs2024_ref_id=";".join(str(s.get("identifier")) for s in sr), wfs2024_ref_type=";".join(str(s.get("type")) for s in sr))
        prow.append(d)
    pd.DataFrame(prow).to_csv(f"{DATA}/{slug}_points_emodnet.csv", index=False)
    log("points written:", len(prow))

    # ---- quality index history at the reef centre (all releases, no geometry)
    qi = wfs_json("emodnet:quality_index", f"INTERSECTS(geom, POINT({lat_c} {lon_c}))", "release,edmo_id,identifier,type,combined,horizontal,vertical,age,purpose")
    sr_all = wfs_json("emodnet:source_references", f"INTERSECTS(geom, POINT({lat_c} {lon_c}))", "release,edmo_id,identifier,type,date_start")
    # ---- patches and CDI polygons within +-1.5 km
    bb = (lat_c - 0.0135, lon_c - 0.0135 / math.cos(math.radians(lat_c)), lat_c + 0.0135, lon_c + 0.0135 / math.cos(math.radians(lat_c)))
    patches = wfs_json("emodnet:source_references", f"release='2024' AND BBOX(geom,{bb[1]},{bb[0]},{bb[3]},{bb[2]},'EPSG:4326')", "release,edmo_id,identifier,type,device,metadata_url")
    qi_box = wfs_json("emodnet:quality_index", f"release='2024' AND BBOX(geom,{bb[1]},{bb[0]},{bb[3]},{bb[2]},'EPSG:4326')", "release,edmo_id,identifier,type,combined,horizontal,vertical,age,purpose")
    cdi_poly = maris("polygons", bb); cdi_pts = maris("points", bb); cdi_trk = maris("tracks", bb)
    log("2024 source patches in 3 km box:", patches); log("CDI polygons:", [(p["n_code"], p["dataname"], p["c_author_edmo"]) for p in cdi_poly])

    # ---- high-resolution composite DTMs: nearest ones
    hr = json.load(open(f"{DATA}/hr_areas.json"))
    def dist_km(r):
        dx = max(r["w"] - lon_c, 0, lon_c - r["e"]) * 111.32 * math.cos(math.radians(lat_c)); dy = max(r["s"] - lat_c, 0, lat_c - r["n"]) * 111.32
        return math.hypot(dx, dy)
    nearest = sorted(hr, key=dist_km)[:5]
    hr_near = [dict(id=r["id"], edmo=r["edmo"], res_arcmin_1_over=r["res"], release=r["rel"], bbox=[round(r[k], 3) for k in "wsen"], dist_km=round(dist_km(r), 1), meta=r["meta"]) for r in nearest]

    # ---- profile(s)
    def profile(xline, tag):
        out = []
        for y in ys:
            la, lo = fr.xy2ll(xline, y); d = dict(y_m=y, x_m=xline, lat=round(la, 7), lon=round(lo, 7)); d.update(cell_info(la, lo)); out.append(d)
        # bilinear on cell-centre lattice (uses WCS-filled values where ERDDAP is masked) - for plotting only
        for d in out:
            fi = (d["lat"] - 15.0) * 960 - 0.5; fj = (d["lon"] + 36.0) * 960 - 0.5; i0, j0 = int(math.floor(fi)), int(math.floor(fj)); a, b = fi - i0, fj - j0
            v = [wcs_val("2024", i0, j0), wcs_val("2024", i0 + 1, j0), wcs_val("2024", i0, j0 + 1), wcs_val("2024", i0 + 1, j0 + 1)]
            d["bilinear_LAT_m"] = (v[0] * (1 - a) * (1 - b) + v[1] * a * (1 - b) + v[2] * (1 - a) * b + v[3] * a * b) if not any(np.isnan(v)) else None
        return out
    prof = profile(xp, "centre"); extra = {}
    for tag, xl in S["extra_profiles"]: extra[tag] = profile(xl, tag)
    return S, fr, ys, prof, extra, cells, prow, qi, sr_all, patches, qi_box, cdi_poly, cdi_pts, cdi_trk, hr_near, (dN, dE), url, wcs_val


if __name__ == "__main__":
    slug = sys.argv[1]
    S, fr, ys, prof, extra, cells, prow, qi, sr_all, patches, qi_box, cdi_poly, cdi_pts, cdi_trk, hr_near, csz, url, wcs_val = main(slug)
    pd.DataFrame(prof).to_csv(f"{DATA}/{slug}_profile_through_reef_centre.csv", index=False)
    for tag, p in extra.items(): pd.DataFrame(p).to_csv(f"{DATA}/{slug}_profile_through_{tag}.csv", index=False)
    res = dict(slug=slug, reef_centre_xy=S["centre_xy"], reef_centre_ll=S["centre_ll"], frame=dict(lat0=fr.lat0, lon0=fr.lon0, bx=math.degrees(fr.bx), by=math.degrees(fr.by)),
               cell_size_m=dict(NS=csz[0], EW=csz[1]), erddap_url=url, qi_history=qi, source_ref_history=sr_all, patches_2024_3km=patches, qi_2024_3km=qi_box,
               cdi_polygons=cdi_poly, cdi_points_n=len(cdi_pts), cdi_tracks_n=len(cdi_trk), hr_nearest=hr_near)
    json.dump(res, open(f"{DATA}/{slug}_results.json", "w"), indent=1, default=str)
    open(f"{DATA}/{slug}_extract_log.txt", "w", encoding="utf-8").write("\n".join(LOG))
    print("done")

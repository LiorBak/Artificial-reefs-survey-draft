# Burkitts Reef: photo-trace of visible rock platform. px -> lat/lon (Web Mercator, bounds from the .geo.json sidecar) -> UTM 56S metres.
import json, math, sys
from pyproj import Transformer, Geod
from shapely.geometry import Polygon
here = sys.argv[1]
geo = json.load(open(f'{here}/src/burkitts_esri_2025-09-05_z19.png.geo.json'))
poly = json.load(open(f'{here}/scripts/pixel_polygon_v1.json'))[0]
W, H = geo['width'], geo['height']; b = geo['bounds']
R = 6378137.0
my = lambda lat: math.log(math.tan(math.pi/4 + math.radians(lat)/2))
iy = lambda y: math.degrees(2*math.atan(math.exp(y)) - math.pi/2)
def px2ll(x, y):
    lon = b['west'] + (b['east']-b['west'])*x/W
    ymerc = my(b['north']) + (my(b['south'])-my(b['north']))*y/H
    return iy(ymerc), lon
ll = [px2ll(x, y) for x, y in poly]
tr = Transformer.from_crs(4326, 32756, always_xy=True)
utm = [tr.transform(lo, la) for la, lo in ll]
# local frame: origin = polygon centroid in UTM; +x east, +y north
P = Polygon(utm); c = P.centroid
loc = [(round(x-c.x, 2), round(y-c.y, 2)) for x, y in utm]
Pl = Polygon(loc)
g = Geod(ellps='WGS84')
area_geod = abs(g.polygon_area_perimeter([lo for la, lo in ll], [la for la, lo in ll])[0])
minx, miny, maxx, maxy = Pl.bounds
# pixel-scale check
px_area = Polygon(poly).area
out = dict(area_utm56s_m2=round(P.area, 1), area_geodesic_m2=round(area_geod, 1),
           area_px2_x_mpp2=round(px_area*geo['m_per_px_center']**2, 1),
           bbox_m=[round(maxx-minx, 1), round(maxy-miny, 1)], centroid_latlon=list(px2ll(*Polygon(poly).centroid.coords[0])),
           ll=[[round(a, 7), round(o, 7)] for a, o in ll], local_m=[list(p) for p in loc],
           perimeter_m=round(P.length, 1))
# per-edge scale: metres per pixel at image centre from the bounds
mid = (b['north']+b['south'])/2
out['m_per_px_from_bounds'] = round((b['east']-b['west'])*math.pi/180*R*math.cos(math.radians(mid))/W, 4)
json.dump(out, open(f'{here}/scripts/computed_v1.json', 'w'), indent=1)
print({k: v for k, v in out.items() if k not in ('ll', 'local_m')})

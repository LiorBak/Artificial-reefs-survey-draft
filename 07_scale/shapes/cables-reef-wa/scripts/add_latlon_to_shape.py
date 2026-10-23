"""cables-reef-wa: add polygons_latlon / centroid_latlon / shoreline_bearing_deg (the keys the page reads, as in the other shapes) to shape.json['geo'].
Original-plan outline (the default) transformed with georef.json; GDA94 treated as WGS84 (difference about 1.8 m). Run after add_geo_to_shape.py."""
import json, numpy as np
exec(open(__file__.rsplit('/', 1)[0] + '/georef_fit.py').read().split("res = differential_evolution")[0])
G = json.load(open(HERE + '/georef.json'))['transform']; th, tx, ty = G['theta_ccw_deg'], G['anchor_E_MGA50_GDA94'] - CX, G['anchor_N_MGA50_GDA94'] - CY
W = world(poly0, th, tx, ty); ll = [Ti.transform(CX + x, CY + y) for x, y in W]
from shapely.geometry import Polygon
c = Polygon(W).centroid; clon, clat = Ti.transform(CX + c.x, CY + c.y)
d = json.load(open(HERE + '/../shape.json')); g = d['geo']
g['polygons_latlon'] = [[[round(la, 7), round(lo, 7)] for lo, la in ll]]; g['centroid_latlon'] = [round(clat, 6), round(clon, 6)]
g['shoreline_bearing_deg'] = json.load(open(HERE + '/shore_datum.json'))['shoreline_bearing_deg_T']; g['source_id'] = 'DoT1999'
g['polygons_note'] = 'default outline = original design plan; GDA94 coordinates treated as WGS84 (about 1.8 m difference)'
json.dump(d, open(HERE + '/../shape.json', 'w'), indent=1, ensure_ascii=False); print(g['centroid_latlon'])

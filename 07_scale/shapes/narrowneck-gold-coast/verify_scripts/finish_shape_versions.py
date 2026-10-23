"""finish_shape_versions.py (2026-10-10): write outline_versions, default_outline, versions_info, faint_seaward_patches, sources s13/s14 and the new confidence
reason into shape.json (idempotent). Inputs: design_outline_2004.json, navionics_polys.json, option2/option2_outline.json, survey2011/relief_zone.json, faint/faint_patches.json."""
import json, os, math
from shapely.geometry import Polygon
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(HERE)
sh=json.load(open(ROOT+"/shape.json"))
geo=json.load(open(ROOT+"/src/wayback/nn_wayback_2020-08-08_r9812_z19.png.geo.json"))["bounds"]
b=math.radians(356.212); u=(math.sin(b),-math.cos(b)); nn=(math.sin(b+math.pi/2),-math.cos(b+math.pi/2)); org=(-517.90,821.74); mpp=0.263665
def my(lat): return math.log(math.tan(math.pi/4+math.radians(lat)/2))
def ll(p):
    x,y=p; px=org[0]+(x*u[0]+y*nn[0])/mpp; py=org[1]+(x*u[1]+y*nn[1])/mpp
    lon=geo["west"]+px/1517*(geo["east"]-geo["west"]); m=my(geo["north"])+py/1517*(my(geo["south"])-my(geo["north"]))
    return [round(math.degrees(2*math.atan(math.exp(m))-math.pi/2),7),round(lon,7)]
def bbox(polys):
    xs=[p[0] for q in polys for p in q]; ys=[p[1] for q in polys for p in q]; return [round(max(ys)-min(ys),1),round(max(xs)-min(xs),1)]  # [cross-shore extent, alongshore extent]
def area(polys): return round(sum(Polygon(q).buffer(0).area for q in polys))
d04=json.load(open(HERE+"/design_outline_2004.json")); nav=json.load(open(HERE+"/navionics_polys.json"))
o2=json.load(open(HERE+"/option2/option2_outline.json")); rz=json.load(open(HERE+"/survey2011/relief_zone.json"))["0.14"]
fp=[p for p in json.load(open(HERE+"/faint/faint_patches.json")) if p["centroid_m"][1]>=241]
photo=sh["canonical"]["polygons_m"]
V=[]
V.append({"id":"photo_2020-08-08","name":"Renewed reef as seen on the 2020 aerial photo (visible container field, 8 Aug 2020)","date":"2020-08-08","kind":"photo_trace",
 "source_ids":["s3","s4"],"method":"Dark container patches thresholded on the 0.26 m/px Esri Wayback r9812 image (G<49), closed r=3.7 m, traced polygons; georeferenced from tile bounds; checked on the 2022 tile (0.2 m).",
 "level":"visible container field after the 2017-18 renewal (down to about the -6 m contour; the deeper toe is not visible, so this is a LOWER BOUND)",
 "area_m2":area(photo),"bbox_m":bbox(photo),"polygons_m":photo,"polygons_latlon":sh["geo"]["polygons_latlon"],
 "note":"Default. Shows the reef as it actually is; the 3 'channel containers' and 2 wing patches are small and faint. 24 further faint patches (~660 m2) lie seaward/between the arms (faint_seaward_patches)."})
op=o2["R"]["outer_-6.0"]["canonical_m"]; oc=[q["canonical_m"] for q in o2["R"]["crest_-2.5"]]
V.append({"id":"design_option2_2017","name":"Renewal design Option 2 (2017, the layout the 2017-18 works followed), -6 m AHD envelope","date":"2017","kind":"design_drawing",
 "source_ids":["s13"],"method":"Corbett et al. 2023 Fig 2 right, calibrated on its 50 m bar (0.5155 m/px), placed by the Jackson 2012 Fig 2/7 -> 2020 image chain (+-15 m, scale +-3 %); outer boundary of the nested contour group; crest loops = the black -2.5 m AHD contours (south loop closed by a 2-px hand patch).",
 "level":"-6 m AHD design contour envelope (outer limit of the design); crest -2.5 m AHD","area_m2":area([op]),"bbox_m":bbox([op]),"polygons_m":[op],"crest_loops_m":oc,"crest_loops_area_m2":[round(Polygon(q).buffer(0).area) for q in oc],
 "polygons_latlon":[[ll(p) for p in op]],
 "note":"A concept drawing: Corbett 2023 says the north reef was almost fully achieved, but the south reef and the bridge only partly. 97 % of the traced 2020 arms lie inside this envelope. No post-renewal as-built plan or survey exists."})
od=d04["outer_-6.0"]["canonical_m"]; odc=[q["canonical_m"] for q in d04["inner_-2.5"]]
V.append({"id":"design_2004_revised","name":"2004 revised design, -6 m AHD envelope (before the 2017-18 renewal)","date":"2004","kind":"design_drawing",
 "source_ids":["s11","s8"],"method":"Jackson et al. 2012 Fig 2 right (same CAD drawing as the contours on Fig 7), placed on the 2020 image by dark-patch NCC (corr 0.57) (+-15 m, scale +-10 %); outer boundary of the nested contours; crest loops = -2.5 m.",
 "level":"-6 m design contour envelope; crest -2.5 m AHD","area_m2":area([od]),"bbox_m":bbox([od]),"polygons_m":[od],"crest_loops_m":odc,"crest_loops_area_m2":[round(Polygon(q).buffer(0).area) for q in odc],
 "polygons_latlon":[[ll(p) for p in od]],"note":"Pre-renewal design; equals Corbett 2023 Option 1. 94.5 % of the traced arms lie inside."})
rzp=rz["canonical_m"]
V.append({"id":"survey_2011-06-09","name":"Surveyed relief zone, bathymetric survey of 9 Jun 2011 (before the 2017-18 renewal)","date":"2011-06-09","kind":"multibeam_survey",
 "source_ids":["s15","s11"],"method":"Jackson et al. 2012 Fig 5a (Gold Coast City Council survey): zone of dense multi-colour contours (colour-pixel density in a 13 px window > 0.14, closed r=5), registered to the design drawing by chamfer fit and placed by the same chain (+-15 m). The figure has NO depth legend, so this is a relief zone, not a depth contour.",
 "level":"where the seabed relief is strong (reef containers); threshold sensitivity: 3,000-7,000 m2 for density 0.18-0.10","area_m2":area(rzp),"bbox_m":bbox(rzp),"polygons_m":rzp,"polygons_latlon":[[ll(p) for p in q] for q in rzp],
 "note":"Older state (about 450 containers, no 2017-18 additions). Only the pre-renewal MEASURED data; coarse, drawn from a contour plot."})
nv=[nav["shoal_4.0m_N"]["canonical_m"],nav["shoal_4.0m_S"]["canonical_m"]]
V.append({"id":"navionics_4.0m_shoals","name":"Navionics chart shoals shallower than 4.0 m (indicative only, read 6 Oct 2026)","date":"2026-10-06","kind":"other",
 "source_ids":["s12"],"method":"Closed 4.0 m loops of the Garmin Navionics SonarChart screenshots (img-50..53) registered to the 2020 image; datum not stated (LAT assumed).",
 "level":"chart shoal; crowd-sourced, smoothed, datum unstated","area_m2":area(nv),"bbox_m":bbox(nv),"polygons_m":nv,"polygons_latlon":[[ll(p) for p in q] for q in nv],
 "note":"NOT a footprint (138 m2 north, 399 m2 south). The south 4.5 m contour is an open U-shape, not a closed loop. Use only as an independent position check (7-25 m agreement)."})
sh["outline_versions"]=V; sh["default_outline"]="photo_2020-08-08"
sh["versions_info"]=("Five outlines are stored. DEFAULT = the renewed reef as seen on the Esri aerial photo of 8 Aug 2020 (visible container field, 6,239 m2): no post-renewal survey or as-built drawing exists, "
 "so the photo is the only evidence of the state actually built. Renewal design Option 2 (Corbett et al. 2023 Fig 2, the layout the 2017-18 works followed, 13,941 m2 to the -6 m contour) is the design of the built version, "
 "but the south reef and bridge were only partly built. The 2004 revised design (13,631 m2) and the 2011 survey relief zone (4,922 m2, Jackson et al. 2012) describe the reef BEFORE the 84 containers of 2017-18. "
 "The Navionics 4.0 m shoals (537 m2) are indicative only. Design outlines are placed to +-15 m and are envelopes larger than the container field; the photo field is a lower bound (deeper toe invisible).")
sh["faint_seaward_patches"]={"note":"Faint dark patches not in the polygons (local-contrast detection on s3: G channel, blur 2 px, background gaussian sigma 30 px excluding traced polygons, diff > 4 DN, >= 10 m2, centroid y >= 241 m). Maybe buried containers or natural reef; not used in any outline. The first (cut-off) run found 20 patches / ~540 m2 with a slightly different recipe.",
 "count":len(fp),"area_m2":round(sum(p["area_m2"] for p in fp)),"patches":fp}
refs=sh["references"]; ids={r["id"] for r in refs}
if "R-C2023" not in ids: refs.append({"id":"R-C2023","citation":"Corbett, B., Mulcahy, M., Elliott-Perkins, A. and Hunt, A. (2023) Narrowneck Artificial Reef Renewal. Australasian Coasts & Ports 2023, pp. 663-669 (papers/ folder, supplied by Lior)","url":"papers/","accessed":"2026-10-07","supports":"Option 1/2 designs, Option 2 built, crest -2.5 m AHD = -1.5 m LAT, Fig 2 plan (50 m bar), Fig 3 pre-works multibeam"})
if "R-JC2019" not in ids: refs.append({"id":"R-JC2019","citation":"Jackson, L.A. and Corbett, B. (2019) Gold Coast surfing reefs: future (Coasts & Ports 2019), PDF p.4","url":"see src/gov/narrowneck-gold-coast_jackson_corbett2019_coasts_ports_SFGC_future.pdf","accessed":"2026-10-07","supports":"outer reef section in 10 m of water"})
srcs=sh["sources"]; sid={s["id"] for s in srcs}
if "s13" not in sid: srcs.append({"id":"s13","role":"design_version","file":"07_scale/shapes/narrowneck-gold-coast/src/gov/corbett2023_extracted/p3_x88.png","citation":"Corbett et al. 2023 Fig 2 (Option 1 left / Option 2 right), PDF p.3","licence":"conference copyright; private research copy; reuse to be checked","retrieved":"2026-10-07"})
if "s15" not in sid: srcs.append({"id":"s15","role":"survey_figure","file":"07_scale/shapes/narrowneck-gold-coast/src/gov/narrowneck-gold-coast_jackson2012_fig5a_reef_bathymetry_2011-06-09_native.jpeg","citation":"Jackson et al. 2012 Fig 5a (Gold Coast City Council bathymetric survey 9 Jun 2011), p.4","licence":"ICCE/Coastal Engineering Research Council; private research copy; reuse to be checked","retrieved":"2026-10-06"})
if "s14" not in sid: srcs.append({"id":"s14","role":"context","file":"07_scale/shapes/narrowneck-gold-coast/src/gov/narrowneck-gold-coast_jackson_corbett2019_coasts_ports_SFGC_future.pdf","citation":"Jackson & Corbett 2019, PDF p.4","licence":"conference copyright; private research copy","retrieved":"2026-10-07"})
json.dump(sh,open(ROOT+"/shape.json","w"),indent=1)
print("versions",[(v["id"],v["area_m2"],v["bbox_m"]) for v in V],"faint",len(fp))

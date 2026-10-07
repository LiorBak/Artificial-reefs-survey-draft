"""Builds shape.json (draft/refined) for narrowneck-gold-coast. Run again after each refinement."""
import json, os, math, subprocess, sys
ROOT=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git"
SH=ROOT+r"\07_scale\shapes\narrowneck-gold-coast"
polys=json.load(open('polys_v2.json')); extras=json.load(open('extras_v2.json'))
frame=json.load(open('frame.json'))
g=json.load(open(SH+r"\src\wayback\nn_wayback_2020-08-08_r9812_z19.png.geo.json"))
mpp=g['m_per_px_center']
reef_keys=['north_arm','south_arm','wing_patch_NW_a','wing_patch_NW_b','weir_1','weir_2_faint','weir_3_faint']
labels=[
 "north arm - envelope of the visible container field (closing radius 14 px = 3.7 m around the thresholded dark patches; includes the 20 m container lying along the seaward tip and the S-pointing leg at the shoreward end)",
 "south arm - envelope of the visible container field (same method; includes the SW container and the container below the arm)",
 "north-west shoreward patch A (isolated containers on the north wing side)",
 "north-west shoreward patch B (isolated containers on the south side of the north wing)",
 "weir container 1 (solid dark, in the channel, 16 m long, E-W)",
 "weir container 2 (FAINT, read by eye)",
 "weir container 3 (FAINT, read by eye)"]
shape_path=SH+r"\shape.json"
old=json.load(open(shape_path,encoding='utf-8')) if os.path.exists(shape_path) else {}
d=old
d.update({
 "slug":"narrowneck-gold-coast","name":"Narrowneck Reef (Gold Coast, Queensland)","status":"traced","updated":"2026-10-06"})
d.setdefault('sources',[])
src3={
 "id":"s3","kind":"satellite","title":"Esri World Imagery Wayback release 9812, z19, 2020-08-08 (post-renewal)",
 "url":"https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/9812/{z}/{y}/{x}",
 "source_page":"Esri Wayback (release 9812)","page_or_figure":"z19 tiles, 1517x1517 px crop, centre -27.98665/153.43455","image_date":"2020-08-08 (Esri identify SRC_DATE2)",
 "credit":"Esri, Maxar, Earthstar Geographics, and the GIS User Community","license":"Esri imagery terms; private research copy only",
 "local_file":"07_scale/shapes/narrowneck-gold-coast/src/wayback/nn_wayback_2020-08-08_r9812_z19.png","image_size":[1517,1517],
 "registry_id":"narrowneck-gold-coast-img-45",
 "georef":{"provider":"Esri World Imagery Wayback","zoom":19,"bounds":g['bounds'],"tile_template":g['tile_template'],"imagery_date":"2020-08-08","attribution":g['attribution']},
 "scale":{"px_per_m":1.0/mpp,"m_per_px":mpp,"method":"georeferenced","evidence":"Web-Mercator z19 tile grid at the site latitude -27.9867: 0.2637 m/px (sidecar m_per_px_center). Scale is not read from the image content; cross-checked against the 20 m container length (container patches 60-80 px long) and against Jackson et al. 2007 Fig 13 scale bar (see METHOD.md).","uncertainty_pct":2},
 "pixel_polygons":[polys[k] for k in reef_keys],
 "polygon_labels":labels,
 "traced_what":"visible container patches of the north and south arm (dark 20 m geotextile containers on pale water): thresholded green channel (<49 after sigma 1 px blur), morphological closing, Douglas-Peucker 3 px; weir containers and shoreward patches read by eye",
 "extras_not_in_polygons":{k:v for k,v in extras.items()},
 "match_notes":"Cross-checked on s4 (independent 2022-11 tile set: offset 0.17 m E, 0.10 m N by phase correlation) and s5 (2019-06-18, by eye).",
 "role":"primary"}
d['sources']=[s for s in d['sources'] if s.get('id')!='s3']+[src3]
json.dump(d,open(shape_path,'w',encoding='utf-8'),indent=2,ensure_ascii=False)
# canonical via geom.py (fixed 2026-10-05)
cmd=[sys.executable,ROOT+r"\07_scale\tools\geom.py",'make-canonical','--shape',shape_path,'--source-id','s3',
     '--origin-px','%.4f,%.4f'%tuple(frame['origin_px']),'--alongshore-dir-px','%.8f,%.8f'%tuple(frame['alongshore_dir_px']),
     '--alongshore-compass-deg','%.3f'%frame['bearing_north_heading_deg']]
r=subprocess.run(cmd,capture_output=True,text=True); print(r.stdout[-600:],r.stderr[-400:])

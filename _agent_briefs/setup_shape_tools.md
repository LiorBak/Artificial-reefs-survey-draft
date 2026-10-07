# Brief: build and test the shape-tracing toolkit -> 07_scale\tools\

Python with pillow + requests (pip install). Write 07_scale\tools\README.md documenting each command with a worked example.

1. satellite.py
   - fetch --lat LAT --lon LON --radius-m R --zoom Z --out PNG [--wayback RELEASE]
     Stitch Esri World Imagery tiles covering the radius:
       https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
     Wayback (older dated imagery, 2014+): release list
       https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json
     tiles https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/{release}/{z}/{y}/{x}
     Write PNG + PNG.geo.json: exact Web-Mercator bounds (north/south/east/west), zoom, metres-per-pixel at centre,
     tile template, attribution "Esri, Maxar, Earthstar Geographics, and the GIS User Community", retrieval date.
     Try to read the imagery capture date at the point (Esri World Imagery identify / metadata service); else "unknown".
   - wayback-list: print available releases (id + date).
   - pix2ll / ll2pix using a .geo.json.
2. overlay.py
   - render --image IMG --polys POLYS --out PNG [--grid N] [--labels] [--alpha 0.35]
     POLYS = JSON file or JSON string: list of polygons, each a list of [x,y]. Semi-transparent fill + outline + numbered vertices; optional labelled pixel grid every N px.
   - zoom --image IMG --box x0 y0 x1 y1 --scale K --grid N --out PNG : crop + enlarge with labelled grid ticks in ORIGINAL pixel coordinates, so an agent can read precise coordinates by eye.
   - compare --image IMG --polys A --polys2 B --out PNG : two outlines in two colours.
3. geom.py (importable + CLI)
   - shoelace area, bbox, centroid, max dimension
   - pixel -> metres with px_per_m + rotation + origin
   - latlon <-> local metres (equirectangular about an anchor)
   - edge bearings, and the angle of each edge/arm to a given shoreline bearing
   - fit_similarity(control_pairs) with residuals
   - make_canonical(shape.json, source_id, origin_px, alongshore_dir_px) -> fills the "canonical" block per 07_scale\SHAPE_SPEC.md
TEST: fetch a stitch near Narrowneck (lat -27.9965, lon 153.4305 is approximate; radius 300 m; zoom 18) into %TEMP%, render a test polygon on it, run geom on it; report metres-per-pixel and whether a capture date was found. Delete test files.

Final JSON: {"tools_ok": bool, "commands": ["..."], "m_per_px_z18_at_narrowneck": number, "capture_date_found": bool, "caveats": ["..."]}

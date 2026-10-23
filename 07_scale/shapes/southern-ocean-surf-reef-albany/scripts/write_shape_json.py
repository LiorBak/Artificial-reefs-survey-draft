"""Assembles ../shape.json from build_out.json, analysis_out.json, polys_px.json (python -I write_shape_json.py)."""
import json, math, sys, numpy as np
sys.path.insert(0, '../../../tools'); import satellite as S
O = json.load(open('build_out.json')); A = json.load(open('analysis_out.json')); P = json.load(open('polys_px.json'))
geo = json.load(open('../src/esri_current_2026-01-20_z18.png.geo.json')); mpp = O['mpp']; beta = O['shoreline']['bearing_deg']
u_al = np.array([math.sin(math.radians(beta)), math.cos(math.radians(beta))]); u_of = np.array([math.sin(math.radians(beta+90)), math.cos(math.radians(beta+90))])
foot = np.array(O['origin_enu_from_centre'])
def m_to_ll(pm):
    out = []
    for x, y in pm:
        e = foot + x*u_al + y*u_of; px, py = 511 + e[0]/mpp, 511 - e[1]/mpp
        r = S.pix2ll(geo, px, py); out.append([round(r[0], 7), round(r[1], 7)])
    return out
sat_ll = [[round(S.pix2ll(geo, x, y)[0], 7), round(S.pix2ll(geo, x, y)[1], 7)] for x, y in P['sat2026_trace']]
des_ll = m_to_ll(O['design']['polygon_m'])
org = m_to_ll([[0, 0]])[0]
sat, des = O['sat'], O['design']
shape = {
 "slug": "southern-ocean-surf-reef-albany", "name": "Southern Ocean Surf Reef (\"Midds Reef\"), Middleton Beach, Albany WA",
 "status": "traced", "updated": "2026-10-10",
 "confidence": {"level": "high",
   "reason": "The built reef shows as a dark wedge on a geo-referenced Esri image of 2026-01-20 that is absent from the 2025-01-16 image of the same spot, and the outline agrees with the scale-barred Bluecoast design plan (outline overlap 81 %, orientation within 3 deg) and with the City's 165 m length (design plan 165 m, satellite 157 m, -5 %).",
   "factors": ["structure clearly visible on geo-referenced satellite imagery (single date, 2026-01-20); before/after pair confirms the dark patch is the reef",
               "lengths along the crest agree with the text value 165 m within 5 % (satellite 157 m, design 165 m); width across crest 117 m (sat) / 121 m (design) vs 'up to 110 m' (+6 % / +10 %)",
               "edge is fuzzy: the deep (offshore) side fades into dark water, so the visible-patch outline is a lower bound for the toe; area of the objective mask 7,700 m2 vs traced 10,900 m2 vs design outer contour 13,100 m2 (area uncertainty about -30 % / +20 %)",
               "no measured as-built survey or LiDAR/multibeam of the reef located (needs network / City or Bluecoast); design plan has a scale bar but no coordinates, so its position comes from the satellite fit",
               "the 140 m 'distance offshore' cannot be reproduced exactly because its reference line is undefined (71 m from the dry-sand edge, about 150 m from the vegetation edge)"]},
 "design_version": {
   "drawn": "Default outline = Bluecoast Consulting Engineers 'Final Reef Design' (detailed design for the reef built Oct 2024 - Mar 2025; design volume 34,000 m3 on 2017 bathymetry; crest -1.0 m AHD). Alternative outline = visible reef on Esri imagery of 2026-01-20 (as built, in service).",
   "why_this_one": "The City of Albany completed-project page gives the same dimensions for the built reef as the Bluecoast final design (165 m long, up to 110 m wide, crest -1.0 m AHD, 62,800 t = about 34,000 m3), and the satellite wedge has the same shape and orientation, so the final design is the built version. Per Lior's rule, no measured survey is available, so the design drawing of the built version is the default over the photo trace.",
   "alternatives_seen": [
     {"what": "Earlier concept/interim positions (Wikipedia ~120 m offshore; City FAQ May 2023 ~145 m; the 2023 relocation to cut injuries)", "source_id": "card R15/R11", "why_not_used": "superseded by the final design table (140 m) and by the satellite image of the built reef"},
     {"what": "Post-opening change: 18 rocks repositioned in March 2026 (Albany Advertiser, per card R11)", "source_id": "card R11", "why_not_used": "after the 2026-01-20 image; a note only (3D shows as-built state), planform effect negligible"},
     {"what": "Gemini polygon (9 vertices, gross 13,500 m2, '160-190 deg' swell apex orientation)", "source_id": "07_scale/00_gemini_footprints_extract.json", "why_not_used": "no original drawing behind it; area 13,500 m2 is close to our design outline (13,104 m2) but its orientation text is invented; not used"}]},
 "sources": [
  {"id": "sat2026", "kind": "satellite", "title": "Esri World Imagery, Middleton Beach reef, captured 2026-01-20", "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
   "source_page": "Esri World Imagery (current layer)", "page_or_figure": "centre -35.018, 117.9207, radius 250 m, zoom 18", "image_date": "2026-01-20",
   "credit": "Esri, Maxar, Earthstar Geographics, and the GIS User Community", "license": "Esri/Maxar imagery terms - private research copy only; reuse rights to be checked before any public release",
   "local_file": "07_scale/shapes/southern-ocean-surf-reef-albany/src/esri_current_2026-01-20_z18.png", "image_size": [1022, 1022], "registry_id": "southern-ocean-surf-reef-albany-img-13",
   "georef": {"provider": "Esri World Imagery", "zoom": 18, "bounds": geo['bounds'], "tile_template": geo['tile_template'], "imagery_date": "2026-01-20", "attribution": geo['attribution']},
   "scale": {"px_per_m": round(1/mpp, 4), "method": "georeferenced", "evidence": "Web-Mercator z18 tile at lat -35.018: 0.4891 m/px (sidecar .geo.json m_per_px_center); image centre px (511,511) = (-35.018, 117.9207) checked with satellite.py pix2ll", "uncertainty_pct": 1},
   "pixel_polygons": [P['sat2026_trace']], "traced_what": "outer edge of the visible dark rock wedge (20 vertices), incl. the breaking-wave patch on the shoreward crest; objective mask outline kept as a check",
   "match_notes": "outline within about 3-8 px (1.5-4 m) of the visible dark edge on the shoreward/south edges; offshore (east) edge is soft, +-10-15 px. Objective mask (green<30) lies 99 % inside the traced polygon (IoU 0.69).", "role": "primary"},
  {"id": "design_plan", "kind": "design_drawing", "title": "Southern Ocean Surf Reef design by Bluecoast (plan with design contours over aerial; scale bar; north up)", "url": "https://raisedwaterresearch.com/wp-content/uploads/2019/12/Souther-Ocean-Surf-Reef-Design-by-Bluecoast.png",
   "source_page": "https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/albany-artificial-surf-reef/", "page_or_figure": "page gallery image 984 x 702 px (same plan as the right half of City of Albany design.jpg)", "image_date": "design stage, before 2025 construction (exact date not stated; based on 2017 bathymetry)",
   "credit": "Bluecoast Consulting Engineers via Raised Water Research", "license": "not stated - private research copy only",
   "local_file": "07_scale/shapes/southern-ocean-surf-reef-albany/src/rwr_bluecoast_design_diagram.png", "image_size": [984, 702], "registry_id": "southern-ocean-surf-reef-albany-img-11", "georef": None,
   "scale": {"px_per_m": 1.52, "method": "scale bar", "evidence": "bar ticks 0 / 0.05 / 0.1 km at px x = 493.5 / 569.5 / 645.5 (zoom 5x with 10 px grid)", "uncertainty_pct": 3},
   "pixel_polygons": [P['design_diagram_trace']], "traced_what": "outermost design contour of the reef footprint (25 vertices)",
   "match_notes": "outline follows the outermost contour within about 3 px (2 m); the 110 m and 140 m dimension arrows on the figure are NOT to the same scale as the bar (arrow lengths 69 m and 117 m by the bar) so they were not used for scaling. North-up is confirmed: the dashed crest line reads 278 deg, inside the stated 270-305 deg N, and a free rotation fit to the satellite outline gives -3 deg.", "role": "primary"},
  {"id": "design_table", "kind": "design_drawing", "title": "Final Reef Design table + plan (City of Albany, Bluecoast)", "url": "https://www.albany.wa.gov.au/Profiles/albany/Assets/ClientData/Surf_Reef/design.jpg",
   "source_page": "https://www.albany.wa.gov.au/council/projects/completed-projects/southern-ocean-surf-reef-sosr.aspx", "page_or_figure": "design table (1026 x 521 px)", "image_date": "design stage (volume on 2017 bathymetry)", "credit": "City of Albany / Bluecoast Consulting Engineers", "license": "no licence stated - private research copy",
   "local_file": "07_scale/shapes/southern-ocean-surf-reef-albany/src/design.jpg", "image_size": [1026, 521], "registry_id": "southern-ocean-surf-reef-albany-img-10", "georef": None, "scale": None, "pixel_polygons": [], "traced_what": "not traced; parameter table read (volume 34,000 m3, crest length 110 m @ -2 m AHD, crest -1.00 m AHD, orientation 270-305 N, 140 m from landward toe, 350 m north of Big4 Caravan Park)", "match_notes": "read values, see METHOD.md step 3", "role": "context"},
  {"id": "sat2025", "kind": "satellite", "title": "Esri World Imagery Wayback 13192, captured 2025-01-16 (before construction)", "url": "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/13192/{z}/{y}/{x}", "source_page": "Esri Wayback", "page_or_figure": "same tile footprint as sat2026", "image_date": "2025-01-16", "credit": "Esri, Maxar, Earthstar Geographics, and the GIS User Community", "license": "Esri/Maxar terms - private research copy",
   "local_file": "07_scale/shapes/southern-ocean-surf-reef-albany/src/esri_wayback13192_2025-01-16_z18.png", "image_size": [1022, 1022], "registry_id": "southern-ocean-surf-reef-albany-img-12", "georef": {"provider": "Esri Wayback", "zoom": 18, "bounds": geo['bounds'], "imagery_date": "2025-01-16"}, "scale": {"px_per_m": round(1/mpp, 4), "method": "georeferenced", "evidence": "same bounds as sat2026", "uncertainty_pct": 1}, "pixel_polygons": [], "traced_what": "nothing (no structure)", "match_notes": "inside the traced polygon mean green 137 vs 129 offshore (no dark patch) in 2025; 57 vs 68 in 2026: confirms the dark wedge is the new reef", "role": "context"},
  {"id": "constr_aerials", "kind": "aerial_photo", "title": "Construction-stage oblique/drone photos (RWR 2025-05; ABC 2025)", "url": "see registry img-03 and img-05", "source_page": "see registry", "page_or_figure": "-", "image_date": "2025 (construction)", "credit": "Raised Water Research; 'Supplied' via ABC News", "license": "not cleared - research copy",
   "local_file": "03_images/reefs/southern-ocean-surf-reef-albany/", "image_size": None, "registry_id": "southern-ocean-surf-reef-albany-img-03, -05", "georef": None, "scale": None, "pixel_polygons": [], "traced_what": "not traced: oblique / no scale, partly built", "match_notes": "qualitative: elongated dark berm tapering seaward, consistent with the wedge; img-05 shows the shoreward arm still under construction", "role": "context"}],
 "canonical": {
   "frame": "metres; origin = foot of the perpendicular from the traced reef centroid onto the beach-face line (edge of bright dry sand in the 2026-01-20 image, fitted bearing %.1f deg true); +x alongshore toward NNE (bearing %.1f deg); +y offshore toward ESE (bearing %.1f deg), i.e. +y is +x turned 90 deg clockwise, as in geom.py and the other shapes (x right, y down = true unmirrored plan view looking at the sea)" % (beta, beta, beta+90),
   "derived_from": "sat2026", "polygons_m": [sat['polygon_m']], "area_m2": sat['area_m2'],
   "bbox_m": {"alongshore": sat['alongshore'], "crossshore": sat['crossshore'], "x_range": sat['x_range'], "y_range": sat['y_range']},
   "max_dim_m": sat['max_dim_m'], "distance_offshore_m": sat['centroid'][1], "distance_offshore_nearest_m": sat['nearest_edge_from_shoreline_m'],
   "distance_offshore_note": "centroid y = %.0f m, nearest edge (shoreward apex) %.0f m, both from the dry-sand beach-face line; the true swash line is about 10-15 m further seaward and the vegetation edge about 80 m further landward, so the City's '140 m from landward toe' (reference line not stated) sits between the two (about 150 m from the vegetation edge)." % (sat['centroid'][1], sat['nearest_edge_from_shoreline_m']),
   "shore_normal_bearing_deg": round(beta+90, 2),
   "extent_along_crest_m": A['sat']['extent_along_crest_m'], "extent_across_crest_m": A['sat']['extent_across_crest_m'],
   "frame_note": "shoreline bearing is local (rows 440-720 of the tile, Theil-Sen, 95 % CI 27.7-33.0 deg); the beach curves (bearing 17 deg in the northern rows 40-320, 27 deg whole-beach)"},
 "geo": {"polygons_latlon": [sat_ll], "shoreline_bearing_deg": beta, "method": "pixel -> lat/lon with the tile's Web-Mercator bounds (satellite.py pix2ll)", "source_id": "sat2026", "origin_latlon": org},
 "angles": [
   {"what": "crest (shoreward/north) edge of the traced wedge, from the east tip to the shoreward apex: bearing", "deg": A['sat_crest_edge_bearing_east_to_apex_deg'], "method": "straight line between traced vertices (px 712,482) and (397,418), true bearing from georeference (north up)"},
   {"what": "design dashed crest line, east to west: bearing (design text: curved 270-305 deg N)", "deg": A['design_dashed_line_bearing_east_to_west_deg'], "method": "px (765,335) to (520,300) on the design plan, north up"},
   {"what": "crest edge vs shoreline (acute angle between lines)", "deg": round(abs(((A['sat_crest_edge_bearing_east_to_apex_deg'] - beta) + 90) % 180 - 90), 1), "method": "|bearing - shoreline bearing %.1f| folded to 0-90; the crest runs about %.0f deg off the shore normal" % (beta, abs(((A['sat_crest_edge_bearing_east_to_apex_deg'] - (beta+90)) + 90) % 180 - 90))}],
 "dimensions_check": [
   {"quantity": "length along the crest", "text_value": "165 m", "text_ref": "card R3 (City of Albany Design Aspects)", "drawing_value": "157.2 m (satellite) / 164.6 m (design plan)", "diff_pct": "-4.7 / -0.2", "comment": "extent of the outline projected on the crest bearing (281.5 / 278.1 deg)"},
   {"quantity": "width up to", "text_value": "110 m", "text_ref": "card R3", "drawing_value": "116.7 m (satellite) / 121.2 m (design) across the crest", "diff_pct": "+6 / +10", "comment": "'up to 110 m' not defined (crest-normal vs shore-normal); measured across the crest bearing"},
   {"quantity": "crest orientation", "text_value": "curved 270-305 deg N", "text_ref": "design table", "drawing_value": "281.5 (satellite crest edge) / 278.1 (design dashed line)", "diff_pct": None, "comment": "inside the stated range"},
   {"quantity": "distance offshore (landward toe)", "text_value": "140 m", "text_ref": "design table / City page", "drawing_value": "71 m from the dry-sand edge; about 150 m from the vegetation edge", "diff_pct": "n/a", "comment": "reference line of the 140 m is not defined; plausible if it is the dune/vegetation toe (+7 %)"},
   {"quantity": "footprint area", "text_value": "not stated (Gemini 13,500 m2)", "text_ref": "Gemini extract", "drawing_value": "10,918 m2 satellite trace / 13,104 m2 design outer contour / 7,707 m2 objective mask", "diff_pct": "design vs Gemini -2.9", "comment": "area depends on the edge definition; see outline versions"},
   {"quantity": "volume vs area", "text_value": "34,000 m3 = 62,800 t / 1.85 t/m3", "text_ref": "design table + card R3", "drawing_value": "mean height over the design outline = 34,000 / 13,104 = 2.6 m", "diff_pct": None, "comment": "bulk density 1.85 t/m3 is an assumption (granite placed at ~35 % voids); only a consistency note"}],
 "gemini": {"values": {"length_m": 165, "width_m": 110, "area_m2": 13500, "crest_depth_m": 1.0, "distance_offshore_m": 140, "orientation": "Apex faces SSE-S swell (160-190 deg)"},
   "sources_used": [
     {"url": "Bluecoast Consulting Engineers: Albany Artificial Surf Reef Design Report (2020) [no URL given]", "what_gemini_said": "dimensions and tonnage as the City page", "our_check": "unverifiable", "evidence": "no URL; not found in our local material; network blocked this run. Numbers equal the City page (card R3), which we use directly."},
     {"url": "City of Albany: Middleton Beach Surf Reef Post-Construction Monitoring (2022) [no URL given]", "what_gemini_said": "(unspecified)", "our_check": "unverifiable", "evidence": "a 2022 'post-construction monitoring' of a reef built in 2024-25 is anachronistic: probably wrong/invented"},
     {"url": "Raised Water Research: Albany Southern Ocean Surf Reef Review (2023) [no URL given]", "what_gemini_said": "(unspecified)", "our_check": "unverifiable", "evidence": "RWR page we hold is 'Midds Reef' (2025); no 2023 review located"}],
   "summary": "Gemini's length/width/crest/offshore/tonnage match the City page and our card; its area 13,500 m2 agrees with our design-outline area (13,104 m2) within 3 %. Its orientation text ('apex faces SSE-S swell, 160-190 deg') has no source and does not match the design table (crest 270-305 deg N). Nothing from Gemini was used."},
 "no_source": None,
 "references": [
  {"id": "R3", "citation": "City of Albany. Southern Ocean Surf Reef (SOSR) project pages (current and completed projects), Design Aspects.", "url": "https://www.albany.wa.gov.au/council/projects/completed-projects/southern-ocean-surf-reef-sosr.aspx", "accessed": "2026-09-24 (card); design.jpg re-fetched 2026-10-06 (registry)", "supports": "165 m long, up to 110 m wide, crest -1.0 m AHD, design table (34,000 m3, 270-305 N, 140 m)"},
  {"id": "RWR", "citation": "Raised Water Research (2025). Midds Reef [spot page]; Bluecoast plan diagram uploaded 2019-12.", "url": "https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/albany-artificial-surf-reef/", "accessed": "2026-10-04 (registry)", "supports": "plan diagram with scale bar"},
  {"id": "Esri", "citation": "Esri, Maxar, Earthstar Geographics, and the GIS User Community. World Imagery (current, 2026-01-20; Wayback 13192, 2025-01-16).", "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer", "accessed": "2026-10-04 (tiles saved)", "supports": "georeferenced planform of the built reef"}],
 "outline_versions": [
  {"id": "design_bluecoast", "name": "Bluecoast final design, outermost contour (design stage, volume on 2017 bathymetry)", "date": "design stage, before the Oct 2024 - Mar 2025 build (exact date not stated)", "kind": "design_drawing", "source_ids": ["design_plan", "design_table"],
   "method": "outermost contour traced on the scale-barred plan (1.52 px/m, north up) and positioned by maximising overlap with the satellite trace (translation only; IoU 0.81)", "level": "outer edge of the designed rock footprint (toe), seabed depth at the toe not stated",
   "area_m2": des['area_m2'], "bbox_m": [des['alongshore'], des['crossshore']], "polygons_m": [des['polygon_m']], "polygons_latlon": [des_ll],
   "note": "Position comes from the satellite fit, not from coordinates on the drawing; shape and size come from the drawing. Along-crest length 164.6 m matches the City's 165 m."},
  {"id": "sat_2026", "name": "Visible reef on Esri satellite image (as built, 20 Jan 2026)", "date": "2026-01-20", "kind": "photo_trace", "source_ids": ["sat2026"],
   "method": "20-vertex outline drawn on the dark rock wedge of the geo-referenced image (0.489 m/px); objective mask kept as a check", "level": "edge of rock visible from above in clear water (offshore edge soft)",
   "area_m2": sat['area_m2'], "bbox_m": [sat['alongshore'], sat['crossshore']], "polygons_m": [sat['polygon_m']], "polygons_latlon": [sat_ll],
   "note": "7,707 m2 core (objective mask) lies inside it; later changes (18 rocks moved March 2026) not shown"}],
 "default_outline": "design_bluecoast",
 "versions_info": "Two outlines of the one reef. Default: the Bluecoast final-design outline (13,100 m2), because per the project rule a design drawing of the built version outranks a photo trace and no measured as-built survey is available; its size and shape come from the scale-barred plan, its position from the satellite fit. Toggle: the reef as visible on an Esri satellite image of 20 Jan 2026 (10,900 m2), the as-built check; it lies inside the design outline, and the dark patch fades offshore where the water deepens. Both agree on length (about 160 m) and crest orientation (about 280 deg true).",
 "outline_versions_chosen": "default design_bluecoast; toggle sat_2026"}
json.dump(shape, open('../shape.json', 'w'), indent=1, ensure_ascii=False); print('written', len(json.dumps(shape)))

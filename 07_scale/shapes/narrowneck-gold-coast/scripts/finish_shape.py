import json, math
ROOT = "C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/narrowneck-gold-coast"
d = json.load(open(ROOT + "/shape.json", encoding='utf-8'))
M = json.load(open('metrics_out.json'))
reg = json.load(open(ROOT + "/design_registration_out.json"))
fr = json.load(open('frame.json'))
cin = json.load(open('council_in_frame.json'))
d['updated'] = "2026-10-06"
d['status'] = "traced"
d['confidence'] = {"level": "medium",
 "reason": "The visible container field of both arms is traced on sharp, georeferenced 2020 imagery (edges good to about 1 m, confirmed on a second tile set and on the Navionics shoal contours), but the deeper seaward toe is not resolved, three channel containers are faint, and the built renewal option is unverified.",
 "factors": [
  "+ both arms resolve into individual 20 m containers on the 2020-08-08 Esri Wayback image (s3); s4 (2022 tile set) agrees to 0.2 m",
  "+ position confirmed independently: the arms fall on the 4.0 / 4.5 m shoal contours of the Garmin Navionics SonarChart (within ~20 m)",
  "+ arm length 134 m (N) vs the design drawing's 121 m to the -6 m contour (Jackson 2007 Fig 13 bar): within 10 %",
  "- the visible field ends at about the -6 m contour; the deeper toe to -8 m is not visible, so the footprint is a lower bound",
  "- channel containers (3, two faint) have an unresolved identity (the 2004 weir containers are N-S oriented and not visible in 2020)",
  "- published envelope sizes (350 x 600, 450 x 250, 256 x 151 m) describe the design footprint or an asset envelope, not the container field",
  "- which of Corbett et al. 2023's two renewal shapes was built is unverified; the drawn state is what is visible after June 2018"]}
d['design_version'] = {
 "drawn": "The RENEWED reef as left after the June 2018 renewal (84 containers added around the existing 2004 revised-design structure; the City says 'minor changes to the shape'), as visible on Esri Wayback 2020-08-08",
 "why_this_one": "Lior's rule (2026-10-06): model the latest as-built state. Post-renewal imagery shows the containers clearly (s3), so the outline is the visible container field, not a design drawing; the 2004 revised design (Jackson 2012 Fig 2/7) is only a prior.",
 "alternatives_seen": [
  {"what": "1998-2000 original design: two separate tapered arms ('split V'), no weir, no flares, arms much longer to -10 m", "source_id": "registry img-26 (Jackson 2007 Fig 2)", "why_not_used": "history; the built shape was truncated and modified from 2002/2004 on"},
  {"what": "2004 revised design: submerged weir (2 containers) in the central channel + flared wings; ~450 containers by 2006", "source_id": "s8, s9, s11 (Jackson 2012 Figs 2, 4, 6, 7)", "why_not_used": "design prior; superseded by the 2018 renewal; used only as a cross-check (design outer contour vs visible field within +-15 m)"},
  {"what": "2017 renewal Option 1 'previous design shape' (crest -2.5 m AHD) vs Option 2 'amended shape' further seaward (~20 m, unverified)", "source_id": "Corbett et al. 2023 abstract via search summaries; City of Gold Coast 2020 page", "why_not_used": "paper not obtainable; the City states the built reef is the amended shape; we trace what is visible, which is within the +-15 m tolerance of both"},
  {"what": "Gemini: two stacked cross-shore lobes (inshore/offshore), 400 x 220 m", "source_id": "07_scale/00_gemini_footprints_extract.json", "why_not_used": "wrong topology and dimensions (METHOD Step 4)"}]}


def esri(id_, title, rel, date, role, reg_id, note, file):
    g = json.load(open(ROOT + "/src/wayback/" + file + ".geo.json"))
    return {"id": id_, "kind": "satellite", "title": title,
            "url": "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/%s/{z}/{y}/{x}" % rel,
            "source_page": "Esri Wayback (release %s)" % rel, "page_or_figure": "z19", "image_date": date,
            "credit": "Esri, Maxar, Earthstar Geographics, and the GIS User Community", "license": "Esri imagery terms; private research copy only",
            "local_file": "07_scale/shapes/narrowneck-gold-coast/src/wayback/" + file, "image_size": [g['width'], g['height']],
            "georef": {"provider": "Esri World Imagery Wayback", "zoom": 19, "bounds": g['bounds'], "tile_template": g['tile_template'], "imagery_date": date, "attribution": g['attribution']},
            "scale": {"px_per_m": 1 / g['m_per_px_center'], "method": "georeferenced", "evidence": "same tile grid and crop as s3", "uncertainty_pct": 2},
            "pixel_polygons": None, "traced_what": None, "match_notes": note, "role": role, "registry_id": reg_id}


S = [s for s in d['sources'] if s['id'] == 's3']
S.append(esri("s4", "Esri Wayback release 47963 (identify 2022-11-06; byte-identical tiles in releases 12428, 20512)", "47963", "2022-11-06 or later", "cross_check", "narrowneck-gold-coast-img-46", "s3 trace laid on it unchanged follows both arms; phase-correlation shift vs s3 0.17 m E, 0.10 m N; NW patch B and channel container 1 not visible", "nn_wayback_2022-11-06_r47963_z19.png"))
S.append(esri("s5", "Esri Wayback release 21485 (2019-06-18), first imagery after the June 2018 renewal", "21485", "2019-06-18", "cross_check", "narrowneck-gold-coast-img-47", "blurrier than s3; arms in the same place by eye (+-3-4 m)", "nn_wayback_2019-06-18_r21485_z19.png"))
S.append(esri("s6", "Esri Wayback release 23264 (2016-07-01), PRE-renewal", "23264", "2016-07-01", "context", "narrowneck-gold-coast-img-48", "murky; north-arm field already reaches the same seaward limit as in 2020", "nn_wayback_2016-07-01_r23264_z19.png"))
S.append({"id": "s7", "kind": "satellite", "title": "Esri Wayback release 9812, z17, 3 km square (shoreline context)", "url": "https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/9812/{z}/{y}/{x}", "image_date": "2020-08-08", "local_file": "07_scale/shapes/narrowneck-gold-coast/src/wayback/nn_wayback_2020-08-08_r9812_z17_shoreline_context.png", "image_size": [2845, 2844], "role": "context", "traced_what": "waterline (285 rows) -> shoreline bearing 356.2 deg", "scale": {"method": "georeferenced", "px_per_m": 1 / 1.0546601493346535}, "registry_id": "narrowneck-gold-coast-img-49"})
S.append({"id": "s1", "kind": "other", "title": "City of Gold Coast Open Data 'Artificial Reef' layer, OBJECTID 4637 (Narrowneck)", "url": "https://services.arcgis.com/3vStCH7NDoBOZ5zn/arcgis/rest/services/Artificial_Reef/FeatureServer/0", "source_page": "https://data-goldcoast.opendata.arcgis.com/datasets/c9d0b521374740cc9e9561b04c453736_0", "image_date": "undated", "credit": "City of Gold Coast", "license": "CC-BY-3.0 (to re-check)", "local_file": "07_scale/shapes/narrowneck-gold-coast/src/gc_opendata_artificial_reef_raw_4326.geojson", "role": "cross_check",
          "match_notes": "loose envelope: %.0f x %.0f m (alongshore x cross-shore) in our frame, %d m2; contains 100%% of the traced reef; attributes HEIGHT 3 m, LENGTH 256, WIDTH 151, TOP_REDUCED_LEVEL -2.5; VOLUME 7,668 unreliable" % (cin['bounds'][2] - cin['bounds'][0], cin['bounds'][3] - cin['bounds'][1], cin['area'])})
S.append({"id": "s2", "kind": "satellite", "title": "Esri World Imagery current z19 crop (2025-10-10)", "local_file": "07_scale/shapes/narrowneck-gold-coast/src/nn_esri_z19_current.png", "image_date": "2025-10-10", "role": "context", "match_notes": "reef almost invisible (dark water): not traced", "registry_id": "narrowneck-gold-coast-img-44"})
for sid, t, pf, lf, rid, note in (
        ("s8", "Jackson et al. 2012 Fig 7: July 2011 aerial + 2004 design contours + maintenance containers", "p.5 Fig 7", "src/gov/narrowneck-gold-coast_jackson2012_fig7_overlay_2011-07_aerial_with_design_contours_and_containers_native.jpeg", "narrowneck-gold-coast-img-10", "DESIGN PRIOR: placed on s3 (design_registration.py): Fig 7 = 0.21 m/px +-10 %, ends +-15 m"),
        ("s9", "Jackson et al. 2012 Fig 6b: July 2011 aerial", "p.5 Fig 6", "src/gov/narrowneck-gold-coast_jackson2012_fig6b_aerial_2011-07_native.jpeg", "narrowneck-gold-coast-img-09", "same photo as s8, 1.75x coarser; 0.3675 m/px"),
        ("s10", "Jackson et al. 2007 Fig 13: surf tracks on the revised design contours, 100 m bar", "Fig 13", "src/gov/narrowneck-gold-coast_jackson2007_fig13_recorded_surf_tracks_on_revised_design_contours_scale_100m_300dpi_crop.png", "narrowneck-gold-coast-img-27", "scale 4.275 px/m (bar black segments 154-241 and 325-407 px = 20 m each)"),
        ("s11", "Jackson et al. 2012 Fig 2 right: revised (2004) design levels", "p.3 Fig 2", "src/gov/narrowneck-gold-coast_jackson2012_fig2_reef_levels_original_and_revised_design_300dpi_crop.png", "narrowneck-gold-coast-img-04", "labelled contour levels -2.50 ... -8.00")):
    S.append({"id": sid, "kind": "paper_figure", "title": t, "page_or_figure": pf, "local_file": "07_scale/shapes/narrowneck-gold-coast/" + lf, "role": "cross_check" if sid in ("s8", "s9", "s10") else "context", "match_notes": note, "registry_id": rid})
S.append({"id": "s12", "kind": "other", "title": "Garmin Navionics SonarChart / Nautical Chart screenshots (z17, z18, shading 0-8 m)", "url": "https://maps.garmin.com/en-US/marine", "image_date": "chart state 2026-10-06", "local_file": "07_scale/shapes/narrowneck-gold-coast/src/navionics/", "role": "cross_check", "match_notes": "s3 arms fall on the 4.0/4.5 m shoal loops; datum not stated (LAT assumed)", "registry_id": "narrowneck-gold-coast-img-50..53"})
d['sources'] = S
s3 = [s for s in S if s['id'] == 's3'][0]
d['geo'] = {"polygons_latlon": M['latlon_polygons'], "polygon_labels": s3['polygon_labels'], "shoreline_bearing_deg": round(fr['bearing_north_heading_deg'], 1),
            "method": "pixel -> lat/lon with the Web-Mercator bounds of s3 (satellite.py pix2ll); shoreline bearing from a least-squares waterline fit to s7 (285 rows)", "source_id": "s3",
            "centroid_latlon": [-27.986629, 153.434052]}
nm = M['per_polygon']
d['angles'] = [
    {"what": "shoreline bearing (north-heading), 2020-08-08 waterline fit", "deg": round(fr['bearing_north_heading_deg'], 1), "method": "s7 waterline, rows +-1.5 km (a=0.0662); the +-800 m window gives 356.5"},
    {"what": "shore-normal (seaward) bearing", "deg": round((fr['bearing_north_heading_deg'] + 90) % 360, 1), "method": "shoreline + 90"},
    {"what": "north arm long axis, bearing", "deg": nm['north_arm']['axis_bearing_deg'], "method": "area-weighted PCA of the polygon; minimum rotated rectangle long side gives 94.0"},
    {"what": "north arm axis vs shoreline (acute)", "deg": nm['north_arm']['axis_to_shoreline_deg'], "method": "geom.angle_to_shoreline; minimum-rectangle value 82.2"},
    {"what": "south arm long axis, bearing", "deg": nm['south_arm']['axis_bearing_deg'], "method": "PCA; minimum rectangle 84.5"},
    {"what": "south arm axis vs shoreline (acute)", "deg": nm['south_arm']['axis_to_shoreline_deg'], "method": "geom.angle_to_shoreline; minimum-rectangle value 88.3"},
    {"what": "angle between the two arm axes (arms converge seaward)", "deg": round(abs(nm['north_arm']['axis_bearing_deg'] - nm['south_arm']['axis_bearing_deg']), 1), "method": "difference of PCA bearings; uncertainty +-5 deg (ragged outlines)"}]
d['canonical'].update({"frame": "metres; origin = waterline point (2020-08-08) nearest the area-weighted reef centroid, s3 px (-517.9, 821.7); +x alongshore toward bearing 356.2 deg (north); +y offshore (bearing 86.2 deg)",
                       "polygon_labels": s3['polygon_labels'], "area_arms_m2": M['area_arms_m2'], "bbox_arms_m": M['bbox_arms_m'], "arm_gap_min_m": M['arm_gap_min_m'], "per_polygon": nm,
                       "note": "polygons_m[0]=north arm, [1]=south arm (the two main bodies), [2],[3]=shoreward patches NW of the north arm, [4..6]=channel containers (5,6 faint). Untraced seaward dark patches are in sources s3 extras_not_in_polygons."})
d['canonical']['shore_normal_bearing_deg'] = round((fr['bearing_north_heading_deg'] + 90) % 360, 1)
d['dimensions_check'] = [
    {"quantity": "overall footprint (alongshore x cross-shore)", "text_value": "350 x 600 m (Wikipedia, axes unassigned); 450 x 250 m (boatgoldcoast); envelope 200-350 x 400-500 m (Jackson & Hornsey 2002 via Vieira 2021 AM p.5)", "text_ref": "card R9 / R8; footprint S1", "drawing_value": "113.3 x 157.4 m (all polygons); arms only 113.3 x 138.8 m", "diff_pct": None, "comment": "the published figures describe the design footprint to about -10 m or an asset envelope; the visible container field is far smaller. Not comparable."},
    {"quantity": "council asset polygon", "text_value": "256 x 151 m, 34,409 m2 (OBJECTID 4637)", "text_ref": "s1", "drawing_value": "%.0f x %.0f m, %.0f m2 in our frame; traced reef inside it 100%%" % (cin['bounds'][2] - cin['bounds'][0], cin['bounds'][3] - cin['bounds'][1], cin['area']), "diff_pct": None, "comment": "loose envelope; its centroid is 10 m south and 30 m seaward of the arms' centroid; the traced area is 18 % of it"},
    {"quantity": "earlier text-derived schematic", "text_value": "600 x 350 m, 114,950 m2, offshore 200 m, chevron", "text_ref": "07_scale/reefs/narrowneck-gold-coast.footprint.json", "drawing_value": "113 x 157 m, 6,239 m2, nearest edge 212 m, centroid 288 m offshore", "diff_pct": -95, "comment": "schematic was built on the envelope numbers; superseded"},
    {"quantity": "arm length (cross-shore) to the design -6 m contour", "text_value": "about 121 m (north arm, Jackson 2007 Fig 13: 4.275 px/m)", "text_ref": "s10", "drawing_value": "134 m (N arm, minimum rectangle) / 136 m (PCA); S arm 111-112 m", "diff_pct": 10.7, "comment": "agrees within about 10 %"},
    {"quantity": "container length", "text_value": "20 m, diameter 3-4.5 m", "text_ref": "Jackson 2007 p.4", "drawing_value": "tip containers 16-22 m long x 3-6 m wide in s3", "diff_pct": None, "comment": "consistent"},
    {"quantity": "channel width between arms", "text_value": "design: channel wall length about 33 m at Fig 13 scale", "text_ref": "s10", "drawing_value": "20.7 m minimum gap between the arm polygons", "diff_pct": -37, "comment": "design channel walls vs actual container edges; the renewal added containers around the channel sides"},
    {"quantity": "distance offshore", "text_value": "~200 m (card); take-off about 300 m offshore (Jackson 2007)", "text_ref": "card R9; Jackson 2007", "drawing_value": "212 m nearest (shoreward wing patches), 240 m arm bodies, centroid 288 m, tips 342-369 m from the 2020-08-08 waterline", "diff_pct": None, "comment": "consistent; depends on tide/beach state"},
    {"quantity": "container count", "text_value": "~450 by 2006; +84 in 2018", "text_ref": "Jackson 2012 p.3; City 2020", "drawing_value": "visible footprint ~70-80 containers", "diff_pct": None, "comment": "most containers are stacked (2 layers at the crest, Jackson 2012 Fig 9) or deeper than the visible limit"}]
d['design_prior'] = {"source_ids": ["s8", "s9", "s10"], "fig7_px_to_s3_px_affine": reg['fig7_px_to_s3_px_affine'], "mpp_fig7": 0.21, "mpp_fig7_uncertainty_pct": 10, "ratio_fig7_over_fig6b": reg['ratio_fig7_over_fig6b'], "ncc_corr": round(reg['ncc_corr'], 3),
                     "placement_uncertainty_m": "+-15 at the arm ends (scale +-10 %, translation +-12 m)",
                     "comparison_canonical_m": {"north_arm": {"design_outer_contour_y": [217.2, 354.1], "traced_y": [239.7, 369.1]}, "south_arm": {"design_outer_contour_y": [207.8, 345.8], "traced_y": [230.3, 341.7]}},
                     "reading": "traced field ends 15 m seaward of the 2004 outer contour at the north tip, 4 m inside it at the south tip; starts about 22 m seaward of the design shoreward wall; both inside the registration tolerance, so the unverified '20 m seaward' shift is neither confirmed nor excluded. The design -2.5 m crest loops cover only the shoreward ~60 m of each arm."}
d['gemini'] = {"values": {"shape": "two stacked cross-shore lobes (inshore/offshore)", "length_m": 400, "width_m": 220, "area_m2": "75,000 gross / 42,650 net", "crest_depth_m": 2.2, "distance_offshore_m": 180},
               "sources_used": [
                   {"url": "Black & Mead (2001) J. Coastal Res. SI 29, 115-130 (search snippet only)", "what_gemini_said": "design of the Gold Coast Reef (title without SI)", "our_check": "unverifiable", "evidence": "paywalled; bibliographic data confirmed by web search; no figure/dimension seen"},
                   {"url": "https://icce-ojs-tamu.tdl.org/icce/article/view/6956", "what_gemini_said": "Jackson et al. 2012 long-term performance (two lobes, 400 x 220 m)", "our_check": "wrong_design_version", "evidence": "Figs 2, 4, 6, 7 show two alongshore-adjacent arms with channel, weir and flared wings; no 400 x 220 m figure in the paper"},
                   {"url": "https://www.coastalmanagement.com.au (ICM case study / webinar, Salyer 2025)", "what_gemini_said": "ICM case study", "our_check": "dimension_not_in_source", "evidence": "images only, no planform or levels (REPORT.md 6.5)"},
                   {"url": "Swellnet, Nettle 2017-11-07 'Narrowneck artificial reef nears completion'", "what_gemini_said": "crest/depth", "our_check": "correct", "evidence": "'depths at low tide ... 2.5 m to 2.6 m' (REPORT.md 6.5); Gemini's crest 2.2 m matches Vieira 2021 AM p.5 instead"}],
               "summary": "Gemini's topology (inshore + offshore lobes) and dimensions (400 x 220 m, 75,000 m2) are not supported by any source; the reef is two alongshore-adjacent arms with a channel, 113 x 157 m of visible container field."}
d['no_source'] = None
d['references'] = [
    {"id": "R-J2012", "citation": "Jackson, A., Tomlinson, R., Corbett, B. and Strauss, D. (2012) Long term performance of a submerged coastal control structure: Narrowneck. Coastal Engineering Proceedings 33, structures.54", "url": "https://icce-ojs-tamu.tdl.org/icce/article/view/6956", "accessed": "2026-10-05", "supports": "topology, Figs 2/4/6/7, container counts, settlement"},
    {"id": "R-J2007", "citation": "Jackson, L.A., Corbett, B., McGrath, J., Tomlinson, R. and Stuart, G. (2007) Narrowneck Reef: review of seven years of monitoring. Shore & Beach 75(4)", "url": "http://hdl.handle.net/10072/17995", "accessed": "2026-10-06", "supports": "Fig 13 scale bar; container size; crest levels"},
    {"id": "R-V2021", "citation": "Vieira da Silva, G., Hamilton, D., Strauss, D., Murray, T., Tomlinson, R. (2021) Sediment pathways and morphodynamic response to a multi-purpose artificial reef. Coastal Engineering 171, 104027 (accepted manuscript)", "url": "http://hdl.handle.net/10072/409362", "accessed": "2026-10-06", "supports": "crest -2.2 m AHD (p.5); seabed Fig 3"},
    {"id": "R-COGC", "citation": "City of Gold Coast (2020) Narrowneck Reef Renewal (archived 2020-08-04)", "url": "http://web.archive.org/web/20200804025419/https://www.goldcoast.qld.gov.au/narrowneck-reef-renewal-39934.html", "accessed": "2026-10-06", "supports": "amended shape, 84 containers"},
    {"id": "R-MSQ", "citation": "Maritime Safety Queensland (2014, 2026) Standard port datum levels; Semidiurnal tidal planes 2026", "url": "https://www.msq.qld.gov.au", "accessed": "2026-10-06", "supports": "AHD = LAT + 0.760; MSL 0.88; HAT 2.03 (Gold Coast Seaway)"},
    {"id": "R-REPORT", "citation": "07_scale/bathymetry/gold_coast/REPORT.md sections 3, 6", "url": "", "accessed": "2026-10-06", "supports": "summary of the above and their pages"}]
d['verified_on'] = None
d['verification'] = []
json.dump(d, open(ROOT + "/shape.json", 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('keys', list(d.keys()))
print(len(json.dumps(d)))

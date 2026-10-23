"""Assemble shape.json from scripts/computed.json + scripts/a2_trace.json. Run from the shape folder after trace_a2.py / compute_shape.py."""
import json
import shapely.geometry as g
C = json.load(open('scripts/computed.json')); T = json.load(open('scripts/a2_trace.json')); E = T['scale_evidence']
R = '03_images/reefs/cables-reef-wa/'
def ver(id, name, date, kind, src, method, level, key, note):
    P = g.Polygon(C[key]); b = P.bounds
    return {"id": id, "name": name, "date": date, "kind": kind, "source_ids": src, "method": method, "level": level, "area_m2": round(P.area, 0),
            "bbox_m": [round(b[2]-b[0], 0), round(b[3]-b[1], 0)], "polygons_m": [C[key]], "note": note}
vers = [
 ver("design_plan_plus_extension_1999", "Construction design plan + southern-arm extension (design drawings, built 1999)", "1992 design (Lyons) / extension 1999; built Feb-Dec 1999", "design_drawing", ["img26", "img06"],
     "Silhouette trace of the outer foot ('interface line') on Blacka et al. (2013) Fig A.2 (Lyons 1992 design plan), scaled from its printed dimensions (6.51 px/m); plus the 'additional fill area' triangle of img06 (320 m3) registered on corners P2 and P1.",
     "outer foot of the designed rock mound (interface line between new rock and the existing seabed), with the extension triangle added at the south-arm end", "v_asbuilt_m",
     "Default: the design drawing of the built reef plus the extension the dossier says was added at the southern end. Not a survey: the built extent is unknown (no aerial or survey image found yet). Extension size is read from a low-resolution drawing."),
 ver("design_plan_original_1999", "Design plan (Lyons 1992 / Fig A.2), before the southern extension", "1992 design drawing, reproduced 2013", "design_drawing", ["img26"],
     "Same silhouette trace as the default, without the extension triangle.", "outer foot of the designed rock mound (interface line)", "v_orig_m",
     "canonical.polygons_m is this polygon. Footprint 4,049 m2; the ramp (area between the set-out line and the crest line) is 3,113 m2."),
 ver("paper_fig7_site_plan_1999", "V outline on the site plan, Pattiaratchi 1999 Fig 7", "1999-04 (paper)", "design_drawing", ["img20"],
     "18 hand-picked vertices of the bold V on the rotated Fig 7 (226 x 367 px raster); 2 m/px assumes the plan's '+' grid is 100 m (label illegible).",
     "outline of the proposed reef as plotted on the site plan (final design)", "fig7_m",
     "Cross-check only. Its assumed scale reproduces the A2 dimensions (122 x 76 m vs 121 x 76 m), which supports the 100 m grid reading."),
 ver("pitt_concept_sketch", "Early concept sketch of the proposed V reef (Pitt)", "1990s (undated)", "other", ["img07"],
     "23 hand-picked vertices of the outer contour of the hand-drawn V; scale from the printed bar 0-200 m (0.855 px/m).", "outer contour of the sketched mound (concept, not the built shape)", "pitt_m",
     "Concept only: a larger (170 x 159 m), symmetric V drawn 100 m off the shore; not the built design."),
]
def src(id, kind, title, url, page, fig, date, credit, local, size, scale, pp, traced, role, reg, match):
    return {"id": id, "kind": kind, "title": title, "url": url, "source_page": page, "page_or_figure": fig, "image_date": date, "credit": credit,
            "license": "not stated / all rights reserved - private research copy", "local_file": local, "image_size": size, "georef": None, "scale": scale,
            "pixel_polygons": pp, "traced_what": traced, "match_notes": match, "role": role, "registry_id": reg}
sources = [
 src("img26", "design_drawing", "Blacka et al. (2013) Fig A.2 'Cable Station ASR Design (After Lyons, 1992)' - plan with RL contours and dimensions",
     "https://doi.org/10.4225/53/58e1dc7368c7a", "UNSW Water Research Laboratory Technical Report 2012/08", "p.93 (PDF p.105) Fig A.2", "1992 design (Lyons); report 11 June 2013",
     "Blacka, Shand, Carley & Mariani; drawing after M. Lyons (1992), UWA", R+"cables-reef-wa_p8-figA2-design-lyons-1992_1992.png", [917, 682],
     {"px_per_m": E['scale_mean_px_per_m'], "method": "printed dimensions",
      "evidence": "4 readings: transect '26.0 m' = %.0f px (%.2f px/m); transect '30.0 m' = %.0f px (%.2f); RL contours at 0.5 m on the printed 1:20 slope are %.1f px apart on the centreline (%.2f px/m); '40.0 m' (RL -3.0 to -1.0 at 1:20) = 258 px (%.2f px/m)" % (E['transect_left_26.0m']['len_px'], E['transect_left_26.0m']['px_per_m'], E['transect_right_30.0m']['len_px'], E['transect_right_30.0m']['px_per_m'], E['contour_spacing_px_mean'], E['contour_spacing_px_per_m_if_1in20_0.5m'], E['dim_40.0m_px_per_m']),
      "uncertainty_pct": 3},
     [T['silhouette_px']], "outer foot of the hatched rock bands (interface line); design ramp polygon in design_surface", "primary", "cables-reef-wa-img-26",
     "Good: silhouette follows the interface line within ~2 px (0.3 m) all round (overlays/cables-reef-wa-img-26_A2_outline_ramp_scale.png)."),
 src("img05", "design_drawing", "Cables Design (caption 'The original design.') - RWR copy of the same Lyons drawing", "https://raisedwaterresearch.com/wp-content/uploads/2019/11/Cables-Design.jpg",
     "https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/cables-reef/", "design section", "1990s (undated)", "Raised Water Research", R+"cables-reef-wa_rwr-original-design-plan_1990s.jpg", [478, 339],
     {"px_per_m": 3.6, "method": "assumed grid", "evidence": "same drawing at 478 px wide, labels illegible; '+' grid 180 px apart assumed 50 m. A2 gives 3.39 px/m for this sheet width, so the assumption was 6% high.", "uncertainty_pct": 25},
     [json.load(open('scripts/p05_toe_pixels.json'))['polys'][0]], "outer foot (silhouette)", "cross_check", "cables-reef-wa-img-05", "Independent re-trace; footprint 4,209 m2 at the assumed scale vs 4,049 m2 on A2 (+4%)."),
 src("img06", "design_drawing", "Cables Additional Fill Area (caption 'The extension to the right.')", "https://raisedwaterresearch.com/wp-content/uploads/2019/11/Cables-Additional-Fill-Area.jpg",
     "https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/cables-reef/", "design section", "1990s (undated)", "Raised Water Research", R+"cables-reef-wa_rwr-additional-fill-area-plan_1990s.jpg", [417, 296],
     {"px_per_m": None, "method": "registered to A2", "evidence": "2-point similarity P2, P1 -> A2: scale %.3f, rotation %.1f deg; 4-point fit on apex, P3, inner apex, valley agrees within 3%%" % (C['reg06_to_A2']['scale'], C['reg06_to_A2']['rot_deg']), "uncertainty_pct": 30},
     [[[76.7, 190.0], [165.0, 212.7], [111.7, 248.3]]], "hatched 'ADDITIONAL FILL AREA' triangle (text: volume 320 m3, mass ~688 t, low resolution)", "cross_check", "cables-reef-wa-img-06", "Triangle picked by eye at 3x zoom, +-3 px; area %.0f m2 on the A2 scale." % C['tri']['area_m2']),
 src("img20", "paper_figure", "Fig 7 'The geographic location of the proposed artificial surfing reef at Cable Station' (printed rotated 90 deg; north to the left)", "http://joas.free.fr/studies/bei/g2s/reefdesign.pdf",
     "same", "p.4 Fig 7", "1999-04-13 (PDF creation date)", "C. Pattiaratchi / Centre for Water Research, UWA", R+"cables-reef-wa_pattiaratchi1999-fig7-geographic-location_1999.png", [226, 367],
     {"px_per_m": 0.5, "method": "assumed grid", "evidence": "'+' grid 50 px apart, 100 m assumed; gives V 122 x 76 m (A2: 121 x 76 m) and centroid 271 m from the shore line (text 250-275 m)", "uncertainty_pct": 15},
     [C['fig7_px']], "bold V outline (rotated frame, north up)", "cross_check", "cables-reef-wa-img-20", "Orientation read from the INDIAN OCEAN label: apex offshore (west)."),
 src("img07", "design_drawing", "Cables Drawing, 'PLAN - PROPOSED CABLES SURFING REEF' (Image: Pitt)", "https://raisedwaterresearch.com/wp-content/uploads/2019/11/Cables-Drawing.jpg",
     "https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/cables-reef/", "design section", "1990s (undated)", "Andrew Pitt (via Raised Water Research)", R+"cables-reef-wa_rwr-pitt-sketch-plan_1990s.jpg", [321, 323],
     {"px_per_m": 0.855, "method": "scale bar", "evidence": "bar 0-200 m = 171 px (native 74..245)", "uncertainty_pct": 10},
     [C['pitt_px']], "outer contour of the hand-drawn mound", "context", "cables-reef-wa-img-07", "Hand sketch; contours drawn, not surveyed; differs from the built design."),
]
orig = C['v_orig']
shape = {
 "slug": "cables-reef-wa", "name": "Cable Station Reef (Cables Reef)", "status": "traced", "updated": "2026-10-10",
 "confidence": {"level": "medium",
   "reason": "Outline traced on a high-resolution copy of the design plan whose printed dimensions (26 m, 30 m, 40 m, 1:20 contours) give the scale to +-3%; size agrees with the text 140 x 70 m within 14% / 9%. It is a design drawing, not a survey, the extension is read from a low-resolution drawing, and no aerial or satellite image could be checked.",
   "factors": ["design plan (Lyons 1992) reproduced in Blacka 2013, not an as-built survey", "scale from four printed dimensions, sd 0.7%", "A2 and the independent RWR copy (img05) agree on area within 4%; the V on paper Fig 7 agrees on dimensions within 1-2% (assumed 100 m grid)", "arm angles %.0f / %.0f deg match the 45 deg design peel angle" % (abs(C['arm_dirs_deg_from_x_axis']['south_arm_outer_edge']), abs(C['arm_dirs_deg_from_x_axis']['north_arm_outer_edge'])), "orientation (apex offshore, north = sheet right) inferred from Fig 7 labels and the Pitt north arrow", "built extent / extension size unknown; satellite and aerial checks need the network"]},
 "design_version": {"drawn": "Lyons (1992) design plan with the 'additional fill area' extension of the southern arm; built Feb-Dec 1999", "why_this_one": "Only plan drawing with legible dimensions; Blacka 2013 (A.1.1) calls this the final reef design; the dossier says the southern end was extended during construction",
   "alternatives_seen": [
     {"what": "Pitt concept sketch (proposal, 100 m off shore, symmetric)", "source_id": "img07", "why_not_used": "earlier concept, different size and shape; kept as a version"},
     {"what": "Oblique wave-basin contour sketch (paper Fig 4)", "source_id": "cables-reef-wa-img-17", "why_not_used": "oblique, no scale"},
     {"what": "2009 Pitt recommendation: shallower reef, longer nose", "source_id": "card R2/R5", "why_not_used": "recommendation, not built"}]},
 "sources": sources,
 "canonical": {"frame": "metres; x alongshore, + toward north (= sheet right); y offshore, + toward west; origin = shoreline point nearest the reef centroid (shoreline assumed N-S); centroid of the default polygon placed 270 m offshore",
   "derived_from": "img26", "polygons_m": [C['v_orig_m']], "area_m2": orig['area_m2'], "bbox_m": {"alongshore": orig['alongshore_m'], "crossshore": orig['crossshore_m']}, "max_dim_m": orig['alongshore_m'], "distance_offshore_m": 270, "shore_normal_bearing_deg": 270},
 "outline_versions": vers, "default_outline": "design_plan_plus_extension_1999",
 "versions_info": "The default outline is the construction design plan (outer foot of the rock mound, traced on Blacka et al. 2013 Fig A.2 after Lyons 1992 and scaled from its printed dimensions) plus the drawn southern-arm extension (320 m3). No survey of the built reef was found, so it is a design drawing, not a measurement. The same plan without the extension, the V printed on the paper's site plan (Fig 7) and an early concept sketch are shown for comparison.",
 "design_surface": {"note": "Design ramp of the Lyons plan: RL contours -1.0 (crest line, inner V) to -3.0 (set-out line, outer edge) every 0.5 m; slopes 1:20 at the apex, 1:15 right arm, ~1:13 left arm (printed labels). Datum of RL not stated on the drawing (see 3d/ and HANDOFF).",
   "levels_RL_m": [-3.0, -2.5, -2.0, -1.5, -1.0], "ramp_polygon_m": C['ramp_m'], "ramp_area_m2": C['ramp']['area_m2'], "source_id": "img26"},
 "geo": None,
 "angles": [{"what": "south arm outer edge vs shoreline (N-S assumed)", "deg": abs(C['arm_dirs_deg_from_x_axis']['south_arm_outer_edge']), "method": "line fit through the outline vertices 16-37, canonical frame (scale-free)"},
            {"what": "north arm outer edge vs shoreline", "deg": abs(C['arm_dirs_deg_from_x_axis']['north_arm_outer_edge']), "method": "line fit through vertices 54-69"},
            {"what": "apex angle", "deg": round(abs(C['arm_dirs_deg_from_x_axis']['south_arm_outer_edge']) + abs(C['arm_dirs_deg_from_x_axis']['north_arm_outer_edge']), 1), "method": "sum of the two arm angles"}],
 "dimensions_check": [
  {"quantity": "length alongshore", "text_value": "140 m (longshore)", "text_ref": "Blacka 2013 Table 4.2 / A.1.1; RWR (card R2)", "drawing_value": "%.1f m (design plan, no extension)" % orig['alongshore_m'], "diff_pct": round((orig['alongshore_m']/140-1)*100), "comment": "text is 'approximately'; drawing printed dimensions give the scale"},
  {"quantity": "width cross-shore", "text_value": "70 m", "text_ref": "same", "drawing_value": "%.1f m (design plan); %.1f m with the extension" % (orig['crossshore_m'], C['v_asbuilt']['crossshore_m']), "diff_pct": round((orig['crossshore_m']/70-1)*100), "comment": "text describes the design plan"},
  {"quantity": "offshore distance (centroid)", "text_value": "250 m (S1) / 275 m (RWR, Blacka)", "text_ref": "S1; Table 4.2", "drawing_value": "271 m measured on Fig 7 (assumed grid)", "diff_pct": None, "comment": "used as input for the origin; not independent"},
  {"quantity": "peel angle / arm angle", "text_value": "45 deg design peel angle", "text_ref": "S1 p.2", "drawing_value": "%.1f and %.1f deg" % (abs(C['arm_dirs_deg_from_x_axis']['south_arm_outer_edge']), abs(C['arm_dirs_deg_from_x_axis']['north_arm_outer_edge'])), "diff_pct": None, "comment": "scale-free"},
  {"quantity": "rock volume", "text_value": "5,500 m3 (Blacka A.1.3); 5,000 (Mead & Borrero 2011, ICM); 3,500 (Wikipedia)", "text_ref": "Blacka; P3; card R1/R4", "drawing_value": "see 3d/METHODS_3D.md (volume above the modelled bed)", "diff_pct": None, "comment": "extension 320 m3 over %.0f m2 = %.2f m" % (C['tri']['area_m2'], 320 / C['tri']['area_m2'])}],
 "gemini": {"values": {}, "sources_used": [], "summary": "Gemini's folder is not in this repo; nothing from Gemini used or checked."},
 "no_source": None,
 "references": [
  {"id": "P8", "citation": "Blacka, M.J., Shand, T.D., Carley, J.T. and Mariani, A. (2013) A Review of Artificial Reefs for Coastal Protection in NSW. WRL Technical Report 2012/08, UNSW Water Research Laboratory", "url": "https://doi.org/10.4225/53/58e1dc7368c7a", "accessed": "papers/ (Lior's copy; intake 2026-10-07)", "supports": "Fig A.2 design plan with RL contours and dimensions; 140 x 70 m; crest submergence 1.0-2.5 m; 275 m offshore; 5,500 m3 granite 1.5 t / 3.0 t; tide range 0.8 m"},
  {"id": "S1", "citation": "Pattiaratchi C.B. (1999) Design studies for an artificial surfing reef: Cable Station, Western Australia. Centre for Water Research, UWA, ref ED1483CP", "url": "http://joas.free.fr/studies/bei/g2s/reefdesign.pdf", "accessed": "2026-10-05", "supports": "3 m contour extended offshore, 1:20 slope up to the 1 m contour, peel angle 45 deg, mean tide level 0.78 m above datum, 250 m offshore, Fig 7 plan"},
  {"id": "R2", "citation": "Raised Water Research (2019) Cables Reef", "url": "https://raisedwaterresearch.com/spot/artificial-reef/australia/western-australia/cables-reef/", "accessed": "2026-09-24", "supports": "drawings img05, img06, img07; 140 x 70 m; 275 m; 3-6 m depth"}],
 "verified_on": None, "verification": [], "checked_without_network": True}
json.dump(shape, open('shape.json', 'w'), indent=1)
print('ok', [(v['id'], v['area_m2'], v['bbox_m']) for v in vers])

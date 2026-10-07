# shape.json spec - 07_scale\shapes\<slug>\shape.json (UTF-8)

{ "slug", "name", "status": "traced|verified", "updated": "YYYY-MM-DD",
  "confidence": { "level": "high|medium|low",
                  "reason": "1-2 plain sentences saying WHY, e.g. 'Outline traced on a 2023 satellite image where the reef is clearly visible; length matches the design report within 5%'",
                  "factors": ["..."] },
  "design_version": { "drawn": "which design / as-built state is drawn, and its date",
                      "why_this_one": "why it is the latest / as-built",
                      "alternatives_seen": [ {"what", "source_id", "why_not_used"} ] },
  "sources": [ { "id": "img1",
                 "kind": "satellite|as_built_survey|design_drawing|aerial_photo|news_graphic|paper_figure|other",
                 "title", "url": "direct image or PDF url", "source_page", "page_or_figure", "image_date", "credit", "license",
                 "local_file": "07_scale/shapes/<slug>/src/<file>", "image_size": [w, h],
                 "georef": null | {"provider": "Esri World Imagery", "zoom", "bounds": {"north","south","east","west"},
                                   "tile_template", "imagery_date", "attribution"},
                 "scale": {"px_per_m", "method": "scale bar | known dimension | georeferenced",
                           "evidence": "e.g. scale bar 0-100 m spans px 112-498", "uncertainty_pct"},
                 "pixel_polygons": [ [[x, y], ...], ... ],
                 "traced_what": "outer toe / crest outline / visible rock / bag field",
                 "match_notes", "role": "primary|cross_check|context" } ],
  "canonical": { "frame": "metres; origin = shoreline point nearest reef centroid; +x alongshore toward <compass dir>; +y offshore",
                 "derived_from": "img id", "polygons_m": [[[x, y], ...]], "area_m2",
                 "bbox_m": {"alongshore", "crossshore"}, "max_dim_m", "distance_offshore_m",
                 "shore_normal_bearing_deg": null | number },
  "geo": null | { "polygons_latlon": [[[lat, lon], ...]], "shoreline_bearing_deg", "method", "source_id" },
  "angles": [ {"what": "e.g. north arm vs shoreline", "deg", "method"} ],
  "dimensions_check": [ {"quantity", "text_value", "text_ref": "card R# / footprint S#", "drawing_value", "diff_pct", "comment"} ],
  "gemini": { "values": {...},
              "sources_used": [ {"url", "what_gemini_said",
                                 "our_check": "correct|wrong_site|wrong_design_version|dimension_not_in_source|dead|unverifiable",
                                 "evidence"} ],
              "summary" },
  "no_source": null | { "searched": ["..."], "gemini_sources": "...", "why_insufficient": "...",
                        "fallback_used": "text-derived schematic from 07_scale/reefs/<slug>.footprint.json" },
  "references": [ {"id", "citation", "url", "accessed", "supports"} ],
  "verified_on": "(set by verifier)", "verification": [ {"check", "verdict", "evidence"} ] }

## Confidence rubric
- high: structure clearly visible on geo-referenced imagery or an as-built survey with a scale, and dimensions agree with text within ~10%.
- medium: traced on a scaled design drawing, or the structure is only partly visible, or dimensions differ 10-25% from text.
- low: no image of the structure; shape inferred from text or a sketch. Fall back to the text-derived schematic and fill "no_source".
The reason must always be stated in plain words; the page shows it next to every drawing.

## Outline versions (added 2026-10-06, Lior's decision)
When a reef has more than one defensible edge definition, store them all and pick a default:
  "outline_versions": [ {"id": "lidar_2022", "name": "Laser survey edge (LiDAR, 19 Mar 2022)", "date": "2022-03-19",
     "kind": "laser_survey|multibeam_survey|design_drawing|photo_trace|other", "source_ids": ["..."], "method": "one sentence",
     "level": "what the edge is (e.g. rock exposed above -2.3 mODN at flight time; design armour foot; visible rock in photo)",
     "area_m2": n, "bbox_m": [L, W], "polygons_m": [[[x,y],...]], "polygons_latlon": [...] (if geo), "note": "..."} , ... ],
  "default_outline": "<id>",
  "versions_info": "2-4 plain sentences for the (i) pop-up: what the versions are, their sources and dates, why the default."
PRIORITY for the default (Lior): measured survey of the structure (laser / LiDAR, multibeam) > design / construction drawing of the
built version > photo trace. The photo trace stays as an optional version. Names must be meaningful and carry the date.
Viewers (Shapes tab, Shape check, 3D viewer, 3D tab) show the default, let the user toggle versions, and put an (i) icon next to the
toggle that opens versions_info plus a small table (name, date, source, area). canonical.polygon_m stays the traced polygon for
traceability; viewers use default_outline when present.

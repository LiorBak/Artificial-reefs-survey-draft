# FEASIBILITY (3D model) - southern-ocean-surf-reef-albany

## UPDATE 2026-10-10 (network run): the 3D model IS now built, with LOW confidence
Decision changed after fetching: seabed depths were found in two places - (1) the Royal HaskoningDHV 2015 "Option B" design plan, which draws coloured seabed contours (-0.5 ... -8 m) over the beach and surf zone, reproduced by Raised Water Research (registry img-16); (2) the BMT 2018 Environmental Impact Assessment, Fig 6.9, which prints spot soundings in m below chart datum (img-14). Contours were georeferenced on the Esri 2025-01-16 image and read along 8 shore-normal transects; the result is a seabed profile (-1 m at 36 m from the dry-sand edge, -3 m at 88 m, -5 m at 126 m, -7 m at 178 m, -8 m at 330 m). Plan (high), crest levels (City design values) and this seabed (low) satisfy the brief's build rule. Model in `3d/` (viewer `3d/index.html`; METHODS_3D.md, REGISTER_3D.md).
What is still missing or weak: no as-built or bathymetric survey; the full Bluecoast Detailed Design Report is not public (only a 5-page executive summary without figures); the 2015 contour datum is unstated (read as AHD); the BMT sounding 2.7 m CD at (x -53, y 32) is 1.6 m deeper than the contours (unresolved); the pile height (mean 2.6 m, max 6.0 m) therefore has +-1 m; the volume of the design outline (34,000 m3) is fitted, not checked (unfitted loft 20,826 m3). Navionics did not render in headless Chrome (nothing bypassed); AusSeabed/GA returned 403; Esri Wayback has only three captures (2022-12-19, 2025-01-16, 2026-01-20), so no construction image. Lior's readings (Navionics, City e-mail) would raise the confidence: `3d/REQUESTS_FOR_LIOR.md`.
Tables below are the offline-run text of 2026-10-10 (before the network run); the "Needs network" list is now done (see HANDOFF.md section 5) except Navionics.


Decision: the 3D model is NOT built yet. The plan shape is traced and verified (confidence high), the crest level and the tides are sourced,
but there is no source for the seabed depth at or around the reef, nor for the height and side slopes of the rock pile. The brief says to
build only if plan, crest and seabed are sourced; the seabed is the gap, and the sources that would fill it are blocked in this container
(general websites, Navionics, EMODnet/AusSeabed). Nothing was invented. Everything else is ready, so a later run can build in about one stage.

## What we have (input: value, source, uncertainty)
| input | value | source | status |
|---|---|---|---|
| a. plan shape | two outlines in a canonical metre frame (x alongshore NNE 30.3 deg true, y offshore 120.3 deg): design outline 13,104 m2, visible-reef outline 10,918 m2; crest bearing 278-282 deg true; 165 m along the crest | shape.json (sat 2026-01-20, Bluecoast plan), VERIFY.md | sourced, high |
| b. crest level | -1.0 m AHD shallowest crest (about 0.74 m below mean low water, 1.34 m below mean high water); crest length 110 m at -2 m AHD | City of Albany design table (img-10) and project page via card R3 | sourced (design value; no as-built survey found) |
| c. height / slopes | NOT given. Layers: belly D50 0.16 m (12,400 t, 18 %), core 0.49 m (23,600 t, 36 %), armour 0.94 m (26,800 t, 46 %); 62,800 t = about 34,000 m3 (design table). Mean height over the design footprint = 34,000 / 13,104 = 2.6 m (inference only) | design table, card R3 | missing (side slope, toe level) |
| d. seabed | NOT given. The design plan shows faint, unlabelled seabed contours east of the reef; the table says volume is "based on 2017 bathymetry". Beach-face to reef: nearest edge 71 m from the dry-sand edge | img-10/img-11 | missing |
| e. tides | mean range 0.4 m, spring range 1.1 m (King George Sound); MLLW = -0.26 m AHD and MHHW = +0.34 m AHD derived from the City's two statements about the crest | card R5, R3 | sourced (derived; datum AHD about MSL) |

## What is missing and why it blocks the build
Without the seabed level at the toe we cannot say how high the pile stands, what the side slopes are, or how the beach profile runs
to the reef; a model with an assumed flat seabed at -4 m would look authoritative and be a guess (the only hint: volume / footprint
gives a mean pile height of 2.6 m, i.e. a seabed of roughly -3.5 to -4.5 m AHD under the crest, but that does not locate the toe, the
profile, or the slopes).

## What would resolve it (any one of 1-3 is enough for a medium-confidence model)
1. Bluecoast Consulting Engineers detailed design report / drawings (cross-sections, 2017 survey contours) via the City of Albany SOSR project page or a papers request. Needs network or Lior.
2. Navionics SonarChart / Garmin chart at the reef (the structure now exists, so it may show in the contours): readings listed below. Needs network (webapp.navionics.com -> maps.garmin.com/en-US/marine/) or Lior's app.
3. Public bathymetry: WA Department of Transport / Geoscience Australia AusSeabed (Albany, King George Sound, nearshore multibeam or LiDAR), 2017 survey by Bluecoast / City of Albany. Needs network.
4. Optional: post-construction as-built survey (City, Mar 2025 practical completion) would also give a measured outline (the default outline version should then be the survey).

## Needs network (exact)
- https://www.albany.wa.gov.au/council/projects/completed-projects/southern-ocean-surf-reef-sosr.aspx and the current-projects page: find the design report / as-built links, re-confirm design.jpg and the table.
- https://www.albany.wa.gov.au/documents/803/albany-artificial-surf-reef-community-update-and-faqs (FAQ PDF, May 2023) for any depth values.
- https://maps.garmin.com/en-US/marine/ (Navionics) zoom 18 at -35.0180, 117.9210: SonarChart and Nautical layers.
- https://ecat.ga.gov.au / AusSeabed portal (https://portal.ga.gov.au/persona/marine) bathymetry tiles for King George Sound / Middleton Beach.
- Esri Wayback releases between 2025-01-16 and 2026-01-20 (satellite.py wayback-list, then fetch at -35.018, 117.9207, r=250 m, z18) to see the construction progress and a second dated image of the finished reef (second check of the soft offshore edge).

## For Lior (Navionics app and Google Earth Pro), points in WGS84 (from scripts/request_points_latlon.json)
| tool | point | read | datum / units | why |
|---|---|---|---|---|
| Navionics | reef centroid -35.018005, 117.920991 | depth at the reef crest and over the reef | note datum/units (m or ft) | crest check vs -1.0 m AHD |
| Navionics | shoreward apex -35.017591, 117.920090; east tip -35.017872, 117.921780; south tip -35.018570, 117.920750 | depth at each | as above | toe depth at the three corners = pile height |
| Navionics | centre line y=50, 100, 300, 400 m: (-35.017485, 117.919902), (-35.017711, 117.920375), (-35.018616, 117.922270), (-35.019069, 117.923218) | depth | as above | seabed profile along the shore normal |
| Navionics | (-35.018487, 117.919823), (-35.018940, 117.920770), (-35.019392, 117.921718) and (-35.016935, 117.920928), (-35.017388, 117.921876), (-35.017841, 117.922823) | depth | as above | seabed 100 m either side, to show the sand-bar and slope |
| Google Earth Pro | beach-face line to apex: ruler from (-35.017258, 117.919428) to (-35.017591, 117.920090) | distance in m | - | confirm 71 m to the dry-sand edge |
| Google Earth Pro | historical imagery slider at the reef | dates of images after 2025-01-16 | - | second image of the finished reef |

## Ready for the build
Shape (both outline versions, lat/lon too), annotated overlays, tide datums, request points, registry updates. When depth data arrive, follow
`_agent_briefs/model_3d.md` and copy the Borth `3d/` pattern (build_3d.py, model.js, docs.js, index.html).

## Source audit 2026-10-10 (see SOURCE_AUDIT_2026-10-10.md for the full tables)
- Sources and how used: Esri World Imagery 2026-01-20 (plan, visible outline); Bluecoast design plan via Raised Water Research (default outline, scale bar); City of Albany design table design.jpg and project profile (crest -1.00 m AHD, 34,000 m3 on 2017 bathymetry, 110 m @ -2 m AHD; re-confirmed by web search 2026-10-10); Wikipedia King George Sound (tide ranges, weak source).
- Assumed (labelled ASSUMPTION in shape.json A1-A9): final design = built reef; design figure north-up and placed by satellite overlap; shoreline = beach-face line; AHD about MSL for the MLLW/MHHW derivation. The "seabed about -3.5 to -4.5 m AHD" remark above is an inference from volume / footprint, NOT used in any model.
- Why no 3D: seabed, pile height and slopes have no source; nothing was invented.
- Confidence: plan HIGH; crest MEDIUM-LOW (design value, no as-built); seabed none; tides LOW-MEDIUM; volume MEDIUM.

# FEASIBILITY - 3D model of Burkitts Reef (2026-10-10): NOT BUILT

Verdict: the brief's rule is BUILD only if (a) plan shape, (b) crest elevation and (d) seabed depth are sourced. Only (a) exists, at low confidence. No 3D folder was created.

| input | what we have | status |
|---|---|---|
| a. plan shape | photo trace of the visible rock platform, Esri 2025-09-05, 31,485 m2 in frame, low confidence (shape.json). UPDATE 2026-10-10: Redgard's Phase 3 work zones located (J&C 2007 Fig 1, georeferenced, ellipse ~1,750 m2, +-20-30 m, LOW); the Feb 1997 first works are still not located. | LOW, partial |
| b. crest level | none. Card: "no shallow-end/minimum depth figure found". Only: boulders worked at low tide with a ~2.5 m tide swing (R4, no datum). Satellite shows the platform awash/exposed, but at an unknown tide. | MISSING |
| c. height, slopes | ~300 m3 moved (R3, R4); with an unknown footprint this gives no height. Natural boulder rock, no designed profile. | MISSING |
| d. seabed depth | none for this site. Dive-site depth "to ~9 m" (R10) is a site-wide maximum, not a profile. No chart, LiDAR or sounding read (network blocked). | MISSING |
| e. tides / datum | ~2.5 m swing (R4, J&C text); J&C Table 1 3.7 m. UPDATE 2026-10-10: MSQ 2026 planes for Burnett Heads retrieved (R20): MHWS 2.94, MHWN 2.35, MLWN 1.20, MLWS 0.61, MSL 1.78, HAT 3.68 m above LAT. Local tides at the site and the AHD link are still not known; tide at image times unknown. | PARTIAL (port values, no site datum) |

Why not "assume and build": a model with an invented platform height and an invented bed would look like data. The reef is also a natural platform: the interesting thing to show is which boulders moved, which nobody recorded.

## What would make it buildable
1. Seabed: Navionics / SonarChart at -24.8153, 152.4671 (z18), or Queensland LiDAR / AusSeabed bathymetry, or Google Earth Pro depth tool (Lior: see REQUESTS_FOR_LIOR.md).
2. Platform crest and tide state: dated low-tide imagery (Esri Wayback releases 2014+, Queensland historical aerials, 1997-98 pair) plus Burnett Heads tide tables for those dates, to calibrate how much rock is exposed at known water level.
3. The reshaped zone: where the ~12 boulders / ~300 m3 were moved. Needs a local account (Redgard, Bargara Boardriders, ABC gallery, Jackson and Corbett 2007) or before/after aerials.
4. A larger south frame (platform continues beyond the current image).
Then the platform could be modelled as a natural shelf (bed -> platform -> reshaped sub-zone) with outline version "photo trace 2025" as default.

## Why this reef is hidden on the page, what was checked, what is assumed (source audit 2026-10-10)
Rule (Lior, 2026-10-10): shapes we do not know are not shown. Burkitts is hidden (footprint.json display:false).
- Why: the only outline we can trace is the natural basalt platform (31,485 m2, a minimum because the image frame cuts it). The reef is the boulder sub-zone moved in 1997 (about 300 m3, about 12 boulders; card R1, R3, R4) and no source says where on the platform it is. Drawing the platform would present the stage as the reef.
- What was checked (with sources): Esri World Imagery 2025-09-05 (img-08, georeferenced; platform visible, sub-zone not); card and dossier (no footprint figure); Redgard petition sketch 7 Sept 1980 (img-01; no scale, no north); registry images 02-05 (no scale); registry 06-07 rejected (a dive video at a marine-park reef that shares the name); earlier Google Maps estimate 120 x 46 m (not reproducible); Gemini 80 x 40 m (uncited, dead links); WebSearch 2026-10-10 for tide levels (Maritime Safety Queensland tidal planes for Burnett Heads exist, values not retrieved).
- Assumed: A1-A8 in shape.json (platform = stage; edge = breaker line at unknown tide; no change since 1997; tide swing ~2.5 m, single source, no datum).
- The "dive depth to ~9 m" (R10) is not used as seabed: the card calls the dive site the same headland, the registry rejected the dive video as another place. Unresolved.
- Confidence: platform outline LOW; reef zone, crest, seabed: none. Full tables: SOURCE_AUDIT_2026-10-10.md.

## Network pass 2026-10-10 (full access): what changed, what did not
- Found: where the reshaping work areas are, in the only form any source gives them: Redgard's Phase 3 annotated oblique aerial (Jackson and Corbett 2007, Fig 1; RWR copy). Georeferenced with 3 GCPs onto Esri imagery 2016-07-31: zone 'Remove to lengthen break' = ellipse ~1,750 m2 (43 x 52 m) on the inner rock flat just seaward of the rock pool; other marks are arrows (surface rocks near the pool, shore break at the NE platform edge, dangerous rocks on the east flank edge). shape.json: reef_zone.located True (LOW), outline version phase3_work_zone_ellipse_esri2016. Display: possible only as a labelled secondary layer 'Phase 3 work zones (Redgard), approx +-25 m, not the 1997 works' - switch (footprint.json) left to main/Lior.
- Not found: the 1997 first works; any crest, seabed or platform level. BRC 2016 1 m LiDAR DEM has NoData over the whole platform and the zone (lowest valid cell 0.58 m, datum not stated); no AusSeabed survey found; QImagery archive needs a token (not bypassed); SurfingRamps unreachable; no pre-2010 satellite imagery exists on Wayback. 3D remains NOT buildable (crest and seabed still missing).
- Tides: see row e above. Dead ends: 02_research/dead_ends/burkitts-reef-bargara.json.
- What would still help: Redgard / Bargara Boardriders (Phase 1-3 maps, Redgard 2006 pers. comm. cited by J&C), Pitt (2005) 'Redgard the Reef Renovator' (Artificial Surf Reef Conference), QImagery 1996-98 aerials via the request form (Lior), Navionics / Google Earth Pro readings.

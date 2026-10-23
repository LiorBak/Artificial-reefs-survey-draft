# HANDOFF - burkitts-reef-bargara (queue item 9, agent run 2026-10-10; for the page builder and any later agent)

## 1. Status per stage
- Trace: platform outline DONE 2026-10-10, LOW (Esri 2025-09-05, img-08) = the stage, not the reef. REEF ZONE LOCATED 2026-10-10 (network pass), LOW: Redgard's Phase 3 work zones from J&C 2007 Fig 1 georeferenced onto Esri 2016-07-31 (shape.json reef_zone, outline version phase3_work_zone_ellipse_esri2016; METHOD section 7). The Feb 1997 first works are still not located.
- Verify: DONE as a documented self-check (VERIFY.md); overlay match "approximate". Status "verified" with that caveat; an independent check was not possible (no second image).
- 3D: NOT BUILT. FEASIBILITY.md (missing crest, seabed, datum, reshaped-zone location).
- Registry: img-08 and img-01 rows updated with results; no new images.
- Page: not touched (04_build is main's). Add the slug to data/models3d_hold.json ("Not yet modelled"). DISPLAY DECISION for main/Lior: shape.json reef_zone.displayable = true (low) only as a labelled secondary layer 'Phase 3 work zones (Redgard, via Jackson and Corbett 2007), approx +-25 m, not the 1997 works'; footprint.json display is still false (outside this agent's scope).

## 2. Key decisions
- Trace the whole visible platform in frame (not the 120 x 46 m earlier estimate: not reproducible, no saved image).
- Frame N-up (x east, y north, origin = polygon centroid) because the platform wraps a curved headland; stated in shape.json.
- One outline version only (photo trace, default by necessity); versions_info says so.
- Polygon cut by image frame at the south (y=1991 px): area/bbox are minimums.

## 3. Key numbers
- Area 31,485 m2 (UTM 56S; 31,508 geodesic; 31,646 pixel x 0.271^2). bbox 321 E-W x 377 N-S m; perimeter 1,133 m; centroid -24.81574, 152.46750. Scale 0.2710 m/px from sidecar bounds (img1). Source: scripts/computed_v1.json.
- Edge trends: east flank seaward edge ~160/340 deg true; north-facing edge ~107 deg true.
- Text numbers (card, not re-fetched): works Feb 1997; ~300 m3; ~12 boulders; AUD 10,000; tide swing ~2.5 m (R4, no datum); dive depth to ~9 m (R10). Card lat/lon (24.8205, 152.4625; also wrong hemisphere sign in the JSON as stored) is Bargara town centre, not the reef: reef is at about -24.8157, 152.4675.
- No crest, seabed or datum numbers exist.

## 4. File map (07_scale/shapes/burkitts-reef-bargara/)
- shape.json: spec-conform; outline_versions, default_outline, geo polygon, verification array.
- METHOD.md (vertex list, steps), sources.md, VERIFY.md, FEASIBILITY.md.
- overlays/img08_esri_2025-09-05_rock_platform_trace_v1.png (4 MB-class, full frame, filled outline + numbered vertices).
- scripts/: pixel_polygon_v1.json (the vertices), compute_shape.py (run `python -I scripts/compute_shape.py <this folder>`), computed_v1.json.
- src/: Esri image + .geo.json (bulky, 5 MB).

## 5. Open issues
- Reshaped zone location unknown; platform vs reef distinction must be on the page.
- Image tide state unknown; waterline edge could shift tens of metres.
- Truncated at south.
- Gemini checks (404, homepages) are from the 2026-09-25 pass, not re-fetched.

## 6. Next steps
1. When network is wider: fetch the needs-network list below, re-trace on a larger frame and dated low-tide images.
2. Lior readings (Navionics, Google Earth) -> re-run feasibility; build 3D only if crest, seabed, datum become sourced.
3. Ask Redgard / Bargara Boardriders (via Lior) which boulders were moved.

## 7. NEEDS NETWORK - DONE 2026-10-10 (full network pass; results in section 8; the list below is the original request, kept for traceability)
1. Esri Wayback list + tiles at centre -24.8153, 152.4671, z19, extended south to lat -24.8235 (the platform continues): `python 07_scale/tools/satellite.py wayback-list`, then `satellite.py fetch --lat -24.8175 --lon 152.4680 --radius-m 450 --zoom 19 --wayback <release>`; hosts server.arcgisonline.com, wayback.maptiles.arcgis.com, s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com. Why: dated images at known low tide, larger frame, 2014+ only.
2. Navionics ChartViewer https://webapp.navionics.com/ (redirects to https://maps.garmin.com/en-US/marine/), SonarChart + Nautical, z18 at -24.8153, 152.4671. Why: bed depths off the platform.
3. Queensland Government imagery / elevation: https://qldglobe.information.qld.gov.au/ and https://qimagery.information.qld.gov.au/ (historical aerials 1990s, may need a request form: not bypassed); ELVIS LiDAR https://elevation.fsdf.org.au/ ; AusSeabed https://portal.ga.gov.au/ . Why: before/after 1997, platform level, bathymetry.
4. Tide tables: Queensland Government Burnett Heads tides https://www.qld.gov.au/transport/marine-safety/tides (verify current URL), or BoM. Why: datum, LAT, MSL, HAT; tide at image times.
5. Original ABC article page and its other photos https://www.abc.net.au/news/2024-01-28/diy-surf-break-built-by-mates-at-burkitts-reef-bargara/103387450 ; Raised Water Research page; Swellnet comment 540429 (re-read for any location detail). Why: wide shots showing the reshaped zone.
6. Jackson and Corbett 2007, "Review of Existing Multi-Functional Artificial Reefs" (ICCE / Griffith); SurfingRamps.com.au (Andrew Pitt) page on Burkitts. Why: possible dimensions or a plan.
7. Wikimedia Commons / Google Maps low-tide photos of Burkitts Reef, Bargara. Why: exposed boulder field.

## Source audit 2026-10-10
SOURCE_AUDIT_2026-10-10.md in this folder holds the sources-with-how-used, statement check, assumptions (A#), decisions (D#), confidence and consistency tables. FEASIBILITY.md / shape.json now carry the why / checked / assumed text (page_status for hidden reefs). Open mismatches are listed in the audit section 2. If kovalam build_shape_json.py is re-run it overwrites the audit additions in shape.json: re-apply from the audit.

## 8. Network pass 2026-10-10 (agent Burkitts+Mexico, cloud) - results per item of section 7
1. Esri Wayback: 197 releases scanned; distinct images at z18: 2016-07-31 (release 23264), 2022-10-03 (47963), 2024-06 (12428, capture not queried), 2025-02-26 (25285), 2025-09-05 (22252 = current); 2010-09-11 only at z17 (release 10). Saved: wide 2016 and 2025-02 frames, north 2016 frame, 2010 z17 (src/wayback/, registry img-15..18). No pre-2010 imagery. Larger south frame saved (platform continues south of the 2025 frame; not re-traced, D8).
2. Navionics: not fetched (interactive app; Lior reading still needed).
3. QImagery archive: ImageServer needs a token (not bypassed) -> Lior via browser/request form. BRC 2016 1 m DEM (public REST): platform and zone NoData (lowest valid 0.58 m). ELVIS: shell only. AusSeabed: no Bargara survey found.
4. Tides: MSQ 2026 planes Burnett Heads retrieved (R20): MHWS 2.94, MHWN 2.35, MLWN 1.20, MLWS 0.61, MSL 1.78, HAT 3.68 m above LAT. J&C 2007: spring range ~2.5 m in text, 3.7 m in Table 1 (both kept; they match MHWS-MLWS 2.33 and HAT-LAT 3.68).
5. ABC article / RWR page / Swellnet re-fetched: no wide shot in ABC; RWR 'Burkitts.jpg' = the Phase 3 aerial; text saved in src/web_text/.
6. J&C 2007 fetched (src/docs/): Fig 1 = KEY FINDING; text: site is on the north side of a headland, effectively a half V; no modelling; initial works monitored on the 'full scale model', additional works 'designed' (Redgard 2006, pers. comm.); no monitoring done; Pitt (2005) 'Redgard the Reef Renovator' cited (not found online). SurfingRamps unreachable.
7. Wikimedia / low-tide photos: none found.
- New numbers: zone ellipse 1,750 m2 (43 x 52 m), centroid -24.81510, 152.46652, +-20-30 m (METHOD 7.5-7.6); arrow tips in scripts/phase3_zone_v1.json.
- New open items: (a) Phase 1-3 maps / what was built when: Redgard, Bargara Boardriders, Pitt 2005 (Lior); (b) QImagery 1996-98 aerials (Lior, browser); (c) a second oblique or more GCPs to firm up the position; (d) display decision (above); (e) re-trace the platform on the larger frame if the platform is ever shown.
- File map additions: src/docs/ (J&C PDF, MSQ PDF), src/web_text/, src/wayback/ (4 images + sidecars), src/dem/ (REST samples), overlays/img10_*, img11_*, scripts/phase3_zone_georef.py, render_phase3_overlay.py, phase3_zone_v1.json. Re-running phase3_zone_georef.py needs only numpy and pyproj (already installed).

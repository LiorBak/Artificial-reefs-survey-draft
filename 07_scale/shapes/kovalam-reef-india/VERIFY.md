# VERIFY - kovalam-reef-india (2026-10-10, same agent as the trace; adversarial self-check, no independent source reachable)

Verdict: shape stays LOW confidence. Photo-space trace is fair; metric scale is NOT supported by the photo alone.

| # | check | verdict | evidence |
|---|---|---|---|
| 1 | Overlay follows the structure | approximate | overlays/img1_trace_v2.png: outline hugs the 5-6 strips and the whitewater patch; the left tip (x 90-200) is a guess into haze, faint streaks right of the whitewater are excluded. Re-rendered from pixel_polys_img1_v2.json by overlay.py render and from rectify_fit.py (img1_camera_fit_check.png). |
| 2 | Design version / state | as-built, early life | One built version (Feb 2010). Aerial is between completion and 2011-03 (brochure date). Later deflation/sinking (RWR; WRL p.70) not drawn; no 2013+ imagery of the structure. The page must say so. |
| 3 | Scale | FAILS to be determined | Camera fit rms is 2.2-2.8 px for camera height 30-80 m, so the photo carries no scale. Footprint 546-1,681 m2 over that range (rectify_result.json). The default (60 m) rests on a lens argument plus WRL's 90 m. |
| 3b | Tool bug check | n/a | geom.py make-canonical NOT used; rotation done explicitly in rectify_fit.py canon(): x = d.t, y = d.n. One point checked by hand: vertex 8 canonical (33.7, 105.7) m; its lat/lon (polygon_latlon[8]) differs from the frame origin by 110.9 m west, 3.1 m south; projecting on the frame axes (bearings 196 / 286 deg) gives x 33.5, y 105.8 m. OK (0.2 m). |
| 4 | Dimensions vs text | partial | WRL Table 4.2: 65 x 85 m, 90 m offshore. H60: 59 x 41 m (-9% / -52%), nearest edge 65 m off the 2011 swash line (75-95 m off the pre-reef shoreline, since the beach widened 10-30 m). H80: 64 x 68 m (-2% / -20%), 92 m. Volume 4,000 m3 over 1,216 m2 would be 3.3 m mean height: the real footprint is likely larger than the traced strips. The 65 x 85 m "max dimensions" may include faint outer strips or design extent. |
| 5 | Provenance | ok | sources.md rows with URL, page, date, credit, licence; every number in METHOD.md has a method or file. Swash points are eyeballed (+-6 m on satellite). |
| 6 | Gemini | not re-checkable | no network. Earlier agents (2026-09-25): crest 1.6 m citations unfindable, offshore 150 m circular, shape smooth crescent. Not used. |
| 7 | Confidence honest | yes | low per SHAPE_SPEC rubric: structure visible but not scaled/georeferenced, dimension disagreement > 25% in one axis. |

## Sensitivity at the default (H 60 m)
- horizon row 185 / 197 (+-6 px): area 1,251 / 1,177 m2, FOV 68 / 78 deg.
- satellite swash line moved 10 m seaward / landward: area unchanged (1,216), reef moves 3 m.
- 2010 aerial vs 2011 satellite swash line: the beach changes by 10-30 m between seasons (Mead & Borrero 2011 s.4.1.4); this is the main positional risk (+-20 m).

## Corrections made to earlier work
- The 2026-09 draft crescent polygon (pixel_polys_img1.json, 56 m offshore centroid) is superseded: it outlined the dark patch, not the strips.
- Registry img-09 file name says 2014 but the capture date is 2011-02-28 (noted in sources.md).

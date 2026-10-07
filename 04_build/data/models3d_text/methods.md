This section sets out, once for all models, how the 3D models were built and how far they can be trusted. It is written from the per-model documents (METHODS_3D.md, SOURCES_3D.md; section numbers are cited like "Pratte's 3.2" and link into the document above) and from the two bathymetry reports. Nothing here is a new measurement. Each model is a *reconstruction from published figures, charts and text*, not a survey: every number carries a source id in the model's provenance table, and what is assumed is marked as assumed.

### 1. Canonical frame and the three.js mapping

All models use the frame of the reef's verified `shape.json` (project spec `SHAPE_SPEC.md`): metres, **x alongshore**, **y offshore** (positive seaward), **z up**, **z = 0 at mean sea level (MSL)**. The origin lies on the waterline of the source image or survey used for the plan. Whether the triple (x, y, z up) is left- or right-handed depends on the sense in which +y is +x turned: for Pratte's Reef (x at 155 deg, y at 245 deg), Boscombe (83.4 / 173.4 deg) and Palm Beach (334.3 / 64.3 deg) +y is +x turned **clockwise** seen from above, so the triple is **left-handed**; for Bunbury (x at 12.32 deg, y at 282.32 deg) it is turned anticlockwise and the triple is right-handed ([Pratte's 3.1](#m3d-prattes-reef-el-segundo-m-3-1), [Boscombe 3.1](#m3d-boscombe-surf-reef-m-3-1), [Bunbury 3.1](#m3d-bunbury-airwave-m-3-1), [Palm Beach 3.1](#m3d-palm-beach-gold-coast-m-3-1)).

The viewer is three.js r170 (right-handed, Y up). To avoid mirroring the reef the models are mapped as

```
Pratte's, Boscombe:  (X, Y, Z) = (x, z, y)        (left-handed canonical frame -> mirror-free)
Bunbury:             (X, Y, Z) = (x, z, -y)       (right-handed canonical frame)
Palm Beach:          E = x sin(bx) + y sin(by),  N = x cos(bx) + y cos(by),  (X, Y, Z) = (E, z, -N)
```

The Palm Beach model checks the frame against `shape.json`: the 47 vertices are reproduced to 0.024 m, whereas a mirrored x gives a mean error of 82.4 m ([Palm Beach 3.1](#m3d-palm-beach-gold-coast-m-3-1)). Compass bearings follow `bearing = bx + atan2(...)` with the true bearing of +x (north in the model frame is shown by the north arrow of each viewer).

### 2. Plan shape

The toe polygon of each model is the **verified trace** in `07_scale/shapes/<slug>/shape.json` (traced on a scaled source image, verified 2026-10-04/05; its own *plan* confidence is separate from the 3D confidence). Sources: Pratte's, the Skelly Engineering design drawing (76 vertices, 435.2 m2, the design layout, **not** an as-built plan); Boscombe, the Esri Wayback image of 2011-09-28 (25 vertices, 4,042 m2); Bunbury, a drone photograph with the text-stated 12 m diameter (112.1 m2); Palm Beach, the Bluecoast/Nearmap aerial (47 vertices, 11,972 m2; intersection over union 0.995 with the City of Gold Coast polygon).

### 3. Crest, toe and flank lofting

The surface is a smooth height field; individual bags, containers or rocks are not drawn. The rules differ per structure because the evidence differs:

```
Pratte's:   h(x,y) = max(0, min(h_top, d_in(x,y)/s)),   z_surface = z_bed(y) + h              (s = 1.0, range 0.5-2.5; h_top = z_crest - z_bed, at least one 1.2 m bag course)
Boscombe:   r(x,y) = clip(r0 + phi/m, 0, H_c),   H_c = max(z_c - S, 0),   z_reef = S + r      (r0 = 1.0 m, m = 3.0, z_c = +0.5 m ACD; phi = signed distance inside the outline)
Bunbury:    symmetric spherical cap on the sloping bed, base D = 12 m, height H = 2.0 m (range 1.6-2.0)
Palm Beach: z_k = z_c - Delta k,  z_toe = z_c - Delta (K + f)                                 (Delta = 0.5 m assumed; z_c = -1.5 m MSL; Delaunay TIN through the traced contour lines)
```

Here `d_in` is the distance from a point inside the toe outline to the outline, `s` and `m` are horizontal run per metre of rise, and `S` is the ambient (pre-reef) seabed ([Pratte's 3.7](#m3d-prattes-reef-el-segundo-m-3-7), [Boscombe 3.5](#m3d-boscombe-surf-reef-m-3-5), [Bunbury 3.5](#m3d-bunbury-airwave-m-3-5), [Palm Beach 3.4](#m3d-palm-beach-gold-coast-m-3-4)). Volumes are the sum of height over a 0.25-1 m grid (rock *envelope*, voids included, for Palm Beach).

### 4. Seabed

| model | seabed source | construction |
|---|---|---|
| Pratte's | NOAA 1/3 arc-second DEM (2010; surveys 1932-2009), check: Garmin Navionics, NOAA CRM | mean of 31 alongshore profiles re-expressed from each profile's own MSL waterline (E8); reef assumed absent from the DEM |
| Boscombe | April 2011 DGPS bathymetry plot, Rendle & Davidson (2012) Fig. 9 | colour bar to height (+-0.2 m), resampled to 1 m; ambient seabed = thin-plate spline through cells outside the reef mask (Duchon 1977; fit r.m.s. 0.021 m); beach and corners extrapolated |
| Bunbury | WA Department of Transport airborne lidar 2009 (10 m cells, AHD), check: Navionics | alongshore median profile; 286 of 2,989 nodes gap-filled; smooth 1:24 slope |
| Palm Beach | Garmin Navionics SonarChart iso-depth lines (1-10 m), no surveyed depth read | thin-plate spline through the lines more than 25 m from the reef, 25 waterline anchors and the toe elevations; `z_b = -d_nav - 0.88` |

### 5. Datums, with the equations used

Every source states heights against its own datum; each model converts to MSL with a published offset. Writing `D` for the source datum and `MSL - D` for its height below MSL:

```
z_MSL = z_D - (MSL - D)                                           (general form)
Pratte's (NOAA CO-OPS 9410840, epoch 1983-2001):  z_MSL = z_MLLW - 0.849 ;  z_MSL = z_NAVD88 - 0.792 ;  LAT = -1.469, HAT = +1.382
Boscombe (NTSLF: chart datum 1.40 m below Ordnance Datum; ODN ~ MSL +-0.1 m):  z_MSL = z_ACD - 1.40 ;  HAT = +1.19, LAT = -1.46
Bunbury (GHD 2021 Table 1; DoT index LAT = AHD - 0.57):  z_MSL = z_AHD - 0.1 ;  LAT = -0.7, HAT = +0.5 (model z)
Palm Beach (MSQ 2026, Gold Coast Seaway):  z_MSL = z_LAT - 0.88 ;  MSL = LAT + 0.88,  HAT = LAT + 2.03 ;  z_MSL = z_AHD - 0.12 (MSL - AHD at the Seaway)
```

Tide levels are static planes (no time curve, set-up or surge). Datum transfer from the gauge to the site is assumed valid (Pratte's 11.7 km, +-0.03 m; Boscombe 1.5 km; Bunbury 3 km, +-0.1 m including the 0.1 m rounding; Palm Beach 18 km, +-0.1 m, MSQ has no Palm Beach row). The datum of each *source* is a separate question: where it is not stated (Boscombe Fig. 9; the Navionics app) it is inferred and flagged with its consequence (Boscombe: +-1.4 m on all absolute heights, relief unchanged).

### 6. Reading the Navionics chart, and inferring its datum

The Garmin Marine Maps viewer (the former Navionics web app) opened without login, CAPTCHA or consent in the author's own headless Chrome (random free DevTools port, fresh profile; never the shared browser) and was read at zoom 17-18 with Web-Mercator scale `res = 156543.034 cos(lat) / 2^zoom` (0.50 m/px at Pratte's, 0.378 m/px at Boscombe, 0.2495 m/px at Bunbury, 0.527 m/px at Palm Beach). Contours were counted or extracted (the edge of the "shallow shading" band is the contour of that depth), labels and soundings were read by eye. The app **states neither datum nor contour interval**, and the charts are crowd-sourced and "not to be used for navigation", so the datum is inferred by testing candidates against an independent source with the root-mean-square difference

```
RMS(o) = sqrt( mean[ (z_reference - (z_nav + o))^2 ] )         o = offset of the candidate datum above/below the reference
```

Results (RMS, m): Pratte's (reef zone, 7 labels vs the DEM) MLLW 0.29, NAVD88 0.32, LAT 0.54, MSL 1.02 - MLLW and NAVD88 are only 0.057 m apart and cannot be separated; Bunbury (111 contours vs the 2009 lidar) LAT 0.32, MLLW 0.67, AHD 0.87, MSL 0.96 - LAT best; Palm Beach (427 toe points) LAT 0.61, MSL 1.28 - LAT best, but the "reference" there is the aerial's own contour lines, so the test is not independent. At Boscombe chart datum was assumed and the shoal areas of the chart match the April 2011 survey to 1-2 % at the 0.5 m and 1 m levels ([Pratte's 3.5](#m3d-prattes-reef-el-segundo-m-3-5), [Boscombe 3.6](#m3d-boscombe-surf-reef-m-3-6), [Bunbury 3.6](#m3d-bunbury-airwave-m-3-6), [Palm Beach 4.3](#m3d-palm-beach-gold-coast-m-4)). Where the structure was removed (Pratte's) the chart gives the seabed only.

### 7. Uncertainty propagation

Independent errors are added in quadrature (first order); the ranges are judgement-based 1-sigma-like values with their basis stated in each model's section 5, not statistical intervals:

```
reef height      H = z_c - z_b             sigma_H^2 = sigma_zc^2 + sigma_zb^2          Pratte's: sqrt(0.3^2 + 0.8^2) = 0.85 m ;  Palm Beach: sigma_zb = 0.46 m -> sigma_H = 0.54 m
crest depth      d_c = P - z_c             sigma_dc^2 = sigma_zc^2 + sigma_P^2          (P = tide plane: LAT, MLLW, ...)
seabed           sigma_zb^2 = (slope x sigma_y)^2 + sigma_survey^2 + sigma_change^2    Bunbury: sigma_zb = 0.61 m, sigma_dc = 0.63 m (Monte Carlo 0.69 +- 0.66 m)
volume           Boscombe ~16 % ;  Palm Beach sigma_V = A x sigma_zb = +-6,000 m3 (28 %) ;  Pratte's sigma_V = 136 m3 (state B)
```

### 8. Confidence rubric (3D)

The plan-shape rubric of `SHAPE_SPEC.md` covers only the outline; the 3D rubric was extended by the model authors. Pratte's and Bunbury use the same words: **high** = built-state footprint from a survey or georeferenced image, crest and seabed from surveys at the site and consistent within 0.3 m, position known to better than 10 m (Bunbury adds: a measured as-built surface); **medium** = all vertical inputs sourced and consistent within 0.5 m, with at most one of (footprint is a design or the surface shape is assumed; position known only to +-50 m; assumed stack height); **low** = two or more of those, or vertical uncertainty at least half the reef height. Palm Beach uses a variant: *high* = crest, height and seabed each from a surveyed value or two agreeing surveys; *medium* = geometry rests on sourced plan/crest/tide values and on depth inferred from two mutually consistent but unlabelled or datum-less sources, with a stated uncertainty and no contradiction larger than twice that; *low* = depth guessed. Boscombe is judged against the same rubric (section 6). The badge and its reason are always shown at the head of each model above ([Pratte's 6](#m3d-prattes-reef-el-segundo-m-6), [Boscombe 6](#m3d-boscombe-surf-reef-m-6), [Bunbury 6](#m3d-bunbury-airwave-m-6), [Palm Beach 6](#m3d-palm-beach-gold-coast-m-6)).

### 9. Vertical exaggeration

The viewers offer a vertical exaggeration VE of 1-5x (default 1x, always displayed) that multiplies **every** height, including the water level and datum labels, and never a plan distance: `tan(theta_apparent) = VE tan(theta_true)`. A 1:3 flank (18.4 deg) looks like 33.7 deg at VE 2 and 59 deg at VE 5. Camera angles read for photo matching are valid only at VE = 1, so photo-match mode forces VE = 1. All numbers in this tab are true values.

### 10. What the picture galleries show

Under each model the gallery lists the images that were read to build it, grouped by the quantity they fixed (plan shape, crest and height, seabed and depth, tides and datum, validation) and, separately, images flagged in the registry (`for_3d_check.pending`) as able to confirm or contradict a model value but **not yet checked**. Hovering a picture shows how it was used and its source; clicking opens a larger view with the full citation, licence and, where one exists, the annotated version showing what was read. All pictures are private research copies; **reuse rights have not been cleared for public release** (see the licence line of each picture).

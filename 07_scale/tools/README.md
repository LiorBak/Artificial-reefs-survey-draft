# Shape-tracing toolkit — `07_scale/tools/`

Three scripts used together to trace a reef's outline off satellite imagery and turn it
into the canonical metres frame described in `07_scale/SHAPE_SPEC.md`:

- **`satellite.py`** — fetch a stitched, cropped Esri World Imagery PNG (current or a
  dated Wayback release) around a lat/lon, with a `.geo.json` sidecar giving exact
  Web-Mercator bounds, zoom, metres-per-pixel, and (best-effort) the imagery capture date.
- **`overlay.py`** — draw traced polygons on top of an image for visual QA: filled +
  outlined + numbered vertices, an optional labelled pixel grid, a zoom-crop with a
  precise coordinate grid for reading vertices by eye, and a two-colour A/B comparison.
- **`geom.py`** — polygon geometry (area, bbox, centroid, max dimension), pixel↔metres
  and lat/lon↔local-metres conversions, edge bearings and shoreline angles, a
  least-squares similarity-transform fit for checking control points, and
  `make-canonical`, which fills a `shape.json`'s `canonical` block directly from one
  source's traced pixel polygons + scale.

Requires `pillow` and `requests` (`pip install pillow requests`); both were already
present in this environment (Pillow 12.2.0, requests). Python 3.14 used for testing.

All three scripts are both **importable modules** (`from geom import shoelace_area, ...`)
and **CLIs** (`python geom.py area --polys ...`). JSON in, JSON out, so they chain in
PowerShell or Bash without extra glue.

Quote every path that contains spaces — the project root has one
(`Artificial reef`).

---

## 1. `satellite.py`

### `fetch` — stitch tiles into a PNG + `.geo.json`

```
python satellite.py fetch --lat LAT --lon LON --radius-m R --zoom Z --out PNG [--wayback RELEASE]
```

Downloads the Esri World Imagery tiles (`.../World_Imagery/MapServer/tile/{z}/{y}/{x}`,
or the dated Wayback endpoint when `--wayback RELEASE` is given) that cover a
`radius-m`-metre box around `(lat, lon)` at zoom `Z`, stitches them, crops exactly to the
requested box, and writes:

- `PNG` — the stitched image.
- `PNG.geo.json` — `{image, width, height, bounds:{north,south,east,west}, zoom,
  m_per_px_center, tile_template, wayback_release, center:{lat,lon}, radius_m,
  attribution, retrieved, capture_date, capture_date_field}`.

Worked example (also the brief's test case, Narrowneck Reef, Gold Coast):

```
python satellite.py fetch --lat -27.9965 --lon 153.4305 --radius-m 300 --zoom 18 --out narrowneck.png
```

Result on this machine: a 1138×1138 PNG, `m_per_px_center` = **0.5273 m/px** at zoom 18,
and `capture_date` = **2025-10-10** (found via the `DATE (YYYYMMDD)` field of the Esri
`identify` operation — see Caveats).

Historical imagery (`--wayback RELEASE`, release ids from `wayback-list` below):

```
python satellite.py fetch --lat -27.9965 --lon 153.4305 --radius-m 150 --zoom 17 --wayback 22869 --out narrowneck_2026-03.png
```

Capture date for a `--wayback` fetch is looked up against *that release's own*
`metadataLayerUrl` (from `waybackconfig.json`), not the live MapServer, so it reflects
the imagery actually baked into that release where possible.

### `wayback-list` — available dated releases

```
python satellite.py wayback-list
```

Prints `release_id   date   title`, newest first, e.g.:

```
   26334  2026-08-05    World Imagery (Wayback 2026-08-05)
   32246  2026-06-30    World Imagery (Wayback 2026-06-30)
```

Pick the `release_id` whose date is closest to (and not after) the design/as-built date
you need, and pass it as `fetch --wayback RELEASE`.

### `pix2ll` / `ll2pix` — convert using a `.geo.json` (no network)

```
python satellite.py pix2ll --geo narrowneck.png.geo.json --x 569 --y 569
python satellite.py ll2pix --geo narrowneck.png.geo.json --lat -27.9965 --lon 153.4305
```

Both work purely from the sidecar's stored `bounds` + `width`/`height` (linear
interpolation in Web-Mercator projected space, then projected back to lat/lon — exact,
not an approximation), so you can re-derive lat/lon for any traced vertex later without
re-fetching anything.

---

## 2. `overlay.py`

### `render` — draw one polygon set

```
python overlay.py render --image narrowneck.png --polys polys.json --out narrowneck_overlay.png --grid 100
```

`polys.json` (or a literal JSON string) = a list of polygons, each a list of `[x, y]`
pixel points, e.g. `[[[500,500],[600,500],[620,580],[520,600]]]`. Draws a semi-transparent
fill (`--alpha`, default 0.35), a solid outline, numbered vertices (`0,1,2,...`;
`--no-labels` to turn off), and an optional yellow pixel grid every `--grid N` pixels
with coordinate labels — handy for reading off a rough `(x,y)` before doing a precise
`zoom`.

### `zoom` — crop + enlarge with a precise coordinate grid

```
python overlay.py zoom --image narrowneck.png --box 450 450 700 650 --scale 3 --grid 25 --out narrowneck_zoom.png
```

Crops `[x0,y0,x1,y1]` = `450 450 700 650` (**original-image pixel coordinates**),
enlarges ×3 (LANCZOS resample), and draws grid lines + tick labels **still in the
original image's pixel coordinates** (not the enlarged ones) at every multiple of
`--grid` — so you can read a vertex's true pixel position directly off the zoomed PNG
by eye, then type it straight into a `shape.json`.

### `compare` — two outlines, two colours

```
python overlay.py compare --image narrowneck.png --polys ours.json --polys2 gemini.json --out compare.png
```

Set A (`--polys`) draws red, set B (`--polys2`) draws cyan, both filled + outlined +
numbered — e.g. to sanity-check our trace against Gemini's footprint on the same image
(remember: Gemini's footprints are known to be partly wrong; this is for visual
comparison only, never a source).

---

## 3. `geom.py`

All subcommands read `--polys`/`--pairs` as either a path to a JSON file or a literal
JSON string, and print JSON to stdout.

| Command | Purpose | Example |
|---|---|---|
| `area` | shoelace area of each polygon + total | `python geom.py area --polys "[[[0,0],[10,0],[10,5],[0,5]]]"` → `{"areas_m2_or_px2":[50.0],"total":50.0}` |
| `bbox` | bounding box over all points | `python geom.py bbox --polys polys.json` |
| `centroid` | area-weighted centroid of each polygon | `python geom.py centroid --polys polys.json` |
| `maxdim` | largest pairwise vertex distance | `python geom.py maxdim --polys polys.json` |
| `px2m` | one pixel point → canonical metres | `python geom.py px2m --point 620,580 --px-per-m 0.5273 --rotation-deg 0 --origin-px 500,580` |
| `m2px` | inverse of `px2m` | `python geom.py m2px --point 227.58,0 --px-per-m 0.5273 --rotation-deg 0 --origin-px 500,580` |
| `latlon2local` | lat/lon → local equirectangular metres about an anchor | `python geom.py latlon2local --lat -27.9960 --lon 153.4310 --anchor-lat -27.9965 --anchor-lon 153.4305` |
| `local2latlon` | inverse of `latlon2local` | `python geom.py local2latlon --x 49.15 --y 55.66 --anchor-lat -27.9965 --anchor-lon 153.4305` |
| `bearings-latlon` | great-circle bearing of each edge of a `[[lat,lon],...]` polygon | `python geom.py bearings-latlon --polys poly_latlon.json` |
| `bearings-xy` | compass bearing of each edge of an xy polygon, given which compass direction `+y` points (`--north-deg`) | `python geom.py bearings-xy --polys polys.json --north-deg 0` |
| `angle-to-shore` | acute angle (0–90°) between an edge bearing and the shoreline bearing (both treated as undirected lines) | `python geom.py angle-to-shore --bearing-deg 37 --shoreline-bearing-deg 0` → `37.0` |
| `fit-similarity` | least-squares similarity transform (scale + rotation + translation, no reflection) from control pairs, with per-point residuals | `python geom.py fit-similarity --pairs "[[[0,0],[10,10]],[[10,0],[20,10]],[[0,10],[10,20]]]"` → scale 1.0, rotation 0°, translation `[10,10]`, zero residuals |
| `make-canonical` | fill a `shape.json`'s top-level `canonical` block from one `sources[]` entry's `pixel_polygons` + `scale.px_per_m` | see below |
| `selftest` | regression test of the pixel↔metres rotation chain (`px2m`, `m2px`, `make-canonical`) for alongshore directions (1,0), (0,1), (-1,0), (0,-1), a 30° diagonal and a 6.6° tilt, y-down pixels, round trips and +y = offshore; exit code 0 = pass | `python geom.py selftest` → `selftest: 334 checks, 0 failed -> PASS` |

`px2m` / `m2px` `--rotation-deg` is the rotation applied to the pixel offset `(dx, dy)` with the plain
matrix `[[cos,-sin],[sin,cos]]`; to put an alongshore pixel vector `(adx, ady)` on `+x` pass
`-atan2(ady, adx)` in degrees (that is what `make-canonical` does). `0` means the image x axis is
already the alongshore axis. (Sign convention fixed 2026-10-05, see Changelog.)

### `make-canonical` worked example

Given a `shape.json` with one source `img1` whose `pixel_polygons` and
`scale.px_per_m` are already filled in:

```
python geom.py make-canonical --shape shapes/narrowneck-gold-coast/shape.json \
    --source-id img1 --origin-px 500,580 --alongshore-dir-px 1,0 \
    --alongshore-compass-deg 90
```

- `--origin-px` = the pixel you are declaring as the canonical origin (a shoreline point
  nearest the reef centroid).
- `--alongshore-dir-px dx,dy` = a **direction** (not a point) in pixel space that should
  become `+x` (alongshore) in the canonical frame — e.g. `1,0` if the shoreline runs
  left-to-right in the image.
- `--alongshore-compass-deg` (optional) = the real-world compass bearing of that same
  direction, if known; used only to fill `shore_normal_bearing_deg` (`+90°` from
  alongshore) — omit it and the field is left `null`.

This writes `canonical: {frame, derived_from, polygons_m, area_m2, bbox_m:
{alongshore, crossshore}, max_dim_m, distance_offshore_m, shore_normal_bearing_deg}`
straight into the `shape.json` (pass `--no-write` to preview without saving).

Note on pixel convention: image pixel space has `+y` pointing **down**; the canonical
frame's `+y` is **offshore**. `make-canonical` handles this rotation for you — you only
ever supply pixel-space inputs (`origin-px`, `alongshore-dir-px`); it does not matter
which way is physically "offshore" in the photo as long as `alongshore-dir-px` is chosen
so that rotating it 90° clockwise (in pixel space) points offshore, which is the normal
case when alongshore runs left-to-right and the sea is below the shoreline in the image.
If a photo has the sea at the top, flip the sign of `alongshore-dir-px` (point it the
other way along the shore) rather than fighting the rotation.

---

## Test run performed while building this toolkit (per brief; files deleted afterward)

```
python satellite.py fetch --lat -27.9965 --lon 153.4305 --radius-m 300 --zoom 18 --out %TEMP%\narrowneck.png
python overlay.py render --image %TEMP%\narrowneck.png --polys "[[[500,500],[600,500],[620,580],[520,600]]]" --out %TEMP%\narrowneck_overlay.png --grid 100
python overlay.py zoom --image %TEMP%\narrowneck.png --box 450 450 700 650 --scale 3 --grid 25 --out %TEMP%\narrowneck_zoom.png
python overlay.py compare --image %TEMP%\narrowneck.png --polys "[[[500,500],[600,500],[600,580]]]" --polys2 "[[[520,520],[610,520],[610,590]]]" --out %TEMP%\narrowneck_compare.png
python geom.py area --polys "[[[500,500],[600,500],[620,580],[520,600]]]"
python geom.py make-canonical --shape %TEMP%\sample_shape.json --source-id img1 --origin-px 500,580 --alongshore-dir-px 1,0 --alongshore-compass-deg 90
python satellite.py fetch --lat -27.9965 --lon 153.4305 --radius-m 150 --zoom 17 --wayback 22869 --out %TEMP%\narrowneck_wayback.png
python satellite.py wayback-list
python satellite.py pix2ll --geo %TEMP%\narrowneck.png.geo.json --x 569 --y 569
python satellite.py ll2pix --geo %TEMP%\narrowneck.png.geo.json --lat -27.9965 --lon 153.4305
```

Results: fetch succeeded (1138×1138 PNG, 0.5273 m/px at centre, capture date
2025-10-10 found via `identify`); overlay render/zoom/compare all produced valid PNGs;
`geom` area/bbox/centroid/maxdim/px2m/m2px/latlon2local/local2latlon/bearings-xy/
angle-to-shore/fit-similarity/make-canonical all checked by hand or by round-trip
(`px2m`→`m2px`, `ll2pix`→`pix2ll`) and matched to floating-point precision; the Wayback
fetch (release 22869, 2026-03-26) also succeeded and returned a capture date (2025-10-10,
via that release's own metadata layer, field `SRC_DATE2`) that predates the release —
expected, see Caveats.

---

## Caveats

- **Capture date is best-effort.** It comes from Esri's `identify` operation at the
  centre point only — it describes the imagery tile *at that one point*, not necessarily
  every corner of a wide fetch, and some areas (especially the 15 m low-resolution
  fallback layer, or thin coastal slivers) have `DATE = "Null"` for every field, in which
  case the sidecar records `"unknown"`. Always treat it as a strong hint, not a
  certificate — note it in the `shape.json` source's `image_date` alongside a plain
  description of how it was obtained.
- **Wayback capture date can repeat across releases.** A Wayback release date is when
  Esri *published* that snapshot, not necessarily when the underlying source imagery for
  your specific point was captured — if that area wasn't refreshed between two releases,
  both will report the same (older) capture date. This is correct behaviour, not a bug;
  it means you may need to go several releases further back to actually see older
  imagery change.
- **`--radius-m` × `--zoom` tile count is capped at 400 tiles** (`fetch` raises instead of
  silently downloading an enormous mosaic) — reduce the radius or zoom if you hit this.
- **Esri tile servers are public but rate-sensitive**; `_fetch_tile` retries 3× with
  backoff on transient failures, but a very large fetch run repeatedly in a short window
  may still see occasional failures — rerun if so.
- **`overlay.py` uses `arial.ttf` if present, else Pillow's built-in bitmap font** for
  vertex numbers and grid labels; on this Windows machine Arial is normally available, so
  labels render crisp and scalable, but expect a cruder bitmap font on systems without it.
- **`make-canonical` assumes a single rotation + scale + translation is enough** (no
  independent x/y scaling, no shear) — correct for a near-nadir satellite crop, not for a
  heavily oblique photo; for an oblique source use `fit_similarity` / a full
  control-point fit instead and fill `canonical` by hand.
- Nothing in this toolkit talks to the Gemini folder; it only fetches from Esri and
  writes under whatever `--out` path you give it (keep that under
  `07_scale/shapes/<slug>/src/` for anything meant to stay in the project, per
  `_agent_briefs/common.md` rule 3).

---

## Changelog

### 2026-10-05 - `geom.py`: rotation sign fixed in `px_to_m` / `m_to_px` / `make_canonical`

**Bug.** `make_canonical` passed `rotation_deg = -atan2(ady, adx)` to `px_to_m`, and `px_to_m`
then rotated by `-rotation_deg` again, so the pixel offset was rotated by `+phi` instead of
`-phi` (phi = pixel-space angle of the alongshore direction). The result was right only for
alongshore `(1,0)` (and `(-1,0)`, where +180 and -180 coincide); for any other direction the
polygon came out rotated by `2*phi`. Reproduced exactly as reported by two independent tracing
agents: alongshore `(0,1)`, a point 10 px below the origin at 1 px/m gave `x = -10` (should be
+10); alongshore `(0.9934, -0.1157)`, a point 100 px along it gave `(97.3, -23.0)` m instead of
`(100, 0)`. Scale, translation, area, centroid and max dimension were not affected (rotation
does not change them); `polygons_m`, `bbox_m` (alongshore/crossshore), `distance_offshore_m`
and any lat/lon derived from the canonical coordinates were.

**Fix.** `px_to_m` now rotates the offset `(dx, dy)` by `+rotation_deg`; `m_to_px` is its exact
inverse (rotates by `-rotation_deg`). `make_canonical` is unchanged in what it passes
(`-atan2(ady, adx)`), so the chain now nets to `-phi`. Convention kept: `+x` = alongshore in the
direction of `alongshore_dir_px`, `+y` = offshore = alongshore turned 90 deg clockwise on screen
(pixel `+y` is down), so alongshore `(1,0)` with the sea below the shoreline gives `+y` = image
down. No other function uses this rotation (`fit_similarity` has its own, tested below).

**Behaviour change to know about.** `px2m` / `m2px --rotation-deg` flipped sign for non-zero
values. Anyone who called `px2m` / `px_to_m` directly with a non-zero rotation under the old
sign must negate it; calls with `0` are unchanged.

**Test.** `python geom.py selftest` (334 checks, exit code 0/1): the bug cases above;
both pixel axes for alongshore (1,0), (0,1), (-1,0), (0,-1); a 30 deg diagonal, -30, 150,
the 6.6 deg Boscombe tilt and a non-unit vector; px->m->px and m->px->m round trips at several
rotations and scales; `make_canonical` end to end on a synthetic reef in the sea for 5
directions (vertices recovered to 1e-8 m, all reef `y > 0`, land side `y < 0`, area/bbox/
offshore distance/shore-normal bearing, written file == returned dict); and `fit_similarity`
recovering a known 30 deg rotation. The same test run against a copy with the old sign fails
44 of 334 checks, so it does catch the bug.

**WARNING - recompute.** Any `canonical` block (or `px2m` / `m2px` result) produced by
`make-canonical` / `px_to_m` before this fix with an alongshore direction other than exactly
`(1,0)` or `(-1,0)` has a rotated frame (error `2*phi`, e.g. 13 deg for a 6.6 deg tilt) and must
be recomputed: rerun `make-canonical` after this fix, or recompute with an explicit
projection (x = offset . u, y = offset . n). Blocks made with `(1,0)` / `(-1,0)` are fine.
Check each `shapes/<slug>/METHOD.md` for whether the author already replaced `make-canonical`
with an explicit rotation.

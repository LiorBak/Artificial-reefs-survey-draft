# 07_scale — reef footprint scale comparison

## Purpose

Lior asked (2026-09-25) for a scale comparison of the artificial reefs' physical
footprints, in the style of his reference graphic
`03_images/from_lior/goldcoast_pptx/image26.png` (a third-party PowerPoint slide showing
several reefs' plan shapes side by side at one scale) — but covering **all 13** of the
project's verified, built artificial surf reefs, not just the Gold Coast pair shown
there.

Gemini (a second AI, working independently in
`C:\Users\lior\Documents\Gemini\AG\artifical reef`) had already attempted the same
comparison (`02_world_reefs_data\reef_footprints.json`,
`reef_footprint_scale_analysis.md`, `scale_sketch_photo_alignment_audit.md`, and SVG/PNG
figures under `05_web_build\images\scale\`). That folder is **read-only** and was never
written to. Its numbers were treated as **unverified candidates only**: every shape,
dimension, depth and distance in Gemini's files was re-derived independently from our
own primary sources (the dossiers, the verified card JSONs, and the papers/photos those
cite), and only kept if it could be confirmed at the source. Nothing from Gemini's
files entered our footprints without that check — see "Gemini comparison" below for
what agreed and what did not.

Our own build lives entirely under this folder (`07_scale/`) and
`04_build/docs/scale/` (a copy of the provenance `.md` files, kept next to the built
HTML page so it is self-contained). Gemini's outline shapes, dimensions and figures
were not copied, redrawn from, or embedded anywhere in our output — every polygon here
was constructed fresh from our own cited sources.

## Method

### Coordinate conventions

Every footprint uses the same convention (stated again, reef-by-reef, in each
`<slug>.footprint.json`'s own `coords` field, since the specific alongshore direction is
not always independently sourced):

- Units: metres.
- x = alongshore (direction stated per reef; usually an unsourced modelling convention,
  not a surveyed azimuth).
- y = offshore, positive seaward.
- Origin: the shoreline point nearest the reef's centroid.
- The shoreline is the line y = 0.

### How shapes were derived

For each reef, an agent read the reef's dossier (`02_research/reefs/<slug>.md`), its
verified card (`02_research/reefs/<slug>.json`), and — where the dossier cited one — the
original design/monitoring paper, then:

1. Established the reef's topology from text (linear ramp, mound/dome, chevron/V,
   crescent, or "other" for anything not matching those, e.g. Borth's two separate rock
   mounds).
2. Read off, or derived from a plan-view figure/photo (with pixel-to-metre scaling
   against a stated dimension or scale bar), a closed polygon (or set of polygons, e.g.
   Narrowneck's two arms, Borth's two mounds, Mount Maunganui's two arms) in the
   coordinate system above.
3. Computed plan-box length × width, and area by the shoelace formula on the polygon
   (`compile_data.geometry_of`; cross-checked in `check.py` against each footprint's own
   stated `area_m2`, within 1.2% in every case).
4. Recorded crest depth (with datum) and distance offshore (with what it is measured
   from — shoreline, seawall base, centroid, etc.), each with its own reference or
   marked "derived"/"open issue" if no source states it directly.
5. Wrote a full derivation table (quantity / value / method / source / uncertainty),
   the images and figures relied on, the coordinate notes, a point-by-point comparison
   against Gemini's corresponding candidate value, open issues, and a verification log —
   all in `<slug>.md`, machine-readable duplicate in `<slug>.footprint.json`.

Only figures/photos already cited by that reef's dossier (or newly found from an
already-cited paper) were consulted — no new photo or video search was done for this
pass.

### Confidence levels

Each footprint carries its own `confidence` field (low / medium, sometimes qualified by
which specific sub-claim it covers — see individual notes). Nothing here is rated
"high": every one of the 13 reefs' plan shapes is reconstructed from a mix of text
descriptions, one or two plan-view figures, and/or scaled photos, not a surveyed CAD
drawing, so all should be read as **schematic, sourced approximations**, not exact
as-built plans.

## Per-reef summary

| Reef | Shape | L × W (m) | Area (m²) | Crest depth | Distance offshore | Confidence | Sources | vs. Gemini | Dossier / verified write-up |
|---|---|---|---|---|---|---|---|---|---|
| Borth coastal defence reef | other (two adjoining mounds) | 145 × 73 | 3,785 | not established (open issue) | 350 m (shoreline, midpoint of conflicting figures) | low | 7 | agrees on "two-part reef"; sub-shape sketch unconfirmed | [dossier](../02_research/reefs/borth-coastal-defence-reef.md) · [verified](verified/borth-coastal-defence-reef.md) |
| Boscombe Surf Reef | linear ramp | 195.0 × 127.6 | 10,861.6 | 0.5 m above LAT | 220 m (seawall base) | medium | 9 | partial agreement, one figure corrected | [dossier](../02_research/reefs/boscombe-surf-reef.md) · [verified](verified/boscombe-surf-reef.md) |
| Bunbury Airwave | mound (inflatable dome) | 12.0 × 12.0 | 113.1 | 1.0 m below LAT (approx.) | 37.5 m (shoreline, design midpoint) | medium | 6 | partial agreement | [dossier](../02_research/reefs/bunbury-airwave.md) · [verified](verified/bunbury-airwave.md) |
| Burkitts Reef (Bargara) | other (natural rock reef, reshaped) | 120 × 46 | 2,480 | 0 m (exposed at low tide) | 0 m (shoreline) | low | 8 | partial agreement | [dossier](../02_research/reefs/burkitts-reef-bargara.md) · [verified](verified/burkitts-reef-bargara.md) |
| Cables Reef (WA) | V / chevron | 140 × 70 | 2,298.8 | 1.5 m below MSL (approx.) | 275 m (shoreline, approx.) | medium | 7 | partial agreement | [dossier](../02_research/reefs/cables-reef-wa.md) · [verified](verified/cables-reef-wa.md) |
| Kovalam Reef (India) | chevron | 87.9 × 41.6 | 1,083.5 | not found (no source) | 55 m (shoreline, schematic estimate) | low | 7 | disagrees — Gemini's depth/distance figures could not be traced to a real source | [dossier](../02_research/reefs/kovalam-reef-india.md) · [verified](verified/kovalam-reef-india.md) |
| Xala Reef (Mexico, 2026) | other | 160 × 80 | 11,200 | 1.5 m below MSL (design analogy) | 270 m (shoreline, design analogy) | low | 6 | partial agreement | [dossier](../02_research/reefs/mexico-reef-2026-unnamed.md) · [verified](verified/mexico-reef-2026-unnamed.md) |
| Mount Maunganui Reef | chevron | 67.8 × 72.9 | 2,497 | 0.9 m below Chart Datum | 250 m (shoreline, convergent across 5 sources) | medium | 8 | strong agreement | [dossier](../02_research/reefs/mount-maunganui-reef.md) · [verified](verified/mount-maunganui-reef.md) |
| Narrowneck Reef (Gold Coast) | chevron, dual-arm | 600 × 350 | 114,950 | 1.5 m below LAT (design/2012) | 200 m (shoreline, inner edge) | medium | 7 | partial agreement — Gemini's concentric-lobe reading rejected | [dossier](../02_research/reefs/narrowneck-gold-coast.md) · [verified](verified/narrowneck-gold-coast.md) |
| Opunake Surf Reef | other (single-arm wedge) | 20 × 90 | 900 | 1.5 m (datum unknown) | 150 m (shoreline, estimated) | medium | 7 | partial agreement | [dossier](../02_research/reefs/opunake-reef.md) · [verified](verified/opunake-reef.md) |
| Palm Beach Reef (Gold Coast) | mound | 160.0 × 80.0 | 9,677.6 | 1.5 m below MSL (≈0.6 m below LAT) | 270 m (shoreline, 19th Ave) | medium | 11 | partial agreement | [dossier](../02_research/reefs/palm-beach-gold-coast.md) · [verified](verified/palm-beach-gold-coast.md) |
| Pratte's Reef (El Segundo) | V (asymmetric chevron) | 57.8 × 31.2 | 324.1 | 1.83 m below MSL (design minimum) | 95 m (shoreline, approx.) | medium | 8 | partial agreement | [dossier](../02_research/reefs/prattes-reef-el-segundo.md) · [verified](verified/prattes-reef-el-segundo.md) |
| Southern Ocean Surf Reef (Albany) | crescent | 165.0 × 110.0 | 9,720.0 | 1.0 m below AHD (≈MSL) | 140 m (shoreline / landward toe) | medium | 7 | partial agreement | [dossier](../02_research/reefs/southern-ocean-surf-reef-albany.md) · [verified](verified/southern-ocean-surf-reef-albany.md) |

"vs. Gemini" is a qualitative read of each `gemini_comparison` block, not a strict
count of agree/disagree fields (those blocks are free text, not a fixed schema); see
each `<slug>.md`'s own "Gemini comparison" section for the point-by-point detail (which
of Gemini's numbers were checked, confirmed, corrected, or rejected as unsourced).
"Sources" counts each footprint's own `references` array (includes any new S# ids the
footprint pass added on top of the dossier's existing R# ids).

Note: `burkitts-reef-bargara.footprint.json` and
`southern-ocean-surf-reef-albany.footprint.json` were present under `07_scale/reefs/`
(both `status: verified`) but had not yet been copied into `07_scale/verified/` — copied
during this documentation pass (2026-09-25) so `verified/` now holds all 13 reefs'
footprint JSON + provenance `.md`, matching `reefs/`.

## The overlay drawing

`07_scale/drawings/overlay.svg` (and `overlay_centroid.svg`) place all 13 footprints on
one frame at one common scale, drawn from the same 13 footprint JSONs — "by shoreline"
keeps each reef's true drawn distance offshore on one shared shoreline line; "by
centroid" aligns every reef on its centroid instead, with a football-pitch (105 × 68 m)
silhouette for scale. `sheet.svg`/`sheet.png` lay all 13 out in a grid, in the spirit of
Lior's reference `image26.png` layout (used only as a layout idea — no content from that
graphic was copied). Full drawing conventions, sourcing rules for every value shown, and
the reference/media-merging rules applied are in `drawings/README.md`.

## Regenerating the drawings

```
python 07_scale/make_drawings.py
```

Reads `07_scale/reefs/<slug>.footprint.json` for all 13 reefs and writes
`07_scale/drawings/<slug>.svg` + `.png`, plus `overlay.svg`, `overlay_centroid.svg`, and
`sheet.svg`/`.png`. See `drawings/README.md` §2–4 for the exact conventions (scale bar,
panel framing, verdict fill colours, area cross-check tolerance, overlay alignment
modes) that the script implements.

## How the page consumes this

`04_build/src/scale.js` reads the same 13 `07_scale/reefs/<slug>.footprint.json`
files (via `04_build/src/compile_data.py`, which folds them into `data/reefs.json` at
build time) to render the "Scale" tab: one panel per reef at a shared scale (default
1 px = 1 m, zoom ×0.5–×2), a "How we drew this" derivation block per panel (every value
carrying its `[R#]`/`[S#]` source pop-up, wired to the same citation pop-up as the rest
of the page), the all-reefs overlay with alignment/legend/football-pitch toggles, and a
footprint comparison table. `04_build/docs/scale/<slug>.md` is an unchanged copy of each
`07_scale/reefs/<slug>.md`, linked from the comparison table and the reef dialog's
"Scale & footprint" section so the page's provenance links work standalone (see
`04_build/README.md` and `07_scale/drawings/README.md` for the full page-side detail and
round 5/6 QA results).

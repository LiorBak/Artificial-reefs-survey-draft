# Gemini footprint/scale extract (READ-ONLY candidates, unverified)

**Status:** Extraction pass only. Nothing here is verified against a primary source unless explicitly marked. Nothing in this file or its companion `.json` may enter our reef cards/dossiers until a follow-up agent confirms a number at the source URL. Gemini's own files were read but never modified (Gemini folder is read-only per project rules).

**Companion machine-readable file:** `00_gemini_footprints_extract.json`

**Sources read:**
- `C:\Users\lior\Documents\Gemini\AG\artifical reef\02_world_reefs_data\reef_footprints.json` (the CAD/geometry database, 16 structures total incl. Israeli ones we don't use)
- `...\reef_footprint_scale_analysis.md` (the narrative dossier Gemini wrote about how/why it built the database)
- `...\scale_sketch_photo_alignment_audit.md` (Gemini's own internal self-audit of the CAD sketches against photos/papers — very useful, it already flags several of its own errors)
- `...\burkitts-reef-bargara.md` and `...\xala-reef-mexico.md` (Gemini's text dossiers for the two of our 13 reefs that have NO entry in `reef_footprints.json`)
- `...\05_web_build\images\scale\master_overlay.png` + `narrowneck.png`, `opunake.png`, `palm_beach.png` (viewed with the Read tool)
- Lior's `03_images\from_lior\goldcoast_pptx\image26.png` (the original inspiration graphic, third-party, never to be embedded)
- `generate_light_scale_figures.py` / `generate_reef_scale_dossier.py` skimmed for method (not fully executed)

---

## 1. What Gemini built, in its own words

Gemini's brief (quoted inside its own dossier) was: *"this is a good pic for comparissement... it would be crazy good if u can get such for all artificial reef... write notes on how u did it, assumptions and sources."* It responded by building:

1. **`reef_footprints.json`** — a structured "true-to-scale" database for **15 structures** (world ASRs + 3 Israeli structures: Ashkelon, Tel Aviv, Haifa-proposed, plus Netanya added later, 16 total). Every structure gets a normalized local coordinate frame — shoreline at `y=0`, seaward `+y`, alongshore centered at `x=0` — and a hand-digitized polygon (`bounding_polygon`, sometimes broken into named `components` like "Inshore Lobe"/"Offshore Lobe").
2. **Per-reef scale PNGs/SVGs** (`05_web_build/images/scale/<slug>.png`) — one plot per reef with the polygon drawn, a 100m scale bar, a "distance offshore" arrow annotation, a dimensions text box (length/width/area/volume/crest depth/tide), and a status badge (OPERATIONAL / PARTIAL BUILD / FAILED, etc.).
3. **`master_overlay.png`** — all reefs superimposed on one shared axis with a 200m master scale bar, to let you eyeball relative size directly (this is Gemini's answer to Lior's "image26.png" brief).
4. **A self-audit** (`scale_sketch_photo_alignment_audit.md`) in which Gemini checked its own 15 CAD polygons against photos, published papers, and its own dimensions table — and found (and flagged) some of its own inconsistencies, most importantly a dimension-inversion bug on Opunake.

## 2. Image descriptions

### `master_overlay.png` (viewed directly)
A single axes system, `x` from about −220 to +220m (alongshore) and `y` from 0 (shoreline, sandy-yellow band at the bottom) to about 400m (offshore), with dashed horizontal reference lines labeled by approximate seabed depth (−2m through −10m). Eight colored outline polygons are superimposed at true relative scale, one color per group, with a legend ("KEY OVERLAY PROFILES"): Narrowneck (blue, 75k m²) sprawls furthest and highest (reaching y≈380m); Living Breakwaters (green) forms two separate lobes further out; Ashkelon Geotube (a second blue shape, stepped-rectangular, 10k m²) sits mid-field as three stacked bars; Palm Beach/Albany (orange, ~13k m²) is a mid-sized hexagon around y=230–310; Boscombe/Mount (purple, ~5k m²) is a small diamond near y=130–200; the Haifa Delta (teal, 10.5k m²) is a triangular wedge in the same y-range as Palm Beach/Albany; Pratte's/Bunbury (red, <1k m²) is a tiny chevron near y=80–105; and a small grey rectangle pair near y=145–190 (unlabeled in the legend, likely the Ashkelon tiers or Netanya units) frames the middle. A "MASTER 200 METERS SCALE BAR" tick mark sits at bottom right, and a magenta dot near the shoreline (unlabeled) may mark a reference point. The overall visual message matches image26.png's intent: it makes clear at a glance that the historic first-generation reefs (Pratte's, Bunbury) are minuscule compared to Narrowneck or Living Breakwaters, and that the proposed Haifa delta sits comfortably inside the size envelope of the modern, successful rock reefs (Palm Beach/Albany).

### `narrowneck.png`, `opunake.png`, `palm_beach.png` (viewed directly, one at a time)
Each per-reef plot uses the same template: light-blue "water" background down to a sandy band at `y=0`, dashed depth-contour gridlines on the right edge, a title + status badge (top), the reef's polygon filled/hatched in a reef-specific color, a vertical dashed arrow from the shoreline up to the reef centroid labeled "`<N>`m offshore", a black 100m scale bar, and a bottom banner with the reef's name/location/build year. A white info box inside the plot repeats Length/Width/Area/Volume/Crest depth/Tide as plain text. Narrowneck's plot shows the two separate lobes exactly as described (inshore ~y=160–225, offshore ~y=250–380) with a big "OPERATIONAL" badge. Palm Beach's plot shows a single hatched hexagon at y≈230–310 with an "OPERATIONAL" badge, matching its polygon well. Opunake's plot is the interesting one: it shows a small, narrow, TALL purple polygon (roughly 30m wide x 67m tall, running from y≈130 to y≈195) with a "PARTIAL BUILD" badge — but the text box in the same image still reads "Length: 80m | Width: 30m", i.e. the picture's own caption contradicts the shape drawn right next to it (see discrepancy list below).

### `image26.png` (Lior's reference, third-party — described only, never embedded)
A single wide image split into four vertical satellite-photo panels labeled Narrowneck, Cables, Mount Reef, and Pratte's Reef, each showing the same aerial/satellite view of the actual reef traced with a white outline polygon directly over the real water/sand imagery (not an abstract CAD sketch). A shared "200 m" scale bar sits at the bottom of the Cables panel, implying (not explicitly repeating per panel) that all four panels are at the same real-world scale, so a viewer can visually compare Narrowneck's two long parallel ovals against Cables' small arrow-shaped patch, Mount Reef's Y/chevron shape, and Pratte's Reef's tiny dotted-texture triangle. A caption below reads "Size wasn't the only problem... Divers who surveyed the reef saw bags had moved, sunk and got covered by sand. And the black polypropylene bags were falling apart." Style takeaway for our own tab: real aerial imagery at one shared scale bar (not abstract vector shapes) reads as more credible and visceral than Gemini's schematic polygon plots — worth considering for our own version, if underlying real geo-referenced imagery is available for any of our 13 reefs.

## 3. Slug mapping used

| Our slug | Gemini id / slug | Has CAD polygon + scale PNG? |
|---|---|---|
| narrowneck-gold-coast | narrowneck / narrowneck-gold-coast | yes |
| cables-reef-wa | cables / cables-reef-wa | yes |
| mount-maunganui-reef | mount_maunganui / mount-maunganui-reef | yes |
| prattes-reef-el-segundo | prattes_reef / prattes-reef-el-segundo | yes |
| boscombe-surf-reef | boscombe / boscombe-surf-reef | yes |
| opunake-reef | opunake / opunake-reef | yes (dimension bug, see below) |
| kovalam-reef-india | kovalam / kovalam-reef-india | yes |
| borth-coastal-defence-reef | borth / borth-coastal-defence-reef | yes |
| bunbury-airwave | bunbury / bunbury-airwave | yes |
| palm-beach-gold-coast | palm_beach / palm-beach-gold-coast | yes |
| southern-ocean-surf-reef-albany | albany / southern-ocean-surf-reef-albany | yes |
| burkitts-reef-bargara | *(none)* | **no** — not in `reef_footprints.json` at all; only prose dims in Gemini's `.md` |
| mexico-reef-2026-unnamed | xala-reef-mexico | **no** — not in `reef_footprints.json` at all; only prose dims in Gemini's `.md` |

Gemini's database also has 3 Israeli structures (Ashkelon, Tel Aviv, Haifa-proposed) and Netanya, which are not among our 13 tracked reefs and are out of scope here.

## 4. Per-reef data — see `00_gemini_footprints_extract.json` for full structured records

Headline findings (full detail, all cited sources, and full suspicion notes are in the JSON):

- **Best matches (low suspicion):** Southern Ocean Surf Reef / Albany (numbers, including exact tonnage breakdown, match our verified card almost exactly — likely same primary source) and Palm Beach (160x80, 25,000 m³, 1.5m crest all match).
- **Worst / most suspicious:**
  - **Opunake** — Gemini's own audit already caught this: the `dimensions` fields (80m x 30m) are inverted relative to its own polygon (30m x 67m), and the published per-reef PNG's caption still shows the wrong, un-fixed numbers. Our verified card gives a THIRD figure (90m x 20m) from real sources. Do not use any of Gemini's three numbers without independent verification.
  - **Borth** — Gemini says 200m offshore; our own sourced research (from ostensibly the same category of contractor/heritage sources) says 300–400m offshore. This is a large, structurally important divergence (nearly 2x), and Gemini gives no citation pinned to its 200m figure.
  - **Narrowneck** — internally, Gemini's own audit flags its "180m offshore" as ambiguous/incomplete (true only for the inshore lobe; true offshore extent to ~380m), and its gross 75,000 m² area is nearly double its own computed net polygon area (42,650 m²). Externally, our verified card gives two different real-sourced footprints (350x600m or 450x250m) that don't match Gemini's clean 400x220m at all.
  - **Mount Maunganui** and **Boscombe** — both have a >1.5-2x gross-vs-net area gap that Gemini's audit flagged internally but never fixed in the public dossier/JSON; Boscombe's gross area (5,200 m²) is also about half of what our own sourced ~1-hectare figure implies.
  - **Burkitts Reef Bargara** and **Mexico/Xala** — Gemini has **no CAD entry at all** for either. Its prose "80m x 40m" (Burkitts) and "~140m x ~75m" (Xala) dimension claims carry no source citation, and in both cases our own verified cards explicitly say the dimension was **"not found"** after a full sourcing pass. These two numbers look like Gemini's own estimates/guesses presented without a hedge (Burkitts) or with only a soft "~" hedge (Xala) — treat both as unverified and do not import them.
- **Reasonable but uncited:** Cables, Kovalam, Pratte's, Bunbury — dimensions are broadly plausible and in some cases (Kovalam's volume, Bunbury's diameter/height) match our own sourced numbers well, but Gemini's 3 "sources" per reef are general reports/papers, never a specific citation for the specific length/width/area figure, so the shape itself should still be treated as Gemini's own reconstruction rather than a verified drawing.

## 5. How Gemini says it derived every shape (methodology, per its own dossier)

From `reef_footprint_scale_analysis.md` §1.2: dimensions were compiled from "peer-reviewed literature, as-built hydrographic surveys, municipal engineering records, and satellite imagery," with alongshore length/cross-shore width/offshore distance/footprint area/volume/crest depth defined explicitly, and every reef's polygon hand-digitized within the shared normalized coordinate frame described above. In practice, per its own self-audit, at least 5 of the 15 CAD sketches have an internal gross-vs-net area inconsistency, 1 has a flat-out dimension-axis inversion bug, and none of the individual length/width/area numbers in `reef_footprints.json` carry an inline citation tying that specific figure to a specific page/quote in the listed sources — the "sources" list is per-reef, not per-number.

## 6. Recommendation for next steps

Per the harness rules, nothing here should enter our cards/dossiers or the site's new comparison tab until a verification agent:
1. Re-checks each suspicious length/width/area/offshore-distance figure against the actual cited engineering source (or an equivalent one we can access), the same way our own reef cards do with `[R#]` references.
2. Decides, reef by reef, whether to use OUR own sourced figures (even if less "clean"/consistent) instead of Gemini's, especially for Opunake, Borth, Narrowneck, Mount Maunganui, Boscombe, Burkitts, and Mexico/Xala.
3. Builds our own scale-comparison graphic/tab (a fresh file, never Gemini's), citing an `[R#]`-style reference or an explicit "estimated from `<image URL>`, method ..." note for every number, per the project rule.

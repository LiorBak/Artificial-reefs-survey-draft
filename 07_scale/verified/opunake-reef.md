# Opunake Surf Reef — footprint research and provenance

Companion file: `opunake-reef.footprint.json` (status: `verified`, verified_on: `2026-09-25`)

## Summary

- **Shape:** No published plan-view drawing was found or was accessible for this reef. We represent it as a schematic single-arm wedge (isosceles triangle) — base at the shoreward end, apex pointing offshore — by direct analogy to the one ASR reef of the same era whose shape a primary source *does* describe (Mount Maunganui: "apex... point[ing] seaward and the structure thicken[ing] towards the base" [R3]). The real Opunake reef produced only a single "right-hand wave" (one peel direction), unlike Mount Maunganui's two-directional wave, so it was almost certainly an *asymmetric* wedge in reality — but no source gives which flank was longer or the arm's compass bearing, so we did not invent that asymmetry.
- **L × W:** 90 m (offshore-projecting axis) × 20 m (alongshore base width) — stated near-verbatim in two independent, accessible secondary sources (raisedwaterresearch.com and surfertoday.com).
- **Area:** 900 m² for the schematic triangle (0.5 × 20 × 90); could be as high as 1,800 m² if the "90 × 20" figure is read as a full rectangular envelope rather than a tapered wedge — no source specifies which, so both are given.
- **Crest depth:** ~1.5 m below an unstated datum — **not published anywhere we could access**; a rough, explicitly low-confidence estimate (±1.0 m).
- **Distance offshore:** ~150 m — **also not published**; a rough, explicitly low-confidence estimate (±75 m), reached independently of Gemini's coincidentally identical figure.
- **Confidence:** medium overall. The two headline dimensions (90 m, 20 m) are solidly sourced; the shape, position, crest depth and distance offshore are schematic/estimated and flagged accordingly.

## Sources and what each gave

- **[R2] Raised Water Research, "Opunake."** Re-fetched in full on 2026-09-25 (curl with a browser user-agent; WebFetch was not needed here, it loaded fine). Gave the exact sentence used for the footprint: *"The bags would cover an area around 90m long and 20m wide."* Also re-confirms the whole failure narrative already in our card (27 bags, $1.7m+ spend, Neil Walker/Nick Behunin/Chris Jensen quotes) — no changes needed to the card from this pass.
- **[R4] SurferToday, "The history of artificial surf reefs."** Re-fetched in full on 2026-09-25. Gives the near-identical sentence: *"The bags would cover an area around 90 meters long and 20 meters wide."* Independently corroborates R2's figure (the two pages clearly share a common underlying text, but the 90×20 figure is stated plainly in both accessible copies).
- **[R3] New Zealand Geographic, "Artificial surf reefs — coming to a beach near you."** This page WebFetch-403'd, but a direct curl (browser user-agent) returned the full 9.3 kB article text with no paywall gate — the article is a 2006 pre-construction piece by Andrew Moores and does NOT actually contain the 90×20 footprint figure anywhere; it is text-only (no figures/diagrams at all in the fetched HTML). It DOES give the useful analogous detail used for our shape assumption: Mount Maunganui's reef "is shaped like a cross between a heavy-limbed V and a delta wing. The apex of the V points seaward and the structure thickens towards the base... will measure 75 m from apex to base and almost 100 m across the base," anchored "250 m off the beach in 4.5 m of water." For Opunake specifically it gives only cost (~$1.3M), wave height (1.8–2.5 m) and ride length (100 m) — no footprint, no depth, no offshore distance. **Correction to the card:** the card cites the 90×20 footprint as [R2][R3][R4]; R3's accessible text does not support that citation — it should read [R2][R4] only (flagged as an open issue below, not corrected in the card itself per this task's scope).
- **[R7] Surf-Forecast.com, Opunake Beach Surf Guide.** Reused from the card (not re-fetched this pass) for the ~2.5 m local tidal range, used only as an input to the crest-depth estimate.
- **[R9] ResearchGate, "Studies for Resource Consent: Opunake Surfing Reef."** Already flagged in the card as blocked. Re-attempted this pass via both WebFetch and a direct curl with a browser user-agent; both returned HTTP 403 / Cloudflare challenge pages. This is the single most likely place the real design dimensions, crest depth and offshore distance were originally published (it is a 2004 ASR Ltd technical/resource-consent study), but it remains inaccessible.
- **Gemini's cited sources** ("Mead & Black 2007 Design Dossier," "Taranaki Regional Council Environmental Monitoring Records 2010") — searched for and not found anywhere accessible to us: not on ResearchGate, not turned up by any of our fetches, and not present in either project's folders. They could not be confirmed at the source, so nothing cited to them was adopted, per this project's rule that "nothing from Gemini enters our files unless an agent confirmed it at the source."

## Images/figures relied on

All three are images already in the card's `images` list; none are new searches. Each was downloaded to the session scratchpad, viewed, and then left there for cleanup (not copied into the project).

| URL | What it shows | What was measured/read off it | Method |
|---|---|---|---|
| `raisedwaterresearch.com/.../Opunake-Location.jpg` | Rocky cove shoreline curving toward a distant headland; a line of buoys/floats strung roughly parallel to the beach, close inshore | General cove shape/orientation only (curving shoreline, headland visible) | Visual inspection; **no scale bar or reference length present**, so nothing quantitative was measured. The buoy line is close to shore and parallel to it, which argues against it marking an offshore reef structure — consistent with the card's existing caveat that this is "not confirmed as a reef marker specifically." |
| `raisedwaterresearch.com/.../Opunake-Reef-Flat.jpg` | View across the bay from the rocky shore toward the surf break | Nothing usable — no structure or scale reference visible | Visual inspection only |
| `raisedwaterresearch.com/.../Opunake-Artist-Rendition.jpg` | Multiple natural-looking swell lines breaking along the beach, several surfers riding different peaks | Nothing usable — no single reef-focused wave distinguishable, no scale reference | Visual inspection only |

We did not attempt Google Maps satellite imagery for this pass: the reef is a submerged, largely-collapsed structure with no source suggesting it is visible from above, and the task scope directs re-checking already-verified images rather than opening new ones (the Google Maps link in the card's images list is a live-tile link, not a fixed image, and inspecting it would not have added a measurable scale reference for a submerged, degraded structure).

## Derivation table

| Quantity | Value | Method | Source | Uncertainty |
|---|---|---|---|---|
| Reef length (offshore-projecting axis) | 90 m | Stated in text | [R2] "The bags would cover an area around 90m long and 20m wide." | As stated; axis assignment (offshore vs. alongshore) is our inference — see Polygon construction |
| Reef length, corroborating | 90 m | Stated in text | [R4] "...around 90 meters long and 20 meters wide." | As stated |
| Reef width (base, alongshore) | 20 m | Stated in text | [R2]/[R4], same sentences | As stated |
| Net footprint area (schematic triangle) | 900 m² | Estimated: 0.5 × 20 m × 90 m | [S1] derived, not sourced | Could be up to 1,800 m² if read as a full rectangle instead of a wedge |
| Crest depth | 1.5 m | Estimated — no published figure found; inferred from the need to trip a published 1.8–2.5 m design wave [R2][R3][R4] while remaining submerged across a ~2.5 m local tidal range [R7] | [S1] | ±1.0 m, low confidence. Verification note: R7 is a live tide table; re-read on 2026-09-25 it showed an instantaneous 2.75 m high/low difference, not a fixed published range — within the same order of magnitude, already absorbed by the ±1.0 m error bar |
| Distance offshore | 150 m | Estimated — no published figure found; loosely scaled down from the only ASR reef offshore-distance we could verify directly in a primary source, Mount Maunganui at 250 m / 4.5 m depth [R3], for Opunake's smaller design wave and sheltered cove | [S1] | ±75 m, low confidence. Coincides with Gemini's unverified 150 m but was derived independently |

## Polygon construction

Coordinate frame: origin at the shoreline point nearest the reef centroid; **x** = alongshore (arbitrary positive direction — no compass bearing is published for this reef in any accessible source); **y** = offshore, positive seaward; shoreline approximated as y = 0.

The reef is drawn as a simple isosceles triangle:
- Base corners at `(-10, 110)` and `(10, 110)` — a 20 m wide base, placed at y = 110 m offshore (i.e., using our 150 m centroid estimate minus half the 90 m length, so the whole 90 m run sits symmetrically around that estimated centroid).
- Apex at `(0, 200)` — 90 m further offshore than the base, matching the published "90 m long" figure exactly by construction.
- Closed back to `(-10, 110)`.

This gives a bounding box of 20 m (alongshore) × 90 m (offshore) — matching both published dimensions exactly — and an area of 900 m² (validated with `shapely`: valid, simple/non-self-intersecting, `bounds = (-10, 110, 10, 200)`, `area = 900.0`).

**What is NOT sourced about this construction:** (1) the 150 m centroid distance offshore, (2) the choice of a *symmetric* triangle rather than the asymmetric wedge the reef almost certainly was (given it produced only a right-hand wave), and (3) the compass bearing of the x/y axes. All three are flagged in `orientation_notes` and `open_issues` in the JSON.

## Gemini comparison

Gemini's live `reef_footprints.json` entry for `opunake` (re-read directly on 2026-09-25) states `alongshore_length_m: 30.0`, `cross_shore_width_m: 67.0`, `footprint_area_m2: 1365.0`, `crest_depth_m: 1.4`, `distance_offshore_m: 150`, shape typology "Single-Arm Triangular Wedge (Incomplete V)," citing "Mead, S. & Black, K. (2007). Opunake Artificial Reef Design Dossier." and "Taranaki Regional Council Environmental Monitoring Records (2010)."

**Important correction to the task brief's framing:** the brief (quoting Gemini's own `scale_sketch_photo_alignment_audit.md`) describes an unresolved "ACTION REQUIRED" contradiction — a metadata table allegedly still reading `80m × 30m` against a `30m × 67m` polygon, with the audit saying the fix "was never applied." We read the live `reef_footprints.json` directly this pass and found `alongshore_length_m: 30.0` / `cross_shore_width_m: 67.0` already in place — i.e., matching the polygon, not 80×30. The specific inversion the audit and task brief describe does not exist in the file as of 2026-09-25 (it appears to have been corrected after the audit doc was written, without the audit doc itself being updated). This is a factual correction to the premise, not a defense of Gemini's numbers — see below.

| Quantity | Gemini | Ours | Why ours |
|---|---|---|---|
| Alongshore length × cross-shore width | 30 m × 67 m (current file) | 90 m × 20 m | Stated near-verbatim in two independent accessible sources (R2, R4: "cover an area around 90m long and 20m wide"). Gemini's 30×67 has no matching quote anywhere we could find; its cited sources are not in our reference list and are not accessible to us (not on ResearchGate, not found by any fetch); Gemini's own audit doc says the polygon was "hand-digitized" against a photo and Gemini's own text dossier, not a primary plan drawing. Not adopted. |
| Area | 1,365 m² | 900 m² (schematic triangle) / up to 1,800 m² (rectangular reading) | Follows from the dimensions dispute above; 1,365 m² is simply the shoelace area of Gemini's own unsourced 7-vertex polygon. |
| Crest depth | 1.4 m | 1.5 m ± 1.0 m (estimate) | Both are estimates in effect; ours is independently derived and explicitly labelled low-confidence rather than presented as sourced fact. The values happen to be close. |
| Distance offshore | 150 m | 150 m ± 75 m (estimate) | Same situation — independently derived, coincidentally identical central value, both low-confidence. |
| Shape narrative | "Cove headland alignment; arm projects cross-shore along northern rocky headland" | Schematic wedge, bearing unknown | No accessible source (including Gemini's own two citations, which we could not locate) actually describes a headland-hugging arm or gives a bearing for Opunake. This reads as an unsourced elaboration built to explain the 30×67 vs. 80×30 discrepancy internally, not an independently documented fact. |

## Open issues

1. No primary source with an actual plan-view drawing, survey or CAD figure for the Opunake reef was found or accessible. NZ Geographic (R3)'s full article text contains no figures at all and does not contain the 90×20 dimension; ResearchGate (R9), the most likely original source (a 2004 ASR/council resource-consent study), is Cloudflare-blocked on both WebFetch and direct curl.
2. The card cites the 90×20 footprint as [R2][R3][R4]; only R2 and R4 actually contain that figure in their accessible text. Worth a small citation fix on the card/dossier in a future pass (not made here, since this task's scope is the footprint file, not card edits).
3. Crest depth and distance offshore are not published anywhere accessible for Opunake specifically; both are explicitly low-confidence estimates in the JSON, kept clearly separate from the two solidly-sourced dimensions.
4. The real reef's left/right asymmetry (single right-hand wave) is not captured by the symmetric schematic triangle, because no source gives the arm's actual skew or compass bearing.
5. Gemini's two cited sources for its dimensions could not be located or accessed anywhere by us, so its 30×67/1,365 m² figures could not be confirmed at the source and are not used, per project rule.
6. **[Fixed this pass]** The JSON's `materials` field cited [R2][R4] for a "non-woven, polyester/polyester-polypropylene fabric" description that is not actually present in either source's text — it was misattributed from R3's description of a *different* reef (Mount Maunganui). Corrected in the JSON; see Verification section below.

## Verification 2026-09-25

Adversarial re-check of every row of the Derivation table, the polygon geometry, the shape classification, and the Gemini comparison, by independently re-fetching each cited source (curl with a browser user-agent where WebFetch was blocked or to cross-check WebFetch's summary) and recomputing the polygon math from scratch. Full per-item verdicts and evidence are in `opunake-reef.footprint.json`'s `verification` array; summary:

- **R2 (raisedwaterresearch.com), "90m long and 20m wide"** — **confirmed.** Re-fetched via curl (HTTP 200); exact sentence present verbatim. Also independently reconfirms "designed to create a right-hand wave on the north side of the cove" and "all 27 geotextile bags were in place" (2009).
- **R4 (surfertoday.com), "90 meters long and 20 meters wide"** — **confirmed.** WebFetch 403'd this pass (as it apparently didn't for the original researcher pass — site behaviour may vary by request); re-fetched successfully via curl instead and parsed the stripped text directly. The exact sentence is present in the Opunake paragraph, alongside the same 1.8–2.5 m / 100 m figures used elsewhere in this file.
- **R3 (nzgeo.com) does NOT contain the 90×20 figure** — **confirmed.** Independently re-fetched the full article (58 kB stripped text); zero matches for "90 m"/"90m" anywhere in the piece. The Mount Maunganui shape-analogy quote and the 250 m/4.5 m offshore-distance/depth figure used in this file's derivation are both confirmed verbatim. Also newly noted: the article states Opunake was planned to have *two* reefs (north + south) — consistent with, and supporting, this file's "(North Reef)" naming.
- **Polygon bbox/area** — **confirmed** by independent recomputation (shoelace formula, plain Python, no external libraries): bbox exactly 20 m × 90 m, area exactly 900.0 m², matching the file's stated values to the reported precision.
- **Shape classification** — **confirmed as the best available option, not a measurement.** No plan-view drawing, aerial photo or CAD figure for Opunake exists or is accessible anywhere we could find; the three card images were re-inspected and, again, show no scale reference or reef structure. Using the verbatim-confirmed Mount Maunganui analogy, while explicitly not inventing the asymmetric skew that a single right-hand wave implies, remains the most defensible choice.
- **R9 (ResearchGate)** — **confirmed still blocked** (independently re-attempted via curl, HTTP 403/Cloudflare).
- **R7 (surf-forecast.com) tidal range** — **confirmed with a caveat.** The live page's next-high/next-low reading gave 2.75 m at time of this fetch, not a fixed published "tidal range" statistic; close enough to the ~2.5 m figure used (already inside a ±1.0 m crest-depth error bar) that no number was changed, but the derivation table entry now notes the imprecision.
- **Materials field fabric citation** — **unsupported, corrected.** "Non-woven, polyester/polyester-polypropylene fabric [R2][R4]" does not appear in either source; that description belongs to R3's account of Mount Maunganui's bags. Fixed in the JSON to drop the false citation and state plainly that Opunake's own bag fabric is not published anywhere accessible to us.
- **Gemini's live `reef_footprints.json` values** (30 m × 67 m, 1,365 m², 1.4 m crest, 150 m offshore, "Single-Arm Triangular Wedge (Incomplete V)", two named-but-inaccessible sources) — **confirmed as accurately transcribed** by a direct read of the live file. Independently recomputed the shoelace area of Gemini's own 7-vertex polygon: 1,365.0 m² exactly, and its bbox: 30 m × 67 m exactly — both match Gemini's own stated numbers exactly, confirming this file's point that Gemini's figures are self-consistent with its own polygon rather than checkable against any primary source.
- **The "stale audit premise" correction** — **confirmed.** Gemini's own `scale_sketch_photo_alignment_audit.md` (row 6 and its detailed Opunake section) does state an unresolved "ACTION REQUIRED" 80×30-vs-30×67 contradiction and recommends the exact 30/67 fix. The live `reef_footprints.json`, read the same day, already contains 30.0/67.0. This confirms the audit document itself is stale on this one point — a correction to the task brief's premise, not a defense of Gemini's underlying (still unsourced) 30×67 figure.
- **No number in the Derivation table lacks a source or an explicit estimation method** — **confirmed.** Every row cites either a re-fetched, quoted secondary source or is explicitly labeled "estimated"/"derived, not sourced" (source_ref `S1`) with a stated uncertainty range.
- **Overall confidence** — kept at **medium**, unchanged. The two headline dimensions are now doubly independently reconfirmed via fresh fetches of two separate sources; shape, crest depth, distance offshore and exact area remain explicitly schematic/estimated, as already flagged.

No numbers were invented and none were found to require lowering; the one substantive correction made was removing the unsupported "polyester/non-woven" fabric citation from the JSON's `materials` field. JSON validated with `json.load()` after edits.

# Paper plan: "Artificial surf reefs: a review of built projects, surf quality, sediment transport and durability, with implications for the Israeli coast"

Author: Lior Bakalo. Course: coastal engineering (instructor feedback below). Deadline: about one day from 2026-10-15.
Format (Lior, 2026-10-15): English, academic style, ~15-20 pages main text + appendices, delivered as PDF.
No public web page now (Lior, 2026-10-15): the GitHub Pages version is postponed; nothing third-party is published.

## Instructor's requirements (translated from Hebrew)
1. "A review of artificial reefs is suitable. But try to include insights (computational if possible, otherwise qualitative,
   following the theory we learned in the course) on the effect of the reef on the waves in the context of surfing quality, for
   different (surfer) levels. There are quite a few papers on this."
2. "It is also important to include in the review the effect on sand transport and the combination of creating a surf reef with
   coastal (beach) stabilisation."

## Lior's own insights (author's observations; translated, to be argued with evidence in the paper)
- (a) Reefs need a lot of volume. Small reefs such as Pratte's Reef simply do not work.
- (b) Little measurable effect on sand transport. In Australia (Gold Coast) they claim it works, but the shoreline itself shows no
  change, only the bed far offshore / at depth, with the claim that the reef protects the shoreline in large storms. This is hard
  to attribute to the reef because sand is nourished there continuously. -> evaluate the sediment question at sites WITHOUT
  nourishment.
- (c) Soft structures (geotextile tubes/containers, the Airwave) do not survive in the breaking zone for long; including the
  geotextile tubes on the Israeli Mediterranean coast (Lior said Netanya, ~winter 2019, a year after deployment; his notes
  describe Ashkelon: 15 of 48 tubes destroyed before completion) -> verify which. But geotubes do support marine life and are the
  cheapest structure.
- (d) The wave made by artificial reefs is usually active on few days, if at all. Australia does it well, but even there the reef
  needs very specific swell conditions. In England (Boscombe, to be confirmed) the structure rose too steeply and the wave was
  surfable only for bodyboarders (too hollow; the reef got very shallow very fast).
- (e) Mechanism of tube failure (Drimer, 2026 paper to be found): most of the wave power acts at the break; it lifts the
  geotextile tube up and then down, which is why most of them tear.
- (f) Depth gap and length: if the seabed goes from 5 m to 2 m that is a big gap, but most waves do not break at 2 m, so a long,
  gradual ramp can still give a good wave; a sudden rise to 1-1.5 m gives a too-hollow wave. Quantify with wave height (breaker
  index, Iribarren number, Mead & Black breaking intensity).
- (g) Surfer level: beginners need a very slowly breaking (spilling) wave, which reefs do not create; once standing, difficulty
  depends on the peel angle (Hutt, Black & Mead 2001). Lior thinks ~30 deg is for good surfers making high-level turns; smaller
  angles are faster and harder (check the real table).
- (h) Israel: (A) tide range is much smaller, so a reef wave would be more consistent through the day and the range of wave power
  hitting the reef is smaller (less damage risk) - but the Netanya/Ashkelon tubes still tore, so maybe the geotextile was simply not
  good; a materials section is needed (geotextile always gets damaged unless very deep?). (B) Strong sand transport, especially at
  Haifa: about 1 m seasonal bed-level change, so a reef can sink into the sand over time - but also an opportunity to trap sand in
  the high-sand seasons (usually October and May), cheaper than bringing new sand (e.g. cover the trapped sand with a geotextile
  sheet and build on top).

## Structure (main text ~15-20 pages)
1. Abstract.
2. Introduction: purpose of surf reefs (surf amenity, coastal protection, ecology), scope, research questions, the Haifa motivation.
3. Methods (general; per-reef detail in Appendix A): source collection and standard (every number cited, confidence), shape
   tracing and georeferencing, 3D reconstruction (seabed + reef + local tides), how depth gaps and ramp lengths were measured,
   the computational approach (section 5), limitations.
4. Survey of built reefs: master table (all reefs incl. those in Bar & Drimer 2023), short narrative per group (Australia, NZ,
   UK, USA, India, Mexico, others / geotube breakwaters), Figure 1 (2D plan shapes, see below) and Figure 2 (depth profiles).
5. Reef effect on waves and surf quality (computational): wave transformation over the reef (shoaling, refraction/focusing,
   breaking criterion H/h), breaker type (Iribarren number from the measured reef-face slope and local Hs/Tp), breaking intensity
   (Mead & Black orthogonal gradient), peel angle and surfer skill (Hutt et al. 2001), surfable window vs tide (crest depth vs
   tide range), volume vs outcome (insight a). Figure 3 (wave/surfer/seabed sketch to scale), Figure 4 (depth gap and ramp length
   for all reefs, with breaker-type zones), Figure 5 (peel angle vs skill), Table (computed per reef).
6. Sediment transport and coastal stabilisation: salients and shoreline response theory (Ranasinghe & Turner 2006; Black & Andrews
   2001), evidence per reef, nourishment confound in Australia, burial/scour, combining surf reefs with stabilisation.
7. Materials and durability: geotextile containers, inflatable/sand-filled (Airwave), rock, concrete/ECOncrete; wave forces in the
   breaking zone (Drimer 2026 model applied to our reefs); ecology benefit of geotubes; cost.
8. Implications for Israel / Haifa: small tide (consistency, smaller load range), wave climate, sand mobility (~1 m seasonal),
   burial risk, sand-trapping opportunity, material choice, recommended next steps.
9. Discussion (insights a-h tested against the evidence) and conclusions.
10. References (all verified).
Appendices: A) per-reef methods and sources (condensed from 07_scale METHODS_3D/HANDOFF); B) 3D reconstructions (images);
C) full data table; D) reefs of Bar & Drimer (2023) not built as surf reefs.

## Figures (specs)
- F1 2D plan shapes: all reefs with a known shape, same metric scale, spaced left-to-right (some overlap fine), vertical axis =
  distance from shoreline (offshore up or down, consistent), shoreline drawn; names and year; hidden/unknown shapes omitted.
- F2 directly below F1, aligned per reef: cross-shore depth profile (seabed and reef, m below MSL, MSL and tide range band),
  blank where unknown.
- F3 wave sketch to scale: seabed, reef ramp, breaking wave of typical Hs, a 1.8 m standing surfer for scale, depth labels.
- F4 all reefs: depth gap (toe - crest) vs ramp length (or mean slope), coloured by outcome, with Iribarren/breaker-type bands for
  a typical swell.
- F5 peel angle vs skill level (Hutt et al. 2001), our reefs' arm angles marked where known.
- F6 volume vs outcome (insight a).
- Appendix B: 3D previews (07_scale/shapes/<slug>/3d/preview_*.png).

## Files
- 08_paper/data/ (reefs.json, reefs_table.csv, profiles/), 08_paper/lit/ (LITERATURE.md, references.json),
  08_paper/notes/ (bar_drimer_2023_coverage.md, drimer_2026_forces.md, israel.md, sediment.md, materials.md, surf_outcomes.md),
  08_paper/analysis/ (scripts + results), 08_paper/figures/, 08_paper/sections/ (markdown per section), 08_paper/build/ (PDF).

## Decisions 2026-10-15 (Lior)
- Tokens are short: NO separate revision/review round. Keep: reference verification (Haiku) and the PDF build.
- A Haiku agent checks whether each insight (a)-(h) is already in the cited literature: 08_paper/notes/insights_in_literature.md.
  The writer must cite it ("consistent with X") or say it is a new observation of this review.

## Workflow scripts (to resume in a new session)
- Round 2: `_agent_briefs/workflows/paper_round2.js`; rounds 3-4: `_agent_briefs/workflows/paper_round3_4.js` (run with the Workflow tool).
- Status 2026-10-16 04:40 UTC: round 1 done (data, profiles, lit, notes, seabed analysis, analysis scripts+results, insights check); round 2 running.

- 2026-10-19 (Lior): length is fine as is (~26 pages main text); no cuts.

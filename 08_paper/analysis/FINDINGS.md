# FINDINGS: the strongest quantitative results, tested against Lior's insights (a)-(h)

> Update 2026-10-20: the recommended Haifa crest is now 1.0 to 1.2 m below MSL (was 0.6 to 1.0 m), about 14,000 to 20,000 m3 per 100 m; basis: model breaking depths (gamma 0.78) plus at least 0.5 m of water over the crest at the 1-year low level (-0.38 m MSL). Field breaking depths are indicative only. See 08_paper/sections/07_israel.md section 7.5. Older statements below are superseded.

Status 2026-10-16; updated 2026-10-19 for the per-reef surf cuts of Albany, Cables and Borth (`RECUT_NOTES.md`). Numbers, methods and sources: `RESULTS.md` (section given as s#). Literature verdicts on each insight: `08_paper/notes/insights_in_literature.md` (the writer cites it: "consistent with X" or "new observation of this review"). Sample sizes are small (8-12 reefs) and outcomes are ordinal judgements, so every statistic is descriptive. Verdicts: SUPPORTED, PARTLY, NOT SUPPORTED, or TOO THIN (data cannot decide).

| # | Finding (one line) | Insight | Verdict |
|---|---|---|---|
| 1 | Reefs that work are big: volume ranks with outcome (rho 0.72-0.93) | a | SUPPORTED (descriptive) |
| 2 | Ramp gradient, not crest depth, sets breaker type; steep faces collapse | f, d | SUPPORTED (direction); thresholds DERIVED |
| 3 | Reefs shape surfable waves only in a narrow height window | d | SUPPORTED; Boscombe "bodyboard only" PARTLY |
| 4 | Peel angles at the break serve advanced surfers, never learners | g | SUPPORTED |
| 5 | Salient predictors overestimate the observed shoreline response 15-50x | b | SUPPORTED where testable; Gold Coast TOO THIN |
| 6 | Soft reefs fail, rock reefs survive (6/7 vs 0/4); uplift is plausible only for small or sealed tubes | c, e | c SUPPORTED; e PARTLY |
| 7 | Israel's 0.4 m tide makes the wave consistent but not more frequent, and does not reduce storm loads | h-A | PARTLY |
| 8 | Haifa sand mobility threatens burial; trapping sand behind a surf reef is negligible | h-B | burial SUPPORTED (input unsourced); sand trap NOT SUPPORTED |

## 1. Reefs that work are big (a) - SUPPORTED, descriptive
- **Correlation.** Model volume vs outcome (8 modelled reefs): Spearman rho 0.93, permutation p 0.005 (s6). Stated volume of all 10 built reefs: rho 0.72, p_perm 0.021.
- **Groups.** All "does not work" reefs are 4,900 m3 or less (Bunbury 105, Pratte's 1,350, Opunake 4,900). Both built reefs rated "works" are 25,000 m3 or more (Palm Beach 25,000, Albany 34,000).
- **Mechanism (DERIVED).** Volume buys ramp length (and relief). Depth gap rho 0.93 (p_perm 0.005), ramp length 0.93 (0.005), mean ramp slope 0.77 (0.039), crest depth 0.39 (0.36, not significant). (Before the 2026-10-19 surf cuts: ramp length 0.85 (0.015), mean slope 0.62 (0.15), crest depth 0.00.) A 1:16-1:20 ramp on a 4-5 m bed needs 15,000-25,000 m3 per 100 m (s10).
- **Caveats.**
  - n is 8-10.
  - Size is collinear with material (the large reefs are recent rock reefs) and with budget.
  - Burkitts (300 m3 moved on a natural reef) "works": including it gives rho 0.43, p 0.21. Volume matters when the reef must build the whole relief.
  - Narrowneck's stated (70,000 m3) and modelled (13,500 m3) volumes differ 5x.
- **Literature.** Already in the literature (insights_in_literature.md s2). The threshold (about 5,000 m3 fails, 25,000 m3 or more works) is new to this review.

## 2. Ramp gradient, not crest depth, sets the breaker type (f, d) - SUPPORTED in direction
- **Gradual ramp.** Palm Beach (89 m ramp, 1:17): median breaker index xi_b 0.49 (plunging), Y 2.01 ("very high"), 0% collapsing (s3).
- **Abrupt rise.**
  - Bunbury (1:2.7): Y below 1.6 in 100% of cases, median xi_b 2.97.
  - Boscombe (1:3): 100%, xi_b 2.00.
  - Mt Maunganui: 91%.
- **Across reefs.** Median xi_b ranks with outcome at rho -0.77 (p_perm 0.039; was -0.69, 0.078 before the surf cuts); the mean ramp slope at 0.77 (0.039); crest depth does not (rho 0.39, p_perm 0.36). Albany, which works, now sits with Palm Beach on a long gentle ramp (99 m, 1:19.8, Y 2.11 on the face, 0% surging); on its former take-off line (22 m, 1:4) it looked like a collapsing reef. The same 2-4 m depth gap gives a surfable wave over a long ramp and a collapsing wave over an abrupt rise.
- **Haifa thresholds (T 6-8 s, s10).**
  - 1:8: collapsing in 67-100% of cases.
  - 1:12-1:16: Y 1.6-1.9 ("extreme", expert).
  - 1:20: advanced and spilling mix.
  - 1:30: spilling.
- **Wave period.** Short periods soften the same reef: surging share 0.21 at 6 s vs 0.41 at 10-12 s.
- **Caveats.**
  - The Mead & Black fit covers 1:9 to 1:40. 98-99% of Boscombe and Bunbury cases are extrapolated.
  - Scatter is large (R^2 0.71; 0.27 in Robertson et al. 2014).
  - Boscombe's 2011 surveyed surface (1:12) still gives Y below 1.6 in 85% of cases.
  - Geometry is idealised for 6 of 9 reefs.
  - The LITERATURE.md D-5/D-6 conflict is resolved: X is read as 1:X (Mead 2000, p.115).
- **Literature.** Partly in the literature; the quantification is new.

## 3. Narrow surfable wave-height window (d) - SUPPORTED; Boscombe detail PARTLY
- **Height window.** At MSL a wave needs H0 of 0.3-1.3 m to break on the reef. Above H0 1.6-5.2 m it breaks seaward of the reef (s2). Over the full grid, 34-84% of cases break on the reef.
- **Surfable time fraction, given the swell (s5).** Palm Beach 0.70, Albany 0.62, Cables 0.55, Borth 0.19, Mt Maunganui 0.16, Narrowneck 0.15, Pratte's 0.04, Bunbury 0.01, Boscombe 0 (Cables, Albany and Bunbury use the WA annual range 1.14, 1.38 and 1.20 m as the local tide; 2026-10-19 tide correction).
- **Reported surfable days per year.** Cables 142, Albany 146, Burkitts 30, Boscombe 77 (design baseline).
- **Boscombe "too steep": SUPPORTED.** The 1:3 flank collapses in every case; the 0.5 m wave gives xi_b 1.6, Y 1.3.
- **Boscombe "only bodyboarders": PARTLY.** The model class reads "bodyboard or expert", but the one audit with surfers reports "advanced level surfers" (Davidson 2010 via Rendle 2016).
- **Caveat.** There is no wave climate, so these are not days per year.

## 4. Peel angles serve advanced surfers, never learners (g) - SUPPORTED
- **Refraction.** Designed arm angles of 45-81 deg refract to 16-62 deg at the break.
- **Skill ratings.** Hutt ratings are 3-9 with refraction and 2-6 without. At H0 0.5 m every reef reaches alpha below 27-29 deg (Hutt 8-9).
- **Learners.** No reef reaches 60 deg or more at the break (Hutt 1-3), with one exception: Borth at H0 = 3 m (61.5 deg, rating 3; RESULTS.md s4), a large wave on a reef with no surf record. Peel speeds are 6.9-11.4 m/s.
- **Beginners.** Spilling is 0-29% of on-reef breaks. A dedicated spilling reef needs a ~1:30 ramp (35,000-49,000 m3 per 100 m).
- **Lior's 30 deg.** It matches the Hutt limits: 29 deg is rating 7 (top amateur), 27 deg is rating 8 (professional).
- **Caveat.** The incident angle phi0 is assumed for 5 of 8 reefs. The Narrowneck alternative (41 deg) moves its rating from 4-9 to 9.
- **Literature.** Already in the literature; Walker's 30 deg is a minimum at 6 ft, not a skill level.

## 5. Salient predictors overestimate shoreline response 15-50x (b) - SUPPORTED where testable
- **Predictions (s7).**
  - Black & Andrews (2001): a salient at every reef (B/S 0.23-0.78), 11-114 m.
  - Ranasinghe et al. (2006): accretion at typical waves (Sa/SZW 1.5-5.5).
- **Observations (SEABED_SEDIMENT.md).**
  - Boscombe: +3.4 m (95% CI +1.3 to +5.3, before/after with controls, 316 surveys) against 84 m predicted. Ratio 0.04 (0.02-0.06); 0.1-0.3 against the lower Eq. 31 reading of 11-35 m.
  - Palm Beach: 2 m or less against 114 m.
  - Cables: the lee high pre-dates the reef, and the beach bulge shrank from +26 to +10 m.
  - Borth: a +30 m bulge with no baseline.
- **Reading.** No reef-attributable signal survives a control. This is consistent with Evans & Ranasinghe (2001, via Blacka et al. 2013 p.22): Black & Andrews over-predicts.
- **Why (DERIVED).**
  - Mid-tide transmission Kt is 0.41-0.80, so 50-90% of the energy passes.
  - Reefs are short (12-132 m) and diffract.
  - Beach management moves whole frontages by tens of metres (Boscombe +72 m3/m in 2006-07).
- **Gold Coast: TOO THIN.** The reef effect cannot be separated from nourishment. The non-nourished sites show effects below resolution (a few metres).

## 6. Soft reefs fail, rock survives; uplift plausible only for small or sealed tubes (c, e)
- **Durability (DERIVED classification of reefs.json).** 6 of 7 geotextile or inflatable reefs had major damage or loss within a few years:
  - Pratte's: disintegrated in about 2 years; removed.
  - Mt Maunganui: ruptures and deflation.
  - Opunake: broke apart.
  - Boscombe: failed in 2011.
  - Kovalam: torn and sunk.
  - Bunbury: tore at installation.
- **Narrowneck** survives only with maintenance: settlement of 1-2 m, and 84 containers renewed in 2017-18.
- **Rock.** 0 of 4 rock reefs failed (Cables, Borth, Palm Beach, Albany; Albany had minor rock movement). Fisher exact p = 0.015. Confound: the rock reefs are newer and better funded.
- **Single-tube sliding (van Steeg 2011).** The critical Hs is 0.34-1.65 m. Depth-limited seas reach it at tube bases of 0.6-3.0 m, i.e. inside every surf-reef crest. Rock of 1-2 t resists the same waves (Hudson).
- **Uplift (e), using Bar & Drimer (2023) with a calibrated linear estimate.**
  - No wave pressure under the tube: uplift exceeds the submerged weight under depth-limited breakers for 1.0-1.65 m tubes at 3-4 m depth, and for 2.2-2.75 m tubes at 6-8 m. Uplift grows as H/D, so small tubes lift first (BD23: "too-small Geotubes").
  - Pressure reaching the base: uplift is 0.22 W' or less, and sliding is only marginal (SIc 0.37-0.56 vs friction 0.5).
  - A tube sees 7,000-14,000 load cycles per day.
- **Verdict (c): SUPPORTED** for durability. "Cheapest" and "marine life" are not tested (literature NEW).
- **Verdict (e): PARTLY.** Lift-then-drop is plausible for small tubes. Tearing is not modelled, and the "Drimer 2026" paper was not found.

## 7. Israel's 0.4 m tide: consistent, not more frequent; storm loads unchanged (h-A) - PARTLY
- **Window depends on wave height only** under the Israeli tide (spring range 0.40 m, Rosen 2001):
  - Palm Beach geometry at H0 1 m: 0.69 of the time with its own tide, 1.00 with the Israeli tide.
  - Mt Maunganui at H0 1 m: 0.41 drops to 0, because it needs low water.
  - Mean change over all cases: +0.01 (range -0.30 to +0.61) (s5).
- **Synthetic Haifa reef** (1:12, crest 1 m): 0.87-0.98 surfable at a 0.2-0.4 m range, vs 0.64-0.68 at 4.3 m.
- **Crest load over a spring tide.** The breaking-height range on the crest is 0.31 m in Israel vs 0.9-3.4 m at the built reefs.
- **Storms are not tidal.**
  - Israeli breaker-zone storms (Hs 3.0-3.3 m, 12 h/yr) exceed the single-tube criterion by 2-5x.
  - With a sealed base, a 2.75 m Israeli tube lifts at 7-9 m depth. Depth alone does not protect it within 16 m (s8.5).
  - The torn Israeli tubes were at Ashkelon North (2018-19), not Netanya.
  - The State Comptroller quotes "months to a few years" for an unarmoured sleeve vs about 30 years armoured.
- **Verdict.** Consistency SUPPORTED. "Smaller damage risk" PARTLY. Material choice decides durability.

## 8. Haifa sand: burial risk; sand trap negligible (h-B)
- **Burial.**
  - A 1 m seasonal bed rise removes 19-40% of the reef's relief.
  - 1 m of settlement raises the wave needed to break on a 0.8 m crest from Hb 0.62 to 1.40 m, above the minimum surfable Hs of 0.45-0.60 m.
  - Built geotextile reefs settled 1-2 m; rock (Cables) did not.
  - The "1 m" is Lior's observation and is unsourced; notes/israel.md derives 0.3-1.3 m. SUPPORTED as a risk.
- **Transport scale (CERC, order of magnitude).** 1 m breakers at 10 deg move about 2,700 m3/day. That equals the published net annual drift (60,000-72,000 m3/yr, Zviely et al. 2007) in about 22 days.
- **Sand trap.** At the observed salient ratio (finding 5) a reef stores about 10-2,400 m3, less than 4% of one year's net drift. The Black & Andrews upper bound (21,000-102,000 m3) is a one-off fill, not a supply. NOT SUPPORTED as a sand source.
- **Building on seasonal sand under a geotextile sheet.** This saves about 7,000 m3 per 100 m (about half of a 1:12 reef section; DERIVED). It has no precedent (literature NEW), and the sheet faces the uplift bounds of finding 6.

## Haifa design envelope (RESULTS.md s10)
- **Crest:** 0.6-1.0 m below MSL; 1.2-1.5 m if Lior's field breaking depths hold (Hs/d ~0.35-0.40). This is the largest open uncertainty.
- **Ramp:** 1:16-1:20 for an advanced or intermediate wave; 1:30 for beginners; never steeper than 1:12.
- **Size:** length 100 m or more; 15,000-25,000 m3 per 100 m (the Palm Beach / Albany class).
- **Material:** rock armour Dn50 about 0.7-0.85 m (1.0-1.6 t).
- **Margin and monitoring:** 0.5-1 m for burial and settlement; seasonal bed surveys with controls.
- **Needed next:** Haifa bathymetry, a WNW wave climate, and a 2-D wave model or a flume test.

# Haifa surfable days: check against published Israeli wave statistics

Date: 2026-10-20. Agent: Haiku 5.5 (read-only check; no repo file edited except this note).
Question (Lior): about 130 surfable days a year at Haifa, of which about 60 have Hs > 1 m; most surfable days are small summer waves (Hs about 0.45-0.8 m). Does the published wave climate fit?

Labels: READ = number taken from a source text (by me or by the earlier agent, page given); SEARCH = search-result excerpt only, source text not opened; DERIVED = my calculation, method given; ASSUMPTION = flagged.

## 1. Sources and access

| Source | What it gives | Status |
|---|---|---|
| Bitan, M., & Zviely, D. (2020). Sand beach nourishment: Experience from the Mediterranean coast of Israel. J. Mar. Sci. Eng. 8(4), 273. https://doi.org/10.3390/jmse8040273 (reference in `08_paper/sections/10_references.md`) | Haifa Hs exceedance 1994-2004: 6% of waves Hs > 2 m; 1.4% in 3.0-4.5 m. Summer calm, Hs rarely above 2 m (section 2.1). Closure-depth wave He 3.0-3.3 m in Haifa Bay vs 5.1-5.8 m open coast (p. 3-4). | Full text NOT opened. MDPI returned HTTP 403 "Access Denied" to curl from the sandbox (policy block; not routed around). Figures are READ in `08_paper/notes/israel.md` section 3 (PDF p. 3), taken from an earlier agent's reading; a search excerpt confirms the 6% / 1.4% numbers and the 1994-2004 period. |
| Spanier, E., & Zviely, D. (2023). J. Mar. Sci. Eng. 11(1), 2 (section 2.3.5 and wave section, PDF p. 8) | Mode 0.5-1.0 m at Ashdod and Haifa (citing Tal 2020 MA thesis); storms Hs > 5 m < 0.1% of time; about 5 storms a year > 3.5 m at Haifa (1993-2015); 70% of waves W to WNW at Haifa. | READ in an earlier note (`israel.md`); not re-opened here. |
| Zviely, D. (2026). Six decades of morphodynamic evolution around Ashdod Port. J. Mar. Sci. Eng. 14(18), 1734 (text near Fig. 8) | Ashdod 1992-2015: Hs <= 1.5 m in about 86.8% of records, Hs > 3 m in < 2% (Ashdod, not Haifa). | READ in `israel.md`. |
| Rilov et al. (2005), cited in a ScienceDirect page (search excerpt only) | Haifa, 5510 measurements: 94% had a maximum wave height > 0.5 m; 57% > 1 m. Metric (Hs or maximum wave) not stated in the excerpt. | SEARCH only. Not opened (ScienceDirect blocked earlier). Could not verify. |
| Knobler et al. (2021), J. Mar. Sci. Eng. 9(6), 660 | Southern-Israel buoy (Ashdod area, not Haifa), 2017-2018; storm season Oct-Apr. | Not used for numbers (not Haifa). |
| CAMERI Haifa buoy (about 24 m depth, hourly since 1993) | Would give the exact exceedance table. | Not obtained (live and historical data on cameri-eng.com; not downloaded). |

No source found gives a seasonal exceedance table for Haifa, nor a count of surfable days.

## 2. Numbers (Hs exceedance, Haifa)

| Threshold | Published value | Source | Status |
|---|---|---|---|
| Hs > 0.5 m | not directly published; implied about 75-85% of time (DERIVED, see section 3) | Rilov 2005 (SEARCH): 94% of maxima > 0.5 m | Weak |
| Hs > 0.75 m | not published; implied about 65-70% (DERIVED) | none | Weak |
| Hs > 1.0 m | not published by Bitan/Spanier. Rilov 2005 (SEARCH): 57% of measurements > 1 m (metric unclear). DERIVED from Bitan's 6% > 2 m: about 45-50% | Rilov (SEARCH); Bitan (READ) + DERIVED | Weak; metric conflict |
| Hs > 2.0 m | 6% of waves (1994-2004) | Bitan & Zviely 2020, PDF p. 3 (READ via earlier note) | READ |
| Hs 3.0-4.5 m | 1.4% of waves | Bitan & Zviely 2020, PDF p. 3 (READ) | READ |
| Hs > 3.5 m (storms) | about 5 events a year (1993-2015) | Spanier & Zviely 2023, PDF p. 8 (READ) | READ |
| Hs > 5 m | < 0.1% of time | Spanier & Zviely 2023, PDF p. 8 (READ) | READ |
| Most common Hs | 0.5-1.0 m (Ashdod and Haifa) | Spanier & Zviely 2023, PDF p. 8, citing Tal 2020 (READ) | READ |
| Summer (Apr-Oct) | calm, Hs rarely above 2 m | Bitan & Zviely 2020, section 2.1, PDF p. 3 (READ) | READ |
| Seasonal split of Hs > 0.5 / > 1 m | not found | none | Not found |

Lior's 130 / 60 are not in any source. The check below uses the time fractions above.

## 3. Estimate: days per year

Conversion: days/yr = fraction of time x 365 (valid if the record covers the year evenly; it is a time fraction, not a count of days with any wave above the threshold).

Method for > 1 m: Bitan's 6% above 2 m (READ) is the only Haifa tail point. I fitted a stretched-exponential exceedance P(Hs > H) = exp(-(H/a)^b), with the shape b = 1.5 to 2 (ASSUMPTION; a Rayleigh-type shape). Then:
- b = 2: a = 1.19 m; P(>1 m) = 0.49; P(>0.75 m) = 0.67; P(>0.5 m) = 0.84.
- b = 1.5: a = 1.18 m; P(>1 m) = 0.46; P(>0.75 m) = 0.62; P(>0.5 m) = 0.76.

| Threshold | Time fraction (estimate) | Days/yr (x 365) | Lior |
|---|---|---|---|
| Hs > 0.5 m (surfable lower bound) | 0.76-0.84 | about 280-310 | 130 surfable days in total |
| Hs > 0.75 m | 0.62-0.67 | about 225-245 | not stated |
| Hs > 1.0 m | 0.46-0.49 | about 170-180 | 60 |
| Hs > 2.0 m | 0.06 (READ) | about 22 | not stated |

Cross-check: Rilov 2005 (SEARCH, metric unclear) gives 57% > 1 m, i.e. about 208 days. If that is a daily-maximum count, the true Hs-based figure would be lower; if it is Hs, it agrees with the 46-49% estimate above.

Days caveat: these are time fractions turned into days. "Days with Hs > 1 m at some time" is larger than the time fraction x 365 (a day with a single 1 m wave counts in full). Lior's "days" must be defined before comparing (a day that is surfable for a set, or a day with the mean above 1 m).

## 4. Verdict

- Total surfable days (130): consistent as a count of usable days. Published Hs > 0.5 m occurs on about 280-310 days, so the 130 figure requires that surfability also depends on period, direction, wind and the reef shape. Plausible; not checked against data.
- Days with Hs > 1 m (60): LOWER than the published wave data imply. The Haifa Hs > 1 m share (about 46-49% of time, about 170-180 days a year, DERIVED from Bitan's 6% above 2 m) is about three times Lior's 60. Rilov 2005 (57%, about 208 days) points the same way. Only the Bitan 6% figure is a READ value; the 1 m tail is an extrapolation.
- Summer small waves (Hs 0.45-0.8 m) as most surfable days: consistent with the published summer calm (Bitan section 2.1), the mode 0.5-1.0 m (Spanier & Zviely), and the surfer descriptions (summer 2-3 ft). Not tested: no seasonal Hs table found.

Overall verdict: 130 surfable days is consistent; 60 days above 1 m is LOWER than published statistics suggest (estimate about 170 days by time fraction), so either Lior's 60 uses a stricter definition (sustained or surfable-set height) or the 60 needs checking. Check Lior's definition before the paper uses either number.

## 5. Caveats

1. No Haifa exceedance table was read in full. The Hs > 1 m share rests on one READ point (6% > 2 m, 1994-2004) and a fitted shape (ASSUMPTION). The 1 m, 0.5 m and 0.75 m figures are model values, not published.
2. Rilov 2005's 57% > 1 m is from a search excerpt; the metric (Hs or maximum wave) is not stated. Do not cite it until the paper is read.
3. Bitan's numbers cover 1994-2004; the Haifa record runs to 2015+. Storm years change the tail.
4. Hs is significant wave height at a 24 m buoy; a surf reef sees waves after refraction and the reef's own breaking. Surfable height depends on the break, not on offshore Hs. The estimate is for offshore Hs.
5. Time fraction x 365 is not a day count (see section 3).
6. Lior's surfable definition (Hs 0.45-0.6 m minimum; max wave 0.6-0.8 m) differs from the Hs thresholds above.
7. Next steps to close the gap (not done): (a) read Bitan & Zviely 2020 full text by a legitimate route (library or author copy) to get its Haifa table and the section 2.1 wording; (b) request CAMERI Haifa buoy hourly data (free registration or from the authors, Zviely) for 1993-2025 and compute exceedance by month and days-with-Hs-above-threshold; (c) ask Lior for the definition of "day" and "60 days above 1 m" in his source.

## Sources list

- Bitan, M.; Zviely, D. (2020). J. Mar. Sci. Eng. 8(4), 273. https://doi.org/10.3390/jmse8040273 (PDF p. 3-4 READ via `08_paper/notes/israel.md`; full text blocked by MDPI 403 in this session).
- Spanier, E.; Zviely, D. (2023). J. Mar. Sci. Eng. 11(1), 2. https://doi.org/10.3390/jmse11010002 (PDF p. 8, READ via `israel.md`).
- Zviely, D. (2026). J. Mar. Sci. Eng. 14(18), 1734. https://doi.org/10.3390/jmse14181734 (READ via `israel.md`).
- Rilov, G. et al. (2005). Haifa wave measurements, as quoted in a ScienceDirect search excerpt (not opened). Full citation not confirmed.
- Knobler, M.; Bar, D.; Cohen, E.; Liberzon, D. (2021). J. Mar. Sci. Eng. 9(6), 660. https://doi.org/10.3390/jmse9060660 (not used for numbers).
- Local: `08_paper/notes/israel.md` section 3; `02_research/israel/israel-wave-climate-and-tides.md`.

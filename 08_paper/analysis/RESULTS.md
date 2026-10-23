# RESULTS: computations for the surf-reef review (08_paper/analysis)

Status 2026-10-16. Written after a sanity check and a rerun of every script (`python3 08_paper/analysis/run_all.py`, 3.5 min, rc 0).
Update 2026-10-19: per-reef SURF CUTS for Albany, Cables and Borth (cut through the surfed part of the reef, perpendicular to the
shoreline; `extract_profiles.py` CUT_OVERRIDES), pipeline re-run; changed rows and correlations are marked in place, old values
kept beside them; full old/new list in `RECUT_NOTES.md`.
Every number below is in a results file named in its section. Tags: **SOURCED** (read in a cited source), **DERIVED** (computed here
from sourced inputs by the stated method), **ASSUMPTION** (chosen value, with the reason). Units SI; z in m above MSL (negative =
below MSL); y = offshore distance (m); H0 = deep-water significant height of the incident wave, shoaled by linear theory along the
profile; Hb, db = height and depth at breaking. Short source keys and full references are in `wavelib.py` (REFS) and
`08_paper/lit/references.json`. Findings for the paper are in `FINDINGS.md`; figure data specs in `FIGURE_SPECS.md`.

## 0. Sanity check and fixes made on 2026-10-16

| Check | Result |
|---|---|
| Formulas in `wavelib.py` against the sources | Battjes breaker limits, d'Angremond and Briganti transmission (incl. bounds), Black & Andrews Eqs. 30-31 (checked on the rendered Blacka et al. 2013 p.21), Ranasinghe thresholds (Blacka p.22-23 text), Hudson, CERC (CEM form) and Hutt table: correct. Mead & Black vortex ratio: re-read in Mead (2000) printed p.115 (Eq. 6.5) and p.121 (Table 6.2): X = orthogonal seabed gradient "given as the horizontal distance to one vertical unit"; Y range 1.42-3.43. |
| Datums and signs | All profiles in m MSL (per-reef datum links in `08_paper/data/profiles/<slug>.json`); tidal planes symmetric about MSL (the WA annual-range band is centred on MSL; Bunbury/Albany keep their documented LAT/HAT/MHHW/MLLW planes in the profile JSON, z0 = mean of the band used). Tide ranges plausible (Israel 0.40 spring; Cables 1.14, Bunbury 1.20 and Albany 1.38 = WA DoT 2026 predicted annual range, approx. LAT-HAT, centred on MSL (ANN_LO/ANN_HI planes), NOT spring ranges; Gold Coast 1.31, Mt Maunganui 1.75, Boscombe 1.76, Borth 4.30 spring; Pratte's 1.65 great diurnal range; Opunake 3.16 and Burkitts 2.33 spring, not in the 3D set). Slope sign (rising shoreward) correct. |
| **Bug 1 (fixed, `surf_analysis.py transform`)** | On the 1 m grid a wave could cross a steep face in one step, so the detected break had Hb/db up to 5.3 (physically impossible; 6-39 % of cases per reef had Hb/db > 0.9). The break is now located inside the last 1 m segment (solve H0 Ks(d) = gamma d). After the fix Hb/db = 0.78 (mean 0.783, max 1.23 in rare non-monotonic cells). Breaking position moves < 1 m; Hb on steep faces drops by up to ~25 % (e.g. Boscombe low tide 0.79 -> 0.73 m). |
| **Bug 2 (fixed, `stability_analysis.py`)** | The uplift ratio U used only the pressure on the tube top (no dynamic pressure under the tube), and the Israeli depth scan scaled SIc with the SI factor instead of the SIc factor. Now both bounds are written: `uplift_fraction` (sealed base, upper bound) and `uplift_fraction_contact` (dynamic pressure reaches the base through the BD23 contact term Fc, lower bound), with `state` / `state_contact`; the contact state uses the BD23 index SIc only (SI without Fc is singular when U -> 1). |
| Values that look odd but are real | Borth crest is ABOVE MSL (-1.09 m "depth" at its highest point, -0.47 m on the surf cut: the coastal-defence reef dries at low water). Narrowneck model volume 13,496 m3 vs stated 70,000 m3 (the 3D model is the 2020 photo trace of the visible reef; the stated figure is the "some 70,000 m3" of Jackson 2007 via the NSW review). Pratte's crest-line ramp 1 m is a tip artefact (the representative line is the centreline). Peel speed is the same for every H at a reef (Snell invariant C/sin(alpha), see s3). |

Concurrent edits by another agent in the same round (kept, not mine): `israel_analysis.py` (tide-range sweep for F7, bed 1:70
sensitivity, extra summary shares) and `summarize.py` (peel angle only where the wave breaks on the reef; xi_b / slope correlations).

## 1. Inputs and their status (`reef_inputs.py`, written to `inputs_used.json`)

Geometry: DERIVED profiles from the 3D models (`08_paper/data/profiles/<slug>.json`, crest line + centreline + second line, 1 m
spacing; method in `profiles/SUMMARY.md`). Surfaces are survey-based for Cables (1999), Borth (2022 LiDAR) and Mt Maunganui
(2013 DEM inside -2 m CD); idealised for Boscombe (flat crest, 1:3 flanks), Pratte's (1.35 m stack, 1:1 flanks), Bunbury
(spherical cap), Palm Beach (contour interpolation), Narrowneck and Albany (design-surface rules). Evidence layers are also run
(Boscombe 2011 DGPS survey after failure; Cables original 1999 design; Mt Maunganui 2013 DEM).

| Reef | H site (m) | T site (s) | phi0 arm-to-crest (deg) | Spring range (m) | Outcome (reefs.json) |
|---|---|---|---|---|---|
| Narrowneck | 1.0 SOURCED (Blacka 2013 T4.3) | 10 ASSUMPTION | 81.1 ASSUMPTION (alt 41) | 1.31 | works rarely |
| Palm Beach | 1.0 ASSUMPTION (Narrowneck value) | 10 ASSUMPTION | 44.7 ASSUMPTION/DERIVED axis | 1.31 | works |
| Cables | 1.5 SOURCED (1-2.5 m, Blacka T4.3) | 12 ASSUMPTION | 45 SOURCED design | 0.80 | mixed/disputed |
| Mt Maunganui | 1.5 SOURCED | 11 SOURCED | 50.1 / 54.9 ASSUMPTION | 1.75 | works rarely |
| Pratte's | 1.2 SOURCED (0.9-1.5) | 6 SOURCED (mean period) | 44.7 / 44.4 DERIVED design | 1.65 | does not work |
| Boscombe | 0.5 SOURCED (typical, not surf) | 8 ASSUMPTION (4 s sourced sea) | 72.9 DERIVED (191 deg design swell) | 1.76 | works rarely |
| Borth | 1.0 ASSUMPTION | 8 ASSUMPTION | 64.2 ASSUMPTION | 4.30 | unknown |
| Bunbury Airwave | 1.0 ASSUMPTION | 12 ASSUMPTION | dome, not computed | 0.40 | does not work |
| Albany | 1.0 SOURCED design 0.8-1.3 | 13 ASSUMPTION | 71.2 ASSUMPTION | 0.60 | works |
| Israel / Haifa | Hs 0.45-0.60 m minimum surfable (Lior's Shikmona buoy readings 2025, author's data); storm Hs 3.0-3.3 m breaker zone 12 h/yr (Zviely et al. 2009); > 5 m, T to 15 s (Carmel et al. 1985) | Tp 5.7-6.2 s observed, 6-8 s forecast (LiorBuoy2025) | swell WNW 284-294 deg | 0.40 spring / 0.15 neap (Rosen 2001) | - |

Every run is repeated for H0 = 0.5, 1, 1.5, 2, 3 m (+ site H) and T = 6, 8, 10, 12, 14 s (+ site T), at MLWS / MSL / MHWS (or
MLLW/MHHW), on all lines. Outcome score for statistics: works 3, works rarely or mixed/disputed 2, does not work 1 (reefs.json
`surf_outcome`, each cited there; an ordinal judgement).

## 2. Breaking position, depth gap and ramp (`surf_analysis.py` -> `results_breaking.csv`, `results_size.csv`)

**Purpose.** Where does a wave of given H0, T and tide break relative to the reef (seaward of it, on the ramp, on the crest,
or not at all), and how does that depend on crest depth, depth gap (crest to toe bed) and ramp length (insight f).

**Method.** 1-D cross-shore transformation along each profile. Water depth d(y) = eta - max(seabed, reef). Linear shoaling,
H = H0 Ks(d), Ks = (cg0/cg)^0.5 [Airy; Dean & Dalrymple 1991]; normal incidence, no refraction, friction or reflection.
Breaking at the first point from offshore where H >= gamma d, gamma = 0.78 [McCowan 1894, value read in Weggel 1972 eq.6];
sensitivity gamma = 0.55 (ASSUMPTION; close to Lior's field breaking depths, s9) and the slope-dependent Weggel (1972) index
gamma_b = b - a Hb/(g T^2), a = 43.75(1 - e^-19m), b = 1.56/(1 + e^-19.5m) (slope capped at 0.1, the calibration limit).
Break position classed against the outermost reef toe and the crest zone (+-0.5 m). Bisection gives the smallest H0 that
breaks on the reef at MSL and the largest H0 that still breaks on (not seaward of) the reef.

**Results** (crest line unless noted; site T; MSL).

| Reef | Crest depth (m) | Relief above bed (m) | Depth gap crest-toe bed (m) | Ramp length (m) | Mean ramp slope | H0 to break on reef (m) | H0 max before breaking seaward (m) | Share of H x T x tide x line cases breaking on the reef |
|---|---|---|---|---|---|---|---|---|
| Narrowneck | 1.92 | 0.92 | 2.08 (rep. line 3.92) | 16 (rep. 37) | 1:14.8 | 1.10 | 4.15 | 0.39 |
| Palm Beach | 1.50 | 3.59 | 5.49 | 89 | 1:17.0 | 0.81 | 5.16 | 0.76 |
| Cables (surf cut) | 1.92 | 1.62 | 4.59 | 45 | 1:23.7 | 1.01 | 3.49 | 0.55 |
| Mt Maunganui | 2.08 | 2.56 | 2.83 | 20 | 1:9.3 | 1.16 | 3.04 | 0.47 |
| Pratte's | 1.86 | 1.35 | 1.41 (rep. 1.60) | 1 (rep. 5) | 1:1.4 (rep. 1:4.1) | 1.31 | 2.28 | 0.34 |
| Boscombe | 0.90 | 3.84 | 4.51 | 13 | 1:3.1 | 0.48 | 4.09 | 0.84 |
| Borth (surf cut) | -0.47 (dries) | 4.78 | 4.77 | 40 | 1:9.5 | 0.05 | 3.01 | 0.67 |
| Bunbury | 0.68 | 1.99 | 2.31 | 5 | 1:2.7 | 0.28 | 1.62 | 0.61 |
| Albany (surf cut, -2 m ridge) | 1.97 | 2.53 | 5.40 | 99 (take-off line 22) | 1:19.8 (take-off line 1:4.0) | 1.00 | 4.92 | 0.62 |

Rank correlation with outcome (n = 8, Borth unknown; `results_outcome_correlations.json`; p_perm = two-sided permutation test,
20,000 shuffles): crest depth rho = 0.39 (p_perm 0.36); depth gap (representative line) rho = 0.93 (p_perm 0.005); relief
(representative line) 0.62 (0.15); ramp length 0.93 (0.005); mean ramp slope (1:X) 0.77 (0.039).
**Surf cuts (2026-10-19).** For Albany, Cables and Borth the crest line is now a per-reef surf cut through the part of the reef
where the wave breaks and is ridden, perpendicular to the shoreline (`extract_profiles.py` CUT_OVERRIDES; `profiles/SUMMARY.md`
s1a; `RECUT_NOTES.md`). Old rows: Cables 1.56 | 2.00 | 4.87 | 44 | 1:20.3 | 0.78 | 3.44 | 0.60; Borth -1.09 | 4.44 | 5.35 | 73 |
1:14.5 | 0.05 | 3.03 | 0.68; Albany 1.17 | 5.93 | 6.15 | 22 | 1:4.0 | 0.52 | 4.77 | 0.70. Old correlations: crest depth 0.00
(1.0), relief 0.85 (0.015), ramp length 0.85 (0.015), mean slope 0.62 (0.15).

**Sensitivity.** gamma 0.55 / 0.78 / Weggel changes the on-reef share by <= 0.2 except Bunbury (0.33-0.73) and Narrowneck
(0.40-0.67). Period has little effect on WHERE waves break (on-reef share 0.62 at 6 s to 0.69 at 14 s, crest lines), but a strong
effect on HOW (s3).

**Limitations.** 1-D, no refraction/diffraction around the reef ends (real reefs focus energy; Mead & Black 2001), linear shoaling
up to breaking (underestimates H near breaking), monochromatic H standing for Hs, seabed under most reefs interpolated, slopes
measured along the model y axis (not the true wave orthogonal for oblique swell).

## 3. Breaker type (Iribarren) and Mead & Black breaking intensity (`results_breaking.csv`, `results_surf_site.csv`)

**Purpose.** Is the wave the reef makes spilling, plunging or collapsing, and how hollow (insights d, f, g)?

**Equations.** Surf similarity at the break xi_b = tan(beta) / (Hb/L0)^0.5, L0 = g T^2 / 2 pi; spilling < 0.4, plunging 0.4-2.0,
surging/collapsing > 2.0 [Battjes 1974 via Lewis et al. 2015 Table 1]. Vortex ratio Y = 0.065 X + 0.821 (R^2 = 0.71), X = 1/tan(beta)
along the wave orthogonal [Mead & Black 2001; Mead 2000 Eq. 6.5, printed p.115]; classes (Mead 2000 Table 6.2, p.121): extreme
1.6-1.9, very high 1.91-2.2, high 2.21-2.5, medium/high 2.51-2.8, medium 2.81-3.1; Y < 1.6 "likely to collapse ... unsurfable"
and Y > 3.1 gentle plunging/spilling (p.121 text). Fit range X = 9.2-40 (Y 1.42-3.43): steeper faces are EXTRAPOLATION (flagged).
tan(beta) = least-squares slope over a window max(4 m, Lb/4) centred on the break (DERIVED; seaward-window slope is 0.87x and
landward 0.43x the centred value, median, reported in the CSV). Skill mapping (ASSUMPTION, interpretive): xi_b >= 2 or Y < 1.6 ->
"too hollow / collapsing: bodyboard or expert"; xi_b < 0.4 -> spilling ("beginner-friendly"); Y 1.6-1.9 expert; 1.9-2.5 advanced;
2.5-3.1 intermediate; > 3.1 novice-intermediate.

Note on the literature conflict (LITERATURE.md D-5/D-6, `notes/insights_in_literature.md` (f)): the formula looked unusable
because it was read with a dimensionless slope m (giving Y ~ 0.82). Mead (2000) states X is "the horizontal distance to one
vertical unit" (1:X); with that reading Y spans the reported 1.42-3.43 for 1:9 to 1:40 slopes. The conflict is resolved; the
formula is used here, within its stated scatter (R^2 0.71; Robertson et al. 2014 found R^2 = 0.27 on their own field data).

**Results** (all H x T x 3 tides x default lines, cases breaking on the reef, gamma 0.78).

| Reef | xi_b median (p10-p90) | Y median (p10-p90) | spill / plunge / surge share | Y < 1.6 share | Y outside fit range | Outcome |
|---|---|---|---|---|---|---|
| Palm Beach | 0.49 (0.31-0.70) | 2.01 (1.76-2.06) | 0.29 / 0.71 / 0.00 | 0.00 | 0.00 | works |
| Cables | 0.61 (0.29-1.79) | 1.69 (1.10-2.41) | 0.19 / 0.75 / 0.06 | 0.39 | 0.32 | mixed |
| Albany | 0.56 (0.06-1.28) | 1.75 (1.25-8.9) | 0.33 / 0.67 / 0.00 | 0.29 | 0.40 | works |
| Narrowneck | 0.97 (0.46-2.44) | 1.36 (1.02-2.03) | 0.07 / 0.75 / 0.18 | 0.72 | 0.58 | works rarely |
| Borth | 1.11 (0.52-2.45) | 1.35 (1.15-1.80) | 0.06 / 0.77 / 0.17 | 0.84 | 0.61 | unknown |
| Pratte's | 1.13 (0.55-2.08) | 1.37 (1.03-2.05) | 0.02 / 0.85 / 0.13 | 0.63 | 0.58 | does not work |
| Mt Maunganui | 1.62 (0.96-2.50) | 1.14 (1.02-1.53) | 0.04 / 0.67 / 0.29 | 0.91 | 0.87 | works rarely |
| Boscombe | 2.00 (1.02-3.30) | 1.06 (1.02-1.20) | 0.00 / 0.50 / 0.50 | 1.00 | 0.99 | works rarely |
| Bunbury | 2.97 (2.09-4.88) | 1.05 (0.98-1.13) | 0.00 / 0.10 / 0.90 | 1.00 | 1.00 | does not work |

Evidence layers: Boscombe surveyed surface 2011 (1:12 mean ramp, after the failure) xi_b 0.79, Y 1.44, 85 % Y < 1.6; Cables
original 1999 design xi_b 0.70, Y 1.94; Mt Maunganui 2013 DEM xi_b 2.82, Y 1.04.
Correlation with outcome (n = 8): median xi_b rho = -0.77 (p_perm 0.039); median X at the break rho = 0.69 (p_perm 0.077).
(Surf cuts 2026-10-19: Albany, Cables, Borth rows and these correlations changed; before: Albany 0.75 / 1.64 / 0.24-0.50-0.26 / 0.47 /
0.56, Cables 0.63 / 1.69 / 0.39, Borth 1.06 / 1.39 / 0.77; xi_b rho -0.69 (0.078), X rho 0.62 (0.15). Albany no longer has surging
cases: on the take-off line 26 % of its on-reef breaks were surging/collapsing, on the -2 m ridge none.)
Site waves (`results_surf_site.csv`): Palm Beach at MSL breaks on the ramp 86 m inside the toe, xi_b 0.56, Y 2.05 ("very high",
plunging); Boscombe at MSL (0.5 m, 8 s) breaks on the crest edge, xi_b 1.60, Y 1.30 (collapsing range); Bunbury xi_b 3.3 at all tides.

**Sensitivity.** Period: surging share 0.21 (6 s), 0.29 (8 s), 0.41 (10-12 s), 0.38 (14 s); spilling share 0.22 (6 s), 0.13 (8 s),
0.04 (10 s), 0 (14 s). The same reef gives gentler waves in short-period seas (relevant for Israel, Tp 6-8 s). Single cases can
flip class when the break moves by a few metres onto a different part of a rough surface (e.g. Mt Maunganui at MSL: 1:30 local
slope, spilling), so distributions, not single cases, are reported.

**Limitations.** Battjes limits were derived for plane beaches; Mead & Black's fit for plunging waves at natural breaks with
X 9-40 (most steep reef faces are outside it); local slope depends on the window; the vortex ratio has large scatter. Classes
are indicators, not predictions of ride quality.

## 4. Peel angle and surfer skill (Hutt et al. 2001) (`results_peel.csv`)

**Purpose.** Which surfer levels can ride the reef's wave (insight g)?

**Equations.** Peel angle alpha = angle between the breaking crest and the peel line (the arm). From the incident crest-to-arm
angle phi0 at the arm toe (depth h0) to the break depth hb by Snell's law along an arm with parallel flank contours:
sin(alpha_b) = sin(phi0) C(hb)/C(h0) (DERIVED method; no diffraction). Peel speed Vp = Cb / sin(alpha_b) [Hutt et al. 2001
definition]; by Snell's law Vp = C(h0)/sin(phi0), the same for every H (a check, not a bug). Skill = lowest Hutt rating whose
peel-angle limit <= alpha: 1: 90, 2: 70, 3: 60, 4: 55, 5: 50, 6: 40, 7: 29, 8: 27 deg, 9-10 "not reached" [Hutt et al. 2001 table
as reproduced in Lewis et al. 2015 Table 3 p.15 and Barlow 2013 Table 1.1 p.12, which agree]. Peel angles below ~25 deg approach
close-outs (Mead & Black 2001 via Lewis et al. 2015 p.3).

**Results** (site T, H0 0.5-3 m, MSL; alpha range = smallest H to largest H; rating range in brackets = refracted; "no refr." =
phi0 used directly).

| Reef | phi0 (status) | alpha_b (deg) | Hutt rating (refracted) | Rating no refr. | Vp (m/s) | Site-H value (summary) |
|---|---|---|---|---|---|---|
| Narrowneck | 81.1 (ASSUMPTION) | 24.5-57.3 | 4-9 | 2 | 7.6 | alpha 39.8 (H0 1.5), rating range 2-7 |
| Narrowneck alt. | 41 (ASSUMPTION, oblique SE swell) | 21.3 | 9 | 6 | 11.4 | - |
| Palm Beach | 44.7 (ASSUMPTION) | 16.2-34.6 | 7-9 | 6 | 11.2 | 21.6, 6-9 |
| Cables | 45 (SOURCED design) | 27.4-36.9 | 7-8 | 6 | 11.0 | 27.4, 6-8 |
| Mt Maunganui | 50.1 / 54.9 (ASSUMPTION) | 21.3-51.9 | 5-9 | 5 | 8.2-8.8 | 35.5, 5-7 |
| Pratte's | 44.7 / 44.4 (DERIVED) | 21.8-48.3 | 6-9 | 6 | 7.6 | 34.8, 6-7 |
| Boscombe | 72.9 (DERIVED) | 24.6-57.2 | 4-9 | 2 | 7.2 | 24.6, 2-9 |
| Borth | 64.2 (ASSUMPTION) | 25.8-61.5 | 3-9 | 3 | 6.9 | 34.9, 3-7 |
| Albany | 71.2 (ASSUMPTION) | 22.3-50.6 | 5-9 | 2 | 8.7 | 30.0, 2-7 |

**Reading.** Every designed arm (phi0 45-81 deg) is refracted to 16-62 deg at the break; at small H (shallow breaking) all reefs
reach alpha < 27-29 deg (Hutt 8-9, professional), and only large waves keep alpha > 50 deg (Hutt <= 5). No reef offers alpha >=
60-70 deg (Hutt 2-3) at the break, i.e. none is a learner's wave. Lior's "about 30 deg for good surfers" matches the Hutt
limits 29 deg (rating 7, top amateur) and 27 deg (rating 8, professional).

**Sensitivity.** phi0 is ASSUMED for 5 of 8 reefs (swell direction at the reef unknown); the Narrowneck alternative 41 deg
moves the rating from 4-9 to 9. Refraction from h0 = outer toe depth; a deeper h0 lowers alpha further.

**Limitations.** Straight-arm Snell model; real reefs have curved contours and diffraction; Hutt's table also sets Hb ranges
(ratings 1-4 need Hb <= 1-4 m), checked in the CSV (`Hb_in_rating_range`).

## 5. Surfable window versus tide, incl. the Israeli tide (`results_tide_window.csv`, `results_tide_range_*.csv`)

**Purpose.** For how much of the time does the reef shape a surfable break, and how does the tide range change that (insights
d and h-A)?

**Method.** Water level stepped every 0.02 m between the extreme tidal planes; at each level the case is "works" (breaks on ramp
or crest) and "surfable" (works, xi_b < 2 and Y >= 1.6; ASSUMPTION). Time fractions = share of a synthetic 29.5-day tide
(semidiurnal M2-type sinusoid, amplitude modulated linearly between neap and spring; ASSUMPTION, no diurnal inequality) spent at
working levels. The same geometry is re-run under the Israeli tide (spring 0.40 m, neap 0.15 m; Rosen 2001) and at a fixed MSL.
Depth-limited wave on the crest: Hmax = 0.78 (eta - z_crest). Tide-range sweep (F7, other agent): synthetic Haifa-type reef (s9)
under spring ranges 0-4.3 m.

**Results** (crest line, site T; `frac` = fraction of the lunar month, given that waves of H0 arrive).

| Reef (spring range) | H0 (m) | Works between eta (m MSL) | Works, local tide | Surfable, local tide | Surfable, Israeli tide | Surfable at MSL only |
|---|---|---|---|---|---|---|
| Palm Beach (1.31) | 1.0 | -0.93 to +0.27 | 0.69 | 0.69 | 1.00 | 1 |
| Narrowneck (1.31) | 1.5 | -0.93 to +0.55 | 0.94 | 0.34 | 0.06 | 0 |
| Cables (1.14 annual) | 1.5 | -0.62 to +0.62 | 1.00 | 1.00 | 1.00 | 1 |
| Mt Maunganui (1.75) | 1.0 | -1.21 to -0.23 | 0.41 | 0.25 | 0.00 | 0 |
| Mt Maunganui | 1.5 | -1.21 to +0.49 | 0.79 | 0.26 | 0.81 | 1 |
| Pratte's (1.65) | 1.2 | -1.24 to -0.14 | 0.43 | 0.00 | 0.00 | 0 |
| Boscombe (1.76) | 0.5 | -1.51 to +0.03 | 0.57 | 0.00 | 0.00 | 0 |
| Albany (1.38 annual) | 1.0 | -0.79 to -0.01 | 0.49 | 0.49 | 0.50 | 1 |

Reef-level summary (`results_reef_summary.csv`, mean over H0 0.5-2 m, best default line): surfable fraction local -> Israeli
tide: Palm Beach 0.70 -> 0.75; Cables 0.55 -> 0.61; Albany 0.62 -> 0.59; Borth 0.19 -> 0.28; Mt Maunganui 0.16 -> 0.20;
Narrowneck 0.15 -> 0.04; Pratte's 0.04 -> 0.05; Boscombe 0 -> 0; Bunbury 0.01 -> 0. Range of depth-limited crest wave over a
spring tide (0.78 x range): Israel 0.31 m; Cables 0.89 m; Bunbury 0.94 m; Gold Coast 1.02 m; Albany 1.08 m; Boscombe 1.37 m; Borth 3.35 m (the WA values use the annual range).
Tide-range sweep (synthetic Haifa reef, 1:12 ramp, crest 1.0 m, mean of H0 0.6-1.5 m): surfable fraction 1.00 (no tide), 0.87
(0.2-0.4 m), 0.81 (1.3 m), 0.72 (2.5 m), 0.64 (4.3 m) at T 7 s; 1.00, 0.98, 0.88, 0.78, 0.68 at T 10 s. A crest depth tuned to
each range recovers part of the loss (0.74-0.79 at 4.3 m). 1:8 ramps stay <= 0.25 at every range (too hollow).

**Reading.** A small tide does not raise the AVERAGE surfable time much (Israeli tide minus local tide, 92 reef x line x H cases:
mean +0.01, range -0.31 to +0.61, 66 % of cases change by less than 0.05); it makes the outcome a function of wave height only: for a given swell the reef works all day or not at all.
Large-tide sites gain a low-tide window for small swells and lose high tides; the small tide removes both. The load range on
the crest over a tide is 3-10x smaller in Israel than at the built reefs.

**Limitations.** Wave arrival statistics are NOT included (no wave climate per site), so fractions are "of the time when such
waves arrive", not surfable days per year (reported days: Cables 142, Albany 146, Boscombe 77-154 design, Burkitts 30 per
reefs.json). Sinusoidal tide; surge and seasonal mean sea level ignored.

## 6. Reef size and volume versus outcome (`results_size.csv`, `results_outcome_correlations.json`, `results_volume_outcome.csv`)

**Purpose.** Test insight (a): small reefs do not work.

**Method.** Spearman rank correlation (average ranks for ties) between size metrics and outcome score; two-sided permutation
p-value (20,000 shuffles, seed 1). Model volume and areas from `hypsometry.py` (reef above the interpolated seabed); stated
volumes from reefs.json (each cited).

| Metric | n | rho | p (t-approx.) | p_perm |
|---|---|---|---|---|
| Model volume (9 modelled reefs, Borth unknown) | 8 | 0.93 | 0.001 | 0.005 |
| Alongshore span | 8 | 0.93 | 0.001 | 0.005 |
| Stated volume, modelled reefs | 8 | 0.77 | 0.025 | 0.037 |
| Area within 1 m of the crest | 8 | 0.77 | 0.025 | 0.037 |
| Ramp length (crest line / surf cut) | 8 | 0.93 | 0.001 | 0.005 |
| Cross-shore span / L at toe | 8 | 0.54 | 0.17 | 0.21 |
| Crest depth (crest line / surf cut) | 8 | 0.39 | 0.34 | 0.36 |
| Stated volume, all built reefs (excl. Burkitts natural platform) | 10 | 0.72 | 0.018 | 0.021 |
| Stated volume incl. Burkitts (300 m3 of rock moved on a natural reef, "works") | 11 | 0.43 | 0.19 | 0.21 |

Stated volumes (m3): Bunbury 105, Burkitts 300, Pratte's 1,350, Mt Maunganui 2,800, Kovalam 4,000, Opunake 4,900, Cables 5,500,
Boscombe 12,800, Palm Beach 25,000, Albany 34,000, Narrowneck 70,000. All three "does not work" reefs are <= 4,900 m3; both
built "works" reefs are >= 25,000 m3.

**Limitations.** n = 8-10; outcome is an ordinal judgement; size is collinear with ramp length, relief, material (the large
recent reefs are rock) and budget, so the correlation is not causal. Burkitts (a reshaped natural reef that works) shows that
volume matters only when the reef must create the whole relief. Narrowneck's stated and modelled volumes differ by 5x.

## 7. Wave transmission and shoreline predictors versus the seabed observations (`coastal_analysis.py`)

**Purpose.** What do standard predictors say about protection and salients, and do the observations (SEABED_SEDIMENT.md) agree
(instructor point 2, insight b)?

**Equations.** Transmission Kt = Ht/Hi: d'Angremond et al. (1996) Kt = -0.4 Rc/Hi + c (B/Hi)^-0.31 (1 - e^-0.5 xi), c = 0.64
permeable / 0.80 impermeable, 0.075 <= Kt <= 0.8, for B/Hi < 10; Briganti et al. (2003) Kt = -0.35 Rc/Hi + 0.51 (B/Hi)^-0.65
(1 - e^-0.41 xi), 0.05 <= Kt <= 0.93 - 0.006 B/Hi, for B/Hi >= 10 (both via Blacka et al. 2013 Eqs. 25-29; originals not read).
Hi = shoaled wave at the outer toe (<= 0.78 d); Rc = crest level - water level; B = crest width within 0.5 m of the line maximum
(DERIVED). Salient: Black & Andrews (2001) via Blacka p.21: no change B/S < ~0.1, salient B/S < 2, tombolo B/S > 0.6; X/B = 0.5
(B/S)^-1.27 (Eq. 30), salient amplitude = S - X, Y_off/D_tot = 0.125 +- 0.02 (Eq. 31); B = alongshore span, S = distance of the
footprint centroid from the MSL line. Ranasinghe et al. (2006) via Blacka p.22-23: Sa/SZW < 1 erosion likely, > 1.5 accretion
likely (peak near 2); SZW = natural surf-zone width from the seabed-only profile (DERIVED; Cables: 1:25 nearshore slope ASSUMED).

**Results** (site H and T).

| Reef | Kt low / mid / high tide | B/S | Salient amplitude, B&A Eq. 30 (m) | Sa/SZW (site H / 2H) | Observed lee response (SEABED_SEDIMENT.md) |
|---|---|---|---|---|---|
| Boscombe | 0.05 / 0.48 / 0.47 | 0.39 | 84 (Eq. 31 with D_tot = 1-3 B: 11-35) | 5.5 / 3.7 | +3.4 m at 0 m ODN (95 % CI +1.3..+5.3), BACI 316 surveys; inside nourishment signals |
| Palm Beach | 0.29 / 0.52 / 0.75 | 0.43 | 114 | 4.8 / 2.0 | contour offsets <= 2 m at 1-3 m (chart, LOW) |
| Cables | 0.38 / 0.52 / 0.67 | 0.47 | 98 (Eq. 31: 14-41) | 3.6 / 2.0 | lee high pre-dates the reef (1995); bed change 1995-2002 +0.03 m (SE 0.04); beach bulge +26 m (2001) shrinking to +10 m (2012) |
| Borth | 0.05 / 0.05 / 0.66 | 0.39 (1.22 both mounds) | 88 | 1.8 / 1.4 | 0 m contour bulge +30 m (+12..+48), single 2022 LiDAR, no baseline |
| Pratte's | 0.80 (cap) | 0.63 | 40 | 2.8 / 1.3 | contours +13 m (+9..+18) offshore in 5 months, no control, datum +-10 m |
| Narrowneck | 0.42 / 0.64 / 0.68 | 0.39 | 104 | 3.3 / 1.3 | not testable (continuous nourishment); literature disputed |
| Mt Maunganui | 0.44 / 0.66 / 0.80 | 0.23 | 79 | 2.1 / 1.1 | not testable here |
| Albany | 0.39 / 0.41 / 0.40 | 0.78 | 77 | 2.4 / 1.6 | not testable here |
| Bunbury | 0.46 / 0.64 / 0.80 | 0.34 | 11 | 1.5 / 0.7 | removed in days |

Range over all H, T, tides: median Kt 0.24-0.80 for the submerged reefs (Boscombe 0.24, Palm Beach 0.35, Albany 0.31, Narrowneck
0.41, Cables 0.52, Bunbury 0.57, Mt Maunganui 0.66, Pratte's 0.80); Borth 0.05 (crest emergent at most tides). H0 at which the natural SZW puts the reef at the Ranasinghe peak (Sa/SZW = 2):
0.7-2.1 m; at the erosion threshold (Sa/SZW = 1): 1.5-4.5 m (storms push every reef into the "erosion likely" zone).

**Reading.** Both predictors expect a salient at every reef (B/S 0.23-0.78; Sa/SZW >= 1.5 at typical waves). Where it can be
measured, the observed lee response is 0.02-0.06 of the Black & Andrews Eq. 30 amplitude (Boscombe 3.4/84 m; Palm Beach <= 2/114 m)
and 0.1-0.3 of the lower Eq. 31 reading; the two positive signals (Cables, Borth) are pre-existing or unattributable. This agrees
with Evans & Ranasinghe (2001, via Blacka 2013 p.22) that Black & Andrews over-predict shoreline response. Kt 0.3-0.7 at mid tide
means 50-90 % of the incident energy passes a 2-D crest section, and 3-D diffraction around 60-130 m long reefs reduces the
shelter further.

**Limitations.** Formulas calibrated for rubble-mound or emergent breakwaters (Briganti applied to impermeable reefs is an
ASSUMPTION); 2-D; S and B definitions vary between authors; observations have 2-10 m resolution and short records.

## 8. Stability of sand containers, rock and the uplift mechanism (`stability_analysis.py`)

**Purpose.** Insights (c), (e), (h-A2): do soft structures survive in the breaking zone, and what does the Bar & Drimer (2023)
model say about lifting?

### 8.1 What is usable from Bar & Drimer (2023) [BD23]
Usable: the definitions SI = Fy/(W' - Fz) and SIc = Fy/(W' - Fz - Fc), Fc = L_contact (P_UW + P_DW)/2 (Eqs. 3-5); the finding that
the critical instant is just before breaking, with an up-wave horizontal force coinciding with uplift in a deep trough (p.8,
p.10-11, Fig. 11); and the read-off numbers (validation pair 12 x 3.8 m, h 5 m, T 7 s, H 0.3-1.6 m: Fy 7-44.5 kN/m, Fz 13-64 kN/m,
SI 0.016-0.106; design tube 11 x 2.2 m, h 4 m, T 9 s, H 2.86 m: SI ~0.17, SIc ~0.31; read by eye from Figs. 5-6 and 11, +-10 %,
`notes/bar_drimer_2023_coverage.md` s6.4). Not usable: the BELWF model itself (code not released), fabric stress or tearing (BD23
treats the tube as rigid). The "Drimer 2026" paper Lior cites was not found (`notes/drimer_2026_forces.md`).

### 8.2 Calibrated Froude-Krylov estimate (ESTIMATE, not BELWF)
Linear incident-wave pressure p = rho g (H/2) cosh k(h+z)/cosh kh cos(kx - wt) integrated over a rigid superellipse section
(p = 2.5, ASSUMPTION) on the bed; Fy, Fz over the top surface, Fc from the bed pressure at the contact ends (L_contact = B,
ASSUMPTION); W' = (rho_fill - rho_w) g A, rho_fill = 2082 kg/m3 (BD23 p.6). Calibration against BD23: Fy ratio BELWF/estimate
1.15-1.38, Fz 0.84-1.00, SI 1.23-1.52 (linear-range factor 1.42 applied); design case SI ratio 0.94, SIc ratio 2.24 (applied when
H/h >= 0.6). Sealed-base uplift U = max Fz / W' (upper bound); contact uplift Uc = max(Fz + Fc)/W' (lower bound).
Scaling (DERIVED): U ~ H / (2 c Delta D cosh kh), c ~ 0.87 the section-area factor, so the sealed-base uplift grows as H/D, like a
stability number; the horizontal index SI is nearly size-independent in linear theory (both force and weight scale with area).

Depth-limited breaking wave (H = 0.78 h at the tube base; max over T 6-12 s; `results_stability_fk.csv`, rows at_break):

| Tube (B x D, m; source) | h = 2-3 m | h = 4 m | h = 5 m | h = 6 m | h = 8 m | Uc (all h) | SIc calibrated |
|---|---|---|---|---|---|---|---|
| Mt Maunganui small 1.5 x 1.0 | U 0.87-1.29 | 1.70 | 2.09 | 2.47 | 3.19 | <= 0.03 | 0.37-0.56 |
| Pratte's bag 2.1 x 1.2 | 0.73-1.08 | 1.41 | 1.74 | 2.06 | 2.66 | <= 0.04 | 0.37-0.56 |
| Narrowneck small / Israeli 3 m tube 3.9 x 1.65 | 0.53-0.78 | 1.03 | 1.27 | 1.50 | 1.94 | <= 0.07 | 0.37-0.56 |
| Boscombe container 5.2 x 2.2 | 0.59 | 0.77 | 0.95 | 1.12 | 1.45 | <= 0.08 | 0.43-0.56 |
| BD23 design tube 11 x 2.2 | 0.57 | 0.75 | 0.93 | 1.10 | 1.43 | <= 0.22 | 0.39-0.53 |
| Israeli 5 m tube 6.5 x 2.75 | - | 0.62 | 0.76 | 0.90 | 1.16 | <= 0.10 | 0.48-0.56 |
| Mt Maunganui large 7.2 x 3.2 | - | 0.54 | 0.66 | 0.78 | 1.00 | <= 0.11 | 0.48-0.56 |

(Breaking H at h = 2, 3, 4, 5, 6, 8 m: 1.56, 2.34, 3.12, 3.90, 4.68, 6.24 m.) Load cycles: 86,400/T = 7,200-14,400 per day.

### 8.3 van Steeg et al. (2011) sliding criterion for single tubes
chi Hs / (Delta sqrt(B D) (f cos a + sin a)) <= 0.65 (Eq. 1, read; tests Hs <= 1.5 m, s0p 0.03), chi = 1 (conservative), f = 0.5
(ASSUMPTION; 0.48 bag-on-bag in Corvaro et al. 2022), a = 0. Critical Hs (rho_fill 2082 / 1900 kg/m3, `results_stability_tubes.csv`):
Mt Maunganui small 0.41 / 0.34 m; Pratte's 0.53 / 0.44; Narrowneck small and Israeli 3 m tube 0.85 / 0.70; Boscombe 1.13 / 0.94;
Narrowneck large 1.28 / 1.06; Israeli 5 m tube 1.42 / 1.17; Mt Maunganui large 1.61 / 1.33; BD23 tube 1.65 / 1.36. A depth-limited
Hs = 0.55 h reaches these values at base depths of only 0.6-3.0 m, i.e. every tube in a surf-reef crest (base 2-3 m) is at or
beyond the criterion whenever waves break on it, and Israeli storm Hs 3.0-3.3 m exceeds it by 2-5x.

### 8.4 Rock (Hudson)
Hs_stable = Delta Dn50 (K_D cot a)^(1/3), K_D = 2.0 (breaking waves, rough angular rock, 2 layers, trunk; SPM 1984 via Verhagen
2012), rho_r 2650 (ASSUMPTION), Dn50 = 0.84 D50 (ASSUMPTION). `results_stability_rock.csv`:
Albany armour (D50 0.94 m) 2.4-4.3 m on the faces of its surf cut (steepest 1:3.5, mean 1:19.8, the latter extrapolated); core
(0.49 m) 1.2-2.2 m; belly (0.16 m) 0.4-0.7 m; Cables 1.5 t / 3 t granite 3.1-6.0 m (cot > 5: extrapolated); Borth 4.5-8 t rock
3.3-6.1 m. (Surf cuts 2026-10-19; before, on the take-off line and old cuts: Albany armour 2.1-2.5 m on 1:2.4-1:4, core 1.1-1.3,
belly 0.4; Cables 3.3-5.7; Borth 3.4-7.0 m.) Depth-limited breakers exceed the Albany armour value on its steep outer face
where the bed is deeper than about 3.1 m (2.7-3.2 m on the take-off line), consistent with the reported movement of some core rock in the 26 May 2025 storm (if
exposed) and the repositioning of ~18 rocks in Feb 2026 (reefs.json).

### 8.5 Israeli tube versus depth (`results_stability_israel_depth.csv`; Hmax = min(1.8 Hs Ks, 0.78 h), ASSUMPTION Rayleigh)
| Case | 5 m tube (6.5 x 2.75) U sealed | 3 m tube (3.9 x 1.65) U sealed | Contact case (both) |
|---|---|---|---|
| Hs 1 m, T 7 s (typical surf) | 0.35 (3.3 m) -> 0.16 (15 m) | 0.54 -> 0.26 | Uc <= 0.06, SIc <= 0.33: stable |
| Hs 3.3 m, T 10 s (12 h/yr storm) | 0.50 (3.3 m), 0.77 (5.3 m), 1.02 (7.3-9.3 m), 0.83 (15 m) | 1.04 (4.2 m), 1.77 (8 m), 1.42 (14 m) | SIc 0.29-0.42: below friction 0.5 |
| Hs 5 m, T 12 s (extreme) | 0.80 (5.3 m), 1.32 (9.3 m), 1.56 (11 m), 1.46 (15 m) | 1.06 (4 m), 2.64 (12 m) | SIc 0.25-0.42 |

**Reading.** If the base is effectively sealed (fine sand, tight contact), storm troughs can lift Israeli-size tubes at 4-9 m
depth and depth alone does not protect them within 16 m; if wave pressure reaches the base, lifting is negligible and sliding is
marginal (SIc 0.37-0.56 against f = 0.5) only under depth-limited breakers >= ~3.9 m. Real behaviour lies between the two bounds;
which applies is not known from BD23. Rock of 1-2 t (Hudson) resists the same depth-limited waves.

**Limitations.** Linear theory and rigid section, no breaking-wave impact, no drag/inertia terms, no fabric fatigue, single tube
(interlocking mounds are more stable: Narrowneck survived storms > 5 m with settlement and 84 containers renewed in 2017-18).

## 9. Israel: burial, longshore transport and the sand-trap idea (`israel_analysis.py`)

**Burial / settlement** (`results_israel_burial.csv`; seasonal bed change 1 m = Lior's observation, NOT sourced: Haifa
bed-level series not found, `notes/israel.md` s4.3 derives 0.3-1.3 m; sensitivity 0.5-1.5 m). A 1 m bed rise removes 19-40 % of
the relief of a reef with crest 0.8-1.5 m and toe 4-6 m (relief 2.5-5.2 m). A 1 m settlement of the crest raises the wave needed to
break on it from Hb 0.62 to 1.40 m (crest 0.8 m) or 0.78 to 1.56 m (crest 1.0 m), above Lior's minimum surfable Hs 0.45-0.60 m.
Observed at built geotextile reefs: 1-2 m local settlement (Narrowneck), crest -1.5 m in a year (Pratte's), ~1 m (Mt Maunganui),
~2 m dip after failure (Boscombe); rock (Cables) -0.16 m in 2.2 y, within survey error (reefs.json durability, cited there).

**Longshore transport** (`results_israel_lst.csv`). CERC Q = K (g/kappa)^0.5 Hb^2.5 sin 2theta_b / (16 (s - 1)(1 - n)), K 0.39,
kappa 0.78, n 0.4, s 2.59 [SPM 1984; CEM III-2]: 240-61,000 m3/day for Hb 0.5-3 m and theta_b 5-15 deg; Hb 1 m at 10 deg moves
2,700 m3/day, i.e. the published NET annual drift at the south Carmel coast (60,000-72,000 m3/yr, Zviely et al. 2007) in about
22 days; Hb 2 m at 10 deg in 4 days. Gross transport is therefore many times the net, and a reef's lee sits in a sand stream that
can fill or bury it within one storm season. Order of magnitude only (CERC uncalibrated for Israel).

**Sand trap** (`results_israel_sandtrap.csv`; V = 0.5 Y_off D_tot (h_closure 5 m + berm 1 m) c, c 0.3-0.6 ASSUMPTION).
Black & Andrews upper bound for B = 60-150 m at S = 150-300 m: Y_off 54-119 m, V = 21,000-102,000 m3 (c 0.3); at 0.25 of that
amplitude: 1,300-6,400 m3. At the observed ratio (0.02-0.06 of Eq. 30, s7) a salient of 1-7 m holds about 10-2,400 m3 (V = 24 c Y_off^2),
i.e. < 4 % of one year's net drift (60,000-72,000 m3/yr) and of the Haifa Port trap rate (~66,000 m3/yr, Zviely et al. 2007,
2009). The "cover seasonal sand with a sheet and build on it" idea (h-B3) has no precedent in the literature found
(`notes/insights_in_literature.md`); as arithmetic (DERIVED), a +1 m high-season bed under a 70 m x 100 m footprint is ~7,000 m3,
about half the fill of a 1:12, 0.8 m-crest reef section (13,150 m3 per 100 m), but the sheet's own stability under storm uplift
is untested (s8 bounds apply).

## 10. Haifa design envelope (`results_israel_design_summary.csv`, `results_israel_design_sweep.csv`, `results_tide_range_*`)

**Method.** Synthetic profile (ASSUMPTION; no Haifa bathymetry in the repo): bed 1:50 from the MSL line (1:70 sensitivity) to
8 m; crest 10 m wide at depth d_c, 200 m offshore; seaward ramp 1:s down to the bed; back slope 1:3. Same breaking, Iribarren,
vortex and surfable rules as s2-s5; H0 0.5-2 m, T 6-8 s (Israeli periods), Israeli tide; shares below are over H0 0.6-1.5 m.

| d_c (m) \ ramp | 1:8 | 1:12 | 1:16 | 1:20 | 1:30 |
|---|---|---|---|---|---|
| 0.6 | 0.00, too hollow, 10,800 | 1.00, expert, 14,600 | 1.00, expert 87 % / spill 13 %, 19,400 | 1.00, advanced 47 % / spill 53 %, 25,300 | 1.00, spilling, 49,100 |
| 0.8 | 0.02, too hollow, 9,700 | 1.00, expert, 13,200 | 1.00, expert/spill, 17,400 | 1.00, adv./spill, 22,700 | 1.00, spilling, 44,300 |
| 1.0 | 0.06, too hollow, 8,800 | 0.91, expert, 11,800 | 0.91, 15,500 | 0.91, 20,200 | 0.91, spilling, 39,700 |
| 1.2 | 0.06, 7,800 | 0.76, 10,500 | 0.76, 13,700 | 0.76, 17,800 | 0.76, 35,200 |
| 1.5 | 0.07, 6,500 | 0.54, 8,600 | 0.54, 11,300 | 0.54, 14,600 | 0.54, 28,600 |
| 2.0 | 0.08, 4,600 | 0.21, 6,000 | 0.21, 7,700 | 0.21, 9,800 | 0.21, 19,000 |

Cell = surfable fraction under the Israeli tide, dominant class at MSL, reef volume per 100 m of length (m3, DERIVED cross-section
x 100). Bed 1:70 gives identical fractions and classes. Ramp lengths: 30-32 m (1:8), 39-53 m (1:12), 66-113 m (1:20), 150-219 m
(1:30). "Expert" at 1:12-1:16 is Y 1.6-1.9 (Mead "extreme"); no "intermediate" class appears because, at T 6-8 s, slopes gentle
enough for Y > 2.5 already give xi_b < 0.4 (spilling).

**Envelope** (DERIVED from the table plus s8-s9):
1. Crest depth: d_c <= 1.0 m below MSL for >= 90 % of 0.6-1.5 m waves to break on the reef (gamma 0.78). Lior's field breaking
   depths (Hs 0.45-0.60 m break at 1.3-1.5 m, Hmax 0.6-0.8 m: Hmax/d ~ 0.46-0.53, Hs/d ~ 0.35-0.40) imply earlier breaking, which
   would allow d_c ~1.2-1.5 m; this is the largest open design uncertainty (sensitivity gamma 0.55 in s2).
2. Ramp: 1:8 or steeper gives collapsing waves (the Boscombe/Bunbury failure mode); 1:12-1:16 an expert, hollow wave; 1:20 an
   advanced/spilling mix; 1:30 spilling (novice) waves. Gentler is safer for surfing quality but costs volume.
3. Volume: 10,000-25,000 m3 per 100 m for 1:12-1:20 (comparable to Palm Beach 25,000 m3 and Albany 34,000 m3, the two built reefs
   rated "works"); 35,000-49,000 m3 per 100 m for a beginner (1:30) ramp.
4. Burial margin: +1 m of bed or settlement moves d_c from 0.8 to 1.8 m (surfable 1.00 -> ~0.3); a crest designed at 0.6-0.8 m
   with a rock (non-settling) body keeps the margin. Monitor the bed seasonally.
5. Material: depth-limited breakers on a 4-5 m toe (Hb 3.1-3.9 m) need Hudson Dn50 ~0.7-0.85 m (1.0-1.6 t at cot 12-20, K_D 2,
   DERIVED, extrapolated beyond cot 5), similar to Albany's armour; single geotextile tubes are below the van Steeg criterion by
   2-5x in storms (s8.3).
6. Tide: Israel's 0.4 m spring range keeps the surfable fraction within 0.87-1.0 of the no-tide value (tide-range sweep, s5).

**Limitations.** No Haifa bathymetry, no 2-D/3-D wave model, no refraction or focusing, synthetic straight ramp; the wave
climate (number of days with H0 >= 0.6 m from WNW) is needed to turn fractions into surfable days.

## 11. Reproduction

`python3 08_paper/analysis/run_all.py` (hypsometry -> surf -> coastal -> stability -> israel -> summarize; ~3.5 min). Scratch
tables used to write this file: `/tmp/claude-0/paper/compute/keytables.py` (not part of the repo). Sources of every input: field
`*_src` in `inputs_used.json`, the profile JSONs and reefs.json citations.

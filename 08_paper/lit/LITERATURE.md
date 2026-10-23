# Surf-science and coastal literature: verified citations, formulas and thresholds

Status: 2026-10-15, paper round 1 (literature agent, Haiku 5.5). Private research repo: do not publish.
Companion file: `08_paper/lit/references.json` (structured list, same ids).
Scratch downloads and renders are outside the repo (session scratchpad, folder `lit/`). Nothing from scratch was copied into the repo.

---

## 0. How to read this file

Status tags (also in references.json):
- **[P]** primary text read by us (the original, an open-access copy, or a local copy in `papers/`).
- **[S]** secondary: read only as reproduced in a later source; the original was not read.
- **[C]** citation checked in Crossref metadata only; content not read.
- **[N]** not confirmed: a detail could not be verified.

Other tags: **DERIVED** = computed by us from a stated formula (method given). **ASSUMPTION** = assumed value or reading, stated where used.
Page numbers are printed page numbers of the cited work, unless marked "PDF p.".
"Read as image" = the value came from a rendered page image, not from the text layer.

---

## 1. Bottom line for the paper

1. **Hutt, Black & Mead (2001) Table 3 is now available** (via Lewis, Hunt & Evans 2015, [P] copy). It gives a minimum peel angle per skill level: 90, 70, 60, 55, 50, 40, 29 (top amateur), 27 (professional), not reached for levels 9-10. Lior's "about 30 degrees" matches level 7 (29 deg); level 8 is 27 deg. The original paper was not read.
2. **Battjes (1974) is open and verified** [P]. The 0.4 / 2.0 breaker-type thresholds belong to the **breaking-point** Iribarren number xi_b. The 0.5 / 3.3 pair is the **offshore** xi_0 form (Galvin's criteria converted). Use both labels explicitly; do not mix them.
3. **Weggel (1972) slope-dependent breaker index is verified** [P, equations read from a rendered page]: H_b/d_b = b[m] - a[m] H_b/T^2 with a[m] = 1.36(1 - e^-19m), b[m] = 1/[0.64(1 + e^-19.5m)]. Goda (2010) gives a revised form with A = 0.17 and slope term (1 + 11 s^(4/3)) [P, rendered p. 76]. McCowan's 0.78 is the flat-bed limit.
4. **Mead & Black (2001) breaking-intensity formula is NOT usable as reproduced.** Robertson et al. (2014) reproduce Y = 0.065 m' + 0.821 (R^2 = 0.71) with Y = vortex ratio and m' = m cos(peel angle). With any dimensionless beach slope the formula gives Y ~ 0.82-0.83 (DERIVED, section 4.3), far below the vortex ratios of 1.4 and above reported in the field literature (Blenkinsopp & Chaplin 2008: 1.46-2.28 on a 1:10 slope; Robertson et al. 2014 p. 10: 1.73-4.43 across field and flume studies). Units or coefficients are wrong or unstated. The breaker-intensity classes were not obtained. Do not use either until the 2001 paper is read.
5. **Peel-rate relation** V_s = c / sin(alpha) [S via Lewis et al. 2015, p. 3, equation read as image]: the surfer must travel at least this speed down the line. Small peel angles are fast. Worked example in section 4.1 (DERIVED).
6. **Shoreline response (Black & Andrews 2001, as reproduced in NSW review)**: no change if B/S < ~0.1; salient if B/S < 2; tombolo if B/S > 0.6; X_off/B = 0.5 (B/S)^-1.27; Y_off/D_tot = 0.125 [S via Blacka et al. 2013 §2.5.2, read as images].
7. **Ranasinghe et al. (2006), "Narrowneck" item**: the Crossref-verified paper (Ranasinghe, Turner & Symonds 2006, Coastal Eng. 53, 589-611) models a generic "typical triangular MPR", not Narrowneck. Do not describe it as a Narrowneck study.
8. **Drimer 2025-2026 paper: not found** after 9 searches. Only Bar & Drimer (2023, JMSE 11(2) 236) is a Drimer geotube-load paper [P, local copy]. Lior should give the title or DOI he saw.
9. **CERC longshore transport** verified from USACE EM 1110-2-1100 Part III Ch. 2 [P, copy]: Q = K rho^(1/2) g^(1/2) H_b^(5/2) sin(2 alpha_b) / [16 kappa (rho_s - rho)(1 - n)], K = 0.39 (SPM 1984, significant height), K = 0.92 (SPM 1984, rms), K = 0.77 (Komar & Inman 1970, rms), kappa = 0.78 (flat) rising above 1.0 on slopes, n = 0.4.

---

## 2. Quick table

| # | Item asked | Status | Open access | Use now? | Main caveat |
|---|---|---|---|---|---|
| 1 | Hutt, Black & Mead 2001 (peel angle vs skill) | Table 3 [S via Lewis 2015 P] | no (original) | yes, with citation chain | units of wave height not printed; original not read |
| 2 | Walker 1974 (surf quality, peel angle) | Fig. 2.12 [S via Blacka 2013 P]; text [N] | no copy found | yes (figure values approximate) | report page count conflicts (311 vs 245 p.) |
| 3 | Mead & Black 2001c (breaking intensity, vortex ratio) | eq. 9 [S via Robertson 2014 P]; classes [N] | no | **no** (inconsistent as reproduced) | eq. units; page conflict 51-65 vs 103-130 |
| 4 | Battjes 1974 (surf similarity, breaker types) | [P] full text | yes | yes | label the offshore xi_0 vs breaking-point xi_b forms |
| 5 | Breaker depth index (McCowan, Weggel, Goda) | Weggel [P], Goda [P copy], McCowan [S] | Weggel yes; Goda no | yes | Goda copy provenance; McCowan title/volume conflict |
| 6 | Scarfe et al. 2003 and 2009 | 2003 [S, not read]; 2009a [C]; 2009 overview [P] | 2009 overview yes; others no | partly | 2003 full text blocked by bot challenge |
| 7 | Ranasinghe & Turner 2006 (submerged structures review) | [C] + [S] | no | yes, as summary only | content not read |
| 8 | Black & Andrews 2001 (salient geometry) | [S] via Blacka 2013 figures | no | yes, with citation chain | journal volume/pages not confirmed |
| 9 | Ranasinghe et al. 2006 (Narrowneck item) | [C] + [S] | no | yes, but NOT Narrowneck | generic triangular reef; Narrowneck context from Jackson 2012 [C] |
| 10 | Bar & Drimer 2023 JMSE 11(2) 236 | [P] local + [C] Crossref | yes (CC BY 4.0) | yes | none |
| 11 | Drimer 2025-2026 wave forces | **not found** | - | no | Lior to supply title/DOI |
| 12 | Dean & Dalrymple, Kamphuis, CERC | CERC [P]; Kamphuis 1991 [C]; books [S]/[N] | CERC yes | CERC yes; books cite-only | Kamphuis textbook edition not confirmed |

---

## 3. Items

### 3.1 Item 1: Hutt, Black & Mead (2001), peel angle vs surfing skill

**Citation.** Hutt, J.A., Black, K.P. & Mead, S.T. (2001). Classification of surf breaks in relation to surfing skill. In: Black, K.P. (ed.) *Natural and Artificial Reefs for Surfing and Coastal Protection*, Journal of Coastal Research, Special Issue No. 29, pp. 66-81. No DOI in Crossref. A JSTOR listing (stable 25736206) was seen in a search result and not opened. Open access: no (not checked). Author order is "Hutt & Black" in Rendle (2016) and "Hutt, Black & Mead" in Atkin et al. and Scarfe et al. (2009).
**Status.** [S] Table 3 as reproduced in Lewis, J., Hunt, S. & Evans, T. (2015). Quantification of surfing amenity for beach value and management. Coastal Conference 2015, Table 3 (their p. 15) [P, full text read]. Original not read.

**Table 3 as reproduced** (columns: level, rating text abbreviated, "Peel angle limit (deg)", "Min./Max. wave height"). The reproduction prints no units for wave height. **ASSUMPTION: metres.** Confirm against Hutt et al. 2001.

| Level | Surfer rating (abridged) | Peel angle limit (deg) | Min. / Max. wave height |
|---|---|---|---|
| 1 | Beginner: not yet able to ride the face; moves forward as the wave advances | 90 | 0.7 / 1.0 |
| 2 | Learner: able to ride laterally along the crest | 70 | 0.65 / 1.5 |
| 3 | Developing speed by pumping on the face | 60 | 0.6 / 2.5 |
| 4 | Beginning standard manoeuvres, on occasion | 55 | 0.55 / 4.0 |
| 5 | Standard manoeuvres consecutively on one wave | 50 | 0.5 / >4.0 |
| 6 | Standard manoeuvres consecutively; advanced manoeuvres on occasion | 40 | 0.45 / >4.0 |
| 7 | Top amateur: consecutively execute advanced manoeuvres | 29 | 0.4 / >4.0 |
| 8 | Professional: consecutively execute advanced manoeuvres | 27 | 0.35 / >4.0 |
| 9 | Top 44 professionals | not reached | 0.3 / >4.0 |
| 10 | Surfers of the future | not reached | 0.3 / >4.0 |

**How to read the "peel angle limit".** Lewis et al. say that skill groups "confined by the minimum peel angle defined in Table 3" can ride lower peel angles if they carry momentum (p. 16). So the column is the **lowest peel angle** a level can handle. A wave with a peel angle below the limit is too fast for that level.

**Lior's hypothesis (g), checked.** "About 30 degrees for good surfers making high-level turns": the table places the top amateur floor at 29 deg (level 7) and the professional floor at 27 deg (level 8). The statement is consistent with the table. Smaller peel angles are faster and harder: confirmed by the peel-rate relation (section 3.2).

**Other statements in the same source (S):**
- Peel angles below about 25 deg approaching 0 deg are "close-outs" that cannot be surfed (Mead & Black 2001, via Lewis p. 3).
- Larger peel angles (70-90 deg) suit beginners; 30-50 deg are more challenging (Lewis p. 3).
- A Portuguese-language review attributes about 25 deg to the most skilled (search snippet, Nemes 2006). This disagrees with Table 3 (27-29 deg). Use the table values and flag the difference.

**Boscombe cross-check (DERIVED, see 4.4).** Rendle (2016) Table 4.4 (citing ASR Ltd 2006) gives design peel angles of 60 +/-5 deg (right) and 70 +/-10 deg (left). Rendle (2016) p. 204 says the built reef needed Hutt level 7-8 rather than the design level 5-6 (citing Davidson 2010 and Hutt & Black 2001). This supports the paper's insight (d) about steep, hollow waves.

### 3.2 Item 2: Walker (1974), surf quality, peel angle and surfer skill

**Citations.**
- Walker, J.R. (1974). *Recreational Surf Parameters*. LOOK Laboratory Technical Report TR-30, Department of Ocean Engineering, University of Hawaii, Honolulu. Length conflicts: 311 p (Atkin et al., ICCE ref list; Google Books catalogue) vs 245 p (Blacka et al. 2013 ref list). Not read. No open copy found (catalogue only).
- Walker, J.R., Palmer, R.Q. & Kukea, J.K. (1972). Recreational surfing on Hawaiian reefs. Proc. 13th ICCE, Vancouver, pp. 2609-2628. DOI 10.9753/icce.v13.147 [C].
- Walker, J.R. & Palmer, R.Q. (1971). A general surf site concept. LOOK Lab TR-18 [S, citation only].

**Figure 2.12 (Walker 1974), read as image** in Blacka, M.J. et al. (2013), WRL TR 2012/08, p. 28 (PDF p. 39) [P, local copy]:
- Axes: peel angle alpha (deg, 0-90) against breaker height H_b (ft, 0-25).
- Isolines of surfer velocity V_s (ft/s) = 15, 20, 25, 30, 35, 40.
- Zones labelled BEGINNER (upper left), INTERMEDIATE (upper middle), EXPERT (upper right). Dashed boundary curves drawn; one is labelled "suggested surfable limit".
- Approximate readings (from the scanned figure; about +/-1 ft and +/-5 deg; ASSUMPTION): the V_s = 15 ft/s isoline reaches 90 deg at H_b of about 4 ft; the V_s = 40 ft/s isoline reaches about 60-65 deg at H_b = 25 ft.
- Digitise the figure before using it as data.

**Peel-angle definition** (Lewis p. 3; Atkin et al.): the angle between the trail of broken whitewater and the crest of the unbroken wave, measured as the wave moves shoreward. Walker et al. (1972) describe alpha as the angle between the unbroken crest and the surfer's velocity (per Atkin et al.). The two definitions differ; state which one the paper uses.

**Peel-rate relation (the computational core of Walker's surfability idea).** Lewis et al. (2015), p. 3, equation read as image, attributed to Henriquez (2004):

    V_s = c / sin(alpha)

where c = wave celerity and alpha = peel angle. V_s is the down-the-line speed a surfer must hold to keep up with the breaking point. Small alpha means high V_s. Henriquez 2004 is [N]: the year is 2005 in Bar & Drimer (2023) ref. 14. Check the source before citing.

### 3.3 Item 3: Mead & Black (2001), breaking intensity and the vortex ratio

**Citation.** Mead, S.T. & Black, K.P. (2001c). Predicting the breaking intensity of surfing waves. In: Black, K.P. (ed.), J. Coastal Research SI 29. **Pages conflict:** 51-65 (Atkin et al. ICCE ref list; Mead, Black & Moores 2007 ref list) vs 103-130 (Blacka et al. 2013 ref list; Robertson et al. 2014 ref list). The majority and the authors' own 2007 list support 51-65. Not resolved. Open access: no. Not accessed: ResearchGate blocked (403), joas.free.fr unresolvable, Scripps eScholarship behind an AWS WAF challenge (not bypassed), WASET behind a Cloudflare challenge (not bypassed).

**Equation (9), as reproduced in** Robertson, B., Nistor, I., Hall, K. & Buckham, B. (2014). Remote measurement and prediction of breaking wave parameters. Coastal Engineering Proceedings 34 (ICCE 2014), paper 41, DOI 10.9753/icce.v34.waves.41. Open access yes (ICCE OJS). **Read as image, printed p. 10 [P]:**

    Y = 0.065 m' + 0.821,    R^2 = 0.71
    m' = m cos(phi)
    Y  = vortex ratio (Robertson's reading; see discrepancy D-5)
    m  = seafloor slope normal gradient
    phi = peel angle of the wave

- Source data: images of waves at 23 plane and barred locations worldwide (Robertson p. 10). Scripps-report snippet gives 46 photographs from 23 beaches [search snippet, not verified].
- Critique (Robertson p. 10-11): Mead & Black "collected no direct quantitative wave data"; Blenkinsopp & Chaplin (2008) measured 1.46-2.28 on a 1:10 slope, so slope is not the only control. On Robertson's own field data, eq. (9) gives R^2 = 0.27 (p. 11). Their own regressions give only weak correlations (R^2 about 0.18-0.27) with wave period, height and depth (p. 11).
- Reference vortex ratios: 1.46-2.28 on a 1:10 slope (Blenkinsopp & Chaplin 2008, Robertson p. 10); 1.73-4.43 across field and flume studies (Robertson p. 10). A search snippet gives 1.42-3.43 for Mead & Black's own data (unverified). Robertson et al. and Johnson (2009) disagree on the wave-height trend (p. 10).

**Breaker-intensity classes** (Mead & Black's classification schedule, "Medium" to "Extreme"): **not obtained.** The ResearchGate figure page is blocked (403). A search snippet gave vortex-ratio bands of about 1.6-3.1 for the classes; unverified, do not use.

**Mead & Black (2001a) and (2001b), other SI 29 papers (citation only):** (a) "Field studies leading to the bathymetric classification of world-class surfing breaks", pp. 5-20 (Mead, Black & Moores 2007; Blacka 2013) vs 5-10 (Rendle 2016); (b) "Functional component configurations controlling surfing wave quality at world-class surfing breaks", pages not confirmed. Blacka et al. (2013) §2.6 says Mead & Black (2001) analysed 34 world-class surf breaks and classified their morphological components (ramp, platform, focus, wedge, ledge, ridge, pinnacle) [P].

**Black & Mead (2001), Gold Coast reef surfing aspects**, JCR 2001, pp. 115-130 (issue not given in Bar & Drimer 2023; reference 17 there, [P] local reference list).

### 3.4 Item 4: Battjes (1974), surf similarity and breaker types

**Citation.** Battjes, J.A. (1974). Surf similarity. Proc. 14th ICCE, Copenhagen, Chapter 26, pp. 466-480. DOI 10.9753/icce.v14.26 [C]. Open access yes: https://icce-ojs-tamu.tdl.org/icce/index.php/icce/article/download/2921/2586/ . **Full text read [P].**

**Surf similarity parameter.** xi = tan(alpha) / sqrt(H / L_0) (Battjes 1974, eq. 11, p. 469; OCR garbled the equation, form checked from the surrounding text: "offshore parameter" and "inshore parameter", p. 469-470). The subscript b marks values at the break point. The break point is the most seaward location where some part of the front is vertical, or where foam first appears at the crest (p. 469).

**Breaking criterion.** Eq. (10), p. 468: xi = 2.3 is the Iribarren-Nogales critical value (confirmed by experiments). Battjes notes it is "a regime about halfway between complete reflection and complete breaking".

**Breaker-type thresholds (p. 470), both forms:**

| Form | Surging / collapsing | Plunging | Spilling | Basis |
|---|---|---|---|---|
| Offshore xi_0 (Galvin's offshore parameter converted) | xi_0 > 3.3 | 0.5 < xi_0 < 3.3 | xi_0 < 0.5 | Galvin's experiments on slopes 1:5, 1:10, 1:20 |
| Breaking-point xi_b (re-analysis of Galvin's data) | xi_b > 2.0 | 0.4 < xi_b < 2.0 | xi_b < 0.4 | "approximate transition values" |

Battjes calls all thresholds approximate and says the transition is gradual. The task's "spilling < 0.4 < plunging < 2.0" is the **breaking-point** set. Lewis et al. 2015 Table 1 (p. 4) gives the same breaking-point limits (after SPM 1977 and Galvin 1968) [S].

**Breaker depth index (p. 471).** gamma_b = H_b/d_b generally 0.7-1.2. For spilling-range xi (small xi), scattered about 0.8, with a slow increase with xi above that. (Battjes' Fig. 1 subscripts are garbled in the OCR; read the figure before quoting a value.)

**Shallow-water limit (p. 468-469).** Solitary-wave limit H_b = 2d_b is "unrealistic"; a ratio of order one seems more reasonable.

Galvin (1968), J. Geophys. Res. 73(12), 3651-3659, DOI 10.1029/JB073i012p03651 [C; not read].

### 3.5 Item 5: Breaker depth index with beach slope (McCowan, Weggel, Goda)

**McCowan (1894).** H_b/d_b = 0.78 from solitary-wave theory, for a flat bed. Citation conflict: "On the highest waves of a permanent type", Phil. Mag. (5) 38, 351-358 (Robertson et al. 2014 ref list) vs "On the highest waves in water", Phil. Mag. (5) 36, 351-358 (Goda 2010 ref list). Value read in Weggel 1972 eq. (6), p. 420 [P]. Not read directly.

**Weggel (1972).** Maximum breaker height for design. Proc. 13th ICCE, Vancouver, Chapter 21, pp. 419-432. DOI 10.9753/icce.v13.21 [C]. Open access yes: https://icce-ojs-tamu.tdl.org/icce/article/download/2764/2428/11915 . **Equations read as image, printed p. 421 [P]:**

    H_b / d_b = b[m] - a[m] (H_b / T^2)                       eq. (9)
    a[m] = 1.36 (1.0 - e^(-19 m))      [s^2/ft]                eq. (10)
    b[m] = 1.0 / [0.64 (1.0 + e^(-19.5 m))]                   eq. (11)

- m = beach slope (tangent). H_b in ft, T in s (Weggel's units).
- Limits (text, p. 421): flat slope gives b -> 0.78 and a -> 0 (H_b/d_b = 0.78, independent of steepness); vertical wall gives b -> 1.56 (= 2 x 0.78).
- SI conversion (ASSUMPTION-free, conversion only): H_b in ft = 3.2808 x H_b in m.
- Weggel also quotes Galvin's plunging-breaker relation and Collins & Weir (p. 420). OCR text only, verify before use: Galvin, H_b/d_b = beta_b, beta_b = 0.92 for m >= 0.07 and beta_b = 1.40 - 6.85 m for m < 0.07; Collins & Weir, H_b/d_b = 0.72 + 5.6 m.

**Goda (2010).** Reanalysis of regular and random breaking wave statistics. Coastal Engineering Journal 52(1), 71-106. DOI 10.1142/S0578563410002129 [C]. Open access: no (WSPC). **A copy was read from an unofficial host** (ancientportsantiques.com, with a WSPC "for personal use only" stamp). Lior should confirm provenance through the library or the publisher before citing page numbers.
- Eq. (1) (Goda 1973/1974 form, as Goda 2010 states; section 2.2, text read): H_b/h_b = (A/(h_b/L_0)) {1 - exp[-1.5 pi (h_b/L_0)(1 + 15 s^(4/3))]}, A = 0.17.
- **Eq. (6), revised, read as image, printed p. 76 [P]:** the same form with slope term (1 + 11 s^(4/3)), A = 0.17. Reduction of breaker height 11% at s = 1/10 and 2% at s = 1/50 (p. 76).
- Yamada et al. (1968) revised McCowan's 0.78 to 0.8261 (Goda 2010, Introduction; page not captured) [S].
- Individual breaker heights: A ranges 0.12-0.18 (Goda's 1975 random model, p. 82) [P]. Incipient significant height is about 30% below regular-wave height (abstract) [P].

**Kamphuis (1991).** Incipient wave breaking. Coastal Engineering 15(3), 185-203. DOI 10.1016/0378-3839(91)90002-x [C]. Not read. Correlation coefficients of four breaker-index forms (Goda 2010 p. 76, [P] via Goda): R^2 = 0.69 for f1(0) (constant), 0.67 for f2(h_b/L_0), 0.84 for f3(s) (slope only), 0.88 for f4(s, h_b/L_0). Goda concludes that slope and relative depth must both be in the formula. Use this to justify eq. (6).

### 3.6 Item 6: Scarfe et al. (2003) and (2009), surfing science and coastal management

- **Scarfe, B.E., Elwany, M.H.S., Mead, S.T. & Black, K.P. (2003).** The science of surfing waves and surfing breaks - a review. Proc. 3rd International Surfing Reef Symposium, Raglan, NZ, 22-25 June 2003. Full text listed on eScholarship (Scripps report, id qt6h72j1fz): served an AWS WAF challenge, **not bypassed; not read** [S, search-snippet summaries only]. Snippets say the four key parameters are breaking height, peel angle, breaking intensity and wave section length. Lior should open it in his own browser or library copy.
- **Scarfe, B.E., Healy, T.R. & Rennie, H.G. (2009a).** Research-based surfing literature for coastal management and the science of surfing - a review. Journal of Coastal Research 25(3), 539-557. DOI 10.2112/07-0958.1 [C]. Open access no (bioone blocked by bot protection; not bypassed). Not read. Crossref lists volume 253 (JCR legacy numbering).
- **Scarfe, B.E., Healy, T.R., Rennie, H.G. & Mead, S.T. (2009b).** Sustainable management of surfing breaks: case studies and recommendations. JCR 25(3), 684-703. DOI 10.2112/08-0999.1 [C]. Not read.
- **Scarfe, B.E., Healy, T.R., Rennie, H.G. & Mead, S.T. (2009).** Sustainable management of surfing breaks - an overview. Reef Journal 1(1). Open access yes (NZ Coastal Restoration Trust PDF). **Read [P]**, page range not confirmed (pp. ~49-50 seen). Useful list of factors for a surfing environmental assessment: bathymetry, offshore and inshore wave climate, sediment pathways and grain size, wave refraction, peel angles, breaker intensity, surfer numbers and seasonality, precise ride location, tide and long-term water-level trends, wind, relating the break to skill level, storm surge. Use this list as the checklist for the paper's methods section (wave-quality factors).

### 3.7 Item 7: Ranasinghe & Turner (2006), shoreline response to submerged structures

**Citation.** Ranasinghe, R. & Turner, I.L. (2006). Shoreline response to submerged structures: a review. Coastal Engineering 53(1), 65-79. DOI 10.1016/j.coastaleng.2005.08.003 [C; Crossref verified]. Open access no (Elsevier). Not read.

**Content, as summarised in Blacka et al. (2013) [S, via P]:**
- Submerged structures can produce two contrasting morphodynamic responses, erosion or accretion. Emergent structures give only accretion (Blacka §2.4.9-2.5, citing Ranasinghe et al. 2006).
- Response is set mainly by cross-shore location. Structures nearer the shore (inside the surf zone) give two-cell circulation: flow crosses the reef, reaches the shore and spreads alongshore, causing leeward erosion (Blacka §2.4.9).
- Ranasinghe & Turner (2006) and Yoshioka et al. (1993) are cited for the role of offshore location, with wave orientation and structure depth of lesser importance (Blacka §2.4.9).

Search snippets (unverified) also say that most submerged structures built to that date eroded their sheltered side, and that the review could not yet identify the controlling variables. Use only as summary; check the paper before quoting.

### 3.8 Item 8: Black & Andrews (2001), salients and tombolos behind offshore features

**Citation.** Black, K.P. & Andrews, C.J. (2001). Sandy shoreline response to offshore obstacles, Part 1: Salient and tombolo geometry and shape; Part 2: Discussion of formative mechanisms. Journal of Coastal Research. **Volume, issue and pages not confirmed** (one secondary listing gives 82-93, unverified). Not in Crossref. Open access no. Not read.

**Rules and equations, as reproduced in Blacka et al. (2013) §2.5.2, report p. 20-21 (PDF pp. 32-33), read as image [S, via P]:**
- Geometry (their Fig. 2.7a): B = obstacle longshore crest length; S = offshore distance from shoreline to obstacle; X_off = distance from salient tip to obstacle; Y_off = salient amplitude; D_L, D_R, D_tot = baseline lengths and total width.
- No change to shoreline when B/S < ~0.1.
- Salient formation when B/S < 2.
- Tombolo formation when B/S > 0.6.
- Eq. (30): X_off / B = 0.5 (B/S)^(-1.27).
- Eq. (31): Y_off / D_tot = 0.125 (+/- 0.02).
- Fig. 2.7c (submerged reefs): data scatter of X/B against B/S over about 0.2-2.2. Blacka notes the method "over-predicts salient size" (examples: Narrowneck, Mount Maunganui) and cannot predict erosion (§2.5.2, text after Fig. 2.8; page not captured).
- Derived from aerial photographs of NSW and NZ coasts; the relations do not include wave exposure or transmission (Blacka §2.5.2).

### 3.9 Item 9: "Ranasinghe et al. (2006) Narrowneck" and the Narrowneck literature

- **Ranasinghe, R., Turner, I.L. & Symonds, G. (2006).** Shoreline response to multi-functional artificial surfing reefs: a numerical and physical modelling study. Coastal Engineering 53(7), 589-611. DOI 10.1016/j.coastaleng.2005.12.004 [C]. Not read.
- **Important:** Blacka et al. (2013) p. 18 says the study examines "a typical triangular MPR" with MIKE 21 and a 3-D physical model. It is a **generic** reef study. Do not cite it as a Narrowneck study.
- Blacka (§2.4.9 and §2.5.2) summarises the mechanisms: offshore location controls two-cell circulation and erosion vs accretion. The magnitude and threshold predictions are "to be considered with caution" because the morphodynamics were not validated (Blacka §2.5.2).
- **Jackson, L., Tomlinson, R., Corbett, B. & Strauss, D. (2012).** Long term performance of a submerged coastal control structure: a case study of the Narrowneck multi-functional artificial reef. Coastal Engineering Proceedings 33 (ICCE 2012), paper 54. DOI 10.9753/icce.v33.structures.54 [C]. Not read. This is the Narrowneck long-term source to use.
- **Corbett, B.B., Mulcahy, M.G., Elliott-Perkins, Z. & Hunt, S. (2023).** Narrowneck artificial reef renewal. Australasian Coasts & Ports 2023, Sunshine Coast, 15-18 Aug 2023. DOI 10.3316/informit.477067242341136. Local copy in `papers/` [P, summary read only].
- Shoreline-response statements for Narrowneck (nourishment confound, Lior's point (b)) must cite Corbett et al. 2023 and Jackson et al. 2012 directly. Neither was read in full in this round.

### 3.10 Item 10: Bar & Drimer (2023), JMSE 11(2), 236

**Citation (verified).** Bar, D. & Drimer, N. (2023). Preliminary design tools for hydrodynamic aspects of submerged impermeable breakwaters. Journal of Marine Science and Engineering 11(2), 236. DOI 10.3390/jmse11020236. Published 17 Jan 2023. Licence CC BY 4.0 (Crossref and PDF p. 1). Open access yes.
- **Status:** [P] local PDF in `Initial info from Lior/` (read in an earlier session; see `08_paper/notes/drimer_force_model.md`); [C] Crossref confirms title, authors, volume, issue, article number, date and licence.
- The paper is the Drimer model cited by Lior for geotube sliding (point e). It models sliding and uplift for impermeable submerged structures and does not model tearing. Its critical instant is "typically just before breaking" (p. 2-3 and p. 10-11, per the earlier note).
- Reference list (local PDF, refs 14-18): Henriquez (2005 MSc, TU Delft, "Artificial surf reefs"); Voorde et al. (2009, J. Coast. Res. 25, 69-79); Lopez et al. (2016, Sci. Total Environ. 550, 910-923); Black & Mead (2001, JCR 115-130, issue not given); Jackson et al. (2012) for Narrowneck; Black & Kerry (1999, Coastal Management 27, 355-365) for Mount Maunganui (author names differ from the "Mead & Black 1999" entry in the NSW list).

### 3.11 Item 11: Drimer (2025-2026) on wave forces on geotextile tubes

**Result: not found.** Searches: 9 WebSearch queries in total. Items 1-6 are the queries listed in `drimer_force_model.md` section 2 (that section says 7 were run, so one is unlisted). Items 7-8 were run in this round. All recorded here:
1. "Drimer 2026 geotextile tube wave forces"; 2. "Drimer uplift force submerged breakwater"; 3. "Drimer geotube submerged breakwater sliding index"; 4. "Bar Drimer 2025 ..."; 5. "Drimer N. geotextile tube uplift ... 2025 journal"; 6. "Daniel Bar Nitai Drimer 2025 2026 ..."; 7. "Drimer geotube uplift breaking zone submerged breakwater 2025 journal paper Technion Coastal Engineering Ocean Engineering"; 8. "Drimer 2025 wave forces geotextile container submerged reef uplift sliding journal article".
- Only Bar & Drimer (2023) matched. A Bar & Drimer 2026 JMSE 14(10) 870 is a wave-energy-converter paper (search snippet, off-topic, not used).
- Other leads (not Drimer, not read): Liu et al. (2025), JMSE 13, 1940 (rubble-mound core slip, CC BY; see drimer_force_model.md); "Stability of upper geotextile tube in a stacked formation under wave loading" (IJGGE 2022, ADS 2022IJGGE...8...32K); Rendle & Davidson (2012, ICCE 33 paper 21, DOI 10.9753/icce.v33.structures.21) on the Boscombe geotextile reef's structural integrity.
- **Ask Lior:** the title, journal or DOI of the "2026 Drimer" paper he saw, or a PDF for "new uploads from lior/".

### 3.12 Item 12: CERC longshore transport and textbooks

**USACE (2002), Coastal Engineering Manual EM 1110-2-1100, Part III, Chapter 2 "Longshore sediment transport"** (dated 30 April 2002). Public-domain US government manual. Copy read from a CE-course site (pdhonline.com) [P]; official source publications.usace.army.mil not checked.
- **Eq. (III-2-7b), CERC form** (text layer garbled; structure checked against the surrounding equations and the known CERC form):

      Q_R = K * rho^(1/2) * g^(1/2) * H_b^(5/2) * sin(2 alpha_b) / [16 kappa (rho_s - rho)(1 - n)]

  Printed page not resolved (near III-2-10/11).
- **Coefficient K** (notes (e)-(f) and text): K = 0.39 with significant wave height (SPM 1984); K = 0.92 with rms height (SPM 1984, dashed reference line in Fig. III-2-4); K = 0.77 with rms height (Komar & Inman 1970, "commonly seen in many longshore transport rate computations"). A worked example takes K = 0.60 for spectra "equivalent to rms conditions" (approx. p. III-2-18/19).
- **Breaker index kappa:** 0.78 for flat beaches, "increases to more than 1.0 depending on beach slope (Weggel 1972)" (note g).
- **Constants:** rho_s = 2650 kg/m^3 (quartz), rho = 1025 kg/m^3 (seawater, 33 ppt), g = 9.81 m/s^2, n = 0.4 (note g).
- The manual also has eq. III-2-8 for K (a slope-dependent form), garbled in the text layer. Not used.

**Kamphuis (1991)**: see 3.5.

**Dean & Dalrymple.** *Water Wave Mechanics for Engineers and Scientists*, Advanced Series on Ocean Engineering Vol. 2, World Scientific, 1991 (original Prentice-Hall 1984, ISBN 0-13-946038-1). Paperback ISBN 978-9810204211 (bookseller listing) [S]. Not read; use for linear wave theory only after checking the chapter.

**Kamphuis textbook.** *Introduction to Coastal Engineering and Management*, World Scientific. Edition and volume not confirmed [N]. Do not cite until checked.

### 3.13 Other items found in this round

- **Robertson, B. et al. (2014)** (ICCE 2014, paper 41): open access, read; the eq. (9) source. Also the best short critique of the vortex method (section 3.3).
- **Lewis, J., Hunt, S. & Evans, T. (2015)**, Coastal Conference 2015 (`coastalconference.com/2015/papers2015/James Lewis.pdf`): open, read. Source of Table 1, the peel-rate equation and Hutt Table 3.
- **Battjes (1974)**: open, read. See 3.4.
- **Weggel (1972)**: open, read. See 3.5.
- **Scarfe et al. (2009) overview (Reef Journal)**: open, read. See 3.6.
- **Atkin, Davies-Campbell & McIntosh (year not confirmed)**, "Deep learning object detection application to surfing wave quality", ICCE OJS id 12664, open, first pages read. Use for the peel-angle definition and the list of standard references only.
- **Mead, Black & Moores (2007)** (Mount Maunganui, Coasts and Ports 2007; informit 10.3316/informit.816670201626573) and **Mead & Borrero (2011)** (Multi-purpose reefs, Coasts and Ports 2011; informit 10.3316/informit.715072832934166): local copies in `papers/`, already in the intake. The Mead, Black & Moores (2007) reference list supplies the 51-65 and 5-20 page ranges.
- **Blacka, Shand, Carley & Mariani (2013)**, WRL TR 2012/08 (NSW review): local copy `papers/Review of artificial reefs for coastal protection in NSW 2013.pdf`. The best local source for Walker Fig. 2.12, Black & Andrews Fig. 2.7 and the shoreline-response summary. Report page = PDF page - 12.
- **Rendle (2016)**, PhD thesis, University of Plymouth, doi 10.24382/4536 (PEARL, open; local copy in `papers/`). Table 4.4 (Boscombe design data) and p. 204 (level 7-8 vs 5-6).

---

## 4. Derived numbers (DERIVED; method and assumptions stated)

### 4.1 Peel-rate speed, V_s = c / sin(alpha)

Method: c = sqrt(g h_b) (shallow-water celerity at the break point). **ASSUMPTION:** h_b = depth at break; no current; no refraction within the peel.

| h_b (m) | c (m/s) | alpha 90 deg | 70 deg | 60 deg | 50 deg | 40 deg | 30 deg | 27 deg | 25 deg |
|---|---|---|---|---|---|---|---|---|---|
| 1.0 | 3.13 | 3.1 | 3.3 | 3.6 | 4.1 | 4.9 | 6.3 | 6.9 | 7.4 |
| 2.0 | 4.43 | 4.4 | 4.7 | 5.1 | 5.8 | 6.9 | 8.9 | 9.8 | 10.5 |
| 3.0 | 5.42 | 5.4 | 5.8 | 6.3 | 7.1 | 8.4 | 10.8 | 11.9 | 12.8 |

Units m/s. Multiply by 3.6 for km/h. (For h_b = 2.0 m: 30 deg gives 8.9 m/s, about 32 km/h; 27 deg gives 9.8 m/s, about 35 km/h.) These are the down-the-line speeds the surfer must hold, not measured speeds. Compare with Hutt's levels in section 3.1.

### 4.2 Weggel (1972) slope coefficients and an example

Method: equations (9)-(11) of Weggel, evaluated directly.

| Slope m | Label | a[m] (s^2/ft) | b[m] | H_b/d_b at H_b/T^2 = 0 |
|---|---|---|---|---|
| 0.02 | 1:50 | 0.430 | 0.932 | 0.93 |
| 0.05 | 1:20 | 0.834 | 1.135 | 1.14 |
| 0.10 | 1:10 | 1.157 | 1.368 | 1.37 |
| 0 | flat | 0 | 0.781 | 0.78 |
| infinity | vertical | 1.360 | 1.562 | 1.56 |

Example, 1:20 slope, SI (H_b in m, T in s, H_b in ft = 3.2808 H_b in m):
- H_b = 1.0 m, T = 10 s: H_b/d_b = 1.107, so d_b = 0.90 m.
- H_b = 1.5 m, T = 10 s: H_b/d_b = 1.094, so d_b = 1.37 m.

Caveat: Weggel's fit is to data with large scatter and is for regular waves. Use Goda eq. (6) for a second opinion (section 3.5).

### 4.3 Mead & Black eq. (9) as reproduced: consistency check

Y = 0.065 m' + 0.821 with m' = m cos(phi).

| m (dimensionless) | phi (deg) | m' | Y |
|---|---|---|---|
| 0.02 | 30 | 0.017 | 0.822 |
| 0.05 | 30 | 0.043 | 0.824 |
| 0.10 | 30 | 0.087 | 0.827 |
| 0.20 | 30 | 0.173 | 0.832 |

Reference vortex ratios: 1.46-2.28 on a 1:10 slope (Blenkinsopp & Chaplin 2008) and 1.73-4.43 across field and flume studies (both Robertson p. 10); a search snippet gives 1.42-3.43 for Mead & Black's own data (unverified). To reach Y = 1.46 the formula needs m' = 9.8; to reach Y = 3.43 it needs m' = 40.1.

**Conclusion:** with dimensionless slopes (0.02-0.2) the formula cannot approach the reported vortex ratios. Either the slope is in other units (DERIVED: if m is in per cent, Y reaches 1.46 only for slopes steeper than about 1:10; if in degrees, only steeper than about 1:6), the coefficient or intercept is misprinted in the reproduction, or Y is a different quantity. Do not compute breaking intensity from it until the 2001 paper is read.

### 4.4 Hutt et al. (2001) mapping of Boscombe design peel angles (ASSUMPTION: Table 3 units)

Using the "lowest peel angle a level can handle" reading (section 3.1):
- Design right peel 60 deg: levels with limit <= 60 can ride it, i.e. levels 3 and above (level 3 has limit 60). Wave-height band for level 3: 0.6-2.5 (units assumed m).
- Design left peel 70 deg: levels 2 and above (level 2 has limit 70; wave-height band 0.65-1.5 m).
- With the stated tolerances: right peel 55-65 deg (ridable by level 3 at 60-65 deg, level 4 at 55 deg); left peel 60-80 deg (level 2 at 70-80 deg, level 3 at 60 deg).

Rendle (2016) p. 204 says the built reef needed level 7-8 rather than the design 5-6. The mapping above shows the design peel angles would be ridable by level 2-3 surfers, These are ridable by level 2-3 surfers, below the 5-6 target the designers intended (Rendle p. 204). A mismatch between target and outcome therefore points to the built peel angles or wave heights differing from the design (to be measured), not to the design peel angles alone. This is a point for the paper's discussion (insight d). The built peel angles are not in this file.

---

## 5. Discrepancies to resolve before the paper is final

| # | Item | Source A | Source B | Action |
|---|---|---|---|---|
| D-1 | Mead & Black 2001c pages | 51-65 (Atkin ICCE; Mead, Black & Moores 2007) | 103-130 (Blacka 2013; Robertson 2014) | Use 51-65 with note; check JCR TOC |
| D-2 | Walker 1974 report length | 311 p (Atkin ICCE; Google Books) | 245 p (Blacka 2013) | Cite without page count; or 311 p with note |
| D-3 | McCowan 1894 title and volume | Phil. Mag. (5) 38 "highest waves of a permanent type" (Robertson 2014) | Phil. Mag. (5) 36 "highest waves in water" (Goda 2010) | Check original |
| D-4 | Mead & Black 2000/2001a pages | 5-20 (Mead, Black & Moores 2007; Blacka 2013) | 5-10 (Rendle 2016) | Use 5-20; check TOC |
| D-5 | Mead & Black eq. (9) meaning | Y = vortex ratio, m' = m cos(phi) (Robertson 2014) | Y = breaker intensity, X = orthogonal gradient (Scripps snippet, not read) | Read original; do not use either until resolved |
| D-6 | Mead & Black eq. (9) values | Y = 0.82-0.83 for any realistic slope (DERIVED, section 4.3) | Reported vortex ratio 1.42-3.43 | Units or coefficient unknown |
| D-7 | Breaker-type thresholds | 0.5 / 3.3 (offshore xi_0) | 0.4 / 2.0 (breaking-point xi_b) | Label each; task mixed them |
| D-8 | Hutt peel angle floor, pros | 27 deg (Table 3, via Lewis 2015) | ~25 deg (Nemes 2006 snippet; close-out threshold in Lewis) | Use Table 3 with citation |
| D-9 | Hutt & Black (2001) author order | Hutt, Black & Mead (Atkin; Scarfe 2009) | Hutt & Black (Rendle 2016) | Use Hutt, Black & Mead |
| D-10 | Scarfe et al. 2009 volume | JCR 25(3) (Rendle; Scarfe overview) | Crossref volume 253 | Cite 25(3) |
| D-11 | Henriquez peel-rate source year | 2004 (Lewis 2015) | 2005 (Bar & Drimer 2023 ref 14) | Check thesis |
| D-12 | Ranasinghe et al. 2006 | Task says "Narrowneck" | Crossref and Blacka: generic triangular MPR | Cite as generic; use Jackson 2012 for Narrowneck |
| D-13 | Drimer "2026" | Lior's claim | Only 2023 paper found | Lior to confirm |
| D-14 | Black & Andrews 2001 volume | JCR (no volume in NSW list) | pages 82-93 (search snippet, unverified) | Find TOC |

---

## 6. ASSUMPTIONS made in this file

- A1. Wave-height units in Hutt Table 3 are metres (not printed in the reproduction).
- A2. Walker Fig. 2.12 readings are approximate (+/- 1 ft, +/- 5 deg).
- A3. Peel-rate example uses c = sqrt(g h_b) and h_b = 1, 2, 3 m.
- A4. The Weggel conversion H_b(ft) = 3.2808 H_b(m) is a unit conversion only.
- A5. Galvin's plunging-breaker and Collins & Weir relations are taken from OCR text in Weggel (p. 420); not checked against the figure.
- A6. Goda 2010 provenance: the copy is assumed to match the WSPC article (checked against the DOI page header and the printed page numbers).

---

## 7. Dead ends (literature searches that gave nothing usable)

Recorded here, not in `02_research/dead_ends/`: that folder holds one file per reef, and the page reads it. Main can move these entries if wanted.

| Source sought | Where tried | Result | Might work |
|---|---|---|---|
| Drimer 2025-2026 wave-force paper | 9 web searches (see 3.11) | not found; only Bar & Drimer 2023 | Lior's own copy or DOI |
| Hutt, Black & Mead (2001) full text | ResearchGate publication page (403 "temporarily unavailable"); search for JSTOR 25736206 not opened | not reached | Lior via university library; Black or Mead by e-mail |
| Mead & Black (2001c) full text | ResearchGate (403); joas.free.fr (DNS unresolvable); Scripps eScholarship (AWS WAF challenge, HTTP 202, not bypassed); WASET (Cloudflare challenge, not bypassed) | not reached | Lior via library; the breaking-intensity classification table |
| Walker (1974) TR-30 text | Google Books catalogue only | catalogue only | University of Hawaii Look Lab archive or library request |
| Scarfe et al. (2003) full text | eScholarship (AWS WAF challenge, not bypassed) | not reached | Lior in his own browser; library copy |
| Scarfe et al. (2009a) full text | bioone (Incapsula block, not bypassed) | not reached | Lior via library |
| Black & Andrews (2001) text | Crossref (no record); web search | no text; equations taken from Blacka 2013 | JCR TOC via library |
| Goda (2010) from the publisher | WSPC not tried; unofficial copy read | copy read (provenance flagged) | Lior via library |
| Kamphuis textbook edition | web search | not confirmed | World Scientific catalogue |
| Robertson et al. (2014) elsewhere | none needed (OA) | - | - |
| USACE EM official host | not tried (copy read) | - | publications.usace.army.mil |
| Hutt table 'Rating of surfer skill (adapted from Hutt 2001)' | ResearchGate figure page (403) | not reached | not needed (Table 3 read via Lewis 2015) |

Blocked-access notes: no login was used. No bot check was bypassed. Where a host returned a challenge page (eScholarship, bioone, WASET), the request was not repeated.

---

## 8. Requests for Lior (for REQUESTS_FOR_LIOR.md, not edited here)

1. Title, journal or DOI of the "2026 Drimer" wave-force paper, or a PDF to put in `new uploads from lior/` (item 11).
2. Browser or library copies of: Hutt, Black & Mead (2001) pp. 66-81 (for Table 3 units and the original text); Mead & Black (2001c) (for eq. 9 units and the breaking-intensity classes); Walker (1974) TR-30 (optional); Scarfe et al. (2003) (for the four-parameter statement); Scarfe et al. (2009a) (for the review). Lior may open these in his own browser; the agent must not.
3. Confirm the Goda (2010) copy against the WSPC article.
4. Decide which Mead & Black page range to cite (51-65 is the majority; 103-130 is in two later sources).

---

## 9. Files and provenance

- `08_paper/lit/LITERATURE.md` (this file), `08_paper/lit/references.json` (37 entries; validated as JSON).
- Local sources read, all in the repo and read-only: `papers/Review of artificial reefs for coastal protection in NSW 2013.pdf` (Blacka et al. 2013), `papers/Rendle, E.J., PhD thesis ... .pdf` (Rendle 2016), `papers/Narrowneck Artificial Reef Renewal ... 2023.pdf`, `papers/Mount Maunganui ... 2007.pdf`, `papers/Multi-Purpose Reefs ... 2011.pdf`, `Initial info from Lior/JMSE1100236...2023BarDrimer ... .pdf` (Bar & Drimer 2023), intake files `05_qa/papers_intake/*.md`.
- Open web sources read (URLs in references.json): Battjes (1974), Weggel (1972), Robertson et al. (2014), Lewis et al. (2015), Scarfe et al. (2009 overview), Atkin et al. (ICCE, year unconfirmed), USACE EM 1110-2-1100 Part III Ch. 2 (copy), Goda (2010) (unofficial copy, flagged).
- Crossref API checks for DOIs: Ranasinghe & Turner 2006; Ranasinghe, Turner & Symonds 2006; Bar & Drimer 2023; Scarfe et al. 2009a and 2009b; Rendle & Davidson 2012; Jackson et al. 2012; Robertson et al. 2014; Battjes 1974; Weggel 1972; Walker et al. 1972; Goda 2010; Kamphuis 1991; Galvin 1968.
- No write to git; nothing in `02_research/dead_ends/`, `04_build/`, `papers/`, `new uploads from lior/`, or `07_scale/`.

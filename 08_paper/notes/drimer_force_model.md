# Drimer wave-force model for geotube sliding, and standard stability formulas (rock, geotextile sand containers)

Status: 2026-10-15, paper round 1 (Haiku 5.5 agent). Scope: Lior's claim (e) in 08_paper/PLAN.md, and the formulas for comparing materials.
Scratch downloads and renders: /tmp/claude-0/paper/drimer/ (not in the repo). Local source PDF is Lior's, read only.

Cite keys used below:
- [BD23] Bar, D.; Drimer, N. (2023). Preliminary Design Tools for Hydrodynamic Aspects of Submerged Impermeable Breakwaters. J. Mar. Sci. Eng. 11(2), 236. https://doi.org/10.3390/jmse11020236. Received 13 Nov 2022, accepted 11 Jan 2023, published 17 Jan 2023 (PDF p.1). Open access, CC BY (PDF p.1 licence notice). Local copy: "/home/user/artificial-reef-survey/Initial info from Lior/JMSE1100236DesignToolsSubmergedImpermeableBreakwaters2023BarDrimer - paper with good summary of wrtifical reefs around the world.pdf". Funded by Israel Ports Development & Assets Co., grant 2031167 (PDF p.1). Data availability: "not applicable" (PDF p.12); code not released.
- [VM12] Verhagen, H.J. (2012). ct5308 Breakwaters and Closure Dams, Ch. 7 "Stability of randomly placed rock mounds". TU Delft lecture notes, 29 March 2012. https://ocw.tudelft.nl/wp-content/uploads/ct530807.pdf. Open course material. Cited by printed slide number.
- [CO22] Corvaro, S.; Lorenzoni, C.; Mancinelli, A.; Marini, F.; Rocchi, S. (2022). Hydraulic Performance of Geotextile Sand Containers for Coastal Defenses. J. Mar. Sci. Eng. 10, 1321 (printed header "2022, 10, 1321"). MDPI open access. PDF: https://iris.univpm.it/retrieve/dcfda89a-7b3a-4790-92d7-94e0aa4b9eb7/jmse-10-01321-v2%20%281%29.pdf (PDF file in scratch as src5.pdf). DOI not extracted from the PDF.
- [DO12] Dassanayake, D.T.; Oumeraci, H. (2012). Hydraulic stability of coastal structures made of geotextile sand containers (GSCs): effect of engineering properties of GSCs. Coastal Engineering 2012, proceedings of ICCE 2012, 33rd International Conference, Santander (printed page header "8 COASTAL ENGINEERING 2012"). PDF in scratch (src3.pdf); open PDF at https://icce-ojs-tamu.tdl.org/icce/article/download/6955/pdf/28594. Paper page range not printed on the PDF; PDF has 14 pages.
- [RO09] Recio, J.M.; Oumeraci, H. (2009). Process based stability formulae for coastal structures made of geotextile sand containers. Coastal Engineering 56, 632-658. Paywalled; NOT accessed. Formulas taken from [CO22] Eqs. 7-11 (secondary).
- [OU03] Oumeraci, H.; Hinz, M.; Bleck, M.; Kortenhaus, A. (2003). Sand-filled Geotextile Containers for Shore Protection. Proc. Coastal Structures 2003, Portland OR, 26-30 Aug 2003. NOT accessed; cited via [CO22] ref. 33 and [DO12].
- [WO98] Wouters, B. (1998). Full reference not in any source we hold; cited as in [DO12] Eq. 1.
- [HU] Hudson, R.Y. Laboratory investigation of rubble-mound breakwaters. J. Waterw. Harb. Div., ASCE. NOT VERIFIED: [VM12] and [CO22] give different years and pages (see section 6). From memory: 1959, vol. 85 (WW3), pp. 93-121. Check before citing.
- [VDM88] van der Meer, J.W. (1988). Rock slopes and gravel beaches under wave attack. PhD thesis, Delft University of Technology (from memory; not verified in our sources, which cite "van der Meer 1988" only, [VM12] slide 17 and [VF] p.1).
- [VF] Verhagen, H.J. The effect of foreshore slope on breakwater stability. Year and venue not on the PDF's first page; cites van Gent 2003 and van der Meer 1988. Open PDF: https://repository.tudelft.nl/file/File_0d4897a3-e215-43f3-b7a7-33444f99a0d2 (scratch src4.pdf).
- [LI25] Liu, C.; Li, H.; Jeng, D.; Chen, W.; Zhou, L.; Chen, W. (2025). Overall Slip Failure of a Rubble Mound Breakwater Core Under Solitary Waves: A Numerical Investigation. J. Mar. Sci. Eng. 13, 1940. https://doi.org/10.3390/jmse13101940. CC BY (PDF notice). NOT a Drimer paper; listed as a related lead only.

---

## 1. Bottom line

1. No 2025 or 2026 Drimer paper on wave forces on geotextile tubes was found. Seven Drimer-specific web searches (section 2) returned only [BD23] as the Drimer geotube load paper. Lior's "2026" may be a misdate of [BD23], or a newer paper that is not indexed here. Lior should confirm the title or DOI he saw. If he has a PDF, it should go into "new uploads from lior/" and this note needs redoing against it.
2. The model in section 4 is therefore taken from [BD23], the Drimer paper already in Lior's folder. It is a 2-D Lagrangian boundary-element wave flume (BELWF) for impermeable submerged structures. It computes the horizontal and vertical wave loads on the tube and a sliding index.
3. [BD23] does not model tearing, fabric tension or seams. Its sliding-critical instant is "typically just before breaking" (Introduction p.2-3; Sec. 3.2 p.10-11; Conclusions p.11), when a deep trough passes the tube. Lior's claim (e) is therefore supported only for sliding, not for tearing (section 4.8).
4. The model is written as equations and inputs (section 4.2 to 4.5). The BELWF code is not released ([BD23] p.12, "Data sharing not applicable"; Appendix A says the authors "programmed a source code", with no release statement). A compute agent cannot run BELWF from the paper alone. Options are in section 4.9.
5. Standard formulas were found in open sources and are in section 5: Hudson (1959) for rock, van der Meer (1988) for rock with the P, S, N and surf-similarity terms, the Wouters (1998) stability number for geotextile sand containers (GSCs) with C_w not available here, and the Recio & Oumeraci (2009) process-based sliding and overturning equations for GSCs with their deformation factors not available here.

---

## 2. Search and access log

| Step | Result |
|---|---|
| WebSearch x7 ("Drimer 2026 geotextile tube wave forces", "Drimer uplift force submerged breakwater", "Drimer geotube submerged breakwater sliding index", "Bar Drimer 2025 ...", "Drimer N. geotextile tube uplift ... 2025 journal", "Daniel Bar Nitai Drimer 2025 2026 ...") | Only [BD23] (doi 10.3390/jmse11020236) is a Drimer geotube load paper. No 2025/2026 Drimer geotube paper appeared. |
| WebFetch https://www.mdpi.com/2077-1312/11/2/236 | DNS error from the WebFetch tool. |
| curl (through the session proxy) https://www.mdpi.com/2077-1312/11/2/236 | HTTP 403 from the proxy. Per /root/.ccr/README.md this is a policy block on the host; not retried, not routed around. The local PDF [BD23] was used instead. |
| WebFetch https://www.cameri-eng.com/daniel-bar-publications | DNS error. Not retried. |
| Search snippet: "Bar and Drimer ... J. Mar. Sci. Eng. 2026, 14, 870, SWAN-WEC, deep-water point absorber" (doi 10.3390/jmse14100870) | Off-topic (wave-energy converter). Not verified. Not used. |
| curl: mdpi-res.com JMSE 13 1940 (Liu et al. 2025) | 200, PDF 9.7 MB (under the 50 MB limit). Not Drimer. Used only as a lead. |
| curl: ocw.tudelft.nl (Verhagen 2012 ch.7), icce-ojs-tamu (Dassanayake & Oumeraci 2012), iris.univpm.it (Corvaro 2022), repository.tudelft.nl (Verhagen foreshore note) | All 200, all open PDFs. Used. |
| Recio & Oumeraci 2009 (Coastal Eng. 56) and Oumeraci et al. 2003 (Portland) | Not reached. Formulas taken from secondary sources [CO22] and [DO12]. |

---

## 3. Source status summary

| Source | Access | Used for | Verification level |
|---|---|---|---|
| [BD23] Bar & Drimer 2023 | Open (CC BY), local copy in Lior's folder | Full model (section 4) | Read from PDF. Equations 1-5 and A2-A48 checked on rendered pages. Fig. 11 read by eye (approximate). |
| [VM12] Verhagen 2012 lecture notes | Open course PDF | Hudson K_D table (slides 5-6); van der Meer equations (slides 15-17, 43) | Text layer partly garbled (OCR of formulas). Surging coefficient and some exponents need checking against [VDM88]. |
| [CO22] Corvaro et al. 2022 | Open (MDPI) | Recio & Oumeraci Eqs. 7-9 and Ns definition (Eq. 11) as reproduced | Equation layout partly garbled. Eq. 7 numerator read from text: "0.5 K_SCD C_D + 2.5 K_SCL C_L mu" over "mu K_SR Delta g - K_SCM C_M du/dt". Verify against [RO09]. |
| [DO12] Dassanayake & Oumeraci 2012 | Open PDF | Wouters (1998) stability number (Eq. 1, rendered and checked); damage classes (Table 3) | Eq. 1 rendered and read directly. Table 3 read from text. |
| [VF] Verhagen foreshore note | Open PDF | Steep/shallow-foreshore caveat for van der Meer | Text read. Year not confirmed. |
| [HU], [VDM88], [WO98], [RO09], [OU03] | Not reached | Only as cited in the sources above | Not verified. Marked where used. |

---

## 4. The Drimer model (Bar & Drimer 2023), in computable form

### 4.1 What the model computes

For a submerged impermeable structure on a given cross-shore profile, [BD23] computes, through time over a full wave period:
- the wave pressure on the structure surface (Eqs. A44-A48), and from it the horizontal force F_y and vertical force F_z per unit structure length (the paper plots kN; the length basis is not stated, see section 6);
- the sliding index SI, which is the minimum friction coefficient needed to stop sliding (Eq. 3), and a corrected SI_c that adds a seabed-contact uplift term (Eqs. 4-5).

It is a 2-D potential-flow model, valid up to breaking (section 4.5).

### 4.2 Equations (numbering as printed in [BD23])

Sliding (Sec. 2.4, p.5-6; Eq. 4-5 on p.10):

- (1) N = F_g - F_b - F_z
  N is the normal reaction from the seabed. F_g is the dry weight, F_b the buoyancy, F_z the vertical wave load (positive = uplift, from the text p.8).
- (2) F_mu = N * mu_min = F_y
  Horizontal resistance from friction equals the horizontal wave load.
- (3) SI = mu_min = F_y / (F_g - F_b - F_z)
  Evaluated over one complete wave period. The critical (maximum) SI is the design value. A negative SI means suction toward the incoming waves (p.8).
- (4) F_c = L_contact * (P_UW + P_DW) / 2
  Uplift from dynamic pressure acting under the tube at the seabed contact (verified on rendered p.10). P_UW and P_DW are the dynamic pressures at the up-wave and down-wave contact points. L_contact is the contact length, which the paper does not give as an equation.
- (5) SI_c = mu_min = F_y / (F_g - F_b - F_z - F_c)
  Verified on rendered p.10. The paper says "it is safe to assume that the dynamic pressure penetrates" under the tube, and so uses SI_c as the conservative value.

Hydrodynamics (Appendix A, p.13-20):

- (A2) Laplace equation for the velocity potential: del^2 Phi = 0 in Omega.
- (A3) Free-surface kinematic condition (Lagrangian): Dx/Dt = del Phi on Gamma_f.
- (A4) Material derivative: D/Dt = d/dt + V . del.
- (A5) Free-surface dynamic condition: D Phi/Dt = (1/2) del Phi . del Phi - P0/rho - g z + a . x on Gamma_f, with P0 = 0.
- (A40-A42) Runge-Kutta 4th order time stepping for x and Phi.
- (A43) Stability limit: Delta t < min(Delta S_j / |x_j|) over the free-surface nodes.
- (A44) Total force on a rigid body: F = integral of P n dA = sum_j P_j Delta S_j n_j.
- (A45) F_y = sum_j P_j Delta S_j cos(alpha_j)
- (A46) F_z = sum_j P_j Delta S_j sin(alpha_j)
- (A47) Element pressure = mean of the two node pressures: P_j = (P_t,i + P_t,i+1) / 2
- (A48) Nodal dynamic pressure: P_t,i = -rho * [ dPhi_i/dt + (1/2) del Phi_t,i . del Phi_t,i ]
  The hydrostatic part does not enter F_y. It is carried by buoyancy in F_z (p.20).

Geometry (Sec. 2.2, p.4-5): the Bezuijen & Vastenburg method, described in words only. An empty tube lying flat has width = half its circumference. At filling ratio FA = 1 the section is a circle of radius R = circumference / (2 pi). At 0.60 <= FA <= 0.85 the underside is flat, each side is a quarter circle, and the upper surface is a semi-ellipse, with curvature continuous at the joins. No area formula is given. The compute agent must implement this geometry itself (ASSUMPTION about the exact construction).

### 4.3 Variables and units

| Symbol | Meaning | Unit | Source |
|---|---|---|---|
| T | wave period | s | [BD23] p.10, p.11 |
| H | wave height (generated, or at the structure) | m | [BD23] p.7, p.10 |
| h | still-water depth | m | [BD23] p.5, p.10 |
| tan alpha | seabed slope (design case 1:40) | - | [BD23] p.10 |
| F_y, F_z | horizontal and vertical wave load on the tube (per unit length basis not stated) | kN (figure axis) | [BD23] Fig. 5, Fig. 11 |
| F_g | dry weight of the tube | kN per unit length (basis assumed) | [BD23] Eq. 1 |
| F_b | buoyancy | kN per unit length (basis assumed) | [BD23] Eq. 1 |
| F_c | seabed-contact uplift | kN per unit length (basis assumed) | [BD23] Eq. 4 |
| L_contact | tube-seabed contact length | m | [BD23] Eq. 4 |
| P_UW, P_DW, P_j, P_t,i | dynamic pressure | Pa | [BD23] A47-A48 |
| rho | water density | kg/m^3 | not stated in [BD23] (ASSUMPTION 1025 kg/m^3 for seawater in any calc) |
| rho_s | sand density (wet saturated) | kg/m^3 | 2082 kg/m^3, [BD23] Sec. 2.4 p.6, citing ref. 37 (a sand-density web page) |
| g | gravity | m/s^2 | not stated (ASSUMPTION 9.81) |
| FA | sand filling ratio | - | 0.60 to 0.85 practical range (p.4); FA = 0.8 used in validation (p.7) |
| R | radius of a fully filled tube (FA = 1) | m | [BD23] p.7: R = 3.425 m in the validation example |
| Delta S_j, n_j, alpha_j | panel length, unit normal, panel angle | m, -, rad | [BD23] A44-A46 |
| Phi | velocity potential | m^2/s | [BD23] A2 |
| mu_min, SI | minimum friction coefficient needed to prevent sliding | - | [BD23] Eq. 3 |

### 4.4 Coefficients and fixed inputs

- Sand density 2082 kg/m^3 (wet saturated sand, p.6). The only material constant in the model. Source is a web page (ref. 37), so treat as low confidence.
- Filling ratio range 0.60-0.85 (geometry, p.4). Validation FA = 0.8 (p.7). Design FA not stated for the design example.
- No drag, lift or inertia coefficients (C_D, C_L, C_M). The model integrates potential-flow pressure and does not use Morison-type coefficients.
- No seabed friction coefficient is given as an input. mu_min is the output.
- Numerics: boundary element count "fewer than 1000" for the same geometry (p.5). The complete design flume has 1160 nodes and takes about 40 h on machine C3 (11th-gen Intel i7 laptop, Table 1 and p.10). Time-step limit from A43.

### 4.5 Validity limits

- Dimension: 2-D (flume), per unit structure length.
- Fluid: ideal, irrotational, potential flow. Viscous effects and eddies are not represented (p.5: "BELWF assumes an ideal fluid and a potential flow").
- Breaking: the Lagrangian BEM is "not valid after breaking of the free surface, due to the assumption of a simply connected domain" (Introduction, p.2-3). The critical state is taken just before breaking. The design-example plunging breaker is simulated only up to the critical instant.
- Structure: impermeable, smooth, rigid body (A44 "forces acting on rigid bodies"). No fabric deformation, no porosity, no uplift-induced shape change. This is the central limitation for tube tearing.
- Validation range: T = 7 s, depth 5 m, H = 0.3 to 1.6 m, freeboard 1.2 m, two tubes making a 12 m structure, FA = 0.8 (p.7). Reference OpenFOAM model: second-order Stokes wave generator, VOF with turbulence (p.5).
- Design range (p.10): T = 9 s, generated H = 2.2 m at the wave generator, intermediate depth 16 m, 1:40 slope to a 4 m shallow shelf, single tube 11 m wide, 2.2 m high, freeboard 1.8 m. Iribarren number 0.17.
- Wave generation for BELWF (design case) is not described. Flag for the compute agent.

### 4.6 Validation results (for the uncertainty statement in the paper)

- Maximum uplift vertical load: good agreement between BELWF and OpenFOAM (p.8).
- Horizontal load: BELWF about 10% higher than OpenFOAM at high waves (p.8).
- Critical friction coefficient SI: BELWF about 15% higher than OpenFOAM in the three cases shown (Figs. 7-9, wave heights 1.3, 1.4, 1.5 m), so BELWF is conservative (p.8).
- Critical state in validation: a deep trough near the tube gives negative (up-wave) F_y at the same time as positive (uplift) F_z (p.8).
- Fig. 6 compares the critical SI at all wave heights (values not extracted).

### 4.7 Worked example from the paper (design case, p.10-11)

Inputs as printed: T = 9 s; H = 2.2 m at generation; shoals from 16 m over 1:40 to 4 m; wave shoals to 2.86 m at the toe of the structure (p.10); tube 11 m wide, 2.2 m high, freeboard 1.8 m; Iribarren 0.17 (p.10).

Outputs (Fig. 11, read by eye from the rendered page, so approximate):
- Peak SI (Eq. 3, solid curve) about 0.17 at t/T = 8.16 (green marker, the instant just before breaking). Uncertainty about +/- 0.03.
- Peak SI_c (Eq. 5, dashed curve) about 0.3 (about 0.32 by eye) at the same instant. Uncertainty about +/- 0.03.
- Negative SI about -0.05 during t/T = 7.4 to 7.9 (trough phase; onshore F_y).
- F_y and F_z mostly within about +/- 100 kN on the figure axis. Fine values are not tabulated, so use only as an order of magnitude.

DERIVED check (method: xi0 = tan(alpha) / sqrt(H/L0), L0 = g T^2 / (2 pi), g = 9.81 m/s^2 ASSUMPTION):
- L0 = 9.81 * 9^2 / (2 pi) = 126.5 m.
- With H = 2.86 m (wave at the toe): xi0 = 0.025 / sqrt(2.86 / 126.5) = 0.166. Matches the paper's 0.17 (p.10).
- With H = 2.2 m (generated): xi0 = 0.190.
- So the paper's 0.17 corresponds to the 2.86 m wave at the toe, not to the 2.2 m generated wave.

### 4.8 Lior's mechanism claim (e), tested against [BD23]

Claim (PLAN.md (e)): most of the wave power acts at the break; it lifts the tube up and then down, which is why most tubes tear.

What [BD23] supports:
- The sliding-critical instant is just before breaking (p.8, p.10-11; Fig. 11 green marker). The load peak is therefore at the break, consistent with "most of the power acts at the break".
- The critical load combination in a deep trough is an onshore horizontal force with positive uplift (p.8). This is the lift-then-release sequence in the claim, for sliding only.

What [BD23] does not support or model:
- Tearing, seam failure, fabric tension, or abrasion. None are modelled. [BD23] explicitly treats the tube as rigid (A44).
- The "lift up and down" cycle as a cause of tearing. [BD23] gives the force cycle, not the stress cycle in the fabric.
- The statement that most tubes tear. [BD23] (p.2) says failures come from "too-small size Geotubes installed or the loss of effectiveness due to sand coverage" (citing [18, 20] in [BD23]). Tearing is not the failure mode the paper names.

Conclusion for the paper: the sliding part of (e) is backed by [BD23]. The tearing part needs a separate source (fabric strength and seam data). Do not cite [BD23] for tearing.

### 4.9 Options for computing with this model (for the compute agent)

Option A (preferred if the code can be obtained): ask Lior or the authors for the BELWF code. Not available from the paper.

Option B (no code): use the paper's equations and read-off values only. The compute agent can evaluate Eqs. 3 and 5 for any force history it has, and can compare materials by the critical SI.

Option C (estimate, flagged as such): linear-wave potential-flow pressure integrated over a rigid section with Eqs. A44-A48 and (4)-(5). Note the paper says the critical state is near breaking, where linear theory fails. Option C cannot give the critical SI. Label any result as ESTIMATE, not DRIMER-MODEL.

---

## 5. Standard stability formulas for comparing materials

### 5.1 Hudson (1959) for rock, non-deformable armour

Formula as stated in [VM12] slide 5 (formula block, read from OCR):
- W >= rho_r * g * H^3 / (Delta^3 * K_D * cot alpha), with Delta = rho_r/rho_w - 1.
- Reference case in [VM12] slide 18: H_s = 2 m, cot alpha = 3, d_n50 = 0.6 m (300-1000 kg), relative density Delta = 1.65, Hudson K_D = 2.

Damage multiplier: [VM12] slide 7 gives a damage multiplier for Hudson for quarry stone (smooth and rough) at damage levels 0-5% to 40-50%. Values in the text layer: 1.00 to 1.54 (smooth), 1.00 to 1.56 (rough). Read from text; check.

K_D values for rough angular quarry stone, from [VM12] slides 5-6 (tables labelled SPM 1977 and SPM 1984):
- SPM 1984 (slide 6), 2 layers, trunk: K_D = 2.0 (breaking), 4.0 (non-breaking). Head: 1.6 and 2.8 (marked *).
- SPM 1977 (slide 5), 2 layers, trunk: K_D = 3.5 (breaking), 4.0 (non-breaking). Head: 2.5 and 2.8 (marked *).
- 3 layers, trunk: SPM 1977 3.9 (breaking) and 4.5 (non-breaking); SPM 1984 2.2 and 4.5.
- 1 layer: trunk non-breaking 2.9 (both editions); head non-breaking 2.3 (SPM 1977) and 2.2 (SPM 1984). Breaking-wave values are marked ** and the notes say "single layer is not recommended under breaking waves" (slide 6).
- K_D values depend on slope (notes: "slight variation ... for different slopes", slide 5).
- Notes footnote: H10 = 1.27 H_s. State which wave height the formula uses.

Compute use: W for given H, K_D, rho_r, and slope. Not valid for geotubes (deformable; Hudson does not account for deformation, [CO22] Sec. 4 and [DO12] p.2, Group 2).

### 5.2 van der Meer (1988) for rock, plunging and surging breakers

Formula as stated in [VM12] slide 17, reconstructed from OCR. Coefficients are standard values; the OCR is partly garbled, so check against [VDM88].
- Plunging (xi_m < xi_t): H_s / (Delta * D_n50) = 6.2 * P^0.18 * (S / sqrt(N))^0.2 * xi_m^(-0.5)
- Surging (xi_m > xi_t): H_s / (Delta * D_n50) = c_s * P^(-0.13) * (S / sqrt(N))^0.2 * sqrt(cot alpha) * xi_m^P, with c_s = 1.0 (OCR shows "10"; check).
- Transition: xi_t = (6.2 * P^0.31 * sqrt(tan alpha))^(1/(P+0.5)). The OCR drops a square root sign, so check.
- Surf-similarity parameter: xi_m = tan alpha / sqrt(2 pi H_s / (g T_m^2)), deep-water values with T_m mean period ([VM12] slide 15).
- Damage: S = A / D_n50^2, with A the erosion area ([VM12] slide 12).
- N = number of waves. P = permeability coefficient; values are on [VM12] slide 16 (figure; not extracted).
- Delta = rho_r/rho_w - 1. D_n50 = (W50 / (rho_r g))^(1/3) ([VM12] slide 12).

Validity (as stated in the sources): deep-water tests; steep and shallow foreshores are not covered. [VF] says the van der Meer formula does not consider shallow water or steep foreshores, and that damage is higher there than expected. [VM12] slide 43 gives general deep-and-shallow forms with H_2% and s_m-1,0, but its OCR is too garbled to use without checking.

### 5.3 Geotextile sand container (GSC) stability number (Wouters 1998, as used in [DO12] Eq. 1)

Rendered and read directly from [DO12] p.2 (Eq. 1):
- N_s = H_s / ((rho_GSC / rho_w - 1) * D) = C_w / sqrt(xi_0), with xi_0 = tan(alpha) / sqrt(H_s / L_0), L_0 = g T^2 / (2 pi).
- H_s: incident significant wave height (m). D: thickness of the armour layer (m). alpha: slope angle. rho_w, rho_GSC: water and container densities. C_w: empirical parameter from hydraulic stability tests; value NOT AVAILABLE in the sources held here.
- [CO22] Eq. 11 uses the same stability number in another form: N_s = H / (Delta * D) = H / (Delta * l_c * sin alpha), with Delta = (rho_s - rho)/rho and l_c the container length (printed as in CO22 p.21).

DERIVED example (from the paper's design case, ASSUMPTION rho_w = 1025 kg/m^3 and D = 2.2 m, the tube height):
- Delta = 2082/1025 - 1 = 1.031.
- N_s = 2.86 / (1.031 * 2.2) = 1.26.
- xi_0 = 0.166.
- Implied C_w = N_s * sqrt(xi_0) = 0.51. This is what C_w would need to be for the Wouters form to hold for this case. It is not a stability result. A threshold C_w for failure is needed and is not available here.

Damage classes ([DO12] Table 3, read from text):
- "Stable": displacement less than 10% of container length and angular motion less than 10 degrees.
- Five categories, DC0 ("no damage") to DC4 ("total failure"); DC1 = "incipient motion" ([DO12] p.8). The numeric thresholds for DC2 to DC4 are in Table 3 and were not read.
- The stability curves in [DO12] are drawn for DC1 only, against crest freeboard R_C* = R_C / H_s and the surf-similarity parameter.

### 5.4 Process-based GSC formulas (Recio & Oumeraci 2009, as reproduced in [CO22] Sec. 4)

These equations are reproduced as printed in [CO22]. The layout is partly garbled. Check against [RO09].

Required length of the container for sliding (Eq. 7):
- l_c >= u^2 * (0.5 * K_SCD * C_D + 2.5 * K_SCL * C_L * mu) / (mu * K_SR * Delta * g - K_SCM * C_M * du/dt)

Required length for overturning (Eq. 8):
- l_c >= u^2 * (0.05 * K_OCD * C_D + 1.25 * K_OCL * C_L) / (0.5 * K_OR * Delta * g - 0.1 * K_OCM * C_M * du/dt)

Required weight (Eq. 9):
- W >= 0.1 * rho_s * g * l_c^3, with l_c the larger of the Eq. 7 and Eq. 8 results.

Inputs and fixed values printed in [CO22]:
- u = velocity at depth H_i / 6 below the free surface.
- mu = 0.48 (friction coefficient between non-woven geotextile bags; [CO22] Sec. 4).
- Delta = (rho_s - rho) / rho.
- Container geometry assumed: length l_c, height l_c / 5, width l_c / 2; container weight W = 0.1 rho_s g l_c^3.
- Assumptions: 80% filled, deformation angle 45 degrees, effective length not affected by deformation = 0.8 l_c ([CO22] Sec. 4, around Eqs. 7-9, from [RO09]).
- Deformation effects: uplift increases exposed area and drag by up to 40%, and reduces resisting force by up to 30% ([CO22] Sec. 4, citing [RO09]). Deformation can change the required length by up to 2x and the required weight by up to 8x ([CO22] Sec. 4).
- NOT AVAILABLE: C_D, C_L, C_M values, and K_SCD, K_SCL, K_SCM, K_SR, K_OCD, K_OCL, K_OR, K_OCM deformation factors. These are "see [34]" in [CO22]. Not obtained.

Compute use: Eqs. 7-9 can be evaluated only once the coefficients are known. They can be compared with a rock weight from Hudson for the same wave and slope, as long as the coefficient source is stated.

### 5.5 Oumeraci et al. (2003) and other GSC limits

[CO22] Fig. 17 compares its data with the Oumeraci et al. (2003) stability-number trend, where N_s vs xi (Iribarren) is plotted. The fitted limit values are NOT AVAILABLE in our sources. Do not invent them.

### 5.6 Comparison table (for the compute agent)

| Formula | Applies to | Key inputs | Coefficients and status | Source |
|---|---|---|---|---|
| Hudson W = rho_r g H^3 / (Delta^3 K_D cot alpha) | rock, non-deformable, breaking or non-breaking | H, Delta, slope, K_D | K_D from SPM 1977/1984 table (2.0-4.0 for 2-layer rough quarry stone, trunk). Check K_D against the original tables. | [VM12] slides 5-6; [HU] not verified |
| van der Meer H_s/(Delta D_n50) = 6.2 P^0.18 (S/sqrt N)^0.2 xi_m^(-0.5) (plunging) | rock, deep water | H_s, T_m, slope, D_n50, S, N, P | 6.2, 0.18, 0.2, -0.5 standard; check P values (slide 16) and transition | [VM12] slide 17; [VDM88] not verified |
| van der Meer surging form (c_s = 1.0) | rock, surging | as above | c_s, exponent on xi_m, sqrt(cot alpha): OCR-garbled; check | [VM12] slide 17; [VDM88] |
| Wouters N_s = H_s / (Delta D) = C_w / sqrt(xi_0) | GSC, slope | H_s, T, slope, D, rho_GSC | C_w NOT AVAILABLE | [DO12] Eq. 1; [WO98] not held |
| Recio & Oumeraci Eqs. 7-9 | GSC sliding, overturning, container weight | u, du/dt, C_D, C_L, C_M, K factors, mu = 0.48 | K factors and C_D, C_L, C_M NOT AVAILABLE | [CO22] Eqs. 7-9 (secondary to [RO09]) |
| BELWF critical SI (Eq. 3 and Eq. 5) | any impermeable submerged structure, before breaking | F_y, F_z, F_g, F_b, F_c | no empirical coefficients; code not released | [BD23] |

---

## 6. Discrepancies and unverified items

1. Drimer paper year: [BD23] is dated 2023 (published 17 January 2023). Lior's notes say "2026". No 2025/2026 Drimer geotube paper found. Confirm with Lior.
2. Hudson citation: [CO22] ref. 38 gives "Hudson, R. ... J. Waterw. Harb. Div. 1956, 93-118". [DO12] calls it "Hudson's formula (1956)". [VM12] does not give the year on the slide. From memory, the standard citation is 1959, vol. 85 (WW3), pp. 93-121. Verify before citing.
3. van der Meer 1988: the full thesis title and the DHL publication number are from memory. The sources only say "van der Meer 1988".
4. Surging coefficient: the OCR in [VM12] slide 17 gives "10" where the standard value is c_s = 1.0. Check against [VDM88].
5. [CO22] Eq. 7: the numerator and denominator are partly garbled in the text layer. The reading above is from the extracted text and is not confirmed visually. Check against [RO09].
6. [BD23] force units: the paper plots "F (KN)" (Fig. 11), but does not say whether forces are per metre of tube, per 2-D flume unit width, or total for the two-tube structure. Assume per metre of tube length for compute work and state it as an ASSUMPTION.
7. [BD23] water density is not stated. Any calculation needs an assumed rho (1025 kg/m^3 seawater, ASSUMPTION).
8. [BD23] Iribarren 0.17 is called the "spilling" range (p.10), but the paper also says the tube makes a plunging breaker. Do not use the 0.17 label for breaker type in the paper without this caveat.
9. Fig. 11 values are read by eye from a rendered page and are approximate (about +/- 0.03 on SI).
10. [BD23] Fig. 6 (critical SI vs wave height) values were not extracted.
11. [VF] year and venue not on the PDF's first page.
12. [CO22] DOI not extracted.
13. Related but not Drimer: [LI25] Liu et al. 2025 (rubble-mound core slip under solitary waves, factor-of-safety method, CC BY). A possible lead for the rock-core part of the materials section. Also a search result (not opened) names Aristodemo & Filianoti (2022, Coastal Engineering) on sliding and overturning of submerged rigid breakwaters under solitary waves. Not verified; do not cite without opening it.

---

## 7. Asks and next steps

For Lior (decision or source needed):
- Confirm the "2026 Drimer" paper: title, DOI or journal. If it exists and is not indexed here, upload the PDF to "new uploads from lior/". Otherwise the paper will use [BD23] (2023) as the Drimer model and say so.
- Ask whether he can get the BELWF code from Drimer or Bar (corresponding author Drimer, nitaid@technion.ac.il, per [BD23] p.1). This is a request by e-mail, which only Lior may send.
- Recio & Oumeraci 2009 (Coastal Eng. 56, 632-658) needs institutional access to get the K factors and C_D, C_L, C_M. Ask Lior for library access or a copy.
- Hudson 1959 and van der Meer 1988 originals are needed to confirm K_D, the surging coefficient and P values.

For the compute agent (no further searches needed for these):
- Evaluate Eqs. 3 and 5 for any force history given, with the units in section 4.3.
- Evaluate xi_0 and N_s for each reef in 08_paper/data/reefs.json once slope, H, T and D are available.
- Hudson and van der Meer give rock sizes only when K_D, P, S, N are fixed. State which values were used.

---

## 8. Files

- This note: /home/user/artificial-reef-survey/08_paper/notes/drimer_force_model.md
- Scratch (not in repo): /tmp/claude-0/paper/drimer/ (bar_nolayout.txt, dasspg-02.png, dass_eq1.png, p10-10.png, p11-11.png, p13-13.png, p19-19.png, p07-07.png, src1.pdf to src5.pdf, jmse13_01940.pdf, verhagen2012_ch7.txt, corvaro.txt, dass.txt).
- Not touched: 04_build/, papers/, "new uploads from lior/", "Initial info from Lior/", 07_scale/ (all read only, and only the Lior file was read).
- No other file in 08_paper/ was created or modified. The other agent's drimer_2026_forces.md did not exist when this note was written. Cross-link if it appears.

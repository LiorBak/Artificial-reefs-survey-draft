#!/usr/bin/env python3
"""wavelib.py - wave and structure formulas used by the 08_paper analysis (one place, each with its source).

Every function names the formula it implements and the source key; full references are in REFS below and in RESULTS.md.
Verification status of each source (read in this project or not) is in REFS[key]['status'].
SI units throughout (m, s, kg, N). Linear (Airy) wave theory unless stated.
"""
import math

import numpy as np

G = 9.81          # m/s2 (ASSUMPTION, standard)
RHO_W = 1025.0    # kg/m3 sea water (ASSUMPTION, standard; [BD23] does not state it)

REFS = {
    'Airy': dict(cite='Linear (Airy) wave theory; dispersion w^2 = g k tanh(kh), group velocity and energy-flux shoaling. Standard textbook result (e.g. Dean & Dalrymple 1991, Water Wave Mechanics for Engineers and Scientists, World Scientific).',
                 status='textbook; not re-read in this project'),
    'McCowan1894': dict(cite='McCowan, J. (1894). On the highest wave of permanent type. Philosophical Magazine, Series 5, 38, 351-358.',
                        status='not read; value 0.78 read in Weggel (1972) eq. 6 p.420 by the literature agent; title/volume conflict noted in 08_paper/lit/LITERATURE.md D-3'),
    'Weggel1972': dict(cite='Weggel, J.R. (1972). Maximum breaker height for design. Proceedings of the 13th International Conference on Coastal Engineering, Vancouver, ASCE, Chapter 21, 419-432. doi:10.9753/icce.v13.21',
                       status='equations 9-11 p.421 read by the literature agent (08_paper/lit/LITERATURE.md s3.5); a = 1.36(1-e^-19m) s2/ft = 43.75(1-e^-19m)/g in SI; used as a sensitivity only'),
    'Battjes1974': dict(cite='Battjes, J.A. (1974). Surf similarity. Proceedings of the 14th International Conference on Coastal Engineering, Copenhagen, ASCE, 466-480.',
                        status='breaker-type limits at the break point (xi_b < 0.4 spilling, 0.4-2.0 plunging, > 2.0 surging) read in Lewis, Hunt & Evans (2015) Table 1 p.5 (after SPM 1977; Galvin 1968)'),
    'Lewis2015': dict(cite='Lewis, J., Hunt, S. and Evans, T. (2015). Quantification of surfing amenity for beach value and management. NSW Coastal Conference 2015 (paper, 23 pp.). https://www.coastalconference.com/2015/papers2015/James%20Lewis.pdf (accessed 2026-10-15).',
                      status='read (PDF in scratch); Table 1 p.5 breaker types, Table 3 p.15 Hutt et al. (2001) skill table'),
    'Hutt2001': dict(cite='Hutt, J.A., Black, K.P. and Mead, S.T. (2001). Classification of surf breaks in relation to surfing skill. Journal of Coastal Research, Special Issue 29, 66-81.',
                     status='original not read; table values read in two reproductions: Lewis et al. (2015) Table 3 p.15 and Barlow (2013) Table 1.1 p.12; they agree'),
    'Barlow2013': dict(cite='Barlow, M. (2013). The effects of anthropometrical, physiological and environmental factors on surfing performance. PhD thesis, Leeds Metropolitan University. https://eprints.leedsbeckett.ac.uk/id/eprint/592/ (accessed 2026-10-15).',
                       status='read (Table 1.1 p.12, Hutt skill rating)'),
    'MeadBlack2001': dict(cite='Mead, S.T. and Black, K.P. (2001). Predicting the breaking intensity of surfing waves. Journal of Coastal Research, Special Issue 29, 51-65 (page range conflict 51-65 vs 103-130, LITERATURE.md D-1). Reproduced as Chapter 6 of Mead (2000) PhD thesis (see Mead2000).',
                          status='read in Mead (2000) Ch.6: Eq. 6.5 Y = 0.065 X + 0.821 (R2 = 0.71), X = orthogonal seabed gradient as horizontal distance per unit vertical, printed p.115 (PDF p.138); Table 6.2 intensity classes printed p.121 (PDF p.144); also Scarfe et al. (2003) p.4 Eq. 1'),
    'Mead2000': dict(cite='Mead, S.T. (2000). Incorporating High-Quality Surfing Breaks into Multi-Purpose Reefs. PhD thesis, University of Waikato, Hamilton, New Zealand (title page dated 2000). https://researchcommons.waikato.ac.nz/handle/10289/13967 (accessed 2026-10-15).',
                     status='read (PDF 25 MB in scratch); Ch.3 ramp function printed p.53-54; Ch.6 vortex ratio'),
    'Scarfe2003': dict(cite='Scarfe, B.E., Elwany, M.H.S., Mead, S.T. and Black, K.P. (2003). The science of surfing waves and surfing breaks - a review. Scripps Institution of Oceanography Technical Report, eScholarship qt6h72j1fz.',
                       status='read (Eq. 1 p.4; peel angle / manoeuvre text p.5-6)'),
    'dAngremond1996': dict(cite="d'Angremond, K., van der Meer, J.W. and de Jong, R.J. (1996). Wave transmission at low-crested structures. Proceedings of the 25th International Conference on Coastal Engineering, Orlando, ASCE, 2418-2427.",
                           status="original not read; equations read in Blacka et al. (2013) Eqs. 25-27 p.15 (PDF p.27). Blacka prints exp(+0.5 xi) and a positive Rc term in Eq. 26: typographical; the standard form with exp(-0.5 xi) and -0.4 Rc/Hi is used here"),
    'Briganti2003': dict(cite='Briganti, R., van der Meer, J.W., Buccino, M. and Calabrese, M. (2003). Wave transmission behind low-crested structures. Proceedings of Coastal Structures 2003, ASCE, 580-592 (summarised in Burcharth et al. 2007).',
                         status='original not read; wide-crest equation read in Blacka et al. (2013) Eq. 29 p.16 (PDF p.28). Validity bounds (0.05 <= Kt <= 0.93 - 0.006 B/Hi) are as commonly quoted from van der Meer et al. (2005), not verified here'),
    'Blacka2013': dict(cite='Blacka, M.J., Shand, T.D., Carley, J.T. and Mariani, A. (2013). A Review of Artificial Reefs for Coastal Protection in NSW. WRL Technical Report 2012/08, UNSW Water Research Laboratory. doi:10.4225/53/58e1dc7368c7a.',
                       status="read (Lior's papers/ folder)"),
    'BlackAndrews2001': dict(cite='Black, K.P. and Andrews, C.J. (2001). Natural and artificial reefs for surfing and coastal protection: salients and tombolos. Journal of Coastal Research, Special Issue 29, 82-93.',
                             status='original not read; criteria and Eqs. 30-31 read in Blacka et al. (2013) p.21 (PDF p.33) incl. Fig. 2.7'),
    'Ranasinghe2006': dict(cite='Ranasinghe, R., Turner, I.L. and Symonds, G. (2006). Shoreline response to multi-functional artificial surfing reefs: a numerical and physical modelling study. Coastal Engineering 53, 589-611.',
                           status='original not read; Sa/SZW thresholds read in Blacka et al. (2013) p.22-23 (PDF p.34-35), Fig. 2.9'),
    'Hudson1959': dict(cite='Hudson, R.Y. (1959). Laboratory investigation of rubble-mound breakwaters. Journal of the Waterways and Harbors Division, ASCE, 85(WW3), 93-121.',
                       status='NOT VERIFIED (sources disagree on year/pages, see 08_paper/notes/drimer_force_model.md s6); formula and K_D from Verhagen (2012) slides 5-6'),
    'Verhagen2012': dict(cite='Verhagen, H.J. (2012). CT5308 Breakwaters and Closure Dams, Ch. 7 Stability of randomly placed rock mounds. TU Delft lecture notes. https://ocw.tudelft.nl/wp-content/uploads/ct530807.pdf',
                         status='read by the Drimer agent (08_paper/notes/drimer_force_model.md s5.1)'),
    'vanSteeg2011': dict(cite='van Steeg, P., Vastenburg, E., Bezuijen, A., Zengerink, E. and de Gijt, J. (2011). Large-scale physical model tests on sand-filled geotextile tubes and containers under wave attack. Coastal Structures 2011 (extended abstract, 2 pp.). https://repository.tudelft.nl/file/File_6363c965-0635-4e41-9e96-1dde8ce20c3b (accessed 2026-10-15).',
                         status='read; Eq. (1) p.2: chi Hs / (Delta sqrt(B D) (f cos a + sin a)) <= 0.65; tests Hs <= 1.5 m, s0p = 0.03, failure mode sliding'),
    'BD23': dict(cite='Bar, D. and Drimer, N. (2023). Preliminary design tools for hydrodynamic aspects of submerged impermeable breakwaters. Journal of Marine Science and Engineering 11(2), 236. https://doi.org/10.3390/jmse11020236',
                 status="read by the Drimer agent (08_paper/notes/drimer_force_model.md s4); local copy in 'Initial info from Lior/'"),
    'Wouters1998': dict(cite='Wouters, J. (1998). Open taludbekledingen; stabiliteit van geosystems (Delft Hydraulics report H1930), as cited in Dassanayake & Oumeraci (2012) Eq. 1.',
                        status='original not held; Ns definition only (C_w not available)'),
    'SPM1984': dict(cite='U.S. Army Corps of Engineers (1984). Shore Protection Manual, 4th ed., CERC, Vicksburg; and USACE (2002) Coastal Engineering Manual EM 1110-2-1100 Part III Ch. 2 (CERC formula, K = 0.39 with Hs, kappa = 0.78, n = 0.4).',
                    status='CEM Part III Ch.2 read by the literature agent (LITERATURE.md s3.12); dimensionally consistent form used here: Q = K sqrt(g) Hb^2.5 sin(2 theta_b) / (16 sqrt(kappa) (s-1)(1-n)); order of magnitude only'),
    'Zviely2007': dict(cite='Zviely, D., Kit, E. and Klein, M. (2007). Longshore sand transport estimates along the Mediterranean coast of Israel in the Holocene. Marine Geology 238, 61-73.',
                       status='read by the Israel dossier agent (02_research/israel/haifa-bay-sediment-budget.md R1)'),
    'Zviely2009': dict(cite='Zviely, D., Kit, E., Rosen, B., Galili, E. and Klein, M. (2009). Shoreline migration and beach-nearshore sand balance over the last 200 years in Haifa Bay (SE Mediterranean). Geo-Marine Letters 29, 93-110.',
                       status='read by the Israel dossier agent (02_research/israel/haifa-bay-sediment-budget.md R2)'),
    'Rosen2001': dict(cite='Rosen, D.S. (2001). A review of sea level monitoring status in Israel. IOLR / GLOSS report. https://gloss-sealevel.org/sites/gloss/files/publications/documents/israel_2001.pdf',
                      status='read by the Israel dossier agent (02_research/israel/israel-wave-climate-and-tides.md R1): spring range ~0.4 m, neap ~0.15 m'),
    'LiorBuoy2025': dict(cite="Bakalo, L. (2025). Sea level measures for minimum 'surfable' waves; Shikmona buoy readings 27 Jul - 15 Aug 2025 (unpublished field notes, 'Initial info from Lior/suggestions illustration and some initial height measurment of surable swells.pdf'), summarised in 01_source_notes/lior_suggestions_and_swell_heights.md.",
                         status="author's own field data"),
}

BREAKER_TYPES = [(0.4, 'spilling'), (2.0, 'plunging'), (float('inf'), 'surging/collapsing')]   # Battjes 1974 via Lewis 2015 Table 1

# Mead (2000) Table 6.2 (printed p.121): vortex ratio ranges -> breaking intensity class
VORTEX_CLASSES = [
    (1.6, 'beyond extreme (Y < 1.6): likely to collapse, unsurfable for stand-up surfing (Mead 2000 p.121)'),
    (1.905, 'extreme (1.6-1.9: square, spitting; e.g. Pipeline, Shark Island)'),
    (2.205, 'very high (1.91-2.2: very hollow; e.g. Kirra Point, Off-The-Wall)'),
    (2.505, 'high (2.21-2.5: pitching, hollow; e.g. Bells Beach, Bingin)'),
    (2.805, 'medium/high (2.51-2.8: some tube sections; e.g. Manu Bay)'),
    (3.105, 'medium (2.81-3.1: steep faced but rarely tubing; e.g. Whangamata)'),
    (float('inf'), 'below medium (Y > 3.1): gentle plunging / spilling, surfable but not high quality (Mead 2000 p.121)'),
]
VORTEX_SHORT = ['beyond_extreme', 'extreme', 'very_high', 'high', 'medium_high', 'medium', 'gentle']

# Hutt et al. (2001) skill table, as reproduced in Lewis et al. (2015) Table 3 p.15 and Barlow (2013) Table 1.1 p.12
# rating: (peel angle limit deg or None = 'not reached', min Hb m, max Hb m (inf = '>4.0'), description)
HUTT = {
    1: (90.0, 0.70, 1.00, 'beginner, not yet able to ride the face; moves forward as the wave advances'),
    2: (70.0, 0.65, 1.50, 'learner, rides laterally along the crest'),
    3: (60.0, 0.60, 2.50, 'generates speed by pumping'),
    4: (55.0, 0.55, 4.00, 'begins to execute standard manoeuvres on occasion'),
    5: (50.0, 0.50, float('inf'), 'executes standard manoeuvres consecutively on a single wave'),
    6: (40.0, 0.45, float('inf'), 'standard manoeuvres consecutively, advanced manoeuvres on occasion'),
    7: (29.0, 0.40, float('inf'), 'top amateur, consecutive advanced manoeuvres'),
    8: (27.0, 0.35, float('inf'), 'professional, consecutive advanced manoeuvres'),
    9: (None, 0.30, float('inf'), 'top 44 professional (peel limit not reached)'),
    10: (None, 0.30, float('inf'), 'surfers of the future (peel limit not reached)'),
}


# ----------------------------------------------------------------------------------------------- linear wave theory
def L0(T):
    """Deep-water wavelength L0 = g T^2 / (2 pi) [Airy]."""
    return G * np.asarray(T, float) ** 2 / (2 * math.pi)


def wavenumber(T, h):
    """Solve w^2 = g k tanh(k h) for k (vectorised; Newton from the Eckart/Fenton start) [Airy]. h <= 0 -> nan."""
    T = np.asarray(T, float)
    h = np.asarray(h, float)
    w = 2 * math.pi / T
    hh = np.where(h > 1e-6, h, np.nan)
    k0 = w ** 2 / G
    k = k0 / np.sqrt(np.tanh(k0 * hh))          # Eckart-type first guess
    for _ in range(30):
        th = np.tanh(k * hh)
        f = G * k * th - w ** 2
        df = G * th + G * k * hh * (1 - th ** 2)
        k = k - f / df
    return k


def wavelength(T, h):
    return 2 * math.pi / wavenumber(T, h)


def celerity(T, h):
    k = wavenumber(T, h)
    return (2 * math.pi / np.asarray(T, float)) / k


def group_velocity(T, h):
    k = wavenumber(T, h)
    hh = np.asarray(h, float)
    kh = k * hh
    n = 0.5 * (1 + 2 * kh / np.sinh(2 * kh))
    return n * (2 * math.pi / np.asarray(T, float)) / k


def shoaling_coefficient(T, h):
    """Ks = sqrt(cg0 / cg(h)), cg0 = g T / (4 pi); normal incidence, no refraction or friction [Airy]."""
    cg0 = G * np.asarray(T, float) / (4 * math.pi)
    return np.sqrt(cg0 / group_velocity(T, h))


# ----------------------------------------------------------------------------------------------- breaking
def gamma_weggel(m, Hb, T):
    """Weggel (1972) breaker index gamma_b = b - a Hb/(g T^2), a = 43.75(1 - e^-19m), b = 1.56/(1 + e^-19.5m).
    m = bed slope (tan). Calibrated for m <= 0.1; larger m is EXTRAPOLATION (flagged by the caller)."""
    m = max(float(m), 1e-4)
    a = 43.75 * (1 - math.exp(-19 * m))
    b = 1.56 / (1 + math.exp(-19.5 * m))
    return b - a * Hb / (G * T ** 2)


def breaker_type(xi_b):
    """Battjes (1974) breaker type from the break-point surf similarity xi_b = tan(beta) / sqrt(Hb / L0)."""
    if xi_b is None or not np.isfinite(xi_b):
        return None
    for lim, name in BREAKER_TYPES:
        if xi_b < lim:
            return name
    return BREAKER_TYPES[-1][1]


def iribarren(tan_beta, H, T):
    """xi = tan(beta) / sqrt(H / L0) (Battjes 1974)."""
    return float(tan_beta) / math.sqrt(H / float(L0(T)))


def vortex_ratio(tan_beta_orth):
    """Mead & Black (2001) / Mead (2000) Eq. 6.5: Y = 0.065 X + 0.821, X = 1 / tan(beta) (horizontal per unit vertical,
    along the wave orthogonal). Data range of the fit: Y 1.42-3.43, i.e. X about 9-40 (Mead 2000 p.115)."""
    X = 1.0 / max(float(tan_beta_orth), 1e-6)
    return 0.065 * X + 0.821, X


def vortex_class(Y):
    for i, (lim, txt) in enumerate(VORTEX_CLASSES):
        if Y < lim:
            return VORTEX_SHORT[i], txt
    return VORTEX_SHORT[-1], VORTEX_CLASSES[-1][1]


# ----------------------------------------------------------------------------------------------- peel angle / skill
def peel_angle_snell(phi0_deg, T, h0, hb):
    """Peel angle at breaking from the angle phi0 between the incident wave crest and a straight reef arm (whose flank
    contours run parallel to the arm), by Snell's law between depth h0 (arm toe) and breaking depth hb:
    sin(alpha_b) = sin(phi0) * C(hb) / C(h0). DERIVED method (straight parallel contours along the arm flank,
    no diffraction); the crest turns toward the arm, so alpha_b <= phi0."""
    c0 = float(celerity(T, h0))
    cb = float(celerity(T, hb))
    s = math.sin(math.radians(phi0_deg)) * cb / c0
    return math.degrees(math.asin(min(1.0, s)))


def hutt_min_rating(alpha_deg, Hb=None):
    """Lowest Hutt et al. (2001) rating able to ride a wave peeling at alpha (alpha >= the rating's peel limit), and
    whether Hb lies in that rating's height range. Ratings 9-10 have no peel limit ('not reached')."""
    for r in range(1, 9):
        lim, hmin, hmax, _ = HUTT[r]
        if alpha_deg >= lim:
            ok = None if Hb is None else (hmin <= Hb <= hmax)
            return r, ok
    return 9, (None if Hb is None else Hb >= HUTT[9][1])


def peel_rate(T, hb, alpha_deg):
    """Down-the-line peel speed Vp = C_b / sin(alpha) (Hutt et al. 2001 definition, linear C at the break depth)."""
    return float(celerity(T, hb)) / max(math.sin(math.radians(alpha_deg)), 1e-6)


# ----------------------------------------------------------------------------------------------- transmission
def kt_dangremond(Rc, Hi, B, tan_a, T, permeable=True):
    """d'Angremond et al. (1996): Kt = -0.4 Rc/Hi + c (B/Hi)^-0.31 (1 - exp(-0.5 xi)), c = 0.64 permeable / 0.80
    impermeable; xi = tan(a)/sqrt(Hi/L0p). Bounds 0.075 <= Kt <= 0.80 (as commonly applied). Rc < 0 = submerged."""
    xi = iribarren(tan_a, Hi, T)
    c = 0.64 if permeable else 0.80
    kt = -0.4 * Rc / Hi + c * (B / Hi) ** -0.31 * (1 - math.exp(-0.5 * xi))
    return float(min(0.80, max(0.075, kt))), xi


def kt_briganti(Rc, Hi, B, tan_a, T):
    """Briganti et al. (2003) wide-crest form (B/Hi > 10): Kt = -0.35 Rc/Hi + 0.51 (B/Hi)^-0.65 (1 - exp(-0.41 xi)).
    Bounds 0.05 <= Kt <= 0.93 - 0.006 B/Hi (as quoted by van der Meer et al. 2005; not verified here)."""
    xi = iribarren(tan_a, Hi, T)
    kt = -0.35 * Rc / Hi + 0.51 * (B / Hi) ** -0.65 * (1 - math.exp(-0.41 * xi))
    upper = 0.93 - 0.006 * B / Hi
    return float(min(upper, max(0.05, kt))), xi


def kt_low_crested(Rc, Hi, B, tan_a, T, permeable=True):
    """Choose d'Angremond (B/Hi < 10) or Briganti (B/Hi >= 10), as recommended in Burcharth et al. (2007) via
    Blacka et al. (2013) p.16. Briganti is calibrated for permeable rubble mounds; for impermeable geotextile reefs it is
    applied as is (ASSUMPTION)."""
    if B / Hi < 10:
        kt, xi = kt_dangremond(Rc, Hi, B, tan_a, T, permeable)
        return kt, xi, 'dAngremond1996' + ('' if permeable else '_impermeable')
    kt, xi = kt_briganti(Rc, Hi, B, tan_a, T)
    return kt, xi, 'Briganti2003'


# ----------------------------------------------------------------------------------------------- shoreline response
def black_andrews(B, S):
    """Black & Andrews (2001) via Blacka et al. (2013) p.21: no change B/S < ~0.1, salient B/S < 2, tombolo B/S > 0.6
    (as printed; the ranges overlap). X_off/B = 0.5 (B/S)^-1.27 (Eq. 30), salient amplitude Y_off = S - X_off,
    basal width D_tot = Y_off / 0.125 (Eq. 31, +-0.02)."""
    r = B / S
    xoff = 0.5 * B * r ** -1.27
    yoff = max(0.0, S - xoff)
    dtot = yoff / 0.125 if yoff > 0 else 0.0
    if r < 0.1:
        mode = 'no change (B/S < 0.1)'
    elif r > 0.6:
        mode = 'tombolo possible (B/S > 0.6; salient range B/S < 2 overlaps)'
    else:
        mode = 'salient (0.1 < B/S < 0.6)'
    return dict(B_over_S=r, X_off_m=xoff, Y_off_m=yoff, D_tot_m=dtot, D_tot_range_m=(yoff / 0.145 if yoff else 0, yoff / 0.105 if yoff else 0), mode=mode)


def ranasinghe_mode(Sa, SZW):
    """Ranasinghe et al. (2006) via Blacka et al. (2013) p.22-23: Sa/SZW < 1 erosion likely; > 1.5 accretion likely,
    peaking near 2.0; 1-1.5 transitional."""
    r = Sa / SZW
    if r < 1.0:
        mode = 'erosion likely (Sa/SZW < 1)'
    elif r <= 1.5:
        mode = 'transitional (1 <= Sa/SZW <= 1.5)'
    else:
        mode = 'accretion likely (Sa/SZW > 1.5; peak near 2)'
    return r, mode


# ----------------------------------------------------------------------------------------------- stability
def hudson_weight(H, rho_r, cot_a, KD, rho_w=RHO_W):
    """Hudson: W = rho_r g H^3 / (Delta^3 K_D cot a), Delta = rho_r/rho_w - 1 (Verhagen 2012 slide 5). Returns mass (kg)
    W/g and Dn50 = (M/rho_r)^(1/3)."""
    D = rho_r / rho_w - 1
    Wn = rho_r * G * H ** 3 / (D ** 3 * KD * cot_a)
    M = Wn / G
    return M, (M / rho_r) ** (1 / 3)


def vansteeg_hs_crit(B, D, rho_fill, f=0.5, alpha_deg=0.0, chi=1.0, rho_w=RHO_W):
    """van Steeg et al. (2011) Eq. 1 rearranged: Hs_crit = 0.65 Delta sqrt(B D) (f cos a + sin a) / chi.
    Delta = (rho_tube - rho_w)/rho_w; f = tube-foundation friction (ASSUMPTION 0.5 unless given); chi = transmission
    reduction parameter (value not given in the abstract; chi = 1 is the conservative choice)."""
    Delta = rho_fill / rho_w - 1
    a = math.radians(alpha_deg)
    return 0.65 * Delta * math.sqrt(B * D) * (f * math.cos(a) + math.sin(a)) / chi


def ns_gsc(Hs, D, rho_fill, rho_w=RHO_W):
    """Stability number Ns = Hs / (Delta D) (Wouters 1998 as in Dassanayake & Oumeraci 2012 Eq. 1)."""
    return Hs / ((rho_fill / rho_w - 1) * D)


def cerc_q(Hb, theta_b_deg, K=0.39, rho_s=2650.0, porosity=0.4, gamma_b=0.78, rho_w=RHO_W):
    """CERC longshore transport (SPM 1984 Eq. 4-49, volumetric form with Hs and K = 0.39):
    Q = K sqrt(g/gamma_b) Hb^2.5 sin(2 theta_b) / (16 (s - 1)(1 - n))  [m3/s of in-place sand]."""
    s = rho_s / rho_w
    return K * math.sqrt(G / gamma_b) * Hb ** 2.5 * math.sin(math.radians(2 * theta_b_deg)) / (16 * (s - 1) * (1 - porosity))

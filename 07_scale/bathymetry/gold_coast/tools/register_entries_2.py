"""More catalogue entries (Narrowneck: Jackson 2007 Shore & Beach, Vieira da Silva 2021 Coastal Engineering AM)."""
from register_entries import add, f3d, NN, ANN

S = "narrowneck-gold-coast"
J07 = dict(
    cit="Jackson, L.A., Corbett, B., McGrath, J., Tomlinson, R. and Stuart, G. (2007). Narrowneck Reef: review of seven years of monitoring. Shore & Beach 75(4), 67-79 (Fall 2007), %s. Griffith Research Online copy, http://hdl.handle.net/10072/17995. Accessed 2026-10-06.",
    url="https://research-repository.griffith.edu.au/bitstreams/7e18bf60-76d6-5bdf-961d-6b572b099c70/download",
    page="http://hdl.handle.net/10072/17995",
    credit="Jackson et al. (2007) / ASBPA Shore & Beach; the paper does not credit individual figures (ICM, GCCC, Griffith)",
    lic="(c) The Author(s) 2007, reproduced on Griffith Research Online in accordance with the publisher's copyright policy (ASBPA); reuse not cleared")
V21 = dict(
    cit="Vieira da Silva, G., Hamilton, D., Strauss, D., Murray, T. and Tomlinson, R. (2021). Sediment pathways and morphodynamic response to a multi-purpose artificial reef - new insights. Coastal Engineering 171, 104027 (accepted manuscript), doi:10.1016/j.coastaleng.2021.104027, %s. Griffith Research Online, http://hdl.handle.net/10072/409362. Accessed 2026-10-06.",
    url="https://research-repository.griffith.edu.au/bitstreams/4627106e-ce70-46d1-aec3-c81b126fdd2c/download",
    page="http://hdl.handle.net/10072/409362",
    credit="Vieira da Silva et al. (2021) / Elsevier (accepted manuscript on Griffith Research Online); City of Gold Coast surveys; Google Earth / Esri base imagery",
    lic="CC BY-NC-ND 4.0 (accepted manuscript, Griffith Research Online rights statement); base imagery under its provider's terms")

ROWS = [
    ("narrowneck-gold-coast_jackson2007_fig2_narrowneck_reef_design_plan_elevation_section_1998_200dpi_crop.png", "design_drawing",
     "Jackson et al. 2007 Fig 2: Narrowneck reef design - plan view, elevation and cross-section A-A (ICM drawing)",
     "p.3 (PDF p.4), Fig 2 (low-resolution raster, rendered at 200 dpi)", "1998-1999 (original design drawing, survey of Jan 1999)",
     "ICM construction-approval drawing of the original two-arm (split V) reef: plan view of the arms on the seabed contours inside a 750 m grid, an elevation profile along the reef axis (flat crest then slope to about -10 m at 580 m) and the double-peaked cross-section A-A. Text and levels are not legible at this resolution.",
     True, "design (original 1998-99, before the 2004 weir and flared wings)", ["plan_trace", "3d_height_slopes", "cross_check"],
     "Shows the original design topology (two separate tapered arms, no weir, no flared wings) and the profile shape along the arm; no numbers legible. The tracer must NOT use this planform for the renewed reef (see Jackson 2012 Fig 2 right). Goes to REPORT.md section 6.",
     "GC-N25", f3d(True, "Which design version the traced outline matches: original split-V (this figure) vs 2004 revised (flared wings + weir)", ["planform"]), []),
    ("narrowneck-gold-coast_jackson2007_fig13_recorded_surf_tracks_on_revised_design_contours_scale_100m_300dpi_crop.png", "plan_figure",
     "Jackson et al. 2007 Fig 13: plot of recorded surf tracks on the revised design contours, with a 0-100 m scale bar",
     "p.11 (PDF p.12), Fig 13 (raster, rendered at 300 dpi)", "surf tracks 2001-2006; contours of the revised (2004) design",
     "Plan of the revised Narrowneck design contours (North Reef and South Reef with flared wings and the weir channel between them), the approximate beach line and GPS surf tracks, with a 0-100 m scale bar. No contour labels.",
     True, "design contours (revised 2004) with surf tracks", ["plan_trace", "scale", "cross_check"],
     "The only metric scale found for the revised-design planform: scale bar calibrated at about 4.25 px/m (0.234 m/px) in the 300 dpi crop (annotated copy). Goes to REPORT.md section 6: scale Jackson 2012 Fig 2 right to this.",
     "GC-N26", f3d(True, "Planform dimensions of the revised design (arm lengths, weir channel width) vs the traced shape, using the 100 m bar", ["planform"]),
     [ANN + r"\narrowneck_jackson2007_fig13_scale_calibration_100m.png"]),
    ("narrowneck-gold-coast_jackson2007_fig14_photo_of_break_with_crest_at_minus0.5m_LAT_200dpi_crop.png", "photo",
     "Jackson et al. 2007 Fig 14: photo of break with crest at -0.5 m LAT (two photos)",
     "p.11 (PDF p.12), Fig 14 (raster, 200 dpi crop)", "2000-2001 (crest at -0.5 m LAT, before the top-up)",
     "Two photographs of a hollow breaking wave over the shallow reef crest (crest at -0.5 m LAT, i.e. RL -1.5 m AHD), the wave sucking dry at the break point.",
     True, "as-built crest -0.5 m LAT (c. 2000-01)", ["context", "3d_crest"],
     "Evidence for the as-built crest (-0.5 m LAT = RL -1.5 m AHD) and its hazardous break; the crest was later lowered. Context for REPORT.md section 6 (crest history).",
     "GC-N27", f3d(False, "None (history of the crest level)", []), []),
    ("narrowneck-gold-coast_jackson2007_fig15_photo_of_break_with_crest_at_minus1.5m_LAT_200dpi_crop.png", "photo",
     "Jackson et al. 2007 Fig 15: underwater photo of a person standing on the reef crest at -1.5 m LAT",
     "p.12 (PDF p.13), Fig 15 (raster, 200 dpi crop)", "2002 flume test / site observation (date not stated)",
     "Underwater photograph of a person standing on the algae-covered geotextile crest, head and torso above the surface, giving a water depth of about 1 m over a crest at -1.5 m LAT (text: about 1 m at -1.5 m LAT, about 0.3 m at -1 m LAT).",
     True, "as-maintained crest about -1.5 m LAT (c. 2002)", ["context", "3d_crest"],
     "The text gives about 1 m depth over the crest at the target crest of -1.5 m LAT (RL -2.5 m AHD); a person's height gives a rough check only. Goes to REPORT.md section 6.",
     "GC-N28", f3d(False, "None (qualitative check of about 1 m depth over the lowered crest)", []), []),
    ("narrowneck-gold-coast_vieira_da_silva2021_fig1_study_area_eta_lines_and_reef_native.jpeg", "plan_figure",
     "Vieira da Silva et al. 2021 Fig 1: study area - Narrowneck aerial, wave model grids, ETA survey lines 50-79",
     "Fig 1 (embedded raster, native resolution)", "figure 2021; base imagery undated",
     "Four panels: Australia locator, Google Earth view of Narrowneck with the reef ringed, regional wave grid, and the local grid with the City's ETA survey lines (ETA 50 to ETA 79) and a zoom on the reef with instrument positions (2019 ADCPs/buoys, 2011 ADCP).",
     True, "site context; reef shown as an icon / ellipse", ["context", "scale"],
     "Locates the ETA beach-profile lines (ETA 63-70 span the Narrowneck survey area; the reef sits between ETA 67 and ETA 68) and the Gold Coast buoy; no depths. Goes to REPORT.md section 4 (ETA lines).",
     "GC-N29", f3d(False, "None", []), []),
    ("narrowneck-gold-coast_vieira_da_silva2021_fig3_ten_topo_bathymetric_surveys_2018-2020_native.jpeg", "survey_plot",
     "Vieira da Silva et al. 2021 Fig 3: ten topo-bathymetric surveys of Narrowneck, 19 July 2018 - 23 April 2020 (ETA 63-70)",
     "Fig 3 (embedded raster, native resolution)",
     "surveys 2018-07-19, 2018-08-02, 2018-08-17, 2018-09-12, 2018-12-12, 2019-03-23, 2019-06-14, 2019-07-24, 2019-12-05, 2020-04-23",
     "Ten colour-ramp (-10 to +8 m) topo-bathymetric maps with labelled 1 m contours from the dune to the -10 m contour between ETA 63 and ETA 70 on aerial imagery, with the reef (dotted ellipse, dense contours from container clutter). Sub-tidal data from City of Gold Coast single-beam echo-sounder + RTK-GPS, 2x2 m grid.",
     True, "as renewed (surveys start one month after the June 2018 renewal)", ["3d_seabed", "cross_check", "scale"],
     "Contour labels read for survey 1 (annotated copy): inshore trough -2/-3, reef inner edge -4/-5, reef body -6 to -8, seaward -9/-10 m (AHD per the text). The only published depth picture of the renewed reef's seabed; the survey is single-beam (not multibeam) and the reef is blurred.",
     "GC-N30", f3d(True, "Seabed around the reef and crest/toe depths: inner edge about -4/-5 m and reef body -6 to -8 m AHD (+-1 m, read by eye); compare with the tracer's/3D model's depth if one is built", ["seabed", "crest_z"]),
     [ANN + r"\narrowneck_vieira2021_fig3_survey1_2018-07-19_depth_labels_read.png"]),
]
for _f, _k, _t, _pf, _dt, _sh, _vis, _st, _us, _how, _gc, _ff, _ann in ROWS:
    _src = J07 if "jackson2007" in _f else V21
    add(S, NN + "\\" + _f, kind=_k, title=_t, cit=_src["cit"] % _pf, url=_src["url"], page=_src["page"], pf=_pf, date=_dt,
        credit=_src["credit"], lic=_src["lic"], shows=_sh, vis=_vis, state=_st, used=_us, how=_how, ann=_ann, gc=_gc, f3d=_ff)

"""Catalogue of the images found by the Gold Coast gov/council/university report search (2026-10-06)."""
import os

ROOT = r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git"
REG = ROOT + r"\03_images\reefs"
WORK = ROOT + r"\07_scale\bathymetry\gold_coast"
NN = ROOT + r"\07_scale\shapes\narrowneck-gold-coast\src\gov"
PB = ROOT + r"\07_scale\shapes\palm-beach-gold-coast\src\gov"
ANN = WORK + r"\annotated"
TODAY = "2026-10-06"
BY = "gold_coast_gov_reports_bathymetry, 2026-10-06"
RIGHTS = "Private research copy; reuse rights to be checked before any public release."

JAC = dict(
    cit="Jackson, A., Tomlinson, R., Corbett, B. and Strauss, D. (2012). Long term performance of a submerged coastal control structure: a case study of the Narrowneck multi-functional artificial reef. Coastal Engineering Proceedings 1(33), structures.54 (Proc. 33rd International Conference on Coastal Engineering, Santander), doi:10.9753/icce.v33.structures.54, %s. https://icce-ojs-tamu.tdl.org/icce/article/view/6956. Accessed 2026-10-06.",
    url="https://icce-ojs-tamu.tdl.org/icce/article/download/6956/pdf",
    page="https://icce-ojs-tamu.tdl.org/icce/article/view/6956",
    credit="Jackson et al. (2012) / ICCE. The paper credits no individual figure; monitoring data and surveys are Gold Coast City Council, ICM and Griffith Centre for Coastal Management.",
    lic="ICCE OJS site carries a Creative Commons Attribution 4.0 (CC BY 4.0) badge; the 2012 record has no per-article rights statement - confirm before public release.")
HUNT = dict(
    cit="Hunt, S., Britton, G., Messiter, D., Prenzler, P., Knight, S. and Watterson, E. (2022). Palm Beach Shoreline Project: innovative coastal management solution. Coastal Engineering Proceedings 37 (ICCE 2022), management.66, doi:10.9753/icce.v37.management.66, %s. https://icce-ojs-tamu.tdl.org/icce/article/view/13024. Accessed 2026-10-06.",
    url="https://icce-ojs-tamu.tdl.org/icce/article/download/13024/12297",
    page="https://icce-ojs-tamu.tdl.org/icce/article/view/13024",
    credit="Hunt et al. (2022); photo credits not stated in the paper (City of Gold Coast project)",
    lic="CC BY 4.0 (article page, Copyright (c) 2023 the authors)")
PREN = dict(
    cit="Prenzler, P., Hunt, S., Elliott-Perkins, Z., Hamilton, D., Messiter, D., Wharton, C. and Watterson, E. (2022). Monitoring of the Palm Beach artificial reef. Coastal Engineering Proceedings 37 (ICCE 2022), structures.65, doi:10.9753/icce.v37.structures.65, %s. https://icce-ojs-tamu.tdl.org/icce/article/view/12921. Accessed 2026-10-06.",
    url="https://icce-ojs-tamu.tdl.org/icce/article/download/12921/12194",
    page="https://icce-ojs-tamu.tdl.org/icce/article/view/12921",
    credit="Prenzler et al. (2022); City of Gold Coast CCTV / aerial base not credited separately",
    lic="CC BY 4.0 (article page, Copyright (c) 2023 the authors)")
DAN = dict(
    cit="Daniels, R., Metters, D. and Ryan, J. (2022). Wave transformation over Palm Beach reef. Coastal Engineering Proceedings 37 (ICCE 2022), papers.63, doi:10.9753/icce.v37.papers.63, %s. https://icce-ojs-tamu.tdl.org/icce/article/view/12702. Accessed 2026-10-06.",
    url="https://icce-ojs-tamu.tdl.org/icce/article/download/12702/11975",
    page="https://icce-ojs-tamu.tdl.org/icce/article/view/12702",
    credit="Daniels, Metters and Ryan (2022), Queensland Government Department of Environment and Science",
    lic="CC BY 4.0 (article page, Copyright (c) 2023 the authors)")
MORT = dict(
    cit="Mortensen, S.B., Hibberd, W.J., Kaergaard, K., Kristensen, S.E., Deigaard, R. and Hunt, S. (2015). Concept design of a multipurpose submerged control structure for Palm Beach, Gold Coast Australia. Australasian Coasts & Ports Conference 2015, Auckland, %s. https://www.dhigroup.com/upload/publications/coastsea/Mortensen_2015.pdf. Accessed 2026-10-06.",
    url="https://www.dhigroup.com/upload/publications/coastsea/Mortensen_2015.pdf",
    page="https://www.dhigroup.com/upload/publications/coastsea/Mortensen_2015.pdf",
    credit="DHI Water & Environment / City of Gold Coast (Mortensen et al. 2015)",
    lic="not stated (conference paper hosted by DHI; copyright the authors / conference)")
Q1CIT = ("Gold Coast bathymetry search (2026). Overlay of (a) City of Gold Coast (2024) Gold Coast DTM Metadata raster "
         "(data.gov.au, CC BY 2.5 AU, zipped file geodatabase DTM_Metadata_Feb_2024_1m), (b) City of Gold Coast Contours MapServer, "
         "on (c) Esri World Imagery %s (private research copy). Accessed 2026-10-06. https://data.gov.au/data/dataset/digital-elevation-models-dem")
Q1URL = "https://data.gov.au/data/dataset/3f1698d1-3789-4dc5-af9d-0fb08f800d77/resource/3c077953-539c-422a-b3ed-64e06978204c/download/dtm_metadata.zip"
Q1PAGE = "https://data.gov.au/data/dataset/digital-elevation-models-dem"

E = []


def f3d(pending, what, vals):
    return {"pending": pending, "what_to_check": what, "model_values_affected": vals}


def add(slug, file, **kw):
    kw.update(slug=slug, file=file)
    kw.setdefault("ann", [])
    E.append(kw)


# ============================================================ Narrowneck
S = "narrowneck-gold-coast"
add(S, NN + r"\narrowneck-gold-coast_jackson2012_page3_200dpi_2012.png", kind="design_drawing",
    title="Jackson et al. 2012 p.3 (page render): Fig 2 reef levels original vs revised design, Fig 3 container placement schedule",
    cit=JAC["cit"] % "page 3 (Figs 2-3)", url=JAC["url"], page=JAC["page"],
    pf="p.3, Figs 2 and 3 (page rendered at 200 dpi from the PDF)",
    date="Fig 2 left: original design 1997-1999; Fig 2 right: final revised design 2004; Fig 3: 1998-2007 schedule",
    credit=JAC["credit"], lic=JAC["lic"],
    shows="Plan-view design contour drawings of the two Narrowneck arms: original design (labels -2 to -10) and the 2004 revised design with flared wings and central weir (crest contour -2.50, labels to -8.00), plus the cumulative container-count chart (450 by 2007). No scale bar, no north arrow.",
    vis=True, state="design (original 1999 and revised 2004)", used=["plan_trace", "3d_crest", "3d_height_slopes", "cross_check"],
    how="Read the contour labels of the revised 2004 design: crest-top -2.50, then -3.00 ... -5.0 every 0.5 m, -6.0, outer limit -8.00; original design labels -2 ... -10 (datum not stated in the paper; AHD from other sources). Annotated copy: 07_scale/bathymetry/gold_coast/annotated/narrowneck_jackson2012_fig2_design_depth_labels_read.png. Goes to REPORT.md section 6 (Narrowneck integration plan) for the tracer; shape.json untouched.",
    ann=[ANN + r"\narrowneck_jackson2012_fig2_design_depth_labels_read.png"], gc="GC-N01",
    f3d=f3d(True, "Tracer: compare the traced planform with the 2004 revised design (flared wings + central weir) in Fig 2 right; crest -2.50 vs adopted -2.5 AHD; confirm datum (AHD vs LAT) of the labels", ["planform", "crest_z", "seabed"]))
add(S, NN + r"\narrowneck-gold-coast_jackson2012_page4_200dpi_2012.png", kind="plan_figure",
    title="Jackson et al. 2012 p.4 (page render): Fig 4 maintenance placement plans 2002-2006, Fig 5 survey 9 June 2011 and isopach 2008-2011",
    cit=JAC["cit"] % "page 4 (Figs 4-5)", url=JAC["url"], page=JAC["page"], pf="p.4, Figs 4 and 5 (page rendered at 200 dpi)",
    date="Fig 4: plans 2002/03, 2004, 2006; Fig 5: survey 9 June 2011 (Gold Coast City Council) and comparison with 2008",
    credit=JAC["credit"], lic=JAC["lic"],
    shows="Plan views of the maintenance container placements on the design contours (2002/03 original planform; 2004 with flared wings and weir; 2006), and the 9 June 2011 hydrographic survey contours of the reef with the isopach 2008-2011 (raised/lowered seabed). Unlabelled colour/contour plots: no depth values, no scale bar.",
    vis=True, state="design + as-maintained (2002-2011)", used=["plan_trace", "cross_check", "context"],
    how="Confirms the design topology (two arms, weir channel, flared wings) and that GCCC surveyed the reef on 9 June 2011; no depth value can be read (no contour labels). Goes to REPORT.md section 6 as evidence that a 2011 survey exists (not published as data).",
    gc="GC-N02", f3d=f3d(True, "Tracer: planform of the traced reef vs the 2004 revised design outline in Fig 4/5 (arms, weir channel, flared wings)", ["planform"]))
add(S, NN + r"\narrowneck-gold-coast_jackson2012_page5_200dpi_2012.png", kind="aerial",
    title="Jackson et al. 2012 p.5 (page render): Fig 6 aerial photographs 2004 and 2011, Fig 7 July 2011 aerial overlaid with design contours and maintenance containers",
    cit=JAC["cit"] % "page 5 (Figs 6-7)", url=JAC["url"], page=JAC["page"], pf="p.5, Figs 6 and 7 (page rendered at 200 dpi)",
    date="Fig 6: 2004 and July 2011; Fig 7: July 2011", credit=JAC["credit"], lic=JAC["lic"],
    shows="Vertical aerial photos of Narrowneck Reef in 2004 and July 2011 (two arms of dark container patches, shore left, sea right) and the 2011 photo overlaid with the revised design contours and as-constructed maintenance containers (ICM).",
    vis=True, state="as-built/maintained (2004, 2011)", used=["plan_trace", "cross_check"],
    how="Fig 7 gives control between the 2004 revised design outline and the July 2011 aerial (no scale bar, no north arrow; georeference to Esri by matching container patches). Goes to REPORT.md section 6 as tracer input.",
    gc="GC-N03", f3d=f3d(True, "Tracer: georeference Fig 6b/7 to Esri and compare outline vs shape.json (planform, arm lengths, weir channel)", ["planform"]))

_b = NN + r"\narrowneck-gold-coast_jackson2012_"


def jn(file, kind, title, pf, date, shows, vis, state, used, how, gc, ff, ann=None):
    add(S, _b + file, kind=kind, title=title, cit=JAC["cit"] % pf, url=JAC["url"], page=JAC["page"], pf=pf, date=date,
        credit=JAC["credit"], lic=JAC["lic"], shows=shows, vis=vis, state=state, used=used, how=how, ann=ann or [], gc=gc, f3d=ff)


jn("fig2_reef_levels_original_and_revised_design_300dpi_crop.png", "design_drawing",
   "Jackson et al. 2012 Fig 2: Reef Levels - Original and Revised Design (crop)", "p.3, Fig 2 (crop of the vector figure rendered at 300 dpi)",
   "original design 1997-1999; revised design 2004",
   "Two contour plans: left the original design with labelled levels -2 to -10; right the final revised design (flared wings, central weir channel) with labelled levels -2.50 (crest top), -3.00 ... -6.0 and -8.00.",
   True, "design (original 1999 / revised 2004)", ["plan_trace", "3d_crest", "3d_height_slopes", "cross_check"],
   "Depth labels read and boxed in annotated/narrowneck_jackson2012_fig2_design_depth_labels_read.png: revised crest -2.50 (both arms), side contours every 0.5 m to -5.0, then -6.0 and -8.00 outer limit; datum not stated in the paper. Goes to REPORT.md section 6.",
   "GC-N04", f3d(True, "Revised-design planform (flared wings, weir) vs the traced shape; crest -2.50 vs 'adopted -1.5 AHD' claim in a search snippet; datum of labels", ["planform", "crest_z", "seabed"]),
   ann=[ANN + r"\narrowneck_jackson2012_fig2_design_depth_labels_read.png"])
jn("fig4_container_placement_plans_2002-2006_native.png", "plan_figure",
   "Jackson et al. 2012 Fig 4: placement of containers for reef maintenance (2002/03, 2004, 2006)", "p.4, Fig 4 (embedded raster, native resolution)", "2002-2006",
   "Three design-contour plans with the container placements of the 2002/03, 2004 (flared wings + weir) and 2006 campaigns, with the campaign table (10 + 15 + 17 = 42 containers).",
   True, "design + maintenance 2002-2006", ["plan_trace", "context"],
   "Shows when the 2004 modification (weir and flared wings) entered the planform; the numbers (42 containers in three campaigns) are already in the Narrowneck METHOD.md. Goes to REPORT.md section 6.",
   "GC-N05", f3d(True, "Planform: which design version (original vs 2004 with weir and flared wings) the traced outline represents", ["planform"]))
jn("fig5a_reef_bathymetry_2011-06-09_native.jpeg", "survey_plot",
   "Jackson et al. 2012 Fig 5a: Narrowneck reef bathymetry survey 9 June 2011", "p.4, Fig 5a (embedded raster)", "survey 2011-06-09",
   "Contour plot of the Gold Coast City Council hydrographic survey over the reef (coloured contour lines inside the revised design outline). No contour labels, scale or datum on the image.",
   True, "as-maintained (2011-06-09)", ["cross_check", "context"],
   "No depth value readable (contours unlabelled). Evidence that a 2011 GCCC reef survey exists and that its contours follow the revised-design outline. Goes to REPORT.md section 6.",
   "GC-N06", f3d(False, "None (unlabelled); request the survey from GCCC if depths are needed", ["seabed"]))
jn("fig5b_isopach_2008-2011_native.jpeg", "survey_plot",
   "Jackson et al. 2012 Fig 5b: isopach of changes to surveyed levels 2008-2011", "p.4, Fig 5b (embedded raster)", "2008-2011",
   "Isopach (difference map) of reef levels 2008 vs 2011: blue/red contours for lowered/raised seabed, with the revised design outline.",
   True, "as-maintained (2008-2011)", ["context"],
   "Context only: shows burial of the seaward containers (raised seabed on the outer reef) and 10 compromised containers; no values readable.",
   "GC-N07", f3d(False, "None", []))
jn("fig6a_aerial_2004_native.jpeg", "aerial",
   "Jackson et al. 2012 Fig 6 (left): aerial photograph of Narrowneck Reef, 2004", "p.5, Fig 6 left (embedded raster)", "2004 (month not stated)",
   "Vertical aerial of the two container arms (dark patches), scan with red cast; shore to the left.",
   True, "as-built/maintained (2004, after the weir modification)", ["plan_trace", "cross_check"],
   "Second aerial for the 2004 planform; no scale bar; usable by control-point matching to Esri. Goes to REPORT.md section 6.",
   "GC-N08", f3d(True, "Planform in 2004 vs shape.json (weir channel, flared wings)", ["planform"]))
jn("fig6b_aerial_2011-07_native.jpeg", "aerial",
   "Jackson et al. 2012 Fig 6 (right): aerial photograph of Narrowneck Reef, July 2011", "p.5, Fig 6 right (embedded raster)", "2011-07",
   "Clear vertical aerial of the two container arms in calm water, individual container patches visible; shore to the left, north up.",
   True, "as-maintained (July 2011; about 10 containers compromised since 2008)", ["plan_trace", "cross_check"],
   "Best pre-renewal aerial of the containers: tracer can trace the 2011 arm outlines by georeferencing to Esri (no scale bar). Goes to REPORT.md section 6.",
   "GC-N09", f3d(True, "Planform in July 2011 vs shape.json and vs the June 2018 renewal (previous vs amended shape)", ["planform"]))
jn("fig7_overlay_2011-07_aerial_with_design_contours_and_containers_native.jpeg", "aerial",
   "Jackson et al. 2012 Fig 7: July 2011 aerial overlaid with design contours and maintenance containers (ICM)", "p.5, Fig 7 (embedded raster)", "2011-07",
   "The July 2011 aerial with the revised design contours (white) and the as-constructed maintenance containers drawn on top: shows how the design planform sits on the actual container patches.",
   True, "as-maintained (July 2011) with 2004 revised design overlay", ["plan_trace", "cross_check"],
   "Control for aligning the design outline with the real patches (arm ends, weir channel). Goes to REPORT.md section 6 as the primary Narrowneck design-vs-real figure.",
   "GC-N10", f3d(True, "Planform: the traced outline should coincide with the white design contours of Fig 7 within the patch width", ["planform"]))
jn("fig1_left_exposed_boulder_wall_1996_native.jpeg", "photo",
   "Jackson et al. 2012 Fig 1 (left): exposed boulder wall at Narrowneck after the 1996 storms", "p.2, Fig 1 left (embedded raster)", "1996",
   "Narrowneck beach looking south after storm erosion in 1996: boulder wall exposed, no beach. The reef does not exist yet.",
   False, "pre-construction (1996)", ["context"], "Context for the reef's purpose; not used for geometry.", "GC-N11", f3d(False, "None", []))
jn("fig1_right_beach_looking_south_2011-08-24_native.jpeg", "photo",
   "Jackson et al. 2012 Fig 1 (right): Narrowneck beach looking south, 24 August 2011", "p.2, Fig 1 right (embedded raster)", "2011-08-24",
   "Widened Narrowneck beach 11 years after nourishment and reef construction; reef not visible.",
   False, "post-construction beach (2011)", ["context"], "Context only (beach width); not used for geometry.", "GC-N12", f3d(False, "None", []))
jn("fig8_failed_container_polyurethane_coating_native.jpeg", "report_photo",
   "Jackson et al. 2012 Fig 8: failed geotextile container with polyurethane coating (dive photo)", "p.6, Fig 8 (embedded raster)",
   "not stated (dive inspections 2000-2011)", "Underwater photo of a failed (torn) polyurethane-coated geotextile sand container on the reef.",
   True, "damaged container (date not stated)", ["context"], "Context: container condition; not used for geometry.", "GC-N13", f3d(False, "None", []))
jn("fig9_sketch_slumping_native.png", "diagram",
   "Jackson et al. 2012 Fig 9: conceptual sketch of slumping of stacked containers (T2 over T4)", "p.7, Fig 9 (embedded raster)", "2012 (sketch)",
   "Cross-section sketch of container layers: a T2 container on two T4 containers, used to explain slumping of the north reef when base containers fail. No scale or levels.",
   True, "diagram (not a survey)", ["context"],
   "Shows the layered stacking (T2 on T4 containers) that the tracer should know about; no dimensions here (container sizes must come from another source).",
   "GC-N14", f3d(True, "Container layer stacking (T2 on 2 x T4) for the renewal's added layer: reef height above seabed", ["height"]))
jn("fig10_container_propeller_damage_native.jpeg", "report_photo",
   "Jackson et al. 2012 Fig 10: container with evidence of propeller damage (dive photo)", "p.8, Fig 10 (embedded raster)", "not stated",
   "Underwater photo of a container cut by a propeller; evidence that boats pass over the crest.",
   True, "damaged container (date not stated)", ["context"],
   "Context only: shallow crest (boat strike), consistent with a crest only 1-1.5 m below low tide; no geometry.", "GC-N15", f3d(False, "None", []))
for _i, (_t, _tag) in enumerate([("a", "kelp (Ecklonia) on a container"), ("b", "red and brown algae on a container"),
                                  ("c", "Sargassum-type algae canopy"), ("d", "algae and fish on a container surface")]):
    jn("fig11%s_marine_species_on_reef_native.jpeg" % _t, "report_photo",
       "Jackson et al. 2012 Fig 11%s: marine species on the reef - %s" % (_t, _tag), "p.9, Fig 11%s (embedded raster)" % _t,
       "not stated (2011 condition survey)", "Underwater photo of marine growth on Narrowneck container surfaces (%s)." % _tag,
       True, "as-built reef ecology (c. 2011)", ["context"], "Context only (ecology); no geometry.", "GC-N%d" % (16 + _i), f3d(False, "None", []))
jn("fig12_narrowneck_beach_looking_south_2009-06-02_native.jpeg", "photo",
   "Jackson et al. 2012 Fig 12: Narrowneck beach looking south, 2 June 2009 (after the 2009 storms)", "p.10, Fig 12 (embedded raster)", "2009-06-02",
   "Eroded Narrowneck beach and scarped dune after the 2009 storm series, looking south; reef not visible.",
   False, "post-construction beach (2009)", ["context"], "Context only (storm response of the beach); no geometry.", "GC-N20", f3d(False, "None", []))
jn("fig16_salient_in_lee_of_reef_2010-05-20_native.png", "photo",
   "Jackson et al. 2012 Fig 16: salient in the lee of Narrowneck Reef, 20 May 2010 (two oblique camera views)", "p.13, Fig 16 (embedded raster)", "2010-05-20",
   "Two oblique shore-based camera views of the beach and the surf zone showing a salient/rip-bar pattern in the lee of the reef; the reef is a faint dark patch offshore.",
   True, "as-maintained (2010-05-20)", ["context", "camera_match"],
   "Context and possible camera-match target (Narrowneck webcam geometry unknown); no geometry read.", "GC-N21", f3d(False, "None", []))
add(S, ANN + r"\q1_narrowneck_dtm_source_coverage_on_esri.png", kind="diagram",
    title="Q1 evidence: City of Gold Coast DTM (source-ID raster) coverage and 1 m contours over Esri imagery at Narrowneck Reef",
    cit=Q1CIT % "2025-10-10", url=Q1URL, page=Q1PAGE,
    pf="annotated overlay generated by 07_scale/bathymetry/gold_coast/q1_dtm_evidence/q1_overlay.py",
    date="imagery 2025-10-10; DTM metadata raster modified 2024-05-13; overlay made 2026-10-06",
    credit="City of Gold Coast (DTM metadata, contours); Esri, Maxar, Earthstar Geographics (imagery); overlay by this project",
    lic="DTM metadata CC BY 2.5 AU; Esri imagery under Esri terms (private research copy)",
    shows="Narrowneck reef (dark arms) lies in a block of ocean where the City's DTM source raster has NO cell (cyan outlines); data blocks (yellow) stop at the beach; the City's 1 m contours there have minimum elevation 0 m AHD. Hence the DTM holds no depth at the reef.",
    vis=True, state="as-built, imagery 2025-10-10", used=["cross_check", "context"],
    how="Answers Q1 (DTM has no nearshore ocean depths): block (row 265, col 210) at the reef centre is absent; contours min 0 m AHD around the reef. Goes to REPORT.md section 2.",
    gc="GC-Q1N", f3d=f3d(False, "None: confirms no surveyed seabed in the City DTM at this reef", ["seabed"]))

# ============================================================ Palm Beach
S = "palm-beach-gold-coast"


def pb(file, kind, title, src, pf, date, shows, vis, state, used, how, gc, ff, ann=None):
    add(S, PB + "\\" + file, kind=kind, title=title, cit=src["cit"] % pf, url=src["url"], page=src["page"], pf=pf, date=date,
        credit=src["credit"], lic=src["lic"], shows=shows, vis=vis, state=state, used=used, how=how, ann=ann or [], gc=gc, f3d=ff)


pb("palm-beach-gold-coast_hunt2022_fig2_backhoe_dredger_and_split_hopper_barge_placing_rock_2019_native.jpeg", "report_photo",
   "Hunt et al. 2022 Fig 2: backhoe dredger and split hopper barge placing rock at the reef site (2019)", HUNT,
   "Fig 2 (word/media/image2.jpeg of the docx)", "May-September 2019 (construction)",
   "Backhoe dredger with a rock-carrying split-hopper barge and tug offshore, seen from the dune; the reef is under construction (not visible).",
   False, "under construction (2019)", ["context"], "Context: construction method (backhoe dredger placing 6-8 t rock). No geometry.", "GC-P01", f3d(False, "None", []))
pb("palm-beach-gold-coast_hunt2022_fig3_backhoe_dredger_at_reef_aerial_2019_native.jpeg", "aerial",
   "Hunt et al. 2022 Fig 3: backhoe dredger at the reef during construction (oblique aerial, 2019)", HUNT,
   "Fig 3 (word/media/image3.jpeg)", "May-September 2019 (construction)",
   "Oblique aerial of the dredger and barge on the reef site a few hundred metres off the beach, looking north towards Burleigh Heads, with the surf break and beach visible.",
   True, "under construction (2019)", ["context", "scale"],
   "Context: the dredger sits on the reef location a few hundred metres off the shoreline, consistent with 225-374 m off the waterline; no measurement taken.", "GC-P02", f3d(False, "None", []))
pb("palm-beach-gold-coast_hunt2022_fig5_wave_breaking_on_reef_native.jpeg", "photo",
   "Hunt et al. 2022 Fig 5: wave breaking and surf amenity on Palm Beach Reef", HUNT,
   "Fig 5 (word/media/image5.jpeg)", "after construction 2019 (date not stated)",
   "Photograph of a wave breaking over the submerged rock reef from the beach side; the reef crest shows as the break line.",
   True, "as-built (after Sept 2019)", ["context", "camera_match"], "Context and potential camera-match target for the 3D viewer; no value read.", "GC-P03",
   f3d(True, "Compare the wave break position/line with the modelled crest outline (59 x 6 m crest slot at -1.5 m MSL) if the camera position can be inferred", ["crest_z", "planform"]))
pb("palm-beach-gold-coast_prenzler2022_fig1_cctv_camera_view_of_reef_native.jpeg", "aerial",
   "Prenzler et al. 2022 Fig 1 (top): CCTV camera view of the reef with the camera field of view drawn on an aerial", PREN,
   "p.1, Fig 1 top (embedded raster)", "2020-2021 (wave-peel tracking period; image date not stated)",
   "Aerial of the beach, reef (dark patch) and the red wedge of the permanent shore-based CCTV camera, with the camera frame showing waves breaking over the reef.",
   True, "as-built (2020-2021)", ["context", "camera_match"], "Gives the camera wedge and one frame of the reef for camera_match; no geometry read.", "GC-P04",
   f3d(True, "Camera-match the CCTV frame to the 3D model (apex of the wedge = camera; reef direction)", ["crest_z", "planform"]))
pb("palm-beach-gold-coast_daniels2022_fig1_buoy_locations_natural_reef_outline_2016_native.jpeg", "aerial",
   "Daniels et al. 2022 Fig 1: wave buoy locations PBO1-4 at the natural Palm Beach reef", DAN,
   "p.1-2, Fig 1 (embedded raster)", "buoys deployed 25 Feb - 31 Aug 2016; aerial undated, before the artificial reef",
   "Aerial with the natural Palm Beach reef outlined (dashed) and the four DWR-G4 buoys (PBO1-PBO4), scale bar 0-2 km and north arrow. The artificial reef (2019) does not exist yet.",
   False, "pre-construction (2016)", ["3d_seabed", "context"],
   "The buoy depths in Table 1 (PBO1 11.33 m at 28.114007 S 153.479249 E; PBO2 11.29 m at 28.109683 S 153.474469 E; PBO3 11.75 m at 28.107191 S 153.473845 E; PBO4 23.80 m at 28.099271 S 153.474321 E; datum not stated) are depth points offshore of the reef; PBO3 is about 214 m seaward of the reef's offshore toe. Goes to REPORT.md section 5.",
   "GC-P05", f3d(True, "Seabed seaward of the offshore toe: model depth at PBO3 (-28.107191, 153.473845) vs 11.75 m (datum unstated, probably below MSL/AHD)", ["seabed"]))
pb("palm-beach-gold-coast_daniels2022_fig2_natural_palm_beach_reef_outlined_aerial_native.jpeg", "aerial",
   "Daniels et al. 2022 Fig 2: natural Palm Beach reef outlined on an aerial photograph", DAN,
   "p.3, Fig 2 (embedded raster)", "undated aerial (before 2019 construction)",
   "Aerial with the large natural rock reef outlined (dashed); water-colour contrast shows the reef's rock/sand; no artificial reef yet.",
   False, "pre-construction (undated)", ["context"],
   "Context: the natural reef 500 m off the beach (10-16 m deep seaward edge, 5-9 m shore edge) that focuses wave energy on the artificial reef site.", "GC-P06", f3d(False, "None", []))
pb("palm-beach-gold-coast_mortensen2015_fig1_erosion_at_palm_beach_native.jpeg", "photo",
   "Mortensen et al. 2015 Fig 1: example of erosion at Palm Beach", MORT, "p.1, Fig 1 (embedded raster)", "not stated (storm erosion before 2014)",
   "Photograph of a scarped dune and exposed rock wall at Palm Beach after a storm; shows the problem the reef addresses.",
   False, "pre-construction (c. 2013)", ["context"], "Context only.", "GC-P07", f3d(False, "None", []))
pb("palm-beach-gold-coast_mortensen2015_fig5_boussinesq_model_waves_breaking_on_scs_render_native.jpeg", "diagram",
   "Mortensen et al. 2015 Fig 5: Boussinesq model waves breaking on the concept SCS (render)", MORT, "p.6, Fig 5 (embedded raster)",
   "2014-2015 model output (concept, not built)",
   "3-D render of modelled waves (Hs 1.7 m, Tp 12 s, 73 deg) breaking on the concept submerged structure in the lower left.",
   False, "design (concept 2014, not the built reef)", ["context"], "Context only (concept design, different position and size).", "GC-P08", f3d(False, "None", []))
pb("palm-beach-gold-coast_mortensen2015_fig6a_baseline_bathymetry_contours_no_scs_native.jpeg", "survey_plot",
   "Mortensen et al. 2015 Fig 6 (top): pre-construction seabed depth contours at the Palm Beach concept site (no structure)", MORT,
   "p.6, Fig 6 top (embedded raster)", "bathymetry from the City's survey before 2014 (date not stated); figure 2015",
   "Contour map of the natural seabed off 19th Avenue in model metres with depth labels 1.5 to 13.5 m every 0.5 m, the concept SCS footprint (grey) and OPTISURF surf-ride tracks. No datum given for the labels.",
   True, "pre-construction seabed (c. 2013-14)", ["3d_seabed", "cross_check"],
   "Depth labels read along y = 3050 m (annotated copy): 2 m at x=394 ... 6.5 m at x=639, 8 m at x=718, 11.5 m at x=836 (model m; land edge x about 255). Reproduces the paper's concept toe depths 6.6 m and 11.4 m (Table 2). Goes to REPORT.md section 5 as the only labelled pre-construction seabed profile found.",
   "GC-P09", f3d(True, "Seabed along the built reef: Navionics-derived toe depths (inner toe -4.35 m MSL, outer toe -7.0 m MSL) vs this survey's depth at +-30 m positions (about 5 m inner, 8 m outer, below an unstated datum); gradient 1:51", ["seabed", "crest_z"]),
   ann=[ANN + r"\palm_beach_mortensen2015_fig6a_depth_contours_read_along_y3050.png"])
pb("palm-beach-gold-coast_mortensen2015_fig6b_bathymetry_contours_with_concept_scs_native.jpeg", "survey_plot",
   "Mortensen et al. 2015 Fig 6 (bottom): seabed contours with the concept SCS in place", MORT, "p.6, Fig 6 bottom (embedded raster)",
   "2014-2015 model setup (concept, not built)",
   "Same seabed contours as Fig 6 top with the concept structure's own contour set (grey, crest contours) drawn over it and coloured surf-ride tracks.",
   True, "design (concept 2014, not built)", ["cross_check", "context"], "Shows the concept structure's footprint on the seabed contours; no new values beyond Fig 6 top.", "GC-P10",
   f3d(False, "None (concept, not built)", []))
add(S, ANN + r"\q1_palm_beach_dtm_source_coverage_on_esri.png", kind="diagram",
    title="Q1 evidence: City of Gold Coast DTM (source-ID raster) coverage and 1 m contours over Esri imagery at Palm Beach",
    cit=Q1CIT % "2025-12-01", url=Q1URL, page=Q1PAGE,
    pf="annotated overlay generated by 07_scale/bathymetry/gold_coast/q1_dtm_evidence/q1_overlay.py",
    date="imagery 2025-12-01; DTM metadata raster modified 2024-05-13; overlay made 2026-10-06",
    credit="City of Gold Coast (DTM metadata, contours); Esri, Maxar, Earthstar Geographics (imagery); overlay by this project",
    lic="DTM metadata CC BY 2.5 AU; Esri imagery under Esri terms (private research copy)",
    shows="Palm Beach artificial reef (dark rock mound) lies 225-374 m off the beach in a region where the City's DTM source raster has NO cell (cyan outlines); data blocks (yellow) stop at the beach edge; the 1 m contours have minimum elevation 0 m AHD (red 0 m line along the beach). The DTM therefore holds no depth at the reef.",
    vis=True, state="as-built, imagery 2025-12-01", used=["cross_check", "context"],
    how="Answers Q1 for Palm Beach: block (row 370, col 238) at the reef centre is absent; so the Navionics-derived seabed in the 3D model cannot be replaced by the DTM (REQUESTS_FOR_LIOR C2 answered 'no'). Goes to REPORT.md section 2.",
    gc="GC-Q1P", f3d=f3d(False, "None: answers REQUESTS_FOR_LIOR C2 (the DTM has no Palm Beach nearshore soundings)", ["seabed"]))

# ---------------------------------------------------------------- City of Gold Coast brochure 2020 (Palm Beach)
S = "palm-beach-gold-coast"
CG = dict(
    cit="City of Gold Coast (2020). Palm Beach Shoreline Project - project overview (brochure, published June 2020, ref 19-TI-00753), %s. https://www.goldcoast.qld.gov.au/files/sharedassets/public/v/1/pdfs/environment/palm-beach-shoreline-project-brochure-a4.pdf (linked from https://www.goldcoast.qld.gov.au/Environment-sustainability/Protecting-our-environment/Managing-our-beaches/Seawalls-artificial-reefs). Accessed 2026-10-06.",
    url="https://www.goldcoast.qld.gov.au/files/sharedassets/public/v/1/pdfs/environment/palm-beach-shoreline-project-brochure-a4.pdf",
    page="https://www.goldcoast.qld.gov.au/Environment-sustainability/Protecting-our-environment/Managing-our-beaches/Seawalls-artificial-reefs",
    credit="City of Gold Coast (brochure; imagery credits not given on the pages used)", lic="not stated (City of Gold Coast publication; copyright City of Gold Coast)")
pb("palm-beach-gold-coast_cogc_brochure2020_p10_oblique_aerial_with_reef_natural_reef_benefit_area_labels_native.jpeg", "aerial",
   "City of Gold Coast 2020 brochure p.8: oblique aerial of Palm Beach with the artificial reef, natural reef and benefit area labelled", CG,
   "brochure page 8 (PDF p.10), full-page aerial (embedded jpeg, native resolution)", "photo undated (before 2019 construction: the artificial reef is drawn as a grey icon); brochure June 2020",
   "Oblique aerial looking north from Currumbin Creek over Palm Beach: the artificial reef is only a grey icon (labelled), with the Palm Beach natural reef, 21st Avenue and 11th Avenue groynes, benefit area, Burleigh headland.",
   False, "pre-construction aerial with the design drawn in (design, 2019)", ["context"],
   "Context and orientation (reef lies between the beach and the natural reef, north of the 21st Avenue groyne); the text on the page gives 160 m long x 80 m wide, 1.5 m below the average water level at its highest point, about 270 m offshore of Nineteenth Avenue.",
   "GC-P11", f3d(True, "Council text vs model: footprint 160 x 80 m (model grid 162 x 91 m), crest 1.5 m below 'average water level' (model -1.5 m MSL), 270 m offshore (model 225-374 m from the waterline)", ["planform", "crest_z"]))
pb("palm-beach-gold-coast_cogc_brochure2020_p11_plan_aerial_with_reef_icon_270m_native.jpeg", "aerial",
   "City of Gold Coast 2020 brochure p.9: plan aerial with the reef icon and the 270 m offshore distance", CG,
   "brochure page 9 (PDF p.11), 'Location and shape of the artificial reef' (embedded jpeg, native resolution)", "aerial undated (before 2019 construction); brochure June 2020",
   "Vertical aerial of 17th-23rd Avenue, Palm Beach with the 21st Avenue groyne, Palm Beach natural reef and a grey icon of the artificial reef with an arrow 'Approx. 270 m' from the beach.",
   False, "pre-construction aerial with the design drawn in (design, 2019)", ["plan_trace", "cross_check", "scale"],
   "Second council depiction of the reef planform (schematic icon, 2637 x 2637 px, no scale bar); the '270 m' arrow is council's distance reef to beach (to the reef's landward edge or centre not specified). Cross-check only: the verified shape comes from the council GIS polygon and the Bluecoast aerial.",
   "GC-P12", f3d(True, "Offshore distance: council 'approx. 270 m' vs model 225 m (nearest) to 374 m (farthest) from the waterline", ["planform"]))
pb("palm-beach-gold-coast_cogc_brochure2020_p11_section_view_crest_1.5m_below_average_water_level_200dpi_crop.png", "cross_section",
   "City of Gold Coast 2020 brochure p.9: section view of the artificial reef (not to scale), crest 1.5 m below average water level", CG,
   "brochure page 9 (PDF p.11), 'Section view of artificial reef' (vector figure rendered at 200 dpi and cropped)", "design drawing 2019/2020 (not to scale)",
   "Schematic cross-section: core rock under armour rock; crest of 6-8 t armour (pink) with 5-6 t (blue) beside it, 4-6 t (yellow) on the long slopes, 1-4 t (green) at the toes; 'AVERAGE WATER LEVEL' dashed line with a 1.5 m dimension to the crest; beach 270 m to the left. The shoreward (left) slope is shorter and steeper than the seaward (right) slope.",
   True, "design (as-built per the City)", ["3d_crest", "3d_height_slopes", "cross_check"],
   "Read: crest 1.5 m below the average water level; layers (core rock, armour); rock classes by zone; asymmetry of the slopes (not to scale, so no slope ratio taken). Corroborates the model crest -1.5 m MSL ('average water level' = MSL/AHD, to be confirmed). Goes to REPORT.md section 5.",
   "GC-P13", f3d(True, "Crest depth 1.5 m below 'average water level' vs model -1.5 m MSL (and the chart label FISH HAVEN 1.5MT); rock-class zones for the surface texture; shoreward slope shorter and steeper than seaward", ["crest_z", "height", "slopes"]))

# ---------------------------------------------------------------- ICM website article (2023): images saved in 03_images/reefs/<slug>/
RI = ROOT + r"\03_images\reefs"
ICM = dict(
    cit="International Coastal Management (2023). Artificial Reefs and Nearshore Nourishment on the Gold Coast: What the Monitoring Shows. ICM website article, published 2023-09-18, image %s. https://www.coastalmanagement.com.au/artificial-reefs-and-nearshore-nourishment-on-the-gold-coast-real-world-results. Accessed 2026-10-06.",
    page="https://www.coastalmanagement.com.au/artificial-reefs-and-nearshore-nourishment-on-the-gold-coast-real-world-results",
    credit="International Coastal Management (ICM) / City of Gold Coast (the page captions some images 'Source: Gold Coast City'; photographer not named)",
    lic="not stated (ICM website image; copyright ICM / City of Gold Coast)")
S = "narrowneck-gold-coast"
add(S, RI + r"\narrowneck-gold-coast\narrowneck-gold-coast_renewal_works_dredger_over_reef_icm_2017-18.png", kind="aerial",
    title="Narrowneck Reef during the renewal works: split-hull dredger over the reef, oblique drone view (ICM 2023 article)",
    cit=ICM["cit"] % "wixstatic 97fa2b_629236... (1254 x 783 px png)", url="https://static.wixstatic.com/media/97fa2b_629236265391409984d5135f7c0e7d33~mv2.png", page=ICM["page"],
    pf="article image (no figure number; shown with the Narrowneck section)", date="2017-2018 (renewal works August 2017 - June 2018; exact date not stated)", credit=ICM["credit"], lic=ICM["lic"],
    shows="Oblique drone view of the Narrowneck reef in clear water with a red split-hull dredger beside it and a yellow navigation buoy in the background; the dark container arms, a wing and gaps are visible through the water.",
    vis=True, state="renewal works in progress (2017-18)", used=["plan_trace", "cross_check", "context"],
    how="Shows the planform of the reef at the time the extra containers were being added (arm and wing outlines, gaps). Oblique, no scale: usable as a qualitative check of the 'previous vs amended shape' question, not for metric tracing. Goes to REPORT.md section 6.",
    gc="GC-N22", f3d=f3d(True, "Narrowneck renewal planform (previous vs amended shape): compare arm/wing outline here with the traced shape; presence of the yellow buoy marks post-2017", ["planform"]))
add(S, RI + r"\narrowneck-gold-coast\narrowneck-gold-coast_drone_view_reef_with_surfers_and_buoy_icm_post2018.jpeg", kind="aerial",
    title="Narrowneck Reef: drone view with surfers paddling over the reef and a yellow navigation buoy (ICM 2023 article)",
    cit=ICM["cit"] % "wixstatic 97fa2b_f69ad0... (1965 x 1450 px jpeg)", url="https://static.wixstatic.com/media/97fa2b_f69ad0ae528945e68229b95f44b86eb0~mv2.jpeg", page=ICM["page"],
    pf="article image (no figure number)", date="not stated (after the 2018 renewal: the yellow buoy is installed; before 2023 publication)", credit=ICM["credit"], lic=ICM["lic"],
    shows="Low oblique drone photo of two surfers paddling next to the submerged reef; the container arms and a wing show as dark patches in turquoise water, a yellow buoy near the horizon, a wave line passing over the reef crest.",
    vis=True, state="as renewed (post-2018)", used=["plan_trace", "cross_check", "context"],
    how="Qualitative view of the renewed reef planform and of wave breaking over the crest; no scale. Goes to REPORT.md section 6 (tracer: renewed state).",
    gc="GC-N23", f3d=f3d(True, "Planform of the renewed reef vs shape.json; crest depth consistency (waves break over the crest at low tide)", ["planform", "crest_z"]))
add(S, RI + r"\narrowneck-gold-coast\narrowneck-gold-coast_aerial_looking_north_narrowneck_surfers_paradise_icm_2023.jpg", kind="aerial",
    title="Narrowneck and Surfers Paradise looking north: the narrow strip between the ocean and the Nerang River (ICM 2023 article)",
    cit=ICM["cit"] % "wixstatic 97fa2b_24e33c... (1920 x 1080 px jpeg)", url="https://static.wixstatic.com/media/97fa2b_24e33cee570148cdab37452aef12253b~mv2.jpg", page=ICM["page"],
    pf="article image (captioned 'Source: Gold Coast City')", date="not stated", credit=ICM["credit"], lic=ICM["lic"],
    shows="Oblique aerial of the northern Gold Coast beach from Surfers Paradise towards the Spit, with the Nerang River on the right; the reef is not clearly visible (surf zone white water at left).",
    vis=False, state="site context (undated, post-2000)", used=["context"],
    how="Site context only (the narrow strip that the reef protects); not used for geometry.", gc="GC-N24", f3d=f3d(False, "None", []))
S = "palm-beach-gold-coast"
add(S, RI + r"\palm-beach-gold-coast\palm-beach-gold-coast_satellite_pair_reef_and_inshore_sandbank_icm_post2019.jpg", kind="satellite",
    title="Palm Beach reef and inshore sandbank: two satellite views (ICM 2023 article)",
    cit=ICM["cit"] % "wixstatic 97fa2b_89f98f... (828 x 528 px jpeg; alt text 'palm beach reef on Gold Coast Australia')", url="https://static.wixstatic.com/media/97fa2b_89f98f3ec7d7457b90a35a81e660d0be~mv2.jpg", page=ICM["page"],
    pf="article image (captioned 'Aerial of sand build up and interruption around reef' on the page)", date="not stated (after September 2019)", credit=ICM["credit"], lic=ICM["lic"],
    shows="Two low-resolution satellite crops of Palm Beach with the artificial reef as a dark elongated mound offshore, the beach at left and a surf-zone sandbank forming inshore of the reef; also the natural reef at the top.",
    vis=True, state="as-built (post-2019, two dates not stated)", used=["cross_check", "context"],
    how="Confirms the reef is still in place and the inshore sandbank formation after construction (no later damage visible); low resolution, no scale. Goes to REPORT.md section 5.",
    gc="GC-P14", f3d=f3d(True, "No-later-change claim: reef still present after construction (2 satellite dates unknown); compare outline orientation with model", ["planform"]))

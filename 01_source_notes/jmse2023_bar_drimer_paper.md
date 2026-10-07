# Bar, D. & Drimer, N. (2023) — "Preliminary Design Tools for Hydrodynamic Aspects of Submerged Impermeable Breakwaters"

- **Source path:** `Initial info from Lior\JMSE1100236DesignToolsSubmergedImpermeableBreakwaters2023BarDrimer - paper with good summary of wrtifical reefs around the world.pdf`
- **Size:** 4,132,311 bytes (3.94 MB)
- **Type:** PDF, 22 pages, native text (not scanned) — extracted cleanly in full with PyMuPDF, no OCR needed, no extraction failures on any page
- **Full citation:** Bar, D.; Drimer, N. Preliminary Design Tools for Hydrodynamic Aspects of Submerged Impermeable Breakwaters. *J. Mar. Sci. Eng.* **2023**, *11*, 236. https://doi.org/10.3390/jmse11020236
- **Journal:** Journal of Marine Science and Engineering (JMSE), MDPI. Open access, **Creative Commons Attribution (CC BY) 4.0** license (stated on p.1) — quotes/figures may be reused with attribution.
- Received 13 Nov 2022; Revised 10 Jan 2023; Accepted 11 Jan 2023; Published 17 Jan 2023.
- Academic Editor: Abdellatif Ouahsine.
- **Date read:** 2026-09-24

## Summary

This is a numerical-methods paper, not primarily a survey paper — despite the folder-name description "paper with good summary of artificial reefs around the world," the world-reef survey is confined to a short, dense paragraph in the Introduction (about 2 paragraphs, PDF page 2) that name-checks 8 real-world projects with citation numbers, plus a broader review-of-reviews citation to "Raised Water Research." The bulk of the paper (Sections 2–4, Appendix A, ~18 of 22 pages) develops and validates a new 2-D boundary-element numerical wave flume, **BELWF** (Boundary Elements Lagrangian Wave Flume), built on Drimer & Agnon's (2006) BEM formulation, extended to simulate **Geotubes** (sand-filled geotextile tubes) as submerged impermeable breakwaters/reefs. BELWF is validated against OpenFOAM (VOF/RANS) simulations of a Geotube under waves, then applied to a practical design example (shoaling from 16 m to 4 m depth over a 1:40 slope, with an 11 m-wide, 2.2 m-high Geotube) to assess wave loads and sliding stability (the "Sliding Index," SI). The paper is funded by **The Israel Ports Development & Assets Company Ltd.** (grant no. 2031167), and both authors are at the Technion (Haifa) — Daniel Bar at CAMERI (Coastal and Marine Engineering Research Institute) and Nitai Drimer (corresponding author) at Mechanical Engineering. For the HTML survey project, this paper's main value is (a) the short but well-cited list of real-world artificial/multifunctional surf reef and Geotube projects to chase down online, (b) confirmation that Israel's first Geotube structure was built in 2018 at **Ashkelon** for beach/cliff erosion (not Haifa/Tel Aviv/Netanya/Herzliya — those are not mentioned in this paper at all), and (c) engineering background on how Geotube reefs are built and why they fail (undersized tubes, sand burial) that is useful context for the "why it worked / why not" narrative. There are no photographs of any real built reef in this PDF — all 16 figures are technical (geometry diagrams, mesh grids, load/time graphs, flowcharts).

## Artificial reefs mentioned

All of these are named in a single passage in the Introduction (PDF p.2 of 22). The paper gives no independent size/cost/financing/outcome detail beyond what is quoted below — everything else about each project (size, cost, exact outcome mechanism, images) must come from the cited references or from web research (see Open questions).

### Narrowneck Reef / "Gold Coast Reef," Queensland, Australia
- **Place / country:** Narrowneck, Gold Coast, Queensland, Australia
- **Year:** not stated in this paper (design paper cited is Black & Mead 2001; case-study paper is Jackson et al. 2012 — actual construction year not given here)
- **Type:** Multifunctional submerged artificial surf reef (ASR), classified by the paper among "submerged artificial surf reefs (ASRs) made of Geotubes"
- **Size / cost:** not stated in this paper
- **Financing:** not stated in this paper
- **Purpose:** Surfing, public amenity, and coastal protection (per the title of ref. [17]) — the paper's framing is "coastal protection, surf amenities and beach safety"
- **Design vs. built:** not discussed in this paper
- **Outcome:** Listed among the ASR projects that the paper says are covered by a "comprehensive review" (ref. [20], Raised Water Research) which found "most of the projects have failed." Reference [18] is specifically a "Long Term Performance" case study of Narrowneck, suggesting real performance data exists in that source. The paper's own diagnosis of common failure causes (ref. [18,20]) is "too-small size Geotubes installed or the loss of effectiveness due to sand coverage."
- **Citations given:** [17] Black, K.; Mead, S. "Design of the Gold Coast Reef for Surfing, Public Amenity and Coastal Protection: Surfing Aspects." *J. Coast. Res.* 2001, 115–130. [18] Jackson, L.; Tomlinson, R.; Corbett, B.; Strauss, D. "Long Term Performance of a Submerged Coastal Control Structure: A Case Study of the Narrowneck Multi-Functional Artificial Reef." *Coast. Eng. Proc.* 2012, 1, 54.

### Pratte's Reef, El Segundo, California, USA
- **Place / country:** El Segundo, California, USA
- **Year:** not stated in this paper
- **Type:** Submerged artificial surf reef (ASR)
- **Size / cost:** not stated in this paper
- **Financing:** not stated in this paper
- **Purpose:** Grouped with the ASR projects aiming at "coastal protection, surf amenities and beach safety"
- **Design vs. built:** not discussed
- **Outcome:** Implicitly included in "most of the projects have failed" (per Raised Water Research review, ref. [20]); no project-specific detail given
- **Citations given:** [14] Henriquez, M. "Artificial Surf Reefs." Master's Thesis, Delft University of Technology, Delft, The Netherlands, 2005.

### Mount Maunganui Beach Reef, New Zealand
- **Place / country:** Mount Maunganui Beach, New Zealand
- **Year:** not stated in this paper
- **Type:** Multipurpose artificial reef
- **Size / cost:** not stated in this paper
- **Financing:** not stated in this paper
- **Purpose:** Multipurpose (coastal protection + surf + amenity, per the general framing)
- **Design vs. built:** not discussed
- **Outcome:** Implicitly included in "most of the projects have failed" per ref. [20]; no project-specific detail given here
- **Citations given:** [19] Black, S.M.; Kerry, A. "Multipurpose, Artificial Reef at Mount Maunganui Beach, New Zealand." *Coast. Manag.* 1999, 27, 355–365.

### Young-Jin Beach, east coast of Korea
- **Place / country:** Young-Jin beach, east coast of South Korea
- **Year:** not stated in this paper (cited source is Oh & Shin 2006)
- **Type:** Geotube used as a **detached breakwater** (paper distinguishes this category from the ASR/surf-reef category above)
- **Size / cost:** not stated in this paper
- **Financing:** not stated in this paper
- **Purpose:** Shore protection ("Using Submerged Geotextile Tubes in the Protection of the E. Korean Shore")
- **Design vs. built:** not discussed
- **Outcome:** not stated in this paper (not covered by the "most have failed" sentence, which the paper appears to apply specifically to the three ASR projects listed just before it — Narrowneck, Pratte's Reef, Mount Maunganui)
- **Citations given:** [21] Oh, Y.I.; Shin, E.C. "Using Submerged Geotextile Tubes in the Protection of the E. Korean Shore." *Coast. Eng.* 2006, 53, 879–895.

### Yucatán, Mexico
- **Place / country:** Yucatán, Mexico
- **Year:** not stated in this paper (cited source 2014)
- **Type:** Geotube submerged breakwater (detached breakwater category)
- **Size / cost:** not stated in this paper
- **Financing:** not stated in this paper
- **Purpose:** Beach protection
- **Design vs. built:** Cited paper is explicitly an "Experimental Study," so likely physical/lab-model work rather than (or in addition to) a field installation — needs checking online
- **Outcome:** not stated in this paper
- **Citations given:** [22] González Leija, M.; Chavez, X.; Alvarez, E.; Mendoza, E.; Silva, R. "Experimental Study on Geotextile Tube Applications as Submerged Breakwaters for Beach Protection in Yucatan, Mexico." *Coast. Eng. Proc.* 2014, 1, 25.

### Al Aqah Beach, Fujairah, UAE
- **Place / country:** Al Aqah Beach, Fujairah, United Arab Emirates
- **Year:** not stated in this paper (cited source 2014)
- **Type:** Geotextile tube, beach nourishment application (detached breakwater category)
- **Size / cost:** not stated in this paper
- **Financing:** not stated in this paper
- **Purpose:** Beach nourishment
- **Design vs. built:** not discussed
- **Outcome:** not stated in this paper
- **Citations given:** [8] Chien, A.; Wu, S.; Tseng, F.; Tang, A. "Geotextile Tubes Application on Beach Nourishment in UAE." *Int. J. Environ. Sci. Dev.* 2014, 5, 506–509.

### Sigandu Beach, Central Java, Indonesia
- **Place / country:** Sigandu Beach, Central Java, Indonesia
- **Year:** not stated in this paper (cited source 2015)
- **Type:** Low-crested breakwater(s), described in the context of Geotube detached breakwaters
- **Size / cost:** not stated in this paper
- **Financing:** not stated in this paper
- **Purpose:** Beach profile / erosion control (paper title references "Beach Profile Changes Due to Low Crested Breakwaters")
- **Design vs. built:** not discussed
- **Outcome:** not stated in this paper directly, but the cited paper's own title ("Beach Profile Changes Due to Low Crested Breakwaters at Sigandu Beach") implies it reports measured morphological change — worth pulling for real before/after data
- **Citations given:** [23] Sulaiman, D.M.; Bachtiar, H.; Taufiq, A.; Hermanto. "Beach Profile Changes Due to Low Crested Breakwaters at Sigandu Beach, Central Java." *Procedia Eng.* 2015, 116, 510–519.

### Ashkelon, Israel (first Israeli Geotube project)
- **Place / country:** Ashkelon shoreline, Israel
- **Year:** **2018** (explicitly stated: "In 2018, the first project of Geotubes structure was established in Israel")
- **Type:** Geotube structure (not specified whether ASR/surf-reef or plain detached breakwater in this paper's text — the cited source's title suggests general "geotextile structures for beach protection")
- **Size / cost:** not stated in this paper
- **Financing:** not stated in this paper
- **Purpose:** "Aimed at mitigating beach and cliff erosion along the Ashkelon shoreline" — i.e., combined beach erosion AND cliff erosion control
- **Design vs. built:** not discussed
- **Outcome:** not stated in this paper (no performance data given)
- **Citations given:** [24] Gouaud, F. "Geotextile Structures for Beach Protection Ashkelon, Israel"; Corinthe Ingénierie: Grimaud, France, 2016. (Note: report dated 2016, two years before the stated 2018 construction — likely the design/feasibility report predating construction.)
- **This is Israel's own project** and should be cross-linked with the project's Israel/sediment section (02_research/israel) as well as with the reef survey (02_research/reefs) — it sits at the intersection of both.

### Living Breakwaters, Staten Island, New York, USA (mentioned outside the main reef paragraph, but is a specific, named, located project)
- **Place / country:** Staten Island, New York, USA
- **Year:** Conference paper 2019 (Coastal Structures Conference 2019, Hanover, Germany); construction/project year not stated in this paper
- **Type:** "Living breakwaters" — grouped by the paper alongside floating breakwaters, Bragg breakwaters, submerged reef balls, and artificial mangrove root systems as alternatives to rubble-mound breakwaters, with "potential advantages in cost, hydrodynamics and environmental features"
- **Size / cost:** not stated in this paper
- **Financing:** not stated in this paper
- **Purpose:** Coastal protection with an ecological/habitat design intent (the term "living breakwaters" implies this, though the paper doesn't elaborate)
- **Design vs. built:** paper cites "Numerical and Physical Modeling to Inform Design," so design-stage modeling is documented in the source
- **Outcome:** not stated in this paper
- **Citations given:** [7] Marrone, J.; Zhou, S.; Brashear, P.; Howe, B.; Baker, S. "Numerical and Physical Modeling to Inform Design of the Living Breakwaters Project, Staten Island, New York." Coastal Structures Conference 2019, Hanover, Germany, 29 Sep–2 Oct 2019.

### Other, non-site-specific "alternative breakwater" technologies named in the Introduction (not tied to a single named place — include for completeness / possible follow-up, but do not treat as individual "reef case studies")
- **Submerged hollow hemispherical artificial reefs** — general technology, not site-specific in this paper. Citations: [4] Armono, H. "Wave Transmission on Submerged Breakwaters Made of Hollow Hemispherical Shape Artificial Reefs." Canadian Coastal Conference, Kingston, ON, Canada, 15 Oct 2003. [5] Na'im, I.; Shahrizal, A.R.M.; Safari, M.D. "A Short Review of Submerged Breakwaters." *MATEC Web Conf.* 2018, 203, 01005.
- **Artificial mangrove root system (ArMS)** — wetland habitat protector, general/modeling study, not a single named beach. Citation: [6] Fatimah, E.; Wahab, A.K.A.; Ismail, H. "Numerical Modeling Approach of an Artificial Mangrove Root System (ArMS) Submerged Breakwater as Wetland Habitat Protector." COPEDEC, Dubai, UAE, 2008.
- **Portugal multifunctional artificial reef (design proposal, not confirmed built in this paper)** — citation [15] Voorde, M.; Antunes do Carmo, J.; Neves, M. "Designing a Preliminary Multifunctional Artificial Reef to Protect the Portuguese Coast." *J. Coast. Res.* 2009, 25, 69–79. Worth checking online whether this was ever built.
- **Mediterranean coast multifunctional artificial reef (review/role paper)** — citation [16] López, I.; Tinoco, H.; Aragonés, L.; García-Barba, J. "The Multifunctional Artificial Reef and Its Role in the Defence of the Mediterranean Coast." *Sci. Total Environ.* 2016, 550, 910–923. Directly relevant to Israel's Mediterranean coast context — should be prioritized in web research.
- **"Raised Water Research"** — not a single reef but a **review website/organization** the paper cites as having conducted "a comprehensive review" of ASR projects worldwide and concluded "most of the projects have failed." This should be searched online directly as a rich secondary source. Citation: [20] "Raised Water Research — Research, News and Advice about Making Waves." https://raisedwaterresearch.com/ (accessed 9 June 2022 by the paper's authors).

## Israel-related content

- **Geotubes — general technical definition (applies to Israel and worldwide):** "Geo-textile bags, filled with saturated sand, dredged from the seabed, termed Geotubes... The woven geotextile container (tube) filters out water but keeps the sand grains inside. The principal construction procedure is laying the empty tubes on the seabed at the desirable location, securing the tubes with temporary anchors and lashing, and the high-pressure injecting of saturated sand, pumped from the seabed." (p.1–2). Geotextile tubes "may serve, for instance, as groins, detached breakwaters, dune foot protection and submerged reefs."
- **Israel's first Geotube project: Ashkelon, 2018** — see full entry above under "Artificial reefs mentioned." Purpose: mitigating **both beach erosion and cliff erosion**. Source report: Gouaud, F. (2016), Corinthe Ingénierie (a French coastal engineering firm based in Grimaud, France) — this French firm should be searched for further Ashkelon project documents/cost data.
- **Haifa, Tel Aviv, Netanya, Herzliya:** **not mentioned anywhere in this paper.** No content on Tel Aviv's early-20th-century breakwaters, Haifa Port's annual sand replenishment, or Netanya/Herzliya sand-recovery attempts — these will need to come from other source files and/or web research, per the task brief.
- **Tides / tidal range in Israel:** **not stated** in this paper (no tide data at all — the paper works entirely in terms of water depth, wave height and wave period, not tidal datums).
- **Swell / wave measurements specific to Israel:** **not stated** as site data. The paper's two worked examples (validation case and "practical design example") use generic engineering parameters, not measured Israeli wave-climate data:
  - *Validation example* (compared against OpenFOAM): two Geotubes forming a 12 m-wide structure; each Geotube filled (100%) radius 3.425 m, filled to 80% (FA = 0.8) giving a Geotube height of 3.8 m; placed on a horizontal seabed at water depth 5 m (freeboard 1.2 m); incident wave period T = 7 s; wave heights stepped from 0.3 m to 1.6 m. Sand density assumed: **2082 kg/m³** for wet saturated sand (cited to a density-of-sand reference website, ref. [37]).
  - *Practical design example*: wave period 9 s, generated wave height 2.2 m, shoaling from an intermediate depth of 16 m over a 1:40 slope to a shallow depth of 4 m, where a Geotube of width 11 m and height 2.2 m (freeboard 1.8 m) is placed; the wave shoals to 2.86 m at the toe of the structure; Iribarren number 0.17 (spilling-breaker range, but the Geotube itself steepens the wave into a plunging breaker).
  - Neither example is stated to represent a specific Israeli coastal site — they read as generic/illustrative design cases, though plausible for Mediterranean nearshore conditions. **Open question:** confirm with the authors/CAMERI whether these parameters were chosen to represent a real Israeli site (e.g., near Haifa).
- **Funding:** "This research was funded by **The Israel Ports Development & Assets Company Ltd.**, grant number 2031167." (Author Contributions section, p.12). This is an Israeli state-linked ports company — worth checking whether it is the same body/family of companies as "Haifa Port company" referenced in Lior's own material (likely related to, or the parent of, Israel Ports Company / Haifa Port Company — needs web confirmation, do not assume identity).
- **Institution:** Technion — Israel Institute of Technology, Haifa. Daniel Bar is affiliated with **CAMERI — Coastal and Marine Engineering Research Institute**, part of the Interdisciplinary Program for Marine Engineering, Technion, Haifa 32000, Israel. Nitai Drimer (corresponding author) is at the Faculty of Mechanical Engineering, Technion, Haifa 32000, Israel (nitaid@technion.ac.il). CAMERI is Israel's principal academic coastal-engineering research body and is very likely to hold real Israeli wave/tide climatology data relevant to this project — worth contacting or searching their publications directly.
- **Lior's own proposals:** not present in this paper (this is a peer-reviewed academic source, not Lior's notes — his proposals are in his own files elsewhere in the folder, e.g. "geotubes in israel and the england surf reef.txt" and the PPTX/PDF files, not yet reviewed by this note).

## People and organisations

- **Daniel Bar** — author; The Interdisciplinary Program for Marine Engineering, Technion; CAMERI (Coastal and Marine Engineering Research Institute), Haifa, Israel.
- **Nitai Drimer** — corresponding author; Faculty of Mechanical Engineering, Technion, Haifa, Israel (nitaid@technion.ac.il); also author of the earlier foundational BEM paper, Drimer & Agnon (2006), which this paper extends.
- **Abdellatif Ouahsine** — Academic Editor who handled the paper for JMSE.
- **The Israel Ports Development & Assets Company Ltd.** — funder of this research (grant no. 2031167). Likely relevant to who finances Israeli coastal-protection infrastructure generally — worth investigating for the "who financed it" thread in the Israel section of the HTML survey.
- **Corinthe Ingénierie** (Grimaud, France) — French coastal engineering firm, author (via F. Gouaud) of the 2016 Ashkelon Geotube design report [24].
- **CAMERI (Coastal and Marine Engineering Research Institute, Technion)** — Israel's main coastal-engineering research institute; likely source of Israeli wave/tide data for the project.
- **"Raised Water Research"** (raisedwaterresearch.com) — cited review organization/website that assessed most world ASR projects as failures; worth researching directly as a secondary source with likely more site-by-site detail than this paper gives.
- **Cited authors tied to specific reef sites** (see full reference list below for exact citations): Black, K.; Mead, S. (Gold Coast/Narrowneck design); Jackson, L.; Tomlinson, R.; Corbett, B.; Strauss, D. (Narrowneck long-term performance case study); Henriquez, M. (Delft MSc thesis on artificial surf reefs, incl. Pratte's Reef); Black, S.M.; Kerry, A. (Mount Maunganui reef); Oh, Y.I.; Shin, E.C. (Korea Geotube shore protection, x2 papers — also a general Geotube coastal-erosion paper); González Leija, M.; Chavez, X.; Alvarez, E.; Mendoza, E.; Silva, R. (Yucatán, Mexico); Chien, A.; Wu, S.; Tseng, F.; Tang, A. (UAE/Fujairah); Sulaiman, D.M.; Bachtiar, H.; Taufiq, A.; Hermanto (Sigandu, Indonesia); Gouaud, F. (Ashkelon, Israel); Marrone, J.; Zhou, S.; Brashear, P.; Howe, B.; Baker, S. (Staten Island Living Breakwaters); Voorde, M.; Antunes do Carmo, J.; Neves, M. (Portugal reef design); López, I.; Tinoco, H.; Aragonés, L.; García-Barba, J. (Mediterranean multifunctional reef).
- **Geotechnical/stability methods authors** (relevant to the engineering "how it's built / design vs. built" thread, not to a specific site): Bezuijen, A.; Vastenburg, E. (Geotube fill-geometry method, book *Geosystems: Design Rules and Applications*); Van Steeg, P.; Vastenburg, E.W. (Deltares large-scale physical model tests on Geotube stability).

## Images extracted

**No photographs of any real, built artificial reef appear anywhere in this PDF.** All raster/vector images are technical figures generated for this modeling study. None are candidates for the HTML page's "photo of each real-world reef" gallery. Listed here for completeness / possible use as an explanatory "how it works" mechanism diagram if ever needed:

| # | Page | Figure | What it shows | Safe to use? |
|---|------|--------|----------------|---------------|
| 1 | 4 | Fig. 1 | Cross-section shapes of a partially filled Geotube at filling ratios 0.60–0.85 (schematic, not a photo) | Yes (CC BY 4.0), but not a "real reef" photo — schematic only |
| 2 | 4 | Fig. 2 | OpenFOAM computational mesh/grid of the wave flume (207,777 cells) | Yes (CC BY), but technical/not illustrative for a lay audience |
| 3 | 5 | Fig. 3 | OpenFOAM simulation frame: a 1 m breaker over the Geotube | Yes (CC BY), simulation render, not a real photo |
| 4 | 5 | Fig. 4 | Schematic of forces (gravity, buoyancy, wave load, friction) acting on a submerged Geotube | Yes (CC BY) — potentially useful as a "why it can fail (sliding)" explainer diagram |
| 5 | 7 | Fig. 5 | Graph: wave loads on the Geotube vs. wave height, BELWF vs. OpenFOAM | Yes (CC BY), technical chart |
| 6 | 7 | Fig. 6 | Graph: Sliding Index (SI) vs. wave height, BELWF vs. OpenFOAM | Yes (CC BY), technical chart |
| 7 | 8 | Figs. 7–9 | Detailed water-surface/loads/SI time-series for wave heights 1.3–1.5 m | Yes (CC BY), technical |
| 8 | 10 | Fig. 10 | Full flume layout showing a developed plunging breaker over the Geotube (simulation) | Yes (CC BY) — visually the most "photogenic" simulation frame if an explainer image is wanted |
| 9 | 11 | Fig. 11 | Pressure diagrams + water-surface/loads/SI for the practical design example | Yes (CC BY), technical |
| 10 | 13–19 | Figs. A1–A5 | Appendix math/numerics: flow-domain sketch, local element interpolation, BEM element scheme, solution flowchart, boundary-element mesh of the Geotube body | Yes (CC BY), purely mathematical/technical |
| — | 1 | (unlabeled) | Front-matter logos (MDPI/JMSE branding, CC BY badge, journal cover thumbnail) | Not applicable / not useful for the survey |

No files were extracted to `03_images/from_lior/` from this source, since there is nothing photographic to extract. (`extracted_images` in the structured output below is empty for this reason.)

## Verbatim quotes worth using

(Paper is CC BY 4.0 licensed — quoting is permitted with attribution: Bar & Drimer, *J. Mar. Sci. Eng.* 2023, 11, 236.)

- On the state of the field, p.2: *"Over the last twenty years, attempts to establish multifunctional submerged artificial surf reefs (ASRs) made of Geotubes have been made around the world, with the expectation that such solutions could incorporate coastal protection, surf amenities and beach safety."*
- On overall outcomes, p.2: *"Unfortunately, in a comprehensive review provided by the 'Raised Water Research', it seems that most of the projects have failed."*
- On why they failed, p.2: *"Common reasons for failure are related to too-small size Geotubes installed or the loss of effectiveness due to sand coverage."*
- On Israel's own project, p.2: *"In 2018, the first project of Geotubes structure was established in Israel, aimed at mitigating beach and cliff erosion along the Ashkelon shoreline."*
- On what Geotubes can be used for, p.1–2: *"Geotextile tubes may serve, for instance, as groins, detached breakwaters, dune foot protection and submerged reefs."*
- Funding statement, p.12: *"This research was funded by The Israel Ports Development & Assets Company Ltd. grant number 2031167."*

## Open questions for web research

1. **Narrowneck / Gold Coast Reef (Australia):** exact build year, size (volume/length/depth), cost, financier, and — critically — its actual long-term outcome per Jackson et al. 2012 [18] (the paper only says it's covered by that "long term performance" case study, not what it concluded). Also check whether it is still functioning today (2026) or has been modified/removed.
2. **Pratte's Reef (El Segundo, CA):** was this the famous submerged-sandbag reef removed after failing/moving? Get build year, size, cost, removal date if applicable, and surfer reviews.
3. **Mount Maunganui Beach Reef (New Zealand):** build year, size, cost, current status — reportedly also considered a failure by some reviews; confirm and find real surfer/community commentary.
4. **Young-Jin Beach (Korea), Yucatán (Mexico), Al Aqah/Fujairah (UAE), Sigandu Beach (Indonesia):** these are Geotube *detached breakwaters*, not surf reefs — find size, cost, financier, and measured outcome (the Sigandu paper title suggests it reports actual beach-profile change data — worth sourcing directly). Chien et al. 2014 (UAE) is an easily searchable open-ish journal (IJESD) — check for full text.
5. **Ashkelon Geotube project (Israel), 2018:** find Corinthe Ingénierie's 2016 design report or any successor publications/news articles; find actual built dimensions, cost, current condition, and any before/after erosion data. This is the single most important item to chase for the Israel section, since it is Israel's only confirmed built Geotube project per this paper.
6. **"Raised Water Research" (raisedwaterresearch.com):** access this site directly — the paper describes it as a "comprehensive review" of ASR projects and the primary source for the "most have failed" claim. It likely has site-by-site detail (and possibly images/reviews) far beyond this paper's brief mention. High priority.
7. **Staten Island Living Breakwaters (New York):** find current status/cost/financier (NY Governor's Office of Storm Recovery funded this — verify independently) and ecological outcome data; useful as a US "living shoreline" contrast case even though it's not primarily a surf reef.
8. **López et al. 2016** ("The Multifunctional Artificial Reef and Its Role in the Defence of the Mediterranean Coast") — directly relevant to Israel's Mediterranean context; try to get full text.
9. **Voorde, Antunes do Carmo & Neves 2009** (Portugal multifunctional reef design) — confirm whether this design was ever actually built, and if so, where and with what outcome.
10. **Israel Ports Development & Assets Company Ltd.** — confirm its relationship (same entity? subsidiary? unrelated?) to "Haifa Port company" mentioned in Lior's own notes as funding annual sand replenishment at Haifa — do not assume they are the same without confirmation.
11. **CAMERI (Technion's Coastal and Marine Engineering Research Institute)** — search their own publication list/site for Israeli wave-climate and tide data (this paper contains none), and for any of their own Haifa/Israel-specific reef or breakwater studies that might complement or update this 2023 paper.
12. Whether the paper's two worked numerical examples (5 m depth / 7 s period / 0.3–1.6 m waves; and 16→4 m depth / 9 s period / 2.2 m wave) are meant to represent real Israeli (e.g., Haifa-area) conditions — not stated in the paper itself; would need to ask the authors or find a companion/follow-up paper.
13. No PDF pages failed to extract and no scanned/non-text pages were encountered, so there are no data-quality open questions on the source file itself.

## Full reference entries copied from the file

All 38 references from the paper's reference list (PDF pages 20–22), copied in full so later agents can search for them online. Numbers correspond to the in-text citation numbers used above and throughout the paper.

1. Burcharth, H.F.; Zanuttigh, B.; Andersen, T.L.; Lara, J.L.; Steendam, G.J.; Ruol, P.; Sergent, P. Coastal Risk Management in a Changing Climate. Chapter 3—Innovative Engineering Solutions and Best Practices to Mitigate Coastal Risk. In *Coastal Risk Management in a Changing Climate*; Butterworth-Heinemann: Oxford, UK, 2015; pp. 55–170.
2. Zhang, C.; Magee, A.R. Effectiveness of Floating Breakwater in Special Configurations for Protecting Nearshore Infrastructures. *J. Mar. Sci. Eng.* 2021, 9, 785.
3. Gao, J.; Ma, X.; Dong, G.; Chen, H.; Liu, Q.; Zang, J. Investigation on the Effects of Bragg Reflection on Harbor Oscillations. *Coast. Eng.* 2021, 170, 103977.
4. Armono, H. Wave Transmission on Submerged Breakwaters Made of Hollow Hemispherical Shape Artificial Reefs. In Proceedings of the Canadian Coastal Conference, Kingston, ON, Canada, 15 October 2003; Volume 2003.
5. Na'im, I.; Shahrizal, A.R.M.; Safari, M.D. A Short Review of Submerged Breakwaters. *MATEC Web Conf.* 2018, 203, 01005.
6. Fatimah, E.; Wahab, A.K.A.; Ismail, H. Numerical Modeling Approach of an Artificial Mangrove Root System (ArMS) Submerged Breakwater as Wetland Habitat Protector; COPEDEC: Dubai, United Arab Emirates, 2008; p. 20.
7. Marrone, J.; Zhou, S.; Brashear, P.; Howe, B.; Baker, S. Numerical and Physical Modeling to Inform Design of the Living Breakwaters Project, Staten Island, New York. In Proceedings of the Coastal Structures Conference 2019, Hanover, Germany, 29 September–2 October 2019.
8. Chien, A.; Wu, S.; Tseng, F.; Tang, A. Geotextile Tubes Application on Beach Nourishment in UAE. *Int. J. Environ. Sci. Dev.* 2014, 5, 506–509.
9. Rahman, A.; Womera, S. Experimental and Numerical Investigation on Wave Interaction with Submerged Breakwater. *J. Water Resour. Ocean. Sci.* 2013, 2, 155.
10. Sharif Ahmadian, A. Numerical Models for Submerged Breakwaters. Chapter 1—Introduction. In *Numerical Models for Submerged Breakwaters*; Sharif Ahmadian, A., Ed.; Butterworth-Heinemann: Boston, MA, USA, 2016; pp. 1–15.
11. Sharif Ahmadian, A. Numerical Models for Submerged Breakwaters. Chapter 2—Fundamental Concepts. In *Numerical Models for Submerged Breakwaters*; Sharif Ahmadian, A., Ed.; Butterworth-Heinemann: Boston, MA, USA, 2016; pp. 17–27.
12. Shin, E.C.; Oh, Y.I. Coastal Erosion Prevention by Geotextile Tube Technology. *Geotext. Geomembr.* 2007, 25, 264–277.
13. Kiran, A.S.; Ravichandran, V.; Sivakholundu, K. Stability Analysis and Design of Offshore Submerged Breakwater Constructed Using Sand Filled Geosynthetic Tubes. *Procedia Eng.* 2015, 116, 310–319.
14. Henriquez, M. Artificial Surf Reefs. Master's Thesis, Delft University of Technology Stevinweg, Delft, The Netherlands, 2005.
15. Voorde, M.; Antunes do Carmo, J.; Neves, M. Designing a Preliminary Multifunctional Artificial Reef to Protect the Portuguese Coast. *J. Coast. Res.* 2009, 25, 69–79.
16. López, I.; Tinoco, H.; Aragonés, L.; García-Barba, J. The Multifunctional Artificial Reef and Its Role in the Defence of the Mediterranean Coast. *Sci. Total Environ.* 2016, 550, 910–923.
17. Black, K.; Mead, S. Design of the Gold Coast Reef for Surfing, Public Amenity and Coastal Protection: Surfing Aspects. *J. Coast. Res.* 2001, 115–130.
18. Jackson, L.; Tomlinson, R.; Corbett, B.; Strauss, D. Long Term Performance of a Submerged Coastal Control Structure: A Case Study of the Narrowneck Multi-Functional Artificial Reef. *Coast. Eng. Proc.* 2012, 1, 54.
19. Black, S.M.; Kerry, A. Multipurpose, Artificial Reef at Mount Maunganui Beach, New Zealand. *Coast. Manag.* 1999, 27, 355–365.
20. Raised Water Research—Research, News and Advice about Making Waves. Available online: https://raisedwaterresearch.com/ (accessed on 9 June 2022).
21. Oh, Y.I.; Shin, E.C. Using Submerged Geotextile Tubes in the Protection of the E. Korean Shore. *Coast. Eng.* 2006, 53, 879–895.
22. González Leija, M.; Chavez, X.; Alvarez, E.; Mendoza, E.; Silva, R. Experimental Study on Geotextile Tube Applications as Submerged Breakwaters for Beach Protection in Yucatan, Mexico. *Coast. Eng. Proc.* 2014, 1, 25.
23. Sulaiman, D.M.; Bachtiar, H.; Taufiq, A.; Hermanto. Beach Profile Changes Due to Low Crested Breakwaters at Sigandu Beach, Central Java. *Procedia Eng.* 2015, 116, 510–519.
24. Gouaud, F. Geotextile Structures for Beach Protection Ashkelon, Israel; Corinthe Ingenierie: Grimaud, France, 2016.
25. Drimer, N.; Agnon, Y. An Improved Low-Order Boundary Element Method for Breaking Surface Waves. *Wave Motion* 2006, 43, 241–258.
26. Grilli, S.T.; Horrillo, J.; Guignard, S. Fully Nonlinear Potential Flow Simulations of Wave Shoaling Over Slopes: Spilling Breaker Model and Integral Wave Properties. *Water Waves* 2020, 2, 263–297.
27. Manolas, D.; Riziotis, V.; Voutsinas, S. Generation and Absorption of Periodic Waves Traveling on a Uniform Current in a Fully Nonlinear BEM-Based Numerical Wave Tank. *J. Mar. Sci. Eng.* 2020, 8, 727.
28. Yan, X.; Bingham, H.; Shao, Y. Finite Difference Solutions for Nonlinear Water Waves Using an Immersed Boundary Method. *Int. J. Numer. Methods Fluids* 2021, 93, 1143–1162. (Note: paper text cites this as "Xu [28]" in-line on p.2, but the reference list byline is Yan, X. et al. — likely an author-order/typo discrepancy in the original paper; flagged, not corrected.)
29. Yuan, D.; Tao, J. Wave Forces on Submerged, Alternately Submerged, and Emerged Semicircular Breakwaters. *Coast. Eng.* 2003, 48, 75–93.
30. Geng, T.; Liu, H.; Dias, F. Solitary-Wave Loads on a Three-Dimensional Submerged Horizontal Plate: Numerical Computations and Comparison with Experiments. *Phys. Fluids* 2021, 33, 037129.
31. Neves, A.; Taveira-Pinto, F. Wave Loads and Performance of Submerged Breakwaters. In *Water Engineering for a Sustainable Environment*; International Association of Hydraulic Research: Madrid, Spain, 2009. (Note: in-text citation on p.2 refers to this as "Pinto and Neves [31]"; reference-list byline order is Neves, A.; Taveira-Pinto, F. — same discrepancy noted as above.)
32. Van Steeg, P.; Vastenburg, E.W. Large Scale Physical Model Tests on the Stability of Geotextile Tubes; Deltares Report 1200162-000; Deltares: Utrecht, The Netherlands, 2010.
33. Jones, L.; Klamo, J.; Kwon, Y.; Didoszak, J. Numerical and Experimental Study of Wave-Induced Load Effects on a Submerged Body Near the Surface. In Proceedings of the ASME 2018 37th International Conference on Ocean, Offshore and Arctic Engineering, Madrid, Spain, 17–22 June 2018.
34. Bezuijen, A.; Vastenburg, E. Geosystems: Design Rules and Applications; CRC Press: Boca Raton, FL, USA, 2012; p. 144.
35. OpenFOAM. Available online: https://www.openfoam.com/ (accessed on 11 July 2022).
36. Chen, G.; Xiong, Q.; Morris, P.J.; Paterson, E.G.; Sergeev, A.; Wang, Y.-C. OpenFOAM for Computational Fluid Dynamics. *Not. Am. Math. Soc.* 2014, 61, 354.
37. Density of Sand in Kg/M3: Density of Dry Sand, Loose Sand, Packed Sand & M Sand. Available online: https://dreamcivil.com/density-of-sand/ (accessed on 13 September 2022).
38. Courant, R. Über die Anwendung der Variationsrechnung in der Theorie der Eigenschwingungen und über neue Klassen von Funktionalgleichungen. *Acta Math.* 1926, 49, 1–68.

**References most directly relevant to the reef survey (priority for web follow-up):** 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 32, 34.

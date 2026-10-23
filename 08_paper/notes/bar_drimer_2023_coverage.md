# Bar & Drimer (2023): every project it names, coverage against our 13 reefs, survey entries for the rest, and the paper's own findings

Status: 2026-10-15, paper round 1, Task A (Sonnet 5.5 agent). Scratch files: /tmp/claude-0/paper/bd23/ and /tmp/claude-0/paper/bd23cov/ (not in the repo).
Related notes (do not duplicate): `08_paper/notes/drimer_force_model.md` (full equation list of the BELWF model, written by the earlier agent), `08_paper/notes/israel.md` (Ashkelon detail), `08_paper/notes/drimer_2026_forces.md`.

## 0. Source and verification levels

[BD23] Bar, D.; Drimer, N. (2023). Preliminary Design Tools for Hydrodynamic Aspects of Submerged Impermeable Breakwaters. J. Mar. Sci. Eng. 11(2), 236. https://doi.org/10.3390/jmse11020236. Received 13 Nov 2022, published 17 Jan 2023 (PDF p.1). CC BY (PDF p.1). 22 PDF pages. Local copy: `Initial info from Lior/JMSE1100236DesignToolsSubmergedImpermeableBreakwaters2023BarDrimer - paper with good summary of wrtifical reefs around the world.pdf` (read only). Text layer read with pdftotext and PyMuPDF; Figures 5, 6 and 11 viewed once as rendered pages (values read by eye, marked "by eye").

Honest description of the paper: Lior's folder name calls it "paper with good summary of artificial reefs around the world". It is not a survey. The whole world survey is one paragraph (PDF p.2, Introduction, lines "Over the last twenty years ..." to "... Ashkelon shoreline [24]"). The other 18 pages develop and validate a 2-D boundary-element wave-flume model (BELWF) for geotextile tubes (Geotubes) as submerged impermeable structures.

Verification levels used below:
- READ = the cited source's own text was opened and the number checked.
- ABSTRACT = only abstract or search summary reached; source paywalled or host blocked.
- CARD = taken from the repo's reef card `02_research/reefs/<slug>.md` (earlier agents' work; its own sources are listed there).
- VENDOR = manufacturer page; treat as promotional.

## 1. Bottom line

1. [BD23] names 8 built projects (3 "multifunctional artificial surf reefs" and 4 Geotube detached breakwaters, plus Ashkelon), and 3 more named projects or studies that are only in the reference list (Living Breakwaters Staten Island [7], a Portuguese multifunctional reef design [15], a Mediterranean multifunctional reef study [16]). Section 2 lists all with reference numbers.
2. Only 3 of the 8 (Narrowneck, Pratte's Reef, Mount Maunganui) are among our 13 reefs. Our other 10 (Cables, Opunake, Boscombe, Kovalam, Borth, Palm Beach, Albany, Burkitts, Bunbury Airwave, Mexico 2026) are not in [BD23].
3. The 5 [BD23] projects we do not hold as one of the 13 are not surf reefs. Young-Jin, Yucatan, Al Aqah and Sigandu are Geotube shore-protection breakwaters. Ashkelon is a cliff-foot geotube protection. Reef cards for the first four already exist (`02_research/reefs/*.md`); they are not in the 13-reef page set. Section 4 gives a short survey entry for each, re-checked against open sources where possible.
4. [BD23]'s claim "most of the projects have failed" (p.2) is borrowed from Raised Water Research [20], not shown in the paper. Our own table (08_paper/data/reefs.json, `surf_outcome`) supports it for soft (geotextile or inflatable) reefs: none of 7 soft reefs is rated "works" (3 "does not work", 3 "works rarely", 1 "mixed/disputed"), while 3 of the 4 rock reefs with a verdict are rated "works". DERIVED tally, see section 5.
5. Findings of [BD23] that can be used in the paper: (a) a sliding-stability index SI and its critical instant, just before breaking, in a deep trough, when an up-wave horizontal force coincides with uplift; (b) uplift and horizontal loads vs wave height for a large tube pair (numbers in section 6.4); (c) a design example with Iribarren number 0.17 where the tube still turns a spilling-range wave into a plunging breaker; (d) validation scatter (BELWF 5 to 15% above OpenFOAM in SI). The paper has no transmission coefficients, no scour, burial or fabric analysis, no surf-quality analysis, and releases no code or data.

## 2. Every project, structure or site named in [BD23]

"Where" gives the PDF page of [BD23]. Reference numbers are [BD23]'s own.

| # | Named in [BD23] | Ref no. | Where | Category in [BD23] |
|---|---|---|---|---|
| 1 | Narrowneck, Queensland, Australia | [17] Black & Mead 2001 (J. Coast. Res. 115-130, as printed); [18] Jackson et al. 2012 | p.2 | multifunctional submerged ASR from Geotubes |
| 2 | Pratte's Reef, El Segundo, California | [14] Henriquez, M. MSc thesis, TU Delft (printed year 2005; other papers cite 2004, not confirmed) | p.2 | ASR |
| 3 | Mount Maunganui Beach, New Zealand | [19] Black, S.M.; Kerry, A. 1999, Coastal Management 27, 355-365 | p.2 | ASR |
| 4 | Young-Jin beach, east coast of Korea | [21] Oh & Shin 2006, Coastal Engineering 53, 879-895 | p.2 | Geotubes as detached breakwaters |
| 5 | Yucatan, Mexico | [22] Gonzalez Leija et al. 2014, Coastal Eng. Proc. 1, 25 | p.2 | Geotube detached breakwaters |
| 6 | Al Aqah Beach, Fujairah, UAE | [8] Chien et al. 2014, Int. J. Environ. Sci. Dev. 5, 506-509 | p.2 (also p.1, as a cost example for non-rubble solutions) | Geotube detached breakwaters |
| 7 | Sigandu Beach, Indonesia | [23] Sulaiman et al. 2015, Procedia Eng. 116, 510-519 | p.2 | Geotube detached breakwaters |
| 8 | Ashkelon shoreline, Israel (2018, "first project of Geotubes structure in Israel", aimed at beach and cliff erosion) | [24] Gouaud, F. 2016, Geotextile Structures for Beach Protection Ashkelon, Israel, Corinthe Ingenierie, Grimaud, France | p.2 | Geotubes |
| 9 | Living Breakwaters, Staten Island, New York | [7] Marrone et al. 2019, Coastal Structures Conf., Hanover | p.1 | "living breakwaters" (alternative to rubble mound) |
| 10 | Portuguese coast multifunctional reef (design) | [15] ten Voorde, Antunes do Carmo, Neves 2009, J. Coast. Res. 25, 69-79 | p.2, with [14,16] | general ASR literature |
| 11 | Mediterranean coast multifunctional reef (study) | [16] Lopez, Tinoco, Aragones, Garcia-Barba 2016, Sci. Total Environ. 550, 910-923 | p.2 | general ASR literature |
| 12 | "Raised Water Research" review website | [20] https://raisedwaterresearch.com/ (accessed 9 June 2022 by the authors) | p.2 | source of "most of the projects have failed" |

Types named without a site (no survey entry needed, one line each in section 4.9): floating breakwaters [1,2], Bragg breakwaters [3], submerged reef balls [4,5], artificial mangrove root system [6], submerged breakwater modelling [9-11], Geotube general [12,13] (Shin & Oh 2007; Kiran et al. 2015). Geotube stability experiments: Van Steeg & Vastenburg [32] (Deltares 1200162-000, 2010). Geotube geometry: Bezuijen & Vastenburg [34] (CRC Press 2012, p.144).

The two simulation cases in [BD23] (section 3.1 and 3.2) are generic, not real sites (section 6).

## 3. Comparison with our 13 reefs

| Our reef (slug) | In [BD23]? | Note |
|---|---|---|
| narrowneck-gold-coast | yes [17,18] | card cites Jackson et al. ICCE 2012 and Blacka et al. 2013 |
| prattes-reef-el-segundo | yes [14] | [BD23] gives only the thesis; our card uses the monitors' own paper |
| mount-maunganui-reef | yes [19] | |
| cables-reef-wa, opunake-reef, boscombe-surf-reef, kovalam-reef-india, borth-coastal-defence-reef, palm-beach-gold-coast, southern-ocean-surf-reef-albany, burkitts-reef-bargara, bunbury-airwave, mexico-reef-2026-unnamed | no | 10 of 13 are not in [BD23] |

[BD23] items without one of the 13 reef slugs, and what the repo holds:

| [BD23] item | Repo holds | Status |
|---|---|---|
| Young-Jin Korea | `02_research/reefs/young-jin-beach-geotube-korea.md/.json` | card exists; section 4.1 re-checked against the open 8ICG paper |
| Yucatan Mexico | `yucatan-geotube-mexico.md/.json` | card exists; section 4.2 re-checked |
| Al Aqah UAE | `al-aqah-beach-geotube-uae.md/.json` | card exists; section 4.3 (manufacturer source) |
| Sigandu Indonesia | `sigandu-beach-breakwaters-indonesia.md/.json` | card exists; section 4.4 (paper itself not reachable) |
| Ashkelon Israel | `02_research/israel/ashkelon-geotubes-2018.md`, `08_paper/notes/israel_geotubes_netanya.md` | detailed; section 4.5 is a summary, see `israel.md` |
| Living Breakwaters | none | new entry section 4.6 |
| Portugal MFAR design [15], Babilonia/Guardamar MFAR study [16] | none | new entries 4.7, 4.8 |
| Other repo cards not in [BD23] | `al-yasat-aali-island-uae`, `icm-california-headlands-unnamed`, `icm-queensland-sandbag-cliff`, `icm-uae-submerged-reef`, `japanese-artificial-reef-program`, `walkable-geotube-breakwater-unnamed` | extra leads from earlier discovery, not part of this task |

## 4. Survey entries for the projects we do not cover

Format: type, year, location, purpose, material, size, outcome, citations, verification. All numbers carry their source.

### 4.1 Young-Jin beach, Gangneung, Gangwon-do, east coast of Korea (Geotube detached breakwaters)

- Type: submerged, double-lined geotextile-tube detached breakwaters. Shore protection, not a surf reef.
- Year: not stated in the source. The paper (published 2006) already reports 12 months of monitoring after installation, so construction was about 2004-2005 (DERIVED from publication date; ASSUMPTION).
- Place: Young-Jin (Yeongjin) beach, east coast of Korea (8ICG p.2, "see Figure 1"; municipality from CARD).
- Purpose and motivation: severe erosion damaging "shoreline scenic views" and public property (8ICG p.1-2). The existing near-shore breakwater used tetrapods and "relatively heavy duty equipment is required" (8ICG p.2). The geotube was chosen as a cheaper, faster alternative (8ICG p.1, citing Pilarczyk 1996 and Heibaum 2002).
- Material: woven geotextile, weight at least 700 g/m2 (Table 1); fill sand specific gravity 2.64, D10 0.50 mm, USCS SP, interface friction angle (dry) 34.7 degrees, internal friction angle (wet) 32.0 degrees (Table 2, 8ICG p.2). Filled by a cutter-suction dredge with a 20 cm pipe, about 500 m3/hour (8ICG p.3).
- Size: "double lined geotextile tubes ... installed in about 3.0 m of water, 90-100 m distant from the shoreline"; one tube 50 m long and 1.8 m in diameter (effective height 1.8 m); four twin (double) units spaced 20.0 m; covers 240 m of shoreline; design adopted after hydraulic model tests: "double lined geotextile tube installed with zero-water depth above the crest" (8ICG p.3-4). One tube was filled in under one hour (p.4). Tube count 8 is DERIVED (4 twin units).
- Outcome (12 months): shoreline extended about 2.4-7.6 m seaward and seabed sand accumulated around the tubes (abstract, p.1 and p.4). At BM1 the shoreline advanced about 5.3 m in 3 months, then re-eroded; the authors speculate this arises from changed tidal flow direction and velocity caused by the installation; BM3 and BM4 similar but smaller re-erosion (p.4). Seaweed inhabited the tube surface after one year (p.4). "The long-term effectiveness ... cannot be judged until more time has passed" because of severe storms on this coast (p.4).
- Cost, contractor, financier: not stated (CARD agrees).
- Citations: Oh, Y.I.; Shin, E.C. (2006). Application of submerged geotextile tubes for erosion prevention in east coast of Korea. In Kuwano & Koseki (eds), Geosynthetics, Proc. 8th Int. Conf. on Geosynthetics (8ICG), Millpress, Rotterdam, pp. 757-760. Open PDF: https://library.geosyntheticssociety.org/wp-content/uploads/resources/proceedings/C.2.03%20Application%20of%20submerged%20geotextile%20tubes%20for%20erosion%20prevention%20in%20east%20coast%20of%20Korea.pdf (READ, 4 pages). Oh, Y.I.; Shin, E.C. (2006). Using submerged geotextile tubes in the protection of the E. Korean shore. Coastal Engineering 53(11), 879-895, https://doi.org/10.1016/j.coastaleng.2006.06.005 (the paper [BD23] cites; paywalled, NOT read).
- Why it matters for us: zero-freeboard soft structure, ~3 m depth, local re-erosion next to the structure, no durability record. Only 12 months of data.

### 4.2 Yucatan coast (Progreso area), Mexico (Geotube submerged breakwaters)

- Type: geotextile tubes as low-crested or semi-submerged breakwaters for beach restoration, not surf reefs.
- Year: field installation 2005 (4 km of tubes installed "by September 2005", Geosynthetics Magazine 2006); further sites 2005-2007 (ICCE 2014 poster). The paper [BD23] cites, González Leija et al. 2014, is a laboratory flume study (poster), not the field project.
- Place: northern Yucatan coast, Mexico; the most developed zone is near Progreso (Geosynthetics Magazine 2006).
- Purpose: stop shoreline retreat of "about 1 m per year and more" over the past 15 years; federal Beach Rehabilitation Program started 2001 (Geosynthetics Magazine 2006).
- Material: woven polypropylene geotextile tubes with a scour apron (Geosynthetics Magazine 2006).
- Design inputs (Geosynthetics Magazine 2006): breaking wave height Hb < 1.0 m (93% occurrence); Tz 4 to 8 s (93%); bed slope tan(theta) 0.1% to 0.5%; tide range 0.90 m; littoral drift 60,000 m3/yr; D50 0.30 mm. The authors computed the Iribarren number and found spilling breakers; crest set so that high-tide freeboard avoids reflection ("too high -> reflection; too low -> effect disappears"). Tube dimensions in this article not extracted (CARD: height 0.9 m, width 1.85 m, cross-section 1.4 m2 at 70% fill; not re-read).
- Outcome: mixed. ICCE 2014 poster: "in some cases shore protection and beach stabilization was achieved ... but in other places the results have been far from the expected"; a downdrift "shadow effect" is shown in its Figure 2; tubes set at negative freeboard of about -0.3 m relative to MSL.
- Laboratory findings that are quotable (ICCE 2014 poster, concluding remarks): wave transmission coefficient depends only on the ratio of submergence depth to incident wave height; geotextile structures act like impermeable concrete ones; "if they are crowned well below the mean water level, the waves steepen and break more violently"; recommended freeboard "not more than twice the dominant wave height". Flume: 37 x 0.80 x 1.20 m, UNAM, 1:5 and 1:10 scales (CARD for scales).
- Cost, contractor: not found. Designer of the field project: Alvarez, Rubio, Ricalde (authors of the 2006 and 2007 papers; role not stated in the text read).
- Citations: Alvarez, E.; Rubio, R.; Ricalde, H. (2006). Back to the beach in Mexico (Shoreline restored with geotextile tubes as submerged breakwaters). Geosynthetics Magazine, 1 June 2006, https://geosyntheticsmagazine.com/2006/06/01/shoreline-restored-with-geotextile-tubes-as-submerged-breakwaters/ (READ). Alvarez, E.; Rubio, R.; Ricalde, H. (2007). Beach restoration with geotextile tubes as submerged breakwaters in Yucatan, Mexico. Geotextiles and Geomembranes 25(4-5), 233-241, https://doi.org/10.1016/j.geotexmem.2007.02.005 (not read). Gonzalez (Gonzalez Leija), M.; Chavez, X.; Alvarez, E.; Mendoza, E.; Silva, R. (2014). Experimental study on geotextile tube applications as submerged breakwaters for beach protection in Yucatan, Mexico. Coastal Engineering Proceedings 34 (printed "1"), poster 25, https://doi.org/10.9753/icce.v34.posters.25, PDF https://icce-ojs-tamu.tdl.org/icce/article/download/8011/pdf_806 (READ, 1-page poster). Note: [BD23] prints "Coast. Eng. Proc. 2014, 1, 25"; the proceedings volume is 34.

### 4.3 Al Aqah Beach, Fujairah, UAE (Geotube groin and submerged breakwater)

- Type: geotextile-tube "anti-U" structure: reconstructed groins plus a seaward submerged breakwater, for beach nourishment and erosion control. Not a surf reef.
- Year: cyclone Gonu hit in 2007; case-study timeline "2010-2014" (ACE page); papers 2013 (WIT) and 2014 (IJESD).
- Place: Al Aqah, Fujairah, Gulf of Oman side of the UAE; client Le Meridien Hotel (ACE page).
- Purpose: after cyclone Gonu, erosion for "several kilometers"; riprap groins "turned out to sink due to the repeated wave actions and yearly unexpected cyclone attacks" (ACE page).
- Material and size: ACETube geotextile tubes; two arms each 200 m long, a "228 m x 225 m safe zone"; tube circumference 8.6 to 17.2 m, length 52 to 77 m; filled in situ with sand (ACE page). Crest depth, fill height, volume: not found.
- Outcome: manufacturer states erosion "well-controlled" and the coast protected from cyclones; no independent monitoring found (VENDOR). [BD23] gives no outcome.
- Cost, contractor: not found. (A 2008 USD 2 M hotel amenities spend in CARD is not the structure cost.)
- Citations: ACE Geosynthetics, Beach Nourishment, Fujarah, UAE, case study (2010-2014), https://www.geoace.com/case/Marine-and-Coastal-Structures-Construction/Beach-Nourishment,-Fujarah,-UAE (READ, VENDOR). Chien, A.; Wu, S.; Tseng, F.; Tang, A. (2014). Geotextile tubes application on beach nourishment in UAE. Int. J. Environ. Sci. Dev. 5(5), 506-509, https://doi.org/10.7763/IJESD.2014.V5.535 (ijesd.org host not reachable here; ABSTRACT level via CARD). Chien, A.; Tseng, F.; Tang, A. (2013). Geotextile tube application on beach refurbishment in UAE. WIT Trans. Ecol. Environ. 169, 231-239, https://doi.org/10.2495/CP130201 (not read).

### 4.4 Sigandu Beach, Batang Regency, Central Java, Indonesia (low-crested Geotube breakwaters)

- Type: low-crested geotextile-tube breakwaters, shore protection.
- Year: installation from September 2014 (paper abstract as recorded in CARD and in a search-result summary of the Academia.edu abstract page); paper 2015.
- Place: Sigandu Beach, about 4 km from the centre of Batang, north coast of Java (Solmax case study, 19 Jan 2023).
- Purpose: tourism beach eroding, attributed to the jetty of Batang Commercial Port (abstract); beach receded about 5 m in 8 years (Solmax).
- Material and size (VENDOR, Solmax): GEOTUBE GT1000ML, circumference 9.5 m, design filled height 1.5 m, length 25 m, on a scour apron (GT500MSA) with two pilot tubes; non-woven inner liner. Number of tubes, crest depth, offshore distance: not found.
- Outcome (abstract only): about one month after installation, rapid sedimentation formed salients and tombolos behind the structures; beach profiles by repeated cross-section surveys. Longer-term outcome: not found. A later paper by the same group, Sulaiman et al. (2017) "Lessons learned from deploying low crested breakwaters in North Coast of Java", Asian and Pacific Coasts 2017, pp. 445-454, https://doi.org/10.1142/9789813233812_0041, might hold it (not read).
- Citations: Sulaiman, D.M.; Bachtiar, H.; Taufiq, A.; Hermanto (2015). Beach profile changes due to low crested breakwaters at Sigandu Beach, Central Java. Procedia Eng. 116, 510-519, https://doi.org/10.1016/j.proeng.2015.08.320 (ScienceDirect full text returned HTTP 403, not bypassed; ABSTRACT level). Solmax (2023). GEOTUBE breakwaters: shoreline protection at Sigandu Beach, Indonesia, https://www.solmax.com/en/apac/case-studies/geotube-breakwaters-shoreline-protection-at-sigandu-beach-indonesia (READ, VENDOR).

### 4.5 Ashkelon, Israel (cliff-foot geotubes, "first geotube project in Israel")

- Type: submerged geotextile-tube structure in five clusters of 48 tubes at the foot of the eroding Ashkelon cliff, temporary protection. Not a surf project.
- Year: contractor began July 2017, completed September 2019 (State Comptroller 2020, PDF p.71 and p.83, READ). MCCP and the press give other dates (see `israel.md`).
- [BD23] says only: "In 2018, the first project of Geotubes structure was established in Israel, aimed at mitigating beach and cliff erosion along the Ashkelon shoreline [24]" (p.2). The cited report is a design report (Gouaud 2016, Corinthe Ingenierie); no copy found online (searches 2026-10-15 returned nothing naming Gouaud or Corinthe with Ashkelon).
- Outcome: "several of the geotubes were damaged and torn shortly after being laid ... after the winter storms, and had to be repaired" (Comptroller 2020, p.71, READ). Cost of construction about NIS 11 M. The 2024 comptroller follow-up report says the geotube protection collapsed in Ashkelon North (p.29). Full story, numbers and sources: `08_paper/notes/israel.md` section 5.
- Citations: State Comptroller of Israel (2020), Local government audit reports 2020, chapter on coastal cliff collapse, PDF pp.71 and 83; Gouaud 2016 (as in [BD23] ref [24], not found online).

### 4.6 Living Breakwaters, Tottenville, Staten Island, New York (nature-based breakwaters)

- Type: eight partially submerged breakwaters of armor stone and "ecologically enhanced concrete units", with "reef ridges" and "reef streets" for habitat; sand replenishment. Coastal risk reduction plus ecology, no surfing.
- Year: construction began 2021 (search summary of project pages); completion announced by the NY Governor in September 2024 (press release, READ).
- Size and cost: 2,400 linear feet of breakwaters, USD 111 M, designed to reduce waves reaching buildings and roads to below three feet (about 0.9 m) (NY Governor press release, READ). Hydrodynamic modelling used (press release). Each structure about 400 ft long per project home page (search summary; not opened).
- Design papers: Baker, Brashear, Tschirky, Marrone, Larson (2018). Design and physical model studies of innovative living breakwaters. Coastal Engineering Proceedings 36, paper 59, https://doi.org/10.9753/icce.v36.papers.59 (abstract only). [BD23] cites Marrone et al. 2019, Coastal Structures Conference, Hanover (not accessed).
- Outcome: too recent for performance data; oyster seeding planned 2025-2026 (search summary).
- Citation (READ): Governor Hochul announces completion of $111 million coastal resiliency project on Staten Island, press release, https://www.governor.ny.gov/news/governor-hochul-announces-completion-111-million-coastal-resiliency-project-staten-island (date shown in the search listing: 27 September 2024; page date not re-checked).
- Relevance: a rock-plus-ecological-concrete submerged breakwater; compare with Israeli ECOncrete use (`israel.md` section 7).

### 4.7 Portugal multifunctional artificial reef (design study, not built as far as found)

- Type: design study for a multifunctional artificial reef (surf and coastal protection) on the Portuguese coast.
- Citation: ten Voorde, M.; Antunes do Carmo, J.; Neves, M. (2009). Designing a preliminary multifunctional artificial reef to protect the Portuguese coast. J. Coast. Res. 25(1), 69-79, https://doi.org/10.2112/07-0827.1 (listed in [BD23] as "Voorde"). Follow-up: Antunes do Carmo, Neves, ten Voorde (2011), J. Coast. Conserv. 15(1), 99-112, https://doi.org/10.1007/s11852-010-0124-1. Neither read; open PDF of the 2009 paper listed at LNEC repository (host not reachable here). Whether anything was built: not found. Verification: bibliographic only.

### 4.8 Babilonia beach, Guardamar del Segura, Alicante, Spain (Mediterranean multifunctional reef design study)

- Type: design method for multifunctional artificial reefs (MFAR), applied to a case study.
- Year: paper 2016.
- Content (abstract as relayed by the University of Alicante record via a search summary): MFARs are built around the world; many failed, possibly because local conditions were not in the design formulas; the paper gives engineers a design method; case study Babilonia beach, an eroding developed shoreline; the reef gives a recreational surfing use usable "60% of the time" by surfers of low to intermediate skill.
- Citation: Lopez, I.; Tinoco, H.; Aragones, L.; Garcia-Barba, J. (2016). The multifunctional artificial reef and its role in the defence of the Mediterranean coast. Sci. Total Environ. 550, 910-923, https://doi.org/10.1016/j.scitotenv.2016.01.180; open version in University of Alicante repository hdl.handle.net/10045/63070 (file download returned HTTP 401, not bypassed). ABSTRACT level only; figures such as the 60% value must be confirmed in the full text before use.
- Relevance: the closest published analogue to a microtidal Mediterranean surf-reef design with a surfer-skill statement. High priority to obtain the full text (Lior via browser or the authors).

### 4.9 Types named without a site (for completeness)

- Floating breakwaters [1,2]; Bragg breakwaters [3]; submerged reef balls [4,5] (Armono 2003, Canadian Coastal Conf.; Na'im et al. 2018, MATEC Web Conf. 203, 01005, a short review of submerged breakwaters); artificial mangrove root system (ArMS) [6] (Fatimah et al., COPEDEC Dubai 2008). [BD23] says these "may present potential advantages in cost, hydrodynamics and environmental features" (p.1). None read.

## 5. [BD23]'s "most of the projects have failed" tested against our data

[BD23] p.2: "in a comprehensive review provided by the 'Raised Water Research' [20], it seems that most of the projects have failed. Common reasons for failure are related to too-small size Geotubes installed or the loss of effectiveness due to sand coverage [18,20]." The paper gives no list, count or definition of "failed" and no figure.

DERIVED tally from `08_paper/data/reefs.json`, field `surf_outcome` (a reading by the dataset agent of the cited sources, not a measurement):
- Soft structures (sand-filled geotextile bags or containers, inflatable): Narrowneck (works rarely), Pratte's (does not work), Mount Maunganui (works rarely), Opunake (does not work), Boscombe (works rarely), Kovalam (mixed/disputed), Bunbury Airwave (does not work). Result: 0 of 7 "works", 3 "does not work".
- Rock structures: Palm Beach (works), Albany (works), Burkitts (works, natural basalt reshaped), Cables (mixed/disputed), Borth (unknown), Mexico 2026 (unknown). Of the four with a verdict, 3 "works".
- Reading: the statement holds for surf outcome of soft reefs. It is silent on coastal-protection outcome (Narrowneck is judged a coastal-protection success in our card). ASSUMPTION: "failed" in [BD23] means "did not give the expected surf or protection benefit".

## 6. The paper's own findings

### 6.1 What it is
BELWF: fully nonlinear 2-D potential-flow Lagrangian boundary-element wave flume, after Drimer & Agnon (2006, Wave Motion 43, 241-258), extended to filled Geotube sections and to pressure and force output. Two normal vectors per node to run closer to breaking (p.3). Valid only while the domain is simply connected, i.e. up to breaking (p.2-3). Funded by The Israel Ports Development & Assets Company Ltd., grant 2031167 (p.12). Data availability: "not applicable" (p.12); code not released.

### 6.2 Geometry and material inputs (p.3-6)
- Geotube section after Bezuijen & Vastenburg [34]: empty tube width = half the circumference; full (FA = 1.0) circle of radius R = circumference / (2 pi); practical filling ratio 0.60-0.85, flat underside, quadrant sides, semi-elliptical top (p.3).
- Wet saturated sand density 2082 kg/m3, from a sand-density web page, ref [37] (p.6). Low-confidence input.

### 6.3 Equations (numbering as printed; full set in `drimer_force_model.md` section 4.2)
- (1) N = Fg - Fb - Fz; (2) F_mu = N mu_min = Fy; (3) SI = mu_min = Fy / (Fg - Fb - Fz) (p.5-6). Fz positive = uplift. SI is the minimum seabed friction coefficient to prevent sliding; negative SI = suction toward the incoming waves, "a common mode of failure of breakwaters" (p.8).
- (4) Fc = L_contact (P_UW + P_DW)/2, (5) SIc = Fy / (Fg - Fb - Fz - Fc): adds dynamic pressure acting under the tube; "safer to assume" it does; the larger of SI and SIc is the design value (p.10-11).

### 6.4 Numerical results (validation case, p.6-8; values from Figs. 5 and 6 read by eye, kN as labelled, length basis not stated)
Case: two tubes, total width 12 m, each R = 3.425 m, FA = 0.8 giving height 3.8 m; depth 5 m, freeboard 1.2 m; T = 7 s; H = 0.3 to 1.6 m measured 13.6 m before the structure (p.6-7).

| H (m) | max abs horizontal load Fy (kN) | max uplift Fz (kN) | SI (BELWF) | SI (OpenFOAM) |
|---|---|---|---|---|
| about 0.3 | about 7 | about 13 | about 0.016 | about 0.020 |
| about 1.0 | about 28 | about 48 (OF about 51) | about 0.066 | about 0.063 |
| about 1.5-1.6 | about 44.5 (BELWF, H 1.6); OF about 38 (H 1.5) | about 64 (OF about 65) | about 0.106 (H 1.6) | about 0.087 (H 1.5) |

Text statements: good agreement for max uplift; BELWF about 10% higher horizontal loads at high waves; SI 5% to 15% higher for H 0.8 to 1.5 m (p.7); minimum friction about 15% higher than OpenFOAM in Figs. 7-9, "safe and conservative for preliminary design" (p.8). Critical state in all cases: a deep trough near the tube, negative (up-wave) Fy with positive (uplift) Fz (p.8). Run times: OpenFOAM 207,777 cells, 4-42 h per wave simulation; BELWF 839 elements, 2-3 h (Table 1, p.6).

DERIVED from the table above (by-eye readings, +/- 10%): (Fg - Fb) = Fy/SI + Fz is about 450-485 kN at the three wave heights, a consistent value, so uplift Fz is only about 3% (H 0.3 m) to 13% (H 1.6 m) of the submerged weight for this large pair, and SI never exceeds about 0.11. For comparison the fill sand against geotextile has an interface friction angle of 34.7 degrees (tan = 0.69, Oh & Shin 2006 8ICG Table 2, dry; a different interface from tube-on-seabed, so only an order-of-magnitude comparison). Large tubes in moderate waves are therefore far from the sliding limit; the paper does not address smaller tubes.

### 6.5 Design example (p.10-11, Fig. 10-11)
T = 9 s; generated H = 2.2 m; shoals from 16 m depth over a 1:40 slope to a 4 m shelf; wave of 2.86 m reaches a single tube 11 m wide, 2.2 m high, freeboard 1.8 m; Iribarren number 0.17 ("spilling breaker" range) but "the Geotube steepens the wave and causes a plunging breaker"; 1160 nodes, about 40 h run (p.10). Critical SI and SIc occur just before the wave breaks (green marker t/T = 8.16 in Fig. 11). By eye: peak SI about 0.17, SIc about 0.31, minimum SI about -0.05 in the trough phase. DERIVED check: L0 = g T^2/(2 pi) = 126.5 m; xi0 = (1/40)/sqrt(2.86/126.5) = 0.166, matches the printed 0.17 (so the printed value uses the 2.86 m wave at the toe, not the generated 2.2 m wave which gives 0.19).

### 6.6 What is NOT in [BD23] (do not cite it for these)
Wave transmission or reflection coefficients; scour, burial or sand coverage; tube fabric stress, seams or tearing (the tube is a rigid impermeable body, A44); surf quality; peel angle; field data; code or data. Failure causes named are only "too-small size Geotubes" and "loss of effectiveness due to sand coverage" (p.2, borrowed from [18,20]).

### 6.7 Sentences usable in our paper (all CC BY, cite [BD23])
- Geotubes "may serve, for instance, as groins, detached breakwaters, dune foot protection and submerged reefs" (p.1-2).
- The most critical sliding state occurs "typically just before breaking" (abstract; p.8; Conclusions p.11).
- At the critical instant "a negative (to the up-wave direction) horizontal load occurs simultaneously with a positive (uplift) vertical load" (p.8).

## 7. Suggested use in the paper (for the writer)

1. Appendix D (reefs in [BD23] not built as surf reefs): one table row per section 4 entry, flagged "shore protection, not surf".
2. Materials section: use section 6.4 numbers as the only published wave-load numbers for a submerged tube pair, with the unit and by-eye caveats.
3. Do not state that [BD23] shows tubes tear. It models sliding only (see `drimer_2026_forces.md`).
4. Use the Yucatan poster and the Young-Jin paper for "soft structures at zero or negative freeboard make waves steepen and break more violently" (ICCE 2014 poster concluding remark 2; Young-Jin zero-freeboard design).

## 8. Gaps and open items

- Obtain López et al. 2016 full text (surfer-skill 60% statement; Babilonia reef geometry and design wave); likely the most relevant external design study for a microtidal Mediterranean reef.
- Oh & Shin 2006 (Coastal Eng.), Sulaiman et al. 2015 (Procedia Eng.), Chien et al. 2014 (IJESD), Alvarez et al. 2007 (Geotext. Geomembr.), Gouaud 2016: not read; every number above for these projects comes from the open companion sources named in each entry.
- Henriquez thesis year: 2005 in [BD23], 2004 in other papers; not confirmed.
- Date of the NY Governor press release not read from the page text.

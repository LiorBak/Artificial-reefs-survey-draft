# Drimer "2026" wave-force paper on geotextile tubes: search result, closest sources, and how to apply the Drimer force model to our reefs

Status: 2026-10-15, paper round 1, Task B (Sonnet 5.5 agent). Scratch: /tmp/claude-0/paper/drimer26/, /tmp/claude-0/paper/zalul/.
Companion notes: `08_paper/notes/drimer_force_model.md` (earlier agent: full BELWF equation list, standard stability formulas for rock and geotextile containers, search log of 7 web searches), `08_paper/notes/bar_drimer_2023_coverage.md` (section 6, the same model, numbers read from the figures), `08_paper/notes/israel.md`.

## 1. Bottom line

1. The paper Lior describes (same author, 2026, a model of wave forces, most wave power at the break, lifts a geotextile tube up and then down, which is why most tear) was NOT FOUND. I searched Crossref (all Drimer-authored works since mid-2023), Semantic Scholar, Google-type web search in English and Hebrew, and the Technion and Zalul pages that could be reached. Nothing matches. Details and queries in section 2. A dead-end entry is logged in `02_research/dead_ends/_paper_general.json`.
2. What exists from the same author: (a) Bar & Drimer 2023 (JMSE 11, 236), the model that gives the "lifting" result (section 4); (b) a Drimer expert opinion of 17 Nov 2024, attached to a 2025 appeal against the Kiryat Haim breakwaters, which discusses geotubes at Haifa Bay in words, with no force model (section 3); (c) four 2025-2026 Drimer papers on other topics (section 2.3), one of them an artificial-reef stability paper (not geotubes).
3. Best reading of Lior's statement: it summarises [BD23], possibly with a talk or the 2024 opinion, and the "2026" is a misdate or a paper not yet indexed. [BD23] supports the sliding half: the critical load is just before breaking, in a deep trough, when an up-wave horizontal force coincides with uplift. It does not model fabric stress, seams or tearing (the tube is a rigid body). So "lifts up and down, which is why most tear" is Lior's inference, not a published result we can cite. Ask Lior for the title or DOI he saw.
4. Application to our reefs: the model cannot be run (no code). A screening method and the inputs we have and lack are in section 5.

## 2. Search log

### 2.1 Queries and access
| Step | Result |
|---|---|
| Crossref API, `query.author=Drimer`, journal articles since 2023-06 (3 pages of 100) | 14 Drimer-named hits, only 6 are Nitai Drimer (list in 2.3); the rest are other people named Drimer. No geotube paper after [BD23]. |
| Crossref `query.bibliographic` "Drimer geotube", "Drimer geotextile tube breaking waves", "Bar Drimer submerged breakwater" | Only [BD23] (doi 10.3390/jmse11020236) and Drimer & Agnon 2006 (Wave Motion 43, 241-258, doi 10.1016/j.wavemoti.2005.09.006). |
| Crossref scan of 2025-2026 works with geotextile/geotube in the title and wave/uplift/breaking/failure/damage keywords (5 queries) | No Drimer or Bar author. Leads by others in 2.4. |
| Semantic Scholar author search "Nitai Drimer" | one profile ("N. Drimer", 25 papers); paper list not retrievable (rate limit 429 on paper calls). |
| OpenAlex API | HTTP 429 (daily budget exhausted); not used. |
| arXiv API | host not resolvable from this environment. |
| WebSearch x9 (English, Hebrew; "Drimer 2026 geotextile tube wave loads uplift tearing", "Daniel Bar Technion CAMERI PhD geotextile", "Bar Drimer 2026 JMSE geotextile", Hebrew "דרימר גיאוטיוב מודל כוחות גלים שבירה הרמה נקרע", etc.) | Only [BD23] each time. The earlier agent's 7 searches gave the same. |
| Technion pages `meeng.technion.ac.il/en/member/nitai-drimer/` (WebFetch: DNS error; curl: "Request Rejected ... BOT security violation") | blocked; NOT bypassed (project rule). Publication list therefore not seen. |
| Google Scholar profile of Drimer (appears in search results) | not fetched (bot-check expected; not attempted). Lior can open it in his browser. |
| MDPI article page for [BD23] | proxy 403 (host policy), per the earlier agent; local PDF used. |

### 2.2 Query strings that gave nothing (for the dead-end file)
"Drimer 2026 geotextile tube wave loads breaking waves uplift tearing numerical model"; "Nitai Drimer Technion Geotube submerged breakwater breaking wave forces fabric stress 2025 2026"; "Drimer geotextile hydroelastic OR fluid-structure breaking wave uplift journal 2026"; "Daniel Bar Technion CAMERI PhD geotextile tube submerged breakwater wave loads Ashkelon geotubes damage failure analysis"; "Bar Drimer 2026 Journal of Marine Science and Engineering geotextile OR Geotube wave loads uplift sliding plunging breaker submerged"; Hebrew "דרימר גיאוטיוב מודל כוחות גלים שבירת הגל הרמה של הצינור נקרע טכניון מאמר 2026"; plus the earlier agent's 7.

### 2.3 Drimer-authored 2025-2026 outputs found (Crossref, DOIs verified by lookup)
| Output | Relevance |
|---|---|
| Bar, D.; Drimer, N. (2026). SWAN-WEC: Introducing an Innovative Design for a Deep Water Point Absorber Wave Energy Converter. J. Mar. Sci. Eng. 14(10), 870, published 7 May 2026. https://doi.org/10.3390/jmse14100870 | Wave energy converter. NOT about geotubes (abstract read via Crossref: deep-water point absorber, two degrees of freedom). The earlier agent's "off-topic" verdict is correct. This is the only 2026 Bar & Drimer paper found. |
| Tal, A.; Drimer, N. (2026). A New Concept for Docking Vessels. J. Mar. Sci. Eng. 14(4), 329, 8 Feb 2026. https://doi.org/10.3390/jmse14040329 | Vessels. Not relevant. |
| Berman, O.; Zavadsky, A.; Drimer, N.; Shashar, N.; Wang, G.; Tarazi, E. (2025). A pure ceramic 3D printed artificial reef: stability and response. J. Cleaner Production 523, 146380, Sept 2025. https://doi.org/10.1016/j.jclepro.2025.146380 | Artificial-reef modules (ceramic, 3D printed). Abstract via search summary of BGU record: two reef sets at 15 m and 23 m depth tracked by photogrammetry, towing-tank tests, loads estimated as a function of wave energy and depth. Stability of reef modules, not geotubes, not the breaking zone. ABSTRACT level. |
| Gur, Y.; Israel, A.; Drimer, N.; Tarazi, E. (2026). Design thinking and innovative design tools for seaweed cultivation: the culture pod. The Design Journal, https://doi.org/10.1080/14606925.2026.2708256 | Aquaculture. Not relevant. |
| Castillo, K.A.; Gafter, R.; Wang, G.; Drimer, N. (2026). Experimental assessment of connector system of a modular floating structure. Lecture Notes in Civil Engineering (5th World Conf. on Floating Solutions), https://doi.org/10.1007/978-981-92-0084-9_14; and Gafter et al. (2026), doi 10.1007/978-981-92-0084-9_10 | Floating structures. Not relevant. |

### 2.4 2025-2026 geotextile-tube leads by other authors (found in Crossref, NOT read)
- Li, W.; Liu, L.; Deng, G. (2026). Back-calculation of a failure in multilayered stacked geotextile tubes using DEM-CFD. Int. J. Geomechanics (April 2026), https://doi.org/10.1061/ijgnai.gmeng-11852.
- Hasbullah, H.; Shaari, M.F.; Abdullah, M.A. (2025). Finite element analysis (FEA) of hydrodynamic wave impact on non-dewatering geotube model. CFD Letters 18(1), 113+, https://doi.org/10.37934/cfdl.18.1.113.
- Mao, W.-L.; Zhang, L.; Wang, T.-W. (2026). Experimental study of seepage-scour failure in geotextile tubes gap with damaged vertical sidewall. PLOS One, https://doi.org/10.1371/journal.pone.0352901.
- Pilarczyk, K.W. (2026). Geotextile forms for sand structures (chapter) in Geosynthetics and Geosystems in Hydraulic and Coastal Engineering, https://doi.org/10.1201/9781003762188-7; Stelljes, K.; Saathoff, F.; Heerten, G. (2026), New applications with nonwoven geotextile sand containers for soft coastal structures, in New Trends in Water and Environmental Engineering, https://doi.org/10.1201/9781003761990-53 (a one-page entry, Crossref).
- Older and directly on fabric stress or tube loads: Hosoi, Y.; Kobayashi, N.; Melby, J. (2004). Wave transmission and force on fabric tube breakwaters. Coastal Structures 2003 (ASCE), pp. 988-1000, https://doi.org/10.1061/40733(147)81 (abstract via search summary: model of breaking and transmission plus wave force on a one- or two-tube structure held by an anchored fabric shroud; computed peak fabric tension in fair agreement with measured tension; time variation of tension hard to predict because of "intermittent tube oscillations"). van Steeg, P.; Vastenburg, E.; Bezuijen, A.; Zengerink, E.; de Gijt, J. (2013). Large-scale physical model tests on sand-filled geotextile tubes and containers under wave attack. Coastal Structures 2011, World Scientific, pp. 1083-1094, https://doi.org/10.1142/9789814412216_0094 (bibliographic only; not confirmed to be the same work as [BD23] ref [32], Deltares report 1200162-000, 2010). Kiran, A.S.; Ravichandran, V.; Karpurapu, R. (2022). Stability of upper geotextile tube in a stacked formation under wave loading. Int. J. Geosynthetics and Ground Engineering 8(3), 32, https://doi.org/10.1007/s40891-022-00376-0 (abstract via search: the upper tube of a stack carries the maximum wave load). Recio & Oumeraci (2009), Coastal Eng. 56(5-6), 632-658, https://doi.org/10.1016/j.coastaleng.2009.01.011 (formulas in `drimer_force_model.md` section 5).

## 3. What Drimer himself says about geotubes in Israel (expert opinion, Nov 2024)

Source: Appeal ("ערר מס' 25 / ...", number not legible in the text layer) of Zalul (Israeli NGO) to the National Planning Council appeals sub-committee against the Coastal Environment Protection Committee decision of 21.05.2025 approving plan 304-0860023 (breakwaters at Kiryat Haim beaches, Haifa), filed 2 July 2025. PDF 28 pages, https://zalul.org.il/wp-content/uploads/2025/07/ערר-שוברי-גלים-קרית-חים-02.07.25.pdf (READ; Hebrew; page numbers are PDF pages). The appeal attaches "an expert opinion by Prof. Nitai Drimer, Technion Faculty of Mechanical Engineering since 2012, head of the ships and marine structures track, director of CAMERI 2001-2013, dated 17.11.2024" as Annex B (PDF p.1). The opinion itself (Annex B) is not on the pages I could reach; the appeal quotes it. (The appeal also prints the date "17.11.2025" once, PDF p.26, which must be a typo because the appeal is dated July 2025; ASSUMPTION.) A second opinion, Naama Sarid (GeoMare, M.Sc. marine geology), cover date November 2024, is at https://zalul.org.il/wp-content/uploads/2025/03/חוות-דעת-בנושא-חלופות-נעמה-שריד.pdf (READ).

Quotes (Hebrew as printed, English translation by me):
- PDF p.23: "בעקבות כשלים בשימוש ב-Geo-Tubes באשקלון, התגבשה דעה ש-Geo-Tubes אינם עמידים בתנאי ישראל. לדעתי דעה זו מוקדמת מדי ולא מבוססת. אין ניסיון מספיק וניתן גם לחזק את ה-Geo-Tubes. הייתי גם מנסה שילוב של גידולי ים שייצמדו ל-Geo-Tubes ויחזקו את המעטפת. האתר הנדון במפרץ חיפה ונתוני הגלים הפוקדים אותו נמוכים משמעותית מהחופים הפתוחים לאורך ישראל. לכן זאת נראית לי הזדמנות טובה לקידום השימוש ב-Geo-Tubes, שיטה עם יתרונות רבים על Rubble Mound ... במהירות ההקמה, צמצום הפרעות לציבור בחוף במשך הפרויקט, ואפשרות הזזה ופינוי."
  Translation: "Following failures in the use of Geo-Tubes at Ashkelon, an opinion formed that Geo-Tubes are not durable in Israeli conditions. In my opinion this view is premature and unfounded. There is not enough experience and the Geo-Tubes can also be strengthened. I would also try combining seaweed growth that attaches to the Geo-Tubes and strengthens the envelope. The site in question in Haifa Bay, and the wave data hitting it, are significantly lower than the open beaches along Israel. So this seems to me a good opportunity to promote use of Geo-Tubes, a method with many advantages over Rubble Mound ... in speed of construction, reduced disturbance to the public at the beach during the project, and the possibility of moving and removing."
- PDF p.15: "התכנון של רוחב המבנה והמרווח לפני המים נועד להנחית גלים גבוהים (שישברו בהשפעת המבנה) ולהעביר נמוכים. הגלים הגבוהים הם הגורמים לעיקר הארוזיה בחוף... בפרויקט הנדון נבדקו אמנם שוברי גלים מטובעים, אולם, לדעתי, לא מספיק רחבים. אני ממליץ לבדוק מערכים של מבנים מטובעים, יותר רחבים, וגם יותר רחוקים מהחוף."
  Translation: "The design of the structure width and the clearance below the water surface is meant to land high waves (that will break due to the structure) and pass low ones. The high waves cause most of the erosion on the beach ... In the project in question submerged breakwaters were examined, but in my opinion not wide enough. I recommend examining arrays of submerged structures, wider and also farther from the shore."
- PDF p.10: Drimer recommended submerged structures that "leave a clearance of 2 metres from the structure crest to the sea surface"; "it is possible and desirable to start with sand feeding and monitor the results, and if needed stabilise with submerged nature-based artificial structures"; "great potential benefit in examining solutions that were not examined at all or not examined enough" (appeal's paraphrase and quote, PDF p.10).
- Sarid opinion PDF p.4-5 cites Bar & Drimer 2023 for the statement that geotextile tubes proved effective as beach embankments and submerged breakwaters against erosion.

How to use: these are an Israeli expert's opinion that the Ashkelon failure does not condemn geotubes, with a hedge that tubes must be "strengthened", and that Haifa Bay waves are lower than the open coast. They contain no force model. They are an opinion document in a legal appeal, so cite as "expert opinion quoted in ...", not as a peer-reviewed source.

## 4. Does [BD23] support the mechanism? (summary; full test in `drimer_force_model.md` section 4.8)

Supports: the critical sliding instant is just before breaking (abstract; p.8; p.10-11; Fig. 11); the critical load combination is up-wave horizontal force plus positive uplift in a deep trough (p.8); dynamic pressure under the tube adds uplift (Eq. 4-5, p.10); the structure turns a spilling-range wave (xi = 0.17) into a plunging breaker (p.10).
Does not support: tearing, seam or fabric failure (rigid-body model); "most tubes tear" (the paper names too-small tubes and sand coverage as failure causes, p.2).

New numbers (DERIVED from by-eye readings of [BD23] Figs. 5-6; see coverage note section 6.4): for the validated large tube pair uplift is 3% to 13% of the submerged weight and SI stays at or below about 0.11. For the single 2.2 m tube of the design example (T = 9 s, 2.86 m wave at the toe, freeboard 1.8 m) the peak SIc is about 0.31, roughly three times the SI of the large pair at its largest wave. Both stay below tan(34.7 degrees) = 0.69 (Oh & Shin 2006 fill-sand interface, only an order-of-magnitude comparison).

DERIVED scaling remark (NOT in [BD23]; ASSUMPTION of geometric similarity at equal relative submergence and H/D): wave load per metre grows roughly with tube width D, weight with D squared, so the uplift-to-weight ratio and SI scale roughly as 1/D. A 1.5 m filled-height tube (Sigandu, Solmax GT1000ML, 9.5 m circumference) would then have about 2.5 times the SI of the 3.8 m tubes at the same relative loading. This matches [BD23]'s own reason for failures ("too-small size Geotubes", p.2) and gives a quantitative argument for Lior's insight (a) (small volumes do not work) for soft reefs. It needs the real BELWF or a flume test to be quantified.

Cycle count (DERIVED, simple arithmetic): at T = 9 s each tube sees about 9,600 load cycles per day (86,400/9) and about 29,000 in a 3-day storm. Whether such cycling tears a fabric depends on fabric and seam fatigue data, which [BD23] does not give; the State Comptroller 2024 attributes tube failures to fabric brittleness, poor laying or filling, and propeller, anchor and diver-knife damage (PDF p.9, footnote 25) and quotes the company that an unarmoured sleeve survives "months to a few years" versus about 30 years for the armoured prototype (PDF p.57; see `israel.md` section 5).

## 5. How to apply the Drimer model to our reefs

### 5.1 Which reefs are in scope
Only soft (geotextile tube or container) or inflatable structures where sliding, uplift or fabric loading is the question: Narrowneck, Pratte's, Mount Maunganui, Opunake, Boscombe, Kovalam, Bunbury Airwave (our 13), plus Ashkelon North, Young-Jin, Yucatan, Sigandu, Al Aqah (outside the 13). Rock reefs are covered by Hudson or van der Meer in `drimer_force_model.md` section 5.

### 5.2 Inputs the model needs
Structure: cross-section width, height, filling ratio (0.60-0.85), sand density (BD23 default 2082 kg/m3), seabed friction coefficient (the output SI is compared with it). Hydrodynamics: still-water depth at the structure in the worst tide, incident H and T at the structure, seabed slope in front, crest freeboard or submergence relative to the water level at that tide. The model handles one tube or a flat-topped group on a horizontal shelf.

### 5.3 What we have and lack (from `08_paper/data/reefs.json`; status in brackets: sou = sourced, der = derived, ass = assumed)
| Reef | Material | Reef height (m) | Crest depth below MSL (m) | Spring tide range (m) | Typical Hs (m), Tp (s) | Missing for the model |
|---|---|---|---|---|---|---|
| Narrowneck | sand-filled geotextile containers | 2.2 (der) | 2.32 (der) | 1.31 (der) | 1.0 (sou), Tp not given | container width, wave at crest, friction |
| Pratte's | sand-filled geotextile bags | 1.35 (der) | 2.68 (der) | 1.65 (der) | none | wave data |
| Mount Maunganui | sand-filled geotextile containers | 2.7 (ass) | 2.03 (der) | 1.75 (der) | 1.5 (sou), 11 (sou) | real container height |
| Opunake | geotextile bags/containers | 3.5 (sou) | not given | not given | 1.8-2.5 design wave face (sou) | crest depth, tide |
| Boscombe | sand-filled non-woven geotextile containers | 3.2 (der) | 0.9 (der) | 1.76 (sou) | 0.5 (sou), 4 (sou) | tube width, friction |
| Kovalam | geotextile containers (strips about 30 m long) | not given | not given | not given | 1-2.5 (sou), 11-15 (sou) | all geometry |
| Bunbury Airwave | inflatable Hypalon dome | 2.0 (sou) | 0.68 (der) | 0.4 (der) | none | wave data (not a tube) |
| Ashkelon North | sand-filled geotubes | not found | not found | about 0.4 spring (Rosen 2001) | storm Hs to about 5 m (see israel.md) | tube size, depth (Lior's guess 2-3 m is unsourced) |
| Young-Jin | double-lined tubes | 1.8 per tube | zero water depth above crest in about 3.0 m | not given | not given | wave data |
| Yucatan | PP tubes | 0.9 (card) | freeboard about -0.3 m (poster) | 0.90 (design basis) | Hb < 1.0 m, Tz 4-8 s | tube size confirmed |
| Sigandu | GT1000ML tubes | 1.5 filled | not found | not found | not found | most inputs |

### 5.4 Screening that can be done now (no model needed)
Step 1: compare local Hs with the crest depth at low and high water: H/h at the crest with a breaker index of about 0.78 (ASSUMPTION; common value for the ratio of breaking height to depth, not from [BD23]). Low-water depth = crest depth below MSL minus half the spring range (ASSUMPTION: symmetric tide). Examples (DERIVED from the dataset values): Mount Maunganui, Hs 1.5 m, crest 2.03 m below MSL, spring range 1.75 m: at MSL H/h = 0.74, at low spring (depth 2.03 - 0.88 = 1.15 m) H/h = 1.3 so waves break on the crest. Boscombe, Hs 0.5 m, crest 0.9 m below MSL, spring range 1.76 m: H/h = 0.56 at MSL, and the crest is at or above water at low spring tide (0.9 - 0.88 = 0.02 m), so the structure is a breaking-zone structure for most of the tide. Narrowneck, Hs 1.0 m, crest 2.32 m, range 1.31 m: H/h = 0.43 at MSL and 0.60 at low spring (depth 1.67 m).
Step 2: where the crest sits in or near the breaking zone, use [BD23] section 6.4 as the order of magnitude for loads and compare tube size with the 1/D scaling in section 4.
Step 3: for a quantitative SI, either obtain the BELWF code from the authors (nitaid@technion.ac.il is printed in the paper as corresponding author; sending e-mail is not allowed for agents, Lior would have to) or run a simple linear potential estimate and label it ESTIMATE, not DRIMER-MODEL.

### 5.5 What Haifa adds
Small tide (about 0.4 m spring, Rosen 2001) means the crest-to-surface clearance varies by less than half a metre, so one design freeboard is valid for the whole tide cycle, whereas Boscombe-type sites move through a range of 1.7 m. That narrows the load range but does not remove the breaking loads. See `israel.md` for the wave climate.

## 6. Open items

- Ask Lior for the exact title, DOI or venue of the "2026 paper" (or whether it was a talk or the 2024 opinion). If it exists, put the PDF in "new uploads from lior/" and redo section 4-5 against it.
- Annex B of the Zalul appeal (Drimer's full 17 Nov 2024 opinion) could contain more detail on geotubes and breaking; it is not on the Zalul pages I could reach (a Zalul page listing was fetched; only Herzliya opinions are linked there). Lior could ask Zalul.
- The Kiryat Haim appeal also mentions a CAMERI report for 2001-2013 dated 17.11.2024 as Annex B (PDF p.1 wording ambiguous: the date may belong to Drimer's opinion rather than to a CAMERI report). Not obtained.

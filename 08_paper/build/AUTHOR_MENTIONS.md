# Author mentions in the paper (review for professional wording)

Scope: `08_paper/sections/` (files in `ORDER.txt`), `08_paper/figures/*.caption.md`, and the text of `08_paper/build/paper.pdf` (97 pages; page numbers from PyMuPDF). The bibliography entries in the PDF were also checked, because they carry author-written notes. Quotes are verbatim from the source file; in bibliography rows they are as rendered in the PDF. Nothing was edited.

## Summary

Rows: 129 (one per distinct sentence or table cell; a sentence that appears in two places is listed once per place).

| category | rows |
|---|---|
| author decision | 16 |
| author observation | 37 |
| AI mention | 6 |
| methods statement | 2 |
| cited authors OK | 7 |
| other | 61 (mostly the neutral phrase "this review", plus internal file paths and process notes, see below) |

Searched and found: "Lior" and "Bakalo" (byline on PDF p.1; one label in Appendix E, PDF p.88); "author"/"author's" (many); "we", "I" as first person, "asked", "requested", "instruct" (except "course instructor"), "Claude", "Haiku", "Sonnet", "Opus", "agent", "prompt", "assistant", "the user", "per Lior": **no first-person or AI-tool hits**. "I" as a roman numeral ("Phase I", "Appendix I") and the initial "I" in "Oh, Y. I." were excluded.

Beyond the search terms, the check found internal file paths, QA notes and process wording in the text and bibliography ("08_paper/...", "notes/tides_check.md", "reef card", "project dossier", "working environment", "to be checked"). These are listed as "other" rows and should be removed before submission.

Caption files out of step with the PDF: `fig9_haifa_envelope.caption.md` still cites "Bakalo, 2025" and "notes/israel.md"; the PDF uses the Figure 12 caption from `07_israel.md` instead. `fig1`, `fig3`, `fig4`, `fig8` and `fig9` caption files are not in the PDF at all.

### The 5 worst wordings

1. **PDF p.88** (`appendix_E_lines.md:7`): "*Lior's cut decisions of 19 October 2026.*" A first name in a label. Change to "Cut decisions of 19 October 2026."
2. **PDF p.86** (`appendix_D_other_structures.md:53`): "The timing the author remembers (first winter after laying) matches Ashkelon North, so Ashkelon is the site used in this review." The site was chosen from recollection. Replace with a sourced selection criterion.
3. **PDF p.8 and p.57** (`02_methods.md:31`, `appendix_A_methods.md:5`): "...defined the research questions and the hypotheses to be tested, and directed the analysis." "Directed" is the phrase that reads as "Lior told the AI". Use "was responsible for the analysis".
4. **PDF p.48** (`build/references.bib:534` and `:576`): "first author's initial given as L. in 08_paper/lit/references.json and as A. in the Appendix references; to be checked" and "host was not reachable from the working environment". Internal QA notes inside a reference list. Delete them and fix the author initial in the source record.
5. **PDF p.5** (`01_introduction.md:15`): "This review responds to two requirements of the course instructor..." It reads as a course assignment. Reword as stated aims. The title block (PDF p.1, `00_front.md:5`) also names the course and instructor.

## Table

| # | PDF page | section file : line | exact sentence (verbatim, ≤40 words) | category | suggestion |
|---|---|---|---|---|---|
| 1 | 1 | sections/00_front.md : 3 | "author: "Lior Bakalo"" | other (byline) | keep |
| 2 | 1 | sections/00_front.md : 5 | "subtitle: "Course paper, SM-52080001 Introduction to Ocean Engineering (Prof. Nitai Drimer)"" | other (course framing; names the instructor) | keep only if the submission requires it; otherwise drop the instructor name |
| 3 | 1 | sections/00_front.md : 7 | "This review compiles the 13 surf reefs built or reshaped since 1997 with traced plan shapes, nine three-dimensional reconstructions and traceable sources." | other ("this review") | keep |
| 4 | 2, 8 | sections/02_methods.md : 29 | "## 2.7 Authorship and use of AI tools" | AI mention (section heading) | keep: required disclosure |
| 5 | 4, 95 | sections/appendix_F_leads.md : 1 | "# Appendix F. Author's leads and their status" | author observation (heading) | reword: "Appendix F. Working leads and their status" |
| 6 | 5 | sections/01_introduction.md : 11 | "The first reef counted in this review, Burkitts Reef at Bargara, Australia, is a natural platform reshaped by hand in 1997" | other ("this review") | keep |
| 7 | 5 | sections/01_introduction.md : 15 | "This review responds to two requirements of the course instructor: to give insight, computational where possible and following the theory of the course, into the effect of a reef on the waves and on surf quality" | author decision (work framed as set by an instructor) | reword: "This review addresses two aims: to give insight, computational where possible and grounded in coastal theory, into the effect of a reef on the waves and on surf quality" |
| 8 | 6 | sections/01_introduction.md : 17 | "The analysis was guided by eight leads from the author's own experience of built reefs and of the Haifa shore, labelled (a) to (h)" | author observation | reword: "The analysis was guided by eight working leads, drawn from experience of built reefs and of the Haifa shore, labelled (a) to (h)" |
| 9 | 6 | sections/01_introduction.md : 17 | "Sand moves strongly with the seasons; the author's unpublished field observation is a seasonal bed-level change of the order of 1 m at Haifa (Section 7)." | author observation | keep; state its basis in Section 7 (unpublished, not measured) |
| 10 | 6 | sections/01_introduction.md : 27 | "Appendix F lists the author's leads and their status." | author observation (leads) | reword: "Appendix F lists the working leads and their status." |
| 11 | 6, 72 | sections/02_methods.md : 5 | "*derived* (computed in this review from sourced inputs, a traced plan shape or a reconstructed three-dimensional model)" | other ("this review") | keep |
| 12 | 8 | sections/02_methods.md : 27 | "Every value is traced to a cited source, and the author's decisions are listed in Appendix A." | author decision | reword: "...and the decisions taken in this review are listed in Appendix A." |
| 13 | 8 | sections/02_methods.md : 27 | "No new field data were collected; the author's Haifa observations are used only in Section 7 and are labelled there." | author observation | keep (clearly labelled) |
| 14 | 8 | sections/02_methods.md : 31 | "The author selected and supplied the primary sources (…), defined the research questions and the hypotheses to be tested, and directed the analysis." | author decision | reword the last clause: "and was responsible for the analysis" (avoid "directed") |
| 15 | 8 | sections/02_methods.md : 31 | "AI tools assisted with source extraction, data compilation, computation and drafting." | AI mention | keep; name the tools and versions once |
| 16 | 8 | sections/02_methods.md : 31 | "Every source added by the AI tools was validated by the author, who also reviewed and confirmed all text, data, calculations and figures" | AI mention | keep (verification statement is good) |
| 17 | 8 | sections/03_survey.md : 5 | "By the classes of this review, three reefs work for surfing (Burkitts, Palm Beach, Albany)" | other ("this review") | keep |
| 18 | 9 | sections/03_survey.md : 7 | "Outcome classes are readings of the cited sources by this review (Appendix C)." | other ("this review") | keep |
| 19 | 12, 33 | sections/03_survey.md : 37 | "according to the founder, the seam opened a couple of days after installation and the wave "worked amazingly" until then (T. Bottegal, Airwave founder, pers. comm., 8 Oct 2026)." | author observation (personal communication) | keep; align with Appendix A (which calls it a spoken interview) and state the basis once |
| 20 | 13 | sections/03_survey.md : 53 | "The defences withstood the storms of December 2011 and show no damage in imagery of 2012-2024 (…; this review), but no surf record exists" | other ("this review") | keep |
| 21 | 13, 79 | sections/03_survey.md : 59 | "the containers were torn, deflated and sunk by 2013 (E. Rendle, pers. comm., 2013, in" | cited authors OK (third-party pers. comm., cited via Blacka et al.) | keep |
| 22 | 13, 79 | sections/appendix_C_data.md : 81 | "(E. Rendle, pers. comm., 2013, in" | cited authors OK (third-party pers. comm., cited via Blacka et al.) | keep |
| 23 | 15 | sections/04_surf_quality.md : 21 | "to 1:6.2 and 1:4.4 (derived in this review)" | other ("this review") | keep |
| 24 | 15 | sections/04_surf_quality.md : 25 | "at the break (method of this review)." | other ("this review") | keep |
| 25 | 15 | sections/04_surf_quality.md : 31 | "One of the author's leads (f; Appendix F) is that the depth gap alone does not decide the wave" | author observation (lead) | reword: "One of the working leads (f; Appendix F) is that..." |
| 26 | 17 | sections/04_surf_quality.md : 35 | "no source found quantifies the contrast between a gradual ramp and a sudden rise; the quantification is new to this review." | other ("this review") | keep |
| 27 | 17 | sections/04_surf_quality.md : 43 | "Boscombe tests the author's lead (d; Appendix F) that its structure rose too steeply and made a wave mostly for bodyboarders." | author observation (lead) | reword: "tests the working lead (d; Appendix F)" |
| 28 | 20 | sections/04_surf_quality.md : 55 | "The author's lead (a; Appendix F) is that reefs need a large volume and that small reefs such as Pratte's do not work." | author observation (lead) | reword: "The working lead (a; Appendix F) is that..." |
| 29 | 24 | sections/04_surf_quality.md : 71 | "Table 2. Computed wave indicators per reef (derived in this review; Appendix A)." | other ("this review") | keep |
| 30 | 25 | sections/04_surf_quality.md : 87 | "Table 3. Sustained breaking after the break point on five lines per reef (derived in this review; Section 4.3, Appendix A, Figure E2)." | other ("this review") | keep |
| 31 | 26 | sections/04_surf_quality.md : 101 | "Data: 08_paper/analysis/results_post_break.csv, results_post_break_summary.csv and results_post_break_lines.json (script post_break.py)" | other (internal file paths and script names) | remove the paths; cite the results in Appendix A |
| 32 | 26 | sections/05_sediment.md : 15 | "Our reefs span both regimes if the distance from the waterline to the crest (Appendix C) is taken as a rough proxy for" | other ("our") | reword: "The reefs in this review span both regimes..." |
| 33 | 27 | sections/05_sediment.md : 23 | "Table 4. Predicted and observed shoreline response (predictions derived in this review; observations from Section 5.3)." | other ("this review") | keep |
| 34 | 28 | sections/05_sediment.md : 39 | "For each, this review compared the lee with control stretches 1.5 to 3.5 reef lengths alongshore and, where possible, before with after." | methods statement | keep |
| 35 | 29 | sections/05_sediment.md : 43 | "from the beach-profile surveys of the @channelcoastal2026a, analysed in this review." | other ("this review") | keep |
| 36 | 29 | sections/05_sediment.md : 57 | "The author's lead (b; Appendix F) is that the Gold Coast reefs are claimed to protect the coast although the shoreline shows little change" | author observation (lead) | reword: "The working lead (b; Appendix F) is that..." |
| 37 | 30 | sections/05_sediment.md : 47 | "from the single-beam soundings of the @wadot2020 and beach-level surveys, analysed in this review." | other ("this review") | keep |
| 38 | 30 | sections/05_sediment.md : 61 | "The rock reef at Cables, on limestone bedrock, shows no toe scour or burial (this review)." | other ("this review") | keep |
| 39 | 31 | sections/05_sediment.md : 51 | "from the lidar terrain model of 19 March 2022 [@welshgovernment2022], analysed in this review." | other ("this review") | keep |
| 40 | 31 | sections/06_materials.md : 7 | "The author's lead (c; Appendix F) holds that soft structures do not survive long in the breaking zone." | author observation (lead) | reword: "The working lead (c; Appendix F) holds that..." |
| 41 | 31 | sections/06_materials.md : 7 | "none of the four rock reefs failed (Fisher exact test, $p$ = 0.015; derived in this review)." | other ("this review") | keep |
| 42 | 33 | sections/06_materials.md : 27 | "the next version will be concrete (T. Bottegal, Airwave founder, pers. comm., 8 Oct 2026)." | author observation (personal communication) | keep; align with 03_survey.md:37 and Appendix A |
| 43 | 33 | sections/06_materials.md : 31 | "A later paper by the same author on tube tearing, mentioned to this review, could not be located" | other (informal source) | reword: "A later paper by the same authors on tube tearing, reported in correspondence, could not be located" |
| 44 | 33 | sections/06_materials.md : 35 | "This review estimated the loads by integrating the linear incident-wave pressure over a rigid tube section" | methods statement | keep |
| 45 | 33 | sections/06_materials.md : 39 | "For the author's insight (e), that most wave power acts at the break and lifts the tube up and then down, which is why most tubes tear, the load part is supported" | author observation | reword: "For insight (e), that most wave power acts at the break..." |
| 46 | 34 | sections/06_materials.md : 39 | "The author's lead (c; Appendix F), that soft structures do not survive long in the breaking zone, is supported by both the record and the stability numbers." | author observation (lead) | reword: "The working lead (c; Appendix F), that soft structures..." |
| 47 | 35 | sections/07_israel.md : 7 | "The author's Shikmona buoy readings (summer 2025, a three-week sample) put the smallest surfable sea at $H_s$ 0.45 to 0.60 m … (author's observation)." | author observation | reword: "Unpublished readings from the Shikmona buoy (summer 2025, three weeks) put..."; cite the buoy's data owner, not the author |
| 48 | 36 | sections/07_israel.md : 15 | "(N. Drimer, as quoted in Zalul, 2025, p. 23; an expert opinion)" | other (names the course instructor as a cited expert) | check the conflict of interest; cite neutrally or drop if he is the instructor |
| 49 | 36 | sections/07_israel.md : 19 | "From daily visits to the Haifa shore the author has observed a seasonal bed-level change of about 1 m … this is a personal observation, not yet published or measured" | author observation | reword: "From site visits, an unpublished observation of a seasonal bed-level change of about 1 m; not yet published or measured" |
| 50 | 36 | sections/07_israel.md : 19 | "With geotextile reefs settling by 1 to 2 m (Section 5.5), burial is a central risk, as the author's lead (h-B; Appendix F) anticipated." | author observation (lead) | reword: "... as lead (h-B; Appendix F) anticipated" |
| 51 | 36 | sections/07_israel.md : 21 | "The author proposes to trap sand in the high-sand seasons (October and May, by the author's observation) and to build the reef on it under a geotextile sheet." | author decision (proposal) | reword: "A proposal is to trap sand in the high-sand seasons (October and May, from unpublished observation) ..." |
| 52 | 37 | sections/07_israel.md : 25 | "The largest uncertainty is the breaking criterion: the author's field observations (…) imply earlier breaking" | author observation | reword: "the unpublished field observations (Section 7.1)" |
| 53 | 37 | sections/07_israel.md : 27 | "the crest depths implied by the field breaking depths observed at Haifa by the author … unpublished field notes, 2025; Section 7.1" | author observation | reword: "observed at Haifa (unpublished field notes, 2025; Section 7.1)" |
| 54 | 37 | sections/07_israel.md : 29 | "Table 6. Screening envelope for a Haifa surf reef (derived in this review; Sections 4 to 7)." | other ("this review") | keep |
| 55 | 38 | sections/08_discussion.md : 3 | "The analysis started from eight leads of the author (Section 1.3); their status is tracked separately in Appendix F" | author observation (lead) | reword: "started from eight working leads (Section 1.3)" |
| 56 | 40 | sections/08_discussion.md : 29 | "To answer the question that motivates the review, which reefs have delivered what they promised, this review rated each reef on three criteria" | other ("this review") | keep |
| 57 | 40 | sections/08_discussion.md : 29 | "The scores are this review's assessment, based on the evidence cited in Sections 3 to 6 and Appendix C" | other ("this review") | keep |
| 58 | 40 | sections/08_discussion.md : 31 | "Table 7. Rating of the built surf reefs by this review (1 = very poor to 5 = very good; ? = no evidence; * = signal not attributable to the reef)." | other ("this review") | keep |
| 59 | 42 | sections/08_discussion.md : 49 | "The rating thus repeats the central result of this review: a surf reef that works is large, built of rock and given a long ramp, and its benefit is surfing rather than beach protection." | other ("this review") | keep |
| 60 | 42 | sections/08_discussion.md : 53 | "The sample is small (8 to 13 reefs), and the outcome classes are this review's readings of sources that are mostly by the designers" | other ("this review") | keep |
| 61 | 42 | sections/08_discussion.md : 53 | "The Haifa analysis rests on a synthetic profile and on unpublished observations of the author." | author observation | reword: "...and on unpublished field observations (Section 7)" |
| 62 | 42 | sections/08_discussion.md : 55 | "(5) Haifa breaking depths that confirm the early breaking observed by the author" | author observation | reword: "observed in unpublished field notes" |
| 63 | 43 | sections/09_conclusions.md : 3 | "In this review's rating (Section 8.4), rock reefs score best on safety and longevity, geotextile and inflatable reefs worst" | other ("this review") | keep |
| 64 | 46 | build/references.bib : 148 | "Private copy supplied by the author. The file prints neither venue nor year; both are taken from the citation recorded in the project files" | author observation (access note) + other (process note) | reword: "Copy held privately; venue and year from the publisher record" |
| 65 | 46 | build/references.bib : 196 | "abstract as recorded in the project dossier; full text not read" | other (internal note in reference) | delete the note |
| 66 | 46 | build/references.bib : 257 | "Private copy supplied by the author; design claims, not measurements." | author observation (access note) | drop "supplied by the author" |
| 67 | 48 | build/references.bib : 534 | "first author's initial given as L. in 08_paper/lit/references.json and as A. in the Appendix references; to be checked" | other (QA note in reference; internal path) | delete; fix the author initial in the source record |
| 68 | 48 | build/references.bib : 576 | "host was not reachable from the working environment; see 08_paper/notes/tides_check.md" | other (process note in reference) | delete the note |
| 69 | 49 | build/references.bib : 596 | "set-down coefficient as summarised in notes/fig3_theory.md" | other (internal file path in reference) | delete the note |
| 70 | 49 | build/references.bib : 678 | "08_paper/lit/references.json uses the ids mead_black2001a and mead_black2001c" | other (internal path in reference) | delete the note |
| 71 | 52 | build/references.bib : 1147 | "Private copy supplied by the author; the council site blocks automated access." | author observation (access note) | drop "supplied by the author" |
| 72 | 53 | build/references.bib : 1259 | "survey used in Section 5 is from the same DoT WA FR package (08_paper/analysis/SEABED_SEDIMENT.md); its listing should" | other (internal file path) | remove the path |
| 73 | 53 | build/references.bib : 1276 | "lower bounds; see 08_paper/notes/tides_check.md" | other (process note in reference) | delete the note |
| 74 | 53 | build/references.bib : 1291 | "against the decision of the Coastal Environment Protection Committee" | other (third-party decision) | keep |
| 75 | 53 | build/references.bib : 1292 | "quotes an expert opinion by N. Drimer of 17 November 2024" | other (names the course instructor as a cited expert) | check conflict of interest; cite neutrally |
| 76 | 54 | build/references.bib : 184 | "developer's account; content taken from the reef card, not re-read" | other (internal note in reference) | delete the note |
| 77 | 54 | build/references.bib : 354 | "company-supplied evidence; taken from the project dossier, not re-opened" | other (internal note in reference) | delete the note |
| 78 | 55 | build/references.bib : 782 | "year as recorded in this review's reef card; the copy read prints no date" | other (internal note in reference) | delete the note |
| 79 | 56 | build/references.bib : 1165 | "Surf reef decision has Opunake buzzing at tourism prospects" | other (third-party title) | keep |
| 80 | 56 | build/references.bib : 1167 | "Copy at h... ; author not printed" | other (author field left blank in the reference; check) | keep or complete the author field |
| 81 | 57 | sections/appendix_A_methods.md : 5 | "The author selected and supplied the primary sources (…), defined the research questions and the hypotheses to be tested, and directed the analysis." | author decision | same reword as 02_methods.md:31 |
| 82 | 57 | sections/appendix_A_methods.md : 5 | "AI tools assisted with source extraction, data compilation, computation and drafting." | AI mention | keep |
| 83 | 57 | sections/appendix_A_methods.md : 5 | "Every source added by the AI tools was validated by the author, who also reviewed and confirmed all text, data, calculations and figures" | AI mention | keep |
| 84 | 58 | sections/appendix_A_methods.md : 17 | "the decisions (D1, D2, ..., with who decided and why)" | author decision | reword: "with their rationale and date" |
| 85 | 58 | sections/appendix_A_methods.md : 19 | "The decisions taken by the author are marked D below (see Section 2.6 on the tools used)." | author decision | reword: "The decisions taken in this review are marked D below" |
| 86 | 61 | sections/appendix_A_methods.md : 69 | "Decision D7 (author, 10 October 2026): the default is the 2020 photograph trace, because it is the only evidence of the state actually built" | author decision | reword: "Decision D7 (10 October 2026): ..." |
| 87 | 62 | sections/appendix_A_methods.md : 101 | "decision D1 (author, 7 October 2026): the as-built bed at the reef is -3.6 m CD" | author decision | reword: "decision D1 (7 October 2026)" |
| 88 | 64 | sections/appendix_A_methods.md : 127 | "datum assumption strongly supported but not stated by the authors" | cited authors OK | keep |
| 89 | 65 | sections/appendix_A_methods.md : 145 | "the laser-survey edge (default, chosen by the author on 6 October 2026; 8,675 m^2^)" | author decision | reword: "chosen on 6 October 2026" |
| 90 | 66 | sections/appendix_A_methods.md : 171 | "a spoken interview with the founder (T. Bottegal, Airwave founder, pers. comm., 8 October 2026; an interested party)" | author observation (personal communication) | keep; align with 03_survey.md:37 |
| 91 | 68 | sections/appendix_A_methods.md : 223 | "A footprint proposed by another AI system was compared with the sources and rejected for Borth (200 by 200 m, 110,000 t; it matched neither drawings, lidar nor imagery)" | AI mention | keep (disclosure); "an AI tool" is plainer than "another AI system" |
| 92 | 69 | sections/appendix_A_methods.md : 231 | "This was resolved by decision D6 (author, 7 October 2026): the -3.0 and -4.0 m contours became controls" | author decision | reword: "decision D6 (7 October 2026)" |
| 93 | 72 | sections/appendix_C_data.md : 10 | "derived: computed in this review from sourced inputs, or from a traced plan shape or a reconstructed 3D model" | other ("this review") | keep |
| 94 | 72 | sections/appendix_C_data.md : 11 | "assumed: an assumption of this review, flagged in Appendix A (A-numbers)" | other ("this review") | keep |
| 95 | 72 | sections/appendix_C_data.md : 14 | "The outcome classes (works, works rarely, does not work, mixed or disputed, unknown) are this review's reading of the cited sources" | other ("this review") | keep |
| 96 | 72 | sections/appendix_C_data.md : 3 | "The table is compiled from the project dataset (files reefs.json and reefs_table.csv, held with the project files and available from the author)." | other (author; file names; availability) | reword: "available on request from the corresponding author"; move file names to a data-availability note |
| 97 | 78 | sections/appendix_C_data.md : 75 | "differ by less than the survey error (this review, from Department of Transport WA soundings)" | other ("this review") | keep |
| 98 | 78 | sections/appendix_C_data.md : 80 | "structure still present (…; this review, Appendix A.7)" | other ("this review") | keep |
| 99 | 82 | sections/appendix_D_other_structures.md : 3 | "Of the eleven projects and studies named in @bar2023, three (Narrowneck, Pratte's Reef and Mount Maunganui) are among our 13 reefs" | other ("our") | reword: "are among the 13 reefs of this review" |
| 100 | 82 | sections/appendix_D_other_structures.md : 3 | "the verification level of this review" | other ("this review") | keep |
| 101 | 82 | sections/appendix_D_other_structures.md : 5 | "ten of our reefs are not mentioned by them" | other ("our") | reword: "ten of the 13 reefs are not mentioned" |
| 102 | 83 | sections/appendix_D_other_structures.md : 25 | "which the authors attribute to changed tidal flow" | cited authors OK | keep |
| 103 | 84 | sections/appendix_D_other_structures.md : 37 | "the authors attribute the speed of the accretion largely to the port jetty and to dredged sediment" | cited authors OK | keep |
| 104 | 85 | sections/appendix_D_other_structures.md : 49 | "the authors' model predicts a maximum beach accretion of 33.2 m over 270 m of beach" | cited authors OK | keep |
| 105 | 86 | sections/appendix_D_other_structures.md : 49 | "the authors note that a microtidal site keeps the reef operable and rarely hidden" | cited authors OK | keep |
| 106 | 86 | sections/appendix_D_other_structures.md : 53 | "The figures of 10 dunam and 4 m height in the author's notes were not found in any source." | author observation (unsourced working notes) | delete the claim, or source it; do not cite the author's notes |
| 107 | 86 | sections/appendix_D_other_structures.md : 53 | "NIS 10.5 million in the author's notes." | author observation (unsourced working notes) | delete, or source it |
| 108 | 86 | sections/appendix_D_other_structures.md : 53 | "the count "15 of 48" in the author's notes and the count "17 by storms, 2 by boats" in an earlier repository dossier are unsupported" | author observation + other (internal dossier) | delete both counts and the "dossier" reference; state only what the sources say |
| 109 | 86 | sections/appendix_D_other_structures.md : 53 | "the author recalled torn tubes at Netanya in winter 2019; no source shows a geotube built or contracted at Netanya" | author observation (recollection) | drop the recollection or label it as unsourced; memory is not evidence |
| 110 | 86 | sections/appendix_D_other_structures.md : 53 | "The timing the author remembers (first winter after laying) matches Ashkelon North, so Ashkelon is the site used in this review." | author decision (site chosen on recollection; worst wording) | replace with a sourced selection criterion (state which documented first-winter failure qualifies Ashkelon North); remove the recollection |
| 111 | 86 | sections/appendix_D_other_structures.md : 57 | "A December 2017 committee decision limited stage 1 to sand feeding" | other (third-party decision, not the author) | keep |
| 112 | 87 | sections/appendix_D_other_structures.md : 65 | "as recorded in an earlier dossier of this review; the report was not re-opened and the entry is not verified" | other (internal dossier reference) | reword: "as recorded in an earlier internal note; not re-opened; not verified" |
| 113 | 88 | sections/appendix_E_lines.md : 5 | "For Albany, Cables and Borth the author fixed the cut on 19 October 2026 (the decisions are listed in the next paragraph)" | author decision | reword: "the cut was fixed on 19 October 2026 (decisions listed below)" |
| 114 | 88 | sections/appendix_E_lines.md : 7 | "*Lior's cut decisions of 19 October 2026.*" | author decision (first name in a label; worst wording) | remove the first name: "Cut decisions of 19 October 2026." |
| 115 | 90 | sections/appendix_E_lines.md : 76 | "68 m right of the plan middle (the plan includes the south oval mound); fixed by the author on 19 October 2026" | author decision (table cell) | reword: "fixed on 19 October 2026" |
| 116 | 91 | sections/appendix_E_lines.md : 98 | "18 m left of the plan middle; fixed by the author on 19 October 2026" | author decision (table cell) | reword: "fixed on 19 October 2026" |
| 117 | 94 | sections/appendix_E_lines.md : 120 | "DERIVED in this review (08_paper/analysis/post_break.py --fig; geometry in results_post_break_lines.json)" | other (internal code path in caption) | remove the paths; keep "derived in this review (method in Appendix A)" |
| 118 | 95 | sections/appendix_F_leads.md : 10 | "Gold Coast cannot be decided" | other (the word "decided" in a verdict) | keep |
| 119 | 95 | sections/appendix_F_leads.md : 3 | "Before the analysis, the author listed eight leads from personal experience of built reefs and of the Haifa shore" | author observation | reword: "Before the analysis, eight working leads were listed from experience of built reefs and of the Haifa shore" |
| 120 | 95 | sections/appendix_F_leads.md : 3 | "This appendix keeps track of each lead: what the evidence of Sections 3 to 7 says about it, and whether it is consistent with published work or new to this review (verdicts by this review)." | other ("this review") | keep |
| 121 | 95 | sections/appendix_F_leads.md : 5 | "Table F1. The author's leads (a) to (h) and their status (verdicts by this review)." | author observation (heading) | reword: "Table F1. Working leads (a) to (h) and their status" |
| 122 | 97 | sections/appendix_F_leads.md : 17 | "the 1 m is the author's personal observation from daily visits to the Haifa shore, backed by Google Earth satellite imagery" | author observation | reword: "the 1 m is an unpublished observation from site visits" |
| 123 | not in PDF (caption file only) | figures/fig1_plan_and_profiles.caption.md : 4 | "Build and data notes (not part of the caption)" | other (internal file paths in caption file) | delete the notes block from the caption file |
| 124 | not in PDF (caption file only) | figures/fig3_wave_sketch.caption.md : 5 | "re-run: python3 -I 08_paper/analysis/figures_wave.py" | other (internal command in caption) | remove; move to a code-availability note |
| 125 | not in PDF (caption file only) | figures/fig4_gap_ramp.caption.md : 5 | "Code: 08_paper/analysis/figures_results.py" | other (internal command in caption) | remove; move to a code-availability note |
| 126 | not in PDF (caption file only) | figures/fig8_stability.caption.md : 7 | "The "Drimer 2026" paper cited by the author was not found." | author observation (unresolved citation) | fix the citation or drop the sentence; not found in the PDF |
| 127 | not in PDF (caption file only) | figures/fig9_haifa_envelope.caption.md : 1 | "(Hs 0.45 to 0.60 m; Bakalo, 2025, unpublished field notes)" | author observation (self-citation; caption file out of step with the PDF) | the PDF already reads "by the author; unpublished field notes, 2025": align and drop the name |
| 128 | not in PDF (caption file only) | figures/fig9_haifa_envelope.caption.md : 6 | "the 1 m seasonal bed change is the author's unsourced observation (notes/israel.md derives 0.3 to 1.3 m)" | author observation + other (internal file path; caption file out of step with the PDF) | reword: "an unpublished observation (Section 7)"; drop the file path |
| 129 | not in PDF (caption file only) | figures/fig9_haifa_envelope.caption.md : 7 | "The deeper crest depths 1.2 to 1.5 m would be allowed if the author's field breaking depths hold (largest open uncertainty)." | author observation (caption file out of step with the PDF) | reword: "if the field breaking depths in Section 7.1 hold" |


## Notes on the method

- Each row was located by a normalised text match in the PDF; a row shows several pages where the sentence recurs.
- The "AI mention" rows describe the disclosure in Section 2.7 and Appendix A. They are factual and should be kept; the wording "another AI system" (Appendix A, p.68) is the only one that needs a tone check.
- "Cited authors OK" covers the authors of cited works and third-party personal communications quoted through a cited source.
- Figure caption rows marked "not in PDF (caption file only)" do not affect the PDF text but must be fixed in the caption files before rebuilding.

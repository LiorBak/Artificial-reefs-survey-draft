# Wording changes (from AUTHOR_MENTIONS.md, 2026-10-20)

Rows not listed were "keep" rows and are unchanged. Section 2.7 and Appendix A.0 (rows 4, 14-16, 81-83) were not touched.

| Rows | Change |
|---|---|
| 5, 10, 121, 119 | Appendix F title "Working hypotheses and their status"; Table F1 header "Hypothesis"; "leads" -> "working hypotheses" throughout |
| 7 | Introduction: "This review addresses two questions: ..." (no instructor) |
| 8, 55 | "eight working hypotheses, drawn from field experience and the literature" (Sections 1.3, 8, App. F) |
| 25, 27, 28, 36, 40, 45, 46, 50 | "The author's lead (x)" -> "Hypothesis (x; Appendix F) holds that ..." |
| 9, 13, 47, 49, 52, 53, 61, 62, 122 | Haifa observations -> "field observations by the author (Appendix G)"; Section 7.1 "about ten weeks, July to October 2025"; "(author's observation)" dropped |
| 51 | "A sand-trapping approach is proposed: ..." |
| 12, 84, 85 | "design choices ... (with their rationale)" instead of "the author's decisions / who decided" |
| 86, 87, 89, 92, 113-116 | Decision tags and dates removed ("Design choice D7:", "default;", "D6:"); Appendix E label "Placement of the cuts at Albany, Cables and Borth"; table cells lose "fixed by the author on 19 October 2026"; "analysis notes of the repository" sentence deleted. Heading "Assumptions and decisions" -> "Assumptions and design choices" |
| 91 | "another AI system" -> "an AI tool" |
| 43 | "same authors ... reported in correspondence" |
| 31, 72, 96, 117 | File paths removed (Section 4.3 data line now points to Appendix A and Figure E2; Appendix C "available from the author on request"; Figure E2 caption "method in Appendix A"; Appendix A "text-derived envelope ... exists in the project files" shortened) |
| 32, 99, 101 | "our reefs" -> "the reefs of this review" / "the 13 reefs" |
| 106-110, 112 | Appendix D (Ashkelon): author's notes, recollection and "dossier" removed; Ashkelon North justified by the State Comptroller's report of torn tubes in the first winter; "earlier internal note" |
| 64-78 | Reference notes cleaned in sections/10_references.md and bib_overrides.py (bib regenerated): "supplied by the author", dossier, reef card, file paths, "working environment" removed; "not verified" / "full text not read" kept. Row 67: Jackson et al. (2012) first author set to "Jackson, L. A." |
| 48, 75 | N. Drimer as quoted expert in Zalul (2025): kept (genuine third-party citation) |
| 123-129 | Build/data notes moved out of figures/*.caption.md into figures/build_notes/*.build_notes.md (not copied into the paper); "Drimer 2026" sentence dropped; fig9 caption file now identical to the Figure 12 caption in 07_israel.md, with "field observations by the author, Appendix G" |

Side fixes found while rebuilding: md2bib.py regenerates references.bib and had dropped hand-added entries. thesurf2023 (renamed from thesurfeye2023), marrone2019, isramar2025 are now entries in 10_references.md (reconstructed, check details) and dally1985 was added (full text not accessed). "≥" in Appendix A replaced by $\ge$. Build: no undefined citations, no missing characters.

Left for the Appendix G rewrite: it still prints "08_paper/data/haifa_breaking_depths.csv".

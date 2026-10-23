# Open issues for Lior (assembly round, 2026-10-19)

Status: assembly complete (no CHECKPOINT needed). Files written or edited in this round are listed at the end.

## For Lior to confirm or decide
1. **AI-tools sentence (Methods 2.6 and Appendix A.0).** The detailed statement "carried out by AI agents (Claude, Anthropic)" was replaced by one neutral sentence in Section 2.6: "Data extraction was assisted by AI tools under the author's supervision; every value was traced to a cited source, and the author's decisions are listed in Appendix A." Appendix A.0 item 6 now only says that decisions are marked D. The sentence on "another AI tool" (Gemini) in 2.1 and A.0 item 1 now reads "Values from secondary compilations whose cited sources could not be fetched and confirmed were not used." Please confirm the wording, or ask for more or less disclosure (course rules may require a specific statement).
2. **Length.** Main text (00-09) is about 16,800 words including tables and captions, plus 12 figures: about 33 pages at 500 words per page, or about 25-28 printed pages at 10.5 pt. The target was 15-20. Long captions were shortened (full captions remain in `figures/*.caption.md`). Further cuts would remove content, so they were not made without your decision. Candidates: (a) shorten the regional narratives of 3.2-3.5 to one paragraph per region (saves about 1,000 words); (b) move the theory of 4.1 (equations) to Appendix A (about 600); (c) move Table 4 (material and fate) to Appendix C, which already has Table C4 (about 380); (d) shorten Table 6 in the Discussion (about 300).
3. **Course name.** `00_front.md` gives "Course paper, Coastal Engineering"; replace it with the exact course name, number and instructor if needed.
4. **Rating (Section 8.3, Table 7).** Copied from `notes/rating_final.md` as approved. Open checks carried over from that file: Narrowneck crest level (-1.0 design vs -1.5 m AHD vs "1 m lowering"); Cables granite vs limestone (B unaffected); C used only as information, not in the rank. Pratte's B = 1 is kept although one YouTube witness says the bags were intact at removal; the text gives both accounts (Sections 3.5, 8.1).

## Data consistency notes (not errors introduced here; flagged for the record)
5. **Borth crest and outlines.** Table 1 and Appendix C give the reef crest 0.19 m above MSL and the volume 30,119 m³ of the 2022 laser-survey edge (8,675 m²); Table 2 (analysis model) uses a crest line over the highest rock, 1.09 m above MSL, and a model volume of 19,954 m³ (7,435 m² footprint); Figure 2 uses the 2024 photo edge for the plan area. The text now says so in the Figure 2 caption and the Table 2 notes.
6. **Palm Beach cost.** Section 3.2 gives AUD 18.2 M for the reef (Appendix C); Section 5.4 calls it "an AU$18 million nourishment project" (Royal HaskoningDHV, n.d.). Check whether the 18.2 M is the reef alone or the whole project. The A$13.2 M video claim was NOT used (the Palm Beach comment files were not written).
7. **Tide.** Section 7.1 said the Israeli tide is "as small as at Bunbury"; after the 2026-10-19 tide correction (Bunbury predicted annual range 1.20 m) it now says "smaller than at any built reef (1.1 to 4.3 m; Section 1.3)". Other tide numbers match `analysis/RESULTS.md` (Israel 0.40 m spring; Cables 1.14, Bunbury 1.20, Albany 1.38 m annual range).
8. **Borth peel-angle exception.** Section 4.4 and `analysis/FINDINGS.md` item 4 now state that Borth at H0 = 3 m reaches 61.9 deg (rating 3), the only case at or above 60 deg. (`FINDINGS.md` was edited because the brief named it explicitly.)

## References
9. All 139 list entries are cited and all in-text citations match the list (`citations_check.json`); three works cited only "as cited in" (Shand, 2011; Weppe et al., 2007; Geofabrics, 2013) are listed in a separate short section, without full entries (no full entry exists in the repo).
10. New entries: **Dan Harmon (2026)**, YouTube video "The $500k Surf Reef Failure", https://www.youtube.com/watch?v=DK7cqXDzLpM (channel name as recorded in `02_research/videos/cables-reef-wa/videos.md`; check that "Dan Harmon" is the channel name); **NZ Herald (2014)**, "Mount's artificial reef to be removed" (year from `notes/rating_evidence.md`; the copy read prints no date - verify).
11. Rosen (2001), van Steeg et al. (2011), Mead (2000), Verhagen (2012) and Barlow (2013) are cited and in the list. **Hudson (1959)** is not cited by author-year (the text says "Hudson formula" and cites US Army CERC, 1984, as tabulated by Verhagen, 2012), so it is not listed; add it only if you want the original cited.
12. Merged duplicates: Mead and Black (2001) without a letter = 2001b (breaking intensity); Channel Coastal Observatory (2026) split into 2026a (frontage data set, Section 5) and 2026b (2010 survey, Appendix A.7). Where two versions of an entry differed, the fuller one was kept; the verifier should check them.
13. YouTube testimony (Pratte's) is used as grade-D evidence only in Sections 3.5, 4.6 and 8.1/8.3. Palm Beach and Kovalam comment files were not written (YouTube bot check), so nothing from them is used.

## Notes for the builder
- Figure numbering in the text: Figures 1-12 in order of first mention, Figure B1 in Appendix B. File names do not match numbers for two figures: `fig8_stability.png` is Figure 11 and `fig9_haifa_envelope.png` is Figure 12.
- Tables 1-7 in the main text (Table 4 in Section 6, Table 5 in Section 7, Tables 6-7 in Section 8); appendix tables keep their A/C numbering.
- `00_front.md` starts with a YAML block (title, author, date, subtitle); pass it first so pandoc reads the metadata.

## Files written or edited in this round
- New: `00_front.md`, `08_discussion.md`, `09_conclusions.md`, `10_references.md`, `citations_check.json`, `ORDER.txt`, `appendix_B_3d.md`, `OPEN_ISSUES.md`.
- Edited: `02_methods.md` (AI sentences), `03_survey.md` (Pratte's testimony, Figure 1-2 captions, Borth note), `04_surf_quality.md` (Borth exception, Pratte's testimony, Table 2 Borth note, shorter captions), `06_materials.md` (Table 4, Figure 11 label and caption), `07_israel.md` (Table 5, Figure 12 label and caption, tide sentence), `appendix_A_methods.md` (AI sentences, Channel Coastal Observatory 2026b), `../analysis/FINDINGS.md` (item 4, Borth exception).

## Lior's reference checks (2026-10-19), applied
- Chien et al. (2014): DOI removed from `10_references.md` (it resolves to an unrelated paper); the entry and Appendix D.4 now say "as reported by Bar and Drimer (2023); original not verified".
- Oh and Shin (2006a, b): Appendix D.1 now states explicitly that it is a submerged geotube shore-protection example, not a surf reef (Section 6.4 uses it only for colonisation).
- Gouaud (2016): cited only through Bar and Drimer (2023) in Appendix D.10, now marked "not verified"; no list entry.
- ten Voorde et al. (2009) Fig. 14: `08_paper/lit/figs/` did not exist when this round ended, so no placeholder was added to `05_sediment.md` (coordinator to add).

## Senior-editor round 2 (2026-10-19, after the profile re-cut; RECUT_NOTES.md)
Done: numbers of the re-cut (Albany, Cables, Borth) carried into 00, 01, 02, 04 (text, Table 2, Fig. 3-7 captions), 05 (Table 3), 06 (Hudson values, Fig. 11 caption), 07 (sand observation, Fig. 12 caption), 03 (Fig. 1-2 captions), Appendix A item 4, Appendix C note 2, Appendix B caption. In-text captions now follow `figures/*.caption.md` in full (Lior: length is fine); Fig. 4 shows only Albany's second (take-off) cut. Discussion rebuilt on the findings (8.1 surf controls incl. post-break depth, 8.2 sediment, 8.3 durability, 8.4 rating = Table 6, 8.5 limitations, 8.6 implications); the lead-by-lead table moved to the new `appendix_F_leads.md` (Table F1; (d) "mostly", supported; (h) split into h-A and h-B). Conclusions 1 and 3 and the abstract rewritten per review points 6. ORDER.txt has appendices E and F. References: added Bowen et al. (1968), Longuet-Higgins & Stewart (1964), Peregrine (1983) (Fig. 3 caption) and Nettle (2017) (Appendix E, SE swell; Nettle 2019 stays, cited in Appendix C). `citations_check.json` regenerated (146 citations; two mis-keyed entries corrected: Prenzler et al. 2023, Spanier & Zviely 2022).

Open:
- "Rarely better than other surf spots in the area" (Conclusion 1, Section 8.4) rests on the narrow working windows (Prenzler et al., 2023; Raised Water Research, n.d.-b) and the author's judgement; no source compares Palm Beach or Burkitts directly with nearby breaks, and Hunt et al. (2022) report longer rides at Palm Beach than in the natural surf zone when it works (the text says so). Lior to confirm the wording.
- Post-break depth (Section 4.3, 8.1, Conclusion 3) is supported only by grade-D testimony and geometry; the 1-D model does not compute it.
- Fig. 12 caption: the caption file cites "Bakalo, 2025, unpublished field notes"; the text writes "observed at Haifa by the author (unpublished field notes, 2025)" so that no reference-list entry is needed for the author's own notes (APA personal-communication convention used elsewhere).
- Fig. 11 caption gives SI_c 0.20-0.56 (figure range), Section 6.3 text 0.37-0.56 (RESULTS 8.2 table); not reconciled here.
- Table C2 (master table) keeps the shallowest-point crest depths (Albany 1.00, Cables 1.55, Borth -0.19); Table 2 uses the surf cuts; both notes say so.
- Item 4 above: the rating table is now Table 6 in Section 8.4 (was Table 7 in 8.3).

# Lior's review of the PDF (2026-10-19) and the work plan

## Lior's points (condensed; his words in quotes)
1. Course: "SM-52080001 Introduction to Ocean Engineering, Prof. Nitai Drimer". DONE (00_front subtitle).
2. Length is fine; no cuts.
3. Authorship statement: the author supplied the sources to the AI tools and validated every external source the AI added. He read and confirmed all the text, added sources, collected surfer testimony (YouTube comments), told the AI which conclusions to look for, reviewed them, and compared the 3D models against figures. "make it sound professional and clear that I reviewed each part of it."
   - Appendix A: add a worked example of the 3D cross-checks, using the reef built from the most different source TYPES.
4. Figures:
   - Fig 3:
     - The water level shoreward of the break should go down a bit and then back up; it should not stay below 0 to the shore (check with theory via Haiku).
     - The lip in (a) is too heavy.
     - Add a second sketch ~1 s later; (b) must show its break, not a pre-break state.
   - Fig 4:
     - Lines look parallel and the axis labels are unclear.
     - Albany Y>1.6 but works? The Albany 2D cut is on the short part, not where the break is (too far left in fig1).
     - The Cables cut is not perpendicular to the shore; take the middle, shore-normal.
     - Move Borth a bit to the right. The other reefs are fine.
     - "should cause many changes in the paper".
   - Fig 5: no "(Lior)" on the figure; use the peel-angle paper (Hutt et al. 2001).
   - Figs 4-7:
     - Legends are needed for shapes and colours. 'Unknown' looks like 'works' (use dots).
     - With colour per reef, write the reef names in the same colour.
     - The shape legend can be given once for the section.
5. Section 8:
   - Not "The author's observations against the evidence". Move that to an appendix (to track the leads).
   - (h) part 2 (mobile sand) is the author's personal observation: he visits the sea at Haifa every day, backed by Google Earth imagery showing more sand accumulating north of the breakwaters.
   - (d) use "mostly" and flag it as supported. (e) is OK.
   - The Discussion should discuss the real findings; Lior "just gave leads to look into".
6. Section 9:
   - Distinguish Albany ("works great") from the other two ("don't work on most conditions, and rarely are better than other surf spots in the area").
   - Conclusion 3 (ramp, not gap): the post-break depth matters too. Pratte's commenters said the wave went deep again quickly and the shape was ruined, so the reef must stay shallow shortly after the break: a triangle, not a V shape.
7. References: proper APA formatting with hanging indent; preferably LaTeX with linked citations ("much more professional").

## Pipeline (agents)
- A Haiku: fig3 theory -> notes/fig3_theory.md
- B Sonnet: authorship statement (02_methods, appendix A.0) + 3D cross-check example (appendix A)
- C Opus: re-cut profiles (Albany, Cables, Borth), re-run analysis, fix figs 1, 3-7 -> analysis/RECUT_NOTES.md
- D Opus (after C):
  - update all numbers in sections 03-07 from RECUT_NOTES;
  - rewrite 08 Discussion on the real findings, with the insights table moved to a new appendix E "Author's leads and their status" (point 5);
  - rewrite 09 per point 6.
- E Sonnet (after D): convert citations to pandoc [@key] + references.bib/CSL (APA 7, hanging indent, linked citations); build via LaTeX (tectonic or xelatex if installable cheaply), else the HTML pipeline with citeproc; then Haiku spot-check and send the PDF.

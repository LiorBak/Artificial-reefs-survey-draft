# Brief: BROWSER QA of 04_build\artificial_reefs.html (round number given in your prompt)

Use the built-in browser pane (tools mcp__Claude_Browser__*; load the anthropic-skills:built-in-browser skill first). Serve the folder:
python -m http.server 8768 from 04_build in the background; stop it at the end. Also run python src\qa_shots.py --prefix round<N>.

## Checks (pass/fail with evidence)
- No console errors on load.
- Shapes tab: mega figure renders all drawings at one scale (compare the 100 m bars); each drawing shows confidence badge + reason +
  design version visibly; the confidence filter works (untick low -> low drawings disappear from the figure AND the table).
- Per-reef Shape check viewer, for at least 5 reefs: switch base images; the outline stays aligned with the image when the window is
  resized (check desktop and mobile widths - take screenshots and LOOK at them); opacity / colour / vertices / dimension toggles work;
  the live satellite view shows the polygon in the right place where geo exists; no-source reefs show the plain explanation.
- Videos tab: filters; a segment click loads the embed at that time; Relevant / Not relevant / Unsure + notes persist after reload;
  Export triggers a JSON download (check via JS that a Blob download is created); Import restores; the Images sub-section toggles work.
- Reef detail dialog shows media + the shape viewer; reference pop-ups still work.
- Mobile (resize_window preset mobile): no horizontal scroll; dark mode readable; reset the window afterwards.

Write 04_build\QA\round<N>_browser.md.
Severity: misaligned overlay, missing confidence reason, or a broken tab = blocker; broken control = major; cosmetic = minor.

## Final JSON
{"report_path","defects":[{"severity","where","what","how_to_reproduce","suggested_fix"}],"checks_passed":["..."],"verdict"}

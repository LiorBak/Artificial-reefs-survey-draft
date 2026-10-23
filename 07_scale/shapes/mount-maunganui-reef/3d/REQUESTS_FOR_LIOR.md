# Requests for Lior - Mount Maunganui Beach Reef 3D model (2026-10-10)

Nothing blocks the model; each item below would improve it. Ordered by effect on the model. Reasons: METHODS_3D.md sections 4 and 7.

1. **[DONE] D1 applied (2026-10-07): the as-built bed is an ASSUMPTION of -3.6 m CD, with an option "later seabed" -2.8 m CD.**
   Both are in the viewer bed selector (#bed=assumed | later | sens_-3.0 ... | nav) and are labelled everywhere. No source states the 2008-09 seabed at the reef; -3.6 m CD reproduces the stated 2,800 m3 (-3.51 survey+skirt, -3.66 toe loft). Mead et al. (2007) Fig 12 (Oct 2006, unfinished reef) reads the bed beside the reef at 2.0-3.7 m (datum unstated), which supports the shallower option. The crest (-0.9 m CD) stays below even LAT (-0.03 m CD) in every bed option.

2. **[DONE] Mead, Black and Moores (2007) (P2) and Mead and Borrero (2011) (P3) read.**
   P2 gives design and construction facts and the Oct 2006 survey of the unfinished reef (no as-built outline, no datum). The "design 6,500 m3 vs as-built 2,800 m3" figure is Fig 3 of P3, not P2. It has an unlabelled grid, no scale or date, and fits the ASR toe outline (IoU 0.87, grid about 10 m), so it corroborates the toe version and was not traced as a new version.

3. **[DECISION] Make the as-built toe outline (ASR "Installed", 1,424 m2) the default outline instead of the 2013 multibeam -2.0 m outline (1,071 m2)?**
   The toe outline is now confirmed by two independent as-built graphics (ASR Installed and Mead & Borrero 2011 Fig 3 bottom), and 3D should show the as-built state. Against it: the 2013 survey is a measured survey with a labelled scale. Not applied; the default stays the 2013 survey outline until you decide (asked via main as D8).

4. **[ASK] Datum of the ASR "Mount Reef Installed" bathymetry image (legend -1.8 to -7.4 m).**
   It is read as MVD-53 here; the same reading as CD would move the toe-level ring from -4.46 to -5.4 m CD. A one-line answer from ASR / Raised Water Research settles whether the 2008 seabed was about -4.5 m CD.

5. **[LOOK] Google Earth historical imagery 2008-2010 over -37.6448, 176.2026.**
   If the reef bags are visible (calm, clear day) they confirm the as-built footprint and the north-arm base bags that the 2013 survey no longer shows. Note the imagery date; no download needed.

6. **[LOOK] Navionics phone app: depth at the reef centre and the 2.4 m sounding at about 36 m along the shore and 345 m out.**
   A second reading of the same 2026 SonarChart in the app (with its stated datum) would check the web-viewer reading used for the seabed (-2.76 m CD at the centre).

7. **[LEGAL] Reuse rights of the private research copies before any public release.**
   The BoPRC / Focus RMG report figures, the ASR image, Esri Wayback tiles and Garmin Navionics screenshots are private copies (07_scale/shapes/mount-maunganui-reef/src/ and 3d/src/); none is embedded in the viewer. Only the LINZ aerial (CC BY 4.0) is open-licensed.

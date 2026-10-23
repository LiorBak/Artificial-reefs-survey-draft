# REQUESTS FOR LIOR - Albany 3D model (2026-10-10)
| tool | where (WGS84) | what to read | datum / units | why it matters |
|---|---|---|---|---|
| Navionics app (or Garmin Marine Maps in your own browser; it did not render in headless Chrome) | reef centroid -35.018005, 117.920991; shoreward apex -35.017591, 117.920090; east tip -35.017872, 117.921780; south tip -35.018570, 117.920750 | depth at each (SonarChart and Nautical layers) | note units and the datum if shown | tests the seabed under the reef and the pile height (now LOW confidence) |
| Navionics app | line y = 50, 100, 300, 400 m: (-35.017485, 117.919902), (-35.017711, 117.920375), (-35.018616, 117.922270), (-35.019069, 117.923218) | depth | as above | cross-shore profile; the model has -2.5 m at y = 75, -4 m at 105, -5 m at 126, -8 m at 330 |
| Navionics app | (-35.017388, 117.921876), (-35.017841, 117.922823), (-35.018940, 117.920770) | depth | as above | sand-bar / alongshore variation |
| e-mail to the City of Albany (you send it) | project team | the full Detailed Design Report (Bluecoast P19024, 2020; only the 5-page summary is public), its 2017 bathymetry and the practical-completion (as-built) survey of March 2025 | - | would replace the weakest part of the model (seabed, heights, slopes, volume fit) |
| Google Earth Pro | historical imagery slider at -35.018, 117.9207 | dates of imagery after 2025-01-16 (Esri Wayback has only 2025-01-16 and 2026-01-20) | - | a second finished-reef image, construction progress |

## W8 (2026-10-13): GA / AusSeabed portal, what to click (picture: `W8_how_to.png`)
1. Open https://portal.ga.gov.au/persona/marine (it is only a map; wait until it draws).
2. Switch ON the AusSeabed bathymetry survey coverage layer ("Bathymetry Survey Acquisitions Coverage").
3. Go to the reef centre: lat -35.018005, lon 117.920991 (about 140 m off Middleton Beach; the red point in the picture).
4. Click inside the coloured outlines at that point; copy from each pop-up: survey name, year, instrument, owner, Data Access URL.
5. Look for "Middleton Bay & Oyster Harbour" (WA Department of Transport, multibeam and laser scanner) and send me the text. I could not draw the portal here (GA blocks the cloud session), so layer names come from GA's 2021 holdings file.

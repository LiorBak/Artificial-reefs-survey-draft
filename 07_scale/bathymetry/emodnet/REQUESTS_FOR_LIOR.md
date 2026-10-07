# REQUESTS_FOR_LIOR - EMODnet bathymetry test (2026-10-06)

Nothing waits on these; the integration plan works with stated assumptions. Each item is something my own headless Chrome could not read because the site shows a bot check or a block page (I did not bypass it).

| # | Tool | What to open / read | What to note | Why it matters |
|---|---|---|---|---|
| 1 | normal browser | https://cdi-bathymetry.seadatanet.org/report/edmo/2607/117452 (the survey that supplies the EMODnet cells at the Boscombe reef; EDMO 2607 = OceanWise Limited) | survey title, survey dates, instrument, **vertical datum / reduction (LAT? ODN?)**, originator (UKHO? MCA?), coverage polygon; screenshot | decides whether the 1.8 m offset between EMODnet and our Fig. 9 / Navionics seabed is a datum issue (assumption A3) and gives the real survey year (my inference: 2011-2012) |
| 2 | normal browser | https://cdi-bathymetry.seadatanet.org/report/edmo/2607/115084 (Borth, sparse cells) and https://cdi-bathymetry.seadatanet.org/report/1982230 ("Poole Bay, Blocks 14-17") | same fields | Borth: confirms the survey age (>30 y) and datum of the only surveyed cells; Boscombe: tells whether 117452 is part of the Poole Bay blocks |
| 3 | EMODnet Map Viewer in a normal browser | https://emodnet.ec.europa.eu/geoviewer/ : switch on "Source Reference of the DTM", click on the sea at 50.7175 N, 1.8389 W and at 52.4835 N, 4.0562 W | the popup text (dataset name, link) | the viewer's own popup may carry the survey name that the machine services do not |
| 4 | Channel Coastal Observatory data request (optional) | Poole Bay bathymetry / beach profile near Boscombe pier (UK CHP multibeam 2011-12 if that is the source) | vertical datum, grid resolution, survey date | a finer dataset than EMODnet exists for Boscombe; the DTM cannot show the reef, a 1-5 m grid could |
| 5 | tide table | Aberystwyth (or Borth) chart datum relative to Ordnance Datum and MSL - LAT | metres | needed to convert EMODnet (LAT) to the Borth model's MSL zero; I could not verify it on a primary page |

# REQUESTS_FOR_LIOR - Boscombe Surf Reef 3D model (2026-10-05)

The model is built and usable as it is (confidence medium). The items below are what I could NOT read myself, or only partly. Each one says what I assumed meanwhile, so nothing is waiting on you. Coordinates are decimal degrees, WGS84 (lat, lon); I computed them from the verified outline and the model frame (x alongshore, y offshore, see `METHODS_3D.md` 3.1).

What I did read myself (so you do not need to repeat it): the Garmin Navionics web viewer (Nautical Chart and SonarChart, metres, zoom 18) - the old ChartViewer is gone, but `maps.garmin.com/en-US/marine` shows both layers without login; soundings and shoal areas are in `annotated\navionics_*.png`. The viewer does NOT state a depth datum or a survey date, and it prints no drying height.

## A. Navionics app (phone / tablet), SonarChart or Nautical Chart, depths in metres

| Tool | Exact lat/lon (or place) | What to read | Datum / units to note | Why it matters for the model |
|---|---|---|---|---|
| Navionics app | 50.717704, -1.838728 (centre of the green drying patch) | tap the green patch: drying height or depth at point; repeat at 3 other points inside the green patch (about 5 m apart) | metres; write down any datum line the app shows (chart datum / LAT?) and whether tide correction is ON | the web viewer prints no drying height: this gives the present crest height above chart datum (model crest as built: +0.5 m ACD; survey April 2011 peak +0.68 m) |
| Navionics app | 50.717851, -1.838682 (peak of the April 2011 survey) | depth at point | metres | tests whether the shoal peak of the chart is the same as the survey peak (13 m away from the green patch centre in my reading) |
| Navionics app | 50.718010, -1.838597 (shoreward toe); 50.717505, -1.839447 (west flank toe); 50.717817, -1.838276 (east flank toe); 50.717033, -1.839104 (offshore tail end) | depth at point at each | metres | present toe depth on four sides = reef height above the seabed (model seabed at these toes -2.4 to -4.7 m ACD) |
| Navionics app | 50.71866, -1.839115 (y 100 m); 50.716697, -1.838757 (y 320 m); 50.717462, -1.840039 (80 m west of the reef); 50.717726, -1.837660 (90 m east) | depth at point | metres | tests the seabed extrapolation outside the Fig. 9 survey (model vs Navionics soundings differ by 0.5 m r.m.s. so far) |
| Navionics app | the shoal at 50.7177, -1.8388 | if the app shows an age / date / source for the chart or SonarChart data of this cell (object info, "chart info", update date) write it down | date | I could not find any survey date in the web viewer; it decides whether the shoal is the 2011 survey, a later one, or crowd-sourced |
| Navionics app | settings screen | what the app says about the depth reference of the chart (chart datum or LAT) | text | assumption A9: chart datum; the area match with the survey (1-2 %) supports it but does not prove it |

## B. Google Earth Pro

| Tool | Exact lat/lon (or place) | What to read | Datum / units to note | Why it matters for the model |
|---|---|---|---|---|
| Google Earth Pro, historical imagery slider | 50.7178, -1.8389 (reef), eye altitude about 400 m | list of imagery dates 2009-2012 and later; screenshot (with the date shown) of the EARLIEST image after Sept 2009 and of any image of 2010 in which the dark bag stripes are visible | date as shown (yyyy-mm-dd) | my outline comes from 28 Sep 2011 (after the damage); a 2009-2010 image would give the true as-built outline and the as-built length |
| Google Earth Pro, ruler (path) | pier head 50.718223, -1.842812 to the outline centroid 50.717532, -1.838909 | distance in metres | metres | model value 285 m; checks the scale of my frame with an independent tool |
| Google Earth Pro, ruler (line) | 50.717033, -1.839104 (SW tail end) to 50.718010, -1.838597 (NE shoreward end) | length | metres | model value 114 m (outline long axis 121 m, longest vertex pair 123 m: from 50.717062, -1.839378 to 50.717921, -1.838273) |
| Google Earth Pro, historical imagery | surf line at 50.719552, -1.839278 (model origin) | in any dated image with a clear waterline: the image date and time, and mark the waterline position along the shore normal (bearing 173 deg) | date + time, metres from the origin | with a tide table value for that moment (section C) this gives one point of the beach profile; the model beach (y < 100 m) is extrapolated, not measured |

## C. Other (not Navionics / Google Earth)

| Tool | Place | What to read | Datum / units | Why it matters |
|---|---|---|---|---|
| normal browser (the site shows a bot check I did not bypass) | https://pearl.plymouth.ac.uk/bms-theses/412/ (Rendle, University of Plymouth thesis) | download; find the bag layout figure, the as-built crest levels and the stated vertical datum of the surveys | text and figure numbers | the only source that may give the as-built layout and a datum statement for the Fig. 9 survey (the ICCE paper's datum sentence is garbled) |
| Channel Coastal Observatory data request | Boscombe beach profile and the Oct 2009 reef bathymetry survey | metadata: vertical datum (ODN or chart datum) and the gridded data if they release it | datum name | would replace the colour read of Fig. 9 and fix the datum (A3) |
| UKHO EasyTide or a tide table | Bournemouth, for the date and time of any photo you want to align | predicted height and the shape of the double high water | m above chart datum | sets the water-level slider; the model uses static levels only |

## D. Added 2026-10-07 (seabed extension run)

D1. EMODnet CDI record 117452 (EDMO 2607, OceanWise Limited; the survey that supplies the DTM 2024 cells at the reef): open it in a normal browser (SeaDataNet CDI catalogue, https://cdi.seadatanet.org/ , search "117452") and read the vertical reference and the survey date. It would give a third, independent check of the datum assumption A3 (the CCO test already gives +0.03 m against -1.37 m).
D2. Channel Coastal Observatory (https://coastalmonitoring.org/ , contact form): ask whether nearshore or offshore bathymetry (single- or multibeam) of Poole Bay at Boscombe exists for 2009-2012, covering y about 40-100 m and y 312-650 m of the model frame. It would replace the spline blend (zone 4, +-0.5 m) and the EMODnet slope extension (zone 5, +-1.2 m).
D3. If you want a different beach date in the model (for example autumn 2009), tell us: the CCO lines 5f00427 and 5f00424 have 2009-09-22 and 2009-11-30, the other nine start on 2010-04-20.

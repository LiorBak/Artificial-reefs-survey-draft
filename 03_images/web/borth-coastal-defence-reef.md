# Web image candidates — Borth coastal defence reef

6 candidates found and verified (HTTP 200, image/* content-type) via `curl -sI -A "Mozilla/5.0"`, except the map entry (a live Google Maps link, not a static image file). None downloaded into the project folder — index only, per instructions.

1. **"A bigger splash: Borth sea defences"** — Chris Denny, 2011-04-19. Wikimedia Commons mirror of a Geograph photo. CC BY-SA 2.0. Wave breaking over the newly-built reef/rock structure.
   https://upload.wikimedia.org/wikipedia/commons/0/06/A_bigger_splash%2C_Borth_sea_defences_-_geograph.org.uk_-_2366565.jpg

2. **"Coastal protection works at Borth"** — Phil Champion, 2011-07-10, Geograph. CC BY-SA 2.0. Construction in progress, beach partly closed.
   https://s0.geograph.org.uk/geophotos/02/55/47/2554717_ca5fc76b.jpg

3. **"Building the reef: Borth sea defences"** — Chris Denny, 2011-08-03, Geograph (same photo cited as R9 in the dossier). CC BY-SA 2.0. Diggers building the offshore reef via the temporary rock causeway.
   https://s0.geograph.org.uk/geophotos/02/57/55/2575564_e576dfb2.jpg

4–5. **Borth Community website, official BAM Nuttall construction progress photos**, 2011-08-18, captioned "Pictures of the construction of the northern & southern multi-purpose reef." License not stated (council/community site, contractor-supplied images) — link-only, do not reproduce without checking.
   https://borthcommunity.info/images/stories/BamNuttall/20110818-100400.jpg
   https://borthcommunity.info/images/stories/BamNuttall/20110818-101454.jpg
   (source page: https://borthcommunity.info/index.php/progress-pictures/326-coastal-defence-progress-pictures-august-2011)

6. **Map** — Google Maps satellite view centred on the Craig y Delyn cliffs (52.4690°N, 4.0681°W), the southern-end location where the reef sits ~300–400 m offshore.
   https://www.google.com/maps?q=52.4690,-4.0681&z=17&t=k

## Rejected / not used
- Two further Wikimedia Commons mirrors of Geograph "Borth sea defences" photos ("Beacon's end..." and "A quiet afternoon on the beach...", both Chris Denny, CC BY-SA 2.0, April 2011) were located and are almost certainly valid, but could not be re-verified with curl this session — Wikimedia's upload.wikimedia.org host started returning HTTP 429 ("Too many requests") to this session's IP partway through verification and did not clear within the session. Not included in the JSON above because the direct-serve check could not be completed, per the "check it serves an image" instruction. A later agent could re-check:
  - https://upload.wikimedia.org/wikipedia/commons/c/cb/Beacon%27s_end%2C_Borth_sea_defences_-_geograph.org.uk_-_2368938.jpg
  - https://upload.wikimedia.org/wikipedia/commons/d/d2/A_quiet_afternoon_on_the_beach%2C_Borth_sea_defences_-_geograph.org.uk_-_2368953.jpg
- Coflein's site record (https://coflein.gov.uk/en/site/424699) references an "Images" sub-page but no direct image URL could be confirmed this session.
- New Civil Engineer's "Borth's Big Dig" article (R1 in the dossier) likely carries construction photos but is subscriber-gated.

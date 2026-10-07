"""Write 07_scale/bathymetry/gold_coast/SOURCES.md from registered_images.json (images) + the documents table below."""
import json, os

WORK = r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\bathymetry\gold_coast"
imgs = json.load(open(WORK + r"\tools\registered_images.json", encoding="utf8"))

DOCS = [
    ("GC-D01", "Gold Coast DTM - dataset page and JSON-LD (City of Gold Coast, data.gov.au)",
     "https://data.gov.au/data/dataset/digital-elevation-models-dem ; https://data.gov.au/data/dataset/3f1698d1-3789-4dc5-af9d-0fb08f800d77.jsonld",
     "dataset description, resources list", "created 2020-10-12, modified 2024-05-13", "City of Gold Coast", "CC BY 2.5 AU", "2026-10-06",
     "States 'Digital Terrain Model of the Gold Coast LGA, including bathymetry in certain areas', DEM accuracy 'at least 15 cm', and the byte sizes: DTM zip 4,141,282,150 B (NOT downloaded), DTM Metadata zip 6,257,930 B."),
    ("GC-D02", "DTM Metadata file geodatabase (dtm_metadata.zip, 6.26 MB; read from %TEMP%, not kept in the project except evidence extracts)",
     "https://data.gov.au/data/dataset/3f1698d1-3789-4dc5-af9d-0fb08f800d77/resource/3c077953-539c-422a-b3ed-64e06978204c/download/dtm_metadata.zip",
     "tables a000001d7 (VAT, 104 rows), a000001d5 (raster blocks), GDB_Items (raster definition + lineage XML)", "raster DTM_Metadata_Feb_2024_1m, last edit 2024-02-27", "City of Gold Coast", "CC BY 2.5 AU", "2026-10-06",
     "1 m source-ID raster of the DTM: origin (515775, 6938225), GDA94 MGA56 + VERTCS AHD (EPSG 5711); 104 survey sources (Lidar 2022, Lidar 2015, Bathymetric Lidar 2014 = Broadwater, estuary/canal cross-sections ...); 65-step lineage; no ocean source. Evidence copies in q1_dtm_evidence/."),
    ("GC-D03", "City of Gold Coast Contours MapServer (50/10/5/1 m contour layers)",
     "https://maps1.goldcoast.qld.gov.au/arcgis/rest/services/Contours/MapServer (layers 1, 2, 7, 8)", "queries only (statistics and counts)", "service live 2026-10-06", "City of Gold Coast", "not stated",
     "2026-10-06", "ELEVATION minimum 0 m in the windows around both reefs; all 226 negative contours (1 m layer) lie at x <= 542,156 (inland waterways); none east of x = 543,500 to the layer's limit x = 556,000."),
    ("GC-D04", "City of Gold Coast open data hub (ArcGIS Hub) catalogue search",
     "https://data-goldcoast.opendata.arcgis.com/api/search/v1/collections/dataset/items?q=...", "searches: bathymetry, beach, hydrographic, nearshore, reef, contour, digital terrain, DEM", "2026-10-06", "City of Gold Coast", "CC BY (hub default)",
     "2026-10-06", "No bathymetry / hydrographic / DEM layer; only the Artificial Reef feature layer (already used) and the Contours / Hillshade services."),
    ("GC-D05", "Maritime Safety Queensland (2014) Standard port datum levels - height above LAT",
     "https://www.msq.qld.gov.au/-/media/TMROnline/msqinternet/MSQFiles/Home/Tides/standardportdatumlevels2014.pdf", "1 page, table", "2014", "Maritime Safety Queensland", "not stated (Queensland Government publication)",
     "2026-10-06", "Gold Coast Seaway: benchmark PM QGS564 6.688 m above LAT; AHD above LAT = 0.760 m (applies at the standard port benchmark only)."),
    ("GC-D06", "Maritime Safety Queensland (2026) Semidiurnal tidal planes 2026 (existing copy in the Palm Beach folder)",
     "https://www.msq.qld.gov.au/_/media/tmronline/msqinternet/msqfiles/home/tides/tidal-planes/2026-semidiurnal-tidal-planes.pdf", "Gold Coast Seaway row", "epoch 2010-2029", "Maritime Safety Queensland", "not stated (Queensland Government publication)",
     "2026-10-06", "Gold Coast Seaway above LAT: MHWS 1.53, MHWN 1.24, MLWN 0.51, MLWS 0.22, MSL 0.88, HAT 2.03; permanent mark PSM 702548 6.688; Snapper Rocks and Tweed rows."),
    ("GC-D07", "Sultmann, S. (2025) State-wide Nearshore Bathymetry Survey for Improved Coastal Hazard Assessment (slides, QCoast2100 forum)",
     "https://www.qcoast2100.com.au/files/assets/qcoast2100/v/1/events/forum-9-documents/2._qcoast_forum_2025_detsi_sel_sultmann_final.pdf", "slides 2-19 (read from the WebFetch-cached copy; direct download 403)", "2025", "Qld Department of Environment, Tourism, Science and Innovation", "not stated",
     "2026-10-06", "Bathymetry relative to AHD; 3351 km2 1 m DEM from 200 m onshore to up to 6 km offshore; Gold Coast in stage one, survey from mid-July 2025; processed DEMs and .las free to councils; 'No decision on public availability'; current Qld data up to 40 years old (BPA ETA surveys)."),
    ("GC-D08", "Queensland Government (2013, reviewed 2024) Seabed mapping; and Coastal and Estuarine Risk Mitigation Program",
     "https://www.qld.gov.au/environment/coasts-waterways/beach/studies/studies-seabed ; https://www.qld.gov.au/environment/coasts-waterways/plans/adaptation-programs/cermp", "web pages", "2013 / 2024", "Queensland Government", "CC BY 4.0 (qld.gov.au default)",
     "2026-10-06", "Only the Sunshine Coast 2011-12 pilot bathymetric LiDAR is published (Open Data portal); the state-wide survey ($4.3 M, airborne sensors up to 2 km offshore) is under way."),
    ("GC-D09", "Jackson, A., Tomlinson, R., Corbett, B. and Strauss, D. (2012) ICCE 33, structures.54 (full PDF)",
     "https://icce-ojs-tamu.tdl.org/icce/article/download/6956/pdf", "13 pp", "2012", "ICCE / authors", "CC BY 4.0 badge on the site (no per-article statement)", "2026-10-06",
     "Narrowneck monitoring: design levels (Fig 2), maintenance (Fig 4), 9 June 2011 survey (Fig 5), 2004/2011 aerials (Figs 6-7); crest 'about 1-1.5 m below low tide'. Copy: shapes/narrowneck-gold-coast/src/gov/."),
    ("GC-D10", "Jackson, L.A. et al. (2007) Narrowneck Reef: review of seven years of monitoring. Shore & Beach 75(4)",
     "http://hdl.handle.net/10072/17995 (bitstream 7e18bf60-76d6-5bdf-961d-6b572b099c70)", "14 pp", "Fall 2007", "ASBPA / Griffith Research Online", "(c) The Author(s) 2007; reproduced per the publisher's policy", "2026-10-06",
     "Crest history: UW recommended -1.0 m AHD; adopted RL -1.5 m AHD (-0.5 m LAT); 2001 top-up -1.0 m LAT; target lowered to -1.5 m LAT (RL -2.5 m AHD); AHD ~ mean sea level; 408 containers 20 m long, 3-4.5 m diameter."),
    ("GC-D11", "Vieira da Silva, G. et al. (2021) Sediment pathways and morphodynamic response to a multi-purpose artificial reef - new insights. Coastal Engineering (accepted manuscript)",
     "http://hdl.handle.net/10072/409362 (bitstream 4627106e-ce70-46d1-aec3-c81b126fdd2c)", "37 pp", "2021", "Elsevier / Griffith Research Online", "CC BY-NC-ND 4.0", "2026-10-06",
     "Narrowneck: reef between the -2 m AHD contour and -10.4 m AHD; crest initially -0.67 m AHD (Black and Mead 2001), adopted -1.5, lowered to -2.5 m AHD, multibeam after the 2018 top-up -2.2 m AHD; Table 1 chronology (2017 design studies of 2 renewal options; renewal Sep 2017 - Jun 2018); ETA 63-70 topo-bathymetric surveys 2018-2020 (City single-beam + RTK-GPS, 2 x 2 m grid, AHD)."),
    ("GC-D12", "Mortensen, S.B. et al. (2015) Concept design of a multipurpose submerged control structure for Palm Beach (DHI)",
     "https://www.dhigroup.com/upload/publications/coastsea/Mortensen_2015.pdf", "7 pp", "2015", "DHI / City of Gold Coast", "not stated", "2026-10-06",
     "Concept crest -1.5 m AHD; offshore toe 560 m offshore in 11.4 m; Table 2 (SCS B: offshore depth 11.4 m, nearshore depth 6.6 m, 53,319 m3); Fig 6 seabed contours."),
    ("GC-D13", "Prenzler, P. et al. (2022) Monitoring of the Palm Beach artificial reef (ICCE abstract 12921)",
     "https://icce-ojs-tamu.tdl.org/icce/article/download/12921/12194", "2 pp", "2022", "ICCE / authors", "CC BY 4.0", "2026-10-06", "'The crest of the reef is 1.5m below mean sea level and consists of 6 to 8 tonne rocks'; hydrographic survey and inspections: stable."),
    ("GC-D14", "Hunt, S. et al. (2022) Palm Beach Shoreline Project: innovative coastal management solution (ICCE; docx)",
     "https://icce-ojs-tamu.tdl.org/icce/article/download/13024/12297", "Figs 1-5", "2022", "ICCE / authors", "CC BY 4.0", "2026-10-06", "Construction May-Sept 2019 by backhoe dredger; 'detailed survey captured throughout construction' for certification (Fig 4, qualitative)."),
    ("GC-D15", "Daniels, R., Metters, D. and Ryan, J. (2022) Wave transformation over Palm Beach reef (ICCE)",
     "https://icce-ojs-tamu.tdl.org/icce/article/download/12702/11975", "Table 1, Figs 1-2", "2022 (buoys 2016)", "ICCE / Qld DES", "CC BY 4.0", "2026-10-06",
     "Natural reef: seaward edge 10-16 m, shore edge 5-9 m, 500 m off the beach, 850 m x 600 m; buoy depths PBO1 11.33, PBO2 11.29, PBO3 11.75, PBO4 23.80 m (datum not stated)."),
    ("GC-D16", "City of Gold Coast (2020) Palm Beach Shoreline Project - project overview brochure",
     "https://www.goldcoast.qld.gov.au/files/sharedassets/public/v/1/pdfs/environment/palm-beach-shoreline-project-brochure-a4.pdf", "16 pp (pp. 8-9 reef design)", "June 2020", "City of Gold Coast", "not stated", "2026-10-06",
     "'160 metres long, 80 metres wide and 1.5 metres below the average water level at its highest point', ~270 m from Nineteenth Avenue; section view (not to scale); scales of physical models 1:42.5 (QGHL) and 1:59 (WRL); City hydrographic and beach survey data since the 1960s."),
    ("GC-D17", "City of Gold Coast - Seawalls and artificial reefs (web page)",
     "https://www.goldcoast.qld.gov.au/Environment-sustainability/Protecting-our-environment/Managing-our-beaches/Seawalls-artificial-reefs", "web page", "2026", "City of Gold Coast", "not stated", "2026-10-06",
     "Palm Beach reef built 2019 with 60,000 t rock, 270 m off Nineteenth Avenue; Narrowneck built 1999 of geotextile sandbags, renewed 2018."),
    ("GC-D18", "International Coastal Management (2023) Artificial reefs and nearshore nourishment on the Gold Coast: what the monitoring shows",
     "https://www.coastalmanagement.com.au/artificial-reefs-and-nearshore-nourishment-on-the-gold-coast-real-world-results", "web article", "2023-09-18", "ICM", "not stated", "2026-10-06", "Narrowneck and Palm Beach reef images (registered); 20-year scientific review; 75% of nourished sand retained at Palm Beach after five years."),
    ("GC-D19", "Nettle, S. (2017) Narrowneck artificial reef nears completion (updated). Swellnet, 7 Nov 2017",
     "https://www.swellnet.com/news/swellnet-dispatch/2017/11/07/narrowneck-artificial-reef-nears-completion-updated", "web article", "2017-11-07", "Swellnet", "not stated", "2026-10-06",
     "City spokesperson: containers placed on top of the existing footprint to raise the crest; data from physical modelling informed the decision to alter the shape; pre-renewal low-tide depths over the reef 2.5-2.6 m (boat skipper)."),
    ("GC-D20", "Nettle, S. (2019) Narrowneck renewal deemed a success. Swellnet, 19 Aug 2019",
     "https://www.swellnet.com/news/swellnet-analysis/2019/08/19/narrowneck-renewal-deemed-success", "web article", "2019-08-19", "Swellnet", "not stated", "2026-10-06", "City: survey data after the renewal show no settlement; 'significant increase in the frequency of wave breaking on the reef'."),
    ("GC-D21", "Raised Water Research (2019) Narrowneck", "https://raisedwaterresearch.com/spot/artificial-reef/australia/queensland/narrowneck/", "web page", "2019", "Raised Water Research", "not stated", "2026-10-06",
     "Secondary summary: split-V shape, 84 containers added 2017-18, crest 'back to its original designed depth of 1.5 m below low tide' (conflicts with the primary papers, which give -2.5 m AHD = -1.5 m LAT as the lowered design crest)."),
    ("GC-D22", "Alvarez, F., De Lucia, L., Vieira da Silva, G. and Javernig, B. (2023) A coastal erosion risk assessment framework. Australasian Coasts & Ports 2023",
     "http://hdl.handle.net/10072/429692 (Griffith Research Online)", "section 2.3.1", "2023", "Griffith / City of Gold Coast", "copyright; personal use", "2026-10-06",
     "City Hydrographic Survey Program: Whole of Coast survey = 80 transects (ETA lines) about 400 m apart, Rainbow Bay to The Spit, 2-4 surveys per year; ETA geometry defined 1965 (Delft Hydraulics Laboratory)."),
    ("GC-D23", "Vieira da Silva, G. et al. (2021) Building coastal resilience via sand backpassing. Ocean & Coastal Management (accepted manuscript)",
     "http://hdl.handle.net/10072/408348", "text", "2021", "Elsevier / Griffith", "CC BY-NC-ND 4.0", "2026-10-06", "ETA 63 = Surfers Paradise, ETA 67 = Narrowneck, ETA 70 = Southport; profiles referenced to +2 m AHD."),
    ("GC-D25", "City of Gold Coast (2020) Narrowneck Reef Renewal - project page (archived 2020-08-04; saved HTML in shapes/narrowneck-gold-coast/src/gov/)",
     "http://web.archive.org/web/20200804025419/https://www.goldcoast.qld.gov.au/narrowneck-reef-renewal-39934.html", "web page", "2018-2020", "City of Gold Coast", "not stated", "2026-10-06",
     "Primary council statement: in 2018 the City placed 84 additional mega geotextile sandbags around the existing structure over 10 months; 'The locations of the new containers were influenced by physical modelling undertaken at the Queensland Government Hydraulics Laboratory, with some minor changes made to the shape of the renewed reef'; two yellow buoys mark a Prohibited Anchorage Area."),
    ("GC-D26", "Nettle, S. (2019) Palm Beach Artificial Reef is currently under construction. Swellnet, 23 May 2019",
     "https://www.swellnet.com/news/swellnet-dispatch/2019/05/23/palm-beach-artificial-reef-currently-under-construction", "web article", "2019-05-23", "Swellnet", "not stated", "2026-10-06",
     "160 x 80 m, 270 m from the shoreline, 1.5 m deep at the shallowest part at average tidal level; profile image supplied by the City."),
    ("GC-D27", "Queensland Government (n.d.) Hydrographic Charts 1802-2013 (Open Data Portal)", "https://www.data.qld.gov.au/dataset/hydrographic-charts-1802-2013", "dataset page (HTTP 202 challenge to scripts; known only from search snippets)", "charts current to 2010", "Queensland Government (MSQ)", "CC BY 4.0 (per search snippet)", "2026-10-06",
     "Lead only: scanned historic charts including Gold Coast beaches (D-series 1987-1999); not downloaded, not read."),
    ("GC-D24", "Corbett, B.B., Mulcahy, M.G., Elliott-Perkins, Z. and Hunt, S. (2023) Narrowneck Artificial Reef Renewal. Australasian Coasts & Ports 2023, Sunshine Coast, 15-18 Aug 2023",
     "https://www.researchgate.net/publication/373684358_Narrowneck_Artificial_Reef_Renewal (HTTP 403); proceedings https://search.informit.org/doi/book/10.3316/informit.9781925627800 (Cloudflare challenge)", "abstract only via search-engine snippets", "2023", "authors / Engineers Australia", "not stated", "2026-10-06",
     "NOT OBTAINED. Snippets: 84 containers added; 'two design options - the previous design shape and an amended shape'; Renewal Option 2 further seaward with slight realignment; Option 1 = modified 2004 design with crest -2.5 m AHD (-1.5 m LAT). Needs Lior's manual download."),
]

lines = ["# SOURCES - Gold Coast nearshore bathymetry and government / council / university report search (run 2026-10-06)", "",
         "Provenance rows for every image saved (GC-N.. = Narrowneck, GC-P.. = Palm Beach, GC-Q1.. = Q1 evidence overlays) and for every document or service consulted (GC-D..). "
         "All image copies are PRIVATE RESEARCH COPIES; reuse rights must be checked before any public release. Registry ids refer to 03_images/reefs/<slug>/images.json.", "",
         "## A. Images", "",
         "| id | registry id | title | URL (image/PDF) | page / figure | date of the image | credit | licence | retrieved | what it shows | local file |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
for e in imgs:
    def c(s): return str(s).replace("|", "/").replace("\n", " ")
    lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | 2026-10-06 | %s | `%s` |" % (e["gc"], e.get("rid", ""), c(e["title"]), c(e["url"]), c(e["pf"]), c(e["date"]), c(e["credit"]), c(e["lic"]), c(e["shows"]), c(os.path.relpath(e["file"], r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git").replace("\\", "/"))))
lines += ["", "## B. Documents, data services and pages consulted", "",
          "| id | title | URL | page / table | date | credit | licence | retrieved | what it gave |", "|---|---|---|---|---|---|---|---|---|"]
for d in DOCS:
    lines.append("| " + " | ".join(str(x).replace("|", "/") for x in d) + " |")
lines += ["", "## C. Blocked, not bypassed", "",
          "- ResearchGate (HTTP 403), ScienceDirect (Cloudflare error 1000), academia.edu and ADS (human-verification page), MDPI (Akamai 403), informit.org (Cloudflare challenge), theinertia.com (403), qcoast2100.com.au (403 to scripts; the copy cached by the WebFetch tool was used).",
          "- Not downloaded on instruction: the 4.1 GB Gold Coast DTM (data.gov.au resource c86062f0-03d7-4030-9a5e-d47b2062315b)."]
open(WORK + r"\SOURCES.md", "w", encoding="utf8").write("\n".join(lines) + "\n")
print("SOURCES.md written:", len(imgs), "image rows,", len(DOCS), "document rows")

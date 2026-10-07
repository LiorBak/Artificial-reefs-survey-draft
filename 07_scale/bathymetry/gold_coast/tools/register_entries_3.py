"""Entries 3: City of Gold Coast 'Narrowneck Reef Renewal' page (archived 2020-08-04), thumbnails only (full-size images are not in the Wayback archive)."""
import os
from register_entries import add, f3d, RI
S = "narrowneck-gold-coast"
CG = dict(
    cit="City of Gold Coast (2020). Narrowneck Reef Renewal (project page; archived copy of 2020-08-04), image %s. Original https://www.goldcoast.qld.gov.au/narrowneck-reef-renewal-39934.html ; archive http://web.archive.org/web/20200804025419/https://www.goldcoast.qld.gov.au/narrowneck-reef-renewal-39934.html. Accessed 2026-10-06.",
    page="http://web.archive.org/web/20200804025419/https://www.goldcoast.qld.gov.au/narrowneck-reef-renewal-39934.html",
    credit="City of Gold Coast; photo/video courtesy International Coastal Management (ICM) where captioned",
    lic="not stated (City of Gold Coast web content)")
_base = "http://web.archive.org/web/20200804025419im_/https://www.goldcoast.qld.gov.au/_images/"
ROWS = [
    ("narrowneck-gold-coast_cogc_renewal_page_faucon_over_reef_drone_thumb_2018.jpg", "faucon-at-NRR-drone-photo-thu.jpg", "aerial",
     "City of Gold Coast Narrowneck Reef Renewal page: split-hull dredger FAUCON over the reef, drone view (200 px thumbnail)",
     "Faucon at Narrowneck Reef Renewal aerial - courtesy ICM; thumbnail of /_images/faucon-at-NRR-drone-photo.jpg", "2017-2018 (renewal works)",
     "Vertical drone view of the red split-hull dredger Faucon above the reef; the dark container arms and a wing are visible beneath and beside it in turquoise water. Only the 200 x 127 px thumbnail is archived.",
     True, "renewal works in progress (2017-18)", ["context", "plan_trace"],
     "Too small to trace; shows that the arms/wing outlines are visible from the air during the works. The full-size image is not archived: ask the City/ICM if needed.", "GC-N31",
     f3d(False, "None (thumbnail only)", [])),
    ("narrowneck-gold-coast_cogc_renewal_page_prohibited_anchorage_yellow_buoy_thumb_2018.jpg", "narrowneck-reef-renewal-buoys-th.jpg", "photo",
     "City of Gold Coast Narrowneck Reef Renewal page: yellow navigation buoy marking the Prohibited Anchorage Area (200 px thumbnail)",
     "Navigation buoys mark the extents of a Prohibited Anchorage Area at Narrowneck artificial reef (thumbnail)", "2018",
     "Yellow navigation buoy with the Surfers Paradise skyline behind; two such buoys mark the extents of the Prohibited Anchorage Area over the reef.",
     False, "as renewed (post-2018)", ["context"],
     "Context only: buoy positions mark the reef extent (positions not given). Evidence that the post-2018 reef carries two yellow buoys (check Esri/Google imagery for them).", "GC-N32",
     f3d(False, "None", [])),
    ("narrowneck-gold-coast_cogc_renewal_page_faucon_split_hull_dredger_thumb_2018.jpg", "narrowneck-reef-renewal-faucon-th.jpg", "photo",
     "City of Gold Coast Narrowneck Reef Renewal page: split-hull dredger FAUCON at the reef site with Narrowneck beach behind (thumbnail)",
     "The split hull dredger named 'FAUCON' at the reef site with Narrowneck beach in the background (thumbnail)", "2017-2018",
     "Side view of the red split-hull dredger Faucon on site, the beach and training works in the background.", False, "renewal works (2017-18)", ["context"],
     "Context: method (container placed from a split-hull barge); no geometry.", "GC-N33", f3d(False, "None", [])),
    ("narrowneck-gold-coast_cogc_renewal_page_faucon_placing_container_over_reef_thumb_2018.jpg", "narrowneck-reef-renewal-geotextile-sand-container-th.jpg", "aerial",
     "City of Gold Coast Narrowneck Reef Renewal page: FAUCON placing a geotextile sand container on the reef (thumbnail)",
     "FAUCON placing a Geotextile Sand Container to renew the Narrowneck artificial reef (thumbnail)", "2017-2018",
     "Vertical drone view of the dredger with a sand-filled container in its hull above the reef arms; the existing container patches show below.", True, "renewal works (2017-18)", ["context", "plan_trace"],
     "Shows how containers are placed on the existing footprint (container length against the hull gives a scale of about 20 m); too small for tracing.", "GC-N34",
     f3d(False, "None (thumbnail only)", [])),
    ("narrowneck-gold-coast_cogc_renewal_page_qghl_physical_model_renewal_options_thumb_2018.jpg", "narrowneck-reef-renewal-physical-modelling-th.jpg", "photo",
     "City of Gold Coast Narrowneck Reef Renewal page: physical modelling of the renewal design options at the Queensland Government Hydraulics Laboratory (thumbnail)",
     "Physical modelling of renewal design options at the Queensland Government Hydraulics Laboratory (thumbnail)", "2017 (design studies of two renewal options)",
     "Close-up of the QGHL wave-basin model of the reef: sand-coloured bed with a wave probe frame and rigging; not enough resolution to see the reef plan.", False, "design options model (2017)", ["context"],
     "Evidence that the two renewal options (previous vs amended shape) were tested in a QGHL basin model in 2017; the page text says the new container locations were influenced by it, 'with some minor changes made to the shape of the renewed reef'. Goes to REPORT.md section 6.", "GC-N35",
     f3d(True, "Which renewal option was built (previous vs amended shape): ask QGHL/City for the model plan or read the Corbett et al. (2023) figure of Options 1 and 2", ["planform"])),
]
for _f, _o, _k, _t, _pf, _dt, _sh, _vis, _st, _us, _how, _gc, _ff in ROWS:
    add(S, os.path.join(RI, "narrowneck-gold-coast", _f), kind=_k, title=_t, cit=CG["cit"] % _pf, url=_base + _o, page=CG["page"], pf=_pf, date=_dt,
        credit=CG["credit"], lic=CG["lic"], shows=_sh, vis=_vis, state=_st, used=_us, how=_how, ann=[], gc=_gc, f3d=_ff)

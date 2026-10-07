"""Register the EMODnet screenshots and profile plots in 03_images/reefs/<slug>/images.json + IMAGES.md and append to NEW_IMAGES_LOG.md
(rule: _agent_briefs/image_registry.md). Append-only; re-reads each file right before writing; skips rows whose file is already registered."""
import hashlib, json, os, re
from PIL import Image

ROOT = r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git"
OUT = "07_scale/bathymetry/emodnet"
REG = f"{ROOT}/03_images/reefs"
TODAY = "2026-10-06"
ADDED = "EMODnet bathymetry test, 2026-10-06"
DOI = "https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1"
CITE_VIEWER = (f"EMODnet Bathymetry Consortium (2024). EMODnet Digital Bathymetry (DTM 2024) [Mean depth / Source references layers], displayed in the EMODnet Map Viewer, "
               f"https://emodnet.ec.europa.eu/geoviewer/ (layer ids 14159 / 13012), DOI {DOI}. Accessed {TODAY}. Licence CC BY 4.0 (EMODnet Terms of Use). "
               "Basemap: Esri World Imagery (Esri, Maxar, Earthstar Geographics). Annotations (cell grid, outline, points, profile, scale bar) added by this project.")
CITE_PLOT = (f"This project ({TODAY}), plot made from EMODnet Bathymetry Consortium (2024). EMODnet Digital Bathymetry (DTM 2024), ERDDAP dataset bathymetry_dtm_2024 "
             f"(https://erddap.emodnet.eu/erddap/griddap/bathymetry_dtm_2024), REST https://rest.emodnet-bathymetry.eu/depth_profile, DOI {DOI}. Accessed {TODAY}. Licence CC BY 4.0.")
LICENCE = ("EMODnet data: CC BY 4.0 (https://emodnet.ec.europa.eu/en/terms-use-emodnet-online-services-data-and-data-products, accessed 2026-10-06); "
           "'not for navigation' (Sextant record). Esri World Imagery basemap: Esri terms, reuse not cleared. Annotations/plots: project products.")
LICENCE_PLOT = "EMODnet data: CC BY 4.0 (EMODnet Terms of Use, accessed 2026-10-06); plot is a project product; model curves from the project's own model.js (read only)."

BOS_CHECK = ("EMODnet DTM 2024 cell means (m rel. LAT; model z_LAT = z_MSL + 1.46) are 1.1-3.1 m deeper than the model seabed in the 7 cells fully inside the model grid (mean -1.80 m, sd 0.66; "
             "reef cell ki34288/kj32794: EMODnet -5.62 vs model seabed -4.23, as-built -3.10) and show no reef (cell max -4.87 vs crest +0.56). Decide whether to adopt the far-field slope "
             "(-1.4 %, y > 380 m) and re-check the survey-datum assumption A3 once CDI 117452 metadata is read (REQUESTS_FOR_LIOR.md in 07_scale/bathymetry/emodnet).")
BORTH_CHECK = ("EMODnet DTM 2024 at the Borth reef: the reef cells are GEBCO 2024 interpolation (-0.34..-0.13 m rel. LAT, flag 1), the real source cells (CDI 115084, age > 30 y, 1 sounding/cell) "
               "start at y = 335 m from the defence line and give a seaward gradient of about -1.1 % (-0.40 m at 367 m to -3.36 m at 652 m). 3D agent: use only as offshore trend / weak 'reef near LAT' check; "
               "verify MSL-LAT at Borth to convert to the model's MSL zero.")

ROWS = {
 "boscombe-surf-reef": [
  dict(file="viewer/boscombe-surf-reef_viewer_dtm_raw.png", annotated=["viewer/boscombe-surf-reef_viewer_dtm_annotated.png"], kind="chart_screenshot",
       title="EMODnet Map Viewer at Boscombe: DTM 2024 mean depth over Esri imagery, with DTM cell grid, reef outline, points and shore-normal profile",
       cite=CITE_VIEWER, url="https://emodnet.ec.europa.eu/geoviewer/", page="layer 14159 'Mean depth natural colour (with land)', centre 50.7175 N 1.8389 W, 1200 x 720 m, 50 % opacity",
       date="DTM 2024 (published 2024-12-31); screenshot 2026-10-06; Esri basemap date not stated by the viewer", credit="EMODnet Bathymetry Consortium (data); Esri, Maxar, Earthstar Geographics (basemap); annotations by this project", lic=LICENCE,
       shows="The 1/16 arc-minute EMODnet DTM cells (116 x 73 m) with their depth in m below LAT (-4.0 to -9.1 over the reef area) around the Boscombe reef; the reef outline (yellow) is smaller than one cell and the DTM shows no shoal there.",
       vis=True, state="damaged / remains (current Esri imagery, faint blurred patch at the reef; date not stated)", used=["cross_check", "3d_seabed", "3d_tides"],
       how="Read the EMODnet cell mean at the reef centre (-5.62 m rel. LAT = -7.08 m MSL with z_LAT = z_MSL + 1.46) and at the toe / seabed points of 3d\\REQUESTS_FOR_LIOR.md (-3.99 .. -5.62 m); compared with the model in 07_scale/bathymetry/emodnet/REPORT.md (EMODnet is 1.1-3.1 m deeper than the model seabed, no reef visible). Not used for model values; integration plan = far-field seabed slope only.",
       linked=[f"{OUT}/REPORT.md", f"{OUT}/METHOD.md", f"{OUT}/data/boscombe-surf-reef_points_emodnet.csv", "07_scale/shapes/boscombe-surf-reef/3d/METHODS_3D.md (S5 datum check)"], check=BOS_CHECK, affected=["seabed", "tides"]),
  dict(file="viewer/boscombe-surf-reef_viewer_sources_raw.png", annotated=["viewer/boscombe-surf-reef_viewer_sources_annotated.png"], kind="chart_screenshot",
       title="EMODnet Map Viewer at Boscombe: 'Source references' layer (survey patch of the DTM) over Esri imagery with cell grid, outline and profile",
       cite=CITE_VIEWER, url="https://emodnet.ec.europa.eu/geoviewer/", page="layer 13012 'Source Reference of the DTM' (V2024), same view as the mean-depth screenshot, 55 % opacity",
       date="V2024 source references (record revised 2025-03-01); screenshot 2026-10-06", credit="EMODnet Bathymetry Consortium (data); Esri, Maxar, Earthstar Geographics (basemap); annotations by this project", lic=LICENCE,
       shows="The coloured patch that supplies the DTM cells at the reef: one survey patch (CDI 117452, EDMO 2607 OceanWise Limited) supplies the DTM cells over the whole sea area shown, beginning about 100 m offshore of the surf line.",
       vis=True, state="damaged / remains (current Esri imagery; date not stated)", used=["cross_check", "3d_seabed"],
       how="Used to identify the source survey of the DTM cells at the reef (CDI 117452, EDMO 2607 = OceanWise Limited, 2024 patch; WFS emodnet:source_references, REST reference). Quality index of that patch: horizontal 3, vertical 4, age 1 (10-30 y), purpose 3 (EMODnet QI record). Documented in REPORT.md; no model value taken.",
       linked=[f"{OUT}/REPORT.md", f"{OUT}/data/boscombe-surf-reef_results.json"], check=BOS_CHECK, affected=["seabed"]),
  dict(file="figures/boscombe-surf-reef_profile_emodnet_vs_model.png", annotated=[], kind="diagram",
       title="Shore-normal depth profile through the Boscombe reef: EMODnet DTM 2024 cells vs the project model (seabed, as-built reef, April 2011 survey surface)",
       cite=CITE_PLOT, url="https://rest.emodnet-bathymetry.eu/depth_profile", page="plot made with scripts/make_plots.py; line x = 0.1 m, y = 0-500 m, bearing 173.4 deg",
       date="plot 2026-10-06; EMODnet DTM 2024; model state AS-BUILT 2009 + April 2011 survey surface", credit="Plot by this project; EMODnet Bathymetry Consortium (data); Fig. 9 survey: Rendle & Davidson (2012) via the project model", lic=LICENCE_PLOT,
       shows="EMODnet cell means with min-max bars and the REST profile as steps (-4.0, -5.6, -7.1, -8.5/-9.1 m rel. LAT) against the model seabed and the lofted reef (crest +0.56 m rel. LAT): the reef is not in the DTM and the DTM is 1-3 m deeper than the model.",
       vis=False, state="analysis diagram (model: as-built 2009; survey surface April 2011)", used=["cross_check", "3d_seabed", "3d_tides"],
       how="Depths read: cell means -3.99 (y 90-205 m), -5.62 (210-320), -7.05 (325-435), -8.52 / -9.10 (440-555), -10.17 (560-650) m rel. LAT; model curves converted with z_LAT = z_MSL + 1.46. Result: Delta = EMODnet - model seabed = -1.39 m at the reef cell, -1.80 +- 0.66 m over 7 cells. Not used for model values; far-field slope proposed in REPORT.md section 'Integration plan'.",
       linked=[f"{OUT}/REPORT.md", f"{OUT}/data/boscombe-surf-reef_profile_through_reef_centre_with_model.csv", f"{OUT}/data/boscombe-surf-reef_profile_REST_depth_profile_y0_500.csv"], check=BOS_CHECK, affected=["seabed", "tides"]),
  dict(file="figures/boscombe-surf-reef_cells_emodnet_vs_model.png", annotated=[], kind="diagram",
       title="EMODnet DTM 2024 cell means vs the project model averaged over the same cell footprints at Boscombe (7 cells fully inside the model grid)",
       cite=CITE_PLOT, url="https://erddap.emodnet.eu/erddap/griddap/bathymetry_dtm_2024", page="plot made with scripts/make_plots.py from data/boscombe-surf-reef_cells_emodnet_vs_model.csv",
       date="plot 2026-10-06; EMODnet DTM 2024", credit="Plot by this project; EMODnet Bathymetry Consortium (data)", lic=LICENCE_PLOT,
       shows="Bars per DTM cell: EMODnet mean (with min-max) against the model seabed, as-built surface and April 2011 survey surface, all m rel. LAT; the reef cell would be 1.1 m shallower on average if the DTM contained a reef like the model's.",
       vis=False, state="analysis diagram", used=["cross_check", "3d_seabed"],
       how="Cell-footprint averages of the model (2 m seabed grid and 1 m reef grid, z_LAT = z_MSL + 1.46) against EMODnet cell means: Delta -1.14 .. -3.05 m (mean -1.80, sd 0.66); the 3 best-sampled cells (n = 12) -1.14, -1.39, -1.30 m. Documents that the DTM cannot validate toe/crest; used only as a cross-check.",
       linked=[f"{OUT}/REPORT.md", f"{OUT}/data/boscombe-surf-reef_cells_emodnet_vs_model.csv", f"{OUT}/data/boscombe-surf-reef_comparison_summary.json"], check=BOS_CHECK, affected=["seabed", "tides"]),
  dict(file="figures/boscombe-surf-reef_dtm_release_history.png", annotated=[], kind="diagram",
       title="EMODnet DTM cells along the Boscombe profile in the releases 2018, 2020, 2022 and 2024",
       cite=CITE_PLOT.replace("ERDDAP dataset bathymetry_dtm_2024", "WCS coverages emodnet__mean_2018/2020/2022/mean").replace("https://erddap.emodnet.eu/erddap/griddap/bathymetry_dtm_2024", "https://ows.emodnet-bathymetry.eu/wcs"),
       url="https://ows.emodnet-bathymetry.eu/wcs", page="plot made with scripts/make_plots.py from data/boscombe-surf-reef_cells_releases_wcs.csv",
       date="plot 2026-10-06; DTM releases 2018, 2020, 2022, 2024", credit="Plot by this project; EMODnet Bathymetry Consortium (data)", lic=LICENCE_PLOT,
       shows="Cell means along the profile: releases 2020, 2022 and 2024 are identical; release 2018 (stored positive-down, sign flipped here) is 0.4 m shallower at the reef cell and 2.6 m shallower in the shoreward cell.",
       vis=False, state="analysis diagram", used=["cross_check"],
       how="Shows that the DTM at the reef did not change after release 2020 and does not contain the reef in any release; supports the survey-age inference (CDI 117452 age class 2 in 2018/2020, 1 in 2022/2024 -> survey about 2011-2012). Not used for model values.",
       linked=[f"{OUT}/REPORT.md", f"{OUT}/data/boscombe-surf-reef_cells_releases_wcs.csv"], check=BOS_CHECK, affected=["seabed"]),
 ],
 "borth-coastal-defence-reef": [
  dict(file="viewer/borth-coastal-defence-reef_viewer_dtm_raw.png", annotated=["viewer/borth-coastal-defence-reef_viewer_dtm_annotated.png"], kind="chart_screenshot",
       title="EMODnet Map Viewer at Borth: DTM 2024 mean depth over Esri imagery, with DTM cell grid, both reef mounds, points and shore-normal profile",
       cite=CITE_VIEWER, url="https://emodnet.ec.europa.eu/geoviewer/", page="layer 14159 'Mean depth natural colour (with land)', centre 52.4835 N 4.0562 W, 1040 x 660 m, 50 % opacity",
       date="DTM 2024 (published 2024-12-31); screenshot 2026-10-06; Esri basemap date not stated by the viewer", credit="EMODnet Bathymetry Consortium (data); Esri, Maxar, Earthstar Geographics (basemap); annotations by this project", lic=LICENCE,
       shows="The two rock mounds (northern hook and southern oval, yellow outline) lie within 3-4 DTM cells whose values are -0.1 to -0.4 m rel. LAT; cells landward of the mounds (+2.7, +5.4) and the reef cells are marked 'i' = interpolated (GEBCO fill).",
       vis=True, state="as-built (current Esri imagery; rock bare at low tide)", used=["cross_check", "3d_seabed", "3d_tides"],
       how="Read the EMODnet cell values at the reef centre (-0.18 m rel. LAT, interpolated, reference GEBCO2024), the mound toes (-0.13 .. -0.40) and seabed points (-0.12 .. -1.10; +0.97 shoreward) from the 16 points in data/borth-coastal-defence-reef_points_emodnet.csv. Not used for model values; offshore gradient and 'reef at about LAT' are the only items proposed in REPORT.md.",
       linked=[f"{OUT}/REPORT.md", f"{OUT}/data/borth-coastal-defence-reef_points_emodnet.csv", "07_scale/shapes/borth-coastal-defence-reef/shape.json (geo.polygons_latlon, canonical frame)"], check=BORTH_CHECK, affected=["seabed", "tides"]),
  dict(file="viewer/borth-coastal-defence-reef_viewer_sources_raw.png", annotated=["viewer/borth-coastal-defence-reef_viewer_sources_annotated.png"], kind="chart_screenshot",
       title="EMODnet Map Viewer at Borth: 'Source references' layer over Esri imagery with cell grid, reef outlines and profile",
       cite=CITE_VIEWER, url="https://emodnet.ec.europa.eu/geoviewer/", page="layer 13012 'Source Reference of the DTM' (V2024), same view as the mean-depth screenshot, 55 % opacity",
       date="V2024 source references (record revised 2025-03-01); screenshot 2026-10-06", credit="EMODnet Bathymetry Consortium (data); Esri, Maxar, Earthstar Geographics (basemap); annotations by this project", lic=LICENCE,
       shows="One survey patch (CDI 115084, EDMO 2607 OceanWise Limited; the CDI polygon service lists a 'CARDIGAN BAY' polygon of OceanWise here) covers the sea west of the beach; the cells nearest the beach, including the reef cells, are interpolated (GEBCO 2024 fill).",
       vis=True, state="as-built (current Esri imagery; rock bare at low tide)", used=["cross_check", "3d_seabed"],
       how="Used to identify the source of the DTM cells at the reef (CDI 115084 + GEBCO 2024 fill) and its quality index (horizontal 0, vertical 3, age 0 = older than 30 y, purpose 3). Documented in REPORT.md; no model value taken.",
       linked=[f"{OUT}/REPORT.md", f"{OUT}/data/borth-coastal-defence-reef_results.json"], check=BORTH_CHECK, affected=["seabed"]),
  dict(file="figures/borth-coastal-defence-reef_profile_emodnet.png", annotated=[], kind="diagram",
       title="Shore-normal depth profile through the Borth reef mounds from the EMODnet DTM 2024 cells (reef centre, northern hook, southern oval) and the REST depth_profile",
       cite=CITE_PLOT, url="https://rest.emodnet-bathymetry.eu/depth_profile", page="plot made with scripts/make_plots.py; lines x = 0, +38.9 and -85.3 m, y = -100..650 m, bearing 269.57 deg (west)",
       date="plot 2026-10-06; EMODnet DTM 2024", credit="Plot by this project; EMODnet Bathymetry Consortium (data); reef outlines from the project's shape.json", lic=LICENCE_PLOT,
       shows="Steps of the DTM along the shore normal: land / beach cells +5.4, +2.7 (interpolated), reef cells -0.34..-0.13 (interpolated, GEBCO), then surveyed cells -0.40, -1.10, -1.91, -2.73, -3.36 m rel. LAT out to 650 m; the reef mounds are invisible at this resolution.",
       vis=False, state="analysis diagram", used=["cross_check", "3d_seabed", "3d_tides"],
       how="Offshore gradient from the surveyed cells (y 335-650 m): -1.1 % (about 1:90); reef-cell values -0.34..-0.13 m rel. LAT are GEBCO fill and only indicate 'reef near LAT'. Proposed in REPORT.md for the future Borth 3D model; nothing is in a model yet.",
       linked=[f"{OUT}/REPORT.md", f"{OUT}/data/borth-coastal-defence-reef_profile_through_reef_centre.csv", f"{OUT}/data/borth-coastal-defence-reef_profile_REST_depth_profile_y0_500.csv"], check=BORTH_CHECK, affected=["seabed", "tides"]),
 ],
}


def sha(path):
    h = hashlib.sha256(); h.update(open(path, "rb").read()); return h.hexdigest()


def md_section(r):
    ck = r["for_3d_check"]
    lines = [f"## {r['id']} - {r['title']}", "", f"![{r['id']}](../../../{r['file']})", ""]
    lines += [f"- **file**: `{r['file']}`"]
    if r["annotated_files"]: lines += [f"- **annotated versions**: " + "; ".join(f"`{a}`" for a in r["annotated_files"])]
    lines += [f"- **kind**: {r['kind']}", f"- **shows**: {r['shows']}", f"- **structure visible**: {r['structure_visible']}", f"- **state shown**: {r['state_shown']}",
              f"- **image date**: {r['image_date']}", f"- **citation**: {r['citation']}", f"- **image URL**: {r['image_url']}", f"- **source page**: {r['source_page']}",
              f"- **page / figure**: {r['page_or_figure']}", f"- **credit**: {r['credit']}", f"- **licence**: {r['license']}", f"- **retrieved**: {r['retrieved']}",
              f"- **used for**: {'; '.join(r['used_for'])}", f"- **How used for the model**: {r['how_used']}",
              f"- **3D check pending**: {'YES' if ck['pending'] else 'no'} - {ck['what_to_check']} (values: {', '.join(ck['model_values_affected'])})",
              f"- **linked records**: {'; '.join(r['linked_records'])}", f"- **size**: {r['bytes']/1e6:.2f} MB, {r['px'][0]}x{r['px'][1]} px", f"- **sha256**: {r['sha256']}",
              f"- **rights**: {r['rights_note']}", f"- **display in HTML**: {r['display']}", f"- **added by**: {r['added_by']}", ""]
    return "\n".join(lines)


registered = []
for slug, rows in ROWS.items():
    jpath = f"{REG}/{slug}/images.json"; mpath = f"{REG}/{slug}/IMAGES.md"
    data = json.load(open(jpath, encoding="utf-8"))                      # re-read right before writing
    have = {r["file"] for r in data}; nxt = max(int(r["id"].rsplit("-", 1)[1]) for r in data) + 1
    new_md = []; log = []
    for row in rows:
        rel = f"{OUT}/{row['file']}"
        if rel in have: print("already registered", rel); continue
        full = f"{ROOT}/{rel}"; im = Image.open(full)
        rid = f"{slug}-img-{nxt:02d}"; nxt += 1
        rec = {"id": rid, "file": rel, "annotated_files": [f"{OUT}/{a}" for a in row["annotated"]], "kind": row["kind"], "title": row["title"], "citation": row["cite"],
               "image_url": row["url"], "source_page": row["url"], "page_or_figure": row["page"], "image_date": row["date"], "credit": row["credit"], "license": row["lic"],
               "retrieved": TODAY, "shows": row["shows"], "structure_visible": row["vis"], "state_shown": row["state"], "used_for": row["used"], "how_used": row["how"],
               "linked_records": row["linked"], "bytes": os.path.getsize(full), "px": [im.size[0], im.size[1]], "sha256": sha(full),
               "rights_note": "Private research copy; reuse rights to be checked before any public release.", "display": True,
               "for_3d_check": {"pending": True, "what_to_check": row["check"], "model_values_affected": row["affected"]}, "added_by": ADDED}
        data.append(rec); new_md.append(md_section(rec)); registered.append(f"{rid} - {rel} - {row['title'][:110]}")
        log.append(f"{TODAY} | {slug} | {rid} | {rel} | {row['shows'][:170]} | PENDING: {row['check'][:230]} | {ADDED}")
    if not new_md: continue
    json.dump(data, open(jpath, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    md = open(mpath, encoding="utf-8").read().rstrip("\n") + "\n\n" + "\n".join(new_md)
    n = len(data); nf = sum(1 for r in data if r.get("file")); nu = sum(1 for r in data if any(u not in ("context", "not_used") for u in r.get("used_for", [])))
    md = re.sub(r"\d+ images registered, \d+ with a file, \d+ used for the model", f"{n} images registered, {nf} with a file, {nu} used for the model", md, count=1)
    open(mpath, "w", encoding="utf-8").write(md)
    with open(f"{REG}/NEW_IMAGES_LOG.md", "a", encoding="utf-8") as f: f.write("\n".join(log) + "\n")
print("\n".join(registered))
json.dump(registered, open(f"{ROOT}/{OUT}/data/images_registered.json", "w", indent=1) if False else open(f"{ROOT}/{OUT}/data/images_registered.json", "w"), indent=1)

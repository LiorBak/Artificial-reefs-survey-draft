"""register_images.py - STEP 0 of the 3D brief for Borth: close the pending for_3d_check rows (results from METHODS_3D.md section 4) and register the
new images (Navionics screenshot series, annotated figures) in 03_images/reefs/borth-coastal-defence-reef/images.json + IMAGES.md + NEW_IMAGES_LOG.md.
Adapted from narrowneck-gold-coast/scripts/nnreg.py.  Idempotent: rows already registered (same file / sha256) are skipped; updates are re-applied safely.
Run from this folder:  python register_images.py
"""
import os, json, hashlib, re, glob
from PIL import Image

ROOT = r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git"
SLUG = "borth-coastal-defence-reef"
REG = os.path.join(ROOT, "03_images", "reefs")
JS = os.path.join(REG, SLUG, "images.json"); MD = os.path.join(REG, SLUG, "IMAGES.md"); LOG = os.path.join(REG, "NEW_IMAGES_LOG.md")
D3 = os.path.join(ROOT, "07_scale", "shapes", SLUG, "3d")
TODAY = "2026-10-07"
BY = "Borth 3D model, finish run, 2026-10-07"
RIGHTS = "Private research copy; reuse rights to be checked before any public release."
M = "07_scale/shapes/borth-coastal-defence-reef/3d/METHODS_3D.md"
S = "07_scale/shapes/borth-coastal-defence-reef/3d/SOURCES_3D.md"


def rel(p): return os.path.relpath(p, ROOT).replace("\\", "/")
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""): h.update(ch)
    return h.hexdigest()
def load(): return json.load(open(JS, encoding="utf8"))
def save(rows):
    tmp = JS + ".tmp"; json.dump(rows, open(tmp, "w", encoding="utf8"), indent=1, ensure_ascii=False); os.replace(tmp, JS)
def next_id(rows): return "%s-img-%02d" % (SLUG, max(int(r["id"].rsplit("-", 1)[1]) for r in rows) + 1)
def A(name): return rel(os.path.join(D3, "annotated", name))


def add(file, kind, title, cit, url, page, pf, date, credit, lic, shows, vis, state, used, how, f3d, ann=(), linked=(), extra=None):
    f = os.path.join(ROOT, file) if not os.path.isabs(file) else file
    rows = load(); sh = sha(f); fr = rel(f)
    hit = [r for r in rows if r.get("sha256") == sh or r.get("file") == fr]
    if hit:
        print("already registered", hit[0]["id"], fr); return hit[0]["id"]
    px = list(Image.open(f).size); rid = next_id(rows)
    row = {"id": rid, "file": fr, "annotated_files": list(ann), "kind": kind, "title": title, "citation": cit, "image_url": url, "source_page": page,
           "page_or_figure": pf, "image_date": date, "credit": credit, "license": lic, "retrieved": TODAY, "shows": shows, "structure_visible": vis,
           "state_shown": state, "used_for": used, "how_used": how, "linked_records": list(linked), "bytes": os.path.getsize(f), "px": px, "sha256": sh,
           "rights_note": RIGHTS, "display": True, "for_3d_check": f3d, "added_by": BY}
    if extra: row.update(extra)
    rows.append(row); save(rows)
    with open(MD, "a", encoding="utf8") as m:
        m.write("\n## %s - %s\n\n![%s](../../../%s)\n\n" % (rid, title, rid, fr))
        m.write("- **file**: `%s`\n- **kind**: %s\n- **shows**: %s\n- **structure visible**: %s\n- **state shown**: %s\n- **image date**: %s\n"
                "- **citation**: %s\n- **image URL**: %s\n- **source page**: %s\n- **page / figure**: %s\n- **credit**: %s\n- **licence**: %s\n- **retrieved**: %s\n"
                "- **used for**: %s\n- **How used for the model**: %s\n- **3D check pending**: %s - %s\n- **linked records**: %s\n- **size**: %d bytes, %dx%d px\n"
                "- **sha256**: %s\n- **rights**: %s\n- **display in HTML**: True\n- **added by**: %s\n" % (
                    fr, kind, shows, vis, state, date, cit, url, page, pf, credit, lic, TODAY, ", ".join(used), how,
                    "YES" if f3d["pending"] else "no", f3d["what_to_check"], "; ".join(linked), row["bytes"], px[0], px[1], sh, RIGHTS, BY))
        if ann: m.write("- **annotated versions**: %s\n" % ", ".join(ann))
        if extra and extra.get("group_files"): m.write("- **group files** (%d): %s ... %s\n" % (len(extra["group_files"]), extra["group_files"][0], extra["group_files"][-1]))
    with open(LOG, "a", encoding="utf8") as l:
        l.write("%s | %s | %s | %s | %s | %s | %s\n" % (TODAY, SLUG, rid, fr, shows[:140].replace("|", "/"),
                (("PENDING: " if f3d["pending"] else "no check: ") + f3d["what_to_check"]).replace("|", "/"), BY))
    print("registered", rid, fr); return rid


def update(rid, result=None, pending=None, add_annotated=(), used_for_add=(), how_append=None, linked_add=()):
    rows = load(); r = [x for x in rows if x["id"] == rid][0]; f = r.setdefault("for_3d_check", {})
    new_ann = [a for a in add_annotated if a not in r["annotated_files"]]
    done = bool(result) and f.get("result") == result
    if pending is not None: f["pending"] = pending
    if result: f["result"] = result
    r["annotated_files"] += new_ann
    for u in used_for_add:
        if u not in r["used_for"]: r["used_for"].append(u)
    if how_append and how_append not in r.get("how_used", ""): r["how_used"] = (r["how_used"] + " " if r.get("how_used") else "") + how_append
    else: how_append = None
    for l in linked_add:
        if l not in r["linked_records"]: r["linked_records"].append(l)
    save(rows)
    if done and not new_ann: print("unchanged", rid); return
    t = open(MD, encoding="utf8").read(); m = re.search(r"(## %s - .*?)(?=\n## |\Z)" % re.escape(rid), t, re.S)
    if not m: print("no IMAGES.md section for", rid); return
    sec = m.group(1); add_lines = ""
    if result and not done: add_lines += "- **3D check result (%s)**: %s\n" % (TODAY, result)
    if how_append: add_lines += "- **How used (update %s)**: %s\n" % (TODAY, how_append)
    if new_ann: add_lines += "- **annotated versions (added %s)**: %s\n" % (TODAY, ", ".join(new_ann))
    if pending is not None: sec = re.sub(r"- \*\*3D check pending\*\*: (YES|no)", "- **3D check pending**: %s" % ("YES" if pending else "no"), sec, count=1)
    sec = sec.rstrip("\n") + "\n" + add_lines
    open(MD, "w", encoding="utf8").write(t[:m.start(1)] + sec + t[m.end(1):]); print("updated", rid)


def series(tag):
    return sorted(rel(p) for p in glob.glob(os.path.join(D3, "src", "navionics", tag + "_shade*.png")))


def main():
    P = SLUG + "-img-"
    NAVCIT = ("Garmin Ltd / Navionics (2026). Marine Maps viewer, %s, depths in metres, zoom %d; series of 11 screenshots with 'Shallow shading' 0, 1, ... 10 m "
              "(centre 52.483453 N, 4.056205 W; page title 'Garmin | Marine Maps', 'Not to be used for navigation'). "
              "https://maps.garmin.com/en-US/marine?maps=another-brand&overlay=false&key=gcm4edq678dp (webapp.navionics.com redirects here). "
              "Captured 2026-10-07 by capture_navionics.py (own headless Chrome). Accessed 2026-10-07.")
    URL = "https://maps.garmin.com/en-US/marine?maps=another-brand&overlay=false&key=gcm4edq678dp"
    f3d = {"pending": False, "what_to_check": "none: seabed and datum cross-check done (METHODS_3D.md 3.6)", "model_values_affected": []}
    how = ("Navionics cross-check (not a model input): contour lines read along 8 pixel rows (0 m = edge of the drying area at y 385-430 m, then 0.5, 1, 1.5, 2, 2.5 m); "
           "datum test by RMS: LAT best (RMS 1.15 m vs HRPP576 Fig 2 -4.0, 0.64 vs EMODnet, 2.30 vs the model) but the chart is 0.6-1.1 m shallower than the references offshore; "
           "the rock mounds are inside the uniform drying area and are not charted (no crest or height reading possible). SOURCES_3D.md STEP 2; METHODS_3D.md 3.6; model.js navionics.")
    lk = [S + " (STEP 2, Navionics)", "07_scale/shapes/borth-coastal-defence-reef/3d/src/navionics/capture_log.json", "07_scale/shapes/borth-coastal-defence-reef/3d/nav_read.py", M + " section 3.6"]
    ids = {}
    for tag, chart, z, ann in (("sonar_z17", "SonarChart Maps", 17, ["A9_navionics_sonarchart_z17_annotated.png"]), ("sonar_z18", "SonarChart Maps", 18, []),
                               ("naut_z17", "Nautical Charts", 17, []), ("naut_z18", "Nautical Charts", 18, ["A10_navionics_nautical_z18_reef_outline.png"])):
        g = series(tag)
        ids[tag] = add(g[0], "chart_screenshot", "Garmin Navionics %s, zoom %d, Borth reef: shallow-shading series 0-10 m (11 files)" % (chart, z), NAVCIT % (chart, z), URL, URL,
                       "%s zoom %d (%.3f m/px); files %s_shade00.0 .. shade10.0 (the blue area is water shallower than the setting, so its edge is the chart contour of that depth)" % (chart, z, 0.730 if z == 17 else 0.365, tag),
                       "chart data dates not shown by the viewer; screenshots 2026-10-07", "Garmin Navionics charts and SonarChart (c) Navionics / Garmin Ltd; screenshots by this project (own headless Chrome)",
                       "Garmin/Navionics terms ('Not to be used for navigation'); no open licence; private research copy, reuse NOT cleared",
                       "The chart around the Borth reef at each shallow-shading value: a uniform green drying area from the beach to y 385-430 m with no raised feature at the rock mounds, contours 0.5-2.5 m seaward of it, one charted shoal 35 m off the north mound head.",
                       False, "seabed (chart, data date unknown); the structure is not shown", ["3d_seabed", "cross_check"], how, f3d,
                       ann=[A(a) for a in ann], linked=lk, extra={"group_files": g})
    add(os.path.join(D3, "annotated", "A8_seabed_source_zones.png"), "diagram", "Borth model seabed: control nodes by source and modelled contours (figure by this project)",
        "This project (2026-10-07). Seabed source-zone map of the Borth 3D model; data: Welsh Government LiDAR 2022 DTM (OGL v3), HRPP576 Fig 2 (Rigden et al. 2013), Royal Haskoning drawings 9V5090/1021-1023, EMODnet DTM 2024 (CC BY 4.0). make_annotations.py.",
        "n/a (own figure)", "07_scale/shapes/borth-coastal-defence-reef/3d/make_annotations.py", "annotated A8", "2026-10-07", "this project (figure); data owners as cited",
        "figure: private research copy; data licences as cited",
        "Plan map (x alongshore, y offshore) of the thin-plate seabed fit with the control nodes coloured by source (LiDAR beach, Fig 2 -3.0 contour, design bed under the arm and oval, assumed tail bed, assumed anchor -4.0 at y = 335 m) and the modelled contours.",
        True, "model seabed (derived)", ["3d_seabed", "cross_check"],
        "Documents where every part of the modelled seabed comes from; shows the weak zones (tail bed assumed, anchor assumed, nothing between y 335 and 520 m but the EMODnet gradient). METHODS_3D.md 3.3 and 4.4.",
        {"pending": False, "what_to_check": "none: documentation figure", "model_values_affected": []}, linked=[M + " section 3.3", S])

    R = {
        P + "14": ("MSL - LAT = 2.75 m (z_MSL = e_LAT - 2.75). The reef-zone EMODnet cells (-2.78..-2.57 mODN) are 1.0-1.4 m shallower than the design bed (-4.0): GEBCO interpolation, not used. Only the offshore gradient -1.1 % (survey cells from y 335 m) is used; the seabed seaward of y 335 m is NOT validated by it (model 1.5 m deeper than the cells at y 368-513, see METHODS_3D 4.4).", []),
        P + "15": ("One survey patch (CDI 115084, OceanWise) supplies the gradient -1.1 % for y 368-652 m (one sounding per cell, age > 30 y): used as a gradient only, anchored on the design bed level at y = 335 m. Kept as context; the Navionics datum test (METHODS_3D 3.6) puts the chart 0.6 m shallower than these cells.", []),
        P + "16": ("The DTM steps along the shore normal confirm the trend (-1.1 %); the absolute reef-zone values are interpolated and are not used. Model vs EMODnet at x -30: 1.5-1.6 m deeper at y 368-513 (METHODS_3D 4.4).", []),
        P + "17": ("Fig 2 traced and georeferenced (A1): -3.0 contour used as seabed control outside the reef zone (model minus contour -0.01 m, n 24); -2.0 contour -0.14 m (n 24, not a control); -4.0 contour: the model is 0.89 m DEEPER (sd 0.14, n 13), because only the -3.0 contour and the -4.0 anchor at y = 335 m plus the EMODnet gradient were used. Open issue (METHODS_3D 4.4, 7).", [A("A1_fig2_contours_read.png"), A("A7_lidar_beach_vs_fig2.png")]),
        P + "20": ("Rings 0-4, crest paths R1-R6 / R2-R5 and the setting-out points R1-R15 re-projected onto the drawing (A2): agree to about 1 pixel; design foot ring IoU 0.9998 against shape.json. Used for the design version, the crest zones (+0.50 / +1.00 / +0.00 ramp 40 m / +1.50) and the toe rings. Note: S1-S1 on 1023 dimensions the oval 46 m between R15 and R14, the SOP table gives 38 m (unresolved).", [A("A2_drg1020_rings_and_sop_read.png")]),
        P + "21": ("Readings confirmed (A3): arm crest +0.50, Type 4 underside -2.20, head +0.00 / -2.70, tail +1.00 / -1.70, transitions 40 m and 15 m, toe berm 1350 / 3000 / 2000 / 500 mm, MHWS +2.56 / MLWS -1.74 printed; the bed -4.0 mODN is derived (2.70 + 1.31 + 0.50 below +0.50), the ground line is schematic.", [A("A3_drg1021_sections_read.png")]),
        P + "22": ("Readings confirmed (A4): N4 crest +0.50 with 1:4 flanks, layer 2.70 m; N5 / N6 head sections +0.00 / -2.70 at SOP R1 / R10; same toe berm as 1021.", [A("A4_drg1022_sections_read.png")]),
        P + "23": ("Readings confirmed (A5): oval crest +1.50, flat top 3000 + 3000 = 6 m, flanks 1:3, Type 4 underside -1.20, Type 5 underside -2.90 (bed derived -3.4, 0.2 m above the printed range), printed bed note '-4.2 TO -3.6m AOD' used for the oval nodes (-3.6 shoreward, -4.2 seaward).", [A("A5_drg1023_sections_read.png")]),
        P + "24": ("LiDAR DSM inside the design crest strips (A6): N arm median +0.58 / p90 +0.91 against design +0.50; oval median +1.55 / p90 +1.75 against +1.50; default surface minus design surface above -2.0 mODN: mean +0.14 m, sd 0.28 m; as-built flanks flatter (1:4-1:5) and 8-10 m wider than the 1:3 design. Beach DTM vs Fig 2: salient behind the mounds (A7).", [A("A6_lidar_crest_check.png")]),
    }
    for rid, (res, ann) in R.items():
        update(rid, result=res, pending=False, add_annotated=ann, how_append="Result of the 3D check %s: %s" % (TODAY, res.split(". ")[0] + ".") if rid.endswith(("14", "15", "16")) else None,
               linked_add=[M + " section 4.5", S])
    # header count in IMAGES.md
    rows = load(); t = open(MD, encoding="utf8").read()
    used = sum(1 for r in rows if any(u not in ("context", "not_used") for u in r.get("used_for", [])))
    t = re.sub(r"\d+ images registered, \d+ with a file, \d+ used for the model", "%d images registered, %d with a file, %d used for the model" % (len(rows), sum(1 for r in rows if r.get("file")), used), t, count=1)
    open(MD, "w", encoding="utf8").write(t)


if __name__ == "__main__":
    main()

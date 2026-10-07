"""Register the images found by the Gold Coast government/council/university report search
(2026-10-06) in 03_images/reefs/<slug>/images.json + IMAGES.md + NEW_IMAGES_LOG.md.
Idempotent: a file already registered (same path or same sha256) is skipped.
images.json is re-read immediately before each write (append only).
Entries live in register_entries.py (so that this file stays small)."""
import os, json, hashlib, sys
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import register_entries_2  # noqa: appends more entries to E
import register_entries_3  # noqa
from register_entries import E, ROOT, REG, WORK, TODAY, BY, RIGHTS


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def load(slug):
    d = REG + "\\" + slug
    os.makedirs(d, exist_ok=True)
    p = d + r"\images.json"
    if os.path.exists(p):
        return json.load(open(p, encoding="utf8"))
    return []


def save(slug, rows):
    p = REG + "\\" + slug + r"\images.json"
    json.dump(rows, open(p, "w", encoding="utf8"), indent=1, ensure_ascii=False)


def next_id(slug, rows):
    n = 0
    for r in rows:
        try:
            n = max(n, int(str(r.get("id", "")).rsplit("-", 1)[1]))
        except Exception:
            pass
    return "%s-img-%02d" % (slug, n + 1)


def main():
    for e in E:
        slug = e["slug"]
        f = e["file"]
        if not os.path.exists(f):
            print("MISSING", f)
            continue
        rows = load(slug)  # re-read right before writing
        sh = sha(f)
        fr = rel(f)
        hit = [r for r in rows if r.get("sha256") == sh or r.get("file") == fr]
        if hit:
            e["rid"] = hit[0]["id"]
            print("already registered", fr, e["rid"])
            continue
        im = Image.open(f)
        px = [im.width, im.height]
        rid = next_id(slug, rows)
        row = {"id": rid, "file": fr, "annotated_files": [rel(a) for a in e["ann"]], "kind": e["kind"], "title": e["title"],
               "citation": e["cit"], "image_url": e["url"], "source_page": e["page"], "page_or_figure": e["pf"],
               "image_date": e["date"], "credit": e["credit"], "license": e["lic"], "retrieved": TODAY,
               "shows": e["shows"], "structure_visible": e["vis"], "state_shown": e["state"], "used_for": e["used"],
               "how_used": e["how"], "for_3d_check": e["f3d"],
               "linked_records": ["07_scale/bathymetry/gold_coast/SOURCES.md " + e["gc"], "07_scale/bathymetry/gold_coast/REPORT.md"],
               "bytes": os.path.getsize(f), "px": px, "sha256": sh, "rights_note": RIGHTS, "display": True, "added_by": BY}
        rows.append(row)
        save(slug, rows)
        e["rid"] = rid
        md = REG + "\\" + slug + r"\IMAGES.md"
        if not os.path.exists(md):
            open(md, "w", encoding="utf8").write("# IMAGES - %s (registry; one section per image, mirrors images.json)\n\n" % slug)
        with open(md, "a", encoding="utf8") as m:
            m.write("## %s - %s\n- file: `%s`\n- annotated: %s\n- kind: %s | state: %s | structure visible: %s | date: %s\n"
                    "- citation: %s\n- image URL: %s | source page: %s | page/figure: %s\n- credit: %s | licence: %s | retrieved: %s\n"
                    "- shows: %s\n- used for: %s\n- how used: %s\n- for_3d_check: pending=%s; check: %s; affects: %s\n- linked: %s\n"
                    "- %d bytes, %dx%d px, sha256 %s\n- %s (added by %s)\n\n" % (
                        rid, e["title"], fr, ", ".join(row["annotated_files"]) or "none", e["kind"], e["state"], e["vis"], e["date"],
                        e["cit"], e["url"], e["page"], e["pf"], e["credit"], e["lic"], TODAY, e["shows"], ", ".join(e["used"]), e["how"],
                        e["f3d"]["pending"], e["f3d"]["what_to_check"], ", ".join(e["f3d"]["model_values_affected"]) or "none",
                        "; ".join(row["linked_records"]), row["bytes"], px[0], px[1], sh, RIGHTS, BY))
        log = REG + r"\NEW_IMAGES_LOG.md"
        if not os.path.exists(log):
            open(log, "w", encoding="utf8").write("# NEW IMAGES LOG (append only)\ndate | slug | registry id | file | shows | for_3d_check what_to_check | added_by\n\n")
        with open(log, "a", encoding="utf8") as l:
            l.write("%s | %s | %s | %s | %s | %s | %s\n" % (
                TODAY, slug, rid, fr, e["shows"][:140].replace("|", "/"),
                (("PENDING: " if e["f3d"]["pending"] else "no check: ") + e["f3d"]["what_to_check"]).replace("|", "/"), BY))
        print("registered", rid, fr)
    json.dump([{k: e.get(k) for k in ("slug", "rid", "gc", "file", "title", "kind", "cit", "url", "pf", "date", "credit", "lic", "shows")} for e in E],
              open(WORK + r"\tools\registered_images.json", "w", encoding="utf8"), indent=1)


if __name__ == "__main__":
    main()

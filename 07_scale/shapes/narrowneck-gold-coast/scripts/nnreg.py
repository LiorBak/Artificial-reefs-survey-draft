"""Registry helper for narrowneck-gold-coast (append-only; re-reads images.json right before each write)."""
import os, json, hashlib, re, tempfile
from PIL import Image
ROOT = r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git"
SLUG = "narrowneck-gold-coast"
REG = os.path.join(ROOT, "03_images", "reefs")
JS = os.path.join(REG, SLUG, "images.json")
MD = os.path.join(REG, SLUG, "IMAGES.md")
LOG = os.path.join(REG, "NEW_IMAGES_LOG.md")
TODAY = "2026-10-06"
BY = "narrowneck-gold-coast plan-shape trace (resume), 2026-10-06"
RIGHTS = "Private research copy; reuse rights to be checked before any public release."

def rel(p): return os.path.relpath(p, ROOT).replace("\\", "/")
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""): h.update(ch)
    return h.hexdigest()
def load(): return json.load(open(JS, encoding="utf8"))
def save(rows):
    tmp = JS + ".tmp"
    json.dump(rows, open(tmp, "w", encoding="utf8"), indent=1, ensure_ascii=False)
    os.replace(tmp, JS)
def next_id(rows):
    n = max(int(r["id"].rsplit("-", 1)[1]) for r in rows)
    return "%s-img-%02d" % (SLUG, n + 1)

def add(file, kind, title, cit, url, page, pf, date, credit, lic, shows, vis, state, used, how, f3d, ann=(), linked=(), extra=None):
    f = os.path.join(ROOT, file) if not os.path.isabs(file) else file
    rows = load()
    sh = sha(f); fr = rel(f)
    hit = [r for r in rows if r.get("sha256") == sh or r.get("file") == fr]
    if hit:
        print("already registered", hit[0]["id"], fr); return hit[0]["id"]
    px = list(Image.open(f).size)
    rid = next_id(rows)
    row = {"id": rid, "file": fr, "annotated_files": [rel(os.path.join(ROOT, a)) if not os.path.isabs(a) else rel(a) for a in ann],
           "kind": kind, "title": title, "citation": cit, "image_url": url, "source_page": page, "page_or_figure": pf,
           "image_date": date, "credit": credit, "license": lic, "retrieved": TODAY, "shows": shows,
           "structure_visible": vis, "state_shown": state, "used_for": used, "how_used": how,
           "linked_records": list(linked), "bytes": os.path.getsize(f), "px": px, "sha256": sh, "rights_note": RIGHTS,
           "display": True, "for_3d_check": f3d, "added_by": BY}
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
    with open(LOG, "a", encoding="utf8") as l:
        l.write("%s | %s | %s | %s | %s | %s | %s\n" % (TODAY, SLUG, rid, fr, shows[:140].replace("|", "/"),
                (("PENDING: " if f3d["pending"] else "no check: ") + f3d["what_to_check"]).replace("|", "/"), BY))
    print("registered", rid, fr)
    return rid

def update(rid, result=None, pending=None, add_annotated=(), used_for_add=(), how_append=None, linked_add=()):
    """Update an existing row (planform check result), mirror in IMAGES.md."""
    rows = load()
    r = [x for x in rows if x["id"] == rid][0]
    f = r.setdefault("for_3d_check", {})
    if pending is not None: f["pending"] = pending
    if result: f["result"] = result
    for a in add_annotated:
        a = rel(os.path.join(ROOT, a)) if not os.path.isabs(a) else rel(a)
        if a not in r["annotated_files"]: r["annotated_files"].append(a)
    for u in used_for_add:
        if u not in r["used_for"]: r["used_for"].append(u)
    if how_append: r["how_used"] = (r["how_used"] + " " if r.get("how_used") else "") + how_append
    for l in linked_add:
        if l not in r["linked_records"]: r["linked_records"].append(l)
    save(rows)
    t = open(MD, encoding="utf8").read()
    pat = re.compile(r"(## %s - .*?)(?=\n## |\Z)" % re.escape(rid), re.S)
    m = pat.search(t)
    if not m:
        print("no IMAGES.md section for", rid); return
    sec = m.group(1)
    add_lines = ""
    if result:
        add_lines += "- **3D / planform check result (%s)**: %s\n" % (TODAY, result)
    if how_append:
        add_lines += "- **How used (update %s)**: %s\n" % (TODAY, how_append)
    if add_annotated:
        add_lines += "- **annotated versions**: %s\n" % ", ".join(r["annotated_files"])
    if pending is not None:
        sec = re.sub(r"- \*\*3D check pending\*\*: (YES|no)", "- **3D check pending**: %s" % ("YES" if pending else "no"), sec, count=1)
        sec = re.sub(r"- for_3d_check: pending=\w+", "- for_3d_check: pending=%s" % pending, sec, count=1)
    sec = sec.rstrip("\n") + "\n" + add_lines
    t = t[:m.start(1)] + sec + t[m.end(1):]
    open(MD, "w", encoding="utf8").write(t)
    print("updated", rid)

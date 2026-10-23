"""File:// smoke test + saved PNG screenshots, using the locally installed headless Edge/Chrome.

Why: the in-app browser pane refuses file:// URLs and cannot save screenshots to disk.
Headless Edge/Chrome can do both, with no extra installs (no Playwright needed).

Usage:  python qa_shots.py [--prefix round3] [--slug <reef-slug>]
Writes: ../QA/<prefix>_*.png and ../QA/<prefix>_file_smoke.txt ; exit code 1 if the smoke test fails.
"""
import argparse, json, os, re, subprocess, sys, tempfile, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
PAGE = BUILD / "artificial_reefs.html"
QA = BUILD / "QA"
# Chrome first: on this machine headless Edge exits 0 but writes nothing (verified 2026-09-25).
CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def browsers():
    found = [c for c in [os.environ.get("CHROME_PATH", "")] + CANDIDATES if c and Path(c).exists()]
    for n in ("chrome", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "msedge"):
        p = shutil.which(n)
        if p and p not in found:
            found.append(p)
    # Playwright's own Chromium on Linux (python -m playwright install chromium)
    found += [str(h) for h in (sorted(Path.home().glob(".cache/ms-playwright/chromium-*/chrome-linux*/chrome")) + sorted(Path("/opt/pw-browsers").glob("chromium-*/chrome-linux*/chrome")))[-1:]]  # + cloud image
    if not found:
        sys.exit("No Chrome/Edge found for headless QA.")
    return found


def run(exe, args, url, profile, timeout=90):
    cmd = [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
           "--no-default-browser-check", "--allow-file-access-from-files",
           f"--user-data-dir={profile}", "--virtual-time-budget=8000", *args, url]
    if hasattr(os, "geteuid") and os.geteuid() == 0:   # cloud container runs as root: Chrome needs this there
        cmd.insert(1, "--no-sandbox")
    return subprocess.run(cmd, capture_output=True, timeout=timeout)


def strip_scripts(dom):
    """DOM text without <script> bodies (the inline JSON / JS also contain the class names)."""
    return re.sub(r"<script\b[^>]*>.*?</script>", "", dom, flags=re.S)


def retired_view_checks(dom):
    """Checks on a DOM dump of <page>#view/scale (or #view/map): the Map and Scale tabs were removed 2026-10-10,
    so the route must fall back to the gallery and no trace of the two views may remain. Returns {name: bool}."""
    body = strip_scripts(dom)
    g = re.search(r'<section id="view-gallery"([^>]*)>', body)
    return {
        "retired route falls back to the gallery (visible)": bool(g) and "hidden" not in g.group(1),
        "no Map / Scale view section or button": 'id="view-scale"' not in body and 'id="view-map"' not in body
            and 'data-view="scale"' not in body and 'data-view="map"' not in body,
        "top navigation is exactly Gallery, Table, 3D models": re.findall(r'<button type="button" data-view="([a-z0-9]+)"', body) == ["gallery", "table", "models3d"],
    }


def dump_dom(url, exe=None):
    """Headless DOM dump of `url` with the first working Chrome/Edge. Returns (exe, dom)."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:
        for cand in ([exe] if exe else []) + browsers():
            r = run(cand, ["--dump-dom"], url, prof)
            dom = r.stdout.decode("utf-8", "replace")
            if len(dom) > 1000:
                return cand, dom
    return None, ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="round3")
    ap.add_argument("--slug", default=None, help="reef slug for the detail/popover shot (default: first reef)")
    a = ap.parse_args()
    if not PAGE.exists():
        sys.exit(f"Missing {PAGE}; run build.py first.")
    QA.mkdir(exist_ok=True)
    url = PAGE.as_uri()
    html = PAGE.read_text(encoding="utf-8")
    m = re.search(r'<script[^>]*id="data"[^>]*>(.*?)</script>', html, re.S)
    reefs = []
    if m:
        try:
            p = json.loads(m.group(1))
            reefs = p.get("reefs", p) if isinstance(p, dict) else p
        except Exception:
            pass
    slug = a.slug or (reefs[0].get("slug") if reefs and isinstance(reefs[0], dict) else None)

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as prof:
        # 1) smoke test: does the page's JS run from file:// and render content?
        #    Use the first browser that actually returns a DOM (some headless builds return nothing).
        exe, dom = None, ""
        for cand in browsers():
            r = run(cand, ["--dump-dom"], url, prof)
            dom = r.stdout.decode("utf-8", "replace")
            if len(dom) > 1000:
                exe = cand
                break
        exe = exe or browsers()[0]
        report, ok = [f"browser: {exe}", f"url: {url}"], True
        grid = re.search(r'id="grid"[^>]*>(.*?)</div>\s*</section>', dom, re.S)
        checks = {
            "dom dumped": len(dom) > 1000,
            "intro rendered": bool(re.search(r'id="intro"[^>]*>\s*\S', dom)),
            "summary rendered": bool(re.search(r'id="summary"[^>]*>\s*<', dom)),
            "gallery tiles rendered": bool(grid and grid.group(1).count("<img") + grid.group(1).count("<article") > 0),
            "references index rendered": bool(re.search(r'id="refindex"[^>]*>\s*<', dom)),
            "footer rendered": bool(re.search(r'id="footer"[^>]*>\s*\S', dom)),
        }
        if reefs:
            checks[f"all {len(reefs)} reefs appear"] = all(
                (isinstance(x, dict) and x.get("slug", "") in dom) for x in reefs)
        for k, v in checks.items():
            report.append(f"{'PASS' if v else 'FAIL'}  {k}")
            ok &= v

        # 1b) the retired Scale route (#view/scale must fall back to the gallery)
        r2 = run(exe, ["--dump-dom"], url + "#view/scale", prof)
        sdom = r2.stdout.decode("utf-8", "replace")
        (QA / f"{a.prefix}_retired_dom.html").write_text(sdom, encoding="utf-8")
        for k, v in retired_view_checks(sdom).items():
            report.append(f"{'PASS' if v else 'FAIL'}  retired route: {k}")
            ok &= v

        # 2) saved screenshots
        shots = [
            ("desktop", "1440,900", url),
            ("desktop_full", "1440,4000", url),
            ("mobile", "390,844", url),
            ("table", "1440,900", url + "#view/table"),
            ("models3d", "1440,900", url + "#view/models3d"),
        ]
        if slug:
            shots += [("detail", "1440,900", f"{url}#reef/{slug}"),
                      ("detail_ref", "1440,900", f"{url}#reef/{slug}/R1"),
                      ("detail_mobile", "390,844", f"{url}#reef/{slug}/R1")]
        shots += [("footprint_detail_S1", "1440,900", f"{url}#reef/borth-coastal-defence-reef/S1")]
        for name, size, u in shots:
            out = QA / f"{a.prefix}_{name}.png"
            if out.exists():
                out.unlink()
            run(exe, [f"--window-size={size}", f"--screenshot={out}"], u, prof)
            good = out.exists() and out.stat().st_size > 5000
            report.append(f"{'PASS' if good else 'FAIL'}  screenshot {out.name} ({out.stat().st_size if out.exists() else 0} B)")
            ok &= good
    report.append("RESULT: " + ("PASS" if ok else "FAIL"))
    report.append("note: headless shots use the OS colour scheme; dark-mode shots still need a manual check.")
    txt = "\n".join(report)
    (QA / f"{a.prefix}_file_smoke.txt").write_text(txt + "\n", encoding="utf-8")
    print(txt)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

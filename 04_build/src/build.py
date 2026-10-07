"""Build the single-file page 04_build/artificial_reefs.html.

Inlines src/styles.css, src/models3d.css/.js (3D models tab; runs src/compile_models3d.py first), src/scale.js (Scale view), src/app.js and data/reefs.json (plus a few display
fields derived here) into src/template.html. No new research: every derived
value below is re-shaped from text already present in the verified cards.

Run:  python "04_build/src/build.py"
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
BUILD = SRC.parent                      # 04_build/
DATA = BUILD / "data" / "reefs.json"
OUT = BUILD / "artificial_reefs.html"
COMPILED_ON = "2026-09-25"

# ---------------------------------------------------------------------------
# Approximate USD figure per reef, used ONLY for the summary total, the cost
# sort and the table's "cost (~US$)" column. Each entry is transcribed from the
# card's own `cost_usd_approx` text; `needle` must literally occur in that text
# (checked below) so a changed card cannot silently keep a stale number.
# low/high in US$; mid = (low+high)/2 is what gets summed.
# Most of these conversions are marked in the cards themselves as rough and
# unsourced -- the page says so next to the total.
# ---------------------------------------------------------------------------
USD = {
    "burkitts-reef-bargara":        dict(low=6_500,      high=7_500,      needle="6,500-7,500", basis="AUD $10,000 excavator hire, 1997"),
    "cables-reef-wa":               dict(low=1_300_000,  high=1_400_000,  needle="1.3-1.4", basis="AUD $2M study + design + build"),
    "narrowneck-gold-coast":        dict(low=1_500_000,  high=1_500_000,  needle="USD $1.5M", basis="original 1999 build only (AUD $2.3M); 2017-18 renewal not added"),
    "prattes-reef-el-segundo":      dict(low=850_000,    high=850_000,    needle="850000", basis="cumulative 2000-2008 figure incl. removal"),
    "mount-maunganui-reef":         dict(low=1_000_000,  high=1_000_000,  needle="1,000,000", basis="NZ$1.5M build"),
    "opunake-reef":                 dict(low=1_100_000,  high=1_100_000,  needle="US$1.1m", basis="~NZ$1.7M spent by 2009"),
    "boscombe-surf-reef":           dict(low=5_100_000,  high=5_100_000,  needle="US $5.1M", basis="GBP 3.2M reef structure"),
    "kovalam-reef-india":           dict(low=1_100_000,  high=1_100_000,  needle="1100000", basis="Rs 75M as built"),
    "borth-coastal-defence-reef":   dict(low=15_000_000, high=17_000_000, needle="US$15-17M", basis="GBP 12-13M completed reef/defence works; sources vary (GBP 7M-29M)"),
    "bunbury-airwave":              dict(low=350_000,    high=400_000,    needle="350,000", basis="total project, disputed between sources; council share A$75,000"),
    "palm-beach-gold-coast":        dict(low=12_500_000, high=12_500_000, needle="12.5 million", basis="AU$18.2M"),
    "southern-ocean-surf-reef-albany": dict(low=7_600_000, high=8_500_000, needle="7.6-8.5", basis="AUD $11.75M committed funds"),
}

# Where the compiler's cost_short would mislead on a tile (headline and USD
# refer to different scopes), show this wording instead -- taken from the card.
COST_TILE_OVERRIDE = {
    "borth-coastal-defence-reef": "GBP 12–13M completed works (~US$15–17M); figures vary by source",
    "bunbury-airwave": "~US$350–400K total project (disputed); council share A$75,000",
}

SOUTHERN = {"Australia", "New Zealand"}   # hemisphere sanity check for map pins
REF_RE = re.compile(r"\[(R\d+)\]")


def fmt_usd(v: float) -> str:
    if v >= 1_000_000:
        s = f"{v / 1_000_000:.2f}".rstrip("0").rstrip(".")
        return f"{s}M"
    if v >= 100_000:
        return f"{round(v / 1_000):,}K"
    return f"{v:,.0f}"


def usd_label(low: float, high: float) -> str:
    if low == high:
        return "~US$" + fmt_usd(low)
    a, b = fmt_usd(low), fmt_usd(high)
    unit = a[-1] if a[-1] == b[-1] and a[-1] in "MK" else ""
    if unit:
        return f"~US${a[:-1]}–{b[:-1]}{unit}"
    return f"~US${a}–{b}"


def refs_in(text) -> list[str]:
    if not isinstance(text, str):
        return []
    seen = []
    for m in REF_RE.findall(text):
        if m not in seen:
            seen.append(m)
    return seen


def main() -> int:
    reefs = json.loads(DATA.read_text(encoding="utf-8"))
    warnings: list[str] = []

    for r in reefs:
        slug = r["slug"]
        # --- USD ---
        spec = USD.get(slug)
        if spec:
            src = str(r.get("cost_usd_approx"))
            if spec["needle"] not in src:
                warnings.append(f"{slug}: USD needle {spec['needle']!r} not found in cost_usd_approx -> dropped from total")
                r["usd"] = None
            else:
                r["usd"] = {
                    "low": spec["low"], "high": spec["high"],
                    "mid": (spec["low"] + spec["high"]) / 2,
                    "label": usd_label(spec["low"], spec["high"]),
                    "basis": spec["basis"],
                    "source_text": src,
                }
        else:
            r["usd"] = None
        r["cost_tile"] = COST_TILE_OVERRIDE.get(slug, r.get("cost_short") or "cost not disclosed")
        r["hover_refs"] = {k: refs_in(r.get(k)) for k in ("size", "cost", "year", "type")}

        # --- map pin sanity ---
        lat, lon = r.get("lat"), r.get("lon")
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            r["map_ok"], r["map_note"] = False, "no coordinates in the card"
        elif not (-90 <= lat <= 90 and -180 <= lon <= 180):
            r["map_ok"], r["map_note"] = False, "card coordinates out of range"
        elif r.get("country") in SOUTHERN and lat > 0:
            r["map_ok"], r["map_note"] = False, (
                f"card coordinates ({lat}, {lon}) fail a hemisphere check "
                f"({r['country']} lies south of the equator) — not plotted")
        else:
            r["map_ok"], r["map_note"] = True, ""
        if not r["map_ok"]:
            warnings.append(f"{slug}: not on map — {r['map_note']}")

        # --- slim: drop fields the page never shows ---
        r["sections"] = [s for s in r.get("sections", []) if s.get("title") != "Quick facts"]
        for k in ("images_rejected", "blocked_sources", "videos_rejected"):
            r.pop(k, None)

    with_cost = [r for r in reefs if r.get("usd")]
    payload = {
        "meta": {
            "compiled_on": COMPILED_ON,
            "n_reefs": len(reefs),
            "n_with_cost": len(with_cost),
            "usd_total_low": sum(r["usd"]["low"] for r in with_cost),
            "usd_total_high": sum(r["usd"]["high"] for r in with_cost),
            "usd_total_mid": sum(r["usd"]["mid"] for r in with_cost),
        },
        "reefs": reefs,
    }
    # '<' -> < keeps "</script>" and "<!--" out of the inline JSON (valid JSON escape).
    data_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")

    # 3D models tab (round 9): discover models, copy viewers, vendor images, render docs -> data/models3d.json
    sys.path.insert(0, str(SRC))
    import compile_models3d  # noqa: PLC0415
    compile_models3d.main()
    data3d_json = (BUILD / "data" / "models3d.json").read_text(encoding="utf-8").replace("<", "\\u003c")
    m3d_css = (SRC / "models3d.css").read_text(encoding="utf-8")
    m3d_js = (SRC / "models3d.js").read_text(encoding="utf-8")

    css = (SRC / "styles.css").read_text(encoding="utf-8")
    js = (SRC / "app.js").read_text(encoding="utf-8")
    tpl = (SRC / "template.html").read_text(encoding="utf-8")
    for name, body, bad in (("styles.css", css, "</style"), ("app.js", js, "</script"),
                            ("models3d.css", m3d_css, "</style"), ("models3d.js", m3d_js, "</script")):
        if bad in body.lower():
            raise SystemExit(f"{name} contains {bad!r}; cannot inline safely")
    for marker in ("/*__CSS__*/", "/*__M3D_CSS__*/", "/*__M3D_JS__*/", "/*__JS__*/", "__DATA__", "__DATA3D__"):
        if tpl.count(marker) != 1:
            raise SystemExit(f"template marker {marker} must appear exactly once")

    html = (tpl.replace("/*__CSS__*/", css)
               .replace("/*__M3D_CSS__*/", m3d_css)
               .replace("/*__M3D_JS__*/", m3d_js)
               .replace("/*__JS__*/", js)
               .replace("__DATA3D__", data3d_json)     # before __DATA__: __DATA3D__ contains the string "__DATA"
               .replace("__DATA__", data_json))
    OUT.write_text(html, encoding="utf-8", newline="\n")

    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")
    print(f"reefs: {len(reefs)}; with USD cost: {len(with_cost)}; "
          f"total ~US${payload['meta']['usd_total_low']:,.0f}-{payload['meta']['usd_total_high']:,.0f}")
    for w in warnings:
        print("NOTE:", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())

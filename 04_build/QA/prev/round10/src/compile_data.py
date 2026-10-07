#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
compile_data.py — Section 1 (world artificial surf reefs) data compiler.

Reads the verified reef cards under 02_research/reefs/<slug>.json, adds a set
of derived/display fields (see 04_build/data/SCHEMA.md for the full field
list), copies every LOCAL image the cards reference (Lior's own figures and
video frame grabs) into 04_build/assets/<slug>/, and writes the compiled,
year-ordered array to 04_build/data/reefs.json.

It does NOT do any new research. Every fact it emits comes straight out of
the card JSON; this script only reshapes/derives, and it flags anything that
looks off (missing [R#], broken image path, etc.) in the "problems" list
that is printed at the end and returned by main().

Run:  python compile_data.py
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]          # .../Artificial reef
CARDS_DIR = ROOT / "02_research" / "reefs"
BUILD_DIR = ROOT / "04_build"
ASSETS_DIR = BUILD_DIR / "assets"
DATA_DIR = BUILD_DIR / "data"
OUT_JSON = DATA_DIR / "reefs.json"

SLUGS = [
    "narrowneck-gold-coast",
    "cables-reef-wa",
    "prattes-reef-el-segundo",
    "mount-maunganui-reef",
    "opunake-reef",
    "boscombe-surf-reef",
    "kovalam-reef-india",
    "borth-coastal-defence-reef",
    "palm-beach-gold-coast",
    "southern-ocean-surf-reef-albany",
    "burkitts-reef-bargara",
    "bunbury-airwave",
    "mexico-reef-2026-unnamed",
]

SECTION_SPECS = [
    # (title, card field(s) -> handled specially for quick_facts)
    ("Quick facts", None),
    ("Motivation & who pushed for it", "motivation"),
    ("Design as planned", "design_as_planned"),
    ("As built vs design", "as_built_vs_design"),
    ("Outcome", "outcome"),
    ("Why it worked / failed", "why_worked_or_failed"),
    ("Unexpected results", "unexpected_results"),
    ("What could have been done better", "could_be_better"),
    ("Relevance to Israel / Haifa", "relevance_to_israel"),
]

QUICK_FACT_FIELDS = [
    ("Name", "name"),
    ("Place", "place"),
    ("Country", "country"),
    ("Year", "year"),
    ("Type", "type"),
    ("Purpose", "purpose"),
    ("Size", "size"),
    ("Cost", "cost"),
    ("Cost (approx. USD)", "cost_usd_approx"),
    ("Financed by", "financed_by"),
    ("Designer", "designer"),
    ("Contractor", "contractor"),
    ("Status now", "status_now"),
    ("Verdict", "verdict"),
]

COUNTRY_FLAGS = {
    "Australia": "🇦🇺",
    "USA": "🇺🇸",
    "United States": "🇺🇸",
    "New Zealand": "🇳🇿",
    "United Kingdom": "🇬🇧",
    "UK": "🇬🇧",
    "India": "🇮🇳",
    "Mexico": "🇲🇽",
}

VERDICT_LABELS = {
    "worked": "Worked",
    "partly worked": "Partly worked",
    "mixed": "Mixed",
    "failed": "Failed",
    "n-a": "Too early to tell",
}

YEAR_CLAUSE_KEYWORDS = ("construction", "built", "build", "install")

REF_TAG_RE = re.compile(r"\[R\d+\]")
REF_GROUP_RE = re.compile(r"\[((?:R\d+)(?:\s*,\s*R\d+)+)\]")
REF_ID_RE = re.compile(r"R\d+")
YEAR_RE = re.compile(r"(?:19|20)\d{2}")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def normalize_refs(text):
    """Turn "[R3, R5]" into "[R3][R5]"; leave already-separate tags alone."""
    if not isinstance(text, str):
        return text

    def repl(m):
        parts = re.split(r"\s*,\s*", m.group(1))
        return "".join(f"[{p.strip()}]" for p in parts)

    return REF_GROUP_RE.sub(repl, text)


def deep_normalize_refs(obj):
    if isinstance(obj, str):
        return normalize_refs(obj)
    if isinstance(obj, list):
        return [deep_normalize_refs(x) for x in obj]
    if isinstance(obj, dict):
        return {k: deep_normalize_refs(v) for k, v in obj.items()}
    return obj


def truncate(text, limit, ellipsis="…"):
    if not isinstance(text, str):
        return text
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    # back off to the last space so we don't chop mid-word
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip(",;: ") + ellipsis


def compute_year(year_text):
    """Return (year_short, sort_year) from the free-text 'year' field."""
    if not isinstance(year_text, str) or not year_text.strip():
        return "date unclear", 9999

    clauses = [c.strip() for c in year_text.split(";") if c.strip()]
    if not clauses:
        clauses = [year_text]

    chosen = None
    for clause in clauses:
        low = clause.lower()
        if any(kw in low for kw in YEAR_CLAUSE_KEYWORDS):
            chosen = clause
            break
    if chosen is None:
        chosen = clauses[0]

    years = sorted({int(y) for y in YEAR_RE.findall(chosen)})
    if not years:
        # fall back to searching the whole field
        years = sorted({int(y) for y in YEAR_RE.findall(year_text)})
    if not years:
        return "date unclear", 9999

    lo, hi = years[0], years[-1]
    year_short = str(lo) if lo == hi else f"{lo}–{hi}"
    return year_short, lo


# Shared "amount" fragment: handles plain numbers, ranges ("3-3.2",
# "12-13") and a trailing scale word/letter ("million", "M", "K", ...).
_NUM = r"[\d][\d,\.]*(?:\s*[-–]\s*[\d][\d,\.]*)?\s*(?:million|billion|thousand|M|K)?"

# One combined regex so re.search naturally returns the LEFTMOST monetary
# mention in the text (usually the headline figure) instead of picking
# whichever currency happened to be listed first in our own pattern list.
_COST_RE = re.compile(
    r"(?:AUD|NZD|USD|GBP|INR|MXN)\s*\$?\s*" + _NUM +
    r"|AU\$\s*" + _NUM +
    r"|A\$\s*" + _NUM +
    r"|NZ\$\s*" + _NUM +
    r"|US\$\s*" + _NUM +
    r"|£\s*" + _NUM +
    r"|Rs\.?\s*" + _NUM +
    r"|₹\s*" + _NUM +
    r"|\$\s*" + _NUM,
    re.I,
)

# For the cost_usd_approx field we specifically want a USD figure, so the
# currency marker must be followed by an actual "$" (this avoids matching
# a bare FX-rate mention like "AUD~USD 0.65" that has no dollar sign).
_USD_RE = re.compile(r"(?:US\$|USD\s*\$)\s*" + _NUM, re.I)


def _first_match(pattern, text):
    m = pattern.search(text)
    return m.group(0).strip() if m else None


def _format_usd_number(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    if value >= 1_000_000:
        s = f"{value/1_000_000:.1f}".rstrip("0").rstrip(".")
        return f"US${s}M"
    if value >= 1_000:
        s = f"{value/1_000:.0f}"
        return f"US${s}K"
    return f"US${value:.0f}"


def compute_cost_short(cost_text, cost_usd_approx):
    base = None
    if isinstance(cost_text, str):
        base = _first_match(_COST_RE, cost_text)
    if base is None and isinstance(cost_text, str):
        base = truncate(cost_text, 40)
    if base is None:
        base = "cost not disclosed"

    usd_part = None
    if isinstance(cost_usd_approx, (int, float)):
        usd_part = _format_usd_number(cost_usd_approx)
    elif isinstance(cost_usd_approx, str) and cost_usd_approx.strip():
        usd_part = _first_match(_USD_RE, cost_usd_approx)

    if usd_part and usd_part.lower().replace(" ", "") not in base.lower().replace(" ", ""):
        return f"{base} (~{usd_part})"
    return base


_NEGATION_STRIP_RE = re.compile(r"\bnot\s+(rock|geotextile)\b", re.I)
_NO_STRIP_RE = re.compile(r"\bno\s+(rock|geotextile)\b", re.I)


def compute_type_short(type_text):
    if not isinstance(type_text, str) or not type_text.strip():
        return "type unclear"
    clean = _NEGATION_STRIP_RE.sub("", type_text)
    clean = _NO_STRIP_RE.sub("", clean)
    low = clean.lower()

    if "bladder" in low or "inflatable" in low or "airwave" in low:
        return "inflatable bladder"
    if "granite" in low:
        return "granite rock"
    if "basalt" in low:
        return "basalt boulder"
    if "riprap" in low:
        return "rock (riprap)"
    if "boulder" in low:
        return "boulder rock"
    if re.search(r"\brock\b", low):
        return "rock reef"
    if "geotextile" in low:
        return "geotextile sand containers"
    return truncate(type_text, 40)


def normalize_verdict(raw):
    if not isinstance(raw, str):
        return "n-a"
    low = raw.strip().lower()
    if "partly" in low or "partial" in low:
        return "partly worked"
    if "mixed" in low:
        return "mixed"
    if "fail" in low:
        return "failed"
    if "work" in low or "success" in low:
        return "worked"
    return "n-a"


def compute_place_short(place, country):
    if not isinstance(place, str) or not place.strip():
        return country or ""
    parts = [p.strip() for p in place.split(",") if p.strip()]
    if len(parts) >= 3:
        loc = parts[1]
    elif parts:
        loc = parts[0]
        if "/" in loc:
            loc = loc.split("/")[-1].strip()
    else:
        loc = place
    return f"{loc}, {country}" if country else loc


def first_two_sentences(text):
    if not isinstance(text, str) or not text.strip():
        return ""
    sentences = SENTENCE_SPLIT_RE.split(text.strip())
    return " ".join(sentences[:2]).strip()


def sentence_has_number_no_ref(sentence):
    return bool(re.search(r"\d", sentence)) and "[R" not in sentence


def collect_facts_without_ref(card, problems, slug):
    fields = [
        "purpose", "motivation", "design_as_planned", "as_built_vs_design",
        "outcome", "why_worked_or_failed", "unexpected_results",
        "could_be_better", "relevance_to_israel", "status_now",
    ]
    flagged = []
    for f in fields:
        text = card.get(f)
        if not isinstance(text, str):
            continue
        for sent in SENTENCE_SPLIT_RE.split(text):
            sent = sent.strip()
            if sent and sentence_has_number_no_ref(sent):
                flagged.append(f"{f}: {truncate(sent, 90)}")
    for item in flagged:
        problems.append(f"[{slug}] fact with a number but no [R#] in {item}")
    return len(flagged)


def collect_ref_ids_used(card):
    used = set()
    fields = [
        "year", "type", "purpose", "size", "cost", "cost_usd_approx",
        "financed_by", "motivation", "designer", "contractor", "status_now",
        "hover_text", "design_as_planned", "as_built_vs_design", "outcome",
        "why_worked_or_failed", "unexpected_results", "could_be_better",
        "relevance_to_israel",
    ]
    for f in fields:
        v = card.get(f)
        if isinstance(v, str):
            used.update(REF_ID_RE.findall(v))
    for rev in card.get("reviews") or []:
        q = rev.get("quote_or_summary", "") if isinstance(rev, dict) else ""
        used.update(REF_ID_RE.findall(q))
    return used


def build_quick_facts_html(card):
    rows = []
    for label, field in QUICK_FACT_FIELDS:
        val = card.get(field)
        if val is None or val == "":
            continue
        if not isinstance(val, str):
            val = str(val)
        rows.append(f"<tr><th>{label}</th><td>{normalize_refs(val)}</td></tr>")
    return "<table class=\"quick-facts\">\n" + "\n".join(rows) + "\n</table>"


def build_sections(card):
    sections = []
    for title, field in SECTION_SPECS:
        if field is None:
            sections.append({"title": title, "html_or_text": build_quick_facts_html(card)})
            continue
        text = card.get(field) or ""
        sections.append({"title": title, "html_or_text": normalize_refs(text)})
    return sections


def copy_local_asset(rel_path, slug, problems):
    """Copy a project-root-relative local file into assets/<slug>/ and
    return the new path (relative to 04_build), or None if missing."""
    if not rel_path:
        return None
    src = ROOT / rel_path
    if not src.is_file():
        problems.append(f"[{slug}] missing local asset (skipped): {rel_path}")
        return None
    dest_dir = ASSETS_DIR / slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.copyfile(src, dest)
    return f"assets/{slug}/{src.name}"


# ---------------------------------------------------------------------------
# Media rules (2026-09-25 media re-check, see 05_qa/media_recheck_changes.md)
#   images[].shows : "structure visible" | "reef effect visible" | "site context only"
#   videos[].about : "about the reef" | "mentions the reef briefly" | "site only — not about the reef"
#   frames[].shows : same vocabulary as images (sometimes with underscores)
# ---------------------------------------------------------------------------
SHOWS_RANK = {"structure visible": 0, "reef effect visible": 1, "site context only": 2}
SHOWS_LABEL = {
    "structure visible": "shows the structure",
    "reef effect visible": "shows the reef's effect",
    "site context only": "site context only",
}
SITE_ONLY_ABOUT = "site only"


def norm_shows(v):
    """'structure_visible' / 'Structure visible' -> 'structure visible'."""
    if not isinstance(v, str):
        return None
    v = v.strip().lower().replace("_", " ")
    if v.startswith("structure"):
        return "structure visible"
    if v.startswith("reef effect"):
        return "reef effect visible"
    if v.startswith("site context"):
        return "site context only"
    return None


def is_site_only(vid):
    return isinstance(vid.get("about"), str) and vid["about"].strip().lower().startswith(SITE_ONLY_ABOUT)


def label_images(images):
    out = []
    for im in images:
        im = dict(im)
        s = norm_shows(im.get("shows"))
        if s:
            im["shows_label"] = SHOWS_LABEL[s]
            im["shows_key"] = s.replace(" ", "-")
        out.append(im)
    return out


def compute_hero_image(card, slug, problems):
    """Hero = best hotlinkable image by what it shows: structure visible, then reef effect
    visible, then site context only, then unlabelled. Within a tier: the media re-check's
    hero_recommendation first, then a photo/aerial with a permissive licence, then card order.
    Falls back to the thumbnail of a video that is about the reef (never a site-only video)."""
    permissive_re = re.compile(r"cc\b|creative commons|public domain|government|\.gov", re.I)
    images = card.get("images") or []
    rec = card.get("hero_recommendation")
    rec = _norm_url(rec.get("url") if isinstance(rec, dict) else rec if isinstance(rec, str) and rec.startswith("http") else "")

    cands = [im for im in images if im.get("hotlink_ok") is True and re.match(r"https?://", im.get("url") or "")]

    def rank(pair):
        i, im = pair
        s = norm_shows(im.get("shows"))
        return (
            SHOWS_RANK.get(s, 3),
            0 if rec and _norm_url(im.get("url")) == rec else 1,
            0 if (im.get("kind") in ("photo", "aerial") and permissive_re.search(im.get("license", "") or "")) else 1,
            i,
        )

    im = min(enumerate(cands), key=rank)[1] if cands else None

    if im:
        s = norm_shows(im.get("shows"))
        return {
            "url": im.get("url"),
            "credit": im.get("credit"),
            "license": im.get("license"),
            "source_page": im.get("source_page"),
            "depicts": im.get("depicts"),
            "shows_label": SHOWS_LABEL.get(s),
        }

    for vid in sorted(card.get("videos") or [], key=lambda v: 0 if (v.get("about") or "").startswith("about the reef") else 1):
        vidid = vid.get("video_id")
        if not vidid or is_site_only(vid):
            continue
        depicts = vid.get("title") or first_two_sentences(vid.get("what_it_shows", ""))
        return {
            "url": f"https://img.youtube.com/vi/{vidid}/hqdefault.jpg",
            "credit": f"YouTube — {vid.get('channel', 'unknown channel')}",
            "license": "YouTube video thumbnail",
            "source_page": vid.get("url"),
            "depicts": depicts,
        }

    problems.append(f"[{slug}] no usable hero image found (no hotlink_ok image or video)")
    return None


def process_videos(card, slug, problems):
    videos = []
    for vid in card.get("videos") or []:
        v = dict(vid)
        if isinstance(v.get("about"), str):
            v["about_label"] = v["about"].strip()
        if is_site_only(vid):
            # site-only video: shown as a plain link with its label; no embed, thumbnail or frames
            v["link_only"] = True
            v["frames"] = []
            videos.append(v)
            continue
        frames = []
        for fr in vid.get("frames") or []:
            fr = dict(fr)
            s = norm_shows(fr.get("shows"))
            if s:
                fr["shows_label"] = SHOWS_LABEL[s]
                fr["shows_key"] = s.replace(" ", "-")
            new_path = copy_local_asset(fr.get("path"), slug, problems)
            if new_path:
                fr["path"] = new_path
                frames.append(fr)
        v["frames"] = frames
        videos.append(v)
    return videos


def process_lior_images(card, slug, problems):
    out = []
    for li in card.get("lior_images") or []:
        li = dict(li)
        new_path = copy_local_asset(li.get("path"), slug, problems)
        if new_path:
            li["path"] = new_path
            out.append(li)
        # missing files already logged by copy_local_asset
    return out


REVIEW_FIELDS = ("who", "role", "quote_or_summary", "outlet", "date", "url", "stance", "origin")
REFERENCE_FIELDS = ("id", "citation", "url", "accessed", "supports", "origin")
# Card fields that hold rejected / internal-only material and must never reach the page.
DROP_FIELDS = ("videos_rejected", "images_rejected", "blocked_sources")


def _norm_url(u):
    u = (u or "").strip().lower()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    return u.rstrip("/")


def process_references(card, slug, problems):
    """Copy references, keeping provenance ('origin') when present."""
    out = []
    for ref in card.get("references") or []:
        if not isinstance(ref, dict):
            continue
        r = {k: ref[k] for k in REFERENCE_FIELDS if k in ref and ref[k] not in (None, "")}
        r.setdefault("url", "")
        if not r.get("id"):
            problems.append(f"[{slug}] reference without id skipped: {truncate(str(ref), 80)}")
            continue
        out.append(r)
    return out


def process_reviews(card, references, slug, problems):
    """Copy reviews, keeping 'stance' and 'origin', and derive 'ref_id': the
    reference whose URL is the review's own URL (so the page can open that
    reference's pop-up from the review). No match -> no ref_id (the review's
    own URL is still shown)."""
    by_url = {}
    for ref in references:
        if ref.get("url"):
            by_url.setdefault(_norm_url(ref["url"]), ref["id"])
    out = []
    for rev in card.get("reviews") or []:
        if not isinstance(rev, dict):
            continue
        r = {k: rev[k] for k in REVIEW_FIELDS if k in rev and rev[k] not in (None, "")}
        rid = by_url.get(_norm_url(rev.get("url")))
        if rid:
            r["ref_id"] = rid
        elif rev.get("url"):
            problems.append(f"[{slug}] review by {rev.get('who')!r}: URL matches no reference (shown as a plain link)")
        out.append(r)
    return out


# ---------------------------------------------------------------------------
# Scale tab: verified footprints (07_scale/reefs/<slug>.footprint.json)
# ---------------------------------------------------------------------------
FOOTPRINT_DIR = ROOT / "07_scale" / "reefs"
DOCS_SCALE_DIR = BUILD_DIR / "docs" / "scale"
FP_REF_RE = re.compile(r"\b([RS]\d{1,3})\b")
FP_ORIGIN = "added by the Scale-tab footprint check, 2026-09-25"
FOOTPRINT_FIELDS = (
    "name", "status", "verified_on", "shape_type", "shape_type_notes", "coords",
    "polygon_notes", "polygon_components_notes", "bbox_m", "bbox_alt_note", "area_m2", "area_m2_notes",
    "max_dimension_m", "crest_depth_m", "crest_depth_alt_note", "distance_offshore_m", "orientation_notes",
    "volume_m3", "materials", "derivation", "images_relied_on", "gemini_comparison", "confidence",
    "open_issues", "references", "verification",
)

# Short display labels for crest depth and distance offshore. Each is transcribed from the
# footprint's own value + datum / measured_from text; (value, needle) must match the footprint
# (checked below) so an edited footprint cannot silently keep a stale label.
CREST_SHORT = {
    "borth-coastal-defence-reef": (None, "not established", "not established (no source)"),
    "boscombe-surf-reef": (0.5, "ABOVE Lowest Astronomical Tide", "+0.5 m, i.e. above LAT (designed crest)"),
    "bunbury-airwave": (1.0, "below the water surface at low tide", "1.0 m below low tide (≈ LAT)"),
    "burkitts-reef-bargara": (0, "exposed dry basalt at low tide", "0 m: rock exposed at low tide"),
    "cables-reef-wa": (1.5, "below the water surface on average tides", "1.5 m below water (average tide)"),
    "kovalam-reef-india": (None, "not found", "not found in any source"),
    "mexico-reef-2026-unnamed": (1.5, "analogy value", "1.5 m below MSL (analogy estimate)"),
    "mount-maunganui-reef": (0.9, "below Chart Datum", "0.9 m below Chart Datum (≈ LAT)"),
    "narrowneck-gold-coast": (1.5, "below low tide waterline", "1.5 m below low tide (≈ LAT), 2012 value"),
    "opunake-reef": (1.5, "no datum stated", "1.5 m, datum not stated"),
    "palm-beach-gold-coast": (1.5, "below mean sea level", "1.5 m below MSL"),
    "prattes-reef-el-segundo": (1.83, "below MSL (design minimum", "1.83 m below MSL (design minimum)"),
    "southern-ocean-surf-reef-albany": (1.0, "below AHD", "1.0 m below AHD (≈ MSL)"),
}
DIST_SHORT = {
    "borth-coastal-defence-reef": (350, "shoreline (approximate", "≈350 m (midpoint of two conflicting figures)"),
    "boscombe-surf-reef": (220, "seawall base", "220 m from the seawall base"),
    "bunbury-airwave": (37.5, "design target range 30-45 m", "37.5 m (design range 30–45 m)"),
    "burkitts-reef-bargara": (0, "shoreline", "0 m (at the shoreline)"),
    "cables-reef-wa": (275, "shoreline (approximate", "≈275 m"),
    "kovalam-reef-india": (55, "schematic y=0 baseline", "≈55 m (schematic, not published)"),
    "mexico-reef-2026-unnamed": (270, "analogy value", "≈270 m (analogy estimate)"),
    "mount-maunganui-reef": (250, "Tay St / Marine Parade", "250 m"),
    "narrowneck-gold-coast": (200, "shoreward/inner edge", "200 m (to the inner edge)"),
    "opunake-reef": (150, "estimated centroid distance", "≈150 m (estimated, to centroid)"),
    "palm-beach-gold-coast": (270, "19th Avenue", "270 m (we placed the centroid there)"),
    "prattes-reef-el-segundo": (95, "100 yards", "≈95 m (“~100 yards”)"),
    "southern-ocean-surf-reef-albany": (140, "landward toe", "140 m (to the landward toe)"),
}


def ring_area_signed(ring):
    a = 0.0
    for i in range(len(ring) - 1):
        a += ring[i][0] * ring[i + 1][1] - ring[i + 1][0] * ring[i][1]
    return a / 2.0


def geometry_of(polys):
    """Area (shoelace), axis-aligned bbox and area-weighted centroid of closed rings (metres).
    Each ring is a separate outline (e.g. Narrowneck's two arms, drawn with opposite winding),
    so ring areas are summed as absolute values."""
    area, cx, cy = 0.0, 0.0, 0.0
    for ring in polys:
        a = ring_area_signed(ring)
        sx = sy = 0.0
        for i in range(len(ring) - 1):
            x0, y0 = ring[i]
            x1, y1 = ring[i + 1]
            c = x0 * y1 - x1 * y0
            sx += (x0 + x1) * c
            sy += (y0 + y1) * c
        if a:  # separate rings (not holes): weight each ring's own centroid by its |area|
            cx += (sx / 6.0 / a) * abs(a)
            cy += (sy / 6.0 / a) * abs(a)
        area += abs(a)
    xs = [p[0] for ring in polys for p in ring]
    ys = [p[1] for ring in polys for p in ring]
    cen = [cx / area, cy / area] if area else [sum(xs) / len(xs), sum(ys) / len(ys)]
    return {
        "area": abs(area),
        "bbox": {"minx": min(xs), "maxx": max(xs), "miny": min(ys), "maxy": max(ys)},
        "centroid": [round(cen[0], 2), round(cen[1], 2)],
    }


def _walk_strings(obj, fn):
    if isinstance(obj, str):
        return fn(obj)
    if isinstance(obj, list):
        return [_walk_strings(x, fn) for x in obj]
    if isinstance(obj, dict):
        return {k: _walk_strings(v, fn) for k, v in obj.items()}
    return obj


def confidence_level(text):
    m = re.search(r"\b(high|medium|low)\b", str(text or "").lower())
    return m.group(1) if m else "unknown"


def load_footprint(slug, card, problems):
    """Footprint record for the Scale tab, plus the footprint references to merge.
    Returns (footprint_dict or None, footprint_refs)."""
    path = FOOTPRINT_DIR / f"{slug}.footprint.json"
    if not path.is_file():
        problems.append(f"[{slug}] no footprint file at {path}")
        return None, []
    raw = json.loads(path.read_text(encoding="utf-8"))

    # --- nothing from *_rejected may reach the page: scrub rejected media URLs from the footprint text
    rej_urls = set()
    for k in ("images_rejected", "videos_rejected"):
        for x in card.get(k) or []:
            if isinstance(x, dict) and x.get("url"):
                rej_urls.add(x["url"])
                rej_urls.add(x["url"].split("?")[0])
    rej_norm = {_norm_url(u) for u in rej_urls}
    WITHHELD = "[rejected image — not shown]"

    def scrub(s):
        for u in sorted(rej_urls, key=len, reverse=True):
            if u and u in s:
                s = s.replace(u, WITHHELD)
        return s

    fp = {k: raw[k] for k in FOOTPRINT_FIELDS if k in raw}
    fp = deep_normalize_refs(_walk_strings(fp, scrub))

    polys = raw.get("polygons_m") or ([raw["polygon_m"]] if raw.get("polygon_m") else [])
    fp["polygons"] = polys
    if not polys:
        problems.append(f"[{slug}] footprint has no polygon")
        return None, []
    geo = geometry_of(polys)
    fp["geom"] = geo
    fp["closed"] = all(len(r) >= 4 and r[0] == r[-1] for r in polys)
    fp["area_computed_m2"] = round(geo["area"], 1)
    a = raw.get("area_m2")
    if isinstance(a, (int, float)) and a > 0 and abs(geo["area"] - a) / a > 0.15:
        problems.append(f"[{slug}] polygon area {geo['area']:.0f} m2 differs >15% from area_m2 {a}")

    shape = str(raw.get("shape_type") or "")
    fp["shape_short"] = shape if len(shape) <= 40 else shape.split("(")[0].strip()
    fp["confidence_level"] = confidence_level(raw.get("confidence"))

    crest = raw.get("crest_depth_m") or {}
    spec = CREST_SHORT.get(slug)
    if spec and spec[0] == crest.get("value") and spec[1] in str(crest.get("datum") or ""):
        fp["crest_label"] = spec[2]
    else:
        v = crest.get("value")
        fp["crest_label"] = (f"{v} m (see datum)" if v is not None else "not established")
        problems.append(f"[{slug}] crest label needle/value mismatch -> generic label used")
    dist = raw.get("distance_offshore_m") or {}
    spec = DIST_SHORT.get(slug)
    if spec and spec[0] == dist.get("value") and spec[1] in str(dist.get("measured_from") or ""):
        fp["distance_label"] = spec[2]
    else:
        v = dist.get("value")
        fp["distance_label"] = f"{v} m" if v is not None else "not established"
        problems.append(f"[{slug}] distance label needle/value mismatch -> generic label used")

    # --- images/figures relied on: mark accepted (thumbnail allowed) / rejected (withheld)
    accepted = {_norm_url(im.get("url")): im for im in (card.get("images") or []) if im.get("url")}
    relied = []
    for im in raw.get("images_relied_on") or []:
        im = dict(im)
        u = _norm_url(im.get("url"))
        if u and (u in rej_norm or _norm_url((im.get("url") or "").split("?")[0]) in rej_norm):
            relied.append({
                "withheld": True,
                "what_it_is": "An image that the 2026-09-25 media re-check REJECTED for this reef; it is not shown or linked on this page (see the provenance file).",
                "what_was_read_off_it": scrub(im.get("what_was_read_off_it") or ""),
            })
            continue
        acc = accepted.get(u)
        im = _walk_strings(im, scrub)
        im["accepted"] = bool(acc)
        im["thumb_ok"] = bool(acc and acc.get("hotlink_ok") is True)
        relied.append(im)
    fp["images_relied_on"] = deep_normalize_refs(relied)

    gc = fp.get("gemini_comparison") or {}
    fp["gemini_n_disagree"] = len(gc.get("disagree") or [])
    fp["gemini_n_agree"] = len(gc.get("agree") or [])

    # --- provenance md: copied next to the page so the package stays self-contained
    md = FOOTPRINT_DIR / f"{slug}.md"
    if md.is_file():
        DOCS_SCALE_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(md, DOCS_SCALE_DIR / md.name)
        fp["provenance_md"] = f"docs/scale/{md.name}"
        fp["provenance_src"] = f"07_scale/reefs/{md.name}"
    else:
        problems.append(f"[{slug}] provenance md missing: {md}")

    # --- footprint references (merged into the reef's list by the caller)
    fp_refs = []
    for ref in raw.get("references") or []:
        if not isinstance(ref, dict) or not ref.get("id"):
            continue
        r = {k: ref[k] for k in ("id", "citation", "url", "accessed", "supports") if ref.get(k) not in (None, "")}
        if ref.get("pdf_url"):
            r["pdf_url"] = ref["pdf_url"]
        u = r.get("url", "")
        if u and not re.match(r"https?://", u):
            # e.g. file:///...Gemini... : a local file on Lior's machine, not a public source
            r["local_file"] = u
            r["url"] = ""
        r.setdefault("url", "")
        fp_refs.append(deep_normalize_refs(_walk_strings(r, scrub)))
    fp.pop("references", None)

    # every id the footprint text mentions (for the pop-up target check)
    blob = json.dumps({k: fp.get(k) for k in ("derivation", "crest_depth_m", "distance_offshore_m", "volume_m3")}, ensure_ascii=False)
    fp["ref_ids_in_derivation"] = sorted(set(FP_REF_RE.findall(blob)), key=lambda x: (x[0], int(x[1:])))
    return fp, fp_refs


def merge_footprint_refs(slug, references, fp_refs, problems):
    """Card refs keep priority. A footprint ref with a new id (S# or unseen R#) is appended and
    tagged; one with the same id and URL is already covered; same id but another URL is kept on the
    card's entry as 'also_url' (e.g. a syndicated copy of the same article) and reported."""
    by_id = {r["id"]: r for r in references}
    for fr in fp_refs:
        cur = by_id.get(fr["id"])
        if cur is None:
            nr = dict(fr)
            nr["origin"] = FP_ORIGIN
            references.append(nr)
            by_id[nr["id"]] = nr
        elif fr.get("url") and _norm_url(fr["url"]) != _norm_url(cur.get("url")):
            cur["also_url"] = fr["url"]
            cur["also_note"] = "The Scale-tab footprint check read this source at a second URL: " + fr.get("citation", "")
            problems.append(f"[{slug}] footprint {fr['id']} URL differs from card {fr['id']} (kept card entry, footprint URL stored as also_url): {fr['url']}")
    return references


# ---------------------------------------------------------------------------
# Main compile
# ---------------------------------------------------------------------------

def compile_card(slug, problems):
    path = CARDS_DIR / f"{slug}.json"
    if not path.is_file():
        problems.append(f"[{slug}] card JSON not found at {path}")
        return None
    card = json.loads(path.read_text(encoding="utf-8"))
    card = deep_normalize_refs(card)

    year_short, sort_year = compute_year(card.get("year"))
    cost_short = compute_cost_short(card.get("cost"), card.get("cost_usd_approx"))
    size_short = truncate(card.get("size") or "", 60)
    type_short = compute_type_short(card.get("type"))
    verdict = normalize_verdict(card.get("verdict"))
    verdict_label = VERDICT_LABELS[verdict]
    country = card.get("country") or ""
    country_flag = COUNTRY_FLAGS.get(country, "")
    place_short = compute_place_short(card.get("place"), country)

    hero_image = compute_hero_image(card, slug, problems)

    hover_text = first_two_sentences(card.get("hover_text") or "")
    hover = {
        "size": size_short,
        "cost": cost_short,
        "year": year_short,
        "outcome": normalize_refs(hover_text),
    }

    sections = build_sections(card)

    videos = process_videos(card, slug, problems)
    lior_images = process_lior_images(card, slug, problems)

    # references / reviews: copied with provenance (origin, stance) kept; images straight through
    references = process_references(card, slug, problems)
    reviews = process_reviews(card, references, slug, problems)
    images = label_images(card.get("images") or [])

    # Scale tab: verified footprint + its references (S# ids kept distinct from the card's R#)
    footprint, fp_refs = load_footprint(slug, card, problems)
    references = merge_footprint_refs(slug, references, fp_refs, problems)
    if footprint:
        known = {r["id"] for r in references}
        for rid in footprint["ref_ids_in_derivation"]:
            if rid not in known:
                problems.append(f"[{slug}] footprint derivation cites {rid} but no such reference exists")

    # verify every [R#] used exists in references
    ref_ids_defined = {r.get("id") for r in references if isinstance(r, dict)}
    ref_ids_used = collect_ref_ids_used(card)
    for section in sections:
        ref_ids_used.update(REF_ID_RE.findall(section["html_or_text"] or ""))
    missing_refs = sorted(ref_ids_used - ref_ids_defined, key=lambda x: int(x[1:]) if x[1:].isdigit() else 0)
    for mref in missing_refs:
        problems.append(f"[{slug}] [{mref}] used in text but not present in references")

    facts_without_ref = collect_facts_without_ref(card, problems, slug)

    out = dict(card)  # keep all original fields except rejected/internal material
    for k in DROP_FIELDS:
        out.pop(k, None)
    out.update({
        "year_short": year_short,
        "sort_year": sort_year,
        "cost_short": cost_short,
        "size_short": size_short,
        "type_short": type_short,
        "verdict": verdict,
        "verdict_label": verdict_label,
        "country_flag": country_flag,
        "place_short": place_short,
        "hero_image": hero_image,
        "hover": hover,
        "sections": sections,
        "reviews": reviews,
        "images": images,
        "videos": videos,
        "lior_images": lior_images,
        "references": references,
        "facts_without_ref": facts_without_ref,
        "footprint": footprint,
    })
    out.pop("hero_recommendation", None)

    # A reference whose URL is a REJECTED video (e.g. Burkitts: Lior found the clips do not show
    # the artificial reef) is dropped from the page when nothing that is still shown cites it,
    # so the rejected video cannot resurface through the reference list / pop-ups.
    # The card itself is left untouched.
    rejected_urls = {_norm_url(v.get("url")) for v in (card.get("videos_rejected") or []) if isinstance(v, dict) and v.get("url")}
    if rejected_urls:
        shown = json.dumps({k: v for k, v in out.items() if k != "references"}, ensure_ascii=False)
        still_cited = set(REF_ID_RE.findall(" ".join(REF_TAG_RE.findall(shown))))
        still_cited.update(rv.get("ref_id") for rv in out["reviews"] if rv.get("ref_id"))
        kept = []
        for ref in out["references"]:
            if _norm_url(ref.get("url")) in rejected_urls and ref["id"] not in still_cited:
                problems.append(f"[{slug}] {ref['id']} not shown: it only points to a rejected video ({ref.get('url')})")
                continue
            kept.append(ref)
        out["references"] = kept
    return out


def main():
    problems = []
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    compiled = []
    for slug in SLUGS:
        card = compile_card(slug, problems)
        if card is not None:
            compiled.append(card)

    compiled.sort(key=lambda c: (c.get("sort_year", 9999), c.get("name", "")))

    # Local assets no longer referenced (e.g. frames of a video now shown as a link only because
    # the media re-check found it is not about the reef) are moved out of assets/ into
    # QA/removed_assets/<slug>/ so the page package holds only what it shows.
    blob = json.dumps(compiled, ensure_ascii=False)
    removed_dir = BUILD_DIR / "QA" / "removed_assets"
    for f in sorted(ASSETS_DIR.rglob("*")):
        if f.is_file():
            rel = str(f.relative_to(BUILD_DIR)).replace("\\", "/")
            if rel not in blob:
                dest = removed_dir / f.parent.name / f.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(f), str(dest))
                problems.append(f"moved unreferenced asset {rel} -> QA/removed_assets/{f.parent.name}/{f.name}")

    OUT_JSON.write_text(
        json.dumps(compiled, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Wrote {len(compiled)} cards to {OUT_JSON}")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print(" -", p)
    else:
        print("No problems flagged.")

    return compiled, problems


if __name__ == "__main__":
    main()

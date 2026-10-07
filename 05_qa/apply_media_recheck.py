#!/usr/bin/env python3
"""
apply_media_recheck.py

Reads every 05_qa/reef/<slug>_media_recheck.json and applies its verdicts to
02_research/reefs/<slug>.json, reversibly (rejected items are moved to
*_rejected arrays / a rejected\\ subfolder, never deleted).

The 13 recheck files were written by different sub-agents and use slightly
different field names for the same concepts (e.g. "shows" vs "classification",
"what_i_saw" vs "evidence" vs "reasoning"). This script normalizes across
those variants (see normalize_verdict / pick_text below) rather than assuming
one fixed schema.

Rules (per the 2026-09-25 task spec):

Images:
  - unrelated_or_wrong_site / could_not_load
        -> move the image object from images[] to images_rejected[],
           reason = 'media re-check 2026-09-25: <verdict> - <evidence text>'
  - site_context_only (aka "site_only")
        -> keep in images[], set images[i]["shows"] = "site context only"
  - structure_visible / reef_effect_visible
        -> keep, set images[i]["shows"] = "structure visible" / "reef effect visible"
  - if the current hero_image is not structure/effect and the recheck
    recommends a different accepted image -> add card["hero_recommendation"]

Videos:
  - unrelated -> move from videos[] to videos_rejected[], with reason
  - site_only -> keep, embed_ok=False, about="site only - not about the reef"
  - mentions_reef_briefly -> keep, about="mentions the reef briefly" + best_timestamp_seconds
  - about_the_reef -> keep, about="about the reef"

Frames (only relevant if the card happens to carry a "frames" list; today none
do, so the card-JSON side is a no-op, but the file-move always runs):
  - unrelated_or_wrong_site -> physically move the frame file to
    03_images/video_frames/<slug>/rejected/ (no-op if already there) and drop
    it from card["frames"] if such a list exists
  - otherwise -> set/keep a "shows" annotation on the matching card["frames"]
    entry if present

Every change is appended to 05_qa/media_recheck_changes.md
(table: reef | item | action | reason). Every card JSON is re-parsed after
writing to confirm it is still valid.
"""

import json
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git")
QA_REEF_DIR = ROOT / "05_qa" / "reef"
CARDS_DIR = ROOT / "02_research" / "reefs"
CHANGELOG = ROOT / "05_qa" / "media_recheck_changes.md"
RECHECK_DATE = "2026-09-25"

# Canonical verdict buckets, normalizing the various sub-agents' spellings.
REJECT_VERDICTS = {"unrelated_or_wrong_site", "could_not_load"}
IMAGE_SHOWS_LABEL = {
    "structure_visible": "structure visible",
    "reef_effect_visible": "reef effect visible",
    "site_context_only": "site context only",
    "site_only": "site context only",  # a couple of files used video-style wording for images/frames
}
VIDEO_UNRELATED = {"unrelated"}
VIDEO_SITE_ONLY = {"site_only"}
VIDEO_BRIEF = {"mentions_reef_briefly"}
VIDEO_FULL = {"about_the_reef"}

TEXT_FIELDS_PRIORITY = [
    "what_i_saw", "evidence", "actual_content_viewed", "reasoning",
    "notes", "note", "classification_detail", "card_depicts", "rationale",
]


def pick_text(obj: dict) -> str:
    for key in TEXT_FIELDS_PRIORITY:
        if obj.get(key):
            return str(obj[key])
    return ""


def verdict_of(obj: dict, *keys: str) -> str:
    """Return the first present value among the given keys (e.g. 'classification',
    'shows', 'about'), whichever field this particular recheck file used."""
    for k in keys:
        v = obj.get(k)
        if v:
            return v
    return ""


def hero_url_of(recheck: dict):
    hr = recheck.get("hero_recommendation")
    if isinstance(hr, dict):
        return hr.get("url"), hr
    if isinstance(hr, str):
        return hr, hr
    return None, None


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(path, "r", encoding="utf-8") as f:
        json.load(f)  # validate roundtrip


def is_structure_or_effect(img) -> bool:
    return img.get("shows") in ("structure visible", "reef effect visible")


def apply_images(card, recheck, slug, log_rows, counts):
    images = card.get("images", [])
    rejected = card.setdefault("images_rejected", [])
    kept_images = []

    by_url = {i.get("url"): i for i in recheck.get("images", []) if i.get("url")}

    for img in images:
        url = img.get("url")
        verdict_obj = by_url.get(url)
        if verdict_obj is None:
            kept_images.append(img)
            continue

        verdict = verdict_of(verdict_obj, "classification", "shows", "action")
        text = pick_text(verdict_obj)

        if verdict in REJECT_VERDICTS or verdict.lower().startswith("reject"):
            reason = f"media re-check {RECHECK_DATE}: {verdict} \u2014 {text}"
            img["reason"] = reason
            rejected.append(img)
            log_rows.append((slug, f"image: {url}", "moved to images_rejected", reason))
            counts["images_rejected"] += 1
        elif verdict in IMAGE_SHOWS_LABEL:
            img["shows"] = IMAGE_SHOWS_LABEL[verdict]
            kept_images.append(img)
            log_rows.append((slug, f"image: {url}", f"kept, shows={img['shows']}", text))
            counts["images_annotated"] += 1
        else:
            kept_images.append(img)
            log_rows.append((slug, f"image: {url}", "no change (unrecognized verdict)", verdict or "(none)"))

    card["images"] = kept_images
    card["images_rejected"] = rejected

    hero_url, hero_raw = hero_url_of(recheck)
    if hero_url:
        current_hero_url = card.get("hero_image") or card.get("hero")
        current_hero_img = next((i for i in kept_images if i.get("url") == current_hero_url), None)
        hero_is_good = current_hero_img is not None and is_structure_or_effect(current_hero_img)
        if not hero_is_good:
            card["hero_recommendation"] = hero_raw
            log_rows.append((slug, "hero_recommendation", "set", hero_url))
            counts["hero_recommendations"] += 1


def apply_videos(card, recheck, slug, log_rows, counts):
    videos = card.get("videos", [])
    rejected = card.setdefault("videos_rejected", [])
    kept_videos = []

    by_key = {}
    for v in recheck.get("videos", []):
        for key in (v.get("url"), v.get("video_id")):
            if key:
                by_key[key] = v

    for vid in videos:
        verdict_obj = by_key.get(vid.get("url")) or by_key.get(vid.get("video_id"))
        if verdict_obj is None:
            kept_videos.append(vid)
            continue

        verdict = verdict_of(verdict_obj, "classification", "about")
        text = pick_text(verdict_obj)
        key_label = vid.get("url") or vid.get("video_id")

        if verdict in VIDEO_UNRELATED:
            reason = f"media re-check {RECHECK_DATE}: unrelated \u2014 {text}"
            vid["reason"] = reason
            rejected.append(vid)
            log_rows.append((slug, f"video: {key_label}", "moved to videos_rejected", reason))
            counts["videos_rejected"] += 1
        elif verdict in VIDEO_SITE_ONLY:
            vid["embed_ok"] = False
            vid["about"] = "site only \u2014 not about the reef"
            kept_videos.append(vid)
            log_rows.append((slug, f"video: {key_label}", "kept, embed_ok=False", text))
            counts["videos_annotated"] += 1
        elif verdict in VIDEO_BRIEF:
            vid["about"] = "mentions the reef briefly"
            if "best_timestamp_seconds" in verdict_obj:
                vid["best_timestamp_seconds"] = verdict_obj["best_timestamp_seconds"]
            kept_videos.append(vid)
            log_rows.append((slug, f"video: {key_label}", "kept, mentions_reef_briefly", text))
            counts["videos_annotated"] += 1
        elif verdict in VIDEO_FULL:
            vid["about"] = "about the reef"
            if "best_timestamp_seconds" in verdict_obj:
                vid["best_timestamp_seconds"] = verdict_obj["best_timestamp_seconds"]
            kept_videos.append(vid)
            log_rows.append((slug, f"video: {key_label}", "kept, about_the_reef", text))
            counts["videos_annotated"] += 1
        else:
            kept_videos.append(vid)
            log_rows.append((slug, f"video: {key_label}", "no change (unrecognized verdict)", verdict or "(none)"))

    card["videos"] = kept_videos
    card["videos_rejected"] = rejected


def apply_frames(card, recheck, slug, log_rows, counts):
    frame_verdicts = recheck.get("frames", [])
    if not frame_verdicts:
        return

    card_frames = card.get("frames")  # not present on any current card, handled defensively

    for fv in frame_verdicts:
        path_str = fv.get("path")
        if not path_str:
            continue
        verdict = verdict_of(fv, "classification", "shows")
        text = pick_text(fv) or (fv.get("shows") if fv.get("classification") else "")
        src = ROOT / path_str

        if verdict in REJECT_VERDICTS:
            if "rejected" in src.parts:
                log_rows.append((slug, f"frame: {path_str}", "no-op (already in rejected/)", text))
            elif src.exists():
                dest_dir = src.parent / "rejected"
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / src.name
                shutil.move(str(src), str(dest))
                log_rows.append((slug, f"frame: {path_str}", "moved to rejected/",
                                  f"media re-check {RECHECK_DATE}: {verdict} \u2014 {text}"))
            else:
                log_rows.append((slug, f"frame: {path_str}", "no-op (file not found)", "already moved or missing"))
            counts["frames_rejected"] += 1
            if isinstance(card_frames, list):
                card["frames"] = [f for f in card_frames if f.get("path") != path_str]
        else:
            counts["frames_annotated"] += 1
            log_rows.append((slug, f"frame: {path_str}", f"annotated shows={verdict or '(none)'}", text))
            if isinstance(card_frames, list):
                for f in card_frames:
                    if f.get("path") == path_str:
                        f["shows"] = IMAGE_SHOWS_LABEL.get(verdict, verdict)


def main():
    counts = {
        "reefs_processed": 0,
        "images_rejected": 0,
        "images_annotated": 0,
        "hero_recommendations": 0,
        "videos_rejected": 0,
        "videos_annotated": 0,
        "frames_rejected": 0,
        "frames_annotated": 0,
        "errors": 0,
    }
    log_rows = []

    recheck_files = sorted(QA_REEF_DIR.glob("*_media_recheck.json"))
    for recheck_path in recheck_files:
        slug = recheck_path.name[: -len("_media_recheck.json")]
        card_path = CARDS_DIR / f"{slug}.json"
        if not card_path.exists():
            log_rows.append((slug, "-", "SKIPPED", f"card file not found: {card_path}"))
            counts["errors"] += 1
            continue

        try:
            recheck = load_json(recheck_path)
            card = load_json(card_path)
        except Exception as e:
            log_rows.append((slug, "-", "SKIPPED", f"failed to parse JSON: {e}"))
            counts["errors"] += 1
            continue

        apply_images(card, recheck, slug, log_rows, counts)
        apply_videos(card, recheck, slug, log_rows, counts)
        apply_frames(card, recheck, slug, log_rows, counts)

        save_json(card_path, card)
        counts["reefs_processed"] += 1

    write_changelog(log_rows, counts)
    print(json.dumps(counts, indent=2))


def write_changelog(log_rows, counts):
    lines = [f"# Media re-check changes \u2014 applied {RECHECK_DATE}\n",
             "| reef | item | action | reason |", "|---|---|---|---|"]
    for reef, item, action, reason in log_rows:
        reason = str(reason or "").replace("|", "\\|").replace("\n", " ")
        item = str(item or "").replace("|", "\\|")
        lines.append(f"| {reef} | {item} | {action} | {reason} |")
    lines.append("")
    lines.append("## Summary counts")
    for k, v in counts.items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    with open(CHANGELOG, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()

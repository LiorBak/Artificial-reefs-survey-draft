# Video index — Other Geotube / Sand-Container Installations, Israel coast

Note: the researcher lead pointed to the Government Company for Protection of Mediterranean Sea Cliffs' official YouTube channel (`@mccp_israel`, 10 videos). None of its videos are specifically about a geotube (because none was built at these sites), but two are directly about the Netanya works that were built **instead of** the geotube option described in the dossier, so they are the best available real footage for this item.

## 1. Breakwater Project Phase A, Netanya North (פרויקט שוברי גלים שלב א' נתניה צפון)
- YouTube: https://www.youtube.com/watch?v=CEmSn956q-g
- Channel: Government Company for Protection of Mediterranean Sea Cliffs (official)
- Duration: 1:57 (117 s) — **embed this one**, short and directly on-topic
- Uploaded: 2024-03-28
- What it shows: aerial/drone footage of the six rock breakwaters actually built at Netanya (Lagoon Beach to Sironit Beach), the site where a marine geotube was a *permitted but never-used* protection option under TAMA 9/13. No spoken narration (background music only — confirmed from the English auto-caption track, which is pure `[Music]`/noise); the real information is in burned-in Hebrew on-screen captions.
- Transcript: `CEmSn956q-g.txt` (dedupe of auto-captions — contains only music/noise markers, no speech; kept for completeness)
- Key quotes (from burned-in captions and uploader description, mm:ss where visible on-screen):
  - 00:15 — "תחילת הפרויקט נובמבר 2020 / רצועת החוף צרה ומסוכנת עקב קריסות רבות" ("Project start November 2020 / beach strip narrow and dangerous due to repeated collapses")
  - 00:28 — "הפרויקט בוצע על ידי חברת מעגן בפיקוח חברת אדיר" ("Project executed by Ma'agan company, supervised by Adir company") — **new contractor names not found in the text sources used for the dossier**
  - Description: "החברה... השלימה בהצלחה את הקמת שישה שוברי גלים... בין חוף לגון לחוף סירונית בעיר נתניה" ("the Company successfully completed construction of six breakwaters... between Lagoon Beach and Sironit Beach in Netanya")
- Frames (2, both viewed and confirmed on-topic):
  - `03_images/video_frames/israel-geotubes-other-sites/CEmSn956q-g_0015.jpg` — pre-construction aerial of the Netanya cliff/beach, Nov 2020 caption
  - `03_images/video_frames/israel-geotubes-other-sites/CEmSn956q-g_0028.jpg` — excavators/trucks actively building a rock breakwater arm into the sea, contractor caption visible

## 2. Sand Feeding on Netanya Beaches 2022 (הזנת חול בחופי נתניה 2022)
- YouTube: https://www.youtube.com/watch?v=X0qKYp71Fm0
- Channel: Government Company for Protection of Mediterranean Sea Cliffs (official)
- Duration: 1:59 (119 s) — **embed this one too**, short and directly on-topic
- Uploaded: 2022-11-21
- What it shows: aerial b-roll of the ~6-week, 150,000 m³ sand-nourishment operation at Netanya via a Spanish dredging vessel, explicitly tied by the uploader's own description to "the breakwater-construction project" and the wider array of solutions to prevent cliff collapse — the sand-feeding component of the same Netanya scheme covered in the dossier's Netanya row. No subtitle track available (checked; none exists for this video), so no transcript file; summarized here from the uploader's video description only.
- Transcript: not available (no captions on this video)
- Key quotes (from uploader description): "הפרויקט נמשך כשישה שבועות וכלל הזנה של 150 אלף מ"ק חול ים נקי, באמצעות אניית מחפר ספרדית" ("The project ran about six weeks and included feeding 150,000 m³ of clean marine sand via a Spanish dredging vessel")
- Frames: none extracted (video is short enough to embed directly; the Phase A video above already documents the visual of active construction)

## Not used
- Other videos on the `@mccp_israel` channel (general aerial cliff photography of Tel Aviv–Bat Yam, Olga–Polag, Ashdod–Ashkelon) are real b-roll of the Mediterranean coast but are not specific to the Hof HaTzuk or Netanya cases in this dossier, so they were excluded to avoid padding the index with off-topic footage.
- No video specific to the Tel Aviv/Hof HaTzuk case, the "armored geotube" pilot, or the 2019 protest was found; the protest is covered by still photos in `03_images/web/israel-geotubes-other-sites.md` instead.

## Technical notes
- yt-dlp initially failed with "This video is not available" for both videos above due to missing JS-challenge solving; resolved with `--js-runtimes node --remote-components ejs:github` (Node.js was available on this machine; ffmpeg was supplied via `imageio_ffmpeg`).

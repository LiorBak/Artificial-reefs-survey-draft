# Images -- Tel Aviv detached breakwaters (20th century)

Indexed image leads for the Tel Aviv shore-parallel detached-breakwater system. No images were downloaded into the project; this file and the paired `.json` index the URLs only.

## 1. Gordon Beach breakwater (Wikimedia Commons)
- **URL:** https://upload.wikimedia.org/wikipedia/commons/b/bc/%D7%A9%D7%95%D7%91%D7%A8_%D7%94%D7%92%D7%9C%D7%99%D7%9D_%D7%91%D7%97%D7%95%D7%A3_%D7%92%D7%95%D7%A8%D7%93%D7%95%D7%9F_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91.jpg
- **Source page:** https://commons.wikimedia.org/wiki/File:שובר_הגלים_בחוף_גורדון_תל_אביב.jpg
- **Credit:** Ronavni, via Wikimedia Commons
- **License:** CC BY-SA 4.0
- **Date:** 2022-01-04
- **Depicts:** The detached rubble-mound breakwater at Gordon Beach, seen from the promenade -- the offshore rock line and the calm lagoon/tombolo area it protects. This is the single clearest, most citable photo of a Tel Aviv breakwater found this pass.
- **Verification:** `curl -sI` -> HTTP 200, `content-type: image/jpeg`. Also opened and viewed directly -- a shore-parallel rock breakwater is clearly visible offshore, sailboat beyond it.

## 2. Metzitzim Beach breakwater after 2023 restoration (Wikimedia Commons)
- **URL:** https://upload.wikimedia.org/wikipedia/commons/2/26/%D7%97%D7%95%D7%A3_%D7%9E%D7%A6%D7%99%D7%A6%D7%99%D7%9D_%D7%9C%D7%90%D7%97%D7%A8_%D7%A9%D7%99%D7%A7%D7%95%D7%9D_%D7%A9%D7%95%D7%91%D7%A8_%D7%94%D7%92%D7%9C%D7%99%D7%9D_%D7%91%D7%A9%D7%A0%D7%AA_2023.jpg
- **Source page:** https://commons.wikimedia.org/wiki/File:חוף_מציצים_לאחר_שיקום_שובר_הגלים_בשנת_2023.jpg
- **Credit:** Ronavni, via Wikimedia Commons
- **License:** CC BY-SA 4.0
- **Date:** 2023-11-13
- **Depicts:** Metzitzim Beach (Zebulun Maritime School Beach), Tel Aviv, showing a low offshore rubble-mound breakwater after its 2023 restoration, the swim-area buoy line, and a shore-end rock groyne. Directly documents ongoing maintenance of the breakwater system referenced in the dossier's "מכרז 110" tender [R6].
- **Verification:** `curl -sI` -> HTTP 200, `content-type: image/jpeg`. Also opened and viewed -- offshore rubble-mound breakwater and rope swim-line clearly visible.

## 3. Satellite view -- Gordon Beach (map)
- **URL:** https://www.google.com/maps/@32.0827,34.7676,650m/data=!3m1!1e3
- **Credit:** Google Maps / satellite imagery providers
- **License:** Google Maps terms of use (link/view only)
- **Depicts:** Live satellite view centered on Gordon Beach (~32.0827 N, 34.7676 E) where the detached breakwater and the sand tombolo it has produced are visible from above.

## Leads checked and rejected this pass
- Tel Aviv municipality beach pages (Gordon, Tel Baruch) -- pages load, but the actual photos served (`.../PublishingImages/...jpg`) are generic beach-activity shots (e.g. beach volleyball) with no breakwater visible; downloaded to scratch and viewed to confirm, then discarded.
- `חוף_גורדון.jpg` (Commons, "tombolo at Gordon Beach") -- file page confirms a tombolo photo, but the image itself was unreachable this pass (Wikimedia rate-limited the fetching IP, HTTP 429, before it could be visually verified) -- **not included**, flagged as a follow-up lead.
- `Charles_Clore_beach,_Tel_Aviv-Yafo_coastal_strip_2013.jpg` and `Hilton_Beach_on_the_Tel_Aviv-Yafo_coastline,_2013.jpg` (Commons) -- both are known to be linked from the Hebrew Wikipedia breakwater article/coastal-strip article, and file-page metadata (author Michael Jacobson, Sep 2013, CC BY-SA) was retrieved, but Wikimedia's upload servers returned HTTP 429 (rate limit) for the remainder of this session before the actual image content could be confirmed to show a breakwater -- **not included**, flagged as follow-up leads worth re-checking later.
- Mishmar HaYam (Gordon Beach caves piece) -- images on the page are close-up fish photographs, not breakwater/structure shots.
- Ynet Tzuk Beach protest photos (2019) -- these show surfers protesting a *planned* geotube breakwater at Tzuk Beach that had not yet been built at the time of the photos, and depict people/signage rather than an existing detached-breakwater structure -- out of scope for "this exact place/structure" as it existed.

## Notes for a follow-up pass
- Retry `commons.wikimedia.org` / `upload.wikimedia.org` fetches for `חוף_גורדון.jpg` (tombolo), `Hilton_Beach_on_the_Tel_Aviv-Yafo_coastline,_2013.jpg`, and `Charles_Clore_beach,_Tel_Aviv-Yafo_coastal_strip_2013.jpg` once the Wikimedia rate limit (HTTP 429, hit repeatedly this session, likely shared across parallel agents on this machine) has cleared -- these are promising, already-identified candidates for beaches 3-6 of a fuller image set.

"""capture_navionics.py - screenshots of Garmin Navionics Marine Maps (https://webapp.navionics.com/ -> https://maps.garmin.com/en-US/marine/)
around the Bunbury Back Beach reef site, in MY OWN headless Chrome (temporary profile, DevTools protocol), never the shared browser pane.

What it does (nothing is accepted, bypassed or logged into; the page needed no login, CAPTCHA or consent dialog on 2026-10-05):
  1. launches chrome.exe --headless=new with a FRESH profile (unique folder under %TEMP%) and a RANDOM free DevTools port (HEADLESS CHROME ISOLATION rule, _agent_briefs/model_3d.md:
     a fixed port 9341 used earlier in this run was hijacked by another agent); remembers ITS OWN PID only and terminates only that PID tree at the end;
     before every screenshot it checks that the tab still shows the Garmin viewer at the site; if not (tab hijacked), the whole capture is repeated with a new port and profile;
  2. injects a hook so that the page's Leaflet map object is reachable as window.__map (the page does not expose it);
  3. opens the viewer with the page's own `key` (geohash of the site), sets Depth units = Meters and Chart type = SonarChart Maps / Nautical Charts
     by clicking the page's own option labels, then Leaflet setView(site, zoom) and saves the map container as PNG;
  4. writes session_state.json (url, centre, zoom, bounds, size, user agent, UTC time).
Output (private research copies, (c) Garmin, "Not to be used for navigation"): sonar_m_z18_dpr1.png (985 x 851 px, 0.4994 m/px), sonar_m_z18_dpr2.png (1970 x 1702 px, 0.2497 m/px),
sonar_m_z17_dpr1.png, nautical_m_z18_dpr2.png, nautical_m_z17_dpr1.png, app_options_sonarchart_meters.png, session_state.json.
Usage:  python capture_navionics.py [--chrome "C:/Program Files/Google/Chrome/Application/chrome.exe"]
Requires: websockets (already installed).  Not part of build_3d.py (the screenshots are inputs; the analysis is nav_annotate.py).
"""
import argparse
import asyncio
import base64
import datetime
import json
import os
import socket
import subprocess
import tempfile
import urllib.request

import websockets

SITE = (-33.3276, 115.6284)            # card-derived site point (shape.json location_note), +-100 m
GEOHASH = "qd44rhyh9"                  # geohash of SITE (9 characters)
HOOK = ("(function(){var _L;Object.defineProperty(window,'L',{configurable:true,get:function(){return _L;},set:function(v){_L=v;"
        "try{if(v&&v.Map&&v.Map.addInitHook){v.Map.addInitHook(function(){window.__map=this;});}}catch(e){}}});})();")
HERE = os.path.dirname(os.path.abspath(__file__))


class CDP:
    def __init__(self, port):
        self.port, self.id, self.pending, self.ws = port, 0, {}, None

    async def connect(self):
        tabs = []
        for _ in range(40):
            try:
                tabs = json.loads(urllib.request.urlopen("http://127.0.0.1:%d/json" % self.port).read())
                break
            except Exception:
                await asyncio.sleep(0.5)
        page = [t for t in tabs if t["type"] == "page"][0]
        self.ws = await websockets.connect(page["webSocketDebuggerUrl"], max_size=2 ** 28)
        asyncio.create_task(self._reader())

    async def _reader(self):
        async for m in self.ws:
            d = json.loads(m)
            if "id" in d and d["id"] in self.pending:
                self.pending.pop(d["id"]).set_result(d)

    async def send(self, method, **params):
        self.id += 1
        fut = asyncio.get_event_loop().create_future()
        self.pending[self.id] = fut
        await self.ws.send(json.dumps({"id": self.id, "method": method, "params": params}))
        r = await asyncio.wait_for(fut, 120)
        if "error" in r:
            raise RuntimeError(method + ": " + json.dumps(r["error"]))
        return r.get("result", {})

    async def eval(self, expr):
        r = await self.send("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(json.dumps(r["exceptionDetails"])[:400])
        return r["result"].get("value")

    async def shot(self, path, clip=None):
        p = {"format": "png"}
        if clip:
            p["clip"] = clip
        r = await self.send("Page.captureScreenshot", **p)
        open(path, "wb").write(base64.b64decode(r["data"]))


async def click_label(c, text):
    return await c.eval("""(()=>{const t=%s;const e=[...document.querySelectorAll('label')].filter(x=>x.children.length<=2&&(x.innerText||'').trim()===t);
      if(!e.length)return 'notfound';e[0].click();return 'clicked';})()""" % json.dumps(text))


async def wait_map(c, url=None, tries=4):
    """wait until the hook has captured the page's Leaflet map; reload the page if it did not (the hook is racy on some loads)"""
    for k in range(tries):
        for _ in range(20):
            if await c.eval("!!(window.__map && window.__map.getSize)"):
                return True
            await asyncio.sleep(1)
        print("map object not found, reloading (%d)" % (k + 1))
        await c.send("Page.navigate", url=url or await c.eval("location.href"))
        await asyncio.sleep(8)
    raise RuntimeError("Leaflet map object never appeared")


async def toggle_options(c):
    await c.send("Input.dispatchMouseEvent", type="mousePressed", x=495, y=155, button="left", clickCount=1)
    await c.send("Input.dispatchMouseEvent", type="mouseReleased", x=495, y=155, button="left", clickCount=1)
    await asyncio.sleep(1.5)


def free_port():
    """a random free TCP port chosen by the OS (bind to port 0)"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sk:
        sk.bind(("127.0.0.1", 0))
        return sk.getsockname()[1]


async def check_tab(c):
    """the tab must still be the Garmin viewer at the site; anything else means it was hijacked or navigated away"""
    href = await c.eval("location.href")
    ok = "maps.garmin.com/en-US/marine" in href and bool(await c.eval("!!(window.__map && window.__map.getCenter)"))
    if not ok:
        raise RuntimeError("tab is not the Garmin viewer any more (href %s): hijacked or navigated away" % href[:80])


async def run(chrome, port):
    prof = tempfile.mkdtemp(prefix="nav_chrome_bunbury_")      # unique fresh profile for this run
    proc = subprocess.Popen([chrome, "--headless=new", "--remote-debugging-port=%d" % port, "--user-data-dir=" + prof, "--window-size=1400,1000",
                             "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--no-first-run", "--no-default-browser-check", "about:blank"])
    print("started own Chrome pid", proc.pid)
    try:
        c = CDP(port)
        await c.connect()
        await c.send("Page.enable")
        await c.send("Runtime.enable")
        await c.send("Page.addScriptToEvaluateOnNewDocument", source=HOOK)
        await c.send("Emulation.setDeviceMetricsOverride", width=1400, height=1000, deviceScaleFactor=1, mobile=False)
        await c.send("Page.navigate", url="https://webapp.navionics.com/")        # redirects to maps.garmin.com/en-US/marine/
        await asyncio.sleep(10)
        print("landed on", await c.eval("location.href"))
        await c.send("Page.navigate", url="https://maps.garmin.com/en-US/marine/?maps=another-brand&overlay=false&key=" + GEOHASH)
        await asyncio.sleep(8)
        URL2 = "https://maps.garmin.com/en-US/marine/?maps=another-brand&overlay=false&key=" + GEOHASH
        await wait_map(c, URL2)
        rect = json.loads(await c.eval("JSON.stringify(document.querySelector('.leaflet-container').getBoundingClientRect())"))
        clip = {"x": rect["x"], "y": rect["y"], "width": rect["width"], "height": rect["height"], "scale": 1}
        await toggle_options(c)                                                       # open MAP OPTIONS
        print("meters:", await click_label(c, "Meters (m)"))
        await asyncio.sleep(1.5)
        print("sonar:", await click_label(c, "SonarChart\u2122 Maps"))
        await asyncio.sleep(3)
        await c.eval("window.__map.setView([%f,%f],17,{animate:false});1" % SITE)
        await asyncio.sleep(4)
        await c.shot(os.path.join(HERE, "app_options_sonarchart_meters.png"))        # whole window with the options panel open (record of the settings)
        await toggle_options(c)                                                       # close it
        state = {}

        async def grab(name, z, dpr):
            await c.send("Emulation.setDeviceMetricsOverride", width=1400, height=1000, deviceScaleFactor=dpr, mobile=False)
            await asyncio.sleep(1)
            await wait_map(c, URL2)
            await c.eval("window.__map.invalidateSize();window.__map.setView([%f,%f],%d,{animate:false});1" % (SITE[0], SITE[1], z))
            await asyncio.sleep(6)
            await check_tab(c)
            try:                                  # read the map state BEFORE the screenshot (the page may re-create its map afterwards)
                state[name] = json.loads(await c.eval("JSON.stringify({centre:window.__map.getCenter(),zoom:window.__map.getZoom(),size:window.__map.getSize(),bounds:window.__map.getBounds()})"))
            except Exception as e:
                state[name] = {"error": str(e)[:120]}
            await check_tab(c)
            await c.shot(os.path.join(HERE, name), clip=clip)
            await check_tab(c)                    # still the same page after the screenshot
            print("saved", name, state[name].get("zoom"))

        await grab("sonar_m_z18_dpr1.png", 18, 1)
        await grab("sonar_m_z18_dpr2.png", 18, 2)
        await grab("sonar_m_z17_dpr1.png", 17, 1)
        await c.send("Emulation.setDeviceMetricsOverride", width=1400, height=1000, deviceScaleFactor=1, mobile=False)
        await toggle_options(c)
        print("nautical:", await click_label(c, "Nautical Charts"))
        await asyncio.sleep(2)
        await toggle_options(c)
        await grab("nautical_m_z18_dpr2.png", 18, 2)
        await grab("nautical_m_z17_dpr1.png", 17, 1)
        json.dump({"href": await c.eval("location.href"), "site": SITE, "geohash": GEOHASH, "ua": await c.eval("navigator.userAgent"), "title": await c.eval("document.title"),
                   "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
                   "options": "Depth units = Meters; SonarChart Maps then Nautical Charts; Seabed areas = Hide (default); shallow shading 1 m (default for metres)",
                   "captures": state}, open(os.path.join(HERE, "session_state.json"), "w"), indent=1)
    finally:
        subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True)       # only the PID tree this script started
        print("terminated own Chrome pid", proc.pid)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--chrome", default=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
    a = ap.parse_args()
    for attempt in range(3):
        port = free_port()
        print("attempt %d: own Chrome on random DevTools port %d" % (attempt + 1, port))
        try:
            asyncio.run(run(a.chrome, port))
            break
        except RuntimeError as e:
            print("capture attempt failed:", e)

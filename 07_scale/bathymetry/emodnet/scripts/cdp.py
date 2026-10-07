"""Minimal Chrome DevTools Protocol driver for an ISOLATED headless Chrome (own random port, own fresh profile).
Never attaches to a port it did not launch. Used for the EMODnet geoviewer (Step 2 of METHOD.md)."""
import asyncio, base64, json, os, socket, subprocess, tempfile, time, urllib.request, shutil, uuid
import websockets

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def free_port():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); p = s.getsockname()[1]; s.close(); return p

class Chrome:
    def __init__(self, width=1600, height=1000, tag="emodnet"):
        self.port = free_port()
        self.profile = os.path.join(tempfile.gettempdir(), f"chrome_{tag}_{uuid.uuid4().hex[:8]}")
        os.makedirs(self.profile, exist_ok=True)
        self.width, self.height = width, height
        args = [CHROME, "--headless=new", f"--remote-debugging-port={self.port}", "--remote-debugging-address=127.0.0.1",
                f"--user-data-dir={self.profile}", "--no-first-run", "--no-default-browser-check", "--disable-extensions",
                "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist",
                f"--window-size={width},{height}", "about:blank"]
        self.proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.pid = self.proc.pid
        self.ws = None; self.msgid = 0; self.events = []; self.pending = {}
        # wait for the port WE opened
        for _ in range(100):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json/version", timeout=1).read(); break
            except Exception: time.sleep(0.2)
        else: raise RuntimeError("chrome did not start")

    async def connect(self):
        pages = json.load(urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json/list"))
        page = [p for p in pages if p["type"] == "page"][0]
        self.ws = await websockets.connect(page["webSocketDebuggerUrl"], max_size=200_000_000)
        self._reader = asyncio.create_task(self._read())
        await self.send("Page.enable"); await self.send("Network.enable"); await self.send("Runtime.enable")
        await self.send("Emulation.setDeviceMetricsOverride", dict(width=self.width, height=self.height, deviceScaleFactor=1, mobile=False))

    async def _read(self):
        async for raw in self.ws:
            m = json.loads(raw)
            if "id" in m and m["id"] in self.pending: self.pending.pop(m["id"]).set_result(m)
            elif m.get("method") == "Fetch.requestPaused": asyncio.create_task(self._fix_config(m))
            else: self.events.append(m)

    async def send(self, method, params=None, timeout=60):
        self.msgid += 1; i = self.msgid
        fut = asyncio.get_event_loop().create_future(); self.pending[i] = fut
        await self.ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
        r = await asyncio.wait_for(fut, timeout)
        if "error" in r: raise RuntimeError(f"{method}: {r['error']}")
        return r.get("result", {})

    async def enable_config_fix(self):
        """The geoviewer appends location.search to config.php?legacybaselayers=1 (=> '1?layers=...'), which makes the server
        return a different base-layer format and the app crashes on any URL with parameters. We rewrite ONLY that one request to
        the clean URL the app itself uses on a plain load. (No access control involved.)"""
        await self.send("Fetch.enable", {"patterns": [{"urlPattern": "*geoviewer/config.php*", "requestStage": "Request"}]})

    async def _fix_config(self, m):
        p = m["params"]; url = p["request"]["url"]
        try:
            if "config.php" in url: await self.send("Fetch.continueRequest", {"requestId": p["requestId"], "url": "https://emodnet.ec.europa.eu/geoviewer/config.php?legacybaselayers=1"})
            else: await self.send("Fetch.continueRequest", {"requestId": p["requestId"]})
        except Exception as e: print("fetch fix failed", e)

    async def goto(self, url, wait=6):
        await self.send("Page.navigate", {"url": url}); await asyncio.sleep(wait)

    async def js(self, expr, await_promise=True):
        r = await self.send("Runtime.evaluate", {"expression": expr, "returnByValue": True, "awaitPromise": await_promise})
        if "exceptionDetails" in r: return {"__error__": r["exceptionDetails"].get("exception", {}).get("description", str(r["exceptionDetails"]))}
        return r["result"].get("value")

    async def shot(self, path, clip=None):
        p = {"format": "png"}
        if clip: p["clip"] = clip
        r = await self.send("Page.captureScreenshot", p)
        open(path, "wb").write(base64.b64decode(r["data"]))

    async def click(self, x, y):
        for t in ("mousePressed", "mouseReleased"):
            await self.send("Input.dispatchMouseEvent", {"type": t, "x": x, "y": y, "button": "left", "clickCount": 1})

    def requests(self, substr=None):
        out = []
        for e in self.events:
            if e.get("method") == "Network.requestWillBeSent":
                u = e["params"]["request"]["url"]
                if substr is None or substr in u: out.append(u)
        return out

    async def close(self):
        try:
            if self.ws: await self.ws.close()
        except Exception: pass
        # kill ONLY the process tree we started
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(1); shutil.rmtree(self.profile, ignore_errors=True)

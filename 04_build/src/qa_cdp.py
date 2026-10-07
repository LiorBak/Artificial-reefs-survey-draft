"""Tiny Chrome DevTools-protocol driver for QA (own headless Chrome, never the shared browser pane).

Every Chrome started here uses a RANDOM free remote-debugging port and a FRESH --user-data-dir under %TEMP%;
the process is terminated by PID on close(). Needs `websockets` (pip install websockets).

    with Chrome(width=1440, height=900) as c:
        c.goto("file:///.../artificial_reefs.html#view/models3d")
        c.wait_for("document.querySelector('.m3d-model')")
        print(c.eval("document.title"))
        c.screenshot("shot.png", full_page=True)
        c.hover_selector(".m3d-thumb")        # real mouse-move to the element's centre
        c.click_selector("button.m3d-load")

Used by qa_models3d.py (3D models tab).
"""
from __future__ import annotations

import asyncio
import base64
import json
import os
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def find_chrome() -> str:
    for c in CANDIDATES:
        if Path(c).exists():
            return c
    p = shutil.which("chrome") or shutil.which("google-chrome")
    if not p:
        raise SystemExit("No Chrome found")
    return p


class Chrome:
    def __init__(self, width: int = 1440, height: int = 900, extra_args: list[str] | None = None,
                 allow_file_access: bool = False, mobile: bool = False, scale: float = 1.0):
        self.width, self.height, self.mobile, self.scale = width, height, mobile, scale
        self.port = free_port()
        self.profile = tempfile.mkdtemp(prefix="reef_cdp_")
        args = [find_chrome(), "--headless=new", f"--remote-debugging-port={self.port}",
                f"--user-data-dir={self.profile}", "--no-first-run", "--no-default-browser-check",
                "--disable-extensions", "--hide-scrollbars", f"--window-size={width},{height}",
                "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist",
                "--remote-allow-origins=*"]
        if allow_file_access:
            args.append("--allow-file-access-from-files")
        args += extra_args or []
        args.append("about:blank")
        self.proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.loop = asyncio.new_event_loop()
        self.ws = None
        self._id = 0
        self.console: list[str] = []
        self.errors: list[str] = []
        self.requests: list[dict] = []
        self._connect()

    # ------------------------------------------------------------------ plumbing
    def _connect(self):
        import websockets  # noqa: PLC0415

        url = None
        for _ in range(100):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{self.port}/json", timeout=1) as r:
                    tabs = json.load(r)
                pages = [t for t in tabs if t.get("type") == "page"]
                if pages:
                    url = pages[0]["webSocketDebuggerUrl"]
                    break
            except Exception:
                pass
            time.sleep(0.2)
        if not url:
            raise RuntimeError("Chrome did not start")
        self.ws = self.loop.run_until_complete(websockets.connect(url, max_size=64 * 1024 * 1024))
        self.call("Page.enable")
        self.call("Runtime.enable")
        self.call("Network.enable")
        self.call("Log.enable")
        self.call("Emulation.setFocusEmulationEnabled", enabled=True)   # headless: focus()/blur() events fire as in a focused window
        self.call("Emulation.setDeviceMetricsOverride", width=self.width, height=self.height,
                  deviceScaleFactor=self.scale, mobile=self.mobile)

    def _handle_event(self, msg: dict):
        m = msg.get("method")
        p = msg.get("params", {})
        if m == "Runtime.consoleAPICalled":
            txt = " ".join(str(a.get("value", a.get("description", ""))) for a in p.get("args", []))
            self.console.append(f"[{p.get('type')}] {txt}")
        elif m == "Runtime.exceptionThrown":
            d = p.get("exceptionDetails", {})
            self.errors.append(f"EXC {d.get('text')} {(d.get('exception') or {}).get('description', '')[:300]}")
        elif m == "Log.entryAdded":
            e = p.get("entry", {})
            if e.get("level") in ("error", "warning"):
                self.errors.append(f"LOG {e.get('level')}: {e.get('text')} {e.get('url', '')}")
        elif m == "Network.responseReceived":
            r = p.get("response", {})
            self.requests.append({"url": r.get("url"), "status": r.get("status")})
        elif m == "Network.loadingFailed":
            self.errors.append(f"NETFAIL {p.get('errorText')} blocked={p.get('blockedReason')} id={p.get('requestId')}")

    def call(self, method: str, **params):
        async def go():
            self._id += 1
            i = self._id
            await self.ws.send(json.dumps({"id": i, "method": method, "params": params}))
            while True:
                msg = json.loads(await asyncio.wait_for(self.ws.recv(), timeout=90))
                if msg.get("id") == i:
                    if "error" in msg:
                        raise RuntimeError(f"{method}: {msg['error']}")
                    return msg.get("result", {})
                self._handle_event(msg)
        return self.loop.run_until_complete(go())

    def pump(self, seconds: float = 0.5):
        """Process pending events for a while (console messages, errors)."""
        async def go():
            end = time.time() + seconds
            while time.time() < end:
                try:
                    msg = json.loads(await asyncio.wait_for(self.ws.recv(), timeout=max(0.05, end - time.time())))
                    self._handle_event(msg)
                except asyncio.TimeoutError:
                    break
        self.loop.run_until_complete(go())

    # ------------------------------------------------------------------ actions
    def goto(self, url: str, wait: float = 1.5):
        self.call("Page.navigate", url=url)
        self.pump(wait)

    def eval(self, expr: str, await_promise: bool = False):
        r = self.call("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=await_promise)
        if "exceptionDetails" in r:
            raise RuntimeError(f"JS error: {r['exceptionDetails'].get('text')} {(r['exceptionDetails'].get('exception') or {}).get('description', '')[:400]}")
        return r["result"].get("value")

    def wait_for(self, expr: str, timeout: float = 30, interval: float = 0.4):
        end = time.time() + timeout
        while time.time() < end:
            try:
                if self.eval(f"!!({expr})"):
                    return True
            except RuntimeError:
                pass
            self.pump(interval)
        return False

    def screenshot(self, path: str | Path, full_page: bool = False, clip: dict | None = None):
        params: dict = {"format": "png"}
        if full_page:
            m = self.call("Page.getLayoutMetrics")
            cs = m.get("cssContentSize") or m.get("contentSize")
            params["clip"] = {"x": 0, "y": 0, "width": cs["width"], "height": min(cs["height"], 16000), "scale": 1}
            params["captureBeyondViewport"] = True
        if clip:
            params["clip"] = {**clip, "scale": 1}
            params["captureBeyondViewport"] = True
        r = self.call("Page.captureScreenshot", **params)
        Path(path).write_bytes(base64.b64decode(r["data"]))
        return Path(path).stat().st_size

    def rect(self, selector: str, index: int = 0):
        js = (f"(()=>{{const e=document.querySelectorAll({json.dumps(selector)})[{index}];if(!e)return null;"
              "e.scrollIntoView({block:'center',inline:'center'});const r=e.getBoundingClientRect();"
              "return {x:r.x,y:r.y,w:r.width,h:r.height};})()")
        return self.eval(js)

    def mouse(self, x: float, y: float, kind: str = "mouseMoved", button: str = "none", clicks: int = 0):
        self.call("Input.dispatchMouseEvent", type=kind, x=x, y=y, button=button, clickCount=clicks)

    def hover_selector(self, selector: str, index: int = 0, settle: float = 0.8):
        r = self.rect(selector, index)
        if not r:
            raise RuntimeError(f"no element for {selector}")
        self.mouse(0, 0)
        self.mouse(r["x"] + r["w"] / 2, r["y"] + r["h"] / 2)
        self.pump(settle)
        return r

    def click_selector(self, selector: str, index: int = 0, settle: float = 0.8):
        r = self.rect(selector, index)
        if not r:
            raise RuntimeError(f"no element for {selector}")
        x, y = r["x"] + r["w"] / 2, r["y"] + r["h"] / 2
        self.mouse(x, y)
        self.mouse(x, y, "mousePressed", "left", 1)
        self.mouse(x, y, "mouseReleased", "left", 1)
        self.pump(settle)
        return r

    VK = {"Escape": 27, "Enter": 13, "Tab": 9, "ArrowLeft": 37, "ArrowRight": 39, "ArrowUp": 38, "ArrowDown": 40, " ": 32}

    def press(self, key: str, code: str | None = None):
        vk = self.VK.get(key, 0)
        for kind in ("rawKeyDown", "keyUp"):
            self.call("Input.dispatchKeyEvent", type=kind, key=key, code=code or key, windowsVirtualKeyCode=vk, nativeVirtualKeyCode=vk)
        self.pump(0.2)

    def set_color_scheme(self, scheme: str):
        self.call("Emulation.setEmulatedMedia", features=[{"name": "prefers-color-scheme", "value": scheme}])

    # ------------------------------------------------------------------ lifecycle
    def close(self):
        try:
            if self.ws is not None:
                self.loop.run_until_complete(self.ws.close())
        except Exception:
            pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=10)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass
        shutil.rmtree(self.profile, ignore_errors=True)
        try:
            self.loop.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()

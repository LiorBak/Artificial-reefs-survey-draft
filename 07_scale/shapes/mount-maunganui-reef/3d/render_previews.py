"""render_previews.py - headless Chrome screenshots of index.html (served by this script on a random free local port) into preview_*.png.

Isolation (brief, HEADLESS CHROME ISOLATION rule): own Chrome process only, an OS-assigned random free DevTools port, a fresh --user-data-dir under %TEMP% unique
to the run, the DevTools websocket taken from the process this script started, terminated by PID at the end; never the shared browser pane.
The jsDelivr CDN named in the import map of index.html is unreachable from this machine; THREE_VENDOR must point to a folder holding build/three.module.js and
examples/jsm/{controls/OrbitControls.js, renderers/CSS2DRenderer.js} (three r170; a copy is kept in %TEMP%\\mmr3d_vendor) and the requests are answered from there
by DevTools request interception.  index.html itself keeps the CDN import map.
Usage: THREE_VENDOR=<dir> python render_previews.py name.png:hash [name.png:hash ...] [--size=1400x900]
"""
import asyncio, base64, json, os, socket, subprocess, sys, tempfile, time, urllib.request
import websockets

HERE = os.path.dirname(os.path.abspath(__file__))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def free_port():
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p


class Dev:
    def __init__(self, ws, vendor):
        self.ws, self.vendor, self.n, self.futs = ws, vendor, 0, {}
        self.task = asyncio.ensure_future(self.reader())

    async def reader(self):
        async for raw in self.ws:
            m = json.loads(raw)
            if 'id' in m and m['id'] in self.futs:
                f = self.futs.pop(m['id'])
                f.set_exception(RuntimeError(str(m['error']))) if 'error' in m else f.set_result(m.get('result', {}))
            elif m.get('method') == 'Fetch.requestPaused' and self.vendor:
                u = m['params']['request']['url']; rel = u.split('three@0.170.0/', 1)[1]
                f = os.path.join(self.vendor, *rel.split('/'))
                if os.path.exists(f):
                    body = base64.b64encode(open(f, 'rb').read()).decode()
                    asyncio.ensure_future(self.send('Fetch.fulfillRequest', requestId=m['params']['requestId'], responseCode=200,
                                                    responseHeaders=[{'name': 'Content-Type', 'value': 'application/javascript'}, {'name': 'Access-Control-Allow-Origin', 'value': '*'}], body=body))
                else:
                    asyncio.ensure_future(self.send('Fetch.failRequest', requestId=m['params']['requestId'], errorReason='Failed'))

    async def send(self, method, **params):
        self.n += 1; i = self.n
        fut = asyncio.get_event_loop().create_future(); self.futs[i] = fut
        await self.ws.send(json.dumps({'id': i, 'method': method, 'params': params}))
        return await asyncio.wait_for(fut, 120)

    async def ev(self, js):
        r = await self.send('Runtime.evaluate', expression=js, returnByValue=True, awaitPromise=True)
        return r.get('result', {}).get('value')


async def main(jobs, w, h):
    hp = free_port()
    http = subprocess.Popen([sys.executable, '-m', 'http.server', str(hp), '--bind', '127.0.0.1'], cwd=HERE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    port = free_port(); prof = tempfile.mkdtemp(prefix='mmr3d_chrome_')
    proc = subprocess.Popen([CHROME, '--headless=new', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--remote-debugging-port=%d' % port,
                             '--user-data-dir=' + prof, '--window-size=%d,%d' % (w, h), '--no-first-run', '--hide-scrollbars', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws_url = None
        for _ in range(60):
            try:
                tabs = json.load(urllib.request.urlopen('http://127.0.0.1:%d/json' % port, timeout=2)); pg = [t for t in tabs if t['type'] == 'page']
                if pg: ws_url = pg[0]['webSocketDebuggerUrl']; break
            except Exception: time.sleep(0.5)
        vendor = os.environ.get('THREE_VENDOR')
        async with websockets.connect(ws_url, max_size=64 * 1024 * 1024) as ws:
            d = Dev(ws, vendor)
            await d.send('Page.enable'); await d.send('Runtime.enable')
            await d.send('Emulation.setDeviceMetricsOverride', width=w, height=h, deviceScaleFactor=1, mobile=False)
            if vendor: await d.send('Fetch.enable', patterns=[{'urlPattern': '*cdn.jsdelivr.net/npm/three@0.170.0/*', 'requestStage': 'Request'}])
            await d.send('Page.addScriptToEvaluateOnNewDocument', source="window.addEventListener('error',function(e){window.__errs=(window.__errs||'')+e.message+' | ';});")
            first = True
            for name, hash_ in jobs:
                url = 'http://127.0.0.1:%d/index.html' % hp
                await d.send('Page.navigate', url=url + '?r=%d#%s' % (int(time.time() * 1000), hash_)); first = False
                await asyncio.sleep(1)
                for _ in range(90):
                    if await d.ev('window.__reefReady === true') is True: break
                    await asyncio.sleep(1)
                await asyncio.sleep(4)
                href = await d.ev('location.href')
                err = await d.ev("(document.getElementById('err').textContent||'') + (window.__errs||'')")
                shot = await d.send('Page.captureScreenshot', format='png')
                open(os.path.join(HERE, name), 'wb').write(base64.b64decode(shot['data']))
                print(name, href, 'ERR: ' + err if err else 'no page errors', flush=True)
    finally:
        for p in (proc, http):
            try: p.terminate(); p.wait(10)
            except Exception: subprocess.run(['taskkill', '/PID', str(p.pid), '/T', '/F'], capture_output=True)       # our own PIDs only


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--size')]
    size = [a for a in sys.argv[1:] if a.startswith('--size=')]
    w, h = (map(int, size[0].split('=')[1].split('x')) if size else (1400, 900))
    jobs = [tuple(a.split(':', 1)) for a in args] or [('preview_plan.png', 'view=plan'), ('preview_oblique.png', 'view=oblique')]
    asyncio.run(main(jobs, w, h))

"""navionics_capture.py - capture the Garmin Navionics chart around the Palm Beach reef (private research copy, 'not for navigation').

What it does (all in ITS OWN headless Chrome with a throw-away profile in %TEMP%; it never touches another browser):
  1. opens https://maps.garmin.com/en-US/marine (the successor of the decommissioned Navionics ChartViewer, no login needed) centred on the
     reef centroid through the page's geohash 'key' parameter;
  2. sets Depth units = Meters, Chart type = Nautical Charts or SonarChart Maps;
  3. for zoom 17 and 18 saves the map area at 'Shallow shading' = 0, 1, ... 10 m. The shaded (blue) region is the water shallower than the setting, so
     its edge is the chart contour of that depth (checked against the printed contour labels, see METHODS_3D.md 3.5);
  4. writes ../src/navionics/<chart>_z<zoom>_shade<value>.png and ../src/navionics/capture_log.json.
No cookie/consent banner, login or CAPTCHA appeared (2026-10-05); if one ever does, stop and ask a person - do not bypass it.
Only the Chrome process started here is terminated (by PID). Requires: Chrome, python 'websockets'.
Usage: python navionics_capture.py [--test]     (--test: one base view per chart type only)
"""
import asyncio, base64, datetime, json, os, socket, subprocess, sys, tempfile, time, urllib.request
import websockets

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, '..', 'src', 'navionics')
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
REEF = (-28.107334, 153.470913)          # council polygon centroid = shape.json geo.centroid_latlon
GEOHASH_KEY = 'r7j0h74ngmnv'             # geohash of REEF (12 characters)
URL = 'https://maps.garmin.com/en-US/marine?maps=another-brand&overlay=false&key=' + GEOHASH_KEY
# hook: expose the Leaflet map instance (the page does not)
HOOK = """(function(){var _L;Object.defineProperty(window,'L',{configurable:true,get:function(){return _L;},set:function(v){_L=v;
try{if(v&&v.Map&&v.Map.addInitHook){v.Map.addInitHook(function(){(window.__maps=window.__maps||[]).push(this);});}}catch(e){}}});})();"""
SET_SHADE = """(function(v){var r=document.querySelector('input[type=range]');if(!r)return 'no range';
var set=Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;set.call(r,String(v));
r.dispatchEvent(new Event('input',{bubbles:true}));r.dispatchEvent(new Event('change',{bubbles:true}));return r.value;})(%s)"""
# page geometry at a 1400 x 900 window (checked 2026-10-05): MAP OPTIONS button, radio buttons, map clip
BTN_OPTIONS, RADIO_METERS, RADIO_SONAR, RADIO_NAUT = (496, 156), (452, 574), (452, 372), (452, 340)
CLIP = dict(x=400, y=113, width=982, height=655, scale=1)


def free_port():
    """a random free port chosen by the OS (bind to port 0); never a fixed number, so we cannot attach to another agent's browser"""
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port


class Chrome:
    def __init__(self, w=1400, h=900):
        self.port = free_port()
        self.profile = tempfile.mkdtemp(prefix='palmbeach3d_chrome_')      # fresh profile, unique to this run
        self.proc = subprocess.Popen([CHROME, '--headless=new', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist',
                                      '--remote-debugging-port=%d' % self.port, '--user-data-dir=' + self.profile, '--window-size=%d,%d' % (w, h),
                                      '--no-first-run', '--no-default-browser-check', '--hide-scrollbars', '--lang=en-US', 'about:blank'],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            try:
                tabs = json.load(urllib.request.urlopen('http://127.0.0.1:%d/json' % self.port, timeout=2))
                pages = [t for t in tabs if t['type'] == 'page']
                if pages:
                    self.ws_url = pages[0]['webSocketDebuggerUrl']; break
            except Exception:
                time.sleep(0.5)

    def close(self):
        try:
            self.proc.terminate(); self.proc.wait(10)
        except Exception:
            subprocess.run(['taskkill', '/PID', str(self.proc.pid), '/T', '/F'], capture_output=True)   # our own PID only


class Page:
    def __init__(self, ws_url):
        self.ws_url, self.n = ws_url, 0

    async def __aenter__(self):
        self.ws = await websockets.connect(self.ws_url, max_size=64 * 1024 * 1024); return self

    async def __aexit__(self, *a):
        await self.ws.close()

    async def send(self, method, **params):
        self.n += 1; i = self.n
        await self.ws.send(json.dumps({'id': i, 'method': method, 'params': params}))
        while True:
            m = json.loads(await asyncio.wait_for(self.ws.recv(), 90))
            if m.get('id') == i:
                if 'error' in m: raise RuntimeError(str(m['error']))
                return m.get('result', {})

    async def ev(self, js):
        r = await self.send('Runtime.evaluate', expression=js, returnByValue=True, awaitPromise=True)
        return r.get('result', {}).get('value')

    async def click(self, xy):
        for t in ('mouseMoved', 'mousePressed', 'mouseReleased'):
            await self.send('Input.dispatchMouseEvent', type=t, x=xy[0], y=xy[1], button='left', clickCount=1)

    async def shot(self, path):
        r = await self.send('Page.captureScreenshot', format='png', clip=CLIP)
        open(path, 'wb').write(base64.b64decode(r['data']))


async def main(test=False):
    os.makedirs(OUTDIR, exist_ok=True)
    ch = Chrome()
    log = dict(url=URL, started=datetime.datetime.now().isoformat(timespec='seconds'), reef_latlon=REEF, files=[],
               note='Garmin Navionics via maps.garmin.com marine map; depth units Meters; not for navigation; private research copy')
    try:
        async with Page(ch.ws_url) as pg:
            await pg.send('Page.enable')
            await pg.send('Page.addScriptToEvaluateOnNewDocument', source=HOOK)
            await pg.send('Page.navigate', url=URL)
            await asyncio.sleep(14)
            for tag, radio in (('sonar', RADIO_SONAR), ('naut', RADIO_NAUT)):
                await pg.click(BTN_OPTIONS); await asyncio.sleep(1.5)
                await pg.click(RADIO_METERS); await asyncio.sleep(1)
                await pg.click(radio); await asyncio.sleep(1)
                await pg.click(BTN_OPTIONS); await asyncio.sleep(1)
                for z in (18, 17):
                    for v in ([0] if test else range(0, 11)):
                        await pg.click(BTN_OPTIONS); await asyncio.sleep(0.8)
                        await pg.ev(SET_SHADE % v)
                        await pg.click(BTN_OPTIONS); await asyncio.sleep(0.8)
                        await pg.ev('(window.__maps[window.__maps.length-1].setView([%f,%f],%d,{animate:false}),0)' % (REEF[0], REEF[1], z))
                        await asyncio.sleep(4)
                        fn = '%s_z%d_shade%04.1f.png' % (tag, z, v)
                        await pg.shot(os.path.join(OUTDIR, fn)); log['files'].append(fn)
                        print(fn, flush=True)
    finally:
        ch.close()
    log['finished'] = datetime.datetime.now().isoformat(timespec='seconds')
    if not test:       # a --test run only re-captures the base views and must not overwrite the log of the full capture
        json.dump(log, open(os.path.join(OUTDIR, 'capture_log.json'), 'w'), indent=1)


if __name__ == '__main__':
    asyncio.run(main('--test' in sys.argv))

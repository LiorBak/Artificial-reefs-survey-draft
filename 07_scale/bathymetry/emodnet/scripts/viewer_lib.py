"""Drive the EMODnet Map Viewer (https://emodnet.ec.europa.eu/geoviewer/) in an isolated headless Chrome and return a screenshot plus the exact
Web-Mercator -> screen-pixel mapping (read from the tiles the viewer itself draws).  See METHOD.md 2f."""
import asyncio, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from cdp import Chrome

R = 6378137.0
ORIGIN = 20037508.342789244
HOOK = r"""
window.__tiles=[];
const orig=CanvasRenderingContext2D.prototype.drawImage;
CanvasRenderingContext2D.prototype.drawImage=function(img,...a){
  try{ if(img && img.src && /tiles\.emodnet|server\.arcgisonline|openstreetmap/.test(img.src) && a.length>=8){ const m=this.getTransform(); window.__tiles.push({src:img.src,a:a.slice(0,8),m:[m.a,m.b,m.c,m.d,m.e,m.f]}); if(window.__tiles.length>4000) window.__tiles.splice(0,2000);} }catch(e){}
  return orig.call(this,img,...a);
};
"""

def merc(lat, lon):
    return R * math.radians(lon), R * math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))

def tile_zxy(src):
    m = re.search(r"arcgisonline\.com/.*/tile/(\d+)/(\d+)/(\d+)", src)
    if m: z, row, col = map(int, m.groups()); return z, col, row
    m = re.search(r"tiles\.emodnet-bathymetry\.eu/.*/(\d+)/(\d+)/(\d+)\.png", src)
    if m: z, col, row = map(int, m.groups()); return z, col, row
    return None

def calibrate(tiles, canvas_off):
    """least-squares affine from the corners of the small (<=600 px) tiles drawn last: px = sx*X + ox ; py = sy*Y + oy (page pixels)"""
    import numpy as np
    xs, pxs, ys, pys = [], [], [], []
    for t in tiles[-500:]:
        k = tile_zxy(t["src"])
        if not k: continue
        z, col, row = k; size = 2 * ORIGIN / 2 ** z; dx, dy, dw, dh = t["a"][4:8]
        a_, b_, c_, d_, e_, f_ = t["m"]
        if abs(b_) > 1e-9 or abs(c_) > 1e-9: continue
        px0, py0 = a_ * dx + e_ + canvas_off[0], d_ * dy + f_ + canvas_off[1]; pw, ph = a_ * dw, d_ * dh
        if pw < 20 or pw > 600: continue
        x0 = -ORIGIN + col * size; ytop = ORIGIN - row * size
        xs += [x0, x0 + size]; pxs += [px0, px0 + pw]; ys += [ytop, ytop - size]; pys += [py0, py0 + ph]
    if len(xs) < 8: raise RuntimeError("not enough tiles for calibration")
    X0 = np.mean(xs); Y0 = np.mean(ys)
    sx, ox = np.polyfit(np.array(xs) - X0, pxs, 1); sy, oy = np.polyfit(np.array(ys) - Y0, pys, 1)
    res = (np.array(pxs) - (sx * (np.array(xs) - X0) + ox), np.array(pys) - (sy * (np.array(ys) - Y0) + oy))
    # return mapping in the form px = sx*X + ox' with X in absolute metres
    return (sx, ox - sx * X0, sy, oy - sy * Y0), [float(np.abs(res[0]).max()), float(np.abs(res[1]).max())]

async def capture(site_name, lat_c, lon_c, half_w_m, half_h_m, layers, basemap, opacities, out_png, width=1700, height=1250, wait=22, toggle=True, extra_wait=6):
    c = Chrome(width, height, tag="gv_" + site_name)
    try:
        await c.connect(); await c.enable_config_fix()
        await c.send("Page.addScriptToEvaluateOnNewDocument", {"source": HOOK})
        x, y = merc(lat_c, lon_c)
        f = 1 / math.cos(math.radians(lat_c))          # Web-Mercator metres per ground metre
        hw, hh = half_w_m * f, half_h_m * f
        url = f"https://emodnet.ec.europa.eu/geoviewer/?layers={','.join(str(l) for l in layers)}&basemap={basemap}&bounds={x-hw:.2f},{y-hh:.2f},{x+hw:.2f},{y+hh:.2f}&filters=&projection=EPSG:3857"
        await c.goto(url, wait=wait)
        # close the layer panel (X button) so that the whole map is visible
        await c.click(40, 102); await asyncio.sleep(1.5)
        if toggle:
            for lid in layers:
                await c.js(f"(()=>{{const b=document.querySelector('#layerLi-{lid} button[title=\"Change the visibility of the layer\"]'); if(b&&b.querySelector('.fa-eye-slash')) b.click();}})()")
        for lid, op in zip(layers, opacities):
            await c.js(f"(()=>{{const i=document.querySelector('#layer-opacity-{lid}'); if(i){{i.value={op}; i.dispatchEvent(new Event('input',{{bubbles:true}}));}}}})()")
        await asyncio.sleep(extra_wait)
        # nudge a redraw so that the hook sees final tiles
        await c.send("Emulation.setDeviceMetricsOverride", dict(width=width, height=height + 1, deviceScaleFactor=1, mobile=False)); await asyncio.sleep(1)
        await c.send("Emulation.setDeviceMetricsOverride", dict(width=width, height=height, deviceScaleFactor=1, mobile=False)); await asyncio.sleep(extra_wait)
        rect = await c.js("(()=>{const e=document.querySelector('.ol-viewport'); const r=e.getBoundingClientRect(); return [r.left,r.top,r.width,r.height]})()")
        tiles = json.loads(await c.js("JSON.stringify(window.__tiles.slice(-600))"))
        cal, spread = calibrate(tiles, (rect[0], rect[1]))
        await c.shot(out_png)
        state = await c.js("location.href")
        return dict(cal=cal, spread=list(spread), rect=rect, url=url, n_tiles=len(tiles), tile_requests=[u for u in c.requests() if "emodnet-bathymetry" in u][:6])
    finally:
        await c.close()

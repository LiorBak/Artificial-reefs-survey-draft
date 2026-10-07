"""probe_geometry.py - read the map geometry (container size / rect, projected position of the centre, zoom) of the Garmin marine viewer in our
own headless Chrome, so that screenshot pixels can be converted to ground coordinates (used by nav_read.py).  Writes nav_geometry.json."""
import asyncio, json, os, sys
import capture_navionics as C

async def main():
    ch = C.Chrome()
    out = {}
    try:
        async with C.Page(ch.ws_url) as pg:
            await pg.send('Page.enable'); await pg.send('Page.addScriptToEvaluateOnNewDocument', source=C.HOOK)
            await pg.send('Page.navigate', url=C.URL); await asyncio.sleep(14)
            for z in (18, 17):
                await pg.ev('(window.__maps[window.__maps.length-1].setView([%f,%f],%d,{animate:false}),0)' % (C.REEF[0], C.REEF[1], z)); await asyncio.sleep(3)
                js = """(function(){var m=window.__maps[window.__maps.length-1];var r=m.getContainer().getBoundingClientRect();var p=m.latLngToContainerPoint([%f,%f]);var s=m.getSize();var c=m.getCenter();
                return JSON.stringify({zoom:m.getZoom(),size:[s.x,s.y],rect:[r.left,r.top,r.width,r.height],reef_container_px:[p.x,p.y],center:[c.lat,c.lng],nmaps:window.__maps.length});})()""" % C.REEF
                out['z%d' % z] = json.loads(await pg.ev(js))
            out['clip'] = C.CLIP
    finally:
        ch.close()
    json.dump(out, open(os.path.join(C.HERE, 'nav_geometry.json'), 'w'), indent=1); print(json.dumps(out))
asyncio.run(main())

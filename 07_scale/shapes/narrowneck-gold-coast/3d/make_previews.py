"""make_previews.py - headless Chrome previews of index.html (own Chrome via 04_build/src/qa_cdp.py: random port, fresh profile).
The sandbox cannot reach the jsdelivr CDN, so the preview serves a COPY of index.html whose import map points at the vendored three.js
(04_build/3d/vendor, read-only use). The real index.html is untouched.   Usage: python make_previews.py [name ...]  (default: all)"""
import os, sys, shutil, tempfile, threading, http.server, socketserver, functools, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, '04_build', 'src'))
from qa_cdp import Chrome
VENDOR = os.path.join(ROOT, '04_build', '3d', 'vendor')
SHOTS = {  # name: (hash, file, wait_js_extra)
    'preview_oblique': ('#view=oblique&water=MSL', os.path.join(HERE, 'preview_oblique.png')),
    'preview_plan': ('#view=plan&water=LAT&version=photo_2020-08-08', os.path.join(HERE, 'preview_plan.png')),
    'preview_arm': ('#view=arm&water=MLWS', os.path.join(HERE, 'preview_arm.png')),
    'preview_option2': ('#view=oblique&version=design_option2_2017&water=LAT', os.path.join(HERE, 'preview_option2.png')),
    'preview_methods_panel': ('#tab=t4&view=oblique', os.path.join(HERE, 'preview_methods_panel.png')),
    'preview_versions_info': ('#info=1&view=plan', os.path.join(HERE, 'preview_versions_info.png')),
}
def main(names):
    tmp = tempfile.mkdtemp(prefix='nn3d_serve_')
    html = open(os.path.join(HERE, 'index.html'), encoding='utf-8').read()
    html = re.sub(r'<script type="importmap">.*?</script>', '<script type="importmap">{"imports":{"three":"/vendor/three.module.js","three/addons/":"/vendor/addons/"}}</script>', html, flags=re.S)
    open(os.path.join(tmp, 'index.html'), 'w', encoding='utf-8').write(html)
    for f in ('model.js', 'docs.js'): shutil.copy(os.path.join(HERE, f), os.path.join(tmp, f))
    shutil.copytree(VENDOR, os.path.join(tmp, 'vendor'))
    os.makedirs(os.path.join(tmp, 'vendor', 'addons'), exist_ok=True)
    # the viewer imports three/addons/controls/OrbitControls.js -> /vendor/addons/controls/OrbitControls.js (exists)
    H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=tmp)
    class Q(H.func):
        def log_message(self, *a): pass
    srv = socketserver.TCPServer(('127.0.0.1', 0), functools.partial(Q, directory=tmp)); port = srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    with Chrome(width=1400, height=900) as c:
        for nme in (names or SHOTS):
            h, out = SHOTS[nme]
            c.goto('about:blank', wait=0.3); c.goto('http://127.0.0.1:%d/index.html%s' % (port, h), wait=1.0)
            try: c.wait_for('window.__ready===true', timeout=60)
            except Exception as e: print('NOT READY', nme, e)
            c.pump(2.0); c.screenshot(out); print('wrote', os.path.basename(out))
        print('console errors:', c.errors[:5])
    srv.shutdown(); shutil.rmtree(tmp, ignore_errors=True)
if __name__ == '__main__': main(sys.argv[1:])

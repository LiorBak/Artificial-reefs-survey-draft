"""Headless previews of 3d/index.html with the vendored three.js (CDNs are blocked). Own Chrome (random port, fresh profile) via 04_build/src/qa_cdp.py.
python3 aux/preview.py [hash ...]  -> preview_plan.png, preview_oblique.png (+ panels)"""
import sys, os, shutil, socket, subprocess, tempfile, time, re
sys.path.insert(0, '/home/user/artificial-reef-survey/04_build/src')
from qa_cdp import Chrome
D3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tmp = tempfile.mkdtemp(prefix='cables_prev_')
for f in ('model.js', 'docs.js'): shutil.copy(os.path.join(D3, f), tmp)
os.symlink('/home/user/artificial-reef-survey/04_build/3d/vendor', os.path.join(tmp, 'vendor'))
h = open(os.path.join(D3, 'index.html'), encoding='utf-8').read()
h = re.sub(r'<script type="importmap">.*?</script>', '<script type="importmap">{"imports":{"three":"./vendor/three.module.js","three/addons/":"./vendor/addons/"}}</script>', h, count=1, flags=re.S)
open(os.path.join(tmp, 'index.html'), 'w', encoding='utf-8').write(h)
s = socket.socket(); s.bind(('127.0.0.1', 0)); port = s.getsockname()[1]; s.close()
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(port), '--bind', '127.0.0.1', '--directory', tmp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
shots = {'preview_plan.png': 'view=plan&water=MSL', 'preview_oblique.png': 'view=oblique&water=MSL', 'preview_crest_ve3.png': 'view=crest&water=MSL&ve=3',
         'preview_versions_info.png': 'view=oblique&info=1', 'preview_methods_panel.png': 'view=oblique&tab=t4', 'preview_lowwater.png': 'view=oblique&water=DATUM&ve=2'}
try:
    with Chrome(width=1400, height=900) as c:
        for n_, (out, hh) in enumerate(shots.items()):
            c.goto(f'http://127.0.0.1:{port}/index.html?r={n_}#{hh}', wait=2.5)
            c.wait_for('window.__ready===true', timeout=40)
            c.pump(1.5)
            c.screenshot(os.path.join(D3, out))
            print(out, 'ok')
        print('errors:', c.errors[:5])
finally:
    srv.terminate(); shutil.rmtree(tmp, ignore_errors=True)

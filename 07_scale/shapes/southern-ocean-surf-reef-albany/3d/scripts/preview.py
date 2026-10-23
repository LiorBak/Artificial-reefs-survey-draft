"""preview.py - headless Chrome screenshots of 3d/index.html (own Chrome via 04_build/src/qa_cdp.py, random port, fresh profile)."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..', '..', '04_build', 'src'))
from qa_cdp import Chrome
import subprocess, socket, time
_s = socket.socket(); _s.bind(('127.0.0.1', 0)); PORT = _s.getsockname()[1]; _s.close()
_srv = subprocess.Popen([sys.executable, '-I', '-m', 'http.server', str(PORT), '--bind', '127.0.0.1'], cwd=os.path.abspath(os.path.join(HERE, '..')), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
URL = 'http://127.0.0.1:%d/index.html' % PORT
OUT = os.path.join(HERE, '..')
shots = [('preview_plan.png', '#view=plan&water=MSL'), ('preview_oblique.png', '#view=oblique&water=MSL&ve=2'),
         ('preview_methods_panel.png', '#tab=t4&view=oblique'), ('preview_info_popup.png', '#info=1&view=plan')]
if len(sys.argv) > 1: shots = [s for s in shots if s[0] in sys.argv[1:]]
with Chrome(width=1400, height=900, allow_file_access=True) as c:
    for fn, h in shots:
        c.goto('about:blank'); c.goto(URL + h)
        c.wait_for('window.__ready===true', timeout=40)
        import time; time.sleep(3)
        c.screenshot(os.path.join(OUT, fn))
        print(fn)
_srv.terminate()

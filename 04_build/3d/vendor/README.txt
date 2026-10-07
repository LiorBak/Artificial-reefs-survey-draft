Vendored three.js 0.170.0 (MIT, see LICENSE_three.txt) so the 3D viewers work OFFLINE.
Source: https://registry.npmjs.org/three/-/three-0.170.0.tgz (downloaded 2026-10-06).
Files: three.module.js (build/), addons/controls/OrbitControls.js, addons/renderers/CSS2DRenderer.js (examples/jsm/, unmodified).

three.bundle.js = the three files above bundled as ONE classic (non-module) script that sets
  window.__THREE_BUNDLE = { THREE, OrbitControls, CSS2DRenderer, CSS2DObject }
WHY: Chrome/Edge block ES-module imports from file:// ("origin null" CORS error, tested 2026-10-06), so an import map
pointing at three.module.js only works over http. A classic <script src=...> works from file:// and http alike.
The copied viewers (04_build/3d/<slug>/index.html) keep their inline <script type="module"> but their `import` lines are
replaced by `const THREE = window.__THREE_BUNDLE.THREE; ...` (done by src/compile_models3d.py). Originals in 07_scale/ untouched.

Rebuild the bundle (only needed to change the three.js version):
  entry.js:  import * as THREE from 'three'; import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
             import {CSS2DRenderer, CSS2DObject} from 'three/addons/renderers/CSS2DRenderer.js';
             window.__THREE_BUNDLE = {THREE, OrbitControls, CSS2DRenderer, CSS2DObject};
  npx esbuild entry.js --bundle --format=iife --minify --legal-comments=none --outfile=three.bundle.js
  (with 'three' resolved to build/three.module.js and the addons importing it).
If a new viewer imports another addon, add it to entry.js and rebuild.

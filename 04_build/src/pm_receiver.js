/* "Match this photo" receiver (round 11). Injected by compile_models3d.inject_chrome at the END of each single-model viewer's module script, so it
   sees the viewer's own `camera` and `controls` (module scope). It only listens to its parent page (e.source === window.parent).
   Messages from the page:
     {type:'m3d-camera', mode:'plan', center_m:[x,y], up_m:[ux,uy], width_m, height_m, crop_frac?, image?, opacity?}   canonical metres (the model.js frame)
     {type:'m3d-camera', mode:'reset'}      restore the camera, FOV, limits and panels the viewer had before the first match
     {type:'m3d-camera', mode:'opacity', opacity:0..1}
   Answers: {type:'m3d-camera-state', matched:true|false, dragged?:true}.
   CFG (filled at build time from data/photo_match.json): A = canonical (x, y) -> scene ground (X, Z); shift = canonical -> model frame offset (m). */
;(function () {
  try {
    var CFG = /*PM_CFG*/null;
    if (!CFG || typeof camera === 'undefined' || typeof controls === 'undefined') return;
    var home = null, spec = null, panelsWere = null, FOV = 8;
    function canvasEl() {
      var l = [].slice.call(document.querySelectorAll('canvas')).sort(function (a, b) { return b.clientWidth * b.clientHeight - a.clientWidth * a.clientHeight; });
      return l[0];
    }
    function num(v) { return typeof v === 'number' && isFinite(v); }
    function toScene(x, y) { x += CFG.shift[0]; y += CFG.shift[1]; return [CFG.A[0][0] * x + CFG.A[0][1] * y, CFG.A[1][0] * x + CFG.A[1][1] * y]; }
    function dirScene(x, y) { return [CFG.A[0][0] * x + CFG.A[0][1] * y, CFG.A[1][0] * x + CFG.A[1][1] * y]; }
    function stateFov() { return (typeof state !== 'undefined' && state && typeof state === 'object' && 'fov' in state) ? state : null; }
    function tell(o) { try { window.parent.postMessage(Object.assign({ type: 'm3d-camera-state' }, o), '*'); } catch (e) { /* ignore */ } }
    function saveHome() {
      if (home) return;
      var s = stateFov();
      home = { pos: camera.position.clone(), up: camera.up.clone(), tgt: controls.target.clone(), fov: camera.fov, near: camera.near, far: camera.far,
        minD: controls.minDistance, maxD: controls.maxDistance, minP: controls.minPolarAngle, maxP: controls.maxPolarAngle, sfov: s ? s.fov : null };
    }
    function overlayBox() {
      var b = document.getElementById('m3d-pmo');
      if (!b) {
        b = document.createElement('div'); b.id = 'm3d-pmo'; b.setAttribute('aria-hidden', 'true');
        b.style.cssText = 'position:fixed;pointer-events:none;overflow:hidden;z-index:6;display:none;outline:1px dashed rgba(255,255,255,.55)';
        var im = document.createElement('img'); im.alt = ''; im.style.cssText = 'position:absolute;display:block;max-width:none';
        b.appendChild(im); document.body.appendChild(b);
      }
      return b;
    }
    function layoutOverlay() {
      var b = document.getElementById('m3d-pmo'); if (!b || !spec || !spec.image) return;
      var el = canvasEl(), r = el.getBoundingClientRect(), s = r.height / spec._v;
      var W = spec.width_m * s, H = spec.height_m * s, cr = spec.crop_frac || [0, 0, 1, 1];
      b.style.left = (r.left + r.width / 2 - W / 2) + 'px'; b.style.top = (r.top + r.height / 2 - H / 2) + 'px';
      b.style.width = W + 'px'; b.style.height = H + 'px';
      var im = b.firstChild;
      im.style.width = (W / cr[2]) + 'px'; im.style.height = (H / cr[3]) + 'px'; im.style.left = (-cr[0] * W / cr[2]) + 'px'; im.style.top = (-cr[1] * H / cr[3]) + 'px';
      b.style.display = 'block';
    }
    function place() {
      var d = spec, el = canvasEl(); if (!el || !el.clientWidth || !el.clientHeight) return false;
      var c = toScene(d.center_m[0], d.center_m[1]), u = dirScene(d.up_m[0], d.up_m[1]), n = Math.hypot(u[0], u[1]); u = [u[0] / n, u[1] / n];
      var cw = el.clientWidth, ch = el.clientHeight;
      var v = Math.max(d.height_m, d.width_m * ch / cw);                // vertical ground extent that shows the whole picture
      d._v = v;
      var dist = (v / 2) / Math.tan(FOV * Math.PI / 360);
      var s = stateFov(); if (s) s.fov = FOV;
      camera.fov = FOV; camera.far = Math.max(home.far, dist * 4); camera.near = Math.min(home.near, dist / 200); camera.updateProjectionMatrix();
      controls.minDistance = 0; controls.maxDistance = Infinity; controls.minPolarAngle = 0;
      camera.up.set(0, 1, 0);
      var eps = Math.max(dist * 0.0015, 0.05);                            // the camera sits a hair behind the picture's bottom edge: screen-up = the picture's up
      camera.position.set(c[0] - u[0] * eps, dist, c[1] - u[1] * eps);
      controls.target.set(c[0], 0, c[1]);
      camera.lookAt(controls.target); controls.update();
      layoutOverlay();
      return true;
    }
    function match(d) {
      if (!d || !d.center_m || !d.up_m || !num(d.width_m) || !num(d.height_m) || !num(d.center_m[0]) || !num(d.center_m[1]) || !num(d.up_m[0]) || !num(d.up_m[1])) return;
      saveHome();
      var P = window.__m3dPanels;                                         // an unobstructed canvas: fold the viewer's side panels while matching
      if (P && !panelsWere) {
        panelsWere = { left: P.state.left, right: P.state.right };
        if (document.getElementById('m3d-hide-left')) P.set('left', false);
        if (document.getElementById('m3d-hide-right')) P.set('right', false);
      }
      spec = { center_m: d.center_m, up_m: d.up_m, width_m: d.width_m, height_m: d.height_m, crop_frac: (d.crop_frac && d.crop_frac.length === 4) ? d.crop_frac : null,
        image: (typeof d.image === 'string' && /^(file|https?|blob|data):/i.test(d.image)) ? d.image : '', opacity: num(d.opacity) ? d.opacity : 0.55 };
      var b = overlayBox();
      if (spec.image) { b.firstChild.src = spec.image; b.style.opacity = String(spec.opacity); } else b.style.display = 'none';
      if (place()) tell({ matched: true });
    }
    function reset() {
      if (!home) return;
      spec = null;                                                         // first: restoring the panels fires 'resize', which would re-place the overlay
      camera.position.copy(home.pos); camera.up.copy(home.up); controls.target.copy(home.tgt);
      camera.fov = home.fov; camera.near = home.near; camera.far = home.far; camera.updateProjectionMatrix();
      controls.minDistance = home.minD; controls.maxDistance = home.maxD; controls.minPolarAngle = home.minP; controls.maxPolarAngle = home.maxP;
      var s = stateFov(); if (s && home.sfov !== null) s.fov = home.sfov;
      camera.lookAt(controls.target); controls.update();
      var b = document.getElementById('m3d-pmo'); if (b) b.style.display = 'none';
      var P = window.__m3dPanels;
      if (P && panelsWere) { if (panelsWere.left && document.getElementById('m3d-hide-left')) P.set('left', true); if (panelsWere.right && document.getElementById('m3d-hide-right')) P.set('right', true); }
      panelsWere = null; home = null;
      tell({ matched: false });
    }
    window.addEventListener('message', function (e) {
      if (e.source !== window.parent) return;
      var d = e.data; if (!d || typeof d !== 'object' || d.type !== 'm3d-camera') return;
      if (d.mode === 'plan') match(d);
      else if (d.mode === 'reset') reset();
      else if (d.mode === 'opacity' && num(d.opacity)) { var b = document.getElementById('m3d-pmo'); if (b) b.style.opacity = String(Math.max(0, Math.min(1, d.opacity))); if (spec) spec.opacity = d.opacity; }
    });
    window.addEventListener('resize', function () { if (spec) place(); });
    controls.addEventListener('start', function () {                     // the user moves the camera: the overlay no longer matches
      if (!spec) return;
      var b = document.getElementById('m3d-pmo'); if (b) b.style.display = 'none';
      spec = null; tell({ matched: false, dragged: true });
    });
    function screenOf(x, y) {                                            // test hook: screen pixel (viewport of this document) of the canonical point (x, y) at ground level
      var p = toScene(x, y), v = new camera.position.constructor(p[0], 0, p[1]), r = canvasEl().getBoundingClientRect();
      camera.updateMatrixWorld(); v.project(camera);
      return [r.left + (v.x + 1) / 2 * r.width, r.top + (1 - v.y) / 2 * r.height];
    }
    window.__m3dMatch = { match: match, reset: reset, active: function () { return !!spec; }, screenOf: screenOf };   // test hooks
  } catch (err) { if (window.console) console.warn('photo-match receiver not installed', err); }
})();

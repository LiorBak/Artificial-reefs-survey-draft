/* "3D models" tab. Inlined by build.py (before app.js). Data: <script id="data3d"> = data/models3d.json (src/compile_models3d.py).
   Public API: window.ReefModels3D = { render(), openModel(slug), openPicture(slug, id), select(id), selected(), unloadAll(), setVersion() }.
   app.js calls render() when the view 'models3d' is shown and unloadAll() when it is left; nothing else in the page depends on this file.
   Round 10 layout (Lior's review): a reef SELECTOR at the top (one model shown at a time + "All (compare)", hash #view/models3d/<slug|all>);
   per model: compact header -> STAGE = 3D viewer + PHOTO PANEL side by side (full screen = the whole stage) -> key numbers, methods
   documents (below); at the bottom the APPENDIX (methods, texts relied on, caveats, references). Long texts sit behind (i) pop-overs
   (ReefInfo, app.js) or the appendix ("read more"). */
(function () {
  'use strict';

  var node = document.getElementById('data3d');
  var D = null;
  try { D = node ? JSON.parse(node.textContent) : null; } catch (e) { D = null; }
  var root = document.getElementById('m3d-root');
  if (!D || !root) { window.ReefModels3D = { render: function () {}, openModel: function () {}, openPicture: function () {}, unloadAll: function () {} }; return; }

  var MAX_LIVE = 2;                       // never more than two live WebGL viewers (in practice one: the selected model)
  var HOVER_MQ = window.matchMedia ? window.matchMedia('(hover: hover) and (pointer: fine)') : { matches: true };
  var rendered = false, live = [], tipFor = null, lb = null, lbState = null, vdlg = null, verSel = {};   // verSel: slug -> chosen outline version id
  var sel = null, picSel = {}, picVer = {}, pmState = {}, verLive = {}, fsStage = null, picsOff = false;   // picsOff (round 11): the right-hand panel (photos / "reefs in this scene") is collapsed; open by default, kept across full screen and model switches
  var BY = {}, PIC = {}, SRC = {}, VIEW = {};
  var CMP = D.combined && D.combined.viewer ? D.combined : null;
  D.models.forEach(function (m) {
    BY[m.slug] = m; SRC[m.slug] = {};
    VIEW[m.slug] = { name: m.name, viewer: m.viewer, poster: m.poster };
    (m.sources || []).forEach(function (s) { if (s.id) SRC[m.slug][s.id] = s; });
    // one display order for the strip, the panel arrows and the lightbox: group order, then data order
    var ord = [];
    D.groups.forEach(function (g) { m.gallery.forEach(function (p) { if (p.group === g.key) ord.push(p); }); });
    m.gallery.forEach(function (p) { if (ord.indexOf(p) < 0) ord.push(p); });
    m._ord = ord;
    ord.forEach(function (p, i) { p._i = i; p._slug = m.slug; PIC[m.slug + '|' + p.id] = p; });
  });
  if (CMP) VIEW.all = { name: 'All reefs compared', viewer: CMP.viewer, poster: CMP.poster || '' };

  // ------------------------------------------------------------------ helpers
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function safeUrl(u) { return /^https?:\/\//i.test(String(u || '')) ? String(u) : ''; }
  function ext(u, text) { var s = safeUrl(u); return s ? '<a href="' + esc(s) + '" target="_blank" rel="noopener noreferrer">' + esc(text || s) + '</a>' : ''; }
  function inl(s) { return esc(s).replace(/\*([^*]+)\*/g, '<i>$1</i>'); }
  function linkify(escaped) { return escaped.replace(/(https?:\/\/[^\s<)]+[^\s<).,;])/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'); }
  function $(sel, r) { return (r || document).querySelector(sel); }
  function $all(sel, r) { return Array.prototype.slice.call((r || document).querySelectorAll(sel)); }
  function cap(s) { s = String(s || ''); return s.charAt(0).toUpperCase() + s.slice(1); }
  function cut(s, n) {                    // one-line version of a long text (the full text goes behind an (i))
    s = String(s || '').replace(/\s+/g, ' ').trim();
    if (s.length <= n) return s;
    var i = s.lastIndexOf(' ', n); if (i < n * 0.6) i = n;
    return s.slice(0, i).replace(/[\s,;:.\-]+$/, '') + '…';
  }
  function shortName(m) { return String(m.name).replace(/\s*\(.*$/, '').replace(/:.*$/, '').trim(); }
  function pp(html) { return '<span class="pp">' + html + '</span>'; }
  function info(label, html) { return window.ReefInfo ? window.ReefInfo.html(label, html) : ''; }
  function goLink(href, text) { return '<a class="more" href="' + href + '" data-m3d-goto>' + text + ' &rarr;</a>'; }

  function sidChips(slug, ids) {
    if (!ids) return '';
    return String(ids).split(/;/).map(function (tok) {
      tok = tok.trim(); if (!tok) return '';
      var id = tok.split(/\s+/)[0], s = SRC[slug] && SRC[slug][id];
      if (!s) return '<span class="m3d-sidtxt">' + esc(tok) + '</span> ';
      var tip = (s.citation || '') + (s.url ? ' [' + s.url + ']' : '');
      return '<span class="m3d-sid" tabindex="0" title="' + esc(tip) + '">' + esc(tok) + '</span>';
    }).join('');
  }

  // ------------------------------------------------------------------ outline / model versions (model.js "versions", build_3d_tab.md 2b)
  function hasVers(m) { return !!(m.versions && m.versions.length); }
  function activeVer(m) { return verSel[m.slug] || m.default_version; }
  function verOf(m, id) { return (m.versions || []).filter(function (v) { return v.id === id; })[0]; }
  function fmtN(x, d) { return Number(x).toLocaleString('en-GB', { maximumFractionDigits: d || 0 }); }
  function verSrcHash(m) { return hasVers(m) ? '#version=' + encodeURIComponent(activeVer(m)) : ''; }
  function viewerSrc(slug) { var v = VIEW[slug]; return v ? v.viewer + (BY[slug] ? verSrcHash(BY[slug]) : '') : ''; }
  function versionNowHTML(m) {
    var v = verOf(m, activeVer(m)); if (!v) return '';
    return '<b>Showing:</b> ' + esc(v.name) + (v.id === m.default_version ? ' <span class="m3d-tag dflt">default</span>' : '') +
      (v.level ? ' &mdash; ' + esc(v.level) : '') + (v.method ? '. <span class="m3d-vmeth">' + esc(v.method) + '</span>' : '') + (v.note ? ' <span class="m3d-vmeth">' + esc(v.note) + '</span>' : '');
  }
  function versionBarHTML(m) {
    if (!hasVers(m)) return '';
    var act = activeVer(m), s = esc(m.slug);
    var btns = m.versions.length > 1 ? '<div class="m3d-vgroup" role="group" aria-labelledby="m3d-vlbl-' + s + '">' + m.versions.map(function (v) {
      return '<button type="button" class="m3d-vbtn" data-m3d-ver="' + s + '|' + esc(v.id) + '" aria-pressed="' + (v.id === act) + '"><span class="n">' + esc(v.name) + '</span>' +
        '<span class="d">' + esc(v.date) + (v.id === m.default_version ? ' &middot; default' : '') + '</span></button>';
    }).join('') + '</div>' : '';
    return '<div class="m3d-versions" data-vbar="' + s + '"><div class="m3d-vrow"><span class="lbl" id="m3d-vlbl-' + s + '">Outline version</span>' + btns +
      '<button type="button" class="m3d-vinfo" data-m3d-vinfo="' + s + '" aria-haspopup="dialog" aria-label="About the outline versions of ' + esc(m.name) + '" title="About the outline versions">i</button></div>' +
      '<p class="m3d-vnow" data-vnow="' + s + '" aria-live="polite" title="Click to read the whole text">' + versionNowHTML(m) + '</p></div>';
  }
  // rows of the key-numbers table that depend on the selected version (computed from the version record)
  function versionRows(m, v) {
    var d = verOf(m, m.default_version), ids = (v.source_ids || []).join('; '), rows = [];
    function vs(key, unit) {
      if (!d || d.id === v.id || d[key] == null || v[key] == null || !d[key]) return '';
      var pc = ((v[key] - d[key]) / d[key]) * 100;
      return 'Default (' + d.name + '): ' + fmtN(d[key]) + ' ' + unit + '; this version ' + (pc >= 0 ? '+' : '') + pc.toFixed(0) + ' % relative to it.';
    }
    rows.push({ q: 'Outline version shown', model: v.name + (v.date ? ' (' + v.date + ')' : ''), stated: '-', diff: '-', ids: ids, note: v.level, ver: true });
    if (v.area_m2 != null) rows.push({ q: 'Footprint area (this version)', model: fmtN(v.area_m2) + ' m²', stated: v.stated.area || '-', diff: '-', ids: ids, note: vs('area_m2', 'm²'), ver: true });
    if (v.bbox_m && v.bbox_m[0] != null && v.bbox_m[1] != null) rows.push({ q: 'Footprint bounding box', model: fmtN(v.bbox_m[0], 1) + ' × ' + fmtN(v.bbox_m[1], 1) + ' m', stated: '-', diff: '-', ids: ids, note: '', ver: true });
    if (v.volume_m3 != null) rows.push({ q: 'Reef volume (this version)', model: fmtN(v.volume_m3) + ' m³', stated: v.stated.volume || '-', diff: '-', ids: ids, note: vs('volume_m3', 'm³'), ver: true });
    return rows;
  }
  function rowsFor(m) {
    var act = activeVer(m), base = (m.key_numbers || []).filter(function (r) { return !hasVers(m) || !r.versions || r.versions.indexOf(act) >= 0; }).map(function (r) {
      var o = r.by_version && r.by_version[act]; if (!o) return r;
      var c = {}; Object.keys(r).forEach(function (k) { c[k] = r[k]; }); Object.keys(o).forEach(function (k) { c[k] = o[k]; }); return c;
    });
    return hasVers(m) ? versionRows(m, verOf(m, act)).concat(base) : base;
  }
  function setVersion(slug, id) {
    var m = BY[slug]; if (!m || !verOf(m, id)) return;
    verSel[slug] = id;
    if (pmState[slug]) { delete pmState[slug]; pmRefresh(slug); }          // the viewer re-loads with the new version: a photo match no longer applies
    $all('[data-m3d-ver^="' + slug + '|"]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-m3d-ver') === slug + '|' + id)); });
    var now = $('[data-vnow="' + slug + '"]'); if (now) now.innerHTML = versionNowHTML(m);
    var kn = $('[data-knbody="' + slug + '"]'); if (kn) kn.innerHTML = knInner(m);
    var fs = $('a[data-m3d-full="' + slug + '"]'); if (fs) fs.href = m.viewer + verSrcHash(m);
    var f = $('[data-viewer="' + slug + '"] iframe');           // live viewer: tell it (postMessage, then a hash-only navigation as a fallback)
    if (f) {
      // The viewers read #version=<id> only when they start (none re-reads it later): the live viewer is re-loaded with a cache-busting query (a hash-only change
      // would not reload) and the hash it already has (camera / water / VE are kept in it by the viewers) with the new version. A viewer that switches live
      // announces it with window.M3D_HANDLES_VERSION = true and receives the postMessage only.
      var live3 = false;
      try { f.contentWindow.postMessage({ type: 'm3d-version', version: id }, '*'); } catch (e) { /* viewer not ready: its initial #version= covers it */ }
      live3 = !!verLive[slug];                                   // announced by the viewer: postMessage {type:'m3d-viewer-caps', handlesVersion:true}
      try { if (f.contentWindow.M3D_HANDLES_VERSION) live3 = true; } catch (e) { /* cross-origin (file://): only the announcement counts */ }
      if (live3) f.src = m.viewer + verSrcHash(m);           // hash-only navigation: the viewer re-reads it on hashchange
      else {
        var hh = '';
        try { hh = f.contentWindow.location.hash || ''; } catch (e) { hh = ''; }
        var q = new URLSearchParams(hh.replace(/^#/, '')); q.set('version', id);
        delete verLive[slug];
        f.src = m.viewer + '?r=' + Date.now() + '#' + q.toString();
      }
    }
  }
  function ensureVdlg() {
    if (vdlg) return vdlg;
    vdlg = document.createElement('dialog');
    vdlg.className = 'm3d-lb m3d-vdlg'; vdlg.setAttribute('aria-labelledby', 'm3d-vdlg-h');
    vdlg.innerHTML = '<button type="button" class="m3d-lb-close" data-m3d-vclose aria-label="Close (Esc)">&times;</button><div class="m3d-vdlg-in"></div>';
    document.body.appendChild(vdlg);
    vdlg.addEventListener('click', function (e) { if (e.target === vdlg || e.target.closest('[data-m3d-vclose]')) vdlg.close(); });
    vdlg.addEventListener('close', function () { var f = vdlg._opener; vdlg._opener = null; if (f && document.contains(f)) f.focus({ preventScroll: true }); });
    return vdlg;
  }
  function openVerDlg(slug, opener) {
    var m = BY[slug]; if (!m || !hasVers(m)) return;
    var d = ensureVdlg(), act = activeVer(m);
    var paras = (m.versions_info || '').split(/\n\s*\n/).filter(Boolean).map(function (t) { return '<p>' + inl(t) + '</p>'; }).join('') || '<p class="m3d-note">model.js carries no <code>versions_info</code> text.</p>';
    var rows = m.versions.map(function (v) {
      var srcs = (v.source_text || []).map(function (t, i) { return '<span class="m3d-vsrc">' + esc(t) + '</span> ' + sidChips(slug, (v.source_ids || [])[i] || ''); }).join('<br>') || '-';
      return '<tr' + (v.id === act ? ' class="act"' : '') + '><td class="q">' + esc(v.name) + (v.id === m.default_version ? ' <span class="m3d-tag dflt">default</span>' : '') + (v.id === act ? ' <span class="m3d-tag now">shown</span>' : '') +
        (v.level ? '<small>' + esc(v.level) + '</small>' : '') + '</td><td>' + esc(v.date || '-') + '</td><td>' + srcs + (v.method ? '<small>' + esc(v.method) + '</small>' : '') + '</td>' +
        '<td>' + (v.area_m2 != null ? fmtN(v.area_m2) + ' m²' : '-') + (v.bbox_m && v.bbox_m[0] != null ? '<small>' + fmtN(v.bbox_m[0], 1) + ' × ' + fmtN(v.bbox_m[1], 1) + ' m</small>' : '') + '</td>' +
        '<td>' + (v.volume_m3 != null ? fmtN(v.volume_m3) + ' m³' : 'not computed') + '</td></tr>';
    }).join('');
    $('.m3d-vdlg-in', d).innerHTML = '<h3 id="m3d-vdlg-h">Outline versions: ' + esc(m.name) + '</h3>' + paras +
      '<div class="m3d-tablewrap"><table class="m3d-t m3d-vt"><thead><tr><th>Name</th><th>Date</th><th>Source</th><th>Footprint</th><th>Volume</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
      '<p class="m3d-note">The page opens on the default version. The version buttons in the model header switch the 3D viewer and the key-numbers table together; the caveats table lists how the versions differ.</p>';
    d._opener = opener || null;
    if (d.showModal) d.showModal(); else d.setAttribute('open', '');
  }

  // ------------------------------------------------------------------ viewer + photo panel ("stage")
  function viewerHTML(slug) {
    var v = VIEW[slug], bg = v.poster ? ' style="background-image:url(\'' + esc(v.poster) + '\')"' : '';
    var vs = esc(slug), m = BY[slug];
    return '<div class="m3d-viewer" data-viewer="' + vs + '"><div class="m3d-poster"' + bg + '><div class="m3d-poster-box">' +
      '<button type="button" class="m3d-btn m3d-load" data-m3d-load="' + vs + '">Load 3D model</button>' +
      '<p>The interactive model opens inside the page (three.js, works offline).</p></div></div></div>' +
      '<div class="m3d-viewer-bar"><button type="button" class="m3d-btn ghost" data-m3d-fs="' + vs + '" aria-pressed="false">Full screen</button>' +
      '<a class="m3d-btn ghost" data-m3d-full="' + vs + '" href="' + esc(viewerSrc(slug)) + '" target="_blank" rel="noopener" title="The viewer on its own page, with a link back to this page">Own page &#8599;</a>' +
      '<button type="button" class="m3d-btn ghost" data-m3d-unload="' + vs + '" hidden>Unload viewer</button>' +
      '<span class="grow">' + (m ? 'Files: <code>' + esc(m.viewer) + '</code>' + (m.built ? ' (generated ' + esc(m.built) + ')' : '') : 'Combined scene: <code>' + esc(v.viewer) + '</code>') + '</span></div>';
  }

  function picVersions(p) { return [{ label: 'Original', web: p.web, w: p.w, h: p.h }].concat((p.annotated || []).map(function (a) { return { label: 'Annotated: ' + a.label, web: a.web, w: a.w, h: a.h }; })); }
  // ---- "Match this photo" (round 11): plan-view pictures with a documented transform (data/photo_match.json) rotate / zoom / move the live 3D model onto the picture's footprint
  function pmLabel(m) {
    var how = { georef: 'georeferenced', direct: 'traced outline', icp: 'outline fit', web_mercator_capture_log: 'chart capture log' }[m.method] || m.method;
    var res = m.kind === 'navionics' ? '' : ', outline residual ' + (m.rms_m != null ? Number(m.rms_m).toFixed(m.rms_m < 10 ? 1 : 0) : '?') + ' m';
    return how + res;
  }
  function pmRowHTML(slug, p) {
    var st = pmState[slug], m = p.match;
    if (!m && !st) return '';
    var here = !!(st && m && st.id === p.id);
    var h = '<div class="m3d-pm" data-pm="' + esc(slug) + '">';
    if (m) h += '<button type="button" class="m3d-btn ghost m3d-pm-btn" data-m3d-match="' + esc(p.id) + '" aria-pressed="' + here + '" title="Rotate, zoom and move the live 3D model so that it covers the same ground as this picture (top-down view). The picture appears semi-transparent over the model; dragging the model ends the match.">Match this photo</button>';
    if (st) h += '<span class="m3d-pm-on"><label class="m3d-pm-op">Overlay <input type="range" min="0" max="100" value="' + Math.round(st.opacity * 100) + '" data-m3d-pmop aria-label="Overlay opacity"' + (st.dragged ? ' disabled' : '') + '></label> ' +
      '<button type="button" class="m3d-btn ghost m3d-pm-reset" data-m3d-pmreset title="Back to the view the model had before matching">Reset view</button></span>';
    if (m) h += '<small class="m3d-pm-note">Top-down, ' + (m.width_m >= 100 ? Math.round(m.width_m) : Number(m.width_m).toFixed(0)) + ' &times; ' + (m.height_m >= 100 ? Math.round(m.height_m) : Number(m.height_m).toFixed(0)) + ' m of ground; ' + esc(pmLabel(m)) + '.' +
      (st && st.dragged ? ' <b>View moved: overlay hidden.</b> Match again or Reset view.' : '') + '</small>';
    return h + '</div>';
  }
  function pmFrame(slug) { var f = $('[data-viewer="' + slug + '"] iframe'); return f && f.contentWindow ? f : null; }
  function pmSend(slug, msg) { var f = pmFrame(slug); if (f) { try { f.contentWindow.postMessage(msg, '*'); return true; } catch (e) { /* ignore */ } } return false; }
  function pmRefresh(slug) { var id = picSel[slug] || (BY[slug] && BY[slug]._ord[0].id); if (id) showPic(slug, id, picVer[slug] || 0); }
  function matchPhoto(slug, id) {
    var p = PIC[slug + '|' + id], m = p && p.match; if (!m) return;
    var op = pmState[slug] ? pmState[slug].opacity : 0.55;
    var msg = { type: 'm3d-camera', mode: 'plan', center_m: m.center_m, up_m: m.up_m, rotation_deg: m.rotation_deg, width_m: m.width_m, height_m: m.height_m, crop_frac: m.crop_frac || null,
      image: new URL(p.web, location.href).href, opacity: op };
    var fresh = live.indexOf(slug) < 0;
    if (fresh) load(slug);
    pmState[slug] = { id: id, opacity: op, dragged: false };
    var f = pmFrame(slug) || $('[data-viewer="' + slug + '"] iframe');
    if (fresh && f) f.addEventListener('load', function () { setTimeout(function () { pmSend(slug, msg); }, 700); }, { once: true });
    else pmSend(slug, msg);
    pmRefresh(slug);
    var stg = stageOf(slug); if (stg && !fsStage) { var r = stg.getBoundingClientRect(); if (r.top < 0 || r.top > window.innerHeight * 0.5) stg.scrollIntoView({ block: 'start', behavior: 'smooth' }); }
  }
  function resetMatch(slug) { pmSend(slug, { type: 'm3d-camera', mode: 'reset' }); delete pmState[slug]; pmRefresh(slug); }
  function picInfoHTML(p) {
    var src = [p.citation].filter(Boolean).join(' ');
    var extra = [p.credit && p.credit !== 'not stated' ? 'Credit: ' + p.credit : '', p.date ? 'Image date: ' + p.date : '', p.license ? 'Licence: ' + p.license : ''].filter(Boolean).join(' · ');
    return pp('<b>How it was used:</b> ' + esc(p.how_used || 'not recorded in the registry') + (p.check_values && p.check_values.length ? ' (model values affected: ' + esc(p.check_values.join(', ')) + ')' : '')) +
      (p.pending ? pp('<b>Flagged, not yet checked:</b> ' + esc(p.check_what)) : '') +
      pp('<b>Source:</b> ' + esc(src || 'not stated') + (extra ? ' &mdash; ' + esc(extra) : '')) +
      '<a class="more" href="#" data-m3d-enlarge>Full citation, licence and rights note &rarr;</a>';
  }
  function picMainHTML(m, p, vi) {
    var vers = picVersions(p), v = vers[vi] || vers[0], n = m._ord.length;
    var tg = vers.length > 1 ? '<span class="m3d-pic-toggle" role="group" aria-label="Original or annotated version">' + vers.map(function (x, k) {
      return '<button type="button" data-picver="' + k + '" aria-pressed="' + (vers[k] === v) + '">' + esc(x.label) + '</button>';
    }).join('') + '</span>' : '';
    var meta = [p.kind, p.date && String(p.date).split(' ')[0]].filter(Boolean).join(' · ');
    return '<figure class="m3d-pic-fig"><button type="button" class="m3d-pic-zoom" data-m3d-enlarge title="Enlarge: full citation, licence and rights note" aria-label="Enlarge: ' + esc(p.title) + '">' +
      '<img src="' + esc(v.web) + '" width="' + v.w + '" height="' + v.h + '" alt="' + esc(p.title + (vi ? ' (annotated)' : '')) + '"></button></figure>' +
      '<div class="m3d-pic-bar"><button type="button" class="m3d-pic-nav" data-picnav="-1" aria-label="Previous picture" title="Previous picture">&larr;</button>' +
      '<span class="m3d-pic-count">' + (p._i + 1) + ' / ' + n + '</span><button type="button" class="m3d-pic-nav" data-picnav="1" aria-label="Next picture" title="Next picture">&rarr;</button>' +
      tg + '<span class="grow"></span>' + info('Details of this picture: how it was used and its source', picInfoHTML(p)) +
      (p.pending ? '<span class="m3d-tag pend">check pending</span>' : '') + '</div>' + (vi ? '' : pmRowHTML(p._slug, p)) +
      '<p class="m3d-pic-cap"><b>' + esc(p.title) + '</b>' + (meta ? ' <span class="mt">' + esc(meta) + '</span>' : '') + '<span class="how">' + esc(cut(p.how_used || '', 210)) + '</span></p>';
  }
  function thumbHTML(p) {
    var tags = (p.pending ? '<span class="m3d-tag pend" title="check pending">!</span>' : '') + (p.annotated.length ? '<span class="m3d-tag" title="has an annotated version">+</span>' : '');
    return '<button type="button" class="m3d-tile m3d-th" data-pic="' + esc(p._slug + '|' + p.id) + '" aria-pressed="false" aria-label="' + esc(p.title) + '. Shows how it was used on hover or focus; press to show it next to the model.">' +
      '<span class="tags">' + tags + '</span><img src="' + esc(p.thumb) + '" width="' + (p.tw || 400) + '" height="' + (p.th || 300) + '" loading="lazy" decoding="async" alt=""></button>';
  }
  function picsHTML(m) {
    var s = esc(m.slug);
    if (!m._ord.length) return '<aside class="m3d-pics" data-pics="' + s + '"><p class="m3d-note">No registered pictures were selected for this model.</p></aside>';
    var first = m._ord[0];
    var groups = D.groups.map(function (g) {
      var items = m._ord.filter(function (p) { return p.group === g.key; });
      if (!items.length) return '';
      return '<div class="m3d-sgroup"><h4 title="' + esc(g.blurb) + '">' + esc(g.label) + ' <span>(' + items.length + ')</span></h4><div class="m3d-thumbs">' + items.map(thumbHTML).join('') + '</div></div>';
    }).join('');
    return '<aside class="m3d-pics" data-pics="' + s + '" aria-label="Pictures used to construct this model"><div class="m3d-pic-main" data-picmain="' + s + '">' + picMainHTML(m, first, 0) + '</div>' +
      '<div class="m3d-pic-strip"><h3 class="m3d-pic-h">Pictures used to construct this model (' + m._ord.length + ')' +
      info('About these pictures', pp('Click a thumbnail to show it next to the 3D model. Hover or focus one for <b>how it was used</b> and its <b>source</b>; the (i) beside the large picture holds the same text, and <i>Enlarge</i> opens the full citation, licence and rights note.') +
        pp('All are private research copies: reuse rights are not cleared.')) + '</h3>' + groups + '</div></aside>';
  }
  function showPic(slug, id, vi) {
    var m = BY[slug], p = PIC[slug + '|' + id]; if (!m || !p) return;
    picSel[slug] = id; picVer[slug] = vi || 0;
    var box = $('[data-picmain="' + slug + '"]'); if (box) box.innerHTML = picMainHTML(m, p, vi || 0);
    var cur = null;
    $all('[data-pics="' + slug + '"] .m3d-th').forEach(function (b) { var on = b.getAttribute('data-pic') === slug + '|' + id; b.setAttribute('aria-pressed', String(on)); if (on) cur = b; });
    var strip = cur && cur.closest('.m3d-pic-strip');
    if (strip && strip.scrollHeight > strip.clientHeight) {          // keep the chosen thumbnail visible without scrolling the page
      var tr = cur.getBoundingClientRect(), sr = strip.getBoundingClientRect();
      if (tr.top < sr.top) strip.scrollTop -= (sr.top - tr.top) + 6; else if (tr.bottom > sr.bottom) strip.scrollTop += (tr.bottom - sr.bottom) + 6;
    }
  }
  function stepPic(slug, dir) {
    var m = BY[slug], p = PIC[slug + '|' + (picSel[slug] || m._ord[0].id)], n = m._ord.length;
    showPic(slug, m._ord[(p._i + dir + n) % n].id, 0);
  }

  // comparison panel of the combined view (replaces the photo panel)
  function cmpAsideHTML() {
    var rows = CMP.models.map(function (c) {
      var m = BY[c.slug], nm = m ? shortName(m) : c.name;
      if (c.status !== 'ok') return '<tr class="no"><td class="q">' + esc(nm) + '</td><td colspan="4">Not in comparison: ' + esc(c.reason || 'not exported') + '</td></tr>';
      return '<tr><td class="q"><span class="m3d-dot m3d-dot-' + esc(c.level) + '" aria-hidden="true"></span>' + esc(nm) + '<small>3D confidence: ' + esc(c.level) + '</small></td>' +
        '<td>' + fmtN(c.area_m2) + '<small>model.js ' + fmtN(c.area_ref_m2) + '</small></td><td>' + (c.crest_z_m > 0 ? '+' : '') + Number(c.crest_z_m).toFixed(2) + '<small>model.js ' + (c.crest_ref_m > 0 ? '+' : '') + Number(c.crest_ref_m).toFixed(2) + '</small></td>' +
        '<td>' + (c.bbox_m ? fmtN(c.bbox_m[0]) + ' × ' + fmtN(c.bbox_m[1]) : '-') + '</td><td><span class="m3d-status ' + (c.ok ? 'resolved' : 'unresolved') + '">' + (c.ok ? 'matches' : 'check') + '</span></td></tr>';
    }).join('');
    return '<aside class="m3d-pics m3d-cmp" data-pics="all" aria-label="Comparison of the reefs in the combined scene"><div class="m3d-cmp-in"><h3 class="m3d-pic-h">The reefs in this scene' +
      info('How to read the combined scene', pp('Every reef is drawn from its own 3D model at <b>one common scale</b>, side by side along a shared shoreline (offshore is towards the viewer in the plan view). Height 0 is each site’s own mean sea level; the depth colours use one scale for all.') +
        pp('<b>Overlay</b> stacks every reef on one origin (centred on its footprint, shore-normal to the same axis) to compare footprints. The vertical-exaggeration slider acts on all reefs together and always shows its value; true heights are 1x.') +
        goLink('#m3d-all-method', 'How the scene is built and checked')) + '</h3>' +
      '<div class="m3d-tablewrap"><table class="m3d-t m3d-cmpt"><thead><tr><th>Reef</th><th>Footprint (m&sup2;)</th><th>Crest z (m MSL)</th><th>Extent along &times; off shore (m)</th><th>Check</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
      '<p class="m3d-note">Footprint and crest are read back from the exported meshes and compared with the model.js values (tolerances in the method section below). Click a reef name in the viewer legend to fly to it.</p></div></aside>';
  }

  // ------------------------------------------------------------------ one model
  function confInfoHTML(m) {
    var c = m.confidence;
    return info('Confidence, vertical exaggeration and state: ' + shortName(m),
      pp('<b>3D confidence: ' + esc(c.level) + '.</b> ' + esc(c.reason || c.reason_short)) +
      pp('<b>State modelled.</b> ' + esc(m.state_full || m.state_short) + (m.built ? ' (model generated ' + esc(m.built) + ')' : '')) +
      pp('<b>Vertical exaggeration.</b> ' + esc(D.ve_generic) + (m.ve_note ? ' ' + esc(m.ve_note) : '')) +
      goLink('#m3d-methods', 'Appendix A: methods and the confidence rubric (section 8)'));
  }
  function headerHTML(m) {
    var c = m.confidence, lvl = c.level, s = esc(m.slug);
    // one line each: the full text stays in the DOM (CSS ellipsis) and sits behind the (i)
    return '<header class="m3d-mhead"><h2 id="m3d-h-' + s + '" tabindex="-1">' + (m.flag ? '<span class="flag" aria-hidden="true">' + m.flag + '</span> ' : '') + esc(m.name) +
      '<small>' + esc(m.place) + (m.verdict_label ? ' &middot; verdict: ' + esc(m.verdict_label) : '') + '</small></h2>' +
      '<div class="m3d-conf m3d-conf-' + esc(lvl) + '"><span class="m3d-badge" title="3D confidence rubric: Appendix A, section 8">3D confidence: ' + esc(lvl) + '</span>' +
      '<span class="m3d-reason" title="' + esc(c.reason_short || c.reason) + '">' + esc(c.reason_short || c.reason) + '</span>' + confInfoHTML(m) + '</div>' +
      '<p class="m3d-state"><b>State modelled:</b> <span class="t" title="' + esc(m.state_short) + '">' + esc(m.state_short) + '</span><span class="m3d-ve">Vertical exaggeration 1&times; by default</span></p></header>';
  }

  function knNotesHTML(m) {
    return info('How to read the key numbers', pp('Model value, the value stated in the sources, and the difference, for each quantity that fixes the shape. Hover a source id for its citation.') +
      pp('Heights are metres relative to the model zero (mean sea level, MSL) unless a datum is named; &quot;below LAT&quot; means below lowest astronomical tide.') +
      (hasVers(m) ? pp('Shaded rows belong to the selected outline version; the other rows apply to every version unless a row says otherwise.') : '') +
      goLink('#m3d-caveats', 'Appendix C: caveats and discrepancies'));
  }
  function knInner(m) {
    var rows = rowsFor(m);
    var head = '<table class="m3d-t m3d-kn"><thead><tr><th>Quantity</th><th>Model (this reconstruction)</th><th>Stated in sources</th><th>Difference (model - stated)</th><th>Source ids</th></tr></thead><tbody>';
    var body = rows.map(function (r) {
      return '<tr' + (r.ver ? ' class="ver"' : '') + '><td class="q">' + esc(r.q) + (r.note ? '<small>' + esc(r.note) + '</small>' : '') + '</td><td>' + esc(r.model) + '</td><td>' + esc(r.stated || '-') + '</td><td class="diff">' + esc(r.diff || '-') + '</td><td>' + sidChips(m.slug, r.ids) + '</td></tr>';
    }).join('');
    var lv = (m.tides && m.tides.levels) || [];
    var allSame = lv.length > 0 && lv.every(function (l) { return l.src === lv[0].src; }) && !SRC[m.slug][String(lv[0].src).split(/\s+/)[0]];
    var tides = lv.map(function (l) {
      return '<tr><td>' + esc(l.id) + '</td><td>' + esc(l.label) + '</td><td class="z">' + (l.z > 0 ? '+' : '') + Number(l.z).toFixed(2) + '</td>' + (allSame ? '' : '<td>' + sidChips(m.slug, l.src) + '</td>') + '</tr>';
    }).join('');
    var tideSrc = allSame;
    return '<div class="m3d-tablewrap">' + head + body + '</tbody></table></div>' +
      (m.key_numbers_curated ? '' : '<p class="m3d-note">Auto-selected from the model.js provenance table (not yet curated into a model-versus-source comparison).</p>') +
      (tides ? '<h4 style="margin:16px 0 6px">Local tide levels used</h4><div class="m3d-tablewrap"><table class="m3d-t m3d-tides"><thead><tr><th>Level</th><th>Name</th><th>z (m rel. MSL)</th>' + (allSame ? '' : '<th>Source</th>') + '</tr></thead><tbody>' + tides + '</tbody></table></div>' +
        (m.tides.note ? '<p class="m3d-note">' + esc(m.tides.note) + '</p>' : '') +
        (tideSrc ? '<p class="m3d-note">Source of the levels: ' + esc((m.tides.levels[0].src || '')) + '</p>' : '') : '');
  }
  function keyNumbersHTML(m) {
    return '<h3 class="m3d-h3" id="m3d-' + esc(m.slug) + '-kn">Key numbers: model vs stated in the sources' + knNotesHTML(m) + '</h3><div data-knbody="' + esc(m.slug) + '">' + knInner(m) + '</div>';
  }

  function docsHTML(m) {
    var s = '<h3 class="m3d-h3">Methods, sources &amp; uncertainty' + info('About these documents', pp('Rendered from the model folder (<code>07_scale/shapes/' + esc(m.slug) + '/3d/</code>). Each section opens on demand.') + goLink('#m3d-methods', 'Project-wide methods (Appendix A)')) + '</h3>';
    if (m.docs.methods) s += '<details class="m3d-det" data-doc="methods" data-slug="' + esc(m.slug) + '" id="m3d-' + esc(m.slug) + '-methods"><summary>Methods, validation, uncertainty and confidence (METHODS_3D.md)</summary><div class="m3d-doc"></div></details>';
    if (m.docs.sources) s += '<details class="m3d-det" data-doc="sources" data-slug="' + esc(m.slug) + '"><summary>Source log: what was read where (SOURCES_3D.md)</summary><div class="m3d-doc"></div></details>';
    s += '<details class="m3d-det" data-doc="prov" data-slug="' + esc(m.slug) + '"><summary>Provenance of every model parameter (model.js, ' + (m.provenance || []).length + ' rows)</summary><div class="m3d-doc"></div></details>';
    if (m.docs.requests) s += '<details class="m3d-det" data-doc="requests" data-slug="' + esc(m.slug) + '"><summary>Open questions: what would resolve them (REQUESTS_FOR_LIOR.md)</summary><div class="m3d-doc"></div></details>';
    return s;
  }

  function refChips(m) {
    if (!m.ref_ids || !m.ref_ids.length) return '';
    var map = {}; D.references.forEach(function (r) { map[r.id] = r; });
    return '<p class="m3d-refchips"><b>References used by this model</b> (' + m.ref_ids.length + '; list in Appendix D): ' + m.ref_ids.map(function (id) {
      var r = map[id]; var n = id.replace('ref', '');
      return '<a href="#m3d-ref-' + id + '" data-m3d-ref title="' + esc((r.text || '').replace(/\*/g, '').slice(0, 160)) + '">' + n + '</a>';
    }).join(' ') + '</p>';
  }

  function stageHTML(slug, aside) {
    var lab = slug === 'all' ? 'Reefs' : 'Photos', what = slug === 'all' ? 'the reefs panel' : 'the photo panel';
    var bar = '<div class="m3d-pcol-bar"><button type="button" class="m3d-pcol" data-m3d-pcol aria-expanded="true" title="Hide ' + what + ' (a &quot;' + lab + '&quot; button stays at the edge)">Hide &#9656;</button></div>';
    aside = aside.replace(/^(<aside[^>]*>)/, '$1' + bar);
    return '<div class="m3d-stage' + (picsOff ? ' pics-off' : '') + '" data-stage="' + esc(slug) + '"><div class="m3d-sv">' + viewerHTML(slug) + '</div>' + aside +
      '<button type="button" class="m3d-pcol m3d-pcol-open" data-m3d-pcol aria-expanded="' + String(!picsOff) + '" title="Show ' + what + '">' + lab + ' &#9656;</button>' +
      '<button type="button" class="m3d-exitfs" data-m3d-exitfs aria-label="Exit full screen (Esc)">&times; Exit full screen</button></div>';
  }
  function setPics(open) {                              // round 11: collapse / open the right-hand panel of every stage (the choice stays when full screen is entered or left)
    picsOff = !open;
    $all('.m3d-stage').forEach(function (st) {
      st.classList.toggle('pics-off', picsOff);
      $all('[data-m3d-pcol]', st).forEach(function (b) { b.setAttribute('aria-expanded', String(!picsOff)); });
    });
    try { window.dispatchEvent(new Event('resize')); } catch (e) { /* ignore */ }
  }
  function modelHTML(m) {
    return '<section class="m3d-model" id="m3d-' + esc(m.slug) + '" data-slug="' + esc(m.slug) + '" aria-labelledby="m3d-h-' + esc(m.slug) + '" hidden>' +
      headerHTML(m) + versionBarHTML(m) + stageHTML(m.slug, picsHTML(m)) +
      '<div class="m3d-below">' + keyNumbersHTML(m) + docsHTML(m) + refChips(m) + '</div></section>';
  }

  // ------------------------------------------------------------------ the combined ("All (compare)") section
  function allHTML() {
    if (!CMP) return '';
    var ok = CMP.models.filter(function (c) { return c.status === 'ok'; }), no = CMP.models.filter(function (c) { return c.status !== 'ok'; });
    var chk = CMP.models.map(function (c) {
      if (c.status !== 'ok') return '<tr><td class="q">' + esc(c.name) + '</td><td colspan="6">Not exported: ' + esc(c.reason || '') + '</td></tr>';
      return '<tr><td class="q">' + esc(c.name) + '</td><td>' + fmtN(c.area_m2, 1) + '</td><td>' + fmtN(c.area_ref_m2, 1) + '</td><td>' + (c.area_rel_err * 100).toFixed(1) + ' %</td><td>' + Number(c.crest_z_m).toFixed(2) + ' / ' + Number(c.crest_ref_m).toFixed(2) + '</td><td>' + Number(c.crest_err_m).toFixed(2) + ' m</td><td><span class="m3d-status ' + (c.ok ? 'resolved' : 'unresolved') + '">' + (c.ok ? 'pass' : 'FAIL') + '</span></td></tr>';
    }).join('');
    return '<section class="m3d-model m3d-all" id="m3d-all" data-slug="all" aria-labelledby="m3d-h-all" hidden>' +
      '<header class="m3d-mhead"><h2 id="m3d-h-all" tabindex="-1">All reefs compared<small>' + ok.length + ' models at one scale' + (no.length ? ' &middot; ' + no.length + ' not in comparison' : '') + '</small></h2>' +
      '<p class="m3d-sub">Every built model in <b>one scene, same scale</b>, along a shared shoreline; use <b>Overlay</b> in the viewer to stack them on one origin.' +
      info('About the combined scene', pp('Each reef keeps its own seabed patch and its own mean-sea-level zero. The geometry is read from each model’s own viewer at build time (not redrawn), then rotated so that offshore points the same way; nothing is mirrored or rescaled.') +
        pp('Confidence differs per reef: the label of each reef carries its 3D confidence. Only the default outline version of each model is shown.') + goLink('#m3d-all-method', 'Method and checks')) + '</p></header>' +
      stageHTML('all', cmpAsideHTML()) +
      '<div class="m3d-below" id="m3d-all-method"><h3 class="m3d-h3">How the combined scene is made, and the checks</h3><div class="m3d-doc m3d-note-block">' + (CMP.method_html || '') + '</div>' +
      '<div class="m3d-tablewrap"><table class="m3d-t m3d-chk"><thead><tr><th>Reef</th><th>Footprint area, exported mesh (m&sup2;)</th><th>Footprint area, model.js (m&sup2;)</th><th>Difference</th><th>Crest z exported / model.js (m MSL)</th><th>Difference</th><th>Result</th></tr></thead><tbody>' + chk + '</tbody></table></div>' +
      '<p class="m3d-note">' + esc(CMP.tolerance_text || '') + '</p></div></section>';
  }

  // ------------------------------------------------------------------ bottom of the tab: appendix
  function appSec(id, title, bodyHTML) {
    return '<details class="m3d-det m3d-appdet" id="' + id + '"><summary>' + title + '</summary><div class="m3d-appbody">' + bodyHTML + '</div></details>';
  }
  function reliedHTML() {
    var out = '<p class="m3d-note">The sentences that fix crest, height, volume, dates and state of each model (at most 25 words each, with page and link). Every quotation is verified verbatim against the model\'s own documents when the page is built.</p>';
    D.models.forEach(function (m) {
      if (!m.relied || !m.relied.length) return;
      out += '<h4>' + esc(m.name) + '</h4>' + m.relied.map(function (q) {
        return '<blockquote class="m3d-quote"><q>' + esc(q.quote) + '</q><span class="w">' + esc(q.where) + ' &mdash; fixes: ' + esc(q.supports) + (safeUrl(q.url) ? ' · ' + ext(q.url, 'link') : '') + '</span></blockquote>';
      }).join('');
    });
    return out;
  }

  function caveatsHTML() {
    var rows = [];
    D.models.forEach(function (m) { (m.caveats || []).forEach(function (c) { rows.push({ m: m, c: c }); }); });
    var opts = '<option value="">All models</option>' + D.models.map(function (m) { return '<option value="' + esc(m.slug) + '">' + esc(m.name) + '</option>'; }).join('');
    var body = rows.map(function (r) {
      var c = r.c, m = r.m, st = c.auto ? 'auto' : (c.status || 'open'), sec = (c.section || '').match(/\d+(?:\.\d+)*/);
      return '<tr data-slug="' + esc(m.slug) + '"' + (c.origin === 'versions' ? ' class="ver" data-origin="versions"' : '') + '><td class="slug">' + esc(m.name) + '</td><td>' + esc(c.q) + '</td><td>' + esc(c.model) + '</td><td>' + esc(c.stated) + '<br>' + sidChips(m.slug, c.ids) + '</td><td>' + esc(c.diff || '') + '</td><td>' + esc(c.reason || '') + '</td><td><span class="m3d-status ' + esc(st) + '">' + esc(st) + '</span><br>' + esc(c.resolve || '') +
        (sec && m.docs.methods ? '<br><a href="#m3d-' + esc(m.slug) + '-m-' + sec[0].replace(/\./g, '-') + '" data-m3d-goto>METHODS_3D ' + esc(c.section) + '</a>' : '') + '</td></tr>';
    }).join('');
    return '<p class="m3d-note">One row per discrepancy between a model and a stated figure, or per unresolved assumption. ' + esc(D.caveats_note) + ' Status: <b>unresolved</b> = a stated number the model does not reproduce; <b>open</b> = needs a datum, survey or reading we do not have; <b>by-design</b> = a deliberate simplification or a different state; <b>resolved</b> = checked and reconciled.</p>' +
      '<div class="m3d-cav-filter"><label>Show <select id="m3d-cav-sel">' + opts + '</select></label><span id="m3d-cav-count">' + rows.length + ' rows</span></div>' +
      '<div class="m3d-tablewrap"><table class="m3d-t m3d-cav"><thead><tr><th>Model</th><th>Quantity</th><th>Our model</th><th>Stated in source (citation)</th><th>Difference</th><th>Likely reason</th><th>Status / what would resolve it</th></tr></thead><tbody>' + body + '</tbody></table></div>';
  }

  function refsHTML() {
    var names = {}; D.models.forEach(function (m) { names[m.slug] = m.name; });
    var li = D.references.map(function (r) {
      var by = r.cited_by.map(function (s) { return esc(names[s] || s); }).join(', ');
      return '<li id="m3d-ref-' + r.id + '" value="' + r.id.replace('ref', '') + '">' + linkify(inl(r.text)) + '<span class="by">Cited by: ' + by + '</span></li>';
    }).join('');
    return '<p class="m3d-note">One merged, de-duplicated author-year list from the References sections of every METHODS_3D.md and the bathymetry reports (' + D.references.length + ' entries). Where two documents cite the same work with different details, the fuller entry is kept. Each model section links to its entries.</p><ol class="m3d-refs">' + li + '</ol>';
  }

  function applicationHTML() {
    return '<section class="m3d-app" id="m3d-app" aria-labelledby="m3d-app-h"><h2 id="m3d-app-h" tabindex="-1">Appendix: methods, texts relied on, caveats and references</h2>' +
      '<p class="m3d-note">The detail behind the pictures and numbers above. Each part opens on demand; the (i) buttons and &ldquo;read more&rdquo; links lead here.</p>' +
      '<ul class="m3d-jump"><li><a href="#m3d-methods" data-m3d-goto>A. Methods</a></li><li><a href="#m3d-relied" data-m3d-goto>B. Texts relied on</a></li><li><a href="#m3d-caveats" data-m3d-goto>C. Caveats &amp; discrepancies</a></li><li><a href="#m3d-refs" data-m3d-goto>D. References</a></li></ul>' +
      appSec('m3d-methods', 'A. Methods (project-wide)', '<div class="m3d-doc">' + D.methods_html + '</div>') +
      appSec('m3d-relied', 'B. Texts we relied on', reliedHTML()) +
      appSec('m3d-caveats', 'C. Caveats and discrepancies', caveatsHTML()) +
      appSec('m3d-refs', 'D. References (' + D.references.length + ')', refsHTML()) + '</section>';
  }

  // ------------------------------------------------------------------ intro + selector (top of the tab)
  function introHTML() {
    var n = D.models.length, notyet = D.not_yet.length + D.feasibility.length;
    return '<div class="m3d-intro">' +
      '<p class="m3d-lead"><b>3D models of the built reefs:</b> reconstructions from drawings, charts, surveys and text, <b>not surveys of the structures</b>. Pick a reef, or compare them all.' +
      info('About the 3D models',
        pp('Each model is a reconstruction. ' + n + ' reef' + (n === 1 ? ' is' : 's are') + ' modelled so far' + (notyet ? '; ' + notyet + ' more are not yet modelled (listed after the models)' : '') + '. For every model the state shown, the 3D confidence with its reason, and the vertical exaggeration are stated.') +
        pp('Below the model and pictures: the key numbers set against the figures stated in the sources and the full methods documents. At the bottom: the project-wide methods, the texts relied on, the caveats and the references.') +
        pp('Confidence: <span class="m3d-conf-high"><span class="m3d-badge">high</span></span> <span class="m3d-conf-medium"><span class="m3d-badge">medium</span></span> <span class="m3d-conf-low"><span class="m3d-badge">low</span></span> (rubric: Appendix A, section 8). Plan-shape confidence (Scale tab) is a separate rating.') +
        goLink('#m3d-app', 'Read more: Appendix')) +
      ' <a class="m3d-applink" href="#m3d-app" data-m3d-goto>Appendix &darr;</a></p></div>';
  }
  function showSelected(smooth) {                         // bring the chosen model's header + stage under the sticky bars
    var el = sel && document.getElementById('m3d-' + sel); if (!el) return;
    var top = el.getBoundingClientRect().top + window.pageYOffset - ((document.getElementById('topnav') || { offsetHeight: 0 }).offsetHeight) - ((document.getElementById('m3d-selwrap') || { offsetHeight: 0 }).offsetHeight) - 8;
    window.scrollTo(0, Math.max(0, top));
  }
  function selectorHTML() {
    var btn = D.models.map(function (m) {
      var lvl = m.confidence.level;
      return '<button type="button" class="m3d-selbtn" data-m3d-sel="' + esc(m.slug) + '" aria-pressed="false" title="' + esc(m.name + ' - 3D confidence: ' + lvl) + '"><span class="m3d-dot m3d-dot-' + esc(lvl) + '" aria-hidden="true"></span><span class="nm">' + esc(shortName(m)) + '</span><span class="sr"> (3D confidence ' + esc(lvl) + ')</span></button>';
    }).join('');
    if (CMP) btn += '<button type="button" class="m3d-selbtn all" data-m3d-sel="all" aria-pressed="false" title="All built models in one scene at the same scale"><span class="nm">All (compare)</span></button>';
    return '<div class="m3d-selwrap" id="m3d-selwrap"><span class="lbl" id="m3d-sellbl">Reef</span><div class="m3d-sel" role="group" aria-labelledby="m3d-sellbl">' + btn + '</div>' +
      '<span class="m3d-selhint">dot = 3D confidence: <span class="m3d-dot m3d-dot-high"></span>high <span class="m3d-dot m3d-dot-medium"></span>medium <span class="m3d-dot m3d-dot-low"></span>low</span></div>';
  }

  function notModelledHTML() {
    var out = '';
    D.feasibility.forEach(function (f) {
      out += '<article class="m3d-feas" id="m3d-' + esc(f.slug) + '"><h3>' + esc(f.name) + ': not modelled</h3><p>' + esc(f.summary) + '</p><details class="m3d-det" data-doc="feas" data-slug="' + esc(f.slug) + '"><summary>Why, and what is missing (FEASIBILITY.md)</summary><div class="m3d-doc"></div></details></article>';
    });
    if (D.not_yet.length) {
      out += '<div class="m3d-not"><h3>Not yet modelled</h3><ul>' + D.not_yet.map(function (r) { return '<li>' + esc(r.name) + ' &mdash; not yet modelled' + (r.note ? ' (' + esc(r.note) + ')' : '') + '</li>'; }).join('') + '</ul></div>';
    }
    return out;
  }

  // ------------------------------------------------------------------ render + selection
  function render() {
    if (!rendered) {
      root.innerHTML = '<div class="m3d">' + introHTML() + selectorHTML() + D.models.map(modelHTML).join('') + allHTML() + notModelledHTML() + applicationHTML() + '</div>';
      rendered = true;
      bindOnce();
    }
    applyHash();
  }
  function firstId() { return D.models.length ? D.models[0].slug : null; }
  function validId(id) { return id === 'all' ? !!CMP : !!BY[id]; }
  function hashId() { var m = /^#view\/models3d(?:\/([a-z0-9-]+))?$/.exec(location.hash); return m ? (m[1] || '') : null; }
  function applyHash() {
    var h = hashId(); if (h === null) return;           // another view's hash
    var want = validId(h) ? h : (sel && validId(sel) ? sel : firstId());
    if (want !== h) { try { history.replaceState(null, '', '#view/models3d/' + want); } catch (e) { /* file:// quirks */ } }
    if (want !== sel) select(want);
  }
  var userPick = false;
  function go(id) {                                      // user choice: select now, and the URL hash follows it (so Back / deep links work)
    if (!validId(id)) return;
    var h = '#view/models3d/' + id;
    if (id === sel && location.hash === h) { showSelected(); return; }
    userPick = true;
    select(id);
    if (location.hash !== h) location.hash = h;           // its hashchange finds the model already selected
  }
  function select(id) {
    if (!validId(id)) id = firstId();
    if (!id) return;
    var prev = sel; sel = id;
    if (fsStage && fsStage.getAttribute('data-stage') !== id) exitFs();
    $all('section.m3d-model').forEach(function (s) { s.hidden = s.getAttribute('data-slug') !== id; });
    $all('[data-m3d-sel]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-m3d-sel') === id)); });
    live.slice().forEach(function (s) { if (s !== id) unload(s); });
    hideTip();
    if (prev !== id) load(id);                           // one model at a time: its viewer starts when it is shown
    if (userPick) { userPick = false; showSelected(); }  // a deliberate choice: show the model from its header down
  }

  function scrollToId(id, flash) {
    var el = document.getElementById(id);
    if (!el) return false;
    var d = el.parentElement && el.parentElement.closest('details'); while (d) { d.open = true; d = d.parentElement && d.parentElement.closest('details'); }
    if (el.tagName === 'DETAILS') { el.open = true; if (el.getAttribute('data-doc')) fillDoc(el); }
    el.scrollIntoView({ block: 'start', behavior: 'auto' });
    if (flash) { el.classList.add('m3d-flash'); setTimeout(function () { el.classList.remove('m3d-flash'); }, 1800); }
    return true;
  }

  // ------------------------------------------------------------------ lazy documents
  function fillDoc(det) {
    if (!det || det.getAttribute('data-filled') || !det.getAttribute('data-doc')) return;
    var slug = det.getAttribute('data-slug'), kind = det.getAttribute('data-doc'), box = $('.m3d-doc', det), m = BY[slug], html = '';
    if (kind === 'methods') html = m.methods_html;
    else if (kind === 'sources') html = m.sources_html;
    else if (kind === 'requests') html = m.requests_html;
    else if (kind === 'feas') { var f = D.feasibility.filter(function (x) { return x.slug === slug; })[0]; html = f ? f.html : ''; }
    else if (kind === 'prov') {
      html = '<div class="m3d-tablewrap"><table class="m3d-t"><thead><tr><th>Parameter</th><th>Value</th><th>Source</th><th>Method</th><th>Uncertainty</th><th>Inferred?</th></tr></thead><tbody>' +
        (m.provenance || []).map(function (p) { return '<tr><td>' + esc(p.parameter) + '</td><td>' + esc(p.value) + (p.unit && p.unit !== '-' ? ' ' + esc(p.unit) : '') + '</td><td>' + sidChips(slug, p.source_id) + '</td><td>' + esc(p.method) + '</td><td>' + esc(p.uncertainty) + '</td><td>' + (p.estimated ? 'estimated' : 'sourced') + '</td></tr>'; }).join('') + '</tbody></table></div>';
    }
    box.innerHTML = html || '<p class="m3d-note">Nothing to show.</p>';
    det.setAttribute('data-filled', '1');
  }

  function goto(href) {
    var id = href.replace(/^#/, '');
    var mm = /^m3d-(.+)-m-[\d-]+$/.exec(id);
    if (mm && BY[mm[1]]) {
      if (sel !== mm[1]) go(mm[1]);                      // the target lives in a model section that is not the visible one
      var det = $('details[data-doc="methods"][data-slug="' + mm[1] + '"]');
      if (det) { det.open = true; fillDoc(det); }
    }
    return scrollToId(id, true);
  }

  // ------------------------------------------------------------------ viewers
  function setPoster(slug) {
    var box = $('[data-viewer="' + slug + '"]'), v = VIEW[slug];
    if (!box || !v) return;
    var bg = v.poster ? ' style="background-image:url(\'' + esc(v.poster) + '\')"' : '';
    box.innerHTML = '<div class="m3d-poster"' + bg + '><div class="m3d-poster-box"><button type="button" class="m3d-btn m3d-load" data-m3d-load="' + esc(slug) + '">Load 3D model</button><p>Viewer unloaded to free the graphics context.</p></div></div>';
    var u = $('[data-m3d-unload="' + slug + '"]'); if (u) u.hidden = true;
  }
  function unload(slug) {
    var i = live.indexOf(slug); if (i >= 0) live.splice(i, 1);
    delete pmState[slug]; delete verLive[slug];
    var box = $('[data-viewer="' + slug + '"]');
    if (box) { var f = $('iframe', box); if (f) f.src = 'about:blank'; setPoster(slug); }
  }
  function load(slug) {
    var v = VIEW[slug], box = $('[data-viewer="' + slug + '"]');
    if (!v || !box || live.indexOf(slug) >= 0) return;
    while (live.length >= MAX_LIVE) unload(live[0]);
    live.push(slug);
    box.innerHTML = '';
    var f = document.createElement('iframe');
    f.title = '3D model: ' + v.name; f.setAttribute('allow', 'fullscreen');
    f.src = viewerSrc(slug);
    box.appendChild(f);
    var u = $('[data-m3d-unload="' + slug + '"]'); if (u) u.hidden = false;
  }

  // ------------------------------------------------------------------ full screen (viewer + photo panel), always with an Exit button
  function stageOf(slug) { return $('.m3d-stage[data-stage="' + slug + '"]'); }
  function syncFs() {
    $all('.m3d-stage').forEach(function (s) { s.classList.toggle('is-full', s === fsStage); });
    $all('[data-m3d-fs]').forEach(function (b) {
      var on = !!fsStage && fsStage.getAttribute('data-stage') === b.getAttribute('data-m3d-fs');
      b.setAttribute('aria-pressed', String(on)); b.textContent = on ? 'Exit full screen' : 'Full screen';
    });
    document.documentElement.classList.toggle('m3d-fs', !!fsStage);
  }
  function enterFs(slug) {
    var st = stageOf(slug); if (!st) return;
    fsStage = st; syncFs();                              // layout first (works for the native and the CSS fallback alike)
    var req = st.requestFullscreen || st.webkitRequestFullscreen;
    if (req) {
      try { var pr = req.call(st); if (pr && pr.catch) pr.catch(function () { /* refused: the CSS full-screen layout stays */ }); } catch (e) { /* same */ }
    }
    var ex = $('.m3d-exitfs', st); if (ex) ex.focus({ preventScroll: true });
  }
  function exitFs() {
    var st = fsStage; fsStage = null; syncFs();
    var fe = document.fullscreenElement || document.webkitFullscreenElement;
    if (fe) { try { (document.exitFullscreen || document.webkitExitFullscreen).call(document); } catch (e) { /* already out */ } }
    var b = st && $('[data-m3d-fs="' + st.getAttribute('data-stage') + '"]'); if (b) b.focus({ preventScroll: true });
  }
  function onFsChange() {                                // native full screen ended by Esc / browser UI: drop the layout class too
    var fe = document.fullscreenElement || document.webkitFullscreenElement;
    if (!fe && fsStage) { fsStage = null; syncFs(); }
  }

  // ------------------------------------------------------------------ tooltip
  var tip = null;
  function ensureTip() {
    if (tip) return tip;
    tip = document.createElement('div');
    tip.className = 'm3d-tip'; tip.id = 'm3d-tip'; tip.setAttribute('role', 'tooltip'); tip.hidden = true;
    document.body.appendChild(tip);
    return tip;
  }
  function tipHTML(p) {
    var src = [p.citation].filter(Boolean).join(' ');
    var extra = [p.credit && p.credit !== 'not stated' ? 'Credit: ' + p.credit : '', p.date ? 'Image date: ' + p.date : '', p.license ? 'Licence: ' + p.license : ''].filter(Boolean).join(' · ');
    return '<p class="t">' + esc(p.title) + '</p>' +
      '<p><b>How it was used:</b> ' + esc(p.how_used || 'not recorded in the registry') + (p.check_values && p.check_values.length ? ' <span class="src">(model values affected: ' + esc(p.check_values.join(', ')) + ')</span>' : '') + '</p>' +
      (p.pending ? '<p class="pend"><b>Flagged, not yet checked:</b> ' + esc(p.check_what) + '</p>' : '') +
      '<p class="src"><b>Source:</b> ' + esc(src || 'not stated') + (extra ? ' &mdash; ' + esc(extra) : '') + '</p>' +
      '<p class="hint">Click to show it next to the 3D model.</p>';
  }
  function showTip(tile) {
    var p = PIC[tile.getAttribute('data-pic')]; if (!p) return;
    var t = ensureTip();
    t.innerHTML = tipHTML(p); t.hidden = false;
    tile.setAttribute('aria-describedby', 'm3d-tip'); tipFor = tile;
    placeTip(tile);
  }
  function placeTip(tile) {
    var t = tip; if (!t) return;
    var r = tile.getBoundingClientRect(), tw = t.offsetWidth, th = t.offsetHeight, vw = window.innerWidth, vh = window.innerHeight;
    var x = Math.min(Math.max(8, r.left + r.width / 2 - tw / 2), vw - tw - 8);
    var y = r.bottom + 8; if (y + th > vh - 8) y = Math.max(8, r.top - th - 8);
    t.style.left = x + 'px'; t.style.top = y + 'px';
  }
  function hideTip() {
    if (tip) tip.hidden = true;
    if (tipFor) { tipFor.removeAttribute('aria-describedby'); tipFor = null; }
  }

  // ------------------------------------------------------------------ lightbox (enlarged view with the full registry record)
  function ensureLb() {
    if (lb) return lb;
    lb = document.createElement('dialog');
    lb.className = 'm3d-lb'; lb.setAttribute('aria-label', 'Picture details');
    lb.innerHTML = '<button type="button" class="m3d-lb-close" data-m3d-lbclose aria-label="Close (Esc)">&times;</button><div class="m3d-lb-in"><div class="m3d-lb-media"></div><div class="m3d-lb-side"></div></div>';
    document.body.appendChild(lb);
    lb.addEventListener('click', function (e) {
      if (e.target === lb) { lb.close(); return; }
      var b = e.target.closest('[data-m3d-lbclose]'); if (b) { lb.close(); return; }
      var t = e.target.closest('[data-lbver]'); if (t) { showVersion(Number(t.getAttribute('data-lbver'))); return; }
      var n = e.target.closest('[data-lbnav]'); if (n) { navLb(Number(n.getAttribute('data-lbnav'))); }
    });
    lb.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') navLb(1); else if (e.key === 'ArrowLeft') navLb(-1); });
    lb.addEventListener('close', function () {
      var st = lbState, f = st && st.opener; lbState = null;
      if (st && BY[st.slug]) showPic(st.slug, st.id, 0);           // the panel next to the model follows the last picture looked at
      if (f && document.contains(f)) f.focus({ preventScroll: true });
    });
    return lb;
  }
  function row(k, v) { return v ? '<dt>' + k + '</dt><dd>' + v + '</dd>' : ''; }
  function openLb(slug, id, opener, vi0) {
    var p = PIC[slug + '|' + id]; if (!p) return;
    var d = ensureLb(); hideTip();
    var chk = p.pending ? '<b>Flagged, not yet checked.</b> ' + esc(p.check_what) : (p.check_what && !/^none/i.test(p.check_what) ? 'Checked. ' + esc(p.check_what) : (p.check_what ? 'Nothing pending: ' + esc(p.check_what) : ''));
    var links = [ext(p.source_page, 'source page'), ext(p.image_url, 'image link')].filter(Boolean).join(' · ');
    $('.m3d-lb-side', d).innerHTML = '<h3>' + esc(p.title) + '</h3><dl>' +
      row('Shows', esc(p.shows)) + row('How it was used', esc(p.how_used)) + row('Model values', esc((p.check_values || []).join(', '))) + row('3D check', chk) +
      row('State shown', esc(p.state)) + row('Image date', esc(p.date)) + row('Kind', esc(p.kind) + (p.structure_visible === true ? ' (structure visible)' : p.structure_visible === false ? ' (structure not visible)' : '')) +
      row('Used for', esc((p.roles || []).join(', '))) + row('Citation', esc(p.citation)) + row('Page / figure', esc(p.page_or_figure)) + row('Credit', esc(p.credit)) +
      row('Licence', esc(p.license)) + row('Rights note', esc(p.rights_note)) + row('Retrieved', esc(p.retrieved)) + row('Links', links) +
      row('Registry', esc(p.id) + ' (03_images/reefs/' + esc(slug) + '/images.json)') + row('Linked records', (p.linked_records || []).map(esc).join('<br>')) + row('Added by', esc(p.added_by)) +
      '</dl><div class="m3d-lb-nav"><button type="button" class="m3d-btn ghost" data-lbnav="-1">&larr; Previous</button><button type="button" class="m3d-btn ghost" data-lbnav="1">Next &rarr;</button><button type="button" class="m3d-btn ghost" data-m3d-lbclose>Close (Esc)</button></div>';
    lbState = { slug: slug, id: id, versions: picVersions(p), opener: opener || (lbState && lbState.opener) || null };
    showVersion(vi0 || 0);
    if (!d.open) { if (d.showModal) d.showModal(); else d.setAttribute('open', ''); }
    $('.m3d-lb-close', d).focus({ preventScroll: true });
  }
  function showVersion(i) {
    var v = lbState.versions[i], media = $('.m3d-lb-media', lb), p = PIC[lbState.slug + '|' + lbState.id];
    var tg = lbState.versions.length > 1 ? '<div class="m3d-lb-toggle" role="group" aria-label="Original or annotated version">' + lbState.versions.map(function (x, k) { return '<button type="button" data-lbver="' + k + '" aria-pressed="' + (k === i) + '">' + esc(x.label) + '</button>'; }).join('') + '</div>' : '';
    media.innerHTML = tg + '<img src="' + esc(v.web) + '" width="' + v.w + '" height="' + v.h + '" alt="' + esc(p.title + (i ? ' (annotated)' : '')) + '">';
  }
  function navLb(dir) {
    var m = BY[lbState.slug], p = PIC[lbState.slug + '|' + lbState.id], n = m._ord.length;
    var q = m._ord[(p._i + dir + n) % n]; openLb(lbState.slug, q.id);
  }

  // ------------------------------------------------------------------ events
  function bindOnce() {
    root.addEventListener('click', function (e) {
      var t = e.target;
      var sb = t.closest('[data-m3d-sel]'); if (sb) { go(sb.getAttribute('data-m3d-sel')); return; }
      var ld = t.closest('[data-m3d-load]'); if (ld) { load(ld.getAttribute('data-m3d-load')); return; }
      var fb = t.closest('[data-m3d-fs]'); if (fb) { var fsl = fb.getAttribute('data-m3d-fs'); if (fsStage && fsStage.getAttribute('data-stage') === fsl) exitFs(); else enterFs(fsl); return; }
      if (t.closest('[data-m3d-exitfs]')) { exitFs(); return; }
      var pc = t.closest('[data-m3d-pcol]'); if (pc) { var st0 = pc.closest('.m3d-stage'); setPics(picsOff); var nb = st0 && $(picsOff ? '.m3d-pcol-open' : '.m3d-pcol-bar .m3d-pcol', st0); if (nb) nb.focus({ preventScroll: true }); return; }
      var mt = t.closest('[data-m3d-match]'); if (mt) { var sm = mt.closest('.m3d-stage'); if (sm) matchPhoto(sm.getAttribute('data-stage'), mt.getAttribute('data-m3d-match')); return; }
      var mr = t.closest('[data-m3d-pmreset]'); if (mr) { var sr = mr.closest('.m3d-stage'); if (sr) resetMatch(sr.getAttribute('data-stage')); return; }
      var vn = t.closest('[data-vnow]'); if (vn) { vn.classList.toggle('open'); vn.title = vn.classList.contains('open') ? 'Click to fold' : 'Click to read the whole text'; return; }
      var vb = t.closest('[data-m3d-ver]'); if (vb) { var kv = vb.getAttribute('data-m3d-ver').split('|'); setVersion(kv[0], kv.slice(1).join('|')); return; }
      var vi = t.closest('[data-m3d-vinfo]'); if (vi) { openVerDlg(vi.getAttribute('data-m3d-vinfo'), vi); return; }
      var ul = t.closest('[data-m3d-unload]'); if (ul) { unload(ul.getAttribute('data-m3d-unload')); return; }
      var pn = t.closest('[data-picnav]');
      if (pn) { var st1 = pn.closest('.m3d-stage'); if (st1) stepPic(st1.getAttribute('data-stage'), Number(pn.getAttribute('data-picnav'))); return; }
      var pv = t.closest('[data-picver]');
      if (pv) { var st2 = pv.closest('.m3d-stage'), s2 = st2 && st2.getAttribute('data-stage'); if (s2) showPic(s2, picSel[s2], Number(pv.getAttribute('data-picver'))); return; }
      var en = t.closest('[data-m3d-enlarge]');
      if (en) { e.preventDefault(); var st3 = en.closest('.m3d-stage'), s3 = st3 && st3.getAttribute('data-stage'); if (s3 && BY[s3]) openLb(s3, picSel[s3] || BY[s3]._ord[0].id, en, picVer[s3] || 0); return; }
      var tile = t.closest('.m3d-tile');
      if (tile) { var k = tile.getAttribute('data-pic').split('|'); showPic(k[0], k[1], 0); hideTip(); return; }
      var go1 = t.closest('a[href^="#m3d-"]');            // in-tab links: appendix parts, methods sections, references, caveat rows
      if (go1) { e.preventDefault(); goto(go1.getAttribute('href')); return; }
    });
    root.addEventListener('mouseover', function (e) { if (!HOVER_MQ.matches) return; var tile = e.target.closest('.m3d-tile'); if (tile && tile !== tipFor) showTip(tile); });
    root.addEventListener('mouseout', function (e) { var tile = e.target.closest('.m3d-tile'); if (tile && !tile.contains(e.relatedTarget) && document.activeElement !== tile) hideTip(); });
    root.addEventListener('focusin', function (e) { var tile = e.target.closest('.m3d-tile'); if (tile) showTip(tile); });
    root.addEventListener('focusout', function (e) { var tile = e.target.closest('.m3d-tile'); if (tile) hideTip(); });
    root.addEventListener('toggle', function (e) { var d = e.target; if (d && d.tagName === 'DETAILS' && d.open) fillDoc(d); }, true);
    root.addEventListener('input', function (e) {
      var r = e.target.closest && e.target.closest('[data-m3d-pmop]'); if (!r) return;
      var sg = r.closest('.m3d-stage'), sl = sg && sg.getAttribute('data-stage'); if (!sl || !pmState[sl]) return;
      pmState[sl].opacity = Number(r.value) / 100; pmSend(sl, { type: 'm3d-camera', mode: 'opacity', opacity: pmState[sl].opacity });
    });
    window.addEventListener('message', function (e) {          // the viewer tells us when the user moved the camera (overlay no longer matches) or the view was reset
      var d = e.data;
      if (d && d.type === 'm3d-viewer-caps') {                  // a viewer says what it can do (round 11): handlesVersion = it switches outline versions live, the page must not re-load it
        $all('[data-viewer] iframe').forEach(function (f) { if (f.contentWindow === e.source) verLive[f.closest('[data-viewer]').getAttribute('data-viewer')] = !!d.handlesVersion; });
        return;
      }
      if (!d || d.type !== 'm3d-camera-state') return;
      var sl = null; Object.keys(pmState).forEach(function (k) { var f = pmFrame(k); if (f && f.contentWindow === e.source) sl = k; });
      if (!sl) return;
      if (d.matched === false && d.dragged) { pmState[sl].dragged = true; pmRefresh(sl); }
    });
    root.addEventListener('change', function (e) {
      if (e.target.id !== 'm3d-cav-sel') return;
      var v = e.target.value, n = 0;
      $all('table.m3d-cav tbody tr').forEach(function (tr) { var show = !v || tr.getAttribute('data-slug') === v; tr.hidden = !show; if (show) n++; });
      $('#m3d-cav-count').textContent = n + ' row' + (n === 1 ? '' : 's');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' && e.key !== 'Esc') return;
      if (tipFor) hideTip();
      // CSS-fallback full screen has no browser Esc: handle it here (native full screen is closed by the browser itself)
      if (fsStage && !(document.fullscreenElement || document.webkitFullscreenElement) && !(lb && lb.open) && !(vdlg && vdlg.open)) exitFs();
    });
    document.addEventListener('fullscreenchange', onFsChange);
    document.addEventListener('webkitfullscreenchange', onFsChange);
    // scrolling: a pointer-hover tooltip is dropped; a keyboard-focused tile keeps its tooltip (focus() itself scrolls the tile into view, which
    // fires a scroll event right after focusin - hiding it there was the "keyboard focus shows no tooltip" bug) and the tooltip follows the tile
    window.addEventListener('scroll', function () { if (!tipFor) return; if (tipFor === document.activeElement) placeTip(tipFor); else if (HOVER_MQ.matches) hideTip(); }, true);
    window.addEventListener('resize', hideTip);
    window.addEventListener('hashchange', function () {     // selector choice, deep link, or Back/Forward
      if (/^#view\/models3d(\/|$)/.test(location.hash)) applyHash();
      else if (/^#view\//.test(location.hash)) live.slice().forEach(unload);
    });
  }

  window.ReefModels3D = {
    render: render,
    select: function (id) { render(); go(id); },
    selected: function () { return sel; },
    openModel: function (slug) { render(); go(slug); },
    openPicture: function (slug, id) { render(); select(slug); showPic(slug, id, 0); openLb(slug, id); },
    setPics: setPics, picsOff: function () { return picsOff; },
    unloadAll: function () { live.slice().forEach(unload); sel = rendered ? null : sel; if (fsStage) exitFs(); },
    setVersion: setVersion,
    data: D
  };
})();

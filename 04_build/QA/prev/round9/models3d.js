/* "3D models" tab. Inlined by build.py (before app.js). Data: <script id="data3d"> = data/models3d.json (src/compile_models3d.py).
   Public API: window.ReefModels3D = { render(), openModel(slug), openPicture(slug, id) }.
   app.js calls render() when the view 'models3d' is shown; nothing else in the page depends on this file.
   Per model: header (state, confidence badge + reason, VE note) -> lazy iframe viewer -> key numbers -> picture gallery
   (hover/focus tooltip + lightbox) -> collapsible METHODS/SOURCES/provenance/REQUESTS.  Bottom: methods, texts relied on,
   caveats table, merged references. */
(function () {
  'use strict';

  var node = document.getElementById('data3d');
  var D = null;
  try { D = node ? JSON.parse(node.textContent) : null; } catch (e) { D = null; }
  var root = document.getElementById('m3d-root');
  if (!D || !root) { window.ReefModels3D = { render: function () {}, openModel: function () {}, openPicture: function () {} }; return; }

  var MAX_LIVE = 2;                       // never more than two live WebGL viewers
  var HOVER_MQ = window.matchMedia ? window.matchMedia('(hover: hover) and (pointer: fine)') : { matches: true };
  var rendered = false, live = [], tipFor = null, lb = null, lbState = null, vdlg = null, verSel = {};   // verSel: slug -> chosen outline version id
  var BY = {}, PIC = {}, SRC = {};
  D.models.forEach(function (m) {
    BY[m.slug] = m; SRC[m.slug] = {};
    (m.sources || []).forEach(function (s) { if (s.id) SRC[m.slug][s.id] = s; });
    m.gallery.forEach(function (p, i) { p._i = i; p._slug = m.slug; PIC[m.slug + '|' + p.id] = p; });
  });

  // ------------------------------------------------------------------ helpers
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function safeUrl(u) { return /^https?:\/\//i.test(String(u || '')) ? String(u) : ''; }
  function ext(u, text) { var s = safeUrl(u); return s ? '<a href="' + esc(s) + '" target="_blank" rel="noopener noreferrer">' + esc(text || s) + '</a>' : ''; }
  function inl(s) { return esc(s).replace(/\*([^*]+)\*/g, '<i>$1</i>'); }
  function linkify(escaped) { return escaped.replace(/(https?:\/\/[^\s<)]+[^\s<).,;])/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'); }
  function $(sel, r) { return (r || document).querySelector(sel); }
  function $all(sel, r) { return Array.prototype.slice.call((r || document).querySelectorAll(sel)); }
  function cap(s) { s = String(s || ''); return s.charAt(0).toUpperCase() + s.slice(1); }

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
      '<p class="m3d-vnow" data-vnow="' + s + '" aria-live="polite">' + versionNowHTML(m) + '</p></div>';
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
    if (v.area_m2 != null) rows.push({ q: 'Footprint area (this version)', model: fmtN(v.area_m2) + ' m\u00b2', stated: v.stated.area || '-', diff: '-', ids: ids, note: vs('area_m2', 'm\u00b2'), ver: true });
    if (v.bbox_m && v.bbox_m[0] != null && v.bbox_m[1] != null) rows.push({ q: 'Footprint bounding box', model: fmtN(v.bbox_m[0], 1) + ' \u00d7 ' + fmtN(v.bbox_m[1], 1) + ' m', stated: '-', diff: '-', ids: ids, note: '', ver: true });
    if (v.volume_m3 != null) rows.push({ q: 'Reef volume (this version)', model: fmtN(v.volume_m3) + ' m\u00b3', stated: v.stated.volume || '-', diff: '-', ids: ids, note: vs('volume_m3', 'm\u00b3'), ver: true });
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
    $all('[data-m3d-ver^="' + slug + '|"]').forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-m3d-ver') === slug + '|' + id)); });
    var now = $('[data-vnow="' + slug + '"]'); if (now) now.innerHTML = versionNowHTML(m);
    var kn = $('[data-knbody="' + slug + '"]'); if (kn) kn.innerHTML = knInner(m);
    var fs = $('a[data-m3d-full="' + slug + '"]'); if (fs) fs.href = m.viewer + verSrcHash(m);
    var f = $('[data-viewer="' + slug + '"] iframe');           // live viewer: tell it (postMessage, then a hash-only navigation as a fallback)
    if (f) {
      try { f.contentWindow.postMessage({ type: 'm3d-version', version: id }, '*'); } catch (e) { /* viewer not ready: its initial #version= covers it */ }
      f.src = m.viewer + verSrcHash(m);
    }
  }
  function ensureVdlg() {
    if (vdlg) return vdlg;
    vdlg = document.createElement('dialog');
    vdlg.className = 'm3d-lb m3d-vdlg'; vdlg.setAttribute('aria-labelledby', 'm3d-vdlg-h');
    vdlg.innerHTML = '<button type="button" class="m3d-lb-close" data-m3d-vclose aria-label="Close">&times;</button><div class="m3d-vdlg-in"></div>';
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
        '<td>' + (v.area_m2 != null ? fmtN(v.area_m2) + ' m\u00b2' : '-') + (v.bbox_m && v.bbox_m[0] != null ? '<small>' + fmtN(v.bbox_m[0], 1) + ' \u00d7 ' + fmtN(v.bbox_m[1], 1) + ' m</small>' : '') + '</td>' +
        '<td>' + (v.volume_m3 != null ? fmtN(v.volume_m3) + ' m\u00b3' : 'not computed') + '</td></tr>';
    }).join('');
    $('.m3d-vdlg-in', d).innerHTML = '<h3 id="m3d-vdlg-h">Outline versions: ' + esc(m.name) + '</h3>' + paras +
      '<div class="m3d-tablewrap"><table class="m3d-t m3d-vt"><thead><tr><th>Name</th><th>Date</th><th>Source</th><th>Footprint</th><th>Volume</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
      '<p class="m3d-note">The page opens on the default version. The version buttons in the model header switch the 3D viewer and the key-numbers table together; the caveats table lists how the versions differ.</p>';
    d._opener = opener || null;
    if (d.showModal) d.showModal(); else d.setAttribute('open', '');
  }

  // ------------------------------------------------------------------ one model
  function confHTML(m) {
    var c = m.confidence, lvl = c.level;
    var more = c.reason && c.reason !== c.reason_short;
    return '<div class="m3d-conf m3d-conf-' + esc(lvl) + '"><span class="m3d-badge" title="3D confidence rubric: see Methods section 8">3D confidence: ' + esc(lvl) + '</span>' +
      '<span class="m3d-reason">' + esc(c.reason_short || c.reason) + '</span>' +
      (more ? '<button type="button" class="m3d-more" data-m3d-more aria-expanded="false">Full reason</button><p class="m3d-full" hidden>' + esc(c.reason) + '</p>' : '') + '</div>';
  }

  function viewerHTML(m) {
    var bg = m.poster ? ' style="background-image:url(\'' + esc(m.poster) + '\')"' : '';
    return '<div class="m3d-viewer" data-viewer="' + esc(m.slug) + '"><div class="m3d-poster"' + bg + '><div class="m3d-poster-box">' +
      '<button type="button" class="m3d-btn m3d-load" data-m3d-load="' + esc(m.slug) + '">Load 3D model</button>' +
      '<p>The interactive model opens inside the page (three.js, works offline). At most ' + MAX_LIVE + ' viewers stay live; loading a third unloads the oldest.</p></div></div></div>' +
      '<div class="m3d-viewer-bar"><a class="m3d-btn ghost" data-m3d-full="' + esc(m.slug) + '" href="' + esc(m.viewer + verSrcHash(m)) + '" target="_blank" rel="noopener">Open full screen</a>' +
      '<button type="button" class="m3d-btn ghost" data-m3d-unload="' + esc(m.slug) + '" hidden>Unload viewer</button>' +
      '<span class="grow">Model files: <code>' + esc(m.viewer) + '</code>' + (m.built ? ' (generated ' + esc(m.built) + ')' : '') + '</span></div>';
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
      (hasVers(m) ? '<p class="m3d-note">The shaded rows belong to the selected outline version (' + esc(verOf(m, activeVer(m)).name) + '); the other rows apply to every version unless a row says otherwise.</p>' : '') +
      (m.key_numbers_curated ? '' : '<p class="m3d-note">Auto-selected from the model.js provenance table (not yet curated into a model-versus-source comparison).</p>') +
      '<p class="m3d-note">Heights are metres relative to the model zero (mean sea level, MSL) unless a datum is named; &quot;below LAT&quot; = below lowest astronomical tide. Hover a source id for its citation.</p>' +
      (tides ? '<h4 style="margin:16px 0 6px">Local tide levels used</h4><div class="m3d-tablewrap"><table class="m3d-t m3d-tides"><thead><tr><th>Level</th><th>Name</th><th>z (m rel. MSL)</th>' + (allSame ? '' : '<th>Source</th>') + '</tr></thead><tbody>' + tides + '</tbody></table></div>' +
        (m.tides.note ? '<p class="m3d-note">' + esc(m.tides.note) + '</p>' : '') +
        (tideSrc ? '<p class="m3d-note">Source of the levels: ' + esc((m.tides.levels[0].src || '')) + '</p>' : '') : '');
  }

  function keyNumbersHTML(m) {
    return '<h3 class="m3d-h3" id="m3d-' + esc(m.slug) + '-kn">Key numbers: model vs stated in the sources</h3><div data-knbody="' + esc(m.slug) + '">' + knInner(m) + '</div>';
  }

  function tileHTML(p) {
    var tags = (p.pending ? '<span class="m3d-tag pend">check pending</span>' : '') + (p.annotated.length ? '<span class="m3d-tag">+ annotated</span>' : '');
    var meta = [p.kind, p.date].filter(Boolean).join(' · ');
    return '<button type="button" class="m3d-tile" data-pic="' + esc(p._slug + '|' + p.id) + '" aria-label="' + esc(p.title) + '. Shows how it was used on hover or focus; press to enlarge.">' +
      '<span class="tags">' + tags + '</span><span class="ph"><img src="' + esc(p.thumb) + '" width="' + (p.tw || 400) + '" height="' + (p.th || 300) + '" loading="lazy" decoding="async" alt=""></span>' +
      '<span class="cap"><b>' + esc(p.title) + '</b><span>' + esc(meta) + '</span></span></button>';
  }

  function galleryHTML(m) {
    var out = '<h3 class="m3d-h3" id="m3d-' + esc(m.slug) + '-pics">Pictures used to construct this model (' + m.gallery.length + ')</h3>' +
      '<p class="m3d-note">Hover or focus a picture for <b>how it was used</b> and its <b>source</b>; click for the large view with the full citation, licence and, where one exists, the annotated version. All are private research copies: reuse rights are not cleared.</p>';
    D.groups.forEach(function (g) {
      var items = m.gallery.filter(function (p) { return p.group === g.key; });
      if (!items.length) return;
      out += '<div class="m3d-group"><h4>' + esc(g.label) + ' (' + items.length + ')</h4><p class="m3d-note">' + esc(g.blurb) + '</p><div class="m3d-grid">' + items.map(tileHTML).join('') + '</div></div>';
    });
    if (!m.gallery.length) out += '<p class="m3d-note">No registered pictures were selected for this model.</p>';
    return out;
  }

  function docsHTML(m) {
    var s = '<h3 class="m3d-h3">Methods, sources &amp; uncertainty</h3><p class="m3d-note">Rendered from the model folder (<code>07_scale/shapes/' + esc(m.slug) + '/3d/</code>). Sections open on demand.</p>';
    if (m.docs.methods) s += '<details class="m3d-det" data-doc="methods" data-slug="' + esc(m.slug) + '" id="m3d-' + esc(m.slug) + '-methods"><summary>Methods, validation, uncertainty and confidence (METHODS_3D.md)</summary><div class="m3d-doc"></div></details>';
    if (m.docs.sources) s += '<details class="m3d-det" data-doc="sources" data-slug="' + esc(m.slug) + '"><summary>Source log: what was read where (SOURCES_3D.md)</summary><div class="m3d-doc"></div></details>';
    s += '<details class="m3d-det" data-doc="prov" data-slug="' + esc(m.slug) + '"><summary>Provenance of every model parameter (model.js, ' + (m.provenance || []).length + ' rows)</summary><div class="m3d-doc"></div></details>';
    if (m.docs.requests) s += '<details class="m3d-det" data-doc="requests" data-slug="' + esc(m.slug) + '"><summary>Open questions: what would resolve them (REQUESTS_FOR_LIOR.md)</summary><div class="m3d-doc"></div></details>';
    return s;
  }

  function refChips(m) {
    if (!m.ref_ids || !m.ref_ids.length) return '';
    var map = {}; D.references.forEach(function (r) { map[r.id] = r; });
    return '<p class="m3d-refchips"><b>References used by this model</b> (' + m.ref_ids.length + '; list at the bottom of the tab): ' + m.ref_ids.map(function (id) {
      var r = map[id]; var n = id.replace('ref', '');
      return '<a href="#m3d-ref-' + id + '" data-m3d-ref title="' + esc((r.text || '').replace(/\*/g, '').slice(0, 160)) + '">' + n + '</a>';
    }).join(' ') + '</p>';
  }

  function modelHTML(m) {
    return '<section class="m3d-model" id="m3d-' + esc(m.slug) + '" data-slug="' + esc(m.slug) + '" aria-labelledby="m3d-h-' + esc(m.slug) + '">' +
      '<header><h2 id="m3d-h-' + esc(m.slug) + '">' + (m.flag ? '<span class="flag" aria-hidden="true">' + m.flag + '</span> ' : '') + esc(m.name) + '<small>' + esc(m.place) + (m.verdict_label ? ' · verdict: ' + esc(m.verdict_label) : '') + '</small></h2>' +
      '<p class="m3d-state"><b>State modelled:</b> ' + esc(m.state_short) + '</p>' + versionBarHTML(m) + confHTML(m) +
      '<p class="m3d-ve"><b>Vertical exaggeration.</b> ' + esc(D.ve_generic) + (m.ve_note ? ' ' + esc(m.ve_note) : '') + '</p></header>' +
      viewerHTML(m) + keyNumbersHTML(m) + galleryHTML(m) + docsHTML(m) + refChips(m) + '</section>';
  }

  // ------------------------------------------------------------------ bottom of the tab
  function reliedHTML() {
    var out = '<section class="m3d-sec" id="m3d-relied"><h3>B. Texts we relied on</h3><p class="m3d-note">The sentences that fix crest, height, volume, dates and state of each model (at most 25 words each, with page and link). Every quotation is verified verbatim against the model\'s own documents when the page is built.</p>';
    D.models.forEach(function (m) {
      if (!m.relied || !m.relied.length) return;
      out += '<h4>' + esc(m.name) + '</h4>' + m.relied.map(function (q) {
        return '<blockquote class="m3d-quote"><q>' + esc(q.quote) + '</q><span class="w">' + esc(q.where) + ' &mdash; fixes: ' + esc(q.supports) + (safeUrl(q.url) ? ' · ' + ext(q.url, 'link') : '') + '</span></blockquote>';
      }).join('');
    });
    return out + '</section>';
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
    return '<section class="m3d-sec" id="m3d-caveats"><h3>C. Caveats and discrepancies</h3><p class="m3d-note">One row per discrepancy between a model and a stated figure, or per unresolved assumption. ' + esc(D.caveats_note) + ' Status: <b>unresolved</b> = a stated number the model does not reproduce; <b>open</b> = needs a datum, survey or reading we do not have; <b>by-design</b> = a deliberate simplification or a different state; <b>resolved</b> = checked and reconciled.</p>' +
      '<div class="m3d-cav-filter"><label>Show <select id="m3d-cav-sel">' + opts + '</select></label><span id="m3d-cav-count">' + rows.length + ' rows</span></div>' +
      '<div class="m3d-tablewrap"><table class="m3d-t m3d-cav"><thead><tr><th>Model</th><th>Quantity</th><th>Our model</th><th>Stated in source (citation)</th><th>Difference</th><th>Likely reason</th><th>Status / what would resolve it</th></tr></thead><tbody>' + body + '</tbody></table></div></section>';
  }

  function refsHTML() {
    var names = {}; D.models.forEach(function (m) { names[m.slug] = m.name; });
    var li = D.references.map(function (r) {
      var by = r.cited_by.map(function (s) { return esc(names[s] || s); }).join(', ');
      return '<li id="m3d-ref-' + r.id + '" value="' + r.id.replace('ref', '') + '">' + linkify(inl(r.text)) + '<span class="by">Cited by: ' + by + '</span></li>';
    }).join('');
    return '<section class="m3d-sec" id="m3d-refs"><h3>D. References</h3><p class="m3d-note">One merged, de-duplicated author-year list from the References sections of every METHODS_3D.md and the bathymetry reports (' + D.references.length + ' entries). Where two documents cite the same work with different details, the fuller entry is kept. Each model section links to its entries.</p><ol class="m3d-refs">' + li + '</ol></section>';
  }

  function applicationHTML() {
    return '<section class="m3d-app" id="m3d-app" aria-labelledby="m3d-app-h"><h2 id="m3d-app-h">Methods, texts relied on, caveats and references</h2>' +
      '<ul class="m3d-jump"><li><a href="#m3d-methods" data-m3d-goto>A. Methods</a></li><li><a href="#m3d-relied" data-m3d-goto>B. Texts relied on</a></li><li><a href="#m3d-caveats" data-m3d-goto>C. Caveats &amp; discrepancies</a></li><li><a href="#m3d-refs" data-m3d-goto>D. References</a></li></ul>' +
      '<section class="m3d-sec" id="m3d-methods"><h3>A. Methods (project-wide)</h3><div class="m3d-doc">' + D.methods_html + '</div></section>' + reliedHTML() + caveatsHTML() + refsHTML() + '</section>';
  }

  function introHTML() {
    var n = D.models.length, notyet = D.not_yet.length + D.feasibility.length;
    return '<div class="m3d-intro"><h2>3D models of the built reefs</h2><p>Each model is a reconstruction from published drawings, charts, surveys and text, <b>not a survey of the structure</b>. ' +
      n + ' reef' + (n === 1 ? ' is' : 's are') + ' modelled so far' + (notyet ? '; ' + notyet + ' more are not yet modelled (listed after the models)' : '') + '. For every model the state shown, the 3D confidence with its reason, and the vertical exaggeration are stated; below the viewer are the key numbers set against the figures stated in the sources, <b>the pictures that were used to construct it</b> (hover for the method and the source), the full methods documents, and at the bottom the project-wide methods, the texts relied on, the caveats and the references.</p>' +
      '<p class="m3d-note">Confidence: <span class="m3d-conf-high"><span class="m3d-badge">high</span></span> <span class="m3d-conf-medium"><span class="m3d-badge">medium</span></span> <span class="m3d-conf-low"><span class="m3d-badge">low</span></span> (rubric: Methods A, section 8). Plan-shape confidence (Scale tab) is a separate rating.</p>' +
      '<ul class="m3d-jump">' + D.models.map(function (m) { return '<li><a href="#view/models3d/' + esc(m.slug) + '" data-m3d-model="' + esc(m.slug) + '">' + esc(m.name) + ' <span class="m3d-conf-' + esc(m.confidence.level) + '"><span class="m3d-badge">' + esc(m.confidence.level) + '</span></span></a></li>'; }).join('') +
      '<li><a href="#m3d-app" data-m3d-goto>Methods &amp; references</a></li></ul></div>';
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

  // ------------------------------------------------------------------ render
  function render() {
    if (!rendered) {
      root.innerHTML = '<div class="m3d">' + introHTML() + D.models.map(modelHTML).join('') + notModelledHTML() + applicationHTML() + '</div>';
      rendered = true;
      bindOnce();
    }
    var m = /^#view\/models3d\/([a-z0-9-]+)$/.exec(location.hash);
    if (m) setTimeout(function () { scrollToId('m3d-' + m[1]); }, 60);
  }

  function scrollToId(id, flash) {
    var el = document.getElementById(id);
    if (!el) return false;
    el.scrollIntoView({ block: 'start', behavior: 'auto' });
    if (flash) { el.classList.add('m3d-flash'); setTimeout(function () { el.classList.remove('m3d-flash'); }, 1800); }
    return true;
  }

  // ------------------------------------------------------------------ lazy documents
  function fillDoc(det) {
    if (!det || det.getAttribute('data-filled')) return;
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
      var det = $('details[data-doc="methods"][data-slug="' + mm[1] + '"]');
      if (det) { det.open = true; fillDoc(det); }
    }
    return scrollToId(id, true);
  }

  // ------------------------------------------------------------------ viewers
  function setPoster(slug) {
    var box = $('[data-viewer="' + slug + '"]'), m = BY[slug];
    if (!box) return;
    var bg = m.poster ? ' style="background-image:url(\'' + esc(m.poster) + '\')"' : '';
    box.innerHTML = '<div class="m3d-poster"' + bg + '><div class="m3d-poster-box"><button type="button" class="m3d-btn m3d-load" data-m3d-load="' + esc(slug) + '">Load 3D model</button><p>Viewer unloaded to free the graphics context.</p></div></div>';
    var u = $('[data-m3d-unload="' + slug + '"]'); if (u) u.hidden = true;
  }
  function unload(slug) {
    var i = live.indexOf(slug); if (i >= 0) live.splice(i, 1);
    var box = $('[data-viewer="' + slug + '"]');
    if (box) { var f = $('iframe', box); if (f) f.src = 'about:blank'; setPoster(slug); }
  }
  function load(slug) {
    var m = BY[slug], box = $('[data-viewer="' + slug + '"]');
    if (!m || !box || live.indexOf(slug) >= 0) return;
    while (live.length >= MAX_LIVE) unload(live[0]);
    live.push(slug);
    box.innerHTML = '';
    var f = document.createElement('iframe');
    f.title = '3D model: ' + m.name; f.setAttribute('allow', 'fullscreen');
    f.src = m.viewer + verSrcHash(m);
    box.appendChild(f);
    var u = $('[data-m3d-unload="' + slug + '"]'); if (u) u.hidden = false;
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
      '<p class="hint">Click for the large view, full citation and licence.</p>';
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

  // ------------------------------------------------------------------ lightbox
  function ensureLb() {
    if (lb) return lb;
    lb = document.createElement('dialog');
    lb.className = 'm3d-lb'; lb.setAttribute('aria-label', 'Picture details');
    lb.innerHTML = '<button type="button" class="m3d-lb-close" data-m3d-lbclose aria-label="Close">&times;</button><div class="m3d-lb-in"><div class="m3d-lb-media"></div><div class="m3d-lb-side"></div></div>';
    document.body.appendChild(lb);
    lb.addEventListener('click', function (e) {
      if (e.target === lb) { lb.close(); return; }
      var b = e.target.closest('[data-m3d-lbclose]'); if (b) { lb.close(); return; }
      var t = e.target.closest('[data-lbver]'); if (t) { showVersion(Number(t.getAttribute('data-lbver'))); return; }
      var n = e.target.closest('[data-lbnav]'); if (n) { navLb(Number(n.getAttribute('data-lbnav'))); }
    });
    lb.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight') navLb(1); else if (e.key === 'ArrowLeft') navLb(-1); });
    lb.addEventListener('close', function () { var f = lbState && lbState.opener; lbState = null; if (f && document.contains(f)) f.focus({ preventScroll: true }); });
    return lb;
  }
  function row(k, v) { return v ? '<dt>' + k + '</dt><dd>' + v + '</dd>' : ''; }
  function openLb(slug, id, opener) {
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
      '</dl><div class="m3d-lb-nav"><button type="button" class="m3d-btn ghost" data-lbnav="-1">&larr; Previous</button><button type="button" class="m3d-btn ghost" data-lbnav="1">Next &rarr;</button></div>';
    var versions = [{ label: 'Original', web: p.web, w: p.w, h: p.h }].concat(p.annotated.map(function (a) { return { label: 'Annotated: ' + a.label, web: a.web, w: a.w, h: a.h }; }));
    lbState = { slug: slug, id: id, versions: versions, opener: opener || (lbState && lbState.opener) || null };
    showVersion(0);
    if (!d.open) { if (d.showModal) d.showModal(); else d.setAttribute('open', ''); }
    $('.m3d-lb-close', d).focus({ preventScroll: true });
  }
  function showVersion(i) {
    var v = lbState.versions[i], media = $('.m3d-lb-media', lb), p = PIC[lbState.slug + '|' + lbState.id];
    var tg = lbState.versions.length > 1 ? '<div class="m3d-lb-toggle" role="group" aria-label="Original or annotated version">' + lbState.versions.map(function (x, k) { return '<button type="button" data-lbver="' + k + '" aria-pressed="' + (k === i) + '">' + esc(x.label) + '</button>'; }).join('') + '</div>' : '';
    media.innerHTML = tg + '<img src="' + esc(v.web) + '" width="' + v.w + '" height="' + v.h + '" alt="' + esc(p.title + (i ? ' (annotated)' : '')) + '">';
  }
  function navLb(dir) {
    var m = BY[lbState.slug], p = PIC[lbState.slug + '|' + lbState.id], n = m.gallery.length;
    var q = m.gallery[(p._i + dir + n) % n]; openLb(lbState.slug, q.id);
  }

  // ------------------------------------------------------------------ events
  function bindOnce() {
    root.addEventListener('click', function (e) {
      var t = e.target;
      var ld = t.closest('[data-m3d-load]'); if (ld) { load(ld.getAttribute('data-m3d-load')); return; }
      var vb = t.closest('[data-m3d-ver]'); if (vb) { var kv = vb.getAttribute('data-m3d-ver').split('|'); setVersion(kv[0], kv.slice(1).join('|')); return; }
      var vi = t.closest('[data-m3d-vinfo]'); if (vi) { openVerDlg(vi.getAttribute('data-m3d-vinfo'), vi); return; }
      var ul = t.closest('[data-m3d-unload]'); if (ul) { unload(ul.getAttribute('data-m3d-unload')); return; }
      var mo = t.closest('[data-m3d-more]');
      if (mo) { var p = mo.nextElementSibling; p.hidden = !p.hidden; mo.setAttribute('aria-expanded', String(!p.hidden)); mo.textContent = p.hidden ? 'Full reason' : 'Hide full reason'; return; }
      var tile = t.closest('.m3d-tile');
      if (tile) {
        // touch: first tap shows the tooltip, second tap opens the large view
        if (!HOVER_MQ.matches && tipFor !== tile) { showTip(tile); return; }
        var k = tile.getAttribute('data-pic').split('|'); openLb(k[0], k[1], tile); return;
      }
      var go = t.closest('a[href^="#m3d-"]');   // in-tab links: methods sections, references, caveat rows
      if (go) { e.preventDefault(); goto(go.getAttribute('href')); return; }
      var mod = t.closest('a[data-m3d-model]');
      if (mod) { e.preventDefault(); history.replaceState(null, '', mod.getAttribute('href')); scrollToId('m3d-' + mod.getAttribute('data-m3d-model')); return; }
      if (tipFor && !t.closest('.m3d-tile')) hideTip();
    });
    root.addEventListener('mouseover', function (e) { if (!HOVER_MQ.matches) return; var tile = e.target.closest('.m3d-tile'); if (tile && tile !== tipFor) showTip(tile); });
    root.addEventListener('mouseout', function (e) { var tile = e.target.closest('.m3d-tile'); if (tile && !tile.contains(e.relatedTarget) && document.activeElement !== tile) hideTip(); });
    root.addEventListener('focusin', function (e) { var tile = e.target.closest('.m3d-tile'); if (tile) showTip(tile); });
    root.addEventListener('focusout', function (e) { var tile = e.target.closest('.m3d-tile'); if (tile) hideTip(); });
    root.addEventListener('toggle', function (e) { var d = e.target; if (d && d.tagName === 'DETAILS' && d.open) fillDoc(d); }, true);
    root.addEventListener('change', function (e) {
      if (e.target.id !== 'm3d-cav-sel') return;
      var v = e.target.value, n = 0;
      $all('table.m3d-cav tbody tr').forEach(function (tr) { var show = !v || tr.getAttribute('data-slug') === v; tr.hidden = !show; if (show) n++; });
      $('#m3d-cav-count').textContent = n + ' row' + (n === 1 ? '' : 's');
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && tipFor) hideTip(); });
    // scrolling: a pointer-hover tooltip is dropped; a keyboard-focused tile keeps its tooltip (focus() itself scrolls the tile into view, which
    // fires a scroll event right after focusin - hiding it there was the "keyboard focus shows no tooltip" bug) and the tooltip follows the tile
    window.addEventListener('scroll', function () { if (!tipFor) return; if (tipFor === document.activeElement) placeTip(tipFor); else if (HOVER_MQ.matches) hideTip(); }, true);
    window.addEventListener('resize', hideTip);
    window.addEventListener('hashchange', function () {            // deep link #view/models3d/<slug> while the tab is already open
      var m = /^#view\/models3d\/([a-z0-9-]+)$/.exec(location.hash);
      if (m && BY[m[1]]) scrollToId('m3d-' + m[1]);
    });
    // leaving the tab: unload live viewers (frees WebGL contexts)
    window.addEventListener('hashchange', function () { if (!/^#view\/models3d/.test(location.hash) && /^#view\//.test(location.hash)) live.slice().forEach(unload); });
  }

  window.ReefModels3D = {
    render: render,
    openModel: function (slug) { render(); scrollToId('m3d-' + slug); },
    openPicture: function (slug, id) { render(); openLb(slug, id); },
    unloadAll: function () { live.slice().forEach(unload); },
    setVersion: setVersion,
    data: D
  };
})();

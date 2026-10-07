/* Artificial Surf Reefs Survey — vanilla JS, no frameworks. Works from file://. */
(function () {
  'use strict';

  var PAYLOAD = JSON.parse(document.getElementById('data').textContent);
  var META = PAYLOAD.meta;
  var REEFS = PAYLOAD.reefs;
  var BY_SLUG = {};
  REEFS.forEach(function (r) { BY_SLUG[r.slug] = r; });

  var VERDICTS = [
    { key: 'worked', label: 'Worked', sym: '✓', note: 'did what it was built for' },
    { key: 'partly worked', label: 'Partly worked', sym: '◐', note: 'some goals met' },
    { key: 'mixed', label: 'Mixed', sym: '≈', note: 'real gains and real failures' },
    { key: 'failed', label: 'Failed', sym: '✕', note: 'did not deliver; removed or abandoned' },
    { key: 'n-a', label: 'Too early to tell', sym: '?', note: 'too new to judge' }
  ];
  var V_BY_KEY = {};
  VERDICTS.forEach(function (v, i) { v.order = i; V_BY_KEY[v.key] = v; });
  var VERDICT_COLOR = { 'worked': '#1e7a46', 'partly worked': '#6fbf7e', 'mixed': '#c98a12', 'failed': '#9b1c1c', 'n-a': '#9aa0a8' };

  // ---------------------------------------------------------------- helpers
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function vclass(key) { return 'v-' + String(key).replace(/\s+/g, '-'); }
  function badge(r) {
    var v = V_BY_KEY[r.verdict] || V_BY_KEY['n-a'];
    var titleAttr = v && v.note ? ' title="' + esc(v.label + ': ' + v.note) + '"' : '';
    return '<span class="badge ' + vclass(v.key) + '"' + titleAttr + '><span class="sym" aria-hidden="true">' + v.sym + '</span>' + esc(v.label) + '</span>';
  }
  function flag(r) { return r.country_flag ? '<span class="flag" aria-hidden="true">' + r.country_flag + '</span> ' : ''; }
  function mmss(sec) {
    sec = Math.max(0, Math.round(Number(sec) || 0));
    var h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    return h ? h + ':' + pad(m) + ':' + pad(s) : m + ':' + pad(s);
  }
  function safeUrl(u) { return /^https?:\/\//i.test(String(u || '')) ? String(u) : ''; }
  function extLink(u, text, cls) {
    var s = safeUrl(u);
    if (!s) return esc(text);
    return '<a href="' + esc(s) + '" target="_blank" rel="noopener noreferrer"' + (cls ? ' class="' + cls + '"' : '') + '>' + esc(text) + '</a>';
  }
  function refIds(r) { var o = {}; (r.references || []).forEach(function (x) { o[x.id] = true; }); return o; }
  function refById(r, id) {
    if (!r._refMap) { r._refMap = {}; (r.references || []).forEach(function (x) { r._refMap[x.id] = x; }); }
    return r._refMap[id] || null;
  }
  function hostOf(u) { var m = /^https?:\/\/([^\/?#]+)/i.exec(String(u || '')); return m ? m[1].replace(/^www\./i, '') : ''; }

  /* ---- info pop-overs (round 10, Lior: "allow to read more by hovering some (i)"). Shared by this page header and the 3D tab:
     infoHTML(label, html) -> <span class="info-wrap"><button class="info-i">i</button><span class="info-pop" hidden>..</span></span>.
     Opens on hover, keyboard focus or click/tap (click pins it); closes on Esc, the x, a click elsewhere, or leaving it.
     Paragraphs inside use <span class="pp"> (never <p>: the markup may sit inside a <p>). */
  var infoSeq = 0, infoOpen = null, infoPinned = false, infoTimer = null;
  function infoHTML(label, html) {
    var id = 'info-' + (++infoSeq);
    return '<span class="info-wrap"><button type="button" class="info-i" aria-expanded="false" aria-controls="' + id + '" aria-label="More information: ' + esc(label) + '" title="' + esc(label) + '">i</button>' +
      '<span class="info-pop" id="' + id + '" role="dialog" aria-label="' + esc(label) + '" hidden><button type="button" class="info-pop-close" aria-label="Close">&times;</button>' + html + '</span></span>';
  }
  function infoPos(btn, pop) {
    var r = btn.getBoundingClientRect(), w = pop.offsetWidth, h = pop.offsetHeight, vw = window.innerWidth, vh = window.innerHeight;
    var x = Math.min(Math.max(8, r.left + r.width / 2 - w / 2), Math.max(8, vw - w - 8));
    var y = r.bottom + 6; if (y + h > vh - 8) y = Math.max(8, r.top - h - 6);
    pop.style.left = x + 'px'; pop.style.top = y + 'px';
  }
  function infoPopOf(btn) { return document.getElementById(btn.getAttribute('aria-controls')); }
  function infoShow(btn, pin) {
    var pop = infoPopOf(btn); if (!pop) return;
    if (infoOpen && infoOpen !== btn) infoHide(true);
    clearTimeout(infoTimer);
    pop.hidden = false; btn.setAttribute('aria-expanded', 'true'); infoOpen = btn; if (pin) infoPinned = true;
    infoPos(btn, pop);
  }
  function infoHide(force) {
    if (!infoOpen || (infoPinned && !force)) return;
    var pop = infoPopOf(infoOpen); if (pop) pop.hidden = true;
    infoOpen.setAttribute('aria-expanded', 'false'); infoOpen = null; infoPinned = false;
  }
  function bindInfo() {
    var hoverOK = window.matchMedia ? window.matchMedia('(hover: hover) and (pointer: fine)').matches : true;
    document.addEventListener('click', function (e) {
      var b = e.target.closest('.info-i');
      if (b) { e.preventDefault(); if (infoOpen === b && infoPinned) infoHide(true); else infoShow(b, true); return; }
      var x = e.target.closest('.info-pop-close');
      if (x) { var ob = infoOpen; infoHide(true); if (ob) ob.focus({ preventScroll: true }); return; }
      if (e.target.closest('.info-pop a')) { infoHide(true); return; }
      if (!e.target.closest('.info-wrap')) infoHide(true);
    });
    document.addEventListener('mouseover', function (e) {
      var w = e.target.closest('.info-wrap'); if (!w || !hoverOK) return;
      clearTimeout(infoTimer);
      var b = w.querySelector('.info-i'); if (b && infoOpen !== b) infoShow(b, false);
    });
    document.addEventListener('mouseout', function (e) {
      var w = e.target.closest('.info-wrap'); if (!w || !hoverOK || (e.relatedTarget && w.contains(e.relatedTarget))) return;
      clearTimeout(infoTimer); infoTimer = setTimeout(function () { infoHide(false); }, 260);
    });
    document.addEventListener('focusin', function (e) { var b = e.target.closest && e.target.closest('.info-i'); if (b && infoOpen !== b) infoShow(b, false); });
    document.addEventListener('focusout', function (e) {
      var w = e.target.closest && e.target.closest('.info-wrap');
      if (w && infoOpen && !(e.relatedTarget && w.contains(e.relatedTarget))) infoHide(false);
    });
    document.addEventListener('keydown', function (e) {
      if ((e.key === 'Escape' || e.key === 'Esc') && infoOpen) { var ob = infoOpen; infoHide(true); ob.focus({ preventScroll: true }); }
    });
    window.addEventListener('scroll', function () { if (infoOpen) infoPos(infoOpen, infoPopOf(infoOpen)); }, true);
    window.addEventListener('resize', function () { if (infoOpen) infoPos(infoOpen, infoPopOf(infoOpen)); });
  }

  /* A source marker: a real <button> that opens the source pop-up for reference `id` of reef r.
     kind 'chip' = the pill used on review cards ("R7 · source details"). */
  function markBtn(r, id, kind) {
    var ref = refById(r, id);
    var label = 'Source ' + id + (ref ? ': ' + short(ref.citation, 90) : '');
    return '<button type="button" class="ref-mark' + (kind === 'chip' ? ' ref-chip' : '') + '" data-ref="' + esc(id) + '"' +
      ' aria-haspopup="dialog" aria-expanded="false" aria-controls="ref-pop" aria-label="' + esc(label) + '">' +
      esc(id) + (kind === 'chip' ? ' · source details' : '') + '</button>';
  }
  function refMarks(ids, r) {
    ids = (ids || []).filter(function (id) { return refById(r, id); });
    return ids.length ? '<sup class="refs">[' + ids.map(function (id) { return markBtn(r, id); }).join(', ') + ']</sup>' : '';
  }

  /* Escape text and turn runs of [R#] tokens into one superscript group.
     mode 'link': each R# becomes a button that opens the source pop-up inside the reef dialog.
     mode 'plain': non-interactive superscript (tiles, table, overlays). */
  var REF_RUN = /(?:\s*\[[RS]\d+\])+/g;
  function refify(text, r, mode) {
    if (text == null || text === '') return '';
    var ids = r ? refIds(r) : {};
    var src = String(text), out = '', last = 0, m;
    REF_RUN.lastIndex = 0;
    while ((m = REF_RUN.exec(src))) {
      out += esc(src.slice(last, m.index));
      var toks = m[0].match(/[RS]\d+/g);
      var parts = toks.map(function (id) {
        if (mode === 'link' && ids[id]) return markBtn(r, id);
        return id;
      });
      out += '<sup class="refs">[' + parts.join(', ') + ']</sup>';
      last = m.index + m[0].length;
    }
    out += esc(src.slice(last));
    return out;
  }
  function paras(text, r) {
    return String(text || '').split(/\n\s*\n|\n/).filter(function (p) { return p.trim(); })
      .map(function (p) { return '<p>' + refify(p.trim(), r, 'link') + '</p>'; }).join('');
  }
  function plainRefs(ids) { return ids && ids.length ? '<sup class="refs">[' + ids.join(', ') + ']</sup>' : ''; }
  function short(s, n) { s = String(s || ''); return s.length > n ? s.slice(0, n - 1).replace(/\s+\S*$/, '') + '…' : s; }
  function uniqRefs(s) { var o = []; (String(s || '').match(/R\d+(?=\])/g) || []).forEach(function (x) { if (o.indexOf(x) < 0) o.push(x); }); return o; }
  function stripRefs(s) { return String(s || '').replace(/\s*\[R\d+\]/g, '').trim(); }
  // for pre-truncated display strings: also drops a token cut in half by truncation ("[R1" / "[R")
  function cleanShort(s) { return stripRefs(s).replace(/\s*\[R?\d*(?=…|$)/g, '').replace(/\s+…/g, '…'); }

  function imgTag(url, alt, extra) {
    return '<img src="' + esc(url) + '" alt="' + esc(alt) + '" loading="lazy" decoding="async" referrerpolicy="no-referrer"' + (extra || '') + '>';
  }
  function fallbackBox(sourcePage, hidden) {
    return '<div class="fallback"' + (hidden ? ' hidden' : '') + '><span>Image unavailable here</span>' +
      (safeUrl(sourcePage) ? extLink(sourcePage, 'view source') : '') + '</div>';
  }

  // ------------------------------------------------------------------ state
  var state = { q: '', verdict: {}, country: {}, type: {}, sort: 'year', dir: 1, view: 'gallery' };
  var lastFocus = null;

  function matches(r) {
    var anyOf = function (set, val) { var keys = Object.keys(set); return !keys.length || set[val]; };
    if (!anyOf(state.verdict, r.verdict) || !anyOf(state.country, r.country) || !anyOf(state.type, r.type_short)) return false;
    if (state.q) {
      var hay = [r.name, r.place, r.country, r.type, r.type_short, r.year, r.hover_text, r.designer, r.contractor, r.financed_by, r.verdict_label].join(' ').toLowerCase();
      return state.q.toLowerCase().split(/\s+/).every(function (w) { return !w || hay.indexOf(w) !== -1; });
    }
    return true;
  }
  var SORTERS = {
    year: function (r) { return r.sort_year; },
    cost: function (r) { return r.usd ? r.usd.mid : null; },
    name: function (r) { return r.name.toLowerCase(); },
    country: function (r) { return r.country; },
    type: function (r) { return r.type_short || ''; },
    size: function (r) { return (r.size_short || '').toLowerCase(); },
    financed: function (r) { return stripRefs(r.financed_by).toLowerCase(); },
    verdict: function (r) { return (V_BY_KEY[r.verdict] || V_BY_KEY['n-a']).order; },
    refs: function (r) { return (r.references || []).length; }
  };
  function current() {
    var key = SORTERS[state.sort] || SORTERS.year, dir = state.dir;
    return REEFS.filter(matches).sort(function (a, b) {
      var x = key(a), y = key(b);
      if (x == null && y == null) return a.sort_year - b.sort_year;
      if (x == null) return 1;          // missing values always last
      if (y == null) return -1;
      if (x < y) return -dir;
      if (x > y) return dir;
      return a.sort_year - b.sort_year;
    });
  }

  // ----------------------------------------------------------------- header
  function renderHeader() {
    var years = REEFS.map(function (r) { return r.sort_year; }).filter(function (y) { return y < 9999; });
    var y0 = Math.min.apply(null, years), y1 = Math.max.apply(null, years);
    var countries = {};
    REEFS.forEach(function (r) { countries[r.country] = true; });
    var nC = Object.keys(countries).length;

    // round 10: two short lines; the rest sits behind the (i) pop-over (shared primitive, see "info pop-overs" below)
    $('#intro').innerHTML = 'The <strong>' + REEFS.length + ' artificial surf reefs</strong> we could document as built (' + y0 + '–' + y1 + ', ' + nC + ' countries): what each was meant to do, what was built, what it cost, how it ended.' +
      infoHTML('About this survey',
        '<span class="pp">Each reef is described by what it was meant to do, what was really built, what it cost, who paid, and how it turned out. It is written for municipal decision-makers and surfers weighing a reef for the Israeli coast.</span>' +
        '<span class="pp">Open any reef for the big picture first (an at-a-glance strip and the outcome), then dig into the sections you care about. Every fact carries a numbered source marker [R#]: tap or hover it to see the source without losing your place.</span>' +
        '<span class="pp">Compiled ' + esc(META.compiled_on) + '. The method is described in the footer and in the References index at the bottom of the page.</span>' +
        '<a class="more" href="#references">Read more: References index &rarr;</a>');

    var leg = $('#legend');
    if (leg) leg.remove();

    var totalM = META.usd_total_mid / 1e6;
    var lowM = META.usd_total_low / 1e6, highM = META.usd_total_high / 1e6;
    $('#summary').innerHTML =
      '<div><dt>Reefs</dt><dd>' + REEFS.length + '<small>built, ' + REEFS.filter(function (r) { return r.verdict === 'failed'; }).length + ' judged failed</small></dd></div>' +
      '<div><dt>Countries</dt><dd>' + nC + '<small>' + esc(Object.keys(countries).join(', ')) + '</small></dd></div>' +
      '<div><dt>Years built</dt><dd>' + y0 + '–' + y1 + '<small>first to most recent construction</small></dd></div>' +
      '<div><dt>Total documented cost</dt><dd>≈ US$' + totalM.toFixed(0) + 'M<small>of ' + META.n_with_cost + ' with cost data (range US$' + lowM.toFixed(1) + '–' + highM.toFixed(1) +
      'M). Mostly rough, unsourced currency conversions from the cards — see each reef.</small></dd></div>';
  }

  // ------------------------------------------------------------------ chips
  function renderChips() {
    function group(title, field, values, labeller, titler) {
      var counts = {};
      REEFS.forEach(function (r) { counts[r[field]] = (counts[r[field]] || 0) + 1; });
      return '<div class="chip-group" role="group" aria-label="Filter by ' + title + '"><span>' + title + '</span>' +
        values.map(function (v) {
          var tip = titler ? titler(v) : '';
          var titleAttr = tip ? ' title="' + esc(tip) + '"' : '';
          return '<button type="button" class="chip" data-f="' + field + '" data-v="' + esc(v) + '"' + titleAttr + ' aria-pressed="false">' + labeller(v) + ' <span class="n">' + (counts[v] || 0) + '</span></button>';
        }).join('') + '</div>';
    }
    var countries = [], types = [];
    REEFS.forEach(function (r) {
      if (countries.indexOf(r.country) < 0) countries.push(r.country);
      if (types.indexOf(r.type_short) < 0) types.push(r.type_short);
    });
    countries.sort(); types.sort();
    var flags = {}; REEFS.forEach(function (r) { flags[r.country] = r.country_flag; });
    var presentV = VERDICTS.filter(function (v) { return REEFS.some(function (r) { return r.verdict === v.key; }); });
    $('#chips').innerHTML =
      group('Verdict', 'verdict', presentV.map(function (v) { return v.key; }), function (k) {
        return '<span class="dot ' + vclass(k) + '" aria-hidden="true"></span>' + esc(V_BY_KEY[k].label);
      }, function (k) {
        var v = V_BY_KEY[k];
        return v ? v.label + ': ' + v.note : '';
      }) +
      group('Country', 'country', countries, function (c) { return (flags[c] ? '<span class="flag" aria-hidden="true">' + flags[c] + '</span>' : '') + esc(c); }, function (c) {
        return 'Filter by country: ' + c;
      }) +
      group('Type', 'type_short', types, function (t) { return esc(t); }, function (t) {
        return 'Filter by structure type: ' + t;
      });
  }
  var FIELD_TO_STATE = { verdict: 'verdict', country: 'country', type_short: 'type' };

  // ---------------------------------------------------------------- gallery
  function tileHTML(r) {
    var h = r.hero_image, hv = r.hover || {};
    var media = h && safeUrl(h.url)
      ? imgTag(h.url, stripRefs(h.depicts) || r.name) + fallbackBox(h.source_page, true)
      : fallbackBox(h && h.source_page, false);
    var descId = 'hv-' + r.slug;
    var credit = h ? 'Image: ' + esc(h.credit || 'unknown') + ' · ' + esc(h.license || 'licence not stated') + ' · ' + extLink(h.source_page, 'source') : '';
    return '<article class="tile" data-slug="' + esc(r.slug) + '">' +
      '<div class="tile-media">' + media + badge(r) +
        '<div class="tile-hover" id="' + descId + '"><dl>' +
          '<dt>Size</dt><dd>' + esc(cleanShort(hv.size || r.size_short) || '—') + plainRefs(r.hover_refs.size) + '</dd>' +
          '<dt>Cost</dt><dd>' + esc(r.cost_tile) + plainRefs(r.hover_refs.cost) + '</dd>' +
          '<dt>Year</dt><dd>' + esc(hv.year || r.year_short) + plainRefs(r.hover_refs.year) + '</dd>' +
        '</dl><p class="oc">' + refify(hv.outcome || '', r, 'plain') + '</p></div>' +
      '</div>' +
      '<div class="tile-body">' +
        '<h3><button type="button" class="tile-open" data-open="' + esc(r.slug) + '" aria-describedby="' + descId + '">' + esc(r.name) + '</button></h3>' +
        '<p class="tile-meta">' + flag(r) + esc(r.place_short) + '</p>' +
        '<p class="tile-meta">' + esc(r.year_short) + ' · ' + esc(r.type_short) + '</p>' +
      '</div>' +
      '<p class="tile-credit" title="' + esc(h ? (h.credit + ' — ' + h.license) : '') + '">' + credit + '</p>' +
    '</article>';
  }
  function renderGallery(list) { $('#grid').innerHTML = list.map(tileHTML).join(''); }

  // ------------------------------------------------------------------ table
  var COLS = [
    { k: 'name', t: 'Name' }, { k: 'country', t: 'Country' }, { k: 'year', t: 'Year' }, { k: 'type', t: 'Type' },
    { k: 'size', t: 'Size' }, { k: 'cost', t: 'Cost (~US$)' }, { k: 'financed', t: 'Financed by' },
    { k: 'verdict', t: 'Verdict' }, { k: 'refs', t: '# refs' }
  ];
  function renderTable(list) {
    var head = '<thead><tr>' + COLS.map(function (c) {
      var s = state.sort === c.k ? (state.dir > 0 ? 'ascending' : 'descending') : 'none';
      return '<th scope="col" aria-sort="' + s + '"><button type="button" data-sort="' + c.k + '">' + esc(c.t) + '</button></th>';
    }).join('') + '</tr></thead>';
    var body = '<tbody>' + list.map(function (r) {
      var cost = r.usd
        ? '<span title="' + esc(r.usd.basis + ' — card: ' + r.usd.source_text) + '">' + esc(r.usd.label) + '</span>'
        : '<span class="muted">not disclosed</span>';
      return '<tr data-open="' + esc(r.slug) + '">' +
        '<td class="nm"><button type="button" class="rowbtn" data-open="' + esc(r.slug) + '">' + esc(r.name) + '</button></td>' +
        '<td>' + flag(r) + esc(r.country) + '</td>' +
        '<td class="yr">' + esc(r.year_short) + plainRefs(r.hover_refs.year) + '</td>' +
        '<td>' + esc(r.type_short) + plainRefs(r.hover_refs.type) + '</td>' +
        '<td class="wide">' + esc(cleanShort(r.size_short)) + plainRefs(r.hover_refs.size) + '</td>' +
        '<td class="num">' + cost + '</td>' +
        '<td class="wide">' + esc(short(stripRefs(r.financed_by), 140)) + plainRefs(uniqRefs(r.financed_by)) + '</td>' +
        '<td>' + badge(r) + '</td>' +
        '<td class="num">' + (r.references || []).length + '</td>' +
      '</tr>';
    }).join('') + '</tbody>';
    $('#table').innerHTML = '<caption class="sr">Artificial surf reefs — click a row for details</caption>' + head + body;
  }

  // ------------------------------------------------------------------ views
  function showNotice(msg) { var n = $('#notice'); if (n) { n.textContent = msg; n.hidden = !msg; } }
  function setView(v) {
    if (v !== 'gallery' && v !== 'table' && v !== 'models3d') v = 'gallery';
    state.view = v;
    $all('.views button').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.view === v)); });
    ['gallery', 'table', 'models3d'].forEach(function (k) { var el = $('#view-' + k); if (el) el.hidden = k !== v; });
    document.body.setAttribute('data-view', v);     // lets CSS hide the reef filters on the 3D models tab
    var vh = v === 'gallery' ? '' : '#view/' + v;
    var keepHash = /^#reef\//.test(location.hash) || (v === 'models3d' && /^#view\/models3d\//.test(location.hash));
    if (!keepHash && location.hash !== vh) history.replaceState(null, '', vh || (location.pathname + location.search));
    showNotice('');
    if (v !== 'models3d' && window.ReefModels3D && window.ReefModels3D.unloadAll) window.ReefModels3D.unloadAll();   // free the WebGL viewers when the tab is left
    render();
  }
  function render() {
    var list = current();
    $('#count').textContent = 'Showing ' + list.length + ' of ' + REEFS.length + ' reefs';
    $('#empty').hidden = list.length > 0;
    if (state.view === 'gallery') renderGallery(list);
    else if (state.view === 'table') renderTable(list);
    else if (state.view === 'models3d' && window.ReefModels3D) window.ReefModels3D.render();   // src/models3d.js
    var sel = $('#sort'), val = state.sort + ':' + state.dir;
    if ($all('option', sel).some(function (o) { return o.value === val; })) sel.value = val;
  }

  // ----------------------------------------------------------- detail view
  /* The reef detail view is "big picture first, dig in as you like":
     title -> jump bar (with counts) -> "At a glance" strip -> accordion sections
     (Quick facts and Outcome open, the rest collapsed with a one-line peek).
     Every [R#] marker is a button that opens the source pop-up (see "source pop-up" below). */
  function quickFacts(r) {
    var rows = [
      ['Place', r.place], ['Country', r.country], ['Year', r.year], ['Type', r.type], ['Purpose', r.purpose],
      ['Size', r.size], ['Cost', r.cost], ['Cost (approx. USD)', r.cost_usd_approx], ['Financed by', r.financed_by],
      ['Designer', r.designer], ['Contractor', r.contractor], ['Status now', r.status_now]
    ];
    return '<table class="qf"><tbody>' + rows.filter(function (x) { return x[1] != null && x[1] !== ''; }).map(function (x) {
      var val = typeof x[1] === 'number' ? 'US$' + x[1].toLocaleString('en-US') : x[1];
      return '<tr><th scope="row">' + esc(x[0]) + '</th><td>' + refify(val, r, 'link') + '</td></tr>';
    }).join('') + '<tr><th scope="row">Verdict</th><td>' + badge(r) + '</td></tr></tbody></table>';
  }

  function glanceHTML(r) {
    var hr = r.hover_refs || {};
    var fin = stripRefs(r.financed_by);
    var cell = function (k, v, cls) { return '<div class="gl' + (cls ? ' ' + cls : '') + '"><span class="gl-k">' + k + '</span><span class="gl-v">' + v + '</span></div>'; };
    var outcome = (r.hover && r.hover.outcome) || '';
    return '<section class="glance" aria-label="At a glance"><h3 class="sr">At a glance</h3><div class="gl-grid">' +
      cell('Verdict', badge(r)) +
      cell('Built', esc(r.year_short) + refMarks(hr.year, r)) +
      cell('Cost', esc(r.cost_tile || 'not disclosed') + refMarks(hr.cost, r)) +
      cell('Size', esc(cleanShort(r.size_short) || '—') + refMarks(hr.size, r)) +
      (fin ? cell('Financed by', esc(short(fin, 150)) + refMarks(uniqRefs(r.financed_by), r), 'gl-wide') : '') +
      '</div>' +
      (outcome ? '<p class="gl-out"><span class="gl-k">In short</span>' + refify(outcome, r, 'link') + '</p>' : '') +
    '</section>';
  }

  function figureHTML(o) {
    // o: {url, alt, caption(html), credit(html), contain, local}
    var box = '<div class="fig-box' + (o.contain ? ' contain' : '') + '">' +
      (o.local
        ? '<img src="' + esc(o.url) + '" alt="' + esc(o.alt) + '" loading="lazy" decoding="async">'
        : imgTag(o.url, o.alt) + fallbackBox(o.source, true)) +
      '<button type="button" class="zoom" data-zoom aria-label="Enlarge image: ' + esc(short(o.alt, 90)) + '"></button></div>';
    return '<figure>' + box + '<figcaption>' + o.caption + (o.credit ? '<span class="cr">' + o.credit + '</span>' : '') + '</figcaption></figure>';
  }

  function imagesBody(r) {
    return '<div class="media-grid">' + (r.images || []).map(function (im) {
      var cred = 'Credit: ' + esc(im.credit || 'unknown') + ' · Licence: ' + esc(im.license || 'not stated') + ' · ' + extLink(im.source_page || im.url, 'source');
      var lab = showsTag(im);
      if (im.hotlink_ok === true && safeUrl(im.url)) {
        return figureHTML({ url: im.url, alt: stripRefs(im.depicts) || r.name, caption: lab + refify(im.depicts, r, 'link'), credit: cred, source: im.source_page, contain: im.kind !== 'photo' });
      }
      // not hotlinkable (e.g. Google Maps views): show a link card instead of the picture
      return '<figure><div class="fig-box"><div class="linkcard"><span>' + esc(im.kind === 'map' ? 'Map / satellite view' : 'Image') + ' — view only at the source</span>' +
        extLink(im.url || im.source_page, 'open ' + (im.kind === 'map' ? 'map' : 'image') + ' ↗') + '</div></div>' +
        '<figcaption>' + lab + refify(im.depicts, r, 'link') + '<span class="cr">' + cred + '</span></figcaption></figure>';
    }).join('') + '</div>';
  }

  /* Media labels from the 2026-09-25 media re-check: what an image / frame actually shows,
     and whether a video is about the reef. */
  function showsTag(x) {
    return x && x.shows_label ? '<span class="tag tag-shows shows-' + esc(x.shows_key || '') + '">' + esc(x.shows_label) + '</span> ' : '';
  }
  function aboutTag(v) {
    if (!v || !v.about_label) return '';
    var k = /^site only/i.test(v.about_label) ? 'site' : /^mentions/i.test(v.about_label) ? 'brief' : 'about';
    return '<span class="tag tag-about about-' + k + '">' + esc(v.about_label) + '</span>';
  }
  function isYouTube(v) { return /youtube/i.test(v.platform || '') || /youtu\.?be/i.test(v.url || ''); }
  function videosBody(r) {
    return (r.videos || []).map(function (v, i) {
      var t = Number(v.best_timestamp_seconds) || 0;
      var yt = isYouTube(v) && /^[\w-]{6,}$/.test(v.video_id || '');
      var meta = [v.channel, v.date, v.duration_seconds ? mmss(v.duration_seconds) + ' long' : ''].filter(Boolean).map(esc).join(' · ');
      var watchUrl = yt ? 'https://www.youtube.com/watch?v=' + encodeURIComponent(v.video_id) + (t ? '&t=' + t + 's' : '') : safeUrl(v.url);
      var watchText = yt ? 'Watch on YouTube' + (t ? ' (from ' + mmss(t) + ')' : '') : 'Watch at the source' + (t ? ' (from ' + mmss(t) + ')' : '');
      var box, uncertain = /^\s*UNCERTAIN\b|\bNOT confirmed\b/.test(v.what_it_shows || '');
      if (v.link_only) {
        // site-only video (not about the reef): a plain link with its label, no player / thumbnail / frames
        return '<div class="video video-linkonly"><h4>' + esc(v.title || 'Video ' + (i + 1)) + '</h4><p class="vmeta">' + meta + ' · ' + aboutTag(v) + '</p>' +
          '<p class="vlink">' + extLink(watchUrl, '▶ ' + watchText) + ' — listed for site context only; it does not show the reef.</p>' +
          '<p>' + refify(v.what_it_shows, r, 'link') + '</p></div>';
      }
      if (yt && v.embed_ok === true && !uncertain) {
        box = '<div class="vbox" data-yt="' + esc(v.video_id) + '" data-start="' + t + '" data-title="' + esc(v.title || 'Video') + '"></div>' +
          '<p class="vlink">If the player does not load, ' + extLink(watchUrl, watchText.charAt(0).toLowerCase() + watchText.slice(1)) + '.</p>';
      } else {
        var thumb = yt ? 'https://img.youtube.com/vi/' + encodeURIComponent(v.video_id) + '/hqdefault.jpg' : (v.frames && v.frames[0] ? v.frames[0].path : '');
        box = '<div class="vbox">' + (thumb ? '<img src="' + esc(thumb) + '" alt="" loading="lazy" referrerpolicy="no-referrer">' : '') +
          '<div class="play">' + extLink(watchUrl, '▶ ' + watchText) + '</div></div>';
      }
      var quotes = (v.key_quotes || []).length
        ? '<p style="margin:10px 0 0;font-weight:600;font-size:.9rem">Key quotes</p><ul class="quotes">' + v.key_quotes.map(function (q) { return '<li>' + refify(q, r, 'link') + '</li>'; }).join('') + '</ul>'
        : '';
      var frames = (v.frames || []).length
        ? '<div class="frames">' + v.frames.map(function (f) {
            return figureHTML({ url: f.path, alt: f.caption || ('Frame at ' + f.timestamp), local: true,
              caption: showsTag(f) + '<b>' + esc(f.timestamp) + '</b> — ' + refify(f.caption, r, 'link'), credit: '' });
          }).join('') + '</div>'
        : '';
      return '<div class="video"><h4>' + esc(v.title || 'Video ' + (i + 1)) + '</h4><p class="vmeta">' + meta + (v.about_label ? ' · ' + aboutTag(v) : '') +
        (uncertain ? ' · <span class="lead">unverified lead — not confirmed to show this reef</span>' : '') + '</p>' + box +
        '<p>' + refify(v.what_it_shows, r, 'link') + '</p>' + quotes + frames + '</div>';
    }).join('');
  }

  // ---- reviews: quote cards with who · role · outlet · date, source chip, stance / provenance tags
  var FORUM_RE = /comment|forum|poster/i;
  function stanceClass(s) {
    s = String(s || '').toLowerCase();
    if (/^pos|praise|favourable|favorable/.test(s)) return 'tag-pos';
    if (/^neg|critic/.test(s)) return 'tag-neg';
    return 'tag-neu';
  }
  function reviewsSummary(rv) {
    if (rv.length < 6) return '';
    var st = {}, order = [], tagged = 0, forum = 0, gem = 0;
    rv.forEach(function (x) {
      if (x.stance) { if (!st[x.stance]) { st[x.stance] = 0; order.push(x.stance); } st[x.stance]++; tagged++; }
      if (FORUM_RE.test(x.role || '')) forum++;
      if (x.origin) gem++;
    });
    var parts = [rv.length + ' voices'];
    parts.push(order.length
      ? 'stance: ' + order.map(function (k) { return st[k] + ' ' + esc(k); }).join(', ') + (tagged < rv.length ? ', ' + (rv.length - tagged) + ' not stance-tagged' : '')
      : 'no stance tags in the data');
    parts.push(forum + ' forum ' + (forum === 1 ? 'comment' : 'comments') + ', ' + (rv.length - forum) + ' named people or organisations');
    if (gem) parts.push(gem + ' via Gemini survey, verified');
    return '<p class="rv-sum">' + parts.join(' · ') + '</p>';
  }
  function reviewsBody(r) {
    var rv = r.reviews || [];
    return reviewsSummary(rv) + '<ul class="reviews">' + rv.map(function (x) {
      var forum = FORUM_RE.test(x.role || '');
      var tags = (x.stance ? '<span class="tag ' + stanceClass(x.stance) + '">' + esc(x.stance) + '</span>' : '') +
        (x.origin ? '<span class="tag tag-gem" title="' + esc(x.origin) + '">' + esc(x.origin) + '</span>' : '');
      var who = ['<b>' + esc(x.who || 'unnamed') + '</b>'];
      if (x.role) who.push('<span class="role">' + esc(x.role) + '</span>');
      if (x.outlet) who.push(esc(x.outlet));
      if (x.date) who.push('<span class="nowrap">' + esc(x.date) + '</span>');
      var src = '';
      if (x.ref_id && refById(r, x.ref_id)) src += markBtn(r, x.ref_id, 'chip');
      if (safeUrl(x.url)) src += '<a class="src-chip" href="' + esc(x.url) + '" target="_blank" rel="noopener noreferrer">' + esc(hostOf(x.url)) + ' ↗</a>';
      return '<li class="rv' + (forum ? ' rv-forum' : '') + '">' + (tags ? '<div class="rv-tags">' + tags + '</div>' : '') +
        '<blockquote>' + refify(x.quote_or_summary, r, 'link') + '</blockquote>' +
        '<p class="who">' + who.join(' · ') + '</p>' + (src ? '<p class="rv-src">' + src + '</p>' : '') + '</li>';
    }).join('') + '</ul>';
  }

  function liorBody(r) {
    return '<div class="media-grid">' + (r.lior_images || []).map(function (f) {
      return figureHTML({ url: f.path, alt: stripRefs(f.caption) || 'Figure', local: true, contain: true, caption: refify(f.caption, r, 'link'), credit: 'From Lior\'s own project files' });
    }).join('') + '</div>';
  }

  function refsHTML(r, idPrefix) {
    return '<ol>' + (r.references || []).map(function (x) {
      return '<li id="' + idPrefix + esc(x.id) + '"><span class="rid">' + esc(x.id) + '</span><span>' +
        esc(x.citation) + (safeUrl(x.url) ? ' ' + extLink(x.url, 'link ↗') : ' <span class="muted">(internal note — no URL)</span>') +
        (safeUrl(x.pdf_url) ? ' ' + extLink(x.pdf_url, 'PDF ↗') : '') +
        (safeUrl(x.also_url) ? ' ' + extLink(x.also_url, 'also read at ↗') : '') +
        (x.origin ? ' <span class="tag tag-gem">' + esc(x.origin) + '</span>' : '') +
        '<span class="rsup">Accessed ' + esc(x.accessed || '—') + (x.supports ? ' · Supports: ' + esc(x.supports) : '') + '</span></span></li>';
    }).join('') + '</ol>';
  }

  var OPEN_BY_DEFAULT = { 'quick-facts': true, 'outcome': true };
  function keyOf(title) { return String(title).toLowerCase().replace(/&/g, 'and').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }
  function accHTML(pfx, key, title, body, opts) {
    opts = opts || {};
    var open = opts.forPrint || OPEN_BY_DEFAULT[key];
    return '<details class="acc' + (opts.cls ? ' ' + opts.cls : '') + '" id="' + pfx + key + '"' + (open ? ' open' : '') + '>' +
      '<summary><h3>' + esc(title) + (opts.count != null ? ' <span class="acc-n">' + opts.count + '</span>' : '') + '</h3>' +
      (opts.peek ? '<span class="acc-peek">' + esc(opts.peek) + '</span>' : '') + '</summary>' +
      '<div class="acc-b">' + body + '</div></details>';
  }

  function detailHTML(r, forPrint) {
    var pfx = forPrint ? 'p-' + r.slug + '-' : 'd-';
    var o = { forPrint: forPrint };
    var nImg = (r.images || []).length, nVid = forPrint ? 0 : (r.videos || []).length, nFig = (r.lior_images || []).length;
    var nRev = (r.reviews || []).length, nRef = (r.references || []).length;
    var hasFp = !!(r.footprint && window.ReefScale);
    var story = (r.sections || []).filter(function (s) { return s.html_or_text; }).map(function (s) {
      return accHTML(pfx, keyOf(s.title), s.title, paras(s.html_or_text, r),
        { forPrint: forPrint, peek: short(stripRefs(s.html_or_text), 140) });
    }).join('');
    var firstSec = (r.sections || []).filter(function (s) { return s.html_or_text; })[0];
    var nav = forPrint ? '' : '<nav class="dnav" aria-label="Jump within this reef">' +
      '<button type="button" data-jump="quick-facts">Facts</button>' +
      (firstSec ? '<button type="button" data-jump="' + keyOf(firstSec.title) + '">Story</button>' : '') +
      (nRev ? '<button type="button" data-jump="reviews">Reviews <span class="n">' + nRev + '</span></button>' : '') +
      (nImg + nVid + nFig ? '<button type="button" data-jump="' + (nImg ? 'images' : nVid ? 'videos' : 'figures') + '">Media <span class="n">' + (nImg + nVid + nFig) + '</span></button>' : '') +
      (hasFp ? '<button type="button" data-jump="scale">Scale</button>' : '') +
      '<button type="button" data-jump="references">Sources <span class="n">' + nRef + '</span></button>' +
      '<button type="button" class="xall" data-expand-all aria-pressed="false">Expand all</button>' +
    '</nav>';
    return '<article class="detail">' +
      '<h2 class="dt"' + (forPrint ? '' : ' id="dlg-title"') + '>' + esc(r.name) + '</h2>' +
      '<p class="dplace">' + flag(r) + esc(r.place) + ', ' + esc(r.country) + '</p>' +
      '<div class="dmeta"><span>' + esc(r.type_short) + '</span>' +
        '<span>Card verified ' + esc(r.verified_on || '—') + '</span>' +
        (forPrint ? '' : '<span class="tip">Tap or hover any <span class="ref-demo">R1</span> marker to see its source</span>' +
          '<button type="button" class="linkish" data-copy>Copy link to this reef</button>') + '</div>' +
      nav +
      glanceHTML(r) +
      accHTML(pfx, 'quick-facts', 'Quick facts', quickFacts(r), o) +
      story +
      (nRev ? accHTML(pfx, 'reviews', 'Reviews by real people', reviewsBody(r), { forPrint: forPrint, count: nRev, cls: 'acc-rv',
        peek: short(stripRefs((r.reviews[0] || {}).quote_or_summary).replace(/^["“]/, ''), 120) + ' — ' + (r.reviews[0].who || '') }) : '') +
      (nImg ? accHTML(pfx, 'images', 'Images', imagesBody(r), { forPrint: forPrint, count: nImg }) : '') +
      (nVid ? accHTML(pfx, 'videos', 'Videos', videosBody(r), { forPrint: forPrint, count: nVid }) : '') +
      (nFig ? accHTML(pfx, 'figures', 'Lior\'s figures', liorBody(r), { forPrint: forPrint, count: nFig }) : '') +
      (hasFp ? accHTML(pfx, 'scale', 'Scale & footprint', window.ReefScale.detailSection(r, forPrint), { forPrint: forPrint,
        peek: 'Plan drawing at a common scale, and how we drew it: every number with its source' }) : '') +
      accHTML(pfx, 'references', 'References', '<div class="refs">' + refsHTML(r, forPrint ? pfx + 'ref-' : 'ref-') + '</div>',
        { forPrint: forPrint, count: nRef, peek: 'Every [R#] above, with what each source supports and when it was checked' }) +
    '</article>';
  }

  var dlg = $('#reef-dialog'), lb = $('#lightbox'), openSlug = null;
  function supportsDialog() { return typeof dlg.showModal === 'function'; }

  function mountIframes() {
    $all('.vbox[data-yt]', dlg).forEach(function (box) {
      var f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(box.dataset.yt) + '?start=' + (parseInt(box.dataset.start, 10) || 0) + '&rel=0';
      f.title = box.dataset.title;
      f.loading = 'lazy';
      f.allow = 'accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      f.allowFullscreen = true;
      f.referrerPolicy = 'strict-origin-when-cross-origin';
      box.appendChild(f);
    });
  }

  // ------------------------------------------------------- source pop-up
  /* One reusable pop-up (#ref-pop) that lives INSIDE the reef <dialog>, so it renders in the
     top layer above the dialog. Anchored to the clicked marker, flips above/below and is clamped
     to the viewport; on narrow screens it becomes a bottom sheet. Opens on click / tap / Enter,
     and on hover after a short delay for mouse users. Dismiss: Esc, click outside, × button,
     or opening another marker. */
  var pop = $('#ref-pop');
  var scaleRoot = $('#view-scale');
  var SHEET_MQ = window.matchMedia ? window.matchMedia('(max-width: 599px)') : { matches: false };
  var HOVER_MQ = window.matchMedia ? window.matchMedia('(hover: hover) and (pointer: fine)') : { matches: false };
  var P = { open: false, anchor: null, id: null, pinned: false, hoverT: 0, leaveT: 0, closedAt: -1e9, raf: 0 };
  var MONTHS = 'January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec';
  var DATE_RES = [
    /\b(\d{4}-\d{2}-\d{2})\b/,
    new RegExp('\\b(\\d{1,2}\\s+(?:' + MONTHS + ')\\.?\\s+\\d{4})\\b'),
    new RegExp('\\b((?:' + MONTHS + ')\\.?\\s+\\d{1,2},?\\s+\\d{4})\\b'),
    new RegExp('\\b((?:' + MONTHS + ')\\s+\\d{4})\\b'),
    /\((\d{4}[a-z]?)\)/
  ];
  function parseCitation(ref) {
    var c = String(ref.citation || '');
    var noAcc = c.replace(/\(?\s*accessed\s+[^);,]*\)?/ig, ' ');
    var out = {};
    for (var i = 0; i < DATE_RES.length; i++) { var m = DATE_RES[i].exec(noAcc); if (m) { out.date = m[1]; break; } }
    var a = /^(.{3,90}?)\s*\((?:\d{4}|n\.d\.|undated|accessed)/i.exec(c);
    if (a && !/https?:|\//.test(a[1])) out.author = a[1].replace(/[.,;:]\s*$/, '');
    if (safeUrl(ref.url)) out.site = hostOf(ref.url);
    return out;
  }
  function popHTML(r, ref) {
    var p = parseCitation(ref), meta = [];
    if (p.author) meta.push('<span><i>by</i> ' + esc(p.author) + '</span>');
    if (p.site) meta.push('<span>' + esc(p.site) + '</span>');
    if (p.date) meta.push('<span>' + esc(p.date) + '</span>');
    var hasUrl = !!safeUrl(ref.url);
    return '<div class="rp-head"><span class="rp-id">' + esc(ref.id) + '</span>' +
        '<span class="rp-kind">' + (hasUrl ? 'Source' : 'Internal project note') + '</span>' +
        '<button type="button" class="rp-x" data-pop-close aria-label="Close source pop-up">×</button></div>' +
      '<p class="rp-cite" id="ref-pop-title">' + esc(ref.citation || '(no citation text)') + '</p>' +
      (meta.length ? '<p class="rp-meta">' + meta.join('<span aria-hidden="true"> · </span>') + '</p>' : '') +
      (ref.supports ? '<div class="rp-sup"><span class="rp-lab">Supports</span>' + esc(ref.supports) + '</div>' : '') +
      (ref.also_note ? '<p class="rp-acc">' + esc(ref.also_note) + (safeUrl(ref.also_url) ? ' ' + extLink(ref.also_url, 'open ↗') : '') + '</p>' : '') +
      '<p class="rp-acc">Accessed ' + esc(ref.accessed || '—') +
        (ref.origin ? ' · <span class="tag tag-gem">' + esc(ref.origin) + '</span>' : '') + '</p>' +
      '<div class="rp-actions">' +
        (hasUrl ? '<a class="rp-open" href="' + esc(ref.url) + '" target="_blank" rel="noopener noreferrer">Open source ↗</a>'
                : '<span class="rp-nourl">(internal note — no URL)</span>') +
        '<button type="button" class="rp-btn" data-pop-list>Show in list</button>' +
        '<button type="button" class="rp-btn" data-pop-copy>Copy citation</button>' +
      '</div>';
  }
  function positionPop() {
    P.raf = 0;
    if (!P.open || !P.anchor) return;
    var sheet = SHEET_MQ.matches;
    pop.classList.toggle('sheet', sheet);
    if (sheet) { pop.style.left = ''; pop.style.top = ''; pop.style.maxHeight = ''; return; }
    var rect = P.anchor.getBoundingClientRect();
    var vw = document.documentElement.clientWidth, vh = window.innerHeight, m = 12, gap = 8;
    if (!document.contains(P.anchor) || (rect.width === 0 && rect.height === 0) || rect.bottom < 0 || rect.top > vh) { closePop(false); return; }
    pop.style.maxHeight = '';
    var w = pop.offsetWidth, h = pop.offsetHeight;
    var below = vh - rect.bottom - gap - m, above = rect.top - gap - m, top, place;
    if (h <= below) { top = rect.bottom + gap; place = 'below'; }
    else if (h <= above) { top = rect.top - gap - h; place = 'above'; }
    else if (below >= above) { pop.style.maxHeight = Math.max(120, below) + 'px'; top = rect.bottom + gap; place = 'below'; }
    else { pop.style.maxHeight = Math.max(120, above) + 'px'; top = rect.top - gap - pop.offsetHeight; place = 'above'; }
    var left = Math.max(m, Math.min(rect.left + rect.width / 2 - w / 2, vw - w - m));
    pop.style.left = Math.round(left) + 'px';
    pop.style.top = Math.round(top) + 'px';
    pop.setAttribute('data-place', place);
    pop.style.setProperty('--caret-x', Math.round(Math.max(16, Math.min(w - 16, rect.left + rect.width / 2 - left))) + 'px');
  }
  function schedulePos() { if (P.open && !P.raf) P.raf = requestAnimationFrame(positionPop); }
  function slugFor(anchor) {
    var host = anchor.closest('[data-slug]');
    return dlg.contains(anchor) ? openSlug : (host ? host.getAttribute('data-slug') : null);
  }
  function openPop(anchor, how) {
    var slug = slugFor(anchor), r = BY_SLUG[slug], id = anchor.getAttribute('data-ref');
    // the pop-up lives inside the reef <dialog> (top layer) when used there, else in <body>
    var home = dlg.contains(anchor) ? dlg : document.body;
    if (pop.parentNode !== home) { closePop(false); home.appendChild(pop); }
    var ref = r && refById(r, id);
    if (!ref) return;
    clearTimeout(P.hoverT); clearTimeout(P.leaveT);
    if (P.anchor && P.anchor !== anchor) P.anchor.setAttribute('aria-expanded', 'false');
    var same = P.open && P.anchor === anchor;
    P.anchor = anchor; P.id = id; P.slug = slug;
    P.pinned = how !== 'hover' || (same && P.pinned);
    if (!same) {
      pop.innerHTML = popHTML(r, ref);
      pop.setAttribute('aria-label', 'Source ' + id);
      pop.hidden = false;
      pop.classList.remove('show');
      P.open = true;
      var ar = anchor.getBoundingClientRect();
      if (ar.bottom < 0 || ar.top > window.innerHeight) anchor.scrollIntoView({ block: 'center' });
      positionPop();
      if (!P.open) return;                          // anchor not visible (e.g. inside a collapsed section)
      void pop.offsetWidth;                         // restart the fade-in
      pop.classList.add('show');
    }
    anchor.setAttribute('aria-expanded', 'true');
    if (how !== 'hover') pop.focus({ preventScroll: true });
  }
  function closePop(returnFocus) {
    clearTimeout(P.hoverT); clearTimeout(P.leaveT);
    if (!P.open) return;
    var a = P.anchor;
    P.open = false; P.pinned = false; P.anchor = null; P.id = null; P.closedAt = performance.now();
    pop.hidden = true; pop.classList.remove('show', 'sheet'); pop.innerHTML = '';
    if (a) { a.setAttribute('aria-expanded', 'false'); if (returnFocus && document.contains(a)) a.focus({ preventScroll: true }); }
  }
  function copyCitation(btn) {
    var r = BY_SLUG[P.slug], ref = r && refById(r, P.id);
    if (!ref) return;
    var text = ref.citation + (safeUrl(ref.url) ? ' ' + ref.url : '') + (ref.accessed ? ' (accessed ' + ref.accessed + ')' : '');
    var done = function (msg) { btn.textContent = msg; setTimeout(function () { if (document.contains(btn)) btn.textContent = 'Copy citation'; }, 2000); };
    var fallback = function () {
      var el = $('.rp-cite', pop), sel = window.getSelection(), rg = document.createRange();
      rg.selectNodeContents(el); sel.removeAllRanges(); sel.addRange(rg);
      done('Selected — press Ctrl+C');
    };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { done('Copied'); }, fallback);
    else fallback();
  }

  // ------------------------------------------------------- accordion helpers
  function setAll(open) {
    $all('details.acc', dlg).forEach(function (d) { d.open = open; });
    var b = $('[data-expand-all]', dlg);
    if (b) { b.textContent = open ? 'Collapse all' : 'Expand all'; b.setAttribute('aria-pressed', String(open)); }
  }
  function syncExpandBtn() {
    var ds = $all('details.acc', dlg), b = $('[data-expand-all]', dlg);
    if (!b || !ds.length) return;
    var all = ds.every(function (d) { return d.open; });
    b.textContent = all ? 'Collapse all' : 'Expand all';
    b.setAttribute('aria-pressed', String(all));
  }
  /* Smooth scroll inside the dialog, with an instant fallback: some embedded browsers drop
     smooth scrolls of a nested scroller, which would leave the reader where they were. */
  function scrollToEl(el, block) {
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    el.scrollIntoView({ block: block, behavior: reduce ? 'auto' : 'smooth' });
    if (reduce) return;
    setTimeout(function () {
      var box = $('.dlg-inner', dlg);
      if (!box || !document.contains(el)) return;
      var top = el.getBoundingClientRect().top - box.getBoundingClientRect().top;
      var want = block === 'center' ? (box.clientHeight - el.offsetHeight) / 2 : 0;
      if (Math.abs(top - want) > 120) el.scrollIntoView({ block: block, behavior: 'auto' });
    }, 700);
  }
  function jumpTo(key) {
    var d = document.getElementById('d-' + key);
    if (!d) return;
    d.open = true;
    scrollToEl(d, 'start');
    var s = $('summary', d);
    if (s) s.focus({ preventScroll: true });
  }

  function openReef(slug, refId, fromHash) {
    var r = BY_SLUG[slug];
    if (!r) return;
    // Re-open even when the same reef was shown before: a closed dialog always gets a fresh open
    // (don't rely on openSlug/hash state, which a pending 'close' event may not have reset yet).
    if (openSlug !== slug || !dlg.open) {
      closePop(false);
      if (!dlg.open) lastFocus = document.activeElement;
      $('#dlg-body').innerHTML = detailHTML(r, false);
      openSlug = slug;
      if (!dlg.open) {
        if (supportsDialog()) dlg.showModal(); else dlg.setAttribute('open', '');
        document.body.classList.add('dlg-open');
      }
      mountIframes();                              // iframes exist only while the dialog is open
      $('.dlg-inner', dlg).scrollTop = 0;
      $('.dlg-close', dlg).focus({ preventScroll: true });
    }
    var h = '#reef/' + slug + (refId ? '/' + refId : '');
    if (!fromHash && location.hash !== h) history.replaceState(null, '', h);
    if (refId) highlightRef(refId);
  }
  function highlightRef(id) {
    var li = document.getElementById('ref-' + id);
    if (!li) return;
    var d = li.closest('details');
    if (d) { d.open = true; syncExpandBtn(); }
    $all('.refs li.hl', dlg).forEach(function (x) { x.classList.remove('hl'); });
    li.classList.add('hl');
    scrollToEl(li, 'center');
    li.setAttribute('tabindex', '-1');
    li.focus({ preventScroll: true });
  }
  function closeReef() { if (dlg.open) { if (supportsDialog()) dlg.close(); else { dlg.removeAttribute('open'); onDialogClosed(); } } }
  function onDialogClosed() {
    if (dlg.open) return;                          // stale 'close' event after a quick re-open
    closePop(false);
    $('#dlg-body').innerHTML = '';                 // destroys iframes
    openSlug = null;
    document.body.classList.remove('dlg-open');
    if (/^#reef\//.test(location.hash)) history.replaceState(null, '', state.view === 'gallery' ? location.pathname + location.search : '#view/' + state.view);
    if (lastFocus && document.contains(lastFocus)) lastFocus.focus({ preventScroll: true });
    else {
      var t = document.querySelector('[data-open]');
      if (t) t.focus({ preventScroll: true });
    }
  }

  function openLightbox(fig) {
    var img = $('img', fig);
    if (!img || img.hidden || img.style.display === 'none') return;
    var cap = $('figcaption', fig);
    $('#lb-media').innerHTML = '<img src="' + esc(img.getAttribute('src')) + '" alt="' + esc(img.alt) + '" referrerpolicy="no-referrer">';
    $('#lb-cap').innerHTML = cap ? cap.innerHTML : '';
    // the caption may carry source markers; in the lightbox they are plain text
    $all('.ref-mark', $('#lb-cap')).forEach(function (b) { var s = document.createElement('span'); s.textContent = b.textContent; b.replaceWith(s); });
    if (typeof lb.showModal === 'function') lb.showModal(); else lb.setAttribute('open', '');
  }

  function routeFromHash() {
    var m = /^#reef\/([a-z0-9-]+)(?:\/([RS]\d+))?$/i.exec(location.hash);
    var vm = /^#view\/(gallery|table|models3d)(?:\/[a-z0-9-]+)?$/.exec(location.hash);
    if (vm && state.view !== vm[1]) setView(vm[1]);
    if (m && BY_SLUG[m[1]]) openReef(m[1], m[2], true);
    else if (dlg.open && !/^#reef\//.test(location.hash)) closeReef();
  }

  // ---------------------------------------------------- references index
  function renderRefIndex() {
    $('#refindex').innerHTML = REEFS.map(function (r) {
      return '<details><summary>' + esc(r.name) + ' <span class="muted">(' + (r.references || []).length + ' references)</span></summary>' +
        '<div class="refs">' + refsHTML(r, 'idx-' + r.slug + '-') + '</div>' +
        '<p><button type="button" class="linkish" data-open="' + esc(r.slug) + '">Open ' + esc(r.name) + '</button></p></details>';
    }).join('');
  }

  function renderFooter() {
    $('#footer').innerHTML =
      '<p><strong>Method.</strong> Research agents gathered each reef\'s record from primary and secondary sources; separate agents then verified every claim against its cited source, and ' +
      'every image and video was checked to show the named site. Verification reports are kept in the project folder <code>05_qa</code>. ' +
      'Only facts carrying a reference tag [R#] are shown; conflicts between sources are stated, not resolved. Dollar conversions marked approximate are rough, mostly unsourced estimates.</p>' +
      '<p>Some reviews and references were first spotted in a parallel survey made with another AI (Gemini). None was taken on trust: each was re-fetched from its original source and checked by our own agents before being added, and is tagged <span class="tag tag-gem">via Gemini survey, verified 2026-09-25</span>.</p>' +
      '<p>Compiled ' + esc(META.compiled_on) + ' · <a href="#references">References index</a> · Sections 2 and 3 in preparation.</p>' +
      '<p>Images are hotlinked from their sources and remain the property of their owners; credits are shown on each. Video embeds are served by YouTube (privacy-enhanced mode).</p>';
  }

  // ---------------------------------------------------------------- print
  function preparePrint() {
    closePop(false);
    var pa = $('#print-all');
    var list = openSlug ? [BY_SLUG[openSlug]] : current();
    document.documentElement.classList.toggle('print-one', !!openSlug);
    pa.innerHTML = list.map(function (r) { return detailHTML(r, true); }).join('');   // every section open
    $all('details', document).forEach(function (d) { if (!d.open) { d.setAttribute('data-print-opened', ''); d.open = true; } });
    $all('img[loading="lazy"]', pa).forEach(function (i) { i.loading = 'eager'; });
  }
  function afterPrint() {
    $('#print-all').innerHTML = '';
    document.documentElement.classList.remove('print-one');
    $all('details[data-print-opened]', document).forEach(function (d) { d.open = false; d.removeAttribute('data-print-opened'); });
  }

  // --------------------------------------------------------------- events
  function bind() {
    $('#q').addEventListener('input', function (e) { state.q = e.target.value.trim(); render(); });
    $('#sort').addEventListener('change', function (e) {
      var p = e.target.value.split(':'); state.sort = p[0]; state.dir = Number(p[1]); render();
    });
    // round 10: the view buttons live in the sticky top bar; choosing one shows that view from its top
    function toViewTop() {
      var s = $('#survey'), nav = $('#topnav');
      window.scrollTo(0, Math.max(0, s.getBoundingClientRect().top + window.pageYOffset - (nav ? nav.offsetHeight : 0) - 6));
    }
    $all('.views button').forEach(function (b) { b.addEventListener('click', function () { showNotice(''); setView(b.dataset.view); if (b.dataset.view === 'gallery') window.scrollTo(0, 0); else toViewTop(); }); });
    $all('[data-home]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); showNotice(''); setView('gallery'); window.scrollTo(0, 0); }); });
    var toTop = $('#to-top');
    if (toTop) {
      toTop.addEventListener('click', function () { window.scrollTo(0, 0); var f = $('.views button[aria-pressed="true"]'); if (f) f.focus({ preventScroll: true }); });
      var onScroll = function () { toTop.hidden = window.pageYOffset < 700; };
      window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
    }
    bindInfo();

    document.addEventListener('click', function (e) {
      var t = e.target;
      // --- source pop-up: marker, controls inside it, and click-outside dismissal
      var mark = t.closest('.ref-mark');
      if (mark && (dlg.contains(mark) || (scaleRoot && scaleRoot.contains(mark)))) {
        e.preventDefault();
        if (P.open && P.anchor === mark && P.pinned) closePop(true);
        else openPop(mark, e.detail === 0 ? 'key' : 'click');
        return;
      }
      if (P.open && pop.contains(t)) {
        if (t.closest('[data-pop-close]')) { closePop(true); return; }
        if (t.closest('[data-pop-list]')) { var id = P.id, ps = P.slug; closePop(false); openReef(ps, id); return; }
        if (t.closest('[data-pop-copy]')) { copyCitation(t.closest('[data-pop-copy]')); return; }
        return;                                    // links inside the pop-up work normally
      }
      if (P.open) closePop(false);                 // any click elsewhere closes it
      // --- in-dialog jump bar and expand/collapse
      var jb = t.closest('[data-jump]');
      if (jb) { jumpTo(jb.dataset.jump); return; }
      var xa = t.closest('[data-expand-all]');
      if (xa) { setAll(xa.getAttribute('aria-pressed') !== 'true'); return; }

      var chip = t.closest('.chip');
      if (chip) {
        var set = state[FIELD_TO_STATE[chip.dataset.f]], v = chip.dataset.v;
        if (set[v]) delete set[v]; else set[v] = true;
        chip.setAttribute('aria-pressed', String(!!set[v]));
        render();
        return;
      }
      if (t.closest('[data-clear]')) {
        state.q = ''; state.verdict = {}; state.country = {}; state.type = {};
        $('#q').value = '';
        $all('.chip').forEach(function (c) { c.setAttribute('aria-pressed', 'false'); });
        render();
        return;
      }
      var sortBtn = t.closest('th [data-sort]');
      if (sortBtn) {
        var k = sortBtn.dataset.sort;
        if (state.sort === k) state.dir = -state.dir; else { state.sort = k; state.dir = (k === 'cost' || k === 'refs') ? -1 : 1; }
        render();
        var again = document.querySelector('th [data-sort="' + k + '"]');
        if (again) again.focus();
        return;
      }
      if (t.closest('[data-copy]')) {
        var url = location.href.split('#')[0] + '#reef/' + openSlug;
        var btn = t.closest('[data-copy]');
        var ok = function () { btn.textContent = 'Link copied'; };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(ok, function () { btn.textContent = url; });
        else btn.textContent = url;
        return;
      }
      var z = t.closest('[data-zoom]');
      if (z) { openLightbox(z.closest('figure')); return; }
      if (t.closest('[data-close]')) {
        var d = t.closest('dialog');
        if (d === lb) lb.close(); else closeReef();
        return;
      }
      if (t.closest('a')) return;                  // let real links work (source links inside tiles etc.)
      var opener = t.closest('[data-open]');
      if (opener) {
        openReef(opener.dataset.open);
      }
    });

    // Hover-to-preview for mouse users: short delay in, short grace period out (so the pointer
    // can travel from the marker onto the pop-up). A clicked (pinned) pop-up ignores hover.
    function onMarkOver(e) {
      if (!HOVER_MQ.matches) return;
      var mark = e.target.closest && e.target.closest('.ref-mark');
      if (mark) {
        clearTimeout(P.leaveT);
        if (P.pinned || (P.open && P.anchor === mark)) return;
        clearTimeout(P.hoverT);
        P.hoverT = setTimeout(function () { if (document.contains(mark) && mark.matches(':hover')) openPop(mark, 'hover'); }, 320);
      } else if (pop.contains(e.target)) {
        clearTimeout(P.leaveT);
      }
    }
    function onMarkOut(e) {
      if (!HOVER_MQ.matches) return;
      var from = e.target.closest && (e.target.closest('.ref-mark') || (pop.contains(e.target) ? pop : null));
      if (!from) return;
      if (e.relatedTarget && (from.contains(e.relatedTarget) || pop.contains(e.relatedTarget))) return;
      clearTimeout(P.hoverT);
      if (P.open && !P.pinned) { clearTimeout(P.leaveT); P.leaveT = setTimeout(function () { if (!P.pinned) closePop(false); }, 260); }
    }
    // hover preview works inside the reef dialog; the pop-up itself
    // (which may live in <body>) keeps itself open while hovered
    dlg.addEventListener('mouseover', onMarkOver);
    dlg.addEventListener('mouseout', onMarkOut);
    if (scaleRoot) {
      scaleRoot.addEventListener('mouseover', onMarkOver);
      scaleRoot.addEventListener('mouseout', onMarkOut);
    }
    pop.addEventListener('mouseover', onMarkOver);
    pop.addEventListener('mouseout', onMarkOut);
    window.addEventListener('scroll', schedulePos, { passive: true });
    $('.dlg-inner', dlg).addEventListener('scroll', schedulePos, { passive: true });
    window.addEventListener('resize', schedulePos);
    dlg.addEventListener('toggle', syncExpandBtn, true);    // <details> toggle events don't bubble: capture

    // Backdrop click closes (the click lands on the <dialog> element itself, outside .dlg-inner);
    // with a source pop-up open, the first backdrop click only closes the pop-up.
    dlg.addEventListener('click', function (e) {
      if (e.target !== dlg) return;
      if (P.open) { closePop(false); e.stopPropagation(); return; }
      closeReef();
    });
    lb.addEventListener('click', function (e) { if (e.target === lb) lb.close(); });
    dlg.addEventListener('close', onDialogClosed);
    var lbClosedAt = -1e9;
    lb.addEventListener('close', function () { $('#lb-media').innerHTML = ''; lbClosedAt = performance.now(); });
    // One Esc closes only the top-most thing: source pop-up, then enlarged image, then the reef.
    // (Chrome can group both dialogs' close requests into one Esc press.)
    lb.addEventListener('cancel', function () { lbClosedAt = performance.now(); });
    dlg.addEventListener('cancel', function (e) {
      var now = performance.now();
      if (P.open || now - P.closedAt < 400 || lb.open || now - lbClosedAt < 400) { e.preventDefault(); closePop(true); }
    });

    // Shared Esc handler (capture phase, runs before the dialogs' own close request)
    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' && e.key !== 'Esc') return;
      if (P.open) { e.preventDefault(); e.stopPropagation(); closePop(true); return; }
      if (!supportsDialog()) {                   // fallback for browsers without <dialog>
        if (lb.open) { lb.removeAttribute('open'); $('#lb-media').innerHTML = ''; }
        else if (dlg.open) closeReef();
      }
    }, true);

    // Image load failures -> neutral placeholder with a "view source" link
    document.addEventListener('error', function (e) {
      var img = e.target;
      if (!img || img.tagName !== 'IMG') return;
      var fb = img.parentNode && img.parentNode.querySelector('.fallback');
      if (fb) { img.hidden = true; fb.hidden = false; var z = img.parentNode.querySelector('[data-zoom]'); if (z) z.hidden = true; }
      else img.style.visibility = 'hidden';
    }, true);

    window.addEventListener('hashchange', routeFromHash);
    window.addEventListener('beforeprint', preparePrint);
    window.addEventListener('afterprint', afterPrint);
  }

  window.ReefInfo = { html: infoHTML };       // (i) pop-over markup for the 3D tab (src/models3d.js)

  // ------------------------------------------------- API for scale.js (Scale view)
  window.ReefApp = {
    REEFS: REEFS, BY_SLUG: BY_SLUG, VERDICT_COLOR: VERDICT_COLOR, V_BY_KEY: V_BY_KEY,
    esc: esc, safeUrl: safeUrl, extLink: extLink, refById: refById, markBtn: markBtn, badge: badge,
    imgTag: imgTag, short: short, flag: flag, openReef: openReef, closeReef: closeReef, closePop: closePop, setView: setView,
    rerender: function () { render(); }
  };

  // ----------------------------------------------------------------- init
  renderHeader();
  renderChips();
  renderRefIndex();
  renderFooter();
  bind();
  var initView = /^#view\/(gallery|table|models3d)(?:\/[a-z0-9-]+)?$/.exec(location.hash);
  setView(initView ? initView[1] : 'gallery');
  routeFromHash();
})();

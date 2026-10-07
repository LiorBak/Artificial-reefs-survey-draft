/* Scale view — every reef's footprint drawn in plan at ONE common scale.
   Inlined by build.py before app.js; talks to app.js through window.ReefApp (set at app.js init).
   Geometry source: reef.footprint (compiled from 07_scale/reefs/<slug>.footprint.json).
   Coordinates are metres: x = alongshore, y = offshore (positive seaward), shoreline = the line y = 0.
   The same drawing rules are ported to Python in 07_scale/make_drawings.py (keep the two in step). */
(function () {
  'use strict';

  // ------------------------------------------------------------ constants
  // FIFA-recommended pitch, 105 x 68 m (Wikipedia "Football pitch", checked 2026-09-25)
  var PITCH = { L: 105, W: 68, area: 105 * 68, url: 'https://en.wikipedia.org/wiki/Football_pitch' };
  // panel drawing margins, in screen px (independent of the scale)
  var G = { ML: 16, MR: 16, MT: 30, BEACH: 24, MB: 34, PAD_M: 15, MIN_HALF_M: 75, BAR_M: 100 };
  var ZOOMS = [0.125, 0.25, 0.5, 1, 2, 4, 8];
  // overlay palette (13 distinct hues, fixed per reef by area rank)
  var PALETTE = ['#4e79a7', '#e15759', '#59a14f', '#f28e2b', '#b07aa1', '#9c755f', '#ff9da7',
                 '#76b7b2', '#edc948', '#bab0ac', '#1f9fd4', '#d37295', '#8cd17d'];
  var VCSS = { 'worked': '--v-worked', 'partly worked': '--v-partly', 'mixed': '--v-mixed', 'failed': '--v-failed', 'n-a': '--v-na' };

  var S = {
    scale: (window.innerWidth || 1200) < 700 ? 0.5 : 1,
    sort: 'desc',
    align: 'shore',          // overlay: 'shore' = true offshore position, 'centroid' = all centroids on one point
    pitch: true,
    hidden: {},              // overlay: slug -> true when toggled off
    tsort: 'area',           // comparison table: current sort column
    tdir: -1,                // comparison table: 1 = ascending, -1 = descending
    list: []
  };

  function A() { return window.ReefApp; }
  function esc(s) { return A().esc(s); }
  function fmt(n, d) {
    if (n == null || isNaN(n)) return '—';
    var v = Number(n);
    return v.toLocaleString('en-US', { maximumFractionDigits: d == null ? (Math.abs(v) < 10 ? 1 : 0) : d });
  }
  function pitches(area) {
    var p = area / PITCH.area;
    if (p >= 10) return fmt(p, 0);
    if (p >= 1) return fmt(p, 1);
    return Number(p.toPrecision(2)).toString();
  }
  function fp(r) { return r.footprint; }
  function area(r) { return fp(r) ? (fp(r).area_m2 || fp(r).area_computed_m2 || 0) : 0; }
  function vfill(r) { return 'var(' + (VCSS[r.verdict] || '--v-na') + ')'; }

  /* Text -> escaped HTML with every bare R#/S# id that exists for this reef turned into a
     source-marker button (opens the source pop-up). */
  var ID_RE = /\b([RS]\d{1,3})\b/g;
  function linkRefs(text, r) {
    if (text == null || text === '') return '';
    if (typeof text !== 'string') text = String(text);
    return esc(text).replace(ID_RE, function (m, id) { return A().refById(r, id) ? A().markBtn(r, id) : m; });
  }
  function idsIn(text, r) {
    var out = [];
    String(text == null ? '' : text).replace(ID_RE, function (m, id) {
      if (A().refById(r, id) && out.indexOf(id) < 0) out.push(id);
      return m;
    });
    return out;
  }
  function marks(ids, r) {
    return ids.length ? '<sup class="refs">[' + ids.map(function (id) { return A().markBtn(r, id); }).join(', ') + ']</sup>' : '';
  }
  /* Source ids of the derivation rows whose quantity matches `re` (and not `not`). */
  function derivIds(r, re, not) {
    var ids = [];
    (fp(r).derivation || []).forEach(function (d) {
      var q = String(d.quantity || '');
      if (re.test(q) && !(not && not.test(q))) idsIn(d.source_ref, r).forEach(function (id) { if (ids.indexOf(id) < 0) ids.push(id); });
    });
    return ids;
  }

  // ------------------------------------------------------------ geometry
  /* Frame of one panel, in metres, and the metre -> px mapping at scale s (px per metre).
     Sea at the top, beach at the bottom; the frame is at least 150 m wide so the 100 m bar fits. */
  function panelFrame(f, s) {
    var b = f.geom.bbox;
    var cx = (b.minx + b.maxx) / 2;
    var half = Math.max((b.maxx - b.minx) / 2 + G.PAD_M, G.MIN_HALF_M);
    var top = Math.max(b.maxy, 0) + G.PAD_M;
    var W = G.ML + 2 * half * s + G.MR, H = G.MT + top * s + G.BEACH + G.MB;
    return {
      W: Math.round(W), H: Math.round(H), s: s,
      tx: function (x) { return G.ML + (x - (cx - half)) * s; },
      ty: function (y) { return G.MT + (top - y) * s; }
    };
  }
  function ringPath(ring, tx, ty) {
    return ring.map(function (p, i) { return (i ? 'L' : 'M') + tx(p[0]).toFixed(1) + ' ' + ty(p[1]).toFixed(1); }).join('') + 'Z';
  }
  function nearestPoint(f) {
    var best = null;
    f.polygons.forEach(function (ring) { ring.forEach(function (p) { if (!best || p[1] < best[1]) best = p; }); });
    return best;
  }

  /* One reef's plan drawing at s px per metre. */
  function panelSVG(r, s) {
    var f = fp(r), fr = panelFrame(f, s), tx = fr.tx, ty = fr.ty, W = fr.W, H = fr.H;
    var y0 = ty(0), o = [];
    o.push('<svg class="sc-svg" xmlns="http://www.w3.org/2000/svg" width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' +
      esc('Plan of ' + r.name + ' at ' + s + ' pixel per metre: ' + fmt(f.bbox_m && f.bbox_m.length_alongshore) + ' m alongshore by ' +
        fmt(f.bbox_m && f.bbox_m.width_crossshore) + ' m cross-shore, shoreline at the bottom') + '">');
    o.push('<rect class="sc-sea" x="0" y="0" width="' + W + '" height="' + y0.toFixed(1) + '"/>');
    o.push('<rect class="sc-sand" x="0" y="' + y0.toFixed(1) + '" width="' + W + '" height="' + G.BEACH + '"/>');
    o.push('<line class="sc-shore" x1="0" x2="' + W + '" y1="' + y0.toFixed(1) + '" y2="' + y0.toFixed(1) + '"/>');
    o.push('<text class="sc-t sc-tm" x="' + (W - G.MR) + '" y="' + (y0 + 15).toFixed(1) + '" text-anchor="end">beach · shoreline (y = 0)</text>');
    // offshore arrow
    var aLen = Math.max(10, Math.min(36, y0 - G.MT + 6));
    o.push('<g class="sc-arrow"><line x1="' + (G.ML + 4) + '" x2="' + (G.ML + 4) + '" y1="' + (y0 - 4).toFixed(1) + '" y2="' + (y0 - 4 - aLen).toFixed(1) + '"/>' +
      '<path d="M' + (G.ML) + ' ' + (y0 - aLen).toFixed(1) + 'l4 -7l4 7z"/></g>');
    o.push('<text class="sc-t sc-tm" x="' + G.ML + '" y="' + (G.MT - 12) + '">↑ offshore (sea)</text>');
    // reef polygon(s)
    o.push('<g class="sc-reef" style="fill:' + vfill(r) + '">' + f.polygons.map(function (ring) {
      return '<path d="' + ringPath(ring, tx, ty) + '"/>';
    }).join('') + '</g>');
    // drawn distance from the shoreline to the nearest point of the drawing
    var np = nearestPoint(f);
    if (np && np[1] * s >= 10) {
      var x = tx(np[0]).toFixed(1);
      o.push('<g class="sc-dim"><line x1="' + x + '" x2="' + x + '" y1="' + y0.toFixed(1) + '" y2="' + ty(np[1]).toFixed(1) + '"/>' +
        '<text class="sc-t" x="' + (Number(x) + 4) + '" y="' + ((y0 + ty(np[1])) / 2 + 4).toFixed(1) + '">' + fmt(np[1], 0) + ' m</text>' +
        '<title>Drawn distance from the shoreline line to the nearest edge of the drawing</title></g>');
    }
    // 100 m scale bar (bottom right)
    var bl = G.BAR_M * s, bx1 = W - G.MR, bx0 = bx1 - bl, by = H - 12;
    o.push('<g class="sc-bar"><rect x="' + bx0.toFixed(1) + '" y="' + (by - 5) + '" width="' + (bl / 2).toFixed(1) + '" height="5"/>' +
      '<rect class="sc-bar2" x="' + (bx0 + bl / 2).toFixed(1) + '" y="' + (by - 5) + '" width="' + (bl / 2).toFixed(1) + '" height="5"/>' +
      '<text class="sc-t" x="' + bx0.toFixed(1) + '" y="' + (by - 9) + '">0</text>' +
      '<text class="sc-t" x="' + bx1 + '" y="' + (by - 9) + '" text-anchor="end">100 m</text></g>');
    o.push('<text class="sc-t sc-tm" x="' + G.ML + '" y="' + (H - 7) + '">1 px = ' + fmt(1 / s, 3) + ' m</text>');
    o.push('</svg>');
    return o.join('');
  }

  // ------------------------------------------------------------ panel parts
  function confBadge(f) {
    var k = f.confidence_level || 'unknown';
    return '<span class="sc-conf conf-' + esc(k) + '" title="' + esc(f.confidence || '') + '">' + esc(k) + ' confidence</span>';
  }
  function factsHTML(r) {
    var f = fp(r), b = f.bbox_m || {}, cr = f.crest_depth_m || {}, di = f.distance_offshore_m || {};
    var dimIds = derivIds(r, /length|width|diameter|dimension|footprint|size|span|extent|arm|chord|topolog|shape|plan/i, /depth|offshore|distance|crest|volume|area|height/i);
    var areaIds = derivIds(r, /area/i);
    var crestIds = idsIn(cr.ref, r), distIds = idsIn(di.ref, r);
    var est = '<span class="sc-est" title="Not a published figure: derived from our own drawing or an estimate; see How we drew this">derived</span>';
    return '<dl class="sc-facts">' +
      '<div><dt>Plan box, L × W</dt><dd>' + fmt(b.length_alongshore) + ' × ' + fmt(b.width_crossshore) + ' m' + marks(dimIds, r) +
        '<small>alongshore × cross-shore' + (b.note ? '; see note' : '') + '</small></dd></div>' +
      '<div><dt>Footprint area</dt><dd>' + fmt(f.area_m2) + ' m²' + (areaIds.length ? marks(areaIds, r) : ' ' + est) +
        '<small>≈ ' + pitches(f.area_m2) + ' × a football pitch (105 × 68 m)</small></dd></div>' +
      '<div><dt>Crest depth</dt><dd>' + esc(f.crest_label || '—') + (crestIds.length ? marks(crestIds, r) : (cr.value != null ? ' ' + est : '')) + '</dd></div>' +
      '<div><dt>Distance offshore</dt><dd>' + esc(f.distance_label || '—') + (distIds.length ? marks(distIds, r) : (di.value != null ? ' ' + est : '')) + '</dd></div>' +
      '<div><dt>Shape</dt><dd title="' + esc(f.shape_type || '') + '">' + esc(f.shape_short || '—') + '</dd></div>' +
    '</dl>';
  }

  function valCell(d) {
    var v = d.value;
    if (v == null || v === '') return '—';
    var u = d.unit && d.unit !== 'n/a' ? ' ' + d.unit : '';
    return esc(typeof v === 'number' ? fmt(v, 2) : String(v)) + esc(u);
  }
  function howHTML(r) {
    var f = fp(r), o = [];
    var der = f.derivation || [];
    o.push('<h4>1 · Derivation: every quantity, how we got it, and from where</h4>');
    o.push('<div class="sc-tw"><table class="sc-tab sc-deriv"><colgroup><col style="width:15%"><col style="width:11%"><col style="width:34%"><col style="width:13%"><col style="width:27%"></colgroup><thead><tr><th>Quantity</th><th>Value</th><th>Method, and the quote or figure relied on</th><th>Source</th><th>Uncertainty</th></tr></thead><tbody>' +
      der.map(function (d) {
        var src = String(d.source_ref == null ? '' : d.source_ref);
        var ids = idsIn(src, r);
        return '<tr><td>' + esc(d.quantity) + '</td><td class="nw">' + valCell(d) + '</td>' +
          '<td>' + linkRefs(d.method, r) + (d.quote_or_figure ? '<q class="sc-q">' + linkRefs(d.quote_or_figure, r) + '</q>' : '') + '</td>' +
          '<td>' + (ids.length ? linkRefs(src, r) : '<span class="sc-est">' + esc(src || 'derived') + '</span>') + '</td>' +
          '<td>' + linkRefs(d.uncertainty, r) + '</td></tr>';
      }).join('') + '</tbody></table></div>');

    var imgs = f.images_relied_on || [];
    o.push('<h4>2 · Images and figures relied on</h4>');
    o.push(imgs.length ? '<ul class="sc-imgs">' + imgs.map(function (im) {
      if (im.withheld) {
        return '<li class="sc-withheld"><div class="sc-imtxt"><b>Image withheld</b> — ' + esc(im.what_it_is) +
          (im.what_was_read_off_it ? '<p><span class="sc-lab">What was read off it</span>' + linkRefs(im.what_was_read_off_it, r) + '</p>' : '') + '</div></li>';
      }
      var u = A().safeUrl(im.url), sp = A().safeUrl(im.source_page);
      var thumb = im.thumb_ok && u ? '<a class="sc-thumb" href="' + esc(sp || u) + '" target="_blank" rel="noopener noreferrer">' + A().imgTag(u, 'Image relied on: ' + A().short(im.what_it_is || '', 80)) + '</a>' : '';
      var links = [];
      if (u) links.push(A().extLink(u, im.accepted ? 'image (in this reef\'s accepted media) ↗' : 'image / document ↗'));
      if (sp && sp !== u) links.push(A().extLink(sp, 'source page ↗'));
      if (!u && im.url) links.push('<span class="muted">' + esc(im.url) + '</span>');
      return '<li>' + thumb + '<div class="sc-imtxt"><p>' + linkRefs(im.what_it_is, r) + '</p>' +
        (im.what_was_read_off_it ? '<p><span class="sc-lab">What was read off it</span>' + linkRefs(im.what_was_read_off_it, r) + '</p>' : '') +
        (links.length ? '<p class="sc-links">' + links.join(' · ') + '</p>' : '') + '</div></li>';
    }).join('') + '</ul>' : '<p class="muted">No image or figure was used; the drawing rests on the text sources above.</p>');

    o.push('<h4>3 · Coordinate conventions and notes</h4><dl class="sc-notes">');
    var note = function (k, v) { if (v) o.push('<dt>' + esc(k) + '</dt><dd>' + linkRefs(v, r) + '</dd>'); };
    note('Coordinates', f.coords);
    note('Shape', f.shape_type_notes || f.shape_type);
    note('Polygon', f.polygon_components_notes || f.polygon_notes);
    note('Orientation', f.orientation_notes);
    note('Plan box note', f.bbox_m && (f.bbox_m.note || f.bbox_m.length_alongshore_note));
    note('Other published size', f.bbox_alt_note);
    note('Area', f.area_m2_notes || ('Shoelace area of the polygon above: ' + fmt(f.area_computed_m2) + ' m² (stored value ' + fmt(f.area_m2) + ' m²).'));
    note('Crest depth datum', f.crest_depth_m && [f.crest_depth_m.datum, f.crest_depth_m.notes, f.crest_depth_m.confidence_note].filter(Boolean).join(' '));
    note('Crest depth over time', f.crest_depth_alt_note);
    note('Distance measured from', f.distance_offshore_m && [f.distance_offshore_m.measured_from, f.distance_offshore_m.notes, f.distance_offshore_m.note, f.distance_offshore_m.confidence_note].filter(Boolean).join(' '));
    note('Materials', f.materials);
    note('Confidence', f.confidence);
    o.push('</dl>');

    var gc = f.gemini_comparison || {};
    o.push('<h4>4 · Gemini comparison <span class="muted">(Gemini\'s values are unverified; shown only to explain differences)</span></h4>');
    if ((gc.agree || []).length) o.push('<p><span class="sc-lab">Where we agree</span></p><ul class="sc-ul">' + gc.agree.map(function (a) { return '<li>' + linkRefs(a, r) + '</li>'; }).join('') + '</ul>');
    if ((gc.disagree || []).length) {
      o.push('<div class="sc-tw"><table class="sc-tab"><thead><tr><th>Quantity</th><th>Gemini</th><th>Ours</th><th>Why ours</th></tr></thead><tbody>' +
        gc.disagree.map(function (d) {
          return '<tr><td>' + esc(d.quantity) + '</td><td>' + esc(d.gemini) + '</td><td>' + linkRefs(d.ours, r) + '</td><td>' + linkRefs(d.why_ours, r) + '</td></tr>';
        }).join('') + '</tbody></table></div>');
    }

    o.push('<h4>5 · Open issues</h4>');
    o.push((f.open_issues || []).length ? '<ul class="sc-ul">' + f.open_issues.map(function (x) { return '<li>' + linkRefs(x, r) + '</li>'; }).join('') + '</ul>' : '<p class="muted">None recorded.</p>');

    var ver = f.verification || [];
    o.push('<h4>6 · Verification</h4><p>Status: <b>' + esc(f.status || '—') + '</b> · verified on ' + esc(f.verified_on || '—') +
      ' · ' + ver.length + ' checks by a separate verification pass.</p>');
    if (ver.length) {
      o.push('<details class="sc-ver"><summary>Show the ' + ver.length + ' checks</summary><div class="sc-tw"><table class="sc-tab"><thead><tr><th>Item</th><th>Verdict</th><th>Evidence</th></tr></thead><tbody>' +
        ver.map(function (v) {
          if (typeof v === 'string') return '<tr><td colspan="3">' + linkRefs(v, r) + '</td></tr>';
          return '<tr><td>' + linkRefs(v.item, r) + '</td><td>' + esc(v.verdict) + '</td><td>' + linkRefs(v.evidence, r) + '</td></tr>';
        }).join('') + '</tbody></table></div></details>');
    }
    if (f.provenance_md) {
      o.push('<p class="sc-prov">Full provenance write-up: <a href="' + esc(f.provenance_md) + '" target="_blank" rel="noopener">' + esc(f.provenance_md) + '</a>' +
        ' <span class="muted">(copy of ' + esc(f.provenance_src) + ')</span></p>');
    }
    return o.join('');
  }

  function panelHTML(r, s) {
    var f = fp(r), w = panelFrame(f, s).W + 30;     // panel at least as wide as its drawing (wraps on small screens)
    return '<article class="sc-panel" data-slug="' + esc(r.slug) + '" id="sc-' + esc(r.slug) + '" style="flex-basis:' + Math.max(300, w) + 'px">' +
      '<header class="sc-head"><h3><button type="button" class="linkish sc-name" data-open="' + esc(r.slug) + '">' + esc(r.name) + '</button></h3>' +
        '<p class="sc-sub">' + A().flag(r) + esc(r.place_short || '') + ' · ' + esc(r.year_short || '') + '</p>' +
        '<div class="sc-badges">' + A().badge(r) + ' ' + confBadge(f) + '</div></header>' +
      '<button type="button" class="sc-drawbtn" data-open="' + esc(r.slug) + '" aria-label="' + esc('Open the full record of ' + r.name) + '">' + panelSVG(r, s) + '</button>' +
      factsHTML(r) +
      '<details class="sc-how" data-how="' + esc(r.slug) + '"><summary>How we drew this <span class="muted">— ' + (f.derivation || []).length + ' derived quantities, ' +
        (f.images_relied_on || []).length + ' images/figures, ' + f.gemini_n_disagree + ' disagreements with Gemini</span></summary>' +
        '<div class="sc-how-b">' + howHTML(r) + '</div></details>' +
    '</article>';
  }

  // ------------------------------------------------------------ overlay
  function overlayOffsets(r) {
    var c = fp(r).geom.centroid;
    return S.align === 'centroid' ? [-c[0], -c[1]] : [-c[0], 0];
  }
  function niceBar(span) {
    var c = [5, 10, 20, 25, 50, 100, 200, 250, 500, 1000], t = span / 5, best = c[0];
    c.forEach(function (x) { if (x <= t) best = x; });
    return best;
  }
  function overlaySVG(list) {
    var vis = list.filter(function (r) { return fp(r) && !S.hidden[r.slug]; });
    var minx = Infinity, maxx = -Infinity, miny = Infinity, maxy = -Infinity;
    var ext = function (x0, x1, y0, y1) { minx = Math.min(minx, x0); maxx = Math.max(maxx, x1); miny = Math.min(miny, y0); maxy = Math.max(maxy, y1); };
    vis.forEach(function (r) {
      var b = fp(r).geom.bbox, d = overlayOffsets(r);
      ext(b.minx + d[0], b.maxx + d[0], b.miny + d[1], b.maxy + d[1]);
    });
    var pitchY = S.align === 'centroid' ? 0 : PITCH.W / 2 + 6;
    if (S.pitch) ext(-PITCH.L / 2, PITCH.L / 2, pitchY - PITCH.W / 2, pitchY + PITCH.W / 2);
    if (!isFinite(minx)) ext(-60, 60, 0, 100);
    if (S.align === 'shore') ext(minx, maxx, 0, maxy);
    var w0 = maxx - minx, h0 = maxy - miny;
    var half = Math.max(w0, h0 * 1.25, 120) / 2 * 1.12;
    var cx = (minx + maxx) / 2;
    var fw = 2 * half, fh = Math.max(h0 * 1.14, fw * 0.62);
    var fy1 = maxy + (fh - h0) * 0.6, fy0 = fy1 - fh;           // frame in metres (y up)
    var beach = S.align === 'shore' ? Math.max(fh * 0.07, 6) : 0;
    if (S.align === 'shore') fy0 = Math.min(fy0, -beach);
    fh = fy1 - fy0;
    var X = function (x) { return (x - (cx - half)).toFixed(2); };
    var Y = function (y) { return (fy1 - y).toFixed(2); };
    var fs = fw / 55, sw = 'vector-effect="non-scaling-stroke"';
    var o = ['<svg class="sc-ov-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ' + fw.toFixed(2) + ' ' + fh.toFixed(2) + '" role="img" aria-label="' +
      esc('Overlay of ' + vis.length + ' reef footprints at one common scale, ' + (S.align === 'shore' ? 'at their true distance offshore' : 'centred on their centroids')) + '" style="font-size:' + fs.toFixed(2) + 'px">'];
    if (S.align === 'shore') {
      o.push('<rect class="sc-sea" x="0" y="0" width="' + fw.toFixed(2) + '" height="' + Y(0) + '"/>');
      o.push('<rect class="sc-sand" x="0" y="' + Y(0) + '" width="' + fw.toFixed(2) + '" height="' + (fh - Number(Y(0))).toFixed(2) + '"/>');
      o.push('<line class="sc-shore" ' + sw + ' x1="0" x2="' + fw.toFixed(2) + '" y1="' + Y(0) + '" y2="' + Y(0) + '"/>');
      o.push('<text class="sc-t sc-tm" x="' + fs.toFixed(2) + '" y="' + (Number(Y(0)) + fs * 1.3).toFixed(2) + '">shared shoreline (y = 0) · beach</text>');
      o.push('<text class="sc-t sc-tm" x="' + fs.toFixed(2) + '" y="' + (fs * 1.4).toFixed(2) + '">↑ offshore · each reef at its drawn distance from the shore, centred alongshore</text>');
    } else {
      o.push('<rect class="sc-sea" x="0" y="0" width="' + fw.toFixed(2) + '" height="' + fh.toFixed(2) + '"/>');
      o.push('<line class="sc-cross" ' + sw + ' x1="' + X(0) + '" x2="' + X(0) + '" y1="0" y2="' + fh.toFixed(2) + '"/><line class="sc-cross" ' + sw + ' x1="0" x2="' + fw.toFixed(2) + '" y1="' + Y(0) + '" y2="' + Y(0) + '"/>');
      o.push('<text class="sc-t sc-tm" x="' + fs.toFixed(2) + '" y="' + (fs * 1.4).toFixed(2) + '">↑ offshore · all centroids on one point (shoreline not shown)</text>');
    }
    if (S.pitch) {
      o.push('<g class="sc-pitch"><rect ' + sw + ' x="' + X(-PITCH.L / 2) + '" y="' + Y(pitchY + PITCH.W / 2) + '" width="' + PITCH.L + '" height="' + PITCH.W + '"/>' +
        '<line ' + sw + ' x1="' + X(0) + '" x2="' + X(0) + '" y1="' + Y(pitchY + PITCH.W / 2) + '" y2="' + Y(pitchY - PITCH.W / 2) + '"/>' +
        '<text class="sc-t" x="' + X(-PITCH.L / 2 + 2) + '" y="' + (Number(Y(pitchY + PITCH.W / 2)) - fs * 0.4).toFixed(2) + '">football pitch 105 × 68 m</text></g>');
    }
    // biggest first so small reefs stay on top
    vis.slice().sort(function (a, b) { return area(b) - area(a); }).forEach(function (r) {
      var d = overlayOffsets(r), col = colorOf(r);
      o.push('<g class="sc-ov-reef" data-open="' + esc(r.slug) + '" data-ov="' + esc(r.slug) + '" style="--c:' + col + '"><title>' + esc(r.name + ' — ' + fmt(area(r)) + ' m²') + '</title>' +
        fp(r).polygons.map(function (ring) {
          return '<path ' + sw + ' d="' + ring.map(function (p, i) { return (i ? 'L' : 'M') + X(p[0] + d[0]) + ' ' + Y(p[1] + d[1]); }).join('') + 'Z"/>';
        }).join('') + '</g>');
    });
    var bar = niceBar(fw), bx1 = fw - fs, bx0 = bx1 - bar, by = fh - fs * 0.8;
    o.push('<g class="sc-bar"><rect x="' + bx0.toFixed(2) + '" y="' + (by - fs * 0.45).toFixed(2) + '" width="' + (bar / 2).toFixed(2) + '" height="' + (fs * 0.45).toFixed(2) + '"/>' +
      '<rect class="sc-bar2" x="' + (bx0 + bar / 2).toFixed(2) + '" y="' + (by - fs * 0.45).toFixed(2) + '" width="' + (bar / 2).toFixed(2) + '" height="' + (fs * 0.45).toFixed(2) + '"/>' +
      '<text class="sc-t" x="' + bx0.toFixed(2) + '" y="' + (by - fs * 0.7).toFixed(2) + '">0</text>' +
      '<text class="sc-t" x="' + bx1.toFixed(2) + '" y="' + (by - fs * 0.7).toFixed(2) + '" text-anchor="end">' + bar + ' m</text></g>');
    o.push('</svg>');
    return o.join('');
  }
  var COLOR = {};
  function assignColors() {
    A().REEFS.filter(fp).slice().sort(function (a, b) { return area(b) - area(a); })
      .forEach(function (r, i) { COLOR[r.slug] = PALETTE[i % PALETTE.length]; });
  }
  function colorOf(r) { if (!COLOR[r.slug]) assignColors(); return COLOR[r.slug] || '#888'; }

  function overlayHTML(list) {
    var withFp = list.filter(fp).slice().sort(function (a, b) { return area(b) - area(a); });
    var legend = withFp.map(function (r) {
      var on = !S.hidden[r.slug];
      return '<button type="button" class="sc-leg" data-sc-toggle="' + esc(r.slug) + '" aria-pressed="' + on + '" style="--c:' + colorOf(r) + '">' +
        '<span class="sw" aria-hidden="true"></span><span class="nm">' + esc(r.name) + '</span><span class="ar">' + fmt(area(r)) + ' m²</span></button>';
    }).join('');
    return '<div class="sc-ov-ctrl" role="group" aria-label="Overlay options">' +
        '<span class="sc-seg" role="group" aria-label="Align">' +
          '<button type="button" data-sc-align="shore" aria-pressed="' + (S.align === 'shore') + '">By shoreline (true distance offshore)</button>' +
          '<button type="button" data-sc-align="centroid" aria-pressed="' + (S.align === 'centroid') + '">By centroid</button></span>' +
        '<button type="button" class="sc-btn" data-sc-pitch aria-pressed="' + S.pitch + '">Football pitch silhouette</button>' +
        '<button type="button" class="sc-btn" data-sc-all="1">Show all</button><button type="button" class="sc-btn" data-sc-all="0">Hide all</button>' +
      '</div>' +
      '<div class="sc-ov-wrap"><div class="sc-ov-fig" id="sc-ov-fig">' + overlaySVG(withFp) + '</div>' +
      '<div class="sc-legend" role="group" aria-label="Show or hide reefs in the overlay">' + legend + '</div></div>' +
      '<p class="sc-note">The frame fits the reefs that are switched on, so hiding the big ones zooms in on the small ones; the scale bar always gives the scale. Click a shape to open that reef.</p>';
  }

  // ------------------------------------------------------------ table
  // Sortable comparison table: same pattern as app.js's gallery table (COLS/SORTERS/current()) —
  // <th aria-sort><button data-*-sort></button></th>, numeric columns sort numerically, text
  // columns alphabetically, confidence by rank. Uses its own data-sc-sort attribute (not app.js's
  // data-sort) so the two tables' click handlers, bound on the same document, don't collide.
  var CONF_ORDER = { high: 3, medium: 2, low: 1 };
  var TCOLS = [
    { k: 'name', t: 'Name', dir0: 1, val: function (r) { return r.name.toLowerCase(); } },
    { k: 'shape', t: 'Shape', dir0: 1, val: function (r) { return (fp(r).shape_short || '').toLowerCase(); } },
    { k: 'length', t: 'L (m)', dir0: -1, val: function (r) { var b = fp(r).bbox_m || {}; return b.length_alongshore == null ? null : Number(b.length_alongshore); } },
    { k: 'width', t: 'W (m)', dir0: -1, val: function (r) { var b = fp(r).bbox_m || {}; return b.width_crossshore == null ? null : Number(b.width_crossshore); } },
    { k: 'area', t: 'Area (m²)', dir0: -1, val: function (r) { var v = fp(r).area_m2; return v == null ? null : Number(v); } },
    { k: 'crest', t: 'Crest depth', dir0: -1, val: function (r) { var c = fp(r).crest_depth_m; return c && c.value != null ? Number(c.value) : null; } },
    { k: 'distance', t: 'Distance offshore', dir0: -1, val: function (r) { var d = fp(r).distance_offshore_m; return d && d.value != null ? Number(d.value) : null; } },
    { k: 'confidence', t: 'Confidence', dir0: -1, val: function (r) { var lvl = fp(r).confidence_level || 'unknown'; return CONF_ORDER[lvl] != null ? CONF_ORDER[lvl] : -1; } },
    { k: 'gemini', t: 'vs Gemini', dir0: -1, val: function (r) { return fp(r).gemini_n_disagree || 0; } },
    { k: 'provenance', t: 'Provenance', dir0: 1, val: function (r) { return fp(r).provenance_md ? r.slug.toLowerCase() : null; } }
  ];
  var TCOL_BY_KEY = {};
  TCOLS.forEach(function (c) { TCOL_BY_KEY[c.k] = c; });
  function sortRows(list, col, dir) {
    var key = col.val;
    return list.slice().sort(function (a, b) {
      var x = key(a), y = key(b);
      if (x == null && y == null) return 0;
      if (x == null) return 1;             // missing values always last
      if (y == null) return -1;
      if (x < y) return -dir;
      if (x > y) return dir;
      return 0;
    });
  }
  function tableHTML(list) {
    var col = TCOL_BY_KEY[S.tsort] || TCOL_BY_KEY.area;
    var rows = sortRows(list.filter(fp), col, S.tdir);
    var head = '<tr>' + TCOLS.map(function (c) {
      var s = S.tsort === c.k ? (S.tdir > 0 ? 'ascending' : 'descending') : 'none';
      return '<th scope="col" aria-sort="' + s + '"><button type="button" data-sc-sort="' + c.k + '">' + esc(c.t) + '</button></th>';
    }).join('') + '</tr>';
    return '<div class="table-wrap" id="sc-table"><table class="data sc-cmp"><caption class="sr">Footprint comparison</caption><thead>' + head +
      '</thead><tbody>' + rows.map(function (r) {
        var f = fp(r), b = f.bbox_m || {};
        var g = f.gemini_n_disagree ? f.gemini_n_disagree + ' disagreement' + (f.gemini_n_disagree === 1 ? '' : 's') : 'agree';
        return '<tr data-open="' + esc(r.slug) + '"><td class="nm"><button type="button" class="rowbtn" data-open="' + esc(r.slug) + '">' + esc(r.name) + '</button></td>' +
          '<td title="' + esc(f.shape_type || '') + '">' + esc(f.shape_short) + '</td>' +
          '<td class="num">' + fmt(b.length_alongshore) + '</td><td class="num">' + fmt(b.width_crossshore) + '</td>' +
          '<td class="num">' + fmt(f.area_m2) + '<br><small class="muted">≈ ' + pitches(f.area_m2) + ' pitches</small></td>' +
          '<td>' + esc(f.crest_label) + '</td><td>' + esc(f.distance_label) + '</td>' +
          '<td>' + confBadge(f) + '</td><td>' + esc(g) + '</td>' +
          '<td>' + (f.provenance_md ? '<a href="' + esc(f.provenance_md) + '" target="_blank" rel="noopener">' + esc(r.slug + '.md') + '</a>' : '—') + '</td></tr>';
      }).join('') + '</tbody></table></div>';
  }

  // ------------------------------------------------------------ render
  function panelsHTML(list) {
    var rows = list.filter(fp).slice().sort(function (a, b) { return S.sort === 'desc' ? area(b) - area(a) : area(a) - area(b); });
    return rows.map(function (r) { return panelHTML(r, S.scale); }).join('');
  }
  function openHows() {
    var o = {};
    document.querySelectorAll('#scale-root details[data-how][open]').forEach(function (d) { o[d.getAttribute('data-how')] = true; });
    return o;
  }
  function render(list) {
    S.list = list;
    var root = document.getElementById('scale-root');
    if (!root) return;
    var keep = openHows();
    var noFp = list.filter(function (r) { return !fp(r); });
    root.innerHTML =
      '<div class="sc-intro">' +
        '<p>Each reef is drawn in plan view — sea at the top, beach at the bottom — at <b>one common scale</b>, so the drawings can be compared directly. ' +
        'The outlines are <b>documented schematics</b> built from published dimensions, design drawings and photos, not surveys: every number below carries its source, ' +
        'or says that it is derived from our own drawing. Open <b>How we drew this</b> under any drawing for the full derivation, the images relied on, the comparison with Gemini\'s earlier attempt, and open issues. ' +
        'A football pitch is taken as ' + A().extLink(PITCH.url, '105 × 68 m (FIFA recommendation)') + ' = 7,140 m².</p>' +
        '<p class="muted">Lior\'s reference graphic traces outlines over real aerial photos. We did not have geo-referenced aerial imagery for all 13 reefs (and this pass added no new images), so we draw the outlines on a plain sea/beach background instead.</p>' +
      '</div>' +
      '<div class="sc-ctrl" role="group" aria-label="Drawing scale">' +
        '<span class="sc-seg"><button type="button" data-sc-zoom="0.5" aria-label="Zoom out (half the scale)">− ×0.5</button>' +
        '<span class="sc-zl" aria-live="polite">1 px = ' + fmt(1 / S.scale, 3) + ' m (' + fmt(S.scale * 100, 1) + ' %)</span>' +
        '<button type="button" data-sc-zoom="2" aria-label="Zoom in (double the scale)">+ ×2</button></span>' +
        '<button type="button" class="sc-btn" data-sc-zoom="reset">Reset to 1 px = 1 m</button>' +
        '<label class="sort"><span>Order</span><select id="sc-sort"><option value="desc"' + (S.sort === 'desc' ? ' selected' : '') + '>Largest area first</option>' +
          '<option value="asc"' + (S.sort === 'asc' ? ' selected' : '') + '>Smallest area first</option></select></label>' +
      '</div>' +
      '<h2 class="sc-h">Each reef on its own, same scale</h2>' +
      '<div class="sc-grid">' + panelsHTML(list) + '</div>' +
      (noFp.length ? '<p class="muted">No footprint yet for: ' + noFp.map(function (r) { return esc(r.name); }).join(', ') + '.</p>' : '') +
      '<h2 class="sc-h">All reefs on one frame</h2>' +
      '<div class="sc-ov" id="sc-ov">' + overlayHTML(list) + '</div>' +
      '<h2 class="sc-h">Comparison table</h2>' +
      tableHTML(list);
    Object.keys(keep).forEach(function (slug) {
      var d = root.querySelector('details[data-how="' + slug + '"]');
      if (d) d.open = true;
    });
  }
  function rerenderOverlay() {
    var box = document.getElementById('sc-ov');
    if (box) box.innerHTML = overlayHTML(S.list);
  }
  function rerenderTable() {
    var box = document.getElementById('sc-table');
    if (box) box.outerHTML = tableHTML(S.list);
  }

  /* Detail-dialog section: the same drawing and facts, plus the How-we-drew-this content. */
  function detailSection(r, forPrint) {
    if (!fp(r)) return '';
    return '<div class="sc-detail" data-slug="' + esc(r.slug) + '">' +
      '<div class="sc-badges">' + confBadge(fp(r)) + '</div>' +
      '<div class="sc-drawwrap">' + panelSVG(r, S.scale) + '</div>' +
      factsHTML(r) +
      (forPrint ? '' : '<p><button type="button" class="linkish" data-goto-scale="' + esc(r.slug) + '">Compare with the other reefs in the Scale view</button></p>') +
      '<div class="sc-how-b">' + howHTML(r) + '</div></div>';
  }

  // ------------------------------------------------------------ events
  document.addEventListener('click', function (e) {
    var t = e.target;
    if (!t.closest) return;
    var so = t.closest('[data-sc-sort]');
    if (so) {
      var k = so.getAttribute('data-sc-sort'), col = TCOL_BY_KEY[k];
      if (S.tsort === k) S.tdir = -S.tdir; else { S.tsort = k; S.tdir = col ? col.dir0 : 1; }
      rerenderTable();
      var again = document.querySelector('[data-sc-sort="' + k + '"]');
      if (again) again.focus();
      return;
    }
    var z = t.closest('[data-sc-zoom]');
    if (z) {
      var v = z.getAttribute('data-sc-zoom'), i = ZOOMS.indexOf(S.scale);
      if (v === 'reset') S.scale = 1;
      else if (v === '2' && i < ZOOMS.length - 1) S.scale = ZOOMS[i + 1];
      else if (v === '0.5' && i > 0) S.scale = ZOOMS[i - 1];
      A().rerender();
      return;
    }
    var tg = t.closest('[data-sc-toggle]');
    if (tg) { var s = tg.getAttribute('data-sc-toggle'); if (S.hidden[s]) delete S.hidden[s]; else S.hidden[s] = true; rerenderOverlay(); return; }
    var al = t.closest('[data-sc-align]');
    if (al) { S.align = al.getAttribute('data-sc-align'); rerenderOverlay(); return; }
    if (t.closest('[data-sc-pitch]')) { S.pitch = !S.pitch; rerenderOverlay(); return; }
    var all = t.closest('[data-sc-all]');
    if (all) {
      S.hidden = {};
      if (all.getAttribute('data-sc-all') === '0') S.list.forEach(function (r) { S.hidden[r.slug] = true; });
      rerenderOverlay();
      return;
    }
    var go = t.closest('[data-goto-scale]');
    if (go) {
      var slug = go.getAttribute('data-goto-scale');
      A().closeReef();
      A().setView('scale');
      setTimeout(function () { var p = document.getElementById('sc-' + slug); if (p) p.scrollIntoView({ block: 'start' }); }, 60);
    }
  });
  document.addEventListener('change', function (e) {
    if (e.target && e.target.id === 'sc-sort') { S.sort = e.target.value; A().rerender(); }
  });
  // legend hover highlights that reef in the overlay
  document.addEventListener('mouseover', function (e) {
    var lg = e.target.closest && e.target.closest('[data-sc-toggle]');
    var fig = document.getElementById('sc-ov-fig');
    if (!fig) return;
    fig.querySelectorAll('.sc-ov-reef.hl').forEach(function (g) { g.classList.remove('hl'); });
    if (lg) { var g = fig.querySelector('[data-ov="' + lg.getAttribute('data-sc-toggle') + '"]'); if (g) g.classList.add('hl'); }
  });

  window.ReefScale = { render: render, detailSection: detailSection, panelSVG: panelSVG, panelFrame: panelFrame, state: S, PITCH: PITCH };
})();

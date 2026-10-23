/* Footprint detail section (slim successor of scale.js, 2026-10-10). The Map and Scale TABS were removed on Lior's decision; this keeps ONLY what the reef
   dialog's "Scale & footprint" section needs: the plan drawing of the traced footprint at one px/m scale, the fact table and the full derivation
   (every quantity, method, source, images relied on, verification) = rule 1 traceability for reefs without a 3D model. The full old Scale view is in
   archive/04_build_removed_2026-10-10/src/scale.js (restore steps: 04_build/HANDOFF.md section 0).
   Inlined by build.py before app.js; talks to app.js through window.ReefApp. Geometry source: reef.footprint (compiled from 07_scale/reefs/<slug>.footprint.json).
   Coordinates are metres: x = alongshore, y = offshore (positive seaward), shoreline = the line y = 0. */
(function () {
  'use strict';

  // ------------------------------------------------------------ constants
  // FIFA-recommended pitch, 105 x 68 m (Wikipedia "Football pitch", checked 2026-09-25)
  var PITCH = { L: 105, W: 68, area: 105 * 68, url: 'https://en.wikipedia.org/wiki/Football_pitch' };
  // panel drawing margins, in screen px (independent of the scale)
  var G = { ML: 16, MR: 16, MT: 30, BEACH: 24, MB: 34, PAD_M: 15, MIN_HALF_M: 75, BAR_M: 100 };
  var VCSS = { 'worked': '--v-worked', 'partly worked': '--v-partly', 'mixed': '--v-mixed', 'failed': '--v-failed', 'n-a': '--v-na' };

  var S = { scale: (window.innerWidth || 1200) < 700 ? 0.5 : 1 };   // px per metre of the drawing in the dialog

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
    var traced = !!f.outline_source;
    var tr = '<span class="sc-est sc-tr" title="Measured on the traced outline (shape.json); see Outline source below">traced</span>';
    var dimIds = traced ? [] : derivIds(r, /length|width|diameter|dimension|footprint|size|span|extent|arm|chord|topolog|shape|plan/i, /depth|offshore|distance|crest|volume|area|height/i);
    var areaIds = traced ? [] : derivIds(r, /area/i);
    var crestIds = idsIn(cr.ref, r), distIds = idsIn(di.ref, r);
    var est = '<span class="sc-est" title="Not a published figure: derived from our own drawing or an estimate; see How we drew this">derived</span>';
    return '<dl class="sc-facts">' +
      '<div><dt>Plan box, L × W</dt><dd>' + fmt(b.length_alongshore) + ' × ' + fmt(b.width_crossshore) + ' m' + (traced ? ' ' + tr : marks(dimIds, r)) +
        '<small>alongshore × cross-shore' + (b.note ? '; see note' : '') + '</small></dd></div>' +
      '<div><dt>Footprint area</dt><dd>' + fmt(f.area_m2) + ' m²' + (traced ? ' ' + tr : areaIds.length ? marks(areaIds, r) : ' ' + est) +
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
    var os = f.outline_source;
    if (os) {
      var dl = f.docs || {}, lk = [];
      if (A().safeUrl(os.url) && !/[{}]/.test(os.url)) lk.push(A().extLink(os.url, 'image / figure ↗'));
      if (A().safeUrl(os.source_page)) lk.push(A().extLink(os.source_page, 'source page ↗'));
      [['method', 'method'], ['verify', 'verification'], ['sources', 'sources']].forEach(function (k) {
        if (dl[k[0]]) lk.push('<a href="' + esc(dl[k[0]]) + '" target="_blank" rel="noopener">' + k[1] + ' (md) ↗</a>');
      });
      o.push('<h4>0 · Outline source: where the drawn shape comes from</h4><dl class="sc-notes">' +
        '<dt>Drawn from</dt><dd>' + esc(os.title || os.derived_from) + (os.image_date ? ' (' + esc(os.image_date) + ')' : '') + (os.kind ? ' <span class="muted">· ' + esc(String(os.kind).replace(/_/g, ' ')) + '</span>' : '') +
          (os.page_or_figure ? '<br><span class="muted">' + esc(os.page_or_figure) + '</span>' : '') + (os.credit ? '<br><span class="muted">Credit: ' + esc(os.credit) + '</span>' : '') + '</dd>' +
        '<dt>Status</dt><dd>' + esc(f.status || '—') + ' · confidence ' + esc(f.confidence_level || '—') + ' · checked ' + esc(f.verified_on || '—') + '</dd>' +
        '<dt>Why this confidence</dt><dd>' + linkRefs(f.confidence, r) + '</dd>' +
        (os.frame ? '<dt>Drawing frame</dt><dd>' + esc(os.frame) + (f.plan_x_flipped ? ' <span class="muted">(drawn with the sea at the top, so x runs right to left)</span>' : '') + '</dd>' : '') +
        (lk.length ? '<dt>Files</dt><dd>' + lk.join(' · ') + '</dd>' : '') + '</dl>');
      if ((f.shape_conf_factors || []).length) {
        o.push('<details class="sc-ver"><summary>Show the ' + f.shape_conf_factors.length + ' confidence factors</summary><ul class="sc-ul">' +
          f.shape_conf_factors.map(function (x) { return '<li>' + linkRefs(x, r) + '</li>'; }).join('') + '</ul></details>');
      }
    }
    o.push('<h4>1 · ' + (os ? 'Earlier text-based estimate (not the drawing): every quantity, how we got it, and from where' : 'Derivation: every quantity, how we got it, and from where') + '</h4>');
    if (os && f.text_estimate_area_m2) o.push('<p class="muted">This table comes from the earlier text-derived footprint note (area ' + fmt(f.text_estimate_area_m2) + ' m²). The drawing above is the traced outline and its numbers are in section 0; crest depth and distance offshore still come from the sources listed here.</p>');
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


  /* Reefs whose shape we do not know (Lior 2026-10-10): NO drawing, only a plain-text reason, the text-only size facts and the feasibility note. */
  function hiddenSection(r) {
    var f = fp(r), d = f.docs || {};
    return '<div class="sc-detail sc-hidden" data-slug="' + esc(r.slug) + '">' +
      '<p class="sc-nodraw"><b>Shape not drawn:</b> no plan, survey or clear image of the reef found (see FEASIBILITY).</p>' +
      '<p><span class="sc-lab">Why</span> ' + linkRefs(f.hidden_reason, r) + '</p>' +
      (r.size ? '<p><span class="sc-lab">Size facts from text only (no drawing)</span> ' + A().refify(r.size, r, 'link') + '</p>' : '') +
      (d.feasibility ? '<p class="sc-prov">Details: <a href="' + esc(d.feasibility) + '" target="_blank" rel="noopener">FEASIBILITY.md</a> <span class="muted">(copy of ' + esc(d.feasibility_src) + ')</span></p>' : '') +
    '</div>';
  }

  /* Detail-dialog section: the same drawing and facts, plus the How-we-drew-this content. */
  function detailSection(r, forPrint) {
    if (!fp(r)) return '';
    if (fp(r).display === false) return hiddenSection(r);
    return '<div class="sc-detail" data-slug="' + esc(r.slug) + '">' +
      '<div class="sc-badges">' + confBadge(fp(r)) + '</div>' +
      '<div class="sc-drawwrap">' + panelSVG(r, S.scale) + '</div>' +
      factsHTML(r) +
      '<div class="sc-how-b">' + howHTML(r) + '</div></div>';
  }

  window.ReefScale = { detailSection: detailSection, hiddenSection: hiddenSection, panelSVG: panelSVG, panelFrame: panelFrame, PITCH: PITCH };
})();

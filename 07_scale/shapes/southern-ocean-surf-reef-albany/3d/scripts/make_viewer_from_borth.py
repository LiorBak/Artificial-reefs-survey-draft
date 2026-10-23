"""make_viewer_from_borth.py - derive 3d/index.html from the Borth viewer (07_scale/shapes/borth-coastal-defence-reef/3d/index.html, 2026-10-10).
Only text, datum labels, grid/camera presets and the single-reef label changes; the three.js scene code is the same."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, '..', '..', '..', 'borth-coastal-defence-reef', '3d', 'index.html'), encoding='utf-8').read().split('\n')
out = []
def line_has(l, s): return l.lstrip().startswith(s)
for l in src:
    if '<title>' in l: l = '<title>Southern Ocean Surf Reef (Albany) - 3D model</title>'
    elif line_has(l, '<h1>Borth'): l = '  <h1>Southern Ocean Surf Reef, Albany WA</h1>'
    elif line_has(l, 'const ZODN'): l = 'const ZODN = 0;                                       // model z is metres AHD (taken as MSL)\nconst LATZ = M.datum.lat_AHD;                          // z of LAT (m AHD), derived'
    elif "$('wlo')) $('wlo').innerHTML" in l: l = "  if ($('wlo')) $('wlo').innerHTML = `<b>${fmt(z)} m AHD</b> (model zero, taken as MSL) = ${(z - LATZ).toFixed(2)} m above LAT (chart datum, derived)`;"
    elif line_has(l, 'const lv = M.levels.map'): l = "  const lv = M.levels.map(l => `<button data-id=\"${l.id}\" title=\"${l.name} - ${l.source}\">${l.id}</button>`).join('');"
    elif line_has(l, '<div class="row small" style="justify-content:space-between'): l = '  <div class="row small" style="justify-content:space-between;margin:0"><span>LAT &minus;0.74 m AHD</span><span>highest predicted 2024 +0.66 m AHD</span></div>'
    elif line_has(l, '<div class="small"><b>Why the slider stops'): l = '  <div class="small"><b>Tide:</b> local tides only (Albany, micro-tidal: spring range about 0.9 m, EIA 2018). The slider runs from LAT to the highest <i>predicted</i> tide of 2024; the true HAT was not found. Storm surge adds 0.4-1.0 m (EIA 2018 s.5). Orange chips are derived or assumed levels (see Sources tab).</div>'
    elif line_has(l, '<div class="small">Rock: <span'): l = '  <div class="small">Rock surface (one colour; the three rock grades are not modelled separately). Yellow line = toe outline of the selected version. Seabed colour = depth. <b>The seabed under and around the reef is read from a 2015 design contour plot (LOW confidence): the heights of the rock pile above the bed are therefore uncertain by about &plusmn;1 m. The fullness of the pile (broad plateau, steep toe) is FITTED to the stated 34,000 m3 (assumption A9), it is not design information.</b></div>'
    elif line_has(l, '<div class="small">Beach and foreshore: Welsh'): l = '  <div class="small">Seabed = one cross-shore profile (alongshore uniform): contour crossings -1 to -7 m read from the Royal HaskoningDHV 2015 Option B plan (depth datum not stated, assumed AHD), landward of -0.5 m and seaward of -7 m assumed. Details: Methods and Sources tabs.</div>`;'
    elif line_has(l, 'const SRCN = '): l = "const SRCN = { sat2026: 'Esri World Imagery 2026-01-20', design_plan: 'Bluecoast design plan (via Raised Water Research)', design_table: 'City of Albany design table / project page', rhdhv2015: 'RHDHV 2015 Option B depth-contour plot (via Raised Water Research)', eia2018: 'BMT 2018 Environmental Impact Assessment (Fig 6.9, soundings m CD)' };"
    elif line_has(l, '<p class="small">Volumes are the model rock volume'): l = '  <p class="small">Volumes are the model rock volume above the modelled seabed. The design-outline volume is FITTED to the stated 34,000 m3 (assumption A9, shape exponent N); the satellite-outline volume is a result. Tonnes at ${M.density_t_m3} t/m³ (62,800 t / 34,000 m³, City of Albany). Version ids for the URL hash: ${M.versions.map(v => v.id).join(\', \')}.</p>`;'
    elif "$('cap').innerHTML" in l: l = "$('cap').innerHTML = `<b>${M.name}</b><br>z = 0 at AHD (taken as MSL). Seabed LOW confidence. Not for navigation.`;"
    elif line_has(l, '<h3>Datum levels (mODN'): l = "  <h3>Water levels (m AHD)</h3><table><tr><th>Level</th><th>z (m AHD)</th><th>above LAT</th><th>Source</th></tr>${allLevels.map(l => `<tr><td>${l.name}</td><td>${fmt(l.z)}</td><td>${(l.z - LATZ).toFixed(2)}</td><td class=\"${l.estimated ? 'est' : ''}\">${l.source}</td></tr>`).join('')}</table>`;"
    elif line_has(l, '<p class="small">Source register'): l = '  <p class="small">Source register (what was read off each source and how), methods, assumptions A1-A12, decisions D1-D10 and confidence per element: <b>Methods tab, button &ldquo;Sources, assumptions, decisions&rdquo;</b>.</p><h3>Provenance (every model value)</h3><table><tr><th>Parameter</th><th>Value</th><th>Source</th><th>Method</th><th>Uncertainty</th></tr>${rows}</table>'
    elif "model: 'borth-coastal-defence-reef'" in l: l = l.replace("borth-coastal-defence-reef", "southern-ocean-surf-reef-albany").replace("canonical x south, y offshore (west), metres", "canonical x alongshore (NNE), y offshore (ESE), metres").replace("z_mODN: +(c.z + ZODN).toFixed(2)", "z_AHD: +(c.z).toFixed(2)")
    elif line_has(l, "curTxt = h ?"): l = "  curTxt = h ? `cursor x ${h.point.x.toFixed(1)}  y ${h.point.z.toFixed(1)}  z ${fmt(h.point.y / state.ve)} m AHD = ${(h.point.y / state.ve - LATZ).toFixed(2)} m above LAT  (${(state.wl - h.point.y / state.ve).toFixed(2)} m below water)` : '';"
    elif line_has(l, "$('hud').textContent"): l = "  $('hud').textContent = `camera x ${c.x.toFixed(1)}  y ${c.y.toFixed(1)}  z ${fmt(c.z, 1)} m AHD\\nheading ${c.hdg.toFixed(0)}° (true)  pitch ${c.pitch.toFixed(0)}°  FOV ${c.vfov.toFixed(0)}° v / ${c.hfov.toFixed(0)}° h\\n` + curTxt;"
    out.append(l)
t = '\n'.join(out)
# seabed colour ramp (m AHD)
t = re.sub(r"const ramp = \[.*?\];", "const ramp = [[-9, [24, 46, 64]], [-6, [40, 76, 96]], [-3.5, [70, 112, 122]], [-1.5, [128, 140, 120]], [0, [196, 180, 134]], [1.5, [214, 198, 150]], [3, [190, 184, 146]]];", t, flags=re.S)
# reef zone colour, outline at seabed + 0.15
t = t.replace("const zoneCol = { 1: [0.60, 0.61, 0.62], 2: [0.40, 0.42, 0.44], 3: [0.42, 0.47, 0.34] };", "const zoneCol = { 1: [0.62, 0.60, 0.56], 2: [0.62, 0.60, 0.56], 3: [0.62, 0.60, 0.56] };")
t = t.replace("pts.push(a[0], v.edge_level_MSL + 0.08, a[1], b[0], v.edge_level_MSL + 0.08, b[1]);", "pts.push(a[0], seaAt(a[0], a[1]) + 0.12, a[1], b[0], seaAt(b[0], b[1]) + 0.12, b[1]);")
# grid extents, bars, north, labels
t = t.replace("x0 = -110, x1 = 150, y0 = 230, y1 = 430", "x0 = -150, x1 = 150, y0 = 0, y1 = 300")
t = t.replace("const nx_ = FR.north_xy[0], ny_ = FR.north_xy[1], o = [-150, 60];", "const nx_ = FR.north_xy[0], ny_ = FR.north_xy[1], o = [-120, 20];")
t = re.sub(r"addLabel\('Defence line.*?\n", "addLabel('Beach-face line (y = 0, edge of dry sand)', () => m2s(-60, 0, seaAt(-60, 0) + 1.0), 'dim', 'misc');\n", t)
t = re.sub(r"addLabel\('Sea / offshore'.*?\n", "addLabel('Sea / offshore (ESE)', () => m2s(0, 300, wlz() + 1), 'water', 'misc');\n", t)
t = re.sub(r"addLabel\('Beach',.*?\n", "addLabel('Beach', () => m2s(-20, -40, seaAt(-20, -40) + 1), 'dim', 'misc');\n", t)
t = re.sub(r"M\.roles\.north && addLabel.*?\n", "M.roles.main && addLabel(M.roles.main.label, () => m2s(M.roles.main.centroid[0], M.roles.main.centroid[1], 7), 'reef', 'reef');\n", t)
t = re.sub(r"M\.roles\.south && addLabel.*?\n", "", t)
t = t.replace("for (let v = -100; v <= 150; v += 50) addLabel('x ' + v, () => m2s(v, 230, wlz()), 'dim', 'axis');", "for (let v = -150; v <= 150; v += 50) addLabel('x ' + v, () => m2s(v, 0, wlz()), 'dim', 'axis');")
t = t.replace("for (let v = 250; v <= 400; v += 50) addLabel('y ' + v, () => m2s(-110, v, wlz()), 'dim', 'axis');", "for (let v = 50; v <= 300; v += 50) addLabel('y ' + v, () => m2s(-150, v, wlz()), 'dim', 'axis');")
t = t.replace("bar(100, 418, 50, '50 m'); bar(100, 408, 10, '10 m');", "bar(90, 290, 50, '50 m'); bar(90, 280, 10, '10 m');")
# views
t = re.sub(r"const T = m2s\(-10, 330, -2\);\n", "", t)
t = re.sub(r"const VIEWS = \{.*?\n\};", """const VIEWS = {
  oblique: { label: 'Oblique from sea', pos: () => m2s(170, 340, 55), tgt: () => m2s(0, 150, -3 * state.ve) },
  plan: { label: 'Plan (north = up-left)', pos: () => m2s(0, 150, 420), tgt: () => m2s(0, 150, 0) },
  crest: { label: 'Along the surf-reef crest', pos: () => { const d = [axisT[0] - axisH[0], axisT[1] - axisH[1]], L = Math.hypot(...d); return m2s(axisT[0] + d[0] / L * 25, axisT[1] + d[1] / L * 25, 2.5); }, tgt: () => m2s(axisH[0], axisH[1], 0) },
  beach: { label: 'From the beach (eye 1.7 m)', pos: () => m2s(0, -10, seaAt(0, -10) + 1.7), tgt: () => m2s(40, 160, 0) },
  side: { label: 'Side view along shore', pos: () => m2s(-330, 150, 8), tgt: () => m2s(0, 150, -3) },
};""", t, flags=re.S)
t = t.replace("const axisH = M.axis_xy ? M.axis_xy.head : [-10, 380], axisT = M.axis_xy ? M.axis_xy.tail : [-60, 268];", "const axisH = M.axis_xy.head, axisT = M.axis_xy.tail;")
t = t.replace("const T = m2s(-10, 330, -2);", "")
t = t.replace("const ph = { x: 0, y: 20, z: 1.7, h: 270, p: 0, fov: 60, op: 0.5, on: false };", "const ph = { x: 0, y: -10, z: 1.7, h: 120, p: 0, fov: 60, op: 0.5, on: false };")
t = t.replace("'x alongshore (+south) m'", "'x alongshore (+NNE) m'").replace("'y offshore (west) m'", "'y offshore (ESE) m'")
t = t.replace("camera.position.set(ph.x, ph.z, ph.y);", "camera.position.set(ph.x, ph.z, ph.y);")
t = t.replace("controls.maxDistance = 1400", "controls.maxDistance = 1200")
# photo text
t = re.sub(r"<div class=\"small\">Beach preset: the reef is about 300 m offshore.*?</div>`;", "<div class=\"small\">Beach preset: the reef starts about 67 m beyond the dry-sand edge and is 165 m long; a phone photo from the beach shows it small. Photo FOV is usually 60-75° horizontal for a phone main camera. The reef is submerged: at low tide you see breaking waves, not rock.</div>`;", t, flags=re.S)
t = t.replace('</head>', '<script>window.addEventListener("error",function(e){window.__err=(window.__err||"")+e.message+" @"+e.lineno+":"+e.colno+"\\n"});window.addEventListener("unhandledrejection",function(e){window.__err=(window.__err||"")+String(e.reason)+"\\n"});</script>\n</head>',1)
open(os.path.join(HERE, '..', 'index.html'), 'w', encoding='utf-8').write(t)
print('written', len(t))

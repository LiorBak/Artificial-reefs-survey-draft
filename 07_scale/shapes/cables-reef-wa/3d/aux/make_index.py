"""One-off: derive 3d/index.html for cables-reef-wa from the finished Borth viewer (07_scale/shapes/borth-coastal-defence-reef/3d/index.html).
Same controls and features (version selector + (i), water slider, vertical exaggeration, views, photo match, sources, methods tabs); Borth-specific
text, datum arithmetic and geometry bits are replaced; plan-only versions and RL contour lines are added; datum reading switch (A/B) added."""
import re, sys
SRC = '../../borth-coastal-defence-reef/3d/index.html'
L = open(SRC, encoding='utf-8').read().split('\n')
def line(n): return L[n - 1]
def setline(n, startswith, new):
    assert line(n).lstrip().startswith(startswith), (n, line(n)[:80])
    L[n - 1] = new
def sub_in(n, old, new, count=1):
    assert line(n).count(old) >= 1, (n, old, line(n)[:120]); L[n - 1] = line(n).replace(old, new)
setline(5, '<title>', '<title>Cables (Cable Station) surfing reef - 3D model</title>')
setline(63, '<h1>', '  <h1>Cables (Cable Station) surfing reef</h1>')
setline(90, 'const ZODN', """const OFFA = M.datum.rl_minus_msl_A;                 // scene Y = z_RL - 0.78 (datum reading A)
let READ = 'A';                                      // datum reading A (RL = chart datum, MSL = RL + 0.78) or B (RL = MSL)
const rlOff = () => (READ === 'A' ? OFFA : 0);       // z_RL - z_MSL
const wlY = () => state.wl - (OFFA - rlOff());       // scene Y of the water plane (state.wl is relative to MSL)
const ZODN = OFFA;                                   // RL = scene Y + OFFA""")
setline(185, 'const wlz', 'const wlz = () => wlY();')
# colour ramp (seabed), zone colours
for i, l in enumerate(L):
    if l.startswith('const ramp = [[-6.6'):
        L[i] = 'const ramp = [[-9.0, [24, 46, 64]], [-6.0, [38, 72, 92]], [-4.5, [60, 100, 112]], [-3.5, [86, 124, 126]], [-2.5, [130, 140, 120]], [-1.5, [170, 160, 120]], [0.5, [200, 180, 130]], [3, [190, 185, 150]], [7, [120, 140, 90]]];'
    if l.startswith('const zoneCol'):
        L[i] = 'const zoneCol = { 1: [0.86, 0.80, 0.66], 2: [0.60, 0.55, 0.47], 3: [0.92, 0.66, 0.30] };'
# buildReef: plan-only versions
txt = '\n'.join(L)
txt = txt.replace("function buildReef(v) {\n  const G = v.grid,", "function buildReefGrid(v) {\n  const G = v.grid,", 1)
assert 'function buildReefGrid' in txt
wrapper = """function mkOutlineLine(v) {
  const pts = []; v.outline_m.forEach(ring => { for (let q = 0; q < ring.length; q++) { const a = ring[q], b = ring[(q + 1) % ring.length]; pts.push(a[0], v.edge_level_MSL + 0.08, a[1], b[0], v.edge_level_MSL + 0.08, b[1]); } });
  const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
  return new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: v.grid ? 0xffd060 : 0x66ddff }));
}
function buildReef(v) { if (v.grid) return buildReefGrid(v); return { mesh: null, line: mkOutlineLine(v) }; }
// design contours (RL) drawn on the modelled surface
const contourG = new THREE.Group(); world.add(contourG);
(function mkContours() {
  (M.contours || []).forEach(c => { const pts = []; c.lines.forEach(ln => { for (let q = 0; q < ln.length - 1; q++) pts.push(ln[q][0], c.z_msl + 0.05, ln[q][1], ln[q + 1][0], c.z_msl + 0.05, ln[q + 1][1]); });
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3)); contourG.add(new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: 0xff9a3c }))); });
})();
"""
txt = txt.replace("function setVersion(id) {", wrapper + "function setVersion(id) {", 1)
txt = txt.replace("  if (reefMesh) { world.remove(reefMesh); world.remove(outlineLine); }", "  if (reefMesh) world.remove(reefMesh); if (outlineLine) world.remove(outlineLine);", 1)
txt = txt.replace("reefMesh = reefCache[id].mesh; outlineLine = reefCache[id].line; world.add(reefMesh); world.add(outlineLine);", "reefMesh = reefCache[id].mesh; outlineLine = reefCache[id].line; if (reefMesh) world.add(reefMesh); world.add(outlineLine); contourG.visible = !!v.grid && state.show.reef;", 1)
txt = txt.replace("water.visible = state.show.water; seabedMesh.visible = state.show.seabed; if (reefMesh) reefMesh.visible = state.show.reef;", "water.visible = state.show.water; seabedMesh.visible = state.show.seabed; if (reefMesh) reefMesh.visible = state.show.reef; contourG.visible = !!verObj().grid && state.show.reef;", 1)
L = txt.split('\n')
txt = '\n'.join(L)
# grid extents, north arrow, labels, bars
txt = txt.replace("x0 = -110, x1 = 150, y0 = 230, y1 = 430;", "x0 = -90, x1 = 90, y0 = 215, y1 = 345;", 1)
txt = txt.replace("o = [-150, 60];", "o = [-120, 225];", 1)
# shoreline block + labels
a = txt.index("// shoreline = defence line y = 0"); b = txt.index("addLabel('Defence line"); c = txt.index("M.roles.north &&")
txt = txt[:a] + "// (the shore line is 235-310 m east of the reef and outside the modelled window)\n" + "addLabel('Open sea (west)', () => m2s(0, 405, wlz() + 1), 'water', 'misc');\naddLabel('Shore: 235-310 m to the east (not modelled)', () => m2s(0, 195, wlz() + 1), 'dim', 'misc');\n" + txt[c:]
txt = re.sub(r"for \(let v = -100; v <= 150; v \+= 50\) addLabel\('x ' \+ v, \(\) => m2s\(v, 230, wlz\(\)\), 'dim', 'axis'\);", "for (let v = -50; v <= 50; v += 50) addLabel('x ' + v, () => m2s(v, 215, wlz()), 'dim', 'axis');", txt)
txt = re.sub(r"for \(let v = 250; v <= 400; v \+= 50\) addLabel\('y ' \+ v, \(\) => m2s\(-110, v, wlz\(\)\), 'dim', 'axis'\);", "for (let v = 250; v <= 300; v += 50) addLabel('y ' + v, () => m2s(-90, v, wlz()), 'dim', 'axis');", txt)
txt = txt.replace("bar(100, 418, 50, '50 m'); bar(100, 408, 10, '10 m');", "bar(30, 340, 50, '50 m'); bar(30, 330, 10, '10 m');", 1)
# setWater / refreshWL / hash
txt = txt.replace("function setWater(z) { state.wl = z; water.position.y = z; gridG.position.y = z; barG.position.y = z; northG.position.y = z; refreshWL(); writeHash(); }",
                  "function setWater(z) { state.wl = z; const y = wlY(); water.position.y = y; gridG.position.y = y; barG.position.y = y; northG.position.y = y; refreshWL(); writeHash(); }", 1)
assert "const y = wlY(); water.position.y" in txt
i = txt.index("  if ($('wlo')) $('wlo').innerHTML ="); j = txt.index("\n", i)
txt = txt[:i] + "  if ($('wlo')) $('wlo').innerHTML = `<b>${fmt(z)} m MSL</b> = RL ${fmt(z + rlOff())} m (design datum; reading ${READ}) = ${(z + 0.78).toFixed(2)} m above the tide-gauge datum`;" + txt[j:]
# views
a = txt.index("const T = m2s(-10, 330, -2);"); b = txt.index("function gotoView")
views = """const T = m2s(0, 270, -3);
const axisH = M.axis_xy ? M.axis_xy.head : [-12, 312], axisT = M.axis_xy ? M.axis_xy.tail : [60, 240];
const VIEWS = {
  oblique: { label: 'Oblique from sea', pos: () => m2s(45, 388, 44), tgt: () => m2s(0, 270, -3 * state.ve) },
  plan: { label: 'Plan (north = left)', pos: () => m2s(0, 272, 260), tgt: () => m2s(0, 270, 0) },
  crest: { label: 'Along the south arm crest', pos: () => { const d = [axisT[0] - axisH[0], axisT[1] - axisH[1]], L = Math.hypot(...d); return m2s(axisT[0] + d[0] / L * 25, axisT[1] + d[1] / L * 25, 3.0); }, tgt: () => m2s(axisH[0], axisH[1], -2) },
  shore: { label: 'From the shore side (eye 1.7 m)', pos: () => m2s(0, 205, 1.7), tgt: () => m2s(0, 280, -2) },
  side: { label: 'Side view along shore', pos: () => m2s(-200, 270, 6), tgt: () => m2s(0, 270, -3) },
};
"""
txt = txt[:a] + views + txt[b:]
# controls tab text
i = txt.index('<div class="row small" style="justify-content:space-between;margin:0">'); j = txt.index('<h3>Vertical exaggeration</h3>')
txt = txt[:i] + """<div class="small">${M.ui.slider_note}</div>
  <h3>Datum reading</h3>
  <div class="row"><select id="rd"><option value="A">A: RL = chart datum (default)</option><option value="B">B: RL = MSL (Blacka 2013)</option></select></div>
  <div class="small">${M.ui.datum_switch}</div>
  """ + txt[j:]
i = txt.index('<div class="small">Rock: <span style="color:#9a9c9e">'); j = txt.index('</div>', i) + 6
txt = txt[:i] + '<div class="small">${M.ui.legend}</div>' + txt[j:]
i = txt.index('<h3>Seabed in this model</h3>'); j = txt.index('`;', i)
txt = txt[:i] + '<h3>Seabed in this model</h3>\n  <div class="small">${M.ui.seabed}</div>\n  <h3>Later changes (not modelled)</h3><div class="small">${M.ui.later_note}</div>\n  ' + txt[j:]
txt = txt.replace("  $('wl').oninput = e => setWater(parseFloat(e.target.value));", "  $('wl').oninput = e => setWater(parseFloat(e.target.value));\n  $('rd').onchange = e => { READ = e.target.value; setWater(state.wl); updateInfoText(); };", 1)
# version info text + modal
i = txt.index("function updateInfoText() {"); j = txt.index("\n}\n", i) + 3
txt = txt[:i] + """function updateInfoText() {
  const v = verObj();
  const vol = v.volume_m3 ? `rock volume ${v.volume_m3.toLocaleString()} m³ (±${v.volume_unc_m3.toLocaleString()} m³ from the bed level; mean thickness ${v.mean_thickness_m} m, max ${v.max_thickness_m} m)` : 'plan outline only (no design levels in this source, not modelled in 3D)';
  $('vinfo').innerHTML = `<b>${v.name}</b><br>Footprint ${v.area_m2.toLocaleString()} m² (${v.bbox_m[0]} x ${v.bbox_m[1]} m bbox); ${vol}. Edge: ${v.level}. ${v.note}`;
}
""" + txt[j:]
i = txt.index("const SRCN = {"); j = txt.index("\n", i)
txt = txt[:i] + "const SRCN = M.source_names || {};" + txt[j:]
i = txt.index("$('info').onclick = () => {"); j = txt.index("$('modal').style.display = 'flex';", i)
txt = txt[:i] + """$('info').onclick = () => {
  const rows = M.versions.map(v => `<tr><td><b>${v.name}</b>${v.id === M.default_version ? ' (default)' : ''}</td><td>${v.date}</td><td>${v.source_ids.map(i => SRCN[i] || i).join('; ')}</td><td>${v.area_m2.toLocaleString()} m²</td><td>${v.volume_m3 ? v.volume_m3.toLocaleString() + ' m³' : 'n/a'}</td><td>${v.level}</td></tr>`).join('');
  $('modalc').innerHTML = `<h2>Outline versions</h2><p>${M.versions_info}</p><table><tr><th>Name</th><th>Date</th><th>Source</th><th>Footprint</th><th>Volume (model)</th><th>Edge = </th></tr>${rows}</table>
  <p class="small">Volumes: rock above the modelled bed, fitted to the stated 5,500 m³ for the default (Blacka 2013). Version ids for the URL hash: ${M.versions.map(v => v.id).join(', ')}.</p>`;
  """ + txt[j:]
txt = txt.replace("z = 0 at MSL (z_MSL = z_ODN − 0.31). Not for navigation.", "z = 0 at MSL (reading A: z_MSL = RL − 0.78). Design drawing, not a survey. Not for navigation.", 1)
# datum table in sources tab
i = txt.index("<h3>Datum levels (mODN to model z)</h3>"); j = txt.index("</table>`;", i)
txt = txt[:i] + "<h3>Water levels (m MSL, reading A; RL = z + 0.78)</h3><table><tr><th>Level</th><th>RL</th><th>m MSL</th><th>Source</th></tr>${allLevels.map(l => `<tr><td>${l.name}</td><td>${fmt(l.rl)}</td><td>${fmt(l.z)}</td><td class=\"${l.estimated ? 'est' : ''}\">${l.source}</td></tr>`).join('')}" + txt[j:]
# photo match json, cursor, hud
txt = txt.replace("model: 'borth-coastal-defence-reef'", "model: 'cables-reef-wa'", 1)
txt = txt.replace("z_mODN: +(c.z + ZODN).toFixed(2)", "z_RL_m: +(c.z + ZODN).toFixed(2), datum_reading: READ", 1)
txt = re.sub(r"z \$\{fmt\(h\.point\.y / state\.ve\)\} m MSL = \$\{fmt\(h\.point\.y / state\.ve \+ ZODN\)\} mODN  \(\$\{\(state\.wl - h\.point\.y / state\.ve\)\.toFixed\(2\)\} m below water\)", "z ${fmt(h.point.y / state.ve + OFFA - rlOff())} m MSL = RL ${fmt(h.point.y / state.ve + OFFA)}  (${(wlY() - h.point.y / state.ve).toFixed(2)} m below water)", txt)
txt = txt.replace("m MSL (${fmt(c.z + ZODN, 1)} mODN)", "m scene (RL ${fmt(c.z + ZODN, 1)})", 1)
txt = txt.replace("'canonical x south, y offshore (west), metres'", "'model x south, y offshore (west), metres; z scene = RL - 0.78'", 1)
txt = txt.replace("['x', 'x alongshore (+south) m', -300, 300, 0.5], ['y', 'y offshore (west) m', -50, 700, 0.5]", "['x', 'x alongshore (+south) m', -300, 300, 0.5], ['y', 'y offshore (west) m', 100, 700, 0.5]", 1)
txt = txt.replace("Beach preset: the reef is about 300 m offshore, so a phone photo shows it very small", "The reef is about 270 m offshore, so a phone photo shows it very small", 1)
txt = txt.replace("ph = { x: 0, y: 20, z: 1.7, h: 270, p: 0, fov: 60, op: 0.5, on: false }", "ph = { x: 0, y: 205, z: 1.7, h: 270, p: 0, fov: 60, op: 0.5, on: false }", 1)
open('index.html', 'w', encoding='utf-8').write(txt)
left = [m for m in ('Borth', 'borth', 'ODN', 'Aberystwyth', 'defence line') if m in txt]
print('written', len(txt), 'leftover words:', left)

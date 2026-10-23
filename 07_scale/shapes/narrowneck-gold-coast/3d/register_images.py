"""register_images.py - STEP 0 results + new images of the Narrowneck 3D run into 03_images/reefs/narrowneck-gold-coast (uses scripts/nnreg.py with the cloud paths).
Idempotent: new rows are skipped when the sha256 is already registered; update() only rewrites results."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
import nnreg as N
N.ROOT = ROOT; N.REG = os.path.join(ROOT, '03_images', 'reefs'); N.JS = os.path.join(N.REG, N.SLUG, 'images.json'); N.MD = os.path.join(N.REG, N.SLUG, 'IMAGES.md'); N.LOG = os.path.join(N.REG, 'NEW_IMAGES_LOG.md')
N.TODAY = '2026-10-10'; N.BY = 'narrowneck-gold-coast 3D model (stage 2), 2026-10-10'
P = '07_scale/shapes/narrowneck-gold-coast/3d/'
S = lambda i: 'narrowneck-gold-coast-img-%02d' % i
LINK = [P + 'SOURCES_3D.md', P + 'METHODS_3D.md']
N.update(S(55), pending=False, add_annotated=[P + 'annotated/A1_corbett_fig3_digitised.png'], used_for_add=['3d_crest'], linked_add=LINK,
         result='DIGITISED 2026-10-10 (3d/prep_multibeam.py): scale 0.4651 m/px; hue -> depth via the colour bar; bed (containers removed) -4 m at the arm ends to -7 m at the toe; relief p90 0.9-1.2 m, p99 1.8-2.2 m; shallowest tops -1.8 (S arm) / -2.5 (N arm) m vs measured crest -2.2 m AHD (datum AHD supported). Placed at (x -5, y 290) m +-10 m.',
         how_append='3D (2026-10-10): digitised into 3d/src/multibeam_fig3.npz; gives the seabed in a 164 x 145 m window and container relief; METHODS_3D 3.2-3.3, 4.2-4.3.')
N.update(S(31), pending=False, add_annotated=[P + 'annotated/A3_vieira_fig3_reef_bed_read.png'], linked_add=LINK,
         result='Read 2026-10-10 (survey 1, 19 Jul 2018, AHD): bed at the reef cyan about -4 to -6, seaward blue -7 to -9, nearshore -1 to -2 within ~100 m: consistent with the model bed (-3.9..-5.1 at y 235-265, -5.8..-7.3 under the reef, -9.6 at 460 m) within +-1 m.',
         how_append='3D (2026-10-10): cross-check of the seabed profile and the nearshore control point (-1.8 m at y 100); METHODS_3D 4.4.')
for i in (4, 1):
    N.update(S(i), pending=False, add_annotated=[P + 'annotated/A4_jackson2012_fig2_contours_read.png'], linked_add=LINK,
             result='Read 2026-10-10: revised design contours -2.50, -3.00, -3.50, -4.00, -4.50, -5.00, -6.00, outer -8.00; crest wedge -2.50 at the shoreward end of each arm; datum not printed (AHD assumed). Used as the surface rule (crest loops + -6 envelope, linear in distance rank); check vs multibeam tops: mean offset +0.26 m, sd 0.66 m (METHODS_3D 4.2).')
N.update(S(50), pending=False, add_annotated=[P + 'annotated/A2_navionics_readings_used.png'], linked_add=LINK,
         result='Read 2026-10-10: labels 7, 8, 9, 10 m (LAT assumed) at y ~402, 411, 474, 514 m used for the seaward bed (AHD = -(depth) - 0.76); 4.0-4.5 over the arms is a smoothed shoal (crest -2.2 AHD = 1.44 m below LAT), not used for the crest; chart land edge is ~80 m seaward of our 2020 waterline so its nearshore contours are not used.')
N.update(S(51), pending=False, linked_add=LINK, result='2026-10-10: the 0.9 spot depth is NOT used (older crest state, 2001-2012 about -1.0 m LAT; Jackson 2007 p.9). Lior asked to read the label in the app (3d/REQUESTS_FOR_LIOR.md).')
N.update(S(14), pending=False, linked_add=LINK, result='2026-10-10: sketch of T2 on 2 x T4 (two layers at the crest); no dimensions, so no height read from it; the model height comes from the 2017 multibeam relief (1-2.5 m).')
N.update(S(24), pending=False, linked_add=LINK, result='2026-10-10: planform (arms converging seaward, channel between) and surf peeling from the north arm are consistent with the model; no number read (oblique, unscaled). Candidate for the photo-match mode.')
N.update(S(1), pending=False, linked_add=LINK, result='2026-10-10: page render of Jackson 2012 p.3; the same Fig 2 as img-04 (see its result); crest -2.50 consistent with -2.5 m AHD design; datum not printed.')
CIT = 'This project (2026). Narrowneck Reef 3D model, 07_scale/shapes/narrowneck-gold-coast/3d (build_3d.py, make_annotations.py, make_previews.py), generated 2026-10-10 from the sources cited in METHODS_3D.md.'
RIGHTS = 'Own figure from third-party data (Esri, Corbett et al. 2023, Garmin Navionics, MSQ); private research copy.'
def new(f, title, shows, how, kind='diagram'):
    N.add(P + f, kind, title, CIT, 'not online (generated)', 'this project', 'figure', '2026-10-10', 'Claude (3D agent) for Lior; underlying data credited in METHODS_3D.md', RIGHTS, shows, True, 'renewed (June 2018) as modelled',
          ['cross_check', '3d_seabed'] if f.startswith('annotated') else ['context'], how, {'pending': False, 'what_to_check': 'none: derived figure', 'model_values_affected': []}, (), LINK)
new('annotated/A5_profile_model_vs_sources.png', 'Narrowneck 3D: model seabed and reef top vs the sources along the shore-normal', 'Profile y = -40..550 m: model seabed (x = 0), multibeam bed band, shallowest multibeam tops, model reef top (default version), Navionics labels 7-10 m, Vieira da Silva ranges and the MSQ tide planes in m AHD.', 'Validation of the seabed and crest levels (METHODS_3D 4.3-4.4).')
new('annotated/A6_versions_on_seabed.png', 'Narrowneck 3D: the five outline versions on the model seabed', 'Plan of the five outlines (photo 2020 default, Option 2 2017, 2004 design, 2011 survey zone, Navionics shoals), the 24 faint patches and the multibeam window on the model seabed.', 'Compares the versions (METHODS_3D 4.1).')
new('preview_oblique.png', 'Narrowneck 3D viewer: oblique view from the sea at MSL', 'Screenshot of the three.js viewer: two container arms and the paddle channel on the model seabed under a translucent MSL water plane, with grid and labels.', 'Visual check of the model (scale, orientation, labels).', 'diagram')
new('preview_plan.png', 'Narrowneck 3D viewer: plan view at LAT', 'Screenshot of the viewer in plan (north = right, shore = top): arms converging seaward, grid 10 m, scale bars.', 'Visual check of the plan and scale.', 'diagram')
N.update(S(69), pending=False, linked_add=LINK, result='2026-10-10: a surfer stands on the crest in a wave trough with ankle-deep water (date, tide and wave height unknown, before 2013 = pre-renewal crest): qualitatively consistent with a crest 1.2-1.7 m below LAT (wave-trough drawdown, Corbett 2023 p.4-5 critical flow at RL -2.5 AHD); no number read, not used for geometry.')

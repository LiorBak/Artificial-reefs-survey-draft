"""style.py - shared figure style of the surf-reef review paper (08_paper/figures).

Import in every figure script:   from style import SLUGS, NAMES, COLORS, MARKERS, setup, save, cm
One colour (+ one marker) per reef, the same in ALL figures. Colour-blind check (dataviz validate_palette.js, light mode):
lightness band PASS, chroma floor PASS, normal-vision separation PASS, CVD separation WARN (worst adjacent pair
Bunbury/Mexico, dE 6.2 protan = floor band), so identity is ALSO carried by a unique marker shape and by direct labels.
Palette = Okabe-Ito / Tol hues, in the dataset order of 08_paper/data/reefs.json.
"""
import os

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
FIG_DIR = os.path.join(REPO, '08_paper', 'figures')
DATA_DIR = os.path.join(REPO, '08_paper', 'data')
SHAPES = os.path.join(REPO, '07_scale', 'shapes')

# dataset order (reefs.json)
SLUGS = ['narrowneck-gold-coast', 'cables-reef-wa', 'prattes-reef-el-segundo', 'mount-maunganui-reef', 'opunake-reef',
         'boscombe-surf-reef', 'kovalam-reef-india', 'borth-coastal-defence-reef', 'palm-beach-gold-coast',
         'southern-ocean-surf-reef-albany', 'burkitts-reef-bargara', 'bunbury-airwave', 'mexico-reef-2026-unnamed']

NAMES = {  # short labels used in all figures
    'narrowneck-gold-coast': 'Narrowneck', 'cables-reef-wa': 'Cables', 'prattes-reef-el-segundo': "Pratte's",
    'mount-maunganui-reef': 'Mt Maunganui', 'opunake-reef': 'Opunake', 'boscombe-surf-reef': 'Boscombe',
    'kovalam-reef-india': 'Kovalam', 'borth-coastal-defence-reef': 'Borth', 'palm-beach-gold-coast': 'Palm Beach',
    'southern-ocean-surf-reef-albany': 'Albany', 'burkitts-reef-bargara': 'Burkitts', 'bunbury-airwave': 'Bunbury Airwave',
    'mexico-reef-2026-unnamed': 'Xala (Mexico)'}

PLACE = {  # place + country code, second label line
    'narrowneck-gold-coast': 'Gold Coast, AU', 'cables-reef-wa': 'Perth, AU', 'prattes-reef-el-segundo': 'California, US',
    'mount-maunganui-reef': 'Bay of Plenty, NZ', 'opunake-reef': 'Taranaki, NZ', 'boscombe-surf-reef': 'Dorset, UK',
    'kovalam-reef-india': 'Kerala, IN', 'borth-coastal-defence-reef': 'Ceredigion, UK', 'palm-beach-gold-coast': 'Gold Coast, AU',
    'southern-ocean-surf-reef-albany': 'Albany, AU', 'burkitts-reef-bargara': 'Bargara, AU', 'bunbury-airwave': 'Bunbury, AU',
    'mexico-reef-2026-unnamed': 'Jalisco, MX'}

COLORS = {
    'narrowneck-gold-coast': '#0072B2', 'cables-reef-wa': '#E69F00', 'prattes-reef-el-segundo': '#CC79A7',
    'mount-maunganui-reef': '#009E73', 'opunake-reef': '#882255', 'boscombe-surf-reef': '#D55E00',
    'kovalam-reef-india': '#8E6BBE', 'borth-coastal-defence-reef': '#56B4E9', 'palm-beach-gold-coast': '#5E4FA2',
    'southern-ocean-surf-reef-albany': '#117733', 'burkitts-reef-bargara': '#AA4499', 'bunbury-airwave': '#1F9E89',
    'mexico-reef-2026-unnamed': '#EE6677'}

# MARKER SHAPE = OUTCOME CLASS (Lior's review 2026-10-19: no per-reef shapes; colour + name label = reef, shape = outcome).
# Outcome per reef = reefs.json surf_outcome.value (read below). 'unknown' is a small HOLLOW square so it never looks like
# 'works' (filled circle). Every figure that uses these shapes carries outcome_legend_handles().
OUTCOME_CLASSES = ['works', 'works rarely', 'mixed', 'does not work', 'unknown']
OUTCOME_MARKER = {'works': 'o', 'works rarely': '^', 'mixed': 'D', 'does not work': 'X', 'unknown': 's'}
OUTCOME_HOLLOW = {'unknown'}
OUTCOME_SIZE = {'works': 1.0, 'works rarely': 1.0, 'mixed': 0.85, 'does not work': 1.05, 'unknown': 0.7}


def outcome_class(o):
    """reefs.json surf_outcome value -> one of OUTCOME_CLASSES"""
    if not isinstance(o, str):
        return 'unknown'
    o = o.strip().lower()
    if o.startswith('works rarely'):
        return 'works rarely'
    if o.startswith('mixed'):
        return 'mixed'
    if o.startswith('does not'):
        return 'does not work'
    if o == 'works':
        return 'works'
    return 'unknown'


def _load_outcomes():
    import json
    try:
        R = json.load(open(os.path.join(DATA_DIR, 'reefs.json'), encoding='utf-8'))
        return {r['slug']: outcome_class((r.get('surf_outcome') or {}).get('value')) for r in R}
    except Exception:
        return {}


OUTCOME = _load_outcomes()
MARKERS = {s: OUTCOME_MARKER[OUTCOME.get(s, 'unknown')] for s in SLUGS}

# neutral inks / grounds (shared)
INK = '#222222'
INK2 = '#555555'
GRID = '#D9D9D9'
UNKNOWN = '#9A9A9A'
SEA = '#EAF3FA'      # sea ground (plan)
SAND = '#F1E7D0'     # beach / seabed fill
SEABED = '#8A6D3B'   # seabed line
TIDE = '#9CC7E8'     # tide band

CM = 1 / 2.54
FULL_W = 17.0 * CM   # inches, full A4 text width
COL_W = 8.3 * CM     # inches, one column


def cm(x):
    return x / 2.54


def setup():
    """matplotlib rcParams: sans-serif, >= 7 pt at print size, vector fonts embedded (Type 42)."""
    from matplotlib import font_manager
    fam = 'DejaVu Sans'
    for f in ('Liberation Sans', 'Arial', 'Helvetica'):
        try:
            font_manager.findfont(f, fallback_to_default=False)
            fam = f
            break
        except Exception:
            pass
    plt.rcParams.update({
        'font.family': fam, 'font.size': 7.5, 'axes.labelsize': 7.5, 'axes.titlesize': 8, 'xtick.labelsize': 7,
        'ytick.labelsize': 7, 'legend.fontsize': 7, 'axes.linewidth': 0.6, 'xtick.major.width': 0.6,
        'ytick.major.width': 0.6, 'xtick.major.size': 2.5, 'ytick.major.size': 2.5, 'lines.linewidth': 1.0,
        'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': INK2, 'axes.labelcolor': INK,
        'xtick.color': INK, 'ytick.color': INK, 'text.color': INK, 'figure.facecolor': 'white',
        'axes.facecolor': 'white', 'savefig.facecolor': 'white', 'pdf.fonttype': 42, 'ps.fonttype': 42,
        'svg.fonttype': 'none', 'mathtext.default': 'regular'})
    return fam


def _dark(c, f=0.6):
    from matplotlib import colors as mc
    r, g, b = mc.to_rgb(c)
    return (r * f, g * f, b * f)


def marker_kw(slug, ms=6.0, outcome=None):
    """matplotlib plot kwargs for one reef point: colour = reef, shape = outcome class (hollow for unknown)."""
    oc = outcome_class(outcome) if outcome is not None else OUTCOME.get(slug, 'unknown')
    col = COLORS.get(slug, UNKNOWN)
    hollow = oc in OUTCOME_HOLLOW
    return dict(marker=OUTCOME_MARKER[oc], ms=ms * OUTCOME_SIZE[oc], mfc='white' if hollow else col,
                mec=col if hollow else _dark(col), mew=1.1 if hollow else 0.5, ls='none')


def outcome_legend_handles(ms=5.5, color='#7F7F7F'):
    """legend entries for the outcome shapes (grey; the colour of a real point is the reef's colour)"""
    from matplotlib.lines import Line2D
    lab = {'works': 'works', 'works rarely': 'works rarely', 'mixed': 'mixed / disputed', 'does not work': 'does not work',
           'unknown': 'unknown (hollow)'}
    out = []
    for oc in OUTCOME_CLASSES:
        hollow = oc in OUTCOME_HOLLOW
        out.append(Line2D([0], [0], marker=OUTCOME_MARKER[oc], ms=ms * OUTCOME_SIZE[oc], mfc='white' if hollow else color,
                          mec=color if hollow else _dark(color), mew=1.1 if hollow else 0.5, ls='none', label=lab[oc]))
    return out


def save(fig, name, dpi=300):
    """Write <name>.png (300 dpi) and <name>.pdf (vector) into 08_paper/figures/."""
    os.makedirs(FIG_DIR, exist_ok=True)
    fig.savefig(os.path.join(FIG_DIR, name + '.png'), dpi=dpi)
    fig.savefig(os.path.join(FIG_DIR, name + '.pdf'))
    plt.close(fig)
    return [os.path.join(FIG_DIR, name + e) for e in ('.png', '.pdf')]

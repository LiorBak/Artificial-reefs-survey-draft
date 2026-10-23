"""Render overlays/img10_phase3_zones_oblique_and_esri2016_v1.png. Run: python -I render_phase3_overlay.py <shape folder> <obl_grid.png>
obl_grid.png = photo crop of J&C Fig 1 (03_images/.../jc2007-fig1-phase3-aerial_p1.png cropped (30,25,580,575), resized 2x LANCZOS)."""
import sys, json, math
from pathlib import Path
from PIL import Image, ImageDraw
root = Path(sys.argv[1]); R = json.load(open(root/'scripts/phase3_zone_v1.json'))
src = Image.open(sys.argv[2]).convert('RGB').resize((600, 600))
base = Image.open(root/'src/wayback/burkitts_esri_wayback-rel23264_img2016-07-31_z18_north.png').convert('RGB').resize((1180, 1180), Image.LANCZOS)
g = json.load(open(root/'src/wayback/burkitts_esri_wayback-rel23264_img2016-07-31_z18_north.png.geo.json'))
def my(l): return math.log(math.tan(math.pi/4+math.radians(l)/2))
def ll2grid(la, lo):
    b = g['bounds']; fx = (lo-b['west'])/(b['east']-b['west']); fy = (my(la)-my(b['north']))/(my(b['south'])-my(b['north']))
    return fx*1180, fy*1180
d = ImageDraw.Draw(base)
d.polygon([ll2grid(*p) for p in R['ellipse_polygon_latlon']], outline=(255, 0, 0), width=3)
for k, (n, (la, lo)) in enumerate(R['arrow_tips_latlon'].items(), 1):
    x, y = ll2grid(la, lo); d.ellipse([x-8, y-8, x+8, y+8], outline=(255, 255, 0), width=3); d.text((x+10, y-6), str(k)+' '+n[:28], fill=(255, 255, 0))
for k, (x, y) in R['gcp_sat_grid'].items():
    d.polygon([(x, y-9), (x+9, y), (x, y+9), (x-9, y)], outline=(0, 255, 255), width=2); d.text((x+11, y-6), 'GCP '+k, fill=(0, 255, 255))
sc = 600/1100; d2 = ImageDraw.Draw(src)
for k, (x, y) in R['gcp_oblique'].items():
    x, y = x*sc, y*sc; d2.polygon([(x, y-6), (x+6, y), (x, y+6), (x-6, y)], outline=(0, 255, 255)); d2.text((x+8, y-5), 'GCP '+k, fill=(0, 255, 255))
d2.text((6, 6), 'J&C 2007 Fig 1 (Redgard photo): GCPs', fill=(255, 255, 0))
out = Image.new('RGB', (1200, 600), 'white'); out.paste(src, (0, 0)); out.paste(base.resize((600, 600), Image.LANCZOS), (600, 0))
ImageDraw.Draw(out).text((606, 6), 'Esri Wayback img 2016-07-31 (Maxar/DigitalGlobe): mapped zone, arrow tips 1-4, GCPs', fill=(255, 255, 0))
out.save(root/'overlays/img10_phase3_zones_oblique_and_esri2016_v1.png')

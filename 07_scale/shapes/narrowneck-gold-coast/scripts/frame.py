import numpy as np, json, math, sys
sys.path.insert(0,r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\tools")
import satellite as S
ROOT=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\shapes\narrowneck-gold-coast"
g19=json.load(open(ROOT+r"\src\wayback\nn_wayback_2020-08-08_r9812_z19.png.geo.json"))
g17=json.load(open('z17_wb9812.png.geo.json'))
pts=np.load('waterline_pts.npy')
A=np.polyfit(pts[:,1],pts[:,0],1)   # x = a*y+b in z17 px
a=A[0]
# two points on the waterline in z17 px -> lat/lon -> z19 px
P=[]
for y in (0,2844):
    x=np.polyval(A,y)
    lat,lon=S.pix2ll(g17,x,y)
    P.append(S.ll2pix(g19,lat,lon))
P=np.array(P)
d=(P[1]-P[0]); d/=np.hypot(*d)
print('waterline in s3 px: through',P[0],'dir (south-heading)',d)
# north-heading alongshore direction in px
u=-d if d[1]>0 else d
print('alongshore (north-heading) px dir',u,'bearing deg',(math.degrees(math.atan2(u[0],-u[1])))%360)
polys=json.load(open('polys_v2.json'))
reef=['north_arm','south_arm','wing_patch_NW_a','wing_patch_NW_b','weir_1','weir_2_faint','weir_3_faint']
import shapely.geometry as sg
from shapely.ops import unary_union
pg=[sg.Polygon(polys[k]) for k in reef]
areas=np.array([p.area for p in pg]); cents=np.array([[p.centroid.x,p.centroid.y] for p in pg])
cen=(cents*areas[:,None]).sum(0)/areas.sum()
print('area-weighted centroid px',cen)
# foot of perpendicular on waterline
v=cen-P[0]; foot=P[0]+np.dot(v,d)*d
print('origin px (foot on waterline)',foot,' distance centroid->waterline m',np.hypot(*(cen-foot))*g19['m_per_px_center'])
json.dump({'origin_px':foot.tolist(),'alongshore_dir_px':u.tolist(),'bearing_north_heading_deg':(math.degrees(math.atan2(u[0],-u[1])))%360,'centroid_px':cen.tolist(),'a_z17':a},open('frame.json','w'))

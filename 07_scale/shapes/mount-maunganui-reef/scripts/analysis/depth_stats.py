import numpy as np, json, math, sys
from scipy import ndimage as ndi
from PIL import Image
R='C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/mount-maunganui-reef/'
pxm=5.45
dep=np.load('dep.npy')              # Fig 3, m CD (swatch mid-depths)
polys=json.load(open(R+'work_polys_fig3_m20_v2.json'))
from PIL import ImageDraw
H,W=dep.shape
def rast(polys):
    im=Image.new('L',(W,H),0); d=ImageDraw.Draw(im)
    for p in polys: d.polygon([tuple(q) for q in p],fill=255)
    return np.array(im)>0
M=rast(polys)
names=['west arm block','mid-top bag','NE small bag','NE lobe','south arm']
# component masks via labels
lab,n=ndi.label(M)
print('Fig 3 (CD): inside -2.0 outline')
for i in range(1,n+1):
    m=lab==i; v=dep[m]
    cy,cx=ndi.center_of_mass(m)
    print(f'  comp {i} centroid px ({cx:.0f},{cy:.0f}) area {m.sum()/pxm**2:.0f} m2: shallowest {v.max():.2f}  p90 {np.percentile(v,90):.2f}  median {np.median(v):.2f}  mean {v.mean():.2f}')
# ambient seabed in rings outside the outline (distance 6-14 m from outline)
dist=ndi.distance_transform_edt(~M)/pxm
ring=(dist>6)&(dist<14)
# sectors by direction of the pixel from the reef centroid: use bearings in the north-up frame
cy,cx=ndi.center_of_mass(M)
yy,xx=np.mgrid[0:H,0:W]
ang=(np.degrees(np.arctan2((xx-cx),-(yy-cy)))%360)   # bearing from reef centroid (grid ~ true)
mapmask=(np.abs(dep)<5)  # all
valid=np.zeros((H,W),bool); valid[70:915,85:890]=True
for name,(a0,a1) in {'seaward NE (22-112)':(22,112),'SE (112-202)':(112,202),'landward SW (202-292)':(202,292),'NW (292-22)':(292,382)}.items():
    a=ang.copy(); sel=((ang>=a0)&(ang<a1)) if a1<=360 else ((ang>=a0)|(ang<a1-360))
    m=ring&sel&valid
    v=dep[m]
    if len(v): print(f'  ring 6-14 m outside, {name}: n={len(v)} median {np.median(v):.2f} p10 {np.percentile(v,10):.2f} p90 {np.percentile(v,90):.2f} min {v.min():.2f}')
# scour hole: deepest region within 40 m of reef
near=(dist<40)&valid
print('  deepest within 40 m of the outline:',dep[near].min())
# area deeper than -3.5 within 25 m
print('  area deeper than -3.4 m within 25 m of outline: %.0f m2'%(((dep<-3.4)&(dist<25)&valid).sum()/pxm**2))
# volume above local ambient bed (plane/ring-median approx per component using ring around it)
def vol(m, comp_ring):
    bed=np.median(dep[comp_ring])
    return float(np.clip(dep[m]-bed,0,None).sum()/pxm**2), bed
tot=0
for i in range(1,n+1):
    m=lab==i
    r=(ndi.distance_transform_edt(~m)/pxm); rr=(r>4)&(r<10)&valid&~M
    v,bed=vol(m,rr); tot+=v
    print(f'  comp {i}: ring bed median {bed:.2f}, volume above ring-median bed (within -2.0 outline) {v:.0f} m3')
print('  total',tot)
# transects: west arm (px x=340: vertical profile y 380..560) ; south arm (px y=650: x 440..580)
for name,pts in {'west arm N-S at x=340':[(340,y) for y in range(380,560)],'south arm W-E at y=650':[(x,650) for x in range(430,590)],'south arm W-E at y=600':[(x,600) for x in range(430,590)]}.items():
    prof=[(round(((p[1]-pts[0][1]) if 'N-S' in name else (p[0]-pts[0][0]))/pxm,2),round(float(dep[p[1],p[0]]),2)) for p in pts]
    # compress consecutive duplicates
    out=[prof[0]]
    for q in prof[1:]:
        if q[1]!=out[-1][1]: out.append(q)
    print(name,out)

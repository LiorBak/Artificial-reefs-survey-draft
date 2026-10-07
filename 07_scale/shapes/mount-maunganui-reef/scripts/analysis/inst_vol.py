import numpy as np, math
from PIL import Image
from scipy import ndimage as ndi
R='C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/mount-maunganui-reef/'
exec(open('reg_inst.py').read().split('mI_raw=')[0])
ppm=5.45*1.0932
valid=okI
print('Installed depth stats (MSL/MVD-53 datum assumed): ppm',ppm)
for T in (-3.8,-4.2):
    m=(depI>T)&okI; m=ndi.binary_opening(m,iterations=1); m=ndi.binary_fill_holes(m)
    lab,n=ndi.label(ndi.binary_closing(m,iterations=2)); sz=ndi.sum(m,lab,range(1,n+1)); keep=[i+1 for i,s in enumerate(sz) if s/ppm**2>15]; mm=np.isin(lab,keep)&m
    dist=ndi.distance_transform_edt(~mm)/ppm
    ring=(dist>5)&(dist<12)&okI
    v=depI[ring]
    cr=depI[mm]
    print(f'T={T}: mask area {mm.sum()/ppm**2:.0f} m2; crest (shallowest 5%) {np.percentile(cr,95):.2f}, p75 {np.percentile(cr,75):.2f}, median {np.median(cr):.2f}; ring 5-12 m: median {np.median(v):.2f} p10 {np.percentile(v,10):.2f} p90 {np.percentile(v,90):.2f}')
    for bed in (np.median(v),-5.0,-5.4):
        vol=np.clip(depI[mm]-bed,0,None).sum()/ppm**2
        print(f'    volume above bed {bed:.2f}: {vol:.0f} m3')
# sectors in rotated (north-up) frame: ring sectors by bearing
dd=np.rot90(depI,k=-1); oo=np.rot90(okI,k=-1)
m=(dd>-3.8)&oo; m=ndi.binary_opening(m,iterations=1); lab,n=ndi.label(ndi.binary_closing(m,iterations=2)); sz=ndi.sum(m,lab,range(1,n+1)); mm=np.isin(lab,[i+1 for i,s in enumerate(sz) if s/ppm**2>15])&m
cy,cx=ndi.center_of_mass(mm); yy,xx=np.mgrid[0:dd.shape[0],0:dd.shape[1]]
ang=np.degrees(np.arctan2(xx-cx,-(yy-cy)))%360
dist=ndi.distance_transform_edt(~mm)/ppm; ring=(dist>5)&(dist<12)&oo
for name,(a0,a1) in {'seaward NE':(22,112),'SE':(112,202),'landward SW':(202,292),'NW':(292,382)}.items():
    sel=((ang>=a0)&(ang<a1)) if a1<=360 else ((ang>=a0)|(ang<a1-360))
    v=dd[ring&sel]
    if len(v): print(f'  ring sector {name}: median {np.median(v):.2f} p10 {np.percentile(v,10):.2f} p90 {np.percentile(v,90):.2f} min {v.min():.2f}')
print('deepest in image',depI[okI].min(), 'area deeper than -6.2 (scour) m2', ((depI<-6.2)&okI).sum()/ppm**2)

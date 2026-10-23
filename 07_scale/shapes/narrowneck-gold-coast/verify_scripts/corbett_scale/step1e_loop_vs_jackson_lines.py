import numpy as np, cv2, json, math
from PIL import Image
from scipy import ndimage
R="C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/narrowneck-gold-coast/"
jk=np.asarray(Image.open(R+"src/gov/narrowneck-gold-coast_jackson2012_fig2_reef_levels_original_and_revised_design_300dpi_crop.png").convert("L"))
jr=jk[:,1020:]; dark=(jr<150); dtJ=ndimage.distance_transform_edt(~dark)
f=json.load(open('c3_fit.json')); s,a,th,tx,ty=f['fit']; c0=np.array(f['c0'])
def tf(P):
    q=np.asarray(P,float)-c0; c,sn=math.cos(th),math.sin(th); X=q[:,0]*s; Y=q[:,1]*s*a
    return np.c_[c*X-sn*Y+tx, sn*X+c*Y+ty]
loops=json.load(open('corbett_loops2.json'))
for nm in ("L_N","L_S"):
    p=tf(loops[nm]['pts']); d=ndimage.map_coordinates(dtJ,[p[:,1],p[:,0]],order=1)
    # centreline correction: Corbett pts are the outer edge of a ~3-4 px (Corbett) line -> ~2 Corbett px = 3 Jackson px outside the centreline
    print(nm,"dist of Corbett loop outer edge to nearest Jackson line px: median",np.median(d).round(1),"p90",np.percentile(d,90).round(1),"max",d.max().round(1),"frac>8px",(d>8).mean().round(2))
    far=p[d>8]
    if len(far): print("   far pts bbox (Jackson px)",far.min(0).round(0),far.max(0).round(0), "n",len(far))
# Jackson ring component for N loop: bbox of dark component containing loop interior seed
dk=dark.astype(np.uint8); n,lab,st,cen=cv2.connectedComponentsWithStats(dk,8)
# which component holds the N loop line: the one whose bbox is smallest containing (170,170)?
cands=[(st[i,4],i) for i in range(1,n) if st[i,0]<150 and st[i,0]+st[i,2]>250 and st[i,1]<130 and st[i,1]+st[i,3]>250 and st[i,4]>300]
print("cands",[(a,tuple(st[i,:4])) for a,i in cands][:6])

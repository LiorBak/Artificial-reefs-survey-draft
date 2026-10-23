import numpy as np, cv2, json
from PIL import Image
R="C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/narrowneck-gold-coast/"
im=np.asarray(Image.open(R+"src/gov/corbett2023_extracted/p3_x88.png").convert("RGB")).astype(int)
sat=im.max(axis=2)-im.min(axis=2)
grey=((sat<12)&(im[...,1]>185)&(im[...,1]<232)).astype(np.uint8); grey[:,:412]=0
op=cv2.morphologyEx(grey,cv2.MORPH_OPEN,np.ones((5,5),np.uint8))
n,lab,st,cen=cv2.connectedComponentsWithStats(op,8)
keep=np.zeros_like(op)
for i in range(1,n):
    if st[i,4]>250: keep[lab==i]=1; print("blob",st[i])
keep=cv2.morphologyEx(keep,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)))
H,W=keep.shape
loops=json.load(open('corbett_loops2.json'))
def fillmask(pts):
    m=np.zeros((H,W),np.uint8); cv2.fillPoly(m,[np.array(pts,np.int32)],1); return m
np.save('grey_keep.npy',keep)
for nm,rows in (("N",(0,150)),("S",(190,300))):
    L=fillmask(loops["L_"+nm]['pts']); g=keep.copy(); g[:rows[0]]=0; g[rows[1]:]=0
    print(nm,"grey area",g.sum(),"loop area",L.sum(), "grey bbox",cv2.boundingRect(g))
    res=[]
    for dx in range(335,380):
        for dy in range(-40,30):
            M=np.roll(np.roll(L,dx,axis=1),dy,axis=0)
            inter=(M&g).sum(); res.append((inter/g.sum(),inter/M.sum(),dx,dy))
    res.sort(key=lambda r:-(r[0]*r[1])); print(" best (cov grey, loop in grey, dx, dy)",[(round(a,2),round(b,2),c,d) for a,b,c,d in res[:4]])

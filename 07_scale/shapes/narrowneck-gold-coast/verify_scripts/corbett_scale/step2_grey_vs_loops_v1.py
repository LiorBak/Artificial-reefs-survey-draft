import numpy as np, cv2, json
from PIL import Image
R="C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/narrowneck-gold-coast/"
im=np.asarray(Image.open(R+"src/gov/corbett2023_extracted/p3_x88.png").convert("RGB")).astype(int)
sat=im.max(axis=2)-im.min(axis=2)
grey=((sat<12)&(im[...,1]>185)&(im[...,1]<232)).astype(np.uint8); grey[:,:412]=0
# bridge thin lines: close
greyc=cv2.morphologyEx(grey,cv2.MORPH_CLOSE,np.ones((5,5),np.uint8))
H,W=grey.shape
loops=json.load(open('corbett_loops.json'))
def fillmask(pts):
    m=np.zeros((H,W),np.uint8); cv2.fillPoly(m,[np.array(pts,np.int32)],1); return m
for nm,rows in (("N",(0,150)),("S",(190,300))):
    L=fillmask(loops["L_"+nm]['pts'])
    best=None
    for infl in (0,4,8):
        Li=cv2.dilate(L,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*infl+1,2*infl+1))) if infl else L
        res=[]
        for dx in range(330,420):
            for dy in range(-40,30):
                M=np.roll(np.roll(Li,dx,axis=1),dy,axis=0)
                g=greyc.copy(); g[:rows[0]]=0; g[rows[1]:]=0
                inter=(M&g).sum(); union=((M|g)>0).sum()
                res.append((inter/union,dx,dy))
        res.sort(reverse=True); print(nm,"infl",infl,"best IoU,dx,dy",[(round(a,3),b,c) for a,b,c in res[:3]])

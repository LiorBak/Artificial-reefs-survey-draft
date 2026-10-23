import numpy as np, cv2, json
from PIL import Image
R="C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/narrowneck-gold-coast/"
rgb=np.asarray(Image.open(R+"src/gov/corbett2023_extracted/p3_x88.png").convert("RGB"))
im=rgb.astype(int); H,W,_=im.shape
line=(im.min(axis=2)<205).astype(np.uint8)
# remove frame and scale bar/text region
for (x0,x1) in ((0,12),(352,420),(758,W)): line[:,x0:x1]=0
line[:14,:]=0; line[322:,:]=0
line[262:,600:760]=0   # scale bar + numbers (right panel)
out={}
for tag,(x0,x1) in (("L",(10,354)),("R",(414,760))):
    m=np.zeros_like(line); m[:,x0:x1]=line[:,x0:x1]
    n,lab,st,_=cv2.connectedComponentsWithStats(m,8)
    keep=np.zeros_like(m)
    for i in range(1,n):
        if st[i,4]>=60: keep[lab==i]=1
    for r_ in (9,15,19,25):
        pad=40
        cl=cv2.morphologyEx(np.pad(keep,pad),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2*r_+1,2*r_+1)))
        n2,lab2,st2,_=cv2.connectedComponentsWithStats((1-cl).astype(np.uint8),4)
        M=(lab2!=lab2[0,0]).astype(np.uint8)[pad:-pad,pad:-pad]
        cc,_=cv2.findContours(M,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cc,key=cv2.contourArea)
        print(tag,"r",r_,"area px",int(cv2.contourArea(c)),"bbox",cv2.boundingRect(c))
        out[(tag,r_)]=c
vis=rgb.copy()
for tag,col in (("L",(255,0,255)),("R",(255,0,255))):
    cv2.drawContours(vis,[out[(tag,15)]],-1,col,1)
Image.fromarray(vis).resize((W*2,H*2),Image.NEAREST).save('c7_vis.png')

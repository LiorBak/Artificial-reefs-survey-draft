import numpy as np, cv2, json, math
from PIL import Image
R="C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/narrowneck-gold-coast/"
im=np.asarray(Image.open(R+"src/gov/corbett2023_extracted/p3_x88.png").convert("RGB")).astype(int)
mx=im.max(axis=2); mpp=50/97.0
line=(mx<150).astype(np.uint8)
seeds={"R_N":(540,95),"R_S":(530,235),"L_N":(155,92),"L_S":(140,237)}
vis=np.asarray(Image.open(R+"src/gov/corbett2023_extracted/p3_x88.png").convert("RGB")).copy()
res={}
for nm,(sx,sy) in seeds.items():
    # close the line mask a bit to stop leaks via label gaps
    cl=cv2.morphologyEx(line,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
    free=(1-cl).astype(np.uint8)
    if not free[sy,sx]:
        ys,xs=np.where(free[sy-8:sy+9,sx-8:sx+9]==1); sy,sx=ys[0]+sy-8,xs[0]+sx-8
    n,lab=cv2.connectedComponents(free,connectivity=4)
    m=(lab==lab[sy,sx]).astype(np.uint8)
    cc,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cc,key=cv2.contourArea)
    fm=np.zeros_like(m); cv2.drawContours(fm,[c],-1,1,-1)
    # add back half line width (loop line ~3 px wide: centre line) -> dilate by 1
    fm=cv2.dilate(fm,np.ones((3,3),np.uint8))
    c2,_=cv2.findContours(fm,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c2=max(c2,key=cv2.contourArea)
    A=cv2.contourArea(c2); (cx,cy),(w,h),ang=cv2.minAreaRect(c2)
    M=cv2.moments(c2); cen=(M['m10']/M['m00'],M['m01']/M['m00'])
    x,y,bw,bh=cv2.boundingRect(c2)
    res[nm]=dict(area_px=A,area_m2=A*mpp**2,minrect_m=sorted([w*mpp,h*mpp],reverse=True),centroid=cen,bbox_px=(x,y,bw,bh),bbox_m=(bw*mpp,bh*mpp),pts=c2[:,0,:].tolist())
    print(nm,round(A),round(A*mpp**2),[round(v*mpp,1) for v in sorted([w,h],reverse=True)],'centroid',[round(v,1) for v in cen],'bbox m',round(bw*mpp,1),round(bh*mpp,1),'bbox',x,y,bw,bh)
    cv2.drawContours(vis,[c2],-1,(255,0,255),1)
json.dump(res,open('corbett_loops.json','w'))
Image.fromarray(vis.astype(np.uint8)).resize((769*2,334*2),Image.NEAREST).save('corbett_loops_vis.png')
for p in ("L","R"):
    a,b=res[p+"_N"],res[p+"_S"]
    print(p,"centroid sep (m) dx,dy",round((b['centroid'][0]-a['centroid'][0])*mpp,1),round((b['centroid'][1]-a['centroid'][1])*mpp,1),
      "total crest extents vertical m", round((max(b['bbox_px'][1]+b['bbox_px'][3],0)-a['bbox_px'][1])*mpp,1))

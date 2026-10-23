import numpy as np, cv2, json
from PIL import Image
R="C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/narrowneck-gold-coast/"
im=np.asarray(Image.open(R+"src/gov/corbett2023_extracted/p3_x88.png").convert("RGB")).astype(int)
sat=im.max(axis=2)-im.min(axis=2); mpp=50/97
th=135
dk=((im.max(axis=2)<th)&(sat<40)).astype(np.uint8)
want={"L_N":(10,14,72,32),"L_S":(10,14,58,199),"R_N":(414,14,61,40),"R_S":(414,14,52,190)}
out={}
vis=np.asarray(Image.open(R+"src/gov/corbett2023_extracted/p3_x88.png").convert("RGB")).copy()
for nm,(x0,y0,bx,by) in want.items():
    x1=360 if nm[0]=='L' else 764
    sub=dk[14:320,x0:x1]; n,lab,st,cen=cv2.connectedComponentsWithStats(sub,8)
    i=[j for j in range(1,n) if abs(st[j,0]-bx)<=2 and abs(st[j,1]-by)<=2 and st[j,4]>400][0]
    m=(lab==i).astype(np.uint8)
    cc,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cc,key=cv2.contourArea)+[x0,y0]
    A=cv2.contourArea(c); (cx,cy),(w,h),ang=cv2.minAreaRect(c); M=cv2.moments(c)
    x,y,bw,bh=cv2.boundingRect(c)
    out[nm]=dict(pts=c[:,0,:].tolist(),area_px=A,area_m2=A*mpp**2,minrect_m=sorted([w*mpp,h*mpp],reverse=True),cen=[M['m10']/M['m00'],M['m01']/M['m00']],bbox=[x,y,bw,bh])
    print(nm,"area m2 (outer edge of line)",round(A*mpp**2),"minrect m",[round(v,1) for v in out[nm]['minrect_m']],"bbox px",x,y,bw,bh)
    cv2.drawContours(vis,[c],-1,(255,0,255),1)
json.dump(out,open('corbett_loops2.json','w'))
Image.fromarray(vis).resize((769*2,334*2),Image.NEAREST).save('corbett_loops2_vis.png')
for p in "LR":
    a,b=out[p+"_N"],out[p+"_S"]
    print(p,"alongshore crest extent (outer edge N top to outer edge S bottom) m",round((b['bbox'][1]+b['bbox'][3]-a['bbox'][1])*mpp,1),"centroid sep m",[round((b['cen'][k]-a['cen'][k])*mpp,1) for k in (0,1)])

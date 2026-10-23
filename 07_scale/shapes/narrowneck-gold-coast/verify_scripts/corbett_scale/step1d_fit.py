import numpy as np, cv2, json, math
exec(open('c3.py').read().split("res={}")[0])
P=CL; c0=P.mean(0)
r=optimize.minimize(lambda q: cost_fixed(q,P,c0), [1.5,1.0,0.0,251.7,299.7],method="Nelder-Mead",options={"xatol":1e-4,"fatol":1e-6,"maxiter":6000})
s,a,th,tx,ty=r.x; print("fit s,a,th,tx,ty",r.x.round(4),"cost",round(r.fun,3))
q=tf(P,c0,*r.x); d=ndimage.map_coordinates(dtJ,[q[:,1],q[:,0]],order=1,mode='nearest')
print("frac<1.5px",(d<1.5).mean().round(3),"frac<3",(d<3).mean().round(3),"median",np.median(d).round(2))
m_per_jpx=0.2100*1.5908; m_per_cpx=50/97
print("m/px Jackson Fig2 (chain)",round(m_per_jpx,4),"m/px Corbett (bar)",round(m_per_cpx,4),"Corbett bar scale implies m/Jpx",round(m_per_cpx/s,4),"ratio bar/chain",round(m_per_cpx/s/m_per_jpx,3))
# reverse check: Jackson pts -> Corbett DT
dtC=ndimage.distance_transform_edt(~skL)
# transform loops of Corbett to Jackson px
loops=json.load(open('corbett_loops.json'))
for nm in ("L_N","L_S"):
    pts=np.array(loops[nm]['pts'],float); qq=tf(pts,c0,*r.x)
    area=cv2.contourArea(qq.astype(np.float32)); print(nm,"area in Jackson px^2",round(area),"-> m2 with chain scale",round(area*m_per_jpx**2),"with Corbett bar",round(loops[nm]['area_m2']))
json.dump({"fit":r.x.tolist(),"c0":c0.tolist(),"cost":r.fun},open("c3_fit.json","w"))
# Jackson inner loops in Jackson Fig2 px (recompute as in design script)
dk2=(jr<150).astype(np.uint8); dk2[:,500:]=0
n,lab,st,_=cv2.connectedComponentsWithStats(dk2,8); kp2=np.zeros_like(dk2)
for i in range(1,n):
    if st[i,4]>=150: kp2[lab==i]=1
pad=40
cl2=cv2.morphologyEx(np.pad(kp2,pad),cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(33,33)))
n3,lab3,st3,cen3=cv2.connectedComponentsWithStats((1-cl2).astype(np.uint8),4)
for i in range(1,n3):
    cx,cy=cen3[i]-pad
    if 5000<st3[i,4]<20000 and cx<260 and (cy<250 or cy>350):
        reg=(lab3==i).astype(np.uint8)[pad:-pad,pad:-pad]
        cc,_=cv2.findContours(reg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cc,key=cv2.contourArea)
        print("Jackson loop at",round(cx),round(cy),"area px",st3[i,4],"m2 chain",round(st3[i,4]*m_per_jpx**2))
print("---- compare loops in Jackson px")
loops=json.load(open('corbett_loops.json'))
def desc(c):
    (cx,cy),(w,h),ang=cv2.minAreaRect(c.astype(np.float32)); M=cv2.moments(c.astype(np.float32)); x,y,bw,bh=cv2.boundingRect(c.astype(np.float32))
    return dict(minrect=sorted([round(w),round(h)],reverse=True),area=round(cv2.contourArea(c.astype(np.float32))),cen=(round(M['m10']/M['m00']),round(M['m01']/M['m00'])),bbox=(x,y,bw,bh))
for nm in ("L_N","L_S"):
    qq=tf(np.array(loops[nm]['pts'],float),c0,*r.x); print("Corbett",nm,desc(qq))
for i in range(1,n3):
    cx,cy=cen3[i]-pad
    if 5000<st3[i,4]<20000 and cx<260 and (cy<250 or cy>350):
        reg=(lab3==i).astype(np.uint8)[pad:-pad,pad:-pad]
        cc,_=cv2.findContours(reg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE); c=max(cc,key=cv2.contourArea)[:,0,:]
        print("Jackson",desc(c))

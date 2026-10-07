import numpy as np, cv2, json
from PIL import Image
ROOT=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\shapes\narrowneck-gold-coast"
OV=ROOT+r"\overlays"
import os; os.makedirs(OV,exist_ok=True)
polys=json.load(open('polys_v2.json')); ext=json.load(open('extras_v2.json'))
reef=['north_arm','south_arm','wing_patch_NW_a','wing_patch_NW_b','weir_1','weir_2_faint','weir_3_faint']
def render(img,out,box,S,stretch,title,pl=None,extras=True,gridstep=50,legend=True,pct=None):
    im=np.asarray(Image.open(ROOT+img).convert('RGB')).astype(float)
    x0,y0,x1,y1=box
    sub=im[y0:y1,x0:x1]
    if pct:
        lo,hi=np.percentile(sub,pct[0]),np.percentile(sub,pct[1])
    else: lo,hi=stretch
    sub=np.clip((sub-lo)/(hi-lo),0,1)**0.85*255
    v=cv2.resize(sub.astype(np.uint8),None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
    col={'north_arm':(255,60,60),'south_arm':(255,200,0),'wing_patch_NW_a':(60,255,60),'wing_patch_NW_b':(255,0,255),'weir_1':(0,255,255),'weir_2_faint':(255,128,0),'weir_3_faint':(255,128,0)}
    for k in (pl or reef):
        a=((np.array(polys[k],float)-[x0,y0])*S).astype(np.int32)
        cv2.polylines(v,[a],True,col[k],2,cv2.LINE_AA)
    if extras:
        for k,p in ext.items():
            a=((np.array(p,float)-[x0,y0])*S).astype(np.int32)
            cv2.polylines(v,[a],True,(190,190,190),1,cv2.LINE_AA)
    # scale bar 20 m (=75.85 px)
    L=int(round(20/0.263665*S)); bx,by=15,v.shape[0]-25
    cv2.line(v,(bx,by),(bx+L,by),(255,255,255),4); cv2.putText(v,'20 m (= one container length)',(bx+L+8,by+5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
    # north arrow
    cv2.arrowedLine(v,(v.shape[1]-40,60),(v.shape[1]-40,20),(255,255,255),2,tipLength=0.3); cv2.putText(v,'N',(v.shape[1]-48,78),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)
    cv2.putText(v,title,(10,22),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2,cv2.LINE_AA)
    for gx in range((x0//gridstep+1)*gridstep,x1,gridstep):
        X=int((gx-x0)*S); cv2.line(v,(X,v.shape[0]-60),(X,v.shape[0]-50),(255,255,255),1); cv2.putText(v,str(gx),(X-12,v.shape[0]-38),cv2.FONT_HERSHEY_SIMPLEX,0.35,(255,255,255),1)
    Image.fromarray(v).save(os.path.join(OV,out)); print(out,v.shape)
box=(240,500,900,1020)
render(r"\src\wayback\nn_wayback_2020-08-08_r9812_z19.png",'s3_primary_trace.png',box,2,(30,100),'s3 Esri Wayback 2020-08-08 z19 (0.2637 m/px) + traced container patches (grey dashed = untraced seaward dark patches)')
render(r"\src\wayback\nn_wayback_2022-11-06_r47963_z19.png",'s4_crosscheck_on_2022-11.png',box,2,(0,0),'s4 Esri Wayback 2022-11-06 tile set + the s3 trace, unchanged (cross-check)',pct=(0.5,80))
render(r"\src\wayback\nn_wayback_2019-06-18_r21485_z19.png",'s5_check_on_2019-06.png',box,2,(0,0),'s5 Esri Wayback 2019-06-18 + the s3 trace, unchanged (position check)',pct=(1,97))
render(r"\src\wayback\nn_wayback_2016-07-01_r23264_z19.png",'s6_pre_renewal_2016-07_with_s3_trace.png',box,2,(0,0),'s6 Esri Wayback 2016-07-01 (pre-renewal) + the s3 trace (context)',pct=(1,97))

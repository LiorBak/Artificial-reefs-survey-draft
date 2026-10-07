import numpy as np, cv2, json, os
from PIL import Image
ROOT=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\shapes\narrowneck-gold-coast"
OV=ROOT+r"\overlays"
reg=json.load(open(ROOT+r"\design_registration_out.json")); T=np.array(reg['fig7_px_to_s3_px_affine']); Tinv=np.linalg.inv(T)
R=reg['ratio_fig7_over_fig6b']
polys=json.load(open(ROOT+r"\trace_s3_out.json"))['polygons_px']
reef=['north_arm','south_arm','wing_patch_NW_a','wing_patch_NW_b','weir_1','weir_2_faint','weir_3_faint']
col={'north_arm':(255,60,60),'south_arm':(255,200,0),'wing_patch_NW_a':(60,255,60),'wing_patch_NW_b':(255,0,255),'weir_1':(0,255,255),'weir_2_faint':(255,128,0),'weir_3_faint':(255,128,0)}
def to7(p): q=Tinv@np.array([p[0],p[1],1.0]); return q[:2]
G=ROOT+r"\src\gov\narrowneck-gold-coast_jackson2012_"
# Fig 7 + trace
f7=np.asarray(Image.open(G+"fig7_overlay_2011-07_aerial_with_design_contours_and_containers_native.jpeg").convert('RGB')).copy()
v=cv2.resize(f7,None,fx=1.5,fy=1.5,interpolation=cv2.INTER_CUBIC)
for k in reef:
    cv2.polylines(v,[(np.array([to7(p) for p in polys[k]])*1.5).astype(np.int32)],True,col[k],2,cv2.LINE_AA)
cv2.putText(v,'Jackson et al. 2012 Fig 7 (July 2011 aerial + 2004 design contours, white) with the 2020 container trace (coloured)',(8,22),cv2.FONT_HERSHEY_SIMPLEX,0.55,(255,255,0),2,cv2.LINE_AA)
L=int(20/0.21*1.5); cv2.line(v,(20,v.shape[0]-25),(20+L,v.shape[0]-25),(255,255,0),4); cv2.putText(v,'20 m at 0.21 m/px (+-10%)',(30+L,v.shape[0]-20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),1,cv2.LINE_AA)
Image.fromarray(v).save(OV+r"\fig7_2011_aerial_design_contours_with_2020_trace.png")
# Fig 6b + trace
f6=np.asarray(Image.open(G+"fig6b_aerial_2011-07_native.jpeg").convert('RGB')).copy()
v=cv2.resize(f6,None,fx=2,fy=2,interpolation=cv2.INTER_CUBIC)
for k in reef:
    pts=[]
    for p in polys[k]:
        x7,y7=to7(p); pts.append([(x7-83.0)/R,(y7+43.0)/R])
    cv2.polylines(v,[(np.array(pts)*2).astype(np.int32)],True,col[k],2,cv2.LINE_AA)
cv2.putText(v,'Jackson et al. 2012 Fig 6b (July 2011 aerial) + 2020 container trace (coloured)',(8,22),cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0),2,cv2.LINE_AA)
L=int(20/0.3675*2); cv2.line(v,(20,v.shape[0]-25),(20+L,v.shape[0]-25),(255,255,0),4); cv2.putText(v,'20 m at 0.37 m/px (+-10%)',(30+L,v.shape[0]-20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),1,cv2.LINE_AA)
Image.fromarray(v).save(OV+r"\fig6b_2011_aerial_with_2020_trace.png")
# design lines on s3
white=((f7.min(axis=2)>225)*255).astype(np.uint8); white[340:410,900:980]=0
x0,y0,x1,y1=240,500,900,1020; S=2
Z=np.array([[S,0,-x0*S],[0,S,-y0*S],[0,0,1]])
W=cv2.warpAffine(white,(Z@T)[:2],((x1-x0)*S,(y1-y0)*S),flags=cv2.INTER_AREA)
im=np.asarray(Image.open(ROOT+r"\src\wayback\nn_wayback_2020-08-08_r9812_z19.png").convert('RGB')).astype(float)
sub=np.clip((im[y0:y1,x0:x1]-30)/70,0,1)**0.85*255
v=cv2.resize(sub.astype(np.uint8),None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
al=(W.astype(float)/255*0.9)[:,:,None]; v=(v*(1-al)+255*al).astype(np.uint8)
for k,c in (('north_arm',(255,60,60)),('south_arm',(255,200,0))):
    cv2.polylines(v,[((np.array(polys[k],float)-[x0,y0])*S).astype(np.int32)],True,c,2,cv2.LINE_AA)
cv2.putText(v,'s3 Esri 2020-08-08 + design contours of Jackson 2012 Fig 7 (white; 2004 design, PRIOR only) + traced arms (red N, orange S)',(8,22),cv2.FONT_HERSHEY_SIMPLEX,0.55,(255,255,0),2,cv2.LINE_AA)
cv2.putText(v,'placement: registered on 2011 container patches, 0.21 m/px +-10%; arm ends uncertain by about +-15 m',(8,44),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,0),1,cv2.LINE_AA)
L=int(round(20/0.263665*S)); cv2.line(v,(15,v.shape[0]-20),(15+L,v.shape[0]-20),(255,255,255),4); cv2.putText(v,'20 m',(25+L,v.shape[0]-14),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1)
Image.fromarray(v).save(OV+r"\design_prior_fig7_contours_on_s3.png")
# metrics in canonical frame (design white pixels -> s3 px -> frame)
fr=json.load(open('frame.json')); mpp=0.26366503733366337
ys,xs=np.where(white>0); P=(T@np.stack([xs,ys,np.ones_like(xs)]).astype(float))[:2].T
O=np.array(fr['origin_px']); u=np.array(fr['alongshore_dir_px']); n=np.array([-u[1],u[0]])
d=P-O; X=(d@u)*mpp; Y=(d@n)*mpp
sh=json.load(open(ROOT+r"\shape.json"))['canonical']['polygons_m']
e=lambda p:(np.array(p)[:,0].min(),np.array(p)[:,0].max(),np.array(p)[:,1].min(),np.array(p)[:,1].max())
xm=(e(sh[0])[0]+e(sh[1])[1])/2
for nm,sel,pi in (('N',X>xm,0),('S',X<xm,1)):
    print(nm,'design y %.1f..%.1f | traced y %.1f..%.1f | design x %.1f..%.1f traced x %.1f..%.1f'%((Y[sel].min(),Y[sel].max(),e(sh[pi])[2],e(sh[pi])[3],X[sel].min(),X[sel].max(),e(sh[pi])[0],e(sh[pi])[1])))

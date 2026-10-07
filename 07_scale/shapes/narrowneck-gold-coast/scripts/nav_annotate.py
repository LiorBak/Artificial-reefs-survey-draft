import numpy as np, cv2, json, math
from PIL import Image
ROOT="C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/narrowneck-gold-coast"
fr=json.load(open('frame.json')); sh=json.load(open(ROOT+'/shape.json'))
mpp_chart=156543.03392*math.cos(math.radians(-27.986629))/2**18   # m per CSS px at z18
print('chart m/px',mpp_chart)
P=sh['canonical']['polygons_m']
# canonical (x alongshore, y offshore) -> east/north metres relative to the reef centroid, then to clip px (centre = reef centroid)
cen=json.load(open('frame.json'))['centroid_px']
O=np.array(fr['origin_px']); u=np.array(fr['alongshore_dir_px']); n=np.array([-u[1],u[0]]); mpp=0.26366503733366337
cen_xy=np.array([((np.array(cen)-O)@u)*mpp,((np.array(cen)-O)@n)*mpp])
b=math.radians(fr['bearing_north_heading_deg'])
ex=np.array([math.sin(b),math.cos(b)]); ey=np.array([math.sin(b+math.pi/2),math.cos(b+math.pi/2)])   # (E,N) of +x, +y
def to_clip(p,cx=491,cy=327):
    d=np.array(p)-cen_xy; en=d[0]*ex+d[1]*ey
    return (cx+en[0]/mpp_chart, cy-en[1]/mpp_chart)
for fn,tag in (('sonar_z18_shade00.0.png','shade0'),('sonar_z18_shade05.0.png','shade5')):
    im=np.asarray(Image.open(ROOT+'/src/navionics/'+fn).convert('RGB')).copy()
    S=2; v=cv2.resize(im,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
    for poly,c in zip(P[:2],((255,0,0),(255,140,0))):
        a=(np.array([to_clip(p) for p in poly])*S).astype(np.int32); ov=v.copy(); cv2.fillPoly(ov,[a],c); v=cv2.addWeighted(ov,0.28,v,0.72,0); cv2.polylines(v,[a],True,c,2,cv2.LINE_AA)
    # annotations (read by eye on the 3x zoom)
    def tx(s,xy,col=(0,0,200)): cv2.putText(v,s,(int(xy[0]*S),int(xy[1]*S)),cv2.FONT_HERSHEY_SIMPLEX,0.6,col,2,cv2.LINE_AA)
    tx('N arm: closed 4.0 m contour (+ 4.5 loop)',(300,205)); tx('S arm: closed 4.5 m loop',(300,480)); tx('0.9 = obstruction/crest label',(250,396),(0,120,0)); tx('6 m loop between arms (hole)',(40,340),(120,0,120))
    tx('contours 5.5 and 6 m around the arms; 7, 8, 9, 10 m seaward (0.5 m labels, datum not stated)',(5,625),(0,0,0))
    tx('Garmin Navionics SonarChart, 2026-10-06, NOT FOR NAVIGATION; red/orange = our s3 trace (map centre assumed = reef centroid, +-20 m)',(5,18),(0,0,0))
    Image.fromarray(v).save(ROOT+'/overlays/navionics_sonar_z18_%s_with_trace_and_readings.png'%tag); print(tag,v.shape)

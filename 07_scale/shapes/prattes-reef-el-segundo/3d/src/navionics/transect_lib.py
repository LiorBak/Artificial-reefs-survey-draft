import numpy as np, math, sys
from PIL import Image
def transect(png, z, lat, bearing=245.0, cx=None, cy=None, s0=-260, s1=600, thr=110):
    im=Image.open(png).convert("RGB"); a=np.array(im).astype(int); H,W,_=a.shape
    res=156543.03392*math.cos(math.radians(lat))/2**z
    cx = W/2 if cx is None else cx; cy = H/2 if cy is None else cy
    b=math.radians(bearing); dx,dy=math.sin(b),-math.cos(b)
    pts=[]
    for s in np.arange(s0,s1,0.25):
        x=cx+dx*s; y=cy+dy*s
        xi,yi=int(round(x)),int(round(y))
        if 0<=xi<W and 0<=yi<H:
            p=a[yi,xi]; pts.append((s*res, int(p.max()), tuple(int(v) for v in p)))
    # dark runs (contour lines / text)
    runs=[]; cur=None
    for d,mx,p in pts:
        if mx<thr:
            if cur is None: cur=[d,d]
            else: cur[1]=d
        else:
            if cur is not None: runs.append(cur); cur=None
    if cur: runs.append(cur)
    # merge runs closer than 0.8 m
    m=[]
    for r in runs:
        if m and r[0]-m[-1][1]<0.8: m[-1][1]=r[1]
        else: m.append(r)
    return res, pts, [ (round((r[0]+r[1])/2,1), round(r[1]-r[0]+0.5,1)) for r in m]
if __name__=="__main__":
    res,pts,cr=transect(sys.argv[1], int(sys.argv[2]), float(sys.argv[3]))
    print("m/px",round(res,3)); print(len(cr),"dark crossings"); print(cr)

def green_end(pts):
    """seaward end (m) of the drying (green, 152,200,0) band along a transect; None if absent"""
    g=[d for d,mx,p in pts if abs(p[0]-152)<12 and abs(p[1]-200)<12 and p[2]<40]
    return max(g) if g else None

def profile_from(png, z, lat, cx, cy, bearing=245.0, s0=-300, s1=600):
    res,pts,cr=transect(png,z,lat,bearing,cx,cy,s0,s1)
    ge=green_end(pts)
    pos=[c[0] for c in cr]
    # index 0 = first dark crossing within 3 m of the green end
    k0=None
    if ge is not None:
        for i,p in enumerate(pos):
            if abs(p-ge)<=3.0: k0=i; break
    return res,ge,pos,k0

import numpy as np, pickle, fitz, collections
from shapely.geometry import Polygon, LineString
fit=pickle.load(open('design_fit.pkl','rb'))['fit']
err,refl,s,R,sm,dm=fit
# pdf -> BNG: inverse of dst = s*R*(src-sm)+dm
def pdf2bng(pt):
    src=((np.array(pt)-dm)@np.linalg.inv(s*R).T)+sm
    return src
d=fitz.open(r"C:\Users\lior\AppData\Local\Temp\claude\C--\cd973dbd-a674-4cd5-adf1-ffb4c361545f\scratchpad\borth_verify\dl\plans\9v5090_1020_rev_c1.pdf"); p=d[0]
M=p.rotation_matrix
dr=p.get_drawings()
def path_pts(it,n=8):
    pts=[]
    for s_ in it['items']:
        if s_[0]=='l': 
            a,b=s_[1],s_[2]
            if not pts: pts.append(a)
            pts.append(b)
        elif s_[0]=='c':
            a,c1,c2,b=s_[1:5]
            if not pts: pts.append(a)
            for t in np.linspace(0,1,n+1)[1:]:
                x=(1-t)**3*a.x+3*(1-t)**2*t*c1.x+3*(1-t)*t**2*c2.x+t**3*b.x
                y=(1-t)**3*a.y+3*(1-t)**2*t*c1.y+3*(1-t)*t**2*c2.y+t**3*b.y
                pts.append(fitz.Point(x,y))
        elif s_[0]=='re':
            r=s_[1]; pts+= [r.tl,r.tr,r.br,r.bl,r.tl]
        elif s_[0]=='qu':
            q=s_[1]; pts+=[q.ul,q.ur,q.lr,q.ll,q.ul]
    return [tuple(pt*M) for pt in pts]
out=[]
for it in dr:
    pts=path_pts(it)
    if len(pts)<8: continue
    A=np.array(pts); 
    # region of reefs in rotated page coords: N reef x 1050-1800,y 270-1350 ; S x 480-1000, y 600-1050
    cx,cy=A.mean(0)
    reg=None
    if 1000<cx<1800 and 250<cy<1400: reg='N'
    elif 450<cx<1010 and 550<cy<1050: reg='S'
    if reg is None: continue
    closed=np.hypot(*(A[0]-A[-1]))<0.8
    length=float(np.hypot(*np.diff(A,axis=0).T).sum())
    ext=A.max(0)-A.min(0)
    out.append((reg,len(pts),closed,round(length,1),round(float(ext[0]),1),round(float(ext[1]),1),it.get('fill') is not None,it.get('width'),it.get('color')))
out.sort(key=lambda r:-r[3])
for o in out[:40]: print(o)

print('=========== polygons in BNG')
from shapely.ops import unary_union, polygonize
import json
res={}
for reg,box in (('N',(1000,1800,250,1400)),('S',(450,1010,550,1050))):
    lines=[]
    for it in dr:
        pts=path_pts(it)
        if len(pts)<15 or it.get('fill') is not None: continue
        A=np.array(pts); cx,cy=A.mean(0)
        if not (box[0]<cx<box[1] and box[2]<cy<box[3]): continue
        ext=A.max(0)-A.min(0)
        if max(ext)<100: continue
        lines.append(LineString([tuple(pdf2bng(q)) for q in pts]))
    print(reg,'lines',len(lines),[round(l.length,1) for l in lines])
    mls=unary_union(lines)
    polys=list(polygonize(mls))
    polys.sort(key=lambda g:-g.area)
    res[reg]=polys
    for g in polys[:12]:
        mrr=g.minimum_rotated_rectangle; 
        print(' poly area %.0f m2 perim %.0f bounds %s'%(g.area,g.length,[round(v) for v in g.bounds]))
pickle.dump({k:[list(g.exterior.coords) for g in v[:8]] for k,v in res.items()},open('design_polys.pkl','wb'))

print('=========== rings')
rings={}
# N rings: closed paths
Nl=[]
for it in dr:
    pts=path_pts(it)
    if len(pts)<15 or it.get('fill') is not None: continue
    A=np.array(pts); cx,cy=A.mean(0)
    if 1000<cx<1800 and 250<cy<1400 and max(A.max(0)-A.min(0))>100:
        Nl.append(np.array([pdf2bng(q) for q in pts]))
Nl.sort(key=lambda a:-Polygon(a).area)
for a in Nl: 
    g=Polygon(a); print('N ring area %.1f perim %.1f'%(g.area,g.length))
rings['N']=[a.tolist() for a in Nl]
# S rings: pair halves
Sl=[]
for it in dr:
    pts=path_pts(it)
    if len(pts)<15 or it.get('fill') is not None: continue
    A=np.array(pts); cx,cy=A.mean(0)
    if 450<cx<1010 and 550<cy<1050 and max(A.max(0)-A.min(0))>100:
        Sl.append(np.array([pdf2bng(q) for q in pts]))
used=set(); Sr=[]
for i,a in enumerate(Sl):
    if i in used: continue
    # find partner whose endpoints are closest to a's endpoints
    best=None
    for j,b in enumerate(Sl):
        if j==i or j in used: continue
        # distance between a end and b start/end
        for ra in (a,a[::-1]):
            for rb in (b,b[::-1]):
                dd=np.hypot(*(ra[-1]-rb[0]))+np.hypot(*(rb[-1]-ra[0]))
                if best is None or dd<best[0]: best=(dd,j,ra,rb)
    dd,j,ra,rb=best; used|={i,j}
    ring=np.vstack([ra,rb]); Sr.append(ring)
    g=Polygon(ring); print('S ring area %.1f perim %.1f gapsum %.2f valid %s'%(g.area,g.length,dd,g.is_valid))
rings['S']=[a.tolist() for a in Sr]
pickle.dump(rings,open('design_rings.pkl','wb'))

print('=========== S rings by equal length')
groups=collections.defaultdict(list)
for a in Sl: groups[round(float(np.hypot(*np.diff(a,axis=0).T).sum()),1)].append(a)
Sr=[]
for L,g in sorted(groups.items(),reverse=True):
    a,b=g[0],g[1]
    best=None
    for ra in (a,a[::-1]):
        for rb in (b,b[::-1]):
            dd=np.hypot(*(ra[-1]-rb[0]))+np.hypot(*(rb[-1]-ra[0]))
            if best is None or dd<best[0]: best=(dd,ra,rb)
    dd,ra,rb=best; ring=np.vstack([ra,rb]); Sr.append(ring); G=Polygon(ring)
    print('S ring len %.1f area %.1f perim %.1f gap %.2f bounds %s'%(L,G.area,G.length,dd,[round(v) for v in G.bounds]))
rings['S']=[a.tolist() for a in Sr]
pickle.dump(rings,open('design_rings.pkl','wb'))

import sys;import os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import prof,numpy as np,json
# (level, expected hue, hue tol, window min/max dy from previous found line)
spec=[(-1.5,99,14,5,40),(-2,126,14,4,18),(-2.5,148,14,4,18),(-3,168,14,4,18),(-3.5,184,14,4,18),(-4,196,16,4,18),(-4.5,215,16,4,18),(-5,226,14,3,22),(-6,234,14,10,45),(-7,244,16,12,70)]
def one(x):
    pk=prof.peaks(x)
    blk=[p for p in pk if 12<p[0]<65 and p[6]<0.3 and p[7]>100]
    if not blk: return None
    y0=blk[0][0];res={-1:y0};last=y0
    for L,h,tol,lo,hi in spec:
        c=[p for p in pk if last+lo<=p[0]<=last+hi and p[5]>0.4 and abs(p[4]-h)<=tol and p[7]>=35]
        if not c: res[L]=None;continue
        c.sort(key=lambda p:-p[7]);res[L]=c[0][0];last=c[0][0]
    return res
if __name__=='__main__':
    R={}
    for x in range(-160,1,20): R[x]=one(x)
    json.dump({str(k):v for k,v in R.items()},open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','src','levels2_raw.json'),'w'))
    for L in [-1]+[s[0] for s in spec]:
        v=[R[x][L] for x in R if R[x] and R[x].get(L) is not None]
        print(L,len(v),'median %.0f IQR %.0f-%.0f'%(np.median(v),*np.percentile(v,[25,75])) if v else '')

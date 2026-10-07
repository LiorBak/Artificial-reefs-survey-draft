import numpy as np, json, fitz, collections
sop={'R1':(260409.145,289284.522),'R2':(260501.860,289331.154),'R3':(260528.445,289332.669),'R4':(260527.416,289323.700),'R5':(260503.909,289322.361),'R6':(260451.697,289299.380),'R7':(260449.504,289284.783),'R8':(260445.718,289281.518),'R9':(260434.301,289276.451),'R10':(260424.002,289276.269),'R11':(260519.537,289254.981),'R12':(260551.566,289116.844),'R13':(260568.429,289104.990),'R14':(260470.000,289162.000),'R15':(260470.000,289200.000)}
cl=[(1323.5,419.5),(1587.9,945.1),(1596.5,1095.9),(1545.7,1090.1),(1538.1,956.8),(1407.8,660.7),(1325.0,648.4),(1306.5,626.9),(1277.8,562.2),(1276.7,503.8),(1156.0,1045.5),(372.9,1227.0),(305.7,1322.5),(628.9,764.5),(844.4,764.5)]
cl=np.array(cl)
keys=list(sop); B=np.array([sop[k] for k in keys])
# initial similarity from R1,R2,R3 (B->pdf), pdf y down
def fit_sim(src,dst,allow_reflect=True):
    # least squares: dst = s*R*src + t, with optional reflection
    best=None
    for refl in (False,True):
        S=src*np.array([1,-1]) if refl else src
        sm=S.mean(0); dm=dst.mean(0); X=S-sm; Y=dst-dm
        U,sig,Vt=np.linalg.svd(X.T@Y); R=(U@Vt).T
        s=sig.sum()/ (X**2).sum()
        pred=(s*(X@R.T))+dm
        err=np.sqrt(((pred-dst)**2).sum(1)).max()
        if best is None or err<best[0]: best=(err,refl,s,R,sm,dm)
    return best
init=fit_sim(B[[0,1,2]],cl[[0,1,2]])
print('init err',init[0],'refl',init[1],'scale pt/m',init[2])
def predict(fit,pts):
    err,refl,s,R,sm,dm=fit
    S=pts*np.array([1,-1]) if refl else pts
    return s*((S-sm)@R.T)+dm
pred=predict(init,B)
# assign
assign={}
for k,pp in zip(keys,pred):
    j=np.argmin(np.hypot(*(cl-pp).T)); assign[k]=(j,round(float(np.hypot(*(cl[j]-pp))),1))
print(assign)
idx=[assign[k][0] for k in keys]
fit=fit_sim(B,cl[idx])
print('all-points fit: max resid pt',fit[0],'refl',fit[1],'scale pt/m',fit[2],'-> 1:%.1f'%( (1/fit[2])*1000/0.3528 ) if False else '', 'expected 5.669 pt/m')
pr=predict(fit,B); print('resid m',[round(float(np.hypot(*(pr[i]-cl[idx[i]]))/fit[2]),3) for i in range(15)])
import pickle; pickle.dump({'fit':fit,'keys':keys},open('design_fit.pkl','wb'))

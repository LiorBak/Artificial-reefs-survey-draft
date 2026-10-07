import json, math, pickle, numpy as np, tifffile
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
D=r"C:\Users\lior\AppData\Local\Temp\claude\C--\cd973dbd-a674-4cd5-adf1-ffb4c361545f\scratchpad\borth_verify"
base=r"C:\Users\lior\Documents\Gemini\AG\Artificial reef - to upload to git\07_scale\shapes\borth-coastal-defence-reef"
dsm=tifffile.imread(D+r"\dl\wg_dsm_SN6089.tif").astype(float)
lab=np.load(D+r"\lab.npy"); E0,N1=260380,289380
r0=290000-N1; c0=E0-260000
W=dsm[r0:r0+lab.shape[0],c0:c0+lab.shape[1]]
Z=np.where((lab==2)|(lab==3),W,np.nan)
rings=pickle.load(open(D+r"\design_rings.pkl",'rb'))
from pyproj import Transformer
tf=Transformer.from_crs('EPSG:4326','EPSG:27700',always_xy=True)
sh=json.load(open(base+r"\shape.json",encoding='utf-8'))
trN=[tf.transform(lo,la) for la,lo in sh['geo']['polygons_latlon'][0]]
trS=[tf.transform(lo,la) for la,lo in sh['geo']['polygons_latlon'][1]]
ext=[E0,E0+lab.shape[1],N1-lab.shape[0],N1]
fig=plt.figure(figsize=(15,7.2))
ax=fig.add_axes([0.03,0.08,0.50,0.84])
im=ax.imshow(Z,extent=ext,cmap='turbo',vmin=-2.5,vmax=2.0,origin='upper')
ax.set_xlim(260385,260555); ax.set_ylim(289125,289360)
for q,c in ((trN,'white'),(trS,'white')):
    a=np.array(q); ax.plot(a[:,0],a[:,1],c,lw=1.4)
for reg in 'NS':
    a=np.array(rings[reg][4]); ax.plot(a[:,0],a[:,1],'k--',lw=1.0)
ax.contour(np.arange(E0,E0+lab.shape[1])+0.5,np.arange(N1,N1-lab.shape[0],-1)-0.5,np.where(np.isnan(Z),-9,Z),levels=[0.5],colors='k',linewidths=0.8)
ax.set_aspect('equal'); ax.set_xlabel('Easting, OSGB36 / BNG (m)'); ax.set_ylabel('Northing (m)')
ax.set_title('Welsh Government LiDAR DSM, SN6089, flown 2022-03-19 03:15 UTC (sea near LAT)\nheights m (assumed ODN); white = traced rock edge, dashed = design armour foot, black line = +0.5 m contour',fontsize=9)
cb=fig.colorbar(im,ax=ax,fraction=0.035,pad=0.01); cb.set_label('DSM height (m, ODN assumed)')
for t,(e,n) in (('N arm section',(260474,289305)),):
    pass
# section lines
# N arm: PCA axis of LiDAR N comp
ys_,xs_=np.where(lab==2); P=np.column_stack([xs_+E0+0.5,N1-ys_-0.5]); c=P.mean(0)
u,s,vt=np.linalg.svd(P-c,full_matrices=False); axv=vt[0]; 
if axv[0]<0: axv=-axv
nrm=np.array([-axv[1],axv[0]])
tcen=15.0; pt=c+tcen*axv
ax.plot([pt[0]-35*nrm[0],pt[0]+35*nrm[0]],[pt[1]-35*nrm[1],pt[1]+35*nrm[1]],'m-',lw=2); ax.text(pt[0]+36*nrm[0],pt[1]+36*nrm[1],'A-A',color='m',fontsize=10)
ax.plot([260435,260530],[289182,289182],'m-',lw=2); ax.text(260532,289182,'B-B',color='m',fontsize=10)
# profiles
ax2=fig.add_axes([0.60,0.56,0.37,0.36]); ax3=fig.add_axes([0.60,0.09,0.37,0.36])
def band_profile(center,direction,perp,halfband,span):
    # sample cells within |along-offset|<=halfband
    ys,xs=np.where(~np.isnan(Z)); X=xs+E0+0.5; Y=N1-ys-0.5; z=Z[ys,xs]
    rel=np.column_stack([X,Y])-center
    al=rel@direction; cr=rel@perp
    sel=np.abs(al)<=halfband
    bins=np.arange(-span,span+1,2.0); idx=np.digitize(cr[sel],bins)
    xs_c=[];med=[];mx=[]
    for k in range(1,len(bins)):
        m=idx==k
        if m.sum()>=3: xs_c.append((bins[k-1]+bins[k])/2); med.append(np.median(z[sel][m])); mx.append(z[sel][m].max())
    return np.array(xs_c),np.array(med),np.array(mx)
xs1,med1,mx1=band_profile(pt,axv,nrm,5.0,40)
# the section is taken ACROSS the arm: along-section coordinate = nrm; band along axis +-5
def band_across(center,axis_dir,cross_dir,halfband,span):
    ys,xs=np.where(~np.isnan(Z)); X=xs+E0+0.5; Y=N1-ys-0.5; z=Z[ys,xs]
    rel=np.column_stack([X,Y])-center
    al=rel@axis_dir; cr=rel@cross_dir
    sel=np.abs(al)<=halfband
    bins=np.arange(-span,span+1,2.0); idx=np.digitize(cr[sel],bins)
    out=[]
    for k in range(1,len(bins)):
        m=idx==k
        if m.sum()>=3: out.append(((bins[k-1]+bins[k])/2,np.median(z[sel][m]),np.percentile(z[sel][m],90),z[sel][m].max()))
    return np.array(out)
A=band_across(pt,axv,nrm,5.0,40)
ax2.plot(A[:,0],A[:,1],'b-o',ms=3,label='LiDAR median (10 m band)'); ax2.plot(A[:,0],A[:,2],'c-',lw=1,label='LiDAR 90th pct'); ax2.plot(A[:,0],A[:,3],'r:',lw=1,label='LiDAR max')
# design section: crest +0.5 width 9 m, 1:3 slopes to -2.2, toe berm; seabed -4.0
cw=4.5; sh0=A[np.argmax(A[:,1]),0]+1.0; xs_d=[sh0+v for v in (-cw-8.1-3,-cw-8.1,-cw,cw,cw+8.1,cw+8.1+3)]; zs_d=[-2.2,-2.2,0.5,0.5,-2.2,-2.2]
ax2.plot(xs_d,zs_d,'k--',lw=1.5,label='design (DRG 9V5090/1021, N3-N3): +0.50 crest, 1:3')
ax2.axhline(-4.0,color='brown',lw=1,ls='-.',label='design seabed about -4.0 m'); ax2.axhline(-2.44,color='gray',lw=0.8,ls=':'); ax2.text(-38,-2.38,'LAT -2.44',fontsize=7,color='gray')
ax2.axhline(2.56,color='teal',lw=0.8,ls=':'); ax2.text(-38,2.62,'MHWS +2.56',fontsize=7,color='teal'); ax2.axhline(-1.74,color='teal',lw=0.8,ls=':'); ax2.text(-38,-1.68,'MLWS -1.74',fontsize=7,color='teal')
ax2.axhline(0.31,color='green',lw=0.8,ls=':'); ax2.text(-38,0.37,'MSL +0.31 (est.)',fontsize=7,color='green')
ax2.set_xlim(-40,40); ax2.set_ylim(-4.3,3.0); ax2.set_title('Section A-A across the northern arm (mid-arm)',fontsize=9); ax2.set_ylabel('height (m ODN)'); ax2.legend(fontsize=6,loc='lower left')
# S: E-W
Bp=band_across(np.array([260468.0,289182.0]),np.array([0.0,1.0]),np.array([1.0,0.0]),8.0,40)
ax3.plot(Bp[:,0],Bp[:,1],'b-o',ms=3,label='LiDAR median (16 m band)'); ax3.plot(Bp[:,0],Bp[:,2],'c-',lw=1,label='LiDAR 90th pct'); ax3.plot(Bp[:,0],Bp[:,3],'r:',lw=1,label='LiDAR max')
cw=3.0; sh1=Bp[np.argmax(Bp[:,1]),0]; xs_d=[sh1+v for v in (-cw-11.4-3,-cw-11.4,-cw,cw,cw+11.4,cw+11.4+3)]; zs_d=[-2.9,-2.9,1.5,1.5,-2.9,-2.9]
ax3.plot(xs_d,zs_d,'k--',lw=1.5,label='design (DRG 9V5090/1023, S2-S2): +1.50 crest, 1:3')
ax3.axhline(-3.9,color='brown',lw=1,ls='-.',label='design seabed -4.2..-3.6'); ax3.axhline(-2.44,color='gray',lw=0.8,ls=':'); ax3.axhline(2.56,color='teal',lw=0.8,ls=':'); ax3.axhline(-1.74,color='teal',lw=0.8,ls=':'); ax3.axhline(0.31,color='green',lw=0.8,ls=':')
ax3.set_xlim(-40,40); ax3.set_ylim(-4.3,3.0); ax3.set_title('Section B-B across the southern (oval) mound (E-W, mid-length)',fontsize=9); ax3.set_ylabel('height (m ODN)'); ax3.set_xlabel('distance across section (m)'); ax3.legend(fontsize=6,loc='lower left')
fig.text(0.60,0.012,'Contains Welsh Government LiDAR 2020-22 data (OGL). Design lines from Royal Haskoning DRG 9V5090/1021, 1023 rev C1; design centred on the measured crest.',fontsize=6)
fig.savefig(base+r"\overlays\verify_lidar_dsm_2022-03-19_sections.png",dpi=110)
print(A[:,0].min(),A[:,0].max(), 'A crest med max',np.nanmax(A[:,1]),'p90 max',np.nanmax(A[:,2]),'| B crest med',np.nanmax(Bp[:,1]),'p90',np.nanmax(Bp[:,2]))

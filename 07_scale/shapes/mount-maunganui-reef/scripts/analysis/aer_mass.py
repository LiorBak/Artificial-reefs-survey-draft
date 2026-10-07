import numpy as np, json, sys
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from skimage import filters, measure
R='C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/mount-maunganui-reef/'
sys.path.insert(0,R+'scripts')
from geo_tools import *
im=np.array(Image.open(R+'src/linz_aerial_2010-11_BD37_1000_1314_crop.png').convert('RGB')).astype(float)
H,W,_=im.shape
bright=ndi.binary_dilation(im.sum(2)>400,iterations=3)
idx=ndi.distance_transform_edt(bright,return_distances=False,return_indices=True)
imm=np.stack([im[:,:,c][idx[0],idx[1]] for c in range(3)],2)
sm=ndi.gaussian_filter(imm,[6,6,0])      # sigma 6 px = 0.75 m
red=sm[...,0]-0.5*(sm[...,1]+sm[...,2])
win=np.zeros((H,W),bool); win[300:950,250:900]=True
vals=red[win]
t=filters.threshold_otsu(vals)
print('otsu',t,'range',vals.min(),vals.max())
for name,thr in [('otsu',t),('otsu-2',t-2),('otsu+2',t+2)]:
    m=(red>thr)&win
    m=ndi.binary_closing(m,iterations=6); m=ndi.binary_fill_holes(m)
    lab,n=ndi.label(m); sz=ndi.sum(m,lab,range(1,n+1))
    m=np.isin(lab,[i+1 for i,s in enumerate(sz) if s*LZ_PX**2>40])
    ys,xs=np.nonzero(m)
    # canonical dims: use E,N from aerial px
    E=xs*LZ_PX; N=-ys*LZ_PX
    ab=315.98; ob=ab+90
    ux=np.array([np.sin(np.radians(ab)),np.cos(np.radians(ab))]); uy=np.array([np.sin(np.radians(ob)),np.cos(np.radians(ob))])
    X=E*ux[0]+N*ux[1]; Y=E*uy[0]+N*uy[1]
    print(name,thr,'area m2',round(m.sum()*LZ_PX**2),'alongshore',round(X.max()-X.min(),1),'crossshore',round(Y.max()-Y.min(),1),'E-W',round(E.max()-E.min(),1),'N-S',round(N.max()-N.min(),1), 'comps',n)
    np.save(f'aer_mass_{name}.npy',m)
# render overlay for otsu
m=np.load('aer_mass_otsu.npy')
a=np.array(Image.open(R+'src/linz_aerial_2010-11_BD37_1000_1314_crop.png').convert('RGB'))
lo=np.percentile(a,1,axis=(0,1)); hi=np.percentile(a,99.5,axis=(0,1))
b=(((a-lo)/(hi-lo)).clip(0,1)**0.8*255).astype(np.uint8)
e=m&~ndi.binary_erosion(m,iterations=2); b[e]=(255,255,0)
polys=json.load(open(R+'work_polys_fig3_m20_v2.json'))
img=Image.fromarray(b); d=ImageDraw.Draw(img)
for p in polys:
    pts=[tuple(f3_to_lz(x,y)) for x,y in p]; d.line(pts+[pts[0]],fill=(255,255,255),width=2)
img.crop((250,300,900,950)).resize((1000,1000),Image.LANCZOS).save('aer_mass_overlay.png')

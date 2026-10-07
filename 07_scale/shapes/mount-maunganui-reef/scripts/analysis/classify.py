import numpy as np, json
from PIL import Image
from scipy import ndimage as ndi
R='C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/mount-maunganui-reef/'
im=np.array(Image.open(R+'src/boprc_fig3_2013_survey.png').convert('RGB')).astype(float)
seps=[619,634,649,663,678,693,708,723,737,752,767,782,796,811,826,841,855,870,885,900,915,929,944,959,974,988,1003]
cols=[]
for k in range(26):
    y0,y1=seps[k],seps[k+1]; ym=(y0+y1)//2
    patch=im[ym-2:ym+3,66:84].reshape(-1,3)
    cols.append(np.median(patch,axis=0))
cols=np.array(cols)
print(cols.astype(int)[:8])
# depth of each swatch (mid)
depth=np.array([+0.1]+[-(0.2*(k-1)+0.1) for k in range(1,26)])
H,W,_=im.shape
d=np.linalg.norm(im[:,:,None,:]-cols[None,None,:,:],axis=3)
idx=d.argmin(2); dm=d.min(2)
ok=dm<60
dep=depth[idx]
dep[~ok]=np.nan
# restrict to map area: x 80..890, y 70..915 ; exclude legend
m=np.zeros((H,W),bool); m[60:920,60:900]=True
m[600:1010,60:90]=False
valid=ok&m
# inpaint: nearest valid
ind=ndi.distance_transform_edt(~valid,return_distances=False,return_indices=True)
dep_f=dep[ind[0],ind[1]]
np.save('dep.npy',dep_f); np.save('valid.npy',valid)
print(valid.sum(), np.nanmin(dep_f), np.nanmax(dep_f))

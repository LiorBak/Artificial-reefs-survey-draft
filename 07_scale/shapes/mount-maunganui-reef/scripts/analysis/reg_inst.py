import numpy as np, math, json
from PIL import Image
from scipy import ndimage as ndi
from scipy.signal import fftconvolve
R='C:/Users/lior/Documents/Gemini/AG/Artificial reef - to upload to git/07_scale/shapes/mount-maunganui-reef/'
# ---- Fig 3 mask (north-up, 5.45 px/m)
dep3=np.load('dep.npy')
win=np.zeros(dep3.shape,bool); win[330:790,180:720]=True
m3=(dep3>-2.0)&win
m3=ndi.binary_closing(m3,iterations=2); m3=ndi.binary_fill_holes(m3)
lab,n=ndi.label(m3); sizes=ndi.sum(m3,lab,range(1,n+1)); m3=np.isin(lab,[i+1 for i,s in enumerate(sizes) if s>300])
# ---- Installed depth map
im=np.array(Image.open(R+'src/mount-reef-installed.jpg').convert('RGB')).astype(float)
bar=im[103:438,531:543,:].mean(1)   # (335,3)
bar_depth=-1.8-(np.arange(103,438)-113)/58.04
H,W,_=im.shape
d=np.linalg.norm(im[:,:,None,:]-bar[None,None,::2,:],axis=3)
idx=d.argmin(2); dm=d.min(2)
depI=bar_depth[::2][idx]; okI=dm<45
plot=np.zeros((H,W),bool); plot[20:505,30:520]=True   # plot area (inside axes) - refine
okI&=plot
mI_raw=(depI>-3.0)&okI
mI_raw=ndi.binary_opening(mI_raw,iterations=1)
# rotate CW 90 (so that it is north-up)
mI=np.rot90(mI_raw,k=-1)   # np.rot90 k=-1 = clockwise
okR=np.rot90(okI,k=-1)
np.save('mI.npy',mI); np.save('m3.npy',m3)
print('mI',mI.shape,mI.sum(),'m3',m3.shape,m3.sum())
Image.fromarray((mI*255).astype(np.uint8)).save('mI.png'); Image.fromarray((m3*255).astype(np.uint8)).save('m3.png')

import sys;import os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import geo as g,numpy as np,colorsys
from PIL import Image
from scipy.ndimage import map_coordinates,median_filter,gaussian_filter1d
m=np.array(Image.open(os.path.join(g.SRC,'rwr_images','rwr_RHDHV_optionB_contours_plan_2015.jpg')).convert('RGB')).astype(float)
def sample(x,ys):
    pts=np.array([g.xy_to_m2(x,y) for y in ys])
    return np.stack([map_coordinates(m[:,:,c],[pts[:,1],pts[:,0]],order=1) for c in range(3)],1)
ys=np.arange(0,330,0.25)
def peaks(x):
    c=sample(x,ys)
    med=median_filter(c,size=(160,1),mode='nearest')
    dev=np.abs(c-med).sum(1);dev=gaussian_filter1d(dev,3)
    pk=[i for i in range(2,len(ys)-2) if dev[i]>=dev[i-1] and dev[i]>dev[i+1] and dev[i]>22]
    # merge peaks within 4 m
    out=[]
    for i in pk:
        if out and ys[i]-ys[out[-1]]<4: 
            if dev[i]>dev[out[-1]]: out[-1]=i
        else: out.append(i)
    res=[]
    for i in out:
        r,gg,b=c[max(0,i-4):i+5].mean(0)/255
        h,s,v=colorsys.rgb_to_hsv(*c[i]/255)
        res.append((round(float(ys[i]),1),int(c[i][0]),int(c[i][1]),int(c[i][2]),round(h*360),round(s,2),round(v,2),int(dev[i])))
    return res
if __name__=='__main__':
    for x in (-150,-100,-50,0):
        print('x=',x)
        for r in peaks(x):print('  ',r)

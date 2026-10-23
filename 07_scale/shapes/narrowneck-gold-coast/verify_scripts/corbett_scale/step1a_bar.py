import numpy as np
from PIL import Image
R="C:/Users/lior/Documents/Claude/Projects/Artificial reef/07_scale/shapes/narrowneck-gold-coast/"
im=np.asarray(Image.open(R+"src/gov/corbett2023_extracted/p3_x88.png").convert("L")).astype(int)
sub=im[290:318,600:760]
dark=sub<110
rows=dark.sum(axis=1); print("rowsums",[(i+290,int(r)) for i,r in enumerate(rows) if r>0])
# horizontal bar row
r=np.argmax(rows)+290; print("bar row",r)
xs=np.where(im[r,600:760]<110)[0]+600; print("bar x",xs.min(),xs.max())
# tick columns: columns with dark pixels above and below the bar row
for x in range(600,760):
    up=(im[r-9:r-1,x]<110).sum(); 
    if up>=5: print("tick col",x,up, im[r-9:r-1,x].tolist())

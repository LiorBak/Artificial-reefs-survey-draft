import json,math,numpy as np
import os
HERE=os.path.dirname(os.path.abspath(__file__))
SRC3=os.path.join(HERE,'..','src');SRC=os.path.join(HERE,'..','..','src')
G=json.load(open(os.path.join(SRC3,'esri_wayback13192_2025-01-16_z18_wide1200m.png.geo.json')))
b=G['bounds'];W=G['width'];H=G['height']
def _my(lat): return math.log(math.tan(math.pi/4+math.radians(lat)/2))
def px2ll(x,y):
    lon=b['west']+(x/W)*(b['east']-b['west'])
    my0,my1=_my(b['north']),_my(b['south']);my=my0+(y/H)*(my1-my0)
    lat=math.degrees(2*math.atan(math.exp(my))-math.pi/2);return lat,lon
def ll2px(lat,lon):
    x=(lon-b['west'])/(b['east']-b['west'])*W
    my0,my1=_my(b['north']),_my(b['south']);y=(_my(lat)-my0)/(my1-my0)*H;return x,y
LAT0,LON0=-35.0172584,117.919428;BETA=30.26
R=6378137.0
def ll2en(lat,lon):
    return ((lon-LON0)*math.pi/180*R*math.cos(math.radians(LAT0)),(lat-LAT0)*math.pi/180*R)
def en2ll(e,n):
    return LAT0+n/R*180/math.pi, LON0+e/(R*math.cos(math.radians(LAT0)))*180/math.pi
ual=np.array([math.sin(math.radians(BETA)),math.cos(math.radians(BETA))]);uof=np.array([math.sin(math.radians(BETA+90)),math.cos(math.radians(BETA+90))])
def en2xy(e,n): v=np.array([e,n]);return float(v@ual),float(v@uof)
def xy2en(x,y): v=x*ual+y*uof;return float(v[0]),float(v[1])
# model2 -> esri wide px similarity
A=5.230668224444005;Bc=-0.00827138411275753;TX=272.1592861795458;TY=-243.4599148047424
def m2_to_epx(x,y): return A*x-Bc*y+TX, Bc*x+A*y+TY
def epx_to_m2(u,v):
    d=A*A+Bc*Bc;u-=TX;v-=TY;return (A*u+Bc*v)/d,(-Bc*u+A*v)/d
def m2_to_xy(x,y):
    u,v=m2_to_epx(x,y);la,lo=px2ll(u,v);return en2xy(*ll2en(la,lo))
def xy_to_m2(x,y):
    e,n=xy2en(x,y);la,lo=en2ll(e,n);u,v=ll2px(la,lo);return epx_to_m2(u,v)

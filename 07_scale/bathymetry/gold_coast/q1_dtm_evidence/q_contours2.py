import requests,json
from pyproj import Transformer
H={'User-Agent':'Mozilla/5.0'}
u='https://maps1.goldcoast.qld.gov.au/arcgis/rest/services/Contours/MapServer'
tr=Transformer.from_crs(28356,4326,always_xy=True)
for lid in [8,7]:
    p={'f':'json','where':'ELEVATION<0','returnExtentOnly':'true','returnCountOnly':'false'}
    r=requests.get(u+'/%d/query'%lid,params=p,headers=H,timeout=90).json()
    print(lid,'negative contours extent',r.get('extent'))
    p={'f':'json','where':'ELEVATION<0','returnCountOnly':'true'}
    print(' count',requests.get(u+'/%d/query'%lid,params=p,headers=H,timeout=90).json())
# negative contours in offshore halves: x > 543500 (east of Seaway longitude) 
for lid in [8,7]:
  for name,(x0,y0,x1,y1) in {'east_of_x543500':(543500,6871999,556000,6938000),'east_of_x546000_Palm':(546000,6880000,556000,6895000)}.items():
    p={'f':'json','where':'ELEVATION<0','geometry':json.dumps({'xmin':x0,'ymin':y0,'xmax':x1,'ymax':y1,'spatialReference':{'wkid':28356}}),'geometryType':'esriGeometryEnvelope','spatialRel':'esriSpatialRelIntersects','returnCountOnly':'true'}
    print(lid,name,requests.get(u+'/%d/query'%lid,params=p,headers=H,timeout=90).json())
# elevation distribution of the 1 m contour nearest to the surf zone: 0 contour geometry length in window

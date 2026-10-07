import requests,json
H={'User-Agent':'Mozilla/5.0'}
u='https://maps1.goldcoast.qld.gov.au/arcgis/rest/services/Contours/MapServer'
wins={'PalmBeach_reef_window_1.5km':(545000,6889800,547800,6892000),'Narrowneck_window':(541500,6903000,544300,6905400),'whole_extent':(515999,6871999,556000,6938000),'Seaway_to_Palm_offshore_strip':(544000,6884000,556000,6910000)}
stats=json.dumps([{'statisticType':'min','onStatisticField':'ELEVATION','outStatisticFieldName':'zmin'},{'statisticType':'max','onStatisticField':'ELEVATION','outStatisticFieldName':'zmax'},{'statisticType':'count','onStatisticField':'ELEVATION','outStatisticFieldName':'n'}])
for lid in [8,7,2,1]:
  for k,(x0,y0,x1,y1) in wins.items():
    p={'f':'json','where':'1=1','geometry':json.dumps({'xmin':x0,'ymin':y0,'xmax':x1,'ymax':y1,'spatialReference':{'wkid':28356}}),'geometryType':'esriGeometryEnvelope','spatialRel':'esriSpatialRelIntersects','outStatistics':stats}
    r=requests.get(u+'/%d/query'%lid,params=p,headers=H,timeout=90).json()
    print(lid,k,r.get('features',r))

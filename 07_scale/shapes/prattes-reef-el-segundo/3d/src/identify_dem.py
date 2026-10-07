import json,sys,urllib.request,urllib.parse
def ident(lon,lat):
    g=json.dumps({"x":lon,"y":lat})
    q=urllib.parse.urlencode({"geometry":g,"geometryType":"esriGeometryPoint","returnGeometry":"false","returnCatalogItems":"true","f":"json"})
    u="https://gis.ngdc.noaa.gov/arcgis/rest/services/DEM_mosaics/DEM_all/ImageServer/identify?"+q
    d=json.load(urllib.request.urlopen(u,timeout=40))
    vals=d['properties']['Values']; feats=d['catalogItems']['features']
    return d['value'],[(f['attributes']['Name'],f['attributes']['CellsizeArcseconds'],f['attributes'].get('VerticalDatum'),f['attributes'].get('DateCompleted'),v) for f,v in zip(feats,vals)]
if __name__=="__main__":
    lon,lat=float(sys.argv[1]),float(sys.argv[2])
    v,items=ident(lon,lat); print(v)
    for i in items: print(i)

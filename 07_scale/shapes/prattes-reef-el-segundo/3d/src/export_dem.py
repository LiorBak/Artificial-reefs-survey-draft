import json,sys,urllib.request,urllib.parse
def export(oid,west,south,east,north,cell_deg,out):
    w=round((east-west)/cell_deg); h=round((north-south)/cell_deg)
    mr=json.dumps({"mosaicMethod":"esriMosaicLockRaster","lockRasterIds":[oid],"ascending":True,"mosaicOperation":"MT_FIRST"})
    q=urllib.parse.urlencode({"bbox":f"{west},{south},{east},{north}","bboxSR":4326,"imageSR":4326,"size":f"{w},{h}","format":"tiff","pixelType":"F32","interpolation":"RSP_NearestNeighbor","mosaicRule":mr,"noData":"-9999","f":"image"})
    u="https://gis.ngdc.noaa.gov/arcgis/rest/services/DEM_mosaics/DEM_all/ImageServer/exportImage?"+q
    data=urllib.request.urlopen(u,timeout=120).read()
    open(out,'wb').write(data); return w,h,len(data)
if __name__=="__main__":
    oid=int(sys.argv[1]); 
    cell=float(sys.argv[2])
    print(export(oid,-118.445,33.905,-118.420,33.925,cell,sys.argv[3]))

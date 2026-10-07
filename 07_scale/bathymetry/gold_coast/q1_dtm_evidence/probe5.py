import pyogrio,os,json
from pyogrio.raw import read
g=os.path.abspath('meta/DTM_Metadata.gdb').replace(chr(92),'/')
meta,fids,geom,fields=read(g+'/a000001d7.gdbtable',read_geometry=False,return_fids=True)
cols=list(meta['fields'])
rows=[[str(x[i]) for x in fields] for i in range(len(fields[0]))]
json.dump({'cols':cols,'rows':rows},open('vat.json','w'))
for r in rows[60:]:
    print(r[0],r[1].split('.')[0],'|',r[2],'|',r[3],'|',r[4],'|',r[5][:10],'|',r[6][:70],'|',r[7][:90])

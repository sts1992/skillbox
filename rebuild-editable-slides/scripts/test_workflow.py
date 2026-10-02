#!/usr/bin/env python3
"""Reproducible local smoke tests; needs the supplied artifact-tool runtime."""
import json,os,pathlib,subprocess,tempfile,zipfile
S=pathlib.Path(__file__).resolve().parent
node=os.environ['CODEX_PRIMARY_RUNTIME_NODE']
base={'schemaVersion':1,'units':'px','slides':[{'width':960,'height':540,'reviewed':True,'elements':[{'id':'t','type':'text','x':40,'y':30,'w':800,'h':70,'text':'Editable smoke test','font':'Arial','fontSize':32},{'id':'grid','type':'table','x':40,'y':140,'w':400,'h':180,'values':[['Item','Count'],['A','4']],'font':'Arial','fontSize':20,'stroke':'#557799'},{'id':'ch','type':'chart','x':480,'y':140,'w':420,'h':280,'title':'Exact fixture values','categories':['A','B'],'series':[{'name':'Count','values':[4,6]}],'font':'Arial','dataVerified':True,'dataSource':'Synthetic test constants 4 and 6'}]}]}
with tempfile.TemporaryDirectory(prefix='editable-slide-test-') as d:
 d=pathlib.Path(d)
 def run(doc,name,ok=True):
  src=d/(name+'.json');src.write_text(json.dumps(doc));out=d/(name+'.pptx')
  p=subprocess.run([node,str(S/'build_pptx.mjs'),str(src),str(out)],capture_output=True,text=True)
  if (p.returncode==0)!=ok:raise AssertionError(name+' unexpected result: '+p.stderr[-3000:])
  return out
 out=run(base,'native')
 subprocess.run(['python3',str(S/'inspect_editability.py'),str(out),'--require-text','Editable smoke test','--require-table','--require-chart','--reject-full-slide-images'],check=True,stdout=subprocess.DEVNULL)
 with zipfile.ZipFile(out) as z:
  xml=z.read('ppt/slides/slide1.xml').decode();assert '557799' in xml,'Table border color not serialized'
 for name,change in [('unreviewed',lambda s:s.update(reviewed=False)),('unknown',lambda s:s['elements'].append({'type':'unknown','x':1,'y':1,'w':2,'h':2})),('full_slide_image',lambda s:s['elements'].append({'type':'image','x':0,'y':0,'w':960,'h':540,'path':'missing.png','rasterReason':'test'})),('unverified_chart',lambda s:s['elements'][-1].update(dataVerified=False))]:
  doc=json.loads(json.dumps(base));change(doc['slides'][0]);run(doc,name,False)
 print('PASS: native text/table/chart, serialized table border, and rejection of unreviewed/unsupported/full-slide-raster/unverified-chart inputs')

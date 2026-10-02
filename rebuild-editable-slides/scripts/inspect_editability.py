#!/usr/bin/env python3
"""Independently inspect OOXML types, text and media coverage without relying on a preview."""
import argparse,json,re,zipfile,xml.etree.ElementTree as E
N={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
a=argparse.ArgumentParser();a.add_argument('pptx');a.add_argument('--require-text',action='append',default=[]);a.add_argument('--require-table',action='store_true');a.add_argument('--require-chart',action='store_true');a.add_argument('--reject-full-slide-images',action='store_true');args=a.parse_args()
with zipfile.ZipFile(args.pptx) as z:
 p=E.fromstring(z.read('ppt/presentation.xml'));sz=p.find('p:sldSz',N);area=int(sz.get('cx'))*int(sz.get('cy'))
 report=[]
 for name in sorted([n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)],key=lambda s:int(re.search(r'(\d+)\.xml$',s).group(1))):
  root=E.fromstring(z.read(name));text=[t.text or '' for t in root.findall('.//a:t',N)];ratios=[]
  for pic in root.findall('.//p:pic',N):
   x=pic.find('.//a:xfrm/a:ext',N)
   if x is not None:ratios.append(round(int(x.get('cx'))*int(x.get('cy'))/area,4))
  report.append({'slide':name,'native_shapes':len(root.findall('.//p:sp',N)),'text_runs':len(text),'native_tables':len(root.findall('.//a:tbl',N)),'native_charts':len(root.findall('.//c:chart',N)),'native_connectors':len(root.findall('.//p:cxnSp',N)),'pictures':len(ratios),'largest_picture_area_ratio':max(ratios,default=0),'text':text})
 joined='\n'.join(t for s in report for t in s['text'])
 for text in args.require_text:
  if text not in joined:raise SystemExit('Missing expected editable text: '+text)
 if args.require_table and not any(s['native_tables'] for s in report):raise SystemExit('Missing native table')
 if args.require_chart and not any(s['native_charts'] for s in report):raise SystemExit('Missing native chart')
 if args.reject_full_slide_images and any(s['largest_picture_area_ratio']>.8 for s in report):raise SystemExit('Full-slide raster detected')
 print(json.dumps(report,ensure_ascii=False,indent=2))

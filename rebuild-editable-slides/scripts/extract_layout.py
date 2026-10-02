#!/usr/bin/env python3
"""Local PDF/PNG/JPEG evidence extraction; produces a review-required draft, never a final deck."""
import argparse, csv, hashlib, io, json, pathlib, shutil, subprocess, sys
from collections import defaultdict
from PIL import Image, ImageOps


def color(value, default='#000000'):
    if value is None: return default
    try:
        if isinstance(value, (int, float)): value = [value]
        if len(value) == 1: rgb = list(value) * 3
        elif len(value) == 3: rgb = value
        elif len(value) == 4:
            c,m,y,k = value; rgb = [(1-c)*(1-k), (1-m)*(1-k), (1-y)*(1-k)]
        else: return default
        return '#' + ''.join(f'{round(max(0,min(1,v))*255):02X}' for v in rgb)
    except (ValueError, TypeError): return default


def box(o, scale=1):
    return {k:round(v*scale,3) for k,v in {'x':o['x0'],'y':o['top'],'w':o['x1']-o['x0'],'h':o['bottom']-o['top']}.items()}


def ocr_image(file, slide, out, args):
    if not shutil.which('tesseract'): raise SystemExit('Missing tesseract; use agent visual transcription or install approved OCR locally.')
    langs = subprocess.run(['tesseract','--list-langs'],capture_output=True,text=True,check=True).stdout.splitlines()[1:]
    missing = [x for x in args.lang.split('+') if x not in langs]
    if missing: raise SystemExit('Missing OCR languages: '+', '.join(missing)+'. Install official traineddata or use agent visual transcription; never silently use English.')
    data = subprocess.run(['tesseract',str(file),'stdout','-l',args.lang,'--psm',str(args.psm),'tsv'],capture_output=True,text=True,check=True).stdout
    (out / f"page-{slide['page']:03}-ocr.tsv").write_text(data)
    groups = defaultdict(list)
    for r in csv.DictReader(io.StringIO(data),delimiter='\t'):
        if r['level']=='5' and r['text'].strip(): groups[(r['block_num'],r['par_num'],r['line_num'])].append(r)
    for n,words in enumerate(groups.values(),1):
        x=min(int(w['left']) for w in words); y=min(int(w['top']) for w in words)
        right=max(int(w['left'])+int(w['width']) for w in words); bottom=max(int(w['top'])+int(w['height']) for w in words)
        confidence=min(float(w['conf']) for w in words)/100
        slide['elements'].append({'id':f'ocr-{n}','type':'text','x':x,'y':y,'w':right-x+5,'h':(bottom-y)*1.5,
          'text':' '.join(w['text'] for w in words),'font':'Arial','fontSize':round((bottom-y)*1.15,2),
          'color':'#000000','confidence':round(confidence,3),'review':['OCR text, language spacing, font, color and baseline must be checked']})
    slide['warnings'].append('OCR only detects text. Reconstruct shapes, tables, diagrams and pictures from the source image. Text boxes are rough estimates.')


def extract(args):
    source=pathlib.Path(args.source).resolve(); out=pathlib.Path(args.output).resolve(); out.mkdir(parents=True,exist_ok=True)
    slides=[]
    if source.suffix.lower()=='.pdf':
        import pdfplumber
        if not shutil.which('pdftoppm'): raise SystemExit('Missing pdftoppm (Poppler); cannot render the PDF for required visual review.')
        with pdfplumber.open(source) as pdf:
            pages=list(range(1,len(pdf.pages)+1)) if not args.pages else [int(p) for p in args.pages.split(',')]
            if not pages or any(p<1 or p>len(pdf.pages) for p in pages): raise SystemExit('Invalid page selection')
            for num in pages:
                p=pdf.pages[num-1]; scale=96/72
                prefix=out/f'page-{num:03}'
                subprocess.run(['pdftoppm','-f',str(num),'-l',str(num),'-singlefile','-scale-to-x',str(round(p.width*scale)),'-scale-to-y',str(round(p.height*scale)),'-png',str(source),str(prefix)],check=True,capture_output=True)
                sl={'page':num,'width':round(p.width*scale,3),'height':round(p.height*scale,3),'sourceImage':str(prefix.with_suffix('.png')),'reviewed':False,'background':'#FFFFFF','elements':[],'warnings':[],'tableCandidates':[]}
                if len(p.chars)<5:
                    if args.no_ocr: sl['warnings'].append('Scanned PDF page: no OCR performed. Visually transcribe/reconstruct, or rerender at higher resolution for OCR.')
                    else: ocr_image(prefix.with_suffix('.png'),sl,out,args)
                else:
                    for n,r in enumerate(p.rects,1):
                        b=box(r,scale)
                        if b['w']<=0 or b['h']<=0: continue
                        sl['elements'].append({'id':f'rect-{n}','type':'shape','geometry':'rect',**b,'fill':color(r.get('non_stroking_color')) if r.get('fill') else 'none','stroke':color(r.get('stroking_color')) if r.get('stroke') else 'none','strokeWidth':max(.2,r.get('linewidth',1)*scale),'review':['Check stacking order; PDF transparency and clipping are not retained']})
                    for n,r in enumerate(p.lines,1):
                        pts=r.get('pts',[])
                        if len(pts)>=2:
                            sl['elements'].append({'id':f'line-{n}','type':'line','x1':pts[0][0]*scale,'y1':pts[0][1]*scale,'x2':pts[-1][0]*scale,'y2':pts[-1][1]*scale,'stroke':color(r.get('stroking_color')),'strokeWidth':max(.2,r.get('linewidth',1)*scale)})
                    # Words preserve local style, including different weights/colors within a line.
                    words=p.extract_words(extra_attrs=['fontname','size','non_stroking_color'],keep_blank_chars=False,return_chars=False)
                    for n,w in enumerate(words,1):
                        font=w['fontname'].split('+')[-1]; size=w['size']*scale
                        sl['elements'].append({'id':f'text-{n}','type':'text',**box(w,scale),'text':w['text'],'font':font,'fontSize':size,'bold':any(t in font.lower() for t in ['bold','black','heavy']),'italic':any(t in font.lower() for t in ['italic','oblique']),'color':color(w.get('non_stroking_color')),'extractionMethod':'pdf-text','review':['Verify font availability and combine word boxes into logical editable text where appropriate']})
                    if any(not c.get('upright',True) for c in p.chars): sl['warnings'].append('Rotated or vertical text present; draft positions/rotations need manual reconstruction.')
                    try:
                        for t in p.find_tables():
                            sl['tableCandidates'].append({'bbox':[v*scale for v in t.bbox],'values':t.extract(),'cells':[[v*scale for v in c] for c in t.cells]})
                    except Exception as e: sl['warnings'].append('Table candidate detection failed: '+str(e))
                    if p.curves: sl['warnings'].append(f'{len(p.curves)} curved/vector paths not reconstructed. Inspect and redraw supported geometry or flag explicitly.')
                    for n,im in enumerate(p.images,1):
                        sl['warnings'].append(f"Embedded image {n} at {box(im,scale)} not inserted automatically. Crop original rendered page only if it is a photo/logo/irreducible graphic and disclose as raster.")
                    sl['warnings'].append('PDF drawing order, gradients, clipping, font substitution and mixed styles require visual review. Table candidates are evidence only; promote reliable grids to native tables.')
                slides.append(sl)
    else:
        im=ImageOps.exif_transpose(Image.open(source)).convert('RGB'); dst=out/'page-001.png'; im.save(dst)
        sl={'page':1,'width':im.width,'height':im.height,'sourceImage':str(dst),'reviewed':False,'background':'#FFFFFF','elements':[],'warnings':[],'tableCandidates':[]}
        if not args.no_ocr: ocr_image(dst,sl,out,args)
        else: sl['warnings'].append('No OCR performed; agent must visually transcribe text and reconstruct all elements.')
        slides.append(sl)
    data={'schemaVersion':1,'source':str(source),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'units':'px','slides':slides,'fontMap':{},'reviewSummary':'Unreviewed extraction. Inspect source images, correct text/layout, reconstruct missing elements and set reviewed true only after checking every page.'}
    target=out/'layout.draft.json'; target.write_text(json.dumps(data,ensure_ascii=False,indent=2)); print(target)

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__); a.add_argument('source'); a.add_argument('output'); a.add_argument('--pages',help='Comma-separated 1-based PDF pages'); a.add_argument('--lang',default='eng'); a.add_argument('--psm',default=11,type=int); a.add_argument('--no-ocr',action='store_true'); extract(a.parse_args())

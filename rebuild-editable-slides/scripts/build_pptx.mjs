#!/usr/bin/env node
// Render an agent-reviewed intermediate layout into native PowerPoint objects.
import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const [input,output,...flags]=process.argv.slice(2);
if(!input||!output) throw new Error('Usage: build_pptx.mjs reviewed-layout.json output.pptx [--draft]');
const modules=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
if(!modules || !path.isAbsolute(modules)) throw new Error('Set CODEX_PRIMARY_RUNTIME_NODE_MODULES to the supplied artifact-tool runtime. Do not install an unofficial substitute.');
const req=createRequire(path.join(modules,'resolver.cjs'));
const {Presentation,PresentationFile}=await import(pathToFileURL(req.resolve('@oai/artifact-tool')).href);
const doc=JSON.parse(await fs.readFile(input,'utf8'));
if(doc.schemaVersion!==1||doc.units!=='px'||!doc.slides?.length) throw new Error('Unsupported/empty layout');
const size={width:doc.slides[0].width,height:doc.slides[0].height};
const p=Presentation.create({slideSize:size});
const root=path.dirname(path.resolve(input));const out=path.resolve(output);await fs.mkdir(path.dirname(out),{recursive:true});
const report={draft:flags.includes('--draft'),slides:[],fontMap:doc.fontMap??{},source:doc.source,sourceSha256:doc.sourceSha256};
const numeric=(v)=>typeof v==='number'&&Number.isFinite(v);
for(const [i,s] of doc.slides.entries()){
 if(s.width!==size.width||s.height!==size.height)throw new Error('Mixed page sizes: normalize deliberately or split decks; never distort silently.');
 if(!s.reviewed&&!flags.includes('--draft'))throw new Error(`Page ${s.page??i+1} has not been reviewed. Inspect the source and revise the JSON first; --draft is only for inspection.`);
 const slide=p.slides.add();slide.background.fill=s.background??'#FFFFFF';
 const counts={text:0,shape:0,line:0,table:0,chart:0,image:0};const ids=new Map();
 for(const [j,e] of s.elements.entries()){
  if(e.type!=='line' && !['x','y','w','h'].every(k=>numeric(e[k])) )throw new Error(`Invalid geometry ${e.id}`);
  if(e.type!=='line' && (e.w<=0||e.h<=0))throw new Error(`Nonpositive box ${e.id}`);
  if(!Object.hasOwn(counts,e.type)) throw new Error(`Unsupported element type ${e.type}; cannot silently omit`);
  counts[e.type]++;
  const pos={left:e.x,top:e.y,width:e.w,height:e.h,rotation:e.rotation??0};
  const font=(doc.fontMap??{})[e.font]??e.font??doc.defaultFont??'Arial';
  let obj;
  if(e.type==='text'||e.type==='shape'){
   obj=slide.shapes.add({name:e.id??`element-${j}`,geometry:e.type==='text'?'textbox':e.geometry??'rect',position:pos,fill:e.fill??'none',line:{fill:e.stroke??'none',width:e.strokeWidth??0}});
   if(e.text!==undefined||e.runs){obj.text=e.runs?[e.runs.map(r=>({run:r.text,textStyle:{typeface:(doc.fontMap??{})[r.font]??r.font??font,fontSize:`${r.fontSize??e.fontSize??20}px`,color:r.color??e.color??'#000000',bold:r.bold??false,italic:r.italic??false}}))]:e.text;obj.text.style={typeface:font,fontSize:e.fontSize??20,color:e.color??'#000000',bold:e.bold??false,italic:e.italic??false,alignment:e.align??'left',verticalAlignment:e.verticalAlign??'top',autoFit:'none',wrap:e.wrap?'square':'none',insets:{left:e.padding??0,right:e.padding??0,top:e.padding??0,bottom:e.padding??0}};}
  }else if(e.type==='line'){
   if(!['x1','y1','x2','y2'].every(k=>numeric(e[k])))throw new Error(`Invalid line ${e.id}`);
   obj=slide.shapes.add({name:e.id,geometry:'line',position:{left:Math.min(e.x1,e.x2),top:Math.min(e.y1,e.y2),width:Math.abs(e.x2-e.x1),height:Math.abs(e.y2-e.y1),verticalFlip:(e.x2-e.x1)*(e.y2-e.y1)<0},fill:'none',line:{fill:e.stroke??'#000000',width:e.strokeWidth??1}});
  }else if(e.type==='table'){
   const rows=e.values?.length,cols=e.values?.[0]?.length;
   if(!rows||!cols||e.values.some(r=>r.length!==cols))throw new Error(`Invalid table matrix ${e.id}`);
   obj=slide.tables.add({rows,columns:cols,left:e.x,top:e.y,width:e.w,height:e.h,values:e.values,columnWidths:e.columnWidths});
   obj.styleOptions={headerRow:false,bandedRows:false};
   obj.cells.block({row:0,column:0,rowCount:rows,columnCount:cols}).assign({fill:e.fill??'#FFFFFF',textStyle:{typeface:font,fontSize:e.fontSize??20,color:e.color??'#000000'},margins:{left:e.padding??8,right:e.padding??8,top:e.padding??6,bottom:e.padding??6},anchor:'center'});
   const border={style:'solid',fill:e.stroke??'#333333',width:e.strokeWidth??1};
   obj.borders.assign({outside:border,inside:border});
   for(let r=0;r<rows;r++)for(let c=0;c<cols;c++)obj.cells.block({row:r,column:c,rowCount:1,columnCount:1}).assign({borders:{outside:border}});
   if(e.rowHeights) for(let r=0;r<rows;r++)obj.rows[r].height=e.rowHeights[r];
   for(const c of e.cellStyles??[]){const cell=obj.getCell(c.row,c.column);if(c.fill)cell.fill=c.fill;if(c.color||c.bold!==undefined)cell.text.style={typeface:font,fontSize:e.fontSize??20,color:c.color??e.color??'#000000',bold:c.bold??false};}
   for(const m of e.merges??[])obj.merge(m);
  }else if(e.type==='chart'){
   if(!e.title?.trim())throw new Error(`Chart ${e.id}: this renderer requires a source-backed nonempty title. Untitled charts need a deliberate visual reconstruction or supported renderer adaptation.`);
   if(!e.dataSource||!e.dataVerified)throw new Error(`Chart ${e.id}: exact values and dataSource must be verified. Do not invent chart data.`);
   if(!e.categories?.length||!e.series?.length||e.series.some(r=>r.values?.length!==e.categories.length||r.values.some(v=>!numeric(v))))throw new Error(`Invalid chart data ${e.id}`);
   const style={typeface:font,fontSize:e.fontSize??16,fill:e.color??'#000000'};
   obj=slide.charts.add(e.chartType??'bar',{position:pos,categories:e.categories,series:e.series,hasLegend:e.hasLegend??false,...(e.title?{title:e.title,titlePlacement:'aboveChart'}:{titlePlacement:'none'}),titleTextStyle:style,barOptions:e.barOptions??{direction:'column',grouping:'clustered'},legend:{textStyle:style,...e.legend},xAxis:{textStyle:style,...e.xAxis},yAxis:{textStyle:style,...e.yAxis},dataLabels:{textStyle:style,...e.dataLabels}});
  }else if(e.type==='image'){
   if(!e.rasterReason)throw new Error(`Image ${e.id} must say why it remains raster`);
   if(e.w*e.h/(size.width*size.height)>.8)throw new Error(`Image ${e.id} covers almost the whole slide. Whole-slide screenshots are not editable reconstruction.`);
   const f=path.resolve(root,e.path);const ext=path.extname(f).toLowerCase();
   if(!['.png','.jpg','.jpeg'].includes(ext))throw new Error('Crop images to PNG/JPEG before building');
   obj=slide.images.add({blob:new Uint8Array(await fs.readFile(f)),contentType:ext==='.png'?'image/png':'image/jpeg',position:pos,fit:'contain',alt:e.rasterReason});
  }
  if(e.id)ids.set(e.id,obj);
 }
 for(const c of s.connectors??[]){if(!ids.has(c.from)||!ids.has(c.to))throw new Error('Missing connector endpoint');slide.shapes.connect(ids.get(c.from),ids.get(c.to),{kind:c.kind??'straight',fromSide:c.fromSide??'right',toSide:c.toSide??'left',line:{fill:c.color??'#000000',width:c.width??2},head:c.arrow===false?undefined:{type:'triangle',width:'sm',length:'sm'}});}
 if(s.notes)slide.speakerNotes.textFrame.setText(s.notes);
 report.slides.push({page:s.page??i+1,counts,warnings:s.warnings??[],rasterElements:s.elements.filter(e=>e.type==='image').map(e=>({id:e.id,reason:e.rasterReason})),reviewed:s.reviewed,reviewNotes:s.reviewNotes??''});
}
await(await PresentationFile.exportPptx(p)).save(out);
await fs.writeFile(out+'.reconstruction.json',JSON.stringify(report,null,2));
for(let i=0;i<p.slides.items.length;i++){const slide=p.slides.items[i];const preview=await p.export({slide,format:'png',scale:1});await fs.writeFile(out.replace(/\.pptx$/i,`-slide-${i+1}.png`),new Uint8Array(await preview.arrayBuffer()));}
console.log(JSON.stringify({output:out,report:out+'.reconstruction.json',...report}));

const fs=require('node:fs');
const {pathToFileURL}=require('node:url');
const path=require('node:path');
const canvas=require('@napi-rs/canvas');
const pdfjsEntry=require.resolve('pdfjs-dist/legacy/build/pdf.mjs');
const pdfjsRoot=path.resolve(path.dirname(pdfjsEntry),'../..');
Object.assign(globalThis,{DOMMatrix:canvas.DOMMatrix,ImageData:canvas.ImageData,Path2D:canvas.Path2D});
class CanvasFactory {
 create(width,height){const c=canvas.createCanvas(width,height);return{canvas:c,context:c.getContext('2d')};}
 reset(pair,width,height){pair.canvas.width=width;pair.canvas.height=height;}
 destroy(pair){pair.canvas.width=0;pair.canvas.height=0;pair.canvas=null;pair.context=null;}
}
(async()=>{
 const pdfjs=await import(pathToFileURL(pdfjsEntry).href);
 const filename=process.argv[2]||path.resolve(__dirname,'../docs/examples/career/ontology-chat-plan.pdf');
 const doc=await pdfjs.getDocument({data:new Uint8Array(fs.readFileSync(filename)),CanvasFactory,disableFontFace:true,useSystemFonts:false,standardFontDataUrl:path.join(pdfjsRoot,'standard_fonts')+path.sep}).promise;
 const pageNumber=Number(process.argv[4]||1);
 const page=await doc.getPage(pageNumber);
 const op=await page.getOperatorList();
 const names=Object.fromEntries(Object.entries(pdfjs.OPS).map(([k,v])=>[v,k]));
 let state={mode:0,lineWidth:1,stroke:null,fill:null};const stack=[],runs=[],modes={};
 for(let i=0;i<op.fnArray.length;i++){
  const name=names[op.fnArray[i]],args=op.argsArray[i];
  if(name==='save')stack.push({...state});
  else if(name==='restore')state=stack.pop()||state;
  else if(name==='setTextRenderingMode')state.mode=args[0];
  else if(name==='setLineWidth')state.lineWidth=args[0];
  else if(name==='setStrokeRGBColor'||name==='setStrokeGray'||name==='setStrokeColor')state.stroke=Array.from(args);
  else if(name==='setFillRGBColor'||name==='setFillGray'||name==='setFillColor')state.fill=Array.from(args);
  else if(name==='showText'){
   const text=args[0].map(x=>typeof x==='number'?'':(x.unicode||x)).join('');
   modes[state.mode]=(modes[state.mode]||0)+1;
   if(state.mode!==0)runs.push({text,...state});
  }
 }
 console.log(JSON.stringify({filename,pages:doc.numPages,pageNumber,modes,nonFillRuns:runs},null,2));
 if(process.argv[3]){
  const viewport=page.getViewport({scale:0.69*96/72*2});
  const c=canvas.createCanvas(Math.ceil(viewport.width),Math.ceil(viewport.height));
  await page.render({canvasContext:c.getContext('2d'),canvas:c,viewport}).promise;
  fs.writeFileSync(process.argv[3],c.toBuffer('image/png'));
  console.log('rendered',process.argv[3]);
 }
 await doc.destroy();
})().catch(e=>{console.error(e);process.exitCode=1});

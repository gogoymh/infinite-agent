const fs = require('node:fs');
const assert = require('node:assert/strict');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
const {PDFDocument} = require('pdf-lib');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'docs/examples/career');
const artifacts = path.join(root, '.artifacts');
fs.mkdirSync(artifacts, {recursive:true});
const checkOnly = process.argv.includes('--check-only');
const htmlUrl = pathToFileURL(path.join(output, 'ontology-chat-plan.html')).href;
const pdfPath = path.join(checkOnly ? artifacts : output, 'ontology-chat-plan.pdf');
(async()=>{
  const browser=await chromium.launch({headless:true,...(process.env.CHROME_PATH ? {executablePath:process.env.CHROME_PATH} : {})});
  const page=await browser.newPage({viewport:{width:1000,height:1300},deviceScaleFactor:2});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(htmlUrl);
  await page.evaluate(()=>document.fonts.ready);
  for(let i=0;i<3;i++) await page.locator('.page').nth(i).screenshot({path:path.join(artifacts, `career-page-${i+1}.png`)});
  await page.locator('.architecture svg').screenshot({path:path.join(checkOnly ? artifacts : output, 'ontology-chat-diagram.png'),scale:'device'});
  const textCollisions=await page.evaluate(()=>Array.from(document.querySelectorAll('.architecture svg')).flatMap(g=>{
    const labels=Array.from(g.querySelectorAll('text')).map(t=>({text:t.textContent,b:t.getBBox()})), overlaps=[];
    for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++){
      const a=labels[i],b=labels[j];
      if(Math.min(a.b.x+a.b.width,b.b.x+b.b.width)-Math.max(a.b.x,b.b.x)>1 &&
        Math.min(a.b.y+a.b.height,b.b.y+b.b.height)-Math.max(a.b.y,b.b.y)>1) overlaps.push([a.text,b.text]);
    }
    return overlaps;
  }));
  assert.deepEqual(textCollisions,[],'알고리즘의 텍스트가 겹칩니다');
  const hiddenConnectors=await page.evaluate(()=>{
    const nodes=Array.from(document.querySelectorAll('svg .node')).map(g=>({shape:g.querySelector('rect,polygon'),label:g.querySelector('.node-title').textContent}));
    const findings=[];
    for(const path of document.querySelectorAll('svg path.edge,svg path.loop-edge,svg path.meta-edge')){
      const length=path.getTotalLength();
      for(let at=1;at<length-1;at+=1){
        const p=path.getPointAtLength(at);
        for(const {shape,label} of nodes){
          const inside=[[.7,0],[-.7,0],[0,.7],[0,-.7]].every(([dx,dy])=>shape.isPointInFill(new DOMPoint(p.x+dx,p.y+dy)));
          if(inside){findings.push({path:path.getAttribute('d'),node:label,x:p.x,y:p.y});at=length;break;}
        }
      }
    }
    return findings;
  });
  assert.deepEqual(hiddenConnectors,[],'박스 내부로 연결선이 지나갑니다');
  assert.equal(await page.locator('.architecture svg > rect:not(.region)').count(),0,'연결선을 가리는 캡션 배경이 있습니다');
  const nodeRegistry=await page.locator('.architecture .node').evaluateAll(gs=>gs.map(g=>({id:g.dataset.nodeId,title:g.dataset.nodeTitle,model:g.dataset.model})));
  assert.deepEqual(nodeRegistry.map(n=>n.id),Array.from({length:25},(_,i)=>String(i+1).padStart(2,'0')));
  for(const ref of await page.locator('.mini-node,.flow-node').evaluateAll(gs=>gs.map(g=>({id:g.dataset.refNode,title:g.dataset.refTitle,model:g.dataset.refModel})))){
    const main=nodeRegistry.find(n=>n.id===ref.id);
    assert.ok(main,'1페이지에 없는 박스 참조');
    assert.equal(ref.title,main.title);assert.equal(ref.model,main.model);
  }
  assert.equal(await page.locator('.example .trace-row').count(),25);
  for(const row of await page.locator('.example .trace-row').all()){
    assert.equal(await row.locator('.mini-node').count(),1,'입출력 행에 박스 그림이 없습니다');
    assert.ok((await row.locator('.io-input').innerText()).trim(),'입력값이 없습니다');
    assert.ok((await row.locator('.io-output').innerText()).trim(),'출력값이 없습니다');
  }
  const flowIds=await page.locator('.single-flow .flow-node').evaluateAll(ns=>ns.map(n=>n.dataset.refNode));
  assert.deepEqual(flowIds,['01','23','02','04','06','08','11','12','13','15','16','24','01','23','02','04','06','11','13','24','15','16','17','22','25']);
  assert.equal(await page.locator('.single-flow .flow-control').count(),24,'한 흐름의 박스가 모두 연결되지 않았습니다');
  assert.equal(flowIds.filter(n=>n==='23').length,2,'두 발화의 수신 안내가 모두 필요합니다');
  assert.equal(flowIds.filter(n=>n==='25').length,1,'최종 전송은 한 번이어야 합니다');
  assert.equal(await page.locator('.contracts').count(),0,'함수 인자 표가 남아 있습니다');
  assert.equal(await page.locator('.io-input code,.io-output code').count(),0,'설명문에 코드 형식이 남아 있습니다');
  const prose=await page.locator('.io-input,.io-output,.flow-input,.flow-output').allTextContents();
  assert.ok(!prose.some(t=>/\b(?:state|results|pending|arguments|sufficient|raw)\s*=/.test(t)),'변수 표기가 남아 있습니다');
  await page.emulateMedia({media:'print'});
  const bounds=await page.locator('.page').evaluateAll(pages=>pages.map(p=>({height:p.getBoundingClientRect().height,contentBottom:Math.max(...Array.from(p.children).map(c=>c.getBoundingClientRect().bottom-p.getBoundingClientRect().top)),paddingBottom:parseFloat(getComputedStyle(p).paddingBottom)})));
  for(let i=0;i<bounds.length;i++) assert.ok(bounds[i].contentBottom+bounds[i].paddingBottom<=bounds[i].height+1,`페이지 ${i+1} 내용이 A4를 넘습니다: ${JSON.stringify(bounds[i])}`);
  await page.pdf({path:pdfPath,format:'A4',preferCSSPageSize:true,printBackground:true});
  const pdf=await PDFDocument.load(fs.readFileSync(pdfPath));
  const count=pdf.getPageCount(),sizes=pdf.getPages().map(p=>p.getSize());
  assert.equal(count,3,'A4 세 페이지가 아닙니다');
  for(const size of sizes){assert.ok(Math.abs(size.width-595.28)<2);assert.ok(Math.abs(size.height-841.89)<2);}
  assert.deepEqual(errors,[]);
  await page.emulateMedia({media:'screen'});
  for(const width of [375,794,1000]){
    await page.setViewportSize({width,height:1300});
    const layout=await page.evaluate(()=>({width:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth}));
    assert.equal(layout.width,layout.scrollWidth,'페이지에 가로 넘침이 있습니다');
  }
  const mobile=await browser.newPage({viewport:{width:375,height:1200},deviceScaleFactor:1});
  await mobile.goto(htmlUrl);
  await mobile.evaluate(()=>document.fonts.ready);
  await mobile.screenshot({path:path.join(artifacts, 'career-mobile.png')});
  const report={pageCount:count,sizes,bounds,errors,textCollisions,hiddenConnectors,nodeCount:await page.locator('g.node').count(),flowVisitCount:flowIds.length};
  fs.writeFileSync(path.join(artifacts, 'career-check.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

flow_visits=[
 ('01',['“이 Notion 공고의 직무명과','회사 사업을 알려줘.”와 공고 링크'],['하나의 진행 요청을 만들고','공고와 회사 설명 요구를 기록합니다.'],'최초 발화 접수'),
 ('23',['첫 발화가 접수되었습니다.'],['“요청을 받았어요. 확인할게요.”를','즉시 보내고 조회를 준비합니다.'],'수신 안내 후'),
 ('02',['공고 링크와 Notion이라는 회사명,','함수 설명과 누적 요구를 읽습니다.'],['공고 조회와 회사 조회를 고릅니다.','필요한 함수의 선택 수에는 제한이 없습니다.'],'두 함수 선택'),
 ('04',['선택한 두 조회의 실행 조건을','확인합니다. 회사명이 이미 있습니다.'],['같은 요청에서 두 조회를 준비합니다.','동시 조회 수를 설정값으로 제어합니다.'],'독립 조회 두 개 준비'),
 ('06',['두 함수의 설명과 필요한 값,','첫 발화를 받습니다.'],['공고 URL과 회사명 추출 요청을','한 묶음으로 준비합니다.'],'DB 조회 준비'),
 ('08',['공고와 회사 조회 요청,','등록된 조회 함수 목록을 받습니다.'],['두 조회 모두 기존 함수를 씁니다.','새 SQL은 만들지 않습니다.'],'등록 조회 재사용'),
 ('11',['함수에 필요한 값과','이미 확정된 값을 비교합니다.'],['URL과 회사명이 미확정이므로','12번에 함께 추출을 요청합니다.'],'미확정 값 두 개'),
 ('12',['두 함수의 인자 규칙과','공고 링크, Notion이라는 발화입니다.'],['Function Calling 한 번으로 URL과','회사명 notion을 두 호출에 넣습니다.'],'인자를 확보하면'),
 ('13',['인자가 채워진 공고 조회와','회사 조회를 받습니다.'],['두 조회를 동시에 시작합니다.','응답은 같은 요청에 기록합니다.'],'공고 응답 먼저 도착'),
 ('15',['공고 응답이 먼저 도착했습니다.','회사 응답은 아직 기다립니다.'],['People Operations Generalist와','원문 공고 링크를 누적합니다.'],'응답 한 개 누적'),
 ('16',['두 조회 중 공고 응답만 도착했고','회사 조회는 계속 진행 중입니다.'],['회사 응답을 기다립니다.','아직 최종 답변을 만들지 않습니다.'],'대기 중 추가 발화'),
 ('24',['사용자가 “내 이력서도 함께','보여줘.”라고 추가로 말했습니다.'],['새 발화를 즉시 접수하고','같은 진행 요청에 전달합니다.'],'같은 요청의 01로'),
 ('01',['첫 요구와 추가 발화,','공고 결과와 진행 중인 회사 조회입니다.'],['같은 요청에 이력서 요구를 더합니다.','기존 요구와 조회 결과도 보존합니다.'],'요구 누적 / 버전 갱신'),
 ('23',['추가 발화가 접수되었습니다.'],['“추가 요청도 받았어요.”를','즉시 보냅니다. 수신 안내 두 번째입니다.'],'추가 수신 안내 후'),
 ('02',['누적된 요구와 이미 확보한 공고,','실행 중인 회사 조회를 읽습니다.'],['내 이력서 조회만 추가로 고릅니다.','공고와 회사는 다시 조회하지 않습니다.'],'필요한 추가 조회 선택'),
 ('04',['회사 조회는 실행 중이며','이력서 조회가 새로 필요합니다.'],['남은 병렬 슬롯에 이력서 조회를 준비하고','기존 회사 조회는 계속 유지합니다.'],'추가 조회만 준비'),
 ('06',['본인 이력서 조회의 설명과','현재 사용자 문맥을 받습니다.'],['이력서 조회에 사용자 문맥을 넘깁니다.','발화에서 추출할 인자는 없습니다.'],'DB 외 기존 자료 함수'),
 ('11',['이력서 함수는 모델이 채울 인자가','없고 사용자 문맥이 이미 있습니다.'],['인자 추출 없이 호출을 준비합니다.','12번은 다시 거치지 않습니다.'],'추출 생략 / 바로 실행'),
 ('13',['현재 사용자 이력서 조회를 받습니다.','회사 조회도 계속 진행 중입니다.'],['기존 조회에 이력서 조회를 추가합니다.','결과는 같은 누적 요청에 연결합니다.'],'추가 조회 실행'),
 ('24',['회사 응답과 본인 이력서 조회의','응답이 도착합니다. 도착 순서는 예시입니다.'],['두 응답을 원래 호출에 연결해','같은 요청의 15번에 전달합니다.'],'각 응답을 15로'),
 ('15',['회사 사업 정보와 이력서 조회 결과,','기존 공고 결과를 함께 읽습니다.'],['문서와 협업 도구(SaaS) 사업 정보와','이력서 결과를 공고 결과에 더합니다.'],'세 조회 결과 누적'),
 ('16',['누적 요청에서 시작한 세 조회가','모두 응답했고 추가 발화도 반영됐습니다.'],['세 결과와 두 발화의 요구를 합칩니다.','완료된 상태를 17번에 넘깁니다.'],'모든 진행 응답 도착'),
 ('17',['공고, 회사, 본인 이력서 결과와','처음부터 누적된 요구를 받습니다.'],['누적 요구가 모두 충족됐으므로','최종 답변 생성으로 보냅니다.'],'누적 요구 전체 충족'),
 ('22',['두 발화의 요구와 세 조회 결과를','한 묶음으로 받습니다.'],['Notion 직무와 회사 설명, 이력서 결과를','모두 담은 최종 답변 하나를 만듭니다.'],'초안 생성 후 전송 검사'),
 ('25',['답변 초안과 누적 요청 버전,','진행 호출과 전송 기록을 확인합니다.'],['추가 발화가 없고 미전송이므로','최종 답변을 한 번 전송합니다.','첫 요청과 추가 요청을 함께 답합니다.'],None),
]
flow_colors={'jev':('#d3a4ff','#6200cc'),'llm':('#98efa9','#006a28'),'code':('#f3f6f8','#8796a1'),'data':('#fff','#aab9c5')}
flow_parts=['''<svg viewBox="0 0 780 1000" role="img" aria-labelledby="single-flow-title single-flow-description">
<title id="single-flow-title">발화별 즉시 수신 안내와 누적 조회 후 한 번 최종 답변하는 흐름</title>
<desc id="single-flow-description">첫 발화에 수신 안내를 즉시 보내고 공고와 회사 조회를 시작한다. 대기 중 이력서 추가 요청을 받으면 다시 즉시 수신 안내를 보내고 같은 요청에 이력서 조회만 추가한다. 기존과 추가 조회를 합친 세 결과가 모두 도착하면 두 발화의 누적 요구를 판단한다. LLM이 최종 답변 하나를 만들고 코드가 누적 버전과 전송 기록을 확인해 한 번 보낸다. 공고와 회사는 실제 DB 확인값이다. 발화, 도착 순서와 이력서 조회는 설계 예시이며 본인 이력서가 반환 가능한 상황을 가정한다.</desc>
<defs><marker id="flow-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#263a48"/></marker><marker id="flow-repeat-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#bb4b18"/></marker></defs>
''']
def flow_text(x,y,value,cls='flow-value',size=10.1):
    flow_parts.append(f'<text x="{x}" y="{y}" class="{cls}" style="font-size:{size}px">{escape(value)}</text>')
def flow_path(d,repeat=False,kind='control'):
    flow_parts.append(f'<path class="flow-{kind}{" flow-repeat" if repeat else ""}" d="{d}"/>')
flow_text(8,13,'입력 (Input)','flow-column',12)
flow_text(384,13,'1페이지의 박스','flow-node-heading',12)
flow_text(528,13,'출력 (Output)','flow-column',12)
seen={};y=24
for i,(ident,inputs,outputs,condition) in enumerate(flow_visits):
    n=next(n for n in nodes if n['id']==ident)
    fill,stroke=flow_colors[n['model']]
    h=40 if ident=='25' else 28
    step=h+11
    x=275;w=218;cx=384;mid=y+h/2
    seen[ident]=seen.get(ident,0)+1
    model={'jev':'Jev','llm':'LLM','code':'코드','data':'데이터'}[n['model']]
    tag=f'{ident} / {model}'+(' (다시 방문)' if seen[ident]>1 else '')
    attrs=f'data-ref-node="{ident}" data-ref-title="{escape(n["title"],quote=True)}" data-ref-model="{n["model"]}"'
    flow_parts.append(f'<g class="flow-node" {attrs}>')
    if n['kind']=='decision':
        flow_parts.append(f'<polygon points="{cx},{y} {x+w},{mid} {cx},{y+h} {x},{mid}" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>')
    else:
        flow_parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>')
    flow_text(cx,y+8,tag,'flow-tag',8.2)
    flow_text(cx,y+21,n['title'],'flow-node-label',10.1)
    flow_parts.append('</g>')
    for k,value in enumerate(inputs):flow_text(8,y+9+11.5*k,value,'flow-value flow-input',9.8)
    for k,value in enumerate(outputs):flow_text(528,y+9+11.5*k,value,'flow-value flow-output',9.8)
    flow_path(f'M246 {mid}H275',kind='data')
    flow_path(f'M493 {mid}H520',kind='data')
    if condition:
        flow_path(f'M384 {y+h}V{y+step}',repeat=ident in ('16','24'))
        flow_text(402,y+step-2,condition,'flow-condition',7.8)
    y+=step
flow_parts.append('</svg>')
utterances='''<main class="page utterance-examples">
<header><div class="top"><strong>추가 요청을 누적하는 한 대화</strong><span>기획 v3.1 / 2026.10.30 / 3 of 3</span></div>
<h1>수신 안내는 매번, 최종 답변은 한 번</h1></header>
<section class="flow-case-values"><p><b>최초 발화</b> “이 Notion 공고의 직무명과 회사가 어떤 사업을 하는지 알려줘.”</p>
<p><b>공고 링크</b> <a href="'''+u+'''">'''+u+'''</a></p>
<p><b>대기 중 추가 발화</b> “내 이력서도 함께 보여줘.”</p></section>
<figure class="figure-scroll single-flow">'''+''.join(flow_parts)+'''</figure>
<footer><span>공고와 회사는 실측 DB 값 / 발화, 도착 순서와 이력서 조회는 설계 예시(반환 가능 가정)</span><span>예시 동시 조회 수 2 / 수신 2회 / 최종 1회</span></footer>
</main>'''

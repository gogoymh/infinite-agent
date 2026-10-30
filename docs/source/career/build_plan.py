from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[3]
parts = []
nodes = []

def text(x, y, value, cls='label', size=11):
    parts.append(f'<text x="{x}" y="{y}" class="{cls}" style="font-size:{size}px">{escape(value)}</text>')

def edge(d, label=None, xy=None, kind='edge'):
    parts.append(f'<path class="{kind}" d="{d}"/>')
    if label:
        for i, value in enumerate(label if isinstance(label, list) else [label]):
            text(xy[0], xy[1]+12*i, value, 'loop-label' if kind=='loop-edge' else 'edge-label', 10.5)

def box(x, y, w, h, title, lines=(), model='code', tag=None, size=16):
    ident=f'{len(nodes)+1:02d}'
    tag=re.sub(r'^\d+\s*/\s*','',tag) if tag else None
    nodes.append(dict(id=ident,title=title,model=model,kind='box',tag=tag))
    parts.append(f'<g class="node {model}" data-model="{model}" data-node-id="{ident}" data-node-title="{escape(title,quote=True)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>')
    cx = x+w/2
    if tag:
        text(cx, y+13, f'{ident} / {tag}', 'tag node-number', 10.5)
        text(cx, y+34, title, 'node-title', size)
        baseline = y+52
    else:
        text(cx, y+23, f'{ident}  {title}', 'node-title node-number', size)
        baseline = y+41
    for i, value in enumerate(lines):
        text(cx, baseline+i*15, value, 'node-sub', 10.8)
    parts.append('</g>')

def decision(cx, cy, title, tag='Jev Noul', w=200, h=80, sub=None, size=15):
    ident=f'{len(nodes)+1:02d}'
    tag=re.sub(r'^\d+\s*/\s*','',tag)
    nodes.append(dict(id=ident,title=title,model='jev',kind='decision',tag=tag))
    parts.append(f'<g class="node jev" data-model="jev" data-node-id="{ident}" data-node-title="{escape(title,quote=True)}"><polygon points="{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}"/>')
    text(cx, cy-13 if sub else cy-10, f'{ident} / {tag}', 'tag node-number', 9.8)
    text(cx, cy+7, title, 'node-title', size)
    if sub:
        text(cx, cy+23, sub, 'node-sub', 9.5)
    parts.append('</g>')

parts.append('''<svg viewBox="0 0 780 960" role="img" aria-labelledby="figure-title figure-description">
<title id="figure-title">온톨로지 챗의 누적 조회와 한 번 응답 구조</title>
<desc id="figure-description">첫 발화와 추가 발화마다 즉시 수신 안내를 보낸다. 발화와 조회를 하나의 진행 요청에 누적하고 Jev가 필요한 추가 함수만 선택한다. 인자가 준비된 독립 조회를 병렬 실행하고 변경과 의존 작업은 순서를 지킨다. 함수 선택에는 개수 제한이 없고, 동시 조회 수만 설정 파라미터로 제어한다. 초과 조회는 대기열에 두고 빈 슬롯이 나면 시작한다. 기존 조회와 추가 조회 결과를 같은 요청에 누적한다. 16에서 실행 가능한 대기열 처리와 진행 호출 응답, 추가 발화 반영을 확인한 뒤 17에서 누적 요구 전체의 충족 여부를 판단한다. 미도착 결과가 있으면 대기를 유지하지만 추가 발화는 즉시 수신한다. 새 발화는 진행 작업과 결과를 보존한 채 최신 요구에 통합한다. 22에서 최종 답변을 생성하고 25의 코드가 누적 버전과 전송 기록을 원자적으로 확인해 한 번 전송한다. 답변 생성 중 추가 발화가 오면 새 요구를 처리한 뒤 다시 생성한다. Jev는 선택과 의미 판단, LLM은 인자 추출과 답변 생성, 코드는 즉시 안내와 결과 취합을 맡는다. 구현 전 기획이다.</desc>
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#263a48"/></marker>
<marker id="loop-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#bb4b18"/></marker>
<marker id="meta-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#82919b"/></marker>
</defs>
<rect class="region" x="257" y="209" width="488" height="181" rx="10"/>
''')
# Data completion and new chat messages are independent events.
edge('M135 88V106','수신 즉시',(169,101))
edge('M240 136H275V52H305')
edge('M595 52H555',kind='meta-edge')
edge('M430 88V118','선택 수 제한 없음',(488,106))
edge('M555 150H595','진행 작업 없음 / 확인 필요',(669,109))
edge('M305 167H248V214H130V224','준비된 함수',(278,190))
edge('M305 175H257V661H305',['기존 호출','대기 중'],(280,617),kind='meta-edge')
edge('M230 256H275','DB 조회',(249,242))
edge('M230 277H248V439H305','DB 외 함수',(280,403))
edge('M130 330V311H270V225H360.6',kind='meta-edge')
edge('M485 256H545','신규 조회',(516,247))
edge('M637 286V320')
edge('M637 374V399H505V410','검증 성공',(580,390))
edge('M730 347H751V697H588V618H555','검증 실패 → 상태 기록',(661,426))
edge('M380 294V410','등록 SQL 재사용',(446,343))
edge('M305 433H230','미확정 인자',(267,423))
edge('M230 454H272V530H305','추출 후 검증',(211,516))
edge('M430 470V496','모든 인자 확정',(491,486))
edge('M555 530H595','필요시',(576,519))
edge('M665 568V574H585V595H555')
edge('M430 562V578','호출별 응답',(492,574))
edge('M430 626V636')
edge('M430 686V702','대기와 진행 완료 / 발화 반영',(507,699))
edge('M305 654H241V156H305',kind='loop-edge')
text(273,674,'슬롯 여유','loop-label',8.5)
text(273,686,'대기열 → 04','loop-label',8.5)
edge('M555 661H595')
text(574,655,'대기','edge-label',9)
edge('M595 619H577V611H555',kind='meta-edge')
text(574,607,'조회 응답','edge-label',8)
edge('M665 684V713H757V8H135V18','새 발화 / 장기 완료 → 01',(661,770),kind='meta-edge')
edge('M317 739H270','부족',(294,729))
edge('M543 739H748V895H235V904','누적 요구 충족 → 답변 생성',(647,732))
edge('M30 712H15V172H282V67H305',kind='loop-edge')
edge('M30 756H24V196H430V183',kind='loop-edge')
edge('M270 756H294V812H357','관계 탐색 선택',(323,798))
edge('M503 812H563','예',(533,799))
edge('M430 841V867H350V904','아니오',(390,861))
edge('M727 812H741V844H652V846','예',(706,838))
edge('M645 841V842H550V880H400V904','아니오',(524,868))
edge('M735 866H771V196H573V150H555',kind='loop-edge')
edge('M90 775V904',['입력 부족 / 실패 / 확인 필요','→ 남은 항목과 상태 안내'],(188,824))
edge('M440 929H495')
text(467,924,'생성 완료','edge-label',8.5)
edge('M735 937H778V3H135V18','답변 생성 중 추가 발화 → 01',(669,754),kind='loop-edge')
edge('M670 183V202H744V894H620V904')

box(30,18,210,70,'발화와 조회 상태 누적하기',['첫 발화와 추가 발화를 같은 요청에','요청 ID 유지 / 요구와 결과를 누적'],size=15)
box(305,16,250,72,'여러 함수 선택',['목록 내 필요한 함수를 개수 제한 없이 선택'],'jev','Jev Noul 배치',18)
box(595,18,150,60,'함수 설명서',['역할, 인자 규칙, 실행 조건'],'data',size=15)
box(305,118,250,65,'실행 순서 정하기',['선택 함수는 대기열에 / 동시 수는 설정값','의존 작업과 변경 작업은 순서 유지'],size=18)
box(595,118,150,65,'답변 / 확인 질문',['실행 없음 / 입력 확인'],'llm','LLM',14)
box(30,224,200,72,'모델에 보낼 입력 묶기',['선택 함수 설명, 인자 규칙, 발화','이미 확보한 값도 함께 전달'],size=15)
box(30,330,200,65,'DB와 조회 함수 목록',['테이블 뜻, 관계와 연결키','재사용할 SQL, 인자 규칙, 버전'],'data',size=15)
decision(380,256,'테이블 / SQL 함수 선택','Jev Choice',210,76,size=14.5)
box(545,224,185,62,'새 SQL + 인자 생성',['SQL, 인자 정의와 값을 함께 생성'],'llm','LLM Function Calling',16)
box(545,320,185,54,'SQL과 인자 검사하기',['조회 전용, 인자 타입 확인 후 등록'],size=15)
box(305,410,250,60,'확보한 값 넣기',['DB 결과, 저장값 → 함수 인자','없는 값만 12번에 추출 요청'],size=16)
box(30,410,200,66,'인자 일괄 추출',['선택 함수의 미확정 값을 한 요청에'],'llm','LLM Function Calling',16)
box(305,496,250,66,'요청한 기능 실행하기',['조회는 설정 한도 안에서 병렬 실행','빈 슬롯에 다음 조회 / 변경은 순서 유지'],size=15.5)
box(595,496,140,72,'자료 해석 / 추출',['자료 처리 작업에서','필요한 생성만 호출'],'llm','LLM',14)
box(305,578,250,48,'조회 결과 누적하기',['기존과 추가 조회를 같은 요청에 기록'],size=16)
box(305,636,250,50,'누적 조회 결과 모으기',['대기열 처리 + 진행 응답 + 발화 반영'],size=16)
decision(430,739,'정보가 충분한가?','Jev Noul',226,74,'누적 요구 전체 기준',16)
box(30,687,240,88,'다음 행동 선택',['남은 호출 / 추가 함수 / 관계 탐색','확인 / 복구 / 진행 상태'],'jev','Jev Choice',17)
decision(430,812,'관련 관계가 있나?',w=146,h=58,size=12.5)
decision(645,812,'관계 정보가 필요한가?',w=164,h=58,size=12.2)
box(570,846,165,44,'연결 대상 읽기',['다음 테이블과 연결 조건'],size=15)
box(30,904,410,50,'누적 결과로 최종 답변 생성',['처음 발화와 추가 요청을 모두 포함'],'llm',size=17)
box(30,106,210,60,'발화별 즉시 수신 안내',['첫 발화와 추가 발화마다 즉시 안내','발화별 1회 / LLM 호출 없음'],size=16)
box(595,602,140,82,'추가 발화와 작업 관리',['추가 발화는 01의 같은 요청에','조회 결과는 15에 계속 누적','장기 완료는 후속 이벤트로'],size=11.7)
box(495,904,240,50,'최종 답변 한 번 전송',['누적 버전 확인 / 중복 전송 방지'],size=16)
text(630,219,'DB 조회 / 등록 SQL 우선','region-title',11)
text(155,188,'추가 함수 → 02 재선택','loop-label',10.5)
text(168,208,'대기 함수 준비되면 → 04','loop-label',10.5)
text(663,193,'연결 대상 확인 후 → 04','loop-label',10.5)
parts.append('</svg>')
svg='\n'.join(parts)
assert [n['id'] for n in nodes]==[f'{i:02d}' for i in range(1,26)]

def mini_node(ident,compact=False):
    n=next(n for n in nodes if n['id']==ident)
    colors={'jev':('#d3a4ff','#6200cc'),'llm':('#98efa9','#006a28'),'code':('#f3f6f8','#8796a1'),'data':('#ffffff','#aab9c5')}
    fill,stroke=colors[n['model']]
    model={'jev':'Jev','llm':'LLM','code':'코드','data':'데이터'}[n['model']]
    attrs=f'data-ref-node="{ident}" data-ref-title="{escape(n["title"],quote=True)}" data-ref-model="{n["model"]}"'
    s=f'<svg class="mini-node" viewBox="0 0 190 42" role="img" aria-label="1페이지 {ident} {escape(n["title"],quote=True)}" {attrs}>'
    if n['kind']=='decision':
        s+=f'<polygon points="95,1 188,21 95,41 2,21" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'
        s+=f'<text x="95" y="13" style="font-size:10px;font-weight:750;fill:{stroke}">{ident}</text>'
        s+=f'<text x="95" y="26" style="font-size:10.5px;font-weight:700">{escape(n["title"])}</text>'
    else:
        dash=' stroke-dasharray="3 3"' if n['model']=='data' else ''
        s+=f'<rect x="1" y="1" width="188" height="40" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.3"{dash}/>'
        s+=f'<text x="95" y="12" style="font-size:9px;font-weight:750;fill:{stroke}">{ident} / {model}</text>'
        lines=[n['title']]
        if len(n['title'])>21:
            words=n['title'].split();lines=['']
            for word in words:
                if len(lines[-1]+' '+word)>21: lines.append(word)
                else: lines[-1]=(lines[-1]+' '+word).strip()
        for i,line in enumerate(lines):
            baseline=27 if len(lines)==1 else 25+i*11
            s+=f'<text x="95" y="{baseline}" style="font-size:10.5px;font-weight:700">{escape(line)}</text>'
    if compact and len(n['title'])<=21:
        s=s.replace('viewBox="0 0 190 42"','viewBox="0 0 190 32"')
        s=s.replace('height="40"','height="30"').replace('188,21 95,41 2,21','188,16 95,31 2,16')
        s=s.replace('y="12"','y="10"').replace('y="13"','y="11"').replace('y="27"','y="23"').replace('y="26"','y="22"')
    return s+'</svg>'

def node_refs(ids):
    return '<div class="node-ref-group">'+''.join((('<span class="mini-arrow" aria-hidden="true">→</span>' if i else '')+mini_node(ident)) for i,ident in enumerate(ids))+'</div>'


html='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>온톨로지 챗 | 누적 조회와 한 번 답변</title>
<meta name="description" content="발화별 즉시 안내, 같은 요청의 추가 조회와 결과 누적, 최종 답변 한 번 전송. A4 세 페이지.">
<style>
:root{--ink:#203747;--sub:#546875;--line:#cbd6de;--jev:#6200cc;--jev-bg:#d3a4ff;--llm:#006a28;--llm-bg:#98efa9;--orange:#bb4b18}
*{box-sizing:border-box}body{margin:0;padding:24px;background:#eef1f4;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif;word-break:keep-all;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;min-height:297mm;margin:0 auto 20px;padding:8mm 12mm 7mm;background:#fff;box-shadow:0 8px 32px #24384912}
.top{display:flex;justify-content:space-between;font-size:9px;color:var(--sub);margin-bottom:6px}.top strong{color:var(--orange)}h1{font-size:29px;line-height:1.12;letter-spacing:-.045em;margin:0;font-weight:760}.subtitle{font-size:13px;line-height:1.4;font-weight:650;margin:5px 0}.intro{font-size:10px;line-height:1.55;color:var(--sub);margin:0}
.figure-head{display:flex;justify-content:space-between;align-items:center;border-top:1px solid var(--line);padding-top:6px;margin:8px 0 4px}.figure-head strong{font-size:10.5px}.legend{display:flex;gap:11px;font-size:8.7px;color:var(--sub)}.legend span{display:flex;align-items:center;gap:4px}.swatch{width:9px;height:9px;border-radius:2px;border:1px solid}.swatch.jev{background:var(--jev-bg);border-color:var(--jev)}.swatch.llm{background:var(--llm-bg);border-color:var(--llm)}.swatch.code{background:#f3f6f8;border-color:#8796a1}
figure{margin:0}svg{display:block;width:100%;height:auto}svg text{font-family:inherit;text-anchor:middle;fill:var(--ink);stroke:none;stroke-width:0}.edge,.meta-edge,.loop-edge{fill:none;stroke-linejoin:round;stroke-linecap:round}.edge{stroke:#263a48;stroke-width:1.65;marker-end:url(#arrow)}.meta-edge{stroke:#82919b;stroke-width:1.35;marker-end:url(#meta-arrow)}.loop-edge{stroke:var(--orange);stroke-width:2.15;marker-end:url(#loop-arrow)}.region{fill:#fff;stroke:#c0ccd5;stroke-width:1.1;stroke-dasharray:5 5}.node rect,.node polygon{stroke-width:1.5}.node.code rect{fill:#f3f6f8;stroke:#8796a1}.node.data rect{fill:#fff;stroke:#aab9c5;stroke-dasharray:4 4}.node.jev rect,.node.jev polygon{fill:var(--jev-bg);stroke:var(--jev);stroke-width:1.7}.node.llm rect{fill:var(--llm-bg);stroke:var(--llm);stroke-width:1.6}.node-title{font-weight:700;letter-spacing:-.025em}.node-sub{fill:#506471}.jev .node-sub,.llm .node-sub{fill:var(--ink)}.tag{font-weight:700}.jev .tag{fill:var(--jev)}.llm .tag{fill:var(--llm)}.edge-label{fill:var(--sub)}.loop-label{fill:var(--orange);font-weight:650}.region-title{font-weight:650}
.notes{border-top:1px solid var(--line);padding-top:6px;margin-top:5px;font-size:9px;line-height:1.55;color:var(--sub)}.notes p{margin:0 0 3px}.notes strong{color:var(--ink)}footer{font-size:7.8px;color:var(--sub);line-height:1.5;margin-top:5px;display:flex;justify-content:space-between;gap:10px}
.contracts h1{font-size:25px}.guide{font-size:9.5px;line-height:1.5;margin:6px 0 8px}.guide b{font-weight:750}.j{color:var(--jev)}.l{color:var(--llm)}code{font-family:"SFMono-Regular",Consolas,"Liberation Mono",monospace;font-size:.96em;letter-spacing:-.035em;overflow-wrap:anywhere;word-break:normal}.fn code{font-size:9px;letter-spacing:-.05em;white-space:nowrap}.fn span{font-size:8px;color:#7b8b95;margin-right:5px}.none{color:#7b8b95}footer a{color:var(--sub)}
table{width:100%;border-collapse:collapse;table-layout:fixed;font-size:9.4px;line-height:1.35}col.fn-col{width:27%}col.req-col{width:16%}col.opt-col{width:30%}col.policy-col{width:27%}th{text-align:left;background:#edf2f5;font-size:9.5px;font-weight:700;padding:5px 4px;border-top:1px solid #9eafb9;border-bottom:1px solid #bac7cf}td{vertical-align:top;padding:3.5px 4px;border-bottom:1px solid #dbe2e7}tbody tr:nth-child(even){background:#fafbfc}
.parameter-key{margin-top:7px;font-size:8.7px;line-height:1.45;color:var(--sub);display:grid;grid-template-columns:1fr 1fr;gap:4px 12px}.parameter-key p{margin:0}.parameter-key strong{color:var(--ink)}.conditions{font-size:8.7px;line-height:1.45;margin-top:6px;display:grid;grid-template-columns:1fr 1fr;gap:10px}.conditions p{margin:0 0 3px}.conditions strong{color:var(--ink)}.efficiency{border-top:1px solid #acbdc8;margin-top:6px;padding-top:5px;font-size:9px;line-height:1.5}.efficiency h2{font-size:10px;margin:0 0 3px}.efficiency p{margin:0 0 3px}
.example h1{font-size:25px}.example .intro{margin-top:7px}.utterance{padding:10px 12px;background:#f3f6f8;border:1px solid #c5d0d8;border-radius:6px;margin:12px 0 8px}.utterance h2{font-size:10px;margin:0 0 4px}.utterance blockquote{margin:0;font-size:13px;line-height:1.55;font-weight:650}.input-url{font-size:9px;line-height:1.4;overflow-wrap:anywhere;margin:5px 0 0;color:var(--sub)}.example a{color:#315968}
.steps{list-style:none;padding:0;margin:0}.step{display:grid;grid-template-columns:24px 1fr;gap:8px;border-bottom:1px solid #d6dfe5;padding:8px 0}.step-number{font-size:15px;font-weight:750;color:#748995;line-height:1.2;padding-top:2px}.step h2{font-size:12px;line-height:1.35;margin:0 0 4px;display:flex;align-items:center;gap:7px}.step p{font-size:10.2px;line-height:1.5;margin:0}.step code{font-size:9.4px}.actor{display:inline-block;font-size:8.5px;line-height:1.3;padding:2px 5px;border-radius:3px;border:1px solid #aab9c5;background:#f3f6f8;color:#536a78;font-weight:700}.actor.jev{background:var(--jev-bg);border-color:var(--jev);color:var(--jev)}.actor.llm{background:var(--llm-bg);border-color:var(--llm);color:var(--llm)}.fact{background:#f4f7f9;border-left:2px solid #a0b1bd;padding:6px 9px;margin-top:5px;font-size:9.5px;line-height:1.5}.fact code{font-size:9.2px}.sql{white-space:pre-wrap;margin:5px 0 0;background:#f4f7f9;padding:6px 9px;border-left:2px solid #a0b1bd;font:9.4px/1.4 "SFMono-Regular",Consolas,"Liberation Mono",monospace}.sample-answer{margin:0;padding:7px 9px;background:#e6f9e9;border-left:3px solid var(--llm);font-size:11px;line-height:1.5}.example-notes{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:9px;font-size:9px;line-height:1.5}.example-notes p{margin:0}.example-notes strong{color:var(--ink)}
.step{padding:3px 0}.step-number{font-size:9.5px;padding-top:11px;white-space:nowrap;font-weight:650}.step p{font-size:10px}.step-heading,.utterance-heading{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:4px}.step-heading h2,.utterance-heading h2{margin:0;font-size:11.5px}.node-ref-group{display:flex;align-items:center;gap:5px;flex-wrap:wrap}.mini-node{display:block;width:180px;height:auto;min-width:0;flex-shrink:0}.mini-arrow{font-size:11px;color:#708797;font-weight:650}.utterance{margin-top:9px;margin-bottom:6px;padding:6px 10px}.utterance blockquote{font-size:12px}.fact{padding:4px 8px}.sql{padding:4px 8px}.sample-answer{padding:5px 8px;font-size:10.5px}.trace-note{font-size:8.8px;line-height:1.4;color:var(--sub);margin-top:4px}.utterance .mini-node{width:180px}
.step-heading{margin-bottom:2px}
.io-example .intro{margin-top:5px}.case-values{margin:7px 0 6px;padding:6px 8px;background:#f3f6f8;border:1px solid #c5d0d8;border-radius:5px;font-size:9.2px;line-height:1.4}.case-values p{margin:0 0 2px}.case-values p:last-child{margin-bottom:0}.case-values .case-question{font-size:11px;font-weight:650}.case-values a{overflow-wrap:anywhere}.io-table{font-size:9.2px;line-height:1.3}.io-table col.node-col{width:28%}.io-table col.input-col{width:31%}.io-table col.output-col{width:41%}.io-table th{padding:4px}.io-table td{padding:1.5px 4px}.io-table .io-node-cell{vertical-align:middle}.io-table .mini-node{width:100%;min-width:0}.io-table code.io-value{display:block;font-size:9.1px;line-height:1.3;letter-spacing:-.04em;overflow-wrap:anywhere;white-space:normal}.io-node-wrap{display:flex;align-items:center;gap:4px}.io-node-wrap .mini-node{width:calc(100% - 15px);flex:0 0 calc(100% - 15px)}.io-order{font-size:8px;min-width:11px;color:#748995;font-weight:650}.io-footnotes{margin-top:6px;font-size:8.5px;line-height:1.4;color:var(--sub)}.io-footnotes p{margin:0 0 3px}.io-footnotes strong{color:var(--ink)}
@page{size:A4 portrait;margin:0}@media print{body{padding:0;background:#fff}.page{margin:0;box-shadow:none;min-height:0;height:297mm;break-after:page}.page:last-child{break-after:auto}.figure-scroll,.table-scroll{overflow:visible}svg{min-width:0}tr{break-inside:avoid}}
@media screen and (max-width:840px){body{padding:12px}.page{width:100%;min-height:0;padding:24px}}
@media screen and (max-width:600px){body{padding:0}.page{padding:22px 14px;margin-bottom:14px}.figure-scroll,.table-scroll{overflow-x:auto}svg{min-width:700px}table{min-width:690px}.figure-head{gap:10px;align-items:flex-start}.legend{gap:6px;font-size:8px}.parameter-key,.conditions,.example-notes{grid-template-columns:1fr}.parameter-key,.conditions{font-size:10px}.efficiency{font-size:10px}.step h2{flex-wrap:wrap}.step p{font-size:12px}.fact{font-size:11px}.example-notes{font-size:11px}footer{display:block}.top{font-size:8px}h1{font-size:27px}}
.utterance-examples h1{font-size:26px}.utterance-examples .intro{margin-top:7px}.dialogue-list{margin-top:10px}.dialogue-case{padding:9px 0 10px;border-top:1px solid #cbd6de;break-inside:avoid}.dialogue-case h2{font-size:12.5px;line-height:1.35;margin:0 0 6px}.dialogue-case h2 span{color:#778c99;font-size:10px;margin-right:8px}.dialogue-user,.dialogue-selection,.dialogue-flow,.dialogue-reply{display:grid;grid-template-columns:48px 1fr;gap:8px;align-items:start}.dialogue-case b{font-size:9px;line-height:1.6;color:#647987;font-weight:650}.dialogue-case p{margin:0;font-size:10.5px;line-height:1.5}.dialogue-user{padding:5px 8px;background:#f3f6f8;border-radius:5px}.dialogue-user p{font-size:12px;font-weight:650}.dialogue-selection{margin-top:5px}.dialogue-selection b{color:var(--jev)}.dialogue-selection p{color:var(--jev);font-size:10px;font-weight:650}.dialogue-flow{margin-top:2px}.dialogue-flow p{font-size:9.5px;color:var(--sub)}.dialogue-reply{margin-top:5px;padding:5px 8px;border-left:3px solid var(--llm);background:#e9faec}.dialogue-reply b{color:var(--llm)}.dialogue-reply p{font-size:11px}.dialogue-context{padding-left:64px;margin-top:3px!important;font-size:8.5px!important;line-height:1.35!important;color:var(--sub);overflow-wrap:anywhere}.dialogue-context a,.dialogue-reply a{color:#315968}.dialogue-notes{font-size:9px;line-height:1.5;border-top:1px solid #cbd6de;padding-top:6px;margin-top:3px;color:var(--sub)}.dialogue-notes p{margin:0}
@media screen and (max-width:600px){.dialogue-case p{font-size:12px}.dialogue-user p{font-size:13px}.dialogue-reply p{font-size:12px}.dialogue-selection p{overflow-wrap:anywhere}.dialogue-context{padding-left:0}.dialogue-user,.dialogue-selection,.dialogue-flow,.dialogue-reply{grid-template-columns:42px 1fr;gap:6px}}
.flow-case-values{margin:7px 0 6px;padding:5px 8px;border:1px solid #c5d0d8;border-radius:5px;background:#f3f6f8;font-size:9.2px;line-height:1.35}.flow-case-values p{margin:0 0 2px}.flow-case-values p:last-child{margin-bottom:0}.flow-case-values p:first-child{font-size:10.5px;font-weight:650}.flow-case-values a{color:#315968;overflow-wrap:anywhere}.single-flow{margin-top:4px}.single-flow .flow-value,.single-flow .flow-column,.single-flow .flow-condition{text-anchor:start;font-family:inherit;letter-spacing:-.01em}.single-flow .flow-column{font-family:inherit;font-weight:750;fill:#203747}.single-flow .flow-node-heading{text-anchor:middle;font-weight:750}.single-flow .flow-tag{text-anchor:middle;font-weight:650;fill:#536878}.single-flow .flow-node-label{text-anchor:middle;font-family:inherit;font-weight:700;letter-spacing:-.02em}.single-flow .flow-control,.single-flow .flow-data{fill:none;stroke:#263a48;stroke-width:1.25;marker-end:url(#flow-arrow)}.single-flow .flow-data{stroke:#8a9aa5;stroke-width:1}.single-flow .flow-repeat{stroke:#bb4b18;stroke-width:1.6;marker-end:url(#flow-repeat-arrow)}.single-flow .flow-condition{font-family:inherit;fill:#647987;letter-spacing:0}

.io-table{font-size:9.25px;line-height:1.43}.io-table col.node-col{width:28%}.io-table col.input-col{width:34%}.io-table col.output-col{width:38%}.io-table td{padding:2px 5px}.io-value{margin:0;font-family:inherit;font-size:9.25px;line-height:1.43;word-break:keep-all}.case-values p{font-family:inherit}.single-flow .flow-value{font-family:inherit;letter-spacing:-.01em}.architecture .intro{font-size:9.4px}.architecture .notes{font-size:8.5px;line-height:1.4}.architecture footer{font-size:7.6px}
</style></head><body>'''

html+='''<main class="page architecture">
<header><div class="top"><strong>커리어 에이전트 / 일괄 전환안</strong><span>기획 v3.1 / 2026.10.30 / 1 of 3</span></div>
<h1>온톨로지 챗</h1><p class="subtitle">발화마다 즉시 안내, 요청과 조회를 누적해 최종 답변은 한 번</p>
<p class="intro">보라색은 Jev의 선택과 판단, 초록색은 LLM의 인자 추출과 답변, 회색은 실행과 대화 상태를 처리하는 코드입니다.</p></header>
<div class="figure-head"><strong>발화별 수신 안내 → 조회 추가와 누적 → 최종 답변 1회</strong><div class="legend"><span><i class="swatch jev"></i>Jev</span><span><i class="swatch llm"></i>LLM</span><span><i class="swatch code"></i>코드</span><span><i class="swatch" style="background:white;border-color:#aab9c5;border-style:dashed"></i>목록</span><span style="color:var(--orange)">↻ 재실행</span></div></div>
<figure class="figure-scroll">'''+svg+'''</figure>
<div class="notes"><p><strong>실행 설정</strong> 함수 선택에는 개수 제한이 없습니다. <code>max_concurrent_queries</code>로 동시 조회 수를 정하고, 초과 조회는 대기열에서 이어서 실행합니다. 의존 작업은 선행 결과를 받은 뒤 실행합니다.</p>
<p><strong>누적과 한 번 전송</strong> 첫 발화와 추가 발화는 같은 요청에 요구와 조회 결과를 누적합니다. 25에서 대기열, 진행 호출, 미처리 발화, 버전과 전송 기록을 확인해 한 번 전송합니다. 생성 중 추가 발화는 즉시 안내하고 다시 조회에 반영합니다.</p></div>
<footer><span>구현 전 기획 / 지원, 조건, 문서, 기억, 조사 기능과 기존 승인 및 발송 정책 유지</span><span>박스 설명 2페이지 / 대화 시나리오 3페이지</span></footer>
</main>'''
case=json.loads((ROOT/'docs/examples/career/fixture.json').read_text())
j,c=case['job'],case['company']
assert j['company_canonical']==c['company_canonical']=='notion'
u=escape(j['url'],quote=True)
exec((ROOT/'docs/source/career/io_section.py').read_text())
html+=example
exec((ROOT/'docs/source/career/flow_section.py').read_text())
html+=utterances+'\n</body></html>'
(ROOT/'docs/examples/career/ontology-chat-plan.html').write_text(html)
print('Updated same HTML: 3 pages, explanatory inputs/outputs, parallel batch barrier and continuous chat scenario')

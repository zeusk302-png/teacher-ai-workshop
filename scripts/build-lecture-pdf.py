"""Create the public lecture handout from selected design and reviewed course sources."""
from pathlib import Path
import json, re, sys, shutil
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'artifacts/python-libs'))
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
PATH=OUT/'teacher-ai-lecture.pdf'
URL='https://zeusk302-png.github.io/teacher-ai-workshop/'
NIST='https://csrc.nist.gov/glossary/term/retrieval_augmented_generation'
GOOGLE='https://support.google.com/gemininotebook/answer/16179559?hl=ko'
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('MalgunBold','C:/Windows/Fonts/malgunbd.ttf'))
pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='MalgunBold',italic='Malgun',boldItalic='MalgunBold')
W,H=960,540
NAVY=HexColor('#05234e');TEAL=HexColor('#007e92');MUTED=HexColor('#527394');PALE=HexColor('#f1f7fb');LINE=HexColor('#d5e5ef')
c=canvas.Canvas(str(PATH),pagesize=(W,H),pageCompression=1)
c.setTitle('학교 규정 검색과 안내문 작성 · 부산보건고 교사 AI 연수')
c.setAuthor('김세영');c.setSubject('RAG·NotebookLM 이론과 공개 자료 검색 및 학교 업무 문서 실습')
page_count=0;checks=[]

def para(text,x,y,width,size=19,color=NAVY,bold=False,leading=None):
    style=ParagraphStyle('p',fontName='MalgunBold' if bold else 'Malgun',fontSize=size,leading=leading or size*1.45,textColor=color,wordWrap='CJK',spaceBefore=0,spaceAfter=0)
    p=Paragraph(text,style);pw,ph=p.wrap(width,H)
    p.drawOn(c,x,H-y-ph)
    checks.append({'page':page_count,'y':y,'height':round(ph,2),'bottom':round(y+ph,2),'text':re.sub('<[^>]+>','',text)[:70]})
    return ph

def txt(text,x,y,size=14,color=MUTED,font='Malgun'):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,H-y-size,text)

def box(x,y,w,h,fill=PALE):
    c.setFillColor(fill);c.roundRect(x,H-y-h,w,h,12,fill=1,stroke=0)

def image(path,x,y,w,h):
    c.drawImage(ImageReader(str(ROOT/path)),x,H-y-h,w,h,preserveAspectRatio=True,anchor='c',mask='auto')

def start(section,title,subtitle=None):
    global page_count
    if page_count:c.showPage()
    page_count+=1
    c.setFillColor(HexColor('#ffffff'));c.rect(0,0,W,H,fill=1,stroke=0)
    image(Path('docs/assets/school-logo.png'),32,17,161,34)
    txt('교사 AI 업무 연수',218,23,14,NAVY,'MalgunBold')
    c.setStrokeColor(LINE);c.line(32,H-65,W-32,H-65)
    txt(section,40,85,12,TEAL,'MalgunBold')
    para(escape(title),40,106,880,31,NAVY,True,39)
    if subtitle:para(escape(subtitle),40,153,880,14,MUTED,leading=20)
    c.setStrokeColor(LINE);c.line(40,34,W-40,34)
    txt('부산보건고등학교 · 학교 자료 검색과 안내문 작성',40,514,10,MUTED)
    txt(f'{page_count:02d}',893,510,14,TEAL,'MalgunBold')
    c.bookmarkPage(f'page{page_count}');c.addOutlineEntry(title,f'page{page_count}',level=0)

def cards(items,y=194,cols=3,heights=240):
    gap=18;cw=(880-(cols-1)*gap)/cols
    for i,(title,body) in enumerate(items):
        x=40+(i%cols)*(cw+gap); yy=y+(i//cols)*(heights+16)
        box(x,yy,cw,heights)
        para(title,x+20,yy+20,cw-40,21,TEAL,True,29)
        para(body,x+20,yy+67,cw-40,17,NAVY,leading=26)

def link(label,url,x=40,y=483,w=880):
    para(f'<a href="{escape(url)}" color="#007e92">{escape(label)}</a>',x,y,w,10,TEAL,leading=14)

def prompt(title,text,note=None):
    start('문서 실습',title)
    box(40,175,880,244)
    para(escape(text).replace('\n','<br/>'),62,195,836,19,leading=29)
    if note:para(escape(note),40,441,880,15,MUTED,leading=23)

start('120분 · 이론과 실습','학교 규정 검색과 안내문 작성')
para('학교 자료를 검색하고<br/><font color="#007e92">교직원 안내문으로 정리합니다.</font>',40,187,470,32,NAVY,True,46)
para('RAG와 NotebookLM의 개념 · 공개 자료 등록과 검색<br/>Word·PowerPoint·Excel 문서 작성과 검토',40,298,470,19,MUTED,leading=30)
image(Path('docs/assets/school-document-flow.png'),524,185,390,186)
image(Path('docs/assets/course-qr.png'),40,401,84,84)
para('강의 사이트 · 자료와 실습 화면<br/><a href="'+URL+'" color="#007e92">'+URL+'</a>',141,411,710,15,leading=25)
txt('교재 작성 2026. 10. 15. · 강사 김세영',524,382,13,MUTED)

profile=json.loads((ROOT/'artifacts/selected-build/profile.json').read_text(encoding='utf-8'))
start('강사 소개','김세영','기업부설연구소 연구소장 · R&D 엔지니어 · 기술교육자')
image(Path(profile['photo']),40,195,145,181)
para('주요 기술 경험',40,388,153,14,TEAL,True)
para('전기차 충전·상호운용 시험<br/>산업용 비전 검사·Edge AI<br/>AI 관광·모빌리티 기술개발',40,416,156,11.5,leading=20)
para('재직 및 경력',216,192,318,17,TEAL,True)
y=228
for period,role in profile['career']:
    txt(period,216,y,11,TEAL,'MalgunBold');y+=20
    y+=para(escape(role),216,y,305,13.5,leading=21)+13
para('학력',216,407,305,16,TEAL,True)
para('<br/>'.join(escape(x) for x in profile['education']),216,440,305,12,leading=20)
para('주요 강의 및 교육',552,192,368,17,TEAL,True)
y=229
for item in profile['lectures']:
    y+=para('• '+escape(item),552,y,368,12.5,leading=20)+6
txt('제공 이력서 기준 · 재직·강의 기록 중 연수 관련 항목 발췌',552,489,9.5,MUTED)

start('수업 안내','오늘의 수업 순서','개념을 익힌 뒤 함께 따라 하고, 조건을 바꿔 문서를 작성합니다.')
rows=[('00–10분','RAG와 NotebookLM','검색과 생성 · 방법과 제품의 차이'),('10–25분','AI 도구 비교','계정 기능 확인과 실습 도구 선택'),('25–55분','학교 자료 등록·검색','PDF 3종 등록 · 질문 · 인용 원문 대조'),('55–65분','휴식','자료 처리와 계정 상태 확인'),('65–80분','스킬과 작성 요청','발췌문·출처·양식·검토 기준 정리'),('80–110분','Word·PPT·Excel 실습','짧은 시연 후 한 형식 선택·작성·검토'),('110–120분','결과 확인','날짜·수치·서식 대조와 수정 사항 공유')]
for i,(t,title,body) in enumerate(rows):
    yy=192+i*40
    if i%2==0:box(40,yy,880,37)
    txt(t,55,yy+9,13,TEAL,'MalgunBold');txt(title,165,yy+9,14,NAVY,'MalgunBold');txt(body,435,yy+9,13,NAVY)

start('수업 안내','준비물과 완료할 결과')
cards([('준비물','노트북과 브라우저<br/>Google 계정<br/>실습에 사용할 외부 AI 계정<br/><br/>계정의 업로드·파일 생성 기능을 먼저 확인합니다.'),('공개 자료 3종','학교규정집<br/>학교규정 개정 사항<br/>학업성적관리 지침<br/><br/>학교·교육청·법령 자료를 구분하고 적용 시점을 확인합니다.'),('완료할 결과','등록한 노트북 1개<br/>검색 데이터가 담긴 작성 요청 1개<br/>검토한 업무 문서 1개<br/><br/>인용 두 곳을 원문과 대조한 기록도 남깁니다.')],heights=268)

start('01 · RAG와 NotebookLM','학교 규정은 어디에서 찾을까요?','같은 질문이라도 AI에게 제공한 자료에 따라 답변이 달라질 수 있습니다.')
cards([('질문','“수행평가 결시 학생의<br/>추가 평가 원칙은?”<br/><br/>학교·학년도·업무 상황을 구체적으로 적습니다.'),('등록한 자료','학교규정집과 개정 사항<br/>해당 학년도 교육청 지침<br/><br/>질문에 필요한 자료를 골라 검색 범위를 정합니다.'),('검토할 내용','적용 대상과 조건<br/>예외와 시행 시점<br/>관련 조항 또는 쪽<br/><br/>담당자가 확인할 항목을 남깁니다.')],heights=260)

start('01 · RAG와 NotebookLM','RAG는 데이터 검색과 답변 생성을 묶는 방식','Retrieval-Augmented Generation · 검색 증강 생성')
cards([('검색','질문과 관련된 문서나 구절을 자료 모음에서 찾습니다.<br/><br/>학교규정집에서 결시 처리에 관한 부분을 찾는 단계입니다.'),('검색 결과 제공','찾은 내용과 질문을 AI가 읽을 입력에 함께 넣습니다.<br/><br/>자료명·조항·적용 시점도 같이 전달하면 검토하기 쉽습니다.'),('답변 생성','AI가 전달받은 내용을 바탕으로 답변을 정리합니다.<br/><br/>검색이 잘못되거나 문맥이 빠지면 답변도 틀릴 수 있습니다.')],heights=263)
link('개념 출처 · NIST RAG 용어 정의',NIST)

start('01 · RAG와 NotebookLM','RAG 처리 순서','질문 → 데이터 검색 → 검색 결과 제공 → 답변 생성')
for i,(title,body) in enumerate([('질문','학교·업무·기준 시점'),('데이터 검색','관련 문서·구절 찾기'),('검색 결과 제공','찾은 내용과 질문 묶기'),('답변 생성','입력 내용을 사용해 정리')]):
    x=40+i*226;box(x,211,202,170)
    txt(f'{i+1:02d}',x+18,230,25,TEAL,'MalgunBold');para(title,x+18,278,166,20,NAVY,True);para(body,x+18,323,166,14,MUTED)
para('자료를 다시 학습시키는 것과는 다릅니다. 이 방식은 검색한 내용을 모델 입력에 제공해 활용합니다.',40,413,880,21,leading=31)
link('개념 출처 · NIST RAG 용어 정의',NIST)

start('01 · RAG와 NotebookLM','RAG와 NotebookLM은 무엇이 다를까요?')
box(40,182,880,278)
cols=[(58,162),(240,304),(568,322)]
for (x,w),label in zip(cols,['비교 항목','RAG','NotebookLM']):para(label,x,200,w,19,TEAL,True)
table=[('무엇인가','검색과 생성을 결합하는 방식','자료를 등록해 질문·정리하는 제품'),('무엇을 고르나','검색 방식·자료 갱신·권한·평가','노트북의 소스·질문·제공 기능'),('직접 만들 때','검색과 모델 연결 등을 설계','제공된 계정 기능을 사용'),('이번 연수','처리 순서를 이해','코딩 없이 자료 검색과 인용 확인')]
for i,row in enumerate(table):
    yy=247+i*50
    for (x,w),value in zip(cols,row):para(escape(value),x,yy,w,15.5,leading=22)
link('자료 기반 채팅·인용 기능 · Google 공식 도움말',GOOGLE)

start('01 · RAG와 NotebookLM','자료 등록과 모델 학습을 구분합니다')
cards([('자료 등록','노트북에서 질문에 사용할 소스를 추가합니다.<br/><br/>등록했다고 사용자가 새로운 언어 모델을 직접 학습한 것은 아닙니다.'),('이번 실습 범위','PDF 자료 선택<br/>질문과 답변<br/>인용 원문 대조<br/><br/>API 기반 검색 시스템을 구축하는 실습과 구분합니다.'),('외부 AI로 전달','확인한 발췌문과 출처를 작성 요청에 넣습니다.<br/><br/>복사만으로 외부 AI가 원래 노트북 전체를 자동 검색하도록 연결되지는 않습니다.')],heights=265)
link('제품 기능 확인 · Google 공식 도움말',GOOGLE)

start('01 · RAG와 NotebookLM','인용은 직접 열어서 확인합니다','답변을 읽고 끝내지 말고, 인용된 원문 두 곳을 확인합니다.')
cards([('날짜와 적용 범위','어느 학년도인가?<br/>언제부터 적용되는가?<br/>어떤 학교급·업무 대상인가?'),('조건과 예외','답변이 조건을 빠뜨렸는가?<br/>예외 조항이 있는가?<br/>인용 앞뒤 문맥은 무엇인가?'),('확인 필요','자료에 없는 담당자·기한·수치는 남겨 둡니다.<br/><br/>자료 간 충돌은 기록하고 업무 담당자가 검토합니다.')],heights=243)
para('다음 실습: 학교 공개 자료 3종을 준비하고 빈 노트북을 만듭니다.',40,461,880,18,TEAL,True)

start('실습 도구','검색과 작성에 사용할 도구를 고릅니다','계정의 실제 메뉴와 사용량을 확인합니다. 파일 생성이 막히면 텍스트와 표로 이어갑니다.')
items=[('NotebookLM','공개 자료 등록·선택, 자료에 관한 질문과 인용 확인'),('ChatGPT·Gemini','확인한 발췌문으로 안내문 초안·문장 수정·구조화'),('Claude','계정의 파일 생성 기능을 확인해 DOCX·PPTX·XLSX 요청'),('Copilot·Grok','웹 자료 탐색에 활용하고 공식 발표·원문과 대조')]
for i,(name,body) in enumerate(items):
    yy=196+i*62;box(40,yy,880,53);txt(name,59,yy+14,17,TEAL,'MalgunBold');para(escape(body),272,yy+14,620,16,leading=24)
link('도구별 최신 공식 안내는 강의 사이트의 AI 도구 비교에서 확인',URL+'index.html#tools')

steps=json.loads((ROOT/'docs/guide-data.js').read_text(encoding='utf-8').split('=',1)[1].strip().rstrip(';'))
steps[0].update(image='assets/guide-current/start-pack.jpg',target='연수 홈의 실습 자료 받기',action='실습 자료 받기를 눌러 ZIP을 내려받고 압축을 풉니다. 학교규정집·개정 사항·학업성적관리 지침 PDF 3종을 준비합니다.',result='압축을 푼 폴더에서 PDF 3개를 확인합니다. ZIP 자체를 올리지 않습니다.')
steps[15]['image']='assets/guide-current/brief-input.jpg';steps[16]['image']='assets/guide-current/brief-result.jpg'
for i,s in enumerate(steps):
    start(f'실습 화면 · {i+1:02d} / 17',s['title'])
    image(Path('docs')/s['image'],40,182,586,304)
    box(647,182,273,303)
    para('할 일',665,199,237,17,TEAL,True)
    para(escape(s['action']),665,235,237,14.5,leading=23)
    para('확인할 결과',665,365,237,17,TEAL,True)
    para(escape(s['result']),665,401,237,13.5,leading=21)
    note=('현재 연수 사이트 · 2026.10.15' if i in (0,15,16) else '실제 서비스 화면 · 2026.10.14')
    if i in (15,16):note+=' · 입력 예시는 규정 발췌가 아닙니다.'
    txt(note,40,490,9.5,MUTED)
    link('같은 단계 열기',URL+f'guide.html#{i}',647,487,273)

start('검색에서 작성으로','작성 요청에 넣을 네 가지')
cards([('업무 목적과 문서 형식','누가 읽는가?<br/>무엇을 해야 하는가?<br/><br/>예: 교직원 안내문<br/>A4 1쪽 · 원칙·절차·참고 자료'),('검색한 데이터와 출처','원문을 확인한 발췌문<br/>자료명·조항 또는 쪽<br/>적용 시점<br/><br/>확인하지 못한 항목은 따로 표시합니다.'),('작성 순서와 검토 기준','자료의 적용 범위 정리<br/>초안 작성<br/>원문과 초안 대조<br/><br/>없는 인명·날짜·수치를 만들지 않도록 요청합니다.')],heights=269)

start('스킬 활용','스킬은 반복 작업의 절차를 담습니다','업무별 작업 순서와 자료·도구 사용법을 묶은 안내를 참고합니다.')
cards([('문서·슬라이드·표','문서 작성과 검토<br/>슬라이드 구성과 넘침 확인<br/>수식 작성과 값 대조<br/><br/>사이트에서 원본 설명과 사용 방식을 확인합니다.'),('사용 환경 확인','서비스가 지원하는 스킬인지<br/>설치나 도구가 필요한지<br/>허용되는 자료 범위는 무엇인지<br/><br/>GitHub에 있다고 모든 채팅 서비스에서 바로 실행되지는 않습니다.'),('이번 수업에서','절차와 검토 기준을 읽습니다.<br/>작성 요청에 필요한 부분을 반영합니다.<br/><br/>설치 여부보다 작업 순서를 문서로 남기는 데 집중합니다.')],heights=273)
link('스킬 목록과 원본 문서',URL+'index.html#skills')

prompt('교직원 안내문을 요청하는 예시','확인한 발췌문과 자료명·조항 또는 쪽·적용 시점만 사용해 교직원 안내문 초안을 작성해 줘.\n\n원칙 / 처리 절차 / 참고 자료 / 확인 필요 사항으로 구성하고 A4 1쪽 분량으로 정리해 줘. 제공되지 않은 담당자·일정·수치는 만들지 말아 줘.\n\n[여기에 확인한 발췌문과 출처를 붙여 넣습니다.]','이 예시는 작성 요청 양식입니다. 실제 규정 내용은 원문에서 확인해 넣습니다.')

start('문서 실습 · Word / 한글','안내문은 내용부터 확인하고 서식을 정리합니다')
cards([('내용 대조','제목과 적용 대상<br/>처리 원칙·조건·예외<br/>담당자·일정·참고 자료<br/><br/>확정 정보와 확인 필요 사항을 구분합니다.'),('문서 열기','DOCX를 Word에서 열거나 본문·표를 편집기에 붙여 넣습니다.<br/><br/>한글을 쓰는 경우 저장 형식과 글꼴·표 배치를 확인합니다.'),('서식 확인','표가 다음 쪽으로 밀리는가?<br/>제목만 남은 쪽이 있는가?<br/>인쇄할 때 잘리는 부분은 없는가?<br/><br/>수정본을 새 이름으로 저장합니다.')],heights=268)

prompt('같은 내용을 교직원 설명용 5장으로','확인한 안내문 내용을 교직원 설명용 슬라이드 5장으로 구성해 줘.\n1장 목적과 대상 / 2장 처리 원칙 / 3장 절차 / 4장 예외·확인 필요 / 5장 참고 자료.\n\n각 장에 핵심 메시지 하나, 짧은 본문, 발표자 메모를 넣어 줘. 제공된 원문 밖의 규정·일정·수치는 추가하지 말아 줘.','PPTX 생성이 어려우면 슬라이드 번호·제목·본문·발표자 메모를 표로 받아 옮깁니다.')

start('문서 실습 · PowerPoint','발표 화면에서 읽히는지 확인합니다')
cards([('장별 메시지','제목만 읽어도 순서가 보이는가?<br/>한 장에 메시지가 여러 개 겹치는가?<br/><br/>중복 문장은 합치고 자세한 설명은 발표자 메모로 옮깁니다.'),('글자와 표','발표 화면에서 글자가 보이는가?<br/>표가 잘리거나 겹치는가?<br/>화면 밖으로 나간 항목이 있는가?<br/><br/>실제 발표 모드로 확인합니다.'),('원문과 일치','짧게 줄이면서 조건·예외를 지웠는가?<br/>날짜·수치가 바뀌었는가?<br/><br/>발표자 메모와 참고 자료에 확인한 출처를 남깁니다.')],heights=270)

start('문서 실습 · Excel','가상 예산 데이터를 수식으로 계산합니다','실습용 가상 데이터 · 담당 부서·상태 열을 유지하고 F열에 금액을 추가합니다. 아래 표는 계산할 항목만 표시합니다.')
headers=['항목','수량','단가','금액']
xs=[57,455,578,728];widths=[370,90,110,166]
for x,w,t in zip(xs,widths,headers):para(t,x,190,w,18,TEAL,True)
budget=[['안내자료 인쇄','120','1,000','120,000'],['간식','50','3,000','150,000'],['체험 재료','20','4,000','80,000'],['현수막','1','50,000','50,000']]
for i,row in enumerate(budget):
    yy=230+i*41;box(40,yy-2,880,38)
    for x,w,t in zip(xs,widths,row):para(t,x,yy+5,w,16,leading=23)
para('합계 400,000원',57,409,450,23,NAVY,True)
para('F2 = B2*C2 → 아래 행으로 복사<br/>합계 = SUM(F2:F5)',555,407,365,18,TEAL,leading=28)
link('가상 예산 CSV 내려받기',URL+'downloads/practice-budget.csv')

prompt('Excel 작성 요청 예시','가상 예산 CSV의 원본 행과 값을 유지해 줘. F열에 금액을 추가하고 각 행은 수량 × 단가 수식으로 계산해 줘.\n\n합계와 가상 예산 상한 500,000원 대비 차액을 수식으로 표시해 줘. 빈 셀·문자형 숫자·중복 행을 점검해 줘. 계산 결과만 입력하지 말고 사용한 수식을 설명해 줘.','수동 대조: 120 × 1,000 = 120,000 / 50 × 3,000 = 150,000 / 합계 400,000 / 차액 100,000원.')

start('문서 실습 · Excel','값과 수식을 따로 확인합니다')
cards([('입력 데이터','원본 행이 모두 있는가?<br/>숫자가 문자로 들어갔는가?<br/>빈 셀·중복 행이 있는가?<br/><br/>원본 CSV와 행 수를 대조합니다.'),('수식','수량과 단가를 곱했는가?<br/>합계 범위가 맞는가?<br/>상한과 차액이 맞는가?<br/><br/>두 행을 직접 계산해 비교합니다.'),('저장과 전달','XLSX를 다시 열어 수식이 남아 있는지 확인합니다.<br/><br/>CSV는 서식·여러 시트·수식을 보존하는 통합문서 형식과 다릅니다.')],heights=270)

start('파일이 생성되지 않을 때','본문·슬라이드 표·CSV로 이어갑니다')
cards([('Word / 한글','복사 가능한 본문과 표를 요청합니다.<br/><br/>문서 편집기에 붙여 넣고 제목·표·쪽 나눔을 확인한 뒤 저장합니다.'),('PowerPoint','슬라이드별 제목·본문·발표자 메모를 표로 요청합니다.<br/><br/>표 내용을 슬라이드에 옮기고 발표 화면에서 확인합니다.'),('Excel','원본 데이터와 수식 설명을 요청합니다.<br/><br/>편집기에서 수식을 입력하고 XLSX로 저장합니다. 파일 확장자만 바꾸지 않습니다.')],heights=268)

start('결과 확인','실습을 마칠 때 남길 세 가지')
cards([('노트북과 검색 기록','공개 자료 등록 확인<br/>질문과 선택한 소스<br/>인용 두 곳의 원문 대조<br/><br/>자료명과 적용 시점을 남깁니다.'),('작성 요청','업무 목적·문서 형식<br/>확인한 발췌문과 출처<br/>작성 순서·검토 기준<br/><br/>TXT 또는 복사 가능한 본문으로 저장합니다.'),('검토한 문서','한 가지 파일 형식 선택<br/>내용·날짜·수치 확인<br/>표·글자·페이지 확인<br/><br/>수정한 내용과 확인 필요 항목을 기록합니다.')],heights=268)

start('참고 자료','공식 도움말과 공개 자료')
references=[('RAG 개념 · NIST',NIST),('소스 기반 채팅과 인용 · Google',GOOGLE),('Gemini Canvas · Google','https://support.google.com/gemini/answer/16047321?hl=ko'),('Claude 파일 작성 · Anthropic','https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude'),('학교·교육청·법령 자료 11종 · 출처와 적용 시점',URL+'index.html#materials'),('도구 비교와 스킬 원본 · 강의 사이트',URL+'index.html#resources')]
for i,(label,url) in enumerate(references):
    para(f'<a href="{escape(url)}" color="#007e92">{escape(label)}</a>',40,192+i*40,880,16,TEAL,leading=23)
para('학교 자료는 사이트 자료실의 공개본을 사용합니다. 실제 업무 적용 전에는 기관의 최신 원문과 담당자 확인이 필요합니다. 계정 기능과 메뉴는 업데이트에 따라 달라질 수 있습니다.',40,450,880,13,MUTED,leading=20)

start('강의 자료','다시 사용할 자료는 사이트에 있습니다')
image(Path('docs/assets/course-qr.png'),55,207,215,215)
para('공개 자료 · 17단계 실습 화면<br/>RAG와 NotebookLM 비교<br/>작성 요청 양식 · 문서 검토 절차<br/>강의 교재 PDF',320,204,585,25,NAVY,True,42)
para('<a href="'+URL+'" color="#007e92">'+URL+'</a>',320,401,585,16,TEAL,leading=27)
para('QR 코드로 강의 사이트에 접속합니다.',320,448,585,17,MUTED)
c.save()
shutil.copyfile(PATH,ROOT/'docs/downloads/teacher-ai-lecture.pdf')
(ROOT/'artifacts/selected-build/pdf-layout-checks.json').write_text(json.dumps({'pages':page_count,'blocks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{page_count} pages: {PATH}')

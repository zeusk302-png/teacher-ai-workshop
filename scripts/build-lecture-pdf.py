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
RAG_BUILD='https://learn.microsoft.com/en-us/azure/search/retrieval-augmented-generation-overview'
pdfmetrics.registerFont(TTFont('Malgun','C:/Windows/Fonts/malgun.ttf'))
pdfmetrics.registerFont(TTFont('MalgunBold','C:/Windows/Fonts/malgunbd.ttf'))
pdfmetrics.registerFontFamily('Malgun',normal='Malgun',bold='MalgunBold',italic='Malgun',boldItalic='MalgunBold')
W,H=960,540
NAVY=HexColor('#05234e');TEAL=HexColor('#007e92');MUTED=HexColor('#527394');PALE=HexColor('#f1f7fb');LINE=HexColor('#d5e5ef')
c=canvas.Canvas(str(PATH),pagesize=(W,H),pageCompression=1)
c.setTitle('학교 자료 검색과 업무 문서 완성 · 부산보건고 교사 AI 연수')
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
    txt('부산보건고등학교 · 학교 자료 검색과 업무 문서 완성',40,514,10,MUTED)
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

start('120분 · 이론과 실습','학교 자료 검색과 업무 문서 완성')
para('NotebookLM으로 준비하고<br/><font color="#007e92">양식 문서를 완성합니다.</font>',40,187,470,32,NAVY,True,46)
para('RAG 원리와 구축 자원 · 자료 검색과 작성 요청<br/>외부 AI로 사전답사 계획서 작성 · 조건 변경과 검토',40,298,470,19,MUTED,leading=30)
image(Path('docs/assets/school-document-flow.png'),524,185,390,186)
image(Path('docs/assets/course-qr.png'),40,401,84,84)
para('강의 사이트 · 자료와 실습 화면<br/><a href="'+URL+'" color="#007e92">'+URL+'</a>',141,411,710,15,leading=25)
txt('교재 수정 2026. 10. 18. · 강사 김세영',524,382,13,MUTED)

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

start('수업 안내','오늘의 수업 순서','자료 등록 5분 · 검색한 내용으로 작성 요청을 만들고 양식 문서를 완성합니다.')
schedule_source=(ROOT/'docs/data.js').read_text(encoding='utf-8')
schedule_block=re.search(r'schedule:\s*\[(.*?)\n\s*\]',schedule_source,re.S).group(1)
rows=[(time+'분',title,body) for time,title,body in re.findall(r"\{time:'([^']+)',title:'([^']+)',description:'([^']+)'\}",schedule_block)]
assert len(rows)==9, 'Review the public 120-minute timetable before rebuilding the PDF'
for i,(t,title,body) in enumerate(rows):
    yy=183+i*34
    if i%2==0:box(40,yy,880,33)
    txt(t,51,yy+9,11,TEAL,'MalgunBold')
    para(escape(title),151,yy+7,264,12,NAVY,True,17)
    para(escape(body),435,yy+2,470,11,NAVY,leading=15)

start('수업 안내','준비물과 완료할 결과')
cards([('준비물','노트북과 브라우저<br/>Google 계정<br/>실습에 사용할 외부 AI 계정<br/><br/>계정의 업로드·파일 생성 기능을 먼저 확인합니다.'),('검색 기초 자료 3종','학교규정집<br/>학교규정 개정 사항<br/>학업성적관리 지침<br/><br/>학교·교육청·법령 자료를 구분하고 적용 시점을 확인합니다.'),('완료할 결과','자료를 등록한 노트북<br/>재사용할 작성 요청<br/>조건 변경을 반영한 문서<br/><br/>검색한 원문 두 곳을 확인한 기록을 남깁니다.')],heights=268)

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
table=[('무엇인가','검색과 생성을 결합하는 방식','자료를 등록해 질문·정리하는 제품'),('무엇을 고르나','검색 방식·자료 갱신·권한·평가','노트북의 소스·질문·제공 기능'),('직접 만들 때','검색과 모델 연결 등을 설계','제공된 계정 기능을 사용'),('이번 연수','처리 순서를 이해','검색·작성 요청 준비에 활용')]
for i,row in enumerate(table):
    yy=247+i*50
    for (x,w),value in zip(cols,row):para(escape(value),x,yy,w,15.5,leading=22)
link('자료 기반 채팅·인용 기능 · Google 공식 도움말',GOOGLE)

start('01 · RAG와 NotebookLM','직접 RAG를 구축할 때 필요한 것','자료와 검색 기능 · 생성 모델 · 연결 프로그램과 운영 환경')
cards([('자료와 검색','자료 수집·텍스트 추출<br/>검색할 구간 나누기<br/>자료명·쪽·적용 연도 보관<br/><br/>검색 색인과 검색 기능<br/>의미 검색에는 임베딩 활용'),('모델과 연결','모델 API 또는 직접 실행<br/>모델 입력·출력 처리<br/><br/>질문 → 검색 → 원문·지시문 구성 → 모델 호출을 프로그램으로 연결'),('실행과 운영','실행 환경과 사용 비용<br/>문서별 접근 권한<br/>개정 자료 반영<br/>검색·답변 품질 검사<br/><br/>자료에 없는 질문도 시험')],heights=255)
para('API 사용 시 GPU 직접 설치 불필요 · 벡터 DB는 검색 방식에 따라 선택 · RAG는 모델 추가 학습 없이 구성 가능',40,459,880,11,MUTED,leading=16)
link('구축 구성 · Microsoft RAG 안내',RAG_BUILD)

start('01 · RAG와 NotebookLM','이번 연수에서는 도구별로 역할을 나눕니다','상황 입력 → 자료 검색 → 작성 요청 → 양식 문서 완성 → 수정·검토')
cards([('NotebookLM','관련 자료와 양식 등록<br/>업무에 필요한 내용 검색<br/>인용 원문 확인<br/><br/>발췌문·입력값·작성 조건을 외부 AI용 요청으로 정리'),('외부 AI와 양식','작성 요청·원문·양식 받기<br/>문서 파일 생성<br/>날짜·인원 변경 반영<br/><br/>파일 생성 기능은 계정과 실행 도구에 따라 확인'),('사람','업무 조건과 자료 선택<br/>요청·파일 복사·첨부<br/>완성 파일 직접 열기<br/><br/>내용·표·쪽 나눔 검사<br/>수정 전 값 잔재 확인')],heights=270)
link('제품 기능 · Google 공식 도움말 · 이 역할 분담은 이번 연수의 진행 방식입니다',GOOGLE)

start('01 · RAG와 NotebookLM','외부 AI에 전달할 세 가지','NotebookLM의 인용 번호만 복사하면 필요한 원문이 함께 전달되지 않을 수 있습니다.')
cards([('작성 요청','업무 목적과 필요한 결과물<br/>양식 항목별 작성 내용<br/>이번 날짜·대상·인원<br/>고정할 작성 규칙<br/>미확정 정보 처리<br/>파일 검토 기준'),('원문 발췌','검색한 내용 중 실제 사용할 구절을 넣습니다.<br/><br/>자료명·조항·쪽·적용 시점도 적고, 외부 AI가 원래 노트북을 읽는다고 가정하지 않습니다.'),('원본 양식','제목·항목·표 구조를 유지할 편집용 파일을 첨부합니다.<br/><br/>PDF 서식을 DOCX로 재구성하는 것과 HWPX 원본 양식을 보존하는 것은 별도 검증이 필요합니다.')],heights=270)
para('RAG는 사용할 내용을 찾는 데 쓰입니다. 문서 파일 생성과 양식 반영에는 별도의 기능·도구가 필요합니다.',40,475,880,12,TEAL,leading=18)

start('01 · RAG와 NotebookLM','인용은 직접 열어서 확인합니다','답변을 읽고 끝내지 말고, 인용된 원문 두 곳을 확인합니다.')
cards([('날짜와 적용 범위','어느 학년도인가?<br/>언제부터 적용되는가?<br/>어떤 학교급·업무 대상인가?'),('조건과 예외','답변이 조건을 빠뜨렸는가?<br/>예외 조항이 있는가?<br/>인용 앞뒤 문맥은 무엇인가?'),('확인 필요','자료에 없는 담당자·기한·수치는 남겨 둡니다.<br/><br/>자료 간 충돌은 기록하고 업무 담당자가 검토합니다.')],heights=243)
para('다음 실습: 학교 검색 기초 자료 3종을 준비하고 빈 노트북을 만듭니다.',40,461,880,18,TEAL,True)

# Shared web notes provide the six deeper lecture summaries. The full prose is on the site.
theory=json.loads((ROOT/'docs/content/rag-theory.json').read_text(encoding='utf-8'))
for chapter in theory:
    start('이론 심화 · 강의 보충',chapter['title'],'자세한 설명은 강의 사이트의 각 탭에서 심화 설명을 펼쳐 읽습니다.')
    cards([(escape(title),escape(body).replace('\n','<br/>')) for title,body in chapter['pdf']],heights=270)
    if chapter['sources']:
        link(chapter['sources'][0][0],chapter['sources'][0][1])
    else:
        link('전체 심화 설명 · 이번 연수의 실습 설계와 사전 테스트',URL+'index.html#concepts')

def long_prompt(title,text):
    lines=text.splitlines();groups=[];group=[]
    style=ParagraphStyle('prompt-measure',fontName='Malgun',fontSize=13,leading=20,wordWrap='CJK')
    for line in lines:
        trial='\n'.join(group+[line])
        height=Paragraph(escape(trial).replace('\n','<br/>'),style).wrap(836,H)[1]
        if height>274 and group:
            groups.append(group);group=[line]
        else:group.append(line)
    if group:groups.append(group)
    for n,part in enumerate(groups):
        start('복사해서 사용할 요청',title+(f' · {n+1}/{len(groups)}' if len(groups)>1 else ''))
        box(40,175,880,300)
        para(escape('\n'.join(part)).replace('\n','<br/>'),62,191,836,13,leading=20)
        link('같은 요청을 사이트에서 복사하기',URL+'index.html#notebook',y=483)

prompt_source=(ROOT/'docs/data.js').read_text(encoding='utf-8')
course_prompts={key:re.search(key+r':`(.*?)`',prompt_source,re.S).group(1) for key in ['search','handoff']}

start('실습 도구','검색과 작성에 사용할 도구를 고릅니다','계정의 실제 메뉴와 사용량을 확인합니다. 파일 생성이 막히면 텍스트와 표로 이어갑니다.')
items=[('NotebookLM','공개 자료 등록·선택, 자료에 관한 질문과 인용 확인'),('ChatGPT·Gemini','확인한 발췌문·입력값·양식을 전달해 작성·수정'),('Claude','계정의 파일 생성 기능을 확인해 DOCX·PPTX·XLSX 요청'),('Copilot·Grok','웹 자료 탐색에 활용하고 공식 발표·원문과 대조')]
for i,(name,body) in enumerate(items):
    yy=196+i*62;box(40,yy,880,53);txt(name,59,yy+14,17,TEAL,'MalgunBold');para(escape(body),272,yy+14,620,16,leading=24)
link('도구별 최신 공식 안내는 강의 사이트의 AI 도구 비교에서 확인',URL+'index.html#tools')

steps=json.loads((ROOT/'docs/guide-data.js').read_text(encoding='utf-8').split('=',1)[1].strip().rstrip(';'))
steps[0].update(image='assets/guide-current/start-pack.jpg',target='연수 홈의 실습 자료 받기',action='실습 자료 받기를 눌러 ZIP을 내려받고 압축을 풉니다. 학교규정집·개정 사항·학업성적관리 지침 PDF 3종을 준비합니다.',result='압축을 푼 폴더에서 PDF 3개를 확인합니다. ZIP 자체를 올리지 않습니다.')
steps[15]['image']='assets/guide-current/brief-input.jpg';steps[16]['image']='assets/guide-current/brief-result.jpg'
for i,s in enumerate(steps):
    if i==7:long_prompt('NotebookLM에 할 검색 요청',course_prompts['search'])
    if i==13:long_prompt('NotebookLM에 할 작성 요청 준비 지시',course_prompts['handoff'])
    start(f'실습 화면 · {i+1:02d} / 17',s['title'])
    image(Path('docs')/s['image'],40,182,586,304)
    box(647,182,273,303)
    para('할 일',665,199,237,17,TEAL,True)
    para(escape(s['action']),665,235,237,14.5,leading=23)
    para('확인할 결과',665,365,237,17,TEAL,True)
    para(escape(s['result']),665,401,237,13.5,leading=21)
    note=('연수 사이트 · 2026.10.18' if i in (0,15,16) else '실제 서비스 화면 · 2026.10.14')
    if i in (15,16):note+=' · 사전답사 계획서 교육용 예시입니다.'
    txt(note,40,490,9.5,MUTED)
    link('같은 단계 열기',URL+f'guide.html#{i}',647,487,273)

start('검색에서 작성으로','작성 요청에 넣을 내용')
cards([('업무 목적과 문서 형식','누가 읽는가?<br/>무엇을 해야 하는가?<br/><br/>예: 사전답사 계획서<br/>A4 1쪽 · 양식의 6개 항목'),('검색한 데이터와 출처','원문을 확인한 발췌문<br/>자료명·조항 또는 쪽<br/>적용 시점<br/><br/>확인하지 못한 항목은 따로 표시합니다.'),('작성 순서와 검토 기준','자료의 적용 범위 정리<br/>초안 작성<br/>원문과 초안 대조<br/><br/>없는 인명·날짜·수치를 만들지 않도록 요청합니다.')],heights=269)

start('스킬 활용','스킬은 반복 작업의 절차를 담습니다','업무별 작업 순서와 자료·도구 사용법을 묶은 안내를 참고합니다.')
cards([('문서·슬라이드·표','문서 작성과 검토<br/>슬라이드 구성과 넘침 확인<br/>수식 작성과 값 대조<br/><br/>사이트에서 원본 설명과 사용 방식을 확인합니다.'),('사용 환경 확인','서비스가 지원하는 스킬인지<br/>설치나 도구가 필요한지<br/>허용되는 자료 범위는 무엇인지<br/><br/>GitHub에 있다고 모든 채팅 서비스에서 바로 실행되지는 않습니다.'),('이번 수업에서','스킬 설치는 선택입니다.<br/>절차와 검토 기준을 읽습니다.<br/>작성 요청에 필요한 부분을 반영합니다.<br/><br/>설치 여부보다 작업 순서를 문서로 남기는 데 집중합니다.')],heights=273)
link('스킬 목록과 원본 문서',URL+'index.html#skills')

start('기본 실습 · 교육용 가상 사례','사전답사 계획서를 한 장으로 완성합니다','공개 매뉴얼 서식 7 · PDF 67페이지 / 인쇄 65쪽')
cards([('자료와 입력값','지침에서 찾을 것:<br/>서식 항목과 점검 사항<br/><br/>이번 입력값:<br/>11월 6일 14~17시<br/>부산박물관 · 교사 A·B<br/>총 2명 · 숙박·식사 없음'),('작성 요청과 양식','NotebookLM에서 발췌·입력값·작성 조건을 정리합니다.<br/><br/>검토한 요청과 원본 서식 PDF를 외부 AI에 전달합니다.<br/>DOCX와 확인용 PDF를 요청합니다.'),('파일 확인','일시·장소·답사일정<br/>답사자·이동수단·점검 사항<br/><br/>미정인 이동수단은<br/>[확인 필요]로 남깁니다.<br/>A4 한 쪽과 표를 확인합니다.')],heights=280)
link('원본 서식과 실제 작성 예시',URL+'guide.html#document-workflow')

start('기본 실습 · 조건 변경','다음 업무에 다시 쓸 수 있는지 시험합니다')
cards([('첫 문서','2026.11.6.(금)<br/>14:00~17:00<br/>교사 A·B · 2명<br/><br/>장소와 점검 사항 확인'),('변경할 조건','2026.11.13.(금)<br/>15:00~18:00<br/>교사 A·B·C · 3명<br/><br/>일정표도 1시간씩 늦추기'),('검사할 결과','본문과 표의 새 값 일치<br/>이전 날짜·시간·2명 잔존<br/>명단과 총인원 일치<br/><br/>나머지 조건 유지<br/>변경본을 새 파일로 받기')],heights=260)
para('2026.10.18. Claude Pro 사전 테스트: PDF 양식을 DOCX로 재구성. 무료 계정 동일 실행·HWPX 원본 보존은 별도 확인 대상입니다.',40,467,880,11,MUTED,leading=16)
link('첫 작성 PDF와 변경 후 PDF 비교',URL+'guide.html#document-workflow')

prompt('양식 작성 요청 예시','첨부 양식과 원문 발췌, 이번 입력값으로 사전답사 계획서를 작성해 줘.\n일시 / 장소 / 답사일정 / 답사자 / 이동수단 / 점검 사항의 순서와 일정표 구조를 참고해 A4 1쪽으로 만들어 줘.\n\n예시의 날짜·이름은 복사하지 말고 미정 정보는 [확인 필요]로 남겨 줘. DOCX와 확인용 PDF, 별도의 항목 반영표를 제공해 줘.','입력값과 확인한 원문을 함께 보내며, 조건 변경은 첫 파일 검토 후 따로 요청합니다.')

start('문서 실습 · Word / 한글','계획서의 내용과 표를 대조하고 서식을 확인합니다')
cards([('내용 대조','제목과 적용 대상<br/>처리 원칙·조건·예외<br/>담당자·일정·참고 자료<br/><br/>확정 정보와 확인 필요 사항을 구분합니다.'),('문서 열기','DOCX를 Word에서 열거나 본문·표를 편집기에 붙여 넣습니다.<br/><br/>한글을 쓰는 경우 저장 형식과 글꼴·표 배치를 확인합니다.'),('서식 확인','표가 다음 쪽으로 밀리는가?<br/>제목만 남은 쪽이 있는가?<br/>인쇄할 때 잘리는 부분은 없는가?<br/><br/>수정본을 새 이름으로 저장합니다.')],heights=268)

prompt('선택 응용 · 계획서를 설명 자료 5장으로','확인한 계획서를 교직원 설명용 슬라이드 5장으로 구성해 줘.\n1장 목적·대상 / 2장 일정·장소 / 3장 답사자·이동 / 4장 점검 사항 / 5장 미정 항목·참고 자료.\n\n각 장에 핵심 메시지 하나, 짧은 본문, 발표자 메모를 넣어 줘. 제공된 원문 밖의 규정·일정·수치는 추가하지 말아 줘.','PPTX 생성이 어려우면 슬라이드 번호·제목·본문·발표자 메모를 표로 받아 옮깁니다.')

start('선택 응용 · PowerPoint','발표 화면에서 읽히는지 확인합니다')
cards([('장별 메시지','제목만 읽어도 순서가 보이는가?<br/>한 장에 메시지가 여러 개 겹치는가?<br/><br/>중복 문장은 합치고 자세한 설명은 발표자 메모로 옮깁니다.'),('글자와 표','발표 화면에서 글자가 보이는가?<br/>표가 잘리거나 겹치는가?<br/>화면 밖으로 나간 항목이 있는가?<br/><br/>실제 발표 모드로 확인합니다.'),('원문과 일치','짧게 줄이면서 조건·예외를 지웠는가?<br/>날짜·수치가 바뀌었는가?<br/><br/>발표자 메모와 참고 자료에 확인한 출처를 남깁니다.')],heights=270)

start('선택 응용 · Excel','가상 예산 데이터를 수식으로 계산합니다','실습용 가상 데이터 · 담당 부서·상태 열을 유지하고 F열에 금액을 추가합니다. 아래 표는 계산할 항목만 표시합니다.')
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

start('선택 응용 · Excel','값과 수식을 따로 확인합니다')
cards([('입력 데이터','원본 행이 모두 있는가?<br/>숫자가 문자로 들어갔는가?<br/>빈 셀·중복 행이 있는가?<br/><br/>원본 CSV와 행 수를 대조합니다.'),('수식','수량과 단가를 곱했는가?<br/>합계 범위가 맞는가?<br/>상한과 차액이 맞는가?<br/><br/>두 행을 직접 계산해 비교합니다.'),('저장과 전달','XLSX를 다시 열어 수식이 남아 있는지 확인합니다.<br/><br/>CSV는 서식·여러 시트·수식을 보존하는 통합문서 형식과 다릅니다.')],heights=270)

start('파일이 생성되지 않을 때','본문·슬라이드 표·CSV로 이어갑니다')
cards([('Word / 한글','복사 가능한 본문과 표를 요청합니다.<br/><br/>문서 편집기에 붙여 넣고 제목·표·쪽 나눔을 확인한 뒤 저장합니다.'),('PowerPoint','슬라이드별 제목·본문·발표자 메모를 표로 요청합니다.<br/><br/>표 내용을 슬라이드에 옮기고 발표 화면에서 확인합니다.'),('Excel','원본 데이터와 수식 설명을 요청합니다.<br/><br/>편집기에서 수식을 입력하고 XLSX로 저장합니다. 파일 확장자만 바꾸지 않습니다.')],heights=268)

start('결과 확인','실습을 마칠 때 남길 세 가지')
cards([('노트북과 검색 기록','공개 자료 등록 확인<br/>질문과 선택한 소스<br/>인용 두 곳의 원문 대조<br/><br/>자료명과 적용 시점을 남깁니다.'),('작성 요청','업무 목적·문서 형식<br/>확인한 발췌문과 출처<br/>작성 순서·검토 기준<br/><br/>TXT 또는 복사 가능한 본문으로 저장합니다.'),('검토한 문서','조건 변경을 반영한 문서<br/>내용·날짜·수치 확인<br/>표·글자·페이지 확인<br/><br/>수정한 내용과 확인 필요 항목을 기록합니다.')],heights=268)

start('참고 자료','공식 도움말과 공개 자료')
references=[('RAG 개념 · NIST',NIST),('소스 기반 채팅과 인용 · Google',GOOGLE),('Gemini Canvas · Google','https://support.google.com/gemini/answer/16047321?hl=ko'),('Claude 파일 작성 · Anthropic','https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude'),('학교·교육청·법령 자료 11종 · 출처와 적용 시점',URL+'index.html#materials'),('도구 비교와 스킬 원본 · 강의 사이트',URL+'index.html#resources')]
for i,(label,url) in enumerate(references):
    para(f'<a href="{escape(url)}" color="#007e92">{escape(label)}</a>',40,192+i*40,880,16,TEAL,leading=23)
para('학교 자료는 사이트 자료실의 공개본을 사용합니다. 실제 업무 적용 전에는 기관의 최신 원문과 담당자 확인이 필요합니다. 계정 기능과 메뉴는 업데이트에 따라 달라질 수 있습니다.',40,450,880,13,MUTED,leading=20)

start('강의 자료','다시 사용할 자료는 사이트에 있습니다')
image(Path('docs/assets/course-qr.png'),55,207,215,215)
para('공개 자료 · 17단계 실습 화면<br/>RAG 이론 심화 6개 장<br/>양식 작성 · 조건 변경 · 검토 절차<br/>강의 교재 PDF',320,204,585,25,NAVY,True,42)
para('<a href="'+URL+'" color="#007e92">'+URL+'</a>',320,401,585,16,TEAL,leading=27)
para('QR 코드로 강의 사이트에 접속합니다.',320,448,585,17,MUTED)
c.save()
shutil.copyfile(PATH,ROOT/'docs/downloads/teacher-ai-lecture.pdf')
(ROOT/'artifacts/selected-build/pdf-layout-checks.json').write_text(json.dumps({'pages':page_count,'blocks':checks},ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{page_count} pages: {PATH}')

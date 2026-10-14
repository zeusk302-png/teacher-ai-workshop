import requests, bs4, re, json, hashlib
from pathlib import Path
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/references';OUT.mkdir(parents=True,exist_ok=True)
ART=ROOT/'artifacts';ART.mkdir(exist_ok=True)
DATE='2026-10-14'
items=[]
def get(url):
 r=requests.get(url,timeout=60);r.raise_for_status();return r
def pdf(id,title,agency,date,page,url,scope):
 p=OUT/(id+'.pdf')
 raw=p.read_bytes() if p.exists() else get(url).content
 assert raw.startswith(b'%PDF'),(id,raw[:80]);p.write_bytes(raw)
 reader=PdfReader(p);tp=ART/(id+'-extracted.txt')
 text=tp.read_text(encoding='utf-8') if tp.exists() else '\n\n'.join(f'[원본 {i+1}쪽]\n'+(x.extract_text() or '') for i,x in enumerate(reader.pages))
 assert len(text)>300,(id,'text unavailable')
 tp=ART/(id+'-extracted.txt');tp.write_text(text,encoding='utf-8')
 items.append(dict(id=id,title=title,agency=agency,published=date,effective=None,checked=DATE,sourceUrl=page,directUrl=url,scope=scope,format='PDF',localPath=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),pages=len(reader.pages),textChars=len(text),versionStatus='2026학년도 공개본',redistribution='공개 공식 원본; 개인정보/권리 검토 전',notes='표·양식은 원본 PDF와 대조'))
 print(id,len(reader.pages),len(text))
def law(id,title,kind,seq,scope):
 query='lsiSeq' if kind=='ls' else ('admRulSeq' if kind=='admRulLs' else 'ordinSeq')
 url=f'https://www.law.go.kr/LSW/{kind}InfoR.do?{query}={seq}&chrClsCd=010202'
 if kind=='ls':url+='&urlMode=lsInfoP&efYd='+('20260219' if seq=='283357' else '20260911')
 elif kind=='admRulLs':url+='&joTpYn=Y&languageType=KO'
 # Administrative-rule endpoint is admRulLsInfoR.do.
 r=get(url);r.encoding='utf-8';s=bs4.BeautifulSoup(r.text,'html.parser')
 body=s.select_one('#contentBody') or s.select_one('.contentBody') or s
 for n in body(['script','style','input','select','button']):n.decompose()
 for n in body.select('.btn, .lawbtn'):n.decompose()
 text=body.get_text('\n',strip=True)
 text=re.sub(r'\n{3,}','\n\n',text)
 assert title.replace(' ','') in text.replace(' ',''),(id,text[:150])
 assert '제1조' in text and '부칙' in re.sub(r'\s+','',text),(id,'missing body')
 page=f'https://www.law.go.kr/LSW/{"admRulInfoP" if kind=="admRulLs" else kind+"InfoP"}.do?{query}={seq}&chrClsCd=010202'
 note=f'{title}\n공식 원문 HTML 본문 추출본 (TXT). 원본 파일 또는 공식 PDF가 아닙니다.\n출처: 법제처 국가법령정보센터\n원문: {page}\n조회기준: {DATE}\n본문과 부칙을 포함합니다. 별표·별지 첨부파일은 이 TXT에 포함되지 않으며 원문에서 별도 확인해야 합니다.\n실제 업무 적용 전 현행 원문과 시행일을 확인하세요.\n\n'
 p=OUT/(id+'.txt');p.write_text(note+text,encoding='utf-8')
 raw=ART/(id+'-source.html');raw.write_text(r.text,encoding='utf-8')
 header=s.get_text(' ',strip=True)[:500]
 dates=re.findall(r'\[시행 ([^\]]+)\]',header)
 items.append(dict(id=id,title=title,agency='법제처 국가법령정보센터 / 교육부' if kind!='ordin' else '법제처 국가법령정보센터 / 부산광역시교육청',published=None,effective=dates[0] if dates else None,checked=DATE,sourceUrl=page,directUrl=None,scope=scope,format='TXT (공식 HTML 본문 추출)',localPath=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size,textChars=len(text),versionStatus='공식 현행 연결 확인',redistribution='법령·행정규칙 본문',notes='본문과 부칙 추출; 별표/별지는 원문에서 별도 확인',heading=header[:250]))
 print(id,len(text),dates)

pdf('school-rules-2026','2026학년도 부산보건고등학교 학교규정집','부산보건고등학교','2026-07-25','https://school.busanedu.net/busanhc.com/na/ntt/selectNttInfo.do?mi=1053507&nttSn=53735975','https://school.busanedu.net/common/nttFileDownload.do?fileKey=b33ad6fb0025819f68683b488028f82c','부산보건고등학교 학칙 및 학교 규정')
pdf('school-rules-amendments-2026','2026학년도 부산보건고등학교 학교규정 개정 사항','부산보건고등학교','2026-07-25','https://school.busanedu.net/busanhc.com/na/ntt/selectNttInfo.do?mi=1053507&nttSn=53735975','https://school.busanedu.net/common/nttFileDownload.do?fileKey=5d5e0ed2646be855385039674f13b3c4','부산보건고등학교 2026 학교규정 개정 비교')
pdf('busan-assessment-2026','2026학년도 고등학교 학업성적관리 시행지침','부산광역시교육청','2026-02','https://www.pen.go.kr/upload/dep07/na/bbs_2629/ntt_1164293/doc_dc66vf893%3D7fvf3%3D45vbd%3D92v0e%3D15bbvdd97vf056_v9335.pdf','https://www.pen.go.kr/upload/dep07/na/bbs_2629/ntt_1164293/doc_dc66vf893%3D7fvf3%3D45vbd%3D92v0e%3D15bbvdd97vf056_v9335.pdf','부산광역시 고등학교 학업성적관리')
pdf('busan-schooltrip-2026','2026학년도 수학여행·수련활동 등 현장체험학습 운영 매뉴얼','부산광역시교육청','2026-02-10','https://home.pen.go.kr/schooltrip/na/ntt/selectNttInfo.do?mi=17289&nttSn=967285','https://home.pen.go.kr/common/nttFileDownload.do?fileKey=9ae35155499f364f8010b53df54c8c1e','부산광역시 학교 현장체험학습 업무')
law('elementary-secondary-education-act','초ㆍ중등교육법','ls','283903','초·중등교육의 학교·교원·학칙·학교생활기록 등')
law('elementary-secondary-education-enforcement','초ㆍ중등교육법 시행령','ls','289439','초·중등교육법 시행에 필요한 사항')
law('personal-information-protection-act','개인정보 보호법','ls','283839','개인정보 처리 전반; 학교 업무 자료의 처리 조건 확인')
law('teacher-status-protection-act','교원의 지위 향상 및 교육활동 보호를 위한 특별법','ls','283357','교원의 지위 및 교육활동 보호')
law('school-record-guideline','학교생활기록 작성 및 관리지침','admRulLs','2100000274694','학교생활기록 작성·관리; 별표·별지 별도 확인')
law('student-guidance-notice','교원의 학생생활지도에 관한 고시','admRulLs','2100000275094','학생생활지도 범위·방식 등')
law('busan-teacher-protection-ordinance','부산광역시교육청 교원의 교육활동 보호에 관한 조례','ordin','2145173','부산광역시교육청 교육활동 보호')
(ART/'public-sources.json').write_text(json.dumps(dict(checked=DATE,sources=items),ensure_ascii=False,indent=2),encoding='utf-8')

import concurrent.futures, hashlib, json, pathlib, subprocess, sys
import requests
ROOT=pathlib.Path(__file__).resolve().parent.parent
BASE='https://zeusk302-png.github.io/teacher-ai-workshop/'
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
files=[p for p in (ROOT/'docs').rglob('*') if p.is_file() and p.name!='notebooklm-public-sources-2026-10-14.zip']
def verify(p):
    rel=p.relative_to(ROOT/'docs').as_posix()
    response=requests.get(BASE+rel+'?v='+commit,timeout=40)
    local=hashlib.sha256(p.read_bytes()).hexdigest()
    remote=hashlib.sha256(response.content).hexdigest()
    return dict(file=rel,status=response.status_code,bytes=len(response.content),matches=local==remote,sha256=remote)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(verify,files))
report=dict(url=BASE,commit=commit,checked='2026-10-14',allMatch=all(r['status']==200 and r['matches'] for r in results),files=results)
(ROOT/'artifacts').mkdir(exist_ok=True)
(ROOT/'artifacts/deployment-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(url=BASE,commit=commit,verifiedFiles=len(results),allMatch=report['allMatch'],failures=[r for r in results if r['status']!=200 or not r['matches']]),ensure_ascii=False))
sys.exit(0 if report['allMatch'] else 1)

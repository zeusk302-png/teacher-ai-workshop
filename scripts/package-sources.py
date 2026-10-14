import json, pathlib, zipfile, csv
ROOT=pathlib.Path(__file__).resolve().parent.parent
manifest=json.loads((ROOT/'artifacts/public-sources.json').read_text(encoding='utf-8-sig'))
(ROOT/'docs/references/source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
out=ROOT/'docs/downloads';out.mkdir(exist_ok=True)
with zipfile.ZipFile(out/'public-source-pack.zip','w',zipfile.ZIP_DEFLATED) as z:
    for s in manifest['sources']:
        p=ROOT/s['localPath'];z.write(p,p.name)
    z.write(ROOT/'docs/references/README.md','README.md')
    z.write(ROOT/'docs/references/source-manifest.json','source-manifest.json')
with (out/'practice-budget.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['항목','수량','단가','담당 부서','상태']);w.writerows([
        ['안내자료 인쇄',120,1000,'행사 준비팀','예정'],['간식',50,3000,'행사 준비팀','예정'],['체험 재료',20,4000,'행사 준비팀','예정'],['현수막',1,50000,'행사 준비팀','예정']])
(out/'practice-budget-README.txt').write_text('교사 AI 연수용 가상 예산 자료\n실제 학교 예산이나 학생 정보가 아닙니다.\n예산 상한 500000원\n예상 합계 400000원\n예상 잔액 100000원\n수량×단가와 합계를 Excel 수식으로 직접 확인하세요.\n',encoding='utf-8')
print('Packaged',len(manifest['sources']),'public sources')

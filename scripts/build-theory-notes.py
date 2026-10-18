"""Embed the shared lecture notes as static, readable HTML in the six theory tabs."""
import json, re
from pathlib import Path
from html import escape

root = Path(__file__).resolve().parents[1]
notes = json.loads((root / 'docs/content/rag-theory.json').read_text(encoding='utf-8'))
page = root / 'docs/index.html'
html = page.read_text(encoding='utf-8')
html = re.sub(r'<!-- theory-notes-\d+:start -->.*?<!-- theory-notes-\d+:end -->', '', html, flags=re.S)
for i, chapter in enumerate(notes):
    blocks = ''.join('<section><h4>' + escape(s['title']) + '</h4>' + ''.join('<p>' + escape(p) + '</p>' for p in s['paragraphs']) + '</section>' for s in chapter['sections'])
    sources = ' · '.join('<a href="' + escape(url) + '" target="_blank" rel="noopener noreferrer">' + escape(label) + '</a>' for label, url in chapter['sources'])
    source_note = '<p class="concept-source">참고: ' + sources + ' · 학교 업무 예시와 진행 방식은 연수용으로 구성했습니다.</p>' if sources else '<p class="concept-source">이번 연수의 실습 설계와 2026.10.18. 사전 테스트를 설명한 내용입니다.</p>'
    block = f'<!-- theory-notes-{i}:start --><details class="theory-notes"><summary><span>심화 설명</span>{escape(chapter["title"])}</summary><div class="theory-reading">{blocks}{source_note}</div></details><!-- theory-notes-{i}:end -->'
    pattern = r'(<article[^>]+id="concept-panel-' + str(i) + r'".*?)(</article>)'
    html, count = re.subn(pattern, lambda m: m[1] + block + m[2], html, count=1, flags=re.S)
    assert count == 1, i
page.write_bytes(html.encode('utf-8'))
print(f'Embedded {len(notes)} theory chapters / {sum(len(c["sections"]) for c in notes)} sections')

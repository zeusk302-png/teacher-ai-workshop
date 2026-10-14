'use strict';
(() => {
  const checks=[...document.querySelectorAll('[data-document-check]')],key='teacher-ai-document-check-v1';
  let saved=[];try{saved=JSON.parse(localStorage.getItem(key)||'[]');if(!Array.isArray(saved))saved=[];}catch{}
  checks.forEach(c=>{c.checked=saved.includes(c.dataset.documentCheck);c.addEventListener('change',update);});
  function update(){const done=checks.filter(c=>c.checked).map(c=>c.dataset.documentCheck);document.getElementById('document-progress').textContent=`${done.length} / 4 항목 완료`;try{localStorage.setItem(key,JSON.stringify(done));}catch{}}
  update();
  document.querySelector('[data-workflow-copy]').addEventListener('click',async()=>{const text=document.getElementById('file-request').textContent,status=document.getElementById('workflow-copy-status');try{await navigator.clipboard.writeText(text);status.textContent='요청을 복사했습니다.';}catch{const range=document.createRange();range.selectNodeContents(document.getElementById('file-request'));const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);status.textContent='요청을 선택했습니다. Ctrl+C 또는 복사 메뉴를 사용하세요.';}});
})();

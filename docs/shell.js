'use strict';
(() => {
 const $=s=>document.querySelector(s),guide=document.body.classList.contains('guide-page');
 const sidebar=$('#course-sidebar'),toggle=$('.menu-toggle'),close=$('.menu-close'),backdrop=$('.menu-backdrop');
 if(!sidebar||!toggle)return;
 let returnFocus=null;
 function menu(open){if(open)returnFocus=document.activeElement;document.body.classList.toggle('menu-open',open);toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'연수 목차 닫기':'연수 목차 열기');backdrop.hidden=!open;if(open)close.focus();else if(returnFocus)returnFocus.focus();}
 toggle.addEventListener('click',()=>menu(toggle.getAttribute('aria-expanded')!=='true'));close.addEventListener('click',()=>menu(false));backdrop.addEventListener('click',()=>menu(false));
 document.addEventListener('keydown',e=>{if(toggle.getAttribute('aria-expanded')!=='true')return;if(e.key==='Escape'){e.preventDefault();menu(false);}if(e.key==='Tab'){const focusable=[...sidebar.querySelectorAll('button,a,summary')].filter(el=>el.getClientRects().length);const first=focusable[0],last=focusable.at(-1);if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}}});
 sidebar.addEventListener('click',e=>{if(e.target.closest('a')&&toggle.getAttribute('aria-expanded')==='true')menu(false);});
 const names=['home','concepts','materials','tools','notebook','skills','studio','schedule','resources'];
 function route(){if(guide)return;let target=location.hash.slice(1)||'home';if(target==='main')return;if(target==='top')target='home';if(!names.includes(target))target='home';document.querySelectorAll('.view').forEach(el=>el.hidden=el.id!==target);document.querySelectorAll('[data-header-view]').forEach(a=>{a.removeAttribute('aria-current');if(a.dataset.headerView===target)a.setAttribute('aria-current','page');});document.querySelectorAll('[data-nav-href]').forEach(a=>{a.removeAttribute('aria-current');if(a.dataset.navHref==='index.html#'+target){a.setAttribute('aria-current','page');const group=a.closest('details');if(group)group.open=true;}});document.title=($('#'+target+' h1')?.innerText.replace(/\s+/g,' ')||'연수 홈')+' · 부산보건고 교사 AI 연수';window.scrollTo({top:0,behavior:'instant'});}
 if(!guide){document.querySelectorAll('a[href^="index.html#"]').forEach(a=>{a.setAttribute('href',a.getAttribute('href').replace('index.html',''));});window.addEventListener('hashchange',route);route();}
 window.addEventListener('resize',()=>{if(window.innerWidth>820&&toggle.getAttribute('aria-expanded')==='true')menu(false);});
})();

'use strict';
(() => {
  const tabs = [...document.querySelectorAll('.concept-tabs [role="tab"]')];
  if (!tabs.length) return;
  const panels = [...document.querySelectorAll('.concept-panel')];
  const prev = document.querySelector('#concept-prev');
  const next = document.querySelector('#concept-next');
  const practice = document.querySelector('#concept-practice');
  let current = 0;
  function show(index, focusTab = false) {
    current = Math.max(0, Math.min(tabs.length - 1, index));
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === current));
      tab.tabIndex = i === current ? 0 : -1;
      panels[i].hidden = i !== current;
    });
    prev.disabled = current === 0;
    next.hidden = current === tabs.length - 1;
    practice.hidden = current !== tabs.length - 1;
    document.querySelector('#concept-counter').textContent = `${current + 1} / ${tabs.length}`;
    if (focusTab) tabs[current].focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => show(index));
    tab.addEventListener('keydown', event => {
      let target;
      if (event.key === 'ArrowRight') target = (index + 1) % tabs.length;
      else if (event.key === 'ArrowLeft') target = (index + tabs.length - 1) % tabs.length;
      else if (event.key === 'Home') target = 0;
      else if (event.key === 'End') target = tabs.length - 1;
      else return;
      event.preventDefault();
      show(target, true);
    });
  });
  prev.addEventListener('click', () => show(current - 1, true));
  next.addEventListener('click', () => show(current + 1, true));
  show(0);
})();

/*
 * Egg Guide — page behaviour. Plain JavaScript, no dependencies.
 * All content is static HTML (so it works without JavaScript and is easy to edit in index.html).
 * Theme logic lives in themes.js and switcher.js. This file only handles the mobile menu,
 * the current-section highlight in the navigation, and the footer year.
 */
'use strict';

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

function initMenu() {
  const btn = $('#menu-btn'), nav = $('#main-nav'), desktop = window.matchMedia('(min-width: 62em)');
  const sync = () => nav.toggleAttribute('inert', !desktop.matches && !nav.classList.contains('open'));
  function set(open, back) {
    nav.classList.toggle('open', open); btn.setAttribute('aria-expanded', String(open)); btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.classList.toggle('sheet-open', open); sync();
    if (open) nav.querySelector('a').focus(); else if (back) btn.focus();
  }
  sync();
  btn.addEventListener('click', () => set(!nav.classList.contains('open')));
  nav.addEventListener('click', (e) => { if (e.target.closest('a')) set(false); });
  document.addEventListener('keydown', (e) => {
    if (!nav.classList.contains('open')) return;
    if (e.key === 'Escape') set(false, true);
    if (e.key === 'Tab') { const items = [btn, ...$$('a', nav)], f = items[0], l = items[items.length - 1]; if (e.shiftKey && document.activeElement === f) { e.preventDefault(); l.focus(); } else if (!e.shiftKey && document.activeElement === l) { e.preventDefault(); f.focus(); } }
  });
  desktop.addEventListener('change', () => { if (desktop.matches) { nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false'); document.body.classList.remove('sheet-open'); } sync(); });
}

function initActiveNav() {
  if (!('IntersectionObserver' in window)) return;
  const links = $$('#main-nav a[href^="#"]');
  const io = new IntersectionObserver((es) => es.forEach((en) => { if (en.isIntersecting) links.forEach((a) => (a.getAttribute('href') === `#${en.target.id}` ? a.setAttribute('aria-current', 'true') : a.removeAttribute('aria-current'))); }), { rootMargin: '-45% 0px -50% 0px' });
  links.map((a) => $(a.getAttribute('href'))).filter(Boolean).forEach((s) => io.observe(s));
  const clear = new IntersectionObserver(([en]) => { if (en.isIntersecting) links.forEach((a) => a.removeAttribute('aria-current')); }, { rootMargin: '-45% 0px -50% 0px' });
  clear.observe($('#top')); const src = $('#sources'); if (src) clear.observe(src);
}

$('#year').textContent = new Date().getFullYear();
initMenu();
initActiveNav();

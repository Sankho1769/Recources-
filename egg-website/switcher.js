/*
 * switcher.js: the theme picker UI. Used on every page (index.html, 404.html).
 * Reads and writes the theme only through window.PortfolioTheme (themes.js), so there is one source of truth.
 * Desktop: a compact popover under the button. Small screens: a bottom sheet that scrolls internally.
 * Markup is a native radio group, so arrow keys, Tab and screen readers work without custom key handling.
 */
(function () {
  'use strict';
  var PT = window.PortfolioTheme;
  var slot = document.getElementById('theme-slot');
  if (!PT || !slot) return;

  var mobile = window.matchMedia('(max-width: 47.99em)');
  function name(id) { return PT.themes.filter(function (t) { return t.id === id; })[0].name; }
  function dots(t) { return '<span class="swatches" aria-hidden="true">' + t.colors.map(function (c) { return '<i style="background:' + c + '"></i>'; }).join('') + '</span>'; }

  slot.innerHTML =
    '<button type="button" class="theme-btn" id="theme-btn" aria-haspopup="dialog" aria-expanded="false" aria-controls="theme-panel">' +
      '<span id="theme-btn-dots"></span><span class="theme-btn-label">Theme</span></button>';

  var panel = document.createElement('div');
  panel.id = 'theme-panel'; panel.className = 'theme-panel'; panel.hidden = true;
  panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-labelledby', 'theme-title');
  panel.innerHTML =
    '<div class="theme-head"><h2 id="theme-title">Colour theme</h2><button type="button" class="theme-close" id="theme-close" aria-label="Close theme menu">Close</button></div>' +
    '<fieldset class="theme-list"><legend class="sr">Choose a colour theme. Changes apply instantly.</legend>' +
    PT.themes.map(function (t) {
      return '<label class="theme-opt"><input type="radio" name="theme" value="' + t.id + '">' + dots(t) +
             '<span class="theme-name">' + t.name + '</span><span class="theme-check" aria-hidden="true">&#10003;</span></label>';
    }).join('') + '</fieldset>';
  var backdrop = document.createElement('div');
  backdrop.className = 'theme-backdrop'; backdrop.hidden = true; backdrop.setAttribute('aria-hidden', 'true');
  document.body.appendChild(backdrop);
  document.body.appendChild(panel);

  var btn = document.getElementById('theme-btn'), btnDots = document.getElementById('theme-btn-dots');

  function sync() {
    var id = PT.get(), t = PT.themes.filter(function (x) { return x.id === id; })[0];
    btnDots.innerHTML = dots(t);
    btn.setAttribute('aria-label', 'Colour theme: ' + t.name + '. Open theme menu');
    Array.prototype.forEach.call(panel.querySelectorAll('input'), function (i) { i.checked = i.value === id; });
  }
  PT.onChange(sync); sync();

  function place() {
    if (mobile.matches) { panel.style.removeProperty('--tp-top'); panel.style.removeProperty('--tp-right'); return; }
    var r = btn.getBoundingClientRect();
    panel.style.setProperty('--tp-top', Math.round(r.bottom + 8) + 'px');
    panel.style.setProperty('--tp-right', Math.max(8, Math.round(window.innerWidth - r.right)) + 'px');
  }
  function open() {
    place(); panel.hidden = false; backdrop.hidden = !mobile.matches;
    btn.setAttribute('aria-expanded', 'true');
    if (mobile.matches) document.body.classList.add('sheet-open');
    var checked = panel.querySelector('input:checked');
    (checked || panel.querySelector('input')).focus({ preventScroll: true });
    if (checked && checked.scrollIntoView) checked.closest('.theme-opt').scrollIntoView({ block: 'nearest' });
  }
  function close(returnFocus) {
    if (panel.hidden) return;
    panel.hidden = true; backdrop.hidden = true; btn.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('sheet-open');
    if (returnFocus) btn.focus();
  }

  btn.addEventListener('click', function () { panel.hidden ? open() : close(true); });
  document.getElementById('theme-close').addEventListener('click', function () { close(true); });
  backdrop.addEventListener('click', function () { close(true); });
  panel.addEventListener('change', function (e) { if (e.target.name === 'theme') PT.set(e.target.value); });
  document.addEventListener('keydown', function (e) {
    if (panel.hidden) return;
    if (e.key === 'Escape') { e.preventDefault(); close(true); return; }
    if (e.key === 'Tab') {                       // keep focus inside the open menu
      var f = [].slice.call(panel.querySelectorAll('input:checked, .theme-close'));
      var first = panel.querySelector('.theme-close'), last = panel.querySelector('input:checked') || first;
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      void f;
    }
  });
  document.addEventListener('pointerdown', function (e) {
    if (!panel.hidden && !mobile.matches && !panel.contains(e.target) && !btn.contains(e.target)) close(false);
  });
  window.addEventListener('resize', function () { if (!panel.hidden) { place(); backdrop.hidden = !mobile.matches; document.body.classList.toggle('sheet-open', mobile.matches); } });
})();

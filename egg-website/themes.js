/*
 * themes.js: the single source of truth for the colour themes.
 *
 * Loaded synchronously in <head> on every page, BEFORE first paint, so the saved theme is applied
 * without a flash. It (1) defines the 12 presets, (2) derives every design token from a few seed
 * colours (guaranteeing readable contrast), (3) injects one <style> block with all themes as CSS
 * custom properties, and (4) sets <html data-theme="...">.
 *
 * To add a theme: add one entry to THEMES. Nothing else needs to change.
 * Seed fields: bg, text, accent are required. Optional: surface, link, highlight.
 * `colors` are the three printed palette swatches shown in the picker.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'portfolio-theme';
  var DEFAULT_ID = 'ink-teal';

  var THEMES = [
    { id: 'aubergine-marigold', name: 'Aubergine & Marigold', mode: 'light', colors: ['#DDE3E8', '#3A0F34', '#EAAA00'], bg: '#DDE3E8', text: '#3A0F34', accent: '#EAAA00' },
    { id: 'creative-pop',       name: 'Creative Pop',         mode: 'light', colors: ['#CBB3E8', '#D4FF3F', '#E34234'], bg: '#CBB3E8', text: '#1E1236', accent: '#E34234', highlight: '#D4FF3F' },
    { id: 'emerald-vermilion',  name: 'Emerald & Vermilion',  mode: 'light', colors: ['#F9EBD7', '#046A38', '#E34222'], bg: '#F9EBD7', text: '#046A38', accent: '#E34222' },
    { id: 'cobalt-red',         name: 'Cobalt & Red',         mode: 'dark',  colors: ['#021861', '#255DCE', '#DE1110'], bg: '#021861', text: '#F3F5FF', accent: '#DE1110', surface: '#0B2A7E', link: '#9DB8FF' },
    { id: 'earth-amber',        name: 'Earth & Amber',        mode: 'dark',  colors: ['#090907', '#6C5636', '#B99D73'], bg: '#090907', text: '#EFE6D6', accent: '#B99D73', surface: '#1C1710' },
    { id: 'ink-teal',           name: 'Ink & Teal',           mode: 'dark',  colors: ['#031211', '#E8E4D3', '#00AEBB'], bg: '#031211', text: '#E8E4D3', accent: '#00AEBB' },
    { id: 'royal-blue',         name: 'Royal Blue',           mode: 'dark',  colors: ['#20309A', '#FFFFFF', '#BB232B'], bg: '#20309A', text: '#FFFFFF', accent: '#BB232B', link: '#FFFFFF' },
    { id: 'porcelain-lemon',    name: 'Porcelain & Lemon',    mode: 'light', colors: ['#F3E6D7', '#9B7ED6', '#E4FF3B'], bg: '#F3E6D7', text: '#2B1D52', accent: '#E4FF3B', link: '#9B7ED6', highlight: '#E4FF3B' },
    { id: 'forest-crimson',     name: 'Forest & Crimson',     mode: 'dark',  colors: ['#171717', '#06110C', '#A31C1B'], bg: '#06110C', text: '#EDEFEA', accent: '#A31C1B', surface: '#171717' },
    { id: 'pink-lemon',         name: 'Pink & Lemon',         mode: 'light', colors: ['#F43F91', '#FFFFFF', '#FFE51A'], bg: '#FFFFFF', text: '#2B0A1B', accent: '#F43F91', highlight: '#FFE51A' },
    { id: 'orchid-orange',      name: 'Orchid & Orange',      mode: 'light', colors: ['#E7B0DE', '#400849', '#FF5A0A'], bg: '#E7B0DE', text: '#400849', accent: '#FF5A0A' },
    { id: 'midnight-lime',      name: 'Midnight & Lime',      mode: 'dark',  colors: ['#030407', '#1558C9', '#D4FF24'], bg: '#030407', text: '#F2F4FA', accent: '#D4FF24', surface: '#0A1230' }
  ];

  /* ---------- colour helpers ---------- */
  function rgb(h) { h = h.replace('#', ''); return [parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]; }
  function hex(c) { return '#' + c.map(function (v) { return ('0' + Math.max(0, Math.min(255, Math.round(v))).toString(16)).slice(-2); }).join('').toUpperCase(); }
  function mix(a, b, t) { var x = rgb(a), y = rgb(b); return hex([x[0] + (y[0] - x[0]) * t, x[1] + (y[1] - x[1]) * t, x[2] + (y[2] - x[2]) * t]); }
  function lum(h) { return rgb(h).map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }).reduce(function (s, v, i) { return s + v * [0.2126, 0.7152, 0.0722][i]; }, 0); }
  function contrast(a, b) { var l1 = lum(a), l2 = lum(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); }
  /* Nudge `fg` away from `bg` (towards white on dark, black on light) until it reaches `min` contrast. */
  function ensure(fg, bg, min) {
    var target = contrast('#FFFFFF', bg) >= contrast('#000000', bg) ? '#FFFFFF' : '#000000', i = 0;
    while (contrast(fg, bg) < min && i++ < 30) fg = mix(fg, target, 0.08);
    return fg;
  }
  /* Tint `bg` towards `tint` as strongly as possible (<= max) while `fg` text stays readable on it. */
  function tint(bg, tintColor, fg, max, min) {
    var t = max;
    while (t > 0 && contrast(fg, mix(bg, tintColor, t)) < min) t -= 0.04;
    return mix(bg, tintColor, Math.max(t, 0));
  }
  function best(bg, candidates, min) {
    for (var i = 0; i < candidates.length; i++) if (contrast(candidates[i], bg) >= min) return candidates[i];
    return contrast('#000000', bg) > contrast('#FFFFFF', bg) ? '#000000' : '#FFFFFF';
  }

  /* ---------- token derivation ---------- */
  function derive(t) {
    var dark = t.mode === 'dark';
    var bg = t.bg, text = t.text, accent = t.accent;
    var surface = t.surface || mix(bg, text, dark ? 0.06 : 0.05);
    var surface2 = mix(surface, text, dark ? 0.07 : 0.06);
    var text2 = ensure(mix(text, bg, 0.3), surface2, 4.6);
    var band = dark ? surface2 : text;
    var onBand = dark ? text : bg;
    var tokens = {
      'color-scheme': dark ? 'dark' : 'light',
      '--bg': bg,
      '--surface': surface,
      '--surface-2': surface2,
      '--text': text,
      '--text-2': text2,
      '--line': mix(bg, text, 0.2),
      '--line-strong': ensure(mix(bg, text, 0.5), surface, 3),
      '--accent': accent,
      '--on-accent': best(accent, [bg, text, '#000000', '#FFFFFF'], 4.5),
      '--accent-edge': contrast(accent, bg) >= 3 ? accent : text,
      '--accent-soft': tint(bg, accent, text, dark ? 0.18 : 0.2, 4.5),
      '--link': ensure(t.link || accent, surface2, 4.5),
      '--focus': ensure(t.link || accent, surface, 3),
      '--highlight': tint(bg, t.highlight || accent, text, 0.55, 4.5),
      '--band': band,
      '--on-band': onBand,
      '--band-2': ensure(mix(onBand, band, 0.3), band, 4.6),
      '--band-line': ensure(mix(band, onBand, 0.5), band, 3),
      '--band-accent': ensure(accent, band, 4.5),
      '--shadow': dark ? 'rgba(0,0,0,.5)' : 'rgba(0,0,0,.14)'
    };
    return tokens;
  }

  function css() {
    return THEMES.map(function (t) {
      var d = derive(t), body = Object.keys(d).map(function (k) { return k + ':' + d[k]; }).join(';');
      return 'html[data-theme="' + t.id + '"]{' + body + '}';
    }).join('\n');
  }

  function find(id) { for (var i = 0; i < THEMES.length; i++) if (THEMES[i].id === id) return THEMES[i]; return null; }
  function read() { try { return window.localStorage.getItem(STORAGE_KEY); } catch (e) { return null; } }
  function write(id) { try { window.localStorage.setItem(STORAGE_KEY, id); } catch (e) { /* storage unavailable: the choice just won't persist */ } }

  document.documentElement.classList.add('js');   // enables JS-only layout (mobile menu, theme picker)
  var current = (find(read()) || find(DEFAULT_ID)).id;
  var listeners = [];

  function apply(id) {
    var t = find(id) || find(DEFAULT_ID);
    current = t.id;
    var root = document.documentElement;
    root.classList.add('no-tx');                       // a theme change must be instant: suppress colour transitions for a moment
    root.setAttribute('data-theme', t.id);
    setTimeout(function () { root.classList.remove('no-tx'); }, 120);
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', derive(t)['--bg']);
  }

  var style = document.createElement('style');
  style.id = 'theme-tokens';
  style.textContent = css();
  document.head.appendChild(style);
  apply(current);

  window.PortfolioTheme = {
    themes: THEMES,
    defaultId: DEFAULT_ID,
    get: function () { return current; },
    set: function (id) {
      if (!find(id)) return;
      apply(id); write(id);
      listeners.forEach(function (fn) { fn(current); });
    },
    onChange: function (fn) { listeners.push(fn); },
    derive: derive,
    contrast: contrast
  };

  // Keep several open tabs in sync.
  window.addEventListener('storage', function (e) {
    if (e.key === STORAGE_KEY && find(e.newValue)) { apply(e.newValue); listeners.forEach(function (fn) { fn(current); }); }
  });
})();

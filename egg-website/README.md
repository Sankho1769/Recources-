# Egg Guide

An informational website about eggs: what they are, the main types, nutrition, how eggs fit into a balanced diet, how to choose and store them safely, simple recipes, and common questions.
Plain **HTML, CSS and vanilla JavaScript**: no framework, no npm, no build step, no external requests (system fonts only).

This site was converted from a developer portfolio. The layout, design system, **12-theme switcher** and responsive behaviour were preserved; only the content and imagery changed.

## Run it
Double-click `index.html` (or `START_EGG_GUIDE.bat` on Windows). Works offline. To publish, upload the folder to any static host (GitHub Pages, Netlify, Cloudflare Pages).

## Files
| File | Purpose |
| --- | --- |
| `index.html` | **All content** (hero, sections, recipes, FAQ, sources) plus the hidden SVG illustration sprite |
| `style.css` | Layout and components. Colours come only from theme tokens |
| `themes.js` | The 12 themes: single source of truth, token derivation, persistence (unchanged) |
| `switcher.js` | Theme picker UI, used on every page (unchanged) |
| `script.js` | Mobile menu, current-section highlight, footer year |
| `404.html` | Not-found page, with the shared header and theme switcher |
| `assets/og-image.png`, `favicon.svg` | Social preview and icon |
| `docs/PRD.md`, `docs/SRS.md` | Product and software requirements, with traceability to tests and a list of what was not tested |
| `tests/browser_tests.py` | Optional Playwright tests (see below) |

## Edit the content
Everything is plain HTML in `index.html`, one `<section>` per topic.
- **Recipes:** copy an `<article class="project">` inside `#recipes`. Each has a figure, name, summary, a `stack` list for serves/time, and a `<details class="more">` with ingredients and method.
- **FAQ:** add a `<details><summary>Question</summary><div class="answer">…</div></details>` inside `.faq`.
- **Nutrition table:** edit the `<table class="data-table">`. If you change numbers, keep the caption's serving size and update the source note. Do not add numbers you cannot source.
- **Illustrations:** original SVG symbols in the sprite at the top of `<body>`; use them with `<svg role="img" aria-label="…" viewBox="…" width=".." height=".."><use href="#ill-name"/></svg>`. Selectors for illustration colours in `style.css` must **not** be scoped under a parent class (SVG `<use>` content has no such ancestor). Always keep `aria-label` text descriptive.
- **Brand name:** "Egg Guide" is a working title. Change it in the header, footer, `<title>` and `404.html`.

## Themes (unchanged)
Twelve presets: Aubergine & Marigold, Creative Pop, Emerald & Vermilion, Cobalt & Red, Earth & Amber, **Ink & Teal (default)**, Royal Blue, Porcelain & Lemon, Forest & Crimson, Pink & Lemon, Orchid & Orange, Midnight & Lime.
`themes.js` derives every design token (including accessible text, link and focus colours) from a few seed colours per theme and applies one `data-theme` attribute. The choice is saved in `localStorage` (key `portfolio-theme`, kept so existing visitors' saved themes still work) and applied before first paint. To add a theme, add one object to `THEMES`.

## Sources and content notes
- Nutrition values: USDA FoodData Central, "Egg, whole, raw, fresh" (per 100 g); per-egg values are calculated for a 50 g large egg and labelled as such. Please re-check against FoodData Central before publishing; USDA datasets differ slightly.
- Storage and safety: USDA Food Safety and Inspection Service guidance.
- The site gives general information and is not medical advice.
- Illustrations are original artwork, not photographs. If you add photographs, record their source and licence.

## Tests (optional)
```
pip install playwright pillow
playwright install chromium
python tests/browser_tests.py
```
Runs checks on a temporary copy (your files are never changed): themes and persistence, responsive overflow at 12 widths, contrast in all 12 themes, the mobile theme sheet, menu, content, recipes, FAQ, illustrations (including a pixel check that artwork is not cropped), reduced motion and no-JavaScript. Add `--json results.json` to save results or `--shots dir/` to save screenshots.

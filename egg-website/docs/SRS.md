# Software Requirements Specification (SRS)

**Product:** Egg Guide — an informational website about eggs
**Version:** 1.0  |  **Date:** 29 October 2026  |  **Status:** Draft for owner review
**Companion document:** [PRD.md](PRD.md)

---

## 1. Introduction
### 1.1 Purpose
This document specifies what the Egg Guide website shall do, the constraints it must meet, and how each requirement is verified.

### 1.2 Scope
A static, single-page website (plus a 404 page) that teaches visitors about eggs: what they are, the main types, nutrition, balanced-diet context, choosing and storing eggs safely, simple recipes and common questions. It includes a site-wide colour-theme system with 12 presets. It has **no backend, database, accounts, analytics or contact form**. The site was converted from a developer portfolio; the layout, design system, theme system and responsive behaviour were preserved.

### 1.3 Definitions
| Term | Meaning |
| --- | --- |
| Theme | One of 12 colour presets applied through design tokens |
| Design token | A CSS custom property such as `--bg` or `--accent`; all stylesheet colours use tokens |
| Illustration | An original SVG drawing in the page's hidden sprite, shown through `<use>` |
| Implemented | Present in the code |
| Verified | Implemented **and** covered by automated checks that passed in the recorded run (section 6) |
| Partially verified / Not measured | Exercised only in part, or not measured; see the Verification column |
| Planned | Not built |

### 1.4 References
`docs/PRD.md`; USDA FoodData Central (nutrition values); USDA FSIS "Shell Eggs from Farm to Table" (storage and safety); WCAG 2.x contrast thresholds; the owner's palette screenshots, graphic-style list and layout guide.

---

## 2. Overall description
### 2.1 Product perspective
A self-contained static site in HTML, CSS and vanilla JavaScript. It depends on no framework, package manager, build step, server or third-party service. Content is static HTML, so it is readable without JavaScript.

### 2.2 Users
Home cooks, curious shoppers, learners and parents, and the site owner who edits `index.html`.

### 2.3 Operating environment
Modern evergreen browsers supporting CSS custom properties, `color-mix()`, `:has()`, SVG `<use>`, and `localStorage`. **Tested only in headless Chromium.**

### 2.4 Constraints
HTML5, CSS3 and vanilla JavaScript only; opens from disk; preserve the existing design, layout, theme system and responsiveness; no invented statistics; credible sources for numbers; no medical claims.

### 2.5 Assumptions
- No egg photography was available, so original illustrations were created. Real photos would require licensed images.
- The brand name "Egg Guide" is a working title chosen during conversion.
- Nutrition values were cross-checked during development against several third-party mirrors of USDA data; the primary USDA pages were not fetched directly (see section 8).

---

## 3. Functional requirements

Statuses are computed from the recorded test run (section 6).

| ID | Requirement | Priority | Status | Verification |
| --- | --- | --- | --- | --- |
| FR-NAV-01 | The page shall provide navigation links to About, Types, Nutrition, Benefits, Storage, Recipes and FAQ. Selecting a link shall scroll the section into view below the sticky header and mark that link as current (`aria-current`). | Must | **Verified** | Automated: seven section-navigation checks. (7 checks) |
| FR-NAV-02 | Below 62em the navigation shall be a menu opened by a button. Opening it shall move focus inside; Escape shall close it and return focus to the button; choosing a link shall close it; while closed it shall not be in the tab order. | Must | **Verified** | Automated: open / Escape / link checks with touch emulation at 390 px. (3 checks) |
| FR-NAV-03 | A "Skip to content" link shall be the first tab stop and move focus to the main content. A "Back to top" link shall appear in the footer. | Should | **Verified** | Automated: skip link on a fresh page load. Footer link inspected, not separately tested. (1 checks) |
| FR-CON-01 | The hero shall show the headline "The Simple Goodness of Eggs.", the supplied description, and two buttons: "Explore Eggs" (to Types) and "Discover Recipes" (to Recipes). | Must | **Verified** | Automated: exact text, button labels, link targets, and that the Recipes button scrolls to the section. (4 checks) |
| FR-CON-02 | The page shall contain: About eggs (what eggs are, how they are produced, why they are used in cooking); Types of eggs (chicken, duck, quail, and the free-range and organic labels) described without claims of nutritional superiority; Benefits (role in a balanced diet); Freshness and storage (selecting, reading the carton, storing, hygiene, safe cooking, leftovers); and a footer with links to every section. | Must | **Verified** | Automated: section headings, type names, footer links, and absence of superiority phrases (a keyword check, not proof). Accuracy of the prose was reviewed manually. (8 checks) |
| FR-CON-03 | The Nutrition section shall explain protein, fats, vitamins and minerals. Any specific value shall state its serving size and source, shall not be invented, and values derived by calculation shall be labelled as calculated. | Must | **Verified** | Automated: table caption states per 100 g and per large egg (50 g); USDA values present; source and "calculated" note beside the table; source links present. (4 checks) |
| FR-CON-04 | The Recipes section shall present five recipes (Boiled eggs, Omelette, Scrambled eggs, Egg curry, Egg sandwich). Each card shall have a name, a short description, an image with alternative text, and expandable ingredients and method that open and close. | Must | **Verified** | Automated: five cards, names, descriptions, images, and open/close behaviour of the details. (5 checks) |
| FR-CON-05 | The FAQ shall contain at least eight questions covering storage, freshness, cooking, varieties and nutrition, implemented as native disclosure elements operable by mouse, touch and keyboard. | Must | **Verified** | Automated: question count, click and keyboard operation, topic coverage keywords. (5 checks) |
| FR-CON-06 | Content shall not claim that eggs cure disease or guarantee health outcomes; it shall state that it is general information and not medical advice and point to doctors or dietitians for medical conditions or allergy; storage and safety guidance shall follow USDA FSIS (refrigerate at 4 °C / 40 °F or below). | Must | **Verified** | Automated: keyword checks for forbidden claim patterns, disclaimer text, USDA reference and the 4 °C (40 °F) figure. These are keyword checks; they cannot prove every sentence is accurate. (3 checks) |
| FR-CON-07 | No developer-portfolio content (names, projects, skills, GitHub or résumé references) shall remain on the page. | Must | **Verified** | Automated: absence of nine portfolio-related words in the rendered text. (1 checks) |
| FR-IMG-01 | Images shall be original SVG illustrations (no raster or external images). Each shall have `role="img"` and a descriptive `aria-label`, explicit width and height, and its artwork shall lie inside its frame. The hidden sprite shall be excluded from assistive technology. | Must | **Verified** | Automated: nine illustrations labelled and dimensioned; sprite `aria-hidden`; no `<img>` elements; pixel check that artwork is not cropped. (4 checks) |
| FR-THM-01 | The site shall offer exactly 12 themes, in this order: Aubergine & Marigold, Creative Pop, Emerald & Vermilion, Cobalt & Red, Earth & Amber, Ink & Teal, Royal Blue, Porcelain & Lemon, Forest & Crimson, Pink & Lemon, Orchid & Orange, Midnight & Lime, each showing its name and three swatches. | Must | **Verified** | Automated. (3 checks) |
| FR-THM-02 | A first-time visitor shall see Ink & Teal. | Must | **Verified** | Automated: attribute and `--bg` at `DOMContentLoaded`. (1 checks) |
| FR-THM-03 | Selecting a theme shall restyle the whole interface immediately without a reload and without colour transitions, and update the `theme-color` meta tag. | Must | **Verified** | Automated: all 12 themes produce distinct pages, stored values and meta colours. (1 checks) |
| FR-THM-04 | The theme shall persist in `localStorage` across reloads, in-page navigation and `index.html` / `404.html`, and be applied by a synchronous `<head>` script before first paint. | Must | **Verified** | Automated: reload, navigation and 404 round trip. "Before first paint" shown via `DOMContentLoaded` state, not frame capture. (4 checks) |
| FR-THM-05 | If storage is unavailable or holds an unknown value the site shall still work and fall back to Ink & Teal. | Must | **Verified** | Automated. (2 checks) |
| FR-THM-06 | The picker shall open from the shared header, show the current theme, be fully keyboard operable (arrows change theme; Escape closes and returns focus; focus stays inside), and close on outside click. | Must | **Verified** | Automated. (8 checks) |
| FR-THM-07 | Below 48em the picker shall be a bottom sheet that fits the viewport, scrolls to all 12 options, dims the page, closes via Close button or backdrop, and causes no horizontal overflow. The theme button shall stay visible in the header. | Must | **Verified** | Automated at 320x568, 375x667 and 390x844 with touch emulation. (18 checks) |
| FR-THM-08 | All stylesheet colours shall use design tokens, and every theme shall define all tokens, derived so contrast thresholds in NFR-A11Y-01 are met. | Must | **Verified** | Automated: token contrast and rendered-text audit. Absence of hard-coded theme colours was inspected, not tested. (Illustration food colours are fixed by design.) (2 checks) |
| FR-404-01 | `404.html` shall show a clear message, a link back, the shared header and the theme switcher. | Should | **Verified** | Automated: theme persists and switcher present. (1 checks) |

---

## 4. Non-functional requirements

| ID | Requirement | Priority | Status | Verification |
| --- | --- | --- | --- | --- |
| NFR-A11Y-01 | Text shall meet 4.5:1 (3:1 for large text) against its rendered background in every theme, including the open picker; focus indicators and control borders shall meet 3:1. | Must | **Verified** | Automated: computed-style audit of every text element in all 12 themes, plus token checks. (2 checks) |
| NFR-A11Y-02 | All interactive controls shall be operable by keyboard with a visible focus indicator. | Must | **Implemented** | Partly exercised (menu, picker, FAQ, recipe details, skip link). No full keyboard audit or screen-reader test. |
| NFR-A11Y-03 | With `prefers-reduced-motion: reduce` animations and transitions shall be effectively disabled and all functions still work. | Must | **Verified** | Automated: theme switching under reduced motion. The CSS rule was inspected. (1 checks) |
| NFR-A11Y-04 | The page shall use semantic landmarks, one `h1`, ordered headings, a captioned data table with scoped headers, labelled controls and unique IDs. | Must | **Verified** | Automated: duplicate-ID check only. Structure inspected, not audited with an external tool. (1 checks) |
| NFR-RSP-01 | There shall be no horizontal page scrolling at 320, 360, 375, 390, 414, 430, 768, 1024, 1280, 1366, 1440 and 1920 px, at 640 and 480 px (200% zoom proxies) and in phone/tablet orientations, in a dark and a light theme. | Must | **Verified** | Automated at all listed sizes with Ink & Teal and Pink & Lemon. (1 checks) |
| NFR-RSP-02 | Headings, buttons, the header (brand, seven navigation links, theme button, menu button) and the nutrition table shall not clip or overflow. | Must | **Verified** | Automated checks for scroll width and bounding boxes. The 320 px table and header were also viewed in screenshots. (2 checks) |
| NFR-RSP-03 | Touch targets (buttons, links, summaries) shall be at least 40 px high on a 390 px viewport. | Should | **Verified** | Automated. (1 checks) |
| NFR-PRV-01 | The site shall make no third-party requests and collect no personal data. The only stored data is the theme id in `localStorage`. | Must | **Verified** | Automated: zero non-local requests. Code inspected for analytics: none. (1 checks) |
| NFR-ROB-01 | Without JavaScript the headline, navigation, default theme and all content (about, table, recipes, FAQ) shall remain available with no horizontal overflow. | Should | **Verified** | Automated with JavaScript disabled. (3 checks) |
| NFR-CODE-01 | Loading and using the site shall produce no console or page errors. | Must | **Verified** | Automated. (1 checks) |
| NFR-COMP-01 | The site shall run by opening `index.html` from disk with no build step. | Must | **Partially verified** | All tests load through `file://` in Chromium. Other browsers not tested. |
| NFR-MNT-01 | Themes shall be defined in one file (`themes.js`), and the theme files shall be unchanged by this content conversion. | Should | **Implemented** | `themes.js` and `switcher.js` verified byte-identical to the previous version by checksum (a development check, not part of the shipped test suite). |
| NFR-CNT-01 | Every specific number on the page shall have a stated source and serving size. Statements not covered by a cited source shall be general, widely known cooking facts and are listed in section 8. | Must | **Implemented** | Reviewed manually against sources found during development. No automated check can verify factual accuracy. |
| NFR-PERF-01 | The site shall have no build step and no third-party assets. No numeric load-time target is set and none was measured. | Should | **Not measured** | File sizes in Appendix C. No Lighthouse or timing run. |

---

## 5. External interfaces
### 5.1 User interface
The existing editorial layout was kept: wide statement beside a narrow index in the hero; a narrow label column beside a wide content column in each section; projects-style lead-plus-pair presentation reused for egg types and recipes; ledger layout reused for nutrients and storage; row lists reused for labels and benefits; the former contact band reused for sources. New components: illustrations, a captioned data table, a callout, and native accordions for recipes and FAQ.

### 5.2 Browser storage
| Key | Value | Written when | Read when |
| --- | --- | --- | --- |
| `portfolio-theme` | one of the 12 theme ids | a theme is selected | every page load, before first paint |

The storage key name was kept unchanged so existing visitors' saved themes continue to work. Access is guarded with `try/catch`.

### 5.3 External links
Two source links (USDA FoodData Central; USDA FSIS Shell Eggs from Farm to Table) open in a new tab with `rel="noopener noreferrer"`. No other external requests.

---

## 6. Verification and traceability
### 6.1 Method
`tests/browser_tests.py` (Python + Playwright, Chromium) loads a temporary copy of the site and runs 95 checks, each tagged with the requirement IDs it covers. Statuses in sections 3 and 4 and the matrix below are generated from that run. One optional check (illustration crop detection) needs Pillow; it ran in this recorded run.

```
pip install playwright pillow
playwright install chromium
python tests/browser_tests.py
```

### 6.2 Result
**95 checks, 95 passed, 0 failed** (29 October 2026, headless Chromium, on the packaged project).

### 6.3 Traceability matrix
| Requirement | Automated checks | Result |
| --- | --- | --- |
| FR-NAV-01 | 7 | all passed |
| FR-NAV-02 | 3 | all passed |
| FR-NAV-03 | 1 | all passed |
| FR-CON-01 | 4 | all passed |
| FR-CON-02 | 8 | all passed |
| FR-CON-03 | 4 | all passed |
| FR-CON-04 | 5 | all passed |
| FR-CON-05 | 5 | all passed |
| FR-CON-06 | 3 | all passed |
| FR-CON-07 | 1 | all passed |
| FR-IMG-01 | 4 | all passed |
| FR-THM-01 | 3 | all passed |
| FR-THM-02 | 1 | all passed |
| FR-THM-03 | 1 | all passed |
| FR-THM-04 | 4 | all passed |
| FR-THM-05 | 2 | all passed |
| FR-THM-06 | 8 | all passed |
| FR-THM-07 | 18 | all passed |
| FR-THM-08 | 2 | all passed |
| FR-404-01 | 1 | all passed |
| NFR-A11Y-01 | 2 | all passed |
| NFR-A11Y-02 | 0 | not covered by an automated check |
| NFR-A11Y-03 | 1 | all passed |
| NFR-A11Y-04 | 1 | all passed |
| NFR-RSP-01 | 1 | all passed |
| NFR-RSP-02 | 2 | all passed |
| NFR-RSP-03 | 1 | all passed |
| NFR-PRV-01 | 1 | all passed |
| NFR-ROB-01 | 3 | all passed |
| NFR-CODE-01 | 1 | all passed |
| NFR-COMP-01 | 0 | not covered by an automated check |
| NFR-MNT-01 | 0 | not covered by an automated check |
| NFR-CNT-01 | 0 | not covered by an automated check |
| NFR-PERF-01 | 0 | not covered by an automated check |

Several checks cover more than one requirement, so counts per row are not additive.

---

## 7. Content data
All content is static HTML in `index.html`. The nutrition table is the only numeric data set.

| Item | Value | Basis |
| --- | --- | --- |
| Energy, protein, total fat, saturated fat, carbohydrate, cholesterol | per 100 g: 143 kcal; 12.56 g; 9.51 g; 3.13 g; 0.72 g; 372 mg | USDA FoodData Central, "Egg, whole, raw, fresh" (SR Legacy) |
| Per large egg (50 g) | 72 kcal; 6.3 g; 4.8 g; 1.6 g; 0.4 g; 186 mg | Calculated as half the per-100 g value, rounded; labelled as calculated on the page |
| Typical egg weights | chicken (large) 50 g; duck 70 g; quail 9 g | USDA household-measure weights |
| Storage and safety | refrigerate at 4 °C (40 °F) or below; raw shell eggs 3–5 weeks; hard-cooked eggs about 1 week; discard cracked eggs; do not wash before storing; egg dishes to 71 °C (160 °F); higher-risk groups avoid runny eggs; 2-hour limit; do not freeze in shell | USDA FSIS guidance |

Cross-type nutrient comparisons were deliberately **not** published: USDA datasets disagree for quail and duck, and a comparison would invite unsupported superiority claims.

---

## 8. Known limitations and unverified areas
- **Browsers/devices:** only headless Chromium tested. Firefox, Safari, real phones and tablets untested; touch was emulated.
- **Assistive technology:** no screen-reader test and no external audit tool (axe, Lighthouse). Contrast was verified by computation and rendered-style audit; semantics were inspected.
- **Nutrition sources:** values were corroborated through third-party mirrors of USDA data, not by loading the USDA site itself. USDA publishes several datasets whose figures differ slightly (for example a newer dataset lists a different energy value). Confirm on FoodData Central before relying on the figures.
- **Un-sourced general statements:** a few widely known cooking facts are stated without a specific citation: a hen's egg takes roughly a day to form; eggs bind, aerate and thicken; the cause of the green ring on hard-boiled yolks; the cooking times in the recipes; and that hard-boiled eggs do not freeze well. Recipe times and quantities are typical home-cooking estimates, not tested recipes.
- **Regional variation:** egg grading, washing, date labelling and the meaning of "free-range" and "organic" differ by country; the page says so rather than defining them.
- **Illustrations:** original artwork, not photographs. Food colours are fixed and do not change with themes.
- **Keyword checks:** the claims, superiority and leftover-content checks look for specific words; they cannot prove every sentence is accurate or free of implied claims.
- **Performance, mail, linting:** no load-time measurement, no linter or type checker configured.

---

## Appendix A. Theme definitions and measured contrast
Unchanged from the previous version. Required: text/background and link ≥ 4.5; secondary text ≥ 4.5.

| # | Theme | Mode | Background | Text | Accent | Text / bg | Secondary text / raised surface | Link / raised surface | Button text / accent |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Aubergine & Marigold | light | `#DDE3E8` | `#3A0F34` | `#EAAA00` | 12.5 | 5.0 | 4.7 | 7.9 |
| 2 | Creative Pop | light | `#CBB3E8` | `#1E1236` | `#E34234` | 9.3 | 4.7 | 4.6 | 5.1 |
| 3 | Emerald & Vermilion | light | `#F9EBD7` | `#046A38` | `#E34222` | 5.7 | 4.8 | 4.6 | 5.1 |
| 4 | Cobalt & Red | dark | `#021861` | `#F3F5FF` | `#DE1110` | 14.8 | 5.1 | 5.5 | 4.6 |
| 5 | Earth & Amber | dark | `#090907` | `#EFE6D6` | `#B99D73` | 16.1 | 6.1 | 5.9 | 7.7 |
| 6 | Ink & Teal | dark | `#031211` | `#E8E4D3` | `#00AEBB` | 15.0 | 5.7 | 5.3 | 7.1 |
| 7 | Royal Blue | dark | `#20309A` | `#FFFFFF` | `#BB232B` | 10.8 | 4.8 | 7.7 | 6.2 |
| 8 | Porcelain & Lemon | light | `#F3E6D7` | `#2B1D52` | `#E4FF3B` | 12.2 | 4.8 | 5.0 | 13.3 |
| 9 | Forest & Crimson | dark | `#06110C` | `#EDEFEA` | `#A31C1B` | 16.6 | 6.6 | 5.0 | 6.6 |
| 10 | Pink & Lemon | light | `#FFFFFF` | `#2B0A1B` | `#F43F91` | 18.1 | 5.5 | 4.9 | 5.1 |
| 11 | Orchid & Orange | light | `#E7B0DE` | `#400849` | `#FF5A0A` | 8.6 | 4.9 | 4.9 | 5.0 |
| 12 | Midnight & Lime | dark | `#030407` | `#F2F4FA` | `#D4FF24` | 18.6 | 6.9 | 13.5 | 17.7 |

## Appendix B. Design tokens
`--bg`, `--surface`, `--surface-2`; `--text`, `--text-2`; `--line`, `--line-strong`; `--accent`, `--on-accent`, `--accent-edge`, `--accent-soft`; `--link`, `--focus`; `--highlight`; `--band`, `--on-band`, `--band-2`, `--band-line`, `--band-accent`; `--shadow`.

## Appendix C. File inventory
| File | Role | Size (bytes) |
| --- | --- | --- |
| `index.html` | All content, navigation, SVG sprite | 39,822 |
| `style.css` | Layout and components (tokens only; illustration food colours fixed) | 22,952 |
| `themes.js` | Theme definitions, token derivation, persistence (unchanged) | 8,263 |
| `switcher.js` | Theme picker UI (unchanged) | 5,128 |
| `script.js` | Mobile menu, current-section highlight, footer year | 2,671 |
| `404.html` | Not-found page | 1,091 |
| `assets/og-image.png` | Social preview image | 64,928 |
| `favicon.svg` | Icon | 278 |
| `tests/browser_tests.py` | Optional developer test suite | n/a |

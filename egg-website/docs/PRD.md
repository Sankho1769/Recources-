# Product Requirements Document (PRD)

**Product:** Egg Guide — an informational website about eggs
**Version:** 1.0  |  **Date:** 29 October 2026  |  **Status:** Draft for owner review
**Companion document:** [SRS.md](SRS.md)

---

## 1. Summary
Egg Guide is a polished, easy-to-read website that helps people learn about eggs: what they are, the main types, what is in them, how they fit into a balanced diet, how to choose and store them safely, and simple ways to cook them. It was converted from a developer portfolio. The existing design, layout, 12-theme switcher and responsive behaviour were deliberately preserved; only the subject, content and imagery changed.

## 2. Background and problem
Eggs are an everyday food, yet people are often unsure how to store them, how to read cartons, how the types differ, or what the nutrition information actually says, and the web is full of exaggerated health claims. Visitors need clear, careful, sourced information in an attractive, accessible format.

**Problem statement:** provide a trustworthy, readable egg guide with honest nutrition information, safe-handling advice and practical recipes, without unsupported claims.

## 3. Goals and non-goals
### 3.1 Goals
| # | Goal | How we know |
| --- | --- | --- |
| G1 | A visitor understands what the site offers on the first screen | Hero headline, description, two clear buttons, "In this guide" index |
| G2 | Information is accurate, sourced and carefully worded | Numbers carry serving size and source; no superiority or medical claims |
| G3 | Visitors can learn the differences between egg types without being told one is "better" | Types section; labels explained as farming descriptions |
| G4 | Visitors can store and handle eggs safely | Storage section aligned with USDA FSIS guidance |
| G5 | Visitors can cook something straight away | Five recipe cards with expandable ingredients and method |
| G6 | The preserved design system keeps working | 12 themes, shared switcher, persistence, responsive layout, accessible controls |
| G7 | The site is easy for the owner to maintain | Static HTML; no build step |

### 3.2 Non-goals
- No medical, dietary or nutritional advice; no claims that eggs cure disease or guarantee outcomes.
- No ranking of egg types by nutritional superiority.
- No e-commerce, accounts, comments, analytics or contact form.
- No stock photography (none was available); illustrations are original.
- Not a complete recipe or nutrition database.

## 4. Users
| Persona | Needs |
| --- | --- |
| **Home cook** | Quick recipes; how long eggs keep; how to boil, scramble, make curry |
| **Curious shopper** | What the types and labels mean; how to read the carton |
| **Learner or parent** | Reliable nutrition basics with sources; safe handling |
| **Site owner** | Edit content in one HTML file; keep the theme system intact |

## 5. Scope
### 5.1 In scope (version 1.0)
Hero; About eggs; Types; Nutrition; Benefits; Storage; Recipes; FAQ; Sources; footer; 404 page; 12-theme system; responsive layout from 320 px up; original illustrations; README, PRD, SRS and optional tests.

### 5.2 Out of scope
Photography, more recipes, search, multilingual content, regional editions, newsletter, comments, contact form (see roadmap).

## 6. User stories and acceptance
| ID | As a… | I want to… | So that… | Acceptance (summary) | SRS |
| --- | --- | --- | --- | --- | --- |
| US-01 | visitor | see what the site is about immediately | I know whether to stay | Headline, description and two buttons | FR-CON-01 |
| US-02 | shopper | learn the types of eggs | I can choose for a dish | Chicken, duck, quail described; labels explained; no superiority claims | FR-CON-02 |
| US-03 | learner | read the nutrition basics with a source | I can trust the numbers | Table with serving sizes; source stated; calculated values labelled | FR-CON-03 |
| US-04 | cook | open a recipe and see ingredients and method | I can cook it | Five recipe cards with expandable details | FR-CON-04 |
| US-05 | visitor | find quick answers | I don't have to read everything | FAQ with 8+ questions, keyboard operable | FR-CON-05 |
| US-06 | household | store and handle eggs safely | we avoid foodborne illness | Storage guidance matching USDA FSIS | FR-CON-06 |
| US-07 | visitor | choose a colour theme from any page | the site suits my preference | 12 named themes; instant; persistent | FR-THM-01–05 |
| US-08 | phone user | use the theme picker comfortably | I can change themes easily | Bottom sheet fits and scrolls | FR-THM-07 |
| US-09 | keyboard user | use menu, picker, recipes and FAQ without a mouse | I can use the site | All operable by keyboard | FR-NAV-02, FR-THM-06, FR-CON-05 |
| US-10 | low-vision visitor | read every theme | no theme is unusable | Contrast thresholds met | NFR-A11Y-01 |
| US-11 | screen-reader user | understand the pictures | I don't miss information | Every illustration has a descriptive label | FR-IMG-01 |

## 7. Content requirements and provenance
| Content | Source or basis | Notes |
| --- | --- | --- |
| Nutrition table (per 100 g and per large egg, 50 g) | USDA FoodData Central "Egg, whole, raw, fresh" | Per-egg values calculated and labelled |
| Typical weights: chicken 50 g, duck 70 g, quail 9 g | USDA household measures | Shown as "about" |
| Storage, hygiene, cooking and leftover guidance | USDA FSIS | Refrigerate at 4 °C / 40 °F or below; 3–5 weeks raw; about a week hard-cooked; etc. |
| Shell colour reflects breed, not flavour | General guidance | No quality or nutrition claim made |
| Production, culinary roles, recipe methods and times | General cooking knowledge | Not individually sourced; recipe times are estimates |
| Free-range and organic | Described as labels that vary by country | No nutritional claim |

Rules: no invented statistics; no cure or guarantee claims; no comparison of nutrient superiority between types; disclaimer and doctor/dietitian pointer present; allergy mentioned.

## 8. Product requirements
| ID | Requirement | Priority | Status | SRS |
| --- | --- | --- | --- | --- |
| P-01 | Hero with required headline, description and two buttons | Must | Built | FR-CON-01 |
| P-02 | About, Types, Nutrition, Benefits, Storage sections | Must | Built | FR-CON-02, FR-CON-03 |
| P-03 | Five recipe cards with expandable details | Must | Built | FR-CON-04 |
| P-04 | FAQ (nine questions) | Must | Built | FR-CON-05 |
| P-05 | Sources section and full footer navigation | Must | Built | FR-CON-02 |
| P-06 | Original illustrations with accessible labels | Must | Built | FR-IMG-01 |
| P-07 | Preserved 12-theme system | Must | Built, unchanged | FR-THM-01–08 |
| P-08 | Responsive 320–1920 px; accessible controls | Must | Built | NFR-RSP, NFR-A11Y |
| P-09 | 404 page with themes | Should | Built | FR-404-01 |
| P-10 | Real photography (licensed) | Could | **Planned** | none |
| P-11 | More recipes, regional units and labelling guidance | Could | **Planned** | none |
| P-12 | Feedback or contact channel | Could | **Planned** (owner decision) | none |

## 9. Design requirements
- **Preserved:** page layout, component structure, typography, spacing, navigation, responsive behaviour, 12 themes, Ink & Teal default.
- **Adapted:** the portfolio's project lead-and-pair layout now presents egg types and recipes; the skills ledger presents nutrients and storage steps; the practice rows present benefits and labels; the contact band presents sources.
- **Imagery:** original flat illustrations. Outlines, plates and panels follow the theme tokens, while food keeps natural colours so eggs always look like eggs.
- **Motion:** unchanged and minimal; reduced-motion respected.

## 10. Success criteria
Acceptance-based, not traffic-based (no analytics exist and none are claimed).

| Criterion | Result in version 1.0 |
| --- | --- |
| Hero text and both buttons exactly as specified | Verified (automated) |
| All required sections present with required content | Verified (automated structure and keyword checks) plus manual accuracy review |
| Nutrition numbers state serving size and source | Verified (automated presence); factual accuracy reviewed manually, with limits (SRS section 8) |
| 12 themes work, default Ink & Teal, persistence | Verified (automated); theme files byte-identical to before |
| Contrast met in every theme | Verified (rendered-style audit) |
| No horizontal overflow at the listed widths | Verified (automated, two themes) |
| Works without JavaScript | Verified (automated) |
| No portfolio content remains | Verified (automated keyword check) |

Automated run: **95 of 95 checks passed** (headless Chromium, 29 October 2026). Untested areas are in SRS section 8.

## 11. Constraints, assumptions and risks
| Risk | Impact | Mitigation |
| --- | --- | --- |
| Nutrition figures differ between USDA datasets or change | Misleading numbers | Cite dataset, state serving size, link to source; owner re-checks on FoodData Central |
| Food-safety guidance varies by country | Incorrect advice locally | Page states practices differ; follows USDA FSIS and tells visitors to follow their carton |
| Visitors read content as medical advice | Harm or liability | Disclaimer, no claims, allergy and doctor/dietitian note |
| Recipe times are estimates | Under-cooked food | Recipes say to cook until fully set; safe-cooking guidance included |
| Illustrations not photographic | Less appetising than photos | Planned item P-10 |
| Untested browsers and devices | Layout bugs | Test Firefox, Safari and real devices before wide release |

## 12. Open questions
| # | Question |
| --- | --- |
| Q1 | Is "Egg Guide" the right name, and who is the publisher shown in the footer? |
| Q2 | Which country or region is the audience? (Affects units, labelling terms, storage norms.) |
| Q3 | Do you have licensed egg photographs to replace the illustrations? |
| Q4 | Should there be a way for visitors to contact or send feedback? (The previous contact form was removed because it no longer fit.) |
| Q5 | Please re-check the nutrition figures on USDA FoodData Central before publishing |
| Q6 | Should more recipes or dietary variants (vegetarian-only, egg-free alternatives) be added? |

## 13. Release plan
| Release | Contents | Status |
| --- | --- | --- |
| **1.0** | Egg content on the preserved design; 12 themes; documentation; tests | **Built** |
| 1.1 | Resolve Q1–Q6; add real photos if available; deploy and set `og:image` URL | **Planned** |
| 1.2 | More recipes; regional guidance | **Planned** |
| Later | Test on Firefox, Safari and real devices; accessibility and performance audits | **Planned** |

## 14. Change from the previous version
Replaced: developer introduction, project showcase, skills, practice, journey, contact form and GitHub/résumé references. Added: egg content, original illustrations, a data table, native accordions. **Unchanged:** `themes.js`, `switcher.js`, the token and layout system, navigation behaviour, responsive rules, 404 page structure, test approach. The `portfolio-theme` storage key was kept so returning visitors keep their theme.

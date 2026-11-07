# Testing checklist

**DONE** = performed in the build environment. **TODO** = you must check.

## A. Automated, no browser – DONE (2026-11-01)
`python3 build.py && python3 tests/check.py` passes with 105 translation keys in de/en/ru. It checks `lang`, canonicals, hreflang for 3 languages + x-default, unique ids, one h1, anchors and local links, form labels, prices, contact details, switcher links, legal page links, and Cyrillic only in Russian.

## B. Headless Chromium – NOT RUN after language list changed
`python3 tests/browser_check.py` reads the configured languages and covers de, en and ru at 1440 / 820 / 375 px. It should be rerun where Playwright and Chromium are available.

## C. Manual – TODO
| Test | DE | EN | RU |
|---|---|---|---|
| Native-speaker review of all text and legal templates | | | |
| Keyboard-only walk (switcher, menu, 3-step form) | | | |
| Screen reader: switcher name, current language, form errors | | | |
| Safari, Firefox, real iPhone/Android | | | |
| Lighthouse (performance, accessibility, SEO) and contrast | | | |
| Backdrop blur performance on an older phone | | | |
| Reduced-motion setting turns drift/hover motion off | | | |

## D. After publishing – TODO
Real URLs equal `site_url`; canonical/hreflang/sitemap open; Search Console shows no hreflang errors; legal pages completed by the owner and reviewed professionally.

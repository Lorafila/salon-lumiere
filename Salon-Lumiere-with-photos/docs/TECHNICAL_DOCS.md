# Technical documentation

## Files
| Path | Purpose |
|---|---|
| `src/legal.html` | Template of the Impressum/privacy page (incomplete template, see legal notes) |
| `src/template.html` | One page layout with `{{key}}` (translated text) and `{{@block}}` (generated HTML) placeholders |
| `src/data.json` | Language-independent facts: brand, contact, hours, service ids and prices, language list, site URL |
| `translations/de.json, en.json, ru.json` | All visible text, flat `"key": "text"` pairs. Keys must be identical in every file (105 keys) |
| `build.py` | Validates translations, fills the template, writes `de/ en/ ru/index.html` and `legal.html`, root `index.html`, `sitemap.xml`, `robots.txt` |
| `de/ en/ ru/index.html` | **Generated** pages – these are what you publish |
| `index.html` (root) | Small redirect: saved choice → browser language → DE |
| `assets/css/style.css`, `assets/js/main.js` | Shared styles and behaviour |
| `tests/check.py` | Automated checks of the built pages (no browser needed) |
| `tests/browser_check.py` | Optional real-browser test (needs `pip install playwright` + `playwright install chromium`) |

## Why build-time translation (decision)
- **Meaning:** a script produces three complete, static pages before publishing.
- **Why:** search engines and screen readers get real text at real URLs; no flash of wrong language; works on any free host; missing translations stop the build instead of reaching visitors. Loading JSON with JavaScript at runtime would fail when opening files directly, hide text from crawlers and need one URL for all languages.
- **Alternative:** hand-copying three HTML files – simple but prices and text drift apart.
- **You must understand:** edit sources, rebuild, publish generated folders.
- **AI can:** translate drafts, add languages, extend the template. **You must:** have texts proof-read by a native speaker.

## Language persistence
URL decides the language (`/en/`). When a visitor clicks the switcher, only the code (`de`/`en`/`ru`) is stored in `localStorage` under `salon-lang`, used only by the root redirect. No cookies, no personal data. Whether this needs mention in a client's privacy policy: verify.

## Dependencies
Python 3.8+ (build only). Visitors need nothing but a browser. No external requests at runtime (system fonts, inline favicon).

## Form
`#contact-form` validates required fields and e-mail pattern, writes messages from `data-msg-*` attributes (translated at build time), then shows the demo notice. No network call.

## Known technical limits
Hash on language switch is preserved by JS; without JS the switcher still works but jumps to the top. Address lines (street, city) are intentionally not translated.

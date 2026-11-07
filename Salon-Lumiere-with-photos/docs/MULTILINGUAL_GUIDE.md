# Multilingual guide

## How it is organized
- Texts: `translations/<code>.json`, flat keys such as `nav.prices`. German is the reference file.
- Shared facts (prices, phone, e-mail, address, hours, service ids): `src/data.json`. Prices appear as numbers; each language only supplies the format (`"price.from": "ab {amount} €"`).
- Layout: `src/template.html`. Structure never differs between languages.

## Edit an existing translation
Change the text in `translations/xx.json` → `python3 build.py` → reload the page. Keep `{amount}`-style placeholders unchanged.

## Change a price or contact detail
Edit `src/data.json` only. All languages update together.

## Languages now: de (default), en, ru. Add another language (example: Turkish `tr`)
1. Copy `translations/en.json` to `translations/tr.json` and translate every value.
2. In `src/data.json` add `"tr"` to `languages` and `"tr": {"name": "Türkçe", "og": "tr_TR"}` to `language_meta`.
3. `python3 build.py` – it creates `tr/index.html`, adds it to the switcher, hreflang, sitemap and root redirect.
4. `python3 tests/check.py`, then do the manual checks below.
5. Right-to-left languages (Arabic, Hebrew) also need `dir="rtl"` and CSS changes – not implemented.

## Test a new language
Automated: build + check (keys, placeholders, `lang`, hreflang, links, prices). Manual: read every section, switch from each section, test form errors, narrow the window to 360 px, have a native speaker review.

## Avoid missing or inconsistent text
The build fails on missing/extra keys, empty values or changed placeholders. It cannot judge translation quality. Never type prices into translation files.

## Reuse for clients
Copy the folder, replace `data.json`, template text and translations, rebuild. Ask the client which languages and who proofreads each.

## Missing-translation policy
Deliberately **no silent fallback** to German: a missing key is a build error.

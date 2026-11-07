# Salon Lumière – multilingual demo website (DE / EN / RU)

Fictional beauty salon. All names, prices, address, phone and e-mail are invented. The contact form is a demo and sends nothing.

## Preview locally
1. Open a terminal in this folder.
2. `python3 -m http.server 8000`
3. Visit http://localhost:8000/ (redirects to a language) or http://localhost:8000/de/

Opening `de/index.html` directly by double-click also works; the root `index.html` redirect and language memory work best through the local server.

## Change something
Edit `src/data.json` (prices, contact, hours) or `translations/*.json` (texts), then run `python3 build.py`. Never edit `de/`, `en/`, `ru/` by hand – they are regenerated.

## Check
`python3 build.py && python3 tests/check.py` (optional browser test: `python3 tests/browser_check.py`, needs `pip install playwright` and `playwright install chromium`)

## Folders
See TECHNICAL_DOCS.md. Guides are in `docs/`.

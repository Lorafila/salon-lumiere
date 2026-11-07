# Troubleshooting

| Problem | Cause / fix |
|---|---|
| `BUILD ERROR: xx.json is missing keys` | Add the listed keys to that file |
| `BUILD ERROR: placeholders ... differ` | Keep `{amount}` exactly as in the German text |
| `python3: command not found` | Install Python 3 (python.org) or try `python build.py` |
| Changes do not appear | Run `python3 build.py`, hard-reload (Ctrl+F5) |
| Page has no styling | Open the page from inside the project folder; `assets/` must sit beside `de/ en/ ru/` |
| Language switch jumps to top | JavaScript disabled or blocked; the page itself still works |
| Root `/` always opens German | Normal when no saved choice and the browser language is not en/ru |
| Wrong URLs in canonical/hreflang | `site_url` in `src/data.json` is not the real address; fix and rebuild |
| Umlauts or Cyrillic garbled | Save files as UTF-8 |

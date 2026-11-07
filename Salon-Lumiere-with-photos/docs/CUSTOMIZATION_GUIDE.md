# Customization guide

After any change: `python3 build.py`, then reload.

- **Prices:** `src/data.json` → `services[].price.amount` and `from` (true = "from/ab/от").
- **Business name, address, phone, e-mail:** `src/data.json`.
- **Opening hours:** `src/data.json` → `hours` (day labels live in translation files; `time: null` shows "closed").
- **Texts:** `translations/*.json`; change all three languages together.
- **Add/remove a service:** add `{id, price}` in `data.json` and `svc.<id>.name` / `svc.<id>.desc` in all three translation files.
- **Colours:** variables at the top of `assets/css/style.css` (`--bg`, `--tx`, `--mut`, `--gold`, `--line`). Keep text/background contrast readable.
- **Photography:** none is included (no licensed photos available). The hero and the gallery use soft-focus placeholder panels (`.hero-art`, `.ph1`–`.ph6`). To use real photos you need images you have the rights to, compressed (e.g. WebP, under ~200 KB each), `<img>` tags with translated `alt` text (new keys in all language files) and crops matching the tile ratios in `style.css`.
- **Masters:** roles are placeholders (`team.*` keys in all four files). Add real names/photos only with the salon's consent and licensed images.
- **Legal pages:** `legal.html` is a template; fill the owner/VAT fields and have the texts reviewed before a real launch.
- **Prices:** only in `src/data.json`, euro only; the text "incl. VAT" in `prices.note` is a demo assumption – confirm.
- **Site address:** `site_url` in `data.json`.

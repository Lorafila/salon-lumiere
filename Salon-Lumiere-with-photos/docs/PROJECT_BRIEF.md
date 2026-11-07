# Project Brief – Salon Lumière (fictional demo) v2.0

**Business:** fictional beauty salon (hair, facial, nails, brows). **Audience:** discerning clients in German-speaking Germany plus EN and RU speakers. **Goal:** portfolio piece and reusable template for real client sites, built with €0.

## Scope
- One page per language: `/de/`, `/en/`, `/ru/` (+ `legal.html` per language). German is the default.
- Sections: hero with opening hours, services bento, masters (role placeholders), euro price menu, about, gallery (placeholder panels), opening hours, contact with 3-step concierge demo form, footer with legal links.
- All prices in euros only, one source (`src/data.json`), identical in all languages. Prices are **demo values**, not verified real prices; real clients must confirm them.
- Design: dark quiet-luxury look, see `docs/DESIGN_BLUEPRINT.md` and `docs/DESIGN_NOTES.md`.

## Technical
HTML, CSS, vanilla JS; Python 3 build script (standard library). No frameworks, cookies, analytics, external fonts, scripts or images.

## Known limitations
No real booking or message delivery; licensed stock photographs are included; Impressum/privacy are **templates**; translations are drafts needing native review (especially RU); multilingual SEO unverified until real URLs; browser coverage limited to headless Chromium so far.

## Costs
Demo €0. Real client (verify current prices): domain about €5–15/year, free static hosting tiers, form/booking services free or paid, your maintenance time.

## Definition of done
Builds; automated and browser tests pass; manual checklist completed by the owner; limitations documented.

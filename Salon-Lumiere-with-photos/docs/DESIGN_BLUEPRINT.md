# Salon Lumière – Quiet Luxury Design Blueprint (2026–2027)

Status: the sections marked **Implemented** exist in this project. Everything marked **Recommendation** is guidance for a production team (Webflow / Figma / Tailwind) and is **not built here**.

## 1. Philosophy
Quiet luxury: restraint, space, one accent. Nothing decorative without purpose; motion only answers the visitor; text always readable. **Implemented** in the dark "Caviar & Champagne" theme.

## 2. Tokens (Implemented in `assets/css/style.css`)
| Token | Dark (implemented) | Light alternative (Recommendation) |
|---|---|---|
| Background | `#0f0c0b` caviar | `#f4efe9` alabaster |
| Text | `#efe7df` / muted `#b9ada5` | `#1b1714` / `#6b625b` |
| Accent | `#dcc08e` champagne gold | `#8c7a64` soft taupe + platinum `#c9c9cc` |
| Lines | `rgba(232,208,160,.22)` | `rgba(60,45,30,.18)` |
Radius 28px (cards), 999px (buttons). Spacing fluid with `clamp()`.

## 3. Typography
**Implemented:** system stacks only – display `Didot / Bodoni 72 / Playfair Display (if installed) / Georgia`, body `Avenir Next / Segoe UI / Helvetica Neue`. No font files, no external requests (relevant for German data-protection practice: no hotlinked fonts).
**Recommendation:** license and **self-host** a haute-couture Didone (headlines, 400 weight, tight tracking −0.02em, sizes 56–110px desktop) plus a geometric sans (body 17–18px, line-height 1.7). Verify each licence allows web embedding before purchase/use. Check Cyrillic coverage for RU.

## 4. Layout – Bento
12-column grid, 12–20px gaps, tiles spanning 3–7 columns, one hero tile (5 cols × 2 rows). **Implemented** for services (`.bento`, `.t1`–`.t6`); collapses to 6 columns ≤960px and 1 column ≤540px. Keep 6 tiles maximum per block; whitespace between sections ≥ 8rem.

## 5. Glass and depth
**Implemented:** fixed `.mesh` layer with three blurred colour fields drifting 40–52 s (transform only, disabled with reduced motion). `.glass`: 135° white→transparent gradient, 1px champagne border, inset top highlight, `backdrop-filter: blur(60px) saturate(140%)`, solid fallback via `@supports`. Used on the hero card, price panel and booking panel; tiles use 28px blur, header 24px (performance trade-off: large blurs are GPU-costly). Neon glow was not used – it conflicts with restraint.

## 6. Page structure
- **Hero (Implemented):** headline bottom-left spanning ~7/11 columns (clamp 40–93px), lead text 19px, two CTAs (primary filled gold, secondary outlined); right: glass card with opening hours. **Recommendation:** replace the mesh with a 6–10 s silent video loop behind the card.
- **Services (Implemented):** interactive bento; hover lifts 4px, a gold spotlight follows the pointer (fine pointers only).
- **Masters (Implemented as roles):** three tall portrait panels; hover cross-fades a second light layer. Names, bios and portfolio images are **not invented** – the salon must supply them. **Recommendation:** portrait 3:4, reveal 3 portfolio images on hover/tap, caption with specialisation only.
- **Prices (Implemented):** typeset menu, euro only, single source `src/data.json`.
- **Concierge booking (Implemented as demo):** 3 steps – ritual, preferred time of day, details; progress text, per-step validation, focus management, translated messages. It sends nothing. **Recommendation:** real delivery needs a service (see costs in docs); consider a calendar slot picker only after availability data exists.

## 7. Interaction spec
Implemented: magnetic buttons (max ≈ 8px shift, pointer devices only), tile spotlight, underline-grow links, smooth anchor scroll (CSS). Not implemented on purpose: custom cursor (accessibility/pointer confusion) and Locomotive-style scroll hijacking (hurts keyboard, reduced-motion and mobile use). If requested later: native `scroll-behavior` plus Lenis-type smoothing behind a reduced-motion check.

## 8. Asset guidelines (recommendations for future replacements or additions; current image sources are listed in `ASSETS_PHOTO_CREDITS.md`)
- Photography: 4K source (≥ 3840 px long edge), export 1600–2400 px WebP/AVIF, ≤ 250 KB each; shallow depth of field (f/1.8–2.8), soft window light, warm 4000–4500 K, subtle grain, consistent grade matching champagne/fig tones.
- Macro textures: silk, hair strands, product caps; subsurface-scattering feel on skin and glass.
- Video loops: 6–10 s, 24–30 fps, H.264 + AV1/WebM, ≤ 3 MB, muted, poster image, no audio, pause on reduced motion/save-data.
- Rights: written licences or releases for every person and image.

## 9. Webflow / Figma / Tailwind mapping (Recommendation)
Figma variables = the token table above; Auto Layout for bento (columns 12, gutter 16). Webflow: global classes `tile`, `glass`, `btn`; CSS variables in custom code. Tailwind: `theme.extend.colors = { caviar:'#0f0c0b', champagne:'#dcc08e', bone:'#efe7df' }`, `borderRadius.xl2 = '28px'`, `fontFamily.display` self-hosted; use `backdrop-blur-[60px]` sparingly. This project deliberately uses plain CSS to keep the stack simple.

## 10. Performance and accessibility budgets
LCP < 2.5 s, page weight < 1 MB without photos, visible focus everywhere, text contrast ≥ 4.5:1, touch targets ≥ 44px, `prefers-reduced-motion` honoured (implemented). Measure with Lighthouse – not yet done.

## 11. Germany notes (verify with a professional; not legal advice)
Impressum and privacy policy are required for a real commercial launch (templates included, marked incomplete); no cookies/trackers/external fonts or scripts are used; prices should be shown including VAT where applicable (demo note says "incl. VAT" – confirm per client); contact-form data handling needs a processor agreement if a service is added.

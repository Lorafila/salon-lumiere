# Design notes (v2.0 quiet luxury)

- **Concept:** a private salon after dark – caviar black, champagne light, glass surfaces over slowly drifting colour fields.
- **Type:** Didot/Bodoni-style display serif from the system, plus a clean system sans. Display look varies slightly per device (no font files by design).
- **Layout:** bento services grid, asymmetric two-column sections, mosaic gallery, oversized footer wordmark.
- **Motion:** only visitor-driven (hover lift, spotlight, magnetic buttons, underline) plus a very slow background drift; everything off with `prefers-reduced-motion`.
- **Imagery:** individual, locally stored Pexels photographs in the gallery and master cards.
- **Languages:** German (default), English and Russian; headings use `hyphens:auto` per page `lang`.
- Full specification: `DESIGN_BLUEPRINT.md`.

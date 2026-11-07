# Deployment guide (free static hosting)

Prices and terms of hosts change – check each provider's current page before relying on this.

## Recommended for a beginner: Netlify Drop or Cloudflare Pages / GitHub Pages
**Option 1 – Netlify (drag and drop)**
1. Set the real address in `src/data.json` → `site_url` (use the address the host gives you first, e.g. `https://my-demo.netlify.app`).
2. `python3 build.py`
3. Make a copy of the folder without `src/`, `tests/`, `docs/`, `build.py` (optional, they are harmless but not needed) and drag it onto the host's upload page.
4. Open `/de/`, `/en/`, `/ru/` and `/` and test.

**Option 2 – GitHub Pages:** push the folder to a repository, enable Pages for the branch. A project site lives under `/repo-name/`, so `site_url` must include that path; links in this site are relative, so they keep working.

## What is free / what may cost
Free: hosting subdomain, the site itself. May cost: own domain (yearly), form or booking services, your time for changes.

## Owner must do
Supply real texts, photos with usage rights, legal pages, and approve the site.

## Before a real client launch (verify with a professional – not legal advice)
Imprint (Impressum) and privacy policy (templates exist in `legal.html`, incomplete by design); cookie/consent rules if anything beyond essential storage is added; whether the language-code `localStorage` needs mention; photo and font licences; contact-form data handling (GDPR/DSGVO) with the chosen provider.

## Do not
Do not publish fictional business data as a real company; do not buy a domain for the demo.

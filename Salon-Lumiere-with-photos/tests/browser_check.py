#!/usr/bin/env python3
"""Optional browser test (needs: pip install playwright && playwright install chromium).
Run after build.py:  python3 tests/browser_check.py"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
R = Path(__file__).parent.parent
LANGS = json.loads((R / "src/data.json").read_text(encoding="utf-8"))["languages"]
fails = []
def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok: fails.append(msg)
def url(l, page="index.html", h=""): return "file://%s/%s/%s%s" % (R, l, page, h)
with sync_playwright() as p:
    b = p.chromium.launch()
    for lang in LANGS:
        for name, w, h in (("desktop", 1440, 900), ("tablet", 820, 1100), ("mobile", 375, 800)):
            tag = "[%s %s]" % (lang, name)
            pg = b.new_page(viewport={"width": w, "height": h}); errs = []; reqs = []
            pg.on("pageerror", lambda e: errs.append(str(e))); pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)
            pg.on("request", lambda r: reqs.append(r.url))
            pg.goto(url(lang)); pg.wait_for_timeout(200)
            check(pg.evaluate("document.documentElement.scrollWidth<=document.documentElement.clientWidth"), tag + " no horizontal overflow")
            check(not errs, tag + " no console/page errors")
            check(pg.evaluate("document.documentElement.lang") == lang, tag + " html lang")
            clip = pg.evaluate("[...document.querySelectorAll('.btn,.lang a,h1,h2,h3')].filter(e=>e.offsetParent&&e.scrollWidth>e.clientWidth+1).map(e=>e.textContent.trim())")
            check(not clip, tag + " no clipped buttons/headings %s" % (clip or ""))
            check(all("\u20ac" in t for t in pg.eval_on_selector_all("td.price", "e=>e.map(x=>x.textContent)")), tag + " prices show \u20ac")
            if name == "mobile":
                hidden = pg.locator("#nav").is_hidden(); pg.click(".menu-btn")
                check(hidden and pg.locator("#nav").is_visible() and pg.get_attribute(".menu-btn", "aria-expanded") == "true", tag + " menu opens")
                pg.click("#nav a[href='#prices']"); check(pg.locator("#nav").is_hidden(), tag + " menu closes after link")
            other = LANGS[(LANGS.index(lang) + 1) % len(LANGS)]
            pg.goto(url(lang, h="#prices")); pg.wait_for_timeout(150)
            pg.click(".lang a[lang='%s']" % other); pg.wait_for_url("**/%s/index.html#prices" % other); pg.wait_for_load_state("load")
            check(pg.evaluate("document.documentElement.lang") == other, tag + " switch to %s keeps #prices" % other)
            # concierge form, three steps
            pg.goto(url(lang)); n0 = len(reqs)
            check(pg.locator("#contact-form .step:visible").count() == 1, tag + " only step 1 visible")
            check(pg.locator("#contact-form .back").is_hidden() and pg.locator("#contact-form .submit").is_hidden() and pg.locator("#contact-form .next").is_visible(), tag + " step 1 shows only Continue button")
            pg.click("#contact-form .next")
            check(bool(pg.inner_text("#f-service-err")) and pg.evaluate("document.activeElement.id") == "f-service", tag + " step 1: translated error + focus")
            pg.select_option("#f-service", "cut"); pg.click("#contact-form .next")
            pg.click("#contact-form .next")
            check(bool(pg.inner_text("#f-time-err")), tag + " step 2: time-of-day required")
            pg.check("#f-time-morning", force=True); pg.click("#contact-form .next")
            check(pg.locator("#contact-form .next").is_hidden() and pg.locator("#contact-form .submit").is_visible() and pg.locator("#contact-form .back").is_visible(), tag + " step 3 shows Back + Submit only")
            pg.click("#contact-form .submit")
            check(bool(pg.inner_text("#f-name-err")) and pg.evaluate("document.activeElement.id") == "f-name", tag + " step 3: empty submit shows errors")
            pg.fill("#f-name", "Test"); pg.fill("#f-email", "bad"); pg.fill("#f-message", "x"); pg.click("#contact-form .submit")
            check(bool(pg.inner_text("#f-email-err")), tag + " invalid e-mail error")
            pg.fill("#f-email", "a@b.de"); pg.click("#contact-form .submit")
            check(pg.locator(".status.ok").is_visible() and len(reqs) == n0, tag + " valid: demo notice, no network request")
            pg.goto(url(lang, "legal.html")); pg.wait_for_timeout(150)
            check(pg.locator("#imprint").is_visible() and pg.locator("#privacy").is_visible() and not errs, tag + " legal page renders without errors")
            pg.close()
    b.close()
print("\n%d failure(s)" % len(fails)); sys.exit(1 if fails else 0)

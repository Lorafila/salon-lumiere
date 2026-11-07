#!/usr/bin/env python3
"""Automated checks on the BUILT site. Run after build.py:  python3 tests/check.py"""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path

R = Path(__file__).parent.parent
D = json.loads((R / "src/data.json").read_text(encoding="utf-8"))
LANGS = D["languages"]
fails = []


def check(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.lang = s.canon = None; s.ids = []; s.hrefs = []; s.alt = []; s.h1 = 0; s.labels = set(); s.inputs = []; s.text = []
    def handle_starttag(s, tag, a):
        a = dict(a)
        if tag == "html": s.lang = a.get("lang")
        if "id" in a: s.ids.append(a["id"])
        if tag == "a" and "href" in a: s.hrefs.append(a["href"])
        if tag == "link" and a.get("rel") == "alternate": s.alt.append((a.get("hreflang"), a.get("href")))
        if tag == "link" and a.get("rel") == "canonical": s.canon = a.get("href")
        if tag == "h1": s.h1 += 1
        if tag == "label": s.labels.add(a.get("for"))
        if tag in ("input", "select", "textarea"): s.inputs.append(a.get("id"))
    def handle_data(s, d): s.text.append(d)


pages, raw = {}, {}
for l in LANGS:
    raw[l] = (R / l / "index.html").read_text(encoding="utf-8")
    p = P(); p.feed(raw[l]); pages[l] = p

site = D["site_url"].rstrip("/")
expected_prices = [s["price"]["amount"] for s in D["services"]]
for l in LANGS:
    p = pages[l]
    check(p.lang == l, "[%s] <html lang> is '%s'" % (l, l))
    check(p.canon == "%s/%s/" % (site, l), "[%s] canonical URL" % l)
    check(sorted(h for h, _ in p.alt) == sorted(LANGS + ["x-default"]), "[%s] hreflang set complete (incl. x-default)" % l)
    check(len(p.ids) == len(set(p.ids)), "[%s] element ids are unique" % l)
    check(p.h1 == 1, "[%s] exactly one h1" % l)
    check("{{" not in raw[l], "[%s] no unreplaced template placeholders" % l)
    bad = [h for h in p.hrefs if h.startswith("#") and h[1:] not in p.ids]
    check(not bad, "[%s] all #anchors resolve %s" % (l, bad or ""))
    badf = [h for h in p.hrefs if not re.match(r"(#|https?:|mailto:|tel:)", h) and not (R / l / h.split("#")[0]).resolve().exists()]
    check(not badf, "[%s] all local links exist %s" % (l, badf or ""))
    check(all(i in p.labels for i in p.inputs), "[%s] every form field has a <label for>" % l)
    check([int(x) for x in re.findall(r'class="price">[^<]*?(\d+)', raw[l])] == expected_prices, "[%s] prices equal data.json" % l)
    for k in ("phone", "email", "street", "city"):
        check(D[k] in raw[l] or D[k].replace("ß", "&szlig;") in raw[l], "[%s] business detail '%s' present" % (l, k))
    check(sum(1 for h in p.hrefs if re.match(r"\.\./\w\w/index.html", h)) == len(LANGS), "[%s] switcher links to all languages" % l)
    prices = re.findall(r'class="price">([^<]*)<', raw[l])
    check(prices and all("\u20ac" in x for x in prices), "[%s] every price is shown in euro (\u20ac)" % l)
    check(not re.search("[\u20bd]|\\bруб|\\bRUB\\b|\\$|\u00a3", re.sub(r"<[^>]+>", " ", raw[l])), "[%s] no ruble/dollar/pound signs" % l)
    lg = (R / l / "legal.html").read_text(encoding="utf-8"); q = P(); q.feed(lg)
    check(q.lang == l and q.canon == "%s/%s/legal.html" % (site, l) and "{{" not in lg, "[%s] legal page: lang, canonical, no placeholders" % l)
    check(sum(1 for h in q.hrefs if re.match(r"\.\./\w\w/legal.html", h)) == len(LANGS), "[%s] legal page switcher links to all languages" % l)
    check(all(h.split("#")[0] == "" or (R / l / h.split("#")[0]).exists() for h in p.hrefs if h.startswith("legal.html")), "[%s] footer legal links resolve" % l)

cyr = lambda s: bool(re.search("[\u0400-\u04FF]", s))
body = lambda l: re.sub(r"<[^>]+>", " ", raw[l])
check(cyr(body("ru")) and not cyr(body("de")) and not cyr(body("en")), "Cyrillic only in ru")
T = {l: json.loads((R / "translations" / (l + ".json")).read_text(encoding="utf-8")) for l in LANGS}
same = [k for l in LANGS if l != "de" for k, v in T[l].items() if v == T["de"][k] and re.search(r"[^\W\d_]{5,}", re.sub(r"\{\w+\}", "", v))]
check(not same, "no long en/ru value identical to German %s" % same)
for f in ("index.html", "sitemap.xml", "robots.txt"):
    check((R / f).exists(), "root file %s exists" % f)
print("\n%d failure(s)" % len(fails))
sys.exit(1 if fails else 0)

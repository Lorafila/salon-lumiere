#!/usr/bin/env python3
"""Builds de/index.html, en/index.html, ru/index.html (+ root redirect, sitemap, robots)
from src/template.html + src/data.json + translations/*.json.  Needs only Python 3.8+.
Run:  python3 build.py        The build STOPS with an error if any translation is missing."""
import html, json, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
D = json.loads((ROOT / "src/data.json").read_text(encoding="utf-8"))
LANGS, DEFAULT, SITE = D["languages"], D["default_language"], D["site_url"].rstrip("/")


def fail(msg):
    sys.exit("BUILD ERROR: " + msg)


T = {}
for l in LANGS:
    p = ROOT / "translations" / (l + ".json")
    if not p.exists():
        fail("missing file " + str(p))
    T[l] = json.loads(p.read_text(encoding="utf-8"))
ref = T[DEFAULT]
for l in LANGS:
    miss, extra = sorted(set(ref) - set(T[l])), sorted(set(T[l]) - set(ref))
    if miss:
        fail("%s.json is missing keys: %s" % (l, miss))
    if extra:
        fail("%s.json has keys not in %s.json: %s" % (l, DEFAULT, extra))
    for k, v in T[l].items():
        if not v.strip():
            fail("%s.json: empty value for '%s'" % (l, k))
        if set(re.findall(r"\{(\w+)\}", v)) != set(re.findall(r"\{(\w+)\}", ref[k])):
            fail("%s.json: placeholders of '%s' differ from %s.json" % (l, k, DEFAULT))

e = lambda s: html.escape(str(s), quote=True)


def price(t, p):
    return t["price.from" if p["from"] else "price.fixed"].format(amount=p["amount"])


def blocks(l, page="index.html"):
    t = T[l]
    sfx = "" if page == "index.html" else page
    b = {"lang": l, "canonical": "%s/%s/%s" % (SITE, l, sfx), "og_locale": D["language_meta"][l]["og"]}
    for k in ("brand", "phone", "phone_href", "email", "street", "city"):
        b[k] = e(D[k])
    b["hreflang"] = "\n".join('<link rel="alternate" hreflang="%s" href="%s/%s/%s">' % (k, SITE, k, sfx) for k in LANGS)
    b["hreflang"] += '\n<link rel="alternate" hreflang="x-default" href="%s">' % (SITE + "/" if not sfx else "%s/%s/%s" % (SITE, DEFAULT, sfx))
    items = []
    for k in LANGS:
        cur = ' aria-current="true"' if k == l else ""
        items.append('<li><a href="../%s/%s" lang="%s" hreflang="%s" aria-label="%s"%s>%s</a></li>'
                     % (k, page, k, k, e(D["language_meta"][k]["name"]), cur, k.upper()))
    b["switcher"] = '<nav class="lang" aria-label="%s"><ul>%s</ul></nav>' % (e(t["lang.label"]), "".join(items))
    b["services"] = "".join('<article class="tile t%d"><h3>%s</h3><p>%s</p></article>'
                            % (i, e(t["svc.%s.name" % s["id"]]), e(t["svc.%s.desc" % s["id"]])) for i, s in enumerate(D["services"], 1))
    b["prices"] = "".join('<tr><th scope="row">%s</th><td class="price">%s</td></tr>'
                          % (e(t["svc.%s.name" % s["id"]]), e(price(t, s["price"]))) for s in D["services"])
    b["options"] = "".join('<option value="%s">%s</option>' % (s["id"], e(t["svc.%s.name" % s["id"]])) for s in D["services"])
    b["gallery"] = "".join('<figure><div class="ph ph%d" role="img" aria-label="%s"></div><figcaption>%s</figcaption></figure>'
                           % (i, e(t["gal.%d" % i]), e(t["gal.%d" % i])) for i in range(1, 7))
    b["hours"] = "".join("<dt>%s</dt><dd>%s</dd>" % (e(t[h["key"]]), e(h["time"] or t["hours.closed"])) for h in D["hours"])
    return b


tpl = (ROOT / "src/template.html").read_text(encoding="utf-8")
legal_tpl = (ROOT / "src/legal.html").read_text(encoding="utf-8")


def render(l, tpl, page):
    t, b = T[l], blocks(l, page)

    def sub(m):
        k = m.group(1)
        if k.startswith("@"):
            if k[1:] not in b:
                fail("template uses unknown generated block " + k)
            return b[k[1:]]
        if k not in t:
            fail("template uses key '%s' that is missing in %s.json" % (k, l))
        return e(t[k])

    return re.sub(r"\{\{([\w.@]+)\}\}", sub, tpl)


for l in LANGS:
    (ROOT / l).mkdir(exist_ok=True)
    (ROOT / l / "index.html").write_text(render(l, tpl, "index.html"), encoding="utf-8")
    (ROOT / l / "legal.html").write_text(render(l, legal_tpl, "legal.html"), encoding="utf-8")

root = """<!doctype html>
<html lang="%(d)s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(brand)s</title>
<link rel="canonical" href="%(site)s/">
<noscript><meta http-equiv="refresh" content="0;url=%(d)s/index.html"></noscript>
<script>
(function(){var L=%(langs)s,s=null;try{s=localStorage.getItem('salon-lang')}catch(e){}
var n=(navigator.language||'%(d)s').slice(0,2).toLowerCase();
var t=L.indexOf(s)>-1?s:(L.indexOf(n)>-1?n:'%(d)s');
location.replace(t+'/index.html'+location.hash);})();
</script></head>
<body><p>%(links)s</p></body></html>
""" % {"d": DEFAULT, "brand": e(D["brand"]), "site": SITE, "langs": json.dumps(LANGS),
       "links": " | ".join('<a href="%s/index.html" lang="%s">%s</a>' % (k, k, e(D["language_meta"][k]["name"])) for k in LANGS)}
(ROOT / "index.html").write_text(root, encoding="utf-8")

urls = ""
for l in LANGS:
    alts = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s/%s/"/>' % (k, SITE, k) for k in LANGS)
    urls += "<url><loc>%s/%s/</loc>%s</url>\n" % (SITE, l, alts)
    urls += "<url><loc>%s/%s/legal.html</loc></url>\n" % (SITE, l)
(ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + "</urlset>\n", encoding="utf-8")
(ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE, encoding="utf-8")
print("OK: built %s (%d translation keys each)" % (", ".join(LANGS), len(ref)))

#!/usr/bin/env python3
"""Static site generator for pmapparel.com. Outputs plain HTML into ./site."""
import json, os, html, datetime

BASE = "https://www.pmapparel.com"
OUT = "site"
TODAY = "2026-07-28"
UPDATED_HUMAN = datetime.date.fromisoformat(TODAY).strftime("%B %Y")

PHONE = "(515) 984-7740"
PHONE_TEL = "+15159847740"
EMAIL = "info@pmapparel.com"
ADDR = "1100 S 5th St"
CITY = "Polk City"
STATE = "IA"
ZIP = "50226"

QUOTE_URL = "https://wkf.ms/3WiETfm"
STORES_URL = "https://pmapparel.chipply.com/"
PROMO_URL = "https://www.promoplace.com/pmapparel"
SPONSOR_URL = "https://form.jotform.com/231636854478064"
IOD_URL = "https://www.iowaondemand.com/"
FB_URL = "https://www.facebook.com/pmapparel"
IG_URL = "https://www.instagram.com/p_mapparel/"
TT_URL = "https://www.tiktok.com/@p_mapparel"
LI_URL = "https://www.linkedin.com/company/p-&-m-apparel"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=P%26M+Apparel+1100+S+5th+St+Polk+City+IA+50226"

LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "@id": BASE + "/#business",
    "name": "P&M Apparel",
    "description": "Woman-owned, third-generation custom apparel company in Polk City, Iowa. Screen printing, embroidery, DTF and fusion transfers, sublimation, promotional products, online team stores, and live event printing for the Des Moines metro and beyond since 1987.",
    "url": BASE + "/",
    "telephone": PHONE_TEL,
    "email": EMAIL,
    "foundingDate": "1987",
    "priceRange": "$$",
    "image": BASE + "/assets/logo-black.png",
    "logo": BASE + "/assets/logo-black.png",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": ADDR,
        "addressLocality": CITY,
        "addressRegion": STATE,
        "postalCode": ZIP,
        "addressCountry": "US",
    },
    "geo": {"@type": "GeoCoordinates", "latitude": 41.7716, "longitude": -93.7130},
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "08:00", "closes": "17:00",
    }],
    "areaServed": ["Polk City IA", "Ankeny IA", "Des Moines IA", "Central Iowa", "United States"],
    "sameAs": [FB_URL, IG_URL, TT_URL, LI_URL],
    "knowsAbout": ["screen printing", "custom embroidery", "DTF transfers", "sublimation printing", "promotional products", "online team stores", "live event printing"],
}

NAV = [
    ("home.", "/"),
    ("services.", "/services/"),
    ("iowa on demand.", "/iowa-on-demand/"),
    ("about.", "/about-us/"),
    ("faq.", "/faq/"),
    ("blog.", "/blog/"),
    ("giving back.", "/shirts-for-scholarships/"),
    ("contact.", "/contact/"),
]

SERVICES = [
    ("screen printing.", "/services/screen-printing/", "Vibrant, durable prints. The most cost-effective choice for larger orders."),
    ("embroidery.", "/services/embroidery/", "A polished, premium look on polos, jackets, hats, and bags. Built to last."),
    ("fusion.", "/services/fusion/", "DTF transfers, vinyl, glitter, rhinestones, and puff. Small orders, big detail."),
    ("sublimation.", "/services/sublimation/", "Full-color, edge-to-edge designs that become part of the fabric."),
    ("live printing.", "/services/live-printing/", "We bring the press to your event and print shirts while guests watch."),
    ("online team stores.", "/services/e-commerce/", "A custom storefront for your group. No forms, no chasing payments. Free to set up."),
    ("state shirts.", "/services/state-shirts/", "Iowa pride, printed in Iowa. Our house line of state designs."),
    ("promo products.", PROMO_URL, "Drinkware, banners, teddy bears, even toilet paper. You think it, we'll ink it."),
]

CSS = r"""
:root{
  --ink:#1a1a1a; --paper:#ffffff; --gray:#6b6b6b; --line:#d9d9d9;
  --head:'Arial Black','Arial Bold',Arial,sans-serif;
  --body:Arial,Helvetica,sans-serif;
  --max:1120px;
}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{transition:none!important}}
body{font-family:var(--body);color:var(--ink);background:var(--paper);font-size:17px;line-height:1.65}
img{max-width:100%;height:auto;display:block}
a{color:inherit}
.wrap{max-width:var(--max);margin:0 auto;padding:0 24px}
h1,h2,h3{font-family:var(--head);font-weight:900;line-height:1.05;letter-spacing:-.5px}
h1{font-size:clamp(2.4rem,6vw,4.2rem);margin-bottom:.5em}
h2{font-size:clamp(1.7rem,3.6vw,2.6rem);margin-bottom:.6em}
h3{font-size:1.15rem;margin-bottom:.4em}
p{margin-bottom:1em}
p:last-child{margin-bottom:0}

/* header */
header{background:var(--ink);color:#fff;position:sticky;top:0;z-index:50;border-bottom:1px solid #000}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 24px;max-width:var(--max);margin:0 auto}
.brand{display:flex;align-items:center;gap:12px;text-decoration:none}
.brand img{width:48px;height:48px}
.brand span{font-family:var(--head);font-size:1.05rem;letter-spacing:.02em}
nav.main{display:flex;gap:22px;flex-wrap:wrap}
nav.main a{color:#fff;text-decoration:none;font-family:var(--head);font-size:.82rem;letter-spacing:.02em}
nav.main a:hover,nav.main a:focus{text-decoration:underline;text-underline-offset:4px}
.cta-btn{display:inline-block;background:#fff;color:var(--ink);font-family:var(--head);font-size:.85rem;padding:10px 18px;text-decoration:none;border:2px solid #fff}
.cta-btn:hover,.cta-btn:focus{background:var(--ink);color:#fff}
.cta-btn.inv{background:var(--ink);color:#fff;border-color:var(--ink)}
.cta-btn.inv:hover,.cta-btn.inv:focus{background:#fff;color:var(--ink)}
.menu-toggle{display:none}
details.mnav{display:none}
@media(max-width:900px){
  nav.main{display:none}
  details.mnav{display:block}
  details.mnav summary{list-style:none;cursor:pointer;font-family:var(--head);color:#fff;font-size:.9rem;padding:8px 12px;border:2px solid #fff}
  details.mnav summary::-webkit-details-marker{display:none}
  details.mnav[open] summary{background:#fff;color:var(--ink)}
  .mnav-panel{position:absolute;left:0;right:0;top:100%;background:var(--ink);border-top:1px solid #333;padding:12px 24px 20px;display:flex;flex-direction:column;gap:4px}
  .mnav-panel a{color:#fff;text-decoration:none;font-family:var(--head);font-size:1rem;padding:10px 0;border-bottom:1px solid #2c2c2c}
}

/* sections */
section{padding:72px 0}
.dark{background:var(--ink);color:#fff}
.texture{background:var(--ink) url('/assets/texture-white20.png') repeat;background-size:339px 449px;color:#fff}
.band{padding:44px 0}
.hero{padding:104px 0 96px}
.hero h1{max-width:14ch}
.hero p.lead{font-size:1.25rem;max-width:56ch;color:#e8e8e8}
.btn-row{display:flex;gap:14px;flex-wrap:wrap;margin-top:28px}

/* grids */
.grid{display:grid;gap:2px;background:var(--ink);border:2px solid var(--ink)}
.grid.cols4{grid-template-columns:repeat(4,1fr)}
.grid.cols3{grid-template-columns:repeat(3,1fr)}
.grid.cols2{grid-template-columns:repeat(2,1fr)}
@media(max-width:900px){.grid.cols4,.grid.cols3{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.grid.cols4,.grid.cols3,.grid.cols2{grid-template-columns:1fr}}
.cell{background:#fff;padding:28px 24px;text-decoration:none;display:block;transition:background .15s,color .15s}
a.cell:hover,a.cell:focus{background:var(--ink);color:#fff}
a.cell:hover .cellsub,a.cell:focus .cellsub{color:#cfcfcf}
.cellsub{color:var(--gray);font-size:.95rem}
.dark .cell{background:var(--ink);color:#fff}

/* stats */
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;text-align:center}
@media(max-width:700px){.stats{grid-template-columns:1fr}}
.stat b{font-family:var(--head);font-size:clamp(2rem,5vw,3.2rem);display:block}
.stat span{color:#bdbdbd;font-size:.95rem}

/* testimonials */
.quote{border-left:4px solid var(--ink);padding:4px 0 4px 22px;margin-bottom:28px}
.quote p{font-size:1.05rem}
.quote footer{font-family:var(--head);font-size:.85rem;margin-top:8px}

/* prose + faq */
.prose{max-width:70ch}
.prose h2{margin-top:1.6em}
.prose ul{margin:0 0 1em 1.2em}
.prose li{margin-bottom:.5em}
table{border-collapse:collapse;width:100%;margin:1em 0 1.5em}
th,td{border:2px solid var(--ink);padding:10px 14px;text-align:left}
th{font-family:var(--head);font-size:.85rem;background:var(--ink);color:#fff}
details.faq{border:2px solid var(--ink);margin-bottom:10px}
details.faq summary{cursor:pointer;font-family:var(--head);font-size:1rem;padding:16px 18px;list-style:none;display:flex;justify-content:space-between;gap:12px}
details.faq summary::-webkit-details-marker{display:none}
details.faq summary::after{content:"+";font-family:var(--head)}
details.faq[open] summary::after{content:"\2013"}
details.faq .a{padding:0 18px 18px;max-width:70ch}

/* steps */
.steps{counter-reset:step;display:grid;gap:0;border-left:2px solid var(--ink);margin-left:8px}
.step{position:relative;padding:0 0 28px 34px}
.step::before{counter-increment:step;content:counter(step);position:absolute;left:-19px;top:-2px;width:36px;height:36px;background:var(--ink);color:#fff;font-family:var(--head);display:flex;align-items:center;justify-content:center;font-size:1rem}
.step h3{padding-top:4px}

/* footer */
footer.site{background:var(--ink);color:#fff;padding:56px 0 40px}
.fgrid{display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px}
@media(max-width:800px){.fgrid{grid-template-columns:1fr}}
footer.site a{color:#fff}
footer.site .fine{color:#9a9a9a;font-size:.85rem;margin-top:34px;border-top:1px solid #333;padding-top:20px}
.flist{list-style:none}
.flist li{margin-bottom:8px}
/* split hero */
.hero-split{display:grid;grid-template-columns:1.05fr 1fr;background:var(--ink);color:#fff;min-height:440px}
.hs-text{padding:80px 48px 72px;display:flex;flex-direction:column;justify-content:center}
.hs-text .lead{font-size:1.2rem;max-width:48ch;color:#e8e8e8}
.hs-img{position:relative;min-height:320px}
.hs-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
@media(max-width:820px){.hero-split{grid-template-columns:1fr}.hs-text{padding:64px 24px 48px}.hs-img{min-height:260px}}
.imgband{padding:0;background:var(--ink)}
.imgband img{width:100%;max-height:480px;object-fit:cover;display:block;opacity:.92}
.splitrow{display:grid;grid-template-columns:1fr 1fr;background:var(--ink)}
.splitrow .sr-img{min-height:340px;position:relative}
.splitrow .sr-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.splitrow .sr-text{background:#fff;padding:64px 48px}
.splitrow.rev .sr-text{order:-1}
@media(max-width:820px){.splitrow{grid-template-columns:1fr}.splitrow.rev .sr-text{order:0}.sr-text{padding:48px 24px}}
.teamgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:var(--ink);border:2px solid var(--ink)}
@media(max-width:900px){.teamgrid{grid-template-columns:repeat(2,1fr)}}
.teamcard{background:#fff;padding:26px 18px;text-align:center}
.teamcard .avatar{width:84px;height:84px;border-radius:50%;background:var(--ink);color:#fff;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;font-family:var(--head);font-size:.7rem}
.teamcard h3{font-size:.95rem;margin-bottom:2px}
.teamcard p{color:var(--gray);font-size:.85rem;margin:0}

/* photo hero */
.hero.photo{background:linear-gradient(90deg,rgba(10,10,10,.88) 0%,rgba(10,10,10,.55) 55%,rgba(10,10,10,.25) 100%),var(--hero-img) center/cover no-repeat #111;color:#fff}
@media(max-width:700px){.hero.photo{background:linear-gradient(rgba(10,10,10,.82),rgba(10,10,10,.82)),var(--hero-img) center/cover no-repeat #111}}
.imgframe{border:2px solid var(--ink);display:block}
.photostrip{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:var(--ink);border:2px solid var(--ink)}
@media(max-width:700px){.photostrip{grid-template-columns:repeat(2,1fr)}}
.photostrip img{width:100%;height:100%;object-fit:cover;aspect-ratio:1/1}
.photostrip figure{margin:0;position:relative;background:#000}
.photostrip figcaption{position:absolute;left:0;bottom:0;background:var(--ink);color:#fff;font-family:var(--head);font-size:.72rem;padding:5px 10px}

/* marquee */
.marquee{background:var(--ink);color:#fff;overflow:hidden;border-top:2px solid var(--ink);border-bottom:2px solid var(--ink);padding:14px 0;white-space:nowrap}
.marquee .track{display:inline-block;animation:scroll 28s linear infinite;font-family:var(--head);font-size:1.25rem;letter-spacing:.02em}
.marquee span{margin:0 26px}
@keyframes scroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.marquee .track{animation:none}}

/* quiz */
.quiz{border:3px solid var(--ink);background:#fff;color:var(--ink);max-width:760px}
.quiz-head{background:var(--ink);color:#fff;padding:16px 22px;font-family:var(--head);display:flex;justify-content:space-between;align-items:center}
.quiz-body{padding:26px 22px}
.quiz h3{font-size:1.35rem;margin-bottom:18px}
.quiz-opts{display:grid;gap:10px}
.quiz-opts button{font-family:var(--head);font-size:.95rem;text-align:left;padding:14px 16px;background:#fff;border:2px solid var(--ink);cursor:pointer;transition:background .12s,color .12s}
.quiz-opts button:hover,.quiz-opts button:focus{background:var(--ink);color:#fff}
.quiz-result h3{font-size:1.8rem}
.quiz-result .cellsub{margin:10px 0 18px}
.quiz-reset{font-family:var(--head);font-size:.8rem;background:none;border:none;color:#fff;cursor:pointer;text-decoration:underline}
/* breadcrumbs */
.crumbs{font-family:var(--head);font-size:.78rem;letter-spacing:.04em;text-transform:lowercase;color:#666;margin:0 0 22px}
.crumbs a{color:#666;text-decoration:none}
.crumbs a:hover{text-decoration:underline}
.crumbs [aria-current]{color:var(--ink)}
.updated{font-size:.85rem;color:#666;font-style:italic}
.skip{position:absolute;left:-9999px;top:0;background:#fff;color:var(--ink);padding:10px 16px;z-index:100}
.skip:focus{left:12px;top:12px}
:focus-visible{outline:3px solid #1a1a1a;outline-offset:2px}
.dark :focus-visible,.texture :focus-visible,header :focus-visible,footer.site :focus-visible{outline-color:#fff}
"""

def esc(s): return html.escape(s, quote=True)

def layout(path, title, desc, body, extra_schema=None, og_type="website"):
    schemas = [LOCAL_BUSINESS]
    if extra_schema:
        schemas += extra_schema if isinstance(extra_schema, list) else [extra_schema]
    ld = "\n".join(
        f'<script type="application/ld+json">{json.dumps(s, separators=(",", ":"))}</script>'
        for s in schemas
    )
    canonical = BASE + path
    nav_links = "".join(f'<a href="{h}">{esc(t)}</a>' for t, h in NAV)
    mnav_links = "".join(f'<a href="{h}">{esc(t)}</a>' for t, h in NAV)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/logo-black.png">
<meta property="og:site_name" content="P&amp;M Apparel">
<meta name="twitter:card" content="summary">
<link rel="icon" href="/assets/logo-black.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header>
  <div class="bar">
    <a class="brand" href="/"><img src="/assets/logo-white.png" alt="P&amp;M Apparel home" width="52" height="52"></a>
    <nav class="main" aria-label="Main">{nav_links}</nav>
    <a class="cta-btn" href="{QUOTE_URL}">get a quote.</a>
    <details class="mnav">
      <summary aria-label="Menu">menu.</summary>
      <div class="mnav-panel">{mnav_links}<a href="{STORES_URL}">online stores.</a></div>
    </details>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site">
  <div class="wrap fgrid">
    <div>
      <img src="/assets/logo-white.png" alt="P&amp;M Apparel logo" width="64" height="64" style="margin-bottom:14px">
      <p><b>P&amp;M Apparel</b><br>{ADDR}<br>{CITY}, {STATE} {ZIP}</p>
      <p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p>Monday to Friday, 8am to 5pm</p>
    </div>
    <div>
      <h3>services.</h3>
      <ul class="flist">
        <li><a href="/services/screen-printing/">Screen printing</a></li>
        <li><a href="/services/embroidery/">Embroidery</a></li>
        <li><a href="/services/fusion/">Fusion &amp; DTF</a></li>
        <li><a href="/services/sublimation/">Sublimation</a></li>
        <li><a href="/services/live-printing/">Live printing</a></li>
        <li><a href="/services/e-commerce/">Online team stores</a></li>
        <li><a href="{PROMO_URL}">Promo products</a></li>
      </ul>
    </div>
    <div>
      <h3>more.</h3>
      <ul class="flist">
        <li><a href="{QUOTE_URL}">Get a quote</a></li>
        <li><a href="{STORES_URL}">Online stores</a></li>
        <li><a href="{IOD_URL}">Iowa On Demand</a></li>
        <li><a href="/shirts-for-scholarships/">Shirts for Scholarships</a></li>
        <li><a href="{SPONSOR_URL}">Sponsorship requests</a></li>
        <li><a href="{FB_URL}">Facebook</a> &middot; <a href="{IG_URL}">Instagram</a> &middot; <a href="{TT_URL}">TikTok</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap fine">
    <p>Good People. Great Gear. &copy; 2026 P&amp;M Apparel. Woman-owned and family-run in Polk City, Iowa since 1987. Serving Ankeny, the Des Moines metro, and teams everywhere.</p>
  </div>
</footer>
</body>
</html>"""

def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"):
        full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)

def service_schema(name, desc, path):
    return {
        "@context": "https://schema.org", "@type": "Service",
        "name": name, "description": desc,
        "provider": {"@id": BASE + "/#business"},
        "areaServed": "Des Moines metro and nationwide",
        "url": BASE + path,
    }

def faq_schema(pairs):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs
        ],
    }

def breadcrumbs(items):
    return {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u}
            for i, (n, u) in enumerate(items)
        ],
    }

def cta_band(heading="ready when you are.", sub="Tell us what you're thinking. Quotes are usually back within 24 hours."):
    return f"""
<section class="texture band">
  <div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:20px">
    <div><h2 style="margin-bottom:.2em">{heading}</h2><p style="color:#dcdcdc;margin:0">{sub}</p></div>
    <div class="btn-row" style="margin:0"><a class="cta-btn" href="{QUOTE_URL}">get a quote.</a><a class="cta-btn" style="background:transparent;color:#fff" href="tel:{PHONE_TEL}">call {PHONE}</a></div>
  </div>
</section>"""

def service_page(slug, h1, title, desc, when, body_html, faqs=None, img=None, img_alt="", name=None):
    path = f"/services/{slug}/"
    name = name or h1.rstrip('.').title()
    schema = [service_schema(name, desc, path),
              breadcrumbs([("Home", "/"), ("Services", "/services/"), (name, path)]),
              {"@context": "https://schema.org", "@type": "WebPage",
               "@id": BASE + path, "url": BASE + path, "name": title,
               "dateModified": TODAY,
               "about": {"@id": BASE + "/#business"}}]
    faq_html = ""
    if faqs:
        schema.append(faq_schema(faqs))
        faq_html = "<h2>common questions.</h2>" + "".join(
            f'<details class="faq"><summary>{esc(q)}</summary><div class="a"><p>{a}</p></div></details>'
            for q, a in faqs)
    if img:
        hero_html = f"""
<section class="hero-split">
  <div class="hs-text">
    <h1>{h1}</h1>
    <p class="lead">{when}</p>
    <div class="btn-row"><a class="cta-btn" href="{QUOTE_URL}">get a quote.</a></div>
  </div>
  <div class="hs-img"><img src="{img}" alt="{esc(img_alt)}"></div>
</section>"""
    else:
        hero_html = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>{h1}</h1>
    <p class="lead" style="font-size:1.2rem;max-width:58ch;color:#e8e8e8">{when}</p>
    <div class="btn-row"><a class="cta-btn" href="{QUOTE_URL}">get a quote.</a></div>
  </div>
</section>"""
    crumb_html = (f'<nav class="crumbs" aria-label="Breadcrumb">'
                  f'<a href="/">home</a> &rsaquo; <a href="/services/">services</a> &rsaquo; '
                  f'<span aria-current="page">{esc(name.lower())}</span></nav>')
    body = f"""
{hero_html}
<section>
  <div class="wrap prose">
    {crumb_html}
    {body_html}
    {faq_html}
  </div>
</section>
{cta_band()}"""
    write(path, layout(path, title, desc, body, schema))

# ---------------------------------------------------------------- HOME
def home():
    tiles = "".join(
        f'<a class="cell" href="{h}"><h3>{esc(n)}</h3><p class="cellsub">{esc(d)}</p></a>'
        for n, h, d in SERVICES)
    testimonials = [
        ("The team at P&M Apparel are fantastic. Timely, communicative, and thoughtful about their work. They listened well to what we needed and translated our vision into something tangible. The quality of the materials and print were excellent. The people are even better.", "Adrianne Towe", "Waukee Community Schools Foundation"),
        ("Amazing work and the staff are the best. I just got a behind-the-scenes tour of their facility. I don't think anyone understands how much work truly goes into the production of a t-shirt. Thank you for always going above and beyond.", "Evie McPherson", "Encore Dance"),
        ("Absolutely amazing people to work with. Prompt responses, knew exactly what I needed, and they did all the shipping. Everything went out less than three weeks from the closing date. And the quality is phenomenal.", "Michelle Petty", "Rebel Legion"),
        ("We have ordered from P&M Apparel multiple times. T-shirts, hoodies, hats, banners and more. Quality surpassed expectations. Customer service and communication is top notch.", "Mayra Worley", "Nick's Painting Plus"),
    ]
    quotes = "".join(
        f'<div class="quote"><p>&ldquo;{esc(t)}&rdquo;</p><footer>{esc(n)} // {esc(o)}</footer></div>'
        for t, n, o in testimonials)
    review_schema = {
        "@context": "https://schema.org", "@type": "LocalBusiness",
        "@id": BASE + "/#business",
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5",
                            "bestRating": "5", "reviewCount": str(len(testimonials))},
        "review": [
            {"@type": "Review", "reviewBody": t,
             "author": {"@type": "Person", "name": n},
             "reviewRating": {"@type": "Rating", "ratingValue": "5"}}
            for t, n, o in testimonials
        ],
    }
    website_schema = {
        "@context": "https://schema.org", "@type": "WebSite",
        "@id": BASE + "/#website", "url": BASE + "/",
        "name": "P&M Apparel",
        "publisher": {"@id": BASE + "/#business"},
    }
    body = f"""
<section class="hero photo" style="--hero-img:url('/assets/photos/hero-floor.jpg')">
  <div class="wrap">
    <h1>custom apparel in polk city, iowa. we can do that.</h1>
    <p class="lead">Screen printing, embroidery, and promotional products for schools, businesses, and teams across the Des Moines metro and beyond. Third-generation family shop. Woman-owned. Let's make something people are proud to wear.</p>
    <div class="btn-row">
      <a class="cta-btn" href="{QUOTE_URL}">get a quote.</a>
      <a class="cta-btn" style="background:transparent;color:#fff" href="{STORES_URL}">shop online stores.</a>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>one shop. every method.</h2>
    <div class="grid cols4">{tiles}</div>
  </div>
</section>
<section class="imgband"><img src="/assets/photos/floor-three-working.jpg" alt="The P&M Apparel production floor mid-shift" loading="lazy"></section>
<section class="dark band">
  <div class="wrap stats">
    <div class="stat"><b>1987</b><span>three generations of family under one roof</span></div>
    <div class="stat"><b>50 + 29</b><span>states and countries we shipped to last year</span></div>
    <div class="stat"><b>90%</b><span>of our business comes from referrals</span></div>
  </div>
</section>
<section class="splitrow">
  <div class="sr-img"><img src="/assets/photos/qc-two-inspect-shirt.jpg" alt="Checking a finished shirt on the production floor" loading="lazy"></div>
  <div class="sr-text prose">
    <h2>good shirts get worn. great shirts get remembered.</h2>
    <p>That's the difference we're chasing. Nobody's really buying shirts. They're buying school pride, employee culture, fundraising, memories, belonging. The shirt is just the vehicle.</p>
    <p><b>Real people, real advice.</b> We ask questions. We make recommendations. We help you pick the right method instead of leaving you to guess.</p>
    <p><b>Everything under one roof.</b> Printing, embroidery, promo, online stores, on-demand, live events. One partner instead of five vendors.</p>
    <p><b>Quality you can see.</b> We check the art, check the order, and check the goods before they leave. Details matter.</p>
    <p><b>No babysitting required.</b> It arrives on time. It looks right. People actually wear it. That's the whole point.</p>
    <p>You can order a shirt from anywhere. You can't order a partner.</p>
  </section>
<section class="dark">
  <div class="wrap">
    <h2>from idea to pickup.</h2>
    <div class="steps" style="border-color:#fff">
      <div class="step" style="--x:0"><h3>reach out.</h3><p>Walk in, call, email, or use the quote form. Whatever's easiest.</p></div>
      <div class="step"><h3>meet your account manager.</h3><p>One person guides your whole order: decoration method, blank garments, online stores, all of it.</p></div>
      <div class="step"><h3>approve your quote.</h3><p>Quotes are usually back within 24 hours. A 50% deposit sends your job into art.</p></div>
      <div class="step"><h3>approve your proof.</h3><p>Every job gets a proof. Nothing prints until you've signed off.</p></div>
      <div class="step"><h3>pick up or ship.</h3><p>Standard turnaround is 8 to 10 business days after art approval. We shipped to all 50 states and 29 countries last year.</p></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>good people. great gear.</h2>
    {quotes}
  </div>
</section>
<section class="dark band">
  <div class="wrap" style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:20px">
    <div><h2 style="margin-bottom:.2em">giving back.</h2><p style="color:#dcdcdc;margin:0">Scholarships for graduating seniors, sponsorships, and donations for the communities that built us.</p></div>
    <a class="cta-btn" href="/shirts-for-scholarships/">learn more.</a>
  </div>
</section>
{cta_band()}"""
    title = "P&M Apparel | Screen Printing & Embroidery in Polk City, IA"
    desc = "Woman-owned, third-generation custom apparel shop serving Ankeny and the Des Moines metro since 1987. Screen printing, embroidery, DTF, promo products, and free online team stores."
    write("/", layout("/", title, desc, body, [review_schema, website_schema]))

# ---------------------------------------------------------------- SERVICES INDEX
def services_index():
    tiles = "".join(
        f'<a class="cell" href="{h}"><h3>{esc(n)}</h3><p class="cellsub">{esc(d)}</p></a>'
        for n, h, d in SERVICES)
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>every method. one roof.</h1>
    <p class="lead">Not sure which method fits? That's literally our job. Here's the plain-English version. We're a phone call away for the rest.</p>
  </div>
</section>
<section>
  <div class="wrap"><div class="grid cols4">{tiles}</div></div>
</section>
<section class="dark">
  <div class="wrap">
    <h2>which one is right for you?</h2>
    <p style="color:#dcdcdc;max-width:60ch;margin-bottom:26px">Three quick questions. We'll point you to the cleanest route. (And if the quiz is wrong, a human will happily overrule it.)</p>
    <div class="quiz" id="quiz">
      <div class="quiz-head"><span id="quiz-step">question 1 of 3.</span><button class="quiz-reset" id="quiz-reset" style="display:none">start over</button></div>
      <div class="quiz-body" id="quiz-body"></div>
    </div>
  </div>
</section>
<script>
(function(){{
  var Q=[
    {{q:"how many pieces are we talking?",o:[["Just 1 to 11","small"],["A solid batch, 12 to 47","med"],["48 or more. Go big.","big"]]}},
    {{q:"what's the look you're after?",o:[["Bold and budget-friendly","bold"],["Premium and stitched","stitch"],["Photo-real, full color","photo"],["Edge-to-edge, all over the garment","allover"]]}},
    {{q:"what's it going on?",o:[["Cotton tees or blends","cotton"],["Light polyester athletic wear","poly"],["Hats, jackets, polos, or bags","structured"]]}}
  ];
  var R={{
    screen:{{t:"screen printing.",d:"Bold, durable, and the best per-piece price at quantity. The workhorse.",u:"/services/screen-printing/"}},
    embroidery:{{t:"embroidery.",d:"Stitched, premium, built to last. The professional look for polos, jackets, hats, and bags.",u:"/services/embroidery/"}},
    fusion:{{t:"fusion.",d:"DTF transfers, vinyl, glitter, and puff. Incredible detail on small runs with a soft feel.",u:"/services/fusion/"}},
    sublimation:{{t:"sublimation.",d:"Full-color ink that becomes part of the fabric. No crack, no peel, no feel.",u:"/services/sublimation/"}}
  }};
  var a=[],body=document.getElementById("quiz-body"),step=document.getElementById("quiz-step"),reset=document.getElementById("quiz-reset");
  function pick(){{
    if(a[1]==="stitch"||(a[1]!=="allover"&&a[2]==="structured"))return"embroidery";
    if(a[1]==="allover")return a[2]==="poly"?"sublimation":"fusion";
    if(a[1]==="photo")return a[2]==="poly"?"sublimation":"fusion";
    if(a[0]==="small")return"fusion";
    return"screen";
  }}
  function ask(i){{
    step.textContent="question "+(i+1)+" of 3.";reset.style.display=i?"inline":"none";
    var h="<h3>"+Q[i].q+"</h3><div class='quiz-opts'>";
    Q[i].o.forEach(function(o){{h+="<button data-v='"+o[1]+"'>"+o[0]+"</button>";}});
    body.innerHTML=h+"</div>";
    body.querySelectorAll("button").forEach(function(b){{b.onclick=function(){{a[i]=b.dataset.v;i<2?ask(i+1):done();}};}});
  }}
  function done(){{
    var r=R[pick()];step.textContent="we can do that.";reset.style.display="inline";
    body.innerHTML="<div class='quiz-result'><h3>"+r.t+"</h3><p class='cellsub'>"+r.d+"</p><div class='btn-row' style='margin-top:6px'><a class='cta-btn inv' href='"+r.u+"'>see how it works.</a><a class='cta-btn inv' style='background:#fff;color:#1a1a1a' href='{QUOTE_URL}'>get a quote.</a></div></div>";
  }}
  reset.onclick=function(){{a=[];ask(0);}};
  ask(0);
}})();
</script>
{cta_band()}"""
    title = "Custom Apparel Services | Screen Printing, Embroidery & More | P&M Apparel"
    desc = "Screen printing, embroidery, DTF fusion transfers, sublimation, live event printing, online team stores, and promotional products in Polk City, Iowa."
    write("/services/", layout("/services/", title, desc, body,
        breadcrumbs([("Home", "/"), ("Services", "/services/")])))

# ---------------------------------------------------------------- SERVICE PAGES
def all_services():
    service_page(
        "screen-printing", "screen printing in polk city &amp; des moines.",
        "Screen Printing in Des Moines & Polk City, IA | P&M Apparel",
        "Custom screen printing in Polk City, Iowa. Vibrant, durable prints for teams, schools, and businesses. 12-piece minimum, 8-10 day turnaround, quotes within 24 hours.",
        "The most cost-effective choice for larger quantities. Vibrant, durable prints that hold up to years of washing and everyday wear.",
        f"""
<h2>built for bulk. built to last.</h2>
<p>Screen printing pushes ink directly through a mesh screen onto the garment, one color at a time. It's the workhorse of custom apparel: bold color, unbeatable durability, and per-piece pricing that gets better as your order grows. Team shirts, staff tees, event merch, spirit wear. If you need a lot of great-looking shirts, this is usually the cleanest route.</p>
<h2>minimums by color count.</h2>
<table>
<tr><th>colors in your design</th><th>minimum quantity</th></tr>
<tr><td>1 to 3 colors</td><td>12 pieces</td></tr>
<tr><td>4 to 6 colors</td><td>24 pieces</td></tr>
<tr><td>7 to 10 colors</td><td>48 pieces</td></tr>
</table>
<p>Under the minimum? We can still help. Orders below minimum carry a $35 per-screen charge, or our <a href="/services/fusion/">fusion methods</a> may fit small runs better. We'll point you the right way.</p>
<h2>how it works.</h2>
<div class="steps">
  <div class="step"><h3>art.</h3><p>Send your logo or idea. Vector files are ideal; our in-house art department can clean up or recreate anything else.</p></div>
  <div class="step"><h3>proof.</h3><p>You approve a quote and a digital proof before anything prints. No surprises.</p></div>
  <div class="step"><h3>screens.</h3><p>We burn one screen per color and dial in registration and ink.</p></div>
  <div class="step"><h3>print.</h3><p>Your order runs on the press, color by color, then cures for maximum durability.</p></div>
  <div class="step"><h3>quality check.</h3><p>Every order is inspected, counted, and folded before pickup or shipping.</p></div>
</div>
<p>Who's it for? Schools and spirit wear, corporate and staff tees, event and fundraiser merch (see <a href="/shirts-for-scholarships/">Shirts for Scholarships</a>), and teams of every kind — pair it with an <a href="/services/e-commerce/">online team store</a> and let everyone order their own size.</p>
<h2>the work.</h2>
<div class="photostrip">
  <figure><img src="/assets/photos/floor-three-working.jpg" alt="Three P&amp;M Apparel printers working the production floor" loading="lazy"><figcaption>on the floor.</figcaption></figure>
  <figure><img src="/assets/photos/press-loading-pink.jpg" alt="Loading a pink shirt onto the screen printing press" loading="lazy"><figcaption>on the press.</figcaption></figure>
  <figure><img src="/assets/photos/qc-two-inspect-shirt.jpg" alt="Two team members inspecting a finished screen printed shirt" loading="lazy"><figcaption>quality check.</figcaption></figure>
  <figure><img src="/assets/photos/packing-order-table.jpg" alt="Packing a finished screen printing order at the table" loading="lazy"><figcaption>packed to go.</figcaption></figure>
</div>
<h2>the details.</h2>
<p>Standard turnaround is 8 to 10 business days after art approval (up to 12 in peak season). We print on Gildan, Bella+Canvas, Comfort Colors, Carhartt, Nike, Adidas, Under Armour, and more. Pantone color matching available. Every job gets a quote approval and a proof approval before anything prints.</p>
<p class="updated">Minimums, turnaround, and pricing details current as of {UPDATED_HUMAN}.</p>""",
        faqs=[
            ("How much does screen printing cost?", "Every job is unique and quoted as such, based on quantity, number of colors and locations, and garment choice. Quotes are usually back within 24 hours. Bulk orders get better per-piece pricing."),
            ("What is the minimum order for screen printing?", "12 pieces for designs with 1 to 3 colors, 24 pieces for 4 to 6 colors, and 48 pieces for 7 to 10 colors. Below-minimum orders carry a $35 per-screen charge."),
            ("How fast can I get my order?", "Standard turnaround is 8 to 10 business days after art approval. Rush orders are available: same day if we have the item in stock, generally next day if we need to order it."),
            ("Can you print my existing logo?", "Yes. Vector files (AI, EPS, PDF) are preferred and high-res PNGs are accepted. Our in-house art department can also clean up or recreate artwork at $100 per hour, with the first 30 minutes free on most orders."),
        ], img="/assets/photos/press-loading-pink.jpg", img_alt="Loading a shirt onto the press at P&M Apparel",
        name="Screen Printing")

    service_page(
        "embroidery", "embroidery.",
        "Custom Embroidery in Des Moines & Polk City, IA | P&M Apparel",
        "Custom embroidery on polos, jackets, hats, and bags in Polk City, Iowa. One-piece minimum, in-house digitizing, Pantone thread matching, and customer-supplied garments welcome.",
        "A polished, professional look on polos, jackets, hats, or bags. Stitched logos add texture and a premium feel that's built to last.",
        f"""
<h2>the premium touch.</h2>
<p>Embroidery stitches your logo directly into the fabric with thread. It reads as quality from across the room, which is why it's the standard for company polos, quarter-zips, jackets, caps, and bags. It doesn't crack, fade, or peel. It just lasts.</p>
<h2>one piece minimum.</h2>
<p>Unlike screen printing, embroidery has no real minimum. Order one jacket or one hundred. There's a one-time $35 setup fee to digitize your logo, and after that it's on file with us forever.</p>
<h2>bring your own garments.</h2>
<p>Already have jackets, hats, or sweaters you love? Bring them in. We decorate customer-supplied garments all the time; we just ask you to sign a simple waiver first, and our team will double-check that your items are a good fit for the machine. Read the full guide: <a href="/customer-supplied-garments/">customer-supplied garments</a>.</p>
<h2>the details.</h2>
<p>Our embroidery technicians color-match thread to existing logos on request, and you're always welcome to choose thread colors yourself. Hats, thick knits, and technical fabrics each have quirks; we'll flag anything before we stitch. Every job gets a proof approval first.</p>""",
        faqs=[
            ("Is there a minimum order for embroidery?", "No. Embroidery is a one-piece minimum, so you can order a single jacket or hat."),
            ("What does embroidery setup cost?", "There's a one-time $35 setup fee to digitize your logo. Once it's digitized, it stays on file for all future orders."),
            ("Can you embroider items I already own?", "Yes. We welcome customer-supplied garments. We ask you to fill out a short waiver first, and our staff will happily double-check your items before we run them."),
            ("Can you embroider hats?", "Yes, though hats are the trickiest canvas. Full-fabric caps can often take side embroidery, trucker caps with plastic mesh cannot, and small panels may require simplifying fine details. Bring your hat in and we'll tell you exactly what's possible."),
        ], img="/assets/photos/emb-worker-hat-machine-close.jpg", img_alt="Hooping a hat on the embroidery machine at P&M Apparel")

    service_page(
        "fusion", "fusion.",
        "DTF Transfers, Vinyl & Specialty Prints in Iowa | P&M Apparel",
        "Fusion decoration at P&M Apparel: DTF transfers, vinyl, glitter, rhinestones, and puff. Perfect for small orders, names and numbers, and detailed full-color designs. One-piece minimum.",
        "Ideal for smaller orders, names and numbers, or highly detailed full-color artwork that isn't practical for screen printing.",
        f"""
<h2>what fusion means here.</h2>
<p>Fusion is our family of heat-applied decoration: DTF (direct-to-film) transfers, vinyl, glitter, rhinestones, and puff. If you've seen a photo-quality print on a single shirt, sparkly team names, or raised 3D lettering, you've seen fusion work.</p>
<h2>when to choose it.</h2>
<p>Fusion shines when screen printing doesn't make sense: one-off shirts, small batches, player names and numbers, or artwork with tons of colors and fine detail. You get incredible detail, a soft hand feel, and quick turnaround without sacrificing durability. One-piece minimum.</p>
<h2>mix and match.</h2>
<p>Fusion plays well with everything else we do. Screen print the front, fusion the personalized names on the back. Add glitter numbers to sublimated jerseys. Your account manager will spec the combination that fits your design and budget.</p>""",
        faqs=[
            ("What is a DTF transfer?", "DTF stands for direct-to-film. Your design is printed in full color onto a special film, then heat-pressed onto the garment. It handles fine detail and unlimited colors with a soft feel and strong durability."),
            ("What's the minimum order for fusion?", "One piece. Fusion is our go-to for small orders and one-offs."),
            ("Can you do names and numbers for my team?", "Yes. Personalized names and numbers are one of the most common fusion jobs we run, often combined with screen printing or sublimation on the same garments."),
        ], img="/assets/photos/fusion-align-transfer.jpg", img_alt="Aligning a transfer at the fusion station")

    service_page(
        "sublimation", "sublimation.",
        "Sublimation Printing in Iowa | Full-Color Custom Apparel | P&M Apparel",
        "Sublimation printing in Polk City, Iowa. Full-color, edge-to-edge designs on light polyester that never crack or peel. One-piece minimum. Quotes within 24 hours.",
        "Perfect for full-color, edge-to-edge designs on light-colored polyester garments. The ink becomes part of the fabric.",
        f"""
<h2>ink that becomes fabric.</h2>
<p>Sublimation uses heat to turn ink into gas that bonds permanently with polyester fibers. The result is a print you can't feel: no crack, no peel, no added weight, ever. It's how all-over prints, photo-real jerseys, and vivid pattern work get made.</p>
<h2>when to choose it.</h2>
<p>Choose sublimation for full-color, edge-to-edge designs on light-colored polyester. Athletic jerseys, all-over prints, and vibrant designs with gradients and photos are its sweet spot. Because the ink dyes the fabric itself, it needs polyester content and light base colors to work its magic.</p>
<h2>the details.</h2>
<p>One-piece minimum. Standard 8 to 10 business day turnaround after art approval. Pairs beautifully with fusion names and numbers for team uniforms.</p>""",
        faqs=[
            ("Will a sublimated print crack or fade?", "No. The ink becomes part of the fabric rather than sitting on top of it, so there's nothing to crack, peel, or feel."),
            ("Can you sublimate on cotton or dark shirts?", "Sublimation requires light-colored, high-polyester fabric. For cotton or dark garments, our fusion (DTF) method delivers similar full-color detail. We'll recommend the right method for your garment."),
        ])

    service_page(
        "live-printing", "live printing.",
        "Live Screen Printing for Events in Iowa | P&M Apparel",
        "Live event screen printing in the Des Moines metro. We bring the press to your grand opening, festival, or company event and print custom shirts on-site while guests watch.",
        "We bring the printing press to your event and print apparel on-site while your guests watch.",
        f"""
<h2>merch, but make it a moment.</h2>
<p>Live printing is exactly what it sounds like: we bring the press to your event and print shirts on-site while your guests watch. Instead of taking home a giveaway they'll forget, they leave with a custom shirt made just for them. It's an experience people remember long after the event is over.</p>
<h2>events it's built for.</h2>
<p>Grand openings, company celebrations, trade shows, conferences, community festivals, school events, sporting events, fundraisers, product launches, employee appreciation days, and customer appreciation events. If you want to draw a crowd, start conversations, and hand people something they'll actually wear, this is one of the most memorable ways to do it.</p>
<h2>we handle everything.</h2>
<p>Equipment, setup, production, and cleanup are all on us. You enjoy the event while your guests watch their shirts come to life.</p>""",
        faqs=[
            ("How does live printing work at an event?", "We bring a screen printing press, blank garments, and our crew to your venue, set up a printing station, and print shirts on the spot as guests watch and pick theirs up warm off the press."),
            ("What do I need to provide for live printing?", "Just the space and the crowd. We handle equipment, setup, production, and cleanup, and we'll work with you ahead of time on designs and garment choices."),
        ])

    service_page(
        "e-commerce", "online team stores.",
        "Free Online Team Stores for Schools & Teams in Iowa | P&M Apparel",
        "Free online team stores built and managed by P&M Apparel. No paper forms, no chasing payments, no leftover inventory. Perfect for Iowa schools, teams, clubs, and businesses.",
        "A simple, organized way for your group to order custom apparel. No paper forms. No chasing payments. No cost to set up.",
        f"""
<h2>stop chasing sizes and money.</h2>
<p>Online team stores give your group a simple, organized way to order custom apparel without passing around paper forms or collecting money. We build a custom storefront with your approved designs, and everyone orders exactly what they want, pays online, and has their order produced and delivered through us.</p>
<h2>who they're for.</h2>
<p>Schools, athletic teams, youth organizations, businesses, nonprofits, booster clubs, events, and fundraisers. If you're tired of tracking sizes, chasing payments, or ending up with extra inventory, an online store takes all of that off your plate while giving everyone more choices.</p>
<h2>what it costs you.</h2>
<p>Nothing. There is no cost to have us build and manage your online store. We handle setup, product selection, artwork, online ordering, payment collection, and reporting. You share the link with your group and let us take care of the rest.</p>
<p>Whether you need a short-term store for a fundraiser or team season, or a year-round company apparel store, we'll recommend the option that fits. Behind the scenes we use Chipply, an industry-leading platform built specifically for custom apparel programs, so your store is easy to shop, secure, and reliable.</p>
<p><a class="cta-btn inv" href="{STORES_URL}">browse current stores.</a></p>""",
        faqs=[
            ("How much does it cost to set up an online team store?", "Nothing. P&M Apparel builds and manages your online store at no cost. We handle setup, artwork, ordering, payment collection, and reporting."),
            ("How do people order from a team store?", "You share a link with your group. Everyone shops the approved designs, picks their sizes, and pays online. Orders are produced and delivered through us."),
            ("Can a store run year-round?", "Yes. We run short-term stores for seasons and fundraisers as well as year-round company and school stores, and we'll recommend which fits your goals."),
        ], img="/assets/photos/packing-order-table.jpg", img_alt="Packing team store orders at P&M Apparel")

    service_page(
        "state-shirts", "state shirts.",
        "State Tournament Shirts in Iowa | Fast Turnaround | P&M Apparel",
        "Your team made it to state. P&M Apparel prints state tournament shirts fast, designed in-house in Polk City, so fans and players have gear before the big game.",
        "Your team punched their ticket to state. Now everyone needs the shirt, and they need it fast. That's our specialty.",
        f"""
<h2>you made it to state. now look like it.</h2>
<p>When your team qualifies for a state tournament, the window between "we're in!" and game day is tiny. State shirts are our rush specialty: our in-house art department turns your school, your sport, and your bracket run into gear that fans, players, and parents actually want to wear, on a timeline that works.</p>
<h2>how it works.</h2>
<p>Call us the moment you qualify. We'll have art moving the same day, and because we print in our own shop in Polk City, we control the schedule. Pair it with a quick <a href="/services/e-commerce/">online store</a> so parents and fans order their own sizes and pay online, with nothing for the booster club to collect or sort.</p>
<p>Every sport, every season, every level. Football, volleyball, wrestling, basketball, soccer, track, cheer, dance, esports. If they're headed to state, we can do that.</p>""")

def csg_page():
    path = "/customer-supplied-garments/"
    faqs = [
        ("Can I bring in my own garments to be decorated?", "Absolutely. Our customer-supplied garments policy lets you bring in items you already own to have them decorated with your logo. We ask you to fill out a short waiver first, and you're always welcome to bring items in for a double check with our staff."),
        ("Why do I need to sign a waiver?", "We take immense care of every item brought into our shop, but accidents happen: fabrics pull and machines break down. Because we didn't source the garments originally, the waiver simply states we won't source replacements."),
        ("Will embroidery affect my waterproof jacket?", "Yes. Embroidery stitches thread through the fabric, and thread carries water. A waterproof item will no longer be fully waterproof after embroidery, so weigh that before decorating technical outerwear."),
    ]
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>customer-supplied garments.</h1>
    <p class="lead">Bring in the jackets, hats, and sweaters you already love. Here's how it works and what to check before you do.</p>
  </div>
</section>
<section>
  <div class="wrap prose">
    <p>Many clients don't realize you can bring us items you already wear and have them decorated with your brand or logo. You absolutely can. Before every customer-supplied order we ask you to fill out a short <b>customer-supplied garments waiver</b>. We take immense care of every item in our shop, but accidents happen, fabrics pull, and machines break down. The waiver simply states that since we didn't source the garments, we won't source replacements. And you're always welcome to bring items in so our staff can double-check them first.</p>
    <h2>fabric checks.</h2>
    <ul>
      <li><b>Weight.</b> Thinner fabric can catch and become damaged, and lightweight fabric can sag under larger, thicker designs. Quick test: if a safety pin weighs the fabric down or creates a catch, think twice.</li>
      <li><b>How it lays.</b> Some cardigans and deep V-necks fall so a chest design would sit near the underarm. Picture where the design lands when the garment is actually on a body.</li>
      <li><b>Size of item vs. size of design.</b> Embroidery that looks right on a men's L can look oversized on a women's XS, and some sleeves are simply too small.</li>
      <li><b>Stretch.</b> Overly stretchy fabrics (poly with spandex) can bubble around a design or damage the fabric after embroidery.</li>
    </ul>
    <h2>placement checks.</h2>
    <ul>
      <li><b>Over pockets or existing logos.</b> Stacking designs gets bulky fast, and a design over a pocket can end up sitting on the collarbone instead of over the heart. We may suggest a different location to keep things cohesive.</li>
      <li><b>Short sleeves.</b> We center designs on the sleeve; oversized designs can bubble.</li>
      <li><b>Dress shirt cuffs.</b> Cuffs need to lay flat with room for the design to stay visible when buttoned. Gathered cuffs can't be embroidered.</li>
    </ul>
    <h2>function checks.</h2>
    <ul>
      <li><b>Pockets.</b> Some pockets end up sewn shut, especially where external and internal pockets overlap.</li>
      <li><b>Weatherproofing.</b> Embroidery makes thread holes, and thread carries water. Waterproof items won't be fully waterproof afterward.</li>
    </ul>
    <h2>hats are their own animal.</h2>
    <p>Location, design detail, and hat construction drastically change what's possible. Trucker caps with plastic mesh can't take side embroidery; full-fabric baseball caps often can. Single side panels need smaller, simplified designs. Thick-knit stocking caps (and thick sweaters or quilted jackets) may need an underlay of thread to keep designs visible.</p>
    <h2>color matching.</h2>
    <p>On request, our embroidery technicians do their best to color-match thread to existing designs on your garments. We can't always be exact, and you're welcome to choose thread colors yourself at any time.</p>
  </div>
</section>
{cta_band("have something in your closet?", "Bring it by Monday to Friday, 8am to 5pm, and we'll take a look together.")}"""
    title = "Customer-Supplied Garments Guide | P&M Apparel"
    desc = "Yes, you can bring your own garments to P&M Apparel for embroidery or printing. Our guide covers the waiver, fabric and placement checks, hats, and color matching."
    write(path, layout(path, title, desc, body, [faq_schema(faqs), breadcrumbs([("Home", "/"), ("Customer-Supplied Garments", path)])]))

# ---------------------------------------------------------------- OTHER PAGES
def about():
    path = "/about-us/"
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>our story is driving your story.</h1>
    <p class="lead">Third-generation. Woman-owned. Family-run since 1987.</p>
  </div>
</section>
<section>
  <div class="wrap prose">
    <h2>literally a mom and pop shop.</h2>
    <p>P&amp;M Apparel started in the basement of Phyllis and Melvin (the P and the M), who took up custom apparel as a new career after farming and remodeling homes most of their lives. Their daughter Kay took over a few years after the business moved to Polk City, and two of her children, Megan and Ryan, joined the ranks as it grew. Megan and Ryan took over ownership in 2023.</p>
    <p>Since 1987, we've helped businesses, schools, nonprofits, and communities create apparel people are proud to wear, through screen printing, embroidery, promotional products, online stores, and on-demand fulfillment. We've grown from Central Iowa to the whole state, the country, and lately, the world. Last year alone we shipped to all 50 states and 29 countries.</p>
    <h2>what we believe.</h2>
    <p>Great apparel builds belonging. Great service still matters. Fast answers matter. Keeping your word matters. That mindset has carried P&amp;M through decades of change while we keep evolving with better systems, stronger creativity, smarter technology, and a team that genuinely cares.</p>
    <p>We're not just decorators. We're problem solvers, idea generators, deadline hitters, and brand builders. We combine real production knowledge with practical business thinking, so you get solutions that work in the real world, not just on paper.</p>
    <p>90% of our business comes from referrals. That's not an accident. It's the relationships.</p>
  </div>
</section>
<section class="splitrow rev">
  <div class="sr-img"><img src="/assets/photos/family-photo-on-press.jpg" alt="A family photo taped to the press at P&M Apparel" loading="lazy"></div>
  <div class="sr-text prose">
    <h2>the photo on the press.</h2>
    <p>Walk the production floor and you'll find a small snapshot taped to the side of one of our presses: three generations of the women who built this company. It's not decoration. It's a reminder of whose name is on the sign.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <h2>the crew.</h2>
    <p style="max-width:60ch;margin-bottom:26px">Sixteen people who print it, stitch it, pack it, and answer the phone when you call. Faces and names coming soon.</p>
    <div class="teamgrid"><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div><div class="teamcard"><div class="avatar">P&amp;M</div><h3>team member.</h3><p>role goes here</p></div></div>
  </div>
</section>
<section class="imgband"><img src="/assets/photos/building-sign-close.jpg" alt="The P&M Apparel building and sign in Polk City" loading="lazy"></section>
<section class="dark band">
  <div class="wrap stats">
    <div class="stat"><b>3</b><span>generations of family under one roof</span></div>
    <div class="stat"><b>1987</b><span>the year it all started in a basement</span></div>
    <div class="stat"><b>100%</b><span>of our art is custom, made in-house</span></div>
  </div>
</section>
{cta_band("come say hi.", "1100 S 5th St in Polk City. Monday to Friday, 8am to 5pm.")}"""
    title = "About P&M Apparel | Woman-Owned Custom Apparel in Iowa Since 1987"
    desc = "P&M Apparel is a woman-owned, third-generation family business in Polk City, Iowa. From Phyllis and Melvin's basement in 1987 to shipping worldwide today."
    schema = {
        "@context": "https://schema.org", "@type": "AboutPage",
        "url": BASE + path, "about": {"@id": BASE + "/#business"},
    }
    write(path, layout(path, title, desc, body, [schema, breadcrumbs([("Home", "/"), ("About Us", path)])]))

def iowa_on_demand():
    path = "/iowa-on-demand/"
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>school pride, on demand.</h1>
    <p class="lead">No bulk orders. No guessing sizes. No leftover boxes.</p>
    <div class="btn-row"><a class="cta-btn" href="{IOD_URL}">shop iowa on demand.</a></div>
  </div>
</section>
<section>
  <div class="wrap prose">
    <p>Iowa On Demand is P&amp;M Apparel's on-demand offshoot, built for local schools. Right now it serves 12 Iowa school districts, with more joining all the time.</p>
    <p>Here's how it works. Fans shop online whenever they want. Each item is produced as orders come in, decorated in-house by our team in Polk City, and shipped fast. No order windows. No leftover boxes in the booster club president's garage. Just school pride, ready when people want it.</p>
    <p>Want your district on Iowa On Demand? <a href="{QUOTE_URL}">Reach out.</a> We can do that.</p>
  </div>
</section>
{cta_band()}"""
    title = "Iowa On Demand | On-Demand School Spirit Wear | P&M Apparel"
    desc = "Iowa On Demand is P&M Apparel's print-on-demand offshoot serving 12 Iowa school districts. Fans shop anytime, gear is decorated in-house in Polk City and shipped fast."
    write(path, layout(path, title, desc, body, breadcrumbs([("Home", "/"), ("Iowa On Demand", path)])))

def scholarships():
    path = "/shirts-for-scholarships/"
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>giving back.</h1>
    <p class="lead">Scholarships, sponsorships, and donations for the communities that have supported us for nearly 40 years.</p>
  </div>
</section>
<section>
  <div class="wrap prose">
    <h2>shirts for scholarships.</h2>
    <p>Every year, we award need-based scholarships to graduating seniors in the school districts we serve, helping them take the next step toward a two-year or four-year college, university, or trade program.</p>
    <p>This isn't a one-time promotion. It's an ongoing commitment to investing in local students. Applicants submit an application, recipients are selected based on need and other program criteria, and scholarship funds are awarded after proof of enrollment.</p>
    <h2>sponsorships and donations.</h2>
    <p>Teams, events, fundraisers, and organizations can submit a <a href="{SPONSOR_URL}">sponsorship request</a> any time. We review every request and support as many as we can. We're always grateful to support the people who support our community.</p>
  </div>
</section>
<section class="dark band">
  <div class="wrap" style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:20px">
    <div><h2 style="margin-bottom:.2em">have a request?</h2><p style="color:#dcdcdc;margin:0">Scholarship questions: call or email. Sponsorships and donations: use the form.</p></div>
    <div class="btn-row" style="margin:0"><a class="cta-btn" href="{SPONSOR_URL}">sponsorship form.</a><a class="cta-btn" style="background:transparent;color:#fff" href="/contact/">contact us.</a></div>
  </div>
</section>"""
    title = "Giving Back | Scholarships, Sponsorships & Donations | P&M Apparel"
    desc = "How P&M Apparel gives back: need-based Shirts for Scholarships awards for graduating Iowa seniors, plus sponsorships and donations for local teams, events, and organizations."
    write(path, layout(path, title, desc, body, breadcrumbs([("Home", "/"), ("Giving Back", path)])))

def contact():
    path = "/contact/"
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>let's make this easy.</h1>
    <p class="lead">Walk in, call, email, or start with the quote form. Whatever's easiest for you.</p>
    <div class="btn-row"><a class="cta-btn" href="{QUOTE_URL}">get a quote.</a></div>
  </div>
</section>
<section class="imgband"><img src="/assets/photos/building-entrance-wide.jpg" alt="The front entrance of P&M Apparel at 1100 S 5th St, Polk City" loading="lazy"></section>
<section>
  <div class="wrap">
    <div class="grid cols3">
      <div class="cell"><h3>visit.</h3><p>{ADDR}<br>{CITY}, {STATE} {ZIP}<br><a href="{MAPS_URL}">Get directions</a></p></div>
      <div class="cell"><h3>talk.</h3><p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div class="cell"><h3>hours.</h3><p>Monday to Friday<br>8:00am to 5:00pm<br>Closed Saturday and Sunday</p></div>
    </div>
  </div>
</section>
<section class="dark">
  <div class="wrap prose">
    <h2>what happens next.</h2>
    <p>Your message gets routed to an account manager who helps with decoration specifics, blank garments, and online stores. Quotes are usually back within 24 hours. A 50% deposit sends your job into art, and after art approval, standard turnaround is 8 to 10 business days.</p>
    <p>Serving Polk City, Ankeny, and the Des Moines metro. Shipping worldwide.</p>
  </div>
</section>"""
    title = "Contact P&M Apparel | Polk City, IA Screen Printing & Embroidery"
    desc = "Contact P&M Apparel at 1100 S 5th St, Polk City, IA 50226. Call (515) 984-7740 or email info@pmapparel.com. Open Monday to Friday, 8am to 5pm. Quotes within 24 hours."
    write(path, layout(path, title, desc, body, breadcrumbs([("Home", "/"), ("Contact", path)])))

def faq_page():
    path = "/faq/"
    faqs = [
        ("What is your minimum order?", "Like Grandpa used to say, our minimum order is 1; we can't do any less. To avoid fees we recommend 12 pieces for screen printing (24 for 4-6 colors, 48 for 7-10 colors). Embroidery and DTF are one-piece minimums. Promo products vary; send us what you're thinking and we'll help."),
        ("How do I place an order?", "Walk in, call, email, or use the quote form; any of them works. Your order gets routed to an account manager who helps with decoration specifics, blank garments, and online stores. A 50% deposit sends the job into art."),
        ("How long does an order take?", "Standard turnaround is 8 to 10 business days after art approval, up to 10 to 12 during peak season."),
        ("Do you do rush orders?", "Yes. If we have the item in stock, we can turn it same day. If we need to order it, generally next day. Rush fees depend on the timeline."),
        ("How much will my order cost?", "Every job is unique and quoted as such. Pricing depends on quantity, number of colors and locations, garment choice, thread count, and rush. Quotes are usually back within 24 hours, and bulk orders get better per-piece pricing."),
        ("Are there setup fees?", "Screen printing orders below minimum carry a $35 per-screen charge. Embroidery has a one-time $35 digitizing setup fee. Promotional products are case by case."),
        ("Do you charge for artwork?", "Custom art is $100 per hour, and the first 30 minutes is free when your order includes production (like shirts). Every piece of our art is custom and made in-house. No judgment. We've printed Comic Sans before."),
        ("What file formats do you need for my logo?", "Vector files (AI, EPS, PDF) are preferred. High-resolution PNGs are accepted. Our art department can clean up or recreate artwork if needed."),
        ("Will I see a proof before you print?", "Yes. Every job gets a quote approval and a proof approval. Nothing prints until you've signed off."),
        ("Can you match my brand colors?", "Yes, we offer Pantone color matching for printing and do our best to color-match embroidery thread to existing designs."),
        ("Can I supply my own garments?", "Absolutely. We decorate customer-supplied garments regularly; we just ask you to sign a short waiver first. See our customer-supplied garments guide for what to check before you bring items in."),
        ("What brands of apparel do you carry?", "Gildan, Bella+Canvas, Comfort Colors, Carhartt, Under Armour, Nike, Adidas, and many more."),
        ("Do you ship?", "Yes. Ship or pick up; your choice. Last year we shipped to all 50 states and 29 countries. Local delivery in the Des Moines metro is available by request, generally for a fee."),
        ("What can you put a logo on besides shirts?", "Hats, hoodies, banners, promo products, drinkware, teddy bears, even toilet paper (yes, really). You think it, we'll ink it."),
        ("Do you offer discounts for schools or nonprofits?", "We don't generally offer flat discounts, but bulk orders get better per-piece pricing, and we give back through our Shirts for Scholarships program and community sponsorships."),
    ]
    items = "".join(
        f'<details class="faq"><summary>{esc(q)}</summary><div class="a"><p>{esc(a)}</p></div></details>'
        for q, a in faqs)
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>answers, before you ask.</h1>
    <p class="lead">Minimums, pricing, turnaround, artwork. The stuff everyone wants to know.</p>
  </div>
</section>
<section>
  <div class="wrap" style="max-width:840px">
    {items}
    <p style="margin-top:28px">Didn't find it? <a href="/contact/">Ask us directly</a>; fast answers matter to us too.</p>
  </div>
</section>
{cta_band()}"""
    title = "FAQ | Minimums, Pricing & Turnaround | P&M Apparel"
    desc = "Answers to the questions we hear most: order minimums, screen printing and embroidery pricing factors, turnaround times, rush orders, artwork files, shipping, and more."
    write(path, layout(path, title, desc, body, [faq_schema(faqs), breadcrumbs([("Home", "/"), ("FAQ", path)])]))

def blog():
    path = "/blog/"
    posts = [
        ("it's just a shirt.", "/blog/its-just-a-shirt/"),
        ("it's not just a shirt.", "/blog/its-not-just-a-shirt/"),
        ("what your print location says about you.", "/blog/what-your-print-location-says-about-you/"),
        ("shirts in sync.", "/blog/shirts-in-sync/"),
    ]
    tiles = "".join(
        f'<a class="cell" href="{u}"><h3>{esc(t)}</h3><p class="cellsub">Read the post</p></a>'
        for t, u in posts)
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>notes from the shop.</h1>
    <p class="lead">Thoughts on shirts, print, and the people who wear them.</p>
  </div>
</section>
<section>
  <div class="wrap"><div class="grid cols2">{tiles}</div></div>
</section>
{cta_band()}"""
    title = "Blog | P&M Apparel"
    desc = "Notes from the P&M Apparel shop floor: thoughts on custom shirts, print methods, and the people who wear them."
    write(path, layout(path, title, desc, body, breadcrumbs([("Home", "/"), ("Blog", path)])))
    # Post stubs to be filled with migrated copy before launch
    for t, u in posts:
        stub = f"""
<section class="texture hero" style="padding:84px 0 60px">
  <div class="wrap"><h1>{esc(t)}</h1></div>
</section>
<section><div class="wrap prose">
<!-- MIGRATE: paste the original post text from the old Google Site here before launch -->
<p><em>This post is being migrated from our old site. Check back soon.</em></p>
</div></section>
{cta_band()}"""
        write(u, layout(u, f"{t.rstrip('.').title()} | P&M Apparel Blog",
                        "From the P&M Apparel blog.", stub, og_type="article"))

def notfound():
    body = f"""
<section class="texture hero">
  <div class="wrap">
    <h1>this page went missing.</h1>
    <p class="lead">The good news: everything else is right where you left it. We've untangled worse.</p>
    <div class="btn-row"><a class="cta-btn" href="/">back to home.</a><a class="cta-btn" style="background:transparent;color:#fff" href="/services/">see services.</a></div>
  </div>
</section>"""
    html_out = layout("/404.html", "Page Not Found | P&M Apparel",
                      "That page doesn't exist. Head back to the P&M Apparel homepage.", body)
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(html_out)

# ---------------------------------------------------------------- SITE FILES
PAGE_PATHS = ["/", "/services/", "/services/screen-printing/", "/services/embroidery/",
    "/services/fusion/", "/services/sublimation/", "/services/live-printing/",
    "/services/e-commerce/", "/services/state-shirts/", "/customer-supplied-garments/",
    "/iowa-on-demand/", "/about-us/", "/faq/", "/contact/", "/shirts-for-scholarships/",
    "/blog/", "/blog/its-just-a-shirt/", "/blog/its-not-just-a-shirt/",
    "/blog/what-your-print-location-says-about-you/", "/blog/shirts-in-sync/"]

def site_files():
    with open(os.path.join(OUT, "styles.css"), "w") as f:
        f.write(CSS)
    urls = "".join(
        f"<url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGE_PATHS)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
    with open(os.path.join(OUT, "llms.txt"), "w") as f:
        f.write(f"""# P&M Apparel

> Woman-owned, third-generation custom apparel company in Polk City, Iowa, serving Ankeny and the Des Moines metro since 1987. Screen printing, embroidery, DTF/fusion transfers, sublimation, promotional products, free online team stores, live event printing, and print-on-demand school apparel via Iowa On Demand. Ships worldwide (all 50 states and 29 countries last year).

Contact: {PHONE}, {EMAIL}, {ADDR}, {CITY}, {STATE} {ZIP}. Hours: Monday-Friday 8am-5pm.

Key facts: 12-piece recommended minimum for screen printing (1-piece minimums for embroidery and DTF). Standard turnaround 8-10 business days after art approval. Rush available (same day if in stock). Quotes within 24 hours. One-time $35 embroidery setup. Custom art $100/hr, first 30 minutes free with production orders. Customer-supplied garments welcome with waiver. Free online team stores (Chipply). Pantone matching available. Brands: Gildan, Bella+Canvas, Comfort Colors, Carhartt, Nike, Adidas, Under Armour.

## Pages
- [Services]({BASE}/services/): all decoration methods explained
- [Screen Printing]({BASE}/services/screen-printing/)
- [Embroidery]({BASE}/services/embroidery/)
- [Fusion / DTF]({BASE}/services/fusion/)
- [Sublimation]({BASE}/services/sublimation/)
- [Live Printing]({BASE}/services/live-printing/)
- [Online Team Stores]({BASE}/services/e-commerce/)
- [Customer-Supplied Garments Guide]({BASE}/customer-supplied-garments/)
- [Iowa On Demand]({BASE}/iowa-on-demand/)
- [FAQ]({BASE}/faq/)
- [About]({BASE}/about-us/)
- [Contact]({BASE}/contact/)
""")

def readme():
    with open("README.md", "w") as f:
        f.write(f"""# pmapparel.com

The P&M Apparel website. Plain, fast, static HTML. No build step required: the `site/` folder is the website.

## How it's organized
- `site/` = the actual website (deploy this)
- `build.py` = the generator that creates `site/` (edit content here, then run `python3 build.py`)

## Deploy to Vercel (first time, ~10 minutes)
1. Create a new repository on GitHub (e.g. `pmapparel-site`) and upload this whole folder.
2. Go to vercel.com, log in, click "Add New > Project", and import the GitHub repo.
3. Framework preset: "Other". Set **Output Directory** to `site`. Leave build command empty.
4. Click Deploy. You'll get a preview URL like pmapparel-site.vercel.app.
5. When ready to go live: Vercel > Project > Settings > Domains > add `www.pmapparel.com`, then follow the DNS instructions it shows (two records to change in GoDaddy).

## Editing content later
Small text fix: edit the HTML file directly in `site/`.
Bigger changes: edit `build.py` and re-run `python3 build.py` (or just ask Claude).

## Before launch checklist
- [ ] Paste the four blog posts from the old Google Site into `site/blog/*/index.html`
- [ ] Swap `site/assets/logo-*.png` for SVG exports from Illustrator (filled logo, black and white versions)
- [ ] Add photos (see below)
- [ ] Verify the site in Google Search Console and submit `sitemap.xml`
- [ ] 301-redirect the bare domain (pmapparel.com) to www in GoDaddy / Vercel
- [ ] Update the LinkedIn address to {ADDR} to match everywhere else

## Adding photos
Export web-size JPGs (1600px wide, ~200-400KB) from the Dropbox `Website Assets/Photos 2024` folder into `site/assets/photos/`, then add `<img>` tags where wanted. Good hero/section candidates: press and production shots (PM-07x-09x series), team shots, and Megan's headshot for the About page.
""")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    home()
    services_index()
    all_services()
    csg_page()
    about()
    iowa_on_demand()
    scholarships()
    contact()
    faq_page()
    blog()
    notfound()
    site_files()
    readme()
    n = sum(len(files) for _, _, files in os.walk(OUT))
    print(f"Built {n} files into {OUT}/")

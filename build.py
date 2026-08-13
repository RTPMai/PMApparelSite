#!/usr/bin/env python3
"""Static site generator for pmapparel.com. Outputs plain HTML into ./site."""
import json, os, html, datetime, re

BASE = "https://www.pmapparel.com"
OUT = "site"
GBP_PLACE_ID = "ChIJ780iSSWC7ocR-TzjT7KFVVU"
GBP_MAP_URL = f"https://www.google.com/maps/place/?q=place_id:{GBP_PLACE_ID}"
GBP_READ_URL = f"https://search.google.com/local/reviews?placeid={GBP_PLACE_ID}"
GBP_WRITE_URL = f"https://search.google.com/local/writereview?placeid={GBP_PLACE_ID}"
# Refresh these two occasionally (they change slowly) and re-run build.py:
GBP_RATING = "4.9"
GBP_COUNT = "328"

TODAY = "2026-08-07"

# Flyover Con. When the dedicated flyovercon site launches, put its URL here
# and the site's Flyover links can point to it.
FLYOVER_URL = None
UPDATED_HUMAN = datetime.date.fromisoformat(TODAY).strftime("%B %Y")

PHONE = "(515) 984-7740"
PHONE_TEL = "+15159847740"
EMAIL = "info@pmapparel.com"
FLYOVER_EMAIL = "ryan@flyovercon.ink"
# Alliteration MailMe signup page for the Flyover Con list (list key: "flyover-con").
MAILME_URL = "https://alliteration-eight.vercel.app/flyover-con-signup.html"
ADDR = "1100 S 5th St"
CITY = "Polk City"
STATE = "IA"
ZIP = "50226"

QUOTE_URL = "https://wkf.ms/3WiETfm"
STORES_URL = "https://pmapparel.chipply.com/"
PROMO_URL = "https://www.promoplace.com/pmapparel"
SPONSOR_URL = "https://form.jotform.com/231636854478064"
IOD_URL = "https://www.iowaondemand.com/"
# Schools on Iowa On Demand: six founding schools, then the six that joined in 2026.
IOD_FOUNDING = ["North Polk", "Ankeny", "Ankeny Centennial", "Woodward-Granger",
                "Ankeny Christian Academy", "Saydel"]
IOD_SCHOOLS = ["Bondurant-Farrar", "Johnston", "Dallas Center-Grimes",
               "Roosevelt", "Perry", "Ballard"]
FB_URL = "https://www.facebook.com/pmapparel"
IG_URL = "https://www.instagram.com/p_mapparel/"
TT_URL = "https://www.tiktok.com/@p_mapparel"
LI_URL = "https://www.linkedin.com/company/p-&-m-apparel"
MAPS_URL = "https://www.google.com/maps/search/?api=1&query=P%26M+Apparel+1100+S+5th+St+Polk+City+IA+50226"

# Press / bio profile URLs, reused in schema (sameAs) and on the press page.
MEGAN_APPARELIST_URL = "https://www.apparelist.com/person/megan-griffith/"
MEGAN_GP_AUTHOR_URL = "https://graphics-pro.com/author/megan-griffith/"
MEGAN_CANVASREBEL_URL = "https://canvasrebel.com/meet-megan-griffith/"
MEGAN_AWARD_URL = "https://screenprintingmag.com/here-are-the-winners-of-the-2024-women-in-screen-printing-awards/"
MEGAN_RISING_STARS_URL = "https://screenprintingmag.com/meet-the-rising-stars-megan-griffith/?highlight=Megan%20Griffith"
RYAN_BOD_URL = "https://www.boardofdecorators.com/board-members/ryan-toney"

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
    "areaServed": ["Polk City IA", "Ankeny IA", "Des Moines IA", "Alleman IA",
                   "Elkhart IA", "Sheldahl IA", "Johnston IA", "Grimes IA",
                   "Dallas Center IA", "Bondurant IA", "Woodward IA", "Granger IA",
                   "Perry IA", "Huxley IA", "Slater IA", "Cambridge IA",
                   "Central Iowa", "United States"],
    "sameAs": [FB_URL, IG_URL, TT_URL, LI_URL, GBP_MAP_URL],
    "hasMap": GBP_MAP_URL,
    "knowsAbout": ["screen printing", "custom embroidery", "DTF transfers", "sublimation printing", "promotional products", "online team stores", "live event printing"],
    "subOrganization": {
        "@type": "Organization",
        "name": "Iowa On Demand",
        "url": "https://www.iowaondemand.com/",
    },
}

NAV = [
    ("home.", "/"),
    ("services.", "/services/"),
    ("pricing.", "/pricing/"),
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
.hero h1.eyebrow{font-size:.95rem;letter-spacing:.14em;font-weight:700;color:#fff;opacity:.85;max-width:none;margin:0 0 14px}
.hero p.mega{font-family:var(--head);font-weight:800;line-height:1.05;font-size:clamp(2.4rem,6vw,4.2rem);max-width:14ch;margin:0 0 .5em;color:#fff}
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
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:34px 20px;text-align:center}
.stat b{font-family:var(--head);font-size:clamp(2.1rem,4vw,3rem);display:block;line-height:1;margin-bottom:8px}
.stat span{color:#bdbdbd;font-size:.92rem;display:block;max-width:22ch;margin:0 auto}
@media(max-width:900px){.stats{grid-template-columns:repeat(2,1fr);gap:28px 14px}}
@media(max-width:700px){.stat b{font-size:1.9rem}.stat span{font-size:.82rem}}

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
.imgband.sign img{max-height:560px;object-position:center 72%}
.splitrow{display:grid;grid-template-columns:1fr 1fr;background:var(--ink)}
.splitrow .sr-img{min-height:340px;position:relative}
.splitrow .sr-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.splitrow .sr-text{background:#fff;padding:64px 48px}
.splitrow.rev .sr-text{order:-1}
@media(max-width:820px){.splitrow{grid-template-columns:1fr}.splitrow.rev .sr-text{order:0}.sr-text{padding:48px 24px}}
.teamgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:var(--ink);border:2px solid var(--ink)}
@media(max-width:900px){.teamgrid{grid-template-columns:repeat(2,1fr)}}
.teamcard{background:#fff;padding:26px 18px;text-align:center}
.teamcard img{width:120px;height:120px;border-radius:50%;object-fit:cover;object-position:center 22%;display:block;margin:0 auto 12px}
.teamcard h3{font-size:.95rem;margin-bottom:2px}
.teamcard p{color:var(--gray);font-size:.85rem;margin:0}
.flipcard{cursor:pointer;perspective:1200px;background:none;padding:0;user-select:none}
.flipcard:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
.flip-inner{position:relative;width:100%;min-height:290px;transform-style:preserve-3d;transition:transform .55s cubic-bezier(.4,.9,.4,1)}
.flipcard.flipped .flip-inner{transform:rotateY(180deg)}
.flip-front,.flip-back{position:absolute;inset:0;backface-visibility:hidden;-webkit-backface-visibility:hidden;background:#fff;padding:26px 18px}
.flip-back{transform:rotateY(180deg);overflow-y:auto;text-align:left;padding:20px 16px}
.flip-back h3{text-align:center;margin-bottom:10px}
.flip-back .q{font-family:var(--head);font-size:.72rem;color:var(--ink);margin:10px 0 2px}
.flip-back .a{font-size:.82rem;color:var(--gray);margin:0}
.flip-front{padding-bottom:34px}
.fliphint{position:absolute;left:0;right:0;bottom:12px;font-family:var(--head);font-size:.6rem;letter-spacing:.08em;color:#b5b5b5;margin:0;text-align:center}
@media (prefers-reduced-motion: reduce){.flip-inner{transition:none}}

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
.quiz-bar{height:6px;background:#e5e5e5}
.quiz-bar i{display:block;height:100%;background:var(--ink);transition:width .35s ease}
.quiz-slide{animation:qslide .28s ease both}
@keyframes qslide{from{opacity:0;transform:translateX(22px)}to{opacity:1;transform:none}}
.quiz-print p{font-family:var(--head);font-size:1.1rem;margin:20px 0;animation:qblink 1s ease infinite}
@keyframes qblink{50%{opacity:.45}}
.quiz-result .stamp{animation:qstamp .4s cubic-bezier(.2,1.6,.4,1) both}
@keyframes qstamp{from{opacity:0;transform:scale(1.7) rotate(-6deg)}to{opacity:1;transform:none}}
.quiz-result .quip{color:#555;font-style:italic}
.gbadge{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 14px;margin:0 0 24px;font-family:var(--head)}
.gbadge b{font-size:1.5rem;letter-spacing:-.01em}
.gbadge span{color:#555}
.gbadge a{font-size:.85rem;color:var(--ink);text-underline-offset:3px}
@media (prefers-reduced-motion: reduce){.quiz-slide,.quiz-result .stamp,.quiz-print p{animation:none}}
/* breadcrumbs */
.crumbs{font-family:var(--head);font-size:.78rem;letter-spacing:.04em;text-transform:lowercase;color:#666;margin:0 0 22px}
.crumbs a{color:#666;text-decoration:none}
.crumbs a:hover{text-decoration:underline}
.crumbs [aria-current]{color:var(--ink)}
.updated{font-size:.85rem;color:#666;font-style:italic}
.faq summary h3{display:inline;font:inherit;margin:0}
.skip{position:absolute;left:-9999px;top:0;background:#fff;color:var(--ink);padding:10px 16px;z-index:100}
.skip:focus{left:12px;top:12px}
:focus-visible{outline:3px solid #1a1a1a;outline-offset:2px}
.dark :focus-visible,.texture :focus-visible,header :focus-visible,footer.site :focus-visible{outline-color:#fff}

/* price machine */
.pbuild{border:3px solid var(--ink);background:#fff;color:var(--ink);max-width:760px}
.pbuild-head{background:var(--ink);color:#fff;padding:16px 22px;font-family:var(--head);display:flex;justify-content:space-between;align-items:center;gap:12px}
.pbuild-head span{font-size:.95rem}
.pbuild-body{padding:24px 22px}
.pb-group{margin-bottom:20px}
.pb-group>b{font-family:var(--head);font-size:.78rem;letter-spacing:.06em;display:block;margin-bottom:8px}
.pb-opts{display:flex;flex-wrap:wrap;gap:8px}
.pb-opts button{font-family:var(--head);font-size:.8rem;padding:11px 14px;background:#fff;border:2px solid var(--ink);cursor:pointer;transition:background .12s,color .12s;min-height:44px}
.pb-opts button:hover,.pb-opts button:focus{background:#efefef}
.pb-opts button[aria-pressed="true"]{background:var(--ink);color:#fff}
.pmeter{margin:26px 0 6px}
.pmeter-track{height:22px;border:2px solid var(--ink);background:#fff;position:relative;overflow:hidden}
.pmeter-track i{display:block;height:100%;background:var(--ink);transition:width .45s cubic-bezier(.3,1.2,.4,1)}
.pmeter-scale{display:flex;justify-content:space-between;font-family:var(--head);font-size:.68rem;color:#8a8a8a;margin-top:5px}
.pmeter-label{font-family:var(--head);font-size:1.25rem;margin:14px 0 4px}
.pmeter-label.bump{animation:qstamp .4s cubic-bezier(.2,1.6,.4,1) both}
.pb-tips{min-height:52px}
.pb-tips p{font-size:.92rem;color:#555;font-style:italic;margin:0 0 6px}
.pb-fine{font-size:.8rem;color:#8a8a8a;margin:16px 0 0}
.pb-cta{margin-top:18px}
@media (prefers-reduced-motion:reduce){.pmeter-track i{transition:none}.pmeter-label.bump{animation:none}}

/* mobile pass */
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{-webkit-tap-highlight-color:rgba(0,0,0,.08)}
@media(max-width:700px){
  section{padding:52px 0}
  .band{padding:36px 0}
  .hero{padding:72px 0 60px}
  .hero p.lead{font-size:1.1rem}
  .imgband img{max-height:300px}
  .quiz-body,.pbuild-body{padding:20px 16px}
  table{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
  .prose h2{margin-top:1.3em}
}
@media(max-width:520px){
  .btn-row{flex-direction:column;align-items:stretch}
  .btn-row .cta-btn{text-align:center;padding:14px 18px}
  .teamcard img{width:96px;height:96px}
  .teamcard,.flip-front,.flip-back{padding:20px 12px}
  .cell{padding:22px 18px}
  .splitrow .sr-text{padding:40px 20px}
  .wrap{padding:0 18px}
}
@media(max-width:900px){
  details.mnav summary{min-height:44px;display:flex;align-items:center}
  .mnav-panel{max-height:calc(100vh - 80px);overflow-y:auto}
  .mnav-panel a{padding:13px 0;font-size:1.05rem}
  header .cta-btn{padding:10px 14px;font-size:.78rem}
}
"""

def esc(s): return html.escape(s, quote=True)

def layout(path, title, desc, body, extra_schema=None, og_type="website", noindex=False):
    robots = '\n<meta name="robots" content="noindex">' if noindex else ""
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
<link rel="canonical" href="{canonical}">{robots}
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/og-default.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:site_name" content="P&amp;M Apparel">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{BASE}/assets/og-default.jpg">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/icons/favicon-32.png" type="image/png" sizes="32x32">
<link rel="icon" href="/assets/icons/favicon-16.png" type="image/png" sizes="16x16">
<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
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
        <li><a href="/pricing/">How pricing works</a></li>
        <li><a href="/flyover-con/">Flyover Con</a></li>
        <li><a href="{STORES_URL}">Online stores</a></li>
        <li><a href="/iowa-on-demand/">Iowa On Demand</a></li>
        <li><a href="/shirts-for-scholarships/">Shirts for Scholarships</a></li>
        <li><a href="/press/">Press &amp; recognition</a></li>
        <li><a href="{SPONSOR_URL}">Sponsorship requests</a></li>
        <li><a href="{FB_URL}">Facebook</a> &middot; <a href="{IG_URL}">Instagram</a> &middot; <a href="{TT_URL}">TikTok</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap fine">
    <p>Good People. Great Gear. &copy; 2026 P&amp;M Apparel. Woman-owned and family-run in Polk City, Iowa since 1987. Serving Ankeny, the Des Moines metro, and teams everywhere. <a href="/privacy-policy/">Privacy Policy</a></p>
  </div>
</footer>
</body>
</html>"""

def _external_blank_target(content):
    """Add target="_blank" rel="noopener" to any <a href="http..."> that
    doesn't point at pmapparel.com. Internal links, mailto:, and tel: are untouched."""
    def repl(m):
        pre, url, post = m.group(1), m.group(2), m.group(3)
        if "pmapparel.com" in url:
            return m.group(0)
        attrs = pre + post
        if "target=" in attrs:
            return m.group(0)
        extra = ' target="_blank"' + ('' if "rel=" in attrs else ' rel="noopener"')
        return f'<a {pre}href="{url}"{post}{extra}>'
    return re.sub(r'<a\s+([^>]*?)href="(https?://[^"]+)"([^>]*)>', repl, content)

def generate_favicons():
    """Regenerate favicon.ico, PNG icon set, and apple-touch-icon from the
    source logo. Runs every build so the icons stay in sync with the logo
    without living as untracked binary output."""
    from PIL import Image
    logo = Image.open(os.path.join(OUT, "assets/logo-black.png")).convert("RGBA")

    def square_pad(im, size, bg=None):
        im = im.copy()
        im.thumbnail((size, size), Image.LANCZOS)
        canvas = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
        canvas.paste(im, ((size - im.width) // 2, (size - im.height) // 2), im)
        return canvas

    icon_dir = os.path.join(OUT, "assets/icons")
    os.makedirs(icon_dir, exist_ok=True)
    for size in (16, 32, 48, 192, 512):
        square_pad(logo, size).save(os.path.join(icon_dir, f"favicon-{size}.png"))

    icon_sizes = [16, 32, 48]
    imgs = [square_pad(logo, s) for s in icon_sizes]
    imgs[0].save(os.path.join(OUT, "favicon.ico"), format="ICO", sizes=[(s, s) for s in icon_sizes])

    # iOS ignores transparency and fills it black, so give the apple touch
    # icon an explicit ink-black background with a white version of the mark.
    apple = Image.new("RGBA", (180, 180), (26, 26, 26, 255))
    mark = logo.copy()
    mark.thumbnail((120, 120), Image.LANCZOS)
    a = mark.split()[-1]
    white_mark = Image.merge("RGBA", (Image.new("L", mark.size, 255),) * 3 + (a,))
    apple.paste(white_mark, ((180 - white_mark.width) // 2, (180 - white_mark.height) // 2), white_mark)
    apple.save(os.path.join(icon_dir, "apple-touch-icon.png"))

    manifest = {
        "name": "P&M Apparel", "short_name": "P&M Apparel",
        "start_url": "/", "display": "standalone",
        "background_color": "#ffffff", "theme_color": "#1a1a1a",
        "icons": [
            {"src": "/assets/icons/favicon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/icons/favicon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }
    with open(os.path.join(OUT, "site.webmanifest"), "w") as f:
        json.dump(manifest, f, separators=(",", ":"))

def generate_social_image():
    """Build a 1200x630 default social-share image (JPEG) from the shop-floor
    hero photo, for og:image / twitter:card. Regenerated every build."""
    from PIL import Image
    src = Image.open(os.path.join(OUT, "assets/photos/hero-floor.jpg")).convert("RGB")
    target_w, target_h = 1200, 630
    scale = target_w / src.width
    resized = src.resize((target_w, round(src.height * scale)), Image.LANCZOS)
    top = (resized.height - target_h) // 2
    cropped = resized.crop((0, top, target_w, top + target_h))
    cropped.save(os.path.join(OUT, "assets/og-default.jpg"), quality=82)

def write(path, content):
    full = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"):
        full = os.path.join(full, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    if full.endswith(".html"):
        content = _external_blank_target(content)
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

def cta_band(heading="ready when you are.", sub="Tell us what you're thinking. Quotes are usually back within 24 hours.", btns=None):
    return f"""
<section class="texture band">
  <div class="wrap" style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:20px">
    <div><h2 style="margin-bottom:.2em">{heading}</h2><p style="color:#dcdcdc;margin:0">{sub}</p></div>
    <div class="btn-row" style="margin:0">{btns or f'<a class="cta-btn" href="{QUOTE_URL}">get a quote.</a><a class="cta-btn" style="background:transparent;color:#fff" href="tel:{PHONE_TEL}">call {PHONE}</a>'}</div>
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
            f'<details class="faq"><summary><h3>{esc(q)}</h3></summary><div class="a"><p>{a}</p></div></details>'
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
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": GBP_RATING,
                            "bestRating": "5", "ratingCount": GBP_COUNT},
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
    <h1 class="eyebrow">custom apparel in polk city, iowa.</h1>
    <p class="mega">we can do that.</p>
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
    <div class="stat"><b>1987</b><span>the year it all started</span></div>
    <div class="stat"><b>3</b><span>generations of family under one roof</span></div>
    <div class="stat"><b>50</b><span>states we shipped to last year</span></div>
    <div class="stat"><b>29</b><span>countries we shipped to last year</span></div>
    <div class="stat"><b>{GBP_RATING}</b><span>stars across {GBP_COUNT} Google reviews</span></div>
    <div class="stat"><b>24</b><span>hours to a typical quote</span></div>
    <div class="stat"><b>1</b><span>piece minimum. yes, really</span></div>
    <div class="stat"><b>16</b><span>real humans on the crew. zero robots</span></div>
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
    <div class="gbadge">
      <b>&#9733; {GBP_RATING}</b>
      <span>from {GBP_COUNT} Google reviews</span>
      <a href="{GBP_READ_URL}" rel="noopener">read them all</a>
      <a href="{GBP_WRITE_URL}" rel="noopener">leave one</a>
    </div>
    {quotes}
  </div>
</section>
<section class="band" style="border-top:2px solid var(--ink);border-bottom:2px solid var(--ink)">
  <div class="wrap" style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:20px">
    <div><h2 style="margin-bottom:.2em">flyover con.</h2><p style="color:#555;margin:0">An apparel industry event inside our working print shop. Real production, honest tours, modest registration fee.</p></div>
    <a class="cta-btn inv" href="/flyover-con/">see the event.</a>
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
def price_machine(dark=False):
    """The gamified 'what moves your price' widget, covering screen printing,
    embroidery, and DTF. Plain-HTML page content stays readable without JS;
    this is an enhancement layer, not hidden content."""
    block = """
<div class="pbuild" id="pbuild">
  <div class="pbuild-head"><span>the price machine.</span><span style="font-size:.7rem;opacity:.75">direction, not dollars</span></div>
  <div class="pbuild-body">
    <div class="pb-group"><b>pick your method.</b><div class="pb-opts" data-k="mth">
      <button type="button" aria-pressed="true">screen printing</button><button type="button">embroidery</button><button type="button">dtf</button></div></div>
    <div class="pb-group"><b>how many pieces?</b><div class="pb-opts" data-k="qty">
      <button type="button">1&ndash;11</button><button type="button" aria-pressed="true">12&ndash;23</button><button type="button">24&ndash;47</button><button type="button">48&ndash;143</button><button type="button">144+</button></div></div>
    <div class="pb-group" id="pb-g-col"><b>how many ink colors?</b><div class="pb-opts" data-k="col">
      <button type="button" aria-pressed="true">1 color</button><button type="button">2&ndash;3</button><button type="button">4&ndash;6</button><button type="button">7&ndash;10</button></div></div>
    <div class="pb-group" id="pb-g-sti" style="display:none"><b>how big is the stitch job?</b><div class="pb-opts" data-k="sti">
      <button type="button" aria-pressed="true">left-chest logo</button><button type="button">cap or hat</button><button type="button">jacket-back big</button></div></div>
    <p class="pb-fine" id="pb-note-dtf" style="display:none;margin:0 0 20px">Full color is included with DTF. No screens, no per-color setup. Go nuts.</p>
    <div class="pb-group"><b>how many locations?</b><div class="pb-opts" data-k="loc">
      <button type="button" aria-pressed="true">one spot</button><button type="button">front + back</button><button type="button">3+ spots</button></div></div>
    <div class="pb-group"><b>what's it going on?</b><div class="pb-opts" data-k="gar">
      <button type="button" aria-pressed="true">basic tee</button><button type="button">retail-soft tee</button><button type="button">polo / hat / hoodie</button></div></div>
    <div class="pb-group"><b>how fast?</b><div class="pb-opts" data-k="spd">
      <button type="button" aria-pressed="true">standard, 8&ndash;10 days</button><button type="button">rush it</button></div></div>
    <div class="pmeter">
      <div class="pmeter-track"><i id="pb-fill" style="width:25%"></i></div>
      <div class="pmeter-scale"><span>$ per piece</span><span>$$$$$ per piece</span></div>
      <p class="pmeter-label" id="pb-label">budget sweet spot.</p>
      <div class="pb-tips" id="pb-tips"></div>
    </div>
    <p class="pb-cta"><a class="cta-btn inv" href="__QUOTE__">get the real number.</a></p>
    <p class="pb-fine">This machine shows which way the number moves, not the number itself. For that, a human reads your actual art and order and gets a quote back to you within about 24 hours.</p>
  </div>
</div>
<script>
(function(){
  var pb=document.getElementById("pbuild");if(!pb)return;
  var sel={mth:0,qty:1,col:0,sti:0,loc:0,gar:0,spd:0};
  var groups=pb.querySelectorAll(".pb-opts");
  var fill=document.getElementById("pb-fill"),label=document.getElementById("pb-label"),tips=document.getElementById("pb-tips");
  var gCol=document.getElementById("pb-g-col"),gSti=document.getElementById("pb-g-sti"),nDtf=document.getElementById("pb-note-dtf");
  var BANDS=[[27,"budget sweet spot."],[45,"great value."],[65,"middle of the road."],[85,"premium territory."],[101,"top shelf."]];
  var QTIP_S=["Under 12 pieces, screen printing carries a $35 per-screen charge. This is exactly where DTF shines instead.",
              "Solid start. The next price break lands at 24 pieces.",
              "Nice. The per-piece math gets noticeably friendlier at 48.",
              "This is where per-piece pricing really starts working for you.",
              "144 and up: our best per-piece pricing. The presses purr at this volume."];
  function tipList(){
    var t=[];
    if(sel.mth===0){
      t.push(QTIP_S[sel.qty]);
      if(sel.col>0)t.push("Every ink color needs its own screen and its own setup. One-color designs are the oldest budget hack in the book.");
    }else if(sel.mth===1){
      if(sel.qty===0)t.push("Embroidery has a true 1-piece minimum. One jacket for the new hire? We're completely serious.");
      else t.push("Embroidery cares less about quantity than screen printing does, but more pieces still spread the hooping time.");
      t.push(sel.sti===2?"Stitch count is embroidery's color count. A jacket-back design carries a lot more thread time than a chest logo.":"New logo? Digitizing is a one-time $35, then it's on file forever. Reorders never pay it again.");
    }else{
      if(sel.qty===0)t.push("DTF's 1-piece minimum and zero per-color setup make it the small-run champion.");
      else if(sel.qty>=2)t.push("Heads up: every DTF piece is placed by hand, so there's no bulk discount. At this quantity, a simple design often screen-prints for less. Ask us to quote it both ways.");
      else t.push("Every DTF piece is placed by hand, one at a time, so per-piece price stays flat as your order grows. No bulk discount, no bulk penalty.");
    }
    if(sel.loc>0)t.push("Each location is a separate run. One strong spot often says more than two.");
    if(sel.gar===2)t.push("The blank drives cost more than the decoration does. The garment can cost more than the art on it.");
    if(sel.spd===1)t.push("Rush is real (same-day if stock allows), but the standard timeline keeps the price standard.");
    if(t.length<2)t.push("This is about as optimized as custom apparel gets. Well played.");
    return t.slice(0,2);
  }
  function score(){
    if(sel.mth===0)return 34-sel.qty*9+sel.col*8+sel.loc*8+sel.gar*9+sel.spd*8;
    if(sel.mth===1)return 33-sel.qty*4+sel.sti*14+sel.loc*8+sel.gar*7+sel.spd*8;
    return 29+sel.loc*8+sel.gar*9+sel.spd*8;
  }
  function render(){
    gCol.style.display=sel.mth===0?"":"none";
    gSti.style.display=sel.mth===1?"":"none";
    nDtf.style.display=sel.mth===2?"":"none";
    var s=Math.max(6,Math.min(98,score()));
    fill.style.width=s+"%";
    var name=BANDS[0][1];for(var i=0;i<BANDS.length;i++){if(s<BANDS[i][0]){name=BANDS[i][1];break;}}
    if(label.textContent!==name){label.textContent=name;label.classList.remove("bump");void label.offsetWidth;label.classList.add("bump");}
    tips.innerHTML=tipList().map(function(x){return "<p>"+x+"</p>";}).join("");
  }
  groups.forEach(function(g){
    var k=g.getAttribute("data-k"),btns=g.querySelectorAll("button");
    btns.forEach(function(b,i){b.addEventListener("click",function(){
      btns.forEach(function(x){x.setAttribute("aria-pressed","false");});
      b.setAttribute("aria-pressed","true");sel[k]=i;render();
    });});
  });
  render();
})();
</script>"""
    return block.replace("__QUOTE__", QUOTE_URL)

# ---------------------------------------------------------------- PRICING
def pricing():
    path = "/pricing/"
    faqs = [
        ("Why doesn't P&M Apparel post prices online?", "Because a posted grid would be wrong within the week. Blank garment costs move constantly, and no two jobs share the same art, color count, locations, and quantity. Instead of a stale price list, we explain exactly what drives the number and return real quotes within about 24 hours."),
        ("What fees does P&M Apparel put in writing?", "A one-time $35 digitizing fee for new embroidery logos (then it's on file forever). Custom artwork at $100 per hour, with the first 30 minutes free on production orders. A 50% deposit sends your job into art. Quotes are free, and online team stores are free to set up."),
        ("What's the cheapest way to print custom shirts?", "One ink color, one print location, a basic cotton tee, ordered at quantity on the standard 8-to-10-day timeline. Quantity is screen printing's biggest lever: per-piece pricing improves at 12, 24, 48, and 144 pieces. (DTF is the exception: it's hand-placed piece by piece, so its price stays flat at any quantity.)"),
        ("Are there minimums?", "Screen printing minimums scale with color count: 12 pieces for 1 to 3 colors, 24 for 4 to 6, and 48 for 7 to 10. Embroidery and DTF have 1-piece minimums."),
        ("Is an instant online price accurate?", "Instant calculators quote a formula, not your order. They can't see that your art needs cleanup, that a different blank saves you money, or that DTF beats screens at your quantity. A human quote catches all three, and ours comes back in about 24 hours."),
    ]
    faq_html = "".join(
        f'<details class="faq"><summary><h3>{esc(q)}</h3></summary><div class="a"><p>{a}</p></div></details>'
        for q, a in faqs)
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>how pricing works.</h1>
    <p class="lead">No mystery, no gotchas, no "call for pricing" runaround. Here's exactly what moves the number on your quote and how to move it in your favor.</p>
  </div>
</section>
<section>
  <div class="wrap prose">
    <h2>the honest part first.</h2>
    <p>You won't find a price grid on this page, and here's the real reason: blank garment prices change constantly, and no two jobs are the same. A grid we posted today would quietly lie to you by Friday. What we can do, and what almost nobody in custom apparel does, is show you the whole machine: every variable that moves your per-piece price, which direction it moves it, and the handful of fees we're happy to put in writing.</p>
    <p>Then, when you're ready, a human (not a formula) reads your actual art and your actual order and sends a real quote, usually within 24 hours.</p>
    <h2>the six things that move your price.</h2>
    <p><b>1. Quantity.</b> The biggest lever by far in screen printing. Setup work (burning screens, loading the press) costs the same whether we print 12 shirts or 400, so the more pieces that setup spreads across, the less each piece carries. Price breaks land at 12, 24, 48, and 144 pieces. The exception is <a href="/services/fusion/">DTF</a>: every piece is placed by hand, one at a time, so its per-piece price stays flat at any quantity, no bulk discount, no bulk penalty. That's exactly why big simple orders belong on the press and small detailed ones belong on DTF.</p>
    <p><b>2. Ink colors.</b> In screen printing, every color is its own screen, its own setup, and its own station on the press. A one-color design is the oldest budget trick in the book. (Under 12 pieces, full-color <a href="/services/fusion/">DTF</a> sidesteps color-count math entirely.)</p>
    <p><b>3. Print locations.</b> Front, back, sleeve: each one is a separate run through the press. A single strong front print often beats front-and-back on both budget and design.</p>
    <p><b>4. The garment itself.</b> The blank usually drives cost more than the decoration does. A basic tee, a retail-soft tee, and a hoodie can be the same print at three very different prices. We'll happily suggest a substitute blank that saves money without looking like it did.</p>
    <p><b>5. Artwork.</b> Print-ready art costs nothing extra. Art that needs recreating or designing from scratch is billed at $100 per hour, and the first 30 minutes are free with any production order, which covers most cleanup jobs entirely.</p>
    <p><b>6. Timeline.</b> Standard turnaround is 8 to 10 business days after art approval. Rush is genuinely available (same day if garments are in stock), but the standard timeline keeps the price standard.</p>
    <h2>the fees we put in writing.</h2>
    <ul>
      <li><b>Quotes: free.</b> Back to you in about 24 hours.</li>
      <li><b>Embroidery digitizing: $35, once.</b> Your logo goes on file forever; reorders never pay it again.</li>
      <li><b>Custom art: $100/hr,</b> first 30 minutes free with a production order.</li>
      <li><b>Deposit: 50%</b> sends your job into art. Nothing prints before you approve a proof.</li>
      <li><b>Online team stores: free</b> to build, host, and manage. Really.</li>
    </ul>
  </div>
</section>
<section class="dark">
  <div class="wrap">
    <h2>play with the machine.</h2>
    <p style="color:#dcdcdc;max-width:60ch;margin-bottom:26px">Flip the levers and watch which way your per-piece price moves. The machine coaches; the humans quote.</p>
    {price_machine(dark=True)}
  </div>
</section>
<section>
  <div class="wrap prose">
    <h2>frequently asked, honestly answered.</h2>
    {faq_html}
    <p style="margin-top:22px">Want the play-by-play on stretching a budget? Read <a href="/blog/how-to-lower-per-shirt-cost/">how to lower your per-shirt cost</a>, or <a href="/blog/how-quotes-work/">how our quotes work</a>.</p>
  </div>
</section>
{cta_band("ready for a real number?", "Send us the idea. A human quotes it within about 24 hours, and the quote is free.")}"""
    title = "How Custom Apparel Pricing Works | P&M Apparel, Polk City IA"
    desc = "The honest guide to custom t-shirt and embroidery pricing: the six variables that move your per-piece price, the fees we put in writing, and an interactive price machine. No gotchas."
    write(path, layout(path, title, desc, body,
                       [faq_schema(faqs), breadcrumbs([("Home", "/"), ("Pricing", path)])]))

# ---------------------------------------------------------------- FLYOVER CON
def flyover():
    path = "/flyover-con/"
    event_schema = {
        "@context": "https://schema.org", "@type": "EventSeries",
        "name": "Flyover Con",
        "description": "A recurring apparel decoration industry event held inside P&M Apparel's working print shop in Polk City, Iowa. Hands-on education, honest shop tours, live production, and real conversations. Built by printers, for printers. A modest registration fee keeps it accessible, with sponsors covering the rest. Held in 2024 and 2026.",
        "url": BASE + path,
        "location": {"@type": "Place", "name": "P&M Apparel",
                     "address": {"@type": "PostalAddress", "streetAddress": ADDR,
                                 "addressLocality": CITY, "addressRegion": STATE,
                                 "postalCode": ZIP, "addressCountry": "US"}},
        "organizer": {"@id": BASE + "/#business"},
    }
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1 class="eyebrow">inside a working print shop // polk city, iowa</h1>
    <p class="mega">flyover con.</p>
    <p class="lead">Some of the best ideas in this industry don't come from the biggest cities or the biggest companies. They come from hardworking shops in the middle of the country that are willing to open their doors and share what they've learned. This is us, opening ours.</p>
    <div class="btn-row">
      <a class="cta-btn" href="{MAILME_URL}" rel="noopener" target="_blank">keep me in the loop.</a>
      <a class="cta-btn" style="background:transparent;color:#fff" href="mailto:{FLYOVER_EMAIL}?subject=Flyover%20Con%20sponsorship">sponsor the education.</a>
    </div>
  </div>
</section>
<section>
  <div class="wrap prose">
    <h2>not another hotel ballroom.</h2>
    <p>You know the formula: convention center, carpet squares, badge scanners, a tote bag of brochures you'll never open. Flyover Con is intentionally none of that. It happens inside our working print shop in Polk City: presses running, dryers humming, real orders moving through the building while you're in it.</p>
    <p>It's designed to feel like an industry reunion inside a real production facility. Fewer sales pitches, more honest conversations. Hands-on demonstrations instead of PowerPoint. Small enough that everyone can actually meet everyone. And the goal for every attendee is the same: leave with things you can implement Monday morning.</p>
    <p>We've hosted it in 2024 and again in 2026, and each time the takeaway is the same: shop life is the attraction. Built by printers, for printers.</p>
  </div>
</section>
<section class="dark">
  <div class="wrap">
    <h2>what flyover con is.</h2>
    <div class="grid cols3">
      <div class="cell"><h3>honest shop tours.</h3><p class="cellsub">No fake showroom, no staged demos. You walk an operating production floor and see the real workflow, mess and all.</p></div>
      <div class="cell"><h3>live production.</h3><p class="cellsub">Equipment being used for actual orders, run by the people who run it every day. Ask them anything.</p></div>
      <div class="cell"><h3>practical sessions.</h3><p class="cellsub">Hands-on education from working decorators. Knowledge you'll use, not brochures you'll recycle.</p></div>
      <div class="cell"><h3>real conversations.</h3><p class="cellsub">Talk directly with owners and operators. No polished marketing talks, no scripts.</p></div>
      <div class="cell"><h3>small on purpose.</h3><p class="cellsub">Sized so you can meet everyone in the building, including the vendors. Community over competition.</p></div>
      <div class="cell"><h3>collaborative vendors.</h3><p class="cellsub">Sponsor interaction that feels like working together, not being worked over.</p></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap prose">
    <h2>accessible. on purpose.</h2>
    <p>Registration is a modest fee, kept intentionally low. It's not how this event makes money; it's there for buy-in, so the room is full of people who actually want to be there. Sponsors cover the rest, and sponsoring Flyover Con isn't buying ad space: it's face-to-face time with working decorators, a seat inside an authentic community event, and a direct hand in keeping industry education accessible.</p>
    <p>If your company wants in on that, <a href="mailto:{FLYOVER_EMAIL}?subject=Flyover%20Con%20sponsorship">let's talk sponsorship</a>.</p>
    <h2>why we host it.</h2>
    <p>Flyover Con is what P&amp;M stands for, turned into an event: generosity, education, transparency, and helping other decorators succeed. We'd rather grow the whole industry than guard our corner of it. Open doors beat closed playbooks.</p>
  </div>
</section>
{cta_band("want in on the next one?", "Join the Flyover Con list and you'll hear about dates, speakers, and registration before anyone else.", btns=f'<a class="cta-btn" href="{MAILME_URL}" rel="noopener" target="_blank">join the list.</a><a class="cta-btn" style="background:transparent;color:#fff" href="mailto:{FLYOVER_EMAIL}?subject=Flyover%20Con">email flyover con.</a>')}"""
    title = "Flyover Con | An Industry Event Inside a Working Print Shop"
    desc = "Flyover Con: hands-on apparel decoration education inside P&M Apparel's working print shop in Polk City, Iowa. Honest shop tours, live production, real conversations. Modest registration fee."
    write(path, layout(path, title, desc, body,
                       [event_schema, breadcrumbs([("Home", "/"), ("Flyover Con", path)])]))

def services_index():
    tiles = "".join(
        f'<a class="cell" href="{h}"><h3>{esc(n)}</h3><p class="cellsub">{esc(d)}</p></a>'
        for n, h, d in SERVICES)
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>every method. one roof.</h1>
    <p class="lead">Not sure which method fits? That's literally our job. We run jobs from 1 piece to 10,000 and beyond, so the only real question is which method. We're a phone call away for the rest.</p>
  </div>
</section>
<section>
  <div class="wrap"><div class="grid cols4">{tiles}</div></div>
</section>
<section class="dark">
  <div class="wrap">
    <h2>which one is right for you?</h2>
    <p style="color:#dcdcdc;max-width:60ch;margin-bottom:26px">Three quick questions and we'll point you to the cleanest route. (And if the quiz is wrong, a human will happily overrule it. The quiz will not be offended.)</p>
    <div class="quiz" id="quiz">
      <div class="quiz-head"><span id="quiz-step">question 1 of 3.</span><button class="quiz-reset" id="quiz-reset" style="display:none">start over</button></div>
      <div class="quiz-bar"><i id="quiz-fill" style="width:0%"></i></div>
      <div class="quiz-body" id="quiz-body"></div>
    </div>
  </div>
</section>
<script>
(function(){{
  var Q=[
    {{q:"how many pieces are we talking?",o:[["Just 1. Maybe a few.","small"],["A solid batch, 12 to 47","med"],["48 to 10,000 and beyond. Go big.","big"]]}},
    {{q:"what's the look you're after?",o:[["Bold and budget-friendly","bold"],["Premium and stitched","stitch"],["Photo-real, full color","photo"],["Edge-to-edge, all over the garment","allover"]]}},
    {{q:"what's it going on?",o:[["Cotton tees or blends","cotton"],["Light polyester athletic wear","poly"],["Hats, jackets, polos, or bags","structured"]]}}
  ];
  var R={{
    screen:{{t:"screen printing.",d:"Bold, durable, and the best per-piece price at quantity. The workhorse.",u:"/services/screen-printing/"}},
    embroidery:{{t:"embroidery.",d:"Stitched, premium, built to last. The professional look for polos, jackets, hats, and bags.",u:"/services/embroidery/"}},
    fusion:{{t:"fusion.",d:"DTF transfers, vinyl, glitter, and puff. Incredible detail on small runs with a soft feel.",u:"/services/fusion/"}},
    sublimation:{{t:"sublimation.",d:"Full-color ink that becomes part of the fabric. No crack, no peel, no feel.",u:"/services/sublimation/"}}
  }};
  var QUIPS={{small:"One piece? Grandpa always said our minimum is 1; we can't do any less.",med:"A perfect-size batch. Right in our wheelhouse.",big:"Go big. 1 piece to 10,000 and beyond; we've shipped to all 50 states, so bring it."}};
  var SPIN=["mixing the ink...","burning the screens...","threading the needle...","consulting three generations...","checking it twice..."];
  var a=[],body=document.getElementById("quiz-body"),step=document.getElementById("quiz-step"),
      reset=document.getElementById("quiz-reset"),fill=document.getElementById("quiz-fill");
  function pick(){{
    if(a[1]==="stitch"||(a[1]!=="allover"&&a[2]==="structured"))return"embroidery";
    if(a[1]==="allover")return a[2]==="poly"?"sublimation":"fusion";
    if(a[1]==="photo")return a[2]==="poly"?"sublimation":"fusion";
    if(a[0]==="small")return"fusion";
    return"screen";
  }}
  function ask(i){{
    step.textContent="question "+(i+1)+" of 3.";reset.style.display=i?"inline":"none";
    fill.style.width=(i/3*100)+"%";
    var h="<div class='quiz-slide'><h3>"+Q[i].q+"</h3><div class='quiz-opts'>";
    Q[i].o.forEach(function(o){{h+="<button data-v='"+o[1]+"'>"+o[0]+"</button>";}});
    body.innerHTML=h+"</div></div>";
    body.querySelectorAll("button").forEach(function(b){{b.onclick=function(){{a[i]=b.dataset.v;i<2?ask(i+1):spin();}};}});
  }}
  function spin(){{
    fill.style.width="100%";step.textContent="working on it.";reset.style.display="none";
    var picks=SPIN.slice().sort(function(){{return .5-Math.random();}}).slice(0,3),n=0;
    body.innerHTML="<div class='quiz-print'><p id='quiz-spin'>"+picks[0]+"</p></div>";
    var el=document.getElementById("quiz-spin");
    var t=setInterval(function(){{n++; if(n<picks.length){{el.textContent=picks[n];}}else{{clearInterval(t);done();}}}},520);
  }}
  function done(){{
    var r=R[pick()];step.textContent="we can do that.";reset.style.display="inline";
    body.innerHTML="<div class='quiz-result'><h3 class='stamp'>"+r.t+"</h3><p class='cellsub'>"+r.d+"</p><p class='cellsub quip'>"+QUIPS[a[0]]+"</p><div class='btn-row' style='margin-top:6px'><a class='cta-btn inv' href='"+r.u+"'>see how it works.</a><a class='cta-btn inv' style='background:#fff;color:#1a1a1a' href='{QUOTE_URL}'>get a quote.</a></div></div>";
  }}
  reset.onclick=function(){{a=[];ask(0);}};
  ask(0);
}})();
</script>
<section>
  <div class="wrap">
    <h2>know your method? now play with your price.</h2>
    <p style="max-width:60ch;margin-bottom:26px">Nobody around here posts a price grid, and we explain <a href="/pricing/">exactly why</a>. But we'll do you one better: flip the levers and watch which way your per-piece price moves before you ever ask for a quote.</p>
    {price_machine()}
  </div>
</section>
{cta_band()}"""
    title = "Custom Apparel Services | Screen Printing, Embroidery & More | P&M Apparel"
    desc = "Screen printing, embroidery, DTF fusion transfers, sublimation, live event printing, online team stores, and promotional products in Polk City, Iowa."
    write("/services/", layout("/services/", title, desc, body,
        breadcrumbs([("Home", "/"), ("Services", "/services/")])))

# ---------------------------------------------------------------- SERVICE PAGES
def all_services():
    service_page(
        "screen-printing", "screen printing in polk&nbsp;city &amp; des&nbsp;moines.",
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
<p>Who's it for? Schools and spirit wear, corporate and staff tees, event and fundraiser merch (see <a href="/shirts-for-scholarships/">Shirts for Scholarships</a>), and teams of every kind. Pair it with an <a href="/services/e-commerce/">online team store</a> and let everyone order their own size.</p>
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
<p>Embroidery stitches your logo directly into the fabric with thread. It reads as quality from across the room, which is why it's the standard for company polos, quarter-zips, jackets, caps, and bags for businesses across Ankeny and the Des Moines metro. It doesn't crack, fade, or peel. It just lasts.</p>
<h2>one piece minimum.</h2>
<p>Unlike screen printing, embroidery has no real minimum. Order one jacket or one hundred. There's a one-time $35 setup fee to digitize your logo, and after that it's on file with us forever.</p>
<h2>the techniques.</h2>
<div class="steps">
  <div class="step"><h3>flat embroidery.</h3><p>The classic: a tight, slightly raised weave stitched into the garment. We digitize every design in-house so we control where each stitch hits.</p></div>
  <div class="step"><h3>3d puff embroidery.</h3><p>A layer of foam under the thread pops the design off the garment for a tactile, dramatic look. Especially popular on caps and team gear. Probably helps you win more games.</p></div>
  <div class="step"><h3>applique.</h3><p>Fabric stitched onto the garment with an embroidered border, like you see on baseball jerseys and retro sweatshirts. Try glitter material for a dance or cheer stunner, go patch-style on hats, or leave edges raw for a frayed look.</p></div>
  <div class="step"><h3>mixed media.</h3><p>Screen printing plus embroidery in one multi-layered design, or embroidery with rhinestones for a platinum-level look. Precision work, which is convenient, because so are we.</p></div>
</div>
<h2>bring your own garments.</h2>
<p>Already have jackets, hats, or sweaters you love? Bring them in. We decorate customer-supplied garments all the time; we just ask you to sign a simple waiver first, and our team will double-check that your items are a good fit for the machine. Read the full guide: <a href="/customer-supplied-garments/">customer-supplied garments</a>.</p>
<h2>the details.</h2>
<p>Our embroidery technicians color-match thread to existing logos on request, and you're always welcome to choose thread colors yourself. Hats, thick knits, and technical fabrics each have quirks; we'll flag anything before we stitch. Every job gets a proof approval first.</p>""",
        faqs=[
            ("Is there a minimum order for embroidery?", "No. Embroidery is a one-piece minimum, so you can order a single jacket or hat."),
            ("What does embroidery setup cost?", "There's a one-time $35 setup fee to digitize your logo. Once it's digitized, it stays on file for all future orders."),
            ("Can you embroider items I already own?", "Yes. We welcome customer-supplied garments. We ask you to fill out a short waiver first, and our staff will happily double-check your items before we run them."),
            ("What is 3D or puff embroidery?", "3D (puff) embroidery places a layer of foam under the thread so the design pops off the garment with a raised, tactile look. It's especially popular on caps and team apparel. We also offer applique (stitched-on fabric with an embroidered border) and mixed-media designs that combine embroidery with screen printing or rhinestones."),
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
        "Sublimation printing in Polk City, Iowa. Full-color, edge-to-edge designs on light polyester that never crack or peel. One-piece minimum. 3 to 4 week turnaround. Quotes within 24 hours.",
        "Perfect for full-color, edge-to-edge designs on light-colored polyester garments. The ink becomes part of the fabric.",
        f"""
<h2>ink that becomes fabric.</h2>
<p>Sublimation uses heat to turn ink into gas that bonds permanently with polyester fibers. The result is a print you can't feel: no crack, no peel, no added weight, ever. It's how all-over prints, photo-real jerseys, and vivid pattern work get made.</p>
<h2>when to choose it.</h2>
<p>Choose sublimation for full-color, edge-to-edge designs on light-colored polyester. Athletic jerseys, all-over prints, and vibrant designs with gradients and photos are its sweet spot. Because the ink dyes the fabric itself, it needs polyester content and light base colors to work its magic.</p>
<h2>the details.</h2>
<p>One-piece minimum. Standard 3 to 4 week turnaround after art approval. Pairs beautifully with fusion names and numbers for team uniforms.</p>""",
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
<h2>two ways to price it.</h2>
<div class="steps">
  <div class="step"><h3>you pay.</h3><p>Guests get an unforgettable keepsake that makes them think of you every time they wear it. We keep track of everything printed and bill you the total. Perfect for giveaways, grand openings, and employee or customer appreciation.</p></div>
  <div class="step"><h3>they pay.</h3><p>We act as your in-house merch vendor with none of the inventory overhead. Guests buy their own shirts, we take out our costs, and we cut you a check for the profits. A unique fundraiser with genuinely low overhead.</p></div>
</div>
<h2>we handle everything.</h2>
<p>Equipment, setup, production, and cleanup are all on us. You enjoy the event while your guests watch their shirts come to life.</p>""",
        faqs=[
            ("How does live printing work at an event?", "We bring a screen printing press, blank garments, and our crew to your venue, set up a printing station, and print shirts on the spot as guests watch and pick theirs up warm off the press."),
            ("How does live printing pricing work?", "One of two ways. You pay: we track everything printed at your event and bill you the total, ideal for giveaways. Or they pay: guests buy their own shirts, we act as your merch vendor, deduct our costs, and cut you a check for the profits, which makes a great low-overhead fundraiser."),
            ("What do I need to provide for live printing?", "Just the space and the crowd. We handle equipment, setup, production, and cleanup, and we'll work with you ahead of time on designs and garment choices."),
        ])

    service_page(
        "e-commerce", "online team stores.",
        "Free Online Team Stores for Schools & Teams in Iowa | P&M Apparel",
        "Free online team stores built and managed by P&M Apparel. No paper forms, no chasing payments, no leftover inventory. Perfect for Iowa schools, teams, clubs, and businesses.",
        "A simple, organized way for your group to order custom apparel. No paper forms. No chasing payments. No cost to set up.",
        f"""
<h2>stop chasing sizes and money.</h2>
<p>Online team stores give your group a simple, organized way to order custom apparel without passing around paper forms or collecting money. We build and manage them for schools and teams across Ankeny, Des Moines, and all of Iowa. We build a custom storefront with your approved designs, and everyone orders exactly what they want, pays online, and has their order produced and delivered through us.</p>
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
<p>When your team qualifies for a state tournament, the window between "we're in!" and game day is tiny. State shirts are our rush specialty: quick turnarounds, online store capabilities, and <b>no rush fees</b>. Whether it's a state tournament or the Drake Relays, it's never too early to start preparing, and it has never been easier.</p>
<h2>how it works.</h2>
<div class="steps">
  <div class="step"><h3>reach out.</h3><p>Use the <a href="{QUOTE_URL}" style="color:inherit">quote form</a> the moment you qualify (or before). It collects everything at once so you can turn your focus back to preparation, not the shirts.</p></div>
  <div class="step"><h3>we handle the art.</h3><p>With 30 minutes of free art time, the possibilities are endless. Our in-house art department turns your school, sport, and bracket run into a design; your approval is all we need.</p></div>
  <div class="step"><h3>store goes live when you win.</h3><p>If your sport's timeline allows, we build the <a href="/services/e-commerce/" style="color:inherit">online store</a> ahead of time and open it the day of your qualifying competition, ready for your team, families, fans, and school community. Store windows close quickly, so having it ready helps everyone.</p></div>
  <div class="step"><h3>we produce and pack.</h3><p>Once the store closes we get to work, producing everything and packaging it individually by order to make distribution easy. Pick up individually at our shop, send a representative for the whole batch, or ask about delivery options.</p></div>
  <div class="step"><h3>show up proud.</h3><p>Your team, families, fans, and school community rep your colors as you take the court, pitch, field, track, pool, or mat.</p></div>
</div>
<p>Some sports have tighter windows than others between qualifying and the state tournament (looking at you, soccer), but we have processes in place to get those done too.</p>
<p>Every sport, every season, every level. Football, volleyball, wrestling, basketball, soccer, track, cheer, dance, esports. If they're headed to state, we can do that.</p>""",
        faqs=[
            ("How fast can you turn state tournament shirts?", "This is our rush specialty, and state tournament orders carry no rush fees. Reach out the moment you qualify and we'll have art moving the same day; if we have the garments in stock we can turn an order same day, generally next day if we need to order them."),
            ("Do you do Drake Relays shirts?", "Yes. The same quick-turnaround, no-rush-fee process covers the Drake Relays and other qualifying meets, with an online store ready to open the moment your athletes punch their ticket."),
            ("Can fans and parents order their own shirts?", "Yes. We can spin up a quick online store so fans and parents pick their own sizes and pay online, with nothing for the booster club to collect, sort, or front."),
            ("Do you design the shirt for us?", "Yes. Our in-house art department turns your school, sport, and bracket run into a custom design. The first 30 minutes of art time is free when your order includes production."),
        ])

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
# Each entry: (name, role, photo, [(question, answer), ...])
# OWNER: paste new Q&As into each person's list; the card back renders all of them.
# --- Press & recognition. Verified, third-party sources only. ---
PRESS_PODCASTS = [
    ("Apparelist Podcast: Inspiring Change in the Apparel Decorating Community",
     "Recorded live at PRINTING United Expo 2024.",
     "https://www.apparelist.com/podcast/apparelist/inspiring-change-in-the-apparel-decorating-community-with-megan-griffith-and-ryan-toney-of-pm-apparel/"),
    ("Rhymes with Odd: Ryan & Megan",
     "The origin story and how a basement operation became a full digital shop.",
     "https://www.ryansnaadt.com/podcast"),
    ("Last Call For Plastisol, Season 2 Ep. 5",
     "Live from PRINTING United Expo in Las Vegas.",
     "https://www.youtube.com/watch?v=4S9RpwBTsls"),
    ("Last Call For Plastisol, Ep. 13",
     "Megan and Ryan talk shop with the LCFP crew.",
     "https://www.youtube.com/watch?v=PvaY91QKoZw"),
    ("Last Call For Plastisol: Flyover Con Happy Hour",
     "A toast to the first Flyover Con.",
     "https://www.youtube.com/watch?v=Q1xPRlpnpLo"),
    ("Shirt Show, Ep. 263",
     "Megan and Ryan join the Shirt Show mic.",
     "https://www.youtube.com/watch?v=vR3L9Nz4t8o"),
    ("DTF Printing Podcast, Ep. 21",
     "Megan goes solo to talk DTF, growth, and running a family shop.",
     "https://www.youtube.com/watch?v=tDueYT1q6_4"),
    ("The Business Spotlight: Our Unconventional Marketing Idea",
     "How Flyover Con became P&M's biggest marketing move.",
     "https://www.youtube.com/watch?v=yVnGAAzjGzk"),
    ("Chipply Customer Stories: P&M Apparel",
     "Ryan on why P&M runs its team stores through Chipply.",
     "https://www.youtube.com/watch?v=dwQCjbrSD4M"),
]
PRESS_ARTICLES = [
    ("Apparelist: P&M Apparel, Leading with Legacy",
     "A longform look at three generations building one shop.",
     "https://www.apparelist.com/longform/pm-apparel-leading-with-legacy/"),
    ("Apparelist: Registration Now Open for Flyover Con 2026",
     "Coverage of the third Flyover Con.",
     "https://www.apparelist.com/2026/02/23/registration-now-open-for-flyover-con-2026/"),
    ("Apparelist: P&M Apparel, Anatol to Host Flyover Con",
     "The 2024 announcement that started it all.",
     "https://www.apparelist.com/2024/03/18/pm-apparel-anatol-to-host-flyover-con/"),
    ("Screen Printing Mag: Custom Apparel Without The Busywork",
     "Ryan on how P&M uses AI to cut the busywork, not the craft.",
     "https://screenprintingmag.com/custom-apparel-without-the-busywork/"),
    (f"CanvasRebel: Meet Megan Griffith",
     "A Q&A on building an inclusive shop floor.",
     MEGAN_CANVASREBEL_URL),
    ("CITY | Clean and Simple: A Seamless Apparel Process with P&M Apparel",
     "An early look at how P&M runs a custom order start to finish.",
     "https://www.citycleanandsimple.com/2018/03/19/seamless-apparel-process-pm-apparel-division-city/"),
    ("CITYVIEW: P&M Apparel Breaks Ground on New Building",
     "The new Polk City building, from the ground up.",
     "https://www.dmcityview.com/just-released/2020/08/17/pm-apparel-breaks-ground-on-new-building-in-polk-city/"),
]
PRESS_COLUMN = [
    ("Merch on demand in the event world", "April 2026", "https://graphics-pro.com/feature/merch-on-demand-in-the-event-world/"),
    ("Building a workplace culture that actually cares", "February 2026", "https://graphics-pro.com/feature/building-workplace-culture-cares/"),
    ("You can't boss like you used to", "January 2026", "https://graphics-pro.com/feature/you-cant-boss-like-you-used-to/"),
    ("Passing down the family business", "November 2025", "https://graphics-pro.com/feature/passing-down-the-family-business/"),
    ("Diversifying in the decorated apparel industry", "October 2025", "https://graphics-pro.com/feature/diversifying-decorated-apparel-industry/"),
    ("We don't sell T-shirts here", "June 2025", "https://graphics-pro.com/feature/we-dont-sell-t-shirts-here/"),
    ("Women in screen printing", "May 2025", "https://graphics-pro.com/feature/women-in-screen-printing/"),
]

TEAM = [
    ("Megan Griffith", "art director + owner", "megan", [("what would you say ya' do here?", "All things art, and I can dip into most of the production, administrative, and financial things as necessary.")]),
    ("Ryan Toney", "grand poobah of many hats + owner", "ryan", [("what would you say ya' do here?", "Webstores, social media, production, sales, a little bit of everything. Plus show tunes, performed without request.")]),
    ("Jacob Whitman", "sales director", "jacob", [("what would you say ya' do here?", "People and process wrangler.")]),
    ("Kim Taylor", "production manager, embroidery", "kim", [("what would you say ya' do here?", "The wizard at the embroidery machine and the fixer around here. The needle and thread is my home.")]),
    ("Margo Niemeyer", "production manager, screen printing", "margo", [("what would you say ya' do here?", "If you order a single item from P&M, it touches my hands. I manage intake and keep production moving from start to finish.")]),
    ("Amanda Clark", "finance manager", "amanda", [("what would you say ya' do here?", "I help folks narrow down thousands of options to what best suits them, and come up with ideas they never knew were possible.")]),
    ("Hannah Posey", "account manager", "hannah", [("what would you say ya' do here?", "I work with schools and sports organizations on apparel and uniforms they can pride themselves on.")]),
    ("Alexis Davis", "account manager", "alexis", [("what would you say ya' do here?", "I help individuals and companies get apparel and swag they enjoy wearing.")]),
    ("Abby Penton", "account manager", "abby", [("what would you say ya' do here?", "I work with dance studios, churches, and all types of personal orders.")]),
    ("Alex Hernandez", "graphic designer", "alex", [("what would you say ya' do here?", "I design custom artwork and mockup proofs, plus video and social media design for P&M marketing.")]),
    ("Maggie Barbour", "press operator", "maggie", [("what would you say ya' do here?", "I reclaim screens, coat them, and burn films. I also help on the embroidery side when needed.")]),
    ("Bailee Bishop", "press operator", "bailee", [("what would you say ya' do here?", "Reclaiming, coating, and rinsing screens, plus pulling and boxing orders.")]),
    ("Taylor Price", "embroidery tech", "taylor", [("what would you say ya' do here?", "I hoop garments and put them on a machine to get a brand new design.")]),
    ("Nicole Printy", "embroidery tech", "nicole", [("what would you say ya' do here?", "I work with the embroidery team to get the best designs onto each piece.")]),
    ("Tess Collins", "shipping specialist", "tess", [("what would you say ya' do here?", "In charge of checking in orders, compiling, and shipping them out.")]),
    ("Quinn Taylor", "press operator", "quinn", [("what would you say ya' do here?", "I help make shirts.")]),
]

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
    <p>We've also had a few people outside our shop take notice. See what's been said in <a href="/press/">press &amp; recognition.</a></p>
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
    <p style="max-width:60ch;margin-bottom:26px">Sixteen people who print it, stitch it, pack it, and answer the phone when you call. In their own&nbsp;words:</p>
    <div class="teamgrid">{"".join(
        f'<div class="teamcard flipcard" tabindex="0" role="button" aria-pressed="false" aria-label="Meet {n}, {r}">'
        f'<div class="flip-inner"><div class="flip-front">'
        f'<img src="/assets/photos/team/{p}.jpg" alt="{n}, {r} at P&M Apparel" loading="lazy" width="240" height="240">'
        f'<h3>{n.lower()}.</h3><p><b>{r}</b></p><p class="fliphint">tap to meet me</p></div>'
        f'<div class="flip-back"><h3>{n.split()[0].lower()}.</h3>'
        + "".join(f'<p class="q">{q}</p><p class="a">{a}</p>' for q, a in qa)
        + '</div></div></div>'
        for n, r, p, qa in TEAM)}</div>
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
{cta_band("come say hi.", "1100 S 5th St in Polk City.<br><span style=\"white-space:nowrap\">Monday to Friday, 8am to 5pm.</span>")}
<script>
document.querySelectorAll(".flipcard").forEach(function(c){{
  function flip(){{var on=c.classList.toggle("flipped");c.setAttribute("aria-pressed",on);}}
  c.addEventListener("click",flip);
  c.addEventListener("keydown",function(e){{if(e.key==="Enter"||e.key===" "){{e.preventDefault();flip();}}}});
}});
</script>"""
    title = "About P&M Apparel | Woman-Owned Custom Apparel in Iowa Since 1987"
    desc = "P&M Apparel is a woman-owned, third-generation family business in Polk City, Iowa. From Phyllis and Melvin's basement in 1987 to shipping worldwide today."
    schema = {
        "@context": "https://schema.org", "@type": "AboutPage",
        "url": BASE + path, "about": {"@id": BASE + "/#business"},
    }
    PERSON_EXTRA = {
        "Megan Griffith": {
            "sameAs": [MEGAN_APPARELIST_URL, MEGAN_GP_AUTHOR_URL, MEGAN_CANVASREBEL_URL],
            "award": "2024 Women in Screen Printing Award",
        },
        "Ryan Toney": {
            "sameAs": [RYAN_BOD_URL],
        },
    }
    employee_schema = []
    for n, r, p, qa in TEAM:
        entry = {"@type": "Person", "name": n, "jobTitle": r,
                  "image": BASE + "/assets/photos/team/" + p + ".jpg",
                  "worksFor": {"@id": BASE + "/#business"}}
        entry.update(PERSON_EXTRA.get(n, {}))
        employee_schema.append(entry)
    write(path, layout(path, title, desc, body, [{"@context": "https://schema.org", "@type": "LocalBusiness", "@id": BASE + "/#business", "employee": employee_schema}] + [schema, breadcrumbs([("Home", "/"), ("About Us", path)])]))

def press():
    path = "/press/"

    def card_grid(items):
        return '<div class="grid cols3">' + "".join(
            f'<a class="cell" href="{u}" target="_blank" rel="noopener">'
            f'<h3>{esc(t)}</h3><p class="cellsub">{esc(d)}</p></a>'
            for t, d, u in items) + '</div>'

    podcasts_html = card_grid(PRESS_PODCASTS)
    articles_html = card_grid(PRESS_ARTICLES)
    column_html = "<ul class=\"flist\" style=\"margin-left:0\">" + "".join(
        f'<li><a href="{u}" target="_blank" rel="noopener">{esc(t)}</a> <span style="color:var(--gray)">({d})</span></li>'
        for t, d, u in PRESS_COLUMN) + "</ul>"

    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>press &amp; recognition.</h1>
    <p class="lead">Podcasts, articles, and a few nice things other people in the industry have said about us. We didn't write any of these.</p>
  </div>
</section>
<section>
  <div class="wrap">
  <div class="prose">
    <h2>recognition.</h2>
    <p>In 2024, Megan Griffith won the <a href="{MEGAN_AWARD_URL}" target="_blank" rel="noopener">Women in Screen Printing Award</a> from Screen Printing Mag. She was also part of the magazine's inaugural <a href="{MEGAN_RISING_STARS_URL}" target="_blank" rel="noopener">Rising Stars</a> class. She sits on the <a href="{MEGAN_APPARELIST_URL}" target="_blank" rel="noopener">Apparelist Advisory Board</a> and writes a recurring column for <a href="{MEGAN_GP_AUTHOR_URL}" target="_blank" rel="noopener">GRAPHICS PRO</a>.</p>
    <p>Ryan Toney was a member of the <a href="{RYAN_BOD_URL}" target="_blank" rel="noopener">Gildan Board of Decorators</a> and founded <a href="/flyover-con/">Flyover Con</a>, an industry conference hosted right on our production floor. He currently serves on Chipply's Client Council and the Polk City Chamber of Commerce Board of Directors.</p>
  </div>
  </div>
</section>
<section class="band">
  <div class="wrap">
    <h2>Megan's column in GRAPHICS PRO.</h2>
    <p style="max-width:60ch;margin-bottom:22px">A recurring column on running a shop, running a family business, and running both at once.</p>
    {column_html}
  </div>
</section>
<section class="band">
  <div class="wrap">
    <h2>podcasts &amp; video.</h2>
    <p style="max-width:60ch;margin-bottom:22px">Conversations about the shop, the industry, and the occasional show tune.</p>
    {podcasts_html}
  </div>
</section>
<section class="band">
  <div class="wrap">
    <h2>articles &amp; features.</h2>
    {articles_html}
  </div>
</section>
{cta_band("want the story straight from us?", "Reach out and we'll point you to the right person.")}"""

    title = "Press & Recognition | P&M Apparel"
    desc = "Podcasts, articles, and industry recognition for P&M Apparel, Megan Griffith, and Ryan Toney, from GRAPHICS PRO, Apparelist, Screen Printing Mag, and more."
    schema = [
        {"@context": "https://schema.org", "@type": "CollectionPage",
         "url": BASE + path, "name": title, "about": {"@id": BASE + "/#business"}},
        {"@context": "https://schema.org", "@type": "Person", "name": "Megan Griffith",
         "jobTitle": "Art Director & Owner", "worksFor": {"@id": BASE + "/#business"},
         "award": "2024 Women in Screen Printing Award",
         "sameAs": [MEGAN_APPARELIST_URL, MEGAN_GP_AUTHOR_URL, MEGAN_CANVASREBEL_URL]},
        {"@context": "https://schema.org", "@type": "Person", "name": "Ryan Toney",
         "jobTitle": "Owner", "worksFor": {"@id": BASE + "/#business"},
         "sameAs": [RYAN_BOD_URL],
         "memberOf": [
             {"@type": "Organization", "name": "Chipply Client Council"},
             {"@type": "Organization", "name": "Polk City Chamber of Commerce Board of Directors"},
         ]},
        breadcrumbs([("Home", "/"), ("Press & Recognition", path)]),
    ]
    write(path, layout(path, title, desc, body, schema))

def iowa_on_demand():
    path = "/iowa-on-demand/"
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>school pride, on&nbsp;demand.</h1>
    <p class="lead">No bulk orders. No guessing sizes. No leftover&nbsp;boxes.</p>
    <div class="btn-row"><a class="cta-btn" href="{IOD_URL}">shop iowa on demand.</a></div>
  </div>
</section>
<section>
  <div class="wrap prose">
    <p><a href="{IOD_URL}">Iowa On Demand</a> is P&amp;M Apparel's on-demand offshoot, built for local schools. Right now it serves 12 Iowa schools, with more joining all the time. The mission: make it easier to support your school with officially licensed spirit wear that's available year-round.</p>
    <h2>the schools.</h2>
    <p>It started with six: {", ".join(IOD_FOUNDING[:-1])}, and {IOD_FOUNDING[-1]}. In 2026, six more joined: {", ".join(IOD_SCHOOLS[:-1])}, and {IOD_SCHOOLS[-1]}, bringing thousands more students, families, alumni, and fans on board. Twelve schools. One place.</p>
    <p>That means school communities across Polk City, Alleman, Elkhart, Ankeny, Johnston, Grimes, Dallas Center, Bondurant, Woodward, Granger, Perry, Huxley, Slater, Cambridge, and Des Moines can grab officially licensed gear whenever the mood strikes: no order windows, no waiting for the next fundraiser.</p>
    <h2>how it works.</h2>
    <p>Fans shop online whenever they want. Each item is produced as orders come in, decorated in-house by our team in Polk City, and shipped fast. No order windows. No leftover boxes in the booster club president's garage. Just school pride, ready when people want it.</p>
    <h2>get your district on board.</h2>
    <p>Want your district on Iowa On Demand? <a href="{QUOTE_URL}">Reach out.</a> We can do that.</p>
  </div>
</section>
{cta_band()}"""
    title = "Iowa On Demand | On-Demand School Spirit Wear | P&M Apparel"
    desc = "Iowa On Demand is P&M Apparel's print-on-demand offshoot serving 12 Iowa school districts. Fans shop anytime, gear is decorated in-house in Polk City and shipped fast."
    write(path, layout(path, title, desc, body, breadcrumbs([("Home", "/"), ("Iowa On Demand", path)])))

def scholarships():
    path = "/shirts-for-scholarships/"
    iod_all = IOD_FOUNDING + IOD_SCHOOLS
    schools_html = ", ".join(f"<b>{s}</b>" for s in iod_all[:-1]) + f", and <b>{iod_all[-1]}</b>"
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
    <p>The P&amp;M Apparel Shirts for Scholarships Fund is dedicated to helping youth in the school districts we serve through <a href="/iowa-on-demand/">Iowa On Demand</a>: {schools_html}. Its vision: empowering Central Iowa youth with need-based educational resources.</p>
    <p>Each year we award need-based scholarships to deserving graduating high school seniors pursuing a course of study at a two-year or four-year college, university, or trade program. Recipients are selected on need and program criteria, and funds are awarded after proof of enrollment.</p>
    <p><b>For 2026:</b> the fund's award ceiling is <b>$2,000</b>, with an individual maximum award of <b>$1,000</b>. Applications are due before <b>May 22 at 5:00 pm</b>. <a href="https://drive.google.com/file/d/1VTxwOn9fDHrAfLU10RGA2es_fbgbmrGE/view" rel="noopener">Download the application.</a></p>
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
    desc = "How P&M Apparel gives back: need-based Shirts for Scholarships awards for graduating seniors in the Iowa On Demand school districts, plus sponsorships and donations for local teams, events, and organizations."
    write(path, layout(path, title, desc, body, breadcrumbs([("Home", "/"), ("Giving Back", path)])))

def privacy():
    path = "/privacy-policy/"
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>privacy policy.</h1>
    <p class="lead">Plain language, no fine-print games. Here's what we collect and what we do with it.</p>
  </div>
</section>
<section>
  <div class="wrap">
  <div class="prose">
    <h2>what we collect.</h2>
    <p>When you request a quote, submit a sponsorship request, or reach out through a form on this site, we collect what you give us: your name, email, phone number, and details about your project or order. We don't collect anything beyond what's needed to get back to you and get your job done.</p>
    <h2>how we use it.</h2>
    <p>Your information is used to respond to your request, quote and produce your order, and keep you updated on its status. We don't sell your information, and we don't share it with anyone outside the vendors who help us run our business.</p>
    <h2>who we share it with.</h2>
    <p>Our quote and sponsorship forms are hosted by Jotform. Our online team stores run on Chipply. Payment processing for online stores is handled by Chipply's payment partners, not by us directly. We may also use analytics tools to understand how visitors use this site; these tools may use cookies or similar technology.</p>
    <h2>your choices.</h2>
    <p>You can ask us what information we have on file, ask us to correct it, or ask us to delete it, by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>. We'll honor reasonable requests as quickly as we can.</p>
    <h2>kids.</h2>
    <p>This site isn't directed at children, and we don't knowingly collect information from anyone under 13.</p>
    <h2>changes to this policy.</h2>
    <p>If this policy changes, we'll update this page. Last updated {UPDATED_HUMAN}.</p>
    <h2>questions?</h2>
    <p><a href="{QUOTE_URL}">Reach out</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>, and we'll get back to you.</p>
  </div>
  </div>
</section>"""
    title = "Privacy Policy | P&M Apparel"
    desc = "How P&M Apparel collects, uses, and protects the information you share with us through quote requests, sponsorship forms, and online team stores."
    write(path, layout(path, title, desc, body, breadcrumbs([("Home", "/"), ("Privacy Policy", path)]), noindex=False))

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
<section class="imgband sign"><img src="/assets/photos/building-entrance-wide.jpg" alt="The front entrance of P&M Apparel at 1100 S 5th St, Polk City" loading="lazy"></section>
<section>
  <div class="wrap">
    <div class="grid cols3">
      <div class="cell"><h3>visit.</h3><p>{ADDR}<br>{CITY}, {STATE} {ZIP}<br><a href="{MAPS_URL}">Get directions</a></p></div>
      <div class="cell"><h3>talk.</h3><p><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
      <div class="cell"><h3>hours.</h3><p>Monday to Friday<br>8:00am to 5:00pm<br>Closed Saturday and Sunday</p></div>
    </div>
    <iframe src="https://www.google.com/maps?q=1100+S+5th+St,+Polk+City,+IA+50226&amp;output=embed"
      width="100%" height="360" style="border:0;border-radius:12px;margin-top:26px"
      loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen
      title="Map to P&amp;M Apparel, 1100 S 5th St, Polk City, Iowa"></iframe>
    <p style="margin-top:14px">Rated <b>&#9733; {GBP_RATING}</b> from {GBP_COUNT} Google reviews.
      <a href="{GBP_READ_URL}" rel="noopener">Read them</a> or
      <a href="{GBP_WRITE_URL}" rel="noopener">leave one</a>. It means a lot to a family shop.</p>
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
        f'<details class="faq"><summary><h3>{esc(q)}</h3></summary><div class="a"><p>{esc(a)}</p></div></details>'
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
        ("how to lower your per-shirt cost.", "/blog/how-to-lower-per-shirt-cost/",
         "Seven real levers that bring your custom apparel price down, straight from the people who quote the jobs. No coupon codes, just math.",
         """
<p>Everyone asks us how much shirts cost. Almost nobody asks the better question: how do I make them cost less? Here are the seven levers that actually move the number, straight from the people who build the quotes. (For the full anatomy of a quote, see <a href="/pricing/">how pricing works</a>.)</p>
<h3>1. order together, not in waves.</h3>
<p>Quantity is the single biggest lever in screen printing. Setup costs the same for 12 shirts as for 400, so every extra piece spreads it thinner. Price breaks land at 12, 24, 48, and 144 pieces. Three separate orders of 20 will always cost more than one order of 60, so if the marketing shirts, the event shirts, and the new-hire shirts share a design, order them in one run. (One honest exception: DTF is placed by hand, piece by piece, so its price stays flat at any quantity, which is why big orders usually move to the press.)</p>
<h3>2. cut an ink color.</h3>
<p>In screen printing, every color is its own screen, its own setup, and its own pass on the press. A three-color design reduced to one smart color doesn't just save money; it usually looks bolder, too. Great one-color design is the oldest budget hack in the industry.</p>
<h3>3. skip the second location.</h3>
<p>Front, back, and sleeve are each a separate trip through the press. One strong front print often communicates more than front-and-back, at a meaningfully lower price. If you need the second location, keep it to one color.</p>
<h3>4. let the blank do the saving.</h3>
<p>The garment usually drives cost more than the printing does. There's often a blank one shelf over that saves real money without looking like it did, and because we quote from live garment pricing, we'll tell you when a substitute makes sense. Just ask "is there a cheaper blank that still looks good?" We love that question.</p>
<h3>5. send clean art (or keep it simple).</h3>
<p>Print-ready vector art costs nothing extra, and the first 30 minutes of art time are free with a production order, which covers most cleanup. From-scratch design runs $100 per hour, so a simple concept described clearly beats a complicated one described vaguely.</p>
<h3>6. ride the standard timeline.</h3>
<p>Standard turnaround is 8 to 10 business days after art approval. Rush is genuinely available when you need it, but planning two weeks ahead keeps the price standard. Deadlines are the most expensive surprise in apparel.</p>
<h3>7. reorder instead of reinventing.</h3>
<p>Once your art is on file (embroidery digitizing is a one-time $35, forever), reorders skip the setup conversation entirely. Same goes for keeping a design consistent year to year: the second run is always the easy one.</p>
<p>Not sure which levers apply to your order? That's literally our job. <a href="/services/">Pick a method</a>, play with the <a href="/pricing/">price machine</a>, or just ask. Quotes are free and usually back within 24 hours.</p>"""),
        ("screen printing vs dtf: how to choose.", "/blog/screen-printing-vs-dtf/",
         "The honest decision guide: when screen printing's bulk economics win, when DTF's one-piece minimum and full-color detail win, and how to pick for your order.",
         """
<p>This is the question behind most quote requests we get, even when it isn't asked out loud. Both methods make great shirts. The right one depends on your order, and the answer is usually obvious once you know three things: your quantity, your color count, and your garment.</p>
<h3>choose screen printing when quantity is on your side.</h3>
<p>Screen printing pushes ink through a mesh screen, one color at a time, then cures it for maximum durability. Because each color needs its own screen, there's real setup work, which is why it has minimums: 12 pieces for 1 to 3 colors, 24 for 4 to 6, 48 for 7 to 10. But once the screens are burned, every additional shirt is fast and cheap to print. That's why per-piece pricing gets better as your order grows, and why screen printing is the workhorse for team shirts, staff tees, spirit wear, and event merch. It's also the most durable printing method we offer: bold color that survives years of washing.</p>
<h3>choose dtf when flexibility is on yours.</h3>
<p>DTF (direct-to-film, part of our fusion family) prints your design in full color onto a film, then heat-presses it onto the garment. There are no screens, so there's no color-count math and no real minimum: one piece is fine. It handles photo-real detail, gradients, and unlimited colors with a soft feel and strong durability. It's our go-to for small batches, one-offs, and player names and numbers.</p>
<h3>the quick rules.</h3>
<p>Under 12 pieces? DTF, almost always. Big order of a bold 1-to-3-color design? Screen printing, almost always. A design with dozens of colors or photographic detail? DTF unless the quantity is large enough that screen printing's setup still pays off. Personalized names on team gear? DTF, often combined with screen printing on the same garments: the front prints on the press, the names heat-press on the back.</p>
<p>And if you're still not sure: that's literally our job. <a href="/services/screen-printing/">Read about screen printing</a>, <a href="/services/fusion/">read about fusion and DTF</a>, or just ask. Quotes are usually back within 24 hours.</p>"""),
        ("embroidery vs screen printing for company apparel.", "/blog/embroidery-vs-screen-printing/",
         "Polos and jackets or staff tees? A practical guide to when stitched logos beat printed ones, what setup actually costs, and how minimums differ.",
         """
<p>When a business orders apparel, the choice usually comes down to embroidery or screen printing. They solve different problems, and most companies eventually use both. Here's how to think about it.</p>
<h3>embroidery: the premium, no-minimum option.</h3>
<p>Embroidery stitches your logo directly into the fabric with thread. It reads as quality from across the room, which is why it's the standard for company polos, quarter-zips, jackets, caps, and bags. It doesn't crack, fade, or peel. There's no real minimum: order one jacket for a new hire or a hundred for the whole team. The only setup is a one-time $35 fee to digitize your logo, and after that it's on file with us forever, so reorders are painless.</p>
<h3>screen printing: the bulk-order workhorse.</h3>
<p>For staff t-shirts, event gear, and giveaways, screen printing wins on economics. Minimums start at 12 pieces (for 1 to 3 colors), and per-piece pricing improves as quantity grows. The prints are bold, vibrant, and extremely durable.</p>
<h3>the practical split.</h3>
<p>Most of our business clients land here: embroidery for the polished layer (polos, outerwear, hats, the things worn to meet customers), screen printing for the volume layer (staff tees, event shirts, giveaways). Structured items like hats and bags are embroidery territory almost by default; flat cotton at quantity is print territory. And if your logo has fine gradients or photographic detail that thread can't render, our <a href="/services/fusion/">fusion methods</a> fill the gap.</p>
<p>One more thing worth knowing: you can bring us garments you already own. We decorate <a href="/customer-supplied-garments/">customer-supplied garments</a> all the time. We just ask for a short waiver first.</p>
<p>Details on both: <a href="/services/embroidery/">embroidery</a> and <a href="/services/screen-printing/">screen printing</a>. Quotes back within 24 hours.</p>"""),
        ("what is sublimation actually good for?", "/blog/what-is-sublimation-good-for/",
         "Sublimation makes prints you can't feel, but only on the right garments. Where it shines, where it fails, and what to use instead.",
         """
<p>Sublimation is the method behind prints you can't feel: the ink turns to gas under heat and bonds permanently with the fabric itself. No crack, no peel, no added weight, ever. It sounds like magic, and on the right garment it basically is. The catch is the phrase "the right garment."</p>
<h3>where sublimation shines.</h3>
<p>Full-color, edge-to-edge designs on light-colored polyester. Athletic jerseys, all-over prints, vivid pattern work, gradients, and photos are its sweet spot. Because the ink dyes the fibers rather than sitting on top, a sublimated jersey feels exactly like a blank one and the print lasts as long as the garment does. It pairs beautifully with fusion names and numbers for team uniforms.</p>
<h3>where it simply doesn't work.</h3>
<p>Sublimation needs polyester content and a light base color. The ink bonds with polyester fibers, so cotton won't hold it, and because it dyes rather than covers, it can't print light designs on dark fabric. This isn't a quality tradeoff, it's chemistry.</p>
<h3>what to use instead.</h3>
<p>For cotton or dark garments, <a href="/services/fusion/">DTF transfers</a> deliver similar full-color detail with a soft feel. For bold designs at quantity on any fabric, <a href="/services/screen-printing/">screen printing</a> is the workhorse. Part of what you get with a full-service shop is that we'll steer you to the right method for your actual garment instead of forcing your design into the wrong one.</p>
<p>One-piece minimum, standard 3 to 4 week turnaround. <a href="/services/sublimation/">More on sublimation here.</a></p>"""),
        ("what does custom apparel cost? how our quotes work.", "/blog/how-quotes-work/",
         "We quote every job individually. Here's exactly what moves the number: quantity breaks, color counts, setup fees, art time, and what happens after you say yes.",
         """
<p>The honest answer to "what does a custom shirt cost?" is: it depends, and anyone who gives you one number without asking questions is guessing. Every job we run is quoted individually. But "it depends" is a lazy place to stop, so here is exactly what it depends on.</p>
<h3>the variables that move your quote.</h3>
<p><b>Quantity.</b> The single biggest lever. Setup work (burning screens, dialing in the press) is spread across your whole order, so per-piece pricing gets meaningfully better as quantity grows. We run jobs from 1 piece to 10,000 and beyond.</p>
<p><b>Colors and locations.</b> In screen printing, every ink color needs its own screen and every print location is a separate run. A 1-color front is the budget option; a 6-color front plus a back adds real work.</p>
<p><b>The garment itself.</b> A basic Gildan tee and a Carhartt jacket are different starting points. We carry Gildan, Bella+Canvas, Comfort Colors, Carhartt, Nike, Adidas, Under Armour, and more, at a range of price points.</p>
<p><b>Method.</b> Screen printing wins at quantity, embroidery and DTF have one-piece minimums, and thread count matters for embroidery quotes.</p>
<h3>the fixed fees, in plain sight.</h3>
<p>Screen printing orders below minimum (12 pieces for 1 to 3 colors) carry a $35 per-screen charge. Embroidery has a one-time $35 digitizing setup fee, after which your logo is on file forever. Custom artwork runs $100 per hour, and the first 30 minutes is free when your order includes production. Rush fees depend on the timeline, except state tournament orders, which carry no rush fees at all.</p>
<h3>what happens when you ask.</h3>
<p>Send us the idea however is easiest: walk in, call, email, or the quote form. Quotes are usually back within 24 hours. You approve the quote, a 50% deposit sends the job into art, you approve a proof, and nothing prints until you've signed off. Standard turnaround is 8 to 10 business days after art approval.</p>
<p>Why don't we publish a price list? Because we'd rather ask you three questions and get the number right than publish a range that's wrong for your job in both directions. <a href="{QUOTE_URL}">Ask us</a>. It costs nothing and takes a day.</p>"""),
        ("it's just a shirt.", "/blog/its-just-a-shirt/",
         "An ode to the easy stuff: why keeping the 'it's just a shirt' mentality keeps our heads cool and your order fixable.",
         """
<p class="lead"><em>an ode to the easy stuff.</em></p>
<p>If there's one thing we are definitely not great at, it's brain surgery. We've tried. We get queasy just holding the scalpel, and we don't even know what we'd do if we actually got to the brain part.</p>
<p>We've officially decided to give up the brain surgeon dream and keep printing shirts.</p>
<p>The thing is, shirts are important to your story and that makes them important to us. But we also know they're not as important as your brain; we're slinging ink on shirts, not brain surgery. So we try not to take ourselves too seriously or make too big a deal out of what we do, while also making sure we're delivering a superior product.</p>
<p>Keeping the mentality of "It's Just a Shirt" helps keep our heads cool if we've got an angry customer. It's just a shirt, it can be replaced. It's just a shirt, we can make it right. We've had customers tell us we've ruined Christmas because the shirt they want is not in stock from our manufacturer, but it's just a shirt. We don't actually have the power to ruin Christmas, at least not with shirts. I'm sure trying to start up a political discussion at the holiday dinner or attempting brain surgery under the tree might do it.</p>
<p>It's just a shirt, so when our team, that's very passionate and meticulous about everything they produce, has a human moment and messes up an order, it's not going to be life or death like on the operating table. We can simply order another shirt and fix it. It may set us back and cost more, but it's not too serious. There's an easy solution.</p>
<p>Now that I've convinced you it's just a shirt, let's talk about when a shirt is not just a shirt. Hang tight, there's a <a href="/blog/its-not-just-a-shirt/">part 2</a>.</p>"""),
        ("it's not just a shirt.", "/blog/its-not-just-a-shirt/",
         "An ode to the hard stuff: the teams, businesses, battles, and fundraisers a shirt can carry and why we care so much.",
         """
<p class="lead"><em>an ode to the hard stuff.</em></p>
<p>Okay but as soon as I convince you it's just a t-shirt, I'm flipping the switch. Because sometimes, a shirt is not just a shirt. And this is where our passion for this business shines.</p>
<p>Sometimes, a shirt is actually a representation of the little league team you dreamed of your kid one day playing on. Sometimes a shirt is a symbol of the business you poured all your blood, sweat, and tears into for countless late nights and weekends to get it off the ground. Sometimes a shirt is a symbol of unity for someone you love who's fighting a battle against cancer. Sometimes a shirt is a rally for funds to help a family get through a hard time.</p>
<p>Sometimes, a shirt is SO much more than just a shirt.</p>
<p>And this is where our drive to be meticulous and to care too much about our product comes in handy. Because we want you to feel like we care about your project as much as you care about your project. In my time here, I've seen our staff cry over a shirt because the message was so heartbreaking. I've seen my team volunteer for events just because they resonated so much with the ethos. We've donated tens of thousands of dollars, bought bikes for kids, and stayed at the shop until all hours making sure a project gets finished. We become friends with our clients, recommend and promote their endeavors on our social media and off the clock, and we've invited some of them to weddings.</p>
<p>It's not just a shirt, it's a relationship, built with trust and an understanding that we aren't just looking to turn a buck. We care about your success. Sometimes the jobs we're working on are full of heavy content or very personal to our client. We want to embrace the hard stuff and honor how much a shirt can mean to you.</p>
<p><a href="https://vimeo.com/658752386" rel="noopener">Watch: it's not just a shirt (video)</a></p>"""),
        ("what your print location says about you.", "/blog/what-your-print-location-says-about-you/",
         "Chest, sleeve, full back, pocket, hood: a tongue-in-cheek personality read on every print placement, plus why unique locations make gear people keep wearing.",
         """
<h3>full front.</h3><p>You're classic and traditional. You know what works and are sticking to it. You're a little bit leery of change, but that's not a bad thing in most cases. You think about dying your hair a lot, but have never gone through with it.</p>
<h3>right sleeve.</h3><p>You need people to know you're cool. Are you cool? Maybe. You probably have three other locations already on your shirt. You definitely have told us about that hunting trip, or your boat, or how your neighbor's grass is always too long.</p>
<h3>left sleeve.</h3><p>You're not sure if you need this print, but don't want to offend your friend Tyler by leaving it off the shirt. You're a little bit extra sometimes, but in a fun and quirky way. You've been told to shush during a movie in the last 3 months.</p>
<h3>locker tag.</h3><p>You're one classy dude. You know that subtlety can bring a lot of attention. You've probably had a mai tai somewhere tropical, but you don't brag about it.</p>
<h3>on the pocket.</h3><p>You've got calluses on your hands and you worked hard for them. You know that sometimes you need to prioritize function over form. Practical and hard working, we love to see it.</p>
<h3>right side.</h3><p>You definitely identified with some sort of "counterculture" while growing up. You've got some good ideas and a creative feather in your cap. You think about dying your hair a lot, and always go through with it.</p>
<h3>left side.</h3><p>You had a sibling who identified with some sort of "counterculture" while growing up, and you haven't stopped thinking about how cool they were. Also a creative person, but in a more refined, almost bureaucratic way.</p>
<h3>full back.</h3><p>You understand that what sells is location, location, location. You've got big ideas and need big ways to share them. You're the type to strike up conversations with strangers and make them feel like an old friend.</p>
<h3>left front.</h3><p>You're a consummate professional, always ready to discuss your brand. You don't need something loud and attention-seeking to get your ideas across because you have your elevator pitch down pat.</p>
<h3>right front.</h3><p>You're into name brands and won't settle for less. You probably brought this item in to us from your favorite retail store and made sure to tell us how good of a deal you got on it. Learning that popcorn is considered a health snack when it's not drowned in butter was one of the top ten best days of your life.</p>
<h3>right sleeve, long.</h3><p>Sometimes subtlety is important, but not to you. You want your message to be seen, heard, felt, smelt, and much more. You've probably seen all of the Die Hard movies, including the bad ones.</p>
<h3>left sleeve, long.</h3><p>You specifically chose a long-sleeved item so you could print here. You have a cool saying or catchphrase with two of your friends. Sometimes you can be a bit too much, but the people who love you look past it.</p>
<h3>right wrist.</h3><p>You're right-handed and know the value of a firm handshake in a first impression. You want to be unique without having to say it. You probably only have one other location printed on this shirt.</p>
<h3>left wrist.</h3><p>You appreciate subtlety more than that "flashy old locker tag". You're nostalgic for a specific restaurant from your youth that closed down at least 5 years ago.</p>
<h3>hood.</h3><p>You ooze cool. You know a thing or two about a thing or two when it comes to alternative branding. Life has thrown you curveballs, and you've either crushed them or dodged out of the way.</p>
<h3>lower back.</h3><p>Yes. We see your butt.</p>
<h3>okay, joking aside.</h3>
<p>We specialize in making sure every project that leaves our doors is unique and leaves a lasting impression. An easy way to do this is to change up where we're printing. And moreover, people are more likely to keep wearing the gear you create if it's more retail-focused. Think unique decoration styles and locations, fashion-focused garments, and trendy colors.</p>
<p>If your customers keep wearing the gear past the event or intended use, that's a free billboard walking around, sharing your message. Apparel that transitions from the office to evening activities seamlessly is free marketing. If your giveaway race tee becomes a runner's favorite workout gear, that's zero-cost advertising for next year's race aimed right at the audience you want to bring in. Your cost-per-touch marketing doesn't stop at social media and traditional advertising. It also includes the branded apparel and promotional products you're already investing in. Might as well make it do work for you too.</p>"""),
        ("shirts in sync.", "/blog/shirts-in-sync/",
         "Why marching band season is a graphic designer's dream: set lists, costume inspiration, and special effects from glow-in-the-dark to 3D puff.",
         """
<p>There's something about band season that is always exciting for me. Unlike normal band folk, I'm not excited about it for the early morning marching practice (wait. Are some of you excited about early morning marching?) or even the half time performances and competitions.</p>
<p>I, naturally, am in it for the shirts.</p>
<p>We get to work on a lot of really fun projects throughout the year, but when it's marching season, I typically get to really stretch my creative muscles. Frankly, it's almost anytime a client in the educational arts comes to me, whether it's choir or drama, fine arts, dance, you name it. They typically hand over the reins and give me creative freedom. It's a graphic designer's dream.</p>
<p>With marching bands, I ask for a set list, costume inspiration, and then spend hours listening to the music, researching the background for their theme, and really tailoring the design to something personal. I want to pick out details of the way the music moves and communicates that the musicians who have invested so many hours memorizing and performing would recognize.</p>
<p>I also like to play with a lot of special effects, if the theme calls for it. We've done glow in the dark, UV responsive ink (changes colors in the sun), foil, 3D puff, raised gloss, glitter, all kinds of fun effects that we don't get to tap into often enough. In a world where I've got a lot of constraints in the design being more reserved or the constraint of the garment itself, these projects tend to blow that out of the water and give my artist heart joy.</p>"""),
    ]
    tiles = "".join(
        f'<a class="cell" href="{u}"><h3>{esc(t)}</h3><p class="cellsub">{esc(d)}</p></a>'
        for t, u, d, b in posts)
    blog_schema = {
        "@context": "https://schema.org", "@type": "Blog",
        "@id": BASE + path + "#blog", "url": BASE + path,
        "name": "P&M Apparel Blog",
        "publisher": {"@id": BASE + "/#business"},
        "blogPost": [{"@type": "BlogPosting", "headline": t.rstrip('.'),
                      "url": BASE + u, "description": d} for t, u, d, b in posts],
    }
    body = f"""
<section class="texture hero" style="padding:84px 0 72px">
  <div class="wrap">
    <h1>the blog. notes from the shop.</h1>
    <p class="lead">Thoughts on shirts, print, and the people who wear them.</p>
  </div>
</section>
<section>
  <div class="wrap"><div class="grid cols2">{tiles}</div></div>
</section>
{cta_band()}"""
    title = "Blog | P&M Apparel"
    desc = "Notes from the P&M Apparel shop floor: thoughts on custom shirts, print methods, and the people who wear them."
    write(path, layout(path, title, desc, body,
                       [blog_schema, breadcrumbs([("Home", "/"), ("Blog", path)])]))
    for t, u, d, b in posts:
        b = b.replace("{QUOTE_URL}", QUOTE_URL)
        post_schema = {
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": t.rstrip('.'), "url": BASE + u, "description": d,
            "dateModified": TODAY,
            "author": {"@type": "Organization", "name": "P&M Apparel"},
            "publisher": {"@id": BASE + "/#business"},
        }
        page = f"""
<section class="texture hero" style="padding:84px 0 60px">
  <div class="wrap">
    <nav class="crumbs" style="color:#bbb" aria-label="Breadcrumb"><a style="color:#bbb" href="/">home</a> &rsaquo; <a style="color:#bbb" href="/blog/">blog</a></nav>
    <h1>{esc(t)}</h1>
  </div>
</section>
<section><div class="wrap prose" style="max-width:760px">
{b}
</div></section>
{cta_band()}"""
        tcase = " ".join(w[:1].upper() + w[1:] for w in t.rstrip('.').split())
        write(u, layout(u, f"{tcase} | P&M Apparel Blog", d, page, extra_schema=[post_schema,
              breadcrumbs([("Home", "/"), ("Blog", "/blog/"), (tcase, u)])], og_type="article"))

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
    html_out = _external_blank_target(html_out)
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(html_out)

# ---------------------------------------------------------------- SITE FILES
PAGE_PATHS = ["/", "/pricing/", "/flyover-con/", "/blog/how-to-lower-per-shirt-cost/",
    "/services/", "/services/screen-printing/", "/services/embroidery/",
    "/services/fusion/", "/services/sublimation/", "/services/live-printing/",
    "/services/e-commerce/", "/services/state-shirts/", "/customer-supplied-garments/",
    "/iowa-on-demand/", "/about-us/", "/press/", "/faq/", "/contact/", "/shirts-for-scholarships/",
    "/privacy-policy/",
    "/blog/", "/blog/screen-printing-vs-dtf/", "/blog/embroidery-vs-screen-printing/",
    "/blog/what-is-sublimation-good-for/", "/blog/how-quotes-work/",
    "/blog/its-just-a-shirt/", "/blog/its-not-just-a-shirt/",
    "/blog/what-your-print-location-says-about-you/", "/blog/shirts-in-sync/"]

def site_files():
    with open(os.path.join(OUT, "styles.css"), "w") as f:
        f.write(CSS)
    urls = "".join(
        f"<url><loc>{BASE}{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in PAGE_PATHS)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(
            "User-agent: *\nAllow: /\n\n"
            "User-agent: GPTBot\nAllow: /\n\n"
            "User-agent: OAI-SearchBot\nAllow: /\n\n"
            "User-agent: ClaudeBot\nAllow: /\n\n"
            "User-agent: Claude-SearchBot\nAllow: /\n\n"
            "User-agent: PerplexityBot\nAllow: /\n\n"
            "User-agent: Google-Extended\nAllow: /\n\n"
            f"Sitemap: {BASE}/sitemap.xml\n")
    with open(os.path.join(OUT, "llms.txt"), "w") as f:
        f.write(f"""# P&M Apparel

> Woman-owned, third-generation custom apparel company in Polk City, Iowa, serving Ankeny and the Des Moines metro since 1987. Screen printing, embroidery, DTF/fusion transfers, sublimation, promotional products, free online team stores, live event printing, and print-on-demand school apparel via Iowa On Demand. Ships worldwide (all 50 states and 29 countries last year).

Contact: {PHONE}, {EMAIL}, {ADDR}, {CITY}, {STATE} {ZIP}. Hours: Monday-Friday 8am-5pm.

Key facts: 12-piece recommended minimum for screen printing (1-piece minimums for embroidery and DTF). Standard turnaround 8-10 business days after art approval for screen printing, embroidery, and DTF; sublimation runs 3-4 weeks. Rush available (same day if in stock). Quotes within 24 hours. One-time $35 embroidery setup. Custom art $100/hr, first 30 minutes free with production orders. Customer-supplied garments welcome with waiver. Free online team stores (Chipply). Pantone matching available. Brands: Gildan, Bella+Canvas, Comfort Colors, Carhartt, Nike, Adidas, Under Armour.

## Pages
- [How Pricing Works]({BASE}/pricing/): the six variables that move per-piece price, fees in writing
- [Flyover Con]({BASE}/flyover-con/): low-cost apparel industry event inside P&M's working print shop
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
- [Press & Recognition]({BASE}/press/): podcasts, articles, and industry recognition
- [Contact]({BASE}/contact/)
- [Privacy Policy]({BASE}/privacy-policy/)
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
    generate_favicons()
    generate_social_image()
    home()
    services_index()
    pricing()
    flyover()
    all_services()
    csg_page()
    about()
    press()
    iowa_on_demand()
    scholarships()
    privacy()
    contact()
    faq_page()
    blog()
    notfound()
    site_files()
    readme()
    n = sum(len(files) for _, _, files in os.walk(OUT))
    print(f"Built {n} files into {OUT}/")

#!/usr/bin/env python3
"""Post-build gate for pmapparel.com. Run after build.py, before packaging.

Checks:
  1. no placeholder href="#"
  2. rel="noopener" on every external link
  3. no duplicate <title> or meta description across pages
  4. every JSON-LD block parses
  5. no em dashes anywhere
  6. sitemap lists every built page, and every listed URL exists
  7. exactly one <h1> per page
Exit code 0 = clean, 1 = failures.
"""
import json, os, re, sys
from collections import defaultdict

SITE = "site"
BASE = "https://www.pmapparel.com"
failures = []


def fail(msg):
    failures.append(msg)


def pages():
    for root, _, files in os.walk(SITE):
        for f in files:
            if f.endswith(".html"):
                path = os.path.join(root, f)
                yield path, open(path, encoding="utf-8").read()


def url_for(path):
    rel = os.path.relpath(path, SITE).replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


titles, descs = defaultdict(list), defaultdict(list)
built = set()

for path, html in pages():
    url = url_for(path)
    if not path.endswith("404.html"):
        built.add(url)

    # 1. placeholder links
    if re.search(r'href\s*=\s*"#"', html):
        fail(f"{url}: placeholder href=\"#\"")

    # 2. noopener on external links
    for m in re.finditer(r"<a\b[^>]*>", html):
        tag = m.group(0)
        href = re.search(r'href\s*=\s*"([^"]*)"', tag)
        if not href:
            continue
        h = href.group(1)
        if h.startswith("http") and not h.startswith(BASE):
            if "noopener" not in tag:
                fail(f"{url}: external link missing rel=noopener -> {h[:60]}")

    # 3. collect titles/descriptions
    t = re.search(r"<title>(.*?)</title>", html, re.S)
    if t:
        titles[t.group(1).strip()].append(url)
    d = re.search(r'<meta\s+name="description"\s+content="(.*?)"', html, re.S)
    if d:
        descs[d.group(1).strip()].append(url)

    # 4. JSON-LD parses
    for i, block in enumerate(
        re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
    ):
        try:
            json.loads(block)
        except Exception as e:
            fail(f"{url}: JSON-LD block {i} does not parse ({e})")

    # 5. em dashes
    if "\u2014" in html:
        fail(f"{url}: contains an em dash")

    # 7. exactly one h1
    n = len(re.findall(r"<h1\b", html))
    if n != 1:
        fail(f"{url}: found {n} <h1> tags, expected 1")

for t, urls in titles.items():
    if len(urls) > 1:
        fail(f"duplicate <title> on {', '.join(urls)}: {t[:60]}")
for d, urls in descs.items():
    if len(urls) > 1:
        fail(f"duplicate meta description on {', '.join(urls)}: {d[:60]}")

# 6. sitemap
sm_path = os.path.join(SITE, "sitemap.xml")
if not os.path.exists(sm_path):
    fail("sitemap.xml is missing")
else:
    sm = open(sm_path, encoding="utf-8").read()
    listed = {u.replace(BASE, "") or "/" for u in re.findall(r"<loc>(.*?)</loc>", sm)}
    for u in sorted(built - listed):
        fail(f"built but not in sitemap: {u}")
    for u in sorted(listed - built):
        fail(f"in sitemap but not built: {u}")

# also check non-html assets for em dashes
for name in ("llms.txt", "robots.txt", "styles.css"):
    p = os.path.join(SITE, name)
    if os.path.exists(p) and "\u2014" in open(p, encoding="utf-8").read():
        fail(f"{name}: contains an em dash")

if failures:
    print(f"FAIL: {len(failures)} issue(s)\n")
    for f in failures:
        print("  -", f)
    sys.exit(1)

print(f"PASS: {len(built)} pages clean.")

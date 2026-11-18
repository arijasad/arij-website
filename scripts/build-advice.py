#!/usr/bin/env python3
"""Render the reviewed admissions advice, without a production build dependency."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json
import re
from site_navigation import install_archive_navigation

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/advice-pages.json').read_text())
ORIGIN = 'https://maths.arijasad.com/'
CHECKED = '2026-11-09'
TEMPLATE = (ROOT / 'when-to-start-step.html').read_text()
HEADER = re.search(r'<header class="site-header">.*?</header>', TEMPLATE, re.S)[0].replace(' aria-current="page"', '')
FOOTER = re.search(r'<footer>.*?</footer>', TEMPLATE, re.S)[0]

class Headings(HTMLParser):
    def __init__(self):
        super().__init__(); self.items = []; self.current = None
    def handle_starttag(self, tag, attrs):
        if tag == 'h2': self.current = [dict(attrs).get('id'), '']
    def handle_data(self, data):
        if self.current is not None: self.current[1] += data
    def handle_endtag(self, tag):
        if tag == 'h2' and self.current:
            assert self.current[0], 'Every advice h2 needs an anchor'
            self.items.append(self.current); self.current = None

def card(p):
    return f'<article class="resource-card"><div class="resource-card__label">{escape(p["category"])}</div><h3><a href="{p["slug"]}.html">{escape(p["cardTitle"])}</a></h3><p>{escape(p["description"])}</p></article>'

def advice_hub(p, body, cycle, sources, related):
    """Give the advice landing page the same section layout as the resource hub."""
    parts = re.split(r'(?=<h2 id=")', body)
    introductions = re.findall(r'<p>.*?</p>', parts[0], re.S)
    sections = []
    colours = {
        'course-guides': 'white', 'compare': 'dark', 'independent': 'cream',
        'tests': 'white', 'dates': 'cream', 'ucas': 'white',
        'practice': 'cream', 'faq': 'white',
    }
    for part in parts[1:]:
        anchor = re.match(r'<h2 id="([^"]+)"', part)[1]
        if anchor == 'course-guides' and introductions:
            part = part.replace('</h2>', '</h2>' + introductions[0], 1)
        if anchor == 'practice' and len(introductions) > 1:
            part = part.replace('</h2>', '</h2>' + introductions[1], 1)
        sections.append(f'<section class="resource-section guide-section guide-section--{colours[anchor]}" aria-labelledby="{anchor}"><div class="container">{part}</div></section>')
    return f'''<main id="main-content">
<section class="resource-hero"><div class="container"><div class="resource-hero__inner"><div class="eyebrow">Cambridge &amp; Oxford applications</div><h1>UCAS <span>application advice.</span></h1><p class="resource-lede">{escape(p['lede'])}</p><p class="guide-meta">{cycle}</p><nav class="guide-jump-links" aria-label="On this page"><a href="#course-guides">Choose your course</a><a href="#tests">Tests &amp; dates</a><a href="#ucas">Application &amp; preparation</a></nav></div></div></section>
{''.join(sections)}
<section class="resource-section guide-section guide-section--cream"><div class="container guide-next-steps"><details class="guide-sources"><summary id="official-sources">Official sources</summary><p>Use these sources for the requirements that apply to your entry year. Follow any specific instructions from your college, including the conditions of your offer.</p><ul>{sources}</ul></details><div><h2 id="read-next">Useful next steps</h2><ul>{related}</ul></div></div></section>
</main>'''

for p in DATA['pages']:
    path = p['slug'] + '.html'
    body = (ROOT / 'content/advice' / path).read_text()
    body = body.replace('<div class="advice-table-wrap"', '<p class="advice-table-hint">On a small screen, scroll the table sideways to compare both columns.</p><div class="advice-table-wrap"')
    if p['slug'] == 'advice':
        for category in ['Course guide', 'Comparison', 'Independent preparation']:
            body = body.replace('{{' + category + '}}', '<div class="resource-grid advice-grid">' + ''.join(card(q) for q in DATA['pages'] if q['category'] == category) + '</div>')
    parser = Headings(); parser.feed(body)
    toc = ''.join(f'<a href="#{i}">{escape(t)}</a>' for i, t in parser.items)
    sources = ''.join(f'<li id="source-{key}"><a href="{escape(DATA["sources"][key]["url"])}">{escape(DATA["sources"][key]["title"])}</a></li>' for key in p['sources'])
    related = ''.join(f'<li><a href="{escape(url)}">{escape(label)}</a></li>' for url, label in p['related'])
    byline = '<a href="about.html">Arij Asad</a>'
    cycle = 'For applications in autumn 2026 for entry in 2027, or deferred entry in 2028.'
    schema = {
        '@context': 'https://schema.org', '@graph': [
            {'@type': 'CollectionPage' if p['slug'] == 'advice' else 'Article',
             '@id': ORIGIN + path, 'url': ORIGIN + path, 'headline': p['title'],
             'name': p['title'], 'description': p['description'],
             'datePublished': CHECKED, 'dateModified': CHECKED,
             'author': {'@type': 'Person', '@id': ORIGIN + 'about.html#arij-asad', 'name': 'Arij Asad', 'url': ORIGIN + 'about.html'},
             'mainEntityOfPage': ORIGIN + path, 'inLanguage': 'en-GB',
             'isPartOf': {'@type': 'WebSite', 'name': 'Arij Asad Maths', 'url': ORIGIN},
             'citation': [DATA['sources'][k]['url'] for k in p['sources']]},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': ORIGIN},
                {'@type': 'ListItem', 'position': 2, 'name': 'UCAS application advice', 'item': ORIGIN+'advice.html'}
            ] + ([] if p['slug'] == 'advice' else [{'@type': 'ListItem', 'position': 3, 'name': p['cardTitle'], 'item': ORIGIN+path}])}
        ]}
    crumb = 'UCAS application advice' if p['slug'] == 'advice' else f'<a href="advice.html">UCAS application advice</a> / {escape(p["cardTitle"])}'
    document = f'''<!DOCTYPE html>
<html lang="en-GB"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(p['title'])} | Arij Asad</title>
<meta name="description" content="{escape(p['description'])}">
<link rel="canonical" href="{ORIGIN+path}"><link rel="icon" href="/favicon.ico?v=dd9f0d4a0c">
<link rel="stylesheet" href="site.css?v=advice-20261109"><link rel="stylesheet" href="advice.css?v=20261109">
<meta name="theme-color" content="#111111">
<meta property="og:type" content="{'website' if p['slug']=='advice' else 'article'}"><meta property="og:title" content="{escape(p['title'])}">
<meta property="og:description" content="{escape(p['description'])}"><meta property="og:url" content="{ORIGIN+path}">
<meta property="og:image" content="{ORIGIN}assets/step-workshop.webp"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head><body class="resource-page advice-page">
<a class="skip-link" href="#main-content">Skip to main content</a>
{HEADER}
<main id="main-content">
<header class="article-hero"><div class="container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {crumb}</nav><div class="eyebrow">{escape(p['category'])}</div><h1>{escape(p['heading'])}</h1><p class="resource-lede">{escape(p['lede'])}</p><div class="article-meta"><span>By {byline}</span></div></div></header>
<div class="container advice-cycle"><p>{cycle}</p></div>
<div class="container article-layout">
<article class="article-body">
{body}
<section class="advice-sources" aria-labelledby="official-sources"><h2 id="official-sources">Official sources</h2><p>Use these sources for the requirements that apply to your entry year. Follow any specific instructions from your college, including the conditions of your offer.</p><ul>{sources}</ul><p class="article-disclaimer">An independent guide by Arij Asad. Preparation suggestions reflect my teaching experience.</p></section>
<section aria-labelledby="read-next"><h2 id="read-next">Useful next steps</h2><ul>{related}</ul></section>
</article>
<aside class="article-aside" aria-label="On this page"><strong>In this guide</strong><nav aria-label="Guide sections">{toc}<a href="#official-sources">Official sources</a></nav><a href="advice.html">All UCAS application advice</a></aside>
</div></main>{FOOTER}<script src="site.js?v=20261109-advice" defer></script></body></html>'''
    if p['slug'] == 'advice':
        document = document.replace('class="resource-page advice-page"', 'class="resource-page advice-page guide-page advice-hub"')
        document = document.replace('</head>', '<link rel="stylesheet" href="assets/guide-layout.css?v=20261118"></head>')
        document = re.sub(r'<main id="main-content">.*?</main>', lambda _: advice_hub(p, body, cycle, sources, related), document, count=1, flags=re.S)
    document = install_archive_navigation(document, path)
    (ROOT/path).write_text(document)
print(f'Built {len(DATA["pages"])} admissions advice pages.')

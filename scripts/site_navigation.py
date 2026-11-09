"""Shared, crawlable navigation for the build-free tuition website."""
from html import escape
import re

ARCHIVES = [
    ('tmua-paper-archive.html', 'TMUA'),
    ('mat-past-papers.html', 'MAT'),
    ('step-past-papers.html', 'STEP'),
    ('esat-paper-archive.html', 'ESAT'),
    ('jmc-past-papers.html', 'JMC'),
    ('imc-past-papers.html', 'IMC'),
    ('smc-past-papers.html', 'SMC'),
    ('amc10-past-papers.html', 'AMC 10'),
    ('amc12-past-papers.html', 'AMC 12'),
    ('aime-past-papers.html', 'AIME'),
    ('bmo-past-papers.html', 'BMO'),
]
STYLE = '<link rel="stylesheet" href="/paper-navigation.css?v=20260910-1">'


def archive_navigation(current_path, chinese=False):
    label = '历年试题（英文）' if chinese else 'Past paper archives'
    links = []
    for path, name in ARCHIVES:
        current = ' aria-current="page"' if path == current_path else ''
        language = ' hreflang="en-GB" lang="en"' if chinese else ''
        links.append(f'<a href="/{path}" aria-label="{escape(name)} paper archive"{current}{language}>{escape(name)}</a>')
    return ('  <!-- Shared past-paper navigation -->\n'
            f'  <nav class="paper-archive-bar" aria-label="{label}">\n'
            '    <div class="paper-archive-bar__inner">\n'
            f'      <span class="paper-archive-bar__label">{label}</span>\n'
            '      <div class="paper-archive-bar__links">' + ''.join(links) + '</div>\n'
            '    </div>\n'
            '  </nav>\n'
            '  <!-- /Shared past-paper navigation -->')


def install_archive_navigation(document, current_path):
    # Keep the advice entry crawlable and present after any page regeneration.
    def add_advice(match):
        navigation = match.group(0)
        navigation = re.sub(r'<a\b[^>]*href="/?advice\.html"[^>]*>.*?</a>', '', navigation, flags=re.S)
        current = ' aria-current="page"' if current_path == 'advice.html' else ''
        chinese = bool(re.search(r'<html[^>]+lang="zh', document))
        label = '申请建议（英文）' if chinese else 'Advice'
        language = ' lang="en" hreflang="en-GB"' if chinese else ''
        link = f'<a href="/advice.html"{current}{language}>{label}</a>'
        return re.sub(r'(<a\b[^>]*href="/?resources\.html")', link + r'\1', navigation, count=1)
    document = re.sub(r'<nav\b[^>]*class="nav-links"[^>]*>.*?</nav>', add_advice, document, flags=re.S)
    document = re.sub(r'\n?  <!-- Shared past-paper navigation -->.*?<!-- /Shared past-paper navigation -->', '', document, flags=re.S)
    header = re.search(r'<header\b[^>]*class="site-header"[^>]*>.*?</header>', document, re.S)
    if header is None:
        return document
    chinese = bool(re.search(r'<html[^>]+lang="zh', document))
    document = document[:header.end()] + '\n' + archive_navigation(current_path, chinese) + document[header.end():]
    document = re.sub(r'\s*<link[^>]+href="/?paper-navigation\.css[^>]*>', '', document)
    return document.replace('</head>', '  ' + STYLE + '\n</head>', 1)

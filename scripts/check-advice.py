#!/usr/bin/env python3
"""Check published HTML metadata, new local links and retained content."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import json
import subprocess
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'data/advice-pages.json').read_text())
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__();self.ids=[];self.links=[];self.h1=0;self.meta={};self.canonical=[];self.scripts=[];self.script=None;self.title='';self.in_title=False;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a' and 'href' in a:self.links.append(a['href'])
        if tag=='h1':self.h1+=1
        if tag=='meta':self.meta[a.get('name',a.get('property',''))]=a.get('content','')
        if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a.get('href'))
        if tag=='script' and a.get('type')=='application/ld+json':self.script=''
        if tag=='title':self.in_title=True
    def handle_data(self,data):
        if self.script is not None:self.script+=data
        if self.in_title:self.title+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.script is not None:self.scripts.append(json.loads(self.script));self.script=None
        if tag=='title':self.in_title=False

pages={p.name:Page(p.read_text()) for p in ROOT.glob('*.html')}
errors=[];added_links={};new_names={p['slug']+'.html' for p in DATA['pages']}
for name,page in pages.items():
    previous=subprocess.run(['git','show','HEAD:'+name],cwd=ROOT,capture_output=True,text=True)
    old=Page(previous.stdout).links if previous.returncode==0 else []
    added=sorted(set(page.links)-set(old));added_links[name]=added
    for href in added:
        u=urlsplit(href)
        if u.scheme or u.netloc:continue
        path=unquote(u.path).lstrip('/') or (name if u.fragment else 'index.html')
        dest=ROOT/path
        if dest.is_dir():dest=dest/'index.html'
        if not dest.exists():errors.append(f'{name}: missing target {href}')
        elif u.fragment and dest.name in pages and unquote(u.fragment) not in pages[dest.name].ids:errors.append(f'{name}: missing anchor {href}')
    if name in new_names:
        if page.h1!=1:errors.append(f'{name}: expected one h1')
        if len(page.ids)!=len(set(page.ids)):errors.append(f'{name}: duplicate ids')
        if page.canonical!=['https://maths.arijasad.com/'+name]:errors.append(f'{name}: canonical mismatch')
        if not page.meta.get('description'):errors.append(f'{name}: no description')
        if 'noindex' in page.meta.get('robots',''):errors.append(f'{name}: noindex')
        if not page.scripts:errors.append(f'{name}: no structured data')
        if '{{' in (ROOT/name).read_text():errors.append(f'{name}: unrendered template')
titles=[pages[n].title for n in new_names]
if len(titles)!=len(set(titles)):errors.append('Duplicate new page titles')
sitemap=ET.parse(ROOT/'sitemap.xml');locations={e.text for e in sitemap.findall('.//{*}loc')}
for n in new_names:
    if 'https://maths.arijasad.com/'+n not in locations:errors.append(f'{n}: absent from sitemap')
# Archive catalogue content must remain exactly the same except the reviewed routes/date.
for exam in ['tmua','step','mat','esat']:
    name=f'data/paper-archives/{exam}.json'
    old=json.loads(subprocess.check_output(['git','show','HEAD:'+name],cwd=ROOT,text=True));new=json.loads((ROOT/name).read_text())
    for d in [old,new]:
        d.pop('adviceLinks',None);d.pop('dateModified',None)
    if old!=new:errors.append(f'{exam}: unintended archive data change')
if errors:
    print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(new_names)} new pages; metadata, schema and sitemap valid. {sum(len(v) for v in added_links.values())} added hrefs inspected; local targets and anchors checked. Existing archive data retained.')

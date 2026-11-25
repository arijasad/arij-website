#!/usr/bin/env python3
"""Package every public HTML page into one navigable, unpublished review file.

Only the output artifact is transformed: production source pages are never edited.
Styles, scripts and images are embedded. Downloadable papers use their live URLs.
Analytics and real enquiry submission are disabled within the review file.
"""
from pathlib import Path
from html import escape, unescape
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
import argparse
import base64
import json
import mimetypes
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://maths.arijasad.com/'

class Tag(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.attrs = dict(attrs)

def attributes(tag):
    parser = Tag()
    parser.feed(tag)
    return parser.attrs

def local_path(url, relative_to='index.html'):
    parsed = urlsplit(urljoin(ORIGIN + relative_to, unescape(url)))
    if parsed.netloc != 'maths.arijasad.com':
        return None
    path = (ROOT / parsed.path.lstrip('/')).resolve()
    if ROOT.resolve() not in path.parents:
        return None
    return path

def data_uri(path):
    mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return 'data:' + mime + ';base64,' + base64.b64encode(path.read_bytes()).decode()

def css_content(path):
    def replace_url(match):
        value = match.group(1).strip().strip('"\'')
        if value.startswith(('data:', '#')):
            return match.group(0)
        asset = local_path(value, str(path.relative_to(ROOT)))
        target = data_uri(asset) if asset and asset.is_file() else urljoin(ORIGIN + str(path.relative_to(ROOT)), value)
        return 'url("' + target + '")'
    return re.sub(r'url\(([^)]+)\)', replace_url, path.read_text())

CHILD_SCRIPT = r'''
(() => {
  const route = window.__websitePreviewRoute || {path:'index.html', search:'', hash:''};
  const reveal = hash => {
    route.hash = hash || '';
    window.dispatchEvent(new Event('hashchange'));
    let id;
    try { id = decodeURIComponent((hash || '').slice(1)); } catch (_) { return; }
    const target = document.getElementById(id);
    if (!target) { if (!hash) window.scrollTo(0, 0); return; }
    let details = target.closest('details');
    while (details) { details.open = true; details = details.parentElement?.closest('details'); }
    target.scrollIntoView();
  };
  window.addEventListener('message', event => {
    if (event.source === parent && event.data?.type === 'website-preview-anchor') reveal(event.data.hash);
  });
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href]');
    if (!anchor) return;
    const url = new URL(anchor.getAttribute('href'), 'https://maths.arijasad.com/' + route.path + route.search);
    if (url.origin !== 'https://maths.arijasad.com') return;
    const path = url.pathname === '/' ? 'index.html' : url.pathname.slice(1);
    if (!(path.endsWith('.html') || url.pathname === '/')) return;
    event.preventDefault();
    parent.postMessage({type:'website-preview-navigate', path, search:url.search, hash:url.hash}, '*');
  });
  const form = document.querySelector('#enquiry-form-fields, #access-application-form');
  if (form) {
    const note = document.createElement('p');
    note.id = 'preview-form-status';
    note.setAttribute('role', 'status');
    note.style.cssText = 'padding:14px 18px;border:1px solid #e3dccf;border-radius:10px;background:#f7f5f0;color:#72531c;';
    note.textContent = 'Preview only: this form will not send any information.';
    form.prepend(note);
    form.addEventListener('submit', event => {
      event.preventDefault();
      note.textContent = 'Preview checked: no information has been sent.';
      if (form.dataset.previewNext) {
        parent.postMessage({type:'website-preview-navigate',path:form.dataset.previewNext,search:'?preview=1',hash:''}, '*');
      }
      note.scrollIntoView({block:'center'});
    });
  }
  if (route.search.includes('preview=1') && route.path === 'access-scheme-next-steps.html') {
    const notice = document.createElement('p');
    notice.setAttribute('role', 'status');
    notice.style.cssText = 'padding:18px;background:#ead9b6;color:#111;margin:0;';
    notice.textContent = 'Preview only: your application has not been sent. These are the next steps after a real submission.';
    document.querySelector('main').prepend(notice);
  }
  document.querySelectorAll('[data-cookie-settings]').forEach(button => button.addEventListener('click', () => {
    alert('Analytics are disabled in this preview.');
  }));
  reveal(route.hash);
})();
'''

def transform(path):
    html = path.read_text()
    def style_link(match):
        tag = match.group(0)
        attrs = attributes(tag)
        if attrs.get('rel') == 'canonical':
            return ''
        if attrs.get('rel') == 'stylesheet':
            css = local_path(attrs['href'], path.name)
            if css and css.is_file():
                return '<style>' + css_content(css) + '</style>'
            raise ValueError(f'Missing preview stylesheet: {path.name}: {attrs["href"]}')
        if attrs.get('rel') in ('icon', 'shortcut icon'):
            icon = local_path(attrs.get('href', ''), path.name)
            if icon and icon.is_file():
                return re.sub(r'href\s*=\s*(["\']).*?\1', lambda _: 'href="' + data_uri(icon) + '"', tag)
        return tag
    html = re.sub(r'<link\b[^>]*>', style_link, html, flags=re.I)
    html = re.sub(r'<base\b[^>]*>', '', html, flags=re.I)
    html = re.sub(r'<meta\b[^>]*name=["\']robots["\'][^>]*>', '', html, flags=re.I)
    html = html.replace('</head>', '<meta name="robots" content="noindex,nofollow"></head>', 1)
    scripts = []
    def script_tag(match):
        tag, source = match.group(1), match.group(2)
        attrs = attributes(tag + '>')
        if attrs.get('type') in ('application/ld+json', 'application/json'):
            return match.group(0)
        if attrs.get('src'):
            script = local_path(attrs['src'], path.name)
            if not script or not script.is_file():
                raise ValueError(f'Missing script: {path.name}: {attrs["src"]}')
            source = script.read_text()
            if script.name == 'site.js':
                # Retain menus, copy-email and enquiry prefill, without analytics.
                source = source.split('(() => {', 1)[0]
                source = source.replace('window.location.search', '(window.__websitePreviewRoute?.search || "")')
        source = source.replace('window.location.hash', '(window.__websitePreviewRoute?.hash || window.location.hash)')
        if source.strip():
            scripts.append(source)
        return ''
    html = re.sub(r'(<script\b[^>]*?)>(.*?)</script\s*>', script_tag, html, flags=re.I | re.S)
    def image_tag(match):
        tag = match.group(0)
        attrs = attributes(tag)
        if attrs.get('src'):
            asset = local_path(attrs['src'], path.name)
            if asset and asset.is_file():
                tag = re.sub(r'src\s*=\s*(["\']).*?\1', lambda _: 'src="' + data_uri(asset) + '"', tag)
            elif asset:
                raise ValueError(f'Missing image: {path.name}: {attrs["src"]}')
        return tag
    html = re.sub(r'<img\b[^>]*>', image_tag, html, flags=re.I)
    def anchor_tag(match):
        tag = match.group(0)
        attrs = attributes(tag)
        href = attrs.get('href')
        if not href:
            return tag
        absolute = urljoin(ORIGIN + path.name, href)
        parsed = urlsplit(absolute)
        is_page = parsed.netloc == 'maths.arijasad.com' and (parsed.path.endswith('.html') or parsed.path == '/')
        destination = href if href.startswith('#') else absolute
        tag = re.sub(r'href\s*=\s*(["\']).*?\1', lambda _: 'href="' + escape(destination, quote=True) + '"', tag)
        tag = re.sub(r'\s+target\s*=\s*(["\']).*?\1', '', tag)
        if not is_page and parsed.scheme in ('http', 'https'):
            tag = tag[:-1] + ' target="_blank" rel="noopener">'
        return tag
    html = re.sub(r'<a\b[^>]*>', anchor_tag, html, flags=re.I)
    def preview_form(match):
        tag = match.group(0)
        if attributes(tag).get('id') not in ('enquiry-form-fields', 'access-application-form'):
            return tag
        tag = re.sub(r'\s+(?:action|method)\s*=\s*(["\']).*?\1', '', tag, flags=re.I)
        return tag[:-1] + ' method="dialog">'
    html = re.sub(r'<form\b[^>]*>', preview_form, html, flags=re.I)
    for script in scripts:
        if re.search(r'</script', script, re.I):
            raise ValueError('Unsafe script terminator in ' + path.name)
    html = html.replace('</body>', ''.join('<script>' + s + '</script>' for s in scripts) + '<script>' + CHILD_SCRIPT + '</script></body>')
    return html

SHELL_CSS = '''
*{box-sizing:border-box}body{margin:0;background:#f7f5f0;color:#1c1c1c;font:14px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.preview-bar{min-height:76px;padding:12px 20px;background:#f7f5f0;color:#1c1c1c;display:flex;align-items:center;justify-content:space-between;gap:20px}.preview-bar p{margin:0;font-size:12px}.preview-controls{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.preview-controls button,.preview-controls select{min-height:40px;padding:8px 12px;border:1px solid #95846a;border-radius:8px;background:#f7f5f0;color:#1c1c1c;font:inherit;font-size:12px;cursor:pointer}.preview-controls button[aria-current=page]{background:#ead9b6;color:#111}.preview-controls button:disabled{opacity:.45;cursor:default}.preview-controls select{max-width:210px}.preview-controls label{font-size:12px}.preview-frame{display:block;width:100%;height:calc(100vh - 76px);height:calc(100dvh - 76px);min-height:500px;border:0;background:#f7f5f0}.sr-only{position:absolute;clip:rect(0,0,0,0);width:1px;height:1px;overflow:hidden}:focus-visible{outline:3px solid #b5975f;outline-offset:3px}@media(max-width:950px){.preview-bar{display:block}.preview-controls{margin-top:9px}.preview-frame{height:calc(100dvh - 124px)}}@media(max-width:540px){.preview-controls{gap:6px}.preview-controls button,.preview-controls select{padding:6px 9px;min-height:36px}.preview-controls select{max-width:160px}.preview-frame{height:calc(100dvh - 166px)}}
body{height:100vh;height:100dvh;display:flex;flex-direction:column}.preview-bar{flex:0 0 auto}.preview-frame{flex:1 1 auto;height:0;min-height:0;max-width:100%;margin-inline:auto}
'''

SHELL_SCRIPT = r'''
const pages = __PAGES__;
const frame = document.getElementById('website-preview');
const picker = document.getElementById('page-picker');
const viewport = document.getElementById('viewport-picker');
viewport.addEventListener('change', () => { frame.style.width = viewport.value === 'full' ? '100%' : viewport.value + 'px'; });
const back = document.getElementById('preview-back');
const forward = document.getElementById('preview-forward');
const trail = [];
let position = -1;
let current = null;
function showPage(path, search='', hash='', record=true) {
  if (!Object.prototype.hasOwnProperty.call(pages,path)) {
    document.getElementById('preview-status').textContent = 'This page is not included in the preview.';
    return;
  }
  const route = {path,search,hash};
  if (record) { trail.splice(position+1); trail.push(route); position=trail.length-1; }
  if (current && current.path===path && current.search===search) {
    frame.contentWindow.postMessage({type:'website-preview-anchor',hash},'*');
  } else {
    const boot = '<script>window.__websitePreviewRoute='+JSON.stringify(route).replace(/</g,'\u003c')+';'+ '</scr'+'ipt>';
    frame.srcdoc = pages[path].html.replace(/<head\b[^>]*>/i, tag=>tag+boot);
  }
  current=route;
  picker.value=path;
  document.querySelectorAll('[data-page]').forEach(b=>{
    if(b.dataset.page===path)b.setAttribute('aria-current','page');else b.removeAttribute('aria-current');
  });
  document.getElementById('preview-status').textContent=pages[path].title;
  back.disabled=position<=0;forward.disabled=position>=trail.length-1;
}
document.querySelectorAll('[data-page]').forEach(b=>b.addEventListener('click',()=>showPage(b.dataset.page)));
picker.addEventListener('change',()=>showPage(picker.value));
back.addEventListener('click',()=>{if(position>0){position--;const r=trail[position];showPage(r.path,r.search,r.hash,false);}});
forward.addEventListener('click',()=>{if(position<trail.length-1){position++;const r=trail[position];showPage(r.path,r.search,r.hash,false);}});
window.addEventListener('message',event=>{
  if(event.source===frame.contentWindow && event.data?.type==='website-preview-navigate') {
    showPage(event.data.path,event.data.search||'',event.data.hash||'');
  }
});
const requestedPage = new URLSearchParams(window.location.search).get('page');
showPage(Object.prototype.hasOwnProperty.call(pages,requestedPage) ? requestedPage : 'index.html', '', window.location.hash);
'''

def build(output):
    pages = {}
    for path in sorted(ROOT.glob('*.html')):
        html = transform(path)
        title = re.search(r'<title>(.*?)</title>', html, re.S | re.I)
        title = unescape(' '.join(title[1].split())) if title else path.stem
        pages[path.name] = {'title':title, 'html':html}
    payload = json.dumps(pages, ensure_ascii=False).replace('<', '\\u003c')
    options = ''.join(f'<option value="{path}">{escape(p["title"].split(" | ")[0])}</option>' for path,p in pages.items())
    buttons = ''.join(f'<button type="button" data-page="{path}">{label}</button>' for path,label in [('index.html','Home'),('interviews.html','Interviews & access scheme'),('access-scheme-application.html','Free interview application'),('cambridge-college-maths-interviews.html','Cambridge interviews'),('oxford-maths-interview-guide.html','Oxford interviews'),('engineering-interview-guide.html','Engineering')])
    shell = f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Arij Asad Maths | Whole website preview</title><style>{SHELL_CSS}</style></head><body><header class="preview-bar"><p>Whole website preview · {len(pages)} pages · Private preview<br><span id="preview-status" role="status">Home</span></p><nav class="preview-controls" aria-label="Website preview controls"><button type="button" id="preview-back" aria-label="Previous preview page">←</button><button type="button" id="preview-forward" aria-label="Next preview page">→</button>{buttons}<label class="sr-only" for="page-picker">All pages</label><select id="page-picker" aria-label="All website pages">{options}</select><label class="sr-only" for="viewport-picker">Preview width</label><select id="viewport-picker" aria-label="Preview width"><option value="full">Desktop / full width</option><option value="768">Tablet · 768px</option><option value="390">Phone · 390px</option><option value="320">Small phone · 320px</option></select></nav></header><noscript><p>Enable JavaScript to navigate the full website preview.</p></noscript><iframe class="preview-frame" id="website-preview" title="Arij Asad Maths website preview" srcdoc="{escape(pages['index.html']['html'],quote=True)}"></iframe><script>{SHELL_SCRIPT.replace('__PAGES__',payload)}</script></body></html>'''
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(shell)
    print(f'Built {len(pages)} pages into {output} ({output.stat().st_size:,} bytes).')
    print('Production pages unchanged by preview packaging. Enquiry submission and analytics disabled in preview.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output')
    build(parser.parse_args().output)

"""Add the access scheme without replacing any existing sections."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
STYLE = '<link rel="stylesheet" href="assets/access-scheme.css?v=20261125">'
APPLY = 'access-scheme-application.html'
EMAIL = '<a href="mailto:arijasadmaths@gmail.com">arijasadmaths@gmail.com</a>'
SECTION = '''
<!-- State School Access Scheme -->
<section class="resource-section access-scheme" id="state-school-access" aria-labelledby="access-title">
  <div class="container access-panel">
    <div class="access-compact-header">
      <div><h2 id="access-title">State School Access Scheme</h2><p class="access-summary">One free mathematics mock interview for eligible students at UK state-funded schools and sixth-form colleges, with personalised written feedback and preparation recommendations.</p><p class="access-assurance">No obligation to purchase additional sessions.</p></div>
      <a class="resource-button" href="access-scheme-application.html">Apply for a free mock interview</a>
    </div>
    <details class="access-details">
      <summary>Eligibility and how it works</summary>
      <div class="access-grid">
        <div class="access-introduction">
      <p>I believe that access to high-quality mathematics interview preparation should not depend on a student’s financial circumstances or educational background.</p>
      <p>To help widen access, I offer a limited number of free mathematics mock interviews to students attending UK state-funded schools and sixth-form colleges.</p>
      <ul class="access-includes">
        <li>One free mathematics mock interview, designed to reflect the style and difficulty of an Oxbridge interview.</li>
        <li>Detailed, personalised written feedback on mathematical reasoning, problem-solving approach and communication.</li>
        <li>Recommendations for further interview preparation.</li>
      </ul></div>
        <div class="access-verification">
      <h3>Eligibility and verification</h3>
      <p>The access scheme is intended primarily for students attending non-selective state schools and sixth-form colleges who have limited access to specialist Oxbridge interview preparation.</p>
      <p>Students attending specialist mathematics schools are not eligible for free mock interviews under this scheme.</p>
      <p>To verify eligibility, simply ask any teacher at your current school or college to email <a href="mailto:arijasadmaths@gmail.com">arijasadmaths@gmail.com</a> from their official school email address, confirming your full name and current enrolment.</p>
      <p>No formal reference, proof of household income or additional supporting documents are required.</p>
      <p>You can apply before your teacher’s confirmation arrives. Your booking will only be confirmed once verification is received and a time is agreed, subject to availability.</p>
      <p>This initiative is open to eligible new, existing and previous students, including those who have previously booked paid sessions.</p>
      <p>Each eligible student may receive one free mock interview, subject to availability.</p></div>
      </div>
      <p class="access-terms">Students who have previously paid remain eligible for their free mock interview.</p>
    </details>
  </div>
</section>
<!-- /State School Access Scheme -->
'''
def install(document, path):
    if path not in ('index.html', 'interviews.html'):
        return document
    document = re.sub(r'\n?<!-- State School Access Scheme -->.*?<!-- /State School Access Scheme -->\n?', '', document, flags=re.S)
    document = re.sub(r'\s*<link[^>]*href="assets/access-scheme\.css[^>]*>', '', document)
    if path == 'index.html':
        return document
    if '<link rel="stylesheet" href="/site-layout.css' in document:
        document = document.replace('<link rel="stylesheet" href="/site-layout.css', STYLE+'\n  <link rel="stylesheet" href="/site-layout.css',1)
    else:
        document = re.sub(r'<style data-access-scheme>.*?</style>', '', document, flags=re.S)
        document = document.replace('</head>', '<style data-access-scheme>'+(ROOT/'assets/access-scheme.css').read_text()+'</style></head>',1)
    if path == 'interviews.html':
        document = re.sub(r'<a href="#state-school-access">.*?</a>', '', document)
        document = document.replace('</nav></div></div></div></section>', '<a href="#state-school-access">State School Access Scheme</a></nav></div></div></div></section>',1)
        document = document.replace('<section class="resource-section interview-section" id="faq">', SECTION+'<section class="resource-section interview-section" id="faq">',1)
    return document
if __name__ == '__main__':
    for name in ('index.html','interviews.html'):
        p=ROOT/name;p.write_text(install(p.read_text(),name))

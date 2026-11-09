#!/usr/bin/env python3
"""Install contextual advice links on existing pages; safe to rerun after rebuilds."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
START = '<!-- Admissions advice route -->'
END = '<!-- /Admissions advice route -->'
routes = {
 'tmua.html': 'Choosing a course? Read the <a href="cambridge-mathematics-application-guide.html">Cambridge Maths</a>, <a href="oxford-mathematics-application-guide.html">Oxford Maths</a> and <a href="cambridge-computer-science-application-guide.html">Cambridge Computer Science</a> application guides, including how TMUA fits each route.',
 'step.html': 'For the wider application, read the <a href="cambridge-mathematics-application-guide.html">Cambridge Mathematics guide</a> or <a href="cambridge-vs-oxford-maths.html">compare Cambridge and Oxford Maths</a>. TMUA and STEP have different roles in the current Cambridge route.',
 'interviews.html': 'Read the full <a href="cambridge-mathematics-application-guide.html">Cambridge Maths application guide</a>, or consider <a href="do-you-need-an-admissions-consultancy.html">what you can prepare independently</a> before deciding whether a practice session would help.',
 'when-to-start-step.html': 'For current course requirements and the relationship between TMUA and STEP, read the <a href="cambridge-mathematics-application-guide.html">Cambridge Maths application guide</a>. For a choice between courses, <a href="cambridge-vs-oxford-maths.html">compare Cambridge and Oxford Maths</a>.',
 'cambridge-maths-interview-guide.html': 'This guide focuses on the discussion. The <a href="cambridge-mathematics-application-guide.html">Cambridge Mathematics application guide</a> covers the wider route, and the <a href="do-you-need-an-admissions-consultancy.html">independent-preparation guide</a> explains how to use free support.',
 'tmua-study-plan.html': 'Before planning the test, check how it fits your course: <a href="cambridge-mathematics-application-guide.html">Cambridge Maths</a>, <a href="oxford-mathematics-application-guide.html">Oxford Maths</a> or <a href="cambridge-computer-science-application-guide.html">Cambridge Computer Science</a>.',
 'maths-challenges.html': 'Thinking about university applications? The <a href="advice.html">admissions advice section</a> explains how mathematical exploration fits alongside subject requirements, tests and interviews. Competition problems can develop useful habits without becoming a medal checklist.',
 'maths-topic-practice.html': 'For a wider plan, choose a course in the <a href="advice.html">Cambridge and Oxford admissions advice section</a>. Use these problems to develop a skill, then return to unfamiliar questions from your chosen assessment.'
}
for filename, text in routes.items():
 p=ROOT/filename; doc=p.read_text()
 doc=re.sub(r'[ \t]*'+re.escape(START)+'.*?'+re.escape(END)+r'\n?', '', doc, flags=re.S)
 block=START+'<section class="advice-route"><div class="container"><h2>Put your preparation in context</h2><p>'+text+'</p></div></section>'+END
 assert '</main>' in doc
 doc=doc.replace('</main>',block+'\n</main>',1);p.write_text(doc)

p=ROOT/'resources.html';doc=p.read_text()
doc=re.sub(r'[ \t]*'+re.escape(START)+'.*?'+re.escape(END)+r'\n?','',doc,flags=re.S)
block='''<section class="resource-section resource-category" id="application-advice"><div class="container"><div class="resource-heading"><h2>Plan an application</h2><p>Course requirements, tests and practical preparation, checked against official sources.</p></div><div class="resource-grid"><article class="resource-card"><div class="resource-card__label">Cambridge and Oxford</div><h3>Maths, Engineering and Computer Science advice</h3><p>Five course guides, course comparisons and a practical look at preparing independently. Clear about Further Maths, three or four A levels and the current TMUA, ESAT and STEP routes.</p><a class="text-link" href="advice.html">Browse the admissions advice</a></article></div></div></section>'''
doc=doc.replace('<section class="resource-section resource-category" id="preparation-guides">',START+block+END+'\n<section class="resource-section resource-category" id="preparation-guides">',1)
doc=doc.replace('<a href="#preparation-guides">Preparation guides</a>','<a href="#preparation-guides">Preparation guides</a><a href="#application-advice">Application advice</a>') if 'href="#application-advice"' not in doc else doc
p.write_text(doc)

p=ROOT/'index.html';doc=p.read_text()
doc=re.sub(r'[ \t]*'+re.escape(START)+'.*?'+re.escape(END)+r'\n?','',doc,flags=re.S)
block=START+'<section class="advice-route"><div class="container"><h2>Considering Cambridge or Oxford?</h2><p>Read the <a href="advice.html">free application guides for Maths, Engineering and Computer Science</a>. Understand the subjects, tests and interviews, compare courses and build an independent preparation plan.</p></div></section>'+END
anchor='<section class="resource-routes"'
# Put the route before the main content closes, outside existing sections.
doc=doc.replace('</main>',block+'\n</main>',1);p.write_text(doc)

for p in ROOT.glob('*.html'):
 doc=p.read_text().replace('site.css?v=challenges-20260910','site.css?v=advice-20261109').replace('site.js?v=20261027-1','site.js?v=20261109-advice')
 p.write_text(doc)
print('Installed contextual admissions advice routes.')

#!/usr/bin/env python3
"""Build the interview hub and its Cambridge, Oxford and Engineering guides.

No deployment or shared-site mutation is performed. College facts and source links
are maintained in data/interview-colleges.json. Recheck the stated admissions cycle
before updating the checked date.
"""
from pathlib import Path
from html import escape as esc
import argparse
import json
import re
from site_navigation import archive_navigation, reorder_main_navigation

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://maths.arijasad.com/'
CHECKED = '18 November 2026'
CTA = 'Enquire now'
CAM_CONTACT = 'contact.html?service=Cambridge%20mathematics%20interview%20preparation#enquiry-form'
OX_CONTACT = 'contact.html?service=Other%20mathematics%20support#enquiry-form'
CENTRAL = 'https://www.undergraduate.study.cam.ac.uk/apply/after/cambridge-interviews'
OX = 'https://www.ox.ac.uk/admissions/undergraduate/applying/guide-for-applicants/interviews'
OX_MATHS = 'https://www.maths.ox.ac.uk/study-here/undergraduate-study/interviews'
OX_TMUA = 'https://www.maths.ox.ac.uk/study-here/undergraduate-study/tmua'
OX_CLUB = 'https://www.maths.ox.ac.uk/outreach/oxford-online-maths-club'
OX_LIVE = 'https://www.maths.ox.ac.uk/study-here/undergraduate-study/tmua/mat-livestream'
CAM_ENG = 'https://www.admissions.eng.cam.ac.uk/guide/procedure'
CAM_ENG_VIDEO = 'https://www.admissions.eng.cam.ac.uk/open-days/open-day-video'
OX_ENG = 'https://eng.ox.ac.uk/study/undergraduate/common-questions'
OX_ENG_PDF = 'https://eng.ox.ac.uk/media/4095/typical_engineering_interview_questions-accessible.pdf'
SITE_TEMPLATE = (ROOT / 'cambridge-maths-interview-guide.html').read_text()
SITE_HEADER = re.search(r'<header class="site-header">.*?</header>', SITE_TEMPLATE, re.S)[0]
SITE_HEADER = SITE_HEADER.replace(' aria-current="page"', '').replace(
    '<a href="interviews.html">', '<a href="interviews.html" aria-current="page">')
SITE_FOOTER = re.search(r'<footer>.*?</footer>', SITE_TEMPLATE, re.S)[0]

def link(url, text, cls=''):
    extra = ' target="_blank" rel="noopener"' if url.startswith('https://') else ''
    return f'<a href="{esc(url, quote=True)}"{extra}' + (f' class="{cls}"' if cls else '') + f'>{text}</a>'

def header(path='interviews.html'):
    return ('<a class="skip-link" href="#main-content">Skip to main content</a>'
            + reorder_main_navigation(SITE_HEADER, path) + archive_navigation(path))

def footer():
    return SITE_FOOTER

def support(oxford=False):
    return f'''<section class="resource-section interview-section" id="contact"><div class="container"><div class="resource-cta"><div><h2>Practise with focused feedback.</h2><p>I offer standalone mock interviews and combined pre-interview test and interview packages. The length and format are tailored to your needs.</p></div>{link(OX_CONTACT if oxford else CAM_CONTACT, CTA, 'resource-button')}</div></div></section>'''

def resource(url, title, description, _author):
    return f'<li>{link(url,title)}<p>{description}</p></li>'

def general_resources():
    return '<ul class="resource-list">' + ''.join([
        resource('https://step.maths.org/interview-preparation/overview', 'Cambridge interview preparation', 'Start with the advice, practice questions and demonstration interviews. Use the commentary to think about how a discussion develops.', 'University of Cambridge, STEP Support Programme.'),
        resource('https://www.drfrost.org/downloadables.php?rid=261', 'Mr Bowler’s problem-solving booklet', 'A substantial collection of university interview-style problems. Choose a small set, attempt them independently, then discuss the reasoning.', 'Tom Bowler; hosted by Dr Frost Learning.'),
        resource('https://step.maths.org/', 'STEP Support Programme', 'Foundation assignments help build the algebra, reasoning and persistence needed for longer problems. Select assignments around a specific weakness.', 'University of Cambridge, STEP Support Programme.'),
        resource('https://www.openbookpublishers.com/books/10.11647/obp.0181', 'Advanced Problems in Mathematics', 'Free book with challenging STEP-based problems, commentary and solutions. Its older examination references are historical.', 'Stephen Siklos. Second edition, Open Book Publishers, 2019.'),
        resource(OX_CLUB, 'Oxford Online Maths Club', 'Recorded mathematical discussions and worksheets. Pause before a solution and work through the problem yourself.', 'University of Oxford Mathematical Institute; regular host Dr James Munro and contributors.'),
        resource('https://openclimb.io/csat/#papers', 'CSAT sample papers', 'Optional mathematical and computing problems for extra practice. CSAT is not a Cambridge Mathematics admissions requirement.', 'Climb Foundation, founded by Dr Bogdan A. Roman, with its question-setting team.'),
        resource('https://bmos.ukmt.org.uk/home/bmo', 'BMO past problems', 'Optional proof-based extension. Begin with accessible BMO1 questions and practise writing a complete argument.', 'UK Mathematics Trust and its British Mathematical Olympiad committees.'),
        resource('https://www.maths.ox.ac.uk/study-here/undergraduate-study/maths-admissions-test', 'Historical MAT papers', 'Older long questions can support interview problem solving. MAT is no longer the Oxford admissions test for the 2027-entry round.', 'University of Oxford Mathematical Institute.')
    ]) + '</ul>'

def hub():
    return f'''<main id="main-content">
<section class="resource-hero"><div class="container"><div class="resource-hero__inner"><p class="eyebrow">Cambridge &amp; Oxford Mathematics</p><h1>Maths <span>interview preparation.</span></h1><p class="resource-lede">Build confidence with unfamiliar problems, explain your ideas clearly and learn how to use a hint. Find tuition options together below, followed by free interview advice and resources.</p><div class="hero-foot"><nav class="jump-links" aria-label="On this page"><a href="#session">Tuition ↓</a><a href="#advice">Advice &amp; resources ↓</a></nav></div></div></div></section>
<section class="resource-section resource-section--dark interview-section" id="session"><div class="container"><div id="tuition" class="eyebrow">Tuition</div><h2>Choose the support you need.</h2><p class="section-lead">Book a mock interview or a test and interview package. We agree the length and format around your college, stage of preparation and goals.</p><div class="tuition-options">
<article class="resource-card interview-offer"><h3>Mock interviews</h3><p>Work through unfamiliar questions in a realistic mathematical discussion. We review your reasoning, communication and response to guidance, with clear priorities for your next practice.</p></article>
<article class="resource-card interview-offer"><h3>Test &amp; interview packages</h3><p>Combine a practice pre-interview paper with an interview based on your work and focused feedback. Useful for preparing for colleges that use written questions before the discussion.</p></article>
</div><p class="service-note">Sessions are discussion-based: try an idea, explain why it might work, respond to a question and adapt. Feedback turns that experience into specific next steps.</p><div class="button-row">{link(CAM_CONTACT, CTA, 'resource-button')}<a class="text-link" href="about.html">More about my teaching ↗</a></div></div></section>
<section class="resource-section resource-section--white interview-section" id="advice"><div class="container"><div class="eyebrow">Advice &amp; resources</div><h2>Understand the process.<br>Then practise the mathematics.</h2><p class="section-lead">Start with the guide for your university. Use the free material to practise reasoning aloud, working with hints and explaining a complete argument.</p><div class="resource-grid interview-guides">
<a class="resource-card guide-link" href="cambridge-college-maths-interviews.html"><h3>Cambridge, college by college</h3><p>All 29 undergraduate colleges, with Trinity first. Published formats, preparation tasks and official specimen links.</p></a>
<a class="resource-card guide-link" href="oxford-maths-interview-guide.html"><h3>Oxford maths interviews</h3><p>The college interview process, online setup, sample questions and official preparation resources.</p></a>
<a class="resource-card guide-link" href="engineering-interview-guide.html"><h3>Engineering interviews</h3><p>Cambridge and Oxford together: what to expect, how to explain your reasoning and useful maths and physics practice.</p></a>
<a class="resource-card guide-link" href="cambridge-maths-interview-guide.html"><h3>How to approach an interview</h3><p>Practical advice on reasoning, communication and responding when a question is unfamiliar.</p></a>
<a class="resource-card guide-link" href="cambridge-interview-problems.html"><h3>Five problems to discuss</h3><p>Try a focused set of interview-style problems, with hints and commentary to support reflection.</p></a>
</div><div class="reading-group"><details id="preparation"><summary>A manageable preparation routine</summary><div class="details-body"><ol class="numbered"><li>Choose a few unfamiliar problems rather than trying to finish every collection.</li><li>Make a sustained attempt before opening a hint. Explain a useful example, diagram or possible approach aloud.</li><li>Listen carefully to guidance, then try to develop the next step yourself.</li><li>Afterwards, identify the idea you missed and return to a related problem. Include graph sketching and arguments built from simple cases.</li></ol><p>Practice with a teacher, friend or study partner can be valuable.</p></div></details>
<details id="resources"><summary>Problem-solving resources</summary><div class="details-body">{general_resources()}</div></details>
<details id="assessed"><summary>What makes a useful practice discussion?</summary><div class="details-body"><p>Explain the mathematical decision that matters: what you notice, why an approach seems promising and where the uncertainty lies. Give yourself time to think, and treat a hint as information you can use.</p><p>In my sessions, we look closely at where progress stopped and choose follow-up problems that develop that particular skill.</p></div></details></div></div></section>
<section class="resource-section interview-section" id="faq"><div class="container narrow"><p class="eyebrow">Practical questions</p><h2>Before you book.</h2><div class="faq"><details><summary>Can I book just one mock interview?</summary><div class="details-body"><p>Yes. You can book a standalone mock interview or a combined test and interview package. We agree an appropriate format together.</p></div></details><details><summary>Are sessions a fixed length?</summary><div class="details-body"><p>No. The balance of practice, discussion and feedback is tailored to your needs. Tell me your college and any published interview arrangements when you enquire.</p></div></details><details><summary>Do I need paid tuition?</summary><div class="details-body"><p>No. Free university resources and discussion with a teacher or study partner can support effective preparation. Tuition is an optional way to get individual practice and feedback.</p></div></details></div></div></section></main>'''

def college_rows(colleges):
    rows=[]
    labels={'online':'Online','person':'In person','varies':'Depends on location'}
    for i,c in enumerate(colleges):
        if c.get('compact'):
            continue
        evidence=''.join(link(s['url'], esc(s['title'])) for s in c['sources'])
        paperlinks=''.join(link(p['url'],esc(p['title']),'paper-link') for p in c['papers'])
        rows.append(f'''<tr{' class="trinity" id="trinity"' if i==0 else ''} data-college-entry data-college="{esc(c['name'],quote=True)}" data-format="{c['category']}" data-papers="{str(bool(c['papers'])).lower()}"><th scope="row"><span class="college-name">{esc(c['name'])}</span><span class="format-tag">{labels[c['category']]}</span><span class="format-note">{esc(c['delivery'])}</span></th><td data-label="Interview &amp; preparation"><p>{esc(c['structure'])}</p></td><td data-label="Papers &amp; official sources"><div class="source-links">{paperlinks}{evidence}</div></td></tr>''')
    return '\n'.join(rows)

def compact_colleges(colleges):
    labels = {'online': 'Online', 'person': 'In person', 'varies': 'Depends on location'}
    cards = []
    for c in colleges:
        if not c.get('compact'):
            continue
        # Link current applicant instructions when available, including location rules.
        source = c['sources'][-1]['url']
        cards.append(f'''<li class="compact-college" data-college-entry data-college="{esc(c['name'],quote=True)}" data-format="{c['category']}" data-papers="false">{link(source, esc(c['name']), 'compact-college-name')}<span class="format-tag">{labels[c['category']]}</span></li>''')
    return f'''<section class="compact-colleges" id="compact-colleges" aria-labelledby="compact-heading"><h3 id="compact-heading">Other colleges</h3><p>These colleges publish less maths-specific interview detail. Select a college for its guidance; your invitation confirms timings, tasks and location arrangements.</p><ul class="compact-college-grid">{''.join(cards)}</ul></section>'''

def cambridge(colleges):
    return f'''<main id="main-content"><section class="article-hero"><div class="container"><p class="breadcrumbs"><a href="interviews.html#advice">Interviews</a> / Cambridge college guide</p><p class="eyebrow">2027 entry · December 2026 interviews</p><h1>Cambridge maths interviews,<br><span>college by college.</span></h1><p class="resource-lede">Find your college’s published interview format, any preparation task and official practice papers. Trinity appears first. Colleges with less published detail are grouped below the table.</p><p class="article-meta">By Arij Asad · Official guidance checked {CHECKED} · 29 colleges</p><div class="hero-foot"><nav class="jump-links" aria-label="On this page"><a href="#colleges">Find a college ↓</a><a href="#contact">Mock interviews ↓</a></nav></div></div></section>
<section class="resource-section interview-section" id="colleges"><div class="container"><h2>Find your college.</h2><div class="note"><p>Your interview invitation will tell you exactly what to expect.</p></div>
<div class="tools" id="college-tools" hidden><label class="field search" for="college-search">College name<input type="search" id="college-search" placeholder="e.g. Trinity or St John’s" autocomplete="off"></label><label class="field" for="college-format">Interview delivery<select id="college-format"><option value="">All formats</option><option value="online">Online for all</option><option value="person">In person</option><option value="varies">Depends on location</option></select></label><label class="filter-check"><input type="checkbox" id="papers-only">With linked practice papers</label><button class="reset" id="reset-colleges" type="button">Reset</button></div><noscript><p>All 29 colleges are listed below. Your browser’s Find command can locate a college.</p></noscript><p class="table-count" id="college-count" role="status" aria-live="polite" aria-atomic="true">29 of 29 colleges shown</p><p class="no-results" id="no-colleges" hidden>No colleges match these filters. Change the name or select Reset.</p>
<table class="college-table" data-college-table><caption class="sr-only">Cambridge undergraduate Mathematics interview arrangements for 2027 entry, checked 18 November 2026</caption><colgroup><col><col><col></colgroup><thead><tr><th scope="col">College &amp; delivery</th><th scope="col">Maths interview &amp; preparation</th><th scope="col">Papers &amp; official sources</th></tr></thead><tbody>{college_rows(colleges)}</tbody></table>
{compact_colleges(colleges)}
<p class="credit-note">This guide covers Cambridge’s 29 undergraduate colleges. You can find more detail through the college links above or {link(CENTRAL,'Cambridge’s interview guidance')}. If you’re unsure about where your interview will take place, ask your college.</p></div></section>
<section class="resource-section interview-section"><div class="container narrow"><h2>How to use this guide.</h2><div class="reading-group"><details><summary>What if two official pages disagree?</summary><div class="details-body"><p>Follow the instructions in your interview invitation. If anything is still unclear, contact the college’s admissions team.</p></div></details><details><summary>How should I prepare for an online interview?</summary><div class="details-body"><p>Read your college’s platform and equipment instructions. Practise writing mathematics, sharing a diagram and explaining your work using the same setup. Ask the college early if you cannot access the required equipment.</p><p><a href="interviews.html#advice">Read the advice and free resource suggestions →</a></p></div></details></div></div></section>{support()}</main>'''

def oxford():
    return f'''<main id="main-content"><section class="article-hero"><div class="container"><p class="breadcrumbs"><a href="interviews.html#advice">Interviews</a> / Oxford maths guide</p><p class="eyebrow">2027 entry · December 2026 interviews</p><h1>Oxford maths interviews.<br><span>What to expect, how to prepare.</span></h1><p class="resource-lede">A guide to the college interview process, the online setup and useful problems to practise. Start with Oxford’s official examples, then build confidence explaining your own reasoning.</p><p class="article-meta">By Arij Asad · Official guidance checked {CHECKED}</p><div class="hero-foot"><nav class="jump-links" aria-label="On this page"><a href="#process">The process ↓</a><a href="#oxford-resources">Free resources ↓</a><a href="#contact">Mock interviews ↓</a></nav></div></div></section>
<section class="resource-section resource-section--white interview-section" id="process"><div class="container"><p class="eyebrow">The college interview process</p><h2>Expect more than one conversation.</h2><div class="step-grid"><article class="step"><span class="num">01 / Invitation</span><h3>Your first college</h3><p>Shortlisted applicants receive online interview invitations. The first interviewing college can differ from your original choice, including after reallocation or an open application.</p>{link(OX,'Oxford’s interview guidance','source-inline')}</article><article class="step"><span class="num">02 / Mathematical discussion</span><h3>About 25 minutes</h3><p>The Maths department describes generally one or two interviews at the first college, each about 25 minutes. Expect unfamiliar problems, graphs or a new definition to explore.</p>{link(OX_MATHS,'Mathematical Institute guidance','source-inline')}</article><article class="step"><span class="num">03 / Another college</span><h3>A normal part of the process</h3><p>The department describes at least one interview at another college. Exact arrangements vary, so use each invitation to confirm the time, format and any preparation.</p>{link(OX_MATHS,'College interview structure','source-inline')}</article></div><div class="note"><p>Most Maths interviews are scheduled for 14 to 17 December 2026; some colleges start in the week beginning 7 December. Your invitation takes priority. {link(OX+'/interview-timetables','Check Oxford’s 2026 timetable')}.</p></div></div></section>
<section class="resource-section resource-section--dark interview-section" id="oxford-advice"><div class="container paired"><div><h2>Make your thinking visible.</h2><p>Try an example, explain a possible approach and say where you are unsure. The discussion gives tutors a way to see how you reason and develop an idea.</p><p>If you receive a hint, pause to understand what it changes. A useful practice session includes time to reflect on why one approach worked and another stalled.</p><p class="small muted">For Mathematics and Computer Science or Mathematics and Philosophy, expect discussion covering both subjects. {link('https://www.maths.ox.ac.uk/study-here/undergraduate-study/prospectus','Read the department prospectus')}.</p></div><div><h2>Check your online setup.</h2><p>Mathematics is listed under Oxford’s tier 3 setup: Microsoft Teams, a Miro whiteboard and a touchscreen with a stylus for handwriting.</p><p>Test writing equations and drawing diagrams in advance. If suitable equipment is unavailable, contact the college; Oxford says applicants and schools are not expected to buy a touchscreen device.</p><p>{link(OX+'/technology','Official technology instructions →')}</p><p class="small muted">Your invitation explains any variation, including a different setup for part of a joint-course interview.</p></div></div></section>
<section class="resource-section interview-section" id="oxford-resources"><div class="container"><p class="eyebrow">Official examples &amp; practice</p><h2>Free resources worth spending time on.</h2><p class="section-lead">Choose a few problems and give them a proper attempt. A demonstration is useful for understanding the discussion, rather than as a performance to memorise.</p><ul class="resource-list">
{resource(OX+'/sample_questions','Oxford sample interview questions','Open the Mathematics section for examples and explanations from tutors. These are practice examples, not advance questions for your interview.','University of Oxford; individual tutors credited on the source page.')}
{resource(OX+'/demonstration_videos','Mathematics demonstration interview','Choose Mathematics (tier 3). Watch the discussion and tutor commentary; a transcript is also available.','University of Oxford and the participating tutors and student.')}
{resource(OX_CLUB,'Oxford Online Maths Club','Recorded problem-solving discussions. Pause at a question, try an approach, then compare it with the discussion.','University of Oxford Mathematical Institute; Dr James Munro and contributors.')}
{resource(OX_LIVE,'Maths livestreams &amp; worksheets','Choose the interview sessions and worksheets to practise discussing a problem and explaining your ideas.','University of Oxford Mathematical Institute.')}
{resource('https://www.maths.ox.ac.uk/system/files/inline-files/26-24-versatility_0.pdf','Versatility worksheet (PDF)','A problem-solving worksheet including a past Oxford interview question. Try it independently, then talk through your reasoning.','University of Oxford Mathematical Institute; sources are identified within the worksheet.')}
{resource('https://www.maths.ox.ac.uk/study-here/undergraduate-study/tmua/mat-livestream/versatility-solutions','Versatility worksheet solutions','Use after an independent attempt, then try to reconstruct the reasoning without the solution in front of you.','University of Oxford Mathematical Institute.')}
</ul><p class="credit-note">Find more problems in the <a href="interviews.html#resources">shared preparation resources</a>.</p></div></section>
<section class="resource-section resource-section--white interview-section" id="oxford-questions"><div class="container narrow"><h2>A few practical questions.</h2><div class="reading-group"><details><summary>Is there a pre-interview maths paper?</summary><div class="details-body"><p>The current central maths guidance reviewed does not specify a single timed preparation paper for all applicants. Follow your college’s invitation for any task or material. A missing public description does not establish that there is no task.</p><p>{link(OX+'/FAQs','Oxford interview FAQs')}</p></div></details><details><summary>Do I need specialist interview training?</summary><div class="details-body"><p>Oxford says special admissions training is not required. Working on mathematics and discussing it with a teacher or study partner are useful ways to prepare. Individual tuition is optional.</p><p>{link(OX_MATHS,'Oxford’s preparation advice')}</p></div></details></div><p class="credit-note">This independent guide summarises public guidance, not private interview questions. Exact arrangements are set by the colleges. <a href="cambridge-college-maths-interviews.html">Looking for Cambridge instead? →</a></p></div></section>{support(True)}</main>'''

def engineering():
    return f'''<main id="main-content">
<section class="article-hero"><div class="container"><p class="breadcrumbs"><a href="interviews.html#advice">Interviews</a> / Engineering</p><p class="eyebrow">Cambridge &amp; Oxford · 2027 entry</p><h1>Engineering interviews.</h1><p class="resource-lede">What to expect at Cambridge and Oxford, how to practise, and a few good places to find problems.</p><p class="article-meta">By Arij Asad · Updated {CHECKED}</p><nav class="jump-links" aria-label="On this page"><a href="#engineering-process">What to expect ↓</a><a href="#engineering-advice">Preparation advice ↓</a><a href="#engineering-resources">Practice resources ↓</a></nav></div></section>
<section class="resource-section interview-section" id="engineering-process"><div class="container"><h2>What happens in the interview?</h2><p class="section-lead">Expect a discussion involving maths and physics. Tutors want to see how you work through a problem and develop an idea when they give you some guidance.</p>
<table class="college-table engineering-comparison"><caption class="sr-only">Cambridge and Oxford Engineering interview arrangements</caption><colgroup><col><col></colgroup><thead><tr><th scope="col">University</th><th scope="col">Interview arrangements</th></tr></thead><tbody>
<tr><th scope="row"><span class="college-name">Cambridge</span><span class="format-tag">Varies by college</span></th><td data-label="Interview arrangements"><p>Your college sets the number and length of interviews. They may be online or in person, depending on your college and location. Check your invitation for any tasks to prepare.</p><div class="engineering-source-links">{link(CENTRAL,'Cambridge interview guidance')} · {link(CAM_ENG,'Engineering admissions guidance')}</div></td></tr>
<tr><th scope="row"><span class="college-name">Oxford</span><span class="format-tag">Online</span></th><td data-label="Interview arrangements"><p>The department describes two interviews at different colleges: about 30 to 45 minutes for the first and around 30 minutes for the second. Your invitation gives the exact arrangements.</p><div class="engineering-source-links">{link(OX_ENG,'Engineering interview guide')} · {link('https://eng.ox.ac.uk/study/undergraduate/applications','Online interview arrangements')}</div></td></tr>
</tbody></table></div></section>
<section class="resource-section resource-section--white interview-section" id="engineering-advice"><div class="container narrow"><p class="eyebrow">My preparation advice</p><h2>Make your reasoning easy to follow.</h2><ol class="numbered engineering-advice">
<li><strong>Draw the situation.</strong> Label the quantities, forces or circuit components. A clear diagram often reveals the first useful step.</li>
<li><strong>Explain your model.</strong> Say which physical principle you are using and what you are assuming. For example, are you ignoring friction or treating a body as a particle?</li>
<li><strong>Check what the answer means.</strong> Look at the units, sign and size. Consider an extreme case, or ask what would happen if a mass, length or voltage doubled.</li>
<li><strong>Use a hint.</strong> If you get stuck, explain where. Listen to the suggestion, try it, and say what it changes in your approach.</li>
<li><strong>Know your own examples.</strong> Revisit projects, reading and interests from your application. Be ready to explain the engineering involved and what you learned.</li>
</ol><p>For practice, choose an unfamiliar problem and talk it through with someone who can ask follow-up questions. Afterwards, identify the step that caused difficulty and try a related problem.</p>
<div class="reading-group"><details><summary>What should I revise?</summary><div class="details-body"><p>Start with the maths and physics you have already studied. Useful areas to revisit include algebra, graphs, calculus, forces, moments, energy and circuits. Practise connecting equations to a physical situation.</p></div></details><details><summary>What do I need for an online interview?</summary><div class="details-body"><p>Oxford lists Engineering under its tier 3 setup: Microsoft Teams, a Miro whiteboard and a touchscreen with a stylus. Practise writing equations and drawing diagrams. Contact the college if suitable equipment is unavailable.</p><p>For Cambridge, follow your college’s instructions about how to share your working.</p><p>{link(OX+'/technology','Oxford technology guidance')} · {link('https://www.undergraduate.study.cam.ac.uk/apply/after/interview-preparation','Cambridge preparation guidance')}</p></div></details></div></div></section>
<section class="resource-section interview-section" id="engineering-resources"><div class="container narrow"><p class="eyebrow">Practice resources</p><h2>A few useful starting points.</h2><ul class="resource-list">
<li>{link(OX+'/sample_questions','Oxford’s sample questions')}<p>Open the Engineering section for questions and tutor commentary. The department’s {link(OX_ENG_PDF,'engineering example (PDF)')} explores forces and the stability of a dam.</p></li>
<li>{link(CAM_ENG_VIDEO,'Cambridge demonstration interview')} · {link('https://www.youtube.com/watch?v=Jy7Uqa1yql0','Oxford demonstration interview')}<p>Watch how the student and tutors develop the discussion. Pause when a problem is introduced and think about what you would try.</p></li>
{resource('https://i-want-to-study-engineering.org/','I Want to Study Engineering','Maths, physics and engineering problems with hints. Try a problem independently before using the help.','University of Cambridge Department of Engineering and the project team.')}
{resource('https://isaacscience.org/physics','Isaac Science Physics','Use targeted physics problems to strengthen an area you find difficult, then practise explaining the reasoning aloud.','Isaac Science team.')}
</ul><p class="small muted">For admissions-test practice and wider application advice: <a href="esat-paper-archive.html">ESAT papers</a> · <a href="cambridge-engineering-application-guide.html">Cambridge Engineering</a> · <a href="oxford-engineering-application-guide.html">Oxford Engineering Science</a>.</p></div></section>
<section class="resource-section interview-section" id="contact"><div class="container"><div class="resource-cta"><div><h2>Practise the mathematical side.</h2><p>For a mock interview focused on mathematical problem solving, get in touch. We can work on where you get stuck, how you use hints and how clearly you explain an idea.</p></div>{link(OX_CONTACT,CTA,'resource-button')}</div></div></section>
</main>'''

PAGES = {
    'interviews.html': ('Cambridge & Oxford Maths Interview Tutor | Arij Asad', 'Cambridge and Oxford maths interview tuition, mock interviews and pre-interview test packages, with free advice and preparation resources.'),
    'cambridge-college-maths-interviews.html': ('Cambridge Maths Interviews by College: Formats & Specimen Papers | Arij Asad', 'Compare published maths interview formats at all 29 Cambridge undergraduate colleges for 2027 entry. Trinity first, with official specimen papers and source links.'),
    'oxford-maths-interview-guide.html': ('Oxford Maths Interviews: Process, Questions & Preparation | Arij Asad', 'Oxford Mathematics interview guide for 2027 entry: college interviews, online technology, official sample questions, videos and free preparation resources.'),
    'engineering-interview-guide.html': ('Cambridge & Oxford Engineering Interviews: Advice & Practice | Arij Asad', 'A concise Cambridge and Oxford Engineering interview guide: what to expect, maths and physics preparation, official sample questions and demonstration interviews.')
}

def theme_css():
    return '\n'.join((ROOT / path).read_text() for path in
                     ['site.css', 'paper-navigation.css', 'assets/interview-pages.css'])

def document(path, body, preview=False):
    title, desc = PAGES[path]
    page_class = ' oxford-interviews' if path == 'oxford-maths-interview-guide.html' else ''
    styles = f'<style>{theme_css()}</style>' if preview else '<link rel="stylesheet" href="site.css?v=advice-20261109"><link rel="stylesheet" href="/paper-navigation.css?v=20261118-both"><link rel="stylesheet" href="assets/interview-pages.css?v=20261118-oxford-layout">'
    schema = {'@context':'https://schema.org','@type':'WebPage' if path=='interviews.html' else 'Article', 'headline':title.split(' | ')[0], 'description':desc,'url':BASE+path, 'author':{'@type':'Person','name':'Arij Asad','url':BASE+'about.html'}}
    if path != 'interviews.html':
        schema['dateModified']='2026-11-18'
    tags = '<meta name="robots" content="noindex,nofollow">' if preview else f'<link rel="icon" href="/favicon.ico?v=dd9f0d4a0c"><link rel="canonical" href="{BASE+path}"><meta property="og:type" content="{ "website" if path=="interviews.html" else "article" }"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{BASE+path}"><meta property="og:image" content="{BASE}assets/small-group-teaching.webp"><meta name="twitter:card" content="summary_large_image"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script>'
    scripts = '<script>'+ (ROOT/'assets/interview-pages.js').read_text()+'</script>' if preview else '<script src="site.js?v=20261109-advice" defer></script><script src="assets/interview-pages.js?v=20261118" defer></script>'
    if preview:
        body=header(path)+body+footer()
        body=re.sub(r'href="(?!https:|#|mailto:)([^"]*)"', lambda m: 'href="'+BASE+m[1].lstrip('/')+'"', body)
        # Reuse the site's menu behaviour, without loading analytics in a preview.
        menu_script = (ROOT/'site.js').read_text().split('const copyButton', 1)[0]
        scripts += '<script>' + menu_script + "document.querySelectorAll('[data-cookie-settings]').forEach(button=>button.addEventListener('click',()=>alert('Analytics are disabled in this preview.')));" + '</script>'
        scripts += '''<script>document.addEventListener('click',function(event){const a=event.target.closest('a');if(!a)return;const u=new URL(a.href);if(u.origin==='https://maths.arijasad.com' && ['interviews.html','cambridge-college-maths-interviews.html','oxford-maths-interview-guide.html','engineering-interview-guide.html'].includes(u.pathname.slice(1))){event.preventDefault();parent.postMessage({type:'interview-preview',page:u.pathname.slice(1),hash:u.hash},'*');}});document.querySelectorAll('a[href^="https://"]').forEach(a=>{a.target='_blank';a.rel='noopener';});window.addEventListener('message',e=>{if(e.source!==parent||e.data?.type!=='interview-preview-anchor')return;let id;try{id=decodeURIComponent(e.data.hash.slice(1));}catch(_){return;}const target=document.getElementById(id);if(target){if(target.tagName==='DETAILS')target.open=true;target.scrollIntoView();}});</script>'''
    else:
        body=header(path)+body+footer()
    return f'<!doctype html>\n<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#111111"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}">{tags}{styles}</head><body class="resource-page interview-pages{page_class}">{body}{scripts}</body></html>\n'

def build(preview_path=None):
    colleges=json.loads((ROOT/'data/interview-colleges.json').read_text())['colleges']
    assert len(colleges)==29 and colleges[0]['name']=='Trinity'
    bodies={'interviews.html':hub(),'cambridge-college-maths-interviews.html':cambridge(colleges),'oxford-maths-interview-guide.html':oxford(),'engineering-interview-guide.html':engineering()}
    for path,body in bodies.items():
        (ROOT/path).write_text(document(path,body),encoding='utf-8')
    if preview_path:
        docs={p:document(p,b,True) for p,b in bodies.items()}
        payload=json.dumps(docs,ensure_ascii=False).replace('<','\\u003c')
        tabs=''.join(f'<button type="button" data-page="{p}" aria-pressed="{str(i==0).lower()}">{label}</button>' for i,(p,label) in enumerate(zip(PAGES,['Interviews','Cambridge colleges','Oxford guide','Engineering guide'])))
        preview_script='''const pages=PAYLOAD;const frame=document.getElementById('page-preview');let active='interviews.html';function showPage(page,hash=''){if(!Object.hasOwn(pages,page))return;active=page;frame.onload=()=>{if(hash)frame.contentWindow.postMessage({type:'interview-preview-anchor',hash},'*');};frame.srcdoc=pages[page];document.querySelectorAll('[data-page]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.page===page)));document.getElementById('preview-status').textContent=page==='interviews.html'?'Existing Interviews page, reorganised':page.startsWith('cambridge')?'New Cambridge college guide':page.startsWith('engineering')?'New Engineering interview guide':'New Oxford interview guide';}document.querySelectorAll('[data-page]').forEach(b=>b.addEventListener('click',()=>showPage(b.dataset.page)));window.addEventListener('message',e=>{if(e.source===frame.contentWindow&&e.data?.type==='interview-preview')showPage(e.data.page,e.data.hash);});'''.replace('PAYLOAD',payload)
        result=f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Arij Asad Maths | Interview pages preview</title><style>{theme_css()}</style></head><body class="interview-preview"><div class="preview-bar"><p>Review draft · Not published<br><span id="preview-status" role="status">Existing Interviews page, reorganised</span></p><nav class="preview-tabs" aria-label="Preview pages">{tabs}</nav></div><noscript><p>Enable JavaScript to switch between the preview pages.</p></noscript><iframe id="page-preview" class="preview-frame" title="Website page preview" srcdoc="{esc(docs['interviews.html'],quote=True)}"></iframe><script>{preview_script}</script></body></html>'''
        Path(preview_path).parent.mkdir(parents=True,exist_ok=True)
        Path(preview_path).write_text(result,encoding='utf-8')
        print(f'Preview: {preview_path}')
    print('Built Interviews, Cambridge colleges, Oxford and Engineering guides. No publication performed.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', help='Optional standalone HTML preview output path')
    build(parser.parse_args().preview)

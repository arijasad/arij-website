#!/usr/bin/env python3
"""Package existing original worksheets without changing their contents."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'assets/teacher-resources'
DEST.mkdir(exist_ok=True)
README = '''Arij Asad Maths: questions, hints and worked solutions
https://maths.arijasad.com/teacher-resources.html

Start with a question and give the student time to explain their approach.
Use a hint when you can see which step is causing difficulty. After working
through the idea, try a related question without the hint.

CONTENTS
1. logic/: separate questions and questions-with-solutions, in PDF and TeX.
2. algebra/: diagnostic questions, teacher solutions and follow-up practice,
   in PDF and TeX. The follow-up sheet includes its own solution material.
3. textbook-practice/: six original practice sheets, each with hints and
   worked solutions after the questions, in PDF and TeX.

Choose the question-only logic and algebra PDFs when sending a task to a
student. The textbook practice PDFs include solutions: print only the question
pages if you want to keep the later pages for discussion.

The TeX files can be uploaded to Overleaf or used to select problems for a
lesson. Keep the question and its solution together in your teaching notes.
You may copy and adapt this original material for lessons and share it with
your students. Please retain the Arij Asad Maths credit and source link.

This pack contains Arij Asad's teaching material. Official exam papers and
third-party SolutionBank files are linked separately on the website and are
not included. No student names or individual feedback are included.
'''
def add(z,name,data):
    # A fixed timestamp makes rebuilding an unchanged pack reproducible.
    from zipfile import ZipInfo
    info=ZipInfo(name,(2026,10,27,0,0,0));info.compress_type=ZIP_DEFLATED
    z.writestr(info,data)
with ZipFile(DEST/'Arij_Asad_Teaching_Resources.zip','w',ZIP_DEFLATED) as z:
    add(z,'START_HERE.txt',README.encode())
    with ZipFile(ROOT/'assets/negation-contrapositive/Negation_and_Contrapositive_Resource.zip') as source:
        for name in source.namelist():
            if name.endswith(('.tex','.pdf')):
                add(z,'logic/'+Path(name).name,source.read(name))
    for folder,label in [('algebra-diagnostic','algebra'),('textbook-practice','textbook-practice')]:
        for file in sorted((ROOT/'assets'/folder).iterdir()):
            if file.suffix in ('.tex','.pdf'):
                add(z,label+'/'+file.name,file.read_bytes())
print(DEST/'Arij_Asad_Teaching_Resources.zip')

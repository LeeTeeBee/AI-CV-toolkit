#!/usr/bin/env python3
"""
CV DOCX Builder
===============
Builds a formatted .docx CV from the CV template.

HOW THIS WORKS
--------------
You do not need to edit this script manually. It is populated and run
automatically by Claude as the final step of the CV drafting workflow.

When you approve a CV draft, Claude will:
1. Copy this script to its working directory
2. Fill in the CV CONTENT section below with the approved CV text
3. Run the script to produce the .docx file
4. Save the output to your CVs folder

SETUP (one-time)
----------------
1. Make sure CV template.docx is present in your job applications folder.
2. Make sure your memory.md contains the correct path to that folder.
3. That's it — Claude handles the rest.

REQUIREMENTS
------------
- CV template.docx must be present in the same folder as this script
- lxml must be installed (pip install lxml --break-system-packages)
- unpack.py and pack.py from the docx skill must be accessible

PATHS (bash sandbox — do not change)
--------------------------------------
"""

import os
import sys
import shutil
import subprocess
from lxml import etree
import copy

# ── Paths ──────────────────────────────────────────────────────────────────────
import glob as _glob

# Resolve session-specific paths dynamically — do not hard-code session name
_session_root = next(iter(_glob.glob('/sessions/*/mnt')), None)
if not _session_root:
    raise RuntimeError("Could not locate session mount root under /sessions/*/mnt")

# Claude sets FOLDER at runtime based on the path in memory.md
FOLDER         = f'{_session_root}/[FOLDER NAME SET BY CLAUDE]'
TEMPLATE       = f'{FOLDER}/CV template.docx'
SCRIPTS        = f'{_session_root}/.claude/skills/docx/scripts/office'
WORK_DIR       = '/tmp/cv_build_work'
UNPACKED_DIR   = f'{WORK_DIR}/unpacked'
TEMPLATE_COPY  = f'{WORK_DIR}/template_copy.docx'


# ==============================================================================
#  CV CONTENT — populated automatically by Claude, do not edit manually
#
#  When Claude runs this script it will replace the variables below with the
#  approved CV content. The structure is shown here for reference only.
#
#  OUTPUT_FILENAME = 'Company - Job Title.docx'
#  NAME    = 'Full name'
#  CONTACT = 'Location - Phone - Email'
#  PROFILE = 'One paragraph, max 90 words, tailored to the role'
#  ACHIEVEMENTS = ['Bullet 1', 'Bullet 2', ...]
#  ROLES = [('Job Title', 'Company', 'Date range', ['Bullet 1', 'Bullet 2', ...]), ...]
#  SKILLS = [('Category', 'skill, skill, skill'), ...]
#  CERTIFICATIONS = [('Cert name', 'Issuing body'), ...]
#  EDUCATION = [('Institution: Qualification', 'Date range'), ...]
# ==============================================================================

OUTPUT_FILENAME = ''
NAME    = ''
CONTACT = ''
PROFILE = ''
ACHIEVEMENTS = []
ROLES = []
SKILLS = []
CERTIFICATIONS = []
EDUCATION = []

# ==============================================================================
#  MACHINERY — do not edit below this line
# ==============================================================================

def W(tag):
    return '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}' + tag

COLOR_PROPS = {'val': '474747', 'themeColor': 'accent5', 'themeShade': 'BF'}

def set_color(el):
    col = etree.SubElement(el, W('color'))
    for k, v in COLOR_PROPS.items():
        col.set(W(k), v)
    return col

def add_title(body, text):
    p = etree.SubElement(body, W('p'))
    pPr = etree.SubElement(p, W('pPr'))
    etree.SubElement(pPr, W('pStyle')).set(W('val'), 'Title')
    etree.SubElement(pPr, W('spacing')).set(W('after'), '120')
    rPr_p = etree.SubElement(pPr, W('rPr'))
    set_color(rPr_p)
    etree.SubElement(rPr_p, W('sz')).set(W('val'), '40')
    etree.SubElement(rPr_p, W('szCs')).set(W('val'), '40')
    r = etree.SubElement(p, W('r'))
    rPr = etree.SubElement(r, W('rPr'))
    set_color(rPr)
    etree.SubElement(rPr, W('sz')).set(W('val'), '40')
    etree.SubElement(rPr, W('szCs')).set(W('val'), '40')
    t = etree.SubElement(r, W('t'))
    t.text = text

def add_contact(body, text):
    p = etree.SubElement(body, W('p'))
    pPr = etree.SubElement(p, W('pPr'))
    sp = etree.SubElement(pPr, W('spacing'))
    sp.set(W('line'), '360'); sp.set(W('lineRule'), 'auto')
    etree.SubElement(pPr, W('jc')).set(W('val'), 'both')
    rPr_p = etree.SubElement(pPr, W('rPr'))
    etree.SubElement(rPr_p, W('b')); etree.SubElement(rPr_p, W('bCs'))
    set_color(rPr_p)
    r = etree.SubElement(p, W('r'))
    rPr = etree.SubElement(r, W('rPr'))
    etree.SubElement(rPr, W('b')); etree.SubElement(rPr, W('bCs'))
    set_color(rPr)
    t = etree.SubElement(r, W('t'))
    t.text = text

def add_profile(body, text):
    p = etree.SubElement(body, W('p'))
    pPr = etree.SubElement(p, W('pPr'))
    sp = etree.SubElement(pPr, W('spacing'))
    sp.set(W('line'), '276'); sp.set(W('lineRule'), 'auto')
    etree.SubElement(pPr, W('jc')).set(W('val'), 'both')
    rPr_p = etree.SubElement(pPr, W('rPr'))
    etree.SubElement(rPr_p, W('bCs'))
    set_color(rPr_p)
    etree.SubElement(rPr_p, W('szCs')).set(W('val'), '20')
    r = etree.SubElement(p, W('r'))
    rPr = etree.SubElement(r, W('rPr'))
    etree.SubElement(rPr, W('bCs'))
    set_color(rPr)
    etree.SubElement(rPr, W('szCs')).set(W('val'), '20')
    t = etree.SubElement(r, W('t'))
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

def add_heading1(body, text):
    p = etree.SubElement(body, W('p'))
    pPr = etree.SubElement(p, W('pPr'))
    etree.SubElement(pPr, W('pStyle')).set(W('val'), 'Heading1')
    sp = etree.SubElement(pPr, W('spacing'))
    sp.set(W('before'), '200'); sp.set(W('after'), '60')
    set_color(etree.SubElement(pPr, W('rPr')))
    r = etree.SubElement(p, W('r'))
    set_color(etree.SubElement(r, W('rPr')))
    etree.SubElement(r, W('t')).text = text

def add_prof_exp_header(body, text):
    p = etree.SubElement(body, W('p'))
    pPr = etree.SubElement(p, W('pPr'))
    sp = etree.SubElement(pPr, W('spacing'))
    sp.set(W('before'), '200'); sp.set(W('after'), '60')
    rPr_p = etree.SubElement(pPr, W('rPr'))
    rf = etree.SubElement(rPr_p, W('rFonts'))
    rf.set(W('asciiTheme'), 'majorHAnsi'); rf.set(W('eastAsiaTheme'), 'majorEastAsia')
    rf.set(W('hAnsiTheme'), 'majorHAnsi'); rf.set(W('cs'), 'Times New Roman (Headings CS)')
    etree.SubElement(rPr_p, W('b'))
    set_color(rPr_p)
    etree.SubElement(rPr_p, W('spacing')).set(W('val'), '-10')
    etree.SubElement(rPr_p, W('sz')).set(W('val'), '24')
    etree.SubElement(rPr_p, W('szCs')).set(W('val'), '32')
    r = etree.SubElement(p, W('r'))
    rPr = etree.SubElement(r, W('rPr'))
    rf2 = etree.SubElement(rPr, W('rFonts'))
    rf2.set(W('asciiTheme'), 'majorHAnsi'); rf2.set(W('eastAsiaTheme'), 'majorEastAsia')
    rf2.set(W('hAnsiTheme'), 'majorHAnsi'); rf2.set(W('cs'), 'Times New Roman (Headings CS)')
    etree.SubElement(rPr, W('b'))
    set_color(rPr)
    etree.SubElement(rPr, W('spacing')).set(W('val'), '-10')
    etree.SubElement(rPr, W('sz')).set(W('val'), '24')
    etree.SubElement(rPr, W('szCs')).set(W('val'), '32')
    etree.SubElement(r, W('t')).text = text

def add_heading2(body, role, company, date_range):
    p = etree.SubElement(body, W('p'))
    pPr = etree.SubElement(p, W('pPr'))
    etree.SubElement(pPr, W('pStyle')).set(W('val'), 'Heading2')
    set_color(etree.SubElement(pPr, W('rPr')))
    r1 = etree.SubElement(p, W('r'))
    set_color(etree.SubElement(r1, W('rPr')))
    etree.SubElement(r1, W('t')).text = f'{role} - {company}'
    r_tab = etree.SubElement(p, W('r'))
    set_color(etree.SubElement(r_tab, W('rPr')))
    etree.SubElement(r_tab, W('tab'))
    r2 = etree.SubElement(p, W('r'))
    set_color(etree.SubElement(r2, W('rPr')))
    etree.SubElement(r2, W('t')).text = date_range

def add_bullet(body, text):
    p = etree.SubElement(body, W('p'))
    pPr = etree.SubElement(p, W('pPr'))
    etree.SubElement(pPr, W('pStyle')).set(W('val'), 'ListParagraph')
    numPr = etree.SubElement(pPr, W('numPr'))
    etree.SubElement(numPr, W('ilvl')).set(W('val'), '0')
    etree.SubElement(numPr, W('numId')).set(W('val'), '33')
    sp = etree.SubElement(pPr, W('spacing'))
    sp.set(W('line'), '276'); sp.set(W('lineRule'), 'auto')
    ind = etree.SubElement(pPr, W('ind'))
    ind.set(W('left'), '357'); ind.set(W('hanging'), '357')
    etree.SubElement(pPr, W('jc')).set(W('val'), 'both')
    rPr_p = etree.SubElement(pPr, W('rPr'))
    set_color(rPr_p)
    etree.SubElement(rPr_p, W('szCs')).set(W('val'), '20')
    r = etree.SubElement(p, W('r'))
    rPr = etree.SubElement(r, W('rPr'))
    set_color(rPr)
    etree.SubElement(rPr, W('szCs')).set(W('val'), '20')
    t = etree.SubElement(r, W('t'))
    t.text = text
    t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

def add_normal(body, text='', blank=False):
    p = etree.SubElement(body, W('p'))
    if not blank:
        pPr = etree.SubElement(p, W('pPr'))
        sp = etree.SubElement(pPr, W('spacing'))
        sp.set(W('line'), '276'); sp.set(W('lineRule'), 'auto')
        etree.SubElement(pPr, W('jc')).set(W('val'), 'both')
        rPr_p = etree.SubElement(pPr, W('rPr'))
        set_color(rPr_p)
        etree.SubElement(rPr_p, W('szCs')).set(W('val'), '20')
        r = etree.SubElement(p, W('r'))
        rPr = etree.SubElement(r, W('rPr'))
        set_color(rPr)
        etree.SubElement(rPr, W('szCs')).set(W('val'), '20')
        t = etree.SubElement(r, W('t'))
        t.text = text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

def add_skills_line(body, category, items):
    p = etree.SubElement(body, W('p'))
    pPr = etree.SubElement(p, W('pPr'))
    sp = etree.SubElement(pPr, W('spacing'))
    sp.set(W('line'), '276'); sp.set(W('lineRule'), 'auto')
    etree.SubElement(pPr, W('jc')).set(W('val'), 'both')
    set_color(etree.SubElement(pPr, W('rPr')))
    r1 = etree.SubElement(p, W('r'))
    rPr1 = etree.SubElement(r1, W('rPr'))
    etree.SubElement(rPr1, W('b')); etree.SubElement(rPr1, W('bCs'))
    set_color(rPr1)
    etree.SubElement(r1, W('t')).text = category + ':'
    r2 = etree.SubElement(p, W('r'))
    set_color(etree.SubElement(r2, W('rPr')))
    t2 = etree.SubElement(r2, W('t'))
    t2.text = ' ' + items
    t2.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

def add_cert_line(body, cert_name, institution):
    p = etree.SubElement(body, W('p'))
    pPr = etree.SubElement(p, W('pPr'))
    sp = etree.SubElement(pPr, W('spacing'))
    sp.set(W('line'), '276'); sp.set(W('lineRule'), 'auto')
    set_color(etree.SubElement(pPr, W('rPr')))
    r1 = etree.SubElement(p, W('r'))
    rPr1 = etree.SubElement(r1, W('rPr'))
    etree.SubElement(rPr1, W('b')); etree.SubElement(rPr1, W('bCs'))
    set_color(rPr1)
    etree.SubElement(r1, W('t')).text = cert_name
    r2 = etree.SubElement(p, W('r'))
    set_color(etree.SubElement(r2, W('rPr')))
    t2 = etree.SubElement(r2, W('t'))
    t2.text = ' - ' + institution
    t2.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')

def add_edu_heading2(body, text, dates):
    p = etree.SubElement(body, W('p'))
    pPr = etree.SubElement(p, W('pPr'))
    etree.SubElement(pPr, W('pStyle')).set(W('val'), 'Heading2')
    set_color(etree.SubElement(pPr, W('rPr')))
    r1 = etree.SubElement(p, W('r'))
    set_color(etree.SubElement(r1, W('rPr')))
    etree.SubElement(r1, W('t')).text = text
    r_tab = etree.SubElement(p, W('r'))
    set_color(etree.SubElement(r_tab, W('rPr')))
    etree.SubElement(r_tab, W('tab'))
    r2 = etree.SubElement(p, W('r'))
    set_color(etree.SubElement(r2, W('rPr')))
    etree.SubElement(r2, W('t')).text = dates


def build():
    # Prepare working directory
    if os.path.exists(WORK_DIR):
        shutil.rmtree(WORK_DIR)
    os.makedirs(WORK_DIR)

    # Copy and unpack template
    shutil.copy2(TEMPLATE, TEMPLATE_COPY)
    subprocess.run(['python3', f'{SCRIPTS}/unpack.py', TEMPLATE_COPY, UNPACKED_DIR], check=True)

    # Load document XML
    doc_xml_path = f'{UNPACKED_DIR}/word/document.xml'
    with open(doc_xml_path, 'r', encoding='utf-8') as f:
        tree = etree.fromstring(f.read().encode('utf-8'))

    body = tree.find(W('body'))
    paragraphs = list(body.findall(W('p')))

    # Extract reusable elements from template
    line_after_heading  = paragraphs[4]   # decorative separator line (used as deepcopy source)
    sectPr              = copy.deepcopy(body.find(W('sectPr')))

    # Clear body
    for child in list(body):
        body.remove(child)

    # Build document
    add_title(body, NAME)
    add_contact(body, CONTACT)
    add_profile(body, PROFILE)

    def sep():
        body.append(copy.deepcopy(line_after_heading))

    add_heading1(body, 'Key Achievements')
    sep()
    for a in ACHIEVEMENTS:
        add_bullet(body, a)

    add_prof_exp_header(body, 'Professional Experience')
    sep()

    for role, company, dates, bullets in ROLES:
        add_heading2(body, role, company, dates)
        for b in bullets:
            add_bullet(body, b)

    add_heading1(body, 'Skills and expertise')
    sep()
    for cat, items in SKILLS:
        add_skills_line(body, cat, items)

    add_heading1(body, 'Certifications')
    sep()
    for cert_name, institution in CERTIFICATIONS:
        add_cert_line(body, cert_name, institution)

    add_heading1(body, 'Education')
    sep()
    for edu_text, edu_dates in EDUCATION:
        add_edu_heading2(body, edu_text, edu_dates)

    body.append(sectPr)

    # Write modified XML
    xml_str = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
    with open(doc_xml_path, 'wb') as f:
        f.write(xml_str)

    # Pack output
    output_path = f'{FOLDER}/{OUTPUT_FILENAME}'
    subprocess.run([
        'python3', f'{SCRIPTS}/pack.py',
        UNPACKED_DIR, output_path,
        '--original', TEMPLATE_COPY
    ], check=True)

    print(f'\nDone — saved to: {output_path}')


if __name__ == '__main__':
    build()

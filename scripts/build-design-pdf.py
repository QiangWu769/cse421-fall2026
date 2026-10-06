#!/usr/bin/env python3
"""Render the course DESIGNDOC into a readable PDF; requires reportlab."""
from pathlib import Path
import re
from html import escape
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether,
    Preformatted, Table, TableStyle,
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from design_figures import build_figures

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assignments/pa1/pintos/src/threads/DESIGNDOC'
OUTPUT = ROOT / 'assignments/pa1/design/PA1-DESIGNDOC.pdf'
TEXT = SOURCE.read_text()
FIGURES = build_figures(ROOT / 'assignments/pa1/design/figures')
NAVY = colors.HexColor('#25384b')
GRAY = colors.HexColor('#555555')
styles = {
    'title': ParagraphStyle('title', fontName='Times-Bold', fontSize=20,
                            leading=23, textColor=NAVY, spaceAfter=5),
    'course': ParagraphStyle('course', fontName='Helvetica', fontSize=10,
                             leading=13, textColor=GRAY, spaceAfter=9),
    'section': ParagraphStyle('section', fontName='Times-Bold', fontSize=16,
                              leading=19, textColor=NAVY, spaceBefore=16,
                              spaceAfter=12, keepWithNext=True),
    'label': ParagraphStyle('label', fontName='Times-Bold', fontSize=11.5,
                            leading=15, textColor=NAVY, spaceBefore=9,
                            spaceAfter=4, keepWithNext=True),
    'question': ParagraphStyle('question', fontName='Times-Italic', fontSize=10.3,
                               leading=13, spaceAfter=8, textColor=GRAY,
                               keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Times-Roman', fontSize=10.8,
                           leading=14.2, spaceAfter=8),
    'small': ParagraphStyle('small', fontName='Times-Roman', fontSize=9.5,
                            leading=12.5, spaceAfter=4),
    'code': ParagraphStyle('code', fontName='Courier', fontSize=8.4,
                           leading=10.8, spaceAfter=9, leftIndent=7),
}

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.saved_states = []
    def showPage(self):
        self.saved_states.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        count = len(self.saved_states)
        for state in self.saved_states:
            self.__dict__.update(state)
            self.setStrokeColor(colors.HexColor('#c4cbd2'))
            self.setLineWidth(.4)
            self.line(49, 39, 563, 39)
            self.setFont('Helvetica', 8)
            self.setFillColor(GRAY)
            self.drawString(49, 27, 'CSE 421/521 | Project 1: Threads')
            self.drawRightString(563, 27, f'{self._pageNumber} / {count}')
            super().showPage()
        super().save()

def para(text, style='body'):
    return Paragraph(escape(text), styles[style])

def answer_flow(text, omit_diagram=False):
    flow = []
    blocks = re.split(r'\n\s*\n', text.strip())
    for block in blocks:
        if not block.strip():
            continue
        if omit_diagram and '--->' in block:
            if flow and isinstance(flow[-1], Paragraph):
                flow.pop()
            continue
        field_lines = block.splitlines()
        if field_lines and all(re.match(r'^[A-Za-z_]\w*: ', line) for line in field_lines):
            data = []
            for line in field_lines:
                field, purpose = line.split(': ', 1)
                data.append([Paragraph(escape(field), ParagraphStyle('field', fontName='Courier', fontSize=9.2, leading=12)),
                             Paragraph(escape(purpose), ParagraphStyle('purpose', fontName='Times-Roman', fontSize=10.4, leading=13.5))])
            table = Table(data, colWidths=[112, 402], hAlign='LEFT')
            table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 9),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LINEBELOW', (0, 0), (-1, -1), .25, colors.HexColor('#e3e6ea')),
            ]))
            flow.extend([table, Spacer(1, 8)])
        elif block.startswith('timer  recent_cpu'):
            rows = []
            for line in block.splitlines():
                fields = line.split()
                if fields and fields[0].isdigit():
                    assert len(fields) == 8, line
                    rows.append(fields)
            assert len(rows) == 10
            data = [
                ['Tick', 'recent_cpu', '', '', 'Priority', '', '', 'Next'],
                ['', 'A', 'B', 'C', 'A', 'B', 'C', 'thread'],
            ] + rows
            table = Table(data, colWidths=[47, 56, 56, 56, 56, 56, 56, 70],
                          hAlign='LEFT', repeatRows=2)
            table.setStyle(TableStyle([
                ('SPAN', (1, 0), (3, 0)), ('SPAN', (4, 0), (6, 0)),
                ('BACKGROUND', (0, 0), (-1, 1), colors.HexColor('#e9edf2')),
                ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
                ('FONTNAME', (0, 2), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LINEBELOW', (0, 1), (-1, 1), .6, colors.HexColor('#8795a4')),
                ('LINEBELOW', (0, 2), (-1, -1), .25, colors.HexColor('#d5dbe1')),
            ]))
            flow.extend([table, Spacer(1, 9)])
        elif (block.startswith('struct ') or block.startswith('static ')
              or block.startswith('int ') or block.startswith('typedef ')
              or block.startswith('#define ') or block.startswith('fixed_t ')
              or block.lstrip().startswith('priority =')
              or '--->' in block or '--lock' in block):
            code = KeepTogether([Preformatted(block, styles['code'])])
            if '--->' in block and flow and isinstance(flow[-1], Paragraph):
                intro = flow.pop()
                flow.append(KeepTogether([intro, code]))
            else:
                flow.append(code)
        else:
            flow.append(para(' '.join(line.strip() for line in block.splitlines())))
    return flow

sections = [
    ('ALARM CLOCK', 'Alarm Clock', ['A' + str(i) for i in range(1, 7)]),
    ('PRIORITY SCHEDULING', 'Priority Scheduling - Proposed Design', ['B' + str(i) for i in range(1, 8)]),
    ('ADVANCED SCHEDULER', 'Advanced Scheduler - Proposed Design', ['C' + str(i) for i in range(1, 7)]),
]
labels = {
    'A1': 'Data structures', 'A2': 'Sleep and wakeup', 'A3': 'Interrupt cost',
    'A4': 'Concurrent sleep calls', 'A5': 'Timer races', 'A6': 'Design choice',
    'B1': 'Data structures', 'B2': 'Donation tracking',
    'B3': 'Priority selection and preemption', 'B4': 'Lock acquisition',
    'B5': 'Lock release', 'B6': 'Priority-update race', 'B7': 'Design choice',
    'C1': 'Data structures', 'C2': 'Scheduling example',
    'C3': 'Table conventions', 'C4': 'Update order and performance',
    'C5': 'Design tradeoffs', 'C6': 'Fixed-point arithmetic',
}

story = [para('Project 1: Threads - Design Document', 'title'),
         para('CSE 421/521 - Operating Systems | Fall 2026', 'course')]
group = TEXT.split('---- GROUP ----', 1)[1].split('---- PRELIMINARIES ----', 1)[0]
for line in group.splitlines():
    if line.strip() and not line.startswith('>>'):
        story.append(para(line.strip(), 'small'))
story += [Spacer(1, 8), para('Alarm Clock is implemented. Priority Scheduling and Advanced Scheduler are planned designs.'),
          para('Technical references: the supplied course assignment and the Pintos Project 1 manual and 4.4BSD Scheduler appendix.', 'small')]
# Use actual links and readable titles instead of long unbroken reference URLs.
for title, url in [
    ('Pintos Project 1 manual', 'https://www.scs.stanford.edu/10wi-cs140/pintos/pintos_2.html'),
    ('Pintos 4.4BSD Scheduler appendix', 'https://www.scs.stanford.edu/10wi-cs140/pintos/pintos_7.html'),
]:
    story.append(Paragraph(f'<link href="{url}" color="#25384b">{title}</link>', styles['small']))
story.append(Spacer(1, 13))

core_count = 0
for index, (marker, title, keys) in enumerate(sections):
    story.append(para(title, 'section'))
    start = re.search(r'^\s*' + re.escape(marker) + r'\s*$', TEXT, re.M).end()
    next_markers = ['PRIORITY SCHEDULING', 'ADVANCED SCHEDULER', 'SURVEY QUESTIONS']
    end = len(TEXT)
    for next_marker in next_markers:
        m = re.search(r'^\s*' + re.escape(next_marker) + r'\s*$', TEXT[start:], re.M)
        if m:
            end = min(end, start + m.start())
    section = TEXT[start:end]
    matches = list(re.finditer(r'^>> ([ABC]\d+):[^\n]*\n(?:>>[^\n]*\n)*', section, re.M))
    assert [m.group(1) for m in matches] == keys
    for i, match in enumerate(matches):
        key = match.group(1)
        question = ' '.join(line[3:].strip() for line in match.group(0).splitlines())
        question = re.sub(r'^[ABC]\d+:\s*', '', question)
        finish = matches[i + 1].start() if i + 1 < len(matches) else len(section)
        answer = section[match.end():finish]
        answer = re.sub(r'^---- [A-Z ]+ ----[ \t]*$', '', answer, flags=re.M).strip()
        assert answer, key
        flows = answer_flow(answer, omit_diagram=(key == 'B2'))
        story.append(KeepTogether([para(f'{key}. {labels[key]}', 'label'),
                                   para(question, 'question'), flows[0]]))
        story.extend(flows[1:])
        if key in FIGURES:
            drawing, caption = FIGURES[key]
            story.append(KeepTogether([Spacer(1, 8), drawing,
                                       para(caption, 'small'), Spacer(1, 10)]))
        core_count += 1
assert core_count == 19

# Keep the original optional survey questions without inventing group feedback.
survey = TEXT.split('SURVEY QUESTIONS', 1)[1]
questions = re.findall(r'^>>[^\n]*\n(?:>>[^\n]*\n)*', survey, re.M)
assert len(questions) == 5
story.append(Spacer(1, 10))
story.append(para('Optional survey questions', 'label'))
for q in questions:
    question = ' '.join(line[3:].strip() for line in q.splitlines())
    story.append(para(question, 'small'))

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter, rightMargin=49,
                        leftMargin=49, topMargin=42, bottomMargin=53,
                        title='CSE 421/521 - Project 1 Design Document',
                        author='Qiang Wu; Mohammad Sahir; Siraat Mustafa',
                        subject='Alarm Clock implementation and planned priority and MLFQS designs',
                        creator='CSE 421/521 Project 1')
doc.build(story, canvasmaker=NumberedCanvas)
print(f'Created {OUTPUT}')

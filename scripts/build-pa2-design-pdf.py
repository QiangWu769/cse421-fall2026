#!/usr/bin/env python3
"""Render the Project 2 design proposal in the original template format; requires ReportLab."""
from pathlib import Path
import re

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Preformatted, PageBreak, KeepTogether
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'assignments/pa2/pintos/src/threads/DESIGNDOC'
OUTPUT = ROOT / 'assignments/pa2/design/PA2-DESIGNDOC.pdf'

raw = SOURCE.read_text()
raw = re.split(r'^\s*SURVEY QUESTIONS\s*$', raw, maxsplit=1, flags=re.M)[0]
blocks = re.split(r'\n\s*\n', raw.strip('\n'))
blocks = [block for block in blocks if not block.startswith((
    '>> Fill in the names',
    '>> If you have any preliminary comments',
    '>> Please cite any offline or online sources',
    'Technical references used for the design:',
))]

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.states = []

    def showPage(self):
        self.states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        count = len(self.states)
        for state in self.states:
            self.__dict__.update(state)
            self.setFont('Courier', 8)
            self.drawRightString(567, 25, f'{self._pageNumber} / {count}')
            super().showPage()
        super().save()

style = ParagraphStyle('template', fontName='Courier', fontSize=10,
                       leading=12.2, spaceAfter=12.2,
                       allowWidows=0, allowOrphans=0)
story = []
pending = []
for block in blocks:
    heading = bool(re.fullmatch(r'\s*[A-Z ]+\n\s*=+', block))
    if heading and block.strip().splitlines()[0] in ('SYSTEM CALLS',):
        story.append(PageBreak())
    pending.append(block)
    if (heading or block.startswith('---- ') or block.startswith('>> ')
            or block.startswith('For H, M, and L') or block.endswith(':')):
        continue
    story.append(KeepTogether([Preformatted('\n\n'.join(pending), style, dedent=0)]))
    pending = []
assert not pending

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter,
                        leftMargin=45, rightMargin=45,
                        topMargin=42, bottomMargin=45,
                        title='CSE 421/521 Project 2 Design Proposal',
                        author='Qiang Wu; Mohammad Sahir; Siraat Mustafa',
                        subject='Project 2 proposed design in the original userprog template',
                        creator='CSE 421/521 Project 2')
doc.build(story, canvasmaker=NumberedCanvas)
print(OUTPUT)

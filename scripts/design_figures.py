"""Editable vector figures for the Project 1 design document."""
from pathlib import Path
import math
import random
from reportlab.graphics.shapes import Drawing, Path as ShapePath, String, Rect
from reportlab.graphics import renderSVG
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

INK = colors.HexColor('#293241')
BLUE = colors.HexColor('#315e85')
RED = colors.HexColor('#a84444')
PALE = colors.HexColor('#f6f8fa')
FONT = 'Helvetica'
for candidate in [
    Path('/System/Library/Fonts/Supplemental/Comic Sans MS.ttf'),
    Path('/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS.ttf'),
]:
    if candidate.is_file():
        pdfmetrics.registerFont(TTFont('SketchLabel', str(candidate)))
        FONT = 'SketchLabel'
        break

rng = random.Random(421)

def rough_line(d, x1, y1, x2, y2, color=INK, width=1.05, dashed=False):
    path = ShapePath(strokeColor=color, strokeWidth=width, fillColor=None)
    if dashed:
        path.strokeDashArray = [3, 3]
    path.moveTo(x1, y1)
    distance = math.hypot(x2-x1, y2-y1)
    nx, ny = (-(y2-y1)/distance, (x2-x1)/distance) if distance else (0, 0)
    for i in range(1, 6):
        f = i/6
        jitter = rng.uniform(-.7, .7)
        path.lineTo(x1+(x2-x1)*f+nx*jitter, y1+(y2-y1)*f+ny*jitter)
    path.lineTo(x2, y2)
    d.add(path)

def arrow(d, x1, y1, x2, y2, color=INK, dashed=False):
    rough_line(d, x1, y1, x2, y2, color, dashed=dashed)
    angle = math.atan2(y2-y1, x2-x1)
    for side in [-1, 1]:
        end_angle = angle + math.pi + side*.42
        rough_line(d, x2, y2, x2+7*math.cos(end_angle), y2+7*math.sin(end_angle), color)

def label(d, text, x, y, size=10.5, color=INK, anchor='middle'):
    d.add(String(x, y, text, fontName=FONT, fontSize=size,
                 fillColor=color, textAnchor=anchor))

def box(d, x, y, width, height, lines, fill=PALE, color=INK):
    if fill is not None:
        d.add(Rect(x+.5, y+.5, width-1, height-1, fillColor=fill, strokeColor=None))
    points=[(x,y),(x+width,y),(x+width,y+height),(x,y+height),(x,y)]
    for a,b in zip(points,points[1:]):
        rough_line(d,*a,*b,color=color)
    step=15
    first=y+height/2+(len(lines)-1)*step/2-3.5
    for i,line in enumerate(lines):
        if isinstance(line,tuple):text,tint=line
        else:text,tint=line,color
        label(d,text,x+width/2,first-i*step,color=tint)

def alarm():
    d=Drawing(514,235)
    label(d,'timer_sleep()',120,214,size=12)
    label(d,'timer interrupt',394,214,size=12)
    box(d,20,158,200,47,['Enqueue sleep request','Sorted by wake_tick'])
    box(d,20,78,200,47,['sema_down(wake)',('BLOCKED',BLUE)])
    box(d,20,10,200,35,[('READY',BLUE)])
    box(d,294,170,200,35,['ticks++'])
    box(d,294,105,200,43,['Remove due sleepers'])
    box(d,294,45,200,35,['sema_up(wake)'])
    arrow(d,120,158,120,125)
    arrow(d,120,78,120,45,color=BLUE,dashed=True)
    label(d,'on signal',130,57,size=8.5,color=BLUE,anchor='start')
    arrow(d,394,170,394,148)
    arrow(d,394,105,394,80)
    arrow(d,220,177,294,127,color=BLUE,dashed=True)
    label(d,'shared list',252,184,size=8.5,color=BLUE)
    arrow(d,294,62,220,27,color=BLUE)
    return d

def donation():
    d=Drawing(514,200)
    label(d,'Donation follows the lock-wait chain',257,185,size=12)
    boxes=[(15,'H',50,'waits for A'),(188,'M',30,'holds A; waits for B'),
           (361,'L',10,'holds B')]
    for x,name,base,state in boxes:
        box(d,x,78,138,91,[name,f'base: {base}',('effective: 50',RED),state])
        rough_line(d,x+32,107,x+105,107,color=RED,width=.7)
    arrow(d,153,126,188,126,color=RED)
    arrow(d,326,126,361,126,color=RED)
    label(d,'lock A',170,142,size=8,color=RED)
    label(d,'lock B',343,142,size=8,color=RED)
    label(d,'Base priorities stay unchanged.',257,54,size=10.5)
    label(d,'After L releases B: L returns to 10; M keeps 50 while H waits for A.',
          257,25,size=9)
    return d

def mlfqs():
    d=Drawing(514,290)
    stages=[
        (240,'each tick',['Charge running non-idle thread','recent_cpu += 1']),
        (187,'each tick',['Wake due sleepers']),
        (134,'every 100 ticks',['Update load_avg, then recent_cpu','for all non-idle threads']),
        (81,'every 4 ticks',['Recalculate non-idle priorities']),
        (28,'after updates',['Compare priorities / time slice','Request yield on IRQ return if needed']),
    ]
    for y,frequency,lines in stages:
        box(d,10,y+5,121,28,[frequency],fill=None,color=BLUE)
        box(d,155,y,339,38,lines)
        rough_line(d,131,y+19,155,y+19,color=BLUE,dashed=True)
    for upper,lower in zip(stages,stages[1:]):
        arrow(d,324,upper[0],324,lower[0]+38)
    label(d,'Use the intervals on the left; skipped steps continue downward.',
          257,5,size=9,color=BLUE)
    return d

FIGURES={
    'A2': ('alarm-clock.svg',alarm,
           'Figure 1. Typical blocking path. A stored early signal lets sema_down() return without blocking; a ready thread runs when selected by the scheduler.'),
    'B2': ('priority-donation.svg',donation,
           'Figure 2. H waits for a lock held by M, and M waits for one held by L. Both holders receive H\'s priority of 50.'),
    'C4': ('mlfqs-updates.svg',mlfqs,
           'Figure 3. Timer-update order with the default TIMER_FREQ of 100. Only non-idle threads participate in CPU and load accounting.'),
}

def build_figures(destination):
    destination.mkdir(parents=True,exist_ok=True)
    result={}
    for key,(filename,build,caption) in FIGURES.items():
        drawing=build()
        renderSVG.drawToFile(drawing,str(destination/filename))
        result[key]=(drawing,caption)
    return result

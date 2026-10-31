"""v1.9: version and changelog."""
import os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
rep("VER='v1.8'", "VER='v1.9'")
rep(" changelog:[{version:'v1.8',", " changelog:[{version:'v1.9',date:'2026-10-31',changes:['Warehouse keeps Acrylic letters (by item: section, letter height, sentence width), Wall Sticker, Die Cut, Acrylic boards; surplus = received − executed','📦 من المخزن on existing items (letters: any stock of the same section); counted as received','Acrylic letters: tahtit width (from Wall Sticker) → max letters width = tahtit − 10 cm, stated in the summary','Floor Header on Old Turkish: ستيكر + تصنيع أكريليك (default, old items too) / ستيكر فقط; execution says what to do','Old design: pharmacy (new / old + photos in the print summary) and item (marked, no built-in image)','Side acrylic: direction = direction of the curve (hint and notes)','Acrylic boards status shown as تصنيع + تركيب (light red) and in shortages / WhatsApp','Management reports: start / end date of every pharmacy','Executed raises received (and old data fixed)','Backups carry the app version and date, shown on restore','Month close checklist','Fix: roll requests no longer break the management report (own field p.rolls)']},{version:'v1.8',")
open(P, 'w', encoding='utf-8').write(s)
print('ok')

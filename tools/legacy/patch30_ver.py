"""v1.6: version and changelog."""
import os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
rep("VER='v1.5'", "VER='v1.6'")
rep(" changelog:[{version:'v1.5',", " changelog:[{version:'v1.6',date:'2026-10-27',changes:['Custody Excel as the owner edited it: yellow title, purple subtitle, no blank row under the title, tighter rows, signatures row 14; column م navy bold on light gold and never coloured with the date; the no-paper sentence stays red and clear with the invoice number small under it; narrower car column with a smaller font; expenses by pharmacy in the summary sheet; footer with the month and page x of y; the PDF and the custody screen follow','Invoice photos appendix PDF: every photo with the same number م as the statement, and the invoices without a photo listed','Old Turkish gondola: number of acrylic pockets to make; the pocket has its own received / executed counter under each gondola, shows in the print / execution shortages, counts in the progress, and moves to / from the warehouse on its own; old receipts keep the pocket with the header / side','Warehouse: pull and print-missing per part group (header + side apart from the pocket); section name not repeated; rows waiting in Add to warehouse are kept until saved or cancelled']},{version:'v1.5',")
open(P, 'w', encoding='utf-8').write(s)
print('ok')

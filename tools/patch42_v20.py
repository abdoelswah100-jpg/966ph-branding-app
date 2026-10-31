"""v2.0: month board header fits the phone, receiving in the bottom bar (reports in the menu), Parcelat letters green."""
import os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
# month board: title on its own line, buttons share the next line (no page wider than the screen)
rep(".mhd{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}",
    ".mhd{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-start;gap:8px}.mhd>div{flex:1 1 100%;min-width:0}.mhd>.b-wa{flex:1 1 140px;justify-content:center;white-space:normal;min-width:0}")
# bottom bar: receiving after pharmacies; reports move to the menu
rep("const ICN={box:", "const ICN={inbox:'<path d=\"M22 12h-6l-2 3h-4l-2-3H2\"/><path d=\"M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z\"/>',box:")
rep("const TABS=[['home','الصيدليات','bld',''],['month','الشهر','bars',''],['wh','المخزن','box',''],['revhub','مراجعة','eye','t-rev'],['all','التقارير','layers',''],['bk','النسخ','db','']];",
    "const TABS=[['home','الصيدليات','bld',''],['rcv','الاستلام','inbox',''],['month','الشهر','bars',''],['wh','المخزن','box',''],['revhub','مراجعة','eye','t-rev'],['bk','النسخ','db','']];")
rep("const TABOF={rcv:'',rca:'',", "const TABOF={rcv:'rcv',rca:'rcv',")
rep("const MENU=[['rcv','الاستلام','box'],['usr',", "const MENU=[['all','التقارير','layers'],['usr',")
rep("a.innerHTML=hdr(V.bp?'<button data-rcvb=\"1\">‹ الصيدلية</button>':backBtn(),'📥 الاستلام')", "a.innerHTML=hdr(V.bp?'<button data-rcvb=\"1\">‹ الصيدلية</button>':'','📥 الاستلام')")
rep("const RCVM='المستلم بيتسجل من شاشة 📥 الاستلام (من القائمة ☰) برقم الصيدلية';", "const RCVM='المستلم بيتسجل من شاشة 📥 الاستلام (في الشريط اللي تحت) برقم الصيدلية';")
# Parcelat letters: light lime green (different from Health)
rep("Mizan:'#BE9857',", "Mizan:'#BE9857','برسلات (Parcelat)':'#A8D86E',")
# version
rep("VER='v1.9'", "VER='v2.0'")
rep(" changelog:[{version:'v1.9',", " changelog:[{version:'v2.0',date:'2026-10-31',changes:['Month board header fits the phone (buttons on their own line; the page was wider than the screen)','Bottom bar: الاستلام after الصيدليات; التقارير moved to the menu','Parcelat letters (برسلات) light lime green #A8D86E, different from Health']},{version:'v1.9',")
open(P, 'w', encoding='utf-8').write(s)
print('ok')
import json
s = open(P, encoding='utf-8').read()
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
D['المستلم بيتسجل من شاشة 📥 الاستلام (في الشريط اللي تحت) برقم الصيدلية'] = 'Received is entered in the 📥 Receiving tab (bottom bar) by pharmacy number'
D.setdefault('الاستلام', 'Receiving')
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('EN ok')

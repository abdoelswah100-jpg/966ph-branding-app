"""v3.1: Wall Sticker «تخطيط»: height filled from the last layout of the pharmacy (Pharmacy section +10), editable;
Acrylic letters: layout height = Wall Sticker layout height of the same section − 10, editable; «الطول» → «الارتفاع» where it means height."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'wsPrep' not in s

# ---- labels: height
rep("num('h','الطول (سم)'),num('w','العرض (سم)'),Q,{k:'nt'", "num('h','الارتفاع (سم)'),num('w','العرض (سم)'),Q,{k:'nt'")
rep("num('h','الطول (سم)'),num('w','العرض (سم)'),Q,Object.assign(num('mg'", "num('h','الارتفاع (سم)'),num('w','العرض (سم)'),Q,Object.assign(num('mg'")
rep("قطعة الطول أو العرض فاضي", "قطعة الارتفاع أو العرض فاضي", 2)
rep("<label>الطول (سم)<input data-cr=\"${i}:h\"", "<label>الارتفاع (سم)<input data-cr=\"${i}:h\"")
rep("'ضرب الطول والعرض لكل بنود Wall Sticker (", "'ضرب الارتفاع والعرض لكل بنود Wall Sticker (")
rep("مفيش أسطر كاملة (طول وعرض وعدد) للإرسال", "مفيش أسطر كاملة (ارتفاع وعرض وعدد) للإرسال")

# ---- automatic heights
rep("function alPrep(d){", "function alPrep(d){if(d.h===undefined||d.h===''||d._ha){const v=alTh(curP(),d.sec);if(v!==''){d.h=v;d._ha=1}else if(d._ha){d.h='';delete d._ha}}")
rep("function form(t,s){if(t.id=='al'){const d=draft(t,s);alPrep(d);const h=form0(t,s);if(!RATIO[d.sec])return h;return h.replace(",
    "function form(t,s){if(t.id=='ws'){const d=draft(t,s);wsPrep(d);const h=form0(t,s);return d._hA?h.replace(/<input data-t=\"ws\" data-k=\"h\"[^>]*>/,m=>m+`<small class=\"autot\">تلقائي من آخر تخطيط في الصيدلية${d.sec=='Pharmacy'?' + 10':''} · عدّله لو مختلف</small>`):h}\n if(t.id=='al'){const d=draft(t,s);alPrep(d);const h0=form0(t,s),h=d._ha?h0.replace(/<input data-t=\"al\" data-k=\"h\"[^>]*>/,m=>m+'<small class=\"autot\">تلقائي: تخطيط Wall Sticker للقسم − 10 · عدّله حسب تقديرك</small>'):h0;if(!RATIO[d.sec])return h;return h.replace(")
rep("document.addEventListener('input',e=>{const x=e.target;\n if(x.dataset.t=='al'&&x.dataset.k=='tw'&&V.dr.al){V.dr.al.tw=x.value;delete V.dr.al._twa;return}",
    "document.addEventListener('input',e=>{const x=e.target;\n if(x.dataset.t=='ws'&&x.dataset.k=='h'&&V.dr.ws){V.dr.ws.h=x.value;delete V.dr.ws._hA;return}\n if(x.dataset.t=='al'&&x.dataset.k=='h'&&V.dr.al){V.dr.al.h=x.value;delete V.dr.al._ha;return}\n if(x.dataset.t=='al'&&x.dataset.k=='tw'&&V.dr.al){V.dr.al.tw=x.value;delete V.dr.al._twa;return}")
JS = r"""// ---------- v3.1: layout heights filled automatically ----------
function wsLastH(p){const L=((p&&p.rows.ws)||[]).filter(r=>r.kd=='تخطيط'&&+r.h>0),a=L.filter(r=>r.sec!='Pharmacy');if(a.length)return +a[a.length-1].h;const b=L.filter(r=>r.sec=='Pharmacy');return b.length&&+b[b.length-1].h>10?+b[b.length-1].h-10:''}
function wsPrep(d){if(d.kd!='تخطيط'){if(d._hA){d.h='';delete d._hA}return}if(d.h===undefined||d.h===''||d._hA){const b=wsLastH(curP());if(b!==''){d.h=d.sec=='Pharmacy'?b+10:b;d._hA=1}else if(d._hA){d.h='';delete d._hA}}}
function alTh(p,sec){const L=((p&&p.rows.ws)||[]).filter(r=>r.kd=='تخطيط'&&r.sec==sec&&+r.h>0);if(!L.length)return '';const v=+L[L.length-1].h-10;return v>0?v:''}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
rep("VER='v3.0'", "VER='v3.1'")
rep(" changelog:[{version:'v3.0',", " changelog:[{version:'v3.1',date:'2026-11-04',changes:['Wall Sticker (تخطيط): the height is filled from the last layout of the pharmacy (Pharmacy section +10), editable','Acrylic letters: layout height = the Wall Sticker layout height of the same section − 10, editable','«الطول» is now «الارتفاع» where it means height (Wall Sticker, Sticker outdoor, calculator, alerts)']},{version:'v3.0',")
EN = {'الارتفاع (سم)':'Height (cm)','قطعة الارتفاع أو العرض فاضي':'pieces with empty height or width','ضرب الارتفاع والعرض لكل بنود':'Multiply height and width of all items of','ارتفاع وعرض وعدد':'height, width and count','تلقائي من آخر تخطيط في الصيدلية':'Automatic from the last layout in the pharmacy','عدّله لو مختلف':'edit it if different','تلقائي: تخطيط Wall Sticker للقسم − 10':'Automatic: section Wall Sticker layout − 10','عدّله حسب تقديرك':'edit as you judge'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D[a2] = c
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')

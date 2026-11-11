"""v1.5 part 4: print only what is missing (warehouse), custody alert below 2000, maintenance search, share before / after photos."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
assert 'function whNet' not in s
rep("// ---------- users, permissions and collecting the supervisors' files ----------", open(os.path.join(R, 'src/x15.js.part'), encoding='utf-8').read() + "\n// ---------- users, permissions and collecting the supervisors' files ----------")
rep(" if(usrClick(d,b)||custClick(d,b)||mntClick(d)||whClick(d,b))return;", " if(usrClick(d,b)||custClick(d,b)||mntClick(d)||whClick(d,b)||x15Click(d,b))return;")
rep(" if(usrChange(x)||custChange(x)||mntChange(x)||whChange(x))return;", " if(usrChange(x)||custChange(x)||mntChange(x)||whChange(x)||x15Change(x))return;")
rep("const PHEDIT=['add',", "const PHEDIT=['sxpull','add',")
# print summary: net of the warehouse
rep("<div id=\"rp\">${c?ckHtml(p):m?mgmtHtml(p):sumHtml(p)}</div><pre id=\"st\" hidden>${esc(sumText(p))}</pre>${outBtns(m)}</main>`;fixT();return}",
    "${!c&&!m?sxBox(p,whNet(p)):''}<div id=\"rp\">${c?ckHtml(p):m?mgmtHtml(p):V.sxw?'<div class=\"sxn\">📦 ملخص الطباعة بعد خصم الموجود في المخزن</div>'+sumHtml(whNet(p).p):sumHtml(p)}</div><pre id=\"st\" hidden>${esc(sumText(!c&&!m&&V.sxw?whNet(p).p:p))}</pre>${outBtns(m)}</main>`;fixT();return}")
# custody alert
rep("<div><small>عدد الفواتير</small><b>${L.length}</b></div></div>\n <div class=\"cbtn\"><button class=\"pr\" data-cscan", "<div><small>عدد الفواتير</small><b>${L.length}</b></div></div>${cAlHtml()}\n <div class=\"cbtn\"><button class=\"pr\" data-cscan")
rep("<label>أقل متبقي ينقل للشهر الجديد<input type=\"number\" inputmode=\"decimal\" data-cc=\"min\" value=\"${C.cfg.min}\"></label></div>",
    "<label>أقل متبقي ينقل للشهر الجديد<input type=\"number\" inputmode=\"decimal\" data-cc=\"min\" value=\"${C.cfg.min}\"></label></div><label>نبّهني لو المتبقي أقل من (0 = من غير تنبيه)<input type=\"number\" inputmode=\"decimal\" data-cc=\"al\" value=\"${cAl()}\"></label>")
rep("${[bkBanner(),syncBanner()].filter(x=>x.startsWith('<div class=\"alr\"')).join('')}", "${[bkBanner(),syncBanner()].filter(x=>x.startsWith('<div class=\"alr\"')).join('')}${cAlHtml(1)}")
rep("V.ce=null;goV({v:'cust',op:{},dr:{},q:V.q,from:V.from});toastT('✓ اتحفظت الفاتورة');",
    "V.ce=null;goV({v:'cust',op:{},dr:{},q:V.q,from:V.from});toastT('✓ اتحفظت الفاتورة');{const a=cAlert();if(a&&a.r+amt>=a.a)setTimeout(()=>toastT('⚠ رصيد العهدة المتبقي بقى '+f2(a.r)+' (أقل من '+f2(a.a)+'). اطلب تعزيز العهدة.'),2500)}")
# maintenance search
rep("function mntHtml(){const C=MU(),q=C.cur,L=mList(q),", "function mntHtml(){const C=MU(),q=C.cur,mf=String(V.mqf||'').trim().toLowerCase(),L=mList(q).filter(x=>!mf||[x.ph,x.ct,x.work,x.det,x.ad,x.sz,x.nt].join(' ').toLowerCase().includes(mf)),")
rep("<div class=\"wcard\"><div class=\"cmo\"><label>الربع<select id=\"mqsel\">", "<div class=\"wcard\"><input class=\"sf\" id=\"mqf\" placeholder=\"🔍 بحث برقم الصيدلية أو نوع العمل\" value=\"${esc(V.mqf||'')}\"><div class=\"cmo\"><label>الربع<select id=\"mqsel\">")
# photos: share button
rep("<small class=\"hint\">الصور بتتحفظ على الجهاز ده ومش بتظهر في أي تقرير. بتتنقل لجهاز تاني بـ \"نسخة كاملة مع الصور والمرفقات\" بس.</small>",
    "${n?`<button data-phshare=\"1\">${ic('share')}مشاركة الصور (واتساب)</button>`:''}<small class=\"hint\">الصور بتتحفظ على الجهاز ده ومش بتظهر في أي تقرير. بتتنقل لجهاز تاني بـ \"نسخة كاملة مع الصور والمرفقات\" بس.</small>")
CSS = "\n.sxw{background:var(--c);border:1px solid var(--ln);border-radius:12px;padding:10px;margin:8px 0;display:grid;gap:6px}.sxw .ph{display:grid;gap:4px}.sxn{background:#FFF4D6;color:#5A4300;border:1px solid #F2B705;border-radius:10px;padding:6px 10px;font-weight:800;text-align:center;margin-bottom:8px}.alr.cal{border-color:#C7313B}.alr.cal b{color:#8B0000}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'اطبع الناقص بس (اخصم الموجود في المخزن)':'Print only what is missing (deduct warehouse stock)','📦 موجود في المخزن ومش هيتطبع:':'📦 In the warehouse, will not be printed:','اسحبهم من المخزن للصيدلية':'Take them from the warehouse for this pharmacy','مفيش حاجة من بنود الصيدلية دي موجودة في المخزن.':'None of this pharmacy items is in the warehouse.','📦 ملخص الطباعة بعد خصم الموجود في المخزن':'📦 Print summary after deducting warehouse stock','هيتخصم الموجود من المخزن ويتحسب مستلم في الصيدلية. تكمل؟':'Stock will be deducted and counted as received in the pharmacy. Continue?','نبّهني لو المتبقي أقل من (0 = من غير تنبيه)':'Alert me when the remaining is below (0 = no alert)','اطلب تعزيز العهدة.':'Ask for a custody top-up.','رصيد العهدة المتبقي':'Custody remaining','أقل من':'below','🔍 بحث برقم الصيدلية أو نوع العمل':'🔍 Search by pharmacy number or work type','مشاركة الصور (واتساب)':'Share photos (WhatsApp)','جاري تجهيز الصور…':'Preparing photos…','مفيش صور على الجهاز ده':'No photos on this device','العهدة':'Custody'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)

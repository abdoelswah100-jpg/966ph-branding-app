"""v1.4 part 2: maintenance (الصيانة) + fix for a pharmacy without a valid shelf type."""
import json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
assert 'function mntHtml' not in s, 'already applied'
JS = open(os.path.join(R, 'src/mnt.js.part'), encoding='utf-8').read()
rep("// ---------- PDF ----------", JS + "\n// ---------- PDF ----------")
rep("const MENU=[['cust','العهدة','sheet'],", "const MENU=[['cust','العهدة','sheet'],['mnt','الصيانة','check'],")
rep("const TABOF={cust:'',ced:'',", "const TABOF={mnt:'',med:'',cust:'',ced:'',")
rep("const PARENT={ced:'cust',", "const PARENT={med:'mnt',ced:'cust',")
rep(" if(V.v=='cust'){a.innerHTML=", " if(V.v=='mnt'){a.innerHTML=hdr(backBtn(),'الصيانة')+`<main>${mntHtml()}</main>`;return}\n if(V.v=='med'){a.innerHTML=hdr('<button data-mcancel=\"1\">‹ الصيانة</button>',V.me&&MU().items.some(x=>x.id==V.me.id)?'تعديل صيانة':'صيانة جديدة')+`<main>${medHtml()}</main>`;return}\n if(V.v=='cust'){a.innerHTML=")
rep(" {const tr=e.target.closest('tr[data-ced]');if(tr&&!b){custClick({ced:tr.dataset.ced});return}}", " {const tr=e.target.closest('tr[data-ced]');if(tr&&!b){custClick({ced:tr.dataset.ced});return}const tm=e.target.closest('tr[data-med]');if(tm&&!b){mntClick({med:tm.dataset.med});return}}")
rep(" if(custClick(d,b))return;", " if(custClick(d,b)||mntClick(d))return;")
rep(" if(custChange(x))return;", " if(custChange(x)||mntChange(x))return;")
# invoice / maintenance photos both live under cimg:<id>:..; add maintenance photos to the full backup
rep("for(const m of Object.values((DB.cust||{}).m||{}))for(const x of m.items||[])for(const k of x.imgs||[]){const b=await idbGet(k);if(b)files[k]=await r2u(b)}",
    "for(const m of Object.values((DB.cust||{}).m||{}))for(const x of m.items||[])for(const k of x.imgs||[]){const b=await idbGet(k);if(b)files[k]=await r2u(b)}for(const x of (DB.mnt||{}).items||[])for(const k of [...(x.imb||[]),...(x.ima||[])]){const b=await idbGet(k);if(b)files[k]=await r2u(b)}")
# a pharmacy whose shelf type is missing or invalid crashed its page: fall back to the first shelf type
rep("p.st=p.st||'لم تبدأ';", "p.st=p.st||'لم تبدأ';if(!(p.sh>=0&&p.sh<SH.length))p.sh=0;")
CSS = r"""
.mwk{display:flex;flex-wrap:wrap;gap:6px}.mwk button{flex:1 1 30%;min-height:38px;font-size:13px;background:var(--c);border:1.5px solid var(--ln)}.mwk button.on{background:var(--wc);border-color:var(--pb);font-weight:800;color:#1B2430}
.mtab tr.mmo td{background:#FFF6D6;font-weight:800;color:var(--pb)}:root[data-th=dark] .mtab tr.mmo td{background:#2A230F;color:#FFE3A8}.mtab tr[data-med]{cursor:pointer}
"""
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'الصيانة':'Maintenance','كشف صيانات':'Maintenance sheet','عدد الأعمال':'Jobs','عدد القطع':'Pieces','عدد الصيدليات':'Pharmacies','الربع':'Quarter','إضافة صيانة':'Add maintenance','تكرار آخر بند':'Repeat last item','الصيدلية':'Pharmacy','نوع العمل':'Work type','التفاصيل':'Details','المقاس':'Size','العدد':'Qty','اضغط على أي بند علشان تعدّله أو تمسحه.':'Tap an item to edit or delete it.','إعدادات الصيانة والاستيراد':'Maintenance settings and import','استيراد صيانات من ملف (اللي Claude بيجهّزه)':'Import maintenance from a file (prepared by Claude)','صيانة جديدة':'New maintenance','تعديل صيانة':'Edit maintenance','‹ الصيانة':'‹ Maintenance','المدينة':'City','نوع الدعاية':'Ad type','المقاس (سم)':'Size (cm)','البيان للمحاسب:':'Statement for the accountant:','صور قبل':'Before photos','صور بعد':'After photos','إضافة':'Add','حفظ':'Save','✓ اتحفظت الصيانة':'✓ Maintenance saved','تمسح البند ده؟':'Delete this item?','✓ اتمسح':'✓ Deleted','لا توجد صيانات مسجلة':'No maintenance recorded','تركيب':'Install','إزالة وتركيب':'Remove and install','تغيير':'Replace','صيانة (إعادة لصق)':'Repair (re-stick)','إعادة تركيب':'Re-install','تصنيع وتركيب':'Make and install','طباعة فقط':'Print only','الربع الأول':'Q1','الربع الثاني':'Q2','الربع الثالث':'Q3','الربع الرابع':'Q4','اختار التاريخ':'Choose the date','اكتب رقم الصيدلية':'Enter the pharmacy number','اختار نوع الدعاية أو اكتب التفاصيل':'Choose the ad type or write the details','اكتب العدد':'Enter the quantity','الربع ده مفيهوش صيانات. تكمل؟':'This quarter has no maintenance. Continue?','الملف ده مش ملف صيانات':'This is not a maintenance file','مفيش صيانات في الملف':'No maintenance in the file','عمل':'jobs','قطعة':'pieces','يناير':'January','فبراير':'February','مارس':'March','أبريل':'April','مايو':'May','يونيو':'June','يوليو':'July','أغسطس':'August','سبتمبر':'September','أكتوبر':'October','نوفمبر':'November','ديسمبر':'December','أخرى':'Other'}
k = s.index('const EN_D=') + len('const EN_D=')
j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a, b in EN.items():
    if a not in D: D[a] = b; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
rep("changes:['Custody (العهدة):", "changes:['Maintenance (الصيانة): quarterly sheet grouped by month, one line per job (date, pharmacy, city, work type, ad type, details, size, qty), statement for the accountant built automatically, before/after photos, Excel and PDF, import file','A pharmacy without a valid shelf type no longer breaks its page','Custody (العهدة):")
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)

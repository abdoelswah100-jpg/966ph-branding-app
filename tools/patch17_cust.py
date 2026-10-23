"""v1.4 part 1: custody (العهدة). Applies to src/app.html once (asserts exact anchors)."""
import json, os, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:120]}')
    s = s.replace(a, b)
assert 'function custHtml' not in s, 'already applied'
JS = open(os.path.join(R, 'src/cust.js.part'), encoding='utf-8').read()
rep("VER='v1.3'", "VER='v1.4'")
rep("<title>966Ph Branding v1.3</title>", "<title>966Ph Branding v1.4</title>")
# jsQR (Apache-2.0) is inlined at build time
rep("<script>", "<script>/*__JSQR__*/</script>\n<script>")
# module
rep("// ---------- PDF ----------", JS + "\n// ---------- PDF ----------")
# menu, views, navigation
rep("const MENU=[['gen','الإعدادات العامة','gear'],", "const MENU=[['cust','العهدة','sheet'],['gen','الإعدادات العامة','gear'],")
rep("const TABOF={exec:'revhub',", "const TABOF={cust:'',ced:'',exec:'revhub',")
rep("const PARENT={exec:'revhub',", "const PARENT={ced:'cust',exec:'revhub',")
rep(" if(V.v=='imgs'){a.innerHTML=", " if(V.v=='cust'){a.innerHTML=hdr(backBtn(),'العهدة')+`<main>${custHtml()}</main>`;return}\n if(V.v=='ced'){a.innerHTML=hdr('<button data-ccancel=\"1\">‹ العهدة</button>',V.ce&&cMo().items.some(x=>x.id==V.ce.id)?'تعديل فاتورة':'فاتورة جديدة')+`<main>${cedHtml()}</main>`;return}\n if(V.v=='imgs'){a.innerHTML=")
rep("render0();if(a.querySelector('img[data-pho]'))phoFill();", "render0();if(a.querySelector('img[data-pho]'))phoFill();if(a.querySelector('img[data-cimg]'))cImgFill();")
# events
rep("document.addEventListener('click',e=>{const b=e.target.closest('button');", "document.addEventListener('click',e=>{const b=e.target.closest('button');\n {const tr=e.target.closest('tr[data-ced]');if(tr&&!b){custClick({ced:tr.dataset.ced});return}}")
rep(" const d=b.dataset,p=curP();", " const d=b.dataset,p=curP();\n if(custClick(d,b))return;")
rep("document.addEventListener('change',e=>{const x=e.target;", "document.addEventListener('change',e=>{const x=e.target;\n if(custChange(x))return;")
# full backup carries the invoice images
rep("t.remove();return Object.assign({},DB,{cfg:Object.assign({},DB.cfg,{ue:0,lb:nowIso()}),_imgs:IMG,_files:files,_photos:photos})",
    "for(const m of Object.values((DB.cust||{}).m||{}))for(const x of m.items||[])for(const k of x.imgs||[]){const b=await idbGet(k);if(b)files[k]=await r2u(b)}t.remove();return Object.assign({},DB,{cfg:Object.assign({},DB.cfg,{ue:0,lb:nowIso()}),_imgs:IMG,_files:files,_photos:photos})")
# CSS
CSS = r"""
.cust .cuh{display:grid;gap:2px;text-align:center;margin-bottom:10px}.cust .cuh b{font-size:16px;color:var(--pb)}.cust .cuh small{color:var(--mu)}
.ckpi{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:8px 0}.ckpi div{background:var(--c2);border:1px solid var(--ln);border-radius:10px;padding:8px;display:grid;gap:2px;text-align:center}.ckpi small{color:var(--mu);font-size:11.5px;font-weight:700}.ckpi b{font-size:18px}
.c-open{color:#1F3864!important}.c-exp{color:#8B0000!important}.c-rem{color:#1E7B45!important}
:root[data-th=dark] .c-open{color:#8FB0FF!important}:root[data-th=dark] .c-exp{color:#FF8A8A!important}:root[data-th=dark] .c-rem{color:#6FD39A!important}
.cbtn{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.cbtn button{flex:1 1 140px;justify-content:center}
.cshare{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}.cshare button{justify-content:center}
.cmo{display:flex;gap:8px;align-items:flex-end;flex-wrap:wrap;margin-bottom:8px}.cmo label{flex:1 1 150px}
.ctab{width:100%;font-size:12.5px}.ctab td,.ctab th{text-align:center;vertical-align:middle;padding:6px 4px}.ctab tr[data-ced]{cursor:pointer}.ctab td small{display:block;color:var(--mu);font-size:10.5px}
.ctab td.cam b{white-space:nowrap}.ctab small.ck{display:inline-block;border-radius:6px;padding:0 6px;margin-top:2px;color:#1B2430;font-weight:700}
.ctab small.cnp,.cnpt{color:#C00000!important;font-weight:800}.cnpt{background:#FDE2E2}
.ctab tr.co-old td:nth-child(-n+4){background:#FAD4D4;color:#B42318}.ctab tr.co-next td:nth-child(-n+4){background:#D6E6FB;color:#1D4ED8}
.cnew{border:1px dashed var(--gold);border-radius:12px;padding:10px;margin:8px 0;background:#FFFBEB}:root[data-th=dark] .cnew{background:#2A230F}
.ced .fm{display:grid;gap:8px}.ced .c2,.cust .c2,.wcard .c2{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.cimgs{display:flex;gap:8px;flex-wrap:wrap;margin:6px 0}.cimgs span{position:relative}.cimgb{padding:0;border:1px solid var(--ln);border-radius:8px;overflow:hidden;background:#fff}.cimgb img{display:block;height:120px;width:auto}
.cimgx{position:absolute;top:2px;inset-inline-end:2px;padding:2px 7px;min-height:0}
.cnpl{color:#C00000}
.cscan{flex-direction:column;align-items:center;justify-content:center;gap:10px}.cscan video{width:100%;max-width:520px;max-height:70vh;background:#000}.cscan p{color:#fff;font-weight:700}.cscan .cbtn{width:100%;max-width:520px;padding:0 12px}.cscan .cbtn button{position:static}
.cscan .cfr{position:absolute;width:min(62vw,300px);height:min(62vw,300px);border:3px solid #F2B705;border-radius:14px;top:calc(50% - min(31vw,150px) - 40px);pointer-events:none}
.cpt{display:grid;gap:2px;text-align:center;background:#0B1B33;color:#fff;border-radius:6px;padding:8px}.cpt b{font-size:15px}.cpt small{color:#C9D2E0;font-size:10px}
.pdfpg .ckpi{grid-template-columns:repeat(4,1fr)}
table.cpdf{width:100%;border-collapse:collapse;font-size:8.6px}table.cpdf th{background:#0B1B33;color:#fff;font-size:8.6px;padding:4px 2px}table.cpdf td{border:1px solid #D5DCE6;text-align:center;vertical-align:middle;padding:3px 2px}
table.cpdf tr:nth-child(even) td{background:#F5F7FA}table.cpdf tr.copen td{background:#FFF6D6;font-weight:800}table.cpdf td.cbal{color:#5B6B80}
table.cpdf tr.ctot td{background:#F2B705!important;font-weight:800;font-size:10px;color:#0B1B33}
table.cpdf tr.co-old td.cmk{background:#FAD4D4!important;color:#B42318;font-weight:700}table.cpdf tr.co-next td.cmk{background:#D6E6FB!important;color:#1D4ED8;font-weight:700}
.pdfpg table.cpdf th,.pdfpg table.cpdf td{font-size:8.4px!important;line-height:1.25!important;padding:3px 2px!important}.pdfpg table.cpdf td.cdn{white-space:nowrap}.pdfpg table.cpdf tr.ctot td{font-size:10px!important}
.csig{display:flex;justify-content:space-between;color:#5B6B80;font-size:10px;margin-top:14px}
"""
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
# English
EN = {'العهدة':'Custody','كشف مصروفات العهدة':'Custody expense sheet','رصيد بداية الشهر':'Month opening balance','إجمالي المصروف':'Total expenses','المتبقي في العهدة':'Remaining in custody','عدد الفواتير':'Invoices','امسح QR بالكاميرا':'Scan QR with camera','فاتورة من صورة':'Invoice from photo','إضافة يدوي':'Add manually','الشهر':'Month','بدء شهر جديد':'Start new month','المتبقي في رصيد العهدة':'Remaining custody balance','اضغط على أي فاتورة علشان تعدّلها أو تمسحها.':'Tap an invoice to edit or delete it.','■ أحمر = تاريخها قبل الشهر':'■ Red = dated before the month','■ أزرق = بعد الشهر.':'■ Blue = after the month.','لسه مفيش فواتير في الشهر ده.':'No invoices in this month yet.','مشاركة Excel':'Share Excel','حفظ Excel':'Save Excel','حفظ PDF':'Save PDF','إعدادات العهدة والاستيراد':'Custody settings and import','المنطقة في عنوان الكشف':'Region in the sheet title','اسم المشرف':'Supervisor name','لوحة العربية (للديزل)':'Car plate (for diesel)','رصيد العهدة الكامل':'Full custody amount','أقل متبقي ينقل للشهر الجديد':'Minimum remaining carried to the new month','رصيد بداية شهر':'Opening balance of','استيراد فواتير من ملف (اللي Claude بيجهّزه)':'Import invoices from a file (prepared by Claude)','بدء شهر':'Start month','المتبقي من شهر':'Remaining from','ابدأ بالمتبقي':'Start with the remaining','ابدأ بـ':'Start with','مبلغ تاني':'Other amount','ابدأ بالمبلغ ده':'Start with this amount','فاتورة جديدة':'New invoice','تعديل فاتورة':'Edit invoice','‹ العهدة':'‹ Custody','✓ اتقرت البيانات من كود QR الفاتورة. راجعها قبل الحفظ.':'✓ Data read from the invoice QR code. Check it before saving.','⚠ ما قدرتش أقرا كود QR من الصورة. كمّل البيانات يدوي من الصورة.':'⚠ Could not read a QR code in the photo. Fill in the data from the photo.','التاريخ':'Date','الوقت':'Time','النوع':'Type','المبلغ شامل الضريبة':'Amount incl. VAT','البيان':'Description','اسم الشركة':'Company','السيارة':'Car','رقم الصيدلية':'Pharmacy no.','رقم الفاتورة':'Invoice no.','⚠ لا توجد فاتورة ورقية (الرجاء الطباعة)':'⚠ No paper invoice (please print)','ملاحظات':'Notes','إرفاق صورة':'Attach photo','حفظ الفاتورة':'Save invoice','تخطي':'Skip','مسح':'Delete','وجّه الكاميرا على كود QR الفاتورة':'Point the camera at the invoice QR code','📷 صوّر من غير QR':'📷 Take photo without QR','✕ إغلاق':'✕ Close','✓ اتحفظت الفاتورة':'✓ Invoice saved','✓ اتحفظت. الفاتورة اللي بعدها':'✓ Saved. Next invoice','اكتب المبلغ':'Enter the amount','اختار التاريخ':'Choose the date','اكتب البيان واسم الشركة':'Enter the description and company','الفاتورة دي ما اتحفظتش. تلغيها؟':'This invoice is not saved. Discard it?','تمسح الفاتورة دي؟':'Delete this invoice?','✓ اتمسحت':'✓ Deleted','وجبات':'Meals','وقود':'Fuel','شحن':'Shipping','سكن':'Lodging','مشتريات':'Purchases','سيارة':'Car','تنقلات':'Transport','إيجار':'Rental','فطار':'Breakfast','غداء':'Lunch','عشاء':'Dinner','عمال الشركة':'company workers','ديزيل':'Diesel','استلام شحن':'Shipment pickup','⚠ لا توجد فاتورة ورقية':'⚠ No paper invoice','لا توجد فاتورة ورقية الرجاء الطباعة':'No paper invoice, please print','الإجمالي':'Total','الشهر ده مفيهوش فواتير. تكمل؟':'This month has no invoices. Continue?','الملف ده مش ملف فواتير':'This is not an invoice file','مفيش فواتير في الملف':'No invoices in the file','قارئ QR مش موجود في النسخة دي':'QR reader is not available in this version','الكاميرا مش متاحة هنا. استخدم "فاتورة من صورة".':'Camera not available here. Use "Invoice from photo".','مفيش إذن للكاميرا. اسمح للتطبيق باستخدام الكاميرا من إعدادات الموبايل، أو استخدم "فاتورة من صورة".':'No camera permission. Allow camera access in the phone settings, or use "Invoice from photo".','الوقت في الكود ممكن يكون بالتوقيت العالمي. لو الوقت المطبوع على الفاتورة':'The time in the code may be UTC. If the time printed on the invoice is','اضغط هنا:':'tap here:','استخدم':'Use','باقي':'remaining','صورة بعدها':'photos after it','أكتر من':'More than',' فالاقتراح يبدأ بالمتبقي.':' so the suggestion starts with the remaining.','أقل من':'Less than',' فالاقتراح يبدأ بالعهدة كاملة.':' so the suggestion starts with the full custody.'}
k = s.index('const EN_D=') + len('const EN_D=')
j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a, b in EN.items():
    if a not in D: D[a] = b; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
s = s.replace("changelog:[{version:'v1.3',", "changelog:[{version:'v1.4',date:'2026-10-23',changes:['Custody (العهدة): monthly expense sheet with QR reading (camera or photo), manual entry, edit, duplicates check, month start rule, Excel and PDF in the agreed layout, import file','Code cleanup steps 1-5 (no behaviour change)']},{version:'v1.3',", 1)
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)

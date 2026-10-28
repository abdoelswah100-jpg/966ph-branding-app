"""v1.8 part 3: company documents (menu): built-in VAT certificate and national address proof (src/cdocs.json, inlined at build),
open / share / save, replace with a newer file on this device (kept in the full backup), back to the original, extra documents, expiry."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'CDOCS' not in s
JS = r"""// ---- company documents: built-in files + a newer copy on this device (IndexedDB 'doc:<id>', meta in cfg.cdocs)
const CDOCS=/*__CDOCS__*/{};
const cdM=()=>(DB.cfg.cdocs=DB.cfg.cdocs||{});
function cdList(){const M=cdM(),L=Object.keys(CDOCS).map(id=>Object.assign({id,b:1,n:CDOCS[id].n,fn:CDOCS[id].f,exp:CDOCS[id].exp||''},M[id]||{}));Object.keys(M).filter(id=>!CDOCS[id]).forEach(id=>L.push(Object.assign({id},M[id])));return L}
async function cdBlob(x){if(x.own){const b=await idbGet('doc:'+x.id);if(b)return b}const c=CDOCS[x.id];if(c&&c.d)return new Blob([Uint8Array.from(atob(c.d),ch=>ch.charCodeAt(0))],{type:'application/pdf'});return null}
const cdExp=x=>x.exp&&x.exp<TD();
function cdocHtml(){const L=cdList(),dd=d=>d?d.split('-').reverse().join('-'):'';
 return `<div class="wcard"><h2>${ic('sheet')}مستندات الشركة</h2><p class="sub">افتح أو شارك أي مستند. لو اتجدد، اضغط «تبديل» واختار الملف الجديد: بيتحفظ على الجهاز ده وفي النسخة الكاملة.</p></div>`+L.map(x=>`<div class="wcard cdoc${cdExp(x)?' exp':''}"><div class="cdh"><b>${esc(x.n||'مستند')}</b>${x.own?`<small class="rshc">نسختك · اتبدل ${dd((x.at||'').slice(0,10))}</small>`:x.b?'<small class="rshc">الأصلي</small>':''}</div>
 ${cdExp(x)?`<div class="alr cal"><small>⚠ <b>منتهي من ${dd(x.exp)}</b>. طلّع نسخة جديدة وبدّلها.</small></div>`:x.exp?`<small class="sub">ينتهي ${dd(x.exp)}</small>`:''}
 <div class="tt"><button class="pr" data-cdo="${x.id}">${ic('share')}فتح / مشاركة</button><button data-cds="${x.id}">${ic('download')}حفظ</button><button data-cdr="${x.id}">${ic('upload')}تبديل</button>${x.own&&x.b?`<button data-cdb="${x.id}">↺ رجوع للأصلي</button>`:''}${!x.b?`<button data-cdd="${x.id}" style="color:var(--rd)">${ic('trash')}حذف</button>`:''}</div>
 <label class="cdel">تاريخ الانتهاء (اختياري)<input type="date" data-cde="${x.id}" value="${esc(x.exp||'')}"></label></div>`).join('')+`<button class="addb" data-cdr="new">${ic('add')}إضافة مستند (زي السجل التجاري)</button><input type="file" id="cdin" accept="application/pdf,image/*" hidden>`}
async function cdOut(id,share){const x=cdList().find(y=>y.id==id);if(!x)return;const b=await cdBlob(x);if(!b)return alert('الملف مش موجود على الجهاز ده');const fn=(x.fn||x.n||'مستند').replace(/[\\/:*?"<>|]/g,'')+(/\.\w+$/.test(x.fn||'')?'':(b.type=='application/pdf'?'.pdf':'.jpg'));
 if(CAPN())return nativeSave(fn,b,b.type||'application/pdf',share);if(share){const r=await shareFile(b,fn,b.type||'application/pdf');if(r)return;const u=URL.createObjectURL(b);window.open(u,'_blank');return}return out(fn,b,b.type||'application/pdf')}
async function cdPut(id,f){let nm;if(id=='new'){nm=(prompt('اسم المستند (مثلًا السجل التجاري):')||'').trim();if(!nm)return;id='u'+Date.now()}const M=cdM(),o=M[id]=Object.assign(M[id]||{},{own:1,at:nowIso(),fn:f.name});if(nm)o.n=nm;if(!await idbSet('doc:'+id,f)){delete M[id];return alert('تعذّر حفظ الملف على الجهاز ده')}
 if(CDOCS[id]&&CDOCS[id].exp&&o.exp===undefined)o.exp='';sv();render();toastT('✓ اتحفظ المستند')}
function cdClick(d){
 if(d.cdo){cdOut(d.cdo,true);return 1}if(d.cds){cdOut(d.cds,false);return 1}
 if(d.cdr){V.cdt=d.cdr;const i=$('#cdin');if(i)i.click();return 1}
 if(d.cdb){if(!confirm('ترجع للملف الأصلي؟ نسختك هتتمسح من الجهاز ده.'))return 1;idbDel('doc:'+d.cdb);delete cdM()[d.cdb];sv();render();return 1}
 if(d.cdd){if(!confirm('تمسح المستند ده؟'))return 1;idbDel('doc:'+d.cdd);delete cdM()[d.cdd];sv();render();return 1}
 return 0}
function cdChange(x){if(x.id=='cdin'){const f=x.files[0];x.value='';if(f&&V.cdt)cdPut(V.cdt,f);return 1}if(x.dataset&&x.dataset.cde){const M=cdM(),id=x.dataset.cde;M[id]=M[id]||{};M[id].exp=x.value;sv();render();return 1}return 0}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
rep("||x15Click(d,b)||rlClick(d))return;", "||x15Click(d,b)||rlClick(d)||cdClick(d))return;")
rep("||x15Change(x)||rlChange(x))return;", "||x15Change(x)||rlChange(x)||cdChange(x))return;")
rep("['mnt','الصيانة','check'],", "['mnt','الصيانة','check'],['cdoc','مستندات الشركة','sheet'],")
rep(" if(V.v=='imgs'){a.innerHTML=hdr(backBtn(),'صور المسميات')", " if(V.v=='cdoc'){a.innerHTML=hdr(backBtn(),'مستندات الشركة')+`<main>${cdocHtml()}</main>`;return}\n if(V.v=='imgs'){a.innerHTML=hdr(backBtn(),'صور المسميات')")
# full backup carries the replaced / added documents
rep("for(const x of uAllSt('mnt').flatMap(c=>(c||{}).items||[]))for(const k of [...(x.imb||[]),...(x.ima||[])]){const b=await idbGet(k);if(b)files[k]=await r2u(b)}t.remove();",
    "for(const x of uAllSt('mnt').flatMap(c=>(c||{}).items||[]))for(const k of [...(x.imb||[]),...(x.ima||[])]){const b=await idbGet(k);if(b)files[k]=await r2u(b)}for(const id of Object.keys((DB.cfg||{}).cdocs||{})){const b=await idbGet('doc:'+id);if(b)files['doc:'+id]=await r2u(b)}t.remove();")
CSS = "\n.cdoc .cdh{display:flex;justify-content:space-between;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:6px}.cdoc.exp{border-color:#E8A0A0}.cdoc .cdel{margin-top:6px;font-size:12px}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
EN = {'مستندات الشركة':'Company documents','شهادة ضريبة القيمة المضافة':'VAT registration certificate','إثبات العنوان الوطني':'National address proof','فتح / مشاركة':'Open / share','تبديل':'Replace','رجوع للأصلي':'Back to the original','نسختك':'Your copy','اتبدل':'replaced','الأصلي':'Original','منتهي من':'Expired on','طلّع نسخة جديدة وبدّلها.':'Get a new copy and replace it.','ينتهي':'Expires','تاريخ الانتهاء (اختياري)':'Expiry date (optional)','إضافة مستند (زي السجل التجاري)':'Add a document (e.g. commercial register)','اسم المستند (مثلًا السجل التجاري):':'Document name (e.g. commercial register):','اتحفظ المستند':'Document saved','الملف مش موجود على الجهاز ده':'The file is not on this device','ترجع للملف الأصلي؟ نسختك هتتمسح من الجهاز ده.':'Back to the original file? Your copy will be removed from this device.','تمسح المستند ده؟':'Delete this document?','افتح أو شارك أي مستند. لو اتجدد، اضغط «تبديل» واختار الملف الجديد: بيتحفظ على الجهاز ده وفي النسخة الكاملة.':'Open or share any document. When it is renewed, tap «Replace» and choose the new file: it is kept on this device and in the full backup.'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)

"""v3.4: custody (invoices without a paper invoice: count, filter, share/save with a picker, statement + invoices together;
wider «البيان» in Excel / PDF / app), layout (home, sync alert, pharmacy, execution cards, warehouse),
warehouse old stock + out-of-stock alert, Google Drive from the web link (GitHub Pages) + monthly Excel."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'cNpGo' not in s
JS = []
CSS = []
EN = {}

# =====================================================================
# 1. custody
# =====================================================================
# count tile (click = filter the table to these invoices)
rep("<div><small>عدد الفواتير</small><b>${L.filter(x=>!x.qt).length}</b></div></div>${cAlHtml()}",
    "<div><small>عدد الفواتير</small><b>${L.filter(x=>!x.qt).length}</b></div><button class=\"cnpk${V.cnpf?' on':''}\" data-cnpf=\"1\"><small>بدون فاتورة ورقية</small><b>${cNpN(M)}</b><em>${V.cnpf?'✓ معروضين بس · اعرض الكل':'اضغط لعرضهم بس'}</em></button></div>${cAlHtml()}")
rep("np=(x.note||'').includes('فاتورة ورقية'),no=x.qt?'':++cn;return `<tr",
    "np=(x.note||'').includes('فاتورة ورقية'),no=x.qt?'':++cn;if(V.cnpf&&(!np||x.qt))return '';return `<tr")
rep("<table class=\"ctab\"><tr><th>م</th><th>التاريخ</th><th>البيان</th>", "<table class=\"ctab\"><tr><th>م</th><th>التاريخ</th><th class=\"cdsc\">البيان</th>")
# grouped share / save buttons
rep("<div class=\"cshare\"><button class=\"pr\" data-cxl=\"share\">${ic('sheet')}مشاركة Excel</button><button class=\"pr\" data-cpdf=\"share\">${ic('share')}مشاركة PDF</button><button data-cxl=\"save\">${ic('download')}حفظ Excel</button><button data-cpdf=\"save\">${ic('download')}حفظ PDF</button><button data-capx=\"share\">${ic('img')}مشاركة صور الفواتير PDF</button><button data-capx=\"save\">${ic('download')}حفظ صور الفواتير PDF</button></div>",
    "<div class=\"cshare c2b\"><button class=\"pr\" data-cmenu=\"share\">${ic('share')}مشاركة…</button><button data-cmenu=\"save\">${ic('download')}حفظ…</button></div>")
# appendix: optional selection of invoices
rep("async function cAppEl(k){const C=CU(),M=C.m[k],L=M.items.filter(x=>!x.qt),el=document.createElement('div'),no=[],pdfs=[];let h=`<div class=\"cpt cy\"><b>ملحق صور فواتير العهدة — ${esc(C.cfg.region)} — شهر ${cMoLab(k)}</b></div>",
    "async function cAppEl(k,sel){const C=CU(),M=C.m[k],L=M.items.filter(x=>!x.qt),el=document.createElement('div'),no=[],pdfs=[];let h=`<div class=\"cpt cy\"><b>${sel?'فواتير بدون فاتورة ورقية':'ملحق صور فواتير العهدة'} — ${esc(C.cfg.region)} — شهر ${cMoLab(k)}</b></div>")
rep(" for(const[i,x] of L.entries()){const ks=x.imgs||[];if(!ks.length){no.push(i+1);continue}",
    " for(const[i,x] of L.entries()){if(sel&&!sel.has(x.id))continue;const ks=x.imgs||[];if(!ks.length){no.push(i+1);continue}")
rep("el.innerHTML=h;return {el,n:L.filter(x=>(x.imgs||[]).some(y=>!isPdfK(y))).length,pdfs}}",
    "el.innerHTML=h;return {el,n:L.filter(x=>(!sel||sel.has(x.id))&&(x.imgs||[]).some(y=>!isPdfK(y))).length,pdfs}}")
# PDF statement: wider description + count line
rep("<table class=\"cpdf\"><tr><th>م</th><th>التاريخ</th><th>الوقت</th><th>البيان</th>", "<table class=\"cpdf\"><tr><th>م</th><th>التاريخ</th><th>الوقت</th><th class=\"cdsc\">البيان</th>")
rep("<td colspan=\"3\">← المتبقي في رصيد العهدة</td></tr></table>\n <div class=\"csig\">",
    "<td colspan=\"3\">← المتبقي في رصيد العهدة</td></tr></table>\n <div class=\"cnpline\">عدد الفواتير بدون فاتورة ورقية: <b>${L.filter(cNp).length}</b></div>\n <div class=\"csig\">")
# Excel: wider «البيان», taller rows for long text, count line under the total
rep("if(np&&rest)HT[r]=32;", "if(np&&rest)HT[r]=32;{const ln=Math.max(Math.ceil(String(x.desc||'').length/44),Math.ceil(String(x.comp||'').length/30));if(ln>1)HT[r]=Math.max(HT[r]||21,13*ln+8)}")
rep(" const sg=tot+2;[['A','D','توقيع المشرف",
    " cell(tot+1,0,'عدد الفواتير بدون فاتورة ورقية: '+L.filter(cNp).length,st({b:1,sz:11,c:'C00000',nb:1}));merges.push(`A${tot+1}:K${tot+1}`);HT[tot+1]=20;\n const sg=tot+3;[['A','D','توقيع المشرف")
rep("const W=[5,11,7,30,10,27,12,14,17,10,30];", "const W=[5,11,7,45,10,27,12,14,17,10,30];")
# edit screen: whole sentence visible under the description field
rep("<input list=\"cdl\" data-cf=\"desc\" value=\"${esc(d.desc)}\"></label>",
    "<input list=\"cdl\" data-cf=\"desc\" value=\"${esc(d.desc)}\"><small class=\"cdsp\"${String(d.desc||'').length>30?'':' hidden'}>${esc(d.desc)}</small></label>")
JS.append(r"""// ---------- v3.4: custody — invoices without a paper invoice ----------
const cNp=x=>!!x&&(x.note||'').includes(NOPAPER);
function cNpN(M){return ((M||cMo()).items||[]).filter(x=>!x.qt&&cNp(x)).length}
let CNP=null;
function cShClose(){document.querySelectorAll('.csh').forEach(x=>x.remove())}
function cShOpen(mode){cShClose();const n=cNpN(),el=document.createElement('div');el.className='csh';
 el.innerHTML=`<div class="cshb"><b>${mode=='share'?'مشاركة':'حفظ'} — عهدة شهر ${cMoLab(CU().cur)}</b>
 <button class="pr" data-cxl="${mode}">${ic('sheet')}Excel العهدة</button><button class="pr" data-cpdf="${mode}">${ic('file')}PDF العهدة</button>
 <button class="pr" data-cnpk="${mode}:all">${ic('layers')}العهدة كاملة: Excel + PDF + فواتير بدون ورقي (${n})</button>
 <button data-cnpk="${mode}:np">${ic('img')}فواتير بدون ورقي بس (${n})</button>
 <button data-capx="${mode}">${ic('img')}صور كل الفواتير PDF</button>
 <button data-cshx="1">إلغاء</button></div>`;document.body.appendChild(el)}
function cNpOpen(mode,kind){const L=cMo().items.filter(x=>!x.qt);CNP={mode,kind,sel:new Set(L.filter(cNp).map(x=>x.id))};cNpDraw()}
function cNpDraw(){cShClose();const L=cMo().items.filter(x=>!x.qt),el=document.createElement('div');el.className='csh';
 el.innerHTML=`<div class="cshb"><b>${CNP.kind=='all'?'العهدة كاملة + ':''}فواتير بدون ورقي</b><small>المعلّم عليها «لا توجد فاتورة ورقية» متعلّمة لوحدها. شيل أو ضيف أي فاتورة.</small>
 <div class="cnpl">${L.map((x,i)=>`<label class="cnpi${cNp(x)?' np':''}"><input type="checkbox" data-cnps="${x.id}"${CNP.sel.has(x.id)?' checked':''}><b>م ${i+1}</b><span>${esc(x.desc)}<small>${esc(x.comp)} · ${f2(x.amt)}${cNp(x)?' · ⚠ بدون ورقي':''}</small></span>${(x.imgs||[]).length?'<i>📎</i>':'<i class="no">بدون صورة</i>'}</label>`).join('')||'<p class="em">مفيش فواتير في الشهر ده.</p>'}</div>
 <div class="cshr"><button class="pr" data-cnpgo="1">${CNP.mode=='share'?'مشاركة':'حفظ'} (<span id="cnpn">${CNP.sel.size}</span> فاتورة)</button><button data-cshx="1">إلغاء</button></div></div>`;document.body.appendChild(el)}
async function cNpGo(){const{mode,kind,sel}=CNP,k=CU().cur,M=CU().m[k],L=M.items.filter(x=>!x.qt),S=L.map((x,i)=>({x,i:i+1})).filter(y=>sel.has(y.x.id));
 if(kind=='np'&&!S.length)return alert('ما اخترتش أي فاتورة');
 const miss=S.filter(y=>!(y.x.imgs||[]).length).map(y=>'م '+y.i);
 if(miss.length&&!confirm(`⚠ الفواتير دي من غير صورة ولا PDF: ${miss.join('، ')}\nمش هتطلع في الملف. تكمل؟`))return;
 cShClose();CNP=null;if(!cQtOk())return;if(M){M.xat=nowIso();svq()}
 const F=[],ttl=(kind=='all'?'عهدة شهر ':'فواتير بدون فاتورة ورقية — شهر ')+cMoLab(k),t=toast('جاري تجهيز الملفات…');
 try{if(kind=='all'){const bl=custXlsx(k);F.push(new File([bl],cName(k,'xlsx'),{type:bl.type}));F.push(new File([await buildPdf(custPdfEl(k),'كشف مصروفات العهدة — شهر '+cMoLab(k))],cName(k,'pdf'),{type:'application/pdf'}))}
  if(S.length){const o=await cAppEl(k,new Set(S.map(y=>y.x.id)));if(o.n)F.push(new File([await buildPdf(o.el,'فواتير بدون فاتورة ورقية — شهر '+cMoLab(k))],cName(k,'pdf').replace(/^عهدة/,'فواتير بدون ورقي عهدة'),{type:'application/pdf'}));
   for(const y of o.pdfs){const b=await idbGet(y.key);if(b)F.push(new File([b],cSafe('فاتورة م '+y.i+(y.j?'-'+y.j:'')+' - '+y.x.desc+' - '+y.x.comp)+'.pdf',{type:'application/pdf'}))}}}
 catch(e){console.error(e)}finally{t.remove()}
 if(!F.length)return alert('ما قدرتش أجهز الملفات');if(mode=='share')return shareFiles(F,ttl);
 for(const f of F){if(CAPN())await nativeSave(f.name,f,f.type,false);else{dl(f.name,f,f.type);await new Promise(r=>setTimeout(r,350))}}toastT('✓ اتحفظ '+F.length+' ملف')}
function v34CustClick(d,b){
 if(d.cmenu){cShOpen(d.cmenu);return 1}
 if(d.cshx){cShClose();CNP=null;return 1}
 if(d.cnpk){const[m,k]=d.cnpk.split(':');cNpOpen(m,k);return 1}
 if(d.cnpgo){cNpGo();return 1}
 if(d.cnpf){V.cnpf=!V.cnpf;render();return 1}
 if(b.closest('.csh')&&(d.cxl||d.cpdf||d.capx))cShClose();
 return 0}
document.addEventListener('change',e=>{const x=e.target;if(!x||!x.dataset||!x.dataset.cnps||!CNP)return;const id=isNaN(+x.dataset.cnps)?x.dataset.cnps:+x.dataset.cnps;const L=cMo().items,it=L.find(y=>String(y.id)==String(x.dataset.cnps));if(!it)return;if(x.checked)CNP.sel.add(it.id);else CNP.sel.delete(it.id);const n=document.getElementById('cnpn');if(n)n.textContent=CNP.sel.size});
document.addEventListener('input',e=>{const x=e.target;if(!x||!x.dataset||x.dataset.cf!='desc')return;const p=x.parentElement.querySelector('.cdsp');if(p){p.textContent=x.value;p.hidden=x.value.length<=30}});
""")
rep("if(usrClick(d,b)||custClick(d,b)||", "if(usrClick(d,b)||v34CustClick(d,b)||custClick(d,b)||")
CSS.append(".ckpi .cnpk{grid-column:1/-1;display:grid;gap:2px;text-align:center;background:#FDE2E2;border:1px solid #F3B5B5;border-radius:10px;padding:8px;color:#8B0000;box-shadow:none}.ckpi .cnpk small{color:#8B0000;font-weight:800}.ckpi .cnpk b{font-size:20px;color:#C00000}.ckpi .cnpk em{font-style:normal;font-size:11px;color:#8B0000;opacity:.8}.ckpi .cnpk.on{outline:2px solid #C00000}"
           ".c2b{display:grid;grid-template-columns:1fr 1fr;gap:8px}"
           ".csh{position:fixed;inset:0;z-index:60;background:rgba(5,12,24,.55);display:flex;align-items:flex-end;justify-content:center}.cshb{background:var(--c);color:var(--tx);width:100%;max-width:560px;max-height:88vh;overflow:auto;border-radius:18px 18px 0 0;padding:14px;display:grid;gap:8px;box-shadow:var(--sh-lg)}.cshb>b{font-size:16px}.cshb>small{color:var(--mu)}.cshb>button{justify-content:flex-start}"
           ".cnpl{display:grid;gap:4px;max-height:52vh;overflow:auto;border:1px solid var(--ln);border-radius:10px;padding:4px}.cnpi{display:flex;align-items:center;gap:8px;padding:8px;border-radius:8px;font-weight:600}.cnpi.np{background:#FDE2E2;color:#5A0B0B}.cnpi input{width:20px;height:20px;flex:none}.cnpi b{flex:none;min-width:38px}.cnpi span{flex:1;min-width:0}.cnpi span small{display:block;opacity:.75;font-size:11px}.cnpi i{font-style:normal;font-size:11px}.cnpi i.no{color:#C00000;font-weight:800}.cshr{display:grid;grid-template-columns:2fr 1fr;gap:8px;position:sticky;bottom:-14px;background:var(--c);padding:6px 0}"
           ".ctab th.cdsc{width:44%}.ctab td:nth-child(3){text-align:start}table.cpdf th.cdsc{width:22%}.cnpline{margin-top:6px;font-size:10px;font-weight:800;color:#C00000;text-align:start}.cdsp{display:block;white-space:normal;word-break:break-word;color:var(--tx);background:var(--c2);border-radius:8px;padding:6px 8px;margin-top:4px;font-weight:600}")
EN.update({'بدون فاتورة ورقية':'Without a paper invoice','اضغط لعرضهم بس':'Tap to show only these','✓ معروضين بس · اعرض الكل':'✓ Only these shown · show all','مشاركة…':'Share…','حفظ…':'Save…','Excel العهدة':'Custody Excel','PDF العهدة':'Custody PDF','فواتير بدون ورقي بس':'Only invoices without paper','صور كل الفواتير PDF':'All invoice photos PDF','إلغاء':'Cancel','فواتير بدون ورقي':'Invoices without paper','عدد الفواتير بدون فاتورة ورقية:':'Invoices without a paper invoice:','بدون صورة':'No photo'})

# =====================================================================
# write
# =====================================================================
JSA = '\n'.join(JS)
rep("// ---------- v1.5 extras ----------", JSA + "// ---------- v1.5 extras ----------")
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}\n" + ''.join(CSS) + "\n")
if os.environ.get('V34_FINAL') == '1':
    rep("VER='v3.3'", "VER='v3.4'")
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')

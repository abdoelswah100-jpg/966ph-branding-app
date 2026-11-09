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
# 2. custody handover (تسليم العهدة): save files, stamp, lock, next month with the remaining; reopen / deliver again
# =====================================================================
rep("<div class=\"cshare c2b\"><button class=\"pr\" data-cmenu=\"share\">${ic('share')}مشاركة…</button><button data-cmenu=\"save\">${ic('download')}حفظ…</button></div>",
    "<div class=\"cshare c2b\"><button class=\"pr\" data-cmenu=\"share\">${ic('share')}مشاركة…</button><button data-cmenu=\"save\">${ic('download')}حفظ…</button></div>${cDlBtn(M)}")
rep(" <div class=\"cbtn\"><button class=\"pr\" data-cscan=\"1\">${ic('cam')}امسح QR بالكاميرا</button>",
    " ${cDlStamp(M)}<div class=\"cbtn\"${cLk(M)?' hidden':''}><button class=\"pr\" data-cscan=\"1\">${ic('cam')}امسح QR بالكاميرا</button>")
rep("<div class=\"cnpline\">عدد الفواتير بدون فاتورة ورقية: <b>${L.filter(cNp).length}</b></div>",
    "<div class=\"cnpline\">عدد الفواتير بدون فاتورة ورقية: <b>${L.filter(cNp).length}</b>${M.dl?` · تاريخ التسليم: <b>${cDd(M.dl.at)}</b>`:''}</div>")
rep("cell(tot+1,0,'عدد الفواتير بدون فاتورة ورقية: '+L.filter(cNp).length,",
    "cell(tot+1,0,'عدد الفواتير بدون فاتورة ورقية: '+L.filter(cNp).length+(M.dl?'     ·     تاريخ التسليم: '+cDd(M.dl.at):''),")
JS.append(r"""// ---------- v3.4: custody handover ----------
const cDd=iso=>String(iso||'').slice(0,10).split('-').reverse().join('-');
const cLk=M=>!!(M&&M.dl&&!M.reo);
const cSig=M=>JSON.stringify((M.items||[]).map(x=>[x.id,x.dt,x.tm,x.desc,x.comp,x.kind,x.amt,x.note,x.car,x.ph,x.ref,x.qt,(x.imgs||[]).length]).concat([M.open]));
function cDlStamp(M){if(!M||!M.dl)return '';const ch=M.dl.sig&&cSig(M)!=M.dl.sig;
 return `<div class="cdlv${M.reo?' re':''}"><b>✓ تم التسليم ${cDd(M.dl.at)}</b>${M.reo?`<small>مفتوحة للتعديل${ch?' · اتعدّلت بعد التسليم':''}. لما تخلص اضغط «إعادة التسليم».</small>`:'<small>العهدة دي مقفولة. لو المحاسب طلب تعديل افتحها.</small>'}${M.reo?'':'<button data-cdreo="1">'+ic('edit')+'فتح للتعديل</button>'}</div>`}
function cDlBtn(M){if(!M)return '';if(!M.dl)return `<button class="pr cdlb" data-cdl="1">✅ تسليم العهدة</button>`;if(M.reo)return `<button class="pr cdlb" data-cdl="re">✅ إعادة التسليم</button>`;return ''}
function cDlOpen(re){cShClose();const C=CU(),k=C.cur,M=C.m[k],L=M.items.filter(x=>!x.qt),r=cRem(M),nk=cNext(k),sg=r>C.cfg.min?r:C.cfg.base,np=L.filter(cNp),miss=L.map((x,i)=>({x,i:i+1})).filter(y=>cNp(y.x)&&!(y.x.imgs||[]).length).map(y=>'م '+y.i),Q=cQts().length,ex=C.m[nk]&&C.m[nk].items.length;
 const el=document.createElement('div');el.className='csh';el.dataset.re=re?'1':'';
 el.innerHTML=`<div class="cshb"><b>${re?'إعادة تسليم':'تسليم'} عهدة شهر ${cMoLab(k)}</b>
 <div class="cdls"><span>عدد الفواتير <b>${L.length}</b></span><span>الإجمالي <b class="c-exp">${f2(cTot(M))}</b></span><span>المتبقي <b class="c-rem">${f2(r)}</b></span><span>بدون فاتورة ورقية <b>${np.length}</b></span></div>
 ${miss.length?`<div class="alr"><small>⚠ فواتير بدون ورقي ومفيهاش صورة ولا PDF: ${miss.join('، ')}</small></div>`:''}${Q?`<div class="alr"><small>⚠ فيه ${Q} عرض سعر مستني فاتورة.</small></div>`:''}
 <small>هيتحفظ: Excel العهدة + PDF العهدة + فواتير بدون ورقي (${np.length})، ومكتوب فيهم تاريخ التسليم.</small>
 ${re?(M.dl&&M.dl.nx&&C.m[M.dl.nx]?`<small>لو المتبقي اتغيّر هسألك تحدّث رصيد بداية ${cMoLab(M.dl.nx)}.</small>`:''):`<div class="cdln"><b>العهدة الجديدة: شهر ${cMoLab(nk)}</b>${ex?`<small>⚠ شهر ${cMoLab(nk)} فيه فواتير. هيتغيّر رصيد بدايته بس.</small>`:''}
 <label class="chk"><input type="radio" name="cdlo" value="${r}"${sg==r?' checked':''}> ابدأ بالمتبقي <b>${f2(r)}</b></label><label class="chk"><input type="radio" name="cdlo" value="${C.cfg.base}"${sg==r?'':' checked'}> ابدأ بالعهدة كاملة <b>${f2(C.cfg.base)}</b></label><label class="chk"><input type="radio" name="cdlo" value="v"> مبلغ تاني <input type="number" inputmode="decimal" id="cdlv" style="max-width:130px"></label>
 <small>${r>C.cfg.min?`المتبقي أكتر من ${f2(C.cfg.min)}، فالاقتراح يبدأ بالمتبقي.`:`المتبقي أقل من ${f2(C.cfg.min)}، فالاقتراح يبدأ بالعهدة كاملة.`}</small></div>`}
 <div class="cshr c3"><button class="pr" data-cdgo="share">${re?'إعادة التسليم':'تسليم'} ومشاركة</button><button class="pr" data-cdgo="save">${re?'إعادة التسليم':'تسليم'} وحفظ</button><button data-cshx="1">إلغاء</button></div></div>`;document.body.appendChild(el)}
async function cFiles(mode,kind,ids,k){const M=CU().m[k],L=M.items.filter(x=>!x.qt),S=L.map((x,i)=>({x,i:i+1})).filter(y=>ids.has(y.x.id));
 const F=[],ttl=(kind=='all'?'عهدة شهر ':'فواتير بدون فاتورة ورقية — شهر ')+cMoLab(k),t=toast('جاري تجهيز الملفات…');
 try{if(kind=='all'){const bl=custXlsx(k);F.push(new File([bl],cName(k,'xlsx'),{type:bl.type}));F.push(new File([await buildPdf(custPdfEl(k),'كشف مصروفات العهدة — شهر '+cMoLab(k))],cName(k,'pdf'),{type:'application/pdf'}))}
  if(S.length){const o=await cAppEl(k,new Set(S.map(y=>y.x.id)));if(o.n)F.push(new File([await buildPdf(o.el,'فواتير بدون فاتورة ورقية — شهر '+cMoLab(k))],cName(k,'pdf').replace(/^عهدة/,'فواتير بدون ورقي عهدة'),{type:'application/pdf'}));
   for(const y of o.pdfs){const b=await idbGet(y.key);if(b)F.push(new File([b],cSafe('فاتورة م '+y.i+(y.j?'-'+y.j:'')+' - '+y.x.desc+' - '+y.x.comp)+'.pdf',{type:'application/pdf'}))}}}
 catch(e){console.error(e)}finally{t.remove()}
 if(!F.length){alert('ما قدرتش أجهز الملفات');return 0}if(mode=='share'){await shareFiles(F,ttl);return F.length}
 for(const f of F){if(CAPN())await nativeSave(f.name,f,f.type,false);else{dl(f.name,f,f.type);await new Promise(r=>setTimeout(r,350))}}toastT('✓ اتحفظ '+F.length+' ملف');return F.length}
async function cDlGo(mode){const sh=document.querySelector('.csh'),re=sh&&sh.dataset.re=='1',C=CU(),k=C.cur,M=C.m[k];if(!M)return;
 let v=null;if(!re){const o=document.querySelector('input[name=cdlo]:checked');v=o?(o.value=='v'?parseFloat(($('#cdlv')||{}).value):+o.value):NaN;if(!(v>=0))return alert('اكتب مبلغ بداية العهدة الجديدة')}
 if(!cQtOk())return;cShClose();const r0=M.dl?M.dl.rem:null;
 M.dl=Object.assign(M.dl||{},{at:nowIso(),rem:cRem(M),tot:cTot(M)});delete M.reo;M.dl.sig=cSig(M);M.xat=nowIso();sv();
 const ids=new Set(M.items.filter(x=>!x.qt&&cNp(x)).map(x=>x.id));await cFiles(mode,'all',ids,k);
 if(!re){const nk=cNext(k);C.m[nk]=C.m[nk]||{items:[]};C.m[nk].open=Math.round(v*100)/100;C.m[nk].why=Math.abs(v-cRem(M))<.005?'المتبقي من شهر '+cMoLab(k):'';M.dl.nx=nk;M.dl.ov=C.m[nk].open;C.cur=nk;V.cnew=false;V.cnpf=false;sv();render();toastT('✓ اتسلمت عهدة '+cMoLab(k)+' وبدأت عهدة '+cMoLab(nk));return}
 const nx=M.dl.nx,N=nx&&C.m[nx],r=cRem(M);
 if(N&&r0!=null&&Math.abs(r-r0)>.004&&Math.abs((+N.open||0)-(+M.dl.ov||0))<.005&&Math.abs((+M.dl.ov||0)-r0)<.005&&confirm(`رصيد بداية ${cMoLab(nx)} كان ${f2(N.open)} (المتبقي القديم)، والمتبقي بعد التعديل بقى ${f2(r)}. تحدّثه؟`)){N.open=Math.round(r*100)/100;M.dl.ov=N.open}
 sv();render();toastT('✓ اتعادت تسليم عهدة '+cMoLab(k))}
function v34DlClick(d,b){
 if(d.cdl){cDlOpen(d.cdl=='re');return 1}
 if(d.cdgo){cDlGo(d.cdgo);return 1}
 if(d.cdreo){const M=cMo();if(confirm('تفتح عهدة شهر '+cMoLab(CU().cur)+' للتعديل؟ بعد ما تخلص التعديلات اضغط «إعادة التسليم».')){M.reo=1;sv();render()}return 1}
 if(V.v=='cust'&&cLk(cMo())&&(d.cscan||d.cman||d.ced||(d.cnew&&d.cnew!=='0')||(d.pick&&/^c(imgs|json)$/.test(d.pick)))){toastT('🔒 عهدة '+cMoLab(CU().cur)+' اتسلمت. اضغط «فتح للتعديل» الأول');return 1}
 return 0}
""")
rep("if(usrClick(d,b)||v34CustClick(d,b)||", "if(usrClick(d,b)||v34DlClick(d,b)||v34CustClick(d,b)||")
CSS.append(".cdlv{display:grid;gap:4px;background:#E3F4E8;border:1px solid #9ED3AE;color:#145A2E;border-radius:12px;padding:10px;margin:8px 0}.cdlv b{font-size:15px}.cdlv.re{background:#FFF4D6;border-color:#E9C46A;color:#6B4C00}.cdlv button{justify-self:start}"
           ".cdlb{width:100%;margin-top:8px;background:#1E7B45!important;border-color:#1E7B45!important;color:#fff!important}"
           ".cdls{display:grid;grid-template-columns:1fr 1fr;gap:6px}.cdls span{background:var(--c2);border:1px solid var(--ln);border-radius:10px;padding:8px;display:grid;text-align:center;font-size:12px;color:var(--mu);font-weight:700}.cdls b{font-size:16px;color:var(--tx)}"
           ".cdln{display:grid;gap:6px;border:1px dashed var(--gold);border-radius:12px;padding:10px}.cdln label.chk{display:flex;align-items:center;gap:8px}.cshr.c3{grid-template-columns:1fr 1fr 1fr}")
EN.update({'✅ تسليم العهدة':'✅ Hand over custody','✅ إعادة التسليم':'✅ Hand over again','فتح للتعديل':'Open for editing','تم التسليم':'Handed over','تاريخ التسليم:':'Handover date:'})

# =====================================================================
# 3. bottom bar: «الصيانة» instead of «النسخ» (moved to the menu); maintenance tab; home = branding pharmacies only
# =====================================================================
rep("['revhub','مراجعة','eye','t-rev'],['bk','النسخ','db','']];", "['revhub','مراجعة','eye','t-rev'],['mnt','الصيانة','wrench','']];")
rep("mnt:'',med:''", "mnt:'mnt',med:'mnt'")
rep("bk:'bk',sync:'bk'", "bk:'',sync:''")
rep("lang:'',imp:'bk'", "lang:'',imp:''")
rep("atb:'bk'}", "atb:''}")
rep("const MENU=[['all','التقارير','layers'],", "const MENU=[['all','التقارير','layers'],['bk','النسخ والاستيراد','db'],")
rep("['cust','العهدة','sheet'],['mnt','الصيانة','check'],", "['cust','العهدة','sheet'],")
rep("${MENU.map(m=>`<button data-mgo=\"${m[0]}\">${ic(m[2])}${m[1]}</button>`).join('')}",
    "${MENU.map(m=>`<button data-mgo=\"${m[0]}\">${ic(m[2])}${m[1]}${m[0]=='bk'&&DB.cfg.ue?`<i class=\"mnb\">${DB.cfg.ue}</i>`:''}</button>`).join('')}")
rep("<button class=\"hmb\" data-menu=\"1\" aria-label=\"القائمة\">${ic('menu')}</button>", "<button class=\"hmb\" data-menu=\"1\" aria-label=\"القائمة\">${ic('menu')}${DB&&DB.cfg&&DB.cfg.ue?'<i class=\"hmnb\"></i>':''}</button>")
rep("if(V.v=='bk'){a.innerHTML=hdr('','النسخ')", "if(V.v=='bk'){a.innerHTML=hdr(backBtn(),'النسخ')")
rep("if(V.v=='mnt'){a.innerHTML=hdr(backBtn(),'الصيانة')", "if(V.v=='mnt'){a.innerHTML=hdr('','🔧 الصيانة')")
rep("function mntHtml(){const C=MU()", "function mntHtml0(){const C=MU()")
# home: branding pharmacies only (maintenance ones live in the maintenance tab)
rep(" const L=DB.ph.filter(p=>(!t||[p.no,p.rg,p.ct,p.name].join(' ').toLowerCase().includes(t))&&(!q.st||p.st==q.st)&&(!q.mo||p.mo==q.mo)).sort(pSort);\n const hc=$('#hcnt');if(hc)hc.textContent=`${DB.ph.length} صيدلية مسجلة · ${L.length} معروضة في البحث`;",
    " const L=DB.ph.filter(p=>isBr(p)&&(!t||[p.no,p.rg,p.ct,p.name].join(' ').toLowerCase().includes(t))&&(!q.st||p.st==q.st)&&(!q.mo||p.mo==q.mo)).sort(pSort);\n const hc=$('#hcnt');if(hc)hc.textContent=`${DB.ph.filter(isBr).length} صيدلية دعاية${t||q.st||q.mo?' · '+L.length+' معروضة':''}${DB.ph.some(isMnt)?' · صيدليات الصيانة في تاب «الصيانة»':''}`;")
# compact home card + sync alert as a small bar that opens
rep("function homeHtml(){const n=DB.ph.length;return vAskHtml()+`<div class=\"hcard\"><div class=\"hc-top\"><span class=\"hc-ic\">${ic('bld')}</span><div><h2>إدارة ومتابعة الصيدليات</h2><small id=\"hcnt\">${n} صيدلية مسجلة · ${n} معروضة في البحث</small></div></div><button class=\"hc-calc\" data-tab=\"calc\">${ic('calc')}حاسبة الأمتار الذكية</button><button class=\"hc-calc\" data-rtgo=\"\">${ic('pin')}جدول السير (من أرقام الصيدليات)</button><div class=\"hc-sep\"></div><button class=\"hc-add\" data-newp=\"1\">${ic('add')}إضافة صيدلية جديدة</button><p class=\"hc-hint\">اضغط هنا لإدراج صيدلية جديدة وحفظ بياناتها مباشرة</p></div>${[bkBanner(),syncBanner()].filter(x=>x.startsWith('<div class=\"alr\"')).join('')}",
    "function homeHtml(){const n=DB.ph.filter(isBr).length;return vAskHtml()+`<div class=\"hcard hc2\"><div class=\"hc-row\"><button class=\"hc-add\" data-newp=\"1\">${ic('add')}صيدلية جديدة</button><button class=\"hc-ib\" data-tab=\"calc\">${ic('calc')}<i>الحاسبة</i></button><button class=\"hc-ib\" data-rtgo=\"\">${ic('pin')}<i>جدول السير</i></button></div><small id=\"hcnt\">${n} صيدلية دعاية</small></div>${[bkBanner()].filter(x=>x.startsWith('<div class=\"alr\"')).join('')}${syncChip()}")
JS.append(r"""// ---------- v3.4: maintenance tab, compact home, sync bar ----------
ICN.wrench='<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>';
function syncChip(){const h=syncBanner();if(!h.startsWith('<div class="alr"'))return '';const n=pendingN();return `<details class="schip" data-id="__sch"${V.op.__sch?' open':''}><summary>⚠ المزامنة: ${n?n+' صيدلية معدلة لسه ما اتصدّرتش':'آخر استيراد قديم'}<small>التفاصيل ›</small></summary>${h}</details>`}
function mntPhHtml(){const t=String(V.mpq||'').trim().toLowerCase(),A=DB.ph.filter(isMnt),L=A.filter(p=>!t||[p.no,p.rg,p.ct,p.name].join(' ').toLowerCase().includes(t)).sort(pSort),cur=MN(),g={};L.forEach(p=>{(g[p.mo||'—']=g[p.mo||'—']||[]).push(p)});const ks=Object.keys(g).sort().reverse();
 return `<div class="hcard hc2"><div class="hc-row"><button class="hc-add" data-newpm="1">${ic('add')}صيدلية صيانة</button><button class="hc-ib" data-madd="1">${ic('wrench')}<i>صيانة جديدة</i></button></div><small>${A.length} صيدلية صيانة</small></div>
 <details class="mg lst" data-id="__mph"${V.op.__mph||t?' open':''}><summary><span>🔧 صيدليات الصيانة</span><i>${A.length}</i></summary><div class="mgb"><input class="sf" id="mpq" placeholder="🔍 بحث برقم الصيدلية أو المنطقة" value="${esc(V.mpq||'')}">${ks.map(k=>{const a=g[k],open=!!t||!!V.op['mm_'+k];return `<details class="mg" data-id="mm_${k}"${open?' open':''}><summary><span>${k==cur?'الشهر الحالي':'شهر'} ${k}</span><i>${a.length}</i></summary><div class="mgb"><small>مكتملة ${a.filter(p=>p.st=='مكتملة').length} من ${a.length}</small>${a.map(pCard).join('')}</div></details>`}).join('')||'<p class="em">'+(t?'مفيش نتائج.':'لسه مفيش صيدليات صيانة. اضغط «صيدلية صيانة».')+'</p>'}</div></details>`}
function mntHtml(){const C=MU(),n=mList(C.cur).length;return mntPhHtml()+`<details class="mg lst" data-id="__mrep"${V.op.__mrep||V.mqf?' open':''}><summary><span>📋 كشف الصيانات · ${mQLab(C.cur)}</span><i>${n}</i></summary><div class="mgb">${mntHtml0()}</div></details>`}
function v34Click(d,b){
 if(d.newpm){goV({v:'add',op:{},dr:{},q:V.q});setTimeout(()=>{const m=$('#pmod');if(m&&[...m.options].some(o=>o.value=='صيانة')){m.value='صيانة';m.dispatchEvent(new Event('change',{bubbles:true}))}const x=$('#pno');if(x)x.focus()},60);return 1}
 return 0}
function v34Change(x){
 if(x.id=='mpq'){V.mpq=x.value;render();const i=$('#mpq');if(i){i.focus();i.setSelectionRange(i.value.length,i.value.length)}return 1}
 return 0}
""")
rep("if(tr&&!b){custClick({ced:tr.dataset.ced});return}", "if(tr&&!b){if(!v34DlClick({ced:tr.dataset.ced},tr))custClick({ced:tr.dataset.ced});return}")
rep("v33Click(d,b)||rlClick(d)", "v33Click(d,b)||v34Click(d,b)||rlClick(d)")
rep("v33Change(x)||rlChange(x)", "v33Change(x)||v34Change(x)||rlChange(x)")
CSS.append(".hc2{padding:12px;gap:8px}.hc-row{display:flex;gap:8px;align-items:stretch}.hc-row .hc-add{flex:1;padding:14px;font-size:17px}.hc-ib{flex:none;width:76px;flex-direction:column;gap:2px;justify-content:center;background:#0A1A32;color:#FFC93C;border:1px solid rgba(201,162,39,.65);border-radius:14px;padding:6px;font-weight:800;font-size:11.5px}.hc-ib svg{width:22px;height:22px}.hc-ib i{font-style:normal}.hc2>small{color:rgba(255,255,255,.82);font-size:12.5px}"
           ".schip{margin:8px 0;border:1px solid #F3B5B5;background:#FDECEC;border-radius:12px}.schip>summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 12px;color:#8B0000;font-weight:800;font-size:13px}.schip>summary::-webkit-details-marker{display:none}.schip>summary small{font-weight:700;opacity:.8;white-space:nowrap}.schip>.alr{margin:0 8px 8px}"
           ".mg.lst>summary{font-size:16px}.hmb{position:relative}.hmnb{position:absolute;top:6px;inset-inline-end:6px;width:10px;height:10px;border-radius:50%;background:#C7313B;border:2px solid var(--nav)}.mnb{font-style:normal;background:#C7313B;color:#fff;border-radius:10px;padding:0 7px;font-size:11px;margin-inline-start:auto}")
EN.update({'الصيانة':'Maintenance','صيدلية جديدة':'New pharmacy','الحاسبة':'Calculator','جدول السير':'Route','صيدلية صيانة':'Maintenance pharmacy','صيانة جديدة':'New maintenance','🔧 صيدليات الصيانة':'🔧 Maintenance pharmacies','النسخ والاستيراد':'Backup and import','صيدلية دعاية':'branding pharmacies','التفاصيل ›':'Details ›'})

# =====================================================================
# 4. pharmacy screen: empty types folded, tools folded; execution cards; warehouse header
# =====================================================================
rep("${TY(p).map(t=>card(t,p)).join('')}<button class=\"pr\" data-sum=\"1\">عرض الملخص / التقرير</button><button data-qe=\"0\">⚡ إدخال سريع (نوع دعاية في كل شاشة)</button><button data-ckv=\"1\">Checklist الاستلام</button><button data-save=\"1\">حفظ ملف الصيدلية</button><button data-cp=\"1\">نسخ الصيدلية</button><button data-tps=\"1\">حفظ كقالب</button>${tplUI()}</main>`",
    "${phCards(p)}<button class=\"pr\" data-sum=\"1\">عرض الملخص / التقرير</button><button data-qe=\"0\">⚡ إدخال سريع (نوع دعاية في كل شاشة)</button><details class=\"pinfo ptl\" data-id=\"__ptl\"${V.op.__ptl?' open':''}><summary>⋯ أدوات الصيدلية <small>Checklist · حفظ · نسخ · قالب</small></summary><div class=\"fm\"><button data-ckv=\"1\">Checklist الاستلام</button><button data-save=\"1\">حفظ ملف الصيدلية</button><button data-cp=\"1\">نسخ الصيدلية</button><button data-tps=\"1\">حفظ كقالب</button>${tplUI()}</div></details></main>`")
JS.append(r"""// ---------- v3.4: pharmacy screen — types with items first, the empty ones folded ----------
function phCards(p){const A=TY(p),fo=V.fo||{},F=A.filter(t=>t.auto||(p.rows[t.id]||[]).length||V.op[t.id]||fo[t.id]||(V.dr&&V.dr[t.id]&&V.ed&&String(V.ed).startsWith(t.id+':'))),E=A.filter(t=>!F.includes(t));
 return F.map(t=>card(t,p)).join('')+(E.length?`<details class="pinfo pemp" data-id="__pem"${V.op.__pem?' open':''}><summary>${ic('add')} باقي الأنواع (${E.length})<small>${E.map(t=>esc(t.n)).join(' · ')}</small></summary>${E.map(t=>card(t,p)).join('')}</details>`:'')}
""")
CSS.append(".pemp>summary,.ptl>summary{display:flex;flex-wrap:wrap;align-items:center;gap:6px}.pemp>summary small,.ptl>summary small{flex-basis:100%;color:var(--mu);font-weight:600;font-size:11.5px;line-height:1.5}.pemp{margin-top:6px}.ptl .fm{display:grid;gap:8px}"
           ".xrow .xn{flex:1;min-width:0}.xrow .xp{flex:0 0 46%;min-width:0}.xrow .xp small{line-height:1.5}")
EN.update({'باقي الأنواع':'Other types','⋯ أدوات الصيدلية':'⋯ Pharmacy tools'})
# warehouse: one line of numbers; filters folded
rep("<div class=\"ckpi\"><div><small>عدد الأصناف</small><b>${W0.length}</b></div><div><small>إجمالي القطع</small><b>${wq(W0.filter(x=>x.unit!='متر').reduce((a,x)=>a+(+x.qty||0),0))}</b></div><div><small>إجمالي الأمتار</small><b>${wq(W0.filter(x=>x.unit=='متر').reduce((a,x)=>a+(+x.qty||0),0))}</b></div><div><small>آخر حركة</small><b style=\"font-size:13px\">${last?fd(last.at).slice(0,10):'—'}</b></div></div>",
    "<div class=\"whst\"><span><b>${W0.length}</b> صنف</span><span><b>${wq(W0.filter(x=>x.unit!='متر').reduce((a,x)=>a+(+x.qty||0),0))}</b> قطعة</span><span><b>${wq(W0.filter(x=>x.unit=='متر').reduce((a,x)=>a+(+x.qty||0),0))}</b> متر</span><span>آخر حركة <b>${last?fd(last.at).slice(0,10):'—'}</b></span></div>")
rep(" ${whChips(W0,F)}<div class=\"c2\"><label>نوع الدعاية<select data-whf=\"ty\">",
    " ${whChips(W0,F)}<details class=\"whfl\" data-id=\"__whf\"${V.op.__whf||F.ty||F.sec||F.mat||F.low?' open':''}><summary>${ic('filter')} فلتر${[F.ty,F.sec,F.mat,F.low].filter(Boolean).length?' ('+[F.ty,F.sec,F.mat,F.low].filter(Boolean).length+')':''}</summary><div class=\"c2\"><label>نوع الدعاية<select data-whf=\"ty\">")
rep(" <label class=\"chk\"><input type=\"checkbox\" id=\"whlow\"${F.low?' checked':''}> رصيد قليل بس</label></div>",
    " <label class=\"chk\"><input type=\"checkbox\" id=\"whlow\"${F.low?' checked':''}> رصيد قليل بس</label></details></div>")
CSS.append(".whst{display:flex;flex-wrap:wrap;gap:6px 14px;justify-content:space-between;background:var(--c2);border:1px solid var(--ln);border-radius:12px;padding:10px 12px;color:var(--mu);font-size:12.5px;font-weight:700}.whst b{color:var(--tx);font-size:15px}.whfl{margin-top:8px}.whfl>summary{cursor:pointer;font-weight:800;display:flex;align-items:center;gap:6px;padding:6px 0}.whfl>summary svg{width:18px;height:18px}")

# =====================================================================
# 5. warehouse: old stock (old design side acrylic, old gandola side acrylic, blank acrylic) + out-of-stock alert
# =====================================================================
rep("const L=W0.filter(x=>(F.sh===''||F.sh==null||x.sh==F.sh)&&", "const L=W0.filter(x=>(!F.old||x.old)&&(F.sh===''||F.sh==null||x.sh==F.sh)&&")
rep("<button class=\"${on('')?'pr':''}\" data-whsh=\"all\">الكل <small>${W.length}</small></button></div>`}",
    "<button class=\"${on('')?'pr':''}\" data-whsh=\"all\">الكل <small>${W.length}</small></button>${W.some(x=>x.old)?`<button class=\"${F.old?'pr':''} whold\" data-whold=\"1\">🕰 قديم <small>${W.filter(x=>x.old).length}</small></button>`:''}</div>`}")
rep("<div class=\"whi\"><b>${esc(x.ty)}</b>", "<div class=\"whi\"><b>${esc(x.ty)}${x.old&&!/قديم/.test(x.ty)?' <small class=\"rshc odt\">تصميم قديم</small>':''}</b>")
rep(" ${whLow()?`<div class=\"alr\"><small>⚠ ${whLow()} صنف رصيده وصل للحد الأدنى أو أقل.</small></div>`:''}",
    " ${whLow()?`<div class=\"alr\"><small>⚠ ${whLow()} صنف رصيده وصل للحد الأدنى أو أقل.</small></div>`:''}${whOutHtml()}")
rep("<button class=\"lnk\" data-whadd=\"1\">إضافة صنف بمقاس خاص (كتابة يدوي) ›</button>`}",
    "<button class=\"lnk\" data-whadd=\"1\">إضافة صنف بمقاس خاص (كتابة يدوي) ›</button><button class=\"lnk\" data-whoa=\"1\">🕰 إضافة مخزون قديم (تصميم قديم / أكريليك فاضي) ›</button>`}")
rep("return o}\nfunction whFrom(p,t,r,i){", "return o.concat(whOldOpts(p,t,r))}\nfunction whFrom(p,t,r,i){")
rep(" if(c.k=='a'){const x=WU().find(y=>y.id==c.id);if(!x||+x.qty<c.n)return;whAdd(x,-c.n,'out','ph:'+p.no,'سحب لبند في الصيدلية (مقاس تاني)');",
    " if(c.k=='o'){const x=WU().find(y=>y.id==c.id);if(!x||+x.qty<c.n)return;whAdd(x,-c.n,'out','ph:'+p.no,'سحب '+x.ty+' لبند في الصيدلية');r.wo=(+r.wo||0)+c.n;sv();tt.remove();render();return toastT('✓ اتسحب من المخزون القديم')}\n if(c.k=='a'){const x=WU().find(y=>y.id==c.id);if(!x||+x.qty<c.n)return;whAdd(x,-c.n,'out','ph:'+p.no,x.old?'سحب تصميم قديم لبند في الصيدلية':'سحب لبند في الصيدلية (مقاس تاني)');")
JS.append(r"""// ---------- v3.4: warehouse old stock + out-of-stock alert ----------
const OLDT={saw:'Side Acrylic Shelves Wall · تصميم قديم',saf:'Side Acrylic Shelves Floor · تصميم قديم',egs:'End gandola - Side أكريليك · تصميم قديم',bwh:'أكريليك فاضي · Wall Header',bfh:'أكريليك فاضي · Floor Header',beg:'أكريليك فاضي · Side جندولة'};
const OLDL={saw:'Side Acrylic رفوف جداري (تصميم قديم)',saf:'Side Acrylic رفوف أرضي (تصميم قديم)',egs:'End gandola Side أكريليك + ستيكر (تركي عادي، تصميم قديم)',bwh:'أكريليك فاضي للـ Wall Header',bfh:'أكريليك فاضي للـ Floor Header',beg:'أكريليك فاضي للـ Side جندولة'};
const OGS='100×25';
function whoSz(k,sh){if(k=='saw')return SZ('saw');if(k=='saf')return SZ('saf.'+sh);if(k=='egs'||k=='beg')return [OGS];if(k=='bwh')return (sh==2?['100']:SZ('wh.len')).map(l=>SZ('wh.h')[sh]+'×'+l);if(k=='bfh'){const a=[SZ('fh.s')[sh]];if(sh!=2&&!a.includes(SZ('fh.l')))a.push(SZ('fh.l'));return a}return []}
function whoD(){const d=V.wo=V.wo||{k:'saw',sh:2,sec:'Health',sd:'يمين',nm:'',sz:'',q:1};if(d.k=='saw')d.sh=2;if(d.k=='egs'||d.k=='beg')d.sh=0;const S=whoSz(d.k,d.sh);if(!S.includes(d.sz))d.sz=S[0]||'';if(d.k=='egs'&&!EG.includes(d.nm))d.nm=EG[0]||'';return d}
function whoHtml(){const d=whoD(),k=d.k,S=whoSz(k,d.sh),sel=(id,L,v,lab)=>`<label>${lab}<select data-wo="${id}">${L.map(x=>{const[v2,l2]=Array.isArray(x)?x:[x,x];return `<option value="${esc(v2)}"${String(v2)==String(v)?' selected':''}>${esc(l2)}</option>`}).join('')}</select></label>`;
 return `<div class="wcard"><h2>🕰 إضافة مخزون قديم</h2><p class="sub">أصناف التصميم القديم والأكريليك الفاضي بتتحفظ لوحدها بعلامة «تصميم قديم»، ومش بتتسحب لوحدها لأي بند. لما يبقى فيه بند في صيدلية بنفس المقاس البرنامج بيعرضها عليك في «📦 من المخزن».</p>
 ${sel('k',Object.keys(OLDL).map(x=>[x,OLDL[x]]),k,'الصنف')}
 ${['saf','bwh','bfh'].includes(k)?sel('sh',SH.map((x,i)=>[i,x]),d.sh,'نوع الرفوف'):`<p class="sub">نوع الرفوف: <b>${SH[d.sh]}</b></p>`}
 ${k=='saw'?sel('sec',S4.concat(['Pharmacy']),d.sec,'القسم'):k=='saf'?sel('sec',S4,d.sec,'القسم'):''}
 ${k=='egs'?sel('nm',EG,d.nm,'القسم · المسمى'):''}
 ${sel('sz',S,d.sz,'المقاس (سم)')}
 ${k=='saw'||k=='saf'?sel('sd',['يمين','يسار'],d.sd,'الجهة'):''}
 <label>العدد<input type="number" inputmode="numeric" min="1" data-wo="q" value="${esc(d.q)}"></label>
 <div class="tt"><button class="pr big" data-whosave="1">${ic('check')}حفظ في المخزن</button><button data-whox="1">رجوع</button></div></div>
 ${(()=>{const L=WU().filter(x=>x.old);return L.length?`<div class="wcard"><b>المخزون القديم (${L.length} صنف)</b>${L.map(whCard).join('')}</div>`:''})()}`}
function whoSave(){const d=whoD(),q=wq(+d.q||0);if(!(q>0))return alert('اكتب العدد');if(!d.sz)return alert('اختار المقاس');
 const o={sh:d.sh,ty:OLDT[d.k],nm:d.k=='egs'?d.nm:(d.k=='saw'||d.k=='saf')?d.sd:'',sec:(d.k=='saw'||d.k=='saf')?d.sec:'',mat:d.k[0]=='b'?'أكريليك فاضي':'أكريليك + ستيكر',size:d.sz,old:1};
 const x=whAdd(o,q,'in','manual','مخزون قديم');x.old=1;sv();snd('ok');d.q=1;render();toastT(`✓ اتضاف ${q} · ${OLDL[d.k]} · ${d.sz} (الرصيد ${wq(x.qty)})`)}
function whOldOpts(p,t,r){if(!p||p._wh||p._rc)return [];const W=WU().filter(x=>x.old&&+x.qty>=1);if(!W.length)return [];const need=Math.max(0,qn(r)-(+r.r||0)),O=[],sz=v=>String(v||'').replace(/\s+/g,''),sh=rsh(r,p.sh);
 const add=(x,n,k,lab)=>{n=Math.min(n,Math.floor(+x.qty));if(n>0)O.push({k,id:x.id,n,txt:`🕰 ${n} ${lab} (في المخزن ${wq(x.qty)})`})};
 if(need>0&&(t.id=='saw'||t.id=='saf'))W.filter(x=>x.ty==OLDT[t.id]&&(t.id=='saw'||x.sh==sh)&&x.sec==r.sec&&sz(x.size)==sz(r.sz)&&x.nm==r.sd).forEach(x=>add(x,need,'a','تصميم قديم بنفس المقاس'));
 if(need>0&&t.id=='eg'&&sh<=1){const n=PARTS.eg[1][1]*need;W.filter(x=>(x.ty==OLDT.egs&&x.nm==r.nm)||x.ty==OLDT.beg).forEach(x=>add(x,n,'o',x.ty==OLDT.egs?'سايد أكريليك تصميم قديم':'أكريليك فاضي للسايد '+OGS))}
 if(need>0&&t.id=='wh'&&!wood(r)){const s0=SZ('wh.h')[sh]+'×'+r.len;W.filter(x=>x.ty==OLDT.bwh&&x.sh==sh&&sz(x.size)==sz(s0)).forEach(x=>add(x,need,'o','أكريليك فاضي بنفس المقاس'))}
 if(need>0&&t.id=='fh'){const z=szOf(t.z(r,p.sh));W.filter(x=>x.ty==OLDT.bfh&&x.sh==sh&&sz(x.size)==sz(z)).forEach(x=>add(x,need,'o','أكريليك فاضي بنفس المقاس'))}
 return O}
function whOut(){const W=WU().filter(x=>!x.old&&+x.qty<=0),R=[];
 if(W.length){const need=[];DB.ph.forEach(p=>{if(!isBr(p)||p.st=='مكتملة'||p._wh)return;TY(p).forEach(t=>(p.rows[t.id]||[]).forEach(r=>{const n=Math.max(0,qn(r)-(+r.r||0));if(!n)return;whParts(t,r,p.sh).forEach(y=>{if(!y.pk)need.push({p,k0:whKey0(y),n:n*y.f})})}))});
  W.forEach(x=>{if(whQty(x)>0)return;const k0=whKey0(x),m={};need.filter(y=>y.k0==k0).forEach(y=>{m[y.p.no]=(m[y.p.no]||0)+y.n});const P=Object.keys(m);if(P.length&&!R.some(o=>whKey0(o.x)==k0))R.push({x,P:P.map(no=>({no,n:wq(m[no])}))})})}
 return R}
function whOutHtml(){const R=whOut();if(!R.length)return '';return `<details class="alr wout" data-id="__wout"${V.op.__wout?' open':''}><summary>⚠ ${R.length} صنف خلص من المخزن وفيه صيدليات محتاجاه <small>التفاصيل ›</small></summary>${R.map(o=>`<small>• <b>${esc(o.x.ty)}</b>${whNm(o.x)?' · '+esc(whNm(o.x)):''} · ${esc(o.x.size||'')} — ${o.P.map(y=>'صيدلية '+esc(y.no)+' ('+y.n+')').join('، ')}</small>`).join('')}<small>اطلبهم من الطباعة (نواقص الطباعة).</small></details>`}
function v34WhClick(d,b){
 if(d.whold){V.wf=V.wf||{};V.wf.old=!V.wf.old;if(V.wf.old)V.wf.sh='';render();return 1}
 if(d.whoa){V.wo=null;goV(Object.assign(V,{v:'who'}));return 1}
 if(d.whosave){whoSave();return 1}
 if(d.whox){goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});return 1}
 return 0}
function v34WhChange(x){if(!x.dataset||x.dataset.wo==null)return 0;const d=whoD(),k=x.dataset.wo;d[k]=k=='sh'?+x.value:x.value;if(k=='k'){d.sz='';if(d.k=='saf'&&d.sh==2&&false)d.sh=0}render();return 1}
""")
rep("if(usrClick(d,b)||v34DlClick(d,b)||", "if(usrClick(d,b)||v34WhClick(d,b)||v34DlClick(d,b)||")
rep("v33Change(x)||v34Change(x)||", "v33Change(x)||v34Change(x)||v34WhChange(x)||")
rep("\n if(V.v=='gd'){", "\n if(V.v=='who'){a.innerHTML=hdr('<button data-whox=\"1\">‹ المخزن</button>','🕰 مخزون قديم')+`<main>${whoHtml()}</main>`;return}\n if(V.v=='gd'){")
rep("wh:'wh',whe:'wh',", "wh:'wh',whe:'wh',who:'wh',")
CSS.append(".whold{border-style:dashed}.wout>summary{cursor:pointer;font-weight:800;display:flex;justify-content:space-between;gap:8px}.wout>summary small{white-space:nowrap}.wout small{display:block;margin-top:4px}")
EN.update({'🕰 إضافة مخزون قديم':'🕰 Add old stock','🕰 مخزون قديم':'🕰 Old stock','تصميم قديم':'Old design','أكريليك فاضي':'Blank acrylic'})

# =====================================================================
# 6. Google Drive from the web link (https, GitHub Pages): sign in with Google Identity Services, same uploads as the
#    phone (own file names), automatic read of the other device's latest file (both ways), monthly Excel
# =====================================================================
rep("const DA=()=>CP('DriveAuth');", "const DA=()=>CP('DriveAuth')||(GWEB()?GWAuth:null);")
rep("const sz=await gdPut('966-day-'+td+'.json',JSON.stringify(gdDay()));", "const sz=await gdPut(gdNm('day')+td+'.json',JSON.stringify(gdDay()));")
rep("name=n.month?'966-month-'+n.month+'.json':'966-full-'+td+'.json';", "name=n.month?gdNm('month')+n.month+'.json':gdNm('full')+td+'.json';")
rep("    gdU(o=>{o.full=td;if(n.month)o.mon=n.month;", "    if(n.month){try{const xb=xlsxAll();await gdPutBlob(name.replace(/\\.json$/,'.xlsx'),xb,xb.type)}catch(e){if(e.need)throw e;console.warn(e)}}\n    gdU(o=>{o.full=td;if(n.month)o.mon=n.month;")
rep("async function gdPrune(){const L=await gdList();for(const [k,n] of Object.entries(GDKEEP)){const A=L.filter(f=>new RegExp('^966-'+k+'-').test(f.name)).sort((a,b)=>a.name<b.name?1:-1);",
    "async function gdPrune(){const L=await gdList(),K=Object.entries(GWEB()?GDKEEPW:GDKEEP).map(([k,n])=>[k,n,'json']).concat([[GWEB()?'lapmonth':'month',12,'xlsx']]);for(const [k,n,x] of K){const A=L.filter(f=>new RegExp('^966-'+k+'-.*\\\\.'+x+'$').test(f.name)).sort((a,b)=>a.name<b.name?1:-1);")

rep("if(CAPN()&&o.on&&o.ed>=30){clearTimeout(GDE);GDE=setTimeout(()=>gdTick(),8000)}", "if((CAPN()||GWEB())&&o.on&&o.ed>=30){clearTimeout(GDE);GDE=setTimeout(()=>gdTick(),8000)}")
rep("if(x&&x.isActive)setTimeout(()=>gdTick(),2500)});setInterval(()=>gdTick(),15*60e3);\n const o=gdS();if(o.on){if(!o.mb)gdU(x=>x.mb=gdPrevM(TD()));gdTick()}}",
    "if(x&&x.isActive)setTimeout(()=>{gdPull();gdTick()},2500)});setInterval(()=>{gdPull();gdTick()},15*60e3);if(GWEB()){gwLoad().catch(()=>{});window.addEventListener('online',()=>setTimeout(()=>{gdPull();gdTick()},3000))}\n const o=gdS();if(o.on){if(!o.mb)gdU(x=>x.mb=gdPrevM(TD()));gdPull().then(()=>gdTick())}}")
rep("function gdHtml(){const o=gdS(),nat=CAPN(),L=V.gdl;", "function gdHtml0(nat){const o=gdS(),L=V.gdl;")
rep("function gdLine(btn){const o=gdS(),nat=CAPN();", "function gdLine(btn){const o=gdS(),nat=CAPN()||GWEB();")
rep("data-gdrs=\"${esc(nat?f.id:f.name)}\"", "data-gdrs=\"${esc(f.id||f.name)}\"")
rep("data-gdrr=\"${esc(nat?f.id:f.name)}\"", "data-gdrr=\"${esc(f.id||f.name)}\"")
rep("const A=L.filter(f=>f.name.startsWith('966-'+k+'-'));", "const A=L.filter(f=>f.name.startsWith('966-'+k+'-')&&/\\.json$/.test(f.name));")
rep("['month','شهرية'],['laptop','اللاب توب']]", "['month','شهرية'],['laptop','اللاب توب'],['lapfull','اللاب توب كاملة'],['lapmonth','اللاب توب شهرية']]")
rep("async function gdRestore(id,mode){const L=V.gdl||[],f=L.find(x=>(CAPN()?x.id:x.name)==id);", "async function gdRestore(id,mode){const L=V.gdl||[],f=L.find(x=>(x.id||x.name)==id);")
rep("const q=CAPN()?await gdGet(id):JSON.parse(await (await f.h.getFile()).text());", "const q=f.id?await gdGet(f.id):JSON.parse(await (await f.h.getFile()).text());")
rep("toastT('✓ اتربط Google Drive');gdTick()", "toastT('✓ اتربط Google Drive');gdPull().then(()=>gdTick())")
JS.append(r"""// ---------- v3.4: Google Drive from the web link (GitHub Pages) ----------
const GWID='1052360360258-3voqs2f8m6qteq4jjldmqp34itpl48td.apps.googleusercontent.com',GWURL='https://abdoelswah100-jpg.github.io/966ph-branding-app/';
const GWEB=()=>!CAPN()&&location.protocol=='https:';
const GDKEEPW={laptop:14,lapfull:4,lapmonth:12};
const gdNm=k=>GWEB()?{day:'966-laptop-',full:'966-lapfull-',month:'966-lapmonth-'}[k]:'966-'+k+'-';
let GWL=null;
function gwLoad(){if(window.google&&google.accounts&&google.accounts.oauth2)return Promise.resolve();if(GWL)return GWL;GWL=new Promise((ok,no)=>{const s=document.createElement('script');s.src='https://accounts.google.com/gsi/client';s.async=true;s.onload=()=>ok();s.onerror=()=>{GWL=null;s.remove();no(new Error('مفيش نت أو صفحة جوجل مش متاحة'))};document.head.appendChild(s)});return GWL}
function gwSaved(){try{const o=JSON.parse(localStorage.getItem('966gwt')||'null');if(o&&o.exp>Date.now()+60e3)return o}catch(e){}return null}
const GWAuth={async authorize(o){const s=gwSaved();if(s)return {token:s.t};if(!o||!o.interactive)return {need:1};await gwLoad();
  return await new Promise((ok,no)=>{const c=google.accounts.oauth2.initTokenClient({client_id:GWID,scope:'https://www.googleapis.com/auth/drive.file',callback:r=>{if(r&&r.access_token){const exp=Date.now()+((+r.expires_in||3600)-120)*1000;try{localStorage.setItem('966gwt',JSON.stringify({t:r.access_token,exp}));localStorage.setItem('966gwu','1')}catch(e){}ok({token:r.access_token})}else no(new Error((r&&(r.error_description||r.error))||'تسجيل الدخول ما نجحش'))},error_callback:e=>no(new Error(e&&e.type=='popup_closed'?'نافذة جوجل اتقفلت قبل ما تكمل':e&&e.type=='popup_failed_to_open'?'المتصفح منع نافذة جوجل. اسمح بالـ popups للموقع ده':(e&&e.message)||'تسجيل الدخول ما نجحش'))});let u=null;try{u=localStorage.getItem('966gwu')}catch(e){}c.requestAccessToken({prompt:u?'':'consent'})})},
 async clearToken(){try{localStorage.removeItem('966gwt')}catch(e){}}};
async function gdPutBlob(name,blob,mime){const fid=await gdFolder();const r0=await gdF('drive/v3/files?fields=files(id)&q='+gdQ("name='"+name+"' and '"+fid+"' in parents and trashed=false"));const ex=((await r0.json()).files||[])[0];
 const B='966x'+Date.now(),meta=ex?{}:{name,parents:[fid],mimeType:mime},body=new Blob(['--'+B+'\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'+JSON.stringify(meta)+'\r\n--'+B+'\r\nContent-Type: '+mime+'\r\n\r\n',blob,'\r\n--'+B+'--'],{type:'multipart/related; boundary='+B});
 await gdF('upload/drive/v3/files'+(ex?'/'+ex.id:'')+'?uploadType=multipart&fields=id',{method:ex?'PATCH':'POST',headers:{'Content-Type':'multipart/related; boundary='+B},body});return blob.size}
// read the other device's newest daily file and merge it (phone ← 966-laptop-…, web link ← 966-day-…)
let GDPB=0;
async function gdPull(manual){if(!DA()||GDPB||!DB)return;const o=gdS();if(!o.on||(o.need&&!manual))return;GDPB=1;let t=null;
 try{const net=await gdNet();if(!net.on){if(manual)alert('مفيش نت');return}if(manual)t=toast('☁️ جاري البحث عن آخر ملف…');
  const L=await gdList(),re=GWEB()?/^966-day-.*\.json$/:/^966-laptop-.*\.json$/,A=L.filter(f=>re.test(f.name)).sort((a,b)=>String(b.modifiedTime||'').localeCompare(String(a.modifiedTime||''))),f=A[0];
  if(!f){if(manual)alert(GWEB()?'مفيش ملفات من الموبايل في Drive لسه.':'مفيش ملفات من اللاب توب في Drive لسه (أو الموبايل مش شايفها).');return}
  if(!manual&&o.pf==f.id&&o.pm==f.modifiedTime)return;
  const q=await gdGet(f.id),msg=await gdApply(q,'merge','قبل دمج '+f.name+' من Google Drive');gdU(x=>{x.pf=f.id;x.pm=f.modifiedTime;x.pn=f.name;x.pt=nowIso()});render();toastT('☁️ اتدمجت آخر بيانات '+(GWEB()?'الموبايل':'اللاب توب')+' · '+msg)}
 catch(e){console.warn(e);if(e.need){if(manual)alert('محتاج تسجيل دخول Google الأول');else gdNeedNote()}else if(manual)alert('⚠ '+(e.message||e))}
 finally{GDPB=0;if(t)t.remove()}}
function gdPullHtml(){const o=gdS();if(!o.on)return '';const w=GWEB()?'الموبايل':'اللاب توب';return `<div class="wcard"><h3>☁️ بيانات ${w}</h3><small>${o.pn?'آخر دمج تلقائي: <b>'+esc(o.pn.replace(/^966-|\.json$/g,''))+'</b> · '+fd(o.pt):'لسه مفيش دمج من '+w}</small><br><small>بيتقرا ويتدمج لوحده كل ما تفتح التطبيق وكل 15 دقيقة (كل صيدلية بتاخد الأحدث، وقبلها نقطة استعادة).</small><div class="tt"><button data-gdpull="1">${ic('db')}اقرا آخر بيانات ${w} دلوقتي</button></div></div>`}
function gdHtml(){if(CAPN())return gdHtml0(true)+gdPullHtml();
 if(GWEB())return `<div class="ph"><small>🌐 فاتح التطبيق من اللينك. Google Drive بيشتغل هنا زي الموبايل بالظبط: بيرفع لوحده، وبيقرا آخر بيانات الموبايل لوحده.</small></div>`+gdHtml0(true)+gdPullHtml()+`<details class="pinfo" data-id="__gdo"${V.op.__gdo?' open':''}><summary>${ic('file')} الطريقة القديمة: فولدر Drive for desktop</summary>${gdHtml0(false)}</details>`;
 return `<div class="ywarn">💡 علشان Google Drive يشتغل لوحده على اللاب توب (يرفع ويقرا بيانات الموبايل من غير Drive for desktop) افتح التطبيق من اللينك:<br><a href="${GWURL}" target="_blank" rel="noopener" dir="ltr">${GWURL}</a><br><small>بياناتك اللي على المتصفح ده مش بتتنقل للينك لوحدها: احفظ نسخة احتياطية هنا واستوردها هناك، أو سيبه يقرا من Drive بعد الربط.</small></div>`+gdHtml0(false)}
// web link: installable app (iPhone / laptop) that works offline
if(location.protocol=='https:'&&!CAPN()){try{const l=document.createElement('link');l.rel='manifest';l.href='manifest.webmanifest';document.head.appendChild(l);const a=document.createElement('link');a.rel='apple-touch-icon';a.href='icon-180.png';document.head.appendChild(a);[['apple-mobile-web-app-capable','yes'],['apple-mobile-web-app-title','966Ph'],['theme-color','#061233']].forEach(([n,c])=>{const m=document.createElement('meta');m.name=n;m.content=c;document.head.appendChild(m)});if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}))}catch(e){}}
""")
JS[:]=[j.replace("function v34Click(d,b){","function v34Click(d,b){\n if(d.gdpull){gdPull(true);return 1}") for j in JS]
EN.update({'الطريقة القديمة: فولدر Drive for desktop':'Old way: Drive for desktop folder'})

# =====================================================================
# write
# =====================================================================
JSA = '\n'.join(JS)
rep("// ---------- v1.5 extras ----------", JSA + "// ---------- v1.5 extras ----------")
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}\n" + ''.join(CSS) + "\n")
rep("VER='v3.3'", "VER='v3.4'")
rep(" changelog:[{version:'v3.3',", " changelog:[{version:'v3.4',date:'2026-11-09',changes:['Custody: count of invoices without a paper invoice (tile that filters the table), «مشاركة…/حفظ…» menus, invoices without paper only or the full custody (Excel + PDF + those invoices) with a picker, the count and the handover date in the Excel/PDF, wider «البيان»','Custody handover «✅ تسليم العهدة»: saves the files, stamps the month «تم التسليم» and locks it, starts the next month with the remaining (or the full custody), «فتح للتعديل» and «إعادة التسليم» (asks to update the next month opening)','Bottom bar: «الصيانة» tab (maintenance pharmacies + report, folded) instead of «النسخ» (moved to the menu); the pharmacies tab shows branding pharmacies only','Layout: compact home card, sync alert as a small bar, pharmacy types with items first and the empty ones folded, pharmacy tools folded, execution cards, warehouse numbers in one line and folded filters','Warehouse: old stock (old design side acrylic, old End gandola side acrylic 100×25, blank acrylic for Wall/Floor Header and gandola side) offered when the size matches; alert when an item ran out and pharmacies still need it','Google Drive from the web link (GitHub Pages): Google sign-in on the laptop/iPhone, same uploads as the phone (966-laptop-…), automatic read of the other device newest file both ways, monthly Excel on Drive; installable and offline on the web link']},{version:'v3.3',")
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')

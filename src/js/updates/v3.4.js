// ---------- v3.4: custody — invoices without a paper invoice ----------
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

// ---------- v3.4: custody handover ----------
const cDd=iso=>String(iso||'').slice(0,10).split('-').reverse().join('-');
const cLk=M=>!!(M&&M.dl&&!M.reo);
const cSig=M=>JSON.stringify((M.items||[]).map(x=>[x.id,x.dt,x.tm,x.desc,x.comp,x.kind,x.amt,x.note,x.car,x.ph,x.ref,x.qt,(x.imgs||[]).length]).concat([M.open,JSON.stringify(M.dep||[])]));
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

// ---------- v3.4: maintenance tab, compact home, sync bar ----------
ICN.wrench='<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>';
function syncChip(){const h=syncBanner();if(!h.startsWith('<div class="alr"'))return '';const n=pendingN();return `<details class="schip" data-id="__sch"${V.op.__sch?' open':''}><summary>⚠ المزامنة: ${n?n+' صيدلية معدلة لسه ما اتصدّرتش':'آخر استيراد قديم'}<small>التفاصيل ›</small></summary>${h}</details>`}
function mntPhHtml(){const t=String(V.mpq||'').trim().toLowerCase(),A=DB.ph.filter(isMnt),L=A.filter(p=>!t||[p.no,p.rg,p.ct,p.name].join(' ').toLowerCase().includes(t)).sort(pSort),cur=MN(),g={};L.forEach(p=>{(g[p.mo||'—']=g[p.mo||'—']||[]).push(p)});const ks=Object.keys(g).sort().reverse();
 return `<div class="hcard hc2"><div class="hc-row"><button class="hc-add" data-newpm="1">${ic('add')}صيدلية صيانة</button><button class="hc-ib" data-madd="1">${ic('wrench')}<i>صيانة جديدة</i></button></div><small>${A.length} صيدلية صيانة</small></div>
 <details class="mg lst" data-id="__mph"${V.op.__mph||t?' open':''}><summary><span>🔧 صيدليات الصيانة</span><i>${A.length}</i></summary><div class="mgb"><input class="sf" id="mpq" placeholder="🔍 بحث برقم الصيدلية أو المنطقة" value="${esc(V.mpq||'')}">${ks.map(k=>{const a=g[k],open=!!t||!!V.op['mm_'+k];return `<details class="mg" data-id="mm_${k}"${open?' open':''}><summary><span>${k==cur?'الشهر الحالي':'شهر'} ${k}</span><i>${a.length}</i></summary><div class="mgb"><small>مكتملة ${a.filter(p=>p.st=='مكتملة').length} من ${a.length}</small>${a.map(pCard).join('')}</div></details>`}).join('')||'<p class="em">'+(t?'مفيش نتائج.':'لسه مفيش صيدليات صيانة. اضغط «صيدلية صيانة».')+'</p>'}</div></details>`}
function mntHtml(){const C=MU(),n=mList(C.cur).length;return mntPhHtml()+`<details class="mg lst" data-id="__mrep"${V.op.__mrep||V.mqf?' open':''}><summary><span>📋 كشف الصيانات · ${mQLab(C.cur)}</span><i>${n}</i></summary><div class="mgb">${mntHtml0()}</div></details>`}
function v34Click(d,b){
 if(d.gdpull){gdPull(true);return 1}
 if(d.newpm){goV({v:'add',op:{},dr:{},q:V.q});setTimeout(()=>{const m=$('#pmod');if(m&&[...m.options].some(o=>o.value=='صيانة')){m.value='صيانة';m.dispatchEvent(new Event('change',{bubbles:true}))}const x=$('#pno');if(x)x.focus()},60);return 1}
 return 0}
function v34Change(x){
 if(x.id=='mpq'){V.mpq=x.value;render();const i=$('#mpq');if(i){i.focus();i.setSelectionRange(i.value.length,i.value.length)}return 1}
 return 0}

// ---------- v3.4: pharmacy screen — types with items first, the empty ones folded ----------
function phCards(p){const A=TY(p),fo=V.fo||{},F=A.filter(t=>t.auto||(p.rows[t.id]||[]).length||V.op[t.id]||fo[t.id]||(V.dr&&V.dr[t.id]&&V.ed&&String(V.ed).startsWith(t.id+':'))),E=A.filter(t=>!F.includes(t));
 return F.map(t=>card(t,p)).join('')+(E.length?`<details class="pinfo pemp" data-id="__pem"${V.op.__pem?' open':''}><summary>${ic('add')} باقي الأنواع (${E.length})<small>${E.map(t=>esc(t.n)).join(' · ')}</small></summary>${E.map(t=>card(t,p)).join('')}</details>`:'')}

// ---------- v3.4: warehouse old stock + out-of-stock alert ----------
const OLDT={saw:'Side Acrylic Shelves Wall · تصميم قديم',saf:'Side Acrylic Shelves Floor · تصميم قديم',egs:'End gandola - Side أكريليك · تصميم قديم',bwh:'أكريليك فاضي · Wall Header',bfh:'أكريليك فاضي · Floor Header',beg:'أكريليك فاضي · Side جندولة'};
const OLDL={saw:'Side Acrylic رفوف جداري (تصميم قديم)',saf:'Side Acrylic رفوف أرضي (تصميم قديم)',egs:'End gandola Side أكريليك + ستيكر (تركي عادي، تصميم قديم)',bwh:'أكريليك فاضي للـ Wall Header',bfh:'أكريليك فاضي للـ Floor Header',beg:'أكريليك فاضي للـ Side جندولة'};
const OGS='100×25';
function whoSz(k,sh){if(k=='saw')return SZ('saw');if(k=='saf')return SZ('saf.'+sh);if(k=='egs'||k=='beg')return [OGS];if(k=='bwh')return (sh==2?['100']:SZ('wh.len')).map(l=>SZ('wh.h')[sh]+'×'+l);if(k=='bfh'){const a=[SZ('fh.s')[sh]];if(sh!=2&&!a.includes(SZ('fh.l')))a.push(SZ('fh.l'));return a}return []}
function whoD(){const d=V.wo=V.wo||{k:'saf',sh:0,sec:'Health',sd:'يمين',nm:'',sz:'',q:1,mt:'أكريليك + ستيكر',real:'',solo:''};if(d.k=='saw')d.sh=2;if(d.k=='egs'||d.k=='beg')d.sh=0;const S=whoSz(d.k,d.sh);if(d.sz!=WOSOLO&&!S.includes(d.sz))d.sz=S[0]||'';if(d.k=='egs'&&!S4.includes(d.sec))d.sec='Baby';return d}
function whoHtml(){const d=whoD(),k=d.k,S=whoSz(k,d.sh),sel=(id,L,v,lab)=>`<label>${lab}<select data-wo="${id}">${L.map(x=>{const[v2,l2]=Array.isArray(x)?x:[x,x];return `<option value="${esc(v2)}"${String(v2)==String(v)?' selected':''}>${esc(l2)}</option>`}).join('')}</select></label>`;
 return `<div class="wcard"><h2>🕰 إضافة مخزون قديم</h2><p class="sub">أصناف التصميم القديم والأكريليك الفاضي بتتحفظ لوحدها بعلامة «تصميم قديم»، ومش بتتسحب لوحدها لأي بند. لما يبقى فيه بند في صيدلية بنفس المقاس البرنامج بيعرضها عليك في «📦 من المخزن».</p>
 ${sel('k',Object.keys(OLDL).map(x=>[x,OLDL[x]]),k,'الصنف')}
 ${['saf','bwh','bfh'].includes(k)?sel('sh',SH.map((x,i)=>[i,x]),d.sh,'نوع الرفوف'):`<p class="sub">نوع الرفوف: <b>${SH[d.sh]}</b></p>`}
 ${k=='saw'?sel('sec',S4.concat(['Pharmacy']),d.sec,'القسم'):k=='saf'||k=='egs'?sel('sec',S4,d.sec,'القسم'):''}
 ${['saf','saw','egs'].includes(k)&&(OSN[d.sec]||[]).length?sel('nm2',[['','— بدون مسمى —']].concat(OSN[d.sec]),osOk(d)?d.nm2:'','المسمى (اختياري — بيظهر بصورته)'):''}
 ${k=='egs'?'<p class="sub">سايد الجندولة بيمشي للجندولة الصغيرة والكبيرة (الفرق في الهيدر بس).</p>':''}
 ${k[0]=='b'?'':sel('mt',['أكريليك + ستيكر','ستيكر فقط'],d.mt,'الخامة')}
 ${sel('sz',S.concat(k[0]=='b'?[]:[[WOSOLO,'مقاس قديم لوحده (اكتبه) — مش بيتعرض على الصيدليات']]),d.sz,'المقاس (سم)')}
 ${d.sz==WOSOLO?`<label>المقاس القديم (سم)<input data-wo="solo" placeholder="مثلاً 35×125" value="${esc(d.solo||'')}"></label>`:`<label>المقاس الفعلي (اختياري)<input data-wo="real" placeholder="مثلاً 118.5×30" value="${esc(d.real||'')}"><small class="autot">لو المقاس الحقيقي مختلف شوية عن المقاس اللي فوق. بيظهر جنبه في المخزن.</small></label>`}
 ${k=='saw'||k=='saf'||k=='egs'?sel('sd',['يمين','يسار'],d.sd,'الجهة (اتجاه الانحناء)'):''}
 ${(()=>{const im=osImgD(d)||OLDIMG[k+'|'+d.sec];return im?`<div class="woim"><img src="${im}" alt=""><small>صورة التصميم القديم لـ ${esc(d.sec)} (بتظهر على الصنف لحد ما تضيف صورته بـ 📷)</small></div>`:''})()}
 <label>العدد<input type="number" inputmode="numeric" min="1" data-wo="q" value="${esc(d.q)}"></label>
 <div class="tt"><button class="pr big" data-whosave="1">${ic('check')}حفظ في المخزن</button><button data-whox="1">رجوع</button></div></div>
 ${(()=>{const L=WU().filter(x=>x.old);return L.length?`<div class="wcard"><b>المخزون القديم (${L.length} صنف)</b>${L.map(whCard).join('')}</div>`:''})()}`}
function whoSave(){const d=whoD(),q=wq(+d.q||0);if(!(q>0))return alert('اكتب العدد');if(!d.sz)return alert('اختار المقاس');
 const solo=d.sz==WOSOLO,sz=solo?String(d.solo||'').trim().replace(/\s*[x×*]\s*/i,'×'):d.sz;if(!sz)return alert('اكتب المقاس القديم');
 const o={sh:d.sh,ty:OLDT[d.k],nm:(d.k=='saw'||d.k=='saf'||d.k=='egs')?(osOk(d)?d.nm2+' · '+d.sd:d.sd):'',sec:(d.k=='saw'||d.k=='saf'||d.k=='egs')?d.sec:'',mat:d.k[0]=='b'?'أكريليك فاضي':d.mt||'أكريليك + ستيكر',size:sz,old:1};
 const real=solo?'':String(d.real||'').trim().replace(/\s*[x×*]\s*/i,'×');
 const x=whAdd(o,q,'in','manual','مخزون قديم'+(real?' (فعلي '+real+')':''));x.old=1;if(solo)x.solo=1;if(real)x.real=real;d.real='';d.solo='';sv();snd('ok');d.q=1;render();toastT(`✓ اتضاف ${q} · ${OLDL[d.k]} · ${sz}${real?' (فعلي '+real+')':''} (الرصيد ${wq(x.qty)})`)}
function whOldOpts(p,t,r){if(!p||p._wh||p._rc||!isOld(p,r))return [];const W=WU().filter(x=>x.old&&!x.solo&&+x.qty>=1);if(!W.length)return [];const need=Math.max(0,qn(r)-(+r.r||0)),O=[],sz=v=>String(v||'').replace(/\s+/g,''),sh=rsh(r,p.sh);
 const add=(x,n,k,lab)=>{n=Math.min(n,Math.floor(+x.qty));if(n>0)O.push({k,id:x.id,n,txt:`🕰 ${n} ${lab}${x.mat&&x.mat!='أكريليك فاضي'?' · '+x.mat:''}${x.real?' · فعلي '+x.real:''}${x.nm?' · '+x.nm:''} (في المخزن ${wq(x.qty)})`})};
 if(need>0&&(t.id=='saw'||t.id=='saf'))W.filter(x=>x.ty==OLDT[t.id]&&(t.id=='saw'||x.sh==sh)&&x.sec==r.sec&&sz(x.size)==sz(r.sz)&&osd(x.nm)==r.sd).forEach(x=>add(x,need,'a','تصميم قديم بنفس المقاس'));
 if(need>0&&t.id=='eg'&&sh<=1){const ns=egRd(egFs(r)*need),na=egRd(egFa(r)*need);W.filter(x=>(x.ty==OLDT.egs&&(x.nm==r.nm||(x.sec&&x.sec==egSec(r.nm))))||x.ty==OLDT.beg).forEach(x=>{const n=x.ty==OLDT.egs?ns:(na||ns);if(n>0)add(x,n,'o',x.ty==OLDT.egs?'سايد أكريليك تصميم قديم':'أكريليك فاضي للسايد '+OGS)})}
 if(need>0&&t.id=='wh'&&!wood(r)){const s0=SZ('wh.h')[sh]+'×'+r.len;W.filter(x=>x.ty==OLDT.bwh&&x.sh==sh&&sz(x.size)==sz(s0)).forEach(x=>add(x,need,'o','أكريليك فاضي بنفس المقاس'))}
 if(need>0&&t.id=='fh'){const z=szOf(t.z(r,p.sh));W.filter(x=>x.ty==OLDT.bfh&&x.sh==sh&&sz(x.size)==sz(z)).forEach(x=>add(x,need,'o','أكريليك فاضي بنفس المقاس'))}
 return O}
function whOut(){const W=WU().filter(x=>!x.old&&+x.qty<=0),R=[];
 if(W.length){const need=[];DB.ph.forEach(p=>{if(!isBr(p)||p.st=='مكتملة'||p._wh)return;TY(p).forEach(t=>(p.rows[t.id]||[]).forEach(r=>{const n=Math.max(0,qn(r)-(+r.r||0));if(!n)return;whParts(t,r,p.sh).forEach(y=>{if(!y.pk)need.push({p,k0:whKey0(y),n:n*y.f})})}))});
  W.forEach(x=>{if(whQty(x)>0)return;const k0=whKey0(x),m={};need.filter(y=>y.k0==k0).forEach(y=>{m[y.p.no]=(m[y.p.no]||0)+y.n});const P=Object.keys(m);if(P.length&&!R.some(o=>whKey0(o.x)==k0))R.push({x,P:P.map(no=>({no,n:wq(m[no])}))})})}
 return R}
function whOutHtml(){const R=whOut();if(!R.length)return '';return `<details class="alr wout" data-id="__wout"${V.op.__wout?' open':''}><summary>⚠ ${R.length} صنف خلص من المخزن وفيه صيدليات محتاجاه <small>التفاصيل ›</small></summary>${R.map(o=>`<small>• <b>${esc(o.x.ty)}</b>${whNm(o.x)?' · '+esc(whNm(o.x)):''} · ${esc(o.x.size||'')} — ${o.P.map(y=>'صيدلية '+esc(y.no)+' ('+y.n+')').join('، ')}</small>`).join('')}<small>اطلبهم من الطباعة (نواقص الطباعة).</small></details>`}
function v34WhClick(d,b){
 if(d.whpic){const x=WU().find(y=>y.id==d.whpic);if(x&&x.pic&&!confirm('الصنف ليه صورة. تغيّرها؟ (إلغاء = تمسحها)')){delete x.pic;sv();render();return 1}whPicPick(d.whpic);return 1}
 if(d.whold){V.wf=V.wf||{};V.wf.old=!V.wf.old;if(V.wf.old)V.wf.sh='';render();return 1}
 if(d.whoa){V.wo=null;goV(Object.assign(V,{v:'who'}));return 1}
 if(d.whosave){whoSave();return 1}
 if(d.whox){goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});return 1}
 return 0}
function v34WhChange(x){if(!x.dataset||x.dataset.wo==null)return 0;const d=whoD(),k=x.dataset.wo;d[k]=k=='sh'?+x.value:x.value;if(k=='k'){d.sz='';if(d.k=='saf'&&d.sh==2&&false)d.sh=0}render();return 1}

// ---------- v3.4: Google Drive from the web link (GitHub Pages) ----------
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
  const q=await gdGet(f.id);GDPL=1;let msg;try{msg=await gdApply(q,'merge','قبل دمج '+f.name+' من Google Drive')}finally{GDPL=0}document.querySelectorAll('.toast.stem').forEach(x=>x.remove());gdU(x=>{x.pf=f.id;x.pm=f.modifiedTime;x.pn=f.name;x.pt=nowIso()});render();toastT('☁️ اتدمجت آخر بيانات '+(GWEB()?'الموبايل':'اللاب توب')+' · '+msg)}
 catch(e){console.warn(e);if(e.need){if(manual)alert('محتاج تسجيل دخول Google الأول');else gdNeedNote()}else if(manual)alert('⚠ '+(e.message||e))}
 finally{GDPB=0;if(t)t.remove();gdStat0()}}
function gdPullHtml(){const o=gdS();if(!o.on)return '';const w=GWEB()?'الموبايل':'اللاب توب';return `<div class="wcard"><h3>☁️ بيانات ${w}</h3><small>${o.pn?'آخر دمج تلقائي: <b>'+esc(o.pn.replace(/^966-|\.json$/g,''))+'</b> · '+fd(o.pt):'لسه مفيش دمج من '+w}</small><br><small>بيتقرا ويتدمج لوحده كل ما تفتح التطبيق وكل 15 دقيقة (كل صيدلية بتاخد الأحدث، وقبلها نقطة استعادة).</small><div class="tt"><button data-gdpull="1">${ic('db')}اقرا آخر بيانات ${w} دلوقتي</button></div></div>`}
function gdHtml(){if(CAPN())return gdHtml0(true)+gdPullHtml();
 if(GWEB())return `<div class="ph"><small>🌐 فاتح التطبيق من اللينك. Google Drive بيشتغل هنا زي الموبايل بالظبط: بيرفع لوحده، وبيقرا آخر بيانات الموبايل لوحده.</small></div>`+gdHtml0(true)+gdPullHtml()+`<details class="pinfo" data-id="__gdo"${V.op.__gdo?' open':''}><summary>${ic('file')} الطريقة القديمة: فولدر Drive for desktop</summary>${gdHtml0(false)}</details>`;
 return `<div class="ywarn">💡 علشان Google Drive يشتغل لوحده على اللاب توب (يرفع ويقرا بيانات الموبايل من غير Drive for desktop) افتح التطبيق من اللينك:<br><a href="${GWURL}" target="_blank" rel="noopener" dir="ltr">${GWURL}</a><br><small>بياناتك اللي على المتصفح ده مش بتتنقل للينك لوحدها: احفظ نسخة احتياطية هنا واستوردها هناك، أو سيبه يقرا من Drive بعد الربط.</small></div>`+gdHtml0(false)}
// web link: installable app (iPhone / laptop) that works offline
if(location.protocol=='https:'&&!CAPN()){try{const l=document.createElement('link');l.rel='manifest';l.href='manifest.webmanifest';document.head.appendChild(l);const a=document.createElement('link');a.rel='apple-touch-icon';a.href='icon-180.png';document.head.appendChild(a);[['apple-mobile-web-app-capable','yes'],['apple-mobile-web-app-title','966Ph'],['theme-color','#061233']].forEach(([n,c])=>{const m=document.createElement('meta');m.name=n;m.content=c;document.head.appendChild(m)});if('serviceWorker' in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}))}catch(e){}}

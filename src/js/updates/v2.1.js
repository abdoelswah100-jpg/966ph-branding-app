// ---------- v2.1: extra items (customer request), remainder closed by the customer, report tables, monthly batch ----------
const XN0='العميل طلب التعديل',XIT='➕ بنود إضافية حسب طلب العميل';
const isXI=r=>!!(r&&r.xi=='نعم');
const xiTag=r=>isXI(r)?`<small class="rshc xit">➕ بند إضافي: ${esc(r.xn||XN0)}</small>`:'';
const ntx=r=>[r.nt,isXI(r)?'➕ بند إضافي: '+(r.xn||XN0):'',r.cx?'🔖 الباقي بطلب العميل':''].filter(Boolean).join(' · ');
function xiRows(p,on){const o={};Object.keys(p.rows||{}).forEach(k=>{const a=p.rows[k];o[k]=Array.isArray(a)?a.filter(r=>isXI(r)==!!on):a});return o}
function xiList(P){const o=[];P.forEach(p=>{if(!Object.values(p.rows||{}).some(a=>Array.isArray(a)&&a.some(isXI)))return;rcvIds(p);TY(p).forEach(t=>(p.rows[t.id]||[]).forEach(r=>{if(!isXI(r))return;sizeRows([Object.assign({},p,{rows:{[t.id]:[r]}})]).forEach(x=>o.push(Object.assign(x,{kind:'xi',ty:XIT,no:p.no,pid:p.id,rid:r._i,xn:r.xn||XN0,tn:t.n})))}))});return o}
const rdelB=x=>`<td class="act"><button data-rdel="base:${x._idx}" title="حذف الصف">حذف</button></td>`;
function pkTbl(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';return `<h3>Side Acrylic Pocket <small>(تابع للجندولة)</small></h3><div class="sc"><table><tr><th>الجهة</th><th>الخامة</th><th>العدد</th><th class="act">إجراء</th></tr>${v.map(x=>`<tr><td>${esc(x.sz)}</td><td>${esc(x.mat)}</td><td>${x.q}</td>${rdelB(x)}</tr>`).join('')}<tr class="tot"><td colspan="2">إجمالي Side Acrylic Pocket</td><td>${v.reduce((a,x)=>a+(+x.q||0),0)} قطعة</td><td class="act"></td></tr></table></div>`}
function abTbl(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';return `<h3>Acrylic boards</h3><div class="sc"><table><tr><th>البند</th><th>المقاس</th><th>الخامة</th><th>الحالة</th><th>العدد</th><th class="act">إجراء</th></tr>${v.map(x=>`<tr><td>${esc(x.n)}</td><td>${esc(x.sz)}</td><td>${esc(x.mat)}</td><td${x.st=='تصنيع + تركيب'?' style="background:#FAD4D4;font-weight:700"':''}>${esc(x.st)}</td><td>${x.q}</td>${rdelB(x)}</tr>`).join('')}<tr class="tot"><td colspan="4">إجمالي Acrylic boards</td><td>${v.reduce((a,x)=>a+(+x.q||0),0)} قطعة</td><td class="act"></td></tr></table></div>`}
function xiTbl(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';const m=new Set(v.map(x=>x.pid)).size>1;return `<h3>${XIT}</h3><div class="sc"><table class="xitb"><tr>${m?'<th>الصيدلية</th>':''}<th>نوع الدعاية</th><th>المقاس</th><th>الخامة</th><th>العدد</th><th>ملاحظات</th><th class="act">إجراء</th></tr>${v.map(x=>`<tr>${m?`<td><b>${esc(x.no)}</b></td>`:''}<td>${esc(x.n)}</td><td>${esc(x.sz)}</td><td>${esc(x.mat)}</td><td>${x.n==='Wall Sticker'?x.a.toFixed(2)+' م²':x.q}</td><td contenteditable="true" data-xn="${x.pid}|${x.rid}" class="xnc">${esc(x.xn)}</td>${rdelB(x)}</tr>`).join('')}</table></div><small class="np sub">✎ اضغط على الملاحظة وعدّلها، وبتتحفظ في البند.</small>`}
document.addEventListener('focusout',e=>{const x=e.target;if(!x||!x.dataset||!x.dataset.xn)return;const[pid,rid]=x.dataset.xn.split('|'),p=DB.ph.find(q=>String(q.id)==pid);if(!p||!uEditP(p))return;let r=null;Object.values(p.rows||{}).forEach(a=>{if(Array.isArray(a)&&!r)r=a.find(y=>y&&y._i==rid)});if(!r)return;const v=x.textContent.trim()||XN0;if(v===r.xn)return;r.xn=v;p.modAt=nowIso();svq();toastT('✓ اتحفظ السبب في البند')});
// remainder closed by the customer (button in the execution list)
function cxTag(x,k){const r=x.r,c=r.cx?'<small class="rshc cxt">🔖 الباقي بطلب العميل (يتحاسب)</small>':'';const q=qn(r),pk=x.t.id=='eg'&&egSub(r,x.s),left=(!(x.t.id=='eg'&&egAO(r,x.s))&&(+r.x||0)<q)||(pk&&SDS.some(([sd])=>pkv(r,'x',sd)<egN(r,x.s,sd)));
 return xiTag(r)+c+(k=='x'&&V.v!='rcv'&&(r.cx||left)?`<button class="np tcx" data-tcx="${x.t.id}:${x.i}">${r.cx?'↺ إلغاء «بطلب العميل»':'🔖 الباقي بطلب العميل'}</button>`:'')}
// management reports of a month, one file per pharmacy
function mrbHtml(){const ms=months(),m=V.mrm||V.mo||MN(),L=DB.ph.filter(p=>p.mo==m&&isBr(p)).sort(pSort),X=V.mrx||{},f=DB.cfg.mrbf||'pdf',n=L.filter(p=>!X[p.id]&&(V.mrk!='pho'||phoHas(p))).length,nf=V.mrk=='pho'?n:n*(f=='both'?2:1);
 return `<div class="wcard"><h2>📤 تقارير الإدارة لكل صيدلية لوحدها</h2><p class="sub">تقرير منفصل لكل صيدلية، كلهم مرة واحدة للمشاركة (واتساب).</p><div class="tt">${[['mg','تقرير الإدارة'],['pho','تقرير صور قبل / بعد']].map(([k,t])=>`<button${(V.mrk||'mg')==k?' class="pr"':''} data-mrbk="${k}">${t}</button>`).join('')}</div><label>الشهر<select id="mrbm">${(ms.includes(m)?ms:ms.concat([m])).map(x=>`<option value="${x}"${x==m?' selected':''}>${x}</option>`).join('')}</select></label>
 ${V.mrk=='pho'?'<small class="hint">تقرير الصور PDF بس، وللصيدليات اللي فيها صور قبل أو بعد.</small>':''}<div class="tt"${V.mrk=='pho'?' hidden':''}>${[['pdf','PDF'],['xlsx','Excel'],['both','الاتنين']].map(([k,t])=>`<button${f==k?' class="pr"':''} data-mrbf="${k}">${t}</button>`).join('')}</div></div>
 <div class="wcard">${L.length?L.map(p=>`<label class="mrbr"><input type="checkbox" data-mrbp="${p.id}"${X[p.id]?'':' checked'}> <b>${esc(p.no)}</b> ${esc(p.name||'')} <small>· ${esc(p.st||'')}</small></label>`).join(''):'<p class="em">مفيش صيدليات في الشهر ده.</p>'}</div>
 <div class="tt"><button class="pr big" data-mrbgo="1"${n?'':' disabled'}>${ic('share')}تجهيز ومشاركة (${nf} ملف)</button></div>`}
const mLab=m=>String(m||'').split('-').reverse().join('-');
async function shareFiles(F,msg){if(!F.length)return;
 if(CAPN()){const U=[];for(const f of F){try{const w=await nWrite(NDIR+'/'+f.name,f);U.push(w.uri)}catch(e){console.error(e)}}if(CP('Share')&&U.length){try{await CP('Share').share({title:msg,text:msg,files:U,dialogTitle:msg})}catch(e){}}toastT('✓ اتحفظ '+U.length+' ملف في Documents/'+NDIR);return}
 try{if(navigator.canShare&&navigator.canShare({files:F})){await navigator.share({files:F,title:msg,text:msg});return}}catch(e){if(e&&e.name=='AbortError')return}
 for(const f of F){dl(f.name,f,f.type);await new Promise(r=>setTimeout(r,350))}toastT('✓ اتنزّل '+F.length+' ملف. ابعتهم من واتساب')}
async function mrbGo(){if(V.mrk=='pho')return mrbGoPho();const m=V.mrm||V.mo||MN(),X=V.mrx||{},L=DB.ph.filter(p=>p.mo==m&&isBr(p)&&!X[p.id]).sort(pSort),f=DB.cfg.mrbf||'pdf';if(!L.length)return;
 const t=toast('جاري تجهيز التقارير… 0 / '+L.length),F=[];
 try{for(let i=0;i<L.length;i++){const p=L[i],el=document.createElement('div');el.innerHTML=mgmtHtml(p);const nm='تقرير الإدارة - صيدلية '+p.no+' - '+mLab(m);
  if(f!='xlsx'){const b=await buildPdf(el,'تقرير تنفيذ للإدارة — '+PL(p));F.push(new File([b],nm+'.pdf',{type:'application/pdf'}))}
  if(f!='pdf'){const b=rpXlsx(el);F.push(new File([b],nm+'.xlsx',{type:b.type||'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}))}
  t.innerHTML='جاري تجهيز التقارير… '+(i+1)+' / '+L.length}}catch(e){console.error(e);t.remove();alert('تعذّر تجهيز التقارير على الجهاز ده');return}
 t.remove();window._mrbF=F;await shareFiles(F,'تقارير تنفيذ للإدارة — شهر '+mLab(m)+' — '+L.length+' صيدلية')}
function v21Click(d,b){
 if(d.tcx){const p=curP(),[tid,i]=d.tcx.split(':'),r=p&&(p.rows[tid]||[])[+i];if(!r)return 1;if(r.cx){delete r.cx}else{if(!confirm('اللي ما اتنفذش من البند ده يتحاسب في تقرير الإدارة، ومش هيظهر ناقص (طباعة ولا تنفيذ). المستلم والمتنفذ زي ما هم. تأكيد؟'))return 1;r.cx=1}p.modAt=nowIso();sv();tkRe();return 1}
 if(d.mrb){goV({v:'mrb',mrm:V.v=='all'&&V.q&&V.q.mo?V.q.mo:(V.mo||MN()),bk:V.v,bam:V.am,op:{},dr:{},q:V.q});return 1}
 if(d.mrbx){const k=V.bk||'month';goV(k=='all'?{v:'all',am:V.bam||'mg',op:{},dr:{},q:V.q}:{v:k,op:{},dr:{},q:V.q});return 1}
 if(d.mrbf){DB.cfg.mrbf=d.mrbf;svq();render();return 1}
 if(d.mrbgo){mrbGo();return 1}
 return 0}
function v21Change(x){
 if(x.id=='mrbm'){V.mrm=x.value;V.mrx={};render();return 1}
 if(x.dataset&&x.dataset.mrbp){V.mrx=V.mrx||{};if(x.checked)delete V.mrx[x.dataset.mrbp];else V.mrx[x.dataset.mrbp]=1;render();return 1}
 return 0}

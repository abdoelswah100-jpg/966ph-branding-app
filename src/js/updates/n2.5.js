// ---------- 2.5 (file n2.5.js) ----------
// 1) Acrylic board «Pharmacy hours QR · دوام الصيدلية» 30×40 (core: 03-sizes.js)
// 2) header below the phone status bar (safe area: CSS + measured fallback on Android edge-to-edge)
// 3) ⏸ on hold: p.hold=1 → kept aside like other users' pharmacies (HID): out of every list, report, shortage, route and notification;
//    one line «⏸ تحت الانتظار» in the pharmacies / maintenance tab with «▶ اعتماد». File {kind:'966-hold', ids:[…]}.
// 4) customer reasons: quick choices العميل طلب التبديل / التغيير / التعديل
// 5) ⏹ «طُلب ولم يُنفذ» (r.cx + r.cxn): button on every row, counted in the management report with its own table, not a shortage,
//    what was received goes to the warehouse with the surplus
// 6) 🔁 swap = «طُلب ولم يُنفذ» on the original + the new row as an extra item linked to it; one warehouse rule (received − executed − damaged)
//    warnings on conflicts; editing the size/name of a received row asks whether it is a swap; edits keep cx / swap links
// 7) «وصفتي» custom type moved to Acrylic boards (2.4 only matched «وصفات»)
// 8) screw caps never below zero; what was installed without stock is deducted as soon as caps are added
// 9) completing a pharmacy with rows not fully executed: executed all / not executed (customer) / keep as shortages
// 10) «يرجع للمخزن» screen shows the reason of each line
// 11) custody: «عمالة» kind (أجرة عامل تحميل وتنزيل بضاعة), camera button for the invoice photo
const CXR=['العميل طلب التبديل','العميل طلب التغيير','العميل طلب التعديل'],CXL='طُلب ولم يُنفذ';
const isHold=p=>!!(p&&p.hold);
const cxLeft=(r,s,t)=>{const q=qn(r);return Math.max(0,q-(+r.x||0))};
// ---- 2) safe area
(function(){try{const m=document.querySelector('meta[name=viewport]');if(m&&!/viewport-fit/.test(m.content))m.content+=',viewport-fit=cover';
 const fix=()=>{const d=document.createElement('div');d.style.cssText='position:fixed;top:0;height:env(safe-area-inset-top,0px);width:1px;visibility:hidden';document.body.appendChild(d);const h=d.getBoundingClientRect().height;d.remove();
  let v=h;if(!v&&typeof CAPN=='function'&&CAPN()&&screen.height-window.innerHeight<20)v=28;document.documentElement.style.setProperty('--sat',v+'px')};
 if(document.body)fix();else addEventListener('DOMContentLoaded',fix);addEventListener('resize',()=>setTimeout(fix,200))}catch(e){}})();
// ---- 3) on hold
const _uApply25=uApply;uApply=function(){const r=_uApply25.apply(this,arguments);try{if(DB.users&&HIDDB===DB){const h=DB.ph.filter(isHold);if(h.length){DB.ph=DB.ph.filter(p=>!isHold(p));HID=HID.concat(h)}}}catch(e){console.warn(e)}return r};
const HOLDL=()=>((HIDDB===DB?HID:[]).concat(DB.ph)).filter(isHold);
function holdAll(fn){return function(){if(HIDDB===DB&&HID.some(isHold)){DB.ph=DB.ph.concat(HID.filter(isHold));HID=HID.filter(p=>!isHold(p))}try{return fn.apply(this,arguments)}finally{try{uApply()}catch(e){}}}}
phImpGo=holdAll(phImpGo);doSync=holdAll(doSync);
function holdSet(ids,on){let n=0;(HIDDB===DB?HID:[]).concat(DB.ph).forEach(p=>{if(ids.includes(p.id)&&!!p.hold!=!!on){if(on)p.hold=1;else delete p.hold;p.modAt=nowIso();n++}});if(n){sv();uApply()}return n}
function holdImp(q){const ids=(q.ids||[]).map(String),A=(HIDDB===DB?HID:[]).concat(DB.ph),L=A.filter(p=>ids.includes(String(p.id))&&!p.hold);
 if(!L.length)return alert('مفيش صيدليات جديدة تتحط تحت الانتظار من الملف ده (يمكن اتعملت قبل كده).');
 if(!confirm(`⏸ تحت الانتظار: ${L.length} صيدلية\n${L.map(p=>p.no+(p.ct&&p.ct!='الرياض'?' '+p.ct:'')).join('، ')}\n\nهيختفوا من القوايم والتقارير والنواقص والمسار، ويبقوا في سطر واحد «⏸ تحت الانتظار». تقدر تعتمدهم في أي وقت.${q.note?'\n\n'+q.note:''}`))return;
 snap('قبل «تحت الانتظار» · '+L.length+' صيدلية');holdSet(L.map(p=>p.id),1);render();toastT('✓ '+L.length+' صيدلية تحت الانتظار')}
function holdBlock(L,id){if(!L.length)return '';const t=String((V.q&&V.q.t)||V.mpq||'').trim().toLowerCase(),M=L.filter(p=>!t||[p.no,p.rg,p.ct,p.name].join(' ').toLowerCase().includes(t)).sort(pSort);
 return `<details class="mg lst hold" data-id="${id}"${V.op[id]||t?' open':''}><summary><span>⏸ تحت الانتظار</span><i>${L.length}</i></summary><div class="mgb"><small class="hint">مش بيدخلوا التقارير ولا كشف الصيانة ولا النواقص ولا المسار، لحد ما تعتمدهم.</small><div class="tt"><button data-hldall="${id}">▶ اعتماد الكل (${L.length})</button></div>
 ${M.map(p=>`<div class="rw holdr"><span><b>${esc(p.no)}</b> ${esc([p.name,p.ct].filter(Boolean).join(' · '))} <small>· ${esc(p.mod||'')} · ${esc(p.mo||'')} · ${Object.values(p.rows||{}).reduce((a,x)=>a+(Array.isArray(x)?x.length:0),0)} بند</small></span><div class="bt"><button class="pr" data-hldok="${p.id}">▶ اعتماد</button></div></div>`).join('')}</div></details>`}
const _hl25=hl;hl=function(){const r=_hl25.apply(this,arguments);try{const h=$('#hl'),L=HOLDL().filter(isBr);if(h&&L.length)h.insertAdjacentHTML('beforeend',holdBlock(L,'__holdb'))}catch(e){console.warn(e)}return r};
const _mntPhHtml25=mntPhHtml;mntPhHtml=function(){const s=_mntPhHtml25.apply(this,arguments),L=HOLDL().filter(isMnt);if(!L.length)return s;const k='<details class="mg lst" data-id="__mph"';return s.includes(k)?s.replace(k,holdBlock(L,'__holdm')+k):s+holdBlock(L,'__holdm')};
// ---- 5) not executed (customer)
const cxTxt=r=>{const n=cxLeft(r),q=qn(r);return `⏹ ${CXL}${n&&n<q?` ${n} من ${q}`:''}${r.cxn?' · '+r.cxn:''}`};
let CXS=null;
function cxOpen(pid,tid,i){const p=DB.ph.find(x=>x.id==pid),r=p&&(p.rows[tid]||[])[+i];if(!r)return;if(r.sw)return alert('البند ده متبدّل بطلب العميل — لو عايز ترجّعه اضغط «↺ إلغاء التبديل».');
 if(cxLeft(r)<=0&&!confirm('البند ده متعلّم متنفذ كله. تعلّمه «'+CXL+'» برضه؟'))return;CXS={pid,tid,i:+i,v:r.cxn||CXR[1]};cxDraw()}
function cxDraw(){cShClose();const p=DB.ph.find(x=>x.id==CXS.pid),t=T.find(x=>x.id==CXS.tid),r=p.rows[CXS.tid][CXS.i],n=cxLeft(r),el=document.createElement('div');el.className='csh';
 el.innerHTML=`<div class="cshb"><b>⏹ ${CXL}</b><small>${esc(t.n)} · ${esc(t.z(r,p.sh))}</small><small class="hint">${n?`<b>${n}</b> من ${qn(r)} ما اتنفذوش.`:''} البند يتحسب في تقرير الإدارة بالعلامة دي، ومش هيظهر في النواقص. اللي اتستلم منه (طباعة أو مخزن) يرجع المخزن مع الفائض.</small>
 <b>السبب</b><div class="tt">${CXR.map(x=>`<button class="${CXS.v==x?'pr':''}" data-cxr="${esc(x)}">${esc(x)}</button>`).join('')}</div><input id="cxrt" placeholder="أو اكتب السبب" value="${CXR.includes(CXS.v)?'':esc(CXS.v||'')}">
 <div class="cshr"><button class="pr" data-cxgo="1">تأكيد</button><button data-swx="1">إلغاء</button></div></div>`;document.body.appendChild(el)}
function cxGo(){const p=DB.ph.find(x=>x.id==CXS.pid),r=p&&p.rows[CXS.tid][CXS.i];if(!r)return;const w=(($('#cxrt')||{}).value||'').trim()||CXS.v||CXR[1];r.cx=1;r.cxn=w;p.modAt=nowIso();cShClose();CXS=null;sv();render();toastT('✓ اتعلّم «'+CXL+'»')}
function cxUndo(pid,tid,i){const p=DB.ph.find(x=>x.id==pid),r=p&&(p.rows[tid]||[])[+i];if(!r)return;if(r.sw)return alert('البند ده متبدّل — استخدم «↺ إلغاء التبديل».');if(!confirm('إلغاء «'+CXL+'» للبند ده؟ هيرجع يظهر في النواقص لو لسه ناقص.'))return;delete r.cx;delete r.cxn;p.modAt=nowIso();sv();render()}
// management report: own table (rows stay counted at the requested quantity)
let MRP=[];const _mrr25=managementReportRows;managementReportRows=function(P0){const P=(P0||[]).filter(p=>!isHold(p));MRP=P;return _mrr25.call(this,P)};
function cxList(P){const o=[];(P||[]).forEach(p=>TY(p).forEach(t=>(p.rows[t.id]||[]).forEach(r=>{if(!r||!r.cx)return;o.push({no:p.no,tn:t.n,z:t.z(r,p.sh),n:cxLeft(r),q:qn(r),w:r.cxn||'',sw:r.sw&&r.sw.to||''})})));return o}
const _xiTbl25=xiTbl;xiTbl=function(L,h){const s=_xiTbl25(L,h),C=cxList(MRP);if(!C.length)return s;const m=new Set(C.map(x=>x.no)).size>1;
 return s+`<h3>⏹ ${CXL} (بطلب العميل)</h3><div class="sc"><table class="xitb"><tr>${m?'<th>الصيدلية</th>':''}<th>نوع الدعاية</th><th>البند</th><th>لم يُنفذ</th><th>السبب</th></tr>${C.map(x=>`<tr>${m?`<td><b>${esc(x.no)}</b></td>`:''}<td>${esc(x.tn)}</td><td>${esc(x.z)}</td><td>${x.n} من ${x.q}</td><td>${esc(x.w)}${x.sw?' ← '+esc(x.sw):''}</td></tr>`).join('')}</table></div><small class="hint">اللي اتبدّل (←) مش محسوب في الجدول فوق، والبديل في «البنود الإضافية». والباقي محسوب فوق بالعدد المطلوب.</small>`};
// ---- 6) swap = not executed + linked extra item
swOpen=function(tid,i,nd){const p=curP(),t=T.find(x=>x.id==tid),r=p&&(p.rows[tid]||[])[+i];if(!r)return;
 if(r.sw)return alert('البند ده متبدّل قبل كده.');if(r.cx&&!confirm('البند ده متعلّم «'+CXL+'» قبل كده. تحوّله لتبديل وتضيف البديل؟'))return;
 if((+r.x||0)>=qn(r)&&!confirm('البند ده متعلّم متنفذ كله ('+(+r.x||0)+'). التبديل معناه إن العميل غيّره وما اتركبش. تكمل؟ (لو اتركب واتشال علّمه هالك من الاختيارات)'))return;
 const P=(whParts(t,r,p.sh)||[]).filter(y=>y.f>0),q=Math.max(0,(+r.r||0)-(+r.x||0))||0;
 SWP={pid:p.id,tid,i:+i,nd:nd||null,P:P.map(y=>({y,k:whKey(y),n:wq(q*y.f),st:isStk(y),v:isStk(y)?'':'wh'})).filter(o=>o.n>0)};swDraw()};
swGo=function(){const miss=SWP.P.filter(o=>!o.v);if(miss.length)return alert('اختار لكل جزء ستيكر: اتركب (هالك) ولا ما اتركبش (يرجع المخزن)');
 const p=DB.ph.find(x=>x.id==SWP.pid),t=T.find(x=>x.id==SWP.tid),r=p.rows[SWP.tid][SWP.i];if(!r)return;snapLater('قبل تبديل بطلب العميل — صيدلية '+p.no,JSON.stringify(DB));
 const hk={};SWP.P.forEach(o=>{if(o.v=='hk')hk[o.k]=(hk[o.k]||0)+o.n});r.cx=1;r.cxn=CXR[0];r.sw={at:nowIso(),hk};const lab=t.z(r,p.sh);
 const nr=JSON.parse(JSON.stringify(SWP.nd||r));['r','x','wf','wfpR','wfpL','wxs','wxh','wxa','rpR','rpL','xpR','xpL','cx','cxn','sw','hk','ck','rcv','swf','an_','_i','wo','rol','_su'].forEach(k=>delete nr[k]);nr.swf=lab;nr.xi='نعم';nr.xn=CXR[0];
 cShClose();SWP=null;p.modAt=nowIso();sv();V.dr[t.id]=nr;V.ed=null;V.op[t.id]=true;V.fo=V.fo||{};V.fo[t.id]=true;V.swF2={pid:p.id,tid:t.id,o:r,n:(p.rows[t.id]||[]).length};render();
 toastT('✓ الأصلي اتعلّم «'+CXL+' · '+CXR[0]+'». اختار البديل واضغط «إضافة»');setTimeout(()=>{const f=document.querySelector('[data-add="'+t.id+'"]');if(f&&f.scrollIntoView)f.scrollIntoView({block:'center'})},80)};
swUndo=function(tid,i){const p=curP(),r=p&&(p.rows[tid]||[])[+i];if(!r||!r.sw)return;const to=r.sw.to;if(!confirm('إلغاء التبديل للبند ده؟ هيرجع بند عادي (مش «'+CXL+'»).'+(to?'\nالبديل «'+to+'» مش هيتمسح — امسحه بإيدك لو مش محتاجه.':'')))return;delete r.sw;delete r.cx;delete r.cxn;p.modAt=nowIso();sv();render()};
const KEEP25=['cx','cxn','sw','swf','rcv','wxh','wxs','wxa','wo','rol','xpR','xpL'];
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-add]');if(!b||V.v!='ph')return;const p=curP(),tid=b.dataset.add,t=T.find(x=>x.id==tid);if(!p||!t)return;
 if(V.ed&&V.ed.t==tid){const L=p.rows[tid]||[],i=V.ed.i,o=L[i],d=V.dr[tid];if(!o)return;
  const ign=['q','nt','xi','xn','hk','mw','_su','swf'],sig=y=>JSON.stringify(t.f.filter(f=>!ign.includes(f.k)).map(f=>y[f.k]==null?'':String(y[f.k])));
  if(d&&(+o.r||0)>0&&!o.sw&&sig(o)!==sig(d)&&confirm(`القطعة القديمة «${t.z(o,p.sh)}» متسجلة مستلمة (${+o.r||0}).\n\nده تبديل بطلب العميل؟\n• موافق: القديمة تفضل «${CXL}» (اللي اتستلم منها يرجع المخزن)، والجديدة تتضاف بند لوحدها.\n• إلغاء: تعديل عادي للبند.`)){e.preventDefault();e.stopImmediatePropagation();const nd=JSON.parse(JSON.stringify(d));V.ed=null;V.dr[tid]={};swOpen(tid,i,nd);return}
  if(o.sw&&!confirm('البند ده متبدّل بطلب العميل. تعدّله برضه؟')){e.preventDefault();e.stopImmediatePropagation();return}
  setTimeout(()=>{const n=(p.rows[tid]||[])[i];if(n&&n!==o){KEEP25.forEach(k=>{if(o[k]!=null&&n[k]==null)n[k]=o[k]});sv()}},0);return}
 const s=V.swF2;if(!s||s.tid!=tid)return;if(s.pid!=p.id){V.swF2=null;return}
 setTimeout(()=>{const L=p.rows[tid]||[];if(L.length!=s.n+1)return;const n=L[L.length-1],o=s.o;if(o&&L.includes(o)){o.sw=o.sw||{at:nowIso(),hk:{}};o.sw.to=t.z(n,p.sh);n.swf=n.swf||t.z(o,p.sh)}V.swF2=null;sv();render()},0)},true);
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-fc],[data-ced]');if(b&&V.swF2&&!b.dataset.ced)V.swF2=null;
 const x=e.target.closest&&e.target.closest('[data-del]');if(!x||V.v!='ph')return;const p=curP(),[tid,k]=x.dataset.del.split(':'),r=p&&(p.rows[tid]||[])[+k];if(!r)return;
 const m=r.sw&&r.cx?`البند ده متبدّل بـ «${r.sw.to||'بديل'}». لو مسحته، البديل هيفضل بند إضافي لوحده. تمسح؟`:r.swf?`البند ده بديل لـ «${r.swf}». لو مسحته، الأصلي هيفضل «${CXL}». تمسح؟`:'';
 if(m&&!confirm(m)){e.preventDefault();e.stopImmediatePropagation()}},true);
// warehouse: one rule (received − executed − damaged), damaged parts of a swap, with the reason
whSurplus=function(p){const m={};if(isHold(p))return m;ckRows(p).forEach(x=>{const r=x.r,d=Math.max(0,(+r.r||0)-(+r.x||0)-hkN(r)),why=r.sw?'تبديل بطلب العميل':r.cx?CXL:'فائض';
 whParts(x.t,r,p.sh).forEach(y=>{const k=whKey(y);let dd=y.pk?Math.max(0,pkv(r,'r',y.pk)-pkv(r,'x',y.pk)):d*y.f+(y.ep?egX(r,y.ep):0);if(r.sw&&r.sw.hk)dd=Math.max(0,dd-(+r.sw.hk[k]||0));
  if(!dd)return;if(!m[k])m[k]=Object.assign({},y,{q:0,why:[]});m[k].q=wq(m[k].q+dd);if(!m[k].why.includes(why))m[k].why.push(why)})});return m};
whtHtml=function(){const p=curP();if(!p)return '';const L=whPlan(p),add=L.filter(x=>x.dl>0),sub=L.filter(x=>x.dl<0),n=a=>a.reduce((s,x)=>s+Math.abs(x.dl),0);
 return `<div class="wcard"><h2>${ic('box')}يرجع للمخزن — صيدلية ${esc(p.no)}</h2><p class="sub">الراجع = المستلم − المتنفذ − الهالك لكل بند، بنوع رفوف البند. الهالك ما بيرجعش.</p>
 ${add.length?`<div class="ph"><small>هيتضاف <b>${add.length} صنف · ${wq(n(add))}</b></small></div>`:''}${sub.length?`<div class="alr"><small>⚠ الصيدلية اتعدلت بعد ترحيل سابق: هيتخصم <b>${sub.length} صنف · ${wq(n(sub))}</b></small></div>`:''}
 <div class="sc"><table class="ctab"><tr><th>الصنف</th><th>المقاس</th><th>الخامة</th><th>الرفوف</th><th>الكمية</th><th>السبب</th></tr>${L.map(x=>`<tr><td>${esc(x.ty)}${x.nm?`<small>${esc(whNm(x))}</small>`:''}</td><td>${esc(x.size||'—')}</td><td>${esc(x.mat||'—')}</td><td>${esc(SH[x.sh]||'—')}</td><td><b class="${x.dl<0?'c-exp':'c-rem'}">${x.dl>0?'+':''}${x.dl} ${whUnit(x.ty)}</b></td><td><small>${esc(x.dl<0?'اتعدّل بعد الترحيل':(x.why||[]).join(' + ')||'فائض')}</small></td></tr>`).join('')}</table></div>
 <div class="tt"><button class="pr big" data-whgo="1">${ic('check')}ترحيل للمخزن</button><button data-whno="1">تجاهل</button></div></div>`};
// ---- 9) completing a pharmacy with rows not fully executed
const cpLeft=p=>ckRows(p).filter(x=>{const r=x.r;if(r.cx)return false;const q=qn(r),pk=x.t.id=='eg'&&egSub(r,x.s),ao=x.t.id=='eg'&&egAO(r,x.s);return (!ao&&(+r.x||0)<q)||(pk&&SDS.some(([sd])=>pkv(r,'x',sd)<egN(r,x.s,sd)))});
let CPS=null;const _whOffer25=whOffer;whOffer=function(p,auto){if(!p||isHold(p))return;if(p.st=='مكتملة'&&!(CPS&&CPS.ok==p.id)){const L=cpLeft(p);if(L.length){CPS={pid:p.id,auto,v:CXR[1]};cpDraw();return}}if(CPS&&CPS.ok==p.id)CPS=null;return _whOffer25.call(this,p,auto)};
function cpDraw(){cShClose();const p=DB.ph.find(x=>x.id==CPS.pid),L=cpLeft(p),el=document.createElement('div');el.className='csh';
 el.innerHTML=`<div class="cshb"><b>✅ الصيدلية ${esc(p.no)} مكتملة — فيه ${L.length} بند متنفذهم أقل من المطلوب</b><div class="cnpl">${L.map(x=>`<div class="swp"><b>${esc(x.t.n)}</b><small>${esc(x.t.z(x.r,p.sh))} · متنفذ ${+x.r.x||0} من ${qn(x.r)}</small></div>`).join('')}</div>
 <div class="cshr"><button class="pr" data-cpx="all">✓ اتنفذوا كلهم</button></div>
 <small class="hint">أو «${CXL}» (بيتحسبوا في تقرير الإدارة واللي اتستلم منهم يرجع المخزن) — السبب:</small><div class="tt">${CXR.map(x=>`<button class="${CPS.v==x?'pr':''}" data-cpr="${esc(x)}">${esc(x)}</button>`).join('')}</div>
 <div class="cshr"><button data-cpx="cx">⏹ ${CXL}</button><button data-cpx="keep">سيبهم نواقص</button></div></div>`;document.body.appendChild(el)}
function cpGo(k){const p=DB.ph.find(x=>x.id==CPS.pid);if(!p)return;const L=cpLeft(p);
 if(k=='all')L.forEach(x=>{const r=x.r,q=qn(r);if(!(x.t.id=='eg'&&egAO(r,x.s))){r.x=q;if((+r.r||0)<q)r.r=q}if(x.t.id=='eg'&&egSub(r,x.s))SDS.forEach(([sd])=>{const n=egN(r,x.s,sd);r['xp'+sd]=n;if((+r['rp'+sd]||0)<n)r['rp'+sd]=n})});
 if(k=='cx')L.forEach(x=>{x.r.cx=1;x.r.cxn=CPS.v||CXR[1]});
 if(k!='keep'){p.modAt=nowIso();sv()}const a=CPS.auto;CPS={ok:p.id};cShClose();render();whOffer(p,a)}
// ---- 8) screw caps never below zero
capAuto=function(){const p=V&&V.p?DB.ph.find(x=>x.id==V.p):null;try{capSettle(p)}catch(e){}if(!p||!p.m23||uStoreRO()||!uEditP(p))return;const t=capN(p,'x'),c=+p.capx||0,d=t-c;if(!d)return;
 if(d<0){whAdd(CAPO,-d,'in','ph:'+p.no,'تصحيح '+CPNM+' (المتنفذ قل)');p.capx=t;return}const k=Math.min(d,Math.max(0,Math.floor(capStock())));if(k>0){whAdd(CAPO,-k,'out','ph:'+p.no,CPNM+' مع السايد أكريليك (متنفذ)');p.capx=c+k}};
function capSettle(skip){if(uStoreRO())return;let st=Math.floor(capStock());if(st<=0)return;DB.ph.forEach(q=>{if(q===skip||!q.m23||st<=0||!uEditP(q))return;const ow=capN(q,'x')-(+q.capx||0);if(ow<=0)return;const k=Math.min(ow,st);whAdd(CAPO,-k,'out','ph:'+q.no,CPNM+' مع السايد أكريليك (متركب قبل ما الأغطية توصل)');q.capx=(+q.capx||0)+k;st-=k})}
const capOwed=p=>p&&p.m23?Math.max(0,capN(p,'x')-(+p.capx||0)):0;
const _capHtml25=capHtml;capHtml=function(p){const h=_capHtml25(p),o=capOwed(p);return h&&o?h+`<div class="alr"><small>⚠ اتركب <b>${o}</b> ${CPNM} من غير ما يتخصموا (المخزن كان فاضي) — هيتخصموا لوحدهم أول ما تضيف أغطية للمخزن.</small></div>`:h};
function capFix25(){if(DB.cfg.m25c||uStoreRO())return;const W=WU().filter(x=>x.ty==CPNM&&+x.qty<0);if(!W.length){DB.cfg.m25c=1;return}
 try{snapLater('قبل تصحيح رصيد '+CPNM+' السالب (2.5)',JSON.stringify(DB))}catch(e){}let n=0;W.forEach(x=>{const v=-(+x.qty);n+=v;whAdd(x,v,'adj','fix','تصحيح: الرصيد ما ينزلش تحت الصفر (2.5)')});
 DB.ph.filter(p=>p.m23&&(+p.capx||0)>0).sort((a,b)=>String(b.modAt||'').localeCompare(String(a.modAt||''))).forEach(p=>{if(n<=0)return;const k=Math.min(n,+p.capx);p.capx=+p.capx-k;n-=k});DB.cfg.m25c=1;sv()}
// ---- 7) «وصفتي» → Acrylic boards
function wsfMig25(){if(DB.cfg.m25w)return;const re=/وصف(ا)?ت/,A=DB.cfg.adTypes||[],ix=[];A.forEach((n,i)=>{if(n&&re.test(n))ix.push(i)});
 const W=WU(),wi=W.filter(x=>re.test((x.ty||'')+' '+(x.nm||''))&&x.nm!='Wasfaty board');if(!ix.length&&!wi.length){DB.cfg.m25w=1;return}
 try{snapLater('قبل نقل «وصفتي» للأكريليك بورد (2.5)',JSON.stringify(DB))}catch(e){}
 const all=DB.ph.concat(HIDDB===DB?HID:[]);all.forEach(p=>{const R=p.rows||{};ix.forEach(i=>{const k='custom_'+i,L=R[k];if(!Array.isArray(L))return;R.ab=R.ab||[];L.forEach(r=>{const st=ABST.includes(String(r.nt||'').trim())?String(r.nt).trim():(p.mod=='تعديل براندنج'?ABIO:ABMK),o={it:'Wasfaty board',q:+r.q||0,stt:st,nt:ABST.includes(String(r.nt||'').trim())?'':(r.nt||'')};['r','x','_i','wf','hk','xi','xn'].forEach(f=>{if(r[f]!=null)o[f]=r[f]});R.ab.push(o)});delete R[k];p.modAt=nowIso()})});
 ix.forEach(i=>{A[i]=''});wi.forEach(x=>{x.ty='Acrylic boards';x.nm='Wasfaty board';x.sec='';x.size='48×80';x.mat='أكريليك';x.sh=-1});DB.cfg.m25w=1;sv()}
setTimeout(()=>{try{wsfMig25()}catch(e){console.warn('wsf25',e)}try{capFix25()}catch(e){console.warn('cap25',e)}},1500);
// ---- 11) custody
if(!CK.includes('عمالة')){CK.push('عمالة');CKC['عمالة']='FCE4D6'}
const _descOf25=descOf;descOf=function(kind,tm,comp){if(kind=='عمالة'){const m=CU().mem[cnk(comp)];return m&&m.desc?m.desc:'أجرة عامل تحميل وتنزيل بضاعة'}return _descOf25.apply(this,arguments)};
// ---- rendering: row buttons and tags, reason chips, hold button, custody camera
const _render0_25=render0;render0=function(){const out=_render0_25.apply(this,arguments);try{
 if(V.v=='ph'){const p=curP();if(p){const ro=uStoreRO()||!uEditP(p);
  document.querySelectorAll('.rw .bt button[data-ed]').forEach(b=>{const[tid,i]=b.dataset.ed.split(':'),r=(p.rows[tid]||[])[+i];if(!r)return;const sp=b.closest('.rw').querySelector('span');
   {const c=sp&&sp.querySelector('.cxt');if(c&&r.cx)c.textContent=cxTxt(r);if(c&&r.sw)c.remove()}
   if(ro||b.parentElement.querySelector('[data-cxo],[data-cxu]')||r.sw)return;if(r.cx)b.insertAdjacentHTML('beforebegin',`<button data-cxu="${tid}:${i}">↺ اتنفذ</button>`);else if(cxLeft(r)>0)b.insertAdjacentHTML('beforebegin',`<button data-cxo="${tid}:${i}" title="${CXL}">⏹ لم يُنفذ</button>`)});
  const pi=document.querySelector('details.pinfo .fm');if(pi&&!ro&&!pi.querySelector('[data-hld]'))pi.insertAdjacentHTML('beforeend',`<div class="tt"><button data-hld="${p.id}">⏸ حطها تحت الانتظار</button><small class="hint">تختفي من القوايم والتقارير والنواقص لحد ما تعتمدها.</small></div>`)}}
 document.querySelectorAll('.fm [data-k="xn"]').forEach(x=>{const l=x.closest('label')||x;if(l.nextElementSibling&&l.nextElementSibling.classList.contains('xnq'))return;l.insertAdjacentHTML('afterend',`<div class="tt xnq">${CXR.map(w=>`<button data-xnq="${x.dataset.t}|${esc(w)}"${x.value==w?' class="pr"':''}>${esc(w)}</button>`).join('')}</div>`)});
 const cp=document.querySelector('[data-cpic]');if(cp&&!document.querySelector('[data-cpicc]'))cp.insertAdjacentHTML('afterend',`<button data-cpicc="1">📷 صورة الفاتورة</button>`);
 }catch(e){console.warn(e)}return out};
function cPicCam(){const i=$('#cimg1');if(!i)return;const a=i.accept;i.accept='image/*';i.setAttribute('capture','environment');i.multiple=false;i.addEventListener('change',()=>{i.accept=a;i.removeAttribute('capture');i.multiple=true},{once:true,capture:true});i.click()}
// ---- clicks
const _v24Click25=v24Click;v24Click=function(d,b){
 if(d.cxo){const[t,i]=d.cxo.split(':');cxOpen(curP().id,t,i);return 1}if(d.cxu){const[t,i]=d.cxu.split(':');cxUndo(curP().id,t,i);return 1}
 if(d.cxr&&CXS){CXS.v=d.cxr;cxDraw();return 1}if(d.cxgo&&CXS){cxGo();return 1}
 if(d.cpr&&CPS){CPS.v=d.cpr;cpDraw();return 1}if(d.cpx&&CPS&&CPS.pid){cpGo(d.cpx);return 1}
 if(d.xnq){const k=d.xnq.indexOf('|'),t=d.xnq.slice(0,k),w=d.xnq.slice(k+1);if(V.dr&&t){V.dr[t]=V.dr[t]||{};V.dr[t].xn=w;render()}return 1}
 if(d.hld){const p=DB.ph.find(x=>x.id==d.hld);if(!p||!confirm('⏸ صيدلية '+p.no+' تحت الانتظار؟\nهتختفي من القوايم والتقارير والنواقص والمسار، وتلاقيها في سطر «⏸ تحت الانتظار».'))return 1;const m=isMnt(p);holdSet([p.id],1);goV({v:m?'mnt':'home',op:{[m?'__holdm':'__holdb']:true},dr:{},q:V.q});toastT('✓ صيدلية '+p.no+' تحت الانتظار');return 1}
 if(d.hldok){const p=HOLDL().find(x=>String(x.id)==String(d.hldok));if(!p)return 1;holdSet([p.id],0);render();toastT('▶ صيدلية '+p.no+' اتعتمدت ورجعت القايمة');return 1}
 if(d.hldall){const L=HOLDL().filter(p=>d.hldall=='__holdm'?isMnt(p):isBr(p));if(!L.length||!confirm('اعتماد '+L.length+' صيدلية ورجوعهم للقايمة؟'))return 1;holdSet(L.map(p=>p.id),0);render();toastT('▶ اتعتمد '+L.length);return 1}
 if(d.cpicc){cPicCam();return 1}
 return _v24Click25(d,b)};
const _v21Click25=v21Click;v21Click=function(d,b){if(d.tcx){const p=curP(),[tid,i]=d.tcx.split(':'),r=p&&(p.rows[tid]||[])[+i];if(!r)return 1;if(r.sw){alert('البند ده متبدّل بطلب العميل — استخدم «↺ إلغاء التبديل» من صفحة الصيدلية.');return 1}if(!r.cx){cxOpen(p.id,tid,i);return 1}}return _v21Click25(d,b)};
// ---- shortages / preparation skip held pharmacies (they are normally kept aside already)
const _nqLines25=nqLines;nqLines=function(p,k){return isHold(p)?[]:_nqLines25(p,k)};
const _prepRows25=prepRows;prepRows=function(p){return isHold(p)?[]:_prepRows25(p)};
// ---- hold file routing
const _syncRoute25=syncRoute;syncRoute=function(q,fn){if(q&&q.kind=='966-hold'){holdImp(q);return 1}return _syncRoute25(q,fn)};
const _whImpOpen25=whImpOpen;whImpOpen=function(q,fn){if(q&&q.kind=='966-hold')return holdImp(q);return _whImpOpen25(q,fn)};

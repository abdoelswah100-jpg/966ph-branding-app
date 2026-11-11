// ---------- warehouse (المخزن): stock per shelf type / ad type / name / material / size ----------
const WXT=['so'],NOSH=['ws','al','ab','dc','fr','c4','cm','ga','ds'];// made to measure, not kept in stock
function WU(){DB.wh=DB.wh||[];DB.wlog=DB.wlog||[];if(DB.wh.some(x=>!x.m22))whFix22();if(DB.wh.some(x=>!x.m38))whFix38();if(DB.wh.some(x=>!x.m39))whFix39();DB.wh.forEach(x=>{if(!x.m19){if(x.ty=='Floor Header'&&x.sh==2&&x.mat=='ستيكر')x.mat=FHM[0];x.m19=1}if(!x.m19w){if(x.ty=='Wall Header'&&x.sh==2&&x.mat=='ستيكر')x.mat=FHM[0];x.m19w=1}});return DB.wh}
const whNm=x=>x.sec&&String(x.nm||'').startsWith(x.sec)?String(x.nm):[x.sec,x.nm].filter(Boolean).join(' · ');
const whKey=x=>[x.sh,x.ty,nk(x.nm),nk(x.sec),nk(x.mat),String(x.size||'').replace(/\s+/g,'')].join('|');
const whUnit=ty=>ty=='Wall Header'||ty==RLTY?'متر':'قطعة';
const wq=v=>Math.round((+v||0)*100)/100;
const whLow=()=>WU().filter(x=>x.min!=null&&x.min!==''&&+x.qty<=+x.min).length;
function whLog(typ,x,qty,src,note){WU();DB.wlog.unshift({at:nowIso(),typ,id:x.id,qty:wq(qty),src:src||'',note:note||'',nm:x.nm,ty:x.ty,size:x.size,sh:x.sh});DB.wlog=DB.wlog.slice(0,3000)}
function whFind(k){return WU().find(x=>whKey(x)==k)}
function whAdd(o,qty,typ,src,note){const k=whKey(o);let x=whFind(k);if(!x){x=Object.assign({id:Date.now()+Math.floor(Math.random()*1e4),qty:0,min:'',unit:whUnit(o.ty)},o);WU().push(x)}x.qty=wq(+x.qty+qty);x.at=nowIso();whLog(typ,x,qty,src,note);return x}
// the pieces one row of a pharmacy stands for (composite types split in their parts), with the shelf type of the item
function whParts(t,r,s){if(WXT.includes(t.id)||t.auto)return [];const sh=rsh(r,s),z=t.z(r,s),sec=scOf(r),nm=r.nm||r.it||r.kd||'',L=[];
 if(t.id=='eg'){const m=egAO(r,s)?null:egSz(r,s);if(m){const sn=egSN(r,sh);if(egFh(r))L.push({ty:'End gandola - Header',nm,sec,size:m.h,mat:m.hm,f:egFh(r),ep:'h'});if(egFs(r))L.push({ty:'End gandola - Side',nm:sn?sn.nm:nm,sec:sn?sn.sec:sec,size:m.sd,mat:m.sm,f:egFs(r),ep:'s'});if(egFa(r))L.push({ty:'End gandola - Side Acrylic',nm:sn?sn.nm:nm,sec:sn?sn.sec:sec,size:m.sd,mat:'أكريليك',f:egFa(r),ep:'a'})}if(/Acrylic Pocket/.test(z)){const n=qn(r);SDS.forEach(([sd,nm2])=>{const c=egN(r,s,sd);if(c)L.push({ty:'Side Acrylic Pocket',nm:'',sec:'',size:nm2,mat:'أكريليك',f:n?c/n:0,pk:sd})})}}
 else if(t.id=='md'){if(mdH(r))L.push({ty:'Medicated - Header',nm,sec,size:String(SZ('md.h')),mat:SZ('mt.md'),f:1});if(mdS(r))L.push({ty:'Medicated - Side',nm,sec,size:String(SZ('md.s')[sh]),mat:SZ('mt.md'),f:1})}
 else if(t.id=='ga')GAP.forEach(([n,f,zz])=>L.push({ty:GAN+' - '+n,nm:'',sec:'',size:zz,mat:GAM,f}));
 else if(t.id=='wh'){L.push({ty:t.n,nm,sec,size:wood(r)?(r.len||'')+'':szOf(z),mat:mtOf(z),f:wood(r)?1:(+r.len||0)/100})}
 else if(t.id=='al'){L.push(r.pc?{ty:t.n,nm:'قطع 30×30',sec:r.sec,size:'30×30',mat:SZ('mt.al'),f:1}:{ty:t.n,nm:'',sec:r.sec,size:`حروف ${r.lh||'—'} سم · عرض ${r.w||'—'} سم`,mat:SZ('mt.al'),f:1})}
 else if(t.id=='ws'){L.push({ty:t.n,nm:r.kd||'',sec:r.sec,size:`${r.h}×${r.w}`,mat:SZ('mt.ws'),f:1})}
 else if(t.id=='ab'){const a=ABV(r.it);L.push({ty:t.n,nm:abNm(r),sec:'',size:a[0],mat:a[1],f:1})}
 else L.push({ty:t.n,nm,sec,size:szOf(z),mat:mtOf(z),f:1});
 return L.map(x=>Object.assign(x,{sh:NOSH.includes(t.id)?-1:sh}))}
// surplus = received - executed, per stock key
function whSurplus(p){const m={};ckRows(p).forEach(x=>{const r=x.r,d=Math.max(0,(+r.r||0)-(+r.x||0));whParts(x.t,r,p.sh).forEach(y=>{const dd=y.pk?Math.max(0,pkv(r,'r',y.pk)-pkv(r,'x',y.pk)):d*y.f+(y.ep?egX(r,y.ep):0);if(!dd)return;const k=whKey(y);if(!m[k])m[k]=Object.assign({},y,{q:0});m[k].q=wq(m[k].q+dd)})});return m}
function whPlan(p){const S=whSurplus(p),D=p.whT||{},L=[];new Set(Object.keys(S).concat(Object.keys(D))).forEach(k=>{const now=S[k]?S[k].q:0,was=+(D[k]||{}).q||0,dl=wq(now-was);if(dl)L.push(Object.assign({},S[k]||D[k],{k,dl,now}))});return L}
function whOffer(p,auto){const L=whPlan(p);if(!L.length){if(!auto)toastT('مفيش فائض جديد يترحّل للمخزن من الصيدلية دي');return}V.wt={pid:p.id,from:V.v,fp:V.p};goV({v:'wht',p:p.id,op:{},dr:{},q:V.q,wt:V.wt})}
function whtHtml(){const p=curP();if(!p)return '';const L=whPlan(p),add=L.filter(x=>x.dl>0),sub=L.filter(x=>x.dl<0),n=a=>a.reduce((s,x)=>s+Math.abs(x.dl),0);
 return `<div class="wcard"><h2>${ic('box')}ترحيل الفائض للمخزن — صيدلية ${esc(p.no)}</h2><p class="sub">الفائض = المستلم − المتنفذ لكل بند، بنوع رفوف البند.</p>
 ${add.length?`<div class="ph"><small>هيتضاف <b>${add.length} صنف · ${wq(n(add))}</b></small></div>`:''}${sub.length?`<div class="alr"><small>⚠ الصيدلية اتعدلت بعد ترحيل سابق: هيتخصم <b>${sub.length} صنف · ${wq(n(sub))}</b></small></div>`:''}
 <div class="sc"><table class="ctab"><tr><th>الصنف</th><th>المقاس</th><th>الخامة</th><th>الرفوف</th><th>الكمية</th></tr>${L.map(x=>`<tr><td>${esc(x.ty)}${x.nm?`<small>${esc(whNm(x))}</small>`:''}</td><td>${esc(x.size||'—')}</td><td>${esc(x.mat||'—')}</td><td>${esc(SH[x.sh]||'—')}</td><td><b class="${x.dl<0?'c-exp':'c-rem'}">${x.dl>0?'+':''}${x.dl} ${whUnit(x.ty)}</b></td></tr>`).join('')}</table></div>
 <div class="tt"><button class="pr big" data-whgo="1">${ic('check')}ترحيل للمخزن</button><button data-whno="1">تجاهل</button></div></div>`}
function whApply(){const p=curP();if(!p)return;const L=whPlan(p);p.whT=p.whT||{};L.forEach(x=>{whAdd({sh:x.sh,ty:x.ty,nm:x.nm,sec:x.sec,mat:x.mat,size:x.size},x.dl,x.dl>0?'in':'out','ph:'+p.no,x.dl>0?'فائض صيدلية':'تعديل صيدلية بعد الترحيل');p.whT[x.k]={sh:x.sh,ty:x.ty,nm:x.nm,sec:x.sec,mat:x.mat,size:x.size,q:x.now}});
 Object.keys(p.whT).forEach(k=>{if(!p.whT[k].q)delete p.whT[k]});p.whAt=nowIso();sv();snd('ok');toastT(`✓ اترحّل ${L.length} صنف للمخزن`);goV({v:'ph',p:p.id,op:{},dr:{},q:V.q})}
// pull from stock when an item is added to a pharmacy
// what the stock can cover for one row: header / side (and other parts) together, the Old Turkish acrylic pocket on its own
function whRowPlan(t,r,sh,st){const P=whParts(t,r,sh);if(!P.length)return null;const M=P.filter(y=>!y.pk),K=P.filter(y=>y.pk),qty=y=>st?whStQ(st,y):whQty(y);
 const nm=M.length?Math.min(Math.max(0,qn(r)-(+r.wf||0)),...M.map(y=>y.f>0?Math.floor((qty(y)+1e-9)/y.f):0)):0,nps={};K.forEach(y=>{nps[y.pk]=Math.min(Math.max(0,egN(r,sh,y.pk)-(+r['wfp'+y.pk]||0)),Math.floor(qty(y)+1e-9))});const np=K.reduce((a,y)=>a+nps[y.pk],0),pe=t.id=='eg'&&M.some(y=>y.ep),ex=pe?egEx(r,M,0,qty):{};return {M,K,nm:pe?0:nm,np,nps,ex,exAll:pe&&egExAll(r,M,ex),lab:mdLab(t,r)}}
const whTxt0=(L,t)=>[L.nm>0?`${L.nm} ${L.lab?L.lab:['eg','md'].includes(t&&t.id)?'هيدر وسايد':t&&t.id=='ga'?'طقم':'قطعة'}`:'',L.np>0?SDS.filter(([sd])=>(L.nps||{})[sd]>0).map(([sd,n])=>`${L.nps[sd]} جيب ${n}`).join(' + '):''].filter(Boolean).join(' + ');
function whTake0(p,t,r,L,note){L.M.forEach(y=>{if(L.nm>0)whTakeQ(y,L.nm*y.f,'ph:'+p.no,note)});L.K.forEach(y=>{const n=(L.nps||{})[y.pk]||0;if(!n)return;whTakeQ(y,n,'ph:'+p.no,note);r['wfp'+y.pk]=(+r['wfp'+y.pk]||0)+n;r['rp'+y.pk]=Math.min(egN(r,p.sh,y.pk),pkv(r,'r',y.pk)+n)});
 if(L.nm>0){r.wf=(+r.wf||0)+L.nm;r.r=Math.min(qn(r),(+r.r||0)+L.nm)}const ne=egExTake(p,r,L,note);return L.nm+L.np+ne}
// take from the warehouse for an item already in the pharmacy (what is not received yet); letters: any stock of the same section
function whFromOpts(p,t,r){if(!p||p._wh||p._rc||!WU().length)return [];const need=Math.max(0,qn(r)-(+r.r||0)),o=rolOpts(p,t,r);const L=whRowPlan(t,r,p.sh);
 if(L&&need>0&&L.nm>0)o.push({k:'x',n:Math.min(need,L.nm),txt:`${Math.min(need,L.nm)} ${L.lab||(['eg','md'].includes(t.id)?'هيدر وسايد':'قطعة')} (نفس المقاس)${whXT(t,r,p.sh,Math.min(need,L.nm))}`});
 if(L&&L.np>0)o.push({k:'p',n:L.np,txt:whTxt({nm:0,np:L.np,nps:L.nps,K:L.K},t)});if(L&&need>0&&egExN(L.ex))o.push({k:'e',n:egExN(L.ex),txt:egExT(L.ex)+(L.exAll?'':' — والباقي يتسجل نقص')+egExXT(L)});
 if(t.id=='al'&&!r.pc&&need>0){const key=L&&L.M[0]?whKey(L.M[0]):'';WU().filter(x=>x.ty==t.n&&x.sec==r.sec&&+x.qty>=1&&whKey(x)!=key&&x.nm!='قطع 30×30').forEach(x=>o.push({k:'a',id:x.id,n:Math.min(need,Math.floor(+x.qty)),txt:`${Math.min(need,Math.floor(+x.qty))} من ${x.sec} · ${x.size} (في المخزن ${wq(x.qty)})`}))}
 return o.concat(whOldOpts(p,t,r))}
function whFrom(p,t,r,i){const O=whFromOpts(p,t,r);if(!O.length)return toastT('مفيش حاجة في المخزن للبند ده');
 const tt=toast(`<span>📦 من المخزن للبند ده (${esc(t.n)}):${O.some(o=>o.rol)?'<br><b>🖨 فيه Floor Header رولاند بنفس المقاس. تسحب منه؟ (لو سحبت منه، نواقص الصيدلية دي هتتعلّم «اطبع على رولاند»)</b>':''}</span>${O.map((o,j)=>`<button class="pr${o.rol?' rolb':''}" data-whf2="${j}">اسحب ${esc(o.txt)}</button>`).join('')}<button data-tclose="1">لا</button>`);tt.classList.add('rem');tt._wf={pid:p.id,tid:t.id,i,O};snd('tick')}
function whFrom2(tt,j){const o=tt._wf,p=DB.ph.find(x=>x.id==o.pid);if(!p)return;const t=T.find(x=>x.id==o.tid),r=(p.rows[o.tid]||[])[o.i],c=o.O[j];if(!t||!r||!c)return;if(c.rol){p.rol=1;r.rol=1;p.modAt=nowIso()}
 if(c.k=='o'){const x=WU().find(y=>y.id==c.id);if(!x||+x.qty<c.n)return;whAdd(x,-c.n,'out','ph:'+p.no,'سحب '+x.ty+' لبند في الصيدلية');r.wo=(+r.wo||0)+c.n;sv();tt.remove();render();return toastT('✓ اتسحب من المخزون القديم')}
 if(c.k=='a'){const x=WU().find(y=>y.id==c.id);if(!x||+x.qty<c.n)return;whAdd(x,-c.n,'out','ph:'+p.no,x.old?'سحب تصميم قديم لبند في الصيدلية':x.rol?'سحب رولاند لبند في الصيدلية':'سحب لبند في الصيدلية (مقاس تاني)');r.wf=(+r.wf||0)+c.n;{const m_=rcvSnap(p,[r]);r.r=Math.min(qn(r),(+r.r||0)+c.n);rcvDiff(p,m_,'wh')}}
 else{const L=whRowPlan(t,r,p.sh);if(!L)return;if(c.k=='x'){L.np=0;L.nps={};L.ex={};L.nm=Math.min(L.nm,c.n)}else if(c.k=='e'){L.np=0;L.nps={}}else{L.nm=0;L.ex={}}whTake(p,t,r,L,'سحب لبند في الصيدلية')}
 sv();tt.remove();render();toastT('✓ اتسحب من المخزن واتحسب مستلم')}
function whPullOffer(p,t,r){if(!p||p._wh||p._rc||!WU().length)return;if(rolOpts(p,t,r).length){const i=(p.rows[t.id]||[]).indexOf(r);if(i>=0)return whFrom(p,t,r,i)}const L=whRowPlan(t,r,p.sh);if(!L||!(L.nm>0||L.np>0||egExN(L.ex)))return;
 const tt=toast(`<span>📦 موجود في المخزن للبند ده (${esc(t.n)}${r.nm?' · '+esc(r.nm):''}): <b>${whTxt(L,t)}</b>.${whXT(t,r,p.sh,L.nm)}${egExN(L.ex)?egExXT(L)+(L.exAll?'':' (والباقي يتسجل نقص)'):''} تسحبهم للصيدلية؟</span><button class="pr" data-whpull="1">اسحب</button><button data-tclose="1">لا</button>`);tt.classList.add('rem');tt._wp={pid:p.id,tid:t.id,i:(p.rows[t.id]||[]).indexOf(r)};snd('tick')}
function whPull(tt){const o=tt._wp,p=DB.ph.find(x=>x.id==o.pid);if(!p)return;const t=T.find(x=>x.id==o.tid),r=(p.rows[o.tid]||[])[o.i];if(!t||!r)return;const L=whRowPlan(t,r,p.sh);if(!L)return;const tx=whTxt(L,t);
 whTake(p,t,r,L,'سحب لبند في الصيدلية');sv();tt.remove();render();toastT(`✓ اتسحب من المخزن (${tx}) واتحسبوا مستلمين`)}
// maintenance: ask before taking from stock
function whMntOffer(x){if(!WU().length)return;const p=mPh(x.ph),sh=p?p.sh:null;const c=WU().filter(w=>+w.qty>0&&(w.ty==x.ad||w.ty.startsWith((x.ad||'')+' -')||(/^Fridge sticker - /.test(x.ad||'')&&w.ty=='Fridge sticker'&&w.nm==x.ad.slice(17)))&&(!x.sz||String(w.size).replace(/\s+/g,'')==String(x.sz).replace(/\s+/g,''))&&(sh==null||w.sh==sh||w.sh==-1));if(!c.length)return;
 const w=c.sort((a,b)=>b.qty-a.qty)[0],n=Math.min(+x.q||1,Math.floor(+w.qty));if(!(n>0))return;
 if(confirm(`📦 في المخزن ${f2(w.qty).replace(/\.00$/,'')} ${w.unit} من ${w.ty}${w.nm?' · '+w.nm:''} مقاس ${w.size}. تخصم ${n} للصيانة دي؟`)){whAdd(w,-n,'out','mnt:'+x.ph,'صيانة '+x.dt);sv();toastT('✓ اتخصم من المخزن')}}
// ---- screens
function whHtml(){const W0=WU(),F=V.wf=V.wf||{},q=(F.t||'').trim().toLowerCase();if(F.sh===undefined)F.sh=whDefSh(W0);
 const L=W0.filter(x=>(!F.old||x.old)&&(!F.rol||x.rol)&&(F.sh===''||F.sh==null||x.sh==F.sh)&&(!F.ty||x.ty==F.ty)&&(!F.sec||x.sec==F.sec)&&(!F.mat||x.mat==F.mat)&&(!F.low||x.min!==''&&x.min!=null&&+x.qty<=+x.min)&&(!q||[x.ty,x.nm,x.sec,x.size,x.mat].join(' ').toLowerCase().includes(q))).sort((a,b)=>a.sh-b.sh||a.ty.localeCompare(b.ty)||String(a.sec).localeCompare(String(b.sec))||String(a.nm).localeCompare(String(b.nm)));
 const pcs=L.filter(x=>x.unit!='متر').reduce((a,x)=>a+(+x.qty||0),0),mt=L.filter(x=>x.unit=='متر').reduce((a,x)=>a+(+x.qty||0),0),last=(DB.wlog||[])[0],u=a=>[...new Set(W0.map(x=>x[a]).filter(v=>v!==''&&v!=null))].sort();
 return `<div class="wcard cust"><div class="whst"><span><b>${W0.length}</b> صنف</span><span><b>${wq(W0.filter(x=>x.unit!='متر').reduce((a,x)=>a+(+x.qty||0),0))}</b> قطعة</span><span><b>${wq(W0.filter(x=>x.unit=='متر').reduce((a,x)=>a+(+x.qty||0),0))}</b> متر</span><span>آخر حركة <b>${last?fd(last.at).slice(0,10):'—'}</b></span></div>
 ${whLow()?`<div class="alr"><small>⚠ ${whLow()} صنف رصيده وصل للحد الأدنى أو أقل.</small></div>`:''}${whOutHtml()}${rolBar()}
 <div class="cbtn"><button class="pr" data-wha="1">${ic('add')}إضافة</button><button class="pr" data-whinv="1">${ic('list')}جرد جديد</button><button data-whlog="1">${ic('db')}سجل الحركات</button></div>
 <div class="cshare"><button data-whxl="share">${ic('sheet')}مشاركة Excel</button><button data-whpdf="share">${ic('share')}مشاركة PDF</button></div></div>
 <div class="wcard"><input class="sf" id="whq" placeholder="🔍 بحث بالاسم أو المقاس" value="${esc(F.t||'')}">
 ${whChips(W0,F)}<details class="whfl" data-id="__whf"${V.op.__whf||F.ty||F.sec||F.mat||F.low?' open':''}><summary>${ic('filter')} فلتر${[F.ty,F.sec,F.mat,F.low].filter(Boolean).length?' ('+[F.ty,F.sec,F.mat,F.low].filter(Boolean).length+')':''}</summary><div class="c2"><label>نوع الدعاية<select data-whf="ty"><option value="">الكل</option>${u('ty').map(x=>`<option${F.ty==x?' selected':''}>${esc(x)}</option>`).join('')}</select></label></div>
 <div class="c2"><label>القسم<select data-whf="sec"><option value="">الكل</option>${u('sec').map(x=>`<option${F.sec==x?' selected':''}>${esc(x)}</option>`).join('')}</select></label><label>الخامة<select data-whf="mat"><option value="">الكل</option>${u('mat').map(x=>`<option${F.mat==x?' selected':''}>${esc(x)}</option>`).join('')}</select></label></div>
 <label class="chk"><input type="checkbox" id="whlow"${F.low?' checked':''}> رصيد قليل بس</label></details></div>
 ${whGroups(L,F)}
 <div class="whsum">المعروض: <b>${L.length}</b> صنف · <b>${wq(pcs)}</b> قطعة · <b>${wq(mt)}</b> متر</div>`}
function wheHtml(){const d=V.we;if(!d)return '';const tys=[...new Set(T.filter(t=>!WXT.includes(t.id)&&!t.auto&&!['eg','md','ga'].includes(t.id)).map(t=>t.n).concat(['End gandola - Header','End gandola - Side','Side Acrylic Pocket','Medicated - Header','Medicated - Side',GAN+' - سايد',GAN+' - هيدر',RLTY,'أخرى']))];
 return `<div class="wcard ced"><div class="fm"><div class="c2"><label>نوع الرفوف<select data-wef="sh">${SH.map((x,i)=>`<option value="${i}"${+d.sh==i?' selected':''}>${x}</option>`).join('')}</select></label><label>نوع الدعاية<select data-wef="ty">${tys.map(x=>`<option${x==d.ty?' selected':''}>${esc(x)}</option>`).join('')}</select></label></div>
 <div class="c2"><label>القسم<select data-wef="sec"><option value="">—</option>${S7.concat(['Medicated']).map(x=>`<option${x==d.sec?' selected':''}>${esc(x)}</option>`).join('')}</select></label><label>المسمى<input data-wef="nm" value="${esc(d.nm)}"></label></div>
 <div class="c2"><label>المقاس (سم)<input data-wef="size" value="${esc(d.size)}" placeholder="مثلًا 11.5×57"></label><label>الخامة<input list="whml" data-wef="mat" value="${esc(d.mat)}"></label></div><datalist id="whml">${ALLM().map(x=>`<option value="${esc(x)}">`).join('')}</datalist>
 <div class="c2"><label>الكمية (${whUnit(d.ty)})<input type="number" inputmode="decimal" data-wef="qty" value="${esc(d.qty)}"></label><label>الحد الأدنى (اختياري)<input type="number" inputmode="decimal" data-wef="min" value="${esc(d.min)}"></label></div>
 <label>ملاحظات<input data-wef="note" value="${esc(d.note||'')}"></label></div>
 <div class="tt"><button class="pr big" data-whsave="1">${ic('check')}حفظ</button><button data-tab="wh">إلغاء</button>${d._old?`<button data-whdel="1" style="color:var(--rd)">${ic('trash')}مسح الصنف</button>`:''}</div></div>`}
function whSave(){const d=V.we;const qty=wq(d.qty);if(!(qty>=0))return alert('اكتب الكمية');if(!d.ty)return alert('اختار نوع الدعاية');const o={sh:+d.sh,ty:d.ty,nm:String(d.nm||'').trim(),sec:d.sec||'',mat:String(d.mat||'').trim(),size:String(d.size||'').trim()};
 if(d._old){const x=WU().find(y=>y.id==d._old);if(!x)return;const k2=whKey(o),other=WU().find(y=>y!==x&&whKey(y)==k2);if(other){if(!confirm('فيه صنف بنفس البيانات. أدمجهم في صنف واحد؟'))return;whAdd(other,qty,'adj','manual','دمج');DB.wh=WU().filter(y=>y!==x)}else{const dq=wq(qty-x.qty);Object.assign(x,o,{unit:whUnit(o.ty),min:d.min===''?'':+d.min,note:d.note||''});if(dq)whAdd(x,dq,'adj','manual','تعديل الصنف');else x.at=nowIso()}}
 else{const x=whAdd(o,qty,'in','manual','إضافة يدوي');x.min=d.min===''?'':+d.min;x.note=d.note||''}
 sv();snd('ok');V.we=null;goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT('✓ اتحفظ الصنف')}
function invHtml(){const L=WU().slice().sort((a,b)=>a.sh-b.sh||a.ty.localeCompare(b.ty)||String(a.nm).localeCompare(String(b.nm))),I=V.inv=V.inv||{},done=L.filter(x=>I[x.id]!==undefined&&I[x.id]!=='').length,only=V.invo;
 return `<div class="wcard"><h2>${ic('list')}جرد المخزن</h2><div class="pgw"><div class="pg"><i style="width:${L.length?Math.round(100*done/L.length):0}%"></i></div><small>${done}/${L.length} صنف اتعدّ</small></div><label class="chk"><input type="checkbox" id="invo"${only?' checked':''}> اللي ما اتعدّش بس</label>
 <div class="sc"><table class="ctab"><tr><th>الصنف</th><th>الرصيد</th><th>العدّ الفعلي</th><th>الفرق</th></tr>${L.filter(x=>!only||I[x.id]===undefined||I[x.id]==='').map(x=>{const c=I[x.id],df=c===undefined||c===''?null:wq(+c-x.qty);return `<tr><td>${esc(x.ty)}<small>${esc([whNm(x),x.size,SH[x.sh]].filter(Boolean).join(' · '))}</small></td><td><b>${wq(x.qty)}</b></td><td><input class="invc" type="number" inputmode="decimal" data-invc="${x.id}" value="${c===undefined?'':esc(c)}"></td><td><b class="${df==null?'':df<0?'c-exp':df>0?'c-rem':''}">${df==null?'—':(df>0?'+':'')+df}</b></td></tr>`}).join('')}</table></div>
 <div class="tt"><button class="pr big" data-invok="1">${ic('check')}اعتماد الجرد</button><button data-invx="1">إلغاء الجرد</button></div></div>`}
function invApply(){const I=V.inv||{},L=WU().filter(x=>I[x.id]!==undefined&&I[x.id]!=='');if(!L.length)return alert('ما اتعدّش أي صنف');const R=[];
 L.forEach(x=>{const before=wq(x.qty),c=wq(I[x.id]),df=wq(c-before);R.push({ty:x.ty,nm:x.nm,sec:x.sec,size:x.size,sh:x.sh,unit:x.unit,before,c,df});if(df)whAdd(x,df,'inv','inv','جرد');else x.at=nowIso()});
 DB.cfg.invAt=nowIso();DB.cfg.invBy=DB.cfg.dsup||'';DB.invs=(DB.invs||[]);DB.invs.unshift({at:DB.cfg.invAt,by:DB.cfg.invBy,rows:R});DB.invs=DB.invs.slice(0,12);V.inv={};sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q});toastT(`✓ اتعتمد الجرد (${R.length} صنف)`)}
function wlogHtml(){const L=(DB.wlog||[]).slice(0,400),TP={in:'إضافة',out:'سحب',adj:'تسوية',inv:'جرد'};return `<div class="wcard"><h2>${ic('db')}سجل الحركات</h2>${DB.invs&&DB.invs.length?`<div class="ph"><small>آخر جرد: ${fd(DB.invs[0].at)}${DB.invs[0].by?' · '+esc(DB.invs[0].by):''}</small><button data-invrep="x">${ic('sheet')}تقرير آخر جرد Excel</button><button data-invrep="p">${ic('share')}PDF</button></div>`:''}
 ${L.length?`<div class="sc"><table class="ctab"><tr><th>التاريخ</th><th>الحركة</th><th>الصنف</th><th>الكمية</th><th>المصدر</th></tr>${L.map(x=>`<tr><td class="cdt">${fd(x.at)}</td><td>${TP[x.typ]||x.typ}</td><td>${esc(x.ty)}<small>${esc([x.nm,x.size,SH[x.sh]].filter(Boolean).join(' · '))}</small></td><td><b class="${x.qty<0?'c-exp':'c-rem'}">${x.qty>0?'+':''}${x.qty}</b></td><td>${esc(x.src=='manual'?'يدوي':x.src=='inv'?'جرد':x.src.replace(/^ph:/,'صيدلية ').replace(/^mnt:/,'صيانة صيدلية '))}${x.note?`<small>${esc(x.note)}</small>`:''}</td></tr>`).join('')}</table></div>`:'<p class="em">لسه مفيش حركات.</p>'}</div>`}
// ---- exports
function whXlsx(){const L=WU().slice().sort((a,b)=>a.sh-b.sh||a.ty.localeCompare(b.ty)||String(a.nm).localeCompare(String(b.nm))),W=xlW(),NAVY='0B1B33',GOLD='F2B705',MUTE='5B6B80';
 const H=['م','نوع الرفوف','نوع الدعاية','القسم','المسمى','المقاس (سم)','الخامة','الرصيد','الوحدة','الحد الأدنى','آخر حركة'];
 W.put(1,0,'رصيد المخزن — '+((DB.cust&&DB.cust.cfg&&DB.cust.cfg.region)||'المنطقة الوسطى (الرياض)'),{sz:15,b:1,c:'FFFFFF',bg:NAVY,nb:1});W.merge('A1:K1');W.put(2,0,'تاريخ: '+TD().split('-').reverse().join('-')+' · '+(DB.cfg.dsup||''),{c:MUTE,nb:1});W.merge('A2:K2');
 H.forEach((h,i)=>W.put(4,i,h,{b:1,c:'FFFFFF',bg:NAVY}));L.forEach((x,j)=>{const lo=x.min!==''&&x.min!=null&&+x.qty<=+x.min;[j+1,SH[x.sh]||'',x.ty,x.sec||'',x.nm||'',x.size||'',x.mat||'',wq(x.qty),x.unit,x.min===''||x.min==null?'':+x.min,x.at?fd(x.at).slice(0,10):''].forEach((v,i)=>W.put(5+j,i,v,{b:i==7,c:i==7&&lo?'8B0000':'000000',bg:lo?'FDE2E2':(j%2?'F5F7FA':null)}))});
 const e=5+L.length;for(let i=0;i<11;i++)W.put(e,i,i==0?'الإجمالي':i==7?wq(L.filter(x=>x.unit!='متر').reduce((a,x)=>a+(+x.qty||0),0)):i==8?'قطعة':i==9?wq(L.filter(x=>x.unit=='متر').reduce((a,x)=>a+(+x.qty||0),0))+' متر':'',{b:1,c:NAVY,bg:GOLD});W.merge(`A${e}:G${e}`);[1,4].forEach(r=>W.ht(r,r==1?32:28));
 return xlBook([['المخزن',W.sheet({cols:[5,14,22,12,24,12,14,10,8,12,12],freeze:4,print:1})]],W,{print:'المخزن',rows:'$4:$4'})}
function whPdfEl(){const L=WU().slice().sort((a,b)=>a.sh-b.sh||a.ty.localeCompare(b.ty)||String(a.nm).localeCompare(String(b.nm))),el=document.createElement('div');el.innerHTML=`<div class="cpt"><b>رصيد المخزن</b><small>${TD().split('-').reverse().join('-')} · ${esc(DB.cfg.dsup||'')}</small></div><table class="cpdf"><tr><th>م</th><th>نوع الرفوف</th><th>نوع الدعاية</th><th>القسم · المسمى</th><th>المقاس</th><th>الخامة</th><th>الرصيد</th><th>الحد الأدنى</th></tr>${L.map((x,i)=>{const lo=x.min!==''&&x.min!=null&&+x.qty<=+x.min;return `<tr><td>${i+1}</td><td>${SH[x.sh]||''}</td><td>${esc(x.ty)}</td><td>${esc(whNm(x))}</td><td>${esc(x.size||'')}</td><td>${esc(x.mat||'')}</td><td class="${lo?'cnpt':''}"><b>${wq(x.qty)} ${x.unit}</b></td><td>${x.min===''||x.min==null?'':x.min}</td></tr>`}).join('')}</table>`;return el}
function invXlsx(v){const W=xlW(),NAVY='0B1B33',GOLD='F2B705',R=v.rows;W.put(1,0,'تقرير جرد المخزن — '+fd(v.at)+(v.by?' — '+v.by:''),{sz:14,b:1,c:'FFFFFF',bg:NAVY,nb:1});W.merge('A1:H1');
 ['م','نوع الرفوف','الصنف','المقاس','الرصيد قبل','العدّ','الفرق','الوحدة'].forEach((h,i)=>W.put(3,i,h,{b:1,c:'FFFFFF',bg:NAVY}));R.forEach((x,j)=>[j+1,SH[x.sh]||'',[x.ty,whNm(x)].filter(Boolean).join(' · '),x.size||'',x.before,x.c,x.df,x.unit].forEach((v2,i)=>W.put(4+j,i,v2,{b:i==6,c:i==6?(x.df<0?'8B0000':x.df>0?'1E7B45':'000000'):'000000'})));
 const e=4+R.length;for(let i=0;i<8;i++)W.put(e,i,i==0?'إجمالي الفروق':i==6?wq(R.reduce((a,x)=>a+x.df,0)):'',{b:1,c:NAVY,bg:GOLD});W.merge(`A${e}:F${e}`);return xlBook([['الجرد',W.sheet({cols:[5,14,40,12,12,10,10,8]})]],W)}
function invPdfEl(v){const el=document.createElement('div');el.innerHTML=`<div class="cpt"><b>تقرير جرد المخزن</b><small>${fd(v.at)}${v.by?' · '+esc(v.by):''}</small></div><table class="cpdf"><tr><th>م</th><th>نوع الرفوف</th><th>الصنف</th><th>المقاس</th><th>الرصيد قبل</th><th>العدّ</th><th>الفرق</th></tr>${v.rows.map((x,i)=>`<tr><td>${i+1}</td><td>${SH[x.sh]||''}</td><td>${esc([x.ty,whNm(x)].filter(Boolean).join(' · '))}</td><td>${esc(x.size||'')}</td><td>${x.before}</td><td>${x.c}</td><td class="${x.df<0?'cnpt':''}"><b>${x.df>0?'+':''}${x.df}</b></td></tr>`).join('')}<tr class="ctot"><td colspan="6">إجمالي الفروق</td><td>${wq(v.rows.reduce((a,x)=>a+x.df,0))}</td></tr></table>`;return el}
async function whExp(kind,mode,inv){const nm=(inv?'جرد المخزن - ':'رصيد المخزن - ')+TD();if(kind=='x'){const bl=inv?invXlsx(inv):whXlsx(),n=nm+'.xlsx';if(CAPN())return nativeSave(n,bl,bl.type,mode!='save');return mode=='save'?out(n,bl,bl.type):shr(n,bl,bl.type)}
 return sharePdf({src:inv?invPdfEl(inv):whPdfEl(),name:nm,title:inv?'تقرير جرد المخزن':'رصيد المخزن'})}
// add to the warehouse with the same item cards as a pharmacy: the rows wait here, then 'حفظ في المخزن' splits them in their parts
let WHPO=null;
const WHAK=()=>'wha966:'+(U().id||'');
function WHP(){if(!WHPO){let rows={};try{rows=JSON.parse(localStorage.getItem(WHAK())||'{}')||{}}catch(e){}WHPO={id:-7,_wh:1,no:'المخزن',sh:+(DB.cfg.whsh||0),rows,an:{},st:'جاري',uid:U().id}}return WHPO}
function whaKeep(){try{const n=whaN();if(n)localStorage.setItem(WHAK(),JSON.stringify(WHPO.rows));else localStorage.removeItem(WHAK())}catch(e){}}
const whaN=()=>Object.values(WHP().rows).reduce((a,r)=>a+r.length,0);
function whaHtml(){const p=WHP(),n=whaN();whaKeep();
 return `<div class="wcard"><h2>${ic('box')}إضافة للمخزن</h2><p class="sub">اختار نوع الدعاية والمسمى زي ما بتضيف في الصيدلية. البنود المركّبة (End gandola و Medicated) بتتقسم لوحدها هيدر وسايد.</p><label>نوع الرفوف<select id="whash">${SH.map((x,i)=>`<option value="${i}"${p.sh==i?' selected':''}>${x}</option>`).join('')}</select></label>${rolOn()&&p.sh!=2?`<label class="chk rolt${V.whRol?' on':''}"><input type="checkbox" id="whrol"${V.whRol?' checked':''}> 🖨 Floor Header رولاند (مات فيلم طباعة رولاند — ألوان مختلفة، بيتحفظ لوحده)</label>`:''}</div>
 ${TY(p).filter(t=>!WXT.includes(t.id)&&!t.auto).map(t=>card(t,p)).join('')}
 <div class="tt what"><button class="pr big" data-whaok="1"${n?'':' disabled'}>${ic('check')}حفظ في المخزن${n?` (${n} بند)`:''}</button><button data-whax="1">إلغاء</button></div><button class="lnk" data-whacp="1">نسخ بنود صيدلية (وبعدين عدّل العدد) ›</button><button class="lnk" data-whcap="1">إضافة غطاء مسمار ›</button><button class="lnk" data-whr="1">إضافة رول ستيكر (تخطيط / ثلجي شفاف) ›</button><button class="lnk" data-whadd="1">صنف غير مسجل أو بمقاس خاص (كتابة يدوي) ›</button><button class="lnk" data-whoa="1">🕰 إضافة مخزون قديم (تصميم قديم / أكريليك فاضي) ›</button><button class="lnk" data-whimp="1">📥 استيراد أصناف مخزن من ملف ›</button><button class="lnk" data-whcat="1">📤 تصدير كتالوج الأصناف (لملفات الجرد) ›</button><input type="file" id="whimpin" accept=".json,application/json" hidden>${rolOn()?'':'<button class="lnk" data-rolon="1">🖨 فتح خيار رولاند تاني ›</button>'}`}
function whaSave(){const p=WHP(),rl=V.whRol&&rolOn();let n=0;TY(p).forEach(t=>(p.rows[t.id]||[]).forEach(r=>{const q=qn(r);whParts(t,r,p.sh).forEach(y=>{const R=rl&&t.id=='fh'&&y.sh!=2;const x=whAdd({sh:y.sh,ty:y.ty,nm:y.nm,sec:y.sec,mat:R?'مات فيلم'+ROLM:y.mat,size:y.size},wq(q*y.f),'in','manual',R?'إضافة للمخزن · رولاند':'إضافة للمخزن');if(R)x.rol=1;n++})}));V.whRol=false;
 WHPO.rows={};whaKeep();WHPO=null;sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT(`✓ اتضاف ${n} صنف للمخزن`)}
function whClick(d,b){
 if(d.wha){WHPO=null;goV({v:'wha',op:{},dr:{},q:V.q,wf:V.wf});return 1}
 if(d.whaok){whaSave();return 1}
 if(d.whcat){whCatExport();return 1}
 if(d.whax){if(whaN()&&!confirm('البنود دي ما اتحفظتش في المخزن. تلغيها؟'))return 1;WHP().rows={};whaKeep();WHPO=null;goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});return 1}
 if(d.whdone){const p=DB.ph.find(x=>x.id==d.whdone);if(!p)return 1;if(p.st!='مكتملة'&&confirm('تحويل حالة الصيدلية إلى «مكتملة»؟')){p.st='مكتملة';sv()}whOffer(p);return 1}
 if(d.whgo){whApply();return 1}if(d.whno){goV({v:'ph',p:V.p,op:{},dr:{},q:V.q});return 1}
 if(d.whfrom){const p=curP(),[tid,i]=d.whfrom.split(':'),t=T.find(x=>x.id==tid),r=p&&(p.rows[tid]||[])[+i];if(r)whFrom(p,t,r,+i);return 1}
 if(d.whf2!=null){const tt=b.closest('.toast');if(tt&&tt._wf)whFrom2(tt,+d.whf2);return 1}
 if(d.whpull){const tt=b.closest('.toast');if(tt&&tt._wp)whPull(tt);return 1}
 if(d.whadd){V.we={sh:0,ty:'Floor Header',sec:'',nm:'',mat:'',size:'',qty:'',min:''};goV(Object.assign(V,{v:'whe'}));return 1}
 if(d.whed){const x=WU().find(y=>y.id==d.whed);if(x){V.we=Object.assign({},x,{_old:x.id});goV(Object.assign(V,{v:'whe'}))}return 1}
 if(d.whsave){whSave();return 1}
 if(d.whdel){if(!confirm('تمسح الصنف ده من المخزن؟'))return 1;const x=WU().find(y=>y.id==V.we._old);if(x){whLog('adj',x,-x.qty,'manual','مسح الصنف');DB.wh=WU().filter(y=>y!==x)}sv();V.we=null;goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});return 1}
 if(d.whst){const[id,dv]=d.whst.split(':'),x=WU().find(y=>y.id==id);if(x){if(+x.qty+(+dv)<0)return 1;whAdd(x,+dv,'adj','manual','');sv();snd('tick');render()}return 1}
 if(d.whinv){V.inv={};goV(Object.assign(V,{v:'inv'}));return 1}
 if(d.invok){if(confirm('اعتماد الجرد هيعدّل أرصدة الأصناف اللي اتعدّت. تكمل؟'))invApply();return 1}
 if(d.invx){if(Object.keys(V.inv||{}).length&&!confirm('إلغاء الجرد؟ مفيش أي رصيد هيتغير.'))return 1;V.inv={};goV({v:'wh',op:{},dr:{},q:V.q});return 1}
 if(d.whlog){goV(Object.assign(V,{v:'wlog'}));return 1}
 if(d.whxl){whExp('x',d.whxl);return 1}if(d.whpdf){whExp('p',d.whpdf);return 1}
 if(d.invrep){const v=(DB.invs||[])[0];if(v)whExp(d.invrep,'share',v);return 1}
 return 0}
function whChange(x){
 if(x.id=='whash'){WHP().sh=+x.value;DB.cfg.whsh=+x.value;V.dr={};svq();render();return 1}
 if(x.id=='whq'){V.wf=V.wf||{};V.wf.t=x.value;render();const i=$('#whq');if(i){i.focus();i.setSelectionRange(i.value.length,i.value.length)}return 1}
 if(x.dataset.whf){V.wf=V.wf||{};V.wf[x.dataset.whf]=x.value;render();return 1}
 if(x.id=='whlow'){V.wf=V.wf||{};V.wf.low=x.checked;render();return 1}
 if(x.id=='invo'){V.invo=x.checked;render();return 1}
 if(x.dataset.invc){V.inv=V.inv||{};V.inv[x.dataset.invc]=x.value;render();return 1}
 if(x.dataset.wef&&V.we){V.we[x.dataset.wef]=x.value;if(x.dataset.wef=='ty')render();return 1}
 return 0}
document.addEventListener('input',e=>{const x=e.target;if(x.dataset&&x.dataset.wef&&V.we&&V.v=='whe'&&x.tagName=='INPUT')V.we[x.dataset.wef]=x.value;if(x.id=='whq')whChange(x)});

// ---- sticker rolls: width 1 m, 50 m a roll; stock in meters
const RLTY='رول ستيكر',RLM=50,RLK=['تخطيط','ثلجي شفاف','أخرى'],RLS=['Beauty','Personal','Health','Baby','Pharmacy','Mizan'];
const rlTxt=m=>{m=wq(m);const n=Math.floor((m+1e-9)/RLM),r=wq(m-n*RLM);return n&&r?`${n} رول + ${r} م`:n?`${n} رول`:`${r} م`};
const rlStock=sec=>wq(WU().filter(x=>x.ty==RLTY&&x.nm=='تخطيط'&&x.sec==sec).reduce((a,x)=>a+(+x.qty||0),0));
// linear meters of تخطيط needed per section: each piece laid on a 1 m wide roll the short way (approximate, no waste)
function rlNeed(p){const o={};(p.rows.ws||[]).forEach(r=>{if(r.kd!='تخطيط')return;const h=+r.h||0,w=+r.w||0,q=+r.q||0;if(!h||!w||!q)return;const op=[];if(w<=100)op.push(h);if(h<=100)op.push(w);const len=op.length?Math.min(...op):h*w/100;o[r.sec]=wq((o[r.sec]||0)+len*q/100)});return o}
function rlBox(p){const N=rlNeed(p),ks=Object.keys(N);if(!ks.length)return '';const rr=p.rolls||{};
 return `<div class="sxw rlw np"><b>${ic('box')} رولات التخطيط (تنبيه ليك بس، مش بيتبعت)</b>${ks.map(k=>{const st=rlStock(k),def=N[k]>st,c=rr[k];return `<div class="rlr${def?' bad':''}"><span><b style="${bgc(COL[k]||'#999')};padding:0 6px;border-radius:6px">${esc(k)}</b> محتاج حوالي <b>${N[k]} م</b> · في المخزن <b>${st?rlTxt(st):'0'}</b> ${def?'← <b class="c-exp">⚠ محتاج رول</b>':'← ✓ يكفي'}</span>${c?`<span class="rlq">مطلوب ${c} رول <button class="np" data-rreq="${esc(k)}:-1">−</button><button class="np" data-rreq="${esc(k)}:1">+</button></span>`:`<button class="${def?'pr':''}" data-rreq="${esc(k)}:${Math.max(1,Math.ceil((N[k]-st)/RLM))}">اطلب رول</button>`}</div>`}).join('')}<small>الحساب تقريبي: كل قطعة على رول عرضه 1 م، من غير الهالك.</small></div>`}
const rlReqHtml=p=>{const rr=p.rolls||{},ks=Object.keys(rr).filter(k=>rr[k]>0);return ks.length?`<h3>مطلوب رولات</h3><div class="sc"><table><tr><th>الرول</th><th>القسم</th><th>المقاس</th><th>العدد</th></tr>${ks.map(k=>`<tr><td>تخطيط</td><td style="${bgc(COL[k]||'#999')};font-weight:700">${esc(k)}</td><td>عرض 1 م × ${RLM} م</td><td><b>${rr[k]} رول</b></td></tr>`).join('')}</table></div>`:''};
const rlReqTxt=p=>{const rr=p.rolls||{},ks=Object.keys(rr).filter(k=>rr[k]>0);return ks.length?['','مطلوب رولات:'].concat(ks.map(k=>`  - تخطيط ${k} · عرض 1 م × ${RLM} م × ${rr[k]} رول`)):[]};
// add rolls to the warehouse
function whrHtml(){const d=V.wr=V.wr||{k:'تخطيط',sec:'Beauty',x:'',n:'',m:''};const tot=(+d.n||0)*RLM+(+d.m||0);
 return `<div class="wcard ced"><h2>${ic('box')}إضافة رول ستيكر</h2><p class="sub">الرول عرضه 1 متر وطوله ${RLM} متر. الرصيد بيتحسب بالمتر.</p><div class="fm">
 <label>النوع<select data-wrf="k">${RLK.map(x=>`<option${x==d.k?' selected':''}>${x}</option>`).join('')}</select></label>
 ${d.k=='تخطيط'?`<label>القسم<select data-wrf="sec">${RLS.map(x=>`<option${x==d.sec?' selected':''}>${x}</option>`).join('')}</select></label>`:''}${d.k=='أخرى'?`<label>اسم النوع<input data-wrf="x" value="${esc(d.x)}"></label>`:''}
 <div class="c2"><label>رولات جديدة (كل رول ${RLM} م)<input type="number" inputmode="numeric" min="0" data-wrf="n" value="${esc(d.n)}"></label><label>رول مفتوح: الباقي منه (متر)<input type="number" inputmode="decimal" min="0" data-wrf="m" value="${esc(d.m)}"></label></div>
 <div class="ph"><small>هيتضاف: <b id="wrtot">${wq(tot)} م${tot?' = '+rlTxt(tot):''}</b></small></div></div>
 <div class="tt"><button class="pr big" data-wrsave="1">${ic('check')}حفظ في المخزن</button><button data-wrx="1">إلغاء</button></div></div>`}
function whrSave(){const d=V.wr,tot=wq((+d.n||0)*RLM+(+d.m||0));if(!(tot>0))return alert('اكتب عدد الرولات أو الباقي بالمتر');if(d.k=='أخرى'&&!String(d.x||'').trim())return alert('اكتب اسم النوع');
 whAdd({sh:-1,ty:RLTY,nm:d.k=='أخرى'?String(d.x).trim():d.k,sec:d.k=='تخطيط'?d.sec:'',mat:'',size:'عرض 1 م'},tot,'in','manual','رول ستيكر');V.wr=null;sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT('✓ اتضاف '+rlTxt(tot))}
function rlClick(d){
 if(d.whr){V.wr=null;goV({v:'whr',op:{},dr:{},q:V.q,wf:V.wf});return 1}
 if(d.wrsave){whrSave();return 1}if(d.wrx){V.wr=null;goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});return 1}
 if(d.rreq){const p=curP();if(!p)return 1;const i=d.rreq.lastIndexOf(':'),k=d.rreq.slice(0,i),n=+d.rreq.slice(i+1);p.rolls=p.rolls||{};const c=p.rolls[k]||0;p.rolls[k]=c?Math.max(0,c+n):n;if(!p.rolls[k])delete p.rolls[k];sv();render();return 1}
 return 0}
function rlChange(x){if(x.dataset&&x.dataset.wrf&&V.wr){V.wr[x.dataset.wrf]=x.value;if(x.tagName=='SELECT')render();return 1}return 0}
document.addEventListener('input',e=>{const x=e.target;if(x.dataset&&x.dataset.wrf&&V.wr&&x.tagName=='INPUT'){V.wr[x.dataset.wrf]=x.value;const t=$('#wrtot');if(t){const v=wq((+V.wr.n||0)*RLM+(+V.wr.m||0));t.textContent=v+' م'+(v?' = '+rlTxt(v):'')}}});
// ---- company documents: built-in files + a newer copy on this device (IndexedDB 'doc:<id>', meta in cfg.cdocs)
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
// old design: banner + photos in the print summary; curve note for side acrylic
const odBanner=p=>p.dz=='قديم'?'<div class="sxn odz">⚠ الصيدلية دي تصميم قديم — يطبع حسب الطلب (شوف صور التصميم القديم في الآخر)</div>':odNeed(p)?'<div class="sxn odz">⚠ فيه بنود تصميم قديم (مكتوب جنبها) — تطبع حسب الطلب</div>':'';
const odPhotos=p=>{const L=phoList(p,'o');return L.length?`<h3>صور التصميم القديم</h3><div class="odg">${L.map(x=>`<img data-phod="${phoKey(p.id,'o',x.k)}" alt="">`).join('')}</div>`:''};
async function odFill(){for(const im of document.querySelectorAll('img[data-phod]')){if(im.getAttribute('src'))continue;const b=await idbGet(im.dataset.phod);if(!b)continue;const u=URL.createObjectURL(b),d=await shrink(u,900);URL.revokeObjectURL(u);if(d)im.src=d}}
const hasCurve=p=>((p.rows.saw||[]).length+(p.rows.saf||[]).length)>0||((p.rows.eg||[]).some(r=>egPK(r,p.sh)));
const curveNote=p=>hasCurve(p)?`<div class="ph curve"><small>ℹ ${CURVE}</small></div>`:'';
// start / end dates of every pharmacy (management reports)
const ddm=d=>d?d.split('-').reverse().join('-'):'—';
const phDates=P=>P.length?`<h3>تواريخ الصيدليات</h3><div class="sc"><table><tr><th>الصيدلية</th><th>الحي</th><th>تاريخ البدء</th><th>تاريخ الانتهاء</th><th>الحالة</th></tr>${P.slice().sort(pSort).map(p=>`<tr><td><b>${esc(p.no)}</b></td><td>${esc(p.name||'—')}</td><td>${ddm(p.ds)}</td><td>${ddm(p.de)}</td><td style="background:${SC[p.st]||'#7A8699'};color:#fff;font-weight:700">${esc(p.st||'')}</td></tr>`).join('')}</table></div>`:'';
// month close: what is still open for the month
function mcloseHtml(){const m=V.mo||MN(),L=DB.ph.filter(p=>p.mo==m&&isBr(p)).sort(pSort),C=CU(),M=C.m[m],sec=(t,ok,rows)=>`<div class="wcard mcl${ok?' ok':''}"><h3>${ok?'✅':'⚠'} ${t}</h3>${ok?'<small>تمام</small>':rows}</div>`,ln=(a,txt)=>`<button class="mcr" ${a}>${txt} ›</button>`;
 const nc=L.filter(p=>p.st!='مكتملة'),sp=L.filter(p=>p.st=='مكتملة'&&whPlan(p).length),nx=L.filter(p=>nqLines(p,'x').length),nr=L.filter(p=>nqLines(p,'r').length),rv=L.filter(p=>revSt(p)!='ok');
 return `<div class="wcard"><h2>${ic('check')}إقفال شهر ${m.slice(5)}-${m.slice(0,4)}</h2><p class="sub">اللي فاضل قبل ما تقفل الشهر. اضغط على أي سطر يوديك له.</p></div>`
 +sec('صيدليات لسه مش مكتملة ('+nc.length+')',!nc.length,nc.map(p=>ln(`data-go="${p.id}"`,`صيدلية ${esc(p.no)} · ${esc(p.st||'لم تبدأ')}`)).join(''))
 +sec('فائض ما اترحّلش للمخزن ('+sp.length+')',!sp.length,sp.map(p=>ln(`data-whdone="${p.id}"`,`صيدلية ${esc(p.no)} · ${whPlan(p).length} صنف`)).join(''))
 +sec('نواقص التنفيذ ('+nx.length+')',!nx.length,nx.map(p=>ln(`data-mcnq="x:${p.id}"`,`صيدلية ${esc(p.no)} · ${nqLines(p,'x').reduce((a,y)=>a+y.d,0)} قطعة`)).join(''))
 +sec('نواقص الطباعة ('+nr.length+')',!nr.length,nr.map(p=>ln(`data-mcnq="r:${p.id}"`,`صيدلية ${esc(p.no)} · ${nqLines(p,'r').reduce((a,y)=>a+y.d,0)} قطعة`)).join(''))
 +sec('المراجعة ('+rv.length+')',!rv.length,rv.map(p=>ln(`data-go="${p.id}"`,`صيدلية ${esc(p.no)} · ${revSt(p)=='old'?'مراجعة قديمة':'ما اتراجعتش'}`)).join(''))
 +sec('العهدة',!!(M&&M.xat&&M.items.length),M&&M.items.length?ln('data-tab="cust"',M.xat?`آخر تصدير ${fd(M.xat)} · فيه تعديل بعده؟ صدّر تاني`:`${M.items.length} فاتورة · لسه ما اتصدّرتش Excel / PDF`):'<small>مفيش فواتير للشهر ده</small>')}
// ---------- v1.9: receiving (الاستلام) separate from the pharmacy: the pharmacy keeps the request and the executed,
// the received is entered here by pharmacy number (same item cards), every change of received is logged in p.rcv
const RCVM='المستلم بيتسجل من شاشة 📥 الاستلام (في الشريط اللي تحت) برقم الصيدلية';
const tkRO=k=>String(k||'')[0]=='r'&&V.v!='rcv';
const RCS={rcv:'استلام من الطباعة',xs:'مش مطلوب → المخزن',wh:'من المخزن',xr:'اتعدّل من التنفيذ',old:'رصيد سابق',q:'مستني تسجيل الصيدلية'};
function rid(){return Date.now().toString(36)+Math.random().toString(36).slice(2,7)}
function RQ(){return DB.rcvq=DB.rcvq||[]}
function rcvRows(p){const L=[];Object.keys(p.rows||{}).forEach(tid=>{const a=p.rows[tid];if(Array.isArray(a))a.forEach(r=>{if(r&&typeof r=='object')L.push([tid,r])})});return L}
function rcvIds(p){const u=new Set();rcvRows(p).forEach(([,r])=>{if(!r._i||u.has(r._i))r._i=rid();u.add(r._i)})}
function migRCV(p){if(p.m20)return;p.rcv=p.rcv||[];rcvIds(p);rcvRows(p).forEach(([tid,r])=>{[['',r.r],['R',r.rpR],['L',r.rpL]].forEach(([sd,v])=>{v=+v||0;if(v>0)p.rcv.push({id:rid(),dt:p.ckd||'',at:'',tid,rid:r._i,sd,n:v,src:'old'})})});p.m20=1}
const tOf=(p,tid)=>T.find(x=>x.id==tid)||TY(p).find(x=>x.id==tid);
function rcvZ(p,tid,r,sd){const t=tOf(p,tid);if(!t)return tid;let z='';try{z=t.z(r,p.sh)}catch(e){}return t.n+': '+z+(sd?' · Side Acrylic Pocket '+(sd=='R'?'يمين':'يسار'):'')}
function rcvSnap(p,rows){rcvIds(p);const m=new Map();(rows||rcvRows(p).map(x=>x[1])).forEach(r=>m.set(r,[+r.r||0,+r.rpR||0,+r.rpL||0]));return m}
function rcvLog(p,tid,r,d,sd,src,dt){p.rcv=p.rcv||[];if(!r._i)r._i=rid();dt=dt||TD();sd=sd||'';let e=p.rcv.find(x=>x.rid==r._i&&(x.sd||'')==sd&&x.src==src&&x.dt==dt);
 if(e){e.n=wq(e.n+d);e.at=nowIso();e.z=rcvZ(p,tid,r,sd);if(!e.n)p.rcv.splice(p.rcv.indexOf(e),1)}else{e={id:rid(),dt,at:nowIso(),tid,rid:r._i,sd,n:wq(d),src,z:rcvZ(p,tid,r,sd)};p.rcv.push(e)}p.modAt=nowIso();return e}
function rcvDiff(p,m,src,dt){const o=[];rcvRows(p).forEach(([tid,r])=>{if(!m.has(r))return;const a=m.get(r),c=[+r.r||0,+r.rpR||0,+r.rpL||0];['','R','L'].forEach((sd,j)=>{const d=wq(c[j]-a[j]);if(d)o.push({t:tOf(p,tid),r,sd,d,e:rcvLog(p,tid,r,d,sd,src,dt)})})});return o}
function rcvAfter(p,m){const R=V.v=='rcv',L=rcvDiff(p,m,R?'rcv':'xr',R?(V.rd||TD()):TD());if(!R)rcvXr(p,L)}
// every take from the warehouse is logged as received 'من المخزن'
function whTake(p,t,r,L,note){const m=rcvSnap(p,[r]),k=whTake0(p,t,r,L,note);rcvDiff(p,m,'wh');return k}
// executed > received: ask if the extra came from the warehouse (then it is taken out of stock)
function whAv(p,t,r,sd){const P=whParts(t,r,p.sh),q=y=>whQty(y);if(sd){const y=P.find(z=>z.pk==sd);return y?Math.floor(q(y)+1e-9):0}const M=P.filter(z=>!z.pk);return M.length?Math.min(...M.map(y=>y.f>0?Math.floor((q(y)+1e-9)/y.f):0)):0}
function whDed(p,t,r,n,sd,note){const k=Math.min(n,whAv(p,t,r,sd));if(!(k>0))return 0;const P=whParts(t,r,p.sh);if(sd){const y=P.find(z=>z.pk==sd);whTakeQ(y,k,'ph:'+p.no,note);r['wfp'+sd]=(+r['wfp'+sd]||0)+k}else{P.filter(z=>!z.pk).forEach(y=>whTakeQ(y,k*y.f,'ph:'+p.no,note));r.wf=(+r.wf||0)+k}return k}
function rcvXr(p,L){if(!p||p._wh||p._rc||!WU().length)return;const C=L.filter(o=>o.d>0&&o.t&&o.e&&o.e.n>0&&whAv(p,o.t,o.r,o.sd)>0);if(!C.length)return;document.querySelectorAll('.toast.rcx').forEach(x=>x.remove());
 const tt=toast(`<span>📦 المتنفذ زاد عن المستلم${C.length>1?' في '+C.length+' بند':''} وفيه رصيد في المخزن. الزيادة جت من المخزن؟${C.some(o=>!o.sd&&whXT(o.t,o.r,p.sh,o.e.n))?'<br><b class="whxw">⚠ جزء منها هيتسحب من مخزن نوع رفوف تاني (نفس المقاس)</b>':''}</span><button class="pr" data-rcxw="1">نعم، اخصمها من المخزن</button><button data-tclose="1">لا، من الطباعة</button>`);tt.classList.add('rem','rcx');tt._rx={pid:p.id,C:C.map(o=>({tid:o.t.id,rid:o.r._i,sd:o.sd,d:o.e.n}))};snd('tick')}
function rcvXw(tt){const o=tt._rx,p=DB.ph.find(x=>x.id==o.pid);tt.remove();if(!p)return;let n=0;o.C.forEach(c=>{const r=(p.rows[c.tid]||[]).find(y=>y._i==c.rid),t=tOf(p,c.tid);if(!r||!t)return;const e=(p.rcv||[]).filter(x=>x.rid==c.rid&&(x.sd||'')==(c.sd||'')&&x.src=='xr').pop(),k=whDed(p,t,r,Math.min(c.d,e?e.n:c.d),c.sd,'المتنفذ أكتر من المستلم — اتخصم من المخزن');if(!k)return;n+=k;if(e){e.n=wq(e.n-k);if(!e.n)p.rcv.splice(p.rcv.indexOf(e),1)}rcvLog(p,c.tid,r,k,c.sd,'wh',TD())});sv();render();toastT(n?'✓ اتخصم '+n+' من المخزن واتسجل مستلم من المخزن':'⚠ مفيش رصيد كفاية في المخزن')}
// the pharmacy for a number (the open one first, then the newest)
function rcvPh(no){no=String(no||'').trim();if(!no)return null;const L=DB.ph.filter(p=>String(p.no||'').trim()==no);if(!L.length)return null;const c=L.find(p=>p.id==V.p);if(c)return c;return L.slice().sort((a,b)=>((a.st=='مكتملة')-(b.st=='مكتملة'))||String(b.mo||'').localeCompare(String(a.mo||''))||b.id-a.id)[0]}
// same item = same type and the same choices (not the count, notes, old design, tahtit width, pocket counts)
const RCX=['q','nt','od','tw','pR','pL','xi','xn','mw'];
function rcSig(t,y,sh){return JSON.stringify((t.f||[]).filter(f=>!RCX.includes(f.k)&&!(f.hide&&f.hide(y,sh))).map(f=>f.k=='rsh'?(!y.rsh||y.rsh==RSAME?'':y.rsh):f.k=='fhm'?fhmOf(y):f.k=='whm'?whmOf(y):String(y[f.k]??'')))}
// received row y -> the requested rows of p (fills what is missing first, the extra stays on the last one)
function rcvPut(p,t,y,dt){const g=rcSig(t,y,p.sh),C=(p.rows[t.id]||[]).filter(c=>rcSig(t,c,p.sh)==g);if(!C.length)return 0;const m=rcvSnap(p,C);
 const dist=(key,n,need)=>{let left=n;C.forEach((c,j)=>{const tk=j==C.length-1?left:Math.min(Math.max(0,need(c)-(+c[key]||0)),left);if(tk>0){c[key]=(+c[key]||0)+tk;left-=tk}})};
 if(!(t.id=='eg'&&egAO(y,p.sh)))dist('r',qn(y),qn);
 if(t.id=='eg'&&egSub(y,p.sh))SDS.forEach(([sd])=>dist('rp'+sd,egN(y,p.sh,sd),c=>egN(c,p.sh,sd)));
 rcvDiff(p,m,'rcv',dt);p.modAt=nowIso();return 1}
function rcvWh(t,y,sh,src,note,neg){let n=0;whParts(t,y,sh).forEach(z=>{const q=wq(qn(y)*z.f);if(!q)return;whAdd({sh:z.sh,ty:z.ty,nm:z.nm,sec:z.sec,mat:z.mat,size:z.size},neg?-q:q,neg?'out':'in',src,note);n++});return n}
function rcvUndo(p,e){if(e.src=='xs'){const t=tOf(p,e.tid);if(t&&e.y)rcvWh(t,e.y,p.sh,'ph:'+p.no,'إلغاء استلام (مش مطلوب)',1)}else{const r=(p.rows[e.tid]||[]).find(y=>y._i==e.rid);if(r){const k=e.sd?'rp'+e.sd:'r';r[k]=Math.max(0,wq((+r[k]||0)-e.n))}}p.rcv.splice(p.rcv.indexOf(e),1);p.modAt=nowIso()}
// waiting items are linked as soon as their pharmacy and item exist
function rcvAuto(){if(!(V.v=='ph'||V.v=='rcv')||!(DB.rcvq||[]).length)return;const p=curP();if(!p||p._wh||p._rc||!uEditP(p))return;let n=0;RQ().slice().forEach(q=>{if(String(q.no).trim()!=String(p.no).trim())return;const t=tOf(p,q.tid);if(t&&rcvPut(p,t,q.y,q.dt)){RQ().splice(RQ().indexOf(q),1);n++}});if(n){svq();setTimeout(()=>toastT('✓ اتربط '+n+' بند مستلم كان مستني الصيدلية دي'),60)}}
// receiving with the item cards (like adding to a pharmacy)
let RCPO=null;const RCAK=()=>'rca966:'+(U().id||'');
function RCP(){if(!RCPO){let o={};try{o=JSON.parse(localStorage.getItem(RCAK())||'{}')||{}}catch(e){}RCPO={id:-8,_rc:1,no:V.rn||'',sh:+(o.sh||0),rows:(o.no==(V.rn||'')&&o.rows)||{},an:{},st:'جاري',uid:U().id}}if(V.rn!=null&&V.rn!==RCPO.no){RCPO.no=V.rn;RCPO.rows={}}const p=rcvPh(RCPO.no);if(p)RCPO.sh=p.sh;return RCPO}
const rcaN=()=>Object.values(RCP().rows).reduce((a,r)=>a+(Array.isArray(r)?r.length:0),0);
function rcaKeep(){try{if(RCPO&&rcaN())localStorage.setItem(RCAK(),JSON.stringify({no:RCPO.no,sh:RCPO.sh,rows:RCPO.rows}));else localStorage.removeItem(RCAK())}catch(e){}}
function rcaHtml(){const p=RCP(),ph=rcvPh(p.no),n=rcaN();rcaKeep();
 return `<div class="wcard"><h2>📥 استلام بالبنود · صيدلية <bdi>${esc(p.no||'—')}</bdi></h2><p class="sub">ضيف البنود اللي استلمتها زي ما بتضيفها في الصيدلية. اللي مطلوب في الصيدلية بيتحسب مستلم، و${ph?'اللي مش مطلوب بيروح المخزن تلقائي.':'الصيدلية لسه مش متسجلة: البنود هتستنى وتتربط لوحدها أول ما تضيف الصيدلية وبنودها.'}</p>${ph?`<small>${PL(ph)} · ${SH[ph.sh]}</small>`:`<label>نوع الرفوف<select id="rcash">${SH.map((x,i)=>`<option value="${i}"${p.sh==i?' selected':''}>${x}</option>`).join('')}</select></label>`}<small>تاريخ الاستلام: ${ddm(V.rd||TD())}</small></div>
 ${TY(p).filter(t=>!t.auto).map(t=>card(t,p)).join('')}
 <div class="tt what"><button class="pr big" data-rcaok="1"${n?'':' disabled'}>${ic('check')}حفظ الاستلام${n?` (${n} بند)`:''}</button><button data-rcax="1">إلغاء</button></div>`}
function rcaSave(){const R=RCP(),p=rcvPh(R.no),dt=V.rd||TD();if(p&&!uEditP(p))return toastT('👁 الصيدلية دي للعرض بس');let a=0,w=0,q=0;
 TY(R).forEach(t=>(R.rows[t.id]||[]).forEach(y=>{
  if(!p){let z='';try{z=t.z(y,R.sh)}catch(e){}RQ().push({id:rid(),no:R.no,sh:R.sh,tid:t.id,y:JSON.parse(JSON.stringify(y)),dt,at:nowIso(),z:t.n+': '+z});q++;return}
  if(rcvPut(p,t,y,dt)){a++;return}
  rcvWh(t,y,p.sh,'ph:'+p.no,'استلام مش مطلوب في صيدلية '+p.no);(p.rcv=p.rcv||[]).push({id:rid(),dt,at:nowIso(),tid:t.id,n:qn(y),src:'xs',y:JSON.parse(JSON.stringify(y)),z:rcvZ(p,t.id,y,'')});w++}));
 R.rows={};rcaKeep();RCPO=null;sv();snd('ok');goV(Object.assign({},V,{v:'rcv',op:{},dr:{},ed:null,fo:{}}));
 toastT([a?`✓ ${a} بند اتحسب مستلم`:'',w?`📦 ${w} بند مش مطلوب راح المخزن`:'',q?`⏳ ${q} بند مستني تسجيل الصيدلية`:''].filter(Boolean).join(' · ')||'مفيش بنود')}
const rcvEZ=(p,e)=>{if(e.z)return e.z;const r=(p.rows[e.tid]||[]).find(y=>y._i==e.rid);return r?rcvZ(p,e.tid,r,e.sd):'(البند اتمسح من الصيدلية)'};
function rcvLogHtml(p){const E=(p.rcv||[]).slice().sort((a,b)=>String(b.dt).localeCompare(String(a.dt))||String(b.at).localeCompare(String(a.at)));if(!E.length)return '';
 return `<h3>سجل الاستلام للصيدلية دي</h3><div class="sc"><table><tr><th>التاريخ</th><th>البند</th><th>العدد</th><th>المصدر</th><th></th></tr>${E.map(e=>`<tr><td>${e.dt?ddm(e.dt):'—'}</td><td>${esc(rcvEZ(p,e))}</td><td><b>${e.n}</b></td><td><small>${RCS[e.src]||esc(e.src)}</small></td><td>${e.src=='rcv'||e.src=='xs'?`<button class="np" data-rcdel="${e.id}" aria-label="إلغاء">✕</button>`:''}</td></tr>`).join('')}</table></div>`}
function rcvQHtml(){const Q=RQ();if(!Q.length)return '';return `<h3>⏳ مستني تسجيل الصيدلية أو البند (${Q.length})</h3><div class="sc"><table><tr><th>التاريخ</th><th>الصيدلية</th><th>البند</th><th>العدد</th><th></th></tr>${Q.map(q=>`<tr><td>${ddm(q.dt)}</td><td><b>${esc(q.no)}</b></td><td>${esc(q.z||q.tid)}</td><td><b>${qn(q.y)}</b></td><td><button class="np" data-rcqw="${q.id}">📦 للمخزن</button> <button class="np" data-rcqd="${q.id}">✕</button></td></tr>`).join('')}</table></div>`}
function rcvRep(f,t){const o=[];DB.ph.forEach(p=>(p.rcv||[]).forEach(e=>{if(e.src=='old'||!e.dt||e.dt<f||e.dt>t)return;o.push({dt:e.dt,no:p.no,nm:p.name||'',z:rcvEZ(p,e),n:e.n,s:e.src})}));RQ().forEach(q=>{if(q.dt>=f&&q.dt<=t)o.push({dt:q.dt,no:q.no,nm:'',z:q.z||q.tid,n:qn(q.y),s:'q'})});return o.sort((a,b)=>a.dt.localeCompare(b.dt)||String(a.no).localeCompare(String(b.no),undefined,{numeric:true}))}
function rcvRepBox(){const f=V.rcf||V.rd||TD(),t=V.rct||V.rd||TD(),L=rcvRep(f,t);return `<div class="wcard"><h3>📄 تقرير الاستلام</h3><div class="dts"><label>من<input type="date" id="rcf" value="${f}"></label><label>إلى<input type="date" id="rct" value="${t}"></label></div><small>${L.length?L.length+' سطر · '+new Set(L.map(x=>x.no)).size+' صيدلية':'مفيش استلام في الفترة دي'}</small>${L.length?`<div class="tt"><button class="pr" data-rcrp="pdf">${ic('sheet')}PDF</button><button data-rcrp="wa">واتساب</button></div>`:''}</div>`}
function rcvPdfEl(f,t,L){const el=document.createElement('div');el.innerHTML=`<div class="cpt"><b>تقرير الاستلام</b><small>${f==t?ddm(f):ddm(f)+' → '+ddm(t)} · ${esc(DB.cfg.dsup||'')}</small></div><table class="cpdf"><tr><th>م</th><th>التاريخ</th><th>الصيدلية</th><th>البند</th><th>العدد</th><th>ملاحظة</th></tr>${L.map((x,i)=>`<tr${x.s=='xs'||x.s=='q'?' style="background:#FFF4D1"':''}><td>${i+1}</td><td>${ddm(x.dt)}</td><td><b>${esc(x.no)}</b>${x.nm?'<br><small>'+esc(x.nm)+'</small>':''}</td><td>${esc(x.z)}</td><td><b>${x.n}</b></td><td>${x.s=='rcv'?'':RCS[x.s]||''}</td></tr>`).join('')}<tr><td colspan="4"><b>الإجمالي</b></td><td><b>${wq(L.reduce((a,x)=>a+(+x.n||0),0))}</b></td><td></td></tr></table>`;return el}
function rcvRepOut(k){const f=V.rcf||V.rd||TD(),t=V.rct||V.rd||TD(),L=rcvRep(f,t);if(!L.length)return;const nm='تقرير الاستلام - '+(f==t?f:f+' إلى '+t);
 if(k=='pdf')return sharePdf({src:rcvPdfEl(f,t,L),name:nm,title:'تقرير الاستلام'});
 const o=['📥 *تقرير الاستلام* '+(f==t?ddm(f):ddm(f)+' → '+ddm(t))];let cur=null;L.forEach(x=>{const g=x.dt+'|'+x.no;if(g!=cur){cur=g;o.push('',`🏥 صيدلية ${x.no}${x.nm?' ('+x.nm+')':''} · ${ddm(x.dt)}`)}o.push(`• ${x.z} ×${x.n}${x.s!='rcv'?' — '+RCS[x.s]:''}`)});shareText(tr(o.join('\n')))}
function rcvHtml(){const no=String(V.rn||'').trim(),p=no?rcvPh(no):null,dt=V.rd||TD(),L=no?DB.ph.filter(x=>String(x.no||'').trim()==no):[];if(p)V.p=p.id;
 let h=`<div class="wcard"><h2>📥 الاستلام</h2><p class="sub">سجّل المستلم من المطبعة برقم الصيدلية. الصيدلية نفسها بيتسجل فيها المطلوب والمتنفذ بس.</p><div class="dts"><label>رقم الصيدلية<input id="rcno" list="rcnol" inputmode="numeric" value="${esc(no)}" placeholder="اكتب الرقم"></label><label>تاريخ الاستلام<input type="date" id="rcdt" value="${dt}"></label></div><datalist id="rcnol">${[...new Set(DB.ph.map(x=>String(x.no||'').trim()).filter(Boolean))].map(x=>`<option value="${esc(x)}">`).join('')}</datalist>${L.length>1?`<div class="tt">${L.map(x=>`<button${p&&p.id==x.id?' class="pr"':''} data-rcpk="${x.id}">${esc(x.mo||'')} · ${esc(x.st||'')}</button>`).join('')}</div>`:''}</div>`;
 if(no&&!p)h+=`<div class="ywarn">الصيدلية رقم <b>${esc(no)}</b> مش متسجلة لسه. تقدر تسجل المستلم بالبنود، وهيتربط لوحده أول ما تضيف الصيدلية وبنودها.</div><div class="tt"><button class="pr big" data-rca="1">${ic('add')}استلام بالبنود</button></div>`;
 if(p)h+=`<div class="ph"><b>${PL(p)}</b><small>${esc(RL(p))} · ${SH[p.sh]}${p.name?' · '+esc(p.name):''}</small></div><div class="tt"><button class="pr big" data-rca="1">${ic('add')}استلام بالبنود (زي إضافة الصيدلية)</button></div><p class="sub">أو اكتب العدد المستلم قدام المطلوب على طول:</p>`+tkHtml(p,'r')+rcvLogHtml(p);
 if(!no)h+=`<p class="em">اكتب رقم الصيدلية علشان تسجل المستلم.</p>`;
 return h+rcvQHtml()+rcvRepBox()}
function rcvClick(d,b){
 if(d.rcxw){const tt=b.closest('.toast');if(tt&&tt._rx)rcvXw(tt);return 1}
 if(d.rcvgo){const p=DB.ph.find(x=>x.id==+d.rcvgo);if(p)goV({v:'rcv',p:p.id,rn:String(p.no||''),bp:p.id,bv:V.v,bsm:V.sm,rd:TD(),op:{},dr:{},q:V.q});return 1}
 if(d.rcvb){const id=V.bp,bv=V.bv;goV(bv=='sum'?{v:'sum',sm:V.bsm||'ck',p:id,op:{},dr:{},q:V.q}:{v:bv&&bv!='rcv'?bv:'ph',p:id,op:{},dr:{},q:V.q});return 1}
 if(d.rcpk){const p=DB.ph.find(x=>x.id==+d.rcpk);if(p){V.p=p.id;V.rn=String(p.no||'');render()}return 1}
 if(d.rca){RCPO=null;goV(Object.assign({},V,{v:'rca',op:{},dr:{},ed:null,fo:{}}));return 1}
 if(d.rcaok){rcaSave();return 1}
 if(d.rcax){if(rcaN()&&!confirm('البنود دي ما اتحفظتش في الاستلام. تلغيها؟'))return 1;RCP().rows={};rcaKeep();RCPO=null;goV(Object.assign({},V,{v:'rcv',op:{},dr:{},ed:null,fo:{}}));return 1}
 if(d.rcdel){const p=curP(),e=p&&(p.rcv||[]).find(x=>x.id==d.rcdel);if(!e)return 1;if(!confirm(e.src=='xs'?'تلغي الاستلام ده؟ هيتشال من المخزن تاني.':'تلغي الاستلام ده ('+e.n+')؟ المستلم في الصيدلية هيقل.'))return 1;rcvUndo(p,e);sv();render();return 1}
 if(d.rcqw){const i=RQ().findIndex(x=>x.id==d.rcqw);if(i<0)return 1;const q=RQ()[i],t=T.find(x=>x.id==q.tid);if(!confirm('تحوّل البند ده للمخزن؟'))return 1;if(t)rcvWh(t,q.y,q.sh,'ph:'+q.no,'استلام لصيدلية '+q.no+' (مش مطلوب)');RQ().splice(i,1);sv();render();toastT('✓ اتحوّل للمخزن');return 1}
 if(d.rcqd){const i=RQ().findIndex(x=>x.id==d.rcqd);if(i>=0&&confirm('تمسح البند ده من الاستلام المستني؟')){RQ().splice(i,1);sv();render()}return 1}
 if(d.rcrp){rcvRepOut(d.rcrp);return 1}
 return 0}
function rcvChange(x){
 if(x.id=='rcno'){V.rn=x.value.trim();const p=rcvPh(V.rn);V.p=p?p.id:null;render();return 1}
 if(x.id=='rcdt'){V.rd=x.value||TD();render();return 1}
 if(x.id=='rcf'||x.id=='rct'){V[x.id]=x.value;render();return 1}
 if(x.id=='rcash'){RCP().sh=+x.value;V.dr={};rcaKeep();render();return 1}
 return 0}

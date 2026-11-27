// ---------- 3.2 (file n3.2.js) ----------
// 1) 🧰 spare (احتياطي): pieces taken from stock on top of the order (r.wz); taken off stock now, counted in the surplus,
//    so what is not installed goes back with «يرجع للمخزن»; a spare that broke = هالك on the row
// 2) 📦 «اسحب المتاح» per type inside a pharmacy (stock shared between rows like the print summary)
// 3) «اطبع الناقص بس»: warning when earlier pharmacies of the month need the same stock
// 4) End gandola Baby (Big) side = the Baby (Small) side print when both sides have the same size (Regular / New Turkish)
// 5) Floor Header «كبير» per shelf type (core fhL; New Turkish 14×76 for now)
// 6) the same surplus is never added twice (log check before «ترحيل للمخزن»)
// 7) stock-take sheet: ⚠ a Wall / Floor Header name that belongs to another section
// 8) a) minimum 3 for items taken often  b) 🗓 last stock-take date per item  c) 📊 monthly warehouse movement (PDF / Excel)
const C32=()=>DB.cfg.c32=DB.cfg.c32||{};
// users.js (permissions) loads after the updates: add the new actions once everything is defined
setTimeout(()=>{try{PHEDIT.push('sp32','spb32','tp32');STEDIT.push('wm32','wm32p','wm32x')}catch(e){console.warn(e)}},0);
// ---- 5) settings: an old single «كبير» override becomes the per-shelf list
function szFix32(){const o=DB.cfg.sz=DB.cfg.sz||{};if(o['fh.l']!=null&&o['fh.ln']==null){o['fh.ln']=SZD['fh.ln'].map((v,i)=>i==1?v:o['fh.l']);delete o['fh.l'];sv()}}
// ---- 4) Baby (Big) side → Baby (Small) side
const egBB32=(y,sh)=>/Side/.test(y.ty)&&/^Baby \(Big\)/.test(String(y.nm||''))&&String(SZ('eg.ss')[sh]).replace(/\s+/g,'')==String(SZ('eg.sl')[sh]).replace(/\s+/g,'');
const _whParts32=whParts;whParts=function(t,r,s){const L=_whParts32.apply(this,arguments);if(t&&t.id=='eg')L.forEach(y=>{if(egBB32(y,y.sh))y.nm=String(y.nm).replace(/^Baby \(Big\)/,'Baby (Small)')});return L};
function egFix32(){let n=0;const W=WU();W.slice().forEach(x=>{if(!egBB32(x,x.sh))return;const nm=String(x.nm).replace(/^Baby \(Big\)/,'Baby (Small)'),k=whKey(Object.assign({},x,{nm})),y=W.find(z=>z!==x&&whKey(z)==k);if(y){y.qty=wq(+y.qty+(+x.qty||0));y.at=nowIso();W.splice(W.indexOf(x),1)}else x.nm=nm;n++});
 DB.ph.forEach(p=>{const T0=p.whT;if(!T0)return;Object.keys(T0).forEach(k=>{const v=T0[k];if(!v||!egBB32(v,v.sh))return;const nv=Object.assign({},v,{nm:String(v.nm).replace(/^Baby \(Big\)/,'Baby (Small)')}),nk2=whKey(nv);delete T0[k];if(T0[nk2])T0[nk2].q=wq((+T0[nk2].q||0)+(+v.q||0));else T0[nk2]=nv;n++})});if(n)sv()}
// ---- 1) spare
const spN=r=>Math.max(0,Math.round(+(r&&r.wz)||0));
function spAv(p,t,r){const P=whParts(t,r,p.sh).filter(y=>!y.pk&&y.f>0);return P.length?Math.min(...P.map(y=>Math.floor((whQty(y)+1e-9)/y.f))):0}
function spTake(p,t,r,n){n=Math.min(n,spAv(p,t,r));if(!(n>0))return 0;whParts(t,r,p.sh).filter(y=>!y.pk&&y.f>0).forEach(y=>whTakeQ(y,n*y.f,'ph:'+p.no,'احتياطي زيادة (بيرجع لو ما اتركبش)'));r.wz=spN(r)+n;p.modAt=nowIso();return n}
function spBack(p,t,r){const n=spN(r);if(!n)return 0;whParts(t,r,p.sh).filter(y=>!y.pk&&y.f>0).forEach(y=>whAdd(y,n*y.f,'in','ph:'+p.no,'احتياطي رجع للمخزن'));r.wz=0;p.modAt=nowIso();return n}
// surplus: received + spare − executed − damaged (the spare is never in the management report or the shortages)
const _whSurplus32=whSurplus;whSurplus=function(p){const m=_whSurplus32.apply(this,arguments);if(isHold(p))return m;ckRows(p).forEach(x=>{const r=x.r,w=spN(r);if(!w||(r.sw&&r.cx))return;
 const a=Math.max(0,(+r.r||0)-(+r.x||0)-hkN(r)),b=Math.max(0,(+r.r||0)+w-(+r.x||0)-hkN(r)),dd=b-a;if(dd<=0)return;whParts(x.t,r,p.sh).filter(y=>!y.pk&&y.f>0).forEach(y=>{const k=whKey(y);if(!m[k])m[k]=Object.assign({},y,{q:0,why:[]});m[k].q=wq(m[k].q+dd*y.f);m[k].why=m[k].why||[];if(!m[k].why.includes('احتياطي'))m[k].why.push('احتياطي')})});return m};
const spTag=r=>spN(r)?`<small class="rshc spt">🧰 احتياطي ${spN(r)}</small>`:'';
function spBlock(tt,p,t,r,i){const av=spAv(p,t,r),w=spN(r);tt.insertAdjacentHTML('beforeend',`<div class="sp32"><small>🧰 <b>احتياطي زيادة</b> عن المطلوب: بيتخصم من المخزن دلوقتي، واللي ما يتركبش بيرجع مع «يرجع للمخزن». لو اتلف، علّمه هالك.${w?` معاك دلوقتي <b>${w}</b>.`:''}</small>
 <div class="spr">${av>0?`<input type="number" inputmode="numeric" min="1" max="${av}" value="1" class="spn"><button class="pr" data-sp32="${t.id}:${i}">خد احتياطي (المتاح ${av})</button>`:'<small>مفيش رصيد للاحتياطي.</small>'}${w?`<button data-spb32="${t.id}:${i}">↩ رجّع الـ ${w}</button>`:''}</div></div>`)}
const _whFrom32=whFrom;whFrom=function(p,t,r,i){if(!p||!t||!r)return _whFrom32.apply(this,arguments);const O=whFromOpts(p,t,r),av=spAv(p,t,r);if(!O.length&&!(av>0)&&!spN(r))return _whFrom32.apply(this,arguments);
 let tt=null;if(O.length){_whFrom32.apply(this,arguments);tt=[...document.querySelectorAll('.toast.rem')].reverse().find(e=>e._wf&&e._wf.pid==p.id&&e._wf.tid==t.id&&e._wf.i==i)}
 if(!tt){tt=toast(`<span>📦 ${esc(t.n)}${r.nm?' · '+esc(r.nm):''}: المطلوب اتاخد كله.</span><button data-tclose="1">إغلاق</button>`);tt.classList.add('rem')}spBlock(tt,p,t,r,i)};
// ---- 2) pull what the stock has for one type
function tpUsed(p,tid){if(!p||uStoreRO()||!WU().length)return [];let N;try{N=whNet(p)}catch(e){return []}return N.used.filter(u=>u.tid==tid&&!((p.rows[tid]||[])[u.i]||{}).cx)}
function tpGo(tid){const p=curP(),t=T.find(x=>x.id==tid);if(!p||!t)return;const U=tpUsed(p,tid),n=U.reduce((a,u)=>a+(+u.n||0)+(+u.np||0),0);if(!n)return toastT('مفيش حاجة في المخزن لـ '+t.n);
 if(!confirm(`📦 هيتسحب من المخزن ${n} لـ ${t.n} في صيدلية ${p.no} ويتحسبوا مستلمين:\n${U.map(u=>'• '+u.z+' — '+u.tx).join('\n')}\n\nفيه نقطة استرجاع قبلها. تكمل؟`))return;
 snap('قبل سحب '+t.n+' — صيدلية '+p.no);let m=0;U.forEach(u=>{const r=(p.rows[tid]||[])[u.i];if(!r)return;const L=whRowPlan(t,r,p.sh);if(L)m+=whTake(p,t,r,L,'سحب '+t.n+' للصيدلية')});p.modAt=nowIso();sv();snd('ok');render();
 undoT('✓ اتسحب '+m+' من المخزن لـ '+t.n,()=>{const x=snaps()[0];if(x&&/^قبل سحب /.test(x.why)){DB=JSON.parse(x.db);norm();sv();render()}})}
// ---- 3) stock that earlier pharmacies of the month need
function avlEarlier(p){const st={};WU().forEach(x=>{const k=x.id+'|'+whKey0(x);st[k]=(st[k]||0)+(+x.qty||0)});const take=(y,n)=>{const k0=whKey0(y);let left=n;Object.keys(st).forEach(k=>{if(left<=1e-9||k.split('|').slice(1).join('|')!=k0)return;const u=Math.min(left,st[k]);st[k]-=u;left-=u})};
 const need=(q,dry)=>{let h=0;const K=new Set();prepRows(q).forEach(x=>{const r=x.r,nd=r.cx?0:Math.max(0,qn(r)-(+r.r||0));if(!nd)return;(whParts(x.t,r,q.sh)||[]).filter(y=>!y.pk&&y.f>0).forEach(y=>{const hv=Math.min(nd,Math.floor((whStQ(st,y)+1e-9)/y.f));if(hv){K.add(whKey0(y));if(!dry)take(y,hv*y.f);h+=hv}})});return {h,K}};
 const a=need(p,1),P=DB.ph.filter(q=>q.mo==p.mo&&q.st!='مكتملة'&&!isHold(q)).sort(pSort),ix=P.indexOf(p);if(ix<=0||!a.h)return null;const who=[];
 P.slice(0,ix).forEach(q=>{const before=JSON.stringify(st),r=need(q,0);if(JSON.stringify(st)!=before&&[...r.K].some(k=>a.K.has(k)))who.push(q.no)});const b=need(p,1);return b.h<a.h?{lost:a.h-b.h,who}:null}
const _sxBox32=sxBox;sxBox=function(p,N){let h=_sxBox32.apply(this,arguments);if(!h||!V.sxw)return h;try{const e=avlEarlier(p);if(e)h=h.replace(/<\/div>$/,`<div class="alr sxe32"><small>⚠ ${e.lost} من الموجود في المخزن محسوبين لصيدليات قبلها في الشهر (${e.who.map(esc).join('، ')||'—'}). لو سحبتهم هنا، هينقصوا عليهم. «الموجود والناقص» في تبويب الشهر بيوزّع المخزن على الصيدليات بالترتيب.</small></div></div>`)}catch(er){console.warn(er)}return h};
// ---- 6) the same surplus twice
function whDup32(p,L){const t0=p.mo?p.mo+'-01':'',T0=p.whT||{},W=WU(),ok=e=>e.src=='ph:'+p.no&&/^(فائض صيدلية|تعديل صيدلية بعد الترحيل)/.test(e.note||'')&&(e.pid!=null?String(e.pid)==String(p.id):String(e.at||'').slice(0,10)>=t0);
 const same=(x,y)=>x.sh==y.sh&&x.ty==y.ty&&nk(x.nm)==nk(y.nm)&&nk(x.sec)==nk(y.sec)&&String(x.size||'').replace(/\s+/g,'')==String(y.size||'').replace(/\s+/g,'');
 return L.filter(x=>x.dl>0).map(x=>{const ids=new Set(W.filter(y=>same(x,y)).map(y=>String(y.id))),net=wq((DB.wlog||[]).reduce((a,e)=>a+(ids.has(String(e.id))&&ok(e)?(+e.qty||0):0),0)),was=+(T0[x.k]||{}).q||0,done=Math.min(x.dl,wq(net-was));return done>0?Object.assign({},x,{done}):null}).filter(Boolean)}
const _whApply32=whApply;whApply=function(){const p=curP();if(!p)return _whApply32.apply(this,arguments);const S=W29().off,L=whPlan(p).filter(x=>!S[x.k]),D=whDup32(p,L),wa=whAdd;let skip=[];
 if(D.length){const last=(DB.wlog||[]).find(e=>e.src=='ph:'+p.no&&/^فائض صيدلية/.test(e.note||''));if(!confirm(`⚠ ${D.length} سطر من الترحيل ده متسجلين في سجل المخزن قبل كده${last?' (آخر ترحيل '+fd(last.at)+')':''}:\n${D.map(x=>'• '+x.ty+(x.nm?' · '+x.nm:'')+' '+(x.size||'')+' — '+x.done).join('\n')}\n\nغالباً الصيدلية رجعت لنسخة قديمة بعد مزامنة، فالترحيل باين كأنه ما اتعملش.\nموافق = ما يتضافوش تاني (يتعلّموا إنهم اترحّلوا)، والباقي يترحّل عادي.\nإلغاء = رجوع.`))return;skip=D.map(x=>({sh:x.sh,ty:x.ty,nm:x.nm,sec:x.sec,size:x.size,n:x.done}))}
 whAdd=function(o,q,typ,src,note){const s=skip.find(z=>z.n>0&&q>0&&z.sh==o.sh&&z.ty==o.ty&&nk(z.nm)==nk(o.nm)&&nk(z.sec)==nk(o.sec)&&String(z.size)==String(o.size));if(s){const u=Math.min(s.n,q);s.n=wq(s.n-u);q=wq(q-u);if(!q)return whFind(whKey(o))||o}const x=wa.call(this,o,q,typ,src,note);if(src=='ph:'+p.no&&DB.wlog[0])DB.wlog[0].pid=p.id;return x};
 try{return _whApply32.apply(this,arguments)}finally{whAdd=wa}};
// ---- 7) stock-take: name from another section
const secOf32=nm=>Object.keys(NM).filter(s=>(NM[s]||[]).some(n=>String(n).toLowerCase()==String(nm||'').toLowerCase()));
const _jrdOpen32=jrdOpen;jrdOpen=function(q,fn){const r=_jrdOpen32.apply(this,arguments);try{const L=(JRD31&&JRD31.L)||[],R=[...document.querySelectorAll('.csh .ctab tr')].slice(1);let n=0;
 L.forEach((z,i)=>{if(!['Wall Header','Floor Header'].includes(z.ty)||!z.sec||!NM[z.sec]||!z.nm)return;const S=secOf32(z.nm);if(!S.length||S.includes(z.sec))return;n++;const c=R[i]&&R[i].cells[0];if(c)c.insertAdjacentHTML('beforeend',`<small class="c-exp">⚠ الاسم ده من قسم ${esc(S.join(' / '))}</small>`)});
 if(n){const b=document.querySelector('.csh .cshb small');if(b)b.insertAdjacentHTML('afterend',`<div class="alr"><small>⚠ ${n} اسم متسجل تحت قسم غير قسمه في البرنامج. لو مطبوع فعلاً بلون القسم ده سيبه، ولو الذكاء الاصطناعي غلط صلّح الملف قبل «اعتمد الجرد».</small></div>`)}}catch(e){console.warn(e)}return r};
// ---- 8b) last stock-take date
const _jrdGo32=jrdGo;jrdGo=function(){const L=(JRD31&&JRD31.L||[]).slice(),r=_jrdGo32.apply(this,arguments);try{const t=nowIso();L.forEach(z=>jrdFind(z).forEach(x=>x.jd=t));if(L.length){sv();render()}}catch(e){console.warn(e)}return r};
function jdFix32(){const W=WU(),m={};(DB.wlog||[]).forEach(e=>{if(e.src=='jard'&&(!m[e.id]||e.at>m[e.id]))m[e.id]=e.at});W.forEach(x=>{if(!x.jd&&m[x.id])x.jd=m[x.id]})}
const _whCard32=whCard;whCard=function(x){const h=_whCard32.apply(this,arguments);return x&&x.jd?h.replace('<small class="mu">','<small class="mu">🗓 آخر جرد '+esc(fd(x.jd).slice(0,10))+' · '):h};
// ---- 8a) minimum 3 for items taken often (only where no minimum was set)
function minFix32(){const c={},t0=new Date(Date.now()-90*864e5).toISOString();(DB.wlog||[]).forEach(e=>{if(e.typ=='out'&&/^ph:/.test(e.src||'')&&e.at>=t0)c[e.id]=(c[e.id]||0)+1});let n=0;WU().forEach(x=>{if(x.unit=='متر'||x.ty=='أخرى'||(x.min!==''&&x.min!=null)||(c[x.id]||0)<2)return;x.min=3;n++});C32().minN=n}
// ---- 8c) monthly movement
const WMC=[['in','داخل (طباعة / إضافة)'],['ret','راجع من صيدليات'],['out','طالع للصيدليات'],['dmg','هالك / استهلاك'],['adj','جرد / تعديل']];
function wmCat(e){const s=String(e.src||''),q=+e.qty||0;if(/^ph:/.test(s))return q<0?'out':'ret';if(/^mnt:/.test(s))return 'out';if(s=='dmg'||s=='use')return 'dmg';if(s=='jard'||s=='conv'||e.typ=='adj')return 'adj';return q>0?'in':'adj'}
function wmData(mo){const W=WU(),by={};W.forEach(x=>by[x.id]=x);const R={};(DB.wlog||[]).forEach(e=>{const m=String(e.at||'').slice(0,7),x=by[e.id];if(!x||m<mo)return;const o=R[e.id]=R[e.id]||{x,after:0,c:{}};if(m>mo){o.after=wq(o.after+(+e.qty||0));return}const k=wmCat(e);o.c[k]=wq((o.c[k]||0)+(+e.qty||0))});
 return Object.values(R).filter(o=>Object.keys(o.c).length).map(o=>{const end=wq((+o.x.qty||0)-o.after),sum=Object.values(o.c).reduce((a,v)=>a+v,0);return Object.assign(o,{end,start:wq(end-sum)})}).sort((a,b)=>a.x.sh-b.x.sh||a.x.ty.localeCompare(b.x.ty)||String(a.x.nm).localeCompare(String(b.x.nm)))}
function wmEl(mo){const D=wmData(mo),tot={},f=v=>v?(v>0?'+':'')+wq(v):'';WMC.forEach(([k])=>tot[k]=wq(D.reduce((a,o)=>a+(o.x.unit=='متر'?0:(o.c[k]||0)),0)));const el=document.createElement('div');
 el.innerHTML=`<div class="cpt"><b>حركة المخزن — شهر ${mo.split('-').reverse().join('-')}</b><small>${TD().split('-').reverse().join('-')} · ${esc(DB.cfg.dsup||'')}</small></div><table class="cpdf"><tr><th>م</th><th>الصنف</th><th>المقاس</th><th>الرفوف</th><th>أول الشهر</th>${WMC.map(([,l])=>`<th>${l}</th>`).join('')}<th>آخر الشهر</th></tr>${D.map((o,i)=>`<tr><td>${i+1}</td><td>${esc(o.x.ty)}${o.x.nm||o.x.sec?' · '+esc(whNm(o.x)):''}</td><td>${esc(o.x.size||'')}</td><td>${SH[o.x.sh]||''}</td><td>${wq(o.start)}</td>${WMC.map(([k])=>`<td>${f(o.c[k])}</td>`).join('')}<td><b>${wq(o.end)} ${esc(o.x.unit)}</b></td></tr>`).join('')}<tr class="tot"><td colspan="5">الإجمالي (قطع)</td>${WMC.map(([k])=>`<td>${f(tot[k])}</td>`).join('')}<td></td></tr></table>`;return {el,n:D.length}}
let WM32=null;
function wmOpen(mo){const ms=[...new Set((DB.wlog||[]).map(e=>String(e.at||'').slice(0,7)).filter(Boolean))].sort().reverse();mo=mo||ms[0]||MN();WM32=mo;const E=wmEl(mo);cShClose();const el=document.createElement('div');el.className='csh';
 el.innerHTML=`<div class="cshb"><b>📊 حركة المخزن للشهر</b><label>الشهر<select id="wm32m">${(ms.includes(mo)?ms:[mo].concat(ms)).map(m=>`<option${m==mo?' selected':''}>${m}</option>`).join('')}</select></label><small>${E.n} صنف اتحرك · من سجل الحركات (آخر 3000 حركة). أول الشهر وآخره محسوبين من الرصيد الحالي بالرجوع للخلف.</small><div class="sc wm32">${E.n?E.el.innerHTML:'<p class="em">مفيش حركات في الشهر ده.</p>'}</div><div class="cshr"><button class="pr" data-wm32p="1">${ic('share')}PDF</button><button data-wm32x="1">${ic('sheet')}Excel</button><button data-cshx="1">إغلاق</button></div></div>`;document.body.appendChild(el)}
async function wmExp(k){const mo=WM32||MN(),n='حركة المخزن - '+mo;if(k=='p')return sharePdf({src:wmEl(mo).el,name:n,title:'حركة المخزن'});const bl=rpXlsx(wmEl(mo).el);if(CAPN())return nativeSave(n+'.xlsx',bl,bl.type,true);return shr(n+'.xlsx',bl,bl.type)}
const _whHtml32=whHtml;whHtml=function(){return _whHtml32.apply(this,arguments).replace('<button data-whlog="1">',`<button data-wm32="1">📊 حركة الشهر</button><button data-whlog="1">`)};
// ---- rendering: spare tag, the stock button when only a spare is possible, per-type pull
// the 3.2 data steps run once, after the 3.1 ones (layout rolls) had their render
let M32=0;const _render032=render0;render0=function(){const out=_render032.apply(this,arguments);if(!M32&&DB&&DB.cfg&&!C32().m){M32=1;try{szFix32();egFix32();jdFix32();minFix32();C32().m=1;sv()}catch(e){console.warn('m32',e)}setTimeout(()=>render(),0);return out}
 try{if(V.v=='ph'){const p=curP();if(p){document.querySelectorAll('details[data-id]').forEach(d=>{const tid=d.dataset.id,t=T.find(x=>x.id==tid),rs=p.rows[tid]||[];if(!t)return;
  d.querySelectorAll('.rw').forEach((w,i)=>{const r=rs[i];if(!r)return;const sp=w.querySelector('span');if(sp&&spN(r)&&!sp.querySelector('.spt'))sp.insertAdjacentHTML('beforeend',spTag(r));const bt=w.querySelector('.bt');
   if(bt&&!bt.querySelector('[data-whfrom]')&&!uStoreRO()&&uEditP(p)&&(spN(r)||(!r.cx&&qn(r)>0&&(+r.r||0)>=qn(r)&&spAv(p,t,r)>0)))bt.insertAdjacentHTML('afterbegin',`<button data-whfrom="${tid}:${i}">📦 من المخزن</button>`)});
  if(!d.querySelector('.tp32')&&!uStoreRO()&&uEditP(p)&&rs.length>1){const U=tpUsed(p,tid),n=U.reduce((a,u)=>a+(+u.n||0)+(+u.np||0),0);if(n){const a=d.querySelector('.addrow,.fm,.addb');const h=`<div class="tp32"><button data-tp32="${tid}">📦 اسحب المتاح لـ ${esc(t.n)} (${n})</button></div>`;if(a)a.insertAdjacentHTML('beforebegin',h);else d.insertAdjacentHTML('beforeend',h)}}})}}}catch(e){console.warn(e)}return out};
const _v24Click32=v24Click;v24Click=function(d,b){
 if(d.sp32||d.spb32){const p=curP(),[tid,i]=String(d.sp32||d.spb32).split(':'),t=T.find(x=>x.id==tid),r=p&&(p.rows[tid]||[])[+i];const tt=b.closest&&b.closest('.toast');if(!r||!t)return 1;
  if(d.sp32){const v=Math.round(+((tt&&tt.querySelector('.spn')||{}).value)||1),n=spTake(p,t,r,Math.max(1,v));sv();if(tt)tt.remove();render();toastT(n?`✓ اتخصم ${n} احتياطي من المخزن. اللي ما يتركبش بيرجع مع «يرجع للمخزن»`:'⚠ مفيش رصيد كفاية')}
  else{const n=spBack(p,t,r);sv();if(tt)tt.remove();render();toastT('✓ رجع '+n+' احتياطي للمخزن')}return 1}
 if(d.tp32){tpGo(d.tp32);return 1}
 if(d.wm32){wmOpen();return 1}if(d.wm32p){wmExp('p');return 1}if(d.wm32x){wmExp('x');return 1}
 return _v24Click32(d,b)};
const _v33Change32=v33Change;v33Change=function(x){if(x.id=='wm32m'){wmOpen(x.value);return 1}return _v33Change32(x)};

// ---------- 2.4 (file n2.4.js) ----------
// 1) Acrylic board A4 (A3 names) + «Wasfaty board» 48×80 — core: 03-sizes.js, 05-ad-types.js, v3.8.js mgMerge
// 2) Acrylic boards work: تركيب فقط / تصنيع وتركيب / ستيكر فقط. Default by pharmacy type; Decorative nail always made + installed.
//    «تركيب فقط» = the pharmacy already has the piece: no warehouse pull, no surplus, not in print shortages / preparation.
// 3) «وصفاتي» custom ad type → Acrylic boards «Wasfaty board» (rows + warehouse), with a restore point
// 4) rows wrap on the phone (CSS in app.css): long notes never widen the page
// 5) هالك (damaged): row field hk — not moved to the warehouse; damaged stock item from the warehouse
// 6) 🔁 swap by the customer: original counted in the management report (cx), each part back to the warehouse or damaged; new row opened
// 7) screw caps: stock shown next to the caps table and a warning when the stock is short
const ABST=['تركيب فقط','تصنيع وتركيب','ستيكر فقط'],ABMK='تصنيع وتركيب',ABIO='تركيب فقط';
function abSttO(r){const p=typeof curP=='function'?curP():null,it=r&&r.it;const first=it=='Decorative nail'||it=='No smoking acrylic'?ABMK:(p&&p.mod=='تعديل براندنج'?ABIO:ABMK);return [first].concat(ABST.filter(x=>x!=first))}
const abIO=(t,r)=>!!(t&&t.id=='ab'&&r&&r.stt==ABIO);
const _whParts24=whParts;whParts=function(t,r,s){if(abIO(t,r))return [];return _whParts24(t,r,s)};
const _nqLines24=nqLines;nqLines=function(p,k){return _nqLines24(p,k).filter(x=>!abIO(x.t,x.r))};
const _prepRows24=prepRows;prepRows=function(p){return _prepRows24(p).filter(x=>!abIO(x.t,x.r))};
// ---- 5) damaged
const HKF=Object.assign(num('hk','🗑 هالك (تالف) — اختياري'),{opt:1,z0:1});
(function(){T.forEach(t=>{if(t.auto||!t.f||!t.f.some(f=>f.k=='q')||t.f.some(f=>f.k=='hk'))return;t.f.push(HKF)});if(!RCX.includes('hk'))RCX.push('hk')})();
const hkN=r=>Math.max(0,Math.round(+(r&&r.hk)||0));
// surplus = received − executed − damaged; a swapped row: received − damaged parts (it is counted as done in the report)
whSurplus=function(p){const m={};ckRows(p).forEach(x=>{const r=x.r,sw=r.sw&&r.cx,d=sw?0:Math.max(0,(+r.r||0)-(+r.x||0)-hkN(r));whParts(x.t,r,p.sh).forEach(y=>{let dd;
  if(sw){const k0=whKey(y),hp=+((r.sw.hk||{})[k0])||0;dd=y.pk?Math.max(0,pkv(r,'r',y.pk)-hp):Math.max(0,(+r.r||0)*y.f+(y.ep?egX(r,y.ep):0)-hp)}
  else dd=y.pk?Math.max(0,pkv(r,'r',y.pk)-pkv(r,'x',y.pk)):d*y.f+(y.ep?egX(r,y.ep):0);
  if(!dd)return;const k=whKey(y);if(!m[k])m[k]=Object.assign({},y,{q:0});m[k].q=wq(m[k].q+dd)})});return m};
const hkTag=r=>hkN(r)?`<small class="rshc hkt">🗑 هالك ${hkN(r)}</small>`:'';
const swTag=r=>r.sw&&r.cx?`<small class="rshc swt">🔁 اتبدّل بطلب العميل${r.sw.to?' ← '+esc(r.sw.to):''}</small>`:r.swf?`<small class="rshc swt">🔁 بدل: ${esc(r.swf)}</small>`:'';
// ---- 6) swap by the customer
const isStk=y=>/ستيكر|sticker/i.test((y.mat||'')+' '+(y.ty||''))&&!/أكريليك|اكريليك|باك لايت|backlit/i.test(y.mat||'');
let SWP=null;
function swOpen(tid,i){const p=curP(),t=T.find(x=>x.id==tid),r=p&&(p.rows[tid]||[])[+i];if(!r)return;const P=(whParts(t,r,p.sh)||[]).filter(y=>y.f>0),q=qn(r);
 SWP={pid:p.id,tid,i:+i,P:P.map(y=>({y,k:whKey(y),n:wq(q*y.f),st:isStk(y),v:isStk(y)?'':'wh'}))};swDraw()}
function swDraw(){cShClose();const p=DB.ph.find(x=>x.id==SWP.pid),t=T.find(x=>x.id==SWP.tid),r=p.rows[SWP.tid][SWP.i],el=document.createElement('div');el.className='csh';
 el.innerHTML=`<div class="cshb"><b>🔁 تبديل بطلب العميل</b><small>${esc(t.n)} · ${esc(t.z(r,p.sh))}. البند ده هيتحسب في تقرير الإدارة، وتقدر تضيف البند الجديد بعده. لكل جزء: يرجع المخزن ولا هالك؟</small>
 <div class="cnpl">${SWP.P.length?SWP.P.map((o,j)=>`<div class="swp"><b>${esc(o.y.ty)}${o.y.nm?' · '+esc(whNm(o.y)):''}</b><small>${esc(o.y.size||'—')} · ${esc(o.y.mat||'—')} · ${o.n} ${whUnit(o.y.ty)}</small>${o.st?'<small class="hint">ستيكر: اتركب؟ لو اتركب واتشال يبقى هالك.</small>':''}
  <div class="tt"><button class="${o.v=='wh'?'pr':''}" data-swv="${j}:wh">${o.st?'ما اتركبش — ':''}📦 يرجع المخزن</button><button class="${o.v=='hk'?'pr':''}" data-swv="${j}:hk">${o.st?'اتركب — ':''}🗑 هالك</button></div></div>`).join(''):'<p class="em">البند ده مالوش أجزاء في المخزن.</p>'}</div>
 <div class="cshr"><button class="pr" data-swgo="1">تأكيد التبديل وإضافة البند الجديد</button><button data-swx="1">إلغاء</button></div></div>`;document.body.appendChild(el)}
function swGo(){const miss=SWP.P.filter(o=>!o.v);if(miss.length)return alert('اختار لكل جزء ستيكر: اتركب (هالك) ولا ما اتركبش (يرجع المخزن)');
 const p=DB.ph.find(x=>x.id==SWP.pid),t=T.find(x=>x.id==SWP.tid),r=p.rows[SWP.tid][SWP.i];if(!r)return;snapLater('قبل تبديل بطلب العميل — صيدلية '+p.no,JSON.stringify(DB));
 const hk={};SWP.P.forEach(o=>{if(o.v=='hk')hk[o.k]=(hk[o.k]||0)+o.n});r.cx=1;r.sw={at:nowIso(),hk};const lab=t.z(r,p.sh);
 const nr=JSON.parse(JSON.stringify(r));['r','x','wf','wfpR','wfpL','wxs','wxh','rpR','rpL','cx','sw','hk','ck','rcv','swf','an_','_i'].forEach(k=>delete nr[k]);nr.swf=lab;
 cShClose();SWP=null;sv();V.dr[t.id]=nr;V.ed=null;V.op[t.id]=true;V.fo=V.fo||{};V.fo[t.id]=true;V.swFrom={tid:t.id,i:p.rows[t.id].indexOf(r)};render();toastT('✓ البند الأصلي اتعلّم «اتبدّل بطلب العميل». غيّر المسمى واحفظ البند الجديد');
 setTimeout(()=>{const f=document.querySelector('.fm [data-k="nm"],.fm select');if(f&&f.scrollIntoView)f.scrollIntoView({block:'center'})},80)}
function swUndo(tid,i){const p=curP(),r=p&&(p.rows[tid]||[])[+i];if(!r||!r.sw)return;if(!confirm('إلغاء «تبديل بطلب العميل» للبند ده؟ (البند الجديد مش هيتمسح)'))return;delete r.sw;delete r.cx;sv();render()}
// remember the link once the new row is saved (the form keeps only its fields)
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-add]');if(!b||!V.swFrom||b.dataset.add!=V.swFrom.tid)return;const s=V.swFrom,p=curP();if(!p)return;const before=new Set(p.rows[s.tid]||[]),o=(p.rows[s.tid]||[])[s.i],lab=V.dr[s.tid]&&V.dr[s.tid].swf;
 setTimeout(()=>{const L=p.rows[s.tid]||[],n=L.find(x=>!before.has(x));if(!n)return;n.swf=lab||'';if(o&&o.sw)o.sw.to=T.find(x=>x.id==s.tid).z(n,p.sh);V.swFrom=null;sv();render()},0)},true);
// swap button in the pharmacy rows
const _render0_24=render0;render0=function(){const r=_render0_24.apply(this,arguments);try{if(V.v=='ph'&&!uStoreRO()){const p=curP();if(p)document.querySelectorAll('.rw .bt button[data-ed]').forEach(b=>{const[tid,i]=b.dataset.ed.split(':'),r=(p.rows[tid]||[])[+i];if(!r||b.parentElement.querySelector('[data-swo],[data-swu]'))return;const sp=b.closest('.rw').querySelector('span');if(sp&&!sp.querySelector('.hkt,.swt'))sp.insertAdjacentHTML('beforeend',hkTag(r)+swTag(r));if(!isBr(p))return;b.insertAdjacentHTML('beforebegin',r.sw&&r.cx?`<button data-swu="${tid}:${i}">↺ إلغاء التبديل</button>`:`<button data-swo="${tid}:${i}" title="تبديل بطلب العميل">🔁 تبديل</button>`)})}
 if(V.v=='wh'&&!uStoreRO())document.querySelectorAll('[data-whed]').forEach(b=>{if(b.parentElement.querySelector('[data-whhk]'))return;b.insertAdjacentHTML('afterend',`<button data-whhk="${b.dataset.whed}">🗑 هالك</button>`)})}catch(e){console.warn(e)}return r};
// ---- 7) screw caps: stock and warning
const capStock=()=>wq(WU().filter(x=>x.ty==CPNM).reduce((a,x)=>a+(+x.qty||0),0));
const capNeed=p=>Math.max(0,capN(p,'q')-capN(p,'x'));
const _capHtml24=capHtml;capHtml=function(p){const h=_capHtml24(p);if(!h)return h;const nd=capNeed(p),st=capStock();return h+`<div class="${nd>st?'alr':'ph'}"><small>${CPNM} في المخزن: <b>${st}</b> · فاضل يتركب هنا: <b>${nd}</b>${nd>st?` · ⚠ ناقص <b>${wq(nd-st)}</b> — وفّرها`:''}</small></div>`};
document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('[data-whfrom]');if(!b)return;const tid=b.dataset.whfrom.split(':')[0];if(!CAPS.some(c=>c[0]==tid))return;setTimeout(()=>{const p=curP();if(!p)return;const nd=capNeed(p),st=capStock();if(nd>st)alert(`⚠ ${CPNM}: الصيدلية دي محتاجة ${nd}، وفي المخزن ${st} بس.\nناقص ${wq(nd-st)} — وفّرها قبل التركيب.`)},400)},true);
// ---- clicks
const _v24Click24=v24Click;v24Click=function(d,b){
 if(d.swo){const[t,i]=d.swo.split(':');swOpen(t,i);return 1}if(d.swu){const[t,i]=d.swu.split(':');swUndo(t,i);return 1}
 if(d.swv&&SWP){const[j,v]=d.swv.split(':');SWP.P[+j].v=v;swDraw();return 1}if(d.swgo&&SWP){swGo();return 1}if(d.swx){cShClose();SWP=null;return 1}
 if(d.whhk){const x=WU().find(y=>String(y.id)==String(d.whhk));if(!x)return 1;const v=prompt(`عدد الهالك من «${x.ty}${x.nm?' · '+x.nm:''}» (في المخزن ${x.qty}):`,'');const n=+String(v||'').replace(/[^\d.]/g,'');if(!(n>0))return 1;if(n>+x.qty&&!confirm('العدد أكبر من الرصيد. تكمل؟'))return 1;const why=prompt('السبب (اختياري):','')||'';whAdd(x,-n,'out','dmg','🗑 هالك'+(why?': '+why:''));sv();snd('ok');toastT('✓ اتخصم '+n+' هالك');render();return 1}
 return _v24Click24(d,b)};
// ---- 3) «وصفاتي» custom ad type → Acrylic boards «Wasfaty board»
function wsfMig(){if(DB.cfg.m24w)return;const A=DB.cfg.adTypes||[],ix=[];A.forEach((n,i)=>{if(n&&/وصفات/.test(n))ix.push(i)});
 const W=WU(),wi=W.filter(x=>/وصفات/.test((x.ty||'')+' '+(x.nm||'')));if(!ix.length&&!wi.length){DB.cfg.m24w=1;return}
 try{snapLater('قبل نقل «وصفاتي» للأكريليك بورد (2.4)',JSON.stringify(DB))}catch(e){}
 DB.ph.forEach(p=>{const R=p.rows||{};ix.forEach(i=>{const k='custom_'+i,L=R[k];if(!Array.isArray(L))return;R.ab=R.ab||[];L.forEach(r=>R.ab.push({it:'Wasfaty board',q:+r.q||0,stt:p.mod=='تعديل براندنج'?ABIO:ABMK,nt:r.nt||'',r:r.r,x:r.x}));delete R[k]})});
 ix.forEach(i=>{A[i]=''});wi.forEach(x=>{x.ty='Acrylic boards';x.nm='Wasfaty board';x.sec='';x.size='48×80';x.mat='أكريليك';x.sh=-1});DB.cfg.m24w=1;sv()}
setTimeout(()=>{try{wsfMig()}catch(e){console.warn('wsf',e)}},1200);
// new acrylic row: the work follows the item and the pharmacy type until the user picks it himself
const _draft24=draft;draft=function(t,s){const d=_draft24(t,s);if(t&&t.id=='ab'&&!(V.ed&&V.ed.t=='ab')&&!d._su){const o=abSttO(d);if(d.stt!==o[0])d.stt=o[0]}return d};
document.addEventListener('change',e=>{const x=e.target;if(x&&x.dataset&&x.dataset.t=='ab'&&x.dataset.k=='stt'&&V.dr&&V.dr.ab)V.dr.ab._su=1},true);

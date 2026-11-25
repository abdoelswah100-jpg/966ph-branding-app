// ---------- 3.1 (file n3.1.js) ----------
// 1) Wall Sticker «تخطيط» rolls in meters per section, taken automatically at execution (logo is printed to size: never);
//    length rule (Abdullah): a band up to 100 cm takes its length, a piece wider than 100 both ways is cut in 100 cm strips,
//    thin strips (≤ 30 cm) are cut 7 by 7 from a 70 cm band of their length (30 cm waste), + 6 % waste on top
// 2) outdoor sticker: printed ones are pulled from stock by exact size (with the arrow); frosted (ثلجي) ones come from the frosted roll in meters
// 3) received in the «الاستلام» tab while the same item is in stock → «من المخزن ولا من الطباعة؟» (execution already asked)
// 4) item statement (⋮): registered, taken by each pharmacy, damaged, returned, used, stock-take differences, now
// 5) consumables («أخرى»): − = used (logged as استهلاك)   6) stock-take file (966-warehouse, mode set): sets the count, logs the difference
const C31=()=>DB.cfg.c31=DB.cfg.c31||{},RLW31=1.06;
// ---- 1) layout length
function lyLen31(L){let c=0;const G={};L.forEach(({h,w,n})=>{if(!h||!w||!n)return;const lo=Math.min(h,w),hi=Math.max(h,w);if(lo<=30){G[hi]=(G[hi]||0)+lo*n;return}c+=(lo<=100?hi:Math.ceil(w/100-1e-9)*h)*n});Object.keys(G).forEach(hi=>{c+=Math.ceil(G[hi]/70-1e-9)*(+hi)});return c}
const rlN31=(r,k)=>k=='q'?(+r.q||0):k=='left'?(r.cx?0:Math.max(0,(+r.q||0)-(+r.x||0))):(+r.x||0);
rlMeters=function(p,k){const o={},G={},put=(y,m)=>{const s=rlKs(y);o[s]=o[s]||{k:y,m:0};o[s].m=wq(o[s].m+m)};
 ((p&&p.rows&&p.rows.ws)||[]).forEach(r=>{const y=rlK(r);if(!y)return;const n=rlN31(r,k);if(!n)return;if(y.nm=='تخطيط'){const s=rlKs(y);(G[s]=G[s]||{y,L:[]}).L.push({h:+r.h||0,w:+r.w||0,n})}else put(y,rlLen(r)*n/100)});
 ((p&&p.rows&&p.rows.so)||[]).forEach(r=>{if(r.km!='ثلجي')return;const n=rlN31(r,k);if(n)put({nm:'ثلجي شفاف',sec:''},rlLen(r)*n/100)});
 Object.keys(G).forEach(s=>put(G[s].y,wq(lyLen31(G[s].L)/100*RLW31)));return o};
// stock: the printed layout rolls (Wall Sticker 5000×100 …) become meter rolls; what pharmacies already executed counts as already taken
function lyFix31(){const c=C31();if(c.ly)return;const W=WU();W.filter(x=>x.ty=='Wall Sticker'&&['تخطيط','سي ثرو'].includes(x.nm)&&/^\d+(\.\d+)?×100$/.test(String(x.size))).forEach(x=>{const m=wq((+String(x.size).split('×')[0]||0)/100*(+x.qty||0));
  if(m>0)whAdd({sh:-1,ty:RLTY,nm:x.nm,sec:x.nm=='تخطيط'?(x.sec||''):'',mat:'',size:'عرض 1 م'},m,'in','conv','تحويل رول '+x.size+' (×'+x.qty+') لمتر');whLog('out',x,-(+x.qty||0),'conv','اتحول لرول بالمتر');W.splice(W.indexOf(x),1)});
 DB.ph.concat(typeof HID!='undefined'&&HIDDB===DB?HID:[]).forEach(p=>{const X=rlMeters(p,'x');p.rlx=p.rlx||{};Object.keys(p.rlx).concat(Object.keys(X)).forEach(s=>{if(/^تخطيط/.test(s)||/^ثلجي/.test(s))p.rlx[s]=X[s]?X[s].m:0});p.m26r=1});c.ly=1;sv()}
try{if(DB&&DB.ph)lyFix31()}catch(e){console.warn('ly31',e)}
// ---- 2) outdoor sticker: arrow + material, stock by exact size, frosted from the roll
(function(){const i=WXT.indexOf('so');if(i>=0)WXT.splice(i,1);const t=T.find(x=>x.id=='so');if(!t)return;const qi=t.f.findIndex(f=>f.k=='q');
 const add=[sel('sa','السهم',()=>['بدون','يمين','يسار']),sel('km','الخامة',()=>['مطبوع','ثلجي'])];add.forEach(f=>{if(!t.f.some(y=>y.k==f.k))t.f.splice(qi<0?t.f.length:qi,0,f)});
 const z0=t.z;t.z=function(r){let z=z0.apply(this,arguments);if(r&&r.sa&&r.sa!='بدون')z+=' · سهم '+r.sa;if(r&&r.km=='ثلجي')z+=' · ثلجي (من رول الثلجي)';return z}})();
const soNm31=r=>((r.nm=='أخرى'?r.nx:r.nm)||'')+(r.sa&&r.sa!='بدون'?' · سهم '+r.sa:'');
const _whParts31=whParts;whParts=function(t,r,s){if(t&&t.id=='so'){if(!r||r.km=='ثلجي')return [];return _whParts31.apply(this,arguments).map(y=>Object.assign(y,{nm:soNm31(r)}))}return _whParts31.apply(this,arguments)};
// ---- 3) receiving tab: ask too
rcvAfter=function(p,m){const R=V.v=='rcv',L=rcvDiff(p,m,R?'rcv':'xr',R?(V.rd||TD()):TD());rcvXr(p,L)};
rcvXr=function(p,L){if(!p||p._wh||p._rc||!WU().length)return;const C=L.filter(o=>o.d>0&&o.t&&o.e&&o.e.n>0&&whAv(p,o.t,o.r,o.sd)>0);if(!C.length)return;document.querySelectorAll('.toast.rcx').forEach(x=>x.remove());const rc=C.some(o=>o.e.src=='rcv');
 const tt=toast(`<span>📦 ${rc?'استلمت'+(C.length>1?' '+C.length+' بند':'')+' والصنف موجود في المخزن. ده اتاخد من المخزن ولا جه من الطباعة؟':'المتنفذ زاد عن المستلم'+(C.length>1?' في '+C.length+' بند':'')+' وفيه رصيد في المخزن. الزيادة جت من المخزن؟'}${C.some(o=>!o.sd&&whXT(o.t,o.r,p.sh,o.e.n))?'<br><b class="whxw">⚠ جزء منها هيتسحب من مخزن نوع رفوف تاني (نفس المقاس)</b>':''}</span><button class="pr" data-rcxw="1">من المخزن — اخصمه</button><button data-tclose="1">لا، من الطباعة</button>`);
 tt.classList.add('rem','rcx');tt._rx={pid:p.id,C:C.map(o=>({tid:o.t.id,rid:o.r._i,sd:o.sd,d:o.e.n,src:o.e.src}))};snd('tick')};
rcvXw=function(tt){const o=tt._rx,p=DB.ph.find(x=>x.id==o.pid);tt.remove();if(!p)return;let n=0;o.C.forEach(c=>{const r=(p.rows[c.tid]||[]).find(y=>y._i==c.rid),t=tOf(p,c.tid);if(!r||!t)return;const sc=c.src||'xr',e=(p.rcv||[]).filter(x=>x.rid==c.rid&&(x.sd||'')==(c.sd||'')&&x.src==sc).pop(),
  k=whDed(p,t,r,Math.min(c.d,e?e.n:c.d),c.sd,sc=='rcv'?'استلام من المخزن':'المتنفذ أكتر من المستلم — اتخصم من المخزن');if(!k)return;n+=k;if(e){e.n=wq(e.n-k);if(!e.n)p.rcv.splice(p.rcv.indexOf(e),1)}rcvLog(p,c.tid,r,k,c.sd,'wh',e&&e.dt||TD())});sv();render();toastT(n?'✓ اتخصم '+n+' من المخزن واتسجل مستلم من المخزن':'⚠ مفيش رصيد كفاية في المخزن')};
// ---- 4) item statement
function whStmt31(x){const L=(DB.wlog||[]).filter(e=>String(e.id)==String(x.id)),G={},ph={};let s=0;const g=(k,v)=>{G[k]=wq((G[k]||0)+v)};
 L.forEach(e=>{const q=+e.qty||0,src=String(e.src||'');s=wq(s+q);if(src=='conv')g('تحويل',q);else if(src=='jard')g('فرق جرد',q);else if(src=='dmg')g('هالك',q);else if(src=='use')g('استهلاك',q);else if(/^ph:/.test(src)){if(q<0){g('اتسحب للصيدليات',q);const k=src.slice(3);ph[k]=wq((ph[k]||0)-q)}else g('رجع من صيدليات (فائض / تصحيح)',q)}else if(src=='import')g('استيراد',q);else if(e.typ=='in')g('إضافة',q);else g('تعديل يدوي (+ / −)',q)});
 const u=whUnit(x.ty),now=+x.qty||0,gap=wq(now-s),f=v=>(v>0?'+':'')+wq(v)+' '+u;
 return `<div class="wcard st31"><h3>📒 كشف حساب الصنف</h3>${L.length?`<div class="sc"><table class="ctab"><tr><th>الحركة</th><th>الكمية</th></tr>${Object.keys(G).map(k=>`<tr><td>${k}</td><td><b class="${G[k]<0?'c-exp':'c-rem'}">${f(G[k])}</b></td></tr>`).join('')}${gap?`<tr><td>قبل بداية السجل</td><td>${f(gap)}</td></tr>`:''}<tr class="tot"><td>الموجود دلوقتي</td><td>${wq(now)} ${u}</td></tr></table></div>
 ${Object.keys(ph).length?`<small>اتسحب لـ: ${Object.keys(ph).map(k=>'صيدلية '+esc(k)+' ('+ph[k]+')').join(' · ')}</small>`:''}<small class="hint">آخر حركة: ${esc(fd(L[0].at))} · ${L.length} حركة</small>`:'<p class="em">مفيش حركات متسجلة للصنف ده لسه.</p>'}</div>`}
const _render031=render0;render0=function(){try{if(DB&&DB.ph&&!C31().ly)lyFix31()}catch(e){console.warn('ly31',e)}const r=_render031.apply(this,arguments);try{if(V.v=='whe'&&V.we&&V.we._old&&!document.querySelector('.st31')){const x=WU().find(y=>String(y.id)==String(V.we._old)),m=document.querySelector('main');if(x&&m)m.insertAdjacentHTML('beforeend',whStmt31(x))}}catch(e){console.warn(e)}return r};
// ---- 5) consumables: − = used
const _whClick31=whClick;whClick=function(d,b){if(d.whst){const[id,dv]=String(d.whst).split(':'),x=WU().find(y=>String(y.id)==String(id));if(x&&x.ty=='أخرى'&&+dv<0){if(+x.qty<1)return 1;whAdd(x,-1,'out','use','استخدمت (استهلاك)');sv();snd('tick');render();return 1}}return _whClick31(d,b)};
// ---- 6) stock-take file: set the count
let JRD31=null;
function jrdFind(z){return WU().filter(x=>x.ty==z.ty&&String(x.nm||'')==String(z.nm||'')&&String(x.sec||'')==String(z.sec||'')&&String(x.size||'')==String(z.size||'')&&(z.sh==null||x.sh==z.sh))}
function jrdOpen(q,fn){const L=(q.items||[]).filter(z=>z&&z.ty&&z.qty!=null&&isFinite(+z.qty)).map(z=>{const F=jrdFind(z),cur=wq(F.reduce((a,x)=>a+(+x.qty||0),0));return Object.assign({},z,{qty:wq(+z.qty),cur,ex:F.length})});if(!L.length)return alert('الملف مفيهوش أصناف صالحة');JRD31={L,fn:fn||'ملف'};cShClose();
 const el=document.createElement('div');el.className='csh';el.innerHTML=`<div class="cshb"><b>📋 جرد — يظبط الرصيد على الرقم اللي اتقاس</b><small>${esc(q.note||'')}</small><div class="sc"><table class="ctab"><tr><th>الصنف</th><th>دلوقتي</th><th>الجديد</th><th>الفرق</th></tr>${L.map(z=>{const d=wq(z.qty-z.cur),u=whUnit(z.ty);return `<tr><td>${esc(z.ty)}<small>${esc([z.nm,z.sec,z.size].filter(Boolean).join(' · '))}${z.ex?'':' · جديد'}</small></td><td>${z.cur} ${u}</td><td><b>${z.qty} ${u}</b></td><td><b class="${d<0?'c-exp':'c-rem'}">${d>0?'+':''}${d}</b></td></tr>`}).join('')}</table></div><small class="hint">الفرق بيتسجل في السجل «فرق جرد». البرنامج بياخد نقطة استرجاع قبلها.</small><div class="cshr"><button class="pr" data-jrd31="1">اعتمد الجرد</button><button data-cshx="1">إلغاء</button></div></div>`;document.body.appendChild(el)}
function jrdGo(){if(!JRD31)return;snap('قبل جرد · '+JRD31.fn);let n=0;JRD31.L.forEach(z=>{const F=jrdFind(z);let x=F[0];if(F.length>1)F.slice(1).forEach(y=>{if(+y.qty){whAdd(y,-(+y.qty),'adj','jard','فرق جرد (دمج في صنف واحد) · '+JRD31.fn)}});const cur=x?+x.qty||0:0,d=wq(z.qty-cur);
 if(!x&&!z.qty)return;if(d||!x){whAdd({sh:z.sh==null?-1:z.sh,ty:z.ty,nm:z.nm||'',sec:z.sec||'',mat:z.mat||'',size:z.size||''},d,'adj','jard','فرق جرد · '+JRD31.fn);n++}});JRD31=null;cShClose();sv();snd('ok');goV({v:'wh',op:{},dr:{},q:V.q,wf:V.wf});toastT('✓ اتظبط '+n+' صنف على الجرد')}
const _whImpOpen31=whImpOpen;whImpOpen=function(q,fn){if(q&&q.kind=='966-warehouse'&&q.mode=='set')return jrdOpen(q,fn);return _whImpOpen31(q,fn)};
const _v24Click31=v24Click;v24Click=function(d,b){if(d.jrd31){jrdGo();return 1}return _v24Click31(d,b)};
// 3.0 replaced capAuto and dropped the roll step that 2.6 had chained to it: put it back (rolls are taken at execution again)
const _capAuto31=capAuto;capAuto=function(){const r=_capAuto31.apply(this,arguments);try{const p=V&&V.p?DB.ph.find(x=>x.id==V.p):null;if(p)rlAuto(p);DB.ph.forEach(q=>{if(q!==p&&q.m26r&&rlOwed(q).length)rlAuto(q)})}catch(e){console.warn('rl',e)}return r};

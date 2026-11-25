// ---------- 3.0 (file n3.0.js) ----------
// Management report: order main → End gandola → Acrylic boards → caps → extra items → not executed (core reportRows);
// a swapped item is not counted, its replacement is counted in the main table with «منهم N تبديل بطلب العميل» (and left out of the extra items);
// caps: one line with the count, split تصنيع وتركيب / تركيب فقط (p.capIO, install-only caps are not taken from the warehouse);
// Decorative nail: تصنيع وتركيب (default) or تركيب فقط; report notes about the shelf type removed, the rest moved to a private note (p.pnt);
// PDF tables repeat their header row on every page (core pdfLayout).
const C30=()=>DB.cfg.c30=DB.cfg.c30||{};
const noSw=r=>!(r&&r.cx&&r.sw),isSwR=r=>!!(r&&isXI(r)&&r.swf);
const mrNoSw=o=>{const n={};Object.keys(o||{}).forEach(k=>{n[k]=Array.isArray(o[k])?o[k].filter(noSw):o[k]});return n};
// main-table rows: not extra (but swap replacements are), never a swapped original
function mrMain(p){const o=mrNoSw(xiRows(p,0));Object.keys(p.rows||{}).forEach(k=>{const a=p.rows[k];if(Array.isArray(a)&&a.some(isSwR))o[k]=(o[k]||[]).concat(a.filter(isSwR))});return o}
// how many of each main-table line are swap replacements
function mrSwMark(raw,P0){(P0||[]).forEach(p=>{Object.keys(p.rows||{}).forEach(k=>{const a=(p.rows[k]||[]);if(!Array.isArray(a))return;const S=a.filter(isSwR);if(!S.length)return;
 sizeRows([Object.assign({},p,{rows:{[k]:S}})]).forEach(s=>{const x=raw.find(y=>y.n==s.n&&y.sz==s.sz&&y.mat==s.mat);if(x)x.sw=(x.sw||0)+(+s.q||0)})})})}
const _xiList30=xiList;xiList=function(P){return _xiList30(P).filter(x=>{const p=(P||[]).find(q=>q.id==x.pid);if(!p)return true;return !Object.values(p.rows||{}).some(a=>Array.isArray(a)&&a.some(r=>r._i==x.rid&&isSwR(r)))})};
// caps counted without the swapped originals
const _capPcs30=capPcs;capPcs=function(p,id,k){const a=((p&&p.rows)||{})[id]||[];if(k!='q'||a.every(noSw))return _capPcs30.apply(this,arguments);return _capPcs30.call(this,Object.assign({},p,{rows:Object.assign({},p.rows,{[id]:a.filter(noSw)})}),id,k)};
// caps: install-only part (the pharmacy provided them)
const capIO=p=>Math.max(0,Math.round(+((p||{}).capIO)||0));
const _capRows30=capRows;capRows=function(P){const L=_capRows30(P);L.forEach(x=>{x.io=Math.min(x.q,(P||[]).reduce((a,p)=>a+capIO(p),0))});return L};
capTbl=function(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';const x=v[0],io=x.io||0,mk=x.q-io,stt=s=>s==ABMK?'<td style="background:#FAD4D4;font-weight:700">تصنيع + تركيب</td>':`<td>${s}</td>`;
 return `<h3>${CPNM}</h3><div class="sc"><table><tr><th>البند</th><th>الحالة</th><th>العدد</th><th class="act">إجراء</th></tr>${mk>0?`<tr><td>${CPNM}</td>${stt(ABMK)}<td>${mk}</td><td class="act"></td></tr>`:''}${io>0?`<tr><td>${CPNM}</td>${stt(ABIO)}<td>${io}</td><td class="act"></td></tr>`:''}<tr class="tot"><td colspan="2">إجمالي ${CPNM}</td><td>${x.q} قطعة</td><td class="act"><button data-rdel="base:${x._idx}" title="حذف الصف">حذف</button></td></tr></table></div>`};
// stock: install-only caps are never taken from the warehouse
const capX30=p=>Math.max(0,capN(p,'x')-capIO(p));
capAuto=function(){const p=V&&V.p?DB.ph.find(x=>x.id==V.p):null;try{capSettle(p)}catch(e){}if(!p||!p.m23||uStoreRO()||!uEditP(p))return;const t=capX30(p),c=+p.capx||0,d=t-c;if(!d)return;
 if(d<0){whAdd(CAPO,-d,'in','ph:'+p.no,'تصحيح '+CPNM+' (المتنفذ قل أو تركيب فقط)');p.capx=t;return}const k=Math.min(d,Math.max(0,Math.floor(capStock())));if(k>0){whAdd(CAPO,-k,'out','ph:'+p.no,CPNM+' مع السايد أكريليك (متنفذ)');p.capx=c+k}};
capSettle=function(skip){if(uStoreRO())return;let st=Math.floor(capStock());if(st<=0)return;DB.ph.forEach(q=>{if(q===skip||!q.m23||st<=0||!uEditP(q))return;const ow=capX30(q)-(+q.capx||0);if(ow<=0)return;const k=Math.min(ow,st);whAdd(CAPO,-k,'out','ph:'+q.no,CPNM+' مع السايد أكريليك (متركب قبل ما الأغطية توصل)');q.capx=(+q.capx||0)+k;st-=k})};
// Decorative nail: made + installed (default) or installation only
const _abSttO30=abSttO;abSttO=function(r){if(r&&r.it==NAIL)return [ABMK,ABIO];return _abSttO30.apply(this,arguments)};
// report notes: the shelf-type warnings go, the rest becomes a private pharmacy note (never printed)
function rnFix30(){const A=DB.ph.concat(typeof HID!='undefined'&&HIDDB===DB?HID:[]);let n=0;A.forEach(p=>{if(p.m30||!p.rn||!/نوع الرفوف/.test(p.rn)){p.m30=1;return}
 const keep=String(p.rn).split(/\s+·\s+/).filter(s=>s.trim()&&!/نوع الرفوف/.test(s));if(keep.length)p.pnt=[p.pnt,keep.join(' · ')].filter(Boolean).join('\n');p.rn='';p.m30=1;p.modAt=nowIso();n++});if(n)sv()}
try{if(DB&&DB.ph)rnFix30()}catch(e){console.warn(e)}
const _render030=render0;render0=function(){const r=_render030.apply(this,arguments);try{if(DB&&DB.ph&&DB.ph.some(p=>!p.m30))rnFix30();if(V.v=='ph'){const p=curP(),t=document.getElementById('trans');if(p&&t&&!document.getElementById('pnt30')){const l=t.closest('label')||t;
 l.insertAdjacentHTML('afterend',`<label>📝 ملاحظات خاصة (ليك إنت — مش بتظهر في أي تقرير)<textarea id="pnt30" rows="3">${esc(p.pnt||'')}</textarea></label>${capPcs(p,'saf','q')||capN(p,'q')?`<label>${CPNM}: منهم «تركيب فقط» (الصيدلية وفّرتهم)<input id="cio30" type="number" inputmode="numeric" min="0" value="${capIO(p)||''}" placeholder="0"></label><small class="hint">الباقي «تصنيع وتركيب». اللي تركيب فقط ما بيتخصمش من المخزن.</small>`:''}`)}}}catch(e){console.warn(e)}return r};
const _v33Change30=v33Change;v33Change=function(x){
 if(x.id=='pnt30'){const p=curP();if(p){p.pnt=x.value;p.modAt=nowIso();sv()}return 1}
 if(x.id=='cio30'){const p=curP();if(p){p.capIO=Math.max(0,Math.round(+x.value||0));p.modAt=nowIso();sv();try{capAuto()}catch(e){}toastT('✓ اتحفظ')}return 1}
 return _v33Change30(x)};

// ---------- v2.3: screw caps with the side acrylic ----------
const CPNM='غطاء مسمار',CAPO={sh:-1,ty:CPNM,nm:'',sec:'',mat:'',size:''};
const CAPS=[['eg','Side Acrylic Pocket (جندولة تركي قديم)',4],['saf','Side Acrylic Shelves Floor',4],['saw','Side Acrylic Shelves Wall',6]];
// pieces of one source: k='q' requested, 'x' executed
function capPcs(p,id,k){const sh=p.sh;return ((p.rows||{})[id]||[]).reduce((a,r)=>{if(id=='eg'){if(!egSub(r,sh))return a;return a+SDS.reduce((b,[sd])=>b+(k=='x'?pkv(r,'x',sd):egN(r,sh,sd)),0)}return a+(k=='x'?(+r.x||0):qn(r))},0)}
const capN=(p,k)=>CAPS.reduce((a,[id,,f])=>a+capPcs(p,id,k)*f,0);
const capLast=p=>{let l=null;TY(p).forEach(t=>{if(CAPS.some(c=>c[0]==t.id)&&capPcs(p,t.id,'q')>0)l=t.id});return l};
function capHtml(p){const L=CAPS.map(([id,n,f])=>[n,capPcs(p,id,'q'),f]).filter(x=>x[1]>0);if(!L.length)return '';const N=L.reduce((a,x)=>a+x[1]*x[2],0);
 return `<h3>${CPNM}</h3><div class="sc"><table><tr><th>مع</th><th>عدد القطع</th><th>لكل قطعة</th><th>عدد الأغطية</th></tr>${L.map(([n,q,f])=>`<tr><td>${esc(n)}</td><td>${q}</td><td>${f}</td><td><b>${q*f}</b></td></tr>`).join('')}<tr class="tot"><td colspan="3"><b>إجمالي ${CPNM}</b></td><td><b>${N} قطعة</b></td></tr></table></div>`}
function capRows(P){const parts=CAPS.map(([id,n,f])=>({n,q:P.reduce((a,p)=>a+capPcs(p,id,'q'),0),f})).filter(x=>x.q>0);if(!parts.length)return [];return [{kind:'cap',n:CPNM,ty:CPNM,sz:'',mat:'',q:parts.reduce((a,x)=>a+x.q*x.f,0),a:0,lm:0,parts}]}
function capTbl(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';const x=v[0];return `<h3>${CPNM}</h3><div class="sc"><table><tr><th>مع</th><th>عدد القطع</th><th>لكل قطعة</th><th>عدد الأغطية</th><th class="act">إجراء</th></tr>${x.parts.map(y=>`<tr><td>${esc(y.n)}</td><td>${y.q}</td><td>${y.f}</td><td>${y.q*y.f}</td><td class="act"></td></tr>`).join('')}<tr class="tot"><td colspan="3">إجمالي ${CPNM}</td><td>${x.q} قطعة</td><td class="act"><button data-rdel="base:${x._idx}" title="حذف الصف">حذف</button></td></tr></table></div>`}
// warehouse: executed caps leave the stock (difference since the last save, p.capx)
function capAuto(){const p=V&&V.p?DB.ph.find(x=>x.id==V.p):null;if(!p||!p.m23||uStoreRO()||!uEditP(p))return;const t=capN(p,'x'),d=t-(+p.capx||0);if(!d)return;whAdd(CAPO,-d,d>0?'out':'in','ph:'+p.no,d>0?CPNM+' مع السايد أكريليك (متنفذ)':'تصحيح '+CPNM+' (المتنفذ قل)');p.capx=t}
function v23Click(d,b){
 if(d.whcap){const v=prompt('عدد '+CPNM+' اللي هيتضاف للمخزن');const n=Math.round(+String(v||'').replace(/[^\d.]/g,''));if(!(n>0))return 1;whAdd(CAPO,n,'in','manual','إضافة '+CPNM);sv();snd('ok');toastT('✓ اتضاف '+n+' '+CPNM+' للمخزن');render();return 1}
 return 0}

// ---------- v1.9: Wall Header and Floor Header on Old Turkish = one stock (same sticker 17.5×100) ----------
// the Wall Header part on Old Turkish (not wood) is stored and pulled as «Floor Header» with the same name, size and material
const OT_WF=(t,r,s)=>t&&t.id=='wh'&&!wood(r)&&rsh(r,s)===2;
const _whParts19=whParts;whParts=function(t,r,s){const L=_whParts19(t,r,s);if(!OT_WF(t,r,s))return L;return L.map(y=>y.ty=='Wall Header'?Object.assign({},y,{ty:'Floor Header'}):y)};
function otWF19(){const W=DB.wh||[];if(!W.some(x=>x.ty=='Wall Header'&&x.sh==2&&!x.old))return;
 if(!DB.cfg.m19wf){try{snapLater('قبل تحديث 1.9 (Wall Header تركي قديم = Floor Header)',JSON.stringify(dbOut()))}catch(e){}DB.cfg.m19wf=nowIso()}
 W.forEach(x=>{if(x.ty=='Wall Header'&&x.sh==2&&!x.old)x.ty='Floor Header'});
 for(let i=W.length-1;i>=0;i--){const k=whKey(W[i]),j=W.findIndex(y=>whKey(y)==k);if(j>=0&&j<i){W[j].qty=wq(+W[j].qty+(+W[i].qty||0));if(W[i].min!==''&&W[i].min!=null&&(W[j].min===''||W[j].min==null))W[j].min=W[i].min;W.splice(i,1)}}
 svq()}
const _WU19=WU;WU=function(){const W=_WU19();if(W.some(x=>x.ty=='Wall Header'&&x.sh==2&&!x.old))otWF19();return DB.wh};

// ---------- v1.9: empty acrylic (أكريليك فاضي) — offered for «ستيكر + تصنيع أكريليك» too, Floor/Wall on Old Turkish share it ----------
const _whOldOpts19=whOldOpts;whOldOpts=function(p,t,r){const o=_whOldOpts19(p,t,r);try{
 if(!p||p._wh||p._rc||!(t.id=='fh'||(t.id=='wh'&&!wood(r))))return o;const sh=rsh(r,p.sh);if(sh!==2)return o;
 const mode=t.id=='wh'?whmOf(r):fhmOf(r);if(mode!=FHM[0]&&!isOld(p,r))return o;
 const need=Math.max(0,qn(r)-(+r.r||0));if(!need)return o;const sz=v=>String(v||'').replace(/\s+/g,''),z=SZ('wh.h')[2]+'×100';
 WU().filter(x=>x.old&&!x.solo&&+x.qty>=1&&(x.ty==OLDT.bwh||x.ty==OLDT.bfh)&&x.sh==2&&sz(x.size)==sz(z)&&!o.some(c=>c.id==x.id)).forEach(x=>{const n=Math.min(need,Math.floor(+x.qty));
  if(n>0)o.push({k:'o',id:x.id,n,txt:`🕰 ${n} أكريليك فاضي ${x.size}${x.ty==OLDT.bwh&&t.id=='fh'?' (من أكريليك الـ Wall Header)':x.ty==OLDT.bfh&&t.id=='wh'?' (من أكريليك الـ Floor Header)':''} — بدل تصنيع أكريليك جديد (في المخزن ${wq(x.qty)})`})})
 }catch(e){console.error(e)}return o};

// ---------- v1.9: receive file from the printing department (kind 966-receive) ----------
// file: {kind:'966-receive', dt:'YYYY-MM-DD', note, ph:[{no, mod, sh, rows:{tid:[row with q = received]}}]}
// it never adds items: each row goes through the same path as «📥 الاستلام ← استلام بالبنود» (rcvPut / rcvWh / waiting list)
let RIMP=null;
function rimPh(z){const no=String(z.no||'').trim(),L=DB.ph.filter(p=>String(p.no||'').trim()==no);if(!L.length)return null;
 const m=z.mod?L.filter(p=>p.mod==z.mod):L;const A=(m.length?m:L).slice().sort((a,b)=>((a.st=='مكتملة')-(b.st=='مكتملة'))||String(b.mo||'').localeCompare(String(a.mo||''))||b.id-a.id);return A[0]}
function rimPlan(q){const P=[];(q.ph||[]).forEach(z=>{const p=rimPh(z),o={z,p,ok:[],xs:[],wait:[],short:[],over:[],n:0};
  const C=p?JSON.parse(JSON.stringify(p)):null;
  Object.keys(z.rows||{}).forEach(tid=>(z.rows[tid]||[]).forEach(y=>{const n=qn(y);if(!(n>0))return;o.n+=n;
   if(!p){const t=T.find(x=>x.id==tid);let s='';try{s=t?t.n+': '+t.z(y,+z.sh||0):tid}catch(e){s=tid}o.wait.push({s,n});return}
   const t=tOf(p,tid);if(!t){o.xs.push({s:tid,n});return}
   if(rcvPut(C,t,y,TD()))o.ok.push({s:rcvZ(p,tid,y,''),n});else o.xs.push({s:rcvZ(p,tid,y,''),n})}));
  if(C)rcvRows(C).forEach(([tid,r])=>{if(r.cx)return;const t=tOf(C,tid);if(!t||(t.id=='eg'&&egAO(r,C.sh)))return;const q2=qn(r),v=+r.r||0;
   if(v<q2)o.short.push({s:rcvZ(C,tid,r,''),n:wq(q2-v),of:q2});else if(v>q2)o.over.push({s:rcvZ(C,tid,r,''),n:wq(v-q2)})});
  P.push(o)});return P}
function rcvImpOpen(q,fn){if(!q||!Array.isArray(q.ph)||!q.ph.length)return alert('ملف الاستلام مفيهوش صيدليات');
 const P=rimPlan(q);RIMP={q,fn:fn||'ملف',P};if(typeof cShClose=='function')cShClose();const el=document.createElement('div');el.className='csh';
 const li=(L,cls,pre)=>L.map(x=>`<div class="cnpi ${cls}"><b>${pre}${wq(x.n)}${x.of?' من '+x.of:''}</b><span>${esc(x.s)}</span></div>`).join('');
 el.innerHTML=`<div class="cshb"><b>📥 ملف استلام من الطباعة · ${P.length} صيدلية</b><small>${esc(RIMP.fn)}${q.note?' · '+esc(q.note):''} · تاريخ الاستلام ${ddm(q.dt||TD())}. الملف ما بيضيفش بنود: بيكتب العدد في «المستلم» للبند المطلوب، واللي مش مطلوب بيروح المخزن. فيه نقطة استرجاع قبل التسجيل.</small>
 <div class="cnpl">${P.map(o=>`<h3>🏥 ${esc(o.z.no)}${o.p?' · '+esc(o.p.mod||'')+' · '+SH[o.p.sh]:' · مش متسجلة'}</h3>
  ${o.p?`<small>✅ ${o.ok.length} بند هيتسجل مستلم · ❌ ناقص بعد الملف ${o.short.reduce((a,x)=>a+x.n,0)} · ➕ زيادة ${o.over.reduce((a,x)=>a+x.n,0)} · 📦 مش مطلوب ${o.xs.reduce((a,x)=>a+x.n,0)}</small>`:`<small>⏳ الصيدلية مش متسجلة: ${o.wait.length} بند هيستنى ويتربط لوحده أول ما تضيفها</small>`}
  ${li(o.short,'rim-sh','❌ ناقص ')}${li(o.over,'rim-ov','➕ زيادة ')}${li(o.xs,'rim-xs','📦 مش مطلوب ← المخزن ')}${li(o.wait,'rim-w','⏳ ')}
  ${o.p&&!o.short.length&&!o.over.length&&!o.xs.length?'<div class="cnpi"><b>✓</b><span>كله مستلم بالظبط</span></div>':''}`).join('')}</div>
 <div class="cshr"><button class="pr" data-rimgo="1">${ic('check')}سجّل الاستلام</button><button data-cshx="1">إلغاء</button></div></div>`;document.body.appendChild(el)}
function rimGo(){if(!RIMP)return;const {q,fn}=RIMP,dt=q.dt||TD();for(const z of q.ph){const p=rimPh(z);if(p&&!uEditP(p))return toastT('👁 صيدلية '+z.no+' للعرض بس')}
 try{snapLater('قبل ملف استلام · '+fn,JSON.stringify(dbOut()))}catch(e){}
 const bid=rid(),U=[];let a=0,w=0,k=0;
 q.ph.forEach(z=>{const p=rimPh(z);const ids=p?new Map((p.rcv||[]).map(e=>[e.id,e.n])):null;
  Object.keys(z.rows||{}).forEach(tid=>(z.rows[tid]||[]).forEach(y0=>{const y=JSON.parse(JSON.stringify(y0));delete y._i;delete y.r;if(!(qn(y)>0))return;
   if(!p){const sh=+z.sh||0,t=T.find(x=>x.id==tid);let s='';try{s=t?t.n+': '+t.z(y,sh):tid}catch(e){}const e={id:rid(),no:String(z.no),sh,tid,y,dt,at:nowIso(),z:s,b:bid};RQ().push(e);U.push({q:e.id});k++;return}
   const t=tOf(p,tid);if(t&&rcvPut(p,t,y,dt)){a++;return}
   if(t)rcvWh(t,y,p.sh,'ph:'+p.no,'استلام مش مطلوب في صيدلية '+p.no+' (ملف استلام)');const e={id:rid(),dt,at:nowIso(),tid,n:qn(y),src:'xs',y,z:rcvZ(p,tid,y,'')};(p.rcv=p.rcv||[]).push(e);U.push({p:p.id,e:e.id,xs:1});w++}));
  if(p)(p.rcv||[]).forEach(e=>{const d=wq(e.n-(ids.get(e.id)||0));if(d>0&&!U.some(u=>u.e==e.id))U.push({p:p.id,e:e.id,d})});if(p)p.modAt=nowIso()});
 DB.cfg.rimLast={b:bid,at:nowIso(),fn,dt,U};RIMP=null;if(typeof cShClose=='function')cShClose();sv();snd('ok');
 const p0=rimPh(q.ph[0]);goV({v:'rcv',p:p0?p0.id:V.p,rn:String(q.ph[0].no||''),rd:dt,op:{},dr:{},q:V.q});
 toastT([a?`✓ ${a} بند اتسجل مستلم`:'',w?`📦 ${w} بند مش مطلوب راح المخزن`:'',k?`⏳ ${k} بند مستني تسجيل الصيدلية`:''].filter(Boolean).join(' · ')||'مفيش بنود')}
// undo the last receive file (only what that file added)
function rimUndo(){const L=DB.cfg.rimLast;if(!L)return;if(!confirm('تتراجع عن ملف الاستلام «'+L.fn+'»؟\nالمستلم اللي الملف ده سجّله بس هيتشال، واللي راح المخزن هيترجع.'))return;
 try{snapLater('قبل التراجع عن ملف استلام · '+L.fn,JSON.stringify(dbOut()))}catch(e){}let n=0;
 L.U.forEach(u=>{if(u.q){const i=RQ().findIndex(x=>x.id==u.q);if(i>=0){RQ().splice(i,1);n++}return}
  const p=DB.ph.find(x=>x.id==u.p);if(!p)return;const e=(p.rcv||[]).find(x=>x.id==u.e);if(!e)return;
  if(u.xs){rcvUndo(p,e);n++;return}
  const r=(p.rows[e.tid]||[]).find(y=>y._i==e.rid),d=Math.min(u.d,e.n);if(r){const k=e.sd?'rp'+e.sd:'r';r[k]=Math.max(0,wq((+r[k]||0)-d))}e.n=wq(e.n-d);if(e.n<=0)p.rcv.splice(p.rcv.indexOf(e),1);p.modAt=nowIso();n++});
 delete DB.cfg.rimLast;sv();render();toastT('↩ اتشال '+n+' سطر استلام من الملف')}
const _rcvHtml19=rcvHtml;rcvHtml=function(){const L=DB.cfg.rimLast;return (L?`<div class="wcard"><small>آخر ملف استلام: <b>${esc(L.fn)}</b> · ${ddm(L.dt||TD())}</small><div class="tt"><button data-rimundo="1">↩ تراجع عن آخر ملف استلام</button></div></div>`:'')+_rcvHtml19()};
const _rcvClick19=rcvClick;rcvClick=function(d,b){if(d.rimgo){rimGo();return 1}if(d.rimundo){rimUndo();return 1}return _rcvClick19(d,b)};
// every file door knows the receive file
const _syncRoute19=syncRoute;syncRoute=function(q,fn){if(q&&q.kind=='966-receive'){alert('الملف ده ملف استلام من الطباعة، مش ملف مزامنة.\nهيتفتح في «📥 الاستلام» (بيكتب المستلم بس، ومش بيضيف بنود).');rcvImpOpen(q,fn);return 1}return _syncRoute19(q,fn)};
const _whImpOpen19=whImpOpen;whImpOpen=function(q,fn){if(q&&q.kind=='966-receive')return rcvImpOpen(q,fn);return _whImpOpen19(q,fn)};

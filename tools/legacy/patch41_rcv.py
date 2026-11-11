"""v1.9 part 4: receiving (الاستلام) separate from the pharmacy request, executed > received may come from the
warehouse (asked), Wall Header on Old Turkish like the Floor Header."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'rcvHtml' not in s

# ---- A. Wall Header on Old Turkish: sticker + acrylic / sticker only
rep("fhmOf=r=>FHM.includes(r&&r.fhm)?r.fhm:FHM[0],", "fhmOf=r=>FHM.includes(r&&r.fhm)?r.fhm:FHM[0],whmOf=r=>FHM.includes(r&&r.whm)?r.whm:FHM[0],")
rep("sel('len','الطول / مقاس الخشب (سم)',r=>wood(r)?SZ('wh.wood'):SZ('wh.len')),Q],",
    "sel('len','الطول / مقاس الخشب (سم)',r=>wood(r)?SZ('wh.wood'):SZ('wh.len')),Object.assign(sel('whm','المطلوب',()=>FHM),{hide:(d,s)=>rsh(d,s)!==2}),Q],")
rep("${SZ('mt.wh')}`", "${s==2?whmOf(r):SZ('mt.wh')}`", 2)
rep("${x.t.id=='fh'&&rsh(x.r,x.s)===2?`<small class=\"rshc fhx\">${k=='x'?(fhmOf(x.r)==FHM[1]?'تركيب ستيكر فقط':'تصنيع أكريليك + تركيب ستيكر'):fhmOf(x.r)}</small>`:''}",
    "${(x.t.id=='fh'||x.t.id=='wh')&&rsh(x.r,x.s)===2?`<small class=\"rshc fhx\">${k=='x'?((x.t.id=='wh'?whmOf(x.r):fhmOf(x.r))==FHM[1]?'تركيب ستيكر فقط':'تصنيع أكريليك + تركيب ستيكر'):(x.t.id=='wh'?whmOf(x.r):fhmOf(x.r))}</small>`:''}")
rep("f.k=='fhm'?(rsh(y,p.sh)===2?fhmOf(y):''):", "f.k=='fhm'?(rsh(y,p.sh)===2?fhmOf(y):''):f.k=='whm'?(rsh(y,p.sh)===2?whmOf(y):''):")
rep("if(x.ty=='Floor Header'&&x.sh==2&&x.mat=='ستيكر')x.mat=FHM[0];x.m19=1}",
    "if(x.ty=='Floor Header'&&x.sh==2&&x.mat=='ستيكر')x.mat=FHM[0];x.m19=1}if(!x.m19w){if(x.ty=='Wall Header'&&x.sh==2&&x.mat=='ستيكر')x.mat=FHM[0];x.m19w=1}")

# ---- B. receiving: storage, migration, hooks
rep("const UST=['cust','mnt','wh','wlog','invs','qi']", "const UST=['cust','mnt','wh','wlog','invs','qi','rcvq']")
rep("function mig(p){mig2(p);migHR(p);migCK(p);migPK(p);migRX(p);", "function mig(p){mig2(p);migHR(p);migCK(p);migPK(p);migRX(p);migRCV(p);")
rep("const curP=()=>V.v=='wha'?WHP():DB.ph.find(x=>x.id==V.p);", "const curP=()=>V.v=='wha'?WHP():V.v=='rca'?RCP():DB.ph.find(x=>x.id==V.p);")
rep("return !!(p&&(p.dz=='قديم'||p._wh))", "return !!(p&&(p.dz=='قديم'||p._wh||p._rc))")
rep("function whFromOpts(p,t,r){if(!p||p._wh||!WU().length)return [];", "function whFromOpts(p,t,r){if(!p||p._wh||p._rc||!WU().length)return [];")
rep("function whPullOffer(p,t,r){if(!p||p._wh||!WU().length)return;", "function whPullOffer(p,t,r){if(!p||p._wh||p._rc||!WU().length)return;")
rep("function whTake(p,t,r,L,note){", "function whTake0(p,t,r,L,note){")
rep("r.wf=(+r.wf||0)+c.n;r.r=Math.min(qn(r),(+r.r||0)+c.n)}", "r.wf=(+r.wf||0)+c.n;{const m_=rcvSnap(p,[r]);r.r=Math.min(qn(r),(+r.r||0)+c.n);rcvDiff(p,m_,'wh')}}")
rep("['wf','wfpR','wfpL'].forEach(k=>{if(o0[k]!=null)r[k]=o0[k]})}", "['wf','wfpR','wfpL'].forEach(k=>{if(o0[k]!=null)r[k]=o0[k]});if(o0._i)r._i=o0._i}")
rep("delete V.dr[d.rep].x;", "delete V.dr[d.rep].x;delete V.dr[d.rep]._i;")
rep("q.id=Date.now();q.no=n.trim();", "q.id=Date.now();q.no=n.trim();delete q.rcv;q.m20=1;")
# checklist actions: received only from the receiving screen; every change of received is logged
rep("if(d.tk||d.tf||d.tkt||d.tkall||d.tkclr){if(!p)return;snd('tick');",
    "if(d.tk||d.tf||d.tkt||d.tkall||d.tkclr){if(!p)return;if(tkRO(String(d.tk||d.tf||d.tkt||d.tkall||d.tkclr).split(':')[0])){toastT(RCVM);return}const m_=rcvSnap(p);snd('tick');")
rep("sv();tkRe();return}", "rcvAfter(p,m_);sv();tkRe();return}")
rep("if(x.dataset.tv){const p=curP(),[k,tid,i]=x.dataset.tv.split(':');if(p){snd('tick');tkSet(p,k,tid,i,x.value);sv();tkRe()}return}",
    "if(x.dataset.tv){const p=curP(),[k,tid,i]=x.dataset.tv.split(':');if(p){if(tkRO(k)){render();return}const m_=rcvSnap(p);snd('tick');tkSet(p,k,tid,i,x.value);rcvAfter(p,m_);sv();tkRe()}return}")
# read-only received in the pharmacy checklist
rep("<div class=\"tt np\"><button data-tkall=\"${k}\">${ic('check')}${TKL[k].all}</button><button data-tkclr=\"${k}\">↺ تصفير الكل</button></div>",
    "${tkRO(k)?`<div class=\"tt np\"><button class=\"pr\" data-rcvgo=\"${p.id}\">📥 سجّل الاستلام للصيدلية دي</button></div><small class=\"np sub\">${RCVM}</small>`:`<div class=\"tt np\"><button data-tkall=\"${k}\">${ic('check')}${TKL[k].all}</button><button data-tkclr=\"${k}\">↺ تصفير الكل</button></div>`}")
rep("<button class=\"np\" data-tkt=\"${k}:${g.t.id}\">✓ الكل</button>", "${tkRO(k)?'':`<button class=\"np\" data-tkt=\"${k}:${g.t.id}\">✓ الكل</button>`}")
TKV = '<td><div class="tkv"><button class="np" data-tk="${id}:-1" aria-label="ناقص">−</button><input type="number" inputmode="numeric" min="0" data-tv="${id}" value="${v}"><button class="np" data-tk="${id}:1" aria-label="زائد">+</button><button class="np tkf" data-tf="${id}">✓</button></div></td>'
rep(TKV, '<td>${tkRO(k)?`<b class="tkro">${v}</b>`:`' + TKV[4:-5] + '`}</td>', 2)
# screens, menu, dispatchers, guards
rep("const MENU=[['usr',", "const MENU=[['rcv','الاستلام','box'],['usr',")
rep("const TABOF={usr:'',", "const TABOF={rcv:'',rca:'',usr:'',")
rep("\n if(V.v=='mclose'){", "\n if(V.v=='rcv'){a.innerHTML=hdr(V.bp?'<button data-rcvb=\"1\">‹ الصيدلية</button>':backBtn(),'📥 الاستلام')+`<main>${rcvHtml()}</main>`;return}\n if(V.v=='rca'){a.innerHTML=hdr('<button data-rcax=\"1\">‹ الاستلام</button>','استلام بالبنود')+`<main>${rcaHtml()}</main>`;return}\n if(V.v=='mclose'){")
rep("function render(){const a=$('#app');EDTD=false;", "function render(){const a=$('#app');EDTD=false;try{rcvAuto()}catch(e){console.error(e)}")
rep("x15Click(d,b)||rlClick(d)", "x15Click(d,b)||rcvClick(d,b)||rlClick(d)")
rep("x15Change(x)||rlChange(x)", "x15Change(x)||rcvChange(x)||rlChange(x)")
rep("['ph','qe','exec','sum','wht','xr','rev'].includes(v)", "['ph','qe','exec','sum','wht','xr','rev','rcv'].includes(v)")
rep("(v=='sum'&&x.dataset&&x.dataset.tv)", "((v=='sum'||v=='rcv')&&x.dataset&&x.dataset.tv)")
rep("const PHEDIT=['cdz',", "const PHEDIT=['rcdel','rcaok','cdz',")

JS = r"""// ---------- v1.9: receiving (الاستلام) separate from the pharmacy: the pharmacy keeps the request and the executed,
// the received is entered here by pharmacy number (same item cards), every change of received is logged in p.rcv
const RCVM='المستلم بيتسجل من شاشة 📥 الاستلام (من القائمة ☰) برقم الصيدلية';
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
function whAv(p,t,r,sd){const P=whParts(t,r,p.sh),q=y=>+(whFind(whKey(y))||{}).qty||0;if(sd){const y=P.find(z=>z.pk==sd);return y?Math.floor(q(y)+1e-9):0}const M=P.filter(z=>!z.pk);return M.length?Math.min(...M.map(y=>y.f>0?Math.floor((q(y)+1e-9)/y.f):0)):0}
function whDed(p,t,r,n,sd,note){const k=Math.min(n,whAv(p,t,r,sd));if(!(k>0))return 0;const P=whParts(t,r,p.sh);if(sd){const y=P.find(z=>z.pk==sd);whAdd(whFind(whKey(y)),-k,'out','ph:'+p.no,note);r['wfp'+sd]=(+r['wfp'+sd]||0)+k}else{P.filter(z=>!z.pk).forEach(y=>whAdd(whFind(whKey(y)),-k*y.f,'out','ph:'+p.no,note));r.wf=(+r.wf||0)+k}return k}
function rcvXr(p,L){if(!p||p._wh||p._rc||!WU().length)return;const C=L.filter(o=>o.d>0&&o.t&&o.e&&o.e.n>0&&whAv(p,o.t,o.r,o.sd)>0);if(!C.length)return;document.querySelectorAll('.toast.rcx').forEach(x=>x.remove());
 const tt=toast(`<span>📦 المتنفذ زاد عن المستلم${C.length>1?' في '+C.length+' بند':''} وفيه رصيد في المخزن. الزيادة جت من المخزن؟</span><button class="pr" data-rcxw="1">نعم، اخصمها من المخزن</button><button data-tclose="1">لا، من الطباعة</button>`);tt.classList.add('rem','rcx');tt._rx={pid:p.id,C:C.map(o=>({tid:o.t.id,rid:o.r._i,sd:o.sd,d:o.e.n}))};snd('tick')}
function rcvXw(tt){const o=tt._rx,p=DB.ph.find(x=>x.id==o.pid);tt.remove();if(!p)return;let n=0;o.C.forEach(c=>{const r=(p.rows[c.tid]||[]).find(y=>y._i==c.rid),t=tOf(p,c.tid);if(!r||!t)return;const e=(p.rcv||[]).filter(x=>x.rid==c.rid&&(x.sd||'')==(c.sd||'')&&x.src=='xr').pop(),k=whDed(p,t,r,Math.min(c.d,e?e.n:c.d),c.sd,'المتنفذ أكتر من المستلم — اتخصم من المخزن');if(!k)return;n+=k;if(e){e.n=wq(e.n-k);if(!e.n)p.rcv.splice(p.rcv.indexOf(e),1)}rcvLog(p,c.tid,r,k,c.sd,'wh',TD())});sv();render();toastT(n?'✓ اتخصم '+n+' من المخزن واتسجل مستلم من المخزن':'⚠ مفيش رصيد كفاية في المخزن')}
// the pharmacy for a number (the open one first, then the newest)
function rcvPh(no){no=String(no||'').trim();if(!no)return null;const L=DB.ph.filter(p=>String(p.no||'').trim()==no);if(!L.length)return null;const c=L.find(p=>p.id==V.p);if(c)return c;return L.slice().sort((a,b)=>((a.st=='مكتملة')-(b.st=='مكتملة'))||String(b.mo||'').localeCompare(String(a.mo||''))||b.id-a.id)[0]}
// same item = same type and the same choices (not the count, notes, old design, tahtit width, pocket counts)
const RCX=['q','nt','od','tw','pR','pL'];
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
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
CSS = "\n.tkro{font-size:15px;display:inline-block;min-width:30px;text-align:center}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
# changelog
rep("'Fix: roll requests no longer break the management report (own field p.rolls)']",
    "'Fix: roll requests no longer break the management report (own field p.rolls)','Receiving (📥 الاستلام) separate from the pharmacy: by pharmacy number, with the item cards or the count against the request; not requested → warehouse automatically; waiting items link when the pharmacy is added; log per pharmacy; receiving report (PDF / WhatsApp)','Executed more than received: asks if the extra came from the warehouse (then taken out of stock)','Wall Header on Old Turkish: ستيكر + تصنيع أكريليك (default) / ستيكر فقط, like the Floor Header']")
EN = {'الاستلام':'Receiving','📥 الاستلام':'📥 Receiving','استلام بالبنود':'Receive by items','استلام بالبنود (زي إضافة الصيدلية)':'Receive by items (like adding a pharmacy)','رقم الصيدلية':'Pharmacy number','تاريخ الاستلام':'Receiving date','اكتب الرقم':'Type the number','سجل الاستلام للصيدلية دي':'Receiving log of this pharmacy','المصدر':'Source','استلام من الطباعة':'Received from print','مش مطلوب → المخزن':'Not requested → warehouse','من المخزن':'From the warehouse','اتعدّل من التنفيذ':'Set by the executed','رصيد سابق':'Earlier balance','مستني تسجيل الصيدلية':'Waiting for the pharmacy','تقرير الاستلام':'Receiving report','📄 تقرير الاستلام':'📄 Receiving report','من':'From','إلى':'To','مفيش استلام في الفترة دي':'No receiving in this period','حفظ الاستلام':'Save receiving','📥 سجّل الاستلام للصيدلية دي':'📥 Record receiving for this pharmacy','المستلم بيتسجل من شاشة 📥 الاستلام (من القائمة ☰) برقم الصيدلية':'Received is entered in the 📥 Receiving screen (menu ☰) by pharmacy number','أو اكتب العدد المستلم قدام المطلوب على طول:':'Or type the received count next to the request:','اكتب رقم الصيدلية علشان تسجل المستلم.':'Type the pharmacy number to record what was received.','نعم، اخصمها من المخزن':'Yes, take it from the warehouse','لا، من الطباعة':'No, from print','📦 للمخزن':'📦 To warehouse','المطلوب':'Required','‹ الاستلام':'‹ Receiving','‹ الصيدلية':'‹ Pharmacy'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j]); add = 0
for a2, c in EN.items():
    if a2 not in D: D[a2] = c; add += 1
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok, EN added', add)

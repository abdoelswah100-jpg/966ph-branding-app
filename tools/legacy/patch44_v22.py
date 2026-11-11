"""v2.2: maintenance pharmacies (own list per month, apart from the monthly board / review / reports, no automatic items,
executed items go to the maintenance log), car plate for fuel and car, Old Turkish one size 17.5x100 (Floor / Wall Header),
Side Acrylic Shelves Wall sizes 215x35 / 215x40 / 215x45, management totals per material."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'mntSync' not in s

# ---- sizes
rep("'saw':['215×35','215×45','40×125'],", "'saw':['215×35','215×40','215×45'],")
rep("'fh.s':['11.5×57','14×59','17×100','12×53.5','11.5×57']", "'fh.s':['11.5×57','14×59','17.5×100','12×53.5','11.5×57']")
rep("NMF,sel('sz','الحجم',r=>two(r)?['صغير','كبير']:['قياسي'])", "NMF,sel('sz','الحجم',(r,s)=>two(r)&&s!==2?['صغير','كبير']:['قياسي'])")
rep("const d=r.sz=='كبير'?SZ('fh.l'):SZ('fh.s')[s];", "const d=r.sz=='كبير'&&s!=2?SZ('fh.l'):SZ('fh.s')[s];")
rep("sel('len','الطول / مقاس الخشب (سم)',r=>wood(r)?SZ('wh.wood'):SZ('wh.len'))", "sel('len','الطول / مقاس الخشب (سم)',(r,s)=>wood(r)?SZ('wh.wood'):s===2?['100']:SZ('wh.len'))")
rep("function WU(){DB.wh=DB.wh||[];DB.wlog=DB.wlog||[];", "function WU(){DB.wh=DB.wh||[];DB.wlog=DB.wlog||[];if(DB.wh.some(x=>!x.m22))whFix22();")

# ---- custody: car plate for fuel and car
rep("car:o.car!=null&&o.car!==''?o.car:(kind=='وقود'?CU().cfg.car:'')", "car:o.car!=null&&o.car!==''?o.car:((kind=='وقود'||kind=='سيارة')?CU().cfg.car:'')")
rep("if(d.kind=='وقود'&&!d.car)d.car=CU().cfg.car", "if((d.kind=='وقود'||d.kind=='سيارة')&&!d.car)d.car=CU().cfg.car", 2)
rep("<label>لوحة العربية (للديزل)<input data-cc=\"car\"", "<label>لوحة العربية (للوقود والسيارة)<input data-cc=\"car\"")

# ---- maintenance pharmacies: no automatic items
rep("st:'لم تبدأ',rows:{ab:ABD()},m1:1,modAt:nowIso()};", "st:'لم تبدأ',rows:mod=='صيانة'?{}:{ab:ABD()},m1:1,modAt:nowIso()};")
rep("mo,st:'لم تبدأ',rows:{ab:ABD()},m1:1,modAt:nowIso()});", "mo,st:'لم تبدأ',rows:($('#pmod').value||'')=='صيانة'?{}:{ab:ABD()},m1:1,modAt:nowIso()});")
# work type on items of a maintenance pharmacy
rep("if(t.f){t.f.push(Object.assign(sel('xi',", "if(t.f){t.f.push(Object.assign(sel('mw','نوع العمل (الصيانة)',()=>MWL()),{hide:()=>{const p=curP();return !isMnt(p)}}));t.f.push(Object.assign(sel('xi',")
rep("f.k=='xi'?(y.xi=='نعم'?'نعم':''):", "f.k=='xi'?(y.xi=='نعم'?'نعم':''):f.k=='mw'?'':")
rep("const RCX=['q','nt','od','tw','pR','pL','xi','xn'];", "const RCX=['q','nt','od','tw','pR','pL','xi','xn','mw'];")
# apart from the monthly board / review / reports
rep("L=DB.ph.filter(p=>p.mo==m).sort(pSort),S=mStats(L),P=pv?mStats(DB.ph.filter(p=>p.mo==pv)):null", "L=DB.ph.filter(p=>p.mo==m&&isBr(p)).sort(pSort),S=mStats(L),P=pv?mStats(DB.ph.filter(p=>p.mo==pv&&isBr(p))):null")
rep("${routeHtml(L.filter(p=>!V.mf||p.st==V.mf))}", "${routeHtml(DB.ph.filter(p=>p.mo==m&&(!V.mf||p.st==V.mf)).sort(pSort))}")
rep("function revStart(m){const ids=DB.ph.filter(x=>x.mo==m).sort(pSort)", "function revStart(m){const ids=DB.ph.filter(x=>x.mo==m&&isBr(x)).sort(pSort)")
rep("need=DB.ph.filter(p=>revSt(p)!='ok').length", "need=DB.ph.filter(p=>isBr(p)&&revSt(p)!='ok').length")
rep("ms.map(m=>{const L=DB.ph.filter(p=>p.mo==m),ok=", "ms.map(m=>{const L=DB.ph.filter(p=>p.mo==m&&isBr(p)),ok=")
rep("const staleN=()=>DB.ph.filter(p=>revSt(p)=='old').length;", "const staleN=()=>DB.ph.filter(p=>isBr(p)&&revSt(p)=='old').length;")
rep("function mcloseHtml(){const m=V.mo||MN(),L=DB.ph.filter(p=>p.mo==m).sort(pSort)", "function mcloseHtml(){const m=V.mo||MN(),L=DB.ph.filter(p=>p.mo==m&&isBr(p)).sort(pSort)")
rep("const PF=()=>DB.ph.filter(p=>!V.q||!V.q.mo||p.mo==V.q.mo);", "const PF=()=>DB.ph.filter(p=>isBr(p)&&(!V.q||!V.q.mo||p.mo==V.q.mo));")
rep("L=DB.ph.filter(p=>p.mo==m).sort(pSort),X=V.mrx||{}", "L=DB.ph.filter(p=>p.mo==m&&isBr(p)).sort(pSort),X=V.mrx||{}")
rep("L=DB.ph.filter(p=>p.mo==m&&!X[p.id]).sort(pSort)", "L=DB.ph.filter(p=>p.mo==m&&isBr(p)&&!X[p.id]).sort(pSort)")
# pharmacies tab: maintenance list under the branding list of each month
rep("const a=g[k],d=a.filter(p=>p.st=='مكتملة').length", "const a0=g[k],a=a0.filter(isBr),mm=a0.filter(isMnt),d=a.filter(p=>p.st=='مكتملة').length")
rep("<span>${k==cur?'الشهر الحالي':'شهر'} ${k}</span><i>${a.length}</i></summary>", "<span>${k==cur?'الشهر الحالي':'شهر'} ${k}</span><i>${a.length}${mm.length?' + 🔧'+mm.length:''}</i></summary>")
rep("<button class=\"pr\" data-rv=\"${k}\">مراجعة هذا الشهر</button></div>${a.map(pCard).join('')}</div></details>`",
    "<button class=\"pr\" data-rv=\"${k}\">مراجعة هذا الشهر</button></div>${a.map(pCard).join('')}${mm.length?`<details class=\"mntg\"${t||q.mo?' open':''}><summary>🔧 صيدليات الصيانة (${mm.length}) <small>· مكتملة ${mm.filter(p=>p.st=='مكتملة').length}</small></summary>${mm.map(pCard).join('')}</details>`:''}</div></details>`")
# keep the maintenance log in step on every save, and fix data once
rep("const sv=()=>{try{", "const sv=()=>{try{try{mntAuto()}catch(e){console.error(e)}")
rep("function render(){const a=$('#app');EDTD=false;", "function render(){const a=$('#app');EDTD=false;try{if(DB&&DB.ph&&DB.ph.some(p=>!p.m22))v22Fix()}catch(e){console.error(e)}")

# ---- management totals per material
rep("+(NOTOT.includes(g.ty)?'':`<tr class=\"tot\"><td colspan=\"3\">إجمالي ${esc(g.ty)}</td><td>${gTot(g.ty,vis)}</td><td class=\"act\"></td></tr>`)}).join('');",
    "+(NOTOT.includes(g.ty)?'':matTot(g.ty,vis))}).join('');")
rep("const base=grpTy(ordinary).map(g=>{const vis=g.a.filter(x=>!hidden.includes(x._idx));", "const base=grpTy(ordinary).map(g=>{const vis=byMat(g.a.filter(x=>!hidden.includes(x._idx)));")
rep("grpTy(L).map(g=>g.a.map(icard).join('')+(NOTOT.includes(g.ty)?'':`<div class=\"icard ttl\"><div class=\"h\"><span>إجمالي ${esc(g.ty)}</span><i class=\"q\">${g.ty=='End gandola'?egTot(g.a):gTot(g.ty,g.a)}</i></div></div>`))",
    "grpTy(L).map(g=>{const a=g.ty=='End gandola'?g.a:byMat(g.a);return a.map(icard).join('')+(NOTOT.includes(g.ty)?'':g.ty=='End gandola'?`<div class=\"icard ttl\"><div class=\"h\"><span>إجمالي ${esc(g.ty)}</span><i class=\"q\">${egTot(g.a)}</i></div></div>`:matSplit(g.ty,a).map(([t,v])=>`<div class=\"icard ttl\"><div class=\"h\"><span>إجمالي ${esc(t)}</span><i class=\"q\">${v}</i></div></div>`).join(''))})")

JS = r"""// ---------- v2.2: maintenance pharmacies, totals per material, one-time data fixes ----------
const isMnt=p=>!!p&&p.mod=='صيانة',isBr=p=>!isMnt(p);
const MWD='تغيير',MWL=()=>[MWD].concat(MW.filter(x=>x!=MWD));
// group rows of one type by material (first appearance order) and total each material apart
function byMat(v){const ms=[];v.forEach(x=>{if(!ms.includes(x.mat||''))ms.push(x.mat||'')});return v.slice().sort((a,b)=>ms.indexOf(a.mat||'')-ms.indexOf(b.mat||''))}
function matSplit(ty,v){const ms=[...new Set(v.map(x=>x.mat||''))];if(ms.length<2||ty=='Wall Sticker')return [[ty,gTot(ty,v)]];return ms.map(m=>[ty+' — '+(m||'—'),gTot(ty,v.filter(x=>(x.mat||'')==m))])}
const matTot=(ty,v)=>matSplit(ty,v).map(([t,x])=>`<tr class="tot"><td colspan="3">إجمالي ${esc(t)}</td><td>${x}</td><td class="act"></td></tr>`).join('');
// executed items of a completed maintenance pharmacy -> lines of the maintenance log (kept in step, no duplicates)
function mntLines(p){const o=[];if(!isMnt(p)||p.st!='مكتملة')return o;rcvIds(p);const dt=p.de||TD();
 TY(p).forEach(t=>{if(t.auto)return;(p.rows[t.id]||[]).forEach(r=>{let z='';try{z=t.z(r,p.sh)}catch(e){}const b={dt,ph:String(p.no),ct:p.name||p.ct||'',work:r.mw||MWD,note:r.nt||''};
  const x=+r.x||0;if(x>0&&!(t.id=='eg'&&egAO(r,p.sh)))o.push(Object.assign({},b,{ad:t.n,det:z,sz:(typeof szOf=='function'?szOf(z):'')||'',q:x,src:'ph:'+p.id+':'+r._i}));
  if(t.id=='eg'&&egSub(r,p.sh))SDS.forEach(([sd,n])=>{const v=pkv(r,'x',sd);if(v>0)o.push(Object.assign({},b,{ad:'Side Acrylic Pocket',det:(r.nm||'')+' · '+n,sz:'',q:v,src:'ph:'+p.id+':'+r._i+':'+sd}))})})});return o}
function mntSync(p){if(!p||uStoreRO()||!uEditP(p))return 0;const M=MU(),pre='ph:'+p.id+':',L=mntLines(p),old=M.items.filter(x=>String(x.src||'').startsWith(pre)),keep=new Set(),F=['dt','ph','ct','work','ad','det','sz','q','note'];let ch=0;
 L.forEach(n=>{let e=old.find(x=>x.src==n.src);if(e){if(F.some(k=>String(e[k])!==String(n[k]))){F.forEach(k=>e[k]=n[k]);e.at=nowIso();ch++}}else{e=Object.assign({id:Date.now()+Math.floor(Math.random()*1e6),imb:[],ima:[],at:nowIso()},n);M.items.push(e);ch++}keep.add(e.src)});
 old.forEach(e=>{if(!keep.has(e.src)){M.items.splice(M.items.indexOf(e),1);ch++}});return {ch,n:L.length,was:old.length}}
let MNTN={};
function mntAuto(){const p=V&&V.p?DB.ph.find(x=>x.id==V.p):null;if(!p)return;const pre='ph:'+p.id+':';if(!isMnt(p)&&!((DB.mnt||{}).items||[]).some(x=>String(x.src||'').startsWith(pre)))return;const r=mntSync(p);if(r&&r.ch){const k=p.id+':'+r.n;if(MNTN[p.id]!==k){MNTN[p.id]=k;setTimeout(()=>toastT(r.n?'🔧 سجل الصيانة: '+r.n+' سطر للصيدلية '+p.no+' (نوع العمل من كل بند)':'🔧 اتشالت سطور الصيدلية '+p.no+' من سجل الصيانة'),60)}}}
// one time: maintenance pharmacies without the automatic boards, Old Turkish Floor Header one size, side acrylic wall size, log in step
const isABD0=r=>r&&ABD().some(a=>a.it==r.it)&&+r.q===1&&r.stt=='تصنيع وتركيب'&&!r.r&&!r.x&&!r.nt&&!r.xi;
function v22Fix(){let ch=0;const S=x=>(!x.rsh||x.rsh=='زي الصيدلية')?x._s:SH.indexOf(x.rsh);
 DB.ph.forEach(p=>{if(p.m22)return;const R=p.rows||{};
  if(isMnt(p)&&Array.isArray(R.ab)&&R.ab.length&&R.ab.every(isABD0)){R.ab=[];ch++}
  (R.fh||[]).forEach(r=>{r._s=p.sh;if(S(r)===2&&r.sz&&r.sz!='قياسي'){r.sz='قياسي';ch++}delete r._s});
  (R.saw||[]).forEach(r=>{if(r.sz=='40×125'){r.sz='215×40';ch++}});
  p.m22=1;ch++;if(isMnt(p))mntSync(p)});
 const pids=new Set(DB.ph.map(p=>String(p.id))),M=DB.mnt&&DB.mnt.items;if(M)for(let i=M.length-1;i>=0;i--){const m=String(M[i].src||'').match(/^ph:([^:]+):/);if(m&&!pids.has(m[1])){M.splice(i,1);ch++}}
 if(ch)svq()}
function whFix22(){const L=DB.wh;L.forEach(x=>{if(x.m22)return;if(x.ty=='Floor Header'&&x.sh==2&&['17×100','11.5×76'].includes(String(x.size)))x.size='17.5×100';if(x.ty=='Side Acrylic Shelves Wall'&&String(x.size)=='40×125')x.size='215×40';x.m22=1});
 for(let i=L.length-1;i>=0;i--){const k=whKey(L[i]),j=L.findIndex(y=>y!==L[i]&&whKey(y)==k);if(j>=0&&j<i){L[j].qty=wq(+L[j].qty+(+L[i].qty||0));L.splice(i,1)}}}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
CSS = "\n.mntg{margin-top:10px;border:1px dashed var(--ln);border-radius:var(--rad-sm);padding:8px;background:var(--c2)}.mntg>summary{font-weight:700}.mntg .pcard{transform:scale(.97)}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
rep("VER='v2.1'", "VER='v2.2'")
rep(" changelog:[{version:'v2.1',", " changelog:[{version:'v2.2',date:'2026-11-02',changes:['Maintenance pharmacies (نوع التعديل صيانة): own closed list under each month in the pharmacies tab; not in the month board, review, monthly management reports; no automatic Acrylic boards; item field نوع العمل (default تغيير); when completed, executed items go to the maintenance log automatically and stay in step','Custody: car plate filled for وقود and سيارة','Old Turkish: Floor Header one size 17.5×100 (Health too), Wall Header 17.5×100 only; material default ستيكر + تصنيع أكريليك with the choice تركيب ستيكر فقط','Side Acrylic Shelves Wall sizes 215×35 / 215×40 / 215×45 (40×125 fixed to 215×40)','Management report and review: totals per material when a type has more than one']},{version:'v2.1',")
EN = {'نوع العمل (الصيانة)':'Work type (maintenance)','🔧 صيدليات الصيانة':'🔧 Maintenance pharmacies','لوحة العربية (للوقود والسيارة)':'Car plate (fuel and car)'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')

// ---------- v2.2: maintenance pharmacies, totals per material, one-time data fixes ----------
const isMnt=p=>!!p&&p.mod=='صيانة',isBr=p=>!isMnt(p);
const MWD='تغيير',MWL=()=>[MWD].concat(MW.filter(x=>x!=MWD));
// group rows of one type by material (first appearance order) and total each material apart
function byMat(v){const ms=[];v.forEach(x=>{if(!ms.includes(x.mat||''))ms.push(x.mat||'')});return v.slice().sort((a,b)=>ms.indexOf(a.mat||'')-ms.indexOf(b.mat||''))}
function matSplit(ty,v){const ms=[...new Set(v.map(x=>x.mat||''))];if(ms.length<2||ty=='Wall Sticker')return [[ty,gTot(ty,v)]];return ms.map(m=>[ty+' — '+(m||'—'),gTot(ty,v.filter(x=>(x.mat||'')==m))])}
const matTot=(ty,v)=>matSplit(ty,v).map(([t,x])=>`<tr class="tot"><td colspan="3">إجمالي ${esc(t)}</td><td>${x}</td><td class="act"></td></tr>`).join('');
// executed items of a completed maintenance pharmacy -> lines of the maintenance log (kept in step, no duplicates)
function mntLines(p){const o=[];if(!isMnt(p)||p.st!='مكتملة')return o;rcvIds(p);const dt=p.de||TD();
 TY(p).forEach(t=>{if(t.auto)return;(p.rows[t.id]||[]).forEach(r=>{let z='';try{z=t.z(r,p.sh)}catch(e){}const b={dt,ph:String(p.no),ct:p.name||p.ct||'',work:r.mw||MWD,note:r.nt||''};
  const x=+r.x||0;if(x>0&&!(t.id=='eg'&&egAO(r,p.sh)))o.push(Object.assign({},b,{ad:t.id=='fr'?frAd(r.kd):t.n,det:z,sz:(typeof szOf=='function'?szOf(z):'')||'',q:x,src:'ph:'+p.id+':'+r._i}));
  if(t.id=='eg'&&egSub(r,p.sh))SDS.forEach(([sd,n])=>{const v=pkv(r,'x',sd);if(v>0)o.push(Object.assign({},b,{ad:'Side Acrylic Pocket',det:(r.nm||'')+' · '+n,sz:'',q:v,src:'ph:'+p.id+':'+r._i+':'+sd}))})})});return o}
function mntSync(p){if(!p||uStoreRO()||!uEditP(p))return 0;const M=MU(),pre='ph:'+p.id+':',L=mntLines(p),old=M.items.filter(x=>String(x.src||'').startsWith(pre)),keep=new Set(),F=['dt','ph','ct','work','ad','det','sz','q','note'];let ch=0;
 L.forEach(n=>{let e=old.find(x=>x.src==n.src);if(e){if(F.some(k=>String(e[k])!==String(n[k]))){F.forEach(k=>e[k]=n[k]);e.at=nowIso();ch++}}else{e=Object.assign({id:Date.now()+Math.floor(Math.random()*1e6),imb:[],ima:[],at:nowIso()},n);M.items.push(e);ch++}keep.add(e.src)});
 old.forEach(e=>{if(!keep.has(e.src)){M.items.splice(M.items.indexOf(e),1);ch++}});return {ch,n:L.length,was:old.length}}
let MNTN={};
function mntAuto(){const p=V&&V.p?DB.ph.find(x=>x.id==V.p):null;if(!p)return;const pre='ph:'+p.id+':';if(!isMnt(p)&&!((DB.mnt||{}).items||[]).some(x=>String(x.src||'').startsWith(pre)))return;const r=mntSync(p);if(r&&r.ch){const k=p.id+':'+r.n;if(MNTN[p.id]!==k){MNTN[p.id]=k;setTimeout(()=>toastT(r.n?'🔧 سجل الصيانة: '+r.n+' سطر للصيدلية '+p.no+' (نوع العمل من كل بند)':'🔧 اتشالت سطور الصيدلية '+p.no+' من سجل الصيانة'),60)}}}
// one time: maintenance pharmacies without the automatic boards, Old Turkish Floor Header one size, side acrylic wall size, log in step
const isABD0=r=>r&&ABD0().some(a=>a.it==r.it)&&+r.q===1&&r.stt=='تصنيع وتركيب'&&!r.r&&!r.x&&!r.nt&&!r.xi;
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

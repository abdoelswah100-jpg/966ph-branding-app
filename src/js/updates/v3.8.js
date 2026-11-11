// ---------- v3.8: acrylic boards ----------
const abSig=a=>(a||[]).map(r=>[r.it,r.an||'',+r.q||0,r.stt||''].join('|')).sort().join('#');
const abUntouched=a=>(a||[]).every(r=>!r.r&&!r.x&&!r.nt&&!r.xi&&!r.wf);
// the modification type changed: boards still as the app put them follow the new type
function abModCh(p,a,b){if(!p||a==b)return 0;const R=p.rows=p.rows||{},cur=R.ab||[];if(!abUntouched(cur)||abSig(cur)!=abSig(ABD(a)))return 0;R.ab=ABD(b);if(!R.ab.length)delete R.ab;return 1}

// management report: one line for Fridge sticker and for Acrylic board A3 (the kinds / names are for the work, not the report)
function mgMerge(L){const o=[],m={};L.forEach(x=>{const n=x.ty=='Fridge sticker'?'Fridge sticker':String(x.n).startsWith(ABA3+' · ')?ABA3:x.n;if(n==x.n){o.push(x);return}const k=n+'|'+x.sz+'|'+x.mat+'|'+(x.st||'');if(!m[k]){m[k]=Object.assign({},x,{n,q:0,a:0,lm:0});o.push(m[k])}m[k].q+=x.q;m[k].a+=x.a||0;m[k].lm+=x.lm||0});return o}

// ---------- v3.8: one stock for items that do not depend on the shelf type ----------
function NOSHT(){const o=new Set();T.forEach(t=>{if(!NOSH.includes(t.id))return;if(t.id=='ga')GAP.forEach(([n])=>o.add(GAN+' - '+n));else o.add(t.n)});return o}
function whFix38(){const S=NOSHT(),W=DB.wh;let ch=0;W.forEach(x=>{if(x.m38)return;if(S.has(x.ty)&&x.sh!==-1){x.sh=-1;ch=1}x.m38=1});
 if(ch)for(let i=W.length-1;i>=0;i--){const k=whKey(W[i]),j=W.findIndex(y=>whKey(y)==k);if(j>=0&&j<i){W[j].qty=wq(+W[j].qty+(+W[i].qty||0));W.splice(i,1)}}}
// one time per pharmacy: transferred surplus keys, A3 rows split by name; maintenance fridge lines by kind
function v38Fix(){const S=NOSHT();
 DB.ph.forEach(p=>{if(p.m38)return;
  if(p.whT){const o={};Object.keys(p.whT).forEach(k=>{const e=p.whT[k];if(e&&S.has(e.ty)&&e.sh!==-1){const y=Object.assign({},e,{sh:-1}),k2=whKey(y);if(o[k2])o[k2].q=wq(+o[k2].q+(+y.q||0));else o[k2]=y}else if(o[k])o[k].q=wq(+o[k].q+(+e.q||0));else o[k]=e});p.whT=o}
  const R=p.rows||{};if(Array.isArray(R.ab)){const o=[];R.ab.forEach(r=>{const q=+r.q||0;if(r&&r.it==ABA3&&!r.an&&(q==5||q==6)){const rr=+r.r||0,xx=+r.x||0,wf=+r.wf||0;
    ABN.slice(0,q).forEach((n,i)=>{const y=Object.assign({},r,{an:n,q:1});if(r.r!=null)y.r=i<rr?1:0;if(r.x!=null)y.x=i<xx?1:0;if(r.wf!=null)y.wf=i<wf?1:0;if(i){delete y._i;delete y.nt;delete y.xi;delete y.xn}o.push(y)})}else o.push(r)});R.ab=o}
  p.m38=1});
 const M=DB.mnt&&DB.mnt.items;if(M&&!DB.mnt.m38){M.forEach(x=>{if(x.ad=='Fridge sticker'){const s=String(x.det||'')+' '+String(x.note||'');const k=/عصير/.test(s)?FRK[0]:/أدوية|ادوية|دواء/.test(s)?FRK[1]:'';if(k)x.ad=frAd(k)}});DB.mnt.m38=1}
 svq()}

// print only what is missing: End gandola parts after the stock (each part on its own)
function egNet(r,L,st,used,t,i,c,q){if(!L||!L.M.some(y=>y.ep))return q;const F={h:egFh(r),s:egFs(r),a:egFa(r)},left={};let any=0;
 L.M.forEach(y=>{if(!y.ep)return;const n=(L.ex||{})[y.ep]||0;if(n)st[whKey(y)]=wq((st[whKey(y)]||0)-n);left[y.ep]=Math.max(0,Math.round(F[y.ep]*q-egX(r,y.ep)-n+1e-9));if(left[y.ep])any=1});
 if(egExN(L.ex))used.push({tid:t.id,i,n:0,np:0,tx:egExT(L.ex),xw:egExXT(L),t:t.n,z:t.z(r,c.sh)});
 if(!any)return 0;r.eh=left.h||0;r.es=left.s||0;if(F.a>0)r.ea=left.a||0;return q}

// ---------- v3.8: End gandola part by part ----------
const EGPN={h:'هيدر',s:'سايد',a:'أكريليك سايد'};
const egExN=ex=>Object.values(ex||{}).reduce((a,n)=>a+(+n||0),0);
const egExT=ex=>Object.keys(ex||{}).filter(k=>ex[k]>0).map(k=>ex[k]+' '+EGPN[k]).join(' + ');
const whTxt=(L,t)=>[whTxt0(L,t),egExT(L&&L.ex)].filter(Boolean).join(' + ');
// what the stock gives for the gondolas it cannot make whole: each part on its own
function egEx(r,M,nm,qty){const o={},rem=Math.max(0,qn(r)-Math.max(+r.r||0,+r.wf||0)-nm);if(!rem)return o;
 M.forEach(y=>{if(!y.ep||!(y.f>0))return;const need=Math.max(0,Math.round(y.f*rem-egX(r,y.ep)+1e-9)),av=Math.floor(qty(y)-nm*y.f+1e-9),n=Math.min(need,Math.max(0,av));if(n>0)o[y.ep]=n});return o}
// the stock covers every part still needed
function egExAll(r,M,ex){const rem=Math.max(0,qn(r)-Math.max(+r.r||0,+r.wf||0));return M.filter(y=>y.ep&&y.f>0).every(y=>(ex[y.ep]||0)>=Math.max(0,Math.round(y.f*rem-egX(r,y.ep)+1e-9)))}
function egExXT(L){const o=new Set();(L.M||[]).forEach(y=>{const n=(L.ex||{})[y.ep];if(n>0)whCross(y,n).forEach(x=>o.add(x))});return o.size?` ⚠ هيتسحب من مخزن ${[...o].join(' و')} (نوع رفوف مختلف، نفس المقاس).`:''}
// parts received count; when every part of one gondola is in, it becomes a received gondola
function egNorm(r){const q=qn(r),F={h:egFh(r),s:egFs(r),a:egFa(r)},E=Object.keys(F).filter(k=>F[k]>0);let g=0;
 if(E.length)while((+r.r||0)<q&&E.every(k=>egX(r,k)+1e-9>=F[k])){E.forEach(k=>r['wx'+k]=egRd(egX(r,k)-F[k]));r.r=(+r.r||0)+1;r.wf=(+r.wf||0)+1;if(++g>999)break}
 ['h','s','a'].forEach(k=>{if((+r.r||0)>=q||!(egX(r,k)>0))delete r['wx'+k]})}
function egExTake(p,r,L,note){let n=0;Object.keys(L.ex||{}).forEach(ep=>{const y=L.M.find(z=>z.ep==ep),c=L.ex[ep];if(!y||!(c>0))return;const g=whTakeQ(y,c,'ph:'+p.no,(note||'')+' (جزء من الجندولة: '+EGPN[ep]+')');r['wx'+ep]=egRd(egX(r,ep)+g);n+=g});if(n)egNorm(r);return n}
// New Arrival gondola: 1 header + 2 sides (one Arabic, one English)
(t=>{if(!t)return;const z0=t.z;t.z=(r,s)=>{const v=z0(r,s);return /^New Arrival/.test(r&&r.nm||'')?v+' · (السايد: 1 عربي + 1 إنجليزي لكل جندولة)':v}})(T.find(x=>x.id=='eg'));


// ---------- v1.5 extras ----------
// print summary after the warehouse stock: what is still in stock is not printed again
function whNet(p){const c=JSON.parse(JSON.stringify(p)),st={},used=[];WU().forEach(x=>{const k=whKey(x);st[k]=(st[k]||0)+(+x.qty||0)});
 TY(c).forEach(t=>{const rs=c.rows[t.id];if(t.auto||!rs||!rs.length)return;c.rows[t.id]=rs.map((r,i)=>{const sub=t.id=='eg'&&egSub(r,c.sh),ao=sub&&egAO(r,c.sh);let q=ao?0:qn(r)-(+r.wf||0);const pp={};if(sub)SDS.forEach(([sd])=>pp[sd]=egN(r,c.sh,sd)-(+r['wfp'+sd]||0));
   const L=whRowPlan(t,r,c.sh,st);if(t.id=='eg'&&!ao)q=egNet(r,L,st,used,t,i,c,q);if(L&&(L.nm>0||L.np>0)){L.M.forEach(y=>st[whKey(y)]=wq((st[whKey(y)]||0)-L.nm*y.f));L.K.forEach(y=>{const n=(L.nps||{})[y.pk]||0;st[whKey(y)]=wq((st[whKey(y)]||0)-n);pp[y.pk]-=n});used.push({tid:t.id,i,n:L.nm,np:L.np,tx:whTxt(L,t),xw:whXT(t,r,c.sh,L.nm),t:t.n,z:t.z(r,c.sh)});q-=L.nm}
   if(sub){const pr=Math.max(0,pp.R||0),pl=Math.max(0,pp.L||0);if(q<=0&&!pr&&!pl)return null;if(q<=0){r.egp=EGPO[2];r.q=Math.max(1,qn(r));r.pR=pr;r.pL=pl;return r}if(!pr&&!pl){r.egp=EGPO[1];r.q=q;return r}r.q=q;r.pR=pr;r.pL=pl;return r}
   if(q<=0)return null;if(r.q!=null)r.q=q;return r}).filter(Boolean)});
 const pre=TY(p).reduce((a,t)=>a+(p.rows[t.id]||[]).reduce((b,r)=>b+Math.min(qn(r),+r.wf||0)+(+r.wfpR||0)+(+r.wfpL||0)+(t.id=='eg'?egXs(r):0),0),0);return {p:c,used,pre}}
function sxBox(p,N){if(!WU().length&&!N.pre)return '';const on=!!V.sxw;
 return `<div class="sxw np"><label class="chk"><input type="checkbox" id="sxw"${on?' checked':''}> اطبع الناقص بس (اخصم الموجود في المخزن)</label>${on?`${N.used.length?`<div class="ph"><small>📦 موجود في المخزن ومش هيتطبع:</small>${N.used.map(u=>`<small>• ${esc(u.t)} · ${esc(u.z)} — <b>${esc(u.tx)}</b>${u.xw?`<b class="whxw">${esc(u.xw)}</b>`:''}</small>`).join('')}<button class="pr" data-sxpull="1">${ic('box')}اسحبهم من المخزن للصيدلية</button></div>`:'<small>مفيش حاجة من بنود الصيدلية دي موجودة في المخزن.</small>'}${N.pre?`<small>✓ ${N.pre} قطعة اتسحبت من المخزن قبل كده ومش هتتطبع.</small>`:''}`:''}</div>`}
function sxPull(p){const N=whNet(p);let n=0;N.used.forEach(u=>{const t=T.find(x=>x.id==u.tid),r=(p.rows[u.tid]||[])[u.i];if(!t||!r)return;const L=whRowPlan(t,r,p.sh);if(L)n+=whTake(p,t,r,L,'سحب لملخص الطباعة')});sv();snd('ok');render();toastT(`✓ اتسحب ${n} من المخزن واتحسبوا مستلمين`)}
// custody: alert when the remaining is below the limit (default 2000, 0 = off)
const cAl=()=>{const v=CU().cfg.al;return v===undefined||v===''||v===null?2000:+v||0};
function cAlert(){if(!DB||!DB.cust)return '';const C=CU(),ks=Object.keys(C.m).sort();if(!ks.length)return '';const k=ks[ks.length-1],M=C.m[k];if(!M||!(M.items||[]).length)return '';const r=cRem(M),a=cAl();return a&&r<a?{k,r,a}:''}
const cAlHtml=(home)=>{const x=cAlert();return x?`<div class="alr cal"><small>⚠ رصيد العهدة المتبقي <b>${f2(x.r)}</b> أقل من ${f2(x.a)} (شهر ${cMoLab(x.k)}). اطلب تعزيز العهدة.</small>${home?'<button data-tab="cust">العهدة</button>':''}</div>`:''};
// before / after photos: share them (WhatsApp)
async function phoShare(p,w){w=w&&w!='1'?w:'ba';const F=[];for(const[sl,t] of [['b','قبل'],['a','بعد']].filter(x=>w.includes(x[0])))for(const[i,x] of phoList(p,sl).entries()){const b=await idbGet(phoKey(p.id,sl,x.k));if(b)F.push({b:await stampBlob(b,stampTxt(p,x)),n:`صيدلية ${p.no} - ${t} ${i+1}.jpg`})}
 if(!F.length)return alert('مفيش صور على الجهاز ده');const msg=`${PL(p)}${p.name?' ('+p.name+')':''} — ${w=='b'?'صور قبل التنفيذ':w=='a'?'صور بعد التنفيذ':'صور قبل وبعد التنفيذ'} (${F.length} صورة)`;try{navigator.clipboard&&navigator.clipboard.writeText(msg)}catch(e){}const tt=toast('جاري تجهيز الصور…');
 try{if(CAPN()&&CP('Share')&&CP('Filesystem')){const FS=CP('Filesystem'),U2=[];for(const f of F){const w=await FS.writeFile({path:f.n,data:await b64of(f.b),directory:'CACHE'});U2.push(w.uri)}tt.remove();await CP('Share').share({title:msg,text:msg,files:U2,dialogTitle:'صور صيدلية '+p.no}).catch(()=>{});return}
  const fl=F.map(f=>new File([f.b],f.n,{type:f.b.type||'image/jpeg'}));tt.remove();if(navigator.canShare&&navigator.canShare({files:fl})){await navigator.share({files:fl,title:msg,text:msg}).catch(()=>{});return}
  F.forEach(f=>dl(f.n,f.b,f.b.type||'image/jpeg'))}finally{tt.remove()}}
function x15Click(d,b){
 if(d.sxpull){const p=curP();if(p&&confirm('هيتخصم الموجود من المخزن ويتحسب مستلم في الصيدلية. تكمل؟'))sxPull(p);return 1}
 if(d.phshare){const p=curP();if(p)phoShare(p,d.phshare);return 1}
 return 0}
function x15Change(x){
 if(x.id=='cdz'){const q=curP();if(q){if(x.value=='قديم')q.dz='قديم';else delete q.dz;q.modAt=nowIso();sv();render()}return 1}
 if(x.id=='sxw'){V.sxw=x.checked;render();return 1}
 return 0}
document.addEventListener('input',e=>{const x=e.target;if(x.id=='mqf'){V.mqf=x.value;render();const i=$('#mqf');if(i){i.focus();i.setSelectionRange(i.value.length,i.value.length)}}});


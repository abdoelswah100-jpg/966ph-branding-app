// ---------- 2.6 (file n2.6.js) ----------
// 1) Acrylic boards total per material  2) decorative nails out of piece counts  3) file inputs reset + repeated pharmacies file warning
// 4) warehouse never below zero  5) 🔍 data check  6) 🚚 car load list  7) 📤 print request (Khobar)  8) 🧰 tools check
// 9) places: phone / WhatsApp / hours / order  10) 📞 contacts  11) menu order, grouped screens (chips)
// 12) settings the owner edits himself (tools, reasons, visit tracking, custody kinds, messages; types: acrylic boards, A3/A4 names,
//     default acrylic per modification, letter ratios, maintenance work types, fridge kinds)  13) sticker rolls deducted at execution
// No place / contact / pharmacy data in the code: they come from a «966-places» file or are typed in the app.
const NAIL='Decorative nail',TOOLS0=['كاتر','ميزان مياه','متر','شنطة','دريل','مسامير','مسامير ديكور','دبل تيب','قلم','بطارية وشاحن','مفك','سوبر جلو','غطاء مسمار أكريليك','مسامير ربط','مسامير حفر','تيب أبيض','تيب شفاف'];
const D26=()=>{const c=DB.cfg;c.c26=c.c26||{};return c.c26};
const TOOLS=()=>(D26().tools&&D26().tools.length?D26().tools:TOOLS0);
const lines=t=>String(t||'').split(/\n|،|,/).map(x=>x.trim()).filter(Boolean);
const B0={CXR:CXR.slice(),MW:MW.slice(),FRK:FRK.slice(),ABN:ABN.slice(),CK:CK.slice(),RATIO:JSON.parse(JSON.stringify(RATIO)),VZ:Object.assign({},VZ,{h0:9}),ABI:ABI.slice()};
const fill=(A,L)=>{A.length=0;L.forEach(x=>A.push(x))};
function cfg26(){try{const c=D26();fill(CXR,c.cxr&&c.cxr.length?c.cxr:B0.CXR);fill(MW,c.mw&&c.mw.length?c.mw:B0.MW);fill(FRK,c.frk&&c.frk.length?c.frk:B0.FRK);fill(ABN,c.abn&&c.abn.length?c.abn:B0.ABN);
 fill(CK,c.ck&&c.ck.length?c.ck:B0.CK);CK.forEach(k=>{if(!CKC[k])CKC[k]='EFEFEF'});Object.keys(RATIO).forEach(k=>{if(!(k in B0.RATIO))delete RATIO[k]});Object.assign(RATIO,JSON.parse(JSON.stringify(B0.RATIO)),c.ratio||{});
 Object.assign(VZ,B0.VZ,c.vz||{});const ax=c.abx||[];fill(ABI,B0.ABI.concat(ax.map(x=>x.it).filter(it=>!B0.ABI.includes(it))));ax.forEach(x=>{SZD['abs.'+x.it]=(x.sz||'—')+'|'+(x.mat||'أكريليك')});
 if(!RLK.includes('سي ثرو'))RLK.splice(Math.max(0,RLK.indexOf('أخرى')),0,'سي ثرو')}catch(e){console.warn('cfg26',e)}}
(function(){const t=T.find(x=>x.id=='fr');if(t){const f=t.f.find(y=>y.k=='kd');if(f)f.o=()=>FRK.slice()}})();
// ---- 1) Acrylic boards total per material
const matSum=v=>{const m={};v.forEach(x=>{const k=x.mat||'—';m[k]=(m[k]||0)+(+x.q||0)});return Object.keys(m).map(k=>`${esc(k)} ${m[k]}${k=='مسمار'?'':' قطعة'}`).join(' · ')};
abTbl=function(L,h){const v=L.filter(x=>!h.includes(x._idx));if(!v.length)return '';return `<h3>Acrylic boards</h3><div class="sc"><table><tr><th>البند</th><th>المقاس</th><th>الخامة</th><th>الحالة</th><th>العدد</th><th class="act">إجراء</th></tr>${v.map(x=>`<tr><td>${esc(x.n)}</td><td>${esc(x.sz)}</td><td>${esc(x.mat)}</td><td${x.st=='تصنيع + تركيب'?' style="background:#FAD4D4;font-weight:700"':''}>${esc(x.st)}</td><td>${x.q}</td>${rdelB(x)}</tr>`).join('')}<tr class="tot"><td colspan="4">إجمالي Acrylic boards</td><td>${matSum(v)}</td><td class="act"></td></tr></table></div>`};
// ---- 2) nails out of piece counts
const noNail=p=>p&&p.rows&&(p.rows.ab||[]).some(r=>r&&r.it==NAIL)?Object.assign({},p,{rows:Object.assign({},p.rows,{ab:p.rows.ab.filter(r=>r.it!=NAIL)})}):p;
const nailN=p=>((p&&p.rows&&p.rows.ab)||[]).filter(r=>r.it==NAIL).reduce((a,r)=>a+(+r.q||0),0);
const _tkProg26=tkProg;tkProg=function(p,k){return _tkProg26(noNail(p),k)};
const _mStats26=mStats;mStats=function(L){const o=_mStats26((L||[]).map(noNail));o.nails=(L||[]).reduce((a,p)=>a+nailN(p),0);return o};
// ---- 3) file inputs: same file twice + repeated pharmacies file
document.addEventListener('change',e=>{const x=e.target;if(x&&x.type=='file')setTimeout(()=>{try{x.value=''}catch(er){}},1500)},true);
const fHash=s=>{let h=0;for(let i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))|0;return String(h)};
const _phImpGo26=phImpGo;phImpGo=function(q,fn){const h=fHash(JSON.stringify(q.ph||[])),L=D26().pih=D26().pih||[],o=L.find(x=>x.h==h);
 if(o&&!confirm('⚠ الملف ده («'+(o.fn||'')+'») اتدخل قبل كده يوم '+fd(o.at)+'.\nتدخله تاني؟'))return;const w0=(piLog()[0]||{}).wi;const r=_phImpGo26.apply(this,arguments);
 if((piLog()[0]||{}).wi!=w0){L.unshift({h,fn:fn||'',at:nowIso()});D26().pih=L.slice(0,30);svq()}return r};
// ---- 4) warehouse never below zero
const _whAdd26=whAdd;whAdd=function(o,qty,typ,src,note){const x=_whAdd26.apply(this,arguments);if(x&&+x.qty<0){const s=wq(-x.qty);x.qty=0;whLog('adj',x,s,'fix','⚠ الرصيد ما كفّاش — ناقص '+s+' (اتسجل صفر)');try{toastT('⚠ «'+x.ty+(x.nm?' · '+x.nm:'')+'» الرصيد ما كفّاش — ناقص '+s)}catch(e){}}return x};
function whFix26(){if(D26().neg||uStoreRO())return;const L=WU().filter(x=>+x.qty<0);L.forEach(x=>{const s=wq(-x.qty);x.qty=0;whLog('adj',x,s,'fix','تصحيح 2.6: الرصيد ما ينزلش تحت الصفر (كان −'+s+')')});D26().neg=1;if(L.length)sv()}
// ---- 13) sticker rolls (Wall Sticker تخطيط / سي ثرو) deducted at execution
const rlK=r=>r&&r.kd=='ثلجي'?{nm:'ثلجي شفاف',sec:''}:r&&r.kd=='تخطيط'?{nm:'تخطيط',sec:r.sec||''}:r&&r.kd=='سي ثرو'?{nm:'سي ثرو',sec:''}:null;
const rlKs=k=>k.nm+(k.sec?' '+k.sec:'');
const rlLen=r=>{const h=+r.h||0,w=+r.w||0;if(!h||!w)return 0;const op=[];if(w<=100)op.push(h);if(h<=100)op.push(w);return op.length?Math.min(...op):h*w/100};
function rlMeters(p,k){const o={};((p&&p.rows&&p.rows.ws)||[]).forEach(r=>{const y=rlK(r);if(!y)return;const n=k=='q'?(+r.q||0):k=='left'?(r.cx?0:Math.max(0,(+r.q||0)-(+r.x||0))):(+r.x||0);if(!n)return;const s=rlKs(y);o[s]=o[s]||{k:y,m:0};o[s].m=wq(o[s].m+rlLen(r)*n/100)});return o}
const rlItems=k=>WU().filter(x=>x.ty==RLTY&&x.nm==k.nm&&String(x.sec||'')==String(k.sec||''));
const rlStockOf=k=>wq(rlItems(k).reduce((a,x)=>a+(+x.qty||0),0));
function rlTake(p,k,m){let left=m;rlItems(k).forEach(x=>{if(left<=1e-9||+x.qty<=0)return;const t=Math.min(left,+x.qty);whAdd(x,-t,'out','ph:'+p.no,'رول '+rlKs(k)+' — Wall Sticker (متنفذ)');left=wq(left-t)});return wq(m-left)}
function rlAuto(p){if(!p||uStoreRO()||!uEditP(p))return;const X=rlMeters(p,'x');if(!p.m26r){p.rlx={};Object.keys(X).forEach(s=>p.rlx[s]=X[s].m);p.m26r=1;return}p.rlx=p.rlx||{};
 Object.keys(X).concat(Object.keys(p.rlx)).filter((s,i,a)=>a.indexOf(s)==i).forEach(s=>{const need=X[s]?X[s].m:0,done=+p.rlx[s]||0,d=wq(need-done);if(!d)return;
  const k=X[s]?X[s].k:/^سي ثرو/.test(s)?{nm:'سي ثرو',sec:''}:/^ثلجي/.test(s)?{nm:'ثلجي شفاف',sec:''}:{nm:'تخطيط',sec:s.replace(/^تخطيط ?/,'')};
  if(d<0){const it=rlItems(k)[0]||{sh:-1,ty:RLTY,nm:k.nm,sec:k.sec,mat:'',size:'عرض 1 م'};whAdd(it,-d,'in','ph:'+p.no,'رول '+s+' — تصحيح (المتنفذ قل)');p.rlx[s]=need;return}
  const t=rlTake(p,k,d);if(t)p.rlx[s]=wq(done+t)})}
const rlOwed=p=>{const X=rlMeters(p,'x'),o=[];Object.keys(X).forEach(s=>{const d=wq(X[s].m-(+((p.rlx||{})[s])||0));if(p.m26r&&d>0)o.push(s+' '+d+' م')});return o};
function rlBox26(p){const N=rlMeters(p,'left'),ks=Object.keys(N);if(!ks.length)return '';const R=rlRes(p);
 const rows=ks.map(s=>{const st=rlStockOf(N[s].k),rs=R[s]||0,av=wq(st-rs),need=N[s].m;return{s,need,st,rs,ok:av>=need-1e-9,miss:wq(need-Math.max(0,av))}});const bad=rows.filter(x=>!x.ok);
 return `<details class="rlx26${bad.length?' bad':''}" data-id="rl_${p.id}"${V.op['rl_'+p.id]?' open':''}><summary>🧻 الرولات: ${bad.length?'⚠ ناقص: '+bad.map(x=>esc(x.s)+' '+x.miss+' م').join(' · '):'✅ كله يكفي'}</summary><div class="sc"><table class="ctab"><tr><th>الرول</th><th>المحتاج</th><th>في المخزن</th><th>محجوز</th><th></th></tr>${rows.map(x=>`<tr><td>${esc(x.s)}</td><td>${x.need} م</td><td>${x.st} م</td><td>${x.rs?x.rs+' م':'—'}</td><td>${x.ok?'✅':'⚠ '+x.miss}</td></tr>`).join('')}</table></div><small class="hint">المحتاج = اللي لسه ما اتنفذش (الجنب الصغير × العدد على رول عرضه 1 م). المحجوز = اللي صيدليات تانية لسه ما خلصتهوش محتاجاه. الرول بيتخصم لوحده لما البند يتعلّم متنفذ.</small></details>`}
function rlRes(p){const o={};DB.ph.forEach(q=>{if(q===p||q.st=='مكتملة')return;const N=rlMeters(q,'left');Object.keys(N).forEach(s=>o[s]=wq((o[s]||0)+N[s].m))});return o}
function rlShort(){const need={},keys={};DB.ph.forEach(q=>{if(q.st=='مكتملة')return;const N=rlMeters(q,'left');Object.keys(N).forEach(s=>{need[s]=wq((need[s]||0)+N[s].m);keys[s]=N[s].k})});
 return Object.keys(need).map(s=>({s,need:need[s],st:rlStockOf(keys[s])})).filter(x=>x.need>x.st+1e-9).map(x=>Object.assign(x,{miss:wq(x.need-x.st)}))}
const _capAuto26=capAuto;capAuto=function(){const r=_capAuto26.apply(this,arguments);try{const p=V&&V.p?DB.ph.find(x=>x.id==V.p):null;if(p)rlAuto(p);DB.ph.forEach(q=>{if(q!==p&&q.m26r&&rlOwed(q).length)rlAuto(q)})}catch(e){console.warn('rl',e)}return r};
function rlFix26(){if(D26().rl)return;DB.ph.forEach(p=>{if(!p.m26r){const X=rlMeters(p,'x');p.rlx={};Object.keys(X).forEach(s=>p.rlx[s]=X[s].m);p.m26r=1}});D26().rl=1}
// ---- 8) tools check
let TLS=null;function tlOpen(pid,next){const p=DB.ph.find(x=>x.id==pid)||HOLDL().find(x=>x.id==pid);TLS={pid,next,ok:{}};tlDraw()}
function tlDraw(){cShClose();const p=DB.ph.find(x=>x.id==TLS.pid),L=TOOLS(),n=L.filter((x,i)=>TLS.ok[i]).length,el=document.createElement('div');el.className='csh';
 el.innerHTML=`<div class="cshb"><b>🧰 راجع أدواتك قبل ما تمشي${p?' — صيدلية '+esc(p.no):''}</b><small class="hint">علّم على اللي معاك (${n} من ${L.length}).</small><div class="tlg">${L.map((x,i)=>`<button class="${TLS.ok[i]?'pr':''}" data-tlt="${i}">${TLS.ok[i]?'✓ ':''}${esc(x)}</button>`).join('')}</div>
 <div class="cshr"><button class="pr" data-tlok="1">✓ كله معايا</button><button data-tlno="1">بعدين</button></div></div>`;document.body.appendChild(el)}
function tlDone(ok){const p=DB.ph.find(x=>x.id==TLS.pid),nx=TLS.next;if(ok&&p){p.tlk=TD();svq()}cShClose();TLS=null;if(nx)nx()}
const _whOffer26=whOffer;whOffer=function(p,auto){if(p&&p.st=='مكتملة'&&p.tlk!=TD()&&!(TLS&&TLS.pid==p.id)&&!(CPS&&CPS.ok==p.id)){const a=auto;tlOpen(p.id,()=>{p.tlk=p.tlk||'_';_whOffer26.call(this,p,a);if(p.tlk=='_')delete p.tlk});return}return _whOffer26.apply(this,arguments)};
const _vOn26=vOn;vOn=function(loc){const S0=Object.assign({},DB.cfg.vst||{}),pre=Object.keys(S0).filter(id=>S0[id]&&S0[id].arr);const r=_vOn26.apply(this,arguments);
 try{const S=DB.cfg.vst||{};pre.forEach(id=>{if(S[id])return;const p=DB.ph.find(x=>String(x.id)==String(id));if(p&&p.tlk!=TD())ntfNowSend('🧰 راجع أدواتك — صيدلية '+p.no,TOOLS().join('، '),{pid:p.id})})}catch(e){}return r};
// ---- 5) data check
function chkList(){const o=[],add=(g,t,go,x)=>o.push({g,t,go,x});
 WU().filter(x=>+x.qty<0).forEach(x=>add('المخزن','رصيد بالسالب: '+x.ty+(x.nm?' · '+x.nm:'')+' '+(x.size||'')+' = '+x.qty,'wh'));
 rlShort().forEach(x=>add('الرولات','رول '+x.s+': المحتاج '+x.need+' م والمخزن '+x.st+' م — ناقص '+x.miss+' م','wh'));
 if(capStock()<0)add('المخزن',CPNM+' رصيده سالب','wh');
 DB.ph.forEach(p=>{const L=PL(p);
  ckRows(p).forEach(x=>{if((+x.r.x||0)>(+x.r.r||0))add('متنفذ أكتر من المستلم',L+' · '+x.t.n+' · '+x.t.z(x.r,p.sh)+' (متنفذ '+x.r.x+' / مستلم '+(+x.r.r||0)+')',p.id)});
  if(p.st!='مكتملة'){const t=tkProg(p,'x');if(t.n&&t.d>=t.n)add('كل البنود اتنفذت ولسه مش مكتملة',L+' · '+p.st,p.id)}
  if(p.st=='مكتملة'&&whPlan(p).some(x=>x.dl))add('فائض ما اترحّلش للمخزن',L,p.id);
  try{if(alerts(p).length)add('تنبيهات في البنود',L+' · '+alerts(p).length+' تنبيه',p.id)}catch(e){}
  if(capOwed(p))add('غطاء مسمار اتركب من غير خصم',L+' · '+capOwed(p),p.id);
  const ro=rlOwed(p);if(ro.length)add('رول اتنفذ من غير خصم',L+' · '+ro.join('، '),p.id);
  if(p.st!='مكتملة'){if(!locC(p))add('من غير موقع',L,p.id);if(isBr(p)&&(!p.ds||!p.de))add('من غير تاريخ بدء / انتهاء',L,p.id);if(/مؤقت/.test(p.rn||''))add('نوع رفوف مؤقت',L+' · '+(SH[p.sh]||''),p.id)}});
 return o}
const chkN=()=>{try{return chkList().length}catch(e){return 0}};
function chkHtml(){const L=chkList(),G={};L.forEach(x=>(G[x.g]=G[x.g]||[]).push(x));const H=HOLDL().length;
 let h=`<div class="wcard"><h2>🔍 فحص البيانات</h2><p class="sub">${L.length?L.length+' حاجة محتاجة مراجعة. دوس على أي سطر يوديك مكانه.':'✅ كله تمام — مفيش حاجة محتاجة مراجعة.'}${H?' · ⏸ '+H+' صيدلية تحت الانتظار (مش محسوبين)':''}</p></div>`;
 Object.keys(G).forEach(g=>{h+=`<details class="wcard" data-id="ck_${g}"${V.op['ck_'+g]!==false?' open':''}><summary><b>${esc(g)}</b><i>${G[g].length}</i></summary>${G[g].map(x=>`<div class="rw"><span>${esc(x.t)}</span><div class="bt"><button ${x.go=='wh'?'data-mgo="wh"':'data-go="'+x.go+'"'}>افتح ›</button></div></div>`).join('')}</details>`});return h}
// ---- 6) car load list
const addD=(d,n)=>{const x=new Date(d+'T12:00:00');x.setDate(x.getDate()+n);return x.toISOString().slice(0,10)};
function ldPh(d){return DB.ph.filter(p=>p.st!='مكتملة'&&p.ds&&p.de&&p.ds<=d&&d<=p.de).sort(pSort)}
function ldData(d){const st={};WU().forEach(x=>{const k=x.id+'|'+whKey0(x);st[k]=(st[k]||0)+(+x.qty||0)});const take=(y,n)=>{const k0=whKey0(y);let left=n;Object.keys(st).forEach(k=>{if(left<=1e-9||k.split('|').slice(1).join('|')!=k0)return;const u=Math.min(left,st[k]);st[k]-=u;left-=u})};
 return ldPh(d).map(p=>{const R=[];prepRows(p).forEach(x=>{const r=x.r,need=r.cx?0:Math.max(0,qn(r)-(+r.r||0));if(!need)return;const P2=(whParts(x.t,r,p.sh)||[]).filter(y=>!y.pk&&y.f>0),z=x.t.z(r,x.s);if(!P2.length){R.push({t:x.t,z,lab:'',need,have:0});return}
  P2.forEach(y=>{const have=Math.min(need,Math.floor((whStQ(st,y)+1e-9)/y.f));if(have)take(y,have*y.f);R.push({t:x.t,z,lab:P2.length>1?y.ty+(y.nm?' · '+y.nm:''):'',sh:y.sh,need,have})})});return{p,R,need:R.reduce((a,x)=>a+x.need,0),have:R.reduce((a,x)=>a+x.have,0)}})}
function ldHtml(){const d=V.ld||addD(TD(),1),D=ldData(d),H=D.reduce((a,x)=>a+x.have,0),N=D.reduce((a,x)=>a+x.need,0);
 let h=`<div class="wcard"><h2>🚚 قايمة تحميل العربية</h2><p class="sub">الصيدليات اللي تاريخ شغلها فيه اليوم ده (ولسه مش مكتملة): اللي تاخده من المخزن بنفس المقاس، واللي ناقص.</p><label>اليوم<input type="date" id="ldd" value="${d}"></label>
 <div class="c2"><div class="sumb"><b>${H}</b><small>تاخده من المخزن</small></div><div class="sumb"><b>${N-H}</b><small>ناقص</small></div></div>
 <div class="tt">${H?`<button class="pr" data-ldgo="all">📦 اتحمّلوا كلهم (${H})</button>`:''}<button data-ldwa="1">${ic('share')}نص واتساب</button></div></div>`;
 if(!D.length)return h+'<p class="em">مفيش صيدليات في اليوم ده (اتأكد من تواريخ البدء والانتهاء).</p>';
 D.forEach(o=>{h+=`<details class="wcard" data-id="ld_${o.p.id}"${V.op['ld_'+o.p.id]!==false?' open':''}><summary><b>${PL(o.p)}</b><small>من المخزن ${o.have} · ناقص ${o.need-o.have}</small></summary>${o.R.length?`<div class="sc"><table class="ctab"><tr><th>البند</th><th>فاضل</th><th>من المخزن</th><th>ناقص</th></tr>${o.R.map(x=>`<tr><td><b>${esc(x.t.n)}</b>${x.lab?' <small>'+esc(x.lab)+'</small>':''}<br><small>${esc(x.z)}</small></td><td>${x.need}</td><td class="${x.have?'c-rem':''}">${x.have||'—'}</td><td class="${x.need>x.have?'c-exp':''}"><b>${x.need-x.have||'✓'}</b></td></tr>`).join('')}</table></div>`:'<p class="em">كل اللي محتاجاه اتستلم.</p>'}${o.have?`<div class="tt"><button data-ldgo="${o.p.id}">📦 اتحمّلوا (${o.have})</button></div>`:''}</details>`});return h}
function ldGo(w){const d=V.ld||addD(TD(),1),P=w=='all'?ldPh(d):ldPh(d).filter(p=>String(p.id)==String(w)),D=ldData(d).filter(o=>P.includes(o.p)&&o.have),n=D.reduce((a,x)=>a+x.have,0);if(!n)return;
 if(!confirm(`📦 هيتسحب من المخزن ${n} قطعة لـ ${D.length} صيدلية (${D.map(o=>o.p.no).join('، ')}) ويتحسبوا مستلمين.\nفيه نقطة استرجاع قبلها. تكمل؟`))return;
 snap('قبل تحميل العربية — '+d);let m=0;D.forEach(o=>{const p=o.p,N=whNet(p);N.used.forEach(u=>{const t=T.find(x=>x.id==u.tid),r=(p.rows[u.tid]||[])[u.i];if(!t||!r)return;const L=whRowPlan(t,r,p.sh);if(L)m+=whTake(p,t,r,L,'تحميل العربية '+d)});p.modAt=nowIso()});
 sv();snd('ok');render();undoT('✓ اتسحب '+m+' من المخزن',()=>{const x=snaps()[0];if(x&&/تحميل العربية/.test(x.why)){DB=JSON.parse(x.db);norm();sv();render()}})}
function ldText(){const d=V.ld||addD(TD(),1),D=ldData(d),o=['🚚 *تحميل العربية* — '+d.split('-').reverse().join('-'),''];D.forEach(x=>{o.push('*صيدلية '+x.p.no+'*'+(x.p.name?' ('+x.p.name+')':''));x.R.forEach(y=>{if(y.have)o.push('📦 '+y.t.n+(y.lab?' · '+y.lab:'')+' · '+y.z+' ×'+y.have);if(y.need>y.have)o.push('⚠ ناقص: '+y.t.n+(y.lab?' · '+y.lab:'')+' · '+y.z+' ×'+(y.need-y.have))});o.push('')});return o.join('\n')}
// ---- 7) print request (Khobar)
const kbM=()=>D26().kbr=D26().kbr||{};
function kbData(mo){const D=avlData(mo),G={};D.forEach(o=>o.R.forEach(x=>{if(x.need<=x.have)return;const k=x.lab?x.lab+' · '+(x.size||''):x.t.n+' · '+x.z;G[k]=G[k]||{k,n:0,ph:[]};G[k].n+=x.need-x.have;if(!G[k].ph.includes(o.p.no))G[k].ph.push(o.p.no)}));return Object.values(G).sort((a,b)=>a.k.localeCompare(b.k))}
function kbHtml(){const ms=months().reverse(),mo=V.am2||V.pm||MN(),L=kbData(mo),M=kbM(),R=rlShort(),nw=L.filter(x=>!M[x.k]);
 return `<div class="wcard"><h2>📤 طلب طباعة الخبر</h2><p class="sub">الناقص اللي مش موجود في المخزن لصيدليات الشهر اللي لسه ما اكتملتش، متجمّع. «مشاركة» بتفتح واتساب وإنت تختار الجروب، وبعدها علّمهم «اتطلبوا» عشان ما يتطلبوش تاني.</p>
 <label>الشهر<select id="kbm">${ms.map(m=>`<option${m==mo?' selected':''}>${m}</option>`).join('')}</select></label>
 <div class="tt"><button class="pr" data-kbwa="new">${ic('share')}مشاركة الجديد (${nw.length})</button><button data-kbwa="all">مشاركة الكل (${L.length})</button>${nw.length?`<button data-kbok="1">✓ علّم الجديد «اتطلب»</button>`:''}</div></div>
 ${L.length?`<div class="wcard"><div class="sc"><table class="ctab"><tr><th>البند</th><th>ناقص</th><th>الصيدليات</th><th>الحالة</th></tr>${L.map(x=>`<tr><td>${esc(x.k)}</td><td><b>${x.n}</b></td><td><small>${x.ph.join('، ')}</small></td><td><small>${M[x.k]?'📤 اتطلب '+M[x.k].dt.split('-').reverse().join('-')+(M[x.k].n!=x.n?' ('+M[x.k].n+')':''):'—'}</small>${M[x.k]?` <button class="lnk" data-kbun="${esc(x.k)}">إلغاء</button>`:''}</td></tr>`).join('')}</table></div></div>`:'<p class="em">مفيش ناقص — كل اللي محتاجينه موجود في المخزن أو اتستلم.</p>'}
 ${R.length?`<div class="wcard alr"><b>🧻 رولات ناقصة</b>${R.map(x=>`<div><small>${esc(x.s)}: ناقص ${x.miss} م (محتاج ${x.need} · المخزن ${x.st})</small></div>`).join('')}</div>`:''}`}
function kbText(w){const mo=V.am2||V.pm||MN(),M=kbM(),L=kbData(mo).filter(x=>w=='all'||!M[x.k]),R=rlShort(),o=['📤 *طلب طباعة* — شهر '+mo.split('-').reverse().join('-'),''];L.forEach(x=>o.push('• '+x.k+' ×'+x.n+' (صيدلية '+x.ph.join('، ')+')'));if(R.length){o.push('','🧻 رولات:');R.forEach(x=>o.push('• رول '+x.s+' — ناقص '+x.miss+' م'))}return o.join('\n')}
// ---- messages: first / last line (settings)
const msgW=(k,t)=>{const m=(D26().msg||{})[k]||{};return [m.h,t,m.f].filter(x=>x&&String(x).trim()).join('\n\n')};
function shareTxt(t){if(navigator.share)navigator.share({text:t}).catch(()=>{});else{try{navigator.clipboard.writeText(t)}catch(e){}window.open('https://wa.me/?text='+encodeURIComponent(t),'_blank')}}
const _nqText26=nqText;nqText=function(){const t=_nqText26.apply(this,arguments);return t?msgW('nq',t):t};
const _rteText26=rteText;rteText=function(){return msgW('rte',_rteText26.apply(this,arguments))};
const _avlText26=avlText;avlText=function(){return msgW('avl',_avlText26.apply(this,arguments))};
// ---- 9 / 10) places with phone / WhatsApp / hours / order, contacts
const telU=t=>'tel:'+String(t||'').replace(/[^\d+]/g,''),waU=t=>{let d=String(t||'').replace(/\D/g,'');if(d.startsWith('00'))d=d.slice(2);if(d.startsWith('0'))d='966'+d.slice(1);return 'https://wa.me/'+d};
const ctB=(tel,wa)=>`${tel?`<a class="locb" href="${telU(tel)}">📞 اتصال</a>`:''}${wa||tel?`<a class="locb go" href="${waU(wa||tel)}" target="_blank" rel="noopener">💬 واتساب</a>`:''}`;
plcHtml=function(){const L=PLC(),hm=DB.cfg.rtHome;
 let h=`<div class="wcard"><h2>${ic('pin')}المواقع الهامة</h2><p class="sub">دوس على الموقع يفتح في جوجل ماب. الموقع اللي عليه 🏠 هو نقطة البداية والرجوع في «جدول السير».</p><div class="locs"><a class="locb" href="${DAWAA_ALL}" target="_blank" rel="noopener">${ic('pin')}مواقع الصيدليات (موقع الدواء ↗)</a></div></div>`;
 if(!L.length)h+='<p class="em">مفيش مواقع لسه. ضيف موقع من تحت أو استورد ملف المواقع.</p>';
 L.forEach((x,i)=>{h+=`<div class="wcard"><div class="locs"><a class="locb go" href="${plcUrl(x.c)}" target="_blank" rel="noopener">${ic('pin')}${esc(x.ic||'📍')} ${esc(x.n)}</a>${ctB(x.tel,x.wa)}</div>
  <small class="hint">${plcC(x.c)}${x.ad?' · '+esc(x.ad):''}</small>${x.hrs?`<small class="hint">🕘 ${esc(x.hrs)}</small>`:''}${x.tel||x.wa?`<small class="hint">${[x.tel?'📞 '+esc(x.tel):'',x.wa&&x.wa!=x.tel?'💬 '+esc(x.wa):''].filter(Boolean).join(' · ')}</small>`:''}
  <div class="tt"><button${String(x.id)==String(hm)?' class="pr"':''} data-plch="${x.id}">🏠 ${String(x.id)==String(hm)?'البداية والرجوع ✓':'البداية والرجوع'}</button>${i?`<button data-plcu="${x.id}" title="لفوق">↑</button>`:''}${i<L.length-1?`<button data-plcdn="${x.id}" title="لتحت">↓</button>`:''}<button data-plce="${x.id}">✏️ تعديل</button><button data-plcd="${x.id}">🗑 حذف</button></div></div>`});
 h+=`<div class="wcard"><h3>➕ موقع جديد</h3><label>الاسم<input id="plcn" placeholder="مثال: مخزن الرياض"></label><label>لينك جوجل ماب أو الإحداثيات<textarea id="plcl" rows="2" placeholder="24.562390, 46.586851"></textarea></label><div class="tt"><button class="pr" data-plca="1">إضافة</button></div></div>`;return h};
const _plcEdit26=plcEdit;plcEdit=async function(id){await _plcEdit26(id);const x=plcGet(id);if(!x)return;const t=prompt('رقم الاتصال (فاضي = مفيش):',x.tel||'');if(t==null)return;const w=prompt('رقم الواتساب (فاضي = نفس رقم الاتصال):',x.wa||'');if(w==null)return;const hr=prompt('مواعيد العمل (اختياري):',x.hrs||'');if(hr==null)return;
 x.tel=t.trim();x.wa=w.trim();x.hrs=hr.trim();sv();render()};
const CNT=()=>D26().cnt=D26().cnt||[];
function cntHtml(){const L=CNT();let h=`<div class="wcard"><h2>📞 أرقام هامة</h2><p class="sub">اتصال أو واتساب بضغطة. تقدر تعدّل أو تضيف أو تمسح.</p></div>`;if(!L.length)h+='<p class="em">مفيش أرقام لسه. ضيف من تحت أو استورد ملف المواقع والأرقام.</p>';
 L.forEach((x,i)=>{h+=`<div class="wcard"><div class="cnt26"><b>${esc(x.n)}</b>${x.t?`<small>${esc(x.t)}</small>`:''}<small dir="ltr">${esc(x.tel||'')}</small></div><div class="locs">${ctB(x.tel,x.wa)}</div>
  <div class="tt">${i?`<button data-cntu="${i}">↑</button>`:''}${i<L.length-1?`<button data-cntdn="${i}">↓</button>`:''}<button data-cnte="${i}">✏️ تعديل</button><button data-cntd="${i}">🗑 حذف</button></div></div>`});
 return h+`<div class="wcard"><h3>➕ رقم جديد</h3><label>الاسم<input id="cntn"></label><label>الصفة<input id="cntt" placeholder="مثال: الطباعة"></label><label>الرقم<input id="cntp" inputmode="tel" placeholder="05xxxxxxxx"></label><label>رقم الواتساب (فاضي = نفس الرقم)<input id="cntw" inputmode="tel"></label><div class="tt"><button class="pr" data-cnta="1">إضافة</button></div></div>`}
const mv=(A,i,d)=>{const j=i+d;if(j<0||j>=A.length)return;const t=A[i];A[i]=A[j];A[j]=t};
plcImpOpen=function(q){const P=Array.isArray(q.places)?q.places.filter(x=>x&&x.n&&Array.isArray(x.c)):[],H=Array.isArray(q.ph)?q.ph.filter(z=>z&&z.no&&Array.isArray(z.c)):[],C=Array.isArray(q.contacts)?q.contacts.filter(x=>x&&x.n):[];
 const hit=H.map(z=>[z,DB.ph.filter(p=>String(p.no)==String(z.no))]),miss=hit.filter(([,a])=>!a.length).map(([z])=>z.no),nP=hit.reduce((a,[,A])=>a+A.length,0);
 if(!confirm(`ملف المواقع والأرقام:\n• ${P.length} موقع هام${P.length?' ('+P.map(x=>x.n).join('، ')+')':''}${C.length?'\n• '+C.length+' رقم هام ('+C.map(x=>x.n).join('، ')+')':''}${H.length?'\n• إحداثيات '+H.length+' صيدلية ('+nP+' سجل في البرنامج)':''}${miss.length?'\n• مش موجودة عندك: '+miss.join('، '):''}\n\nالموجود بنفس الاسم بيتحدّث، والجديد بيتضاف. تكمل؟`))return;
 P.forEach(x=>{let o=PLC().find(y=>y.n==x.n);if(!o){o={id:Date.now()+Math.floor(Math.random()*1e3),n:x.n,ic:x.ic||'📍',ad:'',c:x.c};PLC().push(o)}o.c=x.c;['ic','ad','tel','wa','hrs'].forEach(k=>{if(x[k]!=null&&x[k]!=='')o[k]=x[k]});if(x.home)DB.cfg.rtHome=o.id});
 if(q.order){const ord=P.map(x=>x.n),A=PLC(),inF=A.filter(y=>ord.includes(y.n)).sort((a,b)=>ord.indexOf(a.n)-ord.indexOf(b.n)),out=A.filter(y=>!ord.includes(y.n));DB.cfg.places=inF.concat(out)}
 C.forEach(x=>{const o=CNT().find(y=>y.n==x.n);if(o)Object.assign(o,{t:x.t||o.t,tel:x.tel||o.tel,wa:x.wa||o.wa});else CNT().push({n:x.n,t:x.t||'',tel:x.tel||'',wa:x.wa||''})});
 hit.forEach(([z,A])=>A.forEach(p=>{if(!p.loc)p.loc=plcUrl(z.c);p.locc=z.c;p.locs=p.loc;p.modAt=nowIso()}));
 sv();snd('ok');toastT(`✓ ${P.length} موقع · ${C.length} رقم${nP?' · '+nP+' صيدلية':''}`);goV({v:'plc',op:{},dr:{},q:V.q})};
// ---- 12) types: acrylic boards, A3/A4 names, default acrylic, letters, maintenance work, fridge
function tabHtml(){const c=D26(),ax=c.abx||[],mods=(DB.cfg.modTypes||[]).filter(m=>m!='صيانة');
 let h=`<div class="wcard"><h2>Acrylic boards</h2><p class="sub">البنود ومقاساتها. اللي إنت ضفته تقدر تمسحه؛ الأساسي مقاسه بيتعدّل من «المقاسات والخامات».</p><div class="sc"><table class="ctab"><tr><th>البند</th><th>المقاس · الخامة</th><th></th></tr>${ABI.map(it=>{const x=ax.find(y=>y.it==it);return `<tr><td>${esc(it)}</td><td><small>${esc(String(SZ('abs.'+it)||'—').split('|').join(' · '))}</small></td><td>${x?`<button class="lnk" data-abxd="${esc(it)}">🗑</button>`:''}</td></tr>`}).join('')}</table></div>
 <div class="fm"><b>➕ بند جديد</b><label>الاسم<input id="abxn" placeholder="مثال: لوحة عروض · Offers board"></label><div class="c2"><label>المقاس<input id="abxs" placeholder="30×40"></label><label>الخامة<input id="abxm" value="أكريليك"></label></div><div class="tt"><button class="pr" data-abxa="1">إضافة</button></div></div></div>
 <div class="wcard"><h3>أسماء لوحات A3 / A4</h3><small class="hint">سطر لكل اسم.</small><textarea data-c26="abn" rows="6">${esc(ABN.join('\n'))}</textarea></div>
 <div class="wcard"><h3>الأكريليك التلقائي للصيدلية الجديدة</h3><p class="sub">اللي بيتضاف لوحده حسب نوع التعديل (صيانة = مفيش).</p>`;
 mods.forEach(m=>{const L=ABD(m);h+=`<details class="mg" data-id="abd_${esc(m)}"${V.op['abd_'+m]?' open':''}><summary><span>${esc(m)}</span><i>${L.length}</i></summary><div class="mgb">${L.map((r,i)=>`<div class="rw"><span>${esc(r.it)}${r.an?' · '+esc(r.an):''} ×${r.q} · ${esc(r.stt)}</span><div class="bt"><button data-abdd="${esc(m)}|${i}">🗑</button></div></div>`).join('')||'<p class="em">مفيش</p>'}
  <div class="fm"><div class="c2"><label>البند<select id="abdi_${esc(m)}">${ABI.map(it=>`<option>${esc(it)}</option>`).join('')}</select></label><label>اسم اللوحة (A3/A4)<select id="abdn_${esc(m)}"><option value="">—</option>${ABN.map(n=>`<option>${esc(n)}</option>`).join('')}</select></label></div><div class="c2"><label>العدد<input id="abdq_${esc(m)}" type="number" inputmode="decimal" value="1"></label><label>نوع الشغل<select id="abds_${esc(m)}">${ABST.map(s=>`<option>${esc(s)}</option>`).join('')}</select></label></div>
  <div class="tt"><button class="pr" data-abda="${esc(m)}">إضافة</button>${(c.abd||{})[m]?`<button data-abdr="${esc(m)}">↺ رجوع للأساسي</button>`:''}</div></div></div></details>`});
 return h+'</div>'}
function tlrHtml(){return `<div class="wcard"><h2>نسب حروف الأكريليك</h2><p class="sub">ارتفاع الحروف ← عرض جملة الحروف لكل قسم (h0 × w0). بتأثر على البنود الجديدة.</p><div class="sc"><table class="ctab"><tr><th>القسم</th><th>ارتفاع h0</th><th>عرض w0</th></tr>${Object.keys(RATIO).map(k=>`<tr><td>${esc(k)}</td><td><input type="number" inputmode="decimal" data-c26r="${esc(k)}|0" value="${RATIO[k][0]}"></td><td><input type="number" inputmode="decimal" data-c26r="${esc(k)}|1" value="${RATIO[k][1]}"></td></tr>`).join('')}</table></div><div class="tt"><button data-c26rr="1">↺ رجوع للأساسي</button></div></div>`}
function tlist(t,k,cur,hint){return `<div class="wcard"><h2>${t}</h2><small class="hint">${hint||'سطر لكل نوع.'}</small><textarea data-c26="${k}" rows="8">${esc(cur.join('\n'))}</textarea><div class="tt"><button data-c26x="${k}">↺ رجوع للأساسي</button></div></div>`}
// ---- 12) general settings sections
function setHtml26(){const c=D26(),m=c.msg||{},cu=CU().cfg,ms=(k,t)=>`<b>${t}</b><div class="c2"><label>أول سطر<input data-c26m="${k}|h" value="${esc((m[k]||{}).h||'')}"></label><label>آخر سطر<input data-c26m="${k}|f" value="${esc((m[k]||{}).f||'')}"></label></div>`;
 const sec=(id,t,b)=>`<details class="wcard" data-id="${id}"${V.op[id]?' open':''}><summary><b>${t}</b></summary>${b}</details>`;
 return sec('__s_tl','🧰 الأدوات',`<small class="hint">سطر لكل أداة. بتظهر لما تخلّي الصيدلية مكتملة، وفي إشعار لما تمشي منها.</small><textarea data-c26="tools" rows="8">${esc(TOOLS().join('\n'))}</textarea>`)
 +sec('__s_cx','💬 أسباب طلب العميل',`<small class="hint">سطر لكل سبب.</small><textarea data-c26="cxr" rows="4">${esc(CXR.join('\n'))}</textarea>`)
 +sec('__s_vz','📍 متابعة الزيارات',`<small class="hint">${typeof vOnCfg=='function'&&vOnCfg()?'شغالة':'مقفولة'} — التشغيل والإيقاف من «إدارة التنبيهات».</small><div class="tt"><button data-mgo="ntf">🔔 إدارة التنبيهات ›</button></div>
  <div class="c2"><label>مسافة الوصول (متر)<input type="number" inputmode="decimal" data-c26v="in" value="${Math.round(VZ.in*1000)}"></label><label>مدة الوقفة (دقيقة)<input type="number" inputmode="decimal" data-c26v="stay" value="${VZ.stay}"></label></div>
  <div class="c2"><label>مسافة «مشيت» (متر)<input type="number" inputmode="decimal" data-c26v="out" value="${Math.round(VZ.out*1000)}"></label><label>من الساعة<input type="number" inputmode="decimal" data-c26v="h0" value="${VZ.h0}"></label></div><label>لحد الساعة<input type="number" inputmode="decimal" data-c26v="h1" value="${VZ.h1}"></label>`)
 +sec('__s_ck','💰 العهدة',`<small class="hint">أنواع المصروف (سطر لكل نوع)، وجنب كل نوع البيان الافتراضي بعد «:» (مثال: عمالة: أجرة عامل تحميل وتنزيل بضاعة).</small><textarea data-c26="ck" rows="9">${esc(CK.map(k=>k+((c.ckd||{})[k]?': '+c.ckd[k]:'')).join('\n'))}</textarea>
  <div class="c2"><label>رصيد العهدة الكامل<input type="number" inputmode="decimal" data-c26c="base" value="${cu.base}"></label><label>أقل متبقي ينقل للشهر الجديد<input type="number" inputmode="decimal" data-c26c="min" value="${cu.min}"></label></div>`)
 +sec('__s_ms','✉️ الرسائل',`<small class="hint">بيتحطوا أول وآخر رسالة الواتساب.</small>${ms('nq','النواقص')}${ms('rte','جدول السير')}${ms('avl','الموجود والناقص')}${ms('kbr','طلب طباعة الخبر')}${ms('ld','تحميل العربية')}`)}
// ---- 11) menu, grouped screens
const MCHK=['chk','🔍 فحص البيانات','check'];Object.defineProperty(MCHK,1,{get(){const n=chkN();return 'فحص البيانات'+(n?` <i class="mnb">${n}</i>`:'')}});
fill(MENU,[['all','التقارير','layers'],['bk','النسخ والاستيراد','db'],['cust','العهدة','sheet'],['plc','مواقع وأرقام هامة','pin'],['prep','تجهيز الشغل','check'],MCHK,['cdoc','مستندات الشركة','sheet'],['types','الأنواع والمسميات','list'],['gen','الإعدادات العامة','gear'],['ntf','إدارة التنبيهات','bell'],['prc','التسعير','sheet'],['look','الشكل','look'],['req','الطلبات والأعطال','list'],['calc','الحاسبة','calc'],['usr','المستخدمين والمشرفين','lock'],['lang','اللغة / Language','globe']]);
Object.assign(TABOF,{load:'',kbr:'',chk:'',cnt:'',tab:'',tlr:'',tmw:'',tfr:'',avl:'',plc:''});
const CHIPS=[[['prep','التجهيز'],['load','التحميل'],['avl','الموجود والناقص'],['kbr','طلب الخبر']],[['plc','المواقع'],['cnt','الأرقام']],[['types','الأنواع والمسميات'],['tab','Acrylic boards'],['tlr','الحروف'],['tmw','أعمال الصيانة'],['tfr','الثلاجة'],['set','المقاسات والخامات'],['imgs','صور المسميات']],[['prc','الأسعار'],['docs:quotes','العروض'],['docs:invoices','الفواتير']]];
function chipBar(){const cur=V.v=='docs'?'docs:'+(V.doc||'quotes'):V.v,G=CHIPS.find(g=>g.some(x=>x[0]==cur));if(!G)return '';return `<div class="chip26">${G.map(([k,t])=>`<button class="${k==cur?'pr':''}" data-gov="${k}">${t}</button>`).join('')}</div>`}
const _render0_26=render0;render0=function(){cfg26();const a=$('#app');
 const pg=(t,b)=>{cfg();a.innerHTML=hdr(backBtn(),t)+`<main>${chipBar()}${b}</main>`};
 if(V.v=='chk')return pg('🔍 فحص البيانات',chkHtml());if(V.v=='load')return pg('🚚 تجهيز الشغل',ldHtml());if(V.v=='kbr')return pg('📤 تجهيز الشغل',kbHtml());if(V.v=='cnt')return pg('📞 مواقع وأرقام هامة',cntHtml());
 if(V.v=='tab')return pg('📚 الأنواع والمسميات',tabHtml());if(V.v=='tlr')return pg('📚 الأنواع والمسميات',tlrHtml());
 if(V.v=='tmw')return pg('📚 الأنواع والمسميات',tlist('أنواع أعمال الصيانة','mw',MW,'سطر لكل نوع. «تغيير» بيفضل الافتراضي في بند الصيانة.'));
 if(V.v=='tfr')return pg('📚 الأنواع والمسميات',tlist('أنواع ستيكر الثلاجة','frk',FRK));
 const out=_render0_26.apply(this,arguments);
 try{const m=a.querySelector('main');if(m&&!m.querySelector('.chip26')){const cb=chipBar();if(cb)m.insertAdjacentHTML('afterbegin',cb)}
  if(V.v=='gen'&&m&&!m.querySelector('[data-c26="tools"]'))m.insertAdjacentHTML('beforeend',setHtml26());
  if(V.v=='ph'){const p=curP();if(p){const w=document.querySelector('[data-fo="ws"],[data-add="ws"]');if(w&&!document.querySelector('.rlx26')){const at=w.closest('.addrow')||w.closest('.fm')||w;at.insertAdjacentHTML('beforebegin',rlBox26(p))}
   if(m&&!m.querySelector('[data-tlo]')&&!uStoreRO())m.insertAdjacentHTML('beforeend',`<div class="tt tl26"><button data-tlo="${p.id}">🧰 مراجعة الأدوات قبل ما تمشي</button></div>`)}}
  if(V.v=='bk')bkGroup()}catch(e){console.warn(e)}return out};
// backups screen: grouped sections
function bkGroup(){const m=$('#app main');if(!m||m.querySelector('.bkg26'))return;const S=[...m.querySelectorAll('.bsec')],tt=x=>(x.querySelector('h4')||{}).textContent||'';
 const pick=re=>S.filter(x=>re.test(tt(x)));const G=[['__b_bk','💾 النسخة الاحتياطية',pick(/النسخة الاحتياطية الكاملة/)],['__b_im','📥 الاستيراد',pick(/استيراد صيدليات|إرفاق مخططات/)],['__b_ex','📊 تصدير للتحليل',pick(/Excel وLooker/)],['__b_dir','📁 النسخ التلقائية على اللاب توب',pick(/النسخ التلقائية/)],['__b_adv','⚙️ متقدم',pick(/المزامنة|المواصفات|تطبيق الجوال/)]];
 S.forEach(x=>{const h=x.querySelector('h4');if(h)h.innerHTML=h.innerHTML.replace(/\d\.\s*/,'')});
 let anchor=S[0];if(!anchor)return;G.forEach(([id,t,L])=>{if(!L.length)return;const d=document.createElement('details');d.className='mg lst bkg26';d.dataset.id=id;if(V.op[id]||(id=='__b_bk'&&V.op[id]!==false))d.open=true;d.innerHTML=`<summary><span>${t}</span></summary><div class="mgb"></div>`;anchor.parentNode.insertBefore(d,anchor);L.forEach(x=>d.querySelector('.mgb').appendChild(x));anchor=d.nextSibling});
 const tr=m.querySelector('.trs, .trash')||[...m.querySelectorAll('h3,h4,b')].find(x=>/سلة المحذوفات/.test(x.textContent)),sn=m.querySelector('.snl');
 if(sn){const d=document.createElement('details');d.className='mg lst bkg26';d.dataset.id='__b_rs';if(V.op.__b_rs)d.open=true;d.innerHTML='<summary><span>♻️ الاسترجاع (نقط الاستعادة وسلة المحذوفات)</span></summary><div class="mgb"></div>';const box=d.querySelector('.mgb');
  const blk=[];let n=sn;while(n&&!(n.tagName=='INPUT')){blk.push(n);n=n.nextElementSibling}const tw=tr&&tr.closest('.bsec,.wcard,div');sn.parentNode.insertBefore(d,sn);if(tw&&tw!==m&&!tw.contains(d))box.appendChild(tw);blk.forEach(x=>box.appendChild(x))}}
// ---- clicks / changes
const _v24Click26=v24Click;v24Click=function(d,b){
 if(d.gov){const[v,doc]=d.gov.split(':');goV({v,doc,from:V.from,op:{},dr:{},q:V.q,ld:V.ld,am2:V.am2});if(doc){V.doc=doc;render()}return 1}
 if(d.ldgo){ldGo(d.ldgo);return 1}if(d.ldwa){shareTxt(msgW('ld',ldText()));return 1}
 if(d.kbwa){shareTxt(msgW('kbr',kbText(d.kbwa)));return 1}
 if(d.kbok){const mo=V.am2||V.pm||MN(),M=kbM();kbData(mo).forEach(x=>{if(!M[x.k])M[x.k]={dt:TD(),n:x.n}});Object.keys(M).forEach(k=>{if((new Date(TD())-new Date(M[k].dt))/864e5>60)delete M[k]});sv();render();toastT('✓ اتعلّموا «اتطلب»');return 1}
 if(d.kbun){delete kbM()[d.kbun];sv();render();return 1}
 if(d.tlo){tlOpen(+d.tlo||d.tlo,null);return 1}if(d.tlt&&TLS){TLS.ok[+d.tlt]=!TLS.ok[+d.tlt];tlDraw();return 1}if(d.tlok&&TLS){tlDone(true);return 1}if(d.tlno&&TLS){tlDone(false);return 1}
 if(d.plcu||d.plcdn){const A=PLC(),i=A.findIndex(x=>String(x.id)==String(d.plcu||d.plcdn));if(i>=0){mv(A,i,d.plcu?-1:1);sv();render()}return 1}
 if(d.cntu||d.cntdn){mv(CNT(),+(d.cntu||d.cntdn),d.cntu?-1:1);sv();render();return 1}
 if(d.cntd){const x=CNT()[+d.cntd];if(x&&confirm('حذف «'+x.n+'»؟')){CNT().splice(+d.cntd,1);sv();render()}return 1}
 if(d.cnte){const x=CNT()[+d.cnte];if(!x)return 1;const n=prompt('الاسم:',x.n);if(n==null)return 1;const t=prompt('الصفة:',x.t||'');if(t==null)return 1;const p=prompt('الرقم:',x.tel||'');if(p==null)return 1;const w=prompt('رقم الواتساب (فاضي = نفس الرقم):',x.wa||'');if(w==null)return 1;Object.assign(x,{n:n.trim()||x.n,t:t.trim(),tel:p.trim(),wa:w.trim()});sv();render();return 1}
 if(d.cnta){const n=($('#cntn').value||'').trim();if(!n)return alert('اكتب الاسم'),1;CNT().push({n,t:($('#cntt').value||'').trim(),tel:($('#cntp').value||'').trim(),wa:($('#cntw').value||'').trim()});sv();render();toastT('✓ اتضاف «'+n+'»');return 1}
 if(d.abxa){const it=($('#abxn').value||'').trim(),sz=($('#abxs').value||'').trim(),mat=($('#abxm').value||'').trim()||'أكريليك';if(!it)return alert('اكتب اسم البند'),1;if(ABI.includes(it))return alert('البند ده موجود'),1;const c=D26();c.abx=(c.abx||[]).concat([{it,sz:sz||'—',mat}]);cfg26();sv();render();toastT('✓ اتضاف «'+it+'»');return 1}
 if(d.abxd){const c=D26();if(!confirm('مسح «'+d.abxd+'» من البنود؟ (البنود المتسجلة في الصيدليات بتفضل زي ما هي)'))return 1;c.abx=(c.abx||[]).filter(x=>x.it!=d.abxd);delete SZD['abs.'+d.abxd];cfg26();sv();render();return 1}
 if(d.abda){const m=d.abda,c=D26(),L=ABD(m),it=$('#abdi_'+CSS.escape(m)).value,an=$('#abdn_'+CSS.escape(m)).value,q=+$('#abdq_'+CSS.escape(m)).value||1,stt=$('#abds_'+CSS.escape(m)).value;const r={it,q,stt};if(an&&isAB34(it))r.an=an;c.abd=c.abd||{};c.abd[m]=L.concat([r]);V.op['abd_'+m]=true;sv();render();return 1}
 if(d.abdd){const[m,i]=d.abdd.split('|'),c=D26(),L=ABD(m);L.splice(+i,1);c.abd=c.abd||{};c.abd[m]=L;V.op['abd_'+m]=true;sv();render();return 1}
 if(d.abdr){const c=D26();if(c.abd)delete c.abd[d.abdr];sv();render();return 1}
 if(d.c26rr){delete D26().ratio;cfg26();sv();render();return 1}
 if(d.c26x){delete D26()[d.c26x];cfg26();sv();render();return 1}
 return _v24Click26(d,b)};
const _v33Change26=v33Change;v33Change=function(x){const ds=x.dataset||{};
 if(x.id=='ldd'){V.ld=x.value;render();return 1}if(x.id=='kbm'){V.am2=x.value;render();return 1}
 if(ds.c26){const c=D26(),L=String(x.value).split('\n').map(y=>y.trim()).filter(Boolean);
  if(ds.c26=='ck'){c.ck=L.map(y=>y.split(/[:：]/)[0].trim()).filter(Boolean);c.ckd={};L.forEach(y=>{const i=y.search(/[:：]/);if(i>0){const v=y.slice(i+1).trim();if(v)c.ckd[y.slice(0,i).trim()]=v}})}else c[ds.c26]=L;cfg26();sv();toastT('✓ اتحفظ');return 1}
 if(ds.c26v){const c=D26();c.vz=c.vz||{};let v=+x.value;if(!(v>=0))return 1;if(ds.c26v=='in'||ds.c26v=='out')v=v/1000;c.vz[ds.c26v]=v;cfg26();sv();toastT('✓ اتحفظ');return 1}
 if(ds.c26c){const v=+x.value;if(v>=0){CU().cfg[ds.c26c]=v;sv();toastT('✓ اتحفظ')}return 1}
 if(ds.c26m){const[k,w]=ds.c26m.split('|'),c=D26();c.msg=c.msg||{};c.msg[k]=c.msg[k]||{};c.msg[k][w]=x.value.trim();sv();return 1}
 if(ds.c26r){const[k,i]=ds.c26r.split('|'),c=D26(),v=+x.value;if(!(v>0))return 1;c.ratio=c.ratio||{};c.ratio[k]=(c.ratio[k]||RATIO[k].slice());c.ratio[k][+i]=v;cfg26();sv();toastT('✓ اتحفظ');return 1}
 return _v33Change26(x)};
const _descOf26=descOf;descOf=function(kind,tm,comp){const m=CU().mem[cnk(comp)];if(!(m&&m.desc)){const v=(D26().ckd||{})[kind];if(v)return v}return _descOf26.apply(this,arguments)};
// ---- start: restore point, fixes
setTimeout(()=>{try{if(!D26().snap){snap('قبل تحديث 2.6');D26().snap=1;svq()}}catch(e){}},900);
setTimeout(()=>{try{cfg26();whFix26();rlFix26();svq()}catch(e){console.warn('fix26',e)}},1700);

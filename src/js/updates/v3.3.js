// ---------- v3.3: custom names ----------
const XNT=['ec','md','fh','wh','eg','ga'];
const XNB={NM:Object.fromEntries(Object.entries(NM).map(([k,v])=>[k,v.slice()])),EC:Object.fromEntries(Object.entries(EC).map(([k,v])=>[k,v.slice()])),EG:EG.slice(),MED:MED.slice(),GA:GAL.slice()};
function xnApply(){const X=(DB&&DB.cfg&&DB.cfg.xn)||{},set=(a,b,add)=>{a.length=0;b.forEach(v=>a.push(v));(add||[]).forEach(v=>{if(v&&!a.includes(v))a.push(v)})};
 Object.keys(XNB.NM).forEach(k=>set(NM[k],XNB.NM[k],X['nm:'+k]));Object.keys(X).forEach(k=>{if(/^nm:/.test(k)&&!XNB.NM[k.slice(3)])NM[k.slice(3)]=X[k].slice()});
 Object.keys(XNB.EC).forEach(k=>set(EC[k],XNB.EC[k],X['ec:'+k]));set(EG,XNB.EG,X.eg);set(MED,XNB.MED,X.md);set(GAL,XNB.GA,X.ga)}
const xnKey=(tid,d)=>tid=='ga'?'ga':tid=='ec'?'ec:'+d.sec:tid=='eg'?'eg':tid=='md'||(tid=='fh'&&d.sec=='Medicated')?'md':'nm:'+d.sec;
const XNL=k=>k=='ga'?'ضفها للسلة':k=='eg'?'End gandola':k=='md'?'Medicated':/^ec:/.test(k)?'End cap · '+k.slice(3):'Floor / Wall Header · '+k.slice(3);
function xnNew(tid){const t=T.find(x=>x.id==tid),q=curP(),sh=q?q.sh:0;if(!t)return;const d=draft(t,sh);if(tid=='wh'&&wood(d))return alert('مسميات الخشب ثابتة. غيّر النوع لـ WALL NORMAL الأول.');
 const key=xnKey(tid,d),sp=tid=='eg'?String(d.nm||'Personal · ').split(' · ')[0]:'',ex=tid=='ga'?'عروض رمضان':tid=='ec'?'Sun care · واقي الشمس':tid=='eg'?'Hair care · عناية بالشعر':key=='md'?'La Roche-Posay':'Sun care';
 let v=prompt(`مسمى جديد لـ ${t.n} · ${tid=='ga'?'(اسم الجندولة)':tid=='eg'?'قسم '+sp:key=='md'?'Medicated':'قسم '+(d.sec||'')}\nاكتبه بالشكل: ${ex}${tid=='eg'?'\n(لقسم تاني: اختار مسمى من القسم ده الأول)':''}`,'');if(v==null)return;v=v.replace(/\s+/g,' ').trim();if(!v)return;if(tid=='eg'&&!v.startsWith(sp+' · '))v=sp+' · '+v;
 const f=t.f.find(x=>x.k=='nm'),L=opts(f,d,sh),hit=L.find(x=>x.toLowerCase()==v.toLowerCase());if(hit){d.nm=hit;render();return toastT('المسمى ده موجود، واتختار')}
 const X=DB.cfg.xn=DB.cfg.xn||{};(X[key]=X[key]||[]).push(v);xnApply();d.nm=v;sv();render();toastT('✓ اتضاف المسمى: '+v)}
function xnMgHtml(){const X=DB.cfg.xn||{},K=Object.keys(X).filter(k=>(X[k]||[]).length);return `<h3>المسميات المضافة</h3><small>بتتضاف من قائمة «المسمى» ← «➕ مسمى جديد». لو مسحت مسمى، البنود المسجّلة بيه بتفضل زي ما هي.</small><div class="sc"><table><tr><th>القائمة</th><th>المسمى</th><th>الإجراءات</th></tr>${K.length?K.map(k=>X[k].map((n,i)=>`<tr><td>${esc(XNL(k))}</td><td>${esc(n)}</td><td><button data-xned="${esc(k)}|${i}">تعديل</button> <button data-xndel="${esc(k)}|${i}">حذف</button></td></tr>`).join('')).join(''):'<tr><td colspan="3">لا توجد مسميات مضافة</td></tr>'}</table></div>`}
// ---------- v3.3: warehouse by real size, any shelf type ----------
const whKey0=x=>whKey(x).split('|').slice(1).join('|');
function whPool(y){const k0=whKey0(y),ek=whKey(y);return WU().filter(x=>+x.qty>0&&whKey0(x)==k0).sort((a,b)=>(whKey(b)==ek)-(whKey(a)==ek)||(+b.qty)-(+a.qty))}
const whQty=y=>whPool(y).reduce((a,x)=>a+(+x.qty||0),0);
function whStQ(st,y){const k0=whKey0(y);let n=0;Object.keys(st).forEach(k=>{if(k.split('|').slice(1).join('|')==k0)n+=+st[k]||0});return n}
function whTakeQ(y,n,src,note){let left=wq(n);for(const x of whPool(y)){if(left<=1e-9)break;const d=Math.min(left,+x.qty);whAdd(x,-d,'out',src,note+(whKey(x)!=whKey(y)?' (من مخزن '+(x.sh>=0?SH[x.sh]:'بدون نوع رفوف')+')':''));left=wq(left-d)}return wq(n-left)}
function whCross(y,n){const ek=whKey(y),o=[];let left=n;for(const x of whPool(y)){if(left<=1e-9)break;const d=Math.min(left,+x.qty);if(whKey(x)!=ek&&!(TK3.includes(x.sh)&&TK3.includes(y.sh)))o.push(x.sh>=0?SH[x.sh]:'بدون نوع رفوف');left-=d}return o}
function whXT(t,r,sh,n){if(!(n>0))return '';const o=new Set();whParts(t,r,sh).filter(y=>!y.pk).forEach(y=>whCross(y,n*y.f).forEach(x=>o.add(x)));return o.size?` ⚠ هيتسحب من مخزن ${[...o].join(' و')} (نوع رفوف مختلف، نفس المقاس).`:''}
// ---------- v3.3: «قائمة التجهيز» ----------
function prepRows(p){return ckRows(p).filter(x=>!(x.t.id=='eg'&&egAO(x.r,x.s)))}
function prepHtml(){const ms=months().reverse(),mo=V.pm||V.xm||MN(),P=DB.ph.filter(p=>p.mo==mo).sort(pSort),F=V.pf||'',hide=V.p0!==false,pid=V.pp||'';
 const all=[];P.forEach(p=>{if(pid&&p.id!=pid)return;prepRows(p).forEach(x=>all.push([p,x]))});const tys=[...new Set(all.map(([,x])=>x.t.n))];
 const L=all.filter(([,x])=>!F||x.t.n==F),need=([,x])=>x.r.cx?0:Math.max(0,qn(x.r)-(+x.r.r||0)),left=L.reduce((a,o)=>a+need(o),0),tot=L.reduce((a,[,x])=>a+qn(x.r),0);
 let h=`<div class="wcard"><h2>${ic('check')}قائمة التجهيز</h2><p class="sub">اللي تجهزه من المخزن أو يوصلك من الطباعة: دوس + أو ✓ ويتحسب <b>مستلم</b> للصيدلية. اللي يكمل بيختفي، والباقي بيطلع في «نواقص الطباعة».</p>
 <div class="c2"><label>الشهر<select id="ppm">${ms.map(m=>`<option${m==mo?' selected':''}>${m}</option>`).join('')}</select></label><label>الصيدلية<select id="ppp"><option value="">كل الصيدليات (${P.length})</option>${P.map(p=>`<option value="${p.id}"${p.id==pid?' selected':''}>${esc(p.no)}${p.name?' · '+esc(p.name):''}</option>`).join('')}</select></label></div>
 <div class="rtchips">${['',...tys].map(n=>`<button class="${n==F?'pr':''}" data-ppf="${esc(n)||'*'}">${n?esc(n):'الكل'}</button>`).join('')}</div>
 <label class="chk"><input type="checkbox" id="pph"${hide?' checked':''}> اخفي اللي اكتمل</label>
 <div class="pgw"><div class="pg"><i style="width:${tot?Math.round(100*(tot-left)/tot):0}%"></i></div><small>فاضل <b>${left}</b> من ${tot} قطعة</small></div>
 <div class="tt"><button data-nq="r:mo">${ic('list')}نواقص الطباعة — الشهر</button></div></div>`;
 P.forEach(p=>{if(pid&&p.id!=pid)return;const A=prepRows(p).filter(x=>!F||x.t.n==F);if(!A.length)return;const V2=A.filter(x=>!hide||(!x.r.cx&&qn(x.r)-(+x.r.r||0)>0)),pl=A.reduce((a,x)=>a+(x.r.cx?0:Math.max(0,qn(x.r)-(+x.r.r||0))),0);
  h+=`<details class="wcard ppw" data-id="pp_${p.id}"${V.op['pp_'+p.id]||pid||P.length<4?' open':''}><summary><b>${PL(p)}</b><small>${pl?'فاضل '+pl:'✓ كله اتجهز'}</small></summary>${V2.length?V2.map(x=>{const r=x.r,q=qn(r),v=Math.min(q,+r.r||0),sc=x.t.id=='ab'?'':scOf(r),c=cl(r),z=x.t.z(r,x.s),dt=sc?z.replace(sc+' · ',''):z,id=`${p.id}:${x.t.id}:${x.i}`,st=r.cx||v>=q?'ok':v>0?'pt':'no';
   return `<div class="ppr tk-${st}"><span class="ppn"><small class="ppt" style="${c?bgc(c):''}">${esc(sc||x.t.n)}</small><b>${esc(x.t.n)}</b> ${esc(dt)}${x.t.id=='eg'&&egSub(r,x.s)?'<small class="hint">الجيوب من شاشة الاستلام</small>':''}${r.cx?'<small class="rshc cxt">🔖 الباقي بطلب العميل</small>':''}</span><span class="pps"><button class="np" data-pp="${id}:-1"${v<=0?' disabled':''} aria-label="ناقص">−</button><b>${v}<small>/${q}</small></b><button class="np" data-pp="${id}:1"${v>=q?' disabled':''} aria-label="زائد">+</button><button class="np tkf" data-pp="${id}:all"${v>=q?' disabled':''}>✓</button></span></div>`}).join(''):'<p class="em">✓ كل البنود اتجهزت</p>'}</details>`});
 if(!all.length)h+='<p class="em">مفيش بنود في الشهر ده.</p>';return h}
function prepSet(id,dv){const[pid,tid,i]=id.split(':'),p=DB.ph.find(x=>String(x.id)==pid);if(!p)return;const r=(p.rows[tid]||[])[+i];if(!r)return;const q=qn(r),x=+r.x||0,m=rcvSnap(p,[r]);let v=dv=='all'?q:(+r.r||0)+(+dv);v=Math.max(0,Math.min(q,v));if(v<x){v=x;toastT('⚠ مينفعش المستلم يقل عن المتنفذ ('+x+')')}r.r=v;rcvDiff(p,m,'rcv',TD());p.modAt=nowIso();sv();snd(dv=='-1'?'tick':'ok');render()}
// ---------- v3.3: import ----------
function impIdx(z){const n=String(z.no),A=DB.ph.map((y,i)=>[y,i]).filter(([y])=>String(y.no)==n);if(!A.length)return -1;if(z.mo){const e=A.find(([y])=>y.mo==z.mo);return e?e[1]:-1}const c=A.find(([y])=>y.mo==MN());if(c)return c[1];A.sort((a,b)=>String(b[0].mo||'').localeCompare(String(a[0].mo||'')));return A[0][1]}
function impNewer(q){const L=(q.ph||[q]).map(z=>{const i=impIdx(z);if(i<0)return null;const y=DB.ph[i],t=z.modAt||q.at||'';return t&&(y.modAt||'')>t?y:null}).filter(Boolean);return L.length?`\n\n⚠ الصيدليات دي اتعدّلت في التطبيق بعد الملف، والاستبدال هيمسح التعديلات دي: ${L.map(y=>y.no+' ('+fd(y.modAt)+')').join('، ')}`:''}
function impWhere(q){const L=(q.ph||[]).map(z=>{const i=impIdx(z);return z.no+' → '+(i>=0?'شهر '+(DB.ph[i].mo||'—'):'صيدلية جديدة'+(z.mo?' ('+z.mo+')':''))});return L.length&&L.length<=12?'\n'+L.join('\n'):''}
// ---------- v3.3: laptop data ----------
let ST_P=null;
async function stPersist(){if(CAPN()||!navigator.storage||!navigator.storage.persisted)return;let p=await navigator.storage.persisted();if(!p&&navigator.storage.persist)p=await navigator.storage.persist();ST_P=!!p}
function stWarnHtml(){return ST_P===false?'<div class="ywarn">⚠ المتصفح ما وافقش يحفظ بيانات التطبيق بشكل دائم، فممكن يمسحها. اتأكد إن الإعداد ده مقفول: <b>Chrome</b>: Settings ← Privacy and security ← Site data ← «Clear cookies and site data when you close all windows». <b>Edge</b>: Settings ← Privacy ← «Choose what to clear every time you close the browser». وخلي فولدر Drive مربوط علشان البيانات ترجع لوحدها لو اتمسحت.</div>':''}
function stEmpty(){if(document.querySelector('.toast.stem')||(GWEB()&&gdS().on))return;const t=toast((GWEB()?'<span><b>⚠ مفيش بيانات على المتصفح ده.</b><br>اربط حساب Google والتطبيق هيجيب آخر بيانات الموبايل من Drive لوحده، أو استورد نسخة احتياطية.</span><button class="pr" data-gdlogin="1">ربط حساب Google</button>':'<span><b>⚠ مفيش بيانات على المتصفح ده.</b><br>لو كان عندك بيانات قبل كده، غالبًا المتصفح مسحها لما اتقفل. رجّعها من فولدر Drive (بيدمج آخر نسخة من الموبايل لوحده) أو من نسخة احتياطية.</span><button class="pr" data-gddir="1">ربط فولدر درايف</button>')+'<button data-stbk="1">نسخة احتياطية</button><button data-tclose="1">لأ</button>');t.classList.add('rem','stem')}
function v33Click(d,b){
 if(d.xnadd){const o=b.closest('.nmov');if(o)o.remove();xnNew(d.xnadd);return 1}
 if(d.xned||d.xndel){const[k,i]=(d.xned||d.xndel).split('|'),X=DB.cfg.xn||{},L=X[k]||[],n=L[+i];if(n==null)return 1;
  if(d.xndel){if(!confirm('حذف المسمى «'+n+'» من القائمة؟ البنود المسجّلة بيه هتفضل زي ما هي.'))return 1;L.splice(+i,1)}else{let v=prompt('تعديل المسمى (البنود المسجّلة بالاسم القديم هتفضل بيه):',n);if(v==null)return 1;v=v.replace(/\s+/g,' ').trim();if(!v)return 1;L[+i]=v}
  xnApply();sv();render();return 1}
 if(d.ppf!==undefined){V.pf=d.ppf=='*'?'':d.ppf;render();return 1}
 if(d.pp){const a=d.pp.split(':');prepSet(a.slice(0,3).join(':'),a[3]);return 1}
 if(d.whacp){const no=(prompt('رقم الصيدلية اللي هتنسخ بنودها للمخزن:','')||'').trim();if(!no)return 1;const i=impIdx({no}),p=DB.ph[i];if(!p)return alert('مفيش صيدلية بالرقم ده'),1;const W=WHP();W.sh=p.sh;DB.cfg.whsh=p.sh;let n=0;
  TY(W).filter(t=>!WXT.includes(t.id)&&!t.auto).forEach(t=>{(p.rows[t.id]||[]).forEach(r=>{const o={};t.f.forEach(f=>{if(r[f.k]!=null)o[f.k]=r[f.k]});['rsh','od'].forEach(k=>{if(r[k]!=null)o[k]=r[k]});(W.rows[t.id]=W.rows[t.id]||[]).push(o);n++})});whaKeep();render();toastT('✓ اتنسخ '+n+' بند من صيدلية '+p.no+'. عدّل العدد واحذف اللي مش موجود، وبعدين «حفظ في المخزن»');return 1}
 if(d.stbk){const t=b.closest('.toast');if(t)t.remove();goV({v:'bk',op:{},dr:{},q:V.q});return 1}
 return 0}
function v33Change(x){if(x.dataset&&x.dataset.k=='nm'&&x.value=='__xn'){const tid=x.dataset.t;render();xnNew(tid);return 1}
 if(x.id=='ppm'){V.pm=x.value;V.xm=x.value;V.pp='';render();return 1}
 if(x.id=='ppp'){V.pp=x.value?+x.value:'';render();return 1}
 if(x.id=='pph'){V.p0=x.checked;render();return 1}return 0}

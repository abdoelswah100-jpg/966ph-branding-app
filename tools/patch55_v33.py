"""v3.3: custom names (End cap, Floor / Wall Header, End gandola, Medicated) added from the app and managed in «إدارة الأنواع»;
warehouse pulls by real size across shelf types (same type, section, name, size, material) with a warning before using another
shelf type's stock; «قائمة التجهيز» (month / pharmacy list with − + ✓, counted as received, hides completed items);
import: matches pharmacy number + month and warns when a pharmacy changed in the app after the file; laptop: asks the browser
to keep the data, warns and offers recovery when the data is empty; warehouse add: copy the items of a pharmacy."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'xnApply' not in s

# ================= custom names =================
rep("function render(){const a=$('#app');EDTD=false;", "function render(){const a=$('#app');EDTD=false;try{xnApply()}catch(e){console.error(e)}")
rep("${opts(f,d,s).map(o=>`<option${o==d[f.k]?' selected':''}>${esc(o)}</option>`).join('')}</select>",
    "${opts(f,d,s).map(o=>`<option${o==d[f.k]?' selected':''}>${esc(o)}</option>`).join('')}${f.k=='nm'&&XNT.includes(t.id)?'<option value=\"__xn\">➕ مسمى جديد…</option>':''}</select>")
rep("<input class=\"nmq\" placeholder=\"🔍 ابحث بالاسم\" autocomplete=\"off\"><small>${L.length}</small></div>",
    "<input class=\"nmq\" placeholder=\"🔍 ابحث بالاسم\" autocomplete=\"off\"><small>${L.length}</small><button class=\"xnb\" data-xnadd=\"${tid}\">➕ مسمى جديد</button></div>")
rep("<small>يمكنك تعديل أو حذف أي نوع دعاية مضاف. عند الحذف ستُحذف بيانات هذا النوع من الصيدليات والقوالب أيضًا.</small></div>`}",
    "<small>يمكنك تعديل أو حذف أي نوع دعاية مضاف. عند الحذف ستُحذف بيانات هذا النوع من الصيدليات والقوالب أيضًا.</small>${xnMgHtml()}</div>`}")

# ================= warehouse: pull by size across shelf types =================
rep("qty=y=>st?(st[whKey(y)]||0):(+(whFind(whKey(y))||{}).qty||0);", "qty=y=>st?whStQ(st,y):whQty(y);")
rep("function whTake0(p,t,r,L,note){L.M.forEach(y=>{const x=whFind(whKey(y));if(x&&L.nm>0)whAdd(x,-L.nm*y.f,'out','ph:'+p.no,note)});L.K.forEach(y=>{const n=(L.nps||{})[y.pk]||0;if(!n)return;const x=whFind(whKey(y));if(x)whAdd(x,-n,'out','ph:'+p.no,note);",
    "function whTake0(p,t,r,L,note){L.M.forEach(y=>{if(L.nm>0)whTakeQ(y,L.nm*y.f,'ph:'+p.no,note)});L.K.forEach(y=>{const n=(L.nps||{})[y.pk]||0;if(!n)return;whTakeQ(y,n,'ph:'+p.no,note);")
rep("function whAv(p,t,r,sd){const P=whParts(t,r,p.sh),q=y=>+(whFind(whKey(y))||{}).qty||0;", "function whAv(p,t,r,sd){const P=whParts(t,r,p.sh),q=y=>whQty(y);")
rep("if(sd){const y=P.find(z=>z.pk==sd);whAdd(whFind(whKey(y)),-k,'out','ph:'+p.no,note);r['wfp'+sd]=(+r['wfp'+sd]||0)+k}else{P.filter(z=>!z.pk).forEach(y=>whAdd(whFind(whKey(y)),-k*y.f,'out','ph:'+p.no,note));",
    "if(sd){const y=P.find(z=>z.pk==sd);whTakeQ(y,k,'ph:'+p.no,note);r['wfp'+sd]=(+r['wfp'+sd]||0)+k}else{P.filter(z=>!z.pk).forEach(y=>whTakeQ(y,k*y.f,'ph:'+p.no,note));")
# warnings before using another shelf type's stock
rep("txt:`${Math.min(need,L.nm)} ${L.lab||(['eg','md'].includes(t.id)?'هيدر وسايد':'قطعة')} (نفس المقاس)`", "txt:`${Math.min(need,L.nm)} ${L.lab||(['eg','md'].includes(t.id)?'هيدر وسايد':'قطعة')} (نفس المقاس)${whXT(t,r,p.sh,Math.min(need,L.nm))}`")
rep(". تسحبهم للصيدلية؟</span>", ".${whXT(t,r,p.sh,L.nm)} تسحبهم للصيدلية؟</span>")
rep("used.push({tid:t.id,i,n:L.nm,np:L.np,tx:whTxt(L,t),", "used.push({tid:t.id,i,n:L.nm,np:L.np,tx:whTxt(L,t),xw:whXT(t,r,c.sh,L.nm),")
rep("— <b>${esc(u.tx)}</b>", "— <b>${esc(u.tx)}</b>${u.xw?`<b class=\"whxw\">${esc(u.xw)}</b>`:''}")
rep("الزيادة جت من المخزن؟</span>", "الزيادة جت من المخزن؟${C.some(o=>!o.sd&&whXT(o.t,o.r,p.sh,o.e.n))?'<br><b class=\"whxw\">⚠ جزء منها هيتسحب من مخزن نوع رفوف تاني (نفس المقاس)</b>':''}</span>")

# ================= «قائمة التجهيز» =================
rep("const MENU=[['all','التقارير','layers'],", "const MENU=[['all','التقارير','layers'],['prep','قائمة التجهيز','check'],")
rep("const TABOF={gd:'',", "const TABOF={prep:'',gd:'',")
rep("\n if(V.v=='gd'){", "\n if(V.v=='prep'){a.innerHTML=hdr(backBtn(),'قائمة التجهيز')+`<main>${prepHtml()}</main>`;return}\n if(V.v=='gd'){")
rep("<button data-nq=\"r:mo\">نواقص الطباعة — كل الشهر</button></div>", "<button data-nq=\"r:mo\">نواقص الطباعة — كل الشهر</button><button data-mgo=\"prep\">${ic('check')}قائمة التجهيز</button></div>")

# ================= import: number + month, newer-in-app warning =================
rep("if(!confirm(mergePatch?'دمج بيانات إضافية لـ '+q.ph.length+' صيدليات دون استبدال بياناتها الحالية؟':'استيراد '+q.ph.length+' صيدلية؟ الصيدليات بنفس الرقم ستُستبدل'))return;q.ph.forEach(z=>{const i=DB.ph.findIndex(y=>y.no==z.no);",
    "if(!confirm(mergePatch?'دمج بيانات إضافية لـ '+q.ph.length+' صيدليات دون استبدال بياناتها الحالية؟'+impWhere(q):'استيراد '+q.ph.length+' صيدلية؟ الصيدليات بنفس الرقم والشهر ستُستبدل'+impWhere(q)+impNewer(q)))return;q.ph.forEach(z=>{const i=impIdx(z);")
rep("mig(q);const i=DB.ph.findIndex(y=>y.no==q.no);if(i>=0){if(!confirm('يوجد صيدلية بنفس الرقم. استبدالها؟'))return;",
    "mig(q);const i=impIdx(q);if(i>=0){if(!confirm('يوجد صيدلية بنفس الرقم والشهر. استبدالها؟'+impNewer(q)))return;")

# ================= laptop: keep the data =================
rep("async function gdlInit(){if(CAPN())return;", "async function gdlInit(){if(CAPN())return;try{await stPersist()}catch(e){}")
rep("if(!GDH){gdlRemind();return}", "if(!GDH){if(!DB.ph.length)stEmpty();else gdlRemind();return}")
rep(" ${window.showDirectoryPicker?'':'<div class=\"ywarn\">المتصفح ده مايدعمش ربط الفولدر. افتح التطبيق على Chrome أو Edge.</div>'}",
    " ${window.showDirectoryPicker?'':'<div class=\"ywarn\">المتصفح ده مايدعمش ربط الفولدر. افتح التطبيق على Chrome أو Edge.</div>'}${stWarnHtml()}")

# ================= warehouse add: copy a pharmacy's items =================
rep("<button class=\"lnk\" data-whcap=\"1\">إضافة غطاء مسمار ›</button>", "<button class=\"lnk\" data-whacp=\"1\">نسخ بنود صيدلية (وبعدين عدّل العدد) ›</button><button class=\"lnk\" data-whcap=\"1\">إضافة غطاء مسمار ›</button>")

rep("v28Click(d,b)||v29Click(d,b)||v30Click(d,b)||", "v28Click(d,b)||v29Click(d,b)||v30Click(d,b)||v33Click(d,b)||")
rep("v30Change(x)||v32Change(x)||", "v30Change(x)||v32Change(x)||v33Change(x)||")

JS = r"""// ---------- v3.3: custom names ----------
const XNT=['ec','md','fh','wh','eg'];
const XNB={NM:Object.fromEntries(Object.entries(NM).map(([k,v])=>[k,v.slice()])),EC:Object.fromEntries(Object.entries(EC).map(([k,v])=>[k,v.slice()])),EG:EG.slice(),MED:MED.slice()};
function xnApply(){const X=(DB&&DB.cfg&&DB.cfg.xn)||{},set=(a,b,add)=>{a.length=0;b.forEach(v=>a.push(v));(add||[]).forEach(v=>{if(v&&!a.includes(v))a.push(v)})};
 Object.keys(XNB.NM).forEach(k=>set(NM[k],XNB.NM[k],X['nm:'+k]));Object.keys(X).forEach(k=>{if(/^nm:/.test(k)&&!XNB.NM[k.slice(3)])NM[k.slice(3)]=X[k].slice()});
 Object.keys(XNB.EC).forEach(k=>set(EC[k],XNB.EC[k],X['ec:'+k]));set(EG,XNB.EG,X.eg);set(MED,XNB.MED,X.md)}
const xnKey=(tid,d)=>tid=='ec'?'ec:'+d.sec:tid=='eg'?'eg':tid=='md'||(tid=='fh'&&d.sec=='Medicated')?'md':'nm:'+d.sec;
const XNL=k=>k=='eg'?'End gandola':k=='md'?'Medicated':/^ec:/.test(k)?'End cap · '+k.slice(3):'Floor / Wall Header · '+k.slice(3);
function xnNew(tid){const t=T.find(x=>x.id==tid),q=curP(),sh=q?q.sh:0;if(!t)return;const d=draft(t,sh);if(tid=='wh'&&wood(d))return alert('مسميات الخشب ثابتة. غيّر النوع لـ WALL NORMAL الأول.');
 const key=xnKey(tid,d),sp=tid=='eg'?String(d.nm||'Personal · ').split(' · ')[0]:'',ex=tid=='ec'?'Sun care · واقي الشمس':tid=='eg'?'Hair care · عناية بالشعر':key=='md'?'La Roche-Posay':'Sun care';
 let v=prompt(`مسمى جديد لـ ${t.n} · ${tid=='eg'?'قسم '+sp:key=='md'?'Medicated':'قسم '+(d.sec||'')}\nاكتبه بالشكل: ${ex}${tid=='eg'?'\n(لقسم تاني: اختار مسمى من القسم ده الأول)':''}`,'');if(v==null)return;v=v.replace(/\s+/g,' ').trim();if(!v)return;if(tid=='eg'&&!v.startsWith(sp+' · '))v=sp+' · '+v;
 const f=t.f.find(x=>x.k=='nm'),L=opts(f,d,sh),hit=L.find(x=>x.toLowerCase()==v.toLowerCase());if(hit){d.nm=hit;render();return toastT('المسمى ده موجود، واتختار')}
 const X=DB.cfg.xn=DB.cfg.xn||{};(X[key]=X[key]||[]).push(v);xnApply();d.nm=v;sv();render();toastT('✓ اتضاف المسمى: '+v)}
function xnMgHtml(){const X=DB.cfg.xn||{},K=Object.keys(X).filter(k=>(X[k]||[]).length);return `<h3>المسميات المضافة</h3><small>بتتضاف من قائمة «المسمى» ← «➕ مسمى جديد». لو مسحت مسمى، البنود المسجّلة بيه بتفضل زي ما هي.</small><div class="sc"><table><tr><th>القائمة</th><th>المسمى</th><th>الإجراءات</th></tr>${K.length?K.map(k=>X[k].map((n,i)=>`<tr><td>${esc(XNL(k))}</td><td>${esc(n)}</td><td><button data-xned="${esc(k)}|${i}">تعديل</button> <button data-xndel="${esc(k)}|${i}">حذف</button></td></tr>`).join('')).join(''):'<tr><td colspan="3">لا توجد مسميات مضافة</td></tr>'}</table></div>`}
// ---------- v3.3: warehouse by real size, any shelf type ----------
const whKey0=x=>whKey(x).split('|').slice(1).join('|');
function whPool(y){const k0=whKey0(y),ek=whKey(y);return WU().filter(x=>+x.qty>0&&whKey0(x)==k0).sort((a,b)=>(whKey(b)==ek)-(whKey(a)==ek)||(+b.qty)-(+a.qty))}
const whQty=y=>whPool(y).reduce((a,x)=>a+(+x.qty||0),0);
function whStQ(st,y){const k0=whKey0(y);let n=0;Object.keys(st).forEach(k=>{if(k.split('|').slice(1).join('|')==k0)n+=+st[k]||0});return n}
function whTakeQ(y,n,src,note){let left=wq(n);for(const x of whPool(y)){if(left<=1e-9)break;const d=Math.min(left,+x.qty);whAdd(x,-d,'out',src,note+(whKey(x)!=whKey(y)?' (من مخزن '+(x.sh>=0?SH[x.sh]:'بدون نوع رفوف')+')':''));left=wq(left-d)}return wq(n-left)}
function whCross(y,n){const ek=whKey(y),o=[];let left=n;for(const x of whPool(y)){if(left<=1e-9)break;const d=Math.min(left,+x.qty);if(whKey(x)!=ek)o.push(x.sh>=0?SH[x.sh]:'بدون نوع رفوف');left-=d}return o}
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
function stEmpty(){if(document.querySelector('.toast.stem'))return;const t=toast('<span><b>⚠ مفيش بيانات على المتصفح ده.</b><br>لو كان عندك بيانات قبل كده، غالبًا المتصفح مسحها لما اتقفل. رجّعها من فولدر Drive (بيدمج آخر نسخة من الموبايل لوحده) أو من نسخة احتياطية.</span><button class="pr" data-gddir="1">ربط فولدر درايف</button><button data-stbk="1">نسخة احتياطية</button><button data-tclose="1">لأ</button>');t.classList.add('rem','stem')}
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
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
CSS = "\n.xnb{white-space:nowrap}.whxw{display:block;color:var(--rd);font-size:12px}.ppr{display:flex;align-items:center;gap:8px;padding:8px 4px;border-bottom:1px solid var(--bd)}.ppr:last-child{border-bottom:0}.ppn{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.ppt{align-self:flex-start;padding:1px 6px;border-radius:4px;font-size:11px;font-weight:700}.pps{display:flex;align-items:center;gap:4px}.pps button{width:36px;height:36px;padding:0}.pps b{min-width:44px;text-align:center;font-variant-numeric:tabular-nums}.pps b small{font-weight:400;color:var(--mu)}.ppr.tk-ok{opacity:.6}.ppw>summary{display:flex;justify-content:space-between;gap:8px}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
rep("VER='v3.2'", "VER='v3.3'")
rep(" changelog:[{version:'v3.2',", " changelog:[{version:'v3.3',date:'2026-11-07',changes:['New names from the app: «➕ مسمى جديد» in End cap, Floor Header, Wall Header, End gandola and Medicated; edit / delete in «إدارة الأنواع» (items keep their name)','Warehouse pulls by real size across shelf types (same type, section, name, size, material), with a warning before using another shelf type stock','«قائمة التجهيز»: month or pharmacy list with − + ✓ counted as received, hides completed items, filter by ad type','Import matches pharmacy number + month and warns when a pharmacy changed in the app after the file','Laptop: asks the browser to keep the data, explains the clear-on-close setting, offers recovery when the data is empty','Warehouse add: copy the items of a pharmacy, then edit the counts']},{version:'v3.2',")
EN = {'➕ مسمى جديد…':'➕ New name…','➕ مسمى جديد':'➕ New name','المسميات المضافة':'Added names','لا توجد مسميات مضافة':'No added names','القائمة':'List','قائمة التجهيز':'Preparation list','اخفي اللي اكتمل':'Hide completed','نواقص الطباعة — الشهر':'Print shortages — month','✓ كل البنود اتجهزت':'✓ All items prepared','✓ كله اتجهز':'✓ All prepared','الجيوب من شاشة الاستلام':'Pockets from the receiving screen','نسخ بنود صيدلية (وبعدين عدّل العدد) ›':'Copy a pharmacy\'s items (then edit the counts) ›','نسخة احتياطية':'Backup','كل الصيدليات':'All pharmacies'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')

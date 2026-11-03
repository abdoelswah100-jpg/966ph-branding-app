"""v2.7: stamp on shared / reported photos, before / after photo report PDF (per pharmacy and month batch), quality
checklist (optional, score for the supervisor), phone notifications (built-in + own reminders, 11:00), requests / faults log
(convert to a maintenance pharmacy)."""
import os, sys, json
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(R, 'src/app.html')
s = open(P, encoding='utf-8').read()
def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit(f'COUNT {s.count(a)}!={n}: {a[:150]}')
    s = s.replace(a, b)
assert 'stampBlob' not in s

# ---- 1. stamp when sharing
rep("if(b)F.push({b,n:`صيدلية ${p.no} - ${t} ${i+1}.jpg`})", "if(b)F.push({b:await stampBlob(b,stampTxt(p,x)),n:`صيدلية ${p.no} - ${t} ${i+1}.jpg`})")
# ---- 2. photo report button
rep("${phoList(p,'b').length&&phoList(p,'a').length?`<button class=\"pr\" data-phshare=\"ba\">${ic('share')}قبل + بعد</button>`:''}</div>`:''}",
    "${phoList(p,'b').length&&phoList(p,'a').length?`<button class=\"pr\" data-phshare=\"ba\">${ic('share')}قبل + بعد</button>`:''}<button data-phrep=\"1\">${ic('file')}تقرير الصور PDF</button></div>`:''}")
# month batch: report kind
rep("<p class=\"sub\">تقرير تنفيذ للإدارة منفصل لكل صيدلية، كلهم مرة واحدة للمشاركة (واتساب).</p>",
    "<p class=\"sub\">تقرير منفصل لكل صيدلية، كلهم مرة واحدة للمشاركة (واتساب).</p><div class=\"tt\">${[['mg','تقرير الإدارة'],['pho','تقرير صور قبل / بعد']].map(([k,t])=>`<button${(V.mrk||'mg')==k?' class=\"pr\"':''} data-mrbk=\"${k}\">${t}</button>`).join('')}</div>")
rep(" <div class=\"tt\">${[['pdf','PDF'],['xlsx','Excel'],['both','الاتنين']]", " ${V.mrk=='pho'?'<small class=\"hint\">تقرير الصور PDF بس، وللصيدليات اللي فيها صور قبل أو بعد.</small>':''}<div class=\"tt\"${V.mrk=='pho'?' hidden':''}>${[['pdf','PDF'],['xlsx','Excel'],['both','الاتنين']]")
rep("n=L.filter(p=>!X[p.id]).length,nf=n*(f=='both'?2:1);", "n=L.filter(p=>!X[p.id]&&(V.mrk!='pho'||phoHas(p))).length,nf=V.mrk=='pho'?n:n*(f=='both'?2:1);")
rep("async function mrbGo(){const m=V.mrm||V.mo||MN()", "async function mrbGo(){if(V.mrk=='pho')return mrbGoPho();const m=V.mrm||V.mo||MN()")
# ---- 6. quality checklist + 10. request banner in the pharmacy page
rep("${attHtml(p)}${phoHtml(p)}</div>${alBox(p)}", "${attHtml(p)}${phoHtml(p)}${qcHtml(p)}</div>${reqBan(p)}${alBox(p)}")
rep("<div class=\"pc-ft\"><i>${cntRows(p)} بند مسجل</i>", "${qcChip(p)}${reqChip(p)}<div class=\"pc-ft\"><i>${cntRows(p)} بند مسجل</i>")
rep("<div class=\"wcard\"><h2>${ic('gear')}الإعدادات العامة</h2>", "<div class=\"wcard\"><h2>${ic('gear')}الإعدادات العامة</h2><label>أسئلة فحص الجودة (سطر لكل سؤال، فاضي = الأسئلة الجاهزة)<textarea id=\"cfqc\" rows=\"5\">${esc(QCQ().join('\\n'))}</textarea></label>")
rep("const PHEDIT=['tcx',", "const PHEDIT=['qc','tcx',")
# ---- menu, screens, dispatchers, storage, backups
rep("const MENU=[['all','التقارير','layers'],", "const MENU=[['all','التقارير','layers'],['req','الطلبات والأعطال','list'],['ntf','إدارة التنبيهات','bell'],")
rep("const ICN={inbox:", "const ICN={bell:'<path d=\"M18 8a6 6 0 0 0-12 0c0 7-3 9-3 9h18s-3-2-3-9\"/><path d=\"M13.7 21a2 2 0 0 1-3.4 0\"/>',inbox:")
rep("const TABOF={rte:'home',", "const TABOF={req:'',reqe:'',ntf:'',rte:'home',")
rep("\n if(V.v=='rte'){", "\n if(V.v=='req'){a.innerHTML=hdr(backBtn(),'🛠 الطلبات والأعطال')+`<main>${uStoreBar()}${reqHtml()}</main>`;return}\n if(V.v=='reqe'){a.innerHTML=hdr('<button data-rqx=\"1\">‹ الطلبات</button>',V.re&&V.re._new?'طلب جديد':'تعديل طلب')+`<main>${reqeHtml()}</main>`;return}\n if(V.v=='ntf'){a.innerHTML=hdr(backBtn(),'🔔 إدارة التنبيهات')+`<main>${ntfHtml()}</main>`;return}\n if(V.v=='rte'){")
rep("v21Click(d,b)||v23Click(d,b)||v24Click(d,b)||v26Click(d,b)||", "v21Click(d,b)||v23Click(d,b)||v24Click(d,b)||v26Click(d,b)||v27Click(d,b)||")
rep("x15Change(x)||rcvChange(x)||v21Change(x)||v24Change(x)||v25Change(x)||", "x15Change(x)||rcvChange(x)||v21Change(x)||v24Change(x)||v25Change(x)||v27Change(x)||")
rep("const UST=['cust','mnt','wh','wlog','invs','qi','rcvq']", "const UST=['cust','mnt','wh','wlog','invs','qi','rcvq','req']")
rep("const STEDIT=['whcap',", "const STEDIT=['rqsave','rqdel','rqmnt','rqst','rqphx','whcap',")
rep("const sv=()=>{try{try{mntAuto()}catch(e){console.error(e)}", "const sv=()=>{try{try{mntAuto()}catch(e){console.error(e)}try{reqAuto()}catch(e){console.error(e)}try{ntfLater()}catch(e){}")
rep("for(const p of DB.ph)for(const sl of ['b','a','o'])for(const x of phoList(p,sl)){const k=phoKey(p.id,sl,x.k),b=await idbGet(k);if(b)photos[k]=await r2u(b)}",
    "for(const p of DB.ph)for(const sl of ['b','a','o'])for(const x of phoList(p,sl)){const k=phoKey(p.id,sl,x.k),b=await idbGet(k);if(b)photos[k]=await r2u(b)}for(const r of (DB.req||[]))for(const x of (r.ph||[])){const k=rqKey(r.id,x.k),b=await idbGet(k);if(b)photos[k]=await r2u(b)}")
# notifications plugin start
rep("setTimeout(autoBackup,2500)}", "setTimeout(autoBackup,2500);setTimeout(ntfInit,3500)}")

JS = r"""// ---------- v2.7: stamp, photo report, quality checklist, notifications, requests ----------
const z2n=n=>String(n).padStart(2,'0');
function stampTxt(p,x){const d=x&&x.at?new Date(x.at):new Date();return `${PL(p)}${p.name?' · '+p.name:''} · ${z2n(d.getDate())}-${z2n(d.getMonth()+1)}-${d.getFullYear()} ${z2n(d.getHours())}:${z2n(d.getMinutes())}`}
async function stampBlob(b,t){const u=URL.createObjectURL(b);try{const im=await new Promise((ok,no)=>{const i=new Image();i.onload=()=>ok(i);i.onerror=no;i.src=u});const W=im.naturalWidth,H=im.naturalHeight,c=document.createElement('canvas');c.width=W;c.height=H;const x=c.getContext('2d');x.drawImage(im,0,0);
 const fs=Math.max(14,Math.round(Math.min(W,H*1.6)/34)),bh=Math.round(fs*1.9);x.fillStyle='rgba(0,0,0,.55)';x.fillRect(0,H-bh,W,bh);x.fillStyle='#fff';x.font=`600 ${fs}px sans-serif`;x.textBaseline='middle';try{x.direction='rtl'}catch(e){}x.textAlign='right';x.fillText(t,W-Math.round(fs*.7),H-bh/2,W-fs*1.4);
 return await new Promise(ok=>c.toBlob(bb=>ok(bb||b),'image/jpeg',.88))}catch(e){return b}finally{URL.revokeObjectURL(u)}}
const phoHas=p=>phoList(p,'b').length+phoList(p,'a').length>0;
async function phoImg(p,sl,x){const b=await idbGet(phoKey(p.id,sl,x.k));if(!b)return '';const s2=await stampBlob(b,stampTxt(p,x)),u=URL.createObjectURL(s2),d=await shrink(u,900);URL.revokeObjectURL(u);if(!d)return '';const im=await new Promise(ok=>{const i=new Image();i.onload=()=>ok(i);i.onerror=()=>ok(null);i.src=d});return im?`<img src="${d}" width="${im.naturalWidth}" height="${im.naturalHeight}" alt="">`:''}
async function phoRepEl(p){const el=document.createElement('div'),B=phoList(p,'b'),A=phoList(p,'a'),O=phoList(p,'o'),ddv=d=>d?d.split('-').reverse().join('-'):'—';
 let h=`<div class="cpt"><b>صور قبل / بعد التنفيذ — ${PL(p)}</b><small>${esc(p.name||'')}${p.name?' · ':''}${esc(RL(p))} · ${SH[p.sh]||''} · ${esc(p.mod||'')} · ${esc(p.st||'')} · البدء ${ddv(p.ds)} · الانتهاء ${ddv(p.de)}</small></div>`;
 const n=Math.min(B.length,A.length);if(n)h+=`<div class="phpair phhd"><b>قبل</b><b>بعد</b></div>`;
 for(let i=0;i<n;i++)h+=`<div class="phpair"><div>${await phoImg(p,'b',B[i])}</div><div>${await phoImg(p,'a',A[i])}</div></div>`;
 const rest=async(L,sl,t)=>{if(L.length<=n)return '';let r=`<h3>${t}</h3>`;for(let i=n;i<L.length;i+=2)r+=`<div class="phpair"><div>${await phoImg(p,sl,L[i])}</div><div>${L[i+1]?await phoImg(p,sl,L[i+1]):''}</div></div>`;return r};
 h+=await rest(B,'b',n?'صور قبل إضافية':'صور قبل');h+=await rest(A,'a',n?'صور بعد إضافية':'صور بعد');
 if(O.length){h+='<h3>صور التصميم القديم</h3>';for(let i=0;i<O.length;i+=2)h+=`<div class="phpair"><div>${await phoImg(p,'o',O[i])}</div><div>${O[i+1]?await phoImg(p,'o',O[i+1]):''}</div></div>`}
 el.innerHTML=h;return el}
async function phoRepPdf(p){if(!phoHas(p)&&!phoList(p,'o').length)return alert('مفيش صور للصيدلية دي');const t=toast('جاري تجهيز تقرير الصور…');let el;try{el=await phoRepEl(p)}finally{t.remove()}return sharePdf({src:el,name:'صور قبل وبعد - صيدلية '+p.no,title:'صور قبل / بعد — '+PL(p)})}
async function mrbGoPho(){const m=V.mrm||V.mo||MN(),X=V.mrx||{},L=DB.ph.filter(p=>p.mo==m&&isBr(p)&&!X[p.id]&&phoHas(p)).sort(pSort);if(!L.length)return alert('مفيش صيدليات فيها صور في الشهر ده');
 const t=toast('جاري تجهيز تقارير الصور… 0 / '+L.length),F=[];try{for(let i=0;i<L.length;i++){const p=L[i],el=await phoRepEl(p),b=await buildPdf(el,'صور قبل / بعد — '+PL(p));F.push(new File([b],'صور قبل وبعد - صيدلية '+p.no+' - '+mLab(m)+'.pdf',{type:'application/pdf'}));t.innerHTML='جاري تجهيز تقارير الصور… '+(i+1)+' / '+L.length}}catch(e){console.error(e);t.remove();alert('تعذّر تجهيز التقارير على الجهاز ده');return}
 t.remove();window._mrbF=F;await shareFiles(F,'صور قبل وبعد التنفيذ — شهر '+mLab(m)+' — '+L.length+' صيدلية')}
// quality checklist (optional, the score stays with the supervisor)
const QCD=['الستيكر من غير فقاعات أو تجاعيد','الحروف في نص التخطيط ومستقيمة','الهيدرات مقاسها مظبوط ومثبتة كويس','الألوان والمسميات مطابقة للمطلوب','المكان نضيف بعد الشغل','مفيش بنود ناقصة'];
const QCQ=()=>Array.isArray(DB.cfg.qcq)&&DB.cfg.qcq.length?DB.cfg.qcq:QCD;
function qcScore(p){const a=(p.qc||{}).a||{};let y=0,n=0;QCQ().forEach(q=>{if(a[q]=='y')y++;else if(a[q]=='n')n++});return{y,n,pc:y+n?Math.round(100*y/(y+n)):null}}
function qcHtml(p){const S=qcScore(p),a=(p.qc||{}).a||{},nt=(p.qc||{}).nt||{};return `<details class="pinfo" data-id="__qc"${V.op.__qc?' open':''}><summary>✅ فحص الجودة${S.pc!=null?` (${S.y}/${S.y+S.n} · ${S.pc}%)`:''}</summary>${QCQ().map((q,i)=>`<div class="qcr"><span>${esc(q)}</span><div class="qcb">${[['y','✓'],['n','✗'],['na','لا ينطبق']].map(([v,t])=>`<button class="${a[q]==v?(v=='n'?'qcn':'pr'):''}" data-qc="${i}:${v}">${t}</button>`).join('')}</div>${a[q]=='n'?`<input class="qcnt" data-qcn="${i}" placeholder="ملاحظة (إيه الغلط؟)" value="${esc(nt[q]||'')}">`:''}</div>`).join('')}<small class="hint">اختياري. الدرجة ليك انت بس ومش بتظهر في أي تقرير. الأسئلة بتتعدّل من الإعدادات العامة.</small></details>`}
const qcChip=p=>{const S=qcScore(p);return S.pc!=null?`<div class="pc-ln">✅ الجودة: <b style="color:${S.pc>=90?'#2E8B57':S.pc>=70?'#D98A1D':'#C7313B'}">${S.pc}%</b></div>`:''};
// requests / faults
const RQS=()=>(DB.req=DB.req||[]),RQBY=['الصيدلية','الإدارة','زيارة'],RQST=['جديد','اتجدول','اتعمل'],RQPR=['عادي','مستعجل'],rqKey=(id,k)=>'pho:rq:'+id+':'+k;
const rqOpen=r=>r.st!='اتعمل',rqOf=no=>RQS().filter(r=>String(r.no).trim()==String(no||'').trim());
const reqChip=p=>{const n=rqOf(p.no).filter(rqOpen).length;return n?`<div class="pc-ln">🛠 <b>${n}</b> طلب مفتوح</div>`:''};
const reqBan=p=>{const L=rqOf(p.no).filter(r=>rqOpen(r)||r.mph==p.id);return L.length?`<div class="ywarn">🛠 ${L.map(r=>`<button class="lnk" data-rqed="${r.id}">${esc(r.det||r.ad||'طلب')} · ${esc(r.st)}${r.pr=='مستعجل'?' · مستعجل':''}</button>`).join(' ')}</div>`:''};
function reqAuto(){RQS().forEach(r=>{if(r.mph&&r.st!='اتعمل'){const p=DB.ph.find(x=>x.id==r.mph);if(p&&p.st=='مكتملة'){r.st='اتعمل';r.done=p.de||TD();r.at=nowIso()}}})}
function reqHtml(){const f=V.rqf||'open',L=RQS().filter(r=>f=='all'||(f=='open'?rqOpen(r):!rqOpen(r))).sort((a,b)=>(b.pr=='مستعجل')-(a.pr=='مستعجل')||String(b.dt).localeCompare(String(a.dt))),no=RQS().filter(rqOpen).length;
 return `<div class="wcard"><h2>🛠 الطلبات والأعطال</h2><p class="sub">أي طلب أو عطل من الصيدلية أو الإدارة أو في زيارة. «حوّل لصيانة» بيعمل صيدلية صيانة، ولما تتقفل الطلب بيبقى «اتعمل» لوحده.</p><div class="tt"><button class="pr big" data-rqnew="1">${ic('add')}طلب جديد</button></div><div class="rtchips">${[['open','مفتوحة ('+no+')'],['done','اتعملت'],['all','الكل']].map(([k,t])=>`<button class="${f==k?'pr':''}" data-rqf="${k}">${t}</button>`).join('')}</div></div>
 ${L.length?L.map(r=>`<button class="wcard rqc${r.pr=='مستعجل'?' rqu':''}" data-rqed="${r.id}"><div class="rqh"><b>صيدلية ${esc(r.no)}</b><i class="pill" style="background:${r.st=='اتعمل'?'#2E8B57':r.st=='اتجدول'?'#2F6FD0':'#D98A1D'}">${esc(r.st)}</i></div><small>${ddm(r.dt)} · ${esc(r.by||'')}${r.ad?' · '+esc(r.ad):''}${r.pr=='مستعجل'?' · <b style="color:var(--rd)">مستعجل</b>':''}${(r.ph||[]).length?' · 📷 '+r.ph.length:''}</small><div>${esc(r.det||'')}</div></button>`).join(''):'<p class="em">مفيش طلبات هنا.</p>'}`}
function reqeHtml(){const r=V.re;if(!r)return '';const nos=[...new Set(DB.ph.map(x=>String(x.no||'').trim()).filter(Boolean))],ads=[...new Set(T.filter(t=>!t.auto).map(t=>t.n))].concat(['أخرى']),sel=(k,L)=>`<select data-rqv="${k}">${L.map(x=>`<option${r[k]==x?' selected':''}>${esc(x)}</option>`).join('')}</select>`;
 return `<div class="wcard"><div class="c2"><label>رقم الصيدلية<input data-rqv="no" list="rqnol" inputmode="numeric" value="${esc(r.no||'')}"></label><label>التاريخ<input type="date" data-rqv="dt" value="${r.dt||TD()}"></label></div><datalist id="rqnol">${nos.map(x=>`<option value="${esc(x)}">`).join('')}</datalist>
 <div class="c2"><label>مين طلب${sel('by',RQBY)}</label><label>البند${sel('ad',ads)}</label></div>
 <label>وصف المشكلة / الطلب<textarea data-rqv="det" rows="3">${esc(r.det||'')}</textarea></label>
 <div class="c2"><label>الأولوية${sel('pr',RQPR)}</label><label>الحالة${sel('st',RQST)}</label></div>
 <div class="phb"><div class="phh"><b>صور</b><small>${(r.ph||[]).length}</small></div>${(r.ph||[]).length?`<div class="phg">${r.ph.map(x=>`<span class="pht"><img data-pho="${rqKey(r.id,x.k)}" alt=""><button class="phx" data-rqphx="${x.k}" aria-label="حذف">×</button></span>`).join('')}</div>`:''}<div class="tt"><button data-rqcam="1">${ic('cam')}كاميرا</button><button data-rqgal="1">${ic('img')}من الاستوديو</button></div><input type="file" id="rqin" accept="image/*" hidden></div>
 ${r.mph?`<small class="hint">اتحوّل لصيدلية صيانة. <button class="lnk" data-rqgo="${r.mph}">افتحها ›</button></small>`:''}
 <div class="tt"><button class="pr big" data-rqsave="1">${ic('check')}حفظ</button>${!r._new&&!r.mph?`<button data-rqmnt="1">🔧 حوّل لصيانة</button>`:''}${!r._new?`<button data-rqdel="1" style="color:var(--rd)">${ic('trash')}مسح</button>`:''}</div></div>`}
async function rqAddPh(files){const r=V.re;if(!r)return;let n=0;for(const f of [...files]){const u=b2u(f,f.type),d=await shrink(u,1280);URL.revokeObjectURL(u);if(!d)continue;const b=await (await fetch(d)).blob(),k=rid();if(await idbSet(rqKey(r.id,k),b)){(r.ph=r.ph||[]).push({k,at:nowIso()});n++}}if(n){const o=RQS().find(x=>x.id==r.id);if(o){o.ph=r.ph;svq()}}render()}
function rqToMnt(r){const base=DB.ph.filter(p=>String(p.no).trim()==String(r.no).trim()).sort((a,b)=>String(b.mo||'').localeCompare(String(a.mo||'')))[0]||{};
 const p={id:Date.now(),no:String(r.no).trim(),loc:base.loc||'',locc:base.locc,locs:base.locs,rg:base.rg||RG[0],ct:base.ct||'',name:base.name||'',mod:'صيانة',sup:base.sup||DB.cfg.dsup||'عبدالله السواح',co:base.co||DB.cfg.dco||'عمال الشركة',ds:TD(),de:'',sh:base.sh!=null?base.sh:0,mo:MN(),st:'لم تبدأ',rows:{},m1:1,m20:1,m22:1,m23:1,capx:0,modAt:nowIso(),rqid:r.id};
 DB.ph.push(p);r.mph=p.id;if(r.st=='جديد')r.st='اتجدول';r.at=nowIso();return p}
// notifications (phone app): built-in alerts at a set time + own reminders
const NTD={on:{due:1,stall:1,low:1,bk:1,cust:1},tm:'11:00',sd:3,list:[]};
const NTF=()=>{const c=DB.cfg.ntf=Object.assign({},NTD,DB.cfg.ntf||{});c.on=Object.assign({},NTD.on,c.on||{});c.list=c.list||[];return c};
const NTL={due:'ميعاد انتهاء الصيدليات (بكرة / النهارده / فات)',stall:'صيدلية واقفة من غير تعديل',low:'صنف في المخزن وصل للحد الأدنى',bk:'نسخة احتياطية ما اتعملتش بقالها أسبوع',cust:'العهدة المتبقي أقل من الحد'};
const LN=()=>CP('LocalNotifications');
const nid=s=>{let h=0;for(const c of String(s))h=(h*31+c.charCodeAt(0))|0;return Math.abs(h)%2000000000+1};
const atDay=(d,tm)=>{const[h,m]=String(tm||'11:00').split(':').map(Number);const x=new Date(d);x.setHours(h||0,m||0,0,0);return x};
const nextAt=(from,tm)=>{let x=atDay(from,tm);if(x<=new Date())x=atDay(new Date(Date.now()+864e5),tm);const n=atDay(new Date(),tm);if(x<n)x=n>new Date()?n:atDay(new Date(Date.now()+864e5),tm);return x};
function ntfNow(){const c=NTF(),o=[],td=TD(),tm=c.tm;
 if(c.on.due)DB.ph.forEach(p=>{if(p.st=='مكتملة'||!p.de)return;const d=Math.round((new Date(p.de)-new Date(td))/864e5);if(d<=1)o.push({k:'due',p,t:d<0?'فات ميعاد صيدلية '+p.no:d==0?'النهارده آخر يوم لصيدلية '+p.no:'بكرة آخر يوم لصيدلية '+p.no})});
 if(c.on.stall)DB.ph.forEach(p=>{if(p.st=='مكتملة'||!p.modAt)return;const d=Math.floor((Date.now()-new Date(p.modAt))/864e5);if(d>=c.sd)o.push({k:'stall',p,t:'صيدلية '+p.no+' واقفة من غير تعديل بقالها '+d+' يوم'})});
 if(c.on.low)WU().forEach(x=>{if(x.min!==''&&x.min!=null&&+x.qty<=+x.min)o.push({k:'low',t:'المخزن: '+x.ty+(x.nm?' · '+x.nm:'')+' رصيده '+wq(x.qty)+' (الحد '+x.min+')'})});
 if(c.on.bk&&dayDiff(DB.cfg.lb)>=7)o.push({k:'bk',t:'ما عملتش نسخة احتياطية بقالك '+(dayDiff(DB.cfg.lb)>900?'فترة طويلة':dayDiff(DB.cfg.lb)+' يوم')});
 if(c.on.cust){try{const M=cMo(),lim=cAl();if(M&&lim){const rem=M.open-cTot(M);if(rem<lim)o.push({k:'cust',t:'العهدة: المتبقي '+Math.round(rem)+' ريال أقل من '+lim})}}catch(e){}}
 return o}
function ntfPlan(){const c=NTF(),o=[],tm=c.tm,now=new Date(),lim=Date.now()+30*864e5,add=(key,title,body,at,extra)=>{if(at&&at>now&&+at<lim)o.push({id:nid(key),title,body,schedule:{at,allowWhileIdle:true},extra:extra||{},channelId:'ph966'})};
 if(c.on.due)DB.ph.forEach(p=>{if(p.st=='مكتملة'||!p.de)return;const d0=new Date(p.de);[[-1,'بكرة آخر يوم'],[0,'النهارده آخر يوم'],[1,'فات ميعاد']].forEach(([k,t])=>add('due:'+p.id+':'+k,'📅 '+t,'صيدلية '+p.no+(p.name?' ('+p.name+')':'')+' — الحالة '+(p.st||''),atDay(new Date(+d0+k*864e5),tm),{pid:p.id}))});
 if(c.on.stall)DB.ph.forEach(p=>{if(p.st=='مكتملة'||!p.modAt)return;const t=new Date(+new Date(p.modAt)+c.sd*864e5);add('stall:'+p.id,'⏸ صيدلية واقفة','صيدلية '+p.no+' من غير أي تعديل بقالها '+c.sd+' أيام',nextAt(t,tm),{pid:p.id})});
 if(c.on.bk){const t=DB.cfg.lb?new Date(+new Date(DB.cfg.lb)+7*864e5):new Date();add('bk','💾 نسخة احتياطية','بقالك أسبوع من غير نسخة احتياطية. اعمل واحدة واحفظها على Drive.',nextAt(t,tm),{v:'bk'})}
 const ev=ntfNow().filter(x=>x.k=='low'||x.k=='cust'),sent=DB.cfg.ntfs||{},keep={};ev.forEach(x=>{const k=x.k+':'+x.t.replace(/[\d.]+/g,'');keep[k]=1;if(!sent[k])add('ev:'+k+':'+Date.now(),x.k=='low'?'📦 المخزن':'💰 العهدة',x.t,new Date(Date.now()+3000),{v:x.k=='low'?'wh':'cust'})});DB.cfg.ntfs=keep;
 c.list.forEach(r=>{if(!r.on)return;const[h,m]=String(r.tm||tm).split(':').map(Number),b={id:nid('c:'+r.id),title:'🔔 '+(r.ti||'تذكير'),body:r.tx||'',extra:{},channelId:'ph966'};
  if(r.rp=='day')o.push(Object.assign(b,{schedule:{on:{hour:h,minute:m},allowWhileIdle:true}}));else if(r.rp=='week'){const wd=new Date(r.dt||TD()).getDay()+1;o.push(Object.assign(b,{schedule:{on:{weekday:wd,hour:h,minute:m},allowWhileIdle:true}}))}
  else if(r.rp=='month'){const dd=new Date(r.dt||TD()).getDate();o.push(Object.assign(b,{schedule:{on:{day:dd,hour:h,minute:m},allowWhileIdle:true}}))}else{const at=atDay(new Date(r.dt||TD()),r.tm||tm);if(at>now)o.push(Object.assign(b,{schedule:{at,allowWhileIdle:true}}))}});
 return o}
let NTFT=null,NTFOK=0;
async function ntfInit(){const L=LN();if(!L)return;try{if(L.createChannel)await L.createChannel({id:'ph966',name:'تنبيهات 966Ph',importance:4,visibility:1}).catch(()=>{});L.addListener('localNotificationActionPerformed',e=>{const x=(e&&e.notification&&e.notification.extra)||{};if(x.pid&&DB.ph.some(p=>p.id==x.pid))goV({v:'ph',p:x.pid,op:{},dr:{},q:V.q});else if(x.v)goV({v:x.v,op:{},dr:{},q:V.q})});
 let st=await L.checkPermissions();if(st.display!='granted'&&!DB.cfg.ntfAsk){DB.cfg.ntfAsk=1;svq();st=await L.requestPermissions()}NTFOK=st.display=='granted';if(NTFOK)ntfSync()}catch(e){console.warn(e)}}
function ntfLater(){if(!LN())return;clearTimeout(NTFT);NTFT=setTimeout(ntfSync,4000)}
async function ntfSync(){const L=LN();if(!L)return 0;try{const st=await L.checkPermissions();NTFOK=st.display=='granted';if(!NTFOK)return 0;const P=await L.getPending();if(P&&P.notifications&&P.notifications.length)await L.cancel({notifications:P.notifications.map(n=>({id:n.id}))});const N=ntfPlan();if(N.length)await L.schedule({notifications:N.slice(0,60)});return N.length}catch(e){console.warn(e);return 0}}
async function ntfNowSend(title,body,extra){const L=LN();if(!L||!NTFOK)return;try{await L.schedule({notifications:[{id:nid('now:'+Date.now()),title,body,schedule:{at:new Date(Date.now()+1500),allowWhileIdle:true},extra:extra||{},channelId:'ph966'}]})}catch(e){}}
function ntfHtml(){const c=NTF(),N=ntfNow(),nat=!!LN(),e=V.ne;
 return `${nat?'':'<div class="ywarn">التنبيهات بتوصل على تطبيق الموبايل بس. هنا تقدر تظبط الإعدادات وتشوف التنبيهات الحالية، وبتتنقل للموبايل بالنسخة الاحتياطية أو المزامنة.</div>'}
 <div class="wcard"><h3>التنبيهات الحالية (${N.length})</h3>${N.length?N.map(x=>`<div class="ntr">${x.p?`<button class="lnk" data-rqgo="${x.p.id}">${esc(x.t)} ›</button>`:esc(x.t)}</div>`).join(''):'<small>مفيش تنبيهات دلوقتي ✓</small>'}</div>
 <div class="wcard"><h3>التنبيهات التلقائية</h3><label>الساعة<input type="time" id="ntftm" value="${esc(c.tm)}"></label>${Object.keys(NTL).map(k=>`<label class="chk"><input type="checkbox" data-ntfon="${k}"${c.on[k]?' checked':''}> ${NTL[k]}</label>`).join('')}<label>الصيدلية تعتبر واقفة بعد (يوم)<input type="number" inputmode="numeric" min="1" id="ntfsd" value="${c.sd}"></label>
 ${nat?`<div class="tt"><button data-ntfperm="1">${NTFOK?'✓ الإشعارات مسموحة':'السماح بالإشعارات'}</button><button data-ntftest="1">🔔 تجربة إشعار</button></div>`:''}</div>
 <div class="wcard"><h3>تنبيهاتي (${c.list.length})</h3>${c.list.map(r=>`<div class="ntr"><label class="chk" style="flex:1"><input type="checkbox" data-ntfc="${r.id}"${r.on?' checked':''}> <b>${esc(r.ti||'تذكير')}</b> <small>${esc(r.tx||'')} · ${{'':'مرة واحدة',day:'كل يوم',week:'كل أسبوع',month:'كل شهر'}[r.rp||'']} · ${r.rp?'':ddm(r.dt)+' '}${esc(r.tm||c.tm)}</small></label><button class="np" data-ntfe="${r.id}">✎</button><button class="np" data-ntfd="${r.id}">✕</button></div>`).join('')||'<small>لسه مفيش.</small>'}
 ${e?`<div class="fm"><label>العنوان<input data-nev="ti" value="${esc(e.ti||'')}" placeholder="مثال: مراجعة المخزن"></label><label>الرسالة<input data-nev="tx" value="${esc(e.tx||'')}"></label><div class="c2"><label>التاريخ<input type="date" data-nev="dt" value="${e.dt||TD()}"></label><label>الساعة<input type="time" data-nev="tm" value="${esc(e.tm||c.tm)}"></label></div><label>التكرار<select data-nev="rp">${[['','مرة واحدة'],['day','كل يوم'],['week','كل أسبوع (نفس اليوم)'],['month','كل شهر (نفس التاريخ)']].map(([v,t])=>`<option value="${v}"${(e.rp||'')==v?' selected':''}>${t}</option>`).join('')}</select></label><div class="tt"><button class="pr" data-ntfsave="1">حفظ التنبيه</button><button data-ntfx="1">إلغاء</button></div></div>`:`<div class="tt"><button class="pr" data-ntfadd="1">${ic('add')}تنبيه جديد</button></div>`}</div>`}
function v27Click(d,b){
 if(d.phrep){const p=curP();if(p)phoRepPdf(p);return 1}
 if(d.mrbk){V.mrk=d.mrbk;render();return 1}
 if(d.qc){const p=curP(),[i,v]=d.qc.split(':'),q=QCQ()[+i];if(!p||q==null)return 1;p.qc=p.qc||{a:{},nt:{}};p.qc.a=p.qc.a||{};if(p.qc.a[q]==v)delete p.qc.a[q];else p.qc.a[q]=v;p.qc.at=nowIso();sv();render();return 1}
 if(d.rqf){V.rqf=d.rqf;render();return 1}
 if(d.rqnew){V.re={id:rid(),_new:1,no:'',dt:TD(),by:RQBY[0],ad:'أخرى',det:'',pr:RQPR[0],st:RQST[0],ph:[]};goV(Object.assign({},V,{v:'reqe'}));return 1}
 if(d.rqed){const r=RQS().find(x=>x.id==d.rqed);if(r){V.re=JSON.parse(JSON.stringify(r));goV(Object.assign({},V,{v:'reqe',bkv:V.v,bkp:V.p}))}return 1}
 if(d.rqx){if(V.re&&V.re._new)(V.re.ph||[]).forEach(x=>idbSet(rqKey(V.re.id,x.k),null));goV(Object.assign({},V,{v:V.bkv=='ph'?'ph':'req',p:V.bkp||V.p}));return 1}
 if(d.rqsave){const r=V.re;if(!r)return 1;if(!String(r.no||'').trim())return alert('اكتب رقم الصيدلية'),1;const nw=!!r._new;delete r._new;r.at=nowIso();const i=RQS().findIndex(x=>x.id==r.id);if(i>=0)RQS()[i]=r;else RQS().push(r);sv();snd('ok');if(nw&&r.pr=='مستعجل')ntfNowSend('🛠 طلب مستعجل','صيدلية '+r.no+': '+(r.det||r.ad||''),{v:'req'});goV(Object.assign({},V,{v:'req'}));toastT('✓ اتحفظ الطلب');return 1}
 if(d.rqdel){const r=V.re;if(!r||!confirm('تمسح الطلب ده؟'))return 1;(r.ph||[]).forEach(x=>idbSet(rqKey(r.id,x.k),null));DB.req=RQS().filter(x=>x.id!=r.id);sv();goV(Object.assign({},V,{v:'req'}));return 1}
 if(d.rqmnt){const r0=V.re,r=RQS().find(x=>x.id==r0.id);if(!r)return 1;Object.assign(r,r0);if(!confirm('هتتعمل صيدلية صيانة رقم '+r.no+' في الشهر الحالي، وتضيف فيها البنود. تكمل؟'))return 1;const p=rqToMnt(r);sv();goV({v:'ph',p:p.id,op:{},dr:{},q:V.q});toastT('🔧 اتعملت صيدلية صيانة '+p.no+'. ضيف البند المطلوب');return 1}
 if(d.rqgo){const id=+d.rqgo;if(DB.ph.some(p=>p.id==id))goV({v:'ph',p:id,op:{},dr:{},q:V.q});return 1}
 if(d.rqcam||d.rqgal){const i=$('#rqin');if(!i)return 1;if(d.rqcam){i.setAttribute('capture','environment');i.removeAttribute('multiple')}else{i.removeAttribute('capture');i.setAttribute('multiple','')}i.click();return 1}
 if(d.rqphx){const r=V.re;if(!r)return 1;idbSet(rqKey(r.id,d.rqphx),null);r.ph=(r.ph||[]).filter(x=>x.k!=d.rqphx);const o=RQS().find(x=>x.id==r.id);if(o){o.ph=r.ph;svq()}render();return 1}
 if(d.ntfperm){const L=LN();if(L)L.requestPermissions().then(st=>{NTFOK=st.display=='granted';if(NTFOK)ntfSync();render()});return 1}
 if(d.ntftest){ntfNowSend('🔔 تجربة','التنبيهات شغالة ✓');toastT(NTFOK?'هيوصلك إشعار تجربة دلوقتي':'اسمح بالإشعارات الأول');return 1}
 if(d.ntfadd){V.ne={id:rid(),on:1,ti:'',tx:'',dt:TD(),tm:NTF().tm,rp:''};render();return 1}
 if(d.ntfe){const r=NTF().list.find(x=>x.id==d.ntfe);if(r){V.ne=Object.assign({},r);render()}return 1}
 if(d.ntfx){V.ne=null;render();return 1}
 if(d.ntfsave){const e=V.ne,c=NTF();if(!e)return 1;if(!String(e.ti||'').trim())return alert('اكتب عنوان التنبيه'),1;const i=c.list.findIndex(x=>x.id==e.id);if(i>=0)c.list[i]=e;else c.list.push(e);V.ne=null;svq();ntfLater();render();toastT('✓ اتحفظ التنبيه');return 1}
 if(d.ntfd){const c=NTF();if(!confirm('تمسح التنبيه ده؟'))return 1;c.list=c.list.filter(x=>x.id!=d.ntfd);svq();ntfLater();render();return 1}
 return 0}
function v27Change(x){
 if(x.dataset&&x.dataset.qcn!=null){const p=curP(),q=QCQ()[+x.dataset.qcn];if(p&&q!=null){p.qc=p.qc||{a:{},nt:{}};p.qc.nt=p.qc.nt||{};p.qc.nt[q]=x.value.trim();sv()}return 1}
 if(x.id=='cfqc'){const L=x.value.split('\n').map(s=>s.trim()).filter(Boolean);if(L.length&&L.join('|')!=QCD.join('|'))DB.cfg.qcq=L;else delete DB.cfg.qcq;svq();toastT('✓ اتحفظت أسئلة فحص الجودة');return 1}
 if(x.dataset&&x.dataset.rqv){const r=V.re;if(r){r[x.dataset.rqv]=x.value;if(x.dataset.rqv!='det'&&x.dataset.rqv!='no')render()}return 1}
 if(x.id=='rqin'){const f=x.files;if(f&&f.length)rqAddPh(f).then(()=>{x.value=''});return 1}
 if(x.id=='ntftm'){NTF().tm=x.value||'11:00';svq();ntfLater();return 1}
 if(x.id=='ntfsd'){NTF().sd=Math.max(1,Math.round(+x.value||3));svq();ntfLater();return 1}
 if(x.dataset&&x.dataset.ntfon){NTF().on[x.dataset.ntfon]=x.checked?1:0;svq();ntfLater();render();return 1}
 if(x.dataset&&x.dataset.ntfc){const r=NTF().list.find(y=>y.id==x.dataset.ntfc);if(r){r.on=x.checked?1:0;svq();ntfLater()}return 1}
 if(x.dataset&&x.dataset.nev){if(V.ne)V.ne[x.dataset.nev]=x.value;return 1}
 return 0}
"""
rep("// ---------- v1.5 extras ----------", JS + "// ---------- v1.5 extras ----------")
CSS = "\n.phpair{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:6px 0}.phpair img{width:100%;height:auto;border-radius:4px;display:block}.phhd{text-align:center;font-size:14px}.qcr{display:grid;gap:6px;padding:8px 0;border-bottom:1px solid var(--ln)}.qcb{display:flex;gap:6px}.qcb button{flex:1;padding:6px}.qcb .qcn{background:#C7313B;color:#fff;border-color:#C7313B}.rqc{cursor:pointer;display:block;width:100%;text-align:start;font:inherit;color:inherit}.rqc>div,.rqc>small{display:block}.rqu{border-inline-start:5px solid var(--rd)}.rqh{display:flex;justify-content:space-between;align-items:center;gap:8px}.ntr{display:flex;align-items:center;gap:6px;padding:6px 0;border-bottom:1px solid var(--ln)}\n"
rep("body.cap .capno{display:none!important}", "body.cap .capno{display:none!important}" + CSS)
rep("VER='v2.6'", "VER='v2.7'")
rep(" changelog:[{version:'v2.6',", " changelog:[{version:'v2.7',date:'2026-11-04',changes:['Photos: stamp (pharmacy, district, date and time) on shared photos and in reports; originals unchanged','Before / after photo report PDF per pharmacy and for a whole month (one file per pharmacy)','Quality checklist (optional, questions editable in settings, score only for the supervisor)','Phone notifications at 11:00 (due dates, stalled pharmacies, low stock, backup, custody, urgent requests) + own reminders in إدارة التنبيهات','Requests and faults log with photos, priority and status; convert to a maintenance pharmacy (done automatically when it is completed)']},{version:'v2.6',")
EN = {'أسئلة فحص الجودة (سطر لكل سؤال، فاضي = الأسئلة الجاهزة)':'Quality check questions (one per line, empty = default)','الطلبات والأعطال':'Requests and faults','إدارة التنبيهات':'Notifications','تقرير الصور PDF':'Photo report PDF','فحص الجودة':'Quality check','طلب جديد':'New request','حوّل لصيانة':'To maintenance','لا ينطبق':'N/A','تنبيه جديد':'New reminder','تجربة إشعار':'Test notification','تقرير صور قبل / بعد':'Before / after photo report'}
k = s.index('const EN_D=') + len('const EN_D='); j = s.index(';let TRX=null;', k)
D = json.loads(s[k:j])
for a2, c in EN.items(): D.setdefault(a2, c)
s = s[:k] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[j:]
open(P, 'w', encoding='utf-8').write(s)
print('ok')

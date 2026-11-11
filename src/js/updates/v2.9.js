// ---------- v2.9: Google Drive sync ----------
const GDF='966Ph Backups',GDK='gd966',GDA='https://www.googleapis.com/';
const GDKEEP={day:14,full:4,month:12};
function gdS(){let o={};try{o=JSON.parse(localStorage.getItem(GDK)||'{}')||{}}catch(e){}o.pend=o.pend||{};return o}
function gdW(o){try{localStorage.setItem(GDK,JSON.stringify(o))}catch(e){}}
function gdU(f){const o=gdS();f(o);gdW(o);return o}
const gdN=()=>{const v=Math.round(+DB.cfg.gdn||0);return v>0?Math.min(30,v):5};
const gdAskCell=()=>DB.cfg.gdcell!==false;
const DA=()=>CP('DriveAuth')||(GWEB()?GWAuth:null);
const dIso=d=>d.getFullYear()+'-'+z2(d.getMonth()+1)+'-'+z2(d.getDate());
const gdLastDay=td=>{const d=new Date(td+'T12:00:00');d.setDate(d.getDate()+1);return d.getDate()==1};
const gdPrevM=td=>{const d=new Date(td.slice(0,7)+'-15T12:00:00');d.setMonth(d.getMonth()-1);return dIso(d).slice(0,7)};
const gdDays=(a,b)=>Math.round((new Date(b+'T12:00:00')-new Date(a+'T12:00:00'))/864e5);
const gdMb=n=>n>0?(n/1048576<0.1?'<0.1':(n/1048576).toFixed(1))+' MB':'';
// ---- section stamps: which store changed last (for the merge)
const SECK=()=>UST;let SECH=null,SECT=0;
function secHash(v){const t=JSON.stringify(v===undefined?null:v);let h=0;for(let i=0;i<t.length;i+=7)h=(h*31+t.charCodeAt(i))|0;return t.length+':'+h}
function secStamp(){if(!DB)return;const id=STO||'';if(!SECH){try{SECH=JSON.parse(localStorage.getItem('gdsh')||'{}')||{}}catch(e){SECH={}}}const at=DB.cfg.sat=DB.cfg.sat||{};let ch=0;
 SECK().forEach(k=>{const h=secHash(DB[k]),key=id+'.'+k;if(SECH[key]!==undefined&&SECH[key]!==h){at[k]=nowIso();ch=1}SECH[key]=h});try{localStorage.setItem('gdsh',JSON.stringify(SECH))}catch(e){}return ch}
function secLater(){clearTimeout(SECT);SECT=setTimeout(secStamp,1500)}
// ---- what goes up
function gdDay(){secStamp();const o=dbOut();return Object.assign({},o,{ver:VER,at:nowIso(),device:DB.cfg.dev||(CAPN()?'موبايل':'لاب توب'),cfg:Object.assign({},o.cfg,{ue:0})})}
// ---- Drive REST (phone)
let GDT=null,GDBUSY=0;
async function gdToken(ia){if(GDT&&Date.now()<GDT.exp)return GDT.t;const A=DA();if(!A)throw new Error('مفيش ربط Google على الجهاز ده');
 const r=await A.authorize({interactive:!!ia});if(r&&r.need){gdU(o=>o.need=1);const e=new Error('need');e.need=1;throw e}
 GDT={t:r.token,exp:Date.now()+50*60e3};gdU(o=>{o.need=0;o.on=1});return GDT.t}
async function gdF(path,opt,again){opt=opt||{};const t=await gdToken(opt.ia);const h=Object.assign({Authorization:'Bearer '+t},opt.headers||{});
 const r=await fetch(/^https:/.test(path)?path:GDA+path,{method:opt.method||'GET',headers:h,body:opt.body});
 if(r.status==401&&!again){try{await DA().clearToken({token:t})}catch(e){}GDT=null;return gdF(path,opt,1)}
 if(!r.ok){let m='';try{m=(await r.text()).slice(0,160)}catch(e){}throw new Error('Drive '+r.status+(m?': '+m:''))}return r}
const gdQ=q=>encodeURIComponent(q);
async function gdFolder(){const st=gdS();if(st.fid){try{const r=await gdF('drive/v3/files/'+st.fid+'?fields=id,trashed');const j=await r.json();if(!j.trashed)return st.fid}catch(e){if(e.need)throw e}}
 const r=await gdF('drive/v3/files?spaces=drive&fields=files(id)&q='+gdQ("name='"+GDF+"' and mimeType='application/vnd.google-apps.folder' and trashed=false"));const j=await r.json();let id=j.files&&j.files[0]&&j.files[0].id;
 if(!id){const c=await gdF('drive/v3/files?fields=id',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:GDF,mimeType:'application/vnd.google-apps.folder'})});id=(await c.json()).id}
 gdU(o=>o.fid=id);return id}
async function gdList(){const fid=await gdFolder(),L=[];let pt='';do{const r=await gdF('drive/v3/files?pageSize=200&orderBy=name desc&fields=nextPageToken,files(id,name,size,modifiedTime)&q='+gdQ("'"+fid+"' in parents and trashed=false")+(pt?'&pageToken='+pt:''));const j=await r.json();L.push(...(j.files||[]));pt=j.nextPageToken||''}while(pt);return L}
async function gdPut(name,txt){const fid=await gdFolder();const r0=await gdF('drive/v3/files?fields=files(id)&q='+gdQ("name='"+name+"' and '"+fid+"' in parents and trashed=false"));const ex=((await r0.json()).files||[])[0];
 const blob=new Blob([txt],{type:'application/json'}),meta=ex?{}:{name,parents:[fid],mimeType:'application/json'};
 let loc=null;try{const r=await gdF('upload/drive/v3/files'+(ex?'/'+ex.id:'')+'?uploadType=resumable&fields=id,size',{method:ex?'PATCH':'POST',headers:{'Content-Type':'application/json; charset=UTF-8','X-Upload-Content-Type':'application/json','X-Upload-Content-Length':String(blob.size)},body:JSON.stringify(meta)});loc=r.headers.get('Location')}catch(e){if(e.need)throw e;console.warn(e)}
 if(loc){const r=await fetch(loc,{method:'PUT',headers:{'Content-Type':'application/json'},body:blob});if(!r.ok)throw new Error('Drive upload '+r.status);return blob.size}
 const B='966b'+Date.now(),body=new Blob(['--'+B+'\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n'+JSON.stringify(meta)+'\r\n--'+B+'\r\nContent-Type: application/json\r\n\r\n',blob,'\r\n--'+B+'--'],{type:'multipart/related; boundary='+B});
 await gdF('upload/drive/v3/files'+(ex?'/'+ex.id:'')+'?uploadType=multipart&fields=id',{method:ex?'PATCH':'POST',headers:{'Content-Type':'multipart/related; boundary='+B},body});return blob.size}
async function gdPrune(){const L=await gdList(),K=Object.entries(GWEB()?GDKEEPW:GDKEEP).map(([k,n])=>[k,n,'json']).concat([[GWEB()?'lapmonth':'month',12,'xlsx']]);for(const [k,n,x] of K){const A=L.filter(f=>new RegExp('^966-'+k+'-.*\\.'+x+'$').test(f.name)).sort((a,b)=>a.name<b.name?1:-1);for(const f of A.slice(n)){try{await gdF('drive/v3/files/'+f.id,{method:'DELETE'})}catch(e){console.warn(e)}}}}
async function gdNet(){const N=CP('Network');if(!N)return{on:navigator.onLine!==false,cell:false};try{const r=await N.getStatus();return{on:!!r.connected,cell:r.connectionType=='cellular'}}catch(e){return{on:true,cell:false}}}
// ---- the scheduler
function gdNeeds(st,td){const n={};if(st.day!=td||(st.ed||0)>=30||st.pend.day)n.day=1;
 let mk='';if(gdLastDay(td)&&st.mon!=td.slice(0,7))mk=td.slice(0,7);else{const pm=gdPrevM(td);if(st.mon&&st.mon<pm)mk=pm;else if(!st.mon&&st.mb&&st.mb<pm)mk=pm}
 if(mk)n.month=mk;else if(!st.full||gdDays(st.full,td)>=gdN()||st.pend.full)n.full=1;return n}
async function gdTick(force){if(!DA()||GDBUSY||!DB||!DB.ph.length)return;let st=gdS();if(!st.on&&!force)return;const td=TD(),f=force||{};const n=f.day||f.full?{day:f.day,full:f.full}:gdNeeds(st,td);if(!n.day&&!n.full&&!n.month)return;
 const net=await gdNet();if(!net.on){gdU(o=>{if(n.day)o.pend.day=1;if(n.full||n.month)o.pend.full=1;o.off=1});gdRender();return}
 GDBUSY=1;gdRender();let t=null;try{gdU(o=>o.off=0);
  if(n.day){const sz=await gdPut(gdNm('day')+td+'.json',JSON.stringify(gdDay()));st=gdU(o=>{o.day=td;o.ed=0;delete o.pend.day;o.last=nowIso();o.lastK='day';o.dsz=sz})}
  if(n.full||n.month){const big=!f.full&&net.cell&&gdAskCell()&&st.cell!=td;
   if(big){gdU(o=>o.pend.full=1);if(!st.ww&&!document.querySelector('.toast.gdc')){const tt=toast(`<span>☁️ ${n.month?'النسخة الشهرية':'النسخة الكاملة'} بالصور${st.fsz?' (حوالي '+gdMb(st.fsz)+')':''} جاهزة للرفع وأنت على نت الموبايل.</span><button class="pr" data-gdcell="up">ارفع</button><button data-gdcell="wait">استنى الواي فاي</button>`);tt.classList.add('rem','gdc')}}
   else{t=toast('☁️ جاري رفع '+(n.month?'النسخة الشهرية':'النسخة الكاملة')+' على Google Drive…');const o2=await fullBackupWithFiles(),name=n.month?gdNm('month')+n.month+'.json':gdNm('full')+td+'.json';const sz=await gdPut(name,JSON.stringify(Object.assign(o2,{device:DB.cfg.dev||'موبايل'})));
    if(n.month){try{const xb=xlsxAll();await gdPutBlob(name.replace(/\.json$/,'.xlsx'),xb,xb.type)}catch(e){if(e.need)throw e;console.warn(e)}}
    gdU(o=>{o.full=td;if(n.month)o.mon=n.month;delete o.pend.full;o.ww=0;o.last=nowIso();o.lastK=n.month?'month':'full';o.fsz=sz});if(f.full)toastT('✓ اترفعت النسخة الكاملة على Google Drive')}}
  try{await gdPrune()}catch(e){console.warn(e)}
  gdU(o=>{o.fails=0;o.err='';o.fn=0});if(f.day&&!f.full)toastT('✓ اترفعت على Google Drive')}
 catch(e){console.warn(e);if(e.need){gdNeedNote()}else{const o=gdU(o=>{o.fails=(o.fails||0)+1;o.err=String(e.message||e).slice(0,140);if(n.day)o.pend.day=1;if(n.full||n.month)o.pend.full=1});if(o.fails>=3&&!o.fn){gdU(x=>x.fn=1);ntfNowSend('☁️ Google Drive','الرفع فشل '+o.fails+' مرات ورا بعض. افتح القائمة ← Google Drive',{v:'gd'})}if(force)alert('⚠ الرفع ما نجحش: '+o.err)}}
 finally{if(t)t.remove();GDBUSY=0;gdRender()}}
function gdNeedNote(){const o=gdS();if(o.nn!=TD()){gdU(x=>x.nn=TD());ntfNowSend('🔑 Google Drive','جوجل محتاج تسجيل دخول تاني علشان الرفع يكمل. افتح التطبيق واضغط «تسجيل الدخول».',{v:'gd'})}
 if(!document.querySelector('.toast.gdn')){const tt=remToast('🔑 Google Drive محتاج تسجيل دخول تاني علشان الرفع يكمل.','data-gdlogin','تسجيل الدخول');tt.classList.add('gdn')}gdRender()}
let GDE=0;
function gdEdit(){if(GDPL)return;gdU(o=>o.ed=(o.ed||0)+1);const o=gdS();if((CAPN()||GWEB())&&o.on){clearTimeout(GDE);GDE=setTimeout(()=>{GDE=0;gdTick({day:1}).then(gdStat0)},60e3);gdStat0()}if(!CAPN()&&GDH&&o.ed>=30){clearTimeout(GDE);GDE=setTimeout(()=>gdlWrite(),8000)}}
function gdRender(){gdStat0();if(V&&(V.v=='gd'||V.v=='bk'||V.v=='gen'))render()}
async function gdInit(){if(!DA())return;secStamp();const N=CP('Network');if(N&&N.addListener)N.addListener('networkStatusChange',s2=>{if(!s2.connected)return;const o=gdS();if(s2.connectionType=='wifi'&&o.ww)gdU(x=>{x.ww=0});if(o.on)setTimeout(()=>gdTick(),3000)});
 const A=CP('App');if(A&&A.addListener)A.addListener('appStateChange',x=>{if(x&&x.isActive)setTimeout(()=>{gdPull();gdTick()},2500)});setInterval(()=>gdTick(),15*60e3);setInterval(()=>gdPull(),5*60e3);document.addEventListener('visibilitychange',()=>{if(!document.hidden)setTimeout(()=>gdPull(),1500);else if(GDE){clearTimeout(GDE);GDE=0;gdTick({day:1})}});if(GWEB()){gwLoad().catch(()=>{});window.addEventListener('online',()=>setTimeout(()=>{gdPull();gdTick()},3000))}
 const o=gdS();if(o.on){if(!o.mb)gdU(x=>x.mb=gdPrevM(TD()));gdPull().then(()=>gdTick())}}
function gdLine(btn){const o=gdS(),nat=CAPN()||GWEB();let t,c='';
 if(nat){if(!DA())t='محتاج تحديث التطبيق';else if(!o.on)t='لسه ما اتربطش';else if(GDBUSY){t='⏫ جاري الرفع…'}else if(o.need){t='🔑 محتاج تسجيل دخول تاني';c='bad'}else if(o.pend.day||o.pend.full){t='⏳ مستنية رفع'+(o.off?' (مفيش نت)':o.ww?' (النسخة الكاملة مستنية واي فاي)':o.err?' · '+o.err:'');c='bad'}else if(o.fails){t='⚠ فشل: '+(o.err||'');c='bad'}else if(!o.last){t='متربط · لسه مافيش رفع';c='ok'}else{t='آخر رفع '+fd(o.last)+' ✓ ('+({day:'يومية',full:'كاملة',month:'شهرية'}[o.lastK]||'')+')'+(o.full?' · آخر كاملة '+esc(o.full):'');c='ok'}}
 else{if(!GDH)t='الفولدر لسه ما اتربطش';else{t='📁 '+esc(GDH.name)+(o.lrf?' · آخر قراءة '+esc(o.lrf)+' '+fd(o.lr):'')+(o.lw?' · آخر كتابة '+fd(o.lw):'');c=o.lerr?'bad':'ok';if(o.lerr)t+=' · ⚠ '+esc(o.lerr)}}
 return `<div class="stb gdl"><small>☁️ Google Drive:</small><b class="${c}">${t}</b>${btn?`<button class="lnk" data-gdopen="1">الإعدادات ›</button>`:''}</div>`}
// ---- merge (restore from Drive and the laptop's automatic read)
const gdEmpty=v=>v==null||JSON.stringify(v).length<=24;
function gdMerge(q,why){if(!q||!Array.isArray(q.ph))throw new Error('ملف مش نسخة 966Ph');snap(why||'قبل دمج نسخة من Google Drive');const res={add:0,upd:0,del:0,sec:[]};
 const ALL=()=>DB.ph.concat(HIDDB===DB?HID:[]),find=z=>ALL().find(x=>x.id==z.id)||ALL().find(x=>String(x.no)==String(z.no)&&x.mo==z.mo),put=(l,z)=>{let i=DB.ph.indexOf(l);if(i>=0){DB.ph[i]=z;return}i=HID.indexOf(l);if(i>=0)HID[i]=z};
 DB.del=DB.del||{};Object.keys(q.del||{}).forEach(id=>{const t2=q.del[id],l=ALL().find(x=>x.id==id);if(l&&(l.modAt||BASE)<=t2){DB.ph=DB.ph.filter(x=>x!==l);HID=HID.filter(x=>x!==l);res.del++}if(!(DB.del[id]>t2))DB.del[id]=t2});
 q.ph.forEach(z0=>{const z=JSON.parse(JSON.stringify(z0));mig(z);z.modAt=z.modAt||BASE;const td=DB.del[z.id];if(td&&td>=z.modAt)return;const l=find(z);
  if(!l){DB.ph.push(z);res.add++;return}if((z.modAt||BASE)>(l.modAt||BASE)&&!syncEq(l,z)){z.id=l.id;put(l,z);res.upd++}});
 const uid=STO||U().id,qa=(q.cfg||{}).sat||{},la=DB.cfg.sat=DB.cfg.sat||{},qu=q.uw||{},src=k=>qu[uid]&&qu[uid][k]!==undefined?qu[uid][k]:q[k];
 const lp=gdS().pt||'';UST.forEach(k=>{const inc=src(k);if(inc===undefined||gdEmpty(inc))return;
  if((k=='cust'||k=='mnt')&&!gdEmpty(DB[k])){const nw=(qa[k]||'')>(la[k]||''),b0=JSON.stringify(DB[k]);gdItemMerge(k,DB[k],JSON.parse(JSON.stringify(inc)),nw);if(JSON.stringify(DB[k])!=b0)res.sec.push(k);if(nw)la[k]=qa[k];return}
  if((k=='wh'||k=='wlog')&&lp&&(qa[k]||'')>(la[k]||'')&&(la[k]||'')>lp&&!syncEq(DB[k],inc))res.whc=1;
  if(gdEmpty(DB[k])||(qa[k]||'')>(la[k]||'')){if(syncEq(DB[k],inc))return;DB[k]=JSON.parse(JSON.stringify(inc));la[k]=qa[k]||la[k]||'';res.sec.push(k)}});
 DB.uw=DB.uw||{};Object.keys(qu).forEach(id=>{if(id!=uid&&!DB.uw[id])DB.uw[id]=JSON.parse(JSON.stringify(qu[id]))});
 if((!DB.users||!DB.users.length)&&q.users)DB.users=q.users;['pl','tp','dt'].forEach(k=>{if(gdEmpty(DB[k])&&!gdEmpty(q[k]))DB[k]=q[k]});
 norm();SECH=null;try{localStorage.removeItem('gdsh')}catch(e){}secStamp();sv();return res}
const SECN={cust:'العهدة',mnt:'الصيانة',wh:'المخزن',wlog:'سجل المخزن',invs:'الفواتير',qi:'العروض والفواتير',rcvq:'الاستلام',req:'الطلبات'};
const gdResTxt=r=>`صيدليات: +${r.add} جديدة · ${r.upd} اتحدثت${r.del?' · '+r.del+' اتحذفت':''}${r.sec.length?' · أقسام: '+r.sec.map(k=>SECN[k]||k).join('، '):''}`;
async function gdApply(q,mode,why){const EXR={imgs:q._imgs?Object.assign({},q._imgs,IMG):null,files:q._files,photos:q._photos};delete q._imgs;delete q._files;delete q._photos;
 if(mode=='replace'||!DB.ph.length){snap(why||'قبل استعادة من Google Drive');delete q.ver;delete q.at;delete q.device;DB=q;norm();sv();await restoreExtras(EXR);return 'اتعملت استعادة كاملة ('+DB.ph.length+' صيدلية)'}
 const r=gdMerge(q,why);if(EXR.imgs||EXR.files||EXR.photos)await restoreExtras(EXR);render();if(r.whc)setTimeout(()=>alert('⚠ المخزن اتعدّل على الجهازين قبل ما يتزامنوا، واتاخدت نسخة الجهاز التاني (الأحدث). راجع أرصدة المخزن، ولو فيه حركة ناقصة سجلها تاني أو رجّع من «نقاط الاستعادة».'),300);return gdResTxt(r)}
// ---- laptop: Google Drive for desktop folder (File System Access API)
let GDH=null;
async function gdlInit(){if(CAPN())return;try{await stPersist()}catch(e){}if(window.showDirectoryPicker){try{GDH=(await idbGet('gddir'))||null}catch(e){GDH=null}}if(!GDH){if(!DB.ph.length)stEmpty();else gdlRemind();return}gdRender();const ok=await gdlPerm(false);
 if(!ok){const tt=remToast('☁️ اضغط علشان التطبيق يقرا آخر بيانات الموبايل من فولدر Drive.','data-gdlr','اقرا دلوقتي');tt.classList.add('gdn');return}await gdlRead(false);await gdlWrite(false);setInterval(()=>gdlWrite(false),10*60e3)}
async function gdlPerm(ask){if(!GDH)return false;try{let p=await GDH.queryPermission({mode:'readwrite'});if(p!='granted'&&ask)p=await GDH.requestPermission({mode:'readwrite'});return p=='granted'}catch(e){return false}}
async function gdlFiles(re){const L=[];for await(const e of GDH.values()){if(e.kind=='file'&&re.test(e.name)){try{const f=await e.getFile();L.push({h:e,name:e.name,size:f.size,lm:f.lastModified})}catch(x){}}}return L.sort((a,b)=>b.lm-a.lm||(a.name<b.name?1:-1))}
async function gdlRead(manual,name){try{if(!await gdlPerm(manual))return;const L=await gdlFiles(name?/./:/^966-day-.*\.json$/);const f=name?L.find(x=>x.name==name):L[0];const o=gdS();
 if(!f){if(manual)alert('مفيش ملفات من الموبايل في الفولدر لسه. اتأكد إن الموبايل رفع، وإن Drive for desktop خلص مزامنة.');return}
 if(!manual&&o.lrf==f.name&&o.lrm==f.lm)return;if(manual&&name&&!confirm('دمج '+f.name+' ('+gdMb(f.size)+') مع البيانات اللي على اللاب توب؟ هتتاخد نقطة استعادة قبلها.'))return;
 const tt=toast('☁️ جاري قراءة '+esc(f.name)+'…');let msg;try{const q=JSON.parse(await (await f.h.getFile()).text());msg=await gdApply(q,'merge','قبل دمج '+f.name+' من فولدر Drive')}finally{tt.remove()}
 gdU(x=>{x.lrf=f.name;x.lrm=f.lm;x.lr=nowIso();x.lerr=''});document.querySelectorAll('.toast.gdn').forEach(x=>x.remove());render();toastT('✓ اتقرا '+f.name+' · '+msg)}
 catch(e){console.warn(e);gdU(x=>x.lerr=String(e.message||e).slice(0,100));if(manual)alert('⚠ ما قدرتش أقرا من الفولدر: '+(e.message||e));gdRender()}}
async function gdlWrite(manual){try{if(!GDH||!DB.ph.length||!await gdlPerm(manual))return;const o=gdS();if(!manual&&!(o.ed>0)&&o.lwd==TD())return;
 const n='966-laptop-'+TD()+'.json',fh=await GDH.getFileHandle(n,{create:true}),w=await fh.createWritable();await w.write(JSON.stringify(gdDay()));await w.close();
 const L=(await gdlFiles(/^966-laptop-.*\.json$/)).sort((a,b)=>a.name<b.name?1:-1);for(const x of L.slice(7))try{await GDH.removeEntry(x.name)}catch(e){}
 gdU(x=>{x.lw=nowIso();x.lwd=TD();x.ed=0});gdRender();if(manual)toastT('✓ اتكتب '+n+' في فولدر Drive')}catch(e){console.warn(e);if(manual)alert('⚠ ما قدرتش أكتب في الفولدر: '+(e.message||e))}}
// ---- screen
function gdHtml0(nat){const o=gdS(),L=V.gdl;
 if(nat)return `<div class="wcard"><h2>☁️ Google Drive</h2>${gdLine(0)}<p class="sub">بيرفع على فولدر «${GDF}» في Drive بتاعك. التطبيق بيشوف الملفات اللي هو رفعها بس (صلاحية drive.file).</p>
 ${!DA()?'<div class="ywarn">النسخة دي من التطبيق مافيهاش ربط Google. حدّث لـ v2.9 أو أحدث.</div>':`<div class="tt">${o.on&&!o.need?`<button data-gdup="day">${ic('upload')}ارفع دلوقتي</button><button data-gdup="full">${ic('upload')}ارفع نسخة كاملة بالصور</button>`:`<button class="pr" data-gdlogin="1">${ic('lock')}${o.on?'تسجيل الدخول تاني':'ربط حساب Google'}</button>`}</div>`}
 ${o.on?`<label class="chk"><input type="checkbox" id="gdon" checked> الرفع التلقائي شغال</label>`:''}</div>
 <div class="wcard"><h3>المواعيد</h3><small>• نسخة يومية (البيانات من غير صور): أول مرة تفتح التطبيق في اليوم + كل 30 تعديل.<br>• نسخة كاملة بالصور والمرفقات كل:</small><label>عدد الأيام بين النسخ الكاملة<input type="number" inputmode="numeric" min="1" max="30" id="gdfn" value="${gdN()}"></label>
 <small>• آخر يوم في الشهر: نسخة شهرية كاملة إجباري (لو التطبيق ما اتفتحش في اليوم ده، بتترفع أول ما يتفتح في الشهر الجديد).<br>• بيحتفظ بآخر ${GDKEEP.day} يومية و${GDKEEP.full} كاملة و${GDKEEP.month} شهرية، والأقدم بيتمسح من Drive لوحده.<br>• لو مفيش نت: بتستنى وتترفع أول ما النت يرجع.<br>• الرفع بيحصل والتطبيق مفتوح أو لما ترجع له (مش في الخلفية).</small>
 <label class="chk"><input type="checkbox" id="gdcell"${gdAskCell()?' checked':''}> اسألني قبل رفع النسخة الكاملة على نت الموبايل</label></div>
 <div class="wcard"><h3>الاسترجاع من Drive</h3><small>بيدمج مع اللي على الموبايل: كل صيدلية بتاخد الأحدث، وباقي الأقسام (العهدة، المخزن، الصيانة، الطلبات…) القسم اللي اتعدل آخر واحد. قبلها بتتاخد نقطة استعادة.</small>
 <div class="tt"><button data-gdls="1">${ic('db')}عرض النسخ على Drive</button><button data-pick="gdmfin">${ic('upload')}دمج ملف من اللاب توب</button></div><input type="file" id="gdmfin" accept=".json,application/json" hidden><small class="hint">«دمج ملف من اللاب توب»: اختار Drive ← فولدر ${GDF} ← آخر ملف 966-laptop-… (الموبايل ما بيشوفهوش في القائمة اللي فوق).</small>${L?gdListHtml(L):''}</div>`;
 return `<div class="wcard"><h2>☁️ فولدر Google Drive على اللاب توب</h2>${gdLine(0)}
 ${window.showDirectoryPicker?'':'<div class="ywarn">المتصفح ده مايدعمش ربط الفولدر. افتح التطبيق على Chrome أو Edge.</div>'}${stWarnHtml()}
 <small>1) نزّل Google Drive for desktop وسجّل دخول، وفي شاشة «مزامنة الفولدرات» اضغط Skip.<br>2) بعد أول رفع من الموبايل هيظهر <b>G:\\My Drive\\${GDF}</b>. كليك يمين عليه ← Offline access ← Available offline.<br>3) اضغط «ربط فولدر درايف» واختار الفولدر ده، ولما يسألك اختار «Allow on every visit».</small>
 <div class="tt"><button class="${GDH?'':'pr'}" data-gddir="1">${ic('upload')}${GDH?'تغيير الفولدر':'ربط فولدر درايف'}</button>${GDH?`<button class="pr" data-gdlr="1">اقرا آخر بيانات الموبايل</button><button data-gdlw="1">اكتب نسخة اللاب توب</button>`:''}</div>
 <small>التطبيق بيقرا آخر ملف يومي من الموبايل أول ما تفتحه ويدمجه، وبيكتب ملف «966-laptop-…» في نفس الفولدر (آخر 7). الموبايل مابيشوفش ملفات اللاب توب لوحده؛ لو احتجتها هناك استوردها من «المزامنة».</small></div>
 ${GDH?`<div class="wcard"><h3>الملفات في الفولدر</h3><div class="tt"><button data-gdlls="1">${ic('db')}عرض الملفات</button></div>${L?gdListHtml(L):''}</div>`:''}`}
function gdListHtml(L){if(!L.length)return '<p class="em">مفيش ملفات لسه.</p>';const nat=CAPN(),G=[['day','يومية'],['full','كاملة بالصور'],['month','شهرية'],['laptop','اللاب توب'],['lapfull','اللاب توب كاملة'],['lapmonth','اللاب توب شهرية']];
 return G.map(([k,t])=>{const A=L.filter(f=>f.name.startsWith('966-'+k+'-')&&/\.json$/.test(f.name));if(!A.length)return '';return `<h4>${t} (${A.length})</h4>`+A.map(f=>`<div class="ph gdr"><small style="flex:1"><b>${esc(f.name.replace(/^966-|\.json$/g,''))}</b> · ${fd(f.mt)} · ${gdMb(f.size)}</small><button data-gdrs="${esc(f.id||f.name)}">دمج</button><button data-gdrr="${esc(f.id||f.name)}" style="color:var(--rd)">استبدال</button></div>`).join('')}).join('')}
async function gdGet(id){const r=await gdF('drive/v3/files/'+id+'?alt=media');return JSON.parse(await r.text())}
async function gdRestore(id,mode){const L=V.gdl||[],f=L.find(x=>(x.id||x.name)==id);if(!f)return;
 if(!confirm(mode=='replace'?'استبدال كل البيانات اللي هنا بـ '+f.name+'؟ هتتاخد نقطة استعادة قبلها.':'دمج '+f.name+' ('+gdMb(f.size)+') مع البيانات اللي هنا؟ هتتاخد نقطة استعادة قبلها.'))return;
 const t=toast('☁️ جاري التحميل…');try{const q=f.id?await gdGet(f.id):JSON.parse(await (await f.h.getFile()).text());const m=await gdApply(q,mode,'قبل '+(mode=='replace'?'استبدال':'دمج')+' '+f.name);t.remove();render();alert('✓ '+m)}catch(e){t.remove();alert('⚠ ما نجحش: '+(e.message||e))}}
function v29Click(d,b){
 if(d.gdopen){goV({v:'gd',from:V.v,op:{},dr:{},q:V.q});return 1}
 if(d.gdlogin){const tt=b.closest('.toast');if(tt)tt.remove();GDT=null;gdToken(true).then(()=>{const o=gdS();if(!o.mb)gdU(x=>x.mb=gdPrevM(TD()));toastT('✓ اتربط Google Drive');gdPull().then(()=>gdTick())}).catch(e=>alert(e.need?'لسه محتاج تسجيل دخول':'⚠ تسجيل الدخول ما نجحش: '+(e.message||e))).finally(gdRender);return 1}
 if(d.gdup){(async()=>{if(d.gdup=='full'){const n=await gdNet();if(n.cell&&!confirm('أنت على نت الموبايل. النسخة الكاملة بالصور'+(gdS().fsz?' حوالي '+gdMb(gdS().fsz):'')+'. ترفعها دلوقتي؟'))return}gdTick(d.gdup=='full'?{day:1,full:1}:{day:1})})();return 1}
 if(d.gdcell){const tt=b.closest('.toast');if(tt)tt.remove();if(d.gdcell=='up'){gdU(o=>{o.cell=TD();o.ww=0});gdTick()}else{gdU(o=>o.ww=1);toastT('تمام، هترفع أول ما تتوصل بواي فاي');gdRender()}return 1}
 if(d.gdls){const t=toast('☁️ جاري جلب القائمة…');gdList().then(L=>{V.gdl=L.map(f=>({id:f.id,name:f.name,size:+f.size||0,mt:f.modifiedTime}));render()}).catch(e=>{if(e.need)gdNeedNote();else alert('⚠ '+(e.message||e))}).finally(()=>t.remove());return 1}
 if(d.gdrs||d.gdrr){gdRestore(d.gdrs||d.gdrr,d.gdrr?'replace':'merge');return 1}
 if(d.gddir){(async()=>{try{const h=await window.showDirectoryPicker({id:'gd966',mode:'readwrite'});GDH=h;await idbSet('gddir',h);gdU(o=>{o.lrf='';o.lrm=0});render();await gdlRead(true);await gdlWrite(true)}catch(e){if(e&&e.name!='AbortError')alert('⚠ '+(e.message||e))}})();return 1}
 if(d.gdlr){const tt=b.closest('.toast');if(tt)tt.remove();gdlRead(true).then(()=>gdlWrite(false));return 1}
 if(d.gdlw){gdlWrite(true);return 1}
 if(d.gdlls){(async()=>{if(!await gdlPerm(true))return;V.gdl=(await gdlFiles(/^966-.*\.json$/)).map(f=>({h:f.h,name:f.name,size:f.size,mt:new Date(f.lm).toISOString()}));render()})();return 1}
 return 0}
function v29Change(x){if(x.id=='gdfn'){const v=Math.max(1,Math.min(30,Math.round(+x.value||5)));DB.cfg.gdn=v;x.value=v;svq();toastT('✓ نسخة كاملة كل '+v+' يوم');return 1}
 if(x.id=='gdcell'){DB.cfg.gdcell=x.checked;svq();return 1}
 if(x.id=='gdon'){gdU(o=>o.on=x.checked?1:0);render();return 1}return 0}

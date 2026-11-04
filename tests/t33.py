# v2.9: Google Drive sync (mocked DriveAuth, Network, notifications and a mocked Drive REST server) + laptop folder (mocked File System Access)
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new29.html';D=open(W+'bk1102/data.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
MOCK="""(()=>{const D0=Date;let T=new D0('2026-11-04T10:00:00').getTime();class F extends D0{constructor(...a){super(...(a.length?a:[T]))}static now(){return T}};window.Date=F;window._set=s=>{T=new D0(s).getTime()};
 window._sch=[];window._net={connected:true,connectionType:'wifi'};window._nl=[];window._al=[];window._auth='ok';window._fail=0;window._noLoc=0;window._log=[];
 const FS={},S={};let N=1;const id=()=>'f'+(N++),now=()=>new D0(T).toISOString();window._FS=FS;
 const R=(b,st,h)=>new Response(typeof b=='string'?b:JSON.stringify(b),{status:st||200,headers:h||{'Content-Type':'application/json'}});
 const q2=u=>{const q=decodeURIComponent((u.split('q=')[1]||'').split('&')[0]);const o={};let m=/name='([^']+)'/.exec(q);if(m)o.name=m[1];m=/'([^']+)' in parents/.exec(q);if(m)o.par=m[1];if(/folder/.test(q))o.folder=1;return o};
 const of=f=>({id:f.id,name:f.name,size:String(f.content.length),modifiedTime:f.mt,trashed:false});
 const F0=window.fetch;window.fetch=async(u,o)=>{o=o||{};u=String(u);const m=o.method||'GET';
  if(/^https:\\/\\/upload\\.mock\\//.test(u)){const s=S[u];const txt=await new Response(o.body).text();if(s.id){FS[s.id].content=txt;FS[s.id].mt=now()}else{const i=id();FS[i]=Object.assign({id:i,content:txt,mt:now()},s.meta)}window._log.push('PUT '+(s.id?'upd':'new'));return R({id:1})}
  if(!/googleapis\\.com/.test(u))return F0(u,o);
  if(window._fail>0){window._fail--;return R('boom',500)}
  window._log.push(m+' '+u.replace('https://www.googleapis.com/','').split('?')[0]);
  let x;
  if(x=/drive\\/v3\\/files\\/([^/?]+)\\?alt=media/.exec(u))return R(FS[x[1]].content);
  if(m=='DELETE'){x=/files\\/([^/?]+)/.exec(u);delete FS[x[1]];return R('',204)}
  if(/upload\\/drive\\/v3\\/files/.test(u)){x=/files\\/([^/?]+)\\?/.exec(u);const ex=x&&x[1];
   if(/resumable/.test(u)){if(window._noLoc)return R({},200,{});const k='https://upload.mock/s/'+(N++);S[k]={id:ex,meta:ex?null:JSON.parse(o.body)};return R({},200,{Location:k})}
   const txt=await new Response(o.body).text();const parts=txt.split(/--966b\\d+/);const meta=JSON.parse(parts[1].split('\\r\\n\\r\\n')[1]);const body=parts[2].split('\\r\\n\\r\\n').slice(1).join('\\r\\n\\r\\n').replace(/\\r\\n$/,'');
   if(ex){FS[ex].content=body;FS[ex].mt=now()}else{const i=id();FS[i]=Object.assign({id:i,content:body,mt:now()},meta)}window._log.push('MULTI');return R({id:1})}
  if(x=/drive\\/v3\\/files\\/([^/?]+)\\?fields/.exec(u)){const f=FS[x[1]];return f?R({id:f.id,trashed:false}):R('nf',404)}
  if(/drive\\/v3\\/files\\?/.test(u)&&m=='POST'){const b=JSON.parse(o.body),i=id();FS[i]=Object.assign({id:i,content:'',mt:now()},b);return R({id:i})}
  if(/drive\\/v3\\/files\\?/.test(u)){const q=q2(u);const L=Object.values(FS).filter(f=>(!q.name||f.name==q.name)&&(!q.par||(f.parents||[]).includes(q.par))&&(!q.folder||f.mimeType=='application/vnd.google-apps.folder'));return R({files:L.map(of)})}
  return R('?',400)};
 window.Capacitor={isNativePlatform:()=>true,Plugins:{
  LocalNotifications:{createChannel:async()=>{},addListener:()=>{},checkPermissions:async()=>({display:'granted'}),requestPermissions:async()=>({display:'granted'}),getPending:async()=>({notifications:[]}),cancel:async()=>{},schedule:async o=>{window._sch=window._sch.concat(o.notifications)}},
  DriveAuth:{authorize:async o=>{window._log.push('AUTH '+(o.interactive?'ia':'silent'));if(window._auth=='need'&&!o.interactive)return {need:true};return {token:'tok'+Date.now()}},clearToken:async()=>{}},
  Network:{getStatus:async()=>window._net,addListener:(n,cb)=>{window._nl.push(cb)}},
  App:{addListener:(n,cb)=>{window._al.push([n,cb])}}}};
 window._netSet=(c,t)=>{window._net={connected:c,connectionType:t};window._nl.forEach(cb=>cb(window._net))};
})()"""
names="Object.values(_FS).filter(f=>/^966-/.test(f.name)).map(f=>f.name).sort()"
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));
  DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:90]),x.accept()))
  pg.add_init_script(MOCK)
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(6000)
  pg.evaluate("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200)
  out('bk_line',pg.evaluate("document.querySelector('.gdl').innerText.replace(/\\s+/g,' ')"))
  pg.click('.gdl [data-gdopen]');pg.wait_for_timeout(200);out('screen',pg.evaluate("document.querySelector('header h1').innerText"))
  pg.click('[data-gdlogin]');pg.wait_for_timeout(2500)
  out('after_login',[pg.evaluate(names),pg.evaluate("gdS().mb"),pg.evaluate("document.querySelector('.gdl').innerText.replace(/\\s+/g,' ')")])
  day=pg.evaluate("JSON.parse(Object.values(_FS).find(f=>f.name=='966-day-2026-11-04.json').content)")
  full=pg.evaluate("(f=>[f.content.length,Object.keys(JSON.parse(f.content)._photos||{}).length])(Object.values(_FS).find(f=>f.name=='966-full-2026-11-04.json'))")
  out('day_content',[len(day['ph']),day['ver'],'_photos' in day,day.get('device')]);out('full_content',full)
  out('folder',pg.evaluate("Object.values(_FS).filter(f=>f.mimeType=='application/vnd.google-apps.folder').map(f=>f.name)"))
  # 30 edits -> today's file overwritten
  pg.evaluate("window._log=[]");pg.evaluate("(()=>{for(let i=0;i<30;i++){LASTE=0;sv()}})()");pg.wait_for_timeout(9500)
  out('30edits',[pg.evaluate(names),[x for x in pg.evaluate("window._log") if 'PUT' in x or 'AUTH' in x],pg.evaluate("gdS().ed")])
  # mobile data after 5 days: daily goes, full asks
  pg.evaluate("window._net={connected:true,connectionType:'cellular'};_set('2026-11-09T10:00:00')");pg.evaluate("gdTick()");pg.wait_for_timeout(1500)
  out('cell',[pg.evaluate(names),pg.evaluate("(t=>t&&t.innerText.replace(/\\s+/g,' '))(document.querySelector('.toast.gdc'))")])
  pg.click('.toast.gdc [data-gdcell=wait]');pg.wait_for_timeout(300)
  out('wait',[pg.evaluate("[gdS().ww,gdS().pend]"),pg.evaluate("document.querySelector('.gdl').innerText.replace(/\\s+/g,' ')") if pg.query_selector('.gdl') else None])
  pg.evaluate("gdTick()");pg.wait_for_timeout(800);out('no_reask',pg.evaluate("!!document.querySelector('.toast.gdc')"))
  pg.evaluate("_netSet(true,'wifi')");pg.wait_for_timeout(5000)
  out('wifi',[pg.evaluate(names),pg.evaluate("[gdS().ww,gdS().pend,gdS().full]")])
  # offline queue
  pg.evaluate("_netSet(false,'none');_set('2026-11-10T10:00:00')");pg.evaluate("gdTick()");pg.wait_for_timeout(700)
  pg.evaluate("goV({v:'gd',op:{},dr:{},q:V.q})");out('offline',[pg.evaluate("gdS().pend"),pg.evaluate("document.querySelector('.gdl').innerText.replace(/\\s+/g,' ')")])
  pg.evaluate("_netSet(true,'wifi')");pg.wait_for_timeout(4500);out('back_online',[pg.evaluate(names),pg.evaluate("gdS().pend")])
  # last day of the month -> monthly full, not an extra full
  pg.evaluate("_set('2026-11-30T20:00:00')");pg.evaluate("gdTick()");pg.wait_for_timeout(2500);out('month',[pg.evaluate(names),pg.evaluate("[gdS().mon,gdS().full,gdS().lastK]")])
  # retention: 16 old dailies, 6 full -> 14 / 4
  pg.evaluate("(()=>{const fid=gdS().fid;for(let i=1;i<=16;i++)_FS['x'+i]={id:'x'+i,name:'966-day-2026-10-'+String(i).padStart(2,'0')+'.json',parents:[fid],content:'{}',mt:'2026-10-01T00:00:00Z'};for(let i=1;i<=6;i++)_FS['y'+i]={id:'y'+i,name:'966-full-2026-09-0'+i+'.json',parents:[fid],content:'{}',mt:'2026-09-01T00:00:00Z'}})()")
  pg.evaluate("_set('2026-12-01T09:00:00')");pg.evaluate("gdTick()");pg.wait_for_timeout(2500)
  nm=pg.evaluate(names);out('prune',[len([n for n in nm if n.startswith('966-day-')]),len([n for n in nm if n.startswith('966-full-')]),len([n for n in nm if n.startswith('966-month-')]),[n for n in nm if n.startswith('966-day-')][:2]])
  # multipart fallback when no Location header
  pg.evaluate("window._noLoc=1;window._log=[]");pg.evaluate("gdTick({day:1})");pg.wait_for_timeout(1200);out('multipart',['MULTI' in pg.evaluate("window._log"),pg.evaluate("window._noLoc=0")])
  # 3 failures -> notification once
  pg.evaluate("window._sch=[];window._fail=99;GDT=null");
  for i in range(3):pg.evaluate("gdTick({day:1})");pg.wait_for_timeout(600)
  out('fail3',[pg.evaluate("gdS().fails"),pg.evaluate("window._sch.filter(n=>/Drive/.test(n.title)).map(n=>n.title+' | '+n.body)"),pg.evaluate("document.querySelector('.gdl').innerText.replace(/\\s+/g,' ')")])
  pg.evaluate("window._fail=0;gdTick({day:1})");pg.wait_for_timeout(1200);out('recovered',pg.evaluate("[gdS().fails,gdS().err]"))
  # Google asks to sign in again (testing mode, weekly)
  pg.evaluate("window._sch=[];window._auth='need';GDT=null;_set('2026-12-02T09:00:00')");pg.evaluate("gdTick()");pg.wait_for_timeout(900)
  out('need',[pg.evaluate("gdS().need"),pg.evaluate("window._sch.map(n=>n.title)"),pg.evaluate("(t=>t&&t.innerText.replace(/\\s+/g,' '))(document.querySelector('.toast.gdn'))"),pg.evaluate("document.querySelector('.gdl').innerText.replace(/\\s+/g,' ')")])
  pg.evaluate("window._auth='ok'");pg.click('.toast.gdn [data-gdlogin]');pg.wait_for_timeout(2500);out('relogin',[pg.evaluate("gdS().need"),pg.evaluate("gdS().pend")])
  # restore with merge: a Drive copy where one pharmacy is newer, one older, a new one, and a newer warehouse section
  pg.evaluate("""(()=>{const fid=gdS().fid,q=JSON.parse(JSON.stringify(gdDay())),a=q.ph[0],b=q.ph[1];a.name='اسم من درايف';a.modAt='2099-01-01T00:00:00Z';b.name='قديم';b.modAt='2000-01-01T00:00:00Z';
    q.ph.push(Object.assign(JSON.parse(JSON.stringify(a)),{id:777777,no:'99999',name:'جديدة',modAt:'2099-01-01T00:00:00Z'}));const u=STO;q.uw[u].wh=(q.uw[u].wh||[]).concat([{id:'wz',nm:'صنف من درايف',qty:3}]);q.cfg.sat=Object.assign({},q.cfg.sat,{wh:'2099-01-01T00:00:00Z'});
    _FS['r1']={id:'r1',name:'966-day-2026-12-03.json',parents:[fid],content:JSON.stringify(q),mt:'2026-12-03T00:00:00Z'};window._a=[a.id,b.id,DB.ph.find(p=>p.id==b.id).name]})()""")
  n0=pg.evaluate("DB.ph.length+HID.length");s0=pg.evaluate("SNAPS.length")
  pg.evaluate("goV({v:'gd',op:{},dr:{},q:V.q})");pg.click('[data-gdls]');pg.wait_for_timeout(800)
  out('list',pg.evaluate("[...document.querySelectorAll('.gdr small')].slice(0,3).map(x=>x.innerText)"))
  pg.click('[data-gdrs=r1]');pg.wait_for_timeout(2000)
  out('merge',[pg.evaluate("(a=>[DB.ph.concat(HID).find(p=>p.id==a[0]).name,DB.ph.concat(HID).find(p=>p.id==a[1]).name==a[2]])(window._a)"),pg.evaluate("DB.ph.length+HID.length")-n0,pg.evaluate("(DB.wh||[]).some(x=>x.id=='wz')"),pg.evaluate("SNAPS.length")-s0 if s0<5 else pg.evaluate("SNAPS[0].why"),DL[-2:]])
  out('ERRS',E)
  # ---- laptop: Drive for desktop folder
  ph_file=pg.evaluate("JSON.stringify(Object.assign(JSON.parse(JSON.stringify(gdDay())),{device:'موبايل'}))")
  lp=br.new_page(viewport={'width':1200,'height':900});E2=[];lp.on('pageerror',lambda e:E2.append(str(e)));lp.on('dialog',lambda x:x.accept())
  lp.add_init_script("""(()=>{const files={};window._files=files;const mk=(n)=>({kind:'file',name:n,getFile:async()=>{const f=files[n];return {size:f.t.length,lastModified:f.lm,text:async()=>f.t}},createWritable:async()=>{let b='';return {write:async x=>{b+=x},close:async()=>{files[n]={t:b,lm:Date.now()}}}}});
   const H={kind:'directory',name:'966Ph Backups',queryPermission:async()=>'granted',requestPermission:async()=>'granted',values:async function*(){for(const n of Object.keys(files))yield mk(n)},getFileHandle:async(n,o)=>{if(!files[n]){if(!o||!o.create)throw new Error('nf');files[n]={t:'',lm:Date.now()}}return mk(n)},removeEntry:async n=>{delete files[n]}};
   window._H=H;window.showDirectoryPicker=async()=>H})()""")
  lp.goto(APP);lp.wait_for_timeout(300);lp.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);lp.reload();lp.evaluate("(()=>{const g=idbGet,s2=idbSet;window.idbGet=async k=>k=='gddir'?(window._linked?_H:null):g(k);window.idbSet=async(k,v)=>{if(k=='gddir'){window._linked=1;localStorage.setItem('_lk','1');return}return s2(k,v)};if(localStorage.getItem('_lk'))window._linked=1})()");lp.wait_for_timeout(2500)
  lp.evaluate("goV({v:'gd',op:{},dr:{},q:V.q})");lp.wait_for_timeout(200);out('lap_screen',lp.evaluate("document.querySelector('main').innerText.split('\\n').slice(0,4)"))
  lp.evaluate("t=>{_files['966-day-2026-12-03.json']={t,lm:Date.now()-1000};_files['966-day-2026-11-01.json']={t:'{\"ph\":[]}',lm:Date.now()-9e8}}",ph_file)
  lp.click('[data-gddir]');lp.wait_for_timeout(2500)
  out('lap_link',[lp.evaluate("[gdS().lrf,!!DB.ph.concat(HID).find(p=>p.no=='99999')]"),lp.evaluate("Object.keys(_files).sort()"),lp.evaluate("document.querySelector('.gdl').innerText.replace(/\\s+/g,' ')")])
  # reopen: handle from IndexedDB, same file not merged twice, a newer phone file merged automatically
  lp.evaluate("t=>{const q=JSON.parse(t);q.ph[0].name='أحدث من الموبايل';q.ph[0].modAt='2099-02-01T00:00:00Z';_files['966-day-2026-12-04.json']={t:JSON.stringify(q),lm:Date.now()+5000}}",ph_file)
  st=lp.evaluate("JSON.stringify(Object.assign({},_files))")
  lp.add_init_script("window._files0=%s"%st)
  lp.add_init_script("""(()=>{const F=window._files,F0=window._files0;if(F&&F0)Object.assign(F,F0)})()""")
  lp.reload();lp.evaluate("(()=>{const g=idbGet,s2=idbSet;window.idbGet=async k=>k=='gddir'?(window._linked?_H:null):g(k);window.idbSet=async(k,v)=>{if(k=='gddir'){window._linked=1;localStorage.setItem('_lk','1');return}return s2(k,v)};if(localStorage.getItem('_lk'))window._linked=1})()");lp.wait_for_timeout(3500)
  out('lap_reopen',[lp.evaluate("!!GDH"),lp.evaluate("gdS().lrf"),lp.evaluate("DB.ph.concat(HID).some(p=>p.name=='أحدث من الموبايل')"),lp.evaluate("SNAPS[0]&&SNAPS[0].why")])
  lp.evaluate("goV({v:'gd',op:{},dr:{},q:V.q})");lp.click('[data-gdlls]');lp.wait_for_timeout(600);out('lap_list',lp.evaluate("[...document.querySelectorAll('.gdr small')].map(x=>x.innerText.split(' · ')[0])"))
  out('ERRS2',E2)
  br.close()

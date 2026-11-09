# v3.5 (uses the fake Google of t40): Google Drive from the web link (https). Google sign-in and the Drive API are faked in the test;
# checks: login, upload with laptop names, monthly Excel, automatic read and merge of the phone's newest file, list / restore.
import json, re, time, urllib.parse
from playwright.sync_api import sync_playwright
W='/home/claude/work/';HTML=open(W+'new35.html',encoding='utf-8').read();D=json.loads(open(W+'bk1106/data.json',encoding='utf-8').read())
URL='https://abdoelswah100-jpg.github.io/966ph-branding-app/'
def out(k,v):print(k,'=>',v)
FILES={};SEQ=[0];CALLS=[]
def nid():SEQ[0]+=1;return 'f%d'%SEQ[0]
def now():return time.strftime('%Y-%m-%dT%H:%M:%S.000Z',time.gmtime())+str(SEQ[0])
GSI="""window.google={accounts:{oauth2:{initTokenClient:o=>({requestAccessToken:x=>{window.__gsi=(window.__gsi||0)+1;window.__prompt=x&&x.prompt;setTimeout(()=>o.callback({access_token:'tok123',expires_in:3600}),50)}})}}};"""
def drive(route):
  r=route.request;u=urllib.parse.urlparse(r.url);q=urllib.parse.parse_qs(u.query);path=u.path;CALLS.append((r.method,path,q.get('uploadType',[''])[0]))
  auth=r.headers.get('authorization','')
  if auth!='Bearer tok123':return route.fulfill(status=401,body='no')
  if 'uploadType' in q and q['uploadType'][0]=='resumable':return route.fulfill(status=400,body='no resumable here')
  if path.startswith('/upload/drive/v3/files'):
    body=r.post_data_buffer;ct=r.headers['content-type'];b=ct.split('boundary=')[1];parts=body.split(('--'+b).encode())
    meta=json.loads(parts[1].split(b'\r\n\r\n',1)[1].rsplit(b'\r\n',1)[0] or b'{}');data=parts[2].split(b'\r\n\r\n',1)[1].rsplit(b'\r\n',1)[0]
    m=re.match(r'/upload/drive/v3/files/(\w+)',path)
    if m:f=FILES[m.group(1)];f['data']=data;f['modifiedTime']=now();fid=m.group(1)
    else:fid=nid();FILES[fid]=dict(id=fid,name=meta['name'],parents=meta.get('parents',[]),mimeType=meta.get('mimeType'),data=data,modifiedTime=now())
    return route.fulfill(status=200,content_type='application/json',body=json.dumps({'id':fid,'size':str(len(data))}))
  m=re.match(r'/drive/v3/files/(\w+)$',path)
  if m:
    f=FILES.get(m.group(1))
    if r.method=='DELETE':FILES.pop(m.group(1),None);return route.fulfill(status=204,body='')
    if not f:return route.fulfill(status=404,body='nf')
    if q.get('alt')==['media']:return route.fulfill(status=200,body=f['data'])
    return route.fulfill(status=200,content_type='application/json',body=json.dumps({'id':f['id'],'trashed':False}))
  if path=='/drive/v3/files' and r.method=='POST':
    meta=json.loads(r.post_data);fid=nid();FILES[fid]=dict(id=fid,name=meta['name'],parents=[],mimeType=meta['mimeType'],data=b'',modifiedTime=now());return route.fulfill(status=200,content_type='application/json',body=json.dumps({'id':fid}))
  if path=='/drive/v3/files':
    qs=q.get('q',[''])[0];L=list(FILES.values())
    n=re.search(r"name='([^']+)'",qs);p=re.search(r"'(\w+)' in parents",qs)
    if n:L=[f for f in L if f['name']==n.group(1)]
    if 'folder' in qs:L=[f for f in L if f['mimeType']=='application/vnd.google-apps.folder']
    if p:L=[f for f in L if p.group(1) in f['parents']]
    return route.fulfill(status=200,content_type='application/json',body=json.dumps({'files':[dict(id=f['id'],name=f['name'],size=str(len(f['data'])),modifiedTime=f['modifiedTime']) for f in L]}))
  return route.fulfill(status=404,body='?')
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
  # ---------- phone-like (file://): custody top-up
  pg=br.new_page(viewport={'width':400,'height':860},accept_downloads=True);E=[];pg.on('pageerror',lambda e:E.append(str(e)));DL=[];FL=[];ANS=[]
  def dlg(x):
    DL.append(x.message[:200])
    if x.type=='prompt':x.accept(ANS.pop(0) if ANS else '')
    else:x.accept()
  pg.on('dialog',dlg);pg.on('download',lambda d:FL.append(d))
  pg.goto('file://'+W+'new35.html');pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D));pg.reload();pg.wait_for_timeout(2500)
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.set_input_files('#cjson',W+'cust/عهدة شهر 10-2026 - للاستيراد.json');pg.wait_for_timeout(800)
  k0=pg.evaluate("CU().cur");rem=pg.evaluate("cRem(cMo())")
  pg.click('[data-cdl]');pg.wait_for_timeout(200);pg.click('[data-cdgo=save]');pg.wait_for_timeout(6000)
  out('after_handover',pg.evaluate("[CU().cur,cMo().open,cRem(cMo())]"))
  pg.click('[data-cdep]');pg.wait_for_timeout(200)
  out('dep_sheet',pg.evaluate("[document.querySelector('.csh b').innerText,(document.querySelector('[data-cdepf]')||{}).innerText]"))
  pg.click('[data-cdepf]');pg.fill('#cdpn','تحويل من الشركة');pg.click('[data-cdeps]');pg.wait_for_timeout(300)
  out('dep_saved',pg.evaluate("[cMo().dep.map(d=>[d.amt,d.note]),cAv(cMo()),cRem(cMo()),document.querySelector('.ckpi>div').innerText.replace(/\\s+/g,' '),document.querySelector('.cdepr').innerText.replace(/\\s+/g,' ')]"))
  # add an invoice-like expense then check statement
  pg.evaluate("(()=>{const M=cMo();M.items.push({id:Date.now(),dt:TD(),tm:'10:00',desc:'اختبار',comp:'شركة',kind:'أخرى',amt:300,note:''});sv();render()})()")
  out('rem_after_exp',pg.evaluate("cRem(cMo())"))
  out('pdf',pg.evaluate("(el=>[el.querySelector('tr.copen').innerText.replace(/\\s+/g,' '),el.querySelector('.cnpline').innerText])(custPdfEl(CU().cur))"))
  import base64,zipfile,io,re as _re
  b64=pg.evaluate("(async()=>{const b=custXlsx(CU().cur),a=new Uint8Array(await b.arrayBuffer());let s='';for(const c of a)s+=String.fromCharCode(c);return btoa(s)})()")
  z=zipfile.ZipFile(io.BytesIO(base64.b64decode(b64)));sh=z.read('xl/worksheets/sheet1.xml').decode();ss=z.read('xl/sharedStrings.xml').decode() if 'xl/sharedStrings.xml' in z.namelist() else ''
  out('xlsx',['تعزيز' in sh+ss,_re.findall(r'<c r="H7"[^>]*>.*?</c>',sh)[:1],_re.findall(r'<c r="A3"[^>]*>.*?</c>',sh)[:1]])
  # edit opening ✏️
  ANS.append('4000');pg.click('[data-copen]');pg.wait_for_timeout(300);out('open_edit',pg.evaluate("[cMo().open,cAv(cMo())]"))
  # edit and delete deposit
  pg.click('[data-cdepe]');pg.wait_for_timeout(200);pg.fill('#cdpa','6000');pg.click('[data-cdeps]');pg.wait_for_timeout(200);out('dep_edit',pg.evaluate("cMo().dep.map(d=>d.amt)"))
  pg.click('[data-cdepx]');pg.wait_for_timeout(200);out('dep_del',pg.evaluate("[(cMo().dep||[]).length,cRem(cMo())]"))
  # lock: delivered month blocks top-up
  pg.evaluate(f"CU().cur='{k0}';render()");pg.wait_for_timeout(200);out('locked_no_btn',pg.evaluate("!document.querySelector('[data-cdep]')"))
  # menu / backups
  pg.evaluate("goV({v:'home',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);out('menu_gd',pg.evaluate("MENU.some(m=>m[0]=='gd')"))
  pg.evaluate("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);out('bk_drive',pg.evaluate("[document.querySelector('header').innerText.replace(/\\s+/g,' '),!!document.querySelector('details.gdbk[open]'),!!document.querySelector('.gdbk [data-gdlogin]')]"))
  out('ERRS',E)
  # ---------- web link: empty message, login, auto upload after an edit, auto read
  ctx=br.new_context(viewport={'width':1200,'height':900},service_workers='block')
  ctx.route(URL+'**',lambda rt:rt.fulfill(status=200,content_type='text/html',body=HTML) if rt.request.url.rstrip('/').endswith('966ph-branding-app') or rt.request.url.endswith('index.html') else rt.fulfill(status=404,body=''))
  ctx.route('https://accounts.google.com/gsi/client',lambda rt:rt.fulfill(status=200,content_type='text/javascript',body=GSI))
  ctx.route('https://www.googleapis.com/**',drive)
  fid=nid();FILES[fid]=dict(id=fid,name='966Ph Backups',parents=[],mimeType='application/vnd.google-apps.folder',data=b'',modifiedTime=now())
  d1=nid();FILES[d1]=dict(id=d1,name='966-day-2026-11-09.json',parents=[fid],mimeType='application/json',data=json.dumps(D).encode(),modifiedTime=now())
  w=ctx.new_page();E2=[];w.on('pageerror',lambda e:E2.append(str(e)));w.on('dialog',lambda x:x.accept())
  w.clock.install()
  w.goto(URL);w.wait_for_timeout(500);w.evaluate("localStorage.clear()");w.reload();w.clock.run_for(4000);w.wait_for_timeout(500)
  out('web_empty',w.evaluate("(t=>t&&[t.innerText.split('\\n').slice(0,2).join(' '),!!t.querySelector('[data-gdlogin]'),!t.querySelector('[data-gddir]')])(document.querySelector('.toast.stem'))"))
  w.click('.toast.stem [data-gdlogin]');w.clock.run_for(3000);w.wait_for_timeout(3000);w.clock.run_for(2000);w.wait_for_timeout(1500)
  out('web_pulled',w.evaluate("[gdS().on,DB.ph.length,gdS().pn,!document.querySelector('.toast.stem'),(document.getElementById('gdst')||{}).textContent]"))
  n0=len([f for f in FILES.values() if f['name'].startswith('966-laptop-')])
  ed0=w.evaluate("gdS().ed||0")
  w.evaluate("(()=>{const p=DB.ph[0];p.name='تعديل من اللاب توب';sv()})()");w.wait_for_timeout(300)
  out('pending',[ed0,w.evaluate("[gdS().ed,!!GDE,document.getElementById('gdst').textContent]")])
  w.clock.run_for(61000);w.wait_for_timeout(2500)
  L=[f for f in FILES.values() if f['name'].startswith('966-laptop-')]
  out('auto_upload',[len(L),L and (json.loads(L[-1]['data'])['ph'][0]['name']),w.evaluate("[gdS().ed,document.getElementById('gdst').textContent]")])
  # phone writes a newer file -> read after 5 minutes, no upload loop
  P=json.loads(json.dumps(D));P['ph'][1]['name']='تعديل من الموبايل';P['ph'][1]['modAt']='2099-01-01T00:00:00Z'
  d2=nid();FILES[d2]=dict(id=d2,name='966-day-2026-11-10.json',parents=[fid],mimeType='application/json',data=json.dumps(P).encode(),modifiedTime='2099-01-01T00:00:00.000Z')
  up0=len([c for c in CALLS if c[1].startswith('/upload')])
  w.evaluate("window.__pc=0;const g=gdPull;gdPull=function(m){window.__pc++;return g(m)}")
  for i in range(31):w.clock.run_for(10000);w.wait_for_timeout(150)
  w.wait_for_timeout(2500);out('pc',w.evaluate("window.__pc"))
  out('dbg',w.evaluate("[DB.ph[1].name,gdS().pm,GDPB]"));w.evaluate("gdPull()");w.wait_for_timeout(3000);w.clock.run_for(2000);w.wait_for_timeout(1000)
  out('auto_read',w.evaluate("[DB.ph[1].name,gdS().pn,gdS().ed||0,!!GDE]"))
  w.clock.run_for(61000);w.wait_for_timeout(1500)
  out('no_loop',len([c for c in CALLS if c[1].startswith('/upload')])-up0)
  out('ERRS2',E2);br.close()

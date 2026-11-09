# v3.4 part 3: Google Drive from the web link (https). Google sign-in and the Drive API are faked in the test;
# checks: login, upload with laptop names, monthly Excel, automatic read and merge of the phone's newest file, list / restore.
import json, re, time, urllib.parse
from playwright.sync_api import sync_playwright
W='/home/claude/work/';HTML=open(W+'new34.html',encoding='utf-8').read();D=json.loads(open(W+'bk1106/data.json',encoding='utf-8').read())
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
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');ctx=br.new_context(viewport={'width':1200,'height':900},service_workers='block')
  ctx.route(URL+'**',lambda rt:rt.fulfill(status=200,content_type='text/html',body=HTML) if rt.request.url.rstrip('/').endswith('966ph-branding-app') or rt.request.url.endswith('index.html') else rt.fulfill(status=404,body=''))
  ctx.route('https://accounts.google.com/gsi/client',lambda rt:rt.fulfill(status=200,content_type='text/javascript',body=GSI))
  ctx.route('https://www.googleapis.com/**',drive)
  pg=ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)));DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:160]),x.accept()))
  # phone file already on Drive: folder + 966-day with an extra pharmacy
  fid=nid();FILES[fid]=dict(id=fid,name='966Ph Backups',parents=[],mimeType='application/vnd.google-apps.folder',data=b'',modifiedTime=now())
  P=json.loads(json.dumps(D));extra=json.loads(json.dumps(P['ph'][0]));extra['id']=999001;extra['no']='7777';extra['modAt']='2026-11-09T09:00:00Z';P['ph'].append(extra)
  d1=nid();FILES[d1]=dict(id=d1,name='966-day-2026-11-09.json',parents=[fid],mimeType='application/json',data=json.dumps(P).encode(),modifiedTime=now())
  pg.goto(URL);pg.wait_for_timeout(500);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D));pg.reload();pg.wait_for_timeout(2500)
  out('web',pg.evaluate("[GWEB(),!!DA(),location.protocol,!!document.querySelector('link[rel=manifest]'),!!document.querySelector('meta[name=apple-mobile-web-app-capable]')]"))
  pg.evaluate("goV({v:'gd',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('gd_screen',pg.evaluate("[document.querySelector('main').innerText.slice(0,160).replace(/\\s+/g,' '),!!document.querySelector('[data-gdlogin]'),!!document.querySelector('details[data-id=__gdo]')]"))
  pg.click('[data-gdlogin]');pg.wait_for_timeout(5000)
  out('login',pg.evaluate("[gdS().on,gdS().need,window.__gsi,window.__prompt,!!localStorage.getItem('966gwt')]"))
  out('pulled',[pg.evaluate("[gdS().pn,DB.ph.some(p=>p.no=='7777')]"),DL[-1:] ])
  out('files',sorted(f['name'] for f in FILES.values()))
  # automatic read does not repeat for the same file; a newer phone file is read again
  n0=len([c for c in CALLS if c[0]=='GET' and 'alt' in str(c)])
  pg.evaluate("gdPull()");pg.wait_for_timeout(1500);out('no_repeat',pg.evaluate("gdS().pn"))
  P['ph'][-1]['name']='اسم جديد من الموبايل';P['ph'][-1]['modAt']='2026-11-09T10:00:00Z';SEQ[0]+=1;d2=nid();FILES[d2]=dict(id=d2,name='966-day-2026-11-10.json',parents=[fid],mimeType='application/json',data=json.dumps(P).encode(),modifiedTime='2099-01-01T00:00:00.000Z')
  pg.evaluate("gdPull()");pg.wait_for_timeout(2000);out('newer',pg.evaluate("[gdS().pn,(DB.ph.find(p=>p.no=='7777')||{}).name]"))
  # upload forced day + month with Excel
  pg.evaluate("gdTick({day:1})");pg.wait_for_timeout(2500)
  pg.evaluate("(async()=>{const st=gdS();gdU(o=>{o.mon='2026-09';o.full='2026-11-09'});await gdTick()})()");pg.wait_for_timeout(6000)
  out('after_upload',sorted(f['name'] for f in FILES.values()))
  # list in the screen + restore by id
  pg.evaluate("goV({v:'gd',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);pg.click('[data-gdls]');pg.wait_for_timeout(1500)
  out('list',pg.evaluate("[...document.querySelectorAll('main h4')].map(h=>h.innerText)"))
  out('pull_card',pg.evaluate("(e=>e&&e.innerText.replace(/\\s+/g,' ').slice(0,140))([...document.querySelectorAll('.wcard')].find(w=>w.querySelector('[data-gdpull]')))"))
  out('ERRS',E)
  # file:// laptop: link note
  lp=br.new_page();lp.goto('file://'+W+'new34.html');lp.wait_for_timeout(1500);lp.evaluate("goV({v:'gd',op:{},dr:{},q:V.q})");lp.wait_for_timeout(200)
  out('file_note',lp.evaluate("[GWEB(),!!DA(),(document.querySelector('main .ywarn a')||{}).href]"))
  br.close()

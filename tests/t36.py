# v3.2: merge a laptop backup file from «استيراد ودمج» and from the phone Drive screen
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new32.html';D=open(W+'bk1102/data.json',encoding='utf-8').read();F=W+'t36/';import os;os.makedirs(F,exist_ok=True)
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
  for nat in [0,1]:
    pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:140]),x.accept()))
    if nat:pg.add_init_script("window.Capacitor={isNativePlatform:()=>true,Plugins:{DriveAuth:{authorize:async()=>({token:'t'}),clearToken:async()=>{}}}}")
    pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500)
    # build a "laptop" file: one pharmacy edited later, one new, the warehouse edited later; and an older edit that must lose
    lap=pg.evaluate("""(()=>{const q=JSON.parse(JSON.stringify(gdDay()));q.device='لاب توب';q.ph[0].name='من اللاب توب';q.ph[0].modAt='2099-01-01T00:00:00Z';q.ph[1].name='قديم';q.ph[1].modAt='2000-01-01T00:00:00Z';
      q.ph.push(Object.assign(JSON.parse(JSON.stringify(q.ph[0])),{id:888888,no:'77777',name:'جديدة من اللاب توب'}));const u=STO;q.uw[u].wh=(q.uw[u].wh||[]).concat([{id:'wl',nm:'صنف اللاب توب',qty:2}]);q.cfg.sat=Object.assign({},q.cfg.sat,{wh:'2099-01-01T00:00:00Z'});return JSON.stringify(q)})()""")
    open(F+'966-laptop-2026-11-05.json','w',encoding='utf-8').write(lap)
    a=pg.evaluate("[DB.ph[0].id,DB.ph[1].id,DB.ph[1].name,DB.ph.length+HID.length,SNAPS.length]")
    if nat:
      pg.evaluate("goV({v:'gd',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);out('gd_btn',pg.evaluate("(b=>b&&b.innerText)(document.querySelector('[data-pick=gdmfin]'))"));pg.set_input_files('#gdmfin',F+'966-laptop-2026-11-05.json')
    else:
      pg.evaluate("goV({v:'sync',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);out('sync_label',pg.evaluate("document.querySelector('#syncin').closest('label').innerText.split('\\n')[0]"));pg.set_input_files('#syncin',F+'966-laptop-2026-11-05.json')
    pg.wait_for_timeout(1500)
    out(('phone' if nat else 'laptop')+'_merge',[pg.evaluate(f"(A=>[A.find(p=>p.id=={a[0]}).name,A.find(p=>p.id=={a[1]}).name=={json.dumps(a[2])},A.length-{a[3]},A.some(p=>p.no=='77777'),(DB.wh||[]).some(x=>x.id=='wl'),SNAPS[0].why])(DB.ph.concat(HID))"),DL[-2:]])
    # an old-style sync file still works
    pg.evaluate("goV({v:'sync',op:{},dr:{},q:V.q})");open(F+'sync.json','w').write(pg.evaluate("JSON.stringify(syncPayload())"));pg.set_input_files('#syncin',F+'sync.json');pg.wait_for_timeout(800);out('old_sync',pg.evaluate("[V.v,!!(V.sy&&V.sy.res)]"))
    open(F+'bad.json','w').write('{"x":1}');n=len(DL);pg.set_input_files('#syncin',F+'bad.json');pg.wait_for_timeout(500);out('bad',DL[n:])
    out('ERRS',E);pg.close()
  br.close()

# v1.9 receiving screen, executed>received from warehouse, Wall Header OT — on the owner's 31-10 backup
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new.html';D=open(W+'bk1031/data.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(1800)
  out('mig',pg.evaluate("[DB.ph.length,DB.ph.filter(p=>p.m20).length,DB.ph.reduce((a,p)=>a+(p.rcv||[]).filter(e=>e.src=='old').length,0)]"))
  pid=pg.evaluate("DB.ph.find(p=>p.no=='825').id")
  # pharmacy checklist: received read-only
  pg.evaluate(f"goV({{v:'sum',sm:'ck',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
  out('ck_ro',pg.evaluate("[document.querySelectorAll('#rp [data-tv^=\"r\"]').length,document.querySelectorAll('#rp .tkro').length>0,!!document.querySelector('[data-rcvgo]')]"))
  pg.click('[data-rcvgo]');pg.wait_for_timeout(300)
  out('rcv_view',pg.evaluate("[V.v,V.rn,document.querySelectorAll('[data-tv^=\"r\"]').length>0,document.querySelector('header h1').innerText]"))
  # + on the first row
  tv=pg.evaluate("document.querySelector('[data-tv^=\"r:\"]').dataset.tv");k,tid,i=tv.split(':')
  b0=pg.evaluate(f"+curP().rows['{tid}'][{i}].r||0")
  pg.fill('#rcdt','2026-10-30');pg.dispatch_event('#rcdt','change');pg.wait_for_timeout(200)
  pg.click(f"[data-tk='{tv}:1']");pg.wait_for_timeout(200);pg.click(f"[data-tk='{tv}:1']");pg.wait_for_timeout(200)
  out('plus2',pg.evaluate(f"[{b0},+curP().rows['{tid}'][{i}].r,curP().rcv.filter(e=>e.src=='rcv').map(e=>[e.dt,e.n])]"))
  # receive by items: one requested (same as row 0 of fh) + one not requested
  pg.click('[data-rca]');pg.wait_for_timeout(300)
  out('rca_cards',pg.evaluate("[V.v,curP()._rc,document.querySelectorAll('main details[data-id]').length]"))
  fh0=pg.evaluate(f"JSON.stringify(DB.ph.find(p=>p.id=={pid}).rows.fh[0])");out('fh0',fh0)
  pg.evaluate(f"(()=>{{const y=JSON.parse({fh0!r});['r','x','_i','wf','ck'].forEach(k=>delete y[k]);y.q=1;RCP().rows.fh=[y];const t=T.find(t=>t.id=='wh'),P=DB.ph.find(p=>p.id=={pid});let c=null;for(const sec of S4)for(const nm of (NM[sec]||[]))for(const len of SZ('wh.len')){{const z={{sec,wt:'WALL NORMAL',nm,len,q:3}};if(!c&&!(P.rows.wh||[]).some(r=>rcSig(t,r,P.sh)==rcSig(t,z,P.sh)))c=z}}RCP().rows.wh=[c];render()}})()")
  st0=pg.evaluate("WU().filter(x=>x.ty=='Wall Header').reduce((a,x)=>a+x.qty,0)")
  fr0=pg.evaluate(f"+DB.ph.find(p=>p.id=={pid}).rows.fh[0].r||0")
  pg.click('[data-rcaok]');pg.wait_for_timeout(300)
  out('rca_save',pg.evaluate(f"(p=>[V.v,+p.rows.fh[0].r,WU().filter(x=>x.ty=='Wall Header').reduce((a,x)=>a+x.qty,0),p.rcv.filter(e=>e.src=='xs').map(e=>[e.n,e.z])])(DB.ph.find(p=>p.id=={pid}))")+[fr0,st0])
  out('toast',pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.innerText).slice(-1)"))
  # log list + delete the xs entry (back out of the warehouse)
  out('log_rows',pg.evaluate("document.querySelectorAll('[data-rcdel]').length"))
  xs=pg.evaluate(f"DB.ph.find(p=>p.id=={pid}).rcv.find(e=>e.src=='xs').id");pg.click(f"[data-rcdel='{xs}']");pg.wait_for_timeout(200)
  out('xs_undo',pg.evaluate("WU().filter(x=>x.ty=='Wall Header').reduce((a,x)=>a+x.qty,0)"))
  # unknown pharmacy -> waiting -> linked when added
  pg.fill('#rcno','99999');pg.dispatch_event('#rcno','change');pg.wait_for_timeout(200)
  out('unknown',pg.evaluate("[V.p,!!document.querySelector('.ywarn')]"))
  pg.click('[data-rca]');pg.wait_for_timeout(200)
  pg.evaluate("RCP().rows.ds=[{q:2}];render()");pg.click('[data-rcaok]');pg.wait_for_timeout(300)
  out('queue',pg.evaluate("RQ().map(q=>[q.no,q.tid,q.z])"))
  pg.evaluate("(()=>{const q=JSON.parse(JSON.stringify(DB.ph.find(p=>p.no=='825')));q.id=Date.now();q.no='99999';q.rows={ds:[{q:2}]};delete q.rcv;q.m20=1;DB.ph.push(q);sv();goV({v:'ph',p:q.id,op:{},dr:{},q:V.q})})()");pg.wait_for_timeout(400)
  out('linked',pg.evaluate("[RQ().length,curP().rows.ds[0].r,curP().rcv.map(e=>[e.src,e.n])]"))
  # executed > received with stock -> ask -> take from the warehouse
  pg.evaluate(f"(p=>{{const r=p.rows.fh[0];r.r=0;r.x=0;r.q=2;whParts(T.find(t=>t.id=='fh'),r,p.sh).forEach(y=>whAdd(y,5,'in','test','test'));sv()}})(DB.ph.find(p=>p.id=={pid}))")
  sk=pg.evaluate(f"(p=>{{const y=whParts(T.find(t=>t.id=='fh'),p.rows.fh[0],p.sh)[0];return +(whFind(whKey(y))||{{}}).qty}})(DB.ph.find(p=>p.id=={pid}))")
  pg.evaluate(f"goV({{v:'exec',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
  pg.click("[data-tk='x:fh:0:1']");pg.wait_for_timeout(300)
  out('ask',pg.evaluate("(t=>t?t.innerText.replace(/\\s+/g,' '):null)(document.querySelector('.toast.rcx'))"))
  pg.click('.toast.rcx [data-rcxw]');pg.wait_for_timeout(300)
  out('took',pg.evaluate(f"(p=>{{const r=p.rows.fh[0],y=whParts(T.find(t=>t.id=='fh'),r,p.sh)[0];return [r.r,r.x,r.wf,+(whFind(whKey(y))||{{}}).qty,p.rcv.filter(e=>e.rid==r._i&&e.dt==TD()).map(e=>[e.src,e.n])]}})(DB.ph.find(p=>p.id=={pid}))")+[sk])
  # no stock -> no question
  pg.evaluate("document.querySelectorAll('.toast').forEach(t=>t.remove())")
  pg.click("[data-tk='x:fh:0:1']");pg.wait_for_timeout(200);pg.click("[data-tk='x:fh:0:1']");pg.wait_for_timeout(200)
  out('later',pg.evaluate("[!!document.querySelector('.toast.rcx')]"))
  # received blocked outside the receiving screen
  out('blocked',pg.evaluate("(()=>{V.v='sum';const p=curP(),a=+p.rows.fh[0].r;tkRO('r')||0;return [tkRO('r'),tkRO('x')]})()"))
  # Wall Header Old Turkish
  out('wh_ot',pg.evaluate("(()=>{const t=T.find(t=>t.id=='wh'),r={sec:'Baby',wt:'WALL NORMAL',nm:'x',len:SZ('wh.len')[0],q:1};const r2=Object.assign({},r,{whm:FHM[1]});return [t.z(r,2),t.z(r2,2),t.z(r,0),t.f.find(f=>f.k=='whm').hide(r,0),t.f.find(f=>f.k=='whm').hide(r,2),whParts(t,r,2)[0].mat]})()"))
  # report
  pg.evaluate("goV({v:'rcv',rn:'825',rd:TD(),rcf:'2026-10-01',rct:TD(),op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('report',pg.evaluate("(L=>[L.length,L.map(x=>x.s).filter((v,i,a)=>a.indexOf(v)==i)])(rcvRep('2026-10-01',TD()))"))
  pg.evaluate("window._st=null;shareText=t=>{window._st=t}");pg.click("[data-rcrp=wa]");pg.wait_for_timeout(200);out('wa',pg.evaluate("(window._st||'').split('\\n').slice(0,6)"))
  out('pdf_el',pg.evaluate("rcvPdfEl('2026-10-01',TD(),rcvRep('2026-10-01',TD())).querySelectorAll('tr').length"))
  # backup carries rcv + queue
  out('backup',pg.evaluate("(o=>[o.ph.filter(p=>p.rcv&&p.rcv.length).length,JSON.stringify(o.uw).includes('rcvq')])(dbOut())"))
  pg.screenshot(path=W+'t24_rcv.png',full_page=True)
  out('ERRS',E)
  br.close()

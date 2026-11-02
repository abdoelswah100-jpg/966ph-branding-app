# v2.3 on the owner's 02-11 backup: screw caps, alerts
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new23.html';D=open(W+'bk1102/data.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept('50') if x.type=='prompt' else x.accept())
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2000)
  out('init',pg.evaluate("[DB.ph.every(p=>p.m23),DB.ph.map(p=>p.no+':'+capN(p,'q')+'/'+capN(p,'x')+'/'+p.capx).join(' '),WU().filter(x=>x.ty==CPNM).length]"))
  pid=pg.evaluate("DB.ph.find(p=>p.no=='825').id")
  out('pcs_825',pg.evaluate(f"(p=>CAPS.map(c=>[c[0],capPcs(p,c[0],'q'),capPcs(p,c[0],'x')]))(DB.ph.find(p=>p.id=={pid}))"))
  pg.evaluate(f"goV({{v:'sum',sm:'print',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(400)
  out('sum_order',pg.evaluate("[...document.querySelectorAll('#rp h3')].map(h=>h.innerText).slice(0,40)"))
  out('sum_cap',pg.evaluate("(h=>h?[...h.nextElementSibling.querySelectorAll('tr')].map(r=>r.innerText.replace(/\\s+/g,' ')):null)([...document.querySelectorAll('#rp h3')].find(h=>h.innerText=='غطاء مسمار'))"))
  pg.evaluate(f"goV({{v:'sum',sm:'mgmt',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(400)
  out('mg_h3',pg.evaluate("[...document.querySelectorAll('#rp h3')].map(h=>h.innerText.replace(/\\s+/g,' '))"))
  out('mg_cap',pg.evaluate("(h=>h?[...h.nextElementSibling.querySelectorAll('tr')].map(r=>r.innerText.replace(/\\s+/g,' ')):null)([...document.querySelectorAll('#rp h3')].find(h=>h.innerText=='غطاء مسمار'))"))
  # warehouse add
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.click('[data-whcap]');pg.wait_for_timeout(300)
  out('stock',pg.evaluate("WU().filter(x=>x.ty==CPNM).map(x=>[x.qty,x.unit,x.sh])"))
  # execute 1 more wall shelf piece -> 6 caps out
  i=pg.evaluate(f"DB.ph.find(p=>p.id=={pid}).rows.saw.findIndex(r=>(+r.x||0)<qn(r))");out('saw_i',i)
  if i<0:
    pg.evaluate(f"(p=>{{V.p=p.id;p.rows.saw[0].x=0;sv()}})(DB.ph.find(p=>p.id=={pid}))");i=0
  pg.evaluate(f"goV({{v:'exec',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
  s0=pg.evaluate("WU().find(x=>x.ty==CPNM).qty")
  pg.click(f"[data-tk='x:saw:{i}:1']");pg.wait_for_timeout(300)
  out('after_x',[s0,pg.evaluate("WU().find(x=>x.ty==CPNM).qty"),pg.evaluate("DB.wlog.filter(l=>l.ty==CPNM).slice(0,2).map(l=>[l.typ,l.qty,l.note])")])
  pg.click(f"[data-tk='x:saw:{i}:-1']");pg.wait_for_timeout(300)
  out('undo_x',pg.evaluate("WU().find(x=>x.ty==CPNM).qty"))
  # alerts
  out('alerts',pg.evaluate("DB.ph.map(p=>[p.no,alerts(p)]).filter(x=>x[1].length)"))
  out('alerts_tw',pg.evaluate("alerts({rows:{al:[{sec:'Beauty',h:50,lh:20,w:300,tw:200,q:1}],ws:[]},sh:0})"))
  out('ERRS',E)
  br.close()

# 2.0: Sticker outdoor kept in the warehouse + the one combined stock file
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=json.loads(open(W+'bk1115/data.json',encoding='utf-8').read())
F=json.load(open(W+'out47/966-مخزن-جرد-كامل-بعد-2.0-2026-11-15.json',encoding='utf-8'))
with sync_playwright() as pw:
  br=pw.chromium.launch();pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto('file://'+W+'new20.html');pg.wait_for_timeout(300)
  pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D,ensure_ascii=False));pg.reload();pg.wait_for_timeout(2500)
  out=lambda k,v:print(k,'=>',v)
  out('ver',pg.evaluate("VER"))
  out('WXT / so in NOSH',pg.evaluate("[WXT,NOSH.includes('so')]"))
  out('so fields',pg.evaluate("T.find(t=>t.id=='so').f.map(f=>f.k)"))
  out('so z no dir',pg.evaluate("T.find(t=>t.id=='so').z({nm:'طلباتك',h:30,w:60,q:1},0)"))
  out('so z dir',pg.evaluate("T.find(t=>t.id=='so').z({nm:'جهاز الخدمة الذاتية',h:25,w:50,dir:'يسار',q:1},0)"))
  out('so z بدون',pg.evaluate("T.find(t=>t.id=='so').z({nm:'أرباحي',h:25,w:50,dir:'بدون',q:1},0)"))
  out('wh before',pg.evaluate("[WU().length,Math.round(WU().reduce((a,x)=>a+(+x.qty||0),0)*100)/100]"))
  out('import open',pg.evaluate("f=>{whImpOpen(f,'test');return [WIMP.L.length,WIMP.L.filter(x=>!whImpOk(x)).map(x=>x.ty+' | '+x.nm+' | '+x.size)]}",F))
  pg.evaluate("whImpGo()");pg.wait_for_timeout(400)
  out('wh after',pg.evaluate("[WU().length,Math.round(WU().reduce((a,x)=>a+(+x.qty||0),0)*100)/100]"))
  out('so items',pg.evaluate("WU().filter(x=>x.ty=='ستيكر خارجي').map(x=>[x.sh,x.nm,x.size,x.mat,x.qty,x.unit])"))
  out('silicone',pg.evaluate("WU().filter(x=>/سيليكون/.test(x.nm)).map(x=>[x.sh,x.ty,x.nm,x.qty,x.unit])"))
  out('door/diecut',pg.evaluate("WU().filter(x=>x.ty=='Door sticker'||x.ty=='Die Cut').map(x=>[x.sh,x.ty,x.sec,x.size,x.qty])"))
  # requests pull from stock
  pg.evaluate("""()=>{const p=DB.ph.find(p=>p.st!='مكتملة');p.sh=4;p.rows=Object.assign({},p.rows,{
    so:[{nm:'جهاز الخدمة الذاتية',h:25,w:50,dir:'يمين',q:2},{nm:'جهاز الخدمة الذاتية',h:25,w:50,dir:'يسار',q:5},{nm:'طلباتك',h:25,w:50,q:1}],
    wh:[{sec:'Health',nm:'First aid',wt:'WALL NORMAL',len:'50',q:2},{sec:'Health',nm:'Cough & Cold',wt:'WALL WOOD Magnetic UNITS',len:'24×85',q:1}],
    dc:[{sec:'Baby',q:3}],ds:[{sz:'كبير 200×5',q:1}]});window._P=p}""")
  for tid,i in [('so',0),('so',1),('so',2),('wh',0),('wh',1),('dc',0),('ds',0)]:
    out(f'offer {tid}[{i}]',pg.evaluate(f"(t=>whFromOpts(_P,t,_P.rows.{tid}[{i}]).map(o=>o.k+' '+o.n+' '+o.txt.slice(0,80)))(T.find(t=>t.id=='{tid}'))"))
  out('manual add types has so',pg.evaluate("(()=>{V.we={};const h=wheHtml();V.we=null;return /ستيكر خارجي/.test(h)})()"))
  pg.evaluate("goV({v:'wh',op:{},dr:{},q:V.q})");pg.wait_for_timeout(500)
  out("wh page", pg.evaluate("[/ستيكر خارجي/.test(document.body.innerText), document.body.innerText.length]"))
  out('errors',E);br.close()

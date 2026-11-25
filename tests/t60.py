# 3.1 on the 25-11 backup
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=json.load(open(W+'bk1125/data.json',encoding='utf-8'))
o=lambda k,v:print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch();pg=br.new_page(viewport={'width':360,'height':800});E=[];M=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:(M.append(x.message[:120]),x.accept()))
  pg.goto('file://'+W+'new31.html');pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D,ensure_ascii=False));pg.reload();pg.wait_for_timeout(3500)
  o('ver',pg.evaluate("VER"))
  o('rolls',pg.evaluate("WU().filter(x=>x.ty==RLTY).map(x=>x.nm+' '+(x.sec||'-')+' '+x.size+' '+x.qty+' '+x.unit)"))
  o('old ws rolls left',pg.evaluate("WU().filter(x=>x.ty=='Wall Sticker').length"))
  o('owed after migration',pg.evaluate("DB.ph.map(p=>p.no+':'+rlOwed(p).join(',')).filter(s=>!/:$/.test(s))"))
  o('695 meters x',pg.evaluate("JSON.stringify(Object.fromEntries(Object.entries(rlMeters(DB.ph.find(p=>p.no=='695'&&p.mo=='2026-11'),'x')).map(([k,v])=>[k,v.m])))"))
  # new execution in 295 (Baby 70×1110 band) takes from the Baby roll
  o('execute 295 Baby band',pg.evaluate("""(()=>{const p=DB.ph.find(p=>p.no=='295');V.p=p.id;const b=WU().find(x=>x.ty==RLTY&&x.nm=='تخطيط'&&x.sec=='Baby').qty;const r=p.rows.ws.find(r=>r.sec=='Baby'&&r.w==1110);r.x=1;capAuto();const a=WU().find(x=>x.ty==RLTY&&x.nm=='تخطيط'&&x.sec=='Baby').qty;const lg=p.rows.ws.find(r=>r.kd=='لوجو');if(lg){lg.x=1;capAuto()}return [b,a,wq(b-a),WU().find(x=>x.ty==RLTY&&x.nm=='تخطيط'&&x.sec=='Baby').qty]})()"""))
  o('lyLen strips',pg.evaluate("[lyLen31([{h:220,w:10,n:7}]),lyLen31([{h:220,w:10,n:8}]),lyLen31([{h:70,w:575,n:1}]),lyLen31([{h:285,w:306,n:1}])]"))
  # outdoor sticker
  o('so parts',pg.evaluate("(()=>{const t=T.find(t=>t.id=='so');return [JSON.stringify(whParts(t,{nm:'جهاز الخدمة الذاتية',sa:'يمين',h:25,w:50,q:1},1).map(y=>[y.nm,y.size,whQty(y)])),JSON.stringify(whParts(t,{nm:'أرباحي',km:'ثلجي',h:25,w:50,q:1},1)),t.f.map(f=>f.k).join(',')]})()"))
  # statement
  pg.evaluate("(()=>{const x=WU().find(x=>x.ty=='End cap'&&/Vitamins/.test(x.nm)&&x.size=='64×111');V.we=Object.assign({},x,{_old:x.id});goV(Object.assign(V,{v:'whe'}))})()");pg.wait_for_timeout(500)
  o('statement',pg.evaluate("document.querySelector('.st31')&&document.querySelector('.st31').innerText.replace(/\\s+/g,' ').slice(0,300)"))
  o('width',pg.evaluate("[document.documentElement.scrollWidth,document.documentElement.clientWidth]"))
  # stock-take file
  f={"kind":"966-warehouse","mode":"set","note":"t","items":[{"ty":"رول ستيكر","nm":"تخطيط","sec":"Baby","size":"عرض 1 م","sh":-1,"qty":33},{"ty":"رول ستيكر","nm":"تخطيط","sec":"Health","size":"عرض 1 م","sh":-1,"qty":34}]}
  open(W+'t60set.json','w').write(json.dumps(f,ensure_ascii=False))
  pg.evaluate("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.set_input_files('#imp',W+'t60set.json');pg.wait_for_timeout(800)
  o('set sheet',pg.evaluate("document.querySelector('.csh')&&document.querySelector('.csh').innerText.replace(/\\s+/g,' ').slice(0,250)"))
  pg.evaluate("v24Click({jrd31:1},document.body)");pg.wait_for_timeout(400)
  o('after set',pg.evaluate("WU().filter(x=>x.ty==RLTY&&['Baby','Health'].includes(x.sec)).map(x=>x.sec+' '+x.qty)+' | '+DB.wlog.slice(0,2).map(e=>e.src+' '+e.qty+' '+e.note).join(' / ')"))
  # consumable
  o('consumable',pg.evaluate("(()=>{const x=WU().find(x=>x.ty=='أخرى');if(!x)return 'none';const q=x.qty;whClick({whst:x.id+':-1'},document.body);return [q,x.qty,DB.wlog[0].src,DB.wlog[0].note]})()"))
  o('errors',E);o('dialogs',M)

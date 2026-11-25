import json,base64
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=json.load(open(W+'bk1125/data.json',encoding='utf-8'))
with sync_playwright() as pw:
  br=pw.chromium.launch();pg=br.new_page(viewport={'width':360,'height':800});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto('file://'+W+'new30.html');pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D,ensure_ascii=False));pg.reload();pg.wait_for_timeout(3000)
  o=lambda k,v:print(k,'=>',v)
  o('ver',pg.evaluate("VER"))
  o('notes',pg.evaluate("DB.ph.filter(p=>['510','674','695','249','832','682','295'].includes(String(p.no))).map(p=>p.no+' rn=['+(p.rn||'')+'] pnt=['+(p.pnt||'')+']')"))
  g="DB.ph.find(p=>p.no=='674'&&p.mo=='2026-11')"
  o('674 rows',pg.evaluate(f"(p=>managementReportRows([p]).filter(x=>/Side Acrylic|غطاء/.test(x.n)).map(x=>[x.kind||'',x.n,x.sz,x.q,x.sw||''].join(' | ')))({g})"))
  pg.evaluate(f"(p=>{{const el=document.createElement('div');el.id='tt';el.innerHTML=mgmtHtml(p);document.body.appendChild(el)}})({g})")
  o('order',pg.evaluate("[...document.querySelectorAll('#tt h3')].map(h=>h.textContent.trim())"))
  o('swap note',pg.evaluate("[...document.querySelectorAll('#tt .swn')].map(x=>x.parentNode.textContent)"))
  o('caps table',pg.evaluate("(()=>{const h=[...document.querySelectorAll('#tt h3')].find(h=>/غطاء/.test(h.textContent));return h.nextElementSibling.innerText.replace(/\\s+/g,' ')})()"))
  # install-only caps
  pg.evaluate(f"(p=>{{p.capIO=4}})({g})")
  o('caps io',pg.evaluate(f"(p=>{{const el=document.createElement('div');el.innerHTML=mgmtHtml(p);const h=[...el.querySelectorAll('h3')].find(h=>/غطاء/.test(h.textContent));return h.nextElementSibling.textContent.replace(/\\s+/g,' ')}})({g})"))
  o('nail options',pg.evaluate("abSttO({it:'Decorative nail'})"))
  pg.evaluate(f"(p=>goV({{v:'ph',p:p.id,op:{{__pi:true}},dr:{{}},q:V.q}}))({g})");pg.wait_for_timeout(500)
  o('info fields',[pg.evaluate("!!document.getElementById('pnt30')"),pg.evaluate("!!document.getElementById('cio30')"),pg.evaluate("document.getElementById('pnt30')?.value")])
  o('width',pg.evaluate("[document.documentElement.scrollWidth,document.documentElement.clientWidth]"))
  b=pg.evaluate(f"""async()=>{{const p={g};const el=document.createElement('div');el.innerHTML=mgmtHtml(p);const b=await buildPdf(el,'t');const a=new Uint8Array(await b.arrayBuffer());let s='';for(let i=0;i<a.length;i+=8192)s+=String.fromCharCode.apply(null,a.subarray(i,i+8192));return btoa(s)}}""")
  open(W+'mr/v30-674.pdf','wb').write(base64.b64decode(b))
  o('errors',E)

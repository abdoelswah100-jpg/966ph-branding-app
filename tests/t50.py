# 1.8: WALL WOOD Magnetic for every section, any name; warehouse match by wood size
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=json.loads(open(W+'bk1106/data.json',encoding='utf-8').read())
with sync_playwright() as pw:
  br=pw.chromium.launch();pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto('file://'+W+'new19.html');pg.wait_for_timeout(300)
  pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D,ensure_ascii=False));pg.reload();pg.wait_for_timeout(2500)
  out=lambda k,v:print(k,'=>',v)
  T="T.find(t=>t.id=='wh')"
  for sec in ['Health','Beauty','Baby','Personal','Pharmacy']:
    r={'sec':sec,'wt':'WALL WOOD Magnetic UNITS'}
    out(sec+' wt',pg.evaluate(f"{T}.f.find(f=>f.k=='wt').o({json.dumps(r)},0)"))
    out(sec+' nm (first 5, count)',pg.evaluate(f"(L=>[L.slice(0,5),L.length])({T}.f.find(f=>f.k=='nm').o({json.dumps(r)},0))"))
    out(sec+' len',pg.evaluate(f"{T}.f.find(f=>f.k=='len').o({json.dumps(r)},0)"))
  out('normal Health nm count',pg.evaluate(f"{T}.f.find(f=>f.k=='nm').o({{sec:'Health',wt:'WALL NORMAL'}},0).length"))
  pg.evaluate("""()=>{const I=(o)=>Object.assign({min:'',sec:'',nm:'',mat:'',m22:1,m38:1,m39:1},o);
   const p=DB.ph.find(p=>p.st!='مكتملة');p.sh=0;p.rows={wh:[{sec:'Health',wt:'WALL WOOD Magnetic UNITS',nm:'Medical device',len:'24×85',q:1},{sec:'Beauty',wt:'WALL WOOD Magnetic UNITS',nm:'Hair colorants',len:'19×85',q:2}]};window._P=p;
   const y=whParts(T.find(t=>t.id=='wh'),p.rows.wh[0],0)[0];window._Y=y;
   DB.wh=[I(Object.assign({},y,{id:1,sh:-1,qty:1})),I(Object.assign({},whParts(T.find(t=>t.id=='wh'),p.rows.wh[1],0)[0],{id:2,sh:-1,qty:50}))];DB.wlog=[];sv()}""")
  out('part',pg.evaluate("_Y"))
  out('opts md',pg.evaluate(f"whFromOpts(_P,{T},_P.rows.wh[0]).map(o=>o.k+' '+o.n+' '+o.txt)"))
  out('opts hc',pg.evaluate(f"whFromOpts(_P,{T},_P.rows.wh[1]).map(o=>o.k+' '+o.n+' '+o.txt)"))
  pg.evaluate("goV({v:'ph',p:_P.id,op:{wh:1},dr:{},q:V.q})");pg.wait_for_timeout(500)
  out('card text',pg.evaluate("[...document.querySelectorAll('body *')].filter(e=>/Medical device/.test(e.textContent)&&!e.children.length).slice(0,3).map(e=>e.textContent.slice(0,120))"))
  # form: add new wood row in Health and pick a name
  pg.evaluate("goV({v:'add',p:_P.id,t:'wh',op:{},dr:{},q:V.q})");pg.wait_for_timeout(500)
  out('ver',pg.evaluate("VER"))
  out('errors',E);br.close()

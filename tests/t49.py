# 1.5 + 1.6 (warning when smaller): «مقاس قريب» for every type — End gandola part by part, Floor Header, nothing for far sizes
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=json.loads(open(W+'bk1106/data.json',encoding='utf-8').read())
HN='Health · Health care · نهتم بصحتك'
with sync_playwright() as pw:
  br=pw.chromium.launch();pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto('file://'+W+'new16.html');pg.wait_for_timeout(300)
  pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D,ensure_ascii=False));pg.reload();pg.wait_for_timeout(2500)
  out=lambda k,v:print(k,'=>',v)
  pg.evaluate("""HN=>{const I=(o)=>Object.assign({min:'',sec:'',nm:'',mat:'',m22:1,m38:1,m39:1},o);
   DB.wh=[I({id:1,sh:3,ty:'End gandola - Header',sec:'Health',nm:HN,size:'62×22',mat:'باك لايت',qty:3}),I({id:2,sh:0,ty:'End gandola - Side',sec:'Health',nm:HN,size:'25×101',mat:'ستيكر',qty:4}),
    I({id:3,sh:4,ty:'End gandola - Header',sec:'Health',nm:HN,size:'63.8×28.3',mat:'باك لايت',qty:5}),I({id:4,sh:3,ty:'End gandola - Header',sec:'Health',nm:HN,size:'86×22',mat:'باك لايت',qty:5})];DB.wlog=[];
   const p=DB.ph.find(p=>p.st!='مكتملة');p.sh=0;p.rows={eg:[{nm:HN,sz:'صغير',q:2}],fh:[{sec:'Health',nm:'Strong H Vitamins',sz:'صغير',q:1}]};window._P=p;sv()}""",HN)
  T="T.find(t=>t.id=='eg')"
  out('eg parts',pg.evaluate(f"whParts({T},_P.rows.eg[0],0).map(y=>y.ty+' '+y.size+' '+y.mat+' f'+y.f)"))
  out('eg opts',pg.evaluate(f"whFromOpts(_P,{T},_P.rows.eg[0]).map(o=>o.k+' '+o.n+' '+o.txt)"))
  pg.evaluate("goV({v:'ph',p:_P.id,op:{eg:1},dr:{},q:V.q})");pg.wait_for_timeout(400)
  pg.click('[data-whfrom="eg:0"]');pg.wait_for_timeout(300)
  b=pg.evaluate("[...document.querySelectorAll('[data-whf2]')].map(b=>b.innerText)");out('toast',b)
  pg.click('[data-whf2="0"]');pg.wait_for_timeout(400)   # sides (same size)
  out('after side',pg.evaluate("[_P.rows.eg[0].r||0,_P.rows.eg[0].wxs,_P.rows.eg[0].wxh,WU().map(x=>x.id+':'+x.qty).join(' ')]"))
  out('opts now',pg.evaluate(f"whFromOpts(_P,{T},_P.rows.eg[0]).map(o=>o.k+' '+o.n+' '+o.txt)"))
  pg.click('[data-whfrom="eg:0"]');pg.wait_for_timeout(300);pg.click('[data-whf2="0"]');pg.wait_for_timeout(400)
  out('after header',pg.evaluate("[_P.rows.eg[0].r,_P.rows.eg[0].wf,_P.rows.eg[0].wxs,_P.rows.eg[0].wxh,WU().map(x=>x.id+':'+x.qty).join(' '),DB.wlog[0].note]"))
  out('opts done',pg.evaluate(f"whFromOpts(_P,{T},_P.rows.eg[0]).length"))
  # Floor Header: needed 11.5×57 (Turkish small Health) ; stock Ukraine 12×53.5 (far: -3.5 height)  and a synthetic 12×57.5 Greek
  pg.evaluate("""()=>{const I=(o)=>Object.assign({min:'',sec:'',nm:'',mat:'',m22:1,m38:1,m39:1},o),y=whParts(T.find(t=>t.id=='fh'),_P.rows.fh[0],0)[0];window._Y=y;
   DB.wh.push(I({id:5,sh:3,ty:y.ty,sec:y.sec,nm:y.nm,size:'12×53.5',mat:y.mat,qty:2}),I({id:6,sh:4,ty:y.ty,sec:y.sec,nm:y.nm,size:'12×57.5',mat:y.mat,qty:2}));sv()}""")
  out('fh part',pg.evaluate("_Y.ty+' '+_Y.size+' '+_Y.mat"))
  out('fh opts',pg.evaluate("whFromOpts(_P,T.find(t=>t.id=='fh'),_P.rows.fh[0]).map(o=>o.k+' '+o.n+' '+o.txt)"))
  pg.evaluate("""HN=>{const I=(o)=>Object.assign({min:'',sec:'',nm:'',mat:'',m22:1,m38:1,m39:1},o);DB.wh.push(I({id:7,sh:0,ty:'End gandola - Header',sec:'Health',nm:HN,size:'61×22',mat:'باك لايت',qty:9}));DB.wh.find(x=>x.id==1).qty=0;_P.sh=3;_P.rows.eg=[{nm:HN,sz:'صغير',q:1}];sv()}""",HN)
  out('ukraine opts',pg.evaluate(f"whFromOpts(_P,{T},_P.rows.eg[0]).map(o=>o.k+' '+o.n+' '+o.txt)"))
  out('errors',E);br.close()

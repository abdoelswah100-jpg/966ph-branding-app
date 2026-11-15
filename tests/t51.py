# 1.9: receive file (review, apply, undo), routing, Old Turkish Wall = Floor stock, empty acrylic for «ستيكر + تصنيع أكريليك»
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=json.loads(open(W+'bk1115/data.json',encoding='utf-8').read())
with sync_playwright() as pw:
  br=pw.chromium.launch();pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto('file://'+W+'new19.html');pg.wait_for_timeout(300)
  pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D,ensure_ascii=False));pg.reload();pg.wait_for_timeout(2500)
  out=lambda k,v:print(k,'=>',v)
  # build a receive file from 510's own rows
  q=pg.evaluate("""()=>{const p=DB.ph.find(x=>x.no=='510'),cl=r=>{const y=JSON.parse(JSON.stringify(r));['_i','r','wf','wfpR','wfpL','wxs','wxh','rpR','rpL','x'].forEach(k=>delete y[k]);return y};
   const fh=p.rows.fh.map(cl),wh=p.rows.wh.map(cl);window._B={fh:p.rows.fh.map(r=>[r.q,r.r||0]),wh:p.rows.wh.map(r=>[r.q,r.r||0]),wl:DB.wh.length,wsum:DB.wh.reduce((a,x)=>a+(+x.qty||0),0)};
   fh[0].q=fh[0].q;fh[1].q=Math.max(0,fh[1].q-1);fh[2].q=fh[2].q+2;   // exact, short 1, extra 2
   const rows={fh:fh.slice(0,3),wh:[wh[0],Object.assign({},wh[0],{nm:'Mouthwash',sec:'Personal',q:3})]};   // 2nd = not requested
   return {kind:'966-receive',dt:'2026-11-16',note:'test',ph:[{no:'510',mod:p.mod,sh:p.sh,rows},{no:'99999',sh:0,rows:{wh:[wh[0]]}}]}}""")
  out('fh before',pg.evaluate("_B.fh.slice(0,3)"))
  pg.evaluate("q=>rcvImpOpen(q,'استلام-510.json')",q);pg.wait_for_timeout(400)
  out('sheet',pg.evaluate("document.querySelector('.csh').innerText.slice(0,900)"))
  pg.click('[data-rimgo]');pg.wait_for_timeout(600)
  out('view',pg.evaluate("[V.v,V.rn]"))
  out('fh after',pg.evaluate("DB.ph.find(x=>x.no=='510').rows.fh.slice(0,3).map(r=>[r.q,r.r||0])"))
  out('wh0 after',pg.evaluate("(r=>[r.q,r.r])(DB.ph.find(x=>x.no=='510').rows.wh[0])"))
  out('rcv log',pg.evaluate("DB.ph.find(x=>x.no=='510').rcv.map(e=>e.src+' '+e.n+' '+e.dt)"))
  out('wh stock +',pg.evaluate("[DB.wh.length-_B.wl,DB.wh.reduce((a,x)=>a+(+x.qty||0),0)-_B.wsum]"))
  out('queue',pg.evaluate("RQ().map(x=>x.no+' '+x.z)"))
  out('undo btn',pg.evaluate("!!document.querySelector('[data-rimundo]')"))
  # twice: second file adds on top (batches)
  pg.click('[data-rimundo]');pg.wait_for_timeout(500)
  out('after undo fh',pg.evaluate("DB.ph.find(x=>x.no=='510').rows.fh.slice(0,3).map(r=>[r.q,r.r||0])"))
  out('after undo log/stock/queue',pg.evaluate("[DB.ph.find(x=>x.no=='510').rcv.length,DB.wh.reduce((a,x)=>a+(+x.qty||0),0)-_B.wsum,RQ().length,!!DB.cfg.rimLast]"))
  # same file twice -> second adds
  pg.evaluate("q=>{rcvImpOpen(q,'a');rimGo();rcvImpOpen(q,'b');rimGo()}",q);pg.wait_for_timeout(500)
  out('twice fh',pg.evaluate("DB.ph.find(x=>x.no=='510').rows.fh.slice(0,3).map(r=>[r.q,r.r||0])"))
  pg.click('[data-rimundo]');pg.wait_for_timeout(400)
  out('undo last only',pg.evaluate("DB.ph.find(x=>x.no=='510').rows.fh.slice(0,3).map(r=>[r.q,r.r||0])"))
  # routing
  out('syncRoute',pg.evaluate("q=>{window._o=null;const a=rcvImpOpen;rcvImpOpen=(x,f)=>{_o=f};const r=[syncRoute(q,'s.json'),whImpOpen(q,'w.json')];rcvImpOpen=a;return [r[0],_o]}",q))
  # Old Turkish wall = floor
  out('migrated wall->floor',pg.evaluate("[WU().filter(x=>x.ty=='Wall Header'&&x.sh==2).length,WU().filter(x=>x.ty=='Floor Header'&&x.sh==2).map(x=>x.nm+' '+x.size+' '+x.mat+' '+x.qty).slice(0,8)]"))
  out('wh part sh2',pg.evaluate("whParts(T.find(t=>t.id=='wh'),{sec:'Personal',wt:'WALL NORMAL',nm:'Body Wash',len:'100',whm:'ستيكر فقط',q:1},2)"))
  out('wh part sh0',pg.evaluate("whParts(T.find(t=>t.id=='wh'),{sec:'Personal',wt:'WALL NORMAL',nm:'Body Wash',len:'100',q:1},0).map(y=>y.ty)"))
  pg.evaluate("""()=>{const I=o=>Object.assign({min:'',m22:1,m38:1,m39:1},o);DB.wh.push(I({id:9001,sh:2,ty:'Floor Header',sec:'Personal',nm:'Body Wash',size:'17.5×100',mat:'ستيكر فقط',qty:3}),I({id:9002,sh:2,ty:OLDT.bfh,nm:'',sec:'',size:'17.5×100',mat:'أكريليك فاضي',qty:4,old:1}));
   const p=DB.ph.find(x=>x.st!='مكتملة'&&x.no!='510');p.sh=2;p.dz='';p.rows={wh:[{sec:'Personal',wt:'WALL NORMAL',nm:'Body Wash',len:'100',whm:'ستيكر فقط',q:2},{sec:'Personal',wt:'WALL NORMAL',nm:'Hand Wash',len:'100',whm:'ستيكر + تصنيع أكريليك',q:2}]};window._P=p;sv()}""")
  out('wall pulls floor stock',pg.evaluate("whFromOpts(_P,T.find(t=>t.id=='wh'),_P.rows.wh[0]).map(o=>o.k+' '+o.n+' '+o.txt)"))
  out('acrylic offer (new design)',pg.evaluate("whFromOpts(_P,T.find(t=>t.id=='wh'),_P.rows.wh[1]).map(o=>o.k+' '+o.n+' '+o.txt)"))
  out('no acrylic for sticker-only',pg.evaluate("whOldOpts(_P,T.find(t=>t.id=='wh'),_P.rows.wh[0]).length"))
  out('ver',pg.evaluate("VER"));out('errors',E);br.close()

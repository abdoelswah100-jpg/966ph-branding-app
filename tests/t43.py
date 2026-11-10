# v3.7: End gandola header / side / acrylic counts, Roland Floor Header, warehouse import
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new37.html';D=open(W+'bk1106/data.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:200]),x.accept()))
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500)
  # ---- End gandola counts
  r=pg.evaluate("""(()=>{const base=DB.ph.find(p=>String(p.no)=='510');const q=JSON.parse(JSON.stringify(base));Object.assign(q,{id:777001,no:'9201',sh:0,name:'T',rows:{},rcv:[]});
    q.rows.eg=[{nm:'Baby (Small) · Body care · نهتم بطفلك',sz:'صغير',q:2},{nm:'Baby (Small) · Body care · نهتم بطفلك',sz:'صغير',q:2,eh:3,es:4},{nm:'Health · Vitamins · فيتامينات',sz:'كبير',q:1,eh:0,es:2,ea:2},{nm:'Health · Vitamins · فيتامينات',sz:'كبير',q:1,es:0}];DB.ph.push(q);sv();const t=T.find(x=>x.id=='eg');
    return [q.rows.eg.map(r=>t.z(r,0)),tTot(t,q.rows.eg,0),q.rows.eg.map(r=>whParts(t,r,0).map(y=>[y.ty.replace('End gandola - ',''),y.size,y.mat,y.f])),nqLines(q,'r').filter(x=>x.t.id=='eg').map(x=>[x.pt,x.sz,x.q,x.d]),tkProg(q,'r')]})()""")
  out('z',r[0]);out('tot',r[1]);out('parts',r[2]);out('short',r[3]);out('prog',r[4])
  out('aggr',pg.evaluate("(()=>{const L=aggr();return L.filter(x=>/gandola/.test(x.n)).map(x=>[x.n,x.q||x.t||JSON.stringify(x).slice(0,80)])})()"))
  out('sizes',pg.evaluate("sizeRows([DB.ph.find(p=>p.no=='9201')]).filter(x=>/gandola/.test(x.n)).map(x=>[x.n,x.sz,x.mat,x.q])"))
  # form fields shown
  pg.evaluate("goV({v:'ph',p:777001,op:{eg:1},dr:{},q:V.q});V.fo={eg:1};render()");pg.wait_for_timeout(300)
  out('form',pg.evaluate("['eh','es','ea'].map(k=>!!document.querySelector('[data-t=eg][data-k='+k+']'))"))
  # default rows unchanged (compare with an existing pharmacy)
  out('default_same',pg.evaluate("(()=>{const t=T.find(x=>x.id=='eg');return DB.ph.filter(p=>(p.rows.eg||[]).length).slice(0,2).map(p=>t.z(p.rows.eg[0],p.sh))})()"))
  # ---- warehouse: header only (side 0) through the add screen rows
  pg.evaluate("""(()=>{WU().length=0;const p=WHP();p.sh=0;p.rows={eg:[{nm:'Baby (Small) · Body care · نهتم بطفلك',sz:'صغير',q:4,eh:0}]};whaSave()})()""");pg.wait_for_timeout(300)
  out('wh_side_only',pg.evaluate("WU().map(x=>[x.ty,x.size,x.mat,x.qty])"))
  # ---- Roland
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('rol_toggle',pg.evaluate("!!document.querySelector('#whrol')"))
  pg.evaluate("""(()=>{const p=WHP();p.sh=0;V.whRol=true;p.rows={fh:[{sec:'Health',nm:'Vitamins',q:5}]};whaSave()})()""");pg.wait_for_timeout(300)
  out('rol_items',pg.evaluate("WU().filter(x=>x.rol).map(x=>[x.ty,x.nm,x.sec,x.size,x.mat,x.qty])"))
  pid=pg.evaluate("""(()=>{const q=DB.ph.find(p=>p.id==777001);q.rows.fh=[{sec:'Health',nm:'Vitamins',q:3},{sec:'Beauty',nm:'Sun care',q:2}];sv();return q.id})()""")
  out('rol_opts',pg.evaluate(f"(p=>whFromOpts(p,T.find(t=>t.id=='fh'),p.rows.fh[0]).map(o=>[o.rol||0,o.txt]))(DB.ph.find(p=>p.id=={pid}))"))
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{fh:1}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);pg.click('[data-whfrom="fh:0"]');pg.wait_for_timeout(300)
  out('rol_toast',pg.evaluate("document.querySelector('.toast').innerText.replace(/\\s+/g,' ').slice(0,220)"))
  pg.click('.toast .rolb');pg.wait_for_timeout(300)
  out('rol_taken',pg.evaluate(f"(p=>[p.rol,p.rows.fh[0].r,WU().find(x=>x.rol).qty,DB.wlog[0].note,nqLines(p,'r').filter(x=>x.t.id=='fh').map(x=>[x.nm,x.mat,x.d])])(DB.ph.find(p=>p.id=={pid}))"))
  pg.evaluate("goV({v:'wh',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('rol_bar',pg.evaluate("[(document.querySelector('.rolbar')||{}).innerText,!!document.querySelector('[data-whrolf]')]"))
  pg.click('[data-rolx]');pg.wait_for_timeout(300);out('rol_closed',pg.evaluate(f"[DB.cfg.rolOff,!document.querySelector('.rolbar'),(p=>whFromOpts(p,T.find(t=>t.id=='fh'),p.rows.fh[0]).filter(o=>o.rol).length)(DB.ph.find(p=>p.id=={pid}))]"))
  # ---- import file
  f=W+'t43_wh.json';open(f,'w',encoding='utf-8').write(json.dumps({'kind':'966-warehouse','note':'test','items':[{'sh':'Regular Turkish','ty':'Side Acrylic Shelves Floor · تصميم قديم','nm':'يمين','sec':'Health','mat':'أكريليك + ستيكر','size':'صغير 30×120','qty':1,'old':1,'real':'118.5×30'},{'sh':0,'ty':'End gandola - Side','nm':'Baby (Small) · Body care · نهتم بطفلك','sec':'Baby','mat':'ستيكر','size':'25×101','qty':6}]},ensure_ascii=False))
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);n0=pg.evaluate("WU().length")
  pg.set_input_files('#whimpin',f);pg.wait_for_timeout(600)
  out('imp_sheet',pg.evaluate("[document.querySelector('.csh b').innerText,[...document.querySelectorAll('.csh .cnpi')].map(x=>x.innerText.replace(/\\s+/g,' ').slice(0,120))]"))
  pg.click('[data-whimgo]');pg.wait_for_timeout(400)
  out('imp_done',pg.evaluate(f"[WU().length-{n0},WU().filter(x=>x.old).map(x=>[x.real,x.qty]),WU().filter(x=>x.ty=='End gandola - Side').map(x=>x.qty)]"))
  out('mnt_types',pg.evaluate("mAds().filter(x=>/gandola/.test(x))"))
  out('ERRS',E);br.close()

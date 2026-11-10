# v3.8: End gandola part by part, deodorant header + Care side, Fridge two kinds, shared stock, A3 names, boards by modification type
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new38.html';D=open(W+'bk1106/data.json',encoding='utf-8').read()
F=W+'whimp/966-مخزن-جرد-2026-11-10.json'
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:200]),x.accept()))
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500)
  out('ver',pg.evaluate("VER"))
  out('a3_split',pg.evaluate("DB.ph.filter(p=>(p.rows.ab||[]).some(r=>r.it==ABA3)).map(p=>[p.no,p.mod,(p.rows.ab||[]).filter(r=>r.it==ABA3).map(r=>[r.an||'-',r.q,r.r??'',r.x??'',r.stt].join(':'))])"))
  out('mnt_fr',pg.evaluate("MU().items.filter(x=>/Fridge/.test(x.ad)).map(x=>[x.ad,x.det.slice(0,20)])"))
  # warehouse import
  pg.evaluate("WU().length=0;goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.set_input_files('#whimpin',F);pg.wait_for_timeout(600);pg.click('[data-whimgo]');pg.wait_for_timeout(500)
  out('shared_sh',pg.evaluate("WU().filter(x=>/Fridge|care 4|Camera|ضفها|Acrylic/.test(x.ty)).map(x=>[x.ty.slice(0,14),x.nm.slice(0,22),x.sh,x.qty])"))
  # old merge of stock: item with sh 0 + same item sh 1 -> one
  out('merge38',pg.evaluate("(()=>{DB.wh.push({id:5,sh:1,ty:'Camera sticker',nm:'',sec:'',mat:'—',size:'A5',qty:4});DB.wh.push({id:6,sh:0,ty:'Camera sticker',nm:'',sec:'',mat:'—',size:'A5',qty:1});return WU().filter(x=>x.ty=='Camera sticker').map(x=>[x.sh,x.qty])})()"))
  # Old Turkish pharmacy
  pid=pg.evaluate("""(()=>{const b=DB.ph.find(x=>x.no=='809');const p=JSON.parse(JSON.stringify(b));Object.assign(p,{id:9911,no:'9911',rcv:[],sh:2,st:'جديدة',whT:{}});
   p.rows={eg:[{nm:'Personal · Premium Deo · مزيلات عرق طبية',sz:'قياسي',q:1,egp:'باك لايت + ستيكر بس'},{nm:'عناية',sz:'قياسي',q:2,egp:'باك لايت + ستيكر بس'}],fr:[{kd:'ثلاجة عصير',q:2},{kd:'ثلاجة أدوية',q:1}],c4:[{sz:'كبير 50×180',q:1}],ab:[{it:'Acrylic board A3',an:'ارباحي',q:1,stt:'تركيب فقط'}]};DB.ph.push(p);sv();return p.id})()""")
  T="(p=>Object.keys(p.rows).flatMap(k=>p.rows[k].map((r,i)=>[k,i,whFromOpts(p,T.find(t=>t.id==k),r).map(o=>o.k+':'+o.txt)])))(DB.ph.find(p=>p.id==%d))"%pid
  out('opts',pg.evaluate(T))
  # deodorant: full pull = deo header + 2 Care sides
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{eg:1}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);pg.evaluate("document.querySelectorAll('.toast').forEach(t=>t.remove())");pg.click('[data-whfrom="eg:0"]');pg.wait_for_timeout(300)
  out('deo_toast',pg.evaluate("document.querySelector('.toast').innerText.replace(/\\s+/g,' ').slice(0,200)"));pg.click('.toast [data-whf2="0"]');pg.wait_for_timeout(300)
  out('deo_after',pg.evaluate(f"(p=>[p.rows.eg[0].r,WU().filter(x=>/End gandola/.test(x.ty)&&/عناية|deo/i.test(x.nm)).map(x=>[x.ty.slice(14),x.nm.slice(0,16),x.qty])])(DB.ph.find(p=>p.id=={pid}))"))
  # care: header stock to 0, two gondolas, sides 7 left -> part offer
  pg.evaluate("WU().find(x=>x.ty=='End gandola - Header'&&x.nm=='عناية').qty=0;sv()")
  out('care_opts',pg.evaluate(f"(p=>whFromOpts(p,T.find(t=>t.id=='eg'),p.rows.eg[1]).map(o=>o.k+':'+o.txt))(DB.ph.find(p=>p.id=={pid}))"))
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{eg:1}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);pg.click('[data-whfrom="eg:1"]');pg.wait_for_timeout(300);pg.click('.toast [data-whf2="0"]');pg.wait_for_timeout(300)
  out('care_after',pg.evaluate(f"(p=>{{const r=p.rows.eg[1];return [r.r||0,r.wxs,r.wxh,nqLines(p,'r').filter(x=>x.t.id=='eg').map(x=>[x.nm.slice(0,12),x.pt,x.q,x.v,x.d]),tkProg(p,'r'),WU().find(x=>x.ty=='End gandola - Side'&&x.nm=='عناية').qty]}})(DB.ph.find(p=>p.id=={pid}))"))
  pg.evaluate("WU().find(x=>x.ty=='End gandola - Header'&&x.nm=='عناية').qty=1;sv()")
  out('care_opts2',pg.evaluate(f"(p=>whFromOpts(p,T.find(t=>t.id=='eg'),p.rows.eg[1]).map(o=>o.k+':'+o.txt))(DB.ph.find(p=>p.id=={pid}))"))
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{eg:1}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);pg.click('[data-whfrom="eg:1"]');pg.wait_for_timeout(300);pg.click('.toast [data-whf2="0"]');pg.wait_for_timeout(300)
  out('care_after2',pg.evaluate(f"(p=>{{const r=p.rows.eg[1];return [r.r,r.wf,r.wxs,r.wxh,nqLines(p,'r').filter(x=>x.t.id=='eg').map(x=>[x.pt,x.d])]}})(DB.ph.find(p=>p.id=={pid}))"))
  # fridge
  out('fr_tot',pg.evaluate(f"(p=>tTot(T.find(t=>t.id=='fr'),p.rows.fr,p.sh))(DB.ph.find(p=>p.id=={pid}))"))
  out('fr_aggr',pg.evaluate("aggr().filter(x=>x.n=='Fridge sticker'||x.n=='Acrylic boards').map(x=>[x.n,x.sc,x.q])"))
  out('fr_size',pg.evaluate("sizeRows(DB.ph).filter(x=>/Fridge|A3/.test(x.n)).map(x=>[x.n,x.q,x.st||''])"))
  out('mgr',pg.evaluate("managementReportRows(DB.ph).filter(x=>/Fridge|A3/.test(x.n)).map(x=>[x.n,x.q,x.st||''])"))
  out('mads',pg.evaluate("mAds().filter(x=>/Fridge/.test(x))"))
  out('nq_fr_ab',pg.evaluate(f"(p=>nqLines(p,'r').filter(x=>['fr','ab'].includes(x.t.id)).map(x=>[x.nm,x.d]))(DB.ph.find(p=>p.id=={pid}))"))
  # maintenance offer for fridge (shared stock)
  DL.clear();pg.evaluate("whMntOffer({ph:'9911',ad:'Fridge sticker - ثلاجة أدوية',sz:'30×60',q:1,dt:'2026-11-10'})");out('mnt_offer',DL[:1])
  # new pharmacies by modification type
  res={}
  for mod in ['تعديل براندنج','براندنج جديد','صيانة']:
    pg.evaluate("goV({v:'add',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
    pg.fill('#pno','77'+str(len(res)));pg.select_option('#pmod',mod);pg.click('#addp');pg.wait_for_timeout(300)
    res[mod]=pg.evaluate("(p=>(p.rows.ab||[]).map(r=>abNm(r).replace('Acrylic board ','')+'|'+r.stt))(curP())")
  out('new_ab',res)
  # change modification type of the last («صيانة») -> تعديل براندنج
  pg.evaluate("(()=>{const m=document.querySelector('#pmod');m.value='تعديل براندنج';m.dispatchEvent(new Event('change',{bubbles:true}))})()");pg.wait_for_timeout(300)
  out('mod_change_from_mnt',pg.evaluate("[curP().mod,(curP().rows.ab||[]).length]"))
  pg.evaluate("(()=>{const p=DB.ph.find(x=>x.no=='771');goV({v:'ph',p:p.id,op:{},dr:{},q:V.q})})()");pg.wait_for_timeout(300)
  pg.evaluate("(()=>{const m=document.querySelector('#pmod');m.value='تعديل براندنج';m.dispatchEvent(new Event('change',{bubbles:true}))})()");pg.wait_for_timeout(300)
  out('mod_change',pg.evaluate("[curP().mod,(curP().rows.ab||[]).map(r=>r.stt).join(',')]"))
  # form shows the name only for A3
  pg.evaluate("(()=>{const p=curP();goV({v:'ph',p:p.id,op:{ab:1},dr:{},q:V.q});V.fo={ab:1};V.dr={ab:{it:'Acrylic board A3'}};render()})()");pg.wait_for_timeout(300)
  a=pg.evaluate("!!document.querySelector('[data-t=ab][data-k=an]')")
  pg.evaluate("V.dr={ab:{it:'No smoking acrylic'}};render()");pg.wait_for_timeout(200)
  out('an_field',[a,pg.evaluate("!!document.querySelector('[data-t=ab][data-k=an]')")])
  out('ERRS',E);br.close()

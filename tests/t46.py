# 1.2: Medicated Header one stock (migration of stock + transferred keys), new names, import: repeated file, undo, name fix, new names
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new12.html';D=json.loads(open(W+'bk1106/data.json',encoding='utf-8').read())
F=W+'jard/966-مخزن-Medicated-Header-2026-11-12.json'
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:160]),x.accept()))
  pg.goto(APP);pg.wait_for_timeout(300)
  pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',JSON.stringify(d))}",D);pg.reload();pg.wait_for_timeout(2500)
  out('ver',pg.evaluate("VER"))
  # old-version stock: header per shelf type + a pharmacy that transferred header surplus
  pg.evaluate("""(()=>{const M=o=>Object.assign({min:'',unit:'قطعة',m22:1,m38:1,m39:1},o);WU();DB.wh.length=0;
   DB.wh.push(M({id:'a1',sh:0,ty:'Medicated - Header',nm:'AVENE',sec:'',mat:'باك لايت',size:'12×83',qty:15,min:3}),M({id:'a2',sh:3,ty:'Medicated - Header',nm:'AVENE',sec:'',mat:'باك لايت',size:'12×83',qty:4}),M({id:'a3',sh:4,ty:'Medicated - Header',nm:'Vichy',sec:'',mat:'باك لايت',size:'12×83',qty:2}),M({id:'a4',sh:3,ty:'Medicated - Side',nm:'AVENE',sec:'',mat:'باك لايت',size:'33×72',qty:3}));
   const p=DB.ph[0];p.whT={'0|Medicated - Header|avene||باك لايت|12×83':{sh:0,ty:'Medicated - Header',nm:'AVENE',sec:'',mat:'باك لايت',size:'12×83',q:2}};DB.ph.forEach(p=>delete p.m12);sv()})()""")
  pg.evaluate("localStorage.setItem('ads',JSON.stringify(dbOut()))");pg.reload();pg.wait_for_timeout(2500)
  out('stock',pg.evaluate("WU().map(x=>[x.id,x.sh,x.ty.slice(12),x.nm,x.qty,x.min])"))
  out('whT',pg.evaluate("Object.values(DB.ph[0].whT).map(e=>[e.sh,e.nm,e.q])+' | plan '+JSON.stringify(whPlan(DB.ph[0]).filter(x=>/Medicated/.test(x.ty)).map(x=>[x.sh,x.nm,x.dl]))"))
  pg.wait_for_timeout(5500);out('snap',pg.evaluate("snaps().map(x=>x.why)"))
  out('names',pg.evaluate("['A-Derma','Tricovel','Xerolan'].map(n=>MED.includes(n))"))
  out('parts',pg.evaluate("(()=>{const t=T.find(x=>x.id=='md');return [0,3,4].map(s=>whParts(t,{nm:'AVENE',mdp:'Header + Side',q:1},s).map(y=>[y.ty.slice(12),y.sh,y.size]))})()"))
  out('pull_uk',pg.evaluate("(()=>{const t=T.find(x=>x.id=='md');const L=whRowPlan(t,{nm:'AVENE',mdp:MDP[0],q:2},3);return [MDP[0],L.nm,whXT(t,{nm:'AVENE',mdp:MDP[0],q:2},3,2)]})()"))
  out('cat',pg.evaluate("(()=>{WCK=null;const L=whCatalog().filter(x=>x.ty=='Medicated - Header');return [L.length,[...new Set(L.map(x=>x.sh))],L.some(x=>x.nm=='Xerolan')]})()"))
  # import the real file
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.set_input_files('#whimpin',F);pg.wait_for_timeout(1500)
  out('imp1',pg.evaluate("[document.querySelectorAll('.csh .wimpbad').length,document.querySelectorAll('.csh .wimpdup').length,document.querySelector('[data-whimgo]').className]"))
  pg.click('[data-whimgo]');pg.wait_for_timeout(500)
  out('after1',pg.evaluate("[WU().length,WU().reduce((a,x)=>a+x.qty,0),WU().find(x=>x.nm=='AVENE'&&x.ty=='Medicated - Header').qty]"))
  out('snap_imp',pg.evaluate("snaps()[0].why"))
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('undo_btn',pg.evaluate("(document.querySelector('[data-wiundo]')||{}).innerText"))
  # same file again: warning; add anyway (dialog accepted)
  pg.set_input_files('#whimpin',F);pg.wait_for_timeout(1500)
  out('imp2',pg.evaluate("[document.querySelector('.csh .wimpdup')&&document.querySelector('.csh .wimpdup').innerText.slice(0,80),document.querySelector('[data-whimgo]').innerText]"))
  DL.clear();pg.click('[data-whimgo]');pg.wait_for_timeout(500);out('dlg2',DL)
  out('after2',pg.evaluate("[WU().reduce((a,x)=>a+x.qty,0),WU().find(x=>x.nm=='AVENE'&&x.ty=='Medicated - Header').qty]"))
  # pull some, then undo the second import
  pg.evaluate("(()=>{const x=WU().find(x=>x.nm=='Dermagor');whAdd(x,-8,'out','test','سحب تجربة')})()")
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);DL.clear();pg.click('[data-wiundo]');pg.wait_for_timeout(800);out('dlg_undo',DL)
  out('after_undo',pg.evaluate("[WU().reduce((a,x)=>a+x.qty,0),WU().find(x=>x.nm=='AVENE'&&x.ty=='Medicated - Header').qty,WU().find(x=>x.nm=='Dermagor').qty,!!wiLast(),wiLast()&&wiLast().fn]"))
  # undo the first one too: items it created are removed
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);DL.clear();pg.click('[data-wiundo]');pg.wait_for_timeout(800)
  out('after_undo2',pg.evaluate("[WU().length,WU().map(x=>[x.nm,x.sh,x.qty]),!!wiLast(),!!document.querySelector('[data-wiundo]')]"))
  # a file imported with the old version (same file name in the log)
  pg.evaluate("DB.wlog.unshift({at:'2026-11-11T18:00:00.000Z',typ:'in',id:'zz',qty:3,src:'import',note:'استيراد من ملف · 966-old.json',nm:'',ty:'',size:'',sh:-1});sv()")
  f2=W+'966-old.json';open(f2,'w',encoding='utf-8').write(json.dumps({'kind':'966-warehouse','items':[{'sh':3,'ty':'Medicated - Side','nm':'AVENE','sec':'','mat':'باك لايت','size':'33×72','qty':1}]},ensure_ascii=False))
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.set_input_files('#whimpin',f2);pg.wait_for_timeout(1200)
  out('legacy_dup',pg.evaluate("!!document.querySelector('.csh .wimpdup')"));pg.click('[data-cshx]')
  # name fix + new name
  f3=W+'t46_names.json';open(f3,'w',encoding='utf-8').write(json.dumps({'kind':'966-warehouse','items':[
    {'sh':0,'ty':'Medicated - Header','nm':'Bio Balance','sec':'','mat':'باك لايت','size':'12×83','qty':2},
    {'sh':0,'ty':'Medicated - Header','nm':'dr.organic','sec':'','mat':'باك لايت','size':'12×83','qty':1},
    {'sh':0,'ty':'Medicated - Side','nm':'Sesderma','sec':'','mat':'باك لايت','size':'30×75','qty':4},
    {'sh':0,'ty':'Medicated - Header','nm':'Sesderma','sec':'','mat':'باك لايت','size':'12×83','qty':1},
    {'sh':0,'ty':'Medicated - Side','nm':'Vichy','sec':'','mat':'باك لايت','size':'99×99','qty':1}]},ensure_ascii=False))
  pg.set_input_files('#whimpin',f3);pg.wait_for_timeout(1500)
  out('names_sheet',pg.evaluate("[[...document.querySelectorAll('.csh .cnpi')].map(x=>x.innerText.replace(/\\s+/g,' ').slice(0,140)),!!document.querySelector('[data-wixn]')]"))
  DL.clear();pg.click('[data-wixn]');pg.wait_for_timeout(1500);out('dlg_xn',DL)
  out('names_after',pg.evaluate("[MED.includes('Sesderma'),DB.cfg.xn.md,[...document.querySelectorAll('.csh .winew,.csh .wimpbad')].map(x=>x.innerText.slice(0,50))]"))
  pg.click('[data-whimgo]');pg.wait_for_timeout(500)
  out('names_stock',pg.evaluate("WU().filter(x=>/Biobalance|Organic|Sesderma/.test(x.nm)).map(x=>[x.ty.slice(12),x.nm,x.sh,x.qty])"))
  # md form offers the new names
  out('md_opts',pg.evaluate("(()=>{const t=T.find(x=>x.id=='md');return ['A-Derma','Xerolan','Sesderma'].map(n=>t.f[0].o({},0).includes(n))})()"))
  out('ERRS',E);br.close()

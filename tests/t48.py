# 1.4: «ضفها للسلة» names + migration, End cap «مقاس قريب», import size prefix, sync button with a pharmacies file, Skin care
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';M=W+'maint/';D=json.loads(open(W+'bk1106/data.json',encoding='utf-8').read())
for p in D['ph']:
  if p['no']=='1103' and p['mo']=='2026-11':p['st']='مكتملة';p['mod']='براندنج جديد'
I=lambda **k:dict(dict(id=k.pop('id'),min='',sec='',nm='',mat=''),**k)
D['wh']=[I(id=901,sh=-1,ty='ضفها للسلة - سايد',size='68×102',mat='مات فيلم',qty=6),I(id=902,sh=-1,ty='ضفها للسلة - هيدر',size='20×65',mat='مات فيلم',qty=12),
 I(id=903,sh=-1,ty='ضفها للسلة - سايد',nm='الأساسي',size='68×102',mat='مات فيلم',qty=1),
 I(id=904,sh=0,ty='End cap',sec='Health',nm='Vitamins · فيتامينات',size='81×123',mat='MATMAT',qty=3),
 I(id=905,sh=3,ty='End cap',sec='Health',nm='Vitamins · فيتامينات',size='88×132',mat='MATMAT',qty=5),
 I(id=906,sh=1,ty='End cap',sec='Health',nm='Vitamins · فيتامينات',size='79.5×121',mat='MATMAT',qty=1),
 I(id=907,sh=1,ty='End cap',sec='Health',nm='Vitamins · فيتامينات',size='78×122',mat='MATMAT',qty=4),
 I(id=908,sh=0,ty='End cap',sec='Health',nm='First aid',size='81×123',mat='MATMAT',qty=4)]
D['wlog']=[]
g=[p for p in D['ph'] if p['st']!='مكتملة'][0];g.setdefault('rows',{})['ga']=[{'q':1}];GN=g['no']
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:600]),x.accept()))
  pg.goto('file://'+W+'new14.html');pg.wait_for_timeout(300)
  mt=pg.evaluate("SZ('mt.ec')");s=json.dumps(D,ensure_ascii=False).replace('MATMAT',mt)
  pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",s);pg.reload();pg.wait_for_timeout(2500)
  pg.evaluate("w=>{DB.wh=w;sv();render()}",json.loads(s)['wh'])
  out('ver',pg.evaluate("VER"))
  out('skin care personal',pg.evaluate("EC.Personal.includes('Skin care · العناية بالبشرة')"))
  out('ga stock',pg.evaluate("WU().filter(x=>/^ضفها/.test(x.ty)).map(x=>[x.ty,x.nm,x.qty])"))
  out('ga row',pg.evaluate(f"DB.ph.find(p=>p.no=='{GN}').rows.ga"))
  pg.wait_for_timeout(5500);out('snap',pg.evaluate("snaps().map(s=>s.why).filter(w=>/1.4/.test(w))"))
  out('ga opts',pg.evaluate("[GAL.slice(),opts(T.find(t=>t.id=='ga').f[0],{},0)]"))
  # custom name
  pg.evaluate("DB.cfg.xn=DB.cfg.xn||{};DB.cfg.xn.ga=['عروض رمضان'];xnApply()");out('ga opts+xn',pg.evaluate("GAL.slice()"))
  out('catalog ga',pg.evaluate("whCatalog().filter(x=>/^ضفها/.test(x.ty)).map(x=>x.ty+'|'+x.nm).sort()"))
  # pharmacy row named أجواء صيفية: report + z + pull
  pg.evaluate(f"(()=>{{const p=DB.ph.find(p=>p.no=='{GN}');p.rows.ga.push({{nm:'أجواء صيفية',q:2}});sv()}})()")
  out('z',pg.evaluate(f"DB.ph.find(p=>p.no=='{GN}').rows.ga.map(r=>T.find(t=>t.id=='ga').z(r))"))
  out('sizeRows',pg.evaluate(f"sizeRows([DB.ph.find(p=>p.no=='{GN}')]).filter(x=>/ضفها/.test(x.n)).map(x=>x.n+' '+x.q)"))
  out('opts basic',pg.evaluate(f"(()=>{{const p=DB.ph.find(p=>p.no=='{GN}');const t=T.find(t=>t.id=='ga');return p.rows.ga.map(r=>whFromOpts(p,t,r).map(o=>o.txt))}})()"))
  # End cap near size: Greek large 80×122 needs 3 (1 received)
  pg.evaluate("(()=>{const p=DB.ph.find(p=>p.st!='مكتملة');p.sh=4;p.rows.ec=[{sec:'Health',sz:'كبير 80×122',nm:'Vitamins · فيتامينات',q:3,r:1},{sec:'Health',sz:'كبير 80×122',nm:'First aid',q:1},{sec:'Health',sz:'كبير 91.5×122',nm:'Vitamins · فيتامينات',q:1}];window._P=p;sv()})()")
  out('ec opts',pg.evaluate("_P.rows.ec.map(r=>whFromOpts(_P,T.find(t=>t.id=='ec'),r).map(o=>o.k+' '+o.n+' '+o.txt))"))
  # pull through the toast
  pg.evaluate("goV({v:'ph',p:_P.id,op:{ec:1},dr:{},q:V.q})");pg.wait_for_timeout(500)
  pg.click('[data-whfrom="ec:0"]');pg.wait_for_timeout(300)
  out('toast',pg.evaluate("[...document.querySelectorAll('[data-whf2]')].map(b=>b.innerText)"))
  pg.click('[data-whf2="0"]');pg.wait_for_timeout(500)
  out('after pull',pg.evaluate("[_P.rows.ec[0].r,_P.rows.ec[0].wf,WU().filter(x=>x.ty=='End cap').map(x=>x.id+':'+x.qty).join(' '),(DB.wlog[0]||{}).note]"))
  out('ec opts after',pg.evaluate("whFromOpts(_P,T.find(t=>t.id=='ec'),_P.rows.ec[0]).map(o=>o.txt)"))
  # warehouse import: «كبير 81×123» and an unnamed ضفها للسلة
  F={'kind':'966-warehouse','items':[{'sh':0,'ty':'End cap','sec':'Personal','nm':'Skin care · العناية بالبشرة','mat':mt,'size':'كبير 81×123','qty':2},{'sh':3,'ty':'End cap','sec':'Baby','nm':'','mat':mt,'size':'صغير 67×117','qty':1},{'sh':-1,'ty':'ضفها للسلة - هيدر','nm':'','mat':'مات فيلم','size':'20×65','qty':4},{'sh':-1,'ty':'ضفها للسلة - سايد','nm':'أجواء صيفية','mat':'مات فيلم','size':'68×102','qty':8}]}
  open(W+'t48_wh.json','w').write(json.dumps(F,ensure_ascii=False))
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.set_input_files('#whimpin',W+'t48_wh.json');pg.wait_for_timeout(1200)
  out('imp rows',pg.evaluate("[...document.querySelectorAll('.csh .cnpi')].map(x=>x.innerText.replace(/\\s+/g,' ').slice(0,150))"))
  pg.click('[data-whimgo]');pg.wait_for_timeout(500)
  out('imp stock',pg.evaluate("WU().filter(x=>x.wi).map(x=>[x.ty,x.nm,x.size,x.qty])"))
  # sync button with the pharmacies merge file: no «newest wins», completed 1103 untouched
  orig=pg.evaluate("JSON.stringify(DB.ph.find(p=>p.no=='1103'&&p.st=='مكتملة').rows)")
  pg.evaluate("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(400);DL.clear()
  pg.set_input_files('#syncin',M+'966-صيانة-Riyadh2-26-صيدلية-2026-11 (نهائي).json');pg.wait_for_timeout(1500)
  out('sync dlgs',[d[:120] for d in DL])
  out('after sync',pg.evaluate(f"[DB.ph.filter(p=>p.no=='1103'&&p.mo=='2026-11').map(p=>[p.mod,p.st]),JSON.stringify(DB.ph.find(p=>p.no=='1103'&&p.st=='مكتملة').rows)==={json.dumps(orig)},DB.ph.filter(p=>p.mod=='صيانة'&&p.mo=='2026-11').length,snaps()[0].why]"))
  DL.clear();pg.set_input_files('#syncin',W+'t48_wh.json');pg.wait_for_timeout(800);out('sync wh file',[DL[:1],pg.evaluate("!!document.querySelector('[data-whimgo]')")])
  pg.evaluate("cShClose()")
  # a real full backup still merges (newest wins)
  full=pg.evaluate("JSON.stringify(dbOut())");open(W+'t48_full.json','w').write(full);DL.clear()
  pg.evaluate("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.set_input_files('#syncin',W+'t48_full.json');pg.wait_for_timeout(1200);out('full backup dlg',[d[:60] for d in DL])
  out('errors',E);br.close()

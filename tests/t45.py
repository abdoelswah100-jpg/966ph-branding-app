# v3.9: names, Big -> size migration, Ukraine wide, Care 40x100, rolls, old sides with names, import check, catalog, Turkish no-warning
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new39.html';D=json.loads(open(W+'bk1106/data.json',encoding='utf-8').read())
# seed stock that must be migrated
D.setdefault('cfg',{})
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:200]),x.accept()))
  pg.goto(APP);pg.wait_for_timeout(300)
  # put old-version stock in before the app starts
  pg.evaluate("d=>{localStorage.clear();d.wh=[{id:1,sh:0,ty:'End cap',nm:'Baby milk - Big · حليب الطفل',sec:'Baby',mat:'باك لايت',size:'81×123',qty:2,min:'',unit:'قطعة',m22:1,m38:1},{id:2,sh:0,ty:'End cap',nm:'baby milk · حليب الطفل',sec:'Baby',mat:'باك لايت',size:'81×123',qty:1,min:'',unit:'قطعة',m22:1,m38:1},{id:3,sh:-1,ty:'Sticker care 4 life',nm:'',sec:'',mat:'ستيكر',size:'50×100',qty:6,min:'',unit:'قطعة',m22:1,m38:1},{id:4,sh:-1,ty:'رول ستيكر',nm:'رملي',sec:'',mat:'',size:'عرض 1.27 م',qty:10,min:'',unit:'متر',m22:1,m38:1},{id:5,sh:-1,ty:'رول ستيكر',nm:'ثلجي شفاف',sec:'',mat:'',size:'عرض 1.27 م',qty:35,min:'',unit:'متر',m22:1,m38:1}];localStorage.setItem('ads',JSON.stringify(d))}",D);pg.reload();pg.wait_for_timeout(2500)
  out('ver',pg.evaluate("VER"))
  out('snap',pg.evaluate("snaps().map(x=>x.why)"))
  out('rows',pg.evaluate("DB.ph.flatMap(p=>[...(p.rows.ec||[]).filter(r=>/milk|Food|Bath|Geriatric/.test(r.nm)).map(r=>['ec',p.no,r.nm,r.sz]),...(p.rows.fh||[]).concat(p.rows.wh||[]).filter(r=>/Healthy/.test(r.nm)).map(r=>['fwh',p.no,r.nm,r.sz||'']),...(p.rows.c4||[]).map(r=>['c4',p.no,r.sz])])"))
  out('tpl',pg.evaluate("(DB.tp||[]).flatMap(t=>[...((t.rows||{}).ec||[]).map(r=>[r.nm,r.sz]),...((t.rows||{}).c4||[]).map(r=>r.sz)])"))
  pg.wait_for_timeout(5500);out('snap2',pg.evaluate("snaps().map(x=>x.why)"))
  out('stock',pg.evaluate("(()=>{DB.wh.push({id:'z1',sh:0,ty:'End cap',nm:'Baby milk - Big · حليب الطفل',sec:'Baby',mat:'باك لايت',size:'81×123',qty:2,min:'',unit:'قطعة',m22:1,m38:1},{id:'z2',sh:0,ty:'End cap',nm:'baby milk · حليب الطفل',sec:'Baby',mat:'باك لايت',size:'81×123',qty:1,min:'',unit:'قطعة',m22:1,m38:1},{id:'z3',sh:-1,ty:'Sticker care 4 life',nm:'',sec:'',mat:'ستيكر',size:'50×100',qty:6,min:'',unit:'قطعة',m22:1,m38:1},{id:'z4',sh:-1,ty:'رول ستيكر',nm:'رملي',sec:'',mat:'',size:'عرض 1.27 م',qty:10,min:'',unit:'متر',m22:1,m38:1},{id:'z5',sh:-1,ty:'رول ستيكر',nm:'ثلجي شفاف',sec:'',mat:'',size:'عرض 1.27 م',qty:35,min:'',unit:'متر',m22:1,m38:1});return WU().filter(x=>['z1','z2','z3','z4','z5'].includes(x.id)).map(x=>[x.ty.slice(0,12),x.nm,x.size,x.qty])})()"))
  out('lists',pg.evaluate("[MED.includes('ISDIN'),EC.Health.slice(-3),EC.Beauty.slice(-2),EC.Personal.slice(-1),EC.Baby,EG.filter(x=>/Baby Food|New Arrival/.test(x)),NM.Health.filter(x=>/Healthy/.test(x)),RLK,SZ('c4')]"))
  # parts / sizes
  r=pg.evaluate("""(()=>{const t=n=>T.find(x=>x.id==n);const eg=t('eg'),fh=t('fh');return [
   whParts(eg,{nm:'Personal · Mouthwash · غسول الفم',sz:'قياسي',q:1,egp:'باك لايت + ستيكر بس'},2).map(y=>[y.ty.slice(14),y.nm,y.size]),
   whParts(eg,{nm:'Baby · Baby Food · طعام الطفل',sz:'قياسي',q:1,egp:'باك لايت + ستيكر بس'},2).map(y=>[y.ty.slice(14),y.nm]),
   whParts(eg,{nm:'عناية',sz:'قياسي',q:1,egp:'باك لايت + ستيكر بس'},2).map(y=>[y.ty.slice(14),y.nm]),
   eg.z({nm:'New Arrival · وصل حديثاً',sz:'صغير',q:2},0),
   fh.f.find(f=>f.k=='sz').o({sec:'Health'},3),fh.f.find(f=>f.k=='sz').o({sec:'Baby'},3),fh.f.find(f=>f.k=='sz').o({sec:'Baby'},0),
   [fh.z({sec:'Health',nm:'Kids Vitamins',sz:'عريض كبير'},3),fh.z({sec:'Baby',nm:'Baby milk',sz:'عريض صغير'},3),fh.z({sec:'Health',nm:'Healthy Drinks',sz:'كبير'},0)],
   !!imgOf('Healthy Drinks','Health'),!!imgOf('Healthy food','Health')]})()""")
  for i,x in enumerate(r):out('p'+str(i),x)
  # old sides with name + picture
  pg.evaluate("goV({v:'who',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200)
  pg.select_option('select[data-wo=k]','saf');pg.wait_for_timeout(100);pg.select_option('select[data-wo=sec]','Baby');pg.wait_for_timeout(100)
  pg.select_option('select[data-wo=nm2]','Baby milk');pg.wait_for_timeout(100);pg.select_option('select[data-wo=sd]','يسار');pg.wait_for_timeout(100)
  out('who_img',pg.evaluate("(document.querySelector('.woim img')||{}).src?.slice(0,30)"))
  pg.fill('[data-wo=q]','2');pg.dispatch_event('[data-wo=q]','change');pg.click('[data-whosave]');pg.wait_for_timeout(300)
  out('who_item',pg.evaluate("WU().filter(x=>x.old).map(x=>[x.ty,x.nm,x.sec,x.size,x.qty,!!osImg(x)])"))
  out('who_card_img',pg.evaluate("[...document.querySelectorAll('.whc img.whimg')].length"))
  # offered to an old-design pharmacy row with the same side
  out('who_offer',pg.evaluate("""(()=>{const b=DB.ph.find(p=>p.no=='510');const q=JSON.parse(JSON.stringify(b));Object.assign(q,{id:7771,no:'7771',sh:0,dz:'قديم',rows:{saf:[{sec:'Baby',sz:'صغير 30×120',sd:'يسار',q:1},{sec:'Baby',sz:'صغير 30×120',sd:'يمين',q:1}]},rcv:[]});DB.ph.push(q);sv();return q.rows.saf.map(r=>whOldOpts(q,T.find(t=>t.id=='saf'),r).map(o=>o.txt))})()"""))
  # Turkish shelf types: no warning; Ukraine still warns
  out('cross',pg.evaluate("""(()=>{WU().push({id:91,sh:0,ty:'Medicated - Side',nm:'AVENE',sec:'',mat:'باك لايت',size:'30×75',qty:5,min:'',unit:'قطعة'});const t=T.find(x=>x.id=='md');WU().push({id:92,sh:3,ty:'Medicated - Side',nm:'VICHY',sec:'',mat:'باك لايت',size:'30×75',qty:5,min:'',unit:'قطعة'});return [whXT(t,{nm:'AVENE',mdp:'Side بس',q:1},1,1),whXT(t,{nm:'AVENE',mdp:'Side بس',q:1},2,1),whCross({sh:1,ty:'Medicated - Side',nm:'VICHY',sec:'',mat:'باك لايت',size:'30×75'},1)]})()"""))
  # catalog + import check
  out('catalog',pg.evaluate("(()=>{const L=whCatalog();return [L.length,L.filter(x=>x.nm=='ISDIN').length,L.filter(x=>/Healthy Drinks/.test(x.nm)).length,L.some(x=>/Big|small/i.test(x.nm)&&x.ty=='End cap')]})()"))
  f=W+'t45_wh.json';open(f,'w',encoding='utf-8').write(json.dumps({'kind':'966-warehouse','items':[
    {'sh':0,'ty':'Floor Header','nm':'Hair & Skin Vitamins','sec':'Health','mat':'باك لايت','size':'11.5×76','qty':3},
    {'sh':0,'ty':'Floor Header','nm':'Hair and Skin Vitamin','sec':'Health','mat':'باك لايت','size':'11.5×76','qty':2},
    {'sh':-1,'ty':'رول ستيكر','nm':'رملي','size':'عرض 1 م','qty':5,'unit':'متر'},
    {'sh':0,'ty':'Side Acrylic Shelves Floor · تصميم قديم','nm':'OTC · يمين','sec':'Health','mat':'أكريليك + ستيكر','size':'صغير 30×120','qty':1,'old':1}]},ensure_ascii=False))
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);pg.set_input_files('#whimpin',f);pg.wait_for_timeout(800)
  out('imp_sheet',pg.evaluate("[document.querySelector('.csh small').innerText.slice(0,200),[...document.querySelectorAll('.csh .cnpi')].map(x=>!!x.querySelector('.wimpbad'))]"))
  pg.click('[data-whimgo]');pg.wait_for_timeout(300)
  out('imp_roll',pg.evaluate("WU().filter(x=>x.ty==RLTY).map(x=>[x.nm,x.size,x.qty])"))
  # export
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('cat_btn',pg.evaluate("!!document.querySelector('[data-whcat]')"))
  out('ERRS',E);br.close()

# 2.4: A4 / Wasfaty, acrylic work type, row wrap, damaged, swap by the customer, screw caps, «وصفاتي» migration
import json,copy
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D0=json.load(open(W+'bk1116/data.json',encoding='utf-8'))
def run(pg,js,arg=None):return pg.evaluate(js,arg) if arg is not None else pg.evaluate(js)
def load(pg,D,E):
  pg.goto('file://'+W+'new24.html');pg.wait_for_timeout(300)
  pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D,ensure_ascii=False));pg.reload();pg.wait_for_timeout(2800)
with sync_playwright() as pw:
  br=pw.chromium.launch();pg=br.new_page(viewport={'width':360,'height':800});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  out=lambda k,v:print(k,'=>',v)
  load(pg,D0,E)
  out('ver',run(pg,"VER"))
  out('ABI',run(pg,"ABI.join(' | ')"))
  out('A4 name/size',run(pg,"[abNm({it:'Acrylic board A4',an:'ارباحي'}),ABV('Acrylic board A4').join('|'),ABV('Wasfaty board').join('|')]"))
  out('z A4',run(pg,"T.find(t=>t.id=='ab').z({it:'Acrylic board A4',an:'ارباحي',q:2,stt:'تركيب فقط'},0)"))
  # default work by pharmacy type
  out('stt order',run(pg,"""(()=>{const o=[];const m=DB.ph.find(p=>p.no=='510'&&p.mo=='2026-11'),n=DB.ph.find(p=>p.mod=='براندنج جديد');
    V.p=m.id;o.push('mod A3: '+abSttO({it:'Acrylic board A3'})[0]);o.push('mod nail: '+abSttO({it:'Decorative nail'})[0]);o.push('mod nosmoke: '+abSttO({it:'No smoking acrylic'})[0]);
    V.p=n.id;o.push('new A3: '+abSttO({it:'Acrylic board A3'})[0]);return o})()"""))
  out('whParts io/made',run(pg,"(t=>[whParts(t,{it:'Acrylic board A3',an:'ارباحي',q:1,stt:'تركيب فقط'},0).length,JSON.stringify(whParts(t,{it:'Acrylic board A4',an:'ارباحي',q:1,stt:'تصنيع وتركيب'},0))])(T.find(t=>t.id=='ab'))"))
  out('nq 510 ab lines (install only excluded)',run(pg,"(p=>nqLines(p,'r').filter(x=>x.t.id=='ab').map(x=>x.nm+' '+x.stt+' '+x.d))(DB.ph.find(p=>p.no=='510'&&p.mo=='2026-11'))"))
  out('mgMerge A4',run(pg,"JSON.stringify(mgMerge([{n:'Acrylic board A4 · ارباحي',sz:'A4',mat:'أكريليك',q:2,st:'x'},{n:'Acrylic board A4 · الضمان الصحي',sz:'A4',mat:'أكريليك',q:1,st:'x'},{n:'Acrylic board A3 · ارباحي',sz:'A3',mat:'أكريليك',q:1,st:'x'}]).map(x=>x.n+':'+x.q))"))
  # form: open 510, add an acrylic board → default
  run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='510'&&p.mo=='2026-11');goV({v:'ph',p:p.id,op:{ab:true},dr:{},q:V.q});V.fo={ab:true};render()})()");pg.wait_for_timeout(600)
  out('form A3 default (510 mod)',run(pg,"(()=>{const f=document.querySelector('[data-add=ab]').closest('.fm'),it=f.querySelector('select[data-k=it]');it.value='Acrylic board A3';it.dispatchEvent(new Event('change',{bubbles:true}));return 1})()"));pg.wait_for_timeout(400)
  out('form stt default (510 mod)',run(pg,"(()=>{const s=document.querySelector('[data-add=ab]').closest('.fm').querySelector('select[data-k=stt]');return s?[...s.options].map(o=>o.value+(o.selected?'*':'')).join(' | '):'no select'})()"))
  out('hk field in forms',run(pg,"T.filter(t=>t.f.some(f=>f.k=='hk')).length+' of '+T.length"))
  # layout: a long note must not widen the page (360px)
  run(pg,"(()=>{const p=curP();const L=p.rows.wh||p.rows.fh;L[0].nt='ملاحظة طويلة جدا جدا للتجربة '.repeat(6);L[0].xi='نعم';L[0].xn='لغاه العميل بعد الطباعة وبدله ب ٨ سايد اكريليك وده نص طويل';V.op.wh=true;V.op.fh=true;render()})()");pg.wait_for_timeout(500)
  out('page width 360',run(pg,"[document.documentElement.scrollWidth,document.documentElement.clientWidth,document.body.scrollWidth]"))
  pg.set_viewport_size({'width':400,'height':800});pg.wait_for_timeout(300)
  out('page width 400',run(pg,"[document.documentElement.scrollWidth,document.documentElement.clientWidth]"))
  pg.screenshot(path=W+'t55-rows.png',full_page=False)
  # damaged: received 15, executed 10, damaged 5 → no surplus; without damaged → 5
  out('surplus with/without hk',run(pg,"""(()=>{const p=curP(),r=(p.rows.wh||[])[0];if(!r)return 'no wh';const t=T.find(t=>t.id=='wh');r.q=15;r.r=15;r.x=10;r.hk=5;const a=whSurplus(p);delete r.hk;const b=whSurplus(p);const k=whKey(whParts(t,r,p.sh)[0]);return [(a[k]||{}).q||0,(b[k]||{}).q||0]})()"""))
  out('hk tag',run(pg,"(()=>{const p=curP(),r=p.rows.wh[0];r.hk=2;render();return !!document.querySelector('.rshc.hkt')})()"))
  # swap: gandola row of 510 (header + sides)
  run(pg,"(()=>{const p=curP();V.op.eg=true;render()})()");pg.wait_for_timeout(300)
  out('swap buttons',run(pg,"document.querySelectorAll('[data-swo]').length"))
  out('eg row',run(pg,"(()=>{const p=curP(),r=(p.rows.eg||[])[0];if(!r)return 'no eg';r.r=qn(r);r.x=qn(r);return T.find(t=>t.id=='eg').z(r,p.sh)})()"))
  run(pg,"swOpen('eg',0)");pg.wait_for_timeout(300)
  out('swap parts',run(pg,"SWP.P.map(o=>o.y.ty+' | '+o.y.mat+' | n='+o.n+' | sticker='+o.st+' | '+(o.v||'?')).join(' ;; ')"))
  out('go without choosing stickers',run(pg,"(()=>{const n=SWP.P.filter(o=>!o.v).length;swGo();return [n,!!SWP]})()"))
  run(pg,"SWP.P.forEach((o,j)=>{if(!o.v)o.v=j%2?'wh':'hk'})");run(pg,"swGo()");pg.wait_for_timeout(500)
  out('after swap',run(pg,"(()=>{const p=curP(),r=p.rows.eg[0];return {cx:r.cx,hk:r.sw&&r.sw.hk,draft:!!V.dr.eg,swf:V.dr.eg&&V.dr.eg.swf,newHasR:V.dr.eg&&('r' in V.dr.eg)}})()"))
  out('surplus of swapped row',run(pg,"(()=>{const p=curP(),S=whSurplus(p);return Object.values(S).filter(y=>/gandola/i.test(y.ty)).map(y=>y.ty+' '+(y.nm||'')+' = '+y.q)})()"))
  # save the new row with another name
  out('choose name',run(pg,"(()=>{V.dr.eg.nm='Personal · Personal Care · نهتم بعنايتك';V.dr.eg.sec='Personal';render();return V.dr.eg.nm})()"))
  pg.wait_for_timeout(300)
  pg.click('[data-add="eg"]');pg.wait_for_timeout(600)
  out('after save',run(pg,"(()=>{const p=curP(),L=p.rows.eg;const o=L[0],n=L.find(x=>x.swf);return {n:L.length,orig_to:o.sw&&o.sw.to,newSwf:n&&n.swf,tags:[...document.querySelectorAll('.rshc.swt')].map(x=>x.textContent)}})()"))
  out('mgmt counts original (cx)',run(pg,"(()=>{const p=curP(),r=p.rows.eg[0];return [r.cx,qn(r)]})()"))
  # caps
  out('caps 674',run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='674'&&p.mo=='2026-11');const h=capHtml(p);return [capN(p,'q'),capNeed(p),capStock(),/ناقص/.test(h)]})()"))
  # damaged from the warehouse
  out('wh damaged',run(pg,"(()=>{const x=WU().find(y=>+y.qty>3);const q0=+x.qty;window.prompt=(m,d)=>/السبب/.test(m)?'اتقطع':'2';v24Click({whhk:String(x.id)},document.body);const l=DB.wlog[DB.wlog.length-1]||DB.wlog[0];return [q0,+x.qty,JSON.stringify(DB.wlog.find(y=>y.src=='dmg'))]})()"))
  out('errors',E)
  # «وصفاتي» migration
  D=copy.deepcopy(D0);D['cfg']['adTypes']=['لوحة وصفاتي'];p=[x for x in D['ph'] if x['no']=='510' and x['mo']=='2026-11'][0];p['rows']['custom_0']=[{'q':2,'nt':'تجربة'}]
  D['uw']['u4']['wh'].append({'id':999,'sh':-1,'ty':'لوحة وصفاتي','nm':'','sec':'','mat':'','size':'','qty':3,'unit':'قطعة','m22':1,'m38':1})
  E2=[];pg.on('pageerror',lambda e:E2.append(str(e)));load(pg,D,E2);pg.wait_for_timeout(2500)
  out('wsf mig',run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='510'&&p.mo=='2026-11');return {types:DB.cfg.adTypes,custom:!!p.rows.custom_0,ab:(p.rows.ab||[]).filter(r=>r.it=='Wasfaty board').map(r=>r.q+' '+r.stt+' '+r.nt),wh:WU().filter(x=>/Wasfaty/.test(x.nm)).map(x=>x.ty+'|'+x.size+'|'+x.qty),flag:DB.cfg.m24w}})()"))
  out('errors2',E2);br.close()

# v1.9 on the owner's 31-10 backup: letters to / from the warehouse, letters max width, Floor Header OT, old design, curve note, boards status, dates, received>=executed, backup version, month close, roll request vs management report.
import base64
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new.html';D=open(W+'bk1031/data.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:120]),x.accept()))
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(1800)
  id_=lambda no:pg.evaluate(f"DB.ph.find(p=>p.no=='{no}').id")
  p809,p825,p843,p1533=id_('809'),id_('825'),id_('843'),id_('1533')
  out('migRX_1533_ws0',pg.evaluate(f"(r=>[r.r,r.x])(DB.ph.find(p=>p.id=={p1533}).rows.ws[0])"))
  # 809: Health letters received 2, executed 1 -> surplus to the warehouse
  pg.evaluate(f"(p=>{{const r=p.rows.al.find(r=>r.sec=='Health');r.r=2;r.x=1;sv()}})(DB.ph.find(p=>p.id=={p809}))")
  out('plan_809',pg.evaluate(f"whPlan(DB.ph.find(p=>p.id=={p809})).map(x=>[x.ty,x.sec,x.size,x.dl])"))
  pg.evaluate(f"goV({{v:'ph',p:{p809},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(200);pg.evaluate(f"whOffer(DB.ph.find(p=>p.id=={p809}))");pg.wait_for_timeout(300);pg.click('[data-whgo]');pg.wait_for_timeout(300)
  out('stock_after_809',pg.evaluate("WU().filter(x=>x.ty=='Acrylic letters 8 mm').map(x=>[x.sec,x.size,x.qty,x.sh])"))
  # 825: Health letters not received yet -> 📦 من المخزن (different size from 809)
  pg.evaluate(f"(p=>{{const r=p.rows.al.find(r=>r.sec=='Health'&&r.sz=='كبير');r.r=0;r.x=0;sv()}})(DB.ph.find(p=>p.id=={p825}))")
  pg.evaluate(f"goV({{v:'ph',p:{p825},op:{{al:true}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
  btn=pg.evaluate("(b=>b?b.dataset.whfrom:null)(document.querySelector('details[data-id=al] [data-whfrom]'))");out('from_btn',btn)
  if btn:
    pg.click(f"[data-whfrom='{btn}']");pg.wait_for_timeout(300);out('from_toast',pg.evaluate("document.querySelector('.toast.rem').innerText.replace(/\\s+/g,' ')"))
    pg.click('.toast.rem [data-whf2="0"]');pg.wait_for_timeout(300)
    out('825_row_after',pg.evaluate(f"(r=>[r.r,r.wf])(DB.ph.find(p=>p.id=={p825}).rows.al.find(r=>r.sec=='Health'&&r.sz=='كبير'))"));out('stock_after_pull',pg.evaluate("WU().filter(x=>x.ty=='Acrylic letters 8 mm').map(x=>[x.size,x.qty])"))
  # letters max width from Wall Sticker
  pg.evaluate(f"goV({{v:'ph',p:{p825},op:{{al:true}},dr:{{}},q:V.q,fo:{{al:1}}}})");pg.wait_for_timeout(200)
  pg.select_option("details[data-id=al] select[data-k=sec]",'Health');pg.wait_for_timeout(200)
  for k,v in [('h','40'),('lh','20')]:pg.fill(f"details[data-id=al] input[data-k={k}]",v);pg.dispatch_event(f"details[data-id=al] input[data-k={k}]",'input')
  out('tw_prefill',pg.evaluate("[V.dr.al.tw,V.dr.al._twa,alTw(curP(),'Health')]"))
  pg.click("details[data-id=al] [data-add=al]");pg.wait_for_timeout(200)
  out('al_z',pg.evaluate(f"(p=>T.find(t=>t.id=='al').z(p.rows.al.slice(-1)[0],p.sh))(DB.ph.find(p=>p.id=={p825}))"))
  pg.evaluate(f"goV({{v:'sum',p:{p825},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(400)
  out('al_sentence',pg.evaluate("[...document.querySelectorAll('#rp .almxs')].map(e=>e.innerText)"))
  # Floor Header Old Turkish
  out('fh_825',pg.evaluate(f"(p=>p.rows.fh.slice(0,2).map(r=>T.find(t=>t.id=='fh').z(r,p.sh)))(DB.ph.find(p=>p.id=={p825}))"))
  pg.evaluate(f"goV({{v:'exec',p:{p825},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);out('exec_fh_tag',pg.evaluate("[...document.querySelectorAll('#rp .fhx')].slice(0,2).map(e=>e.textContent)"))
  out('mgmt_fh_mat',pg.evaluate(f"managementReportRows([DB.ph.find(p=>p.id=={p825})]).filter(x=>x.n=='Floor Header').map(x=>x.mat).slice(0,2)"))
  # old design
  pg.evaluate(f"goV({{v:'ph',p:{p825},op:{{__pi:true,__pho:true}},dr:{{}},q:V.q}})");pg.wait_for_timeout(200);pg.select_option('#cdz','قديم');pg.wait_for_timeout(300)
  out('dz',pg.evaluate("curP().dz"));out('old_photo_block',pg.evaluate("document.querySelector('[data-phcam=o]')!=null"))
  pg.evaluate("async()=>{const c=document.createElement('canvas');c.width=60;c.height=40;c.getContext('2d').fillRect(0,0,30,20);const b=await new Promise(ok=>c.toBlob(ok,'image/jpeg'));await phoAdd(curP(),'o',[new File([b],'o.jpg',{type:'image/jpeg'})])}");pg.wait_for_timeout(800)
  pg.evaluate(f"goV({{v:'sum',p:{p825},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(1200)
  out('old_banner',pg.evaluate("(e=>e?e.innerText:null)(document.querySelector('#rp .odz'))"));out('old_photos',pg.evaluate("[...document.querySelectorAll('#rp img[data-phod]')].map(i=>(i.getAttribute('src')||'').slice(0,15))"))
  out('old_no_builtin_img',pg.evaluate("document.querySelectorAll('#rp img.nimg').length"))
  out('sumtext_old',pg.evaluate("sumText(curP()).split('\\n')[1]"))
  # curve note + Acrylic boards status
  pg.evaluate(f"goV({{v:'sum',p:{p843},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);out('curve_sum',pg.evaluate("(e=>e?e.innerText:null)(document.querySelector('#rp .curve'))"))
  pg.evaluate(f"(p=>{{p.rows.ab.forEach(r=>{{r.r=0;r.x=0}});sv()}})(DB.ph.find(p=>p.id=={p843}))")
  pg.evaluate(f"goV({{v:'nq',nk:'r',ns:'ph',p:{p843},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
  out('ab_status',pg.evaluate("(h=>h?[...h.nextElementSibling.querySelectorAll('tr')].slice(0,3).map(r=>r.innerText.replace(/\\s+/g,' ')):null)([...document.querySelectorAll('#rp h3')].find(x=>x.textContent=='Acrylic boards'))"))
  out('ab_red',pg.evaluate("[...document.querySelectorAll('#rp td')].filter(t=>t.textContent=='تصنيع + تركيب').map(t=>t.style.background)[0]"))
  out('ab_text',[l for l in pg.evaluate("nqText()").split('\n') if 'تصنيع' in l][:2])
  # dates in management reports
  pg.evaluate("V.q.mo='2026-10';goV({v:'all',am:'mg',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);out('mg_dates',pg.evaluate("(h=>h?[...h.nextElementSibling.querySelectorAll('tr')].slice(0,3).map(r=>r.innerText.replace(/\\s+/g,' ')):null)([...document.querySelectorAll('#rp h3')].find(x=>x.textContent=='تواريخ الصيدليات'))"))
  out('month_rep_dates',pg.evaluate("monthRepEl('2026-10').innerText.includes('البدء')"))
  # roll request does not break the management report
  pg.evaluate(f"(p=>{{p.rolls={{Health:1}};sv()}})(DB.ph.find(p=>p.id=={p825}))");pg.evaluate(f"goV({{v:'sum',sm:'mgmt',p:{p825},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);out('mgmt_ok_with_roll',pg.evaluate("!!document.querySelector('#rp table')"))
  out('migrate_rr',pg.evaluate("(()=>{const p={rows:{},rr:{Health:2}};mig(p);return [JSON.stringify(p.rolls),JSON.stringify(p.rr)]})()"))
  # executed raises received
  pg.evaluate(f"goV({{v:'exec',p:{p843},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(200);pg.evaluate(f"(p=>{{const r=p.rows.fh[0];r.r=0;r.x=0;sv()}})(DB.ph.find(p=>p.id=={p843}))");pg.evaluate("render()")
  pg.click("[data-tf='x:fh:0']");pg.wait_for_timeout(200);out('x_raises_r',pg.evaluate(f"(r=>[r.r,r.x])(DB.ph.find(p=>p.id=={p843}).rows.fh[0])"))
  # backup version + restore message
  b=pg.evaluate("fullBackupWithFiles().then(o=>[o.ver,!!o.at])");out('backup_ver',b)
  # month close
  pg.evaluate("goV({v:'month',mo:'2026-10',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);pg.click('[data-mcls]');pg.wait_for_timeout(300)
  out('mclose',pg.evaluate("[...document.querySelectorAll('.mcl h3')].map(h=>h.textContent)"))
  pg.screenshot(path='qrt/mclose.png',full_page=True)
  out('menu_shade_ok',pg.evaluate("(()=>{goV({v:'month',mo:'2026-10',op:{},dr:{},q:V.q});document.querySelector('button.hmb').click();document.querySelector('.mshade').click();return V.v})()"))
  out('ver',pg.evaluate("VER"));out('ERRS',E);br.close()

# v1.5: QR scanner (fake camera), warehouse add with pharmacy cards, gondola acrylic option, print-missing-only, custody alert, maintenance search, photo share button, trial badge.
import glob,subprocess,os,json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new.html';D=open(W+'out12/966-data-v1.4.json',encoding='utf-8').read();R={}
def out(k,v):R[k]=v;print(k,'=>',v)
CH='/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
f=(glob.glob('/mnt/user-data/attachments/*/112e5fd3-image.jpg') or [None])[0]
with sync_playwright() as pw:
  if f:
    y=W+'qrt/t20cam.y4m';subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-i',f,'-vf','pad=iw+948:ih+534:474:267:white,crop=474:267:693:1046,scale=1280:720,format=yuv420p','-t','2','-r','10',y],check=True)
    br=pw.chromium.launch(executable_path=CH,args=['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream','--use-file-for-fake-video-capture='+y]);ctx=br.new_context(viewport={'width':390,'height':800},permissions=['camera']);pg=ctx.new_page();E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
    pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(1500)
    pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.evaluate("new MutationObserver((m,o)=>{const f=document.querySelector('.cfr');if(f){const a=f.getBoundingClientRect();window._fc=Math.abs(a.left-(innerWidth-a.right))<=2;o.disconnect()}}).observe(document.body,{childList:true,subtree:true})");pg.click('[data-cscan]');pg.wait_for_timeout(300)
    out('frame_centered',pg.evaluate("window._fc"))
    for i in range(40):
      pg.wait_for_timeout(250)
      if pg.evaluate("V.v=='ced'"):break
    out('qr_read',pg.evaluate("V.ce&&[V.ce.amt,V.ce.dt,!!V.ce._seq,(V.ce.imgs||[]).length]"))
    pg.evaluate("V.ce.desc=V.ce.desc||'اختبار';V.ce.comp=V.ce.comp||'اختبار'");pg.click('[data-csave]');pg.wait_for_timeout(1500)
    out('seq_reopen',pg.evaluate("[!!CSC,CSN,!!document.querySelector('.cscan .ccnt')]"))
    pg.click('[data-cscanx]');pg.wait_for_timeout(300);out('closed',pg.evaluate("[!!CSC,CSN,!!document.querySelector('.cscan')]"))
    out('saved_no_seq_flag',pg.evaluate("cMo().items.some(x=>'_seq' in x)"));out('ERRS_scan',E);br.close();os.remove(y)
  br=pw.chromium.launch(executable_path=CH);pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(1500)
  # warehouse add with pharmacy cards
  pg.evaluate("goV({v:'wh',op:{},dr:{},q:V.q})");pg.click('[data-wha]');pg.wait_for_timeout(200);pg.select_option('#whash','2');pg.wait_for_timeout(200)
  out('wha_types',pg.evaluate("[...document.querySelectorAll('main details[data-id]')].map(d=>d.dataset.id).join(',')"))
  pg.evaluate("V.op.eg=true;render()");pg.click('details[data-id=eg] [data-nmp]');pg.wait_for_timeout(300);out('picker_images',pg.evaluate("document.querySelectorAll('.nmov .nmc img').length>5"));pg.click('.nmov .nmc >> nth=2');pg.wait_for_timeout(200)
  out('egp_field_OT',pg.evaluate("!!document.querySelector('details[data-id=eg] select[data-k=egp]')"))
  pg.fill('details[data-id=eg] input[data-k=q]','3');pg.dispatch_event('details[data-id=eg] input[data-k=q]','input');pg.click('details[data-id=eg] [data-add=eg]');pg.wait_for_timeout(200)
  out('no_pull_toast_in_wha',pg.evaluate("!document.querySelector('.toast [data-whpull]')"))
  pg.click('[data-whaok]');pg.wait_for_timeout(300)
  out('wh_items',pg.evaluate("WU().map(x=>[x.ty,x.size,x.mat,x.sh,x.qty])"));out('wh_thumbs',pg.evaluate("document.querySelectorAll('.whimg').length"));out('pharmacies',pg.evaluate("DB.ph.length"))
  # acrylic option
  pg.evaluate("""(()=>{const p=JSON.parse(JSON.stringify(DB.ph[0]));p.id=999;p.no='T1';p.sh=2;p.rows={eg:[{nm:EG[0],sz:'قياسي',q:2},{nm:EG[1],sz:'قياسي',q:1,egp:'باك لايت + ستيكر بس'},{nm:EG[2],sz:'قياسي',q:3,egp:'أكريليك بس'}]};DB.ph.push(p);sv()})()""")
  pg.evaluate("goV({v:'ph',p:DB.ph[0].id,op:{eg:true},dr:{},q:V.q,fo:{eg:1}})");pg.wait_for_timeout(200);out('egp_field_nonOT',pg.evaluate("!!document.querySelector('select[data-k=egp]')"))
  pg.evaluate("goV({v:'sum',p:999,op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('sum_tables',pg.evaluate("[...document.querySelectorAll('#rp h3')].map(h=>h.textContent)"))
  out('sum_total',pg.evaluate("document.querySelector('#rp .tsum').innerText.replace(/\\s+/g,' ')"))
  out('pocket_rows',pg.evaluate("[...[...document.querySelectorAll('#rp h3')].find(h=>h.textContent=='Side Acrylic Pocket').nextElementSibling.querySelectorAll('tr')].slice(1).map(r=>r.cells[r.cells.length-2]&&r.cells[3]?r.cells[3].innerText:r.innerText.replace(/\\s+/g,' '))"))
  out('sizes',pg.evaluate("sizeRows(DB.ph.filter(x=>x.id==999)).map(x=>[x.n,x.sz,x.q])"))
  out('mgmt',pg.evaluate("managementReportRows(DB.ph.filter(x=>x.id==999)).map(x=>[x.n,x.sz,x.q,x.header,x.side])"))
  out('wh_parts',pg.evaluate("(()=>{const p=DB.ph.find(x=>x.id==999),t=T.find(x=>x.id=='eg');return p.rows.eg.map(r=>whParts(t,r,2).map(y=>y.ty+'×'+y.f))})()"))
  # print missing only
  pid=pg.evaluate("DB.ph.find(x=>x.no=='843').id")
  pg.evaluate("(()=>{const p=DB.ph.find(x=>x.no=='843'),t=T.find(x=>x.id=='fh'),r=p.rows.fh[0];whParts(t,r,p.sh).forEach(y=>whAdd({sh:y.sh,ty:y.ty,nm:y.nm,sec:y.sec,mat:y.mat,size:y.size},1,'in','manual','t'));sv()})()")
  pg.evaluate(f"goV({{v:'sum',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);q0=pg.evaluate(f"qn(DB.ph.find(x=>x.id=={pid}).rows.fh[0])")
  pg.click('#sxw');pg.wait_for_timeout(300);out('sx_used',pg.evaluate("whNet(curP()).used.map(u=>u.n)"));out('sx_banner',pg.evaluate("!!document.querySelector('#rp .sxn')"))
  out('sx_net_q',pg.evaluate("whNet(curP()).p.rows.fh[0].q")==q0-1)
  pg.click('[data-sxpull]');pg.wait_for_timeout(300);out('sx_after_pull',pg.evaluate(f"[DB.ph.find(x=>x.id=={pid}).rows.fh[0].wf,whNet(curP()).used.length,whNet(curP()).p.rows.fh[0].q]"))
  # custody alert
  out('alert_default_7562',pg.evaluate("!!cAlert()"));pg.evaluate("CU().cfg.al=8000;sv();goV({v:'home',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);out('alert_home',pg.evaluate("!!document.querySelector('.alr.cal')"))
  pg.evaluate("CU().cfg.al=0;sv();goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);out('alert_off',pg.evaluate("!document.querySelector('.alr.cal')"))
  # maintenance search
  pg.evaluate("goV({v:'mnt',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);n0=pg.evaluate("document.querySelectorAll('tr[data-med]').length");pg.type('#mqf','ZZZ');pg.wait_for_timeout(200)
  out('mnt_search',[n0,pg.evaluate("document.querySelectorAll('tr[data-med]').length"),pg.evaluate("document.activeElement.id")])
  # photo share button
  pg.evaluate("(()=>{const p=DB.ph[0];p.pho={b:[{k:'x1',sz:10}],a:[]};sv();goV({v:'ph',p:p.id,op:{__pho:true},dr:{},q:V.q})})()");pg.wait_for_timeout(200);out('pho_share_btn',pg.evaluate("!!document.querySelector('[data-phshare]')"))
  out('ver',pg.evaluate("VER"));out('ERRS',E);br.close()
  br=pw.chromium.launch(executable_path=CH);pg=br.new_page();pg.add_init_script("window.T966=1");pg.goto(APP);pg.wait_for_timeout(1200);out('trial_badge',pg.evaluate("!!document.querySelector('.t966')"));br.close()

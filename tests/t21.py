# v1.6: gondola acrylic pocket counter (843), warehouse per part, defects, custody Excel / PDF / appendix.
import base64,glob,io,zipfile,re
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new.html';D=open(W+'out13/966-data-v1.5.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(1500)
  pid=pg.evaluate("DB.ph.find(p=>p.no=='843').id")
  # edit first gondola: pq field
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{eg:true}},dr:{{}},q:V.q}})");pg.click("details[data-id=eg] [data-ed='eg:0']");pg.wait_for_timeout(200)
  out('pq_field_full',pg.evaluate("!!document.querySelector('details[data-id=eg] input[data-k=pq]')"))
  pg.select_option("details[data-id=eg] select[data-k=egp]",'باك لايت + ستيكر بس');pg.wait_for_timeout(200);out('pq_hidden_bs',pg.evaluate("!document.querySelector('details[data-id=eg] input[data-k=pq]')"))
  pg.select_option("details[data-id=eg] select[data-k=egp]",'كامل');pg.wait_for_timeout(200);pg.fill("details[data-id=eg] input[data-k=pq]",'1');pg.dispatch_event("details[data-id=eg] input[data-k=pq]",'input');pg.click("details[data-id=eg] [data-add=eg]");pg.wait_for_timeout(200)
  out('row0',pg.evaluate(f"(r=>[r.q,r.pq,r.egp])(DB.ph.find(p=>p.id=={pid}).rows.eg[0])"))
  out('z_row0',pg.evaluate(f"(p=>T.find(t=>t.id=='eg').z(p.rows.eg[0],p.sh))(DB.ph.find(p=>p.id=={pid}))"))
  # row 4 -> acrylic only
  pg.evaluate(f"(p=>{{p.rows.eg[4].egp='أكريليك بس';sv()}})(DB.ph.find(p=>p.id=={pid}))")
  pg.evaluate(f"goV({{v:'sum',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
  out('pocket_table',pg.evaluate("(h=>h?[...h.nextElementSibling.querySelectorAll('tr')].slice(1).map(r=>r.cells.length>3?r.cells[3].innerText:r.innerText.replace(/\\s+/g,' ')):null)([...document.querySelectorAll('#rp h3')].find(h=>h.textContent=='Side Acrylic Pocket'))"))
  # receipt checklist
  pg.evaluate(f"goV({{v:'sum',sm:'ck',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
  out('pocket_subrows',pg.evaluate("document.querySelectorAll('#rp tr.tkp').length"))
  pg.click("[data-tf='r:eg:0']");pg.wait_for_timeout(200)
  out('row0_after_main_check',pg.evaluate(f"(r=>[r.r,r.rp||0])(DB.ph.find(p=>p.id=={pid}).rows.eg[0])"))
  out('nq_r_eg',pg.evaluate(f"nqLines(DB.ph.find(p=>p.id=={pid}),'r').filter(x=>x.t.id=='eg').map(x=>[x.nm.slice(0,12),x.pt,x.sz,x.q,x.v,x.d])"))
  pg.click("[data-tf='rp:eg:0']");pg.wait_for_timeout(200);out('row0_pocket_check',pg.evaluate(f"DB.ph.find(p=>p.id=={pid}).rows.eg[0].rp"))
  out('prog',pg.evaluate(f"tkProg(DB.ph.find(p=>p.id=={pid}),'r')"))
  pg.click("[data-tkall='r']");pg.wait_for_timeout(200);out('nq_r_eg_after_all',pg.evaluate(f"nqLines(DB.ph.find(p=>p.id=={pid}),'r').filter(x=>x.t.id=='eg').length"))
  out('prog_all',pg.evaluate(f"tkProg(DB.ph.find(p=>p.id=={pid}),'r')"))
  out('nq_x_eg',pg.evaluate(f"nqLines(DB.ph.find(p=>p.id=={pid}),'x').filter(x=>x.t.id=='eg').map(x=>x.pt+' '+x.d)"))
  # migration of an old receipt
  out('migration',pg.evaluate("(()=>{const p={sh:2,rows:{eg:[{nm:EG[0],sz:'قياسي',q:3,r:2,x:1}]}};migPK(p);return [p.rows.eg[0].rp,p.rows.eg[0].xp,p.m16]})()"))
  # warehouse surplus: pocket on its own
  out('surplus',pg.evaluate(f"(()=>{{const p=DB.ph.find(p=>p.id=={pid}),r=p.rows.eg[1];r.r=2;r.x=1;r.rp=2;r.xp=0;return Object.values(whSurplus({{sh:p.sh,rows:{{eg:[r]}}}})).map(y=>y.ty+' '+y.q)}})()"))
  # pull per part: header/side in stock, no pocket
  pg.evaluate("WU().length=0;DB.wlog=[];sv()")
  pg.evaluate(f"(()=>{{const p=DB.ph.find(p=>p.id=={pid}),t=T.find(x=>x.id=='eg'),r={{nm:EG[3],sz:'قياسي',q:2}};whParts(t,r,p.sh).filter(y=>!y.pk).forEach(y=>whAdd({{sh:y.sh,ty:y.ty,nm:y.nm,sec:y.sec,mat:y.mat,size:y.size}},10,'in','manual','t'));sv()}})()")
  out('stock',pg.evaluate("WU().map(x=>x.ty+' '+x.qty)"))
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{eg:true}},dr:{{eg:{{nm:EG[3],sz:'قياسي',q:2,egp:'كامل'}}}},q:V.q,fo:{{eg:1}}}})");pg.wait_for_timeout(200);pg.click("details[data-id=eg] [data-add=eg]");pg.wait_for_timeout(400)
  out('offer',pg.evaluate("(t=>t?t.innerText.replace(/\\s+/g,' '):null)(document.querySelector('.toast.rem'))"))
  pg.click('.toast.rem [data-whpull]');pg.wait_for_timeout(300)
  out('after_pull',pg.evaluate(f"(r=>[r.q,r.r,r.wf,r.rp||0,r.wfp||0])(DB.ph.find(p=>p.id=={pid}).rows.eg.slice(-1)[0])"));out('stock_after',pg.evaluate("WU().map(x=>x.ty+' '+x.qty)"))
  out('nq_new_row',pg.evaluate(f"nqLines(DB.ph.find(p=>p.id=={pid}),'r').filter(x=>x.r===DB.ph.find(p=>p.id=={pid}).rows.eg.slice(-1)[0]).map(x=>x.pt+' '+x.d)"))
  # print-missing: header/side in stock, pocket not -> row becomes acrylic only
  pg.evaluate(f"(()=>{{const p=DB.ph.find(p=>p.id=={pid});p.rows.eg.push({{nm:EG[3],sz:'قياسي',q:2}});sv()}})()")
  out('net_row',pg.evaluate(f"(N=>[N.p.rows.eg.slice(-1)[0].egp,N.p.rows.eg.slice(-1)[0].q,N.used.map(u=>u.tx)])(whNet(DB.ph.find(p=>p.id=={pid})))"))
  # section not repeated + waiting rows kept
  pg.evaluate("whAdd({sh:2,ty:'End gandola - Header',nm:'Personal · Personal Care · نهتم بعنايتك',sec:'Personal',mat:'ستيكر',size:'50×66'},1,'in','manual','t');sv();goV({v:'wh',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200)
  out('no_dup_section',pg.evaluate("![...document.querySelectorAll('.whi small')].some(e=>/Personal · Personal ·/.test(e.textContent))"))
  pg.click('[data-wha]');pg.wait_for_timeout(200);pg.evaluate("V.op.fh=true;render()");pg.click('details[data-id=fh] [data-add=fh]');pg.wait_for_timeout(200);n=pg.evaluate("whaN()")
  pg.reload();pg.wait_for_timeout(1500);pg.evaluate("goV({v:'wh',op:{},dr:{},q:V.q})");pg.click('[data-wha]');pg.wait_for_timeout(200);out('wha_kept',[n,pg.evaluate("whaN()")])
  pg.click('[data-whax]');pg.wait_for_timeout(200);pg.click('[data-wha]');pg.wait_for_timeout(200);out('wha_cleared',pg.evaluate("whaN()"))
  # custody Excel / PDF / appendix
  F=sorted(glob.glob('/mnt/user-data/attachments/*/*.jp*g'))[:2]
  for i,f in enumerate(F):pg.evaluate("async([i,b64])=>{const b=await (await fetch('data:image/jpeg;base64,'+b64)).blob();const x=cMo().items[i];const k=await cImgPut(x.id,b);x.imgs=[k];sv()}",[i,base64.b64encode(open(f,'rb').read()).decode()])
  pg.evaluate("(()=>{const x=cMo().items.find(y=>(y.note||'').includes(NOPAPER));x.ref='فاتورة 12345';x.ph='843-695';sv()})()")
  b=base64.b64decode(pg.evaluate("async()=>{const bl=custXlsx(CU().cur);const r=new FileReader();return await new Promise(ok=>{r.onload=()=>ok(String(r.result).split(',')[1]);r.readAsDataURL(bl)})}"))
  z=zipfile.ZipFile(io.BytesIO(b));s1=z.read('xl/worksheets/sheet1.xml').decode();s2=z.read('xl/worksheets/sheet2.xml').decode();st=z.read('xl/styles.xml').decode()
  out('xl_title_yellow','FFFFFF00' in st);out('xl_purple','FF50164A' in st);out('xl_freeze','ySplit="6"' in s1);out('xl_rich','<r><rPr><b/><sz val="10"/><color rgb="FFC00000"/>' in s1 and 'فاتورة 12345' in s1)
  out('xl_cf_not_A',not re.search(r'conditionalFormatting sqref="A',s1));out('xl_footer','عهدة شهر' in s1 and '&amp;P' in s1);out('xl_by_pharmacy','المصروف حسب الصيدلية' in s2 and 'متقسمة عليهم بالتساوي' in s2);out('xl_car_col','<col min="9" max="9" width="17"' in s1)
  try:
    import openpyxl;wb=openpyxl.load_workbook(io.BytesIO(b));out('xl_opens',wb.sheetnames)
  except Exception as e:out('xl_opens','ERR '+str(e))
  out('pdf_el',pg.evaluate("(e=>[!!e.querySelector('.cpt.cy'),!!e.querySelector('.cpsub'),e.querySelectorAll('td.cnum').length,!!e.querySelector('td.cnpt small.cref')])(custPdfEl(CU().cur))"))
  out('appendix',pg.evaluate("cAppEl(CU().cur).then(o=>[o.n,[...o.el.querySelectorAll('.caxn')].map(e=>e.textContent),(o.el.querySelector('.cpsub:last-child')||{}).textContent.slice(0,40)])"))
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);out('app_list_num',pg.evaluate("document.querySelectorAll('.ctab td.cnum').length"));out('appx_buttons',pg.evaluate("document.querySelectorAll('[data-capx]').length"))
  out('ver',pg.evaluate("VER"));out('ERRS',E);br.close()

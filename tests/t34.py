# v3.0: Medicated «المطلوب», custody PDF invoices (QR from PDF), custody quotes, laptop Drive reminder
import base64
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new30.html';D=open(W+'bk1102/data.json',encoding='utf-8').read();F=W+'t34/'
PH=base64.b64encode(open('/mnt/user-data/attachments/7db5e8a6-d495-596a-8941-a726d2c69b08/e8e6622a-image.jpg','rb').read()).decode()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:160]),x.accept()))
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500)
  # ---------- Medicated
  out('md',pg.evaluate("""(()=>{const p=DB.ph.find(x=>x.no=='843');p.rows.md=[{nm:'AVENE',mdp:'Header بس',q:2},{nm:'Vichy',q:1},{nm:'QV',mdp:'Side بس',q:3}];const t=T.find(x=>x.id=='md');
   const sr=sizeRows([p]).filter(x=>/Medicated/.test(x.n)).map(x=>x.n+' '+x.q);const tb=document.createElement('div');tb.innerHTML=mdTable(p.rows.md,p.sh);
   const tot=[...tb.querySelectorAll('tr.tot td')].map(x=>x.innerText);const nq=nqLines(p,'x').filter(x=>x.t.id=='md').map(x=>x.nm+':'+x.pt+':'+x.d);
   const wp=p.rows.md.map(r=>whParts(t,r,p.sh).map(y=>y.ty.replace('Medicated - ','')).join('+'));const z=p.rows.md.map(r=>t.z(r,p.sh));
   const pr=tkProg(p,'r');p.rows.md.forEach(r=>{r.r=r.q});const pr2=tkProg(p,'r');return {sr,tot,nq,wp,z,lab:p.rows.md.map(r=>mdLab(t,r)),prog:[pr.n,pr2.d-pr.d]}})()"""))
  pg.evaluate("goV({v:'ph',p:DB.ph.find(x=>x.no=='843').id,op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('md_form',pg.evaluate("(()=>{const t=T.find(x=>x.id=='md');V.dr={};const d=draft(t,0);const h=form0(t,0);return [t.f.map(f=>f.k),d.mdp,/data-k=\"mdp\"/.test(h)]})()"))
  # ---------- PDF invoices (laptop: images inside the PDF)
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('cust_btn',pg.evaluate("[document.querySelector('[data-pick=cimgs]').innerText,document.querySelector('#cimgs').accept]"))
  res={}
  for f in ['inv_img.pdf','inv_flate.pdf','inv_photo.pdf','inv_pil.pdf','inv_1bitpng.pdf','inv_vec.pdf','inv_pil1.pdf']:
    pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(150)
    pg.set_input_files('#cimgs',F+f);pg.wait_for_timeout(2500)
    res[f]=pg.evaluate("V.ce?[V.ce.src,V.ce.amt,V.ce.comp,V.ce.dt,(V.ce.imgs||[]).map(k=>/:pdf$/.test(k)),Object.values(V.ce.fn||{}).map(x=>x.n)]:null")
  for k,v in res.items():out('pdf '+k,v)
  out('pdf_tile',pg.evaluate("(e=>e&&e.innerText.replace(/\\s+/g,' '))(document.querySelector('.cpdfb'))"))
  pg.evaluate("()=>{window._wo=[];window.open=(u)=>{window._wo.push(String(u).slice(0,5));return {}}}");pg.click('.cpdfb');pg.wait_for_timeout(400);out('pdf_open',pg.evaluate("window._wo"))
  # save the vector one (no QR) by hand, and a QR one
  pg.evaluate("V.ce.amt=99;V.ce.comp='شركة اختبار';V.ce.desc='مشتريات';V.ce.dt='2026-11-02'");pg.click('[data-csave]');pg.wait_for_timeout(400)
  # oversize
  big=F+'big.pdf';open(big,'wb').write(b'%PDF-1.4\n'+b'0'*(5*1048576+10))
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");n0=len(DL);pg.set_input_files('#cimgs',big);pg.wait_for_timeout(800);out('big',[DL[n0:],pg.evaluate("V.v")])
  # ---------- quotes
  pg.evaluate("(()=>{const C=CU();C.cur='2026-10';C.m['2026-10']=C.m['2026-10']||{open:10000,items:[]};})()")
  tot0=pg.evaluate("cTot(CU().m['2026-10'])");n10=pg.evaluate("CU().m['2026-10'].items.length")
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.click('[data-cman]');pg.wait_for_timeout(200)
  out('qt_sw',pg.evaluate("[...document.querySelectorAll('.cqsw button')].map(b=>b.innerText)"))
  pg.click('[data-cqt="1"]');pg.wait_for_timeout(150)
  pg.evaluate("Object.assign(V.ce,{dt:'2026-10-30',amt:500,comp:'مطبعة النور',desc:'طباعة ستيكر',kind:'مشتريات',ph:'843'})");pg.click('[data-csave]');pg.wait_for_timeout(400)
  out('qt_saved',[pg.evaluate("(x=>x&&[x.qt,x.amt])(CU().m['2026-10'].items.find(x=>x.comp=='مطبعة النور'))"),pg.evaluate("cTot(CU().m['2026-10'])")==tot0,pg.evaluate("document.querySelector('.cqal')&&document.querySelector('.cqal').innerText.split('\\n').slice(0,3)"),pg.evaluate("[...document.querySelectorAll('.cqk b')].map(b=>b.innerText)"),pg.evaluate("(r=>r&&r.innerText.replace(/\\s+/g,' '))(document.querySelector('tr.cqt'))")])
  out('qt_report',pg.evaluate("""(async()=>{const k='2026-10',b=custXlsx(k),t=new TextDecoder().decode(await b.arrayBuffer());const el=custPdfEl(k);return [t.includes('مطبعة النور'),el.innerText.includes('مطبعة النور'),el.querySelectorAll('tr').length]})()"""))
  n0=len(DL);pg.evaluate("()=>{window.out=async()=>{window._out=1};window.dl=()=>{window._dl=1}}");pg.click('[data-cxl=save]');pg.wait_for_timeout(500);out('qt_warn_export',DL[n0:])
  # the invoice arrives in the next month
  pg.evaluate("(()=>{const C=CU();C.m['2026-11']=C.m['2026-11']||{open:9000,items:[]}})()")
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.click('.cqal [data-cqo]');pg.wait_for_timeout(300)
  out('qt_edit',pg.evaluate("[V.v,!!document.querySelector('[data-cqarr]'),document.querySelector('[data-csave]').innerText]"))
  pg.click('[data-cqarr]');pg.wait_for_timeout(300)
  out('arr_banner',[pg.evaluate("CU().cur"),pg.evaluate("(e=>e&&e.innerText.replace(/\\s+/g,' '))(document.querySelector('.cqf'))")])
  pg.click('[data-cqman]');pg.wait_for_timeout(300)
  out('arr_draft',pg.evaluate("[V.ce.comp,V.ce.amt,V.ce.desc,!!V.ce._q,(document.querySelector('.ced .ph')||{}).innerText]"))
  pg.evaluate("Object.assign(V.ce,{dt:'2026-11-02',amt:510,ref:'INV-77'})");pg.click('[data-csave]');pg.wait_for_timeout(400)
  out('arr_saved',pg.evaluate("""(()=>{const C=CU(),inv=C.m['2026-11'].items.find(x=>x.ref=='INV-77'),q=C.m['2026-10'].items.find(x=>x.comp=='مطبعة النور');return [inv&&[inv.dt,inv.amt,inv.note,!!inv.qt],q&&[q.qt,q.qi],cQts().length,cTot(C.m['2026-10'])==%s]})()"""%tot0))
  pg.evaluate("CU().cur='2026-10';goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200)
  out('closed_row',pg.evaluate("(r=>r&&r.innerText.replace(/\\s+/g,' '))(document.querySelector('tr.cqd'))"))
  # same month: quote removed, attachments go to the invoice
  pg.evaluate("""(()=>{const C=CU();C.cur='2026-11';C.m['2026-11'].items.push({id:4242,dt:'2026-11-03',tm:'',kind:'مشتريات',desc:'أكريليك',comp:'ورشة سالم',amt:300,car:'',ph:'',ref:'',note:'',imgs:['cimg:4242:a:pdf'],fn:{'cimg:4242:a:pdf':{n:'q.pdf',sz:10}},qt:1,src:'manual'});sv()})()""")
  pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.click('[data-cqo="2026-11|4242"]');pg.wait_for_timeout(200);pg.click('[data-cqarr]');pg.wait_for_timeout(200);pg.click('[data-cqman]');pg.wait_for_timeout(200)
  pg.evaluate("Object.assign(V.ce,{dt:'2026-11-04'})");pg.click('[data-csave]');pg.wait_for_timeout(400)
  out('same_month',pg.evaluate("(()=>{const M=CU().m['2026-11'];const q=M.items.find(x=>x.id==4242),inv=M.items.find(x=>x.comp=='ورشة سالم');return [!!q,inv&&[inv.amt,inv.note,inv.imgs,!!inv.qt]]})()"))
  # notifications: a quote 5 days old
  pg.evaluate("""(()=>{const d=new Date(Date.now()-5*864e5),iso=d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');CU().m['2026-11'].items.push({id:5151,dt:iso,tm:'',kind:'شحن',desc:'شحن',comp:'السيف',amt:120,car:'',ph:'',ref:'',note:'',imgs:[],qt:1,src:'manual'});sv()})()""")
  out('ntf',[pg.evaluate("ntfNow().filter(x=>x.k=='qt').map(x=>x.t)"),pg.evaluate("ntfPlan().filter(n=>/عرض سعر/.test(n.title)).length"),pg.evaluate("(n=>n&&n.body)(ntfPlan().find(n=>/عرض سعر/.test(n.title)))")])
  pg.evaluate("goV({v:'ntf',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);pg.fill('#ntfqd','7');pg.dispatch_event('#ntfqd','change');out('ntf_qd',[pg.evaluate("NTF().qd"),pg.evaluate("ntfNow().filter(x=>x.k=='qt').length")])
  n0=len(DL);pg.evaluate("CU().cur='2026-11';goV({v:'cust',op:{},dr:{},q:V.q,cnew:true})");pg.evaluate("V.cnew=true;render()");pg.wait_for_timeout(200)
  pg.on('dialog',lambda x:None)
  # ---------- photos appendix with PDFs: the PDFs go as separate files
  pg.evaluate("()=>{window._sf=null;window.shareFiles=async(F,m)=>{window._sf=[m,F.map(f=>[f.name,f.type])]}}")
  out('appendix',pg.evaluate("""(async()=>{const C=CU();C.cur=Object.keys(C.m).find(k=>C.m[k].items.some(x=>x.comp=='شركة اختبار'));const o=await cAppEl(C.cur);await cAppxF(C.cur,o,'share');return [C.cur,o.n,o.pdfs.length,window._sf&&window._sf[1].slice(-2)]})()"""))
  out('ERRS',E)
  # ---------- phone: PDF page render (mocked PdfTools)
  nt=br.new_page(viewport={'width':400,'height':860});E2=[];nt.on('pageerror',lambda e:E2.append(str(e)));nt.on('dialog',lambda x:x.accept())
  nt.add_init_script("""(()=>{window._pt=[];window.Capacitor={isNativePlatform:()=>true,Plugins:{Filesystem:{writeFile:async o=>({uri:'file:///cache/'+o.path}),deleteFile:async()=>{},mkdir:async()=>{}},
   PdfTools:{render:async o=>{window._pt.push(['render',o.path,o.pages]);return {count:1,pages:[window._PH]}},open:async o=>{window._pt.push(['open',o.path,o.mime])}}}};})()""")
  nt.add_init_script("window._PH='%s'"%PH)
  nt.goto(APP);nt.wait_for_timeout(300);nt.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);nt.reload();nt.wait_for_timeout(2500)
  nt.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");nt.wait_for_timeout(200);nt.set_input_files('#cimgs',F+'inv_vec.pdf');nt.wait_for_timeout(4000)
  out('native_pdf',[nt.evaluate("V.ce&&[V.ce.src,V.ce.amt,V.ce.comp,V.ce.dt]"),nt.evaluate("window._pt.map(x=>x[0]+':'+x[2])")])
  nt.click('.cpdfb');nt.wait_for_timeout(500);out('native_open',nt.evaluate("window._pt.filter(x=>x[0]=='open')"))
  out('ERRS2',E2)
  # ---------- laptop reminder
  lp=br.new_page(viewport={'width':1200,'height':900});E3=[];lp.on('pageerror',lambda e:E3.append(str(e)))
  lp.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>false})")
  lp.goto(APP);lp.wait_for_timeout(300);lp.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);lp.reload();lp.wait_for_timeout(2800)
  out('lap_rem',lp.evaluate("(t=>t&&t.innerText.split('\\n').slice(0,4))(document.querySelector('.toast.gdrem'))"))
  lp.click('.toast.gdrem [data-gdremx]');lp.reload();lp.wait_for_timeout(2800);out('lap_rem_tomorrow',lp.evaluate("!!document.querySelector('.toast.gdrem')"))
  lp.evaluate("gdU(o=>o.rmd='')");lp.reload();lp.wait_for_timeout(2800);lp.click('.toast.gdrem [data-gdremgo]');lp.wait_for_timeout(300);out('lap_rem_go',lp.evaluate("[V.v,document.querySelector('header h1').innerText]"))
  out('ERRS3',E3)
  br.close()

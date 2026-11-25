# 2.9 on the 25-11 backup: every new item, widths 360/400, no page errors
import json,base64
from playwright.sync_api import sync_playwright
W='/home/claude/work/';D=json.load(open(W+'bk1125/data.json',encoding='utf-8'))
def run(pg,js,a=None):return pg.evaluate(js,a) if a is not None else pg.evaluate(js)
def wid(pg):return run(pg,"[document.documentElement.scrollWidth,document.documentElement.clientWidth]")
out=lambda k,v:print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch()
  def boot(data,w=360):
    c=br.new_context(viewport={'width':w,'height':800});pg=c.new_page();E=[];M=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:(M.append(x.message[:140]),x.accept()))
    pg.goto('file://'+W+'new29.html');pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(data,ensure_ascii=False));pg.reload();pg.wait_for_timeout(3000);return pg,E,M
  pg,E,M=boot(D)
  out('ver / title',[run(pg,"VER"),run(pg,"document.title")])
  # W) Wall Header pieces
  out('WH stock 17x80 / 17x50',run(pg,"WU().filter(x=>x.ty=='Wall Header'&&/×(80|50)$/.test(x.size)).map(x=>x.nm+' '+x.size+' '+x.qty+' '+x.unit).slice(0,4)"))
  out('WH units',run(pg,"[...new Set(WU().filter(x=>x.ty=='Wall Header').map(x=>x.unit))]"))
  out('WH 17x50 Medical device (was 1.5 m)',run(pg,"WU().find(x=>x.ty=='Wall Header'&&x.nm=='Medical device'&&x.size=='17×50').qty"))
  out('wlog WH 17x80 import',run(pg,"DB.wlog.filter(e=>e.ty=='Wall Header'&&e.size=='17×80').map(e=>e.qty).slice(0,3)"))
  out('migration twice is a no-op',run(pg,"(()=>{const a=JSON.stringify(DB.wh);whFix29();return a==JSON.stringify(DB.wh)})()"))
  # 5 + B) transfer sheet of 510
  run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='510'&&p.mo=='2026-11');V.p=p.id;whOffer(p,false)})()");pg.wait_for_timeout(500)
  out('wht lines',run(pg,"[...document.querySelectorAll('.w29 tr')].slice(1).map(r=>r.cells[1].innerText.replace(/\\n/,' · ')+' | '+r.cells[5].innerText)"))
  out('width wht',wid(pg))
  ks=run(pg,"[...document.querySelectorAll('[data-w29c]')].map(x=>x.dataset.w29c)")
  run(pg,"k=>{const x=document.querySelector(`[data-w29c=\"${CSS.escape(k)}\"]`);x.checked=false;x.dispatchEvent(new Event('change',{bubbles:true}))}",ks[1]);pg.wait_for_timeout(300)
  out('after untick',[run(pg,"document.querySelectorAll('tr.w29off').length"),run(pg,"document.querySelector('[data-whgo]').innerText")])
  run(pg,"k=>{const s=document.querySelector(`[data-w29m=\"${CSS.escape(k)}\"]`);s.value='ستيكر + أكريليك';s.dispatchEvent(new Event('change',{bubbles:true}))}",ks[0]);pg.wait_for_timeout(200)
  run(pg,"v24Click({whgo:1},document.body)||whClick({whgo:1})");pg.wait_for_timeout(400)
  out('after transfer: pending',run(pg,"(p=>whPlan(p).map(x=>x.ty+' '+(x.nm||x.sec)+' '+x.dl))(DB.ph.find(p=>p.no=='510'&&p.mo=='2026-11'))"))
  out('material line in stock',run(pg,"(DB.wlog[0]||{}).note+' | '+WU().filter(x=>x.mat=='ستيكر + أكريليك').map(x=>x.ty+' '+x.nm+' '+x.qty).join(', ')"))
  out('whM',run(pg,"JSON.stringify(DB.ph.find(p=>p.no=='510'&&p.mo=='2026-11').whM)"))
  # A) ✓ all skips swapped
  out('tkall 674',run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='674'&&p.mo=='2026-11');const r=p.rows.saf.find(r=>r.cx);r.x=0;V.p=p.id;goV({v:'ph',p:p.id,op:{},dr:{},q:V.q});const bt=document.createElement('button');bt.dataset.tkall='x';document.querySelector('#app').appendChild(bt);bt.click();const o=p.rows.saf.filter(r=>!r.cx).every(r=>+r.x==qn(r));return [r.x,o]})()"))
  # 6) health room on 295
  run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='295');goV({v:'ph',p:p.id,op:{ws:true},dr:{},q:V.q})})()");pg.wait_for_timeout(500)
  out('hr button',run(pg,"!!document.querySelector('[data-hr29]')"));out('width ph 295',wid(pg))
  run(pg,"hrOpen('h')");pg.wait_for_timeout(200);out('width hr sheet',wid(pg));out('sheet fields',run(pg,"document.querySelectorAll('.hr29 fieldset').length"))
  run(pg,"""(()=>{const s=(i,v)=>document.getElementById(i).value=v;s('hr29dh',210);s('hr29dw',90);s('hr29rh',240);s('hr29rw','120 + 80');s('hr29lh',240);s('hr29lw','100')})()""")
  run(pg,"v24Click({hr29go:'h'},document.body)");pg.wait_for_timeout(400)
  out('hr rows',run(pg,"(p=>['so','ws','al'].map(id=>id+':'+(p.rows[id]||[]).filter(r=>r.hr).map(r=>T.find(t=>t.id==id).z(r,p.sh).slice(0,90)).join(' || ')))(DB.ph.find(p=>p.no=='295'))"))
  out('hr block',run(pg,"document.querySelector('.hr29b')&&document.querySelector('.hr29b').innerText.split('\\n').slice(0,9)"));out('width after hr',wid(pg))
  out('mgmt material 4mm',run(pg,"(p=>managementReportRows([p]).filter(x=>/4 مم/.test(x.mat)).map(x=>x.n+' '+x.sz+' '+x.mat+' '+x.q))(DB.ph.find(p=>p.no=='295'))"))
  out('whParts 4mm',run(pg,"(p=>p.rows.al.filter(r=>r.mm==4).map(r=>whParts(T.find(t=>t.id=='al'),r,p.sh)[0].mat))(DB.ph.find(p=>p.no=='295'))"))
  out('form auto 4 boards',run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='832');const n0=(p.rows.al||[]).length;V.p=p.id;goV({v:'ph',p:p.id,op:{al:true},dr:{al:{sec:HRI,h:'',lh:28,w:200,q:1}},q:V.q,fo:{al:1}});const b=document.querySelector('[data-add=\"al\"]');if(b)b.click();return (p.rows.al||[]).slice(n0).map(r=>(r.pc?'boards ':'line ')+r.q+(r.mm?' mm'+r.mm:'')+' '+(r.nt||''))})()"))
  pg.wait_for_timeout(300)
  run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='295');goV({v:'ph',p:p.id,op:{ws:true},dr:{},q:V.q})})()");pg.wait_for_timeout(300)
  run(pg,"v24Click({hr29del:document.querySelector('[data-hr29del]').dataset.hr29del},document.body)");out('hr deleted',run(pg,"(p=>['so','ws','al'].map(id=>(p.rows[id]||[]).filter(r=>r.hr).length))(DB.ph.find(p=>p.no=='295'))"))
  # 7) Wall Sticker default kind
  out('ws default kd',run(pg,"(()=>{const t=T.find(t=>t.id=='ws');return t.f.find(f=>f.k=='kd').o({})[0]})()"))
  # 8 + S1) file names
  out('fnEn',run(pg,"['تقرير الإدارة - صيدلية 695 - 11-2026.pdf','تقرير الإدارة - صيدلية 695 - 11-2026.xlsx','صور قبل وبعد - صيدلية 510 - 11-2026.pdf','عهدة الوسطى (الرياض) - شهر 11-2026 - 2026-11-25.pdf','pharmacy-695-summary.pdf','نواقص الطباعة - صيدلية 674.xlsx'].map(fnEn)"))
  out('fname mgmt',run(pg,"(()=>{const p=DB.ph.find(p=>p.no=='695'&&p.mo=='2026-11');V.p=p.id;V.v='sum';V.sm='mgmt';return fname()})()"))
  # 8) Excel like the PDF
  b64=run(pg,"""async()=>{const p=DB.ph.find(p=>p.no=='695'&&p.mo=='2026-11');const el=document.createElement('div');el.innerHTML=mgmtHtml(p);const x=rpXlsx(el);const a=new Uint8Array(await x.arrayBuffer());let s='';for(let i=0;i<a.length;i+=8192)s+=String.fromCharCode.apply(null,a.subarray(i,i+8192));return btoa(s)}""")
  open(W+'m29/mg695-29.xlsx','wb').write(base64.b64decode(b64))
  # 3) merge keeps photos under another id
  run(pg,"""async()=>{for(const p of DB.ph)for(const sl of ['b','a','o'])for(const x of phoList(p,sl)){const c=document.createElement('canvas');c.width=c.height=8;const b=await new Promise(r=>c.toBlob(r));await idbSet(phoKey(p.id,sl,x.k),b)}}""")
  run(pg,"""async()=>{const h=HID[0];h.pho={b:[{k:'hz1',sz:10}]};const c=document.createElement('canvas');c.width=c.height=8;await idbSet(phoKey(h.id,'b','hz1'),await new Promise(r=>c.toBlob(r)))}""")
  full=run(pg,"async()=>JSON.stringify(await fullBackupWithFiles())")
  fj=json.loads(full);out('C) hold photo in full',any(k.endswith(':b:hz1') for k in fj['_photos']));out('photos in full',len(fj['_photos']))
  L=json.loads(json.dumps(D))
  for p in L['ph']:
    if p.get('pho'):p['id']=p['id']+7;p['modAt']='2026-11-01T00:00:00.000Z'
  lp,E2,_=boot(L)
  out('merge under other ids',lp.evaluate("async q=>{const msg=await gdApply(JSON.parse(q),'merge','t');let ok=0,miss=0;for(const p of DB.ph)for(const sl of ['b','a'])for(const x of phoList(p,sl)){(await idbGet(phoKey(p.id,sl,x.k)))?ok++:miss++}return [msg,ok,miss]}",full))
  lp2,E3,_=boot(L)
  out('exPhotos only',lp2.evaluate("async q=>{const n=await exPhotos(JSON.parse(q));let ok=0;for(const p of DB.ph)for(const sl of ['b','a'])for(const x of phoList(p,sl))if(await idbGet(phoKey(p.id,sl,x.k)))ok++;return [n,ok,DB.ph.length]}",full))
  out('drive list order',lp2.evaluate("gdListHtml([{name:'966-day-2026-11-25.json',id:'1',mt:'2026-11-25',size:600000},{name:'966-full-2026-11-25.json',id:'2',mt:'2026-11-25',size:43e6}]).replace(/<[^>]+>/g,'|').replace(/\\|+/g,'|').slice(0,160)"))
  out('sync chip while Drive works',lp2.evaluate("(()=>{gdU(o=>{o.on=1;o.need=0;o.fails=0});return syncChip()})()"))
  out('errors',[E,E2,E3])
  br.close()

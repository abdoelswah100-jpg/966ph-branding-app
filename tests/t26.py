# v2.2 on the owner's 02-11 backup
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new22.html';D=open(W+'bk1102/data.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)));pg.on('dialog',lambda x:x.accept())
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2000)
  out('fix',pg.evaluate("[DB.ph.every(p=>p.m22),JSON.stringify(DB.ph.find(p=>p.no=='1136').rows.ab),DB.ph.filter(p=>p.sh==2).map(p=>p.no+':'+[...new Set((p.rows.fh||[]).map(r=>r.sz+'/'+(r.rsh||'')))].join(',')),[...new Set(DB.ph.flatMap(p=>(p.rows.saw||[]).map(r=>r.sz)))],WU().filter(x=>x.ty=='Floor Header'||x.ty=='Side Acrylic Shelves Wall').map(x=>[x.ty,x.sh,x.size,x.qty])]"))
  out('fh_z_836',pg.evaluate("(p=>[...new Set(p.rows.fh.map(r=>T.find(t=>t.id=='fh').z(r,p.sh).split(' · ')[2]))])(DB.ph.find(p=>p.no=='836'))"))
  # home lists
  pg.evaluate("goV({v:'home',op:{},dr:{},q:{t:'',st:'',mo:''}})");pg.wait_for_timeout(400)
  out('home',pg.evaluate("[...document.querySelectorAll('#hl details.mg')].map(d=>[d.querySelector('summary').innerText.replace(/\\s+/g,' '),d.querySelectorAll(':scope > .mgb > .pcard').length,(d.querySelector('.mntg summary')||{}).innerText,d.querySelectorAll('.mntg .pcard').length,(d.querySelector('.mntg')||{}).open])"))
  pg.fill('#q','1136') if pg.query_selector('#q') else None
  # apart
  out('month_n',pg.evaluate("(()=>{V.mo='2026-11';return mStats(DB.ph.filter(p=>p.mo=='2026-11'&&isBr(p))).n})()"))
  pg.evaluate("goV({v:'month',mo:'2026-11',op:{},dr:{},q:{t:'',st:'',mo:''}})");pg.wait_for_timeout(300)
  out('month_board',pg.evaluate("[document.querySelector('.m-all b').innerText,document.querySelector('[data-id=__rt] summary')?document.querySelector('[data-id=__rt] summary').innerText:null]"))
  out('rev_pf',pg.evaluate("[staleN(),(V.q={t:'',st:'',mo:'2026-11'},PF().length)]"))
  # new maintenance pharmacy: empty
  pg.evaluate("goV({v:'add',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  pg.fill('#pno','9991');pg.select_option('#pmod','صيانة');pg.wait_for_timeout(100)
  btn=pg.evaluate("(b=>b?b.outerHTML.slice(0,80):null)(document.querySelector('main button.pr.big, main #padd, main [data-padd]'))");out('add_btn',btn)
  pg.evaluate("document.querySelector('#addp').click()");pg.wait_for_timeout(400)
  out('new_mnt',pg.evaluate("(p=>p?[p.mod,JSON.stringify(p.rows)]:null)(DB.ph.find(p=>p.no=='9991'))"))
  # 657 maintenance -> completed -> log
  pid=pg.evaluate("DB.ph.find(p=>p.no=='657').id");n0=pg.evaluate("MU().items.length")
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{fr:true,__pi:true}},dr:{{}},q:V.q,fo:{{fr:1}}}})");pg.wait_for_timeout(300)
  out('mw_field',pg.evaluate("[!!document.querySelector('details[data-id=fr] select[data-k=mw]'),[...((document.querySelector('details[data-id=fr] select[data-k=mw]')||{}).options||[])].map(o=>o.value)[0]]"))
  pg.select_option('#cst','مكتملة');pg.wait_for_timeout(500)
  out('log_add',pg.evaluate(f"[MU().items.length-{n0},MU().items.filter(x=>String(x.src||'').startsWith('ph:{pid}:')).map(x=>[x.dt,x.ph,x.work,x.ad,x.det,x.q])]"))
  out('toast',pg.evaluate("[...document.querySelectorAll('.toast')].map(t=>t.innerText).slice(-2)"))
  pg.evaluate(f"(p=>{{p.rows.fr[0].mw='تركيب';p.rows.fr[0].x=2;sv()}})(DB.ph.find(p=>p.id=={pid}))");pg.wait_for_timeout(200)
  out('log_upd',pg.evaluate(f"[MU().items.length-{n0},MU().items.filter(x=>String(x.src||'').startsWith('ph:{pid}:')).map(x=>[x.work,x.q])]"))
  pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{__pi:true}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);pg.select_option('#cst','جاري');pg.wait_for_timeout(300)
  out('log_back',pg.evaluate(f"MU().items.length-{n0}"))
  # custody
  out('car',pg.evaluate("[cDraft({kind:'سيارة'}).car,cDraft({kind:'وقود'}).car,cDraft({kind:'وجبات'}).car]"))
  # Old Turkish options
  out('ot',pg.evaluate("(()=>{const fh=T.find(t=>t.id=='fh'),wh=T.find(t=>t.id=='wh');return [opts(fh.f.find(f=>f.k=='sz'),{sec:'Health'},2),opts(fh.f.find(f=>f.k=='sz'),{sec:'Health'},1),opts(wh.f.find(f=>f.k=='len'),{sec:'Baby',wt:'WALL NORMAL'},2),opts(wh.f.find(f=>f.k=='len'),{sec:'Baby',wt:'WALL NORMAL'},1),SZ('saw')]})()"))
  # totals per material
  p809=pg.evaluate("DB.ph.find(p=>p.no=='809').id")
  pg.evaluate(f"goV({{v:'sum',sm:'mgmt',p:{p809},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(400)
  out('tot',pg.evaluate("[...document.querySelectorAll('#rt tr.tot')].map(r=>r.innerText.replace(/\\s+/g,' '))"))
  out('overflow',pg.evaluate("document.documentElement.scrollWidth"))
  out('ERRS',E)
  br.close()

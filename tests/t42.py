# v3.6: old stock (material, actual size, separate old size, gandola side by section + side, old-design only, photos),
# «رملي» roll, item-level merge of custody / maintenance, warehouse warning
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new36.html';D=open(W+'bk1106/data.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  DL=[];pg.on('dialog',lambda x:(DL.append(x.message[:200]),x.accept()))
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500)
  pg.evaluate("WU().length=0;goV({v:'who',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200)
  def add(k,sh,sec,sz,real,sd,q,mt='أكريليك + ستيكر',solo=''):
    pg.select_option('select[data-wo=k]',k);pg.wait_for_timeout(100)
    if pg.locator('select[data-wo=sh]').count():pg.select_option('select[data-wo=sh]',str(sh));pg.wait_for_timeout(100)
    if pg.locator('select[data-wo=sec]').count():pg.select_option('select[data-wo=sec]',sec);pg.wait_for_timeout(100)
    if pg.locator('select[data-wo=mt]').count():pg.select_option('select[data-wo=mt]',mt);pg.wait_for_timeout(100)
    pg.select_option('select[data-wo=sz]',sz);pg.wait_for_timeout(100)
    if solo:pg.fill('[data-wo=solo]',solo);pg.dispatch_event('[data-wo=solo]','change')
    if real:pg.fill('[data-wo=real]',real);pg.dispatch_event('[data-wo=real]','change')
    if pg.locator('select[data-wo=sd]').count():pg.select_option('select[data-wo=sd]',sd);pg.wait_for_timeout(100)
    pg.fill('[data-wo=q]',str(q));pg.dispatch_event('[data-wo=q]','change');pg.wait_for_timeout(100);pg.click('[data-whosave]');pg.wait_for_timeout(250)
  add('saf',0,'Health','صغير 30×120','118.5×30','يمين',1)
  out('img_in_form',pg.evaluate("!!document.querySelector('.woim img')"))
  add('saf',0,'Beauty','صغير 30×120','120.5×30','يمين',1)
  add('saf',0,'Baby','__solo','','يمين',1,solo='35*125')
  add('egs',0,'Baby','100×25','','يمين',1)
  add('egs',0,'Baby','100×25','','يسار',1)
  out('items',pg.evaluate("WU().map(x=>[x.ty,x.sh,x.sec,x.nm,x.size,x.real||'',!!x.solo,x.mat,x.qty])"))
  out('cards',pg.evaluate("[...document.querySelectorAll('.whc')].map(c=>[!!c.querySelector('img.whimg'),c.querySelector('.whi small:nth-of-type(2)').textContent.replace(/\\s+/g,' ').slice(0,60),!!c.querySelector('[data-whpic]')])"))
  # offers: old pharmacy vs new pharmacy
  r=pg.evaluate("""(()=>{const base=DB.ph.find(p=>String(p.no)=='510');const mk=(dz,no)=>{const q=JSON.parse(JSON.stringify(base));Object.assign(q,{id:Date.now()+(+no),no,sh:0,dz,name:'T'+no,rows:{},rcv:[]});q.rows.saf=[{sec:'Health',sz:'صغير 30×120',sd:'يمين',q:1},{sec:'Baby',sz:'صغير 30×120',sd:'يمين',q:1}];q.rows.eg=[{nm:'Baby (Small) · Body care · نهتم بطفلك',q:1},{nm:'Baby (Big) · Body care · نهتم بطفلك',q:1}];DB.ph.push(q);return q};
     const a=mk('قديم','9101'),b=mk('جديد','9102');sv();const f=(p,t)=>(p.rows[t]||[]).map(r=>whOldOpts(p,T.find(x=>x.id==t),r).map(o=>o.txt));return [f(a,'saf'),f(a,'eg'),f(b,'saf'),f(b,'eg')]})()""")
  out('old_ph_saf',r[0]);out('old_ph_eg',r[1]);out('new_ph',[r[2],r[3]])
  # roll kind
  out('roll_kinds',pg.evaluate("RLK"))
  # ---- merge custody / maintenance by item
  m=pg.evaluate("""(()=>{const C=CU(),k=C.cur;C.m[k]={open:1000,items:[{id:1,dt:'2026-11-01',desc:'A',amt:10},{id:2,dt:'2026-11-02',desc:'B',amt:20}]};C.m[k].items=C.m[k].items.filter(x=>x.id!=2);C.m[k].xd={2:'2026-11-10T10:00:00Z'};
     MU().items=[{id:11,dt:'2026-11-01',ph:'1',q:1},{id:12,dt:'2026-11-01',ph:'2',q:1}];sv();secStamp();
     const inc=JSON.parse(JSON.stringify(DB));inc.cust.m[k]={open:1000,items:[{id:2,dt:'2026-11-02',desc:'B',amt:20},{id:3,dt:'2026-11-03',desc:'C (phone)',amt:30},{id:1,dt:'2026-11-01',desc:'A edited',amt:15}],dep:[{id:7,amt:500,dt:'2026-11-05'}]};
     inc.mnt.items=[{id:12,dt:'2026-11-01',ph:'2',q:5},{id:13,dt:'2026-11-02',ph:'3',q:1}];inc.mnt.xd={11:'2026-11-10T11:00:00Z'};
     inc.cfg.sat=Object.assign({},DB.cfg.sat,{cust:'2099-01-01T00:00:00Z',mnt:'2099-01-01T00:00:00Z'});const uid=STO||U().id;if(inc.uw&&inc.uw[uid])['cust','mnt','wh'].forEach(k=>inc.uw[uid][k]=inc[k]);
     const res=gdMerge(inc,'t');const M=CU().m[k];return [res.sec,M.items.map(x=>[x.id,x.desc,x.amt]),(M.dep||[]).map(d=>d.amt),cRem(M),MU().items.map(x=>[x.id,x.q])]})()""")
  out('merge',m)
  # incoming older: local kept for same ids, new ids still added
  m2=pg.evaluate("""(()=>{const C=CU(),k=C.cur;const inc=JSON.parse(JSON.stringify(DB));inc.cust.m[k].items.push({id:4,dt:'2026-11-04',desc:'D old device',amt:40});inc.cust.m[k].items.find(x=>x.id==1).desc='A older';inc.cfg.sat=Object.assign({},DB.cfg.sat,{cust:'2000-01-01T00:00:00Z'});const uid=STO||U().id;if(inc.uw&&inc.uw[uid])['cust','mnt','wh'].forEach(k=>inc.uw[uid][k]=inc[k]);gdMerge(inc,'t');return CU().m[k].items.map(x=>[x.id,x.desc])})()""")
  out('merge_older',m2)
  # warehouse changed on both -> flag
  w=pg.evaluate("""(()=>{gdU(o=>o.pt='2026-11-10T09:00:00Z');DB.cfg.sat.wh='2026-11-10T12:00:00Z';const inc=JSON.parse(JSON.stringify(DB));inc.wh=[{id:99,ty:'X',qty:1}];inc.cfg.sat=Object.assign({},DB.cfg.sat,{wh:'2026-11-10T13:00:00Z'});const uid=STO||U().id;if(inc.uw&&inc.uw[uid])['cust','mnt','wh'].forEach(k=>inc.uw[uid][k]=inc[k]);const r=gdMerge(inc,'t');return [r.whc,WU().length]})()""")
  out('wh_warn',w)
  # backups screen
  pg.evaluate("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);out('bk_sum',pg.evaluate("document.querySelector('.gdbk>summary').innerText.replace(/\\s+/g,' ')"))
  out('ERRS',E);br.close()

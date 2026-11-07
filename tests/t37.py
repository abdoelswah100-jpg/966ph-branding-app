# v3.3: custom names, warehouse by size across shelf types, preparation list, import number+month / newer warning, laptop data, warehouse copy
import json
from playwright.sync_api import sync_playwright
W='/home/claude/work/';APP='file://'+W+'new33.html';D=open(W+'bk1106/data.json',encoding='utf-8').read()
def out(k,v):print(k,'=>',v)
with sync_playwright() as pw:
  br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');pg=br.new_page(viewport={'width':400,'height':860});E=[];pg.on('pageerror',lambda e:E.append(str(e)))
  ANS=[];DL=[]
  def dlg(x):
    DL.append(x.message[:160])
    if x.type=='prompt':x.accept(ANS.pop(0) if ANS else '')
    else:x.accept()
  pg.on('dialog',dlg)
  pg.goto(APP);pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",D);pg.reload();pg.wait_for_timeout(2500)
  pid=pg.evaluate("DB.ph.find(p=>String(p.no)=='510').id")
  # ---- custom End cap name from the select
  pg.evaluate(f"()=>{{goV({{v:'ph',p:{pid},op:{{ec:1,eg:1}},dr:{{}},q:V.q}});V.fo={{ec:1,eg:1}};render()}}");pg.wait_for_timeout(300)
  pg.select_option('select[data-t=ec][data-k=sec]','Beauty');pg.wait_for_timeout(150)
  out('ec_opt',pg.evaluate("[...document.querySelectorAll('select[data-t=ec][data-k=nm] option')].slice(-2).map(o=>o.textContent)"))
  ANS.append('Sun care · واقي الشمس');pg.select_option('select[data-t=ec][data-k=nm]','__xn');pg.wait_for_timeout(400)
  out('ec_new',[pg.evaluate("[V.dr.ec.nm,EC.Beauty.slice(-1)[0],JSON.stringify(DB.cfg.xn)]"),DL[-1][:60]])
  pg.click('[data-add=ec]');pg.wait_for_timeout(300)
  out('ec_row',pg.evaluate(f"DB.ph.find(p=>p.id=={pid}).rows.ec.slice(-1)[0]"))
  # duplicate name -> selects existing
  ANS.append('sun care · واقي الشمس');pg.select_option('select[data-t=ec][data-k=nm]','__xn');pg.wait_for_timeout(300);out('ec_dup',[pg.evaluate("EC.Beauty.filter(x=>/Sun care/i.test(x)).length"),pg.evaluate("V.dr.ec.nm")])
  # End gandola through the picture picker
  pg.click('[data-nmp=eg]');pg.wait_for_timeout(300);ANS.append('Sun care · واقي الشمس');pg.click('.nmov [data-xnadd=eg]');pg.wait_for_timeout(400)
  out('eg_new',pg.evaluate("[V.dr.eg.nm,EG.slice(-1)[0],!!document.querySelector('.nmov')]"))
  # reload keeps them
  pg.reload();pg.wait_for_timeout(2500);out('after_reload',pg.evaluate("[EC.Beauty.includes('Sun care · واقي الشمس'),EG.some(x=>/Sun care/.test(x))]"))
  # manage: rename and delete; rows keep their name
  pg.evaluate("goV({v:'types',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300)
  out('types_tbl',pg.evaluate("[...document.querySelectorAll('[data-xned]')].map(b=>b.closest('tr').innerText.replace(/\\s+/g,' '))"))
  ANS.append('Sun protection · واقي الشمس');pg.click('[data-xned^="ec:Beauty"]');pg.wait_for_timeout(300)
  pg.click('[data-xndel^="eg"]');pg.wait_for_timeout(300)
  out('types_after',[pg.evaluate("JSON.stringify(DB.cfg.xn)"),pg.evaluate("[EC.Beauty.slice(-1)[0],EG.some(x=>/Sun care/.test(x))]"),pg.evaluate(f"DB.ph.find(p=>p.id=={pid}).rows.ec.slice(-1)[0].nm")])
  # ---- warehouse across shelf types
  r=pg.evaluate("""(()=>{WU().length=0;const t=T.find(x=>x.id=='ec');const p=DB.ph.find(x=>String(x.no)=='510');const P=whParts(t,{sec:'Health',sz:'صغير 64×111',nm:'Vitamins · فيتامينات',q:1},1)[0];
    whAdd(Object.assign({},P,{sh:1}),10,'in','manual','test');
    const mk=(sh,no)=>{const q=JSON.parse(JSON.stringify(p));Object.assign(q,{id:Date.now()+sh,no,sh,mo:MN(),name:'T'+no,rows:{},rcv:[]});q.rows.ec=[{sec:'Health',sz:SZ('ec.'+sh)[0],nm:'Vitamins · فيتامينات',q:3}];DB.ph.push(q);return q};
    const a=mk(0,'9001'),b=mk(2,'9002'),c=mk(3,'9003');sv();return [a.id,b.id,c.id,SH.slice()]})()""")
  out('SH',r[3])
  for k,id in zip(['regular','old','ukr'],r[:3]):
    out('opts_'+k,pg.evaluate(f"(p=>whFromOpts(p,T.find(t=>t.id=='ec'),p.rows.ec[0]).map(o=>o.txt))(DB.ph.find(p=>p.id=={id}))"))
  pg.evaluate(f"goV({{v:'ph',p:{r[0]},op:{{ec:1}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300);pg.click('[data-whfrom="ec:0"]');pg.wait_for_timeout(300)
  out('pull_toast',pg.evaluate("(t=>t&&t.innerText.replace(/\\s+/g,' '))(document.querySelector('.toast'))"))
  pg.click('.toast [data-whf2="0"]');pg.wait_for_timeout(400)
  out('pulled',[pg.evaluate("WU().map(x=>[x.sh,x.qty])"),pg.evaluate(f"DB.ph.find(p=>p.id=={r[0]}).rows.ec[0].r"),pg.evaluate("DB.wlog[0].note")])
  # same shelf type stock first
  pg.evaluate("""(()=>{const t=T.find(x=>x.id=='ec');const P=whParts(t,{sec:'Health',sz:'صغير 64×111',nm:'Vitamins · فيتامينات',q:1},0)[0];whAdd(Object.assign({},P,{sh:0}),2,'in','manual','test');sv()})()""")
  out('pool_order',pg.evaluate(f"(p=>{{const t=T.find(x=>x.id=='ec'),r=p.rows.ec[0];const L=whRowPlan(t,r,p.sh);whTake(p,t,r,L,'t');return WU().map(x=>[x.sh,x.qty])}})(DB.ph.find(p=>p.id=={r[1]}))"))
  # ---- preparation list
  pg.evaluate("goV({v:'prep',op:{},dr:{},q:V.q,pp:"+str(pid)+"})");pg.wait_for_timeout(300)
  out('prep_head',pg.evaluate("[document.querySelector('header h1').innerText,document.querySelector('.pgw small').innerText,document.querySelectorAll('.ppr').length,[...document.querySelectorAll('.rtchips button')].map(b=>b.innerText).slice(0,8)]"))
  pg.click('.rtchips [data-ppf="End cap"]');pg.wait_for_timeout(200)
  rows0=pg.evaluate("[...document.querySelectorAll('.ppr')].map(x=>x.innerText.replace(/\\s+/g,' '))");out('prep_ec',rows0)
  pg.click('.rtchips [data-ppf="*"]');pg.wait_for_timeout(200);first=pg.evaluate("[...document.querySelectorAll('.ppr')].find(x=>+x.querySelector('.pps b small').textContent.slice(1)>1).querySelector('[data-pp$=\":1\"]').dataset.pp");rows0=pg.evaluate("[...document.querySelectorAll('.ppr')]");pg.click(f'[data-pp="{first}"]');pg.wait_for_timeout(300)
  idp=first.rsplit(':',1)[0]
  out('prep_plus',[pg.evaluate(f"(a=>{{const p=DB.ph.find(x=>x.id==a[0]);const r=p.rows[a[1]][a[2]];return [r.r,qn(r),(p.rcv||[]).slice(-1)[0].src]}})({json.dumps(idp.split(':')[:1]+[idp.split(':')[1],int(idp.split(':')[2])]).replace('\"'+idp.split(':')[0]+'\"',idp.split(':')[0])})"),pg.evaluate("document.querySelector('.pgw small').innerText")])
  pg.click(f'[data-pp="{idp}:all"]');pg.wait_for_timeout(300);out('prep_all_hidden',[len(rows0),pg.evaluate("document.querySelectorAll('.ppr').length")])
  pg.click('#pph');pg.wait_for_timeout(200);out('prep_show_all',pg.evaluate("document.querySelectorAll('.ppr').length"))
  out('menu_prep',pg.evaluate("MENU.some(m=>m[0]=='prep')"))
  # ---- import: number + month
  pg.evaluate("""(()=>{const a=DB.ph.find(p=>String(p.no)=='674');const old=JSON.parse(JSON.stringify(a));old.id=12345;old.mo='2026-10';old.rows.ec=[];DB.ph.push(old);sv()})()""")
  f1=W+'t37_patch.json';open(f1,'w',encoding='utf-8').write(json.dumps({'mode':'mergePatch','ph':[{'no':'674','rows':{'ec':[{'sec':'Health','sz':'صغير 64×111','nm':'OTC · أدوية لا وصفية','q':1}]}}]},ensure_ascii=False))
  pg.evaluate("goV({v:'bk',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);n=len(DL);pg.set_input_files('#imp',f1);pg.wait_for_timeout(800)
  out('patch_month',[DL[n:],pg.evaluate("DB.ph.filter(p=>String(p.no)=='674').map(p=>[p.mo,(p.rows.ec||[]).length])")])
  # replace with an older copy -> warning
  q=pg.evaluate("(()=>{const p=JSON.parse(JSON.stringify(DB.ph.find(x=>String(x.no)=='695')));p.modAt='2026-11-01T00:00:00Z';return JSON.stringify({ph:[p]})})()")
  f2=W+'t37_rep.json';open(f2,'w',encoding='utf-8').write(q);n=len(DL);pg.set_input_files('#imp',f2);pg.wait_for_timeout(800);out('replace_warn',DL[n:])
  # ---- warehouse add: copy a pharmacy
  pg.evaluate("goV({v:'wha',op:{},dr:{},q:V.q})");pg.wait_for_timeout(300);ANS.append('510');pg.click('[data-whacp]');pg.wait_for_timeout(400)
  out('wha_copy',[pg.evaluate("Object.entries(WHP().rows).map(([k,v])=>k+':'+v.length).join(' ')"),pg.evaluate("WHP().sh"),pg.evaluate("(document.querySelector('[data-whaok]')||{}).innerText")])
  out('ERRS',E)
  # ---- laptop: empty data
  lp=br.new_page();E2=[];lp.on('pageerror',lambda e:E2.append(str(e)))
  lp.goto(APP);lp.wait_for_timeout(300);lp.evaluate("()=>localStorage.clear()");lp.reload();lp.wait_for_timeout(2800)
  out('empty',[lp.evaluate("(t=>t&&t.innerText.split('\\n')[0])(document.querySelector('.toast.stem'))"),lp.evaluate("ST_P")])
  lp.evaluate("ST_P=false;goV({v:'gd',op:{},dr:{},q:V.q})");lp.wait_for_timeout(200);out('st_warn',lp.evaluate("(e=>e&&e.innerText.slice(0,70))(document.querySelector('main .ywarn'))"))
  out('ERRS2',E2);br.close()

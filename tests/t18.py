import json, os, re
from playwright.sync_api import sync_playwright
W='/home/claude/work/';OUT=W+'s18/';os.makedirs(OUT,exist_ok=True)
DATA=open(W+'out6/966-data-v1.2.json',encoding='utf-8').read();errs,res,dl=[],{},[]
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');ctx=br.new_context(viewport={'width':400,'height':860},device_scale_factor=2,accept_downloads=True);pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append('C '+m.text) if m.type=='error' else None);pg.on('dialog',lambda x:(dl.append(x.message[:120]),x.accept()))
    pg.goto('file://'+W+'new.html');pg.wait_for_timeout(300);pg.evaluate("d=>localStorage.setItem('ads',d)",DATA);pg.reload();pg.wait_for_timeout(1500)
    res['tabs']=pg.evaluate("[...document.querySelectorAll('.bnav button')].map(b=>b.dataset.tab)")
    pg.click('button.hmb');pg.wait_for_timeout(100);res['menu_calc']=pg.evaluate("!!document.querySelector('[data-mgo=calc]')");pg.click('[data-mgo=calc]');pg.wait_for_timeout(200);res['calc_view']=pg.evaluate('V.v')
    pid=pg.evaluate("DB.ph.find(p=>p.no=='1533').id");P=f"DB.ph.find(p=>p.id=={pid})"
    # received everything, executed one less on Floor Header / End cap / Wall Header
    pg.evaluate(f"(()=>{{const p={P};['fh','ec','wh','eg','md','ws'].forEach(k=>(p.rows[k]||[]).forEach((r,i)=>{{r.r=qn(r);r.x=Math.max(0,qn(r)-(i%2?1:0))}}));sv()}})()")
    pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
    pg.click(f'button[data-whdone="{pid}"]');pg.wait_for_timeout(400)
    res['wht']=pg.evaluate("[V.v,whPlan(curP()).length,whPlan(curP()).filter(x=>x.ty=='Wall Sticker').length,whPlan(curP()).slice(0,3).map(x=>[x.ty,x.nm,x.size,x.mat,SH[x.sh],x.dl])]")
    res['status']=pg.evaluate(f"{P}.st");pg.screenshot(path=OUT+'01_transfer.png',full_page=True)
    pg.click('button[data-whgo]');pg.wait_for_timeout(300)
    res['stock']=pg.evaluate("[WU().length,wq(WU().filter(x=>x.unit!='متر').reduce((a,x)=>a+x.qty,0)),wq(WU().filter(x=>x.unit=='متر').reduce((a,x)=>a+x.qty,0)),DB.wlog.length]")
    pg.click(f'button[data-whdone="{pid}"]');pg.wait_for_timeout(300);res['again']=[pg.evaluate('V.v'),dl[-1] if dl else '']
    # executed more later -> negative difference only
    pg.evaluate(f"(()=>{{const p={P};const r=p.rows.fh.find((r,i)=>i%2);r.x=qn(r);sv()}})()")
    res['delta']=pg.evaluate(f"whPlan({P}).map(x=>[x.ty,x.nm,x.dl])")
    pg.click(f'button[data-whdone="{pid}"]');pg.wait_for_timeout(300);pg.click('button[data-whgo]');pg.wait_for_timeout(300)
    res['stock2']=pg.evaluate("wq(WU().filter(x=>x.unit!='متر').reduce((a,x)=>a+x.qty,0))")
    # warehouse screen
    pg.click('.bnav button[data-tab=wh]');pg.wait_for_timeout(300);pg.screenshot(path=OUT+'02_wh.png',full_page=True)
    res['cards']=pg.evaluate("document.querySelectorAll('.whc').length")
    pg.select_option('select[data-whf=ty]','Floor Header');pg.wait_for_timeout(200);res['flt_fh']=pg.evaluate("document.querySelectorAll('.whc').length")
    pg.select_option('select[data-whf=ty]','');pg.wait_for_timeout(200)
    fid=pg.evaluate("WU().find(x=>x.ty=='Floor Header').id")
    q0=pg.evaluate(f"WU().find(x=>x.id=={fid}).qty");pg.click(f'button[data-whst="{fid}:1"]');pg.wait_for_timeout(150);res['plus']=pg.evaluate(f"WU().find(x=>x.id=={fid}).qty-{q0}")
    pg.evaluate(f"WU().find(x=>x.id=={fid}).min=5;sv();render()");pg.wait_for_timeout(200);res['low_badge']=pg.evaluate("[whLow(),(document.querySelector('.bnav [data-tab=wh] .nb')||{}).textContent]")
    # manual add
    pg.click('button[data-wha]');pg.wait_for_timeout(200);pg.click('button[data-whadd]');pg.wait_for_timeout(200);pg.select_option('select[data-wef=ty]','Door sticker');pg.wait_for_timeout(150);pg.fill('input[data-wef=nm]','اسحب / ادفع');pg.fill('input[data-wef=size]','10×30');pg.fill('input[data-wef=qty]','12');pg.click('button[data-whsave]');pg.wait_for_timeout(300)
    res['manual']=pg.evaluate("WU().filter(x=>x.ty=='Door sticker').map(x=>[x.nm,x.qty,x.unit])")
    # inventory
    pg.click('button[data-whinv]');pg.wait_for_timeout(300)
    ids=pg.evaluate("WU().slice(0,3).map(x=>x.id)");qs=pg.evaluate("WU().slice(0,3).map(x=>x.qty)")
    for i,(k,q) in enumerate(zip(ids,qs)):
        pg.fill(f'input[data-invc="{k}"]',str(q+[0,-1,2][i]));pg.dispatch_event(f'input[data-invc="{k}"]','change');pg.wait_for_timeout(150)
    res['inv_prog']=pg.inner_text('.pgw small');pg.screenshot(path=OUT+'03_inv.png',full_page=True)
    pg.click('button[data-invok]');pg.wait_for_timeout(300);res['inv_done']=pg.evaluate("[DB.invs[0].rows.length,DB.invs[0].rows.map(x=>x.df),DB.wlog.filter(x=>x.typ=='inv').length]")
    # pull into a pharmacy: add a Floor Header identical to a stock item in another pharmacy with the same shelf type
    st=pg.evaluate("(()=>{const x=WU().find(x=>x.ty=='Floor Header'&&x.qty>0);return {sh:x.sh,nm:x.nm,sec:x.sec}})()")
    other=pg.evaluate(f"(()=>{{const p=DB.ph.find(p=>p.sh=={st['sh']}&&p.no!='1533');return p?p.id:null}})()")
    res['pull_target']=[st,other]
    if other is None:
        other=pg.evaluate(f"(()=>{{const p=DB.ph.find(p=>p.no!='1533');p.sh={st['sh']};sv();return p.id}})()")
    q1=pg.evaluate("WU().find(x=>x.ty=='Floor Header'&&x.qty>0).qty")
    pg.evaluate(f"goV({{v:'ph',p:{other},op:{{fh:true}},dr:{{fh:{{sec:'{st['sec']}',nm:{json.dumps(st['nm'])},q:1}}}},q:V.q,fo:{{fh:1}}}})");pg.wait_for_timeout(300)
    pg.click('button[data-add="fh"]');pg.wait_for_timeout(500)
    res['pull_toast']=pg.evaluate("(document.querySelector('.toast.rem')||{}).textContent||''")[:120]
    if pg.locator('button[data-whpull]').count(): pg.click('button[data-whpull]');pg.wait_for_timeout(300)
    res['pull']=pg.evaluate(f"(()=>{{const p=DB.ph.find(p=>p.id=={other}),r=p.rows.fh[p.rows.fh.length-1];return [r.wf,r.r,WU().find(x=>x.ty=='Floor Header'&&x.nm==r.nm&&x.sh==p.sh).qty]}})()")+[q1]
    # maintenance asks first
    dl.clear();fz=pg.evaluate("(()=>{const x=WU().find(x=>x.ty=='Floor Header'&&x.qty>0);return [x.size,x.qty]})()")
    ph2=pg.evaluate(f"DB.ph.find(p=>p.id=={other}).no")
    pg.evaluate(f"goV({{v:'mnt',op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(200);pg.click('button[data-madd]');pg.wait_for_timeout(200)
    pg.fill('input[data-mf=ph]',str(ph2));pg.dispatch_event('input[data-mf=ph]','change');pg.select_option('select[data-mf=ad]','Floor Header');pg.wait_for_timeout(150);pg.fill('input[data-mf=sz]',fz[0]);pg.dispatch_event('input[data-mf=sz]','change');pg.fill('input[data-mf=det]','تجربة');pg.click('button[data-msave]');pg.wait_for_timeout(300)
    res['mnt_ask']=[x for x in dl if 'المخزن' in x][:1];res['mnt_after']=pg.evaluate("WU().find(x=>x.ty=='Floor Header'&&x.qty>=0&&true).qty")
    # exports + log
    pg.evaluate("goV({v:'wlog',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);res['log_rows']=pg.evaluate("document.querySelectorAll('.ctab tr').length");pg.screenshot(path=OUT+'04_log.png')
    pg.evaluate("goV({v:'wh',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200)
    with pg.expect_download() as d: pg.evaluate("window.navigator.canShare=undefined");pg.click('button[data-whxl]')
    d.value.save_as(OUT+'wh.xlsx');res['xls']=d.value.suggested_filename
    pg.reload();pg.wait_for_timeout(1500);res['persist']=pg.evaluate("[WU().length,DB.wlog.length,(DB.invs||[]).length]")
    pg.evaluate("DB.cfg.lang='en';svq();goV({v:'wh',op:{},dr:{},q:V.q})");pg.wait_for_timeout(400);t=pg.evaluate("document.querySelector('main').innerText");res['en_left']=sorted(set(re.findall(r'[ء-ي][ء-ي ]{2,}',t)))[:20]
    br.close()
for k,v in res.items():print(k,'=>',v)
print('dialogs',dl[:6]);print('ERRS',errs)

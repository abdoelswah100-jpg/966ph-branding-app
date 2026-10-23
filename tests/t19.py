import json, os, re
from playwright.sync_api import sync_playwright
W='/home/claude/work/';OUT=W+'s19/';os.makedirs(OUT,exist_ok=True)
D=json.load(open(W+'out6/966-data-v1.2.json',encoding='utf-8'));S=json.load(open(W+'nov/966-sync - صيدليات شهر 11-2026.json',encoding='utf-8'))
D['ph']+=S['ph'];DATA=json.dumps(D,ensure_ascii=False);errs,res,dl=[],{},[]
def login(pg,uid,pin=None):
    pg.evaluate("uLogout()");pg.wait_for_timeout(150);pg.click(f'[data-ulsel="{uid}"]');pg.wait_for_timeout(150)
    if pin is not None:
        pg.fill('#ulpin',pin);pg.click(f'[data-ulgo="{uid}"]')
    else: pg.click(f'[data-ulgo="{uid}"]')
    pg.wait_for_timeout(300)
with sync_playwright() as pw:
    br=pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome');ctx=br.new_context(viewport={'width':400,'height':860},device_scale_factor=2,accept_downloads=True);pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e)));pg.on('console',lambda m:errs.append('C '+m.text) if m.type=='error' else None);pg.on('dialog',lambda x:(dl.append(x.message[:160]),x.accept()))
    pg.goto('file://'+W+'new.html');pg.wait_for_timeout(300);pg.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",DATA);pg.reload();pg.wait_for_timeout(1500)
    res['start']=pg.evaluate("[U().nm,!!document.getElementById('ulog'),DB.users.length,DB.ph.length,DB.ph.filter(p=>p.mo=='2026-11').map(p=>p.no+':'+uName(p.uid)).join(' ')]")
    # admin sets PINs
    pg.click('button.hmb');pg.wait_for_timeout(100);pg.click('[data-mgo=usr]');pg.wait_for_timeout(300);pg.screenshot(path=OUT+'01_users.png',full_page=True)
    for uid,pin in (('u7','2468'),('u4','1111')):
        pg.click(f'[data-uedit="{uid}"]');pg.wait_for_timeout(200);pg.fill('#upin1',pin);pg.fill('#upin2',pin);pg.click('[data-usave]');pg.wait_for_timeout(400)
    res['pins']=pg.evaluate("DB.users.filter(u=>u.pin).map(u=>u.id)")
    # u7 logs in
    pg.evaluate("uLogout()");pg.wait_for_timeout(200);pg.screenshot(path=OUT+'02_login.png')
    pg.click('[data-ulsel="u7"]');pg.wait_for_timeout(150);pg.fill('#ulpin','0000');pg.click('[data-ulgo="u7"]');pg.wait_for_timeout(300);res['wrong']=pg.inner_text('#lkm')
    pg.fill('#ulpin','2468');pg.click('[data-ulgo="u7"]');pg.wait_for_timeout(400)
    res['u7']=pg.evaluate("[U().nm,!!document.getElementById('ulog'),DB.ph.map(p=>p.no).join(','),HID.length]")
    res['saved_all']=pg.evaluate("JSON.parse(localStorage.getItem('ads')).ph.length")
    pid=pg.evaluate("DB.ph[0].id");pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{fh:true}},dr:{{}},q:V.q,fo:{{fh:1}}}})");pg.wait_for_timeout(300);res['u7_ro_banner']=pg.evaluate("!!document.querySelector('.ywarn')&&document.querySelector('.ywarn').textContent.includes('للعرض')")
    # custody for u7
    pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);pg.click('button[data-cman]');pg.wait_for_timeout(200);pg.fill('input[data-cf=comp]','مطعم سكاكا');pg.dispatch_event('input[data-cf=comp]','change');pg.fill('input[data-cf=amt]','40');pg.click('button[data-csave]');pg.wait_for_timeout(300)
    res['u7_cust']=pg.evaluate("[cMo().items.length,CU().cfg.sup]")
    pg.evaluate("DB.cfg.sz['fh.l']='99×99';svq()");res['u7_ov']=pg.evaluate("JSON.parse(localStorage.getItem('ads')).users.find(u=>u.id=='u7').ov")
    # my work file
    pg.evaluate("window.showSaveFilePicker=undefined;navigator.canShare=undefined")
    with pg.expect_download() as d: pg.click('button.hmb');pg.click('[data-mgo=usr]');pg.wait_for_timeout(200);pg.click('button[data-uexp]')
    d.value.save_as(OUT+'u7.966sup.json');res['file']=json.load(open(OUT+'u7.966sup.json',encoding='utf-8'))['ph'].__len__()
    # manager without edit rights
    login(pg,'u1')
    res['u1']=pg.evaluate("[U().nm,DB.ph.length]")
    pid=pg.evaluate("DB.ph.find(p=>p.no=='1533').id");pg.evaluate(f"goV({{v:'ph',p:{pid},op:{{}},dr:{{}},q:V.q}})");pg.wait_for_timeout(300)
    res['u1_banner']=pg.evaluate("(document.querySelector('.ywarn')||{}).textContent||''")[:60]
    n0=pg.evaluate(f"cntRows(DB.ph.find(p=>p.id=={pid}))");pg.evaluate("document.querySelector('button[data-fo=fh]').click()");pg.wait_for_timeout(200);res['u1_blocked']=pg.evaluate("[!!(V.fo&&V.fo.fh),[...document.querySelectorAll('.toast')].map(t=>t.textContent).join('|')]")
    # view other user's custody (view only)
    pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})");pg.wait_for_timeout(200);pg.select_option('#ustsel','u7');pg.wait_for_timeout(300)
    res['u1_sees_u7_cust']=pg.evaluate("[STO,cMo().items.length,uStoreRO()]")
    pg.click('button[data-cman]');pg.wait_for_timeout(200);res['u1_cust_blocked']=pg.evaluate("V.v")
    # Mohamed Thabet: edits East only
    login(pg,'u3')
    e=pg.evaluate("DB.ph.find(p=>p.no=='62').id");c=pg.evaluate("DB.ph.find(p=>p.no=='1533').id")
    res['u3']=pg.evaluate(f"[DB.ph.length,uEditP(DB.ph.find(p=>p.id=={e})),uEditP(DB.ph.find(p=>p.id=={c}))]")
    # admin: performance, apply settings for everyone, sees u7 custody editable
    login(pg,'u4','1111')
    res['u4']=pg.evaluate("[U().nm,DB.ph.length,(DB.users.find(u=>u.id=='u7').ov.sz||{})['fh.l']]")
    pg.click('button.hmb');pg.click('[data-mgo=usr]');pg.wait_for_timeout(300);pg.screenshot(path=OUT+'03_admin.png',full_page=True)
    res['perf']=pg.evaluate("[...document.querySelectorAll('.ctab tr')].slice(1).map(r=>r.innerText.replace(/\\s+/g,' '))")
    pg.click('[data-uova="u7"]');pg.wait_for_timeout(300);res['applied']=pg.evaluate("[SZ('fh.l'),Object.keys(DB.users.find(u=>u.id=='u7').ov||{}).length]")
    # import u7 file on a fresh device (admin)
    ctx2=br.new_context(accept_downloads=True);p2=ctx2.new_page();p2.on('dialog',lambda x:(dl.append(x.message[:200]),x.accept()));p2.on('pageerror',lambda e:errs.append('P2 '+str(e)))
    p2.goto('file://'+W+'new.html');p2.wait_for_timeout(300);p2.evaluate("d=>{localStorage.clear();localStorage.setItem('ads',d)}",json.dumps(D,ensure_ascii=False));p2.reload();p2.wait_for_timeout(1500)
    p2.evaluate("goV({v:'usr',op:{},dr:{},q:V.q})");p2.wait_for_timeout(200);p2.set_input_files('#usupin',OUT+'u7.966sup.json');p2.wait_for_timeout(800)
    res['import']=dl[-1][:200];res['after_import']=p2.evaluate("[DB.ph.length,(DB.uw.u7&&DB.uw.u7.cust&&Object.values(DB.uw.u7.cust.m)[0].items.length)||0]")
    # reload keeps session and asks PIN
    pg.reload();pg.wait_for_timeout(1500);res['reload']=pg.evaluate("[U().nm,!!document.getElementById('ulog')]")
    pg.evaluate("DB.cfg.lang='en';svq()");pg.evaluate("uShowLogin('')");pg.wait_for_timeout(300);t=pg.evaluate("document.getElementById('ulog').innerText");res['en_login']=sorted(set(re.findall(r'[ء-ي][ء-ي ]{2,}',t)))[:10]
    br.close()
for k,v in res.items():print(k,'=>',v)
print('dialogs',dl[:5]);print('ERRS',errs)

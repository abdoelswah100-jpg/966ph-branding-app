import json, os
from playwright.sync_api import sync_playwright
W = '/home/claude/work/'
DATA = open(W + 'out4/966-data-v1.4.json', encoding='utf-8').read()
MOCK = r"""
window.__calls=[];window.__files={};
window.Capacitor={isNativePlatform:()=>true,Plugins:{
 Filesystem:{mkdir:async o=>{__calls.push(['mkdir',o.path])},writeFile:async o=>{__calls.push(['write',o.path,o.directory,(o.data||'').length]);__files[o.path]=1;return{uri:'file:///storage/emulated/0/Documents/'+o.path}},
  readdir:async o=>({files:Object.keys(__files).filter(k=>k.startsWith(o.path+'/')).map(k=>({name:k.split('/').pop()}))}),deleteFile:async o=>{__calls.push(['del',o.path]);delete __files[o.path]}},
 Share:{share:async o=>{__calls.push(['share',o.files&&o.files[0]])}},
 App:{addListener:(e,f)=>{window.__back=f;__calls.push(['listen',e])},exitApp:()=>{__calls.push(['exit'])}}}};
"""
errs, res = [], {}
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = br.new_context(viewport={'width': 400, 'height': 860}, accept_downloads=True)
    ctx.add_init_script(MOCK)
    pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('dialog', lambda d: d.accept())
    pg.goto('file://' + W + 'full28.html'); pg.wait_for_timeout(300)
    pg.evaluate("d=>localStorage.setItem('ads',d)", DATA); pg.reload(); pg.wait_for_timeout(4000)
    res['cap'] = pg.evaluate("[CAPN(),document.body.classList.contains('cap'),VER]")
    res['auto'] = pg.evaluate("[DB.cfg.ab,DB.cfg.abw,__calls.filter(c=>c[0]=='write').map(c=>c[1])]")
    # xlsx download -> native save + share
    pg.click('button[data-tab="bk"]'); pg.wait_for_timeout(200)
    res['bk_status'] = pg.locator('.stb').all_inner_texts()[:4]
    res['appdl_hidden'] = pg.evaluate("getComputedStyle(document.querySelector('.bsec.dk')).display")
    pg.click('button[data-xlsx="1"]'); pg.wait_for_timeout(600)
    res['xlsx'] = pg.evaluate("__calls.filter(c=>c[0]=='write'||c[0]=='share').slice(-2)")
    pg.click('button[data-bkp="1"]'); pg.wait_for_timeout(800)
    res['backup'] = pg.evaluate("__calls.filter(c=>c[0]=='write'||c[0]=='share').slice(-2)")
    # PDF share
    pid = pg.evaluate("DB.ph.find(p=>p.no=='1533').id")
    pg.evaluate(f"V={{v:'sum',sm:'print',p:{pid},op:{{}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(300)
    res['pt_hidden'] = pg.evaluate("getComputedStyle(document.querySelector('#pt')).display")
    pg.click('#spdf'); pg.wait_for_timeout(6000)
    res['pdf'] = pg.evaluate("__calls.filter(c=>c[0]=='write'||c[0]=='share').slice(-2)")
    # back button
    pg.evaluate("__back()"); pg.wait_for_timeout(100); res['back1'] = pg.evaluate('V.v')
    pg.evaluate("__back()"); pg.wait_for_timeout(100); res['back2'] = pg.evaluate('V.v')
    pg.evaluate("__back()"); pg.evaluate("__back()"); res['exit'] = pg.evaluate("__calls.some(c=>c[0]=='exit')")
    # auto backup prune: simulate 9 older files then rerun
    pg.evaluate("for(let i=1;i<=9;i++)__files['966Ph/auto-backups/966-auto-2026-09-0'+i+'.json']=1;DB.cfg.ab='';autoBackup()"); pg.wait_for_timeout(800)
    res['kept'] = pg.evaluate("Object.keys(__files).filter(k=>k.includes('auto-backups')).length")
    br.close()
print(json.dumps(res, ensure_ascii=False, indent=1)); print('\n'.join(errs) or 'NO ERRORS')

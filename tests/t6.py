import json, os, base64, sys, re
from playwright.sync_api import sync_playwright
DATA = open('/root/.claude/uploads/7db5e8a6-d495-596a-8941-a726d2c69b08/5fd73f2f-966-data-v1.2.json', encoding='utf-8').read()
URL = 'file://' + os.path.abspath('full28.html')
os.makedirs('s6', exist_ok=True)
errs, res, left = [], {}, {}
AR = re.compile(r'[ء-ي][؀-ۿ ]*')
def b64(pg, expr):
    return base64.b64decode(pg.evaluate("async()=>{const b=await (" + expr + ");const a=new Uint8Array(await b.arrayBuffer());let s='';for(let i=0;i<a.length;i++)s+=String.fromCharCode(a[i]);return btoa(s)}"))
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = br.new_context(viewport={'width': 400, 'height': 860}, device_scale_factor=2, accept_downloads=True)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' else None)
    dl_msgs = []
    pg.on('dialog', lambda d: (dl_msgs.append(d.message), d.accept(d.default_value or 'x')))
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.evaluate("d=>{localStorage.setItem('ads',d)}", DATA); pg.reload(); pg.wait_for_timeout(1800)
    def chk(name):
        pg.wait_for_timeout(120)
        t = pg.evaluate("document.body.innerText+' '+[...document.querySelectorAll('[placeholder]')].map(e=>e.placeholder).join(' ')")
        a = sorted(set(x.strip() for x in AR.findall(t) if x.strip()))
        left[name] = a
        pg.screenshot(path=f's6/{name}.png', full_page=True)
    pg.click('button.hmb'); pg.click('button[data-mgo="lang"]'); pg.wait_for_timeout(150); pg.screenshot(path='s6/00_lang_ar.png')
    pg.click('button[data-lang="en"]'); pg.wait_for_timeout(200)
    res['dir'] = pg.evaluate('document.documentElement.dir'); chk('01_lang_en')
    pg.click('button[data-tab="home"]'); chk('02_home')
    pg.click('button.hmb'); pg.wait_for_timeout(100); pg.screenshot(path='s6/02b_menu.png'); pg.evaluate("document.querySelector('.mshade').click()")
    pid = pg.evaluate("DB.ph.find(p=>p.no=='809').id")
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{ws:true,eg:true,__pi:true}},dr:{{}},q:V.q}};render()"); chk('03_ph')
    res['opt_values_ar'] = pg.evaluate("[...document.querySelectorAll('#crg option')].slice(0,2).map(o=>[o.value,o.text])")
    pg.click('button[data-sum="1"]'); chk('04_sum_print')
    open('s6/sum_print.pdf', 'wb').write(b64(pg, 'buildPdf()'))
    pg.click('button[data-sm="mgmt"]'); chk('05_sum_mgmt'); open('s6/sum_mgmt.pdf', 'wb').write(b64(pg, 'buildPdf()'))
    pg.click('button[data-sm="ck"]'); chk('06_sum_ck')
    res['wa_text'] = pg.evaluate("rpText()")[:300]
    pg.click('button[data-tab="month"]'); chk('07_month')
    open('s6/month.pdf', 'wb').write(b64(pg, "buildPdf(monthRepEl(V.mo),'تقرير متابعة شهر '+V.mo)"))
    pg.evaluate("V={v:'calc',op:{},dr:{},q:V.q};render()");pg.wait_for_timeout(200); chk('08_calc')
    pg.click('button[data-tab="revhub"]'); chk('09_revhub')
    pg.click('button[data-rv="2026-10"]'); chk('10_rev')
    pg.click('button[data-tab="all"]')
    for am in ['sec', 'mg', 'sz', 'cmp', 'ph']:
        pg.click(f'button[data-am="{am}"]'); chk('11_all_' + am)
    open('s6/all_ph.pdf', 'wb').write(b64(pg, 'buildPdf()'))
    pg.evaluate("document.querySelector('details.more').open=true")
    with pg.expect_download() as d:
        pg.evaluate("navigator.canShare=()=>false;window.showSaveFilePicker=undefined"); pg.click('#xls')
    d.value.save_as('s6/rep.xlsx')
    pg.click('button[data-tab="bk"]'); chk('12_bk')
    with pg.expect_download() as d:
        pg.click('button[data-xlsx="1"]')
    d.value.save_as('s6/all.xlsx')
    with pg.expect_download() as d:
        pg.click('button[data-looker="1"]')
    d.value.save_as('s6/looker.csv')
    for m in ['gen', 'types', 'set', 'look']:
        pg.click('button.hmb'); pg.click(f'button[data-mgo="{m}"]'); chk('13_' + m)
    pg.click('button[data-tab="home"]'); pg.click('button[data-newp]'); chk('14_add')
    pg.evaluate(f"V={{v:'qe',p:{pid},qi:0,op:{{}},dr:{{}},q:V.q}};render()"); chk('15_qe')
    # data stays Arabic
    res['data_ar'] = pg.evaluate("[DB.ph[0].st,DB.ph[0].rg,DB.ph[0].mod,DB.ph[0].sup]")
    # back to Arabic
    pg.click('button.hmb'); pg.click('button[data-mgo="lang"]'); pg.click('button[data-lang="ar"]'); pg.wait_for_timeout(150)
    res['dir_back'] = pg.evaluate('document.documentElement.dir'); pg.click('button[data-tab="home"]'); pg.screenshot(path='s6/16_back_ar.png')
    res['dialogs'] = dl_msgs[:5]
    br.close()
allleft = sorted(set(x for v in left.values() for x in v))
print(json.dumps(res, ensure_ascii=False, indent=1))
print('LEFT ARABIC:', json.dumps({k: v for k, v in left.items() if v}, ensure_ascii=False, indent=0))
print('\n'.join(errs) or 'NO ERRORS')

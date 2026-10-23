import json, os, base64, sys
from playwright.sync_api import sync_playwright
DATA = open('/root/.claude/uploads/7db5e8a6-d495-596a-8941-a726d2c69b08/5fd73f2f-966-data-v1.2.json', encoding='utf-8').read()
URL = 'file://' + os.path.abspath('full28.html')
os.makedirs('s3', exist_ok=True)
errs, res = [], {}
def b64(pg, expr):
    return base64.b64decode(pg.evaluate("async()=>{const b=await (" + expr + ");const a=new Uint8Array(await b.arrayBuffer());let s='';for(let i=0;i<a.length;i++)s+=String.fromCharCode(a[i]);return btoa(s)}"))
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = br.new_context(viewport={'width': 400, 'height': 860}, device_scale_factor=2, accept_downloads=True)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' else None)
    pg.on('dialog', lambda d: d.accept(d.default_value or '9999'))
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.evaluate("d=>{localStorage.setItem('ads',d)}", DATA); pg.reload(); pg.wait_for_timeout(1800)
    sh = lambda n, f=False: pg.screenshot(path=f's3/{n}.png', full_page=f)
    res['cards'] = pg.locator('.pcard').count(); sh('01_home')
    res['snaps_after_load'] = pg.evaluate('SNAPS.length'); res['idb'] = pg.evaluate('IDB.ok')
    # filter
    pg.click('button[data-flt]'); res['fpanel_visible'] = pg.locator('#fpanel').is_visible()
    pg.select_option('#fs', 'جاري'); res['filtered'] = pg.locator('.pcard').count(); sh('02_filter')
    pg.click('button[data-fclr]')
    # menu
    pg.click('button.hmb'); pg.wait_for_timeout(100); sh('03_menu'); res['menu_items'] = pg.locator('.hmenu button').count()
    for m in ['gen', 'types', 'set', 'look']:
        if not pg.locator('.hmenu').count(): pg.click('button.hmb')
        pg.click(f'button[data-mgo="{m}"]'); pg.wait_for_timeout(150); sh('04_' + m)
    pg.click('button[data-lth="dark"]'); res['th'] = pg.evaluate('DB.cfg.th'); sh('04_look_dark')
    pg.click('button[data-lth=""]'); pg.click('button[data-lfs="18"]'); res['fs'] = pg.evaluate('DB.cfg.fs'); pg.click('button[data-lfs="16"]')
    pg.click('button[data-tab="home"]')
    # pharmacy page
    pg.click('.pcard[data-go] .pc-ln >> nth=0'); pg.wait_for_timeout(200); sh('05_ph')
    res['sbar'] = pg.locator('header .sbar').inner_text()
    pg.evaluate("V.op.dc=true;render()")  # open Die Cut (likely has rows or empty)
    sh('05b_ph_full', True)
    # add flow with stepper on Die Cut
    has_form = pg.locator('details[data-id="dc"] .fm').count()
    if not has_form: pg.click('button[data-fo="dc"]')
    pg.click('details[data-id="dc"] button[data-stp="dc:1"]'); pg.click('details[data-id="dc"] button[data-stp="dc:1"]')
    res['stp_val'] = pg.locator('details[data-id="dc"] input[data-k="q"]').input_value()
    n0 = pg.evaluate("(DB.ph.find(x=>x.id==V.p).rows.dc||[]).length")
    pg.click('button[data-add="dc"]'); res['dc_added'] = pg.evaluate("(DB.ph.find(x=>x.id==V.p).rows.dc||[]).length") - n0
    res['dc_q'] = pg.evaluate("DB.ph.find(x=>x.id==V.p).rows.dc.slice(-1)[0].q")
    # summary + more options
    pg.click('button[data-sum="1"]'); pg.wait_for_timeout(150); sh('06_sum')
    pg.click('#edt'); pg.evaluate("(()=>{const c=document.querySelector('#rp td');c.textContent='X';c.dispatchEvent(new InputEvent('input',{bubbles:true}))})()")
    res['edtd'] = pg.evaluate('EDTD')
    # navigation guard (dialog auto accepts -> navigates)
    pg.click('button[data-tab="month"]'); pg.wait_for_timeout(200); sh('07_month', True)
    res['month_rows'] = pg.locator('button.mrow[data-go]').count()
    open('s3/month.pdf', 'wb').write(b64(pg, "buildPdf(monthRepEl(V.mo),'تقرير شهر')"))
    # calc
    pg.evaluate("V={v:'calc',op:{},dr:{},q:V.q};render()");pg.wait_for_timeout(200)
    pg.fill('input[data-cr="0:h"]', '250'); pg.fill('input[data-cr="0:w"]', '120'); pg.fill('input[data-cr="0:q"]', '4')
    pg.fill('#cfp', '85'); pg.wait_for_timeout(100); sh('08_calc')
    res['calc_tiles'] = pg.locator('#crtiles').inner_text().replace('\n', ' | ')
    pg.select_option('#crph', index=0); pg.click('button[data-crsend]'); pg.wait_for_timeout(150)
    pg.evaluate("V={v:'calc',op:{},dr:{},q:V.q};render()");pg.wait_for_timeout(200); dlg = []
    pg.once('dialog', lambda d: (dlg.append(d.message), d.dismiss()))
    pg.click('button[data-crsend]'); pg.wait_for_timeout(150); res['dup_warn'] = dlg[0][:40] if dlg else None
    # review
    pg.click('button[data-tab="revhub"]'); pg.click('button[data-rv="2026-10"]'); pg.wait_for_timeout(200); sh('09_rev')
    res['icards'] = pg.locator('.icard').count(); res['rvbar'] = pg.locator('.rvbar').is_visible()
    pg.click('button[data-rvdone]'); res['rev_i'] = pg.evaluate('V.rv.i')
    pg.click('button[data-rvp]'); res['rev_state'] = pg.evaluate("revSt(DB.ph.find(x=>x.id==V.p))")
    # bk tab
    pg.click('button[data-tab="bk"]'); pg.wait_for_timeout(150); sh('10_bk', True)
    res['bk_status'] = pg.locator('.stb').all_inner_texts()
    for k, fn in [('xlsx', 's3/out.xlsx'), ('looker', 's3/looker.csv'), ('spec', 's3/spec.json'), ('appdl', 's3/app.html'), ('bkp', 's3/backup.json')]:
        with pg.expect_download() as d:
            if k == 'bkp': pg.evaluate("window.showSaveFilePicker=undefined;navigator.canShare=()=>false")
            pg.click(f'button[data-{k}="1"]')
        d.value.save_as(fn)
    pg.wait_for_timeout(300); res['ue_after_bk'] = pg.evaluate('DB.cfg.ue')
    pg.click('button[data-snapnow]'); res['snaps'] = pg.evaluate('SNAPS.length')
    # reminder at 10 edits
    pg.evaluate("DB.cfg.ue=9;LASTE=0;sv()"); pg.wait_for_timeout(200); res['remind'] = pg.locator('.toast.rem').count()
    # IDB recovery
    pg.wait_for_timeout(500); pg.evaluate("localStorage.removeItem('ads')"); pg.reload(); pg.wait_for_timeout(2000)
    res['recovered_ph'] = pg.evaluate('DB.ph.length')
    sh('11_home_after_recover')
    br.close()
print(json.dumps(res, ensure_ascii=False, indent=1)); print('\n'.join(errs) or 'NO ERRORS')

import json, os, re
from playwright.sync_api import sync_playwright
DATA = open('out3/966-data-v1.3.json', encoding='utf-8').read()
URL = 'file://' + os.path.abspath('full28.html')
os.makedirs('s7', exist_ok=True)
errs, res = [], {}
AR = re.compile(r'[ء-ي][؀-ۿ ]*')
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = br.new_context(viewport={'width': 400, 'height': 860}, device_scale_factor=2, accept_downloads=True,
                         geolocation={'latitude': 24.713551, 'longitude': 46.675296}, permissions=['geolocation'])
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' else None)
    dlg = []
    pg.on('dialog', lambda d: (dlg.append(d.message[:60]), d.accept(d.default_value or 'x')))
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.evaluate("d=>{localStorage.setItem('ads',d)}", DATA); pg.reload(); pg.wait_for_timeout(1800)
    res['ver'] = pg.evaluate('VER'); res['title'] = pg.title()
    res['home_add_btns'] = pg.locator('.pcard button[data-addloc]').count()
    # menu link
    pg.click('button.hmb'); pg.wait_for_timeout(100); pg.screenshot(path='s7/01_menu.png')
    res['menu_href'] = pg.get_attribute('.hmenu a[data-mlink]', 'href')
    with ctx.expect_page() as np:
        pg.click('.hmenu a[data-mlink]')
    res['menu_opened'] = np.value.url; np.value.close(); pg.wait_for_timeout(150)
    res['menu_closed'] = pg.locator('.hmenu').count() == 0
    # add location via home card button
    pid = pg.evaluate("DB.ph.find(p=>p.no=='809').id")
    pg.click(f'.pcard button[data-addloc="{pid}"]'); pg.wait_for_timeout(200)
    res['after_addloc'] = pg.evaluate("[V.v,document.activeElement&&document.activeElement.id]")
    pg.fill('#cloc', 'hello'); pg.locator('#cloc').dispatch_event('change'); pg.wait_for_timeout(100)
    res['bad_loc'] = pg.evaluate("DB.ph.find(x=>x.id==V.p).loc||''")
    pg.fill('#cloc', 'صيدلية الدواء النسيم https://maps.app.goo.gl/AbC123xyz'); pg.locator('#cloc').dispatch_event('change'); pg.wait_for_timeout(150)
    res['loc_saved'] = pg.evaluate("DB.ph.find(x=>x.id==V.p).loc")
    res['rev_state'] = pg.evaluate("revSt(DB.ph.find(x=>x.id==V.p))")
    pg.screenshot(path='s7/02_ph.png')
    res['ph_links'] = pg.evaluate("[...document.querySelectorAll('.phead .locs a')].map(a=>a.href)")
    # coords + geo
    pg.fill('#cloc', '24.7136, 46.6753'); pg.locator('#cloc').dispatch_event('change'); pg.wait_for_timeout(100)
    res['coords'] = pg.evaluate("DB.ph.find(x=>x.id==V.p).loc")
    pg.click('button[data-geo="cloc"]'); pg.wait_for_timeout(600)
    res['geo'] = pg.evaluate("DB.ph.find(x=>x.id==V.p).loc")
    # clicking location link on home card must not open pharmacy page
    pg.click('button[data-tab="home"]'); pg.wait_for_timeout(150)
    with ctx.expect_page() as np:
        pg.click(f'.pcard[data-go="{pid}"] a.locb')
    res['card_link'] = np.value.url; np.value.close(); pg.wait_for_timeout(100)
    res['view_after_card_link'] = pg.evaluate('V.v')
    pg.screenshot(path='s7/03_home.png')
    # add new pharmacy with location
    pg.click('button[data-newp]'); pg.fill('#pno', '9100'); pg.click('button[data-geo="ploc"]'); pg.wait_for_timeout(600)
    res['ploc'] = pg.input_value('#ploc'); pg.screenshot(path='s7/04_add.png', full_page=True)
    pg.click('#addp'); pg.wait_for_timeout(150); res['new_loc'] = pg.evaluate("DB.ph.slice(-1)[0].loc")
    # copy pharmacy drops location
    pg.evaluate("cpyPh(DB.ph.find(p=>p.no=='809'))"); res['copy_loc'] = pg.evaluate("DB.ph.slice(-1)[0].loc===undefined")
    # review screen chips
    pg.click('button[data-tab="revhub"]'); pg.click('button[data-rv="2026-10"]'); pg.wait_for_timeout(150)
    res['rev_chips'] = pg.locator('.rvc .locs .locb').count(); pg.screenshot(path='s7/05_rev.png')
    # exports
    pg.click('button[data-tab="bk"]')
    with pg.expect_download() as d: pg.click('button[data-xlsx="1"]')
    d.value.save_as('s7/all.xlsx')
    with pg.expect_download() as d: pg.click('button[data-looker="1"]')
    d.value.save_as('s7/looker.csv')
    # english
    pg.evaluate("DB.cfg.lang='en';render()"); pg.click('button[data-tab="home"]'); pg.wait_for_timeout(150)
    pg.click('button.hmb'); pg.wait_for_timeout(100); pg.screenshot(path='s7/06_menu_en.png')
    pg.mouse.click(200, 800)
    pg.evaluate(f"V={{v:'ph',p:{pid},op:{{__pi:true}},dr:{{}},q:V.q}};render()"); pg.wait_for_timeout(150)
    t = pg.evaluate("document.body.innerText+' '+[...document.querySelectorAll('[placeholder]')].map(e=>e.placeholder).join(' ')")
    res['en_left'] = sorted(set(x.strip() for x in AR.findall(t) if x.strip()))
    pg.screenshot(path='s7/07_ph_en.png')
    res['dialogs'] = dlg
    br.close()
print(json.dumps(res, ensure_ascii=False, indent=1)); print('\n'.join(errs) or 'NO ERRORS')

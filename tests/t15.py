import json, os, re, subprocess
from playwright.sync_api import sync_playwright
W = '/home/claude/work/'; OUT = W + 's15/'; os.makedirs(OUT, exist_ok=True)
A = '/mnt/user-data/attachments/7db5e8a6-d495-596a-8941-a726d2c69b08/'
IM = [A + x + '-image.jpg' for x in ('e8e6622a', '6911642a', '112e5fd3', 'd0fc00a1', '5313de8e', '84ea4863')]
DATA = open(W + 'out6/966-data-v1.2.json', encoding='utf-8').read()
JS = W + 'cust/عهدة شهر 10-2026 - للاستيراد.json'
URL = 'file://' + W + 'new14.html'
errs, res, dl = [], {}, []
with sync_playwright() as pw:
    br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    ctx = br.new_context(viewport={'width': 400, 'height': 860}, device_scale_factor=2, accept_downloads=True)
    pg = ctx.new_page()
    pg.on('pageerror', lambda e: errs.append('PAGEERR ' + str(e)))
    pg.on('console', lambda m: errs.append('CONSOLE ' + m.text) if m.type == 'error' else None)
    pg.on('dialog', lambda x: (dl.append(x.message[:140]), x.accept()))
    pg.goto(URL); pg.wait_for_timeout(300)
    pg.evaluate("d=>localStorage.setItem('ads',d)", DATA); pg.reload(); pg.wait_for_timeout(2000)
    res['ver'] = pg.evaluate('VER'); res['jsqr'] = pg.evaluate('typeof jsQR')
    pg.click('button.hmb'); pg.wait_for_timeout(150); res['menu_has'] = pg.evaluate("!!document.querySelector('[data-mgo=cust]')")
    pg.click('[data-mgo=cust]'); pg.wait_for_timeout(300)
    res['view'] = pg.evaluate('V.v'); pg.screenshot(path=OUT + '01_empty.png')
    # import the 40 invoices
    pg.set_input_files('#cjson', JS); pg.wait_for_timeout(600)
    res['import'] = pg.evaluate("[CU().cur,cMo().items.length,cTot(cMo()),cRem(cMo()),cMo().open]")
    res['import_alert'] = dl[-1] if dl else ''
    res['kpi'] = pg.evaluate("[...document.querySelectorAll('.ckpi b')].map(b=>[b.textContent,getComputedStyle(b).color])")
    res['rows_old'] = pg.evaluate("document.querySelectorAll('.ctab tr.co-old').length")
    res['np_rows'] = pg.evaluate("document.querySelectorAll('.ctab small.cnp').length")
    pg.screenshot(path=OUT + '02_list.png', full_page=True)
    # re-import -> all duplicates
    pg.set_input_files('#cjson', JS); pg.wait_for_timeout(500); res['reimport_alert'] = dl[-1]
    res['after_reimport'] = pg.evaluate("cMo().items.length")
    # images -> QR
    n0 = pg.evaluate("cMo().items.length")
    pg.set_input_files('#cimgs', IM); pg.wait_for_timeout(1500)
    for _ in range(60):
        if pg.evaluate("V.v") == 'ced': break
        pg.wait_for_timeout(500)
    q = []
    for i in range(len(IM)):
        d = pg.evaluate("(()=>{const d=V.ce;return {src:d.src,comp:d.comp,amt:d.amt,dt:d.dt,tm:d.tm,kind:d.kind,desc:d.desc,car:d.car,alt:d._alt,imgs:(d.imgs||[]).length}})()")
        q.append(d)
        if i == 0: pg.screenshot(path=OUT + '03_editor_qr.png', full_page=True)
        if d['src'] == 'img':
            pg.screenshot(path=OUT + '04_editor_noqr.png', full_page=True)
            pg.fill('input[data-cf=comp]', 'رؤية فيجن للشقق المخدومة'); pg.dispatch_event('input[data-cf=comp]', 'change'); pg.wait_for_timeout(150)
            pg.fill('input[data-cf=amt]', '160'); pg.fill('input[data-cf=dt]', '2026-10-16')
        pg.click('button[data-csave]'); pg.wait_for_timeout(400)
    res['qr_results'] = q
    res['after_images'] = pg.evaluate("[V.v,cMo().items.length]"); res['dup_alerts'] = [x for x in dl if 'شبهها' in x]
    # manual add with meal rule + no-paper flag
    pg.click('button[data-cman]'); pg.wait_for_timeout(300)
    pg.fill('input[data-cf=comp]', 'مطعم تجربة'); pg.dispatch_event('input[data-cf=comp]', 'change'); pg.wait_for_timeout(100)
    pg.fill('input[data-cf=tm]', '20:15'); pg.dispatch_event('input[data-cf=tm]', 'change'); pg.wait_for_timeout(100)
    pg.fill('input[data-cf=amt]', '33.5'); pg.check('#cnp'); pg.wait_for_timeout(100)
    res['manual_draft'] = pg.evaluate("[V.ce.kind,V.ce.desc,V.ce.note]")
    pg.screenshot(path=OUT + '05_manual.png', full_page=True)
    pg.click('button[data-csave]'); pg.wait_for_timeout(300)
    # edit an invoice by tapping its row
    pg.click('.ctab tr[data-ced] >> nth=3'); pg.wait_for_timeout(300)
    res['edit_view'] = pg.evaluate("[V.v,V.ce&&V.ce.comp]")
    pg.fill('input[data-cf=amt]', '27'); pg.click('button[data-csave]'); pg.wait_for_timeout(300)
    res['after_edit_total'] = pg.evaluate("cTot(cMo())")
    pg.reload(); pg.wait_for_timeout(1500)
    res['persist'] = pg.evaluate("[CU().cur,cMo().items.length,cTot(cMo())]")
    pg.evaluate("goV({v:'cust',op:{},dr:{},q:V.q})"); pg.wait_for_timeout(300)
    # Excel
    pg.evaluate('delete window.showSaveFilePicker;window.showSaveFilePicker=undefined')
    with pg.expect_download() as d:
        pg.click('button[data-cxl=save]')
    d.value.save_as(OUT + 'cust.xlsx'); res['xlsx_name'] = d.value.suggested_filename
    # PDF (build only)
    b64 = pg.evaluate("async()=>{const b=await buildPdf(custPdfEl(CU().cur),'x');const a=new Uint8Array(await b.arrayBuffer());let s='';for(let i=0;i<a.length;i++)s+=String.fromCharCode(a[i]);return btoa(s)}")
    import base64; open(OUT + 'cust.pdf', 'wb').write(base64.b64decode(b64))
    # full backup contains invoice images
    res['backup_imgs'] = pg.evaluate("fullBackupWithFiles().then(o=>Object.keys(o._files).filter(k=>/^cimg:/.test(k)).length)")
    # new month (option b)
    pg.click('button[data-cnew="1"]'); pg.wait_for_timeout(200)
    res['new_month_text'] = pg.inner_text('.cnew')[:200]
    pg.screenshot(path=OUT + '06_newmonth.png')
    pg.click('.cnew button.pr'); pg.wait_for_timeout(300)
    res['new_month'] = pg.evaluate("[CU().cur,cMo().open,cMo().items.length]")
    pg.select_option('#cmosel', '2026-10'); pg.wait_for_timeout(200); res['back_month'] = pg.evaluate("[CU().cur,cMo().items.length]")
    # English
    pg.evaluate("DB.cfg.lang='en';svq();render()"); pg.wait_for_timeout(500)
    t = pg.evaluate("document.querySelector('main').innerText"); res['en_left'] = sorted(set(re.findall(r'[ء-ي][ء-ي ]{2,}', t)))[:25]
    pg.screenshot(path=OUT + '07_en.png')
    br.close()
for k, v in res.items(): print(k, '=>', v)
print('dialogs', dl); print('ERRS', errs[:10])
